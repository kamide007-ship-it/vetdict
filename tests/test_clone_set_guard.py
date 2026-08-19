"""Regression tests for the clone-set matching guard (2026-08 audit).

Clinician directive: common presentations must not be steered toward obscure
"difficult" diseases. An old enrichment run stamped one copy-pasted symptom
set onto whole blocks of supplementary diseases (47 unrelated rabbit diseases
sharing one set, 27 amphibian, 43 parakeet …), so obscure diseases surfaced
for everyday complaints while their real presentations were unfindable.

Fixes under test:
- ``unreliable_clone_set_names``: supplementary members of >=5-way identical
  symptom-set groups are excluded from MATCHING (browse unaffected); module
  entries and a reviewed whitelist never are.
- 47 curated supplementary symptom sets (degu tail slip/otitis/nails, torpor,
  egg peritonitis, scaly face, gout, spectacle retention …).
- Dog Tick Paralysis: the set encoded a painful orthopedic gait (4x limping +
  stiffness) instead of ascending flaccid paralysis, and the common tier let
  it surface in the top-3 of every lame-dog complaint.
"""

from api.chat.disease_matcher import _match_species_symptoms_to_diseases
from api.chat.species_data import get_species_data
from api.chat.symptom_extractor import _extract_species_symptoms
from api.species.helpers import unreliable_clone_set_names


def _top(text, species, n=5):
    syms = sorted(_extract_species_symptoms(text, species))
    matches = _match_species_symptoms_to_diseases(list(syms), species, lang="ja")
    return syms, [(m.get("name_ja") or m.get("name_en"), m.get("name_en")) for m in matches[:n]]


class TestGuardUnit:
    def test_module_families_never_suppressed(self):
        # 12 dog eye diseases legitimately share the red-eye triad — module
        # entries must never be suppressed however large the group.
        diseases = [{"name": f"EyeDisease{i}", "symptoms": {"a", "b", "c"}} for i in range(12)]
        assert unreliable_clone_set_names(diseases, "dogtest") == frozenset()

    def test_supplementary_clones_suppressed_and_whitelist_honored(self):
        diseases = [
            {"name": f"Clone{i}", "symptoms": {"x", "y"}, "_supplementary": True} for i in range(6)
        ]
        diseases.append({"name": "Constipation", "symptoms": {"x", "y"}, "_supplementary": True})
        out = unreliable_clone_set_names(diseases, "rabbit")
        assert {f"Clone{i}" for i in range(6)} <= out
        assert "Constipation" not in out  # whitelisted (rabbit)

    def test_small_groups_untouched(self):
        diseases = [
            {"name": f"Pair{i}", "symptoms": {"x", "y"}, "_supplementary": True} for i in range(4)
        ]
        assert unreliable_clone_set_names(diseases, "anytest") == frozenset()


class TestCuratedSetsApplied:
    def test_degu_trio_no_longer_share_the_collapse_clone(self):
        pool = get_species_data("degu")["diseases"]
        by = {d.get("name"): set(d.get("symptoms") or []) for d in pool}
        assert "ear_discharge" in by["Ear Infection"]
        assert "tail_injury" in by["Tail Slip (Degloving)"]
        assert "lameness" in by["Nail Overgrowth"]
        for n in ("Ear Infection", "Tail Slip (Degloving)", "Nail Overgrowth"):
            assert "collapse" not in by[n], f"{n} still carries the collapse clone set"

    def test_chinchilla_pregnancy_toxemia_has_no_male_genital_signs(self):
        # The old set was contaminated with the penile fur-ring signs.
        pool = get_species_data("chinchilla")["diseases"]
        d = next(x for x in pool if x.get("name") == "Pregnancy Toxemia")
        syms = set(d.get("symptoms") or [])
        assert not ({"fur_ring_penis", "paraphimosis", "penile_swelling"} & syms)
        assert "seizures" in syms and "lethargy" in syms

    def test_rabbit_cecotrophy_disorders_use_cecotrope_signs(self):
        pool = get_species_data("rabbit")["diseases"]
        d = next(x for x in pool if x.get("name") == "Cecotrophy Disorders")
        syms = set(d.get("symptoms") or [])
        assert "abnormal_cecotropes" in syms and "soft_stool" in syms
        assert "sudden_death" not in syms  # the old 47-way rabbit clone


class TestRankingOutcomes:
    def test_dog_lame_complaint_excludes_tick_paralysis(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases
        from api.species.dog_diseases import DISEASES as DOG

        tick = next(d for d in DOG if d.get("name") == "Tick Paralysis")
        assert not any(s.startswith("limping") for s in tick["symptoms"])
        assert "stiffness" not in tick["symptoms"]

        syms = extract_symptoms_from_text("後ろ足を引きずる 触ると痛がる")
        top5 = [m["name_ja"] for m in match_symptoms_to_diseases(syms)[:5]]
        assert not any("マダニ麻痺" in n for n in top5), top5

    def test_dog_tick_paralysis_tier_demoted(self):
        from api.species.prevalence_data import (
            JAPAN_REGIONAL_ADJUSTMENTS,
            SPECIES_PREVALENCE,
        )

        assert SPECIES_PREVALENCE["dog"]["Tick Paralysis"] == "uncommon"
        assert JAPAN_REGIONAL_ADJUSTMENTS["dog"]["Tick Paralysis"] == "rare"

    def test_degu_collapse_complaint_not_polluted(self):
        # A collapsed drooling degu must never see nail overgrowth or otitis
        # in its differentials (the old clone set put them there).
        _syms, top = _top("ぐったりして呼吸が速い よだれ", "degu")
        names = [t[1] or "" for t in top]
        assert not any("Nail Overgrowth" in n or n == "Ear Infection" for n in names), top

    def test_hamster_torpor_complaint_ranks_torpor_first(self):
        syms, top = _top("体が冷たい 呼吸がゆっくり 反応がない", "hamster")
        assert "cold_body" in syms and "slow_breathing" in syms
        assert any("冬眠" in (t[0] or "") for t in top[:2]), top

    def test_bird_egg_peritonitis_findable_by_real_presentation(self):
        _syms, top = _top("卵詰まりのようにお腹が膨れて 呼吸が苦しそう", "bird")
        assert any("卵黄性腹膜炎" in (t[0] or "") or "Egg" in (t[1] or "") for t in top), top

    def test_rabbit_ecuniculi_whitelisted_and_still_ranks(self):
        # Whitelisted clone member: E. cuniculi keeps matching head tilt.
        _syms, top = _top("首が傾いている 元気がない", "rabbit")
        assert any("エンセファリトゾーン" in (t[0] or "") or "斜頸" in (t[0] or "") for t in top), top

    def test_snake_spectacle_retention_findable(self):
        _syms, top = _top("脱皮がうまくできない 目が白いまま", "snake")
        assert any("スペクタクル" in (t[0] or "") or "脱皮不全" in (t[0] or "") for t in top[:3]), top
