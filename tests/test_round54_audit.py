"""2026-10 第79弾: 犬の熱中症（チャットDB・暑熱曝露フラグ）、チャット精度第54回
（腰のふらつき・舌の蒼白・粘液便・猫ざ瘡・高所回避・腹部脱毛・猫の咳）、
2.5%ポリアクリルアミドハイドロゲル（馬OA）、チャット候補カード→治療セクション直接着地。"""

import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestHeatStrokeChatEntry:
    def test_heat_exposure_is_heat_stroke(self):
        ids, top = _dog("暑い日に散歩したらぐったりして呼吸が荒いです")
        assert "heat_exposure" in ids and top[0] == "熱中症", (ids, top)
        _, top = _dog("車の中に置いていたらハアハアして倒れました")
        assert top[0] == "熱中症", top

    def test_no_exposure_keeps_cardiopulmonary_ddx(self):
        _, top = _dog("呼吸が荒くてぐったりしています")
        assert "熱中症" not in top[:3], top
        _, top = _dog("散歩中に急に倒れて意識を失いました")
        assert "熱中症" not in top[:3], top

    def test_name_mirrors_dog_module_and_prevalence(self):
        from api.health_checker import DISEASES
        from api.species import dog_diseases
        from api.species.prevalence_data import SPECIES_PREVALENCE

        legacy = next(d for d in DISEASES if d["id"] == "heat_stroke")
        assert any(m["name"] == legacy["name_en"] for m in dog_diseases.DISEASES)
        assert SPECIES_PREVALENCE["dog"]["Heat Stroke"] == "common"


class TestChatClinicalAccuracyAuditRound54:
    def test_lumbar_ataxia(self):
        ids, top = _dog("歩くときに腰がふらつきます")
        assert "ataxia" in ids and any("椎間板" in t or "ウォブラー" in t for t in top[:2]), (ids, top)

    def test_pale_tongue_and_mucoid_bloody_stool(self):
        ids, _ = _dog("舌が白っぽくてぐったりしています")
        assert "pale_gums" in ids, ids
        ids, top = _dog("うんちに粘液と血がついています")
        assert {"diarrhea", "blood_in_stool"} <= ids and top, (ids, top)

    def test_cat_chin_jump_ventral_alopecia(self):
        ids, top = _sp("顎にぶつぶつができています", "cat")
        assert "chin_swelling" in ids and "にきび" in top[0], (ids, top)
        ids, _ = _sp("高い所に登らなくなりました", "cat")
        assert "reluctance_to_jump" in ids, ids
        ids, top = _sp("お腹の毛が薄くなっています", "cat")
        assert "excessive_grooming" in ids and "心因性" in top[0], (ids, top)

    def test_cat_cough_alone_is_asthma_not_incidental_cyst(self):
        _, top = _sp("咳をしています", "cat")
        assert top[0] == "猫喘息", top


class TestBatch87PolyacrylamideHydrogel:
    def test_monograph_and_resolution(self):
        from api.drug_dictionary import _drug_index, find_drugs_in_text, resolve_drug_reference

        d = _drug_index["polyacrylamide_hydrogel"]
        h = d["species_info"]["horse"]
        assert h["safe"] and "1-2 mL" in h["dosage"] and "1〜2 mL" in h["dosage_ja"]
        assert "化膿性関節炎" in d["contraindications_ja"]
        assert any("Tnibar" in r for r in d["references"])
        assert resolve_drug_reference("アースラミド") == "polyacrylamide_hydrogel"
        ids = [x.get("id") for x in find_drugs_in_text("2.5%ポリアクリルアミドハイドロゲル 1関節あたり1〜2 mL")]
        assert "polyacrylamide_hydrogel" in ids

    def test_horse_oa_treatment_references_it(self):
        import json

        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        oa = next(e for e in data if e.get("species", "").lower() == "horse" and e.get("name") == "Osteoarthritis")
        assert "ポリアクリルアミド" in oa["treatment_ja"] and "polyacrylamide" in oa["treatment"]


def test_chat_cards_offer_direct_treatment_jump():
    assert "function openDiseaseAcrossSpecies(name,species,opts)" in APP_JS
    assert APP_JS.count('class="chat-disease-open chat-disease-treat" data-section="treatment"') == 2
    assert "openBtn.dataset.section?{section:openBtn.dataset.section}" in APP_JS
    body = APP_JS.split("function openDiseaseAcrossSpecies(name,species,opts)", 1)[1][:2500]
    assert 'data-jump="${sec}"' in body and "scrollToAnchor(el,{settle:false})" in body
