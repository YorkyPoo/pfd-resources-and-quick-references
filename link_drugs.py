import os
import re

# The directory where your MkDocs markdown files live.
DOCS_DIR = r"docs/protocols"

# A dictionary mapping lowercase text found in the protocols to the exact Wiki-Link name.
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
    "ipratropium": "Ipratropium"
}

def process_protocols():
    sorted_drugs = sorted(DRUG_MAP.keys(), key=len, reverse=True)
    escaped_drugs = [re.escape(drug) for drug in sorted_drugs]
    pattern_string = r"(?<!\[)\b(" + "|".join(escaped_drugs) + r")\b(?!\])"
    regex = re.compile(pattern_string, re.IGNORECASE)
    
    files_modified = 0
    total_links_added = 0

    print("Initiating Pharmacology Wiki-Link Patcher...")

    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                def replace_func(match):
                    matched_text = match.group(1).lower()
                    proper_link_name = DRUG_MAP[matched_text]
                    return f"[[{proper_link_name}]]"

                new_content, subs_made = regex.subn(replace_func, content)

                if subs_made > 0:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"  -> {file}: Added {subs_made} links.")
                    files_modified += 1
                    total_links_added += subs_made

    print("-" * 40)
    print(f"Run Complete. Added {total_links_added} links across {files_modified} files.")

if __name__ == "__main__":
    process_protocols()
