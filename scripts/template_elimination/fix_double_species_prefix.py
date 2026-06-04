"""Fix double-species-prefix artifacts in generated clinical fields.

The first run of ``eliminate_clinical_field_templates.py`` produced phrases
like "猫における猫下部尿路疾患の臨床徴候は..." where the disease name
already contains the species name. The generator has been updated to avoid
this, but existing data still has the artifact. This script trims the
redundant prefix in-place.

It also fixes a couple of generated-content errors:
- ophthalmic templates that mention brachycephalic / specific dog breeds
  appearing on horse / avian / reptile entries.
- musculoskeletal templates that reference dog-specific developmental
  conditions on other species.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    generate_clinical_fields,
)
from scripts.template_elimination.eliminate_clinical_field_templates import (  # noqa: E402
    CLINICAL_FIELDS,
)
from scripts.template_elimination.eliminate_templates import SPECIES_NORM  # noqa: E402

# Species canonical Japanese names — mirror clinical_fields_generator
SP_JA_BY_RAW = {
    "Dog": "犬",
    "Cat": "猫",
    "Horse": "馬",
    "Rabbit": "ウサギ",
    "Hamster": "ハムスター",
    "Guinea Pig": "モルモット",
    "Chinchilla": "チンチラ",
    "Ferret": "フェレット",
    "Hedgehog": "ハリネズミ",
    "Sugar Glider": "フクロモモンガ",
    "Degu": "デグー",
    "Bird": "鳥",
    "Parakeet": "インコ",
    "Parrot": "オウム",
    "Reptile": "爬虫類",
    "Tortoise": "リクガメ",
    "Snake": "ヘビ",
    "Lizard": "トカゲ",
    "Amphibian": "両生類",
    "Fish": "魚",
    "Exotic Other": "その他エキゾチック動物",
}


def fix_double_prefix(text: str, species_ja: str) -> str:
    """Trim "{sp}における{sp}..." to just "{sp}..." when name starts with sp."""
    if not text or not species_ja:
        return text
    prefix = f"{species_ja}における"
    if text.startswith(prefix):
        rest = text[len(prefix) :]
        if rest.startswith(species_ja):
            return rest
    return text


# Mismatched-species sub-template fragments — content that leaks dog/cat
# breed-specific text into other species.
DOG_CAT_BREED_FRAGMENT = "品種特異的素因（短頭種の眼球突出・乾性角結膜炎、コッカースパニエルの白内障、コリーアイ症候群、進行性網膜萎縮の素因犬種）が重要。"
DOG_DEVELOPMENTAL_FRAGMENT = (
    "肥満、過剰運動、不適切な栄養管理（成長期の過剰カロリー・カルシウム）が変性・発達性疾患のリスクを増大させる。"
)


def has_mismatched_breed_content(text: str, species_norm: str) -> bool:
    """True if text contains breed/anatomy content inappropriate for this species."""
    if species_norm in ("dog", "cat"):
        return False
    if DOG_CAT_BREED_FRAGMENT in text:
        return True
    return False


def main() -> None:
    json_path = ROOT / "diseases_all_species.json"
    if not json_path.exists():
        print(f"ERROR: {json_path} not found")
        sys.exit(1)

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    prefix_fixed = 0
    mismatch_regenerated = 0

    for entry in data:
        species_raw = entry.get("species", "")
        species_ja = SP_JA_BY_RAW.get(species_raw, "")
        species_norm = SPECIES_NORM.get(species_raw, species_raw).lower()
        name_ja = entry.get("name_ja", "")
        name_en = entry.get("name", "")
        tagged_cat = entry.get("category", "")

        # Step 1: prefix de-duplication
        for field in CLINICAL_FIELDS:
            v = entry.get(field)
            if not v:
                continue
            new = fix_double_prefix(v, species_ja)
            if new != v:
                entry[field] = new
                prefix_fixed += 1

        # Step 2: regenerate fields containing breed-mismatched content
        mismatched_fields = [f for f in CLINICAL_FIELDS if has_mismatched_breed_content(entry.get(f, ""), species_norm)]
        if mismatched_fields:
            new_content = generate_clinical_fields(species_norm, name_ja, name_en, tagged_cat, mismatched_fields)
            for field, new_text in new_content.items():
                if new_text and new_text != entry.get(field):
                    entry[field] = fix_double_prefix(new_text, species_ja)
                    mismatch_regenerated += 1

    with open(json_path, "w", encoding="utf-8") as f:
        # Compact (no indent): keeps the file under GitHub's 100 MiB blob
        # limit; it is NOT LFS-tracked (read at runtime by the species modules).
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    print(f"Double-prefix fixes: {prefix_fixed}")
    print(f"Mismatched-content regenerations: {mismatch_regenerated}")


if __name__ == "__main__":
    main()
