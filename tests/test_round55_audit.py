"""2026-10 第80弾: 犬の胃潰瘍（チャットDB・黒色便ゲート）、猫の耳血腫（耳介腫脹ID）、
チャット精度第55回（尾の下垂・鼻血・流涙・トカゲ尾の痩せ・馬の眼瞼腫脹/無汗症）、
ベナゼプリル・スピロノラクトン配合錠（カルダリス）、スマホの詳細パネル内 sticky ジャンプバー。"""

import json
import re
import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _horse, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
CSS = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestGastricUlcerChatEntry:
    def test_melena_is_gastric_ulcer(self):
        ids, top = _dog("便が真っ黒でタール状です")
        assert "black_tarry_stool" in ids and top[0] == "胃潰瘍", (ids, top)
        ids, top = _dog("便が黒くて吐いています")
        assert top[0] == "胃潰瘍", (ids, top)

    def test_vomiting_alone_is_not_ulcer(self):
        _, top = _dog("吐いて食欲がありません")
        assert "胃潰瘍" not in top[:2], top

    def test_name_mirrors_dog_module(self):
        from api.health_checker import DISEASES
        from api.species import dog_diseases

        legacy = next(d for d in DISEASES if d["id"] == "gastroduodenal_ulcer")
        assert any(m["name"] == legacy["name_en"] for m in dog_diseases.DISEASES)
        assert "Marks 2018" in legacy["description_en"]


class TestChatClinicalAccuracyAuditRound55:
    def test_cat_fluctuant_pinna_is_aural_hematoma(self):
        ids, top = _sp("耳が腫れてぷよぷよしています", "cat")
        assert "ear_swelling" in ids and top[0] == "猫耳血腫", (ids, top)
        _, top = _sp("耳を掻いて耳垢が出ます", "cat")
        assert top[0] != "猫耳血腫", top

    def test_dog_tail_carried_low_is_back_pain(self):
        ids, _ = _dog("尻尾を振らなくなり下げたままです")
        assert "back_pain" in ids, ids

    def test_epistaxis_beats_bare_bleeding(self):
        ids, top = _dog("鼻血が出ています")
        assert ids == {"epistaxis"} and "鼻腔内腫瘍" in top[0], (ids, top)
        ids, _ = _sp("鼻血が出ています", "cat")
        assert "bleeding" not in ids, ids

    def test_rabbit_lacrimation_and_lizard_tail(self):
        ids, _ = _sp("目から涙がたくさん出ます", "rabbit")
        assert "eye_discharge" in ids, ids
        ids, top = _sp("食べないで痩せてきました 尻尾が細い", "lizard")
        assert "tail_thinning" in ids and any("クリプト" in t for t in top[:3]), (ids, top)

    def test_cat_umbilical_hernia_no_longer_on_bare_pain(self):
        _, top = _sp("体を触ると嫌がって隠れています", "cat", 5)
        assert "猫臍ヘルニア" not in top, top

    def test_horse_eyelid_swelling_and_polite_anhidrosis(self):
        ids, top = _horse("目が腫れて涙が出ます")
        assert "eye_swelling" in ids and "body_swelling" not in ids, ids
        assert top[0] == "結膜炎", top
        ids, top = _horse("汗をかきません")
        assert top[0] == "無汗症", (ids, top)


class TestBatch88Cardalis:
    def test_monograph(self):
        from api.drug_dictionary import _drug_index

        d = _drug_index["benazepril_spironolactone"]
        dog = d["species_info"]["dog"]
        assert dog["safe"] and "0.25 mg/kg" in dog["dosage"] and "2 mg/kg" in dog["dosage"]
        assert "1日1回" in dog["dosage_ja"] and "BESST" in dog["notes"]
        assert d["species_info"]["cat"]["safe"] is False
        assert any("Coffman" in r for r in d["references"])

    def test_resolution_and_interactions(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference
        from api.drug_interactions import find_interactions

        assert resolve_drug_reference("カルダリス") == "benazepril_spironolactone"
        assert resolve_drug_reference("パノクエル") == "fuzapladib"
        ids = [x["id"] for x in find_drugs_in_text("ベナゼプリル 0.25 mg/kg とスピロノラクトン 2 mg/kg")]
        assert "benazepril_spironolactone" not in ids, ids  # 成分言及は配合錠に化けない
        for other in ("spironolactone", "benazepril", "potassium_gluconate"):
            hits = find_interactions(["benazepril_spironolactone", other])
            assert hits and hits[0]["severity"] == "major", other

    def test_mmvd_treatment_mentions_it_in_both_paths(self):
        from api.species import dog_diseases

        mod = next(m for m in dog_diseases.DISEASES if m["name"] == "Mitral Valve Disease (MMVD)")
        blob = json.dumps(mod, ensure_ascii=False, default=list)
        assert "カルダリス" in blob and "Cardalis" in blob
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        e = next(
            x for x in data if x.get("species", "").lower() == "dog" and x.get("name") == "Mitral Valve Disease (MMVD)"
        )
        assert "カルダリス" in e["treatment_ja"] and "Cardalis" in e["treatment"]


class TestStickyJumpBar:
    def test_mobile_sticky_css_and_clip(self):
        assert re.search(r"\.disease-detail\.open \.detail-jump-bar\{position:sticky;top:var\(--sticky-offset", CSS)
        assert "overflow:hidden;overflow:clip;" in CSS  # .card はスクロールコンテナを作らない
        assert 'detail.style.overflowX="clip"' in APP_JS
        assert 'detail.style.overflowX="";' in APP_JS

    def test_landing_offset_and_top_chip(self):
        assert "function _jumpBarOverlay(bar)" in APP_JS
        assert "extraOffset:_jumpBarOverlay(bar)" in APP_JS
        assert "(opts.extraOffset||0)" in APP_JS
        assert "detail-jump-top" in APP_JS and "⬆ 先頭" in APP_JS

    def test_sw_bumped(self):
        sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
        assert int(re.search(r"vetdict-v(\d+)", sw).group(1)) >= 195
