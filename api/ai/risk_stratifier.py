"""Risk stratification engine for veterinary patient assessment.

Assigns patients to risk tiers (LOW/MODERATE/HIGH/CRITICAL) based on
disease severity, age, comorbidities, and prognostic indicators.
Calculates hospitalization probability and generates tier-appropriate
monitoring recommendations.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class RiskTier(Enum):
    """Patient risk classification tiers."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskAssessmentFactors:
    """Input factors for risk stratification."""
    disease: str
    disease_severity: float  # 0-10
    patient_age: float  # years
    patient_species: str = "dog"
    comorbidities: List[str] = field(default_factory=list)
    recovery_probability: float = 0.5  # 0-1, from prognostic predictor
    complication_risk: float = 0.2  # 0-1
    mortality_risk: float = 0.05  # 0-1

    def to_dict(self) -> Dict:
        return {
            "disease": self.disease,
            "disease_severity": self.disease_severity,
            "patient_age": self.patient_age,
            "patient_species": self.patient_species,
            "comorbidities": self.comorbidities,
            "recovery_probability": self.recovery_probability,
            "complication_risk": self.complication_risk,
            "mortality_risk": self.mortality_risk,
        }


@dataclass
class RiskStratificationResult:
    """Output of risk stratification assessment."""
    risk_tier: RiskTier
    risk_score: float  # 0-100
    hospitalization_risk: float  # 0-1
    primary_risk_factors: List[str] = field(default_factory=list)
    monitoring_recommendations: List[str] = field(default_factory=list)
    intervention_level: str = "standard"
    escalation_triggers: List[str] = field(default_factory=list)
    confidence_level: float = 0.7

    def to_dict(self) -> Dict:
        return {
            "risk_tier": self.risk_tier.value,
            "risk_score": round(self.risk_score, 1),
            "hospitalization_risk": round(self.hospitalization_risk, 3),
            "primary_risk_factors": self.primary_risk_factors,
            "monitoring_recommendations": self.monitoring_recommendations,
            "intervention_level": self.intervention_level,
            "escalation_triggers": self.escalation_triggers,
            "confidence_level": round(self.confidence_level, 3),
        }


# ── Risk tier thresholds and intervention details ────────────────────

RISK_THRESHOLDS: Dict[str, Tuple[float, float]] = {
    "low": (0, 30),
    "moderate": (30, 60),
    "high": (60, 80),
    "critical": (80, 100),
}

TIER_INTERVENTIONS: Dict[RiskTier, Dict[str, str]] = {
    RiskTier.LOW: {
        "monitoring_frequency": "Routine (every 2-4 weeks)",
        "testing_level": "Standard periodic labs",
        "treatment_intensity": "Conservative, supportive",
        "intervention_level": "conservative",
    },
    RiskTier.MODERATE: {
        "monitoring_frequency": "Bi-weekly",
        "testing_level": "Enhanced labs + imaging as needed",
        "treatment_intensity": "Standard protocol + close monitoring",
        "intervention_level": "standard",
    },
    RiskTier.HIGH: {
        "monitoring_frequency": "Weekly + phone check-ins",
        "testing_level": "Frequent labs + aggressive imaging",
        "treatment_intensity": "Aggressive intervention, consider referral",
        "intervention_level": "aggressive",
    },
    RiskTier.CRITICAL: {
        "monitoring_frequency": "Daily or hospitalize",
        "testing_level": "Continuous monitoring if hospitalized",
        "treatment_intensity": "Maximum intervention, emergency protocols",
        "intervention_level": "emergency",
    },
}


# ── Disease-specific risk profiles ───────────────────────────────────

DISEASE_RISK_PROFILES: Dict[str, Dict] = {
    "Pancreatitis": {
        "base_risk_score": 45,
        "severity_weight": 4.0,
        "age_risk_per_year": 0.8,
        "hospitalization_base": 0.50,
        "comorbidity_penalties": {
            "Diabetes Mellitus": 15,
            "Chronic Kidney Disease": 12,
            "Obesity": 8,
        },
        "critical_triggers": ["hemorrhagic pancreatitis", "organ failure"],
    },
    "Gastroenteritis": {
        "base_risk_score": 25,
        "severity_weight": 3.0,
        "age_risk_per_year": 0.5,
        "hospitalization_base": 0.25,
        "comorbidity_penalties": {
            "Pancreatitis": 10,
            "Chronic Kidney Disease": 8,
        },
        "critical_triggers": ["severe dehydration", "blood in stool"],
    },
    "Hip Dysplasia": {
        "base_risk_score": 20,
        "severity_weight": 2.5,
        "age_risk_per_year": 0.3,
        "hospitalization_base": 0.15,
        "comorbidity_penalties": {
            "Osteoarthritis": 8,
            "Obesity": 10,
        },
        "critical_triggers": [],
    },
    "Chronic Kidney Disease": {
        "base_risk_score": 55,
        "severity_weight": 5.0,
        "age_risk_per_year": 1.2,
        "hospitalization_base": 0.55,
        "comorbidity_penalties": {
            "Hypertension": 12,
            "Diabetes Mellitus": 15,
            "Heart Disease": 10,
        },
        "critical_triggers": ["uremic crisis", "severe anemia"],
    },
    "Diabetes Mellitus": {
        "base_risk_score": 50,
        "severity_weight": 4.5,
        "age_risk_per_year": 1.0,
        "hospitalization_base": 0.40,
        "comorbidity_penalties": {
            "Pancreatitis": 15,
            "Chronic Kidney Disease": 12,
            "Cushing's Disease": 10,
        },
        "critical_triggers": ["diabetic ketoacidosis", "hypoglycemic crisis"],
    },
    "Heart Disease": {
        "base_risk_score": 55,
        "severity_weight": 5.5,
        "age_risk_per_year": 1.5,
        "hospitalization_base": 0.50,
        "comorbidity_penalties": {
            "Chronic Kidney Disease": 12,
            "Respiratory Disease": 10,
        },
        "critical_triggers": ["congestive heart failure", "arrhythmia"],
    },
    "Lymphoma": {
        "base_risk_score": 70,
        "severity_weight": 5.0,
        "age_risk_per_year": 1.0,
        "hospitalization_base": 0.60,
        "comorbidity_penalties": {
            "Chronic Kidney Disease": 10,
            "Anemia": 8,
        },
        "critical_triggers": ["metastasis", "organ involvement"],
    },
}

# Default profile for diseases not in the knowledge base
_DEFAULT_RISK_PROFILE: Dict = {
    "base_risk_score": 35,
    "severity_weight": 3.5,
    "age_risk_per_year": 0.6,
    "hospitalization_base": 0.30,
    "comorbidity_penalties": {},
    "critical_triggers": [],
}


class RiskStratifier:
    """Stratifies patient risk and generates intervention recommendations."""

    def __init__(self):
        self.assessments: Dict[str, RiskStratificationResult] = {}

    def stratify_risk(
        self, factors: RiskAssessmentFactors
    ) -> RiskStratificationResult:
        """
        Main entry point: calculate risk tier for a patient-disease pair.

        Args:
            factors: Patient and disease factors

        Returns:
            Complete risk stratification result
        """
        profile = DISEASE_RISK_PROFILES.get(factors.disease, _DEFAULT_RISK_PROFILE)

        # Step 1: Base risk score from disease profile
        score = profile["base_risk_score"]

        # Step 2: Severity adjustment (0-10 scale → contribution up to ~50 pts)
        score += factors.disease_severity * profile["severity_weight"]

        # Step 3: Age adjustment
        score += self._calculate_age_adjustment(factors.patient_age, profile)

        # Step 4: Comorbidity penalties
        score += self._calculate_comorbidity_penalty(
            factors.comorbidities, profile
        )

        # Step 5: Prognostic adjustments
        score = self._apply_prognostic_adjustments(
            score,
            factors.recovery_probability,
            factors.complication_risk,
            factors.mortality_risk,
        )

        # Clamp to 0-100
        score = max(0.0, min(100.0, score))

        # Determine tier
        tier = self._determine_risk_tier(score)

        # Calculate hospitalization risk
        hosp_risk = self._calculate_hospitalization_risk(
            factors, score, profile
        )

        # Identify risk factors
        risk_factors = self._identify_risk_factors(factors, profile)

        # Generate monitoring recommendations
        monitoring = self._generate_monitoring_recommendations(tier, factors)

        # Escalation triggers
        escalation = self._generate_escalation_triggers(tier, profile)

        # Intervention level
        intervention = TIER_INTERVENTIONS[tier]["intervention_level"]

        # Confidence based on data completeness
        confidence = self._calculate_confidence(factors)

        result = RiskStratificationResult(
            risk_tier=tier,
            risk_score=score,
            hospitalization_risk=hosp_risk,
            primary_risk_factors=risk_factors,
            monitoring_recommendations=monitoring,
            intervention_level=intervention,
            escalation_triggers=escalation,
            confidence_level=confidence,
        )

        return result

    @staticmethod
    def _calculate_age_adjustment(age: float, profile: Dict) -> float:
        """Calculate age-based risk adjustment."""
        age_per_year = profile.get("age_risk_per_year", 0.6)
        # Young animals (<1 yr) and seniors (>10 yr) have higher risk
        if age < 1.0:
            return age_per_year * 5  # Puppies/kittens: extra vulnerability
        elif age > 10.0:
            return age_per_year * age  # Seniors: increases with age
        elif age > 7.0:
            return age_per_year * (age - 5)  # Middle-aged to senior
        else:
            return 0.0  # Prime age: no adjustment

    @staticmethod
    def _calculate_comorbidity_penalty(
        comorbidities: List[str], profile: Dict
    ) -> float:
        """Sum comorbidity-specific penalties from disease profile."""
        penalties = profile.get("comorbidity_penalties", {})
        total = 0.0
        for comorbidity in comorbidities:
            total += penalties.get(comorbidity, 5.0)  # Default 5 pts per unknown comorbidity
        return total

    @staticmethod
    def _apply_prognostic_adjustments(
        score: float,
        recovery_probability: float,
        complication_risk: float,
        mortality_risk: float,
    ) -> float:
        """Adjust score using prognostic indicators."""
        # Low recovery probability increases risk
        if recovery_probability < 0.5:
            score += (0.5 - recovery_probability) * 20

        # High complication risk increases score
        score += complication_risk * 15

        # High mortality risk is a major factor
        score += mortality_risk * 30

        return score

    @staticmethod
    def _determine_risk_tier(score: float) -> RiskTier:
        """Map numerical score to risk tier."""
        if score >= 80:
            return RiskTier.CRITICAL
        elif score >= 60:
            return RiskTier.HIGH
        elif score >= 30:
            return RiskTier.MODERATE
        else:
            return RiskTier.LOW

    @staticmethod
    def _calculate_hospitalization_risk(
        factors: RiskAssessmentFactors, risk_score: float, profile: Dict
    ) -> float:
        """Estimate probability of hospitalization being needed."""
        base = profile.get("hospitalization_base", 0.30)

        # Score-based adjustment
        score_factor = risk_score / 100.0

        # Combine base with score-derived probability
        hosp_risk = base * 0.4 + score_factor * 0.6

        # Severity boost
        if factors.disease_severity >= 8:
            hosp_risk += 0.15
        elif factors.disease_severity >= 6:
            hosp_risk += 0.05

        # Mortality risk amplification
        hosp_risk += factors.mortality_risk * 0.2

        return max(0.0, min(1.0, hosp_risk))

    @staticmethod
    def _identify_risk_factors(
        factors: RiskAssessmentFactors, profile: Dict
    ) -> List[str]:
        """List primary risk factors driving the score."""
        risk_factors = []

        if factors.disease_severity >= 7:
            risk_factors.append(f"High disease severity ({factors.disease_severity}/10)")
        elif factors.disease_severity >= 5:
            risk_factors.append(f"Moderate disease severity ({factors.disease_severity}/10)")

        if factors.patient_age > 10:
            risk_factors.append(f"Senior patient (age {factors.patient_age})")
        elif factors.patient_age < 1:
            risk_factors.append(f"Neonatal/juvenile patient (age {factors.patient_age})")

        if factors.comorbidities:
            risk_factors.append(
                f"{len(factors.comorbidities)} comorbidities: "
                + ", ".join(factors.comorbidities[:3])
            )

        if factors.recovery_probability < 0.5:
            risk_factors.append(
                f"Low recovery probability ({factors.recovery_probability:.0%})"
            )

        if factors.mortality_risk > 0.1:
            risk_factors.append(
                f"Elevated mortality risk ({factors.mortality_risk:.0%})"
            )

        if factors.complication_risk > 0.3:
            risk_factors.append(
                f"High complication risk ({factors.complication_risk:.0%})"
            )

        return risk_factors

    @staticmethod
    def _generate_monitoring_recommendations(
        tier: RiskTier, factors: RiskAssessmentFactors
    ) -> List[str]:
        """Generate tier-appropriate monitoring plan."""
        info = TIER_INTERVENTIONS[tier]
        recs = [
            f"Monitoring frequency: {info['monitoring_frequency']}",
            f"Testing level: {info['testing_level']}",
            f"Treatment intensity: {info['treatment_intensity']}",
        ]

        if tier in (RiskTier.HIGH, RiskTier.CRITICAL):
            recs.append("Consider specialist referral")
            if factors.comorbidities:
                recs.append("Monitor comorbidity interactions closely")

        if tier == RiskTier.CRITICAL:
            recs.append("Prepare emergency protocols")

        return recs

    @staticmethod
    def _generate_escalation_triggers(
        tier: RiskTier, profile: Dict
    ) -> List[str]:
        """Generate triggers for escalating to a higher care level."""
        triggers = []

        if tier == RiskTier.LOW:
            triggers.append("Symptoms worsen or new symptoms appear")
            triggers.append("No improvement within expected timeframe")
        elif tier == RiskTier.MODERATE:
            triggers.append("No improvement within 1 week")
            triggers.append("Complications developing")
        elif tier == RiskTier.HIGH:
            triggers.append("Any deterioration in condition")
            triggers.append("Medication non-response within 48 hours")
        elif tier == RiskTier.CRITICAL:
            triggers.append("Immediate escalation to emergency care")
            triggers.append("Specialist consultation required")

        # Add disease-specific critical triggers
        for trigger in profile.get("critical_triggers", []):
            triggers.append(f"Disease-specific: {trigger}")

        return triggers

    @staticmethod
    def _calculate_confidence(factors: RiskAssessmentFactors) -> float:
        """Estimate confidence in the risk assessment."""
        confidence = 0.7  # Base confidence

        # Known disease improves confidence
        if factors.disease in DISEASE_RISK_PROFILES:
            confidence += 0.1

        # Prognostic data improves confidence
        if factors.recovery_probability != 0.5:  # Non-default value
            confidence += 0.05
        if factors.complication_risk != 0.2:
            confidence += 0.05

        # Comorbidity info helps
        if factors.comorbidities:
            confidence += 0.03

        return min(confidence, 0.95)
