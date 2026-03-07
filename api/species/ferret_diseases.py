"""Ferret disease dictionary and analysis module.

Defines a couple of conditions typical in ferrets. The analysis function
follows the generic species helper conventions.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .helpers import ADVICE, analyze_symptoms_generic


DISEASES: List[Dict[str, Any]] = [
    {
        "name": "Adrenal Disease",
        "name_ja": "副腎疾患",
        "symptoms": {"hair_loss", "itching", "weight_loss"},
        "description": "Overproduction of sex hormones leading to hair loss and itching.",
        "description_ja": "性ホルモンの過剰分泌により脱毛やかゆみが起こります。",
        "urgency": "moderate",
        "recommended_tests": ["hormone_panel", "ultrasound"],
    },
    {
        "name": "Insulinoma",
        "name_ja": "インスリノーマ",
        "symptoms": {"lethargy", "seizures", "collapse"},
        "description": "A pancreatic tumor causing low blood sugar, resulting in weakness and seizures.",
        "description_ja": "膵臓腫瘍により低血糖が起こり、虚脱や痙攣がみられます。",
        "urgency": "high",
        "recommended_tests": ["blood_glucose", "abdominal_ultrasound"],
    },
]

SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "hair_loss": {"ja": "脱毛", "en": "Hair Loss"},
    "itching": {"ja": "かゆみ", "en": "Itching"},
    "weight_loss": {"ja": "体重減少", "en": "Weight Loss"},
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "seizures": {"ja": "痙攣", "en": "Seizures"},
    "collapse": {"ja": "虚脱・失神", "en": "Collapse / Fainting"},
}


def analyze_symptoms(symptoms: List[str], age_stage: str = "", breed: str | None = None) -> Dict[str, Any]:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
