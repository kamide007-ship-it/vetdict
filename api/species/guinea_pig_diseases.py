"""Guinea pig disease dictionary and analysis module.

Includes a couple of example diseases commonly seen in guinea pigs.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .helpers import ADVICE, analyze_symptoms_generic


DISEASES: List[Dict[str, Any]] = [
    {
        "name": "Scurvy (Vitamin C Deficiency)",
        "name_ja": "ビタミンC欠乏症",
        "symptoms": {"lethargy", "swollen_joints", "pain_on_touch"},
        "description": "A deficiency of vitamin C causing weakness and joint swelling.",
        "description_ja": "ビタミンC欠乏により虚弱や関節の腫れが起こります。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam", "diet_history"],
    },
    {
        "name": "Pododermatitis",
        "name_ja": "足底皮膚炎",
        "symptoms": {"limping_fl", "limping_fr", "swollen_joints"},
        "description": "Inflammation of the foot pads leading to lameness.",
        "description_ja": "足底の炎症により跛行が起こります。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam", "x_rays"],
    },
]

SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "swollen_joints": {"ja": "関節の腫れ", "en": "Swollen Joints"},
    "pain_on_touch": {"ja": "触ると痛がる", "en": "Pain on Touch"},
    "limping_fl": {"ja": "跛行（左前肢）", "en": "Limping (Front Left)"},
    "limping_fr": {"ja": "跛行（右前肢）", "en": "Limping (Front Right)"},
}


def analyze_symptoms(symptoms: List[str], age_stage: str = "", breed: str | None = None) -> Dict[str, Any]:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
