#!/usr/bin/env python3
"""Fetch a teaser figure (usually "Figure 1") for every publication without a featured image.

Sources, in order:
  1. arXiv HTML rendering (arxiv.org/html/<id>) — the first <figure> image;
  2. the arXiv PDF or another open-access PDF — the region above the "Fig. 1"/"Figure 1" caption is rendered at
     200 dpi (works for vector figures too); falls back to the largest raster image on the first pages.
The arXiv id / open-access PDF is taken from the page (links, hugoblox.ids.arxiv) or looked up on Semantic Scholar.
Result: content/publications/<slug>/featured.png + `sync.teaser: <source>` in the front matter.

Needs PyMuPDF:  python3 -m venv .tools/venv && .tools/venv/bin/pip install pymupdf pyyaml
Usage: .tools/venv/bin/python scripts/fetch_teasers.py [--force] [--only SLUG] [--limit N]
"""
import argparse
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_publications as sp  # noqa: E402

import fitz  # PyMuPDF

UA = {"User-Agent": "Mozilla/5.0 (compatible; albarqouni-lab-teasers/1.0)"}
CAPTION = re.compile(r"^\s*(fig\.?|figure)\s*1\b[.:|]?", re.I)


def fetch(url, limit=40_000_000):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(limit), r.headers.get("content-type", "")


def arxiv_id(fm):
    ids = (fm.get("hugoblox") or {}).get("ids") or {}
    if ids.get("arxiv"):
        return re.sub(r"v\d+$", "", str(ids["arxiv"]))
    blob = " ".join(l.get("url", "") for l in fm.get("links") or []) + " " + str((fm.get("publication") or {}).get("name", ""))
    m = re.search(r"(?:arxiv\.org/(?:abs|pdf)/|arXiv:)(\d{4}\.\d{4,5})", blob)
    return m.group(1) if m else ""


def s2_lookup(fm):
    q = urllib.parse.quote(fm.get("title") or "")
    j = sp.get_json(f"https://api.semanticscholar.org/graph/v1/paper/search/match?query={q}&fields=title,externalIds,openAccessPdf")
    time.sleep(1.2)
    d = ((j or {}).get("data") or [{}])[0]
    if not d or sp.norm_title(d.get("title")) != sp.norm_title(fm.get("title")):
        return "", ""
    return (d.get("externalIds") or {}).get("ArXiv") or "", (d.get("openAccessPdf") or {}).get("url") or ""


def from_arxiv_html(aid, dest):
    try:
        html, _ = fetch(f"https://arxiv.org/html/{aid}", 8_000_000)
    except Exception:  # noqa: BLE001 — no HTML rendering for older papers
        return False
    html = html.decode("utf-8", "ignore")
    for src in re.findall(r'<figure[^>]*class="ltx_figure[^"]*"[^>]*>.*?<img[^>]+src="([^"]+)"', html, re.S)[:3]:
        url = urllib.parse.urljoin(f"https://arxiv.org/html/{aid}/", src)
        try:
            data, ctype = fetch(url, 15_000_000)
        except Exception:  # noqa: BLE001
            continue
        if "svg" in ctype or len(data) < 8000:
            continue
        pix = fitz.Pixmap(data)
        if pix.width < 300:
            continue
        if pix.alpha:
            pix = fitz.Pixmap(pix, 0)
        pix.save(str(dest / "featured.png"))
        return True
    return False


def from_pdf(data, dest):
    doc = fitz.open(stream=data, filetype="pdf")
    for page in list(doc)[:3]:
        blocks = page.get_text("blocks")
        cap = next((b for b in blocks if CAPTION.match(b[4] or "")), None)
        if not cap:
            continue
        cap_top = cap[1]
        rects = [fitz.Rect(i["bbox"]) for i in page.get_image_info()]
        rects += [d["rect"] for d in page.get_drawings() if d["rect"].width > 2 or d["rect"].height > 2]
        # text blocks between the figure and the caption belong to the figure (labels, legends)
        above = [r for r in rects if r.y1 <= cap_top + 4 and r.y0 >= cap_top - page.rect.height * 0.8 and r.width < page.rect.width * 0.99]
        if not above:
            continue
        clip = fitz.Rect(above[0])
        for r in above[1:]:
            clip |= r
        # trim anything starting far above the figure body (e.g. a header rule)
        if clip.height < 60 or clip.width < 150:
            continue
        clip = clip + (-4, -4, 4, 2)
        page.get_pixmap(clip=clip, dpi=200).save(str(dest / "featured.png"))
        return True
    # fallback: largest raster image on the first pages
    best = None
    for page in list(doc)[:3]:
        for info in page.get_image_info():
            r = fitz.Rect(info["bbox"])
            if r.width > 150 and r.height > 80 and (not best or r.get_area() > best[1].get_area()):
                best = (page, r)
    if best:
        best[0].get_pixmap(clip=best[1], dpi=200).save(str(dest / "featured.png"))
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    pages = sorted((sp.ROOT / "content/publications").glob("*/index.md"))
    if args.only:
        pages = [p for p in pages if p.parent.name == args.only]
    done = 0
    for p in pages:
        dest = p.parent
        if not args.force and any(dest.glob("featured.*")):
            continue
        fm, body = sp.read_page(p)
        if fm.get("draft"):
            continue
        aid, oa_pdf = arxiv_id(fm), ""
        if not aid:
            aid, oa_pdf = s2_lookup(fm)
        pdfs = [l["url"] for l in fm.get("links") or [] if l.get("type") == "pdf" and l.get("url")]
        source = ""
        try:
            if aid and from_arxiv_html(aid, dest):
                source = f"arxiv-html:{aid}"
            else:
                for url in ([f"https://arxiv.org/pdf/{aid}"] if aid else []) + pdfs + ([oa_pdf] if oa_pdf else []):
                    try:
                        data, ctype = fetch(url)
                    except Exception:  # noqa: BLE001 — paywalled or moved
                        continue
                    if not data.startswith(b"%PDF"):
                        continue
                    if from_pdf(data, dest):
                        source = f"pdf:{url}"
                        break
        except Exception as e:  # noqa: BLE001
            print(f"! {dest.name}: {e}")
        if source:
            fm.setdefault("image", {})
            fm["image"] = {**(fm.get("image") or {}), "caption": (fm.get("image") or {}).get("caption") or "Figure 1 of the paper.", "focal_point": "Center"}
            fm.setdefault("sync", {})["teaser"] = source
            if aid:
                fm.setdefault("hugoblox", {}).setdefault("ids", {})["arxiv"] = aid
            sp.write_page(p, fm, body)
            done += 1
            print(f"+ {dest.name}  ({source.split(':')[0]})", flush=True)
        else:
            print(f"- {dest.name}  (no open-access figure found)", flush=True)
        if args.limit and done >= args.limit:
            break
    print(f"teasers added: {done}")


if __name__ == "__main__":
    main()
