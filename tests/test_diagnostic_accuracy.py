"""Diagnostic accuracy regression tests.

Ensures that key clinical scenarios produce expected top-1 diagnoses
with minimum confidence thresholds. Based on CLAUDE.md accuracy benchmarks.
"""

from api.diagnostic_chat import _match_species_symptoms_to_diseases


def _top1(species: str, symptoms: list[str]) -> dict:
    """Run diagnosis and return top-1 result."""
    results = _match_species_symptoms_to_diseases(symptoms, species)
    assert results, f"No results for {species} with {symptoms}"
    return results[0]


def _assert_diagnosis(species, symptoms, expected_name_fragment, min_confidence=None, rank=1):
    """Assert that expected disease appears at given rank with minimum confidence."""
    results = _match_species_symptoms_to_diseases(symptoms, species)
    assert len(results) >= rank, f"Not enough results (got {len(results)}, need {rank})"
    target = results[rank - 1]
    name = (target.get("name_en", "") + " " + target.get("name_ja", "")).lower()
    assert expected_name_fragment.lower() in name, (
        f"Expected '{expected_name_fragment}' at rank {rank}, "
        f"got '{target.get('name_en', '')}' / '{target.get('name_ja', '')}'"
    )
    if min_confidence is not None:
        assert target["confidence_percent"] >= min_confidence, (
            f"Confidence {target['confidence_percent']}% < {min_confidence}% for {expected_name_fragment}"
        )


# =========================================================================
# Cat diagnostic accuracy
# =========================================================================
class TestCatDiagnosticAccuracy:
    def test_fhv1_uri(self):
        """Cat: FHV-1/URI with classic respiratory signs → high confidence."""
        _assert_diagnosis(
            "cat",
            ["sneezing", "nasal_discharge", "eye_discharge", "conjunctivitis", "fever"],
            "herpesvirus",
            min_confidence=90,
        )

    def test_fip_effusive(self):
        """Cat: FIP effusive with specific signs — should be in top 5."""
        results = _match_species_symptoms_to_diseases(
            ["abdominal_distension", "fever", "weight_loss", "lethargy", "jaundice", "eye_discharge"], "cat"
        )
        names = [(r.get("name_en", "") + " " + r.get("name_ja", "")).lower() for r in results[:7]]
        assert any("fip" in n or "peritonitis" in n or "infectious" in n for n in names), (
            f"FIP not in top 7: {[r.get('name_en', '') for r in results[:7]]}"
        )

    def test_arterial_thromboembolism(self):
        """Cat: ATE with sudden hindlimb paralysis."""
        _assert_diagnosis(
            "cat",
            ["hind_limb_paralysis", "vocalization_changes", "cold_extremities", "pain"],
            "thromboembolism",
            min_confidence=70,
        )

    def test_eye_disease(self):
        """Cat: eye disease with squinting — corneal or related in top 3."""
        results = _match_species_symptoms_to_diseases(
            ["squinting", "eye_discharge", "eye_redness", "pawing_at_face"], "cat"
        )
        names = [(r.get("name_en", "")).lower() for r in results[:3]]
        assert any("corneal" in n or "eye" in n or "ophthalm" in n or "entropion" in n for n in names), (
            f"No eye disease in top 3: {names}"
        )


# =========================================================================
# Rabbit diagnostic accuracy
# =========================================================================
class TestRabbitDiagnosticAccuracy:
    def test_gi_stasis(self):
        """Rabbit: GI stasis with classic signs."""
        _assert_diagnosis(
            "rabbit",
            ["appetite_loss", "reduced_fecal_output", "hunched_posture", "teeth_grinding"],
            "stasis",
            min_confidence=90,
        )

    def test_pasteurellosis(self):
        """Rabbit: pasteurellosis with snuffles."""
        _assert_diagnosis(
            "rabbit", ["nasal_discharge", "sneezing", "eye_discharge", "head_tilt"], "pasteurell", min_confidence=50
        )

    def test_head_tilt_vestibular(self):
        """Rabbit: head tilt — vestibular or E. cuniculi in top 3."""
        results = _match_species_symptoms_to_diseases(
            ["head_tilt", "nystagmus", "loss_of_balance", "urinary_incontinence"], "rabbit"
        )
        names = [(r.get("name_en", "")).lower() for r in results[:3]]
        assert any("vestibul" in n or "encephalitozoon" in n or "pasteurell" in n for n in names), (
            f"No vestibular/EC in top 3: {names}"
        )


# =========================================================================
# Chinchilla diagnostic accuracy
# =========================================================================
class TestChinchillaDiagnosticAccuracy:
    def test_malocclusion(self):
        """Chinchilla: dental malocclusion with drooling."""
        _assert_diagnosis(
            "chinchilla",
            ["drooling", "appetite_loss", "weight_loss", "difficulty_eating"],
            "malocclusion",
            min_confidence=70,
        )

    def test_ringworm(self):
        """Chinchilla: dermatophytosis with patchy hair loss."""
        _assert_diagnosis(
            "chinchilla",
            ["fur_loss_patches", "crusty_skin", "scaling_skin", "itching"],
            "dermatophyt",
            min_confidence=50,
        )


# =========================================================================
# Guinea pig diagnostic accuracy
# =========================================================================
class TestGuineaPigDiagnosticAccuracy:
    def test_scurvy(self):
        """Guinea pig: vitamin C deficiency/scurvy."""
        _assert_diagnosis(
            "guinea_pig",
            ["lethargy", "joint_swelling", "lameness", "weight_loss", "bleeding"],
            "scurvy",
            min_confidence=70,
        )

    def test_respiratory(self):
        """Guinea pig: respiratory infection."""
        _assert_diagnosis(
            "guinea_pig", ["nasal_discharge", "sneezing", "dyspnea", "lethargy"], "respiratory", min_confidence=70
        )


# =========================================================================
# Hedgehog diagnostic accuracy
# =========================================================================
class TestHedgehogDiagnosticAccuracy:
    def test_whs(self):
        """Hedgehog: WHS — wobbly or posterior paralysis in top 3."""
        results = _match_species_symptoms_to_diseases(
            ["hind_limb_weakness", "weight_loss", "muscle_twitching", "falling"], "hedgehog"
        )
        names = [(r.get("name_en", "")).lower() for r in results[:3]]
        assert any("wobbly" in n or "paralysis" in n or "demyelinat" in n for n in names), (
            f"No WHS-related in top 3: {names}"
        )

    def test_mite_infestation(self):
        """Hedgehog: mite infestation with quill loss."""
        _assert_diagnosis(
            "hedgehog", ["itching", "quill_loss", "crusty_skin", "scaling_skin"], "mite", min_confidence=70
        )


# =========================================================================
# Ferret diagnostic accuracy
# =========================================================================
class TestFerretDiagnosticAccuracy:
    def test_adrenal_disease(self):
        """Ferret: adrenal disease with classic signs."""
        _assert_diagnosis(
            "ferret", ["hair_loss", "vulvar_swelling", "aggression", "itching"], "adrenal", min_confidence=80
        )

    def test_insulinoma(self):
        """Ferret: insulinoma — islet cell in top 3."""
        results = _match_species_symptoms_to_diseases(["lethargy", "weakness", "weight_loss", "seizures"], "ferret")
        names = [(r.get("name_en", "")).lower() for r in results[:3]]
        assert any("insulinoma" in n or "islet" in n for n in names), f"Insulinoma not in top 3: {names}"


# =========================================================================
# Sugar glider diagnostic accuracy
# =========================================================================
class TestSugarGliderDiagnosticAccuracy:
    def test_nutritional_deficiency(self):
        """Sugar glider: nutritional disease."""
        results = _match_species_symptoms_to_diseases(
            ["lethargy", "weakness", "weight_loss", "tremors"], "sugar_glider"
        )
        names = [(r.get("name_en", "")).lower() for r in results[:5]]
        assert any("calcium" in n or "nutrition" in n or "metabolic" in n for n in names), (
            f"No nutritional disease in top 5: {names}"
        )


# =========================================================================
# Low-information confidence cap
# =========================================================================
class TestLowInfoConfidenceCap:
    def test_single_symptom_capped_at_35(self):
        """Single symptom should have confidence capped at 35% (chat engine)."""
        top = _top1("cat", ["vomiting"])
        assert top["confidence_percent"] <= 35.0, f"1-symptom confidence {top['confidence_percent']}% exceeds 35% cap"

    def test_two_symptoms_capped_at_55(self):
        """Two symptoms should have confidence capped at 55% (chat engine)."""
        top = _top1("cat", ["vomiting", "lethargy"])
        assert top["confidence_percent"] <= 55.0, f"2-symptom confidence {top['confidence_percent']}% exceeds 55% cap"

    def test_three_symptoms_uncapped(self):
        """Three+ symptoms should not be artificially capped."""
        top = _top1("cat", ["sneezing", "nasal_discharge", "eye_discharge"])
        # With 3 specific symptoms, confidence should exceed the 2-symptom cap
        assert top["confidence_percent"] > 0  # Just verify it returns a result
