#!/usr/bin/env python3
"""Create next semester's course offerings by cloning each course's latest offering.

  python3 scripts/new_semester.py                 # next semester, all courses with `recurring: true`
                                                  # (`frequency: winter|summer` limits a course to one season)
  python3 scripts/new_semester.py WS2627          # a specific semester
  python3 scripts/new_semester.py SS27 air comi-lab   # specific courses

New offerings are created as drafts: lecturers/tutors fill in dates, room and timeline, then remove `draft: true`.
Courses with `auto_publish: true` (e.g. the AiR seminar, offered every semester) are published straight away.
Semester codes: WS2627 = winter 2026/27 (starts mid-October), SS27 = summer 2027 (starts mid-April).
"""
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEACHING = ROOT / "content/teaching"


def next_semester(today=None):
    today = today or dt.date.today()
    y = today.year % 100
    # Planning happens ahead: from March on we prepare the coming winter, from September the coming summer.
    if 3 <= today.month <= 8:
        return f"WS{y:02d}{(y + 1) % 100:02d}"
    return f"SS{(y + 1 if today.month >= 9 else y) % 100:02d}"


def semester_start(code):
    if code.startswith("WS"):
        return dt.date(2000 + int(code[2:4]), 10, 15)
    return dt.date(2000 + int(code[2:4]), 4, 15)


def semester_order(code):
    d = semester_start(code)
    return (d.year, d.month)


def label(code):
    return f"Winter {2000 + int(code[2:4])}/{code[4:6]}" if code.startswith("WS") else f"Summer {2000 + int(code[2:4])}"


def read(p):
    _, head, body = p.read_text(encoding="utf-8").split("---", 2)
    return yaml.safe_load(head) or {}, body


MONTH = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{1,2}"


def reset_body(body):
    """Clear semester-specific details copied from the template: session dates, presenters and the tutor list."""
    out = []
    for line in body.splitlines():
        cells = line.split("|")
        if line.lstrip().startswith("|") and len(cells) > 5 and re.search(MONTH, cells[1]):
            cells[1] = " **TBA** "
            cells[4] = " "  # presenter column
            line = "|".join(cells)
        line = re.sub(r"^(\*\*Tutors:\*\*).*$", r"\1 to be announced", line)
        out.append(line)
    return "\n".join(out) + ("\n" if body.endswith("\n") else "")


def main():
    args = sys.argv[1:]
    sem = args.pop(0).upper() if args and re.match(r"^(WS\d{4}|SS\d{2})$", args[0].upper()) else next_semester()
    wanted = set(args)
    start = semester_start(sem)
    made = 0
    for course in sorted(d for d in TEACHING.iterdir() if (d / "_index.md").exists()):
        cfm, _ = read(course / "_index.md")
        if wanted and course.name not in wanted:
            continue
        if not wanted and not cfm.get("recurring"):
            continue
        # `frequency` in the course's _index.md: "every semester" (default), "winter" or "summer" (once a year)
        freq = str(cfm.get("frequency") or "every semester").lower()
        if not wanted and ((freq == "winter" and not sem.startswith("WS")) or (freq == "summer" and not sem.startswith("SS"))):
            print(f"- {course.name}: offered in {freq} only")
            continue
        offerings = [d for d in course.iterdir() if d.is_dir() and (d / "index.md").exists()]
        if (course / sem.lower()).exists():
            print(f"= {course.name}/{sem.lower()} exists")
            continue
        # one-off editions (`special: true`, e.g. a joint edition with a partner) are never used as templates
        offerings = [d for d in offerings if not read(d / "index.md")[0].get("special")]
        # prefer the latest offering of the same season (WS→WS, SS→SS), else the latest overall
        same = [d for d in offerings if d.name.upper().startswith(sem[:2])] or offerings
        if not same:
            print(f"! {course.name}: no offering to clone")
            continue
        src = max(same, key=lambda d: semester_order(d.name.upper()))
        fm, body = read(src / "index.md")
        fm.update({
            "title": f"{cfm.get('acronym', course.name)} — {label(sem)}",
            "semester": sem, "semesters": [sem],
            "date": start.isoformat(), "start": start.isoformat(), "end": "",
            "draft": not cfm.get("auto_publish"),
            "timeline": [{**t, "date": ""} for t in fm.get("timeline") or []],
            "registration": "", "ecampus_url": "", "basis_url": "",
            "tutors": [], "authors": list(fm.get("lecturers") or fm.get("authors") or []),
        })
        body = reset_body(body)
        dest = course / sem.lower()
        dest.mkdir()
        (dest / "index.md").write_text("---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000) + "---" + body, encoding="utf-8")
        for f in src.glob("featured.*"):
            (dest / f.name).write_bytes(f.read_bytes())
        print(f"+ {course.name}/{sem.lower()}  (from {src.name})")
        made += 1
    print(f"{made} offering(s) created for {label(sem)} — remember to fill in dates/rooms and remove `draft: true`.")


if __name__ == "__main__":
    main()
