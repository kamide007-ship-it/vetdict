"""Hamster disease dictionary and analysis module.

Contains a limited set of conditions commonly seen in hamsters. The
``analyze_symptoms`` function wraps the generic helper.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .helpers import ADVICE, analyze_symptoms_generic


DISEASES: List[Dict[str, Any]] = [
    {
        "name": "Wet Tail",
        "name_ja": "ウェットテイル",
        "symptoms": {"diarrhea", "lethargy", "appetite_loss", "dehydration"},
        "description": "A bacterial infection also known as proliferative ileitis, causing severe diarrhea.",
        "description_ja": "重度の下痢を引き起こす腸の細菌感染症です。",
        "urgency": "high",
        "recommended_tests": ["stool_culture", "physical_exam"],
    },
    {
        "name": "Diabetes",
        "name_ja": "糖尿病",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_loss"},
        "description": "A metabolic disorder characterized by excessive drinking and weight loss.",
        "description_ja": "多飲や体重減少を特徴とする代謝性疾患です。",
        "urgency": "moderate",
        "recommended_tests": ["blood_glucose", "urinalysis"],
    },
]

SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "diarrhea": {"ja": "下痢", "en": "Diarrhea"},
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "appetite_loss": {"ja": "食欲不振", "en": "Appetite Loss"},
    "dehydration": {"ja": "脱水", "en": "Dehydration"},
    "excessive_thirst": {"ja": "多飲", "en": "Excessive Thirst"},
    "excessive_urination": {"ja": "頻尿", "en": "Excessive Urination"},
    "weight_loss": {"ja": "体重減少", "en": "Weight Loss"},
}


def analyze_symptoms(symptoms: List[str], age_stage: str = "", breed: str | None = None) -> Dict[str, Any]:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
