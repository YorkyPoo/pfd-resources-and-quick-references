# Planted-defect evidence — branch `peep-split`, content commit `5d34686`

Round 2 of card t_814299a9. Content commit `5d34686` is the owner's answer on the
CPAP procedure r6 question: row 6 stays `EMT` cited to p.245#4, the `open_question`
field is dropped, the ceiling is untouched at 5–15 cmH2O, and the resolution is
recorded in the binding's `evidence`. The Respiratory Distress r6/r6a split from
`cd6b8a9` is unchanged.

Harness: `/root/.hermes/profiles/developer/cache/scratch/plant_cpap_r6.py` — each
plant edits a tracked file, runs `python3 scripts/level_rule.py --check` through
`subprocess.run(...).returncode` (never a pipe, so the exit code is the checker's
own), prints the matching failure line, restores with `git checkout --` and re-runs
to prove EXIT=0.

```
$ python3 /root/.hermes/profiles/developer/cache/scratch/plant_cpap_r6.py
[1 CPAP r6 chip letter EMT->I] EXIT=1 (expected 1)
    - procedures/CPAP.md row 6: marker I != expected EMT (p.245#4)
    - procedures/CPAP.md row 6: PEMS column dots start at EMT, badge says I
[1 CPAP r6 chip letter EMT->I] restored: EXIT=0 (expected 0)
[2 Distress r6a chip letter I->A] EXIT=1 (expected 1)
    - protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a: marker A != owner ruling I
    - protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a: chip A != the level row-splits.yaml records for this part (I)
[2 Distress r6a chip letter I->A] restored: EXIT=0 (expected 0)
[3 open_question surviving an owner ruling] EXIT=1 (expected 1)
    - procedures/CPAP.md row 6: row-bindings.yaml still records an `open_question` that this owner ruling answers — drop the field, or the owner page keeps asking a decided question
[3 open_question surviving an owner ruling] restored: EXIT=0 (expected 0)
```

What each plant proves:

1. **The CPAP row's kept level is enforced, not narrated.** Changing the chip letter
   to `I` — the change the card originally proposed — fails on the printed citation,
   so the row cannot drift to `I` while p.245#4 prints EMT. This is the guard behind
   the answer, and it is why the answer is "keep EMT" and not a preference.
2. **The Distress split is still live.** Dropping the `I` half of the split to `A`
   trips both the ruling check and the `row-splits.yaml` part check, so `r6a` stays
   chipped `I` from this card's content commit.
3. **A decided question cannot stay on the owner's page.** Re-adding `open_question`
   to the binding *and* an owner ruling for that row makes `--check` fail with the
   stale-question message — the mechanism that closes this question, proven to fire.

Gate log for `5d34686`: `audit/gates/peep-split-5d34686.log` (5/5 EXIT=0).
