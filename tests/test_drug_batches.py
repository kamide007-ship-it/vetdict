import importlib


def test_drug_batch_modules_are_importable():
    batch_1 = importlib.import_module("api.drug_batch_1")
    batch_2 = importlib.import_module("api.drug_batch_2")

    assert isinstance(batch_1.DRUGS_BATCH_1, list)
    assert isinstance(batch_2.DRUGS_BATCH_2, list)
    assert batch_1.DRUGS_BATCH_1
    assert batch_2.DRUGS_BATCH_2


def test_drug_batch_3_importable():
    batch_3 = importlib.import_module("api.drug_batch_3")
    assert isinstance(batch_3.SPECIES_INFO_PATCH, dict)
    assert batch_3.SPECIES_INFO_PATCH


def test_drug_batch_4_importable():
    batch_4 = importlib.import_module("api.drug_batch_4")
    assert isinstance(batch_4.FISH_DRUGS, list)
    assert isinstance(batch_4.FISH_SPECIES_INFO_PATCH, dict)
    assert batch_4.FISH_DRUGS
