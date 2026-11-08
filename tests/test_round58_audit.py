"""2026-11 第83弾: チャット精度第58回（低体温・口腔出血・腰振り歩行・陰部舐め/腫脹・
砂かき反復・ひらがな耳掻き・乏尿・ケンケン・猫ATEの「冷たくて動かない」併記抽出）、
チェッカー結果の鑑別候補ジャンプ・ストリップ。"""

import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound58:
    def test_hip_sway_is_hip_dysplasia(self):
        ids, top = _dog("歩くときに腰が左右に揺れます")
        assert "hip_sway" in ids, ids
        assert top[0] == "股関節形成不全", top

    def test_hip_sway_checkbox_parity(self):
        from api.species.dog_diseases import SYMPTOM_NAMES, analyze_symptoms

        assert "hip_sway" in SYMPTOM_NAMES
        r = analyze_symptoms(["hip_sway", "stiffness"])
        r = r.get("suspected_diseases", r) if isinstance(r, dict) else r
        assert r[0]["name"] == "Hip Dysplasia"

    def test_plain_limping_not_hijacked_by_hip_sway_cluster(self):
        _, top = _dog("足を引きずっています")
        assert top and top[0] == "膝蓋骨脱臼", top

    def test_oral_bleeding_extracted(self):
        ids, top = _dog("口から血が出ています")
        assert ids and "bleeding" not in ids, ids
        assert any("歯" in t or "口" in t for t in top), top

    def test_vulvar_swelling_and_hiragana_licking(self):
        ids, top = _dog("陰部をよくなめていて陰部が腫れています")
        assert "vulvar_discharge" in ids, ids
        assert top, top

    def test_cat_litter_scratching_is_lower_urinary(self):
        ids, top = _sp("トイレの砂をかいてばかりいて何も出ません", "cat")
        assert "straining_to_urinate" in ids, ids
        assert any(("尿" in t) or ("膀胱" in t) for t in top), top

    def test_cat_cold_paralysed_hind_legs_is_ate(self):
        ids, top = _sp("後ろ足が冷たくて動きません", "cat")
        assert {"hind_limb_paralysis", "cold_extremities"} <= ids, ids
        assert any("血栓" in t for t in top), top

    def test_hypothermia_extracted_and_rare_entries_tiered(self):
        ids, top = _sp("急にぐったりして体温が低いです", "cat", 6)
        assert "hypothermia" in ids, ids
        assert not any(x in " ".join(top) for x in ("溺水", "寒冷凝集素")), top

    def test_dog_ear_scratch_oliguria_kenken(self):
        ids, top = _dog("耳を後ろ足でかいてばかりいます")
        assert "ear_scratching" in ids and any("外耳" in t for t in top), (ids, top)
        ids, _ = _dog("水をあまり飲まずおしっこが少ないです")
        assert ids, ids
        ids, top = _dog("後ろ足をケンケンして歩きます")
        assert "limping" in ids, ids


class TestCheckerCandidateJumpStrip:
    def test_strip_rendered_and_wired(self):
        assert "dx-cand-jump-btn" in APP_JS
        assert 'data-dx-rank="${i+1}"' in APP_JS
        i = APP_JS.find('const dxJump=e.target.closest(".dx-cand-jump-btn")')
        assert i > 0
        blk = APP_JS[i : i + 700]
        assert "toggleDetail(head)" in blk and "scrollToAnchor(card)" in blk
        assert "checker_candidate_jump" in blk

    def test_sw_bumped(self):
        sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
        import re

        assert int(re.search(r"vetdict-v(\d+)", sw).group(1)) >= 198
