#!/usr/bin/env bash
# Build one or more branches into their own /preview/<slot>/ subpaths on
# gh-pages, then regenerate the /preview/ index. Only the preview/ subtree of
# gh-pages is written; the live root is never rebuilt or touched.
#
#   bash scripts/publish_preview_slots.sh pilot=pilot-references-block \
#                                       relabel=provider-level-letters
#
# Optional description override: slot=branch  (description defaults to the
# branch's tip commit subject, which is the provenance line reviewers see).
#
# Every slot is built from exactly ONE branch/commit (git rev-parse of the
# branch at publish time). Slots not named on the command line are left alone.
set -euo pipefail

TOOLING="$(cd "$(dirname "$0")" && pwd)"
REPO="$(git -C "$TOOLING" rev-parse --show-toplevel)"
export REPO
cd "$REPO"

if [ "$#" -eq 0 ]; then
  echo "usage: $0 slot=branch [slot=branch ...]" >&2
  exit 2
fi

if ! git ls-remote --exit-code origin gh-pages >/dev/null 2>&1; then
  echo "error: cannot reach origin gh-pages" >&2
  exit 1
fi

WT="$(mktemp -d "${TMPDIR:-/tmp}/pfd-preview-slots.XXXXXX")"
cleanup() {
  cd "$REPO" || true
  for d in "$WT"/*; do
    [ -d "$d" ] && git worktree remove --force "$d" >/dev/null 2>&1 || true
  done
  rm -rf "$WT"
}
trap cleanup EXIT

git config user.name  >/dev/null 2>&1 || git config user.name  "developer"
git config user.email >/dev/null 2>&1 || git config user.email "developer@localhost"

# ---- build every requested slot from its own branch tip -------------------
names=()
for pair in "$@"; do
  slot="${pair%%=*}"
  branch="${pair#*=}"
  if [ "$slot" = "$pair" ] || [ -z "$slot" ] || [ -z "$branch" ]; then
    echo "error: bad argument '$pair' (want slot=branch)" >&2
    exit 2
  fi
  sha="$(git rev-parse --verify "$branch^{commit}")"
  echo "== building slot '$slot' from $branch @ $(git rev-parse --short "$sha")"
  git worktree add -q --detach "$WT/src-$slot" "$sha"
  python3 "$TOOLING/build_preview_slot.py" --slot "$slot" --repo "$WT/src-$slot"
  names+=("$slot|$branch|$sha")
done

# ---- stage on gh-pages ----------------------------------------------------
git worktree add -q --detach "$WT/ghp" origin/gh-pages
cd "$WT/ghp"
git checkout -q -B preview-publish
mkdir -p preview

for entry in "${names[@]}"; do
  IFS='|' read -r slot branch sha <<<"$entry"
  if [ -e "preview/$slot" ]; then
    echo "== replacing existing slot preview/$slot"
    rm -rf "preview/$slot"
  fi
  cp -a "$WT/src-$slot/site_preview/$slot" "preview/$slot"
done

# record provenance in preview/slots.json then regenerate the index
python3 - "$@" <<'PY'
import json, os, pathlib, subprocess, sys
now = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True).stdout.strip()
path = pathlib.Path("preview/slots.json")
data = json.loads(path.read_text()) if path.exists() else {"slots": {}}
for pair in sys.argv[1:]:
    slot, branch = pair.split("=", 1)
    # sha of the branch tip as resolved in the main worktree
    rev = subprocess.run(["git", "rev-parse", branch], capture_output=True, text=True, cwd=os.environ["REPO"]).stdout.strip()
    subject = subprocess.run(["git", "log", "-1", "--format=%s", rev], capture_output=True, text=True, cwd=os.environ["REPO"]).stdout.strip()
    prev = data["slots"].get(slot, {})
    data["slots"][slot] = {
        "branch": branch,
        "sha": rev,
        "description": prev.get("description") or subject,
        "built_at": now,
    }
path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
print("slots.json updated:", ", ".join(sorted(data["slots"])))
PY

python3 "$TOOLING/preview_index.py" "$WT/ghp"

git add -A preview
if git diff --cached --quiet; then
  echo "no changes to publish"
  exit 0
fi
git commit -q -m "preview: publish slot(s) $(printf '%s ' "${names[@]}")from their branch tips" \
                 -m "preview/ only; live root untouched."
git push -q origin HEAD:gh-pages
echo "published: $(git rev-parse HEAD)"
