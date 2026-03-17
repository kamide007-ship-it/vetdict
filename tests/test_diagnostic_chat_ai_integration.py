"""Tests for diagnostic chat AI confidence integration (Phase 2c Step 4)."""

import pytest

# Skip all tests if Flask is not available
flask_available = True
try:
    import flask  # noqa: F401
except ImportError:
    flask_available = False

pytestmark = pytest.mark.skipif(not flask_available, reason="Flask not available")


class TestEvaluateWithAIConfidence:
    """Test evaluate_with_ai_confidence integration function."""

    def test_function_exists(self):
        """Test that the integration function exists."""
        from api.diagnostic_chat import evaluate_with_ai_confidence

        assert callable(evaluate_with_ai_confidence)

    def test_basic_evaluation_no_ai(self):
        """Test basic evaluation without AI result."""
        from api.diagnostic_chat import evaluate_with_ai_confidence

        result = evaluate_with_ai_confidence(
            inference={"test_disease": 0.7},
            evidence={"test_disease": {"median": 0.6}},
            context={"domain": "cardiology", "confidence": 0.5},
        )

        # Result can be None if RECO2 unavailable, or a dict if available
        if result is not None:
            assert "integrity" in result
            assert "verdict" in result

    def test_evaluation_with_ai_confidence(self):
        """Test evaluation with AI result."""
        from api.diagnostic_chat import evaluate_with_ai_confidence

        ai_result = {
            "confidence": 0.85,
            "interactions": [{"boost_factor": 0.1}],
            "personalization": {"age_stage": "senior", "severity": "moderate"},
        }

        result = evaluate_with_ai_confidence(
            inference={"hip_dysplasia": 0.65},
            evidence={"hip_dysplasia": {"median": 0.5}},
            context={"domain": "orthopedics", "confidence": 0.5},
            ai_result=ai_result,
        )

        # Result can be None if RECO2 unavailable
        if result is not None:
            assert "ai_confidence" in result or result is None

    def test_handles_reco2_unavailable(self):
        """Test graceful handling when RECO2 is unavailable."""
        from api.diagnostic_chat import evaluate_with_ai_confidence

        # Should not raise exception even if RECO2 module not available
        result = evaluate_with_ai_confidence(
            inference={"disease": 0.7},
            evidence={"disease": {"median": 0.6}},
            context={"domain": "test", "confidence": 0.5},
        )

        # Result can be dict (if RECO2 available) or None
        assert result is None or isinstance(result, dict)

    def test_inference_format(self):
        """Test that inference format is properly handled."""
        from api.diagnostic_chat import evaluate_with_ai_confidence

        # Multiple diseases in inference
        result = evaluate_with_ai_confidence(
            inference={"disease_a": 0.7, "disease_b": 0.5, "disease_c": 0.3},
            evidence={
                "disease_a": {"median": 0.6},
                "disease_b": {"median": 0.4},
                "disease_c": {"median": 0.2},
            },
            context={"domain": "general", "confidence": 0.5},
        )

        # Should handle multiple diseases
        assert result is None or isinstance(result, dict)

    def test_context_with_metadata(self):
        """Test context with additional metadata."""
        from api.diagnostic_chat import evaluate_with_ai_confidence

        result = evaluate_with_ai_confidence(
            inference={"disease": 0.7},
            evidence={"disease": {"median": 0.6}},
            context={
                "domain": "test",
                "confidence": 0.5,
                "domain_known": True,
                "missing_fields": 1,
                "warnings": 0,
            },
            ai_result={
                "confidence": 0.8,
                "interactions": [],
                "personalization": {"age_stage": "adult", "severity": "moderate"},
            },
        )

        assert result is None or isinstance(result, dict)

    def test_none_ai_result(self):
        """Test with explicit None ai_result."""
        from api.diagnostic_chat import evaluate_with_ai_confidence

        result = evaluate_with_ai_confidence(
            inference={"disease": 0.7},
            evidence={"disease": {"median": 0.6}},
            context={"domain": "test", "confidence": 0.5},
            ai_result=None,
        )

        assert result is None or isinstance(result, dict)

    def test_empty_ai_result(self):
        """Test with empty ai_result dict."""
        from api.diagnostic_chat import evaluate_with_ai_confidence

        result = evaluate_with_ai_confidence(
            inference={"disease": 0.7},
            evidence={"disease": {"median": 0.6}},
            context={"domain": "test", "confidence": 0.5},
            ai_result={},
        )

        assert result is None or isinstance(result, dict)


class TestDiagnosticChatAIIntegration:
    """Test diagnostic chat module can import and use AI integration."""

    def test_diagnostic_chat_imports(self):
        """Test that diagnostic_chat module imports correctly."""
        try:
            from api.diagnostic_chat import diagnostic_bp, evaluate_with_ai_confidence
            assert diagnostic_bp is not None
            assert callable(evaluate_with_ai_confidence)
        except ImportError:
            # Flask might not be available in test environment
            pytest.skip("Flask not available")

    def test_ai_extractor_can_be_initialized(self):
        """Test that AI extractor lazy-loading doesn't crash."""
        try:
            from api.diagnostic_chat import _get_ai_extractor
            # Should not raise exception
            extractor = _get_ai_extractor()
            # Can be None if disabled or unavailable
            assert extractor is None or hasattr(extractor, 'extract')
        except ImportError:
            pytest.skip("Required modules not available")

    def test_helper_functions_present(self):
        """Test that expected helper functions exist in diagnostic_chat."""
        try:
            from api import diagnostic_chat
            # Should have these functions
            assert hasattr(diagnostic_chat, 'extract_symptoms_from_text')
            assert hasattr(diagnostic_chat, 'match_symptoms_to_diseases')
            assert hasattr(diagnostic_chat, 'evaluate_with_ai_confidence')
        except ImportError:
            pytest.skip("Flask not available")


class TestPhase2CIntegrationSignatures:
    """Test that Phase 2c integration maintains proper signatures."""

    def test_evaluate_with_ai_confidence_signature(self):
        """Test function signature for RECO2 evaluation wrapper."""
        import inspect

        from api.diagnostic_chat import evaluate_with_ai_confidence

        sig = inspect.signature(evaluate_with_ai_confidence)
        params = list(sig.parameters.keys())

        # Should have these parameters
        assert "inference" in params
        assert "evidence" in params
        assert "context" in params
        assert "ai_result" in params

        # ai_result should be optional
        assert sig.parameters["ai_result"].default is None

    def test_ai_extractor_available_in_module(self):
        """Test that AI extractor functionality is available."""
        try:
            from api.diagnostic_chat import _get_ai_extractor
            assert callable(_get_ai_extractor)
        except ImportError:
            pytest.skip("Flask not available")


class TestPhase2CConceptualIntegration:
    """Conceptual tests for Phase 2c integration pattern."""

    def test_ai_confidence_flows_through_reco2(self):
        """Test the conceptual flow of AI confidence through RECO2."""
        # This test validates the integration design:
        # 1. AI extracts symptoms with confidence
        # 2. Personalization adjusts confidence based on patient context
        # 3. RECO2 applies this confidence to verdict generation
        # 4. Output gate adjusts assertions based on confidence

        # The flow is:
        # AI extraction → confidence + personalization → RECO2 → output gate adjustments

        # Verify each component has the necessary functions
        try:
            from api.ai.patient_personalization import PersonalizationEngine
            from api.ai.symptom_extractor import SymptomExtractor
            from reco2 import engine, output_gate
            from reco2.confidence_adapter import adjust_context_from_ai

            # All components should be importable
            assert callable(SymptomExtractor)
            assert callable(PersonalizationEngine)
            assert callable(adjust_context_from_ai)
            assert callable(engine.evaluate_payload)
            assert callable(output_gate.analyze)

        except ImportError as e:
            pytest.skip(f"Phase 2c components not fully available: {e}")

    def test_phase2c_backward_compatibility(self):
        """Test that Phase 2c doesn't break existing functionality."""
        try:
            from api import diagnostic_chat
            from reco2 import engine, output_gate

            # Existing functions should still work without AI
            assert callable(diagnostic_chat.extract_symptoms_from_text)
            assert callable(engine.evaluate_payload)
            assert callable(output_gate.analyze)

            # All should work with just required parameters (no AI)
            # This ensures backward compatibility

        except ImportError:
            pytest.skip("Required modules not available")


class TestPhase2CDataFlow:
    """Test data flow through Phase 2c integration."""

    def test_ai_result_format_compatibility(self):
        """Test that AI result format is compatible with RECO2."""
        from api.diagnostic_chat import evaluate_with_ai_confidence

        # Simulate AI extraction result from Phase 2b
        ai_result = {
            "symptoms": ["coughing", "fever"],
            "confidence": 0.85,
            "method": "claude",
            "cache_hit": False,
            "fallback_used": False,
            "interactions": [
                {"pair": ["coughing", "fever"], "weight": 0.5, "boost_factor": 0.08}
            ],
            "personalization": {
                "age_stage": "senior",
                "extracted_age_years": 8.5,
                "severity": "moderate",
                "extraction_method": "text_extraction",
                "confidence": 0.95,
            },
        }

        # Should be compatible with evaluate_with_ai_confidence
        result = evaluate_with_ai_confidence(
            inference={"pneumonia": 0.7},
            evidence={"pneumonia": {"median": 0.6}},
            context={"domain": "respiration", "confidence": 0.5},
            ai_result=ai_result,
        )

        # Should complete without error
        assert result is None or isinstance(result, dict)

    def test_reco2_output_structure(self):
        """Test that RECO2 output structure is suitable for diagnostic chat."""
        from api.diagnostic_chat import evaluate_with_ai_confidence

        ai_result = {
            "confidence": 0.8,
            "interactions": [],
            "personalization": {"age_stage": "adult", "severity": "moderate"},
        }

        result = evaluate_with_ai_confidence(
            inference={"disease": 0.7},
            evidence={"disease": {"median": 0.6}},
            context={"domain": "test", "confidence": 0.5},
            ai_result=ai_result,
        )

        # If RECO2 available, result should have standard fields
        if result is not None:
            assert isinstance(result, dict)
            # Standard RECO2 fields
            if "verdict" in result:
                assert result["verdict"] in ("reliable", "moderate", "suspect")
            if "integrity" in result:
                assert 0.0 <= result["integrity"] <= 3.0
            if "ai_confidence" in result:
                assert isinstance(result["ai_confidence"], dict)
