# Light mode: bringing the domain accents into the light scheme

Card t_19a7477e. Branch `light-colour`, base `origin/main` @ `420d1f74`
(the integrated line: ia-r3 + the offline banner). Content commit `39192bc5`.

Dark mode is the reference and did not move. Every new rule is scoped to
`[data-md-color-scheme="default"]`; proof below.

## What changed

`docs/stylesheets/extra.css` (+62 / −3), `scripts/gen_resource_pages.py`
(caption class hooks), and the three generated pages it rewrites
(`docs/index.md`, `docs/ems/index.md`, `docs/station/policies.md`).

| element | before (light) | after (light) |
|---|---|---|
| card surface | one neutral `#f8fafc` for every domain | `color-mix(in srgb, var(--pfd-accent) 7%, #fff)` |
| card border | `rgba(0,0,0,.16)` grey | 1px `var(--pfd-accent)` (plus the existing 4px left bar) |
| card hover | shadow only | tint deepens to 12% |
| section caption | one grey `rgba(0,0,0,.54)` | per-domain ink (`--pfd-ink`) |
| chip fill | `#fff` | `color-mix(in srgb, var(--pfd-accent) 10%, #fff)` |
| chip border | 45% accent | 100% accent |
| chip label | body ink `rgba(0,0,0,.87)` | per-domain ink |

The four accents themselves are unchanged (`#0284c7` / `#b91c1c` / `#475569` /
`#78716c`). They stay UI weights — a bar, an icon, a border. Body-size text
needs 4.5:1 and EMS `#0284c7` is **4.10:1 on white**, so each domain also gets
a darker ink tone that is only ever used as text:

    EMS   #0369a1     FIRE  #991b1b     ADMIN #334155     util  #57534e

Caption class hooks added by the generator: `.pfd-cap--ems`, `--fire`,
`--admin`, `--util`. The homepage caption "High-acuity tools — one tap" covers
five mixed tiles and deliberately keeps the neutral grey.

## Contrast — measured on the live DOM, not estimated

Method: open the built page in Chromium, read `getComputedStyle` for the
element's `color` and for the nearest ancestor with an opaque background, and
composite any alpha before computing the WCAG ratio. 24 pairs measured.

| element | foreground | surface | ratio | floor |
|---|---|---|---|---|
| card EMS title | rgba(0,0,0,.87) | #edf6fb | 14.95 | 4.5 |
| card EMS sublabel | rgba(0,0,0,.70) | #edf6fb | 8.08 | 4.5 |
| card FIRE title | rgba(0,0,0,.87) | #faefef | 14.59 | 4.5 |
| card FIRE sublabel | rgba(0,0,0,.70) | #faefef | 7.97 | 4.5 |
| chip all label | #800000 | #f2e6e6 | 8.96 | 4.5 |
| chip EMS label | #0369a1 | #e6f3f9 | 5.23 | 4.5 |
| chip FIRE label | #991b1b | #f8e8e8 | 7.02 | 4.5 |
| chip ADMIN label | #334155 | #edeef0 | 8.91 | 4.5 |
| chip util label | #57534e | #f2f1f0 | 6.75 | 4.5 |
| cap "Protocols" | #0369a1 | #ffffff | 5.93 | 4.5 |
| cap "SOPs" | #991b1b | #ffffff | 8.31 | 4.5 |
| cap "Fire resources" | #991b1b | #ffffff | 8.31 | 4.5 |
| cap "City & personnel policies" | #334155 | #ffffff | 10.35 | 4.5 |
| cap "Crew links & portals" | #57534e | #ffffff | 7.63 | 4.5 |
| cap "High-acuity tools — one tap" (unchanged) | rgba(0,0,0,.54) | #ffffff | 4.59 | 4.5 |
| card EMS 1px border | #0284c7 | #edf6fb | 3.75 | 3.0 |
| card EMS icon | #0284c7 | #edf6fb | 3.75 | 3.0 |
| card FIRE 1px border | #b91c1c | #faefef | 5.75 | 3.0 |
| card FIRE icon | #b91c1c | #faefef | 5.75 | 3.0 |
| chip all border | #800000 | #f2e6e6 | 8.96 | 3.0 |
| chip EMS border | #0284c7 | #e6f3f9 | 3.61 | 3.0 |
| chip FIRE border | #b91c1c | #f8e8e8 | 5.46 | 3.0 |
| chip ADMIN border | #475569 | #edeef0 | 6.52 | 3.0 |
| chip util border | #78716c | #f2f1f0 | 4.24 | 3.0 |

**Minimum text ratio 4.59:1** (the untouched neutral caption), minimum on any
changed pair **5.23:1**. **Minimum UI ratio 3.61:1** (EMS chip border), which is
over the 3:1 floor. Raw JSON: `contrast-live.json` beside this file.

The ADMIN card (only on `station/policies.html`) uses the same rules with ink
`#334155` — 9.3:1 on its 7% tint, 6.5:1 for its border.

## Colour is never the only signal

Every tile still spells its domain in the sublabel (`EMS · …`, `FIRE · …`,
`ADMIN · …` / the crew row's own words), every caption is still a word in
capitals, and the four ink tones differ in **lightness** as well as hue (EMS
5.9:1, FIRE 8.3:1, ADMIN 10.4:1, util 7.6:1 on white), so they stay ordered in
greyscale. `after-1280-home-grey.png` is the homepage converted to greyscale: the
EMS and FIRE rows still separate by border darkness and surface tone, and the
labels are unchanged.

## Dark mode did not move — two independent proofs

1. **DOM diff.** Loaded the pre-change build (`site-before`, from `origin/main`)
   and the post-change build (`site-after`) in the same Chromium, forced both to
   slate, and compared `color`, `backgroundColor`, `borderTopColor`,
   `borderLeftColor`, `borderTopWidth` for all 68 `.pfd-card` / `.pfd-chip` /
   `.pfd-cap` / `.pfd-cap--link` / `.pfd-ico` / `.pfd-t` / `.pfd-s` nodes:
   **0 differences**.
2. **Source diff.** `slate_check.py` parses every rule block in the pre- and
   post-image of `extra.css` (25 slate-scoped blocks found in each; positive
   control: a probe line inside a slate block resolves to that block) and
   attributes every added/removed line to its enclosing selector:

       added lines: 62   removed lines: 3
       changed lines inside a slate-scoped rule: 0
       (the only diff line that contains the word "slate" is a comment reading
        "Nothing here is set under the slate scheme.")

## Gates

`audit/gates/run_gates_light_colour.sh` on `39192bc5`, log
`audit/gates/light-colour-39192bc5.log`:

| gate | exit |
|---|---|
| mc_wording | 0 |
| agency_names | 0 |
| build_outstanding | 0 |
| internal_artifacts | 0 |
| **mkdocs_strict (`mkdocs build --strict`)** | **0** |
| link_sweep | 0 |
| internal_artifacts_site | 0 |
| gen_resource_pages --check | 0 (`drift: none`) |
| verify_pems_canonical | **1 — inherited** |
| level_rule | **1 — inherited** |

Both red gates fail **identically on pristine `origin/main` 420d1f74**, run in a
throwaway worktree:

    level_rule              md5 8adf487d97e30e013ec523e0a50a3a08  (identical both sides)
    verify_pems_canonical   md5 26cd556d8002ffdf92421d597ab7b77e  (identical both sides)

`verify_pems_canonical` fails on a missing gitignored cache file
(`.cache/pems_rows.jsonl`), which no fresh worktree has; `level_rule` is the
ledger-vs-page failure recorded in the previous card's handoff. Neither touches
CSS, captions, chips or cards.

## Screenshots (390×844 and 1280×800, light unless stated)

    after-1280-home.png            homepage, 1280
    after-390-home-top.png         homepage, 390
    after-390-home-scroll.png      homepage lower half, 390
    after-1280-protocols.png       Protocols page
    after-1280-emshub.png          EMS Clinical Hub
    after-1280-policies.png        City & Personnel Policies (ADMIN cards)
    after-1280-protocol.png        a protocol page
    after-1280-home-dark.png       homepage, DARK — unchanged
    after-1280-home-grey.png       homepage in greyscale
    after-390-home-grey.png        homepage in greyscale, 390
    before-1280-home.png           pre-change homepage
    before-1280-protocols.png      pre-change Protocols page
    before-1280-protocol.png       pre-change protocol page
