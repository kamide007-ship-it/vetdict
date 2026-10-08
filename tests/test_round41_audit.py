"""2026-10 第65弾: 種非依存の用量テンプレート是正・新規承認薬2剤・チャット精度第41弾・
長文回答の先頭着地（スマホUX）。"""

import json
import re
import sqlite3
import warnings
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
warnings.filterwarnings("ignore")


def _json():
    return json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))


class TestSpeciesDoseTemplates:
    OLD_MELOX = "（小型哺乳類）または0.1-0.2 mg/kg q24h（馬は1.7 mg/kg q24h）"
    OLD_SHOCK = "ショック時 90 mL/kg初期ボーラス"

    def test_no_cross_species_meloxicam_or_shock_template_in_json(self):
        for x in _json():
            for fld in ("treatment_ja", "treatment"):
                t = x.get(fld) or ""
                assert self.OLD_MELOX not in t, (x["species"], x["name"])
                assert self.OLD_SHOCK not in t, (x["species"], x["name"])

    def test_no_template_in_species_modules_or_generators(self):
        for f in list((ROOT / "api" / "species").glob("*_diseases.py")) + list(
            (ROOT / "scripts" / "template_elimination").glob("*.py")
        ):
            if f.name == "fix_species_dose_templates.py":
                continue
            src = f.read_text(encoding="utf-8")
            assert self.OLD_MELOX not in src, f.name
            assert self.OLD_SHOCK not in src, f.name

    def test_non_small_mammals_have_no_small_mammal_en_template(self):
        bad = {
            "Cat",
            "Dog",
            "Horse",
            "Bird",
            "Parrot",
            "Parakeet",
            "Reptile",
            "Lizard",
            "Snake",
            "Tortoise",
            "Amphibian",
        }
        for x in _json():
            if x["species"] in bad:
                assert not (x.get("treatment") or "").startswith("【Small Mammal"), (x["species"], x["name"])

    def test_cat_meloxicam_doses_are_feline(self):
        for x in _json():
            if x["species"] != "Cat":
                continue
            t = (x.get("treatment") or "") + (x.get("treatment_ja") or "")
            assert not re.search(r"(?i)meloxicam 0\.2-0\.5|メロキシカム 0\.2-0\.5", t), x["name"]

    def test_cat_oa_is_curated_and_lists_portela(self):
        x = next(d for d in _json() if d["species"] == "Cat" and d["name"].startswith("Osteoarthritis"))
        assert "安静期間 4-8週" not in x["treatment_ja"]
        assert "フルネベトマブ" in x["treatment_ja"] and "ポルテラ" in x["treatment_ja"]
        assert "Portela" in x["treatment"]

    def test_generator_is_species_aware(self):
        from scripts.template_elimination.fallback_generator import meloxicam_line_ja
        from scripts.template_elimination.template_content_library import SHOCK_FLUID_JA

        assert "0.01-0.03" in meloxicam_line_ja("cat")
        assert "0.6 mg/kg" in meloxicam_line_ja("horse")
        assert "1.0-1.6" in meloxicam_line_ja("parrot")
        assert "5-10 mL/kg" in SHOCK_FLUID_JA["cat"] and "10-20 mL/kg" in SHOCK_FLUID_JA["dog"]

    def test_served_db_cat_oa_not_templated(self):
        db = ROOT / "instance" / "vetdict.db"
        if not db.exists() or db.stat().st_size < 1_000_000:
            pytest.skip("served DB not built")
        con = sqlite3.connect(db)
        rows = con.execute(
            "select treatment, treatment_ja from diseases where species='cat' and name like 'Osteoarthritis%'"
        ).fetchall()
        assert rows
        for en, ja in rows:
            assert not (en or "").startswith("【Small Mammal")
            assert self.OLD_MELOX not in (ja or "")


class TestBatch73NewDrugs:
    def test_entries_and_safety_gates(self):
        from api.drug_dictionary import _drug_index as d

        a, r = d["atinvicitinib"], d["relfovetmab"]
        assert "0.8-1.2 mg/kg" in a["species_info"]["dog"]["dosage"]
        assert "q24h" in a["species_info"]["dog"]["dosage_ja"]
        assert a["species_info"]["cat"]["safe"] is False
        assert "3" in r["species_info"]["cat"]["dosage"] and "12 months" in r["species_info"]["cat"]["dosage"]
        assert r["species_info"]["dog"]["safe"] is False
        assert "国内未承認" in a["species_info"]["dog"]["notes_ja"]

    def test_matcher_resolver_and_interactions(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference
        from api.drug_interactions import find_interactions

        ids = [x["id"] if isinstance(x, dict) else x for x in find_drugs_in_text("ヌメルビ 0.8-1.2 mg/kg、ポルテラ SC")]
        assert "atinvicitinib" in ids and "relfovetmab" in ids
        assert resolve_drug_reference("ぬめるび") == "atinvicitinib"
        sev = {
            (i["drug_a"], i["drug_b"]): i["severity"]
            for i in find_interactions(["atinvicitinib", "oclacitinib", "gilvetmab"])
        }
        assert sev.get(("atinvicitinib", "oclacitinib")) == "major"
        assert sev.get(("gilvetmab", "atinvicitinib")) == "major"
        sev2 = {(i["drug_a"], i["drug_b"]): i["severity"] for i in find_interactions(["relfovetmab", "frunevetmab"])}
        assert sev2.get(("relfovetmab", "frunevetmab")) == "major"

    def test_disease_treatments_link_new_drugs(self):
        from api.drug_dictionary import find_drugs_in_text

        data = _json()
        dad = next(x for x in data if x["species"] == "Dog" and x["name"] == "Canine Atopic Dermatitis")
        ids = [x["id"] if isinstance(x, dict) else x for x in find_drugs_in_text(dad["treatment_ja"])]
        assert "atinvicitinib" in ids


class TestChatClinicalAccuracyAuditRound41:
    @staticmethod
    def _sp(phrase, species, n=5):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms(phrase, species)
        res = _match_species_symptoms_to_diseases(list(ids), species, lang="ja")
        return set(ids), [r.get("name_ja") or "" for r in res[:n]]

    @staticmethod
    def _dog(phrase, n=4):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ids = extract_symptoms_from_text(phrase)
        return set(ids), [r.get("name_ja") or "" for r in match_symptoms_to_diseases(ids)[:n]]

    def test_dog_gdv_attempted_retching(self):
        ids, top = self._dog("夜中に何度も吐こうとしてお腹がふくれています")
        assert "unproductive_retching" in ids
        assert any("胃拡張" in t for t in top[:2]), top

    def test_dog_red_eye_discharge_conjunctivitis_first(self):
        _, top = self._dog("目が赤くて目やにがたくさん出ます")
        assert "結膜炎" in top[0], top

    def test_dog_scooting_on_floor(self):
        ids, top = self._dog("お尻を床にこすりつけて歩きます")
        assert "scooting" in ids and any("肛門嚢" in t for t in top[:2]), top

    def test_dog_painful_red_eye(self):
        ids, _ = self._dog("片目だけ急に充血して痛そうに目を閉じています")
        assert {"redness_in_eyes", "squinting"} <= ids

    def test_cat_overgrooming_and_constipation(self):
        ids, _ = self._sp("毛をなめすぎてお腹の毛がなくなりました", "cat")
        assert {"excessive_grooming", "hair_loss"} <= ids
        ids, top = self._sp("うんちが何日も出ていません", "cat")
        assert "constipation" in ids and any("便秘" in t or "巨大結腸" in t for t in top[:3]), top

    def test_duration_adverb_strip(self):
        from api.chat.symptom_extractor import normalize_chat_text as n

        assert n("便が何日も出ていない") == "便が出ていない"
        assert n("咳が数日続いている") == "咳が続いている"

    def test_cat_acne_and_stud_tail(self):
        _, top = self._sp("下顎に黒いぶつぶつがあります", "cat")
        assert any("にきび" in t for t in top[:2]), top
        ids, _ = self._sp("しっぽの付け根がべたべたしています", "cat")
        assert "greasy_coat" in ids

    def test_ferret_tarry_stool(self):
        ids, top = self._sp("黒いタール状の便が出ます", "ferret")
        assert ids & {"black_tarry_stool", "tarry_stool"}
        assert any("潰瘍" in t or "ヘリコバクター" in t for t in top[:3]), top

    def test_bird_crop_and_gout(self):
        ids, top = self._sp("そのうが腫れて吐き戻しています", "bird")
        assert "crop_distension" in ids and any("そのう" in t or "嗉嚢" in t for t in top[:3]), top
        _, top = self._sp("足に白い塊ができて腫れています", "bird")
        assert any("痛風" in t for t in top[:3]), top

    def test_rabbit_walking_dandruff(self):
        _, top = self._sp("毛がフケっぽくて背中がかゆそうです", "rabbit")
        assert any("ツメダニ" in t for t in top[:4]), top

    def test_horse_hind_drag_not_forelimb(self):
        from api.diagnostic_chat import _extract_equine_symptoms

        ids = set(_extract_equine_symptoms("後ろ足を引きずって腫れています"))
        assert "limb_lameness_hind" in ids and "limb_lameness_fore" not in ids
        assert "limb_lameness_fore" in set(_extract_equine_symptoms("足を引きずっています"))


def test_app_js_long_answers_land_on_answer_top():
    js = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
    assert "function _revealChatMsg(container,el)" in js
    assert "_revealChatMsg(container,wrapper);" in js
    assert "_revealChatMsg(msgs,div)" in js
    assert "last.dataset.revealedTop" in js
    # タッチ端末では回答後に入力欄へ再フォーカスしない（キーボードが回答を覆う）
    assert "if(!_isTouchUI())input.focus();" in js
    css = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    assert ".chat-container{height:calc(100dvh - 240px);min-height:320px;max-height:680px}" in css
