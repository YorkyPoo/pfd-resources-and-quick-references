# Card t_7a22b040 — evidence: CPAP procedure row 6 → I, ceiling 15 mmHg

Branch `peep-final`, based on `peep-split` @ `5ed4464` (the Distress r6/r6a split), with
content commit `277c945` and the gate log commit after it.

## The owner's words

> "Only intermediates and above can titrate peep up to 15 mmhg"

Sent 2026-11-20 with the owner's photograph of PEMS "Airway Management and Ventilatory
Support" (Procedures, page 1 of 2, Version 2022v0722). The photographed CPAP row prints, in
the owner's copy:

> Consider CPAP (PEEP: 5 cmH₂O) for respiratory distress. Refer to *CPAP* procedure.
> **I/P only: Adjust PEEP** to support ventilation and work of breathing, **up to 10 cmH₂O.**

Evidence file: `audit/level-scan/evidence/owner-pages-2026-11-20/airway-management-cpap-2022v0722.jpg`,
sha256 `f4a6c716aa7704f920e634f4767144ccd3f5b05e907ea13a39694b0b57cd02e8` (the same value as
the prunable chat-profile cache directory the image came from). Provenance table in the
`README.md` beside it.

## What changed

| item | before | after |
|---|---|---|
| `docs/procedures/CPAP.md` row 6 chip | `EMT` | **`I`** |
| row 6 action text | `Consider titrating PEEP (5–15 cmH₂O) …` | `Consider titrating PEEP (5–15 mmHg) …` |
| ledger status for the row | `OK`, cited p.245#4 (badge EMT) | `owner_ruled`, `clause_only` on p.239#5 |
| `row-bindings.yaml` CPAP r6 `evidence` | "ANSWERED 2026-11-20, no change …" (agent prose) | the owner's ruling quoted, p.245#4 recorded as the printed row, `open_question` absent |
| `level-rulings.yaml` | — | new `owner_ruled` entry, verbatim ruling, withdrawn-recommendation history |
| `wording-rulings.yaml` | — | the ceiling as ruled: page reads `5–15 mmHg` |

The 5d34686 hunk ("keep EMT, drop the answered open question") is **superseded**, not layered
on: its provenance was an agent's relayed reading, and review rejected it on that ground.

## The ceiling discrepancy is recorded, not resolved

The photographed page caps PEEP adjustment at **10 cmH₂O**; the owner ruled **15 mmHg**. The
page reads 15 mmHg because the owner's number governs the ceiling, and the printed 10 cmH₂O
stays quoted in `level-rulings.yaml` (row 6 `note`), `row-bindings.yaml` (row 6 `evidence`) and
`wording-rulings.yaml` (`source_prints`). It is not converted to cmH₂O anywhere on the page.

## Owner page — measured before and after

Rendered `docs/protocols/outstanding-decisions.md` (generated, never hand-edited):

| section | before (`5ed4464`) | after |
|---|---|---|
| 1. Needs your level decision | 2 rows | **2 rows** |
| 3. Open questions about the rules | 31 | **30** (Batch 7 4 → 3) |
| 4. Already ruled — recorded decisions | 5 | **6** |

Section 1 is unchanged because CPAP r6 was **never in that bucket**: it was a *cited* row
carrying an `open_question`, and a binding's `open_question` publishes under section 3
("Open questions about the rules"), not section 1. That question left section 3 in the
superseded `5d34686` hunk; what this card removes from section 3 is the Batch 7 units
question, whose subject the ruling answers. The card's expectation that section 1 would fall
by one does not match the page's structure — the measured numbers are above.

`CPAP r6` now appears on the owner page only in section 4:

> `procedures/CPAP.md` row 6 — **I** — decided 2026-11-20: "Only intermediates and above can
> titrate peep up to 15 mmhg" Consider titrating PEEP (5–15 mmHg) as needed to improve
> ventilation.

## Gates — 5/5 EXIT=0 on `277c945`

`audit/gates/peep-final-277c945.log`, written by a runner that captures each subprocess's real
exit code (never through a pipe):

| gate | exit |
|---|---|
| `python3 scripts/level_rule.py --check` | 0 |
| `python3 scripts/verify_pems_canonical.py` | 0 |
| `python3 scripts/mc_wording.py --check` | 0 |
| `python3 scripts/build_outstanding_decisions.py --check` | 0 |
| `/root/pfd-ssg-env/bin/mkdocs build --strict` | 0 |

## `main` moved underneath this branch — merged, regenerated, re-gated

`t_c2820e77` merged `peep-i`, `rhythm-derive` and `refs-sweep` into `main` while this card ran.
`peep-final` was therefore merged with `origin/main` `9995acd` → merge commit `07abfd1`;
`git merge-base --is-ancestor origin/main HEAD` exits 0 at the tip below.

Conflicts were resolved the only way the repo allows:

- `audit/level-scan/level-rule-ledger.md` and `docs/protocols/outstanding-decisions.md` —
  generated files: taken from one side, then **regenerated** (`level_rule.py --write`,
  `build_outstanding_decisions.py`), never hand-merged.
- `scripts/level_rule.py` — a real code conflict in the owner-ruled branch of `check()`: main
  added the derived-level (`lvl-deriv`) checks, this branch added the `open_question` guard.
  Both are kept; the `open_question` guard is scoped `not is_derived` (a derived row has no
  ruling to answer).

The merged tree re-runs all five gates at `07abfd1` (`audit/gates/peep-final-07abfd1.log`,
5/5 EXIT=0) and the three planted defects are re-proved there, because the 5/5 log at
`277c945` does not carry forward.

Absolute owner-page numbers on the merged tree (main's `refs-sweep` closed rows of its own, so
these differ from the pre-merge table above):

| section | `277c945` | merged `07abfd1` |
|---|---|---|
| 1. Needs your level decision | 2 rows | **0 rows** |
| 2. Pending authorization | 18 | 15 |
| 3. Open questions about the rules | 30 | 30 |
| 4. Already ruled — recorded decisions | 6 | **6** |

CPAP row 6 is in section 4 on the merged tree as well.

## Three planted defects — each one caught

Each plant was applied to the real worktree, `level_rule.py --check` run, and the file restored
(`git status` clean afterwards). Exit codes are `subprocess.run(...).returncode`.

```
DEFECT 1. chip set back to EMT on row 6 -> docs/procedures/CPAP.md
cmd: python3 scripts/level_rule.py --check
EXIT=1
  FAIL
  - procedures/CPAP.md row 6: marker EMT != owner ruling I

DEFECT 2. ceiling reverted to 15 cmH2O (unit dropped) -> docs/procedures/CPAP.md
cmd: python3 scripts/level_rule.py --check
EXIT=1
  FAIL
  - wording ruling: docs/procedures/CPAP.md does not read "Consider titrating PEEP (5–15 mmHg)
    as needed to improve ventilation." (owner-ruled wording missing)

DEFECT 3. open_question reinstated beside the ruling -> audit/level-scan/row-bindings.yaml
cmd: python3 scripts/level_rule.py --check
EXIT=1
  FAIL
  - procedures/CPAP.md row 6: row-bindings.yaml still records an `open_question` that this
    owner ruling answers — drop the field, or the owner page keeps asking a decided question
```

Defect 2 is the guard the card asked for and the repo did not have before: the ruling's unit is
part of the ruling, and a cmH₂O revert is now a hard `--check` failure via the recorded
`page_reads` string.

All three were **re-planted on the merged tree at `07abfd1`** after the merge, with identical
output and `EXIT=1` each; the worktree was clean afterwards apart from the new gate log.
