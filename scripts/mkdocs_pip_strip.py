#!/usr/bin/env python3
"""Build-time transform: per-row level chip → five-pip strip + tapped-level picker.

Why a hook and not an edit to the pages
---------------------------------------
The level a row carries already exists in the markdown as a chip
(``<span class="lvl lvl-emt">EMT</span>`` plus the optional ``+MC`` / ``*``
markers). That chip *is* the data — ``{min_level, mc_required}``. Rewriting the
tables by hand would duplicate it in a second place, and the next relabel or
reconciliation pass would then have two disagreeing copies. This hook renders
the same fact differently and touches **no** clinical word, level or marker.

The mapper
----------
``states_for(min_idx, mc_levels)`` is the whole clinical surface of this
transform, and it is mechanical:

* every level **below** the row's level          → ``no``    (empty outline)
* the row's level                                → ``go``, or ``call`` when
  the row is bracketed there (``+MC`` / ``*``)
* every level **above** the row's level          → ``go``    (solid)
* a bare ``MC`` chip                             → ``call`` at all five

It is asserted against the owner's prototype —
``audit/level-scan/reference/protocol-format-sample.html`` — by
``scripts/test_pip_strip_mapper.py``. If that test fails, this hook must not be
trusted.

Rows that publish a level the source does not authorise (``lvl-own`` /
OWNER_REQUIRED) are rendered **outline-only** with a distinct tag: a solid pip
would make a guess look like a citation.

``PENDING`` rows
----------------
A level table can be **mixed**: most rows publish a provider level, a few carry
``lvl-pending`` (no level published, pending OMD authorisation). Those pages are
converted; a PENDING row gets five *dashed* pips, no fill, and the tag
``PENDING — no published level``, plus ``data-pending="1"`` so the picker never
counts it as standing, call or not-permitted. Nothing is inferred: the row reads
as "not yet published", which is what the page says.

A table where **every** row is PENDING (Aortic Dissection) publishes no level at
all and is left exactly as it is — five empty-looking pips across a whole
protocol would read as "nobody may act".

Which tables are converted is decided from the **table itself**, never from a
page's folder, title or the presence of a PENDING chip:

* ``policy`` wrapper or a header whose second cell is not ``Level`` → not a
  level table (the administrative pages are ``| # | Basis | Action |``); left
  alone.
* header ``| # | Level | Action |`` → a level table. Converted, PENDING rows
  included.

The classifier **fails the build** if a level table carries a level chip no rule
claims, or if a ``policy``-wrapped table actually has a ``Level`` column with
level chips — that combination is what silently skipped two level tables before.
"""

from __future__ import annotations

import functools
import html as html_lib
import os
import re

LEVELS = ["R", "B", "A", "I", "P"]
FULL = {"R": "EMR", "B": "EMT", "A": "AEMT", "I": "Intermediate", "P": "Paramedic"}
LEVEL_CLASS = {"lvl-emr": 0, "lvl-emt": 1, "lvl-a": 2, "lvl-i": 3, "lvl-p": 4}

# Scope lives in ONE place: `extra.pip_strip` in mkdocs.yml.
#
#   extra:
#     pip_strip:
#       enabled: true     # false restores the chip table on every page
#       pages: all        # or a list of docs-relative paths
#
# Turning the format off is that one boolean and nothing else: the hook is the
# only thing that rewrites the table, so `enabled: false` publishes exactly the
# markup the page carries. A missing key falls back to the defaults below, so a
# page never silently loses its level table.
SCOPE_DEFAULT = {"enabled": True, "pages": "all"}


def scope_from(config):
    """{'enabled': bool, 'pages': None|set(str)} from mkdocs config."""
    extra = {}
    try:
        extra = (config or {}).get("extra") or {}
    except AttributeError:  # a plain dict-like without .get
        extra = {}
    raw = extra.get("pip_strip", SCOPE_DEFAULT)
    if isinstance(raw, bool):
        raw = {"enabled": raw}
    raw = dict(SCOPE_DEFAULT, **(raw or {}))
    pages = raw.get("pages")
    if pages in (None, "all", ["all"]):
        pages = None  # every page
    elif pages is True:
        pages = None
    elif pages is False:
        pages = set()
    elif isinstance(pages, str):
        pages = {pages}
    else:
        pages = set(pages)
    return {"enabled": bool(raw.get("enabled", True)), "pages": pages}

PIP_WORD = {
    "go": "standing order",
    "call": "call Medical Control first",
    "no": "not authorised",
}

# ---------------------------------------------------------------- the mapper


def states_for(min_idx, mc_levels=(), mc_all=False):
    """{min_level, mc_required} → five pip states.

    ``min_idx`` is an index into LEVELS (or None for "no level authorised").
    ``mc_levels`` holds the indices bracketed at that row's own level.
    ``mc_all`` is a bare ``MC`` chip: every level needs Medical Control.
    """
    if mc_all:
        return ["call"] * 5
    if min_idx is None:
        return ["no"] * 5
    mc_levels = set(mc_levels)
    out = []
    for i in range(5):
        if i < min_idx:
            out.append("no")
        else:
            out.append("call" if i in mc_levels else "go")
    return out


def states_to_min(states):
    """Inverse of the mapper, for the prototype round-trip test."""
    if all(s == "call" for s in states):
        return 0, set(), True
    try:
        m = next(i for i, s in enumerate(states) if s != "no")
    except StopIteration:
        return None, set(), False
    mc = {m} if states[m] == "call" else set()
    return m, mc, False


# ------------------------------------------------------------------ parsing

ROW_RE = re.compile(r"<tr>(.*?)</tr>", re.S)
CELL_RE = re.compile(r"<t([hd])\b[^>]*>(.*?)</t\1>", re.S)
LVWRAP_RE = re.compile(r'<div class="lv-wrap(?P<cls>[^"]*)"[^>]*>(?P<body>.*?)</div>', re.S)
# markers the level chip carries besides the level itself:
#   lvl-mc-req  +MC  — this level acts only with Medical Control authorisation
#   lvl-req     *    — agency training documentation + MC written authorisation
#   lvl-deriv   †    — level derived from the source's own wording
#   lvl-own     ⚑    — OWNER_REQUIRED: level not verified against the source
MARK_RE = re.compile(r'<sup class="lvl-(?P<kind>req|deriv)"(?P<attrs>[^>]*)>(?P<glyph>.*?)</sup>',
                     re.S)
TITLE_RE = re.compile(r'title="([^"]*)"', re.S)
MARK_CLASS = {"req": "auth", "deriv": "derived"}


def parse_level_cell(html: str):
    """(min_idx, mc_levels, flags) from one rendered Level cell."""
    flags = {
        # A bare ``MC`` chip means "Medical Control at every level". ``+MC`` is a
        # *second* chip next to a real level and means "at that level only", so
        # mc_all must look for the word ``lvl-mc`` exactly — a substring test
        # matches ``lvl-mc-req`` too and turns eight real rows into "call at all
        # five levels".
        "mc_all": any("lvl-mc" in cls.split()
                      for cls in re.findall(r'class="([^"]*)"', html)),
        "flagged": 'lvl-own' in html,
        "pending": 'lvl-pending' in html,
        "policy": 'lvl-policy' in html,
        "bracketed": 'lvl-mc-req' in html or 'lvl-req' in html,
        "marks": [],
    }
    for m in MARK_RE.finditer(html):
        t = TITLE_RE.search(m.group("attrs"))
        flags["marks"].append((MARK_CLASS[m.group("kind")],
                               html_lib.unescape(re.sub(r"<[^>]+>", "", m.group("glyph"))).strip(),
                               html_lib.unescape(t.group(1)) if t else ""))
    min_idx = None
    for cls, idx in LEVEL_CLASS.items():
        if re.search(r'class="[^"]*\b' + re.escape(cls) + r'\b', html):
            min_idx = idx
            break
    mc = {min_idx} if (flags["bracketed"] and min_idx is not None) else set()
    return min_idx, mc, flags


# ----------------------------------------------------------------- rendering


PENDING_STATES = ["pending"] * 5
PENDING_TAG = "PENDING \u2014 no published level"


def _tag(states, flagged, pending=False):
    if pending:
        return "pending", PENDING_TAG
    if flagged:
        return "flag", "level unverified \u2691"
    if all(s == "call" for s in states):
        return "call", "MC at every level"
    try:
        m = next(i for i, s in enumerate(states) if s != "no")
    except StopIteration:
        return "no", "no level authorised"
    if states[m] == "call":
        above = [i for i in range(m + 1, 5) if states[i] == "go"]
        tail = f", standing from {LEVELS[above[0]]}" if above else ""
        return "call", f"MC at {LEVELS[m]}{tail}"
    return "go", f"standing from {LEVELS[m]}"


def _aria(states, flagged, pending=False):
    if pending:
        return ("no provider level published yet \u2014 PENDING; this row is neither "
                "a standing order nor a bar at any level")
    if flagged:
        return ("no verified provider level \u2014 OWNER_REQUIRED; "
                "the published level is not confirmed against the source")
    parts = [f"{LEVELS[i]} ({FULL[LEVELS[i]]}): {PIP_WORD[states[i]]}" for i in range(5)]
    return "; ".join(parts)


def _marks(flags):
    """``*`` / ``†`` markers the chip carried, kept verbatim with their titles."""
    if not flags.get("marks"):
        return ""
    parts = []
    for kind, glyph, title in flags["marks"]:
        t = f' title="{html_lib.escape(title, quote=True)}"' if title else ""
        parts.append(f'<span class="pip-mark pip-mark-{kind}"{t}>{glyph}</span>')
    return '<span class="pip-marks">' + "".join(parts) + "</span>"


def _render_row(num, action_html, states, flagged, flags=None, pending=False):
    flags = flags or {}
    if pending:
        # PENDING: no level is published. Dashed, unfilled pips and an explicit
        # tag — never a solid pip (standing order) and never the plain empty
        # outline (not authorised), because neither is what the page says.
        pips = "".join('<i class="pip pending"></i>' for _ in states)
    elif flagged:
        # OWNER_REQUIRED: the page publishes a level the source does not
        # authorise. Outline-only pips (no solid fill anywhere) so a guess can
        # never read as a standing order. data-states keeps the page's own
        # claim for auditability; pip-strip.js never renders a verdict from it.
        pips = "".join('<i class="pip no unv"></i>' for _ in states)
    else:
        pips = "".join(f'<i class="pip {s}"></i>' for s in states)
    tcls, ttext = _tag(states, flagged, pending)
    unv = ' data-unverified="1"' if flagged else ""
    pend = ' data-pending="1"' if pending else ""
    return (
        f'<tr data-states="{",".join(states)}"{unv}{pend}>'
        f'<td class="pip-n">{num}</td>'
        f'<td class="pip-act"><div class="pip-action">{action_html}</div>'
        f'<span class="pip-tag-wrap"><span class="pip-tag {tcls}">{ttext}</span>'
        f'{_marks(flags)}</span></td>'
        f'<td class="pip-strip-cell"><span class="pip-strip" role="img" '
        f'aria-label="{_aria(states, flagged, pending)}">{pips}</span></td>'
        f"</tr>"
    )


def _picker():
    btns = "".join(
        f'<button type="button" class="pip-btn" data-level="{L}" '
        f'aria-pressed="false">{L}</button>'
        for L in LEVELS
    )
    return (
        '<p class="pip-pick-label">Tap your certification level</p>'
        '<div class="pip-pick" role="group" aria-label="Show the protocol as your certification level">'
        + btns
        + '<button type="button" class="pip-btn pip-btn-all" data-level="all" '
        'aria-pressed="true">Show all</button></div>'
    )


def _legend():
    return (
        '<div class="pip-legend">'
        '<p class="pip-legend-h">Reading the strip</p>'
        '<ul class="pip-keys">'
        '<li><span class="pip-strip"><i class="pip go"></i></span>'
        "<span><b>Solid</b> \u2014 standing order at that level. You may act.</span></li>"
        '<li><span class="pip-strip"><i class="pip call"></i></span>'
        "<span><b>Hatched</b> \u2014 call Medical Control first at that level.</span></li>"
        '<li><span class="pip-strip"><i class="pip no"></i></span>'
        "<span><b>Empty outline</b> \u2014 not authorised at that level.</span></li>"
        "</ul>"
        '<p class="pip-legend-levels"><span class="pip-letters">R B A I P</span> = '
        "EMR \u00b7 EMT \u00b7 AEMT \u00b7 Intermediate \u00b7 Paramedic</p>"
        '<p class="pip-legend-note">Position names the level and the words name it too, so '
        "colour is never the only signal. Colour is reserved for the one question that matters "
        "on scene: <b>do I act, do I call, or is this not mine.</b></p>"
        "</div>"
    )


# The legend's markup may exist in THIS module only. `_legend()` is the single
# definition; a page that wants the swatches writes the placeholder below and
# the hook splices the function's output in at build time. A second copy in a
# page or an override would drift the first time a pip colour changed, so the
# build fails when one appears under docs/ or overrides/.
LEGEND_OWNER = "scripts/mkdocs_pip_strip.py"
LEGEND_MARKER = b'class="pip-legend"'
LEGEND_TOKEN = "<!-- PIP_LEGEND -->"
GUARD_DIRS = ("docs", "overrides")


def legend_duplicates(repo_root=None):
    """Relative paths under docs/ + overrides/ that carry the legend markup."""
    root = repo_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hits = []
    for sub in GUARD_DIRS:
        base = os.path.join(root, sub)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if d not in (".git", "__pycache__"))
            for name in sorted(filenames):
                path = os.path.join(dirpath, name)
                try:
                    with open(path, "rb") as fh:
                        data = fh.read()
                except OSError:
                    continue
                if LEGEND_MARKER in data:
                    hits.append(os.path.relpath(path, root))
    return hits


def on_config(config, **kwargs):
    """Fail the build when the legend markup is copied outside this module."""
    hits = legend_duplicates()
    if hits:
        detail = "\n".join(f"  {rel}" for rel in hits)
        raise RuntimeError(
            "the protocol legend's markup may exist only in "
            f"{LEGEND_OWNER} (pages get it from the {LEGEND_TOKEN} placeholder); "
            f"found a copy in:\n{detail}"
        )
    return config


def _render_block(rows, flagged=0, pending=0):
    head = (
        '<div class="pip-wrap"><table class="pip-table">'
        "<colgroup><col class=\"pip-col-n\"><col><col class=\"pip-col-strip\"></colgroup>"
        "<thead><tr>"
        '<th class="pip-th-n">#</th><th>Action / Intervention</th>'
        '<th class="pip-th-strip"><span class="pip-strip pip-strip-head">'
        + "".join(f"<i>{L}</i>" for L in LEVELS)
        + "</span></th></tr></thead><tbody>"
    )
    body = "".join(rows)
    tally = (
        '<p class="pip-tally" aria-live="polite">'
        f"Show all \u2014 {len(rows)} actions. Each row names the level its action starts at; "
        "tap a level to see this protocol as you."
        + (f" \u00b7 {flagged} level unverified \u2691" if flagged else "")
        + (f" \u00b7 {pending} PENDING (no published level)" if pending else "")
        + "</p>"
    )
    return (
        '<div class="pip-block" data-pip-block>'
        + _picker()
        + tally
        + head
        + body
        + "</tbody></table></div>"
        + _legend()
        + "</div>"
    )


KNOWN_CHIP = {
    "lvl", "lvl-emr", "lvl-emt", "lvl-a", "lvl-i", "lvl-p",
    "lvl-mc", "lvl-mc-req", "lvl-req", "lvl-deriv", "lvl-own",
    "lvl-pending", "lvl-policy",
}


def chip_classes(cell):
    """Every ``lvl*`` class word in one rendered Level cell."""
    return {w for cls in re.findall(r'class="([^"]*)"', cell)
            for w in cls.split() if w.startswith("lvl")}


def transform_lvwrap(match, rel="<unknown>"):
    """Rewrite one rendered .lv-wrap table, or return it untouched.

    The decision is made from the table: a header ``| # | Level | Action |`` is
    a level table and is converted (PENDING rows included); anything else is
    left alone. Contradictions fail the build instead of silently skipping.
    """
    cls = match.group("cls") or ""
    body = match.group("body")
    row_mt = ROW_RE.findall(body)
    if not row_mt:
        return match.group(0)

    header_cells = CELL_RE.findall(row_mt[0])
    is_level = (len(header_cells) == 3
                and header_cells[1][1].strip().lower() == "level")

    if "policy" in cls.split():
        levels_named = [r for r in row_mt[1:]
                        if len(CELL_RE.findall(r)) == 3
                        and chip_classes(CELL_RE.findall(r)[1][1]) & set(LEVEL_CLASS)]
        if is_level and levels_named:
            raise ValueError(
                f"{rel}: a table is wrapped in 'policy' but has a Level column "
                f"with provider-level chips — refusing to skip a level table")
        if levels_named:
            # A Basis column, not a Level column: `| # | Basis | Action |` where
            # one row names a level as its basis. Rendering a five-pip level
            # strip over a Basis column would be a category error, so it stays a
            # table — but it is named, never silently skipped.
            nums = ", ".join(CELL_RE.findall(r)[0][1].strip() for r in levels_named)
            print(f"pip_strip: {rel}: policy (Basis) table not converted; "
                  f"row(s) {nums} name a provider level as basis")
        return match.group(0)
    if not is_level:
        if any(chip_classes(CELL_RE.findall(r)[1][1]) & set(LEVEL_CLASS)
               for r in row_mt[1:] if len(CELL_RE.findall(r)) == 3):
            raise ValueError(
                f"{rel}: table has provider-level chips but its header is not "
                f"'| # | Level | Action |' — refusing to skip a level table")
        return match.group(0)

    rows = []
    n_flag = 0
    n_pending = 0
    for raw in row_mt[1:]:
        cells = CELL_RE.findall(raw)
        if len(cells) != 3:
            raise ValueError(f"{rel}: level table row has {len(cells)} cells, expected 3")
        num, lvl_cell, act = cells[0][1].strip(), cells[1][1], cells[2][1].strip()
        unknown = chip_classes(lvl_cell) - KNOWN_CHIP
        if unknown:
            raise ValueError(
                f"{rel}: row {num} carries level chip class(es) {sorted(unknown)} "
                f"that no rule claims — classify it before shipping the strip")
        min_idx, mc, flags = parse_level_cell(lvl_cell)
        if flags["pending"]:
            n_pending += 1
            rows.append(_render_row(num, act, PENDING_STATES, False, flags, pending=True))
            continue
        if flags["policy"]:
            raise ValueError(
                f"{rel}: row {num} has a policy chip inside a Level-column table")
        if min_idx is None and not flags["mc_all"] and not flags["flagged"]:
            raise ValueError(
                f"{rel}: row {num} publishes no level and is not PENDING — "
                f"refusing to render it as 'not authorised at any level'")
        states = states_for(min_idx, mc, flags["mc_all"])
        if flags["flagged"]:
            n_flag += 1
        rows.append(_render_row(num, act, states, flags["flagged"], flags))
    if not rows:
        return match.group(0)
    if n_pending == len(rows):
        # The whole table is PENDING (Aortic Dissection): no level exists
        # anywhere, so a five-pip strip would misread as "nobody may act".
        return match.group(0)
    return _render_block(rows, n_flag, n_pending)


def on_page_content(html, page, config, **kwargs):
    scope = scope_from(config)
    if not scope["enabled"]:
        return html
    src = getattr(getattr(page, "file", None), "src_uri", None)
    if scope["pages"] is not None and src not in scope["pages"]:
        return html
    # Placeholder first, and before the pip-block short circuit below: a page
    # with no level table at all (station-info.md) still asks for the legend.
    if LEGEND_TOKEN in html:
        html = html.replace(LEGEND_TOKEN, _legend())
    if 'data-pip-block' in html:
        return html
    return LVWRAP_RE.sub(functools.partial(transform_lvwrap, rel=src or "<unknown>"), html)

