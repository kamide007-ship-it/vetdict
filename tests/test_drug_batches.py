"""Structural and integrity tests for all drug batch modules.

Validates that drug data across batches 1-6 has consistent structure,
required fields, unique IDs, and bilingual content.
"""

from api.drug_batch_1 import DRUGS_BATCH_1
from api.drug_batch_2 import DRUGS_BATCH_2
from api.drug_batch_3 import SPECIES_INFO_PATCH
from api.drug_batch_4 import FISH_DRUGS
from api.drug_batch_5 import DRUGS_BATCH_5, SPECIES_INFO_PATCH_5
from api.drug_batch_6 import (
    DRUG_INTERACTIONS_PATCH_6,
    DRUGS_BATCH_6,
    SPECIES_INFO_PATCH_6,
)

# Fields every drug entry must have (batches 1, 2, 5, 6 — full drugs)
_REQUIRED_DRUG_FIELDS = {
    "id",
    "name",
    "name_ja",
    "category",
    "mechanism",
    "mechanism_ja",
    "species_info",
    "side_effects",
    "side_effects_ja",
    "contraindications",
    "contraindications_ja",
}

# Fields every species_info entry must have
_REQUIRED_SPECIES_INFO_FIELDS = {"safe", "dosage", "dosage_ja", "notes", "notes_ja"}


# ---------------------------------------------------------------------------
# Batch 1
# ---------------------------------------------------------------------------


class TestDrugBatch1:
    def test_nonempty(self):
        assert len(DRUGS_BATCH_1) >= 1

    def test_required_fields(self):
        for drug in DRUGS_BATCH_1:
            missing = _REQUIRED_DRUG_FIELDS - set(drug.keys())
            assert not missing, f"{drug.get('id', '?')}: missing {missing}"

    def test_unique_ids(self):
        ids = [d["id"] for d in DRUGS_BATCH_1]
        assert len(ids) == len(set(ids)), f"Duplicate IDs: {[x for x in ids if ids.count(x) > 1]}"

    def test_species_info_structure(self):
        for drug in DRUGS_BATCH_1:
            for species, info in drug["species_info"].items():
                missing = _REQUIRED_SPECIES_INFO_FIELDS - set(info.keys())
                assert not missing, f"{drug['id']}/{species}: missing {missing}"

    def test_ids_are_lowercase(self):
        for drug in DRUGS_BATCH_1:
            assert drug["id"] == drug["id"].lower(), f"ID not lowercase: {drug['id']}"


# ---------------------------------------------------------------------------
# Batch 2
# ---------------------------------------------------------------------------


class TestDrugBatch2:
    def test_nonempty(self):
        assert len(DRUGS_BATCH_2) >= 5

    def test_required_fields(self):
        for drug in DRUGS_BATCH_2:
            missing = _REQUIRED_DRUG_FIELDS - set(drug.keys())
            assert not missing, f"{drug.get('id', '?')}: missing {missing}"

    def test_unique_ids(self):
        ids = [d["id"] for d in DRUGS_BATCH_2]
        assert len(ids) == len(set(ids))

    def test_new_drugs_present(self):
        """Verify 2026 session drugs are included."""
        ids = {d["id"] for d in DRUGS_BATCH_2}
        expected = {"lokivetmab", "bedinvetmab", "frunevetmab", "gs441524", "molnupiravir"}
        assert expected.issubset(ids), f"Missing: {expected - ids}"

    def test_species_info_structure(self):
        for drug in DRUGS_BATCH_2:
            for species, info in drug["species_info"].items():
                missing = _REQUIRED_SPECIES_INFO_FIELDS - set(info.keys())
                assert not missing, f"{drug['id']}/{species}: missing {missing}"


# ---------------------------------------------------------------------------
# Batch 3 (species info patch)
# ---------------------------------------------------------------------------


class TestDrugBatch3:
    def test_nonempty(self):
        assert len(SPECIES_INFO_PATCH) >= 5

    def test_patch_values_are_dicts(self):
        for drug_id, species_map in SPECIES_INFO_PATCH.items():
            assert isinstance(species_map, dict), f"{drug_id}: expected dict"
            for species, info in species_map.items():
                assert isinstance(info, dict), f"{drug_id}/{species}: expected dict"

    def test_patch_species_info_fields(self):
        for drug_id, species_map in SPECIES_INFO_PATCH.items():
            for species, info in species_map.items():
                missing = _REQUIRED_SPECIES_INFO_FIELDS - set(info.keys())
                assert not missing, f"{drug_id}/{species}: missing {missing}"


# ---------------------------------------------------------------------------
# Batch 5
# ---------------------------------------------------------------------------


class TestDrugBatch5:
    def test_nonempty(self):
        assert len(DRUGS_BATCH_5) >= 1

    def test_required_fields(self):
        for drug in DRUGS_BATCH_5:
            missing = _REQUIRED_DRUG_FIELDS - set(drug.keys())
            assert not missing, f"{drug.get('id', '?')}: missing {missing}"

    def test_unique_ids(self):
        ids = [d["id"] for d in DRUGS_BATCH_5]
        assert len(ids) == len(set(ids))

    def test_species_info_structure(self):
        for drug in DRUGS_BATCH_5:
            for species, info in drug["species_info"].items():
                missing = _REQUIRED_SPECIES_INFO_FIELDS - set(info.keys())
                assert not missing, f"{drug['id']}/{species}: missing {missing}"

    def test_patch_5_nonempty(self):
        assert len(SPECIES_INFO_PATCH_5) >= 1

    def test_patch_5_structure(self):
        for drug_id, species_map in SPECIES_INFO_PATCH_5.items():
            for species, info in species_map.items():
                missing = _REQUIRED_SPECIES_INFO_FIELDS - set(info.keys())
                assert not missing, f"{drug_id}/{species}: missing {missing}"


# ---------------------------------------------------------------------------
# Batch 6
# ---------------------------------------------------------------------------


class TestDrugBatch6:
    def test_nonempty(self):
        assert len(DRUGS_BATCH_6) >= 1

    def test_required_fields(self):
        for drug in DRUGS_BATCH_6:
            missing = _REQUIRED_DRUG_FIELDS - set(drug.keys())
            assert not missing, f"{drug.get('id', '?')}: missing {missing}"

    def test_unique_ids(self):
        ids = [d["id"] for d in DRUGS_BATCH_6]
        assert len(ids) == len(set(ids))

    def test_species_info_structure(self):
        for drug in DRUGS_BATCH_6:
            for species, info in drug["species_info"].items():
                missing = _REQUIRED_SPECIES_INFO_FIELDS - set(info.keys())
                assert not missing, f"{drug['id']}/{species}: missing {missing}"

    def test_patch_6_nonempty(self):
        assert len(SPECIES_INFO_PATCH_6) >= 1

    def test_patch_6_structure(self):
        for drug_id, species_map in SPECIES_INFO_PATCH_6.items():
            for species, info in species_map.items():
                missing = _REQUIRED_SPECIES_INFO_FIELDS - set(info.keys())
                assert not missing, f"{drug_id}/{species}: missing {missing}"

    def test_drug_interactions_patch(self):
        assert isinstance(DRUG_INTERACTIONS_PATCH_6, dict)
        for drug_id, interactions in DRUG_INTERACTIONS_PATCH_6.items():
            assert isinstance(interactions, list), f"{drug_id}: expected list"
            for interaction in interactions:
                assert "drug" in interaction, f"{drug_id}: interaction missing 'drug'"


# ---------------------------------------------------------------------------
# Cross-batch validations
# ---------------------------------------------------------------------------


class TestCrossBatchIntegrity:
    """Validate consistency across all drug batches."""

    def test_no_duplicate_ids_across_batches(self):
        all_ids = (
            [d["id"] for d in DRUGS_BATCH_1]
            + [d["id"] for d in DRUGS_BATCH_2]
            + [d["id"] for d in FISH_DRUGS]
            + [d["id"] for d in DRUGS_BATCH_5]
            + [d["id"] for d in DRUGS_BATCH_6]
        )
        seen = set()
        duplicates = set()
        for drug_id in all_ids:
            if drug_id in seen:
                duplicates.add(drug_id)
            seen.add(drug_id)
        assert not duplicates, f"Duplicate drug IDs across batches: {duplicates}"

    def test_all_batches_have_japanese_names(self):
        """Every drug across all batches must have a Japanese name."""
        all_drugs = DRUGS_BATCH_1 + DRUGS_BATCH_2 + FISH_DRUGS + DRUGS_BATCH_5 + DRUGS_BATCH_6
        for drug in all_drugs:
            assert drug.get("name_ja"), f"{drug['id']}: missing name_ja"

    def test_total_drug_count(self):
        """Sanity check: combined drug count is reasonable."""
        total = len(DRUGS_BATCH_1) + len(DRUGS_BATCH_2) + len(FISH_DRUGS) + len(DRUGS_BATCH_5) + len(DRUGS_BATCH_6)
        # Should have a substantial number of drugs
        assert total >= 30, f"Only {total} drugs across all batches"
