#!/usr/bin/env python3
"""
TRIPOD-Compliant Diagnostic Accuracy Validation Tests

Tests the VetDict diagnostic engine against clinical test cases
using TRIPOD framework metrics.
"""

import json
from pathlib import Path

import pytest

from api.tripod_validation import (
    ConfusionMatrix,
    DiagnosticTestCase,
    DiagnosticValidationFramework,
)


@pytest.fixture
def tripod_framework():
    """Initialize TRIPOD validation framework"""
    return DiagnosticValidationFramework()


@pytest.fixture
def test_cases_json():
    """Load test cases from JSON"""
    test_file = Path(__file__).parent / 'tripod_test_cases.json'
    with open(test_file, 'r', encoding='utf-8') as f:
        return json.load(f)


class TestConfusionMatrix:
    """Test confusion matrix calculations"""

    def test_confusion_matrix_properties(self):
        """Test all confusion matrix properties"""
        cm = ConfusionMatrix(tp=80, tn=15, fp=5, fn=0)

        assert cm.total == 100
        assert cm.accuracy == 0.95
        assert cm.sensitivity == 1.0  # 80/(80+0)
        assert cm.specificity == 0.75  # 15/(15+5)
        assert cm.ppv == pytest.approx(0.9411, abs=0.001)  # 80/(80+5)
        assert cm.npv == 1.0  # 15/(15+0)

    def test_confusion_matrix_zero_division(self):
        """Test zero-division handling"""
        cm = ConfusionMatrix(tp=0, tn=0, fp=0, fn=0)

        assert cm.total == 0
        assert cm.accuracy == 0.0
        assert cm.sensitivity == 0.0
        assert cm.specificity == 0.0
        assert cm.ppv == 0.0
        assert cm.npv == 0.0
        assert cm.f1_score == 0.0

    def test_confusion_matrix_to_dict(self):
        """Test confusion matrix serialization"""
        cm = ConfusionMatrix(tp=70, tn=20, fp=8, fn=2)
        result = cm.to_dict()

        assert result['tp'] == 70
        assert result['tn'] == 20
        assert result['fp'] == 8
        assert result['fn'] == 2
        assert result['total'] == 100
        assert isinstance(result['accuracy'], float)
        assert 0 <= result['accuracy'] <= 1


class TestDiagnosticTestCase:
    """Test case validation"""

    def test_test_case_creation(self):
        """Test creation of diagnostic test case"""
        case = DiagnosticTestCase(
            case_id='cat_001',
            species='Cat',
            primary_disease='FHV-1',
            symptoms=['sneezing', 'nasal_discharge'],
            expected_rank=1,
            confidence_threshold=0.75,
        )

        assert case.case_id == 'cat_001'
        assert case.species == 'Cat'
        assert case.primary_disease == 'FHV-1'
        assert len(case.symptoms) == 2

    def test_test_case_validation_pass(self):
        """Test case validation when results meet criteria"""
        case = DiagnosticTestCase(
            case_id='cat_001',
            species='Cat',
            primary_disease='FHV-1',
            symptoms=['sneezing', 'nasal_discharge'],
            expected_rank=1,
            confidence_threshold=0.75,
        )

        # Record results
        case.predicted_rank = 1
        case.confidence_score = 0.80
        case.test_passed = case.validate()

        assert case.test_passed is True

    def test_test_case_validation_fail_low_confidence(self):
        """Test case validation when confidence is too low"""
        case = DiagnosticTestCase(
            case_id='cat_001',
            species='Cat',
            primary_disease='FHV-1',
            symptoms=['sneezing', 'nasal_discharge'],
            expected_rank=1,
            confidence_threshold=0.75,
        )

        # Record results with low confidence
        case.predicted_rank = 1
        case.confidence_score = 0.60
        case.test_passed = case.validate()

        assert case.test_passed is False

    def test_test_case_validation_fail_rank(self):
        """Test case validation when rank is too low"""
        case = DiagnosticTestCase(
            case_id='cat_001',
            species='Cat',
            primary_disease='FHV-1',
            symptoms=['sneezing', 'nasal_discharge'],
            expected_rank=1,
            confidence_threshold=0.75,
        )

        # Record results with poor rank
        case.predicted_rank = 3
        case.confidence_score = 0.80
        case.test_passed = case.validate()

        assert case.test_passed is False


class TestDiagnosticValidationFramework:
    """Test TRIPOD validation framework"""

    def test_framework_initialization(self, tripod_framework):
        """Test framework initialization"""
        assert len(tripod_framework.test_cases) == 0
        assert len(tripod_framework.metrics_by_species) == 0
        assert len(tripod_framework.metrics_by_symptom_count) == 0

    def test_add_test_case(self, tripod_framework):
        """Test adding a single test case"""
        case = DiagnosticTestCase(
            case_id='test_001',
            species='Dog',
            primary_disease='Parvovirus',
            symptoms=['fever', 'vomiting'],
        )

        tripod_framework.add_test_case(case)

        assert len(tripod_framework.test_cases) == 1
        assert tripod_framework.test_cases[0].case_id == 'test_001'

    def test_add_test_cases_from_json(self, tripod_framework, test_cases_json):
        """Test loading test cases from JSON"""
        tripod_framework.add_test_cases_from_json(
            Path(__file__).parent / 'tripod_test_cases.json'
        )

        assert len(tripod_framework.test_cases) > 0
        assert all(isinstance(case, DiagnosticTestCase) for case in tripod_framework.test_cases)

    def test_record_result(self, tripod_framework):
        """Test recording diagnostic results"""
        case = DiagnosticTestCase(
            case_id='test_001',
            species='Dog',
            primary_disease='Parvovirus',
            symptoms=['fever', 'vomiting'],
        )

        tripod_framework.add_test_case(case)
        tripod_framework.record_result(
            case_id='test_001',
            predicted_rank=1,
            confidence_score=0.85,
            top_n_predictions=[('Parvovirus', 0.85), ('Gastroenteritis', 0.60)],
        )

        recorded_case = tripod_framework.test_cases[0]
        assert recorded_case.predicted_rank == 1
        assert recorded_case.confidence_score == 0.85
        assert recorded_case.test_passed is True

    def test_calculate_metrics_empty(self, tripod_framework):
        """Test metrics calculation with no test cases"""
        metrics = tripod_framework.calculate_metrics()

        assert metrics['total_cases'] == 0
        assert metrics['passed_cases'] == 0
        assert metrics['failed_cases'] == 0
        assert metrics['pass_rate'] == 0.0
        assert metrics['rank_1_accuracy'] == 0.0

    def test_calculate_metrics_with_data(self, tripod_framework):
        """Test metrics calculation with test cases"""
        # Add 3 test cases
        for i in range(3):
            case = DiagnosticTestCase(
                case_id=f'test_{i:03d}',
                species='Dog' if i < 2 else 'Cat',
                primary_disease='Parvovirus',
                symptoms=['fever', 'vomiting'],
            )
            tripod_framework.add_test_case(case)

        # Record results: 2 pass, 1 fail
        tripod_framework.record_result('test_000', 1, 0.85)
        tripod_framework.record_result('test_001', 1, 0.80)
        tripod_framework.record_result('test_002', 2, 0.60)  # Fails (rank 2, low confidence)

        metrics = tripod_framework.calculate_metrics()

        assert metrics['total_cases'] == 3
        assert metrics['passed_cases'] == 2
        assert metrics['failed_cases'] == 1
        assert metrics['pass_rate'] == pytest.approx(0.6667, abs=0.01)
        assert metrics['rank_1_accuracy'] == pytest.approx(0.6667, abs=0.01)

    def test_symptom_count_categorization(self):
        """Test symptom count categorization"""
        framework = DiagnosticValidationFramework()

        assert framework._categorize_symptom_count(1) == 'minimal_symptoms'
        assert framework._categorize_symptom_count(2) == 'minimal_symptoms'
        assert framework._categorize_symptom_count(3) == 'moderate_symptoms'
        assert framework._categorize_symptom_count(5) == 'moderate_symptoms'
        assert framework._categorize_symptom_count(6) == 'comprehensive_symptoms'
        assert framework._categorize_symptom_count(10) == 'comprehensive_symptoms'

    def test_species_metrics_tracking(self, tripod_framework):
        """Test metrics tracking by species"""
        # Add cases for two species
        for species in ['Dog', 'Cat']:
            case = DiagnosticTestCase(
                case_id=f'{species}_001',
                species=species,
                primary_disease='Test Disease',
                symptoms=['fever', 'lethargy'],
            )
            tripod_framework.add_test_case(case)

        # Record results
        tripod_framework.record_result('Dog_001', 1, 0.85)
        tripod_framework.record_result('Cat_001', 2, 0.60)

        metrics = tripod_framework.calculate_metrics()

        assert 'Dog' in metrics['by_species']
        assert 'Cat' in metrics['by_species']
        assert metrics['by_species']['Dog']['tp'] == 1
        assert metrics['by_species']['Cat']['fn'] == 1

    def test_generate_tripod_report(self, tripod_framework):
        """Test TRIPOD report generation"""
        # Add test cases
        for i in range(5):
            case = DiagnosticTestCase(
                case_id=f'test_{i:03d}',
                species='Dog' if i < 3 else 'Cat',
                primary_disease='Parvovirus',
                symptoms=['fever', 'vomiting'],
            )
            tripod_framework.add_test_case(case)

        # Record results
        for i in range(3):
            tripod_framework.record_result(f'test_{i:03d}', 1, 0.80 + i * 0.05)

        for i in range(3, 5):
            tripod_framework.record_result(f'test_{i:03d}', 2, 0.60)

        report = tripod_framework.generate_tripod_report()

        assert report['title'] == 'TRIPOD-Compliant Diagnostic Accuracy Assessment'
        assert report['framework'] == 'VetDict Diagnostic Engine'
        assert 'evaluation_date' in report
        assert 'test_design' in report
        assert 'primary_outcomes' in report
        assert 'interpretation' in report

    def test_interpretation_generation(self, tripod_framework):
        """Test interpretation text generation"""
        # Test different accuracy levels
        metrics_excellent = {'rank_1_accuracy': 0.95}
        result = tripod_framework._generate_interpretation(metrics_excellent)
        assert '90%' in result

        metrics_good = {'rank_1_accuracy': 0.85}
        result = tripod_framework._generate_interpretation(metrics_good)
        assert '80-90%' in result

        metrics_acceptable = {'rank_1_accuracy': 0.75}
        result = tripod_framework._generate_interpretation(metrics_acceptable)
        assert '70-80%' in result

        metrics_poor = {'rank_1_accuracy': 0.60}
        result = tripod_framework._generate_interpretation(metrics_poor)
        assert 'Suboptimal' in result


class TestTripodTestDataIntegrity:
    """Validate test data integrity"""

    def test_test_cases_json_structure(self, test_cases_json):
        """Test that test cases JSON has proper structure"""
        assert isinstance(test_cases_json, list)
        assert len(test_cases_json) > 0

        required_fields = {'case_id', 'species', 'primary_disease', 'symptoms'}

        for case in test_cases_json:
            assert all(field in case for field in required_fields)
            assert isinstance(case['symptoms'], list)
            assert len(case['symptoms']) > 0
            assert 'expected_rank' in case
            assert 'confidence_threshold' in case

    def test_test_cases_species_coverage(self, test_cases_json):
        """Test coverage of different species"""
        species = {case['species'] for case in test_cases_json}

        # Should have at least 5 different species
        assert len(species) >= 5

    def test_test_cases_symptom_count_distribution(self, test_cases_json):
        """Test distribution of symptom counts"""
        minimal = sum(1 for case in test_cases_json if len(case['symptoms']) <= 2)
        moderate = sum(1 for case in test_cases_json if 3 <= len(case['symptoms']) <= 5)
        comprehensive = sum(1 for case in test_cases_json if len(case['symptoms']) >= 6)

        # Should have cases in all categories
        assert minimal > 0
        assert moderate > 0
        assert comprehensive > 0

    def test_expected_rank_validity(self, test_cases_json):
        """Test that expected ranks are valid"""
        for case in test_cases_json:
            assert 1 <= case['expected_rank'] <= 5
            assert 0.50 <= case['confidence_threshold'] <= 0.95


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
