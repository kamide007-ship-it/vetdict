"""Tests for the non-destructive canonical consolidation layer (T103), degu pilot."""

from __future__ import annotations

import pytest

from api.species.canonical import (
    apply_canonical_map,
    load_canonical,
    resolve_redirect,
)


def test_degu_map_loads_with_expected_shape():
    cm = load_canonical("degu")
    assert cm is not None
    assert cm["species"] == "degu"
    assert len(cm["merges"]) >= 1
    # Each merge has a canonical + at least one merged entry, all with slugs.
    for mg in cm["merges"]:
        assert mg["canonical"]["slug"]
        assert mg["merged"]
        for m in mg["merged"]:
            assert m["slug"]


def test_unknown_species_is_noop():
    assert load_canonical("no_such_species") is None
    data = [{"name": "X", "name_ja": "X"}]
    assert apply_canonical_map(data, "no_such_species") is data


def test_apply_drops_merged_and_archived_keeps_canonical():
    cm = load_canonical("degu")
    canonical_slugs = {mg["canonical"]["slug"] for mg in cm["merges"]}
    merged_slugs = {m["slug"] for mg in cm["merges"] for m in mg["merged"]}
    archived_slugs = {a["slug"] for a in cm.get("archives", [])}

    # Synthetic served list containing canonical + merged + archived entries.
    def rec(slug):
        # reconstruct a plausible name whose slug matches
        return {"name": slug.replace("-", " ").title(), "name_ja": slug}

    records = [rec(s) for s in (canonical_slugs | merged_slugs | archived_slugs)]
    out = apply_canonical_map(records, "degu")
    from api.species.canonical import _slug

    out_slugs = {_slug(r["name"]) for r in out}
    # Slugs that must disappear: merged/archived EXCEPT any that are themselves a
    # canonical target (identical-name clusters share a slug on both sides).
    must_be_absent = (merged_slugs | archived_slugs) - canonical_slugs
    assert not (out_slugs & must_be_absent)
    # All canonical slugs survive.
    assert canonical_slugs <= out_slugs


def test_content_inheritance_takes_richest():
    from api.species.canonical import _inherit_content

    canonical = {"name": "A", "treatment_ja": "short"}
    sibling = {"name": "A-dup", "treatment_ja": "a much longer and richer treatment protocol"}
    merged = _inherit_content(canonical, [sibling])
    assert merged["treatment_ja"] == sibling["treatment_ja"]
    # original not mutated
    assert canonical["treatment_ja"] == "short"


def test_resolve_redirect_merged_to_canonical():
    cm = load_canonical("degu")
    mg = cm["merges"][0]
    merged_slug = mg["merged"][0]["slug"]
    canonical_slug = mg["canonical"]["slug"]
    assert resolve_redirect("degu", merged_slug) == canonical_slug
    # canonical itself does not redirect
    assert resolve_redirect("degu", canonical_slug) is None
    assert resolve_redirect("degu", "totally-made-up") is None


def test_served_degu_view_has_no_duplicate_or_archived():
    from api.species import degu_diseases as m
    from api.species.canonical import _slug
    from api.species.helpers import enrich_diseases

    served = enrich_diseases([dict(d) for d in m.DISEASES], "degu")
    names_en = [d.get("name") for d in served]
    served_slugs = {_slug(d.get("name") or d.get("name_en") or "") for d in served}

    # Archived research model is gone.
    assert not any("Alzheimer" in (n or "") for n in names_en)
    # Merged-away entries are gone (except identical-name clusters whose slug is
    # itself the canonical target — those legitimately remain as the canonical).
    cm = load_canonical("degu")
    canonical_slugs = {mg["canonical"]["slug"] for mg in cm["merges"]}
    merged_slugs = {m2["slug"] for mg in cm["merges"] for m2 in mg["merged"]}
    assert not (served_slugs & (merged_slugs - canonical_slugs))


def test_apply_is_idempotent():
    from api.species import degu_diseases as m
    from api.species.helpers import enrich_diseases

    served = enrich_diseases([dict(d) for d in m.DISEASES], "degu")
    once = apply_canonical_map(served, "degu")
    twice = apply_canonical_map(once, "degu")
    assert len(once) == len(twice)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
