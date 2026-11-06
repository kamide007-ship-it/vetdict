"""2026-11 第83弾: チャット精度第58回（脂肪腫・眼瞼腫瘤のチャットDB新設、肛門を気にする・
腰の揺れ・尿臭・口腔黒色腫瘤・猫の便秘/瞬膜・ウサギ歯ぎしり/乳腺・馬の鼻出血/角膜混濁・猫ATE冷感、
オウム鼻炎tier）、齧歯類用歯科・支持療法テンプレートの種間汚染撲滅（犬猫等へのメロキシカム
0.5-1 mg/kg）、ブロードライン（猫）公開、鑑別結果の候補ジャンプ・ストリップとスマホの結果はみ出し是正。"""

import json
import re
import sqlite3
import warnings
from pathlib import Path

import pytest

from tests.test_round46_audit import _dog, _horse, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
CSS = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
DB = ROOT / "instance" / "vetdict.db"
warnings.filterwarnings("ignore")

_RODENT_MELOX = re.compile(r"メロキシカム\s*0\.5[-–]1(?:\.0)?\s*mg/kg")
_RODENT_DOSE_OK = {"guinea_pig", "degu", "chinchilla", "rabbit", "hamster", "bird", "parrot", "parakeet"}


class TestChatClinicalAccuracyAuditRound58:
    def test_bare_lump_lands_on_lipoma_not_mammary(self):
        ids, top = _dog("胸にしこりがあって大きくなっています")
        assert "lumps_bumps" in ids
        assert top[0] == "脂肪腫", top

    def test_mammary_lump_still_mammary_tumor(self):
        _, top = _dog("乳腺にしこりがあります")
        assert top[0] == "乳腺腫瘍", top

    def test_oral_black_mass_drops_generic_lump(self):
        ids, top = _dog("口の中に黒いできものがあります")
        assert ids == {"oral_mass"}, ids
        assert "口腔内腫瘍" in top[0], top

    def test_eyelid_mass_lands_on_meibomian_adenoma(self):
        ids, top = _dog("まぶたにできものがあります")
        assert ids == {"eyelid_mass"}, ids
        assert top[0] == "眼瞼腫瘤（マイボーム腺腫）", top

    def test_new_legacy_entries_mirror_dog_module(self):
        from api.health_checker import DISEASES
        from api.species.dog_diseases import DISEASES as DOG

        names = {d["name"] for d in DOG}
        for did in ("lipoma", "eyelid_mass"):
            legacy = next(d for d in DISEASES if d["id"] == did)
            assert legacy["name_en"] in names, legacy["name_en"]
        lip = next(d for d in DISEASES if d["id"] == "lipoma")
        assert "FNA" in lip["description_ja"] and "肥満細胞腫" in lip["description_ja"]

    def test_interdigital_mass_not_hijacked_by_lipoma(self):
        _, top = _dog("指の間にできものがあって赤いです")
        assert "趾間" in top[0], top

    def test_anal_attention_ataxia_and_urine_odor(self):
        ids, top = _dog("お尻を気にしてしきりに振り返ります")
        assert "scooting" in ids and "肛門嚢" in top[0], top
        ids, top = _dog("歩くと腰が左右にふれます", 4)
        assert "ataxia" in ids
        assert any(("脊髄" in t) or ("ウォブラー" in t) or ("椎間板" in t) for t in top), top
        ids, top = _dog("おしっこのにおいがきつくて回数が多いです")
        assert "cloudy_urine" in ids and "膀胱炎" in top[0], top

    def test_hematuria_pain_is_dysuria_not_glaucoma(self):
        ids, top = _dog("尿が赤くて痛そうにします")
        assert "pain" not in ids and "blood_in_urine" in ids, ids
        assert "緑内障" not in top, top

    def test_cat_constipation_zu_form_and_third_eyelid(self):
        ids, top = _sp("便が出ずに何度もトイレでいきみます", "cat", 4)
        assert "constipation" in ids, ids
        assert any(("便秘" in t) or ("尿道" in t) or ("巨大結腸" in t) for t in top), top
        ids, top = _sp("目の横の膜が出たままです", "cat")
        assert "third_eyelid_protrusion" in ids, ids

    def test_cat_cold_dragging_hind_limb_is_ate(self):
        ids, top = _sp("後ろ足を引きずって冷たいです", "cat", 2)
        assert {"cold_extremities", "muscle_weakness"} <= ids, ids
        assert all("血栓" in t for t in top), top

    def test_rabbit_bruxism_still_is_gi_stasis(self):
        _, top = _sp("歯ぎしりをしてじっとしています", "rabbit", 1)
        assert top[0] == "消化管うっ滞", top

    def test_rabbit_mammary_swelling(self):
        ids, top = _sp("乳首のあたりが腫れています", "rabbit")
        assert "mammary_swelling" in ids and all("乳腺" in t for t in top[:2]), (ids, top)

    def test_parrot_sneezing_is_rhinitis_not_bordetella(self):
        _, top = _sp("くしゃみと鼻水が出ます", "parrot", 3)
        assert "ボルデテラ感染症" not in top, top

    def test_amphibian_white_peeling_skin_is_chytrid(self):
        ids, top = _sp("皮膚が白っぽくはがれています", "amphibian")
        assert "excessive_shedding" in ids and "ツボカビ" in top[0], (ids, top)

    def test_horse_epistaxis_and_corneal_cloudiness_floors(self):
        _, top = _horse("鼻血が出ています", 3)
        assert top[0] == "運動誘発性肺出血", top
        assert "免疫介在性血小板減少症" not in top[:1]
        _, top = _horse("目が白く濁っています", 1)
        assert top[0] == "表在性角膜潰瘍", top


class TestDentalAndSupportiveTemplateCrossSpecies:
    def test_dental_lines_are_species_appropriate(self):
        from scripts.template_elimination.fallback_generator import dental_lines_ja

        for sp in ("dog", "cat", "ferret", "hedgehog", "horse", "bird", "tortoise", "lizard"):
            text = "".join(dental_lines_ja(sp, "X"))
            assert not _RODENT_MELOX.search(text), sp
            assert "臼歯研磨" not in text and "チモシー" not in text, sp
        assert "臼歯研磨" in "".join(dental_lines_ja("rabbit", "X"))
        assert "立位鎮静" in "".join(dental_lines_ja("horse", "X"))

    def test_non_herbivore_small_mammal_supportive_block(self):
        from scripts.template_elimination.template_content_library import _small_mammal_supportive

        assert "0.2 mg/kg" in _small_mammal_supportive("ferret")
        assert "Critical Care/Recovery" not in _small_mammal_supportive("ferret")
        for sp in ("hedgehog", "sugar_glider"):
            assert "0.1-0.2 mg/kg" in _small_mammal_supportive(sp)
        assert "0.5-1.0 mg/kg" in _small_mammal_supportive("guinea_pig")

    def test_json_dog_cat_oral_entries_are_curated(self):
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        by = {(x["species"], x["name_ja"]): x for x in data}
        pap = by[("Dog", "口腔乳頭腫症")]["treatment_ja"]
        assert "自然退縮" in pap and not _RODENT_MELOX.search(pap)
        eg = by[("Cat", "猫口腔好酸球性肉芽腫")]["treatment_ja"]
        assert "プレドニゾロン" in eg and "臼歯研磨" not in eg
        dip = by[("Cat", "瓜実条虫症")]["treatment_ja"]
        assert "ノミ" in dip and "プラジクアンテル 5 mg/kg" in dip

    @pytest.mark.skipif(not DB.exists(), reason="served DB not built")
    def test_served_db_has_no_rodent_meloxicam_dose_in_other_species(self):
        c = sqlite3.connect(DB)
        rows = c.execute("select species,name_ja,treatment_ja from diseases").fetchall()
        if len(rows) < 1000:
            pytest.skip("served DB not populated")
        bad = [(s, n) for s, n, t in rows if s not in _RODENT_DOSE_OK and _RODENT_MELOX.search(t or "")]
        assert not bad, bad[:10]
        herb = [(s, n) for s, n, t in rows if s in {"dog", "cat", "ferret"} and "繊維質食材（チモシー" in (t or "")]
        assert not herb, herb


class TestBatch91Broadline:
    def test_monograph(self):
        from api.drug_dictionary import _drug_index

        d = _drug_index["fipronil_methoprene_eprinomectin_praziquantel"]
        cat = d["species_info"]["cat"]
        assert cat["safe"] and "0.12 mL/kg" in cat["dosage"] and "0.12 mL/kg" in cat["dosage_ja"]
        assert "7週齢" in cat["notes_ja"]
        assert d["species_info"]["dog"]["safe"] is False
        assert d["species_info"]["rabbit"]["safe"] is False

    def test_resolution_keeps_single_agents(self):
        from api.drug_dictionary import resolve_drug_reference

        assert resolve_drug_reference("ブロードライン") == "fipronil_methoprene_eprinomectin_praziquantel"
        assert resolve_drug_reference("フィプロニル") == "fipronil"
        assert resolve_drug_reference("プラジクアンテル") == "praziquantel"
        assert resolve_drug_reference("カーディシュア") == "pimobendan"
        assert resolve_drug_reference("Synulox") == "amoxicillin_clavulanate"

    def test_cat_tapeworm_chip_resolves(self):
        from api.drug_dictionary import find_drugs_in_text

        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        x = next(x for x in data if x["species"] == "Cat" and x["name_ja"] == "瓜実条虫症")
        ids = {z["id"] if isinstance(z, dict) else z for z in find_drugs_in_text(x["treatment_ja"])}
        assert "fipronil_methoprene_eprinomectin_praziquantel" in ids


class TestCheckerCandidateJumpAndMobileWidth:
    def test_jump_strip_wired(self):
        assert "function _buildDxJumpStrip(" in APP_JS
        assert 'id="dxJumpStrip"' in APP_JS
        assert APP_JS.count("_buildDxJumpStrip(contentDiv)") >= 3  # initial render + both sort paths
        assert ".dx-jump-btn" in APP_JS and "checker_candidate_jump" in APP_JS
        assert "contain:inline-size" in CSS

    def test_panels_grid_items_cannot_blow_out(self):
        assert ".panels>*{min-width:0}" in CSS
