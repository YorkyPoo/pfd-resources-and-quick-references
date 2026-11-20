# Evidence — merge of front-matter-2 into main (card t_51e5ae18)

Merge commit: `8c04f54` (main, before the gate-log commit)
Branch tip merged: `2f9d814` (`front-matter-2` after the sync merge, see below)
Content commit reviewed on the branch: `8ab0d3d` (tree unchanged by the sync)
Gate log: `audit/gates/integrate-fm2-8c04f54.log` — 9 of 9 gates EXIT=0, exit codes
captured from the subprocess by `audit/gates/run_gates_merge_fm2.sh`.

## Precondition deviation: the ancestry gate failed at the pinned branch tip

The card said merging `front-matter-2 @ 8ab0d3d` (base `e389a49`, "already contains
the deployed main") and that `git merge-base --is-ancestor origin/main front-matter-2`
must exit 0. Measured on the branch as delivered:

    $ git merge-base --is-ancestor origin/main front-matter-2 ; echo EXIT=$?
    EXIT=1

`front-matter-2` was cut from `e389a49`, which sits on the `front-matter-effective`
line (`5be39b6` → `8132ac3`) and therefore predates both round-2 merges into main:
`03b777a` (rows-rebased) and `88da439` (front-matter-effective), plus the gate-log
commits `64697ed` / `2a36d28` that follow them. So the branch did not contain
`origin/main` = `2a36d28`.

Rather than merge a branch that failed its own gate, `origin/main` was merged **into**
`front-matter-2` first (commit `2f9d814`, no conflicts), then the gate was re-measured:

    $ git merge-base --is-ancestor origin/main front-matter-2 ; echo EXIT=$?
    EXIT=0

The sync changed no byte of the branch's own change. `front-matter-2` vs `origin/main`
immediately before the merge into main was exactly the intended five files:

    audit/gates/front-matter-2-8ab0d3d-evidence.md   |  59 ++++
    audit/gates/front-matter-2-8ab0d3d.log           | 165 ++++++++++
    audit/gates/run_gates_front_matter_2.sh          |  39 +++
    docs/protocols/front-matter/00 - Introduction.md |   4 +-
    scripts/internal_artifacts.py                    | 121 +++++++++---
    5 files changed, 363 insertions(+), 25 deletions(-)

and the merge commit `8c04f54` has the same five-file diff against `origin/main` — no
file outside the branch's own change moved, so nothing live was reverted.

## The merged Introduction diff (both edits, nothing else)

    -**Pending approval by:** Poquoson Fire and Rescue Operational Medical Director (OMD)
    -
    -These protocols have been adopted, adapted, and approved by the Poquoson Fire and
    -Rescue Operational Medical Director to serve the specific operational and clinical
    -needs of our agency and the citizens of Poquoson.
    +These protocols have been adapted from the PEMS Council guidelines to serve the
    +specific operational and clinical needs of this agency and the citizens of Poquoson.

## The approval-claim guard fires on the merged tree (planted-defect proof)

`scripts/internal_artifacts.py` on the merged tree, run from the merge worktree:

| state of `00 - Introduction.md` | command | EXIT |
|---|---|---|
| merged content | `internal_artifacts.py --check` | 0 |
| `**Pending approval by:** … OMD` re-inserted at line 5 | same | **1** — `00 - Introduction.md:5 [omd-approval-claim]` |
| old "adopted, adapted, and approved by … OMD" sentence restored at line 21 | same | **1** — `00 - Introduction.md:21 [omd-approval-claim]` |
| file restored byte-for-byte (`cmp` true) | same | 0 |

## Environment note

`audit/level-scan/.cache/pems_rows.jsonl` is gitignored and only exists in the primary
checkout; `verify_pems_canonical` requires it as a deliverable. It was copied into the
merge worktree (untracked, not committed) before the gate run — the first attempt in a
bare worktree failed on exactly that missing file (`FAIL .cache/pems_rows.jsonl exists`,
EXIT=1), which is the only non-zero result seen on this merge.
