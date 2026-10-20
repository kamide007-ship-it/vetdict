"""2026-10 第74弾: チャット精度第49回・キシリトール中毒（チャットDB）・
イゼニベトマブ（レニビア）公開・救急プロトコルのジャンプバー。"""

import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _horse, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound49:
    def test_xylitol_ingestion_rank1(self):
        ids, top = _dog("キシリトールガムを食べてしまいました")
        assert ids == {"xylitol_ingestion"} and top[0] == "キシリトール中毒", (ids, top)

    def test_xylitol_with_tremors_still_toxicosis(self):
        _, top = _dog("キシリトールを食べて震えています")
        assert top[0] == "キシリトール中毒", top

    def test_plain_seizure_not_hijacked(self):
        _, top = _dog("急に痙攣しました")
        assert top[0] == "てんかん", top

    def test_legacy_name_matches_dog_module(self):
        from api.health_checker import DISEASES
        from api.species import dog_diseases

        legacy = next(d for d in DISEASES if d["id"] == "xylitol_poisoning")
        names = {(d.get("name") if isinstance(d, dict) else d.name) for d in dog_diseases.DISEASES}
        assert legacy["name_en"] in names

    def test_gdv_nothing_comes_out_not_negated(self):
        ids, top = _dog("おなかが張っていて吐こうとしても何も出ません")
        assert "unproductive_retching" in ids and "胃拡張" in top[0], (ids, top)

    def test_exertional_dyspnea_reaches_mmvd(self):
        ids, top = _dog("最近散歩に行きたがらず息切れします")
        assert {"exercise_intolerance", "labored_breathing"} <= ids
        assert "僧帽弁" in top[0], top

    def test_walk_refusal_negative_form_extracts(self):
        ids, _ = _dog("散歩に行きたがらない")
        assert "exercise_intolerance" in ids

    def test_bird_tail_wag_breathing(self):
        ids, _ = _sp("尾を振って呼吸しています", "bird")
        assert "tail_bobbing" in ids

    def test_parakeet_leg_paresis_is_renal_tumor_not_splay_leg(self):
        _, top = _sp("足に力が入らず止まり木につかまれません", "parakeet")
        assert any("腎" in t for t in top), top
        assert "開脚症" not in top[0], top

    def test_horse_anhidrosis(self):
        ids, top = _horse("汗をかかなくなりました")
        assert "misc_anhidrosis" in ids and "無汗" in top[0], (ids, top)


class TestBatch83Izenivetmab:
    def test_monograph_label_facts(self):
        from api.drug_dictionary import DRUGS

        d = next(x for x in DRUGS if x["id"] == "izenivetmab")
        dog = d["species_info"]["dog"]
        assert dog["safe"] and "0.05-0.1 mg/kg" in dog["dosage"] and "3 months" in dog["dosage"]
        assert "12" in d["contraindications"] and "pregnant" in d["contraindications"]
        assert "3.46%" in dog["notes"] and "国内未承認" in dog["notes_ja"]
        assert d["species_info"]["cat"]["safe"] is False

    def test_resolves_and_flags_duplicate_anti_ngf(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference
        from api.drug_interactions import find_interactions

        assert resolve_drug_reference("レニビア") == "izenivetmab"
        assert resolve_drug_reference("いぜにべとまぶ") == "izenivetmab"
        assert "izenivetmab" in [x["id"] for x in find_drugs_in_text("イゼニベトマブ（レニビア）")]
        hits = find_interactions(["izenivetmab", "bedinvetmab"])
        assert hits and hits[0]["severity"] == "major"

    def test_dog_oa_treatment_links_izenivetmab(self):
        from api.drug_dictionary import _build_drug_to_diseases_index

        names = [d.get("name") for d in _build_drug_to_diseases_index().get("izenivetmab", [])]
        assert "Osteoarthritis" in names


def test_emergency_protocol_jump_bar_sections():
    for key in ("emsteps", "emdrugs", "emmonitor"):
        assert f'data-jump="{key}"' in APP_JS
        assert f"{key}:[" in APP_JS
    assert '"emdrugs","emsteps","emmonitor"]' in APP_JS
