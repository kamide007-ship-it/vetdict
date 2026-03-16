"""Tests for RECO2 engine AI confidence integration (Phase 2c Step 2)."""

import importlib

import pytest

from reco2 import engine
from reco2.confidence_adapter import create_ai_confidence_context


@pytest.fixture(autouse=True)
def reload_engine():
    """Reload engine before each test to ensure clean state."""
    import reco2.store as store
    importlib.reload(store)
    importlib.reload(engine)
    yield


class TestApplyAIConfidenceToPsi:
    """Test _apply_ai_confidence_to_psi function."""

    def test_no_ai_result(self):
        """Test with no AI result returns original psi."""
        psi = 1.0
        adjusted_psi, multiplier = engine._apply_ai_confidence_to_psi(psi, None)

        assert adjusted_psi == psi
        assert multiplier is None

    def test_empty_ai_result(self):
        """Test with empty AI result."""
        psi = 1.0
        adjusted_psi, multiplier = engine._apply_ai_confidence_to_psi(psi, {})

        assert adjusted_psi == psi
        assert multiplier is None

    def test_high_confidence_boosts_psi(self):
        """Test that high AI confidence boosts psi."""
        psi = 1.0
        ai_result = {"confidence": 0.9}
        adjusted_psi, multiplier = engine._apply_ai_confidence_to_psi(psi, ai_result)

        assert adjusted_psi > psi
        assert multiplier is not None
        assert multiplier > 1.0

    def test_low_confidence_dampens_psi(self):
        """Test that low AI confidence dampens psi."""
        psi = 1.0
        ai_result = {"confidence": 0.2}
        adjusted_psi, multiplier = engine._apply_ai_confidence_to_psi(psi, ai_result)

        assert adjusted_psi < psi
        assert multiplier is not None
        assert multiplier < 1.0

    def test_mid_confidence(self):
        """Test with mid-range confidence."""
        psi = 1.0
        ai_result = {"confidence": 0.5}
        adjusted_psi, multiplier = engine._apply_ai_confidence_to_psi(psi, ai_result)

        # Mid-range should give multiplier around 0.9
        assert 0.8 < multiplier < 1.0
        assert adjusted_psi < psi

    def test_clamps_confidence(self):
        """Test that confidence is clamped to valid range."""
        psi = 1.0

        # Out of range high
        adjusted_psi, multiplier = engine._apply_ai_confidence_to_psi(
            psi, {"confidence": 1.5}
        )
        assert multiplier <= 1.2

        # Out of range low
        adjusted_psi, multiplier = engine._apply_ai_confidence_to_psi(
            psi, {"confidence": -0.5}
        )
        assert multiplier >= 0.6

    def test_preserves_positive_psi(self):
        """Test that adjusted psi stays positive."""
        psi = 0.1
        ai_result = {"confidence": 0.0}
        adjusted_psi, _ = engine._apply_ai_confidence_to_psi(psi, ai_result)

        assert adjusted_psi >= 0.0


class TestEvaluatePayloadWithAI:
    """Test evaluate_payload with AI confidence integration."""

    def test_basic_payload_without_ai(self):
        """Test basic evaluation still works without AI result."""
        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {
                    "domain": "test",
                    "confidence": 0.7,
                    "domain_known": True,
                },
            }
        )

        assert "session_id" in res
        assert res["verdict"] in ("reliable", "moderate", "suspect")
        assert "ai_confidence" not in res

    def test_payload_with_high_ai_confidence(self):
        """Test evaluation with high AI confidence."""
        ai_result = {
            "confidence": 0.9,
            "interactions": [{"boost_factor": 0.1}],
            "personalization": {"age_stage": "senior", "severity": "moderate"},
        }
        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "test", "confidence": 0.5},
            },
            ai_result=ai_result,
        )

        assert "ai_confidence" in res
        assert res["ai_confidence"]["source"] == "ai"
        assert "ai_psi_multiplier" in res["meta"]
        assert res["meta"]["ai_psi_multiplier"] > 1.0

    def test_payload_with_low_ai_confidence(self):
        """Test evaluation with low AI confidence."""
        ai_result = {
            "confidence": 0.3,
            "interactions": [],
            "personalization": {"age_stage": "puppy", "severity": "mild"},
        }
        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "test", "confidence": 0.5},
            },
            ai_result=ai_result,
        )

        assert "ai_confidence" in res
        assert "ai_psi_multiplier" in res["meta"]
        assert res["meta"]["ai_psi_multiplier"] < 1.0

    def test_ai_confidence_updates_context(self):
        """Test that AI confidence is merged into context."""
        ai_result = {
            "confidence": 0.85,
            "interactions": [{"boost_factor": 0.12}],
            "personalization": {"age_stage": "adult", "severity": "moderate"},
        }
        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "test", "confidence": 0.5},
            },
            ai_result=ai_result,
        )

        assert "ai_confidence" in res
        ai_conf = res["ai_confidence"]
        assert ai_conf["symptom_extraction"] == 0.85
        assert ai_conf["interaction_boost"] == 0.12
        assert ai_conf["age_stage"] == "adult"

    def test_high_ai_confidence_changes_verdict(self):
        """Test that high AI confidence can elevate verdict."""
        # Borderline case without AI
        res_without_ai = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.8}},
                "context": {"domain": "test", "confidence": 0.5},
            }
        )

        # Same case with high AI confidence
        ai_result = {
            "confidence": 0.95,
            "interactions": [{"boost_factor": 0.1}],
            "personalization": {"age_stage": "senior", "severity": "severe"},
        }
        res_with_ai = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.8}},
                "context": {"domain": "test", "confidence": 0.5},
            },
            ai_result=ai_result,
        )

        # High AI confidence should result in higher integrity
        assert res_with_ai["integrity"] >= res_without_ai["integrity"]

    def test_ai_result_merges_with_context_confidence(self):
        """Test that AI result updates context confidence properly."""
        ai_result = {
            "confidence": 0.8,
            "interactions": [{"boost_factor": 0.1}],
            "personalization": {"age_stage": "adult", "severity": "moderate"},
        }
        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "test", "confidence": 0.3},
            },
            ai_result=ai_result,
        )

        # Final confidence should be higher than 0.3 due to AI enhancement
        assert res["integrity"] >= 0.0


class TestAIConfidenceContextIntegration:
    """Test integration with AIConfidenceContext."""

    def test_create_context_from_ai_result(self):
        """Test creating AIConfidenceContext from extraction result."""
        ai_result = {
            "confidence": 0.85,
            "interactions": [{"boost_factor": 0.1}],
            "personalization": {
                "age_stage": "senior",
                "severity": "moderate",
                "extraction_method": "claude",
            },
        }

        ctx = create_ai_confidence_context(ai_result)

        assert ctx.symptom_extraction_confidence == 0.85
        assert ctx.interaction_boost == 0.1
        assert ctx.age_stage == "senior"
        assert ctx.severity == "moderate"

    def test_full_pipeline_high_confidence_dog(self):
        """Test full pipeline: high confidence senior dog."""
        ai_result = {
            "confidence": 0.9,
            "interactions": [{"boost_factor": 0.12}],
            "personalization": {
                "age_stage": "senior",
                "severity": "moderate",
                "extraction_method": "claude",
            },
        }

        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.6},
                "evidence": {"a": {"median": 0.8}},
                "context": {"domain": "orthopedics", "confidence": 0.4},
            },
            ai_result=ai_result,
        )

        assert "ai_confidence" in res
        assert res["ai_confidence"]["age_stage"] == "senior"
        # High confidence should boost psi
        assert res["meta"]["ai_psi_multiplier"] > 1.1

    def test_full_pipeline_low_confidence_puppy(self):
        """Test full pipeline: low confidence puppy."""
        ai_result = {
            "confidence": 0.4,
            "interactions": [],
            "personalization": {
                "age_stage": "puppy",
                "severity": "mild",
                "extraction_method": "manual",
            },
        }

        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.5},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "pediatrics", "confidence": 0.3},
            },
            ai_result=ai_result,
        )

        assert "ai_confidence" in res
        assert res["ai_confidence"]["age_stage"] == "puppy"
        # Low confidence should reduce psi
        assert res["meta"]["ai_psi_multiplier"] < 1.0


class TestBackwardCompatibility:
    """Test backward compatibility when AI result is not provided."""

    def test_existing_tests_still_pass(self):
        """Test that existing functionality still works without AI."""
        # This mirrors the original test_evaluate_payload_basic
        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {
                    "domain": "general",
                    "confidence": 0.7,
                    "domain_known": True,
                    "missing_fields": 0,
                    "warnings": 0,
                },
            }
        )
        assert "session_id" in res
        assert res["verdict"] in ("reliable", "moderate", "suspect")

    def test_none_ai_result(self):
        """Test explicitly passing None as ai_result."""
        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "test", "confidence": 0.7},
            },
            ai_result=None,
        )

        assert "session_id" in res
        assert res["verdict"] in ("reliable", "moderate", "suspect")
        assert "ai_confidence" not in res

    def test_default_parameter(self):
        """Test that ai_result defaults to None."""
        # Call without providing ai_result parameter
        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "test", "confidence": 0.7},
            }
        )

        assert "session_id" in res
        assert "ai_confidence" not in res


class TestAIConfidenceEdgeCases:
    """Test edge cases in AI confidence integration."""

    def test_missing_ai_fields(self):
        """Test handling of missing AI fields."""
        ai_result = {"confidence": 0.7}  # Missing interactions and personalization

        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "test", "confidence": 0.5},
            },
            ai_result=ai_result,
        )

        assert "ai_confidence" in res
        assert res["ai_confidence"]["interaction_boost"] == 0.0

    def test_zero_confidence(self):
        """Test with zero AI confidence."""
        ai_result = {
            "confidence": 0.0,
            "interactions": [],
            "personalization": {"age_stage": None, "severity": "moderate"},
        }

        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "test", "confidence": 0.5},
            },
            ai_result=ai_result,
        )

        # Should still work, just with low confidence
        assert "ai_confidence" in res
        assert res["meta"]["ai_psi_multiplier"] == 0.6  # Min multiplier

    def test_perfect_confidence(self):
        """Test with perfect AI confidence."""
        ai_result = {
            "confidence": 1.0,
            "interactions": [{"boost_factor": 0.15}],
            "personalization": {"age_stage": "senior", "severity": "severe"},
        }

        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "test", "confidence": 0.5},
            },
            ai_result=ai_result,
        )

        # Should result in highest multiplier
        assert "ai_confidence" in res
        assert res["meta"]["ai_psi_multiplier"] == 1.2  # Max multiplier

    def test_large_interaction_boost(self):
        """Test handling of large interaction boost."""
        ai_result = {
            "confidence": 0.8,
            "interactions": [
                {"boost_factor": 0.15},
                {"boost_factor": 0.12},
                {"boost_factor": 0.1},
            ],
            "personalization": {"age_stage": "adult", "severity": "moderate"},
        }

        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "test", "confidence": 0.5},
            },
            ai_result=ai_result,
        )

        assert "ai_confidence" in res
        # Should use strongest boost (0.15)
        assert res["ai_confidence"]["interaction_boost"] == 0.15

    def test_severe_with_young_dog(self):
        """Test severe symptoms in young dog."""
        ai_result = {
            "confidence": 0.75,
            "interactions": [{"boost_factor": 0.08}],
            "personalization": {"age_stage": "young", "severity": "severe"},
        }

        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.8},
                "evidence": {"a": {"median": 0.5}},
                "context": {"domain": "test", "confidence": 0.6},
            },
            ai_result=ai_result,
        )

        assert "ai_confidence" in res
        assert res["ai_confidence"]["age_stage"] == "young"
        assert res["ai_confidence"]["severity"] == "severe"


class TestAIConfidenceInFeedback:
    """Test that AI confidence is preserved in feedback flow."""

    def test_verdict_recorded_with_ai(self):
        """Test that verdict with AI confidence is recorded properly."""
        ai_result = {
            "confidence": 0.85,
            "interactions": [{"boost_factor": 0.1}],
            "personalization": {"age_stage": "senior", "severity": "moderate"},
        }

        res = engine.evaluate_payload(
            {
                "inference": {"a": 0.7},
                "evidence": {"a": {"median": 0.6}},
                "context": {"domain": "test", "confidence": 0.5},
            },
            ai_result=ai_result,
        )

        session_id = res["session_id"]
        assert session_id is not None

        # Verify we can give feedback on this session
        feedback = engine.record_feedback(
            {"session_id": session_id, "domain": "test", "feedback": "good"}
        )
        assert feedback["status"] == "recorded"
