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


class TestAllSpeciesCommonsAudit:
    """開発者指示「全ての動物種にて一般的な疾患が見落とされていないか、確認」
    (2026-09) の全種自己検索監査で検出・修正した逆転の回帰ガード。

    監査手法: 全21種の common/very_common 疾患について、その疾患自身の
    教科書的症状セットで検索し、(a) 本体が top-3 に入るか、(b) 未tier/稀な
    エントリが上位を奪っていないかを検証（88フラグ → 0-3/run に収束）。
    症状セットは Python set のためサンプリングが非決定的 — ここでは固定の
    症状リストで代表的な修正を固定する。"""

    @staticmethod
    def _match(species, symptom_ids):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases

        return _match_species_symptoms_to_diseases(symptom_ids, species)

    def test_gp_dacryocystitis_urinary_clone_purged(self):
        """GP涙嚢炎の supplementary 症状セットが泌尿器クローン
        （blood_in_urine/straining_to_urinate等）で、膀胱炎主訴の上位を
        涙嚢炎が奪っていた。眼徴候セットへのキュレート後は、泌尿器主訴に
        涙嚢炎が出ず、眼主訴では涙嚢炎が1位で引けること。"""
        r = self._match("guinea_pig", ["blood_in_urine", "straining_to_urinate", "frequent_urination"])
        top6 = [x["name_en"] for x in r[:6]]
        assert "Dacryocystitis" not in top6, top6
        assert any("Cystitis" in n or "Bladder Sludge" in n for n in top6[:2]), top6
        r2 = self._match("guinea_pig", ["eye_discharge", "crusty_eyes", "eye_redness"])
        assert r2[0]["name_en"] == "Dacryocystitis", [x["name_en"] for x in r2[:3]]

    def test_pyometra_outranks_retained_fetus_gp_and_rabbit(self):
        """胎子遺残の症状セットは子宮蓄膿症の厳密なサブセットで、未tierの
        まま陰部分泌物主訴で常勝していた（繁殖直後に限定される病歴依存の
        鑑別）。tier整列後は蓄膿症が上位であること。"""
        for sp, retained in (("guinea_pig", "Retained Fetus"), ("rabbit", "Retained Foetus")):
            r = self._match(sp, ["vaginal_discharge", "lethargy", "appetite_loss"])
            names = [x["name_en"] for x in r[:6]]
            assert names[0] == "Pyometra", (sp, names)
            i_ret = names.index(retained) if retained in names else 99
            assert i_ret > 0, (sp, names)

    def test_cat_jaundice_hepatic_commons_first(self):
        """黄疸主訴で猫肝疾患の主鑑別（肝リピドーシス/胆管炎）より上位に
        胆嚢粘液嚢腫（犬の疾患 — 猫は症例報告レベル）が出ていた逆転の是正。"""
        r = self._match("cat", ["lethargy", "vomiting", "appetite_loss", "jaundice"])
        top4 = [x["name_en"] for x in r[:4]]
        assert any("Hepatic Lipidosis" in n for n in top4), top4
        assert any("Cholangitis" in n for n in top4), top4
        assert "Feline Gallbladder Mucocele" not in top4, top4
        muc = next((x for x in r if x["name_en"] == "Feline Gallbladder Mucocele"), None)
        if muc is not None:
            assert muc["prevalence_tier"] == "rare"

    def test_hamster_otitis_retrievable_by_vestibular_signs(self):
        """ハムスター中耳炎の supplementary 症状セットがクローン汚染で
        斜頸・旋回から引けなかった — キュレート後は1位で解決。"""
        r = self._match("hamster", ["head_tilt", "circling"])
        assert r[0]["name_en"] == "Ear Infection (Otitis)", [x["name_en"] for x in r[:3]]

    def test_tortoise_vitamin_a_duplicate_pair_tier_aligned(self):
        """リクガメはモジュールに Vitamin A Deficiency の正準名と括弧付き
        変異の同一疾患2エントリが併存し、未tierの括弧側が正準側
        （very_common）より上に出る自己重複逆転があった。両方 very_common
        に整列していること。"""
        r = self._match("tortoise", ["swollen_eyes", "anorexia", "nasal_discharge"])
        va = [x for x in r if "Vitamin A" in x["name_en"]]
        assert len(va) >= 2, [x["name_en"] for x in r[:8]]
        assert all(x["prevalence_tier"] == "very_common" for x in va), [
            (x["name_en"], x["prevalence_tier"]) for x in va
        ]
        assert "Vitamin A" in r[0]["name_en"], [x["name_en"] for x in r[:3]]

    def test_parrot_pdd_and_heavy_metal_tiered_common(self):
        """削痩+吐き戻し+振戦のオウム主訴で、PDD（tier済みcommon）と
        重金属中毒群が未tierエントリに埋もれないこと。"""
        r = self._match("parrot", ["weight_loss", "regurgitation", "tremors"])
        top5 = r[:5]
        assert any("PDD" in x["name_en"] for x in top5), [x["name_en"] for x in top5]
        assert top5[0]["prevalence_tier"] in ("very_common", "common"), (
            top5[0]["name_en"],
            top5[0]["prevalence_tier"],
        )


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
