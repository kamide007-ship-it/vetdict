#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 Enrichment Runner for VetDict

Enriches diseases for Cat and Horse species using Batches API.
- Cat: 516 diseases
- Horse: 736 diseases
- Total: 1,252 diseases

Uses 50% discount Batches API for cost optimization.
Estimated cost: $62.80
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.disease_batch_enricher import DiseaseBatchEnricher


class Phase1EnrichmentRunner:
    """Orchestrates Phase 1 enrichment for Cat and Horse."""

    def __init__(self):
        self.db_path = Path(__file__).parent.parent / "diseases_all_species.json"
        self.enricher = DiseaseBatchEnricher(model="claude-opus-4-6")
        self.manifest_path = Path(__file__).parent.parent / "phase1_enrichment_manifest.json"

    def load_diseases(self):
        """Load diseases from the main database."""
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def filter_by_species(self, diseases, species_list):
        """Filter diseases by species and check enrichment status."""
        filtered = []
        for disease in diseases:
            if disease.get("species") not in species_list:
                continue

            # Skip if all fields are already populated
            if all(
                disease.get(f)
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
            ):
                continue

            filtered.append(disease)

        return filtered

    def create_enrichment_prompt(self, disease, species, include_references=True):
        """Create an enrichment prompt with species-specific context."""
        disease_name = disease.get("name", "Unknown")
        disease_name_ja = disease.get("name_ja", disease_name)
        description = disease.get("description", "")
        species = disease.get("species", "Unknown")

        # Species-specific references
        references = {"Cat": [1, 2, 8, 12, 43, 44, 45, 46], "Horse": [3, 11, 38, 39, 40, 41]}

        ref_list = references.get(species, [])
        ref_str = f"\n\nReferences: {ref_list}" if include_references and ref_list else ""

        prompt = f"""You are a veterinary medicine expert specializing in {species} diseases.
Generate comprehensive medical information for the following disease.

Disease: {disease_name} ({disease_name_ja})
Species: {species}
Description: {description}{ref_str}

Generate a JSON object with these exact fields (use empty string "" if unable):
{{
  "pathophysiology": "2-3 sentences describing disease mechanism, tissue damage, and progression",
  "pathophysiology_ja": "2-3文で病態生理を説明",
  "causes": "2-3 sentences on primary/secondary causes and risk factors",
  "causes_ja": "2-3文で原因と危険因子を説明",
  "treatment": "2-3 sentences on treatment approaches, medications, management",
  "treatment_ja": "2-3文で治療法とマネジメントを説明",
  "prevention": "2-3 sentences on prevention strategies and risk reduction",
  "prevention_ja": "2-3文で予防と危険因子軽減を説明",
  "prognosis": "2-3 sentences on expected outcomes, recovery timeline, complications",
  "prognosis_ja": "2-3文で予後と回復見込みを説明"
}}

IMPORTANT: Return ONLY valid JSON. No explanations, no markdown code blocks, just raw JSON.
Ensure medical accuracy appropriate for veterinary professionals."""

        return prompt

    def run_phase1(self):
        """Execute Phase 1 enrichment."""
        print("=" * 70)
        print("PHASE 1 ENRICHMENT RUNNER - Cat & Horse")
        print("=" * 70)
        print(f"Start time: {datetime.now().isoformat()}\n")

        # Load diseases
        print("[1/5] Loading disease database...")
        all_diseases = self.load_diseases()
        print(f"✓ Loaded {len(all_diseases)} total diseases")

        # Filter Cat and Horse diseases
        print("\n[2/5] Filtering Cat and Horse diseases...")
        cat_diseases = self.filter_by_species(all_diseases, ["Cat"])
        horse_diseases = self.filter_by_species(all_diseases, ["Horse"])

        print(f"✓ Found {len(cat_diseases)} incomplete Cat diseases")
        print(f"✓ Found {len(horse_diseases)} incomplete Horse diseases")
        print(f"✓ Total Phase 1 diseases: {len(cat_diseases) + len(horse_diseases)}")

        # Create batch requests
        print("\n[3/5] Creating batch requests...")
        enricher = DiseaseBatchEnricher(model="claude-opus-4-6")

        cat_batches = enricher.create_batch_requests(cat_diseases)
        horse_batches = enricher.create_batch_requests(horse_diseases)

        print(f"✓ Cat batches: {len(cat_batches)}")
        print(f"✓ Horse batches: {len(horse_batches)}")
        total_requests = sum(len(b) for b in cat_batches + horse_batches)
        print(f"✓ Total requests: {total_requests}")

        # Submit batches
        print("\n[4/5] Submitting batches to Claude API...")
        manifest = {
            "phase": 1,
            "started_at": datetime.now().isoformat(),
            "species": {
                "Cat": {
                    "disease_count": len(cat_diseases),
                    "batch_count": len(cat_batches),
                    "batch_ids": [],
                    "status": "pending",
                },
                "Horse": {
                    "disease_count": len(horse_diseases),
                    "batch_count": len(horse_batches),
                    "batch_ids": [],
                    "status": "pending",
                },
            },
        }

        # Submit Cat batches
        print("\nSubmitting Cat enrichment batches...")
        for i, batch in enumerate(cat_batches):
            try:
                batch_id = enricher.submit_batch(batch)
                manifest["species"]["Cat"]["batch_ids"].append(batch_id)
                print(f"  ✓ Cat batch {i + 1}/{len(cat_batches)}: {batch_id}")
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"  ✗ Error submitting Cat batch {i + 1}: {e}")

        # Submit Horse batches
        print("\nSubmitting Horse enrichment batches...")
        for i, batch in enumerate(horse_batches):
            try:
                batch_id = enricher.submit_batch(batch)
                manifest["species"]["Horse"]["batch_ids"].append(batch_id)
                print(f"  ✓ Horse batch {i + 1}/{len(horse_batches)}: {batch_id}")
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"  ✗ Error submitting Horse batch {i + 1}: {e}")

        # Save manifest
        print("\n[5/5] Saving enrichment manifest...")
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f"✓ Manifest saved: {self.manifest_path}")

        # Print summary
        print("\n" + "=" * 70)
        print("BATCH SUBMISSION COMPLETE")
        print("=" * 70)
        print("\nPhase 1 Summary:")
        print(f"  - Cat diseases: {len(cat_diseases)}")
        print(f"  - Horse diseases: {len(horse_diseases)}")
        print(f"  - Total diseases: {len(cat_diseases) + len(horse_diseases)}")
        print(f"  - Total batches: {len(cat_batches) + len(horse_batches)}")
        print("  - Estimated cost: $62.80 (50% discount with Batches API)")
        print(f"\nManifest saved: {self.manifest_path}")
        print("\nNext steps:")
        print("  1. Monitor batch status: python3 scripts/phase1_batch_monitor.py")
        print("  2. Process results: python3 scripts/phase1_batch_processor.py")
        print("  3. Validate QA: python3 scripts/phase1_qa_validator.py")
        print("  4. Integrate results: python3 scripts/phase1_integration.py")

        return manifest


if __name__ == "__main__":
    runner = Phase1EnrichmentRunner()
    manifest = runner.run_phase1()
