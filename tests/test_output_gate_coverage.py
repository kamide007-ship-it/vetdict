"""Tests for reco2/output_gate.py – coverage suite."""

import pytest

from reco2.output_gate import (
    analyze,
    soften,
    _adjust_assertion_strength,
    _adjust_psi_modifier_by_confidence,
)


# ---------------------------------------------------------------------------
# 1. analyze – clean text → "healthy" level, "pass" action
# ---------------------------------------------------------------------------
class TestAnalyzeCleanText:
    def test_healthy_level(self):
        result = analyze("The weather is nice today.")
        assert result["level"] == "healthy"
        assert result["action"] == "pass"

    def test_post_d_below_threshold(self):
        result = analyze("The weather is nice today.")
        assert result["post_d"] < 0.30

    def test_result_keys(self):
        result = analyze("Hello world")
        assert "scores" in result
        assert "post_d" in result
        assert "level" in result
        assert "action" in result
        assert "psi_modifier" in result

    def test_scores_subkeys(self):
        result = analyze("Hello world")
        scores = result["scores"]
        assert "assertion_density" in scores
        assert "evidence_gap" in scores
        assert "contradiction" in scores
        assert "provocative" in scores


# ---------------------------------------------------------------------------
# 2. analyze – assertion-heavy text → higher assertion_density
# ---------------------------------------------------------------------------
class TestAnalyzeAssertionHeavy:
    def test_japanese_assertions_raise_density(self):
        text = "必ず効果があります。絶対に安全です。確実に治ります。"
        result = analyze(text)
        assert result["scores"]["assertion_density"] > 0.0

    def test_english_assertions_raise_density(self):
        text = "This will definitely work. It is absolutely safe. You will certainly recover."
        result = analyze(text)
        assert result["scores"]["assertion_density"] > 0.0

    def test_assertion_count_tracked(self):
        text = "必ず definitely always"
        result = analyze(text)
        assert result["counts"]["assertions"] >= 3

    def test_assertion_text_more_risky_than_clean(self):
        clean = analyze("The cat sat on the mat.")
        heavy = analyze("This is definitely absolutely certainly the answer.")
        assert heavy["post_d"] > clean["post_d"]


# ---------------------------------------------------------------------------
# 3. analyze – contradictory text → contradiction detected
# ---------------------------------------------------------------------------
class TestAnalyzeContradiction:
    def test_contradiction_detected_japanese(self):
        text = "必ず効果がありますが、かもしれません。"
        result = analyze(text)
        assert result["scores"]["contradiction"] > 0.0
        assert result["counts"]["contradictions"] >= 1

    def test_contradiction_detected_english(self):
        text = "This always works, but sometimes it does not."
        result = analyze(text)
        assert result["scores"]["contradiction"] > 0.0
        assert result["counts"]["contradictions"] >= 1

    def test_no_contradiction_in_clean_text(self):
        result = analyze("A simple sentence.")
        assert result["counts"]["contradictions"] == 0


# ---------------------------------------------------------------------------
# 4. analyze – provocative text → provocative score
# ---------------------------------------------------------------------------
class TestAnalyzeProvocative:
    def test_provocative_japanese(self):
        text = "このツールは使えない。役に立たない。"
        result = analyze(text)
        assert result["scores"]["provocative"] > 0.0
        assert result["counts"]["provocative"] >= 1

    def test_provocative_english(self):
        text = "This is stupid and useless trash."
        result = analyze(text)
        assert result["scores"]["provocative"] > 0.0
        assert result["counts"]["provocative"] >= 2

    def test_no_provocative_in_clean_text(self):
        result = analyze("A polite and professional statement.")
        assert result["counts"]["provocative"] == 0


# ---------------------------------------------------------------------------
# 5. analyze – confidence parameter → adjusted psi_modifier
# ---------------------------------------------------------------------------
class TestAnalyzeWithConfidence:
    def test_confidence_adds_adjusted_fields(self):
        result = analyze("Some text.", confidence=0.7)
        assert "psi_modifier_adjusted" in result
        assert "confidence_score" in result
        assert "adjusted_text" in result

    def test_no_confidence_omits_adjusted_fields(self):
        result = analyze("Some text.")
        assert "psi_modifier_adjusted" not in result
        assert "confidence_score" not in result

    def test_low_confidence_reduces_psi(self):
        result = analyze("Some text.", confidence=0.3)
        assert result["psi_modifier_adjusted"] <= result["psi_modifier"]

    def test_high_confidence_increases_psi(self):
        result = analyze("Some text.", confidence=0.95)
        assert result["psi_modifier_adjusted"] >= result["psi_modifier"]

    def test_confidence_score_recorded(self):
        result = analyze("text", confidence=0.42)
        assert result["confidence_score"] == 0.42


# ---------------------------------------------------------------------------
# 6. soften – replaces absolute terms
# ---------------------------------------------------------------------------
class TestSoften:
    def test_japanese_kanarazu(self):
        assert "多くの場合" in soften("必ず効果があります")

    def test_japanese_zettaini(self):
        assert "ほぼ" in soften("絶対に安全です")

    def test_english_definitely(self):
        result = soften("This is definitely correct.")
        assert "definitely" not in result.lower()
        assert "likely" in result.lower()

    def test_english_absolutely(self):
        result = soften("This is absolutely safe.")
        assert "absolutely" not in result.lower()
        assert "very likely" in result.lower()

    def test_english_always(self):
        result = soften("This always works.")
        assert "always" not in result.lower()
        assert "typically" in result.lower()

    def test_english_never(self):
        result = soften("This never fails.")
        assert "never" not in result.lower()
        assert "rarely" in result.lower()

    def test_clean_text_unchanged(self):
        text = "The cat sat on the mat."
        assert soften(text) == text

    def test_case_preservation_title(self):
        result = soften("Definitely correct.")
        assert result.startswith("Likely")

    def test_non_string_input(self):
        result = soften(None)
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# 7. _adjust_psi_modifier_by_confidence
# ---------------------------------------------------------------------------
class TestAdjustPsiModifierByConfidence:
    def test_none_confidence_returns_unchanged(self):
        assert _adjust_psi_modifier_by_confidence(0.8, None) == 0.8

    def test_low_confidence_reduces(self):
        base = 0.8
        adjusted = _adjust_psi_modifier_by_confidence(base, 0.3)
        assert adjusted < base
        assert adjusted == pytest.approx(0.7, abs=0.01)

    def test_mid_confidence_unchanged(self):
        base = 0.8
        adjusted = _adjust_psi_modifier_by_confidence(base, 0.7)
        assert adjusted == base

    def test_high_confidence_increases(self):
        base = 0.8
        adjusted = _adjust_psi_modifier_by_confidence(base, 0.9)
        assert adjusted > base
        assert adjusted == pytest.approx(0.95, abs=0.01)

    def test_lower_bound_clamped(self):
        adjusted = _adjust_psi_modifier_by_confidence(0.3, 0.1)
        assert adjusted >= 0.3

    def test_upper_bound_clamped(self):
        adjusted = _adjust_psi_modifier_by_confidence(1.0, 0.95)
        assert adjusted <= 1.0


# ---------------------------------------------------------------------------
# _adjust_assertion_strength (bonus coverage)
# ---------------------------------------------------------------------------
class TestAdjustAssertionStrength:
    def test_low_confidence_softens(self):
        text = "This is definitely the answer."
        result = _adjust_assertion_strength(text, confidence=0.3)
        assert "definitely" not in result.lower()

    def test_high_confidence_strengthens(self):
        text = "This might be the answer."
        result = _adjust_assertion_strength(text, confidence=0.95)
        assert "might" not in result.lower()

    def test_mid_confidence_unchanged(self):
        text = "This might be the answer."
        result = _adjust_assertion_strength(text, confidence=0.7)
        assert result == text

    def test_non_string_input(self):
        result = _adjust_assertion_strength(None, confidence=0.5)
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# Level / action boundary tests
# ---------------------------------------------------------------------------
class TestLevelBoundaries:
    def test_degraded_level(self):
        # Lots of assertions without evidence → high post_d
        text = "必ず 絶対 間違いなく 確実 definitely absolutely certainly always"
        result = analyze(text)
        # Should be at least cautious or higher
        assert result["level"] in ("cautious", "degraded", "critical")
        assert result["action"] in ("annotate", "soften", "regenerate")

    def test_has_evidence_noted(self):
        text = "Source: https://example.com"
        result = analyze(text)
        assert result["notes"]["has_evidence"] is True

    def test_no_evidence_noted(self):
        result = analyze("No references here.")
        assert result["notes"]["has_evidence"] is False
