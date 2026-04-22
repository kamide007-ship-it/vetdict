#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 QA Validator

Validates enriched content for quality and medical accuracy.
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class Phase1QAValidator:
    """Validates Phase 1 enrichment quality."""

    def __init__(self, enriched_db_path=None):
        if enriched_db_path is None:
            # Find the most recent enriched database
            base_path = Path(__file__).parent.parent
            enriched_files = list(base_path.glob("diseases_enriched_phase1_*.json"))
            if not enriched_files:
                raise FileNotFoundError("No enriched database found. Run phase1_batch_processor.py first.")
            enriched_db_path = max(enriched_files)

        self.enriched_db_path = Path(enriched_db_path)
        self.original_db_path = Path(__file__).parent.parent / "diseases_all_species.json"
        self.qa_report_path = (
            Path(__file__).parent.parent / f"qa_report_phase1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

    def load_databases(self):
        """Load both original and enriched databases."""
        with open(self.enriched_db_path, "r", encoding="utf-8") as f:
            enriched = json.load(f)
        with open(self.original_db_path, "r", encoding="utf-8") as f:
            original = json.load(f)
        return original, enriched

    def check_field_presence(self, disease: Dict) -> Dict:
        """Check if all required fields are present."""
        fields = {
            "pathophysiology": disease.get("pathophysiology", ""),
            "pathophysiology_ja": disease.get("pathophysiology_ja", ""),
            "causes": disease.get("causes", ""),
            "causes_ja": disease.get("causes_ja", ""),
            "treatment": disease.get("treatment", ""),
            "treatment_ja": disease.get("treatment_ja", ""),
            "prevention": disease.get("prevention", ""),
            "prevention_ja": disease.get("prevention_ja", ""),
            "prognosis": disease.get("prognosis", ""),
            "prognosis_ja": disease.get("prognosis_ja", ""),
        }
        return {field: bool(value) for field, value in fields.items()}

    def check_field_length(self, disease: Dict) -> Dict:
        """Check if field lengths are reasonable (2-3 sentences)."""
        validations = {}
        for field in [
            "pathophysiology",
            "pathophysiology_ja",
            "causes",
            "causes_ja",
            "treatment",
            "treatment_ja",
            "prevention",
            "prevention_ja",
            "prognosis",
            "prognosis_ja",
        ]:
            value = disease.get(field, "")
            if not value:
                validations[field] = "empty"
            elif len(value) < 30:
                validations[field] = "too_short"
            elif len(value) > 1000:
                validations[field] = "too_long"
            else:
                validations[field] = "ok"
        return validations

    def check_bilingual_balance(self, disease: Dict) -> Dict:
        """Check if both English and Japanese versions exist."""
        pairs = [
            ("pathophysiology", "pathophysiology_ja"),
            ("causes", "causes_ja"),
            ("treatment", "treatment_ja"),
            ("prevention", "prevention_ja"),
            ("prognosis", "prognosis_ja"),
        ]
        balance = {}
        for en, ja in pairs:
            en_present = bool(disease.get(en))
            ja_present = bool(disease.get(ja))
            if en_present and ja_present:
                balance[en] = "balanced"
            elif en_present:
                balance[en] = "en_only"
            elif ja_present:
                balance[en] = "ja_only"
            else:
                balance[en] = "missing"
        return balance

    def check_medical_terminology(self, disease: Dict) -> List[str]:
        """Basic checks for medical terminology."""
        issues = []

        # Check for generic template language
        generic_phrases = [
            "is a disease",
            "can occur in",
            "symptoms may include",
            "treatment involves",
            "should be",
            "is important",
        ]

        for field in ["pathophysiology", "causes", "treatment", "prevention", "prognosis"]:
            value = disease.get(field)
            if not value or not isinstance(value, str):
                continue

            value_lower = value.lower()
            for phrase in generic_phrases:
                if phrase in value_lower:
                    issues.append(f"Generic language in {field}: '{phrase}'")

        return issues

    def validate_sample(self, diseases: List[Dict], sample_size: int = 50) -> Dict:
        """Validate a random sample of diseases."""
        phase1_diseases = [d for d in diseases if d.get("enrichment_phase") == 1]

        if not phase1_diseases:
            raise ValueError("No Phase 1 enriched diseases found.")

        sample_size = min(sample_size, len(phase1_diseases))
        sample = random.sample(phase1_diseases, sample_size)

        print(f"\nValidating sample of {sample_size} diseases...")
        print("-" * 70)

        results = {"total_sampled": sample_size, "passed": 0, "failed": 0, "issues": [], "details": {}}

        for i, disease in enumerate(sample, 1):
            disease_id = disease.get("id")
            disease_name = disease.get("name")

            # Run validation checks
            field_presence = self.check_field_presence(disease)
            field_length = self.check_field_length(disease)
            bilingual = self.check_bilingual_balance(disease)
            terminology_issues = self.check_medical_terminology(disease)

            # Calculate pass/fail
            fields_complete = sum(1 for v in field_presence.values() if v) == 10
            lengths_ok = all(v == "ok" for v in field_length.values())
            no_terminology_issues = len(terminology_issues) == 0

            passed = fields_complete and lengths_ok and no_terminology_issues

            if passed:
                results["passed"] += 1
                status = "✓"
            else:
                results["failed"] += 1
                status = "✗"
                results["issues"].append(
                    {
                        "disease_id": disease_id,
                        "disease_name": disease_name,
                        "field_presence": field_presence,
                        "field_lengths": field_length,
                        "terminology_issues": terminology_issues,
                    }
                )

            results["details"][disease_id] = {
                "name": disease_name,
                "status": "pass" if passed else "fail",
                "field_presence": field_presence,
                "field_lengths": field_length,
                "bilingual_balance": bilingual,
            }

            print(f"  {status} {i:2d}. {disease_name[:50]}")

        return results

    def run_qa_validation(self):
        """Execute QA validation."""
        print("=" * 70)
        print("PHASE 1 QA VALIDATOR")
        print("=" * 70)
        print(f"Start time: {datetime.now().isoformat()}\n")

        # Load databases
        print("[1/3] Loading databases...")
        original, enriched = self.load_databases()
        phase1_count = sum(1 for d in enriched if d.get("enrichment_phase") == 1)
        print(f"✓ Original database: {len(original)} diseases")
        print(f"✓ Enriched database: {len(enriched)} diseases")
        print(f"✓ Phase 1 enriched: {phase1_count} diseases")

        # Validate sample
        print("\n[2/3] Validating sample of Phase 1 diseases...")
        sample_results = self.validate_sample(enriched, sample_size=50)

        pass_rate = 100 * sample_results["passed"] / sample_results["total_sampled"]
        print("\n✓ Validation complete")
        print(f"  Passed: {sample_results['passed']}/{sample_results['total_sampled']} ({pass_rate:.1f}%)")
        print(f"  Failed: {sample_results['failed']}/{sample_results['total_sampled']}")

        # Generate report
        print("\n[3/3] Generating QA report...")
        report = {
            "timestamp": datetime.now().isoformat(),
            "validation_type": "Phase 1 QA",
            "sample_size": sample_results["total_sampled"],
            "pass_rate": pass_rate,
            "results": sample_results,
            "metrics": {
                "fields_completion": 100
                * len(
                    [
                        d
                        for d in enriched
                        if d.get("enrichment_phase") == 1
                        and all(
                            d.get(f)
                            for f in [
                                "pathophysiology",
                                "pathophysiology_ja",
                                "causes",
                                "causes_ja",
                                "treatment",
                                "treatment_ja",
                                "prevention",
                                "prevention_ja",
                                "prognosis",
                                "prognosis_ja",
                            ]
                        )
                    ]
                )
                / max(phase1_count, 1),
                "bilingual_coverage": 100
                * len(
                    [
                        d
                        for d in enriched
                        if d.get("enrichment_phase") == 1
                        and any(
                            d.get(en) and d.get(ja)
                            for en, ja in [
                                ("pathophysiology", "pathophysiology_ja"),
                                ("causes", "causes_ja"),
                                ("treatment", "treatment_ja"),
                                ("prevention", "prevention_ja"),
                                ("prognosis", "prognosis_ja"),
                            ]
                        )
                    ]
                )
                / max(phase1_count, 1),
            },
            "recommendations": self._generate_recommendations(sample_results),
        }

        # Save report
        with open(self.qa_report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"✓ QA report saved: {self.qa_report_path}")

        # Print summary
        print("\n" + "=" * 70)
        print("QA VALIDATION SUMMARY")
        print("=" * 70)
        print(f"\nPass Rate: {pass_rate:.1f}%")
        print("Threshold: 95% (PASS)" if pass_rate >= 95 else "Threshold: 95% (FAIL)")
        print("\nMetrics:")
        print(f"  - Fields Completion: {report['metrics']['fields_completion']:.1f}%")
        print(f"  - Bilingual Coverage: {report['metrics']['bilingual_coverage']:.1f}%")

        if sample_results["issues"]:
            print(f"\nIssues Found ({len(sample_results['issues'])}):")
            for issue in sample_results["issues"][:5]:
                print(f"  - {issue['disease_name'][:40]}")
                if issue["terminology_issues"]:
                    for term_issue in issue["terminology_issues"][:2]:
                        print(f"    • {term_issue}")

        print("\nNext steps:")
        if pass_rate >= 95:
            print("  ✓ Quality acceptable. Proceed with integration:")
            print("    python3 scripts/phase1_integration.py")
        else:
            print("  ✗ Quality below threshold. Manual review recommended.")

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        if results["failed"] > 5:
            recommendations.append("High error rate - consider manual review of failures")
        if len([i for i in results["issues"] if any(i["terminology_issues"])]) > 10:
            recommendations.append("Generic language detected - may need prompt refinement")
        if results["passed"] >= results["total_sampled"] * 0.95:
            recommendations.append("Quality acceptable - safe to integrate into main database")
        return recommendations


if __name__ == "__main__":
    validator = Phase1QAValidator()
    validator.run_qa_validation()
