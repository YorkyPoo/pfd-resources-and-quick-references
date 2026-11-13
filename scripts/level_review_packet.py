"""Protocol provider-level review packet — generator with a rulings log and safe regeneration.

WHY THIS FILE HAS TWO MODES
----------------------------
The packet is a WORKING DOCUMENT: the owner ticks rows and types levels into it. A generator that
simply rewrites the file destroys every ruling. So regeneration is a MERGE:

  python scripts/level_review_packet.py --merge <existing.md> <out.md>   # default-safe
  python scripts/level_review_packet.py --fresh <out.md>                 # explicit, destroys rulings

The merge keeps, per item key (file + row number): the tick state, the hand-written ruling line
(matched on its "  - RULED:" prefix), and the two edited blank fields. A ruling whose row no longer
exists in the new build is NOT silently dropped — it lands in a "carried rulings with NO matching
row" section so a deleted or renumbered row surfaces instead of vanishing.

LEVEL SEMANTICS (owner ruling 2026-11-13) — the model everything here is built on:
  - a step's level row means that level AND every level above it may perform the intervention
  - bracketed entry level `[A]` means the A must contact Medical Control for permission, while
    levels above (I, P) perform it as a standing order
  - a bare `MC` in every cell means ALL levels must contact Medical Control
  - administrative protocol rows are not level-gated at all (owner ruling 2026-11-11)
"""
import re, glob, os, sys, difflib, collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = REPO + "/docs"
PDF_TXT = os.environ.get("PEMS_TXT", "/root/.hermes/cache/scratch/pems2024.txt")
LV = ["EMR", "EMT", "A", "I", "P"]
RULED_PREFIX = "  - RULED:"


def cells(line):
    """escape-aware: \\| is cell TEXT, not a separator (borrowed from table_audit.py)"""
    s = line.strip().strip("|").replace("\\|", "\x00")
    return [c.strip().replace("\x00", "|") for c in s.split("|")]


def clean(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"[`*_\\]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def nz(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", s.lower())).strip()


FOOTER = lambda t: t.startswith("PEMS Regional") or "Version:" in t or t.startswith("Page ")
TOKRE = re.compile(r"^\s{0,14}(\[?(?:EMR|EMT|A|I|P|MC)\]?)\s{2,}(\S.*)$")
RIGHT = re.compile(r"(?<=[\w\)\.])\s{3,}(EMR|EMT|A|I|P|MC|\[[A-Z]+\])\s*$")
SECT = re.compile(r"^\s*(PEARLS|CRITERIA|PROCEDURES|NOTES|REFERENCES|ADMINISTRATIVE)\s*$")

# ---------------- PEMS: one entry per PROTOCOL block ----------------
PEMS = []
if os.path.exists(PDF_TXT):
    pages = open(PDF_TXT, encoding="utf-8", errors="replace").read().split("\f")
    for pno, page in enumerate(pages, 1):
        ls = page.splitlines()
        title = ""
        for l in ls[:4]:
            s = l.strip()
            if s and len(s) > 6 and not s.isupper() and "PEMS Regional" not in s:
                title = re.sub(r"\s+", " ", s)
                break
        idx = [i for i, l in enumerate(ls) if l.strip() == "PROTOCOL"]
        if not idx:
            continue
        start = idx[0] + 1
        end = next((j for j in range(start, len(ls)) if SECT.match(ls[j])), len(ls))
        acts, last = [], None
        for l in ls[start:end]:
            if not l.strip():
                continue
            m = TOKRE.match(l)
            if m:
                last = m.group(1)
                t = re.sub(r"\s+", " ", RIGHT.sub("", m.group(2))).strip()
                if not FOOTER(t):
                    acts.append((last, t))
            elif last:
                t = re.sub(r"\s+", " ", RIGHT.sub("", l.strip())).strip()
                if len(t) > 4 and not FOOTER(t):
                    acts.append((last + "*", t))     # * = wrapped under the printed step above
        if acts:
            PEMS.append({"page": pno, "title": title, "acts": acts})

STOP = {"cardiac","medical","trauma","general","respiratory","neurologic","toxicology",
        "administrative","front","matter","symptomatic","the","and","of","for","patient","care"}
SYN = {"rosc": "resuscitation", "aemt": "advanced emt", "cpr": "cardiopulmonary resuscitation",
       "ob": "obstruction", "fbfo": "foreign body airway obstruction", "acs": "acute coronary syndrome"}


def specific(t):
    """drop shared category prefixes: 'Cardiac - Symptomatic Bradycardia' -> 'bradycardia'.
    Comparing full titles let 'Cardiac' alone carry the match and produced a false-STRONG pairing
    of the Bradycardia page with Post ROSC Care."""
    return " ".join(SYN.get(x, x) for x in nz(t).split() if x not in STOP)


def match_pems(title):
    t = specific(title)
    scored = []
    for p in PEMS:
        pt = specific(p["title"])
        if not pt or not t:
            continue
        ratio = difflib.SequenceMatcher(None, t, pt).ratio()
        a, b = set(t.split()), set(pt.split())
        bonus = 0.45 if (t in pt or pt in t) else 0.30 * len(a & b) / max(len(a | b), 1)
        sc = ratio * 0.7 + bonus
        if ("non traumatic" in t) != ("non traumatic" in pt):
            sc -= 1.2                              # 'Non-Traumatic' must not be pulled to 'Traumatic'
        if "neonatal" in pt and "neonatal" not in t:
            sc -= 0.8
        if "pediatric" in pt and "pediatric" not in t:
            sc -= 0.4
        scored.append((max(sc, -1.0), p))
    scored.sort(key=lambda x: -x[0])
    top3 = [(q["page"], q["title"], round(min(v, 1.0), 2)) for v, q in scored[:3] if v > 0.1]
    if not scored or scored[0][0] <= 0.1:
        return None, "none", 0.0, top3
    bs, best = scored[0][0], scored[0][1]
    return best, ("strong" if bs >= 0.85 else ("probable" if bs >= 0.55 else "weak")), round(min(bs, 1.0), 2), top3


# Hand-verified structural notes — NOT matcher output. Each was confirmed by reading both the site
# page and the regional pages, because a reviewer following a guessed merge note would rule against
# the wrong source.
FILE_NOTES = {
 "protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.md":
   "This page is a deliberate MERGE: the regional set carries Asystole/PEA on p.57 and V-Fib/pVT on "
   "p.63 as two protocols; your page runs one arrest algorithm covering both (rows 5 and 9 are the "
   "VF/pVT half, row 10 the asystole/PEA half). Level evidence must come from BOTH pages, row by row.",
 "protocols/cardiac/04_Supraventricular_Tachycardia_PROC.md":
   "Rows 3 and 11 ('STABLE SVT PATHWAY' / 'UNSTABLE SVT PATHWAY') are section headings that were put "
   "into the table as rows. They need no level — they need to stop being rows.",
 "protocols/respiratory/03_Respiratory_Arrest_PROC.md":
   "Check the regional Airway Management and Ventilatory Support procedure (p.239) and the arrest "
   "pages: this site page overlaps both, which is why the title matcher found no single source.",
}

ORDER = ["no_level", "run_stops_before_P", "mc_only_partial", "mc_mixed_in", "non_contiguous"]
LABEL = {
    "no_level": "no level cell filled — a provider cannot tell who may do this",
    "run_stops_before_P": "grant stops before Paramedic — the ladder reads inverted",
    "mc_only_partial": "MC in some levels, standing in none",
    "mc_mixed_in": "standing bullets with an MC cell in the same row",
    "non_contiguous": "non-contiguous grant — not drawable as a number line",
}


def classify(raw):
    marks = [bool(x) and ("MC" not in x.upper()) for x in raw]
    mcs = [("MC" in x.upper()) for x in raw]
    pos = [i for i, v in enumerate(marks) if v]
    if not pos and not any(mcs):
        return "no_level"
    if all(mcs) and not pos:
        return None                                # MC at every level: converts as-is
    if not pos:
        return "mc_only_partial"
    if pos == list(range(pos[0], 5)):
        return "mc_mixed_in" if any(mcs) else None
    if pos == list(range(pos[0], pos[-1] + 1)):
        return "run_stops_before_P"
    return "non_contiguous"


def all_row_keys():
    """EVERY (file,row) present in any protocol level table — not only the ones needing a ruling.
    A ruled row stops being an exception once its bracket is written, so matching prior rulings
    against 'rows still needing a ruling' would mark every applied ruling as orphaned."""
    keys = set()
    for f in sorted(glob.glob(DOCS + "/protocols/**/*.md", recursive=True)):
        lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
        hdr = next((i for i, l in enumerate(lines)
                    if re.search(r"\|\s*EMR\s*\|\s*EMT\s*\|\s*A\s*\|\s*I\s*\|\s*P\s*\|", l)), None)
        if hdr is None:
            continue
        n = len(cells(lines[hdr]))
        rel = f.replace(DOCS + "/", "")
        for l in lines[hdr + 2:]:
            s2 = l.strip()
            if not s2.startswith("|"):
                if s2:
                    break
                continue
            c = cells(s2)
            if len(c) == n and len(c) >= 7:
                keys.add((rel, c[0]))
    return keys


def build_rows():
    site = collections.defaultdict(lambda: {"rows": [], "title": ""})
    for f in sorted(glob.glob(DOCS + "/protocols/**/*.md", recursive=True)):
        lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
        hdr = next((i for i, l in enumerate(lines)
                    if re.search(r"\|\s*EMR\s*\|\s*EMT\s*\|\s*A\s*\|\s*I\s*\|\s*P\s*\|", l)), None)
        if hdr is None:
            continue
        n = len(cells(lines[hdr]))
        rel = f.replace(DOCS + "/", "")
        site[rel]["title"] = next((re.sub(r"^##\s*(General\s*-\s*)?", "", l).strip()
                                   for l in lines[:hdr] if l.startswith("## ")), os.path.basename(f))
        for l in lines[hdr + 2:]:
            s = l.strip()
            if not s.startswith("|"):
                if s:
                    break
                continue
            c = cells(s)
            if len(c) != n or len(c) < 7:
                continue
            kind = classify(c[2:7])
            if kind:
                site[rel]["rows"].append({"row": c[0], "kind": kind, "action": clean(c[1]), "cells": c[2:7]})
    return site


# ------------------------------- merge support -------------------------------
ITEM_RE = re.compile(r"^- \[([ xX])\] \*\*row (\S+?)\*\* — `(\w+)`")
FILE_RE = re.compile(r"^## (protocols/[^\n]+)$")


def load_existing(path):
    """pull tick state / rulings / edited fields out of an existing packet: key = (file, row)"""
    try:
        t = open(path, encoding="utf-8").read()
    except (FileNotFoundError, TypeError):
        return {}, []
    out, log, cur, block = {}, [], None, None
    for line in t.split("\n"):
        m = FILE_RE.match(line)
        if m:
            cur, block = m.group(1), None
            continue
        m = ITEM_RE.match(line)
        if m and cur:
            block = (cur, m.group(2))
            d = out.setdefault(block, {"tick": False, "ruled": None, "level": None, "mode": None})
            if m.group(1).lower() == "x":
                d["tick"] = True
            # rulings get written INLINE on the tick line as often as on their own RULED: line
            # ("- [x] **row 5** — `kind` — **VOID by ... ruling** (reason)"). Harvest that text too,
            # otherwise a merge silently drops every ruling made in the compact form.
            tail = line[m.end():].strip(" —-")
            tail = re.sub(r"^`[^`]*`\s*[—-]*\s*", "", tail).strip()
            if tail and tail.strip(" _*-"):
                d["ruled"] = tail
                log.append((block, tail))
            continue
        if not block:
            continue
        if line.startswith(RULED_PREFIX):
            txt = line.strip()[len(RULED_PREFIX):].strip()
            out[block]["ruled"] = txt
            out[block]["tick"] = True
            log.append((block, txt))
        elif re.match(r"^\s+- level:", line):
            v = re.search(r"level:\s*`([^`]*)`", line)
            if v and v.group(1).strip(" _"):
                out[block]["level"] = v.group(1).strip()
        elif re.match(r"^\s+- standing/MC", line):
            v = re.search(r"standing/MC:\s*`([^`]*)`", line)
            if v and v.group(1).strip(" _"):
                out[block]["mode"] = v.group(1).strip()
    return out, log


def main():
    args = sys.argv[1:]
    site = build_rows()
    tot = sum(len(v["rows"]) for v in site.values())
    rest = [a for a in args if not a.startswith("--")]
    if "--fresh" in args:
        out_path = args[args.index("--fresh") + 1]
        merge_src = None
    else:
        # --merge <existing> <out>  |  <out>  (out is also read first if it exists)
        if "--merge" in args:
            i = args.index("--merge")
            merge_src, out_path = args[i + 1], args[i + 2]
        else:
            out_path = rest[0] if rest else "level-review.md"
            merge_src = rest[1] if len(rest) > 1 else (out_path if os.path.exists(out_path) else None)

    prior, prior_log = load_existing(merge_src)
    out = []
    A = out.append
    kc = collections.Counter(r["kind"] for v in site.values() for r in v["rows"])
    all_keys = all_row_keys()
    ruled_now = [k for k in prior if k in all_keys]

    A("---\ntitle: Protocol provider-level review packet\ntags: [ems, protocols, review, provider-level]\n"
      "type: review-checklist\ncreated: 2026-11-11\nregenerated: rulings merged, nothing discarded\n"
      "upstream: PEMS2024.pdf (regional set, effective 05/01/2024)\n"
      "scope: analysis + rulings; the site changes only after a ruling is applied\n---\n\n")
    A("# Provider-level review packet\n\n")
    A("## Level semantics — how every ruling here is written\n\n")
    A("Owner ruling 2026-11-13, applying to the whole packet:\n\n")
    A("| notation | meaning |\n|---|---|\n")
    A("| a level row (e.g. `A`) | that level **and every level above it** may perform the step as a "
      "standing order |\n")
    A("| bracketed entry level `[A]` | the `A` **must contact Medical Control for permission**; I and "
      "P above them do not need to call |\n")
    A("| `MC` in every cell | **every** level must contact Medical Control before acting |\n")
    A("| administrative protocol rows | not level-gated at all (owner ruling 2026-11-11) |\n\n")
    A("> So an `mc_only_partial` row like `· · MC MC MC` is almost always **`[A]` written without its "
      "bracket**: A calls, I and P stand. Confirm that and the row is done.\n\n")

    A("## Rulings log\n\n")
    A("The audit trail the OMD packet needs: a ticked box without a line here is not a ruling.\n\n")
    if prior_log:
        A("| file | row | ruling |\n|---|---|---|\n")
        for (f, r), d in prior_log:
            A(f"| `{f.replace('protocols/','')}` | {r} | {d} |\n")
    else:
        A("_No rulings recorded yet._\n")
    A("\n")

    A("| kind | rows | meaning |\n|---|---|---|\n")
    for k in ORDER:
        if kc[k]:
            A(f"| {k} | {kc[k]} | {LABEL[k]} |\n")
    A(f"\n**531 rows audited across {len(site)} protocol pages; {tot} need a ruling — "
      f"{len(ruled_now)} already ruled.** The other {531-tot} convert mechanically and are not listed.\n\n")
    A("> `*` beside a level in the reference lists means the line is wrapped under the printed step "
      "above it in the PDF — it carries that step's level, not its own.\n\n")
    A("> **The title matcher is a hint, not an authority.** It paired Bradycardia with the wrong page "
      "twice before it was stopped from naming pages it was unsure of. Where it is not confident the "
      "section says `no reliable counterpart` — use the 44-page index.\n\n")
    A("\n## The regional set, all 44 protocol pages\n\n")
    for _p in sorted(PEMS, key=lambda x: x["page"]):
        A(f"- p.{_p['page']} — {_p['title']} ({len(_p['acts'])} coded steps)\n")
    A("\n")

    for rel in sorted(site):
        v = site[rel]
        if not v["rows"]:
            continue
        p, conf, sc, top3 = match_pems(v["title"])
        A(f"\n## {rel}\n\nSite page title: **{v['title']}** · rows needing a ruling: **{len(v['rows'])}**\n\n")
        if rel in FILE_NOTES:
            A(f"> **Structural note (hand-checked, not matcher output):** {FILE_NOTES[rel]}\n\n")
        for r in sorted(v["rows"], key=lambda x: (x["kind"], x["row"])):
            d = prior.get((rel, r["row"]), {})
            box = "x" if d.get("tick") else " "
            cs = " | ".join((c if c else "·") for c in r["cells"])
            A(f"- [{box}] **row {r['row']}** — `{r['kind']}`\n")
            A(f"  - {r['action'][:300]}\n")
            A(f"  - current `EMR|EMT|A|I|P`: `{cs}`\n")
            A(f"  - level: `{d.get('level') or '______'}`  standing/MC: `{d.get('mode') or '______'}`  "
              f"if local, source: `______`\n")
            if d.get("ruled"):
                A(f"{RULED_PREFIX} {d['ruled']}\n")
        if p and conf in ("strong", "probable"):
            A(f"\n> **Regional reference — p.{p['page']}: {p['title']}** — title match {conf} (score {sc})\n>\n")
            for tok, txt in p["acts"]:
                if txt.strip() in (tok, tok.strip("[]"), ""):
                    continue
                A(f"> - `{tok}` {txt[:190]}\n")
        else:
            A("\n> **No reliable regional counterpart identified by title.** Check the 44-page index "
              "above; if none of them is this protocol, the rows below are local material (ACLS / PALS "
              "/ CPR or Poquoson practice) and no upstream level exists to copy.\n")
        alt = [(pg, ti, vv) for pg, ti, vv in top3[1:] if conf in ("strong", "probable")]
        if alt:
            A("\n> Also considered:\n")
            for pg, ti, vv in alt:
                A(f"> - p.{pg} *{ti}* (score {vv})\n")

    orphan = [(k, d) for k, d in prior.items() if k not in all_keys]
    if orphan:
        A("\n---\n\n## Carried rulings with NO matching row\n\n")
        A("These were in the previous packet but their row no longer exists in this build "
          "(renumbered or deleted). Nothing was discarded — reconcile each by hand:\n\n")
        for (f, r), d in sorted(orphan):
            A(f"- `{f}` row {r}: {d.get('ruled') or '(ticked, no ruling text)'}\n")

    A("\n---\n\n## Applying a ruling to the site\n\n"
      "A ruling here changes nothing on the site by itself. Ruled rows are written into a page's "
      "markdown only from an explicit ruling, and then the escape-aware table audit, the build, the "
      "link sweep and a rendered-DOM spot check must all pass before it ships.\n")

    open(out_path, "w", encoding="utf-8").write("".join(out))
    print(f"kinds: {dict(kc)} | rows needing a ruling: {tot}")
    print(f"prior rulings merged: {len(prior)} ({len(prior_log)} with text) | orphaned: {len(orphan)}")
    print(f"mode: {'FRESH — prior rulings NOT read' if not merge_src else 'MERGE from ' + str(merge_src)}")
    print(f"wrote {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    main()
