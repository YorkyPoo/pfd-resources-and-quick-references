#!/usr/bin/env python3
"""check_caption_labels.py — a section caption is a LABEL, and the first chip is the route.

Why this exists (card t_75b6aba8): the homepage captions ("EMS Hub", "Fire
resources", "City & personnel policies", "Crew links & portals") used to be
anchors styled as 11.52px uppercase 54%-opacity labels. On the live root at
390px the anchor box measured 14px tall — under the 24px WCAG 2.5.8 minimum and
nowhere near a 44px thumb target — and it pointed at the same page as the first
chip in its row. It looked like a label and was not one.

Two regressions are possible and neither is caught by ``mkdocs build --strict``
(every href is valid) nor by ``check_scroller_hrefs.py`` (no two chips in a row
share an href — a caption is not in the scroller):

  1. a caption grows an ``<a>`` again (markdown ``**[Label](page)**{: .pfd-cap }``
     renders the class onto the ``<p>``, so the anchor lands inside ``.pfd-cap``);
  2. the row's first chip stops being the route to the section page — e.g. the
     chip is dropped or repointed, leaving the caption's old destination with no
     control that reaches it.

Both are exit-1 failures naming the page, the caption/row and the href.

Usage:  python3 scripts/check_caption_labels.py [site_dir]   (default: site)
Exit 0 = captions are labels and every row leads with its section page,
     1 = a caption contains an anchor or a row's first chip is the wrong page,
     2 = no site dir.
"""
from __future__ import annotations

import os
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_resource_pages as gen  # noqa: E402  (constants only; main() is guarded)

# The scroller whose row opens each section, and the page that section is.
# Ordered as quicklinks_block() emits them, so a reordered or dropped row fails
# loudly instead of silently checking the wrong pairing.
SECTIONS = (
    ("pfd-scroller--ems", gen.EMS_CLINICAL_HUB),
    ("pfd-scroller--fire", gen.FIRE_REF_HUB),
    ("pfd-scroller--admin", gen.STATION_POLICIES),
    ("pfd-scroller--util", gen.LINKS_PAGE),
)

HOME = "index.html"


class Scan(HTMLParser):
    """Collect caption elements (class contains pfd-cap) and .pfd-scroller rows."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.caps: list[dict] = []       # {"text": str, "anchors": [href, ...]}
        self.rows: list[dict] = []       # {"kind": class, "hrefs": [href, ...]}
        self._stack: list[tuple[str, str]] = []   # (tag, role: "cap"|"row"|"")
        self._cap: dict | None = None
        self._row: dict | None = None

    # -- helpers ---------------------------------------------------------
    @staticmethod
    def _classes(attrs) -> set[str]:
        for k, v in attrs:
            if k == "class" and v:
                return set(v.split())
        return set()

    def handle_starttag(self, tag, attrs):
        classes = self._classes(attrs)
        role = ""
        if "pfd-cap" in classes and tag != "a":
            self._cap = {"text": "", "anchors": [], "tag": tag}
            self.caps.append(self._cap)
            role = "cap"
        elif tag == "div" and "pfd-scroller" in classes and self._row is None:
            kind = next((c for c in classes if c.startswith("pfd-scroller--")), "")
            self._row = {"kind": kind, "hrefs": []}
            self.rows.append(self._row)
            role = "row"

        if tag == "a":
            href = next((v or "" for k, v in attrs if k == "href"), "")
            if self._cap is not None:
                self._cap["anchors"].append(href)
            if self._row is not None:
                self._row["hrefs"].append(href)

        if tag not in ("area", "base", "br", "col", "embed", "hr", "img", "input",
                       "link", "meta", "source", "track", "wbr"):
            self._stack.append((tag, role))

    def handle_startendtag(self, tag, attrs):
        # self-closing tags never open a caption/row context; just note any <a/>
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        # unwind to the matching open tag; a caption/row context ends only when
        # its own element is the one being closed (inner tags have role "")
        while self._stack:
            open_tag, role = self._stack.pop()
            if role == "cap":
                self._cap = None
            if role == "row":
                self._row = None
            if open_tag == tag:
                break

    def handle_data(self, data):
        if self._cap is not None:
            self._cap["text"] += data


def _norm_href(href: str) -> str:
    """href as served from the site root, fragment dropped."""
    path = href.split("#")[0]
    if not path:
        return ""
    return os.path.normpath(path).replace(os.sep, "/").lstrip("./")


def main() -> int:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
    if not site.is_dir():
        print(f"no site dir at {site.resolve()} — run mkdocs build first")
        return 2
    page = site / HOME
    if not page.is_file():
        print(f"no built homepage at {page.resolve()} — run mkdocs build first")
        return 2

    scan = Scan()
    scan.feed(page.read_text(encoding="utf-8"))

    bad: list[str] = []

    # --- 1. a caption is a label, never a control ------------------------
    for cap in scan.caps:
        label = " ".join(cap["text"].split())
        if cap["anchors"]:
            bad.append(f"{HOME}  .pfd-cap \"{label}\"  contains {len(cap['anchors'])} "
                       f"anchor(s): {cap['anchors']}")
        if not label:
            bad.append(f"{HOME}  .pfd-cap  is empty")

    # --- 2. every row opens with the page its section captions -----------
    if len(scan.rows) != len(SECTIONS):
        bad.append(f"{HOME}  expected {len(SECTIONS)} .pfd-scroller rows "
                   f"({', '.join(k for k, _ in SECTIONS)}), found {len(scan.rows)}")
    for i, (kind, page_md) in enumerate(SECTIONS):
        if i >= len(scan.rows):
            bad.append(f"{HOME}  missing row .{kind} → {page_md}")
            continue
        row = scan.rows[i]
        if row["kind"] != kind:
            bad.append(f"{HOME}  row {i + 1} is .{row['kind']}, expected .{kind}")
            continue
        if not row["hrefs"]:
            bad.append(f"{HOME}  .{kind}  has no chips")
            continue
        want = page_md[:-3] + ".html" if page_md.endswith(".md") else page_md
        got = _norm_href(row["hrefs"][0])
        if got != _norm_href(want):
            bad.append(f"{HOME}  .{kind}  first chip → {got or '(no href)'}, "
                       f"expected the section page {want}")

    print(f"scanned {HOME}: {len(scan.caps)} caption(s), {len(scan.rows)} scroller row(s)")
    for cap in scan.caps:
        print(f"  caption  \"{' '.join(cap['text'].split())}\"")
    for row in scan.rows:
        first = _norm_href(row["hrefs"][0]) if row["hrefs"] else "(no chips)"
        print(f"  row .{row['kind']}  {len(row['hrefs'])} chip(s), first → {first}")

    if bad:
        print(f"\nCAPTION/ROW CHECK FAILED ({len(bad)}):")
        for line in bad:
            print(f"  {line}")
        return 1
    print("\ncaptions are labels · every row leads with its section page")
    return 0


if __name__ == "__main__":
    sys.exit(main())
