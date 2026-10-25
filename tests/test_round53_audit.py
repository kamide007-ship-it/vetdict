"""2026-10 第78弾: 哺乳類の栄養テンプレート治療文の是正（ビタミンD中毒の救急・猫NSHPの甲状腺
治療文混入・馬過剰歯）、犬の偽妊娠（チャットDB）、チャット精度第53回、関連薬品チップ→動物種の用量カード着地。"""

import sqlite3
import warnings
from pathlib import Path

import pytest

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
DB = ROOT / "instance" / "vetdict.db"
warnings.filterwarnings("ignore")
MARKER = "栄養素過不足の特定と食事処方の見直しが治療の根幹"
MAMMALS = {
    "dog",
    "cat",
    "horse",
    "rabbit",
    "guinea_pig",
    "hamster",
    "chinchilla",
    "hedgehog",
    "sugar_glider",
    "ferret",
    "degu",
}


class TestMammalNutritionTreatments:
    def test_library_entries_have_no_template_or_wrong_taxa(self):
        from scripts.template_elimination.mammal_nutrition_treatment_library import ENTRIES

        for (sp, name), e in ENTRIES.items():
            assert MARKER not in e["ja"], (sp, name)
            assert "Exotic Animal Medicine for the Veterinary Technician" not in e["ja"]
            for t in (e["ja"], e.get("en", "")):
                assert "Birds—" not in t and "Reptiles—" not in t, (sp, name)
        # the vitamin D toxicoses stay emergencies with calciuresis
        for k in (("dog", "Vitamin D Toxicosis"), ("cat", "Feline Vitamin D Toxicosis")):
            assert (
                "救急" in ENTRIES[k]["ja"] and "生理食塩水" in ENTRIES[k]["ja"] and "パミドロネート" in ENTRIES[k]["ja"]
            )
        nshp = ENTRIES[("cat", "Nutritional Secondary Hyperparathyroidism")]
        assert "I-131" not in nshp["en"] and "メチマゾール" not in nshp["ja"]

    def test_json_overlay_fixed(self):
        import json

        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        for d in data:
            sp = (d.get("species") or "").lower().replace(" ", "_")
            if sp in MAMMALS:
                assert MARKER not in (d.get("treatment_ja") or ""), (sp, d.get("name"))
            if sp == "cat" and d.get("name") == "Nutritional Secondary Hyperparathyroidism":
                assert "hyperthyroidism" not in (d.get("treatment") or "").lower()

    @pytest.mark.skipif(not DB.exists(), reason="served DB not built")
    def test_served_db_has_no_mammal_nutrition_template_or_reptile_uvb(self):
        c = sqlite3.connect(DB)
        rows = c.execute("select species,name,treatment_ja,prevention_ja from diseases").fetchall()
        if len(rows) < 1000:
            pytest.skip("served DB not populated")
        bad = [(r[0], r[1]) for r in rows if r[0] in MAMMALS and MARKER in (r[2] or "")]
        assert not bad, bad
        uvb = [(r[0], r[1]) for r in rows if r[0] in MAMMALS and "UV-B（爬虫類・若齢動物）" in (r[3] or "")]
        assert not uvb, uvb[:5]

    def test_cross_species_strip_handles_reptile_uvb_clause(self):
        from api.species.helpers import strip_cross_species_text

        t = "OA予防: 適正体重維持。代謝性骨疾患予防: 適切な栄養とUV-B（爬虫類・若齢動物）。早期発見が重要。"
        assert "UV-B" not in strip_cross_species_text(t, "dog")
        assert "UV-B" in strip_cross_species_text(t, "lizard")


class TestPseudopregnancyChatEntry:
    def test_lactation_is_pseudopregnancy(self):
        ids, top = _dog("おっぱいが張ってお乳が出ます、避妊していません")
        assert "lactation" in ids and "偽妊娠" in top[0], (ids, top)

    def test_mammary_mass_stays_tumor(self):
        _, top = _dog("乳腺にしこりがあります")
        assert "乳腺腫瘍" in top[0], top

    def test_name_mirrors_dog_module(self):
        from api.health_checker import DISEASES
        from api.species import dog_diseases

        legacy = next(d for d in DISEASES if d["id"] == "pseudopregnancy")
        assert any(m["name"] == legacy["name_en"] and m["name_ja"] == legacy["name_ja"] for m in dog_diseases.DISEASES)


class TestChatClinicalAccuracyAuditRound53:
    def test_neck_pain_is_ivdd_not_ocular(self):
        ids, top = _dog("首を痛がってキャンと鳴きます")
        assert "neck_pain" in ids and "pain" not in ids and "椎間板" in top[0], (ids, top)

    def test_abdominal_guarding_tremor_is_acute_abdomen(self):
        ids, top = _dog("お腹を見せたがらず触ると嫌がって震えています")
        assert "abdominal_pain" in ids and "膵炎" in top[0], (ids, top)
        _, top = _dog("痙攣を起こして泡を吹きました")
        assert "てんかん" in top[0], top

    def test_budgie_cere_owner_phrase(self):
        ids, top = _sp("鼻の上が茶色くなってガサガサ", "parakeet")
        assert "cere_color_change" in ids and "蝋膜" in top[0], (ids, top)

    def test_oliguria_phrase(self):
        ids, _ = _dog("水を全然飲まず、おしっこもほとんどしない")
        assert "straining_to_urinate" in ids or "decreased_urination" in ids, ids


def test_related_drug_chip_lands_on_species_dose_card():
    assert "function _landOnSpeciesDose" in APP_JS
    assert APP_JS.count("navigateToDrug(tChip.dataset.drug,{landDose:true})") == 2
    assert ".drug-species-highlight" in APP_JS.split("function _landOnSpeciesDose", 1)[1][:400]


def test_nipple_and_ankle_swelling_are_not_cervical_lymph_nodes():
    ids, top = _dog("オスなのに乳首が腫れて毛が抜けて皮膚が黒ずむ")
    assert "swollen_lymph_nodes" not in ids and "精巣腫瘍" in top[0], (ids, top)
    ids, _ = _dog("足首が腫れて痛そう")
    assert "swollen_lymph_nodes" not in ids, ids
    ids, _ = _sp("足首が腫れています", "guinea_pig")
    assert "swollen_lymph_nodes" not in ids, ids
    ids, _ = _dog("首が腫れています")
    assert "swollen_lymph_nodes" in ids, ids


def test_dedupe_never_keeps_a_merged_away_twin_over_its_canonical():
    """Vanish guard: rabbit Vitamin D Toxicity (canonical) must stay browsable."""
    import json

    idx = json.loads((ROOT / "api" / "data" / "disease_search_index.json").read_text(encoding="utf-8"))
    entries = idx if isinstance(idx, list) else idx.get("entries", [])
    names = {(e.get("species"), e.get("name")) for e in entries}
    for key in (
        ("rabbit", "Vitamin D Toxicity"),
        ("chinchilla", "Ringworm (Dermatophytosis)"),
        ("ferret", "Urinary Tract Infection (UTI)"),
        ("bird", "Egg Yolk Peritonitis"),
    ):
        assert key in names, key
