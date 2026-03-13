"""Chief complaints (主訴) keyword mapping for VetDict.

Maps common chief complaint keywords to associated symptoms for quick
differential diagnosis. Enables auto-suggestion and auto-symptom-selection.

Structure:
  CHIEF_COMPLAINTS[species][keyword] = {
    "ja": "嘔吐",
    "en": "Vomiting",
    "common_symptoms": ["vomiting", "lethargy", "anorexia"],
    "frequency": 0.95,  # How common this chief complaint is
    "emergency": False,
  }
"""

from typing import Dict, List

# Chief complaints for dogs (犬の主訴)
CHIEF_COMPLAINTS_DOG: Dict[str, Dict] = {
    "嘔吐": {
        "ja": "嘔吐",
        "en": "Vomiting",
        "common_symptoms": ["vomiting", "lethargy", "anorexia", "dehydration"],
        "frequency": 0.95,
        "emergency": False,
    },
    "Vomiting": {
        "ja": "嘔吐",
        "en": "Vomiting",
        "common_symptoms": ["vomiting", "lethargy", "anorexia", "dehydration"],
        "frequency": 0.95,
        "emergency": False,
    },
    "下痢": {
        "ja": "下痢",
        "en": "Diarrhea",
        "common_symptoms": ["diarrhea", "vomiting", "lethargy", "dehydration"],
        "frequency": 0.92,
        "emergency": False,
    },
    "Diarrhea": {
        "ja": "下痢",
        "en": "Diarrhea",
        "common_symptoms": ["diarrhea", "vomiting", "lethargy", "dehydration"],
        "frequency": 0.92,
        "emergency": False,
    },
    "血便": {
        "ja": "血便",
        "en": "Bloody Stool",
        "common_symptoms": ["bloody_stool", "diarrhea", "vomiting", "lethargy"],
        "frequency": 0.75,
        "emergency": True,
    },
    "Bloody Stool": {
        "ja": "血便",
        "en": "Bloody Stool",
        "common_symptoms": ["bloody_stool", "diarrhea", "vomiting", "lethargy"],
        "frequency": 0.75,
        "emergency": True,
    },
    "咳": {
        "ja": "咳",
        "en": "Coughing",
        "common_symptoms": ["coughing", "difficulty_breathing", "lethargy", "fever"],
        "frequency": 0.88,
        "emergency": False,
    },
    "Coughing": {
        "ja": "咳",
        "en": "Coughing",
        "common_symptoms": ["coughing", "difficulty_breathing", "lethargy", "fever"],
        "frequency": 0.88,
        "emergency": False,
    },
    "元気がない": {
        "ja": "元気がない",
        "en": "Lethargy",
        "common_symptoms": ["lethargy", "fever", "anorexia", "weight_loss"],
        "frequency": 0.90,
        "emergency": False,
    },
    "Lethargy": {
        "ja": "元気がない",
        "en": "Lethargy",
        "common_symptoms": ["lethargy", "fever", "anorexia", "weight_loss"],
        "frequency": 0.90,
        "emergency": False,
    },
    "痒み": {
        "ja": "痒み",
        "en": "Itching",
        "common_symptoms": ["itching", "skin_redness", "hair_loss", "excessive_scratching"],
        "frequency": 0.85,
        "emergency": False,
    },
    "Itching": {
        "ja": "痒み",
        "en": "Itching",
        "common_symptoms": ["itching", "skin_redness", "hair_loss", "excessive_scratching"],
        "frequency": 0.85,
        "emergency": False,
    },
    "耳の痒み": {
        "ja": "耳の痒み",
        "en": "Ear Itching",
        "common_symptoms": ["ear_scratching", "ear_odor", "ear_discharge", "head_shaking"],
        "frequency": 0.82,
        "emergency": False,
    },
    "Ear Itching": {
        "ja": "耳の痒み",
        "en": "Ear Itching",
        "common_symptoms": ["ear_scratching", "ear_odor", "ear_discharge", "head_shaking"],
        "frequency": 0.82,
        "emergency": False,
    },
    "腹部膨満": {
        "ja": "腹部膨満",
        "en": "Bloating",
        "common_symptoms": ["bloating", "bloated_abdomen", "vomiting", "abdominal_pain", "restlessness"],
        "frequency": 0.70,
        "emergency": True,
    },
    "Bloating": {
        "ja": "腹部膨満",
        "en": "Bloating",
        "common_symptoms": ["bloating", "bloated_abdomen", "vomiting", "abdominal_pain", "restlessness"],
        "frequency": 0.70,
        "emergency": True,
    },
    "跛行": {
        "ja": "跛行",
        "en": "Limping",
        "common_symptoms": ["limping_fl", "limping_fr", "limping_rl", "limping_rr", "pain_on_touch"],
        "frequency": 0.78,
        "emergency": False,
    },
    "Limping": {
        "ja": "跛行",
        "en": "Limping",
        "common_symptoms": ["limping_fl", "limping_fr", "limping_rl", "limping_rr", "pain_on_touch"],
        "frequency": 0.78,
        "emergency": False,
    },
    "くしゃみ": {
        "ja": "くしゃみ",
        "en": "Sneezing",
        "common_symptoms": ["sneezing", "nasal_discharge", "eye_discharge", "coughing"],
        "frequency": 0.72,
        "emergency": False,
    },
    "Sneezing": {
        "ja": "くしゃみ",
        "en": "Sneezing",
        "common_symptoms": ["sneezing", "nasal_discharge", "eye_discharge", "coughing"],
        "frequency": 0.72,
        "emergency": False,
    },
    "体重減少": {
        "ja": "体重減少",
        "en": "Weight Loss",
        "common_symptoms": ["weight_loss", "anorexia", "lethargy", "excessive_thirst"],
        "frequency": 0.80,
        "emergency": False,
    },
    "Weight Loss": {
        "ja": "体重減少",
        "en": "Weight Loss",
        "common_symptoms": ["weight_loss", "anorexia", "lethargy", "excessive_thirst"],
        "frequency": 0.80,
        "emergency": False,
    },
    "飲水量増加": {
        "ja": "飲水量増加",
        "en": "Increased Thirst",
        "common_symptoms": ["excessive_thirst", "excessive_urination", "lethargy", "weight_loss"],
        "frequency": 0.75,
        "emergency": False,
    },
    "Increased Thirst": {
        "ja": "飲水量増加",
        "en": "Increased Thirst",
        "common_symptoms": ["excessive_thirst", "excessive_urination", "lethargy", "weight_loss"],
        "frequency": 0.75,
        "emergency": False,
    },
    "尿の異常": {
        "ja": "尿の異常",
        "en": "Urinary Issues",
        "common_symptoms": ["straining_urinate", "excessive_urination", "blood_urine", "incontinence"],
        "frequency": 0.68,
        "emergency": False,
    },
    "Urinary Issues": {
        "ja": "尿の異常",
        "en": "Urinary Issues",
        "common_symptoms": ["straining_urinate", "excessive_urination", "blood_urine", "incontinence"],
        "frequency": 0.68,
        "emergency": False,
    },
    "発熱": {
        "ja": "発熱",
        "en": "Fever",
        "common_symptoms": ["fever", "lethargy", "anorexia", "coughing"],
        "frequency": 0.70,
        "emergency": True,
    },
    "Fever": {
        "ja": "発熱",
        "en": "Fever",
        "common_symptoms": ["fever", "lethargy", "anorexia", "coughing"],
        "frequency": 0.70,
        "emergency": True,
    },
    "呼吸困難": {
        "ja": "呼吸困難",
        "en": "Difficulty Breathing",
        "common_symptoms": ["difficulty_breathing", "coughing", "rapid_breathing", "lethargy"],
        "frequency": 0.65,
        "emergency": True,
    },
    "Difficulty Breathing": {
        "ja": "呼吸困難",
        "en": "Difficulty Breathing",
        "common_symptoms": ["difficulty_breathing", "coughing", "rapid_breathing", "lethargy"],
        "frequency": 0.65,
        "emergency": True,
    },
    "痙攣": {
        "ja": "痙攣",
        "en": "Seizures",
        "common_symptoms": ["seizures", "lethargy", "collapse", "fever"],
        "frequency": 0.55,
        "emergency": True,
    },
    "Seizures": {
        "ja": "痙攣",
        "en": "Seizures",
        "common_symptoms": ["seizures", "lethargy", "collapse", "fever"],
        "frequency": 0.55,
        "emergency": True,
    },
}

# Chief complaints for cats (猫の主訴)
CHIEF_COMPLAINTS_CAT: Dict[str, Dict] = {
    "嘔吐": {
        "ja": "嘔吐",
        "en": "Vomiting",
        "common_symptoms": ["vomiting", "lethargy", "anorexia", "dehydration"],
        "frequency": 0.88,
        "emergency": False,
    },
    "Vomiting": {
        "ja": "嘔吐",
        "en": "Vomiting",
        "common_symptoms": ["vomiting", "lethargy", "anorexia", "dehydration"],
        "frequency": 0.88,
        "emergency": False,
    },
    "下痢": {
        "ja": "下痢",
        "en": "Diarrhea",
        "common_symptoms": ["diarrhea", "vomiting", "lethargy", "dehydration"],
        "frequency": 0.75,
        "emergency": False,
    },
    "Diarrhea": {
        "ja": "下痢",
        "en": "Diarrhea",
        "common_symptoms": ["diarrhea", "vomiting", "lethargy", "dehydration"],
        "frequency": 0.75,
        "emergency": False,
    },
    "元気がない": {
        "ja": "元気がない",
        "en": "Lethargy",
        "common_symptoms": ["lethargy", "fever", "anorexia", "weight_loss"],
        "frequency": 0.92,
        "emergency": False,
    },
    "Lethargy": {
        "ja": "元気がない",
        "en": "Lethargy",
        "common_symptoms": ["lethargy", "fever", "anorexia", "weight_loss"],
        "frequency": 0.92,
        "emergency": False,
    },
    "食欲不振": {
        "ja": "食欲不振",
        "en": "Anorexia",
        "common_symptoms": ["appetite_loss", "lethargy", "weight_loss", "fever"],
        "frequency": 0.85,
        "emergency": True,
    },
    "Anorexia": {
        "ja": "食欲不振",
        "en": "Anorexia",
        "common_symptoms": ["appetite_loss", "lethargy", "weight_loss", "fever"],
        "frequency": 0.85,
        "emergency": True,
    },
    "くしゃみ": {
        "ja": "くしゃみ",
        "en": "Sneezing",
        "common_symptoms": ["sneezing", "nasal_discharge", "eye_discharge", "coughing"],
        "frequency": 0.80,
        "emergency": False,
    },
    "Sneezing": {
        "ja": "くしゃみ",
        "en": "Sneezing",
        "common_symptoms": ["sneezing", "nasal_discharge", "eye_discharge", "coughing"],
        "frequency": 0.80,
        "emergency": False,
    },
    "飲水量増加": {
        "ja": "飲水量増加",
        "en": "Increased Thirst",
        "common_symptoms": ["excessive_thirst", "excessive_urination", "lethargy", "weight_loss"],
        "frequency": 0.78,
        "emergency": False,
    },
    "Increased Thirst": {
        "ja": "飲水量増加",
        "en": "Increased Thirst",
        "common_symptoms": ["excessive_thirst", "excessive_urination", "lethargy", "weight_loss"],
        "frequency": 0.78,
        "emergency": False,
    },
    "尿の異常": {
        "ja": "尿の異常",
        "en": "Urinary Issues",
        "common_symptoms": ["straining_urinate", "excessive_urination", "blood_urine", "incontinence"],
        "frequency": 0.72,
        "emergency": False,
    },
    "Urinary Issues": {
        "ja": "尿の異常",
        "en": "Urinary Issues",
        "common_symptoms": ["straining_urinate", "excessive_urination", "blood_urine", "incontinence"],
        "frequency": 0.72,
        "emergency": False,
    },
    "咳": {
        "ja": "咳",
        "en": "Coughing",
        "common_symptoms": ["coughing", "difficulty_breathing", "lethargy", "fever"],
        "frequency": 0.70,
        "emergency": False,
    },
    "Coughing": {
        "ja": "咳",
        "en": "Coughing",
        "common_symptoms": ["coughing", "difficulty_breathing", "lethargy", "fever"],
        "frequency": 0.70,
        "emergency": False,
    },
}

# All species chief complaints mapping
CHIEF_COMPLAINTS = {
    "dog": CHIEF_COMPLAINTS_DOG,
    "cat": CHIEF_COMPLAINTS_CAT,
}

def get_chief_complaints(species: str = "dog") -> Dict[str, Dict]:
    """Get chief complaints for a specific species.

    Args:
        species: Species ID (e.g., "dog", "cat")

    Returns:
        Dictionary mapping keywords to complaint data
    """
    return CHIEF_COMPLAINTS.get(species, CHIEF_COMPLAINTS_DOG)


def get_chief_complaint_keywords(species: str = "dog", lang: str = "ja") -> List[str]:
    """Get unique chief complaint keywords for a species.

    Args:
        species: Species ID
        lang: Language ("ja" or "en")

    Returns:
        List of keywords for the language
    """
    complaints = get_chief_complaints(species)
    keywords = set()
    for key, data in complaints.items():
        # Add both the key and the display name
        keywords.add(key)
        if lang in data:
            keywords.add(data[lang])
    return sorted(list(keywords))


def get_symptoms_for_complaint(species: str, keyword: str) -> List[str]:
    """Get auto-check symptoms for a chief complaint keyword.

    Args:
        species: Species ID
        keyword: Chief complaint keyword (Japanese or English)

    Returns:
        List of symptom IDs to auto-check
    """
    complaints = get_chief_complaints(species)
    if keyword not in complaints:
        return []

    return complaints[keyword].get("common_symptoms", [])


def is_emergency_complaint(species: str, keyword: str) -> bool:
    """Check if a chief complaint is an emergency.

    Args:
        species: Species ID
        keyword: Chief complaint keyword

    Returns:
        True if emergency, False otherwise
    """
    complaints = get_chief_complaints(species)
    if keyword not in complaints:
        return False

    return complaints[keyword].get("emergency", False)
