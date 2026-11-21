#!/usr/bin/env python3
"""Guard: one legend, and it matches the strip it explains.

Two independent checks, both also run from the pip-strip hook's ``on_config``
so ``mkdocs build --strict`` fails on either:

1. **Single source.** ``_legend()`` in ``scripts/mkdocs_pip_strip.py`` is the
   only definition of the "Reading the strip" block. Pages get it by writing
   the ``<!-- PIP_LEGEND -->`` placeholder, which ``on_page_content`` splices.
   A copy of the block anywhere in the repo (build output excepted) fails the
   check.

2. **No silent drift (both directions).** Every swatch the legend renders must
   be a state ``states_for()`` can emit, and every state the strip emits must
   appear in the legend. A state added to the renderer without a legend line,
   or a legend line for a state that no longer exists, fails.

It also asserts that the reading section still asks for the legend at all, so
the block cannot quietly disappear from ``docs/station-info.md``.

    python3 scripts/check_pip_legend_unique.py
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkdocs_pip_strip import (  # noqa: E402
    LEGEND_OWNER,
    LEGEND_TOKEN,
    legend_duplicates,
    legend_state_problems,
    legend_states,
    strip_states,
)

REPO = os.path.dirname(HERE)
PAGE = os.path.join(REPO, "docs", "station-info.md")


def main() -> int:
    failed = False

    hits = legend_duplicates(REPO)
    if hits:
        failed = True
        print("FAIL: the legend's markup is copied outside " + LEGEND_OWNER)
        for rel, marker in hits:
            print(f"  {rel}  ({marker})")
        print(
            "A page should carry the " + LEGEND_TOKEN + " placeholder instead; "
            "_legend() in " + LEGEND_OWNER + " is the only definition."
        )
    else:
        print(
            "OK: no copy of the legend markup anywhere in the repo — it is "
            "defined only in " + LEGEND_OWNER
        )

    try:
        with open(PAGE, encoding="utf-8") as fh:
            page = fh.read()
    except OSError as exc:
        failed = True
        print(f"FAIL: cannot read {PAGE}: {exc}")
        page = ""
    if page and LEGEND_TOKEN not in page:
        failed = True
        print(f"FAIL: docs/station-info.md does not carry the {LEGEND_TOKEN} placeholder")
    elif page:
        print(f"OK: docs/station-info.md carries the {LEGEND_TOKEN} placeholder")

    problems = legend_state_problems()
    if problems:
        failed = True
        print("FAIL: the legend disagrees with the pip strip it explains:")
        for p in problems:
            print(f"  {p}")
    else:
        print(
            "OK: legend swatches and strip states agree in both directions "
            f"(legend {sorted(legend_states())} == strip {sorted(strip_states())})"
        )

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
