#!/usr/bin/env python3
"""Internal conversion artifacts must never reach the published docs tree.

Two artifact classes leaked onto the public site and were only found by hand:

1. **Conversion QA reports.** `docs/protocols/**/<name>_report.json` — the
   per-protocol output of the PEMS->Poquoson conversion pass ("recommendation":
   "Verify if the 40 mg/kg dose is authorized by the Poquoson OMD …"). MkDocs
   copies every non-Markdown file under `docs/` verbatim, so these were served
   as static files and still named the local office. They live in
   `audit/conversion-reports/` now.

2. **The replacement-mapping block.** The build instruction from
   `protocols/front-matter/00 - AI Formatting Guidelines.md` ("### Mandatory
   Text Replacements Applied" + the `➔` mapping bullets) was pasted onto
   `protocols/respiratory/03_Respiratory_Distress_PROC.md`. The mapping belongs
   in the formatting guidelines page only; a clinical page must not print it.

3. **The AI build prompt itself.** The same
   `protocols/front-matter/00 - AI Formatting Guidelines.md` is the conversion
   build instruction, not clinical content. It stays in the repo as the
   conversion spec but must not be published. MkDocs builds every Markdown file
   under `docs/`, not only the ones listed in `nav`, so leaving it out of the
   nav is not enough: `mkdocs.yml` excludes it with `exclude_docs`, and
   `--site` fails if a built page for it still exists.

`scripts/agency_names.py` could not catch either: it scans `.md` only, and inside
a mapping line it deliberately scans only the text right of `➔` (the source term
on the left is never printed), so a mapping block passes it clean.

Usage:
    python3 scripts/internal_artifacts.py --check    # exit 1 on any artifact
    python3 scripts/internal_artifacts.py --check --site site   # also scan a build
    python3 scripts/internal_artifacts.py --list
    python3 scripts/internal_artifacts.py --json
    python3 scripts/internal_artifacts.py --check --root X
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DOCS = os.path.join(ROOT, 'docs')

# Paths allowed to carry the replacement mapping: the guidelines that DEFINE it.
MAPPING_ALLOWED = ('protocols/front-matter/',)

# Static files that are never content, whatever they are called.
ARTIFACT_GLOBS = ('*_report.json',)

MAPPING_HEADING = 'Mandatory Text Replacements'
MAPPING_ARROW = '\u2794'          # ➔

# Source files that must never be published, even though they stay in docs/.
# The AI formatting guidelines are the conversion build prompt, not clinical
# content; the owner ruled it adds friction for a medic scrolling front matter.
EXCLUDED_SOURCES = (
    'protocols/front-matter/00 - AI Formatting Guidelines.md',
)


def walk(docs):
    for base, _dirs, files in os.walk(docs):
        for fn in sorted(files):
            yield os.path.relpath(os.path.join(base, fn), docs)


def derive(docs=DEFAULT_DOCS):
    findings = []
    for rel in walk(docs):
        slash = rel.replace(os.sep, '/')
        name = os.path.basename(rel)

        for pat in ARTIFACT_GLOBS:
            if fnmatch.fnmatch(name, pat):
                findings.append({
                    'file': slash, 'line': None, 'kind': 'conversion-report',
                    'text': name,
                    'reason': 'conversion QA report served as a static file; '
                              'belongs in audit/conversion-reports/',
                })

        if not name.endswith('.md'):
            continue
        if slash.startswith(MAPPING_ALLOWED):
            continue

        with open(os.path.join(docs, rel), encoding='utf-8') as fh:
            for lineno, line in enumerate(fh, 1):
                text = line.strip()
                is_heading = text.lstrip('#').strip().lower().startswith(
                    MAPPING_HEADING.lower())
                is_mapping = MAPPING_ARROW in text and (
                    'PEMS' in text or 'Regional' in text or 'Peninsula' in text)
                if is_heading or is_mapping:
                    findings.append({
                        'file': slash, 'line': lineno, 'kind': 'replacement-mapping',
                        'text': text[:160],
                        'reason': 'replacement mapping belongs in the formatting '
                                  'guidelines, not on a provider-facing page',
                    })
    return {'findings': findings}


def derive_built(site):
    """Built pages for sources that must stay unpublished.

    MkDocs writes `<stem>.html` with `use_directory_urls: false` and
    `<stem>/index.html` with the default. Check both so the guard does not
    depend on that setting.
    """
    findings = []
    for src in EXCLUDED_SOURCES:
        stem = src[:-3] if src.endswith('.md') else src
        for cand in (os.path.join(site, stem + '.html'),
                     os.path.join(site, stem, 'index.html')):
            if os.path.isfile(cand):
                findings.append({
                    'file': os.path.relpath(cand, site).replace(os.sep, '/'),
                    'line': None, 'kind': 'excluded-page-built',
                    'text': src,
                    'reason': 'source is excluded from the published site but a '
                              'built page exists for it',
                })
    return {'findings': findings}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--root', default=DEFAULT_DOCS)
    ap.add_argument('--site', default=None,
                    help='built site directory to scan for excluded pages')
    args = ap.parse_args()

    d = derive(args.root)
    if args.site:
        d['findings'].extend(derive_built(args.site)['findings'])
    f = d['findings']
    if args.json:
        print(json.dumps(d, indent=1, ensure_ascii=False))
        return 0

    if args.check:
        if f:
            print(f"FAIL — {len(f)} internal conversion artifact(s) published under docs/")
            for r in f:
                where = f":{r['line']}" if r['line'] else ''
                print(f" - {r['file']}{where}  [{r['kind']}] {r['text']}")
            return 1
        print("OK — no conversion QA reports, no replacement-mapping block under docs/, "
              "and no built page for an excluded source")
        return 0

    print(f"findings: {len(f)}")
    for r in f:
        where = f":{r['line']}" if r['line'] else ''
        print(f"  {r['kind']:20s} {r['file']}{where}  {r['text']}")
        print(f"  {'':20s} -> {r['reason']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
