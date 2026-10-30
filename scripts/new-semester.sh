#!/usr/bin/env bash
# Create next semester's course pages (drafts) from the previous offerings.
#   ./scripts/new-semester.sh            → next semester, all recurring courses
#   ./scripts/new-semester.sh WS2627 air → one course
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/new_semester.py "$@"
