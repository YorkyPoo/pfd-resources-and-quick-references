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
    "ipratropium": "Ipratropium"
}

def process_protocols():
    sorted_drugs = sorted(DRUG_MAP.keys(), key=len, reverse=True)
    
    files_modified = 0
    total_links_added = 0

    print("Adding standard Markdown links for drug names...")

    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                changes = 0
                
                # Process each drug from longest to shortest
                for drug_lower, proper_name in DRUG_MAP.items():
                    # Pattern: match the drug name case-insensitively, but NOT if:
                    # - preceded by [ or [[ (already a link start)
                    # - followed by ] or ]( (already a link end)
                    # - preceded by </ (HTML tag end)
                    # Use a more flexible boundary that handles **word** formatting
                    
                    # Build regex that captures optional surrounding ** or * or ` 
                    # and ensures we're not inside a markdown link
                    
                    # Match: (optional formatting)(drug name)(optional formatting)
                    # where the whole thing is not inside [...] or (...)
                    
                    # Simple approach: replace specific patterns
                    for prefix in ['', '*', '**', '`']:
                        for suffix in ['', '*', '**', '`']:
                            pattern = rf"(?<![\[\]]){re.escape(prefix)}({re.escape(drug_lower)}){re.escape(suffix)}(?![\]\(\[])"
                            
                            def replacer(m, pname=proper_name, p=prefix, s=suffix):
                                return f"{p}[{pname}]({PHARM_PATH}{pname.replace(' ', '%20')}.md){s}"
                            
                            new_content, count = re.subn(pattern, replacer, content, flags=re.IGNORECASE)
                            if count > 0:
                                content = new_content
                                changes += count
                
                if changes > 0:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  -> {file}: Added {changes} standard links.")
                    files_modified += 1
                    total_links_added += changes

    print("-" * 40)
    print(f"Complete. Modified {files_modified} files, added {total_links_added} links.")

if __name__ == "__main__":
    process_protocols()
