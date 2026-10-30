#!/usr/bin/env python3
"""One-off migration from the old Academic v4 site (albarqouni_web) to this Hugo Blox site.

Reads the old site strictly read-only and writes into this repository:
  authors            -> data/authors/<slug>.yaml + assets/media/authors/<slug>.<ext>
  publication        -> content/publications/<slug>/
  funded             -> content/projects/<slug>/        (structured partners/funders from PROJECTS below)
  talk               -> content/community/<slug>/
  media              -> content/media/<slug>/
  codes              -> content/code/<slug>/
  positions          -> content/positions/<slug>/
  students/courses   -> content/teaching/<course>/<semester>/

Usage:  python3 scripts/migrate_from_old.py /path/to/albarqouni_web [--force]
"""
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FORCE = "--force" in sys.argv

# ---------------------------------------------------------------------------
# Curated metadata. Everything here should be double-checked by the PI.
# ---------------------------------------------------------------------------
PI = "shadi-albarqouni"

PROJECTS = {
    # old folder: (new slug, start, end, funders, partners, themes, acronym, url)
    "BonnFellowship": ("bonn-fellowship", "2024-01", "2025-12", ["unibonn-funds"], ["weill-cornell", "uni-bonn"], ["computational-imaging"], "", ""),
    "BonnGUC": ("bonn-guc", "2025-01", "2026-12", ["daad", "bmbf"], ["guc", "uni-bonn"], ["responsible-ai"], "", ""),
    "BonnMelbourne": ("bonn-melbourne", "2023-01", "2024-12", ["unibonn-funds"], ["unimelb", "ukb", "uni-bonn"], ["computational-imaging"], "", ""),
    "bacatec": ("bacatec", "2020-01", "2021-12", ["bacatec"], ["stanford", "tum", "siemens"], ["computational-imaging"], "", "https://www.bacatec.de/en/gefoerderte_projekte.html"),
    "bigpicture": ("bigpicture", "2021-02", "2027-01", ["imi"], ["radboud", "tum", "owkin"], ["federated-learning"], "BIGPICTURE", "https://www.bigpicture.eu/"),
    "bild": ("bild", "2025-06", "2025-09", ["daad"], ["utm", "lau", "dpu", "uni-bonn"], ["responsible-ai"], "BILD", "https://bild2025.github.io/"),
    "chestage": ("chestage", "2023-01", "2026-12", ["dfg"], ["uk-freiburg", "ukb"], ["computational-imaging"], "", ""),
    "eeda": ("eeda", "2023-09", "2023-12", ["daad"], ["bau", "helmholtz-munich", "uni-bonn"], ["responsible-ai", "federated-learning"], "EEDA", "https://eeda2023.github.io/"),
    "federated-learning": ("federated-learning", "2020-04", "2025-03", ["helmholtz"], ["helmholtz-munich", "tum"], ["federated-learning"], "", "https://www.helmholtz.de/en/career/careers-at-helmholtz/helmholtz-young-investigator-groups/"),
    "omi": ("omi", "2024-01", "2028-12", ["bmbf"], ["ukb"], ["federated-learning"], "OMI", "https://omi.ikim.nrw/"),
    "radiotherapy": ("radiotherapy", "2022-01", "2025-12", ["dfg"], ["lmu", "tum"], ["computational-imaging"], "", ""),
    "saai": ("saai", "2024-05", "2024-07", ["bmbf"], ["agya", "lau", "uni-bonn"], ["responsible-ai"], "SAAI", "https://saai2024.github.io/"),
    "sanad": ("sanad", "2025-01", "2025-12", ["daad"], ["lau", "utm", "dpu", "uni-bonn"], ["responsible-ai"], "SANAD", ""),
    "symposium": ("symposium", "2025-12", "2025-12", ["daad"], ["lau", "utm", "dpu", "uni-bonn"], ["responsible-ai"], "", ""),
    "telemedicine": ("telemedicine", "2020-04", "", [], ["iugaza"], ["responsible-ai"], "", ""),
    "uncertainty": ("uncertainty", "2020-01", "2022-12", ["daad", "bmbf"], ["ethz", "imperial", "tum"], ["computational-imaging"], "", ""),
}
PROJECT_SLUGS = {v[0] for v in PROJECTS.values()}
# Some old `projects:` values referred to funded projects under other names.
PROJECT_ALIASES = {"federated-learning": "federated-learning", "uncertainty": "uncertainty", "telemedicine": "telemedicine",
                   "omi": "omi", "OMI": "omi", "SANAD": "sanad", "sanad": "sanad"}

# Old "research directions" (content/project) are absorbed into the three themes.
LEGACY_DIRECTION_TO_THEME = {
    "learn-to-reason-and-explain": "computational-imaging", "learn-from-crowds": "computational-imaging", "crowdsourcing": "computational-imaging",
    "learn-from-graph": "computational-imaging", "learn-to-recognize": "computational-imaging", "Learn-to-Recognize": "computational-imaging",
    "uncertainty": "computational-imaging",
    "federated-learning": "federated-learning", "learn-to-adapt": "federated-learning", "leanr-to-adapt": "federated-learning",
    "learn-to-learn": "federated-learning",
    "responsible-ai": "responsible-ai", "telemedicine": "responsible-ai", "mriqt": "responsible-ai", "MRIQT": "responsible-ai",
}

# (old folder, course slug, semester code, start date) — semester codes: WS2526 = winter 2025/26, SS26 = summer 2026
COURSES = {
    "air": dict(title="Artificial Intelligence in Radiology: Applications and Research", acronym="AIR", kind="Seminar",
                faculty="medicine", program="Human Medicine", institution="uni-bonn", sws=2, ects=None, language="English",
                themes=["computational-imaging"],
                offerings=[("AIR", "WS2425", "2024-10-14"), ("AIR_WS2526", "WS2526", "2025-10-13"), ("AIR_SS26", "SS26", "2026-04-13")]),
    "comi-seminar": dict(title="Computational Medical Imaging (Seminar)", acronym="CoMI-S", kind="Seminar", faculty="informatics",
                         program="M.Sc. Computer Science", institution="uni-bonn", sws=2, ects=4, language="English",
                         themes=["computational-imaging", "federated-learning"], offerings=[("CoMI_S_WS2526", "WS2526", "2025-10-13")]),
    "comi-lab": dict(title="Computational Medical Imaging (Lab)", acronym="CoMI-L", kind="Lab", faculty="informatics",
                     program="M.Sc. Computer Science", institution="uni-bonn", sws=4, ects=9, language="English",
                     themes=["computational-imaging", "federated-learning"], offerings=[("CoMI_L_SS26", "SS26", "2026-04-13")]),
    "aim": dict(title="AI in Medicine (AiM): Foundations, Methods, and Critical Perspectives", acronym="AiM", kind="Block course",
                faculty="medicine", program="Interdisciplinary", institution="uni-bonn", sws=None, ects=None, language="English",
                themes=["computational-imaging"], offerings=[("AIM", "SS26", "2026-03-23")]),
    "iml": dict(title="Introduction to Machine Learning", acronym="IML", kind="Lecture", faculty="informatics",
                program="", institution="", sws=None, ects=None, language="English", themes=[],
                offerings=[("iml2022", "SS23", "2023-04-01")]),
    "flh": dict(title="Federated Learning in Healthcare", acronym="FLH", kind="Seminar", faculty="informatics",
                program="M.Sc. Biomedical Computing", institution="tum", sws=2, ects=5, language="English",
                themes=["federated-learning"], offerings=[("flh", "WS2021", "2020-10-15"), ("flhsose2021", "SS21", "2021-03-15")]),
    "aai6430": dict(title="AI for Medical Diagnosis and Prediction", acronym="AAI6430", kind="Course", faculty="medicine",
                    program="", institution="", sws=None, ects=None, language="English", themes=["computational-imaging"],
                    offerings=[("AAI6430", "WS2425", "2024-10-01")]),
    "shams": dict(title="AI Week: Synergizing Human and AI for Multidisciplinary Solutions", acronym="SHAMS", kind="School",
                  faculty="schools", program="PhD students", institution="", sws=None, ects=None, language="English",
                  themes=["responsible-ai"], offerings=[("SHAMS", "WS2425", "2024-11-01")]),
    "eeda-school": dict(title="Autumn School on AI (EEDA)", acronym="EEDA", kind="School", faculty="schools", program="",
                        institution="bau", sws=None, ects=None, language="English", themes=["responsible-ai"], projects=["eeda"],
                        offerings=[("EEDA", "WS2324", "2023-12-14")]),
    "saai-school": dict(title="Summer School on Affordable AI (SAAI)", acronym="SAAI", kind="School", faculty="schools", program="",
                        institution="uni-bonn", sws=None, ects=None, language="English", themes=["responsible-ai"], projects=["saai"],
                        offerings=[("SAAI", "SS24", "2024-07-22")]),
    "bild-school": dict(title="Summer School on Biomedical Imaging with Deep Learning (BILD)", acronym="BILD", kind="School",
                        faculty="schools", program="", institution="utm", sws=None, ects=None, language="English",
                        themes=["responsible-ai"], projects=["bild", "sanad"], offerings=[("BILD", "SS25", "2025-09-01")]),
}

PUB_TYPES = {"0": "manuscript", "1": "paper-conference", "2": "article-journal", "3": "preprint", "4": "report",
             "5": "book", "6": "chapter", "7": "thesis", "8": "patent"}

GROUPS = {"principal investigator": "pi", "researchers": "researchers", "alumni": "alumni",
          "clinical collaborators": "clinical", "senior affiliated researcher": "affiliated",
          "speakers": "guests", "mriqt": "collaborators"}

ICONS = {"envelope": "at-symbol", "twitter": "brands/x", "x-twitter": "brands/x", "github": "brands/github",
         "linkedin": "brands/linkedin", "google-scholar": "academicons/google-scholar", "orcid": "academicons/orcid",
         "researchgate": "academicons/researchgate", "youtube": "brands/youtube", "instagram": "brands/instagram",
         "facebook": "brands/facebook", "mastodon": "brands/mastodon", "bluesky": "brands/bluesky"}

IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_yaml(name):
    return yaml.safe_load((ROOT / "data" / name).read_text()) or {}


ORGS = load_yaml("organizations.yaml")
PLACES = load_yaml("places.yaml")
VENUES = load_yaml("venues.yaml")
THEME_KEYWORDS = {}
for t in ("computational-imaging", "federated-learning", "responsible-ai"):
    fm, _ = None, None
    text = (ROOT / "content/themes" / t / "_index.md").read_text()
    THEME_KEYWORDS[t] = yaml.safe_load(text.split("---")[1]).get("keywords", [])


def split_front_matter(text):
    text = text.lstrip("﻿")
    if text.startswith("---"):
        parts = text.split("\n---", 1)
        head = parts[0][3:]
        body = parts[1].split("\n", 1)[1] if len(parts) > 1 and "\n" in parts[1] else ""
        try:
            fm = yaml.safe_load(head) or {}
        except yaml.YAMLError:
            # Old files sometimes contain unquoted colons in multi-line titles; retry leniently.
            fm = yaml.safe_load(re.sub(r'^(title|summary): "(.*)', lambda m: m.group(0), head, flags=re.M)) or {}
        return fm, body
    if text.startswith("+++"):
        head, _, body = text[3:].partition("\n+++")
        fm = {}
        for line in head.splitlines():
            m = re.match(r'\s*(\w+)\s*=\s*"(.*)"\s*$', line)
            if m:
                fm[m.group(1)] = m.group(2)
        return fm, body.split("\n", 1)[1] if "\n" in body else ""
    return {}, text


def read_page(path):
    try:
        return split_front_matter(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001 — report and keep migrating
        print(f"  ! could not parse {path}: {e}")
        return None, None


def clean(v):
    return v.strip() if isinstance(v, str) else v


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"[\s_]+", "-", s).strip("-")


def write_page(path, fm, body=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not FORCE:
        return False
    dumped = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000)
    path.write_text(f"---\n{dumped}---\n{body.strip()}\n" if body.strip() else f"---\n{dumped}---\n", encoding="utf-8")
    return True


def copy_assets(src_dir, dst_dir, skip=()):
    for f in src_dir.iterdir():
        if f.is_file() and f.suffix.lower() in IMAGE_EXT + (".pdf", ".bib", ".mp4") and f.name not in skip:
            if f.name.startswith(".") or "bkp" in f.name.lower() or "_old" in f.name.lower():
                continue
            shutil.copy2(f, dst_dir / f.name)


def resolve_place(location):
    if not location:
        return None
    loc = location.lower()
    for key, p in PLACES.items():
        if any(a in loc for a in p.get("aliases", [])):
            return key
    return None


def infer_themes(*texts, seed=()):
    blob = " ".join(t for t in texts if isinstance(t, str)).lower()
    found = list(dict.fromkeys(seed))
    for theme, kws in THEME_KEYWORDS.items():
        if theme not in found and any(k in blob for k in kws):
            found.append(theme)
    return found


def match_venue(name):
    if not name:
        return ""
    n = name.lower()
    for key, v in VENUES.items():
        for m in v.get("match", []):
            if (m.startswith("^") and re.search(m, n)) or (not m.startswith("^") and m in n):
                return key
    return ""


def as_list(v):
    if v is None:
        return []
    if isinstance(v, list):
        return [clean(x) for x in v if x not in (None, "", [])]
    return [clean(v)]


def fix_author(a):
    if not isinstance(a, str):
        return a
    a = a.strip()
    return "Shadi Albarqouni" if a in ("admin", "shadi-albarqouni") else a


def legacy_links(fm):
    links = []
    for key, typ in (("url_pdf", "pdf"), ("url_code", "code"), ("url_dataset", "dataset"), ("url_poster", "poster"),
                     ("url_slides", "slides"), ("url_video", "video"), ("url_source", "source"), ("url_project", "project")):
        url = clean(fm.get(key))
        if url:
            links.append({"type": typ, "url": url})
    for l in fm.get("links") or []:
        if isinstance(l, dict) and l.get("url") and "twitter.com/ShadiAlbarqouni" not in l["url"] and l["url"] != "#contact":
            links.append({"name": l.get("name", "Link"), "url": l["url"], "icon": "hero/link"})
    return links


def image_meta(fm):
    img = fm.get("image") or {}
    return {"caption": img.get("caption") or "", "focal_point": img.get("focal_point") or "Smart"} if img else None


# ---------------------------------------------------------------------------
# Migrators
# ---------------------------------------------------------------------------
def migrate_authors(old):
    out = ROOT / "data/authors"
    out.mkdir(parents=True, exist_ok=True)
    avatars = ROOT / "assets/media/authors"
    avatars.mkdir(parents=True, exist_ok=True)
    n = 0
    for d in sorted((old / "content/authors").iterdir()):
        if not d.is_dir() or d.name in ("admin", "albarqouni-lab"):
            continue
        src = d
        if d.name == PI and (old / "content/authors/admin/_index.md").exists():
            src = old / "content/authors/admin"  # the admin profile is the maintained one
        fm, body = read_page(src / "_index.md")
        if fm is None:
            continue
        slug = d.name
        groups = [GROUPS.get(str(g).strip().lower(), "collaborators") for g in as_list(fm.get("user_groups")) if str(g).strip()]
        links = []
        for s in fm.get("social") or []:
            if s.get("link"):
                links.append({"icon": ICONS.get(s.get("icon"), "hero/link"), "url": s["link"]})
        if fm.get("email") and not any(l["url"].startswith("mailto:") for l in links):
            links.insert(0, {"icon": "at-symbol", "url": f"mailto:{fm['email']}"})
        edu = []
        for c in ((fm.get("education") or {}).get("courses") or []):
            edu.append({"degree": c.get("course"), "institution": c.get("institution"),
                        "end": f"{c.get('year')}-12-31" if c.get("year") else None})
        profile = {
            "schema": "hugoblox/author/v1",
            "slug": slug,
            "is_owner": slug == PI,
            "name": {"display": clean(fm.get("name")) or slug.replace("-", " ").title()},
            "role": clean(fm.get("role")) or "",
            "group": groups[0] if groups else "collaborators",
            "bio": (body.strip() or clean(fm.get("bio")) or "").strip(),
            "affiliations": [{"name": o.get("name"), "url": o.get("url", "")} for o in (fm.get("organizations") or []) if o],
            "links": links,
            "interests": [i for i in as_list(fm.get("interests")) if isinstance(i, str)],
            "education": [e for e in edu if e["degree"]],
            # GitHub username — lets this member edit their own profile, news, community and courses via /admin.
            "github": "",
            # Name variants as they appear in publication author lists (used by the Scholar sync).
            "aliases": [],
        }
        if slug == PI:
            profile["aliases"] = ["S Albarqouni", "S. Albarqouni", "Shadi Albarquoni"]
        p = out / f"{slug}.yaml"
        if not p.exists() or FORCE:
            p.write_text(yaml.safe_dump(profile, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8")
            n += 1
        for ext in (".jpg", ".jpeg", ".png", ".webp"):
            av = src / f"avatar{ext}"
            if av.exists():
                shutil.copy2(av, avatars / f"{slug}{ext}")
                break
    print(f"authors: {n}")


def migrate_publications(old):
    n = 0
    for d in sorted((old / "content/publication").iterdir()):
        if not d.is_dir() or not (d / "index.md").exists():
            continue
        fm, body = read_page(d / "index.md")
        if fm is None:
            continue
        venue_name = re.sub(r"[*_]", "", str(fm.get("publication") or "")).strip()
        old_projects = [str(p) for p in as_list(fm.get("projects"))]
        projects = sorted({PROJECT_ALIASES[p] for p in old_projects if p in PROJECT_ALIASES})
        seed = [LEGACY_DIRECTION_TO_THEME[p] for p in old_projects if p in LEGACY_DIRECTION_TO_THEME]
        tags = [t for t in as_list(fm.get("tags")) if isinstance(t, str)]
        ptype = PUB_TYPES.get(str(as_list(fm.get("publication_types"))[0]) if fm.get("publication_types") else "0", "manuscript")
        if "arxiv" in venue_name.lower():
            ptype = "preprint"
        doi = clean(fm.get("doi")) or ""
        date, needs_review = normalize_date(fm.get("date"), d), False
        if not date:
            date, needs_review = "1970-01-01", True
        new = {
            "title": clean(fm.get("title")),
            "date": date,
            "draft": needs_review,  # unknown year: hidden until the Scholar sync or a human fixes it
            "authors": [fix_author(a) for a in as_list(fm.get("authors"))],
            "publication_types": [ptype],
            "publication": {"name": venue_name},
            "venue": match_venue(venue_name),
            "doi": doi,
            "abstract": clean(fm.get("abstract")) or "",
            "themes": list(dict.fromkeys(infer_themes(fm.get("title"), fm.get("abstract"), " ".join(tags), seed=seed))),
            "projects": projects,
            "datasets": [],
            "tags": tags,
            "featured": bool(fm.get("featured")),
            "links": legacy_links(fm),
            "slidev": "",  # URL of the interactive Slidev explainer, once available
            "hugoblox": {"ids": {"doi": doi}} if doi else {},
            "sync": {"source": "legacy", "openalex": "", "scholar": "", "locked": []},
        }
        img = image_meta(fm)
        if img:
            new["image"] = img
        dst = ROOT / "content/publications" / d.name
        if write_page(dst / "index.md", new, body):
            copy_assets(d, dst)
            n += 1
    print(f"publications: {n}")


def normalize_date(value, folder):
    """Return YYYY-MM-DD, falling back to a year found in cite.bib or the title."""
    v = str(value or "").strip().replace("/", "-")
    m = re.match(r"^(\d{4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?", v)
    if m:
        return f"{m.group(1)}-{int(m.group(2) or 1):02d}-{int(m.group(3) or 1):02d}"
    bib = folder / "cite.bib"
    if bib.exists():
        m = re.search(r"year\s*=\s*[{\"]?(\d{4})", bib.read_text(errors="ignore"))
        if m:
            return f"{m.group(1)}-01-01"
        m = re.search(r"\b(19|20)(\d{2})\b", bib.read_text(errors="ignore"))
        if m:
            return f"{m.group(1)}{m.group(2)}-01-01"
    return ""


def strip_sections(body, headings):
    """Drop markdown sections (until the next heading of same or higher level) whose title matches."""
    out, skip_level = [], None
    for line in body.splitlines():
        m = re.match(r"^(#{1,6})\s*(.*?)\s*:?\s*$", line)
        if m:
            level, title = len(m.group(1)), m.group(2).lower().rstrip(":")
            if skip_level and level <= skip_level:
                skip_level = None
            if any(title.startswith(h) for h in headings):
                skip_level = level
                continue
        if skip_level is None and not re.match(r"^\s*!\[(DFG|DAAD|EU|EFPIA|IMI|BaCaTeC|BigPicture)\]", line, re.I):
            out.append(line)
    return "\n".join(out).strip()


def migrate_projects(old):
    n = 0
    for folder, (slug, start, end, funders, partners, themes, acronym, url) in PROJECTS.items():
        d = old / "content/funded" / folder
        page = d / "index.md" if (d / "index.md").exists() else d / "index.txt"
        if not page.exists():
            continue
        fm, body = read_page(page)
        if fm is None:
            continue
        new = {
            "title": clean(fm.get("title")),
            "acronym": acronym,
            "summary": clean(fm.get("summary")) or "",
            "date": f"{start}-01" if start else str(fm.get("date"))[:10],
            "start": start,
            "end": end,
            "status": "",  # computed from start/end at build time unless set (e.g. "proposal")
            "funders": funders,
            "grant_number": "",
            "funding_amount": "",
            "funding_url": url or clean(fm.get("external_link")) or "",
            "role": "",  # our role in the consortium, e.g. "Coordinator", "Partner", "Principal Investigator"
            "pis": [PI],
            "co_pis": [],  # external co-PIs: {name, url, org}
            "authors": [PI],  # team members working on the project (slugs) — shows the project on their profile
            "partners": partners,
            "work_packages": [],  # {id: WP1, title: ..., lead: org-key, our_role: Lead|Contributor, summary: ...}
            "themes": themes,
            "datasets": [],
            "tags": [t for t in as_list(fm.get("tags")) if isinstance(t, str)],
            "featured": True,
        }
        img = image_meta(fm)
        if img:
            new["image"] = img
        body = strip_sections(body, ("partners", "funding", "consortium", "acknowledgment"))
        dst = ROOT / "content/projects" / slug
        if write_page(dst / "index.md", new, body):
            copy_assets(d, dst, skip=("DFG.png", "DAAD.png", "EU.png", "IMI.png", "EFPIA.png", "bacatec.png"))
            n += 1
    print(f"projects: {n}")


def migrate_talks(old):
    n = 0
    for d in sorted((old / "content/talk").iterdir()):
        if not d.is_dir() or not (d / "index.md").exists():
            continue
        fm, body = read_page(d / "index.md")
        if fm is None:
            continue
        old_projects = [str(p) for p in as_list(fm.get("projects"))]
        tags = [t for t in as_list(fm.get("tags")) if isinstance(t, str)]
        location = clean(fm.get("location")) or ""
        summary = clean(fm.get("summary")) or ""
        new = {
            "title": clean(fm.get("title")),
            "date": str(fm.get("date"))[:10] if fm.get("date") else None,
            "date_end": str(fm.get("date_end"))[:10] if fm.get("date_end") else None,
            "event_name": clean(fm.get("event")) or "",
            "event_url": clean(fm.get("event_url")) or "",
            "location": location,
            "place": resolve_place(location) or "",
            "summary": summary,
            "authors": [fix_author(a) if a != "admin" else PI for a in as_list(fm.get("authors"))] or [PI],
            "projects": sorted({PROJECT_ALIASES.get(p, p.lower()) for p in old_projects} & PROJECT_SLUGS),
            "themes": infer_themes(fm.get("title"), summary, " ".join(tags),
                                   seed=[LEGACY_DIRECTION_TO_THEME[p] for p in old_projects if p in LEGACY_DIRECTION_TO_THEME]),
            "tags": tags,
            "featured": bool(fm.get("featured")),
        }
        new["authors"] = [PI if a in ("Shadi Albarqouni",) else a for a in new["authors"]]
        img = image_meta(fm)
        if img:
            new["image"] = img
        dst = ROOT / "content/community" / slugify(d.name)
        if write_page(dst / "index.md", new, body):
            copy_assets(d, dst)
            n += 1
    print(f"community: {n}")


def migrate_media(old):
    n = 0
    for d in sorted((old / "content/media").iterdir()):
        page = d / "_index.md" if (d / "_index.md").exists() else d / "index.md"
        if not d.is_dir() or not page.exists():
            continue
        fm, body = read_page(page)
        if fm is None:
            continue
        new = {
            "title": clean(fm.get("title")),
            "date": str(fm.get("date"))[:10] if fm.get("date") else None,
            "category": "press",
            "external_link": clean(fm.get("external_link")) or "",
            "authors": [PI],
            "projects": [],
            "themes": infer_themes(fm.get("title"), body),
            "place": "",
        }
        img = image_meta(fm)
        if img:
            new["image"] = img
        dst = ROOT / "content/media" / slugify(d.name)
        if write_page(dst / "index.md", new, body):
            copy_assets(d, dst)
            n += 1
    print(f"news (press): {n}")


def migrate_simple(old, section_old, section_new, extra):
    n = 0
    for d in sorted((old / "content" / section_old).iterdir()):
        if not d.is_dir() or not (d / "index.md").exists():
            continue
        fm, body = read_page(d / "index.md")
        if fm is None:
            continue
        new = {"title": clean(fm.get("title")), "summary": clean(fm.get("summary")) or "",
               "date": str(fm.get("date") or fm.get("publishDate") or "")[:10] or None}
        new.update(extra(fm, body))
        img = image_meta(fm)
        if img:
            new["image"] = img
        dst = ROOT / "content" / section_new / slugify(d.name)
        if write_page(dst / "index.md", new, body):
            copy_assets(d, dst)
            n += 1
    print(f"{section_new}: {n}")


def migrate_courses(old):
    base = old / "content/students/courses"
    n = 0
    for slug, c in COURSES.items():
        cdir = ROOT / "content/teaching" / slug
        meta = {k: v for k, v in c.items() if k != "offerings"}
        course_fm = {
            "title": meta["title"], "acronym": meta["acronym"], "format": meta["kind"], "faculty": meta["faculty"],
            "program": meta["program"], "institution": meta["institution"], "sws": meta["sws"], "ects": meta["ects"],
            "language": meta["language"], "themes": meta["themes"], "projects": meta.get("projects", []),
            "module_url": "",   # module handbook entry (BASIS / TUMonline)
            "ecampus_url": "",  # eCampus course room
            "summary": "", "learning_objectives": [], "prerequisites": [],
            "cascade": [{"target": {"kind": "page"}, "params": {"course": slug}}],
        }
        offerings = []
        for folder, semester, start in c["offerings"]:
            d = base / folder
            fm, body = read_page(d / "index.md") if (d / "index.md").exists() else (None, None)
            if fm is None:
                continue
            if not course_fm["summary"]:
                course_fm["summary"] = clean(fm.get("summary")) or ""
            tutors = [fix_author(a) if a != "admin" else PI for a in as_list(fm.get("authors"))]
            tutors = [PI if a == "Shadi Albarqouni" else a for a in tutors] or [PI]
            off = {
                "title": f"{meta['acronym']} — {semester_label(semester)}",
                "semester": semester,
                "semesters": [semester],
                "date": start,
                "start": start,
                "end": "",
                "status": "",
                "lecturers": [PI],
                "authors": list(dict.fromkeys([PI] + tutors)),  # lecturers + tutors (slugs) → listed on their profiles
                "tutors": [t for t in tutors if t != PI],
                "schedule": "", "room": "", "registration": "",
                "basis_url": "", "ecampus_url": "",
                "grading": [],
                "timeline": [],  # {date, topic, speaker, material}
                "funding": [],   # funder keys from data/organizations.yaml
                "themes": meta["themes"], "projects": meta.get("projects", []),
                "summary": clean(fm.get("summary")) or "",
            }
            img = image_meta(fm)
            if img:
                off["image"] = img
            dst = cdir / semester.lower()
            if write_page(dst / "index.md", off, body):
                copy_assets(d, dst)
                for f in d.iterdir():
                    if f.suffix.lower() in (".pdf", ".ics"):
                        shutil.copy2(f, dst / f.name)
                n += 1
            offerings.append(semester)
            if not (cdir / "featured.png").exists():
                for f in d.glob("featured.*"):
                    if f.suffix.lower() in IMAGE_EXT:
                        shutil.copy2(f, cdir / f"featured{f.suffix.lower()}")
                        break
        write_page(cdir / "_index.md", course_fm, "")
    print(f"teaching offerings: {n}")


def semester_label(code):
    code = code.upper()
    if code.startswith("WS"):
        y = code[2:]
        return f"Winter {2000 + int(y[:2])}/{y[2:]}"
    return f"Summer {2000 + int(code[2:])}"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    old = Path(sys.argv[1]).resolve()
    if old == ROOT:
        sys.exit("refusing to migrate onto itself")
    migrate_authors(old)
    migrate_publications(old)
    migrate_projects(old)
    migrate_talks(old)
    migrate_media(old)
    migrate_simple(old, "codes", "code", lambda fm, b: {
        "repository": clean(fm.get("external_link")) or "", "authors": [PI],
        "themes": infer_themes(fm.get("title"), fm.get("summary"), " ".join(t for t in as_list(fm.get("tags")) if isinstance(t, str))),
        "projects": [], "publications": [], "datasets": [], "tags": as_list(fm.get("tags")), "language": "Python", "license": ""})
    migrate_simple(old, "positions", "positions", lambda fm, b: {
        "authors": [PI], "deadline": "", "status": "open" if str(fm.get("publishDate", ""))[:4] >= "2026" else "closed",
        "themes": infer_themes(fm.get("title"), fm.get("summary"))})
    migrate_courses(old)


if __name__ == "__main__":
    main()
