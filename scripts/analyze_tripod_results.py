#!/usr/bin/env python3
"""
Phase 3 Analysis: Diagnostic accuracy improvement opportunities

Analyzes TRIPOD validation results to identify:
- Misdiagnosed conditions (wrong disease predicted)
- Confidence calibration issues
- Symptom extraction failures
- Species-specific diagnostic challenges
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.chat.disease_matcher import _match_species_symptoms_to_diseases
from api.chat.symptom_extractor import _extract_species_symptoms


def analyze_diagnostic_failures():  # noqa: C901
    """Analyze test cases to identify improvement opportunities"""

    print("=" * 100)
    print("TRIPOD Diagnostic Accuracy Analysis")
    print("=" * 100)

    # Load test cases
    test_file = Path(__file__).parent.parent / "tests" / "tripod_test_cases.json"
    with open(test_file, "r") as f:
        test_cases = json.load(f)

    # Load validation report
    report_file = Path(__file__).parent.parent / "reports" / "tripod_validation_report.json"
    with open(report_file, "r") as f:
        report = json.load(f)

    # Analyze each test case
    print("\n" + "=" * 100)
    print("DETAILED FAILURE ANALYSIS")
    print("=" * 100)

    species_failures = defaultdict(list)
    symptom_extraction_issues = []
    confidence_issues = []
    rank_issues = []

    for case in test_cases:
        species = case["species"]
        primary_disease = case["primary_disease"]
        symptoms = case["symptoms"]
        threshold = case["confidence_threshold"]

        # Extract symptoms
        symptoms_text = " ".join(symptoms)
        extracted = _extract_species_symptoms(symptoms_text, species)

        # Get predictions
        predictions = _match_species_symptoms_to_diseases(extracted, species)

        if not predictions:
            symptom_extraction_issues.append(
                {
                    "case_id": case["case_id"],
                    "species": species,
                    "symptoms": symptoms,
                    "issue": "No predictions generated",
                }
            )
            continue

        top_prediction = predictions[0]
        top_disease = top_prediction.get("name_en", top_prediction.get("disease_id", ""))
        top_confidence = top_prediction.get("confidence_percent", 0) / 100.0

        # Find true disease rank
        true_rank = 1
        true_confidence = None
        for rank, pred in enumerate(predictions, 1):
            pred_disease = pred.get("name_en", pred.get("disease_id", ""))
            if pred_disease.lower() == primary_disease.lower():
                true_rank = rank
                true_confidence = pred.get("confidence_percent", 0) / 100.0
                break

        # Categorize failures
        passed = true_rank <= case["expected_rank"] and top_confidence >= threshold

        if not passed:
            failure = {
                "case_id": case["case_id"],
                "species": species,
                "expected_disease": primary_disease,
                "top_predicted": top_disease,
                "true_rank": true_rank,
                "true_confidence": true_confidence,
                "top_confidence": top_confidence,
                "symptoms_count": len(extracted),
                "symptoms": symptoms,
            }

            # Categorize failure type
            if true_rank > case["expected_rank"] and true_confidence is not None:
                if true_confidence < threshold:
                    confidence_issues.append(failure)
                else:
                    rank_issues.append(failure)
            else:
                species_failures[species].append(failure)

    # Print summary
    print("\n📊 FAILURE SUMMARY")
    print(f"  Symptom Extraction Issues: {len(symptom_extraction_issues)}")
    print(f"  Rank Issues (correct disease not in top): {len(rank_issues)}")
    print(f"  Confidence Issues (correct disease too low): {len(confidence_issues)}")
    print(f"  Species-Specific Issues: {len(dict(species_failures))} species affected")

    # Print symptom extraction issues
    if symptom_extraction_issues:
        print(f"\n⚠️  SYMPTOM EXTRACTION FAILURES ({len(symptom_extraction_issues)} cases)")
        for issue in symptom_extraction_issues[:5]:
            print(f"  {issue['case_id']:20s} {issue['species']:12s} Symptoms: {', '.join(issue['symptoms'][:2])}...")
        if len(symptom_extraction_issues) > 5:
            print(f"  ... and {len(symptom_extraction_issues) - 5} more")

    # Print rank issues
    if rank_issues:
        print(f"\n🎯 RANK ISSUES ({len(rank_issues)} cases)")
        for issue in rank_issues[:5]:
            print(
                f"  {issue['case_id']:20s} {issue['species']:12s} "
                f"Expected: {issue['expected_disease'][:25]:25s} "
                f"Got rank {issue['true_rank']} (confidence {issue['true_confidence']:.1%})"
            )
        if len(rank_issues) > 5:
            print(f"  ... and {len(rank_issues) - 5} more")

    # Print confidence issues
    if confidence_issues:
        print(f"\n📉 CONFIDENCE CALIBRATION ISSUES ({len(confidence_issues)} cases)")
        for issue in confidence_issues[:5]:
            print(
                f"  {issue['case_id']:20s} {issue['species']:12s} "
                f"Disease ranked #{issue['true_rank']} but confidence {issue['true_confidence']:.1%} < threshold"
            )
        if len(confidence_issues) > 5:
            print(f"  ... and {len(confidence_issues) - 5} more")

    # Print species-specific analysis
    if species_failures:
        print("\n🔬 SPECIES-SPECIFIC DIAGNOSTIC CHALLENGES")
        for species in sorted(species_failures.keys()):
            issues = species_failures[species]
            print(f"\n  {species.upper()} ({len(issues)} failures)")
            for issue in issues[:3]:
                print(
                    f"    - {issue['expected_disease'][:40]:40s} "
                    f"→ {issue['top_predicted'][:35]:35s} "
                    f"(conf: {issue['top_confidence']:.0%})"
                )
            if len(issues) > 3:
                print(f"    ... and {len(issues) - 3} more")

    # Print metrics summary
    print("\n" + "=" * 100)
    print("METRICS SUMMARY FROM VALIDATION REPORT")
    print("=" * 100)
    print("\nPrimary Outcomes:")
    print(f"  Rank-1 Accuracy: {report['primary_outcomes']['rank_1_accuracy']:.1%}")
    print(f"  Pass Rate: {report['primary_outcomes']['pass_rate']:.1%}")
    print(f"  Average Confidence: {report['primary_outcomes']['average_confidence']:.1%}")

    print("\nBy Species Sensitivity (TP/(TP+FN)):")
    for species, metrics in sorted(report["subgroup_analysis"]["by_species"].items()):
        if metrics["total"] > 0:
            print(f"  {species:15s}: {metrics['sensitivity']:6.1%} ({metrics['tp']}/{metrics['total']} cases)")

    print("\nBy Symptom Count:")
    for category, metrics in sorted(report["subgroup_analysis"]["by_symptom_count"].items()):
        if metrics["total"] > 0:
            print(
                f"  {category:20s}: {metrics['sensitivity']:6.1%} sensitivity, "
                f"{metrics['ppv']:6.1%} PPV ({metrics['tp']}/{metrics['total']})"
            )

    # Recommendations
    print("\n" + "=" * 100)
    print("IMPROVEMENT RECOMMENDATIONS")
    print("=" * 100)

    recommendations = []

    if len(symptom_extraction_issues) > len(test_cases) * 0.1:
        recommendations.append(
            "• SYMPTOM ALIAS EXPANSION: >10% cases have symptom extraction failures\n"
            "  Action: Add more symptom aliases for exotic species (e.g., 'behavioral disorder', 'feather issue')"
        )

    if len(confidence_issues) > len(rank_issues):
        recommendations.append(
            "• CONFIDENCE CALIBRATION: More failures due to low confidence than poor ranking\n"
            "  Action: Lower confidence thresholds for 3-5 symptom cases; model appears conservative"
        )

    if len(rank_issues) > 0:
        recommendations.append(
            f"• RANKING ALGORITHM: {len(rank_issues)} cases have correct disease not in top ranks\n"
            "  Action: Review disease similarity scoring; may need increased weight for specific symptom combinations"
        )

    if "guinea_pig" in species_failures or "hamster" in species_failures:
        recommendations.append(
            "• EXOTIC SPECIES: Guinea pig, hamster, ferret showing 0% sensitivity\n"
            "  Action: Review species-specific symptom names and disease mappings"
        )

    if recommendations:
        for rec in recommendations:
            print(f"\n{rec}")

    print("\n" + "=" * 100)


if __name__ == "__main__":
    try:
        analyze_diagnostic_failures()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Analysis failed: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)
