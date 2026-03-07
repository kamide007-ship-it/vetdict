"""Rabbit disease dictionary and analysis module.

Defines a small set of common conditions affecting rabbits and provides an
analysis function for symptom input. This module uses the shared helper
functions to compute differential diagnoses.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .helpers import ADVICE, analyze_symptoms_generic


DISEASES: List[Dict[str, Any]] = [
    {
        "name": "Gastrointestinal Stasis",
        "name_ja": "消化管うっ滞",
        "symptoms": {"appetite_loss", "lethargy", "abdominal_pain", "constipation", "dehydration"},
        "description": "A potentially life‑threatening slowdown of the gastrointestinal tract common in rabbits.",
        "description_ja": "ウサギに多い危険な消化管の運動低下です。",
        "urgency": "high",
        "recommended_tests": ["physical_exam", "abdominal_xray"],
    },
    {
        "name": "Dental Disease",
        "name_ja": "歯科疾患",
        "symptoms": {"drooling", "appetite_loss", "weight_loss"},
        "description": "Overgrown teeth leading to drooling and difficulty eating.",
        "description_ja": "過長歯により流涎や食欲不振が起こります。",
        "urgency": "moderate",
        "recommended_tests": ["oral_exam", "head_radiographs"],
    },
]

SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "appetite_loss": {"ja": "食欲不振", "en": "Appetite Loss"},
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "abdominal_pain": {"ja": "腹痛", "en": "Abdominal Pain"},
    "constipation": {"ja": "便秘", "en": "Constipation"},
    "dehydration": {"ja": "脱水", "en": "Dehydration"},
    "drooling": {"ja": "よだれ・流涎", "en": "Drooling / Hypersalivation"},
    "weight_loss": {"ja": "体重減少", "en": "Weight Loss"},
}


def analyze_symptoms(symptoms: List[str], age_stage: str = "", breed: str | None = None) -> Dict[str, Any]:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
