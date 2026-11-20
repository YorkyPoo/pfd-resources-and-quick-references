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
import html as html_lib
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
    # Batch 3 — protocols/respiratory/. Derived from the tree: every .md file in that
    # directory (9 pages), nothing hand-picked.
    'protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.md',
    'protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md',
    'protocols/respiratory/03_Pediatric_Stridor_PROC.md',
    'protocols/respiratory/03_Pneumothorax_PROC.md',
    'protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md',
    'protocols/respiratory/03_Respiratory_Arrest_PROC.md',
    'protocols/respiratory/03_Respiratory_Distress_PROC.md',
    'protocols/respiratory/03_Smoke_Inhalation_PROC.md',
    'protocols/respiratory/03_Upper_Airway_Obstruction_PROC.md',
    # Batch 4 — protocols/trauma/ + protocols/toxicology/. Derived from the tree: every
    # .md file in those two directories (6 trauma + 3 toxicology = 9 pages), nothing
    # hand-picked. The card estimated 8; the tree says 9.
    'protocols/trauma/09_Burns_Thermal_PROC.md',
    'protocols/trauma/09_Crush_Syndrome_PROC.md',
    'protocols/trauma/09_Electrical_Injuries_PROC.md',
    'protocols/trauma/09_Hemorrhage_Control_PROC.md',
    'protocols/trauma/09_Lightning_Injuries_PROC.md',
    'protocols/trauma/09_Trauma_PROC.md',
    'protocols/toxicology/06_Nausea_Vomiting_PROC.md',
    'protocols/toxicology/06_Nerve_Agents_PROC.md',
    'protocols/toxicology/06_Overdose_Poisoning_PROC.md',
    # Batch 5 — protocols/general/. Derived from the tree: `grep -l 'class="sc-wrap"'
    # docs/protocols/general/*.md` returns exactly these 6 pages, nothing hand-picked.
    # protocols/medical/07_Hypotension_Shock_Non_Trauma_PROC.md is the seventh page the
    # card names; it was already converted in Batch 2 and is listed above. Its two
    # remaining `sc-wrap` blocks are the Norepinephrine and Epinephrine DRIP CHARTS (a Dose
    # column and a Drops-per-minute column), not level matrices — there is no action row to
    # chip, so they stay sc-wrap. See the Batch 5 ledger note.
    'protocols/general/02_Behavioral_Patient_Restraint_PROC.md',
    'protocols/general/02_Cold_Exposure_PROC.md',
    'protocols/general/02_Diving_and_Drowning_Emergencies_PROC.md',
    'protocols/general/02_Heat_Exposure_PROC.md',
    'protocols/general/02_Pain_Control_PROC.md',
    'protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.md',
    # Batch 6 — front-matter/Universal Patient Care.md. It is a PEMS 2024 PROTOCOL
    # (p.49-50, every row level-badged), not an administrative policy, so it is converted
    # with the ordinary chip chassis; its second `sc-wrap` block is a 3-column
    # HPI / Signs / Differential table with no action rows and stays untouched.
    'protocols/front-matter/Universal Patient Care.md',
    # Batch 7 — docs/procedures/. Derived from the tree: `grep -l 'class="sc-wrap"'
    # docs/procedures/*.md` returns 15 files, of which 13 carry the 7-column
    # provider-level matrix; `Medical_Devices_Pumps.md` is a 2-column
    # Device | Action table (no level column) and `Vaccination.md` has no table at
    # all, so neither is a target. Nothing hand-picked: the 13 are the pages whose
    # header is the level matrix. PEMS 2024 prints each of them as a PROCEDURE in
    # its p.231-275 section, with one badge per row.
    'procedures/CPAP.md',
    'procedures/Capnography.md',
    'procedures/Chest_Decompression.md',
    'procedures/Endotracheal_Intubation.md',
    'procedures/Intraosseous_Access.md',
    'procedures/Medication_Administration.md',
    'procedures/Nasogastric_Tube.md',
    'procedures/Neonatal_Resuscitation.md',
    'procedures/Spinal_Motion_Restriction.md',
    'procedures/Surgical_Airway.md',
    'procedures/Taser_Barb_Removal.md',
    'procedures/Tourniquet_Application.md',
    'procedures/Transcutaneous_Pacing.md',
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
              'PENDING': 'pending', 'POLICY': 'policy'}
PENDING_YAML = os.path.join(AUD, 'pending-protocols.yaml')
PENDING_CHIP = '<span class="lvl lvl-pending">PENDING</span>'

# ----------------------------------------------------------------- POLICY class
# The owner's ruling on administrative pages (2026-11-16): "Treat admin pages as policy:
# cite PEMS administrative policies where they exist, PENDING where the policy is ours."
#
# A POLICY row's authority is one of the 14 PEMS 2024 ADMINISTRATIVE POLICIES (the p.9
# table of contents), not a protocol row: PEMS prints those rules as policy prose, and the
# existing exceptions.yaml already declares these pages `kind: administrative` — "not
# level-gated". So on these pages a row is either
#   * POLICY  — printed in a PEMS administrative policy, cited by policy id + a verbatim
#               quote out of that policy's own pages, or
#   * PENDING — not printed in any PEMS administrative policy; the rule is the agency's.
# The POLICY chip is deliberately NOT a provider level: no badge can be inferred from a
# policy, so none is published.
POLICY_YAML = os.path.join(AUD, 'pems-policies.yaml')
POLICY_SOURCE = os.path.join(ROOT, 'pems_chunks', 'PEMS2024_full.txt')
POLICY_CHIP = '<span class="lvl lvl-policy">POLICY</span>'
POLICY_HEADER = '| # | Basis | Action / Intervention |'
DIV_POLICY_OPEN = '<div class="lv-wrap policy" markdown="1">'
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
    if 'Basis' in line:
        # an administrative-policy page: the column carries POLICY/PENDING, not a level
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
        # consume EVERY trailing note paragraph, not just one: a page can carry several
        # (POLICY / PENDING / flagged-row notes), and a run must replace all of them or
        # they accumulate.
        while q < n and lines[q].startswith('<p class="lv-note">'):
            r = q
            while r < n and '</p>' not in lines[r]:
                r += 1
            end = r
            q = end + 1
            while q < n and lines[q].strip() == '':
                q += 1
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
def load_verifier_exceptions():
    """Leaks the canonical PEMS table carries, documented in verifier-exceptions.yaml.

    The verifier (scripts/verify_pems_canonical.py) fails on any leak not listed here
    and on a listed leak that has stopped leaking, so the list is enforced, not a note.
    """
    import yaml
    path = os.path.join(AUD, 'verifier-exceptions.yaml')
    if not os.path.exists(path):
        return []
    doc = yaml.safe_load(open(path, encoding='utf-8')) or {}
    return doc.get('leaks') or []


def load_json(name):
    with open(os.path.join(AUD, name), encoding='utf-8') as fh:
        return json.load(fh)


RULINGS_YAML = os.path.join(AUD, 'level-rulings.yaml')
BINDINGS_YAML = os.path.join(AUD, 'row-bindings.yaml')
WORDING_YAML = os.path.join(AUD, 'wording-rulings.yaml')
STYLESHEET_YAML = os.path.join(AUD, 'stylesheet-changes.yaml')



def policy_pages_text(pages):
    """Verbatim PEMS 2024 text of the given pages, page markers excluded."""
    keep, cur = [], None
    with open(POLICY_SOURCE, encoding='utf-8') as fh:
        for line in fh:
            m = re.match(r'--- PAGE (\d+) ---', line)
            if m:
                cur = int(m.group(1))
                continue
            if cur in pages:
                keep.append(line)
    return '\n'.join(keep)


def load_policies():
    """The PEMS 2024 administrative policies the site may cite, keyed by id.

    Validated loudly, and self-verifying: the recorded quote must be a verbatim span of
    the pages the entry claims, read out of pems_chunks/PEMS2024_full.txt. A policy that
    the source does not print cannot be cited, exactly as a protocol citation cannot rest
    on prose the cited row does not print.
    """
    import yaml
    if not os.path.exists(POLICY_YAML):
        return {}
    doc = yaml.safe_load(open(POLICY_YAML, encoding='utf-8')) or {}
    out = {}
    for rec in doc.get('policies') or []:
        missing = [k for k in ('id', 'title', 'pages', 'effective', 'quote')
                   if rec.get(k) in (None, '', [])]
        if missing:
            raise SystemExit(f'pems-policies.yaml: entry {rec!r} is missing {missing}')
        if not isinstance(rec['pages'], list) or not all(isinstance(p, int) for p in rec['pages']):
            raise SystemExit(f'pems-policies.yaml: {rec["id"]} pages must be a list of ints')
        text = norm_quote(policy_pages_text(set(rec['pages'])))
        if norm_quote(rec['quote']) not in text:
            raise SystemExit(f'pems-policies.yaml: {rec["id"]} quote is not a verbatim span '
                             f'of PEMS pages {rec["pages"]} — the policy citation does not '
                             f'rest on the source\'s own words')
        if rec['id'] in out:
            raise SystemExit(f'pems-policies.yaml: {rec["id"]} listed twice')
        out[rec['id']] = rec
    return out


_POLICY_CACHE = {}


def policies():
    """Cached `load_policies()` — read once per process."""
    if not _POLICY_CACHE:
        _POLICY_CACHE.update(load_policies())
    return _POLICY_CACHE


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


RELOCATED_YAML = os.path.join(AUD, 'relocated-rows.yaml')
SPLITS_YAML = os.path.join(AUD, 'row-splits.yaml')


def load_relocated():
    """Rows moved OUT of an action table into the page's References & Good Practice block.

    Owner instruction 2026-11-20: guidance that PEMS prints as instruction to the provider
    — scene management, recognition, preparation, assessment — is not a numbered action and
    must not be given a level of our own invention. It moves below the table as prose and
    keeps no chip and no flag.

    A relocated row is still on the page, but it is no longer a chipped action row, so the
    ledger cannot see it any more. This record keeps two things honest: the row's pre-move
    status (so the ledger's historical "flagged before" count does not quietly shrink) and,
    via `proves`, proof that the block the record describes is actually printed on the page.
    """
    import yaml
    if not os.path.exists(RELOCATED_YAML):
        return []
    doc = yaml.safe_load(open(RELOCATED_YAML, encoding='utf-8')) or {}
    out = []
    for rec in doc.get('relocated') or []:
        need = ('file', 'row', 'where', 'proves')
        missing = [k for k in need if rec.get(k) in (None, '', [])]
        if missing:
            raise SystemExit(f'relocated-rows.yaml: entry {rec!r} is missing {missing}')
        if not rec.get('guidance') and rec.get('level') in (None, ''):
            raise SystemExit(f'relocated-rows.yaml: {rec["file"]} row {rec["row"]} has no '
                             f'`level` — a relocated ACTION records the level it carried; '
                             f'guidance prose that carries no level sets `guidance: true`')
        if rec.get('guidance') and rec.get('level') not in (None, ''):
            raise SystemExit(f'relocated-rows.yaml: {rec["file"]} row {rec["row"]} is marked '
                             f'`guidance: true` and still states a level — instruction to the '
                             f'provider carries no provider level')
        out.append(rec)
    return out


def relocated_proofs_missing(rec):
    """The `proves` spans of one relocated row that its page does NOT print."""
    path = os.path.join(DOCS, rec['file'])
    if not os.path.exists(path):
        return ['(page file missing)']
    text = open(path, encoding='utf-8').read()
    return [span for span in rec['proves'] if span not in text]


def load_site_splits():
    """`site_splits:` — the durable record of a bundled action row split into sub-rows.

    `row-splits.yaml` has two disjoint sections. `splits:` records a repair of the PDF
    extraction (one printed cell's lines handed to the next badge); it is checked by
    `pems_canonical.py` / `verify_pems_canonical.py` and is untouched by this pass.
    `site_splits:` records the owner's row-structure ruling of 2026-11-20: a site row that
    bundled several actions is split into one action per row, each part carrying the level
    of the PEMS row that prints it. A bundled row cannot carry one level without over- or
    under-granting half of itself — that is why these rows were flagged OWNER_REQUIRED.

    Numbering: the first part keeps the original number and the rest are lettered (`8`,
    `8a`, `8b`), so the row number stays the audit key bound to its PEMS citation and no
    downstream citation shifts. Each part must name the PEMS row it cites; the level is
    never typed here as the authority — it is what that row prints, and `--check` compares
    the two.
    """
    import yaml
    if not os.path.exists(SPLITS_YAML):
        return []
    doc = yaml.safe_load(open(SPLITS_YAML, encoding='utf-8')) or {}
    out = []
    for rec in doc.get('site_splits') or []:
        need = ('file', 'row', 'reason', 'parts')
        missing = [k for k in need if rec.get(k) in (None, '', [])]
        if missing:
            raise SystemExit(f'row-splits.yaml site_splits: entry {rec!r} is missing {missing}')
        parts = rec['parts']
        if not isinstance(parts, list) or len(parts) < 2:
            raise SystemExit(f'row-splits.yaml site_splits: {rec["file"]} row {rec["row"]} '
                             f'must list at least two parts')
        want = [str(rec['row'])] + [f'{rec["row"]}{chr(97 + i)}' for i in range(len(parts) - 1)]
        got = [str(p.get('row')) for p in parts]
        if got != want:
            raise SystemExit(f'row-splits.yaml site_splits: {rec["file"]} row {rec["row"]} '
                             f'parts are numbered {got}, expected {want} — the first part '
                             f'keeps the original number and the rest are lettered')
        for p in parts:
            miss = [k for k in ('row', 'level', 'pems', 'text') if p.get(k) in (None, '', [])]
            if miss:
                raise SystemExit(f'row-splits.yaml site_splits: {rec["file"]} row '
                                 f'{rec["row"]} part {p.get("row")} is missing {miss}')
            if p['level'] not in LV + ['MC']:
                raise SystemExit(f'row-splits.yaml site_splits: {rec["file"]} part '
                                 f'{p["row"]} level {p["level"]!r} is not a provider level')
            src = p.get('source')
            if src not in ('cited', 'ruling', 'owner_required'):
                raise SystemExit(f'row-splits.yaml site_splits: {rec["file"]} part '
                                 f'{p["row"]} has source {src!r} — it must say `cited` (a '
                                 f'printed PEMS badge), `ruling` (a recorded owner decision) '
                                 f'or `owner_required` (the source scopes the action in a '
                                 f'row badged for another clause, so the level is an open '
                                 f'decision and the part is flagged, not cited)')
        out.append(rec)
    return out


def norm_row_text(text):
    """A row's action as compared by the split check: markup, links and spacing folded."""
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', str(text or ''))
    text = text.replace('**', '').replace('<br>', ' ').replace('<br/>', ' ')
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html_lib.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()


def load_rulings():
    """Owner rulings keyed (file, row). A ruling is a decision, never a source citation.

    A ruling may record EVIDENCE that PEMS prints the action without badgeing it:

      prose_citations: [{page, heading, ordinal, quote}]  a PEARLS / NOTES /
          CONTRAINDICATIONS / INDICATIONS / CRITERIA entry (pems_prose.json). Verified
          verbatim by --check, exactly like a quoted row.
      level_from: {page, ordinal}  a printed, level-badged row whose badge IS the ruled
          level (e.g. the CPAP procedure rows badge EMT for the contraindications the
          page lists). Verified: the chip must equal that row's printed badge.

    Neither field makes the level a PEMS citation: the level is still the owner's scope
    decision (see the file header), and the ledger keeps reporting it as `owner_ruled`.

    `level: FLOOR` is the one derived level: it means "the lowest chip this page itself
    carries", computed by page_floor() from the page, never typed.
    """
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
        if rec['level'] != 'FLOOR' and rec['level'] not in LV + ['MC']:
            raise SystemExit(f'level-rulings.yaml: {rec["file"]} row {rec["row"]} has level '
                             f'{rec["level"]!r} — it must be a provider level, MC, or FLOOR')
        cites = rec.get('prose_citations')
        if cites is not None:
            if not isinstance(cites, list):
                raise SystemExit(f'level-rulings.yaml: {rec["file"]} row {rec["row"]} '
                                 f'prose_citations must be a list')
            for c in cites:
                if not isinstance(c, dict) or not all(
                        c.get(k) not in (None, '') for k in ('page', 'heading', 'ordinal',
                                                             'quote')):
                    raise SystemExit(f'level-rulings.yaml: {rec["file"]} row {rec["row"]} '
                                     f'has a prose citation without page/heading/ordinal/'
                                     f'quote: {c!r}')
        lf = rec.get('level_from')
        if lf is not None:
            if not isinstance(lf, dict) or lf.get('page') is None or lf.get('ordinal') is None:
                raise SystemExit(f'level-rulings.yaml: {rec["file"]} row {rec["row"]} '
                                 f'level_from must name page + ordinal')
        ans = rec.get('answered')
        if ans is not None:
            if not isinstance(ans, dict) or not all(
                    ans.get(k) not in (None, '') for k in ('date', 'level', 'quote')):
                raise SystemExit(f'level-rulings.yaml: {rec["file"]} row {rec["row"]} '
                                 f'`answered` must carry date + level + quote (the owner\'s '
                                 f'words) — a question is only closed by a recorded answer')
            if ans['level'] != rec['level']:
                raise SystemExit(f'level-rulings.yaml: {rec["file"]} row {rec["row"]} is '
                                 f'`answered` {ans["level"]!r} but its `level` is '
                                 f'{rec["level"]!r} — an answer that changes the level must '
                                 f'be the level the ruling records')
        out[(rec['file'], str(rec['row']))] = rec
    return out


def load_bindings():
    """Row-level citations / owner_required declarations, keyed (file, row).

    Validated loudly: a binding must name an existing-kind PEMS pointer and may never
    state a level; an owner_required must carry a reason.

    Two newer, also machine-checked fields:

      cross_page: true   this citation reaches off the page's own governing PEMS source
                         (the owner's 2026-11-16 ruling: an action printed in another
                         protocol/procedure may be cited there). It requires `evidence`
                         AND `quoted_row_text`, the verbatim span from the cited row that
                         is the action. The checker re-reads that span out of
                         pems_table.json, so a citation cannot be justified by prose that
                         the source does not print.
      mc_required: true  the page printed this row's level cell in brackets — that level
                         performs the action only with Medical Control authorisation. The
                         page renders the level chip plus a distinct `+MC` marker, and
                         `--check` fails if that marker is missing or doubled.

    An entry may carry `mc_required` without a citation (a row that stays
    owner_required) and a citation without `mc_required`.
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
        mc = rec.get('mc_required')
        # --- POLICY citation: the rule is printed in a PEMS administrative policy -------
        pol_id = rec.get('policy')
        if pol_id:
            pol = policies().get(pol_id)
            if pol is None:
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} cites '
                                 f'policy {pol_id!r}, which is not in '
                                 f'audit/level-scan/pems-policies.yaml — a policy citation '
                                 f'must name a policy PEMS 2024 publishes')
            if rec.get('pems_page') is not None or rec.get('pems_ordinal') is not None:
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} is a '
                                 f'POLICY row and also names pems_page '
                                 f'{rec.get("pems_page")!r}/pems_ordinal '
                                 f'{rec.get("pems_ordinal")!r} — an administrative-policy '
                                 f'row may not also carry a protocol citation')
            if status not in (None, 'bound'):
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} cites a '
                                 f'policy and also declares status {status!r}')
            q = str(rec.get('policy_quote') or '').strip()
            if not q:
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} cites '
                                 f'policy {pol_id!r} without policy_quote — the policy\'s own '
                                 f'words are the only proof it prints the rule')
            if norm_quote(q) not in norm_quote(policy_pages_text(set(pol['pages']))):
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]}: '
                                 f'policy_quote is not a verbatim span of {pol_id} '
                                 f'(PEMS p.{"/".join(str(p) for p in pol["pages"])}) — the '
                                 f'citation does not rest on the source\'s own words')
            key = (rec['file'], str(rec['row']))
            if key in out:
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} listed twice')
            out[key] = rec
            continue
        if mc is not None and not isinstance(mc, bool):
            raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} has '
                             f'mc_required={mc!r} — it must be true or false')
        if mc and not str(rec.get('evidence') or '').strip():
            raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} declares '
                             f'mc_required without evidence — say which bracketed page '
                             f'cell this marker carries')
        if status == 'owner_required':
            if not rec.get('reason'):
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} is '
                                 f'owner_required without a reason')
            if rec.get('pems_page') is not None:
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} is '
                                 f'owner_required but names pems_page '
                                 f'{rec["pems_page"]!r} — a row that cannot be cited may '
                                 f'not carry a citation')
        elif status not in (None, 'bound'):
            raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} has unknown '
                             f'status {status!r}')
        elif (mc or str(rec.get('mc_bracket_excluded') or '').strip()) \
                and rec.get('pems_page') is None:
            pass  # a marker-only entry: the row keeps whatever citation it already has
        elif rec.get('pems_page') is None or rec.get('pems_ordinal') is None:
            raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} is a binding '
                             f'without pems_page/pems_ordinal')
        if rec.get('cross_page') not in (None, True, False):
            raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} has '
                             f'cross_page={rec.get("cross_page")!r} — it must be true or false')
        if 'flag' in rec:
            # a CORRECTED row: the citation gives the chip, and the flag is what keeps
            # the correction visible. It is not a second level and not an owner_required
            # declaration (which is for a row PEMS does not badge at all).
            if not str(rec.get('flag') or '').strip():
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} has an '
                                 f'empty `flag` — say what the reader must be told')
            if rec.get('pems_page') is None or rec.get('pems_ordinal') is None:
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} declares '
                                 f'a `flag` without a citation — a flagged correction must '
                                 f'still cite the level it was corrected to')
            if status == 'owner_required':
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} is both '
                                 f'owner_required and `flag`ged — a row PEMS does not badge '
                                 f'cannot carry a corrected source level')
        rat = rec.get('ratified')
        if rat is not None:
            # An owner-ratified correction: the flag record stays (it is the audit trail),
            # but the on-page marker is retired. Only a `flag`ged correction may be
            # ratified — there is nothing to ratify on a row that was never corrected.
            if 'flag' not in rec:
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} has a '
                                 f'`ratified` record but no `flag` — only a corrected '
                                 f'correction can be ratified')
            if not isinstance(rat, dict):
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} has '
                                 f'ratified={rat!r} — it must be a mapping')
            for k in ('date', 'by', 'ruling'):
                if not str(rat.get(k) or '').strip():
                    raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} '
                                     f'ratified record has no {k} — the record must say who '
                                     f'ratified the correction, when, and in what words')
            if rat.get('marker') != 'retired':
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} '
                                 f'ratified.marker is {rat.get("marker")!r} — it must be '
                                 f'"retired" (a ratified correction keeps its record and '
                                 f'drops its marker)')
            if rec.get('pems_page') is None or rec.get('pems_ordinal') is None:
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} is '
                                 f'ratified without a citation — the record must still name '
                                 f'the printed page that authorised the chip')
        if rec.get('cross_page'):
            if not str(rec.get('evidence') or '').strip():
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} is a '
                                 f'cross_page citation without evidence')
            if not str(rec.get('quoted_row_text') or '').strip():
                raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} is a '
                                 f'cross_page citation without quoted_row_text — the cited '
                                 f"row's own words are the only proof it prints the action")
        key = (rec['file'], str(rec['row']))
        if key in out:
            raise SystemExit(f'row-bindings.yaml: {rec["file"]} row {rec["row"]} listed twice')
        out[key] = rec
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


def load_row_pending():
    """Row-level pending: one agency-added action on an otherwise PEMS-cited page.

    Keyed (file, row) -> {"carried_from_page", "reason"}. Validated loudly and for the
    same reason a whole-page entry is: a PENDING row is a row nobody has authorized, so
    it may not name a PEMS row, it may not be silent about why, and it must record the
    level the page published before conversion so the provenance can be checked against
    the ledger instead of believed.
    """
    import yaml
    if not os.path.exists(PENDING_YAML):
        return {}
    doc = yaml.safe_load(open(PENDING_YAML, encoding='utf-8')) or {}
    whole = {rec.get('file') for rec in doc.get('protocols') or []}
    out = {}
    for rec in doc.get('rows') or []:
        rel = rec.get('file')
        if not rel:
            raise SystemExit(f'pending-protocols.yaml: row-level entry without a file: {rec!r}')
        if rel in whole:
            raise SystemExit(f'pending-protocols.yaml: {rel} is listed both whole-page and '
                             f'row-level — a pending page has no PEMS row to spare')
        for k in ('pems_page', 'pems_ordinal', 'pems_badge', 'pems_text'):
            if rec.get(k) is not None:
                raise SystemExit(f'pending-protocols.yaml: {rel} row-level entry states {k} — '
                                 f'a pending row may not claim a PEMS citation')
        if not rec.get('rows'):
            raise SystemExit(f'pending-protocols.yaml: {rel} has a row-level entry with no rows')
        for ent in rec['rows']:
            if ent.get('row') is None:
                raise SystemExit(f'pending-protocols.yaml: {rel} has a row entry without a row '
                                 f'number: {ent!r}')
            for k in ('pems_page', 'pems_ordinal', 'pems_badge', 'pems_text'):
                if ent.get(k) is not None:
                    raise SystemExit(f'pending-protocols.yaml: {rel} row {ent["row"]} states '
                                     f'{k} — a pending row may not claim a PEMS citation')
            for k in ('reason', 'carried_from_page'):
                if not str(ent.get(k) or '').strip():
                    raise SystemExit(f'pending-protocols.yaml: {rel} row {ent["row"]} has no '
                                     f'{k}')
            key = (rel, str(ent['row']))
            if key in out:
                raise SystemExit(f'pending-protocols.yaml: {rel} row {ent["row"]} listed twice')
            out[key] = {'carried_from_page': str(ent['carried_from_page']).strip().upper(),
                        'reason': str(ent['reason']).strip(),
                        'note': str(ent.get('note') or '').strip() or None}
    return out


def row_pending_note(spec_rows):
    """The note a page carries when some of its rows are agency additions.

    Says what PENDING means here, row by row, and says how it differs from the
    whole-page ODEMSA case — a paramedic reading a Stroke page must not think the
    whole protocol has lost its source.
    """
    label = ('row ' + spec_rows[0] if len(spec_rows) == 1
             else 'rows ' + ', '.join(spec_rows))
    return ('<strong>PENDING</strong> — ' + label + ': this action has no counterpart in '
            'PEMS 2024. It is an agency addition, so the level it used to show was never '
            'verified against the regional source and is not published as a level now. '
            'Every other action listed is cited to its PEMS 2024 row. This is not the '
            'same case as a whole protocol sourced outside PEMS (e.g. Aortic Dissection, '
            'which comes from ODEMSA and is PENDING on every row): in this case only the '
            'action(s) named are pending, and the rest of the protocol stands on PEMS. '
            '<strong>Pending OMD authorization</strong> — no provider level applies until '
            'the OMD authorizes it.')


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


EXCEPTIONS_YAML = os.path.join(AUD, 'exceptions.yaml')


def sc_wrap_audit():
    """Every docs/ page that still carries an `sc-wrap` block, and whether it is a level
    matrix. `sc-wrap` is the shared wide-table wrapper, so its presence is NOT a defect —
    a provider-level matrix still wrapped in `sc-wrap` is. Derived by walking docs/, not
    from a list."""
    # Two header spellings are level matrices: the pre-2026-11-20 `EMR | EMT | A | I | P`
    # columns, and the owner-ruled `R | B | A | I | P` relabel that replaced them on the
    # front-matter legend. Detecting only the old one made the legend invisible to this
    # audit the moment its labels changed — a silent pass is exactly what this check exists
    # to prevent.
    header = re.compile(r'^\|\s*#\s*\|\s*Action\s*/\s*Intervention\s*\|\s*(?:EMR|R)\s*\|')
    files, blocks, matrices = [], [], []
    for root, _dirs, names in os.walk(DOCS):
        for name in sorted(names):
            if not name.endswith('.md'):
                continue
            path = os.path.join(root, name)
            rel = os.path.relpath(path, DOCS).replace(os.sep, '/')
            lines = open(path, encoding='utf-8').read().split('\n')
            n = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('<div class="sc-wrap'):
                    n += 1
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith('</div>'):
                        if header.match(lines[j]):
                            matrices.append(f'{rel} (line {j + 1})')
                            break
                        j += 1
            if n:
                files.append(rel)
                blocks.append(n)
    return files, sum(blocks), matrices


def policy_targets():
    """The administrative-policy pages, derived — every exceptions.yaml entry whose
    `kind` is `administrative`. Never a hand-picked list: the file already declares
    which pages are policy rather than clinical procedure."""
    import yaml
    if not os.path.exists(EXCEPTIONS_YAML):
        return []
    doc = yaml.safe_load(open(EXCEPTIONS_YAML, encoding='utf-8')) or {}
    return [rec['file'] for rec in doc.get('pages') or []
            if rec.get('kind') == 'administrative' and rec.get('file')]


def governing_pages(rel, align):
    """The PEMS page(s) that are this site page's own source.

    Two recorded inputs, no guessing: the page-level `pems_pages` override in
    audit/level-scan/exceptions.yaml, and every row alignment.json matched to the page's
    own title/section. A citation outside this set is a *cross-page* citation and must
    say so (`cross_page: true`) with the cited row's words quoted.
    """
    import yaml
    pages = set()
    if os.path.exists(EXCEPTIONS_YAML):
        doc = yaml.safe_load(open(EXCEPTIONS_YAML, encoding='utf-8')) or {}
        for rec in doc.get('pages') or []:
            if rec.get('file') == rel:
                for p in rec.get('pems_pages') or []:
                    pages.add(int(p))
    page = next((p for p in align['pages'] if p['site_page'] == rel), None)
    for r in (page or {}).get('rows', []):
        if r.get('status') == 'matched' and r.get('pems_page') is not None:
            pages.add(int(r['pems_page']))
    if not pages:
        raise SystemExit(f'{rel}: no governing PEMS page could be derived (exceptions.yaml '
                         f'pems_pages and alignment.json both empty) — cross-page citation '
                         f'cannot be judged without it')
    return pages


def norm_quote(text):
    """Text folded the way the quote check compares it: case, dashes, bullets, markup."""
    text = (text or '').lower()
    for a, b in (('\u2013', '-'), ('\u2014', '-'), ('\u2019', "'"), ('\u201c', '"'),
                 ('\u201d', '"'), ('\u2022', ' '), ('\u2011', '-'), ('\u00a0', ' '), ('*', '')):
        text = text.replace(a, b)
    text = re.sub(r'[^a-z0-9%.\- ]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def quote_in(quote, row):
    """True when `quote` is a verbatim span of the cited PEMS row's printed text."""
    return bool(row) and norm_quote(quote) in norm_quote(row.get('verbatim_text'))


# ---------------------------------------------------------------- unbadged prose
# PEMS prints clinical instruction in PEARLS / NOTES / CONTRAINDICATIONS / INDICATIONS /
# CRITERIA blocks as well as in level-badged grid rows. `GRID_STOP` in pems_canonical.py
# deliberately ends the table at those headings, so a row whose action PEMS prints only as
# prose can never be cited to a table row: it is cited to the prose index instead
# (audit/level-scan/pems_prose.json, built by scripts/build_pems_prose.py). A prose
# citation names page + heading + ordinal and quotes that entry's own words, so it is
# checkable exactly like a row citation and cannot rest on free text.
def load_prose():
    try:
        return load_json('pems_prose.json')
    except FileNotFoundError:
        raise SystemExit('audit/level-scan/pems_prose.json is missing — run '
                         'scripts/build_pems_prose.py to rebuild the unbadged-prose '
                         'index; a citation to prose cannot be verified without it')


def prose_entry(index, page, heading, ordinal):
    """The index entry for (page, heading, ordinal), or None."""
    for e in (index.get('pages') or {}).get(str(page), []):
        if (str(e.get('heading') or '').upper() == str(heading or '').upper()
                and int(e.get('ordinal')) == int(ordinal)):
            return e
    return None


def prose_quote_in(quote, entry):
    """True when `quote` is a verbatim span of the prose entry's printed text."""
    return bool(entry) and norm_quote(quote) in norm_quote(entry.get('text'))


def check_prose_citations(rel, label, cites, index, fails):
    """Verify a `prose_citations:` list; returns the resolved list for the ledger.

    Every citation must name page + heading + ordinal that exist in the index AND quote
    a verbatim span of that entry. No free-text citation passes.
    """
    if cites is None:
        return []
    if not isinstance(cites, list) or not cites:
        fails.append(f'{rel} {label}: prose_citations must be a non-empty list')
        return []
    out = []
    for c in cites:
        missing = [k for k in ('page', 'heading', 'ordinal', 'quote') if c.get(k) in (None, '')]
        if missing:
            fails.append(f'{rel} {label}: prose citation without {"/".join(missing)} — a '
                         f'citation names page + heading + ordinal and quotes the text')
            continue
        entry = prose_entry(index, c['page'], c['heading'], c['ordinal'])
        if entry is None:
            fails.append(f'{rel} {label}: prose citation p.{c["page"]} {c["heading"]} '
                         f'#{c["ordinal"]} is not in pems_prose.json')
            continue
        if not prose_quote_in(c['quote'], entry):
            fails.append(f'{rel} {label}: the quote is not a verbatim span of p.{c["page"]} '
                         f'{c["heading"]} #{c["ordinal"]}')
            continue
        out.append({'page': int(c['page']), 'heading': str(c['heading']).upper(),
                    'ordinal': int(c['ordinal']), 'quote': c['quote'],
                    'text': entry['text']})
    return out


def page_floor(rel):
    """The lowest provider level this page itself chips, read out of the file.

    A ruling may take the page's own BLS floor as its level (owner's Pearl ruling
    2026-11-17: a BLS-scope action carries the page's floor, not the level its old
    matrix happened to publish). The floor is DERIVED here — never typed into the yaml,
    never guessed — and the derivation is printed by the caller.
    """
    lines = open(os.path.join(DOCS, rel), encoding='utf-8').read().split('\n')
    chips, rows_seen = [], []
    for reg in find_regions(lines):
        for row in reg['rows']:
            if is_banner(row):
                continue
            rows_seen.append(row['ordinal'])
            m = CHIP_RE.search(row['level_cell'] or '')
            if m and m.group(2) in LV:
                chips.append(m.group(2))
    if not chips:
        raise SystemExit(f'{rel}: a page floor was requested but the page carries no '
                         f'provider chip — cannot derive one')
    return min(chips, key=LV.index), chips, rows_seen




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


def row_key(ordinal):
    """A table row's ledger key: an int for a plain number, the string for a lettered one.

    Splitting a bundled action (owner ruling 2026-11-20) keeps the original number on the
    first sub-row and letters the rest (`8`, `8a`, `8b`) so the row number stays the audit
    key it always was and no downstream citation shifts. A lettered sub-row therefore has a
    string key; everything that only indexed numeric rows must go through this.
    """
    s = str(ordinal).strip()
    return int(s) if s.isdigit() else s


def compound_tokens(row, span=None):
    """Inline level tokens inside the PEMS row text, e.g. '(I / P)' or '[EMR]'.

    PEMS prints ONE badge per row but sometimes scopes a clause to another level in the
    text. Such a row cannot be reproduced as a single chip without contradicting either
    the badge or the row's own wording.

    `span` is the clause a binding quotes as the words this site row publishes
    (`quoted_row_text`). On a split row that clause is only part of the compound PEMS row,
    so a token OUTSIDE it cannot contradict this row's chip — the half it scoped is now a
    row of its own with its own citation. Only a token inside the published clause counts.
    """
    if not row:
        return []
    text = row.get('verbatim_text') or ''
    if span:
        text = str(span)
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
            if b.get('mc_required'):
                extra['mc_required'] = True
                extra['mc_evidence'] = b.get('evidence')
            if b.get('pems_page') is not None:
                ptr, basis = (b['pems_page'], b['pems_ordinal']), 'row-bindings:bound'
                extra['binding_evidence'] = b.get('evidence')
                extra['cross_page'] = bool(b.get('cross_page'))
                extra['quoted_row_text'] = b.get('quoted_row_text')
            if b.get('status') == 'owner_required':
                extra['forced_owner'] = b['reason']
                extra['owner_note'] = b.get('owner_note')
            if b.get('flag'):
                # a corrected row: the chip is the source badge, but the row's level
                # changed under an owner ruling and the page must keep saying so —
                # unless the owner has ratified the correction and retired the marker
                # (then the record above stays in the ledger and the marker does not)
                extra['flag'] = b['flag']
                extra['ratified'] = b.get('ratified')

        source_row = pems.get(ptr) if ptr else None
        badge, bracketed = badge_of(source_row) if source_row else (None, False)
        out.append({'ordinal': ordinal, 'ptr': ptr, 'basis': basis, 'badge': badge,
                    'bracketed': bracketed, 'pems_row': source_row, 'extra': extra,
                    'adjudicated': rec, 'resolved': resolved_cite})
    return out


# ------------------------------------------------------------------- rendering
MC_REQ_MARK = ('<span class="lvl lvl-mc-req" title="this level performs the action only '
               'with Medical Control authorisation (PEMS prints the level cell in '
               'brackets)">+MC</span>')


def chip(level, bracketed=False, owner=False, mc_required=False, flag=None):
    html = f'<span class="lvl lvl-{CHIP_CLASS.get(level, "na")}">{level}</span>'
    if mc_required:
        # A second marker, not a second level: the level still grants the skill, the
        # bracketed page cell said the level needs Medical Control to authorise it. Kept
        # deliberately distinct from the `MC` chip, which means the action *is* a Medical
        # Control contact.
        html += MC_REQ_MARK
    if bracketed:
        html += ('<sup class="lvl-req" title="PEMS 2024 prints this badge in brackets: agency '
                 'training documentation and Medical Control written authorization required">*</sup>')
    if owner:
        # Page voice (owner ruling 2026-11-20): the marker's tooltip is reader text. No
        # audit vocabulary, no ledger/file reference, no self-reference to the table.
        html += ('<sup class="lvl-own" title="Provider level for this action is awaiting a '
                 'Medical Control decision">&#9873;</sup>')
    if flag:
        # A corrected row: the chip IS the level PEMS prints (so this is not
        # OWNER_REQUIRED), but the row carried a different level until the owner ruled
        # on it and the owner asked for that history to stay visible on the page.
        # The tooltip is reader text: markdown bold is stripped, quotes escaped.
        title = html_lib.escape(re.sub(r'\*\*(.+?)\*\*', r'\1', str(flag)), quote=True)
        html += f'<sup class="lvl-fix" title="{title}">&#9873;</sup>'
    return html


def render_block(rows, note=None, banner=None, header=NEW_HEADER, div_open=DIV_OPEN):
    out = []
    if banner:
        out += [banner, '']
    out += [div_open, '', header, '|:---:|---|---|']
    for r in rows:
        cell = r.get('level_cell') or chip(r['level'], r.get('bracketed', False),
                                           r.get('owner', False), r.get('mc_required', False),
                                           r.get('flag'))
        out.append(f"| {r['ordinal']} | {cell} | {r['action']} |")
    out += ['', '</div>']
    if note:
        # written as HTML, not markdown: attr_list does not run on a paragraph inside a
        # markdown="1" div, and the note must never render as raw "{: .lv-note }" text.
        # page_note_for() joins several notes with a blank line; each gets its own <p> so a
        # blank line can never end the HTML block early.
        for part in note.split('\n\n'):
            out += ['', '<p class="lv-note">'
                    + re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', part) + '</p>']
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
        if (b.get('leftmost') is not None or b.get('markers')
                or e.get('status') == 'pending_row_omd'):
            # a pending row may have published no level at all (leftmost None); its
            # before-record still has to be carried forward or a re-run reads the
            # PENDING chip as the pre-conversion level and the provenance check fails
            out[(e['file'], str(e['row']))] = b
    return out


# ------------------------------------------------------------------- the build
def _decide(row, r, ruled_for_row, pending_row=None):
    """(level, owner, status, reason, new_text, before, ruled) for one action row."""
    existing = CHIP_RE.search(row['level_cell'] or '')
    before_low = (leftmost_level(row['cells']) if row['cells'] is not None
                  else (existing.group(2) if existing else None))
    marked = marked_levels(row['cells'])
    new_text, stripped = strip_tokens(row['action'])
    before = {'leftmost': before_low, 'markers': marked,
              'text_label': text_label(row['action']), 'text_tokens': stripped}

    extra = r['extra']
    if pending_row:
        # an agency addition on an otherwise PEMS-cited page: no chip level at all, and
        # the level the page used to publish is recorded as provenance only
        return ('PENDING', False, 'pending_row_omd', pending_row['reason'], new_text,
                before, None)
    if extra.get('binding', {}).get('policy'):
        # an administrative-policy row: the authority is a PEMS policy, not a protocol row,
        # so there is no printed provider badge to publish — the chip says POLICY and the
        # ledger cites the policy id + the verbatim span out of that policy's own pages
        return ('POLICY', False, 'policy', None, new_text, before, None)
    if ruled_for_row:
        # the owner's decision replaces the inherited level; it is NOT PEMS-verified
        return ruled_for_row['level'], False, 'owner_ruled', None, new_text, before, ruled_for_row

    resolved_level = cells_level((r['resolved'] or {}).get('resolved_cells'))
    tokens = compound_tokens(r['pems_row'],
                             (extra.get('binding') or {}).get('quoted_row_text'))

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
    row_pending = load_row_pending()
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
            if ruled and ruled['level'] == 'FLOOR':
                # a derived level: the page's own lowest chip, read out of the page here,
                # never typed into the yaml. Print the derivation so the log shows it.
                floor, chips_seen, rows_seen = page_floor(rel)
                print(f'floor({rel.split("/")[-1]}) = {floor}  (chips scanned: '
                      f'{len(chips_seen)} on {len(rows_seen)} rows: {", ".join(chips_seen)})')
                _m = CHIP_RE.search(row['level_cell'] or '')
                was = (leftmost_level(row['cells']) if row['cells'] is not None
                       else (_m.group(2) if _m else None))
                print(f'row {row["ordinal"]}: {was or "(no chip)"} -> {floor}')
                ruled = dict(ruled, level=floor,
                             derived_floor={'level': floor, 'chips': chips_seen})
            rp = row_pending.get((rel, str(row['ordinal'])))
            level, owner, status, reason, new_text, before, ruled = _decide(row, r, ruled, rp)
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
            if rp and before.get('leftmost') and before['leftmost'] != rp['carried_from_page']:
                # provenance is checkable, not typed: the yaml must state the level the
                # page actually published before conversion
                problems.append(f'{rel} row {row["ordinal"]}: pending-protocols.yaml records '
                                f'carried_from_page {rp["carried_from_page"]} but the page '
                                f'published {before["leftmost"]} before conversion')
            stripped = before['text_tokens'] or prior_tok.get((rel, str(row['ordinal'])), [])
            before['text_tokens'] = stripped
            if level is None:
                problems.append(f'{rel} row {row["ordinal"]}: no PEMS level and no existing '
                                f'marker — cannot place a marker')
            blocks[-1]['rows'].append({'ordinal': row['ordinal'], 'action': new_text,
                                       'level': level, 'bracketed': r['bracketed'],
                                       'owner': owner,
                                       'flag': (None if r['extra'].get('ratified')
                                                else r['extra'].get('flag')),
                                       'mc_required': bool(r['extra'].get('mc_required'))
                                       and level not in ('PENDING', 'MC')})
            entry = {
                'file': rel,
                'row': row_key(row['ordinal']),
                'action': re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', new_text)
                              .replace('**', '').replace('<br>', ' ')[:150],
                'level_published': level,
                'status': status,
                'reason': reason,
                'owner_note': r['extra'].get('owner_note'),
                'owner_ruling': ({'date': ruled['date'], 'ruling': ruled['ruling'],
                                  'note': ruled.get('note')} if ruled else None),
                'pems_page': r['ptr'][0] if r['ptr'] else None,
                'pems_ordinal': r['ptr'][1] if r['ptr'] else None,
                'pems_badge': r['badge'],
                'compound_tokens': compound_tokens(
                    r['pems_row'], (r['extra'].get('binding') or {}).get('quoted_row_text')),
                'bracketed': r['bracketed'],
                'pems_text': (r['pems_row'] or {}).get('verbatim_text'),
                'binding_evidence': r['extra'].get('binding_evidence'),
                'quoted_row_text': r['extra'].get('quoted_row_text'),
                'cross_page': bool(r['extra'].get('cross_page')),
                'mc_required': bool(r['extra'].get('mc_required'))
                and level not in ('PENDING', 'MC'),
                'mc_evidence': r['extra'].get('mc_evidence'),
                'flag_reason': r['extra'].get('flag'),
                'ratified': r['extra'].get('ratified'),
                'basis': r['basis'],
                'before': before,
                'note': r['extra'].get('adjudication'),
            }
            if rp:
                # a PENDING row may not carry a PEMS citation, even the one the alignment
                # or an adjudication had attached to it before the row was ruled uncited
                entry.update({'pems_page': None, 'pems_ordinal': None, 'pems_badge': None,
                              'pems_text': None, 'compound_tokens': [], 'basis': None,
                              'carried_from_page': rp['carried_from_page'],
                              'pending_note': rp.get('note'),
                              'note': 'agency addition — pending OMD authorization'})
            if ruled and (ruled.get('prose_citations') or ruled.get('level_from')):
                # The owner decided this level, and the ruling records where PEMS prints
                # the action (prose) and/or which printed row's badge it adopts. Any row the
                # alignment/adjudication had attached to the row is NOT the authority for the
                # level, so the ledger must not publish that as a citation. What it does
                # publish is that evidence, verified verbatim by --check.
                # A legacy ruling with no recorded evidence (SVT r2, 2026-11-15) keeps the
                # ledger shape it always had: no citation, no basis, note from owner_ruling.
                entry.update({
                    'pems_page': None, 'pems_ordinal': None, 'pems_badge': None,
                    'pems_text': None, 'compound_tokens': [],
                    'basis': 'owner-rulings:ruled',
                    'prose_citations': [{'page': int(c['page']),
                                         'heading': str(c['heading']).upper(),
                                         'ordinal': int(c['ordinal']),
                                         'quote': c['quote']}
                                        for c in (ruled.get('prose_citations') or [])],
                    'level_from': ruled.get('level_from'),
                    'ruling': ruled.get('ruling'),
                    'ruling_date': ruled.get('date'),
                    'derived_floor': ruled.get('derived_floor'),
                    'note': ruled.get('note') or 'owner ruling — level decided by the owner',
                })
            pol_b = r['extra'].get('binding') or {}
            if pol_b.get('policy'):
                # a POLICY row cites a policy, never a protocol row: the ledger carries the
                # policy id, its pages and the verbatim span, and NO pems_page/ordinal
                pol = policies()[pol_b['policy']]
                entry.update({'pems_page': None, 'pems_ordinal': None, 'pems_badge': None,
                              'pems_text': None, 'compound_tokens': [], 'basis': None,
                              'policy': pol['id'], 'policy_title': pol['title'],
                              'policy_pages': pol['pages'],
                              'policy_effective': pol['effective'],
                              'policy_quote': pol_b['policy_quote'],
                              'policy_note': pol_b.get('policy_note'),
                              'note': 'PEMS administrative policy — ' + pol['title']})
            ledger.append(entry)
        if reg['banner']:
            blocks[0]['banner'] = heading_for(reg['banner'])
        regions_out.append({'blocks': blocks})
    return regions_out, ledger, problems, lines, regions


def _row_ranges(nums):
    """'18-20, 23' from [18,19,20,23] — keeps page notes short."""
    out, start, prev = [], None, None
    for n in nums:
        if start is None:
            start = prev = n
        elif prev is not None and n == prev + 1:
            prev = n
        else:
            out.append((start, prev))
            start = prev = n
    if start is not None:
        out.append((start, prev))
    return ', '.join(str(a) if a == b else f'{a}-{b}' for a, b in out)


def page_note_for(ledger):
    notes = []
    pol_rows = [e for e in ledger if e['status'] == 'policy']
    if pol_rows:
        ids = []
        for e in pol_rows:
            if e['policy'] not in ids:
                ids.append(e['policy'])
        rows = [e['row'] for e in pol_rows]
        label = ('row ' + str(rows[0]) if len(rows) == 1 else 'rows ' + _row_ranges(rows))
        cites = '; '.join(
            f"<em>{policies()[i]['title']}</em> (PEMS p."
            + ', '.join(str(p) for p in policies()[i]['pages']) + ')' for i in ids)
        notes.append('<strong>POLICY</strong> — ' + label + ': no provider level applies. '
                     'PEMS publishes these rules as administrative policy, not as a clinical '
                     'protocol: each is cited to the PEMS 2024 administrative policy that '
                     'prints it — ' + cites + ' — and no provider level is published, because '
                     'PEMS prints these rules as policy rather than as level-badged protocol '
                     'rows.')
        xp = [e for e in ledger if e.get('cross_page')]
        if xp:
            notes.append('A provider level does not by itself make an administrative rule a '
                         'protocol: '
                         + '; '.join(
                             f"one of them is printed as row p.{e['pems_page']}#"
                             f"{e['pems_ordinal']} of the PEMS 2024 protocol and is cited "
                             f"there, so its chip is that row's level ({e['level_published']})"
                             for e in xp) + '. No administrative policy prints it.')
    pending_rows = [e for e in ledger if e['status'] == 'pending_row_omd']
    if pending_rows:
        custom = [e.get('pending_note') for e in pending_rows if e.get('pending_note')]
        if custom:
            # a row whose action IS printed in PEMS (e.g. in PEARLS) needs a note that
            # says so; the generic "no counterpart" wording would be false for it
            notes.append(' '.join(custom))
        else:
            notes.append(row_pending_note([str(e['row']) for e in pending_rows]))
    owner_rows = [str(e['row']) for e in ledger if e['status'] == 'OWNER_REQUIRED']
    if owner_rows:
        # A row whose OWNER_REQUIRED reason is not the generic "no PEMS row prints it" case
        # (e.g. the row bundles two actions PEMS prints at two *lower* levels) carries its own
        # `owner_note` in row-bindings.yaml, because the generic sentence would be false for it.
        custom = [e['owner_note'] for e in ledger if e['status'] == 'OWNER_REQUIRED'
                  and e.get('owner_note')]
        plain = [str(e['row']) for e in ledger if e['status'] == 'OWNER_REQUIRED'
                 and not e.get('owner_note')]
        notes.extend(custom)
        if plain:
            # Page voice (owner ruling 2026-11-20): plain reader instruction only — no audit
            # token, no row number, no file path. The ⚑ on the chip marks which action it is.
            notes.append('&#9873; **Level pending Medical Control review** — PEMS 2024 does not '
                         'print a provider level for this action as a level-badged row, so the '
                         'level shown is provisional. Treat it as provisional until Medical '
                         'Control confirms it.')
    fixed = [(e['row'], e.get('flag_reason')) for e in ledger
             if e.get('flag_reason') and not e.get('ratified')]
    if fixed:
        # Page voice (owner ruling 2026-11-20): the flag text is reader instruction, written in
        # row-bindings.yaml; no row numbers, no audit vocabulary, no file path here.
        notes.append('&#9873; ' + ' '.join(why for _r, why in fixed))
    mc_rows = [str(e['row']) for e in ledger if e.get('mc_required')]
    if mc_rows:
        label = ('row ' + mc_rows[0] if len(mc_rows) == 1
                 else 'rows ' + ', '.join(mc_rows))
        notes.append('**+MC** — the marked action(s) may be performed at the level shown only '
                     'with Medical Control authorisation. PEMS prints that level in '
                     'brackets; the marker carries that meaning into the single-level layout. '
                     'It is not a second level and not the same as an <code>MC</code> chip, '
                     'which marks an action that is itself a Medical Control contact.')
    if any(e['bracketed'] for e in ledger):
        notes.append('* **Bracketed badge** — the level is printed in brackets in the source: '
                     'agency post-affiliation training documentation on file, plus the '
                     'Medical Control written authorization for that skill. The brackets are '
                     "the source's own.")
    return '\n\n'.join(notes) if notes else None


def splice(rel):
    """Rewrite every level-table region; leave every other line byte-identical."""
    regions_out, ledger, problems, lines, regions = plan(rel)
    if problems:
        for p in problems:
            print('PROBLEM:', p)
        raise SystemExit(2)
    page_note = page_note_for(ledger)
    if rel in policy_targets():
        header, div_open = POLICY_HEADER, DIV_POLICY_OPEN
    else:
        header, div_open = NEW_HEADER, DIV_OPEN

    out, last = [], 0
    for ri, (reg, reg_out) in enumerate(zip(regions, regions_out)):
        out += lines[last:reg['start']]
        pieces = []
        for bi, block in enumerate(reg_out['blocks']):
            last_block = (ri == len(regions) - 1 and bi == len(reg_out['blocks']) - 1)
            if bi:
                pieces.append('')
            pieces += render_block(block['rows'], note=(page_note if last_block else None),
                                   banner=block['banner'], header=header, div_open=div_open)
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
                'row': row_key(ordinal),
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


# The pre-conversion branch base (`main`). The page-side bracket notation lives only in
# these revisions, so the bracket rows are re-derived from here rather than trusted from a
# list typed into the card or into row-bindings.yaml.
BASE_REV = '768ad68'
BRACKET_CELL = re.compile(r'^\[(EMR|EMT|A|I|P)\]$')


def page_base_rev(rel):
    """The revision whose page is this page's pre-conversion state.

    Defaults to BASE_REV (the branch base, `main`). A page whose bracket notation was
    added on the level-scan branch *after* that base needs its own pre-conversion
    revision, recorded as `base_rev` on its exceptions.yaml entry — otherwise
    `base_brackets()` reads a revision that never carried the brackets and the `+MC`
    check silently passes on a row whose bracket was dropped.
    """
    import yaml
    if os.path.exists(EXCEPTIONS_YAML):
        doc = yaml.safe_load(open(EXCEPTIONS_YAML, encoding='utf-8')) or {}
        for rec in doc.get('pages') or []:
            if rec.get('file') == rel and rec.get('base_rev'):
                return str(rec['base_rev'])
    return BASE_REV


def base_brackets(rel):
    """{row ordinal: bracketed level} from the page's pre-conversion revision.

    On those pages a level cell reading `[X]` means "X performs this action only with
    Medical Control authorisation" (owner ruling 2026-11-13). The collapse to one chip
    deleted that notation, so `--check` re-derives the set and demands each row either
    carry the `+MC` marker or record why it cannot.
    """
    text = git_show(page_base_rev(rel), rel)
    if not text:
        return {}
    out = {}
    for line in text.split('\n'):
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if len(cells) < 7 or not cells[0].isdigit():
            continue
        for i, c in enumerate(cells[2:7]):
            if BRACKET_CELL.match(c):
                out[cells[0]] = LV[i]
                break
    return out


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


# ------------------------------------------- owner-facing open-question cards
# The ledger's OPEN OWNER QUESTIONS section is copied verbatim into the page the OWNER
# reads (`docs/protocols/outstanding-decisions.md`), so a card that states the pre-ruling
# state is a published false reason, not an internal note. These two cards therefore
# DERIVE their state from the ledger: the Cold Exposure card was hand-written and went
# on saying "rows 6 and 9 are OWNER_REQUIRED / printed nowhere / kept and flagged" after
# the 2026-11-17 Pearl ruling had made both rows `owner_ruled` with verbatim citations,
# and the administrative card kept asking about Stroke Field Triage row 1 after that row
# had been levelled `EMT`. `check_ledger_markdown()` fails `--check` on any drift.
ADMIN_PENDING_PROSE = {
    ('01_Behavioral_Health_Transportation_Decision_PROC.md', '6'): (
        'law-enforcement custody',
        'PEMS prints the rule only as prose in the Behavioral Emergencies restraint '
        'guidelines (p.73), not in any administrative policy and not as a level-badged row.'),
    ('01_Behavioral_Health_Transportation_Decision_PROC.md', '7'): (
        'handcuffed transport',
        'PEMS prints the rule only as prose in the Behavioral Emergencies restraint '
        'guidelines (p.73), not in any administrative policy and not as a level-badged row.'),
    ('01_Infant_Abandonment_PROC.md', '2'): (
        '"assess infant and provide medical care"',
        'the policy prints no assessment/treatment step.'),
    ('01_Stroke_Field_Triage_PROC.md', '4'): (
        'life-threats route to nearest ED',
        'the Stroke policy prints it nowhere.'),
}


def open_question_facts(ledger):
    """The state the two owner-facing Batch-5 question cards must state, from the ledger."""
    cold = [e for e in ledger
            if e['file'].endswith('02_Cold_Exposure_PROC.md') and e['row'] in (6, 9)]
    admin_pages = {e['file'] for e in ledger if e['status'] == 'policy'}
    admin_pending = [e for e in ledger
                     if e['status'] == 'pending_row_omd' and e['file'] in admin_pages]
    return {'cold': cold,
            'cold_by_row': {e['row']: e for e in cold},
            'admin_pending': admin_pending}


def _cite_brief(c):
    """`p.67 PEARLS #5: "the quoted words"` — page, heading and ordinal, then the quote."""
    q = ' '.join((c.get('quote') or c.get('text') or '').split())
    if len(q) > 110:
        q = q[:107].rstrip() + '…'
    return f"p.{c['page']} {c['heading']} #{c['ordinal']}" + (f': "{q}"' if q else '')


def _rows_label(rows):
    rows = sorted(rows)
    return f'row {rows[0]}' if len(rows) == 1 else f'rows {rows[0]}-{rows[-1]}'


ADMIN_PAGE_NAME = {
    '01_Behavioral_Health_Transportation_Decision_PROC.md': 'Behavioral Health',
    '01_Infant_Abandonment_PROC.md': 'Infant Abandonment',
    '01_Stroke_Field_Triage_PROC.md': 'Stroke Field Triage',
}


COLD_PAGE = 'protocols/general/02_Cold_Exposure_PROC.md'

# The Cold page's owner ruling is a RECORDED DECISION, not an open question: the owner
# answered "Anyone can warm a patient, EMR" on 2026-11-20. It is emitted in its own
# OWNER_RULED section, never in OPEN OWNER QUESTIONS — the page the owner reads is titled
# "decisions still waiting on you", so an answered card there is a published falsehood.
COLD_RULED_HEADER = '## OWNER_RULED — Cold Exposure pilot (owner ruling 2026-11-20)'

# Pages whose unbadged PEMS prose lives in a "References & Good Practice" block. The owner's
# 2026-11-20 ruling: the page states the recorded level; the PEMS citation itself stays in
# audit/level-scan/ and must NOT be printed on the page ("I do not want that Source: PEMS
# 2024 post in the final product"). `--check` fails if the line comes back.
AUDIT_ONLY_PROVENANCE = {
    'protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md',
    'protocols/general/02_Cold_Exposure_PROC.md',
}


def _cold_relocated_rows():
    """The recorded relocations for the Cold Exposure page, keyed by row."""
    return {r['row']: r for r in load_relocated() if r['file'].endswith('02_Cold_Exposure_PROC.md')}


def cold_question_cards(ledger):
    """The Cold-page cards that are genuinely OPEN — normally none.

    Rows 6 and 9 left the action table in the 2026-11-20 pilot and the owner ANSWERED the
    floor question the same day (`EMR`), so neither is a question any more: the recorded
    decision is emitted by `cold_ruled_cards()` into the ledger's OWNER_RULED section. What
    stays here is the failure mode — a relocation the page or `relocated-rows.yaml` does not
    actually carry, or a ledger that still records the rows as open — because that is work
    the owner still has to see.
    """
    facts = open_question_facts(ledger)
    by_row = facts['cold_by_row']
    r6, r9 = by_row.get(6), by_row.get(9)
    if r6 is None or r9 is None:
        # The rows left the ledger because they left the action table. Say that ONLY if the
        # page really carries the block: `relocated-rows.yaml` says what moved, and the
        # page's own text has to prove it. Otherwise this card would be an assertion about
        # a block nobody can see — the exact failure the card exists to prevent.
        moved = _cold_relocated_rows()
        unrecorded = [n for n in (6, 9) if n not in moved]
        unproved = {n: relocated_proofs_missing(moved[n]) for n in (6, 9)
                    if n in moved and relocated_proofs_missing(moved[n])}
        if unrecorded or unproved:
            why = []
            if unrecorded:
                why.append(f'row(s) {", ".join(str(n) for n in unrecorded)} have no entry in '
                           '`audit/level-scan/relocated-rows.yaml`')
            for n, spans in sorted(unproved.items()):
                why.append(f'row {n}: the page does not print {", ".join(repr(s) for s in spans)}')
            out = ['- **Batch 5 — Cold Exposure rows 6 and 9 are no longer in this ledger.** '
                   'The relocation this pilot recorded does not check out: ' + '; '.join(why)
                   + '. Repair the page or `relocated-rows.yaml`, then re-run '
                   '`scripts/level_rule.py --write` before publishing — do not publish this '
                   'card as it stands.']
            floor_cards, answered = cold_floor_question(ledger)
            return out + ([] if answered else floor_cards)
        # The relocation itself is a RECORDED ruling, not a question — `cold_ruled_cards()`
        # publishes it in the ledger's OWNER_RULED section.
        return []
    if r6['status'] == 'owner_ruled' and r9['status'] == 'owner_ruled':
        return []
    floor_cards, answered = cold_floor_question(ledger)
    return ['- **Batch 5 — Cold Exposure rows 6 and 9, as the ledger records them today.** '
            + '; '.join(f"row {e['row']} is `{e['status']}` at `{e['level_published']}`"
                        for e in sorted(facts['cold'], key=lambda e: e['row']))
            + '. Any row not `owner_ruled` here is still open and carries its flag.'] \
        + ([] if answered else floor_cards)


def cold_ruled_cards(ledger):
    """The Cold page's RECORDED rulings, emitted into the ledger's OWNER_RULED section.

    Nothing here is a question. Two decisions live in this block: the 2026-11-20 pilot
    relocation (rows 6 and 9 out of the action table, by the owner's presentation ruling)
    and the owner's answer to the BLS-floor question the 2026-11-17 card left open — `EMR`,
    "anyone can warm a patient". The history is kept and the owner's words are quoted, but
    the cards are filed as decisions, so the open-question count the owner reads excludes
    them.
    """
    facts = open_question_facts(ledger)
    r6, r9 = facts['cold_by_row'].get(6), facts['cold_by_row'].get(9)
    out = []
    if r6 is None or r9 is None:
        moved = _cold_relocated_rows()
        if any(n not in moved or relocated_proofs_missing(moved[n]) for n in (6, 9)):
            return []
        levels = ', '.join(f"row {n} `{moved[n]['level']}` ({moved[n]['pems']})"
                           for n in (6, 9))
        out.append('- **Pilot 2026-11-20 — Cold Exposure rows 6 and 9 were moved out of the '
                   'action table into the page\'s "References & Good Practice" block.** Both '
                   'are unbadged PEMS p.67 PEARLS prose; the owner\'s presentation ruling puts '
                   'unbadged prose below the table instead of chipping it. The levels this '
                   f'page records for them ({levels}, Pearl ruling 2026-11-17) are stated in '
                   'that block and stay in `level-rulings.yaml`; they are no longer chips, so '
                   'they are no longer in this ledger.')
    elif r6['status'] == 'owner_ruled' and r9['status'] == 'owner_ruled':
        c6 = ', '.join(_cite_brief(c) for c in (r6.get('prose_citations') or []))
        c9 = ', '.join(_cite_brief(c) for c in (r9.get('prose_citations') or []))
        out.append(
            '- **Batch 5 — Cold Exposure rows 6 and 9 are OWNER_RULED (Pearl ruling '
            '2026-11-17); the "prints nowhere" reason was false and no flag remains.** '
            f'Row 6 (active external rewarming with heat packs) is printed in the '
            f'protocol\'s own Pearls — {c6} — so the level stays `{r6["level_published"]}`: '
            'a Pearl that restates a BLS skill does not create a new provider authority, '
            'and PEMS prints no badge for it. '
            f'Row 9 (Medical Control before use of AED) is printed — {c9} — so the level '
            f'stays `{r9["level_published"]}`: a Medical Control contact is not a provider '
            'level. Neither row is flagged on its page any more; both were cleared by the '
            'ruling, not left as questions.')
    else:
        return []
    floor_cards, answered = cold_floor_question(ledger)
    if answered:
        out += floor_cards
    return out


def cold_floor_question(ledger):
    """The Cold r6 floor tension: `(cards, answered)`.

    The card's own table kept row 6 at `EMT`, but the ruling's test is "BLS-scope -> the
    page's BLS floor" and this page chips a lower floor. The level is not changed here;
    the disagreement is recorded so a reader comparing the two rules is not left with an
    unexplained contradiction.

    Since the 2026-11-20 pilot row 6 is no longer a chipped row, so the same tension is
    read off the page's References & Good Practice block — which states the level in prose
    and is exactly where the owner would now meet it.

    `answered` is True only when the owner has ruled and the recorded level now equals the
    page's own floor: the card is then a RECORDED DECISION (it belongs in the ledger's
    OWNER_RULED section), not a question waiting on the owner.
    """
    by_row = open_question_facts(ledger)['cold_by_row']
    r6 = by_row.get(6)
    where = f'the row now reads `{r6["level_published"]}`' if r6 is not None else ''
    if r6 is not None:
        if r6['status'] != 'owner_ruled':
            return [], False
        file_rel, level = r6['file'], r6['level_published']
    else:
        moved = _cold_relocated_rows().get(6)
        if moved is None or relocated_proofs_missing(moved):
            return [], False
        file_rel, level = moved['file'], moved['level']
        where = ('the page\'s "References & Good Practice" block now states '
                 f'`{level}`')
    floor, chips, _seen = page_floor(file_rel)
    if floor == level:
        # The level now equals the page's own BLS floor, so the tension recorded on
        # 2026-11-17 is closed. Do not drop it: the owner was ASKED and ANSWERED, and the
        # answer is the reason the level is what it is. The card is rebuilt from the ruling
        # (`answered`) and the page floor, so deleting the answer, changing the recorded
        # level away from the floor, or changing the page's chips all make the ledger's md
        # stop matching --check.
        rul = (load_rulings().get((file_rel, '6')) or {})
        ans = rul.get('answered') or {}
        if not ans:
            return [], False
        return [f'- **Cold Exposure row 6 — the BLS-floor question was ASKED and ANSWERED '
                f'(owner ruling {ans["date"]}): `{ans["level"]}`.** The question recorded '
                f'here on 2026-11-17 was whether the rewarming item keeps `EMT` although '
                f'the page\'s own BLS floor is lower: the ruling\'s test reads "BLS-scope -> '
                f'the page\'s BLS floor", heat packs are a BLS skill, and the page chips a '
                f'floor of `{floor}` (derived from the page\'s {len(chips)} level chips, in '
                f'file order: {", ".join(chips)}). The owner answered on {ans["date"]}: '
                f'**{ans["level"]}** — "{ans["quote"]}". The item stays below the action '
                f'table in the page\'s "References & Good Practice" block, and that block '
                f'now states `{ans["level"]}`, the page\'s own derived floor. The history is '
                f'kept in `level-rulings.yaml`; no open question remains for this row.'], True
    return [f'- **Pearl ruling 2026-11-17 — Cold Exposure row 6 keeps '
            f'`{level}` although the page\'s own BLS floor is `{floor}`.** '
            f'The ruling\'s test reads "BLS-scope -> the page\'s BLS floor", and heat packs '
            f'are a BLS skill ("anyone can do that"), yet this card\'s row table said the '
            f'level stays unchanged, so {where} while '
            f'the page itself chips a floor of `{floor}` (derived from the page\'s '
            f'{len(chips)} level chips, in file order: {", ".join(chips)}). Both readings '
            f'agree the action is BLS-scope and that no new authority is created; they '
            f'disagree only on which BLS level prints. Owner to confirm: keep '
            f'`{level}` as directed, or lower it to the page floor '
            f'`{floor}`? Nothing changes on the page until then.'], False


def admin_pending_cards(ledger):
    """The Batch-6 administrative PENDING card, counting and naming rows from the ledger."""
    pend = open_question_facts(ledger)['admin_pending']
    if not pend:
        return []
    out = [f'- **Batch 6 — the {len(pend)} administrative PENDING row(s), for the owner\'s '
           'one-pass ruling.** Each row below is an administrative rule that no PEMS 2024 '
           'administrative policy prints:']
    # group consecutive rows of the SAME file with the SAME explanation into one clause
    groups = []
    for e in sorted(pend, key=lambda e: (e['file'], e['row'])):
        short = e['file'].split('/')[-1]
        desc, why = ADMIN_PENDING_PROSE.get(
            (short, str(e['row'])), ('', (e.get('reason') or '').strip()))
        if groups and groups[-1]['file'] == short and groups[-1]['why'] == why:
            groups[-1]['rows'].append(e['row'])
            if desc and desc not in groups[-1]['descs']:
                groups[-1]['descs'].append(desc)
        else:
            groups.append({'file': short, 'rows': [e['row']], 'why': why,
                           'descs': [desc] if desc else []})
    clauses = []
    for g in groups:
        name = ADMIN_PAGE_NAME.get(
            g['file'], g['file'].replace('_PROC.md', '').split('_', 1)[-1].replace('_', ' '))
        desc = '; '.join(g['descs'])
        clauses.append(f"{name} {_rows_label(g['rows'])}" + (f' ({desc})' if desc else '')
                       + (f': {g["why"]}' if g['why'] else '.'))
    out.append('  ' + ' '.join(clauses))
    # a row this card used to ask about, now ruled: say so instead of leaving the owner
    # with a count that silently shrank.
    sft = [e for e in ledger
           if e['file'].endswith('01_Stroke_Field_Triage_PROC.md') and e['row'] == 1]
    if sft and sft[0]['status'] != 'pending_row_omd':
        e = sft[0]
        cite = (f' (p.{e["pems_page"]}#{e["pems_ordinal"]})' if e.get('pems_page') is not None
                else '')
        out.append(f'  Stroke Field Triage row 1 is no longer in this set: the Pearl ruling '
                   f'levelled it `{e["level_published"]}`{cite}, so the administrative '
                   f'PENDING count is {len(pend)}. Each row keeps its reason in '
                   '`pending-protocols.yaml` and on the page.')
    else:
        out.append('  Each keeps its reason in `pending-protocols.yaml` and on the page.')
    return out


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
             '| `row-bindings:bound` **×page** | a row-level citation to a PEMS 2024 row on ANOTHER page (owner ruling 2026-11-16); the cited row\'s quoted words are in *Cross-page citations* |',
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
        if e.get('cross_page'):
            pems += ' **×page**'
        if e.get('mc_required'):
            pems += ' +MC'
        f = e['file'].split('/')[-1]
        lines.append(f"| `{f}` | {e['row']} | {e['level_published']} | {pems} | {text} | "
                     f"{e['basis'] or '—'} | {e['status']} |")
    # ---------------------------------------------------------------- cross-page citations
    cross = [e for e in ledger if e.get('cross_page')]
    lines += ['', '## Cross-page citations (owner ruling 2026-11-16)', '',
              'The owner ruled: *"Cite across pages — if PEMS prints the action in a procedure,',
              'use that procedure\'s level and cite it."* Each row below cites a PEMS 2024 row',
              'that is **not** on the page\'s own governing source. `cross_page: true` is',
              'recorded in `row-bindings.yaml` with the citing evidence, and `quoted_row_text` is',
              'the verbatim span from the cited row that the checker re-reads out of',
              '`pems_table.json` — a citation whose quote the cited row does not print fails',
              '`--check`. The chip is the badge that row prints, not the page\'s old level.', '',
              f'**{len(cross)} row(s).**', '']
    if not cross:
        lines.append('None — every PEMS citation is to the page\'s own source.')
    for e in cross:
        lines.append(f"- `{e['file']}` row {e['row']}: **{e['level_published']}** from "
                     f"p.{e['pems_page']}#{e['pems_ordinal']} (was "
                     f"{e.get('status_before') or e['before']['leftmost']}) — quoted: "
                     f"\"{e.get('quoted_row_text')}\"")
        lines.append(f"  - action: {e['action']}")
        if e.get('binding_evidence'):
            lines.append(f"  - evidence: {e['binding_evidence']}")

    # ---------------------------------------------------------------- the +MC marker
    mcrows = [e for e in ledger if e.get('mc_required')]
    lines += ['', '## `+MC` — Medical-Control-required marker (owner ruling 2026-11-16)', '',
              'These pages printed the level cell in brackets, meaning *that level performs the',
              'action only with Medical Control authorisation* (owner ruling 2026-11-13). The',
              'single-chip layout deleted that meaning; the `+MC` marker carries it back as a',
              'second marker beside the level chip. It is deliberately not a second level chip,',
              'and it is styled distinctly from the `MC` chip, which means the action *is* a',
              'Medical Control contact. Source of truth is `mc_required: true` in',
              '`row-bindings.yaml` (never a hand-written span); `--check` fails if the marker is',
              'missing or doubled, and it re-derives the bracketed rows from each page\'s',
              f'pre-conversion revision (`{BASE_REV}` by default, or the page\'s recorded',
              '`base_rev` in `exceptions.yaml` when the bracket notation was added on the',
              'level-scan branch after that base) so a bracketed row cannot be silently',
              'dropped.', '',
              f'**{len(mcrows)} row(s).**', '']
    if not mcrows:
        lines.append('None.')
    for e in mcrows:
        lines.append(f"- `{e['file']}` row {e['row']}: **{e['level_published']}** +MC")
        if e.get('mc_evidence'):
            lines.append(f"  - evidence: {e['mc_evidence']}")
    excl = [(k, v) for k, v in load_bindings().items() if v.get('mc_bracket_excluded')]
    lines += ['', '### Bracketed rows whose bracket cannot be carried', '',
              'A bracketed page cell whose level is **not** the level the row now publishes',
              'cannot be carried by `+MC` without changing its meaning. The rows below record, in',
              '`row-bindings.yaml`, which case each is. Nothing here is silently dropped: `--check`',
              'fails on a bracketed row that is neither `mc_required` nor `mc_bracket_excluded`.', '']
    if not excl:
        lines.append('None.')
    for (f, row), rec in excl:
        lines.append(f"- `{f}` row {row}: {rec['mc_bracket_excluded'].strip()}")

    # ------------------------------------------------------- flagged rows before -> after
    # A relocated row left the action table, so it is no longer in this ledger — its
    # pre-move status is read from relocated-rows.yaml instead, or the history would
    # silently shrink by exactly the rows this pass moved.
    reloc = load_relocated()
    files = []
    for e in ledger:
        if e['file'] not in files:
            files.append(e['file'])
    for r in reloc:
        if r['file'] not in files:
            files.append(r['file'])

    def _flagged(status):
        return status in ('OWNER_REQUIRED', 'pending_omd', 'pending_row_omd')

    lines += ['', '## Flagged rows before -> after, per page (derived, not typed)', '',
              '"Before" is the status the previous `level-rule-ledger.json` recorded for that row',
              '(`status_before`, captured by the writer); "after" is the status on this page now.',
              'A row that stopped being flagged is a **cross-page citation** or was closed by a',
              'recorded decision — the citation that cleared it is listed above and in the table.',
              'Rows relocated out of an action table are not in the ledger any more, so their',
              'pre-move status is read from `audit/level-scan/relocated-rows.yaml` (the',
              '**relocated** column) — these historical counts do not shrink just because a row',
              'left the table; a relocated row that was flagged before counts as cleared by the',
              'move, not by a citation.', '',
              '| page | flagged before | flagged after | cleared | of which cross-page '
              '| of which relocated |',
              '|---|---:|---:|---:|---:|---:|']
    reloc_all = load_relocated()
    for f in files:
        rows = [e for e in ledger if e['file'] == f]
        rel = [r for r in reloc_all if r['file'] == f]
        before = sum(1 for e in rows if _flagged(e.get('status_before')))
        rel_before = sum(1 for r in rel if _flagged(r.get('status_before')))
        after = sum(1 for e in rows if _flagged(e['status']))
        cross_n = sum(1 for e in rows if e.get('cross_page')
                      and _flagged(e.get('status_before')))
        # A page with no prior ledger record is newly converted: it had no flags to
        # clear, so "before - after" would print a negative. Say "new" instead.
        cleared = (str(before + rel_before - after) if (before or rel_before) else 'new')
        lines.append(f"| `{f.split('/')[-1]}` | {before + rel_before} | {after} | {cleared} | "
                     f"{cross_n} | {rel_before} |")
    tot_before = sum(1 for e in ledger if _flagged(e.get('status_before'))) \
        + sum(1 for r in reloc_all if _flagged(r.get('status_before')))
    tot_after = sum(1 for e in ledger if _flagged(e['status']))
    lines += ['', f'**Total: {tot_before} flagged before, {tot_after} after '
                  f'({tot_before - tot_after} cleared).**', '']

    # ------------------------------------------- rows moved below the action table
    lines += ['', '## Rows moved below the action table (References & Good Practice)', '',
              'Owner instruction 2026-11-20: guidance PEMS prints as instruction to the',
              'provider is not a numbered action and must not be given a level of our own',
              'invention. Such a row leaves the action table and the ledger; it is recorded',
              'here and in `audit/level-scan/relocated-rows.yaml` with what it was and where',
              'it now reads, so nothing can be deleted silently. `--check` re-reads the page',
              'and fails if the recorded block is not printed there.', '',
              f'**{len(reloc)} row(s).**', '']
    if not reloc:
        lines.append('None.')
    for r in reloc:
        lvl = ('no level — guidance, not an action' if r.get('guidance')
               else f"level `{r['level']}`")
        was = f" (was `{r['status_before']}`)" if r.get('status_before') else ''
        lines.append(f"- `{r['file']}` row {r['row']}: {lvl}{was} — {r['where']}")
        if r.get('note'):
            lines.append(f"  - {r['note']}")

    # ------------------------------------------------ rows split into one action each
    splits = load_site_splits()
    lines += ['', '## Rows split into one action each (owner instruction 2026-11-20)', '',
              'A row that bundled more than one action cannot carry one level without over- or',
              'under-granting half of itself — that is why every row below was flagged',
              'OWNER_REQUIRED. Each is now one action per row, and each part cites the PEMS 2024',
              'row that prints **that** action, so the chip is the source\'s badge and nothing was',
              'invented. The first part keeps the row number and the rest are lettered, so the',
              'number stays the audit key bound to its citation and no downstream reference',
              'shifts. The durable record is `audit/level-scan/row-splits.yaml` `site_splits:`;',
              '`--check` re-reads every part on the page and compares its chip with the badge of',
              'the row it names. `source` is `cited` when a printed badge authorises the level,',
              '`owner_required` when the source prints the action but scopes it in the row\'s own',
              'words inside a cell badged for another clause (or two printed rows disagree) — the',
              'part is then flagged and the PEMS row shown is the row that PRINTS the action, not',
              'a level citation. `source: ruling` would mean a recorded owner decision; none of',
              'these parts is one.', '']
    if not splits:
        lines.append('None.')
    else:
        lines += ['| page | row | part | level | PEMS row | source |',
                  '|---|---|---|---|---|---|']
        for rec in splits:
            short = rec['file'].split('/')[-1]
            for p in rec['parts']:
                lines.append(f"| `{short}` | {rec['row']} | {p['row']} | {p['level']} | "
                             f"{p['pems']} | {p.get('source', 'cited')} |")
        n_before = len(splits)
        n_after = sum(len(r['parts']) for r in splits)
        lines += ['', f'**{n_before} row(s) became {n_after} sub-rows.** Every part carries',
                  'exactly one level, and no part restates a level in its action text.', '']
        for rec in splits:
            def _part(p):
                tag = ' — OWNER_REQUIRED, printing row' if p.get('source') == 'owner_required' \
                    else ''
                return f"{p['row']} `{p['level']}` ({p['pems']}{tag})"
            lines.append(f"- `{rec['file']}` row {rec['row']}: "
                         + '; '.join(_part(p) for p in rec['parts']))
            lines.append(f"  - why: {' '.join(rec['reason'].split())}")

    owner = [e for e in ledger if e['status'] == 'OWNER_REQUIRED']
    lines += ['', '## OWNER_REQUIRED', '',
              f'**{len(owner)} row(s).** No PEMS 2024 row authorises a provider level for these',
              'actions, after the cross-page search (a row is only cleared when a PEMS row',
              'actually prints the action — see *Cross-page citations* above). The chip keeps the',
              'level the page already published and carries the flag. Nothing here was invented:',
              'each reason says either that no PEMS row anywhere prints the action, or which row',
              'prints it and why its badge contradicts the row\'s own words.', '']
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
              'PEMS row column above is empty on purpose.', '',
              'Where the action IS printed in the source, the entry names the unbadged prose that',
              'prints it by page + heading + ordinal and quotes it verbatim (the same discipline as',
              'a cross-page row citation). That evidence settles *that the row is not silent*; it',
              'does not turn the level into a printed badge. `level from` names the printed row',
              'whose badge the ruling adopts, when the level itself comes from one.', '']
    if not ruled:
        lines.append('None — every action row is either PEMS-verified or OWNER_REQUIRED.')
    for e in ruled:
        r = e.get('owner_ruling') or {}
        lines.append(f"- `{e['file']}` row {e['row']} — **{e['level_published']}** — "
                     f"status `owner_ruled`. {r.get('note') or r.get('ruling')}")
        for c in e.get('prose_citations') or []:
            lines.append(f"  - printed in unbadged prose: p.{c['page']} {c['heading']} "
                         f"#{c['ordinal']} — \"{c['quote']}\"")
        lf = e.get('level_from')
        if lf:
            lines.append(f"  - level from: p.{lf['page']}#{lf['ordinal']} (the badge PEMS prints "
                         f"for the procedure the rule governs)")
        if e.get('derived_floor'):
            df = e['derived_floor']
            lines.append(f"  - level derived: the page's own lowest chip = {df['level']} "
                         f"(chips on the page: {', '.join(df['chips'])}) — read out of the page "
                         f"by `page_floor()`, not typed")
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

    cold_ruled = cold_ruled_cards(ledger)
    lines += ['', COLD_RULED_HEADER, '',
              'Decided, not open. The owner ruled these on 2026-11-20 and the page states the',
              'recorded level; they are filed here so the open-question count the owner reads',
              'excludes them. The history is kept — what was asked, and the owner\'s words —',
              'and the PEMS citation stays in `audit/level-scan/` (`level-rulings.yaml`,',
              '`relocated-rows.yaml`), deliberately not printed on the page.', '']
    if not cold_ruled:
        lines.append('None.')
    lines += cold_ruled

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
    prows = [e for e in ledger if e['status'] == 'pending_row_omd']
    lines += ['', '## PENDING_OMD — row-level (agency additions on PEMS-cited pages)', '',
              f'**{len(prows)} row(s).** The page is PEMS-cited and every other row on it names '
              'the PEMS 2024 row that authorizes it. These rows do not: the agency added them '
              'and PEMS publishes no such action, so no provider level is published for them '
              'until the OMD authorizes one. The chip is `PENDING`; `carried_from_page` records '
              'the level the page published before conversion and is **provenance only**.', '']
    if not prows:
        lines.append('None.')
    for e in prows:
        lines.append(f"- `{e['file']}` row {e['row']}: PENDING (carried from the page as "
                     f"**{e['carried_from_page']}**) — {e['action'][:90]}")
        lines.append(f"  - reason: {e['reason']}")
    policed = [e for e in ledger if e['status'] == 'policy']
    pol_files = sorted({e['file'] for e in policed})
    cited_ids = []
    for e in policed:
        if e['policy'] not in cited_ids:
            cited_ids.append(e['policy'])
    lines += ['', '## POLICY — PEMS 2024 administrative policy (owner ruling 2026-11-16)', '',
              'The owner ruled: *"Treat admin pages as policy: cite PEMS administrative',
              'policies where they exist, PENDING where the policy is ours."* An administrative',
              'page is therefore chipped **`POLICY`** where a PEMS 2024 administrative policy',
              'prints the rule, and **`PENDING`** where no PEMS policy prints it. A `POLICY` row',
              'publishes **no provider level**: PEMS prints these rules as policy prose, not as',
              'level-badged protocol rows, and `exceptions.yaml` already declares these pages',
              '`kind: administrative` — not level-gated. Each row below names the policy, its',
              'PEMS pages and a verbatim span of that policy; `audit/level-scan/pems-policies.yaml`',
              'is the only list of citable policies, and `--check` fails on an unknown policy id,',
              'on a `POLICY` row that also carries a protocol citation, on a `PENDING` row that',
              'carries a policy reference, and on a quote the policy pages do not print.', '',
              f'**{len(policed)} row(s) across {len(pol_files)} page(s), citing {len(cited_ids)} '
              f'of the 14 PEMS 2024 administrative policies.**', '']
    lines += ['| policy id | title | PEMS pages | effective | rows |', '|---|---|---|---|---:|']
    for pid in cited_ids:
        pol = policies()[pid]
        n = sum(1 for e in policed if e['policy'] == pid)
        lines.append(f"| `{pid}` | {pol['title']} | p."
                     + ', '.join(str(p) for p in pol['pages'])
                     + f" | {pol['effective']} | {n} |")
    lines.append('')
    for rel in pol_files:
        rows = [e for e in policed if e['file'] == rel]
        lines.append(f'- `{rel}` — {len(rows)} POLICY row(s)')
        for e in rows:
            pol = policies()[e['policy']]
            lines.append(f"  - row {e['row']}: `{e['policy']}` (p."
                         + ', '.join(str(p) for p in pol['pages'])
                         + f') — "{e["policy_quote"]}"')
            if e.get('policy_note'):
                lines.append(f"    - note: {e['policy_note']}")
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
    # ------------------------------------------------------- corrected rows (CORRECTED)
    # A flagged correction that the owner has ratified keeps this record and loses its
    # on-page marker. The record must still answer: which printed page authorised the
    # chip, what the page published before, and who ratified the change.
    fixed = [e for e in ledger if e.get('flag_reason')]
    lines += ['', '## CORRECTED — level corrected against the printed page', '',
              f'**{len(fixed)} row(s).** A `CORRECTED` row published a level different from',
              'the one its cited PEMS 2024 row prints. `row-bindings.yaml` keeps the correction',
              'reason (`flag`), the p.247 citation and the evidence. Where the owner has since',
              'read the correction and ratified it, `ratified` records the date, the ratifying',
              'party and the ruling words, and the on-page ⚑ marker is **retired** — the chip',
              'stays the corrected level. `--check` fails a ratified row that still carries the',
              'marker, and an unratified flagged row that has lost it.', '']
    if not fixed:
        lines.append('None.')
    for e in fixed:
        lines.append(f"- `{e['file']}` row {e['row']}: **{e['level_published']}** from "
                     f"p.{e['pems_page']}#{e['pems_ordinal']} (published "
                     f"{e['before']['leftmost']} before the correction)")
        lines.append(f"  - correction: {e['flag_reason']}")
        if e.get('binding_evidence'):
            lines.append(f"  - evidence: {e['binding_evidence']}")
        rat = e.get('ratified')
        if rat:
            lines.append(f"  - ratified: **{str(rat.get('by') or 'owner')}**, {rat.get('date')} "
                         f"— marker retired")
            lines.append(f"  - ruling: {str(rat.get('ruling') or '').strip()}")
            if rat.get('decision'):
                lines.append(f"  - decision: {str(rat['decision']).strip()}")
        else:
            lines.append('  - ratified: no — the ⚑ marker stays on the page until the owner '
                         'rules on it')
    lines += ['', '## OPEN OWNER QUESTIONS', '',
              'Recorded, not fixed. Not verified against PEMS 2024; needs the owner\'s',
              'decision before the page is treated as final.', '',
              '- **Post-ROSC has no row for PEMS p.59#0** ("Follow Universal Patient Care…", badge',
              '  EMR) — missing row, not a level defect.',
              '- **p.61#4 and p.63#7 are compound rows — RESOLVED for the split rows (2026-11-20).**',
              '  The two printed rows carry one badge plus an inline level token scoping a clause',
              '  (`[EMR]` on the AED clause; `(I / P)` on the rhythm decision). A site row that',
              '  published the whole row could not be chipped without contradicting one half, so it',
              '  was flagged. Those rows are now split one clause per row (see *Rows split into one',
              '  action each*), each citing the printed row for its own clause, and `--check` only',
              '  counts a compound token that falls inside the clause the row quotes. A site row',
              '  that still publishes a whole compound row without a C2 `resolved_cells` decision',
              '  would still be flagged — none is left.',
              '- **Aortic Dissection & AAA (`04b`) has no PEMS 2024 protocol**: its source is',
              '  ODEMSA Section 2.5 (Revised 06/2015). It is converted to the 3-column chassis',
              '  with every row chipped `PENDING` (Pending OMD Authorization); see PENDING_OMD',
              '  above. The page must not be given a PEMS citation by any later pass.',
              '- **Aortic Dissection row 11 (Medical Control contact) is chipped `PENDING`, not',
              '  `MC`**, because this project\'s rule is one `PENDING` chip on every action row of',
              '  a page with no PEMS protocol. Owner ruling needed: is `PENDING` alone correct on',
              '  such a page, or should a Medical-Control row read `MC` + `PENDING` (both chips)?',
              '  Nothing on the page changes until the owner rules.',
              '- **`05_Stroke_TIA` rows 8 and 9 are agency additions** — PEMS 2024 p.131 prints 6',
              '  Stroke / TIA rows and neither "Establish 18g IV in Right AC" nor "Call COR at the',
              '  receiving hospital" is one of them. Owner ruling 2026-11-15: they are chipped',
              '  `PENDING` (Pending OMD Authorization), not given a level, and the ⚑ OWNER_REQUIRED',
              '  marker is removed because PENDING supersedes it. `carried_from_page` keeps the',
              '  level the page used to publish (row 8 `I`, row 9 `A`) as provenance only; see',
              '  PENDING_OMD — row-level above. This is NOT the whole-page case: the rest of the',
              '  Stroke page is PEMS-cited.',
              f'- **Whether every OWNER_REQUIRED row should become PENDING is UNANSWERED.** The',
              '  owner was asked and did not rule, so the other '
              f'{len(owner)} OWNER_REQUIRED rows keep their',
              '  level + ⚑ flag exactly as they were. Do not convert them without a ruling.',
              '- **Respiratory pages — the OWNER_REQUIRED rows that remain after the cross-page',
              '  pass.** PEMS 2024 prints one respiratory protocol (p.123-124) and one',
              '  inhalation-irritant protocol (p.153); the rest of these pages\' content is printed',
              '  in procedures (p.239, p.241, p.243, p.245, p.247, p.269) and other protocols',
              '  (Burns p.87-88, Sedation p.55). Where such a procedure prints the action it is now',
              '  cited (see *Cross-page citations*); where it does not, or prints it only across',
              '  rows of different levels, the row keeps the level the page published with its',
              '  reason in `row-bindings.yaml`. **After the 2026-11-20 row-structure pass no',
              '  respiratory row is flagged**: each bundled row is split and each half cites the',
              '  procedure row that prints it, and the four rows that were not actions moved below',
              '  their tables.',
              '- **Site-side `[X]` brackets — RESOLVED (owner ruling 2026-11-16).** The owner ruled',
              '  *"Add a second marker so [X] survives in the chassis"*. Bracketed rows now carry',
              '  the level chip plus a distinct `+MC` marker (see the `+MC` section above);',
              '  `row-bindings.yaml` is the source of truth and `--check` re-derives the bracketed',
              '  rows from the pre-conversion pages. A bracketed cell whose level is not the level',
              '  the row now publishes, or a row that is itself a Medical Control contact, cannot',
              '  carry `+MC` without changing its meaning — those rows say so explicitly under',
              '  *Bracketed rows whose bracket cannot be carried* above.',
              '- **Batch 4 — Burns row 6 (HF-burn calcium) is PENDING, not OWNER_REQUIRED.** The',
              '  page published no level at all, so there is no level to keep and flag. PEMS 2024',
              '  prints the HF calcium treatment only in the Burns protocol\'s PEARLS (p.87-88',
              '  prose), not as a level-badged row; the only table rows printing calcium chloride',
              '  1 g IV/IO over 3 minutes are p.91#5 (crush syndrome, badge [I]) and p.120#8',
              '  (CCB/BB overdose, badge I), whose indications differ. Confirm PENDING is preferred',
              '  over citing one of those rows across indications.',
              '- **Batch 4 — Electrical row 7 and Lightning row 7 — RESOLVED 2026-11-20.** Each',
              '  row printed a 12-lead ECG (p.96#8, badge EMT) and continuous rhythm monitoring',
              '  (p.96#11, badge I) as one action. Owner instruction: split rather than accept one',
              '  level. Row 7 is now the 12-lead at EMT and row 7a the rhythm monitoring at I on',
              '  both pages (see *Rows split into one action each*).',
              '- **Batch 4 — Trauma row 2 and row 6 — RESOLVED 2026-11-20.** Row 2 (scene safety +',
              '  extrication) is split: scene safety at EMR (p.49#1) and extrication at EMT',
              '  (p.91#7). Row 6 (assess shock / refer to Shock protocol) is recognition and',
              '  referral, not a numbered action, so it moved below the table into the page\u2019s',
              '  References & Good Practice block with no level (see *Rows moved below the action',
              '  table*).',
              '- **Batch 4 — Crush rows 4-5 carry `+MC` from brackets added on the level-scan',
              '  branch.** The [A]/[I] notation was added by ef540f9 after the branch base',
              '  768ad68, so this page\'s pre-conversion bracket set is recorded as `base_rev:',
              '  cf8af7a` in `exceptions.yaml`. Confirm the branch-added brackets are the owner\'s',
              '  intended notation and not a scanner artifact.',
              '- **Batch 4 — three cross-page citations reach procedures.** Hemorrhage rows 8-9',
              '  cite the Tourniquet Application procedure (p.273#6 EMR, p.273#7 MC) and Trauma',
              '  row 7 cites Universal Patient Care (p.50#9 A). Each cited row prints the action',
              '  verbatim; confirm citing a procedure for a protocol-page row is intended.',
              '- **Batch 5 — four card premises were wrong, and the tree/source were followed.**',
              '  (a) `07_Hypotension_Shock_Non_Trauma` was already converted in Batch 2; its two',
              '  remaining `sc-wrap` blocks are the Norepinephrine and Epinephrine DRIP CHARTS',
              '  (columns: Dose | Drops per minute) — dose tables, not level matrices, with no',
              '  action row to chip. They keep `sc-wrap` and are excluded from `TARGETS`. Confirm',
              '  a drip chart should never be converted. (b) `02_Diving_and_Drowning` did NOT need',
              '  OWNER_REQUIRED: PEMS p.93#6 prints "Contact Medical Control for transport',
              '  destination guidance if decompression injury is suspected" badged MC, so row 7',
              '  is cited, not flagged. (c) `02_Behavioral_Patient_Restraint` is not',
              '  admin-policy-only: PEMS p.71#2 prints "Restrain patient by least restrictive',
              '  means necessary. Refer to administrative policy Patient Restraint." at EMR and',
              '  p.71#4 prints de-escalation at EMR, so both are cited from the protocol row.',
              '  (d) the general/ scope is 6 pages, not 6-plus-medical: `grep` is the source.',
              '- **Batch 5 — Pain Control rows 6 and 7 now print `A` + `*` (PEMS `[A]` bracket),',
              '  down from the `I` the page published.** p.77#5 is the only row that prints',
              '  fentanyl/morphine and PEMS brackets its badge: AEMT, with agency training',
              '  documentation and Medical Control written authorisation. The one-chip chassis',
              '  cannot reproduce a bracket, so the asterisk note carries it. Owner to confirm',
              '  that the analgesia ladder is A+MC in PEMS and not I.',
              '- **Batch 5 — Sedation: ketamine is out, and the action table is p.55 verbatim',
              '  (owner ruling 2026-11-20).** Verbatim: *"Remove ketamine. We do not have RSI yet.',
              '  If Ketamine is in the pharm section. You can leave that alone."* Both ketamine',
              '  rows are gone with the drug — pre-intubation sedation (no PEMS 2024 row; p.123#4',
              '  says "RSI is not addressed in PEMS regional protocols") and post-intubation',
              '  ketamine (printed in exactly one PEMS row, p.72#9 behavioural restraint at P,',
              '  never as an airway sedative). No level was re-decided to clear them: the rows were',
              '  replaced by rows p.55 prints with their own badges, so the two OWNER_REQUIRED',
              '  flags left with the rows. The action table now publishes *Sedation Post Advanced',
              '  Airway* p.55 in printed order — EMR universal care (p.55#0), EMT airway',
              '  confirmation (p.55#1), I fentanyl 25 – 50 mcg / 0.5 – 1 mcg/kg max 25 mcg with',
              '  its printed',
              '  repeat cell (p.55#2), I midazolam 2.5 mg / 0.1 mg/kg, max 2.5 mg IV/IO or 5 mg',
              '  IN/IM, with its printed repeat cell (p.55#3), MC contact (p.55#4). The BP-',
              '  assessment row (Pain Control p.77#2) and the IV/IO-access row (Universal Patient',
              '  Care p.50#9) that the page used to carry are removed: p.55 prints neither, and an',
              '  A chip on IV access is a level the source does not badge. The page header,',
              '  Overview, Criteria and Differential sections are not printed on p.55 and are',
              '  unchanged by this pass. `docs/pharmacology/Ketamine.md` is out of scope by the',
              '  same ruling and untouched.',
              ] + cold_question_cards(ledger) + [
              '- **Batch 6 — administrative pages are chipped POLICY / PENDING, not levelled.**',
              '  Owner ruling 2026-11-16: *"Treat admin pages as policy."* All 14 administrative',
              '  pages are now 3-column tables whose marker column says `POLICY` (the rule is',
              '  printed in one of the 14 PEMS 2024 administrative policies) or `PENDING` (no',
              '  PEMS policy prints it). No provider level is published on those pages, so the',
              '  levels they used to show (mostly the cumulative EMR-through-P dot grid, which',
              '  was the same re-encoding defect the conversion removed elsewhere) are gone.',
              '  Every removed level is still recorded per row as `before.leftmost` above.',
              '- **Batch 6 — three of the 14 administrative policies ARE printed with provider',
              '  badges, and those badges are not republished.** PEMS prints Death & Criteria for',
              '  Withholding Resuscitation (p.21-22), Patient Refusal (p.27-28) and Trauma Field',
              '  Triage (p.43) as level-badged policy tables, not only as prose. Under the ruling',
              '  those rows are chipped `POLICY` like the rest, so the badge a reader could have',
              '  seen (EMT/I/MC on the Death and Refusal rows) is not on the site page. If the',
              '  owner wants those three pages levelled from the policy\'s own badges, that is a',
              '  second ruling and a small change: the badges are in pems_table.json and every',
              '  row prints its policy id here.',
              ] + admin_pending_cards(ledger) + [
              '- **Batch 6 — the STEMI page has one PEMS level, cited where printed.** STEMI row 7',
              '  (serial ECGs every 10 minutes) is not in the STEMI Field Triage policy; it is',
              '  printed verbatim as row p.107#9 of the Chest Pain protocol, badge MC, and is cited',
              '  there (`cross_page: true`). It is the only level chip left on an administrative',
              '  page, and the page note says why. Owner to confirm a protocol-row citation on a',
              '  policy page is preferable to a PENDING chip on a rule PEMS does print.',
              '- **Batch 6 — `07_Hypotension_Shock_Non_Trauma` needs no further conversion.** The',
              '  card inherited it for two remaining `sc-wrap` blocks; both are the',
              '  Norepinephrine/Epinephrine DRIP CHARTS (columns: Dose | Drops per minute with a',
              '  60-drop set). They are dose tables with no action row and no provider-level',
              '  column, so there is nothing to chip. The card premise (sc-wrap == unconverted',
              '  level matrix) is wrong here, exactly as Batch 5 reported.',
              '- **Batch 6 — "grep -rn sc-wrap docs/ returns nothing" cannot be the criterion.**',
              '  `sc-wrap` is the shared stylesheet wrapper for any wide table, used by ~80',
              '  non-level tables (pediatric dosing grids, COR phone lists, GCS tables, the SOP',
              '  pages). Converting or deleting them would edit clinical content the task forbids',
              '  touching. The check this batch enforces and reports instead: **zero level',
              '  matrices remain on `sc-wrap` anywhere under docs/** — i.e. no table whose header',
              '  is `| # | Action / Intervention | EMR | EMT | A | I | P |` still sits inside an',
              '  `sc-wrap`. At Batch 6 that count was not 0: 13 `docs/procedures/` pages still',
              '  carried the matrix, outside every batch\'s scope and only REPORTED. Batch 7',
              '  converted those 13, so the count is 0 now and `--check` gates every one of them;',
              '  the only page left outside the gate is the front-matter legend that defines the',
              '  level columns and is correct as it stands.',
              '- **Batch 6 — `rows_mc_required` = 8 is correct; the two "bracketed" Batch 5 rows',
              '  are a DIFFERENT bracket.** The 8 are page-cell brackets (`[X]` in the',
              '  pre-conversion site page) carrying the `+MC` marker. Pain Control rows 6-7 carry',
              '  an asterisk instead because the bracket is PEMS\'s, not the page\'s:',
              '  pems_table.json records p.77#5 `badge_tokens: ["[A]"]`, so the chip is `A` plus',
              '  the `*` source-bracket marker, and `+MC` (which means "this page printed the',
              '  level cell in brackets") would be a false statement about that row. Both',
              '  conventions are derived from data, not typed: `*` from the PEMS badge token,',
              '  `+MC` from row-bindings.yaml `mc_required` re-checked against the page\'s base',
              '  revision. No marker failed to apply.',
              '- **Batch 6 — Universal Patient Care row 11 moves EMT -> EMR.** The page printed',
              '  EMT-and-above for "Refer to relevant protocols / consider contacting Medical',
              '  Control"; PEMS p.49#5 badges the same sentence EMR. Chip follows the source, and',
              '  the move is listed under *Level moved by the source*. Its 11 row numbers are',
              '  unchanged, so the 34 inbound references from other pages (none of which point at',
              '  a row number or anchor) cannot break.',
              '- **Batch 7 — the 13 `docs/procedures/` pages are bound to the PEMS 2024',
              '  PROCEDURES section.** The card listed p.231, 235, 239, 241, 243, 245, 247, 249,',
              '  263, 269, 273 as the available rows; `pems_table.json` actually carries the whole',
              '  procedure section (p.231-275), and the page -> PEMS page binding was derived from',
              '  it (each page\'s `pems_pages` in `exceptions.yaml`, title-matched, plus the row',
              '  citations in `row-bindings.yaml`): CPAP p.245, Capnography p.241, Chest',
              '  Decompression p.243, Endotracheal Intubation p.247, Intraosseous p.249, Medication',
              '  Administration p.257-258, Nasogastric Tube p.259, Neonatal Resuscitation p.261,',
              '  Spinal Motion Restriction p.267, Surgical Airway p.269, Taser Barb Removal p.271,',
              '  Tourniquet p.273, Transcutaneous Pacing p.275. `Medical_Devices_Pumps.md`',
              '  (2-column Device | Action) and `Vaccination.md` (prose list, no table) carry no',
              '  level matrix and were left byte-identical.',
              '- **Batch 7 — 15 rows move to the level PEMS prints.** The rule is "chip = the',
              '  level PEMS prints", so the chip follows the source. 14 of these print a LOWER',
              '  level (more permissive) than the page published, and owner should confirm each',
              '  ladder: CPAP r6 `P -> EMT` (PEEP titration); Endotracheal Intubation r4 and r10',
              '  `P -> I` (adult oral intubation, analgesia/sedation: PEMS prints both inside',
              '  p.247#3 and p.247#9 at badge I); Intraosseous r8 `P -> A` (IO lidocaine); Medication',
              '  Administration r3 and r4 `I -> A` (IV and IO administration, p.257#3/#5 badge A);',
              '  Nasogastric Tube r1-r6 `P -> I` (the whole procedure is badge I on p.259); Neonatal',
              '  Resuscitation r2 and r4 `EMT -> EMR` (BVM and chest compressions, p.261#5/#9 badge',
              '  EMR). The 15th moves the other way: Endotracheal Intubation r2 `EMT -> I`,',
              '  because the row bundles a sentence PEMS prints at I (see the bundled-row rule',
              '  below) and an EMT chip would over-grant it. No row keeps a cumulative dot grid.',
              '- **Batch 7 — a row that bundles more than one PEMS level takes the HIGHEST level.**',
              '  One rule for every bundled row: the chip is the highest (most restrictive) of the',
              '  source levels the row prints, and the evidence names each sub-step level, so a',
              '  lower-level sentence can never be published under a lower chip. Applied to the',
              '  three bundled rows: ETT r2 `I` (C-spine sentence p.247#3 badge I, position step',
              '  p.247#2 badge EMT) — the EMT over-grant the earlier draft only disclosed is now',
              '  REMOVED from the page, since the chip is the higher level; ETT r6 `P` (escalation',
              '  p.247#7 badge P, re-oxygenate sentence p.247#6 badge I); Neonatal r3 `I` (ECG',
              '  p.261#7 badge I, EtCO2 sub-step p.261#6 badge EMT). All three are CITED rows, not',
              "  OWNER_REQUIRED; each row's `evidence` in `row-bindings.yaml` states the rule and",
              '  both levels.',
              '- **Batch 7 — CPAP units disagree with the source, and the action text was not',
              '  edited.** The page reads PEEP "5 cmH2O" (r3) and "5-15 cmH2O" (r6); PEMS p.245#1',
              '  prints "5 mmHg" and p.245#4 extracts as "titratingPEEP9%-15mmHg)". Reconciliation',
              '  (mmHg vs cmH2O, and 5-15 vs 9%-15) is a clinical-text decision outside this',
              '  conversion, so only the chip was bound; owner to reconcile the page wording.',
              '- **Pearl ruling 2026-11-17 + ketamine ruling 2026-11-20 and the row-structure',
              '  instruction — the "prints nowhere" bucket is empty.** It held 17 rows before the Pearl',
              '  ruling and 6 after it, and every one of those six has since left the action',
              '  table: the four guidance rows the owner moved below their pages\u2019 tables on',
              '  2026-11-20 (Pediatric Stridor r2 scene management, Pneumothorax r5 equipment',
              '  readiness, Upper Airway Obstruction r2 recognition, Trauma r6 assess shock \u2014',
              '  recorded in <code>audit/level-scan/relocated-rows.yaml</code>, not deleted), and',
              '  the two Sedation ketamine rows (r4 pre-intubation sedation, r5 post-intubation',
              '  ketamine), which the p.55 verbatim rewrite deleted with the drug. No converted',
              '  action row is left without a printed badge, so no row is counted in this',
              '  bucket and no OWNER_REQUIRED flag rests on a missing source row.']

    # Derived from `changed` so the prose can never disagree with the table above:
    # an MC -> other move and an other -> MC move are counted and named from data.
    lost_mc = [e for e in changed
               if e['before']['leftmost'] == 'MC' and e['level_published'] != 'MC']
    to_mc = [e for e in changed
             if e['level_published'] == 'MC' and e['before']['leftmost'] != 'MC']
    already_mc = [e for e in ledger if e['status'] == 'OK'
                  and e['level_published'] == 'MC'
                  and e['before']['leftmost'] == 'MC']

    def _mcrow(e):
        return f"`{e['file'].split('/')[-1]}` row {e['row']}"

    lines.append(f'- **Batch 3 — {len(lost_mc)} row(s) lost a Medical-Control requirement the '
                 'page printed.** Each is now chipped at the level PEMS prints:')
    for e in lost_mc:
        lines.append(f"  {_mcrow(e)} was `{e['before']['leftmost']}`, now "
                     f"`{e['level_published']}` (p.{e['pems_page']}#{e['pems_ordinal']}).")
    lines.append('  The rule is "chip = the level PEMS prints", and the source grants these '
                 'actions on standing order, but the owner should confirm that dropping a '
                 'page-printed MC requirement is intended.')
    if to_mc:
        lines.append('  Row(s) in the converted set that moved *to* MC, now matching the '
                     "source's MC row: "
                     + '; '.join(f"{_mcrow(e)} `{e['before']['leftmost']}` -> "
                                 f"`{e['level_published']}` "
                                 f"(p.{e['pems_page']}#{e['pems_ordinal']})" for e in to_mc)
                     + '.')
    if already_mc:
        lines.append('  Already `MC` on the page and matching the source, so not moved '
                     '(converted set, whole list): '
                     + '; '.join(f"{_mcrow(e)} (p.{e['pems_page']}#{e['pems_ordinal']})"
                                 for e in already_mc) + '.')
    lines += [
              '- **Batch 3 — four rows published no level at all** (Respiratory Arrest r11, r14,',
              '  r15; Smoke Inhalation r8). There was nothing to keep, so each is bound to the row',
              '  that prints the action: p.269#0 (Surgical Airway, already a C2 ruling), p.55#2',
              '  (Fentanyl), p.55#3 (Midazolam), p.88#8 (Hydroxocobalamin). Confirm that binding a',
              '  level-less row is preferred over chipping it PENDING.']
    exc = load_verifier_exceptions()
    lines += ['', '## Verifier exceptions (known, documented, enforced)', '',
              'Defects the audit artifacts carry that `scripts/verify_pems_canonical.py` is told',
              'to expect, one record each. A leak not listed here fails the verifier, and a listed',
              'entry that stops reproducing also fails it, so this list cannot go stale or hide a',
              'new defect. Source of truth: `audit/level-scan/verifier-exceptions.yaml`.', '']
    if not exc:
        lines.append('None — the verifier tolerates no badge-bleed leak.')
    for e in exc:
        lines.append(f"- **p.{e.get('page')} #{e.get('ordinal')}** "
                     f"({e.get('section_heading') or 'unnamed section'}): the PEMS margin badge "
                     f"word bleeds into the recorded row text. {e.get('reason')}")

    # --------------------------------------------------------------- whole-site totals
    sw_files, sw_blocks, sw_matrices = sc_wrap_audit()
    pol_rows_all = [e for e in ledger if e['status'] == 'policy']
    lines += ['', '## Whole-site totals (derived from the ledger, not typed)', '',
              '| metric | value |', '|---|---:|',
              f'| converted pages — protocol/procedure chassis | {len(TARGETS) + len(PENDING_TARGETS)} |',
              f'| converted pages — administrative policy (POLICY/PENDING) | '
              f'{len(policy_targets())} |',
              f'| action rows — total | {len(ledger)} |',
              f'| action rows relocated out of an action table (still on the page, not in '
              f'this ledger — `relocated-rows.yaml`) | {len(load_relocated())} |',
              f'| cited to a PEMS protocol row (incl. cross-page) | '
              f"{sum(1 for e in ledger if e['status'] == 'OK')} |",
              f'| cross-page citations | {sum(1 for e in ledger if e.get("cross_page"))} |',
              f'| POLICY (PEMS administrative policy) | {len(pol_rows_all)} |',
              f'| PENDING (no PEMS source: whole page + row-level + administrative) | '
              f"{sum(1 for e in ledger if e['status'] in ('pending_omd', 'pending_row_omd'))} |",
              f'| OWNER_REQUIRED | {sum(1 for e in ledger if e["status"] == "OWNER_REQUIRED")} |',
              f'| rows moved below the action table (References & Good Practice) | {len(reloc)} |',
              f'| OWNER_RULED | {sum(1 for e in ledger if e["status"] == "owner_ruled")} |',
              f'| +MC markers | {sum(1 for e in ledger if e.get("mc_required"))} |',
              '', '### `sc-wrap` — whole `docs/` tree, walked (not a directory list)', '',
              f'{sw_blocks} `sc-wrap` block(s) in {len(sw_files)} file(s). `sc-wrap` is the '
              'shared stylesheet wrapper for any wide table, so its presence is not a defect: '
              'the defect is a provider-level matrix still inside one. '
              f'**Provider-level matrices inside `sc-wrap`: {len(sw_matrices)}** — '
              + str(sum(1 for m in sw_matrices
                        if m.split(' (line')[0]
                        in set(TARGETS + PENDING_TARGETS + policy_targets())))
              + ' on a page this project has converted (0 expected; `--check` fails on any), '
              "the rest on page(s) outside every batch's scope and reported, not gated "
              "(since Batch 7 that is only the front-matter legend, which defines the level "
              "columns and is labelled by the owner's ruling — R / B / A / I / P since "
              "2026-11-20 — never converted to one chip per row).", '']
    for m in sw_matrices:
        lines.append(f'- {m}')
    lines.append('')
    lines.append('Files still carrying `sc-wrap` (all non-level tables — dose charts, phone '
                 'lists, SOP grids, GCS and screening tables): ' +
                 ', '.join(f'`{f}`' for f in sw_files) + '.')
    return '\n'.join(lines) + '\n'


def check_ledger_markdown(ledger, fails):
    """The committed ledger markdown must be exactly what `emit_md()` derives, and the two
    owner-facing Batch-5/Batch-6 cards must state the ledger's own state.

    The cards are copied verbatim into the page the owner reads, so a stale card is a
    published false reason. This guard is what makes that a `--check` failure: hand-edit
    the markdown (or forget to regenerate after a ruling) and the comparison fails; change
    a row's status so a card's claim no longer holds and the assertions below fail.
    """
    path = os.path.join(AUD, 'level-rule-ledger.md')
    try:
        disk = open(path, encoding='utf-8').read()
    except FileNotFoundError:
        fails.append('audit/level-scan/level-rule-ledger.md is missing — the owner-facing '
                     'open-question cards live in it')
        return
    md = emit_md(ledger)
    if disk != md:
        import difflib
        diff = [l for l in difflib.unified_diff(disk.split('\n'), md.split('\n'),
                                                'level-rule-ledger.md', 'emit_md(ledger)',
                                                lineterm='', n=0)][:10]
        fails.append('audit/level-scan/level-rule-ledger.md != what emit_md() derives from '
                     'level-rule-ledger.json — re-run `scripts/level_rule.py --write`:\n    '
                     + '\n    '.join(diff))
    section = disk.split('## OPEN OWNER QUESTIONS', 1)
    section = section[1].split('\n## ', 1)[0] if len(section) > 1 else ''
    ruled = disk.split(COLD_RULED_HEADER, 1)
    ruled = ruled[1].split('\n## ', 1)[0] if len(ruled) > 1 else ''
    facts = open_question_facts(ledger)
    cold = facts['cold_by_row']
    # a row the card says is still flagged must really be flagged
    if all(cold.get(n) is not None and cold[n]['status'] == 'owner_ruled' for n in (6, 9)):
        for stale in ('Cold Exposure rows 6 and 9 are OWNER_REQUIRED',
                      'no PEMS row anywhere prints heat packs'):
            if stale in section:
                fails.append(f'OPEN OWNER QUESTIONS still publishes the pre-ruling claim '
                             f'{stale!r} although Cold Exposure rows 6 and 9 are owner_ruled '
                             f'in the ledger')
        for n in (6, 9):
            head = f'p.{cold[n]["prose_citations"][0]["page"]} ' \
                   f'{cold[n]["prose_citations"][0]["heading"]} ' \
                   f'#{cold[n]["prose_citations"][0]["ordinal"]}' \
                if cold[n].get('prose_citations') else None
            if head and head not in section:
                fails.append(f'OPEN OWNER QUESTIONS omits the verbatim citation {head} that '
                             f'clears Cold Exposure row {n}')
    elif cold.get(6) is None and any(r['row'] == 6 for r in load_relocated()):
        # Row 6 left the ledger with the pilot relocation and the owner has RULED (EMR,
        # 2026-11-20). The record must sit in the OWNER_RULED section and must NOT sit in the
        # open questions — the page the owner reads is titled "decisions still waiting on
        # you", so a decided card there is a published falsehood (review round 3, 2026-11-20).
        if 'Cold Exposure rows 6 and 9' not in ruled:
            fails.append('OWNER_RULED no longer names Cold Exposure rows 6 and 9, which '
                         '`relocated-rows.yaml` records as moved into the page\'s '
                         'References & Good Practice block')
        ruled_cards = cold_ruled_cards(ledger)
        if not ruled_cards:
            fails.append('OWNER_RULED carries no Cold Exposure ruling card although '
                         '`level-rulings.yaml` records the 2026-11-20 answer (EMR)')
        for card in ruled_cards:
            if card not in ruled:
                fails.append('OWNER_RULED drops a Cold Exposure card the ruling derives — '
                             'the relocation record or the 2026-11-20 ASKED/ANSWERED card')
            if card in section:
                fails.append('OPEN OWNER QUESTIONS still publishes a DECIDED Cold Exposure '
                             'card — the owner answered on 2026-11-20 (`EMR`); it belongs in '
                             'the ledger\'s OWNER_RULED section, not in the open questions '
                             'the owner is asked to answer')
        for card in cold_question_cards(ledger):
            if card not in section:
                fails.append('OPEN OWNER QUESTIONS drops a Cold Exposure card that is still '
                             'open (a relocation the page does not carry, or a floor '
                             'question the owner has not answered)')
        # the level the page prints, the level the audit trail records and the level the
        # ruling records must be one number: a relocation cannot drift away from its ruling.
        rulings = load_rulings()
        for n, moved in sorted(_cold_relocated_rows().items()):
            rul = rulings.get((moved['file'], str(n))) or {}
            if rul and rul.get('level') != moved['level']:
                fails.append(f'`relocated-rows.yaml` records Cold Exposure row {n} at '
                             f'{moved["level"]!r} but `level-rulings.yaml` rules it '
                             f'{rul["level"]!r} — the page, the relocation record and the '
                             f'ruling must state one level')
    # the administrative card's count and row set must be the ledger's
    n_admin = len(facts['admin_pending'])
    if n_admin and f'the {n_admin} administrative PENDING row(s)' not in section:
        fails.append(f'OPEN OWNER QUESTIONS does not state the ledger\'s administrative '
                     f'PENDING count ({n_admin})')
    for e in facts['admin_pending']:
        name = ADMIN_PAGE_NAME.get(e['file'].split('/')[-1])
        if name and not re.search(re.escape(name) + r' rows? [\d,\-]+', section):
            fails.append(f'OPEN OWNER QUESTIONS omits administrative PENDING row '
                         f'{name} {e["row"]}')


def check():
    align, adjudicated = load_json('alignment.json'), load_json('adjudicated.json')
    pems = pems_index(load_json('pems_table.json'))
    rulings, bindings = load_rulings(), load_bindings()
    prose = load_prose()
    row_pending = load_row_pending()
    try:
        ledger_rows = load_json('level-rule-ledger.json')['rows']
    except FileNotFoundError:
        ledger_rows = []
    led = {(e['file'], str(e['row'])): e for e in ledger_rows}

    fails, report, pending_row_rows, ruling_cites = [], [], [], []
    check_ledger_markdown(ledger_rows, fails)
    # Every relocated row's `proves` spans must be printed on its page. The Cold card
    # already reads them, but the Pulmonary rows had no reader at all, so a reworded page
    # could orphan the record silently. One rule for every relocated row.
    for rec in load_relocated():
        missing = relocated_proofs_missing(rec)
        if missing:
            fails.append(f'`relocated-rows.yaml` {rec["file"]} row {rec["row"]}: the page '
                         f'does not print {", ".join(repr(s) for s in missing)} — the '
                         f'relocation record describes a block the page no longer carries')
    kept_words, removed_words = load_token_decisions()
    seen_kept = {}
    for rel in TARGETS:
        path = os.path.join(DOCS, rel)
        raw = open(path, encoding='utf-8').read()
        base = base_brackets(rel)
        if rel in AUDIT_ONLY_PROVENANCE and 'Source: PEMS 2024' in raw:
            fails.append(f'{rel}: the reader-facing "Source: PEMS 2024 ..." paragraph is back '
                         f'on the page — the owner\'s 2026-11-20 ruling removed it from the '
                         f'published product; the citation belongs in audit/level-scan/ '
                         f'(`level-rulings.yaml`, `relocated-rows.yaml`), not on the page')
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
        mc_rows, cross_rows = [], []
        for row, r in zip(rows, res):
            chips = CHIP_RE.findall(row['level_cell'] or '')
            if len(chips) != 1:
                fails.append(f'{rel} row {row["ordinal"]}: {len(chips)} level markers, expected 1')
                continue
            level = chips[0][1]
            # --- the +MC marker: a bracketed page cell must survive the collapse -------
            cell = row['level_cell'] or ''
            n_mc = cell.count('lvl-mc-req')
            b = bindings.get((rel, str(row['ordinal']))) or {}
            want_mc = bool(b.get('mc_required')) and bool(base.get(str(row['ordinal'])) == level) \
                and level not in ('PENDING', 'MC')
            if want_mc and n_mc != 1:
                fails.append(f'{rel} row {row["ordinal"]}: the page printed this level cell in '
                             f'brackets and row-bindings.yaml marks it mc_required, but the '
                             f'chip carries {n_mc} +MC markers, expected exactly 1')
            if not want_mc and n_mc:
                fails.append(f'{rel} row {row["ordinal"]}: chip carries a +MC marker but '
                             f'row-bindings.yaml does not mark the row mc_required')
            if n_mc > 1:
                fails.append(f'{rel} row {row["ordinal"]}: {n_mc} +MC markers, expected 1')
            if b.get('mc_required') and level == 'MC':
                fails.append(f'{rel} row {row["ordinal"]}: mc_required on an MC chip — the '
                             f'action is itself a Medical Control contact, so a +MC marker '
                             f'would duplicate it; use mc_bracket_excluded')
            brk = base.get(str(row['ordinal']))
            if brk and not b.get('mc_required') and not b.get('mc_bracket_excluded'):
                fails.append(f'{rel} row {row["ordinal"]}: the page printed a bracketed level '
                             f'cell ({brk}) and the row neither carries mc_required nor says '
                             f'in row-bindings.yaml why the bracket cannot be carried '
                             f'(mc_bracket_excluded)')
            # --- cross-page citation ---------------------------------------------------
            if b.get('pems_page') is not None:
                gp = governing_pages(rel, align)
                is_cross = int(b['pems_page']) not in gp
                if is_cross and not b.get('cross_page'):
                    fails.append(f'{rel} row {row["ordinal"]}: cites p.{b["pems_page"]}#'
                                 f'{b["pems_ordinal"]}, outside this page\'s own source '
                                 f'{sorted(gp)}, but is not marked cross_page: true')
                if b.get('cross_page') and not is_cross:
                    fails.append(f'{rel} row {row["ordinal"]}: marked cross_page: true but '
                                 f'p.{b["pems_page"]} IS this page\'s own source {sorted(gp)}')
                if b.get('cross_page') or b.get('quoted_row_text'):
                    q = b.get('quoted_row_text')
                    src = pems.get((b['pems_page'], b['pems_ordinal']))
                    if src is None:
                        fails.append(f'{rel} row {row["ordinal"]}: cites p.{b["pems_page"]}#'
                                     f'{b["pems_ordinal"]}, which is not in pems_table.json')
                    elif not q:
                        fails.append(f'{rel} row {row["ordinal"]}: this row publishes one '
                                     f'clause of a PEMS row but records no quoted_row_text — '
                                     f'quote the clause it publishes so the chip can be '
                                     f'checked against it')
                    elif not quote_in(q, src):
                        fails.append(f'{rel} row {row["ordinal"]}: quoted_row_text is not a '
                                     f'verbatim span of the cited row p.{b["pems_page"]}#'
                                     f'{b["pems_ordinal"]} — the citation does not rest on '
                                     f'the source\'s own words')
                    if src is not None and r['badge'] is not None and r['pems_row'] is not None:
                        # the chip must be the badge the cited row prints
                        if b['pems_page'] != (r['ptr'] or (None, None))[0]:
                            fails.append(f'{rel} row {row["ordinal"]}: cross_page binding and '
                                         f'resolved pointer disagree')
                    cross_rows.append({'row': row['ordinal'], 'level': level,
                                       'pems': f'p.{b["pems_page"]}#{b["pems_ordinal"]}',
                                       'badge': (r['badge'] or None),
                                       'quoted': b.get('quoted_row_text')})
            if want_mc:
                mc_rows.append({'row': row['ordinal'], 'level': level,
                                'bracket': brk})
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
            rp = row_pending.get((rel, str(row['ordinal'])))
            if rp:
                # an agency addition on an otherwise PEMS-cited page: PENDING and nothing
                # else. No level chip, no OWNER_REQUIRED flag (PENDING supersedes it), no
                # PEMS citation, and the carried level must match both the yaml and the
                # ledger's record of what the page published before conversion.
                if level != 'PENDING':
                    fails.append(f'{rel} row {row["ordinal"]}: marked pending in '
                                 f'pending-protocols.yaml but the chip reads {level}')
                if 'lvl-own' in (row['level_cell'] or ''):
                    fails.append(f'{rel} row {row["ordinal"]}: PENDING row still carries the '
                                 f'OWNER_REQUIRED marker (PENDING supersedes it)')
                if 'lvl-req' in (row['level_cell'] or ''):
                    fails.append(f'{rel} row {row["ordinal"]}: PENDING row carries the '
                                 f'bracketed-badge marker')
                if re.search(r'\bp\.\s?\d+', row['action']):
                    fails.append(f'{rel} row {row["ordinal"]}: action text names a PEMS page — '
                                 f'a pending row may not claim a PEMS citation')
                e = led.get((rel, str(row['ordinal'])))
                if e is None:
                    fails.append(f'{rel} row {row["ordinal"]}: pending row missing from the ledger')
                else:
                    if e['status'] != 'pending_row_omd':
                        fails.append(f'{rel} row {row["ordinal"]}: ledger says {e["status"]}, '
                                     f'the page is chipped PENDING')
                    if e.get('pems_page') or e.get('pems_ordinal') or e.get('pems_badge'):
                        fails.append(f'{rel} row {row["ordinal"]}: pending ledger row claims a '
                                     f'PEMS citation (p.{e.get("pems_page")}#'
                                     f'{e.get("pems_ordinal")}, badge {e.get("pems_badge")})')
                    if not e.get('reason'):
                        fails.append(f'{rel} row {row["ordinal"]}: pending row has no reason in '
                                     f'the ledger')
                    if e.get('carried_from_page') != rp['carried_from_page']:
                        fails.append(f'{rel} row {row["ordinal"]}: ledger carried_from_page '
                                     f'{e.get("carried_from_page")} != pending-protocols.yaml '
                                     f'{rp["carried_from_page"]}')
                    before = (e.get('before') or {}).get('leftmost')
                    if before and before != rp['carried_from_page']:
                        fails.append(f'{rel} row {row["ordinal"]}: pending-protocols.yaml '
                                     f'carried_from_page {rp["carried_from_page"]} != the level '
                                     f'the page published before conversion {before}')
                pending_row_rows.append({'row': row['ordinal'], 'chip': 'PENDING',
                                         'carried_from_page': rp['carried_from_page'],
                                         'reason': rp['reason']})
                continue
            if level == 'PENDING':
                fails.append(f'{rel} row {row["ordinal"]}: chipped PENDING but there is no '
                             f'row-level entry for it in pending-protocols.yaml')
            if ruled:
                want_level = ruled['level']
                if want_level == 'FLOOR':
                    want_level, _chips, _rows = page_floor(rel)
                if level != want_level:
                    fails.append(f'{rel} row {row["ordinal"]}: marker {level} != owner ruling '
                                 f'{want_level}')
                if 'lvl-own' in (row['level_cell'] or ''):
                    fails.append(f'{rel} row {row["ordinal"]}: owner-ruled row still carries '
                                 f'the OWNER_REQUIRED marker')
                # a ruling must rest on printed prose: the citation is verified verbatim
                # against the prose index, so a ruling can no longer be free text.
                cites = check_prose_citations(rel, f'row {row["ordinal"]}',
                                              ruled.get('prose_citations'), prose, fails)
                lf = ruled.get('level_from')
                if r['badge'] is not None and not cites and not lf:
                    fails.append(f'{rel} row {row["ordinal"]}: owner ruling recorded but PEMS '
                                 f'row {r["ptr"]} already badges it and the ruling records no '
                                 f'prose citation — ruling is stale')
                if lf:
                    src = pems.get((lf['page'], lf['ordinal']))
                    if src is None:
                        fails.append(f'{rel} row {row["ordinal"]}: ruling level_from '
                                     f'p.{lf["page"]}#{lf["ordinal"]} is not in '
                                     f'pems_table.json')
                    else:
                        badge, _brk = badge_of(src)
                        if badge != want_level:
                            fails.append(f'{rel} row {row["ordinal"]}: ruling level '
                                         f'{want_level} != the badge p.{lf["page"]}#'
                                         f'{lf["ordinal"]} prints ({badge})')
                e = led.get((rel, str(row['ordinal'])))
                if e is None:
                    fails.append(f'{rel} row {row["ordinal"]}: owner_ruled row missing from '
                                 f'the ledger')
                else:
                    if e['status'] != 'owner_ruled':
                        fails.append(f'{rel} row {row["ordinal"]}: ledger says {e["status"]}, '
                                     f'level-rulings.yaml rounds it owner_ruled')
                    if e.get('pems_page') or e.get('pems_ordinal') or e.get('pems_badge'):
                        fails.append(f'{rel} row {row["ordinal"]}: owner_ruled ledger row '
                                     f'claims a PEMS row citation (p.{e.get("pems_page")}#'
                                     f'{e.get("pems_ordinal")}) — a ruling is not a citation')
                    # one source of truth: the ledger must carry the yaml's own citations
                    want = [(int(c['page']), str(c['heading']).upper(), int(c['ordinal']))
                            for c in (ruled.get('prose_citations') or [])]
                    got = [(c['page'], c['heading'], c['ordinal'])
                           for c in (e.get('prose_citations') or [])]
                    if want != got:
                        fails.append(f'{rel} row {row["ordinal"]}: ledger prose citations '
                                     f'{got} != level-rulings.yaml {want}')
                ruled_rows.append({'row': row['ordinal'], 'level': level, 'status': 'owner_ruled',
                                   'prose': [f"p.{c['page']} {c['heading']} #{c['ordinal']}"
                                             for c in cites]})
                if cites:
                    ruling_cites.append({'file': rel, 'row': row['ordinal'],
                                         'level': level,
                                         'citations': [f"p.{c['page']} {c['heading']} "
                                                       f"#{c['ordinal']}" for c in cites]})
                continue

            resolved_level = cells_level((r['resolved'] or {}).get('resolved_cells'))
            tokens = compound_tokens(r['pems_row'],
                                     (r['extra'].get('binding') or {}).get('quoted_row_text'))
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
            # a CORRECTED row: the chip IS the cited badge, and the flag records the
            # history. Three states are distinguished, and only these three:
            #   flag + no ratified  -> the marker MUST be on the chip
            #   flag + ratified     -> the marker MUST be gone (retired by the owner)
            #   no flag             -> the marker must be absent
            binding = r['extra'].get('binding') or {}
            b_flag = binding.get('flag')
            b_rat = binding.get('ratified')
            has_fix = 'lvl-fix' in (row['level_cell'] or '')
            if b_flag and not b_rat and not has_fix:
                fails.append(f'{rel} row {row["ordinal"]}: row-bindings.yaml flags this row as '
                             f'a correction, it is not owner-ratified, and the chip does not '
                             f'carry the flag')
            if b_flag and b_rat and has_fix:
                fails.append(f'{rel} row {row["ordinal"]}: the owner ratified this correction '
                             f'on {b_rat.get("date")} and retired the marker, but the chip '
                             f'still carries the CORRECTED flag')
            if b_rat and not b_flag:
                fails.append(f'{rel} row {row["ordinal"]}: ratification recorded without the '
                             f'correction it ratifies')
            if has_fix and not b_flag:
                fails.append(f'{rel} row {row["ordinal"]}: the chip carries the correction flag '
                             f'but row-bindings.yaml does not declare one')
            if b_flag:
                e_fix = led.get((rel, str(row['ordinal'])))
                if e_fix is None or e_fix.get('flag_reason') != b_flag:
                    fails.append(f'{rel} row {row["ordinal"]}: the ledger does not record the '
                                 f'binding\'s flag reason')
                else:
                    if (e_fix.get('pems_page'), e_fix.get('pems_ordinal')) != \
                            (binding.get('pems_page'), binding.get('pems_ordinal')):
                        fails.append(f'{rel} row {row["ordinal"]}: the ledger does not record '
                                     f'the printed page the correction was checked against')
                    if bool(e_fix.get('ratified')) != bool(b_rat):
                        fails.append(f'{rel} row {row["ordinal"]}: ledger ratification record '
                                     f'does not match row-bindings.yaml')
                    elif b_rat:
                        got = e_fix.get('ratified') or {}
                        for k in ('date', 'by', 'ruling'):
                            if str(got.get(k) or '').strip() != str(b_rat.get(k) or '').strip():
                                fails.append(f'{rel} row {row["ordinal"]}: ledger ratified '
                                             f'{k} does not match row-bindings.yaml')
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
                       'owner_required': owner_rows, 'owner_ruled': ruled_rows,
                       'mc_required': mc_rows, 'cross_page': cross_rows})

    # ------------------------------------------------- administrative-policy pages
    # Owner ruling 2026-11-16: "Treat admin pages as policy: cite PEMS administrative
    # policies where they exist, PENDING where the policy is ours." So on these pages the
    # marker is POLICY (a PEMS administrative policy prints the rule) or PENDING (no PEMS
    # policy prints it), and never a provider level: there is no protocol row to badge.
    policy_report = []
    for rel in policy_targets():
        path = os.path.join(DOCS, rel)
        if not os.path.exists(path):
            fails.append(f'{rel}: administrative page listed in exceptions.yaml but missing')
            continue
        raw = open(path, encoding='utf-8').read()
        if POLICY_HEADER not in raw:
            fails.append(f'{rel}: no policy table ({POLICY_HEADER!r} missing)')
        if NEW_HEADER in raw:
            fails.append(f'{rel}: administrative page carries the provider-level header '
                         f'{NEW_HEADER!r} — its rows are POLICY or PENDING, not a level')
        if DIV_OPEN in raw:
            fails.append(f'{rel}: administrative page still uses the provider-level '
                         f'{DIV_OPEN!r} chassis')
        if re.search(r'^\|\s*#\s*\|\s*Action\s*/\s*Intervention\s*\|\s*EMR\s*\|', raw, re.M):
            fails.append(f'{rel}: legacy 5-column level matrix still present')
        regions = find_regions(raw.split('\n'))
        if not regions:
            fails.append(f'{rel}: no level-table region found')
        if any(is_banner(r) for reg in regions for r in reg['rows']):
            fails.append(f'{rel}: section banner still encoded as a table row')
        rows = [r for reg in regions for r in reg['rows'] if not is_banner(r)]
        if not rows:
            fails.append(f'{rel}: no action rows found')
        pol_rows, pend_rows, xpage_rows, seen = [], [], [], set()
        for row in rows:
            ordn = str(row['ordinal'])
            seen.add(ordn)
            chips = CHIP_RE.findall(row['level_cell'] or '')
            if len(chips) != 1:
                fails.append(f'{rel} row {ordn}: {len(chips)} markers, expected 1')
                continue
            level, cell = chips[0][1], row['level_cell'] or ''
            for mark in ('lvl-own', 'lvl-req', 'lvl-mc-req'):
                if mark in cell:
                    fails.append(f'{rel} row {ordn}: a POLICY/PENDING chip may not carry the '
                                 f'provider-level marker {mark}')
            b = bindings.get((rel, ordn)) or {}
            rp = row_pending.get((rel, ordn))
            e = led.get((rel, ordn))
            if TEXT_TOKEN.search(row['action']):
                fails.append(f'{rel} row {ordn}: level token left in the action text')
            hits = level_hits(row['action'])
            allowed = kept_words.get((rel, ordn), [])
            for hit in hits:
                if hit not in allowed:
                    fails.append(f'{rel} row {ordn}: level word {hit!r} left in the action '
                                 f'text with no keep decision in '
                                 f'audit/level-scan/token-decisions.yaml')
            for a in allowed:
                if a in hits:
                    seen_kept[(rel, ordn, a)] = True
            if b.get('policy') and rp:
                fails.append(f'{rel} row {ordn}: cites policy {b["policy"]!r} and is also '
                             f'listed as a PENDING row in pending-protocols.yaml')
            if b.get('policy'):
                if level != 'POLICY':
                    fails.append(f'{rel} row {ordn}: row-bindings.yaml cites policy '
                                 f'{b["policy"]!r} but the chip reads {level}')
                if not POLICY_CHIP in cell:
                    fails.append(f'{rel} row {ordn}: POLICY chip is not {POLICY_CHIP!r}')
                if e is None:
                    fails.append(f'{rel} row {ordn}: POLICY row missing from the ledger')
                else:
                    if e['status'] != 'policy':
                        fails.append(f'{rel} row {ordn}: ledger says {e["status"]}, the page '
                                     f'is chipped POLICY')
                    if e.get('pems_page') or e.get('pems_ordinal') or e.get('pems_badge'):
                        fails.append(f'{rel} row {ordn}: POLICY ledger row also claims a '
                                     f'protocol citation (p.{e.get("pems_page")}#'
                                     f'{e.get("pems_ordinal")}) — an administrative-policy row '
                                     f'may not carry one')
                    if e.get('policy') != b['policy']:
                        fails.append(f'{rel} row {ordn}: ledger policy {e.get("policy")!r} != '
                                     f'row-bindings.yaml {b["policy"]!r}')
                    if norm_quote(e.get('policy_quote')) != norm_quote(b.get('policy_quote')):
                        fails.append(f'{rel} row {ordn}: ledger quote and row-bindings.yaml '
                                     f'quote disagree')
                pol_rows.append({'row': ordn, 'policy': b['policy'],
                                 'pages': policies()[b['policy']]['pages']})
            elif rp:
                if level != 'PENDING':
                    fails.append(f'{rel} row {ordn}: listed as a PENDING row in '
                                 f'pending-protocols.yaml but the chip reads {level}')
                if e is None:
                    fails.append(f'{rel} row {ordn}: PENDING row missing from the ledger')
                else:
                    if e['status'] != 'pending_row_omd':
                        fails.append(f'{rel} row {ordn}: ledger says {e["status"]}, the page '
                                     f'is chipped PENDING')
                    if not e.get('reason'):
                        fails.append(f'{rel} row {ordn}: PENDING row has no reason')
                    if e.get('policy'):
                        fails.append(f'{rel} row {ordn}: PENDING row carries a policy '
                                     f'reference ({e["policy"]!r}) — PENDING means no PEMS '
                                     f'policy prints it')
                    if e.get('pems_page') or e.get('pems_ordinal'):
                        fails.append(f'{rel} row {ordn}: PENDING row claims a PEMS citation')
                    before = (e.get('before') or {}).get('leftmost')
                    if before and before != rp['carried_from_page']:
                        fails.append(f'{rel} row {ordn}: carried_from_page '
                                     f'{rp["carried_from_page"]} != the level the page '
                                     f'published before conversion {before}')
                pend_rows.append({'row': ordn, 'reason': rp['reason'],
                                  'carried_from_page': rp['carried_from_page']})
            elif b.get('pems_page') is not None:
                # a rule the policies do not print but a level-badged PROTOCOL row does:
                # cited where printed (owner ruling 2026-11-16), chip = that row's badge
                src = pems.get((b['pems_page'], b['pems_ordinal']))
                if src is None:
                    fails.append(f'{rel} row {ordn}: cites p.{b["pems_page"]}#'
                                 f'{b["pems_ordinal"]}, which is not in pems_table.json')
                else:
                    badge, _ = badge_of(src)
                    if level != badge:
                        fails.append(f'{rel} row {ordn}: chip {level} != the badge '
                                     f'p.{b["pems_page"]}#{b["pems_ordinal"]} prints ({badge})')
                    q = b.get('quoted_row_text') or ''
                    if not q:
                        fails.append(f'{rel} row {ordn}: cross-page citation without '
                                     f'quoted_row_text')
                    elif not quote_in(q, src):
                        fails.append(f'{rel} row {ordn}: quoted_row_text is not a verbatim '
                                     f'span of the cited row p.{b["pems_page"]}#'
                                     f'{b["pems_ordinal"]}')
                if not b.get('cross_page'):
                    fails.append(f'{rel} row {ordn}: cites a protocol row and is not marked '
                                 f'cross_page: true')
                if e is None or e['status'] not in ('OK',):
                    fails.append(f'{rel} row {ordn}: cross-page citation, ledger says '
                                 f'{e["status"] if e else "missing"}')
                elif (e.get('pems_page'), e.get('pems_ordinal')) != (b['pems_page'],
                                                                     b['pems_ordinal']):
                    fails.append(f'{rel} row {ordn}: ledger cites '
                                 f'p.{e.get("pems_page")}#{e.get("pems_ordinal")} != '
                                 f'row-bindings.yaml p.{b["pems_page"]}#{b["pems_ordinal"]}')
                xpage_rows.append({'row': ordn, 'protocol': b['pems_page'],
                                   'ordinal': b['pems_ordinal'], 'level': level})
            elif level in ('POLICY', 'PENDING'):
                fails.append(f'{rel} row {ordn}: chipped {level} but the row is neither a '
                             f'POLICY citation (row-bindings.yaml `policy:`) nor a recorded '
                             f'PENDING row (pending-protocols.yaml `rows:`)')
        for (f, r), b in bindings.items():
            if f == rel and b.get('policy') and r not in seen:
                fails.append(f'{rel}: row-bindings.yaml cites policy {b["policy"]!r} for row '
                             f'{r}, which is not an action row on the page')
        for (f, r), rp in row_pending.items():
            if f == rel and r not in seen:
                fails.append(f'{rel}: pending-protocols.yaml lists row {r}, which is not an '
                             f'action row on the page')
        policy_report.append({'file': rel, 'rows': len(rows),
                              'policy': pol_rows, 'pending': pend_rows,
                              'cross_page': xpage_rows})

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

    # ------------------------------------------------------------- relocated rows
    # A row that moved below the action table has to be provably still on the page, and
    # provably gone from the action table and the ledger. `proves` is the page's own words,
    # so an edited-away block fails here instead of leaving a permanent record of a move
    # that no longer describes the page.
    relocated = load_relocated()
    reloc_rows = []
    for rec in relocated:
        rel, num = rec['file'], str(rec['row'])
        miss = relocated_proofs_missing(rec)
        if miss:
            fails.append(f'{rel} row {num}: relocated-rows.yaml records this row as moved below '
                         f'the table, but the page does not print '
                         + ', '.join(repr(s) for s in miss))
            continue
        path = os.path.join(DOCS, rel)
        if not os.path.exists(path):
            fails.append(f'{rel}: relocated-rows.yaml names a page that does not exist')
            continue
        rows = [r for reg in find_regions(open(path, encoding='utf-8').read().split('\n'))
                for r in reg['rows'] if not is_banner(r)]
        if any(str(r['ordinal']) == num for r in rows):
            fails.append(f'{rel} row {num}: recorded as relocated, but the action table still '
                         f'carries that row number — the move did not happen')
        if (rel, num) in led:
            fails.append(f'{rel} row {num}: recorded as relocated, but the ledger still lists '
                         f'it as an action row (re-run scripts/level_rule.py --write)')
        reloc_rows.append({'file': rel, 'row': rec['row'], 'where': rec['where'],
                           'level': rec.get('level'), 'guidance': bool(rec.get('guidance'))})

    # ------------------------------------------------------------ site row splits
    # Every split a page carries is recorded in row-splits.yaml `site_splits:` with the PEMS
    # row each part cites. The chip must be that row's badge (not a level typed into the
    # file), the part's words must be on the page, and no un-recorded lettered row may
    # exist — a split that only lives in the page is a renumbering nobody can audit.
    site_splits = load_site_splits()
    split_rows = []
    recorded = set()
    for rec in site_splits:
        rel = rec['file']
        path = os.path.join(DOCS, rel)
        if not os.path.exists(path):
            fails.append(f'{rel}: row-splits.yaml site_splits names a page that does not exist')
            continue
        by_num = {}
        for reg in find_regions(open(path, encoding='utf-8').read().split('\n')):
            for r in reg['rows']:
                if not is_banner(r):
                    by_num[str(r['ordinal'])] = r
        for p in rec['parts']:
            num = str(p['row'])
            recorded.add((rel, num))
            label = f'{rel} row {num}'
            row = by_num.get(num)
            if row is None:
                fails.append(f'{label}: named as a split part in row-splits.yaml but the page '
                             f'carries no such row')
                continue
            chips = CHIP_RE.findall(row['level_cell'] or '')
            if len(chips) != 1:
                fails.append(f'{label}: {len(chips)} level markers, expected 1')
            elif chips[0][1] != p['level']:
                fails.append(f'{label}: chip {chips[0][1]} != the level row-splits.yaml '
                             f'records for this part ({p["level"]})')
            if norm_row_text(p['text']) not in norm_row_text(row['action']):
                fails.append(f'{label}: the part text recorded in row-splits.yaml is not what '
                             f'the page prints: {p["text"]!r}')
            m = re.match(r'^p\.(\d+)#(\d+)$', str(p['pems']).strip())
            if p.get('source') == 'ruling':
                # the level is a recorded owner decision, not a printed badge: the ruling
                # must exist at that level, and where it names a printed row the part must
                # name the same one.
                rul = rulings.get((rel, num))
                if rul is None:
                    fails.append(f'{label}: recorded as a `ruling` part but level-rulings.yaml '
                                 f'has no ruling for it')
                elif rul['level'] != p['level']:
                    fails.append(f'{label}: row-splits.yaml records level {p["level"]} but '
                                 f'level-rulings.yaml rules {rul["level"]}')
                elif m and rul.get('level_from') and \
                        (rul['level_from'].get('page'), rul['level_from'].get('ordinal')) != \
                        (int(m.group(1)), int(m.group(2))):
                    fails.append(f'{label}: row-splits.yaml names {p["pems"]} but the ruling '
                                 f'is adopted from p.{rul["level_from"].get("page")}#'
                                 f'{rul["level_from"].get("ordinal")}')
                split_rows.append({'file': rel, 'parent': rec['row'], 'row': num,
                                   'level': p['level'], 'pems': str(p['pems']),
                                   'source': 'ruling'})
                continue
            if p.get('source') == 'owner_required':
                # The source prints the action but scopes it in the row's own words inside
                # a cell badged for another clause (or two printed rows disagree about its
                # level). That is the compound-row case this checker refuses to chip as
                # cited, so the part keeps the level the source's words give it and stays
                # flagged: the citation is the row that PRINTS the action, not a badge.
                b = bindings.get((rel, num)) or {}
                if b.get('status') != 'owner_required':
                    fails.append(f'{label}: recorded as an `owner_required` part but '
                                 f'row-bindings.yaml does not declare it owner_required')
                elif not str(b.get('reason') or '').strip():
                    fails.append(f'{label}: owner_required in row-bindings.yaml without a reason')
                if (rel, num) in rulings:
                    fails.append(f'{label}: recorded as `owner_required` but level-rulings.yaml '
                                 f'still rules it {rulings[(rel, num)]["level"]} — a level '
                                 f'cannot be both an open decision and an owner ruling')
                split_rows.append({'file': rel, 'parent': rec['row'], 'row': num,
                                   'level': p['level'], 'pems': str(p['pems']),
                                   'source': 'owner_required'})
                continue
            if not m:
                fails.append(f'{label}: pems {p["pems"]!r} is not written p.<page>#<ordinal>')
                continue
            key = (int(m.group(1)), int(m.group(2)))
            src = pems.get(key)
            if src is None:
                fails.append(f'{label}: the cited PEMS row p.{key[0]}#{key[1]} is not in '
                             f'pems_table.json')
                continue
            badge, _brk = badge_of(src)
            if badge != p['level']:
                fails.append(f'{label}: row-splits.yaml records level {p["level"]}, but the '
                             f'cited PEMS row p.{key[0]}#{key[1]} prints {badge}')
            b = bindings.get((rel, num)) or {}
            if (b.get('pems_page'), b.get('pems_ordinal')) != key:
                fails.append(f'{label}: the page row does not cite p.{key[0]}#{key[1]} in '
                             f'row-bindings.yaml (it cites p.{b.get("pems_page")}#'
                             f'{b.get("pems_ordinal")}) — the split record and the citation '
                             f'disagree')
            split_rows.append({'file': rel, 'parent': rec['row'], 'row': num,
                               'level': p['level'], 'pems': str(p['pems'])})
    # the other direction: a lettered row on a converted page that no split record explains
    for rel in TARGETS:
        path = os.path.join(DOCS, rel)
        if not os.path.exists(path):
            continue
        for reg in find_regions(open(path, encoding='utf-8').read().split('\n')):
            for r in reg['rows']:
                num = str(r['ordinal'])
                if not is_banner(r) and not num.isdigit() and (rel, num) not in recorded:
                    fails.append(f'{rel} row {num}: a lettered sub-row with no entry in '
                                 f'row-splits.yaml `site_splits` — a split may not exist only '
                                 f'on the page')

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

    # no provider-level matrix may survive inside an `sc-wrap` block anywhere under
    # docs/ on a page this project has converted. Every page that carries one is in
    # scope now: the protocol batches, the administrative policies, and (Batch 7) the
    # 13 docs/procedures/ pages. The only page left is the front-matter legend, which
    # DEFINES the level columns (relabelled R / B / A / I / P by the owner's 2026-11-20
    # ruling) and is never converted to one chip per row — it is counted and
    # reported, never silently passed off as clean.
    sw_files, sw_blocks, sw_matrices = sc_wrap_audit()
    in_scope = set(TARGETS + PENDING_TARGETS + policy_targets())
    sw_out_of_scope = []
    for m in sw_matrices:
        rel = m.split(' (line')[0]
        if rel in in_scope:
            fails.append(f'{m}: a provider-level matrix is still wrapped in sc-wrap')
        else:
            sw_out_of_scope.append(m)

    # a keep decision may not point at a page or row that is not in scope
    for (f, row), words in kept_words.items():
        if f not in set(TARGETS + PENDING_TARGETS + policy_targets()):
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
        'ruling_prose_citations': ruling_cites,
        'rows_mc_required': sum(len(r.get('mc_required') or []) for r in report),
        'rows_cross_page': sum(len(r.get('cross_page') or []) for r in report),
        'policy_pages': len(policy_report),
        'policy_rows_total': sum(r['rows'] for r in policy_report),
        'rows_policy': sum(len(r['policy']) for r in policy_report),
        'rows_policy_pending': sum(len(r['pending']) for r in policy_report),
        'policies_cited': sorted({p['policy'] for r in policy_report for p in r['policy']}),
        'policy_report': policy_report,
        'sc_wrap_files': len(sw_files),
        'sc_wrap_blocks': sw_blocks,
        'sc_wrap_level_matrices': sw_matrices,
        'sc_wrap_level_matrices_out_of_scope': sw_out_of_scope,
        'sc_wrap_files_list': sw_files,
        'cross_page_citations': [{'file': r['file'], 'row': c['row'], 'pems': c['pems'],
                                  'level': c['level'], 'quoted_row_text': c['quoted']}
                                 for r in report for c in (r.get('cross_page') or [])],
        'mc_required_rows': [{'file': r['file'], 'row': c['row'], 'level': c['level'],
                              'bracket': c['bracket']}
                             for r in report for c in (r.get('mc_required') or [])],
        'pending_pages': len(PENDING_TARGETS),
        'rows_pending_omd': sum(len(r['pending']) for r in pending_report),
        'pending': pending_report,
        'rows_pending_row_omd': len(pending_row_rows),
        'pending_row_level': pending_row_rows,
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
        'rows_relocated': len(reloc_rows),
        'relocated': reloc_rows,
        'site_split_parents': len(site_splits),
        'site_split_rows': split_rows,
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
    print(f"OK — {summary['rows_mc_required']} row(s) carry the +MC marker (a bracketed page "
          f"level cell: that level performs the action only with Medical Control authorisation), "
          f"exactly one marker each.")
    print(f"OK — {len(ruling_cites)} owner_ruled row(s) cite unbadged PEMS prose by page + "
          f"heading + ordinal, each quoting a verbatim span of its indexed entry "
          f"({sum(len(c['citations']) for c in ruling_cites)} citation(s) checked against "
          f"audit/level-scan/pems_prose.json); 0 rulings rest on free text.")
    print(f"OK — {summary['rows_cross_page']} row(s) are cited across pages (cross_page: true), "
          f"each with the cited row's own words quoted verbatim out of pems_table.json.")
    n_own = sum(1 for r in summary['site_split_rows'] if r.get('source') == 'owner_required')
    own_txt = (f'; {n_own} of them are flagged OWNER_REQUIRED because PEMS scopes the action '
               f'inside a row badged for another clause (the split record says so)'
               if n_own else '')
    print(f"OK — {summary['site_split_parents']} bundled row(s) are split into "
          f"{len(summary['site_split_rows'])} sub-rows, each one action; every part cites the "
          f"PEMS 2024 row that prints it and its chip is that row's badge "
          f"(row-splits.yaml `site_splits`, re-read against the pages){own_txt}.")
    print(f"OK — {summary['rows_relocated']} row(s) moved out of an action table into a "
          f"References & Good Practice block; each is recorded in relocated-rows.yaml with "
          f"page text that proves the block is still printed, and none is still in the ledger "
          f"as an action row.")
    print(f"OK — {summary['rows_pending_omd']} action rows across "
          f"{summary['pending_pages']} page(s) are chipped PENDING (Pending OMD Authorization) "
          f"because PEMS 2024 publishes no such protocol; 0 of them claim a PEMS citation.")
    print(f"OK — {summary['rows_pending_row_omd']} action row(s) on an otherwise PEMS-cited "
          f"page are chipped PENDING as agency additions awaiting OMD authorization "
          f"(pending-protocols.yaml `rows:`); 0 of them claim a PEMS citation.")
    print(f"OK — {summary['policy_pages']} administrative-policy page(s) carry "
          f"{summary['policy_rows_total']} action rows: {summary['rows_policy']} chipped POLICY "
          f"(cited to one of {len(summary['policies_cited'])} PEMS 2024 administrative "
          f"policies, each with a verbatim quote out of that policy's own pages), "
          f"{summary['rows_policy_pending']} chipped PENDING (no PEMS policy prints the rule). "
          f"0 of them publish a provider level and 0 of them claim a protocol citation.")
    print(f"OK — sc-wrap: {summary['sc_wrap_blocks']} wide-table block(s) in "
          f"{summary['sc_wrap_files']} docs file(s) — mostly dose charts, phone lists and SOP "
          f"tables that are not level matrices; 0 provider-level matrices on an sc-wrap on any "
          f"page this project has converted.")
    print(f"REPORTED, NOT GATED — "
          f"{len(summary['sc_wrap_level_matrices_out_of_scope'])} provider-level matrix/matrices "
          f"inside sc-wrap remain on a page outside every conversion batch's scope "
          f"(the front-matter legend, which DEFINES the level columns — R / B / A / I / P):")
    for m in summary['sc_wrap_level_matrices_out_of_scope']:
        print('   -', m)
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
    for rel in policy_targets():
        _regions_out, ledger, problems, _lines, _regions = plan(rel)
        bad += problems
        all_ledger += ledger
        if args.map:
            print(f'== {rel}  (administrative policy)')
            for e in ledger:
                print(f'   {e["row"]:>3} {e["status"]:<14} level={str(e["level_published"]):<8} '
                      f'before_leftmost={str(e["before"]["leftmost"]):<4} '
                      f'policy={e.get("policy") or "-"}')
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
        # What did the ledger say about each row BEFORE this run? Read the committed one
        # (`HEAD`), not the working copy a previous --write in this run may have already
        # overwritten — otherwise the before -> after report lies about its own baseline.
        prior = {}
        try:
            raw = subprocess.run(['git', '-C', ROOT, 'show',
                                  'HEAD:audit/level-scan/level-rule-ledger.json'],
                                 capture_output=True, text=True, check=True).stdout
            prior = {(e['file'], str(e['row'])): e.get('status')
                     for e in json.loads(raw)['rows']}
        except (subprocess.CalledProcessError, ValueError, KeyError):
            try:
                prior = {(e['file'], str(e['row'])): e.get('status')
                         for e in load_json('level-rule-ledger.json')['rows']}
            except (FileNotFoundError, KeyError):
                prior = {}
        # A baseline already recorded in the ledger is carried forward, never recomputed:
        # a later --write must not move the "before" line it is being compared against.
        try:
            carried = {(e['file'], str(e['row'])): e.get('status_before')
                       for e in load_json('level-rule-ledger.json')['rows']}
        except (FileNotFoundError, KeyError):
            carried = {}
        for rel in TARGETS:
            splice(rel)
        for rel in policy_targets():
            splice(rel)
        for rel in PENDING_TARGETS:
            splice_pending(rel, pending_specs[rel])
            _r, ledger, _p, _l, _g = plan_pending(rel, pending_specs[rel])
            all_ledger += ledger
        for e in all_ledger:
            key = (e['file'], str(e['row']))
            # A row already in the ledger keeps the status_before it recorded, even when
            # that value is None (a newly converted page had no flags to clear). Only a
            # row absent from the ledger falls back to the status at HEAD.
            e['status_before'] = carried[key] if key in carried else prior.get(key)
        out = os.path.join(AUD, 'level-rule-ledger.json')
        with open(out, 'w', encoding='utf-8') as fh:
            json.dump({'generated_by': 'scripts/level_rule.py',
                       'rule': 'one marker per action = the lowest provider level PEMS 2024 '
                               'prints for that action',
                       'targets': TARGETS,
                       'pending_targets': PENDING_TARGETS,
                       'verifier_exceptions': load_verifier_exceptions(),
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
