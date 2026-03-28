"""Tests for api/drug_batch_4.py — Fish-specific medications."""


from api.drug_batch_4 import FISH_DRUGS, FISH_SPECIES_INFO_PATCH

REQUIRED_DRUG_FIELDS = {"id", "name", "name_ja", "category", "category_ja",
                        "description", "description_ja", "species_info"}
REQUIRED_SPECIES_INFO_FIELDS = {"safe", "dosage", "dosage_ja", "notes", "notes_ja"}


class TestFishDrugs:
    def test_fish_drugs_is_nonempty_list(self):
        assert isinstance(FISH_DRUGS, list)
        assert len(FISH_DRUGS) >= 10

    def test_every_drug_has_required_fields(self):
        for drug in FISH_DRUGS:
            missing = REQUIRED_DRUG_FIELDS - set(drug.keys())
            assert not missing, f"{drug.get('id', '?')} missing {missing}"

    def test_every_drug_has_fish_species_info(self):
        for drug in FISH_DRUGS:
            assert "fish" in drug["species_info"], f"{drug['id']} has no fish species_info"
            info = drug["species_info"]["fish"]
            missing = REQUIRED_SPECIES_INFO_FIELDS - set(info.keys())
            assert not missing, f"{drug['id']} fish info missing {missing}"

    def test_all_drug_ids_unique(self):
        ids = [d["id"] for d in FISH_DRUGS]
        assert len(ids) == len(set(ids))

    def test_all_drugs_have_fish_safe_true(self):
        for drug in FISH_DRUGS:
            assert drug["species_info"]["fish"]["safe"] is True, (
                f"{drug['id']} should be safe for fish"
            )

    def test_known_drugs_present(self):
        ids = {d["id"] for d in FISH_DRUGS}
        expected = {"methylene_blue", "malachite_green", "formalin_fish",
                    "copper_sulfate", "potassium_permanganate", "oxylinic_acid"}
        assert expected.issubset(ids)


class TestFishSpeciesInfoPatch:
    def test_patch_is_nonempty_dict(self):
        assert isinstance(FISH_SPECIES_INFO_PATCH, dict)
        assert len(FISH_SPECIES_INFO_PATCH) >= 1

    def test_patch_entries_have_fish_key(self):
        for drug_id, info in FISH_SPECIES_INFO_PATCH.items():
            assert "fish" in info, f"Patch for {drug_id} missing 'fish' key"

    def test_patch_fish_info_has_required_fields(self):
        for drug_id, info in FISH_SPECIES_INFO_PATCH.items():
            fish = info["fish"]
            for field in ("safe", "dosage", "dosage_ja"):
                assert field in fish, f"Patch {drug_id} missing '{field}'"
