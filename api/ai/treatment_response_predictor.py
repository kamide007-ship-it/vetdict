"""Treatment response prediction system.

Predicts likelihood of treatment success based on disease, patient factors,
and treatment options. Analyzes multiple treatment modalities and their efficacy.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class TreatmentModality(Enum):
    """Types of treatment modalities."""
    PHARMACOLOGICAL = "pharmacological"
    SURGICAL = "surgical"
    BEHAVIORAL = "behavioral"
    NUTRITIONAL = "nutritional"
    PHYSICAL_THERAPY = "physical_therapy"
    COMBINATION = "combination"
    SUPPORTIVE = "supportive"
    ALTERNATIVE = "alternative"


class TreatmentAdherence(Enum):
    """Treatment adherence levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    UNKNOWN = "unknown"


@dataclass
class TreatmentOption:
    """A specific treatment option for a disease."""
    name: str
    modality: TreatmentModality
    disease: str
    expected_success_rate: float  # 0-1
    onset_time_days: float  # How long until effect
    duration_days: Optional[float]  # How long treatment lasts (None = indefinite)
    cost_category: str  # "low", "medium", "high"
    side_effects_probability: float  # 0-1
    contraindications: List[str] = field(default_factory=list)
    preconditions: List[str] = field(default_factory=list)
    evidence_level: str = "moderate"  # "low", "moderate", "high"
    notes: str = ""

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "modality": self.modality.value,
            "disease": self.disease,
            "expected_success_rate": round(self.expected_success_rate, 4),
            "onset_time_days": self.onset_time_days,
            "duration_days": self.duration_days,
            "cost_category": self.cost_category,
            "side_effects_probability": round(self.side_effects_probability, 4),
            "contraindications": self.contraindications,
            "preconditions": self.preconditions,
            "evidence_level": self.evidence_level,
            "notes": self.notes,
        }


@dataclass
class TreatmentResponse:
    """Prediction of treatment response."""
    disease: str
    treatment_name: str
    success_probability: float  # 0-1
    success_probability_ci: Tuple[float, float]  # 95% confidence interval
    expected_timeline: str  # "immediate", "days", "weeks", "months"
    compliance_likelihood: float  # Probability patient will adhere
    expected_side_effects: List[str]
    monitoring_requirements: List[str]
    alternative_treatments: List[str]
    confidence_level: float  # 0-1
    risk_benefit_ratio: str  # "favorable", "balanced", "unfavorable"
    recommendations: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "disease": self.disease,
            "treatment_name": self.treatment_name,
            "success_probability": round(self.success_probability, 4),
            "success_probability_ci": (
                round(self.success_probability_ci[0], 4),
                round(self.success_probability_ci[1], 4),
            ),
            "expected_timeline": self.expected_timeline,
            "compliance_likelihood": round(self.compliance_likelihood, 4),
            "expected_side_effects": self.expected_side_effects,
            "monitoring_requirements": self.monitoring_requirements,
            "alternative_treatments": self.alternative_treatments,
            "confidence_level": round(self.confidence_level, 4),
            "risk_benefit_ratio": self.risk_benefit_ratio,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp,
        }


class TreatmentKnowledgeBase:
    """Knowledge base of treatment options for diseases."""

    TREATMENT_OPTIONS = {
        "Pancreatitis": [
            TreatmentOption(
                name="Supportive Care (IV fluids, rest, diet)",
                modality=TreatmentModality.SUPPORTIVE,
                disease="Pancreatitis",
                expected_success_rate=0.80,
                onset_time_days=2.0,
                duration_days=14.0,
                cost_category="medium",
                side_effects_probability=0.05,
                evidence_level="high",
                preconditions=["Adequate vascular access"],
                notes="First-line treatment, critical for recovery",
            ),
            TreatmentOption(
                name="Pancreatic Enzyme Inhibitors",
                modality=TreatmentModality.PHARMACOLOGICAL,
                disease="Pancreatitis",
                expected_success_rate=0.65,
                onset_time_days=1.0,
                duration_days=10.0,
                cost_category="high",
                side_effects_probability=0.15,
                evidence_level="moderate",
                contraindications=["Renal failure"],
                notes="Used in severe cases",
            ),
            TreatmentOption(
                name="Bland Diet Recovery",
                modality=TreatmentModality.NUTRITIONAL,
                disease="Pancreatitis",
                expected_success_rate=0.75,
                onset_time_days=7.0,
                duration_days=30.0,
                cost_category="low",
                side_effects_probability=0.0,
                evidence_level="high",
                notes="Transition to low-fat diet",
            ),
        ],
        "Osteoarthritis": [
            TreatmentOption(
                name="NSAIDs (Carprofen, Meloxicam)",
                modality=TreatmentModality.PHARMACOLOGICAL,
                disease="Osteoarthritis",
                expected_success_rate=0.70,
                onset_time_days=1.0,
                duration_days=None,  # Indefinite
                cost_category="low",
                side_effects_probability=0.10,
                contraindications=["Renal disease", "Gastrointestinal ulcers"],
                evidence_level="high",
                notes="Most common treatment",
            ),
            TreatmentOption(
                name="Physical Therapy & Exercise",
                modality=TreatmentModality.PHYSICAL_THERAPY,
                disease="Osteoarthritis",
                expected_success_rate=0.65,
                onset_time_days=14.0,
                duration_days=None,
                cost_category="medium",
                side_effects_probability=0.0,
                evidence_level="high",
                notes="Should be combined with medication",
            ),
            TreatmentOption(
                name="Joint Supplements (Glucosamine, Chondroitin)",
                modality=TreatmentModality.NUTRITIONAL,
                disease="Osteoarthritis",
                expected_success_rate=0.45,
                onset_time_days=21.0,
                duration_days=None,
                cost_category="medium",
                side_effects_probability=0.05,
                evidence_level="moderate",
                notes="Long-term management",
            ),
            TreatmentOption(
                name="Surgical Joint Procedures",
                modality=TreatmentModality.SURGICAL,
                disease="Osteoarthritis",
                expected_success_rate=0.60,
                onset_time_days=0.0,
                duration_days=365.0,
                cost_category="high",
                side_effects_probability=0.15,
                evidence_level="moderate",
                preconditions=["Surgical candidate", "Severe disease"],
                notes="For advanced cases",
            ),
        ],
        "Diabetes Mellitus": [
            TreatmentOption(
                name="Insulin Therapy",
                modality=TreatmentModality.PHARMACOLOGICAL,
                disease="Diabetes Mellitus",
                expected_success_rate=0.85,
                onset_time_days=1.0,
                duration_days=None,
                cost_category="high",
                side_effects_probability=0.20,
                evidence_level="high",
                preconditions=["Owner can administer injections"],
                notes="Essential for most diabetic dogs/cats",
            ),
            TreatmentOption(
                name="Dietary Management (High-protein diet)",
                modality=TreatmentModality.NUTRITIONAL,
                disease="Diabetes Mellitus",
                expected_success_rate=0.50,
                onset_time_days=14.0,
                duration_days=None,
                cost_category="medium",
                side_effects_probability=0.0,
                evidence_level="moderate",
                notes="Essential component of therapy",
            ),
            TreatmentOption(
                name="Oral Hypoglycemic Agents",
                modality=TreatmentModality.PHARMACOLOGICAL,
                disease="Diabetes Mellitus",
                expected_success_rate=0.40,
                onset_time_days=3.0,
                duration_days=None,
                cost_category="low",
                side_effects_probability=0.15,
                contraindications=["Type 1 diabetes"],
                evidence_level="moderate",
                notes="Limited efficacy in dogs, more useful in cats",
            ),
            TreatmentOption(
                name="Weight Management Program",
                modality=TreatmentModality.BEHAVIORAL,
                disease="Diabetes Mellitus",
                expected_success_rate=0.55,
                onset_time_days=30.0,
                duration_days=None,
                cost_category="low",
                side_effects_probability=0.0,
                evidence_level="high",
                notes="Improves insulin sensitivity",
            ),
        ],
        "Hip Dysplasia": [
            TreatmentOption(
                name="NSAIDs for Pain Management",
                modality=TreatmentModality.PHARMACOLOGICAL,
                disease="Hip Dysplasia",
                expected_success_rate=0.65,
                onset_time_days=1.0,
                duration_days=None,
                cost_category="low",
                side_effects_probability=0.10,
                evidence_level="high",
                notes="Manage inflammation and pain",
            ),
            TreatmentOption(
                name="Surgical Intervention (THR)",
                modality=TreatmentModality.SURGICAL,
                disease="Hip Dysplasia",
                expected_success_rate=0.85,
                onset_time_days=0.0,
                duration_days=365.0,
                cost_category="high",
                side_effects_probability=0.15,
                preconditions=["Surgical candidate", "Severe disease"],
                evidence_level="high",
                notes="Total Hip Replacement - excellent long-term outcome",
            ),
            TreatmentOption(
                name="Physical Rehabilitation",
                modality=TreatmentModality.PHYSICAL_THERAPY,
                disease="Hip Dysplasia",
                expected_success_rate=0.60,
                onset_time_days=14.0,
                duration_days=None,
                cost_category="medium",
                side_effects_probability=0.0,
                evidence_level="moderate",
                notes="Strengthen supporting muscles",
            ),
            TreatmentOption(
                name="Weight Management",
                modality=TreatmentModality.BEHAVIORAL,
                disease="Hip Dysplasia",
                expected_success_rate=0.55,
                onset_time_days=30.0,
                duration_days=None,
                cost_category="low",
                side_effects_probability=0.0,
                evidence_level="high",
                notes="Reduce joint stress",
            ),
        ],
    }

    @classmethod
    def get_treatment_options(cls, disease: str) -> List[TreatmentOption]:
        """Get all treatment options for a disease."""
        return cls.TREATMENT_OPTIONS.get(disease, [])

    @classmethod
    def get_treatment(cls, disease: str, treatment_name: str) -> Optional[TreatmentOption]:
        """Get specific treatment option."""
        options = cls.get_treatment_options(disease)
        for option in options:
            if option.name == treatment_name:
                return option
        return None


class TreatmentResponsePredictor:
    """Predicts treatment response and success likelihood.

    Factors considered:
    - Disease type and severity
    - Patient age and comorbidities
    - Prior treatment history
    - Medication interactions
    - Owner compliance likelihood
    - Cost and resource constraints
    """

    def __init__(self):
        """Initialize treatment predictor."""
        self.predictions: Dict[Tuple[str, str], TreatmentResponse] = {}
        self.outcome_history: List[Tuple[str, str, bool]] = []

    def predict_treatment_response(self,
                                   disease: str,
                                   treatment_name: str,
                                   patient_age: float,
                                   comorbidities: List[str] = None,
                                   prior_treatments: List[str] = None,
                                   owner_compliance_likelihood: float = 0.7,
                                   disease_severity: float = 5.0) -> Optional[TreatmentResponse]:
        """Predict response to specific treatment.

        Args:
            disease: Disease name
            treatment_name: Treatment option name
            patient_age: Patient age in years
            comorbidities: List of comorbid conditions
            prior_treatments: List of previously tried treatments
            owner_compliance_likelihood: Probability owner will comply (0-1)
            disease_severity: Disease severity (0-10)

        Returns:
            TreatmentResponse prediction or None if treatment not found
        """
        comorbidities = comorbidities or []
        prior_treatments = prior_treatments or []

        treatment = TreatmentKnowledgeBase.get_treatment(disease, treatment_name)
        if not treatment:
            return None

        # Base success probability
        success_prob = treatment.expected_success_rate

        # Adjust for contraindications
        for contraindication in treatment.contraindications:
            if contraindication.lower() in [c.lower() for c in comorbidities]:
                success_prob *= 0.5  # 50% reduction

        # Adjust for age
        success_prob *= self._age_adjustment_factor(patient_age, disease)

        # Adjust for disease severity
        success_prob *= self._severity_adjustment_factor(disease_severity)

        # Adjust for prior treatment failure
        failure_penalty = len([t for t in prior_treatments if t != treatment_name]) * 0.05
        success_prob = max(0, success_prob - failure_penalty)

        # Clamp to [0, 1]
        success_prob = max(0, min(1, success_prob))

        # Calculate compliance impact
        actual_success_prob = success_prob * owner_compliance_likelihood

        # Calculate side effects
        side_effects = self._predict_side_effects(treatment, comorbidities, patient_age)

        # Determine timeline
        timeline = self._determine_timeline(treatment.onset_time_days)

        # Calculate confidence interval
        ci = self._calculate_confidence_interval(success_prob, disease)

        # Get alternatives
        alternatives = self._get_alternative_treatments(disease, treatment_name)

        # Assess risk-benefit
        risk_benefit = self._assess_risk_benefit(
            success_prob, treatment.side_effects_probability, disease_severity
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            treatment, success_prob, owner_compliance_likelihood, comorbidities
        )

        response = TreatmentResponse(
            disease=disease,
            treatment_name=treatment_name,
            success_probability=actual_success_prob,
            success_probability_ci=ci,
            expected_timeline=timeline,
            compliance_likelihood=owner_compliance_likelihood,
            expected_side_effects=side_effects,
            monitoring_requirements=self._get_monitoring_requirements(treatment),
            alternative_treatments=alternatives,
            confidence_level=self._calculate_confidence(disease, treatment_name),
            risk_benefit_ratio=risk_benefit,
            recommendations=recommendations,
        )

        self.predictions[(disease, treatment_name)] = response
        return response

    def predict_all_treatments(self,
                              disease: str,
                              patient_age: float,
                              comorbidities: List[str] = None,
                              owner_compliance_likelihood: float = 0.7,
                              disease_severity: float = 5.0
                              ) -> List[TreatmentResponse]:
        """Predict response to all available treatments for disease.

        Args:
            disease: Disease name
            patient_age: Patient age
            comorbidities: List of comorbidities
            owner_compliance_likelihood: Probability of compliance
            disease_severity: Disease severity (0-10)

        Returns:
            List of TreatmentResponse predictions sorted by success probability
        """
        options = TreatmentKnowledgeBase.get_treatment_options(disease)

        responses = []
        for option in options:
            response = self.predict_treatment_response(
                disease=disease,
                treatment_name=option.name,
                patient_age=patient_age,
                comorbidities=comorbidities,
                owner_compliance_likelihood=owner_compliance_likelihood,
                disease_severity=disease_severity,
            )
            if response:
                responses.append(response)

        # Sort by success probability (descending)
        responses.sort(key=lambda r: r.success_probability, reverse=True)
        return responses

    def _age_adjustment_factor(self, patient_age: float, disease: str) -> float:
        """Calculate age-based adjustment factor."""
        if patient_age < 1:
            return 0.8  # Puppies/kittens have higher risk
        elif patient_age > 10:
            return 0.85  # Seniors have slightly lower success
        else:
            return 1.0

    def _severity_adjustment_factor(self, disease_severity: float) -> float:
        """Calculate severity-based adjustment factor."""
        # More severe disease = lower treatment success
        return 1.0 - (disease_severity * 0.05)  # 5% per severity point

    def _predict_side_effects(self,
                             treatment: TreatmentOption,
                             comorbidities: List[str],
                             patient_age: float) -> List[str]:
        """Predict likely side effects."""
        side_effects = []

        if treatment.side_effects_probability > 0.1:
            if treatment.modality == TreatmentModality.PHARMACOLOGICAL:
                side_effects.append("Gastrointestinal upset")

                if "Renal disease" in comorbidities:
                    side_effects.append("Worsened renal function")

            elif treatment.modality == TreatmentModality.SURGICAL:
                side_effects.append("Post-operative pain")
                side_effects.append("Surgical site infection risk")

                if patient_age > 8:
                    side_effects.append("Prolonged recovery")

        if patient_age > 12:
            side_effects.append("Age-related anesthesia risk")

        return side_effects

    def _determine_timeline(self, onset_days: float) -> str:
        """Determine expected timeline for treatment effect."""
        if onset_days == 0:
            return "immediate"
        elif onset_days <= 1:
            return "hours"
        elif onset_days <= 7:
            return "days"
        elif onset_days <= 30:
            return "weeks"
        else:
            return "months"

    def _calculate_confidence_interval(self,
                                      probability: float,
                                      disease: str) -> Tuple[float, float]:
        """Calculate 95% confidence interval."""
        import math

        # Standard error for proportions
        se = math.sqrt(probability * (1 - probability) / 50)  # 50 assumed sample size

        # 95% CI uses z ≈ 1.96
        margin = 1.96 * se

        lower = max(0, probability - margin)
        upper = min(1, probability + margin)

        return (lower, upper)

    def _get_alternative_treatments(self, disease: str, current_treatment: str) -> List[str]:
        """Get alternative treatment options."""
        options = TreatmentKnowledgeBase.get_treatment_options(disease)
        alternatives = [
            o.name for o in options
            if o.name != current_treatment
        ]
        return alternatives[:3]  # Return top 3 alternatives

    def _assess_risk_benefit(self,
                            success_prob: float,
                            side_effect_prob: float,
                            disease_severity: float) -> str:
        """Assess risk-benefit ratio."""
        # Risk = side effect probability + disease severity factor
        risk = side_effect_prob + (disease_severity * 0.05)

        # Benefit = success probability
        benefit = success_prob

        if benefit > 0.7 and risk < 0.3:
            return "favorable"
        elif benefit > 0.5 and risk < 0.5:
            return "balanced"
        else:
            return "unfavorable"

    def _get_monitoring_requirements(self, treatment: TreatmentOption) -> List[str]:
        """Determine monitoring requirements for treatment."""
        monitoring = []

        if treatment.modality == TreatmentModality.PHARMACOLOGICAL:
            monitoring.append("Periodic liver/kidney function tests")
            monitoring.append("Monitor for adverse reactions")

        elif treatment.modality == TreatmentModality.SURGICAL:
            monitoring.append("Post-operative wound checks")
            monitoring.append("Pain assessment")

        elif treatment.modality == TreatmentModality.NUTRITIONAL:
            monitoring.append("Weight and body condition")
            monitoring.append("Appetite and food tolerance")

        elif treatment.modality == TreatmentModality.PHYSICAL_THERAPY:
            monitoring.append("Mobility and pain level")
            monitoring.append("Exercise tolerance")

        return monitoring

    def _calculate_confidence(self, disease: str, treatment_name: str) -> float:
        """Calculate confidence level for prediction."""
        # Base confidence
        confidence = 0.7

        treatment = TreatmentKnowledgeBase.get_treatment(disease, treatment_name)
        if treatment:
            # Increase if high evidence level
            if treatment.evidence_level == "high":
                confidence += 0.2
            elif treatment.evidence_level == "moderate":
                confidence += 0.1

        return min(1.0, confidence)

    def _generate_recommendations(self,
                                 treatment: TreatmentOption,
                                 success_prob: float,
                                 compliance: float,
                                 comorbidities: List[str]) -> List[str]:
        """Generate clinical recommendations."""
        recommendations = []

        if success_prob > 0.7:
            recommendations.append("Strongly recommended for this patient")
        elif success_prob > 0.5:
            recommendations.append("Consider as primary treatment option")
        else:
            recommendations.append("Consider as adjunctive therapy only")

        if compliance < 0.5:
            recommendations.append("Verify owner compliance before initiating")

        for contraindication in treatment.contraindications:
            if contraindication.lower() in [c.lower() for c in comorbidities]:
                recommendations.append(
                    f"Use caution due to {contraindication.lower()}"
                )

        return recommendations

    def record_outcome(self,
                      disease: str,
                      treatment_name: str,
                      success: bool):
        """Record actual treatment outcome for learning.

        Args:
            disease: Disease name
            treatment_name: Treatment used
            success: Whether treatment was successful
        """
        self.outcome_history.append((disease, treatment_name, success))

    def get_treatment_statistics(self) -> Dict:
        """Get statistics about treatment outcomes."""
        if not self.outcome_history:
            return {"total_outcomes": 0}

        total = len(self.outcome_history)
        successful = sum(1 for _, _, success in self.outcome_history if success)

        # Group by treatment
        treatment_stats = {}
        for disease, treatment, success in self.outcome_history:
            key = (disease, treatment)
            if key not in treatment_stats:
                treatment_stats[key] = {"total": 0, "successful": 0}

            treatment_stats[key]["total"] += 1
            if success:
                treatment_stats[key]["successful"] += 1

        return {
            "total_outcomes": total,
            "success_rate": round(successful / total, 4) if total > 0 else 0,
            "treatment_outcomes": treatment_stats,
        }

    def to_dict(self) -> Dict:
        """Export predictor state."""
        return {
            "predictions_made": len(self.predictions),
            "outcomes_recorded": len(self.outcome_history),
            "statistics": self.get_treatment_statistics(),
        }
