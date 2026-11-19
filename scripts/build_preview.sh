#!/usr/bin/env bash
# Build the /preview/ duplicate of the site from the current checkout (main).
# Live build (site/ + gh-pages root) is untouched: output goes to site_preview/.
set -euo pipefail
cd "$(dirname "$0")/.."

MKDOCS="${MKDOCS:-mkdocs}"

python3 scripts/build_preview_cfg.py
rm -rf site_preview
"$MKDOCS" build -f mkdocs.preview.yml

echo "---- preview build checks ----"
if [ -e site_preview/sw.js ]; then
  echo "FAIL: site_preview/sw.js exists" >&2
  exit 1
fi
echo "OK: no site_preview/sw.js"
cat site_preview/robots.txt
test -f site_preview/index.html && echo "OK: site_preview/index.html present"
