"""Prognostic outcome prediction system.

Predicts disease outcomes including recovery probability, treatment success rate,
complications risk, and mortality risk with confidence intervals.
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class PrognosticOutcome(Enum):
    """Possible disease outcomes."""

    RECOVERED = "recovered"
    CHRONIC = "chronic"
    DETERIORATED = "deteriorated"
    DIED = "died"
    UNKNOWN = "unknown"


class SeverityLevel(Enum):
    """Disease severity levels."""

    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


@dataclass
class PrognosticFactors:
    """Factors influencing prognosis."""

    disease: str
    disease_severity: float  # 0-10
    patient_age: float  # Years
    patient_species: str
    comorbidities: List[str] = field(default_factory=list)
    treatment_type: Optional[str] = None
    treatment_compliance_likelihood: float = 0.7  # 0-1
    access_to_care: float = 0.8  # 0-1 (1.0 = full access)
    overall_health_status: float = 0.5  # 0-1 (0 = poor, 1 = excellent)

    def to_dict(self) -> Dict:
        return {
            "disease": self.disease,
            "disease_severity": self.disease_severity,
            "patient_age": self.patient_age,
            "patient_species": self.patient_species,
            "comorbidities": self.comorbidities,
            "treatment_type": self.treatment_type,
            "treatment_compliance_likelihood": self.treatment_compliance_likelihood,
            "access_to_care": self.access_to_care,
            "overall_health_status": self.overall_health_status,
        }


@dataclass
class PrognosticPrediction:
    """Prediction of disease outcome and prognosis."""

    disease: str
    recovery_probability: float  # 0-1
    recovery_probability_ci: Tuple[float, float]  # Confidence interval
    treatment_success_probability: float  # 0-1
    complication_risk: float  # 0-1
    mortality_risk: float  # 0-1
    estimated_recovery_time_days: Optional[float] = None
    likely_outcome: PrognosticOutcome = PrognosticOutcome.UNKNOWN
    confidence_level: float = 0.7  # 0-1
    risk_factors: List[str] = field(default_factory=list)
    protective_factors: List[str] = field(default_factory=list)
    recommended_monitoring: List[str] = field(default_factory=list)
    epistemic_uncertainty: float = 0.0  # Model uncertainty
    aleatoric_uncertainty: float = 0.0  # Data variability
    clinical_notes: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "disease": self.disease,
            "recovery_probability": round(self.recovery_probability, 4),
            "recovery_probability_ci": (
                round(self.recovery_probability_ci[0], 4),
                round(self.recovery_probability_ci[1], 4),
            ),
            "treatment_success_probability": round(self.treatment_success_probability, 4),
            "complication_risk": round(self.complication_risk, 4),
            "mortality_risk": round(self.mortality_risk, 4),
            "estimated_recovery_time_days": self.estimated_recovery_time_days,
            "likely_outcome": self.likely_outcome.value,
            "confidence_level": round(self.confidence_level, 4),
            "risk_factors": self.risk_factors,
            "protective_factors": self.protective_factors,
            "recommended_monitoring": self.recommended_monitoring,
            "epistemic_uncertainty": round(self.epistemic_uncertainty, 4),
            "aleatoric_uncertainty": round(self.aleatoric_uncertainty, 4),
            "clinical_notes": self.clinical_notes,
            "timestamp": self.timestamp,
        }


class DiseasePrognosticKnowledge:
    """Knowledge base of disease-specific prognostic information."""

    DISEASE_PROGNOSIS = {
        "Pancreatitis": {
            "base_recovery_rate": 0.75,
            "avg_recovery_time_days": 14.0,
            "severity_impact": 0.15,  # Per point (0-10)
            "age_impact": 0.02,  # Per year
            "complications": ["Diabetes Mellitus", "Chronic Pancreatitis"],
            "protective_factors_weights": {
                "good_nutrition": 0.1,
                "early_treatment": 0.15,
                "supportive_care": 0.12,
            },
        },
        "Hip Dysplasia": {
            "base_recovery_rate": 0.40,  # Chronic, not acute recovery
            "avg_recovery_time_days": 365.0,  # Long-term management
            "severity_impact": 0.10,
            "age_impact": 0.03,
            "complications": ["Osteoarthritis", "Canine Cognitive Dysfunction"],
            "protective_factors_weights": {
                "weight_management": 0.15,
                "physical_therapy": 0.18,
                "pain_management": 0.12,
            },
        },
        "Diabetes Mellitus": {
            "base_recovery_rate": 0.30,  # Chronic disease
            "avg_recovery_time_days": float("inf"),  # Lifelong
            "severity_impact": 0.12,
            "age_impact": 0.02,
            "complications": ["Kidney Disease", "Neuropathy", "Retinopathy"],
            "protective_factors_weights": {
                "insulin_compliance": 0.20,
                "diet_management": 0.15,
                "monitoring": 0.18,
            },
        },
        "Osteoarthritis": {
            "base_recovery_rate": 0.35,
            "avg_recovery_time_days": 180.0,
            "severity_impact": 0.08,
            "age_impact": 0.04,
            "complications": ["Canine Cognitive Dysfunction", "Mobility Loss"],
            "protective_factors_weights": {
                "anti_inflammatory": 0.15,
                "physical_therapy": 0.18,
                "weight_management": 0.12,
            },
        },
        "Gastroenteritis": {
            "base_recovery_rate": 0.85,
            "avg_recovery_time_days": 7.0,
            "severity_impact": 0.10,
            "age_impact": 0.01,
            "complications": ["Pancreatitis", "Dehydration"],
            "protective_factors_weights": {
                "fluid_replacement": 0.15,
                "bland_diet": 0.12,
                "antimicrobial_if_needed": 0.10,
            },
        },
    }

    @classmethod
    def get_disease_info(cls, disease: str) -> Optional[Dict]:
        """Get prognostic information for disease."""
        return cls.DISEASE_PROGNOSIS.get(disease)


class PrognosticPredictor:
    """Predicts disease outcomes and prognosis.

    Calculates:
    - Recovery probability (0-100%)
    - Treatment success rate
    - Complication risk
    - Mortality risk
    - Progression timeline
    """

    def __init__(self):
        """Initialize prognostic predictor."""
        self.predictions: Dict[str, PrognosticPrediction] = {}
        self.outcome_database: List[Tuple[str, str, Dict]] = []  # disease, outcome, factors

    def predict_prognosis(self, factors: PrognosticFactors) -> PrognosticPrediction:
        """Predict disease prognosis.

        Args:
            factors: PrognosticFactors describing patient and disease

        Returns:
            PrognosticPrediction with outcome probabilities
        """
        disease_info = DiseasePrognosticKnowledge.get_disease_info(factors.disease)

        if not disease_info:
            return self._create_default_prediction(factors)

        # Calculate base recovery probability
        base_recovery = disease_info["base_recovery_rate"]

        # Adjust for severity
        severity_adjustment = -disease_info["severity_impact"] * factors.disease_severity
        adjusted_recovery = base_recovery + severity_adjustment

        # Adjust for age
        age_adjustment = -disease_info["age_impact"] * factors.patient_age
        adjusted_recovery += age_adjustment

        # Adjust for comorbidities
        comorbidity_penalty = len(factors.comorbidities) * 0.08
        adjusted_recovery -= comorbidity_penalty

        # Adjust for protective factors
        if factors.treatment_type:
            protective_bonus = self._calculate_protective_bonus(
                factors.disease, factors.treatment_type, disease_info.get("protective_factors_weights", {})
            )
            adjusted_recovery += protective_bonus

        # Apply treatment compliance
        adjusted_recovery *= 0.5 + 0.5 * factors.treatment_compliance_likelihood

        # Apply access to care
        adjusted_recovery *= 0.7 + 0.3 * factors.access_to_care

        # Clamp to [0, 1]
        recovery_probability = max(0, min(1, adjusted_recovery))

        # Calculate treatment success probability
        treatment_success = self._calculate_treatment_success(recovery_probability, factors)

        # Calculate complications and mortality
        complication_risk = self._calculate_complication_risk(factors, disease_info)
        mortality_risk = self._calculate_mortality_risk(factors, recovery_probability)

        # Determine likely outcome
        likely_outcome = self._determine_outcome(recovery_probability, mortality_risk)

        # Calculate recovery time
        recovery_time = self._calculate_recovery_time(disease_info, recovery_probability, factors)

        # Create prediction
        prediction = PrognosticPrediction(
            disease=factors.disease,
            recovery_probability=recovery_probability,
            recovery_probability_ci=self._calculate_confidence_interval(recovery_probability, confidence_level=0.95),
            treatment_success_probability=treatment_success,
            complication_risk=complication_risk,
            mortality_risk=mortality_risk,
            estimated_recovery_time_days=recovery_time,
            likely_outcome=likely_outcome,
            confidence_level=self._calculate_confidence_level(factors),
            risk_factors=self._identify_risk_factors(factors),
            protective_factors=self._identify_protective_factors(factors),
            recommended_monitoring=self._recommend_monitoring(factors),
            epistemic_uncertainty=self._calculate_epistemic_uncertainty(factors),
            aleatoric_uncertainty=self._calculate_aleatoric_uncertainty(factors),
        )

        self.predictions[factors.disease] = prediction
        return prediction

    def _create_default_prediction(self, factors: PrognosticFactors) -> PrognosticPrediction:
        """Create default prediction for unknown diseases."""
        # Conservative estimate for unknown diseases
        recovery_prob = 0.5 - (factors.disease_severity * 0.05)

        return PrognosticPrediction(
            disease=factors.disease,
            recovery_probability=max(0, min(1, recovery_prob)),
            recovery_probability_ci=(0.3, 0.7),
            treatment_success_probability=0.5,
            complication_risk=0.3,
            mortality_risk=0.1,
            likely_outcome=PrognosticOutcome.UNKNOWN,
            confidence_level=0.3,
            clinical_notes="Insufficient data for specific prognosis",
        )

    def _calculate_protective_bonus(self, disease: str, treatment_type: str, weights: Dict[str, float]) -> float:
        """Calculate bonus from protective factors."""
        bonus = 0.0

        # Generalized protective factors
        treatment_bonuses = {
            "surgical": 0.20,
            "medical": 0.15,
            "supportive": 0.10,
            "combined": 0.25,
        }

        bonus += treatment_bonuses.get(treatment_type.lower(), 0.10)

        return min(0.30, bonus)  # Cap bonus at 30%

    def _calculate_treatment_success(self, recovery_prob: float, factors: PrognosticFactors) -> float:
        """Calculate treatment success probability."""
        # Treatment success correlates with recovery probability
        success = recovery_prob * 0.9  # 90% correlation

        # Boost if treatment is available
        if factors.treatment_type:
            success *= 1.1

        return min(1.0, success)

    def _calculate_complication_risk(self, factors: PrognosticFactors, disease_info: Dict) -> float:
        """Calculate risk of complications."""
        base_risk = 0.15  # 15% baseline

        # Increase with severity
        base_risk += factors.disease_severity * 0.05

        # Increase with age
        base_risk += min(0.20, factors.patient_age * 0.01)

        # Increase with comorbidities
        base_risk += len(factors.comorbidities) * 0.10

        # Reduce with good overall health
        base_risk *= 1 - factors.overall_health_status * 0.3

        return min(1.0, base_risk)

    def _calculate_mortality_risk(self, factors: PrognosticFactors, recovery_prob: float) -> float:
        """Calculate mortality risk."""
        base_risk = (1 - recovery_prob) * 0.3  # Inverse of recovery

        # Increase with severity
        base_risk += factors.disease_severity * 0.02

        # Increase significantly with age (elderly)
        if factors.patient_age > 10:
            base_risk += (factors.patient_age - 10) * 0.01

        # Increase with comorbidities
        base_risk += len(factors.comorbidities) * 0.05

        # Reduce with access to care
        base_risk *= 1 - factors.access_to_care * 0.3

        return min(1.0, max(0, base_risk))

    def _determine_outcome(self, recovery_prob: float, mortality_risk: float) -> PrognosticOutcome:
        """Determine likely outcome."""
        if mortality_risk > 0.3:
            return PrognosticOutcome.DIED

        if recovery_prob > 0.7:
            return PrognosticOutcome.RECOVERED

        if recovery_prob > 0.3:
            return PrognosticOutcome.CHRONIC

        return PrognosticOutcome.DETERIORATED

    def _calculate_recovery_time(
        self, disease_info: Dict, recovery_prob: float, factors: PrognosticFactors
    ) -> Optional[float]:
        """Calculate estimated recovery time."""
        base_time = disease_info.get("avg_recovery_time_days")

        if base_time is None or base_time == float("inf"):
            return None

        # Increase time if low recovery probability
        time_multiplier = 1.0 + (1 - recovery_prob) * 0.5

        # Increase time with age
        time_multiplier *= 1 + factors.patient_age * 0.02

        # Decrease time with good health status
        time_multiplier *= 1 - factors.overall_health_status * 0.2

        return base_time * time_multiplier

    def _calculate_confidence_interval(self, probability: float, confidence_level: float = 0.95) -> Tuple[float, float]:
        """Calculate confidence interval for probability."""
        # Standard error approximation
        se = math.sqrt(probability * (1 - probability) / 100)

        # Z-score for 95% CI ≈ 1.96
        z = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}.get(confidence_level, 1.96)

        margin = z * se

        lower = max(0, probability - margin)
        upper = min(1, probability + margin)

        return (lower, upper)

    def _calculate_confidence_level(self, factors: PrognosticFactors) -> float:
        """Calculate confidence level for prediction."""
        confidence = 0.7  # Base confidence

        # Increase if good data available
        if factors.disease_severity > 0:
            confidence += 0.1

        # Decrease with age uncertainty
        if factors.patient_age > 0:
            confidence -= 0.05

        # Decrease with comorbidities
        confidence -= len(factors.comorbidities) * 0.05

        return max(0.3, min(1.0, confidence))

    def _identify_risk_factors(self, factors: PrognosticFactors) -> List[str]:
        """Identify risk factors."""
        risks = []

        if factors.disease_severity >= 7:
            risks.append("High disease severity")

        if factors.patient_age > 10:
            risks.append("Advanced age")

        if len(factors.comorbidities) > 0:
            risks.append(f"Comorbidities: {', '.join(factors.comorbidities)}")

        if factors.treatment_compliance_likelihood < 0.5:
            risks.append("Low treatment compliance likelihood")

        if factors.access_to_care < 0.5:
            risks.append("Limited access to care")

        if factors.overall_health_status < 0.4:
            risks.append("Poor overall health status")

        return risks

    def _identify_protective_factors(self, factors: PrognosticFactors) -> List[str]:
        """Identify protective factors."""
        factors_list = []

        if factors.disease_severity < 3:
            factors_list.append("Mild disease severity")

        if factors.patient_age < 5:
            factors_list.append("Young patient")

        if len(factors.comorbidities) == 0:
            factors_list.append("No comorbidities")

        if factors.treatment_compliance_likelihood > 0.8:
            factors_list.append("High treatment compliance likely")

        if factors.access_to_care > 0.8:
            factors_list.append("Good access to care")

        if factors.overall_health_status > 0.7:
            factors_list.append("Excellent overall health")

        if factors.treatment_type:
            factors_list.append(f"Available treatment: {factors.treatment_type}")

        return factors_list

    def _recommend_monitoring(self, factors: PrognosticFactors) -> List[str]:
        """Recommend monitoring strategies."""
        monitoring = []

        if factors.disease_severity >= 5:
            monitoring.append("Weekly clinical examination")

        if len(factors.comorbidities) > 0:
            monitoring.append("Monitor for complications")

        if factors.disease_severity >= 6:
            monitoring.append("Daily vital signs monitoring")

        if "Diabetes Mellitus" in factors.comorbidities:
            monitoring.append("Regular glucose monitoring")

        if "Kidney Disease" in factors.comorbidities:
            monitoring.append("Regular renal function tests")

        if factors.patient_age > 8:
            monitoring.append("Geriatric-specific monitoring")

        if not monitoring:
            monitoring.append("Standard follow-up visits")

        return monitoring

    def _calculate_epistemic_uncertainty(self, factors: PrognosticFactors) -> float:
        """Calculate model uncertainty (epistemic)."""
        # Uncertainty increases with data rarity
        uncertainty = 0.2  # Base model uncertainty

        # Decrease with known disease
        disease_info = DiseasePrognosticKnowledge.get_disease_info(factors.disease)
        if disease_info:
            uncertainty -= 0.1

        # Increase with missing data
        if factors.treatment_type is None:
            uncertainty += 0.05

        return min(0.5, max(0, uncertainty))

    def _calculate_aleatoric_uncertainty(self, factors: PrognosticFactors) -> float:
        """Calculate data variability (aleatoric)."""
        # Uncertainty increases with disease and patient variability
        uncertainty = 0.1  # Base data uncertainty

        # Increase with age variability
        uncertainty += 0.02

        # Increase with comorbidities (more variability)
        uncertainty += len(factors.comorbidities) * 0.05

        # Increase with low health status (more variability)
        uncertainty += (1 - factors.overall_health_status) * 0.05

        return min(0.4, max(0, uncertainty))

    def add_outcome_data(self, disease: str, actual_outcome: PrognosticOutcome, factors: PrognosticFactors):
        """Add actual outcome for model refinement.

        Args:
            disease: Disease name
            actual_outcome: Observed outcome
            factors: Original prognostic factors
        """
        self.outcome_database.append((disease, actual_outcome.value, factors.to_dict()))

    def get_statistics(self) -> Dict:
        """Get statistics about predictions."""
        if not self.outcome_database:
            return {
                "total_outcomes": 0,
                "prediction_accuracy": None,
            }

        predictions = self.predictions
        outcomes = self.outcome_database

        correct = 0
        for disease, outcome, _factors_dict in outcomes:
            if disease in predictions:
                pred = predictions[disease]
                if pred.likely_outcome.value == outcome:
                    correct += 1

        accuracy = correct / len(outcomes) if outcomes else 0

        return {
            "total_outcomes": len(outcomes),
            "prediction_accuracy": round(accuracy, 4),
            "total_predictions_made": len(predictions),
        }

    def to_dict(self) -> Dict:
        """Export predictor state."""
        return {
            "predictions": {disease: pred.to_dict() for disease, pred in self.predictions.items()},
            "statistics": self.get_statistics(),
            "outcome_count": len(self.outcome_database),
        }
