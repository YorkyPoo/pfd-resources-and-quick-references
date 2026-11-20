#!/usr/bin/env bash
# Build one or more branches into their own /preview/<slot>/ subpaths on
# gh-pages, then regenerate the /preview/ index. Only the preview/ subtree of
# gh-pages is written; the live root is never rebuilt or touched.
#
#   bash scripts/publish_preview_slots.sh \
#        pilot=pilot-references-block="Pilot: prose out of action tables" \
#        relabel=provider-level-letters="R|B|A|I|P relabel"
#
# Each argument is slot=branch or slot=branch=description. When the description
# is omitted the branch tip's commit subject is used.
#
# Every slot is built from exactly ONE branch/commit (git rev-parse of that
# branch at publish time, in a throwaway worktree). Slots not named on the
# command line are left alone.
set -euo pipefail

TOOLING="$(cd "$(dirname "$0")" && pwd)"
REPO="$(git -C "$TOOLING" rev-parse --show-toplevel)"
export REPO
cd "$REPO"

if [ "$#" -eq 0 ]; then
  echo "usage: $0 slot=branch[=description] [slot=branch[=description] ...]" >&2
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
MANIFEST="$WT/manifest.tsv"
: >"$MANIFEST"
for pair in "$@"; do
  slot="${pair%%=*}"
  rest="${pair#*=}"
  branch="${rest%%=*}"
  desc=""
  if [ "$rest" != "$branch" ]; then
    desc="${rest#*=}"
  fi
  if [ "$slot" = "$pair" ] || [ -z "$slot" ] || [ -z "$branch" ]; then
    echo "error: bad argument '$pair' (want slot=branch[=description])" >&2
    exit 2
  fi
  case "$slot" in
    *[!a-z0-9_-]*) echo "error: invalid slot name '$slot'" >&2; exit 2 ;;
  esac
  sha="$(git rev-parse --verify "$branch^{commit}")"
  if [ -z "$desc" ]; then
    desc="$(git log -1 --format=%s "$sha")"
  fi
  echo "== building slot '$slot' from $branch @ $(git rev-parse --short "$sha")"
  git worktree add -q --detach "$WT/src-$slot" "$sha"
  python3 "$TOOLING/build_preview_slot.py" --slot "$slot" --repo "$WT/src-$slot"
  printf '%s\t%s\t%s\t%s\n' "$slot" "$branch" "$sha" "$desc" >>"$MANIFEST"
done

# ---- stage on gh-pages ----------------------------------------------------
git worktree add -q --detach "$WT/ghp" origin/gh-pages
cd "$WT/ghp"
git checkout -q -B preview-publish
mkdir -p preview

while IFS=$'\t' read -r slot branch sha desc; do
  if [ -e "preview/$slot" ]; then
    echo "== replacing existing slot preview/$slot"
    rm -rf "preview/$slot"
  fi
  cp -a "$WT/src-$slot/site_preview/$slot" "preview/$slot"
done <"$MANIFEST"

# record provenance in preview/slots.json, then regenerate the index
python3 - "$MANIFEST" <<'PY'
import json, pathlib, subprocess, sys

now = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                     capture_output=True, text=True).stdout.strip()
path = pathlib.Path("preview/slots.json")
data = json.loads(path.read_text()) if path.exists() else {"slots": {}}

with open(sys.argv[1], encoding="utf-8") as fh:
    for line in fh:
        line = line.rstrip("\n")
        if not line:
            continue
        slot, branch, sha, desc = line.split("\t")
        data.setdefault("slots", {})[slot] = {
            "branch": branch,
            "sha": sha,
            "description": desc,
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
SLOT_LIST="$(cut -f1 "$MANIFEST" | paste -sd, -)"
git commit -q -m "preview: publish slot(s) $SLOT_LIST — one branch tip per slot" \
                 -m "preview/ only; live root untouched; no push to main."
git push -q origin HEAD:gh-pages
echo "published: $(git rev-parse HEAD)"
