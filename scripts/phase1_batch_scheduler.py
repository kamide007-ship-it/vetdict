#!/usr/bin/env python3
"""
Phase 1 Batch Scheduler - Automate enrichment for all animal species.

This script orchestrates batch submission for disease enrichment across all species,
starting with high-priority species (high disease count). It manages the lifecycle:
1. Group diseases by species
2. Submit batches in priority order
3. Track completion and results
4. Generate enrichment manifest

Usage:
    # Start Phase 1 enrichment for all species
    python scripts/phase1_batch_scheduler.py start

    # Check status of all active batches
    python scripts/phase1_batch_scheduler.py status

    # Retrieve results from completed batches
    python scripts/phase1_batch_scheduler.py retrieve [batch_id]

    # Show scheduling plan without executing
    python scripts/phase1_batch_scheduler.py plan
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from api.disease_batch_enricher import DiseaseBatchEnricher
from api.disease_content_enricher import DiseaseEnricher
from api.symptom_checker import _DISEASE_DB


class Phase1Scheduler:
    """Orchestrate batch enrichment for all species in priority order."""

    # Species priority (count threshold defines high/medium/low priority)
    SPECIES_PRIORITY = {
        "Horse": 1,      # 736 expected
        "Dog": 2,        # 576 current
        "Cat": 3,        # 516 expected
        "Bird": 4,       # 308 expected
        "Rabbit": 5,     # 271 expected
        "Parakeet": 6,   # 251 expected
    }

    def __init__(self):
        self.enricher = DiseaseBatchEnricher()
        self.status_enricher = DiseaseEnricher()
        self.manifest_path = project_root / "phase1_manifest.json"
        self.batch_tracking = self._load_manifest()

    def _load_manifest(self) -> Dict:
        """Load or create batch tracking manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path, "r") as f:
                return json.load(f)
        return {
            "started_at": None,
            "batches": {},
            "species_order": [],
            "statistics": {}
        }

    def _save_manifest(self):
        """Save batch tracking manifest."""
        with open(self.manifest_path, "w") as f:
            json.dump(self.batch_tracking, f, indent=2)

    def group_by_species(self) -> Dict[str, List[Dict]]:
        """Group all diseases by species."""
        species_groups = {}
        for disease in _DISEASE_DB:
            species = disease.get("species", "Unknown")
            if species not in species_groups:
                species_groups[species] = []
            species_groups[species].append(disease)
        return species_groups

    def get_incomplete_diseases(self, species_diseases: List[Dict]) -> List[Dict]:
        """Filter to only incomplete diseases needing enrichment."""
        incomplete = []
        for disease in species_diseases:
            # Check if all required fields are present and non-empty
            required_fields = ["pathophysiology", "causes", "treatment", "prevention", "prognosis"]
            if not all(disease.get(field) for field in required_fields):
                incomplete.append(disease)
        return incomplete

    def create_scheduling_plan(self) -> Dict[str, Dict]:
        """Create enrichment scheduling plan by species."""
        species_groups = self.group_by_species()

        plan = {}
        for species, diseases in species_groups.items():
            incomplete = self.get_incomplete_diseases(diseases)
            priority = self.SPECIES_PRIORITY.get(species, 999)

            plan[species] = {
                "priority": priority,
                "total_diseases": len(diseases),
                "incomplete_diseases": len(incomplete),
                "complete_diseases": len(diseases) - len(incomplete),
                "completion_percentage": 100 * (len(diseases) - len(incomplete)) / len(diseases) if diseases else 0,
                "estimated_cost": len(incomplete) * 0.025,  # 50% batch discount
                "batch_size": len(incomplete)
            }

        return dict(sorted(plan.items(), key=lambda x: x[1]["priority"]))

    def show_plan(self):
        """Display scheduling plan without executing."""
        plan = self.create_scheduling_plan()

        print("=" * 80)
        print("PHASE 1 BATCH ENRICHMENT SCHEDULE")
        print("=" * 80)
        print("\nSpecies Prioritization (ordered by execution):\n")

        total_incomplete = 0
        total_cost = 0

        for species, info in plan.items():
            if info["incomplete_diseases"] > 0:
                print(f"  {info['priority']}. {species}")
                print(f"     Total: {info['total_diseases']} | Complete: {info['complete_diseases']} | "
                      f"Incomplete: {info['incomplete_diseases']} ({info['completion_percentage']:.1f}% complete)")
                print(f"     Est. Cost: ${info['estimated_cost']:.2f}")
                print()
                total_incomplete += info["incomplete_diseases"]
                total_cost += info["estimated_cost"]

        print("=" * 80)
        print(f"TOTAL DISEASES TO ENRICH: {total_incomplete}")
        print(f"TOTAL ESTIMATED COST: ${total_cost:.2f} (vs ${total_cost * 2:.2f} standard pricing)")
        print(f"SAVINGS WITH BATCH API: ${total_cost:.2f} (50%)")
        print("PROCESSING TIME: 1-6 hours (batches run asynchronously)")
        print("=" * 80)

    def submit_all_batches(self, interactive=True):
        """Submit enrichment batches for all species in priority order."""
        plan = self.create_scheduling_plan()

        self.batch_tracking["started_at"] = datetime.now().isoformat()
        species_to_process = []

        for species, info in plan.items():
            if info["incomplete_diseases"] > 0:
                species_to_process.append((species, info))

        if not species_to_process:
            print("✓ All diseases are complete. No enrichment needed.")
            return

        print("=" * 80)
        print(f"STARTING PHASE 1 ENRICHMENT ({len(species_to_process)} species)")
        print("=" * 80)

        batch_schedule = []

        for priority, (species, info) in enumerate(species_to_process, 1):
            species_diseases = self.group_by_species()[species]
            incomplete = self.get_incomplete_diseases(species_diseases)

            print(f"\n[{priority}/{len(species_to_process)}] {species} ({len(incomplete)} diseases)")
            print(f"    Cost: ${info['estimated_cost']:.2f}")

            if interactive:
                response = input("    Submit batch? (y/n): ").strip().lower()
                if response != "y":
                    print("    ⊘ Skipped")
                    continue

            print("    Submitting...", end=" ", flush=True)

            try:
                # Create batch requests for this species
                batch_requests = self.enricher.create_batch_requests(incomplete)
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
                    "estimated_cost": info["estimated_cost"]
                }

                batch_schedule.append({
                    "species": species,
                    "priority": priority,
                    "batch_ids": batch_ids,
                    "submitted_at": datetime.now().isoformat()
                })

                print(f"✓ {len(batch_ids)} batch(es) submitted")
                print(f"    Batch IDs: {', '.join(batch_ids[:2])}{'...' if len(batch_ids) > 2 else ''}")
                print("    Track with: python scripts/phase1_batch_scheduler.py status")

                # Small delay between submissions to avoid rate limiting
                if priority < len(species_to_process):
                    time.sleep(2)

            except Exception as e:
                print(f"✗ Failed: {e}")
                self.batch_tracking["batches"][species] = {
                    "status": "failed",
                    "error": str(e),
                    "failed_at": datetime.now().isoformat()
                }

        self._save_manifest()

        print("\n" + "=" * 80)
        print("PHASE 1 SUBMISSION COMPLETE")
        print("=" * 80)
        print(f"\nSubmitted {len(batch_schedule)} batches for {len(batch_schedule)} species")
        print(f"Total cost: ${sum(b['estimated_cost'] for b in self.batch_tracking['batches'].values() if 'estimated_cost' in b):.2f}")
        print("\nNext steps:")
        print("  1. Monitor batches with: python scripts/phase1_batch_scheduler.py status")
        print("  2. Retrieve results when ready: python scripts/phase1_batch_scheduler.py retrieve <batch_id>")
        print("  3. Proceed to Phase 2: UI/UX redesign (tabs, filters, AI chat)")

    def check_status(self):
        """Check status of all active batches."""
        if not self.batch_tracking["batches"]:
            print("No batches found. Start with: python scripts/phase1_batch_scheduler.py start")
            return

        print("=" * 80)
        print("PHASE 1 BATCH STATUS")
        print("=" * 80)

        for species, info in self.batch_tracking["batches"].items():
            if info.get("status") == "failed":
                print(f"\n✗ {species}")
                print(f"  Error: {info.get('error')}")
                continue

            batch_ids = info.get("batch_ids", [])
            print(f"\n○ {species}")
            print(f"  Submitted: {info.get('submitted_at', 'N/A')}")

            all_completed = True
            for batch_id in batch_ids:
                try:
                    batch = self.enricher.client.messages.batches.retrieve(batch_id)
                    status_emoji = "🟢" if batch.processing_status == "ended" else "🟡"

                    print(f"  {status_emoji} Batch: {batch_id}")
                    print(f"     Status: {batch.processing_status}")
                    print(f"     Processing: {batch.request_counts.processing} | "
                          f"Succeeded: {batch.request_counts.succeeded} | "
                          f"Errored: {batch.request_counts.errored}")

                    if batch.processing_status != "ended":
                        all_completed = False
                    elif batch.processing_status == "ended":
                        print(f"     ✓ Ready to retrieve: python scripts/phase1_batch_scheduler.py retrieve {batch_id}")

                except Exception as e:
                    print(f"  ✗ Error checking batch {batch_id}: {e}")
                    all_completed = False

            if all_completed and batch_ids:
                self.batch_tracking["batches"][species]["status"] = "completed"

        self._save_manifest()

    def retrieve_results(self, batch_id: str):
        """Retrieve and process results from a completed batch."""
        print(f"Retrieving results for batch: {batch_id}")
        print("=" * 80)

        try:
            batch = self.enricher.client.messages.batches.retrieve(batch_id)

            if batch.processing_status != "ended":
                print(f"✗ Batch not ready. Status: {batch.processing_status}")
                print("Try again later.")
                return

            print("✓ Batch completed!")
            print(f"  Succeeded: {batch.request_counts.succeeded}")
            print(f"  Errored: {batch.request_counts.errored}")

            # Process results
            print("\nProcessing results...")
            enriched_diseases = self.enricher.process_batch_results(batch_id, _DISEASE_DB)

            # Save enriched data
            output_path = project_root / f"enriched_diseases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(enriched_diseases, f, ensure_ascii=False, indent=2)

            print(f"✓ Enriched data saved to: {output_path}")

            # Show enrichment status
            status = self.status_enricher.get_enrichment_status(enriched_diseases)
            print("\n" + "=" * 80)
            print("ENRICHMENT STATUS")
            print("=" * 80)
            print(f"Total diseases: {status['total']}")
            print(f"Complete: {status['complete']} ({status['complete_percentage']}%)")
            print(f"Incomplete: {status['incomplete']}")
            print("\nField Coverage:")
            for field, coverage in status["field_coverage"].items():
                bars = "█" * int(coverage / 5) + "░" * (20 - int(coverage / 5))
                print(f"  {field:20} [{bars}] {coverage}%")

            print("\n" + "=" * 80)
            print("NEXT STEPS FOR PHASE 2")
            print("=" * 80)
            print("1. Review enriched data for quality")
            print("2. Integrate into production database")
            print("3. Implement Phase 2 UI/UX improvements:")
            print("   - Tabbed interface (Overview, Pathophysiology, Causes, etc.)")
            print("   - Search and filter functionality")
            print("   - AI question chat interface")
            print("   - Multi-language support (EN/JA)")

        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()


def main():
    scheduler = Phase1Scheduler()

    if len(sys.argv) < 2:
        print("Usage: python scripts/phase1_batch_scheduler.py <command>")
        print("\nCommands:")
        print("  plan      - Show scheduling plan without executing")
        print("  start     - Start Phase 1 enrichment for all species")
        print("  status    - Check status of active batches")
        print("  retrieve  - Retrieve results from completed batch")
        sys.exit(1)

    command = sys.argv[1]

    if command == "plan":
        scheduler.show_plan()
    elif command == "start":
        interactive = "--no-interact" not in sys.argv
        scheduler.submit_all_batches(interactive=interactive)
    elif command == "status":
        scheduler.check_status()
    elif command == "retrieve":
        if len(sys.argv) < 3:
            print("Error: batch_id required")
            print("Usage: python scripts/phase1_batch_scheduler.py retrieve <batch_id>")
            sys.exit(1)
        scheduler.retrieve_results(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
