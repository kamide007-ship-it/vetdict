#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 Batch Monitor

Monitors the status of submitted batches and provides real-time updates.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import anthropic


class Phase1BatchMonitor:
    """Monitors Phase 1 batch processing status."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.manifest_path = Path(__file__).parent.parent / "phase1_enrichment_manifest.json"

    def load_manifest(self):
        """Load the enrichment manifest."""
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def check_batch_status(self, batch_id):
        """Check status of a single batch."""
        try:
            batch = self.client.messages.batches.retrieve(batch_id)
            return {
                "id": batch.id,
                "status": batch.processing_status,
                "request_counts": {
                    "processing": batch.request_counts.processing,
                    "succeeded": batch.request_counts.succeeded,
                    "errored": batch.request_counts.errored,
                },
            }
        except Exception as e:
            return {"id": batch_id, "status": "error", "error": str(e)}

    def monitor_phase1(self, interval=30, max_wait_hours=6):
        """Monitor Phase 1 batches until completion."""
        manifest = self.load_manifest()
        start_time = datetime.now()
        max_wait_seconds = max_wait_hours * 3600

        print("=" * 70)
        print("PHASE 1 BATCH MONITOR")
        print("=" * 70)
        print(f"Started: {start_time.isoformat()}")
        print(f"Max wait: {max_wait_hours} hours\n")

        all_batches = {}

        # Collect all batch IDs
        for species, data in manifest["species"].items():
            for batch_id in data.get("batch_ids", []):
                all_batches[batch_id] = {"species": species, "status": "unknown"}

        if not all_batches:
            print("❌ No batches found in manifest. Run phase1_enrichment_runner.py first.")
            return

        print(f"Monitoring {len(all_batches)} batches...\n")

        completed_batches = {}
        datetime.now()

        while True:
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > max_wait_seconds:
                print(f"\n⏱️  Max wait time ({max_wait_hours}h) exceeded. Exiting.")
                break

            # Check all batches
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking batch statuses...\n")
            all_completed = True

            for batch_id, batch_info in all_batches.items():
                status_info = self.check_batch_status(batch_id)
                species = batch_info["species"]

                if status_info.get("error"):
                    print(f"  ❌ {species:10s} {batch_id[:20]}... - ERROR: {status_info['error']}")
                    all_completed = False
                else:
                    status = status_info["status"]
                    counts = status_info.get("request_counts", {})
                    total = counts.get("processing", 0) + counts.get("succeeded", 0) + counts.get("errored", 0)

                    if status == "processing":
                        pct = 100 * (counts.get("succeeded", 0) + counts.get("errored", 0)) / max(total, 1)
                        print(f"  ⏳ {species:10s} {batch_id[:20]}... - PROCESSING ({pct:.0f}% complete)")
                        all_completed = False
                    elif status == "succeeded":
                        print(
                            f"  ✅ {species:10s} {batch_id[:20]}... - COMPLETED ({counts.get('succeeded', 0)} succeeded, {counts.get('errored', 0)} errors)"
                        )
                        completed_batches[batch_id] = status_info
                    else:
                        print(f"  ⚠️  {species:10s} {batch_id[:20]}... - {status.upper()}")
                        if status not in ["processing", "succeeded"]:
                            all_completed = False

                all_batches[batch_id]["status"] = status_info.get("status", "unknown")

            if all_completed:
                print("\n" + "=" * 70)
                print("✅ ALL BATCHES COMPLETED!")
                print("=" * 70)
                print(f"\nCompleted batches: {len(completed_batches)}")
                for _batch_id, info in completed_batches.items():
                    counts = info.get("request_counts", {})
                    print(f"  - {info['id'][:40]}...")
                    print(f"    Succeeded: {counts.get('succeeded', 0)}, Errored: {counts.get('errored', 0)}")
                break

            # Wait before next check
            print(f"\nNext check in {interval}s... (press Ctrl+C to cancel)")
            try:
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\n\n⏸️  Monitoring paused by user.")
                break

        print(f"\nElapsed time: {(datetime.now() - start_time).total_seconds() / 60:.1f} minutes")
        print("\nNext steps:")
        print("  python3 scripts/phase1_batch_processor.py  # Retrieve and process results")


if __name__ == "__main__":
    monitor = Phase1BatchMonitor()
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 30  # Default 30 seconds between checks
    monitor.monitor_phase1(interval=interval)
