"""2026-10 第66弾: 種キーワード誤検出の是正・チャット精度第42弾・新規承認薬3剤。"""

import re
import warnings
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
warnings.filterwarnings("ignore")


class TestSpeciesDetectionFalsePositives:
    @pytest.mark.parametrize(
        "text",
        [
            "皮膚がベタベタして臭いです",
            "脱皮がうまくいきません",
            "肉球に亀裂があります",
            "蛇行して歩きます",
            "馬尾症候群が疑われます",
            "狂犬病ワクチンの後に元気がない",
            "焼き鳥の串を食べてしまった",
            "うまれつき心雑音がある",
        ],
    )
    def test_symptom_words_do_not_switch_species(self, text):
        from api.chat.constants import detect_species_from_text

        assert detect_species_from_text(text) is None

    @pytest.mark.parametrize(
        "text,species",
        [("猫 皮膚がベタベタ", "cat"), ("ベタが尾ぐされ", "fish"), ("ウマ 疝痛", "horse"), ("馬が転がる", "horse")],
    )
    def test_explicit_species_still_detected(self, text, species):
        from api.chat.constants import detect_species_from_text

        assert detect_species_from_text(text) == species

    def test_quick_tap_phrases_never_switch_species(self):
        from api.chat.constants import detect_species_from_text

        src = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
        i = src.index('const quickSymptoms=currentLang==="ja"?{')
        block = src[i : src.index("}:{", i)]
        for m in re.finditer(r"(\w+):\[([^\]]*)\]", block):
            for phrase in re.findall(r'"([^"]+)"', m.group(2)):
                found = detect_species_from_text(phrase)
                assert found in (None, m.group(1)), (m.group(1), phrase, found)

    def test_chat_endpoint_keeps_selected_species(self):
        from api.vetdict_api import app

        r = app.test_client().post(
            "/api/diagnostic-chat/chat", json={"message": "皮膚がベタベタして臭いです", "species": "dog"}
        )
        assert r.status_code == 200
        assert r.get_json()["species"] == "dog"

    def test_app_js_notes_species_switch(self):
        src = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
        assert "function _noteChatSpeciesSwitch(" in src
        assert src.count("_noteChatSpeciesSwitch(species,data") == 2


class TestChatClinicalAccuracyAuditRound42:
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

    def test_dog_malassezia_greasy_skin(self):
        ids, top = self._dog("皮膚がベタベタして臭いです")
        assert "greasy_skin" in ids and top[0] == "マラセチア皮膚炎", top

    def test_dog_itching_alone_not_hijacked_by_malassezia(self):
        _, top = self._dog("体をかゆがって毛が抜けます")
        assert "マラセチア皮膚炎" not in top

    def test_bare_blood_follows_body_site(self):
        ids, top = self._dog("下痢が続いて血が混じっています")
        assert "blood_in_stool" in ids and "blood_in_urine" not in ids
        assert not any("膀胱炎" in t for t in top[:2]), top
        ids, _ = self._dog("吐いたものに血が混じっています")
        assert "blood_in_urine" not in ids and "vomiting" in ids
        ids, _ = self._dog("おしっこに血が混じっています")
        assert "blood_in_urine" in ids
        ids, top = self._sp("鼻水に血が混じります", "cat")
        assert not ids & {"bloody_urine", "blood_in_urine"}, ids

    def test_dog_nocturia_and_circling(self):
        ids, _ = self._dog("夜中に何度もおしっこに起きます")
        assert "frequent_urination" in ids
        ids, _ = self._dog("歩くとふらふらして同じところを回ります")
        assert "circling" in ids

    def test_cat_weight_loss_restlessness_hyperthyroid(self):
        _, top = self._sp("急に痩せてきて落ち着きがありません", "cat")
        assert any("甲状腺機能亢進" in t for t in top[:3]), top

    def test_snake_polite_dysecdysis(self):
        ids, top = self._sp("脱皮がうまくいきません", "snake")
        assert "dysecdysis" in ids and top[0] == "脱皮不全", top

    def test_parakeet_bumpy_beak_mites(self):
        _, top = self._sp("くちばしの周りがボコボコしています", "parakeet")
        assert "疥癬" in top[0], top

    def test_bird_crop_swollen(self):
        ids, top = self._sp("そのうが膨れて吐き戻します", "bird")
        assert "crop_distension" in ids and any("嗉嚢" in t or "素嚢" in t for t in top[:2]), top

    def test_cat_straining_to_defecate(self):
        ids, _ = self._sp("トイレでうんちをしようといきむが出ません", "cat")
        assert ids & {"constipation", "straining_to_defecate"}

    def test_horse_hot_hoof_reluctant_to_walk(self):
        from api.diagnostic_chat import _extract_equine_symptoms, _match_equine_symptoms_to_diseases

        ids = _extract_equine_symptoms("蹄が熱くて歩きたがりません")
        top = [r.get("name_ja") for r in _match_equine_symptoms_to_diseases(ids)[:2]]
        assert set(top) == {"蹄膿瘍", "急性蹄葉炎"}, top
        top1 = [r.get("name_ja") for r in _match_equine_symptoms_to_diseases(["hoof_heat"])[:3]]
        assert "蹄膿瘍" in top1 and "急性蹄葉炎" in top1, top1

    def test_horse_strangles_submandibular_swelling(self):
        from api.diagnostic_chat import _extract_equine_symptoms, _match_equine_symptoms_to_diseases

        ids = _extract_equine_symptoms("鼻から黄色い鼻水が出て下顎が腫れています")
        assert "gen_swollen_lymph" in ids
        top = [r.get("name_ja") for r in _match_equine_symptoms_to_diseases(ids)[:3]]
        assert "腺疫" in top, top

    def test_legacy_malassezia_name_matches_dog_module(self):
        from api.health_checker import DISEASES
        from api.species import dog_diseases

        legacy = next(d for d in DISEASES if d["id"] == "malassezia_dermatitis")
        names = {(d.get("name") if isinstance(d, dict) else d.name) for d in dog_diseases.DISEASES}
        assert legacy["name_en"] in names


class TestBatch74:
    def _d(self, did):
        from api.drug_dictionary import DRUGS

        return next(x for x in DRUGS if x["id"] == did)

    def test_nocita_label_doses_and_route_limits(self):
        d = self._d("bupivacaine_liposomal")
        assert "5.3 mg/kg" in d["species_info"]["dog"]["dosage"] and "0.4 mL/kg" in d["species_info"]["dog"]["dosage"]
        assert "10.6 mg/kg" in d["species_info"]["cat"]["dosage"]
        assert "intrathecal" in d["contraindications"] and "5 months" in d["contraindications"]
        assert any(i["severity"] == "major" and "Lidocaine" in i["drug"] for i in d["drug_interactions"])

    def test_zorbium_unit_doses_and_dog_gate(self):
        d = self._d("buprenorphine_transdermal")
        cat = d["species_info"]["cat"]
        for frag in ("8 mg (0.4 mL)", "20 mg (1 mL)", "1-2 h before surgery"):
            assert frag in cat["dosage"], frag
        assert "高体温" in cat["notes_ja"]
        assert d["species_info"]["dog"]["safe"] is False

    def test_verdinexor_label_and_honest_framing(self):
        d = self._d("verdinexor")
        dog = d["species_info"]["dog"]
        assert "1.25 mg/kg" in dog["dosage"] and "1.5 mg/kg" in dog["dosage"] and "72 h" in dog["dosage"]
        assert "CHOPの代替ではない" in dog["notes_ja"]
        assert d["species_info"]["cat"]["safe"] is False

    def test_matcher_checker_and_disease_links(self):
        import json

        from api.drug_dictionary import find_drugs_in_text
        from api.drug_interactions import find_interactions

        assert "verdinexor" in [x["id"] for x in find_drugs_in_text("ベルジネクソル（ラバーディア）")]
        assert "buprenorphine_transdermal" in [x["id"] for x in find_drugs_in_text("ゾルビウム")]
        assert find_interactions(["gilvetmab", "verdinexor"])
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        dog = {x["name"]: x for x in data if x["species"] == "Dog"}
        ccl = dog["Cranial Cruciate Ligament Rupture"]
        lym = dog["Lymphoma"]
        assert "bupivacaine_liposomal" in [x["id"] for x in find_drugs_in_text(ccl["treatment_ja"])]
        assert "verdinexor" in [x["id"] for x in find_drugs_in_text(lym["treatment_ja"])]
        assert "Nocita" in ccl["treatment"] and "verdinexor" in lym["treatment"]
