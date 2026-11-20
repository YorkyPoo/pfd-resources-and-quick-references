# Card t_7a22b040 — review round 1 fix: the CPAP Pearls bullet now matches the owner ruling

Branch `peep-final`, tip `e9a7e72` (content), gate log `audit/gates/peep-final-e9a7e72.log`.
Everything else on the branch (`CPAP.md` row 6 = `I`, ceiling `5–15 mmHg`, `owner_ruled` on
p.239#5's `I/P only` clause, `open_question` absent, Batch 7 units question gone) is unchanged
and was verified in the round-1 review.

## The blocking item, and the fix

Reviewer, round 1 (artifact lens), blocking item 1: `docs/procedures/CPAP.md:40` still read

> CPAP, BiPAP, and PEEP are "RED DOT" procedures at all EMS certification levels (refer to
> department-specific authorization/training policy).

— the p.245#4 sentence, three lines below a row that now says `I`.

Took the reviewer's option 1 (qualify, keep the source sentence recognisable):

> CPAP and BiPAP are "RED DOT" procedures at all EMS certification levels; PEEP titration
> above the initial 5 cmH2O setting is Intermediate and above (refer to
> department-specific authorization/training policy).

Rows 1–5, the contraindications and the other three Pearls bullets are untouched.

Two record-only edits came with it:

- `level-rulings.yaml`, CPAP r6 `note`: condensed to the verbatim ruling, the clause basis,
  the ceiling and its recorded discrepancy, plus **one** history line saying the earlier
  agent recommendation is withdrawn and superseded (reviewer non-blocking item 4).
- `row-bindings.yaml`, CPAP r6 `evidence`: one sentence recording that the Pearls bullet is
  qualified to the ruling, so the page's prose and its table agree on the record.

## Gates — 5/5 EXIT=0 on `e9a7e72`

`audit/gates/peep-final-e9a7e72.log`, written by `audit/gates/run_gates_peep_final_pearls.sh`,
which captures each subprocess's real exit code (never through a pipe):

| gate | exit |
|---|---|
| `python3 scripts/verify_pems_canonical.py` | 0 |
| `python3 scripts/level_rule.py --check` | 0 |
| `python3 scripts/mc_wording.py --check` | 0 |
| `python3 scripts/build_outstanding_decisions.py --check` | 0 |
| `/root/pfd-ssg-env/bin/mkdocs build --strict` | 0 |

## Three planted defects, re-proved on `e9a7e72`

`audit/gates/plant_defects_4eb2d85.py` edits the real worktree, runs `level_rule.py --check`,
records `subprocess.returncode`, and `git checkout --`s the file back. Worktree clean of edits
afterwards (only the untracked gate logs remain).

```
DEFECT 1. chip set back to EMT on row 6 -> docs/procedures/CPAP.md
cmd: python3 scripts/level_rule.py --check
EXIT=1
  - procedures/CPAP.md row 6: marker EMT != owner ruling I

DEFECT 2. ceiling reverted to 15 cmH2O (unit dropped) -> docs/procedures/CPAP.md
cmd: python3 scripts/level_rule.py --check
EXIT=1
  - wording ruling: docs/procedures/CPAP.md does not read "Consider titrating PEEP (5–15 mmHg)
    as needed to improve ventilation." (owner-ruled wording missing)

DEFECT 3. open_question reinstated beside the ruling -> audit/level-scan/row-bindings.yaml
cmd: python3 scripts/level_rule.py --check
EXIT=1
  - procedures/CPAP.md row 6: row-bindings.yaml still records an `open_question` that this
    owner ruling answers — drop the field, or the owner page keeps asking a decided question
```

## Rendered page, from the published preview (HTTP, cache-busted)

`/preview/peep-final/procedures/CPAP.html`:

- row 6: `<span class="lvl lvl-i">I</span>` + `Consider titrating PEEP (5–15 mmHg) as needed to improve ventilation.`
- Pearls: `RED DOT" procedures at all EMS certification levels; PEEP titration above the initial 5 cmH2O setting is Intermediate and above (refer to department-specific authorization/training policy).`

`/preview/peep-final/protocols/outstanding-decisions.html`: `Needs your level decision — 0 rows`,
`Open questions about the rules — 30`, `Already ruled — recorded decisions — 6` (unchanged from
the round-1 handoff; this round changed no ledger row).

Sibling slot `/preview/peep-split/procedures/CPAP.html` still carries the unqualified bullet,
which is what slot independence looks like.
