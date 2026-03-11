"""Landing page veterinary references used for disease evidence mapping."""

from __future__ import annotations

from typing import Dict, List

# Canonical references shown in templates/index.html.
REFERENCE_CATALOG: Dict[int, Dict[str, str]] = {
    1: {"title": "Small Animal Internal Medicine (6th)", "url": ""},
    2: {"title": "Textbook of Veterinary Internal Medicine (8th)", "url": ""},
    3: {"title": "Equine Internal Medicine (4th)", "url": ""},
    4: {"title": "Ferrets, Rabbits, and Rodents (4th)", "url": ""},
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
    23: {"title": "Medical History and Physical Examination in Companion Animals", "url": ""},
    24: {"title": "Clinical signs approach to differential diagnosis", "url": ""},
    26: {"title": "Clinical Veterinary Advisor: Dogs and Cats", "url": ""},
    31: {"title": "Hedgehog health and disease", "url": ""},
    32: {"title": "BSAVA Manual of Exotic Pets", "url": ""},
    33: {"title": "Avian Medicine and Surgery in Practice", "url": ""},
    34: {"title": "Mader's Reptile and Amphibian Medicine and Surgery", "url": ""},
    35: {"title": "Current Therapy in Exotic Pet Practice", "url": ""},
    38: {"title": "Equine Surgery (5th)", "url": ""},
    39: {"title": "Robinson's Current Therapy in Equine Medicine", "url": ""},
    59: {"title": "Fundamentals of Veterinary Clinical Pathology", "url": ""},
}

SPECIES_REFERENCE_NUMBERS: Dict[str, List[int]] = {
    "dog": [1, 2, 7, 12, 13, 15, 23, 24, 26],
    "cat": [1, 2, 7, 8, 12, 13, 15, 23, 24, 26],
    "horse": [3, 11, 14, 38, 39, 59],
    "rabbit": [4, 9, 10, 32, 35],
    "hamster": [4, 10, 32, 35],
    "guinea_pig": [4, 10, 32, 35],
    "chinchilla": [4, 10, 32, 35],
    "ferret": [4, 10, 32, 35],
    "hedgehog": [10, 31, 32, 35],
    "sugar_glider": [10, 32, 35],
    "degu": [4, 10, 32, 35],
    "bird": [6, 33, 35],
    "parakeet": [6, 33, 35],
    "parrot": [6, 33, 35],
    "reptile": [5, 34, 35],
    "tortoise": [5, 34, 35],
    "snake": [5, 34, 35],
    "lizard": [5, 34, 35],
    "amphibian": [5, 34, 35],
    "exotic_other": [10, 32, 35],
}

FIELD_REFERENCE_NUMBERS: Dict[str, List[int]] = {
    "description": [23, 24],
    "pathophysiology": [7],
    "causes": [7, 24],
    "prevention": [13],
    "treatment": [12, 15],
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
