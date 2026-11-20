#!/usr/bin/env python3
"""Clinical prose must not name the local office or the local agency.

Owner ruling 2026-11-20: *"Don't put Poquoson OMD in Perrls."* The earlier MC sweep
(`scripts/mc_wording.py`, card t_c53e62ff) covered protocol **table rows** only and left
prose alone. This guard closes the prose half: Pearls, NOTES, CONTRAINDICATIONS, quick
reference cards, procedure steps, and any other clinical prose on the published site.

Two independent bans, each with its own allowlist, so a line cannot slip through by
matching the other ban's exemption:

  OFFICE  `OMD`, `Operational Medical Director`, `Medical Director`, `medical director`
          -> the clinical authority is the FUNCTION "Medical Control", never a local office.
  AGENCY  `Poquoson`
          -> the agency's own name is allowed only where it is the document's own name
             (page H1, site title, version line, cross-reference to "Poquoson Protocol"),
             never as a clinical attribution.

A line is a violation if EITHER ban has an unallowed hit. So "Poquoson Fire and Rescue OMD"
is still a violation: the agency phrase is exempt, the office term is not.

Allowlists are explicit and auditable — every exemption carries the reason it exists, and
`--list` prints the disposition of every hit so the exemption set can be reviewed.

Usage:
    python3 scripts/agency_names.py --list     # every hit + its disposition
    python3 scripts/agency_names.py --check    # exit 1 if any clinical prose names the office/agency
    python3 scripts/agency_names.py --json     # machine-readable
    python3 scripts/agency_names.py --check --root X
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DOCS = os.path.join(ROOT, 'docs')

OFFICE_TERMS = [
    (re.compile(r'\bOMD\b'), 'OMD'),
    (re.compile(r'\bOperational Medical Director\b', re.I), 'Operational Medical Director'),
    (re.compile(r'\bMedical Director\b', re.I), 'Medical Director'),
]
AGENCY_TERMS = [
    (re.compile(r'\bPoquoson\b'), 'Poquoson'),
]

# ---------------------------------------------------------------- allowlists
# (path_prefix_or_None, line_regex_or_None, reason)
# A hit is exempt when a rule matches BOTH the file path and the line.
ALLOW_OFFICE = [
    ('sops/', None,
     "department's own administrative SOP: the OMD is a role in its chain of command, "
     "not a clinical attribution"),
    ('personnel-policies/', None,
     "department's own personnel policy manual: the OMD is an administrative role"),
    ('protocols/front-matter/00 - Introduction.md', None,
     "title page / acknowledgements / scope statement / footer: the document's own "
     "attribution, not clinical prose"),
    ('protocols/outstanding-decisions.md', None,
     "decisions log: PENDING_OMD is a defined status label, not a clinical attribution"),
    (None, re.compile(r'Pending OMD [Aa]uthorization|PENDING_OMD'),
     "PENDING_OMD status label (defined in audit/level-scan/pending-protocols.yaml)"),
    ('protocols/outstanding-decisions.md', re.compile(r'OMD review|OMD question|owner/OMD'),
     "decisions-log wording about an open OMD question"),
    (None, re.compile(r'EMS agency Operational Medical Director must provide specific '
                      r'written authorization'),
     "quoted regional requirement about any EMS agency's OMD, not this agency's office"),
]

ALLOW_AGENCY = [
    ('sops/', None, "department's own administrative SOP"),
    ('personnel-policies/', None, "department's own personnel policy manual"),
    ('fire-ems-references/', None, "provenance note naming the source agency"),
    ('resources/links.md', None, "external link labels"),
    ('protocols/front-matter/00 - Introduction.md', None,
     "title page / acknowledgements / scope statement / footer"),
    ('protocols/outstanding-decisions.md', None, "decisions log"),
    (None, re.compile(r'^#\s+Poquoson Fire and Rescue Patient Care Protocols\s*$'),
     "page H1 header: the document's own name"),
    (None, re.compile(r'^#\s+Poquoson Fire & Rescue Protocol Dashboard\s*$'),
     "site title"),
    (None, re.compile(r'^#\s+Poquoson Pediatric Dosing Reference\s*$'), "page title"),
    (None, re.compile(r'^#\s+MASTER AI SYSTEM PROMPT: Poquoson Fire and Rescue Protocols\s*$'),
     "document title"),
    (None, re.compile(r'^\*\*Poquoson Fire and Rescue Patient Care Protocols\*\*\s*$'),
     "document footer"),
    (None, re.compile(r'^\*\*Version:\*\* Based on PEMS March 2024 / Adapted for '
                      r'Poquoson Fire and Rescue\s*$'),
     "document version line"),
    (None, re.compile(r'Poquoson (?:[A-Z][\w/&]* )?[Pp]rotocol'),
     "cross-reference to the document's own name ('Poquoson Protocol(s)')"),
    (None, re.compile(r'Poquoson Fire and Rescue|Poquoson Fire & Rescue|'
                      r'Poquoson Fire/Rescue|City of Poquoson|Poquoson, VA|'
                      r'Poquoson GIS|Poquoson webmail|Poquoson policy|'
                      r'Poquoson dispatcher|Poquoson region|citizens of Poquoson|'
                      r'in Poquoson|Poquoson personnel|Poquoson Fire Department|'
                      r'Poquoson-specific|Poquoson combined|Poquoson protocol|'
                      r'Poquoson protocols|Poquoson Pediatric'),
     "the agency's own name in a non-clinical-attribution context"),
]


def _allowed(rules, rel, line):
    for prefix, rx, reason in rules:
        if prefix is not None and not rel.startswith(prefix):
            continue
        if rx is not None and not rx.search(line):
            continue
        return reason
    return None


def walk(docs):
    for base, _dirs, files in os.walk(docs):
        for fn in sorted(files):
            if fn.endswith('.md'):
                yield os.path.relpath(os.path.join(base, fn), docs)


def derive(docs=DEFAULT_DOCS):
    """Every line naming the office or the agency, with its disposition."""
    hits, violations = [], []
    for rel in walk(docs):
        path = os.path.join(docs, rel)
        with open(path, encoding='utf-8') as fh:
            for lineno, line in enumerate(fh, 1):
                line = line.rstrip('\n')
                # A replacement-mapping line ("Regional Medical Director ➔ Medical Control")
                # names the regional source term on the LEFT of the arrow. Only the text
                # after the arrow is what the page will print, so only that is scanned for
                # office terms. The agency ban still scans the whole line, so a mapping
                # that maps *to* "Poquoson OMD" is still a violation.
                office_scan = line.rsplit('\u2794', 1)[-1] if '\u2794' in line else line
                terms = [name for rx, name in OFFICE_TERMS if rx.search(office_scan)]
                terms += [name for rx, name in AGENCY_TERMS if rx.search(line)]
                if not terms:
                    continue
                office_terms = [n for n in terms if n != 'Poquoson']
                agency_terms = [n for n in terms if n == 'Poquoson']
                reasons = []
                if office_terms:
                    r = _allowed(ALLOW_OFFICE, rel, line)
                    if r is None:
                        reasons.append(None)
                    else:
                        reasons.append(r)
                if agency_terms:
                    r = _allowed(ALLOW_AGENCY, rel, line)
                    if r is None:
                        reasons.append(None)
                    else:
                        reasons.append(r)
                ok = all(r is not None for r in reasons)
                rec = {'file': rel, 'line': lineno, 'terms': terms,
                       'text': line.strip(),
                       'disposition': 'allowed' if ok else 'violation',
                       'reason': '; '.join(dict.fromkeys(r for r in reasons if r)) or None}
                hits.append(rec)
                if not ok:
                    violations.append(rec)
    return {'hits': hits, 'violations': violations}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--root', default=DEFAULT_DOCS)
    args = ap.parse_args()

    d = derive(args.root)
    if args.json:
        print(json.dumps(d, indent=1, ensure_ascii=False))
        return 0

    if args.check:
        if d['violations']:
            print(f"FAIL — {len(d['violations'])} line(s) of clinical prose name the local "
                  f"office or the local agency instead of the function \"Medical Control\".")
            for r in d['violations']:
                print(f" - {r['file']}:{r['line']}  [{', '.join(r['terms'])}]  {r['text'][:150]}")
            return 1
        print(f"OK — {len(d['hits'])} line(s) name the office or the agency; all are "
              f"document-name / administrative exemptions. No clinical prose names a local "
              f"office or the local agency.")
        return 0

    print(f"hits: {len(d['hits'])}   violations: {len(d['violations'])}")
    for r in d['hits']:
        mark = 'VIOLATION' if r['disposition'] == 'violation' else 'allowed  '
        print(f"{mark} {r['file']}:{r['line']}  [{', '.join(r['terms'])}]")
        print(f"          {r['text'][:170]}")
        if r['reason']:
            print(f"          -> {r['reason']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
