#!/usr/bin/env python3
"""
TRIPOD-compliant Diagnostic Accuracy Validation Framework

Implements transparent evaluation of VetDict diagnostic engine using TRIPOD guidelines.

TRIPOD focuses on:
1. Sensitivity: TP / (TP + FN) — true positive rate
2. Specificity: TN / (TN + FP) — true negative rate
3. PPV (Positive Predictive Value): TP / (TP + FP)
4. NPV (Negative Predictive Value): TN / (TN + FN)
5. Accuracy: (TP + TN) / (TP + TN + FP + FN)
6. F1-Score: 2 * (Precision * Recall) / (Precision + Recall)

Test Case Format:
{
    "case_id": "cat_URI_001",
    "species": "Cat",
    "primary_disease": "Upper Respiratory Infection",
    "symptoms": ["sneezing", "nasal_discharge", "fever"],
    "expected_rank": 1,  # position in diagnosis list
    "confidence_threshold": 0.80,  # minimum acceptable confidence
    "notes": "Classic URI presentation"
}

Metrics:
- Rank 1 Accuracy: percentage cases where true disease is #1 in differential
- Confidence Distribution: histogram of confidence scores
- Sensitivity by Species: per-species sensitivity
- Sensitivity by Symptom Count: 1-2 vs 3-5 vs 6+ symptoms
"""

import json
import logging
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ConfusionMatrix:
    """Confusion matrix components"""

    tp: int = 0  # True Positive
    tn: int = 0  # True Negative
    fp: int = 0  # False Positive
    fn: int = 0  # False Negative

    @property
    def total(self) -> int:
        return self.tp + self.tn + self.fp + self.fn

    @property
    def accuracy(self) -> float:
        """Accuracy = (TP + TN) / Total"""
        if self.total == 0:
            return 0.0
        return (self.tp + self.tn) / self.total

    @property
    def sensitivity(self) -> float:
        """Sensitivity = TP / (TP + FN) — true positive rate"""
        denominator = self.tp + self.fn
        if denominator == 0:
            return 0.0
        return self.tp / denominator

    @property
    def specificity(self) -> float:
        """Specificity = TN / (TN + FP) — true negative rate"""
        denominator = self.tn + self.fp
        if denominator == 0:
            return 0.0
        return self.tn / denominator

    @property
    def ppv(self) -> float:
        """PPV = TP / (TP + FP) — positive predictive value"""
        denominator = self.tp + self.fp
        if denominator == 0:
            return 0.0
        return self.tp / denominator

    @property
    def npv(self) -> float:
        """NPV = TN / (TN + FN) — negative predictive value"""
        denominator = self.tn + self.fn
        if denominator == 0:
            return 0.0
        return self.tn / denominator

    @property
    def f1_score(self) -> float:
        """F1-Score = 2 * (Precision * Recall) / (Precision + Recall)"""
        precision = self.ppv
        recall = self.sensitivity
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)

    def to_dict(self) -> Dict[str, float]:
        """Export metrics as dictionary"""
        return {
            "tp": self.tp,
            "tn": self.tn,
            "fp": self.fp,
            "fn": self.fn,
            "total": self.total,
            "accuracy": round(self.accuracy, 4),
            "sensitivity": round(self.sensitivity, 4),
            "specificity": round(self.specificity, 4),
            "ppv": round(self.ppv, 4),
            "npv": round(self.npv, 4),
            "f1_score": round(self.f1_score, 4),
        }


@dataclass
class DiagnosticTestCase:
    """Single diagnostic test case"""

    case_id: str
    species: str
    primary_disease: str  # Gold standard (true diagnosis)
    symptoms: List[str]
    expected_rank: int = 1  # Expected position in differential (1 = best)
    confidence_threshold: float = 0.80
    notes: str = ""

    # Results (populated after testing)
    predicted_rank: int = None
    confidence_score: float = None
    top_n_predictions: List[Tuple[str, float]] = None
    test_passed: bool = None

    def validate(self) -> bool:
        """Check if test case passed"""
        if self.predicted_rank is None or self.confidence_score is None:
            return False

        # Pass if:
        # 1. Predicted rank matches or better than expected, AND
        # 2. Confidence meets threshold
        return self.predicted_rank <= self.expected_rank and self.confidence_score >= self.confidence_threshold


class DiagnosticValidationFramework:
    """TRIPOD-compliant diagnostic validation framework"""

    def __init__(self):
        self.test_cases: List[DiagnosticTestCase] = []
        self.results: Dict[str, Any] = {}
        self.metrics_by_species: Dict[str, ConfusionMatrix] = defaultdict(ConfusionMatrix)
        self.metrics_by_symptom_count: Dict[str, ConfusionMatrix] = defaultdict(ConfusionMatrix)

    def add_test_case(self, case: DiagnosticTestCase) -> None:
        """Add a test case to the suite"""
        self.test_cases.append(case)

    def add_test_cases_from_json(self, json_path: str) -> None:
        """Load test cases from JSON file"""
        with open(json_path, "r", encoding="utf-8") as f:
            cases_data = json.load(f)

        for case_data in cases_data:
            case = DiagnosticTestCase(
                case_id=case_data["case_id"],
                species=case_data["species"],
                primary_disease=case_data["primary_disease"],
                symptoms=case_data["symptoms"],
                expected_rank=case_data.get("expected_rank", 1),
                confidence_threshold=case_data.get("confidence_threshold", 0.80),
                notes=case_data.get("notes", ""),
            )
            self.add_test_case(case)

    def record_result(
        self,
        case_id: str,
        predicted_rank: int,
        confidence_score: float,
        top_n_predictions: List[Tuple[str, float]] = None,
    ) -> None:
        """Record test result for a case"""
        for case in self.test_cases:
            if case.case_id == case_id:
                case.predicted_rank = predicted_rank
                case.confidence_score = confidence_score
                case.top_n_predictions = top_n_predictions or []
                case.test_passed = case.validate()
                break

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate all diagnostic accuracy metrics.

        Note: the test set contains only gold-standard positive cases (one
        correct disease per case), so there is no ground-truth "negative"
        population. Per-species confusion matrices therefore track only TP
        (test passed) and FN (test failed); specificity and NPV are
        structurally undefined and are reported alongside a more
        interpretable ``rank_1_accuracy`` field.
        """
        # Reset aggregators so the method is idempotent when called multiple
        # times on the same framework instance (e.g. in long-running scripts
        # or tests that record additional results after a first snapshot).
        self.metrics_by_species = defaultdict(ConfusionMatrix)
        self.metrics_by_symptom_count = defaultdict(ConfusionMatrix)

        results = {
            "total_cases": len(self.test_cases),
            "passed_cases": sum(1 for c in self.test_cases if c.test_passed),
            "failed_cases": sum(1 for c in self.test_cases if c.test_passed is False),
            "pass_rate": 0.0,
            "rank_1_accuracy": 0.0,
            "average_confidence": 0.0,
            "by_species": {},
            "by_symptom_count": {},
            "confusion_matrix": {},
        }

        if not self.test_cases:
            return results

        # Overall pass rate
        results["pass_rate"] = results["passed_cases"] / results["total_cases"]

        # Rank 1 accuracy
        rank_1_count = sum(1 for c in self.test_cases if c.predicted_rank == 1)
        results["rank_1_accuracy"] = rank_1_count / results["total_cases"]

        # Average confidence (include 0.0 scores; only skip not-yet-recorded)
        confidences = [c.confidence_score for c in self.test_cases if c.confidence_score is not None]
        if confidences:
            results["average_confidence"] = sum(confidences) / len(confidences)

        # Aggregate confusion matrix over the whole suite
        rank_1_counts_by_species: Dict[str, int] = defaultdict(int)
        rank_1_counts_by_symptom: Dict[str, int] = defaultdict(int)
        totals_by_species: Dict[str, int] = defaultdict(int)
        totals_by_symptom: Dict[str, int] = defaultdict(int)

        agg = ConfusionMatrix()
        for case in self.test_cases:
            if case.test_passed:
                agg.tp += 1
                self.metrics_by_species[case.species].tp += 1
            else:
                agg.fn += 1
                self.metrics_by_species[case.species].fn += 1

            symptom_category = self._categorize_symptom_count(len(case.symptoms))
            if case.test_passed:
                self.metrics_by_symptom_count[symptom_category].tp += 1
            else:
                self.metrics_by_symptom_count[symptom_category].fn += 1

            totals_by_species[case.species] += 1
            totals_by_symptom[symptom_category] += 1
            if case.predicted_rank == 1:
                rank_1_counts_by_species[case.species] += 1
                rank_1_counts_by_symptom[symptom_category] += 1

        results["confusion_matrix"] = agg.to_dict()

        def _with_rank1(cm_dict, passed, total):
            cm_dict["rank_1_accuracy"] = round(passed / total, 4) if total else 0.0
            return cm_dict

        for species, cm in self.metrics_by_species.items():
            results["by_species"][species] = _with_rank1(
                cm.to_dict(),
                rank_1_counts_by_species[species],
                totals_by_species[species],
            )

        for sym_cat, cm in self.metrics_by_symptom_count.items():
            results["by_symptom_count"][sym_cat] = _with_rank1(
                cm.to_dict(),
                rank_1_counts_by_symptom[sym_cat],
                totals_by_symptom[sym_cat],
            )

        return results

    @staticmethod
    def _categorize_symptom_count(count: int) -> str:
        """Categorize symptom count for subgroup analysis"""
        if count <= 2:
            return "minimal_symptoms"
        elif count <= 5:
            return "moderate_symptoms"
        else:
            return "comprehensive_symptoms"

    def generate_tripod_report(self) -> Dict[str, Any]:
        """Generate TRIPOD-compliant validation report"""
        metrics = self.calculate_metrics()

        report = {
            "title": "TRIPOD-Compliant Diagnostic Accuracy Assessment",
            "framework": "VetDict Diagnostic Engine",
            "evaluation_date": datetime.now().isoformat(),
            "test_design": {
                "type": "Prospective Cohort",
                "total_cases": metrics["total_cases"],
                "species_count": len(metrics["by_species"]),
                "gold_standard": "Clinical expert consensus",
            },
            "primary_outcomes": {
                "rank_1_accuracy": round(metrics["rank_1_accuracy"], 4),
                "pass_rate": round(metrics["pass_rate"], 4),
                "average_confidence": round(metrics["average_confidence"], 4),
            },
            "accuracy_metrics": metrics["confusion_matrix"],
            "subgroup_analysis": {
                "by_species": metrics["by_species"],
                "by_symptom_count": metrics["by_symptom_count"],
            },
            "interpretation": self._generate_interpretation(metrics),
        }

        return report

    @staticmethod
    def _generate_interpretation(metrics: Dict[str, Any]) -> str:
        """Generate plain-language interpretation of results"""
        rank_1 = metrics["rank_1_accuracy"]

        if rank_1 >= 0.90:
            return "Excellent diagnostic accuracy: 90%+ rank-1 accuracy achieved."
        elif rank_1 >= 0.80:
            return "Good diagnostic accuracy: 80-90% rank-1 accuracy demonstrated."
        elif rank_1 >= 0.70:
            return "Acceptable diagnostic accuracy: 70-80% rank-1 accuracy; room for improvement."
        else:
            return f"Suboptimal accuracy: {rank_1 * 100:.1f}% rank-1 accuracy; improvements needed."


if __name__ == "__main__":
    # Example usage
    framework = DiagnosticValidationFramework()
    print("✅ TRIPOD framework initialized")
