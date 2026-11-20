#!/usr/bin/env python3
"""Build `docs/protocols/outstanding-decisions.md` — the owner-facing, phone-first
list of every decision the level-rule conversion still needs.

READ-ONLY OVER THE LEDGER. Every row, reason, level and page note on the output
page is copied from `audit/level-scan/level-rule-ledger.json` (rows) and
`audit/level-scan/level-rule-ledger.md` (open questions) — nothing on the page is
typed by hand. Totals are derived from the lists and asserted against the
ledger's own stated totals, so a hand-typed count cannot drift in.

Usage:
    python3 scripts/build_outstanding_decisions.py           # write the page
    python3 scripts/build_outstanding_decisions.py --print   # dump to stdout
    python3 scripts/build_outstanding_decisions.py --check   # exit 1 if stale
"""
from __future__ import annotations

import argparse
import html
import json
import os
import posixpath
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER_JSON = os.path.join(ROOT, 'audit', 'level-scan', 'level-rule-ledger.json')
LEDGER_MD = os.path.join(ROOT, 'audit', 'level-scan', 'level-rule-ledger.md')
MKDOCS_YML = os.path.join(ROOT, 'mkdocs.yml')
DOCS = os.path.join(ROOT, 'docs')
OUT_REL = 'protocols/outstanding-decisions.md'
OUT = os.path.join(DOCS, OUT_REL)

NAV_LINE = re.compile(r'^\s*- (.+?): (\S+\.md)\s*$')
# a reason says "PEMS prints it, but the printed badge conflicts with the row's words"
# when it names rows whose levels cannot be reconciled into one chip.
CONFLICT = re.compile(r'contradict|conflict|two levels|three levels|multiple levels|'
                      r'single badge|one chip cannot|two rows|three rows|at one level',
                      re.I)
FLAG = '&#9873;'          # ⚑ OWNER_REQUIRED marker used on the protocol pages


def read_nav():
    """{docs-relative path: human nav label} from mkdocs.yml, plus nav order."""
    labels, order = {}, {}
    with open(MKDOCS_YML, encoding='utf-8') as fh:
        for line in fh:
            m = NAV_LINE.match(line.rstrip('\n'))
            if not m:
                continue
            label, path = m.group(1), m.group(2)
            if path in labels:      # last nav occurrence wins, as mkdocs does
                continue
            order[path] = len(order)
            labels[path] = label
    return labels, order


def esc(text):
    return html.escape(text or '', quote=True)


def link_to(doc_rel, name, cls='od-page'):
    """Relative .md link target from this page, percent-encoded like the rest of the
    site. Emitted as a MARKDOWN link by `page_heading()` so mkdocs rewrites it to the
    built .html and `--strict` fails if the target does not exist."""
    target = urllib.parse.quote(posixpath.relpath(doc_rel, 'protocols'), safe='/-_.~')
    return target


def page_heading(doc_rel, label, count):
    rows = 'row' if count == 1 else 'rows'
    return f'#### [{label}]({link_to(doc_rel, label)}) — {count} {rows}'


def load_ledger():
    with open(LEDGER_JSON, encoding='utf-8') as fh:
        return json.load(fh)


def ledger_md_text():
    with open(LEDGER_MD, encoding='utf-8') as fh:
        return fh.read()


def stated_total(md, header):
    """The row count the ledger itself states at the top of a section."""
    start = md.index(header)
    chunk = md[start:start + 4000]
    m = re.search(r'\*\*(\d+) row\(s\)', chunk)
    if not m:
        raise SystemExit(f'no stated row total after header {header!r}')
    return int(m.group(1))


def page_note(doc_rel, want):
    """The verbatim `<p class="lv-note">` block a reader sees on that page."""
    path = os.path.join(DOCS, doc_rel)
    if not os.path.exists(path):
        return None
    body = open(path, encoding='utf-8').read()
    notes = [n for n in re.findall(r'<p class="lv-note">(.*?)</p>', body, re.S)
             if want.lower() in n.lower()]
    if not notes:
        return None
    text = ' '.join(notes)
    text = re.sub(r'<[^>]+>', '', text)          # tags out, words kept verbatim
    return re.sub(r'\s+', ' ', text).strip()


ROW_LINE = re.compile(r'^\|\s*(\d+)\s*\|\s*(<span[^>]*>.*?</span>(?:<sup.*?</sup>)?)\s*\|(.*)\|\s*$')


def clean_cell(text):
    """The action cell as the reader sees it: markup off, words and line breaks kept."""
    text = re.sub(r'<br\s*/?>', ' / ', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<sup[^>]*>.*?</sup>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    text = text.replace('**', '').replace('`', '')
    return re.sub(r'\s+', ' ', text).strip()


def page_actions(rows):
    """{file: {row: action text}} read off each protocol page's own table.

    The ledger's `action` field is cut at 150 characters; the row text the owner
    must read is not. Taken from the page the row lives on, so the card quotes
    what is actually published."""
    cache, out = {}, {}
    wanted = {}
    for row in rows:
        wanted.setdefault(row['file'], set()).add(int(row['row']))
    for rel, nums in wanted.items():
        path = os.path.join(DOCS, rel)
        if rel not in cache:
            cache[rel] = open(path, encoding='utf-8').read().split('\n') if os.path.exists(path) else []
        found = {}
        for line in cache[rel]:
            m = ROW_LINE.match(line.rstrip())
            if m:
                found[int(m.group(1))] = clean_cell(m.group(3))
        missing = nums - set(found)
        if missing:
            raise SystemExit(f'{rel}: no table row for row(s) {sorted(missing)}')
        out[rel] = found
    return out


def nearest_pems(md):
    """{(file, row): 'p.63#7'} from the ledger's OWNER_REQUIRED bullets — the JSON
    ledger does not carry the nearest-row field."""
    start = md.index('## OWNER_REQUIRED')
    end = md.index('## OWNER_RULED')
    out, cur = {}, None
    head = re.compile(r"^- `([^`]+)` row (\d+) —")
    near = re.compile(r'nearest PEMS row, NOT cited as authority:\s*(.+?)\s*$')
    for line in md[start:end].split('\n'):
        m = head.match(line)
        if m:
            cur = (m.group(1), int(m.group(2)))
            continue
        m = near.search(line)
        if m and cur:
            out[cur] = m.group(1)
    return out


def note_for_row(note, n):
    """The slice of the page note that speaks about row `n`, when the note is
    written per row (`PENDING — row 6: ...`); the whole note otherwise."""
    if not note:
        return note
    parts = re.split(r'(?=PENDING — rows? [\d,\s-]*\d)', note)
    for part in parts:
        m = re.match(r'PENDING — rows? ([\d,\s-]+?):', part)
        if not m:
            continue
        nums = set()
        for chunk in m.group(1).split(','):
            chunk = chunk.strip()
            if '-' in chunk:
                a, b = chunk.split('-')
                nums.update(range(int(a), int(b) + 1))
            elif chunk.isdigit():
                nums.add(int(chunk))
        if n in nums:
            return part.strip()
    return note


def group_by_page(rows, labels, order):
    pages = {}
    for row in rows:
        pages.setdefault(row['file'], []).append(row)
    def key(item):
        return (order.get(item[0], 10 ** 6), item[0])
    return sorted(pages.items(), key=key)


def human(rel, labels):
    return labels.get(rel) or posixpath.basename(rel).replace('_PROC.md', '') \
        .replace('.md', '').replace('_', ' ')


def owner_required_card(row, action, near_cite):
    near = ''
    if near_cite:
        near = (f'<p class="od-near">Nearest PEMS row: <strong>{esc(near_cite)}</strong> '
                f'&mdash; <em>not cited as authority</em></p>')
    lvl = row['level_published']
    cls = lvl.lower().replace('+mc', '')
    return f'''<div class="od-card od-cat-{row['cat']}">
<p class="od-head"><span class="od-row">Row {row["row"]}</span> <span class="lvl lvl-{esc(cls)}">{esc(lvl)}</span> {FLAG}</p>
<p class="od-action">{esc(action)}</p>
<p class="od-reason"><strong>Why it is flagged:</strong> {esc(row['reason'])}</p>
{near}
</div>'''


def pending_card(row, action, carried, note=None):
    why = row['reason'] or row.get('note') or ''
    note_html = ''
    if note:
        note_html = (f'<p class="od-pagenote"><strong>Note on the page:</strong> '
                     f'{esc(note)}</p>')
    return f'''<div class="od-card od-cat-pending">
<p class="od-head"><span class="od-row">Row {row["row"]}</span> <span class="lvl lvl-pending">PENDING</span></p>
<p class="od-action">{esc(action)}</p>
<p class="od-reason"><strong>Why:</strong> {esc(why)}</p>
{note_html}
<p class="od-near">Was carried from the page as <strong>{esc(carried)}</strong> &mdash; provenance only, not a citation.</p>
</div>'''


def carried_level(row):
    return row.get('carried_from_page') or (row.get('before') or {}).get('leftmost') or 'NONE'


RULED_HEADER = '## OWNER_RULED — Cold Exposure pilot'


def section_entries(md, header):
    """Every `- ` entry of one ledger section, verbatim (head + continuation lines)."""
    lines = md.split('\n')
    start = next((i for i, l in enumerate(lines) if l.startswith(header)), None)
    if start is None:
        raise SystemExit(f'ledger markdown has no section starting {header!r}')
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith('## ')),
               len(lines))
    entries = []
    for line in lines[start + 1:end]:
        if line.startswith('- '):
            entries.append([line[2:]])
        elif line.startswith('  ') and entries and line.strip():
            entries[-1].append(line.strip())
    out = []
    for chunk in entries:
        head = chunk[0]
        bold = re.search(r'\*\*(.+?)\*\*', head)
        lead = bold.group(1) if bold else head
        batch = re.search(r'\bBatch (\d+)\b', head)
        out.append({
            'raw': ' '.join(chunk),
            'lead': lead,
            'text': ' '.join(chunk),
            'batch': f'Batch {batch.group(1)}' if batch else 'No batch recorded',
        })
    return out


def open_questions(md):
    """Every entry of the ledger's OPEN OWNER QUESTIONS section, verbatim."""
    return section_entries(md, '## OPEN OWNER QUESTIONS')


def ruled_entries(md):
    """Every entry of the ledger's OWNER_RULED section for the Cold pilot, verbatim.

    These are RECORDED DECISIONS (the owner answered on 2026-11-20), so they are published
    under their own heading and never counted as open questions.
    """
    return section_entries(md, RULED_HEADER)


def inline_md(text):
    """The ledger's own inline markdown, escaped first so no tag can slip through."""
    t = esc(text)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t, flags=re.S)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t


def topic_buckets(entries, labels):
    """Group each open question by the batch that recorded it.

    The ledger records no topic field for these entries, and these questions cross
    pages ("a row that bundles two PEMS levels"), so guessing a page from prose
    mislabels them. The batch IS the topic of work; every card still leads with the
    ledger's own bold heading, which names the subject."""
    buckets = {}
    for entry in entries:
        buckets.setdefault(entry['batch'], []).append(entry)

    def key(batch):
        m = re.search(r'(\d+)', batch)
        return (0 if not m else 1, int(m.group(1)) if m else 0)

    return {b: buckets[b] for b in sorted(buckets, key=key)}


def build():
    labels, order = read_nav()
    ledger = load_ledger()
    md = ledger_md_text()
    rows = ledger['rows']

    owner = [dict(r, cat=('conflict' if CONFLICT.search(r.get('reason') or '') else 'nowhere'))
             for r in rows if r['status'] == 'OWNER_REQUIRED']
    pend_page = [r for r in rows if r['status'] == 'pending_omd']
    pend_row = [r for r in rows if r['status'] == 'pending_row_omd']
    actions = page_actions(owner + pend_page + pend_row)
    nearest = nearest_pems(md)
    questions = open_questions(md)
    ruled = ruled_entries(md)
    buckets = topic_buckets(questions, labels)
    # ---- The 2026-11-20 owner ruling is a DECISION, not a question. It is published under
    # ---- its own heading and must never drift back into the open list the page asks the
    # ---- owner to answer: this page is titled "decisions still waiting on you".
    assert ruled, 'the ledger records no Cold Exposure ruling — nothing to publish as decided'
    assert any('ASKED and ANSWERED' in r['text'] for r in ruled), \
        'the Cold Exposure row 6 ASKED/ANSWERED ruling is missing from the OWNER_RULED section'
    assert not any('ASKED and ANSWERED' in q['text'] for q in questions), \
        'the Cold Exposure row 6 ruling is still published as an OPEN question'
    assert not any('Cold Exposure rows 6 and 9' in q['text'] for q in questions), \
        'the Cold Exposure relocation is still published as an OPEN question'

    # ---- counts are derived from the lists, then asserted against the ledger's
    # ---- own stated totals. A disagreement is a hard failure, never a warning.
    t_owner = stated_total(md, '## OWNER_REQUIRED')
    t_pend_page = stated_total(md, '## PENDING_OMD — Pending OMD Authorization')
    t_pend_row = stated_total(md, '## PENDING_OMD — row-level')
    assert len(owner) == t_owner, (len(owner), t_owner)
    assert len(pend_page) == t_pend_page, (len(pend_page), t_pend_page)
    assert len(pend_row) == t_pend_row, (len(pend_row), t_pend_row)
    n_nowhere = sum(1 for r in owner if r['cat'] == 'nowhere')
    n_conflict = sum(1 for r in owner if r['cat'] == 'conflict')
    assert n_nowhere + n_conflict == len(owner)
    # ---- The "PEMS prints this nowhere" bucket, asserted by MEMBERSHIP, not by count ----
    # ---- The owner's Pearl ruling of 2026-11-17 (BLS/ALS scope test) cleared every flag whose
    # reason claimed the source is silent, EXCEPT four rows the source genuinely does not
    # print. The 2026-11-20 ketamine ruling then removed the two Sedation rows that card had
    # put out of scope (pre-intubation sedation r4, post-intubation ketamine r5): both rows
    # left the page, so neither is a question any more. The bucket now holds four rows: three
    # genuinely absent, plus Trauma r6, whose "prints nowhere" reason is only half true (p.84
    # PEARLS #3 prints the recognition half) and whose level question therefore stays open.
    # A quiet re-categorisation of any row must fail the build rather than move the number the
    # owner reads on the page.
    nowhere_expected = {
        ('protocols/respiratory/03_Pediatric_Stridor_PROC.md', 2),      # genuinely absent
        ('protocols/respiratory/03_Pneumothorax_PROC.md', 5),           # genuinely absent
        ('protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md', 2),  # genuinely absent
        ('protocols/trauma/09_Trauma_PROC.md', 6),                      # out of scope (this card)
    }
    nowhere_got = {(r['file'], int(r['row'])) for r in owner if r['cat'] == 'nowhere'}
    assert nowhere_got == nowhere_expected, (
        'the "PEMS prints this nowhere" bucket changed membership:\n'
        f'  unexpected: {sorted(nowhere_got - nowhere_expected)}\n'
        f'  missing:    {sorted(nowhere_expected - nowhere_got)}')
    assert n_nowhere == len(nowhere_expected)
    print(f'the "PEMS prints this nowhere" bucket is {n_nowhere} rows (was 17 before the '
          f'2026-11-17 Pearl ruling, 6 after it, 4 after the 2026-11-20 ketamine ruling '
          f'removed the two Sedation rows it had left out of scope): 3 genuinely absent from '
          f'the source, plus Trauma r6 whose level question stays open — membership asserted, '
          f'not typed', file=sys.stderr)

    o = []
    w = o.append
    w('---')
    w('title: Outstanding Decisions')
    w('description: Every protocol row and open question still waiting on the owner.')
    w('search:')
    w('  boost: 4')
    w('---')
    w('')
    w('# Outstanding Decisions')
    w('')
    w('<div class="od-intro" markdown="1">')
    w('Every row below is a decision **still waiting on you** — except the last section, '
      'which records rulings you have already made. Nothing here changes a '
      'protocol: the pages keep working exactly as they do today, and answering is '
      'optional row by row.')
    w('')
    w('This page is generated from the conversion ledger '
      '(`audit/level-scan/level-rule-ledger.json`) — the reasons are copied verbatim, '
      'and the counts are computed from the lists, not typed in.')
    w('')
    w(f'| what | how many |')
    w('|---|---:|')
    w(f'| Rows that need your level decision (`OWNER_REQUIRED`, marked {FLAG} on the page) '
      f'| **{len(owner)}** |')
    w(f'| Rows pending authorization (`PENDING`) | **{len(pend_page) + len(pend_row)}** '
      f'({len(pend_page)} whole-page + {len(pend_row)} single-row) |')
    w(f'| Open questions on how the rules themselves should read | **{len(questions)}** |')
    w(f'| Rulings already recorded — decided, no action needed | **{len(ruled)}** |')
    w('')
    w('</div>')
    w('')
    # ---------------------------------------------------------------- preamble
    w('<h2 id="what-each-decision-means">What each decision means</h2>')
    w('')
    w('<div class="od-preamble" markdown="1">')
    w(f'- **&#9873; `OWNER_REQUIRED`** — the protocol shows a provider level, but no '
      'PEMS 2024 row authorises that level for that action. The level you see is '
      '**kept from the page as it was published, not taken from the source**. It is '
      'marked so nobody mistakes it for a verified regional citation. Your answer '
      'decides which level the row should carry.')
    w('- **`PENDING`** — no provider level is published at all yet. Either the whole '
      'protocol is not in PEMS 2024 (Aortic Dissection & AAA comes from ODEMSA), or '
      'the agency added the row and PEMS prints no such action. The row stays '
      '`PENDING` until the operational medical director authorises a level.')
    w('- **`POLICY`** — the row is an administrative rule that PEMS prints as policy '
      'prose, not as a level-badged protocol row. Policy rows publish no provider '
      'level, so there is nothing here for you to level.')
    w('- **`+MC`** — the original page printed that level in brackets (`[A]`), meaning '
      '"at this level only with Medical Control". The chip carries the level and a '
      'second marker carries the bracket, so the notation survives.')
    w('- **`*` (asterisk)** — PEMS itself brackets that badge (`[A]` in the regional '
      'table). The asterisk means the bracket comes from the source, not from our '
      'page.')
    w('- **Why the level is "kept from the page, not the source"** — the site pages '
      'predate the conversion. Where the source does not settle a level, the '
      'conversion refuses to invent one: it keeps what the page already published '
      'and raises a flag so the uncertainty is visible instead of being silently '
      'wiped out.')
    w('')
    w('</div>')
    w('')
    # ------------------------------------------------------------------ legend
    w('<h2 id="two-kinds">Two kinds of flagged row</h2>')
    w('')
    w('<div class="od-legend" markdown="1">')
    w(f'- <span class="od-chip od-chip-nowhere">PEMS prints this nowhere</span> — '
      f'**{n_nowhere} rows**. No PEMS 2024 row prints the action at all (or prints it '
      'only in pieces that no single row covers). Your answer is a level of our own, '
      'or `PENDING`.')
    w(f'- <span class="od-chip od-chip-conflict">PEMS prints it, but the badge contradicts '
      f'the row\'s own words</span> — **{n_conflict} rows**. A PEMS row prints the '
      'action, but its printed badge conflicts with the text of that same row, or the '
      'action is spread over rows at different levels. Your answer is which one wins '
      '(and whether the row should be split).')
    w('')
    w(f'Jump to: [PEMS prints this nowhere](#pems-prints-this-nowhere) · '
      f'[PEMS prints it, badge contradicts](#pems-prints-it-badge-contradicts)')
    w('')
    w('</div>')
    w('')
    # ------------------------------------------------------- 1. OWNER_REQUIRED
    w(f'<h2 id="owner-required">1. Needs your level decision — {len(owner)} rows</h2>')
    w('')
    w(f'Grouped by protocol page, in the order they appear in the site navigation. '
      f'Each card shows the page, the row number, the level the page shows today with '
      f'the {FLAG} flag, the row text word for word, and the full reason it is flagged.')
    w('')
    for cat, title, anchor in (
            ('nowhere', 'PEMS prints this nowhere', 'pems-prints-this-nowhere'),
            ('conflict', 'PEMS prints it, but the badge contradicts the row\'s words',
             'pems-prints-it-badge-contradicts')):
        group = [r for r in owner if r['cat'] == cat]
        w(f'<h3 id="{anchor}">{esc(title)} — {len(group)} rows</h3>')
        w('')
        for rel, page_rows in group_by_page(group, labels, order):
            w(page_heading(rel, human(rel, labels), len(page_rows)))
            w('')
            w('<div class="od-page-block">')
            for row in page_rows:
                w(owner_required_card(row, actions[row['file']][int(row['row'])],
                                      nearest.get((row['file'], int(row['row'])))))
            w('</div>')
            w('')
    # ------------------------------------------------------------ 2. PENDING
    admin_pages = {r['file'] for r in rows if r['status'] == 'policy'}
    pend_clin = [r for r in pend_row if r['file'] not in admin_pages]
    pend_admin = [r for r in pend_row if r['file'] in admin_pages]
    assert len(pend_clin) + len(pend_admin) == len(pend_row)
    w(f'<h2 id="pending">2. Pending authorization — {len(pend_page) + len(pend_row)} rows</h2>')
    w('')
    w(f'**{len(pend_page)} whole-page rows** — a protocol that is not in PEMS 2024 at all. '
      f'**{len(pend_clin)} clinical agency additions** — a row the agency wrote on a page '
      f'that is otherwise PEMS-cited. **{len(pend_admin)} administrative rules** — a policy '
      f'row no PEMS administrative policy prints.')
    w('')
    w(f'<p class="od-pagenote">The brief for this page said "14 PENDING rows" (11 + 3). '
      f'The ledger records {len(pend_row)} single-row PENDING entries: {len(pend_clin)} '
      f'clinical agency additions plus {len(pend_admin)} administrative rules. Both are '
      f'listed below, so the number you see here is {len(pend_page) + len(pend_row)} — '
      f'derived from the ledger, not from the brief. The {len(pend_admin)} administrative '
      f'rules are decided together with the Batch 6 administrative ruling (see the open '
      f'questions).</p>')
    w('')
    for label, anchor, group in (
            ('Whole page not in PEMS 2024', 'pending-whole-page', pend_page),
            ('Clinical agency additions', 'pending-agency', pend_clin),
            ('Administrative rules PEMS does not print', 'pending-admin', pend_admin)):
        w(f'<h3 id="{anchor}">{esc(label)} — {len(group)} rows</h3>')
        w('')
        for rel, page_rows in group_by_page(group, labels, order):
            note = page_note(rel, 'PENDING')
            per_row = [note_for_row(note, int(r['row'])) for r in page_rows]
            whole = all(n == note for n in per_row)
            w(page_heading(rel, human(rel, labels), len(page_rows)))
            w('')
            w('<div class="od-page-block">')
            if note and whole:
                w(f'<p class="od-pagenote"><strong>Note you will see on the page:</strong> '
                  f'{esc(note)}</p>')
            for row, row_note in zip(page_rows, per_row):
                w(pending_card(row, actions[row['file']][int(row['row'])],
                               carried_level(row),
                               None if whole else row_note))
            w('</div>')
            w('')
    # ------------------------------------------------------- 3. OPEN QUESTIONS
    w(f'<h2 id="open-questions">3. Open questions about the rules — {len(questions)}</h2>')
    w('')
    w('These are not row-level decisions. Each one is a question about how the rule '
      'itself should read, recorded in the conversion ledger and grouped here by the '
      'batch that raised it — the batch is the topic of work, and every card opens with '
      'the ledger\'s own heading naming its subject.')
    w('')
    for batch in buckets:
        items = buckets[batch]
        w(f'<h3>{esc(batch)} <span class="od-count">{len(items)}</span></h3>')
        w('')
        for entry in items:
            w('<div class="od-card od-cat-question">')
            w(f'<p class="od-head"><span class="od-batch">{esc(entry["batch"])}</span></p>')
            w(f'<p class="od-question">{inline_md(entry["text"])}</p>')
            w('</div>')
        w('')
    # ------------------------------------------- 4. RECORDED RULINGS (already decided)
    w(f'<h2 id="ruled">4. Already ruled — recorded decisions — {len(ruled)}</h2>')
    w('')
    w('The owner has already answered these, so they are not waiting on you. They are '
      'published as a record: the page states the level that was decided, and the answer '
      'and the PEMS citation stay in the audit trail '
      '(`audit/level-scan/level-rulings.yaml`, `audit/level-scan/relocated-rows.yaml`).')
    w('')
    for entry in ruled:
        w('<div class="od-card od-cat-question">')
        w('<p class="od-head"><span class="od-batch">Decided</span></p>')
        w(f'<p class="od-question">{inline_md(entry["text"])}</p>')
        w('</div>')
    w('')
    w('<p class="od-foot">Generated from the conversion ledger by '
      '`scripts/build_outstanding_decisions.py`. Row text and reasons are the ledger\'s '
      'own words; this page adds no clinical content and edits no protocol page.</p>')
    return '\n'.join(o) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--print', dest='stdout', action='store_true')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    page = build()
    if args.stdout:
        sys.stdout.write(page)
        return 0
    if args.check:
        if not os.path.exists(OUT):
            print(f'FAIL — {OUT_REL} is missing')
            return 1
        if open(OUT, encoding='utf-8').read() != page:
            print(f'FAIL — {OUT_REL} is stale; re-run '
                  f'scripts/build_outstanding_decisions.py')
            return 1
        print(f'OK — {OUT_REL} matches the ledger')
        return 0
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(page)
    print(f'wrote {OUT_REL} ({len(page)} bytes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
