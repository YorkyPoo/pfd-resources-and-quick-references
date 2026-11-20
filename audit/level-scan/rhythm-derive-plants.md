# Rhythm derivation — planted-defect evidence

Card t_5e96ecb8, branch `rhythm-derive`. Every plant below was made in a throwaway copy of
the worktree (`tar` copy including `.git`), never in the branch, and every copy page was
restored byte-exact afterwards with the copy's own `level_rule.py --check` and
`build_outstanding_decisions.py --check` back at `EXIT=0`.

The defect this card exists to stop: the owner-facing page asked him a level question that
his own standing rule answers — *"If an EMT-I can do it then so can a Paramedic. You just
have to put the lowest provider level and everyone above can do it too."*

## Plant 1 — a row whose own words name the ladder is derived, never asked

Synthetic action row 13 added to `04_Asystole_and_Pulseless_Electrical_Activity_PROC.md`,
no PEMS counterpart, text scoping it to the ladder:

    | 13 | <span class="lvl lvl-emt">EMT</span> | Identify the presenting rhythm category (as determined by EMT-I or P). |

`python3 scripts/level_rule.py --write` → **EXIT=0**. Rendered:

    | 13 | <span class="lvl lvl-i">I</span><sup class="lvl-deriv" title="Provider level derived from the source's own wording: ...">&#8224;</sup> | Identify the presenting rhythm category (as determined by EMT-I or P). |

- chip `I` (the lowest level the ladder names), `lvl-deriv` dagger present, **no** `lvl-own` flag
- `python3 scripts/build_outstanding_decisions.py --print` → **EXIT=0**, and row 13 does
  **not** appear under "Needs your level decision" (headline stayed `2 rows`, the two PEEP
  rows owned by the other card)
- `python3 scripts/level_rule.py --check` → **EXIT=1**, on an unrelated rule: the planted row
  still *prints* the level words `(as determined by EMT-I or P)` in its action text and has no
  `kept`/`removed` record in `token-decisions.yaml`. That is the existing level-word-in-text
  gate, not a failure of the derivation; it is why the two real rows cite the ladder from the
  PEMS row's own words instead of restating it on the page.

## Plant 2 — a bundled row scoped by a sub-clause ladder still reaches the owner

Bundling initiation and titration back into one row on the Asthma page, where the titration
half is scoped `I/P only:` (a colon — it governs one clause, not the whole row):

    | 8a | ... &#9873;</sup> | **CPAP:** initiate 5 cm H₂O. I/P only: Titrate PEEP up to **10 cm H₂O** to support ventilation and work of breathing. |

- `python3 scripts/level_rule.py --write` → **EXIT=0**, row keeps `lvl-own`, gains **no** dagger
- `python3 scripts/build_outstanding_decisions.py --print` → **EXIT=0**, row 8a is **still
  under "Needs your level decision"**, headline unchanged at `2 rows`

So the derivation does not swallow a bundle conflict: `derivable_floor()` ignores a ladder that
only scopes a sub-clause, and `auto_derived()` additionally refuses when the printed badge is
not the derived floor.

## Backstop — the generator refuses to publish the false question

With the same bundled row's flagged shape but a **whole-row** ladder in its text, the row was
still `OWNER_REQUIRED` in the ledger while its words answered the question. The generator
refused to write the page:

    REFUSING to publish a level question the ladder rule already answers:
      - protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.md row 8a: the source scopes
        this action to "I/P", so the level is the lowest it names (I); the row is still
        published as a question
    EXIT=1

That guard is `ladder_answered_questions()` in `scripts/build_outstanding_decisions.py`; it
imports `derivable_floor` from `level_rule.py` so the writer and the checker cannot drift.

## Restore

Each copy ended with `level_rule.py --write` → `EXIT=0`, `level_rule.py --check` → `EXIT=0`,
`build_outstanding_decisions.py --check` → `EXIT=0`, and both edited pages byte-identical to
their pre-plant content.
