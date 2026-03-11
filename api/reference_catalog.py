"""Landing page veterinary references used for disease evidence mapping."""

from __future__ import annotations

from typing import Dict, List

# Canonical references shown in templates/index.html ([1]-[60]).
REFERENCE_CATALOG: Dict[int, Dict[str, str]] = {
    1: {"title": "Small Animal Internal Medicine (6th)", "url": ""},
    2: {"title": "Textbook of Veterinary Internal Medicine (8th)", "url": ""},
    3: {"title": "Equine Internal Medicine (4th)", "url": ""},
    4: {"title": "Ferrets, Rabbits, and Rodents: Clinical Medicine and Surgery (4th)", "url": ""},
    5: {"title": "Current Therapy in Reptile Medicine and Surgery", "url": ""},
    6: {"title": "Avian Medicine: Principles and Application", "url": ""},
    7: {"title": "Merck Veterinary Manual", "url": "https://www.merckvetmanual.com/"},
    8: {"title": "The Cat: Clinical Medicine and Management", "url": ""},
    9: {"title": "Textbook of Rabbit Medicine", "url": ""},
    10: {"title": "Exotic Companion Medicine Handbook", "url": ""},
    11: {"title": "Large Animal Internal Medicine (5th)", "url": ""},
    12: {"title": "Plumb's Veterinary Drug Handbook (9th)", "url": "https://www.wiley.com/en-us/Plumb%27s+Veterinary+Drug+Handbook-p-9781119344452"},
    13: {"title": "WSAVA Global Nutrition Guidelines", "url": "https://wsava.org/global-guidelines/global-nutrition-guidelines/"},
    14: {"title": "HorseDVM", "url": "https://horsedvm.com/"},
    15: {"title": "犬と猫の治療薬ガイド EduOne", "url": "https://search.eduone.jp/"},
    16: {"title": "Breed Predispositions to Disease in Dogs and Cats (3rd)", "url": ""},
    17: {"title": "Veterinary Medical Guide to Dog and Cat Breeds", "url": ""},
    18: {"title": "Canine Genetics and Epidemiology (Pedersen et al. 2015)", "url": ""},
    19: {"title": "Longevity and mortality of owned dogs in England", "url": ""},
    20: {"title": "Osteochondrodysplasia in Scottish Fold cats", "url": ""},
    21: {"title": "DNA mutations of the cat", "url": ""},
    22: {"title": "Breed-specific genetic testing for canine hereditary diseases", "url": ""},
    23: {"title": "Medical History and Physical Examination in Companion Animals", "url": ""},
    24: {"title": "Clinical signs approach to differential diagnosis", "url": ""},
    25: {"title": "Risk factors for gastric dilatation-volvulus", "url": ""},
    26: {"title": "Clinical Veterinary Advisor: Dogs and Cats (3rd)", "url": ""},
    27: {"title": "Chronic kidney disease in small animals", "url": ""},
    28: {"title": "Canine and Feline Endocrinology (4th)", "url": ""},
    29: {"title": "Manual of Canine and Feline Neurology (4th)", "url": ""},
    30: {"title": "Veterinary Surgery: Small Animal", "url": ""},
    31: {"title": "Hedgehog health and disease", "url": ""},
    32: {"title": "BSAVA Manual of Exotic Pets (5th)", "url": ""},
    33: {"title": "Avian Medicine and Surgery in Practice (2nd)", "url": ""},
    34: {"title": "Mader's Reptile and Amphibian Medicine and Surgery (3rd)", "url": ""},
    35: {"title": "Current Therapy in Exotic Pet Practice", "url": ""},
    36: {"title": "Guinea pigs chapter (Quesenberry & Carpenter)", "url": ""},
    37: {"title": "Chinchillas chapter (Quesenberry & Carpenter)", "url": ""},
    38: {"title": "Equine Surgery (5th)", "url": ""},
    39: {"title": "Robinson's Current Therapy in Equine Medicine (7th)", "url": ""},
    40: {"title": "Pascoe's Principles & Practice of Equine Dermatology", "url": ""},
    41: {"title": "Diagnosis and Management of Lameness in the Horse", "url": ""},
    42: {"title": "Color Atlas of Diseases and Disorders of the Foal", "url": ""},
    43: {"title": "Plumb's Veterinary Drug Handbook (drug section)", "url": "https://www.wiley.com/en-us/Plumb%27s+Veterinary+Drug+Handbook-p-9781119344452"},
    44: {"title": "Veterinary Pharmacology and Therapeutics (10th)", "url": ""},
    45: {"title": "Papich Handbook of Veterinary Drugs (5th)", "url": ""},
    46: {"title": "BSAVA Small Animal Formulary (9th)", "url": ""},
    47: {"title": "犬と猫の治療薬ガイド EduOne (drug section)", "url": "https://search.eduone.jp/"},
    48: {"title": "Equine Medications", "url": ""},
    49: {"title": "Standards™ Differential Diagnosis Lists", "url": "https://standards.vet/features/differential-diagnosis-lists/"},
    50: {"title": "Cornell CONSULTANT", "url": "http://consultant.vet.cornell.edu/"},
    51: {"title": "DDx in Small Animal Medicine", "url": "https://apps.apple.com/us/app/ddx-in-small-animal-medicine/id1204472783"},
    52: {"title": "LafeberVet Differential Diagnosis", "url": "https://lafeber.com/vet/content_types/differential-diagnosis-list/"},
    53: {"title": "Clinician's Brief differential diagnosis", "url": "https://www.cliniciansbrief.com/article/veterinary-differential-diagnosis-symptoms-disease"},
    54: {"title": "VetGeni Veterinary Drug Database", "url": "https://www.vetgeni.com/veterinary-drug-database"},
    55: {"title": "Drugs.com Veterinary", "url": "https://www.drugs.com/vet/"},
    56: {"title": "Animal Drugs @ FDA", "url": "https://animaldrugsatfda.fda.gov/adafda/views/"},
    57: {"title": "VIN Veterinary Partner", "url": "https://veterinarypartner.vin.com/"},
    58: {"title": "World Veterinary Association", "url": "https://worldvet.org/evml/"},
    59: {"title": "Fundamentals of Veterinary Clinical Pathology (2nd)", "url": ""},
    60: {"title": "BSAVA Manual of Canine and Feline Clinical Pathology (3rd)", "url": ""},
}

SPECIES_REFERENCE_NUMBERS: Dict[str, List[int]] = {
    "dog": [1, 2, 7, 12, 13, 15, 16, 17, 23, 24, 26, 27, 28, 29, 30, 43, 44, 45, 46, 47, 59, 60],
    "cat": [1, 2, 7, 8, 12, 13, 15, 16, 17, 20, 21, 23, 24, 26, 27, 28, 29, 30, 43, 44, 45, 46, 47, 59, 60],
    "horse": [3, 11, 14, 38, 39, 40, 41, 42, 48, 59, 60],
    "rabbit": [4, 9, 10, 32, 35, 36],
    "hamster": [4, 10, 32, 35],
    "guinea_pig": [4, 10, 32, 35, 36],
    "chinchilla": [4, 10, 32, 35, 37],
    "ferret": [4, 10, 32, 35],
    "hedgehog": [10, 31, 32, 35],
    "sugar_glider": [10, 32, 35],
    "degu": [4, 10, 32, 35],
    "bird": [6, 33, 35, 52],
    "parakeet": [6, 33, 35, 52],
    "parrot": [6, 33, 35, 52],
    "reptile": [5, 34, 35],
    "tortoise": [5, 34, 35],
    "snake": [5, 34, 35],
    "lizard": [5, 34, 35],
    "amphibian": [5, 34, 35],
    "exotic_other": [10, 32, 35],
}

FIELD_REFERENCE_NUMBERS: Dict[str, List[int]] = {
    "description": [23, 24, 26],
    "pathophysiology": [7, 27, 28, 29],
    "causes": [7, 24],
    "prevention": [13, 24],
    "treatment": [12, 15, 43, 44, 45, 46],
    "prognosis": [26],
    "symptoms_summary": [23, 24],
}


def normalize_reference_numbers(reference_numbers: List[int]) -> List[int]:
    """Return sorted unique catalog numbers that exist in REFERENCE_CATALOG."""
    return sorted({int(n) for n in reference_numbers if int(n) in REFERENCE_CATALOG})


def build_reference_sources(reference_numbers: List[int]) -> List[Dict[str, str]]:
    """Convert reference numbers to API-safe evidence source entries."""
    sources: List[Dict[str, str]] = []
    for number in normalize_reference_numbers(reference_numbers):
        ref = REFERENCE_CATALOG[number]
        entry: Dict[str, str] = {
            "id": f"ref-{number}",
            "name": f"[{number}] {ref['title']}",
            "number": str(number),
        }
        entry["url"] = ref.get("url", "")
        sources.append(entry)
    return sources
