"""Apply blood-disorder subtype-specific content to existing entries.

After ``gen_blood_disorder`` was added with detailed subtype branches
(estrogen-induced AA, neonatal isoerythrolysis, EIA, hemoplasmosis, HUS,
iron deficiency, conure hemorrhagic), some entries that already had generic
blood-disorder content (from a prior pass) need to be upgraded.

This script:
1. Iterates all entries whose name_ja contains a blood-disorder keyword
2. Routes through ``generate_content()`` to get the (possibly subtype-specific) output
3. If the new generator output is meaningfully different from the existing
   content AND the existing content lacks the subtype-specific markers,
   replaces it.

This is idempotent: re-running won't disturb entries whose content already
matches a subtype.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.template_content_library import generate_content  # noqa: E402

SPECIES_NORM = {
    "Bird": "bird",
    "Parakeet": "parakeet",
    "Parrot": "parrot",
    "Horse": "horse",
    "Guinea Pig": "guinea_pig",
    "Rabbit": "rabbit",
    "Chinchilla": "chinchilla",
    "Hedgehog": "hedgehog",
    "Snake": "snake",
    "Lizard": "lizard",
    "Amphibian": "amphibian",
    "Sugar Glider": "sugar_glider",
    "Degu": "degu",
    "Reptile": "reptile",
    "Exotic Other": "exotic_other",
    "Hamster": "hamster",
    "Ferret": "ferret",
    "Tortoise": "tortoise",
    "Fish": "fish",
    "Cat": "cat",
    "Dog": "dog",
}

# Subtype markers — when present in name_ja, indicate the entry deserves the specific
# subtype branch. The matching unique fingerprint in the generated content tells us
# whether the existing content already uses the subtype.
SUBTYPE_FINGERPRINTS = [
    # (name keyword, fingerprint in generated content)
    ("エストロゲン", "エストロゲン誘発性再生不良性貧血"),
    ("高エストロゲン", "エストロゲン誘発性再生不良性貧血"),
    ("新生子溶血", ("FNI", "新生駒")),
    ("新生児溶血", ("FNI", "新生駒")),
    ("馬伝染性貧血", "EIA、Equine Infectious Anemia"),
    ("EIA", "EIA、Equine Infectious Anemia"),
    ("ヘモプラズマ", "Mycoplasma haemofelis"),
    ("haemominutum", "Mycoplasma haemofelis"),
    ("haemofelis", "Mycoplasma haemofelis"),
    ("伝染性貧血", "EIA"),  # may match either feline or equine
    ("感染性貧血", "Mycoplasma haemofelis"),
    ("溶血性尿毒症", "溶血性尿毒症症候群（HUS）の治療"),
    ("HUS", "溶血性尿毒症症候群（HUS）の治療"),
    ("鉄欠乏", "鉄欠乏性貧血の治療"),
    ("コニュア", "コニュア出血症候群（Conure Bleeding Syndrome"),
]


def _has_subtype_fingerprint(text: str, fingerprint) -> bool:
    if isinstance(fingerprint, tuple):
        return any(fp in text for fp in fingerprint)
    return fingerprint in text


def _has_subtype_name(name: str) -> str | None:
    """Return the first matching subtype keyword if any."""
    for kw, _ in SUBTYPE_FINGERPRINTS:
        if kw in name:
            return kw
    return None


def _needs_upgrade(name_ja: str, current_tx: str) -> bool:
    """True if the entry name indicates a subtype but the current text doesn't include the fingerprint."""
    if not name_ja or not current_tx:
        return False
    matched_fingerprint = None
    for kw, fp in SUBTYPE_FINGERPRINTS:
        if kw in name_ja:
            matched_fingerprint = fp
            break
    if matched_fingerprint is None:
        return False
    return not _has_subtype_fingerprint(current_tx, matched_fingerprint)


def upgrade_json(path: Path) -> int:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    upgraded = 0
    for entry in data:
        name_ja = entry.get("name_ja", "") or ""
        species_disp = entry.get("species", "")
        species_norm = SPECIES_NORM.get(species_disp, species_disp)
        current = entry.get("treatment_ja", "") or ""

        if not _needs_upgrade(name_ja, current):
            continue
        new_content = generate_content(species_norm, name_ja, entry.get("name", ""))
        if new_content is None:
            continue
        new_tx = new_content.get("treatment_ja", "")
        if not new_tx:
            continue
        # Only upgrade if the new content is meaningfully different AND has the fingerprint
        for kw, fp in SUBTYPE_FINGERPRINTS:
            if kw in name_ja and _has_subtype_fingerprint(new_tx, fp):
                entry["treatment_ja"] = new_tx
                if new_content.get("prognosis_ja"):
                    entry["prognosis_ja"] = new_content["prognosis_ja"]
                upgraded += 1
                break

    if upgraded:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return upgraded


def main() -> int:
    json_path = ROOT / "diseases_all_species.json"
    n = upgrade_json(json_path)
    print(f"Upgraded {n} blood-disorder entries with subtype-specific content")
    return 0


if __name__ == "__main__":
    sys.exit(main())
