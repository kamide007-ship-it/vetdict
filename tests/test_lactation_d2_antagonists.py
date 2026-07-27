"""Sulpiride and the D2-antagonist galactagogue effect must be present and honest.

A vet reported two gaps: sulpiride (Dogmatil) was missing entirely, and
metoclopramide (Primperan) was described only as a prokinetic/antiemetic with no
mention of its prolactin-raising effect, which is why it is used for insufficient
milk production in the bitch.

The risk in fixing this is transplanting human medicine. Sulpiride in people is
dosed 150-1,200 mg/day for gastric ulcer, depression and schizophrenia; those are
not animal doses, and copying them in is the same failure that once put diabetic
foot ulcer and retinopathy into the degu database. So these tests assert the
veterinary dosing is present where evidence exists (horse) and that species
without evidence say so instead of carrying an extrapolated number.
"""

from __future__ import annotations

import re

from api.drug_dictionary import DRUGS, get_drug_by_id

# Human psychiatric/GI daily doses that must never appear as an animal dose.
HUMAN_DOSE = re.compile(r"\b(150|300|600|1200|1,200)\s*mg\s*/?\s*(day|日)", re.I)


def test_sulpiride_is_present():
    drug = get_drug_by_id("sulpiride")
    assert drug is not None, "sulpiride is missing from the dictionary"
    assert "スルピリド" in drug["name_ja"]


def test_sulpiride_covers_all_21_species():
    drug = get_drug_by_id("sulpiride")
    assert len(drug["species_info"]) == 21, "every species should get an evidence-based answer"


def test_sulpiride_horse_dosing_is_sourced():
    horse = get_drug_by_id("sulpiride")["species_info"]["horse"]
    assert horse["safe"] is True
    assert "mg/kg" in horse["dosage"]
    # The equine dose must be traceable, not asserted.
    assert "Theriogenology" in horse["notes"]
    assert horse.get("evidence_grade") == "A"


def test_species_without_evidence_are_not_marked_usable():
    """ "Not established" must not render as ✓ — that reads as "safe to use"."""
    info = get_drug_by_id("sulpiride")["species_info"]
    for species, entry in info.items():
        if species == "horse":
            continue
        assert entry.get("safe") is not True, f"{species} claims sulpiride is established when it is not"
        assert "確立されていない" in (entry.get("notes_ja") or "") + (entry.get("dose") or "") + (
            entry.get("dosage_ja") or ""
        )


def test_no_human_dosing_transplanted_into_sulpiride():
    drug = get_drug_by_id("sulpiride")
    blob = " ".join(
        str(v.get(k, "") or "")
        for v in drug["species_info"].values()
        for k in ("dosage", "dosage_ja", "dose", "notes", "notes_ja")
    )
    assert not HUMAN_DOSE.search(blob), "human daily dosing leaked into the veterinary entry"


def test_metoclopramide_documents_the_galactagogue_effect():
    drug = get_drug_by_id("metoclopramide")
    assert "プロラクチン" in drug["mechanism_ja"], "prolactin effect still missing from the mechanism"
    assert "prolactin" in drug["mechanism"].lower()


def test_metoclopramide_dog_lactation_use_is_sourced_and_caveated():
    dog = get_drug_by_id("metoclopramide")["species_info"]["dog"]
    notes = (dog.get("notes_ja") or "") + (dog.get("notes") or "")
    assert "29359978" in notes, "canine galactagogue dosing is not traceable to its source"
    assert "0.2 mg/kg" in notes
    # The study did not improve puppy weight gain; overstating it would mislead.
    assert "体重増加" in notes or "weight gain" in notes


def test_prokinetic_dosing_was_not_overwritten_by_the_lactation_note():
    """Adding the galactagogue use must not disturb the existing GI dose."""
    dog = get_drug_by_id("metoclopramide")["species_info"]["dog"]
    assert "mg/kg" in (dog.get("dosage_ja") or dog.get("dosage") or "")


def test_sulpiride_conflicts_with_prolactin_suppressors():
    interactions = {i["drug"].lower() for i in get_drug_by_id("sulpiride").get("drug_interactions", [])}
    assert "cabergoline" in interactions, "opposing D2 agonist should be flagged"


def test_dictionary_still_has_no_duplicate_names():
    seen = set()
    for drug in DRUGS:
        key = str(drug.get("name", "")).strip().lower()
        assert key not in seen, f"adding batch 30 reintroduced a duplicate: {key}"
        seen.add(key)
