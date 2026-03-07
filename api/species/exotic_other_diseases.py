"""exotic_other_diseases.py – その他エキゾチック動物の一般的な疾患

フェレットやハリネズミなど特定分類に含まれないエキゾチックアニマルを想定した
簡易的な疾患データベースです。症状から鑑別診断候補を提示する際に使用します。
この情報は教育目的であり、診断は獣医師にご相談ください。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "obesity": {"ja": "肥満", "en": "Obesity"},
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "dermatitis": {"ja": "皮膚炎", "en": "Dermatitis"},
    "hair_loss": {"ja": "脱毛", "en": "Hair loss"},
    "pruritus": {"ja": "掻痒", "en": "Pruritus"},
}

DISEASES: List[Dict] = [
    {
        "name": "肥満症",
        "name_en": "Obesity",
        "symptoms": ["obesity", "lethargy"],
        "description": "カロリー摂取過多や運動不足により体重が過剰になる状態。",
        "severity": "mild",
        "recommended_tests": ["体重測定", "栄養評価"],
        "name_ja": "肥満症",
        "description_ja": "カロリー摂取過多や運動不足により体重が過剰になる状態。",
        "urgency": "low",
    },
    {
        "name": "皮膚炎",
        "name_en": "Dermatitis",
        "symptoms": ["dermatitis", "hair_loss", "pruritus"],
        "description": "アレルギーや寄生虫などさまざまな原因による皮膚の炎症。",
        "severity": "moderate",
        "recommended_tests": ["皮膚検査", "寄生虫検査"],
        "name_ja": "皮膚炎",
        "description_ja": "アレルギーや寄生虫などさまざまな原因による皮膚の炎症。",
        "urgency": "medium",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
