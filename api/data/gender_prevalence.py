"""Gender-based disease prevalence data.

Provides gender-specific risk multipliers for diseases where gender affects
susceptibility or prevalence. Supports both English and Japanese keywords.
"""

import logging
from dataclasses import dataclass
from typing import Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class GenderContext:
    """Extracted gender information."""

    gender: Optional[str] = None  # "male" | "female" | None
    confidence: float = 0.5  # How confident we are in the gender extraction
    extraction_method: str = "unknown"  # "text_extraction" | "user_input" | "inference"


# Gender keywords for English and Japanese
GENDER_KEYWORDS = {
    "en": {
        "male": (
            [
                "male",
                "boy",
                "tom",
                "tomcat",
                "boar",
                "buck",
                "stallion",
                "ram",
                "rooster",
                "cock",
                "drake",
                "♂",
            ],
            0.85,
        ),
        "female": (
            [
                "female",
                "girl",
                "queen",
                "doe",
                "sow",
                "mare",
                "ewe",
                "hen",
                "duck",
                "♀",
            ],
            0.85,
        ),
    },
    "ja": {
        "male": (
            ["オス", "男の子", "息子", "牡", "雄"],
            0.9,
        ),
        "female": (
            ["メス", "女の子", "娘", "牝", "雌"],
            0.9,
        ),
    },
}

# Gender-based disease risk multipliers
# Format: {species: {disease_name: {gender: multiplier}}}
# Multiplier > 1.0 = higher risk for this gender
# Multiplier < 1.0 = lower risk for this gender

GENDER_RISK_MULTIPLIERS: Dict[str, Dict[str, Dict[str, float]]] = {
    "dog": {
        # Reproductive system diseases
        "Prostate Disease": {"male": 2.5, "female": 0.0},
        "Prostate Cancer": {"male": 2.5, "female": 0.0},
        "Benign Prostatic Hyperplasia": {"male": 2.5, "female": 0.0},
        "Prostatitis": {"male": 2.5, "female": 0.0},
        "Testicular Cancer": {"male": 2.5, "female": 0.0},
        "Testicular Torsion": {"male": 2.0, "female": 0.0},
        "Cryptorchidism": {"male": 2.0, "female": 0.0},
        "Pyometra": {"male": 0.0, "female": 2.5},
        "Uterine Stump Pyometra": {"male": 0.0, "female": 2.5},
        "Uterine Infection": {"male": 0.0, "female": 2.5},
        "Ovarian Cysts": {"male": 0.0, "female": 1.8},
        "Mammary Gland Tumors": {"male": 0.1, "female": 2.0},
        "Mammary Cancer": {"male": 0.1, "female": 2.0},
        # Urinary system
        "Urinary Tract Infection": {"male": 0.8, "female": 1.3},
        "Bladder Stones": {"male": 1.3, "female": 1.5},
        "Urolithiasis": {"male": 1.3, "female": 1.5},
        # Hip Dysplasia (slight male bias in some studies)
        "Hip Dysplasia": {"male": 1.1, "female": 1.0},
        # Cryptorchidism-related conditions
        "Inguinal Hernia": {"male": 1.5, "female": 1.0},
        # Behavioral/neutering-related
        "Hemangiosarcoma": {"male": 1.2, "female": 1.0},
    },
    "cat": {
        # Reproductive system diseases
        "Pyometra": {"male": 0.0, "female": 2.5},
        "Feline Pyometra": {"male": 0.0, "female": 2.5},
        "Uterine Infection": {"male": 0.0, "female": 2.5},
        "Ovarian Cysts": {"male": 0.0, "female": 1.8},
        "Testicular Cancer": {"male": 2.0, "female": 0.0},
        "Mammary Gland Tumors": {"male": 0.1, "female": 2.0},
        "Feline Mammary Gland Tumors": {"male": 0.1, "female": 2.0},
        # Urinary system - females more prone to certain FLUTD
        "Feline Lower Urinary Tract Disease (FLUTD)": {"male": 1.5, "female": 1.0},
        "FLUTD": {"male": 1.5, "female": 1.0},
        "Feline Urinary Obstruction": {"male": 2.5, "female": 1.0},
        "Urinary Obstruction": {"male": 2.5, "female": 1.0},
        "Feline Urolitiasis": {"male": 1.8, "female": 1.3},
        # FIP slightly more common in males in some studies
        "Feline Infectious Peritonitis (FIP)": {"male": 1.2, "female": 1.0},
    },
    "rabbit": {
        # Reproductive system diseases
        "Pyometra": {"male": 0.0, "female": 2.0},
        "Uterine Adenocarcinoma": {"male": 0.0, "female": 2.5},
        "Ovarian Cysts": {"male": 0.0, "female": 1.5},
        "Testicular Cancer": {"male": 1.5, "female": 0.0},
        # Mammary-related
        "Mammary Gland Tumors": {"male": 0.1, "female": 1.8},
    },
    "hamster": {
        # Syrian hamster females: pyometra risk
        "Hamster Pyometra": {"male": 0.0, "female": 2.0},
        "Pyometra": {"male": 0.0, "female": 2.0},
        "Ovarian Cysts": {"male": 0.0, "female": 1.5},
    },
    "guinea_pig": {
        # Guinea pig females: ovarian cysts, reproductive disease
        "Ovarian Cysts": {"male": 0.0, "female": 2.5},
        "Pyometra": {"male": 0.0, "female": 2.0},
        "Uterine Adenocarcinoma": {"male": 0.0, "female": 1.8},
    },
    "ferret": {
        # Adrenal disease slightly more in females (spayed)
        "Adrenal Disease": {"male": 1.0, "female": 1.3},
        # Reproductive cancers
        "Testicular Tumor": {"male": 2.0, "female": 0.0},
        "Ovarian Tumor": {"male": 0.0, "female": 1.8},
    },
    "bird": {
        # Egg binding in females only
        "Egg Binding": {"male": 0.0, "female": 3.0},
        "Chronic Egg Laying": {"male": 0.0, "female": 2.5},
        # Testicular tumors in males
        "Testicular Tumor": {"male": 1.8, "female": 0.0},
    },
    "parakeet": {
        "Egg Binding": {"male": 0.0, "female": 3.0},
        "Chronic Egg Laying": {"male": 0.0, "female": 2.5},
    },
    "parrot": {
        "Egg Binding": {"male": 0.0, "female": 3.0},
        "Chronic Egg Laying": {"male": 0.0, "female": 2.5},
        "Feather Plucking": {"male": 1.0, "female": 1.2},  # Slight female bias
    },
    "reptile": {
        "Egg Binding": {"male": 0.0, "female": 3.0},
        "Reproductive Disorder": {"male": 0.0, "female": 1.8},
    },
    "snake": {
        "Egg Binding": {"male": 0.0, "female": 3.0},
        "Inclusion Body Disease (IBD)": {"male": 1.0, "female": 1.0},
    },
    "lizard": {
        "Egg Binding": {"male": 0.0, "female": 3.0},
        "Metabolic Bone Disease": {"male": 1.0, "female": 1.3},  # Females laying eggs need more calcium
    },
    "tortoise": {
        "Egg Binding": {"male": 0.0, "female": 3.0},
        "Reproductive Disorder": {"male": 0.0, "female": 1.8},
    },
    "horse": {
        # Reproductive system diseases
        "Cryptorchidism": {"male": 2.0, "female": 0.0},
        "Equine Herpes Virus": {"male": 1.0, "female": 1.2},  # Pregnant mares more susceptible
        "Prepuce Infection (Smegma)": {"male": 3.0, "female": 0.0},
    },
}


class GenderExtractor:
    """Extracts gender information from natural language text."""

    @classmethod
    def extract(cls, text: str) -> GenderContext:
        """
        Extract gender from natural language text.

        Args:
            text: User input describing patient

        Returns:
            GenderContext with extracted gender information
        """
        if not text or not isinstance(text, str):
            return GenderContext()

        # Try English keywords first
        for gender, (keywords, confidence) in GENDER_KEYWORDS["en"].items():
            text_lower = text.lower()
            for keyword in keywords:
                if keyword in text_lower:
                    return GenderContext(
                        gender=gender,
                        confidence=confidence,
                        extraction_method="text_extraction",
                    )

        # Try Japanese keywords
        for gender, (keywords, confidence) in GENDER_KEYWORDS["ja"].items():
            for keyword in keywords:
                if keyword in text:
                    return GenderContext(
                        gender=gender,
                        confidence=confidence,
                        extraction_method="text_extraction",
                    )

        # No gender found
        return GenderContext()

    @classmethod
    def normalize_gender(cls, gender_str: Optional[str]) -> Optional[str]:
        """
        Normalize gender string to standard format.

        Args:
            gender_str: Raw gender string (e.g., "M", "F", "male", "メス")

        Returns:
            Normalized gender ("male" | "female" | None)
        """
        if not gender_str or not isinstance(gender_str, str):
            return None

        gender_lower = gender_str.lower().strip()

        # Common abbreviations and variations
        if gender_lower in ("m", "male", "boy", "tom", "boar", "buck"):
            return "male"
        if gender_lower in ("f", "female", "girl", "queen", "doe", "sow"):
            return "female"

        # Try extracting first character
        if gender_lower and gender_lower[0] in ("m", "b", "t"):
            return "male"
        if gender_lower and gender_lower[0] in ("f", "g", "q"):
            return "female"

        return None
