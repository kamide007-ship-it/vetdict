"""evidence_grading.py - エビデンスグレード判定モジュール

治療プロトコル・推奨事項のエビデンス強度を分類する。
GRADE-inspired 4段階分類（A/B/C/D）。

設計原則:
- 引用文献の有無・質を機械的に検出
- 用量・投与経路・モニタリング指標の詳細度を評価
- AI生成データへの注意喚起

使用方針:
- ユーザーには「このアプリのデータはAI支援で生成されたものを獣医師がレビュー」と明示
- エビデンスバッジで信頼性を可視化
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# エビデンスグレード定義
# ---------------------------------------------------------------------------
GRADE_A = "A"  # 高: 専門家コンセンサス/CVMガイドラインに準拠した明確な引用
GRADE_B = "B"  # 中: 教科書レベルの引用 (Plumb's, Lumb & Jones, Ettinger等)
GRADE_C = "C"  # 低: 一般的な臨床実践記述、引用は弱い
GRADE_D = "D"  # 不明: AI生成主体、引用や具体性なし

GRADE_LABELS = {
    GRADE_A: {"en": "Strong evidence", "ja": "高エビデンス"},
    GRADE_B: {"en": "Moderate evidence", "ja": "中等度エビデンス"},
    GRADE_C: {"en": "Limited evidence", "ja": "限定的エビデンス"},
    GRADE_D: {"en": "Unclear evidence", "ja": "エビデンス不明"},
}

GRADE_COLORS = {
    GRADE_A: "#16a34a",  # green
    GRADE_B: "#0891b2",  # cyan
    GRADE_C: "#d97706",  # orange
    GRADE_D: "#6b7280",  # gray
}

# ---------------------------------------------------------------------------
# 引用文献の質的評価
# ---------------------------------------------------------------------------
_HIGH_QUALITY_REFS = re.compile(
    r"\b(ACVIM|AAHA|AAFP|ISFM|WSAVA|RECOVER|ISCAID|FECAVA|AVMA|ECVN|ECVAA|"
    r"BSAVA|AVA|RVC|Cochrane|ACVS|ACVO|ACVD|ACVR|ACVN|ACVECC)\b",
    re.IGNORECASE,
)
_TEXTBOOK_REFS = re.compile(
    r"\b(Plumb|Lumb|Jones|Ettinger|Greene|Stashak|Reed|Bayly|Dyson|Mader|"
    r"Quesenberry|Carpenter|Harkness|Dixon|Tully|Doneley|Speer|Beaufrère|"
    r"Wright|Whitaker|Nelson|Couto)('s)?\s*(?:&|and)?\s*\w*",
    re.IGNORECASE,
)
_JOURNAL_REFS = re.compile(
    r"\b(JAVMA|JVIM|VS\b|VRR|JFMS|JSAP|JAAHA|EVE|JAMA|NEJM|"
    r"Vet\s*(?:J|Rec|Surg|Anaesth)|Equine\s*Vet\s*J|Avian\s*Pathol)\b",
    re.IGNORECASE,
)
_YEAR_REF = re.compile(r"(?:Ref|参考)\s*[:：]?\s*[A-Z][a-zA-Z\-]+\s*\d{4}|\(\d{4}\)|\b(19|20)\d{2}\b")


# ---------------------------------------------------------------------------
# 治療プロトコルの詳細度評価
# ---------------------------------------------------------------------------
_DOSE_PATTERN = re.compile(
    r"\d+(?:\.\d+)?\s*(?:[-~–]\s*\d+(?:\.\d+)?)?\s*(?:mg|μg|ug|mcg|g|IU|U)\s*/\s*kg", re.IGNORECASE
)
_ROUTE_PATTERN = re.compile(r"\b(IV|IM|SC|PO|IO|IP|topical|inhaled|nebulized)\b")
_INTERVAL_PATTERN = re.compile(r"\bq\d+(?:[-~–]\d+)?\s*(?:h|d|wk)\b", re.IGNORECASE)
_MONITORING_PATTERN = re.compile(
    r"(monitor|monitoring|モニタリング|監視|trough|peak|level|levels|"
    r"BUN|creatinine|ALT|AST|PCV|PT|INR|血糖|電解質)",
    re.IGNORECASE,
)


@dataclass
class EvidenceAssessment:
    """エビデンス評価結果"""

    grade: str
    grade_label_en: str
    grade_label_ja: str
    color: str
    score: int  # 0-100の内部スコア
    has_citation: bool
    citation_quality: str  # "high" / "textbook" / "journal" / "year_only" / "none"
    has_dosing: bool
    has_route: bool
    has_interval: bool
    has_monitoring: bool
    detected_refs: list[str]


def _extract_citations(text: str) -> tuple[str, list[str]]:
    """引用文献を検出し、最高品質を返す"""
    if not text:
        return ("none", [])

    refs: list[str] = []

    high_match = _HIGH_QUALITY_REFS.findall(text)
    if high_match:
        refs.extend([m.upper() if isinstance(m, str) else m[0] for m in high_match])
        return ("high", list(set(refs)))

    textbook_match = _TEXTBOOK_REFS.findall(text)
    if textbook_match:
        # tuples of groups; take first
        clean = [m[0] if isinstance(m, tuple) else m for m in textbook_match]
        refs.extend(clean)
        return ("textbook", list(set(refs)))

    journal_match = _JOURNAL_REFS.findall(text)
    if journal_match:
        refs.extend([m if isinstance(m, str) else m[0] for m in journal_match])
        return ("journal", list(set(refs)))

    if _YEAR_REF.search(text):
        return ("year_only", [])

    return ("none", [])


def assess(text: str) -> EvidenceAssessment:
    """治療プロトコル文字列のエビデンスを評価"""
    text = text or ""

    citation_quality, refs = _extract_citations(text)
    has_citation = citation_quality != "none"
    has_dosing = bool(_DOSE_PATTERN.search(text))
    has_route = bool(_ROUTE_PATTERN.search(text))
    has_interval = bool(_INTERVAL_PATTERN.search(text))
    has_monitoring = bool(_MONITORING_PATTERN.search(text))

    # スコア算定
    score = 0
    if citation_quality == "high":
        score += 40
    elif citation_quality == "textbook":
        score += 30
    elif citation_quality == "journal":
        score += 25
    elif citation_quality == "year_only":
        score += 10
    if has_dosing:
        score += 20
    if has_route:
        score += 15
    if has_interval:
        score += 10
    if has_monitoring:
        score += 15

    # グレード判定
    if score >= 70 and citation_quality in ("high", "textbook"):
        grade = GRADE_A
    elif score >= 50:
        grade = GRADE_B
    elif score >= 25:
        grade = GRADE_C
    else:
        grade = GRADE_D

    return EvidenceAssessment(
        grade=grade,
        grade_label_en=GRADE_LABELS[grade]["en"],
        grade_label_ja=GRADE_LABELS[grade]["ja"],
        color=GRADE_COLORS[grade],
        score=score,
        has_citation=has_citation,
        citation_quality=citation_quality,
        has_dosing=has_dosing,
        has_route=has_route,
        has_interval=has_interval,
        has_monitoring=has_monitoring,
        detected_refs=refs[:5],  # 最大5件
    )


def to_dict(assessment: EvidenceAssessment) -> dict:
    """JSON返却用に辞書化"""
    return {
        "grade": assessment.grade,
        "grade_label_en": assessment.grade_label_en,
        "grade_label_ja": assessment.grade_label_ja,
        "color": assessment.color,
        "score": assessment.score,
        "has_citation": assessment.has_citation,
        "citation_quality": assessment.citation_quality,
        "has_dosing": assessment.has_dosing,
        "has_route": assessment.has_route,
        "has_interval": assessment.has_interval,
        "has_monitoring": assessment.has_monitoring,
        "detected_refs": assessment.detected_refs,
    }


# ---------------------------------------------------------------------------
# AI生成・臨床免責事項テキスト
# ---------------------------------------------------------------------------
AI_CONTENT_DISCLAIMER = {
    "ja": (
        "本データは AI 補助で生成され、獣医師レビューを経たものを掲載していますが、"
        "個別症例の確定診断・治療方針の決定には必ず獣医師の臨床判断と最新の参考文献を"
        "ご確認ください。用量・薬品相互作用は処方前に必ず再確認することを強く推奨します。"
    ),
    "en": (
        "This data is AI-assisted and reviewed by veterinarians, but for individual case "
        "diagnosis and treatment decisions, always rely on clinical judgment and consult "
        "current authoritative references. Always verify doses and drug interactions "
        "before prescribing."
    ),
}

DIAGNOSTIC_DISCLAIMER = {
    "ja": (
        "AIによる鑑別診断結果は参考情報であり、確定診断ではありません。"
        "信頼度スコアはアルゴリズム計算値であり、実臨床での感度/特異度の検証は進行中です。"
        "必ず病歴・身体検査・追加検査と総合して判断してください。"
    ),
    "en": (
        "AI differential diagnosis results are reference information only, not definitive "
        "diagnoses. Confidence scores are algorithmic calculations; clinical sensitivity/"
        "specificity validation is ongoing. Always integrate with history, physical exam, "
        "and additional diagnostics."
    ),
}

DOSE_CALCULATOR_DISCLAIMER = {
    "ja": (
        "計算結果は薬品データベースの記載用量範囲に基づく参考値です。"
        "個別症例（年齢・体調・併用薬・腎肝機能等）に応じた用量調整は必ず処方獣医師が判断してください。"
        "投与前に薬品添付文書も確認することを推奨します。"
    ),
    "en": (
        "Calculated values are references based on documented dose ranges from the drug database. "
        "Individualized dose adjustments (age, condition, concurrent medications, renal/hepatic function, etc.) "
        "are the prescribing veterinarian's responsibility. Verify the drug package insert before administration."
    ),
}
