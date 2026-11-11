"""Build-time field blocks: on-scene summaries on SOPs + quick-reference bars on protocols.

Why a hook instead of editing the markdown:

1. **EO 6.00 is porter-owned.** It is registered in `scripts/port_reference.py` SITE_MAP,
   so any summary typed into `docs/sops/.../EO-600-*.md` is destroyed the next time that
   vault note is re-ported. Same for the initial-alarm matrix. A build-time block survives.
2. **Idempotent by construction.** Nothing is written into a source file, so there is no
   marker to maintain and no double-injection on a rebuild.
3. **One auditable table.** Every injected sentence lives in this file, so a reviewer can
   read the whole clinical surface this adds in one place.

Content rule that matters more than the plumbing: the bullets below are **pointers into the
page's own ratified text**, each carrying the section it came from. They restate the SOP's
structure — they do not add doses, thresholds, or authorities. Nothing here may state a
clinical action that the source section does not already state.
"""
import posixpath
import re

# ---------------------------------------------------------------- summaries
# src_uri -> bullets. Derived by reading each SOP; every bullet names its section.
SUMMARIES = {
    "sops/emergency-operations/EO-600-First-to-Arrive-Duties.md": {
        "title": "30-Second On-Scene Summary",
        "bullets": [
            "First arriving officer **establishes Command** and keeps it until a face-to-face, "
            "radio-announced transfer — §VI.",
            "Priorities in order: **life safety, incident stabilization, property conservation** — §IV.",
            "Risk doctrine: **risk a lot for a savable life, risk little for savable property, "
            "risk nothing for what is already lost** — §V.",
            "**Size-up is continuous** (Building / Incident / Resource); complete a 360 when "
            "conditions and staffing permit. First-arriving engine **secures water supply** — §VII, §X.",
            "Initial radio report carries unit, arrival, building description, conditions, strategy, "
            "initial actions, command, tactical channel and working-incident declaration — §VIII. "
            "Company assignments follow §XII.",
        ],
    },
    "sops/ems/EMS-1000-ALS-Engine-Response.md": {
        "title": "30-Second On-Scene Summary",
        "bullets": [
            "**Engine response plus the medic unit** for the complaint types this SOP lists; it "
            "applies to all career and volunteer personnel — §I, §II, §III.",
            "Airway / breathing / circulation: **cardiac or respiratory arrest, near drowning, "
            "difficulty breathing, chest pain** — §III.",
            "**Burns:** second or third degree over major body portions (especially head and face) "
            "and **all electrical burns** — §III.",
            "**Trauma:** serious blunt or any penetrating injury, shootings, stabbings, "
            "lacerations with significant blood loss, severe orthopaedic emergencies "
            "(spine, pelvis, multiple fractures), and MVCs described as car/pedestrian, "
            "car/bicycle, motorcycle, rolled over or entrapment — §III.",
            "Neuro / OB / other: **altered level of consciousness, stroke, repeated or extended "
            "seizure (or first seizure, febrile seizure), imminent or post childbirth "
            "including miscarriage and pregnancy or labour complications, heat with "
            "convulsions or delirium, possible DOA** — §III.",
            "The SOP states plainly that it **is not all-inclusive** and cannot encompass every "
            "situation — use judgement and contact Medical Control when unsure.",
        ],
    },
}

# --------------------------------------------------------------- quick refs
# Store the TARGET FILE ONLY. The href is computed per page with relpath, because these
# pages live at different depths (protocols/cardiac/x.html needs ../../quick-refs/, while a
# page at docs root needs quick-refs/). Hardcoding "../quick-refs/..." produced 41 broken
# links in a live build — and MkDocs did NOT warn, because on_post_page injection happens
# AFTER link validation, so nothing else checks these hrefs. scripts/link_sweep.py does.
CARDS = {
    "gcs": ("Glasgow Coma Scale", "quick-refs/glasgow-coma-scale.html"),
    "apgar": ("APGAR Scoring", "quick-refs/apgar-scoring.html"),
    "tbsa": ("Burn TBSA Estimation", "quick-refs/burn-tbsa-estimation.html"),
    "ecg": ("12-Lead Placement & Territories", "quick-refs/ecg-12-lead-placement.html"),
}

# (src_uri prefix, card keys) — explicit so a reviewer can see exactly which clinical
# pages gain a cross-link. Prefix match, so "protocols/trauma/" covers every trauma file.
REF_RULES = [
    ("protocols/trauma/09_Burns_Thermal", ["tbsa"]),
    ("protocols/trauma/09_Electrical", ["tbsa"]),
    ("protocols/trauma/09_Lightning", ["tbsa"]),
    ("protocols/respiratory/03_Smoke_Inhalation", ["tbsa"]),
    ("protocols/trauma/", ["gcs"]),
    ("protocols/administrative/01_Trauma_Field_Triage", ["gcs"]),
    ("protocols/administrative/01_STEMI", ["ecg"]),
    ("protocols/cardiac/04_Chest_Pain_ACS", ["ecg"]),
    ("protocols/cardiac/04b_Aortic_Dissection", ["ecg"]),
    ("protocols/cardiac/", ["ecg"]),
    ("protocols/medical/07_OB_Emergencies", ["apgar", "gcs"]),
    ("protocols/administrative/01_Safe_Transport_of_Pediatric", ["gcs", "apgar"]),
    ("protocols/general/02_Diving_and_Drowning", ["gcs"]),
    ("protocols/neurologic/", ["gcs"]),
]


def _src(page):
    f = getattr(page, "file", None)
    return str(getattr(f, "src_uri", "") or "") if f is not None else ""


def on_page_markdown(markdown, page, config, files, **kwargs):
    """Insert the on-scene summary above Section I (after the Connected Notes block)."""
    spec = SUMMARIES.get(_src(page))
    if not spec:
        return markdown
    box = [f'!!! abstract "{spec["title"]}"']
    box += [f"    - {b}" for b in spec["bullets"]]
    block = "\n".join(box) + "\n\n"
    # Anchor on the first Roman-numeral section heading; CONNECTED blocks sit above it and
    # admonitions must not be nested inside them.
    m = re.search(r"^## (?:I{1,3}|IV|V|VI{1,3}|IX|X{1,3})[.]?\s", markdown, re.M)
    if not m:
        m = re.search(r"^## ", markdown, re.M)
    if not m:
        return markdown
    return markdown[:m.start()] + block + markdown[m.start():]


def on_post_page(output, *, page, config):
    """Insert a quick-reference chip strip directly under the page title."""
    src = _src(page)
    if not src:
        return output
    keys, seen = [], set()
    for prefix, ks in REF_RULES:
        if src.startswith(prefix) or src == prefix + ".md":
            for k in ks:
                if k not in seen:
                    seen.add(k)
                    keys.append(k)
    if not keys:
        return output
    # relative depth of THIS page's output file, so the chip href is correct at any level
    here = posixpath.dirname(getattr(page.file, "dest_path", "") or "") or "."
    chips = " ".join(
        '<a class="qref" href="{}">{}</a>'.format(posixpath.relpath(tgt, here), label)
        for label, tgt in (CARDS[k] for k in keys))
    bar = f'<div class="qrefbar"><span class="qref-lbl">Quick ref</span>{chips}</div>'
    # Under the H1 so it is seen before the protocol body, never after a scroll.
    m = re.search(r"</h1>", output)
    if not m:
        return output
    return output[:m.end()] + "\n" + bar + output[m.end():]
