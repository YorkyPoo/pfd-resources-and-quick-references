# Provider level grid — relabelled R / B / A / I / P

**Card:** t_49b31001 · **Owner ruling:** 2026-11-20 · **Branch:** `provider-level-letters`
(off local `main` @ `9818904`) · **Preview:** <https://yorkypoo.github.io/pfd-resources-and-quick-references/preview/>

## Mapping applied

| Column | Full name printed in the legend | Legacy abbreviation kept in parentheses |
|---|---|---|
| **R** | Emergency Medical Responder | (EMR) |
| **B** | Emergency Medical Technician | (EMT) |
| **A** | Advanced Emergency Medical Technician | (AEMT) |
| **I** | Intermediate | — |
| **P** | Paramedic | — |

The parenthetical is the only relabel decision the card left open. It is there because the
rest of the site — and the PEMS 2024 source — still print `EMR` / `EMT` (496 chips, see the
census below). Without it a reader who is handed "B" has no bridge to the source document
they are holding. Each full name appears exactly once.

## What changed on the page

`docs/protocols/front-matter/01 - How to Read the Protocols.md` — four label edits plus one
rendering fix, nothing else:

1. Legend: five bullets now lead with the letter (`**R:** Emergency Medical Responder (EMR)` …).
2. "locate your certification level at the top of the columns (EMR, EMT, A, I, P)" → `(R, B, A, I, P)`.
3. Matrix header: `| # | Action / Intervention | EMR | EMT | A | I | P |` → `| … | R | B | A | I | P |`.
4. Cumulative ladder note: `(EMR→EMT→A→I→P)` → `(R→B→A→I→P)`.
5. Blank line inserted before the legend list.

**Untouched, verified byte-for-byte:** all four data rows and the separator row
(`diff` of `^| [0-9]` and `^|---` between the parent and the edit is empty), so the
dot / blank / `[I]` / `MC` pattern carries exactly the authority it carried before. The key
text about dot / blank / MC / ⚠ is unchanged. The illustrative conflict example
("a label reading *EMT and above* beside a blank EMT cell") still says EMT on purpose — it
quotes the **source**, which still says EMT.

**Item 5 is a fix, not a label change.** On the live site the five bullets render as one
paragraph with a literal `* ` on each line, because the list sat directly under the lead-in
paragraph. The card requires the legend to actually give each letter's full name, so the
list now renders as a list. Verified against the live root before the change
(`<p>The protocols use the following abbreviations …: * <strong>EMR:</strong> …`).

## Gate conflict found and handled (not weakened)

`scripts/level_rule.py`'s `sc_wrap_audit()` recognised a level matrix by the header
`| # | Action / Intervention | EMR |`. The moment the legend was relabelled, the audit
stopped seeing it: the gate would have reported **0** matrices instead of the honest **1**, a
silent pass on the one page that must keep a multi-column matrix. The header regex now accepts
both spellings (`(?:EMR|R)`), verified to still find exactly **1** matrix across **63**
`sc-wrap` blocks — no new hits. The ledger and the `--check`/`--report` prose that described
the legend as "must stay as it is" were regenerated to match the ruling.

## Remaining full level names on the site (for the owner's decision)

`scripts/count_level_vocabulary.py` (added by this card, read-only, re-runnable):

### Per-row chips — the letters not yet followed

| Chip label | Count |
|---|---|
| `EMT` | 138 |
| `EMR` | 134 |
| `I` | 107 |
| `A` | 90 (already the new letter) |
| `P` | 27 (already the new letter) |
| **total** | **496 chips in 11 directories** |

So 272 chips still print `EMR` / `EMT`; `I`, `A`, `P` are already single letters. Following
the ruling onto the chips is a 2-token edit in the converter plus a ledger regenerate — not
done, not asked.

### Full names in prose / table cells (chips excluded): 207 in 29 files

| Location | Count |
|---|---|
| `protocols/outstanding-decisions.md` | 113 |
| `sops/ems/` (7 pages) | 48 |
| `protocols/respiratory/` (6 pages) | 17 |
| `protocols/front-matter/` (3 pages, incl. this legend's 7) | 10 |
| `protocols/cardiac/` (3 pages) | 6 |
| `sops/general-administration/` (2 pages) | 4 |
| `station-info.md` | 2 |
| `training/index.md` | 2 |
| `pharmacology/Ondansetron.md` | 1 |
| `procedures/Endotracheal_Intubation.md` | 1 |
| `protocols/administrative/01_Stroke_Field_Triage_PROC.md` | 1 |
| `sops/public-relations/PR-200-Ride-Along-Program.md` | 1 |
| `sops/safety-and-health/SH-300-Station-Conduct-and-Safety.md` | 1 |
| **total** | **207** |

**Pediatric dosing tables: 0.** `docs/pediatric-dosing/*` carry weight-based doses with no
provider-level column or name at all — nothing to relabel there.

## Gates (tree `5aea342`, logs committed; identical `docs/` at `1521a2e`)

| Gate | Result |
|---|---|
| `scripts/verify_pems_canonical.py` | **EXIT=0** |
| `scripts/level_rule.py --check` | **EXIT=0** (reports 1 out-of-scope matrix = this legend, line 34) |
| `scripts/mc_wording.py --check` | **EXIT=0** |
| `mkdocs build --strict` | **EXIT=0** |
| `scripts/build_outstanding_decisions.py --check` | **EXIT=1 — pre-existing on `main`, not caused by this card** |

That last one: `docs/protocols/outstanding-decisions.md` on `main` still says the ETT rows are
`p.247#3` / `p.247#5`; the source rows are `#4` / `#6` since the row-split work. Reproduced on a
clean `main` worktree (`--check` fails there too, and a rebuild there produces exactly the same
two-line diff), so it is a stale generated page inherited from `main`. Not fixed here — out of
this card's scope, one command to fix.

## Preview

- Matrix page: <https://yorkypoo.github.io/pfd-resources-and-quick-references/preview/protocols/front-matter/01%20-%20How%20to%20Read%20the%20Protocols.html>
- Protocol page: <https://yorkypoo.github.io/pfd-resources-and-quick-references/preview/procedures/Capnography.html>
- Live root: <https://yorkypoo.github.io/pfd-resources-and-quick-references/protocols/front-matter/01%20-%20How%20to%20Read%20the%20Protocols.html> — still `EMR / EMT / A / I / P`, untouched.
- `origin/main` before and after: `2cf1f4f`. Nothing was pushed to `main`.

The preview is built from `pilot-references-block` + this card's commits (branch
`preview-relabel-tmp`, `e2509e2`, four gates EXIT=0 there too), so the pilot pages already
published for review stay visible instead of being reverted to `main`.
