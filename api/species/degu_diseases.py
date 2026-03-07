"""degu_diseases.py – デグーの疾患データと鑑別診断

デグーは小型齧歯類の一種で、特有の健康問題を持ちます。このモジュールでは
デグーに一般的な疾患をいくつか示し、症状から簡易的な鑑別診断を行える関数
を提供します。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "polyuria": {"ja": "多尿", "en": "Polyuria"},
    "polydipsia": {"ja": "多飲", "en": "Polydipsia"},
    "cataract": {"ja": "白内障", "en": "Cataract"},
    "weight_loss": {"ja": "体重減少", "en": "Weight loss"},
    "dental_malocclusion": {"ja": "不正咬合", "en": "Malocclusion"},
    "drooling": {"ja": "流涎", "en": "Drooling"},
    "anorexia": {"ja": "食欲不振", "en": "Anorexia"},
}

DISEASES: List[Dict] = [
    {
        "name": "糖尿病",
        "name_en": "Diabetes Mellitus",
        "symptoms": ["polyuria", "polydipsia", "weight_loss", "cataract"],
        "description": "血糖コントロールの障害により多飲多尿や体重減少が起こる代謝性疾患。",
        "severity": "moderate",
        "recommended_tests": ["血糖検査", "尿検査"],
        "name_ja": "糖尿病",
        "description_ja": "血糖コントロールの障害により多飲多尿や体重減少が起こる代謝性疾患。",
        "urgency": "medium",
    },
    {
        "name": "歯科疾患",
        "name_en": "Dental Disease",
        "symptoms": ["dental_malocclusion", "drooling", "anorexia", "weight_loss"],
        "description": "歯の過成長や不正咬合により食欲が低下する疾患。",
        "severity": "mild",
        "recommended_tests": ["口腔内検査", "頭部X線検査"],
        "name_ja": "歯科疾患",
        "description_ja": "歯の過成長や不正咬合により食欲が低下する疾患。",
        "urgency": "low",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    """デグー用の鑑別診断関数。"""
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
