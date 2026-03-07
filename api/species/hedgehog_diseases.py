"""hedgehog_diseases.py – ハリネズミの一般的な疾患と鑑別診断

このモジュールではハリネズミに多く見られる代表的な疾患を少数サンプルとして示し、
与えられた症状から鑑別診断を行う簡易エンジンを提供します。実際の診断は獣医師の
判断を必要とし、本データは教育目的の参考情報です。

各疾患は症状リストと推奨検査を持ち、`analyze_symptoms` 関数を通じて症状リスト
から一致度に基づいた候補リストを返します。詳細な評価ロジックは `helpers.py` に
定義された `analyze_symptoms_generic` を使用しています。
"""

from __future__ import annotations

from typing import Dict, List

from .helpers import analyze_symptoms_generic, ADVICE


# シンボリック症状名の定義
SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    "anorexia": {"ja": "食欲不振", "en": "Anorexia"},
    "diarrhea": {"ja": "下痢", "en": "Diarrhea"},
    "weight_loss": {"ja": "体重減少", "en": "Weight loss"},
    "drooling": {"ja": "流涎", "en": "Drooling"},
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "weakness": {"ja": "衰弱", "en": "Weakness"},
}

# 疾患データベース
DISEASES: List[Dict] = [
    {
        "name": "サルモネラ症",
        "name_en": "Salmonellosis",
        "symptoms": ["anorexia", "diarrhea", "lethargy"],
        "description": "細菌感染による消化器症状と全身状態の悪化を引き起こす感染症。",
        "severity": "moderate",
        "recommended_tests": ["糞便培養", "血液検査"],
        # 共通フォーマットに合わせた追加情報
        "name_ja": "サルモネラ症",
        "description_ja": "細菌感染による消化器症状と全身状態の悪化を引き起こす感染症。",
        "urgency": "medium",
    },
    {
        "name": "口内炎",
        "name_en": "Stomatitis",
        "symptoms": ["drooling", "anorexia", "weight_loss"],
        "description": "口腔内の炎症により摂食不良や体重減少を招く疾患。",
        "severity": "mild",
        "recommended_tests": ["口腔内検査", "血液検査"],
        "name_ja": "口内炎",
        "description_ja": "口腔内の炎症により摂食不良や体重減少を招く疾患。",
        "urgency": "low",
    },
]


def analyze_symptoms(symptoms: List[str], age_stage: str | None = None) -> Dict:
    """ハリネズミ用の鑑別診断エンジン。

    与えられた症状リストに基づいて `helpers.analyze_symptoms_generic` を呼び出し、
    候補疾患と推奨検査を返します。

    Args:
        symptoms: ユーザーが報告した症状のリスト
        age_stage: 任意の年齢層情報（未使用だがインターフェース整合性のため）

    Returns:
        辞書形式の分析結果
    """
    return analyze_symptoms_generic(symptoms, DISEASES, SYMPTOM_NAMES, ADVICE)
