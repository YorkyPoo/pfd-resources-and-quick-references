#!/usr/bin/env bash
# Teardown for /preview/.
#
#   bash audit/level-scan/preview-teardown.sh            # remove ALL slots + index
#   bash audit/level-scan/preview-teardown.sh <slot>     # remove ONE slot, index regenerates
#
# Thin wrapper over scripts/preview_slot_teardown.sh so there is one
# implementation: it writes only the preview/ subtree of gh-pages and never
# rebuilds or touches the live root.
set -euo pipefail

REPO="$(git rev-parse --show-toplevel)"
cd "$REPO"

if [ "$#" -gt 1 ]; then
  echo "usage: $0 [slot]" >&2
  exit 2
fi

SLOT_ARG="${1:---all}"
exec bash "$REPO/scripts/preview_slot_teardown.sh" "$SLOT_ARG"
