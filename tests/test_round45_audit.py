"""2026-10 第70弾: 外部寄生虫・皮膚糸状菌・フェレットフィラリアの汎用駆虫テンプレート撲滅、
パロキセチン/ネクスガードプラス/フェルプレバ公開、チャット精度第45回、
スクロールトップボタンの「検索欄へ戻る」2段階化。"""

import json
import sqlite3
import warnings
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "instance" / "vetdict.db"
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")

TEMPLATE_EN = "Anti-parasitic therapy appropriate to the parasite (fenbendazole"
TEMPLATE_JA = "同定された寄生虫に応じた適切な駆虫薬が必要"


def _sp(phrase, species, n=5):
    from api.chat.disease_matcher import _match_species_symptoms_to_diseases
    from api.chat.symptom_extractor import _extract_species_symptoms

    ids = _extract_species_symptoms(phrase, species)
    res = _match_species_symptoms_to_diseases(list(ids), species, lang="ja")
    return set(ids), [r.get("name_ja") or "" for r in res[:n]]


def _dog(phrase, n=5):
    from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

    ids = extract_symptoms_from_text(phrase)
    return set(ids), [r.get("name_ja") or "" for r in match_symptoms_to_diseases(ids)[:n]]


def _horse(phrase):
    from api.diagnostic_chat import _extract_equine_symptoms

    return set(_extract_equine_symptoms(phrase))


class TestEctoparasiteFungalTemplateElimination:
    @pytest.fixture(scope="class")
    def entries(self):
        return {(e["species"], e["name"]): e for e in json.loads((ROOT / "diseases_all_species.json").read_text())}

    def test_library_entries_carry_no_template(self, entries):
        from scripts.template_elimination.ectoparasite_fungal_treatment_library import CURATED

        for key in CURATED:
            e = entries[key]
            assert TEMPLATE_EN not in (e.get("treatment") or ""), key
            assert TEMPLATE_JA not in (e.get("treatment_ja") or ""), key
            assert "フローテーション法で原因虫種を特定してから駆虫薬" not in (e.get("treatment_ja") or ""), key

    def test_dermatophytoses_are_antifungal_not_antiparasitic(self, entries):
        for sp, name in [
            ("Hamster", "Dermatophytosis (Ringworm)"),
            ("Guinea Pig", "Dermatophytosis (Ringworm)"),
            ("Bird", "Dermatophytosis (Ringworm)"),
            ("Exotic Other", "Hedgehog Ringworm (Trichophyton)"),
            ("Horse", "Coccidioidomycosis"),
        ]:
            en = entries[(sp, name)]["treatment"]
            assert "antiparasitics are not indicated" in en, name
            assert any(k in en for k in ("terbinafine", "itraconazole", "Itraconazole", "Terbinafine")), name

    def test_tarantula_never_gets_acaricides(self, entries):
        for name in ("Mite Infestation (Tarantula)", "Oral Nematodes (Tarantula)"):
            e = entries[("Exotic Other", name)]
            assert "ivermectin" in e["treatment"] and "致死的" in e["treatment_ja"], name
        from api.species import exotic_other_diseases as m

        for d in m.DISEASES:
            if d["name"] in ("Mite Infestation (Tarantula)", "Oral Nematodes (Tarantula)"):
                assert "ivermectin" in d["treatment"] and "Species-appropriate antiparasitic" not in d["treatment"]

    def test_ferret_heartworm_slow_kill(self, entries):
        for name in ("Heartworm Disease", "Heartworm (Dirofilaria)"):
            e = entries[("Ferret", name)]
            assert "melarsomine" in e["treatment"].lower() and "slow-kill" in e["treatment"], name
            assert "メラルソミン" in e["treatment_ja"], name

    def test_chelonian_ivermectin_warning_on_snake_mites(self, entries):
        e = entries[("Reptile", "Snake Mite Infestation (Ophionyssus natricis) - Severe")]
        assert "chelonian" in e["treatment"] and "カメ類" in e["treatment_ja"]

    @pytest.mark.skipif(not DB.exists(), reason="served DB not built")
    def test_served_db_ectoparasite_and_fungal_rows_curated(self):
        c = sqlite3.connect(DB)
        rows = c.execute(
            "select species,name,treatment,treatment_ja from diseases where "
            "name like '%mite%' or name like '%ringworm%' or name like '%dermatoph%' "
            "or name like '%mange%' or (species='ferret' and name like '%heartworm%')"
        ).fetchall()
        assert rows
        for sp, name, t, tj in rows:
            assert TEMPLATE_EN not in (t or ""), (sp, name)
            assert TEMPLATE_JA not in (tj or ""), (sp, name)


class TestBatch77:
    def test_drugs_present_and_bilingual(self):
        from api.drug_dictionary import DRUGS

        idx = {d["id"]: d for d in DRUGS}
        for did in ("paroxetine", "nexgard_plus", "felpreva"):
            d = idx[did]
            for sp, info in d["species_info"].items():
                assert info["dosage"] and info["dosage_ja"], (did, sp)
        assert idx["nexgard_plus"]["species_info"]["cat"]["safe"] is False
        assert idx["felpreva"]["species_info"]["dog"]["safe"] is False
        assert "14.4 mg/kg" in idx["felpreva"]["species_info"]["cat"]["dosage"]
        assert "0.024 mg/kg moxidectin" in idx["nexgard_plus"]["species_info"]["dog"]["dosage"]
        assert "amitraz" in idx["paroxetine"]["contraindications"].lower()

    def test_text_matcher_and_resolver(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        assert "paroxetine" in {d["id"] for d in find_drugs_in_text("代替: パロキセチン0.5-1mg/kg PO q24h")}
        assert resolve_drug_reference("ぱろきせちん") == "paroxetine"
        assert resolve_drug_reference("フェルプレバ") == "felpreva"
        assert resolve_drug_reference("NexGard PLUS") == "nexgard_plus"
        assert resolve_drug_reference("ネクスガード") == "afoxolaner"

    def test_interaction_registry(self):
        from api.drug_interactions import find_interactions

        found = {(i["drug_a"], i["drug_b"]): i["severity"] for i in find_interactions(["paroxetine", "selegiline"])}
        assert found[("paroxetine", "selegiline")] == "contraindicated"

    def test_disease_links(self):
        from api.drug_dictionary import find_drugs_in_text

        entries = {(e["species"], e["name"]): e for e in json.loads((ROOT / "diseases_all_species.json").read_text())}
        assert "felpreva" in {d["id"] for d in find_drugs_in_text(entries[("Cat", "Flea Infestation")]["treatment_ja"])}
        hook = entries[("Dog", "Hookworm Infection")]["treatment_ja"]
        assert TEMPLATE_JA not in hook
        assert "nexgard_plus" in {d["id"] for d in find_drugs_in_text(hook)}


class TestChatClinicalAccuracyAuditRound45:
    def test_dog_pancreatitis_belly_pain(self):
        ids, top = _dog("急にお腹を痛がって、何度も吐いています")
        assert "abdominal_pain" in ids and any("膵炎" in t for t in top[:3]), top

    def test_dog_cushing_pot_belly(self):
        ids, top = _dog("おしっこの量がとても多くて、水ばかり飲みます。お腹がぽっこりしています")
        assert {"excessive_thirst", "bloating"} <= ids and any("クッシング" in t for t in top), top

    def test_dog_ataxia_stumbling_spinal(self):
        ids, top = _dog("後ろ足がふらついて、つまずくことが多くなりました")
        assert "ataxia" in ids and any("椎間板" in t or "変性性脊髄" in t for t in top[:3]), top

    def test_dog_facial_edema_urticaria(self):
        ids, top = _dog("顔がむくんで、目の周りが赤く腫れています")
        assert "facial_swelling" in ids and any("蕁麻疹" in t for t in top[:3]), top

    def test_cat_overgrooming(self):
        ids, top = _sp("毛をむしってお腹がハゲています", "cat")
        assert "excessive_grooming" in ids, ids

    def test_cat_bite_abscess(self):
        ids, top = _sp("顔に傷があって、腫れて熱を持っています", "cat")
        assert any("膿瘍" in t for t in top[:3]), top

    def test_bird_egg_binding_cant_lay(self):
        ids, top = _sp("卵を産めずに、いきんでいます", "bird")
        assert any("卵詰まり" in t or "難産" in t for t in top[:3]), top

    def test_hamster_wet_tail_area(self):
        ids, top = _sp("しっぽのあたりが濡れて元気がありません", "hamster")
        assert "wet_tail" in ids, ids

    def test_ferret_green_slime_ece(self):
        ids, top = _sp("下痢が緑色です", "ferret")
        assert any("カタル性腸炎" in t for t in top[:3]), top

    def test_bird_white_oral_plaques(self):
        ids, _ = _sp("口の中に白い膜があります", "bird")
        assert ids & {"white_patches_in_mouth", "oral_plaques", "oral_lesions"}, ids

    def test_horse_quidding_and_lumps_and_local_heat(self):
        assert "dental_quidding" in _horse("ご飯をこぼして食べるのが遅いです")
        assert "skin_sarcoid" in _horse("皮膚にこぶがたくさんあります")
        assert {"limb_filling", "limb_tendon_heat"} <= _horse("足が腫れて熱を持っています")


def test_scroll_top_button_jumps_to_tab_search_first():
    assert "function _scrollTopLandingTarget()" in APP_JS
    i = APP_JS.index("/* --- Scroll-to-top button with progress ring --- */")
    block = APP_JS[i : i + 4000]
    assert "scrollToAnchor(lt)" in block and "jump_to_search" in block
    assert 'getElementById("cookieConsent")' in block and '"important"' in block
