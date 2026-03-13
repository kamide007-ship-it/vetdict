"""Multi-species symptom mapping and disambiguation data.

Provides species-aware symptom name mapping, severity thresholds, and
cross-species symptom normalization for accurate diagnosis across all species.
"""

from typing import Dict, List, Set

# ==============================================================================
# SYMPTOM ALIASES: Maps symptom concepts to species-specific manifestations
# ==============================================================================
# Each symptom concept can manifest differently across species
# Example: "lameness" → dog:"limping", horse:"stride_shortening", rabbit:"hopping_deficit"

SYMPTOM_SPECIES_ALIASES: Dict[str, Dict[str, List[str]]] = {
    # Respiratory symptoms
    "coughing": {
        "dog": ["cough", "dry_cough", "wet_cough", "nonproductive_cough"],
        "cat": ["cough", "occasional_cough", "chronic_cough"],
        "rabbit": ["cough", "wheezing"],
        "hamster": ["cough", "squeaking"],
        "guinea_pig": ["cough", "chittering"],
        "ferret": ["cough", "honking"],
        "bird": ["cough", "tail_bobbing", "wheezing"],
        "reptile": ["gaping", "wheezing"],
        "horse": ["cough", "exercise_cough"],
        "hedgehog": ["cough"],
    },
    "sneezing": {
        "dog": ["sneeze", "sneezing_episodes"],
        "cat": ["sneeze", "sneezing", "paroxysmal_sneezing"],
        "rabbit": ["sneeze", "sneezing"],
        "hamster": ["sneeze"],
        "guinea_pig": ["sneeze"],
        "ferret": ["sneeze"],
        "bird": ["sneezing"],
        "reptile": [],  # Reptiles don't typically sneeze
        "horse": ["nasal_flare"],
        "hedgehog": ["sneeze"],
    },
    "labored_breathing": {
        "dog": ["dyspnea", "difficult_breathing", "shortness_of_breath", "tachypnea"],
        "cat": ["dyspnea", "difficult_breathing", "labored_respiration"],
        "rabbit": ["labored_respiration", "open_mouth_breathing"],
        "hamster": ["rapid_breathing", "open_mouth_breathing"],
        "guinea_pig": ["rapid_breathing"],
        "ferret": ["rapid_breathing"],
        "bird": ["labored_respiration", "tail_bobbing"],
        "reptile": ["open_mouth_breathing", "gaping"],
        "horse": ["heaving", "flank_movement"],
        "hedgehog": ["rapid_breathing"],
    },
    "wheezing": {
        "dog": ["wheeze", "wheezing_sounds"],
        "cat": ["wheeze", "wheezing", "asthmatic_breathing"],
        "rabbit": ["wheeze"],
        "hamster": ["wheeze"],
        "guinea_pig": ["wheeze"],
        "ferret": ["wheeze"],
        "bird": ["wheezing"],
        "reptile": ["wheezing"],
        "horse": ["wheeze"],
        "hedgehog": ["wheeze"],
    },
    "nasal_discharge": {
        "dog": ["runny_nose", "nasal_drip", "nose_discharge"],
        "cat": ["runny_nose", "nasal_discharge"],
        "rabbit": ["nasal_discharge", "snuffly_nose"],
        "hamster": ["nasal_discharge"],
        "guinea_pig": ["nasal_discharge"],
        "ferret": ["nasal_discharge"],
        "bird": ["nasal_discharge", "nostrils_discharge"],
        "reptile": ["nasal_discharge"],
        "horse": ["nasal_discharge"],
        "hedgehog": ["nasal_discharge"],
    },

    # Gastrointestinal symptoms
    "vomiting": {
        "dog": ["vomit", "regurgitation", "retching"],
        "cat": ["vomit", "regurgitation", "hairball_vomiting"],
        "rabbit": ["vomiting"],  # Rabbits cannot vomit
        "hamster": [],  # Hamsters cannot vomit
        "guinea_pig": [],  # Guinea pigs cannot vomit
        "ferret": ["vomit", "regurgitation"],
        "bird": ["regurgitation"],
        "reptile": [],  # Some cannot vomit
        "horse": [],  # Horses rarely vomit
        "hedgehog": ["vomit"],
    },
    "diarrhea": {
        "dog": ["diarrhea", "loose_stool", "soft_stool"],
        "cat": ["diarrhea", "loose_stool"],
        "rabbit": ["diarrhea", "loose_fecal_pellets"],
        "hamster": ["diarrhea", "wet_tail"],
        "guinea_pig": ["diarrhea"],
        "ferret": ["diarrhea"],
        "bird": ["diarrhea", "wet_droppings"],
        "reptile": ["diarrhea"],
        "horse": ["diarrhea"],
        "hedgehog": ["diarrhea"],
    },
    "constipation": {
        "dog": ["constipation", "difficulty_defecating"],
        "cat": ["constipation", "difficulty_defecating"],
        "rabbit": ["reduced_feces", "constipation"],
        "hamster": ["constipation"],
        "guinea_pig": ["constipation"],
        "ferret": ["constipation"],
        "bird": ["constipation"],
        "reptile": ["constipation"],
        "horse": ["constipation"],
        "hedgehog": ["constipation"],
    },
    "appetite_loss": {
        "dog": ["anorexia", "poor_appetite", "not_eating"],
        "cat": ["anorexia", "poor_appetite"],
        "rabbit": ["anorexia", "not_eating"],
        "hamster": ["reduced_eating"],
        "guinea_pig": ["anorexia"],
        "ferret": ["anorexia"],
        "bird": ["anorexia"],
        "reptile": ["anorexia"],
        "horse": ["anorexia"],
        "hedgehog": ["anorexia"],
    },
    "abdominal_pain": {
        "dog": ["abdominal_pain", "tender_belly", "hunched_posture"],
        "cat": ["abdominal_pain", "tender_belly"],
        "rabbit": ["abdominal_pain", "hunched_posture", "teeth_grinding"],
        "hamster": ["abdominal_distension"],
        "guinea_pig": ["abdominal_pain"],
        "ferret": ["abdominal_pain"],
        "bird": ["abdominal_distension"],
        "reptile": ["abdominal_distension"],
        "horse": ["colic", "abdominal_pain"],
        "hedgehog": ["abdominal_pain"],
    },

    # Lameness/Mobility symptoms
    "lameness": {
        "dog": ["limping", "non_weight_bearing", "favor_limb"],
        "cat": ["limping", "non_weight_bearing"],
        "rabbit": ["hopping_deficit", "non_weight_bearing", "bunny_hopping_abnormal"],
        "hamster": ["dragging_limb"],
        "guinea_pig": ["reluctant_movement"],
        "ferret": ["limping"],
        "bird": ["perching_difficulty", "wing_drag", "limping"],
        "reptile": ["locomotion_abnormality"],
        "horse": ["lameness", "stride_shortening", "head_bob"],
        "hedgehog": ["limping"],
    },
    "joint_swelling": {
        "dog": ["swollen_joint", "joint_enlargement"],
        "cat": ["swollen_joint"],
        "rabbit": ["swollen_joint"],
        "hamster": ["swelling"],
        "guinea_pig": ["joint_swelling"],
        "ferret": ["joint_swelling"],
        "bird": ["wing_swelling"],
        "reptile": ["limb_swelling"],
        "horse": ["joint_swelling"],
        "hedgehog": ["swelling"],
    },

    # Fever/Temperature symptoms
    "fever": {
        "dog": ["elevated_temperature", "high_temperature"],
        "cat": ["fever", "elevated_temperature"],
        "rabbit": ["fever"],
        "hamster": ["fever"],
        "guinea_pig": ["fever"],
        "ferret": ["fever"],
        "bird": ["fever"],
        "reptile": ["basking_behavior"],  # Reptiles cannot regulate temperature
        "horse": ["fever"],
        "hedgehog": ["fever"],
    },

    # Lethargy/Energy symptoms
    "lethargy": {
        "dog": ["fatigue", "low_energy", "sluggish", "sleepiness"],
        "cat": ["lethargy", "low_activity", "sleeping_more"],
        "rabbit": ["lethargy", "inactive"],
        "hamster": ["reduced_activity"],
        "guinea_pig": ["lethargy"],
        "ferret": ["lethargy"],
        "bird": ["lethargy", "fluffed_feathers"],
        "reptile": ["reduced_basking", "inactivity"],
        "horse": ["lethargy", "poor_performance"],
        "hedgehog": ["lethargy"],
    },

    # Weight/Body condition
    "weight_loss": {
        "dog": ["weight_loss", "lean", "thin"],
        "cat": ["weight_loss", "lean"],
        "rabbit": ["weight_loss"],
        "hamster": ["weight_loss"],
        "guinea_pig": ["weight_loss"],
        "ferret": ["weight_loss"],
        "bird": ["weight_loss"],
        "reptile": ["weight_loss"],
        "horse": ["weight_loss"],
        "hedgehog": ["weight_loss"],
    },
    "obesity": {
        "dog": ["overweight", "excess_weight"],
        "cat": ["overweight", "obesity"],
        "rabbit": ["obesity"],
        "hamster": ["obesity"],
        "guinea_pig": ["overweight"],
        "ferret": ["obesity"],
        "bird": ["obesity"],
        "reptile": ["obesity"],
        "horse": ["obesity", "cresty_neck"],
        "hedgehog": ["obesity"],
    },

    # Skin/Coat symptoms
    "itching": {
        "dog": ["pruritus", "scratching", "itchy"],
        "cat": ["pruritus", "scratching"],
        "rabbit": ["barbering", "fur_chewing"],
        "hamster": ["barbering"],
        "guinea_pig": ["fur_chewing"],
        "ferret": ["itching"],
        "bird": ["feather_plucking"],
        "reptile": ["rubbing"],
        "horse": ["itching"],
        "hedgehog": ["quill_loss"],
    },
    "hair_loss": {
        "dog": ["alopecia", "bald_spots", "hair_shedding"],
        "cat": ["alopecia", "baldness"],
        "rabbit": ["hair_loss", "bald_patches"],
        "hamster": ["hair_loss"],
        "guinea_pig": ["hair_loss"],
        "ferret": ["alopecia"],
        "bird": ["feather_loss", "molt_abnormal"],
        "reptile": ["scale_loss"],
        "horse": ["hair_loss"],
        "hedgehog": ["quill_loss"],
    },
    "skin_rash": {
        "dog": ["skin_rash", "red_skin", "dermatitis"],
        "cat": ["skin_rash", "dermatitis"],
        "rabbit": ["skin_lesion"],
        "hamster": ["skin_lesion"],
        "guinea_pig": ["skin_lesion"],
        "ferret": ["skin_lesion"],
        "bird": ["skin_lesion"],
        "reptile": ["scale_abnormality"],
        "horse": ["dermatitis"],
        "hedgehog": ["skin_lesion"],
    },

    # Eye symptoms
    "eye_discharge": {
        "dog": ["eye_discharge", "ocular_discharge"],
        "cat": ["eye_discharge", "tearing"],
        "rabbit": ["eye_discharge"],
        "hamster": ["eye_discharge"],
        "guinea_pig": ["eye_discharge"],
        "ferret": ["eye_discharge"],
        "bird": ["ocular_discharge"],
        "reptile": ["ocular_discharge"],
        "horse": ["eye_discharge"],
        "hedgehog": ["eye_discharge"],
    },
    "squinting": {
        "dog": ["squinting", "eye_squinting"],
        "cat": ["squinting"],
        "rabbit": ["squinting"],
        "hamster": ["squinting"],
        "guinea_pig": ["squinting"],
        "ferret": ["squinting"],
        "bird": ["eye_closure"],
        "reptile": ["eye_closure"],
        "horse": ["squinting"],
        "hedgehog": ["squinting"],
    },

    # Urinary symptoms
    "urinary_frequency": {
        "dog": ["frequent_urination", "polyuria"],
        "cat": ["frequent_urination", "polyuria"],
        "rabbit": ["frequent_urination"],
        "hamster": ["frequent_urination"],
        "guinea_pig": ["frequent_urination"],
        "ferret": ["frequent_urination"],
        "bird": ["frequent_urination"],
        "reptile": ["frequent_urination"],
        "horse": ["frequent_urination"],
        "hedgehog": ["frequent_urination"],
    },
    "urinary_straining": {
        "dog": ["straining_to_urinate", "dysuria"],
        "cat": ["straining_to_urinate", "dysuria"],
        "rabbit": ["straining_to_urinate"],
        "hamster": ["straining_to_urinate"],
        "guinea_pig": ["straining_to_urinate"],
        "ferret": ["straining_to_urinate"],
        "bird": ["straining_to_urinate"],
        "reptile": ["straining_to_urinate"],
        "horse": ["straining_to_urinate"],
        "hedgehog": ["straining_to_urinate"],
    },

    # Behavioral symptoms
    "aggression": {
        "dog": ["aggressive_behavior", "biting", "growling"],
        "cat": ["aggressive_behavior", "biting", "hissing"],
        "rabbit": ["biting", "aggressive"],
        "hamster": ["biting", "aggressive"],
        "guinea_pig": ["aggressive"],
        "ferret": ["aggressive", "biting"],
        "bird": ["aggressive", "biting"],
        "reptile": ["aggressive"],
        "horse": ["aggressive", "biting"],
        "hedgehog": ["aggressive"],
    },
    "disorientation": {
        "dog": ["disorientation", "confusion", "staring"],
        "cat": ["disorientation"],
        "rabbit": ["disorientation"],
        "hamster": ["disorientation"],
        "guinea_pig": ["disorientation"],
        "ferret": ["disorientation"],
        "bird": ["disorientation"],
        "reptile": ["disorientation"],
        "horse": ["disorientation"],
        "hedgehog": ["disorientation"],
    },
}

# ==============================================================================
# SPECIES-SPECIFIC SYMPTOM SEVERITY THRESHOLDS
# ==============================================================================
# Different species present symptoms at different severity levels
# These thresholds help normalize symptom severity across species

SYMPTOM_SEVERITY_THRESHOLDS: Dict[str, Dict[str, Dict[str, float]]] = {
    "lameness": {
        "dog": {
            "mild": 0.0,
            "moderate": 0.5,
            "severe": 0.8,
        },
        "cat": {
            "mild": 0.0,
            "moderate": 0.6,
            "severe": 0.9,
        },
        "rabbit": {
            "mild": 0.2,
            "moderate": 0.6,
            "severe": 0.9,
        },
        "horse": {
            "mild": 0.1,
            "moderate": 0.4,
            "severe": 0.7,
        },
        "bird": {
            "mild": 0.3,
            "moderate": 0.7,
            "severe": 1.0,
        },
        "default": {
            "mild": 0.0,
            "moderate": 0.5,
            "severe": 0.8,
        },
    },
    "weight_loss": {
        "dog": {
            "mild": 0.05,
            "moderate": 0.10,
            "severe": 0.20,
        },
        "cat": {
            "mild": 0.05,
            "moderate": 0.10,
            "severe": 0.20,
        },
        "rabbit": {
            "mild": 0.05,
            "moderate": 0.10,
            "severe": 0.20,
        },
        "hamster": {
            "mild": 0.02,
            "moderate": 0.05,
            "severe": 0.10,
        },
        "default": {
            "mild": 0.05,
            "moderate": 0.10,
            "severe": 0.20,
        },
    },
}

# ==============================================================================
# SYMPTOM EXCLUSION RULES
# ==============================================================================
# Some symptoms should be excluded for certain species entirely

SYMPTOM_EXCLUSIONS: Dict[str, List[str]] = {
    "rabbit": ["vomiting"],  # Rabbits cannot vomit
    "hamster": ["vomiting"],  # Hamsters cannot vomit
    "guinea_pig": ["vomiting"],  # Guinea pigs cannot vomit
    "horse": ["vomiting"],  # Horses rarely vomit
    "reptile": ["vomiting"],  # Many reptiles cannot vomit
    "bird": [],
    "cat": [],
    "dog": [],
    "ferret": [],
    "hedgehog": [],
}

# ==============================================================================
# SPECIES-SPECIFIC SYMPTOM PROMINENCE
# ==============================================================================
# How prominently a symptom manifests in a species
# Used to adjust confidence scores

SYMPTOM_PROMINENCE: Dict[str, Dict[str, float]] = {
    "coughing": {
        "dog": 1.0,
        "cat": 0.9,
        "rabbit": 0.7,
        "bird": 1.1,
        "horse": 1.1,
        "default": 0.8,
    },
    "sneezing": {
        "cat": 1.2,
        "rabbit": 1.0,
        "dog": 0.8,
        "bird": 0.7,
        "default": 0.8,
    },
    "lameness": {
        "dog": 1.0,
        "horse": 1.2,
        "rabbit": 0.9,
        "cat": 0.8,
        "default": 0.8,
    },
    "weight_loss": {
        "cat": 1.1,
        "dog": 1.0,
        "rabbit": 0.9,
        "default": 0.8,
    },
    "appetite_loss": {
        "cat": 1.2,
        "rabbit": 1.0,
        "dog": 0.9,
        "default": 0.8,
    },
    "lethargy": {
        "cat": 1.0,
        "dog": 0.9,
        "rabbit": 0.8,
        "bird": 0.7,
        "default": 0.8,
    },
}

# ==============================================================================
# SPECIES COMPATIBILITY MATRIX
# ==============================================================================
# Which symptoms are relevant for each species (1.0 = fully relevant, 0.0 = not relevant)

SPECIES_SYMPTOM_COMPATIBILITY: Dict[str, Dict[str, float]] = {
    "vomiting": {
        "dog": 1.0,
        "cat": 1.0,
        "ferret": 1.0,
        "rabbit": 0.0,  # Cannot vomit
        "hamster": 0.0,  # Cannot vomit
        "guinea_pig": 0.0,  # Cannot vomit
        "horse": 0.1,  # Very rare
        "bird": 0.5,
        "reptile": 0.5,
        "hedgehog": 0.8,
    },
    "lameness": {
        "dog": 1.0,
        "cat": 1.0,
        "rabbit": 1.0,
        "hamster": 0.9,
        "guinea_pig": 0.9,
        "ferret": 0.9,
        "bird": 0.8,
        "reptile": 0.8,
        "horse": 1.0,
        "hedgehog": 0.9,
    },
    "sneezing": {
        "dog": 0.8,
        "cat": 1.0,
        "rabbit": 1.0,
        "hamster": 0.8,
        "guinea_pig": 0.8,
        "ferret": 0.8,
        "bird": 0.7,
        "reptile": 0.0,  # Reptiles don't sneeze
        "horse": 0.7,
        "hedgehog": 0.8,
    },
    "coughing": {
        "dog": 1.0,
        "cat": 0.9,
        "rabbit": 0.7,
        "hamster": 0.6,
        "guinea_pig": 0.6,
        "ferret": 0.8,
        "bird": 1.0,
        "reptile": 0.6,
        "horse": 1.0,
        "hedgehog": 0.7,
    },
    "diarrhea": {
        "dog": 1.0,
        "cat": 1.0,
        "rabbit": 1.0,
        "hamster": 1.0,
        "guinea_pig": 1.0,
        "ferret": 1.0,
        "bird": 1.0,
        "reptile": 1.0,
        "horse": 1.0,
        "hedgehog": 1.0,
    },
}

# ==============================================================================
# CROSS-SPECIES SYMPTOM MAPPING FUNCTION
# ==============================================================================

def normalize_symptom_for_species(symptom_name: str, species: str) -> str:
    """
    Normalize a symptom name to the most appropriate form for a given species.

    Args:
        symptom_name: The symptom name or ID to normalize
        species: Target species

    Returns:
        Normalized symptom name or alias appropriate for the species
    """
    species_lower = species.lower()

    # Check if this is a primary symptom with aliases
    if symptom_name in SYMPTOM_SPECIES_ALIASES:
        aliases = SYMPTOM_SPECIES_ALIASES[symptom_name].get(species_lower, [])
        if aliases:
            return aliases[0]  # Return primary alias for species
        # Fallback to default aliases if species not listed
        if "default" in SYMPTOM_SPECIES_ALIASES[symptom_name]:
            return SYMPTOM_SPECIES_ALIASES[symptom_name]["default"][0]

    # Return original symptom name if no mapping found
    return symptom_name


def get_symptom_severity_threshold(
    symptom: str,
    species: str,
    severity_level: str = "moderate"
) -> float:
    """
    Get the severity threshold for a symptom in a specific species.

    Args:
        symptom: Symptom name
        species: Target species
        severity_level: "mild", "moderate", or "severe"

    Returns:
        Severity threshold (0-1)
    """
    species_lower = species.lower()
    severity_lower = severity_level.lower()

    if symptom not in SYMPTOM_SEVERITY_THRESHOLDS:
        return 0.5  # Default moderate threshold

    thresholds = SYMPTOM_SEVERITY_THRESHOLDS[symptom]
    species_thresholds = thresholds.get(species_lower)

    if not species_thresholds:
        species_thresholds = thresholds.get("default", {})

    return species_thresholds.get(severity_lower, 0.5)


def is_symptom_valid_for_species(symptom: str, species: str) -> bool:
    """
    Check if a symptom is valid for a given species.

    Args:
        symptom: Symptom name
        species: Target species

    Returns:
        True if symptom is valid for species, False otherwise
    """
    species_lower = species.lower()

    # Check exclusion list
    if symptom in SYMPTOM_EXCLUSIONS.get(species_lower, []):
        return False

    # Check compatibility matrix if available
    if symptom in SPECIES_SYMPTOM_COMPATIBILITY:
        compatibility = SPECIES_SYMPTOM_COMPATIBILITY[symptom].get(
            species_lower, 0.5
        )
        return compatibility > 0.0

    return True


def get_symptom_prominence(symptom: str, species: str) -> float:
    """
    Get how prominently a symptom manifests in a species (0-1+ multiplier).

    Args:
        symptom: Symptom name
        species: Target species

    Returns:
        Prominence multiplier (1.0 = baseline, >1.0 = more prominent, <1.0 = less prominent)
    """
    species_lower = species.lower()

    if symptom not in SYMPTOM_PROMINENCE:
        return 1.0  # Default baseline

    prominence_map = SYMPTOM_PROMINENCE[symptom]
    return prominence_map.get(species_lower, prominence_map.get("default", 1.0))


def get_compatible_symptoms(species: str) -> Set[str]:
    """
    Get all symptoms that are compatible with a given species.

    Args:
        species: Target species

    Returns:
        Set of compatible symptom names
    """
    species_lower = species.lower()
    exclusions = set(SYMPTOM_EXCLUSIONS.get(species_lower, []))

    compatible = set()
    for symptom in SYMPTOM_SPECIES_ALIASES.keys():
        if symptom not in exclusions:
            if symptom not in SPECIES_SYMPTOM_COMPATIBILITY:
                compatible.add(symptom)
            else:
                compatibility = SPECIES_SYMPTOM_COMPATIBILITY[symptom].get(
                    species_lower, 0.5
                )
                if compatibility > 0.0:
                    compatible.add(symptom)

    return compatible
