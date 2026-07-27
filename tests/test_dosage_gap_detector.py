"""The dosage-gap detector must not cry wolf over drug-class conventions.

A naive "is there a qNh in the string" scan calls ~46% of the dictionary
incomplete. Most of those are correctly written: inhalant anaesthetics are dosed
as a MAC percentage, topicals are applied rather than dosed per kilo, induction
and emergency drugs are single doses to effect, antiparasitics say "repeat in 14
days" instead of qNh, and the sponsor's supplements point at the product label.

If the detector reported those as gaps it would send a vet chasing hundreds of
non-problems and bury the real ones, so the classification is pinned here.
"""

from __future__ import annotations

from scripts.quality.detect_dosage_gaps import FREQUENCY, NOT_APPLICABLE, ROUTE, UNESTABLISHED, scan


def test_frequency_accepts_real_world_notations():
    for text in (
        "5-10 mg/kg PO/IM q24-48h",  # hyphenated range — missed by a naive \bq\d+h\b
        "10 mg/kg PO q48-72h",
        "0.2-0.4 mg/kg SC; repeat in 14 days",  # antiparasitic schedule
        "2.5-5 mg/L bath for 5-10 days",  # immersion duration
        "0.05-1 mcg/kg/min CRI",  # continuous infusion
        "5 mg/kg IV once",
        "1日2回 経口",
        "20 mg/kg 経口 12時間毎",
    ):
        assert FREQUENCY.search(text), f"frequency not recognised in {text!r}"


def test_route_accepts_japanese_and_english():
    for text in ("5 mg/kg PO", "0.1 mg/kg SC", "2.5 mg/kg 経口", "局所に塗布", "10 mg/L 薬浴"):
        assert ROUTE.search(text), f"route not recognised in {text!r}"


def test_contraindicated_entries_are_not_treated_as_gaps():
    for text in ("N/A 使用不可", "Contraindicated", "禁忌"):
        assert NOT_APPLICABLE.search(text)


def test_unestablished_is_distinguished_from_a_defect():
    """ "Not well established" is a truthful blank, not a missing-data bug."""
    assert UNESTABLISHED.search("Not well established 十分に確立されていない")


def test_scan_excludes_class_correct_entries_and_stays_bounded():
    report = scan()
    # The class-aware exclusions must actually be doing work, otherwise the
    # detector has silently regressed into the naive scan.
    assert report["excluded_by_class"], "no class exclusions applied"
    assert sum(report["excluded_by_class"].values()) > 100

    # Real gaps should be a reviewable worklist, not "half the dictionary".
    assert report["total_gaps"] < 900, f"detector regressed to naive scan: {report['total_gaps']}"
    assert report["unestablished_count"] >= 1

    # Nothing that survived as a gap may be an inhalant, a supplement, or a
    # contraindication — those are exactly the false positives being guarded.
    for gap in report["gaps"]:
        name = gap["drug"].lower()
        assert "isoflurane" not in name and "sevoflurane" not in name
        assert "refer to product label" not in gap["dosage"].lower()
