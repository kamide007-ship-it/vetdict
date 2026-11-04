"""2026-11 第83弾: チャット精度第58回（足底出血・歯肉腫脹・後肢ガクガク・黄疸「目の色が」形・
雄猫のトイレ内反復怒責・「ダニがいる」・直腸脱（チャットDB新設）・寒がり＋体重増加→甲状腺
機能低下・卵が出てきません・鼻孔の泡沫・馬「咳が運動時に」・猫口内炎の包含とバルトネラtier・
高齢猫の嘔吐＋体重減少の年齢ゲート付きブースト）、猫のアチパメゾール容量の是正（犬の同容量則
は猫では過量）、表記ゆれエイリアスの薬品検索への反映。"""

import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _horse, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound58:
    def test_dog_foot_bleeding_and_gum_swelling(self):
        ids, _ = _dog("足の裏から血が出ています")
        assert ids, ids
        ids, top = _dog("歯ぐきが腫れて口から血が出ます")
        assert any("歯周" in t or "口腔" in t for t in top), (ids, top)

    def test_dog_hind_leg_wobble_is_orthopedic_or_spinal_not_seizure(self):
        ids, top = _dog("後ろ足がガクガクして階段が上れません")
        assert "tremors" not in ids, ids
        assert top[0] != "てんかん", top

    def test_jaundice_eye_colour_form(self):
        ids, _ = _dog("目の色が黄色っぽいです")
        assert ids, ids

    def test_dog_rectal_prolapse_entry(self):
        ids, top = _dog("おしりから赤いものが出ています")
        assert "rectal_prolapse" in ids and top[0] == "直腸脱", (ids, top)
        _, top = _dog("下痢をしています")
        assert "直腸脱" not in top, top

    def test_rectal_prolapse_name_mirrors_dog_module(self):
        from api.health_checker import DISEASES
        from api.species.dog_diseases import DISEASES as DOG

        legacy = next(d for d in DISEASES if d["id"] == "rectal_prolapse")
        assert any(d["name"] == legacy["name_en"] for d in DOG)

    def test_cold_intolerance_weight_gain_is_hypothyroid(self):
        _, top = _dog("眠ってばかりで寒がります 太りました")
        assert top[0] == "甲状腺機能低下症", top

    def test_male_cat_repeated_litterbox_straining_is_urinary(self):
        ids, top = _sp("トイレで何度もいきんでいます オスです", "cat", 5)
        assert "straining_to_urinate" in ids, ids
        assert any("尿" in t for t in top[:3]), top

    def test_snake_mites_present_form(self):
        ids, top = _sp("体にダニがいます", "snake")
        assert "visible_mites" in ids and any("ダニ" in t for t in top), (ids, top)

    def test_bird_egg_not_coming_out_polite(self):
        ids, top = _sp("卵が出てきません", "bird")
        assert "egg_binding" in ids and "卵" in top[0], (ids, top)

    def test_tortoise_nasal_froth_is_respiratory_not_vomiting(self):
        ids, _ = _sp("鼻から泡が出ています", "tortoise")
        assert "nasal_discharge" in ids and "regurgitation" not in ids, ids

    def test_cat_stomatitis_subsumes_generic_swelling(self):
        ids, top = _sp("口の中が赤く腫れて痛がります", "cat")
        assert ids == {"stomatitis"}, ids
        assert top[0] == "猫慢性歯肉口内炎", top

    def test_horse_cough_word_order(self):
        ids, top = _horse("咳が運動時に出ます")
        assert "resp_cough_at_exercise" in ids, ids
        assert any("喘息" in t or "IAD" in t for t in top), top

    def test_senior_cat_vomiting_weight_loss_age_gated(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases as m

        senior = [x["name_ja"] for x in m(["vomiting", "weight_loss"], "cat", lang="ja", age_category="senior")[:3]]
        young = [x["name_ja"] for x in m(["vomiting", "weight_loss"], "cat", lang="ja")[:3]]
        assert "甲状腺機能亢進症" in senior, senior
        assert "甲状腺機能亢進症" not in young, young

    def test_free_chat_passes_senior_age_for_cats(self):
        import os

        os.environ.setdefault("SECRET_KEY", "test")
        from api.vetdict_api import app

        r = app.test_client().post(
            "/api/diagnostic-chat/chat",
            json={"message": "吐く回数が増えて痩せてきました 高齢です", "species": "cat", "lang": "ja"},
        )
        names = [c.get("name_ja") for c in r.get_json()["disease_candidates"][:3]]
        assert "甲状腺機能亢進症" in names, names


class TestFelineAtipamezoleVolume:
    def test_drug_dictionary_cat_half_volume(self):
        from api.drug_dictionary import DRUGS

        d = next(x for x in DRUGS if x["id"] == "atipamezole")
        cat = d["species_info"]["cat"]
        assert "Half the volume" in cat["dosage"] and "半量" in cat["dosage_ja"], cat
        assert "Same volume" in d["species_info"]["dog"]["dosage"]

    def test_anesthesia_cat_protocols_no_equal_volume_rule(self):
        from api.anesthesia_protocols import ANESTHESIA_PROTOCOLS as P

        blob = str(P["cat"])
        assert "atipamezole equal volume" not in blob
        assert "アティパメゾール同容量" not in blob
        assert "Same volume as dexmedetomidine'" not in blob
        assert "half the volume" in blob.lower()
        # 犬は承認用法どおり同容量のまま
        assert "equal volume" in str(P["dog"])


class TestVariantAliasesReachDrugSearch:
    def test_atipamezole_ti_variant_in_search_aliases(self):
        from api.drug_dictionary import DRUGS

        d = next(x for x in DRUGS if x["id"] == "atipamezole")
        assert "アティパメゾール" in d["search_aliases"]

    def test_client_search_folds_loanword_orthography(self):
        i = APP_JS.index("function normalizeDrugSearchText")
        body = APP_JS[i : i + 900]
        assert '.replace(/ティ/g,"チ")' in body and '.replace(/ヴ/g,"ブ")' in body

    def test_sw_cache_bumped(self):
        sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
        assert "vetdict-v198" in sw
