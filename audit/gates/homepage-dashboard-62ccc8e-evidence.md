# Homepage dashboard — round 2 (review changes applied)

Branch `homepage-dashboard`, content commit `62ccc8e` (parent `ceb0515`; the dashboard
itself landed in `3991306`, parent `cf3d308` = `origin/main`). No commit to `main`.

This round applies the two defects from the review of `3991306`. Everything else in
`audit/gates/homepage-dashboard-3991306-evidence.md` still holds and was re-measured
below; nothing in that file was regressed.

## What changed (generator only, plus one CSS accent)

| File | Change |
|---|---|
| `scripts/gen_resource_pages.py:472` | `CREW_CHIPS` emitted with `chip(..., "util")` instead of `"admin"` |
| `scripts/gen_resource_pages.py:125` | `POLICY_TILES` label `Exposure Reporting` → `Exposure / Infection Control` |
| `scripts/gen_resource_pages.py:193` | `POLICY_GROUPS` ("Safety & exposure") chip label, same rename |
| `docs/stylesheets/extra.css` | new `.pfd-chip--util` accent: `#78716c` light, `#a8a29e` dark |
| `docs/index.md`, `docs/station/policies.md` | regenerated (never hand-edited) |

`python3 scripts/gen_resource_pages.py --check` → `drift: none — all files current`, EXIT=0.

## 1. Crew Links is no longer painted as administrative (measured)

Rendered from the strict build (`site/`), Chrome, computed `::before` background:

| Row | class | measured dot (light) | measured dot (dark) |
|---|---|---|---|
| City & Personnel Policies (6 chips) | `pfd-chip pfd-chip--admin` | `rgb(71, 85, 105)` = `#475569` | `rgb(148, 163, 184)` = `#94a3b8` |
| Crew Links & Portals (6 chips) | `pfd-chip pfd-chip--util` | `rgb(120, 113, 108)` = `#78716c` | `rgb(168, 162, 158)` = `#a8a29e` |

The two sets no longer measure the same colour. Perceptual distance (CIE76 ΔE,
`audit/gates/deltae_util.py`):

```
light  util vs admin 21.16   util vs ems 47.50   util vs fire 69.67
dark   util vs admin 15.60   util vs ems 45.83   util vs fire 55.18
```

The utility accent is a warm stone neutral, so it is distinct from all three domain
hues and still reads as "not a domain" rather than as a fourth emergency service.

## 2. Exposure tile now names its destination (both pages)

The destination is `sops/ems/EMS-1900-Incident-Infection-Control.md` (EMS 19.00
Incident Infection Control), which carries the post-exposure procedure but has no
exposure heading or anchor. The label now says what the page is:

```
site/index.html                     → "Exposure / Infection Control"
site/station/policies.html          → "Exposure / Infection Control"
```

Both come from the two generator tile lists, so homepage and policies page agree.

## 3. Re-measured, unchanged from round 1 (must not regress)

| Check | Value |
|---|---|
| `.pfd-card` tiles | 5 |
| `.pfd-scroller` | 2 (`pfd-scroller--ems`, `pfd-scroller--fire`) |
| `.qlone` elements | 0 |
| `scrollWidth == innerWidth` at 390 | 390 == 390 |
| `scrollWidth == innerWidth` at 320 | 320 == 320 |
| labels overflowing their box at 320 | 0 |
| `.md-top` on dashboard | `display: none`, rect `[0,0,0,0]` |
| H1 box at 390 | `[16, 100, 358, 52]` (pill suppressed, no overlap) |
| dark card surface / page | `rgb(48, 51, 58)` on `rgb(30, 33, 41)` |
| dark chip text | `rgba(226, 228, 233, 0.82)` |

Dark mode was switched with the site's own palette toggle (body
`data-md-color-scheme="slate"`), not by faking CSS variables.

## 4. Pip strip is not collateral damage (same build)

`/protocols/cardiac/04_Chest_Pain_ACS_PROC.html` at 390px:

```
pip-blocks 1 · pips 73 · pip-strip.css linked · pip-strip.js loaded
scrollWidth 390 == innerWidth 390 · .md-top display: block (only the dashboard hides it)
```

`git diff --stat ceb0515 62ccc8e` touches only the four files in the table above:
no file under `docs/protocols/`, `docs/procedures/`, no `pip-strip.css`, no
`pip-strip.js`, no `mkdocs_pip_strip.py`.

## 5. Gates

`audit/gates/homepage-dashboard-62ccc8e.log` — 12/12 gates, every one `EXIT=0`
(`gen_resource_pages`, `pip_mapper`, `verify_pems_canonical`, `level_rule`,
`mc_wording`, `agency_names`, `build_outstanding`, `internal_artifacts`,
`mkdocs_strict`, `verify_pip_strip`, `link_sweep`, `internal_artifacts_site`).

Screenshots: `audit/homepage/evidence-2026-11-20/utility-row-390-light-r2.png` and
`utility-row-390-dark-r2.png`.
