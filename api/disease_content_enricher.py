#!/usr/bin/env python3
"""
Disease Content Enricher Module

Uses Claude API to enrich incomplete disease records with:
- Pathophysiology (病態生理)
- Causes (原因)
- Treatment (治療)
- Prevention (予防)
- Prognosis (予後)

Supports batch processing for cost efficiency.
"""

import json
import os
from typing import Optional
import anthropic


class DiseaseEnricher:
    """Enriches disease data using Claude API."""

    def __init__(self, model: str = "claude-opus-4-6"):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    def _build_enrichment_prompt(self, disease: dict) -> str:
        """Build a prompt to generate missing disease information."""
        disease_name = disease.get("name", "Unknown Disease")
        disease_name_ja = disease.get("name_ja", disease_name)
        description = disease.get("description", "")
        description_ja = disease.get("description_ja", description)

        return f"""You are a veterinary medicine expert. Based on the following disease information,
generate detailed medical information in both English and Japanese.

Disease Name (EN): {disease_name}
Disease Name (JA): {disease_name_ja}

Current Description (EN): {description}
Current Description (JA): {description_ja}

Generate the following fields in valid JSON format:
1. pathophysiology (EN) - Detailed explanation of the disease mechanism
2. pathophysiology_ja (JA) - 病態生理の詳細説明
3. causes (EN) - Primary and secondary causes
4. causes_ja (JA) - 原因の詳細説明
5. treatment (EN) - Treatment approaches and management
6. treatment_ja (JA) - 治療法とマネジメント
7. prevention (EN) - Prevention strategies and risk reduction
8. prevention_ja (JA) - 予防と危険因子の軽減
9. prognosis (EN) - Expected outcomes and recovery
10. prognosis_ja (JA) - 予後と回復見込み

Return ONLY valid JSON with these exact keys. Be concise but comprehensive (2-3 sentences per field).
Ensure medical accuracy appropriate for veterinary professionals."""

    def enrich_single_disease(self, disease: dict) -> dict:
        """Enrich a single disease record with missing information."""
        # Check which fields are missing
        missing_fields = []
        field_pairs = [
            ("pathophysiology", "pathophysiology_ja"),
            ("causes", "causes_ja"),
            ("treatment", "treatment_ja"),
            ("prevention", "prevention_ja"),
            ("prognosis", "prognosis_ja"),
        ]

        for en_field, ja_field in field_pairs:
            if not disease.get(en_field) and not disease.get(ja_field):
                missing_fields.append((en_field, ja_field))

        if not missing_fields:
            return disease  # All fields present

        # Generate missing information
        prompt = self._build_enrichment_prompt(disease)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            thinking={"type": "adaptive"},
            output_config={"effort": "high"},
            messages=[{"role": "user", "content": prompt}],
        )

        # Extract JSON from response
        try:
            response_text = next(
                (b.text for b in response.content if b.type == "text"), ""
            )
            # Try to extract JSON from the response
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                enriched_data = json.loads(json_str)

                # Merge with original disease data
                for key, value in enriched_data.items():
                    if key not in disease or not disease[key]:
                        disease[key] = value

        except (json.JSONDecodeError, ValueError) as e:
            print(f"Failed to parse response for {disease.get('name')}: {e}")

        return disease

    def get_enrichment_status(self, diseases: list) -> dict:
        """Analyze completeness of disease data."""
        complete = 0
        incomplete = []
        field_counts = {
            "pathophysiology": 0,
            "causes": 0,
            "treatment": 0,
            "prevention": 0,
            "prognosis": 0,
        }

        for d in diseases:
            has_all_fields = True
            for field in field_counts:
                has_field = bool(d.get(field) or d.get(f"{field}_ja"))
                if has_field:
                    field_counts[field] += 1
                else:
                    has_all_fields = False

            if has_all_fields:
                complete += 1
            else:
                incomplete.append(
                    {
                        "name": d.get("name", "Unknown"),
                        "name_ja": d.get("name_ja", ""),
                    }
                )

        return {
            "total": len(diseases),
            "complete": complete,
            "complete_percentage": round((complete / len(diseases) * 100), 1)
            if diseases
            else 0,
            "incomplete": len(incomplete),
            "field_coverage": {
                k: round((v / len(diseases) * 100), 1) if diseases else 0
                for k, v in field_counts.items()
            },
            "sample_incomplete": incomplete[:10],
        }


def main():
    """Example usage of DiseaseEnricher."""
    # Load dog diseases
    from api.symptom_checker import _DISEASE_DB

    enricher = DiseaseEnricher()

    # Check current status
    status = enricher.get_enrichment_status(_DISEASE_DB)
    print("Current Status:")
    print(f"  Total diseases: {status['total']}")
    print(f"  Complete: {status['complete']} ({status['complete_percentage']}%)")
    print(f"  Incomplete: {status['incomplete']}")
    print("\nField Coverage:")
    for field, coverage in status["field_coverage"].items():
        print(f"  {field}: {coverage}%")

    # Enrich a sample incomplete disease
    sample_incomplete = next(
        (d for d in _DISEASE_DB if not d.get("pathophysiology")), None
    )
    if sample_incomplete:
        print(f"\n--- Enriching: {sample_incomplete.get('name')} ---")
        enriched = enricher.enrich_single_disease(sample_incomplete.copy())
        print(f"Pathophysiology: {enriched.get('pathophysiology', 'N/A')[:100]}...")
        print(f"Causes: {enriched.get('causes', 'N/A')[:100]}...")


if __name__ == "__main__":
    main()
