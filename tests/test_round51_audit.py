"""2026-10 第76弾: 多種列挙型テンプレートの種間汚染除去・Palladia/マシチニブ ID 衝突の是正・
リーシュマニア症予防のキュレーション・デルタメトリン首輪公開・チャット精度第51回・
疾患詳細ジャンプバーの「予防」チップ。"""

import json
import sqlite3
import warnings
from pathlib import Path

import pytest

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
DB = ROOT / "instance" / "vetdict.db"
warnings.filterwarnings("ignore")


class TestCrossSpeciesEnumerationStrip:
    def test_herbivore_and_bird_clauses_dropped_for_dog(self):
        from api.species.helpers import strip_cross_species_text as f

        t = (
            "管理が中心。小動物（犬猫）: 毎日の歯磨き。"
            "草食動物（ウサギ・モルモット・チンチラ・デグー）: 高繊維チモシー乾草を主食。鳥類: カトルボーン。早期発見。"
        )
        assert f(t, "dog") == "管理が中心。小動物（犬猫）: 毎日の歯磨き。早期発見。"
        assert "チモシー" in f(t, "rabbit") and "犬猫" not in f(t, "rabbit")
        assert "カトルボーン" in f(t, "parakeet") and "チモシー" not in f(t, "parakeet")

    def test_reptile_uvb_clause_and_tooth_trimming_gated(self):
        from api.species.helpers import strip_cross_species_text as f

        t = "カルシウム不足: 骨軟化。ビタミンD/UV-B不足（爬虫類）: 代謝性骨疾患・骨軟化。"
        assert "爬虫類" not in f(t, "cat") and "爬虫類" in f(t, "tortoise")
        tx = "歯科検査が必要である。不正咬合は種と重症度に応じて歯のトリミング、研磨、抜歯が必要となる。スケーリング。"
        assert "トリミング" not in f(tx, "dog") and "トリミング" in f(tx, "rabbit") and "トリミング" in f(tx, "horse")

    def test_inline_herbivore_nutrition_replaced_for_carnivores(self):
        from api.species.helpers import strip_cross_species_text as f

        t = "給餌が要となる（草食性小動物は高繊維チモシー乾草を主体に、モルモットはビタミンCを継続補給、糖質過多を避ける）。"
        assert "肉食" in f(t, "ferret") and "チモシー" not in f(t, "ferret")
        assert "チモシー" in f(t, "guinea_pig")

    @pytest.mark.skipif(not DB.exists(), reason="served DB not built")
    def test_served_db_has_no_foreign_group_clauses(self):
        con = sqlite3.connect(DB)
        bad = con.execute(
            "select count(*) from diseases where species in ('dog','cat','ferret','hedgehog','sugar_glider') "
            "and (prevention_ja like '%チモシー乾草%' or treatment_ja like '%歯のトリミング%' "
            "or clinical_signs_ja like '%UV-B不足（爬虫類）%' or prevention_ja like '%カトルボーン%')"
        ).fetchone()[0]
        assert bad == 0
        bad2 = con.execute(
            "select count(*) from diseases where species in ('dog','cat','horse','bird','parakeet') "
            "and clinical_signs_ja like '%UV-B不足（爬虫類）%'"
        ).fetchone()[0]
        assert bad2 == 0


class TestMasitinibPalladiaIdFix:
    def test_palladia_resolves_to_toceranib_not_masitinib(self):
        from api.drug_dictionary import resolve_drug_reference as r

        assert r("Palladia") == "toceranib"
        assert r("palladia") == "toceranib"
        assert r("Kinavet") == "masitinib" and r("マシチニブ") == "masitinib"

    def test_masitinib_monograph_warns_against_confusion(self):
        from api.drug_dictionary import DRUGS

        d = next(x for x in DRUGS if x["id"] == "masitinib")
        assert "palladia" not in {x["id"] for x in DRUGS}
        dog = d["species_info"]["dog"]
        assert "toceranib" in dog["notes"].lower() and "トセラニブ" in dog["notes_ja"]
        assert "UPC" in dog["notes"] and "Hahn 2008" in dog["notes"]

    def test_gilvetmab_oncology_list_uses_real_ids(self):
        from api.drug_dictionary import DRUGS
        from api.drug_interactions import GILVETMAB_UNSTUDIED_ONCOLOGY_IDS

        ids = {x["id"] for x in DRUGS}
        assert "masitinib" in GILVETMAB_UNSTUDIED_ONCOLOGY_IDS
        assert set(GILVETMAB_UNSTUDIED_ONCOLOGY_IDS) <= ids


class TestLeishmaniasisAndDeltamethrin:
    def _records(self):
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        return {(r.get("species"), r.get("name")): r for r in data}

    def test_prevention_names_the_sand_fly_vector(self):
        recs = self._records()
        for key in [("Dog", "Leishmaniasis"), ("Dog", "Leishmaniosis"), ("Cat", "Feline Leishmaniasis")]:
            r = recs[key]
            assert "サシチョウバエ" in r["prevention_ja"] and "sand fl" in r["prevention"]
            assert "フィラリア）: 流行地" not in r["prevention_ja"]
        cat = recs[("Cat", "Feline Leishmaniasis")]
        assert "有毒" in cat["prevention_ja"] and "フルメトリン" in cat["prevention_ja"]

    def test_deltamethrin_collar_monograph(self):
        from api.drug_dictionary import DRUGS, find_drugs_in_text, resolve_drug_reference

        d = next(x for x in DRUGS if x["id"] == "deltamethrin_collar")
        assert d["species_info"]["dog"]["safe"] is True and d["species_info"]["cat"]["safe"] is False
        assert "Maroli" in d["species_info"]["dog"]["notes"]
        assert resolve_drug_reference("スカリボール") == "deltamethrin_collar"
        recs = self._records()
        tx = recs[("Dog", "Leishmaniasis")]["treatment_ja"]
        assert "deltamethrin_collar" in {x["id"] for x in find_drugs_in_text(tx)}
        assert tx.count("デルタメトリン首輪") == 1


class TestChatClinicalAccuracyAuditRound51:
    def test_polite_hair_loss_and_cushing_triad(self):
        from api.chat.symptom_extractor import normalize_chat_text

        assert normalize_chat_text("毛が抜けます") == "毛が抜ける"
        ids, top = _dog("よく食べるのにお腹がふくれて毛が抜けます")
        assert {"increased_appetite", "bloating", "hair_loss"} <= ids
        assert "クッシング" in top[0], top

    def test_bloating_diarrhea_does_not_trigger_cushing(self):
        _, top = _dog("お腹がふくれて下痢をしています")
        assert "クッシング" not in top[0]

    def test_tail_base_pain_and_tangled_gait(self):
        ids, top = _dog("しっぽを振らなくなり、しっぽの付け根を触ると痛がります")
        assert "back_pain" in ids and "pain" not in ids and "椎間板" in top[0], top
        ids, top = _dog("左右の後ろ足がもつれるように歩きます")
        assert "ataxia" in ids and any("脊髄" in t or "椎間板" in t for t in top), top

    def test_fever_phrases_reach_impa(self):
        ids, top = _dog("高熱が出て関節が腫れて歩きたがりません")
        assert "fever" in ids and "多発性関節炎" in top[0], top

    def test_senior_cat_weight_loss_poor_coat(self):
        ids, top = _sp("高齢で痩せてきて毛艶が悪くなりました", "cat")
        assert {"weight_loss", "poor_coat"} <= ids and top[0] in ("慢性腎臓病", "甲状腺機能亢進症"), top

    def test_cat_red_eye_and_chin_acne(self):
        ids, top = _sp("目が真っ赤で涙が止まりません", "cat")
        assert "conjunctivitis" in ids or "redness_in_eyes" in ids, ids
        ids, top = _sp("顎の下に黒いブツブツがあります", "cat")
        assert "chin_swelling" in ids and "にきび" in top[0], top

    def test_sugar_glider_hind_paralysis_is_mbd(self):
        ids, top = _sp("後ろ足が麻痺して動きません", "sugar_glider")
        assert "hind_leg_paralysis" in ids and "代謝性骨疾患" in top[0], top

    def test_hamster_wet_tail_and_snake_mites(self):
        ids, top = _sp("しっぽのまわりが濡れてぐったりしています", "hamster")
        assert "wet_tail" in ids and "ウェットテイル" in top[0], top
        ids, top = _sp("体にダニがついていて水入れに浸かってばかり", "snake")
        assert {"visible_mites", "excessive_soaking"} <= ids and "ダニ" in top[0], top


def test_disease_jump_bar_has_prevention_chip():
    assert 'data-jump="prevention"' in APP_JS
    assert 'prevention:["🛡️ 予防","🛡️ Prevention"]' in APP_JS
    assert '"prognosis","prevention"' in APP_JS


def test_drug_deep_link_falls_back_to_server_alias_resolution():
    i = APP_JS.index("function _handleDeepLinkHash")
    body = APP_JS[i : i + 2500]
    assert "/api/drugs/${encodeURIComponent(link.id)}" in body
    assert "(x.aliases||[])" in body


def test_sw_cache_bumped():
    sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
    import re

    assert int(re.search(r"vetdict-v(\d+)", sw).group(1)) >= 190
