"""dose_calculator.py - 体重ベース用量計算機

薬品データの用量文字列（例: "20-35 mg/kg IV q6-8h"）を解析し、
動物の体重から具体的な投与量を計算する。

設計原則:
- 単位変換（mg/kg, μg/kg, g/kg, mg, IU/kg）対応
- 範囲（low-high）対応
- 投与経路・間隔の抽出
- 製剤濃度（mg/mL）が指定されていれば容量(mL)も計算
- 安全閾値（最大用量・体重外れ値）の警告
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# 単位変換テーブル (基準: mg)
# ---------------------------------------------------------------------------
_UNIT_TO_MG = {
    "mg": 1.0,
    "g": 1000.0,
    "μg": 0.001,
    "ug": 0.001,
    "mcg": 0.001,
    "ng": 0.000001,
    "iu": None,  # IU は薬剤特異的でmg換算不可
    "u": None,
}

# 解析対象パターン
# 例: "20-35 mg/kg", "0.1 mg/kg", "5-10 μg/kg", "100 IU/kg"
_DOSE_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:[-~–]\s*(\d+(?:\.\d+)?))?\s*(mg|g|μg|ug|mcg|ng|IU|U)\s*/\s*kg",
    re.IGNORECASE,
)
# 例: "100 mg/cat", "50 mg/animal" (絶対量)
_FIXED_DOSE_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:[-~–]\s*(\d+(?:\.\d+)?))?\s*(mg|g|μg|ug|mcg|IU|U)\s*/\s*(?:animal|cat|dog|head|羽|頭)",
    re.IGNORECASE,
)
# 投与経路
_ROUTE_RE = re.compile(
    r"\b(IV|IM|SC|PO|IO|IP|IN|ID|topical|inhaled|nebulized|epidural|intra-articular|q\.s\.|per os|ICe)\b",
    re.IGNORECASE,
)
# 投与間隔
_INTERVAL_RE = re.compile(
    r"q\s*(\d+(?:\.\d+)?)\s*(?:[-~–]\s*(\d+(?:\.\d+)?))?\s*(h|hr|hour|d|day|wk|week)",
    re.IGNORECASE,
)


@dataclass
class ParsedDose:
    """解析済み用量データ"""

    low_mg_per_kg: float | None = None
    high_mg_per_kg: float | None = None
    unit: str = "mg"
    is_iu: bool = False  # IU/Uの場合mg換算不可
    fixed_low: float | None = None  # 体重非依存の絶対量
    fixed_high: float | None = None
    routes: list[str] = field(default_factory=list)
    interval_low_h: float | None = None
    interval_high_h: float | None = None
    raw_dosage: str = ""
    parsed: bool = False


@dataclass
class DoseCalculation:
    """計算結果"""

    drug_id: str
    drug_name: str
    species: str
    body_weight_kg: float
    parsed: ParsedDose
    low_dose: float | None = None  # 最終投与量（mg or IU）
    high_dose: float | None = None
    dose_unit: str = "mg"
    volume_low_ml: float | None = None  # 製剤濃度を指定した場合
    volume_high_ml: float | None = None
    concentration_mg_per_ml: float | None = None
    warnings: list[str] = field(default_factory=list)
    routes: list[str] = field(default_factory=list)
    interval_text: str = ""


def _normalize_unit(unit: str) -> tuple[str, float | None]:
    """単位を正規化し、mg換算係数を返す"""
    u = unit.lower()
    if u in ("μg", "ug", "mcg"):
        return ("μg", _UNIT_TO_MG[u])
    if u in ("iu", "u"):
        return ("IU", None)
    return (u, _UNIT_TO_MG.get(u))


def parse_dosage(dosage_str: str) -> ParsedDose:
    """用量文字列をパース"""
    parsed = ParsedDose(raw_dosage=dosage_str or "")
    if not dosage_str:
        return parsed

    # 体重ベース用量
    match = _DOSE_RE.search(dosage_str)
    if match:
        low_str, high_str, unit_str = match.groups()
        unit_normalized, mg_factor = _normalize_unit(unit_str)
        try:
            low_val = float(low_str)
            high_val = float(high_str) if high_str else low_val
            if mg_factor is not None:
                parsed.low_mg_per_kg = low_val * mg_factor
                parsed.high_mg_per_kg = high_val * mg_factor
                parsed.unit = "mg"
            else:
                # IU/U はそのまま保持
                parsed.low_mg_per_kg = low_val
                parsed.high_mg_per_kg = high_val
                parsed.unit = unit_normalized
                parsed.is_iu = True
            parsed.parsed = True
        except ValueError:
            pass

    # 固定用量
    fixed_match = _FIXED_DOSE_RE.search(dosage_str)
    if fixed_match and not parsed.parsed:
        low_str, high_str, unit_str = fixed_match.groups()
        try:
            parsed.fixed_low = float(low_str)
            parsed.fixed_high = float(high_str) if high_str else parsed.fixed_low
            parsed.unit = unit_str.lower()
            parsed.parsed = True
        except ValueError:
            pass

    # 投与経路
    parsed.routes = list({m.upper() for m in _ROUTE_RE.findall(dosage_str)})

    # 投与間隔
    int_match = _INTERVAL_RE.search(dosage_str)
    if int_match:
        low_str, high_str, unit = int_match.groups()
        try:
            multiplier = 24.0 if unit.lower().startswith("d") else 168.0 if unit.lower().startswith("w") else 1.0
            parsed.interval_low_h = float(low_str) * multiplier
            parsed.interval_high_h = float(high_str) * multiplier if high_str else parsed.interval_low_h
        except ValueError:
            pass

    return parsed


# ---------------------------------------------------------------------------
# 種別の体重妥当性閾値 (kg)
# ---------------------------------------------------------------------------
_SPECIES_WEIGHT_RANGE = {
    "dog": (0.5, 90.0),
    "cat": (0.5, 12.0),
    "horse": (50.0, 1200.0),
    "rabbit": (0.5, 10.0),
    "hamster": (0.02, 0.2),
    "guinea_pig": (0.5, 1.5),
    "chinchilla": (0.4, 0.8),
    "ferret": (0.5, 2.5),
    "hedgehog": (0.3, 1.5),
    "sugar_glider": (0.08, 0.16),
    "degu": (0.15, 0.35),
    "bird": (0.005, 5.0),
    "parakeet": (0.025, 0.05),
    "parrot": (0.05, 1.5),
    "reptile": (0.01, 200.0),
    "tortoise": (0.05, 200.0),
    "snake": (0.01, 100.0),
    "lizard": (0.005, 10.0),
    "amphibian": (0.001, 5.0),
    "fish": (0.001, 50.0),
    "exotic_other": (0.005, 100.0),
}


def calculate_dose(
    drug: dict[str, Any],
    species: str,
    body_weight_kg: float,
    concentration_mg_per_ml: float | None = None,
) -> DoseCalculation:
    """薬品データと体重から具体的な投与量を計算"""

    species_info = (drug.get("species_info") or {}).get(species, {})
    dosage_str = species_info.get("dosage", "") or drug.get("dosage", "")
    parsed = parse_dosage(dosage_str)

    result = DoseCalculation(
        drug_id=drug.get("id", ""),
        drug_name=drug.get("name", ""),
        species=species,
        body_weight_kg=body_weight_kg,
        parsed=parsed,
        routes=parsed.routes,
    )

    # 体重妥当性チェック
    if species in _SPECIES_WEIGHT_RANGE:
        low_w, high_w = _SPECIES_WEIGHT_RANGE[species]
        if body_weight_kg < low_w * 0.5 or body_weight_kg > high_w * 1.5:
            result.warnings.append(
                f"⚠ 入力体重 {body_weight_kg} kg は {species} の通常範囲 ({low_w}-{high_w} kg) から大きく外れています"
            )

    # 安全性チェック
    if not species_info.get("safe", True):
        result.warnings.append(f"⚠ この薬品は {species} に対して安全性が確認されていない、または禁忌です")

    if not parsed.parsed:
        result.warnings.append("⚠ 用量データを自動解析できませんでした。原文を参照してください")
        return result

    # 投与量計算
    if parsed.low_mg_per_kg is not None:
        result.low_dose = parsed.low_mg_per_kg * body_weight_kg
        result.high_dose = (parsed.high_mg_per_kg or parsed.low_mg_per_kg) * body_weight_kg
        result.dose_unit = parsed.unit
    elif parsed.fixed_low is not None:
        result.low_dose = parsed.fixed_low
        result.high_dose = parsed.fixed_high
        result.dose_unit = parsed.unit
        result.warnings.append("ℹ 体重非依存の固定用量です")

    # 容量計算（製剤濃度がある場合）
    if concentration_mg_per_ml and result.low_dose and not parsed.is_iu:
        result.concentration_mg_per_ml = concentration_mg_per_ml
        result.volume_low_ml = result.low_dose / concentration_mg_per_ml
        result.volume_high_ml = (result.high_dose or result.low_dose) / concentration_mg_per_ml

    # 投与間隔テキスト
    if parsed.interval_low_h:
        if parsed.interval_high_h and parsed.interval_high_h != parsed.interval_low_h:
            result.interval_text = f"q{int(parsed.interval_low_h)}-{int(parsed.interval_high_h)}h"
        else:
            result.interval_text = f"q{int(parsed.interval_low_h)}h"

    return result


def to_dict(calc: DoseCalculation) -> dict[str, Any]:
    """DoseCalculationを辞書化（JSON返却用）"""
    return {
        "drug_id": calc.drug_id,
        "drug_name": calc.drug_name,
        "species": calc.species,
        "body_weight_kg": calc.body_weight_kg,
        "low_dose": round(calc.low_dose, 4) if calc.low_dose is not None else None,
        "high_dose": round(calc.high_dose, 4) if calc.high_dose is not None else None,
        "dose_unit": calc.dose_unit,
        "volume_low_ml": round(calc.volume_low_ml, 4) if calc.volume_low_ml is not None else None,
        "volume_high_ml": round(calc.volume_high_ml, 4) if calc.volume_high_ml is not None else None,
        "concentration_mg_per_ml": calc.concentration_mg_per_ml,
        "routes": calc.routes,
        "interval": calc.interval_text,
        "raw_dosage": calc.parsed.raw_dosage,
        "parsed": calc.parsed.parsed,
        "warnings": calc.warnings,
    }
