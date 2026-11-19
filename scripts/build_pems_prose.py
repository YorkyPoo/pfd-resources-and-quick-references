#!/usr/bin/env python3
"""Build `audit/level-scan/pems_prose.json` — an index of PEMS unbadged prose.

WHY THIS EXISTS
---------------
`pems_table.json` holds level-badged GRID ROWS only. In `scripts/pems_canonical.py`
the words `PEARLS`, `NOTES`, `REFERENCES`, `CRITERIA`, `CONTRAINDICATIONS` are
`GRID_STOP` tokens: the grid parse ends at them and everything printed below is
discarded. `audit/level-scan/nowhere-flag-audit.md` §3.1 shows that 12 of the 17
published "PEMS prints this nowhere" flags are falsified by exactly that prose,
plus the p.245 CPAP contraindication block behind three more.

This script extracts that prose. It changes no level and assigns no badge: every
entry carries `"badge": null` because PEMS prints these sections with no level
column at all. A verifier may therefore search this index before asserting that
the source is silent.

HOW
---
Source: the PDF's text layer in **layout mode** (`pdftotext -layout`), one page at
a time, cached at `audit/level-scan/.cache/pems_layout.txt`. Plain-mode text is
NOT usable as the source: on the procedure pages (p.245–p.275 region) it prints
with no spaces between words, and on multi-column bullet lists it reorders the
items. Layout mode keeps the printed spacing and reading order for every page.

Granularity, per the task spec:
  * PEARLS and NOTES  -> one entry per top-level bullet (U+2022), ordinal 1..n
    within that heading on that page. Sub-bullets (`o ...`) stay inside their
    parent bullet. A non-bullet line indented less than the section's bullet
    markers starts a new entry (p.248 prints trailing paragraphs after its last
    bullet). Two text-layer artefacts are corrected so that one entry really is
    one printed bullet: (a) a layout line that prints two bullets side by side
    (the two-column reversible-causes list on p.236/p.264) is split at the
    second glyph — see `_expand_two_column`; (b) a fragment that merely
    continues an unfinished sentence (`p.45 ...to the closest` /
    `• hospital emergency department.`, p.248's flush-left `scientific
    literature...` tail) is folded back into its bullet — see
    `_merge_continuations`, which prints every merge it makes.
  * CONTRAINDICATIONS / INDICATIONS / CRITERIA -> one entry per heading block,
    bullets kept inside the block.
  * A heading whose block has no bullets at all (p.51's Glasgow Coma Scale
    table under PEARLS) is one block entry.

Every entry is then VERIFIED against `pems_chunks/PEMS2024_full.txt` — the
flattened text layer `pems_table.json` cites as `sources.text_layer` — by one of
three checks, and the script fails if none holds:
  * `ordered`: the entry's alphanumeric characters, whitespace removed, appear
    as a contiguous run in that page's flattened text (the normal case);
  * `multiset`: the entry's word multiset is contained in the page's (used on
    multi-column pages, where the flattened stream prints the same words in a
    different column order — p.107 CRITERIA);
  * `bbox_multiset`: letters-only word multiset contained in the PDF word-box
    stream (used on the procedure pages p.245–p.275, whose flattened text prints
    with no spaces and whose word boxes render subscripts as stray digits).
The verbatim characters always come from the same PDF page; verification only
proves they are that page's words and nothing was invented.

Output shape: `{"pages": {"<page>": [entry, ...]}}` with a key for **all 280
PDF pages** — a page with no prose section is an empty list, so "the index
covers the whole document" is checkable rather than implied.

    python3 scripts/build_pems_prose.py            # write the index
    python3 scripts/build_pems_prose.py --check    # compare, write nothing
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pems_level_scan as P  # noqa: E402

REPO = P.REPO
OUT_JSON = os.path.join(REPO, "audit", "level-scan", "pems_prose.json")
LAYOUT_CACHE = os.path.join(P.OUTDIR, ".cache", "pems_layout.txt")
TEXT_LAYER = os.path.join(REPO, "pems_chunks", "PEMS2024_full.txt")

HEADINGS = {"PEARLS", "NOTES", "CONTRAINDICATIONS", "INDICATIONS", "CRITERIA"}
BULLET_LEVEL = {"PEARLS", "NOTES"}
# Any of these ends the prose block: the next heading, or the grid restarting.
STOP = HEADINGS | {"REFERENCES", "ADMINISTRATIVE", "PROCEDURES", "DOCUMENTATION",
                   "PURPOSE", "POLICY", "COMMENT", "AUTHORIZATION",
                   "PROTOCOL", "PROCEDURE"}
SUB_BULLET = re.compile(r"^(?:o|▪|§|\*|·)\s")
BULLET = "\u2022"
# (predecessor, merged tail) for every fragment folded back into its bullet;
# printed by `main()` so the split rule is auditable, not implicit.
MERGES: list[tuple[str, str]] = []


# ---------------------------------------------------------------------------
def _layout_text(force: bool = False) -> dict[int, list[str]]:
    """PDF text layer in layout mode, split per page (cached)."""
    if force or not os.path.exists(LAYOUT_CACHE):
        if not os.path.exists(P.PDF):
            sys.exit(f"PEMS PDF not found at {P.PDF!r}; set PEMS_PDF")
        try:
            txt = subprocess.run(["pdftotext", "-layout", P.PDF, "-"],
                                 capture_output=True, text=True, check=True).stdout
        except FileNotFoundError:
            sys.exit("pdftotext (poppler-utils) is required to read the PEMS PDF")
        os.makedirs(os.path.dirname(LAYOUT_CACHE), exist_ok=True)
        open(LAYOUT_CACHE, "w", encoding="utf-8").write(txt)
    txt = open(LAYOUT_CACHE, encoding="utf-8", errors="replace").read()
    # U+E000..F8FF are this PDF's private-use bullet glyphs (wingding squares,
    # alarm bells). Map them to the standard bullet so blocks read uniformly;
    # they carry no words and never appear in the flattened text layer.
    txt = re.sub(r"[\ue000-\uf8ff]+", BULLET, txt)
    pages = [p.replace("\x0c", "") for p in txt.split("\x0c")]
    if pages and not pages[-1].strip():
        pages.pop()
    return {i: pg.split("\n") for i, pg in enumerate(pages, 1)}


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _stop_token(line: str) -> bool:
    t = line.strip().rstrip(":").strip().upper()
    return t in STOP


def _heading(line: str) -> str | None:
    t = line.strip().rstrip(":").strip().upper()
    return t if t in HEADINGS else None


def _parse_page(lines: list[str]) -> tuple[list[dict], int]:
    """One page's layout lines -> (prose entries, PEARLS heading count)."""
    # The running footer is a block of its own (rule line, protocol title,
    # version, page number). Cut the page at the last footer line so its title
    # is never absorbed into the last bullet.
    cut = len(lines)
    for idx, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("PEMS Regional Patient Care ") or s.startswith("Regional Patient Care "):
            cut = idx
    body = []
    for ln in lines[:cut]:
        s = ln.strip()
        if not s:
            continue
        if re.match(r"^Version:\s", s):
            continue
        if re.match(r"^.*Page \d+ of \d+$", s) or re.match(r"^\d+ of \d+$", s):
            continue
        body.append(ln)
    entries: list[dict] = []
    n_pearls = 0
    i = 0
    while i < len(body):
        head = _heading(body[i])
        if head is None:
            i += 1
            continue
        if head == "PEARLS":
            n_pearls += 1
        j = i + 1
        while j < len(body) and _heading(body[j]) is None and not _stop_token(body[j]):
            j += 1
        block = [ln for ln in body[i + 1:j]]
        if head in BULLET_LEVEL:
            texts = _split_bullets(block)
        else:
            whole = _clean(" ".join(block))
            texts = [whole] if whole else []
        for ordinal, txt in enumerate(texts, 1):
            if txt:
                entries.append({"heading": head, "ordinal": ordinal,
                                "text": txt, "badge": None})
        i = j
    return entries, n_pearls


def _split_bullets(block: list[str]) -> list[str]:
    """Bullet-level split of one heading's lines."""
    lines = [ln for ln in block if ln.strip()]
    if not any(ln.lstrip().startswith(BULLET) for ln in lines):
        whole = _clean(" ".join(lines))
        return [whole] if whole else []
    lines = [sub for ln in lines for sub in _expand_two_column(ln)]
    groups: list[list[str]] = []
    cur: list[str] = []
    marker_indent: int | None = None
    for ln in lines:
        stripped = ln.lstrip()
        is_bullet = stripped.startswith(BULLET)
        if is_bullet:
            if cur:
                groups.append(cur)
            cur = [ln]
            marker_indent = _indent(ln)
        elif cur and marker_indent is not None and _indent(ln) < marker_indent \
                and not SUB_BULLET.match(stripped):
            # a paragraph set back to the left of the bullet list: its own entry
            groups.append(cur)
            cur = [ln]
            marker_indent = _indent(ln)
        else:
            cur.append(ln)
    if cur:
        groups.append(cur)
    out = []
    for grp in groups:
        txt = _clean(" ".join(grp))
        txt = txt[len(BULLET):].strip() if txt.startswith(BULLET) else txt
        if txt:
            out.append(txt)
    return _merge_continuations(out)


# ---------------------------------------------------------------------------
# two printed columns, and bullets that continue an unfinished sentence
# ---------------------------------------------------------------------------
# Two text-layer artefacts break "one entry per top-level bullet". Both are
# corrections to the WRONG split, never a merge of two real bullets.

TERMINAL_PUNCT = re.compile(r"[.:;!?)\]”\"]$")


def _expand_two_column(line: str) -> list[str]:
    """Split a bullet line that holds TWO printed bullets.

    The reversible-causes list on p.236 and p.264 is set in two columns and the
    layout text puts one item from each column on a single line
    (`•  Hypoxia              •  Tension pneumothorax`). One entry per printed
    bullet means 12 entries, not 6 fused pairs — otherwise `p.236 PEARLS #17`
    names two bullets at once and cannot be cited.
    """
    stripped = line.lstrip()
    if not stripped.startswith(BULLET) or stripped.count(BULLET) < 2:
        return [line]
    indent = line[: len(line) - len(stripped)]
    parts = [p.strip() for p in stripped.split(BULLET)[1:]]
    return [f"{indent}{BULLET} {p}" for p in parts if p]


def _merge_continuations(texts: list[str]) -> list[str]:
    """Merge an entry that is really the tail of the previous bullet.

    Sometimes the PDF puts a bullet glyph (or a flush-left continuation line)
    in the middle of one sentence: p.45 prints `…to the closest` then
    `• hospital emergency department.`, and p.248 prints `* Note: … available`
    then `scientific literature and should be reserved…` one character left of
    the bullet column. The marker follows the print, so such a tail would
    otherwise become a fragment entry that reads as a self-contained Pearl and
    can be cited as one. Rule: a group whose text starts lower-case and whose
    predecessor does not end in terminal punctuation continues that predecessor.
    """
    merged: list[str] = []
    for txt in texts:
        if merged and txt[:1].islower() and not TERMINAL_PUNCT.search(merged[-1]):
            MERGES.append((merged[-1], txt))
            merged[-1] = _clean(merged[-1] + " " + txt)
        else:
            merged.append(txt)
    return merged


# ---------------------------------------------------------------------------
def _keys(s: str) -> tuple[str, collections.Counter]:
    return (re.sub(r"[^a-z0-9]", "", s.lower()),
            collections.Counter(re.findall(r"[a-z0-9]+", s.lower())))


def _word_tokens(s: str) -> list[str]:
    """Letters-only word tokens: the word boxes render subscripts as separate
    digits ("ETCO₂" -> "etco", "2"), so digits are noise on this basis."""
    return re.findall(r"[a-z]+", s.lower())


def _bbox_page_words() -> dict[int, collections.Counter]:
    """Per-page token multiset from the PDF word boxes.

    Used as an independent second rendering for pages whose FLATTENED text layer
    prints with no spaces between words: there the printed characters agree but
    the word boundaries are lost, so a word-multiset check cannot be done on it.
    Order is not asserted on this basis (multi-column lists reorder), only that
    every word is one the page prints.
    """
    xml = P._read_pdf_xml(False)
    out: dict[int, collections.Counter] = {}
    for pno, m in enumerate(P.PAGE_RE.finditer(xml), 1):
        ws = P._words(m.group(3))
        out[pno] = collections.Counter(_word_tokens(" ".join(w["t"] for w in ws)))
    return out


def build(force: bool = False) -> tuple[dict, int, list[dict], list[str]]:
    layout = _layout_text(force)
    assert len(layout) == 280, len(layout)
    flat = open(TEXT_LAYER, encoding="utf-8", errors="replace").read()
    parts = re.split(r"--- PAGE (\d+) ---", flat)
    flat_pages = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
    assert len(flat_pages) == 280, len(flat_pages)

    pages: dict[str, list[dict]] = {}
    n_pearls = 0
    methods: list[dict] = []
    failures: list[str] = []
    bbox: dict[int, collections.Counter] | None = None
    for pno, lines in layout.items():
        entries, page_pearls = _parse_page(lines)
        n_pearls += page_pearls
        # every page is a key: "the index covers all 280 pages" must be checkable,
        # and a page with no prose section is an empty list, not a missing page.
        pages[str(pno)] = entries
        if not entries:
            continue
        hay_chars, hay_words = _keys(flat_pages[pno])
        for e in entries:
            chars, words = _keys(e["text"])
            method = None
            if chars and chars in hay_chars:
                method = "ordered"
            elif words and not (words - hay_words):
                method = "multiset"
            else:
                if bbox is None:
                    bbox = _bbox_page_words()
                need = collections.Counter(_word_tokens(e["text"]))
                if need and not (need - bbox[pno]):
                    method = "bbox_multiset"
            if method is None:
                failures.append(f"p.{pno} {e['heading']} #{e['ordinal']}: "
                                f"{e['text'][:80]!r}")
            else:
                methods.append({"page": pno, "heading": e["heading"],
                                "ordinal": e["ordinal"], "method": method})
    return {"pages": pages}, n_pearls, methods, failures


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="build in memory, compare with the committed index, write nothing")
    ap.add_argument("--rebuild", action="store_true", help="re-read the PDF")
    args = ap.parse_args(argv)
    MERGES.clear()
    data, n_pearls, methods, failures = build(args.rebuild)
    n_pages = len(data["pages"])
    n_with = sum(1 for v in data["pages"].values() if v)
    n_entries = sum(len(v) for v in data["pages"].values())
    by_method = collections.Counter(m["method"] for m in methods)
    by_head = collections.Counter(e["heading"] for v in data["pages"].values() for e in v)
    print(f"pages indexed: {n_pages}/280 ({n_with} yielded prose entries)")
    print(f"entries: {n_entries}")
    print(f"PEARLS headings found: {n_pearls}")
    print("by heading: " + ", ".join(f"{k}={v}" for k, v in sorted(by_head.items())))
    print("text-layer verification: " + ", ".join(f"{k}={v}" for k, v in sorted(by_method.items()))
          + f", FAILED={len(failures)}")
    print(f"fragment merges (tail folded back into its bullet): {len(MERGES)}")
    for head, tail in MERGES:
        print(f"  merged: {head[-60:]!r} + {tail[:60]!r}")
    for f in failures[:20]:
        print("  FAIL " + f)
    if failures:
        return 1
    if args.check:
        if not os.path.exists(OUT_JSON):
            print(f"MISSING {os.path.relpath(OUT_JSON, REPO)}")
            return 1
        old = json.load(open(OUT_JSON, encoding="utf-8"))
        same = old == data
        print("index is up to date" if same else "index DIFFERS from a fresh build")
        return 0 if same else 1
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {os.path.relpath(OUT_JSON, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
