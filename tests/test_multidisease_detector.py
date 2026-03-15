"""Tests for multidisease_detector.py.

Covers MultiDiseaseDetector, MultiDiseaseSession, and DiseaseCombination.
"""

import pytest

from api.ai.multidisease_detector import (
    DiseaseCombination,
    MultiDiseaseDetector,
    MultiDiseaseSession,
    _classify_symptom_system,
)


# ── Helper factories ─────────────────────────────────────────────────

def _disease(name, match_percent=50, **kwargs):
    d = {"name": name, "match_percent": match_percent}
    d.update(kwargs)
    return d


def _combo(diseases, confidence=0.5, **kwargs):
    return DiseaseCombination(
        diseases=diseases,
        combined_confidence=confidence,
        component_confidences={d: 0.5 for d in diseases},
        interaction_effect=0.0,
        shared_symptom_count=0,
        **kwargs,
    )


# ── DiseaseCombination dataclass ─────────────────────────────────────

class TestDiseaseCombination:

    def test_to_dict_keys(self):
        combo = _combo(["A", "B"], confidence=0.65)
        d = combo.to_dict()
        assert d["diseases"] == ["A", "B"]
        assert d["combined_confidence"] == 0.65
        assert "interaction_effect" in d
        assert "confidence_sources" in d

    def test_to_dict_rounds_floats(self):
        combo = DiseaseCombination(
            diseases=["A"],
            combined_confidence=0.12345,
            component_confidences={"A": 0.67891},
            interaction_effect=0.33333,
            shared_symptom_count=1,
        )
        d = combo.to_dict()
        assert d["combined_confidence"] == 0.123
        assert d["component_confidences"]["A"] == 0.679
        assert d["interaction_effect"] == 0.333


# ── MultiDiseaseDetector.should_explore_multidisease ─────────────────

class TestShouldExploreMultidisease:

    def test_too_few_symptoms(self):
        result = MultiDiseaseDetector.should_explore_multidisease(
            detected_symptoms=["s1", "s2"],
            suspected_diseases=[_disease("A", 80), _disease("B", 70)],
        )
        assert result is False

    def test_too_few_diseases(self):
        result = MultiDiseaseDetector.should_explore_multidisease(
            detected_symptoms=["s1", "s2", "s3", "s4", "s5"],
            suspected_diseases=[_disease("A", 80)],
        )
        assert result is False

    def test_similar_confidence_triggers(self):
        result = MultiDiseaseDetector.should_explore_multidisease(
            detected_symptoms=["s1", "s2", "s3", "s4", "s5"],
            suspected_diseases=[
                _disease("A", 80),
                _disease("B", 72),  # within 15% of 80
            ],
        )
        assert result is True

    def test_large_confidence_gap_no_trigger(self):
        result = MultiDiseaseDetector.should_explore_multidisease(
            detected_symptoms=["s1", "s2", "s3", "s4", "s5"],
            suspected_diseases=[
                _disease("A", 90),
                _disease("B", 40),  # spread > 0.15
            ],
        )
        # Spread is 0.5 → doesn't trigger similarity heuristic
        # But 5 symptoms is not >= 7 → false
        assert result is False

    def test_senior_age_triggers(self):
        result = MultiDiseaseDetector.should_explore_multidisease(
            detected_symptoms=["s1", "s2", "s3", "s4", "s5"],
            suspected_diseases=[
                _disease("A", 90),
                _disease("B", 40),
            ],
            patient_context={"age_years": 12},
        )
        assert result is True

    def test_many_symptoms_triggers(self):
        symptoms = [f"s{i}" for i in range(7)]
        result = MultiDiseaseDetector.should_explore_multidisease(
            detected_symptoms=symptoms,
            suspected_diseases=[
                _disease("A", 90),
                _disease("B", 40),
            ],
        )
        assert result is True


# ── MultiDiseaseDetector.generate_multidisease_candidates ────────────

class TestGenerateMultidiseaseCandidates:

    def test_fewer_than_2_diseases(self):
        combos = MultiDiseaseDetector.generate_multidisease_candidates(
            suspected_diseases=[_disease("A", 80)],
            detected_symptoms=["s1", "s2"],
        )
        assert combos == []

    def test_generates_pairwise_combinations(self):
        combos = MultiDiseaseDetector.generate_multidisease_candidates(
            suspected_diseases=[
                _disease("A", 80),
                _disease("B", 60),
                _disease("C", 50),
            ],
            detected_symptoms=["s1", "s2", "s3"],
        )
        # Should generate pairs from top candidates
        assert isinstance(combos, list)
        for combo in combos:
            assert len(combo.diseases) == 2
            assert combo.combined_confidence >= MultiDiseaseDetector.MIN_COMBINATION_CONFIDENCE

    def test_sorted_by_confidence_descending(self):
        combos = MultiDiseaseDetector.generate_multidisease_candidates(
            suspected_diseases=[
                _disease("A", 80),
                _disease("B", 60),
                _disease("C", 50),
            ],
            detected_symptoms=["s1", "s2", "s3"],
        )
        if len(combos) >= 2:
            for i in range(len(combos) - 1):
                assert combos[i].combined_confidence >= combos[i + 1].combined_confidence

    def test_low_confidence_filtered_out(self):
        combos = MultiDiseaseDetector.generate_multidisease_candidates(
            suspected_diseases=[
                _disease("A", 80),
                _disease("B", 10),  # Below MIN_CONFIDENCE_THRESHOLD (0.25)
            ],
            detected_symptoms=["s1"],
        )
        assert combos == []

    def test_patient_context_passed(self):
        combos = MultiDiseaseDetector.generate_multidisease_candidates(
            suspected_diseases=[
                _disease("A", 80),
                _disease("B", 60),
            ],
            detected_symptoms=["s1"],
            patient_context={"age_years": 12, "severity": "severe"},
        )
        assert isinstance(combos, list)


# ── MultiDiseaseDetector._calculate_interaction_effect ────────────────

class TestInteractionEffect:

    def test_zero_symptoms(self):
        effect = MultiDiseaseDetector._calculate_interaction_effect("A", "B", 0, 0)
        assert effect == 0.0

    def test_high_overlap_competitive(self):
        effect = MultiDiseaseDetector._calculate_interaction_effect("A", "B", 7, 10)
        assert effect < 0

    def test_low_overlap_synergistic(self):
        effect = MultiDiseaseDetector._calculate_interaction_effect("A", "B", 1, 10)
        assert effect > 0

    def test_moderate_overlap_neutral(self):
        effect = MultiDiseaseDetector._calculate_interaction_effect("A", "B", 4, 10)
        assert effect == 0.0


# ── MultiDiseaseDetector.validate_combination ────────────────────────

class TestValidateCombination:

    def test_validate_returns_tuple(self):
        combo = _combo(["Hip Dysplasia", "Osteoarthritis"])
        valid, reason = MultiDiseaseDetector.validate_combination(combo)
        assert isinstance(valid, bool)
        assert isinstance(reason, str)

    def test_unknown_combination_still_valid(self):
        combo = _combo(["UnknownDisease1", "UnknownDisease2"])
        valid, reason = MultiDiseaseDetector.validate_combination(combo)
        assert valid is True


# ── MultiDiseaseDetector.rank_combinations_by_likelihood ─────────────

class TestRankCombinations:

    def test_ranks_descending(self):
        combos = [
            _combo(["A", "B"], confidence=0.3),
            _combo(["C", "D"], confidence=0.9),
            _combo(["E", "F"], confidence=0.6),
        ]
        ranked = MultiDiseaseDetector.rank_combinations_by_likelihood(combos)
        assert ranked[0].combined_confidence == 0.9
        assert ranked[1].combined_confidence == 0.6
        assert ranked[2].combined_confidence == 0.3

    def test_empty_list(self):
        assert MultiDiseaseDetector.rank_combinations_by_likelihood([]) == []


# ── MultiDiseaseDetector.estimate_symptom_allocation ─────────────────

class TestEstimateSymptomAllocation:

    def test_returns_dict(self):
        alloc = MultiDiseaseDetector.estimate_symptom_allocation(
            diseases=["A", "B"],
            detected_symptoms=["s1", "s2"],
        )
        assert isinstance(alloc, dict)
        assert "A" in alloc
        assert "B" in alloc


# ── MultiDiseaseDetector.apply_ambiguity_adjustment ──────────────────

class TestApplyAmbiguityAdjustment:

    def test_adjustment_reduces_confidence(self):
        combo = _combo(["A", "B"], confidence=0.8)
        adjusted = MultiDiseaseDetector.apply_ambiguity_adjustment(combo, 0.7)
        assert adjusted.combined_confidence == pytest.approx(0.56)
        assert adjusted.ambiguity_adjusted is True
        assert "ambiguity_analysis" in adjusted.confidence_sources

    def test_adjustment_factor_1_no_change(self):
        combo = _combo(["A", "B"], confidence=0.8)
        adjusted = MultiDiseaseDetector.apply_ambiguity_adjustment(combo, 1.0)
        assert adjusted.combined_confidence == 0.8


# ── MultiDiseaseSession ─────────────────────────────────────────────

class TestMultiDiseaseSession:

    def test_init(self):
        combo = _combo(["A", "B"], confidence=0.6)
        session = MultiDiseaseSession(
            session_id="test-123",
            detected_symptoms=["s1", "s2"],
            initial_candidates=[combo],
        )
        assert session.session_id == "test-123"
        assert session.current_focus is combo
        assert len(session.explored_combinations) == 1

    def test_init_no_candidates(self):
        session = MultiDiseaseSession(
            session_id="test",
            detected_symptoms=[],
            initial_candidates=[],
        )
        assert session.current_focus is None

    def test_update_combination_confidence(self):
        combo = _combo(["A", "B"], confidence=0.6)
        session = MultiDiseaseSession("test", ["s1"], [combo])
        session.update_combination_confidence(combo, 0.75)

        key = tuple(sorted(combo.diseases))
        assert 0.75 in session.confidence_history[key]

    def test_should_continue_no_focus(self):
        session = MultiDiseaseSession("test", [], [])
        assert session.should_continue_exploration() is False

    def test_should_continue_high_confidence(self):
        combo = _combo(["A", "B"], confidence=0.85)
        session = MultiDiseaseSession("test", ["s1"], [combo])
        assert session.should_continue_exploration() is False

    def test_should_continue_low_confidence(self):
        combo = _combo(["A", "B"], confidence=0.5)
        session = MultiDiseaseSession("test", ["s1"], [combo])
        assert session.should_continue_exploration() is True


# ── Explanation generation ───────────────────────────────────────────

class TestExplanations:

    def test_explanation_ja_with_mechanism(self):
        exp = MultiDiseaseDetector._generate_explanation_ja("A", "B", None)
        assert "組み合わせ" in exp

    def test_explanation_en_with_mechanism(self):
        exp = MultiDiseaseDetector._generate_explanation_en("A", "B", None)
        assert "possible" in exp.lower()


# ── _classify_symptom_system ─────────────────────────────────────────

class TestClassifySymptomSystem:

    def test_respiratory_symptom(self):
        systems = _classify_symptom_system("coughing")
        assert "respiratory" in systems

    def test_gastrointestinal_symptom(self):
        systems = _classify_symptom_system("vomiting")
        assert "gastrointestinal" in systems

    def test_musculoskeletal_symptom(self):
        systems = _classify_symptom_system("limping")
        assert "musculoskeletal" in systems

    def test_neurological_symptom(self):
        systems = _classify_symptom_system("seizure_episodes")
        assert "neurological" in systems

    def test_dermatological_symptom(self):
        systems = _classify_symptom_system("itching")
        assert "dermatological" in systems

    def test_urinary_symptom(self):
        systems = _classify_symptom_system("frequent_urination")
        assert "urinary" in systems

    def test_cardiac_symptom(self):
        systems = _classify_symptom_system("heart_murmur")
        assert "cardiac" in systems

    def test_ophthalmic_symptom(self):
        systems = _classify_symptom_system("eye_discharge")
        assert "ophthalmic" in systems

    def test_systemic_symptom(self):
        systems = _classify_symptom_system("fever")
        assert "systemic" in systems

    def test_unclassified_symptom(self):
        systems = _classify_symptom_system("completely_unknown_xyz")
        assert systems == {"unclassified"}

    def test_multi_system_symptom(self):
        """Paralysis maps to both musculoskeletal and neurological."""
        systems = _classify_symptom_system("paralysis")
        assert "musculoskeletal" in systems
        assert "neurological" in systems

    def test_hyphen_normalized(self):
        """Hyphens in symptom IDs are normalized to underscores."""
        systems = _classify_symptom_system("hair-loss")
        assert "dermatological" in systems


# ── should_explore_multidisease body-system clustering ───────────────

class TestShouldExploreBodySystemClustering:

    def test_multi_system_symptoms_trigger(self):
        """Symptoms spanning 2+ body systems should trigger multi-disease."""
        symptoms = [
            "coughing", "sneezing", "nasal_discharge",  # respiratory
            "vomiting", "diarrhea",  # gastrointestinal
        ]
        diseases = [
            _disease("DiseaseA", 60),
            _disease("DiseaseB", 55),
        ]
        result = MultiDiseaseDetector.should_explore_multidisease(
            symptoms, diseases
        )
        assert result is True

    def test_single_system_symptoms_no_trigger(self):
        """Symptoms all in one system should not trigger via clustering."""
        symptoms = [
            "coughing", "sneezing", "nasal_discharge",
            "wheezing", "breathing_difficulty",
        ]
        # Two diseases with very different confidence (spread >= 0.15)
        diseases = [
            _disease("DiseaseA", 80),
            _disease("DiseaseB", 30),
        ]
        result = MultiDiseaseDetector.should_explore_multidisease(
            symptoms, diseases
        )
        # Single system + wide confidence spread → no trigger
        assert result is False

    def test_too_few_symptoms_still_rejected(self):
        """Even multi-system, <5 symptoms is rejected."""
        symptoms = ["coughing", "vomiting", "limping"]
        diseases = [_disease("A", 50), _disease("B", 50)]
        result = MultiDiseaseDetector.should_explore_multidisease(
            symptoms, diseases
        )
        assert result is False


# ── estimate_symptom_allocation with disease_symptom_sets ────────────

class TestBayesianSymptomAllocation:

    def test_unique_symptoms_assigned_correctly(self):
        """Symptoms unique to one disease go to that disease."""
        alloc = MultiDiseaseDetector.estimate_symptom_allocation(
            diseases=["Flu", "Arthritis"],
            detected_symptoms=["coughing", "limping"],
            disease_symptom_sets={
                "Flu": {"coughing", "sneezing"},
                "Arthritis": {"limping", "stiffness"},
            },
        )
        assert "coughing" in alloc["Flu"]
        assert "limping" in alloc["Arthritis"]

    def test_shared_symptom_goes_to_least_loaded(self):
        """Shared symptoms go to the disease with fewer allocations."""
        alloc = MultiDiseaseDetector.estimate_symptom_allocation(
            diseases=["A", "B"],
            detected_symptoms=["s1", "s2", "shared"],
            disease_symptom_sets={
                "A": {"s1", "shared"},
                "B": {"s2", "shared"},
            },
        )
        # s1→A, s2→B, shared→either (both have 1 each, so min picks first)
        assert "s1" in alloc["A"]
        assert "s2" in alloc["B"]
        assert "shared" in alloc["A"] or "shared" in alloc["B"]

    def test_unmatched_symptoms_not_allocated(self):
        """Symptoms not in any disease set are skipped."""
        alloc = MultiDiseaseDetector.estimate_symptom_allocation(
            diseases=["A", "B"],
            detected_symptoms=["unknown_symptom"],
            disease_symptom_sets={
                "A": {"s1"},
                "B": {"s2"},
            },
        )
        assert alloc["A"] == []
        assert alloc["B"] == []

    def test_no_symptom_sets_returns_empty(self):
        """Without disease_symptom_sets, returns empty allocation."""
        alloc = MultiDiseaseDetector.estimate_symptom_allocation(
            diseases=["A", "B"],
            detected_symptoms=["s1", "s2"],
            disease_symptom_sets=None,
        )
        assert alloc == {"A": [], "B": []}

    def test_load_balancing_across_diseases(self):
        """All-shared symptoms are distributed across diseases."""
        alloc = MultiDiseaseDetector.estimate_symptom_allocation(
            diseases=["A", "B"],
            detected_symptoms=["s1", "s2", "s3", "s4"],
            disease_symptom_sets={
                "A": {"s1", "s2", "s3", "s4"},
                "B": {"s1", "s2", "s3", "s4"},
            },
        )
        # Should roughly balance: 2 each
        assert len(alloc["A"]) == 2
        assert len(alloc["B"]) == 2

    def test_three_diseases_allocation(self):
        """Allocation works with 3 diseases."""
        alloc = MultiDiseaseDetector.estimate_symptom_allocation(
            diseases=["A", "B", "C"],
            detected_symptoms=["s1", "s2", "s3"],
            disease_symptom_sets={
                "A": {"s1"},
                "B": {"s2"},
                "C": {"s3"},
            },
        )
        assert alloc["A"] == ["s1"]
        assert alloc["B"] == ["s2"]
        assert alloc["C"] == ["s3"]
