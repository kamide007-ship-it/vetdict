"""2026-11 第83弾: チャット精度第58回（挙上肢位の漢字形・肛門周囲腫脹・腰の沈下・
毛玉の頻回嘔吐・腹部の舐め壊し・膿性眼脂・歯肉腫瘤・肥満猫の多飲→糖尿病・
盲腸便の固着・甲羅の陥凹）、馬・周術期ブランド名の解決、
問診モード最終結果の候補ジャンプ・ストリップ。"""

import re
import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound58:
    def test_kanji_raised_limb_is_orthopedic_not_glaucoma(self):
        ids, top = _dog("散歩中に急にキャンと鳴いて後ろ足を上げました")
        assert "pain" not in ids and "limping" in ids, ids
        assert "緑内障" not in top and any(("膝蓋" in t) or ("十字" in t) for t in top), top

    def test_bare_perianal_swelling(self):
        ids, top = _dog("おしりが腫れて痛がります")
        assert "緑内障" not in top and any("肛門" in t for t in top), (ids, top)

    def test_hindquarter_sinking_is_neurologic(self):
        ids, top = _dog("歩き方がおかしくて腰が落ちています")
        assert "ataxia" in ids
        assert any(("椎間板" in t) or ("脊髄" in t) for t in top), top

    def test_cat_frequent_hairballs(self):
        ids, top = _sp("毛玉をよく吐きます", "cat")
        assert "hairball_retching" in ids, ids
        assert any(("毛球" in t) or ("喘息" in t) for t in top), top

    def test_cat_belly_overgrooming(self):
        ids, top = _sp("お腹を舐めて毛がなくなっています", "cat", 5)
        assert "excessive_grooming" in ids, ids

    def test_rabbit_purulent_eye_discharge(self):
        ids, top = _sp("目から白い膿が出ています", "rabbit")
        assert "eye_discharge" in ids and "abscess" not in ids, ids
        assert "皮下膿瘍" not in top, top

    def test_guinea_pig_joint_pain_chain_reaches_scurvy(self):
        _, top = _sp("食欲がなく関節を痛がって歩きません", "guinea_pig", 3)
        assert any(("壊血" in t) or ("ビタミンC" in t) for t in top), top

    def test_gingival_mass_is_oral_tumor(self):
        ids, top = _dog("歯茎にしこりがあります")
        assert "lumps_bumps" not in ids, ids
        assert "乳腺腫瘍" not in top and any(("口腔" in t) or ("エプーリス" in t) for t in top), top

    def test_obese_polydipsic_cat_is_diabetes(self):
        ids, top = _sp("太っていて水をたくさん飲みます", "cat")
        assert {"weight_gain", "excessive_thirst"} <= ids, ids
        assert top[0] == "糖尿病" or "糖尿" in top[0], top

    def test_rabbit_caked_feces_and_tortoise_shell_pits(self):
        ids, _ = _sp("お尻に糞がこびりついています", "rabbit")
        assert "abnormal_cecotropes" in ids, ids
        ids, top = _sp("甲羅に穴があいて臭いです", "tortoise")
        assert "shell_pitting" in ids
        assert any("甲羅" in t for t in top), top

    def test_cat_jaundice_and_chin_acne(self):
        ids, _ = _sp("体が黄色くなっています", "cat")
        assert "jaundice" in ids
        ids, top = _sp("顎の下が黒くぶつぶつしています", "cat")
        assert "chin_swelling" in ids and top, top


class TestBrandAliasesRound58:
    def test_equine_perioperative_brands_resolve(self):
        from api.drug_dictionary import resolve_drug_reference, search_drugs

        cases = {
            "Torbugesic": "butorphanol",
            "Simbadol": "buprenorphine",
            "Domosedan": "detomidine",
            "Ovuplant": "deslorelin_implant",
            "Strongid": "pyrantel_pamoate",
            "Safe-Guard": "fenbendazole",
            "Zimecterin": "ivermectin",
        }
        for q, did in cases.items():
            assert resolve_drug_reference(q) == did, q
            assert [d["id"] for d in search_drugs(q)][:1] == [did], q


class TestGuidedFinalCandidateJump:
    def test_guided_final_has_jump_strip_and_ranked_cards(self):
        i = APP_JS.index("function guidedRenderFinalResults")
        body = APP_JS[i : APP_JS.index("let drugsLoaded=false", i)]
        assert "chat-cand-jump-btn" in body
        assert 'class="chat-disease-card" data-rank="${i+1}"' in body

    def test_jump_handler_falls_back_to_page_scroll(self):
        i = APP_JS.index('closest(".chat-cand-jump-btn")')
        body = APP_JS[i : i + 1200]
        assert "container.scrollHeight<=container.clientHeight" in body
        assert "scrollToAnchor(card)" in body

    def test_sw_cache_bumped(self):
        sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
        assert int(re.search(r"vetdict-v(\d+)", sw).group(1)) >= 198


class TestDentalTemplateSpecies:
    LEGACY = "高速ダイヤモンドバーで臼歯研磨"

    def test_no_elodont_template_outside_elodont_species(self):
        import json

        from scripts.template_elimination.fallback_generator import ELODONT_SPECIES

        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        bad = [
            (e["species"], e["name"])
            for e in data
            if self.LEGACY in (e.get("treatment_ja") or "")
            and e["species"].lower().replace(" ", "_") not in ELODONT_SPECIES
        ]
        assert not bad, bad

    def test_no_dog_cat_meloxicam_overdose_in_dental_text(self):
        import json

        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        bad = [
            e["name"]
            for e in data
            if e["species"] in ("Dog", "Cat") and "メロキシカム 0.5-1 mg/kg" in (e.get("treatment_ja") or "")
        ]
        assert not bad, bad

    def test_generator_is_species_aware(self):
        from scripts.template_elimination.fallback_generator import dental_lines_ja

        for sp in ("dog", "cat", "horse", "ferret", "lizard", "bird", "tortoise"):
            txt = "\n".join(dental_lines_ja(sp, "X"))
            assert self.LEGACY not in txt and "0.5-1 mg/kg" not in txt, sp
        assert "立位鎮静" in dental_lines_ja("horse", "X")[0]
        assert self.LEGACY in "\n".join(dental_lines_ja("rabbit", "X"))

    def test_cat_oral_curated_treatment_reaches_runtime(self):
        from api.species.helpers import _is_template_text

        assert _is_template_text(
            "猫における口腔腫瘤・エプリスの治療: 原因の鑑別診断に基づく特異的治療。支持療法（輸液・栄養・疼痛管理）。環境管理。定期的なモニタリングと治療調整。"
        )
        import json

        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        eg = next(e for e in data if e["species"] == "Cat" and e["name"] == "Feline Oral Eosinophilic Granuloma")
        assert "メチルプレドニゾロン" in eg["treatment_ja"] and "臼歯" not in eg["treatment_ja"]
