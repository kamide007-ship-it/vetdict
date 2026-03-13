"""Symptom role classifier for pathophysiology-aware diagnosis.

Classifies the role of symptoms (primary, secondary, complication) in disease
pathophysiology, enabling more accurate multi-disease diagnosis.
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class SymptomRoleAnalysis:
    """Analysis of symptom's role in disease pathophysiology."""

    symptom_id: str
    symptom_name: str
    disease_name: str
    primary_role: str  # "primary", "secondary", "complication", "warning_sign"
    primary_confidence: float  # Confidence in primary role classification
    alternative_roles: List[Tuple[str, float]]  # [(role, confidence), ...]
    pathophysiology_explanation: str
    clinical_significance: str  # "essential", "important", "minor", "coincidental"
    appears_early_in_course: bool  # In disease progression timeline
    reversible_with_treatment: bool
    associations_with_other_symptoms: List[str]


class SymptomRoleAnalyzer:
    """Analyzes symptom roles based on pathophysiology."""

    # Role hierarchy: primary < secondary < complication
    ROLE_HIERARCHY = {
        "primary": 0,
        "secondary": 1,
        "complication": 2,
        "warning_sign": -1,  # Most important
        "coincidental": 3,
    }

    # Keywords indicating symptom type in descriptions
    PRIMARY_KEYWORDS = {
        "主症状": 0.9,
        "main symptom": 0.9,
        "primary symptom": 0.9,
        "chief complaint": 0.85,
        "初期症状": 0.85,
        "early sign": 0.8,
        "classic": 0.8,
        "典型的": 0.8,
    }

    SECONDARY_KEYWORDS = {
        "二次症状": 0.7,
        "secondary symptom": 0.7,
        "accompanying": 0.65,
        "associated": 0.6,
        "続発症状": 0.7,
        "伴随": 0.65,
    }

    COMPLICATION_KEYWORDS = {
        "合併症": 0.8,
        "complication": 0.8,
        "consequence": 0.75,
        "develops from": 0.7,
        "secondary to": 0.7,
        "as a result of": 0.65,
    }

    @classmethod
    def analyze_symptom_role(
        cls,
        symptom_id: str,
        symptom_name: str,
        disease: Dict[str, Any],
    ) -> SymptomRoleAnalysis:
        """
        Analyze the role of a symptom in a disease's pathophysiology.

        Args:
            symptom_id: ID of the symptom
            symptom_name: Display name of symptom
            disease: Disease record from database

        Returns:
            SymptomRoleAnalysis with detailed role information
        """

        # Get pathophysiology information
        pathophysiology = disease.get("pathophysiology", disease.get("description", ""))
        symptoms_list = disease.get("symptoms", [])
        complications = disease.get("complications", [])
        disease_name = disease.get("name", disease.get("name_ja", ""))

        # Determine primary role
        primary_role, role_confidence = cls._determine_primary_role(
            symptom_id,
            symptom_name,
            symptoms_list,
            pathophysiology,
            complications,
        )

        # Analyze pathophysiology connection
        patho_explanation = cls._explain_pathophysiology(
            symptom_name, pathophysiology, primary_role
        )

        # Determine clinical significance
        significance = cls._assess_clinical_significance(
            primary_role, role_confidence, disease.get("severity_score", 0.5)
        )

        # Check progression timing
        appears_early = cls._check_early_appearance(
            symptom_name, pathophysiology, disease
        )

        # Check reversibility
        reversible = cls._check_reversibility(
            symptom_name, disease, primary_role
        )

        # Get alternative roles
        alternatives = cls._get_alternative_roles(
            primary_role, role_confidence
        )

        # Find associated symptoms
        associations = cls._find_symptom_associations(
            symptom_name, disease
        )

        analysis = SymptomRoleAnalysis(
            symptom_id=symptom_id,
            symptom_name=symptom_name,
            disease_name=disease_name,
            primary_role=primary_role,
            primary_confidence=role_confidence,
            alternative_roles=alternatives,
            pathophysiology_explanation=patho_explanation,
            clinical_significance=significance,
            appears_early_in_course=appears_early,
            reversible_with_treatment=reversible,
            associations_with_other_symptoms=associations,
        )

        return analysis

    @classmethod
    def _determine_primary_role(
        cls,
        symptom_id: str,
        symptom_name: str,
        symptoms_list: List[str],
        pathophysiology: str,
        complications: List[str],
    ) -> Tuple[str, float]:
        """
        Determine primary role of symptom using multiple signals.

        Returns:
            (role, confidence)
        """

        # Signal 1: Position in symptom list (earlier = more primary)
        position_score = cls._score_by_position(symptom_id, symptom_name, symptoms_list)

        # Signal 2: Keywords in pathophysiology
        keyword_scores = cls._score_by_keywords(symptom_name, pathophysiology)

        # Signal 3: Complication list membership
        complication_score = cls._score_complication_membership(
            symptom_id, symptom_name, complications
        )

        # Signal 4: Symptom-disease name similarity
        name_similarity_score = cls._score_name_similarity(symptom_name, pathophysiology)

        # Combine signals (weighted)
        weights = {
            "position": 0.3,
            "keywords": 0.35,
            "complication": 0.2,
            "similarity": 0.15,
        }

        combined_score = (
            position_score * weights["position"]
            + keyword_scores.get("combined", 0.5) * weights["keywords"]
            + complication_score * weights["complication"]
            + name_similarity_score * weights["similarity"]
        )

        # Determine role based on scores and signals
        if keyword_scores.get("primary", 0) > 0.6:
            return "primary", min(1.0, 0.9 + combined_score * 0.1)
        elif keyword_scores.get("complication", 0) > 0.6:
            return "complication", min(1.0, keyword_scores.get("complication", 0.6))
        elif position_score > 0.7:
            return "primary", position_score
        elif complication_score > 0.6:
            return "complication", complication_score
        elif position_score > 0.4:
            return "secondary", position_score
        else:
            return "secondary", 0.5

    @staticmethod
    def _score_by_position(
        symptom_id: str,
        symptom_name: str,
        symptoms_list: List[str],
    ) -> float:
        """Score symptom importance by its position in symptom list."""
        if not symptoms_list:
            return 0.5

        # Find position
        position = None
        for i, symptom in enumerate(symptoms_list):
            if symptom_id in str(symptom) or symptom_name.lower() in str(symptom).lower():
                position = i
                break

        if position is None:
            return 0.0

        # Earlier position = higher importance
        # Score decreases from 1.0 to 0.3 across list
        max_position = len(symptoms_list)
        score = 1.0 - (position / max(max_position, 1)) * 0.7
        return score

    @staticmethod
    def _score_by_keywords(symptom_name: str, pathophysiology: str) -> Dict[str, float]:
        """Score symptom role using keywords in pathophysiology."""
        patho_lower = pathophysiology.lower()
        symptom_lower = symptom_name.lower()

        scores = {
            "primary": 0.0,
            "secondary": 0.0,
            "complication": 0.0,
            "combined": 0.5,
        }

        # Check primary keywords
        for keyword, score in SymptomRoleAnalyzer.PRIMARY_KEYWORDS.items():
            if keyword.lower() in patho_lower and symptom_lower in patho_lower:
                # Keyword appears near symptom name
                scores["primary"] = max(scores["primary"], score)

        # Check secondary keywords
        for keyword, score in SymptomRoleAnalyzer.SECONDARY_KEYWORDS.items():
            if keyword.lower() in patho_lower and symptom_lower in patho_lower:
                scores["secondary"] = max(scores["secondary"], score)

        # Check complication keywords
        for keyword, score in SymptomRoleAnalyzer.COMPLICATION_KEYWORDS.items():
            if keyword.lower() in patho_lower and symptom_lower in patho_lower:
                scores["complication"] = max(scores["complication"], score)

        # Combined score (weighted by role)
        scores["combined"] = (
            scores["primary"] * 0.4
            + scores["secondary"] * 0.3
            + scores["complication"] * 0.3
        )

        return scores

    @staticmethod
    def _score_complication_membership(
        symptom_id: str,
        symptom_name: str,
        complications: List[str],
    ) -> float:
        """Check if symptom is listed in complications."""
        if not complications:
            return 0.0

        for complication in complications:
            if symptom_id in str(complication) or symptom_name.lower() in str(complication).lower():
                return 0.8  # High confidence if explicitly listed as complication
        return 0.0

    @staticmethod
    def _score_name_similarity(symptom_name: str, pathophysiology: str) -> float:
        """Score based on how prominently symptom is mentioned in pathophysiology."""
        symptom_lower = symptom_name.lower()
        patho_lower = pathophysiology.lower()

        if symptom_lower not in patho_lower:
            return 0.0

        # Count occurrences (more = more important)
        occurrence_count = patho_lower.count(symptom_lower)

        # Position of first mention (earlier = more important)
        first_mention = patho_lower.find(symptom_lower)
        position_ratio = first_mention / max(len(pathophysiology), 1)

        # Combine: multiple mentions + early position = higher score
        score = min(0.9, (occurrence_count * 0.2) + (1.0 - position_ratio * 0.5))
        return score

    @staticmethod
    def _assess_clinical_significance(
        primary_role: str,
        role_confidence: float,
        disease_severity: float,
    ) -> str:
        """Assess clinical significance of symptom."""
        if primary_role == "primary" and role_confidence > 0.7:
            return "essential"
        elif primary_role in ["primary", "warning_sign"]:
            return "important"
        elif primary_role == "secondary" and role_confidence > 0.6:
            return "important"
        elif primary_role == "complication" and disease_severity > 0.6:
            return "important"
        else:
            return "minor"

    @staticmethod
    def _check_early_appearance(
        symptom_name: str,
        pathophysiology: str,
        disease: Dict[str, Any],
    ) -> bool:
        """Check if symptom appears early in disease course."""
        symptoms_list = disease.get("symptoms", [])

        if not symptoms_list:
            return False

        # Symptoms at beginning of list typically appear early
        symptom_lower = symptom_name.lower()
        for i, sym in enumerate(symptoms_list[:3]):  # Check first 3
            if symptom_lower in str(sym).lower():
                return True

        # Check pathophysiology for early-stage keywords
        patho_lower = pathophysiology.lower()
        early_keywords = [
            "initially", "early", "開始時", "最初", "最初の症状",
            "first manifestation", "早期"
        ]

        for keyword in early_keywords:
            if keyword in patho_lower and symptom_lower in patho_lower:
                return True

        return False

    @staticmethod
    def _check_reversibility(
        symptom_name: str,
        disease: Dict[str, Any],
        primary_role: str,
    ) -> bool:
        """Check if symptom is reversible with treatment."""
        # Structural complications are often irreversible
        structural_keywords = [
            "fibrosis", "atrophy", "necrosis", "death",
            "scarring", "degeneration", "permanent",
            "線維化", "萎縮", "壊死", "瘢痕化"
        ]

        pathophysiology = disease.get("pathophysiology", "").lower()

        for keyword in structural_keywords:
            if keyword in pathophysiology and symptom_name.lower() in pathophysiology:
                return False

        # Primary symptoms are usually reversible, complications often not
        if primary_role == "complication":
            return False
        elif primary_role in ["primary", "secondary"]:
            return True

        # Default: assume reversible
        return True

    @staticmethod
    def _explain_pathophysiology(
        symptom_name: str,
        pathophysiology: str,
        primary_role: str,
    ) -> str:
        """Generate explanation of symptom's pathophysiological connection."""
        if not pathophysiology:
            return f"{symptom_name} appears in this disease."

        # Extract relevant portion of pathophysiology
        symptom_lower = symptom_name.lower()
        patho_lower = pathophysiology.lower()

        # Find sentence containing symptom
        sentences = pathophysiology.split(". ")
        for sentence in sentences:
            if symptom_lower in sentence.lower():
                return sentence.strip()

        # If no direct mention, return first sentence
        if sentences:
            return sentences[0].strip()

        return pathophysiology[:200]

    @staticmethod
    def _get_alternative_roles(
        primary_role: str,
        confidence: float,
    ) -> List[Tuple[str, float]]:
        """Get alternative possible roles with confidences."""
        all_roles = ["primary", "secondary", "complication", "warning_sign"]
        alternatives = []

        for role in all_roles:
            if role != primary_role:
                # Alternative confidence decreases with primary confidence
                if role == "primary" and primary_role == "secondary":
                    alt_conf = (1.0 - confidence) * 0.7
                elif role == "secondary" and primary_role == "primary":
                    alt_conf = (1.0 - confidence) * 0.5
                else:
                    alt_conf = (1.0 - confidence) * 0.3

                if alt_conf > 0.1:
                    alternatives.append((role, round(alt_conf, 2)))

        return sorted(alternatives, key=lambda x: x[1], reverse=True)

    @staticmethod
    def _find_symptom_associations(
        symptom_name: str,
        disease: Dict[str, Any],
    ) -> List[str]:
        """Find other symptoms that typically accompany this symptom."""
        symptom_lower = symptom_name.lower()
        symptoms_list = disease.get("symptoms", [])

        # Get symptoms that appear near target symptom in the list
        associations = []

        for i, sym in enumerate(symptoms_list):
            if symptom_lower in str(sym).lower():
                # Get nearby symptoms (±2 positions)
                for j in range(max(0, i - 2), min(len(symptoms_list), i + 3)):
                    if i != j:
                        nearby = str(symptoms_list[j])
                        if nearby not in associations:
                            associations.append(nearby)

        return associations[:5]  # Return top 5


class RoleClassifier:
    """High-level role classifier for symptom-disease pairs."""

    @classmethod
    def classify_symptom_roles(
        cls,
        symptom_ids: List[str],
        symptom_names: Optional[Dict[str, str]] = None,
        disease_candidates: List[Dict[str, Any]] = None,
    ) -> Dict[str, Dict[str, SymptomRoleAnalysis]]:
        """
        Classify roles for all symptoms across all disease candidates.

        Args:
            symptom_ids: List of symptom IDs
            symptom_names: Mapping of symptom_id to display name
            disease_candidates: List of candidate diseases

        Returns:
            {disease_name: {symptom_id: SymptomRoleAnalysis, ...}, ...}
        """
        if symptom_names is None:
            symptom_names = {}
        if disease_candidates is None:
            disease_candidates = []

        result = {}

        for disease in disease_candidates:
            disease_name = disease.get("name", disease.get("name_ja", ""))
            roles = {}

            for symptom_id in symptom_ids:
                symptom_name = symptom_names.get(symptom_id, symptom_id)

                role_analysis = SymptomRoleAnalyzer.analyze_symptom_role(
                    symptom_id=symptom_id,
                    symptom_name=symptom_name,
                    disease=disease,
                )

                roles[symptom_id] = role_analysis

            if roles:
                result[disease_name] = roles

        return result

    @classmethod
    def get_primary_symptoms(
        cls,
        disease: Dict[str, Any],
        symptom_ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Get list of primary symptoms for a disease."""
        symptoms_list = disease.get("symptoms", [])

        if symptom_ids:
            # Filter to specific symptoms
            primary = []
            for symptom_id in symptom_ids:
                role_analysis = SymptomRoleAnalyzer.analyze_symptom_role(
                    symptom_id, symptom_id, disease
                )
                if role_analysis.primary_role == "primary":
                    primary.append(symptom_id)
            return primary
        else:
            # Return top 3 symptoms
            return symptoms_list[:3] if symptoms_list else []

    @classmethod
    def get_complication_symptoms(
        cls,
        disease: Dict[str, Any],
    ) -> List[str]:
        """Get list of symptoms that are complications of disease."""
        return disease.get("complications", [])
