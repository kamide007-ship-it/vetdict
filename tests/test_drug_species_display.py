"""Species dosing must display, and duplicate drug entries must be consolidated.

Two defects found in the live drug dictionary, both reported from the UI:

1. **Every species rendered as ✗ with an empty dose.** The frontend reads
   ``species_info[sp].dosage`` and draws ``info.safe ? "✓" : "✗"``, but later
   batches wrote the dose under ``dose`` and omitted ``safe``. 336 of 610 drugs
   (55%) were affected — Gabapentin showed ✗ for dog, cat and horse despite
   carrying a documented dose for each. To a vet that reads as "not usable in
   this species", which is the opposite of the truth and clinically dangerous.

2. **The same drug split across several entries.** Gabapentin existed three
   times (``gabapentin`` / ``gabapentin_pain`` / ``gabapentin_oral``), so species
   coverage and disease links were scattered — the "Chronic Pain" copy listed no
   diseases at all.

Both are pinned as invariants rather than counts, so they cannot silently return.
"""

from __future__ import annotations

import pytest

from api.drug_dictionary import DRUGS, resolve_drug_id


def _species_entries():
    for drug in DRUGS:
        for species, info in (drug.get("species_info") or {}).items():
            if isinstance(info, dict):
                yield drug, species, info


def test_every_species_entry_with_a_dose_displays_it():
    """No species entry may hold a dose only under the non-rendered ``dose`` key."""
    hidden = [
        (d.get("id"), sp)
        for d, sp, info in _species_entries()
        if (info.get("dose") or info.get("dose_ja")) and not (info.get("dosage") or info.get("dosage_ja"))
    ]
    assert not hidden, f"dose present but not rendered for {len(hidden)} entries, e.g. {hidden[:5]}"


def test_species_with_a_dose_is_not_marked_unsafe_by_omission():
    """A documented dose must not render ✗ merely because ``safe`` was absent.

    The one legitimate exception is an entry whose notes flag a contraindication:
    those are deliberately left without ``safe`` so they keep rendering ✗ with the
    warning shown. Defaulting them to safe would invert the warning — the first
    attempt at this normalisation did exactly that to "hydrogen peroxide is
    CONTRAINDICATED in cats", which ``test_drug_safety`` caught.
    """
    from api.drug_dictionary import _notes_flag_contraindication

    missing = [
        (d.get("id"), sp)
        for d, sp, info in _species_entries()
        if (info.get("dosage") or info.get("dosage_ja"))
        and info.get("safe") is None
        and not _notes_flag_contraindication(info)
    ]
    assert not missing, f"{len(missing)} species entries would render ✗ despite a dose, e.g. {missing[:5]}"


def test_contraindicated_species_never_defaults_to_safe():
    """The dangerous inversion is pinned: a flagged contraindication is never ✓."""
    from api.drug_dictionary import DRUGS as _D

    idx = {d["id"]: d for d in _D if d.get("id")}
    cat = (idx.get("hydrogen_peroxide_emetic", {}).get("species_info") or {}).get("cat")
    if cat is not None:
        assert cat.get("safe") is not True, "hydrogen peroxide must not render ✓ for cats"


def test_explicit_contraindications_are_preserved():
    """Normalisation must not flip a deliberate ``safe=False`` to safe."""
    unsafe = [(d.get("id"), sp) for d, sp, info in _species_entries() if info.get("safe") is False]
    assert len(unsafe) >= 100, "explicit species contraindications disappeared"


def test_gabapentin_is_a_single_entry_covering_the_main_species():
    gaba = [d for d in DRUGS if str(d.get("name", "")).lower().startswith("gabapentin")]
    assert len(gaba) == 1, f"gabapentin should be one entry, got {[d.get('name') for d in gaba]}"
    info = gaba[0].get("species_info") or {}
    for species in ("dog", "cat", "horse", "rabbit"):
        entry = info.get(species)
        assert entry, f"gabapentin lost its {species} dosing in the merge"
        assert entry.get("safe") is True, f"gabapentin renders ✗ for {species}"
        assert entry.get("dosage") or entry.get("dosage_ja"), f"gabapentin has no displayed dose for {species}"


def test_no_exact_duplicate_drug_names_remain():
    seen: dict[str, str] = {}
    dupes = []
    for drug in DRUGS:
        key = str(drug.get("name", "")).strip().lower()
        if not key:
            continue
        if key in seen:
            dupes.append((key, seen[key], drug.get("id")))
        seen[key] = drug.get("id")
    assert not dupes, f"duplicate drug names still served: {dupes[:5]}"


@pytest.mark.parametrize("old_id", ["gabapentin_pain", "gabapentin_oral"])
def test_merged_drug_id_still_resolves(old_id):
    """Consolidation is logical: old ids keep working instead of 404ing."""
    assert resolve_drug_id(old_id) == "gabapentin"


def test_merged_drug_id_serves_over_http(old_id="gabapentin_pain"):
    flask_app = pytest.importorskip("api.vetdict_api", reason="flask not installed").app
    client = flask_app.test_client()
    resp = client.get(f"/api/drugs/{old_id}")
    assert resp.status_code == 200
    assert (resp.get_json() or {}).get("drug", {}).get("id") == "gabapentin"
