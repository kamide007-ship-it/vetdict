#!/usr/bin/env python3
"""Species drug caveats the corpus stated on some records but not others.

Both facts were already in this database, applied inconsistently — so whether a
vet saw the warning depended on which page they opened, which is worse than a
uniform omission because the reader cannot know the caveat exists.

* ~30-40% of rabbits carry serum atropinesterase, so atropine may simply fail;
  glycopyrrolate is preferred and tropicamide is used for mydriasis. Five records
  said so, ten prescribed atropine silently — including the bradycardia lines.
* African grey parrots are distinctly sensitive to itraconazole (anorexia,
  depression, hepatotoxicity at doses other psittacines tolerate).
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest

from scripts.template_elimination.species_drug_caveats import species_drug_caveat

DB_PATH = REPO_ROOT / "instance" / "vetdict.db"


def test_rabbit_atropine_gets_the_atropinesterase_caveat():
    text = "不整脈管理: 徐脈（AVブロック）: アトロピン 0.1-0.5 mg/kg SC/IV（急性期）。"
    out = species_drug_caveat("rabbit", "Congestive Heart Failure", "うっ血性心不全", text)
    assert out is not None
    assert "アトロピナーゼ" in out and "グリコピロレート" in out
    assert text.rstrip("。") in out, "the original therapy must be preserved"


def test_records_already_making_the_point_are_untouched():
    for text in (
        "散瞳が必要な場合はアトロピンではなくトロピカミドを使用（約30%にアトロピナーゼ）。",
        "アトロピン点眼 q12h（ウサギはアトロピナーゼあり→無効のことあり）。",
    ):
        assert species_drug_caveat("rabbit", "Uveitis", "ぶどう膜炎", text) is None


def test_bird_itraconazole_gets_the_african_grey_caveat():
    text = "抗真菌薬：イトラコナゾール 5-10 mg/kg PO q12h × 6-12週が第一選択。"
    out = species_drug_caveat("bird", "Aspergillosis", "アスペルギルス症", text)
    assert out is not None
    assert "ヨウム" in out and "ボリコナゾール" in out
    assert "イトラコナゾール 5-10 mg/kg" in out, "itraconazole stays first-line for birds generally"


def test_grey_caveat_skipped_when_already_present_in_any_phrasing():
    text = "イトラコナゾール 5-10 mg/kg PO q12h（African grey では減量）。"
    assert species_drug_caveat("parrot", "Aspergillosis", "アスペルギルス症", text) is None


def test_other_species_and_toxicosis_records_are_untouched():
    atropine = "アトロピン 0.04 mg/kg IV。"
    for species in ("dog", "cat", "horse", "ferret"):
        assert species_drug_caveat(species, "Bradycardia", "徐脈", atropine) is None
    # A record about the poisoning itself needs no prescribing caveat.
    assert species_drug_caveat("rabbit", "Atropine Toxicosis", "アトロピン中毒", atropine) is None


def test_caveat_is_idempotent():
    text = "アトロピン 0.1 mg/kg SC。"
    once = species_drug_caveat("rabbit", "Myocarditis", "心筋炎", text)
    assert once is not None
    assert species_drug_caveat("rabbit", "Myocarditis", "心筋炎", once) is None


@pytest.mark.skipif(not DB_PATH.is_file(), reason="served DB not built")
def test_served_db_has_no_uncaveated_rabbit_atropine():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT species, name, treatment_ja FROM diseases "
        "WHERE species IN ('rabbit','guinea_pig','chinchilla','degu') AND treatment_ja LIKE '%アトロピン%'"
    ).fetchall()
    conn.close()
    offenders = [
        (r["species"], r["name"])
        for r in rows
        if not any(k in (r["treatment_ja"] or "") for k in ("アトロピナーゼ", "グリコピロレート", "トロピカミド"))
    ]
    assert not offenders, f"atropine prescribed without the atropinesterase caveat: {offenders}"


@pytest.mark.skipif(not DB_PATH.is_file(), reason="served DB not built")
def test_served_db_bird_itraconazole_notes_grey_sensitivity():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT species, name, treatment_ja FROM diseases "
        "WHERE species IN ('bird','parakeet','parrot') AND treatment_ja LIKE '%イトラコナゾール%'"
    ).fetchall()
    conn.close()
    offenders = [
        (r["species"], r["name"])
        for r in rows
        if not any(k in (r["treatment_ja"] or "") for k in ("ヨウム", "African", "african", "アフリカ"))
    ]
    assert not offenders, f"itraconazole without the African grey caveat: {offenders[:5]}"
