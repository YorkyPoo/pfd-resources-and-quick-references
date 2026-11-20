# Preview slots — /preview/&lt;slot&gt;/

**Preview created 2026-11-19. Tear down by 2026-11-26.**

Index: <https://yorkypoo.github.io/pfd-resources-and-quick-references/preview/>

## Why slots

`/preview/` used to be a **single slot**: every card republished it from its own
branch, so each republish wiped the other card's pages and each reviewer then
blocked for "the preview does not show my change." That is a block loop, not a
defect. Now each branch gets its own subpath:

```
/preview/                 ← index: slot, description, branch @ short SHA, build time
/preview/<slot>/          ← one branch/commit, never overwritten by another card
```

A slot is only replaced when someone explicitly republishes that slot.

## Publish a slot (from the repo root)

```bash
# every slot is built from its branch's OWN tip commit in a throwaway worktree
bash scripts/publish_preview_slots.sh \
    pilot=pilot-references-block \
    relabel=provider-level-letters
```

- Writes only the `preview/` subtree of `gh-pages`; the live root is untouched.
- Never pushes `main` (a `main` push force-runs `mkdocs gh-deploy`, which would
  deploy to the live root **and** wipe `preview/`).
- Slots not named on the command line are left alone.
- Provenance (branch, full sha, build timestamp) is recorded in
  `preview/slots.json` and rendered into `preview/index.html`.

## Remove one slot

```bash
bash scripts/preview_slot_teardown.sh pilot    # one slot; index regenerates
bash scripts/preview_slot_teardown.sh --all    # whole /preview/ subtree
```

Teardown refuses to touch anything that is not a real `preview/<slot>/`
directory, so it cannot remove the live root or another card's slot.

## Local build (no publish)

```bash
bash scripts/build_preview.sh <slot>     # -> site_preview/<slot>/
```

## Preview-only deltas

`scripts/build_preview_cfg.py --slot <slot>` derives `mkdocs.preview.<slot>.yml`
from `mkdocs.yml` — there is no hand-copied second config. Per slot:

| Setting | Preview value |
|---|---|
| `site_url` | `.../pfd-resources-and-quick-references/preview/<slot>/` |
| `site_dir` | `site_preview/<slot>/` |
| service worker / offline plugin | **disabled** (no `sw.js`, no registration) |
| web manifest | removed from the output |
| robots | `<meta name="robots" content="noindex, nofollow">` on every page |
| `preview/<slot>/robots.txt` | `User-agent: *` / `Disallow: /` |

**Service worker is deliberately absent in every slot.** Two workers on the same
origin (even one registered under `/preview/`) can serve stale protocol levels
to the owner's phone and can influence the live site's cache. Offline access is
not needed for draft review.

## Hazard: a push to `main` wipes every slot

`.github/workflows/deploy.yml` runs `mkdocs gh-deploy --force` on every push to
`main`. That force-pushes `gh-pages` from `main`, which (a) deploys `main` to
the live root and (b) deletes `preview/`. Until the owner rules on the
corrections, do **not** push `main`. If slots are wiped this way, re-run the
publish command above.

## Legacy single-slot teardown script

`audit/level-scan/preview-teardown.sh` still exists and removes the whole
`preview/` subtree (`preview_slot_teardown.sh --all` does the same thing). Use
the per-slot script for day-to-day work.
