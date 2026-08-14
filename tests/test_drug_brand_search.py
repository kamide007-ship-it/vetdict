"""商品名エイリアス検索の回帰テスト（利用者報告バグ: 「バイトリル」検索0件）。

Covers:
- BRAND_NAME_ALIASES 登録簿が search_aliases にマージされ検索で解決されること
- かな・全角半角の入力ゆれ正規化（ひらがな / 半角カナ / 全角英字）
- 別名の衝突監査（別薬品の name/name_ja/別名と正規化後に衝突しないこと）
- /api/drugs ペイロードが search_aliases を配信すること（フロント検索が参照）
- フロントエンド（app.js）の別名検索・0件時UXの配線
"""

import sys
from pathlib import Path

import pytest
from flask import Flask

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.drug_brand_names import BRAND_NAME_ALIASES
from api.drug_dictionary import (
    _DRUG_KEYWORD_INDEX,
    DRUGS,
    _normalize_search_text,
    drug_bp,
    resolve_drug_id,
    search_drugs,
)

APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
MAIN_CSS = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def client():
    app = Flask(__name__)
    app.register_blueprint(drug_bp)
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def _result_ids(query, **kwargs):
    return [d["id"] for d in search_drugs(query, **kwargs)]


class TestBrandNameSearch:
    def test_baytril_resolves_enrofloxacin(self):
        """利用者報告バグの再現ケース: バイトリル → エンロフロキサシン。"""
        assert _result_ids("バイトリル") == ["enrofloxacin"]
        assert _result_ids("Baytril") == ["enrofloxacin"]

    def test_input_variants_normalized(self):
        """ひらがな・半角カナ・全角英字でも一致する。"""
        assert _result_ids("ばいとりる") == ["enrofloxacin"]
        assert _result_ids("ﾊﾞｲﾄﾘﾙ") == ["enrofloxacin"]
        assert _result_ids("Ｂａｙｔｒｉｌ") == ["enrofloxacin"]

    def test_major_brand_names_resolve(self):
        """主要な日本の商品名が正しい薬品に解決される。"""
        expectations = {
            "メタカム": "meloxicam",
            "ドミトール": "medetomidine",
            "アンチセダン": "atipamezole",
            "クラバモックス": "amoxicillin_clavulanate",
            "パナクール": "fenbendazole",
            "ネクスガード": "afoxolaner",
            "プレドニン": "prednisolone",
            "メルカゾール": "methimazole",
            "ピモベハート": "pimobendan",
            "プラビックス": "clopidogrel",
            "ガスター": "famotidine",
            "プリンペラン": "metoclopramide",
            "ケタラール": "ketamine",
            "イソジン": "povidone_iodine",
            "ST合剤": "trimethoprim_sulfa",
        }
        for brand, drug_id in expectations.items():
            ids = _result_ids(brand)
            assert drug_id in ids, f"{brand} → {drug_id} が検索結果に無い（実際: {ids[:5]}）"

    def test_brand_search_respects_category_filter(self):
        """カテゴリフィルタ併用時も商品名検索が機能する。"""
        assert "enrofloxacin" in _result_ids("バイトリル", category="antibiotics")
        assert _result_ids("バイトリル", category="nsaids") == []


class TestBrandRegistryIntegrity:
    def test_all_registry_keys_resolve_to_existing_drugs(self):
        """登録簿のキーが実在の薬品ID（統合後の正規ID含む）に解決される。"""
        drug_ids = {d["id"] for d in DRUGS}
        for drug_id in BRAND_NAME_ALIASES:
            assert resolve_drug_id(drug_id) in drug_ids, f"未知の薬品ID: {drug_id}"

    def test_no_cross_drug_alias_collisions(self):
        """別名が（正規化後に）他薬品の別名・name・name_ja と衝突しない。

        衝突すると検索・治療テキストチップが誤った薬品に解決されうる。
        「デクスドミトール ⊃ ドミトール」のような包含は部分一致検索の仕様として
        許容し、完全一致の衝突のみ禁止する。
        """
        owner: dict[str, str] = {}
        problems = []
        for drug_id, aliases in BRAND_NAME_ALIASES.items():
            canonical = resolve_drug_id(drug_id)
            for alias in aliases:
                norm = _normalize_search_text(alias)
                if norm in owner and owner[norm] != canonical:
                    problems.append((alias, owner[norm], canonical))
                owner[norm] = canonical
        for d in DRUGS:
            for key in (d.get("name", ""), d.get("name_ja", "")):
                norm = _normalize_search_text(key)
                if norm in owner and owner[norm] != d["id"]:
                    problems.append((key, owner[norm], d["id"]))
        assert not problems, f"別名の衝突: {problems}"

    def test_generic_word_brands_stay_excluded(self):
        """一般語と衝突する商品名（プログラム・ランダ等）を索引に入れない。

        治療テキストスキャン（find_drugs_in_text）で「リハビリプログラム」
        「ランダム化試験」等に誤チップが付くのを防ぐ設計判断のガード。
        """
        for banned in ("プログラム", "ランダ"):
            assert banned.lower() not in _DRUG_KEYWORD_INDEX
            for aliases in BRAND_NAME_ALIASES.values():
                assert banned not in aliases

    def test_brand_aliases_reach_keyword_index(self):
        """商品名が治療テキスト→関連薬品チップの索引にも載る。"""
        assert _DRUG_KEYWORD_INDEX.get("バイトリル".lower()) == "enrofloxacin"
        assert _DRUG_KEYWORD_INDEX.get("メタカム".lower()) == "meloxicam"


class TestApiPayload:
    def test_api_drugs_payload_includes_search_aliases(self, client):
        """フロント検索が参照する search_aliases が /api/drugs で配信される。"""
        data = client.get("/api/drugs").get_json()
        enro = next(d for d in data["drugs"] if d["id"] == "enrofloxacin")
        assert "バイトリル" in enro.get("search_aliases", [])

    def test_api_drugs_search_param_matches_brand(self, client):
        """API側 search パラメータでも商品名が一致する。"""
        data = client.get("/api/drugs?search=バイトリル").get_json()
        assert [d["id"] for d in data["drugs"]] == ["enrofloxacin"]


class TestFrontendWiring:
    def test_app_js_normalizes_and_searches_aliases(self):
        """renderDrugList の検索が正規化 + search_aliases 照合を行う配線。"""
        assert "function normalizeDrugSearchText(" in APP_JS
        assert 'normalize("NFKC")' in APP_JS
        assert "_drugMatchesSearch" in APP_JS
        assert "d.search_aliases" in APP_JS

    def test_app_js_zero_result_ux(self):
        """0件時のフィルタ解除ボタンと検索ヒントの配線。"""
        assert "drugClearFiltersBtn" in APP_JS
        assert "drugNoMatchHint" in APP_JS
        assert "drugClearFilters" in APP_JS

    def test_app_js_brand_hit_tag_and_css(self):
        """商品名一致時のタグ表示（なぜヒットしたかの明示）とCSS。"""
        assert "drug-brand-hit" in APP_JS
        assert ".drug-brand-hit" in MAIN_CSS

    def test_placeholder_mentions_brand_search(self):
        """検索プレースホルダが商品名検索可能なことを案内する。"""
        assert "バイトリル" in APP_JS
