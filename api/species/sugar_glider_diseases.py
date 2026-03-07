"""sugar_glider_diseases.py – フクロモモンガの疾患データと鑑別診断

このモジュールではフクロモモンガ（シュガーグライダー）の代表的な疾患を簡易的に
取り上げ、ユーザーが入力した症状から鑑別候補を提示します。ここで提供する情報は
一般的なものに限られ、最終的な診断は獣医師が行う必要があります。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "weakness": {"ja": "衰弱", "en": "Weakness"},
    "seizures": {"ja": "痙攣", "en": "Seizures"},
    "bone_deformity": {"ja": "骨変形", "en": "Bone deformity"},
    "respiratory_distress": {"ja": "呼吸困難", "en": "Respiratory distress"},
    "nasal_discharge": {"ja": "鼻水", "en": "Nasal discharge"},
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
}

DISEASES: List[Dict] = [
    {
        "name": "代謝性骨疾患",
        "name_en": "Metabolic Bone Disease",
        "symptoms": ["weakness", "bone_deformity", "seizures"],
        "description": "カルシウムやビタミンD不足により骨が軟化する栄養性疾患。",
        "severity": "severe",
        "recommended_tests": ["血液生化学検査", "X線検査"],
        "name_ja": "代謝性骨疾患",
        "description_ja": "カルシウムやビタミンD不足により骨が軟化する栄養性疾患。",
        "urgency": "high",
    },
    {
        "name": "呼吸器感染症",
        "name_en": "Respiratory Infection",
        "symptoms": ["respiratory_distress", "nasal_discharge", "lethargy"],
        "description": "細菌やウイルスによる呼吸器系の感染症。",
        "severity": "moderate",
        "recommended_tests": ["胸部レントゲン", "血液検査"],
        "name_ja": "呼吸器感染症",
        "description_ja": "細菌やウイルスによる呼吸器系の感染症。",
        "urgency": "medium",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    """フクロモモンガ用の鑑別診断関数。"""
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
