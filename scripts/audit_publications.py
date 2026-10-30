#!/usr/bin/env python3
"""Verify every publication against OpenAlex / Crossref / Semantic Scholar / arXiv and (optionally) fix it.

For each content/publications/*/index.md:
  1. find the canonical record — by DOI, else by title (OpenAlex, then Crossref);
     a match is accepted only if title similarity >= 0.93, year differs by <= 1 and >= 1 author family name overlaps;
  2. compare and, with --apply, fix: DOI, publisher landing page, venue name/ISSN/type, publication date,
     abstract (OpenAlex → Crossref → Semantic Scholar → arXiv), and a truncated author list ("others");
  3. check that the publisher / PDF / code links resolve (403/429 from bot-blocking publishers count as "unverified", not broken);
  4. write docs/publication-audit.md (and .json) listing what was verified, changed, or needs a human.

Fields listed in a page's `sync.locked` are never touched. Curated fields (themes, projects, datasets, tags,
featured, slidev, body text) are never touched.

Usage: python3 scripts/audit_publications.py [--apply] [--only SLUG] [--no-links]
"""
import argparse
import datetime as dt
import difflib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_publications as sp  # noqa: E402  (shared helpers: get_json, norm_title, reconstruct_abstract, canonical_author …)

ROOT = sp.ROOT
MAILTO = sp.MAILTO


def sim(a, b):
    return difflib.SequenceMatcher(None, sp.norm_title(a), sp.norm_title(b)).ratio()


def family(name):
    parts = re.sub(r"[^\w\s-]", " ", name or "").split()
    return parts[-1].lower() if parts else ""


def author_overlap(ours, theirs):
    a = {family(x) for x in ours if x and x.lower() not in ("others", "et al")}
    b = {family(x) for x in theirs}
    return len(a & b)


def oa(path):
    sep = "&" if "?" in path else "?"
    return sp.get_json(f"https://api.openalex.org/{path}" + (f"{sep}mailto={MAILTO}" if MAILTO else ""))


def openalex_candidates(fm):
    try:
        return _openalex_candidates(fm)
    except sp.RateLimited as e:
        print(f"  ! OpenAlex rate-limited ({e}); using Crossref", flush=True)
        return []


def _openalex_candidates(fm):
    doi = sp.norm_doi(fm.get("doi"))
    if doi:
        w = oa(f"works/doi:{urllib.parse.quote(doi)}")
        if w:
            return [w]
    q = urllib.parse.quote(re.sub(r"[^\w\s-]", " ", fm.get("title") or "")[:250])
    j = oa(f"works?search={q}&per-page=5")
    return (j or {}).get("results", [])


def crossref_candidate(fm):
    q = urllib.parse.quote(fm.get("title") or "")
    j = sp.get_json(f"https://api.crossref.org/works?rows=5&query.author=Albarqouni&query.bibliographic={q}" + (f"&mailto={MAILTO}" if MAILTO else ""))
    for it in ((j or {}).get("message") or {}).get("items", []):
        title = (it.get("title") or [""])[0]
        year = ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0]
        authors = [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in it.get("author", [])]
        yield {"title": title, "doi": it.get("DOI", ""), "year": year, "authors": authors,
               "venue": (it.get("container-title") or [""])[0], "type": it.get("type"),
               "abstract": re.sub(r"<[^>]+>", "", it.get("abstract", "")).strip(), "url": (it.get("resource") or {}).get("primary", {}).get("URL", ""),
               "issn": it.get("ISSN", [])}


def accept(fm, title, year, authors):
    y0 = str(fm.get("date") or "")[:4]
    okyear = (not y0.isdigit()) or y0 == "1970" or (year and abs(int(y0) - int(year)) <= 1)
    s = sim(fm.get("title"), title)
    return s >= 0.93 and okyear and author_overlap(fm.get("authors") or [], authors) >= 1, s


def arxiv_abstract(arxiv_id):
    try:
        req = urllib.request.Request(f"https://export.arxiv.org/api/query?id_list={arxiv_id}", headers={"User-Agent": sp.UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            root = ET.fromstring(r.read())
        ns = {"a": "http://www.w3.org/2005/Atom"}
        e = root.find("a:entry/a:summary", ns)
        return re.sub(r"\s+", " ", e.text).strip() if e is not None and e.text else ""
    except Exception:  # noqa: BLE001
        return ""


def s2(doi=None, title=None):
    fields = "title,abstract,externalIds,openAccessPdf,year,venue,publicationVenue"
    if doi:
        return sp.get_json(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi)}?fields={fields}") or {}
    j = sp.get_json(f"https://api.semanticscholar.org/graph/v1/paper/search/match?query={urllib.parse.quote(title or '')}&fields={fields}")
    return ((j or {}).get("data") or [{}])[0]


def check_url(url):
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 (compatible; comi-lab-link-check)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        if e.code in (405, 501):  # HEAD not allowed → try GET
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=20) as r:
                    return r.status
            except urllib.error.HTTPError as e2:
                return e2.code
            except Exception:  # noqa: BLE001
                return 0
        return e.code
    except Exception:  # noqa: BLE001
        return 0


def audit(path, apply, check_links):
    fm, body = sp.read_page(path)
    locked = set((fm.get("sync") or {}).get("locked") or [])
    rec = {"slug": path.parent.name, "title": fm.get("title"), "status": "not found", "changes": [], "issues": [], "source": ""}
    match = None
    for w in openalex_candidates(fm):
        authors = [a["author"]["display_name"] for a in w.get("authorships", [])]
        ok, s = accept(fm, w.get("title"), w.get("publication_year"), authors)
        if ok:
            match = ("openalex", w, authors, s)
            break
    if not match:
        for c in crossref_candidate(fm):
            ok, s = accept(fm, c["title"], c["year"], c["authors"])
            if ok:
                match = ("crossref", c, c["authors"], s)
                break
    if not match:
        rec["issues"].append("no matching record in OpenAlex/Crossref — check title or add the DOI manually")
        return rec, fm, body
    rec["status"] = "pending"

    src, w, authors, s = match
    rec["source"], rec["similarity"] = src, round(s, 3)
    new = {}
    if src == "openalex":
        loc = w.get("primary_location") or {}
        source = loc.get("source") or {}
        new["doi"] = sp.norm_doi(w.get("doi"))
        new["venue_name"] = source.get("display_name") or ""
        new["issn"] = source.get("issn") or []
        new["source_id"] = (source.get("id") or "").rsplit("/", 1)[-1]
        new["source_type"] = source.get("type") or ""
        new["landing"] = loc.get("landing_page_url") or ""
        new["date"] = w.get("publication_date") or ""
        new["abstract"] = sp.reconstruct_abstract(w.get("abstract_inverted_index"))
        new["oa_pdf"] = (w.get("best_oa_location") or {}).get("pdf_url") or ""
        new["openalex"] = (w.get("id") or "").rsplit("/", 1)[-1]
        new["type"] = w.get("type")
        new["citations"] = w.get("cited_by_count", 0)
    else:
        new.update({"doi": w["doi"].lower(), "venue_name": w["venue"], "issn": w["issn"], "landing": w["url"],
                    "abstract": w["abstract"], "date": f"{w['year']}-01-01" if w["year"] else "", "type": w["type"]})
    if not new.get("abstract") and new.get("doi"):
        new["abstract"] = sp.crossref_abstract(new["doi"])
    arxiv = ""
    if not new.get("abstract"):
        x = s2(new.get("doi") or None, fm.get("title"))
        time.sleep(1.1)
        if x and sim(x.get("title"), fm.get("title")) >= 0.93:
            new["abstract"] = x.get("abstract") or ""
            arxiv = (x.get("externalIds") or {}).get("ArXiv") or ""
            if not new.get("oa_pdf"):
                new["oa_pdf"] = (x.get("openAccessPdf") or {}).get("url") or ""
    if not new.get("abstract") and arxiv:
        new["abstract"] = arxiv_abstract(arxiv)
        rec["abstract_source"] = "arXiv"

    def change(field, value, why):
        if field in locked or value in (None, "", []):
            return
        if fm.get(field) != value:
            rec["changes"].append(f"{field}: {why}")
            fm[field] = value

    # DOI
    if new.get("doi") and sp.norm_doi(fm.get("doi")) != new["doi"]:
        change("doi", new["doi"], "set" if not fm.get("doi") else f"corrected from {fm.get('doi')}")
    # venue
    cur_venue = (fm.get("publication") or {}).get("name", "") if isinstance(fm.get("publication"), dict) else ""
    junk = (not cur_venue) or cur_venue.lower() in ("springer", "springer nature", "springer international publishing", "cited here",
                                                    "lecture notes in computer science") or "(if:" in cur_venue.lower()
    preprint = re.search(r"arxiv|medrxiv|biorxiv|research square|ssrn", new.get("venue_name") or "", re.I)
    if preprint and cur_venue and not junk and not re.search(r"arxiv", cur_venue, re.I):
        new["venue_name"] = ""  # never replace a published venue with its preprint
    if new.get("venue_name") and "venue" not in locked and (junk or sim(cur_venue, new["venue_name"]) < 0.5 and src == "openalex"):
        if not junk and not ("arxiv" in cur_venue.lower() and "arxiv" in new["venue_name"].lower()):
            rec["issues"].append(f"venue differs: site='{cur_venue}' vs {src}='{new['venue_name']}' (updated)")
        fm["publication"] = {"name": new["venue_name"]}
        rec["changes"].append("publication.name")
    if new.get("venue_name"):
        key = sp.match_venue(fm["publication"]["name"] if isinstance(fm.get("publication"), dict) else new["venue_name"])
        if key and fm.get("venue") != key and "venue" not in locked:
            fm["venue"] = key
            rec["changes"].append(f"venue: {key}")
    # date (only fill unknown/1970 or fix year mismatch > 0)
    cur_date = str(fm.get("date") or "")
    if new.get("date") and "date" not in locked and (cur_date.startswith("1970") or cur_date[:4] != new["date"][:4]):
        if not cur_date.startswith("1970"):
            rec["issues"].append(f"year differs: site={cur_date[:4]} record={new['date'][:4]} (updated)")
        fm["date"] = new["date"]
        fm["draft"] = False
        rec["changes"].append("date")
    # abstract: fill when missing or clearly a stub
    cur_abs = (fm.get("abstract") or "").strip()
    if new.get("abstract") and "abstract" not in locked:
        if len(cur_abs) < 200:
            fm["abstract"] = new["abstract"]
            rec["changes"].append("abstract")
        elif sim(cur_abs[:300], new["abstract"][:300]) < 0.5:
            rec["issues"].append("site abstract differs from the record — kept the site version, please check")
    if not (fm.get("abstract") or "").strip():
        rec["issues"].append("no abstract available from any source — add it by hand")
    # authors: replace truncated lists ("others") or initial-only lists with the full canonical list
    cur_auth = fm.get("authors") or []
    if "authors" not in locked and authors and (any(a.lower() in ("others", "et al", "et al.") for a in cur_auth) or len(cur_auth) < len(authors)):
        fm["authors"] = [sp.canonical_author(a) for a in authors]
        rec["changes"].append(f"authors: {len(cur_auth)} → {len(authors)}")
    # links: publisher landing page + open-access PDF
    links = fm.get("links") or []
    have = {l.get("type") for l in links}
    if new.get("oa_pdf") and "pdf" not in have and "links" not in locked:
        links.append({"type": "pdf", "url": new["oa_pdf"]})
        rec["changes"].append("links.pdf")
    if new.get("landing") and not fm.get("doi") and "source" not in have and "links" not in locked:
        links.append({"type": "source", "url": new["landing"], "name": "Publisher"})
        rec["changes"].append("links.publisher")
    fm["links"] = links
    if fm.get("doi"):
        fm.setdefault("hugoblox", {}).setdefault("ids", {})["doi"] = fm["doi"]
    sync = dict(fm.get("sync") or {})
    sync.update({"verified": dt.date.today().isoformat(), "verified_by": src, "issn": new.get("issn") or [],
                 "source_id": new.get("source_id", ""), "source_type": new.get("source_type", "")})
    if new.get("openalex"):
        sync["openalex"] = new["openalex"]
        sync["citations"] = max(sync.get("citations") or 0, new.get("citations") or 0)
    sync.pop("needs_review", None) if not rec["issues"] else None
    fm["sync"] = sync

    if check_links:
        urls = ([f"https://doi.org/{fm['doi']}"] if fm.get("doi") else []) + [l["url"] for l in fm.get("links") or [] if l.get("url")]
        for u in urls:
            code = check_url(u)
            if code in (404, 410) or code == 0 and "doi.org" in u:
                rec["issues"].append(f"broken link ({code or 'no response'}): {u}")
    rec["status"] = "verified" if not rec["issues"] else "check"
    return rec, fm, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--no-links", action="store_true")
    ap.add_argument("--force", action="store_true", help="re-check pages that were already verified")
    args = ap.parse_args()
    pages = sorted((ROOT / "content/publications").glob("*/index.md"))
    if args.only:
        pages = [p for p in pages if p.parent.name == args.only]
    report = []
    prev = {}
    pj = ROOT / "docs/publication-audit.json"
    if pj.exists():
        prev = {r["slug"]: r for r in json.loads(pj.read_text())}
    for i, p in enumerate(pages, 1):
        if not args.force and prev.get(p.parent.name, {}).get("status") == "verified":
            report.append(prev[p.parent.name])
            continue
        try:
            rec, fm, body = audit(p, args.apply, not args.no_links)
        except sp.RateLimited as e:
            print(f"[{i}/{len(pages)}] deferred  {p.parent.name}  ({e})", flush=True)
            report.append({"slug": p.parent.name, "title": "", "status": "deferred", "changes": [], "issues": [str(e)], "source": ""})
            continue
        report.append(rec)
        print(f"[{i}/{len(pages)}] {rec['status']:9} {rec['slug']}  {'; '.join(rec['changes'])}  {' | '.join(rec['issues'])}", flush=True)
        if args.apply and rec["source"]:
            sp.write_page(p, fm, body)
    out = ROOT / "docs"
    out.mkdir(exist_ok=True)
    (out / "publication-audit.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    counts = {s: sum(r["status"] == s for r in report) for s in ("verified", "check", "not found")}
    lines = [f"# Publication audit — {dt.date.today().isoformat()}", "",
             f"**{counts['verified']}** verified · **{counts['check']}** need a look · **{counts['not found']}** not found in OpenAlex/Crossref", "",
             "A record counts as *verified* when title (≥ 93 % similar), year (±1) and at least one author match an OpenAlex or Crossref record,",
             "and the abstract and publisher link come from that record. Re-run: `python3 scripts/audit_publications.py --apply`.", ""]
    for status, title in (("not found", "Not found — fix the title or add the DOI by hand"), ("check", "Needs a human look"), ("verified", "Verified")):
        rows = [r for r in report if r["status"] == status]
        if not rows:
            continue
        lines += [f"## {title} ({len(rows)})", "", "| page | issues | changes made |", "|---|---|---|"]
        for r in rows:
            lines.append(f"| [{r['title']}](../content/publications/{r['slug']}/index.md) | {'<br>'.join(r['issues'])} | {', '.join(r['changes'])} |")
        lines.append("")
    (out / "publication-audit.md").write_text("\n".join(lines))
    print(counts)


if __name__ == "__main__":
    main()
