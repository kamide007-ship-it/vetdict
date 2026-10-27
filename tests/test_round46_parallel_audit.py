"""2026-10 第71弾: チャット精度第46回・MMVDオーバーレイ是正・猫ATE文の異種混入撲滅・
専門医紹介行の是正・Japanese-only English treatment の検証済み英訳・アピキサバン/
クレデリオプラス公開・疾患詳細のセクション・ジャンプバー。"""

import json
import re
import sqlite3
import warnings
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "instance" / "vetdict.db"
JSON = ROOT / "diseases_all_species.json"
warnings.filterwarnings("ignore")
CJK = re.compile(r"[぀-ヿ一-鿿]")


def _sp(phrase, species, n=5):
    from api.chat.disease_matcher import _match_species_symptoms_to_diseases
    from api.chat.symptom_extractor import _extract_species_symptoms

    ids = _extract_species_symptoms(phrase, species)
    res = _match_species_symptoms_to_diseases(list(ids), species, lang="ja")
    return set(ids), [r.get("name_ja") or "" for r in res[:n]]


def _dog(phrase, n=4):
    from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

    ids = extract_symptoms_from_text(phrase)
    return set(ids), [r.get("name_ja") or "" for r in match_symptoms_to_diseases(ids)[:n]]


def _ja_heavy(text):
    return bool(text) and len(CJK.findall(text)) > len(text) * 0.3


class TestChatClinicalAccuracyAuditRound46Parallel:
    def test_bare_swollen_is_not_bloating(self):
        from api.chat.symptom_aliases import SYMPTOM_ALIASES

        assert SYMPTOM_ALIASES["腫れてる"] == "swelling"
        ids, _ = _dog("リンパ節が腫れてる 熱がある")
        assert "swollen_lymph_nodes" in ids and "bloating" not in ids

    def test_dog_neck_lump_fever_reaches_lymphoma(self):
        ids, top = _dog("首に大きなしこりがあって熱があります", 5)
        assert "swollen_lymph_nodes" in ids and any("リンパ腫" in t for t in top), top

    def test_dog_whitish_eye(self):
        ids, top = _dog("目の色が白っぽくなってきました")
        assert ids and any("白内障" in t for t in top), top

    def test_dog_perianal_swelling_anal_sac(self):
        ids, top = _dog("お尻のまわりが腫れて痛がります")
        assert "scooting" in ids and "肛門嚢" in top[0], top

    def test_dog_stark_white_gums(self):
        ids, top = _dog("急に元気がなくなって歯茎が真っ白です", 5)
        assert "pale_gums" in ids and any(k in " ".join(top) for k in ("血管肉腫", "溶血", "貧血")), top

    def test_dog_otitis_beats_aural_hematoma_without_swelling(self):
        _, top = _dog("耳が痒い 頭を振る", 1)
        assert "外耳炎" in top[0], top

    def test_cat_ate_screaming(self):
        _, top = _sp("後ろ足を引きずって急に鳴き叫びました", "cat", 3)
        assert any("血栓" in t for t in top), top

    def test_reptile_mouth_swelling_is_mouth_rot(self):
        ids, top = _sp("口が腫れてチーズのようなものが出ています", "reptile", 2)
        assert "stomatitis" in ids and any("口内炎" in t for t in top), top

    def test_guinea_pig_mange_seizures(self):
        _, top = _sp("毛が抜けてかゆがってひきつけを起こします", "guinea_pig", 2)
        assert any("疥癬" in t or "Trixacarus" in t for t in top), top


class TestMMVDOverlay:
    def test_json_mmvd_has_no_template(self):
        data = json.loads(JSON.read_text(encoding="utf-8"))
        d = next(x for x in data if x["species"] == "Dog" and x["name"] == "Mitral Valve Disease (MMVD)")
        for f in (
            "treatment_ja",
            "prognosis_ja",
            "causes_ja",
            "clinical_signs_ja",
            "diagnosis_ja",
            "pathophysiology_ja",
        ):
            assert "系統的アプローチにより" not in d[f], f
        assert "ピモベンダン" in d["treatment_ja"] and "EPIC" in d["treatment_ja"]
        assert "LA/Ao" in d["diagnosis_ja"]
        assert "In cats" not in d["clinical_signs"]

    def test_served_db_mmvd(self):
        if not DB.exists():
            pytest.skip("served DB not built")
        c = sqlite3.connect(DB)
        tx = c.execute(
            "select treatment_ja from diseases where species='dog' and name='Mitral Valve Disease (MMVD)'"
        ).fetchone()
        if not tx:
            pytest.skip("MMVD not in served DB")
        assert "ピモベンダン" in tx[0]


class TestCrossSpeciesAndReferral:
    def test_no_feline_ate_sentence_outside_cats(self):
        bad = [
            (d["species"], d["name"])
            for d in json.loads(JSON.read_text(encoding="utf-8"))
            if d["species"] != "Cat"
            and (
                "In cats, feline aortic thromboembolism" in (d.get("clinical_signs") or "")
                or "猫では FATE" in (d.get("clinical_signs_ja") or "")
            )
        ]
        assert not bad, bad[:5]

    def test_generator_gates_feline_ate_to_cats(self):
        from scripts.template_elimination.clinical_fields_generator import gen_clinical_signs, gen_clinical_signs_ja

        assert "FATE" not in gen_clinical_signs_ja("cardiac", "心疾患", "horse")
        assert "FATE" in gen_clinical_signs_ja("cardiac", "心疾患", "cat")
        assert "aortic" not in gen_clinical_signs("cardiac", "Heart Disease", "dog")

    def test_runtime_strip_marker_covers_feline_ate(self):
        from api.species.helpers import strip_cross_species_text

        txt = "代償期: 心雑音。猫では FATE（大動脈血栓塞栓症）として急性後肢麻痺で発症することがある。"
        assert "FATE" not in strip_cross_species_text(txt, "horse")
        assert "FATE" in strip_cross_species_text(txt, "cat")

    def test_no_zoo_medicine_referral_anywhere(self):
        for p in [JSON, *(ROOT / "api" / "species").glob("*_diseases.py")]:
            assert "ACZMまたはAVMAエキゾチック分科会" not in p.read_text(encoding="utf-8"), p.name

    def test_referral_line_is_species_appropriate(self):
        from scripts.template_elimination.fix_specialist_referral_line import referral_line

        assert "ACVIM" in referral_line("dog") and "ECEIM" in referral_line("horse")
        assert "Avian" in referral_line("parrot") and "Reptile" in referral_line("snake")
        assert "Exotic Companion Mammal" in referral_line("hamster")


class TestEnglishTreatmentMirrors:
    def test_translations_are_english_and_numerically_verified(self):
        from scripts.template_elimination.apply_en_treatment_translations import MANUALLY_REVIEWED, verify

        path = ROOT / "api" / "data" / "treatment_en_translations.json"
        data = json.loads(path.read_text(encoding="utf-8"))["entries"]
        assert len(data) >= 90
        for key, en in data.items():
            assert not CJK.search(en), key
        if not DB.exists():
            pytest.skip("served DB not built")
        ja_entries = json.loads(path.read_text(encoding="utf-8")).get("ja_entries", {})
        for key, ja in ja_entries.items():
            assert verify(ja, data[key]) is None, key
        c = sqlite3.connect(DB)
        for key, en in data.items():
            sp, name = key.split("|", 1)
            if key in ja_entries or (sp, name) in MANUALLY_REVIEWED:
                continue
            row = c.execute("select treatment_ja from diseases where species=? and name=?", (sp, name)).fetchone()
            if not row or not row[0]:
                continue
            assert verify(row[0], en) is None, key

    def test_served_db_has_no_japanese_only_english_treatment(self):
        if not DB.exists():
            pytest.skip("served DB not built")
        c = sqlite3.connect(DB)
        bad = [f"{r[0]}|{r[1]}" for r in c.execute("select species,name,treatment from diseases") if _ja_heavy(r[2])]
        assert not bad, bad[:5]

    def test_runtime_horse_path_serves_english_treatment(self):
        from api.vetdict_api import app

        items = app.test_client().get("/api/health-check/diseases?species=horse").get_json()
        items = items if isinstance(items, list) else items.get("diseases", [])
        assert items and all(d.get("treatment") for d in items)
        assert not [d["name"] for d in items if _ja_heavy(d["treatment"])]

    def test_verifier_rejects_altered_dose(self):
        from scripts.template_elimination.apply_en_treatment_translations import verify

        assert verify("イベルメクチン0.2 mg/kg PO", "ivermectin 0.2 mg/kg PO") is None
        assert verify("イベルメクチン0.2 mg/kg PO", "ivermectin 0.4 mg/kg PO")
        assert verify("週1回評価", "assess weekly") is None
        assert verify("投与", "投与 dose")


class TestBatch80ApixabanCredelioPlus:
    def _d(self, i):
        from api.drug_dictionary import DRUGS

        return next(d for d in DRUGS if d["id"] == i)

    def test_apixaban_doses_and_registry(self):
        from api.drug_interactions import find_interactions

        d = self._d("apixaban")
        assert "0.625 mg" in d["species_info"]["cat"]["dosage"]
        assert "0.5 mg/kg" in d["species_info"]["dog"]["dosage"]
        assert "CURATIVE" in " ".join(d["references"])
        sev = {
            (i["drug_a"], i["drug_b"]): i["severity"]
            for i in find_interactions(["apixaban", "rivaroxaban", "clopidogrel"])
        }
        assert sev[("apixaban", "rivaroxaban")] == "major"
        assert sev[("apixaban", "clopidogrel")] == "moderate"

    def test_credelio_plus_label_and_gates(self):
        d = self._d("lotilaner_milbemycin")
        dog = d["species_info"]["dog"]
        assert "20-41 mg/kg" in dog["dosage"] and "0.75-1.53 mg/kg" in dog["dosage"]
        assert "heartworm-negative" in dog["notes"] and d["species_info"]["cat"]["safe"] is False

    def test_resolution_and_treatment_links(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        assert resolve_drug_reference("あぴきさばん") == "apixaban"
        assert resolve_drug_reference("クレデリオプラス") == "lotilaner_milbemycin"
        assert resolve_drug_reference("クレデリオ") == "lotilaner"
        ids = [x["id"] if isinstance(x, dict) else x for x in find_drugs_in_text("アピキサバン 0.625 mg/頭")]
        assert "apixaban" in ids
        cat_ate = next(
            x
            for x in json.loads(JSON.read_text(encoding="utf-8"))
            if x["species"] == "Cat" and x["name"] == "Aortic Thromboembolism (Saddle Thrombus)"
        )
        assert "アピキサバン" in cat_ate["treatment_ja"] and "apixaban" in cat_ate["treatment"]


def test_app_js_detail_jump_bar_wired():
    js = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
    css = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    assert "function _addDetailJumpBar" in js and "_addDetailJumpBar(detail);" in js
    for key in ("treatment", "prognosis", "diagnosis", "signs"):
        assert f'dt data-jump="{key}"' in js
    assert "scrollToAnchor(dt,{settle:false" in js and "e.stopPropagation()" in js
    assert ".detail-jump-chip" in css and "min-height:40px" in css
