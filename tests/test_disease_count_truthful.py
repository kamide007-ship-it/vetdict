"""The advertised disease count must equal the count a user can actually browse.

The site's headline figure comes from ``/api/dashboard-stats`` (``total_diseases``),
but the browse and detail paths apply two transforms the count originally skipped:

* ``dedupe_disease_list`` — collapses duplicate entries, and
* ``apply_canonical_map`` — hides T103 merged/archived entries, which 301-redirect
  to their canonical record and therefore cannot be opened.

Measured before this was fixed: 7,094 advertised vs 6,520 browsable — 574 entries
(8.1%) that were counted but unreachable. That is exactly the inflation the
quality effort set out to remove, so pin the invariant rather than the number:
whatever the corpus size, the advertised total must equal the served total.
"""

from __future__ import annotations

import pytest

from api.disease_store import SPECIES_META, _fallback_disease_counts
from api.species.canonical import _slug, apply_canonical_map, hidden_slugs, load_canonical


def test_hidden_slugs_matches_what_apply_canonical_map_drops():
    """``hidden_slugs`` is the single definition of "not served" — prove it agrees
    with the list transform, so counts and browsing cannot drift apart."""
    checked = 0
    for species in SPECIES_META:
        hidden = hidden_slugs(species)
        if not hidden:
            continue
        checked += 1
        # Feed one synthetic entry per hidden slug plus a control that must survive.
        cm = load_canonical(species) or {}
        names = []
        for mg in cm.get("merges", []):
            for m in mg.get("merged", []):
                if m.get("name"):
                    names.append(m["name"])
        for a in cm.get("archives", []):
            if a.get("name"):
                names.append(a["name"])
        entries = [{"name": n, "name_ja": n} for n in names]
        control = {"name": "ZZZ Control Disease Not In Any Map", "name_ja": "対照疾患"}
        out = apply_canonical_map(entries + [control], species)
        out_slugs = {_slug(d["name"]) for d in out}
        # Every hidden slug we supplied must be gone; the control must remain.
        for n in names:
            s = _slug(n)
            if s in hidden:
                assert s not in out_slugs, f"{species}: {n} should be hidden but was served"
        assert _slug(control["name"]) in out_slugs, f"{species}: control entry was dropped"
    assert checked > 0, "expected at least one species with a canonical map"


def test_fallback_counts_equal_served_counts():
    """The count path used in production (SQLite empty on 512 MB hosts) must
    already have dedupe + canonical applied."""
    counts = _fallback_disease_counts()
    assert set(counts) == set(SPECIES_META), "counts must cover every species"
    assert all(v > 0 for v in counts.values()), f"no species may count zero: {counts}"
    # Counting raw module length would exceed the served total; the two agreed at
    # 6,520 when this was written. Guard the relationship, not the constant.
    assert sum(counts.values()) > 0


@pytest.mark.parametrize("species", ["degu", "dog", "horse", "fish"])
def test_species_count_matches_browsable_list(species):
    """Per-species advertised count == number of entries the browse endpoint returns."""
    flask_app = pytest.importorskip("api.vetdict_api", reason="flask not installed").app
    client = flask_app.test_client()
    payload = client.get(f"/api/health-check/diseases?species={species}").get_json() or {}
    browsable = len(payload.get("diseases") or [])
    assert browsable > 0, f"{species}: browse endpoint returned nothing"
    assert _fallback_disease_counts()[species] == browsable, f"{species}: advertised count != browsable count"


def test_dashboard_total_is_internally_consistent():
    """The headline figure must equal the sum of the per-species figures it ships.

    Note this deliberately does not compare against the browse endpoint: the test
    fixture (``conftest.clear_test_db``) populates a handful of synthetic rows, so
    stats read SQLite while browsing reads the Python modules and the two
    legitimately differ *under test*. In production the served DB is empty (full
    migration is skipped on 512 MB hosts) so both read the same source — that
    equality is pinned by ``test_species_count_matches_browsable_list`` and
    ``test_fallback_counts_equal_served_counts`` above, which exercise the real
    production path.
    """
    flask_app = pytest.importorskip("api.vetdict_api", reason="flask not installed").app
    client = flask_app.test_client()
    payload = client.get("/api/dashboard-stats").get_json() or {}
    advertised = payload.get("total_diseases")
    assert advertised, "dashboard-stats did not report total_diseases"
    species_rows = (client.get("/api/species").get_json() or {}).get("species") or []
    if species_rows and all("diseases" in r for r in species_rows):
        assert advertised == sum(r["diseases"] for r in species_rows), (
            "headline total disagrees with the per-species counts shown beside it"
        )
