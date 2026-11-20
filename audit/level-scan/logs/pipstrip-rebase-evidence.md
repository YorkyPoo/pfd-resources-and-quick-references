# pip-strip — rebase onto main and re-verification (2026-11-20)

Card t_10349df8. Branch `pilot-pipstrip` rebased from `6339178` (cut from
`pilot-references-block`) onto `main` @ `d5fd03c`.

## Rebase

    git rebase origin/main   → 3 commits replayed, NO conflicts
    tip before: 6339178   tip after: see HEAD of this commit

The hook edits no protocol page, so the markdown-level changes on `main`
(`Cold Exposure` prose rows 6/9, `Pulmonary Edema` row 9 level) replayed under
it unchanged. Nothing in the transform needed patching.

## Finding — the flagged row no longer exists on main

`pilot-pipstrip` carried a rule that an OWNER_REQUIRED row (`lvl-own` chip,
outline-only pips + ⚑) renders distinctly on Pulmonary Edema. Since the branch
was cut, `main` resolved that row: Pulmonary Edema row 9 is now a **verified
`lvl-i`** (`I`, CPAP titration — owner ruling, `t_432b2e79` chain). It is no
longer flagged, so the outline-only / flagged-tally path is **not exercised by
either pilot page today**: both pages report `unverified/OWNER_REQUIRED: 0`.
The code path is still present in `scripts/mkdocs_pip_strip.py` (`flagged` →
`pip no unv`, `data-unverified`, `level unverified ⚑` tally bucket) and was not
removed or altered here. Reported, not "fixed" — a level change is out of scope.

## Gates — 9/9 EXIT=0

See `audit/gates/pilot-pipstrip-rebase-<sha>.log` (this branch). Same nine gates
as every other card: verify_pems_canonical, level_rule, mc_wording,
agency_names, build_outstanding, internal_artifacts, mkdocs_strict,
link_sweep, internal_artifacts_site. Summary line: `ALL GATES EXIT=0 (9 of 9)`.

## Mapper test — unchanged, still 10/10

`python3 scripts/test_pip_strip_mapper.py` → all 10 prototype rows reproduced,
row 9 `no,no,no,call,go`, `EXIT=0`.

## Rendered check (local `site/`, 390 px viewport, device metrics 390×844 DPR 2)

    python3 scripts/verify_pip_strip.py --base site   → EXIT=0
    Cold Exposure      : 7 rows, picker R B A I P + Show all, Show all pressed
    Pulmonary Edema    : 10 rows, picker R B A I P + Show all, Show all pressed

Action column width, measured in the browser (`getBoundingClientRect`):

    Pulmonary Edema pip-table            : 279 px  (390 px viewport, colgroup #24 / action 279 / strip 86)
    How-to-Read matrix action column     : 180 px  (same 390 px viewport)
    document scrollWidth                 : 390 px  → no horizontal scroll

Greyscale: solid vs hatched vs empty outline remain distinguishable —
row 13 (`call,call,call,call,call`, tag "MC AT EVERY LEVEL") shows diagonal
hatching against the solid pips above it; the empty outline of an unauthorised
level is distinct from both.
