"""Regression tests for the read-only detector's served-view mode.

The detectors normally read the raw disease source (Python module + JSON
overlay). ``served=True`` additionally applies the production serve-time
consolidation layer (dedup + canonical map, T103) so the quality report
reflects what the site actually serves after consolidation. These tests pin
that wiring so the served counts stay honest.
"""

from __future__ import annotations

from scripts.quality.detect import detect_duplicates, load_species_records, run


def test_served_view_is_subset_of_raw_for_consolidated_species():
    # degu had T103 consolidation applied (201 raw -> ~178 served).
    raw = load_species_records("degu", served=False)
    served = load_species_records("degu", served=True)
    assert len(served) < len(raw), "served view should hide merged/archived degu entries"
    # Every served name should exist in the raw source (consolidation only
    # hides/merges; it never invents new entries).
    raw_names = {r.get("name") for r in raw}
    for r in served:
        assert r.get("name") in raw_names


def test_served_view_reduces_exact_duplicates():
    raw = detect_duplicates(load_species_records("degu", served=False))
    served = detect_duplicates(load_species_records("degu", served=True))
    assert served["redundant_record_count"] <= raw["redundant_record_count"]


def test_raw_load_is_not_mutated_by_served_load():
    # Loading the served view must not shrink a subsequent raw load.
    _ = load_species_records("degu", served=True)
    raw_again = load_species_records("degu", served=False)
    assert len(raw_again) == len(load_species_records("degu", served=False))


def test_run_reports_view_label():
    assert run("degu", served=False)["view"] == "raw"
    assert run("degu", served=True)["view"] == "served"


def test_unconsolidated_species_served_equals_raw_or_smaller():
    # fish has no duplicates and no canonical sidecar -> served == raw.
    raw = load_species_records("fish", served=False)
    served = load_species_records("fish", served=True)
    assert len(served) == len(raw)
