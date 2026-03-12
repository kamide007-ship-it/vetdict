#!/usr/bin/env python3
"""
Phase 1 Expansion Batch Scheduler - Process all 4,806 diseases across 7 species.

This script orchestrates concurrent batch processing for all animal species:
- Cat (516), Horse (736), Bird (308), Rabbit (271), Parakeet (251), Others (1,148)

All batches are submitted simultaneously for maximum efficiency.

Usage:
    # Start all species batches simultaneously
    python scripts/phase1_expansion_batch_scheduler.py start --all-species --concurrent

    # Check status of all batches
    python scripts/phase1_expansion_batch_scheduler.py status

    # Retrieve results from all completed batches
    python scripts/phase1_expansion_batch_scheduler.py retrieve-all

    # Show expansion plan
    python scripts/phase1_expansion_batch_scheduler.py plan
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from api.disease_batch_enricher import DiseaseBatchEnricher
from api.disease_content_enricher import DiseaseEnricher


class Phase1ExpansionScheduler:
    """Orchestrate batch enrichment for all 7 animal species."""

    # Species to process (excluding Dog which is handled separately)
    EXPANSION_SPECIES = {
        "Cat": 516,
        "Horse": 736,
        "Bird": 308,
        "Rabbit": 271,
        "Parakeet": 251,
        "Others": 1148,
    }

    def __init__(self):
        self.enricher = DiseaseBatchEnricher()
        self.status_enricher = DiseaseEnricher()
        self.manifest_path = project_root / "phase1_expansion_manifest.json"
        self.metadata_path = project_root / "diseases_all_species.json"
        self.batch_tracking = self._load_manifest()

    def _load_manifest(self) -> Dict:
        """Load or create batch tracking manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path, "r") as f:
                return json.load(f)
        return {
            "started_at": None,
            "completed_at": None,
            "batches": {},
            "species_order": list(self.EXPANSION_SPECIES.keys()),
            "statistics": {
                "total_diseases": sum(self.EXPANSION_SPECIES.values()),
                "total_cost_estimate": sum(self.EXPANSION_SPECIES.values()) * 0.025,
                "total_standard_cost": sum(self.EXPANSION_SPECIES.values()) * 0.05
            }
        }

    def _save_manifest(self):
        """Save batch tracking manifest."""
        with open(self.manifest_path, "w") as f:
            json.dump(self.batch_tracking, f, indent=2)

    def _load_metadata(self) -> List[Dict]:
        """Load pre-generated disease metadata."""
        if not self.metadata_path.exists():
            print(f"✗ Error: {self.metadata_path} not found")
            print("  Run: python scripts/generate_disease_metadata.py --all-species")
            sys.exit(1)

        with open(self.metadata_path, "r") as f:
            return json.load(f)

    def show_plan(self):
        """Display expansion scheduling plan."""
        print("=" * 80)
        print("PHASE 1 EXPANSION - BATCH SCHEDULING PLAN")
        print("=" * 80)
        print("\nTarget Species (6 species, 4,230 diseases):\n")

        total_cost = 0
        for species, count in self.EXPANSION_SPECIES.items():
            cost = count * 0.025
            total_cost += cost
            print(f"  {species:15} {count:5} diseases  →  ${cost:8.2f}")

        print("\n" + "=" * 80)
        print(f"{'TOTAL':15} {sum(self.EXPANSION_SPECIES.values()):5} diseases  →  ${total_cost:8.2f}")
        print("=" * 80)
        print(f"\nStandard API cost:     ${sum(self.EXPANSION_SPECIES.values()) * 0.05:.2f}")
        print(f"Batch API cost (50%):  ${total_cost:.2f}")
        print(f"Savings:               ${sum(self.EXPANSION_SPECIES.values()) * 0.05 - total_cost:.2f}")
        print(f"\nProcessing time:       1-6 hours (all species simultaneous)")
        print(f"Execution strategy:    Concurrent batch submission")

    def submit_all_batches(self, interactive=True):
        """Submit enrichment batches for all species simultaneously."""
        self.batch_tracking["started_at"] = datetime.now().isoformat()

        # Load metadata
        print("\nLoading pre-generated disease metadata...")
        all_diseases = self._load_metadata()

        print("=" * 80)
        print("PHASE 1 EXPANSION - BATCH SUBMISSION")
        print("=" * 80)
        print(f"\nTotal diseases to enrich: {len(all_diseases)}")
        print(f"Species: {len(self.EXPANSION_SPECIES)}")
        print(f"Total cost: ${sum(self.EXPANSION_SPECIES.values()) * 0.025:.2f}\n")

        if interactive:
            response = input("Proceed with batch submission? (y/n): ").strip().lower()
            if response != "y":
                print("✗ Cancelled")
                return

        # Group diseases by species
        species_groups = {}
        for disease in all_diseases:
            species = disease["species"]
            if species not in species_groups:
                species_groups[species] = []
            species_groups[species].append(disease)

        # Submit batches for each species
        batch_ids_by_species = {}

        print("\n" + "=" * 80)
        print("SUBMITTING BATCHES")
        print("=" * 80)

        for species in self.EXPANSION_SPECIES.keys():
            if species not in species_groups:
                print(f"⊘ {species}: No diseases found in metadata")
                continue

            species_diseases = species_groups[species]

            print(f"\n[{species}] {len(species_diseases)} diseases")
            print(f"  Cost: ${len(species_diseases) * 0.025:.2f}")
            print("  Submitting...", end=" ", flush=True)

            try:
                # Create batch requests for this species
                batch_requests = self.enricher.create_batch_requests(species_diseases)
                total_requests = sum(len(b) for b in batch_requests)

                # Submit each batch
                batch_ids = []
                for batch_requests_chunk in batch_requests:
                    batch_id = self.enricher.submit_batch(batch_requests_chunk)
                    batch_ids.append(batch_id)

                # Track in manifest
                self.batch_tracking["batches"][species] = {
                    "batch_ids": batch_ids,
                    "submitted_at": datetime.now().isoformat(),
                    "status": "processing",
                    "total_requests": total_requests,
                    "disease_count": len(species_diseases),
                    "estimated_cost": len(species_diseases) * 0.025
                }

                batch_ids_by_species[species] = batch_ids

                print(f"✓ {len(batch_ids)} batch(es)")
                for batch_id in batch_ids:
                    print(f"    └─ {batch_id}")

                # Small delay between submissions
                time.sleep(1)

            except Exception as e:
                print(f"✗ Failed: {e}")
                self.batch_tracking["batches"][species] = {
                    "status": "failed",
                    "error": str(e),
                    "failed_at": datetime.now().isoformat()
                }

        self._save_manifest()

        # Summary
        submitted = len(batch_ids_by_species)
        print("\n" + "=" * 80)
        print("PHASE 1 EXPANSION SUBMISSION COMPLETE")
        print("=" * 80)
        print(f"\n✓ Submitted {submitted} species")
        print(f"✓ Total batches: {sum(len(ids) for ids in batch_ids_by_species.values())}")

        total_cost = sum(
            self.batch_tracking["batches"][sp]["estimated_cost"]
            for sp in batch_ids_by_species.keys()
            if sp in self.batch_tracking["batches"]
        )
        print(f"✓ Total cost: ${total_cost:.2f}")

        print("\nNext steps:")
        print("  1. Monitor batches: python scripts/phase1_expansion_batch_scheduler.py status")
        print("  2. When complete: python scripts/phase1_expansion_batch_scheduler.py retrieve-all")

    def check_status(self):
        """Check status of all batches."""
        if not self.batch_tracking["batches"]:
            print("No batches found. Start with: python scripts/phase1_expansion_batch_scheduler.py start")
            return

        print("=" * 80)
        print("PHASE 1 EXPANSION - BATCH STATUS")
        print("=" * 80)

        all_completed = True

        for species, info in self.batch_tracking["batches"].items():
            if info.get("status") == "failed":
                print(f"\n✗ {species}")
                print(f"  Error: {info.get('error')}")
                all_completed = False
                continue

            batch_ids = info.get("batch_ids", [])
            print(f"\n○ {species} ({info.get('disease_count', 0)} diseases)")
            print(f"  Submitted: {info.get('submitted_at', 'N/A')}")

            species_completed = True
            for batch_id in batch_ids:
                try:
                    batch = self.enricher.client.messages.batches.retrieve(batch_id)
                    status_emoji = "🟢" if batch.processing_status == "ended" else "🟡"

                    print(f"  {status_emoji} {batch_id}")
                    print(f"     Status: {batch.processing_status}")
                    print(f"     Succeeded: {batch.request_counts.succeeded} | "
                          f"Errored: {batch.request_counts.errored}")

                    if batch.processing_status != "ended":
                        species_completed = False
                        all_completed = False

                except Exception as e:
                    print(f"  ✗ Error: {e}")
                    species_completed = False
                    all_completed = False

        # Summary
        print("\n" + "=" * 80)
        if all_completed:
            print("✓ ALL BATCHES COMPLETE!")
            print("  Retrieve results: python scripts/phase1_expansion_batch_scheduler.py retrieve-all")
        else:
            print("⏳ Still processing... Check again in 30 minutes")
        print("=" * 80)

        self._save_manifest()

    def retrieve_all_results(self):
        """Retrieve results from all completed batches."""
        print("=" * 80)
        print("PHASE 1 EXPANSION - RESULTS RETRIEVAL")
        print("=" * 80)

        for species, info in self.batch_tracking["batches"].items():
            if info.get("status") == "failed":
                print(f"\n✗ {species}: Failed batch (skipping)")
                continue

            batch_ids = info.get("batch_ids", [])
            for batch_id in batch_ids:
                try:
                    batch = self.enricher.client.messages.batches.retrieve(batch_id)

                    if batch.processing_status != "ended":
                        print(f"\n⚠ {species}: Batch not ready yet")
                        print(f"  Status: {batch.processing_status}")
                        continue

                    print(f"\n✓ {species}")
                    print(f"  Batch: {batch_id}")
                    print(f"  Succeeded: {batch.request_counts.succeeded}")
                    print(f"  Errored: {batch.request_counts.errored}")

                except Exception as e:
                    print(f"\n✗ {species}: Error retrieving batch {batch_id}")
                    print(f"  {e}")

        print("\n" + "=" * 80)
        print("NEXT: Integrate results into main database")
        print("=" * 80)


def main():
    scheduler = Phase1ExpansionScheduler()

    if len(sys.argv) < 2:
        print("Usage: python scripts/phase1_expansion_batch_scheduler.py <command>")
        print("\nCommands:")
        print("  plan          - Show expansion plan")
        print("  start         - Submit all species batches")
        print("  status        - Check batch status")
        print("  retrieve-all  - Retrieve all results")
        sys.exit(1)

    command = sys.argv[1]

    if command == "plan":
        scheduler.show_plan()
    elif command == "start":
        interactive = "--no-interact" not in sys.argv
        scheduler.submit_all_batches(interactive=interactive)
    elif command == "status":
        scheduler.check_status()
    elif command == "retrieve-all":
        scheduler.retrieve_all_results()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
