"""treatment_plan.py - 鑑別診断から治療プラン生成

確定診断（または高信頼度鑑別）と患者情報から、構造化された治療プランを生成する。
- 疾患の治療プロトコル抽出
- 薬品名の自動検出と用量計算
- 薬品-薬品相互作用の自動チェック
- 動物種特異的禁忌の警告
- モニタリング指標の抽出
- エビデンスグレードの付与
- チェックリスト生成

設計原則:
- 一つの疾患 + 患者情報 → 一つの構造化プラン
- 薬品検出は drug_dictionary との照合
- 全ての推奨に対してエビデンスバッジを付与
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from api.dose_calculator import calculate_dose
from api.dose_calculator import to_dict as dose_to_dict
from api.drug_interactions import (
    find_interactions,
    find_species_specific_warnings,
)
from api.evidence_grading import assess as evidence_assess

# ---------------------------------------------------------------------------
# モニタリング指標の検出パターン
# ---------------------------------------------------------------------------
_MONITORING_TERMS = [
    # 検査項目
    ("BUN", "腎機能（BUN）"),
    ("creatinine", "クレアチニン"),
    ("ALT", "肝酵素（ALT）"),
    ("AST", "肝酵素（AST）"),
    ("ALP", "肝酵素（ALP）"),
    ("CBC", "全血球計算（CBC）"),
    ("PCV", "ヘマトクリット（PCV）"),
    ("PT", "プロトロンビン時間（PT）"),
    ("INR", "INR（凝固）"),
    ("electrolyte", "電解質"),
    ("potassium", "カリウム"),
    ("calcium", "カルシウム"),
    ("glucose", "血糖"),
    ("血糖", "血糖"),
    ("trough", "トラフ濃度"),
    ("level", "薬物血中濃度"),
    # バイタル
    ("blood pressure", "血圧"),
    ("heart rate", "心拍数"),
    ("respiratory rate", "呼吸数"),
    ("temperature", "体温"),
    ("ECG", "心電図"),
    ("oxygen", "酸素飽和度"),
    ("SpO2", "SpO2"),
]


@dataclass
class DrugRecommendation:
    """薬品推奨エントリ"""

    drug_id: str
    drug_name: str
    drug_name_ja: str
    raw_dosage: str  # 治療文中から抽出された生の用量文字列
    calculated_dose: dict[str, Any] | None = None  # 体重指定時のみ
    species_safe: bool = True
    species_warnings: list[dict[str, Any]] = field(default_factory=list)
    evidence_grade: str = "D"


@dataclass
class TreatmentPlan:
    """構造化治療プラン"""

    disease_id: str
    disease_name: str
    disease_name_ja: str
    species: str
    body_weight_kg: float | None
    treatment_text: str  # 元の治療プロトコル（参考表示用）
    treatment_text_ja: str

    drugs: list[DrugRecommendation] = field(default_factory=list)
    drug_drug_interactions: list[dict[str, Any]] = field(default_factory=list)
    monitoring_parameters: list[dict[str, str]] = field(default_factory=list)
    overall_evidence_grade: str = "D"
    overall_evidence_score: int = 0

    checklist: list[dict[str, str]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _detect_drugs_in_text(text: str, drug_lookup: dict[str, dict[str, Any]]) -> list[str]:
    """
    治療文中に含まれる薬品IDを検出する。
    drug_lookup: {drug_id: drug_dict} のマッピング
    """
    if not text:
        return []
    detected: list[str] = []
    text_lower = text.lower()
    for drug_id, drug in drug_lookup.items():
        names = [drug_id]
        if drug.get("name"):
            names.append(drug["name"].lower())
        if drug.get("name_ja"):
            names.append(drug["name_ja"])
        for name in names:
            if not name or len(name) < 4:  # 短すぎる名前は誤検出回避
                continue
            # 単語境界で照合（英語のみ）
            if name.lower() in text_lower or name in text:
                if drug_id not in detected:
                    detected.append(drug_id)
                break
    return detected


def _extract_dose_for_drug_in_text(text: str, drug_id: str, drug_name: str) -> str:
    """治療文中から特定薬品の用量を抽出"""
    if not text:
        return ""
    # 薬品名後の用量部分を抽出 (薬品名 + 数値 + 単位/kg)
    # 大文字小文字無視で薬品名を検索し、その後30文字程度を見る
    pattern = re.compile(
        re.escape(drug_name) + r"\s*[:：]?\s*([^.]{0,100}?(?:mg|μg|ug|mcg|g|IU|U)\s*/\s*kg[^.]{0,30})",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return ""


def _extract_monitoring(text: str) -> list[dict[str, str]]:
    """治療文からモニタリング指標を抽出"""
    if not text:
        return []
    found: list[dict[str, str]] = []
    seen: set[str] = set()
    text_lower = text.lower()
    for keyword, label_ja in _MONITORING_TERMS:
        if keyword.lower() in text_lower and keyword not in seen:
            seen.add(keyword)
            found.append({"key": keyword, "label_en": keyword, "label_ja": label_ja})
    return found


def _generate_checklist(
    drugs: list[DrugRecommendation],
    monitoring: list[dict[str, str]],
    has_emergency_drug: bool,
    species: str,
    lang: str = "ja",
) -> list[dict[str, str]]:
    """治療プランのチェックリスト生成"""
    items: list[dict[str, str]] = []

    # 1. 患者評価
    items.append(
        {
            "category": "assessment",
            "ja": "患者の現病歴・既往歴・併用薬の確認",
            "en": "Verify patient history, comorbidities, and concurrent medications",
        }
    )
    items.append(
        {
            "category": "assessment",
            "ja": "体重・バイタルサイン記録",
            "en": "Record body weight and vital signs",
        }
    )

    # 2. 薬品処方前確認
    if drugs:
        items.append(
            {
                "category": "prescription",
                "ja": "薬品禁忌・アレルギー歴の最終確認",
                "en": "Final check of contraindications and allergy history",
            }
        )
        items.append(
            {
                "category": "prescription",
                "ja": "薬品相互作用チェック（既存処方との照合）",
                "en": "Check drug interactions with existing prescriptions",
            }
        )
        items.append(
            {
                "category": "prescription",
                "ja": f"用量計算の独立確認（{species}の体重ベース）",
                "en": f"Independent verification of dose calculation ({species} body weight)",
            }
        )
        items.append(
            {
                "category": "prescription",
                "ja": "薬品添付文書の確認",
                "en": "Review drug package inserts",
            }
        )

    # 3. インフォームドコンセント
    items.append(
        {
            "category": "consent",
            "ja": "オーナーへの治療目的・期待される効果・副作用の説明",
            "en": "Explain treatment purpose, expected benefits, and adverse effects to owner",
        }
    )
    items.append(
        {
            "category": "consent",
            "ja": "予後の説明と再診時期の提示",
            "en": "Discuss prognosis and follow-up schedule",
        }
    )

    # 4. モニタリング
    if monitoring:
        items.append(
            {
                "category": "monitoring",
                "ja": "モニタリング指標のベースライン取得",
                "en": "Obtain baseline values for monitoring parameters",
            }
        )
        items.append(
            {
                "category": "monitoring",
                "ja": "再評価間隔の設定（薬剤・重症度に応じて）",
                "en": "Set re-evaluation interval based on drug and severity",
            }
        )

    # 5. 緊急時
    if has_emergency_drug:
        items.append(
            {
                "category": "emergency",
                "ja": "副作用・有害事象への対応プロトコルの準備",
                "en": "Prepare adverse event response protocol",
            }
        )

    return items


def build_treatment_plan(
    disease: dict[str, Any],
    drug_lookup: dict[str, dict[str, Any]],
    species: str,
    body_weight_kg: float | None = None,
    lang: str = "ja",
) -> TreatmentPlan:
    """
    疾患データと患者情報から構造化治療プランを生成。

    Args:
        disease: {name, name_ja, treatment, treatment_ja, species, urgency, ...}
        drug_lookup: 薬品DB全体（drug_id → drug_dict）
        species: 動物種ID
        body_weight_kg: 体重（任意。指定時は用量計算）
        lang: 言語
    """
    treatment_text = disease.get("treatment", "") or ""
    treatment_text_ja = disease.get("treatment_ja", "") or ""
    # 検出は両言語のテキストで行う
    combined_text = f"{treatment_text}\n{treatment_text_ja}"

    # 薬品検出
    detected_drug_ids = _detect_drugs_in_text(combined_text, drug_lookup)

    # 各薬品の推奨情報構築
    drugs: list[DrugRecommendation] = []
    for did in detected_drug_ids:
        drug = drug_lookup.get(did)
        if not drug:
            continue

        raw_dose = _extract_dose_for_drug_in_text(combined_text, did, drug.get("name", did))

        # 用量計算（体重指定時）
        calc_dict = None
        if body_weight_kg and body_weight_kg > 0:
            try:
                calc = calculate_dose(drug, species, body_weight_kg)
                calc_dict = dose_to_dict(calc)
            except Exception:
                pass

        # 動物種安全性
        si = (drug.get("species_info") or {}).get(species, {})
        species_safe = si.get("safe", True) if si else True
        species_warnings = find_species_specific_warnings(did, species)

        # エビデンスグレード（薬品エントリの説明全体から）
        drug_text = " ".join(
            [
                drug.get("mechanism", "") or "",
                drug.get("notes", "") or "",
                si.get("notes", "") or "",
                si.get("dosage", "") or "",
            ]
        )
        ev = evidence_assess(drug_text)

        drugs.append(
            DrugRecommendation(
                drug_id=did,
                drug_name=drug.get("name", did),
                drug_name_ja=drug.get("name_ja", drug.get("name", did)),
                raw_dosage=raw_dose,
                calculated_dose=calc_dict,
                species_safe=species_safe,
                species_warnings=species_warnings,
                evidence_grade=ev.grade,
            )
        )

    # 薬品-薬品相互作用
    interactions = find_interactions(detected_drug_ids) if len(detected_drug_ids) >= 2 else []

    # モニタリング
    monitoring = _extract_monitoring(combined_text)

    # 全体エビデンスグレード（治療文から）
    overall_ev = evidence_assess(combined_text)

    # 警告メッセージ
    warnings: list[str] = []
    if not body_weight_kg:
        warnings.append(
            "体重未指定のため用量計算は省略されています。正確な処方には体重入力をお願いします。"
            if lang == "ja"
            else "Body weight not specified — dose calculation skipped. Provide weight for accurate prescribing."
        )
    if any(not d.species_safe for d in drugs):
        warnings.append(
            "⚠ この動物種で安全性が確認されていない薬品が含まれます。代替薬を検討してください。"
            if lang == "ja"
            else "⚠ Plan contains drugs not verified safe for this species. Consider alternatives."
        )
    if any(d.species_warnings for d in drugs):
        warnings.append(
            "⚠ 動物種特異的禁忌警告があります。詳細を確認してください。"
            if lang == "ja"
            else "⚠ Species-specific contraindications detected. Review carefully."
        )
    if interactions:
        warnings.append(
            f"⚠ {len(interactions)}件の薬品相互作用が検出されました。"
            if lang == "ja"
            else f"⚠ {len(interactions)} drug-drug interaction(s) detected."
        )

    has_emergency_drug = (disease.get("urgency", "") or "").lower() == "emergency"

    plan = TreatmentPlan(
        disease_id=disease.get("id", "") or disease.get("disease_id", ""),
        disease_name=disease.get("name", ""),
        disease_name_ja=disease.get("name_ja", disease.get("name", "")),
        species=species,
        body_weight_kg=body_weight_kg,
        treatment_text=treatment_text,
        treatment_text_ja=treatment_text_ja,
        drugs=drugs,
        drug_drug_interactions=interactions,
        monitoring_parameters=monitoring,
        overall_evidence_grade=overall_ev.grade,
        overall_evidence_score=overall_ev.score,
        checklist=_generate_checklist(drugs, monitoring, has_emergency_drug, species, lang=lang),
        warnings=warnings,
    )
    return plan


def to_dict(plan: TreatmentPlan) -> dict[str, Any]:
    """JSON返却用に辞書化"""
    return {
        "disease_id": plan.disease_id,
        "disease_name": plan.disease_name,
        "disease_name_ja": plan.disease_name_ja,
        "species": plan.species,
        "body_weight_kg": plan.body_weight_kg,
        "treatment_text": plan.treatment_text,
        "treatment_text_ja": plan.treatment_text_ja,
        "drugs": [
            {
                "drug_id": d.drug_id,
                "drug_name": d.drug_name,
                "drug_name_ja": d.drug_name_ja,
                "raw_dosage": d.raw_dosage,
                "calculated_dose": d.calculated_dose,
                "species_safe": d.species_safe,
                "species_warnings": d.species_warnings,
                "evidence_grade": d.evidence_grade,
            }
            for d in plan.drugs
        ],
        "drug_drug_interactions": plan.drug_drug_interactions,
        "monitoring_parameters": plan.monitoring_parameters,
        "overall_evidence_grade": plan.overall_evidence_grade,
        "overall_evidence_score": plan.overall_evidence_score,
        "checklist": plan.checklist,
        "warnings": plan.warnings,
    }
