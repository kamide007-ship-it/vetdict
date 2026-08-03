#!/usr/bin/env python3
"""Oral penicillins/lincosamides must never be prescribed to hindgut fermenters.

In rabbits, guinea pigs, chinchillas and degus these drugs destroy the caecal
flora, *Clostridium spiroforme* overgrows and the animal dies of enterotoxaemia.
The corpus prescribed them by mouth, with a dose, on 100 records — many from a
shared template whose own parenthesis read "（小型哺乳類除く）" while sitting on
the chinchilla page.
"""

from __future__ import annotations

import re
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest

from scripts.template_elimination.hindgut_antibiotic_safety import (
    HINDGUT_SPECIES,
    make_oral_antibiotics_safe,
    substitute_for,
)

_DANGER = re.compile(
    r"(アモキシシリン|amoxicillin|アンピシリン|ampicillin|クリンダマイシン|clindamycin"
    r"|リンコマイシン|lincomycin|セファレキシン|cephalexin|エリスロマイシン|erythromycin)",
    re.I,
)
_ORAL = re.compile(r"\bPO\b|経口|内服")
_DOSE = re.compile(r"\d[\d.\-〜~ ]*mg/kg")
_WARN = re.compile(r"(禁忌|致死|使用しない|投与しない|避け|contraindicat|fatal|avoid|never)", re.I)

DB_PATH = REPO_ROOT / "instance" / "vetdict.db"


def _prescribes_unsafely(text: str) -> bool:
    for sentence in re.split(r"(?<=[。．])", text or ""):
        if _WARN.search(sentence) or not _DOSE.search(sentence):
            continue
        if not _DANGER.search(sentence):
            continue
        # Ampicillin is contraindicated by any route; the rest need an oral marker.
        if _ORAL.search(sentence) or re.search(r"アンピシリン|ampicillin", sentence, re.I):
            return True
    return False


def test_rewrites_oral_beta_lactam_to_safe_alternative():
    text = "乳腺炎は培養感受性試験を指針とし、エンロフロキサシン 5-15 mg/kg PO/IM q12-24h またはアモキシシリン・クラブラン酸 12.5-25 mg/kg PO q12h（小型哺乳類除く）を開始。"
    out = make_oral_antibiotics_safe("chinchilla", text)
    assert out is not None
    # The drug may only appear in the appended contraindication line, never in
    # the therapy itself, so check the body before the ⚠ warning.
    body = out.split("⚠")[0]
    assert "アモキシシリン" not in body
    assert "トリメトプリム・スルファ" in body
    assert "エンロフロキサシン" in body, "safe alternatives already present must be preserved"
    assert "Clostridium spiroforme" in out, "must explain why the drug was removed"


def test_substitute_dose_comes_from_the_drug_dictionary():
    """The replacement dose must be the vet-reviewed per-species formulary figure.

    A single hardcoded dose would be wrong for half the group: trimethoprim-sulfa
    is 30 mg/kg PO q12h in the rabbit and guinea pig but 15-30 mg/kg in the
    chinchilla and degu, and metronidazole is 20 mg/kg except in the chinchilla
    (10-20 mg/kg). Reading the dictionary keeps the rewritten treatment and the
    published drug tab from ever disagreeing.
    """
    from api.drug_dictionary import get_drug_by_id

    for species in sorted(HINDGUT_SPECIES):
        for drug_id, anaerobic in (("trimethoprim_sulfa", False), ("metronidazole", True)):
            expected = get_drug_by_id(drug_id)["species_info"][species]["dosage"]
            out = substitute_for(species, anaerobic=anaerobic)
            assert expected in out, f"{species}/{drug_id}: {out!r} does not carry formulary dose {expected!r}"
            # The surrounding prescribing text uses the PO/q12h convention.
            assert "mg/kg" in out and "PO" in out


def test_substitute_dose_varies_by_species():
    """Guard the specific figures that differ, so a regression is visible."""
    assert substitute_for("rabbit", anaerobic=False) != substitute_for("chinchilla", anaerobic=False)
    assert "30 mg/kg" in substitute_for("rabbit", anaerobic=False)
    assert "15-30 mg/kg" in substitute_for("chinchilla", anaerobic=False)
    assert "10-20 mg/kg" in substitute_for("chinchilla", anaerobic=True)
    assert "20 mg/kg" in substitute_for("degu", anaerobic=True)


def test_lincosamide_becomes_metronidazole():
    out = make_oral_antibiotics_safe("rabbit", "クリンダマイシン 5.5-11 mg/kg PO BID。")
    assert out is not None and "メトロニダゾール" in out and "クリンダマイシン" not in out.split("⚠")[0]


def test_ampicillin_swapped_even_when_parenteral():
    """Ampicillin is contraindicated in these species by any route."""
    out = make_oral_antibiotics_safe("rabbit", "具体的な薬剤目安: Ampicillin 20 mg/kg IV、enrofloxacin 5-10 mg/kg IV。")
    assert out is not None and "Ampicillin" not in out.split("⚠")[0]


def test_parenteral_penicillin_g_is_preserved():
    """Penicillin G SC/IM bypasses the gut and is used clinically — keep it."""
    text = "■ 抗菌薬: ペニシリンG 20,000-40,000 IU/kg IM/SC BID × 10-14日。"
    assert make_oral_antibiotics_safe("chinchilla", text) is None


def test_existing_contraindication_warnings_are_not_rewritten():
    text = "■禁忌: ペニシリン系・セファロスポリン系・リンコマイシン系は致死的腸炎→絶対禁忌。"
    assert make_oral_antibiotics_safe("guinea_pig", text) is None


def test_other_species_are_untouched():
    text = "アモキシシリン・クラブラン酸 12.5-25 mg/kg PO q12h。"
    for species in ("dog", "cat", "ferret", "horse"):
        assert make_oral_antibiotics_safe(species, text) is None


@pytest.mark.skipif(not DB_PATH.is_file(), reason="served DB not built")
def test_served_db_has_no_unsafe_hindgut_prescriptions():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    placeholders = ",".join("?" * len(HINDGUT_SPECIES))
    rows = conn.execute(
        f"SELECT species, name, treatment_ja FROM diseases WHERE species IN ({placeholders})",
        tuple(sorted(HINDGUT_SPECIES)),
    ).fetchall()
    conn.close()
    offenders = [(r["species"], r["name"]) for r in rows if _prescribes_unsafely(r["treatment_ja"] or "")]
    assert not offenders, f"unsafe oral antibiotic advice for hindgut fermenters: {offenders[:5]}"
