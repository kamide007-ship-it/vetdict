"""2026-10 第74弾: チャット精度第49回・亀頭包皮炎の新設（犬モジュール＋チャットDB）・
前立腺肥大症のチャット経路・イゼニベトマブ（レニビア）公開・英語ボイラープレート是正・
検索欄 Enter 着地（スマホの「検索」キー）。"""

import json
import re
import sqlite3
import warnings
from pathlib import Path

import pytest

from tests.test_round46_audit import _dog, _horse, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
DB = ROOT / "instance" / "vetdict.db"
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound49:
    def test_purulent_preputial_discharge_is_balanoposthitis(self):
        ids, top = _dog("陰茎から膿が出ています")
        assert ids == {"preputial_discharge"} and top[0] == "亀頭包皮炎", (ids, top)

    def test_bloody_preputial_discharge_with_hematuria_is_bph(self):
        _, top = _dog("おちんちんから血が出ておしっこに血が混じります")
        assert top[0] == "良性前立腺肥大症", top
        _, top = _dog("陰茎から血が垂れて便が細い")
        assert top[0] == "良性前立腺肥大症", top

    def test_female_vulvar_discharge_still_pyometra(self):
        # 雄の分泌物を新設しても雌の子宮蓄膿症ゲートは不変
        _, top = _dog("陰部から膿が出て水をよく飲む")
        assert top[0] == "子宮蓄膿症", top

    def test_preputial_chain_never_falls_back_to_vulvar(self):
        from api.chat.symptom_extractor import ID_SYNONYMS

        assert "vulvar_discharge" not in ID_SYNONYMS["preputial_discharge"]
        ids, _ = _sp("包皮から膿が出ています", "ferret")
        assert ids & {"discharge_from_prepuce", "preputial_swelling"}, ids

    def test_dog_red_papules_and_patchy_alopecia(self):
        ids, top = _dog("お腹の皮膚に赤いぶつぶつがあります")
        assert "skin_rashes" in ids and any("膿皮" in t or "アレルギー" in t for t in top), top
        ids, _ = _dog("毛が束になって抜けて地肌が見えています")
        assert "hair_loss" in ids

    def test_tail_base_pain_not_glaucoma(self):
        ids, top = _dog("尻尾を触ると痛がります")
        assert "back_pain" in ids and "緑内障" not in top[0], top

    def test_cat_frequent_litter_visits(self):
        ids, top = _sp("トイレに何回も行きます", "cat")
        assert "frequent_urination" in ids and any("膀胱" in t or "尿" in t for t in top), top

    def test_cat_scratching_behind_ears(self):
        ids, _ = _sp("耳の後ろを掻きこわしています", "cat")
        assert "scratching_ears" in ids, ids

    def test_frequency_adverb_stripped(self):
        from api.chat.symptom_extractor import normalize_chat_text

        assert normalize_chat_text("毛玉を頻繁に吐きます") == "毛玉を吐く"

    def test_parakeet_head_flicking_extracted(self):
        ids, top = _sp("嘔吐して首を振っています", "parakeet")
        assert "head_shaking" in ids and any("嗉嚢" in t or "そ嚢" in t for t in top), top

    def test_amphibian_skin_peeling_is_chytrid(self):
        ids, top = _sp("皮膚がはがれて元気がありません", "amphibian")
        assert "excessive_shedding" in ids and any("ツボカビ" in t for t in top), top

    def test_parakeet_dry_beak_scale(self):
        ids, top = _sp("くちばしの周りがかさかさです", "parakeet")
        assert ids and any("疥癬" in t for t in top), top

    def test_cat_weight_loss_with_poor_coat_extracts_both(self):
        ids, _ = _sp("痩せて毛艶が悪くなりました", "cat")
        assert {"weight_loss", "poor_coat"} <= ids, ids

    def test_horse_throat_swelling_dysphagia_is_strangles(self):
        ids, top = _horse("喉が腫れて飲み込めない")
        assert "body_swelling" not in ids and "腺疫" in top[0], (ids, top)
        _, top = _horse("鼻から餌が出て飲み込めない")
        assert "チョーク" in top[0], top

    def test_horse_hiragana_hind_lameness(self):
        ids, _ = _horse("後ろ足をひきずっています")
        assert ids == {"limb_lameness_hind"}, ids


class TestBalanoposthitisEntry:
    def test_legacy_name_mirrors_dog_module(self):
        from api.chat.species_data import get_species_data
        from api.health_checker import DISEASES

        legacy = {d["id"]: d for d in DISEASES}
        mod = {(d["name"] if isinstance(d, dict) else d.name) for d in get_species_data("dog")["diseases"]}
        assert legacy["balanoposthitis"]["name_en"] in mod
        assert legacy["benign_prostatic_hyperplasia"]["name_en"] in mod

    def test_module_entry_is_curated(self):
        from api.species.dog_diseases import DISEASES

        e = next(d for d in DISEASES if d["name"] == "Balanoposthitis")
        for f in (
            "description",
            "causes",
            "pathophysiology",
            "clinical_signs",
            "diagnosis",
            "treatment",
            "prognosis",
            "prevention",
        ):
            assert e.get(f) and e.get(f + "_ja"), f
        assert "スメグマ" in e["description_ja"] and "chlorhexidine" in e["treatment"]

    def test_prevalence_keys(self):
        from api.species.prevalence_data import SPECIES_PREVALENCE

        assert SPECIES_PREVALENCE["dog"]["Balanoposthitis"] == "common"
        assert SPECIES_PREVALENCE["dog"]["Benign Prostatic Hyperplasia (BPH)"] == "common"

    @pytest.mark.skipif(not DB.exists(), reason="served DB not built")
    def test_served_db_has_entry(self):
        con = sqlite3.connect(DB)
        try:
            row = con.execute(
                "select treatment_ja from diseases where species='dog' and name='Balanoposthitis'"
            ).fetchone()
        finally:
            con.close()
        if row is None:
            pytest.skip("served DB predates this entry")
        assert "クロルヘキシジン" in row[0]


class TestEnglishBoilerplateFixed:
    MARKS = (
        "Multifactorial etiology including infectious, environmental, immune, and host-related",
        "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary",
    )

    def test_reproductive_entries_have_specific_english(self):
        from api.species import cat_diseases, dog_diseases

        names = {
            "Pseudopregnancy (False Pregnancy / Galactorrhea)",
            "Pseudopregnancy (Feline)",
            "Ovarian Cysts (Feline)",
            "Postpartum Metritis (Feline)",
        }
        for e in [*dog_diseases.DISEASES, *cat_diseases.DISEASES]:
            if e.get("name") in names:
                for f in ("causes", "prevention"):
                    assert not any(m in (e.get(f) or "") for m in self.MARKS), (e["name"], f)


class TestBatch83Izenivetmab:
    def _drug(self):
        from api.drug_dictionary import DRUGS

        return next(d for d in DRUGS if d["id"] == "izenivetmab")

    def test_label_dosing_and_contraindications(self):
        d = self._drug()
        dog = d["species_info"]["dog"]
        assert "0.05-0.1 mg/kg" in dog["dosage"] and "3 months" in dog["dosage"]
        for band in ("5-10 kg 0.5 mg", "40.1-60 kg 3.0 mg", "0.1 mL/kg"):
            assert band in dog["dosage"], band
        assert "3ヶ月に1回" in dog["dosage_ja"] and "12ヶ月齢以上" in dog["dosage_ja"]
        assert d["species_info"]["cat"]["safe"] is False
        assert "12 months" in d["contraindications"] and "lactating" in d["contraindications"]
        assert "3.46%" in dog["notes"]

    def test_resolution_and_duplicate_anti_ngf_interaction(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference
        from api.drug_interactions import find_interactions

        assert resolve_drug_reference("レニビア") == "izenivetmab"
        assert resolve_drug_reference("いぜにべとまぶ") == "izenivetmab"
        hits = [x["id"] if isinstance(x, dict) else x for x in find_drugs_in_text("イゼニベトマブ（レニビア）")]
        assert "izenivetmab" in hits
        res = find_interactions(["izenivetmab", "bedinvetmab"])
        assert res and res[0]["severity"] == "major"

    def test_dog_oa_treatment_mentions_it(self):
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        oa = next(e for e in data if e.get("species") == "Dog" and e.get("name") == "Osteoarthritis")
        assert "イゼニベトマブ" in oa["treatment_ja"] and "Izenivetmab" in oa["treatment"]


def test_list_search_enter_lands_on_results():
    assert "function setupListSearchEnter" in APP_JS
    assert '_boot("listSearchEnter",setupListSearchEnter)' in APP_JS
    body = APP_JS[APP_JS.index("function setupListSearchEnter") :][:2000]
    for inp in ("diseaseSearch", "drugSearch", "anesthesiaSearch", "emergencySearch"):
        assert inp in body
    assert "input.blur()" in body and "toggleDbItem(target)" in body
    # global search: Enter without highlight opens the first result
    assert 'e.key==="Enter"&&!e.isComposing){' in APP_JS
    assert "items.find(it=>base(it.dataset.name)===q||base(it.dataset.nameJa)===q))||items[0]" in APP_JS


def test_sw_cache_bumped():
    sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
    assert int(re.search(r"vetdict-v(\d+)", sw).group(1)) >= 186
