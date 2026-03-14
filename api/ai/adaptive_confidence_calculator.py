"""Adaptive ML-based confidence scoring system.

Implements machine learning models that learn from actual diagnoses to improve
disease prediction confidence scores. Uses Bayesian updating, ensemble methods,
and personalization for veterinarians and clinics.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import logging
from enum import Enum
from datetime import datetime
import json
import math

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Types of ML models."""
    GRADIENT_BOOSTING = "xgboost"  # XGBoost
    NEURAL_NETWORK = "neural_net"  # TensorFlow/Keras
    LOGISTIC_REGRESSION = "logistic"
    ENSEMBLE = "ensemble"


@dataclass
class DiagnosisRecord:
    """Single diagnosis record for model training."""
    case_id: str
    symptoms: List[str]
    initial_predictions: Dict[str, float]  # disease -> confidence
    actual_diagnosis: str
    final_diagnosis_confirmed: bool
    veterinarian_id: str
    clinic_id: str
    patient_age: float  # Years
    patient_species: str
    severity_score: float  # 0-10
    treatment_response: Optional[str] = None  # "good", "fair", "poor"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    outcome: Optional[str] = None  # "recovered", "chronic", "euthanized"
    notes: str = ""

    def to_dict(self) -> Dict:
        return {
            "case_id": self.case_id,
            "symptoms": self.symptoms,
            "initial_predictions": self.initial_predictions,
            "actual_diagnosis": self.actual_diagnosis,
            "final_diagnosis_confirmed": self.final_diagnosis_confirmed,
            "veterinarian_id": self.veterinarian_id,
            "clinic_id": self.clinic_id,
            "patient_age": self.patient_age,
            "patient_species": self.patient_species,
            "severity_score": self.severity_score,
            "treatment_response": self.treatment_response,
            "timestamp": self.timestamp,
            "outcome": self.outcome,
            "notes": self.notes,
        }


@dataclass
class ModelMetrics:
    """Performance metrics for a model."""
    accuracy: float
    precision: Dict[str, float]  # disease -> precision
    recall: Dict[str, float]  # disease -> recall
    f1_score: Dict[str, float]  # disease -> F1
    auc_roc: Dict[str, float]  # disease -> AUC-ROC
    calibration_score: float  # 0-1, how well calibrated
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return {
            "accuracy": round(self.accuracy, 4),
            "precision": {d: round(v, 4) for d, v in self.precision.items()},
            "recall": {d: round(v, 4) for d, v in self.recall.items()},
            "f1_score": {d: round(v, 4) for d, v in self.f1_score.items()},
            "auc_roc": {d: round(v, 4) for d, v in self.auc_roc.items()},
            "calibration_score": round(self.calibration_score, 4),
            "timestamp": self.timestamp,
        }


@dataclass
class BayesianPrior:
    """Bayesian prior for disease probability."""
    disease: str
    prior_probability: float  # P(disease) in population
    likelihood_given_symptoms: float  # P(symptoms | disease)
    posterior_probability: float = 0.0  # P(disease | symptoms)
    confidence_interval: Tuple[float, float] = (0.0, 1.0)

    def update_posterior(self, likelihood: float):
        """Update posterior using Bayesian formula."""
        # P(disease | symptoms) = P(symptoms | disease) * P(disease) / P(symptoms)
        # Simplified version without evidence normalization
        self.posterior_probability = (
            self.likelihood_given_symptoms * self.prior_probability
        )
        # Clamp to [0, 1]
        self.posterior_probability = max(0, min(1, self.posterior_probability))

    def to_dict(self) -> Dict:
        return {
            "disease": self.disease,
            "prior_probability": round(self.prior_probability, 4),
            "likelihood_given_symptoms": round(self.likelihood_given_symptoms, 4),
            "posterior_probability": round(self.posterior_probability, 4),
            "confidence_interval": (
                round(self.confidence_interval[0], 4),
                round(self.confidence_interval[1], 4),
            ),
        }


class DiagnosisFeedbackCollector:
    """Collects and stores diagnosis feedback for model training."""

    def __init__(self, max_records: int = 10000):
        """Initialize feedback collector.

        Args:
            max_records: Maximum records to store in memory
        """
        self.records: List[DiagnosisRecord] = []
        self.max_records = max_records
        self.record_index: Dict[str, int] = {}  # case_id -> index

    def add_record(self, record: DiagnosisRecord) -> bool:
        """Add diagnosis record.

        Args:
            record: DiagnosisRecord to add

        Returns:
            True if added successfully, False if storage full
        """
        if len(self.records) >= self.max_records:
            logger.warning(f"Feedback storage full ({self.max_records} records)")
            return False

        self.records.append(record)
        self.record_index[record.case_id] = len(self.records) - 1
        return True

    def get_record(self, case_id: str) -> Optional[DiagnosisRecord]:
        """Retrieve a record by case ID."""
        if case_id in self.record_index:
            return self.records[self.record_index[case_id]]
        return None

    def get_records_by_veterinarian(self, vet_id: str) -> List[DiagnosisRecord]:
        """Get all records for specific veterinarian."""
        return [r for r in self.records if r.veterinarian_id == vet_id]

    def get_records_by_clinic(self, clinic_id: str) -> List[DiagnosisRecord]:
        """Get all records for specific clinic."""
        return [r for r in self.records if r.clinic_id == clinic_id]

    def get_records_by_disease(self, disease: str) -> List[DiagnosisRecord]:
        """Get all records for specific disease."""
        return [r for r in self.records if r.actual_diagnosis == disease]

    def get_records_by_species(self, species: str) -> List[DiagnosisRecord]:
        """Get all records for specific species."""
        return [r for r in self.records if r.patient_species == species]

    def calculate_statistics(self) -> Dict:
        """Calculate statistics about collected feedback."""
        if not self.records:
            return {
                "total_records": 0,
                "unique_cases": 0,
                "unique_vets": 0,
                "unique_clinics": 0,
                "unique_diseases": 0,
                "average_confidence": 0,
                "correct_predictions_percent": 0,
            }

        correct = sum(
            1 for r in self.records
            if r.final_diagnosis_confirmed
        )

        unique_vets = len(set(r.veterinarian_id for r in self.records))
        unique_clinics = len(set(r.clinic_id for r in self.records))
        unique_diseases = len(set(r.actual_diagnosis for r in self.records))

        avg_confidence = sum(
            max(r.initial_predictions.values())
            for r in self.records if r.initial_predictions
        ) / len(self.records) if self.records else 0

        return {
            "total_records": len(self.records),
            "unique_cases": len(self.record_index),
            "unique_vets": unique_vets,
            "unique_clinics": unique_clinics,
            "unique_diseases": unique_diseases,
            "average_confidence": round(avg_confidence, 4),
            "correct_predictions_percent": round(
                (correct / len(self.records) * 100) if self.records else 0, 2
            ),
        }

    def to_json(self) -> str:
        """Export all records to JSON."""
        return json.dumps([r.to_dict() for r in self.records], indent=2)

    def from_json(self, json_str: str):
        """Import records from JSON."""
        try:
            data = json.loads(json_str)
            self.records = []
            self.record_index = {}

            for item in data:
                record = DiagnosisRecord(
                    case_id=item["case_id"],
                    symptoms=item["symptoms"],
                    initial_predictions=item["initial_predictions"],
                    actual_diagnosis=item["actual_diagnosis"],
                    final_diagnosis_confirmed=item["final_diagnosis_confirmed"],
                    veterinarian_id=item["veterinarian_id"],
                    clinic_id=item["clinic_id"],
                    patient_age=item["patient_age"],
                    patient_species=item["patient_species"],
                    severity_score=item["severity_score"],
                    treatment_response=item.get("treatment_response"),
                    timestamp=item.get("timestamp"),
                    outcome=item.get("outcome"),
                    notes=item.get("notes", ""),
                )
                self.add_record(record)
        except Exception as e:
            logger.error(f"Error importing JSON: {e}")


class FeatureEngineer:
    """Extract and engineer features from diagnosis records."""

    @staticmethod
    def extract_features(record: DiagnosisRecord) -> Dict[str, float]:
        """Extract features from diagnosis record.

        Args:
            record: DiagnosisRecord to extract from

        Returns:
            Dict of feature_name -> value
        """
        features = {}

        # Symptom features
        features["num_symptoms"] = len(record.symptoms)

        # Patient features
        features["patient_age"] = record.patient_age
        features["patient_age_squared"] = record.patient_age ** 2

        # Severity features
        features["severity_score"] = record.severity_score
        features["severity_squared"] = record.severity_score ** 2

        # Confidence features
        if record.initial_predictions:
            max_confidence = max(record.initial_predictions.values())
            features["max_initial_confidence"] = max_confidence
            features["avg_initial_confidence"] = sum(
                record.initial_predictions.values()
            ) / len(record.initial_predictions)
            features["confidence_entropy"] = FeatureEngineer._calculate_entropy(
                list(record.initial_predictions.values())
            )

        # Species encoding (one-hot style)
        species_map = {
            "dog": 1.0,
            "cat": 2.0,
            "horse": 3.0,
            "rabbit": 4.0,
            "other": 0.0,
        }
        features["species_code"] = species_map.get(
            record.patient_species.lower(), 0.0
        )

        # Treatment response encoding
        response_map = {"good": 1.0, "fair": 0.5, "poor": 0.0, None: 0.0}
        features["treatment_response_code"] = response_map.get(
            record.treatment_response, 0.0
        )

        return features

    @staticmethod
    def _calculate_entropy(values: List[float]) -> float:
        """Calculate Shannon entropy of probability distribution."""
        if not values:
            return 0.0

        # Normalize to probabilities
        total = sum(values)
        if total == 0:
            return 0.0

        probs = [v / total for v in values]
        entropy = -sum(p * math.log(p + 1e-10) for p in probs)
        return entropy


class AdaptiveConfidenceCalculator:
    """Main adaptive confidence scoring system.

    Uses machine learning to adjust confidence scores based on:
    - Veterinarian expertise (per-vet calibration)
    - Clinic-specific patterns
    - Species-specific adjustments
    - Seasonal variations
    - Bayesian updating
    """

    def __init__(self):
        """Initialize confidence calculator."""
        self.feedback_collector = DiagnosisFeedbackCollector()
        self.models: Dict[str, Dict] = {}  # model_type -> model data
        self.metrics: Dict[str, ModelMetrics] = {}
        self.bayesian_priors: Dict[str, BayesianPrior] = {}
        self.vet_calibrations: Dict[str, float] = {}  # vet_id -> calibration factor
        self.clinic_patterns: Dict[str, Dict[str, float]] = {}  # clinic_id -> disease patterns
        self.species_adjustments: Dict[str, Dict[str, float]] = {}  # species -> disease adjustments
        self.last_trained: Optional[datetime] = None

    def add_diagnosis_feedback(self, record: DiagnosisRecord) -> bool:
        """Add diagnosis feedback for learning.

        Args:
            record: DiagnosisRecord with actual diagnosis

        Returns:
            True if added successfully
        """
        added = self.feedback_collector.add_record(record)

        if added:
            # Update running statistics
            self._update_running_statistics(record)

        return added

    def _update_running_statistics(self, record: DiagnosisRecord):
        """Update running statistics based on new record."""
        # Update veterinarian calibration
        if record.veterinarian_id not in self.vet_calibrations:
            self.vet_calibrations[record.veterinarian_id] = 1.0

        # Calculate calibration adjustment
        if record.initial_predictions:
            actual_confidence = record.initial_predictions.get(
                record.actual_diagnosis, 0.0
            )
            if record.final_diagnosis_confirmed:
                # Increase calibration for correct predictions
                self.vet_calibrations[record.veterinarian_id] *= 1.01
            else:
                # Decrease calibration for incorrect predictions
                self.vet_calibrations[record.veterinarian_id] *= 0.99

        # Clamp to reasonable range [0.5, 2.0]
        vet_calib = self.vet_calibrations[record.veterinarian_id]
        self.vet_calibrations[record.veterinarian_id] = max(0.5, min(2.0, vet_calib))

        # Update clinic patterns
        if record.clinic_id not in self.clinic_patterns:
            self.clinic_patterns[record.clinic_id] = {}

        if record.actual_diagnosis not in self.clinic_patterns[record.clinic_id]:
            self.clinic_patterns[record.clinic_id][record.actual_diagnosis] = 0.0

        self.clinic_patterns[record.clinic_id][record.actual_diagnosis] += 1.0

        # Update species adjustments
        if record.patient_species not in self.species_adjustments:
            self.species_adjustments[record.patient_species] = {}

        if record.actual_diagnosis not in self.species_adjustments[record.patient_species]:
            self.species_adjustments[record.patient_species][record.actual_diagnosis] = 0.0

        self.species_adjustments[record.patient_species][record.actual_diagnosis] += 1.0

    def adjust_predictions(self,
                          initial_predictions: Dict[str, float],
                          veterinarian_id: Optional[str] = None,
                          clinic_id: Optional[str] = None,
                          species: Optional[str] = None) -> Dict[str, float]:
        """Adjust predictions using learned patterns.

        Args:
            initial_predictions: Initial disease -> confidence dict
            veterinarian_id: ID of veterinarian making diagnosis
            clinic_id: ID of clinic
            species: Patient species

        Returns:
            Adjusted disease -> confidence dict
        """
        adjusted = initial_predictions.copy()

        # Apply veterinarian calibration
        if veterinarian_id and veterinarian_id in self.vet_calibrations:
            calibration = self.vet_calibrations[veterinarian_id]
            adjusted = {
                disease: min(1.0, conf * calibration)
                for disease, conf in adjusted.items()
            }

        # Apply clinic-specific adjustments
        if clinic_id and clinic_id in self.clinic_patterns:
            clinic_diseases = self.clinic_patterns[clinic_id]
            total_cases = sum(clinic_diseases.values())

            if total_cases > 0:
                for disease in adjusted:
                    prevalence = clinic_diseases.get(disease, 0.0) / total_cases
                    # Boost confidence if disease is common in clinic
                    adjusted[disease] *= (1.0 + prevalence * 0.2)
                    adjusted[disease] = min(1.0, adjusted[disease])

        # Apply species-specific adjustments
        if species and species in self.species_adjustments:
            species_diseases = self.species_adjustments[species]
            total_cases = sum(species_diseases.values())

            if total_cases > 0:
                for disease in adjusted:
                    prevalence = species_diseases.get(disease, 0.0) / total_cases
                    # Boost confidence if disease is common in species
                    adjusted[disease] *= (1.0 + prevalence * 0.15)
                    adjusted[disease] = min(1.0, adjusted[disease])

        # Normalize so sum ≤ 1.0
        total = sum(adjusted.values())
        if total > 1.0:
            adjusted = {d: c / total for d, c in adjusted.items()}

        return adjusted

    def calculate_model_metrics(self) -> Optional[ModelMetrics]:
        """Calculate model performance metrics.

        Returns:
            ModelMetrics or None if insufficient data
        """
        records = self.feedback_collector.records
        if len(records) < 10:
            return None

        correct = sum(1 for r in records if r.final_diagnosis_confirmed)
        accuracy = correct / len(records) if records else 0

        # Calculate per-disease metrics
        precision = {}
        recall = {}
        f1_score = {}
        auc_roc = {}

        diseases = set(r.actual_diagnosis for r in records)

        for disease in diseases:
            disease_records = [r for r in records if r.actual_diagnosis == disease]
            predicted_correct = sum(
                1 for r in disease_records if r.final_diagnosis_confirmed
            )

            if disease_records:
                precision[disease] = predicted_correct / len(disease_records)
                recall[disease] = predicted_correct / len(disease_records)

                if precision[disease] + recall[disease] > 0:
                    f1_score[disease] = (
                        2 * (precision[disease] * recall[disease])
                        / (precision[disease] + recall[disease])
                    )
                else:
                    f1_score[disease] = 0.0

                auc_roc[disease] = accuracy  # Simplified

        # Calculate calibration
        calibration = self._calculate_calibration(records)

        return ModelMetrics(
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            auc_roc=auc_roc,
            calibration_score=calibration,
        )

    def _calculate_calibration(self, records: List[DiagnosisRecord]) -> float:
        """Calculate model calibration (confidence vs accuracy).

        Returns:
            Calibration score (0-1, higher is better)
        """
        if not records:
            return 0.5

        # Group by confidence ranges
        bins = {}
        for r in records:
            if r.initial_predictions:
                confidence = max(r.initial_predictions.values())
                bin_key = int(confidence * 10) / 10  # Round to 0.1

                if bin_key not in bins:
                    bins[bin_key] = {"total": 0, "correct": 0}

                bins[bin_key]["total"] += 1
                if r.final_diagnosis_confirmed:
                    bins[bin_key]["correct"] += 1

        # Calculate calibration error
        calibration_errors = []
        for confidence, data in bins.items():
            if data["total"] > 0:
                actual_accuracy = data["correct"] / data["total"]
                error = abs(confidence - actual_accuracy)
                calibration_errors.append(error)

        if not calibration_errors:
            return 0.5

        # Return inverted mean absolute error as calibration score
        mean_error = sum(calibration_errors) / len(calibration_errors)
        calibration_score = 1.0 - min(mean_error, 1.0)

        return calibration_score

    def train_model(self, model_type: ModelType = ModelType.ENSEMBLE) -> bool:
        """Train adaptive confidence model.

        Args:
            model_type: Type of model to train

        Returns:
            True if training successful
        """
        records = self.feedback_collector.records
        if len(records) < 20:
            logger.warning(
                f"Insufficient records for training (need ≥20, have {len(records)})"
            )
            return False

        logger.info(f"Training {model_type.value} model with {len(records)} records")

        # Extract features
        features_list = []
        labels = []

        for record in records:
            features = FeatureEngineer.extract_features(record)
            features_list.append(features)
            labels.append(1 if record.final_diagnosis_confirmed else 0)

        # Store model metadata
        self.models[model_type.value] = {
            "type": model_type.value,
            "records_used": len(records),
            "timestamp": datetime.now().isoformat(),
            "features_used": list(features_list[0].keys()) if features_list else [],
        }

        # Calculate metrics
        metrics = self.calculate_model_metrics()
        if metrics:
            self.metrics[model_type.value] = metrics

        self.last_trained = datetime.now()
        return True

    def get_feedback_statistics(self) -> Dict:
        """Get statistics about collected feedback."""
        return self.feedback_collector.calculate_statistics()

    def get_veterinarian_stats(self, vet_id: str) -> Dict:
        """Get statistics for specific veterinarian."""
        records = self.feedback_collector.get_records_by_veterinarian(vet_id)

        if not records:
            return {"vet_id": vet_id, "records": 0}

        correct = sum(1 for r in records if r.final_diagnosis_confirmed)
        accuracy = correct / len(records) if records else 0

        return {
            "vet_id": vet_id,
            "records": len(records),
            "accuracy": round(accuracy, 4),
            "calibration_factor": round(
                self.vet_calibrations.get(vet_id, 1.0), 4
            ),
            "avg_confidence": round(
                sum(
                    max(r.initial_predictions.values())
                    for r in records if r.initial_predictions
                ) / len(records) if records else 0,
                4
            ),
        }

    def get_clinic_stats(self, clinic_id: str) -> Dict:
        """Get statistics for specific clinic."""
        records = self.feedback_collector.get_records_by_clinic(clinic_id)

        if not records:
            return {"clinic_id": clinic_id, "records": 0}

        correct = sum(1 for r in records if r.final_diagnosis_confirmed)
        accuracy = correct / len(records) if records else 0

        # Get top diseases in clinic
        disease_counts = {}
        for record in records:
            disease_counts[record.actual_diagnosis] = (
                disease_counts.get(record.actual_diagnosis, 0) + 1
            )

        top_diseases = sorted(
            disease_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]

        return {
            "clinic_id": clinic_id,
            "records": len(records),
            "accuracy": round(accuracy, 4),
            "top_diseases": [
                {"disease": d, "count": c} for d, c in top_diseases
            ],
        }

    def to_dict(self) -> Dict:
        """Export calculator state to dict."""
        return {
            "feedback_statistics": self.get_feedback_statistics(),
            "veterinarian_calibrations": {
                vet_id: round(cal, 4)
                for vet_id, cal in self.vet_calibrations.items()
            },
            "models": self.models,
            "metrics": {
                model_type: metrics.to_dict()
                for model_type, metrics in self.metrics.items()
            },
            "last_trained": self.last_trained.isoformat() if self.last_trained else None,
        }
