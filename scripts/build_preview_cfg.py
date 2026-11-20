#!/usr/bin/env python3
"""Derive a per-slot preview MkDocs config from mkdocs.yml.

The preview config is always derived (never a hand-copied second config), so a
preview slot cannot drift from the live nav/content config. One config file is
written per slot because each slot carries its own site_url and site_dir:

    mkdocs.preview.<slot>.yml
    site_url: .../preview/<slot>/
    site_dir: site_preview/<slot>

Other deltas vs the live config:
  * theme.custom_dir -> overrides_preview (no SW registration, unconditional noindex)
  * plugins   -> search only (no offline plugin)
  * hooks     -> drop mkdocs_post_build.py (which generates sw.js), add
                 scripts/mkdocs_preview.py

Usage:
    python3 scripts/build_preview_cfg.py --slot pilot
    python3 scripts/build_preview_cfg.py --slot relabel --site-url https://.../preview/relabel/
"""
import argparse
import os
import re
import yaml

BASE_URL = "https://yorkypoo.github.io/pfd-resources-and-quick-references/preview/"


def valid_slot(name: str) -> str:
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,31}", name):
        raise SystemExit(f"error: invalid slot name {name!r} (lowercase a-z, 0-9, _-)")
    return name


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slot", required=True, help="slot name, e.g. pilot")
    ap.add_argument("--site-url", default=None,
                    help="override site_url (default .../preview/<slot>/)")
    ap.add_argument("--repo", default=".", help="repository root (default: cwd)")
    ap.add_argument("--config-out", default=None,
                    help="config path (default <repo>/mkdocs.preview.<slot>.yml)")
    args = ap.parse_args()

    slot = valid_slot(args.slot)
    repo = os.path.abspath(args.repo)
    src = os.path.join(repo, "mkdocs.yml")
    with open(src, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)

    cfg["site_url"] = args.site_url or f"{BASE_URL}{slot}/"
    cfg["site_dir"] = f"site_preview/{slot}"
    cfg.setdefault("theme", {})["custom_dir"] = "overrides_preview"
    cfg["plugins"] = ["search"]

    hooks = [h for h in cfg.get("hooks", []) if not h.endswith("mkdocs_post_build.py")]
    if "scripts/mkdocs_preview.py" not in hooks:
        hooks.append("scripts/mkdocs_preview.py")
    cfg["hooks"] = hooks

    out = args.config_out or os.path.join(repo, f"mkdocs.preview.{slot}.yml")
    with open(out, "w", encoding="utf-8") as fh:
        yaml.safe_dump(cfg, fh, sort_keys=False, allow_unicode=True, width=4096)

    print(f"wrote {out} (slot={slot}, site_url={cfg['site_url']}, "
          f"site_dir={cfg['site_dir']}, plugins=[search], SW hook removed)")


if __name__ == "__main__":
    main()
