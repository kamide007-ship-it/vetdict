#!/usr/bin/env python3
"""Seed the SQLite database from the existing Python disease data.

Usage:
    python seed_db.py [--force]

Options:
    --force   Drop and recreate all tables before seeding.
"""

from __future__ import annotations

import sys
import os
from pathlib import Path

# Ensure project root is on sys.path
root = Path(__file__).resolve().parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from flask import Flask
from api.database import db, Disease, disease_symptoms, disease_tests, init_db


# ---------------------------------------------------------------------------
# Species -> module mapping for loading DISEASES lists
# ---------------------------------------------------------------------------

SPECIES_MODULES = {
    "dog": ("api.symptom_checker", "_DISEASE_DB"),
    "cat": ("api.species.cat_diseases", "DISEASES"),
    "rabbit": ("api.species.rabbit_diseases", "DISEASES"),
    "hamster": ("api.species.hamster_diseases", "DISEASES"),
    "chinchilla": ("api.species.chinchilla_diseases", "DISEASES"),
    "guinea_pig": ("api.species.guinea_pig_diseases", "DISEASES"),
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
    "exotic_other": ("api.species.exotic_other_diseases", "DISEASES"),
}

# Text fields that may exist on disease dicts
TEXT_FIELDS = [
    "description", "description_ja",
    "causes", "causes_ja",
    "pathophysiology", "pathophysiology_ja",
    "prevention", "prevention_ja",
    "treatment", "treatment_ja",
    "prognosis", "prognosis_ja",
]


def _load_diseases(module_path: str, attr_name: str):
    """Dynamically import a module and return its disease list."""
    import importlib
    mod = importlib.import_module(module_path)
    return getattr(mod, attr_name)


def seed_species(species: str, module_path: str, attr_name: str) -> int:
    """Insert diseases for one species. Returns the count of diseases added."""
    diseases = _load_diseases(module_path, attr_name)
    count = 0

    for d in diseases:
        name = d.get("name", "")
        if not name:
            continue

        # Check if already exists
        existing = Disease.query.filter_by(species=species, name=name).first()
        if existing:
            continue

        disease = Disease(
            species=species,
            name=name,
            name_ja=d.get("name_ja", ""),
            urgency=d.get("urgency", "moderate"),
        )

        # Set text fields
        for field in TEXT_FIELDS:
            val = d.get(field, "")
            if val:
                setattr(disease, field, val)

        db.session.add(disease)
        db.session.flush()  # Get the ID

        # Insert symptoms
        symptoms = d.get("symptoms", set())
        if isinstance(symptoms, (set, frozenset, list, tuple)):
            for symptom_id in symptoms:
                db.session.execute(
                    disease_symptoms.insert().values(
                        disease_id=disease.id,
                        symptom_id=str(symptom_id),
                    )
                )

        # Insert recommended tests
        tests = d.get("recommended_tests", [])
        for i, test_id in enumerate(tests):
            db.session.execute(
                disease_tests.insert().values(
                    disease_id=disease.id,
                    test_id=str(test_id),
                    sort_order=i,
                )
            )

        count += 1

    db.session.commit()
    return count


def seed_all(force: bool = False):
    """Seed all species into the database."""
    if force:
        db.drop_all()
        db.create_all()

    total = 0
    for species, (module_path, attr_name) in SPECIES_MODULES.items():
        try:
            count = seed_species(species, module_path, attr_name)
            if count > 0:
                print(f"  {species}: {count} diseases added")
            else:
                print(f"  {species}: already seeded (skipped)")
            total += count
        except Exception as e:
            print(f"  {species}: ERROR - {e}")

    print(f"\nTotal: {total} diseases seeded")
    return total


def main():
    force = "--force" in sys.argv

    app = Flask(__name__)
    init_db(app)

    with app.app_context():
        if force:
            print("Force mode: dropping and recreating all tables...")
        print("Seeding disease database...")
        seed_all(force=force)
        print("Done.")


if __name__ == "__main__":
    main()
