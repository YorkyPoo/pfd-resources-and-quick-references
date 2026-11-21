# Bottom bar at 360px — measured, not assumed

Card t_f135bb3f renamed two bottom-bar labels (owner ruling 2026-11-20):
`EMS` → **`Protocols`**, `Fire` → **`SOPs`**. Longer words in the same four equal
cells, so the fit was measured in the built page rather than eyeballed.

## Method

* Built with `mkdocs build --strict` (EXIT=0) on branch `ia-r3`.
* Served from the build output over local HTTP; measured in headless Chrome with
  `Emulation.setDeviceMetricsOverride(width=360, height=740, deviceScaleFactor=2, mobile=True)`
  — i.e. the phone media query (`max-width: 760px`) is the one that applies.
* Read `getBoundingClientRect()` of each `.bbitem`, `.bbtxt`, and a `Range` over the
  label text to count rendered lines; compared `scrollWidth` to `clientWidth` to catch
  truncation.

## Result (page: `/resources/ems.html`)

| label | cell W×H (px) | label box W (px) | lines | scroll>client |
|---|---:|---:|---:|---|
| Home | 90 × 56 | 36.9 | 1 | no |
| **Protocols** | 90 × 56 | **60.5** | 1 | no |
| **SOPs** | 90 × 56 | 34.1 | 1 | no |
| Station | 90 × 56 | 45.2 | 1 | no |

* Bar: `display: flex`, width 360px, height 57px (56px rows + 1px top border).
* Four cells stay **equal width** (90px each = 360/4) and each row is **56px tall**,
  so the 44px minimum hit area still holds with room to spare.
* Widest label is **Protocols at 60.5px inside a 90px cell** (≈86px of usable width
  after the cell's 2px side padding) — **25px of slack, no wrap, no truncation**.
* No horizontal page overflow at 360px (`document.body.scrollWidth == 360`).

The same measurement was repeated on the other renamed pages and on the homepage:
`/resources/fire.html` (`SOPs`), `/resources/fire-resources.html` (`Fire Resources`),
`/ems/index.html`, `/index.html` — all `bodyScrollWidth == innerWidth == 360`.

## Why no abbreviation

`Protocols` fits, so nothing was shortened to fit. If a future label does not fit, the
answer is a measurement recorded here, not a silent abbreviation.
