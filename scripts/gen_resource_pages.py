#!/usr/bin/env python3
"""gen_resource_pages.py — mkdocs.yml nav is the single source of truth.

Reads the nav tree, classifies every page into FIRE (SOPs) / FIRE_REF (fire
references) / EMS (protocols) / STATION / DEPT, then writes (idempotently, only
when content differs):

  docs/resources/ems.md             "Protocols" — every EMS page, static category
                                    buttons on top, Front Matter first
  docs/resources/fire.md            "SOPs" — every fire SOP page, grouped
  docs/resources/fire-resources.md  "Fire Resources" — frameworks, field
                                    references, strategies, FORCES study aid
  docs/resources/station.md         "Station Hub"
  docs/ems/index.md                 EMS clinical/learning hub
  docs/station/policies.md          City & personnel policies
  docs/index.md                     QUICKLINKS block: name + link only
  mkdocs.yml                        nav block

Naming is the owner's ruling of 2026-11-20: the protocol index is **Protocols**,
the fire SOP index is **SOPs**, and what is left over (frameworks, field
references, strategies, the FORCES study aid) is **Fire Resources**.

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
FIRE_HUB = "resources/fire.md"           # page title "SOPs" (owner ruling 2026-11-20)
EMS_HUB = "resources/ems.md"             # page title "Protocols"
# What is NOT an SOP on the fire side: frameworks, field references, strategies and
# the FORCES study aid. Owner ruling 2026-11-20, split out of the old fire hub.
FIRE_REF_HUB = "resources/fire-resources.md"
STATION_HUB = "resources/station.md"
LINKS_PAGE = "resources/links.md"
# Clinical landing page behind the homepage scroller (owner card t_e787ab8d): the
# homepage must not be a sitemap, so the protocol categories get their own page with
# the clinical lists on it, while resources/ems.md stays the complete A-Z index.
EMS_CLINICAL_HUB = "ems/index.md"
# City & personnel policies — moved out of the homepage hero and out of the fire
# section onto their own page inside the Station tab.
STATION_POLICIES = "station/policies.md"

QL_START = "<!-- QUICKLINKS:START (generated — scripts/gen_resource_pages.py; do not hand-edit) -->"
QL_END = "<!-- QUICKLINKS:END -->"

# group label renames: the old menu nested things under section names that stop
# making sense once fire and EMS are split onto their own pages.
GROUP_RENAME = {
    ("EMS", "EMS"): "EMS SOPs",                     # was buried under "Fire SOPs"
    ("Fire & EMS References", "FIRE"): "Field References",
    ("Fire & EMS References", "FIRE_REF"): "Field References",
    # A page flat under the top-level EMS section inherits that section's own label,
    # which repeated the page title as a group heading on the hub. Same failure class
    # as "Station Hub inside Station Hub" (owner report 2026-11-11).
    #
    # Outstanding Decisions: the group was called "Orientation" and sat FIRST on the
    # Protocols page. It is an audit page, not a clinical entry point, and the owner
    # ruled it to the bottom (2026-11-20) — so both the label and the position follow.
    ("Orientation", "EMS"): "Outstanding Decisions",
    # FORCES is a study aid, not an SOP. It keeps its nav home (Emergency Operations)
    # but the group is renamed for the Fire Resources page, where it now sits.
    ("Emergency Operations", "FIRE_REF"): "Study Aids",
    # A page placed flat under a section inherits that section's own label as its group,
    # which put "Station Hub" INSIDE "Station Hub" in the drawer (owner report 2026-11-11) and
    # repeated the page title as an H2 on the hub. Give those groups names that describe the
    # content instead of restating the section.
    ("Station Hub", "STATION"): "Orientation",
    ("Crew Links", "STATION"): "Portals & Systems",
}

# Pages that sit FLAT in their nav section (no group of their own). Their group name is
# pinned by path so it survives every nav rewrite: medications.md is a group of one,
# and Outstanding Decisions must keep its own heading instead of inheriting the
# section name "Protocols".
PATH_GROUP = {
    "medications.md": "Medications & Calculators",
    "protocols/outstanding-decisions.md": "Outstanding Decisions",
}

# display order inside each hub AND in the homepage jump strips — highest-traffic
# first (owner ruling 2026-11-10: "the more important things need to be a higher
# hierarchy to the left"). Reorder here and both hubs + strips follow.
#
# FIRE = the SOPs page, so only SOP families are listed here; the reference shelf
# (frameworks / field references / strategies) moved to Fire Resources.
FIRE_ORDER = ["Emergency Operations", "Special Operations", "Equipment & Apparatus",
              "Safety & Health", "General Administration", "Public Relations"]
# Fire Resources order is the owner's own listing order (2026-11-20).
FIRE_REF_ORDER = ["Frameworks", "Field References", "Strategies", "Study Aids"]
# Protocols page, top to bottom (owner ruling 2026-11-20): Front Matter and Quick
# References are orientation material and go first; the audit page goes last.
EMS_ORDER = ["Front Matter", "Quick References", "Cardiac", "Respiratory", "Trauma",
             "Medical", "Administrative", "Procedures", "Toxicology", "Neurologic",
             "General", "Pharmacology", "Medications & Calculators",
             "Pediatric Dosing Reference", "EMS SOPs", "Outstanding Decisions"]
# Owner ruled Procedures ABOVE Pharmacology. Assert it here rather than trusting the
# table above: a future reorder that breaks the ruling must fail the generator.
if EMS_ORDER.index("Procedures") > EMS_ORDER.index("Pharmacology"):
    raise SystemExit("EMS_ORDER: Procedures must stay above Pharmacology (owner ruling)")

# Station groups in display order. These are the RENAMED group labels (see GROUP_RENAME):
# naming the section's own word here would re-render "Station Hub" inside "Station Hub".
# Unknown groups are appended by ordered_groups(), so a new station page never fails the build.
STATION_ORDER = ["Orientation", "Portals & Systems", "Policies & Administration", "Training"]

# ---------------------------------------------------------------- homepage data
# High-acuity, one-tap tools.  (label, target, sublabel, domain, icon)
# The domain drives the accent bar + icon colour AND is spelled out in the sublabel,
# because colour alone is never the only signal (same rule as the pip strip).
SCENE_TOOLS = [
    ("Pediatric Dosing Calculator", "pediatric-dosing/calculator.md",
     "Weight-based dosing", "EMS", "dose"),
    ("Drugs & Drip Rates", "medications.md",
     "Push & infusion rates", "EMS", "drug"),
    ("Skills Procedures", "resources/ems.md#procedures",
     "Step-by-step skills", "EMS", "skills"),
    ("Alarm Assignments", "fire-ems-references/initial-alarm-company-assignments.md",
     "Who rides what", "FIRE", "alarm"),
    ("First to Arrive (EO 6.00)", "sops/emergency-operations/EO-600-First-to-Arrive-Duties.md",
     "Initial company roles", "FIRE", "arrive"),
]

# The four homepage scrollers (owner card t_a650f9ea: "first button is the section,
# then real destinations"). Each strip leads with the hub it belongs to, so the first
# tap is never a surprise, and every chip after it carries its own URL.
EMS_CLINICAL_STRIP = [
    ("Cardiac", EMS_HUB + "#cardiac"),
    ("Respiratory", EMS_HUB + "#respiratory"),
    ("Trauma", EMS_HUB + "#trauma"),
    ("Medical", EMS_HUB + "#medical"),
    ("Pediatric", EMS_HUB + "#pediatric-dosing-reference"),
]
EMS_CLINICAL_HUB_CHIP = ("EMS Clinical Hub", EMS_CLINICAL_HUB)
EMS_HUB_CHIP = ("All protocols", EMS_HUB)
EMS_PROCEDURES_CHIP = ("Procedures", "resources/ems.md#procedures")
# Fire side, split in two (owner ruling 2026-11-20): the SOP index and the
# reference shelf are different pages now, so each scroller points at its own page.
SOP_HUB_CHIP = ("All SOPs", FIRE_HUB)
SOP_STRIP = [
    ("Emergency Operations", FIRE_HUB + "#emergency-operations"),
    ("Special Operations", FIRE_HUB + "#special-operations"),
    ("Equipment & Apparatus", FIRE_HUB + "#equipment-apparatus"),
    ("Safety & Health", FIRE_HUB + "#safety-health"),
    ("General Administration", FIRE_HUB + "#general-administration"),
    ("Public Relations", FIRE_HUB + "#public-relations"),
]
FIRE_REF_HUB_CHIP = ("Fire resources", FIRE_REF_HUB)
FIRE_REF_STRIP = [
    ("Frameworks", FIRE_REF_HUB + "#frameworks"),
    ("Field References", FIRE_REF_HUB + "#field-references"),
    ("Strategies", FIRE_REF_HUB + "#strategies"),
    ("FORCES Study Aid", FIRE_REF_HUB + "#study-aids"),
]

# Static category buttons across the top of the Protocols page — one button per
# category, ALL visible at once, no horizontal scroller and no drawer (owner ruling
# 2026-11-20: the scroller hid half the categories off the right edge of a phone).
# Anchors are validated against the headings the page actually gets, so a renamed
# group aborts the build instead of shipping a dead button.
EMS_BUTTONS = [
    ("Cardiac", "#cardiac"),
    ("Respiratory", "#respiratory"),
    ("Trauma", "#trauma"),
    ("Medical", "#medical"),
    ("Pediatric", "#pediatric-dosing-reference"),
    ("Administrative", "#administrative"),
    ("Procedures", "#procedures"),
    ("Toxicology", "#toxicology"),
    ("Neurologic", "#neurologic"),
    ("General", "#general"),
    ("Pharmacology", "#pharmacology"),
    ("EMS SOPs", "#ems-sops"),
]
# Tools, not categories: these leave the page for a working calculator, so they carry
# .qdtool and sit after the categories in the same wrapping button block.
EMS_TOOLS = [
    ("Drug Calculator", "../medications.md#advanced-drip-rate-protocol-calculator"),
    ("Pediatric Calculator", "../pediatric-dosing/calculator.md"),
]

# Bottom utility row, left column: the five policies a crew actually reaches for.
POLICY_TILES = [
    ("Hazardous Weather", "personnel-policies/policies/26-hazardous-weather.md",
     "Storm, closure, call-back"),
    ("Overtime / Comp Time", "personnel-policies/policies/13-overtime-compensatory-time.md",
     "Pay codes & comp banks"),
    ("Leave", "personnel-policies/policies/15-annual-leave-vrs-plan-1-plan-2-and.md",
     "Annual, sick, FMLA"),
    # The label names the destination page (EMS 19.00 Incident Infection Control): there
    # is no standalone exposure-reporting page and that SOP has no exposure anchor, so a
    # label promising "Exposure Reporting" would over-promise the target.
    ("Exposure / Infection Control", "sops/ems/EMS-1900-Incident-Infection-Control.md",
     "Post-exposure steps"),
    ("City HR Manual", "personnel-policies/index.md",
     "City HR policy manual"),
]

# Bottom utility row, right column: the portals a crew actually opens. The first three
# are the systems themselves (their own hosts, titled as the sites title themselves);
# the rest are the links.md group anchors (hand-written {#ids} in links.md, so a title
# rename cannot drift them) plus the station hub.
CREW_CHIPS = [
    ("ESO Suite", "https://www.esosuite.net/login/Va00340"),
    ("LogRx", "https://logrx.com/"),
    ("VendNovation", "https://ems.vendnovation.com/"),
    ("Maps & Danger", LINKS_PAGE + "#response"),
    ("Run Docs", LINKS_PAGE + "#doc"),
    ("Apparatus", LINKS_PAGE + "#readiness"),
    ("Training", LINKS_PAGE + "#training"),
    ("City", LINKS_PAGE + "#city"),
    ("Station Hub", STATION_HUB),
]
LINKS_HUB_CHIP = ("All Links", LINKS_PAGE)

# EMS clinical hub — the administrative set a crew reaches for before/after the call
# (owner's words: "refusals, destination, documentation, reporting").
EMS_ADMIN = [
    ("Refusals / AMA",
     "protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md",
     "Capacity, signature, risk"),
    ("Destination &amp; Diversion",
     "protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md",
     "Where and why"),
    ("Documentation &amp; Reporting", "sops/ems/EMS-1700-Mandatory-Reporting.md",
     "Mandatory reports"),
    ("Death Criteria / Withholding",
     "protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.md",
     "When not to start"),
    ("Field Triage", "protocols/administrative/01_STEMI_Field_Triage_PROC.md",
     "STEMI, stroke, trauma"),
    ("ALS Release to BLS", "protocols/administrative/01_ALS_Release_to_BLS_PROC.md",
     "Handing a call down"),
]
# Calculator entry points. Icons come from ICONS (drawn SVG, no icon font).
EMS_CALCS = [
    ("Drug &amp; Drip Rates", "medications.md", "Push and infusion calculator", "drug"),
    ("Pediatric Dosing Calculator", "pediatric-dosing/calculator.md",
     "Weight-based dosing", "dose"),
    ("Pediatric Dosing Tables", "pediatric-dosing/dosing-tables.md",
     "Length-based, no math", "dose"),
]
# EMS Operations & SOPs (owner-named set). Every target is checked against disk in
# quicklinks_block(); only the labels are ours.
EMS_OPS = [
    ("Controlled Substances", "sops/ems/EMS-2100-Controlled-Substances.md",
     "Waste, sign-out, drug box"),
    ("Refusals / AMA", "protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md",
     "Capacity, signature, risk"),
    # There is no separate "diversion" page in this repository; destination and
    # diversion decisions live in this protocol, so the tile points at the real text
    # rather than at a page that does not exist.
    ("Destination & Diversion",
     "protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md",
     "Where and why"),
    ("Documentation & Reporting", "sops/ems/EMS-1700-Mandatory-Reporting.md",
     "Mandatory reports"),
    ("Mass Casualty / IMS", "sops/emergency-operations/EO-100-Incident-Management-System.md",
     "Command, triage, branches"),
]

# The EMS SOP entry points on the clinical hub — a SHORT list (owner ruling
# 2026-11-20: "remove most of the SOP… make it more of the EMS resources and learning
# page"), never all 23. The complete list stays on the Protocols page's EMS SOPs
# section, which is where the hub links for the rest.
EMS_SOP_SHORT = [
    ("General EMS Guidelines", "sops/ems/EMS-100-General-EMS-Guidelines.md",
     "How we run EMS calls"),
    ("Controlled Substances", "sops/ems/EMS-2100-Controlled-Substances.md",
     "Waste, sign-out, drug box"),
    ("Medication Management & Pharmacy",
     "sops/ems/EMS-2000-Medication-Management-and-Pharmacy.md",
     "Stocking, expiries, exchange"),
    ("EMS Do Not Resuscitate", "sops/ems/EMS-600-EMS-Do-Not-Resuscitate.md",
     "DNR orders in the field"),
    ("Patient Transport", "sops/ems/EMS-1200-Patient-Transport.md",
     "Transport decisions"),
    ("EMS Certifications", "sops/ems/EMS-1300-EMS-Certifications.md",
     "Who is credentialed for what"),
]


# The EMS SOP chips on the homepage scroller. Labels are the owner's own group names
# (card t_a650f9ea); every target is one of EMS_OPS' verified pages, so the chip and
# the hub card for the same SOP never point at different files.
EMS_SOP_STRIP = [(label, path) for label, path in
                 (("Controlled Substances", "sops/ems/EMS-2100-Controlled-Substances.md"),
                  ("Refusals / AMA",
                   "protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.md"),
                  ("Diversion",
                   "protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md"),
                  ("Documentation", "sops/ems/EMS-1700-Mandatory-Reporting.md"),
                  ("MCI", "sops/emergency-operations/EO-100-Incident-Management-System.md"))]

# Policy page grouping (the full manual index still lives on personnel-policies/).
POLICY_GROUPS = [
    ("Leave & pay", [
        ("Overtime / Comp Time", "personnel-policies/policies/13-overtime-compensatory-time.md"),
        ("Annual Leave", "personnel-policies/policies/15-annual-leave-vrs-plan-1-plan-2-and.md"),
        ("Sick Leave", "personnel-policies/policies/23-sick-leave-vrs-plan-1-plan-2-and.md"),
        ("Family & Medical Leave", "personnel-policies/policies/18-family-and-medical-leave.md"),
        ("Administrative Leave", "personnel-policies/policies/14-administrative-leave.md"),
        ("Bereavement Leave", "personnel-policies/policies/16-bereavement-leave.md"),
    ]),
    ("Schedule & weather", [
        ("Work Schedules", "personnel-policies/policies/09-work-schedules-and-attendance.md"),
        ("Hazardous Weather", "personnel-policies/policies/26-hazardous-weather.md"),
    ]),
    ("Safety & exposure", [
        ("Safety Program", "personnel-policies/policies/28-safety-program-procedures.md"),
        ("Workers' Comp", "personnel-policies/policies/24-workers-compensation-and-light-duty.md"),
        ("Exposure / Infection Control", "sops/ems/EMS-1900-Incident-Infection-Control.md"),
    ]),
    ("Conduct & benefits", [
        ("Conduct & Discipline", "personnel-policies/policies/39-employee-conduct-progressive-discipline.md"),
        ("Grievance Procedure", "personnel-policies/policies/41-grievance-procedure.md"),
        ("Uniforms", "personnel-policies/policies/36-uniforms-protective-clothing-and-effective-date.md"),
        ("Hiring & Promotion", "personnel-policies/policies/07-recruitment-hiring-promotion.md"),
        ("Vehicles & Driving", "personnel-policies/policies/29-vehicle-usage-and-driving-policy.md"),
        ("Retiree Health", "personnel-policies/policies/43-retiree-health-insurance-coverage.md"),
    ]),
]

# Icons are drawn from primitives (rect/circle/line) rather than an icon font or a
# :shortcode: extension: the glyph cannot depend on a JS fetch, and adding
# pymdownx.emoji would rewrite prose on 280 clinical pages for five homepage tiles.
ICONS = {
    "dose": ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<rect x="4" y="2.5" width="16" height="19" rx="2.5" fill="none" '
             'stroke="currentColor" stroke-width="1.8"/>'
             '<rect x="6.6" y="5" width="10.8" height="3.6" rx="1" fill="currentColor"/>'
             '<circle cx="8.6" cy="12.6" r="1.25" fill="currentColor"/>'
             '<circle cx="12" cy="12.6" r="1.25" fill="currentColor"/>'
             '<circle cx="15.4" cy="12.6" r="1.25" fill="currentColor"/>'
             '<circle cx="8.6" cy="16.6" r="1.25" fill="currentColor"/>'
             '<circle cx="12" cy="16.6" r="1.25" fill="currentColor"/>'
             '<circle cx="15.4" cy="16.6" r="1.25" fill="currentColor"/></svg>'),
    "drug": ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
             '<g transform="rotate(-45 12 12)">'
             '<rect x="2.6" y="8.4" width="18.8" height="7.2" rx="3.6" fill="none" '
             'stroke="currentColor" stroke-width="1.8"/>'
             '<line x1="12" y1="8.4" x2="12" y2="15.6" stroke="currentColor" '
             'stroke-width="1.8"/></g></svg>'),
    "skills": ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
               '<rect x="9.4" y="2.8" width="5.2" height="18.4" rx="1.6" fill="currentColor"/>'
               '<rect x="2.8" y="9.4" width="18.4" height="5.2" rx="1.6" fill="currentColor"/></svg>'),
    "alarm": ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
              '<path d="M12 2.6a5.6 5.6 0 0 0-5.6 5.6v3.3L4 16h16l-2.4-4.5V8.2A5.6 5.6 0 0 0 12 2.6z" '
              'fill="currentColor"/>'
              '<rect x="10.2" y="17.2" width="3.6" height="3.8" rx="1.8" fill="currentColor"/></svg>'),
    "arrive": ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
               '<rect x="2" y="6.6" width="11.4" height="8.8" rx="1.5" fill="currentColor"/>'
               '<rect x="14.4" y="9.4" width="6.6" height="6" rx="1.4" fill="currentColor"/>'
               '<circle cx="6.6" cy="17.8" r="1.9" fill="currentColor"/>'
               '<circle cx="17.2" cy="17.8" r="1.9" fill="currentColor"/></svg>'),
}

# Personnel policies are not in the nav (only the index page is), so the strip
# names the high-traffic ones explicitly and each is checked against disk.
POLICY_CHIPS = [
    ("Full Policy Manual", "personnel-policies/index.md"),
    ("Full Text Archive", "personnel-policies/other/personnel-policy-manual.md"),
]


# ------------------------------------------------------------------ nav reading
def load_cfg():
    return yaml.safe_load(CONFIG.read_text())


# Classification is PATH-based, not menu-label-based, so the script stays
# idempotent after it has rewritten the nav into Fire/EMS hubs.
EMS_PATHS = ("protocols/", "procedures/", "pharmacology/", "medications.md",
             "pediatric-dosing/", "sops/ems/", "quick-refs/", "ems/")
# Fire reference shelf: what is NOT an SOP (owner ruling 2026-11-20). Checked before
# FIRE_PATHS, which still claims everything under sops/.
FIRE_REF_PATHS = ("fire-ems-references/",)
FIRE_REF_PAGES = {"sops/emergency-operations/EO-600a-FORCES-Mnemonic.md"}
FIRE_PATHS = ("fire-ems-references/", "sops/")
# Station = non-clinical, non-fireground utility pages (the "station mode" tempo).
# bucket_of checks the HUB constants first, so resources/station.md classifies as HUB
# even though it also starts with "resources/"; this tuple therefore lists only member
# pages, never the hub itself.
STATION_PATHS = ("station-info.md", "resources/links.md", "training/", "station/")


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
    if path in (FIRE_HUB, EMS_HUB, STATION_HUB, EMS_CLINICAL_HUB, FIRE_REF_HUB):
        return "HUB"
    if path.startswith(STATION_PATHS):
        return "STATION"
    if path.startswith("personnel-policies/"):
        return "DEPT"
    if path.startswith(EMS_PATHS):
        return "EMS"
    if path in FIRE_REF_PAGES or path.startswith(FIRE_REF_PATHS):
        return "FIRE_REF"
    if path.startswith(FIRE_PATHS):
        return "FIRE"
    raise SystemExit(f"UNCLASSIFIED page {path!r} (nav top {rec['top']!r}) — add a rule")


def group_of(rec):
    """deepest nav parent = the group the page sits in; flat sections use top."""
    return rec["parents"][-1] if rec["parents"] else rec["top"]


def group_name(rec, bucket):
    # A page that sits FLAT in its section takes the section name as its nav parent,
    # so on the next run it would invent a group called after the section ("Protocols").
    # Key these by path: the classification then never depends on how the nav was
    # written last time.
    if rec.get("file") in PATH_GROUP:
        return PATH_GROUP[rec["file"]]
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
    "FIRE": ("**Standard operating procedures** for the fire side — emergency "
             "operations, special operations, equipment and apparatus, safety, and "
             "department administration. Frameworks, field references, strategies and "
             "the FORCES study aid are on the [Fire Resources](fire-resources.md) page; "
             "clinical protocols are on [Protocols](ems.md)."),
    "FIRE_REF": ("The fire side's **reference shelf** — frameworks, field references, "
                 "strategies, and the FORCES mnemonic study aid. None of it is an SOP: "
                 "the SOPs themselves are on the [SOPs](fire.md) page."),
    "EMS": ("Every **protocol** in one index — clinical categories, skills procedures, "
            "medications, pediatric dosing, and the EMS SOPs. Front Matter and Quick "
            "References are at the top because they are how you read the rest. Fire "
            "SOPs live on the [SOPs](fire.md) page, reference material on "
            "[Fire Resources](fire-resources.md)."),
    "STATION": ("**Station mode** — the things you look up between calls, not during "
                "one: how this site works, what changed recently, training drills, and "
                "the [Crew Links & Portals](links.md) launchpad. Clinical decisions live "
                "on the [Protocols](ems.md) and [SOPs](fire.md) pages."),
}


def build_hub(bucket, title, groups):
    """Hub page: H1, lead, navigation control, then one section per group.

    On the Protocols page the navigation control is a block of STATIC category
    buttons (owner ruling 2026-11-20) — every category visible at once, wrapping
    into rows, never a horizontal scroller. Every other hub keeps the one-row
    jump strip.
    """
    lines = [f"# {title}", "", HUB_LEAD[bucket], ""]
    if bucket == "EMS":
        anchors = {slugify(g) for g, _ in groups}
        dead = [f"{l} -> {t}" for l, t in EMS_BUTTONS if t.lstrip("#") not in anchors]
        if dead:
            raise SystemExit(
                "EMS_BUTTONS point at headings that do not exist on the Protocols page: "
                + ", ".join(dead))
        missing = [t for _l, t in EMS_TOOLS
                   if not (DOCS / "resources" / t.split("#")[0]).resolve().exists()]
        if missing:
            raise SystemExit(f"EMS_TOOLS point at pages that do not exist: {missing}")
        buttons = " ".join(f"[{l}]({t})" for l, t in EMS_BUTTONS)
        tools = " ".join(f"[{l}]({t}){{ .qdtool }}" for l, t in EMS_TOOLS)
        lines += ['<div class="qldots" markdown="1">', "", buttons + " " + tools, "",
                  "</div>", ""]
    else:
        chip = "**Jump:** " + " ".join(f"[{g}](#{slugify(g)})" for g, _ in groups)
        lines += ['<div class="qljump" markdown="1">', "", chip, "", "</div>", ""]
    for g, recs in groups:
        # A group holding exactly one page with the same name (Outstanding Decisions)
        # would otherwise read "## Outstanding Decisions / - Outstanding Decisions".
        # Link the heading instead: the anchor is still #outstanding-decisions because
        # MkDocs slugs a heading by its text, links included.
        if len(recs) == 1 and recs[0]["label"] == g:
            rel = posixpath.relpath("docs/" + recs[0]["file"], "docs/resources")
            lines += [f"## [{g}]({rel})", ""]
            continue
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
            # One page whose label IS the group label (Outstanding Decisions, Training, …)
            # would otherwise nest "X" inside "X" in the drawer — the same duplicate the
            # owner flagged for Station Hub. Emit it flat instead.
            if len(recs) == 1 and recs[0]["label"] == g:
                nodes.append({recs[0]["label"]: recs[0]["file"]})
            else:
                nodes.append({g: [{r["label"]: r["file"]} for r in recs]})
        return nodes

    dept = [r for r in records if bucket_of(r) == "DEPT" and r["file"]]
    return [{"Home": HOME_PAGE},
            {"Protocols": [{"Protocols Home": EMS_HUB},
                           {"EMS Clinical Hub": EMS_CLINICAL_HUB},
                           *group_nodes("EMS", EMS_ORDER)]},
            {"SOPs": [{"SOPs Home": FIRE_HUB}, *group_nodes("FIRE", FIRE_ORDER)]},
            {"Fire Resources": [{"Fire Resources Home": FIRE_REF_HUB},
                                *group_nodes("FIRE_REF", FIRE_REF_ORDER)]},
            {"Personnel Policies": [{r["label"]: r["file"]} for r in dept]},
            {"Station Hub": [{"Station Hub Home": STATION_HUB},
                             *group_nodes("STATION", STATION_ORDER)]}]


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
def rel(from_dir, target):
    """docs-relative target ('path.md#anchor') -> href relative to docs/<from_dir>/."""
    page, _, anchor = target.partition("#")
    href = posixpath.relpath("docs/" + page, "docs/" + from_dir) if from_dir else page
    return href + ("#" + anchor if anchor else "")


def card(label, href, sub, domain, icon=None, plain=False):
    """One elevated tile: accent bar + optional icon + title + sublabel.

    Emitted as a markdown link with inline HTML, so MkDocs still rewrites the href
    (a raw `<a href="x.md">` would ship a dead .md link) and the tile is complete in
    the served HTML with JavaScript off.
    """
    ico = f'<span class="pfd-ico">{ICONS[icon]}</span>' if icon else ""
    classes = f".pfd-card .pfd-card--{domain.lower()}"
    if plain:
        classes += " .pfd-card--plain"
    return (f'- [{ico}<span class="pfd-t">{label}</span>'
            f'<span class="pfd-s">{domain} · {sub}</span>]'
            f'({href}){{ {classes} }}')


def chip(label, href, kind):
    return f'[{label}]({href}){{ .pfd-chip .pfd-chip--{kind} }}'


def check_targets(records):
    """Every curated target must exist — a renamed page breaks the build, never a tile."""
    nav_paths = {r["file"] for r in records if r["file"]}
    on_disk = lambda p: ((DOCS / p.split("#")[0]).exists()
                         or p.split("#")[0] == FIRE_REF_HUB)  # this script writes it
    missing = [p for _l, p, *_ in SCENE_TOOLS if p.split("#")[0] not in nav_paths]
    missing += [p for _l, p, _s in POLICY_TILES if not on_disk(p)]
    missing += [p for _l, p in EMS_SOP_STRIP if not on_disk(p)]
    missing += [p for _l, p in EMS_CLINICAL_STRIP if not on_disk(p)]
    missing += [p for _l, p in SOP_STRIP if not on_disk(p)]
    missing += [p for _l, p in FIRE_REF_STRIP if not on_disk(p)]
    missing += [p for _l, p, _s in EMS_SOP_SHORT if not on_disk(p)]
    # FIRE_REF_HUB is created by this script, so on the FIRST run after the split it is
    # not in the on-disk nav yet; every later --check run has it and checks it.
    missing += [p for p in (SOP_HUB_CHIP[1], FIRE_REF_HUB_CHIP[1], EMS_CLINICAL_HUB_CHIP[1],
                            EMS_HUB_CHIP[1])
                if p not in nav_paths and p != FIRE_REF_HUB]
    missing += [EMS_PROCEDURES_CHIP[1].split("#")[0]] * (not on_disk(EMS_PROCEDURES_CHIP[1]))
    missing += [p for _l, p in CREW_CHIPS if not p.startswith("http") and not on_disk(p)]
    missing += [p for _l, p, _s in EMS_OPS if not on_disk(p)]
    missing += [p for _l, p, _s in EMS_ADMIN if not on_disk(p)]
    missing += [p for _l, p, _s, _i in EMS_CALCS if not on_disk(p)]
    missing += [p for _g, pairs in POLICY_GROUPS for _l, p in pairs if not on_disk(p)]
    missing += [p for _l, p in POLICY_CHIPS if not on_disk(p)]
    missing += [p for p in (LINKS_PAGE, STATION_HUB, STATION_POLICIES, EMS_CLINICAL_HUB)
                if p not in nav_paths]
    if missing:
        raise SystemExit(f"curated link target no longer exists: {missing}")


def quicklinks_block(records):
    """The on-scene dashboard: five high-acuity tools and four scrollers.

    Card t_a650f9ea (owner's words, applied literally): every scroller starts with the
    section itself, then the real destinations. The two bottom groups are scrollers
    too, and each crew-links chip carries its own URL — the earlier row pointed all
    six chips at links.md, which is one link wearing six labels.
    """
    check_targets(records)

    parts = [QL_START, "",
             '<section class="pfd-zone" markdown="1">', "",
             '<p class="pfd-cap">High-acuity tools — one tap</p>', "",
             '<div class="pfd-quick-grid" markdown="1">', ""]
    parts += [card(label, path, sub, domain, icon)
              for label, path, sub, domain, icon in SCENE_TOOLS]
    parts += ["", "</div>", "", "</section>", "",
              '<section class="pfd-zone" markdown="1">', "",
              f'**[Protocols]({EMS_HUB})**'
              '{: .pfd-cap .pfd-cap--link .pfd-cap--ems }', "",
              '<div class="pfd-scroller pfd-scroller--ems" markdown="1">', ""]
    parts += [chip(*EMS_HUB_CHIP, "all"), chip(*EMS_CLINICAL_HUB_CHIP, "ems"),
              chip(*EMS_PROCEDURES_CHIP, "ems")]
    parts += [chip(label, href, "ems") for label, href in EMS_SOP_STRIP]
    parts += [chip(label, href, "ems") for label, href in EMS_CLINICAL_STRIP]
    parts += ["", "</div>", "",
              f'**[SOPs]({FIRE_HUB})**'
              '{: .pfd-cap .pfd-cap--link .pfd-cap--fire }', "",
              '<div class="pfd-scroller pfd-scroller--fire" markdown="1">', ""]
    parts += [chip(*SOP_HUB_CHIP, "all")]
    parts += [chip(label, href, "fire") for label, href in SOP_STRIP]
    parts += ["", "</div>", "",
              f'**[Fire resources]({FIRE_REF_HUB})**'
              '{: .pfd-cap .pfd-cap--link .pfd-cap--fire }', "",
              '<div class="pfd-scroller pfd-scroller--fire" markdown="1">', ""]
    parts += [chip(*FIRE_REF_HUB_CHIP, "all")]
    parts += [chip(label, href, "fire") for label, href in FIRE_REF_STRIP]
    parts += ["", "</div>", "", "</section>", "",
              '<section class="pfd-secondary-row" markdown="1">', "",
              '<div class="pfd-secondary" markdown="1">', "",
              f'**[City &amp; personnel policies]({STATION_POLICIES})**'
              '{: .pfd-cap .pfd-cap--link .pfd-cap--admin }', "",
              '<div class="pfd-scroller pfd-scroller--admin" markdown="1">', ""]
    # Scroller order is the owner's: the hub, the full list, then the five policies a
    # crew actually reaches for.
    parts += [chip("City &amp; Personnel Policies", STATION_POLICIES, "admin"),
              chip("All policies", STATION_POLICIES + "#full-policy-list", "admin")]
    parts += [chip(label, path, "admin") for label, path, _s in POLICY_TILES]
    parts += ["", "</div>", "", "</div>", "",
              '<div class="pfd-secondary" markdown="1">', "",
              f'**[Crew links &amp; portals]({LINKS_PAGE})**'
              '{: .pfd-cap .pfd-cap--link .pfd-cap--util }', "",
              '<div class="pfd-scroller pfd-scroller--util" markdown="1">', ""]
    # Utility, not admin: these are "where do I go" links, not policy, so they carry
    # their own neutral accent and the colour code never claims the crew row is policy.
    parts += [chip(*LINKS_HUB_CHIP, "util")]
    parts += [chip(label, href, "util") for label, href in CREW_CHIPS]
    parts += ["", "</div>", "", "</div>", "", "</section>", "",
              QL_END]
    return "\n".join(parts)


def build_ems_hub(ems_groups):
    """ems/index.md — the EMS learning page, not a second protocol index.

    Owner ruling 2026-11-20: "Remove most of the SOP. Make it more of the EMS resources
    and learning page." The full clinical category listing was dropped because it
    duplicated the Protocols page (the "jump to another jump" complaint). What stays:
    administrative protocols, a SHORT EMS SOP entry list, and the calculators. Every
    page dropped from here is still listed on resources/ems.md — the nav-coverage
    check in main() proves each nav page is placed on exactly one hub.
    """
    counts = {g: len(recs) for g, recs in ems_groups}
    lines = ["# EMS Clinical Hub", "",
             "**On-scene EMS.** This is the learning page: the administrative protocols "
             "you reach for before and after the call, the few EMS SOPs that come up "
             "most, and the calculators. Every clinical protocol, by category, is on "
             "[Protocols](../resources/ems.md).", "",
             '<section class="pfd-zone" markdown="1">', "",
             '<p class="pfd-cap pfd-cap--ems">Administrative protocols</p>', "",
             '<div class="pfd-quick-grid" markdown="1">', ""]
    for label, path, sub in EMS_ADMIN:
        lines.append(card(label, rel("ems", path), sub, "EMS", plain=True))
    lines += ["", "</div>", "",
              f"All {counts.get('Administrative', 0)} administrative protocols are listed "
              "under [Administrative](../resources/ems.md#administrative) on the Protocols "
              "page.", "", "</section>", "",
              '<section class="pfd-zone" markdown="1">', "",
             '<p class="pfd-cap pfd-cap--ems">EMS SOPs — the six that come up most</p>', "",
             '<div class="pfd-quick-grid" markdown="1">', ""]
    for label, path, sub in EMS_SOP_SHORT:
        lines.append(card(label, rel("ems", path), sub, "EMS", plain=True))
    lines += ["", "</div>", "",
              "All 23 EMS SOPs are listed under "
              "[EMS SOPs](../resources/ems.md#ems-sops).", "", "</section>", "",
              '<section class="pfd-zone" markdown="1">', "",
              '<p class="pfd-cap pfd-cap--ems">Calculators</p>', "",
              '<div class="pfd-quick-grid" markdown="1">', ""]
    for label, path, sub, icon in EMS_CALCS:
        lines.append(card(label, rel("ems", path), sub, "EMS", icon, plain=True))
    lines += ["", "</div>", "", "</section>", "",
              "## Where the rest is", "",
              "- **Every protocol** — [Protocols](../resources/ems.md), with a button for "
              "each category at the top of the page.",
              "- **Fire-side SOPs** — [SOPs](../resources/fire.md).",
              "- **Frameworks, field references, strategies, FORCES** — "
              "[Fire Resources](../resources/fire-resources.md)."]
    return "\n".join(lines).rstrip() + "\n"


def build_policies_page():
    """station/policies.md — City & personnel policies, out of the homepage hero."""
    lines = ["# City & Personnel Policies", "",
             "City of Poquoson personnel policy and department policy, out of the on-scene "
             "flow. Nothing on this page is a clinical decision — protocols are on the "
             "[EMS Clinical Hub](../ems/index.md) and fireground procedure is under "
             "[SOPs](../resources/fire.md).", "",
             '<section class="pfd-zone" markdown="1">', "",
             '<p class="pfd-cap pfd-cap--admin">Most reached</p>', "",
             '<div class="pfd-quick-grid" markdown="1">', ""]
    for label, path, sub in POLICY_TILES:
        lines.append(card(label, rel("station", path), sub, "ADMIN", plain=True))
    lines += ["", "</div>", "", "</section>", "", "## Full policy list", ""]
    for group, pairs in POLICY_GROUPS:
        lines += [f"### {group}", "",
                  " ".join(chip(label, rel("station", path), "admin") for label, path in pairs),
                  ""]
    lines += ["### The whole manual", "",
              " ".join(chip(label, rel("station", path), "admin") for label, path in POLICY_CHIPS),
              ""]
    return "\n".join(lines).rstrip() + "\n"


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
    old_set = set(old)
    hub_set = {FIRE_HUB, EMS_HUB, STATION_HUB, EMS_CLINICAL_HUB, FIRE_REF_HUB}

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
    fire_ref_g = ordered_groups([r for r in records if bucket_of(r) == "FIRE_REF" and r["file"]],
                                "FIRE_REF", FIRE_REF_ORDER)
    ems_g = ordered_groups([r for r in records if bucket_of(r) == "EMS" and r["file"]],
                           "EMS", EMS_ORDER)
    station_g = ordered_groups([r for r in records if bucket_of(r) == "STATION" and r["file"]],
                               "STATION", STATION_ORDER)
    placed = [r["file"] for _, gs in (("FIRE", fire_g), ("FIRE_REF", fire_ref_g),
                                      ("EMS", ems_g), ("STATION", station_g))
              for _g, recs in gs for r in recs]
    non_hub = {r["file"] for r in records if bucket_of(r) in ("HOME", "DEPT")}
    hub_missing = old_set - set(placed) - non_hub
    if hub_missing:
        raise SystemExit(f"HUB COVERAGE FAILURE: {sorted(hub_missing)}")
    if len(placed) != len(set(placed)):
        raise SystemExit("HUB COVERAGE FAILURE: a page is listed twice")

    files = {
        "docs/" + EMS_HUB: build_hub("EMS", "Protocols", ems_g),
        "docs/" + FIRE_HUB: build_hub("FIRE", "SOPs", fire_g),
        "docs/" + FIRE_REF_HUB: build_hub("FIRE_REF", "Fire Resources", fire_ref_g),
        "docs/" + STATION_HUB: build_hub("STATION", "Station Hub", station_g),
        "docs/" + EMS_CLINICAL_HUB: build_ems_hub(ems_g),
        "docs/" + STATION_POLICIES: build_policies_page(),
        "docs/index.md": splice_index((DOCS / "index.md").read_text(), quicklinks_block(records)),
        "mkdocs.yml": splice_nav(CONFIG.read_text(), nav),
    }

    drift = [rel for rel, text in files.items()
             if not (ROOT / rel).exists() or (ROOT / rel).read_text() != text]
    print(f"pages: {len(old_set)}  sop groups: {len(fire_g)} "
          f"({sum(len(g[1]) for g in fire_g)})  fire-ref groups: {len(fire_ref_g)} "
          f"({sum(len(g[1]) for g in fire_ref_g)})  ems groups: {len(ems_g)} "
          f"({sum(len(g[1]) for g in ems_g)})  station groups: {len(station_g)} "
          f"({sum(len(g[1]) for g in station_g)})")
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
