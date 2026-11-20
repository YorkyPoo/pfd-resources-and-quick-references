#!/usr/bin/env bash
# Build ONE preview slot from the current checkout into site_preview/<slot>/.
#
#   bash scripts/build_preview.sh pilot
#
# Publishing is a separate step (scripts/publish_preview_slots.sh, which builds
# a branch worktree per slot) so a local build never touches gh-pages.
set -euo pipefail
cd "$(dirname "$0")/.."

SLOT="${1:-local}"
exec python3 scripts/build_preview_slot.py --slot "$SLOT" --repo "$(pwd)"
