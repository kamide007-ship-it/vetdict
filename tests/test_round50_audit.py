"""2026-10 第75弾: チャット精度第50回・英語臨床徴候の定型句撲滅・猫の歯の吸収病変（FORL）の
キュレーション・エルツグリフロジン／メチルフェニデート公開・麻酔/緊急プロトコルのジャンプバー。"""

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


def _json_records():
    data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data["diseases"]


class TestChatClinicalAccuracyAuditRound50:
    def test_ulcerated_purulent_ear_is_otitis(self):
        ids, top = _dog("耳の中がただれて黄色い膿が出ています")
        assert "ear_discharge" in ids and top[0] == "外耳炎", top

    def test_cat_fiery_red_mouth_is_fcgs(self):
        ids, top = _sp("口の中が真っ赤でよだれが多く食べたがりません", "cat")
        assert "stomatitis" in ids and top[0] == "猫慢性歯肉口内炎", top

    def test_face_rubbing_with_adverb_and_periocular_redness(self):
        ids, top = _dog("顔をしきりに前足でこすっていて目の周りが赤いです")
        assert {"itching", "redness_in_eyes"} <= ids, ids
        assert any("アトピー" in t or "結膜" in t for t in top), top

    def test_curated_shikirini_key_survives_adverb_strip(self):
        from api.chat.symptom_extractor import normalize_chat_text

        assert "陰部をしきりに舐め" in normalize_chat_text("陰部をしきりに舐めています")
        assert normalize_chat_text("水を全然飲まない") == "水を飲まない"

    def test_perianal_mass_subsumes_generic_lump(self):
        ids, top = _dog("お尻のまわりにしこりができています")
        assert "lumps_bumps" not in ids and "scooting" in ids, ids
        assert "肛門" in top[0], top

    def test_unilateral_proptosis_phrase(self):
        ids, top = _dog("右の目だけ飛び出したように大きく見えます")
        assert ids == {"eye_bulging"} and "眼球" in top[0], top

    def test_cat_resorbing_teeth_is_forl(self):
        ids, top = _sp("歯が欠けたように溶けて口を痛がります", "cat")
        assert "tooth_loss" in ids and "pain" not in ids, ids
        assert "猫の歯の吸収病変" in top, top

    def test_cat_anuria_negated_form_still_extracted(self):
        ids, top = _sp("水を全然飲まずおしっこもしていません", "cat")
        assert "decreased_urination" in ids and top[0] == "尿道閉塞", top

    def test_plain_negation_still_guarded(self):
        ids, _ = _dog("咳はまったくありません")
        assert not ids, ids

    def test_tooth_loss_falls_back_for_other_species(self):
        ids, top = _sp("歯が溶けています", "rabbit")
        assert ids and any("歯" in t or "咬合" in t for t in top), (ids, top)


class TestClinicalSignsFillerStripped:
    def test_strip_filler_unit(self):
        from scripts.template_elimination.strip_clinical_signs_filler import strip_filler

        s = (
            "Clinical signs of addison's disease in dog include: Vomiting, Lethargy.; typical viral etiology "
            "presentation; variable severity depending on disease stage; response to treatment helps confirm diagnosis"
        )
        assert strip_filler(s) == "Clinical signs of addison's disease in dog include: Vomiting, Lethargy."
        semi = "Fever; cough; sneezing; typical viral etiology presentation; symptom timeline varies by individual"
        assert strip_filler(semi) == "Fever; cough; sneezing."
        curated = "Fever; cough; observe for systemic signs (fever, malaise)"
        assert strip_filler(curated) == curated

    def test_no_filler_left_in_json(self):
        bad = [
            r["name"]
            for r in _json_records()
            if "etiology presentation" in (r.get("clinical_signs") or "")
            or "helps confirm diagnosis" in (r.get("clinical_signs") or "")
        ]
        assert not bad, bad[:5]

    @pytest.mark.skipif(not DB.exists(), reason="served DB not built")
    def test_no_filler_in_served_db(self):
        con = sqlite3.connect(DB)
        n = con.execute(
            "select count(*) from diseases where clinical_signs like '%etiology presentation%'"
            " or clinical_signs like '%helps confirm diagnosis%'"
        ).fetchone()[0]
        assert n == 0


class TestFelineToothResorptionCurated:
    def _rec(self):
        return next(
            r for r in _json_records() if r["name"] == "Feline Tooth Resorption (FORL)" and r["species"] == "Cat"
        )

    def test_json_fields_are_forl_specific(self):
        r = self._rec()
        assert "歯冠切断" in r["treatment_ja"] and "歯科X線" in r["treatment_ja"]
        assert "トリミング" not in r["treatment_ja"]
        for f in ("causes", "causes_ja", "prevention_ja", "clinical_signs_ja"):
            assert "草食" not in r[f] and "herbivore" not in r[f].lower(), f
        assert "odontoclast" in r["causes"].lower()

    def test_module_matches_and_carries_tooth_loss(self):
        from api.species.cat_diseases import DISEASES

        d = next(x for x in DISEASES if x["name"] == "Feline Tooth Resorption (FORL)")
        assert "tooth_loss" in d["symptoms"]
        assert "トリミング" not in d["treatment_ja"] and "草食" not in d["causes_ja"]


class TestBatch84ReferencedAgents:
    def _drug(self, did):
        from api.drug_dictionary import DRUGS

        return next(d for d in DRUGS if d["id"] == did)

    def test_ertugliflozin_horse_only_with_trig_monitoring(self):
        d = self._drug("ertugliflozin")
        h = d["species_info"]["horse"]
        assert h["safe"] and "0.05 mg/kg" in h["dosage"] and "中性脂肪" in h["dosage_ja"]
        assert d["species_info"]["dog"]["safe"] is False and d["species_info"]["cat"]["safe"] is False
        assert any("Sundra" in r for r in d["references"])

    def test_methylphenidate_diagnostic_trial_and_mao_gate(self):
        d = self._drug("methylphenidate")
        assert "0.2-1 mg/kg" in d["species_info"]["dog"]["dosage"]
        assert d["species_info"]["cat"]["safe"] is False
        from api.drug_interactions import find_interactions

        hits = find_interactions(["methylphenidate", "selegiline"])
        assert hits and hits[0]["severity"] == "contraindicated"

    @pytest.mark.parametrize(
        "text,did",
        [
            ("エルツグリフロジン 0.05-0.15 mg/kg PO SID", "ertugliflozin"),
            ("メチルフェニデート（0.2-1 mg/kg PO 単回投与）", "methylphenidate"),
            ("セフポドキシム 5-10 mg/kg PO q24h", "cefpodoxime"),
            ("マイコフェノール酸 10-15 mg/kg", "mycophenolate"),
            ("ファイロコキシブ(エクオキソル) 0.1 mg/kg", "firocoxib"),
            ("アンフォテリシンB（1.5 mg/kg", "amphotericin_b"),
        ],
    )
    def test_text_matcher_resolves(self, text, did):
        from api.drug_dictionary import find_drugs_in_text

        ids = [x if isinstance(x, str) else x.get("id") for x in find_drugs_in_text(text)]
        assert did in ids, (text, ids)


class TestProtocolJumpBar:
    def test_anesthesia_and_emergency_sections_are_jump_targets(self):
        for anchor in (
            'class="anesthesia-drugs-table" data-jump="anesdrugs"',
            'class="anesthesia-monitor-section" data-jump="monitor"',
            'class="anesthesia-references" data-jump="refs"',
            'data-jump="emsteps"',
            'data-jump="emdrugs"',
        ):
            assert anchor in APP_JS, anchor
        for key in ("emsteps", "emdrugs", "anesdrugs", "monitor", "refs"):
            assert f'"{key}"' in APP_JS.split("function _addDetailJumpBar")[1].split("\n}\n")[0], key

    def test_service_worker_bumped(self):
        sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
        import re

        assert int(re.search(r"vetdict-v(\d+)", sw).group(1)) >= 189
