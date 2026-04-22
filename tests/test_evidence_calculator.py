"""Tests for evidence_calculator.py - Evidence-based confidence scoring."""

from api.ai.evidence_calculator import (
    EvidenceBreakdown,
    EvidenceScorer,
    build_confidence_breakdown_response,
)


class TestEvidenceBreakdown:
    def test_to_dict_keys(self):
        eb = EvidenceBreakdown(
            disease_name="Test",
            raw_symptom_score=0.7,
            evidence_level=2,
            evidence_multiplier=1.3,
            weighted_evidence_component=0.325,
            demographic_adjustment=1.0,
            weighted_demographic_component=0.15,
            final_confidence=0.65,
            calculation_notes="test",
        )
        d = eb.to_dict()
        assert d["disease_name"] == "Test"
        assert d["evidence_level"] == 2
        assert "raw_symptom_score" in d
        assert "final_confidence" in d

    def test_to_dict_rounds_floats(self):
        eb = EvidenceBreakdown(
            disease_name="X",
            raw_symptom_score=0.12345,
            evidence_level=3,
            evidence_multiplier=1.12345,
            weighted_evidence_component=0.12345,
            demographic_adjustment=1.12345,
            weighted_demographic_component=0.12345,
            final_confidence=0.12345,
        )
        d = eb.to_dict()
        assert d["raw_symptom_score"] == 0.123
        assert d["final_confidence"] == 0.123


class TestCalculateEvidenceScore:
    def test_returns_tuple(self):
        score, breakdown = EvidenceScorer.calculate_evidence_score("Test Disease", 0.7)
        assert isinstance(score, float)
        assert isinstance(breakdown, EvidenceBreakdown)

    def test_score_in_valid_range(self):
        score, _ = EvidenceScorer.calculate_evidence_score("Test", 0.5)
        assert 0.0 <= score <= 1.0

    def test_higher_raw_score_higher_final(self):
        score_low, _ = EvidenceScorer.calculate_evidence_score("Test", 0.2)
        score_high, _ = EvidenceScorer.calculate_evidence_score("Test", 0.8)
        assert score_high > score_low

    def test_demographic_adjustment_affects_score(self):
        score_normal, _ = EvidenceScorer.calculate_evidence_score("Test", 0.5, 1.0)
        score_high, _ = EvidenceScorer.calculate_evidence_score("Test", 0.5, 1.5)
        assert score_high > score_normal

    def test_use_evidence_false(self):
        score, breakdown = EvidenceScorer.calculate_evidence_score(
            "Test",
            0.5,
            use_evidence=False,
        )
        assert breakdown.evidence_level == 4
        assert breakdown.evidence_multiplier == 1.0

    def test_clamps_raw_score(self):
        score, _ = EvidenceScorer.calculate_evidence_score("Test", 1.5)
        assert score <= 1.0
        score2, _ = EvidenceScorer.calculate_evidence_score("Test", -0.5)
        assert score2 >= 0.0

    def test_zero_raw_score(self):
        score, _ = EvidenceScorer.calculate_evidence_score("Test", 0.0)
        assert score >= 0.0

    def test_breakdown_disease_name(self):
        _, breakdown = EvidenceScorer.calculate_evidence_score("Pancreatitis", 0.6)
        assert breakdown.disease_name == "Pancreatitis"


class TestBuildNotes:
    def test_level_1_description(self):
        notes = EvidenceScorer._build_notes(1, 1.4, 1.0)
        assert "RCT" in notes
        assert "strongest" in notes

    def test_level_4_description(self):
        notes = EvidenceScorer._build_notes(4, 1.0, 1.0)
        assert "Clinical observation" in notes

    def test_boosted_evidence(self):
        notes = EvidenceScorer._build_notes(2, 1.3, 1.0)
        assert "boosted" in notes

    def test_no_boost_evidence(self):
        notes = EvidenceScorer._build_notes(4, 1.0, 1.0)
        assert "no boost" in notes

    def test_reduced_demographic(self):
        notes = EvidenceScorer._build_notes(3, 1.0, 0.8)
        assert "reduced" in notes

    def test_enhanced_demographic(self):
        notes = EvidenceScorer._build_notes(3, 1.0, 1.2)
        assert "enhanced" in notes

    def test_neutral_demographic(self):
        notes = EvidenceScorer._build_notes(3, 1.0, 1.0)
        assert "neutral" in notes


class TestScoreMultipleDiseases:
    def test_returns_list(self):
        diseases = [
            {"name": "Disease A", "match_percent": 70},
            {"name": "Disease B", "match_percent": 50},
        ]
        result = EvidenceScorer.score_multiple_diseases(diseases)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_result_has_breakdown(self):
        diseases = [{"name": "Test", "match_percent": 60}]
        result = EvidenceScorer.score_multiple_diseases(diseases)
        assert "confidence_breakdown" in result[0]
        assert "confidence_before_evidence" in result[0]

    def test_sorted_descending(self):
        diseases = [
            {"name": "Low", "match_percent": 30},
            {"name": "High", "match_percent": 90},
        ]
        result = EvidenceScorer.score_multiple_diseases(diseases)
        assert result[0]["match_percent"] >= result[1]["match_percent"]

    def test_with_demographic_adjustments(self):
        diseases = [{"name": "Test", "match_percent": 50}]
        adjustments = {"Test": 1.3}
        result = EvidenceScorer.score_multiple_diseases(
            diseases,
            demographic_adjustments=adjustments,
        )
        assert len(result) == 1

    def test_without_evidence(self):
        diseases = [{"name": "Test", "match_percent": 50}]
        result = EvidenceScorer.score_multiple_diseases(diseases, use_evidence=False)
        assert len(result) == 1


class TestApplyEvidenceAdjustment:
    def test_returns_dict(self):
        disease = {"name": "Test", "match_percent": 70}
        result = EvidenceScorer.apply_evidence_adjustment(disease)
        assert isinstance(result, dict)
        assert "confidence_breakdown" in result

    def test_preserves_original_keys(self):
        disease = {"name": "Test", "match_percent": 70, "custom_key": "value"}
        result = EvidenceScorer.apply_evidence_adjustment(disease)
        assert result["custom_key"] == "value"

    def test_stores_original_confidence(self):
        disease = {"name": "Test", "match_percent": 70}
        result = EvidenceScorer.apply_evidence_adjustment(disease)
        assert result["confidence_before_evidence"] == 70


class TestBuildConfidenceBreakdownResponse:
    def test_returns_dict(self):
        result = build_confidence_breakdown_response("Test Disease", 0.7)
        assert isinstance(result, dict)

    def test_has_expected_keys(self):
        result = build_confidence_breakdown_response("Test", 0.5)
        assert "disease" in result
        assert "final_confidence" in result
        assert "final_confidence_percent" in result
        assert "breakdown" in result
        assert "formula_explanation" in result

    def test_disease_name_correct(self):
        result = build_confidence_breakdown_response("Pancreatitis", 0.6)
        assert result["disease"] == "Pancreatitis"

    def test_with_demographic_adjustment(self):
        result = build_confidence_breakdown_response("Test", 0.5, 1.3)
        assert result["final_confidence"] > 0
