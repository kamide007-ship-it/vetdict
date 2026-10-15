"""Apply ectoparasite_fungal_treatment_library to diseases_all_species.json.

Usage: python3 -m scripts.template_elimination.fix_ectoparasite_fungal_treatments [--apply]
"""

import json
import sys
from pathlib import Path

from scripts.template_elimination.ectoparasite_fungal_treatment_library import CURATED, is_replaceable

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"


def main(apply: bool) -> int:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    changed = 0
    seen = set()
    for e in data:
        key = (e.get("species"), e.get("name"))
        if key not in CURATED:
            continue
        seen.add(key)
        ja, en = CURATED[key]
        if ja and is_replaceable(e.get("treatment_ja")):
            e["treatment_ja"] = ja
            changed += 1
        if en and is_replaceable(e.get("treatment")):
            e["treatment"] = en
            changed += 1
    missing = set(CURATED) - seen
    print(f"fields replaced: {changed}; library keys not found: {sorted(missing)}")
    if apply:
        JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
