#!/usr/bin/env bash
# One-command teardown of the /preview/ duplicate.
#
#   bash audit/level-scan/preview-teardown.sh
#
# Removes only gh-pages/preview/, commits, and pushes. The live root of
# gh-pages is not rebuilt or touched. Safe to run twice: if preview/ is
# already gone it exits without pushing.
set -euo pipefail

REPO="$(git rev-parse --show-toplevel)"
cd "$REPO"

if ! git ls-remote --exit-code origin gh-pages >/dev/null 2>&1; then
  echo "error: cannot reach origin gh-pages" >&2
  exit 1
fi

WT="$(mktemp -d "${TMPDIR:-/tmp}/pfd-preview-teardown.XXXXXX")"
cleanup() {
  cd "$REPO" || true
  git worktree remove --force "$WT" >/dev/null 2>&1 || true
  git branch -D preview-teardown >/dev/null 2>&1 || true
}
trap cleanup EXIT

git worktree add -q --detach "$WT" origin/gh-pages
cd "$WT"
git checkout -q -B preview-teardown

git config user.name  >/dev/null 2>&1 || git config user.name  "developer"
git config user.email >/dev/null 2>&1 || git config user.email "developer@localhost"

if ! git ls-files --error-unmatch preview >/dev/null 2>&1; then
  echo "preview/ is not present on gh-pages — nothing to tear down."
  exit 0
fi

git rm -r -q preview
git commit -q -m "preview: tear down /preview/ duplicate (expiry 2026-11-26)"
git push origin preview-teardown:gh-pages
echo "teardown pushed: $(git rev-parse HEAD)"
