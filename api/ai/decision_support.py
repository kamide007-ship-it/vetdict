"""Advanced Decision Support Engine (Stage 6).

Synthesizes outputs from risk stratification, prognosis, and treatment
predictions into actionable clinical decision guidance: referral
recommendations, follow-up scheduling, alert generation, and clinical
pathway selection.
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

from api.ai.prognostic_predictor import PrognosticPrediction
from api.ai.risk_stratifier import (
    RiskStratificationResult,
    RiskTier,
)
from api.ai.treatment_response_predictor import TreatmentResponse

logger = logging.getLogger(__name__)


class ClinicalPathway(Enum):
    """Recommended clinical care pathway."""

    OUTPATIENT_CONSERVATIVE = "outpatient_conservative"
    OUTPATIENT_ACTIVE = "outpatient_active"
    DAY_HOSPITAL = "day_hospital"
    INPATIENT = "inpatient"
    EMERGENCY = "emergency"
    PALLIATIVE = "palliative"


class AlertSeverity(Enum):
    """Clinical alert severity levels."""

    INFO = "info"
    WARNING = "warning"
    URGENT = "urgent"
    CRITICAL = "critical"


@dataclass
class ClinicalAlert:
    """A clinical alert or flag for veterinary staff."""

    severity: AlertSeverity
    message: str
    category: str  # e.g. "risk", "treatment", "follow-up"

    def to_dict(self) -> Dict:
        return {
            "severity": self.severity.value,
            "message": self.message,
            "category": self.category,
        }


@dataclass
class FollowUpSchedule:
    """Recommended follow-up schedule."""

    next_visit_days: int
    visit_type: str  # e.g. "recheck", "lab_only", "full_exam"
    recurring_interval_days: Optional[int] = None
    duration_weeks: Optional[int] = None
    notes: str = ""

    def to_dict(self) -> Dict:
        return {
            "next_visit_days": self.next_visit_days,
            "visit_type": self.visit_type,
            "recurring_interval_days": self.recurring_interval_days,
            "duration_weeks": self.duration_weeks,
            "notes": self.notes,
        }


@dataclass
class DecisionSupportResult:
    """Complete decision support output."""

    clinical_pathway: ClinicalPathway
    alerts: List[ClinicalAlert] = field(default_factory=list)
    follow_up: Optional[FollowUpSchedule] = None
    referral_recommended: bool = False
    referral_reason: str = ""
    hospitalization_recommended: bool = False
    owner_instructions: List[str] = field(default_factory=list)
    clinical_summary: str = ""

    def to_dict(self) -> Dict:
        return {
            "clinical_pathway": self.clinical_pathway.value,
            "alerts": [a.to_dict() for a in self.alerts],
            "follow_up": self.follow_up.to_dict() if self.follow_up else None,
            "referral_recommended": self.referral_recommended,
            "referral_reason": self.referral_reason,
            "hospitalization_recommended": self.hospitalization_recommended,
            "owner_instructions": self.owner_instructions,
            "clinical_summary": self.clinical_summary,
        }


# ── Pathway selection rules ─────────────────────────────────────────

PATHWAY_RULES: Dict[RiskTier, ClinicalPathway] = {
    RiskTier.LOW: ClinicalPathway.OUTPATIENT_CONSERVATIVE,
    RiskTier.MODERATE: ClinicalPathway.OUTPATIENT_ACTIVE,
    RiskTier.HIGH: ClinicalPathway.INPATIENT,
    RiskTier.CRITICAL: ClinicalPathway.EMERGENCY,
}

# ── Follow-up defaults by tier ──────────────────────────────────────

FOLLOW_UP_DEFAULTS: Dict[RiskTier, Dict] = {
    RiskTier.LOW: {
        "next_visit_days": 14,
        "visit_type": "recheck",
        "recurring_interval_days": 28,
        "duration_weeks": 8,
    },
    RiskTier.MODERATE: {
        "next_visit_days": 7,
        "visit_type": "full_exam",
        "recurring_interval_days": 14,
        "duration_weeks": 12,
    },
    RiskTier.HIGH: {
        "next_visit_days": 3,
        "visit_type": "full_exam",
        "recurring_interval_days": 7,
        "duration_weeks": 12,
    },
    RiskTier.CRITICAL: {
        "next_visit_days": 1,
        "visit_type": "full_exam",
        "recurring_interval_days": 2,
        "duration_weeks": 8,
    },
}

# ── Owner instruction templates ─────────────────────────────────────

_OWNER_INSTRUCTIONS: Dict[RiskTier, List[str]] = {
    RiskTier.LOW: [
        "Continue medications as prescribed",
        "Monitor appetite and energy levels",
        "Return if symptoms worsen",
    ],
    RiskTier.MODERATE: [
        "Administer all medications on schedule",
        "Keep a daily symptom log",
        "Restrict activity as instructed",
        "Contact clinic if new symptoms appear",
    ],
    RiskTier.HIGH: [
        "Follow treatment plan strictly",
        "Monitor temperature twice daily",
        "Keep a detailed symptom and appetite log",
        "Call the clinic immediately if condition deteriorates",
        "Prepare for possible hospitalization",
    ],
    RiskTier.CRITICAL: [
        "Follow all emergency care instructions",
        "Ensure 24-hour observation",
        "Have emergency clinic contact readily available",
        "Transport to emergency facility if any worsening observed",
    ],
}


class DecisionSupportEngine:
    """Generates advanced clinical decision support from prior-stage outputs."""

    def generate_decision_support(
        self,
        risk_result: RiskStratificationResult,
        prognosis: PrognosticPrediction,
        treatments: List[TreatmentResponse],
        disease: str,
        disease_severity: float,
        patient_age: float,
    ) -> DecisionSupportResult:
        """
        Synthesize risk, prognosis and treatment data into clinical decisions.

        Args:
            risk_result: Output from RiskStratifier
            prognosis: Output from PrognosticPredictor
            treatments: Ranked treatment options
            disease: Primary diagnosed disease
            disease_severity: Severity 0-10
            patient_age: Patient age in years

        Returns:
            DecisionSupportResult with pathway, alerts, follow-up, etc.
        """
        tier = risk_result.risk_tier

        # 1. Select clinical pathway
        pathway = self._select_pathway(tier, prognosis, disease_severity)

        # 2. Generate alerts
        alerts = self._generate_alerts(risk_result, prognosis, treatments, disease_severity)

        # 3. Build follow-up schedule
        follow_up = self._build_follow_up(tier, disease, prognosis)

        # 4. Determine referral need
        referral_recommended, referral_reason = self._assess_referral(tier, prognosis, disease_severity)

        # 5. Hospitalization recommendation
        hospitalization = self._assess_hospitalization(risk_result, prognosis)

        # 6. Owner instructions
        owner_instructions = self._generate_owner_instructions(tier, disease, treatments)

        # 7. Clinical summary
        summary = self._generate_summary(disease, tier, pathway, prognosis, treatments)

        return DecisionSupportResult(
            clinical_pathway=pathway,
            alerts=alerts,
            follow_up=follow_up,
            referral_recommended=referral_recommended,
            referral_reason=referral_reason,
            hospitalization_recommended=hospitalization,
            owner_instructions=owner_instructions,
            clinical_summary=summary,
        )

    @staticmethod
    def _select_pathway(
        tier: RiskTier,
        prognosis: PrognosticPrediction,
        disease_severity: float,
    ) -> ClinicalPathway:
        """Select clinical pathway, adjusting for edge cases."""
        base = PATHWAY_RULES[tier]

        # Override: very poor prognosis → palliative regardless of tier
        if prognosis.mortality_risk > 0.6 and prognosis.recovery_probability < 0.2:
            return ClinicalPathway.PALLIATIVE

        # Override: moderate tier + high severity → day hospital
        if tier == RiskTier.MODERATE and disease_severity >= 7:
            return ClinicalPathway.DAY_HOSPITAL

        return base

    @staticmethod
    def _generate_alerts(
        risk_result: RiskStratificationResult,
        prognosis: PrognosticPrediction,
        treatments: List[TreatmentResponse],
        disease_severity: float,
    ) -> List[ClinicalAlert]:
        """Generate clinical alerts based on all inputs."""
        alerts: List[ClinicalAlert] = []

        # Risk-based alerts
        if risk_result.risk_tier == RiskTier.CRITICAL:
            alerts.append(
                ClinicalAlert(
                    severity=AlertSeverity.CRITICAL,
                    message="Patient classified as CRITICAL risk — immediate intervention required",
                    category="risk",
                )
            )
        elif risk_result.risk_tier == RiskTier.HIGH:
            alerts.append(
                ClinicalAlert(
                    severity=AlertSeverity.URGENT,
                    message="Patient classified as HIGH risk — close monitoring required",
                    category="risk",
                )
            )

        # Hospitalization alert
        if risk_result.hospitalization_risk > 0.7:
            alerts.append(
                ClinicalAlert(
                    severity=AlertSeverity.URGENT,
                    message=f"High hospitalization probability ({risk_result.hospitalization_risk:.0%})",
                    category="risk",
                )
            )

        # Mortality alert
        if prognosis.mortality_risk > 0.3:
            alerts.append(
                ClinicalAlert(
                    severity=AlertSeverity.CRITICAL,
                    message=f"Elevated mortality risk ({prognosis.mortality_risk:.0%})",
                    category="prognosis",
                )
            )

        # Low recovery alert
        if prognosis.recovery_probability < 0.3:
            alerts.append(
                ClinicalAlert(
                    severity=AlertSeverity.WARNING,
                    message=f"Low recovery probability ({prognosis.recovery_probability:.0%})",
                    category="prognosis",
                )
            )

        # Treatment concern: no high-success options
        if treatments and all(t.success_probability < 0.4 for t in treatments):
            alerts.append(
                ClinicalAlert(
                    severity=AlertSeverity.WARNING,
                    message="No treatment option exceeds 40% success probability",
                    category="treatment",
                )
            )

        # Severity alert
        if disease_severity >= 9:
            alerts.append(
                ClinicalAlert(
                    severity=AlertSeverity.URGENT,
                    message=f"Very high disease severity ({disease_severity}/10)",
                    category="risk",
                )
            )

        return alerts

    @staticmethod
    def _build_follow_up(
        tier: RiskTier,
        disease: str,
        prognosis: PrognosticPrediction,
    ) -> FollowUpSchedule:
        """Build follow-up schedule from tier defaults + adjustments."""
        defaults = FOLLOW_UP_DEFAULTS[tier]
        notes = f"Follow-up for {disease}"

        # Adjust if chronic condition
        if prognosis.recovery_probability < 0.4:
            notes += " — chronic management may be needed"

        return FollowUpSchedule(
            next_visit_days=defaults["next_visit_days"],
            visit_type=defaults["visit_type"],
            recurring_interval_days=defaults["recurring_interval_days"],
            duration_weeks=defaults["duration_weeks"],
            notes=notes,
        )

    @staticmethod
    def _assess_referral(
        tier: RiskTier,
        prognosis: PrognosticPrediction,
        disease_severity: float,
    ) -> Tuple[bool, str]:
        """Determine if specialist referral is recommended."""
        if tier == RiskTier.CRITICAL:
            return True, "Critical risk tier warrants specialist consultation"

        if tier == RiskTier.HIGH and disease_severity >= 8:
            return True, "High risk with severe disease — specialist recommended"

        if prognosis.mortality_risk > 0.4:
            return True, "Elevated mortality risk requires specialist evaluation"

        return False, ""

    @staticmethod
    def _assess_hospitalization(
        risk_result: RiskStratificationResult,
        prognosis: PrognosticPrediction,
    ) -> bool:
        """Determine if hospitalization is recommended."""
        if risk_result.risk_tier == RiskTier.CRITICAL:
            return True
        if risk_result.hospitalization_risk > 0.65:
            return True
        return prognosis.mortality_risk > 0.4

    @staticmethod
    def _generate_owner_instructions(
        tier: RiskTier,
        disease: str,
        treatments: List[TreatmentResponse],
    ) -> List[str]:
        """Generate take-home instructions for pet owners."""
        instructions = list(_OWNER_INSTRUCTIONS[tier])

        if treatments:
            top = treatments[0]
            instructions.insert(0, f"Primary treatment: {top.treatment_name}")

        instructions.append(f"Diagnosis: {disease}")
        return instructions

    @staticmethod
    def _generate_summary(
        disease: str,
        tier: RiskTier,
        pathway: ClinicalPathway,
        prognosis: PrognosticPrediction,
        treatments: List[TreatmentResponse],
    ) -> str:
        """Generate a short clinical summary string."""
        treatment_str = treatments[0].treatment_name if treatments else "supportive care"
        return (
            f"{disease} — {tier.value.upper()} risk. "
            f"Pathway: {pathway.value.replace('_', ' ')}. "
            f"Recovery probability: {prognosis.recovery_probability:.0%}. "
            f"Recommended treatment: {treatment_str}."
        )
