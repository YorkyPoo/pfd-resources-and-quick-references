# Gate evidence — branch `peep-split`, content commit `5ed4464`

Card: **t_a628eefa** — run the five validation gates for the PEEP titration fixes and log the
results. Parents: `t_4a38c264` (Respiratory Distress r6 split at `110dd3c`, tip `5ed4464`) and
`t_ca5ba752` (CPAP r6 owner brief — no procedure change, so no gate impact).

Worktree: `/root/.hermes/kanban/boards/lifeos-consolidation/workspaces/t_814299a9/wt`
(branch `peep-split`), tree clean at `5ed44647b9289fdb28e8059def96ef3b3d581d2e` before the run.

## Gates — 5/5 EXIT=0

Log: `audit/gates/peep-split-5ed4464.log` (raw gate output, exit codes taken from each
subprocess, never typed).

| gate | command | exit | what it asserted |
|---|---|---:|---|
| level_rule | `python3 scripts/level_rule.py --check` | 0 | 518 action rows across 54 pages: 504 carry exactly one marker equal to the cited PEMS 2024 badge, 2 OWNER_REQUIRED with a recorded reason, 9 owner_ruled; 21 bundled rows split into 47 sub-rows; 5 owner_ruled rows cite unbadged prose by verbatim span |
| verify_pems_canonical | `python3 scripts/verify_pems_canonical.py` | 0 | 8 verifier stages, including `c2.split_map` and `c2.row_splits` (the split the parent card landed) |
| mc_wording | `python3 scripts/mc_wording.py --check` | 0 | 27 MC rows on 26 pages name no OMD / Medical Director / named individual |
| build_outstanding_decisions | `python3 scripts/build_outstanding_decisions.py --check` | 0 | `protocols/outstanding-decisions.md` matches the ledger; "PEMS prints this nowhere" bucket = 0 rows |
| mkdocs_strict | `/root/pfd-ssg-env/bin/mkdocs build --strict` | 0 | built in 7.29 s, no strict warnings |

## Planted defect — the harness is live, not silently passing

One defect planted in the worktree, gate run through `subprocess.run` so the exit code is the
gate's own, then the file restored with its exact bytes and the gate re-run:

```
BEFORE: | 6a | <span class="lvl lvl-i">I</span> | • **Titration:** Titrate PEEP up to **10 cmH2O** ...

PLANTED rc= 1
    FAIL
     - protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a: marker EMT != owner ruling I
     - protocols/respiratory/03_Respiratory_Distress_PROC.md row 6a: chip EMT != the level row-splits.yaml records for this part (I)
restored identical: True
RESTORED rc= 0
```

The parent card already proved three further plants on this same tip
(`audit/gates/peep-split-110dd3c-distress-r6.md`): chip letter, dropped `clause_only`, and a
word changed inside the `clause_of` span — 3/3 caught, each restored to EXIT=0.

## Not done here

- No defect ticket: no gate failed, so there is no failure log to quote.
- No merge to `main` and no preview publish — `peep-split` still carries `5d34686`, the CPAP r6
  hunk whose "owner answer / ANSWERED" provenance the reviewer rejected; the branch must not be
  merged as-is. `t_ca5ba752` holds the open owner decision for that row.
- The wider `run_gates.sh` set (`agency_names`, `internal_artifacts`, `link_sweep`) is outside
  the five gates this card names.
