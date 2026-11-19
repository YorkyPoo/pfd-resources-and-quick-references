#!/usr/bin/env python3
"""Look up an action description in the PEMS unbadged-prose index.

`audit/level-scan/pems_prose.json` (built by `scripts/build_pems_prose.py`) holds
PEARLS / NOTES / CONTRAINDICATIONS / INDICATIONS / CRITERIA text that the level
table never sees. Use this before asserting that "PEMS prints this nowhere":
a silence claim is only admissible after a prose search comes back empty.

THE MATCHER IS DELIBERATELY DUMB
--------------------------------
It is token overlap, not clinical reasoning. Query and entry are lower-cased and
split into word tokens; tokens shorter than 3 characters are dropped (they are
almost all articles/prepositions) and so is a small stop-word list. An entry is
returned when at least MIN_OVERLAP (default 0.45) of the query's content tokens
appear in the entry's token set. Results are ordered by that fraction, ties
broken by page then ordinal.

    from pems_prose import lookup
    lookup("right-sided 12-lead ECG")        # -> [(page, heading, ordinal, text), ...]

    python3 scripts/pems_prose.py "contact medical control prior to use of AED"
    python3 scripts/pems_prose.py "CPAP contraindication pneumothorax" --limit 5

A low score is not evidence of absence by itself: paraphrase-heavy actions need
a lower --min-overlap or a tighter query. The helper reports the score so a
verifier can judge it.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(REPO, "audit", "level-scan", "pems_prose.json")
MIN_OVERLAP = 0.45

STOP = {
    "the", "and", "for", "with", "that", "from", "are", "was", "were", "not", "any",
    "all", "this", "these", "those", "into", "than", "then", "when", "where", "which",
    "who", "whom", "its", "his", "her", "their", "our", "you", "your", "may", "can",
    "must", "should", "will", "would", "has", "have", "had", "been", "being", "but",
    "per", "via", "each", "other", "such", "also", "only", "more", "most", "less",
    "any", "anyone", "onto", "upon", "out", "off", "over", "under", "about", "after",
    "before", "during", "while", "without", "within", "against", "between",
}


def _tokens(s: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", s.lower())
            if len(t) >= 3 and t not in STOP}


def load(path: str = INDEX) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def lookup(description: str, min_overlap: float = MIN_OVERLAP,
           index: dict | None = None) -> list[tuple[int, str, int, str]]:
    """Return [(page, heading, ordinal, text)] best match first."""
    idx = index if index is not None else load()
    q = _tokens(description)
    if not q:
        return []
    scored = []
    for page_s, entries in idx["pages"].items():
        for e in entries:
            toks = _tokens(e["text"])
            if not toks:
                continue
            score = len(q & toks) / len(q)
            if score >= min_overlap:
                scored.append((score, int(page_s), e["heading"], e["ordinal"], e["text"]))
    scored.sort(key=lambda x: (-x[0], x[1], x[3]))
    return [(p, h, o, t) for _, p, h, o, t in scored]


def lookup_scored(description: str, min_overlap: float = MIN_OVERLAP,
                  index: dict | None = None) -> list[tuple[float, int, str, int, str]]:
    idx = index if index is not None else load()
    q = _tokens(description)
    if not q:
        return []
    out = []
    for page_s, entries in idx["pages"].items():
        for e in entries:
            toks = _tokens(e["text"])
            if not toks:
                continue
            score = len(q & toks) / len(q)
            if score >= min_overlap:
                out.append((score, int(page_s), e["heading"], e["ordinal"], e["text"]))
    out.sort(key=lambda x: (-x[0], x[1], x[3]))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("description")
    ap.add_argument("--min-overlap", type=float, default=MIN_OVERLAP,
                    help=f"fraction of query content tokens that must appear (default {MIN_OVERLAP})")
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args(argv)
    hits = lookup_scored(args.description, args.min_overlap)
    if not hits:
        print("no prose match — but absence here is only evidence of absence after "
              "the query is tightened and --min-overlap lowered deliberately")
        return 1
    print(f"{len(hits)} match(es), best first (threshold {args.min_overlap}):")
    for score, page, head, ordinal, text in hits[:args.limit]:
        snippet = text if len(text) <= 300 else text[:297] + "..."
        print(f"  {score:.2f}  p.{page} {head} #{ordinal}  {snippet}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
