"""parrot_diseases.py – オウム類（大型）の代表的疾患

コンゴウインコやヨウムなど大型オウム類で見られる疾患を簡易的に示し、
症状から鑑別診断の候補を生成します。教育目的のみを想定しており、
最終的な診断や治療は獣医師にご相談ください。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "respiratory_distress": {"ja": "呼吸困難", "en": "Respiratory distress"},
    "feather_plucking": {"ja": "羽毛むしり", "en": "Feather plucking"},
    "skin_lesions": {"ja": "皮膚病変", "en": "Skin lesions"},
    "weight_loss": {"ja": "体重減少", "en": "Weight loss"},
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "anorexia": {"ja": "食欲不振", "en": "Anorexia"},
}

DISEASES: List[Dict] = [
    {
        "name": "アスペルギルス症",
        "name_en": "Aspergillosis",
        "symptoms": ["respiratory_distress", "lethargy", "anorexia"],
        "description": "真菌感染による呼吸器疾患。大型オウムで重篤になることがある。",
        "severity": "severe",
        "recommended_tests": ["胸部レントゲン", "真菌培養"],
        "name_ja": "アスペルギルス症",
        "description_ja": "真菌感染による呼吸器疾患。大型オウムで重篤になることがある。",
        "urgency": "high",
    },
    {
        "name": "羽毛むしり症候群",
        "name_en": "Feather Plucking Syndrome",
        "symptoms": ["feather_plucking", "skin_lesions", "weight_loss"],
        "description": "ストレスや環境要因により自ら羽毛をむしる行動障害。",
        "severity": "chronic",
        "recommended_tests": ["ストレス評価", "皮膚検査"],
        "name_ja": "羽毛むしり症候群",
        "description_ja": "ストレスや環境要因により自ら羽毛をむしる行動障害。",
        "urgency": "low",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
