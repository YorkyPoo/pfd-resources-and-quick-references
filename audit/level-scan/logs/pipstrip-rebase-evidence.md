# pip-strip — rebase onto main and re-verification (2026-11-20)

Card t_10349df8. Branch `pilot-pipstrip` rebased from `6339178` (cut from
`pilot-references-block`) onto `main` @ `d5fd03c`.

## Rebase

    git rebase origin/main   → 3 commits replayed, NO conflicts
    tip before: 6339178   tip after: a370a31 (the frozen tip — see below)

## Frozen tip, and the one publish that serves it

    frozen tip (code)      : a370a3169b60215f8cc887168804abee2f498f2f
                             branch pilot-pipstrip-rebased (pushed, non-force)
    published slot         : /preview/pipstrip/
    preview/slots.json     : pipstrip.sha = a370a3169b60215f8cc887168804abee2f498f2f
                             pipstrip.built_at = 2026-11-20T15:18:51Z
                             17 slots; siblings' built_at unchanged
    gh-pages commit        : e5239516eebc2d0d7bb03269145c57554b2c9d8b
                             ("preview: publish slot(s) pipstrip — one branch tip per slot")

No further slot publish and no further code commit happen after this evidence.
The evidence files below were generated *against that published build*, each
headed with the sha it describes. They are committed in an audit-only commit
made immediately after the publish, so the branch tip is one commit beyond the
slot sha while `git diff --name-only a370a31 <tip> -- docs/ scripts/ mkdocs.yml`
is empty — the site the slot serves is byte-identical to what the evidence
describes. That is the one ordering that avoids the stale-evidence trap: the
slot sha cannot appear in a header of the commit that created it.

Generation commands (this machine, 2026-11-20 15:22–15:23 UTC):

    curl -sS -H 'Cache-Control: no-cache' \
      "<slot>/protocols/…/03_Pulmonary_Edema_Congestion_PROC.html?cb=<usec>"   → HTTP 200
    python3 scripts/verify_pip_strip.py --base <live slot URL> --src docs      → EXIT=0
    bash run_gates_pipstrip_a370a31.sh                                         → ALL GATES EXIT=0 (9 of 9)
    python3 pipstrip_negative.py                                               → control EXIT=0, both defects EXIT=1

## Round-3 evidence index

| file | what it proves |
|---|---|
| `audit/level-scan/logs/pipstrip-rowcheck-a370a31.txt` | live fetch per page: URL, HTTP status, bytes, sha256 of the HTML read, `<tr data-states` count, every row's number/states/tag vs the markdown chip at a370a31, `N rows in markdown / N in HTML / N compared / 0 mismatches`, and the verifier's verbatim output with EXIT |
| `audit/level-scan/logs/pipstrip-negative-a370a31.txt` | planted-defect tests **run at tip a370a31** (verifier blob `27574de1fc5dd304b1d00339f263aa8c94caedab`), control EXIT=0, defect A EXIT=1, defect B EXIT=1 |
| `audit/gates/pilot-pipstrip-rebased-a370a31.log` | the nine gates **run at tip a370a31** with per-gate `EXIT=` lines and `ALL GATES EXIT=0 (9 of 9)` |

The older `audit/level-scan/logs/pipstrip-rowcheck.txt` (headed `slot sha
c543ecc`) was removed in the same commit: it described the superseded build and
could only be mistaken for current evidence.

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

See `audit/gates/pilot-pipstrip-rebased-a370a31.log` (this branch, run at the
frozen tip). Same nine gates
as every other card: verify_pems_canonical, level_rule, mc_wording,
agency_names, build_outstanding, internal_artifacts, mkdocs_strict,
link_sweep, internal_artifacts_site. Summary line: `ALL GATES EXIT=0 (9 of 9)`.
The earlier `pilot-pipstrip-rebase-255f5fa.log` is kept as history; it was run
at `255f5fa` and does not describe the frozen tip.

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

    live slot (slot sha a370a31, gh-pages e523951, fetched 2026-11-20 15:22:56 UTC) → EXIT=0
      Cold Exposure   : 7 rows in markdown / 7 in HTML / 7 compared / 0 mismatches
      Pulmonary Edema : 10 rows in markdown / 10 in HTML / 10 compared / 0 mismatches

Evidence transcript: `audit/level-scan/logs/pipstrip-rowcheck-a370a31.txt`
(full output, every row's states and chip, the sha256 of each HTML fetched).
The negatives are in `audit/level-scan/logs/pipstrip-negative-a370a31.txt`, run
at the same tip: control EXIT=0, row 9 rendered `no,go,go,go,go` vs chip
`no,no,no,go,go` → EXIT=1, row 13 dropped → EXIT=1 (including the
tally-vs-rows mismatch).

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

