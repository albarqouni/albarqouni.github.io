#!/usr/bin/env python3
"""Refresh the "Now: …" line of alumni (data/authors/<slug>.yaml, group: alumni) from public sources.

Run yearly (.github/workflows/alumni-now.yml opens a pull request for review). Sources, strongest first:
  1. ORCID public record (employment with no end date → "Role, Organisation"), if the profile has an ORCID link
  2. OpenAlex: the alumnus's most recent paper *without* Shadi Albarqouni → the institution listed on it
     (only papers from the last 2 years count, so an old affiliation is never presented as current)
  3. GitHub profile "company", if the profile has a `github:` username
Never uses Google Scholar or LinkedIn (no API; automated access is not allowed).

ORCID and GitHub (stated by the person) are written to `now` if they name an organisation not already in the current
line; the evidence goes to `now_source: {source, url, checked}`. OpenAlex affiliations are only leads (papers lag job
changes, OpenAlex merges namesakes): they are listed in docs/alumni-now.md for a human to check. Add `now` to `sync.locked` (or set `now_locked: true`) to
keep a hand-written line. Nothing is deleted: alumni without new evidence keep what they have.

Usage: python3 scripts/alumni_now.py [--dry-run] [--only SLUG]
Env:   OPENALEX_API_KEY (recommended), GITHUB_TOKEN (optional)
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import sync_publications as sp  # noqa: E402  (get_json with OpenAlex key + rate-limit handling, load_params)

TODAY = dt.date.today()
RECENT_YEARS = 2
OWN = re.compile(r"\bBonn\b|Universitätsklinikum Bonn|Helmholtz AI", re.I)  # the lab's own homes — not a new position


def norm(name):
    s = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]+", " ", s).split()


def same_person(a, b):
    """Family name equal and given names compatible: "M Tarek Shaban" ~ "Tarek Shaban", but not ~ "Muhammad Shaban"."""
    x, y = norm(a), norm(b)
    if not x or not y or x[-1] != y[-1]:
        return False
    fx, fy = {w for w in x[:-1] if len(w) > 1}, {w for w in y[:-1] if len(w) > 1}
    if fx and fy:
        return bool(fx & fy)  # both spell out a given name: one must match
    return bool({w[0] for w in x[:-1]} & {w[0] for w in y[:-1]}) or len(x) == 1 or len(y) == 1


def orcid_id(d):
    for link in d.get("links") or []:
        m = re.search(r"orcid\.org/(\d{4}-\d{4}-\d{4}-\d{3}[\dX])", link.get("url") or "")
        if m:
            return m.group(1)
    return d.get("orcid") or ""


def from_orcid(oid):
    j = sp.get_json(f"https://pub.orcid.org/v3.0/{oid}/employments", headers={"Accept": "application/json"})
    for group in (j or {}).get("affiliation-group") or []:
        for s in group.get("summaries") or []:
            e = s.get("employment-summary") or {}
            if e.get("end-date"):
                continue
            org = (e.get("organization") or {}).get("name") or ""
            role = e.get("role-title") or ""
            if org:
                return ", ".join(x for x in (role, org) if x), f"https://orcid.org/{oid}"
    return None


def coauthors(pi_id):
    """OpenAlex author ids of everyone who published with the PI: {author_id: display_name}."""
    out = {}
    for w in sp.discover_openalex(pi_id):
        for a in w.get("authorships") or []:
            au = a.get("author") or {}
            if au.get("id"):
                out[au["id"].rsplit("/", 1)[-1]] = au.get("display_name") or ""
    return out


def from_openalex(author_id, pi_id, names):
    j = sp.get_json(f"https://api.openalex.org/works?filter=author.id:{author_id},"
                    f"from_publication_date:{TODAY.year - RECENT_YEARS}-01-01&sort=publication_date:desc&per-page=25")
    for w in (j or {}).get("results") or []:
        ids = {((a.get("author") or {}).get("id") or "").rsplit("/", 1)[-1] for a in w.get("authorships") or []}
        if pi_id in ids:
            continue  # a paper with us says nothing about where they are now
        for a in w.get("authorships") or []:
            printed = a.get("raw_author_name") or (a.get("author") or {}).get("display_name") or ""
            if ((a.get("author") or {}).get("id") or "").endswith(author_id) and any(same_person(printed, n) for n in names):
                # OpenAlex sometimes merges namesakes into one author id: the name printed on this paper must match
                insts = [i.get("display_name") for i in a.get("institutions") or [] if i.get("display_name")]
                insts = [i for i in insts if not OWN.search(i)]
                if insts:
                    return insts[0], (w.get("doi") or w.get("id")), w.get("publication_year")
    return None


def from_github(user):
    headers = {"User-Agent": "albarqouni-lab-site", "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    try:
        with urllib.request.urlopen(urllib.request.Request(f"https://api.github.com/users/{user}", headers=headers), timeout=30) as r:
            company = (json.loads(r.read()).get("company") or "").strip().lstrip("@")
    except Exception:  # noqa: BLE001 — optional source
        return None
    return (company, f"https://github.com/{user}") if company else None


def is_new(proposal, current):
    """True if the proposal names an organisation not already mentioned in the current `now` line."""
    words = [w for w in norm(proposal) if len(w) > 3 and w not in {"university", "institute", "technical", "center", "centre"}]
    cur = " ".join(norm(current))
    return bool(words) and not all(w in cur for w in words)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()
    lab = sp.load_params()
    pi = sp.openalex_author_id(lab)
    try:
        team = coauthors(pi) if pi else {}
    except sp.RateLimited as e:
        print(f"OpenAlex rate limit ({e}); set OPENALEX_API_KEY. Continuing with ORCID/GitHub only.")
        team = {}
    changed, report = 0, []
    for p in sorted((ROOT / "data/authors").glob("*.yaml")):
        d = yaml.safe_load(p.read_text()) or {}
        if d.get("group") != "alumni" or (args.only and p.stem != args.only):
            continue
        name = (d.get("name") or {}).get("display") or p.stem
        current = d.get("now") or ""
        locked = d.get("now_locked") or "now" in ((d.get("sync") or {}).get("locked") or [])
        found = None
        oid = orcid_id(d)
        if oid:
            r = from_orcid(oid)
            if r:
                found = (r[0], "ORCID", r[1])
        if not found:
            ids = [i for i, n in team.items() if any(same_person(n, x) for x in [name] + (d.get("aliases") or []))]
            for i in ids:
                try:
                    r = from_openalex(i, pi, [n for n in [name] + (d.get("aliases") or []) if any(len(w) > 1 for w in norm(n)[:-1])] or [name])
                except sp.RateLimited:
                    r = None
                if r:
                    found = (r[0], f"OpenAlex (paper {r[2]})", r[1])
                    break
        if not found and d.get("github"):
            r = from_github(d["github"])
            if r:
                found = (r[0], "GitHub profile", r[1])
        if not found:
            print(f"  {p.stem:24} no public evidence — kept: {current or '(none)'}")
            continue
        text, source, url = found
        text = re.sub(r"\s*\([^)]*\)$", "", text)  # "Rohde & Schwarz (Germany)" → "Rohde & Schwarz"
        if not is_new(text, current):
            print(f"  {p.stem:24} confirmed by {source}: {current}")
            d["now_source"] = {"source": source, "url": url, "checked": TODAY.isoformat()}
        elif locked or source.startswith("OpenAlex"):
            # a paper's affiliation lags job changes and OpenAlex merges namesakes: it is only reported as a lead
            print(f"? {p.stem:24} {'LOCKED — ' if locked else ''}{source} lists “{text}” (kept: {current or '(none)'})   [{url}]")
            report.append(f"| {name} | {current or '—'} | {text} | [{source}]({url}) |")
            continue
        else:
            print(f"~ {p.stem:24} {current or '(none)'}  →  {text}   [{source}: {url}]")
            d["now"] = text
            d["now_source"] = {"source": source, "url": url, "checked": TODAY.isoformat()}
            changed += 1
        if not args.dry_run:
            p.write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=1000))
    print(f"{changed} alumni updated")
    if not args.dry_run and not args.only:
        (ROOT / "docs/alumni-now.md").write_text(
            f"# Alumni — leads for the \"Now\" line ({TODAY.isoformat()})\n\n"
            "Generated by `scripts/alumni_now.py`. Affiliations on the alumni's most recent papers without us (OpenAlex).\n"
            "They are **not** applied automatically — papers lag job changes and namesakes get mixed up. Check each one and,\n"
            "if it is right, edit `now:` in `data/authors/<slug>.yaml`.\n\n"
            "| Alumnus | Now (site) | Latest paper lists | Source |\n|---|---|---|---|\n" + "\n".join(report) + "\n")


if __name__ == "__main__":
    main()
