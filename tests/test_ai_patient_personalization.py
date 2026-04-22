"""Tests for patient personalization module."""

from api.ai.patient_personalization import (
    AgeExtractor,
    PatientContext,
    PersonalizationEngine,
    SeverityInference,
    personalize_extraction_result,
)


class TestAgeExtractor:
    """Test age extraction from natural language."""

    def test_extract_puppy_keyword_en(self):
        """Test English puppy keyword extraction."""
        context = AgeExtractor.extract("My puppy has been coughing")
        assert context.age_stage == "puppy"
        assert context.confidence > 0.7

    def test_extract_senior_keyword_en(self):
        """Test English senior keyword extraction."""
        context = AgeExtractor.extract("My senior dog has arthritis")
        assert context.age_stage == "senior"
        assert context.confidence > 0.7

    def test_extract_young_keyword_en(self):
        """Test English young keyword extraction."""
        context = AgeExtractor.extract("My young dog is very active")
        assert context.age_stage == "young"
        assert context.confidence >= 0.6

    def test_extract_numeric_age_years(self):
        """Test numeric age extraction (years)."""
        context = AgeExtractor.extract("My 3 year old dog is sick")
        assert context.extracted_age_years is not None
        assert context.extracted_age_years == 3.0
        assert context.age_stage == "adult"  # 3 years old is adult
        assert context.confidence > 0.9

    def test_extract_numeric_age_yo(self):
        """Test numeric age extraction (yo format)."""
        context = AgeExtractor.extract("My 5yo dog has hip pain")
        assert context.extracted_age_years == 5.0
        assert context.age_stage == "adult"

    def test_extract_numeric_age_months(self):
        """Test numeric age extraction (months)."""
        context = AgeExtractor.extract("My 6 month old puppy is sick")
        assert context.extracted_age_years is not None
        assert abs(context.extracted_age_years - 0.5) < 0.01  # 6 months ≈ 0.5 years
        assert context.age_stage == "puppy"

    def test_extract_japanese_puppy(self):
        """Test Japanese puppy keyword extraction."""
        context = AgeExtractor.extract("子犬が咳をしている")
        assert context.age_stage == "puppy"
        assert context.confidence > 0.7

    def test_extract_japanese_senior(self):
        """Test Japanese senior keyword extraction."""
        context = AgeExtractor.extract("老犬が元気がない")
        assert context.age_stage == "senior"

    def test_extract_japanese_numeric_age(self):
        """Test Japanese numeric age extraction."""
        context = AgeExtractor.extract("うちの犬は3歳です")
        assert context.extracted_age_years == 3.0
        assert context.age_stage == "adult"  # 3 years old is adult

    def test_extract_no_age(self):
        """Test when no age information present."""
        context = AgeExtractor.extract("My dog is not feeling well")
        assert context.age_stage is None
        assert context.extracted_age_years is None

    def test_extract_empty_text(self):
        """Test with empty text."""
        context = AgeExtractor.extract("")
        assert context.age_stage is None

    def test_stage_from_age_puppy(self):
        """Test age stage classification for puppies."""
        assert AgeExtractor._stage_from_age(0.5) == "puppy"
        assert AgeExtractor._stage_from_age(0.9) == "puppy"

    def test_stage_from_age_young(self):
        """Test age stage classification for young."""
        assert AgeExtractor._stage_from_age(1.5) == "young"
        assert AgeExtractor._stage_from_age(2.5) == "young"

    def test_stage_from_age_adult(self):
        """Test age stage classification for adult."""
        assert AgeExtractor._stage_from_age(4.0) == "adult"
        assert AgeExtractor._stage_from_age(6.0) == "adult"

    def test_stage_from_age_senior(self):
        """Test age stage classification for senior."""
        assert AgeExtractor._stage_from_age(8.0) == "senior"
        assert AgeExtractor._stage_from_age(12.0) == "senior"


class TestSeverityInference:
    """Test severity assessment from symptoms."""

    def test_severity_mild_single_symptom(self):
        """Test mild severity with single symptom."""
        severity = SeverityInference.assess(1, ["coughing"])
        assert severity == "mild"

    def test_severity_moderate_few_symptoms(self):
        """Test moderate severity with 2-4 symptoms."""
        for count in [2, 3, 4]:
            severity = SeverityInference.assess(count, ["symptom1", "symptom2"])
            assert severity == "moderate"

    def test_severity_severe_many_symptoms(self):
        """Test severe severity with 5+ symptoms."""
        severity = SeverityInference.assess(5, ["s1", "s2", "s3", "s4", "s5"])
        assert severity == "severe"

    def test_severity_urgent_override(self):
        """Test urgent symptoms override normal severity."""
        # Urgent symptom overrides low count
        severity = SeverityInference.assess(1, ["difficulty_breathing"])
        assert severity == "severe"

    def test_severity_multiple_urgent(self):
        """Test multiple urgent symptoms."""
        severity = SeverityInference.assess(2, ["seizure", "bleeding"])
        assert severity == "severe"


class TestPersonalizationEngine:
    """Test personalization engine."""

    def test_personalize_senior_dog_hip_dysplasia(self):
        """Test age-based confidence adjustment for senior."""
        context = PatientContext(age_stage="senior", severity="moderate")
        adjusted = PersonalizationEngine.personalize_disease_confidence("hip_dysplasia", 0.65, context)

        # Should be boosted for senior dogs
        assert adjusted > 0.65

    def test_personalize_puppy_hypoglycemia(self):
        """Test age-based confidence adjustment for puppy."""
        context = PatientContext(age_stage="puppy", severity="moderate")
        adjusted = PersonalizationEngine.personalize_disease_confidence("hypoglycemia", 0.55, context)

        # Should be boosted for puppies
        assert adjusted > 0.55

    def test_personalize_unknown_disease(self):
        """Test personalization with unknown disease (no multiplier)."""
        context = PatientContext(age_stage="adult", severity="moderate")
        original = 0.70
        adjusted = PersonalizationEngine.personalize_disease_confidence("unknown_disease", original, context)

        # Should only apply severity multiplier (1.0 for moderate)
        assert adjusted == original

    def test_personalize_severe_symptom(self):
        """Test severity-based confidence boost."""
        context = PatientContext(age_stage="adult", severity="severe")
        adjusted = PersonalizationEngine.personalize_disease_confidence("generic_disease", 0.70, context)

        # Severe should boost confidence (1.15x)
        assert adjusted > 0.70

    def test_personalize_mild_symptom(self):
        """Test severity-based confidence reduction."""
        context = PatientContext(age_stage="adult", severity="mild")
        adjusted = PersonalizationEngine.personalize_disease_confidence("generic_disease", 0.70, context)

        # Mild should reduce confidence (0.85x)
        assert adjusted < 0.70

    def test_personalize_confidence_capped(self):
        """Test confidence is capped at 1.0."""
        context = PatientContext(age_stage="senior", severity="severe")
        adjusted = PersonalizationEngine.personalize_disease_confidence("hip_dysplasia", 0.95, context)

        assert adjusted <= 1.0

    def test_personalize_confidence_floored(self):
        """Test confidence is floored at 0.0."""
        context = PatientContext(age_stage="puppy", severity="mild")
        # Some disease with heavy negative adjustment
        adjusted = PersonalizationEngine.personalize_disease_confidence("cognitive_dysfunction", 0.05, context)

        assert adjusted >= 0.0

    def test_personalize_all_diseases(self):
        """Test batch personalization of diseases."""
        diseases = [
            {"name": "hip_dysplasia", "confidence": 0.65},
            {"name": "hypoglycemia", "confidence": 0.55},
            {"name": "generic_disease", "confidence": 0.70},
        ]
        context = PatientContext(age_stage="senior", severity="moderate")

        personalized = PersonalizationEngine.personalize_all_diseases(diseases, context)

        assert len(personalized) == 3
        # All should have confidence_adjustment field
        for disease in personalized:
            assert "confidence_adjustment" in disease
            assert 0.0 <= disease["confidence"] <= 1.0

    def test_build_context_from_text_with_symptoms(self):
        """Test building complete context from text."""
        text = "My 3 year old dog is coughing and vomiting"
        symptoms = ["coughing", "vomiting"]

        context = PersonalizationEngine.build_context_from_text(text, symptoms)

        assert context.age_stage == "adult"  # 3 years old is adult
        assert context.extracted_age_years == 3.0
        assert context.severity == "moderate"  # 2 symptoms

    def test_build_context_severe_from_symptoms(self):
        """Test context severity inference from many symptoms."""
        text = "My dog is sick"
        symptoms = ["coughing", "vomiting", "diarrhea", "fever", "lethargy", "loss_of_appetite"]

        context = PersonalizationEngine.build_context_from_text(text, symptoms)

        assert context.severity == "severe"  # 6 symptoms

    def test_build_context_inference_method(self):
        """Test extraction method is set to inference when no keywords found."""
        text = "My dog is not feeling well"
        symptoms = ["symptom1"]

        context = PersonalizationEngine.build_context_from_text(text, symptoms)

        assert context.extraction_method == "inference"


class TestPatientContext:
    """Test PatientContext data class."""

    def test_patient_context_defaults(self):
        """Test default values."""
        context = PatientContext()

        assert context.age_stage is None
        assert context.extracted_age_years is None
        assert context.severity == "moderate"
        assert context.confidence == 0.5

    def test_patient_context_initialization(self):
        """Test initialization with values."""
        context = PatientContext(
            age_stage="senior",
            extracted_age_years=8.5,
            severity="severe",
            confidence=0.9,
        )

        assert context.age_stage == "senior"
        assert context.extracted_age_years == 8.5
        assert context.severity == "severe"
        assert context.confidence == 0.9


class TestPersonalizeExtractionResult:
    """Test integration with extraction results."""

    def test_personalize_extraction_result(self):
        """Test adding personalization to extraction result."""
        extraction = {
            "symptoms": ["coughing", "fever"],
            "confidence": 0.85,
            "method": "claude",
        }
        text = "My 3 year old dog has coughing and fever"

        result = personalize_extraction_result(extraction, text)

        assert "personalization" in result
        assert result["personalization"]["age_stage"] == "adult"  # 3 years old is adult
        assert result["personalization"]["extracted_age_years"] == 3.0
        assert result["personalization"]["severity"] == "moderate"
        # Original fields should be preserved
        assert result["symptoms"] == ["coughing", "fever"]
        assert result["confidence"] == 0.85
