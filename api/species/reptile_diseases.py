"""reptile_diseases.py – 爬虫類の一般的な疾患と鑑別診断

トカゲやヘビ、カメといった広義の爬虫類で共通して見られる代表的な疾患を挙げ、
症状の一致度に基づいて候補を提示する簡易診断エンジンを提供します。ここで扱う
情報は教育目的であり、実際の診療は獣医師が行う必要があります。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "soft_shell": {"ja": "甲羅軟化/骨軟化", "en": "Soft shell/Bone softening"},
    "weakness": {"ja": "衰弱", "en": "Weakness"},
    "anorexia": {"ja": "食欲不振", "en": "Anorexia"},
    "respiratory_distress": {"ja": "呼吸困難", "en": "Respiratory distress"},
    "open_mouth_breathing": {"ja": "口を開けて呼吸", "en": "Open-mouth breathing"},
    "nasal_discharge": {"ja": "鼻水", "en": "Nasal discharge"},
}

DISEASES: List[Dict] = [
    {
        "name": "代謝性骨疾患",
        "name_en": "Metabolic Bone Disease",
        "symptoms": ["soft_shell", "weakness", "lethargy"],
        "description": "カルシウム不足や紫外線不足により骨が軟化する栄養性疾患。",
        "severity": "severe",
        "recommended_tests": ["血液検査", "X線検査"],
        "name_ja": "代謝性骨疾患",
        "description_ja": "カルシウム不足や紫外線不足により骨が軟化する栄養性疾患。",
        "urgency": "high",
    },
    {
        "name": "呼吸器感染症",
        "name_en": "Respiratory Infection",
        "symptoms": ["respiratory_distress", "open_mouth_breathing", "nasal_discharge", "lethargy"],
        "description": "低温や湿度管理不良などにより起こる感染症。",
        "severity": "moderate",
        "recommended_tests": ["口腔内検査", "レントゲン検査"],
        "name_ja": "呼吸器感染症",
        "description_ja": "低温や湿度管理不良などにより起こる感染症。",
        "urgency": "medium",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
