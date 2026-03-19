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

from api.species.amphibian_diseases import analyze_symptoms as analyze_amphibian
from api.species.bird_diseases import analyze_symptoms as analyze_bird

# 個別の動物種モジュールをインポート
from api.species.cat_diseases import analyze_symptoms as analyze_cat
from api.species.chinchilla_diseases import analyze_symptoms as analyze_chinchilla
from api.species.degu_diseases import analyze_symptoms as analyze_degu

# Equine (horse) は独自の大規模データベースと診断エンジンを持つ
from api.species.equine_diseases import generate_differential_diagnosis
from api.species.exotic_other_diseases import analyze_symptoms as analyze_exotic_other
from api.species.ferret_diseases import analyze_symptoms as analyze_ferret
from api.species.guinea_pig_diseases import analyze_symptoms as analyze_guinea_pig
from api.species.hamster_diseases import analyze_symptoms as analyze_hamster
from api.species.hedgehog_diseases import analyze_symptoms as analyze_hedgehog
from api.species.helpers import _find_enrichment
from api.species.lizard_diseases import analyze_symptoms as analyze_lizard
from api.species.parakeet_diseases import analyze_symptoms as analyze_parakeet
from api.species.parrot_diseases import analyze_symptoms as analyze_parrot
from api.species.rabbit_diseases import analyze_symptoms as analyze_rabbit
from api.species.reptile_diseases import analyze_symptoms as analyze_reptile
from api.species.snake_diseases import analyze_symptoms as analyze_snake
from api.species.sugar_glider_diseases import analyze_symptoms as analyze_sugar_glider
from api.species.tortoise_diseases import analyze_symptoms as analyze_tortoise
from api.symptom_checker import analyze_symptoms as analyze_dog

# ── Horse category-based content templates ──
_HORSE_TRANSMISSION: dict[str, tuple[str, str]] = {
    "viral": (
        "Transmitted through direct contact, aerosol droplets, fomites, or insect vectors.",
        "直接接触、飛沫、汚染物、昆虫媒介により伝播する。",
    ),
    "bacterial": (
        "Transmitted through direct contact, wound contamination, ingestion, or aerosol.",
        "直接接触、創傷汚染、経口摂取、飛沫により伝播する。",
    ),
    "fungal": (
        "Transmitted through environmental spore exposure or contact with infected animals.",
        "環境中の胞子曝露または感染動物との接触により伝播する。",
    ),
    "parasitic": (
        "Transmitted through ingestion of larvae/eggs, vector-mediated, or percutaneous penetration.",
        "幼虫・虫卵の経口摂取、媒介動物、経皮侵入により伝播する。",
    ),
}
_HORSE_TRANS_DEFAULT = (
    "Not directly transmissible between horses in most cases.",
    "ほとんどの場合、馬間で直接伝播しない。",
)


def _horse_category(name: str, desc: str) -> str:
    """Simple category classifier for horse diseases."""
    combined = (name + " " + desc).lower()
    for cat in ("viral", "bacterial", "fungal", "parasitic"):
        keywords = {
            "viral": ["virus", "viral", "herpes", "influenza", "ehv", "eav", "wnv", "rabies"],
            "bacterial": ["bacterial", "streptococc", "staphylococc", "clostrid", "salmonell",
                          "rhodococc", "strangles", "abscess", "septic", "cellulitis"],
            "fungal": ["fungal", "mycosis", "aspergill", "ringworm", "dermatophyt"],
            "parasitic": ["parasit", "strongyl", "ascarid", "tapeworm", "bot", "mange",
                          "mite", "tick", "lice"],
        }
        for kw in keywords[cat]:
            if kw in combined:
                return cat
    return "general"


def analyze_horse(
    symptoms: List[str],
    age_stage: str | None = None,
    *,
    breed: str | None = None,
    onset: str | None = None,
    age_years: float | None = None,
    species: str | None = None,
    lab_values: dict | None = None,
    gender: str | None = None,
    vaccines: list | None = None,
    vaccination_status: str | None = None,
) -> Dict:
    """馬用の症状解析。馬の鑑別診断エンジンに委譲する。

    馬用データベースでは症状を "所見キー" として扱うため、入力された
    症状文字列がそのまま所見キーとして渡されることを想定しています。

    Args:
        symptoms: 所見キーのリスト
        age_stage: "young" / "adult" / "senior" など（馬用エンジンに渡される）
        breed: 品種コード（任意）
        onset: 発症経過（任意）
        age_years: 年齢（任意）
        species: 動物種コード（任意）
        lab_values: 検査値（任意）
        gender: 性別（任意）
        vaccines: ワクチンIDリスト（任意）
        vaccination_status: ワクチン接種状況（任意）

    Returns:
        dict: 鑑別診断結果を共通形式に整形した辞書
    """
    checked = set(symptoms)
    diff_list = generate_differential_diagnosis(checked, age_stage or "")

    # Vaccine-preventable disease exclusion
    vaccine_preventable: set = set()
    vaccine_list = [str(v) for v in (vaccines or []) if v]
    if vaccine_list:
        try:
            from api.data.vaccine_mapping import get_preventable_diseases
            vaccine_preventable = get_preventable_diseases(vaccine_list)
        except ImportError:
            pass

    # Lab boosts for horse
    lab_boosts: Dict[str, float] = {}
    if lab_values:
        try:
            from api.species.helpers import compute_lab_boosts
            lab_boosts = compute_lab_boosts(lab_values, species="horse")
        except ImportError:
            pass

    possible_conditions = []
    recommended_tests: List[str] = []

    for item in diff_list:
        dis = item.disease
        name = dis.name_ja or dis.name_en or dis.id
        name_en = dis.name_en or ""

        # Skip vaccine-preventable diseases
        if name in vaccine_preventable or name_en in vaccine_preventable:
            continue

        severity = dis.severity.lower() if dis.severity else "unknown"
        severity_map = {
            "critical": "critical",
            "severe": "high",
            "moderate": "moderate",
            "mild": "low",
        }
        severity_level = severity_map.get(severity, "unknown")
        tests = [t[1] for t in (dis.recommended_exams or [])]
        recommended_tests.extend(tests)
        _cat = _horse_category(dis.name_en or "", dis.description_ja or "")
        _trans = _HORSE_TRANSMISSION.get(_cat, _HORSE_TRANS_DEFAULT)
        _diag_en = (
            f"Diagnosis is based on clinical signs, history, and physical examination. "
            f"Recommended diagnostics: {', '.join(tests[:4])}."
        ) if tests else "Diagnosis is based on clinical signs, history, and physical examination."
        _diag_ja = (
            f"臨床徴候、病歴、身体検査に基づき診断する。推奨検査: {', '.join(tests[:4])}。"
        ) if tests else "臨床徴候、病歴、身体検査に基づき診断する。"

        # Apply lab boost if available
        lab_multiplier = 1.0
        if lab_boosts:
            from api.species.helpers import _fuzzy_boost_lookup
            lab_multiplier = min(_fuzzy_boost_lookup(name, lab_boosts), 1.5)
            if lab_multiplier == 1.0:
                lab_multiplier = min(_fuzzy_boost_lookup(name_en, lab_boosts), 1.5)

        match_pct = round(item.confidence_pct * lab_multiplier)
        match_pct = min(match_pct, 100)

        # Determine likelihood tier
        if match_pct >= 50:
            likelihood = "high"
        elif match_pct >= 30:
            likelihood = "moderate"
        else:
            likelihood = "low"
        # Color class
        if match_pct >= 70:
            color_class = "score-high"
        elif match_pct >= 45:
            color_class = "score-moderate"
        elif match_pct >= 25:
            color_class = "score-low"
        else:
            color_class = "score-minimal"

        possible_conditions.append(
            {
                "name": name,
                "name_ja": dis.name_ja or "",
                "match_count": item.match_count,
                "confidence": round(item.confidence_pct, 2),
                "match_percent": match_pct,
                "likelihood": likelihood,
                "color_class": color_class,
                "severity": severity_level,
                "description": dis.description_ja or dis.name_ja,
                "description_ja": dis.description_ja or "",
                "pathophysiology": dis.pathophysiology or "",
                "causes": dis.etiology or "",
                "treatment": dis.treatment_protocol or dis.general_management or "",
                "prevention": dis.prevention or "",
                "prognosis": dis.prognosis or "",
                "clinical_signs": dis.clinical_signs_detail or "",
                "risk_factors": dis.risk_factors or "",
                "recommended_tests": tests,
                "matching_symptoms": sorted(item.matched_findings),
                "total_symptoms": len(dis.associated_findings) if dis.associated_findings else 0,
                "_name_en": dis.name_en or "",
                "transmission": _trans[0],
                "transmission_ja": _trans[1],
                "urgency": dis.urgency or "moderate",
                "pathophysiology_ja": "",
                "causes_ja": "",
                "treatment_ja": "",
                "prevention_ja": "",
                "prognosis_ja": "",
                "clinical_signs_ja": "",
                "diagnosis": _diag_en,
                "diagnosis_ja": _diag_ja,
                # Scoring transparency
                "scoring_detail": {
                    "weighted_recall": round(item.match_ratio, 3),
                    "coverage": round(item.match_ratio, 3),
                    "weighted_score": round(item.weighted_score, 3),
                    "cluster_boost": 1.0,
                    "negative_penalty": round(1.0 - item.absence_penalty, 3),
                    "specificity_bonus": 0.0,
                    "prevalence_prior": 1.0,
                    "breed_multiplier": 1.0,
                    "gender_multiplier": 1.0,
                    "age_multiplier": 1.0,
                    "onset_multiplier": 1.0,
                    "lab_multiplier": round(lab_multiplier, 3),
                    "confidence_level": item.confidence_level,
                    "absence_penalty": round(item.absence_penalty, 3),
                    "rule_out_note": item.rule_out_note,
                },
                # Key findings that are missing (for follow-up questions)
                "missing_key_symptoms": sorted(item.absent_key_findings),
            }
        )

    # JSON エンリッチメントから日本語フィールドを補完
    _ja_enrich_fields = (
        "pathophysiology_ja", "causes_ja", "treatment_ja",
        "prevention_ja", "prognosis_ja", "clinical_signs_ja",
        "transmission", "transmission_ja", "diagnosis", "diagnosis_ja",
    )
    for cond in possible_conditions:
        # 英語名で検索（最も確実）→ 日本語名フォールバック
        enrichment = _find_enrichment("Horse", cond.get("_name_en", ""))
        if not enrichment:
            enrichment = _find_enrichment("Horse", cond.get("name_ja", ""))
        if enrichment:
            for field in _ja_enrich_fields:
                if not cond.get(field) and enrichment.get(field):
                    cond[field] = enrichment[field]
        # 内部キーを除去
        cond.pop("_name_en", None)

    # 重複する検査を除外
    dedup_tests = []
    for t in recommended_tests:
        if t not in dedup_tests:
            dedup_tests.append(t)
    # Compute overall severity
    severity = "low"
    for c in possible_conditions:
        u = c.get("urgency", "low")
        if u == "emergency" and c.get("likelihood") == "high":
            severity = "emergency"
            break
        if u == "high" and c.get("match_percent", 0) >= 30:
            severity = "high"
        elif u == "moderate" and c.get("match_percent", 0) >= 50 and severity == "low":
            severity = "moderate"

    return {
        "possible_conditions": possible_conditions,
        "suspected_diseases": possible_conditions,
        "recommended_tests": dedup_tests,
        "severity": severity,
        "breed_risk_applied": False,
        "gender_risk_applied": False,
        "onset_applied": onset is not None,
        "onset": onset,
        "age_applied": age_years is not None,
        "age_years": age_years,
        "age_stage": age_stage,
        "pair_boost_applied": False,
        "lab_boost_applied": len(lab_boosts) > 0,
        "lab_values": lab_values,
        "vaccination_adjustment_applied": len(vaccine_preventable) > 0,
        "vaccine_preventable_excluded": len(vaccine_preventable) > 0,
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
    vaccines: list[str] | None = None,
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
        vaccines: ワクチンIDのリスト（任意）
        vaccination_status: ワクチン接種状況 "current" | "outdated" | "none"（任意）

    Returns:
        辞書形式の分析結果

    Raises:
        ValueError: 未対応の種が指定された場合
    """
    species_key = (species or "dog").lower()
    if species_key not in SPECIES_HANDLERS:
        raise ValueError(f"Unsupported species: {species}")
    # 犬: 全パラメータを渡す
    if species_key == "dog":
        return analyze_dog(
            symptoms,
            breed=breed,
            onset=onset,
            age_years=age_years,
            lab_values=lab_values,
            gender=gender,
            vaccines=vaccines,
            vaccination_status=vaccination_status,
        )
    elif species_key == "horse":
        handler = SPECIES_HANDLERS[species_key]
        return handler(
            symptoms, age_stage,
            breed=breed, onset=onset, age_years=age_years,
            species=species_key,
            lab_values=lab_values,
            gender=gender,
            vaccines=vaccines,
            vaccination_status=vaccination_status,
        )
    else:
        handler = SPECIES_HANDLERS[species_key]
        # Try passing all params including vaccination; fall back gracefully
        # if the species handler hasn't been updated to accept them yet.
        try:
            return handler(
                symptoms, age_stage,
                breed=breed, onset=onset, age_years=age_years,
                species=species_key,
                lab_values=lab_values,
                gender=gender,
                vaccines=vaccines,
                vaccination_status=vaccination_status,
            )
        except TypeError:
            return handler(
                symptoms, age_stage,
                breed=breed, onset=onset, age_years=age_years,
                species=species_key,
                lab_values=lab_values,
                gender=gender,
            )
