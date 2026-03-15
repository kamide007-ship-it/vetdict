"""Tests for decision_support.py - Advanced Decision Support Engine (Stage 6)."""

import pytest

from api.ai.decision_support import (
    AlertSeverity,
    ClinicalAlert,
    ClinicalPathway,
    DecisionSupportEngine,
    DecisionSupportResult,
    FollowUpSchedule,
    FOLLOW_UP_DEFAULTS,
    PATHWAY_RULES,
    _OWNER_INSTRUCTIONS,
)
from api.ai.risk_stratifier import RiskStratificationResult, RiskTier
from api.ai.prognostic_predictor import PrognosticPrediction
from api.ai.treatment_response_predictor import TreatmentResponse


# ── Helpers ──────────────────────────────────────────────────────────

def _risk_result(tier=RiskTier.MODERATE, score=50.0, hosp_risk=0.4, **kw):
    defaults = {
        "risk_tier": tier,
        "risk_score": score,
        "hospitalization_risk": hosp_risk,
        "primary_risk_factors": [],
        "monitoring_recommendations": [],
        "escalation_triggers": [],
        "confidence_level": 0.8,
    }
    defaults.update(kw)
    return RiskStratificationResult(**defaults)


def _prognosis(recovery=0.6, complication=0.2, mortality=0.05, **kw):
    defaults = {
        "disease": "Pancreatitis",
        "recovery_probability": recovery,
        "recovery_probability_ci": (recovery - 0.1, recovery + 0.1),
        "treatment_success_probability": 0.6,
        "complication_risk": complication,
        "mortality_risk": mortality,
        "risk_factors": [],
        "protective_factors": [],
        "recommended_monitoring": [],
        "confidence_level": 0.7,
        "epistemic_uncertainty": 0.2,
    }
    defaults.update(kw)
    return PrognosticPrediction(**defaults)


def _treatment(name="Fluid therapy", success=0.7, **kw):
    defaults = {
        "disease": "Pancreatitis",
        "treatment_name": name,
        "success_probability": success,
        "success_probability_ci": (success - 0.1, success + 0.1),
        "expected_timeline": "5-7 days",
        "compliance_likelihood": 0.8,
        "expected_side_effects": [],
        "monitoring_requirements": [],
        "alternative_treatments": [],
        "confidence_level": 0.7,
        "risk_benefit_ratio": "favorable",
    }
    defaults.update(kw)
    return TreatmentResponse(**defaults)


# ── Data integrity ──────────────────────────────────────────────────

class TestDataIntegrity:

    def test_pathway_rules_cover_all_tiers(self):
        for tier in RiskTier:
            assert tier in PATHWAY_RULES

    def test_follow_up_defaults_cover_all_tiers(self):
        for tier in RiskTier:
            assert tier in FOLLOW_UP_DEFAULTS

    def test_owner_instructions_cover_all_tiers(self):
        for tier in RiskTier:
            assert tier in _OWNER_INSTRUCTIONS
            assert len(_OWNER_INSTRUCTIONS[tier]) > 0

    def test_follow_up_defaults_have_required_keys(self):
        required = ["next_visit_days", "visit_type", "recurring_interval_days", "duration_weeks"]
        for tier, defaults in FOLLOW_UP_DEFAULTS.items():
            for key in required:
                assert key in defaults, f"{tier.value} missing {key}"


# ── Dataclass to_dict ───────────────────────────────────────────────

class TestClinicalAlert:

    def test_to_dict(self):
        a = ClinicalAlert(AlertSeverity.WARNING, "test msg", "risk")
        d = a.to_dict()
        assert d["severity"] == "warning"
        assert d["message"] == "test msg"
        assert d["category"] == "risk"


class TestFollowUpSchedule:

    def test_to_dict(self):
        f = FollowUpSchedule(next_visit_days=7, visit_type="recheck")
        d = f.to_dict()
        assert d["next_visit_days"] == 7
        assert d["visit_type"] == "recheck"
        assert d["recurring_interval_days"] is None


class TestDecisionSupportResult:

    def test_to_dict(self):
        r = DecisionSupportResult(
            clinical_pathway=ClinicalPathway.INPATIENT,
            alerts=[ClinicalAlert(AlertSeverity.URGENT, "msg", "risk")],
            follow_up=FollowUpSchedule(3, "full_exam"),
            referral_recommended=True,
            referral_reason="reason",
            hospitalization_recommended=True,
            owner_instructions=["do X"],
            clinical_summary="summary",
        )
        d = r.to_dict()
        assert d["clinical_pathway"] == "inpatient"
        assert len(d["alerts"]) == 1
        assert d["follow_up"]["next_visit_days"] == 3
        assert d["referral_recommended"] is True
        assert d["hospitalization_recommended"] is True


# ── Pathway selection ───────────────────────────────────────────────

class TestSelectPathway:

    def test_low_tier(self):
        p = DecisionSupportEngine._select_pathway(
            RiskTier.LOW, _prognosis(), 3.0
        )
        assert p == ClinicalPathway.OUTPATIENT_CONSERVATIVE

    def test_moderate_tier(self):
        p = DecisionSupportEngine._select_pathway(
            RiskTier.MODERATE, _prognosis(), 4.0
        )
        assert p == ClinicalPathway.OUTPATIENT_ACTIVE

    def test_high_tier(self):
        p = DecisionSupportEngine._select_pathway(
            RiskTier.HIGH, _prognosis(), 7.0
        )
        assert p == ClinicalPathway.INPATIENT

    def test_critical_tier(self):
        p = DecisionSupportEngine._select_pathway(
            RiskTier.CRITICAL, _prognosis(), 9.0
        )
        assert p == ClinicalPathway.EMERGENCY

    def test_palliative_override(self):
        p = DecisionSupportEngine._select_pathway(
            RiskTier.HIGH,
            _prognosis(recovery=0.1, mortality=0.7),
            8.0,
        )
        assert p == ClinicalPathway.PALLIATIVE

    def test_moderate_high_severity_day_hospital(self):
        p = DecisionSupportEngine._select_pathway(
            RiskTier.MODERATE, _prognosis(), 7.0
        )
        assert p == ClinicalPathway.DAY_HOSPITAL


# ── Alert generation ────────────────────────────────────────────────

class TestGenerateAlerts:

    def test_critical_tier_alert(self):
        alerts = DecisionSupportEngine._generate_alerts(
            _risk_result(tier=RiskTier.CRITICAL, score=90),
            _prognosis(), [], 8.0,
        )
        assert any(a.severity == AlertSeverity.CRITICAL for a in alerts)

    def test_high_tier_alert(self):
        alerts = DecisionSupportEngine._generate_alerts(
            _risk_result(tier=RiskTier.HIGH, score=70),
            _prognosis(), [], 6.0,
        )
        assert any(a.severity == AlertSeverity.URGENT for a in alerts)

    def test_high_hospitalization_alert(self):
        alerts = DecisionSupportEngine._generate_alerts(
            _risk_result(hosp_risk=0.8),
            _prognosis(), [], 5.0,
        )
        assert any("hospitalization" in a.message.lower() for a in alerts)

    def test_mortality_alert(self):
        alerts = DecisionSupportEngine._generate_alerts(
            _risk_result(),
            _prognosis(mortality=0.4), [], 5.0,
        )
        assert any("mortality" in a.message.lower() for a in alerts)

    def test_low_recovery_alert(self):
        alerts = DecisionSupportEngine._generate_alerts(
            _risk_result(),
            _prognosis(recovery=0.2), [], 5.0,
        )
        assert any("recovery" in a.message.lower() for a in alerts)

    def test_no_good_treatment_alert(self):
        alerts = DecisionSupportEngine._generate_alerts(
            _risk_result(),
            _prognosis(),
            [_treatment(success=0.3), _treatment(success=0.2)],
            5.0,
        )
        assert any("treatment" in a.category for a in alerts)

    def test_high_severity_alert(self):
        alerts = DecisionSupportEngine._generate_alerts(
            _risk_result(), _prognosis(), [], 9.0,
        )
        assert any("severity" in a.message.lower() for a in alerts)

    def test_low_risk_no_alerts(self):
        alerts = DecisionSupportEngine._generate_alerts(
            _risk_result(tier=RiskTier.LOW, score=15, hosp_risk=0.2),
            _prognosis(recovery=0.8, mortality=0.02),
            [_treatment(success=0.8)],
            3.0,
        )
        assert len(alerts) == 0


# ── Follow-up schedule ──────────────────────────────────────────────

class TestBuildFollowUp:

    def test_low_tier_follow_up(self):
        fu = DecisionSupportEngine._build_follow_up(
            RiskTier.LOW, "Gastroenteritis", _prognosis()
        )
        assert fu.next_visit_days == 14
        assert fu.visit_type == "recheck"

    def test_critical_tier_follow_up(self):
        fu = DecisionSupportEngine._build_follow_up(
            RiskTier.CRITICAL, "Lymphoma", _prognosis()
        )
        assert fu.next_visit_days == 1

    def test_chronic_note(self):
        fu = DecisionSupportEngine._build_follow_up(
            RiskTier.MODERATE, "CKD", _prognosis(recovery=0.3)
        )
        assert "chronic" in fu.notes.lower()

    def test_disease_in_notes(self):
        fu = DecisionSupportEngine._build_follow_up(
            RiskTier.LOW, "Hip Dysplasia", _prognosis()
        )
        assert "Hip Dysplasia" in fu.notes


# ── Referral assessment ─────────────────────────────────────────────

class TestAssessReferral:

    def test_critical_tier_referral(self):
        rec, reason = DecisionSupportEngine._assess_referral(
            RiskTier.CRITICAL, _prognosis(), 8.0
        )
        assert rec is True
        assert "Critical" in reason

    def test_high_tier_severe_referral(self):
        rec, reason = DecisionSupportEngine._assess_referral(
            RiskTier.HIGH, _prognosis(), 8.0
        )
        assert rec is True

    def test_high_mortality_referral(self):
        rec, reason = DecisionSupportEngine._assess_referral(
            RiskTier.MODERATE, _prognosis(mortality=0.5), 5.0
        )
        assert rec is True
        assert "mortality" in reason.lower()

    def test_low_risk_no_referral(self):
        rec, reason = DecisionSupportEngine._assess_referral(
            RiskTier.LOW, _prognosis(), 3.0
        )
        assert rec is False
        assert reason == ""


# ── Hospitalization assessment ──────────────────────────────────────

class TestAssessHospitalization:

    def test_critical_tier(self):
        assert DecisionSupportEngine._assess_hospitalization(
            _risk_result(tier=RiskTier.CRITICAL), _prognosis()
        ) is True

    def test_high_hosp_risk(self):
        assert DecisionSupportEngine._assess_hospitalization(
            _risk_result(hosp_risk=0.7), _prognosis()
        ) is True

    def test_high_mortality(self):
        assert DecisionSupportEngine._assess_hospitalization(
            _risk_result(), _prognosis(mortality=0.5)
        ) is True

    def test_low_risk_no_hospitalization(self):
        assert DecisionSupportEngine._assess_hospitalization(
            _risk_result(tier=RiskTier.LOW, hosp_risk=0.2),
            _prognosis(mortality=0.02),
        ) is False


# ── Owner instructions ──────────────────────────────────────────────

class TestOwnerInstructions:

    def test_includes_disease(self):
        instr = DecisionSupportEngine._generate_owner_instructions(
            RiskTier.LOW, "Pancreatitis", []
        )
        assert any("Pancreatitis" in i for i in instr)

    def test_includes_treatment(self):
        instr = DecisionSupportEngine._generate_owner_instructions(
            RiskTier.MODERATE, "X", [_treatment(name="IV Fluids")]
        )
        assert any("IV Fluids" in i for i in instr)

    def test_critical_has_emergency(self):
        instr = DecisionSupportEngine._generate_owner_instructions(
            RiskTier.CRITICAL, "X", []
        )
        assert any("emergency" in i.lower() for i in instr)


# ── Clinical summary ────────────────────────────────────────────────

class TestGenerateSummary:

    def test_contains_disease(self):
        s = DecisionSupportEngine._generate_summary(
            "Pancreatitis", RiskTier.MODERATE,
            ClinicalPathway.OUTPATIENT_ACTIVE,
            _prognosis(), [_treatment()],
        )
        assert "Pancreatitis" in s

    def test_contains_tier(self):
        s = DecisionSupportEngine._generate_summary(
            "X", RiskTier.HIGH, ClinicalPathway.INPATIENT,
            _prognosis(), [_treatment()],
        )
        assert "HIGH" in s

    def test_contains_treatment(self):
        s = DecisionSupportEngine._generate_summary(
            "X", RiskTier.LOW, ClinicalPathway.OUTPATIENT_CONSERVATIVE,
            _prognosis(), [_treatment(name="Surgery")],
        )
        assert "Surgery" in s

    def test_no_treatments_fallback(self):
        s = DecisionSupportEngine._generate_summary(
            "X", RiskTier.LOW, ClinicalPathway.OUTPATIENT_CONSERVATIVE,
            _prognosis(), [],
        )
        assert "supportive care" in s


# ── Full integration ────────────────────────────────────────────────

class TestGenerateDecisionSupport:

    def test_returns_result(self):
        engine = DecisionSupportEngine()
        result = engine.generate_decision_support(
            risk_result=_risk_result(),
            prognosis=_prognosis(),
            treatments=[_treatment()],
            disease="Pancreatitis",
            disease_severity=5.0,
            patient_age=6.0,
        )
        assert isinstance(result, DecisionSupportResult)

    def test_low_risk_outpatient(self):
        engine = DecisionSupportEngine()
        result = engine.generate_decision_support(
            risk_result=_risk_result(tier=RiskTier.LOW, score=15, hosp_risk=0.2),
            prognosis=_prognosis(recovery=0.8, mortality=0.02),
            treatments=[_treatment(success=0.8)],
            disease="Hip Dysplasia",
            disease_severity=3.0,
            patient_age=4.0,
        )
        assert result.clinical_pathway == ClinicalPathway.OUTPATIENT_CONSERVATIVE
        assert result.referral_recommended is False
        assert result.hospitalization_recommended is False

    def test_critical_risk_emergency(self):
        engine = DecisionSupportEngine()
        result = engine.generate_decision_support(
            risk_result=_risk_result(tier=RiskTier.CRITICAL, score=90, hosp_risk=0.9),
            prognosis=_prognosis(recovery=0.2, mortality=0.4),
            treatments=[_treatment(success=0.3)],
            disease="Lymphoma",
            disease_severity=9.0,
            patient_age=12.0,
        )
        assert result.clinical_pathway == ClinicalPathway.EMERGENCY
        assert result.referral_recommended is True
        assert result.hospitalization_recommended is True
        assert len(result.alerts) > 0

    def test_to_dict_serializable(self):
        engine = DecisionSupportEngine()
        result = engine.generate_decision_support(
            risk_result=_risk_result(),
            prognosis=_prognosis(),
            treatments=[_treatment()],
            disease="Pancreatitis",
            disease_severity=5.0,
            patient_age=6.0,
        )
        d = result.to_dict()
        assert isinstance(d, dict)
        assert "clinical_pathway" in d
        assert "alerts" in d
        assert "follow_up" in d

    def test_palliative_pathway_override(self):
        engine = DecisionSupportEngine()
        result = engine.generate_decision_support(
            risk_result=_risk_result(tier=RiskTier.HIGH, score=75, hosp_risk=0.6),
            prognosis=_prognosis(recovery=0.1, mortality=0.7),
            treatments=[_treatment(success=0.2)],
            disease="Lymphoma",
            disease_severity=9.0,
            patient_age=14.0,
        )
        assert result.clinical_pathway == ClinicalPathway.PALLIATIVE
