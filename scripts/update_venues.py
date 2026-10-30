#!/usr/bin/env python3
"""Yearly refresh of venue statistics in data/venues.yaml (run by .github/workflows/update-venues.yml every July).

  * OpenAlex  — for every journal/conference we publish in: 2-year mean citedness + h-index (automatic, open data).
               Journals that appear in our publications but not yet in the registry are added automatically.
  * Acceptance rates — CV/ML conferences from github.com/lixin4ever/Conference-Acceptance-Rate (years already in the
               registry are kept: hand-curated numbers win).
  * SJR quartiles — only with --sjr <scimagojr.csv> (SCImago blocks automated downloads).
  * Re-assigns `venue:` on publications, and reports journals whose Clarivate JIF is older than the latest JCR release.

Usage: python3 scripts/update_venues.py [--sjr scimagojr.csv] [--dry-run]
"""
import argparse
import collections
import datetime as dt
import re
import sys
import urllib.request
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_publications as sp  # noqa: E402

ROOT = sp.ROOT
REG = ROOT / "data/venues.yaml"
ACC_README = "https://raw.githubusercontent.com/lixin4ever/Conference-Acceptance-Rate/master/README.md"
ACC_NAMES = {"cvpr": "CVPR", "iccv": "ICCV", "eccv": "ECCV", "neurips": "NeurIPS", "aaai": "AAAI", "wacv": "WACV", "bmvc": "BMVC"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]


def latest_jcr_year(today=None):
    today = today or dt.date.today()
    return today.year - 1 if today.month >= 7 else today.year - 2  # JCR appears each June with the previous year's JIF


def fetch_acceptance():
    try:
        with urllib.request.urlopen(urllib.request.Request(ACC_README, headers={"User-Agent": sp.UA}), timeout=30) as r:
            text = r.read().decode()
    except Exception as e:  # noqa: BLE001
        print(f"! acceptance dataset unavailable: {e}")
        return {}
    out = collections.defaultdict(dict)
    for name, yy, rate in re.findall(r"^\|\s*([A-Za-z]+)'(\d{2})\s*\|\s*([\d.]+)%", text, flags=re.M):
        for key, label in ACC_NAMES.items():
            if name.lower() == label.lower():
                out[key][2000 + int(yy)] = float(rate)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sjr")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    reg = yaml.safe_load(REG.read_text()) or {}
    header = REG.read_text().split("\n# ---", 1)[0]

    # ---- sources used by our publications (from the audit/sync: sync.source_id, sync.issn)
    pubs = []
    used = collections.Counter()
    sources = {}
    for p in (ROOT / "content/publications").glob("*/index.md"):
        fm, body = sp.read_page(p)
        pubs.append((p, fm, body))
        s = fm.get("sync") or {}
        if s.get("source_id"):
            sources[s["source_id"]] = {"issn": s.get("issn") or [], "type": s.get("source_type") or "",
                                       "name": (fm.get("publication") or {}).get("name", "")}
            used[s["source_id"]] += 1

    # ---- OpenAlex metrics for registry entries + auto-add journals we publish in
    by_issn = {i.upper(): k for k, v in reg.items() for i in v.get("issn", [])}
    for sid, info in sources.items():
        src = sp.get_json(f"https://api.openalex.org/sources/{sid}") or {}
        if not src:
            continue
        issns = [i.upper() for i in (src.get("issn") or [])]
        key = next((by_issn[i] for i in issns if i in by_issn), None) or sp.match_venue(src.get("display_name", ""))
        if not key:
            if src.get("type") not in ("journal", "conference") or "arxiv" in (src.get("display_name") or "").lower():
                continue
            key = slug(src.get("display_name", sid))
            reg[key] = {"name": src["display_name"], "short": src.get("abbreviated_title") or src["display_name"],
                        "match": [src["display_name"].lower()], "type": src.get("type"), "issn": src.get("issn") or []}
            print(f"+ venue {key}")
        st = src.get("summary_stats") or {}
        reg[key]["openalex"] = {"id": sid, "citedness_2yr": round(st.get("2yr_mean_citedness") or 0, 2),
                                "h_index": st.get("h_index"), "updated": dt.date.today().isoformat()}
        if not reg[key].get("issn") and src.get("issn"):
            reg[key]["issn"] = src["issn"]
    # registry journals not (yet) linked through a publication: look up by ISSN
    for key, v in reg.items():
        if v.get("type") == "journal" and not v.get("openalex") and v.get("issn"):
            src = sp.get_json(f"https://api.openalex.org/sources/issn:{v['issn'][0]}") or {}
            st = src.get("summary_stats") or {}
            if st:
                v["openalex"] = {"id": src["id"].rsplit("/", 1)[-1], "citedness_2yr": round(st.get("2yr_mean_citedness") or 0, 2),
                                 "h_index": st.get("h_index"), "updated": dt.date.today().isoformat()}

    # ---- acceptance rates (curated values win)
    for key, rates in fetch_acceptance().items():
        if key in reg:
            acc = reg[key].setdefault("acceptance", {}) or {}
            for y, r in rates.items():
                if y not in acc and str(y) not in acc:
                    acc[y] = r
                    print(f"~ {key} {y}: {r}%")
            reg[key]["acceptance"] = dict(sorted(acc.items(), key=lambda kv: int(kv[0])))

    # ---- SJR quartiles
    if args.sjr:
        import csv
        best = {}
        with open(args.sjr, encoding="utf-8", errors="ignore") as f:
            for row in csv.DictReader(f, delimiter=";"):
                for issn in (row.get("Issn") or "").split(","):
                    issn = issn.strip()
                    if len(issn) == 8:
                        best[f"{issn[:4]}-{issn[4:]}".upper()] = row.get("SJR Best Quartile", "")
        for v in reg.values():
            q = next((best[i.upper()] for i in v.get("issn", []) if best.get(i.upper())), None)
            if q and q != "-":
                v["quartile"] = q

    # ---- report stale JIFs
    jcr = latest_jcr_year()
    stale = [(k, v) for k, v in reg.items() if v.get("type") == "journal" and (v.get("impact_factor") or {}).get("year", 0) < jcr]
    unverified = [(k, v) for k, v in reg.items() if (v.get("impact_factor") or {}) and not v["impact_factor"].get("verified")]
    lines = [f"# Venue statistics report — {dt.date.today().isoformat()}", "",
             f"Latest JCR release: JIF {jcr}. Journals below have no JIF for {jcr} yet — look them up in Clarivate JCR and edit `data/venues.yaml`.", "",
             "| venue | current JIF | OpenAlex 2-yr citedness | our papers |", "|---|---|---|---|"]
    counts = collections.Counter(fm.get("venue") for _, fm, _ in pubs)
    for k, v in sorted(stale, key=lambda kv: -counts.get(kv[0], 0)):
        jif = v.get("impact_factor") or {}
        lines.append(f"| {v['name']} | {jif.get('value', '—')} ({jif.get('year', '—')}) | {(v.get('openalex') or {}).get('citedness_2yr', '—')} | {counts.get(k, 0)} |")
    if unverified:
        lines += ["", "Values marked `verified: false` (from aggregators/slides): " + ", ".join(v["name"] for _, v in unverified)]
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs/venue-report.md").write_text("\n".join(lines) + "\n")

    if args.dry_run:
        print("\n".join(lines))
        return
    # ---- write registry (keep header comment) and re-assign venues on publications
    with REG.open("w") as f:
        f.write(header.rstrip() + "\n\n")
        for k, v in reg.items():
            f.write(yaml.safe_dump({k: v}, sort_keys=False, allow_unicode=True, width=1000))
    sp.VENUES.clear()
    sp.VENUES.update(reg)
    changed = 0
    for p, fm, body in pubs:
        if "venue" in ((fm.get("sync") or {}).get("locked") or []):
            continue
        key = sp.match_venue((fm.get("publication") or {}).get("name", "") if isinstance(fm.get("publication"), dict) else "")
        if key and key != fm.get("venue"):
            fm["venue"] = key
            sp.write_page(p, fm, body)
            changed += 1
    print(f"registry: {len(reg)} venues · publications re-assigned: {changed} · stale JIFs: {len(stale)}")


if __name__ == "__main__":
    main()
