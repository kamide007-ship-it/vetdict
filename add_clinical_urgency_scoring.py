#!/usr/bin/env python3
"""
Add clinical urgency scoring and severity-based content recommendations.

This script:
1. Ensures urgency field is standardized
2. Adds severity_score (1-5 scale)
3. Adds estimated_cost_level (low/moderate/high)
4. Adds hospitalization_likelihood
5. Adds monitoring_frequency recommendations
"""

import json
from typing import Dict


class UrgencyScoringEngine:
    """Add urgency scoring and severity information"""

    def __init__(self):
        self.urgency_map = self._build_urgency_map()
        self.cost_keywords = self._build_cost_keywords()

    def _build_urgency_map(self) -> Dict[str, int]:
        """Map urgency levels to severity scores"""
        return {
            "emergency": 5,
            "high": 4,
            "moderate": 3,
            "low": 2,
            "minimal": 1,
        }

    def _build_cost_keywords(self) -> Dict[str, Dict]:
        """Build cost estimation based on disease characteristics"""
        return {
            "high_cost": {
                "keywords": [
                    "surgery",
                    "chemotherapy",
                    "radiation",
                    "hospitalization",
                    "intensive",
                    "cancer",
                    "neoplastic",
                    "cardiac",
                    "multiple medications",
                ],
                "cost_level": "high",
                "monitoring": "weekly",
            },
            "moderate_cost": {
                "keywords": ["infection", "antibiotic", "treatment", "therapy", "management", "medication", "dietary"],
                "cost_level": "moderate",
                "monitoring": "bi-weekly",
            },
            "low_cost": {
                "keywords": [
                    "prevention",
                    "supportive",
                    "monitoring",
                    "observation",
                    "dietary management",
                    "preventive",
                ],
                "cost_level": "low",
                "monitoring": "monthly",
            },
        }

    def _estimate_hospitalization(self, urgency: str, treatment: str, disease_name: str) -> str:
        """Estimate likelihood of hospitalization"""
        urgency_lower = urgency.lower()
        treatment_lower = treatment.lower()

        if urgency_lower == "emergency":
            return "high"
        elif urgency_lower == "high":
            if any(word in treatment_lower for word in ["hospitalization", "intensive", "surgery", "transfusion"]):
                return "high"
            elif any(word in treatment_lower for word in ["supportive", "medication", "therapy"]):
                return "moderate"
            else:
                return "low"
        elif urgency_lower == "moderate":
            if any(word in treatment_lower for word in ["surgery", "hospitalization"]):
                return "moderate"
            else:
                return "low"
        else:
            return "low"

    def _estimate_treatment_cost(self, treatment: str, disease_name: str) -> str:
        """Estimate treatment cost level"""
        text = (treatment + disease_name).lower()

        high_cost_keywords = [
            "surgery",
            "chemotherapy",
            "radiation",
            "intensive care",
            "hospitalization",
            "multiple",
            "prolonged",
            "specialized",
            "oncology",
            "cardiologist",
            "neurologist",
        ]

        moderate_cost_keywords = [
            "antibiotic",
            "antifungal",
            "medication",
            "therapy",
            "medication",
            "treatment",
            "management",
            "dietary",
            "monitoring",
            "2-4 weeks",
            "3-8 weeks",
        ]

        for keyword in high_cost_keywords:
            if keyword in text:
                return "high"

        for keyword in moderate_cost_keywords:
            if keyword in text:
                return "moderate"

        return "low"

    def _recommend_monitoring_frequency(self, urgency: str, treatment_duration: str = "") -> str:
        """Recommend monitoring frequency"""
        urgency_lower = urgency.lower()

        frequency_map = {
            "emergency": "continuous",
            "high": "weekly",
            "moderate": "bi-weekly",
        }
        return frequency_map.get(urgency_lower, "monthly")

    def add_clinical_scores(self, input_file: str, output_file: str) -> Dict:
        """Add urgency scores and clinical recommendations"""
        print(f"Loading data from {input_file}...")
        with open(input_file, "r", encoding="utf-8") as f:
            diseases = json.load(f)

        updated = 0
        added_fields = 0

        print(f"Processing {len(diseases)} disease records...")

        for i, disease in enumerate(diseases):
            if (i + 1) % 500 == 0:
                print(f"  Progress: {i + 1}/{len(diseases)}")

            urgency = disease.get("urgency", "moderate").lower()
            treatment = disease.get("treatment", "")
            disease_name = disease.get("name", "")

            # 1. Ensure urgency is standardized
            if urgency not in self.urgency_map:
                urgency = "moderate"
                disease["urgency"] = urgency
                updated += 1

            # 2. Add severity_score
            if not disease.get("severity_score"):
                disease["severity_score"] = self.urgency_map.get(urgency, 3)
                added_fields += 1

            # 3. Add estimated_cost_level
            if not disease.get("estimated_cost_level"):
                cost = self._estimate_treatment_cost(treatment, disease_name)
                disease["estimated_cost_level"] = cost
                added_fields += 1

            # 4. Add hospitalization_likelihood
            if not disease.get("hospitalization_likelihood"):
                hosp = self._estimate_hospitalization(urgency, treatment, disease_name)
                disease["hospitalization_likelihood"] = hosp
                added_fields += 1

            # 5. Add monitoring_frequency
            if not disease.get("monitoring_frequency"):
                freq = self._recommend_monitoring_frequency(urgency)
                disease["monitoring_frequency"] = freq
                added_fields += 1

            # 6. Add treatment_duration_weeks estimate if possible
            if not disease.get("treatment_duration_weeks"):
                treatment_lower = treatment.lower()
                if "2-4 weeks" in treatment_lower or "2 to 4 weeks" in treatment_lower:
                    disease["treatment_duration_weeks"] = 3
                elif "1-2 weeks" in treatment_lower:
                    disease["treatment_duration_weeks"] = 1.5
                elif "3-8 weeks" in treatment_lower or "3 to 8 weeks" in treatment_lower:
                    disease["treatment_duration_weeks"] = 5.5
                elif "4-6 weeks" in treatment_lower:
                    disease["treatment_duration_weeks"] = 5
                elif "lifelong" in treatment_lower or "chronic" in disease_name.lower():
                    disease["treatment_duration_weeks"] = float("inf")
                else:
                    # Default estimates
                    if urgency == "emergency":
                        disease["treatment_duration_weeks"] = 1
                    elif urgency == "high":
                        disease["treatment_duration_weeks"] = 2
                    elif urgency == "moderate":
                        disease["treatment_duration_weeks"] = 4
                    else:
                        disease["treatment_duration_weeks"] = 8

        print(f"\nSaving {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(diseases, f, ensure_ascii=False, indent=2)

        return {
            "total": len(diseases),
            "updated": updated,
            "fields_added": added_fields,
        }


def main():
    """Main entry point"""
    input_file = "/home/user/vetdict/diseases_all_species.json"
    output_file = "/home/user/vetdict/diseases_all_species_scored.json"

    engine = UrgencyScoringEngine()

    print("=" * 70)
    print("Clinical Urgency Scoring and Severity Assessment")
    print("=" * 70)

    results = engine.add_clinical_scores(input_file, output_file)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total records processed:  {results['total']}")
    print(f"Urgency standardized:     {results['updated']}")
    print(f"New fields added:         {results['fields_added']}")
    print("=" * 70)

    # Display summary statistics
    print("\nNew fields added:")
    print("  • severity_score (1-5): Numeric urgency level")
    print("  • estimated_cost_level (low/moderate/high): Treatment cost estimate")
    print("  • hospitalization_likelihood (low/moderate/high): Hospitalization need")
    print("  • monitoring_frequency: How often to monitor (continuous/weekly/bi-weekly/monthly)")
    print("  • treatment_duration_weeks: Estimated treatment duration")


if __name__ == "__main__":
    main()
