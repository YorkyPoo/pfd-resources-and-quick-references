# /preview/ duplicate — expiry 2026-11-26

**Preview created 2026-11-19. Tear down by 2026-11-26.**

URL: <https://yorkypoo.github.io/pfd-resources-and-quick-references/preview/>

## What this is

A full duplicate of the site, built from `main` at `d4eca8d` (the A1 level
corrections), served under the `/preview/` subpath of the same GitHub Pages
project. It exists so the owner can review the corrections on any device
without deploying `main` to the live root.

The live root (`https://yorkypoo.github.io/pfd-resources-and-quick-references/`)
is **unchanged** — it still carries the older deployment from `main` `2cf1f4f`.

## Why it expires

A preview is a second source of truth. Left up, someone reads last week's
levels off it on a call. Delete it by **2026-11-26**.

## Teardown (one command)

From the repo root:

```bash
bash audit/level-scan/preview-teardown.sh
```

That removes `gh-pages/preview/`, commits, and pushes. It does not touch the
live root.

## Rebuilding

The preview config is derived from `mkdocs.yml`, so it cannot drift from the
live nav/content config. From the repo root:

```bash
source /root/pfd-ssg-env/bin/activate   # or any env with mkdocs-material
bash scripts/build_preview.sh           # -> site_preview/
# then copy site_preview/ into gh-pages/preview/ and push, as done on 2026-11-19
```

Preview-only deltas (all applied by `scripts/build_preview_cfg.py` and the
`overrides_preview/` theme override):

| Setting | Preview value |
|---|---|
| `site_url` | `.../pfd-resources-and-quick-references/preview/` |
| `site_dir` | `site_preview/` |
| service worker / offline plugin | **disabled** (no `sw.js`, no registration) |
| web manifest | removed from the preview output |
| robots | `<meta name="robots" content="noindex, nofollow">` on every page |
| `preview/robots.txt` | `User-agent: *` / `Disallow: /` |

**Service worker is deliberately absent.** Two workers on the same origin
(even one registered under `/preview/`) can serve stale protocol levels to the
owner's phone and can influence the live site's cache. Offline access is not
needed for draft review.

## Hazard: a push to `main` wipes this preview

`.github/workflows/deploy.yml` runs `mkdocs gh-deploy --force` on every push to
`main`. That force-pushes `gh-pages` from `main`, which (a) deploys `main` to
the live root and (b) deletes `preview/`. Until the owner rules on the
corrections, do **not** push `main`. If the preview is wiped this way, re-run
the rebuild steps above.
