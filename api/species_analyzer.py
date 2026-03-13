"""species_analyzer.py – マルチ動物種の症状解析ルーティング

本モジュールは、`/api/analyze-symptoms` エンドポイントなどから呼び出され、
指定された動物種に応じて適切な鑑別診断エンジンを選択します。デフォルト
では犬用の症状チェッカーを使用し、サポートされている他の動物種については
`api/species` 配下の各モジュールに定義された `analyze_symptoms` 関数を
呼び出します。

対応する動物種コードは小文字で受け付けます。未知の種が指定された場合は
`ValueError` を送出します。今後新しい種を追加する際は、`SPECIES_HANDLERS`
辞書にエントリを追記してください。
"""

from __future__ import annotations

from typing import Callable, Dict, List

from api.symptom_checker import analyze_symptoms as analyze_dog

# 個別の動物種モジュールをインポート
from api.species.cat_diseases import analyze_symptoms as analyze_cat
from api.species.rabbit_diseases import analyze_symptoms as analyze_rabbit
from api.species.hamster_diseases import analyze_symptoms as analyze_hamster
from api.species.chinchilla_diseases import analyze_symptoms as analyze_chinchilla
from api.species.guinea_pig_diseases import analyze_symptoms as analyze_guinea_pig
from api.species.ferret_diseases import analyze_symptoms as analyze_ferret
from api.species.hedgehog_diseases import analyze_symptoms as analyze_hedgehog
from api.species.sugar_glider_diseases import analyze_symptoms as analyze_sugar_glider
from api.species.degu_diseases import analyze_symptoms as analyze_degu
from api.species.bird_diseases import analyze_symptoms as analyze_bird
from api.species.parakeet_diseases import analyze_symptoms as analyze_parakeet
from api.species.parrot_diseases import analyze_symptoms as analyze_parrot
from api.species.reptile_diseases import analyze_symptoms as analyze_reptile
from api.species.tortoise_diseases import analyze_symptoms as analyze_tortoise
from api.species.snake_diseases import analyze_symptoms as analyze_snake
from api.species.lizard_diseases import analyze_symptoms as analyze_lizard
from api.species.amphibian_diseases import analyze_symptoms as analyze_amphibian
from api.species.exotic_other_diseases import analyze_symptoms as analyze_exotic_other

# Equine (horse) は独自の大規模データベースと診断エンジンを持つ
from api.species.equine_diseases import generate_differential_diagnosis
from api.species.equine_diseases import DISEASE_DATABASE as EQUINE_DB


def analyze_horse(symptoms: List[str], age_stage: str | None = None) -> Dict:
    """馬用の症状解析。馬の鑑別診断エンジンに委譲する。

    馬用データベースでは症状を "所見キー" として扱うため、入力された
    症状文字列がそのまま所見キーとして渡されることを想定しています。

    Args:
        symptoms: 所見キーのリスト
        age_stage: "young" / "adult" / "senior" など（馬用エンジンに渡される）

    Returns:
        dict: 鑑別診断結果を共通形式に整形した辞書
    """
    checked = set(symptoms)
    diff_list = generate_differential_diagnosis(checked, age_stage or "")
    possible_conditions = []
    recommended_tests: List[str] = []

    for item in diff_list:
        dis = item.disease
        # 日本語名があればそれを使用
        name = dis.name_ja or dis.name_en or dis.id
        # 重症度を英語から日本語レベルへ簡易変換
        severity = dis.severity.lower() if dis.severity else "unknown"
        severity_map = {
            "critical": "critical",
            "severe": "high",
            "moderate": "moderate",
            "mild": "low",
        }
        severity_level = severity_map.get(severity, "unknown")
        # 推奨検査の日本語名のみ抽出（優先度順）
        tests = [t[1] for t in (dis.recommended_exams or [])]
        recommended_tests.extend(tests)
        possible_conditions.append(
            {
                "name": name,
                "match_count": item.match_count,
                "confidence": round(item.confidence_pct, 2),
                "severity": severity_level,
                "description": dis.description_ja or dis.name_ja,
                "recommended_tests": tests,
            }
        )
    # 重複する検査を除外
    dedup_tests = []
    for t in recommended_tests:
        if t not in dedup_tests:
            dedup_tests.append(t)
    return {
        "possible_conditions": possible_conditions,
        "recommended_tests": dedup_tests,
    }


# それぞれの動物種コードに対応する解析関数
# 注: 犬は analyze_species_symptoms 内で直接呼び出すため lambda 不要
SPECIES_HANDLERS: Dict[str, Callable[[List[str], str | None], Dict]] = {
    "dog": None,  # handled specially in analyze_species_symptoms
    "cat": analyze_cat,
    "rabbit": analyze_rabbit,
    "hamster": analyze_hamster,
    "chinchilla": analyze_chinchilla,
    "guinea_pig": analyze_guinea_pig,
    "ferret": analyze_ferret,
    "hedgehog": analyze_hedgehog,
    "sugar_glider": analyze_sugar_glider,
    "degu": analyze_degu,
    "bird": analyze_bird,
    "parakeet": analyze_parakeet,
    "parrot": analyze_parrot,
    "reptile": analyze_reptile,
    "tortoise": analyze_tortoise,
    "snake": analyze_snake,
    "lizard": analyze_lizard,
    "amphibian": analyze_amphibian,
    "exotic_other": analyze_exotic_other,
    "horse": analyze_horse,
}


def analyze_species_symptoms(
    species: str,
    symptoms: List[str],
    age_stage: str | None = None,
    *,
    breed: str | None = None,
    onset: str | None = None,
    age_years: float | None = None,
    lab_values: dict | None = None,
    gender: str | None = None,
    vaccination_status: str | None = None,
) -> Dict:
    """動物種に応じて適切な鑑別診断関数を呼び出すユーティリティ。

    Args:
        species: 動物種コード（小文字）
        symptoms: 症状コードのリスト
        age_stage: 任意の年齢カテゴリ（馬用などで使用）
        breed: 品種コード（任意）
        onset: 発症経過 "acute"/"subacute"/"chronic"（任意）
        age_years: 年齢（年単位の数値、任意）
        lab_values: 検査値 {項目ID: 数値} の辞書（任意）
        gender: 性別 "male" | "female"（任意）
        vaccination_status: ワクチン接種状況 "current" | "outdated" | "none"（任意）

    Returns:
        辞書形式の分析結果

    Raises:
        ValueError: 未対応の種が指定された場合
    """
    species_key = (species or "dog").lower()
    if species_key not in SPECIES_HANDLERS:
        raise ValueError(f"Unsupported species: {species}")
    # 犬: 全パラメータ（breed, onset, age_years, lab_values, gender, vaccination_status）を渡す
    if species_key == "dog":
        return analyze_dog(
            symptoms,
            breed=breed,
            onset=onset,
            age_years=age_years,
            lab_values=lab_values,
            gender=gender,
            vaccination_status=vaccination_status,
        )
    elif species_key == "horse":
        handler = SPECIES_HANDLERS[species_key]
        return handler(symptoms, age_stage)
    else:
        handler = SPECIES_HANDLERS[species_key]
        return handler(
            symptoms, age_stage,
            breed=breed, onset=onset, age_years=age_years,
            species=species_key,
            lab_values=lab_values,
            gender=gender,
            vaccination_status=vaccination_status,
        )
