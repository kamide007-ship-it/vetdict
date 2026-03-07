"""snake_diseases.py – ヘビの代表的な疾患

ヘビ類で報告される代表的な疾患をいくつか収録し、症状に基づく鑑別診断を
簡易的に提供します。ここに記載された内容は一般的な情報であり、必ずしも
全ての症例に当てはまるわけではありません。診断は獣医師にご相談ください。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "regurgitation": {"ja": "吐出", "en": "Regurgitation"},
    "paralysis": {"ja": "麻痺", "en": "Paralysis"},
    "stargazing": {"ja": "スターゲイジング", "en": "Stargazing"},
    "scale_lesions": {"ja": "鱗の病変", "en": "Scale lesions"},
    "skin_discoloration": {"ja": "皮膚変色", "en": "Skin discoloration"},
    "anorexia": {"ja": "食欲不振", "en": "Anorexia"},
}

DISEASES: List[Dict] = [
    {
        "name": "包括体疾患",
        "name_en": "Inclusion Body Disease",
        "symptoms": ["regurgitation", "paralysis", "stargazing", "anorexia"],
        "description": "多くはボアやニシキヘビで見られる致死性のウイルス感染症。",
        "severity": "critical",
        "recommended_tests": ["PCR検査", "ウイルス検査"],
        "name_ja": "包括体疾患",
        "description_ja": "多くはボアやニシキヘビで見られる致死性のウイルス感染症。",
        "urgency": "high",
    },
    {
        "name": "スケイルロット",
        "name_en": "Scale Rot",
        "symptoms": ["scale_lesions", "skin_discoloration", "anorexia"],
        "description": "不衛生な環境や湿度不良により鱗に炎症や変色が起こる疾患。",
        "severity": "moderate",
        "recommended_tests": ["皮膚検査", "細菌培養"],
        "name_ja": "スケイルロット",
        "description_ja": "不衛生な環境や湿度不良により鱗に炎症や変色が起こる疾患。",
        "urgency": "medium",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
