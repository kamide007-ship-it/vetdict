"""tortoise_diseases.py – リクガメの代表的な疾患

リクガメ科の動物で頻繁に見られる健康問題を取り上げ、症状から鑑別診断候補を
提示する簡易エンジンを提供します。ここで示される情報は教育目的のみであり、
獣医師の診断を代替するものではありません。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "shell_rot": {"ja": "甲羅腐敗", "en": "Shell rot"},
    "soft_shell": {"ja": "甲羅軟化", "en": "Soft shell"},
    "anorexia": {"ja": "食欲不振", "en": "Anorexia"},
    "swollen_eyes": {"ja": "眼腫脹", "en": "Swollen eyes"},
    "nasal_discharge": {"ja": "鼻水", "en": "Nasal discharge"},
    "respiratory_distress": {"ja": "呼吸困難", "en": "Respiratory distress"},
}

DISEASES: List[Dict] = [
    {
        "name": "甲羅腐敗症",
        "name_en": "Shell Rot",
        "symptoms": ["shell_rot", "anorexia"],
        "description": "甲羅に細菌やカビが侵入し壊死を起こす疾患。",
        "severity": "moderate",
        "recommended_tests": ["甲羅検査", "細菌培養"],
        "name_ja": "甲羅腐敗症",
        "description_ja": "甲羅に細菌やカビが侵入し壊死を起こす疾患。",
        "urgency": "medium",
    },
    {
        "name": "ビタミンA欠乏症",
        "name_en": "Vitamin A Deficiency",
        "symptoms": ["swollen_eyes", "nasal_discharge", "respiratory_distress", "anorexia"],
        "description": "不適切な食事によりビタミンAが不足し、目や呼吸器に症状が出る疾患。",
        "severity": "mild",
        "recommended_tests": ["血液検査", "栄養評価"],
        "name_ja": "ビタミンA欠乏症",
        "description_ja": "不適切な食事によりビタミンAが不足し、目や呼吸器に症状が出る疾患。",
        "urgency": "low",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
