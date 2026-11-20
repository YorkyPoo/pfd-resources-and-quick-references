# Card t_041a6f40 — front-matter-2 — planted-defect evidence

Branch `front-matter-2`, content commit `8ab0d3d` (base `front-matter-effective` `e389a49`).
Guard: `scripts/internal_artifacts.py` — a front-matter page fails when `OMD` /
`Operational Medical Director` / `Medical Director` sits within 60 characters of an
approval-family word (`approv*`, `adopt*`, `endors*`, `signed`, `signing`, `signature`).

## 1. Guard passes on the shipped tree

```
$ python3 scripts/internal_artifacts.py --check
OK — no conversion QA reports, no replacement-mapping block under docs/, no effective date or OMD approval claim on a front-matter page, and no built page for an excluded source
EXIT=0
```

## 2. Plant 1 — the Pending line put back (header block)

```
$ python3 scripts/internal_artifacts.py --check
FAIL — 1 internal conversion artifact(s) published under docs/
 - protocols/front-matter/00 - Introduction.md:5  [omd-approval-claim] es, and Procedures **Pending approval by:** Poquoson Fire and Rescue Operational Medical Director (OMD) --
EXIT=1
```

## 3. Plant 2 — the old acknowledgement sentence put back (line 21)

```
$ python3 scripts/internal_artifacts.py --check
FAIL — 1 internal conversion artifact(s) published under docs/
 - protocols/front-matter/00 - Introduction.md:21  [omd-approval-claim] ve been adopted, adapted, and approved by the Poquoson Fire and Rescue Operational Medical Director to serve
EXIT=1
```

## 4. Both plants removed — guard green again

```
$ python3 scripts/internal_artifacts.py --check
OK — no conversion QA reports, no replacement-mapping block under docs/, no effective date or OMD approval claim on a front-matter page, and no built page for an excluded source
EXIT=0
```

## What the guard deliberately does not fire on

The Scope of Practice sentence stays:

> These protocols apply exclusively to EMS providers operating under the medical direction of the Poquoson Fire and Rescue OMD.

It names the OMD as the source of medical *direction* — who the document applies to — not
as an approver. No approval-family word sits within 60 characters of the mention, so it
passes. The Goals bullet ("To ensure an accountability structure for our Operational
Medical Director…") is likewise untouched and passes.

## Other acceptance greps

```
$ grep -n "approved by" docs/protocols/front-matter/*.md
(no output)
EXIT=1  # grep: no match
```
