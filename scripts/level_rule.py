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
     (audit/level-scan/alignment.json -> adjudicated.json -> merged rows),
  2. takes that row's printed badge from audit/level-scan/pems_table.json,
  3. writes a single level chip, and strips level tokens out of the action text,
  4. refuses to invent a level: a row with no PEMS row keeps its current leftmost
     level and is flagged OWNER_REQUIRED in the ledger and on the page.

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

TARGETS = [
    'protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md',
    'protocols/cardiac/04_Post_Resuscitation_Care_PROC.md',
]

LV = ['EMR', 'EMT', 'A', 'I', 'P']
CHIP_CLASS = {'EMR': 'emr', 'EMT': 'emt', 'A': 'a', 'I': 'i', 'P': 'p', 'MC': 'mc'}
TEXT_TOKEN = re.compile(r'(?<![A-Za-z0-9])(EMR|EMT|A|I|P|MC)\s*:\s*')
SEPARATOR = re.compile(r'^\|[\s:|-]+\|$')
NEW_HEADER = '| # | Level | Action / Intervention |'
DIV_OPEN = '<div class="lv-wrap" markdown="1">'
CHIP_RE = re.compile(r'<span class="lvl lvl-([a-z]+)">([A-Z]+)</span>')


# --------------------------------------------------------------------- parsing
def split_cells(line):
    return [p.strip() for p in line.strip().strip('|').split('|')]


def parse_page(path):
    """Blocks of table rows. A block is {'banner': str|None, 'rows': [...]}."""
    blocks = [{'banner': None, 'rows': []}]
    in_tbl, new_format, seen_table = False, False, False
    for raw in open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        if not in_tbl:
            if line.startswith('| # |') and 'Level' in line:
                in_tbl, new_format, seen_table = True, True, True
                continue
            if line.startswith('| # |') and 'EMR' in line:
                in_tbl, new_format, seen_table = True, False, True
                continue
            if seen_table and re.match(r'^#{4,} ', line):
                # a pathway heading between two tables is this page's section banner
                blocks.append({'banner': line.lstrip('#').strip(), 'rows': []})
            continue
        if SEPARATOR.match(line):
            continue
        if not line.strip().startswith('|'):
            in_tbl = False
            continue
        cells = split_cells(line)
        if new_format:
            if len(cells) < 3:
                continue
            blocks[-1]['rows'].append({'ordinal': cells[0], 'action': cells[2],
                                       'level_cell': cells[1], 'cells': None})
        else:
            if len(cells) < 7:
                continue
            row = {'ordinal': cells[0], 'action': cells[1], 'cells': cells[2:7],
                   'level_cell': None}
            if is_banner(row):
                # a full-width banner opens its own block; it is not an action row
                blocks.append({'banner': row['action'], 'rows': []})
            else:
                blocks[-1]['rows'].append(row)
    return [b for b in blocks if b['banner'] or b['rows']]


def is_banner(row):
    if row['cells'] is None:
        return False
    text = row['action'].strip()
    return text.startswith('**') and text.endswith('**') and not any(c.strip() for c in row['cells'])


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
    inside the sentence ("...after two attempts, MC: Contact Poquoson OMD") loses its
    colon and the capital that followed it, so the sentence still reads as one sentence.
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


def significant(text):
    return {w for w in re.findall(r'[a-z]{3,}', text.lower())}


def resolve(rel, rows, align, adjudicated, pems):
    """Per-row PEMS citation, derived — nothing hand-written."""
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

        source_row = pems.get(ptr) if ptr else None
        badge, bracketed = badge_of(source_row) if source_row else (None, False)
        out.append({'ordinal': ordinal, 'ptr': ptr, 'basis': basis, 'badge': badge,
                    'bracketed': bracketed, 'pems_row': source_row, 'extra': extra,
                    'adjudicated': rec})
    return out


# ------------------------------------------------------------------- rendering
def chip(level, bracketed=False, owner=False):
    html = f'<span class="lvl lvl-{CHIP_CLASS.get(level, "na")}">{level}</span>'
    if bracketed:
        html += ('<sup class="lvl-req" title="PEMS 2024 prints this badge in brackets: agency '
                 'training documentation and OMD written authorization required">*</sup>')
    if owner:
        html += ('<sup class="lvl-own" title="OWNER_REQUIRED: no PEMS 2024 row authorises this '
                 'action\'s provider level">&#9873;</sup>')
    return html


def render_block(rows, note=None):
    out = [DIV_OPEN, '', NEW_HEADER, '|:---:|---|---|']
    for r in rows:
        out.append(f"| {r['ordinal']} | {r['level_cell']} | {r['action']} |")
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


# ------------------------------------------------------------------- the build
def plan(rel):
    """Return (blocks_out, ledger, problems) for one page, without writing."""
    path = os.path.join(DOCS, rel)
    align, adjudicated, table = load_json('alignment.json'), load_json('adjudicated.json'), load_json('pems_table.json')
    pems = pems_index(table)
    blocks = parse_page(path)
    actions = [r for b in blocks for r in b['rows'] if not is_banner(r)]
    res = resolve(rel, actions, align, adjudicated, pems)

    ledger, problems = [], []
    blocks_out, cursor = [], 0
    for block in blocks:
        new_rows = []
        for row in block['rows']:
            r = res[cursor]
            cursor += 1
            existing = CHIP_RE.search(row['level_cell'] or '')
            before_low = (leftmost_level(row['cells']) if row['cells'] is not None
                          else (existing.group(2) if existing else None))
            marked = marked_levels(row['cells'])
            label = text_label(row['action'])
            new_text, stripped = strip_tokens(row['action'])

            owner = r['badge'] is None
            if r['adjudicated'] and r['adjudicated'].get('decision') == 'UNRESOLVED':
                owner = True
            level = r['badge'] if r['badge'] else before_low
            if level is None:
                problems.append(f'{rel} row {row["ordinal"]}: no PEMS level and no existing '
                                'marker — cannot place a marker')
            new_rows.append({'ordinal': row['ordinal'], 'action': new_text,
                             'level_cell': chip(level, r['bracketed'], owner)})
            ledger.append({
                'file': rel,
                'row': int(row['ordinal']),
                'action': re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', new_text).replace('**', '').replace('<br>', ' ')[:150],
                'level_published': level,
                'status': 'OWNER_REQUIRED' if owner else 'OK',
                'pems_page': r['ptr'][0] if r['ptr'] else None,
                'pems_ordinal': r['ptr'][1] if r['ptr'] else None,
                'pems_badge': r['badge'],
                'bracketed': r['bracketed'],
                'pems_text': (r['pems_row'] or {}).get('verbatim_text'),
                'basis': r['basis'],
                'before': {
                    'leftmost': before_low,
                    'markers': marked,
                    'text_label': label,
                    'text_tokens': stripped,
                },
                'note': r['extra'].get('adjudication'),
            })
        if block['banner']:
            blocks_out.append({'heading': heading_for(block['banner']), 'rows': new_rows})
        else:
            blocks_out.append({'heading': None, 'rows': new_rows})
    return blocks_out, ledger, problems


def splice(path, blocks_out, ledger):
    """Replace the intervention table region of the page, keeping everything else.

    The region runs from the first table wrapper to the next section heading (### Pearls
    and friends), so it works on the legacy sc-wrap page and on its own output alike —
    re-running --write is a no-op.
    """
    with open(path, encoding='utf-8') as fh:
        lines = fh.read().split('\n')
    open_i = next(i for i, l in enumerate(lines)
                  if l.startswith('<div class="sc-wrap') or l.startswith('<div class="lv-wrap'))
    close_i = next(i for i in range(open_i + 1, len(lines)) if re.match(r'^#{1,3} ', lines[i]))

    notes = []
    owner_rows = [str(e['row']) for e in ledger if e['status'] == 'OWNER_REQUIRED']
    if owner_rows:
        label = 'row ' + owner_rows[0] if len(owner_rows) == 1 else 'rows ' + ', '.join(owner_rows)
        notes.append('&#9873; **OWNER_REQUIRED** — ' + label +
                     ': no PEMS 2024 row authorises a provider level for this action. The level '
                     'shown is the one this page already published; it is not verified against '
                     'the source.')
    if any(e['bracketed'] for e in ledger):
        notes.append('* **[ ] badge in PEMS 2024** — the source prints this level in brackets: '
                     'agency post-affiliation training documentation on file, plus the '
                     "OMD's written authorization for that skill. The bracketing is the source's, "
                     'not this page\'s.')
    page_note = '\n\n'.join(notes) if notes else None

    pieces = []
    for bi, block in enumerate(blocks_out):
        if block['heading']:
            pieces += [block['heading'], '']
        note = page_note if bi == len(blocks_out) - 1 else None
        pieces += render_block(block['rows'], note)
        if bi < len(blocks_out) - 1:
            pieces.append('')
    pieces.append('')
    new = lines[:open_i] + pieces + lines[close_i:]
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(new))


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
    for rel in TARGETS:
        text = git_show(base, rel)
        if text is None:
            continue
        path = os.path.join(AUD, '..', '..', 'docs', rel)
        tmp = os.path.join(ROOT, '.level-rule-base.tmp')
        with open(tmp, 'w', encoding='utf-8') as fh:
            fh.write(text)
        blocks = parse_page(tmp)
        os.unlink(tmp)
        rows = [r for b in blocks for r in b['rows'] if not is_banner(r)]
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
             '`basis` says how the PEMS row was bound: `alignment:matched` (section+ordinal in',
             '`alignment.json`), `adjudicated:*` (a ruling in `adjudicated.json`),',
             '`alignment:merged_into_site_row` (PEMS merges what the page splits).', '',
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
    lines += ['', '## OWNER_REQUIRED', '']
    if not owner:
        lines.append('None — every action row is authorised by a PEMS 2024 row.')
    for e in owner:
        lines.append(f"- `{e['file']}` row {e['row']} — **{e['level_published']}** kept from the "
                     f"page, not from the source: {e['action']}")
    tokens = [(e['file'], e['row'], e['before']['text_tokens']) for e in ledger
              if e['before']['text_tokens']]
    lines += ['', '## Level tokens removed from action text', '']
    lines.append(f'{len(tokens)} row(s):')
    lines.append('')
    for f, row, toks in tokens:
        lines.append(f"- `{f.split('/')[-1]}` row {row}: removed {', '.join(toks)}")
    return '\n'.join(lines) + '\n'


def check():
    align, adjudicated, table = load_json('alignment.json'), load_json('adjudicated.json'), load_json('pems_table.json')
    pems = pems_index(table)
    fails, report = [], []
    for rel in TARGETS:
        path = os.path.join(DOCS, rel)
        raw = open(path, encoding='utf-8').read()
        if NEW_HEADER not in raw:
            fails.append(f'{rel}: no collapsed level table ({NEW_HEADER!r} missing)')
        if re.search(r'^\|\s*#\s*\|\s*Action\s*/\s*Intervention\s*\|\s*EMR\s*\|', raw, re.M):
            fails.append(f'{rel}: legacy 5-column level matrix still present')
        blocks = parse_page(path)
        rows = [r for b in blocks for r in b['rows']]
        if any(is_banner(r) for r in rows if r['cells'] is not None):
            fails.append(f'{rel}: section banner still encoded as a table row')
        # rebuild the citation map from the same derive path to confirm each chip
        res = resolve(rel, rows, align, adjudicated, pems)
        owner_rows, ok_rows = [], []
        for row, r in zip(rows, res):
            chips = CHIP_RE.findall(row['level_cell'])
            if len(chips) != 1:
                fails.append(f'{rel} row {row["ordinal"]}: {len(chips)} level markers, expected 1')
                continue
            level = chips[0][1]
            if TEXT_TOKEN.search(row['action']):
                fails.append(f'{rel} row {row["ordinal"]}: level token left in the action text')
            if r['badge'] is None:
                owner_rows.append((row['ordinal'], level))
                continue
            if level != r['badge']:
                fails.append(f'{rel} row {row["ordinal"]}: marker {level} != PEMS badge {r["badge"]} '
                             f'(p.{r["ptr"][0]}#{r["ptr"][1]})')
            # independent confirmation: the printed columns must start at that level
            src = r['pems_row']
            cols = src.get('columns') or {}
            filled = [k for k in LV if cols.get(k)]
            mc_row = filled and all(cols[k] == 'MC' for k in filled)
            if filled and not mc_row and filled[0] != level:
                    fails.append(f'{rel} row {row["ordinal"]}: PEMS column dots start at '
                                 f'{filled[0]}, badge says {level}')
            ok_rows.append((row['ordinal'], level))
        report.append({'file': rel, 'rows': len(rows), 'verified': len(ok_rows),
                       'owner_required': owner_rows})

    # what the collapse actually changed, counted from the ledger (never hand-counted)
    try:
        ledger = load_json('level-rule-ledger.json')['rows']
    except FileNotFoundError:
        ledger = []
    changed = [e for e in ledger if e['before']['leftmost'] != e['level_published']]
    text_tokens = [(e['file'], e['row'], e['before']['text_tokens'])
                   for e in ledger if e['before']['text_tokens']]
    base, per_file, totals = defect_counts()
    print(json.dumps({'base': base, 'per_file': report,
                      'raised_by_pems': [{'file': e['file'], 'row': e['row'],
                                          'page_level': e['before']['leftmost'],
                                          'pems_level': e['level_published'],
                                          'pems': f"p.{e['pems_page']}#{e['pems_ordinal']}"}
                                         for e in changed],
                      'tokens_stripped': text_tokens,
                      'defects_on_base': per_file,
                      'defect_totals_on_base': totals}, indent=1))
    if fails:
        print('\nFAIL')
        for f in fails:
            print(' -', f)
        return 1
    print('\nOK — every action row in both protocols has exactly one marker, no level token '
          'in its text, and a marker equal to the level printed by the cited PEMS row.')
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
        blocks_out, ledger, problems = plan(rel)
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
        if args.write:
            splice(os.path.join(DOCS, rel), blocks_out, ledger)
    if bad:
        print('PROBLEMS:')
        for p in bad:
            print(' -', p)
        return 2
    if args.map:
        return 0
    if args.write:
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
