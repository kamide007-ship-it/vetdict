"""amphibian_diseases.py – 両生類の代表的な疾患

カエルやイモリなどの両生類に発生する代表的な疾患を取り上げ、
簡易的な鑑別診断を提供するモジュールです。情報は教育目的であり、
専門的な診断や治療は獣医師が行うべきです。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "skin_shedding": {"ja": "皮膚の脱落", "en": "Skin shedding"},
    "ulcers": {"ja": "潰瘍", "en": "Ulcers"},
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "anorexia": {"ja": "食欲不振", "en": "Anorexia"},
    "hemorrhage": {"ja": "出血", "en": "Hemorrhage"},
    "red_legs": {"ja": "四肢の発赤", "en": "Red legs"},
}

DISEASES: List[Dict] = [
    {
        "name": "カエルツボカビ症",
        "name_en": "Chytridiomycosis",
        "symptoms": ["skin_shedding", "ulcers", "lethargy", "anorexia"],
        "description": "ツボカビ菌感染により皮膚が障害され致死的となることもある。",
        "severity": "severe",
        "recommended_tests": ["PCR検査", "皮膚スクレイピング"],
        "name_ja": "カエルツボカビ症",
        "description_ja": "ツボカビ菌感染により皮膚が障害され致死的となることもある。",
        "urgency": "high",
    },
    {
        "name": "レッドレッグ病",
        "name_en": "Red-leg Disease",
        "symptoms": ["hemorrhage", "red_legs", "lethargy", "anorexia"],
        "description": "細菌感染や環境不良が原因で四肢が赤くなり出血を伴う疾患。",
        "severity": "moderate",
        "recommended_tests": ["皮膚検査", "細菌培養"],
        "name_ja": "レッドレッグ病",
        "description_ja": "細菌感染や環境不良が原因で四肢が赤くなり出血を伴う疾患。",
        "urgency": "medium",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
