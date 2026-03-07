"""Chinchilla disease dictionary and analysis module.

Provides a few representative conditions for chinchillas with an analysis
function using the shared helper.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .helpers import ADVICE, analyze_symptoms_generic


DISEASES: List[Dict[str, Any]] = [
    {
        "name": "Dental Disease",
        "name_ja": "歯科疾患",
        "symptoms": {"drooling", "appetite_loss", "weight_loss"},
        "description": "Malocclusion or overgrown teeth leading to difficulty eating and drooling.",
        "description_ja": "不正咬合や歯の過長により食事が困難となり流涎が起こります。",
        "urgency": "moderate",
        "recommended_tests": ["oral_exam", "skull_radiographs"],
    },
    {
        "name": "Heat Stroke",
        "name_ja": "熱中症",
        "symptoms": {"excessive_panting", "lethargy", "collapse"},
        "description": "Overheating due to high ambient temperatures causing panting and collapse.",
        "description_ja": "高温環境による体温上昇でパンティングや虚脱が起こります。",
        "urgency": "high",
        "recommended_tests": ["physical_exam", "body_temperature"],
    },
]

SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "drooling": {"ja": "よだれ・流涎", "en": "Drooling / Hypersalivation"},
    "appetite_loss": {"ja": "食欲不振", "en": "Appetite Loss"},
    "weight_loss": {"ja": "体重減少", "en": "Weight Loss"},
    "excessive_panting": {"ja": "過度のパンティング", "en": "Excessive Panting"},
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "collapse": {"ja": "虚脱・失神", "en": "Collapse / Fainting"},
}


def analyze_symptoms(symptoms: List[str], age_stage: str = "", breed: str | None = None) -> Dict[str, Any]:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
