#!/usr/bin/env python3
"""C1d: deterministic text-binding pass over the aligner's `no_counterpart` rows.

The aligner (`pems_canonical.align_page`) settles a site row on structure: the
section heading, the ordinal, and the row's own bold label, each PEMS row used at
most once. A row it cannot settle is reported as `no_counterpart` — a local
addition, or a PEMS row worded beyond recognition. This module asks those
leftovers one more question, of text only, before that verdict stands:

    does this row's own wording occur in the PEMS pages its page is aligned to?

No vision, no raster, no new structural rule. The candidate set is the per-page
`pems_row_ledger` — exactly the PEMS rows the aligner already had in scope for
that page — so page scope is unchanged, and the normalisation/tokenisation are
the aligner's own (`pems_canonical.sim`, `label_keys`, `distinctive`,
`pems_level_scan.clean`). No new similarity metric, no per-row special cases, no
hand-edited verdicts.

Two outcomes per row, both recorded on the row as `text_binding`:

  bound_by_text      the row's wording occurs in a free PEMS row on an assigned
                     page. The row is promoted to `matched` against that PEMS row
                     and takes **that row's badge** as its level evidence.
  no_evidence_local  nothing bound. The negative search is recorded too — query
                     terms, pages searched, the best coverage found and why it
                     fell short — so "local" is a checked statement rather than an
                     assumption. `subtype` separates the rows that are simply
                     local from the rows whose best evidence sits on a PEMS row a
                     sibling site row already holds (not local, and not bindable
                     either: that is a shared-row adjudication).

Binding rules (the card's, no looser):

  * `verbatim`      one of the site row's phrases (the whole row, its label head
                    before ':' / '•' / '<br>', or its body) occurs as an exact
                    case-insensitive substring of the PEMS row. The recorded
                    `matched_phrase` is the substring as it appears upstream.
  * `token_binding` coverage >= FLOOR (0.40, the aligner's own text floor: the
                    fraction of the site row's significant tokens that occur in
                    the PEMS row) AND an anchor — a shared drug name (from the
                    site's own pharmacology index) or dose, or the row's whole
                    distinctive label head. A shared ordinary word never binds.

A row that clears neither is `no_evidence_local`, whatever its coverage.
"""
from __future__ import annotations

import os
import re

import pems_canonical as C
import pems_level_scan as P

FLOOR = 0.40                      # the aligner's text floor; never weakened here
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHARM = os.path.join(REPO, "docs", "pharmacology")
LEVEL_COLS = ("EMR", "EMT", "A", "I", "P")

# A row is "free" to take a binding when no site row holds the PEMS row yet.
# `duplicate_in_source` is free: the aligner called the row a copy of another
# PEMS row because their text is >=0.85 similar, which is true of the naloxone IN
# row and the naloxone IV/IO row — different routes, different badges — so a site
# row can legitimately be a duplicate's counterpart. `merged_into_site_row` is
# NOT free: the aligner already found that row's content inside a wider site row,
# and a second claim on it is a shared-row adjudication, not a level fix.
FREE = ("absent", "claimed_by_ambiguous_site_row", "duplicate_in_source")

# Words a site row uses as connective tissue. Dropped so coverage measures the
# intervention rather than the sentence. The aligner's own `_sig` (`sig_tokens`)
# also drops every word shorter than four letters and every digit, which reduces
# "Opiate Overdose: Administer Naloxone 1-2 mg IN" to three tokens; coverage is
# counted here with a stop-list instead so a short dose row is not structurally
# unable to clear any floor. `sim()` — the aligner's score — is untouched.
STOP = set("""the and with for from that this into than then when which while also may should
must consider considered admin administer administered administering patient patients adult adults
pediatric dose doses maximum repeat repeated once until after before only per via apply applied
applies obtain obtained provide provided perform performed assess assessed assessing monitor
monitored monitoring maintain maintained initial protocol protocols procedure procedures refer
referred as needed if is are be been being was were has have had having following indicate
indicated according appropriate each any all other another using use used uses or of to in on at
by an a it its their they them there here which who whom whose what when where why how about above
below up down out off over under again further then both more most such no nor not own same so too
very can will just don should now within without during between through against ensure determine
initiate initiated start started continue continued may might
""".split())

WORD_RE = re.compile(r"[a-z0-9][a-z0-9%/.\-]*")
DOSE_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:[-\u2013\u2014]\s*(\d+(?:\.\d+)?))?\s*"
    r"(mg|mcg|g|ml|meq|j|joules|kg|%|units?)", re.I)


def _drug_tokens() -> set[str]:
    """Drug names, from the site's own pharmacology index.

    The card asks for a *drug* anchor, not any rare word: "Rapid transport to
    Level I/II Trauma Center" shares "center" and "trauma" with a PEMS row about
    immediate transport to the closest ED, and an anchor that accepts those words
    binds two different interventions. The drug list is the site's own, so it is
    checkable without reading the PDF, and it does not depend on the PEMS text.
    """
    out: set[str] = set()
    if not os.path.isdir(PHARM):
        return out
    for fn in sorted(os.listdir(PHARM)):
        if not fn.endswith(".md"):
            continue
        for w in WORD_RE.findall(fn[:-3].lower()):
            if len(w) >= 4:
                out.add(w)
    return out


DRUGS = _drug_tokens()


# ---------- tokens ----------------------------------------------------------

def _words(s: str) -> list[str]:
    return [w.rstrip(".,;:") for w in WORD_RE.findall((s or "").lower())]


def _dose_keys(s: str) -> set[str]:
    """Dose tokens, canonicalised so `1-2 mg` meets `1 – 2 mg` and `0.5–2 mg`."""
    out = set()
    for m in DOSE_RE.finditer(s or ""):
        lo, hi, unit = m.group(1), m.group(2), m.group(3).lower()
        out.add(f"{lo}-{hi} {unit}" if hi else f"{lo} {unit}")
    return out


def _sig(s: str) -> set[str]:
    """Significant tokens: a word of >= 3 letters that is not connective tissue,
    plus every dose."""
    out = {w for w in _words(P.clean(s)) if len(w) >= 3 and w not in STOP}
    out |= _dose_keys(s)
    return out


def _drugs_in(s: str) -> set[str]:
    return {w for w in _words(P.clean(s)) if w in DRUGS}


# ---------- site-row phrases ------------------------------------------------

def phrases(action: str) -> list[tuple[str, str]]:
    """The stretches of a site row that can bind, as (kind, text).

    A site row is a bold label plus a bullet body: "Opiate Overdose:<br>Administer
    Naloxone 1-2 mg IN". The label may name the protocol while the body carries
    the intervention and its dose. Both are the row's own wording, so the row,
    its label head and its body are each available to bind; the kind is recorded
    with the evidence so a human can see which one bound.
    """
    txt = P.clean(action or "")
    out: list[tuple[str, str]] = []
    head = re.split(r":|\u2022|<br\s*/?>", txt, maxsplit=1)[0].strip()
    head = re.sub(r"\s*\([^()]*\)\s*$", "", head).strip().rstrip(" -:;,")
    if _sig(head):
        out.append(("label", head))
    parts = re.split(r":|\u2022|<br\s*/?>", txt, maxsplit=1)
    if len(parts) == 2 and _sig(parts[1]):
        out.append(("body", parts[1].strip().lstrip("\u2022").strip()))
    if _sig(txt):
        out.append(("row", txt))
    out.sort(key=lambda kv: -len(_sig(kv[1])))
    return out


def _substring_in(phrase: str, hay: str) -> str | None:
    """The phrase as it literally appears in `hay` (case-insensitive), or None."""
    pat = r"\s+".join(re.escape(w) for w in phrase.split())
    m = re.search(pat, hay or "", re.I)
    return m.group(0) if m else None


# ---------- scoring ---------------------------------------------------------

def coverage_of(phrase: str, pems: str) -> float:
    """Fraction of `phrase`'s significant tokens that occur in the PEMS row."""
    A, B = _sig(phrase), _sig(pems)
    return len(A & B) / len(A) if A else 0.0


def anchors_of(site: str, pems: str) -> list[str]:
    """The words that can carry a token binding on their own.

    Two kinds, both already trusted elsewhere in this pipeline:
      * a drug name (from the site's pharmacology index) or a dose that both rows
        carry — the card's "drug name plus dose token";
      * the site row's whole distinctive label head, via the aligner's own
        `label_keys` + `distinctive`: every head-noun word of the label must occur
        in the PEMS row. Requiring all of them is what stops "Rapid transport to
        Level I/II Trauma Center" from binding a row that only says
        "transport ... Trauma Center".
    """
    out = _drugs_in(site) & _drugs_in(pems)
    out |= _dose_keys(site) & _dose_keys(pems)
    keys = C.distinctive(C.label_keys(P.clean(site)))
    # Two words minimum: one shared word is not a label head, it is a shared word
    # ("Oxygen Administration" -> "oxygen" would otherwise anchor oxygen to any
    # row that mentions oxygen, which is the failure mode the aligner's label
    # rule avoids by requiring EVERY key of the label).
    if len(keys) >= 2 and keys <= {t[:6] for t in _sig(P.clean(pems))}:
        out |= set(keys)
    return sorted(out)


def upstream_anchors(anchors: list[str], pems: str) -> list[str]:
    """The anchors as they are written in the PEMS row.

    The audit trail must name the phrase that actually occurs upstream, so a dose
    recorded as `1-2 mg` comes back as the source's own `1 – 2 mg`, and a
    six-character label prefix (`cardio`) comes back as the word it prefixes
    (`cardiac`). The verifier then checks the phrase against the PEMS row text
    itself rather than against this function's opinion of it.
    """
    raw_dose = {}
    for m in DOSE_RE.finditer(pems or ""):
        lo, hi, unit = m.group(1), m.group(2), m.group(3).lower()
        raw_dose.setdefault(f"{lo}-{hi} {unit}" if hi else f"{lo} {unit}", m.group(0))
    words = _words(pems)
    out: list[tuple[int, str]] = []
    for a in anchors:
        if a in raw_dose:
            text = raw_dose[a]
        elif a in words:
            text = a
        else:                      # a label key: a 6-character prefix
            text = next((w for w in words if w.startswith(a)), a)
        out.append(((pems or "").lower().find(text.lower()), text))
    return [t for _i, t in sorted(out)]


def score(action: str, pems: str) -> dict:
    """Best reading of this site row against one PEMS row."""
    verb = None
    for kind, phrase in phrases(action):
        hit = _substring_in(phrase, pems)
        if hit and len(_sig(hit)) >= 2:
            verb = {"phrase_kind": kind, "phrase": phrase, "matched_phrase": hit}
            break
    best_cov, best_kind, best_phrase = 0.0, "row", ""
    for kind, phrase in phrases(action):
        c = coverage_of(phrase, pems)
        if c > best_cov:
            best_cov, best_kind, best_phrase = c, kind, phrase
    return {"verbatim": verb, "coverage": best_cov, "coverage_basis": best_kind,
            "coverage_phrase": best_phrase,
            # the card's definition, unmodified: coverage of the WHOLE site row,
            # kept alongside the best phrase so an inflated short-label reading
            # can never masquerade as broad textual agreement
            "coverage_row": coverage_of(P.clean(action), pems),
            "anchors": anchors_of(action, pems), "sim": C.sim(action, pems)}


def _rank(r: dict) -> tuple:
    return (1 if r["verbatim"] else 0, round(r["coverage"], 6), len(r["anchors"]),
            round(r["sim"], 6))


def best_candidate(action: str, entries: list[dict]) -> dict | None:
    """Highest-ranked in-scope PEMS row for this site row.

    Ties are broken by document order (page, then ordinal), so the result is
    deterministic; when two rows score the same, both appear in the page evidence
    and the report names them rather than hiding the tie.
    """
    scored = []
    for e in entries:
        s = score(action, e["verbatim_text"])
        s["entry"] = e
        scored.append(s)
    if not scored:
        return None
    scored.sort(key=lambda s: (-_rank(s)[0], -_rank(s)[1], -_rank(s)[2], -_rank(s)[3],
                               s["entry"]["pems_page"], s["entry"]["ordinal"]))
    return scored[0]


def candidates(ledger: list[dict]) -> list[dict]:
    """PEMS rows in this page's scope that no site row holds yet."""
    return [e for e in ledger if e.get("disposition") in FREE]


def held_by(entry: dict) -> str | None:
    """Which site row already holds this PEMS row, if any."""
    if entry.get("site_row") not in (None, ""):
        return str(entry["site_row"])
    if entry.get("claimed_by_site_rows"):
        return ",".join(str(x) for x in entry["claimed_by_site_rows"])
    return None


def _dotted(columns: dict | None) -> list[str]:
    return [c for c in LEVEL_COLS if (columns or {}).get(c)]


def badge_agrees(site_cells: list[str], badge_columns: dict | None) -> bool | None:
    """Does the site's published level cell set equal the PEMS row's?

    A PEMS row prints one mark per level it applies to (A, I and P all dotted for
    an "A" row), and so does the site's grid, so the two sets are directly
    comparable. None when there is nothing to compare.
    """
    if not badge_columns:
        return None
    site = {c for c, v in zip(LEVEL_COLS, site_cells or []) if (v or "").strip()}
    pems = set(_dotted(badge_columns))
    if not site or not pems:
        return None
    return site == pems


# ---------- the verdict -----------------------------------------------------

def _evidence(s: dict, columns: dict | None, site_cells: list[str]) -> dict:
    """The auditable shape of one scored candidate."""
    e = s["entry"]
    return {"pems_page": e["pems_page"], "pems_ordinal": e["ordinal"],
            "pems_row_text": e["verbatim_text"], "badge_tokens": e["badges"],
            "badge_columns": _dotted(columns) or None,
            "coverage": round(s["coverage"], 3),
            "coverage_row": round(s["coverage_row"], 3),
            "coverage_basis": s["coverage_basis"],
            "anchors": upstream_anchors(s["anchors"], e["verbatim_text"]),
            "similarity": round(s["sim"], 3),
            "held_by_site_row": held_by(e), "disposition": e["disposition"],
            "badge_agrees_with_site": badge_agrees(site_cells, columns)}


def classify(action: str, ledger: list[dict], site_cells: list[str] | None = None,
             columns: dict | None = None) -> dict:
    """Apply the binding rules to one site row. A pure function of its inputs."""
    site_cells = site_cells or []
    query = sorted(_sig(action))
    pages = sorted({e["pems_page"] for e in ledger})
    free = candidates(ledger)
    b_free = best_candidate(action, free)
    b_any = best_candidate(action, ledger)
    base = {"query": query, "pages_searched": pages, "free_candidates": len(free)}

    if b_free is not None:
        v = b_free["verbatim"]
        if v:
            return {**base, "verdict": "bound_by_text", "method": "verbatim",
                    "matched_phrase": v["matched_phrase"],
                    "phrase_kind": v["phrase_kind"], "phrase": v["phrase"],
                    **_evidence(b_free, columns, site_cells)}
        if b_free["coverage"] >= FLOOR and b_free["anchors"]:
            return {**base, "verdict": "bound_by_text", "method": "token_binding",
                    "matched_phrase": " ".join(
                        upstream_anchors(b_free["anchors"],
                                         b_free["entry"]["verbatim_text"])),
                    "phrase_kind": b_free["coverage_basis"],
                    "phrase": b_free["coverage_phrase"],
                    **_evidence(b_free, columns, site_cells)}

    # Nothing bound. Say why, with the best look at the whole page scope.
    out = {**base, "verdict": "no_evidence_local"}
    if b_any is None:
        out.update(subtype="no_pems_row_in_scope",
                   pems_page=None, pems_ordinal=None, pems_row_text="",
                   badge_tokens=[], badge_columns=None, coverage=0.0,
                   coverage_row=0.0, coverage_basis=None, anchors=[], similarity=0.0,
                   held_by_site_row=None, disposition=None,
                   badge_agrees_with_site=None,
                   note="the page resolved no PEMS rows at all")
        return out
    holder = held_by(b_any["entry"])
    if holder and b_any["coverage"] >= FLOOR:
        out.update(subtype="best_evidence_is_held",
                   note=("this row's best text evidence is p.%s row %s (coverage "
                         "%.2f, badge %s), which site row %s already holds: the row "
                         "is not a local addition, it is a second site row on an "
                         "already-attributed PEMS row — a shared-row adjudication, "
                         "not a level fix"
                         % (b_any["entry"]["pems_page"], b_any["entry"]["ordinal"],
                            b_any["coverage"], "/".join(b_any["entry"]["badges"]),
                            holder)),
                   **_evidence(b_any, columns, site_cells))
        return out
    best = b_free or b_any
    out.update(**_evidence(best, columns, site_cells))
    if best["coverage"] >= FLOOR and not best["anchors"]:
        out.update(subtype="no_anchor",
                   note=("coverage %.2f (whole row %.2f) clears the %.2f floor, but the "
                         "row shares no drug name, no dose and no whole label head with "
                         "that PEMS row, so the binding would rest on an ordinary word: %s"
                         % (best["coverage"], best["coverage_row"], FLOOR,
                            best["entry"]["verbatim_text"][:160])))
    else:
        out.update(subtype="below_floor",
                   note=("no free PEMS row in scope reaches the %.2f floor for this "
                         "row (best %.2f against p.%s row %s%s)"
                         % (FLOOR, best["coverage"], best["entry"]["pems_page"],
                            best["entry"]["ordinal"],
                            ", shared words: " + ", ".join(best["anchors"])
                            if best["anchors"] else "")))
    return out


# ---------- application to an alignment result ------------------------------

def apply(res: dict, site_rows: dict, columns_by_row: dict | None = None) -> list[dict]:
    """Run the pass over one page result, in place.

    `site_rows` maps a site row number to its full text (the alignment result
    truncates `action` to 200 characters; binding must see all of it).
    `columns_by_row` maps (pems_page, ordinal) to the PEMS row's level columns.
    Bound rows are promoted to `matched`; every other `no_counterpart` row keeps
    its status and gains its `text_binding` evidence. Returns the promotions.
    """
    ledger = res.get("pems_row_ledger") or []
    columns_by_row = columns_by_row or {}
    promoted: list[dict] = []
    for row in res.get("rows") or []:
        if row.get("status") != "ambiguous" or row.get("reason_kind") != "no_counterpart":
            continue
        num = row["site_row"]
        action = site_rows.get(num) or site_rows.get(str(num)) or row["action"]
        cells = row.get("cells") or []
        # First pass picks the candidate; the badge columns belong to the row it
        # cites, so classify again with those columns resolved.
        v = classify(action, ledger, cells)
        v = classify(action, ledger, cells,
                     columns_by_row.get((v.get("pems_page"), v.get("pems_ordinal"))))
        row["text_binding"] = v
        if v["verdict"] != "bound_by_text":
            continue
        e = next((x for x in ledger
                  if x["pems_page"] == v["pems_page"]
                  and x["ordinal"] == v["pems_ordinal"]), None)
        assert e is not None, f"bound row names a PEMS row outside the page ledger: {v}"
        row.update(status="matched", pems_page=v["pems_page"],
                   pems_ordinal=v["pems_ordinal"], pems_section=e.get("section", ""),
                   pems_text=e["verbatim_text"][:240], badges=list(v["badge_tokens"]),
                   similarity=round(v["similarity"], 3),
                   match_basis=f"text-binding:{v['method']}")
        row.pop("reason", None)
        row.pop("reason_kind", None)
        was = e.get("disposition")
        e["disposition"] = "matched"
        e["site_row"] = num
        e["claimed_by_site_rows"] = []
        e["note"] = f"bound by the C1d text pass ({v['method']}); was {was}"
        absent = res.get("absent") or []
        for i, a in enumerate(list(absent)):
            if a.get("pems_page") == v["pems_page"] and a.get("ordinal") == v["pems_ordinal"]:
                absent.pop(i)
                break
        promoted.append(row)
    return promoted


def band(coverage: float) -> int:
    """The card's coverage bands: 0 = 0.0, 1 = 0.1, 2 = 0.2, 3 = >=0.3."""
    if coverage < 0.1:
        return 0
    if coverage < 0.2:
        return 1
    if coverage < 0.3:
        return 2
    return 3


BAND_LABEL = {0: "0.0", 1: "0.1", 2: "0.2", 3: ">=0.3"}


def write_md(results: list[dict], path: str) -> None:
    """`text-binding.md`: the evidence for all 86 rows, readable without JSON."""
    c = counts(results)
    rows = []
    for p in results:
        for r in p.get("rows") or []:
            if r.get("text_binding"):
                rows.append((p["site_page"], r))
    bands = {0: 0, 1: 0, 2: 0, 3: 0}
    for _page, r in rows:
        tb = r["text_binding"]
        bands[band(tb.get("coverage_row", tb["coverage"]))] += 1
    bound = [(pg, r) for pg, r in rows if r["text_binding"]["verdict"] == "bound_by_text"]
    local = [(pg, r) for pg, r in rows if r["text_binding"]["verdict"] != "bound_by_text"]
    sub = c["no_evidence_local_by_subtype"]

    L = ["# Text-binding pass over the `no_counterpart` rows (C1d)\n\n",
         "Every row the structural aligner reported as `no_counterpart` was searched "
         "once more, on text alone, inside the PEMS pages its page is aligned to. "
         "No vision, no raster, no change to the aligner's scope: the candidates are "
         "the rows of the page's own `pems_row_ledger`.\n\n",
         "A row binds on `verbatim` (one of its phrases is an exact substring of the "
         "PEMS row) or on `token_binding` (coverage of the row's significant tokens "
         "clears the aligner's 0.40 floor AND the row shares a drug name, a dose, or "
         "its whole distinctive label head with that PEMS row). Anything else is "
         "`no_evidence_local`, and its negative search is recorded too.\n\n",
         f"**{len(rows)} rows** — bound_by_text **{len(bound)}**, "
         f"no_evidence_local **{len(local)}** ("
         + ", ".join(f"{k} {v}" for k, v in sub.items()) + ").\n\n",
         "Coverage bands (coverage of the whole site row against its best candidate "
         "in the page's own scope): "
         + ", ".join(f"{BAND_LABEL[b]} → {bands[b]}" for b in sorted(bands)) + ".\n\n",
         "## Bound and promoted to `matched`\n\n"]
    if not bound:
        L.append("None.\n\n")
    for pg, r in sorted(bound, key=lambda x: (x[0], str(x[1]["site_row"]))):
        tb = r["text_binding"]
        L.append(f"### `{pg.split('/')[-1]}` row {r['site_row']} → p.{tb['pems_page']} "
                 f"row {tb['pems_ordinal']} badge `{'/'.join(tb['badge_tokens'])}`\n\n"
                 f"- site row: {r['action'][:300]}\n"
                 f"- PEMS row ({tb['disposition']}): {tb['pems_row_text'][:300]}\n"
                 f"- method `{tb['method']}` ({tb['phrase_kind']}), coverage "
                 f"{tb['coverage']:.2f} (whole row {tb.get('coverage_row', 0):.2f}), "
                 f"anchors: {', '.join(tb['anchors']) or '—'}\n"
                 f"- matched phrase: `{tb['matched_phrase']}`\n"
                 f"- site level cells: {r['cells']} vs PEMS badge columns: "
                 f"{tb['badge_columns']} — agrees: {tb['badge_agrees_with_site']}\n\n")

    L.append("## No evidence for a free PEMS row (`no_evidence_local`)\n\n")
    for subtype in sorted({r["text_binding"]["subtype"] for _p, r in local}):
        group = [(pg, r) for pg, r in local if r["text_binding"]["subtype"] == subtype]
        L.append(f"### `{subtype}` — {len(group)} rows\n\n")
        for pg, r in sorted(group, key=lambda x: (x[0], str(x[1]["site_row"]))):
            tb = r["text_binding"]
            L.append(f"- `{pg.split('/')[-1]}` row {r['site_row']} "
                     f"(p.{tb['pems_page']} row {tb['pems_ordinal']}, coverage "
                     f"{tb['coverage']:.2f}) — {tb['note']}\n"
                     f"  - site row: {r['action'][:220]}\n"
                     f"  - pages searched: {tb['pages_searched']}; free candidates: "
                     f"{tb['free_candidates']}; query: {', '.join(tb['query'][:12])}\n")
        L.append("\n")
    open(path, "w", encoding="utf-8").write("".join(L))


def counts(results: list[dict]) -> dict:
    """Census of the pass over a list of page results."""
    out: dict = {"bound_by_text": 0, "no_evidence_local": 0}
    sub: dict[str, int] = {}
    for p in results:
        for r in p.get("rows") or []:
            tb = r.get("text_binding")
            if not tb:
                continue
            out[tb["verdict"]] = out.get(tb["verdict"], 0) + 1
            if tb["verdict"] == "no_evidence_local":
                sub[tb["subtype"]] = sub.get(tb["subtype"], 0) + 1
    out["no_evidence_local_by_subtype"] = dict(sorted(sub.items()))
    return out
