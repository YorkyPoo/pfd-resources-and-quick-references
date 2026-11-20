# Homepage → on-scene dashboard — evidence (card t_e787ab8d)

Branch `homepage-dashboard`, content commit `3991306` (parent `cf3d308` = `origin/main`).
No commit to `main`; no protocol page touched. Preview slot:
<https://yorkypoo.github.io/pfd-resources-and-quick-references/preview/home/>
(gh-pages commit `09e64de`, `preview/` subtree only — verified: `git diff --name-only 09e64de^ 09e64de | grep -v '^preview/'` is empty).

Everything below was measured in Chrome against the **published** slot
(`…/preview/home/`) and/or the same build served locally, not inferred from source.

## 1. Structure (rendered)

| Zone | Rendered from the served HTML |
|---|---|
| Top | 5 tiles: Pediatric Dosing Calculator · Drugs & Drip Rates · Skills Procedures · Alarm Assignments · First to Arrive (EO 6.00) — `document.querySelectorAll('.pfd-card').length = 5` |
| Middle | 2 scrollers: `pfd-scroller--ems` (All EMS SOPs · Cardiac · Respiratory · Trauma · Medical · Pediatric) and `pfd-scroller--fire` (Emergency Ops · Field References · Strategies · Frameworks · Special Operations · Equipment & Apparatus) |
| Bottom | `.pfd-secondary-row` → City & Personnel Policies (5 chips + All policies) beside Crew Links & Portals (6 chips). One column < 761px, two columns ≥ 761px (`grid-template-columns: 451.797px 451.812px` at 1200px) |

Grid: `139.203px 139.203px` at 320px and `174.203px 174.203px` at 390px (two-up);
`302.266px 302.266px 302.281px` at 1200px (three-up).

## 2. `qlone` gone, marker kept, generator is the source

```
$ grep -c 'qlone' docs/index.md
0
$ grep -n 'QUICKLINKS' docs/index.md
7:<!-- QUICKLINKS:START (generated — scripts/gen_resource_pages.py; do not hand-edit) -->
75:<!-- QUICKLINKS:END -->
$ python3 scripts/gen_resource_pages.py --check   # idempotent, EXIT=0
pages: 233  fire groups: 9 (90)  ems groups: 16 (136)  station groups: 4 (4)
drift: none — all files current
```

The generator now also writes `docs/ems/index.md` (clinical hub) and
`docs/station/policies.md` (policies), and their nav entries are regenerated from
`mkdocs.yml` rather than hand-maintained. `.qlone` / `.qltools` CSS was removed
with the door rows; `.qljump` is untouched (the hub pages still use it).

## 3. Back-to-top pill vs H1

`body:has(.pfd-quick-grid) .md-top { display: none !important; }` — the pill is
suppressed on dashboard pages only. Measured on the published slot at 390px:

```
topPill display = "none",  rect = [0, 0, 0, 0]     (no box, cannot overlap)
H1 box          = [16, 100, 374, 152]
```
At 320px: pill `none` / rect `[0,0,0,0]`, H1 `[16, 100, 304, 152]`.

The feature is not disabled site-wide: on the same build,
`protocols/cardiac/04_Chest_Pain_ACS_PROC.html` reports `.md-top` `display: block`.

## 4. Contrast (computed colours, alpha composited over the real surface)

Light scheme — card surface `#f8fafc`, page `#ffffff`:

| element | foreground | ratio |
|---|---|---|
| card title | `#212121` (rgba 0,0,0,.87) | **16.07:1** |
| card sublabel (domain line) | `#4d4d4d` (80% ink) | **8.40:1** |
| EMS accent bar `#0284c7` | — | 4.10:1 (graphic, ≥3:1) |
| FIRE accent bar `#b91c1c` | — | 6.47:1 |
| ADMIN accent bar `#475569` | — | 7.58:1 |
| chip text | `#212121` | 16.07:1 |
| zone caption | `#757575` | 4.59:1 |

Dark scheme — card surface `#30333a`, page `#1e2129`:

| element | foreground | ratio |
|---|---|---|
| card title | `#c2c4ca` | **7.27:1** |
| card sublabel | `#a5a7ad` | **5.25:1** |
| EMS accent `#38bdf8` | — | 5.91:1 |
| FIRE accent `#f87171` | — | 4.58:1 |
| ADMIN accent `#94a3b8` | — | 4.94:1 |

The sublabel deliberately uses 80% of the body ink instead of Material's
`--md-default-fg-color--light` (which measured 4.59:1): the sublabel is the only
place the domain is *spelled*, so it is held well above the 4.5:1 floor.
Accent colours are lightened on slate because the light-scheme hexes measure
~1.5–2.2:1 as icon/bar on the dark card.

## 5. Phone widths, horizontal scroll, scroller count

Published slot, device emulation, `document.documentElement.scrollWidth`:

| viewport | scrollWidth | bodyScrollWidth | scrollers | cards |
|---|---|---|---|---|
| 320 | 320 | 320 | 2 | 5 |
| 390 | 390 | 390 | 2 | 5 |

Same on `/preview/home/ems/index.html` (320: 320) and
`/preview/home/station/policies.html` (320: 320). No horizontal page scroll.
Each of the two scrollers scrolls internally (621px / 856px of chips inside a
286–356px box) — that is the intended behaviour, and the count of *scrollers* is 2.

At 320px the tile type steps down (title 13.44px, icon 22px) because Material's
global word-break split "Assignments" into "Assignmen/ts" at 139px; measured
after the fix: every `.pfd-t`/`.pfd-s` has `scrollWidth == clientWidth`.

## 6. Gates

`audit/gates/run_gates_homepage.sh` → `audit/gates/homepage-dashboard-3991306.log`:

```
gen_resource_pages EXIT=0    pip_mapper EXIT=0
verify_pems_canonical EXIT=0 level_rule EXIT=0
mc_wording EXIT=0            agency_names EXIT=0
build_outstanding EXIT=0     internal_artifacts EXIT=0
mkdocs_strict EXIT=0         verify_pip_strip EXIT=0
link_sweep EXIT=0            internal_artifacts_site EXIT=0
ALL GATES EXIT=0 (12 of 12)
```

Note on `verify_pems_canonical`: its deliverable check wants the gitignored
derived cache `audit/level-scan/.cache/pems_rows.jsonl`. A fresh worktree does
not have it, so the file was copied from a sibling worktree of the same repo
(`wt-piproll`); it is gitignored and is not part of the commit. Without it the
gate fails on a missing cache file, not on any content invariant.

## 7. Pip strip is not collateral damage

Same build, `protocols/cardiac/04_Chest_Pain_ACS_PROC.html` (local and published):

```
pipBlocks = 1, pips = 73, pickerButtons = 6,
pip-strip.css loaded = true, pip-strip.js loaded = true
```
`docs/stylesheets/pip-strip.css`, `docs/javascripts/pip-strip.js` and
`scripts/mkdocs_pip_strip.py` are untouched (`git diff --stat` lists neither).
`verify_pip_strip --base site --archive audit/archive/tables-2026-11-20` is
EXIT=0 in the gate log.

## Screenshots (`audit/homepage/evidence-2026-11-20/`)

| file | what it shows |
|---|---|
| `home-390-light.png` | published home, 390px, light |
| `home-390-dark.png` | published home, 390px, dark scheme |
| `home-320-light.png` | published home, 320px |
| `home-390-utility-row.png` | the two-column utility row (policies / crew links) |
| `ems-hub-390.png` | new `ems/index.html` clinical hub |
| `policies-390.png` | new `station/policies.html` |

## Known limits / decisions worth an owner's eye

* **"Diversion"** has no page of its own in this repository. The EMS hub's
  *Destination & Diversion* tile points at
  `protocols/administrative/01_Transportation_and_Destination_Determination_PROC.md`,
  the protocol that actually decides destination. It is labelled for the topic,
  not for a page that does not exist.
* **"Exposure Reporting"** likewise has no personnel-policy page; the tile points at
  `sops/ems/EMS-1900-Incident-Infection-Control.md`, whose "post-exposure" section is
  the written procedure.
* **"City HR"** points at `personnel-policies/index.md` (the city personnel manual
  index) and is labelled *City HR Manual*.
* Regenerating the hubs also picked up pre-existing drift: `protocols/outstanding-decisions.md`
  was in the nav but missing from `resources/ems.md`, so the EMS hub gained an
  *Orientation* group (renamed via `GROUP_RENAME`, same fix class as the
  2026-11-11 "Station Hub inside Station Hub" report).
* GitHub Pages served the *previous* `extra.css` on first visit after re-publishing;
  a hard refresh (cache clear) showed the new file. Worth knowing when the owner
  opens the slot.
