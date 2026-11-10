#!/usr/bin/env python3
"""gen_resource_pages.py — mkdocs.yml nav is the single source of truth.

Reads the nav tree, classifies every page into FIRE / EMS / DEPT, then writes
(idempotently, only when content differs):

  docs/resources/fire.md   fire hub — every fire page, grouped
  docs/resources/ems.md    ems hub  — every EMS page, procedures included
  docs/index.md            QUICKLINKS block: name + link only, phone-compact
  mkdocs.yml               nav block: Home / Fire Resources / EMS Resources /
                           Personnel Policies

Safety: every page path in the OLD nav must survive into the NEW nav and into
exactly one hub. Anything dropped, duplicated, or unclassified aborts the run.

Usage:  python scripts/gen_resource_pages.py [--check | --dry]
"""
from __future__ import annotations

import posixpath
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONFIG = ROOT / "mkdocs.yml"

HOME_PAGE = "index.md"
FIRE_HUB = "resources/fire.md"
EMS_HUB = "resources/ems.md"

QL_START = "<!-- QUICKLINKS:START (generated — scripts/gen_resource_pages.py; do not hand-edit) -->"
QL_END = "<!-- QUICKLINKS:END -->"

# group label renames: the old menu nested things under section names that stop
# making sense once fire and EMS are split onto their own pages.
GROUP_RENAME = {
    ("EMS", "EMS"): "EMS SOPs",                    # was buried under "Fire SOPs"
    ("Fire & EMS References", "FIRE"): "Field References",
}

# display order inside each hub AND in the homepage jump strips — highest-traffic
# first (owner ruling 2026-11-10: "the more important things need to be a higher
# hierarchy to the left"). Reorder here and both hubs + strips follow.
FIRE_ORDER = ["Emergency Operations", "Field References", "Strategies", "Frameworks",
              "Special Operations", "Equipment & Apparatus", "Safety & Health",
              "General Administration", "Public Relations"]
EMS_ORDER = ["Cardiac", "Respiratory", "Trauma", "Medical", "Administrative",
             "Procedures", "Toxicology", "Neurologic", "General", "Pharmacology",
             "Medications & Calculators", "Pediatric Dosing Reference",
             "EMS SOPs", "Front Matter"]

# Static one-tap tools on the homepage: no scrolling, no menu. Labels are ours
# (the source pages carry truncated PDF-dump titles). Every path is validated
# against the live nav, so a renamed page breaks the build instead of shipping
# a dead tile.
SCENE_TOOLS = [
    ("Pediatric Dosing Calculator", "pediatric-dosing/calculator.md"),
    ("Pediatric Dosing Tables", "pediatric-dosing/dosing-tables.md"),
    ("Drugs & Calculators", "medications.md"),
    ("Skills Procedures", "resources/ems.md#procedures"),
    ("Alarm Assignments", "fire-ems-references/initial-alarm-company-assignments.md"),
    ("First to Arrive (EO 6.00)", "sops/emergency-operations/EO-600-First-to-Arrive-Duties.md"),
]

# Personnel policies are not in the nav (only the index page is), so the strip
# names the high-traffic ones explicitly and each is checked against disk.
POLICY_CHIPS = [
    ("Hazardous Weather", "personnel-policies/policies/26-hazardous-weather.md"),
    ("Overtime / Comp Time", "personnel-policies/policies/13-overtime-compensatory-time.md"),
    ("Work Schedules", "personnel-policies/policies/09-work-schedules-and-attendance.md"),
    ("Annual Leave", "personnel-policies/policies/15-annual-leave-vrs-plan-1-plan-2-and.md"),
    ("Sick Leave", "personnel-policies/policies/23-sick-leave-vrs-plan-1-plan-2-and.md"),
    ("Family & Medical Leave", "personnel-policies/policies/18-family-and-medical-leave.md"),
    ("Uniforms", "personnel-policies/policies/36-uniforms-protective-clothing-and-effective-date.md"),
    ("Workers' Comp", "personnel-policies/policies/24-workers-compensation-and-light-duty.md"),
    ("Conduct & Discipline", "personnel-policies/policies/39-employee-conduct-progressive-discipline.md"),
    ("Grievance Procedure", "personnel-policies/policies/41-grievance-procedure.md"),
    ("Hiring & Promotion", "personnel-policies/policies/07-recruitment-hiring-promotion.md"),
    ("Vehicles & Driving", "personnel-policies/policies/29-vehicle-usage-and-driving-policy.md"),
    ("Full Policy Manual", "personnel-policies/index.md"),
    ("Full Text Archive", "personnel-policies/other/personnel-policy-manual.md"),
]


# ------------------------------------------------------------------ nav reading
def load_cfg():
    return yaml.safe_load(CONFIG.read_text())


# Classification is PATH-based, not menu-label-based, so the script stays
# idempotent after it has rewritten the nav into Fire/EMS hubs.
EMS_PATHS = ("protocols/", "procedures/", "pharmacology/", "medications.md",
             "pediatric-dosing/", "sops/ems/")
FIRE_PATHS = ("fire-ems-references/", "sops/")


def flatten(nav, parents=(), top=None, out=None):
    """nav tree -> flat records (label, file, parents, top), in menu order."""
    if out is None:
        out = []
    for item in nav or []:
        if isinstance(item, str):
            out.append({"label": item, "file": item, "parents": parents, "top": top or item})
            continue
        if not isinstance(item, dict):
            raise SystemExit(f"unexpected nav entry: {item!r}")
        for label, val in item.items():
            newtop = label if top is None else top
            if isinstance(val, str):
                out.append({"label": label, "file": val, "parents": parents, "top": newtop})
            else:
                flatten(val, parents + (label,), newtop, out)
    return out


# ------------------------------------------------------------- classification
def bucket_of(rec):
    path = rec["file"] or ""
    if path == HOME_PAGE:
        return "HOME"
    if path in (FIRE_HUB, EMS_HUB):
        return "HUB"
    if path.startswith("personnel-policies/"):
        return "DEPT"
    if path.startswith(EMS_PATHS):
        return "EMS"
    if path.startswith(FIRE_PATHS):
        return "FIRE"
    raise SystemExit(f"UNCLASSIFIED page {path!r} (nav top {rec['top']!r}) — add a rule")


def group_of(rec):
    """deepest nav parent = the group the page sits in; flat sections use top."""
    return rec["parents"][-1] if rec["parents"] else rec["top"]


def group_name(rec, bucket):
    return GROUP_RENAME.get((group_of(rec), bucket), group_of(rec))


def ordered_groups(recs, bucket, order):
    """[(group, [rec,...])] in `order`, unknown groups appended, recs in menu order."""
    buckets = {}
    for r in recs:
        buckets.setdefault(group_name(r, bucket), []).append(r)
    known = [g for g in order if g in buckets]
    extra = [g for g in buckets if g not in order]
    if extra:
        print(f"  note: groups not in {bucket}_ORDER: {extra}")
    return [(g, buckets[g]) for g in known + extra]


# -------------------------------------------------------------------- hub pages
def slugify(text):
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[\s_-]+", "-", s).strip("-")


HUB_LEAD = {
    "FIRE": ("Everything attached to the **fire side** — tactical references, "
             "emergency operations, equipment and apparatus, special operations, "
             "safety, and department administration. EMS clinical content lives on "
             "the [EMS Resources](ems.md) page."),
    "EMS": ("Everything attached to the **EMS side** — protocols, skills "
            "procedures, medications, pediatric dosing, and EMS administration. "
            "Fire content lives on the [Fire Resources](fire.md) page."),
}


def build_hub(bucket, title, groups):
    chip = "**Jump:** " + " ".join(f"[{g}](#{slugify(g)})" for g, _ in groups)
    lines = [f"# {title}", "", HUB_LEAD[bucket], "",
             '<div class="qljump" markdown="1">', "", chip, "", "</div>", ""]
    for g, recs in groups:
        lines += [f"## {g}", ""]
        for r in recs:
            rel = posixpath.relpath("docs/" + r["file"], "docs/resources")
            lines.append(f"- [{r['label']}]({rel})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ------------------------------------------------------------------- new nav
def build_nav(records):
    def group_nodes(bucket, order):
        nodes = []
        for g, recs in ordered_groups([r for r in records
                                       if bucket_of(r) == bucket and r["file"]], bucket, order):
            nodes.append({g: [{r["label"]: r["file"]} for r in recs]})
        return nodes

    dept = [r for r in records if bucket_of(r) == "DEPT" and r["file"]]
    return [{"Home": HOME_PAGE},
            {"Fire Resources": [{"Fire Resources Home": FIRE_HUB}, *group_nodes("FIRE", FIRE_ORDER)]},
            {"EMS Resources": [{"EMS Resources Home": EMS_HUB}, *group_nodes("EMS", EMS_ORDER)]},
            {"Personnel Policies": [{r["label"]: r["file"]} for r in dept]}]


def nav_paths(nav):
    out = []

    def rec(node):
        for item in node or []:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                for v in item.values():
                    (rec(v) if not isinstance(v, str) else out.append(v))
    rec(nav)
    return out


# --------------------------------------------------------------- homepage block
def quicklinks_block(records):
    """Three pairings: one big door row directly above its own jump strip, plus a
    static tool row that needs no scrolling and no menu (owner ruling 2026-11-10)."""
    fire = ordered_groups([r for r in records if bucket_of(r) == "FIRE" and r["file"]],
                          "FIRE", FIRE_ORDER)
    ems = ordered_groups([r for r in records if bucket_of(r) == "EMS" and r["file"]],
                         "EMS", EMS_ORDER)

    nav_paths = {r["file"] for r in records if r["file"]}
    missing = [p for _l, p in SCENE_TOOLS if p.split("#")[0] not in nav_paths]
    missing += [p for _l, p in POLICY_CHIPS if not (DOCS / p).exists()]
    if missing:
        raise SystemExit(f"curated link target no longer exists: {missing}")

    def chips(groups, hub, label):
        # space-separated: .qljump is a flex row, CSS gap supplies the spacing
        return f"**{label}:** " + " ".join(f"[{g}]({hub}#{slugify(g)})" for g, _ in groups)

    n_fire = sum(len(g[1]) for g in fire)
    n_ems = sum(len(g[1]) for g in ems)

    parts = [QL_START, "",
             '<div class="qlcap" markdown="1">', "", "**On-scene tools — one tap**", "", "</div>",
             "",
             '<div class="qltools" markdown="1">', "",
             " ".join(f"[{l}]({p})" for l, p in SCENE_TOOLS), "", "</div>", ""]

    doors = [("Fire Resources", "resources/fire.md", f"{n_fire} pages",
              chips(fire, "resources/fire.md", "Fire")),
             ("EMS Resources", "resources/ems.md", f"{n_ems} pages · procedures inside",
              chips(ems, "resources/ems.md", "EMS")),
             ("Personnel Policies", "personnel-policies/index.md", "43 indexed",
              "**Policies:** " + " ".join(f"[{l}]({p})" for l, p in POLICY_CHIPS))]

    for title, href, sub, strip in doors:
        parts += ['<div class="qlone" markdown="1">', "",
                  f'**[{title}]({href})** <span class="qlcount">{sub}</span>', "", "</div>", "",
                  '<div class="qljump" markdown="1">', "", strip, "", "</div>", ""]
    parts += [QL_END]
    return "\n".join(parts)


def splice_index(text, block):
    pat = re.compile(re.escape(QL_START) + r".*?" + re.escape(QL_END), re.S)
    if not pat.search(text):
        raise SystemExit("index.md lost its QUICKLINKS sentinels — refusing to guess where to insert")
    return pat.sub(lambda _m: block, text)


def splice_nav(cfg_text, nav):
    dump = yaml.dump(nav, sort_keys=False, default_flow_style=False,
                     allow_unicode=True, width=1000)
    if not dump.endswith("\n"):
        dump += "\n"
    lines = cfg_text.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("nav:"))
    # the nav block is a sequence whose items start at column 0 ("- Home: index.md"),
    # so only a top-level MAPPING key ends it — never match a bare list item.
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"^\w[\w-]*:", lines[i])),
               len(lines))
    tail = "\n".join(lines[end:])
    return "\n".join(lines[:start]) + "\nnav:\n" + dump + (tail if tail.strip() else "")


# ------------------------------------------------------------------------ main
def main():
    check, dry = "--check" in sys.argv, "--dry" in sys.argv
    cfg = load_cfg()
    records = flatten(cfg["nav"])
    old = [r["file"] for r in records if r["file"] and bucket_of(r) != "HUB"]
    old_set, hub_set = set(old), {FIRE_HUB, EMS_HUB}

    nav = build_nav(records)
    new = nav_paths(nav)
    new_set = set(new) - hub_set
    dropped, invented = old_set - new_set, new_set - old_set
    if dropped or invented:
        raise SystemExit(f"NAV COVERAGE FAILURE dropped={sorted(dropped)} invented={sorted(invented)}")
    dupes = {p for p in new if p not in hub_set and new.count(p) > 1}
    if dupes:
        raise SystemExit(f"NAV COVERAGE FAILURE duplicated={sorted(dupes)}")

    fire_g = ordered_groups([r for r in records if bucket_of(r) == "FIRE" and r["file"]],
                            "FIRE", FIRE_ORDER)
    ems_g = ordered_groups([r for r in records if bucket_of(r) == "EMS" and r["file"]],
                           "EMS", EMS_ORDER)
    placed = [r["file"] for _, gs in (("FIRE", fire_g), ("EMS", ems_g))
              for _g, recs in gs for r in recs]
    non_hub = {r["file"] for r in records if bucket_of(r) in ("HOME", "DEPT")}
    hub_missing = old_set - set(placed) - non_hub
    if hub_missing:
        raise SystemExit(f"HUB COVERAGE FAILURE: {sorted(hub_missing)}")
    if len(placed) != len(set(placed)):
        raise SystemExit("HUB COVERAGE FAILURE: a page is listed twice")

    files = {
        "docs/" + FIRE_HUB: build_hub("FIRE", "Fire Resources", fire_g),
        "docs/" + EMS_HUB: build_hub("EMS", "EMS Resources", ems_g),
        "docs/index.md": splice_index((DOCS / "index.md").read_text(), quicklinks_block(records)),
        "mkdocs.yml": splice_nav(CONFIG.read_text(), nav),
    }

    drift = [rel for rel, text in files.items()
             if not (ROOT / rel).exists() or (ROOT / rel).read_text() != text]
    print(f"pages: {len(old_set)}  fire groups: {len(fire_g)} "
          f"({sum(len(g[1]) for g in fire_g)})  ems groups: {len(ems_g)} "
          f"({sum(len(g[1]) for g in ems_g)})")
    print("drift:", ", ".join(drift) or "none — all files current")
    if dry:
        for rel in drift:
            print(f"\n===== {rel} =====\n{files[rel][:3000]}")
        return 0
    if check:
        return 1 if drift else 0
    for rel in drift:
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(files[rel])
        print(f"wrote {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
