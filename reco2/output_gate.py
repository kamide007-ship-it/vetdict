import logging
import math
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_CONTRADICTION_PAIRS = [
    ("必ず", "かもしれません"), ("絶対に", "可能性があります"),
    ("確実に", "不確実"), ("always", "sometimes"),
    ("never", "occasionally"), ("definitely", "might"),
    ("100%", "uncertain"),
]

_SOFTEN_JA = [
    ("必ず", "多くの場合"), ("絶対に", "ほぼ"),
    ("間違いなく", "おそらく"), ("確実に", "高い確率で"),
]
_SOFTEN_EN = [
    ("definitely", "likely"), ("absolutely", "very likely"),
    ("certainly", "probably"), ("always", "typically"),
    ("never", "rarely"),
]

_ASSERT_TOKENS = [
    "必ず", "絶対", "間違いなく", "確実", "100%",
    "definitely", "absolutely", "certainly", "always", "never",
]

_PROVOCATIVE = [
    "バカ", "アホ", "ふざけるな", "舐めるな", "ゴミ",
    "使えない", "役に立たない",
    "idiot", "stupid", "shut up", "trash", "useless",
]

_EVIDENCE_MARKERS = [
    "出典", "引用", "根拠", "データ", "論文", "参考", "URL", "リンク",
    "source", "citation", "evidence", "data", "paper", "study", "link", "http://", "https://",
]

def _count_hits(text: str, words: List[str]) -> int:
    t = text.lower()
    c = 0
    for w in words:
        if not w:
            continue
        c += t.count(w.lower())
    return c

def _saturating_score(count: int, sensitivity: float = 1.0) -> float:
    return math.tanh((count / 3.0) * sensitivity)

def _contradiction_hits(text: str) -> int:
    t = text.lower()
    hits = 0
    for a, b in _CONTRADICTION_PAIRS:
        if a.lower() in t and b.lower() in t:
            hits += 1
    return hits

def analyze(
    text: str,
    w_assertion: float = 0.30,
    w_evidence: float = 0.30,
    w_contradiction: float = 0.25,
    w_provocative: float = 0.15,
    confidence: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Analyze text quality with optional AI confidence enhancement.

    Args:
        text: Text to analyze
        w_assertion: Weight for assertion density
        w_evidence: Weight for evidence gap
        w_contradiction: Weight for contradictions
        w_provocative: Weight for provocative language
        confidence: Optional AI confidence score (0.0-1.0) for enhancing results

    Returns:
        Analysis result with quality metrics and recommended action
    """
    if not isinstance(text, str):
        text = str(text or "")
    t = text.strip()

    assert_count = _count_hits(t, _ASSERT_TOKENS)
    prov_count = _count_hits(t, _PROVOCATIVE)
    contra_hits = _contradiction_hits(t)
    has_evidence = _count_hits(t, _EVIDENCE_MARKERS) > 0

    s_assert = _saturating_score(assert_count, sensitivity=1.4)

    # Evidence gap: assertions without any evidence markers should be treated as a strong gap.
    evidence_gap_count = 0
    if assert_count > 0 and not has_evidence:
        evidence_gap_count = 5  # saturate
    s_evgap = _saturating_score(evidence_gap_count, sensitivity=1.2)

    s_contra = _saturating_score(contra_hits, sensitivity=1.5)
    s_prov = _saturating_score(prov_count, sensitivity=1.3)

    post_d = (
        (s_assert * w_assertion)
        + (s_evgap * w_evidence)
        + (s_contra * w_contradiction)
        + (s_prov * w_provocative)
    )
    psi_mod = max(0.3, 1.0 - post_d * 0.7)

    # Adjust psi modifier if confidence provided
    psi_mod_adjusted = _adjust_psi_modifier_by_confidence(psi_mod, confidence)

    if post_d >= 0.70:
        level, action = "critical", "regenerate"
    elif post_d >= 0.50:
        level, action = "degraded", "soften"
    elif post_d >= 0.30:
        level, action = "cautious", "annotate"
    else:
        level, action = "healthy", "pass"

    result = {
        "scores": {
            "assertion_density": round(float(s_assert), 6),
            "evidence_gap": round(float(s_evgap), 6),
            "contradiction": round(float(s_contra), 6),
            "provocative": round(float(s_prov), 6),
        },
        "post_d": round(float(post_d), 6),
        "level": level,
        "action": action,
        "psi_modifier": round(float(psi_mod), 6),
        "counts": {
            "assertions": int(assert_count),
            "contradictions": int(contra_hits),
            "provocative": int(prov_count),
        },
        "notes": {
            "has_evidence": bool(has_evidence),
        },
    }

    # Add confidence-based adjustments if provided
    if confidence is not None:
        result["psi_modifier_adjusted"] = round(float(psi_mod_adjusted), 6)
        result["confidence_score"] = round(float(confidence), 3)
        result["adjusted_text"] = _adjust_assertion_strength(text, confidence)

    return result

def soften(text: str) -> str:
    if not isinstance(text, str):
        text = str(text or "")
    out = text
    for a, b in _SOFTEN_JA:
        out = out.replace(a, b)
    for a, b in _SOFTEN_EN:
        out = re.sub(
            re.escape(a),
            lambda match, replacement=b: _apply_case_pattern(match.group(0), replacement),
            out,
            flags=re.IGNORECASE,
        )
    return out


def _apply_case_pattern(source: str, replacement: str) -> str:
    if source.isupper():
        return replacement.upper()
    is_title_case = source[:1].isupper() and (source[1:].islower() if len(source) > 1 else True)
    if is_title_case:
        return replacement.capitalize()
    return replacement


def _adjust_assertion_strength(
    text: str, confidence: float, soften_threshold: float = 0.6, strengthen_threshold: float = 0.85
) -> str:
    """
    Adjust assertion strength based on AI confidence.

    Args:
        text: Text to adjust
        confidence: AI confidence score (0.0-1.0)
        soften_threshold: Confidence below this triggers softening
        strengthen_threshold: Confidence above this triggers strengthening

    Returns:
        Adjusted text with modified assertions
    """
    if not isinstance(text, str):
        return str(text or "")

    confidence = max(0.0, min(1.0, float(confidence)))

    # Low confidence: soften assertions
    if confidence < soften_threshold:
        return soften(text)

    # High confidence: strengthen text by removing qualifiers
    if confidence > strengthen_threshold:
        # Remove hedges and qualifiers
        out = text
        hedges = [
            ("might", "will"),
            ("may", "will"),
            ("could", "will"),
            ("possibly", ""),
            ("likely", ""),
            ("probably", ""),
            ("かもしれません", "です"),
            ("可能性があります", "あります"),
            ("おそらく", ""),
            ("多くの場合", ""),
        ]
        for a, b in hedges:
            out = re.sub(
                re.escape(a),
                lambda match, replacement=b: _apply_case_pattern(match.group(0), replacement)
                if replacement
                else "",
                out,
                flags=re.IGNORECASE,
            )
        return out

    # Mid confidence: leave as is
    return text


def _adjust_psi_modifier_by_confidence(
    psi_mod: float, confidence: Optional[float] = None
) -> float:
    """
    Adjust psi modifier based on AI confidence.

    Formula:
    - Low confidence (< 0.5): reduce psi_mod by 0.1
    - Mid confidence (0.5-0.85): use psi_mod unchanged
    - High confidence (> 0.85): increase psi_mod by 0.15

    Args:
        psi_mod: Original psi modifier
        confidence: AI confidence score (0.0-1.0), optional

    Returns:
        Adjusted psi modifier
    """
    if confidence is None:
        return psi_mod

    confidence = max(0.0, min(1.0, float(confidence)))

    if confidence < 0.5:
        # Low confidence reduces psi modifier
        adjusted = psi_mod - 0.1
    elif confidence > 0.85:
        # High confidence increases psi modifier
        adjusted = psi_mod + 0.15
    else:
        # Mid confidence: no change
        adjusted = psi_mod

    # Keep within reasonable bounds
    adjusted = max(0.3, min(adjusted, 1.0))

    logger.debug(
        f"Adjusted psi_modifier by confidence: "
        f"base={psi_mod:.3f}, confidence={confidence:.3f}, adjusted={adjusted:.3f}"
    )

    return adjusted
