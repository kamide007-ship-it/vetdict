#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 Integration

Integrates Phase 1 enriched data into the main disease database.
Creates backup and validates integration before commit.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path


class Phase1Integration:
    """Integrates Phase 1 enriched data into main database."""

    def __init__(self):
        self.db_path = Path(__file__).parent.parent / "diseases_all_species.json"
        self.backup_path = (
            Path(__file__).parent.parent
            / f"diseases_all_species_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        # Find the most recent enriched database
        enriched_files = list(Path(__file__).parent.parent.glob("diseases_enriched_phase1_*.json"))
        if not enriched_files:
            raise FileNotFoundError("No enriched database found. Run phase1_batch_processor.py first.")
        self.enriched_db_path = max(enriched_files)

    def backup_original(self):
        """Create backup of original database."""
        print(f"Creating backup: {self.backup_path}")
        shutil.copy(self.db_path, self.backup_path)
        print("✓ Backup created")

    def load_databases(self):
        """Load both original and enriched databases."""
        with open(self.db_path, "r", encoding="utf-8") as f:
            original = json.load(f)
        with open(self.enriched_db_path, "r", encoding="utf-8") as f:
            enriched = json.load(f)
        return original, enriched

    def merge_databases(self, original, enriched):
        """Merge enriched data into original database."""
        # Create a mapping for quick lookup
        enriched_map = {d["id"]: d for d in enriched}

        merged_count = 0
        for disease in original:
            disease_id = disease["id"]
            if disease_id in enriched_map:
                enriched_disease = enriched_map[disease_id]

                # Update all enrichment fields
                for field in [
                    "pathophysiology",
                    "pathophysiology_ja",
                    "causes",
                    "causes_ja",
                    "treatment",
                    "treatment_ja",
                    "prevention",
                    "prevention_ja",
                    "prognosis",
                    "prognosis_ja",
                ]:
                    if field in enriched_disease and enriched_disease[field]:
                        disease[field] = enriched_disease[field]

                # Add enrichment metadata
                disease["enriched_at"] = enriched_disease.get("enriched_at", datetime.now().isoformat())
                disease["enrichment_phase"] = 1

                merged_count += 1

        return original, merged_count

    def validate_merge(self, original, enriched, merged_count):
        """Validate merge integrity."""
        print("\nValidation Checks:")
        print(f"  Original database: {len(original)} diseases")
        print(f"  Enriched database: {len(enriched)} diseases")
        print(f"  Merged count: {merged_count}")
        print(
            f"  Size unchanged: {len(original) == len(enriched)} ✓"
            if len(original) == len(enriched)
            else "  Size mismatch: ✗"
        )

        # Check field coverage
        phase1_diseases = [d for d in original if d.get("enrichment_phase") == 1]
        avg_fields = sum(
            sum(
                1
                for f in [
                    "pathophysiology",
                    "pathophysiology_ja",
                    "causes",
                    "causes_ja",
                    "treatment",
                    "treatment_ja",
                    "prevention",
                    "prevention_ja",
                    "prognosis",
                    "prognosis_ja",
                ]
                if d.get(f)
            )
            for d in phase1_diseases
        ) / max(len(phase1_diseases), 1)

        print(f"  Phase 1 diseases: {len(phase1_diseases)}")
        print(f"  Avg fields populated: {avg_fields:.1f}/10")

        return len(original) == len(enriched)

    def save_merged_database(self, original):
        """Save merged database as main database."""
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(original, f, ensure_ascii=False, indent=2)
        print(f"✓ Merged database saved: {self.db_path}")

    def run_integration(self):
        """Execute integration."""
        print("=" * 70)
        print("PHASE 1 INTEGRATION")
        print("=" * 70)
        print(f"Start time: {datetime.now().isoformat()}\n")

        # Step 1: Backup
        print("[1/4] Creating backup...")
        self.backup_original()

        # Step 2: Load databases
        print("\n[2/4] Loading databases...")
        original, enriched = self.load_databases()
        print(f"✓ Original: {len(original)} diseases")
        print(f"✓ Enriched: {len(enriched)} diseases")

        # Step 3: Merge
        print("\n[3/4] Merging databases...")
        merged, merged_count = self.merge_databases(original, enriched)
        print(f"✓ Merged {merged_count} diseases")

        # Step 4: Validate and save
        print("\n[4/4] Validating and saving...")
        valid = self.validate_merge(original, enriched, merged_count)

        if not valid:
            print("\n❌ Validation failed! Restoring from backup...")
            shutil.copy(self.backup_path, self.db_path)
            print("✓ Restored original database")
            return False

        self.save_merged_database(merged)

        # Summary
        print("\n" + "=" * 70)
        print("✅ INTEGRATION COMPLETE")
        print("=" * 70)
        print("\nIntegration Summary:")
        print(f"  Diseases merged: {merged_count}")
        print(f"  Backup created: {self.backup_path}")
        print(f"  Database updated: {self.db_path}")
        print("\nNext steps:")
        print("  1. Review changes: git diff diseases_all_species.json")
        print("  2. Commit changes: git add diseases_all_species.json && git commit -m '...'")
        print("  3. Push to branch: git push -u origin <branch>")

        return True


if __name__ == "__main__":
    integration = Phase1Integration()
    success = integration.run_integration()
    exit(0 if success else 1)
