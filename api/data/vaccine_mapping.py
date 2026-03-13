"""Vaccine-preventable diseases mapping for VetDict.

Maps vaccination status to preventable diseases for diagnostic exclusion.
Enables reduction of differential diagnosis by excluding vaccine-preventable
diseases when appropriate vaccination records are present.

Structure:
  VACCINE_TYPES[vaccine_name] = {
    "ja": "ワクチン名（日本語）",
    "en": "Vaccine Name (English)",
    "preventable_diseases": ["Disease1", "Disease2", ...],
    "schedule": "推奨接種スケジュール",
    "species": ["dog", "cat", ...],
  }
"""

from typing import Dict, List

# Vaccine types and their preventable diseases
VACCINE_TYPES: Dict[str, Dict] = {
    "core_5in1": {
        "ja": "混合5種ワクチン",
        "en": "5-in-1 Vaccine (DPPi+L+C)",
        "components": ["DHPPC"],  # Distemper, Hepatitis, Parvovirus, Parainfluenza, Coronavirus
        "preventable_diseases": [
            "Canine Parvovirus",
            "Canine Distemper",
            "Canine Infectious Hepatitis",
            "Parainfluenza",
            "Canine Coronavirus",
        ],
        "schedule": "8週齢、12週齢、16週齢、1年後追加接種",
        "species": ["dog"],
        "required": True,
    },
    "core_8in1": {
        "ja": "混合8種ワクチン",
        "en": "8-in-1 Vaccine (DPPi+L+C+LeptoBordetella)",
        "components": ["DHPPC+Lepto+Bordetella"],
        "preventable_diseases": [
            "Canine Parvovirus",
            "Canine Distemper",
            "Canine Infectious Hepatitis",
            "Parainfluenza",
            "Canine Coronavirus",
            "Leptospirosis",
            "Bordetella bronchiseptica",
        ],
        "schedule": "8週齢、12週齢、16週齢、1年後追加接種",
        "species": ["dog"],
        "required": True,
    },
    "rabies": {
        "ja": "狂犬病ワクチン",
        "en": "Rabies Vaccine",
        "components": ["Rabies"],
        "preventable_diseases": [
            "Rabies",
        ],
        "schedule": "12週齢以降1回、1年後追加接種、以降3年毎",
        "species": ["dog", "cat"],
        "required": True,
    },
    "fvrcp": {
        "ja": "猫用混合3種ワクチン",
        "en": "Feline FVRCP (Feline Viral Rhinotracheitis, Calicivirus, Panleukopenia)",
        "components": ["FVR+FCV+FPV"],
        "preventable_diseases": [
            "Feline Viral Rhinotracheitis",
            "Feline Calicivirus",
            "Feline Panleukopenia",
        ],
        "schedule": "8週齢、12週齢、16週齢、1年後追加接種",
        "species": ["cat"],
        "required": True,
    },
    "felv": {
        "ja": "猫白血病ワクチン",
        "en": "Feline Leukemia Virus (FeLV) Vaccine",
        "components": ["FeLV"],
        "preventable_diseases": [
            "Feline Leukemia Virus (FeLV)",
        ],
        "schedule": "8週齢、12週齢、1年後追加接種",
        "species": ["cat"],
        "required": False,
    },
    "felv_fiv": {
        "ja": "猫白血病・猫免疫不全ウイルスワクチン",
        "en": "FeLV/FIV Vaccine",
        "components": ["FeLV+FIV"],
        "preventable_diseases": [
            "Feline Leukemia Virus (FeLV)",
            "Feline Immunodeficiency Virus (FIV)",
        ],
        "schedule": "8週齢、12週齢、1年後追加接種",
        "species": ["cat"],
        "required": False,
    },
    "leptospirosis": {
        "ja": "レプトスピラワクチン",
        "en": "Leptospirosis Vaccine",
        "components": ["Leptospirosis"],
        "preventable_diseases": [
            "Leptospirosis",
        ],
        "schedule": "8週齢、12週齢、16週齢、1年後追加接種",
        "species": ["dog"],
        "required": False,
    },
    "bordetella": {
        "ja": "ボルデテラワクチン",
        "en": "Bordetella Vaccine",
        "components": ["Bordetella"],
        "preventable_diseases": [
            "Bordetella bronchiseptica",
            "Tracheobronchitis (Kennel Cough)",
        ],
        "schedule": "8週齢以降、1年毎",
        "species": ["dog"],
        "required": False,
    },
    "influenza": {
        "ja": "犬インフルエンザワクチン",
        "en": "Canine Influenza Vaccine",
        "components": ["CIV"],
        "preventable_diseases": [
            "Canine Influenza Virus",
            "Canine Tracheobronchitis",
        ],
        "schedule": "初回2回（2-4週間間隔）、1年毎",
        "species": ["dog"],
        "required": False,
    },
    "giardia": {
        "ja": "ジアルジアワクチン",
        "en": "Giardia Vaccine",
        "components": ["Giardia"],
        "preventable_diseases": [
            "Giardiasis",
        ],
        "schedule": "初回3回（1-2週間間隔）、1年毎",
        "species": ["dog"],
        "required": False,
    },
}

# Get vaccines by species
VACCINES_BY_SPECIES = {
    "dog": [v_id for v_id, v in VACCINE_TYPES.items() if "dog" in v.get("species", [])],
    "cat": [v_id for v_id, v in VACCINE_TYPES.items() if "cat" in v.get("species", [])],
}

# Get preventable diseases by vaccine
PREVENTABLE_BY_VACCINE: Dict[str, List[str]] = {
    vaccine_id: vaccine_data.get("preventable_diseases", [])
    for vaccine_id, vaccine_data in VACCINE_TYPES.items()
}


def get_vaccines_for_species(species: str) -> Dict[str, Dict]:
    """Get all vaccines relevant to a species.

    Args:
        species: Species ID (e.g., "dog", "cat")

    Returns:
        Dictionary of vaccine_id -> vaccine data
    """
    vaccine_ids = VACCINES_BY_SPECIES.get(species, [])
    return {v_id: VACCINE_TYPES[v_id] for v_id in vaccine_ids if v_id in VACCINE_TYPES}


def get_preventable_diseases(vaccine_ids: List[str]) -> set[str]:
    """Get all diseases preventable by the given vaccines.

    Args:
        vaccine_ids: List of vaccine IDs (e.g., ["core_5in1", "rabies"])

    Returns:
        Set of disease names preventable by these vaccines
    """
    preventable = set()
    for vaccine_id in vaccine_ids:
        diseases = PREVENTABLE_BY_VACCINE.get(vaccine_id, [])
        preventable.update(diseases)
    return preventable


def get_vaccine_schedule(vaccine_id: str) -> str:
    """Get recommended vaccination schedule for a vaccine.

    Args:
        vaccine_id: Vaccine ID

    Returns:
        Schedule string in Japanese
    """
    if vaccine_id not in VACCINE_TYPES:
        return "不明"
    return VACCINE_TYPES[vaccine_id].get("schedule", "不明")


def is_core_vaccine(vaccine_id: str) -> bool:
    """Check if a vaccine is a core (recommended) vaccine.

    Args:
        vaccine_id: Vaccine ID

    Returns:
        True if core vaccine, False otherwise
    """
    if vaccine_id not in VACCINE_TYPES:
        return False
    return VACCINE_TYPES[vaccine_id].get("required", False)


def get_vaccine_components(vaccine_id: str) -> List[str]:
    """Get vaccine components.

    Args:
        vaccine_id: Vaccine ID

    Returns:
        List of component abbreviations
    """
    if vaccine_id not in VACCINE_TYPES:
        return []
    return VACCINE_TYPES[vaccine_id].get("components", [])
