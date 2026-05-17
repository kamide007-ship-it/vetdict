"""Disease matching algorithm for multi-species differential diagnosis.

IDF-weighted harmonic mean scoring with specificity bonuses,
negative evidence penalties, urgency boosts, and prevalence correction.
"""

import math

from api.chat.species_data import get_species_data
from api.species import prevalence_data as _prev_mod

# Synonym expansion table shared across species — bridges concept-equivalent IDs
# (e.g. fin_rot ↔ frayed_fins, hair_loss ↔ alopecia, polydipsia ↔ excessive_thirst).
# Hoisted to module scope so the dict literal isn't rebuilt on every call.
_SYN: dict[str, list[str]] = {
    "frayed_fins": ["fin_rot"],
    "fin_rot": ["frayed_fins"],
    "redness_skin": ["fin_hemorrhage", "hemorrhage", "skin_redness"],
    "fin_hemorrhage": ["redness_skin"],
    "skin_redness": ["redness_skin", "hemorrhage", "red_legs", "red_ventrum"],
    "loss_of_appetite": ["appetite_loss", "anorexia"],
    "appetite_loss": ["loss_of_appetite", "anorexia"],
    "anorexia": ["loss_of_appetite", "appetite_loss"],
    "constipation": ["reduced_fecal_output", "small_fecal_pellets", "decreased_fecal_output"],
    "small_fecal_pellets": ["reduced_fecal_output", "constipation"],
    "reduced_fecal_output": ["small_fecal_pellets", "constipation", "decreased_fecal_output"],
    "decreased_fecal_output": ["reduced_fecal_output", "constipation", "small_fecal_pellets"],
    "bloating": ["abdominal_distension", "abdominal_pain"],
    "abdominal_distension": ["bloating", "abdominal_pain"],
    "abdominal_pain": ["bloating", "abdominal_distension", "hunched_posture"],
    "hunched_posture": ["abdominal_pain"],
    "excessive_drooling": ["drooling"],
    "drooling": ["excessive_drooling"],
    "frequent_urination": ["excessive_urination", "polyuria", "increased_urination"],
    "excessive_urination": ["frequent_urination", "polyuria", "increased_urination"],
    "increased_urination": ["excessive_urination", "frequent_urination", "polyuria"],
    "excessive_thirst": ["polydipsia", "increased_thirst"],
    "increased_thirst": ["excessive_thirst", "polydipsia"],
    "polydipsia": ["excessive_thirst", "increased_thirst"],
    "polyuria": ["excessive_urination", "frequent_urination", "increased_urination"],
    "hair_loss": ["alopecia", "scaling", "quill_loss", "severe_quill_loss", "feather_loss", "circular_hair_loss"],
    "circular_hair_loss": ["hair_loss", "alopecia"],
    "alopecia": ["hair_loss", "circular_hair_loss"],
    "feather_loss": ["hair_loss", "feather_plucking"],
    "feather_plucking": ["feather_loss", "self_mutilation"],
    "skin_lesions": [
        "scaling",
        "dermatitis",
        "skin_rash",
        "crusting",
        "thick_crusting",
        "flaky_skin",
        "dry_skin",
        "shell_discoloration",
        "shell_pitting",
        "skin_crusting",
    ],
    "scaly_skin": ["scaling", "dandruff", "skin_crusting", "dry_skin"],
    "skin_crusting": ["scaling", "scaly_skin", "dandruff"],
    "scaling": ["skin_lesions", "dandruff", "scaly_skin"],
    "dandruff": ["scaling", "scaly_skin", "skin_crusting"],
    "itching": ["pruritus", "scratching", "mild_itching", "ear_scratching"],
    "pruritus": ["itching", "scratching", "mild_itching", "ear_scratching"],
    "cloudy_eyes": ["cloudy_eye", "cloudiness_in_eyes", "corneal_cloudiness", "corneal_opacity"],
    "cloudy_eye": ["cloudy_eyes", "corneal_cloudiness", "corneal_opacity"],
    "corneal_opacity": ["corneal_cloudiness", "cloudy_eyes", "cloudy_eye"],
    "corneal_cloudiness": ["corneal_opacity", "cloudy_eyes", "cloudy_eye"],
    "tearing": ["excessive_tearing", "epiphora"],
    "excessive_tearing": ["tearing", "epiphora"],
    "vision_loss": ["blindness", "cloudy_eye", "cataracts"],
    "open_mouth_breathing": ["respiratory_distress", "labored_breathing"],
    "labored_breathing": ["respiratory_distress", "open_mouth_breathing", "dyspnea"],
    "respiratory_distress": ["labored_breathing", "open_mouth_breathing", "dyspnea"],
    "wheezing": ["coughing", "labored_breathing", "respiratory_distress"],
    "soft_bones": [
        "bone_weakness",
        "jaw_softening",
        "shell_soft_spots",
        "fractures",
        "bone_deformity",
        "soft_shell",
        "shell_softening",
    ],
    "bone_deformity": ["soft_bones", "limb_deformity", "shell_deformity", "fractures", "swollen_limbs"],
    "shell_softening": ["soft_shell", "soft_bones", "shell_deformity"],
    "soft_shell": ["shell_softening", "soft_bones", "shell_deformity"],
    "shell_deformity": ["bone_deformity", "soft_shell", "shell_softening"],
    "head_tilt": ["vestibular_signs", "torticollis"],
    "fluffed_feathers": ["feather_fluffing"],
    "paralysis_or_paresis": [
        "paralysis",
        "paresis",
        "hind_limb_weakness",
        "posterior_paresis",
        "progressive_paralysis",
        "hindlimb_weakness",
        "hind_limb_paralysis",
    ],
    "paralysis": ["hind_limb_paralysis", "paralysis_or_paresis", "hind_limb_weakness"],
    "sudden_paralysis": ["hind_limb_paralysis", "paralysis", "paralysis_or_paresis"],
    "hind_limb_paralysis": ["paralysis", "sudden_paralysis", "paralysis_or_paresis", "hind_limb_weakness"],
    "eye_swelling": [
        "periorbital_swelling",
        "swollen_eyes",
        "blepharitis",
        "pop_eye",
        "exophthalmia",
        "exophthalmos",
        "bulging_eye",
        "eye_bulging",
        "enlarged_eye",
        "eye_protrusion",
    ],
    "eye_protrusion": ["eye_swelling", "eye_bulging", "pop_eye", "exophthalmos", "bulging_eye", "proptosis"],
    "eye_bulging": ["eye_protrusion", "eye_swelling", "pop_eye", "exophthalmos", "enlarged_eye", "proptosis"],
    "enlarged_eye": ["eye_bulging", "eye_swelling", "exophthalmos", "pop_eye", "eye_protrusion"],
    "exophthalmos": ["eye_protrusion", "eye_bulging", "eye_swelling", "pop_eye", "enlarged_eye", "proptosis"],
    "jaundice": ["icterus", "yellow_skin"],
    "vomiting": ["regurgitation", "crop_stasis"],
    "regurgitation": ["vomiting"],
    "head_shaking": ["head_bobbing"],
    "gill_swelling": ["gill_redness"],
    "gill_paleness": ["gill_necrosis"],
    "nystagmus": ["head_tilt", "rolling"],
    "ataxia": ["tremors", "incoordination", "wobbling", "stumbling", "mild_ataxia"],
    "tremors": ["ataxia", "shaking", "muscle_twitching"],
    "wobbling": ["ataxia", "incoordination", "stumbling"],
    "ear_discharge": ["ear_infection", "otitis", "ear_mites"],
    "blood_in_urine": ["hematuria", "uterine_bleeding"],
    "blood_in_stool": ["melena", "bleeding_gums", "hematochezia"],
    "weight_loss": ["rough_coat", "poor_growth", "emaciation"],
    "lethargy": ["reluctance_to_move", "weakness", "pain_on_touch"],
    "hind_limb_weakness": [
        "hindlimb_weakness",
        "posterior_paresis",
        "hind_limb_paralysis",
        "progressive_paralysis",
        "hind_leg_weakness",
    ],
    "hindlimb_weakness": ["hind_limb_weakness", "posterior_paresis", "hind_limb_paralysis", "hind_leg_weakness"],
    "hind_leg_weakness": ["hind_limb_weakness", "hindlimb_weakness", "posterior_paresis", "hind_limb_paralysis"],
    "swollen_eyes": ["eye_swelling", "periorbital_swelling"],
    "sneezing": ["nasal_discharge"],
    "wet_tail": ["diarrhea"],
    "diarrhea": ["wet_tail"],
    "poor_coat": ["hair_loss", "dry_skin"],
    "dry_skin": ["poor_coat", "flaky_skin", "scaling"],
    "flaky_skin": ["dry_skin", "scaling", "crusting"],
    "thinning_skin": ["hair_loss"],
    "darkened_coloration": ["dark_coloration", "discoloration"],
    "dark_coloration": ["darkened_coloration", "discoloration"],
    "cold_limbs": ["cold_extremities"],
    "cold_extremities": ["cold_limbs"],
    "self_mutilation": ["self_chewing", "feather_plucking"],
    "self_chewing": ["self_mutilation"],
    "behavioral_change": ["behavioral_changes", "aggression"],
    "behavioral_changes": ["behavioral_change"],
    "effusion": ["pleural_effusion", "abdominal_distension", "ascites"],
    "pleural_effusion": ["effusion", "abdominal_distension"],
    "ascites": ["effusion", "abdominal_distension", "bloating", "dropsy"],
    "dropsy": ["bloating", "edema", "ascites", "abdominal_distension"],
    "overgrown_teeth": [
        "dental_overgrowth",
        "incisor_overgrowth",
        "molar_overgrowth",
        "malocclusion",
        "visible_tooth_overgrowth",
    ],
    "dental_overgrowth": ["overgrown_teeth", "malocclusion", "visible_tooth_overgrowth"],
    "visible_tooth_overgrowth": ["overgrown_teeth", "dental_overgrowth", "malocclusion"],
    "dysecdysis": ["retained_shed", "retained_skin", "shedding_problems"],
    "retained_shed": ["dysecdysis", "retained_skin"],
    "retained_skin": ["dysecdysis", "retained_shed"],
    "crop_swelling": ["crop_stasis", "ingluvitis"],
    "crop_stasis": ["crop_swelling", "ingluvitis"],
    "red_legs": ["red_ventrum", "skin_redness", "hemorrhage"],
    "red_ventrum": ["red_legs", "skin_redness"],
    "edema": ["swelling", "bloating", "ascites"],
    "swelling": ["edema", "facial_swelling", "eye_swelling"],
    "rough_coat": ["poor_coat", "dry_skin"],
    "scaly_legs": ["leg_scales", "scaly_face"],
    "leg_scales": ["scaly_legs", "scaly_face"],
    "scaly_face": ["scaly_legs", "leg_scales", "crusty_beak"],
    "hole_in_head": ["head_erosion", "head_pitting"],
    # --- Additional clinical synonyms (extended coverage; new keys only) ---
    # Cardiac signs
    "coughing": ["cough", "honking_cough", "kennel_cough", "reverse_sneezing"],
    "cough": ["coughing", "honking_cough"],
    "exercise_intolerance": ["weakness", "lethargy", "reluctance_to_move", "reluctance_move"],
    "syncope": ["collapse", "fainting", "loss_of_consciousness"],
    "collapse": ["syncope", "fainting", "loss_of_consciousness"],
    "fainting": ["syncope", "collapse"],
    # Neurological
    "seizures": ["convulsions", "fits", "epileptic_seizure", "tonic_clonic"],
    "convulsions": ["seizures", "fits"],
    "circling": ["walking_in_circles", "head_pressing"],
    "head_pressing": ["circling", "head_tilt"],
    "disorientation": ["confusion", "circling", "head_pressing", "behavior_change"],
    "behavior_change": ["aggression_change", "anxiety", "disorientation"],
    # GI extended (NEW keys only — keys already defined above are skipped)
    "appetite_increase": ["polyphagia", "increased_appetite"],
    "vomiting_after_drinking": ["vomiting", "regurgitation", "projectile_vomiting"],
    "hematochezia": ["bloody_stool", "blood_in_stool", "melena"],
    "melena": ["dark_stool", "blood_in_stool", "bloody_stool"],
    # Urinary extended
    "straining_urinate": ["dysuria", "stranguria", "blocked_urethra", "urethral_obstruction"],
    "blood_urine": ["hematuria", "bloody_urine", "pink_urine", "red_urine"],
    "incontinence": ["urinary_incontinence", "fecal_incontinence", "urine_leakage"],
    "urinary_incontinence": ["incontinence", "urine_leakage", "bladder_leakage"],
    # Respiratory extended
    "nasal_discharge": ["runny_nose", "rhinitis", "sniffles", "snuffles"],
    "rapid_breathing": ["tachypnea", "labored_breathing", "panting"],
    "excessive_panting": ["tachypnea", "rapid_breathing", "panting"],
    "dyspnea": ["labored_breathing", "respiratory_distress", "open_mouth_breathing"],
    # Pain/orthopedic
    "limping_fl": ["lameness_fl", "limp", "lameness", "stiffness", "limping"],
    "limping_fr": ["lameness_fr", "limp", "lameness", "stiffness", "limping"],
    "limping_rl": ["lameness_rl", "limp", "lameness", "stiffness", "limping"],
    "limping_rr": ["lameness_rr", "limp", "lameness", "stiffness", "limping"],
    "lameness": ["limp", "limping", "limping_fl", "limping_fr", "limping_rl", "limping_rr"],
    "stiffness": ["stiff_gait", "lameness", "reluctance_to_move", "reluctance_move"],
    "pain_on_touch": ["pain_on_palpation", "tenderness", "discomfort"],
    # Skin/coat extended (new keys only)
    "skin_itching": ["itching", "pruritus", "scratching"],
    "lumps": ["mass", "tumor", "nodule", "growth", "swelling"],
    # Eye
    "eye_redness": ["red_eye", "ocular_redness", "conjunctivitis"],
    "eye_discharge": ["ocular_discharge", "tearing", "epiphora", "pus_in_eye"],
    "squinting": ["blepharospasm", "eye_closed", "eye_squint", "photophobia"],
    # Ear
    "ear_scratching": ["ear_pruritus", "scratching_ears", "head_shaking"],
    # General/systemic
    "fever": ["pyrexia", "hyperthermia", "high_temperature"],
    "low_temperature": ["hypothermia", "cold_extremities", "subnormal_temperature"],
    "weak_pulse": ["thready_pulse", "absent_pulse", "weak_femoral_pulse"],
    "pale_gums": ["pallor", "mucous_membrane_pallor", "white_gums", "anemic"],
    # Reproductive
    "mammary_swelling": ["mammary_enlargement", "lactation", "mammary_mass"],
    "genital_discharge": ["vulvar_discharge", "preputial_discharge", "vaginal_discharge"],
    # Behavioral
    "anxiety": ["nervousness", "hiding", "trembling", "panting"],
    "aggression_change": ["aggression", "irritability", "behavior_change"],
    "hiding": ["seeking_solitude", "withdrawal", "anxiety"],
}

# Prevalence tier multipliers (region-aware data is loaded per call by species).
_PREVALENCE_MULTIPLIER: dict[str, float] = {
    "very_common": 1.35,
    "common": 1.125,
    "uncommon": 0.875,
    "rare": 0.70,
}

# Per-species IDF data: {species: (symptom_disease_count, total_diseases)}.
# Cached after first call since the disease data is loaded at module import
# time and doesn't change at runtime.
_SPECIES_IDF_CACHE: dict[str, tuple[dict[str, int], int]] = {}

# Tracks which species have had metadata enrichment applied (idempotent).
_METADATA_ENRICHED: set[str] = set()


def _ensure_metadata_enriched(species: str, diseases: list) -> None:
    """Apply lazy metadata auto-enrichment (age_predisposition / onset_pattern)
    once per species. Mutates disease dicts in-place.
    """
    if species in _METADATA_ENRICHED:
        return
    try:
        from api.chat.metadata_enricher import enrich_diseases_inplace

        enrich_diseases_inplace(diseases)
    except (ImportError, Exception):  # noqa: BLE001 — best-effort enrichment
        pass
    _METADATA_ENRICHED.add(species)


def _get_species_idf(species: str, diseases: list) -> tuple[dict[str, int], int]:
    """Return (symptom_disease_count, total_diseases) for a species, cached.

    The disease list is fixed at module load — counting how often each symptom
    appears across all diseases is a one-shot computation per species.
    """
    cached = _SPECIES_IDF_CACHE.get(species)
    if cached is not None:
        return cached
    # Apply metadata enrichment once before any matching uses the data
    _ensure_metadata_enriched(species, diseases)
    counts: dict[str, int] = {}
    for disease in diseases:
        for s in disease.get("symptoms", set()):
            counts[s] = counts.get(s, 0) + 1
    total = max(len(diseases), 1)
    _SPECIES_IDF_CACHE[species] = (counts, total)
    return counts, total


def _match_species_symptoms_to_diseases(
    symptom_ids: list[str],
    species: str,
    *,
    pain_score: int | None = None,
    lab_values: dict | None = None,
    breed: str | None = None,
    age_category: str | None = None,
    onset_pattern: str | None = None,
    lang: str = "",
) -> list[dict]:
    """Match symptom IDs to species-specific diseases using advanced weighted scoring.

    Uses the same harmonic-mean + specificity + negative-evidence algorithm as
    the dog matcher (match_symptoms_to_diseases) to achieve consistent,
    high-accuracy differential diagnosis across all species.

    Optional clinical context (pain_score, lab_values, breed, age_category,
    onset_pattern) refines scoring when available:
    - age_category: 'puppy'/'young'/'adult'/'senior' (or similar species-specific terms)
      boosts diseases listing this age in age_predisposition
    - onset_pattern: 'acute'/'subacute'/'chronic' boosts diseases listing this pattern
    - breed: boosts diseases listing this breed in common_breeds (case-insensitive substring match)
    """

    sp_data = get_species_data(species)
    if not sp_data or not symptom_ids:
        return []

    # Expand user symptoms with synonyms for better disease matching.
    expanded_set = set(symptom_ids)
    for sid in symptom_ids:
        for alt in _SYN.get(sid, []):
            expanded_set.add(alt)
    symptom_set = expanded_set
    diseases = sp_data["diseases"]

    # --- Load prevalence data for this species (region-aware) ---
    _region = "jp" if lang == "ja" else ("intl" if lang else "")
    _prevalence = _prev_mod.get_prevalence_for_species(species, region=_region)

    # --- Compute lab abnormality boosts for this species ---
    # Returns {disease_name: boost_multiplier} where multiplier > 1.0 for matching diseases.
    _lab_boosts: dict[str, float] = {}
    if lab_values:
        try:
            from api.species.helpers import compute_lab_boosts

            _lab_boosts = compute_lab_boosts(lab_values, species=species)
        except (ImportError, Exception):  # noqa: BLE001 — best-effort scoring layer
            _lab_boosts = {}

    # --- Build per-symptom specificity for this species (cached) ---
    symptom_disease_count, total_diseases = _get_species_idf(species, diseases)

    _weight_cache: dict[str, float] = {}

    def _compute_weight(sym_id: str) -> float:
        """Higher weight for symptoms that appear in fewer diseases (more specific)."""
        cached = _weight_cache.get(sym_id)
        if cached is not None:
            return cached
        count = symptom_disease_count.get(sym_id, 1)
        # IDF-inspired: log(N / count) + 1, clamped to [1.0, 3.0]
        idf = math.log(total_diseases / max(count, 1)) + 1.0
        weight = max(1.0, min(idf, 3.0))
        _weight_cache[sym_id] = weight
        return weight

    user_weights = {s: _compute_weight(s) for s in symptom_set}
    total_user_weight = sum(user_weights.values())

    matches = []
    for disease in diseases:
        disease_symptoms = set(disease.get("symptoms", set()))
        if not disease_symptoms:
            continue

        matched = symptom_set & disease_symptoms
        if not matched:
            continue

        # --- Weighted recall (how well user symptoms match this disease) ---
        matched_weight = sum(user_weights.get(s, 1.0) for s in matched)
        weighted_recall = matched_weight / total_user_weight if total_user_weight > 0 else 0

        # --- Coverage (how much of the disease's symptom profile is covered) ---
        total_disease_weight = sum(_compute_weight(s) for s in disease_symptoms)
        covered_weight = sum(_compute_weight(s) for s in matched)
        coverage = covered_weight / total_disease_weight if total_disease_weight > 0 else 0

        # --- Harmonic mean base score ---
        if weighted_recall + coverage > 0:
            base_score = 2.0 * weighted_recall * coverage / (weighted_recall + coverage)
        else:
            base_score = 0.0

        # --- Specificity bonus: reward matching highly specific symptoms ---
        specificity_bonus = 0.0
        for s in matched:
            w = _compute_weight(s)
            if w >= 2.5:
                specificity_bonus += 0.06
            elif w >= 1.8:
                specificity_bonus += 0.03
        base_score = min(base_score + specificity_bonus, 1.0)

        # --- Negative evidence penalty ---
        # Scale penalty by how many symptoms the user actually provided vs disease total.
        # When user provides few symptoms relative to disease total, reduce penalty.
        missing = disease_symptoms - symptom_set
        negative_penalty = 1.0
        if len(symptom_set) >= 3 and len(disease_symptoms) >= 3:
            obs_ratio = min(1.0, len(symptom_ids) / len(disease_symptoms))
            for s in missing:
                w = _compute_weight(s)
                if w >= 2.5:
                    negative_penalty -= 0.06 * obs_ratio
                elif w >= 2.0:
                    negative_penalty -= 0.03 * obs_ratio
            negative_penalty = max(negative_penalty, 0.55)

        # --- Coverage completeness bonus ---
        # Reward diseases where more absolute symptoms matched (not just ratio).
        # This prevents diseases with few symptoms from dominating.
        coverage_bonus = 1.0
        absolute_match_count = len(matched)
        if absolute_match_count >= 4:
            coverage_bonus = 1.10
        elif absolute_match_count >= 3:
            coverage_bonus = 1.05

        # --- Urgency boost: slightly favor high-urgency diseases for safety ---
        urgency = disease.get("urgency", "low")
        urgency_factor = {"emergency": 1.05, "high": 1.02}.get(urgency, 1.0)

        # --- Prevalence prior ---
        disease_name = disease.get("name", "")
        prevalence_tier = _prevalence.get(disease_name, "")
        prevalence_mult = _PREVALENCE_MULTIPLIER.get(prevalence_tier, 1.0)

        # --- Age-predisposition factor (if user supplied patient age category) ---
        # age_category should be one of: puppy/kitten/foal/young/adult/senior/geriatric
        age_factor = 1.0
        if age_category:
            disease_age_set = disease.get("age_predisposition")
            if disease_age_set:
                age_lc = str(age_category).lower().strip()
                age_set_lc = {str(a).lower() for a in disease_age_set}
                # Direct match: boost by 10%
                if age_lc in age_set_lc:
                    age_factor = 1.10
                else:
                    # Cross-species age synonyms
                    age_aliases = {
                        "puppy": {"young", "juvenile"},
                        "kitten": {"young", "juvenile"},
                        "foal": {"young", "juvenile"},
                        "young_adult": {"young", "adult"},
                        "geriatric": {"senior"},
                        "elderly": {"senior"},
                    }
                    if age_aliases.get(age_lc, set()) & age_set_lc:
                        age_factor = 1.07
                    # Mismatch penalty: if disease specifies age set and patient
                    # age is clearly outside, mild down-weight
                    elif (
                        age_lc in {"puppy", "kitten", "young", "young_adult"}
                        and age_set_lc == {"senior"}
                        or age_lc in {"senior", "geriatric", "elderly"}
                        and age_set_lc == {"young"}
                    ):
                        age_factor = 0.85

        # --- Onset pattern factor (acute / subacute / chronic) ---
        onset_factor = 1.0
        if onset_pattern:
            disease_onset_set = disease.get("onset_pattern")
            if disease_onset_set:
                onset_lc = str(onset_pattern).lower().strip()
                onset_set_lc = {str(o).lower() for o in disease_onset_set}
                if onset_lc in onset_set_lc:
                    onset_factor = 1.08
                # Mismatch penalty for clear contradiction
                elif (
                    onset_lc == "acute"
                    and onset_set_lc == {"chronic"}
                    or onset_lc == "chronic"
                    and onset_set_lc == {"acute"}
                ):
                    onset_factor = 0.85

        # --- Breed factor (matches common_breeds substring) ---
        breed_factor = 1.0
        if breed:
            disease_breeds = disease.get("common_breeds") or disease.get("breed_predisposition") or ""
            if isinstance(disease_breeds, str) and disease_breeds:
                breed_lc = breed.lower().strip()
                if breed_lc and breed_lc in disease_breeds.lower():
                    breed_factor = 1.12

        # --- Lab abnormality factor ---
        # _lab_boosts maps disease name → multiplier (>1.0 means lab pattern fits disease).
        # Apply best match by name with conservative cap to prevent over-confidence.
        lab_factor = 1.0
        if _lab_boosts:
            # Try Japanese name first then English name; fall back to substring matching
            name_en = disease.get("name", "") or ""
            name_ja = disease.get("name_ja", "") or ""
            best_match = _lab_boosts.get(name_en) or _lab_boosts.get(name_ja)
            if best_match is None:
                # Fuzzy: any boost key contained in (or containing) disease name
                for boost_name, mult in _lab_boosts.items():
                    if (
                        boost_name
                        and (boost_name in name_en or boost_name in name_ja)
                        and (best_match is None or mult > best_match)
                    ):
                        best_match = mult
            if best_match is not None:
                # Clamp to [1.0, 1.40] to avoid runaway certainty from lab alone
                lab_factor = max(1.0, min(float(best_match), 1.40))

        composite = (
            base_score
            * negative_penalty
            * urgency_factor
            * coverage_bonus
            * prevalence_mult
            * age_factor
            * onset_factor
            * breed_factor
            * lab_factor
        )

        # --- Logistic confidence calibration ---
        raw_logistic = 1.0 / (1.0 + math.exp(-6.0 * (composite - 0.4)))
        confidence = min(round(raw_logistic * 100, 1), 95.0)

        # --- Low-information confidence cap ---
        # When user provides very few symptoms, cap confidence to prevent
        # false sense of certainty from non-specific presentations.
        # Use original symptom count (before synonym expansion).
        user_symptom_count = len(symptom_ids)
        if user_symptom_count == 1:
            confidence = min(confidence, 35.0)
        elif user_symptom_count == 2:
            confidence = min(confidence, 55.0)

        matches.append(
            {
                "disease_id": disease.get("name", ""),
                "name_ja": disease.get("name_ja", ""),
                "name_en": disease.get("name", ""),
                "severity": urgency,
                "similarity_score": round(composite, 3),
                "confidence_percent": confidence,
                "matched_symptoms": sorted(matched),
                "unmatched_user_symptoms": sorted(symptom_set - disease_symptoms),
                "additional_disease_symptoms": sorted(disease_symptoms - symptom_set),
                "missing_key_symptoms": sorted(s for s in missing if _compute_weight(s) >= 1.8),
                "description": disease.get("description", ""),
                "description_ja": disease.get("description_ja", ""),
                "description_en": disease.get("description", ""),
                "recommended_tests": disease.get("recommended_tests", []),
                "scoring_detail": {
                    "weighted_recall": round(weighted_recall, 3),
                    "coverage": round(coverage, 3),
                    "negative_penalty": round(negative_penalty, 3),
                    "urgency_factor": urgency_factor,
                    "age_factor": age_factor,
                    "onset_factor": onset_factor,
                    "breed_factor": breed_factor,
                    "lab_factor": round(lab_factor, 3),
                },
            }
        )

    matches.sort(key=lambda m: m["similarity_score"], reverse=True)
    return matches
