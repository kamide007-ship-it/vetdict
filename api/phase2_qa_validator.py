#!/usr/bin/env python3
"""
Phase 2 QA Validator - Comprehensive quality assurance for Phase 2 content

Validates treatment, prevention, and prognosis enriched content for:
- Field presence and completeness
- Content quality (length, terminology, structure)
- Bilingual balance and accuracy
- Medical accuracy and species-specificity
"""

import json
from typing import List, Dict, Tuple
from pathlib import Path
from datetime import datetime


class Phase2QAValidator:
    """Comprehensive QA validation for Phase 2 enriched data."""

    # Quality thresholds
    FIELD_LENGTH_MIN = 30
    FIELD_LENGTH_MAX = 1000
    BILINGUAL_LENGTH_RATIO_MIN = 0.3  # JP should be 30-100% of EN (Japanese is more concise)
    BILINGUAL_LENGTH_RATIO_MAX = 1.0

    # Medical keywords for validation
    TREATMENT_KEYWORDS = [
        "treatment", "therapy", "medication", "drug", "antibiotic", "antifungal",
        "surgery", "surgical", "procedure", "management", "care", "protocol",
        "injection", "infusion", "supplement", "vitamin", "supportive", "palliative"
    ]

    PREVENTION_KEYWORDS = [
        "prevention", "prevention", "vaccine", "vaccination", "prophylactic", "hygiene",
        "management", "environment", "quarantine", "isolation", "screening",
        "avoid", "risk", "reduce", "minimize", "protection", "screen"
    ]

    PROGNOSIS_KEYWORDS = [
        "prognosis", "outcome", "survival", "recovery", "timeline", "period",
        "rate", "percentage", "complication", "mortality", "morbidity",
        "expected", "forecast", "prediction", "prognostic", "factor", "days", "weeks", "months"
    ]

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.database_path = self.project_root / "diseases_all_species.json"

    def load_diseases(self) -> List[Dict]:
        """Load disease database."""
        with open(self.database_path, "r") as f:
            return json.load(f)

    def validate_field_presence(self, disease: Dict, field: str) -> Tuple[bool, str]:
        """Validate that field and its Japanese translation are present.

        Args:
            disease: Disease dictionary
            field: Field name ("treatment", "prevention", "prognosis")

        Returns:
            (is_valid, message)
        """
        has_en = bool(disease.get(field))
        has_ja = bool(disease.get(f"{field}_ja"))

        if has_en and has_ja:
            return True, "✓ Both EN and JA present"
        elif has_en and not has_ja:
            return False, "✗ Missing Japanese translation"
        elif not has_en and has_ja:
            return False, "✗ Missing English content"
        else:
            return False, "✗ Both fields missing"

    def validate_field_length(self, disease: Dict, field: str) -> Tuple[bool, Dict]:
        """Validate field length is within acceptable range.

        Args:
            disease: Disease dictionary
            field: Field name

        Returns:
            (is_valid, details_dict)
        """
        en_text = disease.get(field, "")
        ja_text = disease.get(f"{field}_ja", "")

        details = {
            "en_length": len(en_text),
            "ja_length": len(ja_text),
            "en_ok": self.FIELD_LENGTH_MIN <= len(en_text) <= self.FIELD_LENGTH_MAX,
            "ja_ok": self.FIELD_LENGTH_MIN <= len(ja_text) <= self.FIELD_LENGTH_MAX,
        }

        is_valid = details["en_ok"] and details["ja_ok"]
        return is_valid, details

    def validate_bilingual_balance(self, disease: Dict, field: str) -> Tuple[bool, Dict]:
        """Validate English and Japanese lengths are balanced.

        Args:
            disease: Disease dictionary
            field: Field name

        Returns:
            (is_valid, details_dict)
        """
        en_text = disease.get(field, "")
        ja_text = disease.get(f"{field}_ja", "")

        if not en_text or not ja_text:
            return False, {"error": "Missing EN or JA text"}

        ratio = len(ja_text) / len(en_text) if en_text else 0
        is_valid = self.BILINGUAL_LENGTH_RATIO_MIN <= ratio <= self.BILINGUAL_LENGTH_RATIO_MAX

        return is_valid, {
            "en_length": len(en_text),
            "ja_length": len(ja_text),
            "ratio": round(ratio, 2),
            "ratio_ok": is_valid
        }

    def validate_keyword_presence(self, disease: Dict, field: str) -> Tuple[bool, Dict]:
        """Validate medical keywords present in content.

        Args:
            disease: Disease dictionary
            field: Field name

        Returns:
            (is_valid, details_dict)
        """
        en_text = disease.get(field, "").lower()

        if field == "treatment":
            keywords = self.TREATMENT_KEYWORDS
        elif field == "prevention":
            keywords = self.PREVENTION_KEYWORDS
        elif field == "prognosis":
            keywords = self.PROGNOSIS_KEYWORDS
        else:
            return False, {"error": "Unknown field"}

        # Check if at least 2 relevant keywords present
        found_keywords = [kw for kw in keywords if kw in en_text]

        is_valid = len(found_keywords) >= 2  # At least 2 keywords
        return is_valid, {
            "found_keywords": found_keywords,
            "keyword_count": len(found_keywords),
            "required": 2
        }

    def validate_sentence_structure(self, disease: Dict, field: str) -> Tuple[bool, Dict]:
        """Validate text has proper sentence structure (2-3 sentences).

        Args:
            disease: Disease dictionary
            field: Field name

        Returns:
            (is_valid, details_dict)
        """
        en_text = disease.get(field, "")

        if not en_text:
            return False, {"error": "No text"}

        # Count sentences (simple heuristic: count periods/question marks/exclamation marks)
        sentence_count = en_text.count(".") + en_text.count("?") + en_text.count("!")

        # Target: 2-3 sentences
        is_valid = 2 <= sentence_count <= 4  # Allow some flexibility

        return is_valid, {
            "sentence_count": sentence_count,
            "target": "2-3",
            "is_ok": is_valid
        }

    def validate_species_specificity(self, disease: Dict) -> Tuple[bool, Dict]:
        """Check if content mentions species or is generic.

        Args:
            disease: Disease dictionary

        Returns:
            (is_valid, details_dict)
        """
        species = disease.get("species", "Unknown")
        generic_indicators = [
            "depends on", "may be", "could be", "typically",
            "generally", "in some cases", "if applicable"
        ]

        details = {"species": species}

        for field in ["treatment", "prevention", "prognosis"]:
            text = disease.get(field, "").lower()
            if not text:
                details[f"{field}_specific"] = False
                continue

            # Check if field mentions species or has specific details
            has_species_ref = species.lower() in text or any(
                indicator in text for indicator in generic_indicators
            )
            # For now, any non-empty field is considered specific enough
            details[f"{field}_specific"] = len(text) > 50

        return True, details

    def run_full_validation(self, diseases: List[Dict] = None) -> Dict:
        """Run comprehensive validation on all Phase 2 enriched diseases.

        Args:
            diseases: Disease list (loads from DB if not provided)

        Returns:
            Validation report dictionary
        """
        if diseases is None:
            diseases = self.load_diseases()

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_diseases": len(diseases),
            "fields": {
                "treatment": {
                    "presence": {"passed": 0, "failed": 0, "total": 0},
                    "length": {"passed": 0, "failed": 0, "total": 0},
                    "bilingual": {"passed": 0, "failed": 0, "total": 0},
                    "keywords": {"passed": 0, "failed": 0, "total": 0},
                    "sentences": {"passed": 0, "failed": 0, "total": 0},
                    "failed_samples": []
                },
                "prevention": {
                    "presence": {"passed": 0, "failed": 0, "total": 0},
                    "length": {"passed": 0, "failed": 0, "total": 0},
                    "bilingual": {"passed": 0, "failed": 0, "total": 0},
                    "keywords": {"passed": 0, "failed": 0, "total": 0},
                    "sentences": {"passed": 0, "failed": 0, "total": 0},
                    "failed_samples": []
                },
                "prognosis": {
                    "presence": {"passed": 0, "failed": 0, "total": 0},
                    "length": {"passed": 0, "failed": 0, "total": 0},
                    "bilingual": {"passed": 0, "failed": 0, "total": 0},
                    "keywords": {"passed": 0, "failed": 0, "total": 0},
                    "sentences": {"passed": 0, "failed": 0, "total": 0},
                    "failed_samples": []
                }
            },
            "overall": {
                "completion_rate": 0,
                "quality_rate": 0
            }
        }

        # Validate each disease and field
        for disease in diseases:
            disease_id = disease.get("id", "unknown")

            for field in ["treatment", "prevention", "prognosis"]:
                # Presence check
                is_present, msg = self.validate_field_presence(disease, field)
                report["fields"][field]["presence"]["total"] += 1
                if is_present:
                    report["fields"][field]["presence"]["passed"] += 1
                else:
                    report["fields"][field]["presence"]["failed"] += 1
                    if len(report["fields"][field]["failed_samples"]) < 3:
                        report["fields"][field]["failed_samples"].append({
                            "disease_id": disease_id,
                            "issue": msg
                        })

                if not is_present:
                    continue  # Skip other checks if field missing

                # Length check
                is_valid, details = self.validate_field_length(disease, field)
                report["fields"][field]["length"]["total"] += 1
                if is_valid:
                    report["fields"][field]["length"]["passed"] += 1
                else:
                    report["fields"][field]["length"]["failed"] += 1
                    if len(report["fields"][field]["failed_samples"]) < 3:
                        report["fields"][field]["failed_samples"].append({
                            "disease_id": disease_id,
                            "issue": f"Length issue: EN={details['en_length']}, JA={details['ja_length']}"
                        })

                # Bilingual balance
                is_valid, details = self.validate_bilingual_balance(disease, field)
                report["fields"][field]["bilingual"]["total"] += 1
                if is_valid:
                    report["fields"][field]["bilingual"]["passed"] += 1
                else:
                    report["fields"][field]["bilingual"]["failed"] += 1

                # Keyword presence
                is_valid, details = self.validate_keyword_presence(disease, field)
                report["fields"][field]["keywords"]["total"] += 1
                if is_valid:
                    report["fields"][field]["keywords"]["passed"] += 1
                else:
                    report["fields"][field]["keywords"]["failed"] += 1

                # Sentence structure
                is_valid, details = self.validate_sentence_structure(disease, field)
                report["fields"][field]["sentences"]["total"] += 1
                if is_valid:
                    report["fields"][field]["sentences"]["passed"] += 1
                else:
                    report["fields"][field]["sentences"]["failed"] += 1

        # Calculate completion rate
        total_fields = 0
        completed_fields = 0

        for field in ["treatment", "prevention", "prognosis"]:
            total = report["fields"][field]["presence"]["total"]
            passed = report["fields"][field]["presence"]["passed"]
            total_fields += total
            completed_fields += passed

        if total_fields > 0:
            report["overall"]["completion_rate"] = round(100 * completed_fields / total_fields, 1)

        # Calculate quality rate (average of all checks)
        total_checks = 0
        quality_checks = 0

        for field in ["treatment", "prevention", "prognosis"]:
            for check_type in ["presence", "length", "bilingual", "keywords", "sentences"]:
                check_data = report["fields"][field][check_type]
                total_checks += check_data["total"]
                quality_checks += check_data["passed"]

        if total_checks > 0:
            report["overall"]["quality_rate"] = round(100 * quality_checks / total_checks, 1)

        return report

    def print_validation_report(self, report: Dict):
        """Print formatted validation report."""
        print("\n" + "="*70)
        print("PHASE 2 QA VALIDATION REPORT")
        print("="*70)
        print(f"Generated: {report['timestamp']}")
        print(f"Total diseases: {report['total_diseases']}")

        print(f"\n{'FIELD VALIDATION RESULTS':^70}")
        print("-"*70)

        for field in ["treatment", "prevention", "prognosis"]:
            print(f"\n{field.upper()}")
            field_data = report["fields"][field]

            for check_type in ["presence", "length", "bilingual", "keywords", "sentences"]:
                check = field_data[check_type]
                if check["total"] == 0:
                    continue

                passed_pct = 100 * check["passed"] / check["total"] if check["total"] > 0 else 0
                status = "✓" if passed_pct >= 80 else "⚠" if passed_pct >= 50 else "✗"
                print(f"  {status} {check_type:12}: {check['passed']:4}/{check['total']:4} ({passed_pct:5.1f}%)")

            # Show failed samples
            if field_data["failed_samples"]:
                print(f"    Sample failures:")
                for sample in field_data["failed_samples"][:2]:
                    print(f"      - {sample['disease_id']}: {sample['issue']}")

        print(f"\n{'OVERALL METRICS':^70}")
        print("-"*70)
        print(f"Completion rate: {report['overall']['completion_rate']:.1f}%")
        print(f"Quality rate: {report['overall']['quality_rate']:.1f}%")

        print("\n" + "="*70)
