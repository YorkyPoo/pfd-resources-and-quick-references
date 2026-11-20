#!/usr/bin/env python3
"""Re-plant the three defects on the current tip and capture level_rule --check output."""
import subprocess, pathlib, sys

REPO = pathlib.Path("/root/.hermes/profiles/developer/cache/scratch/wt-peep-final")
CPAP = REPO / "docs/procedures/CPAP.md"
BIND = REPO / "audit/level-scan/row-bindings.yaml"


def check():
    p = subprocess.run([sys.executable, "scripts/level_rule.py", "--check"], cwd=REPO,
                       capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip().splitlines()


def restore():
    subprocess.run(["git", "checkout", "--", "docs/procedures/CPAP.md",
                    "audit/level-scan/row-bindings.yaml"], cwd=REPO, check=True)


def report(n, desc, path_repl):
    rc, out = check()
    fails = [l for l in out if l.strip().startswith("-")]
    print(f"DEFECT {n}. {desc}")
    print(f"cmd: python3 scripts/level_rule.py --check")
    print(f"EXIT={rc}")
    for l in fails[:6]:
        print("  " + l.strip())
    print()
    restore()
    return rc


def plant(path, old, new):
    t = path.read_text()
    assert old in t, f"anchor missing in {path}"
    path.write_text(t.replace(old, new, 1))


restore()
t0 = CPAP.read_text()
plant(CPAP, '<span class="lvl lvl-i">I</span> | Consider titrating PEEP',
      '<span class="lvl lvl-emt">EMT</span> | Consider titrating PEEP')
r1 = report(1, "chip set back to EMT on row 6 -> docs/procedures/CPAP.md", None)

plant(CPAP, "Consider titrating PEEP (5–15 mmHg) as needed to improve ventilation.",
      "Consider titrating PEEP (5–15 cmH2O) as needed to improve ventilation.")
r2 = report(2, "ceiling reverted to 15 cmH2O (unit dropped) -> docs/procedures/CPAP.md", None)

anchor = ("  - file: procedures/CPAP.md\n    row: 6\n    pems_page: 245\n")
plant(BIND, anchor, anchor + "    open_question: \"Which source governs the PEEP ceiling?\"\n")
r3 = report(3, "open_question reinstated beside the ruling -> audit/level-scan/row-bindings.yaml", None)

clean = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True, text=True).stdout
print("git status --porcelain after restores:")
print(clean if clean.strip() else "(clean)")
print("SUMMARY", "all caught" if (r1, r2, r3) == (1, 1, 1) else f"UNEXPECTED {r1},{r2},{r3}")
