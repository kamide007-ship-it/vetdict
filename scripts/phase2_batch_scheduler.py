#!/usr/bin/env python3
"""
Phase 2 Batch Scheduler - Orchestrate treatment, prevention, prognosis enrichment

Manages batch submission and monitoring for Phase 2 enrichment across all species.
Implements species-staged scheduling for better control and monitoring.

Usage:
    # Show scheduling plan without executing
    python scripts/phase2_batch_scheduler.py plan

    # Start Phase 2 enrichment
    python scripts/phase2_batch_scheduler.py start [--stage treatment|prevention|prognosis]

    # Monitor batch progress
    python scripts/phase2_batch_scheduler.py status [--verbose]

    # Retrieve and integrate results
    python scripts/phase2_batch_scheduler.py retrieve [batch_id]

    # Run QA validation
    python scripts/phase2_batch_scheduler.py validate
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import argparse

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from api.phase2_batch_enricher import Phase2BatchEnricher
from api.symptom_checker import _DISEASE_DB


class Phase2Scheduler:
    """Orchestrate Phase 2 enrichment for all species in priority order."""

    # Species priority by disease count (high volume first)
    SPECIES_PRIORITY = [
        ("Others", 2148),
        ("Horse", 736),
        ("Cat", 516),
        ("Bird", 308),
        ("Rabbit", 271),
        ("Parakeet", 251),
    ]

    # Batch size per request (100 diseases per batch for manageability)
    BATCH_SIZE = 100

    def __init__(self):
        self.enricher = Phase2BatchEnricher()
        self.manifest_path = project_root / "phase2_enrichment_manifest.json"
        self.database_path = project_root / "diseases_all_species.json"
        self.manifest = self._load_manifest()
        self.diseases = self._load_diseases()

    def _load_manifest(self) -> Dict:
        """Load or create Phase 2 enrichment manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path, "r") as f:
                manifest = json.load(f)
                print(f"✓ Loaded existing manifest from {self.manifest_path.name}")
                return manifest

        # Create new manifest
        manifest = {
            "phase": 2,
            "started_at": None,
            "current_stage": None,
            "stages": {
                "treatment": {
                    "status": "pending",
                    "batches": {},
                    "stats": {"total": 0, "submitted": 0, "completed": 0}
                },
                "prevention": {
                    "status": "pending",
                    "batches": {},
                    "stats": {"total": 0, "submitted": 0, "completed": 0}
                },
                "prognosis": {
                    "status": "pending",
                    "batches": {},
                    "stats": {"total": 0, "submitted": 0, "completed": 0}
                }
            },
            "species_status": {},
            "recovery_state": {
                "last_successful_batch": None,
                "last_checkpoint": None
            }
        }

        print(f"✓ Created new manifest")
        return manifest

    def _load_diseases(self) -> List[Dict]:
        """Load diseases from database."""
        with open(self.database_path, "r") as f:
            diseases = json.load(f)
        print(f"✓ Loaded {len(diseases)} diseases from database")
        return diseases

    def _save_manifest(self):
        """Save manifest to file."""
        with open(self.manifest_path, "w") as f:
            json.dump(self.manifest, f, indent=2)
        print(f"✓ Manifest saved to {self.manifest_path.name}")

    def _save_diseases(self):
        """Save enriched diseases back to database."""
        with open(self.database_path, "w") as f:
            json.dump(self.diseases, f, indent=2)
        print(f"✓ Database saved ({len(self.diseases)} diseases)")

    def group_by_species(self) -> Dict[str, List[Dict]]:
        """Group all diseases by species."""
        species_groups = {}
        for disease in self.diseases:
            species = disease.get("species", "Others")
            if species not in species_groups:
                species_groups[species] = []
            species_groups[species].append(disease)
        return species_groups

    def get_incomplete_diseases(self, diseases: List[Dict], stage: str) -> List[Dict]:
        """Filter to diseases needing Phase 2 enrichment for given stage."""
        incomplete = []
        field = stage  # "treatment", "prevention", "prognosis"

        for disease in diseases:
            # Include if field is missing or empty
            if not disease.get(field) or not disease.get(f"{field}_ja"):
                incomplete.append(disease)

        return incomplete

    def create_scheduling_plan(self) -> Dict[str, Dict]:
        """Create enrichment scheduling plan by species and stage."""
        species_groups = self.group_by_species()
        plan = {}

        stages = ["treatment", "prevention", "prognosis"]

        for stage in stages:
            plan[stage] = {
                "stage": stage,
                "total_diseases": 0,
                "species_details": []
            }

            # Sort by priority
            for species_name, _ in self.SPECIES_PRIORITY:
                if species_name not in species_groups:
                    continue

                diseases = species_groups[species_name]
                incomplete = self.get_incomplete_diseases(diseases, stage)

                if incomplete:
                    num_batches = (len(incomplete) + self.BATCH_SIZE - 1) // self.BATCH_SIZE
                    plan[stage]["species_details"].append({
                        "species": species_name,
                        "disease_count": len(incomplete),
                        "batch_count": num_batches,
                        "batch_size": self.BATCH_SIZE
                    })
                    plan[stage]["total_diseases"] += len(incomplete)

        return plan

    def show_plan(self):
        """Display enrichment scheduling plan."""
        plan = self.create_scheduling_plan()

        print("\n" + "="*70)
        print("PHASE 2 ENRICHMENT SCHEDULING PLAN")
        print("="*70)

        for stage_name in ["treatment", "prevention", "prognosis"]:
            stage_plan = plan[stage_name]
            print(f"\n📋 STAGE: {stage_name.upper()}")
            print(f"   Total diseases to enrich: {stage_plan['total_diseases']}")

            for sp_detail in stage_plan["species_details"]:
                print(f"\n   {sp_detail['species']}")
                print(f"   ├─ Diseases: {sp_detail['disease_count']}")
                print(f"   ├─ Batches: {sp_detail['batch_count']} (size: {sp_detail['batch_size']})")
                cost = sp_detail["disease_count"] * 0.025  # ~$0.025 per disease
                print(f"   └─ Est. cost: ${cost:.2f}")

        print("\n" + "="*70)
        print("EXECUTION SEQUENCE")
        print("="*70)
        print("""
1. treatment (治療): Treatment protocols and medication approaches
2. prevention (予防): Preventive measures and vaccination strategies
3. prognosis (予後): Expected outcomes and recovery timelines

Total estimated cost: $450-550
Total estimated time: 8-12 hours of API processing
""")

    def start_enrichment(self, stage: str = None, max_batches: int = None):
        """Start Phase 2 enrichment batch submissions.

        Args:
            stage: Specific stage to enrich ("treatment", "prevention", "prognosis")
                  If None, starts with "treatment"
            max_batches: Maximum batches to submit (for testing)
        """
        if not stage:
            stage = "treatment"

        if stage not in ["treatment", "prevention", "prognosis"]:
            print(f"❌ Invalid stage: {stage}")
            return

        print(f"\n{'='*70}")
        print(f"PHASE 2 ENRICHMENT - STAGE: {stage.upper()}")
        print(f"{'='*70}")

        # Initialize manifest if needed
        if not self.manifest.get("started_at"):
            self.manifest["started_at"] = datetime.now().isoformat()

        self.manifest["current_stage"] = stage

        species_groups = self.group_by_species()
        total_submitted = 0
        batch_counter = 0

        # Process each species in priority order
        for species_name, _ in self.SPECIES_PRIORITY:
            if species_name not in species_groups:
                continue

            diseases = species_groups[species_name]
            incomplete = self.get_incomplete_diseases(diseases, stage)

            if not incomplete:
                print(f"\n✓ {species_name}: All {len(diseases)} diseases already enriched")
                continue

            print(f"\n📤 {species_name}: Enriching {len(incomplete)} diseases")

            # Create batches for this species
            batches = self.enricher.create_phase2_batch_requests(
                incomplete, stage=stage, batch_size=self.BATCH_SIZE
            )

            if max_batches and batch_counter >= max_batches:
                print(f"   (Stopping at {max_batches} batches for testing)")
                break

            # Submit each batch
            for batch_num, batch_requests in enumerate(batches, 1):
                batch_counter += 1

                try:
                    batch_id = self.enricher.submit_batch(
                        batch_requests,
                        description=f"{species_name} {stage} batch {batch_num}/{len(batches)}"
                    )

                    # Track batch in manifest
                    self.manifest["stages"][stage]["batches"][batch_id] = {
                        "species": species_name,
                        "batch_num": batch_num,
                        "total_batches": len(batches),
                        "disease_count": len(batch_requests),
                        "submitted_at": datetime.now().isoformat(),
                        "status": "submitted",
                        "results": None
                    }

                    total_submitted += len(batch_requests)
                    self.manifest["stages"][stage]["stats"]["submitted"] += 1

                    # Brief pause between submissions to avoid rate limits
                    if batch_counter < (batch_counter + 1):  # Not the last batch
                        time.sleep(2)

                except Exception as e:
                    print(f"   ❌ Error submitting batch: {e}")
                    continue

            # Update species status
            self.manifest["species_status"][species_name] = {
                "stage": stage,
                "incomplete_count": len(incomplete),
                "batches_submitted": len(batches),
                "status": "submitted"
            }

        print(f"\n{'='*70}")
        print(f"SUBMISSION SUMMARY")
        print(f"{'='*70}")
        print(f"Stage: {stage}")
        print(f"Batches submitted: {batch_counter}")
        print(f"Total diseases: {total_submitted}")
        print(f"Est. cost: ${total_submitted * 0.025:.2f}")
        print(f"Est. time: 1-8 hours (async processing)")

        # Save manifest
        self.manifest["stages"][stage]["status"] = "in_progress"
        self._save_manifest()

    def show_status(self, verbose: bool = False):
        """Show current status of all batches."""
        if not self.manifest.get("stages"):
            print("❌ No batches found. Run 'start' command first.")
            return

        print(f"\n{'='*70}")
        print(f"PHASE 2 BATCH STATUS")
        print(f"{'='*70}")

        for stage_name in ["treatment", "prevention", "prognosis"]:
            stage_data = self.manifest["stages"].get(stage_name, {})
            batches = stage_data.get("batches", {})
            stats = stage_data.get("stats", {})

            print(f"\n📊 {stage_name.upper()}")
            print(f"   Status: {stage_data.get('status', 'unknown')}")
            print(f"   Submitted: {stats.get('submitted', 0)} batches")
            print(f"   Completed: {stats.get('completed', 0)} batches")

            if verbose:
                for batch_id, batch_info in batches.items():
                    print(f"\n   Batch: {batch_id}")
                    print(f"   ├─ Species: {batch_info.get('species')}")
                    print(f"   ├─ Diseases: {batch_info.get('disease_count')}")
                    print(f"   ├─ Status: {batch_info.get('status')}")
                    print(f"   └─ Submitted: {batch_info.get('submitted_at')}")

                    # Check batch status from API
                    try:
                        api_status = self.enricher.check_batch_status(batch_id)
                        print(f"       API Status: {api_status['status']}")
                        print(f"       Processed: {api_status['request_counts']['processed']}")
                        print(f"       Succeeded: {api_status['request_counts']['succeeded']}")
                        if api_status['request_counts']['errored'] > 0:
                            print(f"       Errored: {api_status['request_counts']['errored']}")
                    except Exception as e:
                        print(f"       Error checking API status: {e}")

    def retrieve_results(self, batch_id: str = None):
        """Retrieve and integrate results from completed batches."""
        print(f"\n{'='*70}")
        print(f"PHASE 2 RESULT RETRIEVAL")
        print(f"{'='*70}")

        if batch_id:
            # Retrieve specific batch
            print(f"\n📥 Retrieving batch: {batch_id}")
            self._retrieve_single_batch(batch_id)
        else:
            # Retrieve all completed batches
            print(f"\n📥 Checking for completed batches...")
            retrieved_count = 0

            for stage_name in ["treatment", "prevention", "prognosis"]:
                batches = self.manifest["stages"][stage_name].get("batches", {})
                for bid, batch_info in batches.items():
                    if batch_info.get("status") == "completed":
                        continue  # Already retrieved

                    try:
                        status = self.enricher.check_batch_status(bid)
                        if status["status"] == "ended":
                            print(f"   ✓ Batch {bid[:8]}... is complete")
                            self._retrieve_single_batch(bid)
                            retrieved_count += 1
                    except Exception as e:
                        print(f"   Error checking batch {bid[:8]}...: {e}")

            if retrieved_count == 0:
                print("   No completed batches found. Check status with 'status' command.")

    def _retrieve_single_batch(self, batch_id: str):
        """Retrieve results from a single batch and integrate into database."""
        try:
            print(f"   Retrieving results...")
            results = self.enricher.retrieve_batch_results(batch_id)

            # Find batch info in manifest
            batch_info = None
            stage_name = None
            for stage, stage_data in self.manifest["stages"].items():
                if batch_id in stage_data.get("batches", {}):
                    batch_info = stage_data["batches"][batch_id]
                    stage_name = stage
                    break

            if not batch_info:
                print(f"   ❌ Batch {batch_id} not found in manifest")
                return

            # Process and integrate results
            succeeded = 0
            failed = 0

            for result in results:
                custom_id = result["custom_id"]
                disease_id = custom_id.split("-")[1] if "-" in custom_id else None

                # Find disease in database
                disease = None
                for d in self.diseases:
                    if d.get("id") == disease_id:
                        disease = d
                        break

                if not disease:
                    failed += 1
                    continue

                # Integrate data if successful
                if result["status"] == "succeeded":
                    data = result.get("data", {})
                    for field in [stage_name, f"{stage_name}_ja"]:
                        if field in data:
                            disease[field] = data[field]
                            if "enriched_at" not in disease:
                                disease["enriched_at"] = datetime.now().isoformat()
                            disease["enrichment_phase"] = 2
                    succeeded += 1
                else:
                    failed += 1

            print(f"   ✓ Processed: {succeeded + failed} results")
            print(f"     - Succeeded: {succeeded}")
            print(f"     - Failed: {failed}")

            # Update manifest
            batch_info["status"] = "completed"
            batch_info["results"] = {
                "succeeded": succeeded,
                "failed": failed
            }
            batch_info["completed_at"] = datetime.now().isoformat()

            self.manifest["stages"][stage_name]["stats"]["completed"] += 1
            self.manifest["recovery_state"]["last_successful_batch"] = batch_id
            self.manifest["recovery_state"]["last_checkpoint"] = datetime.now().isoformat()

            # Save updates
            self._save_manifest()
            self._save_diseases()
            print(f"   ✓ Database updated and saved")

        except Exception as e:
            print(f"   ❌ Error retrieving batch: {e}")

    def validate_quality(self):
        """Run QA validation on Phase 2 enriched data."""
        print(f"\n{'='*70}")
        print(f"PHASE 2 QUALITY ASSURANCE VALIDATION")
        print(f"{'='*70}")

        from api.phase2_qa_validator import Phase2QAValidator
        validator = Phase2QAValidator()

        # Sample validation
        sample_size = min(100, len(self.diseases) // 10)
        print(f"\n Sampling {sample_size} diseases for validation...")

        # Get diverse sample
        import random
        sample = random.sample(self.diseases, sample_size)

        results = {
            "total_sampled": sample_size,
            "treatments": {"present": 0, "absent": 0},
            "prevention": {"present": 0, "absent": 0},
            "prognosis": {"present": 0, "absent": 0},
        }

        for disease in sample:
            for field in ["treatment", "prevention", "prognosis"]:
                if disease.get(field) and disease.get(f"{field}_ja"):
                    results[field]["present"] += 1
                else:
                    results[field]["absent"] += 1

        # Print results
        print(f"\nValidation Results:")
        for field in ["treatment", "prevention", "prognosis"]:
            present = results[field]["present"]
            total = results[field]["present"] + results[field]["absent"]
            pct = 100 * present / total if total > 0 else 0
            print(f"  {field}: {present}/{total} present ({pct:.1f}%)")

        print(f"\n✓ Validation complete")


def main():
    parser = argparse.ArgumentParser(description="Phase 2 Disease Enrichment Scheduler")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # plan command
    subparsers.add_parser("plan", help="Show scheduling plan without executing")

    # start command
    start_parser = subparsers.add_parser("start", help="Start Phase 2 enrichment")
    start_parser.add_argument("--stage", choices=["treatment", "prevention", "prognosis"],
                             default="treatment", help="Which stage to process")
    start_parser.add_argument("--max-batches", type=int, help="Max batches to submit (for testing)")

    # status command
    status_parser = subparsers.add_parser("status", help="Show batch status")
    status_parser.add_argument("--verbose", action="store_true", help="Show detailed info")

    # retrieve command
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve batch results")
    retrieve_parser.add_argument("batch_id", nargs="?", help="Specific batch ID to retrieve")

    # validate command
    subparsers.add_parser("validate", help="Run QA validation")

    args = parser.parse_args()

    scheduler = Phase2Scheduler()

    if args.command == "plan":
        scheduler.show_plan()
    elif args.command == "start":
        scheduler.start_enrichment(stage=args.stage, max_batches=args.max_batches)
    elif args.command == "status":
        scheduler.show_status(verbose=args.verbose)
    elif args.command == "retrieve":
        scheduler.retrieve_results(batch_id=args.batch_id)
    elif args.command == "validate":
        scheduler.validate_quality()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
