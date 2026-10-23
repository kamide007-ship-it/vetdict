"""2026-10 第76弾: チャット精度第51回・草食動物/鳥類の異種文の撲滅（犬猫等の消化器・歯科欄）・
鑑別診断結果カードのセクション・ジャンプバー。"""

import json
import re
import sqlite3
import warnings
from pathlib import Path

import pytest

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
DB = ROOT / "instance" / "vetdict.db"
warnings.filterwarnings("ignore")

_HERB_MARKS = ("草食動物（ウサギ", "草食動物GI stasis", "鳥類: 適切なくちばし", "草食動物では繊維")


def _json_records():
    data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data["diseases"]


class TestChatClinicalAccuracyAuditRound51:
    def test_fiery_red_eyes_is_conjunctivitis(self):
        ids, top = _dog("目が真っ赤で目やにが多いです")
        assert "redness_in_eyes" in ids and "結膜炎" in top, (ids, top)

    def test_back_palpation_pain_is_ivdd(self):
        ids, top = _dog("背中を触ると痛がります")
        assert "back_pain" in ids and "椎間板" in top[0], (ids, top)

    def test_hind_weakness_and_stumbling(self):
        ids, top = _dog("後ろ足の力が弱くなってよろけます")
        # legacy dog vocabulary folds hind-limb weakness into limping
        assert "ataxia" in ids and ids & {"hind_limb_weakness", "limping"}, ids
        assert "椎間板" in top[0], top

    def test_wobbly_is_ataxia_not_tremor(self):
        from api.chat.symptom_aliases import SYMPTOM_ALIASES

        assert SYMPTOM_ALIASES["よろよろ"] == "ataxia"

    def test_perianal_red_swelling_is_anal_sac(self):
        ids, top = _dog("おしりの横が赤く腫れて痛がります")
        assert "肛門" in top[0], (ids, top)

    def test_small_frequent_urination_is_lower_urinary(self):
        ids, top = _dog("おしっこの回数が増えて量が少ないです")
        assert any("膀胱" in t or "結石" in t for t in top), (ids, top)

    def test_food_quantity_phrase_is_not_urinary(self):
        ids, _ = _dog("食べる量が少ないです")
        assert "straining_to_urinate" not in ids, ids

    def test_dilated_pupil(self):
        ids, _ = _dog("左の目だけ瞳孔が開いています")
        assert ids, ids

    def test_rabbit_itchy_crusted_ears_reach_ear_ddx(self):
        ids, top = _sp("耳を痒がってかさぶたがあります", "rabbit", 5)
        assert "ear_scratching" in ids, ids

    def test_snake_purulent_mouth_reaches_oral_ddx(self):
        ids, top = _sp("口の中に膿があります", "snake")
        assert ids and any("口内炎" in t or "口腔膿瘍" in t for t in top), (ids, top)


class TestCrossTaxonGiDentalClauses:
    def test_strip_unit_owner_aware(self):
        from api.species.helpers import strip_cross_species_text, strip_cross_species_text_en

        t = "犬の予防。草食動物（ウサギ・モルモット・チンチラ・デグー）: 高繊維チモシー乾草。異物誤食予防。"
        assert strip_cross_species_text(t, "dog") == "犬の予防。異物誤食予防。"
        assert strip_cross_species_text(t, "rabbit") == t
        en = "Causes include plaque.\nIn herbivores, insufficient fibre causes stasis. Stress also contributes."
        out = strip_cross_species_text_en(en, "dog")
        assert "herbivore" not in out and out.startswith("Causes include plaque.\n")
        assert strip_cross_species_text_en(en, "horse") == en

    def test_dog_cat_json_free_of_herbivore_clauses(self):
        bad = []
        for r in _json_records():
            if r["species"] not in ("Dog", "Cat"):
                continue
            for k, v in r.items():
                if isinstance(v, str) and (any(m in v for m in _HERB_MARKS) or "In herbivores" in v):
                    bad.append((r["name"], k))
        assert not bad, bad[:5]

    def test_rabbit_keeps_its_own_clause(self):
        hits = [
            r["name"]
            for r in _json_records()
            if r["species"] == "Rabbit"
            and any("草食動物（ウサギ" in (v or "") for v in r.values() if isinstance(v, str))
        ]
        assert hits

    @pytest.mark.skipif(not DB.exists(), reason="served DB not built")
    def test_served_db_dog_cat_clean(self):
        con = sqlite3.connect(DB)
        rows = con.execute(
            "select id, prevention_ja, causes, causes_ja from diseases where species in ('dog','cat')"
        ).fetchall()
        bad = [r[0] for r in rows if any(m in (v or "") for v in r[1:] for m in (*_HERB_MARKS, "In herbivores"))]
        assert not bad, bad[:5]


class TestCheckerCardJumpBar:
    def test_checker_card_sections_are_jump_targets(self):
        for key in ("signs", "diagnosis", "treatment", "prognosis"):
            assert f'class="detail-section" data-jump="{key}"' in APP_JS, key
        body = APP_JS.split("function toggleDetail(head){")[1].split("\n}\n")[0]
        assert "_addDetailJumpBar(detail)" in body

    def test_service_worker_bumped(self):
        sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
        assert int(re.search(r"vetdict-v(\d+)", sw).group(1)) >= 190
