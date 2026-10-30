#!/usr/bin/env python3
"""Fetch the lead photo of each news item from its source article and record a proper credit.

For every content/media/<slug>/index.md with an `external_link`:
  * YouTube links → video thumbnail; credit = channel name (YouTube oEmbed).
  * Other pages   → <meta property="og:image"> (or twitter:image); credit = photographer if the page names one
                    ("Foto:", "Photo:", "Bild:", "©", "Credit:" near the image / in figure captions), else the outlet
                    (og:site_name or domain).
Writes featured.<ext> (only if the item has none, unless --force) and front matter:
  image.caption: "Photo: <credit>"   image_credit: {name, source, url}
Existing photos keep their file; their credit is filled from the page if it was empty or generic.
Usage: python3 scripts/news_images.py [--force] [--only SLUG] [--dry-run]
"""
import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
      "Accept-Language": "en,de;q=0.8"}
CREDIT_RE = re.compile(r"(?:Foto|Fotos|Photo|Photos|Bild|Bildquelle|Image|Credit|Credits|Fotografie|©|&copy;)\s*[:©]?\s*([^<>\n|]{3,80})", re.I)


def fetch(url, limit=6_000_000):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read(limit), r.headers.get("content-type", ""), r.geturl()


def meta(page, *names):
    for n in names:
        m = re.search(r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]*content=["\']([^"\']+)' % re.escape(n), page, re.I) \
            or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\']%s["\']' % re.escape(n), page, re.I)
        if m:
            return html.unescape(m.group(1)).strip()
    return ""


def youtube_id(url):
    m = re.search(r"(?:v=|youtu\.be/|embed/)([\w-]{11})", url)
    return m.group(1) if m else ""


def find_credit(page, img_url):
    """Photographer credit close to the lead image or in a figure caption; '' if none found."""
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", page, flags=re.S | re.I)
    cands = []
    fn = Path(urllib.parse.urlparse(img_url).path).name.split(".")[0] if img_url else ""
    if fn:
        i = text.find(fn)
        if i > 0:
            cands.append(text[i:i + 2500])
    cands += re.findall(r"<figcaption.*?</figcaption>", text, flags=re.S | re.I)[:4]
    cands += re.findall(r'class="[^"]*(?:caption|credit|copyright|photo-?credit|bildunterschrift)[^"]*"[^>]*>(.*?)<', text, flags=re.S | re.I)[:6]
    for c in cands:
        plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c)))
        m = CREDIT_RE.search(plain)
        if m:
            name = m.group(1).strip(" .,;:-–")
            name = re.split(r"\s{2,}| - | – | \| ", name)[0]
            name = name.strip(" ()[]")
            if (2 < len(name) < 70 and re.search(r"[A-Za-zÀ-ž]{3}", name)
                    and not re.search(r"cookie|javascript|privacy|datenschutz|http|all rights|rights reserved", name, re.I)):
                return name
    return ""


def site_name(page, url):
    return meta(page, "og:site_name", "application-name") or urllib.parse.urlparse(url).netloc.replace("www.", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    report = []
    for p in sorted((ROOT / "content/media").glob("*/index.md")):
        if args.only and p.parent.name != args.only:
            continue
        _, head, body = p.read_text(encoding="utf-8").split("---", 2)
        fm = yaml.safe_load(head) or {}
        url = (fm.get("external_link") or "").strip()
        if not url:
            continue
        has_img = any(f.name.startswith("featured.") for f in p.parent.iterdir())
        img_url, credit, source = "", "", ""
        try:
            yid = youtube_id(url) if "youtube.com" in url or "youtu.be" in url else ""
            if yid:
                o = json.loads(fetch(f"https://www.youtube.com/oembed?url={urllib.parse.quote(url)}&format=json")[0])
                credit, source = o.get("author_name", ""), "YouTube"
                img_url = f"https://img.youtube.com/vi/{yid}/maxresdefault.jpg"
            elif url.lower().split("?")[0].endswith(".pdf") or "pdfjs" in url:
                report.append((p.parent.name, "PDF link — no photo to take", ""))
                continue
            else:
                raw, ctype, final = fetch(url)
                page = raw.decode("utf-8", "ignore")
                img_url = meta(page, "og:image", "og:image:url", "twitter:image", "twitter:image:src")
                if img_url:
                    img_url = urllib.parse.urljoin(final, img_url)
                source = site_name(page, final)
                credit = find_credit(page, img_url)
        except Exception as e:  # noqa: BLE001 — unreachable/blocked sites are reported, not fatal
            report.append((p.parent.name, f"could not fetch ({e.__class__.__name__}: {str(e)[:60]})", ""))
            continue

        changed = []
        if img_url and (args.force or not has_img):
            try:
                try:
                    data, ctype, _ = fetch(img_url, 15_000_000)
                except urllib.error.HTTPError:
                    if not yid:
                        raise
                    data, ctype, _ = fetch(f"https://img.youtube.com/vi/{yid}/hqdefault.jpg")  # older videos: no maxres
                ext = {"image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}.get(ctype.split(";")[0], ".jpg")
                if len(data) > 5000 and not args.dry_run:
                    for old in p.parent.glob("featured.*"):
                        old.unlink()
                    (p.parent / f"featured{ext}").write_bytes(data)
                    changed.append("photo")
            except Exception as e:  # noqa: BLE001
                report.append((p.parent.name, f"image download failed: {e}", img_url))
        who = credit or source
        if who:
            cur = ((fm.get("image") or {}).get("caption") or "").strip()
            generic = (not cur) or cur.lower().rstrip(": ") in ("image credit", "photo") or "photo" not in changed and False
            # a named photographer from the source page always wins over an older/generic caption
            if "photo" in changed or credit or not cur or cur.lower().strip().endswith("credit:"):
                fm["image"] = {**(fm.get("image") or {}), "caption": f"Photo: {who}" + (f" / {source}" if credit and source and source not in credit else ""),
                               "focal_point": (fm.get("image") or {}).get("focal_point", "Smart")}
                changed.append("credit")
            fm["image_credit"] = {"name": credit or "", "source": source, "url": url}
        report.append((p.parent.name, ", ".join(changed) or "kept", f"{who}"))
        if not args.dry_run:
            p.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000) + "---" + body, encoding="utf-8")
    for r in report:
        print(f"{r[0]:26} {r[1]:28} {r[2]}")


if __name__ == "__main__":
    main()
