#!/usr/bin/env python3
"""Chelonian ivermectin safety, and Japan-available antiparasitic products.

Two findings from extending the contraindication audit to ferrets, birds and
reptiles:

* Ivermectin is lethal in chelonians and this site's own drug dictionary already
  marks it ``safe=False`` / ``N/A`` for ``tortoise`` — yet tortoise disease pages
  prescribed it with a dose. One even claimed 「カメでの安全性は確立」, a truncation
  of 「確立されていない」 that asserted the opposite of the truth.
* The canine roundworm record's Japanese treatment was a generic template with no
  drug, dose or product, while its English text carried a usable protocol — so the
  Japanese-facing site (the primary audience) had nothing actionable.
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

from scripts.template_elimination.chelonian_ivermectin_safety import (
    make_chelonian_antiparasitics_safe,
    replacement_for,
)

DB_PATH = REPO_ROOT / "instance" / "vetdict.db"
_DOSED_IVERMECTIN = re.compile(r"(イベルメクチン|ivermectin)[^、。\n]{0,30}\d[\d.\-〜~ ]*(mg/kg|mcg/kg)", re.I)


def test_dosed_ivermectin_is_removed_for_chelonians():
    text = "⑥ イベルメクチン（爬虫類のみ）: 0.2 mg/kg IM/SC q14日 × 2回。"
    out = make_chelonian_antiparasitics_safe("tortoise", "Nematode Infection", "線虫感染", text)
    assert out is not None
    assert not _DOSED_IVERMECTIN.search(out.split("⚠")[0])
    assert "カメ類" in out and "禁忌" in out


def test_reversed_safety_claim_is_repaired():
    """「安全性は確立——」 is a truncation that reverses the meaning."""
    text = "イベルメクチン 0.2 mg/kg SC/PO q14日 × 2-3回（⚠カメでの安全性は確立——用量注意）。"
    out = make_chelonian_antiparasitics_safe("tortoise", "Ascarid Infection", "回虫感染症", text)
    assert out is not None
    assert "安全性は確立——" not in out
    assert not _DOSED_IVERMECTIN.search(out.split("⚠")[0])


def test_replacement_matches_the_parasite_class():
    """An ectoparasite record must not be handed an anthelmintic."""
    assert "フェンベンダゾール" in replacement_for("Ascarid Infection 回虫", "", "tortoise")
    assert "プラジクアンテル" in replacement_for("Cestode Infection 条虫", "", "tortoise")
    ecto = replacement_for("Tick Infestation マダニ", "", "tortoise")
    assert "フェンベンダゾール" not in ecto and "プラジクアンテル" not in ecto
    assert "物理的除去" in ecto


def test_snakes_and_lizards_are_untouched():
    """Ivermectin is safe and standard in squamates — do not over-correct."""
    text = "イベルメクチン 0.2 mg/kg SC/PO q14日 × 2回。"
    for species in ("snake", "lizard", "reptile"):
        assert make_chelonian_antiparasitics_safe(species, "Nematode Infection", "線虫感染", text) is None


def test_ivermectin_toxicosis_record_is_not_rewritten():
    """That record is *about* the poisoning; naming the drug is correct."""
    text = "リクガメにおけるイベルメクチン中毒の治療には迅速な除染と支持療法が必要である。"
    assert make_chelonian_antiparasitics_safe("tortoise", "Ivermectin Toxicosis", "イベルメクチン中毒", text) is None


@pytest.mark.skipif(not DB_PATH.is_file(), reason="served DB not built")
def test_served_db_has_no_dosed_ivermectin_for_chelonians():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT name, name_ja, treatment_ja FROM diseases WHERE species = 'tortoise'").fetchall()
    conn.close()
    offenders = [
        r["name"]
        for r in rows
        if not re.search(r"中毒|toxicos", f"{r['name']} {r['name_ja']}", re.I)
        and _DOSED_IVERMECTIN.search((r["treatment_ja"] or "").split("⚠")[0])
    ]
    assert not offenders, f"ivermectin still prescribed to chelonians: {offenders}"


@pytest.mark.skipif(not DB_PATH.is_file(), reason="served DB not built")
def test_canine_roundworm_names_real_drugs_and_jp_products():
    """The Japanese text must be as actionable as the English one."""
    conn = sqlite3.connect(str(DB_PATH))
    row = conn.execute("SELECT treatment_ja FROM diseases WHERE species = 'dog' AND name LIKE 'Roundworm%'").fetchone()
    conn.close()
    assert row, "canine roundworm record missing"
    tx = row[0] or ""
    # Real drugs with doses, not a generic "適切な駆虫薬" template.
    assert "パモ酸ピランテル" in tx and "mg/kg" in tx
    assert "ミルベマイシンオキシム" in tx, "milbemycin is a mainstay in Japan"
    # Japan-available product, with the label dose from the manufacturer.
    assert "プロコックス" in tx and "0.5 mL/kg" in tx
    assert "エモデプシド" in tx and "トルトラズリル" in tx
    # Puppy schedule and the zoonosis that makes this a public-health issue.
    assert "2週齢" in tx and "幼虫移行症" in tx
    assert "適切な駆虫薬が必要である" not in tx, "generic template must be gone"
