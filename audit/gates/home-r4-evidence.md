# home-r4 gate evidence — card t_a2f382dd

Runner: `audit/gates/run_gates_home_r4.sh` (18 gates; the 16 of the ia-r3 floor plus
`naming_sweep` and `protocols_untouched`). Log: `audit/gates/home-r4-<sha>.log`.

## Result on the content commit

17 of 18 EXIT=0, including every gate this card names in its acceptance:

| gate | exit |
|---|---|
| gen_resource_pages (`--check`, drift none) | 0 |
| mkdocs_strict (`mkdocs build --strict`) | 0 |
| link_sweep | 0 |
| hub_anchors | 0 |
| bottom_bar | 0 |
| scroller_hrefs | 0 |
| naming_sweep (no "Drugs & Drip" / "Medications & Calculators") | 0 |
| protocols_untouched | 0 |
| the other eight content gates | 0 |
| **level_rule** | **1 — pre-existing on `main`, not this branch** |

## level_rule is red on main before this card touches anything

`git worktree add --detach /tmp/main-check ebb1efb4` (the `main` tip this branch was cut
from), then `python3 scripts/level_rule.py --check` → **EXIT=1**, and the failure text is
byte-identical to the one on home-r4 (md5 of the last 900 bytes of both outputs:
`c65ca9d0e73d5d37d5b67807b514379e`):

```
audit/level-scan/level-rule-ledger.md != what emit_md() derives from level-rule-ledger.json
  -63 `sc-wrap` block(s) in 46 file(s) ... Provider-level matrices inside `sc-wrap`: 1
  - - protocols/front-matter/01 - How to Read the Protocols.md (line 34)
  +62 `sc-wrap` block(s) in 45 file(s) ... Provider-level matrices inside `sc-wrap`: 0
```

Cause: the committed ledger md still records the front-matter "How to Read the Protocols"
legend as still inside an `sc-wrap` provider-level matrix; the page no longer has one.
`docs/protocols/` is untouched by home-r4 (`protocols_untouched` gate = 0 files changed),
so this is inherited from `main` — most likely the `howto-pipstrip` merge (d4893ca5)
editing that page without a `scripts/level_rule.py --write` to follow. Fixing it means
regenerating `audit/level-scan/level-rule-ledger.md`, which is a protocol-front-matter
audit trail, not homepage work — left for its own card.

## verify_pems_canonical needs a local cache, not content

Its first run on this fresh worktree failed on `.cache/pems_rows.jsonl exists` — a
gitignored PDF-parse cache (`audit/level-scan/.cache/`, note `.gitignore:27`), absent in
any new worktree. With that cache copied in, **EXIT=0, all invariants hold**. Nothing in
this card's diff is involved.
