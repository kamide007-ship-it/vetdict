"""prompt_manager.py – System and user prompt templates for Claude

Generates structured prompts for symptom extraction with species/language
context and enforces JSON response format.
"""

from typing import List, Tuple


class PromptManager:
    """Manages prompt generation for Claude symptom extraction."""

    def __init__(self, species: str = "dog", language: str = "en"):
        """
        Initialize prompt manager.

        Args:
            species: Animal species (dog, cat, horse, etc.)
            language: Language code ("en" or "ja")
        """
        self.species = species.lower()
        self.language = language.lower() if language else "en"

    def get_system_prompt(self) -> str:
        """
        Get system prompt defining Claude's role and behavior.

        Returns:
            System prompt string
        """
        if self.language == "ja":
            return """あなたは獣医診断支援AIです。ユーザーが自然言語で説明した症状を、
標準的な症状コードに変換します。

以下のルールに従ってください：
1. JSON形式で必ず応答してください
2. 症状が見つからなかった場合は空のリストを返してください
3. 確信度は0.0～1.0の数値で表してください
4. 不確実な症状は除外し、確信度を低く設定してください
5. 症状の理由づけを簡潔に提供してください"""
        else:
            return """You are a veterinary diagnostic support AI. Convert natural language
symptom descriptions into standardized symptom codes.

Follow these rules:
1. Always respond in JSON format
2. Return empty list if no symptoms found
3. Confidence is a number from 0.0 to 1.0
4. Exclude uncertain symptoms and set confidence lower
5. Provide brief reasoning for identified symptoms"""

    def get_extraction_prompt(
        self,
        user_text: str,
        available_symptoms: List[str],
    ) -> str:
        """
        Get user prompt with symptom list and user input.

        Args:
            user_text: User's symptom description
            available_symptoms: List of valid symptom IDs

        Returns:
            User prompt string
        """
        symptoms_str = ", ".join(sorted(available_symptoms))

        if self.language == "ja":
            return f"""患者: {self.species}

有効な症状コード: {symptoms_str}

患者の説明: "{user_text}"

以下のJSON形式で応答してください:
{{
  "extracted_symptoms": ["症状コード1", "症状コード2"],
  "confidence": 0.95,
  "reasoning": "抽出理由の簡潔な説明",
  "unmapped_expressions": ["マッピングされなかった表現"]
}}"""
        else:
            return f"""Patient species: {self.species}

Valid symptom codes: {symptoms_str}

Patient description: "{user_text}"

Respond in this JSON format:
{{
  "extracted_symptoms": ["symptom_code1", "symptom_code2"],
  "confidence": 0.95,
  "reasoning": "Brief explanation of extraction",
  "unmapped_expressions": ["expressions that didn't map"]
}}"""


def build_symptom_extraction_prompt(
    user_input: str,
    species: str,
    symptoms_list: List[str],
    language: str = "en",
) -> Tuple[str, str]:
    """
    Build system and user prompts for symptom extraction.

    Args:
        user_input: User's symptom description
        species: Animal species
        symptoms_list: Valid symptom IDs
        language: Language code ("en" or "ja")

    Returns:
        Tuple of (system_prompt, user_prompt)
    """
    manager = PromptManager(species=species, language=language)
    system_prompt = manager.get_system_prompt()
    user_prompt = manager.get_extraction_prompt(user_input, symptoms_list)
    return (system_prompt, user_prompt)
