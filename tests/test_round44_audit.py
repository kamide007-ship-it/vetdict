"""2026-10 第69弾: チャット精度第44回・馬の治療欄（説明文の複写）是正・EMS重複統合・
臨床徴候のカテゴリ・テンプレート是正・ブランド名解決・メタミゾール公開。"""

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


def _horse(phrase, n=3):
    from api.diagnostic_chat import _extract_equine_symptoms, _match_equine_symptoms_to_diseases

    ids = _extract_equine_symptoms(phrase)
    return set(ids), [r.get("name_ja") or "" for r in _match_equine_symptoms_to_diseases(ids)[:n]]


class TestChatClinicalAccuracyAuditRound44:
    def test_dog_petechiae_lands_on_itp(self):
        ids, top = _dog("お腹に赤い点々がたくさん出ています")
        assert "petechiae" in ids and "血小板" in top[0], top

    def test_itp_is_complaint_gated(self):
        _, top = _dog("元気がなくて鼻血が出ました")
        assert "血小板" not in top[0], top

    def test_dog_neck_scream(self):
        ids, top = _dog("首を触ると悲鳴をあげて、頭を下げたまま動きません")
        assert "neck_pain" in ids and any("椎間板" in t for t in top[:3]), top

    def test_dog_regurgitation_polite(self):
        ids, top = _dog("食べたものを未消化のまま戻します")
        assert "regurgitation" in ids and any("巨大食道" in t for t in top), top

    def test_dog_urination_leg_lifting_is_not_lameness(self):
        ids, top = _dog("おしっこが出にくそうで、何度も足をあげています")
        assert "limping" not in ids and ids & {"straining", "frequent_urination"}, ids
        assert any(k in " ".join(top[:3]) for k in ("膀胱炎", "結石", "前立腺")), top

    def test_bare_leg_lifting_still_lameness(self):
        ids, _ = _dog("散歩のあとに足をあげて歩きます")
        assert "limping" in ids

    def test_dog_senior_ataxia_is_spinal_not_epilepsy(self):
        ids, top = _dog("後ろ足の筋肉が落ちて、ふらふらと歩きます。老犬です")
        assert "ataxia" in ids and "tremors" not in ids, ids
        assert "てんかん" not in top[0] and "アジソン" not in top[0], top

    def test_gradual_adverb_stripped(self):
        from api.chat.symptom_extractor import normalize_chat_text

        assert normalize_chat_text("お腹がだんだん大きくなって") == "お腹が大きくなって"

    def test_bird_perch_hiragana_not_self_negated(self):
        ids, top = _sp("足を引きずって止まり木にとまれません", "bird")
        assert "inability_to_perch" in ids, ids

    def test_hamster_cheek_and_chinchilla_patchy(self):
        ids, top = _sp("頬が片方だけ腫れたままです", "hamster")
        assert "cheek_swelling" in ids and any("頬袋" in t for t in top[:3]), top
        ids, _ = _sp("毛がまだらに抜けています", "chinchilla")
        assert ids

    def test_cat_corneal_surface_cloudiness(self):
        ids, top = _sp("目の表面が白っぽくなって、涙が出ています", "cat")
        assert "corneal_cloudiness" in ids and any("角膜" in t for t in top[:3]), top

    def test_rabbit_mammary_area(self):
        ids, _ = _sp("乳腺のあたりにしこりがあります", "rabbit")
        assert ids


class TestEquineRound44:
    def test_strangles_fever_lymph_pair(self):
        _, top = _horse("下顎が腫れて膿が出て、熱があります")
        assert any("腺疫" in t for t in top), top

    def test_tendon_heat_pair(self):
        ids, top = _horse("前足の腱が腫れて熱を持っています")
        assert {"limb_tendon_swelling", "limb_tendon_heat"} <= ids
        assert any("屈腱" in t for t in top), top

    def test_foal_bruxism_ptyalism(self):
        _, top = _horse("歯ぎしりをして、よだれを垂らしています")
        assert "胃潰瘍" in top[0], top

    def test_weight_loss_is_dental_or_parasites(self):
        _, top = _horse("体重が減ってきました")
        assert set(top[:2]) & {"内部寄生虫感染", "不正咬合"}, top

    def test_thrush_back_pain_dark_urine_vocab(self):
        assert "hoof_thrush" in _horse("蹄の裏から悪臭がして黒い汁が出ます")[0]
        assert "body_back_pain" in _horse("背中を触ると嫌がります")[0]
        assert "body_dark_urine" in _horse("おしっこの色が赤茶色です")[0]

    def test_ems_single_entry_with_obesity_findings(self):
        import api.species.equine_diseases as eq

        ems = [d for d in eq.DISEASE_DATABASE if "Metabolic Syndrome" in d.name_en]
        assert len(ems) == 1, [d.name_en for d in ems]
        f = set(ems[0].associated_findings)
        assert {"body_fat_deposits", "body_neck_crest", "hoof_laminitis_signs"} <= f
        assert not f & {"gen_weight_loss", "body_hirsutism"}  # PPID signs
        assert "輸液" not in ems[0].treatment_protocol and "肝性脳症" not in ems[0].treatment_protocol
        _, top = _horse("ゆっくり体重が増えて首の上が太く、蹄葉炎になりました")
        assert "メタボリック" in top[0], top

    def test_ems_prevalence_key_resolves(self):
        from api.species.prevalence_data import SPECIES_PREVALENCE

        assert SPECIES_PREVALENCE["horse"].get("Equine Metabolic Syndrome") == "common"


class TestHorseTreatmentNotDescriptionCopy:
    def test_json_horse_treatment_ja_is_not_description(self):
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        bad = [
            r["name"]
            for r in data
            if r.get("species") == "Horse"
            and r.get("treatment_ja")
            and r.get("description_ja")
            and r["treatment_ja"][:30] == r["description_ja"][:30]
        ]
        assert not bad, bad

    def test_laminitis_and_influenza_have_treatment(self):
        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        by = {r["name"]: r for r in data if r.get("species") == "Horse"}
        assert "ACVIM" in by["Laminitis"]["treatment_ja"] or "蹄" in by["Laminitis"]["treatment_ja"]
        assert "メタミゾール" in by["Equine Influenza"]["treatment_ja"]
        assert "metamizole" in by["Equine Influenza"]["treatment"]
        assert "ヨード" in by["Thrush"]["treatment_ja"]

    def test_runtime_horse_thrush_treatment_is_treatment(self):
        import api.species.equine_diseases as eq

        d = next(d for d in eq.DISEASE_DATABASE if d.name_en == "Thrush")
        assert d.treatment_protocol[:30] != d.description_ja[:30]

    @pytest.mark.skipif(not DB.exists() or DB.stat().st_size < 1_000_000, reason="served DB not built")
    def test_served_db_horse_treatment_not_description_copy(self):
        c = sqlite3.connect(DB)
        n = c.execute(
            "select count(*) from diseases where species='horse' and treatment_ja!='' "
            "and substr(treatment_ja,1,30)=substr(description_ja,1,30)"
        ).fetchone()[0]
        assert n == 0


class TestClinicalSignsCategoryTemplate:
    def test_runtime_grounding_replaces_other_disease_listing(self):
        from api.health_checker import _ground_missing_supplementary_fields

        item = {
            "clinical_signs_ja": "鳥における糖尿病の臨床徴候はホルモン異常または代謝障害の種類により特異的パターンを示す。クッシング症候群: ...",
            "clinical_signs": "Clinical signs follow the specific hormonal or metabolic disturbance. Addison's disease: ...",
            "symptoms_display": [
                {"name_ja": "多飲", "name_en": "Polydipsia"},
                {"name_ja": "体重減少", "name_en": "Weight loss"},
            ],
            "diagnosis": "x",
            "diagnosis_ja": "x",
        }
        _ground_missing_supplementary_fields(item, "bird")
        assert "クッシング" not in item["clinical_signs_ja"] and "多飲" in item["clinical_signs_ja"]
        assert "Addison" not in item["clinical_signs"] and "Polydipsia" in item["clinical_signs"]

    def test_curated_signs_untouched(self):
        from api.health_checker import _ground_missing_supplementary_fields

        item = {
            "clinical_signs_ja": "キュレート済み",
            "clinical_signs": "curated",
            "diagnosis": "x",
            "diagnosis_ja": "x",
        }
        _ground_missing_supplementary_fields(item, "dog")
        assert item["clinical_signs_ja"] == "キュレート済み"

    @pytest.mark.skipif(not DB.exists() or DB.stat().st_size < 1_000_000, reason="served DB not built")
    def test_served_db_template_mostly_eliminated(self):
        c = sqlite3.connect(DB)
        n = c.execute(
            "select count(*) from diseases where clinical_signs_ja like '%ホルモン異常または代謝障害の種類により特異的パターン%'"
            " or clinical_signs_ja like '%分布パターンが診断に有用%'"
        ).fetchone()[0]
        assert n < 30, n


class TestBrandAndMetamizole:
    @pytest.mark.parametrize(
        "brand,drug_id",
        [
            ("セレニア", "maropitant"),
            ("Cerenia", "maropitant"),
            ("ブラベクト", "fluralaner"),
            ("れぼりゅーしょん", "selamectin"),
            ("フロントライン", "fipronil"),
            ("アトピカ", "cyclosporine"),
            ("クレデリオ", "lotilaner"),
            ("ジコータル", "desoxycorticosterone"),
            ("ソレンシア", "frunevetmab"),
            ("リブレラ", "bedinvetmab"),
            ("ドルモセダン", "detomidine"),
            ("ボンキャット", "pregabalin"),
            ("スルピリン", "metamizole"),
            ("じぴろん", "metamizole"),
        ],
    )
    def test_brand_resolves_in_interaction_checker(self, brand, drug_id):
        from api.drug_dictionary import resolve_drug_reference

        assert resolve_drug_reference(brand) == drug_id

    def test_metamizole_monograph(self):
        from api.drug_dictionary import DRUGS, find_drugs_in_text

        d = next(x for x in DRUGS if x["id"] == "metamizole")
        si = d["species_info"]
        assert "30 mg/kg" in si["horse"]["dosage"] and "12-hour" in si["horse"]["dosage"]
        assert si["dog"]["safe"] and "agranulocytosis" in si["dog"]["notes"]
        assert si["cat"]["safe"] and "hypersalivation" in si["cat"]["notes"].lower()
        for sp in si.values():
            assert sp["dosage"] and sp["dosage_ja"] and sp["notes_ja"]
        ids = [x.get("id") if isinstance(x, dict) else x for x in find_drugs_in_text("解熱にスルピリン 30 mg/kg IV")]
        assert "metamizole" in ids

    def test_metamizole_registry_interactions(self):
        from api.drug_interactions import find_interactions

        pairs = {(x["drug_a"], x["drug_b"], x["severity"]) for x in find_interactions(["metamizole", "acepromazine"])}
        assert ("metamizole", "acepromazine", "major") in pairs

    def test_bonqat_feline_label_dose(self):
        from api.drug_dictionary import DRUGS

        cat = next(x for x in DRUGS if x["id"] == "pregabalin")["species_info"]["cat"]
        assert "5 mg/kg" in cat["notes"] and "Bonqat" in cat["notes"] and "ボンキャット" in cat["notes_ja"]


class TestHorseRuntimeTreatmentTemplates:
    def test_runtime_uses_curated_json_over_module_category_template(self):
        import api.species.equine_diseases as eq

        by = {d.name_en: d for d in eq.DISEASE_DATABASE}
        assert "エピネフリン" in by["Anaphylaxis"].treatment_protocol
        assert "KCl" in by["Hypokalemia"].treatment_protocol
        assert "セレン" in by["Selenium Deficiency"].treatment_protocol
        assert "輸液療法(カリウム補充" not in by["Selenium Deficiency"].treatment_protocol
        assert "蹄壁" in by["White Line Disease"].treatment_protocol

    def test_no_horse_category_treatment_template_shared_widely(self):
        import collections

        import api.species.equine_diseases as eq

        c = collections.Counter(d.treatment_protocol[:50] for d in eq.DISEASE_DATABASE)
        assert c.most_common(1)[0][1] <= 3, c.most_common(3)
