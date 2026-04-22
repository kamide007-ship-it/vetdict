"""Vaccination protection and disease prevention data.

Maps vaccines to the diseases they prevent and confidence reduction factors
when vaccination status is current. Supports species-specific vaccine protocols.
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class VaccineProtection:
    """Vaccine protection information for a disease."""

    disease_name: str
    vaccine_names: List[str]  # Common vaccine names (e.g., "DHPP", "Rabies")
    protection_effectiveness: float  # 0.0-1.0, how well vaccine prevents this disease
    confidence_reduction: float  # 0.3-0.8, factor to reduce confidence if vaccinated
    # confidence_reduction example: 0.5 = reduce to 50% of original, 0.3 = reduce to 30%
    notes: str = ""

    def to_dict(self):
        return {
            "disease_name": self.disease_name,
            "vaccine_names": self.vaccine_names,
            "protection_effectiveness": self.protection_effectiveness,
            "confidence_reduction": self.confidence_reduction,
            "notes": self.notes,
        }


# Vaccine-preventable diseases database
# Maps disease names to vaccination protection information
VACCINATION_PROTECTION: Dict[str, VaccineProtection] = {
    # ==================== DOG DISEASES ====================
    "Canine Parvovirus": VaccineProtection(
        disease_name="Canine Parvovirus",
        vaccine_names=["DHPP", "DPP", "5-in-1", "Parvovirus"],
        protection_effectiveness=0.95,  # Highly effective
        confidence_reduction=0.15,  # Reduce to 15% if vaccinated (85% reduction)
        notes="Core vaccine. Current vaccination makes parvovirus very unlikely.",
    ),
    "Canine Distemper": VaccineProtection(
        disease_name="Canine Distemper",
        vaccine_names=["DHPP", "DPP", "5-in-1", "Distemper"],
        protection_effectiveness=0.98,
        confidence_reduction=0.1,  # Reduce to 10% if vaccinated (90% reduction)
        notes="Core vaccine. Current vaccination makes distemper extremely unlikely.",
    ),
    "Rabies": VaccineProtection(
        disease_name="Rabies",
        vaccine_names=["Rabies"],
        protection_effectiveness=1.0,
        confidence_reduction=0.05,  # Reduce to 5% if vaccinated (95% reduction)
        notes="Core vaccine. Current vaccination essentially prevents rabies.",
    ),
    "Canine Hepatitis": VaccineProtection(
        disease_name="Canine Hepatitis",
        vaccine_names=["DHPP", "DPP", "5-in-1"],
        protection_effectiveness=0.90,
        confidence_reduction=0.2,
        notes="Core vaccine component.",
    ),
    "Leptospirosis": VaccineProtection(
        disease_name="Leptospirosis",
        vaccine_names=["DHPP", "Leptospira"],
        protection_effectiveness=0.80,  # Less effective than core vaccines
        confidence_reduction=0.3,
        notes="Non-core vaccine. Some protection; wanes over time.",
    ),
    "Bordetella Bronchiseptica": VaccineProtection(
        disease_name="Bordetella Bronchiseptica",
        vaccine_names=["Bordetella"],
        protection_effectiveness=0.75,
        confidence_reduction=0.4,
        notes="Non-core vaccine. Intranasal vaccine for kennel cough.",
    ),
    "Parainfluenza": VaccineProtection(
        disease_name="Parainfluenza",
        vaccine_names=["DHPP", "Parainfluenza"],
        protection_effectiveness=0.80,
        confidence_reduction=0.35,
        notes="Non-core vaccine. Part of kennel cough prevention.",
    ),
    # ==================== CAT DISEASES ====================
    "Feline Panleukopenia": VaccineProtection(
        disease_name="Feline Panleukopenia",
        vaccine_names=["FVRCP", "3-in-1"],
        protection_effectiveness=0.95,
        confidence_reduction=0.15,  # Reduce to 15% if vaccinated
        notes="Core vaccine. Current vaccination makes FPV very unlikely.",
    ),
    "Feline Herpes Virus (FHV-1)": VaccineProtection(
        disease_name="Feline Herpes Virus (FHV-1)",
        vaccine_names=["FVRCP", "3-in-1"],
        protection_effectiveness=0.80,
        confidence_reduction=0.3,
        notes="Core vaccine. Some protection against URD.",
    ),
    "Feline Calicivirus": VaccineProtection(
        disease_name="Feline Calicivirus",
        vaccine_names=["FVRCP", "3-in-1"],
        protection_effectiveness=0.75,
        confidence_reduction=0.35,
        notes="Core vaccine. Protection against some FCV strains.",
    ),
    "Feline Rabies": VaccineProtection(
        disease_name="Feline Rabies",
        vaccine_names=["Rabies"],
        protection_effectiveness=1.0,
        confidence_reduction=0.05,
        notes="Core vaccine. Current vaccination prevents rabies.",
    ),
    "Feline Leukemia (FeLV)": VaccineProtection(
        disease_name="Feline Leukemia (FeLV)",
        vaccine_names=["FeLV"],
        protection_effectiveness=0.85,
        confidence_reduction=0.25,
        notes="Non-core vaccine. Some protection; risk-based.",
    ),
    # ==================== RABBIT DISEASES ====================
    "Rabbit Myxomatosis": VaccineProtection(
        disease_name="Rabbit Myxomatosis",
        vaccine_names=["Myxomatosis"],
        protection_effectiveness=0.90,
        confidence_reduction=0.2,
        notes="Available in endemic areas. Provides good protection.",
    ),
    "Rabbit Hemorrhagic Disease (RHD)": VaccineProtection(
        disease_name="Rabbit Hemorrhagic Disease (RHD)",
        vaccine_names=["RHD", "VHD"],
        protection_effectiveness=0.95,
        confidence_reduction=0.15,
        notes="Vaccine available. Provides strong protection.",
    ),
    # ==================== FERRET DISEASES ====================
    "Ferret Distemper": VaccineProtection(
        disease_name="Ferret Distemper",
        vaccine_names=["Distemper", "CDV"],
        protection_effectiveness=0.95,
        confidence_reduction=0.1,
        notes="Important vaccine. Current vaccination makes distemper unlikely.",
    ),
    "Ferret Rabies": VaccineProtection(
        disease_name="Ferret Rabies",
        vaccine_names=["Rabies"],
        protection_effectiveness=1.0,
        confidence_reduction=0.05,
        notes="Rabies vaccine for ferrets provides complete protection.",
    ),
}


class VaccinationStatusHandler:
    """Handles vaccination status and disease confidence adjustment."""

    @classmethod
    def get_vaccination_protection(cls, disease_name: str) -> Optional[VaccineProtection]:
        """
        Get vaccination protection information for a disease.

        Args:
            disease_name: Name of the disease

        Returns:
            VaccineProtection if disease is vaccine-preventable, None otherwise
        """
        return VACCINATION_PROTECTION.get(disease_name)

    @classmethod
    def get_confidence_reduction(cls, disease_name: str, default: float = 1.0) -> float:
        """
        Get confidence reduction factor if vaccinated for a disease.

        Args:
            disease_name: Name of the disease
            default: Default factor if disease not vaccine-preventable (1.0 = no reduction)

        Returns:
            Confidence reduction factor (0.0-1.0)
        """
        protection = cls.get_vaccination_protection(disease_name)
        if protection:
            return protection.confidence_reduction
        return default

    @classmethod
    def is_vaccine_preventable(cls, disease_name: str) -> bool:
        """Check if a disease has vaccination protection data."""
        return disease_name in VACCINATION_PROTECTION

    @classmethod
    def apply_vaccination_adjustment(
        cls,
        disease_name: str,
        match_percent: int,
        vaccination_status: Optional[str] = None,
    ) -> tuple[int, bool]:
        """
        Apply vaccination status adjustment to disease confidence.

        Args:
            disease_name: Name of the disease
            match_percent: Current match percentage (0-100)
            vaccination_status: "current", "outdated", "none", or None

        Returns:
            Tuple of (adjusted_match_percent, adjustment_applied)
        """
        # No adjustment if vaccination status unknown or outdated/none
        if vaccination_status != "current":
            return match_percent, False

        # Get protection information
        protection = cls.get_vaccination_protection(disease_name)
        if not protection:
            return match_percent, False

        # Apply reduction factor
        adjusted_percent = int(match_percent * protection.confidence_reduction)
        return adjusted_percent, True

    @classmethod
    def apply_vaccination_to_diseases(
        cls,
        diseases: List[Dict],
        vaccination_status: Optional[str] = None,
    ) -> List[Dict]:
        """
        Apply vaccination status adjustment to multiple diseases.

        Args:
            diseases: List of disease dicts with "name" and "match_percent"
            vaccination_status: "current", "outdated", "none", or None

        Returns:
            List with adjusted match_percent for vaccine-preventable diseases
        """
        # No adjustment if no vaccination status provided
        if not vaccination_status or vaccination_status not in ("current", "outdated", "none"):
            return diseases

        adjusted = []
        for disease in diseases:
            disease_copy = disease.copy()
            disease_name = disease.get("name", "")

            # Apply vaccination adjustment
            original_percent = disease.get("match_percent", 0)
            adjusted_percent, adjustment_applied = cls.apply_vaccination_adjustment(
                disease_name, original_percent, vaccination_status
            )

            if adjustment_applied:
                disease_copy["match_percent_before_vaccination"] = original_percent
                disease_copy["match_percent"] = adjusted_percent
                disease_copy["vaccination_adjustment_applied"] = True
            else:
                disease_copy["vaccination_adjustment_applied"] = False

            adjusted.append(disease_copy)

        return adjusted
