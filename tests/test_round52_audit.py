"""2026-10 第77弾: 避妊後尿失禁（USMI）の新設・グルコン酸カリウム/イマチニブ/ゾレドロン酸の公開・
チャット精度第52回・「← 戻る」で直前にタップしたカード位置へ復帰。"""

import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestUsmiEntry:
    def test_sleeping_leakage_is_usmi(self):
        for phrase in ("寝ている時におしっこが漏れています", "おしっこを我慢できずに漏らしてしまいます"):
            ids, top = _dog(phrase)
            assert "incontinence" in ids and "尿道括約筋" in top[0], (phrase, ids, top)

    def test_neuro_incontinence_stays_neuro(self):
        _, top = _dog("後ろ足が動かなくなっておしっこを漏らします")
        assert "椎間板" in top[0], top
        _, top = _dog("夜鳴きして同じところを回りおしっこを漏らす")
        assert "認知機能" in top[0], top

    def test_legacy_name_mirrors_dog_module_and_prevalence(self):
        from api.health_checker import DISEASES
        from api.species import dog_diseases
        from api.species.prevalence_data import SPECIES_PREVALENCE

        legacy = next(d for d in DISEASES if d["id"] == "usmi")
        module = next(d for d in dog_diseases.DISEASES if d["name"].startswith("Urethral Sphincter"))
        assert legacy["name_en"] == module["name"]
        assert legacy["name_ja"] == module["name_ja"]
        assert SPECIES_PREVALENCE["dog"][module["name"]] == "common"
        for k in ("フェニルプロパノールアミン", "エストリオール", "神経因性膀胱", "尿培養"):
            assert k in module["treatment_ja"], k

    def test_treatment_chips_reach_ppa_and_estriol(self):
        from api.drug_dictionary import find_drugs_in_text
        from api.species import dog_diseases

        module = next(d for d in dog_diseases.DISEASES if d["name"].startswith("Urethral Sphincter"))
        ids = {d["id"] for d in find_drugs_in_text(module["treatment_ja"])}
        assert {"phenylpropanolamine", "estriol"} <= ids, ids


class TestBatch85:
    def test_entries_bilingual_with_doses(self):
        from api.drug_dictionary import _drug_index

        for did in ("potassium_gluconate", "imatinib", "zoledronate"):
            d = _drug_index[did]
            for sp, info in d["species_info"].items():
                assert info["dosage"] and info["dosage_ja"], (did, sp)
                assert info["notes"] and info["notes_ja"], (did, sp)
        assert "2-4 mEq/cat" in _drug_index["potassium_gluconate"]["species_info"]["cat"]["dosage"]
        assert "10 mg/kg" in _drug_index["imatinib"]["species_info"]["dog"]["dosage"]
        z = _drug_index["zoledronate"]["species_info"]["dog"]["dosage"]
        assert "0.1 mg/kg" in z and "15 minutes" in z

    def test_matcher_and_resolver(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        cases = {
            "Potassium gluconate 2-4 mEq/cat PO q12h": "potassium_gluconate",
            "Imatinib mesylate 10 mg/kg PO q24h": "imatinib",
            "zoledronate 0.1 mg/kg IV q28d": "zoledronate",
        }
        for text, did in cases.items():
            assert did in {d["id"] for d in find_drugs_in_text(text)}, text
        # potassium chloride/citrate are not stolen by the new gluconate entry
        assert {d["id"] for d in find_drugs_in_text("Potassium chloride IV 20 mEq/L")} == {"potassium_chloride"}
        for q, did in (("トゥミルK", "potassium_gluconate"), ("グリベック", "imatinib"), ("ゾメタ", "zoledronate")):
            r = resolve_drug_reference(q)
            assert (r.get("id") if isinstance(r, dict) else r) == did, q

    def test_interaction_registry(self):
        from api.drug_interactions import find_interactions

        for a, b in (
            ("imatinib", "toceranib"),
            ("zoledronate", "pamidronate"),
            ("potassium_gluconate", "spironolactone"),
        ):
            hits = find_interactions([a, b])
            assert hits and hits[0]["severity"] == "major", (a, b)


class TestChatClinicalAccuracyAuditRound52:
    def test_greasy_coat_is_malassezia(self):
        ids, top = _dog("毛が脂っぽくてフケが多いです")
        assert "greasy_skin" in ids and "マラセチア" in top[0], (ids, top)

    def test_ear_palpation_pain_is_ear_ddx_not_glaucoma(self):
        ids, top = _dog("耳を触ると痛がって鳴きます")
        assert "pain" not in ids and ids & {"ear_scratching", "head_shaking"}, ids
        assert all("緑内障" not in t for t in top), top

    def test_cat_cloudy_painful_eye_is_ocular(self):
        ids, top = _sp("目が白く濁って痛そうです", "cat")
        assert "eye_pain" in ids and "pain" not in ids, ids
        assert all(any(k in t for k in ("白内障", "緑内障", "ぶどう膜", "角膜", "角結膜", "水晶体")) for t in top), top

    def test_generic_pain_without_eye_signs_unchanged(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = set(_extract_species_symptoms("お腹を触ると痛がります", "cat"))
        assert "eye_pain" not in ids, ids

    def test_cat_spotted_crusts_is_miliary(self):
        ids, top = _sp("皮膚にかさぶたが点々とできて痒がります", "cat")
        assert "miliary_dermatitis" in ids, ids
        assert any("粟粒" in t or "ノミアレルギー" in t for t in top[:2]), top

    def test_cat_folding_pinna_reaches_ear(self):
        ids, top = _sp("耳が折れ曲がってきました", "cat")
        assert ids and any("耳" in t for t in top), (ids, top)


class TestBackNavReturnsToTappedCard:
    def test_history_records_anchor_and_back_uses_it(self):
        assert "_lastNavTrigger" in APP_JS and "function _navReturnAnchor" in APP_JS
        assert "anchor:_navReturnAnchor(_lastNavTrigger)" in APP_JS
        assert ".treatment-drugs-section" in APP_JS
        assert "last.anchor&&last.anchor.isConnected" in APP_JS

    def test_open_disease_across_species_offers_back(self):
        i = APP_JS.index("function openDiseaseAcrossSpecies")
        body = APP_JS[i : i + 1200]
        assert "_pushNavHistory(fromView" in body and '_showBackNav("diseaseBackNav"' in body

    def test_sw_cache_bumped(self):
        sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
        assert int(__import__("re").search(r"vetdict-v(\d+)", sw).group(1)) >= 192
