# Light colour, rebased onto home-r4 — one coherent preview

Card t_ecef0aea. Branch `light-colour-r2`, base **home-r4 `a869a4c3`**,
content tip **`f75bc4ef`**. Supersedes the sequencing of the parent card
(t_19a7477e), whose branch was cut from `origin/main` `420d1f74` and therefore
showed the pre-round-4 homepage.

## Rebase

    $ git log --oneline -5
    f75bc4ef audit(gates): fix the gate runner's repo root (audit/gates is two levels down)
    8e3b811b audit(gates): light-colour — record the published slot and the before shots
    88a86fba audit(gates): light-colour 39192bc5 — 7/9 EXIT=0, both reds fail byte-identically on pristine main
    36865545 Light scheme: give cards, captions and chips their domain colour
    0763113d offline banner: pin it under the top chrome, never over the bottom nav
    a869a4c3 audit(gates): 17/18 EXIT=0 on home-r4 (58cda79e); level_rule fails identically on pristine main

The replay pulled in `0763113d` (the offline banner) as well: home-r4 was cut
before that merge, so the rebased tip now carries home-r4's structure **and**
the banner. It applied cleanly.

Two conflicts, both resolved as **home-r4's structure with light-colour's
classes**:

| file | resolution |
|---|---|
| `scripts/gen_resource_pages.py` | home-r4's `quicklinks_block()` (EMS Hub caption, no SOPs scroller, six scene tiles); light-colour's caption class hooks re-applied |
| `docs/index.md` | not hand-merged — regenerated from the resolved generator |

`docs/ems/index.md` and `docs/station/policies.md` auto-merged; both are
generated and were re-emitted by the generator, so all three pages are
generator output, not hand edits. `git diff a869a4c3..HEAD` on those three
pages is exactly the caption class hooks and nothing else.

Caption → domain mapping the rebased generator emits (rendered, `grep pfd-cap`):

| caption | class | ink |
|---|---|---|
| `EMS HUB` | `.pfd-cap--ems` | `#0369a1` |
| `FIRE RESOURCES` | `.pfd-cap--fire` | `#991b1b` |
| `CITY & PERSONNEL POLICIES` | `.pfd-cap--admin` | `#334155` |
| `CREW LINKS & PORTALS` | `.pfd-cap--util` | `#57534e` |
| `HIGH-ACUITY TOOLS — ONE TAP` | (none — mixed domains) | neutral `rgba(0,0,0,.54)` |

The `SOPs` scroller is gone from round 4, and nothing carries a fire caption
for it: `grep -c 'SOPs' docs/index.md` = **0**.

## Gates on the rebased tip

`audit/gates/run_gates_light_colour_rebased.sh` → log
`audit/gates/light-colour-r2-f75bc4ef.log`. Union of the home-r4 (18) and
light-colour (9) suites.

    EXIT=0  gen_resource_pages (drift: none)      EXIT=0  mkdocs_strict
    EXIT=0  connected_notes                       EXIT=0  verify_pip_strip
    EXIT=0  pip_mapper                            EXIT=0  link_sweep
    EXIT=0  mc_wording                            EXIT=0  internal_artifacts_site
    EXIT=0  agency_names                          EXIT=0  scroller_hrefs
    EXIT=0  build_outstanding                     EXIT=0  hub_anchors
    EXIT=0  internal_artifacts                    EXIT=0  bottom_bar
    EXIT=0  naming_sweep                          EXIT=0  protocols_untouched
    EXIT=0  slate_untouched (0 changed slate lines)
    EXIT=1  verify_pems_canonical  — INHERITED
    EXIT=1  level_rule             — INHERITED

Both reds are byte-identical to pristine `origin/main` `420d1f74`, run in a
throwaway worktree:

    level_rule              md5 8adf487d97e30e013ec523e0a50a3a08  (identical)
    verify_pems_canonical   md5 26cd556d8002ffdf92421d597ab7b77e  (identical)

`verify_pems_canonical` fails on the gitignored cache `.cache/pems_rows.jsonl`
(no fresh worktree has it); `level_rule` is the ledger-vs-page failure recorded
in the earlier cards. Neither touches CSS, captions, chips or cards.

## Contrast — re-measured after the rebase

Method: Chromium `getComputedStyle` on the **rebased** `site/` build, foreground
composited over the nearest opaque ancestor background, WCAG 2.x ratio. Raw
data: `audit/gates/light-colour-r2-contrast-live.json` (30 pairs, 3 pages).

| element | ratio | floor |
|---|---|---|
| card EMS title / sublabel | 14.95 / 8.08 | 4.5 |
| card FIRE title / sublabel | 14.59 / 7.97 | 4.5 |
| chip all / EMS / FIRE / ADMIN / util label | 8.96 / 5.23 / 7.02 / 8.91 / 6.75 | 4.5 |
| cap EMS Hub | 5.93 | 4.5 |
| cap Fire resources | 8.31 | 4.5 |
| cap City & personnel policies | 10.35 | 4.5 |
| cap Crew links & portals | 7.63 | 4.5 |
| cap High-acuity tools (unchanged) | 4.59 | 4.5 |
| card ADMIN (policies page) title / sublabel | 14.75 / 8.02 | 4.5 |
| card EMS/FIRE 1px border + icon | 3.75 / 5.75 | 3.0 |
| chip EMS/FIRE/ADMIN/util border | 3.61 / 5.46 / 6.52 / 4.24 | 3.0 |

Minimum text pair **4.59:1** (the untouched neutral caption); minimum on any
changed text pair **5.23:1**; minimum UI pair **3.61:1**. All above floor.
The ratios equal the pre-rebase numbers because the page background is still
Material's light `#fff` and the tints are unchanged — these are fresh reads of
the rebased DOM, not carried-over values.

## Dark mode still did not move

1. **Source.** `python3 audit/gates/slate_check.py a869a4c3` →
   `changed lines inside a slate-scoped rule: 0` (positive control fires).
   Against `origin/main` the same check is also 0.
2. **Computed styles.** Base build (`a869a4c3`) vs rebased build, both forced to
   slate with transitions disabled, 12 shared selectors (EMS/FIRE card, its
   title/sublabel/icon, all five chip variants, both caption variants):
   **0 differences**. `color`, `backgroundColor`, `borderTopColor`,
   `borderLeftColor`, `borderTopWidth` compared on each.

Pitfall worth recording: switching the scheme attribute at runtime and reading
`getComputedStyle` immediately returns the *pre-switch* colour, because
Material transitions link colours over 125 ms. The first pass showed phantom
chip differences; injecting `*{transition:none!important}` before the switch
made them disappear. The slate attribute lives on `<body>`, not `<html>`.

## Published slot — verified on the live URL, not just locally

`bash scripts/publish_preview_slots.sh light-colour=light-colour-r2` (tooling
from `origin/preview-slots` @ `4dce3d6c`) replaced the **existing** slot; no
second slot was opened. gh-pages commit `baba2319`:

    git diff --name-only 859cce67..origin/gh-pages | grep -v '^preview/'   -> empty
    changed paths outside preview/light-colour/  -> preview/index.html, preview/slots.json
    sw.js files under preview/                   -> 0
    preview/slots.json: light-colour -> branch light-colour-r2, sha 1aa622c3…
    sibling slot home-r4                         -> still present (333 files)

Live DOM (`preview/light-colour/index.html`, cache-busted):

- captions render **EMS Hub**, **Fire resources**, **City & personnel policies**,
  **Crew links & portals** — one `pfd-cap--ems/fire/admin/util` each, plus the
  neutral mixed-tools caption
- six scene tiles incl. **Drug Calculator** and **Pharmacology**; no SOPs scroller
- contrast re-measured on the published page: card EMS title 14.95, sublabel
  8.08, border 3.75; chips 8.96 / 5.23 / 7.02 / 8.91 / 6.75; captions 5.93 /
  8.31 / 10.35 / 7.63; neutral caption 4.59 — same values as the local build
- dark mode on the live slot vs the live `home-r4` slot, both forced to slate
  with transitions disabled, 12 selectors: **0 differences**

The rebased tip also carries the offline banner (`0763113d`), which home-r4
predates: its JS creates the strip at runtime, so its absence from the static
HTML is expected — the CSS and the override script are both in the build.

## Screenshots (rebased build)

    evidence/rebased-1280-home-light.png   homepage, light, 1280
    evidence/rebased-390-home-light.png    homepage, light, 390
    evidence/rebased-1280-home-dark.png    homepage, slate, 1280
