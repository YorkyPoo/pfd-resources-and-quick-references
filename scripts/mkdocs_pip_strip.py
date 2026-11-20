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

Tables whose level cell is ``PENDING`` or ``POLICY`` publish no provider level
at all; they are left exactly as they are, because a five-pip strip has no slot
for "no level exists" and inventing one would be a clinical claim.
"""

from __future__ import annotations

import re

LEVELS = ["R", "B", "A", "I", "P"]
FULL = {"R": "EMR", "B": "EMT", "A": "AEMT", "I": "Intermediate", "P": "Paramedic"}
LEVEL_CLASS = {"lvl-emr": 0, "lvl-emt": 1, "lvl-a": 2, "lvl-i": 3, "lvl-p": 4}

# Scope: the owner's pilot is two pages, so the transform runs nowhere else.
# Adding a page is this one line — there is no per-page markup to copy.
PILOT_PAGES = {
    "protocols/general/02_Cold_Exposure_PROC.md",
    "protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md",
}

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


def parse_level_cell(html: str):
    """(min_idx, mc_levels, flags) from one rendered Level cell."""
    flags = {
        "mc_all": bool(re.search(r'class="[^"]*\blvl-mc\b', html)),
        "flagged": 'lvl-own' in html,
        "pending": 'lvl-pending' in html or 'lvl-policy' in html,
        "bracketed": 'lvl-mc-req' in html or 'lvl-req' in html,
    }
    min_idx = None
    for cls, idx in LEVEL_CLASS.items():
        if re.search(r'class="[^"]*\b' + re.escape(cls) + r'\b', html):
            min_idx = idx
            break
    mc = {min_idx} if (flags["bracketed"] and min_idx is not None) else set()
    return min_idx, mc, flags


# ----------------------------------------------------------------- rendering


def _tag(states, flagged):
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


def _aria(states, flagged):
    if flagged:
        return ("no verified provider level \u2014 OWNER_REQUIRED; "
                "the published level is not confirmed against the source")
    parts = [f"{LEVELS[i]} ({FULL[LEVELS[i]]}): {PIP_WORD[states[i]]}" for i in range(5)]
    return "; ".join(parts)


def _render_row(num, action_html, states, flagged):
    if flagged:
        # OWNER_REQUIRED: the page publishes a level the source does not
        # authorise. Outline-only pips (no solid fill anywhere) so a guess can
        # never read as a standing order. data-states keeps the page's own
        # claim for auditability; pip-strip.js never renders a verdict from it.
        pips = "".join('<i class="pip no unv"></i>' for _ in states)
    else:
        pips = "".join(f'<i class="pip {s}"></i>' for s in states)
    tcls, ttext = _tag(states, flagged)
    unv = ' data-unverified="1"' if flagged else ""
    return (
        f'<tr data-states="{",".join(states)}"{unv}>'
        f'<td class="pip-n">{num}</td>'
        f'<td class="pip-act"><div class="pip-action">{action_html}</div>'
        f'<span class="pip-tag-wrap"><span class="pip-tag {tcls}">{ttext}</span></span></td>'
        f'<td class="pip-strip-cell"><span class="pip-strip" role="img" '
        f'aria-label="{_aria(states, flagged)}">{pips}</span></td>'
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


def _render_block(rows, flagged=0):
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


def transform_lvwrap(match):
    """Rewrite one rendered .lv-wrap table, or return it untouched."""
    cls = match.group("cls") or ""
    if "pending" in cls or "policy" in cls:
        return match.group(0)
    body = match.group("body")
    row_mt = ROW_RE.findall(body)
    if not row_mt:
        return match.group(0)

    header_cells = CELL_RE.findall(row_mt[0])
    if len(header_cells) != 3 or header_cells[1][1].strip().lower() != "level":
        return match.group(0)

    rows = []
    n_flag = 0
    for raw in row_mt[1:]:
        cells = CELL_RE.findall(raw)
        if len(cells) != 3:
            return match.group(0)
        num, act = cells[0][1].strip(), cells[2][1].strip()
        min_idx, mc, flags = parse_level_cell(cells[1][1])
        if flags["pending"]:
            return match.group(0)
        states = states_for(min_idx, mc, flags["mc_all"])
        if flags["flagged"]:
            n_flag += 1
        rows.append(_render_row(num, act, states, flags["flagged"]))
    if not rows:
        return match.group(0)
    return _render_block(rows, n_flag)


def on_page_content(html, page, config, **kwargs):
    src = getattr(getattr(page, "file", None), "src_uri", None)
    if src not in PILOT_PAGES:
        return html
    if 'data-pip-block' in html:
        return html
    return LVWRAP_RE.sub(transform_lvwrap, html)
