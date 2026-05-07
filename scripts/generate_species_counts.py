#!/usr/bin/env python3
"""Generate species_counts.json without full SQLite migration.

This lightweight script counts diseases and drugs from Python modules and
writes instance/species_counts.json (~700 bytes).  Unlike migrate_to_sqlite.py
it does NOT keep all modules in memory simultaneously — it loads each module,
counts, then discards it, keeping peak RSS under ~80 MB.

Usage:
    python scripts/generate_species_counts.py
"""

import gc
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SPECIES_MODULES = {
    "dog": ("api.species.dog_diseases", "DISEASES"),
    "horse": ("api.species.equine_diseases", "DISEASE_DATABASE"),
    "cat": ("api.species.cat_diseases", "DISEASES"),
    "rabbit": ("api.species.rabbit_diseases", "DISEASES"),
    "hamster": ("api.species.hamster_diseases", "DISEASES"),
    "guinea_pig": ("api.species.guinea_pig_diseases", "DISEASES"),
    "chinchilla": ("api.species.chinchilla_diseases", "DISEASES"),
    "ferret": ("api.species.ferret_diseases", "DISEASES"),
    "hedgehog": ("api.species.hedgehog_diseases", "DISEASES"),
    "sugar_glider": ("api.species.sugar_glider_diseases", "DISEASES"),
    "degu": ("api.species.degu_diseases", "DISEASES"),
    "bird": ("api.species.bird_diseases", "DISEASES"),
    "parakeet": ("api.species.parakeet_diseases", "DISEASES"),
    "parrot": ("api.species.parrot_diseases", "DISEASES"),
    "reptile": ("api.species.reptile_diseases", "DISEASES"),
    "tortoise": ("api.species.tortoise_diseases", "DISEASES"),
    "snake": ("api.species.snake_diseases", "DISEASES"),
    "lizard": ("api.species.lizard_diseases", "DISEASES"),
    "amphibian": ("api.species.amphibian_diseases", "DISEASES"),
    "fish": ("api.species.fish_diseases", "DISEASES"),
    "exotic_other": ("api.species.exotic_other_diseases", "DISEASES"),
}


def main():
    disease_counts = {}
    for sp_id, (mod_path, attr) in SPECIES_MODULES.items():
        already = mod_path in sys.modules
        try:
            mod = importlib.import_module(mod_path)
            data = getattr(mod, attr, [])
            disease_counts[sp_id] = len(data) if data else 0
            del data
            del mod
        except Exception as e:
            print(f"  WARNING: {sp_id}: {e}")
            disease_counts[sp_id] = 0
        if not already and mod_path in sys.modules:
            del sys.modules[mod_path]
        gc.collect()

    # Drug counts — drug_dictionary is lightweight (~5 MB)
    drug_counts = {}
    total_drugs = 0
    try:
        from api.drug_dictionary import DRUGS

        total_drugs = len(DRUGS)
        for d in DRUGS:
            for sp in d.get("species_info") or {}:
                drug_counts[sp] = drug_counts.get(sp, 0) + 1
    except Exception as e:
        print(f"  WARNING: drugs: {e}")

    out_dir = ROOT / "instance"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "species_counts.json"
    payload = {
        "disease_counts": disease_counts,
        "drug_counts": drug_counts,
        "total_drugs": total_drugs,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False))

    total_diseases = sum(disease_counts.values())
    print(f"species_counts.json written: {total_diseases} diseases, {total_drugs} drugs ({out_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
