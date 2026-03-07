"""bird_diseases.py – 鳥類共通の疾患データと鑑別診断

鳥類に広く見られる代表的な疾患をいくつか掲載し、症状から鑑別診断候補を
導き出す簡易的なエンジンを提供します。具体的な診断は必ず獣医師にご相談
ください。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "respiratory_distress": {"ja": "呼吸困難", "en": "Respiratory distress"},
    "nasal_discharge": {"ja": "鼻水", "en": "Nasal discharge"},
    "weight_loss": {"ja": "体重減少", "en": "Weight loss"},
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "anorexia": {"ja": "食欲不振", "en": "Anorexia"},
}

DISEASES: List[Dict] = [
    {
        "name": "オウム病 (クラミジア症)",
        "name_en": "Avian Chlamydiosis",
        "symptoms": ["respiratory_distress", "nasal_discharge", "weight_loss"],
        "description": "クラミジア感染症により呼吸器症状と体重減少を起こす疾患。人獣共通感染症として知られる。",
        "severity": "moderate",
        "recommended_tests": ["PCR検査", "血液検査"],
        "name_ja": "オウム病 (クラミジア症)",
        "description_ja": "クラミジア感染症により呼吸器症状と体重減少を起こす疾患。人獣共通感染症として知られる。",
        "urgency": "medium",
    },
    {
        "name": "アスペルギルス症",
        "name_en": "Aspergillosis",
        "symptoms": ["respiratory_distress", "lethargy", "anorexia"],
        "description": "真菌感染により呼吸器系に病変が生じる疾患。",
        "severity": "severe",
        "recommended_tests": ["レントゲン検査", "真菌培養"],
        "name_ja": "アスペルギルス症",
        "description_ja": "真菌感染により呼吸器系に病変が生じる疾患。",
        "urgency": "high",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    """鳥類用の鑑別診断関数。"""
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
