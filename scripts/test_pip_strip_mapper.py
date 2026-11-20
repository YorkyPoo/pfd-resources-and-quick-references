#!/usr/bin/env python3
"""Prove the pip mapper against the owner's prototype, row by row.

The prototype is `audit/level-scan/reference/protocol-format-sample.html`
(12,492 bytes). Its ten sample rows are the specification the mapper must
reproduce. This test:

1. asserts the reference copy is intact (byte size 12,492),
2. parses the prototype's own ``s:[...]`` state arrays out of the file (so the
   comparison is against the owner's data, not a hand-copied expectation),
3. inverts each array to ``{min_level, mc_required}`` with ``states_to_min``,
4. runs the real ``states_for`` mapper forward from that, and
5. diffs the result.

Exit 0 only when all ten rows and the header substitution match.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from mkdocs_pip_strip import LEVELS, states_for, states_to_min  # noqa: E402

REF = os.path.join(ROOT, "audit", "level-scan", "reference",
                   "protocol-format-sample.html")
EXPECTED_BYTES = 12492

STATE_RE = re.compile(r'\{a:"(.*?)",s:\[([^\]]*)\]\}', re.S)


def main() -> int:
    size = os.path.getsize(REF)
    ok_size = size == EXPECTED_BYTES
    print(f"reference: {os.path.relpath(REF, ROOT)}")
    print(f"  bytes  : {size} (expected {EXPECTED_BYTES}) -> "
          f"{'ok' if ok_size else 'FAIL'}")

    html = open(REF, encoding="utf-8").read()
    rows = STATE_RE.findall(html)
    if len(rows) != 10:
        print(f"  FAIL: parsed {len(rows)} sample rows, expected 10")
        return 1

    bad = 0
    print()
    print(f"  {'#':>2}  {'derived input':<34} {'prototype states':<26} "
          f"{'mapper output':<26} result")
    for i, (action, states_raw) in enumerate(rows, 1):
        prototype = [s.strip().strip('"') for s in states_raw.split(",")]
        min_idx, mc, mc_all = states_to_min(prototype)
        if mc_all:
            desc = "MC chip (all levels)"
        elif min_idx is None:
            desc = "no level"
        else:
            desc = f"min={LEVELS[min_idx]}" + (f" +MC at {LEVELS[min_idx]}" if mc else "")
        out = states_for(min_idx, mc, mc_all)
        good = out == prototype
        if not good:
            bad += 1
        print(f"  {i:>2}  {desc:<34} {','.join(prototype):<26} "
              f"{','.join(out):<26} {'ok' if good else 'FAIL'}")

    # the owner's substitution: headers are R B A I P, not 1 2 3 4 5
    header_ok = LEVELS == ["R", "B", "A", "I", "P"]
    proto_uses_digits = 'const NUM=["1","2","3","4","5"]' in html
    print()
    print(f"  header letters              : {''.join(LEVELS)} -> "
          f"{'ok' if header_ok else 'FAIL'}")
    print(f"  prototype still numbers 1-5 : {proto_uses_digits} "
          f"(substitution confirmed)")

    print()
    if not ok_size or bad or not header_ok:
        print(f"{bad} row(s) disagree; reference size ok={ok_size}; "
              f"header ok={header_ok}")
        return 1
    print("all 10 prototype rows reproduced by the mapper")
    return 0


if __name__ == "__main__":
    sys.exit(main())
