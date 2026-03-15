"""Coverage tests for reco2.output_gate module."""

import pytest

from reco2.output_gate import (
    analyze,
    soften,
    _adjust_assertion_strength,
    _adjust_psi_modifier_by_confidence,
)


class TestAnalyzeCleanText:
    """analyze() with clean, neutral text returns healthy/pass."""

    def test_healthy_level(self):
        result = analyze("The weather is nice today.")
        assert result["level"] == "healthy"

    def test_pass_action(self):
        result = analyze("The weather is nice today.")
        assert result["action"] == "pass"

    def test_low_post_d(self):
        result = analyze("The weather is nice today.")
        assert result["post_d"] < 0.30

    def test_scores_present(self):
        result = analyze("The weather is nice today.")
        scores = result["scores"]
        assert "assertion_density" in scores
        assert "evidence_gap" in scores
        assert "contradiction" in scores
        assert "provocative" in scores

    def test_psi_modifier_near_one(self):
        result = analyze("The weather is nice today.")
        assert result["psi_modifier"] >= 0.9


class TestAnalyzeAssertionHeavy:
    """analyze() with assertion-heavy text produces higher assertion_density."""

    def test_assertion_density_elevated(self):
        text = "You must definitely always do this. 必ず absolutely certainly."
        result = analyze(text)
        assert result["scores"]["assertion_density"] > 0.0

    def test_assertion_count_tracked(self):
        text = "definitely always 必ず 絶対"
        result = analyze(text)
        assert result["counts"]["assertions"] >= 4

    def test_evidence_gap_when_no_evidence(self):
        text = "definitely this is true"
        result = analyze(text)
        assert result["scores"]["evidence_gap"] > 0.0

    def test_no_evidence_gap_with_evidence(self):
        text = "definitely true, source: https://example.com"
        result = analyze(text)
        assert result["scores"]["evidence_gap"] == 0.0
        assert result["notes"]["has_evidence"] is True


class TestAnalyzeContradiction:
    """analyze() detects contradictory pairs in text."""

    def test_contradiction_detected(self):
        text = "This will definitely happen, but it might not."
        result = analyze(text)
        assert result["scores"]["contradiction"] > 0.0
        assert result["counts"]["contradictions"] >= 1

    def test_japanese_contradiction(self):
        text = "必ず成功します。かもしれません。"
        result = analyze(text)
        assert result["counts"]["contradictions"] >= 1

    def test_no_contradiction_in_clean_text(self):
        result = analyze("A simple sentence with no issues.")
        assert result["counts"]["contradictions"] == 0


class TestAnalyzeProvocative:
    """analyze() detects provocative language."""

    def test_provocative_score_english(self):
        text = "This tool is stupid and useless trash."
        result = analyze(text)
        assert result["scores"]["provocative"] > 0.0
        assert result["counts"]["provocative"] >= 3

    def test_provocative_score_japanese(self):
        text = "バカみたいに使えないゴミツール"
        result = analyze(text)
        assert result["counts"]["provocative"] >= 2

    def test_no_provocative_in_clean_text(self):
        result = analyze("This is a helpful tool.")
        assert result["counts"]["provocative"] == 0


class TestAnalyzeWithConfidence:
    """analyze() with confidence parameter adjusts psi_modifier."""

    def test_confidence_adds_adjusted_fields(self):
        result = analyze("Some text", confidence=0.7)
        assert "psi_modifier_adjusted" in result
        assert "confidence_score" in result
        assert "adjusted_text" in result

    def test_low_confidence_reduces_psi(self):
        result = analyze("Some text", confidence=0.3)
        assert result["psi_modifier_adjusted"] <= result["psi_modifier"]

    def test_high_confidence_increases_psi(self):
        result = analyze("Some text", confidence=0.95)
        assert result["psi_modifier_adjusted"] >= result["psi_modifier"]

    def test_no_confidence_no_adjusted_fields(self):
        result = analyze("Some text")
        assert "psi_modifier_adjusted" not in result
        assert "confidence_score" not in result


class TestAnalyzeLevelsAndActions:
    """Verify level/action thresholds."""

    def test_critical_level(self):
        # Combine assertions + provocative + contradictions, no evidence
        text = (
            "definitely always 必ず 絶対 間違いなく certainly absolutely "
            "stupid idiot useless trash "
            "definitely might always sometimes"
        )
        result = analyze(text)
        assert result["post_d"] >= 0.70
        assert result["level"] == "critical"
        assert result["action"] == "regenerate"


class TestSoften:
    """soften() replaces absolute terms with milder alternatives."""

    def test_soften_japanese_kanarazu(self):
        assert "多くの場合" in soften("必ず成功します")
        assert "必ず" not in soften("必ず成功します")

    def test_soften_japanese_zettai(self):
        assert "ほぼ" in soften("絶対に大丈夫")
        assert "絶対に" not in soften("絶対に大丈夫")

    def test_soften_english_definitely(self):
        result = soften("This is definitely true")
        assert "likely" in result.lower()
        assert "definitely" not in result.lower()

    def test_soften_english_absolutely(self):
        result = soften("Absolutely correct")
        assert "likely" in result.lower()
        assert "absolutely" not in result.lower()

    def test_soften_english_always(self):
        result = soften("This always works")
        assert "typically" in result.lower()
        assert "always" not in result.lower()

    def test_soften_english_never(self):
        result = soften("This never fails")
        assert "rarely" in result.lower()
        assert "never" not in result.lower()

    def test_soften_preserves_clean_text(self):
        text = "The cat sat on the mat."
        assert soften(text) == text


class TestAdjustPsiModifierByConfidence:
    """_adjust_psi_modifier_by_confidence behavior."""

    def test_none_confidence_returns_original(self):
        assert _adjust_psi_modifier_by_confidence(0.8, None) == 0.8

    def test_low_confidence_reduces(self):
        result = _adjust_psi_modifier_by_confidence(0.8, 0.3)
        assert result == pytest.approx(0.7, abs=0.01)

    def test_high_confidence_increases(self):
        result = _adjust_psi_modifier_by_confidence(0.8, 0.9)
        assert result == pytest.approx(0.95, abs=0.01)

    def test_mid_confidence_unchanged(self):
        result = _adjust_psi_modifier_by_confidence(0.8, 0.7)
        assert result == pytest.approx(0.8, abs=0.01)

    def test_result_clamped_lower_bound(self):
        result = _adjust_psi_modifier_by_confidence(0.3, 0.1)
        assert result >= 0.3

    def test_result_clamped_upper_bound(self):
        result = _adjust_psi_modifier_by_confidence(1.0, 0.95)
        assert result <= 1.0


class TestAdjustAssertionStrength:
    """_adjust_assertion_strength adjusts text based on confidence."""

    def test_low_confidence_softens(self):
        result = _adjust_assertion_strength("必ず成功します", 0.3)
        assert "多くの場合" in result

    def test_high_confidence_removes_hedges(self):
        result = _adjust_assertion_strength("This might work", 0.9)
        assert "might" not in result.lower()

    def test_mid_confidence_no_change(self):
        text = "This might work well"
        result = _adjust_assertion_strength(text, 0.7)
        assert result == text

    def test_non_string_input(self):
        result = _adjust_assertion_strength(None, 0.5)
        assert isinstance(result, str)
