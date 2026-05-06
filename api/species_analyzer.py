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

import importlib
import inspect
from functools import lru_cache
from typing import Any, Callable, Dict, List

# Lazy imports: species modules are loaded on first use to reduce startup memory
# from 528MB peak to ~50MB. Each module is 1-2MB of disease data.
from api.data.vaccine_mapping import get_preventable_diseases
from api.species.helpers import _find_enrichment, _fuzzy_boost_lookup, compute_lab_boosts
from api.species.prevalence_data import get_prevalence_for_species

# Lazy species import registry — module path → function name
_SPECIES_MODULE_MAP = {
    "amphibian": ("api.species.amphibian_diseases", "analyze_symptoms"),
    "bird": ("api.species.bird_diseases", "analyze_symptoms"),
    "cat": ("api.species.cat_diseases", "analyze_symptoms"),
    "chinchilla": ("api.species.chinchilla_diseases", "analyze_symptoms"),
    "degu": ("api.species.degu_diseases", "analyze_symptoms"),
    "exotic_other": ("api.species.exotic_other_diseases", "analyze_symptoms"),
    "ferret": ("api.species.ferret_diseases", "analyze_symptoms"),
    "fish": ("api.species.fish_diseases", "analyze_symptoms"),
    "guinea_pig": ("api.species.guinea_pig_diseases", "analyze_symptoms"),
    "hamster": ("api.species.hamster_diseases", "analyze_symptoms"),
    "hedgehog": ("api.species.hedgehog_diseases", "analyze_symptoms"),
    "lizard": ("api.species.lizard_diseases", "analyze_symptoms"),
    "parakeet": ("api.species.parakeet_diseases", "analyze_symptoms"),
    "parrot": ("api.species.parrot_diseases", "analyze_symptoms"),
    "rabbit": ("api.species.rabbit_diseases", "analyze_symptoms"),
    "reptile": ("api.species.reptile_diseases", "analyze_symptoms"),
    "snake": ("api.species.snake_diseases", "analyze_symptoms"),
    "sugar_glider": ("api.species.sugar_glider_diseases", "analyze_symptoms"),
    "tortoise": ("api.species.tortoise_diseases", "analyze_symptoms"),
}
_SPECIES_FUNC_CACHE: Dict[str, Any] = {}


def _lazy_load(species_key: str):
    """Lazily import and cache species analyze function."""
    if species_key in _SPECIES_FUNC_CACHE:
        return _SPECIES_FUNC_CACHE[species_key]
    entry = _SPECIES_MODULE_MAP.get(species_key)
    if not entry:
        return None
    mod = importlib.import_module(entry[0])
    func = getattr(mod, entry[1])
    _SPECIES_FUNC_CACHE[species_key] = func
    return func


def _lazy_dog():
    if "dog" not in _SPECIES_FUNC_CACHE:
        from api.symptom_checker import analyze_symptoms as analyze_dog
        _SPECIES_FUNC_CACHE["dog"] = analyze_dog
    return _SPECIES_FUNC_CACHE["dog"]


def _lazy_horse():
    if "horse" not in _SPECIES_FUNC_CACHE:
        _SPECIES_FUNC_CACHE["horse"] = analyze_horse
    return _SPECIES_FUNC_CACHE["horse"]

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


@lru_cache(maxsize=1)
def _horse_symptom_id_to_name() -> Dict[str, Dict[str, str]]:
    """Build the {symptom_id: {ja, en}} lookup for horse HEALTH_CHECK_ITEMS once.

    Used to translate raw IDs like 'resp_cough' into display names. Equine items
    are static at module load, so a 1-slot lru_cache is sufficient.
    """
    try:
        from api.species.equine_diseases import HEALTH_CHECK_ITEMS
    except ImportError:
        return {}
    out: Dict[str, Dict[str, str]] = {}
    for _cat, items in HEALTH_CHECK_ITEMS.items():
        for sid, ja_name, en_name in items:
            out[sid] = {"ja": ja_name, "en": en_name}
    return out


def _horse_category(name: str, desc: str) -> str:
    """Simple category classifier for horse diseases."""
    combined = (name + " " + desc).lower()
    for cat in ("viral", "bacterial", "fungal", "parasitic"):
        keywords = {
            "viral": ["virus", "viral", "herpes", "influenza", "ehv", "eav", "wnv", "rabies"],
            "bacterial": [
                "bacterial",
                "streptococc",
                "staphylococc",
                "clostrid",
                "salmonell",
                "rhodococc",
                "strangles",
                "abscess",
                "septic",
                "cellulitis",
            ],
            "fungal": ["fungal", "mycosis", "aspergill", "ringworm", "dermatophyt"],
            "parasitic": ["parasit", "strongyl", "ascarid", "tapeworm", "bot", "mange", "mite", "tick", "lice"],
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
    from api.species.equine_diseases import generate_differential_diagnosis

    checked = set(symptoms)
    diff_list = generate_differential_diagnosis(checked, age_stage or "")

    # Vaccine-preventable disease exclusion
    vaccine_preventable: set = set()
    vaccine_list = [str(v) for v in (vaccines or []) if v]
    if vaccine_list:
        vaccine_preventable = get_preventable_diseases(vaccine_list)

    # Lab boosts for horse
    lab_boosts: Dict[str, float] = {}
    if lab_values:
        lab_boosts = compute_lab_boosts(lab_values, species="horse")

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
            (
                f"Diagnosis is based on clinical signs, history, and physical examination. "
                f"Recommended diagnostics: {', '.join(tests[:4])}."
            )
            if tests
            else "Diagnosis is based on clinical signs, history, and physical examination."
        )
        _diag_ja = (
            (f"臨床徴候、病歴、身体検査に基づき診断する。推奨検査: {', '.join(tests[:4])}。")
            if tests
            else "臨床徴候、病歴、身体検査に基づき診断する。"
        )

        # Apply lab boost if available
        lab_multiplier = 1.0
        if lab_boosts:
            lab_multiplier = min(_fuzzy_boost_lookup(name, lab_boosts), 1.5)
            if lab_multiplier == 1.0:
                lab_multiplier = min(_fuzzy_boost_lookup(name_en, lab_boosts), 1.5)

        # Onset multiplier for horse
        onset_multiplier = 1.0
        if onset:
            disease_onsets = getattr(dis, "onset_pattern", None)
            if disease_onsets:
                onset_multiplier = 1.15 if onset in disease_onsets else 0.85

        # Age multiplier for horse
        age_multiplier = 1.0
        if age_years is not None:
            horse_age_stage = (
                "puppy"
                if age_years < 1.0
                else "young"
                if age_years < 4.0
                else "adult"
                if age_years < 15.0
                else "senior"
            )
            age_pred = getattr(dis, "age_predisposition", None)
            if age_pred:
                age_multiplier = 1.15 if horse_age_stage in age_pred else 0.85

        # Gender multiplier for horse
        gender_multiplier = 1.0
        # Breed multiplier for horse (placeholder for future breed risk data)
        breed_multiplier = 1.0

        combined_horse_boost = onset_multiplier * age_multiplier * breed_multiplier * gender_multiplier * lab_multiplier
        combined_horse_boost = max(0.6, min(combined_horse_boost, 3.0))

        match_pct = round(item.confidence_pct * combined_horse_boost)
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
                    "breed_multiplier": round(breed_multiplier, 3),
                    "gender_multiplier": round(gender_multiplier, 3),
                    "age_multiplier": round(age_multiplier, 3),
                    "onset_multiplier": round(onset_multiplier, 3),
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
        "pathophysiology_ja",
        "causes_ja",
        "treatment_ja",
        "prevention_ja",
        "prognosis_ja",
        "clinical_signs_ja",
        "transmission",
        "transmission_ja",
        "diagnosis",
        "diagnosis_ja",
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

    # Build symptom_names lookup for frontend display (translates raw IDs
    # like "resp_cough" to {"ja": "咳が出る", "en": "Cough"} in the UI).
    used_symptoms: set[str] = set(symptoms)
    for cond in possible_conditions:
        used_symptoms.update(cond.get("matching_symptoms", []) or [])
        used_symptoms.update(cond.get("missing_key_symptoms", []) or [])
    id_to_name = _horse_symptom_id_to_name()
    symptom_names_lookup: Dict[str, Dict[str, str]] = {
        sid: id_to_name[sid] for sid in used_symptoms if sid in id_to_name
    }

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
        "symptom_names": symptom_names_lookup,
    }


# Lazy species handler resolver — loads modules on first access
_SPECIES_KEYS = [
    "dog", "cat", "rabbit", "hamster", "chinchilla", "guinea_pig",
    "ferret", "hedgehog", "sugar_glider", "degu", "bird", "parakeet",
    "parrot", "reptile", "tortoise", "snake", "lizard", "amphibian",
    "fish", "exotic_other", "horse",
]


def _resolve_handler(species_key: str):
    """Resolve species handler lazily."""
    if species_key == "dog":
        return None  # handled specially
    if species_key == "horse":
        return _lazy_horse()
    return _lazy_load(species_key)


# SPECIES_HANDLERS is kept as a dict for backward compatibility checks
# but handlers are resolved lazily via _resolve_handler()
SPECIES_HANDLERS: Dict[str, Any] = {k: None for k in _SPECIES_KEYS}


@lru_cache(maxsize=None)
def _handler_kwargs(handler: Callable) -> frozenset[str]:
    """Return parameter names accepted by a handler (excluding positionals).

    Cached per-handler so we introspect signatures once, then filter optional
    kwargs deterministically instead of catching TypeError repeatedly.
    Returns an "all-accepting" sentinel via a special marker if the handler
    declares **kwargs.
    """
    try:
        sig = inspect.signature(handler)
    except (TypeError, ValueError):
        return frozenset()
    names: set[str] = set()
    for p in sig.parameters.values():
        if p.kind == inspect.Parameter.VAR_KEYWORD:
            return frozenset({"*"})  # accepts everything
        if p.kind in (inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
            names.add(p.name)
    return frozenset(names)


def _filter_kwargs(handler: Callable, candidates: Dict[str, Any]) -> Dict[str, Any]:
    accepted = _handler_kwargs(handler)
    if "*" in accepted:
        return candidates
    return {k: v for k, v in candidates.items() if k in accepted}


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
    pain_score: int | None = None,
    lang: str = "",
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
    # Load region-aware prevalence map (forwarded to handlers that accept it).
    _region = "jp" if lang == "ja" else ("intl" if lang else "")
    _prevalence_map = get_prevalence_for_species(species_key, region=_region)
    # 犬: 全パラメータを直接渡す（シグネチャが固定）
    if species_key == "dog":
        return _lazy_dog()(
            symptoms,
            breed=breed,
            onset=onset,
            age_years=age_years,
            lab_values=lab_values,
            gender=gender,
            vaccines=vaccines,
            vaccination_status=vaccination_status,
        )
    handler = _resolve_handler(species_key)
    if handler is None:
        raise ValueError(f"No handler for species: {species_key}")
    candidate_kwargs: Dict[str, Any] = {
        "breed": breed,
        "onset": onset,
        "age_years": age_years,
        "species": species_key,
        "lab_values": lab_values,
        "gender": gender,
        "vaccines": vaccines,
        "vaccination_status": vaccination_status,
        "prevalence_map": _prevalence_map,
    }
    return handler(symptoms, age_stage, **_filter_kwargs(handler, candidate_kwargs))
