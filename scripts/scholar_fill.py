#!/usr/bin/env python3
"""Fill publications from their Google Scholar entries (abstract, venue, publisher link, PDF, date).

Google Scholar has no API: this uses the `scholarly` library politely (one profile request + one request per paper,
8–15 s apart, resumable cache) and is meant to be run locally, not from CI. It stops at the first sign of blocking
(CAPTCHA / "unusual traffic") instead of trying to get around it.

Only fills *missing* fields (abstract, venue, links, date) and respects `sync.locked`.
Usage: .tools/venv/bin/python scripts/scholar_fill.py TODO.json [--new NEW.json] [--cache CACHE.json]
  TODO.json: [{"slug": ..., "gs_id": ...}]   NEW.json: [{"id": gs_id, "title": ...}] → creates new pages
"""
import argparse
import datetime as dt
import json
import random
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_publications as sp  # noqa: E402
from scholarly import scholarly  # noqa: E402

TYPE = {"journal": "article-journal", "conference": "paper-conference", "book": "chapter", "patent": "patent"}


def load_profile():
    a = scholarly.fill(scholarly.search_author_id(sp.load_params().get("scholar_id", "CPuApzoAAAAJ")), sections=["publications"])
    return {p["author_pub_id"]: p for p in a["publications"]}


def refresh_stats():
    """Profile totals (citations, h-index, i10) → data/scholar.json, which the banner and the PI profile read."""
    a = scholarly.fill(scholarly.search_author_id(sp.load_params().get("scholar_id", "CPuApzoAAAAJ")), sections=["basics", "indices"])
    if not a.get("citedby"):
        return
    stats = {"citations": a["citedby"], "h_index": a.get("hindex"), "i10_index": a.get("i10index"),
             "source": "Google Scholar", "updated": dt.date.today().isoformat()}
    (sp.ROOT / "data/scholar.json").write_text(json.dumps(stats, indent=2))
    print(f"scholar.json: {stats['citations']} citations, h {stats['h_index']}, i10 {stats['i10_index']}")


def details(pub):
    f = scholarly.fill(pub)
    b = f.get("bib", {})
    venue = b.get("journal") or b.get("conference") or b.get("booktitle") or b.get("publisher") or ""
    kind = "journal" if b.get("journal") else "conference" if (b.get("conference") or b.get("booktitle")) else ""
    return {"title": b.get("title", ""), "abstract": (b.get("abstract") or "").strip(), "venue": venue, "kind": kind,
            "year": b.get("pub_year"), "authors": [a.strip() for a in (b.get("author") or "").split(" and ") if a.strip()],
            "pub_url": f.get("pub_url") or "", "eprint": f.get("eprint_url") or "", "cites": f.get("num_citations", 0),
            "volume": b.get("volume"), "pages": b.get("pages"), "publisher": b.get("publisher")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("todo")
    ap.add_argument("--new")
    ap.add_argument("--cache", default=str(sp.ROOT / ".tools/scholar_cache.json"))
    args = ap.parse_args()
    cache = json.loads(Path(args.cache).read_text()) if Path(args.cache).exists() else {}
    todo = [t for t in json.loads(Path(args.todo).read_text()) if t.get("gs_id")]
    new = json.loads(Path(args.new).read_text()) if args.new else []
    wanted = [t["gs_id"] for t in todo] + [n["id"] for n in new]
    try:
        refresh_stats()
    except Exception as e:  # noqa: BLE001 — keep the previous snapshot
        print(f"! scholar stats not refreshed: {e}")
    if any(w not in cache for w in wanted):
        pubs = load_profile()
        for gid in wanted:
            if gid in cache or gid not in pubs:
                continue
            try:
                cache[gid] = details(pubs[gid])
            except Exception as e:  # noqa: BLE001 — most likely blocked: stop, keep what we have
                print(f"! stopped at {gid}: {e}")
                break
            Path(args.cache).write_text(json.dumps(cache, indent=1, ensure_ascii=False))
            print(f"· {cache[gid]['title'][:70]}", flush=True)
            time.sleep(random.uniform(8, 15))

    filled = 0
    for t in todo:
        d = cache.get(t["gs_id"])
        if not d:
            continue
        p = sp.ROOT / "content/publications" / t["slug"] / "index.md"
        fm, body = sp.read_page(p)
        locked = set((fm.get("sync") or {}).get("locked") or [])
        ch = []
        if d["abstract"] and "abstract" not in locked and len((fm.get("abstract") or "").strip()) < 200:
            fm["abstract"] = re.sub(r"\s+", " ", d["abstract"]); ch.append("abstract")
        cur = (fm.get("publication") or {}).get("name", "") if isinstance(fm.get("publication"), dict) else ""
        if d["venue"] and "publication" not in locked and (not cur or cur.lower() in ("springer", "springer nature", "cited here", "lecture notes in computer science")):
            fm["publication"] = {"name": d["venue"]}; ch.append("venue")
        links = fm.get("links") or []
        have = {l.get("url") for l in links}
        if d["pub_url"] and d["pub_url"] not in have and not fm.get("doi") and "links" not in locked:
            links.append({"type": "source", "url": d["pub_url"], "name": "Publisher"}); ch.append("publisher link")
        if d["eprint"] and d["eprint"] not in have and not any(l.get("type") == "pdf" for l in links) and "links" not in locked:
            links.append({"type": "pdf", "url": d["eprint"]}); ch.append("pdf")
        fm["links"] = links
        if d["year"] and str(fm.get("date", "")).startswith("1970") and "date" not in locked:
            fm["date"], fm["draft"] = f"{d['year']}-01-01", False; ch.append("date")
        sync = fm.setdefault("sync", {})
        sync["scholar"] = t["gs_id"]
        sync["citations"] = max(sync.get("citations") or 0, d["cites"] or 0)
        fm["venue"] = sp.match_venue((fm.get("publication") or {}).get("name", "")) or fm.get("venue", "")
        sp.write_page(p, fm, body)
        if ch:
            filled += 1
            print(f"~ {t['slug']}: {', '.join(ch)}")

    for n in new:
        d = cache.get(n["id"])
        if not d:
            continue
        slug = sp.slugify(d["title"], str(d["year"] or ""), n["id"].split(":")[-1])
        dest = sp.ROOT / "content/publications" / slug
        if dest.exists():
            continue
        fm = {"title": d["title"], "date": f"{d['year']}-01-01" if d["year"] else "1970-01-01", "draft": not d["year"],
              "authors": [sp.canonical_author(a) for a in d["authors"]],
              "publication_types": [TYPE.get(d["kind"], "paper-conference" if d["kind"] else "manuscript")],
              "publication": {"name": d["venue"]}, "venue": sp.match_venue(d["venue"]), "doi": "", "abstract": d["abstract"],
              "themes": sp.infer_themes(d["title"], d["abstract"]), "projects": [], "datasets": [], "tags": [], "featured": False,
              "links": ([{"type": "source", "url": d["pub_url"], "name": "Publisher"}] if d["pub_url"] else []) + ([{"type": "pdf", "url": d["eprint"]}] if d["eprint"] else []),
              "slidev": "", "hugoblox": {}, "sync": {"source": "scholar", "scholar": n["id"], "citations": d["cites"], "needs_review": True, "locked": []}}
        sp.write_page(dest / "index.md", fm, "")
        print(f"+ {slug}")
    print(f"filled {filled}")


if __name__ == "__main__":
    main()
