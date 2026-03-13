"""Symptom context engine for multi-disease diagnosis.

Contextualizes symptoms within the framework of multiple disease hypotheses,
identifying ambiguous symptoms and their medical significance across diseases.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum
import logging
import math

logger = logging.getLogger(__name__)


class SymptomRole(Enum):
    """Role of symptom in disease pathophysiology."""
    PRIMARY_SYMPTOM = "primary_symptom"
    SECONDARY_SYMPTOM = "secondary_symptom"
    COMPLICATION = "complication"
    PATHOGNOMONIC = "pathognomonic"  # Highly specific to disease
    NON_SPECIFIC = "non_specific"  # Present in many diseases


@dataclass
class SymptomContext:
    """Medical context of a symptom within a specific disease."""

    symptom_id: str
    symptom_name: str
    disease_name: str
    context_role: SymptomRole  # Primary/secondary/complication
    pathophysiology_link: str  # Mechanism connecting symptom to disease
    specificity_score: float  # How specific is symptom to this disease (0-1)
    sensitivity_score: float  # How often symptom appears in disease (0-1)
    likelihood_ratio_positive: float  # LR+ for diagnostic utility
    likelihood_ratio_negative: float  # LR- for diagnostic utility
    confidence_weight: float  # Context-specific confidence weight (0-1)
    supporting_evidence: List[str] = field(default_factory=list)  # Evidence citations
    related_findings: List[str] = field(default_factory=list)  # Often accompanies

    def to_dict(self):
        """Serialize to dictionary."""
        return {
            "symptom_id": self.symptom_id,
            "symptom_name": self.symptom_name,
            "disease_name": self.disease_name,
            "context_role": self.context_role.value,
            "pathophysiology_link": self.pathophysiology_link,
            "specificity_score": round(self.specificity_score, 3),
            "sensitivity_score": round(self.sensitivity_score, 3),
            "likelihood_ratio_positive": round(self.likelihood_ratio_positive, 3),
            "likelihood_ratio_negative": round(self.likelihood_ratio_negative, 3),
            "confidence_weight": round(self.confidence_weight, 3),
            "supporting_evidence": self.supporting_evidence,
            "related_findings": self.related_findings,
        }


@dataclass
class AmbiguityReport:
    """Comprehensive ambiguity analysis for a symptom."""

    symptom_id: str
    symptom_name: str
    ambiguity_score: float  # 0 (clear) to 1 (highly ambiguous)
    entropy_score: float  # Information entropy across diseases
    contexts: Dict[str, SymptomContext]  # Context per disease
    disease_count_with_symptom: int  # How many diseases have this symptom
    predominant_disease: Optional[str]  # Most likely disease
    competing_diseases: List[str]  # Other likely diseases
    recommendation: str  # "keep_all", "reduce_confidence", "ask_clarification"
    clarification_questions: List[str] = field(default_factory=list)  # To resolve ambiguity
    confidence_adjustment_factor: float = 1.0  # Multiplier for confidence scores
    explanation_ja: str = ""
    explanation_en: str = ""

    def to_dict(self):
        """Serialize to dictionary."""
        return {
            "symptom_id": self.symptom_id,
            "symptom_name": self.symptom_name,
            "ambiguity_score": round(self.ambiguity_score, 3),
            "entropy_score": round(self.entropy_score, 3),
            "contexts": {
                disease: ctx.to_dict()
                for disease, ctx in self.contexts.items()
            },
            "disease_count_with_symptom": self.disease_count_with_symptom,
            "predominant_disease": self.predominant_disease,
            "competing_diseases": self.competing_diseases,
            "recommendation": self.recommendation,
            "clarification_questions": self.clarification_questions,
            "confidence_adjustment_factor": round(self.confidence_adjustment_factor, 3),
            "explanation_ja": self.explanation_ja,
            "explanation_en": self.explanation_en,
        }


class SymptomContextualizer:
    """Contextualizes symptoms within multiple disease hypotheses."""

    # Thresholds for ambiguity
    HIGH_AMBIGUITY_THRESHOLD = 0.6
    MODERATE_AMBIGUITY_THRESHOLD = 0.4
    LOW_AMBIGUITY_THRESHOLD = 0.2

    # Score thresholds for roles
    PATHOGNOMONIC_THRESHOLD = 0.85  # LR+ > 10, LR- < 0.1
    PRIMARY_SYMPTOM_SPECIFICITY = 0.70
    SECONDARY_SYMPTOM_SPECIFICITY = 0.40

    @staticmethod
    def contextualize_symptom(
        symptom_id: str,
        symptom_name: str,
        disease_names: List[str],
        disease_database: List[Dict[str, Any]],
        prevalence_data: Optional[Dict[str, float]] = None,
    ) -> Dict[str, SymptomContext]:
        """
        Contextualize a symptom across multiple diseases.

        Args:
            symptom_id: ID of the symptom
            symptom_name: Display name of symptom
            disease_names: List of candidate diseases
            disease_database: Complete disease database
            prevalence_data: Optional prevalence data for Bayesian adjustment

        Returns:
            Dictionary mapping disease name to SymptomContext
        """
        contexts = {}

        for disease_name in disease_names:
            # Find disease in database
            disease = next(
                (d for d in disease_database
                 if d.get("name", "") == disease_name or d.get("name_ja", "") == disease_name),
                None
            )

            if not disease:
                continue

            # Build context
            context = SymptomContextualizer._build_symptom_context(
                symptom_id=symptom_id,
                symptom_name=symptom_name,
                disease=disease,
            )

            if context:
                contexts[disease_name] = context

        return contexts

    @staticmethod
    def _build_symptom_context(
        symptom_id: str,
        symptom_name: str,
        disease: Dict[str, Any],
    ) -> Optional[SymptomContext]:
        """
        Build SymptomContext for single disease.

        Extracts pathophysiology, specificity, sensitivity from disease database.
        """
        disease_name = disease.get("name", disease.get("name_ja", ""))

        # Get symptoms from disease entry
        disease_symptoms = disease.get("symptoms", [])
        if isinstance(disease_symptoms, str):
            disease_symptoms = [disease_symptoms]

        # Check if symptom is present
        symptom_present = any(
            symptom_id in sym or symptom_name.lower() in str(sym).lower()
            for sym in disease_symptoms
        )

        if not symptom_present:
            return None

        # Get pathophysiology
        pathophysiology = disease.get(
            "pathophysiology",
            disease.get("description", "")
        )

        # Estimate specificity and sensitivity
        specificity = SymptomContextualizer._estimate_specificity(
            symptom_id, disease, disease_symptoms
        )
        sensitivity = SymptomContextualizer._estimate_sensitivity(
            symptom_id, disease, disease_symptoms
        )

        # Calculate LR+ and LR-
        lr_positive = sensitivity / (1 - specificity) if specificity < 1 else 100.0
        lr_negative = (1 - sensitivity) / specificity if specificity > 0 else 0.01

        # Determine role
        role = SymptomContextualizer._classify_symptom_role(
            specificity, sensitivity, lr_positive, lr_negative
        )

        # Extract evidence
        evidence = SymptomContextualizer._extract_evidence(
            disease, symptom_name
        )

        context = SymptomContext(
            symptom_id=symptom_id,
            symptom_name=symptom_name,
            disease_name=disease_name,
            context_role=role,
            pathophysiology_link=pathophysiology[:500],  # Truncate
            specificity_score=specificity,
            sensitivity_score=sensitivity,
            likelihood_ratio_positive=lr_positive,
            likelihood_ratio_negative=lr_negative,
            confidence_weight=SymptomContextualizer._calculate_weight(
                specificity, sensitivity, role
            ),
            supporting_evidence=evidence,
            related_findings=disease.get("common_findings", []),
        )

        return context

    @staticmethod
    def _estimate_specificity(
        symptom_id: str,
        disease: Dict[str, Any],
        disease_symptoms: List[str],
    ) -> float:
        """
        Estimate how specific symptom is to this disease.

        Based on disease prevalence, symptom frequency in disease, etc.
        """
        # Base specificity: position in symptom list (earlier = more specific)
        symptom_position = next(
            (i for i, s in enumerate(disease_symptoms)
             if symptom_id in str(s) or symptom_id in str(s).lower()),
            len(disease_symptoms)
        )

        position_specificity = 1.0 - (symptom_position / max(len(disease_symptoms), 1))

        # Adjust for disease rarity (rare diseases have more specific symptoms)
        prevalence = disease.get("prevalence_score", 0.5)
        rarity_factor = 1.0 - prevalence if prevalence > 0 else 0.5

        specificity = 0.5 * position_specificity + 0.5 * rarity_factor
        return max(0.0, min(1.0, specificity))

    @staticmethod
    def _estimate_sensitivity(
        symptom_id: str,
        disease: Dict[str, Any],
        disease_symptoms: List[str],
    ) -> float:
        """
        Estimate how often symptom appears in disease.

        Based on its presence in symptom list and disease severity.
        """
        # Presence = sensitivity (symptom is present in disease record)
        presence = 1.0 if any(
            symptom_id in str(s) for s in disease_symptoms
        ) else 0.0

        # Severity factor (severe diseases have more variable symptoms)
        severity = disease.get("severity_score", 0.5)
        severity_factor = 1.0 - (severity * 0.3)  # High severity → slightly lower sensitivity

        sensitivity = presence * severity_factor
        return max(0.0, min(1.0, sensitivity))

    @staticmethod
    def _classify_symptom_role(
        specificity: float,
        sensitivity: float,
        lr_positive: float,
        lr_negative: float,
    ) -> SymptomRole:
        """Classify symptom role based on diagnostic parameters."""
        if lr_positive > 10 and lr_negative < 0.1:
            return SymptomRole.PATHOGNOMONIC
        elif specificity >= SymptomContextualizer.PRIMARY_SYMPTOM_SPECIFICITY:
            return SymptomRole.PRIMARY_SYMPTOM
        elif specificity >= SymptomContextualizer.SECONDARY_SYMPTOM_SPECIFICITY:
            return SymptomRole.SECONDARY_SYMPTOM
        elif specificity < 0.3:
            return SymptomRole.NON_SPECIFIC
        else:
            return SymptomRole.COMPLICATION

    @staticmethod
    def _calculate_weight(
        specificity: float,
        sensitivity: float,
        role: SymptomRole,
    ) -> float:
        """Calculate confidence weight for this context."""
        # Harmonic mean of specificity and sensitivity (F-score)
        if specificity + sensitivity == 0:
            return 0.0

        f_score = 2 * (specificity * sensitivity) / (specificity + sensitivity)

        # Adjust based on role
        role_multipliers = {
            SymptomRole.PATHOGNOMONIC: 1.2,
            SymptomRole.PRIMARY_SYMPTOM: 1.0,
            SymptomRole.SECONDARY_SYMPTOM: 0.7,
            SymptomRole.COMPLICATION: 0.5,
            SymptomRole.NON_SPECIFIC: 0.3,
        }

        weight = f_score * role_multipliers.get(role, 0.5)
        return max(0.0, min(1.0, weight))

    @staticmethod
    def _extract_evidence(
        disease: Dict[str, Any],
        symptom_name: str,
    ) -> List[str]:
        """Extract evidence citations from disease record."""
        evidence = []

        # Check for citations in disease
        if "citations" in disease:
            evidence.extend(disease["citations"][:3])

        # Check for references
        if "references" in disease:
            refs = disease["references"]
            if isinstance(refs, list):
                evidence.extend(str(r) for r in refs[:2])

        return evidence[:3]  # Limit to 3


class AmbiguitySolver:
    """Identifies and resolves symptom ambiguities in multi-disease diagnosis."""

    @classmethod
    def analyze_symptom_set(
        cls,
        symptom_ids: List[str],
        symptom_names: Optional[List[str]] = None,
        disease_candidates: List[Dict[str, Any]] = None,
        disease_database: List[Dict[str, Any]] = None,
    ) -> List[AmbiguityReport]:
        """
        Analyze complete symptom set for ambiguities.

        Args:
            symptom_ids: List of detected symptom IDs
            symptom_names: Optional display names for symptoms
            disease_candidates: Current disease candidates with scores
            disease_database: Complete disease database

        Returns:
            List of AmbiguityReport for each symptom
        """
        if disease_database is None:
            disease_database = []

        if disease_candidates is None:
            disease_candidates = []

        reports = []

        # Get top disease names from candidates
        top_diseases = [
            d.get("name", d.get("name_ja", ""))
            for d in disease_candidates[:5]
        ]

        for symptom_id in symptom_ids:
            symptom_name = symptom_names.get(symptom_id) if symptom_names else symptom_id

            report = cls._analyze_single_symptom(
                symptom_id=symptom_id,
                symptom_name=symptom_name,
                disease_candidates=top_diseases,
                disease_database=disease_database,
            )

            if report:
                reports.append(report)

        return reports

    @classmethod
    def _analyze_single_symptom(
        cls,
        symptom_id: str,
        symptom_name: str,
        disease_candidates: List[str],
        disease_database: List[Dict[str, Any]],
    ) -> Optional[AmbiguityReport]:
        """Analyze single symptom for ambiguity across disease candidates."""

        # Get contexts
        contexts = SymptomContextualizer.contextualize_symptom(
            symptom_id=symptom_id,
            symptom_name=symptom_name,
            disease_names=disease_candidates,
            disease_database=disease_database,
        )

        if not contexts:
            return None

        # Calculate ambiguity score
        ambiguity_score = cls._calculate_ambiguity_score(contexts)
        entropy_score = cls._calculate_entropy(contexts)

        # Determine recommendation
        recommendation = cls._get_recommendation(ambiguity_score)

        # Find predominant disease
        predominant = max(
            contexts.items(),
            key=lambda x: (x[1].specificity_score, x[1].sensitivity_score)
        )[0] if contexts else None

        # Get competing diseases
        competing = [
            disease for disease in contexts.keys()
            if disease != predominant
        ]

        # Generate clarification questions
        clarification_qs = cls._generate_clarification_questions(
            symptom_name, contexts
        ) if recommendation == "ask_clarification" else []

        report = AmbiguityReport(
            symptom_id=symptom_id,
            symptom_name=symptom_name,
            ambiguity_score=ambiguity_score,
            entropy_score=entropy_score,
            contexts=contexts,
            disease_count_with_symptom=len(contexts),
            predominant_disease=predominant,
            competing_diseases=competing,
            recommendation=recommendation,
            clarification_questions=clarification_qs,
            confidence_adjustment_factor=cls._calculate_adjustment_factor(
                ambiguity_score, recommendation
            ),
            explanation_en=cls._generate_explanation(
                symptom_name, ambiguity_score, predominant, competing
            ),
        )

        return report

    @staticmethod
    def _calculate_ambiguity_score(
        contexts: Dict[str, SymptomContext]
    ) -> float:
        """
        Calculate symptom ambiguity using Shannon entropy-inspired metric.

        High ambiguity: symptom has similar meaning across diseases
        Low ambiguity: symptom is specific to one disease
        """
        if not contexts:
            return 0.0

        # Normalize specificities to probabilities
        specificities = [ctx.specificity_score for ctx in contexts.values()]
        total = sum(specificities)

        if total == 0:
            return 1.0

        probs = [s / total for s in specificities]

        # Shannon entropy: H = -sum(p * log2(p))
        entropy = -sum(
            p * math.log2(p) if p > 0 else 0
            for p in probs
        )

        # Normalize by max entropy (uniform distribution)
        max_entropy = math.log2(len(contexts)) if len(contexts) > 1 else 1.0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

        return min(1.0, normalized_entropy)

    @staticmethod
    def _calculate_entropy(
        contexts: Dict[str, SymptomContext]
    ) -> float:
        """Calculate raw Shannon entropy for diagnostic information content."""
        if not contexts:
            return 0.0

        specificities = [ctx.specificity_score for ctx in contexts.values()]
        total = sum(specificities)

        if total == 0:
            return 0.0

        probs = [s / total for s in specificities]
        entropy = -sum(
            p * math.log2(p) if p > 0 else 0
            for p in probs
        )

        return entropy

    @staticmethod
    def _get_recommendation(ambiguity_score: float) -> str:
        """Get recommendation based on ambiguity level."""
        if ambiguity_score >= SymptomContextualizer.HIGH_AMBIGUITY_THRESHOLD:
            return "ask_clarification"
        elif ambiguity_score >= SymptomContextualizer.MODERATE_AMBIGUITY_THRESHOLD:
            return "reduce_confidence"
        else:
            return "keep_all"

    @staticmethod
    def _calculate_adjustment_factor(
        ambiguity_score: float,
        recommendation: str,
    ) -> float:
        """Calculate confidence adjustment factor for ambiguous symptoms."""
        if recommendation == "ask_clarification":
            # Significantly reduce confidence
            return 1.0 - (ambiguity_score * 0.6)
        elif recommendation == "reduce_confidence":
            # Moderately reduce confidence
            return 1.0 - (ambiguity_score * 0.3)
        else:
            # No adjustment
            return 1.0

    @staticmethod
    def _generate_clarification_questions(
        symptom_name: str,
        contexts: Dict[str, SymptomContext],
    ) -> List[str]:
        """Generate clarification questions to resolve ambiguity."""
        questions = []

        # Generic clarification questions
        if len(contexts) >= 2:
            questions.append(f"When did {symptom_name.lower()} start?")
            questions.append(f"Is {symptom_name.lower()} constant or intermittent?")
            questions.append(f"Has {symptom_name.lower()} worsened, improved, or stayed the same?")

        # Disease-specific questions for top contexts
        sorted_contexts = sorted(
            contexts.items(),
            key=lambda x: x[1].specificity_score,
            reverse=True
        )

        for disease, context in sorted_contexts[:2]:
            if context.related_findings:
                finding = context.related_findings[0]
                questions.append(
                    f"Is there {finding.lower()} accompanying the {symptom_name.lower()}?"
                )

        return questions[:3]  # Return top 3 questions

    @staticmethod
    def _generate_explanation(
        symptom_name: str,
        ambiguity_score: float,
        predominant: Optional[str],
        competing: List[str],
    ) -> str:
        """Generate human-readable explanation of ambiguity."""
        if ambiguity_score >= SymptomContextualizer.HIGH_AMBIGUITY_THRESHOLD:
            explanation = (
                f"'{symptom_name}' is ambiguous across multiple diseases. "
            )
            if predominant:
                explanation += f"Most likely associated with {predominant}, "
            if competing:
                explanation += f"but also seen in {', '.join(competing[:2])}. "
            explanation += "Clarification questions will help narrow down the diagnosis."
            return explanation
        elif ambiguity_score >= SymptomContextualizer.MODERATE_AMBIGUITY_THRESHOLD:
            explanation = (
                f"'{symptom_name}' has moderate ambiguity. "
            )
            if predominant:
                explanation += f"Most specific to {predominant}."
            return explanation
        else:
            explanation = f"'{symptom_name}' is clearly indicative of specific disease(s)."
            return explanation

    @classmethod
    def adjust_confidence_for_ambiguity(
        cls,
        disease_confidences: Dict[str, float],
        ambiguity_reports: List[AmbiguityReport],
    ) -> Dict[str, float]:
        """
        Adjust disease confidences based on symptom ambiguities.

        Args:
            disease_confidences: Current confidence scores per disease
            ambiguity_reports: Ambiguity analysis results

        Returns:
            Adjusted confidence scores
        """
        adjusted = disease_confidences.copy()

        for report in ambiguity_reports:
            if report.recommendation != "keep_all":
                # Apply adjustment factor to all diseases with this ambiguous symptom
                for disease in report.contexts.keys():
                    if disease in adjusted:
                        adjusted[disease] *= report.confidence_adjustment_factor

        return adjusted
