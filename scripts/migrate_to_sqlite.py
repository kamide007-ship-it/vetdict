#!/usr/bin/env python3
"""Migrate existing disease/drug/symptom data from Python modules and JSON into SQLite.

Usage:
    python scripts/migrate_to_sqlite.py [--db-path PATH]

Default DB path: instance/vetdict.db
"""

import importlib
import json
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from api.database import get_connection, init_db, upsert_disease, upsert_drug, upsert_symptom

# ---------------------------------------------------------------------------
# Species module mapping: species_key → module path
# ---------------------------------------------------------------------------
SPECIES_MODULES = {
    "cat": "api.species.cat_diseases",
    "rabbit": "api.species.rabbit_diseases",
    "bird": "api.species.bird_diseases",
    "hamster": "api.species.hamster_diseases",
    "guinea_pig": "api.species.guinea_pig_diseases",
    "ferret": "api.species.ferret_diseases",
    "hedgehog": "api.species.hedgehog_diseases",
    "chinchilla": "api.species.chinchilla_diseases",
    "reptile": "api.species.reptile_diseases",
    "snake": "api.species.snake_diseases",
    "lizard": "api.species.lizard_diseases",
    "tortoise": "api.species.tortoise_diseases",
    "parakeet": "api.species.parakeet_diseases",
    "parrot": "api.species.parrot_diseases",
    "amphibian": "api.species.amphibian_diseases",
    "degu": "api.species.degu_diseases",
    "sugar_glider": "api.species.sugar_glider_diseases",
    "exotic_other": "api.species.exotic_other_diseases",
}

# Dog uses symptom_checker module (different structure)
DOG_MODULE = "api.symptom_checker"
DOG_DISEASES_VAR = "_DISEASE_DB"
DOG_SYMPTOMS_VAR = "_SYMPTOM_NAMES"


def _load_module(module_path: str):
    return importlib.import_module(module_path)


def migrate_species_diseases(conn, species_key: str, module_path: str) -> int:
    """Load DISEASES from a species module and insert into SQLite. Returns count."""
    mod = _load_module(module_path)
    diseases = getattr(mod, "DISEASES", [])
    count = 0
    for i, d in enumerate(diseases):
        disease_id = d.get("id") or f"{species_key}_{i:04d}"
        record = {
            "id": disease_id,
            "species": species_key,
            "name": d.get("name", ""),
            "name_ja": d.get("name_ja", d.get("name", "")),
            "description": d.get("description"),
            "description_ja": d.get("description_ja"),
            "pathophysiology": d.get("pathophysiology"),
            "pathophysiology_ja": d.get("pathophysiology_ja"),
            "causes": d.get("causes"),
            "causes_ja": d.get("causes_ja"),
            "treatment": d.get("treatment"),
            "treatment_ja": d.get("treatment_ja"),
            "prevention": d.get("prevention"),
            "prevention_ja": d.get("prevention_ja"),
            "prognosis": d.get("prognosis"),
            "prognosis_ja": d.get("prognosis_ja"),
            "urgency": d.get("urgency"),
            "symptoms": d.get("symptoms", set()),
            "recommended_tests": d.get("recommended_tests", []),
            "onset_pattern": d.get("onset_pattern"),
            "age_predisposition": d.get("age_predisposition"),
        }
        upsert_disease(conn, record)
        count += 1
    return count


def migrate_species_symptoms(conn, species_key: str, module_path: str) -> int:
    """Load SYMPTOM_NAMES from a species module and insert into SQLite."""
    mod = _load_module(module_path)
    symptom_names = getattr(mod, "SYMPTOM_NAMES", {})
    count = 0
    for sid, names in symptom_names.items():
        upsert_symptom(
            conn,
            symptom_id=f"{species_key}_{sid}",
            name_en=names.get("en", sid),
            name_ja=names.get("ja", sid),
            species=species_key,
        )
        count += 1
    return count


def migrate_dog_diseases(conn) -> int:
    """Migrate dog diseases from symptom_checker module."""
    mod = _load_module(DOG_MODULE)
    diseases = getattr(mod, DOG_DISEASES_VAR, [])
    count = 0
    for i, d in enumerate(diseases):
        disease_id = d.get("id") or f"dog_{i:04d}"
        record = {
            "id": disease_id,
            "species": "dog",
            "name": d.get("name", ""),
            "name_ja": d.get("name_ja", d.get("name", "")),
            "description": d.get("description"),
            "description_ja": d.get("description_ja"),
            "pathophysiology": d.get("pathophysiology"),
            "pathophysiology_ja": d.get("pathophysiology_ja"),
            "causes": d.get("causes"),
            "causes_ja": d.get("causes_ja"),
            "treatment": d.get("treatment"),
            "treatment_ja": d.get("treatment_ja"),
            "prevention": d.get("prevention"),
            "prevention_ja": d.get("prevention_ja"),
            "prognosis": d.get("prognosis"),
            "prognosis_ja": d.get("prognosis_ja"),
            "urgency": d.get("urgency"),
            "symptoms": d.get("symptoms", set()),
            "recommended_tests": d.get("recommended_tests", []),
            "onset_pattern": d.get("onset_pattern"),
            "age_predisposition": d.get("age_predisposition"),
        }
        upsert_disease(conn, record)
        count += 1

    symptom_names = getattr(mod, DOG_SYMPTOMS_VAR, {})
    for sid, names in symptom_names.items():
        upsert_symptom(conn, f"dog_{sid}", names.get("en", sid), names.get("ja", sid), "dog")

    return count


def migrate_json_enrichments(conn) -> int:
    """Overlay enrichment data from diseases_all_species.json."""
    json_path = ROOT / "diseases_all_species.json"
    if not json_path.exists():
        print(f"  [skip] {json_path} not found")
        return 0

    with open(json_path, encoding="utf-8") as f:
        entries = json.load(f)

    count = 0
    for entry in entries:
        disease_id = entry.get("id")
        if not disease_id:
            continue
        # Update only enrichment fields on existing records
        conn.execute(
            """UPDATE diseases SET
                description = COALESCE(?, description),
                description_ja = COALESCE(?, description_ja),
                pathophysiology = COALESCE(?, pathophysiology),
                pathophysiology_ja = COALESCE(?, pathophysiology_ja),
                causes = COALESCE(?, causes),
                causes_ja = COALESCE(?, causes_ja),
                treatment = COALESCE(?, treatment),
                treatment_ja = COALESCE(?, treatment_ja),
                prevention = COALESCE(?, prevention),
                prevention_ja = COALESCE(?, prevention_ja),
                prognosis = COALESCE(?, prognosis),
                prognosis_ja = COALESCE(?, prognosis_ja),
                enriched_at = ?,
                enrichment_phase = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?""",
            (
                entry.get("description"),
                entry.get("description_ja"),
                entry.get("pathophysiology"),
                entry.get("pathophysiology_ja"),
                entry.get("causes"),
                entry.get("causes_ja"),
                entry.get("treatment"),
                entry.get("treatment_ja"),
                entry.get("prevention"),
                entry.get("prevention_ja"),
                entry.get("prognosis"),
                entry.get("prognosis_ja"),
                entry.get("enriched_at"),
                entry.get("enrichment_phase"),
                disease_id,
            ),
        )
        if conn.execute("SELECT changes()").fetchone()[0] > 0:
            count += 1
    return count


def migrate_drugs(conn) -> int:
    """Migrate drugs from drug_dictionary module."""
    mod = _load_module("api.drug_dictionary")
    drugs = getattr(mod, "DRUGS", [])
    count = 0
    for drug in drugs:
        upsert_drug(conn, drug)
        count += 1
    return count


def migrate_equine(conn) -> int:
    """Migrate equine diseases (Disease dataclass with different field names)."""
    mod = _load_module("api.species.equine_diseases")
    disease_db = getattr(mod, "DISEASE_DATABASE", [])
    count = 0
    for d in disease_db:
        record = {
            "id": d.id,
            "species": "horse",
            "name": d.name_en,
            "name_ja": d.name_ja,
            "description": d.description_ja,
            "description_ja": d.description_ja,
            "pathophysiology": d.pathophysiology,
            "causes": d.etiology,
            "treatment": d.treatment_protocol,
            "prevention": d.prevention,
            "prognosis": d.prognosis,
            "urgency": d.urgency or d.severity,
            "symptoms": set(d.associated_findings),
            "recommended_tests": [(e[1] if len(e) > 1 else str(e)) for e in (d.recommended_exams or [])],
        }
        upsert_disease(conn, record)
        count += 1
    return count


def main(db_path: str | None = None):
    print("=" * 60)
    print("VetDict Data Migration → SQLite")
    print("=" * 60)

    init_db(db_path)

    with get_connection(db_path) as conn:
        total_diseases = 0
        total_symptoms = 0

        # Dog (special module)
        print("\n[dog] migrating diseases...")
        n = migrate_dog_diseases(conn)
        print(f"  → {n} diseases")
        total_diseases += n

        # Equine (special structure)
        print("\n[horse] migrating diseases...")
        n = migrate_equine(conn)
        print(f"  → {n} diseases")
        total_diseases += n

        # All other species
        for species_key, module_path in sorted(SPECIES_MODULES.items()):
            print(f"\n[{species_key}] migrating diseases...")
            n = migrate_species_diseases(conn, species_key, module_path)
            print(f"  → {n} diseases")
            total_diseases += n

            ns = migrate_species_symptoms(conn, species_key, module_path)
            print(f"  → {ns} symptoms")
            total_symptoms += ns

        # JSON enrichments overlay
        print("\n[enrichment] overlaying JSON enrichments...")
        n = migrate_json_enrichments(conn)
        print(f"  → {n} diseases enriched")

        # Drugs
        print("\n[drugs] migrating drug dictionary...")
        n = migrate_drugs(conn)
        print(f"  → {n} drugs")

        # Summary
        stats = conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
        drug_count = conn.execute("SELECT COUNT(*) FROM drugs").fetchone()[0]
        symptom_count = conn.execute("SELECT COUNT(*) FROM symptoms").fetchone()[0]

        print("\n" + "=" * 60)
        print("Migration complete!")
        print(f"  Diseases:  {stats}")
        print(f"  Symptoms:  {symptom_count}")
        print(f"  Drugs:     {drug_count}")
        print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate VetDict data to SQLite")
    parser.add_argument("--db-path", default=None, help="SQLite database path")
    args = parser.parse_args()
    main(args.db_path)
