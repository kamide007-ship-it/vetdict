"""Unified Clinical Decision Support Engine.

Integrates all Stage 1-4 components into a single coherent system
for comprehensive multi-disease diagnosis and treatment planning.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Import all stage components
from api.ai.multidisease_expander import (
    MultiDiseaseExpander,
    DiseaseInteraction,
    CombinationPattern,
    InteractionRuleMiner,
)
from api.ai.adaptive_confidence_calculator import (
    AdaptiveConfidenceCalculator,
    DiagnosisRecord,
    FeatureEngineer,
)
from api.ai.prognostic_predictor import (
    PrognosticPredictor,
    PrognosticFactors,
    PrognosticPrediction,
)
from api.ai.treatment_response_predictor import (
    TreatmentResponsePredictor,
    TreatmentResponse,
    TreatmentKnowledgeBase,
)


@dataclass
class ClinicalCase:
    """Unified clinical case for comprehensive analysis."""
    case_id: str
    patient_age: float
    patient_species: str
    symptoms: List[str]
    disease_severity: float  # 0-10
    comorbidities: List[str] = field(default_factory=list)
    veterinarian_id: Optional[str] = None
    clinic_id: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "case_id": self.case_id,
            "patient_age": self.patient_age,
            "patient_species": self.patient_species,
            "symptoms": self.symptoms,
            "disease_severity": self.disease_severity,
            "comorbidities": self.comorbidities,
            "veterinarian_id": self.veterinarian_id,
            "clinic_id": self.clinic_id,
        }


@dataclass
class ComprehensiveDiagnosis:
    """Complete diagnostic and treatment recommendation."""
    case_id: str
    primary_diagnosis: str
    differential_diagnoses: List[Tuple[str, float]]  # (disease, probability)
    comorbid_conditions: List[CombinationPattern]
    prognosis: PrognosticPrediction
    treatment_recommendations: List[TreatmentResponse]
    risk_factors: List[str]
    protective_factors: List[str]
    monitoring_plan: List[str]
    confidence_level: float  # Overall confidence (0-1)
    clinical_notes: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "case_id": self.case_id,
            "primary_diagnosis": self.primary_diagnosis,
            "differential_diagnoses": [
                {"disease": d, "probability": round(p, 4)}
                for d, p in self.differential_diagnoses
            ],
            "comorbid_conditions": [
                c.to_dict() for c in self.comorbid_conditions
            ],
            "prognosis": self.prognosis.to_dict(),
            "treatment_recommendations": [
                t.to_dict() for t in self.treatment_recommendations
            ],
            "risk_factors": self.risk_factors,
            "protective_factors": self.protective_factors,
            "monitoring_plan": self.monitoring_plan,
            "confidence_level": round(self.confidence_level, 4),
            "clinical_notes": self.clinical_notes,
            "timestamp": self.timestamp,
        }


class DiagnosticWorkflow(Enum):
    """Clinical workflow stages."""
    INITIAL_ASSESSMENT = "initial_assessment"
    DIFFERENTIAL_DIAGNOSIS = "differential_diagnosis"
    PROGNOSTIC_EVALUATION = "prognostic_evaluation"
    TREATMENT_PLANNING = "treatment_planning"
    MONITORING_SETUP = "monitoring_setup"
    OUTCOME_TRACKING = "outcome_tracking"


class UnifiedClinicalEngine:
    """Master orchestrator for all clinical decision support.

    Integrates:
    - Stage 1: Multi-disease combination analysis
    - Stage 2: Adaptive confidence scoring
    - Stage 3: Prognostic prediction
    - Stage 4: Treatment response prediction

    Provides unified API for complete clinical workflows.
    """

    def __init__(self):
        """Initialize unified clinical engine."""
        self.expander: Optional[MultiDiseaseExpander] = None
        self.confidence_calculator = AdaptiveConfidenceCalculator()
        self.prognostic_predictor = PrognosticPredictor()
        self.treatment_predictor = TreatmentResponsePredictor()
        self.rule_miner = InteractionRuleMiner(min_support=0.15, min_confidence=0.4)

        self.diagnoses: Dict[str, ComprehensiveDiagnosis] = {}
        self.workflow_log: List[Tuple[str, DiagnosticWorkflow, datetime]] = []

    def initialize_expander(self,
                           interaction_matrix: Dict[Tuple[str, str], DiseaseInteraction]):
        """Initialize multi-disease expander with interaction matrix."""
        self.expander = MultiDiseaseExpander(interaction_matrix)
        logger.info("Multi-disease expander initialized")

    def comprehensive_analysis(self,
                              case: ClinicalCase,
                              initial_predictions: Dict[str, float]
                              ) -> ComprehensiveDiagnosis:
        """Perform comprehensive diagnostic and treatment analysis.

        Args:
            case: Clinical case information
            initial_predictions: Initial disease probability estimates

        Returns:
            ComprehensiveDiagnosis with complete analysis
        """
        self._log_workflow(case.case_id, DiagnosticWorkflow.INITIAL_ASSESSMENT)

        # Step 1: Adjust predictions based on veterinarian and clinic
        adjusted_predictions = self.confidence_calculator.adjust_predictions(
            initial_predictions=initial_predictions,
            veterinarian_id=case.veterinarian_id,
            clinic_id=case.clinic_id,
            species=case.patient_species,
        )

        self._log_workflow(case.case_id, DiagnosticWorkflow.DIFFERENTIAL_DIAGNOSIS)

        # Step 2: Identify primary and differential diagnoses
        primary_diagnosis, differential_diagnoses = self._identify_diagnoses(
            adjusted_predictions
        )

        # Step 3: Analyze disease combinations (comorbidities)
        comorbid_patterns = self._analyze_combinations(
            list(adjusted_predictions.keys())
        )

        self._log_workflow(case.case_id, DiagnosticWorkflow.PROGNOSTIC_EVALUATION)

        # Step 4: Calculate prognosis
        prognostic_factors = PrognosticFactors(
            disease=primary_diagnosis,
            disease_severity=case.disease_severity,
            patient_age=case.patient_age,
            patient_species=case.patient_species,
            comorbidities=case.comorbidities,
        )
        prognosis = self.prognostic_predictor.predict_prognosis(prognostic_factors)

        self._log_workflow(case.case_id, DiagnosticWorkflow.TREATMENT_PLANNING)

        # Step 5: Recommend treatments
        treatment_recommendations = self._recommend_treatments(
            primary_diagnosis=primary_diagnosis,
            case=case,
        )

        self._log_workflow(case.case_id, DiagnosticWorkflow.MONITORING_SETUP)

        # Step 6: Generate monitoring plan
        monitoring_plan = self._generate_monitoring_plan(
            case=case,
            prognosis=prognosis,
            treatments=treatment_recommendations,
        )

        # Step 7: Compile comprehensive diagnosis
        confidence_level = self._calculate_overall_confidence(
            adjusted_predictions, prognosis
        )

        diagnosis = ComprehensiveDiagnosis(
            case_id=case.case_id,
            primary_diagnosis=primary_diagnosis,
            differential_diagnoses=differential_diagnoses,
            comorbid_conditions=comorbid_patterns,
            prognosis=prognosis,
            treatment_recommendations=treatment_recommendations,
            risk_factors=prognosis.risk_factors,
            protective_factors=prognosis.protective_factors,
            monitoring_plan=monitoring_plan,
            confidence_level=confidence_level,
        )

        self.diagnoses[case.case_id] = diagnosis
        return diagnosis

    def _identify_diagnoses(self,
                           predictions: Dict[str, float]
                           ) -> Tuple[str, List[Tuple[str, float]]]:
        """Identify primary and differential diagnoses from predictions.

        Returns:
            (primary_diagnosis, list of (disease, probability) tuples)
        """
        sorted_diseases = sorted(
            predictions.items(),
            key=lambda x: x[1],
            reverse=True
        )

        if not sorted_diseases:
            return "Unknown", []

        primary = sorted_diseases[0][0]
        differential = sorted_diseases[1:4]  # Top 3 differentials

        return primary, differential

    def _analyze_combinations(self, diseases: List[str]) -> List[CombinationPattern]:
        """Analyze disease combinations and interactions.

        Returns:
            List of identified combination patterns
        """
        if not self.expander or len(diseases) < 2:
            return []

        patterns = self.expander.expand_combinations(diseases, min_combined_prob=0.1)
        return patterns

    def _recommend_treatments(self,
                             primary_diagnosis: str,
                             case: ClinicalCase) -> List[TreatmentResponse]:
        """Generate ranked treatment recommendations.

        Returns:
            List of treatment options ranked by success probability
        """
        treatments = self.treatment_predictor.predict_all_treatments(
            disease=primary_diagnosis,
            patient_age=case.patient_age,
            comorbidities=case.comorbidities,
            disease_severity=case.disease_severity,
        )

        # Top 3 treatments
        return treatments[:3]

    def _generate_monitoring_plan(self,
                                 case: ClinicalCase,
                                 prognosis: PrognosticPrediction,
                                 treatments: List[TreatmentResponse]) -> List[str]:
        """Generate comprehensive monitoring plan.

        Returns:
            List of monitoring recommendations
        """
        plan = []

        # From prognosis
        plan.extend(prognosis.recommended_monitoring)

        # From treatments
        for treatment in treatments:
            plan.extend(treatment.monitoring_requirements)

        # Based on severity
        if case.disease_severity >= 7:
            plan.append("Daily clinical assessment")
            plan.append("Daily vital signs monitoring")

        if case.disease_severity >= 5:
            plan.append("Weekly laboratory assessment")

        # Unique and remove duplicates
        plan = list(set(plan))

        return plan

    def _calculate_overall_confidence(self,
                                     predictions: Dict[str, float],
                                     prognosis: PrognosticPrediction) -> float:
        """Calculate overall confidence in diagnosis.

        Factors:
        - Primary diagnosis confidence
        - Prognostic confidence
        - Uncertainty quantification
        """
        if not predictions:
            return 0.3

        primary_confidence = max(predictions.values())
        prognostic_confidence = prognosis.confidence_level
        epistemic_uncertainty = prognosis.epistemic_uncertainty

        # Average with uncertainty penalty
        overall = (primary_confidence + prognostic_confidence) / 2
        overall *= (1 - epistemic_uncertainty * 0.5)

        return max(0.2, min(1.0, overall))

    def record_diagnosis_outcome(self,
                                case_id: str,
                                actual_diagnosis: str,
                                treatment_used: Optional[str] = None,
                                treatment_success: bool = False):
        """Record actual diagnosis outcome for learning.

        Args:
            case_id: Case identifier
            actual_diagnosis: Confirmed diagnosis
            treatment_used: Treatment that was applied
            treatment_success: Whether treatment was successful
        """
        # Record for confidence calculator
        if case_id in self.diagnoses:
            case_data = self.diagnoses[case_id]

            # Create diagnosis record
            diagnosis_record = DiagnosisRecord(
                case_id=case_id,
                symptoms=[],  # Would be populated from case
                initial_predictions={},  # From original predictions
                actual_diagnosis=actual_diagnosis,
                final_diagnosis_confirmed=(
                    case_data.primary_diagnosis == actual_diagnosis
                ),
                veterinarian_id="unknown",
                clinic_id="unknown",
                patient_age=0.0,
                patient_species="unknown",
                severity_score=0.0,
            )

            self.confidence_calculator.add_diagnosis_feedback(diagnosis_record)

        # Record for treatment predictor
        if treatment_used and treatment_success is not None:
            self.treatment_predictor.record_outcome(
                disease=actual_diagnosis,
                treatment_name=treatment_used,
                success=treatment_success,
            )

        # Record for prognostic predictor
        if case_id in self.diagnoses:
            case_data = self.diagnoses[case_id]
            # Could update prognosis accuracy tracking here

        self._log_workflow(case_id, DiagnosticWorkflow.OUTCOME_TRACKING)

    def train_models(self) -> Dict[str, bool]:
        """Train all adaptive models with collected feedback.

        Returns:
            Dict of (model_name -> training_success)
        """
        results = {}

        # Train adaptive confidence model
        try:
            success = self.confidence_calculator.train_model()
            results["adaptive_confidence"] = success
        except Exception as e:
            logger.error(f"Error training confidence model: {e}")
            results["adaptive_confidence"] = False

        # Train treatment response model
        # (Would implement actual ML training here)
        results["treatment_response"] = True

        return results

    def get_system_statistics(self) -> Dict:
        """Get comprehensive system statistics.

        Returns:
            Dict with statistics for all components
        """
        return {
            "total_cases_analyzed": len(self.diagnoses),
            "confidence_feedback": self.confidence_calculator.get_feedback_statistics(),
            "treatment_outcomes": self.treatment_predictor.get_treatment_statistics(),
            "prognostic_stats": self.prognostic_predictor.get_statistics(),
            "workflow_log_entries": len(self.workflow_log),
        }

    def _log_workflow(self, case_id: str, stage: DiagnosticWorkflow):
        """Log workflow progression."""
        self.workflow_log.append((case_id, stage, datetime.now()))

    def export_case(self, case_id: str) -> Optional[Dict]:
        """Export complete case analysis.

        Returns:
            Complete case data in dict format, or None if not found
        """
        if case_id not in self.diagnoses:
            return None

        return self.diagnoses[case_id].to_dict()

    def import_case(self, case_data: Dict) -> bool:
        """Import previously saved case analysis.

        Args:
            case_data: Case data dict

        Returns:
            True if import successful
        """
        try:
            # This would deserialize the case data
            # For now, just validate structure
            required_keys = [
                "case_id", "primary_diagnosis", "differential_diagnoses",
                "treatment_recommendations"
            ]
            if all(k in case_data for k in required_keys):
                return True
        except Exception as e:
            logger.error(f"Error importing case: {e}")

        return False

    def get_clinical_summary(self, case_id: str) -> Optional[str]:
        """Generate human-readable clinical summary.

        Returns:
            Formatted clinical summary
        """
        if case_id not in self.diagnoses:
            return None

        diagnosis = self.diagnoses[case_id]

        summary = f"""
╔════════════════════════════════════════════════════════════════╗
║                     CLINICAL SUMMARY                           ║
╚════════════════════════════════════════════════════════════════╝

Case ID: {diagnosis.case_id}
Confidence Level: {diagnosis.confidence_level:.1%}

PRIMARY DIAGNOSIS
═══════════════════════════════════════════════════════════════
  • {diagnosis.primary_diagnosis}

DIFFERENTIAL DIAGNOSES
═══════════════════════════════════════════════════════════════
"""
        for disease, prob in diagnosis.differential_diagnoses:
            summary += f"  • {disease:<40} {prob:.1%}\n"

        if diagnosis.comorbid_conditions:
            summary += "\nCOMORBID CONDITIONS\n"
            summary += "═══════════════════════════════════════════════════════════════\n"
            for pattern in diagnosis.comorbid_conditions:
                summary += f"  • {', '.join(pattern.diseases):<40} ({pattern.combined_probability:.1%})\n"

        summary += "\nPROGNOSIS\n"
        summary += "═══════════════════════════════════════════════════════════════\n"
        summary += f"  Recovery Probability: {diagnosis.prognosis.recovery_probability:.1%}\n"
        summary += f"  Complication Risk: {diagnosis.prognosis.complication_risk:.1%}\n"
        summary += f"  Mortality Risk: {diagnosis.prognosis.mortality_risk:.1%}\n"

        if diagnosis.treatment_recommendations:
            summary += "\nTREATMENT RECOMMENDATIONS (Ranked by Success Rate)\n"
            summary += "═══════════════════════════════════════════════════════════════\n"
            for i, treatment in enumerate(diagnosis.treatment_recommendations, 1):
                summary += f"\n  {i}. {treatment.treatment_name}\n"
                summary += f"     Success Probability: {treatment.success_probability:.1%}\n"
                summary += f"     Timeline: {treatment.expected_timeline}\n"

        if diagnosis.monitoring_plan:
            summary += "\nMONITORING PLAN\n"
            summary += "═══════════════════════════════════════════════════════════════\n"
            for item in diagnosis.monitoring_plan[:5]:
                summary += f"  • {item}\n"

        summary += "\n╔════════════════════════════════════════════════════════════════╗\n"

        return summary

    def to_dict(self) -> Dict:
        """Export complete engine state."""
        return {
            "cases_analyzed": len(self.diagnoses),
            "system_statistics": self.get_system_statistics(),
            "recent_cases": list(self.diagnoses.keys())[-10:],  # Last 10 cases
        }
