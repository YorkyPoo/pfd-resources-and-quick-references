"""Add standard Markdown links for drug names across docs/protocols.

Rewritten 2026-11-14: the original version re-linked drug names that already
appeared inside an existing link *destination*, e.g. it turned

    [Atropine](../../pharmacology/Atropine Sulfate.md)

into

    [Atropine](../../pharmacology/[Atropine](../pharmacology/Atropine.md) Sulfate.md)

because its guard only rejected a `[` or `]` immediately adjacent to the name.
Any URL containing a drug name was corrupted. Existing links, images and
inline code spans are now masked out before substitution and restored after,
so the script is idempotent: a second run adds nothing.

  python link_drugs.py            # apply
  python link_drugs.py --dry-run  # report what would change, write nothing
"""
import argparse
import os
import re

DOCS_DIR = r"docs/protocols"
PHARM_PATH = "../pharmacology/"

DRUG_MAP = {
    "epinephrine": "Epinephrine",
    "amiodarone": "Amiodarone",
    "atropine": "Atropine",
    "fentanyl": "Fentanyl",
    "ketamine": "Ketamine",
    "midazolam": "Midazolam",
    "naloxone": "Naloxone",
    "narcan": "Naloxone",
    "ondansetron": "Ondansetron",
    "zofran": "Ondansetron",
    "albuterol": "Albuterol",
    "aspirin": "Aspirin",
    "nitroglycerin": "Nitroglycerin",
    "dextrose": "Dextrose",
    "glucagon": "Glucagon",
    "sodium bicarbonate": "Sodium Bicarbonate",
    "adenosine": "Adenosine",
    "lidocaine": "Lidocaine",
    "magnesium sulfate": "Magnesium Sulfate",
    "calcium chloride": "Calcium Chloride",
    "ipratropium": "Ipratropium",
}

# Spans that must never be edited: existing links/images and inline code.
LINK_RE = re.compile(r"!?\[[^\]]*\]\([^)]*\)")
CODE_RE = re.compile(r"`[^`]*`")
MASK = "\x00{}\x00"


def masker():
    """Return (mask_new, unmask) sharing one span registry.

    Links inserted by an earlier drug pass must be masked before the next
    pass, otherwise the label of the new link is matched again and the text
    ends up as `[[Epinephrine](a)](a)`.
    """
    spans = []

    def mask_new(content):
        def _sub(m):
            spans.append(m.group(0))
            return MASK.format(len(spans) - 1)

        content = CODE_RE.sub(_sub, content)
        content = LINK_RE.sub(_sub, content)
        return content

    def unmask(content):
        for i, original in enumerate(spans):
            content = content.replace(MASK.format(i), original)
        return content

    return mask_new, unmask


def link_drugs(content, pharm_path=PHARM_PATH):
    """Return (new_content, count).

    A line that already links a drug is left completely alone: the existing
    link is authoritative, and a second pass over the same line only produces
    duplicate links (`[Ondansetron](x) ([Ondansetron](x))`) or links the bold
    heading of a pearl instead of its prose.
    """
    changes = 0
    out = []
    for line in content.splitlines(keepends=True):
        mask_new, unmask = masker()
        masked = mask_new(line)
        line_changes = 0
        for drug_lower, proper_name in sorted(DRUG_MAP.items(), key=lambda kv: len(kv[0]), reverse=True):
            target_url = f"{pharm_path}{proper_name.replace(' ', '%20')}.md"
            if f"]({target_url})" in line:
                continue
            for prefix in ["", "*", "**", "`"]:
                for suffix in ["", "*", "**", "`"]:
                    pattern = rf"(?<![\w-]){re.escape(prefix)}{re.escape(drug_lower)}{re.escape(suffix)}(?![\w-])"
                    target = f"{prefix}[{proper_name}]({target_url}){suffix}"
                    masked, count = re.subn(pattern, target, masked, flags=re.IGNORECASE)
                    if count:
                        line_changes += count
                        masked = mask_new(masked)
        changes += line_changes
        out.append(unmask(masked))
    return "".join(out), changes


def pharm_path_for(filepath):
    """Relative path from this protocol page to docs/pharmacology/.

    Hardcoding `../pharmacology/` was wrong for pages two directories deep
    (`docs/protocols/cardiac/x.md` needs `../../pharmacology/`), so every link
    the old script added pointed at a directory that does not exist.
    """
    page_dir = os.path.dirname(os.path.abspath(filepath))
    pharm_dir = os.path.abspath(os.path.join("docs", "pharmacology"))
    return os.path.relpath(pharm_dir, page_dir).replace(os.sep, "/") + "/"


def process_protocols(dry_run=False):
    files_modified = 0
    total_links_added = 0

    print("Adding standard Markdown links for drug names...")

    for root, dirs, files in os.walk(DOCS_DIR):
        for file in sorted(files):
            if not file.endswith(".md"):
                continue
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            new_content, changes = link_drugs(content, pharm_path=pharm_path_for(filepath))
            if changes > 0:
                if not dry_run:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                print(f"  -> {file}: {'would add' if dry_run else 'added'} {changes} links.")
                files_modified += 1
                total_links_added += changes

    print("-" * 40)
    verb = "would modify" if dry_run else "modified"
    print(f"Complete. {verb} {files_modified} files, {'would add' if dry_run else 'added'} {total_links_added} links.")
    return files_modified


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Add standard Markdown links for drug names")
    ap.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    args = ap.parse_args()
    process_protocols(dry_run=args.dry_run)
