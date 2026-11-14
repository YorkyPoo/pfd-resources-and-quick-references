#!/usr/bin/env python3
"""Read-only reconciliation: published protocol site (docs/protocols) vs vault master.

Re-run:  python3 reconcile.py
Reads:   site working tree docs/protocols/**/*.md, vault EMS folder, site git history via `git show` (read-only).
Writes:  only into this directory: drift.json, summary.json, sample10.json, provenance.json,
         RECONCILIATION_REPORT.md (NARRATIVE.md, if present, is appended verbatim).
"""
import re, os, json, glob, random, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
SITE_DIR = os.path.join(REPO, 'docs', 'protocols')
VAULT_DIR = os.environ.get(
    'VAULT_DIR',
    '/root/System/mindpalace/30 - projects/Active/EMS Protocols/Poquoson Fire and Rescue Patient Care Protocols')
LEVELS = ['EMR', 'EMT', 'A', 'I', 'P']
LVL_NAME = {'A': 'AEMT'}
ORD = {'blank': 0, 'mc': 1, 'br': 1, 'dot': 2}          # own-level authority ordinal (literal view)
RANK = {'S': 2, 'M': 1, 'N': 0, 'N*': 0}                 # effective view: standing > MC > none
HDR = re.compile(r'\|\s*EMR\s*\|\s*EMT\s*\|\s*A\s*\|\s*I\s*\|\s*P\s*\|')
SEP = re.compile(r'^\|[\s:|-]+\|$')
DIV_WORDS = re.compile(r'\b(pathway|anaphylaxis|non-anaphylaxis)\b')
ACTION_WORDS = re.compile(r'\d|\b(administer|apply|consider|obtain|monitor|repeat|give|contact|transport|if|for)\b')
SEED = 20261114
BUCKET_PRI = ['site_broader', 'site_narrower', 'bracket_shape', 'eff_only']


# ---------------------------------------------------------------- parsing
def cells(line):
    """escape-aware split: \\| is cell TEXT (same as level_review_packet.cells)"""
    s = line.strip().strip('|').replace('\\|', '\x00')
    return [c.strip().replace('\x00', '|') for c in s.split('|')]


def parse_text(text):
    L = text.splitlines()
    tables, i = [], 0
    while i < len(L):
        if L[i].lstrip().startswith('|') and HDR.search(L[i]):
            hdr = cells(L[i]); n = len(hdr)
            t = {'header_line': i + 1, 'ncol': n, 'rows': [], 'malformed': []}
            j = i + 1
            if j < len(L) and SEP.match(L[j].strip()):
                j += 1
            while j < len(L) and L[j].strip().startswith('|'):
                c = cells(L[j])
                if n == 7 and len(c) == 7:
                    t['rows'].append({'line': j + 1, 'raw': L[j], 'num': c[0], 'action': c[1], 'lv': c[2:7]})
                else:
                    t['malformed'].append({'line': j + 1, 'raw': L[j], 'ncells': len(c),
                                           'num': c[0] if c else ''})
                j += 1
            tables.append(t)
            i = j
        else:
            i += 1
    return tables


def lvkind(raw, col):
    s = raw.strip().strip('"\'`*_').replace('·', '•').upper().strip()
    if s == '':
        return 'blank'
    if s == '•':
        return 'dot'
    if s == 'MC':
        return 'mc'
    m = re.fullmatch(r'\[(EMR|EMT|A|I|P)\]', s)
    if m:
        return 'br' if m.group(1) == col else 'br_mismatch'
    return 'other'


def norm_text(s):
    s = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)          # markdown links -> link text
    s = s.replace('<br/>', ' ').replace('<br>', ' ').replace('&nbsp;', ' ')
    s = s.replace('**', '').replace('__', '')
    return re.sub(r'\s+', ' ', s).strip().lower()


def is_divider(has_num, t, kinds):
    if any(k != 'blank' for k in kinds):
        return False
    if DIV_WORDS.search(t) and len(t) <= 40:
        return True
    return (not has_num) and len(t) <= 48 and not ACTION_WORDS.search(t)


# ---------------------------------------------------------------- semantics
def effective(kinds):
    """Owner rulings: • at N = standing at N and above (cumulative). [X] at N = X must call MC, above act
    standing, BELOW denied (floor). Plain MC = that level must call MC; it is NOT implied upward
    (site legend: 'MC is never implied'). Blank = no authority unless a lower • or [X] supplies it."""
    out, flags = [], []
    for L in range(5):
        own = kinds[L]
        floor = any(kinds[F] == 'br' for F in range(L + 1, 5))
        if floor:
            if own != 'blank':
                flags.append(('floor_conflict', LEVELS[L]))
            out.append('N*' if own != 'blank' else 'N')
        elif own == 'dot':
            out.append('S')
        elif own in ('mc', 'br'):
            out.append('M')
        elif own == 'blank':
            out.append('S' if any(k in ('dot', 'br') for k in kinds[:L]) else 'N')
        else:
            out.append('U')
    return out, flags


def dot_below_mc(kinds):
    """Legend: a • implies standing at every HIGHER tier. A higher tier carrying an explicit MC or [X]
    therefore contradicts a lower-tier •. Returns the offending levels (source-data conflicts per legend)."""
    bad = []
    for L in range(5):
        if kinds[L] in ('mc', 'br') and any(kinds[N] == 'dot' for N in range(L)):
            bad.append(LEVELS[L])
    return bad


def literal_bucket(sk, vk):
    if sk == vk:
        return None
    if ORD[sk] == ORD[vk]:
        return 'bracket_shape'
    return 'site_broader' if ORD[sk] > ORD[vk] else 'site_narrower'


def eff_bucket(se, ve):
    if se == ve:
        return None
    if 'U' in (se, ve):
        return 'unknown'
    return 'site_broader' if RANK[se] > RANK[ve] else 'site_narrower'


# ---------------------------------------------------------------- corpus loading
def read_tree(root):
    out = {}
    for f in sorted(glob.glob(root + '/**/*.md', recursive=True)):
        out[os.path.relpath(f, root)] = open(f, encoding='utf-8').read()
    return out


def git_show_tree(rev, prefix):
    names = subprocess.run(['git', '-C', REPO, 'ls-tree', '-r', '--name-only', rev, prefix],
                           capture_output=True, text=True, check=True).stdout.splitlines()
    out = {}
    for p in names:
        if p.endswith('.md'):
            out[os.path.relpath(p, prefix)] = subprocess.run(
                ['git', '-C', REPO, 'show', f'{rev}:{p}'], capture_output=True, text=True, check=True).stdout
    return out


def by_basename(texts, label):
    d = {}
    for rel, txt in texts.items():
        b = os.path.basename(rel)
        if b in d:
            raise SystemExit(f'duplicate basename on {label}: {b}')
        d[b] = {'rel': rel, 'text': txt, 'tables': parse_text(txt)}
    return d


# ---------------------------------------------------------------- comparison
def row_key(r):
    return ('n', int(r['num'])) if r['num'].isdigit() else ('l', norm_text(r['action'])[:80])


def compare_corpora(S, V):
    recs, stats, cellc, internal = [], collections.Counter(), collections.Counter(), []
    for fb in sorted(set(S) & set(V)):
        st, vt = S[fb]['tables'], V[fb]['tables']
        if not st or not vt:
            stats['paired_without_matrix'] += 1
            continue
        if len(st) != 1 or len(vt) != 1:
            stats['multi_table_file'] += 1
        gated = not fb.startswith('01_')
        sT, vT = st[0], vt[0]
        sidx, vidx = {}, {}
        for r in sT['rows']:
            sidx.setdefault(row_key(r), r)
        for r in vT['rows']:
            vidx.setdefault(row_key(r), r)
        smal = {int(m['num']) for m in sT['malformed'] if m['num'].isdigit()}
        vmal = {int(m['num']) for m in vT['malformed'] if m['num'].isdigit()}
        base = {'file': S[fb]['rel'], 'folder': 'administrative' if not gated else 'clinical', 'gated': gated}
        for k in sorted(set(sidx) | set(vidx) | {('n', x) for x in smal | vmal}, key=lambda z: (z[0], str(z[1]))):
            s, v = sidx.get(k), vidx.get(k)
            is_num = k[0] == 'n'
            rowid = str(k[1]) if is_num else 'unnumbered'
            rec = dict(base, row=rowid, key=str(k[1]))
            s_bad = is_num and k[1] in smal
            v_bad = is_num and k[1] in vmal
            if s is None and v is None:
                b = 'unparseable_site' if s_bad else 'unparseable_vault'
                stats[b] += 1
                recs.append(dict(rec, bucket=b, cells=[]))
                continue
            if s is None:
                assert v is not None
                b = 'unparseable_site' if s_bad else 'row_missing_site'
                stats[b] += 1
                recs.append(dict(rec, bucket=b, cells=[], vault_line=v['line'], vault_raw=v['raw'],
                                 vault_action=v['action']))
                continue
            if v is None:
                b = 'unparseable_vault' if v_bad else 'row_missing_vault'
                stats[b] += 1
                recs.append(dict(rec, bucket=b, cells=[], site_line=s['line'], site_raw=s['raw'],
                                 site_action=s['action']))
                continue
            sk = [lvkind(c, LEVELS[i]) for i, c in enumerate(s['lv'])]
            vk = [lvkind(c, LEVELS[i]) for i, c in enumerate(v['lv'])]
            if any(x in ('other', 'br_mismatch') for x in sk + vk):
                stats['unrecognized_cell_row'] += 1
                recs.append(dict(rec, bucket='unrecognized_cell', cells=[], site_line=s['line'], vault_line=v['line']))
                continue
            st_n, vt_n = norm_text(s['action']), norm_text(v['action'])
            common = dict(site_line=s['line'], vault_line=v['line'], site_raw=s['raw'], vault_raw=v['raw'],
                          action=s['action'], site_lv=s['lv'], vault_lv=v['lv'])
            if st_n != vt_n:
                stats['text_differs'] += 1
                recs.append(dict(rec, bucket='text_differs', cells=[], vault_action=v['action'], **common))
                continue
            if is_divider(k[0] == 'n', st_n, sk) and is_divider(k[0] == 'n', vt_n, vk):
                stats['divider'] += 1
                recs.append(dict(rec, bucket='divider', cells=[], **common))
                continue
            stats['rows_compared'] += 1
            effS, flS = effective(sk)
            effV, flV = effective(vk)
            for _ in flS:
                stats['site_internal_floor_conflict'] += 1
            for _ in flV:
                stats['vault_internal_floor_conflict'] += 1
            if dot_below_mc(sk):
                stats['site_internal_dot_below_mc_rows'] += 1
                internal.append({'side': 'site', 'file': S[fb]['rel'], 'row': rowid, 'levels': dot_below_mc(sk),
                                 'line': s['line']})
            if dot_below_mc(vk):
                stats['vault_internal_dot_below_mc_rows'] += 1
                internal.append({'side': 'vault', 'file': V[fb]['rel'], 'row': rowid, 'levels': dot_below_mc(vk),
                                 'line': v['line']})
            cl = []
            for i in range(5):
                lb = literal_bucket(sk[i], vk[i])
                eb = eff_bucket(effS[i], effV[i])
                if lb is None and eb is None:
                    continue
                if lb is None:
                    lb = 'eff_only'
                cl.append({'level': LEVELS[i], 'site': s['lv'][i], 'vault': v['lv'][i],
                           'site_kind': sk[i], 'vault_kind': vk[i], 'site_eff': effS[i], 'vault_eff': effV[i],
                           'literal': lb, 'effective': eb})
                cellc[('literal', lb, 'gated' if gated else 'admin')] += 1
                if eb:
                    cellc[('effective', eb, 'gated' if gated else 'admin')] += 1
            if cl:
                pri = min((BUCKET_PRI.index(c['literal']) for c in cl), default=9)
                rb = BUCKET_PRI[pri] if pri < 9 else 'eff_only'
                stats['rows_with_cell_discrepancy'] += 1
                recs.append(dict(rec, bucket=rb, cells=cl, **common))
    return recs, stats, cellc, internal


# ---------------------------------------------------------------- provenance replay (in memory only)
TIERS = ['EMR', 'EMT', 'A', 'I', 'P']


def script_cols(line):
    s = line.strip().strip('|').replace('\\|', '\x00')
    return [c.replace('\x00', '|') for c in s.split('|')]


def replay_inheritance(text):
    """In-memory replica of scripts/fix_scope_inheritance.py. Never writes. Returns (new_text_rows, fills)."""
    lines = text.splitlines()
    fills, tables_after, i = [], [], 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i + 1]):
            names = [c.strip(' *').upper() for c in script_cols(ln)]
            if len(names) == 7 and set(TIERS) <= set(names):
                idx = [names.index(t) for t in TIERS]
                j = i + 2
                rows = []
                while j < len(lines) and lines[j].startswith('|'):
                    cl = script_cols(lines[j])
                    if len(cl) == 7:
                        for k in range(4):
                            src, dst = cl[idx[k]], cl[idx[k + 1]]
                            if ('\u2022' in src or re.search(r'\bMC\b', src)) and not ('\u2022' in dst or re.search(r'\bMC\b', dst)):
                                kind = 'dot' if '\u2022' in src else 'mc'
                                cl[idx[k + 1]] = src
                                fills.append({'row': cl[0].strip(), 'dst': TIERS[k + 1], 'src_kind': kind,
                                              'src_level': TIERS[k]})
                    rows.append(cl)
                    j += 1
                tables_after.append(rows)
                i = j
                continue
        i += 1
    return tables_after, fills


def provenance(pre_docs, post_docs, head_docs):
    """Replay the 16c0627 script on its pre-state; check against its post-state; count effect by source."""
    rep = {}
    for rel, txt in pre_docs.items():
        rep[rel] = replay_inheritance(txt)
    files_with_fill = sorted({r for r, (t, f) in rep.items() if f})
    total_fills = sum(len(f) for t, f in rep.values())
    by_kind = collections.Counter(x['src_kind'] for t, f in rep.values() for x in f)
    # 1) replay vs actual post-state, cell by cell (level kinds, row by row)
    mism = 0
    for rel, (tabs, fills) in rep.items():
        post_tabs = [t['rows'] for t in parse_text(post_docs.get(rel, ''))]
        if len(post_tabs) != len(tabs):
            mism += 1
            continue
        for rt, pt in zip(tabs, post_tabs):
            for r1, r2 in zip(rt, pt):
                if len(r1) != 7:
                    continue
                for c in range(2, 7):
                    if lvkind(r1[c], TIERS[c - 2]) != lvkind(r2['lv'][c - 2], TIERS[c - 2]):
                        mism += 1
    # 2) effect on effective authority: pre-state vs replayed, per level
    eff_changes = collections.Counter()
    for rel, txt in pre_docs.items():
        pre_t = parse_text(txt)
        post_t = parse_text(post_docs.get(rel, ''))
        if not pre_t or not post_t or rel not in rep:
            continue
        _, fills = rep[rel]
        fill_by_row = collections.defaultdict(dict)
        for f in fills:
            fill_by_row[f['row']][f['dst']] = f['src_kind']
        for tp, tq in zip(pre_t[:1], post_t[:1]):
            for r1, r2 in zip(tp['rows'], tq['rows']):
                if not fill_by_row.get(r1['num']):
                    continue
                before, _ = effective([lvkind(c, TIERS[i]) for i, c in enumerate(r1['lv'])])
                after, _ = effective([lvkind(c, TIERS[i]) for i, c in enumerate(r2['lv'])])
                for i, L in enumerate(TIERS):
                    if L in fill_by_row[r1['num']] and before[i] != after[i]:
                        eff_changes[(fill_by_row[r1['num']][L], f'{before[i]}->{after[i]}')] += 1
    # 3) three-way: literal + effective discrepancies vs vault for pre / post-16c0627 / HEAD
    return {
        'files_with_fills': len(files_with_fill), 'total_fills_docs_wide': total_fills,
        'fills_by_source_kind': dict(by_kind), 'replay_vs_post_mismatches': mism,
        'effective_changes_by_source': {f'{k[0]} {k[1]}': v for k, v in eff_changes.items()},
    }


# ---------------------------------------------------------------- report
def fmt_cells(cl):
    return ', '.join(f"{c['level']}: {c['site'] or '∅'} / {c['vault'] or '∅'} [{c['literal']}"
                     + (f"; eff {c['site_eff']}→{c['vault_eff']}" if c['site_eff'] != c['vault_eff'] else '') + ']'
                     for c in cl)


def consequence(c):
    lv = LVL_NAME.get(c['level'], c['level'])
    se, ve = c['site_eff'], c['vault_eff']
    if c['effective'] == 'site_broader':
        if se == 'S' and ve == 'M':
            return f"{lv} would be told they may perform this as a STANDING order; vault requires Medical Control first."
        if se == 'S' and ve == 'N':
            return f"{lv} would be told they may perform this as a STANDING order; vault does not authorize {lv} at all."
        if se == 'M' and ve == 'N':
            return f"{lv} would be told they may perform this after an MC call; vault does not authorize {lv} at all."
    if c['effective'] == 'site_narrower':
        if ve == 'S':
            return f"{lv} would be told they may NOT perform this as standing (or must call MC); vault authorizes it as standing."
        if ve == 'M':
            return f"{lv} would be told they may not perform this; vault allows it after an MC call."
    if c['effective'] is None:
        return 'Notation only under the cumulative rule: no change in what the level may do.'
    return 'Effective authority differs; see cell detail.'


def score(rec):
    if not rec['gated'] or rec['bucket'] in ('text_differs', 'divider', 'unparseable_site', 'unparseable_vault'):
        return 0
    if rec['bucket'] == 'row_missing_site':
        return 60
    if rec['bucket'] == 'row_missing_vault':
        return 40
    best = 0
    for c in rec['cells']:
        s = 0
        if c['effective'] == 'site_broader':
            s = {('S', 'M'): 100, ('S', 'N'): 100, ('M', 'N'): 80}.get((c['site_eff'], c['vault_eff']), 60)
            if c['level'] in ('EMR', 'EMT'):
                s += 10
        elif c['effective'] == 'site_narrower':
            s = {('M', 'S'): 70, ('N', 'S'): 70, ('N', 'M'): 50, ('M', 'S'): 70}.get((c['site_eff'], c['vault_eff']), 40)
        elif c['effective'] is None and c['literal'] in ('site_broader', 'site_narrower'):
            s = 5
        best = max(best, s)
    return best


def implied_unwritten(S):
    """Blank cells that the cumulative rule already authorizes (a lower • or [X] with no MC-type cell between),
    i.e. cells a copy relies on the reader to infer. Also counts blanks directly above a plain MC with no
    • below (the legend says MC is never implied, so these stay unauthorized). Returns (n, examples, n_above_mc)."""
    n, n_mc, ex = 0, 0, []
    for b, f in S.items():
        for t in f['tables']:
            for r in t['rows']:
                kinds = [lvkind(c, LEVELS[i]) for i, c in enumerate(r['lv'])]
                for L in range(5):
                    if kinds[L] == 'blank' and any(k in ('dot', 'br') for k in kinds[:L]):
                        n += 1
                        ex.append({'file': f['rel'], 'row': r['num'], 'level': LEVELS[L], 'line': r['line']})
                    if L > 0 and kinds[L] == 'blank' and kinds[L - 1] == 'mc' and not any(k == 'dot' for k in kinds[:L]):
                        n_mc += 1
    return n, ex, n_mc


def main():
    site_texts = read_tree(SITE_DIR)
    vault_texts = read_tree(VAULT_DIR)
    S_all = by_basename(site_texts, 'site')
    V_all = by_basename(vault_texts, 'vault')
    # front-matter files (How-to-Read legend example tables etc.) are NOT protocols: reported as an appendix
    FRONT_S = {b for b in S_all if S_all[b]['rel'].startswith('front-matter')}
    FRONT_V = {b for b in V_all if b in FRONT_S}
    S = {b: v for b, v in S_all.items() if b not in FRONT_S}
    V = {b: v for b, v in V_all.items() if b not in FRONT_V}
    S_front = {b: S_all[b] for b in FRONT_S}
    V_front = {b: V_all[b] for b in FRONT_V}
    pre = git_show_tree('16c0627^', 'docs')
    post = git_show_tree('16c0627', 'docs')
    pre_p = {k: v for k, v in pre.items() if k.startswith('protocols/')}
    post_p = {k: v for k, v in post.items() if k.startswith('protocols/')}
    Spre = by_basename({k.split('/', 1)[1]: v for k, v in pre_p.items()}, 'site@16c0627^')
    Spost = by_basename({k.split('/', 1)[1]: v for k, v in post_p.items()}, 'site@16c0627')
    Spre = {b: v for b, v in Spre.items() if b not in FRONT_S}
    Spost = {b: v for b, v in Spost.items() if b not in FRONT_S}

    recs, stats, cellc, internal = compare_corpora(S, V)
    recs_pre, stats_pre, cellc_pre, _ = compare_corpora(Spre, V)
    recs_post, stats_post, cellc_post, _ = compare_corpora(Spost, V)
    recs_front, stats_front, cellc_front, _ = compare_corpora(S_front, V_front)
    # internal (site-only) conflict reporting uses the same function; keep only the head-side list
    S, V = S, V  # protocol-scope maps (front matter excluded)

    # pairing
    sb, vb = set(S), set(V)
    paired = sorted(sb & vb)
    site_only = sorted(sb - vb)
    vault_only = sorted(vb - sb)
    site_has_elsewhere = {b: sorted(os.path.relpath(p, REPO) for p in glob.glob(REPO + f'/docs/**/{b}', recursive=True)
                                    if not p.startswith(SITE_DIR)) for b in vault_only}
    site_has_elsewhere = {b: v for b, v in site_has_elsewhere.items() if v}
    files_compared = [b for b in paired if S[b]['tables'] and V[b]['tables']]
    prov = provenance(pre, post, site_texts)

    summary = {
        'site_protocol_md_files': len(S), 'vault_md_files': len(V),
        'site_files_with_matrix': sum(1 for b in S if S[b]['tables']),
        'vault_files_with_matrix': sum(1 for b in V if V[b]['tables']),
        'paired_basenames': len(paired), 'files_compared_both_have_matrix': len(files_compared),
        'site_only_unpaired': site_only, 'vault_only_unpaired': vault_only,
        'vault_only_basename_found_elsewhere_in_site_docs': site_has_elsewhere,
        'stats': dict(stats),
        'cell_counts': {f'{a}|{b}|{c}': n for (a, b, c), n in sorted(cellc.items())},
        'discrepancy_records': len(recs),
        'provenance_16c0627': prov,
        'three_way': {
            'pre_16c0627': {'stats': dict(stats_pre), 'cells': {f'{a}|{b}|{c}': n for (a, b, c), n in sorted(cellc_pre.items())}},
            'post_16c0627': {'stats': dict(stats_post), 'cells': {f'{a}|{b}|{c}': n for (a, b, c), n in sorted(cellc_post.items())}},
            'head': {'stats': dict(stats), 'cells': {f'{a}|{b}|{c}': n for (a, b, c), n in sorted(cellc.items())}},
        },
    }
    for r in recs:
        r['score'] = score(r)
    ranked = sorted([r for r in recs if r['score'] > 0],
                    key=lambda r: (-r['score'], -len(r['cells']), r['file'], str(r['row'])))
    top20 = ranked[:20]

    # sample-of-10 pool: every cell-level literal discrepancy (clinical AND admin), in deterministic order
    pool = []
    for r in recs:
        for c in r['cells']:
            if c['literal'] in ('site_broader', 'site_narrower', 'bracket_shape'):
                pool.append({'file': r['file'], 'row': r['row'], 'level': c['level'], 'literal': c['literal'],
                             'effective': c['effective'], 'site': c['site'], 'vault': c['vault'],
                             'site_line': r.get('site_line'), 'vault_line': r.get('vault_line'),
                             'site_raw': r.get('site_raw'), 'vault_raw': r.get('vault_raw'),
                             'action': r.get('action', ''), 'gated': r['gated']})
    sample = random.Random(SEED).sample(pool, min(10, len(pool))) if pool else []

    by_level = collections.Counter()
    for r in recs:
        if r['gated'] and r['bucket'] not in ('divider', 'text_differs'):
            for c in r['cells']:
                by_level[(c['level'], c['site_kind'], c['vault_kind'], c['literal'])] += 1
    summary['gated_cell_pattern_counts'] = {' | '.join(k): v for k, v in sorted(by_level.items(), key=lambda x: -x[1])}
    summary['front_matter_appendix'] = {
        'files': sorted(S_front[b]['rel'] for b in S_front),
        'stats': dict(stats_front), 'cells': {f'{a}|{b}|{c}': n for (a, b, c), n in sorted(cellc_front.items())}}
    summary['internal_conflicts'] = {'site_rows_dot_below_explicit_MC_or_bracket': sum(1 for x in internal if x['side'] == 'site'),
                                     'vault_rows_dot_below_explicit_MC_or_bracket': sum(1 for x in internal if x['side'] == 'vault')}
    summary['vault_only_unpaired_count'] = len(vault_only)
    summary['implied_unwritten_cells'] = {}
    for side, D in [('site', S), ('vault', V)]:
        n, ex, n_mc = implied_unwritten(D)
        summary['implied_unwritten_cells'][side] = n
        summary['implied_unwritten_cells'][side + '_examples'] = ex
        summary['implied_unwritten_cells'][side + '_blank_directly_above_plain_MC'] = n_mc

    summary['text_differs_rows'] = [{'file': r['file'], 'row': r['row'], 'site': norm_text(r.get('action', ''))[:140],
                                     'vault': norm_text(r.get('vault_action', ''))[:140]}
                                    for r in recs if r['bucket'] == 'text_differs']
    summary['site_only_unpaired'] = site_only
    summary['vault_only_unpaired'] = vault_only
    json.dump(summary, open(os.path.join(HERE, 'summary.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(recs, open(os.path.join(HERE, 'drift.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(internal, open(os.path.join(HERE, 'internal_conflicts.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(sample, open(os.path.join(HERE, 'sample10.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump(prov, open(os.path.join(HERE, 'provenance.json'), 'w'), indent=1, ensure_ascii=False)
    json.dump({'top20': top20, 'pool_size': len(pool)}, open(os.path.join(HERE, 'top20.json'), 'w'),
              indent=1, ensure_ascii=False)
    build_report(summary, top20, sample, internal)
    print(json.dumps({k: summary[k] for k in ['paired_basenames', 'files_compared_both_have_matrix',
                                             'stats', 'cell_counts', 'internal_conflicts']}, indent=1, ensure_ascii=False))
    print('site_only', len(site_only), 'vault_only', len(vault_only), 'pool', len(pool), 'top20', len(top20))
    print('provenance', json.dumps(prov, ensure_ascii=False))


def build_report(summary, top20, sample, internal):
    L = []
    w = L.append
    st = summary['stats']
    w('# Reconciliation report: published protocol site vs vault master')
    w('')
    w('Generated by `reconcile.py` (read-only over both corpora). Every number below is reproduced by re-running the script; '
      'raw inputs are cited by file and line.')
    w('')
    w('## 1. Totals')
    w('')
    w('| Measure | Count |')
    w('|---|---|')
    w(f"| Site protocol .md files (front matter excluded) | {summary['site_protocol_md_files']} |")
    w(f"| Vault protocol .md files | {summary['vault_md_files']} |")
    w(f"| Basenames paired | {summary['paired_basenames']} |")
    w(f"| **Files compared** (paired and both have a level matrix) | **{summary['files_compared_both_have_matrix']}** |")
    w(f"| Site-only unpaired files | {len(summary['site_only_unpaired'])} |")
    w(f"| Vault-only unpaired files | {len(summary['vault_only_unpaired'])} |")
    w(f"| Rows compared (same #, identical intervention text, not divider) | **{st.get('rows_compared', 0)}** |")
    w(f"| Rows with at least one cell discrepancy | {st.get('rows_with_cell_discrepancy', 0)} |")
    w(f"| Divider rows (excluded) | {st.get('divider', 0)} |")
    w(f"| text_differs rows (excluded from level counts) | {st.get('text_differs', 0)} |")
    w(f"| row_missing_site (vault has row, site lacks it) | {st.get('row_missing_site', 0)} |")
    w(f"| row_missing_vault (site has row, vault lacks it) | {st.get('row_missing_vault', 0)} |")
    w(f"| unparseable rows (malformed cell count; not guessed) | site {st.get('unparseable_site', 0)} / vault {st.get('unparseable_vault', 0)} |")
    w('')
    w('### Cell-level buckets (per brief definitions)')
    w('')
    cc = summary['cell_counts']

    def g(k):
        return cc.get(k, 0)
    w('| Bucket | Clinical (gated) rows | Administrative rows (not level-gated) |')
    w('|---|---|---|')
    for b in ['site_narrower', 'site_broader', 'bracket_shape', 'eff_only']:
        w(f"| literal `{b}` | {g(f'literal|{b}|gated')} | {g(f'literal|{b}|admin')} |")
    w('')
    w('`literal` = raw cell kinds compared (•, MC, [X], blank). `eff_only` = cells equal literally but whose effective authority differs because of a neighbouring cell.')
    w('')
    w(f"Blank cells the cumulative rule already authorizes but the copy leaves unwritten: site **{summary['implied_unwritten_cells']['site']}**, vault **{summary['implied_unwritten_cells']['vault']}** (all protocol rows). Blank cells directly above a plain MC with no `•` below (not authorized under the legend): site {summary['implied_unwritten_cells']['site_blank_directly_above_plain_MC']}, vault {summary['implied_unwritten_cells']['vault_blank_directly_above_plain_MC']}.")
    w('')
    w('Vault cells that rely on inference: ' + '; '.join(f"{x['file']} row {x['row']} {x['level']} (line {x['line']})" for x in summary['implied_unwritten_cells']['vault_examples']) + '.')
    w('')
    w('### Effective authority (owner cumulative rule applied)')
    w('')
    w('| Bucket | Clinical (gated) | Administrative |')
    w('|---|---|---|')
    for b in ['site_narrower', 'site_broader']:
        w(f"| effective `{b}` | {g(f'effective|{b}|gated')} | {g(f'effective|{b}|admin')} |")
    w('')
    w('Effective model: `•` at N = standing at N and above (cumulative, legend). `[X]` at N = X must call MC, levels above act standing, '
      'levels below denied (floor). Plain `MC` = that level must call MC and is **not** implied upward (legend: "MC is never implied"). '
      'Blank = not authorized unless a lower `•` or `[X]` supplies it.')
    w('')
    w('### Internal consistency (per side)')
    w('')
    ic = summary['internal_conflicts']
    w(f"- Floor conflicts (non-blank cell below an active bracket): site {st.get('site_internal_floor_conflict', 0)}, vault {st.get('vault_internal_floor_conflict', 0)}.")
    w(f"- Rows where a lower `•` sits under an explicit MC/[X] (legend calls these source-data conflicts for OMD): site {ic['site_rows_dot_below_explicit_MC_or_bracket']}, vault {ic['vault_rows_dot_below_explicit_MC_or_bracket']}.")
    w('')
    w('## 2. Pattern behind most discrepancies')
    w('')
    w('Gated cell patterns (site value / vault value → literal bucket), top ten:')
    w('')
    w('| Level | site kind | vault kind | literal bucket | cells |')
    w('|---|---|---|---|---|')
    for k, v in list(summary['gated_cell_pattern_counts'].items())[:10]:
        lv, sk, vk, lb = [x.strip() for x in k.split('|')]
        w(f'| {lv} | {sk} | {vk} | {lb} | {v} |')
    w('')
    w('## 3. Three-way check: did the 16c0627 inheritance script move the site toward the vault?')
    w('')
    w('| Site state | rows compared | literal site_narrower (clinical) | literal site_broader (clinical) | effective site_narrower (clinical) | effective site_broader (clinical) |')
    w('|---|---|---|---|---|---|')
    for name, key in [('before 16c0627 (16c0627^)', 'pre_16c0627'), ('after 16c0627', 'post_16c0627'), ('HEAD (current)', 'head')]:
        t = summary['three_way'][key]
        c = t['cells']
        w(f"| {name} | {t['stats'].get('rows_compared', 0)} | {c.get('literal|site_narrower|gated', 0)} | "
          f"{c.get('literal|site_broader|gated', 0)} | {c.get('effective|site_narrower|gated', 0)} | {c.get('effective|site_broader|gated', 0)} |")
    w('')
    p = summary['provenance_16c0627']
    w(f"Replay of `scripts/fix_scope_inheritance.py` in memory on the pre-16c0627 tree: **{p['total_fills_docs_wide']} fills in {p['files_with_fills']} files** "
      f"(commit message claims 699 cells / 65 matrices). Fills by source: {p['fills_by_source_kind']}. "
      f"Replay vs committed post-state mismatches: **{p['replay_vs_post_mismatches']}**. "
      f"Levels whose effective authority changed by fill type: {p['effective_changes_by_source'] or 'none'}.")
    w('')
    w('## 4. Top 20 discrepancies (clinical rows, ranked by provider-facing severity)')
    w('')
    w('Score: effective site_broader S over M/N = 100 (+10 at EMR/EMT); S over M = 80 for M over N; effective site_narrower = 40–70; '
      'row missing on site = 60; row missing on vault = 40. Ties broken by number of differing cells.')
    w('')
    w('| # | File | Row | Intervention (truncated) | Site EMR/EMT/A/I/P | Vault EMR/EMT/A/I/P | Bucket | If the site is authoritative |')
    w('|---|---|---|---|---|---|---|---|')
    for i, r in enumerate(top20, 1):
        txt = r.get('action', '') or r.get('vault_action', '') or r.get('site_action', '')
        txt = re.sub(r'\*\*|\[|\]\([^)]*\)|<br>', ' ', txt)
        txt = re.sub(r'\s+', ' ', txt).strip()[:90]
        sl = ' / '.join(x or '∅' for x in r.get('site_lv', ['?'] * 5))
        vl = ' / '.join(x or '∅' for x in r.get('vault_lv', ['?'] * 5))
        worst = max(r['cells'], key=lambda c: score_cell(c)) if r['cells'] else None
        cons = consequence(worst) if worst else ('Row exists in one copy only.' if 'missing' in r['bucket'] else '')
        bucket = r['bucket'] + (f" ({worst['effective']})" if worst and worst['effective'] else '')
        w(f"| {i} | {r['file']} | {r['row']} | {txt} | {sl} | {vl} | {bucket} | {cons} |")
    w('')
    w('## 5. Internal conflicts flagged for OMD (listed, not resolved)')
    w('')
    w('| Side | File | Row | Levels with an explicit MC/[X] under a lower `•` |')
    w('|---|---|---|---|')
    for x in internal[:40]:
        w(f"| {x['side']} | {x['file']} | {x['row']} | {', '.join(x['levels'])} |")
    if len(internal) > 40:
        w(f'| … | {len(internal) - 40} more in internal_conflicts.json | | |')
    w('')
    w('## 6. Sample of 10 hand-verified discrepancies')
    w('')
    w('Drawn with `random.Random(20261114)` from all cell-level literal discrepancies (clinical and admin). Raw source lines are printed exactly as they appear in the files.')
    w('')
    for i, s in enumerate(sample, 1):
        w(f"**{i}. {s['file']} row {s['row']} — level {s['level']}** — automated: site `{s['site'] or '∅'}` vs vault `{s['vault'] or '∅'}` → `{s['literal']}`")
        w(f"- site line {s['site_line']}: `{(s['site_raw'] or '').strip()[:260]}`")
        w(f"- vault line {s['vault_line']}: `{(s['vault_raw'] or '').strip()[:260]}`")
        w('')
    w('## 7. Rows with text differences (excluded from level counts)')
    w('')
    w('| File | Row | Site text (normalised, 140 chars) | Vault text (normalised, 140 chars) |')
    w('|---|---|---|---|')
    for x in summary['text_differs_rows']:
        w(f"| {x['file']} | {x['row']} | {x['site']} | {x['vault']} |")
    w('')
    w('## 8. Narrative (hand-written, see NARRATIVE.md)')
    w('')
    nar = os.path.join(HERE, 'NARRATIVE.md')
    if os.path.exists(nar):
        w(open(nar, encoding='utf-8').read())
    else:
        w('_NARRATIVE.md not present._')
    open(os.path.join(HERE, 'RECONCILIATION_REPORT.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


def score_cell(c):
    if c['effective'] == 'site_broader':
        return {('S', 'M'): 100, ('S', 'N'): 100, ('M', 'N'): 80}.get((c['site_eff'], c['vault_eff']), 60) + (10 if c['level'] in ('EMR', 'EMT') else 0)
    if c['effective'] == 'site_narrower':
        return {('M', 'S'): 70, ('N', 'S'): 70, ('N', 'M'): 50}.get((c['site_eff'], c['vault_eff']), 40)
    return 0



if __name__ == '__main__':
    main()
