"""2026-10 第74弾: チャット精度第49回・キシリトール中毒（チャットDB）・
イゼニベトマブ（レニビア）公開・救急プロトコルのジャンプバー。"""

import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _horse, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound49Parallel:
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


def test_emergency_protocol_jump_bar_sections():
    for key in ("emsteps", "emdrugs", "emmonitor"):
        assert f'data-jump="{key}"' in APP_JS
        assert f"{key}:[" in APP_JS
    assert '"emdrugs","emsteps","emmonitor"]' in APP_JS
