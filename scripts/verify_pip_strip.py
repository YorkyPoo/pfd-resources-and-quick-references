#!/usr/bin/env python3
"""Report the pip-strip evidence for the two pilot pages.

    python3 scripts/verify_pip_strip.py --base <site_dir or https://…/preview/pilot/>

Reads the *rendered HTML* — the same bytes a phone gets — and prints, per page:

  * the picker buttons and which one is aria-pressed
  * the strip header letters
  * the tally line
  * row count, and how many rows are in the OWNER_REQUIRED (unverified) class
  * one row's tag text, and every distinct tag

Exit 1 if a page is missing the block, the header is not R B A I P, the picker
is not six buttons, no button is pressed on load, or **any row's rendered
`data-states` disagrees with the level chip in the page's markdown source**
(both are printed side by side when it does).

The source cross-check is the point: the strip's whole job is to restate the
level chip, so a verifier that only counts rows and buttons cannot catch a
strip that says the wrong thing.
"""
import argparse
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mkdocs_pip_strip import LEVEL_CLASS, LEVELS, states_for  # noqa: E402

PAGES = [
    ("protocols/general/02_Cold_Exposure_PROC.md",
     "protocols/general/02_Cold_Exposure_PROC.html"),
    ("protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.md",
     "protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.html"),
]

CHIP_RE = re.compile(r'class="lvl(?P<cls>[^"]*)"')


def states_from_chip(cell: str):
    """(states, flagged) for one markdown Level cell, using the same mapper."""
    m = CHIP_RE.search(cell)
    cls = m.group("cls") if m else ""
    flagged = "lvl-own" in cls
    min_idx = None
    for name, idx in LEVEL_CLASS.items():
        if re.search(r"\b" + re.escape(name) + r"\b", cls):
            min_idx = idx
            break
    mc_all = "lvl-mc" in cls
    bracketed = "lvl-mc-req" in cls or "lvl-req" in cls
    mc = {min_idx} if (bracketed and min_idx is not None) else set()
    return states_for(min_idx, mc, mc_all), flagged


def expected_rows(md_path: str):
    """[(num, states, flagged)] from the markdown table, in page order."""
    with open(md_path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    out = []
    in_table = False
    for line in lines:
        s = line.strip()
        if s.startswith("|") and s.count("|") >= 4:
            cells = [c.strip() for c in s.strip("|").split("|")]
            if len(cells) < 3:
                continue
            if not in_table:
                in_table = True  # header row
                continue
            if set(cells[0]) <= set(":- "):  # separator
                continue
            num, chip = cells[0], cells[1]
            if not re.fullmatch(r"\d+[a-z]?", num):
                in_table = False
                continue
            states, flagged = states_from_chip(chip)
            out.append((num, states, flagged))
        else:
            if in_table:
                break
    return out


def load(base: str, rel: str) -> str:
    if base.startswith("http"):
        url = base.rstrip("/") + "/" + rel
        req = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
        with urllib.request.urlopen(req, timeout=30) as fh:
            return fh.read().decode("utf-8", "replace")
    with open(os.path.join(base, rel), encoding="utf-8") as fh:
        return fh.read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--src", default="docs",
                    help="docs/ dir holding the markdown the site was built from "
                         "(default: docs). Every row is checked against it.")
    args = ap.parse_args()

    failed = False
    for md_rel, rel in PAGES:
        print("=" * 78)
        print(rel)
        try:
            html = load(args.base, rel)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL: cannot load ({exc})")
            failed = True
            continue

        i = html.find("data-pip-block")
        if i < 0:
            print("  FAIL: no data-pip-block in the rendered page")
            failed = True
            continue
        blk = html[i:html.find("</tbody></table></div>", i)]

        btns = re.findall(
            r'<button type="button" class="pip-btn[^"]*" data-level="([^"]+)" '
            r'aria-pressed="([^"]+)">([^<]*)</button>', blk)
        print("  picker : " + " | ".join(f"{t} pressed={p}" for d, p, t in btns))
        if len(btns) != 6:
            print(f"  FAIL: {len(btns)} picker buttons, expected 6")
            failed = True
        if not any(p == "true" for _, p, _ in btns):
            print("  FAIL: nothing aria-pressed on load")
            failed = True
        if [d for d, _, _ in btns] != ["R", "B", "A", "I", "P", "all"]:
            print("  FAIL: picker order is not R B A I P + Show all")
            failed = True

        head = re.findall(r'<span class="pip-strip pip-strip-head">((?:<i>[^<]*</i>)+)</span>', blk)
        letters = re.findall(r"<i>([^<]*)</i>", head[0]) if head else []
        print("  header : " + " ".join(letters))
        if letters != ["R", "B", "A", "I", "P"]:
            print("  FAIL: strip header is not R B A I P")
            failed = True

        tally = re.search(r'class="pip-tally"[^>]*>(.*?)</p>', blk, re.S)
        tally_txt = re.sub(r"\s+", " ", re.sub("<[^>]+>", "", tally.group(1))).strip() if tally else ""
        print(f"  tally  : {tally_txt}")
        if not tally_txt:
            print("  FAIL: no tally line")
            failed = True

        rows = re.findall(r'<tr data-states="([^"]+)"([^>]*)>(.*?)</tr>', blk, re.S)
        flagged = sum(1 for _, a, _ in rows if "data-unverified" in a)
        tags = [re.search(r'pip-tag [a-z]+">([^<]*)<', r[2]) for r in rows]
        tag_txt = [t.group(1) if t else "?" for t in tags]
        nums = [re.search(r'<td class="pip-n">([^<]*)</td>', r[2]) for r in rows]
        nums = [n.group(1).strip() if n else "?" for n in nums]
        print(f"  rows   : {len(rows)}  (unverified/OWNER_REQUIRED: {flagged})")
        print(f"  row1   : states={rows[0][0]} tag=\"{tag_txt[0]}\"")
        print("  tags   : " + " | ".join(dict.fromkeys(tag_txt)))

        # ---- every row against the level chip in its own markdown source ----
        src_path = os.path.join(args.src, md_rel)
        try:
            want = expected_rows(src_path)
        except OSError as exc:
            print(f"  FAIL: cannot read source {src_path} ({exc})")
            failed = True
            want = []
        print(f"  source : {md_rel} — {len(want)} chip rows")
        print("  --- n | rendered | chip ---")
        for i in range(max(len(rows), len(want))):
            has_got = i < len(rows)
            has_exp = i < len(want)
            if has_got and has_exp:
                g_num, g_st = nums[i], rows[i][0]
                e_num, e_st = want[i][0], ",".join(want[i][1])
                if g_st == e_st and g_num == e_num:
                    print(f"  OK  {g_num:>3} | {g_st:<24} | {e_st}"
                          f"  (chip row {e_num}{', OWNER_REQUIRED' if want[i][2] else ''})")
                else:
                    print(f"  BAD {g_num:>3} | {g_st:<24} | {e_st}")
                    print(f"  FAIL: row {g_num} renders {g_st}, chip says {e_st}"
                          + ("" if g_num == e_num else f" (row number {g_num} vs {e_num})"))
                    failed = True
            elif has_got:
                print(f"  BAD {nums[i]:>3} | {rows[i][0]:<24} | <no chip row>")
                print(f"  FAIL: row {nums[i]} is rendered but has no chip in the source")
                failed = True
            else:
                e_st = ",".join(want[i][1])
                print(f"  BAD {want[i][0]:>3} | {'<not rendered>':<24} | {e_st}")
                print(f"  FAIL: source row {want[i][0]} ({e_st}) is missing from the page")
                failed = True
        n_in_tally = re.search(r"(\d+) actions", tally_txt)
        if n_in_tally and int(n_in_tally.group(1)) != len(rows):
            print(f"  FAIL: tally says {n_in_tally.group(1)} actions, "
                  f"table has {len(rows)} rows")
            failed = True
        if flagged and f"{flagged} level unverified" not in tally_txt:
            print(f"  FAIL: {flagged} unverified row(s) not disclosed in the tally")
            failed = True
        if 'role="img"' not in blk or "aria-label=" not in blk:
            print("  FAIL: strip has no text alternative")
            failed = True

    print("=" * 78)
    print("FAILED" if failed else "OK — both pages carry the pip strip")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
