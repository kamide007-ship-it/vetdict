"""2026-11 第83弾: チャット精度第58回（猫ATEの非連続形「冷たくなって動かない」の
併記抽出・犬の散瞳＋充血→緑内障・ケンケン/けんけん・フクロモモンガ「かじる」・
猫の腹部過剰グルーミング・魚の水面ぱくぱく）、行動学サプリの商品名解決
（Zylkene/Anxitane）、問診モード最終結果の候補ジャンプ・ストリップ。"""

import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound58:
    def test_cat_ate_cold_and_paralysed_hind_limbs(self):
        ids, top = _sp("後ろ足が急に冷たくなって動きません", "cat")
        assert {"cold_extremities", "hind_limb_paralysis"} <= ids, ids
        assert "血栓" in top[0], top

    def test_coextract_registry_is_wired(self):
        from api.chat.symptom_aliases import ALIAS_COEXTRACT, SYMPTOM_ALIASES

        for key in ALIAS_COEXTRACT:
            assert key in SYMPTOM_ALIASES, key

    def test_dog_red_eye_with_mydriasis_is_glaucoma(self):
        ids, top = _dog("片方の目が赤くて瞳が大きいです")
        assert "vision_loss" in ids and top[0] == "緑内障", (ids, top)

    def test_bare_red_eye_not_hijacked_by_glaucoma(self):
        _, top = _dog("目が赤くて目やにが出ます")
        assert top[0] != "緑内障", top

    def test_kenken_katakana_and_hiragana(self):
        for phrase in ("後ろ足をケンケンします", "けんけんして歩きます"):
            ids, top = _dog(phrase)
            assert "limping" in ids, (phrase, ids)
            assert any(("膝蓋" in t) or ("関節" in t) or ("靭帯" in t) for t in top), top

    def test_sugar_glider_kajiru_self_mutilation(self):
        ids, top = _sp("自分の体をかじっています", "sugar_glider")
        assert "self_mutilation" in ids and any("自己損傷" in t for t in top), (ids, top)

    def test_cat_belly_overgrooming(self):
        ids, top = _sp("お腹の毛を舐めて薄くなっています", "cat")
        assert "excessive_grooming" in ids, ids
        assert any(("脱毛" in t) or ("グルーミング" in t) for t in top), top

    def test_fish_surface_gasping_hiragana(self):
        ids, top = _sp("水面でぱくぱくしています", "fish")
        assert "gasping_surface" in ids, ids
        assert any(("中毒" in t) or ("ショック" in t) or ("酸素" in t) for t in top), top

    def test_paku_paku_eating_is_not_gasping(self):
        ids, _ = _dog("ご飯をぱくぱく食べるのに痩せます")
        assert "gasping_surface" not in ids


class TestBehaviouralSupplementBrandResolution:
    def test_zylkene_and_anxitane_resolve(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        ids = {d["id"] for d in find_drugs_in_text("Zylkene 15 mg/kg PO q24h; Anxitane 2.5-5 mg/kg PO q12h")}
        assert {"alpha_casozepine", "l_theanine"} <= ids, ids
        assert resolve_drug_reference("ジルケーン") == "alpha_casozepine"
        assert resolve_drug_reference("アンキシタン") == "l_theanine"


class TestGuidedCandidateJumpStrip:
    def test_shared_strip_helper_used_by_both_renderers(self):
        assert "function _candJumpStripHtml(names)" in APP_JS
        assert APP_JS.count("_candJumpStripHtml(") >= 3
        assert 'class="chat-disease-card" data-rank="${i+1}"' in APP_JS
