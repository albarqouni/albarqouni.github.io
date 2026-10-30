#!/usr/bin/env python3
"""Keep every URL of the old albarqouni.github.io (Academic v4) site working after the switch.

1. Reads all page URLs of the old published site (its `public/` folder, i.e. the albarqouni.github.io repo checkout)
   and stores them in scripts/legacy-urls.txt (used by scripts/check_legacy_urls.py in CI).
2. Builds the new site; for every old URL the new site does NOT serve itself, writes a redirect page into
   legacy/<old path>/index.html (meta-refresh + rel=canonical + noindex — what Hugo uses for aliases, and what
   Google treats as a permanent redirect on static hosts like GitHub Pages).
3. Copies the old downloadable files (paper PDFs/videos, BibTeX, lecture slides, docs …) to the same paths under
   legacy/, so external links to them keep working. Copyrighted third-party material listed in EXCLUDE is skipped.

legacy/ is mounted into the site's static files (config/_default/module.yaml).
Usage: python3 scripts/make_legacy_redirects.py /path/to/old/public
"""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import migrate_from_old as mig  # noqa: E402  (PROJECTS / COURSES / slugify mappings used for the migration)

SITE = "https://albarqouni.github.io"
OUT = ROOT / "legacy"
FILE_EXT = {".pdf", ".pptx", ".ppt", ".ics", ".bib", ".zip", ".mp4", ".mov", ".docx", ".xlsx", ".ipynb"}
EXCLUDE = [re.compile(r"Gonzales,Woods-Digital\.Image\.Processing", re.I)]  # copyrighted textbook — never republish
OLD_THEME = {  # old research directions (content/project) → new themes
    "learn-to-reason-and-explain": "responsible-ai", "learn-from-crowds": "responsible-ai", "learn-from-graph": "computational-imaging",
    "learn-to-recognize": "computational-imaging", "learn-to-adapt": "responsible-ai", "learn-to-learn": "computational-imaging",
    "federated-learning": "federated-learning", "affordable-ai": "responsible-ai"}
SPECIAL = {
    "authors/admin/": "authors/shadi-albarqouni/", "authors/shadi-n-albarqouni/": "authors/shadi-albarqouni/",
    "authors/albarqouni-lab/": "team/", "admin/": "admin/", "resume/": "authors/shadi-albarqouni/", "post/": "community/",
    "talk/": "community/", "talks/": "community/", "publication/": "publications/", "funded/": "projects/", "project/": "themes/",
    "media/": "media/", "codes/": "code/", "courses/": "teaching/", "students/": "teaching/", "students/courses/": "teaching/",
    "students/theses/": "positions/", "students/calls/": "positions/", "slides/": "publications/", "collaborations/": "projects/",
"categories/": "media/", "publication_types/": "publications/", "tags/": "publications/",
    "team/positions/": "positions/", "people/": "team/", "authors/mhd-hasan-sarhan/": "authors/hasan-sarhan/",
    "authors/c-baur/": "authors/christoph-baur/", "authors/linda-mai-bui/": "authors/mai-bui/",
    "authors/m-tarek-shaban/": "authors/tarek-shaban/",
    "mriqt/": "demos/mriqt-demo/",
    "authors/rd-soberanis-mukul/": "authors/roger-soberanis-mukul/", "authors/roger-d-soberanis-mukul/": "authors/roger-soberanis-mukul/",
    "authors/roger-david-soberanis-mukul/": "authors/roger-soberanis-mukul/",
    "authors/matthaus-heer/": "authors/matthaeus-heer/",
    "resume/experience/": "authors/shadi-albarqouni/", "slides/_example/": "publications/", "slides/federated/": "projects/federated-learning/",
    "slides/pres/": "publications/", "talks/annu/": "community/",
}


def build_new_site(dest):
    env = dict(os.environ, PATH=f"{ROOT}/.tools/bin:{ROOT}/.tools/go/bin:" + os.environ.get("PATH", ""))
    subprocess.run(["hugo", "--gc", "--quiet", "-d", dest], cwd=ROOT, env=env, check=True)


def exists(built, url):
    return (Path(built) / url / "index.html").exists() if url else (Path(built) / "index.html").exists()


def target_for(url, built, merged):
    """Best new URL for an old one (without leading slash)."""
    if url in SPECIAL:
        return SPECIAL[url]
    parts = url.strip("/").split("/")
    sec, slug = parts[0], (parts[1] if len(parts) > 1 else "")
    cands = []
    if sec == "publication":
        cands = [f"publications/{merged.get(slug, slug)}/", f"publications/{slug}/", "publications/"]
    elif sec == "talk":
        cands = [f"community/{mig.slugify(slug)}/", "community/"]
    elif sec == "media":
        cands = [f"media/{mig.slugify(slug)}/", "media/"]
    elif sec == "funded":
        cands = [f"projects/{mig.PROJECTS.get(slug, (mig.slugify(slug),))[0]}/", "projects/"]
    elif sec == "project":
        cands = [f"themes/{OLD_THEME.get(slug, '')}/" if slug in OLD_THEME else f"projects/{slug}/", "themes/"]
    elif sec == "codes":
        cands = [f"code/{mig.slugify(slug)}/", "code/"]
    elif sec in ("students", "courses"):
        folder = parts[-1]
        for course, c in mig.COURSES.items():
            for off_folder, sem, _ in c["offerings"]:
                if off_folder.lower() == folder.lower():
                    cands.append(f"teaching/{course}/{sem.lower()}/")
        cands.append("teaching/")
    elif sec == "positions":
        cands = [f"positions/{mig.slugify(slug)}/", "positions/"]
    elif sec == "authors":
        cands = [f"authors/{slug}/"]
        def fam(x):  # family name, umlaut spellings unified (schaefer/schafer, tuerk/turk)
            return re.sub(r"(?<=[aou])e", "", x.split("-")[-1])
        team = sorted(p.stem for p in (ROOT / "data/authors").glob("*.yaml"))
        built_authors = sorted(p.name for p in (Path(built) / "authors").iterdir() if p.is_dir())
        cands += [f"authors/{a}/" for a in team if fam(a) == fam(slug) and a[0] == slug[0]]
        cands += [f"authors/{a}/" for a in built_authors if fam(a) == fam(slug) and a[0] == slug[0]]
        cands.append("team/")
    elif sec == "tags":
        cands = [f"tags/{slug}/", "publications/?q=" + slug.replace("-", "+")]
    elif sec == "publication_types":
        types = {"1": "conference", "2": "journal", "3": "preprint", "4": "other", "5": "book", "6": "book", "7": "thesis", "8": "patent"}
        cands = [f"publications/?type={types.get(slug, '')}" if slug in types else "publications/"]
    elif sec == "team":
        cands = ["positions/" + (mig.slugify(parts[-1]) + "/" if len(parts) > 2 else ""), "positions/"]
    for c in cands:
        if "?" in c or exists(built, c):
            return c
    return ""


def redirect_html(target):
    t = html.escape(f"{SITE}/{target}", quote=True)
    return (f'<!doctype html><html lang="en"><head><title>{t}</title><link rel="canonical" href="{t}">'
            f'<meta name="robots" content="noindex"><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={t}">'
            f'</head><body>Moved to <a href="{t}">{t}</a></body></html>\n')


def main():
    old = Path(sys.argv[1]).resolve()
    if not (old / "index.html").exists():
        sys.exit(f"{old} is not the old site's public/ folder (no index.html) — nothing changed")
    urls = set()
    for p in old.rglob("index.html"):
        rel = str(p.parent.relative_to(old))
        if ".git" in p.parts or re.search(r"(^|/)page/\d+$", rel):
            continue
        urls.add("" if rel == "." else rel + "/")
    urls = [u for u in urls if not u.startswith("xtarx.github.io")]
    # also the section roots, which old menus linked to
    urls = sorted(set(urls) | {k for k in SPECIAL if not k.startswith("authors/")})
    (ROOT / "scripts/legacy-urls.txt").write_text("\n".join(u or "/" for u in urls) + "\n")

    merged = {}
    for p in (ROOT / "content/publications").glob("*/index.md"):
        fm = yaml.safe_load(p.read_text().split("---")[1]) or {}
        for m in (fm.get("sync") or {}).get("merged") or []:
            merged[m] = p.parent.name

    backup = OUT.with_name("legacy.bak")
    if backup.exists():
        shutil.rmtree(backup)
    if OUT.exists():
        OUT.rename(backup)
    OUT.mkdir()  # must exist: it is mounted into the site
    with tempfile.TemporaryDirectory() as built:
        try:
            build_new_site(built)
        except subprocess.CalledProcessError:  # keep the previous redirects if the site does not build
            shutil.rmtree(OUT)
            backup.rename(OUT)
            sys.exit("hugo build failed — legacy/ left unchanged; fix the build and re-run")
        shutil.rmtree(backup, ignore_errors=True)
        made, kept, lost = 0, 0, []
        for u in urls:
            if exists(built, u):
                kept += 1
                continue
            t = target_for(u, built, merged)
            if not t:
                lost.append(u)
                continue
            dest = OUT / u / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(redirect_html(t))
            made += 1
    # old downloadable files at their original paths
    copied = skipped = 0
    for f in old.rglob("*"):
        if not f.is_file() or ".git" in f.parts or f.suffix.lower() not in FILE_EXT or "xtarx.github.io" in f.parts:
            continue
        rel = f.relative_to(old)
        if any(x.search(str(rel)) for x in EXCLUDE):
            skipped += 1
            continue
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
        copied += 1
    print(f"old URLs: {len(urls)} · served by new site: {kept} · redirects written: {made} · unresolved: {len(lost)}")
    print(f"files copied: {copied} · excluded: {skipped}")
    for u in lost:
        print("  unresolved:", u)


if __name__ == "__main__":
    main()
