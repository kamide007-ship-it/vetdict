"""Common helpers for species-specific disease analysis.

This module provides a generic `analyze_symptoms_generic` function that can be
used by each species-specific module to perform basic differential diagnosis.
It mirrors the dog symptom checker output structure but operates on a custom
disease list and symptom name mapping. A shared advice dictionary is also
defined here for consistent messaging across species.
"""

from __future__ import annotations

from typing import Any, Dict, List, Set

# Default advice messages for various severity levels. These are used when
# species-specific modules do not supply their own advice dictionary.
ADVICE: Dict[str, Dict[str, str]] = {
    "low": {
        "en": "Low severity: Monitor the condition and consult a veterinarian if symptoms worsen.",
        "ja": "軽度: 様子を見て、症状が悪化した場合は獣医師に相談してください。",
    },
    "moderate": {
        "en": "Moderate severity: It is advisable to have the animal examined by a veterinarian soon.",
        "ja": "中等度: 早めに獣医師の診察を受けることをお勧めします。",
    },
    "high": {
        "en": "High severity: Prompt veterinary care is recommended.",
        "ja": "重度: 速やかに獣医師の診察を受けてください。",
    },
    "emergency": {
        "en": "Emergency: Seek immediate veterinary attention.",
        "ja": "緊急: 直ちに獣医師の診察を受けてください。",
    },
}


def _compute_severity(suspected: List[Dict[str, Any]]) -> str:
    """Determine the overall severity level from the list of suspected diseases.

    The rules are similar to the dog implementation: if any emergency
    disease is highly likely, return "emergency". If any high-urgency disease
    is high or moderately likely, return "high". If any disease is highly
    likely, return "moderate". Otherwise return "low".
    """
    # Emergency override
    for disease in suspected:
        if disease.get("_urgency") == "emergency" and disease.get("likelihood") == "high":
            return "emergency"
    # High severity conditions
    for disease in suspected:
        if disease.get("_urgency") in ("high", "emergency") and disease.get("likelihood") in ("high", "moderate"):
            return "high"
    # Moderate severity if any high likelihood
    for disease in suspected:
        if disease.get("likelihood") == "high":
            return "moderate"
    return "low"


def analyze_symptoms_generic(
    symptoms: List[str],
    diseases: List[Dict[str, Any]],
    symptom_names: Dict[str, Dict[str, str]],
    advice: Dict[str, Dict[str, str]] | None = None,
) -> Dict[str, Any]:
    """Generic differential diagnosis engine.

    Parameters
    ----------
    symptoms:
        A list of symptom identifiers provided by the user.
    diseases:
        A list of dictionaries representing diseases. Each dictionary must
        include the keys: ``name``, ``name_ja``, ``symptoms`` (a set of
        identifiers), ``description``, ``description_ja``, ``urgency``, and
        ``recommended_tests`` (list of strings).
    symptom_names:
        A mapping from symptom identifiers to their bilingual names. Only
        identifiers present in this mapping will be included in the output.
    advice:
        Optional advice dictionary overriding the global ADVICE. Must follow
        the same structure as ADVICE if provided.

    Returns
    -------
    dict
        A dictionary with the same structure as the dog symptom checker
        response: ``suspected_diseases``, ``recommended_tests``, ``severity``,
        ``general_advice``, ``general_advice_ja``, ``breed_genetic_tests``,
        ``breed_risk_applied``, and ``symptom_names``.
    """
    symptom_set: Set[str] = set(symptoms)
    suspected: List[Dict[str, Any]] = []

    for disease in diseases:
        disease_symptoms = set(disease.get("symptoms", set()))
        if not disease_symptoms:
            continue
        matching = symptom_set & disease_symptoms
        if not matching:
            continue
        coverage = len(matching) / len(disease_symptoms)
        match_percent = round(coverage * 100)
        # Determine likelihood tiers similar to dog algorithm
        if coverage >= 0.5:
            likelihood = "high"
        elif coverage >= 0.3:
            likelihood = "moderate"
        else:
            likelihood = "low"
        # Map coverage percentage to a simple color class
        if match_percent >= 70:
            color_class = "score-high"
        elif match_percent >= 45:
            color_class = "score-moderate"
        elif match_percent >= 25:
            color_class = "score-low"
        else:
            color_class = "score-minimal"
        suspected.append({
            "name": disease["name"],
            "name_ja": disease["name_ja"],
            "likelihood": likelihood,
            "match_percent": match_percent,
            "color_class": color_class,
            "description": disease.get("description", ""),
            "description_ja": disease.get("description_ja", ""),
            "pathophysiology": disease.get("pathophysiology", ""),
            "pathophysiology_ja": disease.get("pathophysiology_ja", ""),
            "causes": disease.get("causes", ""),
            "causes_ja": disease.get("causes_ja", ""),
            "prevention": disease.get("prevention", ""),
            "prevention_ja": disease.get("prevention_ja", ""),
            "treatment": disease.get("treatment", ""),
            "treatment_ja": disease.get("treatment_ja", ""),
            "prognosis": disease.get("prognosis", ""),
            "prognosis_ja": disease.get("prognosis_ja", ""),
            "matching_symptoms": sorted(matching),
            "match_count": len(matching),
            "total_symptoms": len(disease_symptoms),
            "_urgency": disease.get("urgency", "low"),
            "_match_ratio": coverage,
        })

    # Sort results primarily by match_percent then by number of matching symptoms
    suspected.sort(key=lambda d: (d["match_percent"], d["match_count"]), reverse=True)

    # Compute overall severity
    severity = _compute_severity(suspected)

    # Collect recommended tests, preserving order and uniqueness. We look up
    # the corresponding disease definition by name and extend the list with
    # its recommended tests only once per unique test.
    recommended_tests: List[str] = []
    seen_tests: Set[str] = set()
    for entry in suspected:
        for disease in diseases:
            if disease.get("name") == entry.get("name"):
                for test in disease.get("recommended_tests", []):
                    if test not in seen_tests:
                        recommended_tests.append(test)
                        seen_tests.add(test)
                break

    # Clean internal fields
    for entry in suspected:
        entry.pop("_urgency", None)
        entry.pop("_match_ratio", None)

    # Determine advice dictionary
    advice_dict = advice or ADVICE
    advice_pair = advice_dict.get(severity, advice_dict["low"])

    # Build symptom names lookup
    used_symptoms: Set[str] = set()
    for entry in suspected:
        used_symptoms.update(entry["matching_symptoms"])
    symptom_names_lookup: Dict[str, Dict[str, str]] = {
        sid: symptom_names[sid] for sid in used_symptoms if sid in symptom_names
    }

    return {
        "suspected_diseases": suspected,
        "recommended_tests": recommended_tests,
        "severity": severity,
        "general_advice": advice_pair["en"],
        "general_advice_ja": advice_pair["ja"],
        "breed_genetic_tests": [],
        "breed_risk_applied": False,
        "symptom_names": symptom_names_lookup,
    }
