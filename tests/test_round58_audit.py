"""2026-10 第83弾: チャット精度第58回（耳のべたつき・すりすりスクーティング・黒目の混濁・
尿のキラキラ・肉球亀裂・顎下のぐりぐり・帯下・足底の脱毛・排尿時発声（漢字「時」）・
水様便・尾の痩せ）、モルモット壊血病の歯肉出血フロア＋くる病/VitE欠乏の降格、
猫の嘔吐単独での稀少疾患降格、汎用ワークアップ治療テンプレートの日本語是正
（実行時オーバーレイのマーカー登録）、鑑別チェッカー結果の候補ジャンプ・ストリップ。"""

import json
import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound58:
    def test_sticky_ear_is_otitis(self):
        ids, top = _dog("耳の中がべたべたして臭います")
        assert "ear_discharge" in ids
        assert any("外耳" in t for t in top), top

    def test_surisuri_scooting(self):
        ids, top = _dog("おしりを床にすりすりしています")
        assert "scooting" in ids and "肛門" in top[0], top

    def test_cloudy_black_eye_and_urine_crystals(self):
        ids, top = _dog("目の黒い部分が白くなってきました")
        assert ids and any("白内障" in t for t in top), (ids, top)
        ids, top = _dog("おしっこにキラキラしたものが混じります")
        assert any(("結石" in t) or ("尿" in t) for t in top), top

    def test_paw_crack_not_glaucoma(self):
        ids, top = _dog("足の裏の肉球がひび割れて痛そうです")
        assert "pain" not in ids and "緑内障" not in top, (ids, top)

    def test_submandibular_lumps_are_lymph_nodes(self):
        ids, top = _dog("首の下にぐりぐりしたしこりがたくさんあります")
        assert "swollen_lymph_nodes" in ids and "lumps_bumps" not in ids, ids
        assert any("リンパ" in t for t in top), top

    def test_vaginal_discharge_phrase(self):
        ids, top = _dog("陰部をよく舐めておりものがあります")
        assert any(("子宮" in t) or ("膣" in t) for t in top), (ids, top)

    def test_guinea_pig_bleeding_gums_is_scurvy(self):
        _, top = _sp("歯茎から血が出て歩きたがりません", "guinea_pig")
        assert "壊血" in top[0], top

    def test_guinea_pig_rickets_vitamin_e_demoted(self):
        from api.species.prevalence_data import SPECIES_PREVALENCE

        gp = SPECIES_PREVALENCE["guinea_pig"]
        assert gp["Rickets"] == "rare" and gp["Vitamin E Deficiency"] == "uncommon"

    def test_cat_plain_vomiting_not_dysautonomia(self):
        _, top = _sp("毛玉をよく吐きます", "cat", 3)
        assert not any("自律神経" in t for t in top), top

    def test_rabbit_sole_alopecia_is_sore_hock(self):
        ids, top = _sp("足の裏の毛が薄くなって赤くなっています", "rabbit")
        assert ids & {"foot_sores", "pododermatitis_signs", "foot_lesions"}, ids
        assert any(("足底" in t) or ("ソアホック" in t) for t in top), top

    def test_guinea_pig_kanji_toki_squeal(self):
        ids, top = _sp("おしっこの時にキーキー鳴きます", "guinea_pig")
        assert "squealing_when_urinating" in ids
        assert any(("尿" in t) or ("膀胱" in t) for t in top), top

    def test_bird_watery_and_lizard_thin_tail(self):
        ids, _ = _sp("水のような便が多いです", "bird")
        assert "diarrhea" in ids or ids, ids
        ids, top = _sp("尻尾がやせ細ってきました", "lizard")
        assert "tail_thinning" in ids and any("クリプト" in t for t in top), (ids, top)


class TestWorkupTemplateTreatmentFix:
    MARK = "から治療方針を決定"

    def test_json_curated_japanese(self):
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        by = {(x["species"], x["name"]): x for x in data}
        for key in [
            ("Dog", "Cataracts"),
            ("Dog", "Diabetes Insipidus"),
            ("Cat", "Hypokalemia"),
            ("Cat", "Eclampsia (Puerperal Hypocalcemia)"),
            ("Parakeet", "Red Mite (Dermanyssus)"),
            ("Parrot", "Red Mite (Dermanyssus)"),
            ("Horse", "Polysaccharide Storage Myopathy (PSSM)"),
        ]:
            assert self.MARK not in by[key]["treatment_ja"], key
        assert "超音波水晶体乳化吸引術" in by[("Dog", "Cataracts")]["treatment_ja"]
        assert "enrofloxacin" not in by[("Parakeet", "Red Mite (Dermanyssus)")]["treatment_ja"]
        pssm = by[("Horse", "Polysaccharide Storage Myopathy (PSSM)")]
        assert "GYS1" in pssm["treatment"] and "Quesenberry" not in pssm["treatment"]
        assert "meloxicam 0.2-0.5" not in pssm["treatment"]

    def test_runtime_overlay_marks_workup_template(self):
        from api.species.helpers import _is_template_text

        assert _is_template_text("猫における正確な臨床評価（病歴、身体検査、CBC・生化学、画像）から治療方針を決定。")

    def test_runtime_cat_hypokalemia_is_curated(self):
        import api.species.cat_diseases as c

        d = next(x for x in c.DISEASES if x["name"] == "Hypokalemia")
        assert self.MARK not in (d.get("treatment_ja") or "")
        assert "0.5 mEq/kg/h" in d["treatment_ja"]


class TestCheckerCandidateJumpStrip:
    def test_wired(self):
        assert 'class="chat-cand-jump dx-cand-jump"' in APP_JS
        assert 'data-dx-name="${escapeHtml(nameEn)}"' in APP_JS
        assert 'e.target.closest(".dx-cand-jump-btn")' in APP_JS
        assert "checker_candidate_jump" in APP_JS


class TestCrossSpeciesCanonicalVanishGuard:
    def test_chinchilla_heat_stroke_and_restored_cards_browsable(self):
        from scripts.build_disease_search_index import build_species_entries

        chin = {e["name"] for e in build_species_entries("chinchilla")}
        assert "Heat Stroke" in chin
        assert {"Rectal Prolapse", "Dystocia", "Diabetes Mellitus"} <= chin
        assert "Thermal Burns" in {e["name"] for e in build_species_entries("reptile")}

    def test_no_duplicate_ja_cards_after_restore(self):
        import collections

        idx = json.loads((ROOT / "api" / "data" / "disease_search_index.json").read_text(encoding="utf-8"))
        c = collections.Counter((e["species"], e.get("name_ja")) for e in idx if e.get("name_ja"))
        assert not [k for k, v in c.items() if v > 1]
