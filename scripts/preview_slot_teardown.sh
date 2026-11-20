#!/usr/bin/env bash
# Remove ONE preview slot without touching the others, then regenerate the
# /preview/ index. Only the preview/ subtree of gh-pages is written.
#
#   bash scripts/preview_slot_teardown.sh pilot
#   bash scripts/preview_slot_teardown.sh --all     # remove /preview/ entirely
#
# Refuses to remove anything unless the target is a real slot directory under
# preview/<name>/ (slots.json entry + directory). Safe to run twice.
set -euo pipefail

TOOLING="$(cd "$(dirname "$0")" && pwd)"
REPO="$(git -C "$TOOLING" rev-parse --show-toplevel)"
cd "$REPO"

if [ "$#" -ne 1 ]; then
  echo "usage: $0 <slot>|--all" >&2
  exit 2
fi
TARGET="$1"

if ! git ls-remote --exit-code origin gh-pages >/dev/null 2>&1; then
  echo "error: cannot reach origin gh-pages" >&2
  exit 1
fi

WT="$(mktemp -d "${TMPDIR:-/tmp}/pfd-preview-teardown.XXXXXX")"
cleanup() {
  cd "$REPO" || true
  git worktree remove --force "$WT/ghp" >/dev/null 2>&1 || true
  rm -rf "$WT"
}
trap cleanup EXIT

git config user.name  >/dev/null 2>&1 || git config user.name  "developer"
git config user.email >/dev/null 2>&1 || git config user.email "developer@localhost"

git worktree add -q --detach "$WT/ghp" origin/gh-pages
cd "$WT/ghp"
git checkout -q -B preview-teardown

if [ "$TARGET" = "--all" ]; then
  if [ ! -e preview ]; then
    echo "preview/ is absent — nothing to tear down."
    exit 0
  fi
  git rm -r -q preview
  git commit -q -m "preview: tear down all preview slots"
  git push -q origin HEAD:gh-pages
  echo "teardown pushed: $(git rev-parse HEAD)"
  exit 0
fi

case "$TARGET" in
  *[!a-z0-9_-]*|"") echo "error: invalid slot name '$TARGET'" >&2; exit 2 ;;
esac
if [ ! -d "preview/$TARGET" ]; then
  echo "slot preview/$TARGET does not exist — nothing to tear down."
  exit 0
fi

rm -rf "preview/$TARGET"

python3 - "$TARGET" <<'PY'
import json, pathlib, sys
slot = sys.argv[1]
p = pathlib.Path("preview/slots.json")
if p.exists():
    data = json.loads(p.read_text())
    data.get("slots", {}).pop(slot, None)
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
PY

python3 "$TOOLING/preview_index.py" "$WT/ghp"

git add -A preview
git commit -q -m "preview: tear down slot '$TARGET' (other slots untouched)"
git push -q origin HEAD:gh-pages
echo "teardown pushed: $(git rev-parse HEAD)"
