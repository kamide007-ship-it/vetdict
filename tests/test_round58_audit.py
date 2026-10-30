"""2026-10 第83弾: チャット精度第58回（スウェイ歩様→股関節形成不全・陰部を舐める→尿路感染・
尾根部を噛む→ノミ・首のしこり語順ゆれ＋リンパ節腫大の包含・猫嘔吐/鳥シックバードの未tier是正）、
クロナゼパム／ベンズニダゾール（referenced-but-absent）、鑑別チェッカー結果の候補ジャンプ。"""

import json
import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
CSS = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound58:
    def test_swaying_gait_is_hip_dysplasia(self):
        ids, top = _dog("歩くときに腰が左右に揺れています")
        assert "swaying_gait" in ids, ids
        assert any(("股関節" in t) or ("脊髄" in t) for t in top), top

    def test_swaying_gait_species_fallback(self):
        ids, _ = _sp("腰を左右に振って歩きます", "cat")
        assert "swaying_gait" not in ids and ids, ids

    def test_dog_vulvar_licking_is_uti(self):
        ids, top = _dog("おしっこの後に陰部をよく舐めます")
        assert "genital_licking" in ids, ids
        assert any(("膀胱" in t) or ("尿" in t) for t in top), top

    def test_cat_perineal_licking_still_surfaces_lower_urinary(self):
        ids, _ = _sp("陰部をずっと舐めています", "cat")
        assert "excessive_grooming" in ids, ids

    def test_tailhead_biting_is_flea(self):
        ids, top = _dog("尻尾の付け根を噛んでいます")
        assert "flea_signs" in ids
        assert any("ノミ" in t for t in top), top

    def test_neck_lump_word_order_subsumes_generic_lump(self):
        ids, top = _sp("しこりが首にあって痩せてきました", "cat", 3)
        assert "lumps" not in ids, ids
        assert any(("リンパ" in t) or ("甲状腺" in t) for t in top), top

    def test_cat_vomiting_rare_entries_demoted(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases

        res = _match_species_symptoms_to_diseases(["vomiting"], "cat", lang="ja")[:3]
        names = [r["name_en"] for r in res]
        assert "Feline Myasthenic Crisis" not in names, names
        assert not any("Key-Gaskell" in n for n in names), names


class TestBatch91ClonazepamBenznidazole:
    def test_present_and_bilingual(self):
        from api.drug_dictionary import DRUGS

        by = {d["id"]: d for d in DRUGS}
        for did in ("clonazepam", "benznidazole"):
            d = by[did]
            dog = d["species_info"]["dog"]
            assert dog["safe"] and dog["dosage"] and dog["dosage_ja"]
            assert d["species_info"]["cat"]["safe"] is False
        assert "taper" in by["clonazepam"]["species_info"]["dog"]["notes"]
        assert "60 days" in by["benznidazole"]["species_info"]["dog"]["dosage"]

    def test_resolution_from_disease_text(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        assert any(d["id"] == "clonazepam" for d in find_drugs_in_text("Myoclonus: clonazepam 0.5 mg/kg PO q8h"))
        assert any(d["id"] == "benznidazole" for d in find_drugs_in_text("Benznidazole 5-10 mg/kg PO q12h"))
        assert resolve_drug_reference("リボトリール") == "clonazepam"
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else data.get("diseases", data)
        dist = [e for e in items if e.get("species") == "Dog" and e.get("name") == "Canine Distemper Encephalitis"]
        assert dist and "クロナゼパム" in dist[0]["treatment_ja"]


class TestCheckerCandidateJump:
    def test_strip_built_and_rebuilt_on_sort(self):
        assert "function _renderCheckerCandJump(contentDiv)" in APP_JS
        assert APP_JS.count("_renderCheckerCandJump(contentDiv);") >= 3
        assert "checker_candidate_jump" in APP_JS
        assert ".checker-cand-jump-btn" in APP_JS

    def test_grid_items_do_not_blow_out_on_mobile(self):
        assert ".panels>*{min-width:0}" in CSS
        assert ".disease-result.chat-card-flash" in CSS

    def test_sw_bumped(self):
        sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
        assert "vetdict-v198" in sw
