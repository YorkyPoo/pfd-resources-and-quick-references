# Gate + planted-defect evidence — branch `peep-split`, content commit `cd6b8a9`

Card: t_814299a9 — CPAP procedure r6 and Respiratory Distress r6 still publish PEEP
titration at EMT. Base: `peep-i` (d239848), which itself sits on `main` 81f41f7.

## Gates

Log: `audit/gates/peep-split-cd6b8a9.log`, written by `write_gate_log.py` (exit codes
captured from the subprocess, never typed).

| gate | command | exit |
|---|---|---:|
| level_rule | `python3 scripts/level_rule.py --check` | 0 |
| verify_pems_canonical | `python3 scripts/verify_pems_canonical.py` | 0 |
| mc_wording | `python3 scripts/mc_wording.py --check` | 0 |
| build_outstanding_decisions | `python3 scripts/build_outstanding_decisions.py --check` | 0 |
| mkdocs_strict | `/root/pfd-ssg-env/bin/mkdocs build --strict` | 0 |

## Planted defects — 5/5 caught, each restored to EXIT=0

Each plant edits the worktree, runs `python3 scripts/level_rule.py --check` through
`subprocess.run` (so the exit code is the gate's own, not a pipe's), prints the matching
FAIL line, restores the file with `git checkout --`, and re-runs the gate.

### 1. row 6a's chip letter changed I -> EMT

```
[1 chip letter on row 6a] EXIT=1 (expected 1)
    - protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a: marker EMT != owner ruling I
    - protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a: chip EMT != the level row-splits.yaml records for this part (I)
[1 chip letter on row 6a] restored: EXIT=0 (expected 0)
```

### 2. the clause_of token stops being a verbatim span of p.239#5

The token is planted in `level-rulings.yaml`, `level-rule-ledger.json` AND
`level-rule-ledger.md` so the three stay consistent and only the verbatim check can catch
it. (A truncated-tail token is NOT a valid plant: `"...and work of breathin"` is still a
substring of the printed row and the gate correctly passes it. The plant adds a letter
inside a word: `Adjusts`.)

```
[2 clause token not verbatim] EXIT=1 (expected 1)
    - protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md row 8a: the clause 'I/P only: Adjusts PEEP to support ventilation and work of breathing' is not a verbatim span of p.239#5
    - protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md row 9: the clause 'I/P only: Adjusts PEEP to support ventilation and work of breathing' is not a verbatim span of p.239#5
[2 clause token not verbatim] restored: EXIT=0 (expected 0)
```

(The same three entries carry the token, so the first two FAIL lines name the two older
rows; row 6a's line is present below them in the full output.)

### 3. `clause_only: true` removed from the row 6a ruling

```
[3 clause_only removed from row 6a] EXIT=1 (expected 1)
    level-rulings.yaml: protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a declares a clause_of but not clause_only: true — a clause_of ruling may retire the OWNER_REQUIRED flag only when the site row covers the scoped clause alone
[3 clause_only removed from row 6a] restored: EXIT=0 (expected 0)
```

### 4. the whole row-6 `site_splits` record deleted — 6a is a split nobody can audit

```
[4 split record missing for row 6/6a] EXIT=1 (expected 1)
    - protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a: a lettered sub-row with no entry in row-splits.yaml `site_splits` — a split may not exist only on the page
[4 split record missing for row 6/6a] restored: EXIT=0 (expected 0)
```

### 5. an owner ruling answers the CPAP row 6 question while `open_question` survives

```
[5 open_question after a ruling answers it] EXIT=1 (expected 1)
    - procedures/CPAP.md row 6: row-bindings.yaml still records an `open_question` that this owner ruling answers — drop the field, or the owner page keeps asking a decided question
[5 open_question after a ruling answers it] restored: EXIT=0 (expected 0)
```

## Rendered output

`site/protocols/respiratory/03_Respiratory_Distress_PROC.html`:

```
ROW: 6 EMT CPAP (Continuous Positive Airway Pressure): • Indications: ... • Initial ...
     chips: ['EMT']
ROW: 6a I • Titration: Titrate PEEP up to 10 cmH2O to support ventilation and work of breathing.
     chips: ['I']
```

`site/protocols/outstanding-decisions.html`: "Open questions about the rules — 32" (was
31), "Already ruled — recorded decisions — 5" (was 4), and the CPAP row 6 card reads
"*CPAP.md* row 6 — an open level question, recorded not fixed."
