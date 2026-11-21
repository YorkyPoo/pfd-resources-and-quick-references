"""Prove no changed line in docs/stylesheets/extra.css lives inside a slate-scoped rule.

Same detector as the light-colour card, parameterised by base so it can be re-run
on the rebased branch (base a869a4c3) instead of origin/main.

Usage: python3 audit/gates/slate_check.py [BASE]      (default: a869a4c3)
"""
import subprocess
import sys

BASE = sys.argv[1] if len(sys.argv) > 1 else "a869a4c3"
FILE = "docs/stylesheets/extra.css"


def blocks(lines):
    out, buf, start = [], [], None
    for i, raw in enumerate(lines, start=1):
        s = raw
        while "/*" in s and "*/" in s:
            a, b = s.index("/*"), s.index("*/")
            s = s[:a] + s[b + 2:]
        if "{" in s and start is None:
            pre = s.split("{")[0]
            if pre.strip():
                buf = [pre]
            start = i
            s = s.split("{", 1)[1]
        if start is not None:
            if "}" in s:
                sel = " ".join(" ".join(buf).split())
                out.append((sel, start, i))
                start, buf = None, []
                s = s.split("}", 1)[1]
    return out


old_lines = subprocess.run(["git", "show", f"{BASE}:{FILE}"],
                           capture_output=True, text=True).stdout.splitlines()
new_lines = open(FILE, encoding="utf-8").read().splitlines()
old_blocks, new_blocks = blocks(old_lines), blocks(new_lines)

diff = subprocess.run(["git", "diff", "-U0", BASE, "--", FILE],
                      capture_output=True, text=True).stdout.splitlines()

old_no = new_no = None
changed = []
for ln in diff:
    if ln.startswith("@@"):
        o, n = ln.split()[1:3]
        old_no = int(o.split(",")[0].lstrip("-"))
        new_no = int(n.split(",")[0].lstrip("+"))
        continue
    if ln[:3] in ("---", "+++") or old_no is None:
        continue
    if ln.startswith("-"):
        changed.append(("old", old_no, ln[1:])); old_no += 1
    elif ln.startswith("+"):
        changed.append(("new", new_no, ln[1:])); new_no += 1
    else:
        old_no += 1; new_no += 1


def slate_hit(side, line_no):
    bset = old_blocks if side == "old" else new_blocks
    for sel, a, b in bset:
        if a <= line_no <= b and "slate" in sel:
            return sel
    return None


hits = []
for side, no, text in changed:
    if not text.strip():
        continue
    sel = slate_hit(side, no)
    if sel:
        hits.append((side, no, text.strip()[:80], sel[:110]))

added = sum(1 for c in changed if c[0] == "new")
removed = sum(1 for c in changed if c[0] == "old")
print(f"base: {BASE}   file: {FILE}")
print(f"slate-scoped rule blocks: base={sum(1 for s,_,_ in old_blocks if 'slate' in s)} "
      f"head={sum(1 for s,_,_ in new_blocks if 'slate' in s)}  (total blocks head={len(new_blocks)})")
ctrl = next((s, a, b) for s, a, b in new_blocks if "slate" in s and b - a >= 1)
print("positive control: line", ctrl[1] + 1, "resolves to slate block ->",
      bool(slate_hit("new", ctrl[1] + 1)))
print(f"added lines: {added}   removed lines: {removed}")
print(f"changed lines inside a slate-scoped rule: {len(hits)}")
for h in hits:
    print("   HIT", h)
print("VERDICT:", "PASS — zero slate lines changed" if not hits else "FAIL")
sys.exit(1 if hits else 0)
