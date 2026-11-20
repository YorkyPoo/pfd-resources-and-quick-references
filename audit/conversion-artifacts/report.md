# Internal conversion artifacts removed from the published site

Card `t_a733bb2e`. Found while sweeping agency names out of clinical prose (`t_a3c436f6`).

Two classes of internal conversion artifact were reachable on the public GitHub Pages
build. Neither is clinical prose, so the agency-name sweep (`scripts/agency_names.py`,
`.md` only) left them alone.

## Decision

| class | count found | decision |
|---|---:|---|
| `docs/protocols/**/<name>_report.json` | **54** | moved to `audit/conversion-reports/protocols/…` (path structure preserved); out of `docs/`, therefore out of the build |
| replacement-mapping block on a clinical page | 1 page, 4 lines | removed from the page; the mapping stays in `protocols/front-matter/00 - AI Formatting Guidelines.md`, which is where it is defined |

The card named 6 `*_report.json` files because it listed the ones that still printed
"Poquoson OMD". **All 54** `*_report.json` under `docs/` are the same class of artifact —
per-protocol conversion QA output — and all 54 were being copied verbatim into `site/`
(MkDocs publishes every non-Markdown file under `docs/`). They are all moved.

Nothing in the repo read them: `grep -rn "_report.json" --include='*.md' docs/ scripts/`
returns no reference, and no other code globs `docs/**/*_report.json`.

## What was removed from the page

`docs/protocols/respiratory/03_Respiratory_Distress_PROC.md` ended with 4 published lines
(`### Mandatory Text Replacements Applied` + 3 `➔` bullets). The last one was:

```
### Mandatory Text Replacements Applied      <- line 87 (heading)
- Peninsula EMS / PEMS ➔ Poquoson Fire and Rescue
- PEMS Medical Advisory Committee / Regional Medical Director ➔ Medical Control
- Regional Protocol(s) ➔ Poquoson Protocol(s)
```

Gone, and the page now ends on Pearl 10. The page built from the tip carries no mapping
block and no `➔` character.

## Why the existing guard did not see either

`scripts/agency_names.py` scans `.md` only — the `.json` files are invisible to it. And for
a mapping line it deliberately scans only the text right of `➔` (the source term on the
left is never printed), so the block passed its two bans clean: after the sweep, the three
bullets read `Poquoson Fire and Rescue` / `Medical Control` / `Poquoson Protocol(s)`, all
allowlisted shapes.

## New guard

`scripts/internal_artifacts.py --check` — fails the build if either class returns:

* any `*_report.json` under `docs/`;
* any `Mandatory Text Replacements` heading, or any `➔` mapping line naming PEMS /
  Regional / Peninsula, outside `protocols/front-matter/`.

Verified against the real pre-fix tree (the `agency-names` tip worktree), not a synthetic
probe: **58 findings, EXIT=1** (54 reports + 4 mapping lines). Against this branch:
**0 findings, EXIT=0**.

## Gates at this branch tip

| gate | EXIT |
|---|---:|
| `scripts/verify_pems_canonical.py` | 0 |
| `scripts/level_rule.py --check` | 0 |
| `scripts/mc_wording.py --check` | 0 |
| `scripts/agency_names.py --check` | 0 |
| `scripts/internal_artifacts.py --check` | 0 |
| `mkdocs build --strict` | 0 |
| `scripts/build_outstanding_decisions.py --check` | 1 (inherited; byte-identical output on `agency-names` tip) |

`verify_pems_canonical.py` reads `audit/level-scan/.cache/pems_rows.jsonl`, a git-ignored
build cache: in a worktree without it the gate reports `.cache/pems_rows.jsonl exists`
FAIL. Regenerating it (`python3 scripts/pems_canonical.py --stage all`) makes the gate
pass, but that regeneration also rewrites the tracked `audit/level-scan/alignment.json`
and `pems_table.json`, so those regenerated copies were reverted — the committed artifacts
are unchanged by this card.

## Content checks

Measured against the published `preview/agency-names` slot on `gh-pages` (built from the
`agency-names` tip) for "before", and against this branch's own `mkdocs build --strict`
output for "after".

| check | before (`agency-names` tip) | after (this branch) |
|---|---:|---:|
| `grep -rn "Poquoson OMD" docs/` | 3 hits (one line in each of 3 `*_report.json`) | **0** |
| `*_report.json` built into the site | 54 | **0** |
| files in the built site naming "Poquoson OMD" | 3 | **0** |
| `Mandatory Text Replacements` in the built respiratory page | present (3 HTML matches) | **absent** |
| mapping lines on the page source | 4 | **0** |
| `audit/conversion-reports/**` naming "Poquoson OMD" | — | 3 (unpublished, kept as the findings they are) |

The 3 moved reports that name the office keep that wording: they are the QA notes that
raised the question, and they are now outside the published tree by construction.
