"""PROTOTYPE ONLY (branch prototype/mobile-bottom-bar) — fixed 4-item mobile bottom bar.

Injected at build time so removing the prototype is deleting one line from mkdocs.yml; no
page source is touched. NOT on main.

Design constraints this satisfies, and why each one is here:
 - 4 items (Home / EMS / Fire / Station), equal width, min 44px hit area, glyph + label each.
 - padding-bottom: env(safe-area-inset-bottom) so the home-indicator band on iPhone does not
   eat half of the tap target — a bar measured at 56px in a browser can be effectively 24px
   on a notched phone without it.
 - max-width 768px only: desktop keeps the tabs bar it already has; two nav systems is worse
   than either one.
 - Paths are computed per page with relpath because protocol pages live at depths 1-3.
 - The existing drawer FAB at (320,770) is RAISED above the bar, not removed: the bar holds
   four destinations, the FAB still holds the full menu and search. Overlapping them would
   put a 54px circle on top of a live tab.
"""
import posixpath
import re

ITEMS = [
    ("Home", "index.html"),
    ("EMS", "resources/ems.html"),
    ("Fire", "resources/fire.html"),
    ("Station", "resources/station.html"),
]

# Station was "☰" — the same three-line hamburger the drawer FAB renders one row above it
# (the FAB is Material's menu SVG), which read as a duplicated control: owner ruling
# 2026-11-11. "▦" is an apps-grid glyph: it says "launchpad" and is distinct from the FAB and
# from its ⌂ / ✚ / ▲ siblings.
# Glyph presence was measured, not assumed: in the built page at font:40px sans-serif, ▦ has an
# advance width of 37.8px while the unmapped .notdef box measures 30.0px — equal widths would
# have meant tofu, which no CSS rule can reveal.
ICON = {"Home": "⌂", "EMS": "✚", "Fire": "▲", "Station": "▦"}


def on_post_page(output, *, page, config):
    # depth of this page's own output file, so ../.. resolves from wherever we are
    here = posixpath.dirname(getattr(page.file, "dest_path", "") or "") or "."
    cells = []
    for label, target in ITEMS:
        href = posixpath.relpath(target, here)
        cells.append(
            f'<a class="bbitem" href="{href}"><span class="bbico">{ICON[label]}</span>'
            f'<span class="bbtxt">{label}</span></a>'
        )
    bar = f'<nav class="bbnav" aria-label="Field navigation">{"".join(cells)}</nav>'
    m = re.search(r"</body>", output)
    if not m:
        return output
    return output[:m.start()] + bar + output[m.end():]
