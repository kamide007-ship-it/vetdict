#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 Batch Processor

Retrieves completed batch results and integrates them back into the database.
"""

import json
import os
import re
import sys
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
                custom_id = result.custom_id
                content = ""
                status = "errored"

                # Extract content from successful results
                if hasattr(result.result, 'message') and result.result.message and result.result.message.content:
                        content = result.result.message.content[0].text
                        status = "succeeded"

                results.append({
                    "custom_id": custom_id,
                    "content": content,
                    "status": status
                })
            return results
        except Exception as e:
            print(f"❌ Error retrieving batch {batch_id}: {e}")
            return []

    def parse_enrichment_response(self, response_text: str) -> Optional[Dict]:
        """Parse JSON from Claude response, handling truncated responses."""
        try:
            # Try direct JSON parsing
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass

        # Try extracting JSON from markdown code blocks
        match = re.search(r'```(?:json)?\s*(\{[\s\S]*)', response_text, re.DOTALL)
        if match:
            json_text = match.group(1).rstrip()
            # Remove trailing code block marker if present
            if json_text.endswith('```'):
                json_text = json_text[:-3].rstrip()
        else:
            # Find JSON object in response
            start = response_text.find('{')
            if start == -1:
                return None
            json_text = response_text[start:].rstrip()

        # Handle truncated/incomplete JSON
        # Strategy: Remove everything after the last complete value
        if not json_text.endswith('}'):
            # Find the last closing quote and comma pattern
            # Remove everything after the last ', (complete key-value pair)
            last_comma_quote = -1
            for i in range(len(json_text) - 1, -1, -1):
                if i > 0 and json_text[i-1:i+1] == '",':
                    last_comma_quote = i + 1
                    break

            if last_comma_quote > 0:
                # Keep everything up to and including the last complete value
                json_text = json_text[:last_comma_quote].rstrip()
                # Remove the trailing comma
                if json_text.endswith(','):
                    json_text = json_text[:-1]

            # Add closing braces for any open braces
            brace_count = json_text.count('{') - json_text.count('}')
            if brace_count > 0:
                json_text += '}' * brace_count

        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            pass

        return None

    def process_batch_results(self, manifest: Dict, diseases: List[Dict]) -> Dict:
        """Process all batch results and collect enriched data."""
        print("\n" + "=" * 70)
        print("PROCESSING BATCH RESULTS")
        print("=" * 70)

        enriched_data = {
            "Cat": {},
            "Horse": {}
        }
        error_log = []

        # Build disease ID mappings by species
        disease_id_mapping = {"Cat": {}, "Horse": {}}
        for idx, disease in enumerate(diseases):
            species = disease.get("species")
            if species in disease_id_mapping:
                disease_id_mapping[species][idx] = disease.get("id")

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
                    # Extract disease index from custom_id (e.g., "disease-0" -> 0)
                    try:
                        disease_idx = int(result["custom_id"].split("-")[1])
                    except (IndexError, ValueError):
                        disease_idx = None

                    # Map to actual disease ID
                    actual_disease_id = None
                    species_disease_ids = [d for d in diseases if d.get("species") == species]
                    if disease_idx is not None and disease_idx < len(species_disease_ids):
                        actual_disease_id = species_disease_ids[disease_idx].get("id")

                    if result["status"] == "succeeded" and result["content"] and actual_disease_id:
                        parsed = self.parse_enrichment_response(result["content"])
                        if parsed:
                            enriched_data[species][actual_disease_id] = parsed
                            species_succeeded += 1
                        else:
                            error_log.append({
                                "custom_id": result["custom_id"],
                                "actual_id": actual_disease_id,
                                "species": species,
                                "batch_id": batch_id,
                                "error": "Failed to parse JSON"
                            })
                            species_errored += 1
                    else:
                        error_log.append({
                            "custom_id": result["custom_id"],
                            "actual_id": actual_disease_id,
                            "species": species,
                            "batch_id": batch_id,
                            "error": "API error or empty response or invalid ID"
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

        print("\n[2/4] Loading disease database...")
        diseases = self.load_diseases()
        print(f"✓ Loaded {len(diseases)} diseases")

        print("\n[3/4] Retrieving batch results...")
        results = self.process_batch_results(manifest, diseases)

        print("\n[4/4] Integrating enriched data...")
        diseases = self.integrate_enrichment(diseases, results["enriched_data"])

        # Save enriched database
        self.save_enriched_database(diseases)

        # Print summary
        print("\n" + "=" * 70)
        print("PROCESSING COMPLETE")
        print("=" * 70)
        print("\nResults Summary:")
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
        print("\nNext steps:")
        print("  1. Review enriched database")
        print("  2. Run QA checks: python3 scripts/phase1_qa_validator.py")
        print("  3. Integrate into main DB: python3 scripts/phase1_integration.py")


if __name__ == "__main__":
    processor = Phase1BatchProcessor()
    processor.run_processor()
