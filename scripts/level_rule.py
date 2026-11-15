#!/usr/bin/env python3
"""Collapse a protocol's provider-level matrix to ONE level per action.

The owner's rule:
    "I need the provider levels to be correct for the intervention/actions.
     The lowest provider level followed by the intervention/action."

PEMS 2024 already prints it that way: one narrow column carrying a single provider
badge (EMR / EMT / A / I / P, or MC for a Medical-Control-contact row), then the
action text, with full-width section banners between blocks of rows. The site's
7-column EMR|EMT|A|I|P dot matrix was a re-encoding of that, and it re-encoded it
wrongly: it published every level the action is *permitted* at (cumulative dots) and,
on SVT, also typed the level into the action text. Both are the friction.

What this script does, per action row:
  1. resolves the PEMS 2024 row that authorises the action
     (row-bindings.yaml -> adjudicated.json -> alignment.json),
  2. takes that row's printed badge from audit/level-scan/pems_table.json,
  3. writes a single level chip, and strips level tokens out of the action text,
  4. refuses to invent a level: a row with no PEMS row keeps its current leftmost
     level and is flagged OWNER_REQUIRED in the ledger and on the page.

Three precedence tiers:
  * row-bindings.yaml — a data-extraction record: either a citation (pems_page /
    pems_ordinal, resolved against pems_table.json) or an explicit owner_required with
    a reason. Nothing there states a level; the level always comes from the source or
    from the page.
  * adjudicated.json — C2 visual rulings. A record with `resolved_cells` fixes the
    level for that row (leftmost filled column): a reviewed decision.
  * alignment.json — the C1 automatic binding, matched rows only.

A row bound to a *compound* PEMS row (one printed badge plus an inline level token such
as "[EMR]" or "(I / P)" scoping a clause) gets no chip: a single chip would contradict
either the badge or the row's own wording. It is flagged OWNER_REQUIRED.

Every level-table region of a page is converted; non-level tables (dosing charts,
weight grids) are left byte-identical.

Usage:
    python3 scripts/level_rule.py --map      # print the resolution, change nothing
    python3 scripts/level_rule.py --write    # rewrite the target pages + ledger
    python3 scripts/level_rule.py --check    # verify the published pages
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUD = os.path.join(ROOT, 'audit', 'level-scan')
DOCS = os.path.join(ROOT, 'docs')

# Batch 1 — protocols/cardiac/. The two pages converted in t_e71bb92c are listed first
# so --check keeps verifying them and --write stays a no-op on them.
TARGETS = [
    'protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md',
    'protocols/cardiac/04_Post_Resuscitation_Care_PROC.md',
    'protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.md',
    'protocols/cardiac/04_Bradycardia_PROC.md',
    'protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md',
    'protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.md',
    'protocols/cardiac/04_Chest_Pain_ACS_PROC.md',
    'protocols/cardiac/04_Hypertensive_Crisis_PROC.md',
    'protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.md',
    # Batch 2 — protocols/medical/ + protocols/neurologic/. Derived from the tree:
    # every page in those two directories, nothing hand-picked.
    'protocols/medical/07_Sepsis_PROC.md',
    'protocols/medical/07_Allergic_Reaction_Anaphylaxis_PROC.md',
    'protocols/medical/07_OB_Emergencies_PROC.md',
    'protocols/medical/07_Hypotension_Shock_Non_Trauma_PROC.md',
    'protocols/neurologic/05_Seizure_PROC.md',
    'protocols/neurologic/05_Hypoglycemia_Hyperglycemia_PROC.md',
    'protocols/neurologic/05_Stroke_TIA_PROC.md',
]

# Pages sourced from OUTSIDE PEMS 2024. PEMS prints no equivalent protocol, so no row on
# these pages can be verified against it: every action row is chipped PENDING (Pending OMD
# Authorization) and the level the agency page already published is recorded in the ledger
# as `carried_from_page`. Sources live in audit/level-scan/pending-protocols.yaml.
PENDING_TARGETS = [
    'protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.md',
]

LV = ['EMR', 'EMT', 'A', 'I', 'P']
CHIP_CLASS = {'EMR': 'emr', 'EMT': 'emt', 'A': 'a', 'I': 'i', 'P': 'p', 'MC': 'mc',
              'PENDING': 'pending'}
PENDING_YAML = os.path.join(AUD, 'pending-protocols.yaml')
PENDING_CHIP = '<span class="lvl lvl-pending">PENDING</span>'
PENDING_REASON = ('this protocol is not published in PEMS 2024; its source prints no PEMS '
                  'row to cite, so the level is not verified against a regional source')
TEXT_TOKEN = re.compile(r'(?<![A-Za-z0-9])(EMR|EMT|A|I|P|MC)\s*:\s*')
# Level words that can survive inside action text. TEXT_TOKEN above only sees the
# "LEVEL:" prefixes the stripper removes, so a check built on it cannot see
# "(as determined by EMT-I or P)" or "(AED for EMR/EMT, Manual for I/P)" — the very
# tokens the conversion was supposed to settle. These four patterns do, and every hit
# they make must be covered by an explicit keep decision in token-decisions.yaml.
LEVEL_WORD = re.compile(r'\b(?:EMR|EMT|AEMT|Paramedic|Intermediate)\b', re.I)
LEVEL_PAREN = re.compile(r'\([^)]*\b(?:A|I|P)\b[^)]*\)')
LEVEL_PAIR = re.compile(r'(?<![A-Za-z0-9])(?:A|I|P|EMR|EMT)\s*/\s*(?:A|I|P|EMR|EMT)'
                        r'(?![A-Za-z0-9])')
LEVEL_RANGE = re.compile(r'(?<![A-Za-z0-9])(?:EMR|EMT|A|I|P)\s*(?:-|or)\s*(?:A|I|P)'
                         r'(?![A-Za-z0-9])')
LEVEL_HIT_RES = (LEVEL_WORD, LEVEL_PAREN, LEVEL_PAIR, LEVEL_RANGE)
TOKEN_DECISIONS_YAML = os.path.join(AUD, 'token-decisions.yaml')
SEPARATOR = re.compile(r'^\|[\s:|-]+\|$')
NEW_HEADER = '| # | Level | Action / Intervention |'
DIV_OPEN = '<div class="lv-wrap" markdown="1">'
DIV_PENDING_OPEN = '<div class="lv-wrap pending" markdown="1">'
CHIP_RE = re.compile(r'<span class="lvl lvl-([a-z]+)">([A-Z]+)</span>')
LEVEL_HEADER = re.compile(r'^\|\s*#\s*\|')
DIV_ANY = re.compile(r'^<div class="(sc|lv)-wrap')
# inline level tokens inside a PEMS row's printed text
INLINE_BRACKET = re.compile(r'\[(EMR|EMT|A|I|P)\]')
INLINE_PAREN = re.compile(r'\((EMR|EMT|A|I|P)\s*/\s*(EMR|EMT|A|I|P)\)')


# --------------------------------------------------------------------- parsing
def split_cells(line):
    return [p.strip() for p in line.strip().strip('|').split('|')]


def is_level_header(line):
    if not LEVEL_HEADER.match(line):
        return None
    if 'EMR' in line:
        return 'old'
    if 'Level' in line:
        return 'new'
    return None


def table_rows(block_lines):
    """Table rows of one <div> block, in order."""
    out, fmt = [], None
    for line in block_lines:
        fmt_line = is_level_header(line)
        if fmt_line:
            fmt = fmt_line
            continue
        if fmt is None:
            continue
        if SEPARATOR.match(line):
            continue
        if not line.strip().startswith('|'):
            fmt = None
            continue
        cells = split_cells(line)
        if fmt == 'new':
            if len(cells) < 3:
                continue
            out.append({'ordinal': cells[0], 'action': cells[2],
                        'level_cell': cells[1], 'cells': None})
        else:
            if len(cells) < 7:
                continue
            out.append({'ordinal': cells[0], 'action': cells[1], 'cells': cells[2:7],
                        'level_cell': None})
    return out


def is_banner(row):
    if row['cells'] is None:
        return False
    text = row['action'].strip()
    return text.startswith('**') and text.endswith('**') and not any(c.strip() for c in row['cells'])


def find_regions(lines):
    """Every level-matrix region on the page, with its exact line span.

    A region is the level table inside a <div class="sc-wrap|lv-wrap"> wrapper, an
    optional `#### BANNER` heading immediately above it, and an optional trailing
    <p class="lv-note">. Non-level tables (dosing charts, weight grids) are not
    regions and are left untouched.
    """
    regions, i, n = [], 0, len(lines)
    while i < n:
        if not DIV_ANY.match(lines[i]):
            i += 1
            continue
        k = i + 1
        while k < n and not lines[k].startswith('</div>'):
            k += 1
        body = lines[i + 1:k]
        is_level = any(is_level_header(l) for l in body)
        if not is_level:
            i = k + 1
            continue
        start, banner = i, None
        p = i - 1
        while p >= 0 and lines[p].strip() == '':
            p -= 1
        if p >= 0 and re.match(r'^#### ', lines[p]):
            banner = lines[p][5:].strip()
            start = p
        end = k
        q = end + 1
        while q < n and lines[q].strip() == '':
            q += 1
        if q < n and lines[q].startswith('<p class="lv-note">'):
            r = q
            while r < n and '</p>' not in lines[r]:
                r += 1
            end = r
        regions.append({'start': start, 'end': end, 'banner': banner,
                        'rows': table_rows(body)})
        i = end + 1
    return regions


def parse_page(path):
    """Every action row on the page in document order (banners excluded)."""
    lines = open(path, encoding='utf-8').read().split('\n')
    return [r for reg in find_regions(lines) for r in reg['rows'] if not is_banner(r)]


def leftmost_level(cells):
    if cells is None:
        return None
    toks = [c.strip('[] ').upper() for c in cells]
    filled = [t for t in toks if t]
    if not filled:
        return None
    if all(t == 'MC' for t in filled):
        return 'MC'
    for i, t in enumerate(toks):
        if t:
            return LV[i] if i < len(LV) else None
    return None


def cells_level(cells):
    """Leftmost filled column of a resolved_cells list (a C2 decision)."""
    if not cells or not isinstance(cells, list):
        return None
    toks = [str(c).strip('[] ').upper() for c in cells]
    filled = [t for t in toks if t]
    if filled and all(t == 'MC' for t in filled):
        return 'MC'
    for i, t in enumerate(toks):
        if t and i < len(LV):
            return LV[i]
    return None


def marked_levels(cells):
    if cells is None:
        return []
    return [LV[i] for i, c in enumerate(cells) if i < len(LV) and c.strip()]


def text_label(action):
    m = TEXT_TOKEN.match(action)
    return m.group(1) if m else None


def strip_tokens(action):
    """Remove level tokens typed into the action text; report them.

    A token at the start is a duplicated level prefix and is simply dropped. A token
    inside the sentence ("...after two attempts, MC: Contact Medical Control") loses
    its colon and the capital that followed it, so the sentence still reads as one.
    """
    found, out, pos = [], [], 0
    for m in TEXT_TOKEN.finditer(action):
        out.append(action[pos:m.start()])
        nxt = action[m.end():m.end() + 1]
        if m.start() > 0 and nxt.isupper():
            nxt = nxt.lower()
        out.append(nxt)
        found.append(m.group(1))
        pos = m.end() + 1
    out.append(action[pos:])
    return ''.join(out), found


def level_hits(action):
    """Every provider-level expression left in an action text, as merged spans.

    Deliberately independent of strip_tokens: it does not care who put the word
    there, only that a level word is in the published sentence. Overlapping matches
    from the four patterns collapse to the widest span, so one parenthetical counts
    once even though LEVEL_WORD, LEVEL_PAIR and LEVEL_RANGE all fire inside it.
    """
    spans = []
    for rx in LEVEL_HIT_RES:
        for m in rx.finditer(action):
            spans.append((m.start(), m.end()))
    merged = []
    for start, end in sorted(spans):
        if merged and start < merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [action[s:e] for s, e in merged]


def load_token_decisions():
    """Explicit keep/remove decisions for level words that survive in action text.

    Returns (kept, removed): kept is keyed (file, row) -> list of hit strings, removed
    is a list of records. A level word left on a page is a failure unless a `kept`
    record names it, and a `kept` record that no longer matches the page is a failure
    too, so the file cannot rot into a rubber stamp.
    """
    import yaml
    if not os.path.exists(TOKEN_DECISIONS_YAML):
        return {}, []
    doc = yaml.safe_load(open(TOKEN_DECISIONS_YAML, encoding='utf-8')) or {}
    kept, removed = {}, []
    for rec in doc.get('kept') or []:
        if not rec.get('file') or rec.get('row') is None:
            raise SystemExit(f'token-decisions.yaml: incomplete kept record {rec!r}')
        for k in ('hits', 'reason'):
            if not rec.get(k):
                raise SystemExit(f'token-decisions.yaml: {rec["file"]} row {rec["row"]} '
                                 f'kept record has no {k}')
        kept.setdefault((rec['file'], str(rec['row'])), []).extend(rec['hits'])
    for rec in doc.get('removed') or []:
        for k in ('file', 'row', 'hit', 'reason'):
            if rec.get(k) in (None, ''):
                raise SystemExit(f'token-decisions.yaml: incomplete removed record {rec!r}')
        removed.append(rec)
    return kept, removed


# ----------------------------------------------------------------- level source
def load_json(name):
    with open(os.path.join(AUD, name), encoding='utf-8') as fh:
        return json.load(fh)


RULINGS_YAML = os.path.join(AUD, 'level-rulings.yaml')
BINDINGS_YAML = os.path.join(AUD, 'row-bindings.yaml')
WORDING_YAML = os.path.join(AUD, 'wording-rulings.yaml')
STYLESHEET_YAML = os.path.join(AUD, 'stylesheet-changes.yaml')


def load_wording_rulings():
    """Owner rulings on wording (not level): decisions the source text does not support.

    Recorded so a later pass cannot "restore" the source reading as if the page were wrong.
    """
    import yaml
    if not os.path.exists(WORDING_YAML):
        return []
    doc = yaml.safe_load(open(WORDING_YAML, encoding='utf-8')) or {}
    out = []
    for rec in doc.get('rulings') or []:
        for k in ('file', 'page_reads', 'ruling'):
            if not rec.get(k):
                raise SystemExit(f'wording-rulings.yaml: incomplete ruling {rec!r}')
        if rec.get('status') != 'owner_ruled':
            raise SystemExit(f'wording-rulings.yaml: status must be "owner_ruled" ({rec}')
        out.append(rec)
    return out


def load_stylesheet_changes():
    """Deliberate cross-page CSS changes, so a reviewer does not read them as accidents."""
    import yaml
    if not os.path.exists(STYLESHEET_YAML):
        return []
    doc = yaml.safe_load(open(STYLESHEET_YAML, encoding='utf-8')) or {}
    out = []
    for rec in doc.get('changes') or []:
        for k in ('date', 'files', 'why'):
            if not rec.get(k):
                raise SystemExit(f'stylesheet-changes.yaml: incomplete entry {rec!r}')
        out.append(rec)
    return out


def load_rulings():
    """Owner rulings keyed (file, row). A ruling is a decision, never a source citation."""
    import yaml
    if not os.path.exists(RULINGS_YAML):
        return {}
    doc = yaml.safe_load(open(RULINGS_YAML, encoding='utf-8')) or {}
    out = {}
    for rec in doc.get('rulings') or []:
        if not rec.get('file') or rec.get('row') is None or not rec.get('level'):
            raise SystemExit(f'level-rulings.yaml: incomplete ruling {rec!r}')
        if rec.get('status') != 'owner_ruled':
            raise SystemExit(f'level-rulings.yaml: status must be "owner_ruled" (row {rec}')
        out[(rec['file'], str(rec['row']))] = rec
    return out


def load_bindings():
    """Row-level citations / owner_required declarations, keyed (file, row).

    Validated loudly: a binding must name an existing-kind PEMS pointer and may never
    state a level; an owner_required must carry a reason.
    """
    import yaml
    if not os.path.exists(BINDINGS_YAML):
        return {}
    doc = yaml.safe_load(open(BINDINGS_YAML, encoding='utf-8')) or {}
    out = {}
    for rec in doc.get('bindings') or []:
        if not rec.get('file') or rec.get('row') is None:
            raise SystemExit(f'row-bindings.yaml: incomplete entry {rec!r}')
        if 'level' in rec:
            raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} states a '
                             f'level — a binding cites the source, it never sets a level')
        status = rec.get('status')
        if status == 'owner_required':
            if not rec.get('reason'):
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} is '
                                 f'owner_required without a reason')
        elif status not in (None, 'bound'):
            raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} has unknown '
                             f'status {status!r}')
        elif rec.get('pems_page') is None or rec.get('pems_ordinal') is None:
            raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} is a binding '
                             f'without pems_page/pems_ordinal')
        out[(rec['file'], str(rec['row']))] = rec
    return out


def load_pending():
    """Pages sourced outside PEMS 2024, keyed by file.

    Validated loudly: the source is required, no PEMS pointer may be stated (that would be
    the fake citation this file exists to prevent), and every action row must have a
    carried level recorded.
    """
    import yaml
    if not os.path.exists(PENDING_YAML):
        return {}
    doc = yaml.safe_load(open(PENDING_YAML, encoding='utf-8')) or {}
    out = {}
    for rec in doc.get('protocols') or []:
        if not rec.get('file') or not rec.get('source'):
            raise SystemExit(f'pending-protocols.yaml: incomplete entry {rec!r}')
        for k in ('pems_page', 'pems_ordinal', 'pems_badge', 'pems_text'):
            if rec.get(k) is not None:
                raise SystemExit(f'pending-protocols.yaml: {rec["file"]} states {k} — a '
                                 f'pending protocol may not claim a PEMS citation')
        if not rec.get('carried_levels'):
            raise SystemExit(f'pending-protocols.yaml: {rec["file"]} has no carried_levels')
        out[rec['file']] = rec
    return out


def pending_note(spec):
    """The visible note printed above a pending protocol's table."""
    return ('**Pending OMD Authorization** — this protocol is sourced from '
            f'{spec["source"]}. PEMS 2024 does not publish this protocol. Levels below are '
            "carried from the agency's existing page and are **not verified against a "
            'regional source**.')


def note_para(note):
    """A note as the HTML paragraph written to the page.

    Markdown bold is converted here, not by attr_list: a paragraph inside a `markdown="1"`
    div does not get it, and the note must never render as literal `**` text.
    """
    return ('<p class="lv-note">' + re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', note)
            + '</p>')


def pending_note_html(spec):
    """The Pending OMD note exactly as it is written onto the page."""
    return note_para(pending_note(spec))


def pems_index(table):
    idx = {}
    for doc in table['pems_docs']:
        for row in doc['rows']:
            idx[(row['page'], row['ordinal'])] = row
    return idx


def badge_of(row):
    """The single provider badge PEMS prints for this row, and its bracket flag."""
    cols = row.get('columns') or {}
    filled = [v for v in cols.values() if v]
    if filled and all(v == 'MC' for v in filled):
        return 'MC', False
    tok = (row.get('badge_tokens') or [None])[0]
    if not tok:
        return None, False
    return tok.strip('[] '), tok.strip().startswith('[')


def compound_tokens(row):
    """Inline level tokens inside the PEMS row text, e.g. '(I / P)' or '[EMR]'.

    PEMS prints ONE badge per row but sometimes scopes a clause to another level in the
    text. Such a row cannot be reproduced as a single chip without contradicting either
    the badge or the row's own wording.
    """
    if not row:
        return []
    text = row.get('verbatim_text') or ''
    found = INLINE_BRACKET.findall(text)
    for a, b in INLINE_PAREN.findall(text):
        found += [a, b]
    return sorted(set(found))


def significant(text):
    return {w for w in re.findall(r'[a-z]{3,}', text.lower())}


def resolve(rel, rows, align, adjudicated, pems, bindings=None):
    """Per-row PEMS citation, derived — hand-written only in row-bindings.yaml."""
    bindings = bindings or {}
    page = next((p for p in align['pages'] if p['site_page'] == rel), None)
    by_row = {str(r['site_row']): r for r in (page['rows'] if page else [])}
    adj = {}
    for rec in adjudicated['records']:
        if rec.get('file') == rel and rec.get('row') is not None:
            adj[str(rec['row'])] = rec

    # PEMS rows the alignment merged into an unnamed site row: bind by text overlap —
    # the same signal that produced the recorded 0.78 best_similarity_to_a_site_row.
    merged = {}
    for entry in (page or {}).get('merged_into_site_row', []) or []:
        best, best_score = None, 0.0
        for row in rows:
            a, b = significant(entry['verbatim_text']), significant(strip_tokens(row['action'])[0])
            if not (a and b):
                continue
            score = len(a & b) / len(a | b)
            if score > best_score:
                best, best_score = row, score
        if best is not None:
            merged[str(best['ordinal'])] = ((entry['pems_page'], entry['ordinal']), best_score)

    out = []
    for row in rows:
        ordinal = str(row['ordinal'])
        ptr, basis, extra = None, None, {}
        a = by_row.get(ordinal)
        rec = adj.get(ordinal)
        if a and a['status'] == 'matched':
            ptr, basis = (a['pems_page'], a['pems_ordinal']), 'alignment:matched'
        elif rec and rec.get('pems_page') is not None:
            # the adjudicated ruling is the reviewed pointer; it outranks an unresolved
            # "shared_pems_row" marker in the alignment pass
            ptr, basis = (rec['pems_page'], rec['pems_ordinal']), 'adjudicated:' + rec['decision']
            extra['adjudication'] = rec.get('verdict')
        elif a and a.get('reason_kind') == 'shared_pems_row':
            ci = a.get('contained_in_pems') or {}
            ptr, basis = (ci.get('pems_page'), ci.get('pems_ordinal')), 'alignment:shared_pems_row'
        elif ordinal in merged:
            ptr, basis = merged[ordinal][0], 'alignment:merged_into_site_row'
            extra['merge_overlap'] = round(merged[ordinal][1], 2)
        elif a and a.get('status') == 'ambiguous':
            extra['alignment_reason'] = a.get('reason')
            if not rec:
                ci = a.get('contained_in_pems') or {}
                if ci.get('pems_page') is not None:
                    ptr, basis = (ci['pems_page'], ci['pems_ordinal']), 'alignment:ambiguous'

        resolved_cite = None
        if rec and isinstance(rec.get('resolved_cells'), list) and len(rec['resolved_cells']) == 5:
            resolved_cite = rec
            if rec.get('pems_page') is not None:
                ptr = (rec['pems_page'], rec['pems_ordinal'])

        b = bindings.get((rel, ordinal))
        if b:
            extra['binding'] = b
            if b.get('pems_page') is not None:
                ptr, basis = (b['pems_page'], b['pems_ordinal']), 'row-bindings:bound'
                extra['binding_evidence'] = b.get('evidence')
            if b.get('status') == 'owner_required':
                extra['forced_owner'] = b['reason']

        source_row = pems.get(ptr) if ptr else None
        badge, bracketed = badge_of(source_row) if source_row else (None, False)
        out.append({'ordinal': ordinal, 'ptr': ptr, 'basis': basis, 'badge': badge,
                    'bracketed': bracketed, 'pems_row': source_row, 'extra': extra,
                    'adjudicated': rec, 'resolved': resolved_cite})
    return out


# ------------------------------------------------------------------- rendering
def chip(level, bracketed=False, owner=False):
    html = f'<span class="lvl lvl-{CHIP_CLASS.get(level, "na")}">{level}</span>'
    if bracketed:
        html += ('<sup class="lvl-req" title="PEMS 2024 prints this badge in brackets: agency '
                 'training documentation and Medical Control written authorization required">*</sup>')
    if owner:
        html += ('<sup class="lvl-own" title="OWNER_REQUIRED: no PEMS 2024 row authorises this '
                 'action\'s provider level">&#9873;</sup>')
    return html


def render_block(rows, note=None, banner=None):
    out = []
    if banner:
        out += [banner, '']
    out += [DIV_OPEN, '', NEW_HEADER, '|:---:|---|---|']
    for r in rows:
        cell = r.get('level_cell') or chip(r['level'], r.get('bracketed', False),
                                           r.get('owner', False))
        out.append(f"| {r['ordinal']} | {cell} | {r['action']} |")
    out += ['', '</div>']
    if note:
        # written as HTML, not markdown: attr_list does not run on a paragraph inside a
        # markdown="1" div, and the note must never render as raw "{: .lv-note }" text.
        out += ['', '<p class="lv-note">' + re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', note)
                + '</p>']
    return out


def heading_for(text):
    plain = text.strip().strip('*').strip()
    return '#### ' + plain[:1].upper() + plain[1:]


def prior_tokens():
    """Level tokens a previous run already stripped, keyed (file, row).

    The page no longer carries them, so a re-run of --write would otherwise report
    "0 row(s)" and silently erase the record of what the collapse changed.
    """
    try:
        rows = load_json('level-rule-ledger.json')['rows']
    except (FileNotFoundError, KeyError):
        return {}
    return {(e['file'], str(e['row'])): (e.get('before') or {}).get('text_tokens') or []
            for e in rows}


def prior_before():
    """The pre-conversion 'before' record, keyed (file, row).

    Once a page is in the collapsed format its leftmost/markers are gone from the page
    itself, so a re-run must carry them forward from the ledger or the record of what
    the conversion changed is lost (and "level moved by the source" reports 0).
    """
    try:
        rows = load_json('level-rule-ledger.json')['rows']
    except (FileNotFoundError, KeyError):
        return {}
    out = {}
    for e in rows:
        b = e.get('before') or {}
        if b.get('leftmost') is not None or b.get('markers'):
            out[(e['file'], str(e['row']))] = b
    return out


# ------------------------------------------------------------------- the build
def _decide(row, r, ruled_for_row):
    """(level, owner, status, reason, new_text, before, ruled) for one action row."""
    existing = CHIP_RE.search(row['level_cell'] or '')
    before_low = (leftmost_level(row['cells']) if row['cells'] is not None
                  else (existing.group(2) if existing else None))
    marked = marked_levels(row['cells'])
    new_text, stripped = strip_tokens(row['action'])
    before = {'leftmost': before_low, 'markers': marked,
              'text_label': text_label(row['action']), 'text_tokens': stripped}

    extra = r['extra']
    if ruled_for_row:
        # the owner's decision replaces the inherited level; it is NOT PEMS-verified
        return ruled_for_row['level'], False, 'owner_ruled', None, new_text, before, ruled_for_row

    resolved_level = cells_level((r['resolved'] or {}).get('resolved_cells'))
    tokens = compound_tokens(r['pems_row'])

    if extra.get('forced_owner'):
        return (before_low, True, 'OWNER_REQUIRED', extra['forced_owner'], new_text, before, None)
    if resolved_level:
        return resolved_level, False, 'OK', None, new_text, before, None
    if r['badge'] is None:
        reason = (extra.get('alignment_reason')
                  or 'no PEMS 2024 row authorises this action\'s provider level')
        return (before_low, True, 'OWNER_REQUIRED', reason, new_text, before, None)
    if tokens:
        reason = ('PEMS prints one badge (%s) on a compound row whose own text scopes a clause '
                  'to %s; a single chip would contradict either the badge or the row\'s own '
                  'text' % (r['badge'], '/'.join(tokens)))
        return (before_low, True, 'OWNER_REQUIRED', reason, new_text, before, None)
    return r['badge'], False, 'OK', None, new_text, before, None


def plan(rel):
    """Return (regions_out, ledger, problems, lines, regions) for one page."""
    path = os.path.join(DOCS, rel)
    align = load_json('alignment.json')
    adjudicated = load_json('adjudicated.json')
    pems = pems_index(load_json('pems_table.json'))
    rulings, bindings = load_rulings(), load_bindings()
    prior_tok = prior_tokens()
    prior = prior_before()

    lines = open(path, encoding='utf-8').read().split('\n')
    regions = find_regions(lines)
    actions = [r for reg in regions for r in reg['rows'] if not is_banner(r)]
    res = resolve(rel, actions, align, adjudicated, pems, bindings)

    ledger, problems, regions_out = [], [], []
    cursor = 0
    for reg in regions:
        blocks = [{'banner': None, 'rows': []}]
        for row in reg['rows']:
            if is_banner(row):
                blocks.append({'banner': heading_for(row['action']), 'rows': []})
                continue
            r = res[cursor]
            cursor += 1
            ruled = rulings.get((rel, str(row['ordinal'])))
            level, owner, status, reason, new_text, before, ruled = _decide(row, r, ruled)
            prior_b = prior.get((rel, str(row['ordinal'])))
            if prior_b and row['cells'] is None:
                # already collapsed: the page itself no longer holds the pre-conversion
                # record, so carry it forward from the ledger
                before = {'leftmost': prior_b.get('leftmost'), 'markers': prior_b.get('markers') or [],
                          'text_label': prior_b.get('text_label'),
                          'text_tokens': before['text_tokens'] or prior_b.get('text_tokens') or []}
                if (status == 'OWNER_REQUIRED' and prior_b.get('leftmost')
                        and level != prior_b['leftmost']):
                    # an uncited row keeps the level the page published before conversion —
                    # never a level that only a now-withdrawn binding justified
                    level = prior_b['leftmost']
            stripped = before['text_tokens'] or prior_tok.get((rel, str(row['ordinal'])), [])
            before['text_tokens'] = stripped
            if level is None:
                problems.append(f'{rel} row {row["ordinal"]}: no PEMS level and no existing '
                                f'marker — cannot place a marker')
            blocks[-1]['rows'].append({'ordinal': row['ordinal'], 'action': new_text,
                                       'level': level, 'bracketed': r['bracketed'],
                                       'owner': owner})
            ledger.append({
                'file': rel,
                'row': int(row['ordinal']),
                'action': re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', new_text)
                              .replace('**', '').replace('<br>', ' ')[:150],
                'level_published': level,
                'status': status,
                'reason': reason,
                'owner_ruling': ({'date': ruled['date'], 'ruling': ruled['ruling'],
                                  'note': ruled.get('note')} if ruled else None),
                'pems_page': r['ptr'][0] if r['ptr'] else None,
                'pems_ordinal': r['ptr'][1] if r['ptr'] else None,
                'pems_badge': r['badge'],
                'compound_tokens': compound_tokens(r['pems_row']),
                'bracketed': r['bracketed'],
                'pems_text': (r['pems_row'] or {}).get('verbatim_text'),
                'binding_evidence': r['extra'].get('binding_evidence'),
                'basis': r['basis'],
                'before': before,
                'note': r['extra'].get('adjudication'),
            })
        if reg['banner']:
            blocks[0]['banner'] = heading_for(reg['banner'])
        regions_out.append({'blocks': blocks})
    return regions_out, ledger, problems, lines, regions


def page_note_for(ledger):
    notes = []
    owner_rows = [str(e['row']) for e in ledger if e['status'] == 'OWNER_REQUIRED']
    if owner_rows:
        label = ('row ' + owner_rows[0] if len(owner_rows) == 1
                 else 'rows ' + ', '.join(owner_rows))
        notes.append('&#9873; **OWNER_REQUIRED** — ' + label +
                     ': no PEMS 2024 row authorises a provider level for this action. The level '
                     'shown is the one this page already published; it is not verified against '
                     'the source. See <code>audit/level-scan/level-rule-ledger.md</code>.')
    if any(e['bracketed'] for e in ledger):
        notes.append('* **[ ] badge in PEMS 2024** — the source prints this level in brackets: '
                     'agency post-affiliation training documentation on file, plus the '
                     "Medical Control written authorization for that skill. The bracketing is the source's, "
                     'not this page\'s.')
    return '\n\n'.join(notes) if notes else None


def splice(rel):
    """Rewrite every level-table region; leave every other line byte-identical."""
    regions_out, ledger, problems, lines, regions = plan(rel)
    if problems:
        for p in problems:
            print('PROBLEM:', p)
        raise SystemExit(2)
    page_note = page_note_for(ledger)

    out, last = [], 0
    for ri, (reg, reg_out) in enumerate(zip(regions, regions_out)):
        out += lines[last:reg['start']]
        pieces = []
        for bi, block in enumerate(reg_out['blocks']):
            last_block = (ri == len(regions) - 1 and bi == len(reg_out['blocks']) - 1)
            if bi:
                pieces.append('')
            pieces += render_block(block['rows'], note=(page_note if last_block else None),
                                   banner=block['banner'])
        out += pieces
        last = reg['end'] + 1
    out += lines[last:]
    with open(os.path.join(DOCS, rel), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out))


def render_note(note):
    """The note as it lands on the page: markdown bold turned into <strong>."""
    return '<p class="lv-note">' + re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', note) + '</p>'


def render_pending_block(rows, note=None, banner=None):
    """The 3-column chassis for a page PEMS does not publish, note first, no dot grid."""
    out = []
    if banner:
        out += [banner, '']
    if note:
        out += [note_para(note), '']
    out += [DIV_PENDING_OPEN, '', NEW_HEADER, '|:---:|---|---|']
    for r in rows:
        out.append(f"| {r['ordinal']} | {PENDING_CHIP} | {r['action']} |")
    out += ['', '</div>']
    return out


def plan_pending(rel, spec):
    """(regions_out, ledger, problems, lines, regions) for one non-PEMS page.

    No PEMS row is looked up, none is cited, and no level is invented: the chip is PENDING
    on every row and the level the page already published is recorded as carried_from_page.
    """
    path = os.path.join(DOCS, rel)
    carried = {int(k): str(v).upper() for k, v in (spec['carried_levels'] or {}).items()}
    lines = open(path, encoding='utf-8').read().split('\n')
    regions = find_regions(lines)

    ledger, problems, regions_out = [], [], []
    for reg in regions:
        blocks = [{'banner': None, 'rows': []}]
        for row in reg['rows']:
            if is_banner(row):
                blocks.append({'banner': heading_for(row['action']), 'rows': []})
                continue
            ordinal = row['ordinal']
            existing = CHIP_RE.search(row['level_cell'] or '')
            on_page = (leftmost_level(row['cells']) if row['cells'] is not None
                       else (existing.group(2) if existing else None))
            recorded = carried.get(int(ordinal)) if str(ordinal).isdigit() else None
            if row['cells'] is not None and recorded and on_page != recorded:
                problems.append(f'{rel} row {ordinal}: pending-protocols.yaml records carried '
                                f'level {recorded} but the page publishes {on_page}')
            if recorded is None:
                problems.append(f'{rel} row {ordinal}: no carried_levels entry in '
                                f'pending-protocols.yaml')
            new_text, stripped = strip_tokens(row['action'])
            blocks[-1]['rows'].append({'ordinal': ordinal, 'action': new_text,
                                       'level': 'PENDING', 'bracketed': False,
                                       'owner': False})
            ledger.append({
                'file': rel,
                'row': int(ordinal),
                'action': re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', new_text)
                              .replace('**', '').replace('<br>', ' ')[:150],
                'level_published': 'PENDING',
                'status': 'pending_omd',
                'reason': PENDING_REASON,
                'owner_ruling': None,
                # no PEMS row, no PEMS badge, no PEMS text: this page is not a PEMS protocol
                'pems_page': None,
                'pems_ordinal': None,
                'pems_badge': None,
                'compound_tokens': [],
                'bracketed': False,
                'pems_text': None,
                'binding_evidence': None,
                'basis': None,
                'carried_from_page': recorded,
                'pending_source': spec['source'],
                'before': {'leftmost': on_page, 'markers': marked_levels(row['cells']),
                           'text_label': text_label(row['action']),
                           'text_tokens': stripped},
                'note': 'not PEMS 2024 — pending OMD authorization',
            })
        if reg['banner']:
            blocks[0]['banner'] = heading_for(reg['banner'])
        regions_out.append({'blocks': blocks})
    return regions_out, ledger, problems, lines, regions


def strip_trailing_notes(chunk):
    """Drop note paragraphs at the tail of a preserved slice.

    The pending renderer emits the Pending OMD Authorization note itself, so a note that
    already sits directly above the table (written by an earlier run or by hand) would be
    duplicated on every --write. Strip it from the preserved slice and let the renderer
    own the note, which keeps --write idempotent.
    """
    i = len(chunk)
    stripped = False
    while True:
        j = i
        while j > 0 and chunk[j - 1].strip() == '':
            j -= 1
        if j > 0 and chunk[j - 1].startswith('<p class="lv-note">') and '</p>' in chunk[j - 1]:
            i = j - 1
            stripped = True
        else:
            break
    return chunk[:i] if stripped else chunk


def splice_pending(rel, spec):
    """Rewrite every level-table region of a pending page; leave every other line as-is."""
    regions_out, ledger, problems, lines, regions = plan_pending(rel, spec)
    if problems:
        for p in problems:
            print('PROBLEM:', p)
        raise SystemExit(2)
    note = pending_note(spec)
    out, last = [], 0
    for reg, reg_out in zip(regions, regions_out):
        out += strip_trailing_notes(lines[last:reg['start']])
        pieces = []
        for bi, block in enumerate(reg_out['blocks']):
            if bi:
                pieces.append('')
            pieces += render_pending_block(block['rows'], note=(note if bi == 0 else None),
                                           banner=block['banner'])
        out += pieces
        last = reg['end'] + 1
    out += lines[last:]
    with open(os.path.join(DOCS, rel), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out))


def git_show(rev, rel):
    try:
        return subprocess.run(['git', '-C', ROOT, 'show', f'{rev}:docs/{rel}'],
                              capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None


def defect_counts():
    """The three defects named in the owner's rule, measured on the branch base."""
    base = subprocess.run(['git', '-C', ROOT, 'merge-base', 'HEAD', 'level-scan'],
                          capture_output=True, text=True, check=True).stdout.strip()
    totals = {'rows': 0, 'level_in_text': 0, 'label_vs_leftmost': 0,
              'multi_marker': 0, 'no_marker': 0}
    per_file = {}
    tmp = os.path.join(ROOT, '.level-rule-base.tmp')
    for rel in TARGETS:
        text = git_show(base, rel)
        if text is None:
            continue
        with open(tmp, 'w', encoding='utf-8') as fh:
            fh.write(text)
        rows = parse_page(tmp)
        os.unlink(tmp)
        c = {'rows': len(rows),
             'level_in_text': sum(1 for r in rows if text_label(r['action'])),
             'multi_marker': sum(1 for r in rows if len(marked_levels(r['cells'])) > 1),
             'no_marker': sum(1 for r in rows if not marked_levels(r['cells'])),
             'label_vs_leftmost': sum(1 for r in rows
                                      if text_label(r['action']) and leftmost_level(r['cells'])
                                      and text_label(r['action']) != leftmost_level(r['cells']))}
        per_file[rel] = c
        for k in totals:
            totals[k] += c[k]
    return base, per_file, totals


def emit_md(ledger):
    """The per-action citation table: one line per action row, source cited."""
    lines = ['# Level rule — per-action PEMS citation', '',
             'Generated by `scripts/level_rule.py`. Rule: **one marker per action = the lowest',
             'provider level PEMS 2024 prints for that action**, and the level never appears in',
             'the action text.', '',
             '`basis` says how the PEMS row was bound:',
             '',
             '| basis | meaning |',
             '|---|---|',
             '| `row-bindings:bound` | a row-level citation in `audit/level-scan/row-bindings.yaml`, evidence recorded there |',
             '| `alignment:matched` | section+ordinal match in `alignment.json` |',
             '| `adjudicated:*` | a C2 ruling in `adjudicated.json` |',
             '| `alignment:merged_into_site_row` | PEMS merges rows the page splits |',
             '| `alignment:ambiguous` | an ambiguous alignment row, cited but not machine-matched |',
             '',
             '| file | row | level | PEMS row | PEMS printed row text | basis | status |',
             '|---|---:|---|---|---|---|---|']
    for e in ledger:
        text = (e['pems_text'] or '—').replace('|', '\\|')
        if len(text) > 150:
            text = text[:147] + '…'
        pems = f"p.{e['pems_page']}#{e['pems_ordinal']}" if e['pems_page'] else '—'
        f = e['file'].split('/')[-1]
        lines.append(f"| `{f}` | {e['row']} | {e['level_published']} | {pems} | {text} | "
                     f"{e['basis'] or '—'} | {e['status']} |")
    owner = [e for e in ledger if e['status'] == 'OWNER_REQUIRED']
    lines += ['', '## OWNER_REQUIRED', '',
              f'**{len(owner)} row(s).** No PEMS 2024 row authorises a provider level for these',
              'actions. The chip keeps the level the page already published and carries the flag.',
              'Nothing here was invented. Each entry records why it could not be cited.', '']
    if not owner:
        lines.append('None — no action row is left without a level decision.')
    for e in owner:
        lines.append(f"- `{e['file']}` row {e['row']} — **{e['level_published']}** kept from the "
                     f"page, not from the source. {e['action']}")
        if e['pems_page']:
            lines.append(f"  - nearest PEMS row, NOT cited as authority: "
                         f"p.{e['pems_page']}#{e['pems_ordinal']}")
        lines.append(f"  - reason: {e['reason']}")
    ruled = [e for e in ledger if e['status'] == 'owner_ruled']
    lines += ['', '## OWNER_RULED', '',
              'The owner decided these levels. They are **decisions, not source citations**:',
              'no PEMS 2024 row badges the action, the row is not PEMS-verified, and the',
              'PEMS row column above is empty on purpose.', '']
    if not ruled:
        lines.append('None — every action row is either PEMS-verified or OWNER_REQUIRED.')
    for e in ruled:
        r = e.get('owner_ruling') or {}
        lines.append(f"- `{e['file']}` row {e['row']} — **{e['level_published']}** — "
                     f"status `owner_ruled`. {r.get('note') or r.get('ruling')}")
    wording = load_wording_rulings()
    lines += ['', '## OWNER_RULED — wording (not level)', '',
              'Decisions the OWNER made about how a phrase reads. These are **rulings, not',
              'source readings**: the source prints something else, and the page is right by',
              'the ruling. A later pass must not "restore" the source wording.', '']
    if not wording:
        lines.append('None.')
    for rec in wording:
        lines.append(f"- `{rec['file']}` — source prints \"{rec.get('source_prints') or '—'}\"; "
                     f"the page reads **\"{rec['page_reads']}\"** ({rec.get('date')})")
        lines.append(f"  - ruling: {rec['ruling'].strip()}")

    sheet = load_stylesheet_changes()
    lines += ['', '## SHARED STYLESHEET CHANGES (not protocol content)', '',
              'Deliberate CSS changes made during conversion work. They affect **every** page',
              'that uses the `.lv-wrap` chassis, not only the batch that introduced them. They',
              'are styling fixes, not level decisions and not accidental diffs.', '']
    if not sheet:
        lines.append('None.')
    for rec in sheet:
        lines.append(f"- **{rec['date']}** — `" + '`, `'.join(rec['files']) + '`')
        for sel in rec.get('selectors') or []:
            lines.append(f"  - rule: `{sel}`")
        lines.append(f"  - affects: {rec['affects'].strip()}")
        lines.append(f"  - why: {rec['why'].strip()}")
        if rec.get('scope_note'):
            lines.append(f"  - scope: {rec['scope_note'].strip()}")

    pending = [e for e in ledger if e['status'] == 'pending_omd']
    pend_files = sorted({e['file'] for e in pending})
    lines += ['', '## PENDING_OMD — Pending OMD Authorization', '',
              f'**{len(pending)} row(s) across {len(pend_files)} page(s).** These protocols are',
              'not published in PEMS 2024, so no row on them can be cited to PEMS. Every row is',
              'chipped `PENDING`; `carried_from_page` records the level the agency page already',
              'published and is **provenance only, not a citation**. No PEMS page or row is',
              'named for any of these rows, and none may be added without a real regional',
              'source.', '']
    if not pending:
        lines.append('None — every converted page is sourced from PEMS 2024.')
    for rel in pend_files:
        rows = [e for e in pending if e['file'] == rel]
        lines.append(f'- `{rel}` — {len(rows)} row(s); source: '
                     f'**{rows[0].get("pending_source") or "—"}**')
        for e in rows:
            lines.append(f"  - row {e['row']}: PENDING (carried from the page as "
                         f"**{e['carried_from_page']}**) — {e['action'][:90]}")
    tokens = [(e['file'], e['row'], e['before']['text_tokens']) for e in ledger
              if e['before']['text_tokens']]
    lines += ['', '## Level tokens removed from action text', '']
    lines.append(f'{len(tokens)} row(s):')
    lines.append('')
    for f, row, toks in tokens:
        lines.append(f"- `{f.split('/')[-1]}` row {row}: removed {', '.join(toks)}")
    kept, removed = load_token_decisions()
    lines += ['', '## Level words kept in action text (deliberate)', '',
              'Provider-level words a sweep of the action text still finds. Each is a clinical',
              'qualifier, decided and recorded in `audit/level-scan/token-decisions.yaml`; a',
              'later pass must not strip them. The sweep (`audit/level-scan/token_sweep.py`)',
              'sees 0 such words on every Batch-2, neurologic and Aortic page.', '']
    if not kept:
        lines.append('None.')
    for (f, row), hits in sorted(kept.items()):
        lines.append(f"- `{f.split('/')[-1]}` row {row}: kept {', '.join(hits)}")
    if removed:
        lines.append('')
        lines.append('Removed by decision (not restated by the chip, so not left to a later '
                     'pass):')
        for rec in removed:
            lines.append(f"- `{rec['file'].split('/')[-1]}` row {rec['row']}: removed "
                         f"{rec['hit']}")
    changed = [e for e in ledger if e['status'] == 'OK' and e['before']['leftmost']
               and e['before']['leftmost'] != e['level_published']]
    lines += ['', '## Level moved by the source (page level -> PEMS printed level)', '',
              f'{len(changed)} row(s). These are rows where the page under- or over-granted the',
              'level the cited PEMS row prints. Review them first.', '']
    for e in changed:
        lines.append(f"- `{e['file']}` row {e['row']}: **{e['before']['leftmost']} -> "
                     f"{e['level_published']}** (p.{e['pems_page']}#{e['pems_ordinal']}) — "
                     f"{e['action'][:90]}")
    lines += ['', '## OPEN OWNER QUESTIONS', '',
              'Recorded, not fixed. Not verified against PEMS 2024; needs the owner\'s',
              'decision before the page is treated as final.', '',
              '- **Post-ROSC has no row for PEMS p.59#0** ("Follow Universal Patient Care…", badge',
              '  EMR) — missing row, not a level defect.',
              '- **p.61#4 and p.63#7 are compound rows** (one badge, plus an inline level token',
              '  scoping a clause). Every site row bound to them without a C2 `resolved_cells`',
              '  decision is flagged OWNER_REQUIRED rather than given a chip.',
              '- **Aortic Dissection & AAA (`04b`) has no PEMS 2024 protocol**: its source is',
              '  ODEMSA Section 2.5 (Revised 06/2015). It is converted to the 3-column chassis',
              '  with every row chipped `PENDING` (Pending OMD Authorization); see PENDING_OMD',
              '  above. The page must not be given a PEMS citation by any later pass.',
              '- **Aortic Dissection row 11 (Medical Control contact) is chipped `PENDING`, not',
              '  `MC`**, because this project\'s rule is one `PENDING` chip on every action row of',
              '  a page with no PEMS protocol. Owner ruling needed: is `PENDING` alone correct on',
              '  such a page, or should a Medical-Control row read `MC` + `PENDING` (both chips)?',
              '  Nothing on the page changes until the owner rules.',
              '- **`05_Stroke_TIA` row 9 is `OWNER_REQUIRED` with chip `A`** — the level the page',
              '  published before conversion. The EMR it had been given rested only on PEMS',
              '  p.131#2 by text resemblance, and that resemblance was withdrawn (the PEMS row',
              '  records a last-known-well time and a contact, not a pre-registration call).',
              '  Owner ruling needed: should the row read `EMR` *uncited* instead of `A`?']
    return '\n'.join(lines) + '\n'


def check():
    align, adjudicated = load_json('alignment.json'), load_json('adjudicated.json')
    pems = pems_index(load_json('pems_table.json'))
    rulings, bindings = load_rulings(), load_bindings()
    try:
        ledger_rows = load_json('level-rule-ledger.json')['rows']
    except FileNotFoundError:
        ledger_rows = []
    led = {(e['file'], str(e['row'])): e for e in ledger_rows}

    fails, report = [], []
    kept_words, removed_words = load_token_decisions()
    seen_kept = {}
    for rel in TARGETS:
        path = os.path.join(DOCS, rel)
        raw = open(path, encoding='utf-8').read()
        if NEW_HEADER not in raw:
            fails.append(f'{rel}: no collapsed level table ({NEW_HEADER!r} missing)')
        if re.search(r'^\|\s*#\s*\|\s*Action\s*/\s*Intervention\s*\|\s*EMR\s*\|', raw, re.M):
            fails.append(f'{rel}: legacy 5-column level matrix still present')
        if not find_regions(raw.split('\n')):
            fails.append(f'{rel}: no level-table region found')
        regions = find_regions(raw.split('\n'))
        if any(is_banner(r) for reg in regions for r in reg['rows']):
            fails.append(f'{rel}: section banner still encoded as a table row')
        rows = [r for reg in regions for r in reg['rows'] if not is_banner(r)]
        res = resolve(rel, rows, align, adjudicated, pems, bindings)
        owner_rows, ok_rows, ruled_rows = [], [], []
        for row, r in zip(rows, res):
            chips = CHIP_RE.findall(row['level_cell'] or '')
            if len(chips) != 1:
                fails.append(f'{rel} row {row["ordinal"]}: {len(chips)} level markers, expected 1')
                continue
            level = chips[0][1]
            if TEXT_TOKEN.search(row['action']):
                fails.append(f'{rel} row {row["ordinal"]}: level token left in the action text')
            hits = level_hits(row['action'])
            allowed = kept_words.get((rel, str(row['ordinal'])), [])
            for hit in hits:
                if hit not in allowed:
                    fails.append(f'{rel} row {row["ordinal"]}: level word {hit!r} left in the '
                                 f'action text with no keep decision in '
                                 f'audit/level-scan/token-decisions.yaml')
            for a in allowed:
                if a in hits:
                    seen_kept[(rel, str(row['ordinal']), a)] = True
                else:
                    fails.append(f'{rel} row {row["ordinal"]}: token-decisions.yaml keeps {a!r} '
                                 f'but the action text no longer contains it (stale decision)')
            ruled = rulings.get((rel, str(row['ordinal'])))
            if ruled:
                if level != ruled['level']:
                    fails.append(f'{rel} row {row["ordinal"]}: marker {level} != owner ruling '
                                 f'{ruled["level"]}')
                if 'lvl-own' in (row['level_cell'] or ''):
                    fails.append(f'{rel} row {row["ordinal"]}: owner-ruled row still carries '
                                 f'the OWNER_REQUIRED marker')
                if r['badge'] is not None:
                    fails.append(f'{rel} row {row["ordinal"]}: owner ruling recorded but PEMS '
                                 f'row {r["ptr"]} already badges it — ruling is stale')
                ruled_rows.append({'row': row['ordinal'], 'level': level, 'status': 'owner_ruled'})
                continue

            resolved_level = cells_level((r['resolved'] or {}).get('resolved_cells'))
            tokens = compound_tokens(r['pems_row'])
            must_own = bool(r['extra'].get('forced_owner')) or (
                resolved_level is None and (r['badge'] is None or bool(tokens)))
            has_flag = 'lvl-own' in (row['level_cell'] or '')
            if must_own:
                if not has_flag:
                    fails.append(f'{rel} row {row["ordinal"]}: no citable PEMS level but the chip '
                                 f'is not flagged OWNER_REQUIRED')
                e = led.get((rel, str(row['ordinal'])))
                if e is None:
                    fails.append(f'{rel} row {row["ordinal"]}: OWNER_REQUIRED row missing from '
                                 f'the ledger')
                else:
                    if e['status'] != 'OWNER_REQUIRED':
                        fails.append(f'{rel} row {row["ordinal"]}: ledger says {e["status"]}, '
                                     f'the page is flagged OWNER_REQUIRED')
                    if not e.get('reason'):
                        fails.append(f'{rel} row {row["ordinal"]}: OWNER_REQUIRED with no reason '
                                     f'in the ledger')
                    before = (e.get('before') or {}).get('leftmost')
                    if before and level != before:
                        fails.append(f'{rel} row {row["ordinal"]}: OWNER_REQUIRED chip {level} '
                                     f'!= the level the page published before conversion {before}')
                owner_rows.append({'row': row['ordinal'], 'level': level,
                                   'pems': (f"p.{r['ptr'][0]}#{r['ptr'][1]}" if r['ptr'] else None)})
                continue
            if has_flag:
                fails.append(f'{rel} row {row["ordinal"]}: chip carries the OWNER_REQUIRED flag '
                             f'but the row is cited to PEMS {r["ptr"]}')
            want = resolved_level or r['badge']
            if level != want:
                where = f' (p.{r["ptr"][0]}#{r["ptr"][1]})' if r['ptr'] else ''
                fails.append(f'{rel} row {row["ordinal"]}: marker {level} != expected {want}{where}')
            src = r['pems_row'] or {}
            cols = src.get('columns') or {}
            filled = [k for k in LV if cols.get(k)]
            mc_row = filled and all(cols[k] == 'MC' for k in filled)
            if filled and not mc_row and filled[0] != level and not resolved_level:
                fails.append(f'{rel} row {row["ordinal"]}: PEMS column dots start at '
                             f'{filled[0]}, badge says {level}')
            ok_rows.append({'row': row['ordinal'], 'level': level,
                            'pems': (f"p.{r['ptr'][0]}#{r['ptr'][1]}" if r['ptr'] else None),
                            'basis': r['basis']})
        report.append({'file': rel, 'rows': len(rows), 'verified': len(ok_rows),
                       'owner_required': owner_rows, 'owner_ruled': ruled_rows})

    # pages outside PEMS 2024: every row PENDING, and not one PEMS citation claimed
    pending_specs = load_pending()
    pending_report = []
    for rel in PENDING_TARGETS:
        path = os.path.join(DOCS, rel)
        if not os.path.exists(path):
            fails.append(f'{rel}: pending page listed but missing')
            continue
        spec = pending_specs.get(rel)
        if spec is None:
            fails.append(f'{rel}: pending page has no entry in pending-protocols.yaml')
            continue
        raw = open(path, encoding='utf-8').read()
        if NEW_HEADER not in raw:
            fails.append(f'{rel}: no collapsed level table ({NEW_HEADER!r} missing)')
        if re.search(r'^\|\s*#\s*\|\s*Action\s*/\s*Intervention\s*\|\s*EMR\s*\|', raw, re.M):
            fails.append(f'{rel}: legacy 5-column level matrix still present')
        if note_para(pending_note(spec)) not in raw:
            fails.append(f'{rel}: the Pending OMD Authorization note is not on the page')
        regions = find_regions(raw.split('\n'))
        if any(is_banner(r) for reg in regions for r in reg['rows']):
            fails.append(f'{rel}: section banner still encoded as a table row')
        rows = [r for reg in regions for r in reg['rows'] if not is_banner(r)]
        if not rows:
            fails.append(f'{rel}: no action rows found')
        pend_rows = []
        for row in rows:
            chips = CHIP_RE.findall(row['level_cell'] or '')
            if chips != [('pending', 'PENDING')]:
                fails.append(f'{rel} row {row["ordinal"]}: expected exactly one PENDING chip, '
                             f'found {chips or "none"}')
                continue
            if 'lvl-own' in (row['level_cell'] or '') or 'lvl-req' in (row['level_cell'] or ''):
                fails.append(f'{rel} row {row["ordinal"]}: PENDING chip carries a provenance '
                             f'marker (OWNER_REQUIRED / bracketed)')
            if TEXT_TOKEN.search(row['action']):
                fails.append(f'{rel} row {row["ordinal"]}: level token left in the action text')
            allowed = kept_words.get((rel, str(row['ordinal'])), [])
            pending_hits = level_hits(row['action'])
            for hit in pending_hits:
                if hit not in allowed:
                    fails.append(f'{rel} row {row["ordinal"]}: level word {hit!r} left in the '
                                 f'action text with no keep decision in '
                                 f'audit/level-scan/token-decisions.yaml')
            for a in allowed:
                if a in pending_hits:
                    seen_kept[(rel, str(row['ordinal']), a)] = True
                else:
                    fails.append(f'{rel} row {row["ordinal"]}: token-decisions.yaml keeps {a!r} '
                                 f'but the action text no longer contains it (stale decision)')
            if re.search(r'\bp\.\s?\d+', row['action']):
                fails.append(f'{rel} row {row["ordinal"]}: action text names a PEMS page — a '
                             f'pending row may not claim a PEMS citation')
            e = led.get((rel, str(row['ordinal'])))
            if e is None:
                fails.append(f'{rel} row {row["ordinal"]}: pending row missing from the ledger')
                continue
            if e['status'] != 'pending_omd':
                fails.append(f'{rel} row {row["ordinal"]}: ledger says {e["status"]}, the page '
                             f'is chipped PENDING')
            if e.get('pems_page') or e.get('pems_ordinal') or e.get('pems_badge'):
                fails.append(f'{rel} row {row["ordinal"]}: pending ledger row claims a PEMS '
                             f'citation (p.{e.get("pems_page")}#{e.get("pems_ordinal")}, '
                             f'badge {e.get("pems_badge")})')
            if not e.get('carried_from_page'):
                fails.append(f'{rel} row {row["ordinal"]}: ledger has no carried_from_page level')
            want = {int(k): str(v).upper()
                    for k, v in (spec['carried_levels'] or {}).items()}.get(int(row['ordinal']))
            if want is None:
                fails.append(f'{rel} row {row["ordinal"]}: no carried_levels entry in '
                             f'pending-protocols.yaml')
            elif e.get('carried_from_page') != want:
                fails.append(f'{rel} row {row["ordinal"]}: ledger carried_from_page '
                             f'{e.get("carried_from_page")} != pending-protocols.yaml {want}')
            pend_rows.append({'row': row['ordinal'], 'chip': 'PENDING',
                              'carried_from_page': e.get('carried_from_page')})
        pending_report.append({'file': rel, 'source': spec['source'], 'rows': len(rows),
                               'pending': pend_rows, 'pems_citations': 0})

    # owner rulings on wording: the page must actually read the ruled phrase
    for rec in load_wording_rulings():
        p = os.path.join(ROOT, rec['file'])
        if not os.path.exists(p):
            fails.append(f"wording ruling: {rec['file']} does not exist")
            continue
        body = open(p, encoding='utf-8').read()
        if rec['page_reads'] not in body:
            fails.append(f"wording ruling: {rec['file']} does not read "
                         f"\"{rec['page_reads']}\" (owner-ruled wording missing)")

    # the MC wording guard sweeps the whole docs tree, not just TARGETS
    mc = subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'mc_wording.py'),
                         '--check'], capture_output=True, text=True)
    if mc.returncode != 0:
        fails += ['mc_wording: ' + l.strip() for l in mc.stdout.splitlines() if l.strip()]

    # a keep decision may not point at a page or row that is not in scope
    for (f, row), words in kept_words.items():
        if f not in set(TARGETS + PENDING_TARGETS):
            fails.append(f'token-decisions.yaml: {f} is not a converted page')
            continue
        for w in words:
            if (f, row, w) not in seen_kept:
                fails.append(f'token-decisions.yaml: {f} row {row} keeps {w!r} but that text '
                             f'was not found in that row on the page')

    changed = [e for e in ledger_rows if e['status'] == 'OK' and e['before']['leftmost']
               and e['before']['leftmost'] != e['level_published']]
    text_tokens = [(e['file'], e['row'], e['before']['text_tokens'])
                   for e in ledger_rows if e['before']['text_tokens']]
    summary = {
        'pages': len(TARGETS),
        'rows_total': sum(r['rows'] for r in report),
        'rows_verified': sum(r['verified'] for r in report),
        'rows_owner_required': sum(len(r['owner_required']) for r in report),
        'rows_owner_ruled': sum(len(r['owner_ruled']) for r in report),
        'pending_pages': len(PENDING_TARGETS),
        'rows_pending_omd': sum(len(r['pending']) for r in pending_report),
        'pending': pending_report,
        'per_page': report,
        'level_moved_by_pems': [{'file': e['file'], 'row': e['row'],
                                 'page_level': e['before']['leftmost'],
                                 'pems_level': e['level_published'],
                                 'pems': f"p.{e['pems_page']}#{e['pems_ordinal']}"}
                                for e in changed],
        'tokens_stripped': text_tokens,
        'level_words_kept': [{'file': f, 'row': row, 'hit': hit}
                             for (f, row, hit) in sorted(seen_kept)],
        'level_words_removed': [{'file': r['file'], 'row': r['row'], 'hit': r['hit']}
                                for r in removed_words],
    }
    print(json.dumps(summary, indent=1))
    if fails:
        print('\nFAIL')
        for f in fails:
            print(' -', f)
        return 1
    print(f"\nOK — {summary['rows_total']} action rows across {summary['pages']} pages: "
          f"{summary['rows_verified']} carry exactly one marker equal to the level printed by the "
          f"cited PEMS 2024 row, {summary['rows_owner_required']} are flagged OWNER_REQUIRED with a "
          f"recorded reason, {summary['rows_owner_ruled']} are owner_ruled. "
          f"{len(seen_kept)} level word(s) survive in action text as recorded clinical "
          f"qualifiers (audit/level-scan/token-decisions.yaml); every other level token found by "
          f"an independent sweep of the action text is either kept there or gone.")
    print(f"OK — {summary['rows_pending_omd']} action rows across "
          f"{summary['pending_pages']} page(s) are chipped PENDING (Pending OMD Authorization) "
          f"because PEMS 2024 publishes no such protocol; 0 of them claim a PEMS citation.")
    return 0


# ------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--map', action='store_true')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    if args.check:
        return check()

    pending_specs = load_pending()
    for rel in PENDING_TARGETS:
        if rel not in pending_specs:
            raise SystemExit(f'{rel} is in PENDING_TARGETS but not in '
                             f'audit/level-scan/pending-protocols.yaml')

    all_ledger, bad = [], []
    for rel in TARGETS:
        _regions_out, ledger, problems, _lines, _regions = plan(rel)
        bad += problems
        all_ledger += ledger
        if args.map:
            print(f'== {rel}')
            for e in ledger:
                print(f'   {e["row"]:>3} {e["status"]:<14} level={str(e["level_published"]):<4} '
                      f'before_leftmost={str(e["before"]["leftmost"]):<4} '
                      f'text_label={str(e["before"]["text_label"]):<4} '
                      f'markers={len(e["before"]["markers"])} '
                      f'pems={e["pems_page"]}#{e["pems_ordinal"]} basis={e["basis"]}')
    for rel in PENDING_TARGETS:
        _regions_out, ledger, problems, _lines, _regions = plan_pending(rel, pending_specs[rel])
        bad += problems
        if args.map:
            print(f'== {rel}  (PENDING_OMD — no PEMS 2024 protocol)')
            for e in ledger:
                print(f'   {e["row"]:>3} {e["status"]:<14} level={e["level_published"]:<8} '
                      f'carried_from_page={str(e["carried_from_page"]):<4} '
                      f'pems=None basis=None')
    if args.report:
        for rel in PENDING_TARGETS:
            all_ledger += plan_pending(rel, pending_specs[rel])[1]
    if bad:
        print('PROBLEMS:')
        for p in bad:
            print(' -', p)
        return 2
    if args.map:
        return 0
    if args.write:
        for rel in TARGETS:
            splice(rel)
        for rel in PENDING_TARGETS:
            splice_pending(rel, pending_specs[rel])
            _r, ledger, _p, _l, _g = plan_pending(rel, pending_specs[rel])
            all_ledger += ledger
        out = os.path.join(AUD, 'level-rule-ledger.json')
        with open(out, 'w', encoding='utf-8') as fh:
            json.dump({'generated_by': 'scripts/level_rule.py',
                       'rule': 'one marker per action = the lowest provider level PEMS 2024 '
                               'prints for that action',
                       'targets': TARGETS,
                       'pending_targets': PENDING_TARGETS,
                       'rows': all_ledger}, fh, indent=1)
        print(f'wrote {os.path.relpath(out, ROOT)} ({len(all_ledger)} rows)')
        md = os.path.join(AUD, 'level-rule-ledger.md')
        with open(md, 'w', encoding='utf-8') as fh:
            fh.write(emit_md(all_ledger))
        print(f'wrote {os.path.relpath(md, ROOT)}')
        return 0
    if args.report:
        print(emit_md(all_ledger))
        return 0
    ap.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
