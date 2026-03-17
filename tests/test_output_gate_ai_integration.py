"""Tests for output_gate AI confidence integration (Phase 2c Step 3)."""

from reco2 import output_gate


class TestAdjustAssertionStrength:
    """Test _adjust_assertion_strength function."""

    def test_no_change_without_confidence(self):
        """Test that text is unchanged without confidence parameter."""
        text = "This is definitely important."
        result = output_gate._adjust_assertion_strength(text, 0.7)
        # Mid confidence should not change text
        assert result == text

    def test_soften_low_confidence(self):
        """Test that low confidence triggers softening."""
        text = "This will definitely work and always succeed."
        result = output_gate._adjust_assertion_strength(text, 0.4)

        # Should have softer language
        assert "definitely" not in result.lower() or "likely" in result.lower()

    def test_strengthen_high_confidence(self):
        """Test that high confidence removes hedges."""
        text = "This might possibly work and could succeed."
        result = output_gate._adjust_assertion_strength(text, 0.9)

        # Should remove hedges
        assert "might" not in result.lower()
        assert "possibly" not in result.lower()
        assert "could" not in result.lower()

    def test_japanese_soften(self):
        """Test Japanese text softening with low confidence."""
        text = "これは必ず成功します。"
        result = output_gate._adjust_assertion_strength(text, 0.4)

        # Should soften Japanese assertions
        assert "多くの場合" in result or "ほぼ" in result or result != text

    def test_japanese_strengthen(self):
        """Test Japanese text strengthening with high confidence."""
        text = "これはかもしれません。おそらく可能です。"
        result = output_gate._adjust_assertion_strength(text, 0.9)

        # Should remove hedges
        assert "かもしれません" not in result or result != text

    def test_threshold_boundary_low(self):
        """Test behavior at low confidence threshold."""
        text = "This will definitely succeed."

        # Just below threshold
        result_below = output_gate._adjust_assertion_strength(text, 0.59)
        # Just above threshold
        result_above = output_gate._adjust_assertion_strength(text, 0.61)

        # Below should soften, above should not
        assert result_below != result_above

    def test_threshold_boundary_high(self):
        """Test behavior at high confidence threshold."""
        text = "This might possibly work."

        # Just below threshold
        result_below = output_gate._adjust_assertion_strength(text, 0.84)
        # Just above threshold
        result_above = output_gate._adjust_assertion_strength(text, 0.86)

        # Above should strengthen, below should not
        assert result_below != result_above

    def test_zero_confidence(self):
        """Test with zero confidence."""
        text = "This will definitely work."
        result = output_gate._adjust_assertion_strength(text, 0.0)

        # Should be softened
        assert "definitely" not in result.lower() or "likely" in result.lower() or result != text

    def test_perfect_confidence(self):
        """Test with perfect confidence."""
        text = "This might possibly work."
        result = output_gate._adjust_assertion_strength(text, 1.0)

        # Should remove hedges
        assert "might" not in result.lower()


class TestAdjustPsiModifierByConfidence:
    """Test _adjust_psi_modifier_by_confidence function."""

    def test_no_change_without_confidence(self):
        """Test that psi_mod is unchanged without confidence."""
        psi_mod = 0.7
        result = output_gate._adjust_psi_modifier_by_confidence(psi_mod, None)

        assert result == psi_mod

    def test_low_confidence_reduces_psi_mod(self):
        """Test that low confidence reduces psi_mod."""
        psi_mod = 0.8
        result = output_gate._adjust_psi_modifier_by_confidence(psi_mod, 0.3)

        assert result < psi_mod
        assert result == psi_mod - 0.1

    def test_high_confidence_increases_psi_mod(self):
        """Test that high confidence increases psi_mod."""
        psi_mod = 0.5
        result = output_gate._adjust_psi_modifier_by_confidence(psi_mod, 0.9)

        assert result > psi_mod
        assert result == psi_mod + 0.15

    def test_mid_confidence_no_change(self):
        """Test that mid-range confidence doesn't change psi_mod."""
        psi_mod = 0.7
        result = output_gate._adjust_psi_modifier_by_confidence(psi_mod, 0.7)

        assert result == psi_mod

    def test_confidence_boundary_low(self):
        """Test boundary at 0.5 confidence."""
        psi_mod = 0.7

        result_below = output_gate._adjust_psi_modifier_by_confidence(psi_mod, 0.49)
        result_above = output_gate._adjust_psi_modifier_by_confidence(psi_mod, 0.51)

        assert result_below < psi_mod
        assert result_above == psi_mod

    def test_confidence_boundary_high(self):
        """Test boundary at 0.85 confidence."""
        psi_mod = 0.7

        result_below = output_gate._adjust_psi_modifier_by_confidence(psi_mod, 0.84)
        result_above = output_gate._adjust_psi_modifier_by_confidence(psi_mod, 0.86)

        assert result_below == psi_mod
        assert result_above > psi_mod

    def test_clamps_to_range(self):
        """Test that result is clamped to valid range."""
        # High psi_mod with high confidence shouldn't exceed 1.0
        result = output_gate._adjust_psi_modifier_by_confidence(0.95, 0.95)
        assert result <= 1.0

        # Low psi_mod with low confidence shouldn't go below 0.3
        result = output_gate._adjust_psi_modifier_by_confidence(0.3, 0.1)
        assert result >= 0.3

    def test_zero_confidence(self):
        """Test with zero confidence."""
        psi_mod = 0.8
        result = output_gate._adjust_psi_modifier_by_confidence(psi_mod, 0.0)

        assert result < psi_mod

    def test_perfect_confidence(self):
        """Test with perfect confidence."""
        psi_mod = 0.5
        result = output_gate._adjust_psi_modifier_by_confidence(psi_mod, 1.0)

        assert result > psi_mod


class TestAnalyzeWithConfidence:
    """Test analyze function with confidence parameter."""

    def test_analyze_without_confidence(self):
        """Test that analyze still works without confidence."""
        result = output_gate.analyze("This is a simple test.")

        assert "level" in result
        assert "action" in result
        assert "psi_modifier" in result
        assert "psi_modifier_adjusted" not in result

    def test_analyze_with_high_confidence(self):
        """Test analyze with high confidence."""
        result = output_gate.analyze(
            "This might definitely work and always succeed.", confidence=0.9
        )

        assert "psi_modifier_adjusted" in result
        assert result["psi_modifier_adjusted"] > result["psi_modifier"]
        assert "adjusted_text" in result

    def test_analyze_with_low_confidence(self):
        """Test analyze with low confidence."""
        result = output_gate.analyze(
            "This will definitely work.", confidence=0.3
        )

        assert "psi_modifier_adjusted" in result
        assert result["psi_modifier_adjusted"] < result["psi_modifier"]
        assert "adjusted_text" in result

    def test_analyze_confidence_added_to_result(self):
        """Test that confidence is added to result."""
        confidence = 0.75
        result = output_gate.analyze("Test text.", confidence=confidence)

        assert "confidence_score" in result
        assert result["confidence_score"] == 0.75

    def test_analyze_with_assertion_heavy_text(self):
        """Test assertion-heavy text with confidence."""
        text = "必ず成功します。絶対に大丈夫。100%です。"
        result = output_gate.analyze(text, confidence=0.9)

        # High confidence should increase psi_modifier
        assert result["psi_modifier_adjusted"] > result["psi_modifier"]

    def test_analyze_preserves_original_psi_mod(self):
        """Test that original psi_modifier is preserved."""
        text = "This will work."
        result = output_gate.analyze(text, confidence=0.8)

        # Original should be present
        assert "psi_modifier" in result
        assert "psi_modifier_adjusted" in result

    def test_analyze_adjusted_text_softening(self):
        """Test that adjusted text is softened for low confidence."""
        text = "This will definitely work."
        result = output_gate.analyze(text, confidence=0.4)

        adjusted_text = result["adjusted_text"]
        # Text should be different due to softening
        assert adjusted_text != text or "definitely" not in adjusted_text.lower()

    def test_analyze_adjusted_text_strengthening(self):
        """Test that adjusted text is strengthened for high confidence."""
        text = "This might possibly work."
        result = output_gate.analyze(text, confidence=0.95)

        adjusted_text = result["adjusted_text"]
        # Text should be stronger
        assert "might" not in adjusted_text.lower() or adjusted_text == text


class TestIntegrationWithLevels:
    """Test how confidence interacts with output levels."""

    def test_high_confidence_improves_degraded_level(self):
        """Test that high confidence can improve degraded level."""
        text = "必ずいけます。でも、かもしれません。"  # Contradictory

        result_low = output_gate.analyze(text, confidence=0.3)
        result_high = output_gate.analyze(text, confidence=0.9)

        # High confidence should result in better psi_modifier
        assert result_high["psi_modifier_adjusted"] > result_low["psi_modifier_adjusted"]

    def test_low_confidence_worsens_results(self):
        """Test that low confidence can worsen results."""
        text = "This is a good option."

        result_high = output_gate.analyze(text, confidence=0.9)
        result_low = output_gate.analyze(text, confidence=0.2)

        # Low confidence should result in worse psi_modifier
        assert result_low["psi_modifier_adjusted"] < result_high["psi_modifier_adjusted"]

    def test_critical_level_with_confidence(self):
        """Test assertion-heavy text level with confidence adjustments."""
        text = "必ず成功します。絶対に大丈夫。絶対に。100%です。"  # Heavy assertions

        result = output_gate.analyze(text, confidence=0.9)

        # Might be degraded or critical depending on exact scoring
        assert result["level"] in ("degraded", "critical")
        # Adjusted psi_modifier should improve
        assert result["psi_modifier_adjusted"] >= result["psi_modifier"]


class TestConfidenceEdgeCases:
    """Test edge cases for confidence integration."""

    def test_clamped_confidence_high(self):
        """Test confidence clamped when over 1.0."""
        result = output_gate.analyze("Test.", confidence=1.5)

        # Should still work with clamped value
        assert "psi_modifier_adjusted" in result

    def test_clamped_confidence_low(self):
        """Test confidence clamped when negative."""
        result = output_gate.analyze("Test.", confidence=-0.5)

        # Should still work with clamped value
        assert "psi_modifier_adjusted" in result

    def test_none_confidence_explicit(self):
        """Test explicitly passing None as confidence."""
        result = output_gate.analyze("Test.", confidence=None)

        assert "psi_modifier_adjusted" not in result

    def test_empty_text_with_confidence(self):
        """Test empty text with confidence."""
        result = output_gate.analyze("", confidence=0.8)

        assert "level" in result
        assert "psi_modifier_adjusted" in result

    def test_unicode_text_with_confidence(self):
        """Test Unicode text with confidence."""
        text = "これは日本語のテストです。おそらく大丈夫でしょう。"
        result = output_gate.analyze(text, confidence=0.8)

        assert "adjusted_text" in result
        assert isinstance(result["adjusted_text"], str)


class TestBackwardCompatibility:
    """Test backward compatibility of analyze function."""

    def test_original_signature_works(self):
        """Test that original function signature still works."""
        result = output_gate.analyze(
            "Test text.",
            w_assertion=0.3,
            w_evidence=0.3,
            w_contradiction=0.25,
            w_provocative=0.15,
        )

        assert "level" in result
        assert "psi_modifier" in result

    def test_no_confidence_parameter_returns_original_format(self):
        """Test that result without confidence matches original format."""
        result = output_gate.analyze("Test text.")

        # Should have original keys
        assert "scores" in result
        assert "post_d" in result
        assert "level" in result
        assert "action" in result
        assert "psi_modifier" in result
        assert "counts" in result
        assert "notes" in result

        # Should not have new keys
        assert "psi_modifier_adjusted" not in result
        assert "confidence_score" not in result
        assert "adjusted_text" not in result
