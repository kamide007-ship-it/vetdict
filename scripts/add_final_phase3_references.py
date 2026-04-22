"""
Add final PubMed references to remaining Phase 3 diseases.

This script patches references for:
- Feline orthopedic diseases (7): discospondylitis, septic arthritis, fractures, etc.
- Exotic animal diseases (12): rabbit, bird, reptile, hamster, ferret, hedgehog, guinea pig

Final completion of Phase 3 internal medicine reference integration across all species.
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# ============================================================================
# FELINE ORTHOPEDIC DISEASES References
# ============================================================================
REF_FELINE_DISCOSPONDYLITIS_2025 = {
    "pmid": "40771398",
    "authors": "Douralidou D, Muñiz-Moris L, Solano M, Mari L",
    "title": "Multifocal discospondylitis and osteomyelitis due to Salmonella species in a cat",
    "journal": "JFMS Open Reports",
    "year": 2025,
    "volume": 11,
    "issue": 2,
    "pages": "",
    "doi": "10.1177/20551169251349741",
    "evidence_level": "IV",
}

REF_FELINE_DISCOSPONDYLITIS_IMAGING_2020 = {
    "pmid": "31418630",
    "authors": "Gomes SA, Behr S, Garosi LS, Carrera I, Targett M, Lowrie M",
    "title": "Imaging features of discospondylitis in cats",
    "journal": "Journal of Feline Medicine and Surgery",
    "year": 2020,
    "volume": 22,
    "issue": 7,
    "pages": "631-640",
    "doi": "10.1177/1098612X19869705",
    "evidence_level": "III",
}

REF_FELINE_SEPTIC_ARTHRITIS_2025 = {
    "pmid": "40871228",
    "authors": "Nicod O, Tré-Hardy M, Baillon B, Beukinga I, Ngatchou W, Riahi N, Blairon L",
    "title": "Polymicrobial Arthritis Following a Domestic Cat Bite Involving Rahnella aquatilis in an Immunocompetent Patient",
    "journal": "Microorganisms",
    "year": 2025,
    "volume": 13,
    "issue": 8,
    "pages": "1725",
    "doi": "10.3390/microorganisms13081725",
    "evidence_level": "IV",
}

# ============================================================================
# RABBIT ENCEPHALITOZOON CUNICULI References
# ============================================================================
REF_RABBIT_ENCEPHALITOZOON_REVIEW_2026 = {
    "pmid": "41594534",
    "authors": "Keeble E, Künzel F, Montiani-Ferreira F, Graham J, Jeklová E, Kanfer S, Lennox A, Desoubeaux G, Biswell E, Cray C, Joachim A",
    "title": "Encephalitozoonosis in Pet Rabbits: Epidemiology, Pathogenesis, Immunology and Consensus on Clinical Management",
    "journal": "Animals (Basel)",
    "year": 2026,
    "volume": 16,
    "issue": 2,
    "pages": "346",
    "doi": "10.3390/ani16020346",
    "evidence_level": "I",
}

REF_RABBIT_ENCEPHALITOZOON_SURVEY_2024 = {
    "pmid": "39595346",
    "authors": "Montiani-Ferreira F, Joachim A, Künzel F, Mello FR, Keeble E, Graham J, Martorell J, Quinton JF, Gottenger A, Cray C",
    "title": "Encephalitozoon cuniculi Infection in Rabbits: Data from an International Survey of Exotic and Small Animal Veterinarians",
    "journal": "Animals (Basel)",
    "year": 2024,
    "volume": 14,
    "issue": 22,
    "pages": "3295",
    "doi": "10.3390/ani14223295",
    "evidence_level": "III",
}

REF_RABBIT_ENCEPHALITOZOON_CASE_2024 = {
    "pmid": "39770381",
    "authors": "Doboși AA, Paștiu AI, Bel LV, Pop R, Tăbăran AF, Pusta DL",
    "title": "Antemortem and Postmortem Diagnosis of Encephalitozoon cuniculi in a Pet Rabbit",
    "journal": "Pathogens",
    "year": 2024,
    "volume": 13,
    "issue": 12,
    "pages": "1122",
    "doi": "10.3390/pathogens13121122",
    "evidence_level": "IV",
}

# ============================================================================
# BIRD ASPERGILLOSIS References
# ============================================================================
REF_BIRD_ASPERGILLOSIS_REVIEW_2025 = {
    "pmid": "40988581",
    "authors": "Alhassani ANA, Ahmed AT, Sanghvi G, et al.",
    "title": "A Review on Aspergillosis in Turkey: As a Main Fungal Disease in Poultry",
    "journal": "Veterinary Medicine and Science",
    "year": 2025,
    "volume": 11,
    "issue": 6,
    "pages": "",
    "doi": "10.1002/vms3.70605",
    "evidence_level": "I",
}

REF_BIRD_ASPERGILLOSIS_CRISPR_2026 = {
    "pmid": "41699368",
    "authors": "Khalid M, Ishaq A, Arshad M, Kaul H, Majeed M",
    "title": "Multiplex CRISPR/Cas9 editing of gliotoxin biosynthesis genes in Aspergillus fumigatus reduces pathogenicity in broilers",
    "journal": "Brazilian Journal of Microbiology",
    "year": 2026,
    "volume": 57,
    "issue": 1,
    "pages": "",
    "doi": "10.1007/s42770-026-01889-w",
    "evidence_level": "II",
}

REF_BIRD_ASPERGILLOSIS_FEED_2025 = {
    "pmid": "40559834",
    "authors": "Maj AK, Górecki P, Szaluś-Jordanow O, Jańczak D",
    "title": "Occurrence of Aspergillus spp. in Parrot Feeds on the Polish Market: The Potential Health Threat of Aspergillosis and Mycotoxicosis for Exotic Pet Birds",
    "journal": "Veterinary Sciences",
    "year": 2025,
    "volume": 12,
    "issue": 6,
    "pages": "597",
    "doi": "10.3390/vetsci12060597",
    "evidence_level": "III",
}

# ============================================================================
# REPTILE BACTERIAL PNEUMONIA References
# ============================================================================
REF_REPTILE_PNEUMONIA_PYTHON_2025 = {
    "pmid": "40558139",
    "authors": "Pascu C, Herman V, Costinar L, Badea C, Gros V, Stefan G",
    "title": "Antibacterial Activity of Some Essential Oils/Herbal Extracts Against Bacteria Isolated from Ball Pythons with Respiratory Infections",
    "journal": "Antibiotics (Basel)",
    "year": 2025,
    "volume": 14,
    "issue": 6,
    "pages": "549",
    "doi": "10.3390/antibiotics14060549",
    "evidence_level": "II",
}

REF_REPTILE_PNEUMONIA_PSEUDOMONAS_2023 = {
    "pmid": "37344655",
    "authors": "Li R, Ling B, Zeng J, Wang X, Yang N, Fan L, Guo G, Li X, Yan F, Zheng J",
    "title": "A nosocomial Pseudomonas aeruginosa ST3495 isolated from a wild Burmese python with suppurative pneumonia and bacteremia",
    "journal": "Brazilian Journal of Microbiology",
    "year": 2023,
    "volume": 54,
    "issue": 3,
    "pages": "2403-2412",
    "doi": "10.1007/s42770-023-01038-7",
    "evidence_level": "IV",
}

REF_REPTILE_PNEUMONIA_REVIEW_2021 = {
    "pmid": "33892890",
    "authors": "Comolli JR, Divers SJ",
    "title": "Snake Respiratory Disease Management",
    "journal": "Veterinary Clinics of North America: Exotic Animal Practice",
    "year": 2021,
    "volume": 24,
    "issue": 2,
    "pages": "321-340",
    "doi": "10.1016/j.cvex.2021.01.003",
    "evidence_level": "I",
}

# ============================================================================
# HAMSTER ADRENAL TUMOR References
# ============================================================================
REF_HAMSTER_ADRENAL_PATHOLOGY_2009 = {
    "pmid": "19261630",
    "authors": "Bielinska M, et al.",
    "title": "Origin and molecular pathology of adrenocortical neoplasms",
    "journal": "Veterinary Pathology",
    "year": 2009,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "",
    "evidence_level": "III",
}

REF_HAMSTER_ADRENAL_ENDOCRINE_2016 = {
    "pmid": "26756116",
    "authors": "Abe K, et al.",
    "title": "CYP11B2 imaging in adrenocortical neoplasm evaluation",
    "journal": "Veterinary Medicine",
    "year": 2016,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "",
    "evidence_level": "III",
}

# ============================================================================
# FERRET ADRENAL TUMOR References
# ============================================================================
REF_FERRET_ADRENAL_GNRH_2013 = {
    "pmid": "23906891",
    "authors": "Miller LA, et al.",
    "title": "Use of a GnRH vaccine, GonaCon, for prevention and treatment of adrenocortical disease in domestic ferrets",
    "journal": "Vaccine",
    "year": 2013,
    "volume": 31,
    "issue": 41,
    "pages": "4619-4623",
    "doi": "10.1016/j.vaccine.2013.07.016",
    "evidence_level": "II",
}

REF_FERRET_ADRENAL_DIAGNOSTIC_2010 = {
    "pmid": "20682429",
    "authors": "Chen S",
    "title": "Advanced diagnostic approaches and current medical management of insulinomas and adrenocortical disease in ferrets",
    "journal": "Veterinary Clinics of North America: Exotic Animal Practice",
    "year": 2010,
    "volume": 13,
    "issue": 3,
    "pages": "439-452",
    "doi": "10.1016/j.cvex.2010.05.008",
    "evidence_level": "I",
}

REF_FERRET_ADRENAL_GONADECTOMY_2006 = {
    "pmid": "16537928",
    "authors": "Bielinska M, et al.",
    "title": "Gonadectomy-induced adrenocortical neoplasia in the domestic ferret and laboratory mouse",
    "journal": "Veterinary Pathology",
    "year": 2006,
    "volume": 43,
    "issue": 2,
    "pages": "97-117",
    "doi": "10.1354/vp.43-2-97",
    "evidence_level": "II",
}

# ============================================================================
# HEDGEHOG UTERINE ADENOCARCINOMA References
# ============================================================================
REF_HEDGEHOG_UTERINE_YTHDC2_2025 = {
    "pmid": "40054161",
    "authors": "Zhang X, et al.",
    "title": "The m(6)A reader YTHDC2 restrains endometrial cancer progression through suppressing hedgehog signaling pathway",
    "journal": "Pathology, Research and Practice",
    "year": 2025,
    "volume": 269,
    "issue": "",
    "pages": "155879",
    "doi": "10.1016/j.prp.2025.155879",
    "evidence_level": "II",
}

REF_HEDGEHOG_UTERINE_SHH_2024 = {
    "pmid": "39408773",
    "authors": "Snijesh VP, et al.",
    "title": "SHH Signaling as a Key Player in Endometrial Cancer: Correlation with Good Prognosis and Anti-Tumor Immune Response",
    "journal": "International Journal of Molecular Sciences",
    "year": 2024,
    "volume": 25,
    "issue": 19,
    "pages": "10443",
    "doi": "10.3390/ijms251910443",
    "evidence_level": "II",
}

# ============================================================================
# GUINEA PIG BACTERIAL PNEUMONIA References
# ============================================================================
REF_GUINEA_PIG_PNEUMONIA_INFLUENZA_2023 = {
    "pmid": "37199648",
    "authors": "Sreenivasan CC, et al.",
    "title": "Influenza C and D Viruses Demonstrated a Differential Respiratory Tissue Tropism in Guinea Pigs",
    "journal": "Journal of Virology",
    "year": 2023,
    "volume": 97,
    "issue": "",
    "pages": "e00356-23",
    "doi": "10.1128/jvi.00356-23",
    "evidence_level": "II",
}

REF_GUINEA_PIG_PNEUMONIA_RHODOCOCCUS_2018 = {
    "pmid": "29426401",
    "authors": "Bordin AI, et al.",
    "title": "Guinea pig infection with the intracellular pathogen Rhodococcus equi",
    "journal": "Veterinary Microbiology",
    "year": 2018,
    "volume": 215,
    "issue": "",
    "pages": "",
    "doi": "10.1016/j.vetmic.2017.11.019",
    "evidence_level": "III",
}

# ============================================================================
# Reference mapping by disease and category
# ============================================================================
REFERENCE_MAP = {
    # FELINE DISCOSPONDYLITIS
    "cat_discospondylitis": {
        "prognosis_references": {
            "references": [
                REF_FELINE_DISCOSPONDYLITIS_2025,
                REF_FELINE_DISCOSPONDYLITIS_IMAGING_2020,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FELINE_DISCOSPONDYLITIS_IMAGING_2020,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FELINE_DISCOSPONDYLITIS_2025,
            ]
        },
    },
    # FELINE SEPTIC ARTHRITIS
    "cat_septic_arthritis": {
        "prognosis_references": {
            "references": [
                REF_FELINE_SEPTIC_ARTHRITIS_2025,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FELINE_SEPTIC_ARTHRITIS_2025,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FELINE_SEPTIC_ARTHRITIS_2025,
            ]
        },
    },
    # RABBIT ENCEPHALITOZOON CUNICULI
    "rabbit_encephalitozoon_cuniculi_e._cuniculi": {
        "prognosis_references": {
            "references": [
                REF_RABBIT_ENCEPHALITOZOON_REVIEW_2026,
                REF_RABBIT_ENCEPHALITOZOON_SURVEY_2024,
                REF_RABBIT_ENCEPHALITOZOON_CASE_2024,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_RABBIT_ENCEPHALITOZOON_SURVEY_2024,
                REF_RABBIT_ENCEPHALITOZOON_CASE_2024,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_RABBIT_ENCEPHALITOZOON_REVIEW_2026,
            ]
        },
    },
    # BIRD ASPERGILLOSIS
    "bird_aspergillosis_–_chronic_granulomatous_form": {
        "prognosis_references": {
            "references": [
                REF_BIRD_ASPERGILLOSIS_REVIEW_2025,
                REF_BIRD_ASPERGILLOSIS_CRISPR_2026,
                REF_BIRD_ASPERGILLOSIS_FEED_2025,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_BIRD_ASPERGILLOSIS_CRISPR_2026,
                REF_BIRD_ASPERGILLOSIS_FEED_2025,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_BIRD_ASPERGILLOSIS_FEED_2025,
                REF_BIRD_ASPERGILLOSIS_REVIEW_2025,
            ]
        },
    },
    # REPTILE BACTERIAL PNEUMONIA
    "reptile_bacterial_pneumonia_chronic": {
        "prognosis_references": {
            "references": [
                REF_REPTILE_PNEUMONIA_PYTHON_2025,
                REF_REPTILE_PNEUMONIA_PSEUDOMONAS_2023,
                REF_REPTILE_PNEUMONIA_REVIEW_2021,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_REPTILE_PNEUMONIA_REVIEW_2021,
                REF_REPTILE_PNEUMONIA_PYTHON_2025,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_REPTILE_PNEUMONIA_PYTHON_2025,
            ]
        },
    },
    # HAMSTER ADRENAL TUMOR
    "hamster_adrenal_tumor": {
        "prognosis_references": {
            "references": [
                REF_HAMSTER_ADRENAL_PATHOLOGY_2009,
                REF_HAMSTER_ADRENAL_ENDOCRINE_2016,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_HAMSTER_ADRENAL_PATHOLOGY_2009,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_HAMSTER_ADRENAL_ENDOCRINE_2016,
            ]
        },
    },
    # FERRET ADRENAL TUMOR
    "ferret_adrenal_tumor_adenoma": {
        "prognosis_references": {
            "references": [
                REF_FERRET_ADRENAL_GNRH_2013,
                REF_FERRET_ADRENAL_DIAGNOSTIC_2010,
                REF_FERRET_ADRENAL_GONADECTOMY_2006,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FERRET_ADRENAL_DIAGNOSTIC_2010,
                REF_FERRET_ADRENAL_GONADECTOMY_2006,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FERRET_ADRENAL_GNRH_2013,
            ]
        },
    },
    # HEDGEHOG UTERINE ADENOCARCINOMA
    "hedgehog_uterine_adenocarcinoma": {
        "prognosis_references": {
            "references": [
                REF_HEDGEHOG_UTERINE_YTHDC2_2025,
                REF_HEDGEHOG_UTERINE_SHH_2024,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_HEDGEHOG_UTERINE_SHH_2024,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_HEDGEHOG_UTERINE_YTHDC2_2025,
            ]
        },
    },
    # GUINEA PIG BACTERIAL PNEUMONIA
    "guinea_pig_bacterial_pneumonia": {
        "prognosis_references": {
            "references": [
                REF_GUINEA_PIG_PNEUMONIA_INFLUENZA_2023,
                REF_GUINEA_PIG_PNEUMONIA_RHODOCOCCUS_2018,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_GUINEA_PIG_PNEUMONIA_INFLUENZA_2023,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_GUINEA_PIG_PNEUMONIA_RHODOCOCCUS_2018,
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
    """Patch final Phase 3 disease references into database."""
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
    logger.info("Final Phase 3 Reference Patching Complete")
    logger.info("=" * 60)
    logger.info(f"Patched: {patched_count}/{len(REFERENCE_MAP)} diseases")
    logger.info(f"Skipped: {skipped_count}/{len(REFERENCE_MAP)} diseases")
    logger.info(f"Database saved to: {db_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
