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
]

LV = ['EMR', 'EMT', 'A', 'I', 'P']
CHIP_CLASS = {'EMR': 'emr', 'EMT': 'emt', 'A': 'a', 'I': 'i', 'P': 'p', 'MC': 'mc'}
TEXT_TOKEN = re.compile(r'(?<![A-Za-z0-9])(EMR|EMT|A|I|P|MC)\s*:\s*')
SEPARATOR = re.compile(r'^\|[\s:|-]+\|$')
NEW_HEADER = '| # | Level | Action / Intervention |'
DIV_OPEN = '<div class="lv-wrap" markdown="1">'
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


# ----------------------------------------------------------------- level source
def load_json(name):
    with open(os.path.join(AUD, name), encoding='utf-8') as fh:
        return json.load(fh)


RULINGS_YAML = os.path.join(AUD, 'level-rulings.yaml')
BINDINGS_YAML = os.path.join(AUD, 'row-bindings.yaml')


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
    tokens = [(e['file'], e['row'], e['before']['text_tokens']) for e in ledger
              if e['before']['text_tokens']]
    lines += ['', '## Level tokens removed from action text', '']
    lines.append(f'{len(tokens)} row(s):')
    lines.append('')
    for f, row, toks in tokens:
        lines.append(f"- `{f.split('/')[-1]}` row {row}: removed {', '.join(toks)}")
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
              '- **Aortic Dissection & AAA (`04b`) is not converted**: its cited source is ODEMSA',
              '  Section 2.5 (Revised 06/2015), and PEMS 2024 prints no Aortic Dissection or AAA',
              '  protocol, so no row on that page can be cited.']
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

    # the MC wording guard sweeps the whole docs tree, not just TARGETS
    mc = subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'mc_wording.py'),
                         '--check'], capture_output=True, text=True)
    if mc.returncode != 0:
        fails += ['mc_wording: ' + l.strip() for l in mc.stdout.splitlines() if l.strip()]

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
        'per_page': report,
        'level_moved_by_pems': [{'file': e['file'], 'row': e['row'],
                                 'page_level': e['before']['leftmost'],
                                 'pems_level': e['level_published'],
                                 'pems': f"p.{e['pems_page']}#{e['pems_ordinal']}"}
                                for e in changed],
        'tokens_stripped': text_tokens,
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
          f"recorded reason, {summary['rows_owner_ruled']} are owner_ruled. No level token remains "
          f"in any action text.")
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
        out = os.path.join(AUD, 'level-rule-ledger.json')
        with open(out, 'w', encoding='utf-8') as fh:
            json.dump({'generated_by': 'scripts/level_rule.py',
                       'rule': 'one marker per action = the lowest provider level PEMS 2024 '
                               'prints for that action',
                       'targets': TARGETS, 'rows': all_ledger}, fh, indent=1)
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
