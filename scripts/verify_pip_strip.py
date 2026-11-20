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
is not six buttons, or no button is pressed on load.
"""
import argparse
import os
import re
import sys
import urllib.request

PAGES = [
    "protocols/general/02_Cold_Exposure_PROC.html",
    "protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.html",
]


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
    args = ap.parse_args()

    failed = False
    for rel in PAGES:
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
        print(f"  rows   : {len(rows)}  (unverified/OWNER_REQUIRED: {flagged})")
        print(f"  row1   : states={rows[0][0]} tag=\"{tag_txt[0]}\"")
        print("  tags   : " + " | ".join(dict.fromkeys(tag_txt)))
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
