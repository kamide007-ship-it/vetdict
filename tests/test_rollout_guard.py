"""Regression tests for the rollout failure-guard (`_evaluate_guards`).

Two historical bugs this pins:

1. **Dead guards.** `_GUARD` once keyed on detector-internal names
   (`exact_duplicate_cluster_count`, `family_cluster_count`, `heading_only`) that
   never matched the summary *row* keys (`dup_clusters`, `families`,
   `heading_only_tx`), so those guards silently read 0 and could never fire — a
   failure-detection guard that could not fail.
2. **False halt-warnings.** The drug/citation mis-link guards evaluated the *raw*
   pre-guard count, tripping the SPEC auto-stop on amphibian/exotic_other even
   though the shipped T108 species-guard reduces the production residual to 0.
   Those are benign (production absorbs them) and must be an informational note,
   not a halt-warning.
"""

from __future__ import annotations

from scripts.quality.rollout import _GUARD, _evaluate_guards


def _row(species="amphibian", **over):
    base = {
        "species": species,
        "dup_clusters": 0,
        "families": 0,
        "nonclinical": 0,
        "heading_only_tx": 0,
        "drug_mismatch": 0,
        "citation_mismatch": 0,
        "drug_mismatch_residual": 0,
        "citation_mismatch_residual": 0,
        "mt_review": 0,
    }
    base.update(over)
    return base


def test_guard_keys_match_row_fields():
    # Every guard key must be a real row field, or the guard is dead.
    row = _row()
    for key in _GUARD:
        assert key in row, f"guard key {key!r} does not match any row field"


def test_absorbed_drug_mismatch_is_benign_not_warning():
    # Raw far over ceiling, but shipped guard residual 0 → benign note, no warning.
    rows = [_row(drug_mismatch=220, drug_mismatch_residual=0)]
    warnings, benign = _evaluate_guards(rows)
    assert warnings == []
    assert len(benign) == 1 and "benign" in benign[0] and "amphibian" in benign[0]


def test_leaking_drug_guard_is_a_real_warning():
    # Residual itself over ceiling means the shipped guard is leaking → real halt.
    rows = [_row(drug_mismatch=500, drug_mismatch_residual=250)]
    warnings, benign = _evaluate_guards(rows)
    assert benign == []
    assert len(warnings) == 1 and "leaking" in warnings[0]


def test_citation_mismatch_residual_aware():
    rows = [_row(citation_mismatch=300, citation_mismatch_residual=0)]
    warnings, benign = _evaluate_guards(rows)
    assert warnings == []
    assert benign and "citation_mismatch" in benign[0]


def test_revived_dup_cluster_guard_fires_on_explosion():
    # Previously dead; must now fire when exact-duplicate clusters explode.
    rows = [_row(species="dog", dup_clusters=_GUARD["dup_clusters"] + 1)]
    warnings, _ = _evaluate_guards(rows)
    assert len(warnings) == 1 and "dup_clusters" in warnings[0]


def test_normal_family_scale_does_not_false_fire():
    # Family candidates are review targets that scale with corpus size (horse=123,
    # dog=119 are normal) — they must stay under the ceiling and not warn.
    rows = [_row(species="horse", families=123), _row(species="dog", families=119)]
    warnings, benign = _evaluate_guards(rows)
    assert warnings == []
    assert benign == []


def test_gross_family_explosion_still_fires():
    rows = [_row(families=_GUARD["families"] + 1)]
    warnings, _ = _evaluate_guards(rows)
    assert len(warnings) == 1 and "families" in warnings[0]


def test_clean_rows_yield_nothing():
    warnings, benign = _evaluate_guards([_row(), _row(species="fish")])
    assert warnings == [] and benign == []
