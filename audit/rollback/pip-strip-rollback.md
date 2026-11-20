# Rollback runbook — five-pip level strip rollout

Written 2026-11-20. Scope: undoing the pip-strip rollout that replaced the
per-row level chip table on every convertible protocol/procedure page with a
five-pip strip plus tapped-level picker.

Nothing in this rollout edits markdown. The strip is produced at build time by
`scripts/mkdocs_pip_strip.py` from the chip the page already carries, so a
rollback is either "stop the hook" or "revert the commit" — no clinical text has
to be restored by hand.

## Reference SHAs

| what | ref |
|---|---|
| last pre-rollout state (backup tag) | `tables-backup-2026-11-20` → `d5fd03c` |
| rollout branch tip (14 commits) | `b3ff73b` |
| merge of the rollout into `main` | `9d47a89` (merge of `b3ff73b`) |
| published `main` after the rollout | `cf3d308` (= `9d47a89` + 12/12 gate log) |
| squashed single-commit packaging | tip of branch `pipstrip-atomic` (one commit on `d5fd03c`) |
| verbatim pre-rollout table markup | `audit/archive/tables-2026-11-20/` (69 pages, 621 rows) |

## Option 1 — one-key off switch (fastest, no history rewrite)

`mkdocs.yml` already carries the switch:

```yaml
extra:
  pip_strip:
    enabled: true    # -> false
    pages: all
```

Flip it to `false`, commit, push to `main`. The deploy workflow
(`.github/workflows/deploy.yml`) rebuilds and publishes; every page comes back
as the per-row chip table.

```bash
git switch main && git pull --ff-only
sed -i 's/^    enabled: true$/    enabled: false/' mkdocs.yml
/root/pfd-ssg-env/bin/mkdocs build --strict     # local proof before pushing
git commit -am "pip-strip: disable the five-pip strip (rollback)"
git push origin main
```

Verified 2026-11-20 in an isolated worktree at `cf3d308` with `enabled: false`:
`mkdocs build --strict` EXIT=0; 69 `lv-wrap` pages, 644 level chips, 0 pip
rows — identical counts to a pre-rollout build of `d5fd03c`; 329 of 332 site
files byte-identical after dropping the two pip asset tags (see "Residue"
below).

## Option 2 — one revert commit (history-preserving, undoes the merge)

```bash
git switch main && git pull --ff-only
git revert --no-edit -m 1 9d47a89     # -m 1 = keep the pre-rollout parent
git diff --stat tables-backup-2026-11-20 HEAD -- docs scripts mkdocs.yml
/root/pfd-ssg-env/bin/mkdocs build --strict
git push origin main
```

Verified 2026-11-20 in an isolated worktree at `cf3d308`: the revert applied
cleanly, `git diff --stat d5fd03c HEAD` listed only two post-merge audit files
(`audit/gates/pipstrip-rollout-9d47a89.log`,
`audit/gates/run_gates_merge_pipstrip.sh`) and no product path; `mkdocs build
--strict` EXIT=0 with 329/332 site files byte-identical to the pre-rollout
baseline build; and the pre-rollout gate set passed 9/9 EXIT=0 on the reverted
tree (`verify_pems_canonical`, `level_rule`, `mc_wording`, `agency_names`,
`build_outstanding`, `internal_artifacts`, `mkdocs_strict`, `link_sweep`,
`internal_artifacts_site`).

Reverting the **squashed** packaging instead (`git revert <pipstrip-atomic tip>`)
restores the tree to `d5fd03c` exactly, because that commit is a pure addition
on top of it — verified by tree hash in a throwaway worktree.

## Option 3 — reset to the backup tag (last resort, rewrites `main`)

Only if nothing else has landed on `main` since the rollout, and only with the
owner's agreement — this discards commits and needs a force push.

```bash
git switch main
git reset --hard tables-backup-2026-11-20
git push --force-with-lease origin main
```

`tables-backup-2026-11-20` is an annotated tag (object `2e88065`) that peels to
`d5fd03c`, the last release with the per-row chip tables.

## Option 4 — per-page restore

`audit/archive/tables-2026-11-20/index.md` lists all 69 snapshotted pages with
their tables, rows and chips; each `.html` file under that directory holds the
page's rendered `lv-wrap` markup verbatim. Paste a file's markup back into the
page in place of the strip to restore that page alone.

## Residue a rollback leaves behind

* With the off switch (Option 1) the plugin is gone but `mkdocs.yml` still lists
  `stylesheets/pip-strip.css` and `javascripts/pip-strip.js` in `extra_css` /
  `extra_javascript`, so every page keeps those two `<link>`/`<script>` tags.
  They are inert without the strip markup. Remove those two lines too if you
  want a byte-clean rebuild.
* Options 2–3 remove the assets and the hook outright; nothing is left.
* Both options rewrite `main`, so the deploy workflow must run (`push` to
  `main`, or `workflow_dispatch`) before the published site changes. The live
  preview slot is published by its own step and is not touched by a rollback of
  `main` alone.

## How the fallback was tested (2026-11-20)

Isolated git worktrees off the real repo, each built with
`/root/pfd-ssg-env/bin/mkdocs build --strict`, compared file-by-file by sha256
against a baseline build of `d5fd03c`:

| path | worktree | build | result |
|---|---|---|---|
| pre-rollout baseline | `d5fd03c` | EXIT=0 | 280 pages, 69 `lv-wrap`, 644 chips, 0 pip rows |
| Option 1 (off switch) | `cf3d308` + `enabled: false` | EXIT=0 | 329/332 identical to baseline after dropping pip asset tags |
| Option 2 (revert merge) | `cf3d308` + revert of `9d47a89` | EXIT=0 | 329/332 identical to baseline; gate suite passed |
| Option 2 (squashed) | revert of `pipstrip-atomic` tip | — | tree equals `d5fd03c` |

The three files that still differ are derived from git history, not content:
`station-info.html` (recent-changes list and build timestamp),
`search/search_index.json` and `search/search_index.js` (which embed that page's
text). Every clinical page is byte-identical to its pre-rollout output.

## Caveats

* `audit/gates/run_gates.sh` (the pre-rollout gate runner) has a pre-existing
  bug: it does `cd "$(dirname "$0")/.."`, which lands in `audit/` rather than
  the repo root, so every gate fails with `can't open file '.../audit/scripts/...'`.
  Run the gate commands from the repo root instead (they are listed in the
  Option 2 section) or fix that `cd` first. This defect exists on `d5fd03c` and
  is unrelated to the rollout.
* `python3 scripts/verify_pems_canonical.py` (part of the gate suite) needs the
  git-ignored `audit/level-scan/.cache/pems_rows.jsonl`; copy it into a fresh
  worktree first or that gate fails for reasons unrelated to the rollback.
* `scripts/verify_pip_strip.py` and `scripts/negative_test_pip_strip.py` are
  rollout-specific: after a rollback they are expected to fail or be absent,
  which is the point. Do not treat that as a rollback failure.
