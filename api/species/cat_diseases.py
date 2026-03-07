"""Cat disease dictionary and analysis module.

This module defines a small set of example feline diseases and exposes an
`analyze_symptoms` function that leverages the generic species helper to
produce differential diagnosis results. Additional diseases can be added to
the ``DISEASES`` list following the same structure.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .helpers import ADVICE, analyze_symptoms_generic

# Example feline diseases. In a production system this list should be
# comprehensive and cover common and serious conditions affecting cats.
DISEASES: List[Dict[str, Any]] = [
    {
        "name": "Feline Upper Respiratory Infection",
        "name_ja": "猫の上部呼吸器感染症",
        "symptoms": {"coughing", "sneezing", "nasal_discharge", "fever"},
        "description": "A common viral or bacterial infection causing sneezing and nasal discharge.",
        "description_ja": "くしゃみや鼻水を引き起こすウイルスまたは細菌の感染症です。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam", "complete_blood_count"],
    },
    {
        "name": "Chronic Kidney Disease",
        "name_ja": "慢性腎疾患",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_loss", "appetite_loss"},
        "description": "Progressive loss of kidney function leading to increased drinking and weight loss.",
        "description_ja": "腎機能の進行性の低下により、多飲や体重減少を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "urinalysis"],
    },
]

# Symptom name mapping for feline symptoms used in this module. Only codes
# referenced in ``DISEASES`` need to be defined here.
SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "coughing": {"ja": "咳", "en": "Coughing"},
    "sneezing": {"ja": "くしゃみ", "en": "Sneezing"},
    "nasal_discharge": {"ja": "鼻水", "en": "Nasal Discharge"},
    "fever": {"ja": "発熱", "en": "Fever"},
    "excessive_thirst": {"ja": "多飲", "en": "Excessive Thirst"},
    "excessive_urination": {"ja": "頻尿", "en": "Excessive Urination"},
    "weight_loss": {"ja": "体重減少", "en": "Weight Loss"},
    "appetite_loss": {"ja": "食欲不振", "en": "Appetite Loss"},
}


def analyze_symptoms(symptoms: List[str], age_stage: str = "", breed: str | None = None) -> Dict[str, Any]:
    """Analyze feline symptoms and return suspected diseases.

    Parameters
    ----------
    symptoms:
        A list of symptom identifier strings.
    age_stage:
        Optional age stage (unused for cats in this example).
    breed:
        Not used for cats; included for interface compatibility.

    Returns
    -------
    dict
        Analysis result in the same format as the dog symptom checker.
    """
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
