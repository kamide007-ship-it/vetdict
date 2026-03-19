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
    "equine_rabies": {
        "ja": "馬用狂犬病ワクチン",
        "en": "Equine Rabies Vaccine",
        "components": ["Rabies"],
        "preventable_diseases": ["Rabies"],
        "schedule": "初回接種後、年1回追加接種",
        "species": ["horse"],
        "required": True,
    },
    "equine_influenza": {
        "ja": "馬インフルエンザワクチン",
        "en": "Equine Influenza Vaccine",
        "components": ["EIV"],
        "preventable_diseases": [
            "Equine Influenza",
            "馬インフルエンザ",
        ],
        "schedule": "初回2回接種（3-6週間隔）、6ヶ月後追加、以後年1回",
        "species": ["horse"],
        "required": True,
    },
    "equine_herpes": {
        "ja": "馬ヘルペスウイルスワクチン",
        "en": "Equine Herpesvirus Vaccine",
        "components": ["EHV-1", "EHV-4"],
        "preventable_diseases": [
            "Equine Herpesvirus (EHV)",
            "馬ヘルペスウイルス感染症",
            "Equine Rhinopneumonitis",
        ],
        "schedule": "6ヶ月ごと、妊娠馬は妊娠5・7・9ヶ月に追加",
        "species": ["horse"],
        "required": False,
    },
    "equine_tetanus": {
        "ja": "馬用破傷風ワクチン",
        "en": "Equine Tetanus Toxoid",
        "components": ["Tetanus"],
        "preventable_diseases": [
            "Tetanus",
            "破傷風",
        ],
        "schedule": "初回2回接種（4-6週間隔）、1年後追加、以後年1回",
        "species": ["horse"],
        "required": True,
    },
    "equine_wee_eee": {
        "ja": "馬脳炎ワクチン（東部・西部）",
        "en": "Eastern/Western Equine Encephalomyelitis Vaccine",
        "components": ["EEE", "WEE"],
        "preventable_diseases": [
            "Eastern Equine Encephalomyelitis",
            "Western Equine Encephalomyelitis",
            "馬脳炎",
        ],
        "schedule": "年1回（蚊の活動期前に接種）",
        "species": ["horse"],
        "required": True,
    },
    "equine_wnv": {
        "ja": "馬用ウエストナイルウイルスワクチン",
        "en": "West Nile Virus Vaccine",
        "components": ["WNV"],
        "preventable_diseases": [
            "West Nile Virus",
            "ウエストナイル熱",
        ],
        "schedule": "年1回（蚊の活動期前に接種）",
        "species": ["horse"],
        "required": True,
    },
    "equine_strangles": {
        "ja": "馬用腺疫ワクチン",
        "en": "Strangles Vaccine",
        "components": ["S. equi"],
        "preventable_diseases": [
            "Strangles",
            "腺疫",
        ],
        "schedule": "初回2-3回接種、以後年1回（リスクベース）",
        "species": ["horse"],
        "required": False,
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
    "rhdv": {
        "ja": "ウサギ出血病ワクチン",
        "en": "Rabbit Hemorrhagic Disease Vaccine",
        "components": ["RHDV1", "RHDV2"],
        "preventable_diseases": [
            "Rabbit Hemorrhagic Disease (RHDV)",
            "Rabbit Hemorrhagic Disease Virus 2 (RHDV2)",
        ],
        "schedule": "10週齢以降1回、1年後追加接種",
        "species": ["rabbit"],
        "required": True,
    },
    "myxomatosis": {
        "ja": "粘液腫症ワクチン",
        "en": "Myxomatosis Vaccine",
        "components": ["Myxoma"],
        "preventable_diseases": ["Myxomatosis"],
        "schedule": "6週齢以降1回、6ヶ月後追加接種",
        "species": ["rabbit"],
        "required": True,
    },
    "ferret_cdv": {
        "ja": "フェレット用ジステンパーワクチン",
        "en": "Ferret Canine Distemper Vaccine",
        "components": ["CDV-ferret"],
        "preventable_diseases": ["Canine Distemper"],
        "schedule": "8週齢、12週齢、16週齢、1年後追加接種",
        "species": ["ferret"],
        "required": True,
    },
}

VACCINES_BY_SPECIES = {
    species: [
        vaccine_id
        for vaccine_id, vaccine_data in VACCINE_TYPES.items()
        if species in vaccine_data.get("species", [])
    ]
    for species in {"dog", "cat", "ferret", "rabbit", "horse"}
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
