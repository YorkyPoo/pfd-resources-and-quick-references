# Card t_0a50256d — peep-i — planted-defect evidence

Branch `peep-i`, content commit `e4ae668` (base `main` `81f41f7`).

Guards under test: `scripts/level_rule.py --check` — after this card it also verifies the new
`clause_of:` ruling mechanism. A `clause_of` ruling must name a clause that is a VERBATIM span
of the printed row it cites, the ruled level must be the lowest level that clause names, that
row's own badge must differ (else the row is the citation), `clause_only: true` must be
declared, and no `row-bindings.yaml` entry may still declare the row `owner_required`.

## 1. Guard passes on the shipped tree

```
$ python3 scripts/level_rule.py --check
OK — ... 2 of them are flagged OWNER_REQUIRED ...
OK — 5 owner_ruled row(s) cite unbadged PEMS prose ...
EXIT=0
```

Full log: `audit/gates/peep-i-e4ae668.log` (5 gates, 0 failing).

## 2. Plant 1 — the ⚑ flag put back on the now-`clause_only` Pulmonary Edema row 9

```
$ python3 scripts/level_rule.py --check
FAIL
 - protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md row 9: owner-ruled row still carries the OWNER_REQUIRED marker
EXIT=1
```

## 3. Plant 2 — the ruling's clause token no longer a verbatim span of p.239#5

Colon replaced with a comma: `I/P only, Adjust PEEP ...`

```
$ python3 scripts/level_rule.py --check
FAIL
 - protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md row 9: the clause 'I/P only, Adjust PEEP to support ventilation and work of breathing' is not a verbatim span of p.239#5
 - protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md row 9: ledger clause_of {...} != level-rulings.yaml clause {...}
EXIT=1
```

## 4. Plant 3 — `clause_only: true` removed from a `clause_of` ruling

```
$ python3 scripts/level_rule.py --check
level-rulings.yaml: protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md row 9 declares a clause_of but not clause_only: true — a clause_of ruling may retire the OWNER_REQUIRED flag only when the site row covers the scoped clause alone
EXIT=1
```

## 5. Restored

```
$ git checkout -- docs/protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md audit/level-scan/level-rulings.yaml
$ python3 scripts/level_rule.py --check
EXIT=0
$ git status --short
(only the gate log this evidence accompanies)
```

## Why the guard matters (the bug it prevents)

An earlier 2026-11-20 attempt chipped Pulmonary Edema row 9 at `I` as an owner ruling although
the owner had never ruled on PEEP titration, and retired the flag on Asthma row 8 while that
row still bundled CPAP initiation (printed EMT) with titration (I/P). Plant 1 and Plant 3 are
the two halves of that failure: a retired flag on a row that is not a single authorisation, and
a ruling with no printed basis to check it against.
