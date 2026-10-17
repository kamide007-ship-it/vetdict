"""2026-10 第72弾: チャット精度第47回・カルビマゾール/タシピミジン公開・
薬品詳細のセクション・ジャンプ（動物種別用量/禁忌/相互作用）。"""

import json
import re
import warnings
from pathlib import Path

from tests.test_round46_audit import _dog, _sp

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
warnings.filterwarnings("ignore")


class TestChatClinicalAccuracyAuditRound47:
    def test_dog_hind_ataxia_prefers_spinal_over_orthopedic(self):
        ids, top = _dog("後ろ足がふらついて立ち上がれません")
        assert "ataxia" in ids
        assert any(k in top[0] for k in ("椎間板", "変性性脊髄")), top

    def test_orthopedic_penalty_needs_ataxia(self):
        # 失調の無い跛行主訴は整形外科ddxを維持
        _, top = _dog("後ろ足を引きずって痛がります")
        assert any(k in " ".join(top) for k in ("膝蓋", "十字", "肘")), top

    def test_dog_toe_touching_lameness(self):
        ids, top = _dog("歩くときに足を浮かせて歩いています")
        assert "limping" in ids and any(k in " ".join(top) for k in ("膝蓋", "十字", "肘")), top

    def test_dog_ascites_maps_to_cardiac_hepatic_neoplastic(self):
        ids, top = _dog("おなかに水がたまっているようです")
        assert "ascites" in ids
        assert set(top) <= {"血管肉腫", "拡張型心筋症", "肝臓病"}, top

    def test_dog_painful_trembling_is_ivdd_not_epilepsy(self):
        _, top = _dog("体を触ると痛がって震えています")
        assert "椎間板" in top[0], top
        # 疼痛を伴わない痙攣はてんかん維持
        _, top2 = _dog("痙攣して意識がなくなった")
        assert "てんかん" in top2[0], top2

    def test_dog_worms_from_anus(self):
        ids, top = _dog("おしりから白い虫が出ています")
        assert "worms_in_stool" in ids and any("寄生虫" in t or "条虫" in t for t in top), top

    def test_dog_malodorous_cloudy_urine(self):
        ids, top = _dog("尿のにおいが強くて濁っています")
        assert "cloudy_urine" in ids and "膀胱" in top[0], top

    def test_cat_inappropriate_urination_outside_box(self):
        ids, _ = _sp("トイレの外でおしっこをしてしまいます", "cat")
        assert ids

    def test_rabbit_ear_shaking_cerumen(self):
        ids, top = _sp("耳を振って耳垢がたまっています", "rabbit")
        assert ids and any("耳" in t for t in top), top

    def test_bird_egg_binding_zu_form(self):
        ids, top = _sp("卵が出ずにいきんでいます", "bird")
        assert "egg_binding" in ids and "卵詰まり" in top[0], top

    def test_cat_fever_effusion_is_wet_fip(self):
        _, top = _sp("お腹に水がたまって元気がなく熱があります", "cat", 3)
        assert "伝染性腹膜炎" in top[0], top

    def test_cat_abdominal_distension_not_cryptorchidism(self):
        _, top = _sp("お腹が膨れてきました", "cat", 3)
        assert not any(k in " ".join(top) for k in ("停留精巣", "胃拡張", "脾捻転")), top


class TestBatch81CarbimazoleTasipimidine:
    def _get(self, i):
        from api.drug_dictionary import DRUGS

        return next(d for d in DRUGS if d["id"] == i)

    def test_carbimazole_label_and_safety(self):
        d = self._get("carbimazole")
        cat = d["species_info"]["cat"]
        assert "15 mg" in cat["dosage"] and "10-25 mg" in cat["dosage"] and cat["dosage_ja"]
        assert "STOP" in cat["notes"] and "中止" in cat["notes_ja"]
        assert "6 mg methimazole" in d["mechanism"]

    def test_tasipimidine_dose_and_cat_gate(self):
        d = self._get("tasipimidine")
        assert "30 µg/kg" in d["species_info"]["dog"]["dosage"] and d["species_info"]["dog"]["dosage_ja"]
        assert d["species_info"]["cat"]["safe"] is False

    def test_resolution_and_text_chips(self):
        from api.drug_dictionary import find_drugs_in_text, resolve_drug_reference

        for q, want in (
            ("カルビマゾール", "carbimazole"),
            ("ビダルタ", "carbimazole"),
            ("テッシー", "tasipimidine"),
            ("Isemid", "torsemide"),
            ("torasemide", "torsemide"),
            ("Credelio CAT", "lotilaner"),
        ):
            r = resolve_drug_reference(q)
            assert (r.get("id") if isinstance(r, dict) else r) == want, q
        ids = {d["id"] for d in find_drugs_in_text("Carbimazole: 5 mg PO q8-12h")}
        assert "carbimazole" in ids

    def test_registry_interactions(self):
        from api.drug_interactions import find_interactions

        found = find_interactions(["carbimazole", "methimazole", "tasipimidine", "dexmedetomidine"])
        pairs = {(x["drug_a"], x["drug_b"], x["severity"]) for x in found}
        assert ("carbimazole", "methimazole", "major") in pairs
        assert ("tasipimidine", "dexmedetomidine", "major") in pairs

    def test_noise_phobia_links_new_anxiolytic(self):
        from api.drug_dictionary import find_drugs_in_text

        data = json.loads((ROOT / "diseases_all_species.json").read_text(encoding="utf-8"))
        e = next(x for x in data if x.get("species") == "Dog" and x.get("name") == "Noise Phobia")
        assert "タシピミジン" in e["treatment_ja"] and "Tasipimidine" in e["treatment"]
        assert "tasipimidine" in {d["id"] for d in find_drugs_in_text(e["treatment_ja"])}


class TestDrugDetailJumpBar:
    def test_drug_template_marks_jump_targets(self):
        assert '<dt data-jump="contra">' in APP_JS
        assert '<dt data-jump="interactions">' in APP_JS
        assert 'class="drug-species-title" data-jump="dosage"' in APP_JS
        assert 'querySelectorAll("[data-jump]")' in APP_JS
        assert re.search(r'key==="dosage"\)\{const hl=detail\.querySelector\("\.drug-species-highlight"\)', APP_JS)

    def test_sw_bumped(self):
        sw = (ROOT / "static" / "sw.js").read_text(encoding="utf-8")
        assert int(re.search(r"vetdict-v(\d+)", sw).group(1)) >= 184
