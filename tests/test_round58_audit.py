"""2026-11 第83弾: チャット精度第58回・猫鼻平面SCCのキュレーション・
JA治療欄ワークアップ・テンプレートの検証済み日本語訳（犬猫馬）・馬の誤種テンプレート
（小型哺乳類のメロキシカム用量・小動物の歯科全身麻酔文）の是正・Amodip（猫用アムロジピン）/
KBroVet（臭化カリウム）承認の反映・スマホの戻る操作で直前のタブと位置へ復帰。"""

import json
import sqlite3
import warnings
from pathlib import Path

import pytest

from tests.test_round46_audit import _dog, _horse, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
DB = ROOT / "instance" / "vetdict.db"
WORKUP = "正確な臨床評価（病歴、身体検査、CBC・生化学、画像）から治療方針を決定"
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound58:
    def test_postprandial_bloat_with_distress_is_gdv(self):
        ids, top = _dog("ご飯を食べた後にお腹が膨れて苦しそう")
        assert {"bloating", "labored_breathing"} <= ids, ids
        assert any("胃拡張" in t for t in top), top

    def test_perianal_attention_is_anal_sac(self):
        ids, top = _dog("肛門のまわりを気にしてなめています")
        assert "scooting" in ids and any("肛門" in t for t in top), (ids, top)

    def test_tail_base_pruritus_is_flea_allergy(self):
        ids, top = _dog("しっぽの付け根をかゆがって毛が抜けています")
        assert "flea_signs" in ids and any("ノミ" in t for t in top), (ids, top)

    def test_cold_intolerance_points_to_hypothyroidism(self):
        ids, top = _dog("眠ってばかりで寒がりです")
        assert "cold_intolerance" in ids and top[0] == "甲状腺機能低下症", (ids, top)

    def test_cat_dark_ear_debris_is_ear_mites(self):
        ids, top = _sp("耳が黒く汚れてかゆがっています", "cat")
        assert "ear_discharge" in ids
        assert any(("耳ダニ" in t) or ("外耳" in t) for t in top), top

    def test_cat_distended_lethargic_is_wet_fip(self):
        _, top = _sp("お腹がふくれて元気がありません", "cat")
        assert any("伝染性腹膜炎" in t for t in top), top

    def test_cat_gross_hematuria_and_jaundice_variants(self):
        ids, top = _sp("おしっこが真っ赤です", "cat")
        assert ({"blood_in_urine", "bloody_urine"} & ids) and any(("膀胱" in t) or ("尿" in t) for t in top), top
        ids, _ = _sp("目の色が黄色っぽくて食べません", "cat")
        assert "jaundice" in ids

    def test_cat_nasal_planum_lesion_is_scc(self):
        ids, top = _sp("鼻の上にできものがあります", "cat")
        assert "nasal_planum_lesion" in ids
        assert any("扁平上皮癌" in t for t in top), top

    def test_ferret_abdomen_snake_mites_amphibian_oedema(self):
        _, top = _sp("咳をしてお腹が大きいです", "ferret")
        assert any("心" in t for t in top), top
        ids, _ = _sp("体にダニがいます", "snake")
        assert "visible_mites" in ids
        ids, top = _sp("体がむくんでいます", "amphibian")
        assert "edema" in ids and any(("浮腫" in t) or ("水腫" in t) for t in top), top

    def test_horse_rolling_recumbent_is_colic(self):
        ids, top = _horse("寝転んで起き上がろうとしません")
        assert {"dig_colic_signs", "gen_recumbent"} <= ids
        assert top[0] == "疝痛", top


class TestTreatmentTemplateCuration:
    def test_cat_nasal_planum_scc_not_generic_oncology(self):
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        r = next(x for x in data if x.get("name") == "Feline Squamous Cell Carcinoma (Nasal Planum)")
        assert "紫外線" in r["causes_ja"] and "ホルモン依存性" not in r["prevention_ja"]
        assert "酸化亜鉛" in r["prevention_ja"] and "FeLV" not in r["transmission"]
        assert "nasal_planum_lesion" in r["symptoms"]

    def test_served_db_no_workup_template_on_dog_cat_horse(self):
        if not DB.exists():
            pytest.skip("served DB not built")
        c = sqlite3.connect(DB)
        n = c.execute(
            "select count(*) from diseases where species in ('dog','cat') and treatment_ja like ?",
            (f"%{WORKUP}%",),
        ).fetchone()[0]
        assert n == 0

    def test_served_db_horse_dental_and_exotic_templates_removed(self):
        if not DB.exists():
            pytest.skip("served DB not built")
        c = sqlite3.connect(DB)
        assert not c.execute(
            "select count(*) from diseases where species='horse' and treatment_ja like '%全身麻酔下での歯科処置が必須%'"
        ).fetchone()[0]
        bad = c.execute(
            "select name from diseases where species='horse' and treatment like '%meloxicam 0.2-0.5 mg/kg q24-48h%'"
        ).fetchall()
        assert not bad, bad
        sep = c.execute(
            "select treatment_ja from diseases where species='horse' and name='Sharp Enamel Points'"
        ).fetchone()
        assert sep and "立位鎮静" in sep[0]

    def test_runtime_paths_serve_curated_protocols(self):
        from api.vetdict_api import app

        cl = app.test_client()

        def get(sp):
            j = cl.get(f"/api/health-check/diseases?species={sp}").get_json()
            return {d["name"]: d for d in (j if isinstance(j, list) else j.get("diseases", []))}

        horse = get("horse")
        assert "立位鎮静" in horse["Sharp Enamel Points"]["treatment_ja"]
        assert "NSC" in horse["Polysaccharide Storage Myopathy (PSSM)"]["treatment"]
        cat = get("cat")
        assert WORKUP not in cat["Systemic Hypertension"]["treatment_ja"]
        assert "Amodip" in cat["Systemic Hypertension"]["treatment_ja"]

    def test_horse_library_numerically_consistent(self):
        from scripts.template_elimination.apply_en_treatment_translations import verify
        from scripts.template_elimination.horse_template_treatment_library import HORSE_TREATMENTS

        for name, (en, ja) in HORSE_TREATMENTS.items():
            assert verify(ja, en) is None, name
            assert "Quesenberry" not in en and "0.2-0.5 mg/kg" not in en, name


class TestDrugLabelUpdates:
    def test_amodip_feline_label_and_kbrovet(self):
        from api.drug_dictionary import DRUGS, resolve_drug_reference

        aml = next(d for d in DRUGS if d["id"] == "amlodipine")
        cat = aml["species_info"]["cat"]
        assert "0.125-0.25 mg/kg" in cat["dosage"] and "2.5 kg" in cat["dosage"]
        assert "Amodip" in cat["dosage_ja"] and "国内未承認" in cat["dosage_ja"]
        kbr = next(d for d in DRUGS if d["id"] == "potassium_bromide")
        assert "141-615" in kbr["species_info"]["dog"]["dosage"]
        assert "0.9% NaCl" in kbr["species_info"]["dog"]["notes"]
        for q, want in (("Amodip", "amlodipine"), ("KBroVet", "potassium_bromide"), ("Itrafungol", "itraconazole")):
            r = resolve_drug_reference(q)
            assert (r.get("id") if isinstance(r, dict) else r) == want, q


class TestMobileBackButtonHistory:
    def test_tab_taps_push_history_and_popstate_restores_scroll(self):
        assert "function _recordViewHistory(view,push)" in APP_JS
        assert "history.pushState({vdView:view}" in APP_JS
        assert 'window.addEventListener("popstate"' in APP_JS
        assert "vdY" in APP_JS and 'behavior:"instant"' in APP_JS
        assert APP_JS.count("{focusSearch:true,push:true}") >= 2
        assert "_popstateHandledAt<500" in APP_JS
