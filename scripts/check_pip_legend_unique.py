#!/usr/bin/env python3
"""Guard: the protocol legend's markup may exist in ONE place only.

``_legend()`` in ``scripts/mkdocs_pip_strip.py`` is the single definition of the
"Reading the strip" block. A page gets it by writing the ``<!-- PIP_LEGEND -->``
placeholder, which ``on_page_content`` replaces with ``_legend()``. A second copy
in a page or an override would drift the first time a pip colour changed, so the
build fails when ``class="pip-legend"`` appears under ``docs/`` or ``overrides/``.

The same check runs from the hook's ``on_config``, so ``mkdocs build --strict``
fails too. This script is the direct entry point:

    python3 scripts/check_pip_legend_unique.py
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mkdocs_pip_strip import LEGEND_OWNER, GUARD_DIRS, legend_duplicates  # noqa: E402

REPO = os.path.dirname(HERE)


def main() -> int:
    hits = legend_duplicates(REPO)
    if hits:
        print("FAIL: the legend's markup is copied outside " + LEGEND_OWNER)
        for rel in hits:
            print(f"  {rel}")
        print(
            "The page should carry the <!-- PIP_LEGEND --> placeholder instead; "
            "_legend() in " + LEGEND_OWNER + " is the only definition."
        )
        return 1
    print(
        "OK: no class=\"pip-legend\" under "
        + " + ".join(f"{d}/" for d in GUARD_DIRS)
        + " — the legend is defined only in " + LEGEND_OWNER
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
