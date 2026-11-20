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

---

# Review round 1 — the answers (2026-11-20, t_10349df8 run 256)

## Rebase, as SHAs

    $ git rev-parse --short d5fd03c c543ecc
    d5fd03c  c543ecc
    $ git merge-base --is-ancestor d5fd03c c543ecc; echo $?
    0
    $ git log --oneline d5fd03c..c543ecc
    c543ecc audit(level-scan): pip-strip rebased onto main d5fd03c — 9/9 gates EXIT=0, 10/10 mapper, re-measured 279px at 390px
    255f5fa audit(level-scan): pip-strip acceptance evidence (measurements, live fetch, gates)
    303b1f5 audit(level-scan): pip-strip gate log at b3ff795
    6bfc0ba protocol format: five-pip strip driven by a tapped level (pilot, 2 pages)

Four commits, not three: three are audit/evidence commits (`6bfc0ba` is the
feature commit; `303b1f5`, `255f5fa`, `c543ecc` are logs). No commit in the
range touches `docs/protocols/**` — both pilot pages are byte-identical to
`origin/main` (checked: `git show origin/main:<page>` == working file).

## `.gitignore` — kept, with a reason

    $ git diff origin/main c543ecc -- .gitignore
    +mkdocs.preview.*.yml

One line, added by the feature commit `6bfc0ba`. It is *not* pip-strip content:
the per-slot publisher (`scripts/build_preview_slot.py`, which this slot was
built with) writes a per-slot config named `mkdocs.preview.<slot>.yml` into its
throwaway build worktree. The plain `mkdocs.preview.yml` was already ignored;
without this glob each publish leaves per-slot configs as untracked noise.
Nothing is ignored that used to be tracked, and no runtime behaviour changes.

## Gate line 31 — what it actually compares

    $ sed -n '899,903p' scripts/verify_pems_canonical.py
    section("docs_clean")
    print("no protocol pages touched")
    st = subprocess.run(["git", "status", "--porcelain", "--", "docs/"], cwd=REPO,
                        capture_output=True, text=True).stdout.strip()
    check(st == "", "git status shows no modified files under docs/")

It is a **working-tree cleanliness** check inside the `verify_pems_canonical`
gate: `git status --porcelain -- docs/` must be empty, i.e. no uncommitted edit
to a protocol page. It says nothing about files *added by the branch* — which
is why it passes with `docs/javascripts/pip-strip.js` and
`docs/stylesheets/pip-strip.css` committed. The wording is loose (it says "no
modified files", not "no uncommitted changes"); the logic is correct for its
purpose and was not changed on this branch.

## Per-row correctness — now machine-checked

`scripts/verify_pip_strip.py` previously checked structure only (6 buttons,
header letters, tally count, a tag exists) and could not have caught a strip
that restated a level wrongly. It now reads the page's own markdown and
compares **every** row: row number and `data-states` against the level chip
mapped through the same `states_for()` the hook uses.

    live slot (sha c543ecc) → EXIT=0
      Cold Exposure   : 7 chip rows, 7 rendered rows, 7/7 identical
      Pulmonary Edema : 10 chip rows, 10 rendered rows, 10/10 identical

Evidence transcript: `audit/level-scan/logs/pipstrip-rowcheck.txt` (full output,
plus two planted defects that the check catches: row 9 rendered
`no,go,go,go,go` vs chip `no,no,no,go,go` → EXIT=1; row 13 dropped from the
page → EXIT=1, including the tally-vs-rows mismatch).

Row 9 on the live page: `data-states="no,no,no,go,go"`, tag "standing from I",
chip `<span class="lvl lvl-i">I</span>` — matches. The `no,no,no,call,go` line
in `test_pip_strip_mapper.py` is the prototype's sample row (row 9 of the
owner's reference HTML) and is never offered as live evidence.

## Finding — the source tables themselves skip numbers

Live row numbers, verbatim from the rendered `<td class="pip-n">`:

    Cold Exposure   : 1 2 3 4 5 7 8            (no row 6)
    Pulmonary Edema : 1 2 3 4 5 9 10 11 12 13  (no rows 6, 7, 8)

The gaps are in `main`'s markdown, not in the strip: both pages are identical
to `origin/main`, whose tables number 1–5 then 9–13 for Pulmonary Edema and
1–5 then 7–8 for Cold Exposure (left over from the PEEP/rows splits). The
strip reproduces the page's own numbering; it does not invent rows to fill a
gap, and "10 actions" is the count of real rows. A renumbering would be a
content change on `main`, i.e. a different card.

