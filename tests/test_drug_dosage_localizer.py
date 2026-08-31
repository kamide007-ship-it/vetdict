"""薬用量ローカライザ（api/drug_dosage_localizer.py）の回帰テスト。

決定論的・fail-closed 設計を検証する:
  * 数値・単位は改変せず保持する
  * 投与経路・投与間隔の英語略号のみ日本語化する
  * 自由文（未知の英単語を含む）は None を返す（誤訳を出さない）
  * CJK を含む原文は変換しない
  * DRUGS 統合後に dosage_ja 欠落が補完され、既存の dosage_ja は保持される
"""

import api.drug_dictionary as drug_dictionary
from api.drug_dosage_localizer import fill_missing_dosage_ja, localize_dosage


class TestCanonicalDoseStrings:
    def test_simple_po_frequency(self):
        assert localize_dosage("10-20 mg/kg PO q12h") == "10-20 mg/kg 経口 12時間毎"

    def test_compound_route(self):
        assert localize_dosage("5-10 mg/kg PO/IM q24h") == "5-10 mg/kg 経口/筋注 24時間毎"

    def test_frequency_range(self):
        assert localize_dosage("5-10 mg/kg PO q8-12h") == "5-10 mg/kg 経口 8-12時間毎"

    def test_day_frequency(self):
        assert localize_dosage("8 mg/kg SC q14d") == "8 mg/kg 皮下 14日毎"

    def test_numbers_preserved_verbatim(self):
        # 数値（用量そのもの）は一切改変されない
        out = localize_dosage("12.5-25 mg/kg PO q12h")
        assert "12.5-25 mg/kg" in out

    def test_per_animal_denominator(self):
        assert localize_dosage("1-3 mg/dog PO q24h") == "1-3 mg/頭 経口 24時間毎"
        assert localize_dosage("0.5-1 mg/cat PO q24h") == "0.5-1 mg/頭 経口 24時間毎"

    def test_sentence_final_period_does_not_leak_frequency(self):
        # "q24h." のような文末ピリオド付き頻度略号は、ピリオドを剥がして
        # 頻度辞書にマッチさせる。剥がさないと数値保持パスを通って英語の
        # 略号がそのまま日本語出力に漏れる（2026-08 に meclizine で発生）。
        out = localize_dosage("12.5 mg/cat PO q24h.")
        assert out == "12.5 mg/頭 経口 24時間毎."
        assert "q24h" not in out
        # 小数点（トークン内部の "."）は影響を受けない
        assert "12.5" in out

    def test_bsa_unit_preserved(self):
        assert localize_dosage("2 mg/m² IV q24h") == "2 mg/m² 静注 24時間毎"

    def test_bath_and_or_connector(self):
        out = localize_dosage("5 mg/kg PO q24h or 5 mg/L bath")
        assert out == "5 mg/kg 経口 24時間毎 または 5 mg/L 薬浴"


class TestFixedPhrases:
    def test_not_established(self):
        assert localize_dosage("Not established") == "用量未確立"

    def test_not_established_trailing_period(self):
        assert localize_dosage("Not established.") == "用量未確立"

    def test_not_indicated(self):
        assert localize_dosage("Not indicated") == "適応なし"


class TestPhrasePatterns:
    """管理語彙フレーズ（2026-08 拡張）の決定論的変換を検証する。"""

    def test_repeat_in_days(self):
        assert localize_dosage("50-100 mg/kg PO, repeat in 14 days") == "50-100 mg/kg 経口, 14日後に再投与"

    def test_duration_after_multiplication(self):
        assert localize_dosage("20-50 mg/kg PO q24h × 3-5 days") == ("20-50 mg/kg 経口 24時間毎 × 3-5日間")

    def test_single_dose(self):
        assert localize_dosage("1-2 mg/kg IM/ICe single dose") == "1-2 mg/kg 筋注/体腔内 単回投与"

    def test_q_days_spelled_out(self):
        out = localize_dosage("50 mg/kg PO q14 days or 10 mg/L bath × 6h")
        assert out == "50 mg/kg 経口 14日毎 または 10 mg/L 薬浴 × 6h"

    def test_drops_and_sublingual(self):
        assert localize_dosage("5-7 mg/kg IV/IM or 1 drop sublingual") == ("5-7 mg/kg 静注/筋注 または 1滴 舌下")

    def test_ophthalmic_ribbon(self):
        assert localize_dosage("Apply 1cm ribbon to affected eye q6-8h") == ("患眼に1cmリボン状に塗布 6-8時間毎")

    def test_nebulized_with_duration(self):
        assert localize_dosage("Nebulized 0.5 mg/ml for 10-15 min") == ("ネブライザー投与 0.5 mg/ml 10-15分間")

    def test_not_established_prefix_with_empirical_dose(self):
        # 前半の固定句と後半の用量が両方変換され、区切り記号前の空白は残らない
        out = localize_dosage("Not established; empirical 10-30 mg/kg PO q24-48h")
        assert out == "用量未確立; 経験的に 10-30 mg/kg 経口 24-48時間毎"

    def test_numbers_inside_phrases_preserved(self):
        out = localize_dosage("5 mg/kg IM q3-5d × 8 injections (loading); then monthly maintenance")
        assert out == "5 mg/kg 筋注 3-5日毎 × 8回注射 (負荷); その後 月1回 維持"

    def test_bilingual_exact_split(self):
        drugs = [
            {
                "id": "x",
                "species_info": {"degu": {"dosage": "Not established in this species 本種では確立されていない"}},
            }
        ]
        filled = fill_missing_dosage_ja(drugs)
        assert filled == 1
        info = drugs[0]["species_info"]["degu"]
        assert info["dosage"] == "Not established in this species"
        assert info["dosage_ja"] == "本種では確立されていない"


class TestFailClosed:
    def test_free_text_returns_none(self):
        # 管理語彙・フレーズに無い自由文はフレーズ拡張後も変換しない
        assert localize_dosage("Consult formulary before use in neonates") is None

    def test_titrate_prose_returns_none(self):
        assert localize_dosage("titrate to effect") is None

    def test_partial_prose_returns_none(self):
        # 用量部分は正しくても、末尾に自由文があれば変換しない
        assert localize_dosage("200 mcg/kg PO/topical; dilute for small birds") is None

    def test_cjk_source_returns_none(self):
        # 原文に日本語が混じっていれば変換対象外
        assert localize_dosage("60-90 mg/m² PO q3週; CBC必須") is None

    def test_empty_and_none(self):
        assert localize_dosage("") is None
        assert localize_dosage(None) is None

    def test_no_translatable_token_returns_none(self):
        # 変換すべき語彙が無い（数値のみ）場合は None
        assert localize_dosage("10 mg/kg") is None


class TestFillMissing:
    def test_does_not_overwrite_existing(self):
        drugs = [
            {
                "id": "x",
                "species_info": {"dog": {"dosage": "10 mg/kg PO q12h", "dosage_ja": "既存の用量"}},
            }
        ]
        filled = fill_missing_dosage_ja(drugs)
        assert filled == 0
        assert drugs[0]["species_info"]["dog"]["dosage_ja"] == "既存の用量"

    def test_fills_missing(self):
        drugs = [{"id": "x", "species_info": {"dog": {"dosage": "10 mg/kg PO q12h"}}}]
        filled = fill_missing_dosage_ja(drugs)
        assert filled == 1
        assert drugs[0]["species_info"]["dog"]["dosage_ja"] == "10 mg/kg 経口 12時間毎"

    def test_skips_unconvertible(self):
        drugs = [{"id": "x", "species_info": {"dog": {"dosage": "Apply to lesion"}}}]
        filled = fill_missing_dosage_ja(drugs)
        assert filled == 0
        assert "dosage_ja" not in drugs[0]["species_info"]["dog"]


class TestModuleIntegration:
    def test_localizer_applied_at_load(self):
        # モジュールロード時に補完が実行され、少なくとも数百件が埋まっている
        assert getattr(drug_dictionary, "_DOSAGE_JA_FILLED", 0) > 100

    def test_localizer_output_never_exposes_english_route_or_freq(self):
        # localize_dosage が返す日本語文字列には、生の投与経路（PO/IM/IV/SC）や
        # 頻度略号（q12h 等）が決して残らないことを、実データ全体で検証する。
        import re

        route_or_freq = re.compile(r"\b(PO|IM|IV|SC|SQ|IO|IP|ICe)\b|\bq\d+-?\d*[hd]\b")
        for d in drug_dictionary.DRUGS:
            for _sp, info in (d.get("species_info") or {}).items():
                dosage = info.get("dosage")
                if not dosage:
                    continue
                out = localize_dosage(dosage)
                if out is not None:
                    assert not route_or_freq.search(out), f"leaked route/freq in {out!r} from {dosage!r}"

    def test_fullwidth_paren_citation_fails_closed_not_partial(self):
        # "q24h（Carpenter）" — a citation glued to the frequency token with
        # full-width parens — used to slip through the digit-preserving path
        # and leak the raw English frequency into the Japanese output. Full-
        # width parens are now tokenized as separators, so the unknown
        # citation word triggers the fail-closed None instead.
        assert localize_dosage("50-100 mg/kg PO q24h（Carpenter）") is None
        # plain conversions are unaffected
        assert localize_dosage("50-100 mg/kg PO q24h") == "50-100 mg/kg 経口 24時間毎"
