"""第38弾: 一般的疾患の可視化 + モバイルUX（2026-09）.

開発者フィードバック2件への回帰ガード:
1.「鑑別診断時に、いきなり重篤な疾患ではなく、一般的な疾患が見落とされがち」
   → 全エンジンが prevalence_tier を結果に公開し、UIは頻度チップ+一般的鑑別
   ノートで可視化する。馬チェッカーは汎用種と同じ2相（よくある疾患を先に）
   提示になる。ランキング数式そのものは不変（緊急疾患の安全ブーストは意図的）。
2.「スマホで使われることが多い」→ iOSフォーカスズームの無効化（16px）、
   44pxタップ目標、印刷ポップアップブロック時のトースト。
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
MAIN_CSS = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")


class TestPrevalenceTierExposure:
    def test_generic_chat_matcher_exposes_tier(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases

        r = _match_species_symptoms_to_diseases(["loss_of_appetite", "small_fecal_pellets"], "rabbit")
        assert r, "no rabbit matches"
        assert "prevalence_tier" in r[0]
        assert r[0]["prevalence_tier"] == "very_common"  # GI stasis

    def test_legacy_dog_chat_matcher_exposes_tier(self):
        from api.diagnostic_chat import match_symptoms_to_diseases

        r = match_symptoms_to_diseases(["vomiting", "loss_of_appetite"])
        assert r and "prevalence_tier" in r[0]
        assert r[0]["prevalence_tier"] in ("very_common", "common")

    def test_horse_results_expose_tier_and_two_phase_presentation(self):
        """馬経路は tier 未公開・フラット表示のみで、稀な疾患が先頭に並び
        「一般的な疾患が見落とされがち」だった。汎用種と同じ2相分割
        （phase_1_common を先に提示）を要求する。"""
        from api.species_analyzer import analyze_horse

        h = analyze_horse(["hoof_heat", "limb_lameness_fore"])
        conds = h["possible_conditions"]
        assert conds and "prevalence_tier" in conds[0]
        phases = h.get("suspected_diseases_by_phase")
        assert phases, "horse payload must carry suspected_diseases_by_phase"
        ph1 = phases["phase_1_common"]
        assert ph1, "phase 1 (common) must not be empty for the hot-hoof presentation"
        assert all(c["prevalence_tier"] in ("very_common", "common") for c in ph1)
        ph1_names = {c["name"] for c in ph1[:3]}
        assert {"蹄膿瘍", "蹄葉炎"} & ph1_names, ph1_names

    def test_generic_checkbox_exposes_tier(self):
        from api import species_analyzer as sa

        g = sa.analyze_species_symptoms("cat", ["sneezing", "nasal_discharge", "eye_discharge"])
        lst = g["suspected_diseases"]
        assert lst and lst[0].get("prevalence_tier") == "very_common"  # feline URI


class TestBirdHeavyMetalInversionFixed:
    def test_bird_generic_sick_presentation_ranks_commons_first(self):
        """鳥「下痢+元気がない」で、未tierの重金属変異エントリと鉤頭虫
        （伴侶鳥では稀 — 主に野鳥・水禽の寄生虫）が tier付き common を
        押しのけて上位を占めていた逆転の再発防止。"""
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases

        r = _match_species_symptoms_to_diseases(["diarrhea", "lethargy"], "bird")
        assert len(r) >= 5
        top3 = r[:3]
        assert all(x.get("prevalence_tier") in ("very_common", "common") for x in top3), [
            (x["name_en"], x.get("prevalence_tier")) for x in top3
        ]
        acantho = next((x for x in r if "Acanthocephalan" in x["name_en"]), None)
        assert acantho is not None and acantho["prevalence_tier"] == "rare"
        # 重金属変異エントリは common に整列（Ritchie & Harrison）
        hm = next((x for x in r if "Heavy Metal" in x["name_en"]), None)
        assert hm is not None and hm["prevalence_tier"] == "common"


class TestFrontendCommonDiseaseVisibility:
    def test_freq_chip_and_common_dx_note_defined(self):
        assert "function freqChip(" in APP_JS
        assert "function commonDxNote(" in APP_JS
        # ノートは 1位が common/very_common なら出さない設計
        assert 'if(isCommon(tier(list[0])))return""' in APP_JS

    def test_chip_rendered_in_both_chat_card_renderers(self):
        # 自由入力チャット候補カード + 問診モード最終結果カード
        assert APP_JS.count("${freqChip(") >= 2

    def test_note_wired_into_chat_guided_and_flat_checker_fallbacks(self):
        # 自由チャット（insertAdjacentHTML）+ 問診 + チェッカーのフラット2経路
        assert APP_JS.count("commonDxNote(") >= 5  # 定義1 + 呼び出し4

    def test_css_classes_present(self):
        for cls in (".freq-chip", ".freq-common", ".freq-rare", ".common-dx-note"):
            assert cls in MAIN_CSS, cls


class TestMobileErgonomics:
    def test_ios_zoom_block_covers_new_inputs(self):
        """フォーカス時フォント<16pxはiOS Safariがページを自動ズームする。
        計算機の入力/select・相互作用チェッカー・ランディングチャットは
        既存の16pxブロック新設後に追加され漏れていた。"""
        i = MAIN_CSS.index("Prevent iOS auto-zoom")
        block = MAIN_CSS[i : i + 900]
        for sel in (
            ".calc-row input[type=number]",
            ".calc-row select",
            "#interactionDrugIds",
            "#landingChatInput",
        ):
            assert sel in block, sel
        assert "font-size:16px!important" in block

    def test_mobile_tap_targets_meet_44px(self):
        i = MAIN_CSS.index("計算機は片手タップ操作前提")
        block = MAIN_CSS[i : i + 800]
        assert ".calc-tab-btn{min-height:44px" in block
        assert "min-height:44px" in block.split(".cross-nav-btn")[1][:40]
        # ラベルを上段に積む（狭幅での折返し崩れ防止）
        assert "flex-basis:100%" in block

    def test_print_popup_block_shows_toast(self):
        """window.open が null（ポップアップブロック）のとき、従来は
        無反応だった — 飼い主向けシート・麻酔チェックリストの両方で
        トースト案内を出す。"""
        assert APP_JS.count("ポップアップがブロックされました") >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
