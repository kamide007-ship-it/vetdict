#!/usr/bin/env python3
"""
Phase 3-3: Run TRIPOD Diagnostic Accuracy Validation

Executes the diagnostic engine against test cases and generates
TRIPOD-compliant validation report.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.chat.disease_matcher import _match_species_symptoms_to_diseases
from api.chat.symptom_extractor import _extract_species_symptoms
from api.tripod_validation import DiagnosticValidationFramework


def run_diagnostic_validation():
    """Execute TRIPOD diagnostic accuracy validation"""

    print("=" * 80)
    print("TRIPOD-Compliant Diagnostic Accuracy Validation")
    print("=" * 80)

    # Initialize framework
    framework = DiagnosticValidationFramework()

    # Load test cases
    test_file = Path(__file__).parent.parent / 'tests' / 'tripod_test_cases.json'
    print(f"\nLoading test cases from: {test_file}")

    framework.add_test_cases_from_json(str(test_file))
    print(f"✓ Loaded {len(framework.test_cases)} test cases")

    # Run diagnostic engine for each test case
    print("\nExecuting diagnostic engine on all test cases...")
    passed_count = 0
    failed_count = 0

    for i, case in enumerate(framework.test_cases, 1):
        try:
            # Convert species to lowercase (dog, cat, etc.)
            species_lower = case.species.lower()

            # Extract symptoms for the specific species
            symptoms_text = ' '.join(case.symptoms)
            species_symptoms = _extract_species_symptoms(
                symptoms_text,
                species_lower,
            )

            # Match symptoms to diseases
            predictions = _match_species_symptoms_to_diseases(
                species_symptoms,
                species_lower,
            )

            if predictions:
                # Get top prediction confidence
                top_prediction = predictions[0]
                top_confidence = top_prediction.get('confidence_percent', 0) / 100.0
                predicted_rank = 1

                # Check if true disease is in predictions
                for rank, pred in enumerate(predictions, 1):
                    pred_disease = pred.get('name_en', pred.get('disease_id', ''))
                    if pred_disease.lower() == case.primary_disease.lower():
                        predicted_rank = rank
                        break

                # Create top-n predictions list (disease, confidence tuples)
                top_n = [
                    (p.get('name_en', p.get('disease_id', '')), p.get('confidence_percent', 0) / 100.0)
                    for p in predictions[:5]
                ]

                # Record result
                framework.record_result(
                    case_id=case.case_id,
                    predicted_rank=predicted_rank,
                    confidence_score=top_confidence,
                    top_n_predictions=top_n,
                )

                test_passed = case.test_passed
                if test_passed:
                    passed_count += 1
                    status = "✓"
                else:
                    failed_count += 1
                    status = "✗"

                # Print progress
                if i % 5 == 0:
                    print(
                        f"  [{i:3d}/{len(framework.test_cases)}] {status} "
                        f"{case.species:12s} {case.primary_disease[:30]:30s} "
                        f"rank={predicted_rank} conf={top_confidence:.2%}"
                    )
            else:
                failed_count += 1
                if i % 5 == 0:
                    print(
                        f"  [{i:3d}/{len(framework.test_cases)}] ✗ "
                        f"{case.species:12s} (No predictions)"
                    )

        except Exception as e:
            failed_count += 1
            if i % 10 == 0:
                print(f"  ERROR at [{i:3d}] {case.case_id}: {str(e)}")

    print("\n✓ Diagnostic engine execution complete")
    print(f"  Passed: {passed_count}")
    print(f"  Failed: {failed_count}")

    # Calculate metrics
    print("\nCalculating TRIPOD metrics...")
    metrics = framework.calculate_metrics()

    print(f"\n  Total Cases: {metrics['total_cases']}")
    print(f"  Passed Cases: {metrics['passed_cases']}")
    print(f"  Pass Rate: {metrics['pass_rate']:.1%}")
    print(f"  Rank-1 Accuracy: {metrics['rank_1_accuracy']:.1%}")
    print(f"  Average Confidence: {metrics['average_confidence']:.2%}")

    # Print species-specific metrics
    if metrics['by_species']:
        print("\n  By Species:")
        for species, cm_dict in metrics['by_species'].items():
            print(
                f"    {species:15s}: "
                f"sensitivity={cm_dict['sensitivity']:.2%} "
                f"specificity={cm_dict['specificity']:.2%} "
                f"ppv={cm_dict['ppv']:.2%}"
            )

    # Print symptom count metrics
    if metrics['by_symptom_count']:
        print("\n  By Symptom Count:")
        for sym_cat, cm_dict in metrics['by_symptom_count'].items():
            print(
                f"    {sym_cat:20s}: "
                f"sensitivity={cm_dict['sensitivity']:.2%} "
                f"ppv={cm_dict['ppv']:.2%}"
            )

    # Generate TRIPOD report
    print("\nGenerating TRIPOD-compliant report...")
    report = framework.generate_tripod_report()

    # Save report
    report_file = Path(__file__).parent.parent / 'reports' / 'tripod_validation_report.json'
    report_file.parent.mkdir(parents=True, exist_ok=True)

    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"✓ Report saved to: {report_file}")

    # Print report summary
    print("\n" + "=" * 80)
    print("TRIPOD Validation Report Summary")
    print("=" * 80)
    print(f"\nFramework: {report['framework']}")
    print(f"Test Design: {report['test_design']['type']}")
    print(f"Total Cases: {report['test_design']['total_cases']}")
    print(f"Species Count: {report['test_design']['species_count']}")
    print("\nPrimary Outcomes:")
    print(f"  Rank-1 Accuracy: {report['primary_outcomes']['rank_1_accuracy']:.1%}")
    print(f"  Pass Rate: {report['primary_outcomes']['pass_rate']:.1%}")
    print(f"  Average Confidence: {report['primary_outcomes']['average_confidence']:.2%}")
    print(f"\nInterpretation: {report['interpretation']}")
    print("\n" + "=" * 80)

    return report


if __name__ == '__main__':
    try:
        report = run_diagnostic_validation()
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ TRIPOD validation failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
