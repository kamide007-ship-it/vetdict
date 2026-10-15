"""2026-10 第71弾: チャット精度第46回・点耳薬5製品の公開・オスルニア成分誤記の是正・
疾患/薬品へのディープリンク（共有リンク）。"""

import json
import re
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


def _sp(phrase, species, n=3):
    from api.chat.disease_matcher import _match_species_symptoms_to_diseases
    from api.chat.symptom_extractor import _extract_species_symptoms

    ids = _extract_species_symptoms(phrase, species)
    res = _match_species_symptoms_to_diseases(list(ids), species, lang="ja")
    return set(ids), [r.get("name_ja") or "" for r in res[:n]]


def _dog(phrase, n=3):
    from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

    ids = extract_symptoms_from_text(phrase)
    return set(ids), [r.get("name_ja") or "" for r in match_symptoms_to_diseases(ids)[:n]]


def _horse(phrase, n=3):
    from api.diagnostic_chat import _extract_equine_symptoms, _match_equine_symptoms_to_diseases

    ids = _extract_equine_symptoms(phrase)
    return set(ids), [r.get("name_ja") or "" for r in _match_equine_symptoms_to_diseases(ids)[:n]]


class TestChatClinicalAccuracyAuditRound46:
    def test_dog_tartar_halitosis(self):
        ids, top = _dog("歯石がひどくて口がくさいです")
        assert "bad_breath" in ids and "歯周" in top[0], top

    def test_dog_pigmenturia_pale_gums_is_hemolysis(self):
        ids, top = _dog("急に元気がなくなり歯茎が白くおしっこが赤茶色です")
        assert "dark_urine" in ids
        assert any(k in " ".join(top[:2]) for k in ("溶血", "免疫介在")), top

    def test_dog_anal_sac_abscess(self):
        ids, top = _dog("おしりの横が腫れて破れて膿が出ています")
        assert "scooting" in ids and "肛門嚢" in top[0], top

    def test_dog_multiple_neck_lumps_lymphoma(self):
        ids, top = _dog("首にしこりが何個もあります")
        assert "swollen_lymph_nodes" in ids and "リンパ腫" in top[0], top

    def test_dog_enlarged_painful_eye_glaucoma(self):
        _, top = _dog("片方の目が急に大きくなって痛そうで充血しています")
        assert "緑内障" in top[0], top

    def test_cat_skin_twitching_fhs(self):
        ids, top = _sp("背中の皮膚をピクピクさせて急に走り出します", "cat")
        assert "skin_twitching" in ids and any("過敏" in t for t in top), top

    def test_cat_pinnal_jaundice(self):
        ids, top = _sp("嘔吐が続いて食欲がなく耳の内側が黄色っぽい", "cat")
        assert "jaundice" in ids and any(k in " ".join(top) for k in ("肝", "胆管")), top

    def test_cat_ate_scream(self):
        ids, top = _sp("後ろ足をひきずって急に歩けなくなり鳴き叫んでいます", "cat")
        assert "血栓" in top[0], top

    def test_rabbit_ear_crusts_longest_match(self):
        ids, _ = _sp("耳をしきりに掻いて耳の中にかさぶたがたくさん", "rabbit")
        assert "ear_crusting" in ids

    def test_parakeet_unilateral_leg_paralysis(self):
        ids, top = _sp("足が片方動かず腹部が膨れています", "parakeet")
        assert ids and any(k in " ".join(top) for k in ("腎", "腫瘍")), top

    def test_amphibian_chytrid_excessive_shedding(self):
        _, top = _sp("皮膚が白く濁って脱皮が多く元気がありません", "amphibian")
        assert any("ツボカビ" in t for t in top), top

    def test_horse_cough_exercise_intolerance_asthma(self):
        _, top = _horse("咳をして鼻水が出て運動を嫌がります")
        assert "喘息" in top[0], top


class TestBatch79OticProducts:
    def _get(self, i):
        from api.drug_dictionary import DRUGS

        return next(d for d in DRUGS if d["id"] == i)

    def test_label_doses_and_tm_warning(self):
        osurnia = self._get("florfenicol_terbinafine_betamethasone_otic")
        assert "7 days" in osurnia["species_info"]["dog"]["dosage"]
        assert osurnia["species_info"]["cat"]["safe"] is False
        otomax = self._get("gentamicin_betamethasone_clotrimazole_otic")
        assert "4 drops" in otomax["species_info"]["dog"]["dosage"] and "8 drops" in otomax["species_info"]["dog"]["dosage"]
        surolan = self._get("polymyxin_miconazole_prednisolone_otic")
        assert surolan["species_info"]["cat"]["safe"] is True and "5 drops" in surolan["species_info"]["cat"]["dosage"]
        for i in (
            "florfenicol_terbinafine_betamethasone_otic",
            "florfenicol_terbinafine_mometasone_otic",
            "gentamicin_betamethasone_clotrimazole_otic",
            "orbifloxacin_mometasone_posaconazole_otic",
            "polymyxin_miconazole_prednisolone_otic",
        ):
            d = self._get(i)
            assert "鼓膜" in d["species_info"]["dog"]["notes_ja"] and "tympanic" in d["species_info"]["dog"]["notes"]
            assert d["species_info"]["dog"]["dosage_ja"]

    def test_brand_resolution_and_text_chips(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        for q, want in (
            ("オスルニア", "florfenicol_terbinafine_betamethasone_otic"),
            ("ネプトラ", "florfenicol_terbinafine_mometasone_otic"),
            ("オトマックス", "gentamicin_betamethasone_clotrimazole_otic"),
            ("ポサテックス", "orbifloxacin_mometasone_posaconazole_otic"),
            ("スロラン", "polymyxin_miconazole_prednisolone_otic"),
        ):
            r = resolve_drug_reference(q)
            assert (r.get("id") if isinstance(r, dict) else r) == want
        ids = {d["id"] for d in find_drugs_in_text("e.g., Surolan, Otomax, Posatex")}
        assert {"polymyxin_miconazole_prednisolone_otic", "gentamicin_betamethasone_clotrimazole_otic"} <= ids

    def test_components_do_not_chip_combo_products(self):
        from api.drug_dictionary import find_drugs_in_text

        for text in ("ベタメタゾン外用", "モメタゾン点鼻", "クロトリマゾール軟膏"):
            ids = {d["id"] for d in find_drugs_in_text(text)}
            assert not any(i.endswith("_otic") for i in ids), (text, ids)

    def test_osurnia_ingredient_error_fixed(self):
        raw = (ROOT / "diseases_all_species.json").read_text(encoding="utf-8")
        assert "nepafenac/florfenicol" not in raw and "オシミクロ" not in raw
        data = json.loads(raw)
        dog_otitis = next(e for e in data if e.get("species") == "Dog" and e.get("name") == "Ear Infection (Otitis)")
        assert "ベタメタゾン" in dog_otitis["treatment_ja"] and "オスルニア" in dog_otitis["treatment_ja"]


class TestDeepLinks:
    def test_router_and_share_button_wired(self):
        assert "function _parseDeepLinkHash" in APP_JS and "function _handleDeepLinkHash" in APP_JS
        assert re.search(r'else if\(hash\)_handleDeepLinkHash\(hash\)', APP_JS)
        assert "else _handleDeepLinkHash(hash);" in APP_JS
        assert APP_JS.count('class="cross-nav-btn share-link-btn"') == 1
        assert "share-link-btn\" data-kind=\"drug\"" in APP_JS
        assert 'closest(".share-link-btn")' in APP_JS and "navigator.share" in APP_JS

    def test_parse_deep_link_by_node(self):
        import shutil
        import subprocess

        node = shutil.which("node")
        if not node:
            import pytest

            pytest.skip("node not available")
        m = re.search(r"function _parseDeepLinkHash\(hash\)\{.*?\n\}\n", APP_JS, re.S)
        js = (
            "const SPECIES_ICONS={dog:1,cat:1};\n"
            + m.group(0)
            + 'console.log(JSON.stringify([_parseDeepLinkHash("#drug=enrofloxacin"),'
            '_parseDeepLinkHash("#disease=dog:"+encodeURIComponent("Ear Infection (Otitis)")),'
            '_parseDeepLinkHash("#disease=zebra:X"),_parseDeepLinkHash("#drugs"),_parseDeepLinkHash("#drug=%E0")]))'
        )
        out = json.loads(subprocess.run([node, "-e", js], capture_output=True, text=True, check=True).stdout)
        assert out[0] == {"kind": "drug", "id": "enrofloxacin"}
        assert out[1] == {"kind": "disease", "species": "dog", "name": "Ear Infection (Otitis)"}
        assert out[2] is None and out[3] is None and out[4] is None
