#!/usr/bin/env python3
"""Sync publications from Google Scholar and enrich them with OpenAlex / Crossref / Semantic Scholar.

Pipeline
  1. Discover   — papers on the Google Scholar profile (via `scholarly`, if installed and not blocked);
                  falls back to OpenAlex works of the lab PI (by OpenAlex author id or ORCID).
  2. Match      — against existing content/publications/* by DOI or normalised title.
  3. Enrich     — DOI, abstract, venue, type, authors, date, open-access PDF, code links (OpenAlex → Crossref → S2).
  4. Write      — new pages get `sync.needs_review: true`; existing pages only get *missing* fields filled
                  (never overwrites curated fields; list any field in `sync.locked` to protect it entirely).
  5. Extras     — data/scholar.json (total citations, h-index), optional teaser figure from the OA PDF
                  (needs PyMuPDF), optional SJR quartile refresh (--sjr scimagojr.csv).

Usage
  python3 scripts/sync_publications.py [--dry-run] [--limit N] [--sjr path/to/scimagojr.csv] [--no-scholar]

Environment: OPENALEX_MAILTO (polite pool), S2_API_KEY (optional).
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PUBS = ROOT / "content/publications"
MAILTO = os.environ.get("OPENALEX_MAILTO", "")
OPENALEX_KEY = os.environ.get("OPENALEX_API_KEY", "")  # free key from openalex.org — anonymous use has a tiny shared daily budget


class RateLimited(Exception):
    """Raised when an API asks us to come back much later (e.g. OpenAlex daily budget exhausted)."""
UA = "albarqouni-lab-site/1.0 (" + (MAILTO or "https://github.com/albarqouni") + ")"

CSL = {"article": "article-journal", "journal-article": "article-journal", "proceedings-article": "paper-conference",
       "book-chapter": "chapter", "book": "book", "dissertation": "thesis", "preprint": "preprint", "posted-content": "preprint",
       "review": "article-journal", "conference-abstract": "abstract", "meeting-abstract": "abstract", "editorial": "article-journal", "report": "report"}


# proceedings titles of MICCAI satellite workshops (published in LNCS without "workshop" in the book title)
MICCAI_WORKSHOPS = (r"ophthalmic medical image analysis|brainlesion|clinical image-based procedures|machine learning in medical imaging"
                    r"|domain adaptation and representation transfer|distributed,? (and )?collaborative|deep learning and data labeling"
                    r"|data engineering in medical imaging|uncertainty for safe utilization|simplifying medical ultrasound"
                    r"|medical image learning with limited|applications of medical artificial intelligence|resource-efficient medical image"
                    r"|interpretability of machine intelligence|fairness of ai in medical imaging|predictive intelligence in medicine"
                    r"|graphs in biomedical image analysis|computational pathology|deep generative models|medical optical imaging")

SKIP_TYPES = {"dataset", "paratext", "peer-review", "erratum", "supplementary-materials", "retraction", "other", "letter"}

# ------------------------------------------------------------------ helpers
def get_json(url, headers=None, retries=3):
    if OPENALEX_KEY and "api.openalex.org" in url and "api_key=" not in url:
        url += ("&" if "?" in url else "?") + "api_key=" + OPENALEX_KEY
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 429:
                wait = int(e.headers.get("retry-after") or 5)
                if wait > 120:
                    raise RateLimited(f"{url.split('?')[0]} — retry after {wait}s")
                time.sleep(max(wait, 5 * (i + 1)))
                continue
            print(f"  ! {e.code} {url[:100]}", file=sys.stderr)
            return None
        except Exception as e:  # noqa: BLE001 — network hiccups should not stop the sync
            print(f"  ! {e} {url[:100]}", file=sys.stderr)
            time.sleep(2)
    return None


def norm_title(t):
    t = unicodedata.normalize("NFKD", html.unescape(t or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", t)


def slugify(t, year, fallback=""):
    ascii_t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    words = [w for w in re.sub(r"[^a-z0-9 ]+", " ", ascii_t).split() if len(w) > 2][:5]
    if len(words) < 2:
        words = [fallback.lower()] if fallback else words
    return f"{year}-{'-'.join(words)}"[:70].strip("-")


def norm_doi(d):
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (d or "").strip()).lower()


def read_page(path):
    text = path.read_text(encoding="utf-8")
    _, head, body = text.split("---", 2)
    return yaml.safe_load(head) or {}, body


def write_page(path, fm, body=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    dumped = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000)
    path.write_text(f"---\n{dumped}---{body if body.startswith(chr(10)) else chr(10) + body}", encoding="utf-8")


def load_yaml(name):
    return yaml.safe_load((ROOT / "data" / name).read_text()) or {}


def load_params():
    p = yaml.safe_load((ROOT / "config/_default/params.yaml").read_text())
    return p.get("lab", {})


def reconstruct_abstract(inv):
    if not inv:
        return ""
    pos = {}
    for word, idx in inv.items():
        for i in idx:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


# ------------------------------------------------------------------ lookups
VENUES = load_yaml("venues.yaml")
AUTHORS = {}
for f in (ROOT / "data/authors").glob("*.yaml"):
    a = yaml.safe_load(f.read_text()) or {}
    AUTHORS[f.stem] = a
THEME_KW = {}
for d in (ROOT / "content/themes").iterdir():
    if (d / "_index.md").exists():
        THEME_KW[d.name] = read_page(d / "_index.md")[0].get("keywords", [])


def match_venue(name):
    n = (name or "").lower()
    if re.search(r"workshop|challenge", n):  # satellite events carry no main-conference rank / acceptance rate
        return ""
    for key, v in VENUES.items():
        for m in v.get("match", []):
            if (m.startswith("^") and re.search(m, n)) or (not m.startswith("^") and m in n):
                return key
    return ""


def canonical_author(name):
    """Map a name variant to the team member's profile slug (so the paper appears on their profile); others unchanged."""
    n = norm_title(name)
    for slug, a in AUTHORS.items():
        display = (a.get("name") or {}).get("display", "")
        variants = [display] + list(a.get("aliases") or [])
        if any(norm_title(v) == n for v in variants if v):
            return slug
        # "S Albarqouni" ~ "Shadi Albarqouni": same family name and first initial
        parts, dparts = name.replace(".", " ").split(), display.split()
        if parts and dparts and parts[-1].lower() == dparts[-1].lower() and parts[0][:1].lower() == dparts[0][:1].lower():
            return slug
    return name


def infer_themes(*texts):
    blob = " ".join(t for t in texts if t).lower()
    return [t for t, kws in THEME_KW.items() if any(k in blob for k in kws)]


# ------------------------------------------------------------------ discovery
def discover_scholar(scholar_id):
    try:
        from scholarly import scholarly  # type: ignore
    except ImportError:
        print("scholarly not installed — skipping Google Scholar discovery")
        return None, {}
    try:
        author = scholarly.fill(scholarly.search_author_id(scholar_id), sections=["basics", "indices", "publications"])
    except Exception as e:  # noqa: BLE001 — Scholar often blocks CI runners
        print(f"Google Scholar unavailable ({e}); falling back to OpenAlex")
        return None, {}
    stats = {"citations": author.get("citedby"), "h_index": author.get("hindex"), "i10_index": author.get("i10index")}
    works = []
    for p in author.get("publications", []):
        b = p.get("bib", {})
        works.append({"title": b.get("title"), "year": b.get("pub_year"), "venue": b.get("citation", ""),
                      "scholar_citations": p.get("num_citations", 0), "scholar_id": p.get("author_pub_id", "")})
    return works, stats


def openalex_author_id(lab):
    if lab.get("openalex_author"):
        return lab["openalex_author"]
    if lab.get("orcid"):
        j = get_json(f"https://api.openalex.org/authors/orcid:{lab['orcid']}")
        if j:
            return j["id"].rsplit("/", 1)[-1]
    j = get_json("https://api.openalex.org/authors?search=" + urllib.parse.quote("Shadi Albarqouni"))
    if j and j.get("results"):
        best = max(j["results"], key=lambda a: a.get("works_count", 0))
        print(f"OpenAlex author guessed: {best['id']} — set params.yaml lab.openalex_author to pin it")
        return best["id"].rsplit("/", 1)[-1]
    return ""


def discover_openalex(author_id):
    works, cursor = [], "*"
    while cursor:
        j = get_json(f"https://api.openalex.org/works?filter=author.id:{author_id}&per-page=200&cursor={cursor}"
                     + (f"&mailto={MAILTO}" if MAILTO else ""))
        if not j:
            break
        works += j["results"]
        cursor = j["meta"].get("next_cursor")
    return works


def openalex_by_title(title):
    q = urllib.parse.quote(re.sub(r"[:,]", " ", title)[:250])
    j = get_json(f"https://api.openalex.org/works?search={q}&per-page=3" + (f"&mailto={MAILTO}" if MAILTO else ""))
    for w in (j or {}).get("results", []):
        if norm_title(w.get("title")) == norm_title(title):
            return w
    return None


def crossref_abstract(doi):
    j = get_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")
    a = ((j or {}).get("message") or {}).get("abstract", "")
    return re.sub(r"<[^>]+>", "", a).strip()


def s2_extra(doi):
    headers = {"x-api-key": os.environ["S2_API_KEY"]} if os.environ.get("S2_API_KEY") else None
    j = get_json(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi)}"
                 "?fields=abstract,externalIds,openAccessPdf", headers)
    return j or {}


# ------------------------------------------------------------------ build front matter from OpenAlex
def from_openalex(w):
    doi = norm_doi(w.get("doi"))
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    venue = src.get("display_name") or ""
    if doi and re.search(r"^lecture notes|^springer|^communications in computer", venue, re.I):
        # OpenAlex names only the book series; Crossref has the proceedings title (MICCAI 2026, OMIA, BrainLes, …)
        cr = (get_json(f"https://api.crossref.org/works/{doi}") or {}).get("message") or {}
        book = [t for t in cr.get("container-title") or [] if not re.match(r"lecture notes|communications in", t, re.I)]
        if book:
            venue = book[0] + (f", {venue}" if venue.lower().startswith(("lecture", "communications")) else "")
            if re.match(MICCAI_WORKSHOPS, book[0], re.I):
                venue = venue.replace(book[0], book[0] + " — MICCAI workshop", 1)
    abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
    if not abstract and doi:
        abstract = crossref_abstract(doi)
    extra = s2_extra(doi) if doi and not abstract else {}
    abstract = abstract or extra.get("abstract") or ""
    authors = [canonical_author(a["author"]["display_name"]) for a in w.get("authorships", [])]
    links = []
    oa = (w.get("best_oa_location") or {}).get("pdf_url") or (extra.get("openAccessPdf") or {}).get("url")
    if oa:
        links.append({"type": "pdf", "url": oa})
    code = re.findall(r"https?://github\.com/[\w.-]+/[\w.-]+", abstract)
    if code:
        links.append({"type": "code", "url": code[0].rstrip(".")})
    arxiv = ((extra.get("externalIds") or {}).get("ArXiv")) or ""
    ptype = CSL.get(w.get("type"), "manuscript")
    if (src.get("type") == "conference") or re.search(r"conference|proceedings|miccai|symposium|workshop|lecture notes in computer science", venue, re.I):
        ptype = "paper-conference"
    if re.search(r"arxiv|medrxiv|biorxiv|research square|ssrn", venue, re.I):
        ptype = "preprint"
    # congress abstracts: typed by OpenAlex, published in a journal supplement (e.g. RöFo "S 01", ARD EULAR issue),
    # or on German Medical Science meeting pages (DOI 10.3205/<yy><meeting><no>)
    biblio = w.get("biblio") or {}
    if (w.get("type") in ("conference-abstract", "meeting-abstract")
            or re.match(r"10\.3205/\d{2}[a-z]", (w.get("doi") or "").replace("https://doi.org/", ""))
            or re.match(r"s\s*\d", str(biblio.get("issue") or ""), re.I)
            or re.search(r"\babstracts?\b|kongress|jahrestagung", venue, re.I)):
        ptype = "abstract"
    title = html.unescape(w.get("title") or "")
    return {
        "title": title,
        "date": w.get("publication_date") or f"{w.get('publication_year')}-01-01",
        "authors": authors,
        "publication_types": [ptype],
        "publication": {"name": venue},
        "venue": match_venue(venue),
        "doi": doi,
        "abstract": abstract,
        "themes": infer_themes(title, abstract),
        "projects": [],
        "datasets": [],
        "tags": [c["display_name"] for c in (w.get("keywords") or [])[:5]],
        "featured": False,
        "links": links,
        "slidev": "",
        "hugoblox": {"ids": {k: v for k, v in (("doi", doi), ("arxiv", arxiv)) if v}},
        "sync": {"source": "openalex", "openalex": (w.get("id") or "").rsplit("/", 1)[-1], "scholar": "",
                 "citations": w.get("cited_by_count", 0), "needs_review": True, "locked": [],
                 "updated": dt.date.today().isoformat()},
    }, oa


def teaser_from_pdf(pdf_url, dest):
    """Save the largest figure from the first pages of an open-access PDF as featured.png (needs PyMuPDF)."""
    try:
        import fitz  # type: ignore
    except ImportError:
        return False
    try:
        req = urllib.request.Request(pdf_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read(30_000_000)
        doc = fitz.open(stream=data, filetype="pdf")
        best = None
        for page in list(doc)[:3]:
            for img in page.get_images(full=True):
                pix = fitz.Pixmap(doc, img[0])
                if pix.width < 300 or pix.height < 150:
                    continue
                if not best or pix.width * pix.height > best.width * best.height:
                    best = pix
        if best:
            if best.n - best.alpha >= 4:
                best = fitz.Pixmap(fitz.csRGB, best)
            best.save(str(dest / "featured.png"))
            return True
    except Exception as e:  # noqa: BLE001
        print(f"  ! teaser extraction failed: {e}")
    return False


def bibtex(fm, key):
    kind = {"article-journal": "article", "paper-conference": "inproceedings"}.get(fm["publication_types"][0], "misc")
    field = "journal" if kind == "article" else "booktitle"
    lines = [f"@{kind}{{{key},", f"  title = {{{fm['title']}}},", f"  author = {{{' and '.join(fm['authors'])}}},",
             f"  year = {{{str(fm['date'])[:4]}}},"]
    if fm["publication"]["name"]:
        lines.append(f"  {field} = {{{fm['publication']['name']}}},")
    if fm["doi"]:
        lines.append(f"  doi = {{{fm['doi']}}},")
    return "\n".join(lines) + "\n}\n"


# ------------------------------------------------------------------ SJR quartiles
def refresh_quartiles(csv_path):
    import csv
    best = {}
    with open(csv_path, encoding="utf-8", errors="ignore") as f:
        for row in csv.DictReader(f, delimiter=";"):
            q = row.get("SJR Best Quartile", "")
            for issn in (row.get("Issn") or "").split(","):
                issn = issn.strip()
                if len(issn) == 8:
                    best[f"{issn[:4]}-{issn[4:]}"] = q
    path = ROOT / "data/venues.yaml"
    text = path.read_text()
    venues = yaml.safe_load(text)
    changed = 0
    for key, v in venues.items():
        for issn in v.get("issn", []):
            q = best.get(issn.upper())
            if q and q != v.get("quartile"):
                text = re.sub(rf"(^{re.escape(key)}:\n(?:  .*\n)*?  quartile: )Q\d", rf"\g<1>{q}", text, flags=re.M)
                changed += 1
                break
    path.write_text(text)
    print(f"quartiles updated: {changed}")


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--sjr", help="SCImago journal rank CSV to refresh quartiles")
    ap.add_argument("--no-scholar", action="store_true")
    args = ap.parse_args()
    lab = load_params()

    if args.sjr:
        refresh_quartiles(args.sjr)

    # existing pages, indexed by DOI and normalised title
    existing = {}
    for p in PUBS.glob("*/index.md"):
        fm, body = read_page(p)
        existing[norm_title(fm.get("title"))] = p
        if fm.get("doi"):
            existing[norm_doi(fm["doi"])] = p

    scholar_works, stats = (None, {}) if args.no_scholar else discover_scholar(lab.get("scholar_id", ""))
    oa_id = openalex_author_id(lab)
    oa_works = discover_openalex(oa_id) if oa_id else []
    print(f"discovered: scholar={len(scholar_works or [])} openalex={len(oa_works)}")
    oa_by_title = {norm_title(w.get("title")): w for w in oa_works}

    candidates = list(oa_works)
    for s in scholar_works or []:
        if norm_title(s["title"]) not in oa_by_title:
            w = openalex_by_title(s["title"])
            candidates.append(w or {"title": s["title"], "publication_year": s.get("year"), "_scholar": s})
    scholar_cites = {norm_title(s["title"]): s for s in scholar_works or []}

    created = updated = 0
    for w in candidates[: args.limit or None]:
        title = w.get("title")
        if not title:
            continue
        key_t, key_d = norm_title(title), norm_doi(w.get("doi"))
        path = existing.get(key_d) or existing.get(key_t)
        s = scholar_cites.get(key_t)
        if path and not path.exists():  # created earlier in this (dry) run
            continue
        if path:  # ---- update an existing page, filling only missing fields
            fm, body = read_page(path)
            locked = set((fm.get("sync") or {}).get("locked") or [])
            new, _ = from_openalex(w) if w.get("id") else ({}, None)
            changes = {}
            for field in ("doi", "abstract", "venue"):
                if field not in locked and not fm.get(field) and new.get(field):
                    changes[field] = new[field]
            if "date" not in locked and (fm.get("draft") or str(fm.get("date", "")).startswith("1970")) and new.get("date"):
                changes["date"], changes["draft"] = new["date"], False
            # a preprint that has since been published (journal / conference / abstract) gets its new type and venue
            if ("publication_types" not in locked and (fm.get("publication_types") or [""])[0] == "preprint"
                    and (new.get("publication_types") or ["preprint"])[0] in ("article-journal", "paper-conference", "abstract")):
                changes["publication_types"] = new["publication_types"]
                if "publication" not in locked and new.get("publication"):
                    changes["publication"] = new["publication"]
            if "links" not in locked and new.get("links"):
                have = {l.get("type") for l in fm.get("links") or []}
                add = [l for l in new["links"] if l["type"] not in have]
                if add:
                    changes["links"] = (fm.get("links") or []) + add
            sync = dict(fm.get("sync") or {})
            sync.update({"openalex": new.get("sync", {}).get("openalex") or sync.get("openalex", ""),
                         "citations": max((new.get("sync") or {}).get("citations", 0), (s or {}).get("scholar_citations", 0)),
                         "updated": dt.date.today().isoformat()})
            if s:
                sync["scholar"] = s.get("scholar_id", "")
            changes["sync"] = sync
            if changes.keys() - {"sync"}:
                updated += 1
                print(f"~ {path.parent.name}: {', '.join(sorted(changes.keys() - {'sync'}))}")
            fm.update(changes)
            if fm.get("doi"):
                fm.setdefault("hugoblox", {}).setdefault("ids", {})["doi"] = fm["doi"]
            if not args.dry_run:
                write_page(path, fm, body)
            continue

        # ---- new publication
        if w.get("type") in SKIP_TYPES or w.get("is_paratext") or w.get("is_retracted"):
            continue
        if not w.get("id"):
            print(f"? not found in OpenAlex, skipped: {title}")
            continue
        fm, oa_pdf = from_openalex(w)
        if s:
            fm["sync"]["scholar"] = s.get("scholar_id", "")
            fm["sync"]["citations"] = max(fm["sync"]["citations"], s.get("scholar_citations", 0))
        slug = slugify(fm["title"], str(fm["date"])[:4], fm["sync"]["openalex"])
        while (PUBS / slug).exists():
            slug += "-b"
        dest = PUBS / slug
        print(f"+ {slug}")
        created += 1
        existing[key_t] = dest / "index.md"
        if args.dry_run:
            continue
        write_page(dest / "index.md", fm, "")
        (dest / "cite.bib").write_text(bibtex(fm, slug.replace("-", "_")))
        if oa_pdf:
            teaser_from_pdf(oa_pdf, dest)
        existing[key_t] = dest / "index.md"
        if key_d:
            existing[key_d] = dest / "index.md"

    if stats and not args.dry_run:
        stats["updated"] = dt.date.today().isoformat()
        stats["source"] = "Google Scholar"
        (ROOT / "data/scholar.json").write_text(json.dumps(stats, indent=2))
    elif oa_id and not args.dry_run:
        a = get_json(f"https://api.openalex.org/authors/{oa_id}") or {}
        prev = json.loads((ROOT / "data/scholar.json").read_text()) if (ROOT / "data/scholar.json").exists() else {}
        # keep the (usually higher) Scholar numbers if we could not reach Scholar this time
        prev.setdefault("citations", a.get("cited_by_count"))
        prev.setdefault("h_index", (a.get("summary_stats") or {}).get("h_index"))
        prev["openalex_citations"] = a.get("cited_by_count")
        prev["updated"] = dt.date.today().isoformat()
        (ROOT / "data/scholar.json").write_text(json.dumps(prev, indent=2))
    print(f"created {created}, updated {updated}")


if __name__ == "__main__":
    main()
