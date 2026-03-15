#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 Auto Executor

Monitors batch completion and automatically runs subsequent steps:
1. Batch monitoring
2. Result processing
3. QA validation
4. Database integration
"""

import json
import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import anthropic


class Phase1AutoExecutor:
    """Orchestrates Phase 1 enrichment steps automatically."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.manifest_path = Path(__file__).parent.parent / "phase1_enrichment_manifest.json"
        self.script_dir = Path(__file__).parent

    def load_manifest(self):
        """Load the enrichment manifest."""
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def check_all_batches_complete(self) -> bool:
        """Check if all batches are complete."""
        manifest = self.load_manifest()

        for species, data in manifest["species"].items():
            for batch_id in data.get("batch_ids", []):
                try:
                    batch = self.client.messages.batches.retrieve(batch_id)
                    if batch.processing_status != "succeeded":
                        return False
                except Exception as e:
                    print(f"Error checking batch {batch_id}: {e}")
                    return False

        return True

    def run_script(self, script_name: str, description: str) -> bool:
        """Run a Python script and capture output."""
        script_path = self.script_dir / script_name
        print(f"\n{'='*70}")
        print(f"{description}")
        print(f"{'='*70}")

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=False,
                text=True,
                timeout=1800  # 30 minutes timeout
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"❌ Script {script_name} timed out")
            return False
        except Exception as e:
            print(f"❌ Error running {script_name}: {e}")
            return False

    def wait_for_batches(self, check_interval: int = 60, max_wait_hours: int = 6):
        """Wait for all batches to complete."""
        print("=" * 70)
        print("PHASE 1 AUTO EXECUTOR")
        print("=" * 70)
        print(f"Started: {datetime.now().isoformat()}")
        print(f"Checking batch completion every {check_interval} seconds")
        print(f"Max wait time: {max_wait_hours} hours\n")

        start_time = datetime.now()
        max_wait_seconds = max_wait_hours * 3600
        check_count = 0

        while True:
            elapsed = (datetime.now() - start_time).total_seconds()
            check_count += 1

            print(f"[Check {check_count}] {datetime.now().strftime('%H:%M:%S')} - Checking batch status...")

            try:
                manifest = self.load_manifest()
                all_complete = True
                statuses = {}

                for species, data in manifest["species"].items():
                    for batch_id in data.get("batch_ids", []):
                        batch = self.client.messages.batches.retrieve(batch_id)
                        status = batch.processing_status
                        statuses[species] = status

                        if status == "succeeded":
                            counts = batch.request_counts
                            print(f"  ✅ {species:10s} - COMPLETED ({counts.succeeded} succeeded, {counts.errored} errors)")
                        elif status == "processing":
                            counts = batch.request_counts
                            total = counts.processing + counts.succeeded + counts.errored
                            pct = 100 * (counts.succeeded + counts.errored) / max(total, 1)
                            print(f"  ⏳ {species:10s} - PROCESSING ({pct:.0f}%)")
                            all_complete = False
                        else:
                            print(f"  ⚠️  {species:10s} - {status.upper()}")
                            all_complete = False

                if all_complete:
                    print(f"\n✅ All batches completed!")
                    break

                if elapsed > max_wait_seconds:
                    print(f"\n❌ Max wait time ({max_wait_hours}h) exceeded. Exiting.")
                    return False

                print(f"  Next check in {check_interval}s...\n")
                time.sleep(check_interval)

            except Exception as e:
                print(f"  ❌ Error: {e}")
                print(f"  Next check in {check_interval}s...\n")
                time.sleep(check_interval)

        return True

    def run_all_steps(self):
        """Execute all Phase 1 steps automatically."""
        print("\n" + "=" * 70)
        print("Starting automatic Phase 1 execution pipeline")
        print("=" * 70)

        # Step 1: Wait for batches
        if not self.wait_for_batches(check_interval=60, max_wait_hours=6):
            print("\n❌ Failed to complete batch processing within time limit")
            return False

        # Step 2: Process batch results
        print("\n[Step 1/4] Processing batch results...")
        if not self.run_script("phase1_batch_processor.py", "PHASE 1 BATCH PROCESSOR"):
            print("❌ Batch processing failed")
            return False

        # Step 3: QA Validation
        print("\n[Step 2/4] Running QA validation...")
        if not self.run_script("phase1_qa_validator.py", "PHASE 1 QA VALIDATOR"):
            print("❌ QA validation failed")
            return False

        # Step 4: Database Integration
        print("\n[Step 3/4] Integrating into main database...")
        if not self.run_script("phase1_integration.py", "PHASE 1 INTEGRATION"):
            print("❌ Database integration failed")
            return False

        # Summary
        print("\n" + "=" * 70)
        print("✅ PHASE 1 EXECUTION COMPLETE")
        print("=" * 70)
        print("\nAll steps completed successfully!")
        print("\nNext steps:")
        print("  1. Review enriched database: diseases_all_species.json")
        print("  2. Commit changes:")
        print("     git add diseases_all_species.json")
        print("     git commit -m 'Phase 1 enrichment: 1,252 diseases (Cat + Horse)'")
        print("  3. Push to branch:")
        print("     git push -u origin claude/add-vet-database-bfwB9")

        return True


if __name__ == "__main__":
    executor = Phase1AutoExecutor()
    success = executor.run_all_steps()
    sys.exit(0 if success else 1)
