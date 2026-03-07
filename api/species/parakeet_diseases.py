"""parakeet_diseases.py – インコ（小型オウム類）の疾患データ

このモジュールではセキセイインコやラブバードなどの小型オウム類で見られる
代表的な疾患を簡易的に紹介し、症状リストから鑑別候補を生成します。ここで
提供する情報は教育目的であり、診断や治療は獣医師に相談してください。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "feather_loss": {"ja": "羽毛喪失", "en": "Feather loss"},
    "beak_deformity": {"ja": "嘴の変形", "en": "Beak deformity"},
    "weight_loss": {"ja": "体重減少", "en": "Weight loss"},
    "regurgitation": {"ja": "吐出", "en": "Regurgitation"},
    "neurological_signs": {"ja": "神経症状", "en": "Neurological signs"},
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
}

DISEASES: List[Dict] = [
    {
        "name": "嘴羽毛病",
        "name_en": "Psittacine Beak and Feather Disease",
        "symptoms": ["feather_loss", "beak_deformity", "weight_loss"],
        "description": "サーコウイルス感染により羽毛や嘴に異常をきたす慢性疾患。",
        "severity": "chronic",
        "recommended_tests": ["PCR検査", "羽毛検査"],
        "name_ja": "嘴羽毛病",
        "description_ja": "サーコウイルス感染により羽毛や嘴に異常をきたす慢性疾患。",
        "urgency": "low",
    },
    {
        "name": "前胃拡張症",
        "name_en": "Proventricular Dilatation Disease",
        "symptoms": ["regurgitation", "weight_loss", "neurological_signs", "lethargy"],
        "description": "神経系に影響し消化不良や体重減少を招くウイルス性疾患。",
        "severity": "severe",
        "recommended_tests": ["クロア検査", "レントゲン検査"],
        "name_ja": "前胃拡張症",
        "description_ja": "神経系に影響し消化不良や体重減少を招くウイルス性疾患。",
        "urgency": "high",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
