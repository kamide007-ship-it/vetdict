"""Tests for risk_stratifier.py - Patient risk stratification."""


from api.ai.risk_stratifier import (
    _DEFAULT_RISK_PROFILE,
    DISEASE_RISK_PROFILES,
    RISK_THRESHOLDS,
    TIER_INTERVENTIONS,
    RiskAssessmentFactors,
    RiskStratificationResult,
    RiskStratifier,
    RiskTier,
)


def _factors(**kwargs):
    """Helper to create RiskAssessmentFactors with defaults."""
    defaults = {
        "disease": "Pancreatitis",
        "disease_severity": 5.0,
        "patient_age": 5.0,
    }
    defaults.update(kwargs)
    return RiskAssessmentFactors(**defaults)


# ── Data integrity ───────────────────────────────────────────────────

class TestDataIntegrity:

    def test_risk_thresholds_cover_full_range(self):
        assert RISK_THRESHOLDS["low"][0] == 0
        assert RISK_THRESHOLDS["critical"][1] == 100

    def test_tier_interventions_for_all_tiers(self):
        for tier in RiskTier:
            assert tier in TIER_INTERVENTIONS

    def test_disease_profiles_have_required_keys(self):
        required = ["base_risk_score", "severity_weight", "age_risk_per_year",
                     "hospitalization_base", "comorbidity_penalties"]
        for name, profile in DISEASE_RISK_PROFILES.items():
            for key in required:
                assert key in profile, f"{name} missing {key}"

    def test_default_profile_has_required_keys(self):
        assert "base_risk_score" in _DEFAULT_RISK_PROFILE
        assert "severity_weight" in _DEFAULT_RISK_PROFILE


# ── RiskAssessmentFactors ────────────────────────────────────────────

class TestRiskAssessmentFactors:

    def test_to_dict(self):
        f = _factors()
        d = f.to_dict()
        assert d["disease"] == "Pancreatitis"
        assert d["disease_severity"] == 5.0

    def test_defaults(self):
        f = RiskAssessmentFactors(disease="X", disease_severity=3, patient_age=2)
        assert f.patient_species == "dog"
        assert f.comorbidities == []
        assert f.recovery_probability == 0.5


# ── RiskStratificationResult ────────────────────────────────────────

class TestRiskStratificationResult:

    def test_to_dict(self):
        r = RiskStratificationResult(
            risk_tier=RiskTier.HIGH,
            risk_score=72.5,
            hospitalization_risk=0.65,
        )
        d = r.to_dict()
        assert d["risk_tier"] == "high"
        assert d["risk_score"] == 72.5
        assert d["hospitalization_risk"] == 0.65


# ── RiskTier ─────────────────────────────────────────────────────────

class TestRiskTier:

    def test_values(self):
        assert RiskTier.LOW.value == "low"
        assert RiskTier.MODERATE.value == "moderate"
        assert RiskTier.HIGH.value == "high"
        assert RiskTier.CRITICAL.value == "critical"


# ── RiskStratifier ───────────────────────────────────────────────────

class TestStratifyRisk:

    def test_returns_result(self):
        rs = RiskStratifier()
        result = rs.stratify_risk(_factors())
        assert isinstance(result, RiskStratificationResult)

    def test_low_risk_case(self):
        rs = RiskStratifier()
        result = rs.stratify_risk(_factors(
            disease="Hip Dysplasia",
            disease_severity=2.0,
            patient_age=3.0,
            comorbidities=[],
            recovery_probability=0.9,
            complication_risk=0.05,
            mortality_risk=0.0,
        ))
        assert result.risk_tier == RiskTier.LOW

    def test_critical_risk_case(self):
        rs = RiskStratifier()
        result = rs.stratify_risk(_factors(
            disease="Lymphoma",
            disease_severity=9.0,
            patient_age=12.0,
            comorbidities=["Chronic Kidney Disease", "Anemia"],
            recovery_probability=0.2,
            complication_risk=0.6,
            mortality_risk=0.4,
        ))
        assert result.risk_tier == RiskTier.CRITICAL

    def test_score_in_valid_range(self):
        rs = RiskStratifier()
        result = rs.stratify_risk(_factors())
        assert 0.0 <= result.risk_score <= 100.0

    def test_hospitalization_risk_in_valid_range(self):
        rs = RiskStratifier()
        result = rs.stratify_risk(_factors())
        assert 0.0 <= result.hospitalization_risk <= 1.0

    def test_unknown_disease_uses_default(self):
        rs = RiskStratifier()
        result = rs.stratify_risk(_factors(disease="UnknownDisease"))
        assert isinstance(result.risk_tier, RiskTier)

    def test_severity_increases_risk(self):
        rs = RiskStratifier()
        low = rs.stratify_risk(_factors(disease_severity=2.0))
        high = rs.stratify_risk(_factors(disease_severity=9.0))
        assert high.risk_score > low.risk_score

    def test_comorbidities_increase_risk(self):
        rs = RiskStratifier()
        no_comorb = rs.stratify_risk(_factors(comorbidities=[]))
        with_comorb = rs.stratify_risk(_factors(
            comorbidities=["Diabetes Mellitus", "Chronic Kidney Disease"],
        ))
        assert with_comorb.risk_score > no_comorb.risk_score

    def test_age_senior_increases_risk(self):
        rs = RiskStratifier()
        young = rs.stratify_risk(_factors(patient_age=3.0))
        senior = rs.stratify_risk(_factors(patient_age=12.0))
        assert senior.risk_score > young.risk_score

    def test_age_puppy_increases_risk(self):
        rs = RiskStratifier()
        prime = rs.stratify_risk(_factors(patient_age=4.0))
        puppy = rs.stratify_risk(_factors(patient_age=0.5))
        assert puppy.risk_score > prime.risk_score

    def test_has_monitoring_recommendations(self):
        rs = RiskStratifier()
        result = rs.stratify_risk(_factors())
        assert len(result.monitoring_recommendations) > 0

    def test_has_escalation_triggers(self):
        rs = RiskStratifier()
        result = rs.stratify_risk(_factors())
        assert len(result.escalation_triggers) > 0

    def test_confidence_for_known_disease(self):
        rs = RiskStratifier()
        known = rs.stratify_risk(_factors(disease="Pancreatitis"))
        unknown = rs.stratify_risk(_factors(disease="UnknownXYZ"))
        assert known.confidence_level > unknown.confidence_level


class TestDetermineRiskTier:

    def test_low_tier(self):
        assert RiskStratifier._determine_risk_tier(15) == RiskTier.LOW

    def test_moderate_tier(self):
        assert RiskStratifier._determine_risk_tier(45) == RiskTier.MODERATE

    def test_high_tier(self):
        assert RiskStratifier._determine_risk_tier(70) == RiskTier.HIGH

    def test_critical_tier(self):
        assert RiskStratifier._determine_risk_tier(90) == RiskTier.CRITICAL

    def test_boundary_30(self):
        assert RiskStratifier._determine_risk_tier(30) == RiskTier.MODERATE

    def test_boundary_60(self):
        assert RiskStratifier._determine_risk_tier(60) == RiskTier.HIGH

    def test_boundary_80(self):
        assert RiskStratifier._determine_risk_tier(80) == RiskTier.CRITICAL


class TestAgeAdjustment:

    def test_puppy(self):
        adj = RiskStratifier._calculate_age_adjustment(0.5, _DEFAULT_RISK_PROFILE)
        assert adj > 0

    def test_prime_age(self):
        adj = RiskStratifier._calculate_age_adjustment(4.0, _DEFAULT_RISK_PROFILE)
        assert adj == 0.0

    def test_middle_aged(self):
        adj = RiskStratifier._calculate_age_adjustment(8.0, _DEFAULT_RISK_PROFILE)
        assert adj > 0

    def test_senior(self):
        adj = RiskStratifier._calculate_age_adjustment(12.0, _DEFAULT_RISK_PROFILE)
        assert adj > 0


class TestComorbidityPenalty:

    def test_no_comorbidities(self):
        penalty = RiskStratifier._calculate_comorbidity_penalty(
            [], DISEASE_RISK_PROFILES["Pancreatitis"]
        )
        assert penalty == 0.0

    def test_known_comorbidity(self):
        penalty = RiskStratifier._calculate_comorbidity_penalty(
            ["Diabetes Mellitus"], DISEASE_RISK_PROFILES["Pancreatitis"]
        )
        assert penalty == 15  # Exact value from profile

    def test_unknown_comorbidity_default(self):
        penalty = RiskStratifier._calculate_comorbidity_penalty(
            ["UnknownCondition"], DISEASE_RISK_PROFILES["Pancreatitis"]
        )
        assert penalty == 5.0  # Default penalty


class TestHospitalizationRisk:

    def test_high_severity_boosts(self):
        factors_high = _factors(disease_severity=9.0)
        factors_low = _factors(disease_severity=3.0)
        profile = DISEASE_RISK_PROFILES["Pancreatitis"]
        high = RiskStratifier._calculate_hospitalization_risk(factors_high, 80, profile)
        low = RiskStratifier._calculate_hospitalization_risk(factors_low, 40, profile)
        assert high > low

    def test_clamped_to_valid_range(self):
        factors = _factors(disease_severity=10, mortality_risk=0.9)
        profile = DISEASE_RISK_PROFILES["Pancreatitis"]
        risk = RiskStratifier._calculate_hospitalization_risk(factors, 100, profile)
        assert 0.0 <= risk <= 1.0


class TestIdentifyRiskFactors:

    def test_high_severity_listed(self):
        factors = _factors(disease_severity=8.0)
        rf = RiskStratifier._identify_risk_factors(factors, _DEFAULT_RISK_PROFILE)
        assert any("severity" in f.lower() for f in rf)

    def test_senior_age_listed(self):
        factors = _factors(patient_age=12.0)
        rf = RiskStratifier._identify_risk_factors(factors, _DEFAULT_RISK_PROFILE)
        assert any("Senior" in f for f in rf)

    def test_comorbidities_listed(self):
        factors = _factors(comorbidities=["Diabetes"])
        rf = RiskStratifier._identify_risk_factors(factors, _DEFAULT_RISK_PROFILE)
        assert any("comorbidities" in f.lower() for f in rf)

    def test_mortality_risk_listed(self):
        factors = _factors(mortality_risk=0.2)
        rf = RiskStratifier._identify_risk_factors(factors, _DEFAULT_RISK_PROFILE)
        assert any("mortality" in f.lower() for f in rf)


class TestMonitoringRecommendations:

    def test_critical_tier_has_emergency(self):
        recs = RiskStratifier._generate_monitoring_recommendations(
            RiskTier.CRITICAL, _factors()
        )
        assert any("emergency" in r.lower() for r in recs)

    def test_low_tier_has_routine(self):
        recs = RiskStratifier._generate_monitoring_recommendations(
            RiskTier.LOW, _factors()
        )
        assert any("Routine" in r for r in recs)
