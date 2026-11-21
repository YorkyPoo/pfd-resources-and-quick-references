# IA round 3 — guards, planted defects, and what each one proves

Card t_f135bb3f. Every guard added or relied on for this card was proved able to FAIL by
planting the defect it is meant to catch. A gate that cannot fail is decoration.

Runner: `audit/gates/run_gates_ia_r3.sh` → `audit/gates/ia-r3-2ccf3bb.log` (15/15 EXIT=0).
Planted-defect log: `~/.hermes/cache/scratch/ia-r3-plants.log`.

| # | planted defect | guard | observed |
|---|---|---|---|
| 1 | `EMS_ORDER` has Procedures **below** Pharmacology | assert in `scripts/gen_resource_pages.py` | `EMS_ORDER: Procedures must stay above Pharmacology (owner ruling)` EXIT=1 |
| 2 | one static button points at `#cardiology` (no such heading) | `build_hub()` anchor validation vs the headings actually generated | `EMS_BUTTONS point at headings that do not exist: ['#cardiology']` EXIT=1 |
| 3 | two chips in one `.qljump` row share `#frameworks` | `scripts/check_scroller_hrefs.py` | `resources/fire-resources.html .qljump ['#frameworks']` EXIT=1 |
| 4 | bottom-bar label reverted `Protocols` → `EMS` | `scripts/check_bottom_bar.py` | `labels are ['Home','EMS','SOPs','Station'], expected [... 'Protocols' ...]` EXIT=1 |
| 5 | a protocol page changes | `protocols_untouched` gate: `git diff --name-only origin/main..HEAD -- docs/protocols/ \| wc -l` | this branch prints **0**; the same command over a range that does contain protocol work prints **114**, so the check is capable of being non-zero |
| 6 | the Protocols `Pediatric` button re-pointed at `#pediatric` (no such heading on the rendered page) | `scripts/check_hub_anchors.py` on the built site (plant rebuilt with `mkdocs build`, not a hand-edited HTML file) | `resources/ems.html .qldots [Pediatric] -> #pediatric (no such id on this page)` EXIT=1 — `mkdocs build --strict` itself stayed green, which is why this gate exists |

Plant 6 is the card t_5b03da25 guard: `check_hub_anchors.py` resolves every control in
`.qldots` / `.qljump` / `.pfd-scroller` against the **rendered** page (same-page `#frag`
must be an `id` in that document; `page.html#frag` must find the page and the id on it).
The pre-build sibling guard in `build_hub()` compares `EMS_BUTTONS` against the headings
it is about to emit; planted the same way it prints
`EMS_BUTTONS point at headings that do not exist on the Protocols page: Pediatric -> #pediatric`
EXIT=1. Both name the button **and** the anchor, as the card requires.

Plant 3 needed a second attempt: a blind `href="#strategies"` replace hit the **sidebar
nav** link first (3 occurrences in the page), so nothing was planted in the chip row and
the check correctly passed. The plant now targets `<a href="#strategies">Strategies</a>`
inside the row. Recorded here because a green gate after a no-op plant is worse than no
gate at all.

Gate runner bug caught by the first run: `gen_connected_notes.py` documented a `--check`
mode in its docstring but never implemented it (argparse exited 2). `--check` now exists
(exit 1 on drift, evaluates porter-owned pages, writes nothing), which is what keeps the
renamed "Browse the rest of this side" labels from silently rotting on 29 SOP pages.
