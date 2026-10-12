"""2026-10 第67弾: チャット精度第43回・薬品重複統合・新規承認薬3剤・皮膚科テンプレートの種間汚染是正。"""

import json
import sqlite3
import warnings
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
warnings.filterwarnings("ignore")


def _sp(phrase, species, n=5):
    from api.chat.disease_matcher import _match_species_symptoms_to_diseases
    from api.chat.symptom_extractor import _extract_species_symptoms

    ids = _extract_species_symptoms(phrase, species)
    res = _match_species_symptoms_to_diseases(list(ids), species, lang="ja")
    return set(ids), [r.get("name_ja") or "" for r in res[:n]]


def _dog(phrase, n=4):
    from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

    ids = extract_symptoms_from_text(phrase)
    return set(ids), [r.get("name_ja") or "" for r in match_symptoms_to_diseases(ids)[:n]]


class TestChatClinicalAccuracyAuditRound43:
    def test_dog_cloudy_malodorous_urine_is_uti(self):
        ids, top = _dog("おしっこの臭いがきつくて濁っています")
        assert "cloudy_urine" in ids and "膀胱炎" in top[0], top

    def test_dog_fever_joint_pain_is_impa(self):
        ids, top = _dog("発熱があり、関節を痛がって歩きません")
        assert {"fever", "joint_swelling"} <= ids and "IMPA" in top[0], top

    def test_impa_does_not_hijack_bare_fever_or_limping(self):
        _, top = _dog("熱があって元気がありません")
        assert "IMPA" not in top[0], top
        _, top = _dog("後ろ足を引きずっています")
        assert not any("IMPA" in t for t in top[:2]), top

    def test_hiragana_raised_leg(self):
        ids, top = _dog("散歩のあとに足をあげて歩きます")
        assert "limping" in ids and any(k in " ".join(top) for k in ("膝蓋骨", "十字靭帯", "関節")), top

    def test_periocular_swelling(self):
        ids, _ = _dog("目の周りが腫れて、かゆがっています")
        assert "eye_swelling" in ids

    def test_eye_wont_open_is_blepharospasm_and_conjunctivitis_first(self):
        ids, top = _dog("目やにがひどくて目が開かない")
        assert "squinting" in ids and top[0] == "結膜炎", top
        ids, top = _sp("目やにがひどく、目が開きません", "cat")
        assert not ids & {"enlarged_eye", "eye_bulging"}, ids
        assert any("上部呼吸器" in t or "結膜炎" in t or "ヘルペス" in t for t in top[:3]), top

    def test_cat_abdominal_breathing(self):
        ids, top = _sp("お腹で呼吸をしていて、苦しそうです", "cat")
        assert ids & {"labored_breathing", "dyspnea", "difficulty_breathing"}, ids

    def test_cat_miliary_scabs(self):
        _, top = _sp("皮膚にかさぶたがたくさんあり、かゆがります", "cat")
        assert any(k in " ".join(top[:3]) for k in ("ノミ", "アレルギー", "粟粒", "好酸球")), top

    def test_cat_cannot_jump_ranks_oa_not_rare_spinal(self):
        ids, top = _sp("後ろ足がふらつき、高い所へ飛び乗れません", "cat")
        assert "reluctance_to_jump" in ids and "tremors" not in ids, ids
        assert "変形性関節症" in top[:3], top
        _, top = _sp("高い所に飛び乗らなくなりました", "cat")
        assert top[0] == "変形性関節症", top

    def test_guinea_pig_squeal_on_urination(self):
        _, top = _sp("おしっこをするときに鳴きます", "guinea_pig")
        assert any("尿" in t or "膀胱" in t for t in top[:3]), top

    def test_chinchilla_diarrhea_not_hijacked_by_muscle_wasting(self):
        _, top = _sp("下痢をして元気がありません", "chinchilla")
        assert top[0] != "筋萎縮", top

    def test_lizard_bloated_extracts_and_toe_dysecdysis(self):
        ids, _ = _sp("食欲がなく、お腹が膨らんでいます", "lizard")
        assert "abdominal_swelling" in ids, ids
        ids, top = _sp("脱皮した皮が指に残っています", "lizard")
        assert "dysecdysis" in ids and "脱皮不全" in top[0], top

    def test_horse_hot_foreleg_is_hot_hoof_pair(self):
        from api.diagnostic_chat import _extract_equine_symptoms, _match_equine_symptoms_to_diseases

        ids = _extract_equine_symptoms("前足が熱くて立ちたがりません")
        assert {"hoof_heat", "limb_lameness_fore"} <= set(ids), ids
        top = [r.get("name_ja") for r in _match_equine_symptoms_to_diseases(ids)[:3]]
        assert any("蹄葉炎" in t or "蹄膿瘍" in t for t in top), top

    def test_ga_to_mo_variant_only_replaces_particle(self):
        from api.chat.symptom_aliases import SYMPTOM_ALIASES

        assert "鳴きなもらいきむ" not in SYMPTOM_ALIASES
        assert not any("上もる" in k or "痛もる" in k for k in SYMPTOM_ALIASES)
        assert SYMPTOM_ALIASES.get("糞も小さく") == SYMPTOM_ALIASES.get("糞が小さく")

    def test_legacy_impa_name_matches_dog_module(self):
        from api.health_checker import DISEASES
        from api.species import dog_diseases

        legacy = next(d for d in DISEASES if d["id"] == "immune_mediated_polyarthritis")
        names = {(d.get("name") if isinstance(d, dict) else d.name) for d in dog_diseases.DISEASES}
        assert legacy["name_en"] in names


class TestBatch75AndDrugDedup:
    def _d(self, did):
        from api.drug_dictionary import get_drug_by_id

        return get_drug_by_id(did)

    def test_ropinirole_label_and_cat_gate(self):
        d = self._d("ropinirole_ophthalmic")
        dog = d["species_info"]["dog"]
        assert "3.75 mg/m²" in dog["dosage"] and "15 minutes" in dog["dosage"]
        assert "メトクロプラミド" in dog["notes_ja"] and "マロピタント" in dog["notes_ja"]
        assert d["species_info"]["cat"]["safe"] is False
        assert "corrosives" in d["contraindications"]

    def test_simparica_trio_label_and_heartworm_gate(self):
        d = self._d("sarolaner_moxidectin_pyrantel")
        dog = d["species_info"]["dog"]
        for frag in ("1.2 mg/kg", "24 µg/kg", "5 mg/kg", "8 weeks", "1.25 kg"):
            assert frag in dog["dosage"], frag
        assert "フィラリア抗原検査陰性" in dog["notes_ja"]
        assert d["species_info"]["cat"]["safe"] is False

    def test_enflicoxib_weekly_and_washout(self):
        from api.drug_interactions import find_interactions

        d = self._d("enflicoxib")
        dog = d["species_info"]["dog"]
        assert "8 mg/kg" in dog["dosage"] and "4 mg/kg" in dog["dosage"] and "WEEKLY" in dog["dosage"]
        assert "休薬" in dog["notes_ja"]
        assert d["species_info"]["cat"]["safe"] is False
        assert find_interactions(["enflicoxib", "prednisolone"])[0]["severity"] == "contraindicated"
        assert find_interactions(["enflicoxib", "meloxicam"])

    def test_matcher_and_resolver(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        assert "ropinirole_ophthalmic" in [x["id"] for x in find_drugs_in_text("ロピニロール点眼液（クレボー）")]
        assert "enflicoxib" in [x["id"] for x in find_drugs_in_text("エンフリコキシブ（ダクソコックス）")]
        assert "sarolaner_moxidectin_pyrantel" in [x["id"] for x in find_drugs_in_text("シンパリカトリオ")]
        assert resolve_drug_reference("くれぼー") == "ropinirole_ophthalmic"

    def test_duplicate_cards_merged_and_old_ids_resolve(self):
        from api.drug_dictionary import DRUGS, get_drug_by_id

        ids = {d["id"] for d in DRUGS}
        for old, new in (
            ("selamectin_sarolaner_combo", "selamectin_sarolaner"),
            ("scopolamine_butylbromide", "butylscopolamine"),
            ("piroxicam_transitional_cell", "piroxicam_bladder"),
        ):
            assert old not in ids and get_drug_by_id(old)["id"] == new
        assert "rabbit" in get_drug_by_id("butylscopolamine")["species_info"]

    def test_disease_content_links_new_drugs(self):
        from api.drug_dictionary import find_drugs_in_text
        from api.species import dog_diseases

        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        dog = {x["name"]: x for x in data if x["species"] == "Dog"}
        assert "enflicoxib" in [x["id"] for x in find_drugs_in_text(dog["Osteoarthritis"]["treatment_ja"])]
        assert "sarolaner_moxidectin_pyrantel" in [
            x["id"] for x in find_drugs_in_text(dog["Flea Allergy Dermatitis"]["treatment_ja"])
        ]
        choc = next(d for d in dog_diseases.DISEASES if d.get("name") == "Chocolate Toxicosis")
        assert "ropinirole_ophthalmic" in [x["id"] for x in find_drugs_in_text(choc["treatment_ja"])]


class TestFabricatedAndCrossSpeciesContent:
    def test_librela_fabricated_name_gone(self):
        for f in ("diseases_all_species.json", "diseases_comprehensive_enriched.json"):
            assert "ベラジフルフェンプロピル" not in (ROOT / f).read_text(encoding="utf-8")
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        oa = next(x for x in data if x["species"] == "Dog" and x["name"] == "Osteoarthritis")
        assert "ベジンベトマブ（リブレラ" in oa["treatment_ja"]

    def test_json_no_canine_only_drugs_in_derm_template_for_other_species(self):
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        for x in data:
            if x["species"] in ("Dog",):
                continue
            t = x.get("treatment_ja") or ""
            assert "オクラシチニブ（犬専用）。" not in t, (x["species"], x["name"])
            if x["species"] in ("Horse", "Degu"):
                assert "アポキル、サイトポイント" not in t, (x["species"], x["name"])

    def test_non_skin_diseases_lost_derm_workup(self):
        from scripts.template_elimination.fix_derm_template_cross_species import CURATED, DERM_MARKER

        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        byk = {(x["species"], x["name"]): x for x in data}
        for sp, name in (("Snake", "Flagellate Protozoan Infection"), ("Guinea Pig", "Trichobezoar")):
            x = byk.get((sp, name))
            if x:
                assert DERM_MARKER not in (x.get("treatment_ja") or ""), name
        assert "メトロニダゾール" in CURATED[("snake", "Flagellate Protozoan Infection")][0]

    @pytest.mark.skipif(not (ROOT / "instance" / "vetdict.db").exists(), reason="served DB not built")
    def test_served_db_free_of_cross_species_derm_drugs(self):
        c = sqlite3.connect(ROOT / "instance" / "vetdict.db")
        n = c.execute(
            "select count(*) from diseases where species!='dog' and treatment_ja like '%オクラシチニブ（犬専用）%'"
        ).fetchone()[0]
        if c.execute("select count(*) from diseases").fetchone()[0] < 1000:
            pytest.skip("served DB not populated")
        assert n == 0
        row = c.execute(
            "select treatment_ja from diseases where species='snake' and name='Flagellate Protozoan Infection'"
        ).fetchone()
        assert row and "メトロニダゾール" in row[0] and "皮膚生検" not in row[0]


def test_mobile_tap_targets_css():
    css = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    i = css.rindex("第67弾")
    block = css[i:]
    for sel in (".first-visit-coach-close", ".anesthesia-weight-clear", ".chat-mode-btn", ".az-mode-toggle"):
        assert sel in block
    assert "min-height:40px" in block
