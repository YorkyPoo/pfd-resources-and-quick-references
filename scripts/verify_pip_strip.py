#!/usr/bin/env python3
"""Verify the pip strip on every converted page, row by row, against the markdown.

    python3 scripts/verify_pip_strip.py --base <site_dir or https://…/preview/all-pages/>
    python3 scripts/verify_pip_strip.py --base site --archive audit/archive/tables-2026-11-20

The page list is **derived in code**, never hand-written: every markdown page
that carries a level table — wrapper without ``policy``, three columns, second
header cell ``Level``, and at least one row that publishes a level — must
render a strip. A table whose every row is ``PENDING`` publishes no level and
must not be converted; a page whose only tables have no ``Level`` column must
not either.

Reads the *rendered HTML* — the same bytes a phone gets — and, per page:

  * the picker (six buttons, one pressed on load), header ``R B A I P``, tally
  * every row's ``data-states`` against the level chip in that page's markdown
  * a ``PENDING`` row renders ``pending,pending,pending,pending,pending`` with
    ``data-pending`` and its own tag; it is never ``no,no,no,no,no``
  * the ``*`` / ``†`` markers the chip carried, which must survive the strip
  * row count against the markdown, and the tally against the rows
  * with ``--archive``: pages skipped by the rollout must be byte-identical to
    the archived pre-rollout markup, so nothing outside the list moved.

The chip reading here is written independently of ``mkdocs_pip_strip``'s
rendered-HTML reader (it walks the spans of the markdown cell and word-splits
each class list), so agreement is evidence, not a tautology; the ladder itself
is covered by ``scripts/test_pip_strip_mapper.py`` against the owner's prototype.

Exit 0 only when every expected page and every row agrees.
"""
import argparse
import html as html_lib
import os
import re
import sys
import urllib.request
from urllib.parse import quote as urlquote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkdocs_pip_strip import LEVELS, PENDING_STATES, states_for  # noqa: E402

DIV = re.compile(r'<div class="lv-wrap(?P<cls>[^"]*)"[^>]*>(?P<body>.*?)</div>', re.S)
LEVEL_WORD = {"lvl-emr": 0, "lvl-emt": 1, "lvl-a": 2, "lvl-i": 3, "lvl-p": 4}
SUP = re.compile(r'<sup class="lvl-(req|deriv)"[^>]*>(.*?)</sup>', re.S)
BLOCK = re.compile(r'<div class="pip-block" data-pip-block>(.*?)</tbody></table></div>', re.S)
ROW = re.compile(r'<tr data-states="([^"]+)"([^>]*)>(.*?)</tr>', re.S)


# ---------------------------------------------------- what the markdown says

def chip_states(cell):
    """(states, marks) for one markdown Level cell — independent reader."""
    if 'lvl-pending' in cell:
        return list(PENDING_STATES), []
    cls_words = [cls.split() for cls in re.findall(r'<span class="([^"]*)"[^>]*>', cell)]
    level = None
    mc_all = False
    for words in cls_words:
        for name, idx in LEVEL_WORD.items():
            if name in words:
                level = idx
        if 'lvl-mc' in words:
            mc_all = True
    bracketed = 'lvl-mc-req' in cell or 'lvl-req' in cell
    mc = {level} if (bracketed and level is not None) else set()
    states = states_for(level, mc, mc_all and level is None)
    marks = [html_lib.unescape(m.group(2).strip()) for m in SUP.finditer(cell)]
    return states, marks


def page_tables(md_path, rel=None):
    """[(kind, [(num, states, marks)])] per lv-wrap table, in order.

    kind is 'convert' (a level table with at least one published level),
    'pending' (a level table where every row is PENDING — no level exists) or
    'policy' (no Level column). A level chip in a table the rules would not
    convert is a contradiction and raises, so a misclassified page can never be
    silently skipped again.
    """
    text = open(md_path, encoding='utf-8', errors='replace').read()
    out = []
    for m in DIV.finditer(text):
        cls = (m.group('cls') or '').split()
        rows = [ln.strip() for ln in m.group('body').splitlines()
                if ln.strip().startswith('|')]
        cells = [[c.strip() for c in r.strip('|').split('|')] for r in rows]
        hdr = cells[0] if cells else []
        is_level = len(hdr) == 3 and hdr[1].strip().lower() == 'level'
        body = []
        for c in cells[1:]:
            if len(c) < 3 or set(c[0]) <= set(':- ') or not re.fullmatch(r'\d+[a-z]?', c[0]):
                continue
            body.append(c)
        level_chips = [c for c in body
                       if any(w in LEVEL_WORD
                              for cl in re.findall(r'class="([^"]*)"', c[1])
                              for w in cl.split())]
        if not (is_level and 'policy' not in cls):
            if level_chips and 'policy' in cls:
                out.append(('policy-named-level', []))
                continue
            if level_chips:
                raise ValueError(f'{rel or md_path}: provider-level chips in a table with no '
                                 f'Level column — refusing to treat it as a policy table')
            out.append(('policy', []))
            continue
        parsed = []
        pending = 0
        for c in body:
            states, marks = chip_states(c[1])
            if states == PENDING_STATES:
                pending += 1
            elif all(s == 'no' for s in states):
                raise ValueError(f'{rel or md_path}: row {c[0]} publishes no level and is not '
                                 f'PENDING — refusing to render it as "not authorised"')
            parsed.append((c[0], states, marks))
        if parsed and pending == len(parsed):
            out.append(('pending', parsed))
        else:
            out.append(('convert', parsed))
    return out


def expected_pages(docs):
    """{docs-relative .md path: [table, ...]} for pages that must be converted."""
    exp = {}
    for root, dirs, files in os.walk(docs):
        dirs.sort()
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, docs).replace(os.sep, '/')
            tables = [b for kind, b in page_tables(p, rel) if kind == 'convert']
            if tables:
                exp[rel] = tables
    return exp


def unchanged_pages(docs):
    """Pages that carry an lv-wrap table but must NOT be converted."""
    out = set()
    for root, dirs, files in os.walk(docs):
        for f in files:
            if not f.endswith('.md'):
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, docs).replace(os.sep, '/')
            tables = page_tables(p, rel)
            if tables and not any(kind == 'convert' for kind, _ in tables):
                out.add(rel)
    return out


# ------------------------------------------------------------ reading a page

def load(base, rel):
    html_rel = rel[:-3] + '.html'
    if base.startswith('http'):
        url = base.rstrip('/') + '/' + urlquote(html_rel, safe='/')
        req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(req, timeout=30) as fh:
            return fh.read().decode('utf-8', 'replace')
    with open(os.path.join(base, html_rel), encoding='utf-8') as fh:
        return fh.read()


def archive_blocks(archive, rel):
    html_rel = rel[:-3] + '.html'
    with open(os.path.join(archive, html_rel), encoding='utf-8') as fh:
        return [m.group(0) for m in DIV.finditer(fh.read())]


def check_page(rel, tables, html, problems):
    blocks = BLOCK.findall(html)
    if len(blocks) != len(tables):
        problems.append(f'{rel}: {len(blocks)} pip block(s), markdown has {len(tables)} table(s)')
        return 0, len(blocks), sum(len(t) for t in tables), sum(
            len(ROW.findall(b)) for b in blocks)
    rows_ok = 0
    md_rows = html_rows = 0
    for ti, (blk, want) in enumerate(zip(blocks, tables), 1):
        where = f'{rel} table {ti}'
        btns = re.findall(r'<button type="button" class="pip-btn[^"]*" data-level="([^"]+)" '
                          r'aria-pressed="([^"]+)">', blk)
        if [d for d, _ in btns] != ['R', 'B', 'A', 'I', 'P', 'all']:
            problems.append(f'{where}: picker is {[d for d, _ in btns]}, expected R B A I P + all')
        if not any(p == 'true' for _, p in btns):
            problems.append(f'{where}: nothing aria-pressed on load')
        head = re.search(r'<span class="pip-strip pip-strip-head">((?:<i>[^<]*</i>)+)</span>', blk)
        letters = re.findall(r'<i>([^<]*)</i>', head.group(1)) if head else []
        if letters != LEVELS:
            problems.append(f'{where}: header {letters}, expected R B A I P')
        tally = re.search(r'class="pip-tally"[^>]*>(.*?)</p>', blk, re.S)
        tally_txt = re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', tally.group(1))).strip() if tally else ''
        if not tally_txt:
            problems.append(f'{where}: no tally line')
        m = re.search(r'(\d+) actions', tally_txt)
        got = ROW.findall(blk)
        md_rows += len(want)
        html_rows += len(got)
        if m and int(m.group(1)) != len(got):
            problems.append(f'{where}: tally says {m.group(1)} actions, table has {len(got)}')
        n_unv = sum(1 for _, attrs, _ in got if 'data-unverified' in attrs)
        if n_unv and f'{n_unv} level unverified' not in tally_txt:
            problems.append(f'{where}: {n_unv} unverified row(s) not disclosed in the tally')
        n_pend = sum(1 for _, attrs, _ in got if 'data-pending' in attrs)
        if n_pend and f'{n_pend} PENDING (no published level)' not in tally_txt:
            problems.append(f'{where}: {n_pend} PENDING row(s) not disclosed in the tally')
        if len(got) != len(want):
            problems.append(f'{where}: {len(got)} rows rendered, markdown has {len(want)}')
        for i in range(min(len(got), len(want))):
            states, _attrs, inner = got[i]
            nm = re.search(r'<td class="pip-n">([^<]*)</td>', inner)
            num = nm.group(1).strip() if nm else '?'
            e_num, e_states, e_marks = want[i]
            e_pending = e_states == PENDING_STATES
            if num != e_num:
                problems.append(f'{where}: row {i + 1} numbered {num}, markdown {e_num}')
            if ('data-pending' in _attrs) != e_pending:
                problems.append(f'{where}: row {e_num} data-pending is '
                                f'{"present" if "data-pending" in _attrs else "absent"}, '
                                f'chip is {"PENDING" if e_pending else "a level"}')
            if e_pending:
                pips = re.findall(r'<i class="([^"]*)"></i>', inner)
                if pips != ['pip pending'] * 5:
                    problems.append(f'{where}: PENDING row {e_num} renders pips {pips}, '
                                    f'expected 5 dashed "pip pending"')
                if 'pip-tag pending' not in inner:
                    problems.append(f'{where}: PENDING row {e_num} has no pending tag')
            if states != ','.join(e_states):
                problems.append(f'{where}: row {e_num} renders {states}, chip says '
                                f'{",".join(e_states)}')
            marks = [re.sub(r'\s+', '', x) for x in
                     re.findall(r'<span class="pip-mark pip-mark-[a-z]+"[^>]*>(.*?)</span>',
                                inner, re.S)]
            if marks != [re.sub(r'\s+', '', x) for x in e_marks]:
                problems.append(f'{where}: row {e_num} markers {marks}, chip carries {e_marks}')
            rows_ok += 1
    return rows_ok, len(blocks), md_rows, html_rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True, help='built site dir or https://…/preview/<slot>/')
    ap.add_argument('--src', default='docs', help='markdown dir the site was built from')
    ap.add_argument('--archive', default='audit/archive/tables-2026-11-20',
                    help='pre-rollout archive; skipped pages must match it byte for byte '
                         '(empty string disables the check)')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    exp = expected_pages(args.src)
    skip = unchanged_pages(args.src)
    problems = []
    total_rows = 0
    total_md = total_html = 0

    for rel, tables in sorted(exp.items()):
        try:
            html = load(args.base, rel)
        except Exception as exc:  # noqa: BLE001
            problems.append(f'{rel}: cannot load ({exc})')
            continue
        n, nb, md, ht = check_page(rel, tables, html, problems)
        total_rows += n
        total_md += md
        total_html += ht
        if not args.quiet:
            print(f'  ok  {rel:74s} {nb} block(s), {n} row(s)')

    for rel in sorted(skip):
        try:
            html = load(args.base, rel)
        except Exception as exc:  # noqa: BLE001
            problems.append(f'{rel}: cannot load ({exc})')
            continue
        if 'data-pip-block' in html:
            problems.append(f'{rel}: converted, but its only tables publish no provider level')
            continue
        if args.archive:
            try:
                if archive_blocks(args.archive, rel) != [m.group(0) for m in DIV.finditer(html)]:
                    problems.append(f'{rel}: table markup differs from the archive')
            except OSError as exc:
                problems.append(f'{rel}: archive file missing ({exc})')

    print()
    print(f'pages converted : {len(exp)}')
    print(f'action rows     : {total_rows}')
    print(f'pages untouched : {len(skip)} (no provider level in any table)')
    mismatches = len(problems)
    print(f'{total_md} rows in markdown / {total_html} rows in HTML / {total_rows} compared '
          f'/ {mismatches} mismatches')
    if problems:
        print(f'FAIL — {len(problems)} problem(s):')
        for p in problems:
            print('  ' + p)
        return 1
    print('OK — every converted page matches its markdown, row by row; '
          'every untouched page is unchanged')
    return 0


if __name__ == '__main__':
    sys.exit(main())
