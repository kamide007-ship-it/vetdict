#!/usr/bin/env python3
"""
Phase 2 Batch Processor - Process and integrate Phase 2 batch results

Handles result retrieval, parsing, validation, and integration into the
disease database for treatment, prevention, and prognosis fields.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from api.phase2_batch_enricher import Phase2BatchEnricher
from api.phase2_qa_validator import Phase2QAValidator


class Phase2BatchProcessor:
    """Process batch results and integrate into disease database."""

    def __init__(self):
        self.enricher = Phase2BatchEnricher()
        self.validator = Phase2QAValidator()
        self.manifest_path = project_root / "phase2_enrichment_manifest.json"
        self.database_path = project_root / "diseases_all_species.json"

    def load_manifest(self) -> Dict:
        """Load enrichment manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path, "r") as f:
                return json.load(f)
        return {}

    def load_diseases(self) -> List[Dict]:
        """Load disease database."""
        with open(self.database_path, "r") as f:
            return json.load(f)

    def save_manifest(self, manifest: Dict):
        """Save manifest."""
        with open(self.manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

    def save_diseases(self, diseases: List[Dict]):
        """Save disease database."""
        with open(self.database_path, "w") as f:
            json.dump(diseases, f, indent=2)

    def process_batch_results(
        self, batch_id: str, stage: str = "treatment"
    ) -> Tuple[int, int, int]:
        """Process results from a single batch and integrate into database.

        Args:
            batch_id: Batch ID to process
            stage: Field stage ("treatment", "prevention", "prognosis")

        Returns:
            (succeeded_count, failed_count, error_count)
        """
        print(f"\n📥 Processing batch: {batch_id[:16]}...")
        print(f"   Stage: {stage}")

        # Check batch status first
        try:
            status = self.enricher.check_batch_status(batch_id)
            if status["status"] != "ended":
                print(f"   ⚠  Batch not ready. Status: {status['status']}")
                return 0, 0, 0
        except Exception as e:
            print(f"   ❌ Error checking batch status: {e}")
            return 0, 0, 1

        # Retrieve results
        try:
            results = self.enricher.retrieve_batch_results(batch_id)
        except Exception as e:
            print(f"   ❌ Error retrieving batch: {e}")
            return 0, 0, 1

        # Load database and manifest
        diseases = self.load_diseases()
        manifest = self.load_manifest()

        # Create disease lookup map for faster access
        disease_map = {d.get("id"): d for d in diseases}

        succeeded = 0
        failed = 0
        error_count = 0

        # Process each result
        for result in results:
            custom_id = result.get("custom_id", "")

            # Extract disease ID from custom_id format: "disease-{id}-{stage}"
            try:
                parts = custom_id.split("-")
                disease_id = "-".join(parts[1:-1])  # Handle IDs with hyphens
            except Exception:
                error_count += 1
                continue

            disease = disease_map.get(disease_id)
            if not disease:
                error_count += 1
                continue

            if result["status"] == "succeeded":
                data = result.get("data", {})

                # Validate required fields
                if stage in data and f"{stage}_ja" in data:
                    en_content = data[stage]
                    ja_content = data[f"{stage}_ja"]

                    # Basic content validation
                    if en_content and ja_content and len(en_content) >= 30 and len(ja_content) >= 30:
                        disease[stage] = en_content
                        disease[f"{stage}_ja"] = ja_content
                        disease["enrichment_phase"] = 2
                        disease["enriched_at"] = datetime.now().isoformat()
                        succeeded += 1
                    else:
                        failed += 1
                else:
                    failed += 1

            elif result["status"] == "parse_error":
                # Try to salvage raw text
                raw_text = result.get("raw_text", "")
                if raw_text and len(raw_text) >= 30:
                    # Store raw text as fallback
                    disease[stage] = raw_text[:250]  # Truncate to reasonable length
                    disease["enrichment_phase"] = 2
                    disease["enriched_at"] = datetime.now().isoformat()
                    succeeded += 1
                else:
                    failed += 1

            else:
                failed += 1

        # Save updates
        self.save_diseases(diseases)

        # Update manifest
        if batch_id in manifest.get("stages", {}).get(stage, {}).get("batches", {}):
            manifest["stages"][stage]["batches"][batch_id]["status"] = "processed"
            manifest["stages"][stage]["batches"][batch_id]["processed_at"] = datetime.now().isoformat()
            manifest["stages"][stage]["batches"][batch_id]["results"] = {
                "succeeded": succeeded,
                "failed": failed,
                "errors": error_count
            }
            self.save_manifest(manifest)

        print(f"   ✓ Processed {len(results)} results")
        print(f"     - Succeeded: {succeeded}")
        print(f"     - Failed: {failed}")
        print(f"     - Errors: {error_count}")

        return succeeded, failed, error_count

    def process_all_completed_batches(self):
        """Automatically process all completed batches."""
        manifest = self.load_manifest()

        if not manifest.get("stages"):
            print("❌ No batches found in manifest")
            return

        print("\n" + "="*70)
        print("PROCESSING ALL COMPLETED BATCHES")
        print("="*70)

        total_succeeded = 0
        total_failed = 0
        total_errors = 0
        processed_count = 0

        for stage_name in ["treatment", "prevention", "prognosis"]:
            stage_data = manifest.get("stages", {}).get(stage_name, {})
            batches = stage_data.get("batches", {})

            if not batches:
                continue

            print(f"\n📋 Stage: {stage_name.upper()}")
            print(f"   Total batches: {len(batches)}")

            for batch_id, batch_info in batches.items():
                # Skip if already processed
                if batch_info.get("status") == "processed":
                    print(f"   ✓ {batch_id[:16]}... already processed")
                    continue

                # Check if batch is complete
                try:
                    status = self.enricher.check_batch_status(batch_id)
                    if status["status"] != "ended":
                        print(f"   ⏳ {batch_id[:16]}... still processing")
                        continue
                except Exception as e:
                    print(f"   ❌ {batch_id[:16]}... error checking status: {e}")
                    continue

                # Process the batch
                succ, fail, errs = self.process_batch_results(batch_id, stage_name)
                total_succeeded += succ
                total_failed += fail
                total_errors += errs
                processed_count += 1

        print(f"\n{'='*70}")
        print("PROCESSING SUMMARY")
        print(f"{'='*70}")
        print(f"Batches processed: {processed_count}")
        print(f"Total succeeded: {total_succeeded}")
        print(f"Total failed: {total_failed}")
        print(f"Total errors: {total_errors}")

    def validate_processed_data(self):
        """Run QA validation on processed Phase 2 data."""
        print("\n" + "="*70)
        print("VALIDATING PHASE 2 DATA QUALITY")
        print("="*70)

        diseases = self.load_diseases()
        report = self.validator.run_full_validation(diseases)
        self.validator.print_validation_report(report)

        return report

    def generate_summary(self):
        """Generate Phase 2 processing summary."""
        manifest = self.load_manifest()
        diseases = self.load_diseases()

        print("\n" + "="*70)
        print("PHASE 2 ENRICHMENT SUMMARY")
        print("="*70)

        # Count enriched diseases
        enriched_counts = {
            "treatment": 0,
            "prevention": 0,
            "prognosis": 0
        }

        for disease in diseases:
            for field in enriched_counts:
                if disease.get(field) and disease.get(f"{field}_ja"):
                    enriched_counts[field] += 1

        print(f"\nTotal diseases: {len(diseases)}")
        for field, count in enriched_counts.items():
            pct = 100 * count / len(diseases)
            print(f"  {field:12}: {count:5} ({pct:5.1f}%)")

        # Batch statistics
        print("\nBatch Statistics:")
        for stage_name in ["treatment", "prevention", "prognosis"]:
            stage_data = manifest.get("stages", {}).get(stage_name, {})
            stage_data.get("batches", {})
            stats = stage_data.get("stats", {})

            print(f"\n  {stage_name.upper()}")
            print(f"    Submitted: {stats.get('submitted', 0)}")
            print(f"    Completed: {stats.get('completed', 0)}")
            print(f"    Status: {stage_data.get('status', 'unknown')}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Phase 2 Batch Processor")
    subparsers = parser.add_subparsers(dest="command")

    # process command
    process_parser = subparsers.add_parser("process", help="Process batch results")
    process_parser.add_argument("batch_id", help="Batch ID to process")
    process_parser.add_argument("--stage", default="treatment",
                                choices=["treatment", "prevention", "prognosis"])

    # process-all command
    subparsers.add_parser("process-all", help="Process all completed batches")

    # validate command
    subparsers.add_parser("validate", help="Validate Phase 2 data quality")

    # summary command
    subparsers.add_parser("summary", help="Generate enrichment summary")

    args = parser.parse_args()

    processor = Phase2BatchProcessor()

    if args.command == "process":
        processor.process_batch_results(args.batch_id, args.stage)
    elif args.command == "process-all":
        processor.process_all_completed_batches()
    elif args.command == "validate":
        processor.validate_processed_data()
    elif args.command == "summary":
        processor.generate_summary()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
