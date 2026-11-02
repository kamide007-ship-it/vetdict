"""2026-11 第83弾: チャット精度第58回（眼瞼腫瘤・猫の砂かき無尿・〜てきません正規化・
リンパ節腫大の包含・馬の膿性鼻汁/鼻孔拡張と腺疫ペア・猫の稀少嘔吐エントリtier）、
メトプロロール/クロナゼパム（referenced-but-absent）、問診最終結果の候補ジャンプ。"""

import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _horse, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound58:
    def test_eyelid_mass_lands_on_eyelid_tumor(self):
        ids, top = _dog("まぶたにできものがあります")
        assert "eyelid_mass" in ids and "lumps_bumps" not in ids, ids
        assert top[0] == "眼瞼腫瘤（マイボーム腺腫）", top

    def test_eyelid_tumor_name_mirrors_dog_module(self):
        from api.health_checker import DISEASES
        from api.species.dog_diseases import DISEASES as DOG

        legacy = next(d for d in DISEASES if d["id"] == "eyelid_tumor")
        assert any(d["name"] == legacy["name_en"] for d in DOG)

    def test_generic_lump_not_hijacked_by_eyelid(self):
        _, top = _dog("お腹にしこりがあります")
        assert "眼瞼腫瘤（マイボーム腺腫）" not in top, top

    def test_polite_te_kimasen_normalised(self):
        from api.chat.symptom_extractor import normalize_chat_text

        assert normalize_chat_text("卵が出てきません") == "卵が出てこない"
        ids, top = _sp("卵が出てきません", "bird")
        assert ids and any("卵" in t or "難産" in t for t in top), (ids, top)

    def test_cat_litter_scratching_nothing_out_is_obstruction(self):
        ids, top = _sp("トイレの砂をかいて何も出ません", "cat", 5)
        assert "straining_to_urinate" in ids, ids
        assert any(("閉塞" in t) or ("尿" in t) or ("膀胱" in t) for t in top), top

    def test_cat_neck_lump_subsumes_generic_lump(self):
        ids, _ = _sp("しこりが首にあります", "cat")
        assert "lumps" not in ids, ids

    def test_horse_purulent_discharge_and_lymph_is_strangles(self):
        ids, top = _horse("鼻から膿が出て顎の下が腫れています")
        assert {"gen_swollen_lymph", "resp_nasal_discharge"} <= ids, ids
        assert top[0] == "腺疫", top

    def test_horse_nostril_flare_extracted(self):
        ids, _ = _horse("呼吸が荒く鼻の穴が広がっています")
        assert {"resp_nostril_flare", "resp_labored_breathing"} <= ids, ids

    def test_cat_rare_vomiting_entries_tiered(self):
        from api.species.prevalence_data import SPECIES_PREVALENCE as P

        cat = P["cat"]
        assert cat["Feline Dysautonomia (Key-Gaskell Syndrome) - Acute"] == "rare"
        assert cat["Feline Myasthenic Crisis"] == "rare"
        _, top = _sp("黄色い液を吐きます", "cat", 3)
        assert not any(("自律神経" in t) or ("筋無力症" in t) for t in top), top


class TestBatch91MetoprololClonazepam:
    def test_present_with_bilingual_dosing(self):
        from api.drug_dictionary import _drug_index as idx

        for did in ("metoprolol", "clonazepam"):
            d = idx[did]
            dog = d["species_info"]["dog"]
            assert dog["safe"] and dog["dosage"] and dog["dosage_ja"], did
        assert idx["clonazepam"]["species_info"]["cat"]["safe"] is False
        assert "Center" in " ".join(idx["clonazepam"]["references"])

    def test_text_matcher_and_resolver(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        assert "metoprolol" in [d["id"] for d in find_drugs_in_text("metoprolol 0.1-0.5 mg/kg PO q12h")]
        assert "clonazepam" in [d["id"] for d in find_drugs_in_text("clonazepam 0.5 mg/kg PO q8h")]
        assert resolve_drug_reference("セロケン") == "metoprolol"
        assert resolve_drug_reference("リボトリール") == "clonazepam"

    def test_beta_blocker_ccb_interaction_registered(self):
        from api.drug_interactions import find_interactions

        for other in ("diltiazem", "verapamil", "atenolol"):
            res = find_interactions(["metoprolol", other])
            assert res and res[0]["severity"] == "major", other


def test_guided_final_results_have_candidate_jump():
    fi = APP_JS.index("function guidedRenderFinalResults(data){")
    body = APP_JS[fi : fi + 8000]
    assert "chat-cand-jump-btn" in body and 'data-rank="${i+1}"' in body
    assert "container.scrollHeight>container.clientHeight" in APP_JS
