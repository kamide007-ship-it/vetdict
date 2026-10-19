"""2026-10 第73弾: チャット精度第48回・外傷性眼球脱出の新設・シクレソニド吸入（馬）公開・
馬喘息の治療文の誤記是正・疾患詳細ジャンプバーの「関連薬品」チップ。"""

import re
import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _horse, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound48:
    def test_dog_bulging_eye_reaches_proptosis(self):
        ids, top = _dog("目が飛び出しています")
        assert "eye_bulging" in ids and "眼球脱出" in top[0], top

    def test_dog_buphthalmos_still_glaucoma(self):
        # 「目が大きく見える」は牛眼（緑内障）— 外傷性脱出には寄せない
        _, top = _dog("片目が急に赤くて痛そう 目が大きく見える")
        assert "緑内障" in top[0], top

    def test_abdominal_pain_not_contaminated_by_bare_pain(self):
        ids, top = _dog("お腹が痛そう")
        assert ids == {"abdominal_pain"} and "膵炎" in top[0], (ids, top)

    def test_dog_ear_odor_redness(self):
        ids, top = _dog("耳がくさくて赤いです")
        assert ids and "外耳" in top[0], top

    def test_dog_face_rubbing_and_lost_tooth(self):
        ids, _ = _dog("顔を床にこすりつけています")
        assert "itching" in ids
        ids, top = _dog("歯が抜けました")
        assert "歯周" in top[0], top

    def test_cat_ventroflexion(self):
        ids, top = _sp("首を下げたまま歩きます", "cat")
        assert "ventroflexion_of_neck" in ids
        assert any(k in " ".join(top) for k in ("カリウム", "チアミン")), top

    def test_cat_head_shaking_polite_form(self):
        ids, top = _sp("耳を後ろに倒して頭をよく振ります", "cat")
        assert "head_shaking" in ids and any("耳" in t for t in top), top

    def test_cat_cervical_nodule_is_hyperthyroidism(self):
        ids, top = _sp("喉の下にしこりがあります", "cat")
        assert ids == {"palpable_thyroid_nodule"}, ids  # 汎用「しこり」を包含
        assert "甲状腺機能亢進" in top[0], top

    def test_cat_yowling_weight_loss_still_hyperthyroid(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("夜中に大声で鳴く 高齢 痩せてきた", "cat")
        assert "甲状腺機能亢進" in _match_species_symptoms_to_diseases(syms, "cat")[0]["name_ja"]

    def test_cat_ventral_alopecia_is_overgrooming(self):
        ids, _ = _sp("お腹に毛がなくなってしまった", "cat")
        assert "excessive_grooming" in ids

    def test_cat_stomatitis_not_led_by_rare_entries(self):
        _, top = _sp("口内炎がひどくてよだれが出ます", "cat")
        assert any("歯肉口内炎" in t for t in top[:3]), top
        assert not any("電気コード" in t for t in top[:3]), top

    def test_guinea_pig_scurvy_gum_bleeding(self):
        ids, top = _sp("足を引きずって歯茎から血が出ます", "guinea_pig")
        assert "bleeding_gums" in ids and any("壊血病" in t for t in top), top

    def test_bird_excessive_egg_laying(self):
        ids, top = _sp("卵を産みすぎています", "bird")
        assert "excessive_egg_laying" in ids and any("産卵" in t for t in top), top

    def test_lizard_rubber_jaw_kanji(self):
        ids, top = _sp("顎が腫れて柔らかい", "lizard")
        assert "jaw_softening" in ids and any("骨" in t for t in top), top

    def test_dog_tail_base_alopecia_is_flea(self):
        ids, top = _dog("しっぽの付け根に脱毛と黒いブツブツ")
        assert "flea_signs" in ids and "ノミ" in top[0], top

    def test_cat_lip_ulcer(self):
        ids, top = _sp("口の周りがただれています", "cat")
        assert "oral_ulcers" in ids and top, top

    def test_horse_mane_tail_rubbing_is_pruritus(self):
        ids, top = _horse("皮膚がかゆくてたてがみや尾をこすります")
        assert "skin_itching" in ids and top, top

    def test_rabbit_dehydration_not_primary_tier(self):
        from api.species.prevalence_data import SPECIES_PREVALENCE

        assert SPECIES_PREVALENCE["rabbit"]["Dehydration"] == "uncommon"


class TestTraumaticProptosisEntry:
    def test_module_entry_curated(self):
        from api.species.dog_diseases import DISEASES

        d = next(x for x in DISEASES if x["name"] == "Traumatic Proptosis (Globe Prolapse)")
        assert "eye_bulging" in d["symptoms"] and d["urgency"] == "emergency"
        for f in ("treatment_ja", "treatment", "prognosis_ja", "pathophysiology_ja", "causes_ja", "prevention_ja"):
            assert len(d[f]) > 80, f
        assert "押し戻" in d["treatment_ja"] and "瞼板縫合" in d["treatment_ja"]
        assert "対光反射" in d["prognosis_ja"] and "Gilger" in d["pathophysiology"]

    def test_legacy_name_mirrors_module_and_prevalence(self):
        from api.health_checker import DISEASES
        from api.species.prevalence_data import SPECIES_PREVALENCE

        leg = next(x for x in DISEASES if x["id"] == "traumatic_proptosis")
        assert leg["name_en"] == "Traumatic Proptosis (Globe Prolapse)"
        assert SPECIES_PREVALENCE["dog"]["Traumatic Proptosis (Globe Prolapse)"] == "uncommon"

    def test_checkbox_parity(self):
        from api.species.dog_diseases import SYMPTOM_CATEGORIES, SYMPTOM_NAMES, VALID_SYMPTOMS

        assert "eye_bulging" in VALID_SYMPTOMS and "eye_bulging" in SYMPTOM_NAMES
        assert "eye_bulging" in SYMPTOM_CATEGORIES["eyes_ears"]["symptoms"]


class TestBatch82Ciclesonide:
    def test_label_regimen_and_safety(self):
        from api.drug_dictionary import _drug_index

        d = _drug_index["ciclesonide_inhaled"]
        h = d["species_info"]["horse"]
        assert h["safe"] and "343" in h["dosage"] and "8 actuations q12h" in h["dosage"]
        assert "12 actuations q24h" in h["dosage"] and "12噴霧 q24h" in h["dosage_ja"]
        assert "not a bronchodilator" in h["notes"] and "国内未承認" in h["notes_ja"]
        assert d["species_info"]["dog"]["safe"] is False and d["species_info"]["cat"]["safe"] is False

    def test_resolution_and_disease_link(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        assert resolve_drug_reference("アセルボ") == "ciclesonide_inhaled"
        assert resolve_drug_reference("しくれそにど") == "ciclesonide_inhaled"
        ids = [x["id"] if isinstance(x, dict) else x for x in find_drugs_in_text("シクレソニド(Aservo EquiHaler)")]
        assert "ciclesonide_inhaled" in ids

    def test_equine_asthma_text_corrected(self):
        src = (ROOT / "api" / "species" / "equine_diseases.py").read_text(encoding="utf-8")
        assert "Dembexin" not in src
        assert "吸入デキサメタゾン" not in src
        assert src.count("シクレソニド(Aservo EquiHaler") == 2


def test_jump_bar_has_related_drugs_chip():
    assert 'drugs:["💉 関連薬品"' in APP_JS
    assert re.search(r'order=\["treatment","drugs",', APP_JS)
    assert 'key==="drugs"?detail.querySelector(".treatment-drugs-section")' in APP_JS
