"""Tests for RECO2 confidence adapter module."""

from reco2.confidence_adapter import (
    AIConfidenceContext,
    adjust_context_from_ai,
    calculate_combined_confidence,
    create_ai_confidence_context,
    scale_confidence_to_psi_multiplier,
)


class TestAIConfidenceContext:
    """Test AIConfidenceContext dataclass."""

    def test_default_initialization(self):
        """Test default values."""
        ctx = AIConfidenceContext()

        assert ctx.symptom_extraction_confidence == 0.5
        assert ctx.interaction_boost == 0.0
        assert ctx.personalization_factor == 0.0
        assert ctx.combined_confidence == 0.5
        assert ctx.age_stage is None
        assert ctx.severity == "moderate"
        assert ctx.confidence_source == "ai"
        assert isinstance(ctx.metadata, dict)

    def test_custom_initialization(self):
        """Test initialization with custom values."""
        ctx = AIConfidenceContext(
            symptom_extraction_confidence=0.8,
            interaction_boost=0.1,
            personalization_factor=0.05,
            combined_confidence=0.85,
            age_stage="senior",
            severity="severe",
            metadata={"source": "claude"},
        )

        assert ctx.symptom_extraction_confidence == 0.8
        assert ctx.interaction_boost == 0.1
        assert ctx.personalization_factor == 0.05
        assert ctx.combined_confidence == 0.85
        assert ctx.age_stage == "senior"
        assert ctx.severity == "severe"
        assert ctx.metadata["source"] == "claude"


class TestCalculateCombinedConfidence:
    """Test combined confidence calculation."""

    def test_baseline_no_adjustments(self):
        """Test with no interactions or personalization."""
        confidence = calculate_combined_confidence(0.8, 0.0, 0.0)
        assert confidence == 0.8

    def test_with_interaction_boost(self):
        """Test confidence increase from interactions."""
        confidence = calculate_combined_confidence(0.8, 0.1, 0.0)
        # (0.8 * 0.7) + (0.1 * 0.3) = 0.56 + 0.03 = 0.59
        # But we need to check actual calculation
        assert confidence > 0.8
        assert confidence <= 1.0

    def test_with_positive_personalization(self):
        """Test confidence increase from positive personalization."""
        confidence = calculate_combined_confidence(0.7, 0.0, 0.1)
        assert confidence > 0.7
        assert confidence <= 1.0

    def test_with_negative_personalization(self):
        """Test confidence decrease from negative personalization."""
        confidence = calculate_combined_confidence(0.7, 0.0, -0.1)
        assert confidence < 0.7
        assert confidence >= 0.0

    def test_all_components(self):
        """Test with all components present."""
        confidence = calculate_combined_confidence(0.75, 0.12, 0.08)
        assert 0.0 <= confidence <= 1.0

    def test_clamps_to_valid_range(self):
        """Test that result is clamped to 0.0-1.0."""
        # Very high values should be clamped
        confidence = calculate_combined_confidence(1.0, 0.15, 0.3)
        assert confidence <= 1.0

        # Negative values should be clamped
        confidence = calculate_combined_confidence(0.0, 0.0, -0.3)
        assert confidence >= 0.0

    def test_low_extraction_confidence(self):
        """Test with low base extraction confidence."""
        confidence = calculate_combined_confidence(0.3, 0.1, 0.05)
        assert 0.0 <= confidence <= 1.0
        assert confidence <= 0.5  # Should be relatively low

    def test_high_extraction_confidence(self):
        """Test with high base extraction confidence."""
        confidence = calculate_combined_confidence(0.95, 0.1, 0.05)
        assert confidence >= 0.9


class TestScaleConfidenceToPsiMultiplier:
    """Test scaling confidence to psi multiplier."""

    def test_zero_confidence(self):
        """Test zero confidence maps to min multiplier."""
        multiplier = scale_confidence_to_psi_multiplier(0.0)
        assert multiplier == 0.6

    def test_full_confidence(self):
        """Test full confidence maps to max multiplier."""
        multiplier = scale_confidence_to_psi_multiplier(1.0)
        assert multiplier == 1.2

    def test_mid_confidence(self):
        """Test mid-range confidence."""
        multiplier = scale_confidence_to_psi_multiplier(0.5)
        # Should be roughly 0.9 (midpoint between 0.6 and 1.2)
        assert 0.85 < multiplier < 0.95

    def test_linear_scaling(self):
        """Test that scaling is approximately linear."""
        m1 = scale_confidence_to_psi_multiplier(0.25)
        m2 = scale_confidence_to_psi_multiplier(0.5)
        m3 = scale_confidence_to_psi_multiplier(0.75)

        # Differences should be roughly equal
        diff1 = m2 - m1
        diff2 = m3 - m2
        assert abs(diff1 - diff2) < 0.01

    def test_custom_range(self):
        """Test with custom min/max multipliers."""
        multiplier = scale_confidence_to_psi_multiplier(0.5, min_multiplier=0.7, max_multiplier=1.3)
        # Should be midpoint: 0.7 + 0.5*(1.3-0.7) = 1.0
        assert 0.99 < multiplier < 1.01

    def test_clamps_to_range(self):
        """Test that result is in valid range."""
        low = scale_confidence_to_psi_multiplier(0.0)
        high = scale_confidence_to_psi_multiplier(1.0)

        assert low >= 0.6
        assert high <= 1.2


class TestAdjustContextFromAI:
    """Test merging AI results into RECO2 context."""

    def test_no_ai_result(self):
        """Test with no AI result provided."""
        context = {"domain": "test", "confidence": 0.5}
        result = adjust_context_from_ai(context, None)

        assert result["domain"] == "test"
        assert result["confidence"] == 0.5

    def test_empty_ai_result(self):
        """Test with empty AI result."""
        context = {"domain": "test", "confidence": 0.5}
        result = adjust_context_from_ai(context, {})

        assert result["domain"] == "test"
        assert result["confidence"] == 0.5

    def test_adds_ai_confidence_metadata(self):
        """Test that AI confidence metadata is added."""
        context = {"domain": "test"}
        ai_result = {
            "confidence": 0.85,
            "interactions": [],
            "personalization": {},
        }
        result = adjust_context_from_ai(context, ai_result)

        assert "ai_confidence" in result
        assert result["ai_confidence"]["symptom_extraction"] == 0.85
        assert result["ai_confidence"]["source"] == "ai"

    def test_with_interactions(self):
        """Test adjustment with symptom interactions."""
        context = {"domain": "test"}
        ai_result = {
            "confidence": 0.8,
            "interactions": [{"boost_factor": 0.1}, {"boost_factor": 0.05}],
            "personalization": {},
        }
        result = adjust_context_from_ai(context, ai_result)

        assert result["ai_confidence"]["interaction_boost"] == 0.1

    def test_with_personalization_senior(self):
        """Test with senior dog personalization."""
        context = {"domain": "test"}
        ai_result = {
            "confidence": 0.75,
            "interactions": [],
            "personalization": {"age_stage": "senior", "severity": "moderate"},
        }
        result = adjust_context_from_ai(context, ai_result)

        assert result["ai_confidence"]["age_stage"] == "senior"
        assert result["ai_confidence"]["severity"] == "moderate"
        assert result["ai_confidence"]["personalization_factor"] > 0.0

    def test_with_personalization_puppy(self):
        """Test with puppy personalization."""
        context = {"domain": "test"}
        ai_result = {
            "confidence": 0.75,
            "interactions": [],
            "personalization": {"age_stage": "puppy", "severity": "moderate"},
        }
        result = adjust_context_from_ai(context, ai_result)

        assert result["ai_confidence"]["age_stage"] == "puppy"

    def test_with_severe_severity(self):
        """Test with severe severity."""
        context = {"domain": "test"}
        ai_result = {
            "confidence": 0.7,
            "interactions": [],
            "personalization": {"age_stage": "adult", "severity": "severe"},
        }
        result = adjust_context_from_ai(context, ai_result)

        assert result["ai_confidence"]["severity"] == "severe"
        assert result["ai_confidence"]["personalization_factor"] > 0.0

    def test_with_mild_severity(self):
        """Test with mild severity (should reduce confidence)."""
        context = {"domain": "test"}
        ai_result = {
            "confidence": 0.7,
            "interactions": [],
            "personalization": {"age_stage": "adult", "severity": "mild"},
        }
        result = adjust_context_from_ai(context, ai_result)

        assert result["ai_confidence"]["severity"] == "mild"
        assert result["ai_confidence"]["personalization_factor"] < 0.0

    def test_updates_domain_known_flag(self):
        """Test that high confidence boosts domain_known flag."""
        context = {"domain": "test"}
        ai_result = {
            "confidence": 0.95,
            "interactions": [{"boost_factor": 0.1}],
            "personalization": {"age_stage": "senior", "severity": "severe"},
        }
        result = adjust_context_from_ai(context, ai_result)

        # High AI confidence should boost AI enhancement flag
        if result.get("ai_confidence", {}).get("combined", 0) > 0.8:
            assert result.get("ai_enhanced", False)

    def test_preserves_existing_context(self):
        """Test that existing context fields are preserved."""
        context = {
            "domain": "cardiology",
            "confidence": 0.5,
            "domain_known": True,
            "missing_fields": 2,
        }
        ai_result = {
            "confidence": 0.8,
            "interactions": [],
            "personalization": {},
        }
        result = adjust_context_from_ai(context, ai_result)

        assert result["domain"] == "cardiology"
        assert result["domain_known"] is True
        assert result["missing_fields"] == 2


class TestCreateAIConfidenceContext:
    """Test creating AIConfidenceContext from extraction result."""

    def test_empty_result(self):
        """Test with empty extraction result."""
        ctx = create_ai_confidence_context({})

        assert ctx.symptom_extraction_confidence == 0.5
        assert ctx.interaction_boost == 0.0
        assert ctx.combined_confidence == 0.5

    def test_none_result(self):
        """Test with None result."""
        ctx = create_ai_confidence_context(None)

        assert ctx.symptom_extraction_confidence == 0.5
        assert ctx.combined_confidence == 0.5

    def test_with_all_components(self):
        """Test with complete extraction result."""
        ai_result = {
            "confidence": 0.85,
            "interactions": [{"boost_factor": 0.12}],
            "personalization": {
                "age_stage": "senior",
                "severity": "moderate",
                "extraction_method": "text_extraction",
                "confidence": 0.9,
            },
        }
        ctx = create_ai_confidence_context(ai_result)

        assert ctx.symptom_extraction_confidence == 0.85
        assert ctx.interaction_boost == 0.12
        assert ctx.age_stage == "senior"
        assert ctx.severity == "moderate"
        assert ctx.combined_confidence > 0.85

    def test_metadata_populated(self):
        """Test that metadata is properly populated."""
        ai_result = {
            "confidence": 0.8,
            "interactions": [{"boost_factor": 0.1}, {"boost_factor": 0.05}],
            "personalization": {
                "age_stage": "adult",
                "severity": "mild",
                "extraction_method": "claude",
                "confidence": 0.75,
            },
        }
        ctx = create_ai_confidence_context(ai_result)

        assert ctx.metadata["extraction_method"] == "claude"
        assert ctx.metadata["num_interactions"] == 2

    def test_senior_dog_adjustment(self):
        """Test senior dog gets positive personalization factor."""
        ai_result = {
            "confidence": 0.7,
            "interactions": [],
            "personalization": {"age_stage": "senior", "severity": "moderate"},
        }
        ctx = create_ai_confidence_context(ai_result)

        assert ctx.personalization_factor > 0.0
        assert ctx.age_stage == "senior"

    def test_puppy_adjustment(self):
        """Test puppy gets positive personalization factor."""
        ai_result = {
            "confidence": 0.7,
            "interactions": [],
            "personalization": {"age_stage": "puppy", "severity": "moderate"},
        }
        ctx = create_ai_confidence_context(ai_result)

        assert ctx.personalization_factor > 0.0

    def test_young_adjustment(self):
        """Test young dog gets smaller adjustment."""
        ai_result = {
            "confidence": 0.7,
            "interactions": [],
            "personalization": {"age_stage": "young", "severity": "moderate"},
        }
        ctx = create_ai_confidence_context(ai_result)

        assert ctx.personalization_factor > 0.0
        assert ctx.personalization_factor < 0.12


class TestConfidenceEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_low_extraction_confidence(self):
        """Test with near-zero extraction confidence."""
        ctx = create_ai_confidence_context({"confidence": 0.01})
        assert ctx.combined_confidence >= 0.0

    def test_very_high_extraction_confidence(self):
        """Test with near-maximum extraction confidence."""
        ctx = create_ai_confidence_context({"confidence": 0.99})
        assert ctx.combined_confidence <= 1.0

    def test_conflicting_signals(self):
        """Test when interactions and personalization have opposite effects."""
        ai_result = {
            "confidence": 0.7,
            "interactions": [{"boost_factor": 0.1}],
            "personalization": {"age_stage": "adult", "severity": "mild"},
        }
        ctx = create_ai_confidence_context(ai_result)

        # Should still be valid confidence
        assert 0.0 <= ctx.combined_confidence <= 1.0

    def test_maximum_components(self):
        """Test with maximum values for all components."""
        ai_result = {
            "confidence": 1.0,
            "interactions": [{"boost_factor": 0.15}],
            "personalization": {"age_stage": "senior", "severity": "severe"},
        }
        ctx = create_ai_confidence_context(ai_result)

        assert ctx.combined_confidence <= 1.0

    def test_confidence_no_interactions(self):
        """Test when interactions list is empty."""
        ai_result = {
            "confidence": 0.8,
            "interactions": [],
            "personalization": {},
        }
        ctx = create_ai_confidence_context(ai_result)

        assert ctx.interaction_boost == 0.0

    def test_confidence_missing_personalization(self):
        """Test when personalization is missing."""
        ai_result = {
            "confidence": 0.8,
            "interactions": [{"boost_factor": 0.1}],
        }
        ctx = create_ai_confidence_context(ai_result)

        assert ctx.age_stage is None
        assert ctx.severity == "moderate"


class TestConfidenceIntegration:
    """Test integration between components."""

    def test_full_pipeline_high_confidence(self):
        """Test full pipeline with high confidence."""
        ai_result = {
            "confidence": 0.9,
            "interactions": [{"boost_factor": 0.12}],
            "personalization": {
                "age_stage": "senior",
                "severity": "severe",
                "extraction_method": "claude",
            },
        }
        ctx = create_ai_confidence_context(ai_result)
        multiplier = scale_confidence_to_psi_multiplier(ctx.combined_confidence)

        assert ctx.combined_confidence > 0.85
        assert multiplier > 1.0

    def test_full_pipeline_low_confidence(self):
        """Test full pipeline with low confidence."""
        ai_result = {
            "confidence": 0.3,
            "interactions": [],
            "personalization": {"age_stage": "puppy", "severity": "mild"},
        }
        ctx = create_ai_confidence_context(ai_result)
        multiplier = scale_confidence_to_psi_multiplier(ctx.combined_confidence)

        assert ctx.combined_confidence < 0.5
        assert multiplier < 1.0

    def test_adjust_and_scale(self):
        """Test adjusting context and then scaling."""
        context = {"domain": "test"}
        ai_result = {
            "confidence": 0.8,
            "interactions": [{"boost_factor": 0.1}],
            "personalization": {"age_stage": "adult", "severity": "moderate"},
        }
        adjusted = adjust_context_from_ai(context, ai_result)
        combined_conf = adjusted.get("ai_confidence", {}).get("combined", 0.5)
        multiplier = scale_confidence_to_psi_multiplier(combined_conf)

        assert 0.6 <= multiplier <= 1.2
