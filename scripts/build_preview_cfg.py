#!/usr/bin/env python3
"""Derive mkdocs.preview.yml from mkdocs.yml.

Keeping the preview config derived (not a hand-copied duplicate) means the
preview cannot drift from the live nav/content config. The only deltas are:
  * site_url  -> .../preview/
  * site_dir  -> site_preview
  * theme.custom_dir -> overrides_preview (no SW registration, unconditional noindex)
  * plugins   -> search only (no offline plugin)
  * hooks     -> drop mkdocs_post_build.py (which generates sw.js), add
                 scripts/mkdocs_preview.py
"""
import yaml

with open("mkdocs.yml", encoding="utf-8") as fh:
    cfg = yaml.safe_load(fh)

cfg["site_url"] = "https://yorkypoo.github.io/pfd-resources-and-quick-references/preview/"
cfg["site_dir"] = "site_preview"
cfg.setdefault("theme", {})["custom_dir"] = "overrides_preview"
cfg["plugins"] = ["search"]

hooks = [h for h in cfg.get("hooks", []) if not h.endswith("mkdocs_post_build.py")]
if "scripts/mkdocs_preview.py" not in hooks:
    hooks.append("scripts/mkdocs_preview.py")
cfg["hooks"] = hooks

with open("mkdocs.preview.yml", "w", encoding="utf-8") as fh:
    yaml.safe_dump(cfg, fh, sort_keys=False, allow_unicode=True, width=4096)

print("wrote mkdocs.preview.yml (site_url=/preview/, plugins=[search], "
      "post_build SW hook removed)")
