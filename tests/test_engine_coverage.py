"""Comprehensive tests for reco2/engine.py."""

import math

import pytest

from reco2.engine import (
    _alpha,
    _apply_ai_confidence_to_psi,
    _beta,
    _confidence_adjusted,
    _context_match_score,
    _euclidean_distance,
    _integrity,
    _purity,
    _temperature,
    _verdict_from_psi,
    evaluate_payload,
    get_logs,
    get_status,
    patrol,
    record_feedback,
)


# ---------------------------------------------------------------------------
# Helper: _euclidean_distance
# ---------------------------------------------------------------------------

class TestEuclideanDistance:
    def test_matching_keys(self):
        I = {"a": 1.0, "b": 2.0}
        P = {"a": {"median": 1.0}, "b": {"median": 2.0}}
        assert _euclidean_distance(I, P) == pytest.approx(0.0)

    def test_matching_keys_with_difference(self):
        I = {"a": 3.0, "b": 0.0}
        P = {"a": {"median": 0.0}, "b": {"median": 4.0}}
        # sqrt(9 + 16) = 5.0
        assert _euclidean_distance(I, P) == pytest.approx(5.0)

    def test_no_matching_keys_uses_union(self):
        I = {"x": 3.0}
        P = {"y": {"median": 4.0}}
        # No intersection -> union {"x", "y"}
        # x: I=3.0, P missing -> median=0.0 -> diff=3.0
        # y: I missing -> 0.0, P median=4.0 -> diff=-4.0
        # sqrt(9 + 16) = 5.0
        assert _euclidean_distance(I, P) == pytest.approx(5.0)

    def test_empty_dicts(self):
        # Both empty -> union is empty -> no keys -> distance 0
        assert _euclidean_distance({}, {}) == pytest.approx(0.0)

    def test_empty_inference_nonempty_evidence(self):
        I = {}
        P = {"a": {"median": 5.0}}
        # No intersection -> union {"a"}
        # I missing -> 0.0, median=5.0 -> diff=-5.0
        assert _euclidean_distance(I, P) == pytest.approx(5.0)

    def test_evidence_value_not_dict(self):
        I = {"a": 2.0}
        P = {"a": "not_a_dict"}
        # e is not a dict -> m = 0.0
        assert _euclidean_distance(I, P) == pytest.approx(2.0)

    def test_partial_overlap(self):
        I = {"a": 1.0, "b": 2.0}
        P = {"a": {"median": 0.0}}
        # Intersection is {"a"} -> only "a" used
        # diff = 1.0 - 0.0 = 1.0
        assert _euclidean_distance(I, P) == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Helper: _context_match_score
# ---------------------------------------------------------------------------

class TestContextMatchScore:
    def test_high_confidence_domain_known(self):
        ctx = {"confidence": 0.9, "domain_known": True}
        # 0.9 + 0.1 = 1.0 (capped)
        assert _context_match_score(ctx) == pytest.approx(1.0)

    def test_low_confidence(self):
        ctx = {"confidence": 0.1}
        assert _context_match_score(ctx) == pytest.approx(0.1)

    def test_domain_known_bonus(self):
        ctx = {"confidence": 0.5, "domain_known": True}
        # 0.5 + 0.1 = 0.6
        assert _context_match_score(ctx) == pytest.approx(0.6)

    def test_missing_fields_penalty(self):
        ctx = {"confidence": 0.5, "missing_fields": 3}
        # 0.5 - 0.09 = 0.41
        assert _context_match_score(ctx) == pytest.approx(0.41)

    def test_warnings_penalty(self):
        ctx = {"confidence": 0.5, "warnings": 2}
        # 0.5 - 0.08 = 0.42
        assert _context_match_score(ctx) == pytest.approx(0.42)

    def test_combined_penalties(self):
        ctx = {"confidence": 0.8, "domain_known": True, "missing_fields": 2, "warnings": 1}
        # 0.8 + 0.1 - 0.06 - 0.04 = 0.8
        assert _context_match_score(ctx) == pytest.approx(0.8)

    def test_clamp_to_zero(self):
        ctx = {"confidence": 0.0, "missing_fields": 10, "warnings": 10}
        assert _context_match_score(ctx) == pytest.approx(0.0)

    def test_clamp_to_one(self):
        ctx = {"confidence": 1.0, "domain_known": True}
        # 1.0 + 0.1 capped at 1.0
        assert _context_match_score(ctx) == pytest.approx(1.0)

    def test_confidence_above_one_clamped(self):
        ctx = {"confidence": 1.5}
        # confidence clamped to 1.0
        assert _context_match_score(ctx) == pytest.approx(1.0)

    def test_confidence_below_zero_clamped(self):
        ctx = {"confidence": -0.5}
        assert _context_match_score(ctx) == pytest.approx(0.0)

    def test_empty_context(self):
        assert _context_match_score({}) == pytest.approx(0.0)

    def test_none_missing_fields(self):
        ctx = {"confidence": 0.5, "missing_fields": None}
        assert _context_match_score(ctx) == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# Helper: _purity
# ---------------------------------------------------------------------------

class TestPurity:
    def test_domain_known(self):
        ctx = {"confidence": 0.8, "domain_known": True}
        # cms = 0.8 + 0.1 = 0.9, domain_known -> no scaling
        assert _purity(ctx) == pytest.approx(0.9)

    def test_domain_not_known(self):
        ctx = {"confidence": 0.8, "domain_known": False}
        # cms = 0.8, not domain_known -> 0.8 * 0.9 = 0.72
        assert _purity(ctx) == pytest.approx(0.72)

    def test_domain_not_known_default(self):
        ctx = {"confidence": 0.5}
        # cms = 0.5, domain_known defaults False -> 0.5 * 0.9 = 0.45
        assert _purity(ctx) == pytest.approx(0.45)

    def test_high_value_clamped(self):
        ctx = {"confidence": 1.0, "domain_known": True}
        # cms = 1.0 (capped), domain_known -> 1.0
        assert _purity(ctx) == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Helper: _alpha
# ---------------------------------------------------------------------------

class TestAlpha:
    def test_zero(self):
        assert _alpha(0.0) == pytest.approx(1.0)

    def test_one(self):
        assert _alpha(1.0) == pytest.approx(1.2)

    def test_half(self):
        assert _alpha(0.5) == pytest.approx(1.1)


# ---------------------------------------------------------------------------
# Helper: _beta
# ---------------------------------------------------------------------------

class TestBeta:
    def test_above_threshold(self):
        assert _beta(0.81) == pytest.approx(1.0)

    def test_at_threshold(self):
        # purity == 0.8 is NOT > 0.8, so max(0.5, 0.8) = 0.8
        assert _beta(0.8) == pytest.approx(0.8)

    def test_below_threshold(self):
        assert _beta(0.6) == pytest.approx(0.6)

    def test_very_low_clamped(self):
        assert _beta(0.3) == pytest.approx(0.5)

    def test_zero(self):
        assert _beta(0.0) == pytest.approx(0.5)

    def test_one(self):
        assert _beta(1.0) == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Helper: _temperature
# ---------------------------------------------------------------------------

class TestTemperature:
    def test_zero_distance(self):
        # T_base * exp(0) = T_base
        assert _temperature(0.8, 1.5, 0.0) == pytest.approx(0.8)

    def test_small_distance(self):
        expected = 0.8 * math.exp(-1.5 * 0.1)
        assert _temperature(0.8, 1.5, 0.1) == pytest.approx(expected)

    def test_large_distance_hits_minimum(self):
        # Very large D -> exp(-k*D) ~ 0 -> clamped to 0.1
        assert _temperature(0.8, 1.5, 100.0) == pytest.approx(0.1)

    def test_minimum_floor(self):
        result = _temperature(0.8, 5.0, 10.0)
        assert result == pytest.approx(0.1)

    def test_high_t_base(self):
        assert _temperature(2.0, 0.0, 5.0) == pytest.approx(2.0)

    def test_zero_k(self):
        # exp(0) = 1 -> T = T_base
        assert _temperature(0.5, 0.0, 10.0) == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# Helper: _integrity
# ---------------------------------------------------------------------------

class TestIntegrity:
    def test_basic(self):
        # (1/0.5) * 1.2 * 1.0 = 2.4
        assert _integrity(0.5, 1.2, 1.0) == pytest.approx(2.4)

    def test_low_temperature(self):
        # (1/0.1) * 1.0 * 1.0 = 10.0
        assert _integrity(0.1, 1.0, 1.0) == pytest.approx(10.0)

    def test_all_ones(self):
        # (1/1.0) * 1.0 * 1.0 = 1.0
        assert _integrity(1.0, 1.0, 1.0) == pytest.approx(1.0)

    def test_combined(self):
        # (1/0.8) * 1.1 * 0.7 = 0.9625
        assert _integrity(0.8, 1.1, 0.7) == pytest.approx(0.9625)


# ---------------------------------------------------------------------------
# Helper: _verdict_from_psi
# ---------------------------------------------------------------------------

class TestVerdictFromPsi:
    def test_reliable(self):
        verdict, ja = _verdict_from_psi(1.2)
        assert verdict == "reliable"

    def test_reliable_high(self):
        verdict, ja = _verdict_from_psi(5.0)
        assert verdict == "reliable"

    def test_moderate(self):
        verdict, ja = _verdict_from_psi(0.8)
        assert verdict == "moderate"

    def test_moderate_mid(self):
        verdict, ja = _verdict_from_psi(1.0)
        assert verdict == "moderate"

    def test_suspect(self):
        verdict, ja = _verdict_from_psi(0.79)
        assert verdict == "suspect"

    def test_suspect_zero(self):
        verdict, ja = _verdict_from_psi(0.0)
        assert verdict == "suspect"

    def test_boundary_1_19(self):
        verdict, _ = _verdict_from_psi(1.19)
        assert verdict == "moderate"

    def test_boundary_1_2(self):
        verdict, _ = _verdict_from_psi(1.2)
        assert verdict == "reliable"

    def test_japanese_labels(self):
        _, ja = _verdict_from_psi(1.5)
        assert ja == "信頼できる"
        _, ja = _verdict_from_psi(1.0)
        assert ja == "ふつう"
        _, ja = _verdict_from_psi(0.5)
        assert ja == "あやしい"


# ---------------------------------------------------------------------------
# Helper: _confidence_adjusted
# ---------------------------------------------------------------------------

class TestConfidenceAdjusted:
    def test_high_psi_boosts(self):
        # psi=1.2 -> factor = max(0.6, min(1.25, 1.2/1.2)) = 1.0
        result = _confidence_adjusted(0.8, 1.2)
        assert result == pytest.approx(0.8)

    def test_low_psi_dampens(self):
        # psi=0.6 -> factor = max(0.6, min(1.25, 0.6/1.2)) = max(0.6, 0.5) = 0.6
        result = _confidence_adjusted(0.8, 0.6)
        assert result == pytest.approx(0.48)

    def test_very_high_psi(self):
        # psi=3.0 -> factor = min(1.25, 3.0/1.2) = 1.25
        result = _confidence_adjusted(0.8, 3.0)
        assert result == pytest.approx(1.0)  # clamped to 1.0

    def test_zero_base(self):
        result = _confidence_adjusted(0.0, 1.5)
        assert result == pytest.approx(0.0)

    def test_base_clamped(self):
        result = _confidence_adjusted(1.5, 1.2)
        # base clamped to 1.0, factor=1.0 -> 1.0
        assert result == pytest.approx(1.0)

    def test_negative_base_clamped(self):
        result = _confidence_adjusted(-0.5, 1.2)
        assert result == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Helper: _apply_ai_confidence_to_psi
# ---------------------------------------------------------------------------

class TestApplyAiConfidenceToPsi:
    def test_no_ai_result(self):
        psi, mult = _apply_ai_confidence_to_psi(1.0, None)
        assert psi == pytest.approx(1.0)
        assert mult is None

    def test_empty_dict(self):
        psi, mult = _apply_ai_confidence_to_psi(1.0, {})
        # Empty dict is falsy check: `not ai_result` -> True for empty dict
        # Actually {} is falsy in `not {}` -> True? No, `not {}` is True.
        # Wait: bool({}) is False, so `not {}` is True -> returns original
        psi2, mult2 = _apply_ai_confidence_to_psi(1.0, {})
        assert psi2 == pytest.approx(1.0)
        assert mult2 is None

    def test_not_a_dict(self):
        psi, mult = _apply_ai_confidence_to_psi(1.0, "string")
        assert psi == pytest.approx(1.0)
        assert mult is None

    def test_with_ai_result(self):
        ai = {"confidence": 0.5}
        psi, mult = _apply_ai_confidence_to_psi(1.0, ai)
        # confidence=0.5 -> multiplier = 0.6 + 0.5*0.6 = 0.9
        assert mult == pytest.approx(0.9)
        assert psi == pytest.approx(0.9)

    def test_high_confidence(self):
        ai = {"confidence": 1.0}
        psi, mult = _apply_ai_confidence_to_psi(2.0, ai)
        # multiplier = 0.6 + 1.0*0.6 = 1.2
        assert mult == pytest.approx(1.2)
        assert psi == pytest.approx(2.4)

    def test_zero_confidence(self):
        ai = {"confidence": 0.0}
        psi, mult = _apply_ai_confidence_to_psi(1.0, ai)
        # multiplier = 0.6
        assert mult == pytest.approx(0.6)
        assert psi == pytest.approx(0.6)

    def test_clamped_confidence(self):
        ai = {"confidence": 2.0}
        psi, mult = _apply_ai_confidence_to_psi(1.0, ai)
        # confidence clamped to 1.0 -> multiplier = 1.2
        assert mult == pytest.approx(1.2)


# ---------------------------------------------------------------------------
# Public: evaluate_payload
# ---------------------------------------------------------------------------

def _make_payload(confidence=0.8, domain_known=True, domain="cardiology"):
    return {
        "inference": {"a": 1.0, "b": 2.0},
        "evidence": {"a": {"median": 1.0}, "b": {"median": 2.0}},
        "context": {
            "confidence": confidence,
            "domain_known": domain_known,
            "domain": domain,
        },
    }


class TestEvaluatePayload:
    def test_valid_payload(self, temp_instance):
        result = evaluate_payload(_make_payload())
        assert "session_id" in result
        assert "deviation" in result
        assert "temperature" in result
        assert "integrity" in result
        assert "verdict" in result
        assert result["verdict"] in ("reliable", "moderate", "suspect")
        assert "meta" in result
        assert "context_match_score" in result["meta"]
        assert "purity" in result["meta"]

    def test_zero_distance_reliable(self, temp_instance):
        payload = _make_payload(confidence=0.9, domain_known=True)
        result = evaluate_payload(payload)
        # Zero distance -> T=T_base=0.8, high cms -> likely reliable
        assert result["deviation"] == pytest.approx(0.0)
        assert result["verdict"] in ("reliable", "moderate")

    def test_invalid_type_raises(self, temp_instance):
        with pytest.raises(ValueError, match="Invalid JSON"):
            evaluate_payload("not a dict")

    def test_invalid_payload_types(self, temp_instance):
        with pytest.raises(ValueError, match="Invalid payload types"):
            evaluate_payload({"inference": "bad", "evidence": {}, "context": {}})

    def test_missing_domain(self, temp_instance):
        payload = {
            "inference": {"a": 1.0},
            "evidence": {"a": {"median": 1.0}},
            "context": {"confidence": 0.5},
        }
        with pytest.raises(ValueError, match="context.domain is required"):
            evaluate_payload(payload)

    def test_empty_domain_string(self, temp_instance):
        payload = {
            "inference": {"a": 1.0},
            "evidence": {"a": {"median": 1.0}},
            "context": {"confidence": 0.5, "domain": "  "},
        }
        with pytest.raises(ValueError, match="context.domain is required"):
            evaluate_payload(payload)

    def test_with_ai_result(self, temp_instance):
        payload = _make_payload()
        ai_result = {"confidence": 0.9}
        result = evaluate_payload(payload, ai_result=ai_result)
        assert "session_id" in result

    def test_result_meta_fields(self, temp_instance):
        result = evaluate_payload(_make_payload())
        meta = result["meta"]
        assert "k" in meta
        assert "eta" in meta
        assert "total_sessions" in meta
        assert "domain_weight" in meta
        assert "alpha" in meta
        assert "beta" in meta

    def test_increments_total_sessions(self, temp_instance):
        r1 = evaluate_payload(_make_payload())
        r2 = evaluate_payload(_make_payload())
        assert r2["meta"]["total_sessions"] == r1["meta"]["total_sessions"] + 1

    def test_confidence_adjusted_in_result(self, temp_instance):
        result = evaluate_payload(_make_payload())
        assert 0.0 <= result["confidence_adjusted"] <= 1.0


# ---------------------------------------------------------------------------
# Public: record_feedback
# ---------------------------------------------------------------------------

class TestRecordFeedback:
    def test_valid_good_feedback(self, temp_instance):
        r = evaluate_payload(_make_payload())
        result = record_feedback({
            "session_id": r["session_id"],
            "domain": "cardiology",
            "feedback": "good",
        })
        assert result["status"] == "recorded"
        assert result["reward"] == 1.0

    def test_valid_bad_feedback(self, temp_instance):
        r = evaluate_payload(_make_payload())
        result = record_feedback({
            "session_id": r["session_id"],
            "domain": "cardiology",
            "feedback": "bad",
        })
        assert result["status"] == "recorded"
        assert result["reward"] == -1.0

    def test_valid_recalculate_feedback(self, temp_instance):
        r = evaluate_payload(_make_payload())
        result = record_feedback({
            "session_id": r["session_id"],
            "domain": "cardiology",
            "feedback": "recalculate",
        })
        assert result["status"] == "recorded"
        assert result["reward"] == pytest.approx(0.3)

    def test_duplicate_ignored(self, temp_instance):
        r = evaluate_payload(_make_payload())
        sid = r["session_id"]
        record_feedback({"session_id": sid, "domain": "cardiology", "feedback": "good"})
        result = record_feedback({"session_id": sid, "domain": "cardiology", "feedback": "bad"})
        assert result["status"] == "duplicate_ignored"

    def test_invalid_feedback_type(self, temp_instance):
        result = record_feedback({
            "session_id": "abc",
            "domain": "cardiology",
            "feedback": "invalid_value",
        })
        assert result == ({"error": "invalid_feedback"}, 400)

    def test_missing_session_id(self, temp_instance):
        result = record_feedback({"domain": "cardiology", "feedback": "good"})
        assert result == ({"error": "session_id_required"}, 400)

    def test_missing_domain(self, temp_instance):
        result = record_feedback({"session_id": "abc", "feedback": "good"})
        assert result == ({"error": "domain_required"}, 400)

    def test_invalid_json(self, temp_instance):
        result = record_feedback("not a dict")
        assert result == ({"error": "invalid_json"}, 400)

    def test_weight_updates(self, temp_instance):
        r = evaluate_payload(_make_payload(domain="dermatology"))
        initial_weight = r["meta"]["domain_weight"]
        record_feedback({
            "session_id": r["session_id"],
            "domain": "dermatology",
            "feedback": "good",
        })
        status = get_status()
        domain_weights = {d["domain"]: d["weight"] for d in status["domains"]}
        assert domain_weights["dermatology"] > initial_weight


# ---------------------------------------------------------------------------
# Public: patrol
# ---------------------------------------------------------------------------

class TestPatrol:
    def test_no_logs(self, temp_instance):
        result = patrol(manual=True)
        assert result["adjusted"] is False
        assert result["reason"] == "no_logs"

    def test_with_logs(self, temp_instance):
        for _ in range(3):
            evaluate_payload(_make_payload())
        result = patrol(manual=True)
        assert "new_k" in result
        assert "new_eta" in result
        assert "window" in result
        assert result["manual"] is True

    def test_manual_flag(self, temp_instance):
        # Need logs for manual flag to appear in result
        evaluate_payload(_make_payload())
        result = patrol(manual=False)
        assert result["manual"] is False

    def test_window_stats(self, temp_instance):
        for _ in range(5):
            evaluate_payload(_make_payload())
        result = patrol()
        window = result["window"]
        assert "avgD" in window
        assert "sumR" in window
        assert "avgPsi" in window
        assert "window_size" in window
        assert window["window_size"] <= 10


# ---------------------------------------------------------------------------
# Public: get_status
# ---------------------------------------------------------------------------

class TestGetStatus:
    def test_empty_state(self, temp_instance):
        status = get_status()
        assert status["total_sessions"] == 0
        assert status["k"] == pytest.approx(1.5)
        assert status["eta"] == pytest.approx(0.01)
        assert status["domains"] == []
        assert status["avg_deviation"] == pytest.approx(0.0)
        assert status["to_next_patrol"] == 10

    def test_with_sessions(self, temp_instance):
        r1 = evaluate_payload(_make_payload(domain="neurology"))
        r2 = evaluate_payload(_make_payload(domain="cardiology"))
        # Domains only appear after feedback records a weight
        record_feedback({"session_id": r1["session_id"], "domain": "neurology", "feedback": "good"})
        record_feedback({"session_id": r2["session_id"], "domain": "cardiology", "feedback": "good"})
        status = get_status()
        assert status["total_sessions"] == 2
        domain_names = [d["domain"] for d in status["domains"]]
        assert "neurology" in domain_names
        assert "cardiology" in domain_names

    def test_verdict_distribution(self, temp_instance):
        evaluate_payload(_make_payload())
        status = get_status()
        dist = status["verdict_distribution"]
        assert "reliable" in dist
        assert "moderate" in dist
        assert "suspect" in dist
        total = dist["reliable"] + dist["moderate"] + dist["suspect"]
        assert total >= 1

    def test_to_next_patrol(self, temp_instance):
        evaluate_payload(_make_payload())
        status = get_status()
        assert status["to_next_patrol"] == 9

    def test_ranges(self, temp_instance):
        status = get_status()
        assert "ranges" in status
        assert "k" in status["ranges"]
        assert "eta" in status["ranges"]
        assert len(status["ranges"]["k"]) == 2
        assert len(status["ranges"]["eta"]) == 2


# ---------------------------------------------------------------------------
# Public: get_logs
# ---------------------------------------------------------------------------

class TestGetLogs:
    def test_empty(self, temp_instance):
        logs = get_logs()
        assert logs == []

    def test_with_data(self, temp_instance):
        evaluate_payload(_make_payload())
        evaluate_payload(_make_payload())
        logs = get_logs()
        assert len(logs) == 2

    def test_limit(self, temp_instance):
        for _ in range(5):
            evaluate_payload(_make_payload())
        logs = get_logs(limit=3)
        assert len(logs) == 3

    def test_order_most_recent_first(self, temp_instance):
        evaluate_payload(_make_payload(domain="first"))
        evaluate_payload(_make_payload(domain="second"))
        logs = get_logs()
        # reversed order: most recent first
        assert logs[0]["domain"] == "second"
        assert logs[1]["domain"] == "first"

    def test_log_entry_fields(self, temp_instance):
        evaluate_payload(_make_payload())
        logs = get_logs()
        entry = logs[0]
        assert "session_id" in entry
        assert "ts" in entry
        assert "domain" in entry
        assert "D" in entry
        assert "T" in entry
        assert "psi" in entry
        assert "verdict" in entry
