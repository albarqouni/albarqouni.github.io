#!/usr/bin/env python3
"""Sync the Code section with the public repositories of the lab's GitHub organisation.

For every public, non-fork repository of `lab.github_org` (params.yaml):
  * content/code/<repo>/index.md — title, summary (repo description or first README paragraph), repository URL,
    language, stars, license, topics, last update, linked publication(s), themes, course (for teaching repos)
  * body — the README's overview/abstract section(s), cleaned of badges and HTML, plus install/usage pointers
  * featured.<ext> — the first real figure in the README (badges/logos skipped); falls back to the linked
    publication's teaser figure
Curated edits survive re-syncs: fields listed in `sync.locked` (and the body, if "body" is locked) are never touched.
New repositories appear automatically on the next run (.github/workflows/sync-code.yml, weekly).

Usage: python3 scripts/sync_code_repos.py [--dry-run] [--only REPO]
Env:   GITHUB_TOKEN (optional, raises the API rate limit)
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import sync_publications as sp  # noqa: E402  (infer_themes, norm_title, read/write helpers)

API = "https://api.github.com"
SKIP_IMG = re.compile(r"shields\.io|badge|travis-ci|codecov|logo|icon|colab-badge|\.svg(\?|$)|img\.youtube|hits\.|visitor", re.I)
COURSES = {"aim-bigs": "aim", "air": "air"}  # repo (lower) → teaching course slug


def gh(path, raw=False):
    headers = {"User-Agent": "albarqouni-lab-site", "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(API + path, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            return data.decode("utf-8", "ignore") if raw else json.loads(data)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def readme(repo, branch):
    """README via raw.githubusercontent.com (not counted against the API rate limit)."""
    for name in ("README.md", "readme.md", "README.MD", "Readme.md", "README.rst", "README"):
        try:
            req = urllib.request.Request(f"https://raw.githubusercontent.com/{repo}/{branch}/{name}", headers={"User-Agent": "albarqouni-lab-site"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError:
            continue
    return gh(f"/repos/{repo}/readme", raw=True) or ""


def clean_md(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<(p|div)[^>]*align=[^>]*>.*?</\1>", "", text, flags=re.S | re.I)  # centred logo/badge blocks
    text = re.sub(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", "", text)                      # linked badges
    text = re.sub(r"!\[[^\]]*\]\([^)]*(shields\.io|badge)[^)]*\)", "", text)
    text = re.sub(r"<img[^>]*>", "", text)
    text = re.sub(r"</?(a|br|sup|sub|b|i|em|strong|span|center|p|div)[^>]*>", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def sections(md):
    """Split README into (heading, text) pairs."""
    parts, cur, buf = [], "", []
    for line in md.splitlines():
        m = re.match(r"^\s{0,3}(#{1,4})\s+(.*)", line)
        if m:
            parts.append((cur, "\n".join(buf).strip()))
            cur, buf = m.group(2).strip(), []
        else:
            buf.append(line)
    parts.append((cur, "\n".join(buf).strip()))
    return [(h, t) for h, t in parts if t or h]


def first_paragraph(text):
    for para in re.split(r"\n\s*\n", text):
        p = para.strip()
        if (len(p) > 60 and not p.startswith(("```", "|", "-", "*", ">", "!", "<", "#")) and not re.match(r"^\[.*\]\(.*\)$", p)
                and not re.search(r"pip3? install|requirements\.txt|conda (create|env)|git clone|[├└│]", p, re.I) and not p.endswith(":")):
            return re.sub(r"\s+", " ", p)
    return ""


def readme_images(md, repo, branch):
    imgs = re.findall(r"!\[[^\]]*\]\(([^)\s]+)", md) + re.findall(r'<img[^>]+src=["\']([^"\']+)', md)
    out = []
    for u in imgs:
        if SKIP_IMG.search(u):
            continue
        if not u.startswith("http"):
            u = f"https://raw.githubusercontent.com/{repo}/{branch}/{u.lstrip('./')}"
        u = re.sub(r"github\.com/([^/]+/[^/]+)/blob/", r"raw.githubusercontent.com/\1/", u)
        out.append(u)
    return out


def download(url, dest_dir):
    req = urllib.request.Request(url, headers={"User-Agent": "albarqouni-lab-site"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data, ctype = r.read(20_000_000), r.headers.get("content-type", "")
    sig = {b"\x89PNG": ".png", b"\xff\xd8\xff": ".jpg", b"RIFF": ".webp", b"GIF8": ".gif"}
    ext = next((e for s, e in sig.items() if data.startswith(s)), None)
    if not ext or len(data) < 8000:  # not a raster image, or a tiny icon
        return None
    for old in dest_dir.glob("featured.*"):
        old.unlink()
    (dest_dir / f"featured{ext}").write_bytes(data)
    return ext


def match_publications(repo, md):
    """Our publications referenced by the repo: arXiv id / DOI in the README, or the repo name in a paper title/slug."""
    ids = set(re.findall(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", md, re.I))
    dois = {d.lower().rstrip(").,") for d in re.findall(r"10\.\d{4,9}/[^\s)\]\"'>]+", md)}
    name = re.sub(r"[-_](nmi|official|code)$", "", repo["name"].lower())
    hits = []
    for p in (ROOT / "content/publications").glob("*/index.md"):
        fm, _ = sp.read_page(p)
        ax = str(((fm.get("hugoblox") or {}).get("ids") or {}).get("arxiv") or "")
        doi = (fm.get("doi") or "").lower()
        title = sp.norm_title(fm.get("title"))
        key = sp.norm_title(name)
        if (ax and ax.split("v")[0] in ids) or (doi and doi in dois) or (len(key) >= 4 and (key in title[:40] or key in p.parent.name.replace("-", ""))):
            hits.append((fm.get("date") or "", p.parent.name))
    return [s for _, s in sorted(hits, reverse=True)]


WEAK = re.compile(r"source code of|official|offical|^please|^if you|^this (repo|repository) (contains|hosts)|^the source code", re.I)


def pick_summary(desc, md_clean, para, pubs):
    """Most informative one-liner: repo description, the README overview, the paper abstract, the first paragraph."""
    overview = next((first_paragraph(t) for h, t in sections(md_clean)
                     if re.search(r"abstract|overview|introduction|summary|about|description", h, re.I)), "")
    paper = ""
    if pubs:
        pfm, _ = sp.read_page(ROOT / "content/publications" / pubs[0] / "index.md")
        sents = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", pfm.get("abstract") or "").strip())
        if sents[0]:
            paper = f"Code for “{pfm.get('title')}”. " + " ".join(sents[:2])
    for c in (desc, overview, paper, para):
        c = re.sub(r"\*\*|__|`", "", c or "").strip()
        if len(c) >= 50 and not WEAK.search(c):
            return c[:300] + ("…" if len(c) > 300 else "")
    return desc


def paper_section(pubs):
    """Fallback description: the abstract of the accompanying paper."""
    if not pubs:
        return ""
    fm, _ = sp.read_page(ROOT / "content/publications" / pubs[0] / "index.md")
    abstract = re.sub(r"\s+", " ", (fm.get("abstract") or "")).strip()
    if len(abstract) < 200:
        return ""
    return f"### About the method\n\nFrom the abstract of [{fm.get('title')}](/publications/{pubs[0]}/):\n\n> {abstract}"


def build_body(md, repo_url, desc, pubs=()):
    secs = sections(clean_md(md))
    keep, extra = [], []
    for h, t in secs:
        hl = h.lower()
        if not t or re.search(r"citation|cite|bibtex|license|acknowledg|contact|contribut|badge", hl):
            continue
        if re.search(r"abstract|overview|introduction|about|summary|method|highlights|^$|description|motivation|key idea", hl) and len(keep) < 3:
            keep.append((h, t))
        elif re.search(r"install|setup|usage|getting started|quick ?start|requirements|data|train|inference|reproduc", hl):
            extra.append(h)
    out = []
    for h, t in keep:
        if re.search(r"pip3? install|requirements\.txt", t) and len(t) < 400:
            continue
        t = re.sub(r"```.*?```", "", t, flags=re.S).strip()
        if len(t) < 40 or t.strip() == desc:
            continue
        out.append((f"### {h}\n\n" if h and h.lower() not in ("", "about") else "") + t[:2500])
    if not out and pubs:
        out.append(paper_section(pubs))
    if extra:
        out.append("### Using the code\n\nThe repository README covers " + ", ".join(dict.fromkeys(extra[:5])).lower()
                   + f". See [the repository on GitHub]({repo_url}#readme) for step-by-step instructions.")
    return "\n\n".join(out).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()
    org = sp.load_params().get("github_org", "albarqounilab")
    repos = gh(f"/orgs/{org}/repos?per_page=100&type=public&sort=updated") or []
    for repo in repos:
        if repo["fork"] or repo.get("private") or (args.only and repo["name"] != args.only):
            continue
        slug = re.sub(r"^-", "", re.sub(r"[^a-z0-9-]+", "-", repo["name"].lower())).strip("-")
        dest = ROOT / "content/code" / slug
        page = dest / "index.md"
        fm, body = (sp.read_page(page) if page.exists() else ({}, ""))
        locked = set((fm.get("sync") or {}).get("locked") or [])
        branch = repo.get("default_branch", "main")
        md = readme(repo["full_name"], branch)
        md_clean = clean_md(md)
        desc = (repo.get("description") or "").strip()
        para = first_paragraph(md_clean)
        pubs = fm.get("publications") if "publications" in locked else match_publications(repo, md)
        summary = pick_summary(desc, md_clean, para, pubs) or f"Code repository {repo['name']}."
        course = COURSES.get(repo["name"].lower())
        themes = []
        for s in pubs:
            pfm, _ = sp.read_page(ROOT / "content/publications" / s / "index.md")
            themes += pfm.get("themes") or []
        if not themes:
            themes = sp.infer_themes(repo["name"], desc, para, " ".join(repo.get("topics") or []))
        new = {
            "title": fm.get("title") if "title" in locked else (repo["name"] + (f" — {desc}" if 0 < len(desc) <= 60 else "")),
            "summary": fm.get("summary") if "summary" in locked else summary,
            "date": (repo.get("created_at") or "")[:10],
            "lastmod": (repo.get("pushed_at") or "")[:10],
            "repository": repo["html_url"],
            "homepage": repo.get("homepage") or "",
            "language": repo.get("language") or "",
            "stars": repo.get("stargazers_count", 0),
            "license": ((repo.get("license") or {}).get("spdx_id") or "").replace("NOASSERTION", ""),
            "topics": repo.get("topics") or [],
            "code_type": "teaching" if course else "research",
            "course": course or "",
            "publications": fm.get("publications") if "publications" in locked else pubs,
            "themes": fm.get("themes") if "themes" in locked else sorted(set(themes), key=["computational-imaging", "responsible-ai", "federated-learning"].index) if themes else [],
            "projects": fm.get("projects") or [],
            "datasets": fm.get("datasets") or [],
            "authors": fm.get("authors") or ["shadi-albarqouni"],
            "modality": fm.get("modality") or [],
            "sync": {"source": "github", "repo": repo["full_name"], "locked": sorted(locked)},
        }
        if fm.get("image"):
            new["image"] = fm["image"]
        new_body = body if ("body" in locked and body.strip()) else build_body(md, repo["html_url"], summary, new["publications"] or [])
        teaser = ""
        if not args.dry_run:
            dest.mkdir(parents=True, exist_ok=True)
            if "image" not in locked:
                for u in readme_images(md, repo["full_name"], branch)[:4]:
                    try:
                        if download(u, dest):
                            teaser = "README figure"
                            new["image"] = {"caption": f"Figure from the [{repo['name']} README]({repo['html_url']}).", "focal_point": "Center"}
                            break
                    except Exception:  # noqa: BLE001 — broken image links in READMEs are common
                        continue
                if not teaser and pubs:
                    src = next((f for f in (ROOT / "content/publications" / pubs[0]).glob("featured.*")), None)
                    if src:
                        for old in dest.glob("featured.*"):
                            old.unlink()
                        (dest / f"featured{src.suffix}").write_bytes(src.read_bytes())
                        teaser = f"paper teaser ({pubs[0]})"
                        new["image"] = {"caption": "Teaser figure of the accompanying paper.", "focal_point": "Center"}
            sp.write_page(page, new, "\n" + new_body + "\n")
        print(f"{'+' if not fm else '~'} {slug:16} ★{new['stars']:<3} {new['language']:16} pubs={pubs[:2]} teaser={teaser or '-'} themes={new['themes']}")


if __name__ == "__main__":
    main()
