#!/usr/bin/env python3
"""Independent cross-check (not the guard): count <a> inside any .pfd-cap element
in a built page, with a plain regex, so the answer does not come from the guard's
own HTMLParser."""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "site/index.html"
html = open(path, encoding="utf-8").read()
pat = re.compile(r'<[a-z]+ class="[^"]*\bpfd-cap\b[^"]*"[^>]*>(.*?)</[a-z]+>', re.S)
caps = pat.findall(html)
anchors = sum(c.count("<a") for c in caps)
print(f"{path}: {len(caps)} .pfd-cap element(s), {anchors} <a> inside them")
for c in caps:
    print("   ", " ".join(re.sub(r"<[^>]+>", "", c).split()) or "(empty)")
print("PASS" if anchors == 0 else "FAIL")
sys.exit(0 if anchors == 0 else 1)
