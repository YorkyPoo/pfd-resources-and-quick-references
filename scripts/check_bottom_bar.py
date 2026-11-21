#!/usr/bin/env python3
"""check_bottom_bar.py — the field bar must keep its four named destinations.

Renaming EMS→Protocols and Fire→SOPs (owner ruling 2026-11-20) is a one-line change in
scripts/mkdocs_bottom_bar.py, which means a typo there ships a bar with three items, a
duplicate target, or a label swapped onto the wrong page — and nothing else in the suite
notices, because every href still resolves.

Checks, on the BUILT html:

  * exactly four `.bbitem` cells, in order Home / Protocols / SOPs / Station
  * every cell carries both a glyph (`.bbico`) and a label (`.bbtxt`)
  * the hrefs are four DISTINCT pages, and they are the four the bar promises
  * the bar is present on the 404 page too (on_post_build path)

Usage:  python3 scripts/check_bottom_bar.py [site_dir]      (default: site)
Exit 0 = contract holds, 1 = drift, 2 = no site dir.
"""
from __future__ import annotations

import os
import re
import sys

LABELS = ["Home", "Protocols", "SOPs", "Station"]
# page -> the four targets it must render, relative to that page's own directory
TARGETS = ["../index.html", "ems.html", "fire.html", "station.html"]
CELL = re.compile(r'<a class="bbitem" href="([^"]+)">(.*?)</a>', re.S)


def bar_of(text: str):
    m = re.search(r'<nav class="bbnav"[^>]*>(.*?)</nav>', text, re.S)
    return CELL.findall(m.group(1)) if m else None


def main() -> int:
    site = sys.argv[1] if len(sys.argv) > 1 else "site"
    if not os.path.isdir(site):
        print(f"no site dir at {os.path.abspath(site)} — run mkdocs build first")
        return 2
    problems = []
    page = os.path.join(site, "resources", "ems.html")
    with open(page, encoding="utf-8") as fh:
        cells = bar_of(fh.read())
    if cells is None:
        problems.append("resources/ems.html: no .bbnav at all")
    else:
        if len(cells) != 4:
            problems.append(f"expected 4 bar cells, found {len(cells)}")
        # .bbtxt text is the label; strip any leading glyph text
        got_labels = []
        for _h, body in cells:
            m = re.search(r'<span class="bbtxt">(.*?)</span>', body, re.S)
            got_labels.append(re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else None)
            if '<span class="bbico">' not in body:
                problems.append(f"cell {got_labels[-1]!r} has no glyph")
        if got_labels != LABELS:
            problems.append(f"labels are {got_labels}, expected {LABELS}")
        hrefs = [h for h, _b in cells]
        if len(set(hrefs)) != len(hrefs):
            problems.append(f"duplicate targets in the bar: {hrefs}")
        if hrefs != TARGETS:
            problems.append(f"targets are {hrefs}, expected {TARGETS}")
    err = os.path.join(site, "404.html")
    if os.path.exists(err):
        with open(err, encoding="utf-8") as fh:
            if bar_of(fh.read()) is None:
                problems.append("404.html lost the field bar")
    else:
        problems.append("404.html missing from the build")

    if problems:
        print("BOTTOM BAR DRIFT:")
        for p in problems:
            print("  -", p)
        return 1
    print(f"bottom bar OK: {LABELS} -> {TARGETS} (4 equal cells, glyph + label each)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
