#!/usr/bin/env python3
"""gen_connected_notes.py — auto-generate the EO 6.00 "Connected Notes" box.

Gold pattern (owner ruling 2026-11-09), per SOP page:

    !!! info "SOP Header"           <- boxed metadata (converted from .sop-meta div)
        <meta line, indented>
    <!-- CONNECTED:START -->
    !!! abstract "Connected Notes"
        - **Referenced SOPs:** [Title](../path.html) | ...
    <!-- CONNECTED:END -->

THE SCRIPT PICKS THE LINKS. Sources, in order:

  1. same-family sibling   — EO 6.00a ↔ EO 6.00 (same dir, same digits, letter suffix)
  2. body SOP citations    — "EO 13.00", "GA 7.00". Identity comes ONLY from the
                             filename code (prefix+digits); a citation is accepted
                             when its digits resolve to exactly one file, so dump
                             noise ("EO 13.0", "EO 13") can pad to 1300 but a
                             collision is REPORTED, never guessed.
  3. EMS content mentions  — on EMS-side pages, named procedures / protocols / drug
                             pages link when their nav label appears in the body
  4. hub link              — Fire/EMS resources hub anchored on the page's group

Labels come from mkdocs.yml nav, not from the page H1 — the ported PDFs all begin
with "Poquoson Fire and Rescue Patient Care Protocols", which is not a title.

Usage:
  python scripts/gen_connected_notes.py                    # dry run + JSON report
  python scripts/gen_connected_notes.py --limit 10 --apply # phased rollout
  python scripts/gen_connected_notes.py --headers          # also box the meta div
  python scripts/gen_connected_notes.py --check            # exit 1 if drift
"""
from __future__ import annotations

import argparse
import collections
import json
import posixpath
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SOPS = DOCS / "sops"

sys.path.insert(0, str(ROOT / "scripts"))
from gen_resource_pages import (flatten, load_cfg, bucket_of, group_name, slugify)

START = "<!-- CONNECTED:START (auto — scripts/gen_connected_notes.py; do not hand-edit) -->"
END = "<!-- CONNECTED:END -->"
HDR_RE = re.compile(r'^!!! info "SOP Header"[ \t]*$', re.M)
OLD_BOX = re.compile(r'^!!! abstract "Connected Notes"[ \t]*\n(?:[ \t]{4}.*\n|\n)*', re.M)
MARKED = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
META_DIV = re.compile(r'^<div class="sop-meta">(.*?)</div>[ \t]*$', re.M)
CODE_FN = re.compile(r"^([A-Z]{2,3})[-_ ]?(\d+)([a-z]?)", re.I)
CITE_RE = re.compile(r"\b(EO|EMS|GA|EA|EQ|SH|PR|SO)[ \t]+(\d+(?:\.\d+)?)([a-z]?)\b")
PREFIX_FIX = {"EQ": "EA"}

# generic phrases that must never become a "linked content" label
STOP_LABELS = {"poquoson", "patient care protocol", "protocol tracker", "overview",
               "introduction", "full text archive", "policy manual", "medications"}
MIN_LABEL = 7


def rel(from_dir, target):
    return posixpath.relpath("docs/" + target, "docs/" + from_dir)


def nav_labels(records):
    """path -> label, plus (path -> group) from the menu."""
    lab, grp = {}, {}
    for r in records:
        if r["file"]:
            lab.setdefault(r["file"], r["label"])
            grp.setdefault(r["file"], group_name(r, bucket_of(r)))
    return lab, grp


# --------------------------------------------------------------------- identity
def code_index():
    """Two maps, built ONLY from filenames (their digits are the authority):
       exact: prefix+digits+suffix -> path   (EO-600a)
       base : prefix+digits        -> path   (EO-600 — suffixed files excluded,
                                              so a plain "EO 6.00" citation can
                                              never collide with its study aid)"""
    exact, base = collections.defaultdict(set), collections.defaultdict(set)
    for p in DOCS.rglob("*.md"):
        r = str(p.relative_to(DOCS)).replace("\\", "/")
        m = CODE_FN.match(p.stem)
        if not m:
            continue
        pre = PREFIX_FIX.get(m.group(1).upper(), m.group(1).upper())
        digits, suf = m.group(2), m.group(3)
        exact[pre + digits + suf].add(r)
        if not suf:
            base[pre + digits].add(r)
    return exact, base


def cite_targets(exact, base, prefix, num, suffix):
    """Resolve one body citation to exactly one page — or to nothing.

    Dump noise gives several spellings for the same SOP ("EO 13.00", "EO 13.0",
    "EO 13"). Candidates are the digit string plus its zero-padded forms; a hit
    set larger than one page is AMBIGUOUS and refused, never guessed.
    """
    pre = PREFIX_FIX.get(prefix.upper(), prefix.upper())
    digits = num.replace(".", "")
    table = exact if suffix else base
    key = pre + digits + (suffix or "")
    cands = {key}
    if table is base:
        if not digits.endswith("00"):
            cands.add(pre + digits + "0")
            cands.add(pre + digits + "00")
        elif len(digits) > 1:
            cands.add(pre + digits[:-1])           # "110" <- "11.0"
    hits = set()
    for k in cands:
        hits |= table.get(k, set())
    return hits if len(hits) == 1 else set()


def siblings_of(path):
    m = CODE_FN.match(path.stem)
    if not m:
        return []
    out = []
    for p in sorted(path.parent.glob("*.md")):
        if p == path or "index" in p.stem.lower():
            continue
        m2 = CODE_FN.match(p.stem)
        if m2 and m2.group(1).upper() == m.group(1).upper() and m2.group(2) == m.group(2):
            out.append(str(p.relative_to(DOCS)).replace("\\", "/"))
    return out


# ------------------------------------------------------------------ link picker
def collect(r, path, exact, base, labels, groups, ems_targets):
    """Emit the Connected Notes groups. `seen` is shared across all sources so one
    page never appears twice in the box (title mentions duplicate the sibling link)."""
    d = posixpath.dirname(r)
    text = path.read_text()
    body = MARKED.sub("", OLD_BOX.sub("", text))
    keep = []
    for l in body.split("\n"):
        s = l.lstrip()
        if s.startswith("|") or s.startswith("# ") or s.startswith('.sop-meta') \
           or l.startswith("<div class=\"sop-meta\">") or l.startswith("!!! info \"SOP Header\""):
            continue                      # titles/headers talk ABOUT this page, not to others
        keep.append(l)
    body = "\n".join(keep)
    out, seen = [], {r}

    def add(heading, items):
        items = [(l, t) for l, t in items if t.split("#")[0] not in seen]
        seen.update(t.split("#")[0] for _l, t in items)
        if items:
            out.append((heading, items))
        return items

    add("Same SOP family", [(labels.get(s, Path(s).stem), rel(d, s)) for s in siblings_of(path)])

    refs = []
    for pre, num, suf in CITE_RE.findall(body):
        t = cite_targets(exact, base, pre, num, suf)
        if not t:
            continue
        target = next(iter(t))
        if target in seen or bucket_of({"file": target}) not in ("FIRE", "EMS"):
            continue
        refs.append((labels.get(target, Path(target).stem), rel(d, target)))
        seen.add(target)                       # a repeated citation links once
    add("Referenced SOPs", refs[:6])

    add("Named on this page", [
        (lab, rel(d, tgt)) for lab, tgt in ems_targets
        if tgt != r and re.search(r"(?<![\w/])" + re.escape(lab.lower()) + r"(?![\w])", body.lower())
    ][:5])

    if not out:
        # no real connection found -> emit NO box. An empty "Connected Notes" box
        # on 72 pages reads as broken, and the hub is already in the menu.
        return []

    b = bucket_of({"file": r})
    if b in ("FIRE", "EMS"):
        hub = "resources/fire.md" if b == "FIRE" else "resources/ems.md"
        g = groups.get(r)
        add("Browse the rest of this side",
            [(labels.get(hub, "Resources") + (f" · {g}" if g else ""),
              rel(d, hub) + (f"#{slugify(g)}" if g else ""))])
    return out


def render(groups):
    """Flush-left: a 4-space indent at top level would render as a code block."""
    if not groups:
        return ""
    lines = [START, '!!! abstract "Connected Notes"']
    for heading, items in groups:
        if items:
            rendered = " &nbsp;|&nbsp; ".join(f"[{l}]({t})" for l, t in items)
            lines.append(f'    - **{heading}:** {rendered}')
    lines.append(END)
    return "\n".join(lines) + "\n"


def box_header(text):
    """convert the first .sop-meta div into the boxed `!!! info "SOP Header"`, and
    indent a metadata line that was left outside an existing box (EO 6.00 shipped
    that bug: an unindented line is not admonition content, so the box rendered empty)."""
    if HDR_RE.search(text):
        # (?![ \t]{4}) — NOT \s: \s would match the newline itself and "succeed"
        return re.sub(r'(!!! info "SOP Header"\n)(?![ \t]{4})', r"\1    ", text, count=1)
    def _sub(m):
        inner = m.group(1)
        # keep the bold labels: <strong>Category:</strong> -> **Category:**
        inner = re.sub(r"<strong>(.*?)</strong>", r"**\1**", inner)
        inner = re.sub(r"<[^>]+>", "", inner).replace("&nbsp;·&nbsp;", " · ").strip()
        # PDF-dump underscore junk clings to the code: "**SOP** _ EMS 15.0 _"
        inner = re.sub(r"\s*_\s+(?=\S)", " ", inner)
        inner = re.sub(r"\s+_\s*$", "", inner)
        inner = re.sub(r"\s{2,}·\s{2,}", "  ·  ", inner)
        return '!!! info "SOP Header"\n    ' + inner
    return META_DIV.sub(_sub, text, count=1)


def place_block(text, block):
    """Replace the marked block in place; otherwise insert it after the H1 +
    header card and before the first rule/section heading."""
    if not block.strip():
        # nothing connected: drop a stale auto-box, keep any hand-written one
        return MARKED.sub("", text).replace("\n\n\n", "\n\n") if MARKED.search(text) else text
    if MARKED.search(text):
        return MARKED.sub(lambda _m: block.rstrip("\n"), text, count=1)
    if OLD_BOX.search(text):
        # the match ate the blank line after the box; put it back
        return OLD_BOX.sub(lambda _m: block.rstrip("\n") + "\n\n", text, count=1)
    lines = text.split("\n")
    anchor = 0
    for i, l in enumerate(lines):
        if HDR_RE.match(l) or l.startswith('<div class="sop-meta">'):
            anchor = i
            break
    # header admonition owns its indented continuation lines
    j = anchor + 1
    if HDR_RE.match(lines[anchor]):
        while j < len(lines) and (lines[j].startswith("    ") or not lines[j].strip()):
            if not lines[j].strip() and (j + 1 >= len(lines) or lines[j + 1].startswith("    ")):
                j += 1
            else:
                break
    while j < len(lines) and not lines[j].startswith(("---", "## ", "<!--")):
        j += 1
    lines.insert(j, block.rstrip("\n") + "\n")
    return "\n".join(lines)


def porter_owned():
    """Pages GENERATED by port_reference.py from vault notes. Writing a box into them
    would be silently erased on the next re-port, so the script leaves them alone."""
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        import port_reference
        return set(getattr(port_reference, "SITE_MAP", {}).values())
    except Exception as e:
        print(f"  warning: cannot read SITE_MAP ({e}) — treating no page as porter-owned")
        return set()


# ------------------------------------------------------------------ shared setup
def build_context():
    records = flatten(load_cfg()["nav"])
    labels, groups = nav_labels(records)
    labels["resources/fire.md"] = "Fire Resources"
    labels["resources/ems.md"] = "EMS Resources"
    exact, base = code_index()

    # "named on this page" targets: any real page whose MENU label is distinctive
    # enough to survive being found in prose. Two guards: multi-word labels only
    # (single words allowed just for drug/procedure names like "Ketamine" or
    # "Capnography"), and never a group name — "Emergency Operations" appears in
    # ordinary sentences and is not a link.
    group_names = {g.lower() for g in groups.values() if g}
    named = []
    for r in sorted(labels):
        if bucket_of({"file": r}) not in ("FIRE", "EMS"):
            continue
        key = re.split(r"\s*/\s*", labels[r].strip())[0].strip()
        low = key.lower()
        if len(key) < MIN_LABEL or low in STOP_LABELS or any(s in low for s in STOP_LABELS):
            continue
        if low in group_names:
            continue
        if " " not in key and not r.startswith(("pharmacology/", "procedures/")):
            continue
        named.append((key, r))
    named.sort(key=lambda x: -len(x[0]))
    return {"labels": labels, "groups": groups, "exact": exact, "base": base,
            "named": named}


def rewrite_page(r, ctx, headers=False):
    """Return the page text with box + Connected Notes applied (no write)."""
    path = DOCS / r
    text = path.read_text()
    got = collect(r, path, ctx["exact"], ctx["base"], ctx["labels"], ctx["groups"], ctx["named"])
    src = box_header(text) if headers else text
    return place_block(src, render(got)), got


def apply_to_page(r, headers=True):
    """Hook for port_reference.py: porter pages get the same auto-box at port time,
    so a re-port cannot silently delete what the sweep wrote."""
    new, got = rewrite_page(r, build_context(), headers=headers)
    if new != (DOCS / r).read_text():
        (DOCS / r).write_text(new)
    return sum(len(i) for _, i in got)


# ------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--headers", action="store_true",
                    help="also convert the .sop-meta div into the boxed SOP Header")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="", help="substring filter on page path")
    ap.add_argument("--allow-ported", action="store_true",
                    help="also touch pages the porter regenerates (default: skip — "
                         "port_reference.py calls apply_to_page instead)")
    ap.add_argument("--report", default=str(Path.home() / ".hermes/cache/scratch/connected_notes_report.json"))
    a = ap.parse_args()

    ctx = build_context()
    pages = [str(a2.relative_to(DOCS)).replace("\\", "/")
             for a2 in sorted(SOPS.rglob("*.md")) if "index" not in a2.stem.lower()]
    owned = porter_owned()
    ported_in_scope = [p for p in pages if p in owned]
    if not a.allow_ported:
        pages = [p for p in pages if p not in owned]
    if a.only:
        pages = [p for p in pages if a.only in p]
    if a.limit:
        pages = pages[:a.limit]

    stats = collections.Counter()
    detail, changes, examples = [], {}, []
    for r in pages:
        text = (DOCS / r).read_text()
        new, got = rewrite_page(r, ctx, headers=a.headers)
        n = sum(len(i) for _, i in got)
        stats["pages"] += 1
        stats["links"] += n
        stats["boxed"] += (n > 0)
        stats["changed"] += (new != text)
        detail.append({"page": r, "links": n,
                       "groups": {h: [l for l, _ in i] for h, i in got},
                       "changed": new != text})
        if new != text:
            changes[r] = new
        if 3 <= n <= 6 and len(examples) < 6:
            examples.append((r, new[:1500]))

    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(json.dumps({"stats": dict(stats),
                                          "skipped_porter_owned": ported_in_scope,
                                          "pages": detail}, indent=1))
    if a.apply:
        for r, new in changes.items():
            (DOCS / r).write_text(new)

    print(f"[{'APPLIED' if a.apply else 'DRY RUN'}] pages={stats['pages']} "
          f"with-box={stats['boxed']} links={stats['links']} changed={stats['changed']} "
          f"skipped(porter-owned)={len(ported_in_scope) if not a.allow_ported else 0}")
    print(f"report: {a.report}")
    for r, sample in examples[:2]:
        print(f"\n########## {r}\n{sample}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
