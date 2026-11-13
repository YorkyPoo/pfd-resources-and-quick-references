"""Backfill RULED: lines into the review packet for rows already fixed on the site.

Source of truth is the PACKET's own recorded 'current' cells, not the built site: the site rows
have already been rewritten to their ruled form, so re-reading them would find nothing to do.
Rule applied (owner MC ruling 2026-11-13): MC in a contiguous run to P with no bullets is a
bracketed grant — lowest MC level becomes [X], every level above becomes standing (•).
"""
import re, sys

VAULT = "/root/System/mindpalace/40 - areas/Paramedic/Protocol Level Review Packet.md"
LV = ["EMR", "EMT", "A", "I", "P"]
APPLY = "--apply" in sys.argv

lines = open(VAULT, encoding="utf-8").read().split("\n")
touched, cur, i = [], None, 0
while i < len(lines):
    m = re.match(r"^## (protocols/[^\n]+)$", lines[i])
    if m:
        cur = m.group(1)
        i += 1
        continue
    if re.match(r"^- \[ \] \*\*row \d+\*\* — `mc_only_partial`$", lines[i]) and cur:
        j, cell_line = i + 1, None
        while j < len(lines) and lines[j].startswith("  - "):
            if "current `EMR|EMT|A|I|P`" in lines[j]:
                cell_line = lines[j]
                break
            j += 1
        if cell_line:
            part = cell_line.split("`:")[-1].strip()
            raw = [x.strip().strip("`").strip() for x in part.split("|")]
            # NOTE: the packet prints an empty cell as MIDDLE DOT (U+00B7), so the placeholder has
            # to be excluded or every row looks like it has a bullet and nothing ever matches.
            PLACEHOLDER = {"", "\u00b7", "·", "?", "None"}
            mcs = [k for k, x in enumerate(raw) if x and "MC" in x.upper()]
            bul = [k for k, x in enumerate(raw) if x and x not in PLACEHOLDER and "MC" not in x.upper()]
            if mcs and not bul and len(mcs) < 5 and mcs == list(range(min(mcs), 5)):
                lo = min(mcs)
                ruling = (f"[{LV[lo]}] = {LV[lo]} must contact Medical Control; "
                          f"{', '.join(LV[lo + 1:])} standing (owner MC ruling 2026-11-13)")
                row_no = re.search(r"row (\d+)", lines[i]).group(1)
                lines[i] = lines[i].replace("- [ ]", "- [x]")
                k = i + 1
                while k < len(lines) and lines[k].startswith("  - "):
                    k += 1
                lines.insert(k, f"  - RULED: {ruling}")
                touched.append((cur, row_no, LV[lo]))
                i = k + 1   # resume right after the inserted RULED line, not two past it
                continue
    i += 1

print(f"{'APPLIED' if APPLY else 'DRY RUN'}: {len(touched)} rows would gain a RULED line")
for f, r, lv in touched:
    print(f"   {f.split('/')[-1][:40]:42} row {r:>3} -> [{lv}]")
if APPLY:
    open(VAULT, "w", encoding="utf-8").write("\n".join(lines))
    txt = open(VAULT, encoding="utf-8").read()
    print(f"\nRULED lines now: {txt.count('- RULED:')} | ticked: {len(re.findall(chr(94) + r'- \[x\]', txt, re.M))}")
