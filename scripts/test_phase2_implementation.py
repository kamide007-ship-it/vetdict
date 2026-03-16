#!/usr/bin/env python3
"""
Test Phase 2 Implementation - Validate basic functionality

Tests batch enricher, scheduler, processor, and validator modules
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from api.phase2_batch_enricher import Phase2BatchEnricher
from api.phase2_qa_validator import Phase2QAValidator
from api.phase2_recovery_manager import Phase2RecoveryManager


def test_imports():
    """Test that all modules can be imported."""
    print("\n✓ All imports successful")


def test_batch_enricher():
    """Test batch enricher module."""
    print("\n" + "="*70)
    print("TEST 1: Phase 2 Batch Enricher")
    print("="*70)

    enricher = Phase2BatchEnricher()
    print("✓ Phase2BatchEnricher instantiated")

    # Create test disease
    test_disease = {
        "id": "test_001",
        "name": "Test Disease",
        "name_ja": "テスト病",
        "species": "Cat",
        "description": "A test disease for validation",
        "pathophysiology": "Test pathophysiology"
    }

    # Test prompt generation
    try:
        treatment_prompt = enricher._build_treatment_prompt(test_disease)
        assert "treatment" in treatment_prompt.lower()
        print("✓ Treatment prompt generated")

        prevention_prompt = enricher._build_prevention_prompt(test_disease)
        assert "prevention" in prevention_prompt.lower()
        print("✓ Prevention prompt generated")

        prognosis_prompt = enricher._build_prognosis_prompt(test_disease)
        assert "prognosis" in prognosis_prompt.lower()
        print("✓ Prognosis prompt generated")
    except Exception as e:
        print(f"❌ Prompt generation failed: {e}")
        return False

    # Test batch request creation
    try:
        diseases = [test_disease]
        batches = enricher.create_phase2_batch_requests(diseases, stage="treatment")
        assert len(batches) > 0
        assert len(batches[0]) > 0
        print(f"✓ Batch requests created ({len(batches[0])} requests per batch)")
    except Exception as e:
        print(f"❌ Batch creation failed: {e}")
        return False

    print("\n✅ Batch Enricher tests passed")
    return True


def test_qa_validator():
    """Test QA validator module."""
    print("\n" + "="*70)
    print("TEST 2: Phase 2 QA Validator")
    print("="*70)

    validator = Phase2QAValidator()
    print("✓ Phase2QAValidator instantiated")

    # Create test disease with complete Phase 2 data
    test_disease = {
        "id": "test_001",
        "name": "Feline Leukemia",
        "species": "Cat",
        "treatment": "Treatment with antiviral agents and supportive care. Management of secondary infections with appropriate antibiotics and immunosuppressive therapy.",
        "treatment_ja": "抗ウイルス剤と支持療法による治療。二次感染の管理が重要で、適切な抗生物質と免疫抑制療法が必要です。",
        "prevention": "Vaccination recommended for kittens at 8-12 weeks with booster shots. Testing before introduction to new environments and isolation of positive cats.",
        "prevention_ja": "仔猫の予防接種（8-12週齢）とブースター接種が推奨されます。新しい環境への導入前の検査と陽性猫の隔離が重要です。",
        "prognosis": "Prognosis is poor for persistent infections, with survival typically 3-4 years. Some cats may achieve abortive or regressive infection with better outcomes. Regular monitoring is essential.",
        "prognosis_ja": "持続感染の予後は不良で、通常3～4年の生存期間が期待されます。一部の猫は中止性または退行性感染を達成し、より良い予後が得られます。定期的な監視が不可欠です。"
    }

    try:
        # Test field presence
        is_valid, msg = validator.validate_field_presence(test_disease, "treatment")
        assert is_valid, msg
        print("✓ Field presence validation passed")

        # Test field length
        is_valid, details = validator.validate_field_length(test_disease, "treatment")
        assert is_valid, f"Length validation failed: {details}"
        print("✓ Field length validation passed")

        # Test bilingual balance
        is_valid, details = validator.validate_bilingual_balance(test_disease, "treatment")
        assert is_valid, f"Bilingual validation failed: {details}"
        print("✓ Bilingual balance validation passed")

        # Test keyword presence
        is_valid, details = validator.validate_keyword_presence(test_disease, "treatment")
        assert is_valid, f"Keyword validation failed: {details}"
        print(f"✓ Keyword validation passed ({details['keyword_count']} keywords found)")

        # Test sentence structure
        is_valid, details = validator.validate_sentence_structure(test_disease, "treatment")
        assert is_valid, f"Sentence validation failed: {details}"
        print(f"✓ Sentence structure validation passed ({details['sentence_count']} sentences)")

    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False

    print("\n✅ QA Validator tests passed")
    return True


def test_recovery_manager():
    """Test recovery manager module."""
    print("\n" + "="*70)
    print("TEST 3: Phase 2 Recovery Manager")
    print("="*70)

    manager = Phase2RecoveryManager()
    print("✓ Phase2RecoveryManager instantiated")

    try:
        # Test recovery report generation
        report = manager.get_recovery_report()
        assert "timestamp" in report
        assert "phase" in report
        print("✓ Recovery report generated")

        # Print report summary
        print(f"\n  Phase: {report['phase']}")
        print(f"  Batches submitted: {report['batches_submitted']}")
        print(f"  Batches completed: {report['batches_completed']}")
        print(f"  Failed batches: {report['failed_batches']}")
        print(f"  Checkpoints: {report['checkpoints']}")

    except Exception as e:
        print(f"❌ Recovery manager test failed: {e}")
        return False

    print("\n✅ Recovery Manager tests passed")
    return True


def test_data_loading():
    """Test disease database loading."""
    print("\n" + "="*70)
    print("TEST 4: Disease Database Loading")
    print("="*70)

    database_path = project_root / "diseases_all_species.json"

    if not database_path.exists():
        print(f"❌ Database not found at {database_path}")
        return False

    try:
        with open(database_path, "r") as f:
            diseases = json.load(f)

        print(f"✓ Loaded {len(diseases)} diseases from database")

        # Check Phase 2 enrichment status
        treatment_count = sum(1 for d in diseases if d.get("treatment"))
        prevention_count = sum(1 for d in diseases if d.get("prevention"))
        prognosis_count = sum(1 for d in diseases if d.get("prognosis"))

        print("\nCurrent Phase 2 Enrichment Status:")
        print(f"  Treatment: {treatment_count}/{len(diseases)} ({100*treatment_count/len(diseases):.1f}%)")
        print(f"  Prevention: {prevention_count}/{len(diseases)} ({100*prevention_count/len(diseases):.1f}%)")
        print(f"  Prognosis: {prognosis_count}/{len(diseases)} ({100*prognosis_count/len(diseases):.1f}%)")

        # Sample a few diseases
        print("\nSample disease:")
        sample = diseases[0]
        print(f"  ID: {sample.get('id')}")
        print(f"  Name: {sample.get('name')}")
        print(f"  Species: {sample.get('species')}")
        print(f"  Phase 1 complete: {bool(sample.get('pathophysiology') and sample.get('causes'))}")
        print(f"  Phase 2 fields: treatment={bool(sample.get('treatment'))}, "
              f"prevention={bool(sample.get('prevention'))}, "
              f"prognosis={bool(sample.get('prognosis'))}")

    except Exception as e:
        print(f"❌ Database loading failed: {e}")
        return False

    print("\n✅ Database loading test passed")
    return True


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("PHASE 2 IMPLEMENTATION TEST SUITE")
    print("="*70)

    results = []

    try:
        test_imports()
        results.append(("Imports", True))
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        results.append(("Imports", False))

    results.append(("Batch Enricher", test_batch_enricher()))
    results.append(("QA Validator", test_qa_validator()))
    results.append(("Recovery Manager", test_recovery_manager()))
    results.append(("Database Loading", test_data_loading()))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:20} {status}")

    all_passed = all(passed for _, passed in results)

    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
