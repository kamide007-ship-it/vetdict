"""Vaccine IDs mapped to the diseases they help prevent."""

from __future__ import annotations

VACCINE_TYPES: dict[str, dict[str, object]] = {
    "core_5in1": {
        "ja": "混合5種ワクチン",
        "en": "5-in-1 Vaccine",
        "components": ["DHPPC"],
        "preventable_diseases": [
            "Canine Parvovirus",
            "Canine Distemper",
            "Canine Infectious Hepatitis",
            "Parainfluenza",
        ],
        "schedule": "8週齢、12週齢、16週齢、1年後追加接種",
        "species": ["dog"],
        "required": True,
    },
    "core_8in1": {
        "ja": "混合8種ワクチン",
        "en": "8-in-1 Vaccine",
        "components": ["DHPPC+Lepto+Bordetella"],
        "preventable_diseases": [
            "Canine Parvovirus",
            "Canine Distemper",
            "Canine Infectious Hepatitis",
            "Parainfluenza",
            "Leptospirosis",
            "Kennel Cough (Bordetella)",
        ],
        "schedule": "8週齢、12週齢、16週齢、1年後追加接種",
        "species": ["dog"],
        "required": True,
    },
    "rabies": {
        "ja": "狂犬病ワクチン",
        "en": "Rabies Vaccine",
        "components": ["Rabies"],
        "preventable_diseases": ["Rabies", "Feline Rabies", "Ferret Rabies"],
        "schedule": "12週齢以降1回、以後法令や地域指針に従う",
        "species": ["dog", "cat", "ferret"],
        "required": True,
    },
    "fvrcp": {
        "ja": "猫用混合3種ワクチン",
        "en": "Feline FVRCP",
        "components": ["FVR+FCV+FPV"],
        "preventable_diseases": [
            "Feline Herpes Virus (FHV-1)",
            "Feline Calicivirus",
            "Feline Panleukopenia",
        ],
        "schedule": "8週齢、12週齢、16週齢、1年後追加接種",
        "species": ["cat"],
        "required": True,
    },
    "felv": {
        "ja": "猫白血病ワクチン",
        "en": "Feline Leukemia Vaccine",
        "components": ["FeLV"],
        "preventable_diseases": ["Feline Leukemia Virus (FeLV)"],
        "schedule": "8週齢、12週齢、1年後追加接種",
        "species": ["cat"],
        "required": False,
    },
}

VACCINES_BY_SPECIES = {
    species: [
        vaccine_id
        for vaccine_id, vaccine_data in VACCINE_TYPES.items()
        if species in vaccine_data.get("species", [])
    ]
    for species in {"dog", "cat", "ferret"}
}


def get_vaccines_for_species(species: str) -> dict[str, dict[str, object]]:
    """Return all known vaccines for a species."""
    vaccine_ids = VACCINES_BY_SPECIES.get(species, [])
    return {
        vaccine_id: VACCINE_TYPES[vaccine_id]
        for vaccine_id in vaccine_ids
        if vaccine_id in VACCINE_TYPES
    }


def get_preventable_diseases(vaccine_ids: list[str]) -> set[str]:
    """Return the diseases covered by the given vaccine IDs."""
    preventable: set[str] = set()
    for vaccine_id in vaccine_ids:
        vaccine_data = VACCINE_TYPES.get(vaccine_id, {})
        diseases = vaccine_data.get("preventable_diseases", [])
        preventable.update(str(disease) for disease in diseases)
    return preventable


def get_vaccine_schedule(vaccine_id: str) -> str:
    """Return the suggested schedule for a vaccine."""
    vaccine_data = VACCINE_TYPES.get(vaccine_id, {})
    return str(vaccine_data.get("schedule", "不明"))


def is_core_vaccine(vaccine_id: str) -> bool:
    """Return whether the vaccine is considered core."""
    vaccine_data = VACCINE_TYPES.get(vaccine_id, {})
    return bool(vaccine_data.get("required", False))


def get_vaccine_components(vaccine_id: str) -> list[str]:
    """Return the component labels for a vaccine."""
    vaccine_data = VACCINE_TYPES.get(vaccine_id, {})
    components = vaccine_data.get("components", [])
    return [str(component) for component in components]
