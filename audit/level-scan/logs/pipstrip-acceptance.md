# Pip strip — acceptance evidence

Branch `pilot-pipstrip` (rebased onto `pilot-references-block` 6ff8706). The
exact tip is the first line of `audit/level-scan/logs/pipstrip-gates.txt` and
the `sha` for slot `pilot` in `preview/slots.json`.
Preview slot: <https://yorkypoo.github.io/pfd-resources-and-quick-references/preview/pilot/>
Built from that one branch tip; `main` and `origin/main` untouched (9818904 / 2cf1f4f).

## 1. Reference file

    $ wc -c audit/level-scan/reference/protocol-format-sample.html
    12492 audit/level-scan/reference/protocol-format-sample.html

Copied from the owner's cache, committed, not shipped (`audit/` is outside `docs/`),
not linked from the nav.

## 2. Mapper reproduces all ten prototype rows

`python3 scripts/test_pip_strip_mapper.py` — parses the prototype's own `s:[…]`
arrays, inverts them to `{min_level, mc_required}`, runs the real mapper forward
and diffs. EXIT=0.

     1  min=R      go,go,go,go,go             ok
     5  min=B      no,go,go,go,go             ok
     6  min=A      no,no,go,go,go             ok
     8  min=I      no,no,no,go,go             ok
     9  min=I +MC  no,no,no,call,go           ok
    10  MC chip    call,call,call,call,call   ok
    …10/10 rows reproduce; header R B A I P (prototype still prints 1 2 3 4 5)

## 3. Both pages on /preview/pilot/, one branch tip

Cold Exposure and Pulmonary Edema both render the block; a third protocol page
(`cardiac/04_Asystole…`) still carries the old `lv-wrap` table and no
`data-pip-block`, i.e. the transform is scoped to the two pilot pages
(`PILOT_PAGES` in `scripts/mkdocs_pip_strip.py`).

## 4. Fetched from the live preview URL

`audit/level-scan/logs/pipstrip-live-evidence.txt` — verbatim `curl` output for:
the six picker buttons (`Show all` `aria-pressed="true"`), the strip header
`<i>R</i><i>B</i><i>A</i><i>I</i><i>P</i>`, row 1's tag `standing from R`, and
the tally line.

`python3 scripts/verify_pip_strip.py --base https://…/preview/pilot/` → EXIT=0.

## 5. Tally line, Show all (server-rendered, JS off)

    Cold:      Show all — 7 actions. … tap a level to see this protocol as you.
    Pulmonary: Show all — 10 actions. … · 1 level unverified ⚑

Tapped state (measured in the browser, level B on Pulmonary):

    B: of 10 actions on this protocol — 5 standing, 1 need Medical Control,
    3 not permitted (dimmed). 1 level unverified ⚑.

## 6. Flagged rows, from code

    Cold Exposure         7 rows, 0 OWNER_REQUIRED
    Pulmonary Edema      10 rows, 1 OWNER_REQUIRED (row 9, CPAP titration)

That row renders an outline-only dashed strip (no solid fill anywhere) and the
⚑ marker survives; it is counted in its own tally bucket and never in
"standing" or "not permitted".

## 7. Gates (all on the same tree — its hash opens the gate log)

    verify_pems_canonical EXIT=0
    level_rule            EXIT=0
    mc_wording            EXIT=0
    mkdocs build --strict EXIT=0
    mapper test           EXIT=0

Full log: `audit/level-scan/logs/pipstrip-gates.txt`.

## 8. Action column width — measured in the browser, 390 × 844, DPR 2

Same page, same viewport, `td.getBoundingClientRect().width`:

    new strip table : [24, 279, 86]  → action column 279px
    How-to-Read matrix : [28, 180, 51, 50, 36, 36, 36] → action column 180px

279px beats 180px by 99px (+55%). `document.scrollWidth = 390` — no horizontal
scroll at 390px or at 320px (action column 209px there).

The table reclaims the 16px page gutter each side (`margin: 0 -0.8rem` on
`.pip-wrap`) — without it the action column measures 247px, which still beats
the matrix but misses the 259px the prototype asked for.
