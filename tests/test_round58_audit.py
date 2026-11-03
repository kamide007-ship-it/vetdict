"""2026-11 第83弾: チャット精度第58回（エ段＋ます の一段動詞丁寧形正規化・
暑い日の散歩・腹側の擦りつけ・後ろ足で耳を掻く・吐けず・目の横の腫脹＋排膿・
ホットスポット病変描写・動きません・フクロモモンガ Neospora tier）、
馬EEDの英語治療文（日本語のまま配信されていた）、ProHeart 6/12 の用量明細、
薬品→疾患チップ着地時の治療文中の薬品名ハイライト。"""

import json
import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestPoliteNormalizationRound58:
    def test_e_row_masu_forms(self):
        from api.chat.symptom_extractor import normalize_chat_text as n

        assert n("水を飲むとむせます") == "水を飲むとむせる"
        assert n("足が震えます") == "足が震える"
        assert n("おしっこが漏れます") == "おしっこが漏れる"
        assert n("歩けません") == "歩けない"
        assert n("見えませんでした") == "見えなかった"
        assert n("痩せました") == "痩せた"
        assert n("後ろ足が動きません") == "後ろ足が動かない"
        # 五段動詞（ます語幹がイ段）は誤活用しない
        assert n("咳き込みます") == "咳き込みます"

    def test_choking_polite_extracts(self):
        ids, top = _dog("水を飲むとむせます")
        assert "coughing" in ids and top, (ids, top)


class TestChatClinicalAccuracyAuditRound58:
    def test_heat_exposure_no_particle(self):
        ids, top = _dog("暑い日の散歩のあとぐったりしています")
        assert "heat_exposure" in ids and top[0] == "熱中症", (ids, top)

    def test_ventral_rubbing_is_pruritus_not_anal_sac(self):
        ids, _ = _dog("おなかを地面にこすりつけて歩きます")
        assert "itching" in ids and "scooting" not in ids, ids

    def test_ear_scratching_with_hind_leg(self):
        ids, top = _dog("しきりに後ろ足で耳を掻きます")
        assert "ear_scratching" in ids and "外耳" in top[0], (ids, top)

    def test_unproductive_retching_zu_form(self):
        ids, top = _dog("吐こうとしても吐けずお腹が張っています")
        assert "unproductive_retching" in ids and "胃拡張" in top[0], (ids, top)

    def test_periorbital_swelling_with_pus_is_tooth_root_abscess(self):
        ids, top = _dog("目の横が腫れて膿が出ます")
        assert "facial_swelling" in ids, ids
        assert any("歯根膿瘍" in t for t in top[:2]), top

    def test_hot_spot_lesion_description(self):
        _, top = _dog("皮膚が赤く湿ってじゅくじゅくしています")
        assert any("ホットスポット" in t for t in top[:2]), top

    def test_sugar_glider_neospora_demoted(self):
        from api.species.prevalence_data import SPECIES_PREVALENCE

        sg = SPECIES_PREVALENCE["sugar_glider"]
        assert sg["Neosporosis"] == "rare"
        _, top = _sp("後ろ足が動きません", "sugar_glider")
        assert top[0] != "ネオスポラ症", top


class TestHorseEedEnglishTreatment:
    def test_translation_numeric_fidelity(self):
        from api.species.en_treatment_translations import en_treatment_for
        from scripts.template_elimination.apply_en_treatment_translations import verify

        en = en_treatment_for("horse", "Early Embryonic Death (EED) / Early Pregnancy Loss")
        assert en and en.startswith("[Dosing basis]")
        from api.species.equine_diseases import DISEASE_DATABASE

        d = next(x for x in DISEASE_DATABASE if x.name_en.startswith("Early Embryonic Death"))
        assert verify(d.treatment_protocol, en) is None

    def test_japanese_detection_catches_dose_heavy_ja(self):
        from api.species.en_treatment_translations import is_mostly_japanese
        from api.species.equine_diseases import DISEASE_DATABASE

        d = next(x for x in DISEASE_DATABASE if x.name_en.startswith("Early Embryonic Death"))
        assert is_mostly_japanese(d.treatment_protocol)
        # 英文中の日本語製品名の注記だけでは日本語扱いしない
        assert not is_mostly_japanese("Mamushi antivenin (馬血清マムシ抗毒素): 1 vial (6,000 units) IV slowly")


class TestProHeartMonograph:
    def test_concentrations_and_ages(self):
        from api.drug_dictionary import _drug_index, resolve_drug_reference

        dog = _drug_index["moxidectin_injectable"]["species_info"]["dog"]
        assert "3.4 mg/mL" in dog["dosage"] and "10 mg/mL" in dog["dosage"]
        assert "12ヶ月齢以上" in dog["dosage_ja"] and "取り違えない" in dog["dosage_ja"]
        assert resolve_drug_reference("ProHeart 12") == "moxidectin_injectable"
        assert resolve_drug_reference("Prilactone") == "spironolactone"


class TestDrugToDiseaseHighlight:
    def test_wired(self):
        assert "function _highlightDrugMention(root,names)" in APP_JS
        assert 'section:"treatment",highlight:hl' in APP_JS
        assert '_jumpBarOverlay(det.querySelector(".detail-jump-bar"))' in APP_JS
        css = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
        assert "mark.drug-mention-hit" in css

    def test_sw_bumped(self):
        sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
        assert "vetdict-v198" in sw


def test_translation_file_is_valid_json():
    data = json.loads((ROOT / "api" / "data" / "treatment_en_translations.json").read_text(encoding="utf-8"))
    assert "horse|Early Embryonic Death (EED) / Early Pregnancy Loss" in data["entries"]
