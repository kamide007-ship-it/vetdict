"""Coverage tests for api.species.helpers module."""

import pytest

from api.species.helpers import ADVICE, SPECIES_BREEDS, analyze_symptoms_generic


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_symptom_names():
    return {
        "vomiting": {"en": "Vomiting", "ja": "嘔吐"},
        "lethargy": {"en": "Lethargy", "ja": "元気消失"},
        "diarrhea": {"en": "Diarrhea", "ja": "下痢"},
        "fever": {"en": "Fever", "ja": "発熱"},
        "cough": {"en": "Cough", "ja": "咳"},
    }


@pytest.fixture
def sample_diseases():
    return [
        {
            "name": "Gastroenteritis",
            "name_ja": "胃腸炎",
            "symptoms": {"vomiting", "diarrhea", "lethargy", "fever"},
            "description": "Inflammation of the stomach and intestines.",
            "description_ja": "胃と腸の炎症。",
            "urgency": "moderate",
            "recommended_tests": ["Blood Test", "Fecal Exam"],
        },
        {
            "name": "Kennel Cough",
            "name_ja": "ケンネルコフ",
            "symptoms": {"cough", "lethargy", "fever"},
            "description": "Infectious tracheobronchitis.",
            "description_ja": "感染性気管気管支炎。",
            "urgency": "low",
            "recommended_tests": ["Chest X-ray"],
        },
        {
            "name": "Unrelated Disease",
            "name_ja": "無関係の病気",
            "symptoms": {"skin_rash", "hair_loss"},
            "description": "A skin condition.",
            "description_ja": "皮膚疾患。",
            "urgency": "low",
            "recommended_tests": ["Skin Scraping"],
        },
    ]


# ---------------------------------------------------------------------------
# ADVICE structure validation
# ---------------------------------------------------------------------------

class TestAdviceStructure:
    """ADVICE dict has correct keys and bilingual values."""

    def test_has_all_severity_keys(self):
        for key in ("low", "moderate", "high", "emergency"):
            assert key in ADVICE

    def test_each_entry_has_en_and_ja(self):
        for key in ADVICE:
            assert "en" in ADVICE[key]
            assert "ja" in ADVICE[key]

    def test_values_are_nonempty_strings(self):
        for key in ADVICE:
            assert isinstance(ADVICE[key]["en"], str) and len(ADVICE[key]["en"]) > 0
            assert isinstance(ADVICE[key]["ja"], str) and len(ADVICE[key]["ja"]) > 0


# ---------------------------------------------------------------------------
# SPECIES_BREEDS validation
# ---------------------------------------------------------------------------

class TestSpeciesBreeds:
    """SPECIES_BREEDS contains expected species."""

    def test_has_cat(self):
        assert "cat" in SPECIES_BREEDS

    def test_breed_entries_have_required_fields(self):
        for species, breeds in SPECIES_BREEDS.items():
            for breed in breeds:
                assert "id" in breed, f"Missing 'id' in {species} breed"
                assert "name" in breed, f"Missing 'name' in {species} breed"
                assert "risk" in breed, f"Missing 'risk' in {species} breed"

    def test_breed_risk_values_are_numeric(self):
        for species, breeds in SPECIES_BREEDS.items():
            for breed in breeds:
                for disease, multiplier in breed.get("risk", {}).items():
                    assert isinstance(multiplier, (int, float)), (
                        f"Non-numeric risk for {breed['id']}/{disease}"
                    )


# ---------------------------------------------------------------------------
# analyze_symptoms_generic
# ---------------------------------------------------------------------------

class TestAnalyzeSymptomsGenericBasic:
    """Basic invocations of analyze_symptoms_generic."""

    def test_matching_symptoms_returns_results(self, sample_diseases, sample_symptom_names):
        result = analyze_symptoms_generic(
            symptoms=["vomiting", "diarrhea"],
            diseases=sample_diseases,
            symptom_names=sample_symptom_names,
        )
        assert len(result["suspected_diseases"]) >= 1
        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Gastroenteritis" in names

    def test_no_matching_symptoms_empty(self, sample_diseases, sample_symptom_names):
        result = analyze_symptoms_generic(
            symptoms=["nonexistent_symptom"],
            diseases=sample_diseases,
            symptom_names=sample_symptom_names,
        )
        assert result["suspected_diseases"] == []

    def test_unrelated_disease_excluded(self, sample_diseases, sample_symptom_names):
        result = analyze_symptoms_generic(
            symptoms=["vomiting", "diarrhea", "lethargy"],
            diseases=sample_diseases,
            symptom_names=sample_symptom_names,
        )
        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Unrelated Disease" not in names


class TestAnalyzeSymptomsGenericResultStructure:
    """Verify the result dict contains all expected keys."""

    def test_top_level_keys(self, sample_diseases, sample_symptom_names):
        result = analyze_symptoms_generic(
            symptoms=["vomiting"],
            diseases=sample_diseases,
            symptom_names=sample_symptom_names,
        )
        assert "suspected_diseases" in result
        assert "recommended_tests" in result
        assert "severity" in result
        assert "general_advice" in result
        assert "general_advice_ja" in result
        assert "breed_risk_applied" in result
        assert "onset_applied" in result
        assert "age_applied" in result
        assert "symptom_names" in result

    def test_suspected_disease_entry_keys(self, sample_diseases, sample_symptom_names):
        result = analyze_symptoms_generic(
            symptoms=["vomiting", "diarrhea"],
            diseases=sample_diseases,
            symptom_names=sample_symptom_names,
        )
        entry = result["suspected_diseases"][0]
        assert "name" in entry
        assert "name_ja" in entry
        assert "likelihood" in entry
        assert "match_percent" in entry
        assert "matching_symptoms" in entry
        assert "description" in entry

    def test_severity_is_valid(self, sample_diseases, sample_symptom_names):
        result = analyze_symptoms_generic(
            symptoms=["vomiting"],
            diseases=sample_diseases,
            symptom_names=sample_symptom_names,
        )
        assert result["severity"] in ("low", "moderate", "high", "emergency")


class TestAnalyzeSymptomsGenericBreedRisk:
    """Breed risk multipliers affect match_percent."""

    def test_breed_risk_applied_flag(self, sample_symptom_names):
        diseases = [
            {
                "name": "Feline Hypertrophic Cardiomyopathy (HCM)",
                "name_ja": "肥大型心筋症",
                "symptoms": {"lethargy", "cough"},
                "description": "Heart disease",
                "description_ja": "心疾患",
                "urgency": "high",
                "recommended_tests": ["Echocardiogram"],
            },
        ]
        result = analyze_symptoms_generic(
            symptoms=["lethargy", "cough"],
            diseases=diseases,
            symptom_names=sample_symptom_names,
            breed="cat_maine_coon",
            species="cat",
        )
        assert result["breed_risk_applied"] is True

    def test_breed_risk_increases_score(self, sample_symptom_names):
        diseases = [
            {
                "name": "Feline Hypertrophic Cardiomyopathy (HCM)",
                "name_ja": "肥大型心筋症",
                "symptoms": {"lethargy", "cough"},
                "description": "Heart disease",
                "description_ja": "心疾患",
                "urgency": "high",
                "recommended_tests": ["Echocardiogram"],
            },
        ]
        result_no_breed = analyze_symptoms_generic(
            symptoms=["lethargy", "cough"],
            diseases=diseases,
            symptom_names=sample_symptom_names,
        )
        result_breed = analyze_symptoms_generic(
            symptoms=["lethargy", "cough"],
            diseases=diseases,
            symptom_names=sample_symptom_names,
            breed="cat_maine_coon",
            species="cat",
        )
        score_no_breed = result_no_breed["suspected_diseases"][0]["match_percent"]
        score_breed = result_breed["suspected_diseases"][0]["match_percent"]
        assert score_breed >= score_no_breed


class TestAnalyzeSymptomsGenericAdvice:
    """Custom advice dict is used when provided."""

    def test_custom_advice(self, sample_diseases, sample_symptom_names):
        custom_advice = {
            "low": {"en": "Custom low advice", "ja": "カスタム低"},
            "moderate": {"en": "Custom moderate", "ja": "カスタム中"},
            "high": {"en": "Custom high", "ja": "カスタム高"},
            "emergency": {"en": "Custom emergency", "ja": "カスタム緊急"},
        }
        result = analyze_symptoms_generic(
            symptoms=["vomiting"],
            diseases=sample_diseases,
            symptom_names=sample_symptom_names,
            advice=custom_advice,
        )
        # severity should be "low" for a single non-urgent symptom
        assert "Custom" in result["general_advice"]

    def test_default_advice_used(self, sample_diseases, sample_symptom_names):
        result = analyze_symptoms_generic(
            symptoms=["vomiting"],
            diseases=sample_diseases,
            symptom_names=sample_symptom_names,
        )
        # Should use the global ADVICE dict
        severity = result["severity"]
        assert result["general_advice"] == ADVICE[severity]["en"]
        assert result["general_advice_ja"] == ADVICE[severity]["ja"]
