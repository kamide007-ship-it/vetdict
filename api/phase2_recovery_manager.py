#!/usr/bin/env python3
"""
Phase 2 Recovery Manager - Handle failures and provide fault tolerance

Implements checkpoint system, retry logic, and resume capability for robust
Phase 2 batch processing.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class Phase2RecoveryManager:
    """Manage checkpoints, retries, and recovery for Phase 2 processing."""

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.manifest_path = self.project_root / "phase2_enrichment_manifest.json"
        self.recovery_state_path = self.project_root / "phase2_recovery_state.json"
        self.database_path = self.project_root / "diseases_all_species.json"

    def load_manifest(self) -> Dict:
        """Load enrichment manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path, "r") as f:
                return json.load(f)
        return {}

    def save_manifest(self, manifest: Dict):
        """Save manifest."""
        with open(self.manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

    def load_recovery_state(self) -> Dict:
        """Load recovery state."""
        if self.recovery_state_path.exists():
            with open(self.recovery_state_path, "r") as f:
                return json.load(f)
        return {
            "checkpoints": [],
            "failed_batches": [],
            "last_recovery": None
        }

    def save_recovery_state(self, state: Dict):
        """Save recovery state."""
        with open(self.recovery_state_path, "w") as f:
            json.dump(state, f, indent=2)

    def create_checkpoint(self, stage: str, batch_num: int, batch_id: str):
        """Create a checkpoint after successful batch processing.

        Args:
            stage: Processing stage ("treatment", "prevention", "prognosis")
            batch_num: Batch number processed
            batch_id: Batch ID
        """
        state = self.load_recovery_state()

        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "stage": stage,
            "batch_num": batch_num,
            "batch_id": batch_id,
            "status": "completed"
        }

        state["checkpoints"].append(checkpoint)
        state["last_checkpoint"] = checkpoint
        self.save_recovery_state(state)

        print(f"✓ Checkpoint created: {stage} batch {batch_num}")

    def mark_failed_batch(self, batch_id: str, error: str, stage: str):
        """Mark a batch as failed for retry.

        Args:
            batch_id: Batch ID that failed
            error: Error message
            stage: Processing stage
        """
        state = self.load_recovery_state()

        failed = {
            "batch_id": batch_id,
            "stage": stage,
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "retry_count": 0
        }

        state["failed_batches"].append(failed)
        self.save_recovery_state(state)

        print(f"⚠  Marked batch {batch_id[:16]}... as failed: {error}")

    def get_failed_batches(self, stage: str = None, max_retries: int = 3) -> List[Dict]:
        """Get list of failed batches eligible for retry.

        Args:
            stage: Filter by stage ("treatment", "prevention", "prognosis")
            max_retries: Max retry attempts before giving up

        Returns:
            List of failed batch dicts
        """
        state = self.load_recovery_state()
        eligible = []

        for failed in state.get("failed_batches", []):
            if failed.get("retry_count", 0) >= max_retries:
                continue  # Too many retries

            if stage and failed.get("stage") != stage:
                continue  # Different stage

            eligible.append(failed)

        return eligible

    def increment_retry_count(self, batch_id: str):
        """Increment retry count for a failed batch.

        Args:
            batch_id: Batch ID to retry
        """
        state = self.load_recovery_state()

        for failed in state.get("failed_batches", []):
            if failed.get("batch_id") == batch_id:
                failed["retry_count"] = failed.get("retry_count", 0) + 1
                break

        self.save_recovery_state(state)

    def can_resume_from_checkpoint(self, stage: str) -> Optional[Dict]:
        """Check if processing can resume from a checkpoint.

        Args:
            stage: Processing stage to check

        Returns:
            Checkpoint dict if can resume, None otherwise
        """
        state = self.load_recovery_state()
        checkpoints = state.get("checkpoints", [])

        if not checkpoints:
            return None

        # Find last checkpoint for this stage
        for checkpoint in reversed(checkpoints):
            if checkpoint.get("stage") == stage:
                return checkpoint

        return None

    def get_resume_batch_number(self, stage: str) -> int:
        """Get the batch number to resume from.

        Args:
            stage: Processing stage

        Returns:
            Next batch number to process (0 if starting fresh)
        """
        checkpoint = self.can_resume_from_checkpoint(stage)

        if not checkpoint:
            return 0

        # Resume from next batch after checkpoint
        return checkpoint.get("batch_num", 0) + 1

    def get_recovery_report(self) -> Dict:
        """Generate a recovery status report.

        Returns:
            Report dictionary
        """
        manifest = self.load_manifest()
        state = self.load_recovery_state()

        report = {
            "timestamp": datetime.now().isoformat(),
            "phase": 2,
            "manifest_status": manifest.get("current_stage", "not_started"),
            "batches_submitted": 0,
            "batches_completed": 0,
            "failed_batches": len(state.get("failed_batches", [])),
            "checkpoints": len(state.get("checkpoints", [])),
            "last_checkpoint": state.get("last_checkpoint"),
            "stages_status": {}
        }

        # Get status by stage
        for stage_name in ["treatment", "prevention", "prognosis"]:
            stage_data = manifest.get("stages", {}).get(stage_name, {})
            batches = stage_data.get("batches", {})

            submitted = sum(1 for b in batches.values() if b.get("status") in ["submitted", "processing", "completed"])
            completed = sum(1 for b in batches.values() if b.get("status") == "completed")

            report["stages_status"][stage_name] = {
                "submitted": submitted,
                "completed": completed,
                "status": stage_data.get("status")
            }
            report["batches_submitted"] += submitted
            report["batches_completed"] += completed

        # Failed batches details
        report["failed_batch_details"] = []
        for failed in state.get("failed_batches", [])[:5]:  # Show last 5
            report["failed_batch_details"].append({
                "batch_id": failed.get("batch_id"),
                "stage": failed.get("stage"),
                "retry_count": failed.get("retry_count", 0),
                "error": failed.get("error")
            })

        return report

    def print_recovery_report(self, report: Dict):
        """Print formatted recovery report.

        Args:
            report: Report dictionary from get_recovery_report()
        """
        print("\n" + "="*70)
        print("PHASE 2 RECOVERY STATUS REPORT")
        print("="*70)
        print(f"Generated: {report['timestamp']}")
        print(f"Current Status: {report['manifest_status']}")

        print(f"\nBatch Statistics:")
        print(f"  Submitted: {report['batches_submitted']}")
        print(f"  Completed: {report['batches_completed']}")
        print(f"  Failed: {report['failed_batches']}")
        print(f"  Checkpoints: {report['checkpoints']}")

        print(f"\nStage Status:")
        for stage_name, stage_status in report["stages_status"].items():
            print(f"  {stage_name:12}: {stage_status['submitted']:3} submitted, "
                  f"{stage_status['completed']:3} completed "
                  f"({stage_status['status']})")

        if report["failed_batch_details"]:
            print(f"\nFailed Batches (Recent):")
            for failed in report["failed_batch_details"]:
                print(f"  {failed['batch_id'][:16]}... ({failed['stage']})")
                print(f"    Retries: {failed['retry_count']}, Error: {failed['error'][:50]}")

        last_checkpoint = report.get("last_checkpoint")
        if last_checkpoint:
            print(f"\nLast Checkpoint:")
            print(f"  Stage: {last_checkpoint.get('stage')}")
            print(f"  Batch: {last_checkpoint.get('batch_num')}")
            print(f"  Time: {last_checkpoint.get('timestamp')}")

        print("\n" + "="*70)

    def cleanup_old_checkpoints(self, keep_count: int = 20):
        """Clean up old checkpoints, keeping only recent ones.

        Args:
            keep_count: Number of recent checkpoints to keep
        """
        state = self.load_recovery_state()

        checkpoints = state.get("checkpoints", [])
        if len(checkpoints) > keep_count:
            removed = len(checkpoints) - keep_count
            state["checkpoints"] = checkpoints[-keep_count:]
            self.save_recovery_state(state)
            print(f"✓ Cleaned up {removed} old checkpoints")

    def cleanup_resolved_failures(self):
        """Remove failed batches that have been successfully recovered.

        This checks the manifest to see if previously failed batches
        are now marked as completed.
        """
        manifest = self.load_manifest()
        state = self.load_recovery_state()

        resolved = 0
        remaining_failures = []

        for failed in state.get("failed_batches", []):
            batch_id = failed.get("batch_id")
            stage = failed.get("stage")

            # Check if batch is now completed in manifest
            batches = manifest.get("stages", {}).get(stage, {}).get("batches", {})
            batch_info = batches.get(batch_id, {})

            if batch_info.get("status") == "completed":
                resolved += 1
            else:
                remaining_failures.append(failed)

        state["failed_batches"] = remaining_failures
        self.save_recovery_state(state)

        if resolved > 0:
            print(f"✓ Removed {resolved} resolved failures from recovery queue")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Phase 2 Recovery Manager")
    subparsers = parser.add_subparsers(dest="command")

    # status command
    subparsers.add_parser("status", help="Show recovery status")

    # cleanup command
    subparsers.add_parser("cleanup", help="Clean up old checkpoints and resolved failures")

    args = parser.parse_args()

    manager = Phase2RecoveryManager()

    if args.command == "status":
        report = manager.get_recovery_report()
        manager.print_recovery_report(report)
    elif args.command == "cleanup":
        manager.cleanup_old_checkpoints()
        manager.cleanup_resolved_failures()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
