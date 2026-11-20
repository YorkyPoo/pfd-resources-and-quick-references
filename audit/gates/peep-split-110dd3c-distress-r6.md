# Respiratory Distress r6 split — verification evidence

Card: `t_4a38c264` (Split Respiratory Distress r6 into initiation and titration rows).
Branch `peep-split`. The split itself is content commit **`cd6b8a9`**; this card added the
`level-rulings.yaml` comment correction at **`110dd3c`**. Every command below was executed in
the worktree `/root/.hermes/kanban/boards/lifeos-consolidation/workspaces/t_814299a9/wt`;
the exit codes are the real subprocess return codes (captured with `subprocess.run(...)
.returncode` in a probe script, never through a pipe — a `cmd | head` returns head's code).

## The split, as it stands

| row | chip | status | basis |
|---|---|---|---|
| 6 (initiation) | `EMT` | cited | `p.239#5` cross-page + `quoted_row_text` "Consider CPAP (PEEP: 5 cmH2O) for respiratory distress." |
| 6a (titration) | `I` | `owner_ruled`, `clause_only: true` | `clause_of p.239#5` token "I/P only: Adjust PEEP to support ventilation and work of breathing" |

Source facts re-read out of `audit/level-scan/pems_table.json` (not out of the comment):

```
--- p.239#5  doc='Airway Management and Ventilatory Support'
   badge_tokens: ['EMT']  columns: {'EMR': '', 'EMT': '•', 'A': '•', 'I': '•', 'P': '•'}
   text: 'Consider CPAP (PEEP: 5 cmH2O) for respiratory distress. Refer to CPAP procedure.
          I/P only: Adjust PEEP to support ventilation and work of breathing, up to 10 cmH O.** 2'
--- p.123#3  doc='Respiratory Distress'
   badge_tokens: ['EMT']
   text: 'Consider non-invasive (CPAP) or invasive (SGA) ventilatory support.'

clause token verbatim in p.239#5 : True
quoted_row_text verbatim p.239#5 : True
```

Row 6 cites `p.239#5` rather than the automatic `p.123#3`: both carry badge EMT, but `p.123#3`
prints "consider CPAP support" and no PEEP setting, while row 6 publishes "Initial Settings:
PEEP 5 cmH2O" — `p.239#5` prints both halves of the split. This matches how Asthma r8/r8a was
split (both off `p.239#5`).

## Checks

```
python3 scripts/level_rule.py --check        EXIT=0
```
```
OK — 518 action rows across 54 pages: 504 carry exactly one marker equal to the level printed
by the cited PEMS 2024 row, 2 are flagged OWNER_REQUIRED with a recorded reason, 9 are
owner_ruled. ...
OK — 21 bundled row(s) are split into 47 sub-rows, each one action; every part cites the PEMS
2024 row that prints it and its chip is that row's badge (row-splits.yaml `site_splits`,
re-read against the pages); ...
```

```
python3 scripts/level_rule.py --write        EXIT=0   (624 ledger rows; rewrote 0 of 320 hashed files)
```
`--write` is a no-op on this tree: the page, `level-rule-ledger.json/md` and
`outstanding-decisions.md` already equal what the writer emits (md5 of all 320 `docs/` +
`audit/level-scan` files identical before/after).

```
/root/pfd-ssg-env/bin/mkdocs build --strict  EXIT=0   (Documentation built in 7.03 seconds)
```

Table syntax probe on `docs/protocols/respiratory/03_Respiratory_Distress_PROC.md`:

```
table at line 48-69: 22 lines (header + separator + 20 rows)
rows with pipe count != 4: none
row numbers: ['1','2','3','3a','4','5','6','6a','7','8','9','10','11','12','13','14','15','16','16a','16b']
duplicate row numbers: none
chips: [('1','emr'),('2','emr'),('3','emt'),('3a','i'),('4','emr'),('5','emr'),('6','emt'),('6a','i'),
        ('7','emt'),('8','i'),('9','a'),('10','a'),('11','a'),('12','a'),('13','a'),('14','i'),
        ('15','emt'),('16','emt'),('16a','i'),('16b','p')]
unclosed <div>: 1 vs </div>: 1
```

Rendered page (from that `--strict` build), tags stripped:

```
row 5 : level='EMR'
row 6 : level='EMT' css=emt   CPAP (Continuous Positive Airway Pressure): • Indications: Adults with
                              respiratory distress due to pulmonary edema, infection, or near-drowning
                              • Initial Settings: PEEP 5
row 6a: level='I'   css=i     • Titration: Titrate PEEP up to 10 cmH2O to support ventilation and work of
                              breathing.
row 7 : level='EMT'
```

## Planted defects — 3/3 caught, each restored to a clean EXIT=0

Anchor-preserving single-token edits, `--check` re-run, then `git checkout --` and re-run.

```
[1 chip letter I->A on row 6a] returncode 1
    - protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a: marker A != owner ruling I
    - protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a: chip A != the level
      row-splits.yaml records for this part (I)
    restored -> returncode 0

[2 clause_only dropped from the 6a ruling] returncode 1
    level-rulings.yaml: protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a declares a
    clause_of but not clause_only: true — a clause_of ruling may retire the OWNER_REQUIRED flag
    only when the si...
    restored -> returncode 0

[3 clause token word changed (Adjust->Adjusts)] returncode 1
    - protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a: the clause 'I/P only: Adjusts
      PEEP to support ventilation and work of breathing' is not a verbatim span of p.239#5
    - protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a: ledger clause_of {...token:
      'I/P only: Adjust PEEP...'} != level-rulings.yaml clause {...token: 'I/P only: Adjusts...'}
    restored -> returncode 0
```

Plant 1 is the one this card is about: the `I` chip is a recorded owner decision, and the
checker refuses any other letter on that row and cross-checks it against the split record.
Plant 3 changes a word *inside* the span — a truncated tail ("…work of breathin") would still
be a verbatim substring and would correctly pass, so it proves nothing.

## Correction made by this card

`audit/level-scan/level-rulings.yaml`, the block comment above the 2026-11-20 PEEP rulings,
still read "`clause_only: true` on both … see Respiratory Distress r6, which still bundles both
and is therefore NOT covered here" — contradicted by the `row: 6a` entry 60 lines below it.
Reworded to the measured state (three `clause_only` rulings; Distress r6 was the bundled row
the ruling could not reach until it was split). Comment text only: no level, page or generated
artifact changed.

## Not done here

- The standard gate log `audit/gates/<branch>-<sha>.log` — card **`t_a628eefa`** owns the full
  five-gate run and the log; this card ran `level_rule --check`/`--write` and
  `mkdocs build --strict` for syntax verification only.
- No push to `main`, no preview slot. `peep-split` is stacked on `peep-i`.
- `procedures/CPAP.md` row 6 (the other half of the parent card) is a separate, still-open
  owner decision — out of scope for this card.
