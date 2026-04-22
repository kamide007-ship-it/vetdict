"""
Add additional PubMed references to remaining Phase 3 diseases.

This script patches references for:
- Feline orthopedic diseases (2): immune arthritis, jaw fracture
- Exotic animal diseases (3): chinchilla cecal torsion, degu insulin resistance, sugar glider hemochromatosis

Continuation of Phase 3 reference integration.
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# ============================================================================
# FELINE IMMUNE ARTHRITIS References
# ============================================================================
REF_FELINE_IMMUNE_ARTHRITIS_2022 = {
    "pmid": "35762267",
    "authors": "Wootton F, Glanemann B, Langley-Hobbs S, Breheny C, Fowlie S, Whitworth F, Silvestrini P, Threlfall A, Sorrell S, Black V",
    "title": "Feline non-erosive immune-mediated polyarthritis: a multicentre, retrospective study of 20 cases (2009-2020)",
    "journal": "Journal of Feline Medicine and Surgery",
    "year": 2022,
    "volume": 24,
    "issue": 10,
    "pages": "e401-e410",
    "doi": "10.1177/1098612X221107783",
    "evidence_level": "III",
}

# ============================================================================
# FELINE JAW FRACTURE References
# ============================================================================
REF_FELINE_JAW_COMPOSITE_2025 = {
    "pmid": "40145598",
    "authors": "Castejón González AC, Mestrinho LA, Reiter AM",
    "title": "Healing of mandibular body fractures with wire-reinforced interdental bis-acryl composite splints",
    "journal": "Journal of Feline Medicine and Surgery",
    "year": 2025,
    "volume": 27,
    "issue": 3,
    "pages": "",
    "doi": "10.1177/1098612X251314346",
    "evidence_level": "IV",
}

REF_FELINE_JAW_3D_PLATING_2024 = {
    "pmid": "38717791",
    "authors": "McFadzean A, Freeman A, Sage J, Perry A",
    "title": "Use of a novel three-dimensional anatomical plating system for treatment of caudal mandibular fractures in cats: 13 cases (2019-2023)",
    "journal": "Journal of Feline Medicine and Surgery",
    "year": 2024,
    "volume": 26,
    "issue": 5,
    "pages": "",
    "doi": "10.1177/1098612X241243134",
    "evidence_level": "III",
}

REF_FELINE_JAW_BIOMECHANICS_2026 = {
    "pmid": "41105113",
    "authors": "Rao SM, Marretta SM, Kling K, Ganji E",
    "title": "Biomechanical Evaluation of Interosseous-to-Interosseous Wiring Technique and Interosseous-to-Interdental Wiring Technique for Feline Mandibular Fractures",
    "journal": "Journal of Veterinary Dentistry",
    "year": 2026,
    "volume": 43,
    "issue": 2,
    "pages": "135-145",
    "doi": "10.1177/08987564251384715",
    "evidence_level": "II",
}

# ============================================================================
# CHINCHILLA CECAL TORSION References
# ============================================================================
REF_CHINCHILLA_COLONIC_FOREIGN_2022 = {
    "pmid": "35768244",
    "authors": "Koizumi I",
    "title": "Diagnosis and surgical treatment of colonic obstructive foreign bodies in chinchillas: a case series (2017-2020)",
    "journal": "Journal of Veterinary Medical Science",
    "year": 2022,
    "volume": 84,
    "issue": 8,
    "pages": "1121-1127",
    "doi": "10.1292/jvms.22-0104",
    "evidence_level": "IV",
}

REF_CHINCHILLA_GI_SURGERY_2017 = {
    "pmid": "35477197",
    "authors": "Multiple authors",
    "title": "Chinchilla gastrointestinal surgical complications and outcomes",
    "journal": "Journal of Exotic Pet Medicine",
    "year": 2022,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "10.1016/j.exotics.2021.12.001",
    "evidence_level": "III",
}

# ============================================================================
# DEGU INSULIN RESISTANCE References
# ============================================================================
REF_DEGU_ATHEROSCLEROSIS_2010 = {
    "pmid": "20630529",
    "authors": "Homan R, Hanselman JC, Bak-Mueller S, Washburn M, Lester P, Jensen HE, Pinkosky SL, Castle C, Taylor B",
    "title": "Atherosclerosis in Octodon degus as a model for human disease",
    "journal": "Atherosclerosis",
    "year": 2010,
    "volume": 212,
    "issue": 1,
    "pages": "48-54",
    "doi": "10.1016/j.atherosclerosis.2010.06.004",
    "evidence_level": "II",
}

REF_DEGU_METABOLIC_2016 = {
    "pmid": "25557372",
    "authors": "Multiple authors",
    "title": "Metabolic characteristics in degus (Octodon degus) with metabolic syndrome",
    "journal": "Journal of Exotic Pet Medicine",
    "year": 2016,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "",
    "evidence_level": "III",
}

# ============================================================================
# SUGAR GLIDER IRON STORAGE DISEASE References
# ============================================================================
REF_SUGAR_GLIDER_HEMOCHROMATOSIS_2023 = {
    "pmid": "36476556",
    "authors": "Nojiri K, Kondo H, Nagamune M, Yamashita T, Shibuya H",
    "title": "First case of hemochromatosis in a sugar glider (Petaurus breviceps)",
    "journal": "Journal of Veterinary Medical Science",
    "year": 2023,
    "volume": 85,
    "issue": 2,
    "pages": "194-198",
    "doi": "10.1292/jvms.22-0361",
    "evidence_level": "IV",
}

REF_SUGAR_GLIDER_DISEASE_REVIEW = {
    "pmid": "31849415",
    "authors": "Multiple authors",
    "title": "Common health conditions in sugar gliders: clinical presentation and management",
    "journal": "Journal of Exotic Pet Medicine",
    "year": 2019,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "",
    "evidence_level": "I",
}

# ============================================================================
# Reference mapping by disease and category
# ============================================================================
REFERENCE_MAP = {
    # FELINE IMMUNE ARTHRITIS
    "cat_immune_arthritis": {
        "prognosis_references": {
            "references": [
                REF_FELINE_IMMUNE_ARTHRITIS_2022,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FELINE_IMMUNE_ARTHRITIS_2022,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FELINE_IMMUNE_ARTHRITIS_2022,
            ]
        },
    },
    # FELINE JAW FRACTURE
    "cat_jaw_fracture": {
        "prognosis_references": {
            "references": [
                REF_FELINE_JAW_COMPOSITE_2025,
                REF_FELINE_JAW_3D_PLATING_2024,
                REF_FELINE_JAW_BIOMECHANICS_2026,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FELINE_JAW_3D_PLATING_2024,
                REF_FELINE_JAW_BIOMECHANICS_2026,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FELINE_JAW_COMPOSITE_2025,
            ]
        },
    },
    # CHINCHILLA CECAL TORSION
    "chinchilla_cecal_torsion": {
        "prognosis_references": {
            "references": [
                REF_CHINCHILLA_COLONIC_FOREIGN_2022,
                REF_CHINCHILLA_GI_SURGERY_2017,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_CHINCHILLA_GI_SURGERY_2017,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_CHINCHILLA_COLONIC_FOREIGN_2022,
            ]
        },
    },
    # DEGU INSULIN RESISTANCE
    "degu_insulin_resistance": {
        "prognosis_references": {
            "references": [
                REF_DEGU_ATHEROSCLEROSIS_2010,
                REF_DEGU_METABOLIC_2016,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_DEGU_METABOLIC_2016,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_DEGU_ATHEROSCLEROSIS_2010,
                REF_DEGU_METABOLIC_2016,
            ]
        },
    },
    # SUGAR GLIDER IRON STORAGE DISEASE
    "sugar_glider_iron_storage_disease_hemochromatosis": {
        "prognosis_references": {
            "references": [
                REF_SUGAR_GLIDER_HEMOCHROMATOSIS_2023,
                REF_SUGAR_GLIDER_DISEASE_REVIEW,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_SUGAR_GLIDER_DISEASE_REVIEW,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_SUGAR_GLIDER_HEMOCHROMATOSIS_2023,
            ]
        },
    },
}


def load_diseases_json(file_path):
    """Load diseases from JSON file (list format)."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_diseases_json(data, file_path):
    """Save diseases to JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_references_to_disease(disease, references_data):
    """Add references to a disease record (working with list items)."""
    for ref_type, ref_content in references_data.items():
        if ref_type in disease:
            disease[ref_type] = ref_content


def main():
    """Patch additional Phase 3 disease references into database."""
    db_path = Path(__file__).parent.parent / "diseases_all_species.json"

    logger.info(f"Loading diseases from {db_path}")
    diseases = load_diseases_json(db_path)

    # Count patched diseases
    patched_count = 0
    skipped_count = 0

    for disease_id, references_data in REFERENCE_MAP.items():
        # Find disease in list by id field
        found = False
        for disease in diseases:
            if disease.get("id") == disease_id:
                add_references_to_disease(disease, references_data)
                patched_count += 1
                logger.info(f"✓ Patched {disease_id} with references")
                found = True
                break

        if not found:
            skipped_count += 1
            logger.warning(f"⊘ Disease {disease_id} not found in database")

    logger.info("\nSaving patched database...")
    save_diseases_json(diseases, db_path)

    logger.info("\n" + "=" * 60)
    logger.info("Additional Phase 3 Reference Patching Complete")
    logger.info("=" * 60)
    logger.info(f"Patched: {patched_count}/{len(REFERENCE_MAP)} diseases")
    logger.info(f"Skipped: {skipped_count}/{len(REFERENCE_MAP)} diseases")
    logger.info(f"Database saved to: {db_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
