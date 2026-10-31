#!/usr/bin/env python3
"""Link publications to projects from the rules in data/project_rules.yaml.

Prints every proposed link with the reason, and writes docs/project-mapping.md for review.
With --apply, adds the project to each paper's `projects:` list (never removes; skips papers
whose `sync.locked` contains "projects").

Usage: python3 scripts/map_projects.py [--apply] [--only PROJECT]
"""
import argparse
import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PUBS = ROOT / "content/publications"
PROJECTS = ROOT / "content/projects"
RULES = ROOT / "data/project_rules.yaml"
REPORT = ROOT / "docs/project-mapping.md"


def norm(name):
    s = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]+", "-", s).strip("-")


def front(path):
    text = path.read_text()
    _, fm, body = text.split("---\n", 2)
    return yaml.safe_load(fm) or {}, text


def month(value, default):
    s = str(value or "").strip("'\" ")
    if not s:
        return default
    return s[:7] if len(s) >= 7 else s[:4] + "-01"


def shift(ym, years):
    return f"{int(ym[:4]) + years:04d}{ym[4:]}"


def window(rule, project):
    start = month(project.get("start") or project.get("date"), "2000-01")
    end = month(project.get("end"), "2100-12")
    lo = month(rule.get("from"), shift(start, -1))
    hi = month(rule.get("to"), shift(end, 3) if end != "2100-12" else end)
    if rule.get("from") and len(str(rule["from"])) == 4:
        lo = f"{rule['from']}-01"
    if rule.get("to") and len(str(rule["to"])) == 4:
        hi = f"{rule['to']}-12"
    return lo, hi


def check(rule, authors, text):
    """Return a reason string if the rule matches, else None."""
    reasons = []
    any_a = [norm(a) for a in rule.get("any_authors") or []]
    all_a = [norm(a) for a in rule.get("all_authors") or []]
    author_ok = None
    if any_a or all_a:
        hits = [a for a in any_a if a in authors]
        author_ok = (not any_a or bool(hits)) and all(a in authors for a in all_a)
        if author_ok:
            reasons.append("co-author " + ", ".join(sorted(set(hits + all_a))))
    kw_ok = None
    if rule.get("keywords"):
        found = [k for k in rule["keywords"] if re.search(k, text, re.I)]
        kw_ok = bool(found)
        if kw_ok:
            reasons.append("keyword " + ", ".join(f"/{k}/" for k in found))
    mode = rule.get("match") or ("authors" if author_ok is not None else "keywords")
    ok = {"authors": author_ok, "keywords": kw_ok, "authors+keywords": bool(author_ok and kw_ok),
          "either": bool(author_ok or kw_ok)}[mode]
    return "; ".join(reasons) if ok else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()

    keys = re.findall(r"^([A-Za-z0-9_-]+):", RULES.read_text(), re.M)
    dupes = sorted({k for k in keys if keys.count(k) > 1})
    if dupes:  # Hugo refuses to build with duplicate keys in data files
        raise SystemExit(f"duplicate project rules in {RULES.relative_to(ROOT)}: {', '.join(dupes)}")
    rules = yaml.safe_load(RULES.read_text()) or {}
    projects = {p.parent.name: front(p)[0] for p in PROJECTS.glob("*/index.md")}
    proposals = {}  # project -> [(slug, title, date, reason, already)]
    linked = {}  # project -> {slug: (title, date)} as currently curated
    for path in sorted(PUBS.glob("*/index.md")):
        fm, text = front(path)
        if fm.get("draft"):
            continue
        slug = path.parent.name
        authors = {norm(a) for a in fm.get("authors") or []}
        title, abstract = str(fm.get("title", "")), str(fm.get("abstract", ""))
        date = str(fm.get("date", ""))[:7]
        have = list(fm.get("projects") or [])
        for p in have:
            linked.setdefault(p, {})[slug] = (fm.get("title", ""), date)
        add = []
        for key, rule in rules.items():
            if args.only and key != args.only:
                continue
            if key not in projects:
                print(f"! rule for unknown project {key}")
                continue
            rule = rule or {}
            if slug in (rule.get("exclude") or []):
                continue
            reason = "listed in include" if slug in (rule.get("include") or []) else None
            if not reason:
                lo, hi = window(rule, projects[key])
                if not (lo <= date <= hi):
                    continue
                hay = title if rule.get("fields") == "title" else f"{title} {abstract}"
                reason = check(rule, authors, hay)
            if reason:
                proposals.setdefault(key, []).append((slug, fm.get("title", ""), date, reason, key in have))
                if key not in have:
                    add.append(key)
        locked = "projects" in ((fm.get("sync") or {}).get("locked") or [])
        if args.apply and add and not locked:
            new = have + add
            block = "projects:\n" + "".join(f"- {p}\n" for p in new)
            if re.search(r"^projects:.*?(?=^(?!- )\S)", text, re.M | re.S):
                text = re.sub(r"^projects:.*?(?=^(?!- )\S)", block, text, count=1, flags=re.M | re.S)
            else:
                text = text.replace("\n---\n", "\n" + block + "---\n", 1)
            path.write_text(text)

    lines = ["# Publication → project mapping", "",
             "Generated by `scripts/map_projects.py` from `data/project_rules.yaml`. "
             "✓ = already linked, + = new link proposed by the rules.", ""]
    total_new = 0
    for key in sorted(projects):
        rows = proposals.get(key, [])
        new = sum(1 for r in rows if not r[4])
        total_new += new
        title = projects[key].get("title", key)
        lines.append(f"## {key} — {title}  ({len(rows)} papers, {new} new)")
        if key not in rules:
            lines.append("_No rule yet._")
        for slug, t, date, reason, already in sorted(rows, key=lambda r: r[2], reverse=True):
            lines.append(f"- {'✓' if already else '+'} `{slug}` ({date}) {t} — _{reason}_")
        matched = {r[0] for r in rows}
        for slug, (t, date) in sorted(linked.get(key, {}).items(), key=lambda kv: kv[1][1], reverse=True):
            if slug not in matched:
                lines.append(f"- ✓ `{slug}` ({date}) {t} — _linked by hand, not matched by the rule_")
        lines.append("")
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(lines))
    print(f"{total_new} new links proposed across {len(proposals)} projects"
          f"{' — applied' if args.apply else ' (dry run; --apply to write)'} → {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
