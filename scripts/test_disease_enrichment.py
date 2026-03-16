#!/usr/bin/env python3
"""
Test script for disease content enrichment.

Enrich a small sample of diseases to verify quality before running full batch.
Run this to test the enrichment pipeline locally.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from api.disease_content_enricher import DiseaseEnricher


def test_enrichment():
    """Test enrichment on a sample disease."""
    print("=" * 70)
    print("VetDict Disease Content Enrichment Test")
    print("=" * 70)

    # Initialize enricher
    try:
        enricher = DiseaseEnricher()
        print("✓ DiseaseEnricher initialized")
    except Exception as e:
        print(f"✗ Failed to initialize enricher: {e}")
        print("  Make sure ANTHROPIC_API_KEY is set")
        return False

    # Load disease database
    try:
        from api.symptom_checker import _DISEASE_DB
        print(f"✓ Loaded {len(_DISEASE_DB)} diseases")
    except Exception as e:
        print(f"✗ Failed to load disease database: {e}")
        return False

    # Get enrichment status
    print("\n" + "=" * 70)
    print("Current Status")
    print("=" * 70)
    status = enricher.get_enrichment_status(_DISEASE_DB)
    print(f"Total diseases:     {status['total']}")
    print(f"Complete:           {status['complete']} ({status['complete_percentage']}%)")
    print(f"Incomplete:         {status['incomplete']}")
    print("\nField Coverage:")
    for field, coverage in status["field_coverage"].items():
        bars = "█" * int(coverage / 5) + "░" * (20 - int(coverage / 5))
        print(f"  {field:20} [{bars}] {coverage}%")

    # Find an incomplete disease for testing
    print("\n" + "=" * 70)
    print("Test Enrichment")
    print("=" * 70)

    incomplete_disease = None
    for disease in _DISEASE_DB:
        if not disease.get("pathophysiology") and not disease.get("causes"):
            incomplete_disease = disease
            break

    if not incomplete_disease:
        print("✓ All diseases are already complete! No testing needed.")
        return True

    disease_name = incomplete_disease.get("name", "Unknown")
    disease_name_ja = incomplete_disease.get("name_ja", disease_name)

    print(f"\nTest Disease: {disease_name} ({disease_name_ja})")
    print(f"Description: {incomplete_disease.get('description', 'N/A')[:100]}...")
    print("\nEnriching... (may take 10-30 seconds)")

    try:
        enriched = enricher.enrich_single_disease(incomplete_disease.copy())

        print("\n" + "-" * 70)
        print("RESULTS")
        print("-" * 70)

        # Display enriched content
        fields = {
            "Pathophysiology": ("pathophysiology", "pathophysiology_ja"),
            "Causes": ("causes", "causes_ja"),
            "Treatment": ("treatment", "treatment_ja"),
            "Prevention": ("prevention", "prevention_ja"),
            "Prognosis": ("prognosis", "prognosis_ja"),
        }

        all_successful = True
        for label, (en_field, ja_field) in fields.items():
            en_content = enriched.get(en_field, "")
            ja_content = enriched.get(ja_field, "")

            if en_content or ja_content:
                print(f"\n✓ {label}:")
                if en_content:
                    print(f"  EN: {en_content[:150]}...")
                if ja_content:
                    print(f"  JA: {ja_content[:150]}...")
            else:
                print(f"\n✗ {label}: No content generated")
                all_successful = False

        print("\n" + "-" * 70)

        if all_successful:
            print("✓ Enrichment successful! Ready for batch processing.")
            return True
        else:
            print("⚠ Some fields were not generated. Check API response.")
            return False

    except Exception as e:
        print(f"✗ Enrichment failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_batch_recommendations():
    """Show recommendations for batch enrichment."""
    print("\n" + "=" * 70)
    print("Batch Enrichment Recommendations")
    print("=" * 70)

    from api.disease_batch_enricher import DiseaseBatchEnricher
    from api.symptom_checker import _DISEASE_DB

    enricher = DiseaseBatchEnricher()
    batches = enricher.create_batch_requests(_DISEASE_DB)

    total_requests = sum(len(b) for b in batches)

    print(f"\nTo enrich all {len(_DISEASE_DB)} diseases:")
    print(f"  Number of batches: {len(batches)}")
    print(f"  Total API calls:   {total_requests}")
    print(f"  Estimated cost:    ~${total_requests * 0.025:.2f} (50% batch discount)")
    print("  Processing time:   1-6 hours (batches run asynchronously)")
    print(f"  vs Standard API:   ~${total_requests * 0.05:.2f} in seconds")
    print(f"\nSavings: ~${total_requests * 0.025:.2f} (50% discount!)")

    print("\nTo start batch processing, run:")
    print("  python scripts/run_disease_enrichment.py")


if __name__ == "__main__":
    success = test_enrichment()

    if success:
        show_batch_recommendations()
        print("\n✓ Test passed! You're ready for batch enrichment.")
        sys.exit(0)
    else:
        print("\n✗ Test failed. Please check the errors above.")
        sys.exit(1)
