"""犬の停留精巣が疾患DBで見つからない問題の回帰テスト（利用者報告）。

2つの独立したバグがあった:
1. **UIカテゴリ誤分類**: classifyDisease（app.js）の infectious 正規表現 `crypto`
   （クリプトコッカス用）が「**Crypto**rchidism」に部分一致し、停留精巣が
   「カテゴリで探す」で〈感染症〉に収容され〈生殖器〉に存在しなかった。
   同型の部分一致バグ: Dy**skin**esia→皮膚、No**cardi**osis→循環器、
   Dacryo**cystit**is→泌尿器、Gall**bladder**→泌尿器。
2. **治療文の性別・種別取り違え**: fallback_generator の reproductive テンプレート
   （卵停滞・卵管脱・OHE・鳥1-3 IU/羽）が雄犬・雄猫の停留精巣と哺乳類の
   雌性生殖器疾患にスタンプされていた。猫モジュールは病態生理も
   「停留精巣は腫瘍性疾患である（癌遺伝子…）」という誤った腫瘍ボイラープレートだった。
"""

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")

MAMMALS = {
    "dog",
    "cat",
    "horse",
    "rabbit",
    "hamster",
    "guinea pig",
    "guinea_pig",
    "chinchilla",
    "ferret",
    "hedgehog",
    "sugar glider",
    "sugar_glider",
    "degu",
}


def _overlay_entries():
    return json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))


class TestTreatmentSexSpeciesMismatch:
    def test_no_avian_egg_binding_treatment_on_mammals(self):
        """哺乳類の treatment_ja に鳥の卵詰まりテンプレート（IU/羽・卵停滞）が無い。"""
        offenders = []
        for e in _overlay_entries():
            sp = (e.get("species") or "").lower()
            tj = e.get("treatment_ja") or ""
            if sp in MAMMALS and ("IU/羽" in tj or "卵停滞" in tj):
                offenders.append((sp, e.get("name")))
        assert not offenders, f"哺乳類に鳥用生殖器テンプレートが残存: {offenders}"

    def test_cryptorchidism_treatment_is_male_specific(self):
        """犬・猫の停留精巣の treatment_ja が精巣摘出プロトコルである（OHE/卵巣でない）。"""
        for want_sp in ("dog", "cat"):
            e = next(
                x
                for x in _overlay_entries()
                if (x.get("species") or "").lower() == want_sp and x.get("name") == "Cryptorchidism"
            )
            tj = e.get("treatment_ja") or ""
            assert "精巣摘出" in tj or "去勢" in tj, f"{want_sp}: 精巣摘出プロトコルが無い"
            for bad in ("卵停滞", "卵巣子宮", "OHE", "IU/羽"):
                assert bad not in tj, f"{want_sp}: 雌・鳥用の文言が残存: {bad}"

    def test_cat_module_pathophysiology_not_oncology_boilerplate(self):
        """猫モジュールの停留精巣 pathophysiology_ja が腫瘍ボイラープレートでない。"""
        src = (ROOT / "api" / "species" / "cat_diseases.py").read_text(encoding="utf-8")
        i = src.find('"name": "Cryptorchidism"')
        block = src[i : i + 3000]
        assert "癌遺伝子" not in block, "停留精巣に腫瘍性疾患ボイラープレートが残存"
        assert "鼠径管" in block, "発生異常としての正しい病態記述が無い"

    def test_cryptorchidism_all_fields_curated_and_clean(self):
        """犬・猫の停留精巣は全臨床フィールドが疾患固有で、雌/鳥/腫瘍テンプレ汚染が無い。

        利用者要望「しっかりと記載」: clinical_signs は「子宮蓄膿・乳腺炎・難産・
        妊娠中毒症の徴候」という雌用カテゴリ文、EN の causes/pathophysiology/
        prevention/diagnosis は感染症/腫瘍/雌生殖器ボイラープレートだった。
        """
        bad_markers = (
            "子宮蓄膿",
            "Pyometra",
            "卵停滞",
            "IU/羽",
            "乳腺炎",
            "難産",
            "Dystocia",
            "oestrus",
            "癌遺伝子",
            "neoplastic diseases involves",
            "infectious (bacterial",
            "requiring veterinary evaluation",
        )
        fields = (
            "description",
            "description_ja",
            "causes",
            "causes_ja",
            "pathophysiology",
            "pathophysiology_ja",
            "prevention",
            "prevention_ja",
            "clinical_signs",
            "clinical_signs_ja",
            "treatment",
            "treatment_ja",
            "diagnosis",
            "diagnosis_ja",
            "prognosis",
            "prognosis_ja",
        )
        for want_sp in ("dog", "cat"):
            e = next(
                x
                for x in _overlay_entries()
                if (x.get("species") or "").lower() == want_sp and x.get("name") == "Cryptorchidism"
            )
            for f in fields:
                v = e.get(f) or ""
                assert v, f"{want_sp}.{f} が空"
                for b in bad_markers:
                    assert b not in v, f"{want_sp}.{f} にテンプレ汚染: {b!r}"
            # 疾患固有の核心記述
            assert "セルトリ" in (e.get("pathophysiology_ja") or "")
            assert "Sertoli" in (e.get("pathophysiology") or "")

    def test_dog_module_entry_fully_curated(self):
        """犬モジュールの停留精巣エントリが疾患固有の日英記載＋推奨検査を持つ。"""
        src = (ROOT / "api" / "species" / "dog_diseases.py").read_text(encoding="utf-8")
        i = src.find('"name": "Cryptorchidism"')
        block = src[i : i + 6000]
        for marker in ("INSL3", "精巣導帯", "セルトリ細胞腫", "recommended_tests", "hCG/GnRH"):
            assert marker in block, f"犬モジュールに {marker} が無い"
        for bad in ("Multifactorial etiology including infectious", "tissue injury, inflammatory response"):
            assert bad not in block, f"犬モジュールに汎用テンプレが残存: {bad!r}"

    def test_fallback_generator_male_repro_guard(self):
        """fallback_generator が雄性生殖器疾患に卵停滞テンプレートを生成しない。"""
        from scripts.template_elimination.fallback_generator import _class_specific_lines

        male = "\n".join(_class_specific_lines("dog", "reproductive", "停留精巣（陰睾）"))
        assert "精巣摘出" in male or "去勢" in male
        for bad in ("卵停滞", "OHE", "IU/羽", "卵巣子宮"):
            assert bad not in male, f"雄性疾患に雌用文言: {bad}"
        # 哺乳類の雌性疾患: 卵停滞・鳥用量は出さず難産表現
        mammal_f = "\n".join(_class_specific_lines("hamster", "reproductive", "子宮平滑筋腫"))
        assert "IU/羽" not in mammal_f and "卵停滞" not in mammal_f
        assert "難産" in mammal_f
        # 産卵動物は卵停滞の文言を維持
        avian_f = "\n".join(_class_specific_lines("bird", "reproductive", "卵管炎"))
        assert "卵停滞" in avian_f


class TestCategoryClassifierWiring:
    def test_two_pass_name_first_classification(self):
        """classifyDisease が疾患名優先の2パス分類になっている。"""
        assert "DISEASE_CAT_MATCH_ORDER" in APP_JS
        assert 'const nameText=(d.name||"")+" "+(d.name_ja||"")' in APP_JS
        # 名前パスは MATCH_ORDER、説明文パスは表示順（DISEASE_CAT_ORDER）
        assert "for(const catId of DISEASE_CAT_MATCH_ORDER)" in APP_JS
        body = APP_JS[APP_JS.index("function classifyDisease") :][:1500]
        assert "DISEASE_CAT_ORDER" in body

    def test_substring_collision_regex_fixes(self):
        """部分一致バグを起こした正規表現トークンが修正されている。"""
        cats = APP_JS[APP_JS.index("const DISEASE_CATEGORIES=") :][:6000]
        # crypto（bare）は Cryptorchidism に誤マッチした → 全綴りのみ
        assert "cryptococc" in cats and "cryptospor" in cats
        assert not re.search(r"\|crypto\|", cats), "bare crypto が復活している"
        # skin は Dyskinesia に誤マッチした → 語境界付き
        assert r"\bskin" in cats
        # cystit は Dacryocystitis に、bladder は Gallbladder に誤マッチした
        assert r"\bcystit" in cats
        assert "(?:^|[^l])bladder" in cats
        # nocardia は Nocardiosis（-osis形）を取りこぼした
        assert "nocardi|" in cats or "nocardi/" in cats

    def test_reproductive_keyword_covers_cryptorchid(self):
        """生殖器カテゴリの正規表現が cryptorchid を含む（停留精巣の受け皿）。"""
        m = re.search(r"reproductive:\{[^}]*keywords:/([^/]+)/", APP_JS)
        assert m and "cryptorchid" in m.group(1)


class TestServedCryptorchidism:
    @pytest.fixture(scope="class")
    def client(self):
        from api.vetdict_api import app

        app.config["TESTING"] = True
        with app.test_client() as c:
            yield c

    def test_dog_cryptorchidism_served_with_male_treatment(self, client):
        """配信APIで犬の停留精巣が男性器プロトコル付きで取得できる（利用者報告ケース）。"""
        data = client.get("/api/health-check/diseases?species=dog").get_json()
        d = next(x for x in data["diseases"] if x.get("name") == "Cryptorchidism")
        assert "停留精巣" in (d.get("name_ja") or "")
        tj = d.get("treatment_ja") or ""
        assert "精巣摘出" in tj or "去勢" in tj
        assert "卵停滞" not in tj and "IU/羽" not in tj

    def test_cross_species_search_finds_cryptorchidism(self, client):
        """横断検索「停留精巣」が犬を含む複数種でヒットする。"""
        data = client.get("/api/diseases?q=%E5%81%9C%E7%95%99%E7%B2%BE%E5%B7%A3").get_json()
        items = data.get("diseases") or data.get("results") or []
        species = {(i.get("species") or "").lower() for i in items}
        assert "dog" in species, f"犬がヒットしない: {species}"
