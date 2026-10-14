"""2026-10 第70弾: チャット精度第45回・外部寄生虫症の治療テンプレート撲滅・
ブラベクトプラス/ネクスガードプラス公開・犬ノミアレルギー性皮膚炎（チャットDB）。"""

import json
import sqlite3
import warnings
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "instance" / "vetdict.db"
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


class TestChatClinicalAccuracyAuditRound45:
    def test_dog_scooting_hiragana(self):
        ids, top = _dog("お尻をなめて床をすべるように歩いています")
        assert "scooting" in ids and "肛門嚢" in top[0], top

    def test_dog_hind_limp_hiragana(self):
        ids, top = _dog("散歩の後に後ろ足をひきずっています")
        assert ids and any(k in " ".join(top) for k in ("膝蓋", "十字", "関節")), top

    def test_dog_interdigital_mass(self):
        ids, top = _dog("足の指の間にできものができて舐めています")
        assert "paw_redness" in ids and "趾間" in top[0], top

    def test_dog_scleral_redness(self):
        ids, top = _dog("白目の部分が赤くて涙が多いです")
        assert any(k in " ".join(top[:3]) for k in ("結膜炎", "緑内障")), top

    def test_dog_flea_allergy_entry(self):
        ids, top = _dog("しっぽの付け根の毛が抜けてかさぶたがあります")
        assert "flea_signs" in ids and "ノミアレルギー" in top[0], top

    def test_flea_entry_is_complaint_gated(self):
        _, top = _dog("毛が抜けてかゆがっています")
        assert "ノミアレルギー" not in top[0], top

    def test_flea_entry_name_mirrors_dog_module(self):
        from api.health_checker import DISEASES
        from api.species.dog_diseases import DISEASES as MOD

        legacy = next(d for d in DISEASES if d["id"] == "flea_allergy_dermatitis")
        names = {(d["name"] if isinstance(d, dict) else d.name) for d in MOD}
        assert legacy["name_en"] in names

    def test_dog_incontinence_and_neck(self):
        ids, _ = _dog("おしっこが漏れてしまいます")
        assert "incontinence" in ids
        ids, top = _dog("首を触ると痛がって鳴きます")
        assert "neck_pain" in ids and any("椎間板" in t for t in top[:3]), top

    def test_poor_coat_is_not_weight_loss(self):
        from api.chat.symptom_aliases import SYMPTOM_ALIASES

        assert SYMPTOM_ALIASES["毛艶が悪い"] == "poor_coat"

    def test_cat_pu_wording(self):
        ids, top = _sp("水を飲む量が多くて痩せてきて毛艶も悪いです", "cat", 3)
        assert "excessive_thirst" in ids and any(k in " ".join(top) for k in ("腎", "甲状腺", "糖尿")), top

    def test_cat_ear_tip_scc(self):
        ids, top = _sp("耳の先が白くて赤くただれています", "cat", 4)
        assert ids and any(k in " ".join(top) for k in ("扁平上皮癌", "日光")), top

    def test_cat_flea_signs_fall_back(self):
        ids, top = _sp("しっぽの付け根の毛が抜けています", "cat", 4)
        assert any("ノミ" in t for t in top), top

    def test_bird_egg_laying_effort(self):
        ids, top = _sp("卵を産もうとしてずっと力んでいます", "bird", 2)
        assert any(k in " ".join(top) for k in ("卵詰まり", "卵停滞")), top

    def test_ferret_melena_gastric_ulcer(self):
        ids, top = _sp("黒い下痢が出ています", "ferret", 3)
        assert "black_tarry_stool" in ids and any(k in " ".join(top) for k in ("胃潰瘍", "ヘリコバクター")), top

    def test_rabbit_sore_hocks(self):
        _, top = _sp("足の裏の毛が抜けて赤くなっています", "rabbit", 2)
        assert any(k in " ".join(top) for k in ("足底", "ソアホック")), top

    def test_lizard_rubber_jaw_kanji(self):
        ids, top = _sp("後ろ足が弱くて顎がやわらかい", "lizard", 2)
        assert "jaw_softening" in ids and any(k in " ".join(top) for k in ("代謝性骨", "MBD", "栄養性二次")), top


JSON = ROOT / "diseases_all_species.json"
EN_MARK = "Anti-parasitic therapy appropriate to the parasite (fenbendazole"
JA_MARKS = ("同定された寄生虫に応じた適切な駆虫薬", "糞便PCR/直接鏡検/フローテーション法で原因虫種を特定")
ECTO = ("Mite", "Flea", "Mange", "Scabies", "Demodic", "Cheyletiell", "Louse", "Tick ")


class TestEctoparasiteTreatments:
    def test_no_endoparasite_template_on_ectoparasites_in_json(self):
        bad = []
        for d in json.loads(JSON.read_text(encoding="utf-8")):
            if not any(k in d.get("name", "") for k in ECTO):
                continue
            if EN_MARK in (d.get("treatment") or "") or any(m in (d.get("treatment_ja") or "") for m in JA_MARKS):
                bad.append((d["species"], d["name"]))
        assert not bad, bad

    def test_tarantula_mites_never_get_acaricides(self):
        d = next(x for x in json.loads(JSON.read_text(encoding="utf-8")) if x["name"] == "Mite Infestation (Tarantula)")
        assert "lethal" in d["treatment"] and "致死的" in d["treatment_ja"]
        assert "never" in d["treatment"].lower()

    def test_bird_red_mite_no_carbaryl_on_bird(self):
        d = next(x for x in json.loads(JSON.read_text(encoding="utf-8")) if x["name"] == "Red Mite (Dermanyssus)")
        assert "カルバリル5%パウダーの体表散布" not in d["treatment_ja"]

    def test_served_db_clean(self):
        if not DB.exists():
            pytest.skip("served DB not built")
        c = sqlite3.connect(DB)
        n = c.execute(
            "select count(*) from diseases where treatment like ? and (name like '%Mite%' or name like '%Mange%' or name like '%Flea%')",
            (f"%{EN_MARK}%",),
        ).fetchone()[0]
        assert n == 0
        en = c.execute("select pathophysiology from diseases where species='cat' and name='Feline Obesity'").fetchone()
        if en:
            assert "tissue injury, inflammatory response" not in en[0]


class TestBatch77Parasiticides:
    def test_entries_and_label_facts(self):
        from api.drug_dictionary import DRUGS

        idx = {d["id"]: d for d in DRUGS}
        bp = idx["fluralaner_moxidectin_topical"]["species_info"]
        assert bp["cat"]["safe"] and not bp["dog"]["safe"]
        assert (
            "40 mg/kg" in bp["cat"]["dosage"] and "1.2 kg" in bp["cat"]["dosage"] and "6 months" in bp["cat"]["dosage"]
        )
        nx = idx["afoxolaner_moxidectin_pyrantel"]["species_info"]
        assert nx["dog"]["safe"] and not nx["cat"]["safe"]
        assert (
            "2.5 mg/kg" in nx["dog"]["dosage"]
            and "24 µg/kg" in nx["dog"]["dosage"]
            and "8 weeks" in nx["dog"]["dosage"]
        )
        assert "陰性" in nx["dog"]["notes_ja"] or "検査" in nx["dog"]["notes_ja"]

    def test_resolution_without_stealing_single_agents(self):
        from api.drug_dictionary import resolve_drug_reference as r

        assert r("ブラベクトプラス") == "fluralaner_moxidectin_topical"
        assert r("ぶらべくとぷらす") == "fluralaner_moxidectin_topical"
        assert r("ネクスガードプラス") == "afoxolaner_moxidectin_pyrantel"
        assert r("ブラベクト") == "fluralaner"
        assert r("ネクスガード") == "afoxolaner"

    def test_disease_text_links(self):
        from api.drug_dictionary import find_drugs_in_text

        data = {(d["species"], d["name"]): d for d in json.loads(JSON.read_text(encoding="utf-8"))}
        ids = {d["id"] for d in find_drugs_in_text(data[("Cat", "Flea Infestation")]["treatment_ja"])}
        assert "fluralaner_moxidectin_topical" in ids
        ids = {d["id"] for d in find_drugs_in_text(data[("Dog", "Heartworm Disease")]["treatment_ja"])}
        assert "afoxolaner_moxidectin_pyrantel" in ids
