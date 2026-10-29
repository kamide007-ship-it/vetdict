"""2026-10 第82弾: チャット精度第57回（排尿後の怒責・扁平便→前立腺/会陰ヘルニア・
足先を擦る固有位置感覚障害・粘液便・涙やけ・頸部痛姿勢・吐出・猫の鼻梁痂皮/無尿・
ウサギ耳痂皮/尿砂・卵塞/脱皮不全のず形）、ピモベンダン注射液（ベトメディン注射液）、
チャット回答の薬品リンク→相談中の動物種の用量カード着地。"""

import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _horse, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound57:
    def test_post_void_straining_is_lower_urinary(self):
        ids, top = _dog("おしっこをした後もずっといきんでいます", 3)
        assert "straining_to_urinate" in ids, ids
        assert any(("尿" in t) or ("膀胱" in t) or ("前立腺" in t) for t in top), top

    def test_dysuria_plus_flat_stool_is_prostate(self):
        ids, top = _dog("おしっこが出にくそうで便も平べったい")
        assert {"straining_to_urinate", "flat_stool"} <= ids, ids
        assert top[0] == "良性前立腺肥大症", top

    def test_bare_dysuria_not_hijacked_by_prostate(self):
        _, top = _dog("おしっこが出にくそうです")
        assert top[0] != "良性前立腺肥大症", top

    def test_constipation_lands_on_perineal_hernia(self):
        _, top = _dog("便秘しています")
        assert top and top[0] == "会陰ヘルニア", top

    def test_perineal_hernia_name_mirrors_dog_module(self):
        from api.health_checker import DISEASES
        from api.species.dog_diseases import DISEASES as DOG

        legacy = next(d for d in DISEASES if d["id"] == "perineal_hernia")
        assert any(d["name"] == legacy["name_en"] for d in DOG)

    def test_toe_scuffing_is_proprioceptive_ataxia(self):
        ids, top = _dog("後ろ足の爪をこすって歩きます")
        assert "ataxia" in ids, ids
        assert any(("椎間板" in t) or ("脊髄" in t) for t in top), top

    def test_mucoid_stool_tear_staining_neck_pain(self):
        ids, _ = _dog("便にゼリー状のものがついています")
        assert "diarrhea" in ids
        ids, _ = _dog("目の下が涙で茶色く汚れています")
        assert "eye_discharge" in ids
        ids, top = _dog("歩くと首を下げて痛がります")
        assert "neck_pain" in ids and "緑内障" not in top, (ids, top)

    def test_regurgitation_after_drinking_is_megaesophagus(self):
        ids, top = _dog("水を飲んだ後に吐きます 体重が減っています", 3)
        assert "regurgitation" in ids
        assert any("食道" in t for t in top), top

    def test_cat_nasal_crust_and_anuria(self):
        ids, top = _sp("鼻の上にかさぶたがあって治りません", "cat")
        assert "non_healing_wound" in ids, ids
        ids, top = _sp("トイレに入っては何も出ずに出てきます", "cat")
        assert "decreased_urination" in ids
        assert any("尿道" in t for t in top), top

    def test_rabbit_ear_crust_and_urine_sand(self):
        ids, top = _sp("耳の中に茶色いかさぶたがあります", "rabbit")
        assert "ear_crusting" in ids, ids
        ids, top = _sp("おしっこにざらざらした砂が混じります", "rabbit")
        assert "thick_white_urine" in ids, ids

    def test_zu_form_egg_binding_and_dysecdysis(self):
        ids, top = _sp("お尻から卵が出てこずいきんでいます", "bird")
        assert "egg_binding" in ids and any("卵" in t for t in top), (ids, top)
        ids, top = _sp("脱皮がうまくいかず指に残っています", "lizard")
        assert "dysecdysis" in ids and any("脱皮" in t for t in top), (ids, top)

    def test_snake_many_mites(self):
        ids, top = _sp("ダニがたくさんついています", "snake")
        assert ids and any("ダニ" in t for t in top), (ids, top)

    def test_horse_limb_swelling_drops_generic_body_swelling(self):
        ids, top = _horse("左後肢が腫れて熱を持っています", 5)
        assert "body_swelling" not in ids and "limb_filling" in ids, ids
        assert "肥満細胞腫" not in top, top


class TestBatch90PimobendanInjection:
    def test_monograph(self):
        from api.drug_dictionary import _drug_index

        d = _drug_index["pimobendan_injection"]
        dog = d["species_info"]["dog"]
        assert "0.15 mg/kg" in dog["dosage"] and "12 hours" in dog["dosage"]
        assert "1回のみ" in dog["dosage_ja"] and "0.2 mL/kg" in dog["dosage"]
        assert d["species_info"]["cat"]["safe"] is False
        assert "日本" in dog["notes_ja"]

    def test_resolution_keeps_oral_brand(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        assert resolve_drug_reference("ベトメディン") == "pimobendan"
        assert resolve_drug_reference("ベトメディン注射液") == "pimobendan_injection"
        oral = [d["id"] for d in find_drugs_in_text("ピモベンダン 0.25 mg/kg PO q12h")]
        assert oral == ["pimobendan"], oral
        iv = [d["id"] for d in find_drugs_in_text("furosemide 2-4 mg/kg IV bolus + pimobendan IV")]
        assert "pimobendan_injection" in iv

    def test_dog_chf_protocol_mentions_injection(self):
        import json

        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        e = next(x for x in data if x["species"] == "Dog" and x["name"] == "Heart Disease/CHF")
        assert "ベトメディン注射液" in e["treatment_ja"] and "0.15 mg/kg" in e["treatment"]


class TestChatDrugLinkLandsOnChatSpeciesDose:
    def test_wired(self):
        assert 'data-sp="${escapeHtml(sp)}"' in APP_JS
        assert "landDose:true,species:chatSp" in APP_JS
        assert "function _landOnSpeciesDose(item,tries,sp)" in APP_JS
