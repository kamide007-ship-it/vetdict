"""2026-10 第81弾: チャット精度第56回（患肢をかばう・毛玉を吐けない・眼の混濁/羞明・
排尿時の発声・ウジの是正・脚のかさぶた・皮膚のかさかさ）、組換えヒトTSH（タイロゲン）、
チャット回答の候補ジャンプ・ストリップ。"""

import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
CSS = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound56:
    def test_guarding_a_limb_is_lameness(self):
        ids, top = _dog("右の前足をかばって歩いています")
        assert "lameness_or_limping" in ids or "limping" in ids, ids
        assert top, top

    def test_cat_unproductive_hairball_retching(self):
        ids, top = _sp("毛玉を吐こうとして出ません", "cat", 5)
        assert "hairball_retching" in ids, ids
        assert top[0] == "猫毛球閉塞症" and "猫喘息" in top, top

    def test_cat_cough_alone_still_asthma(self):
        _, top = _sp("咳をしています", "cat")
        assert top[0] == "猫喘息", top

    def test_cat_cloudy_photophobic_eye_is_uveitis_or_ulcer(self):
        ids, top = _sp("目の色が濁って眩しそうにしています", "cat", 3)
        assert {"cloudiness_in_eyes", "squinting"} <= ids, ids
        assert any(("ぶどう膜" in t) or ("角膜" in t) for t in top), top
        assert top[0] != "虹彩黒色腫", top

    def test_guinea_pig_squeal_on_urination(self):
        ids, top = _sp("おしっこをするときにキーキー鳴きます", "guinea_pig", 4)
        assert "squealing_when_urinating" in ids, ids
        assert any(("尿" in t) or ("膀胱" in t) for t in top[:3]), top

    def test_maggot_phrase_no_longer_diarrhea(self):
        from api.chat.symptom_aliases import SYMPTOM_ALIASES

        assert SYMPTOM_ALIASES["ウジがわいてる"] == "maggots_visible"
        ids, top = _sp("お尻の周りにウジがいます", "rabbit")
        assert "maggots_visible" in ids and "ハエウジ" in top[0], (ids, top)

    def test_parakeet_leg_crusts_and_hamster_dry_skin(self):
        ids, top = _sp("足にかさぶたがあってガサガサしています", "parakeet")
        assert any("疥癬" in t for t in top), (ids, top)
        ids, _ = _sp("毛が抜けて皮膚がかさかさです", "hamster")
        assert "hair_loss" in ids and len(ids) >= 2, ids


class TestBatch89Thyrotropin:
    def test_monograph(self):
        from api.drug_dictionary import _drug_index

        d = _drug_index["thyrotropin_alfa"]
        dog = d["species_info"]["dog"]
        cat = d["species_info"]["cat"]
        assert "75-150 µg" in dog["dosage"] and "6 hours" in dog["dosage"]
        assert "6時間後" in dog["dosage_ja"] and "Boretti" in dog["dosage"]
        assert "25-200 µg" in cat["dosage"] and "医原性" in cat["notes_ja"]
        assert any("Stegeman" in r for r in d["references"])

    def test_resolution_and_disease_link(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        assert resolve_drug_reference("タイロゲン") == "thyrotropin_alfa"
        assert resolve_drug_reference("rhTSH") == "thyrotropin_alfa"
        ids = [d["id"] for d in find_drugs_in_text("TSH刺激試験で確認後、レボチロキシンを試用")]
        assert "thyrotropin_alfa" in ids and "levothyroxine" in ids


class TestChatCandidateJumpStrip:
    def test_wired(self):
        assert "chat-cand-jump-btn" in APP_JS and "card.dataset.rank=String(i+1)" in APP_JS
        assert 'closest(".chat-cand-jump-btn")' in APP_JS
        assert ".chat-cand-jump{" in CSS and ".chat-card-flash" in CSS
        sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
        import re

        assert int(re.search(r"vetdict-v(\d+)", sw).group(1)) >= 196
