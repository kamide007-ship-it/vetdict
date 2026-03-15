"""Coverage tests for reco2.input_gate module."""

import pytest

from reco2.input_gate import analyze, rebuild_prompt


class TestAnalyzeCleanText:
    """analyze() with clean, neutral text returns low risk."""

    def test_low_risk_level(self):
        result = analyze("Please check my dog's symptoms.")
        assert result["risk_level"] == "low"

    def test_t_mod_one(self):
        result = analyze("Please check my dog's symptoms.")
        assert result["temperature_modifier"] == 1.0

    def test_action_proceed(self):
        result = analyze("Please check my dog's symptoms.")
        assert result["action"] == "proceed"

    def test_pre_d_below_threshold(self):
        result = analyze("Please check my dog's symptoms.")
        assert result["pre_d"] < 0.30

    def test_no_warnings(self):
        result = analyze("Please check my dog's symptoms.")
        assert result["warnings"] == []

    def test_scores_present(self):
        result = analyze("Please check my dog's symptoms.")
        scores = result["scores"]
        assert "ambiguity" in scores
        assert "assertion_demand" in scores
        assert "emotional_pressure" in scores
        assert "unrealistic" in scores


class TestAnalyzeVagueText:
    """analyze() with vague/ambiguous text raises ambiguity score."""

    def test_ambiguity_elevated(self):
        text = "なんか適当にいい感じにしてください。whatever, kind of."
        result = analyze(text)
        assert result["scores"]["ambiguity"] > 0.0

    def test_warning_present(self):
        text = "なんかとか適当に"
        result = analyze(text)
        assert any("曖昧" in w for w in result["warnings"])


class TestAnalyzeDemandText:
    """analyze() with demanding/assertion text raises assertion_demand."""

    def test_assertion_demand_elevated(self):
        text = "100% guarantee this. 絶対に確実に必ず間違いない。"
        result = analyze(text)
        assert result["scores"]["assertion_demand"] > 0.0

    def test_warning_present(self):
        text = "絶対に必ず guarantee"
        result = analyze(text)
        assert any("断定" in w for w in result["warnings"])


class TestAnalyzeEmotionalText:
    """analyze() with emotional text raises emotional_pressure."""

    def test_emotional_pressure_elevated(self):
        text = "急いで！今すぐ早く！できないの！hurry!"
        result = analyze(text)
        assert result["scores"]["emotional_pressure"] > 0.0

    def test_exclamation_marks_boost(self):
        text_base = "急いで"
        text_exclaim = "急いで！！！"
        r_base = analyze(text_base)
        r_exclaim = analyze(text_exclaim)
        assert r_exclaim["scores"]["emotional_pressure"] >= r_base["scores"]["emotional_pressure"]

    def test_warning_present(self):
        text = "急いで今すぐ"
        result = analyze(text)
        assert any("感情" in w for w in result["warnings"])


class TestAnalyzeUnrealisticText:
    """analyze() with unrealistic expectations raises unrealistic score."""

    def test_unrealistic_elevated(self):
        text = "完璧に全て解決して一瞬で。perfect instantly solve everything."
        result = analyze(text)
        assert result["scores"]["unrealistic"] > 0.0

    def test_warning_present(self):
        text = "完璧に全て解決"
        result = analyze(text)
        assert any("非現実" in w for w in result["warnings"])


class TestAnalyzeEscalation:
    """When 3+ risk factors are active, pre_d is multiplied by 1.25."""

    def test_three_factors_escalation(self):
        # Activate ambiguity + assertion + emotion (3 factors)
        text = "なんか適当に 絶対に guarantee 急いで！"
        result = analyze(text)
        # With 3 active factors, the 1.25 multiplier kicks in
        # We verify pre_d is higher than a simple weighted sum would suggest
        scores = result["scores"]
        raw_pre_d = (
            scores["ambiguity"] * 0.20
            + scores["assertion_demand"] * 0.25
            + scores["emotional_pressure"] * 0.30
            + scores["unrealistic"] * 0.25
        )
        # After escalation, actual pre_d should be >= raw_pre_d
        assert result["pre_d"] >= raw_pre_d * 1.20  # allow slight rounding


class TestAnalyzeRiskLevels:
    """Verify risk level thresholds and corresponding t_mod values."""

    def test_critical_risk(self):
        # Combine many triggers to push pre_d >= 0.70
        text = (
            "なんか適当にいい感じに "
            "絶対に必ず確実に100%保証して断言して "
            "急いで！今すぐ！早く！できないの！ "
            "完璧に全て解決して一瞬で万能な "
        )
        result = analyze(text)
        assert result["risk_level"] in ("critical", "high")
        assert result["temperature_modifier"] <= 0.5

    def test_low_risk_values(self):
        result = analyze("My cat seems fine today.")
        assert result["risk_level"] == "low"
        assert result["temperature_modifier"] == 1.0
        assert result["action"] == "proceed"


class TestRebuildPrompt:
    """rebuild_prompt returns appropriate (prompt, directive) for each risk level."""

    def test_critical_returns_empty_prompt(self):
        analysis = {"risk_level": "critical"}
        prompt, directive = rebuild_prompt("user input", analysis)
        assert prompt == ""
        assert directive == "critical"

    def test_low_returns_original(self):
        analysis = {"risk_level": "low"}
        prompt, directive = rebuild_prompt("user input", analysis)
        assert prompt == "user input"
        assert directive == "none"

    def test_moderate_adds_guidelines(self):
        analysis = {"risk_level": "moderate"}
        prompt, directive = rebuild_prompt("user input", analysis)
        assert "user input" in prompt
        assert "指針" in prompt
        assert directive == "moderate"

    def test_high_adds_warning_directives(self):
        analysis = {"risk_level": "high"}
        prompt, directive = rebuild_prompt("user input", analysis)
        assert "user input" in prompt
        assert "重要指針" in prompt
        assert directive == "high"

    def test_none_analysis_defaults_to_low(self):
        prompt, directive = rebuild_prompt("user input", None)
        assert prompt == "user input"
        assert directive == "none"
