import importlib


def test_drug_batch_modules_are_importable():
    batch_1 = importlib.import_module("api.drug_batch_1")
    batch_2 = importlib.import_module("api.drug_batch_2")

    assert isinstance(batch_1.DRUGS_BATCH_1, list)
    assert isinstance(batch_2.DRUGS_BATCH_2, list)
    assert batch_1.DRUGS_BATCH_1
    assert batch_2.DRUGS_BATCH_2
