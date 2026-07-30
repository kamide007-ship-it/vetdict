#!/usr/bin/env python3
"""Regression test for commonly-encountered conditions that were missing.

These everyday dog/cat presentations (travel sickness, coprophagia, electrical
cord injury, frostbite, foxtail/grass-awn migration, smoke inhalation) had no
database entry despite being routine reasons an owner or vet looks something up.

The test also guards a species-specific SAFETY fact: the motion-sickness
maropitant (Cerenia) dose is 8 mg/kg in the dog but only 1 mg/kg in the cat —
these must not be conflated.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from api.species.cat_diseases import DISEASES as CAT_DISEASES
from api.species.dog_diseases import DISEASES as DOG_DISEASES
from api.species.dog_diseases import VALID_SYMPTOMS as DOG_SYMPTOMS

_DOG_NEW = {
    "Motion Sickness (Travel Sickness)": "normal",
    "Coprophagia": "normal",
    "Electrical Cord Injury (Electrocution)": "emergency",
    "Frostbite": "high",
    "Foxtail / Grass Awn Migration": "normal",
    "Smoke Inhalation": "emergency",
}
_CAT_NEW = {
    "Feline Motion Sickness (Travel Sickness)": "normal",
    "Feline Electrical Cord Injury (Electrocution)": "emergency",
}


def _by_name(diseases):
    return {d["name"]: d for d in diseases}


def test_new_dog_conditions_present_with_expected_urgency():
    dogs = _by_name(DOG_DISEASES)
    for name, urgency in _DOG_NEW.items():
        assert name in dogs, f"missing dog condition: {name}"
        d = dogs[name]
        assert d["urgency"] == urgency, f"{name}: urgency {d['urgency']} != {urgency}"
        assert not (set(d["symptoms"]) - set(DOG_SYMPTOMS)), f"{name}: unknown symptom id"
        for field in ("description_ja", "pathophysiology_ja", "treatment_ja", "prognosis_ja"):
            assert (d.get(field) or "").strip(), f"{name}: {field} empty"


def test_new_cat_conditions_present_with_expected_urgency():
    cats = _by_name(CAT_DISEASES)
    for name, urgency in _CAT_NEW.items():
        assert name in cats, f"missing cat condition: {name}"
        d = cats[name]
        assert d["urgency"] == urgency, f"{name}: urgency {d['urgency']} != {urgency}"
        for field in ("description_ja", "pathophysiology_ja", "treatment_ja", "prognosis_ja"):
            assert (d.get(field) or "").strip(), f"{name}: {field} empty"


def test_maropitant_dose_differs_between_dog_and_cat():
    """Cerenia is 8 mg/kg for canine motion sickness but 1 mg/kg in the cat."""
    dog = _by_name(DOG_DISEASES)["Motion Sickness (Travel Sickness)"]
    cat = _by_name(CAT_DISEASES)["Feline Motion Sickness (Travel Sickness)"]
    assert "8 mg/kg" in dog["treatment_ja"] and "マロピタント" in dog["treatment_ja"]
    assert "1 mg/kg" in cat["treatment_ja"] and "マロピタント" in cat["treatment_ja"]
    assert "8 mg/kg" not in cat["treatment_ja"], "cat must not carry the canine 8 mg/kg maropitant dose"


def test_electrocution_warns_of_delayed_pulmonary_edema():
    for diseases, name in (
        (DOG_DISEASES, "Electrical Cord Injury (Electrocution)"),
        (CAT_DISEASES, "Feline Electrical Cord Injury (Electrocution)"),
    ):
        d = _by_name(diseases)[name]
        assert "肺水腫" in d["treatment_ja"], f"{name}: must flag (delayed) pulmonary edema"
        assert "神経原性" in d["pathophysiology_ja"], f"{name}: must name neurogenic mechanism"
