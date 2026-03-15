#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 Batch Processor

Retrieves completed batch results and integrates them back into the database.
"""

import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import anthropic


class Phase1BatchProcessor:
    """Processes Phase 1 batch results and updates database."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.manifest_path = Path(__file__).parent.parent / "phase1_enrichment_manifest.json"
        self.db_path = Path(__file__).parent.parent / "diseases_all_species.json"
        self.enriched_db_path = Path(__file__).parent.parent / f"diseases_enriched_phase1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    def load_manifest(self):
        """Load the enrichment manifest."""
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_diseases(self):
        """Load diseases from the database."""
        with open(self.db_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def retrieve_batch_results(self, batch_id) -> List[Dict]:
        """Retrieve results from a completed batch."""
        try:
            results = []
            for result in self.client.messages.batches.results(batch_id):
                results.append({
                    "custom_id": result.result.message.custom_id if hasattr(result.result.message, 'custom_id') else result.custom_id,
                    "content": result.result.message.content[0].text if result.result.message.content else "",
                    "status": "succeeded" if result.result.message else "errored"
                })
            return results
        except Exception as e:
            print(f"❌ Error retrieving batch {batch_id}: {e}")
            return []

    def parse_enrichment_response(self, response_text: str) -> Optional[Dict]:
        """Parse JSON from Claude response."""
        try:
            # Try direct JSON parsing
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try extracting JSON from markdown code blocks
            match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass

            # Try finding JSON object in response
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    pass

            return None

    def process_batch_results(self, manifest: Dict) -> Dict:
        """Process all batch results and collect enriched data."""
        print("\n" + "=" * 70)
        print("PROCESSING BATCH RESULTS")
        print("=" * 70)

        enriched_data = {
            "Cat": {},
            "Horse": {}
        }
        error_log = []

        for species, species_data in manifest["species"].items():
            print(f"\n{species} Results:")
            print("-" * 40)

            species_succeeded = 0
            species_errored = 0

            for i, batch_id in enumerate(species_data.get("batch_ids", [])):
                print(f"  Batch {i+1}: {batch_id[:30]}...")

                results = self.retrieve_batch_results(batch_id)
                print(f"    Retrieved {len(results)} results")

                for result in results:
                    if result["status"] == "succeeded" and result["content"]:
                        parsed = self.parse_enrichment_response(result["content"])
                        if parsed:
                            enriched_data[species][result["custom_id"]] = parsed
                            species_succeeded += 1
                        else:
                            error_log.append({
                                "custom_id": result["custom_id"],
                                "species": species,
                                "batch_id": batch_id,
                                "error": "Failed to parse JSON"
                            })
                            species_errored += 1
                    else:
                        error_log.append({
                            "custom_id": result["custom_id"],
                            "species": species,
                            "batch_id": batch_id,
                            "error": "API error or empty response"
                        })
                        species_errored += 1

            print(f"  Results: {species_succeeded} succeeded, {species_errored} errored")

        return {
            "enriched_data": enriched_data,
            "error_log": error_log,
            "stats": {
                "total_succeeded": sum(len(v) for v in enriched_data.values()),
                "total_errored": len(error_log)
            }
        }

    def integrate_enrichment(self, diseases: List[Dict], enriched_data: Dict) -> List[Dict]:
        """Integrate enriched data back into disease records."""
        print("\n" + "=" * 70)
        print("INTEGRATING ENRICHED DATA")
        print("=" * 70)

        integrated_count = 0

        for disease in diseases:
            species = disease.get("species")
            disease_id = disease.get("id")

            if species not in enriched_data:
                continue

            if disease_id in enriched_data[species]:
                enriched = enriched_data[species][disease_id]

                # Update fields
                for field in ["pathophysiology", "pathophysiology_ja", "causes", "causes_ja",
                             "treatment", "treatment_ja", "prevention", "prevention_ja",
                             "prognosis", "prognosis_ja"]:
                    if field in enriched and enriched[field]:
                        disease[field] = enriched[field]

                # Add metadata
                disease["enriched_at"] = datetime.now().isoformat()
                disease["enrichment_phase"] = 1
                integrated_count += 1

        print(f"✓ Integrated {integrated_count} enriched diseases")
        return diseases

    def save_enriched_database(self, diseases: List[Dict]):
        """Save enriched database to file."""
        with open(self.enriched_db_path, 'w', encoding='utf-8') as f:
            json.dump(diseases, f, ensure_ascii=False, indent=2)
        print(f"✓ Enriched database saved: {self.enriched_db_path}")

    def run_processor(self):
        """Execute the batch processor."""
        print("=" * 70)
        print("PHASE 1 BATCH PROCESSOR")
        print("=" * 70)
        print(f"Start time: {datetime.now().isoformat()}\n")

        # Load data
        print("[1/4] Loading manifest...")
        manifest = self.load_manifest()
        print(f"✓ Found {sum(len(data.get('batch_ids', [])) for data in manifest['species'].values())} batches")

        print("\n[2/4] Retrieving batch results...")
        results = self.process_batch_results(manifest)

        print("\n[3/4] Loading disease database...")
        diseases = self.load_diseases()
        print(f"✓ Loaded {len(diseases)} diseases")

        print("\n[4/4] Integrating enriched data...")
        diseases = self.integrate_enrichment(diseases, results["enriched_data"])

        # Save enriched database
        self.save_enriched_database(diseases)

        # Print summary
        print("\n" + "=" * 70)
        print("PROCESSING COMPLETE")
        print("=" * 70)
        print(f"\nResults Summary:")
        print(f"  Succeeded: {results['stats']['total_succeeded']}")
        print(f"  Errored: {results['stats']['total_errored']}")
        print(f"  Success rate: {100 * results['stats']['total_succeeded'] / max(results['stats']['total_succeeded'] + results['stats']['total_errored'], 1):.1f}%")

        if results["error_log"]:
            print(f"\nErrors ({len(results['error_log'])}):")
            for i, error in enumerate(results["error_log"][:10]):  # Show first 10
                print(f"  {i+1}. {error['custom_id']} ({error['species']}): {error['error']}")
            if len(results["error_log"]) > 10:
                print(f"  ... and {len(results['error_log']) - 10} more")

        print(f"\nEnriched database: {self.enriched_db_path}")
        print(f"\nNext steps:")
        print(f"  1. Review enriched database")
        print(f"  2. Run QA checks: python3 scripts/phase1_qa_validator.py")
        print(f"  3. Integrate into main DB: python3 scripts/phase1_integration.py")


if __name__ == "__main__":
    processor = Phase1BatchProcessor()
    processor.run_processor()
