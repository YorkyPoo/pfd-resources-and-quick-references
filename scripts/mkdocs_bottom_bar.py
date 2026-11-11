"""Fixed 4-item mobile bottom bar (Home / EMS / Fire / Station).

Injected at build time so removing it later is deleting one line from mkdocs.yml; no page
source is touched. Merged to main 2026-11-11 after the phone hand-test of /prototype/.

Design constraints this satisfies, and why each one is here:
 - 4 items (Home / EMS / Fire / Station), equal width, min 44px hit area, glyph + label each.
 - padding-bottom: env(safe-area-inset-bottom) so the home-indicator band on iPhone does not
   eat half of the tap target — a bar measured at 56px in a browser can be effectively 24px
   on a notched phone without it.
 - <=760px only (matching the existing FAB media query, not a new 768px one): desktop
   keeps the tabs bar it already has; two nav systems at once is worse than either one.
 - Paths are computed per page with relpath because protocol pages live at depths 1-3.
 - The existing drawer FAB at (320,770) is RAISED above the bar, not removed: the bar holds
   four destinations, the FAB still holds the full menu and search. Overlapping them would
   put a 54px circle on top of a live tab.
"""
import os
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


def render_bar(here="."):
    """Bar markup for a page sitting in output directory `here`."""
    cells = []
    for label, target in ITEMS:
        href = posixpath.relpath(target, here)
        cells.append(
            f'<a class="bbitem" href="{href}"><span class="bbico">{ICON[label]}</span>'
            f'<span class="bbtxt">{label}</span></a>'
        )
    return f'<nav class="bbnav" aria-label="Field navigation">{"".join(cells)}</nav>'


def on_post_page(output, *, page, config):
    # depth of this page's own output file, so ../.. resolves from wherever we are
    here = posixpath.dirname(getattr(page.file, "dest_path", "") or "") or "."
    m = re.search(r"</body>", output)
    if not m:
        return output
    return output[:m.start()] + render_bar(here) + output[m.end():]


def on_post_build(config, **kwargs):
    """Give the 404 page its bar too.

    404.html is rendered from the theme's template, not from a Page object, so on_post_page
    never fires for it — and the error page is exactly where a field user lands from a bad
    bookmark or a stale service-worker hit. Without the bar it is the only screen in the app
    with no way to get back to a protocol except the browser's own controls.
    """
    path = os.path.join(config["site_dir"], "404.html")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    if 'class="bbnav"' in html:  # idempotent: never double-inject on a re-run
        return
    m = re.search(r"</body>", html)
    if not m:
        return
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html[: m.start()] + render_bar(".") + html[m.end():])
