#!/usr/bin/env python3
"""Build one preview slot from the checkout it is run in.

    python3 scripts/build_preview_slot.py --slot pilot [--repo PATH]

Derives mkdocs.preview.<slot>.yml from mkdocs.yml (scripts/build_preview_cfg.py)
and builds into <repo>/site_preview/<slot>/. Then asserts the preview safety
properties every slot must keep:

  * no service worker (sw.js) in the output
  * slot-level robots.txt that disallows everything
  * index.html present

Exit code is non-zero if any of those fail, so a broken slot never gets shipped.
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def find_mkdocs(repo: str) -> str:
    for cand in (
        os.environ.get("MKDOCS"),
        "/root/pfd-ssg-env/bin/mkdocs",
    ):
        if cand and os.path.exists(cand):
            return cand
    return "mkdocs"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slot", required=True)
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    slot = args.slot

    cfg_out = os.path.join(repo, f"mkdocs.preview.{slot}.yml")
    subprocess.run(
        [sys.executable, os.path.join(HERE, "build_preview_cfg.py"),
         "--slot", slot, "--repo", repo, "--config-out", cfg_out],
        check=True,
    )

    site_dir = os.path.join(repo, "site_preview", slot)
    if os.path.isdir(site_dir):
        import shutil
        shutil.rmtree(site_dir)

    mkdocs = find_mkdocs(repo)
    subprocess.run([mkdocs, "build", "-f", cfg_out], cwd=repo, check=True)

    print(f"---- preview slot checks: {slot} ----")
    failures = []
    if os.path.exists(os.path.join(site_dir, "sw.js")):
        failures.append("site_preview/%s/sw.js exists (service worker must be off)" % slot)
    robots = os.path.join(site_dir, "robots.txt")
    if not os.path.exists(robots):
        failures.append("site_preview/%s/robots.txt missing" % slot)
    else:
        with open(robots, encoding="utf-8") as fh:
            body = fh.read()
        print(body.strip())
        if "Disallow: /" not in body:
            failures.append("robots.txt does not disallow everything")
    if not os.path.exists(os.path.join(site_dir, "index.html")):
        failures.append("site_preview/%s/index.html missing" % slot)

    if failures:
        for f in failures:
            print("FAIL:", f, file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: slot {slot} built at {site_dir} (no sw.js, robots Disallow:/, index.html present)")


if __name__ == "__main__":
    main()
