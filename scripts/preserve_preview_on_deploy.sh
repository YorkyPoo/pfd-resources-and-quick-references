#!/usr/bin/env bash
# Preserve the /preview/ slot subtree across a whole-branch `gh-pages` deploy.
#
#   scripts/preserve_preview_on_deploy.sh <pre-deploy-gh-pages-sha> [remote]
#
# `mkdocs gh-deploy --force` replaces the ENTIRE gh-pages branch with the
# `main` build. `main` has no preview/ subtree, so without this step every
# deploy silently deletes /preview/<slot>/ (this actually happened: run
# 44682670389 wiped 1152 preview files).
#
# This restores the preview/ subtree from the pre-deploy tip onto the freshly
# deployed branch as one extra commit, byte-for-byte (same tree hash), and
# asserts that nothing outside preview/ was touched. It never rebuilds a slot,
# so preview/slots.json keeps naming exactly the branch/SHA each slot was
# published from — a deploy cannot silently republish a newer tip under an old
# slot name. Refreshing a slot stays an explicit `publish_preview_slots.sh`
# run.
#
# Exit codes: 0 = preview/ present and byte-identical (or nothing to preserve),
# 1 = could not restore.
set -euo pipefail

PREV="${1:?usage: $0 <pre-deploy-gh-pages-sha> [remote]}"
REMOTE="${2:-origin}"
BRANCH="${PREVIEW_DEPLOY_BRANCH:-gh-pages}"

TOOLING="$(cd "$(dirname "$0")" && pwd)"
REPO="${GITHUB_WORKSPACE:-$(git -C "$TOOLING" rev-parse --show-toplevel)}"
TMPROOT="${RUNNER_TEMP:-${TMPDIR:-/tmp}}"
ATTEMPTS="${PREVIEW_PRESERVE_ATTEMPTS:-3}"

git -C "$REPO" rev-parse --verify --quiet "${PREV}^{commit}" >/dev/null \
  || { echo "preserve: error: '$PREV' is not a commit in $REPO" >&2; exit 1; }

if ! git -C "$REPO" cat-file -e "${PREV}:preview" 2>/dev/null; then
  echo "preserve: ${PREV} carries no preview/ subtree — nothing to preserve"
  exit 0
fi

PREV_TREE="$(git -C "$REPO" rev-parse "${PREV}:preview")"
echo "preserve: pre-deploy preview/ tree = $PREV_TREE"

BASE="$(mktemp -d "$TMPROOT/pfd-preserve.XXXXXX")"
WT="$BASE/ghp"
cleanup() {
  git -C "$REPO" worktree remove --force "$WT" >/dev/null 2>&1 || true
  git -C "$REPO" worktree prune >/dev/null 2>&1 || true
  rm -rf "$BASE"
}
trap cleanup EXIT

set_identity() {
  git -C "$WT" config user.name  >/dev/null 2>&1 || git -C "$WT" config user.name  "deploy-bot"
  git -C "$WT" config user.email >/dev/null 2>&1 || git -C "$WT" config user.email "deploy-bot@localhost"
}

attempt=1
while [ "$attempt" -le "$ATTEMPTS" ]; do
  git -C "$REPO" fetch --no-tags "$REMOTE" "+refs/heads/$BRANCH:refs/remotes/$REMOTE/$BRANCH"
  NEW="$(git -C "$REPO" rev-parse "refs/remotes/$REMOTE/$BRANCH")"

  if [ "$(git -C "$REPO" rev-parse "${NEW}:preview" 2>/dev/null || echo none)" = "$PREV_TREE" ]; then
    echo "preserve: preview/ already intact at $NEW — nothing to do"
    exit 0
  fi

  echo "preserve: restoring preview/ onto $NEW (attempt $attempt/$ATTEMPTS)"
  git -C "$REPO" worktree remove --force "$WT" >/dev/null 2>&1 || true
  rm -rf "$WT"
  git -C "$REPO" worktree add -q --detach "$WT" "$NEW"
  set_identity

  git -C "$WT" rm -rq --cached --ignore-unmatch preview >/dev/null 2>&1 || true
  rm -rf "$WT/preview"
  git -C "$WT" checkout --quiet "$PREV" -- preview

  # Never touch anything but preview/.
  if ! git -C "$WT" diff --quiet "$NEW" -- . ':(exclude)preview'; then
    echo "preserve: error: restore would modify paths outside preview/:" >&2
    git -C "$WT" diff --name-status "$NEW" -- . ':(exclude)preview' >&2
    exit 1
  fi

  git -C "$WT" add -A preview
  if git -C "$WT" diff --cached --quiet; then
    echo "preserve: no staged change (preview/ already matches) — nothing to do"
    exit 0
  fi
  git -C "$WT" commit --quiet \
    -m "preview: preserve /preview/ slots across the main deploy" \
    -m "mkdocs gh-deploy --force replaced gh-pages with the main build; this restores the preview/ subtree from ${PREV} byte-for-byte. Live root untouched."

  if git -C "$WT" push --quiet "$REMOTE" "HEAD:refs/heads/$BRANCH"; then
    GOT="$(git -C "$WT" rev-parse "HEAD:preview")"
    if [ "$GOT" != "$PREV_TREE" ]; then
      echo "preserve: error: published preview/ tree $GOT != $PREV_TREE" >&2
      exit 1
    fi
    echo "preserve: OK — preview/ restored byte-identically at $(git -C "$WT" rev-parse --short HEAD)"
    exit 0
  fi

  echo "preserve: push rejected on attempt $attempt (concurrent gh-pages update?) — retrying"
  attempt=$((attempt + 1))
  sleep 3
done

echo "preserve: error: could not restore preview/ after $ATTEMPTS attempts" >&2
exit 1
