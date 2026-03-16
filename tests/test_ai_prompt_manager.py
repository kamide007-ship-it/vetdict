"""Tests for AI prompt manager module."""

from api.ai.prompt_manager import PromptManager, build_symptom_extraction_prompt


def test_prompt_manager_en():
    """Test prompt manager with English language."""
    manager = PromptManager(species="dog", language="en")

    system_prompt = manager.get_system_prompt()
    assert "veterinary" in system_prompt.lower()
    assert "json" in system_prompt.lower()

    user_prompt = manager.get_extraction_prompt(
        "coughing",
        ["coughing", "nasal_discharge"],
    )
    assert "coughing" in user_prompt
    assert "nasal_discharge" in user_prompt
    assert "dog" in user_prompt


def test_prompt_manager_ja():
    """Test prompt manager with Japanese language."""
    manager = PromptManager(species="dog", language="ja")

    system_prompt = manager.get_system_prompt()
    assert "獣医" in system_prompt
    assert "JSON" in system_prompt

    user_prompt = manager.get_extraction_prompt(
        "咳",
        ["coughing", "nasal_discharge"],
    )
    assert "咳" in user_prompt
    assert "dog" in user_prompt


def test_build_symptom_extraction_prompt_en():
    """Test prompt building function with English."""
    system, user = build_symptom_extraction_prompt(
        user_input="My dog has been coughing",
        species="dog",
        symptoms_list=["coughing", "nasal_discharge", "fever"],
        language="en",
    )

    assert len(system) > 0
    assert len(user) > 0
    assert "coughing" in user
    assert "nasal_discharge" in user
    assert "fever" in user
    assert "dog" in user
    assert "veterinary" in system.lower()


def test_build_symptom_extraction_prompt_ja():
    """Test prompt building function with Japanese."""
    system, user = build_symptom_extraction_prompt(
        user_input="犬が咳をしている",
        species="dog",
        symptoms_list=["coughing", "nasal_discharge"],
        language="ja",
    )

    assert len(system) > 0
    assert len(user) > 0
    assert "獣医" in system


def test_species_context():
    """Test that species context is included in prompts."""
    manager_dog = PromptManager(species="dog", language="en")
    manager_cat = PromptManager(species="cat", language="en")

    prompt_dog = manager_dog.get_extraction_prompt("test", ["symptom1"])
    prompt_cat = manager_cat.get_extraction_prompt("test", ["symptom1"])

    assert "dog" in prompt_dog
    assert "cat" in prompt_cat


def test_symptom_list_injection():
    """Test that symptom list is properly injected into prompts."""
    symptoms = ["symptom_a", "symptom_b", "symptom_c"]
    manager = PromptManager(species="dog", language="en")

    prompt = manager.get_extraction_prompt("test input", symptoms)

    for symptom in symptoms:
        assert symptom in prompt
