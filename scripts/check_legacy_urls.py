#!/usr/bin/env python3
"""Fail if any URL of the old site (scripts/legacy-urls.txt) is not served by the built site.

Usage: python3 scripts/check_legacy_urls.py public/
"""
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
urls = [u.strip() for u in (Path(__file__).parent / "legacy-urls.txt").read_text().splitlines() if u.strip()]
missing = [u for u in urls if not (root / ("" if u == "/" else u) / "index.html").exists()]
print(f"legacy URLs: {len(urls)} · missing: {len(missing)}")
for u in missing[:50]:
    print("  MISSING /" + u.lstrip("/"))
sys.exit(1 if missing else 0)
