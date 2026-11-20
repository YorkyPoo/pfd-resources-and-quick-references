# AI formatting guidelines excluded from the published site

Card `t_501bd6b4`. Owner ruling 2026-11-20: *"That adds friction. Exclude it."*

`docs/protocols/front-matter/00 - AI Formatting Guidelines.md` is the conversion
build prompt, not clinical content. It was publicly served as **"MASTER AI SYSTEM
PROMPT: Poquoson Fire and Rescue Protocols"** from the front-matter path. A medic
scrolling front matter lands on an AI prompt.

## What changed

| item | change |
|---|---|
| source file | **kept** in `docs/` — it is the conversion spec and must not be deleted |
| `mkdocs.yml` | `exclude_docs` now lists the file; no HTML page is produced |
| `nav` | the page was already absent from `nav` (grep found no entry); MkDocs builds every `.md` under `docs/`, so nav absence alone was not enough |
| `scripts/internal_artifacts.py` | new `--site` check: fails if a built page exists for an excluded source. It checks both `<stem>.html` (`use_directory_urls: false`) and `<stem>/index.html` |
| replacement mapping | confirmed absent from every other page (`grep -rn "Mandatory Text Replacements" docs/` → 0 hits) |
| inbound links | none. `grep -rn "AI Formatting\|AI%20Formatting\|00 - AI" docs/` → 0 hits, so nothing 404s |

The preview config (`scripts/build_preview_cfg.py`) is derived from `mkdocs.yml`,
so the exclusion applies to previews too without a second edit.

## Guard proof

Pre-fix built tree (`site/`, still carrying the page):

```
$ python3 scripts/internal_artifacts.py --check --site site
FAIL — 1 internal conversion artifact(s) published under docs/
 - protocols/front-matter/00 - AI Formatting Guidelines.html  [excluded-page-built] protocols/front-matter/00 - AI Formatting Guidelines.md
EXIT=1
```

Fixed build (`build-fix-ai-063928`, `mkdocs build --strict` EXIT=0):

```
$ python3 scripts/internal_artifacts.py --check --site build-fix-ai-063928
OK — no conversion QA reports, no replacement-mapping block under docs/, and no built page for an excluded source
EXIT=0
```

The strict build produced 280 pages, down from 281; `find … -path "*front-matter*"`
lists only Introduction, How to Read the Protocols, and Universal Patient Care.

## Gates

Full tails in `gates.txt`.

| gate | EXIT |
|---|---:|
| `mkdocs build --strict` | 0 |
| `scripts/internal_artifacts.py --check --site <build>` | 0 |
| `scripts/link_sweep.py <build>` | 0 — 280 pages, 71,585 internal hrefs, clean |
| `scripts/verify_pems_canonical.py` | 0 |
| `scripts/level_rule.py --check` | 0 |
| `scripts/mc_wording.py --check` | 0 |
| `scripts/agency_names.py --check` | 0 |
| `scripts/internal_artifacts.py --check` | 0 |

`link_sweep.py` against the *preview* build reports 246 broken paths, all from
`404.html`. That is the sweep's fixed `/pfd-resources-and-quick-references/`
prefix meeting the preview's `/preview/` site_url; it is a pre-existing preview
artifact, not a link introduced here. The live-config build is clean.

## Preview

Slot: `/preview/ai-prompt-exclusion/` — published on `gh-pages`; `main` untouched.
