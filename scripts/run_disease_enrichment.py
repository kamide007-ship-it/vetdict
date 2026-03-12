#!/usr/bin/env python3
"""
Run disease content enrichment batch.

This script enriches all incomplete diseases using Claude API Batches (50% cost reduction).
Batches process asynchronously and can take 1-6 hours to complete.

Usage:
    # Check batches status
    python scripts/run_disease_enrichment.py status batch_id_1 batch_id_2

    # Submit new batch
    python scripts/run_disease_enrichment.py submit

    # Retrieve results
    python scripts/run_disease_enrichment.py retrieve batch_id
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from api.disease_batch_enricher import DiseaseBatchEnricher
from api.symptom_checker import _DISEASE_DB


def save_batch_manifest(batch_ids: list):
    """Save batch IDs to a manifest file for tracking."""
    manifest_path = Path(__file__).parent.parent / "enrichment_manifest.json"

    manifest = {"timestamp": datetime.now().isoformat(), "batch_ids": batch_ids}

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"✓ Batch manifest saved to {manifest_path}")
    print(f"  Track batches with: python scripts/run_disease_enrichment.py status {' '.join(batch_ids)}")


def cmd_submit():
    """Submit a new batch for enrichment."""
    print("=" * 70)
    print("Disease Content Enrichment - Batch Submission")
    print("=" * 70)

    enricher = DiseaseBatchEnricher()

    # Create batch requests
    print(f"\nPreparing batch from {len(_DISEASE_DB)} diseases...")
    batches = enricher.create_batch_requests(_DISEASE_DB)
    total_requests = sum(len(b) for b in batches)

    print(f"✓ {len(batches)} batch(es) created with {total_requests} requests")
    print(f"  Estimated cost: ~${total_requests * 0.025:.2f} (50% batch discount)")
    print(f"  Processing time: 1-6 hours\n")

    # Submit batches
    batch_ids = []
    for i, batch_requests in enumerate(batches):
        print(f"Submitting batch {i+1}/{len(batches)}...")
        batch_id = enricher.submit_batch(batch_requests)
        batch_ids.append(batch_id)

    # Save manifest for tracking
    save_batch_manifest(batch_ids)

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("\n1. Batches are now processing asynchronously (1-6 hours)")
    print("\n2. Check status periodically:")
    print(f"   python scripts/run_disease_enrichment.py status {' '.join(batch_ids[:2])} ...")
    print("\n3. Retrieve results when processing_status == 'ended':")
    print(f"   python scripts/run_disease_enrichment.py retrieve {batch_ids[0]}")


def cmd_status(*batch_ids):
    """Check status of one or more batches."""
    if not batch_ids:
        print("Usage: python scripts/run_disease_enrichment.py status batch_id1 batch_id2 ...")
        sys.exit(1)

    enricher = DiseaseBatchEnricher()

    print("=" * 70)
    print("Batch Status")
    print("=" * 70 + "\n")

    for batch_id in batch_ids:
        batch = enricher.client.messages.batches.retrieve(batch_id)

        status_emoji = (
            "🟢" if batch.processing_status == "ended" else "🟡"
        )
        print(f"{status_emoji} Batch: {batch_id}")
        print(f"  Status:       {batch.processing_status}")
        print(f"  Processing:   {batch.request_counts.processing}")
        print(f"  Succeeded:    {batch.request_counts.succeeded}")
        print(f"  Errored:      {batch.request_counts.errored}")

        if batch.processing_status == "ended":
            print(f"  ✓ Ready to retrieve results:")
            print(f"    python scripts/run_disease_enrichment.py retrieve {batch_id}")
        print()


def cmd_retrieve(batch_id: str):
    """Retrieve results from a completed batch."""
    if not batch_id:
        print("Usage: python scripts/run_disease_enrichment.py retrieve batch_id")
        sys.exit(1)

    enricher = DiseaseBatchEnricher()

    print("=" * 70)
    print(f"Retrieving batch results: {batch_id}")
    print("=" * 70)

    batch = enricher.client.messages.batches.retrieve(batch_id)

    if batch.processing_status != "ended":
        print(f"✗ Batch not ready. Status: {batch.processing_status}")
        print(f"  Try again later.")
        sys.exit(1)

    print(f"\n✓ Batch completed!")
    print(f"  Succeeded: {batch.request_counts.succeeded}")
    print(f"  Errored:   {batch.request_counts.errored}")

    # Process results
    print(f"\nProcessing results...")
    diseases = enricher.process_batch_results(batch_id, _DISEASE_DB)

    # Save enriched database
    output_path = (
        Path(__file__).parent.parent
        / f"enriched_diseases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(diseases, f, ensure_ascii=False, indent=2)

    print(f"✓ Enriched diseases saved to: {output_path}")

    # Show summary
    print("\n" + "=" * 70)
    print("Enrichment Summary")
    print("=" * 70)

    from api.disease_content_enricher import DiseaseEnricher
    enricher_summary = DiseaseEnricher()
    status = enricher_summary.get_enrichment_status(diseases)

    print(f"\nTotal diseases:     {status['total']}")
    print(f"Complete:           {status['complete']} ({status['complete_percentage']}%)")
    print(f"Incomplete:         {status['incomplete']}")
    print("\nField Coverage:")
    for field, coverage in status["field_coverage"].items():
        bars = "█" * int(coverage / 5) + "░" * (20 - int(coverage / 5))
        print(f"  {field:20} [{bars}] {coverage}%")

    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print(f"\n1. Review enriched data in: {output_path}")
    print("\n2. Validate quality by sampling diseases")
    print("\n3. Backup current database")
    print(f"\n4. Replace api/symptom_checker.py disease data with enriched version")
    print("\n5. Run tests: pytest tests/")
    print("\n6. Deploy to production")


def cmd_help():
    """Show help message."""
    print("""
Disease Content Enrichment Tool

Usage:
    python scripts/run_disease_enrichment.py <command> [args]

Commands:
    submit              Submit new batch for enrichment
    status batch_ids    Check status of batch(es)
    retrieve batch_id   Retrieve and process batch results
    help                Show this help message

Examples:
    # Submit new batch
    python scripts/run_disease_enrichment.py submit

    # Check multiple batches
    python scripts/run_disease_enrichment.py status batch_123 batch_456

    # Get results
    python scripts/run_disease_enrichment.py retrieve batch_123
""")


def main():
    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "submit":
        cmd_submit()
    elif command == "status":
        cmd_status(*sys.argv[2:])
    elif command == "retrieve":
        if len(sys.argv) < 3:
            print("Error: batch_id required")
            cmd_help()
            sys.exit(1)
        cmd_retrieve(sys.argv[2])
    elif command in ("help", "-h", "--help"):
        cmd_help()
    else:
        print(f"Unknown command: {command}\n")
        cmd_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
