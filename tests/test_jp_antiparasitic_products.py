#!/usr/bin/env python3
"""Japan-available antiparasitic products on the parasitology records.

The records listed generic actives but rarely the product a Japanese vet orders
by name, so the advice stopped short of the decision being made. This guards the
product block, the two safety notes that ride with it, and — most importantly —
the substring collisions that would attach the wrong product list.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest

from scripts.template_elimination.jp_antiparasitic_products import apply_jp_products, jp_product_block

DB_PATH = REPO_ROOT / "instance" / "vetdict.db"
_BASE = "駆虫を行う。"


def test_products_match_the_parasite_and_species():
    dog_worm = jp_product_block("dog", "Roundworm Infection (Toxocara)", "回虫症", _BASE)
    assert dog_worm and "プロコックス" in dog_worm and "ドロンタール" in dog_worm
    assert "0.5 mL/kg" in dog_worm, "the one published per-kg figure must be kept"

    cat_worm = jp_product_block("cat", "Roundworm Infection", "回虫症", _BASE)
    assert cat_worm and "ブロードライン" in cat_worm
    assert "ドロンタール" not in cat_worm, "canine tablet must not be offered for a cat"


def test_weight_band_products_do_not_invent_a_dose():
    """Spot-ons and chewables are dosed from the pack, not by mg/kg."""
    block = jp_product_block("dog", "Flea Infestation", "ノミ寄生症", _BASE)
    assert block and "体重帯別に製品ラベルに従う" in block
    assert "mg/kg" not in block, "must not fabricate a mg/kg for a weight-band product"


def test_cat_flea_block_warns_about_canine_permethrin():
    block = jp_product_block("cat", "Flea Infestation", "ノミ寄生症", _BASE)
    assert block and "ペルメトリン" in block and "絶対に使用しない" in block


def test_heartworm_block_requires_pre_treatment_testing():
    block = jp_product_block("dog", "Heartworm Disease", "犬糸状虫症", _BASE)
    assert block and "抗原検査" in block and "ミクロフィラリア" in block


def test_echinococcus_notifiable_status_is_stated():
    block = jp_product_block("dog", "Tapeworm Infection (Dipylidium/Echinococcus)", "条虫症", _BASE)
    assert block and "エキノコックス" in block and "届出" in block


def test_coccidioidomycosis_is_not_treated_as_coccidiosis():
    """Coccidioides is a systemic FUNGUS — it must not get an anticoccidial."""
    for species, name, name_ja in (
        ("dog", "Coccidioidomycosis (Valley Fever)", "コクシジオイデス症（渓谷熱）"),
        ("cat", "Feline Coccidioidomycosis", "猫コクシジオイデス症"),
    ):
        assert jp_product_block(species, name, name_ja, _BASE) is None
    # The genuine protozoal record still gets its block.
    assert jp_product_block("dog", "Coccidiosis", "コクシジウム症", _BASE) is not None


def test_cytauxzoonosis_is_not_treated_as_a_tick_infestation():
    """A tick-BORNE protozoal disease is not a tick infestation."""
    assert jp_product_block("cat", "Tick-Borne Disease (Cytauxzoonosis)", "シタウクソーン症", _BASE) is None


def test_block_is_idempotent():
    once = apply_jp_products("dog", "Flea Infestation", "ノミ寄生症", _BASE)
    assert once is not None
    assert apply_jp_products("dog", "Flea Infestation", "ノミ寄生症", once) is None


@pytest.mark.skipif(not DB_PATH.is_file(), reason="served DB not built")
def test_served_db_carries_the_product_block():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT species, name, treatment_ja FROM diseases "
        "WHERE species IN ('dog','cat') AND treatment_ja LIKE '%日本国内で入手可能な代表的製剤%'"
    ).fetchall()
    conn.close()
    assert len(rows) >= 20, f"expected the parasitology records to carry the block, got {len(rows)}"
    # No record may carry it twice.
    for row in rows:
        assert (row["treatment_ja"] or "").count("【日本国内で入手可能な代表的製剤】") == 1, (
            f"{row['species']}/{row['name']}: product block duplicated"
        )


def test_exotic_species_blocks_flag_their_lethal_drug():
    """Exotics have almost nothing licensed, so the contraindication is the point."""
    herb = jp_product_block("rabbit", "Ear Mite Infestation", "耳ダニ症", _BASE)
    assert herb and "フィプロニル" in herb and "禁忌" in herb

    bird = jp_product_block("parrot", "Knemidokoptes Mite", "トリヒゼンダニ症", _BASE)
    assert bird and "イベルメクチン" in bird
    assert "フィプロニル" in bird and "鳥に用いない" in bird

    ferret = jp_product_block("ferret", "Flea Infestation", "ノミ寄生症", _BASE)
    assert ferret and "セラメクチン" in ferret
    assert "適応外" in ferret, "must be honest that these are off-label"
    assert "フィラリア" in ferret, "ferrets are highly susceptible to heartworm"


def test_added_products_are_present():
    dog_worm = jp_product_block("dog", "Roundworm Infection", "回虫症", _BASE)
    assert dog_worm and "カルドメック" in dog_worm and "シンパリカ®トリオ" in dog_worm
    cat_flea = jp_product_block("cat", "Flea Infestation", "ノミ寄生症", _BASE)
    assert cat_flea and "レボリューション®プラス" in cat_flea
