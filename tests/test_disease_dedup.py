"""Regression tests for disease de-duplication.

Historically several species modules carried the same disease twice under
slightly different English names ("Xylitol Poisoning" / "Xylitol Toxicosis")
or with a redundant species suffix ("Heat Stroke" / "Heat Stroke - Chinchilla"),
which rendered two identical cards in the disease browser. ``dedupe_disease_list``
collapses those at load time, keeping the entry with the richest content.
"""

import pytest
from flask import Flask

from api.health_checker import health_bp
from api.species.helpers import dedupe_disease_list


def _d(name, name_ja="", **fields):
    d = {"name": name, "name_ja": name_ja}
    d.update(fields)
    return d


class TestDedupeUnit:
    def test_merges_by_english_name_keeps_richer(self):
        items = [
            _d("Myxomatosis", "粘液腫症（別名）", treatment_ja="短い"),
            _d("Myxomatosis", "粘液腫症", treatment_ja="非常に詳細な治療プロトコル" * 10),
        ]
        out = dedupe_disease_list(items)
        assert len(out) == 1
        # richer entry (longer content) is kept
        assert out[0]["name_ja"] == "粘液腫症"

    def test_merges_by_name_ja_across_different_english(self):
        items = [
            _d("Heat Stroke", "熱中症", causes_ja="a"),
            _d("Heat Stroke - Chinchilla", "熱中症", causes_ja="a" * 500),
        ]
        out = dedupe_disease_list(items)
        assert len(out) == 1
        assert out[0]["name"] == "Heat Stroke - Chinchilla"

    def test_keeps_distinct_diseases(self):
        items = [
            _d("Myxomatosis", "粘液腫症"),
            _d("Myxomatosis - Amyxomatous Form", "粘液腫症（無粘液腫型）"),
            _d("Myxomatosis - Respiratory Form", "粘液腫症（呼吸器型）"),
        ]
        out = dedupe_disease_list(items)
        assert len(out) == 3

    def test_transitive_union_three_way(self):
        # A shares english with B; B shares name_ja with C -> all one group
        items = [
            _d("Listeriosis", "リステリア症A", causes_ja="x"),
            _d("Listeriosis", "リステリア症", causes_ja="x" * 100),
            _d("Listeriosis - Chinchilla", "リステリア症", causes_ja="x" * 50),
        ]
        out = dedupe_disease_list(items)
        assert len(out) == 1
        assert out[0]["name_ja"] == "リステリア症"

    def test_preserves_order_of_kept_entries(self):
        items = [
            _d("Alpha", "ア"),
            _d("Beta", "ベ"),
            _d("Alpha", "ア"),  # dup of first
            _d("Gamma", "ガ"),
        ]
        out = dedupe_disease_list(items)
        assert [d["name"] for d in out] == ["Alpha", "Beta", "Gamma"]

    def test_handles_object_entries(self):
        class D:
            def __init__(self, name_en, name_ja, treatment_ja=""):
                self.name_en = name_en
                self.name_ja = name_ja
                self.treatment_ja = treatment_ja

        items = [D("Colic", "疝痛", "short"), D("Colic", "疝痛", "longer detail" * 20)]
        out = dedupe_disease_list(items)
        assert len(out) == 1
        assert out[0].treatment_ja.startswith("longer")

    def test_empty_and_singleton_passthrough(self):
        assert dedupe_disease_list([]) == []
        one = [_d("Solo", "単独")]
        assert dedupe_disease_list(one) == one

    def test_no_change_returns_same_object(self):
        items = [_d("A", "ア"), _d("B", "ビ")]
        assert dedupe_disease_list(items) is items


class TestAcronymBridge:
    """裸の頭字語名エントリ（"HYPP"）と正式名エントリ（"...(HYPP)"）の統合。

    馬モジュールで HYPP/DDSP/PSSM/EOTRH が2枚のカードとして表示されていた
    （2026-08 発見）。裸の頭字語エントリは、その頭字語をサフィックスに持つ
    正式名エントリが種内に一意に存在する場合のみ統合され、正式名側が残る。
    """

    def test_bare_acronym_merges_into_unique_full_name(self):
        items = [
            _d(
                "Hyperkalemic Periodic Paralysis (HYPP)",
                "高カリウム性周期性麻痺(HYPP)",
                causes_ja="SCN4A遺伝子変異" * 10,
            ),
            _d("HYPP", "高カリウム性周期性四肢麻痺", causes_ja="x"),
        ]
        out = dedupe_disease_list(items)
        assert len(out) == 1
        assert out[0]["name"] == "Hyperkalemic Periodic Paralysis (HYPP)"

    def test_full_name_survives_even_when_bare_entry_is_richer(self):
        # 正式名がカードの正準タイトルであり JSON overlay / prevalence のキー。
        # モジュール段階の richness に関わらず正式名側を残す。
        items = [
            _d("HYPP", "高カリウム性周期性四肢麻痺", causes_ja="長い誤テンプレート" * 50),
            _d("Hyperkalemic Periodic Paralysis (HYPP)", "高カリウム性周期性麻痺(HYPP)", causes_ja="x"),
        ]
        out = dedupe_disease_list(items)
        assert len(out) == 1
        assert out[0]["name"] == "Hyperkalemic Periodic Paralysis (HYPP)"

    def test_ambiguous_acronym_never_bridges(self):
        # "(DM)" を糖尿病と変性性脊髄症が共有 → 裸の "DM" はどちらにも統合しない
        items = [
            _d("Diabetes Mellitus (DM)", "糖尿病"),
            _d("Degenerative Myelopathy (DM)", "変性性脊髄症"),
            _d("DM", "ＤＭ"),
        ]
        assert len(dedupe_disease_list(items)) == 3

    def test_mixed_case_short_name_is_not_an_acronym(self):
        # "Ich"（白点病）は頭字語ではないため "(ICH)" と統合しない
        items = [
            _d("Ich", "白点病"),
            _d("Ichthyophthirius (ICH)", "白点病（重症型）"),
        ]
        assert len(dedupe_disease_list(items)) == 2

    def test_served_db_has_no_bare_acronym_duplicates(self):
        import re
        import sqlite3
        from pathlib import Path

        db = Path("instance/vetdict.db")
        if not db.exists():
            import pytest

            pytest.skip("served DB not built")
        conn = sqlite3.connect(db)
        rows = conn.execute("SELECT species, name FROM diseases").fetchall()
        by_sp = {}
        for sp, nm in rows:
            by_sp.setdefault(sp, set()).add(nm)
        offenders = []
        for sp, names in by_sp.items():
            for nm in names:
                m = re.search(r"\(([A-Z][A-Z0-9\-]{2,7})\)\s*$", nm or "")
                if m and m.group(1) in names:
                    offenders.append((sp, nm, m.group(1)))
        assert not offenders, f"bare acronym duplicate cards remain: {offenders}"


class TestDedupeIntegration:
    @pytest.fixture
    def client(self):
        app = Flask(__name__)
        app.register_blueprint(health_bp)
        app.config["TESTING"] = True
        return app.test_client()

    @pytest.mark.parametrize("species", ["dog", "cat", "rabbit", "chinchilla", "degu", "tortoise", "lizard"])
    def test_browser_endpoint_has_no_duplicate_cards(self, client, species):
        resp = client.get(f"/api/health-check/diseases?species={species}")
        assert resp.status_code == 200
        diseases = resp.get_json()["diseases"]
        en_names = [d.get("name", "") for d in diseases if d.get("name")]
        ja_names = [d.get("name_ja", "") for d in diseases if d.get("name_ja")]
        assert len(en_names) == len(set(en_names)), f"duplicate English names in {species}"
        assert len(ja_names) == len(set(ja_names)), f"duplicate Japanese names in {species}"


class TestCrossSpeciesStrip:
    """The strip removes stale cross-species enumeration sentences from visible
    JA fields, but only for species where the clause is not clinically relevant,
    and never touches inline comparative mentions."""

    def test_strips_reptile_potz_block_from_mammal(self):
        from api.species.helpers import strip_cross_species_text

        text = (
            "犬の治療: 抗菌薬エンロフロキサシン 5 mg/kg PO q12h。"
            "支持療法（爬虫類）: 種別POTZ（preferred optimum temperature zone）維持が免疫機能回復の前提条件。"
            "経過観察を継続する。"
        )
        out = strip_cross_species_text(text, "dog")
        assert "支持療法（爬虫類）" not in out
        assert "エンロフロキサシン" in out
        assert "経過観察を継続する。" in out

    def test_keeps_reptile_block_for_reptile(self):
        from api.species.helpers import strip_cross_species_text

        text = "支持療法（爬虫類）: 種別POTZ維持が前提条件。輸液を行う。"
        assert strip_cross_species_text(text, "snake") == text

    def test_strips_cat_hyperthyroid_prevention_from_dog(self):
        from api.species.helpers import strip_cross_species_text

        text = (
            "糖尿病: 肥満予防、定期運動。"
            "甲状腺機能亢進症（猫）: ヨウ素過剰摂取の回避、缶詰食のBPA曝露低減。"
            "クッシング症候群: 定期的臨床評価。"
        )
        out = strip_cross_species_text(text, "dog")
        assert "甲状腺機能亢進症（猫）" not in out
        assert "糖尿病:" in out and "クッシング症候群:" in out

    def test_keeps_inline_cross_species_mention(self):
        # Inline differential mention inside a comma list must NOT be removed.
        from api.species.helpers import strip_cross_species_text

        text = "二次性要因として高血圧、甲状腺機能亢進症（猫）、栄養性、薬剤性が含まれる。"
        assert strip_cross_species_text(text, "dog") == text

    def test_handles_newline_prefixed_clause(self):
        from api.species.helpers import strip_cross_species_text

        text = "抗菌薬投与。\n支持療法（爬虫類）: 種別POTZ維持が前提。\n経過観察。"
        out = strip_cross_species_text(text, "amphibian")
        assert "支持療法（爬虫類）" not in out
        assert "抗菌薬投与。" in out

    def test_never_blanks_a_field(self):
        from api.species.helpers import strip_cross_species_text

        text = "支持療法（爬虫類）: 種別POTZ維持が前提条件。"
        # whole field is the clause -> keep original rather than emit empty
        assert strip_cross_species_text(text, "dog") == text

    def test_no_change_returns_original(self):
        from api.species.helpers import strip_cross_species_text

        text = "犬の糖尿病はインスリン依存性である。"
        assert strip_cross_species_text(text, "dog") is text


class TestSpeciesTagAndSpellingFold:
    """2026-08 audit: ~250 duplicate-card pairs escaped the exact-match rules —
    JA titles differing only by a display-noise species tag ("羽毛嚢胞" vs
    "羽毛嚢胞（鳥）") and EN spelling/plural variants ("Heatstroke" vs
    "Heat Stroke", "Tularaemia" vs "Tularemia")."""

    def test_ja_species_tag_suffix_merges(self):
        items = [
            _d("Feather Cysts", "羽毛嚢胞", treatment_ja="curated protocol " * 20),
            _d("Feather Cyst", "羽毛嚢胞（鳥）", treatment_ja="short"),
        ]
        out = dedupe_disease_list(items)
        assert len(out) == 1
        assert out[0]["name"] == "Feather Cysts"

    def test_ja_clinical_qualifier_never_merges(self):
        # Clinical qualifiers are not species tags — deliberately distinct
        # subtype entries must survive.
        items = [
            _d("Iron Storage Disease (non-hemochromatosis)", "鉄蓄積症"),
            _d("Iron Storage Disease (Hemochromatosis)", "鉄蓄積症（ヘモクロマトーシス）（鳥）"),
        ]
        assert len(dedupe_disease_list(items)) == 2
        items = [
            _d("Heat Stroke", "熱中症"),
            _d("Heat Stroke - Severe", "熱中症（重度）"),
        ]
        assert len(dedupe_disease_list(items)) == 2

    def test_en_spelling_and_plural_fold_merges(self):
        for a, b in [
            ("Heatstroke", "Heat Stroke"),
            ("Tularaemia", "Tularemia"),
            ("Hypoglycaemia", "Hypoglycemia"),
            ("Mammary Tumors", "Mammary Tumor"),
        ]:
            items = [_d(a, "あ", treatment_ja="x" * 100), _d(b, "い", treatment_ja="y")]
            out = dedupe_disease_list(items)
            assert len(out) == 1, f"{a} / {b} must merge"

    def test_en_paren_qualifiers_never_fold(self):
        for a, b in [
            ("Chytridiomycosis (Bd)", "Chytridiomycosis (Bsal)"),
            ("Fracture (Wing)", "Fracture (Leg)"),
            ("Anorexia (Multifactorial)", "Anorexia (Behavioral)"),
        ]:
            items = [_d(a, "あ"), _d(b, "い")]
            assert len(dedupe_disease_list(items)) == 2, f"{a} / {b} must NOT merge"

    def test_template_entry_never_beats_curated_twin(self):
        # The generic-workup boilerplate is longer than many curated protocols;
        # richness must discount it so the curated twin survives.
        template = (
            "【モルモットにおける腸閉塞】 腸閉塞はモルモットにおける正確な臨床評価"
            "（病歴、身体検査、CBC・生化学、画像）から治療方針を決定。 " * 5
        )
        items = [
            _d("Intestinal Obstruction", "腸閉塞（モルモット）", treatment_ja=template),
            _d("Ileus", "腸閉塞", treatment_ja="輸液療法（乳酸リンゲル液 10mL/kg/hr IV/SC）。疼痛管理。"),
        ]
        out = dedupe_disease_list(items)
        assert len(out) == 1
        assert out[0]["name"] == "Ileus"

    def test_served_db_bucked_shin_merged_with_correct_etiology(self):
        import sqlite3
        from pathlib import Path

        db = Path(__file__).resolve().parents[1] / "instance" / "vetdict.db"
        if not db.exists():
            pytest.skip("served DB not built")
        conn = sqlite3.connect(db)
        rows = conn.execute(
            "select name, causes_ja from diseases where species='horse' and name like 'Bucked%'"
        ).fetchall()
        assert len(rows) == 1, f"bucked shin duplicate cards must be merged, got {[r[0] for r in rows]}"
        name, causes = rows[0]
        assert name == "Bucked Shins"
        # Etiology is repetitive-strain remodeling, never the acute external
        # trauma template (falls/bites/traffic accidents).
        assert "反復" in causes
        assert "交通事故" not in causes
