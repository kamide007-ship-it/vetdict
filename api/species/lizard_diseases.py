"""lizard_diseases.py – トカゲ類の代表的な疾患

トカゲ類でしばしば報告される疾患を少数例としてまとめ、症状から鑑別診断候補
を生成する機能を提供します。情報は教育目的であり、獣医師の診断を置き換える
ものではありません。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "soft_bones": {"ja": "骨軟化", "en": "Soft bones"},
    "weakness": {"ja": "衰弱", "en": "Weakness"},
    "sunken_eyes": {"ja": "眼窩陥没", "en": "Sunken eyes"},
    "dry_skin": {"ja": "乾燥肌", "en": "Dry skin"},
    "decreased_skin_elasticity": {"ja": "皮膚の弾力低下", "en": "Decreased skin elasticity"},
}

DISEASES: List[Dict] = [
    {
        "name": "代謝性骨疾患",
        "name_en": "Metabolic Bone Disease",
        "symptoms": ["soft_bones", "weakness", "lethargy"],
        "description": "カルシウム不足により骨が脆くなる栄養性疾患。",
        "severity": "severe",
        "recommended_tests": ["血液検査", "X線検査"],
        "name_ja": "代謝性骨疾患",
        "description_ja": "カルシウム不足により骨が脆くなる栄養性疾患。",
        "urgency": "high",
    },
    {
        "name": "脱水症",
        "name_en": "Dehydration",
        "symptoms": ["sunken_eyes", "dry_skin", "decreased_skin_elasticity", "lethargy"],
        "description": "水分不足により全身状態が悪化する状態。",
        "severity": "moderate",
        "recommended_tests": ["物理的評価", "血液検査"],
        "name_ja": "脱水症",
        "description_ja": "水分不足により全身状態が悪化する状態。",
        "urgency": "medium",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
