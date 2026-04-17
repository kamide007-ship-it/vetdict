"""Symptom extraction from natural language text.

Extracts symptom IDs from JP/EN text using longest-match-first strategy.
"""

from api.chat.species_data import _SPECIES_DATA
from api.chat.symptom_aliases import SYMPTOM_ALIASES


def _extract_species_symptoms(text: str, species: str) -> list[str]:
    """Extract symptom IDs from text using species-specific SYMPTOM_NAMES.

    Uses longest-match-first strategy and Japanese particle splitting
    for maximum extraction accuracy across all species.
    """
    sp_data = _SPECIES_DATA.get(species)
    if not sp_data:
        return []

    text_lower = text.lower()
    matched: set[str] = set()
    symptom_names = sp_data["symptom_names"]

    # Cross-species ID mapping: dog aliases use "loss_of_appetite" but many
    # species modules use "appetite_loss", "anorexia", etc. for the same concept.
    _ID_SYNONYMS: dict[str, list[str]] = {
        # Appetite
        "loss_of_appetite": ["appetite_loss", "anorexia", "poor_appetite", "decreased_appetite"],
        "appetite_loss": ["loss_of_appetite", "anorexia", "poor_appetite", "decreased_appetite"],
        "anorexia": ["loss_of_appetite", "appetite_loss", "poor_appetite"],
        # General
        "lethargy": ["depression", "inactivity", "weakness", "listlessness", "muscle_wasting"],
        "weakness": ["lethargy", "depression", "inactivity"],
        "depression": ["lethargy", "inactivity", "weakness"],
        "fever": ["hyperthermia", "elevated_temperature"],
        # GI
        "diarrhea": ["loose_stool", "watery_stool", "soft_stool"],
        "vomiting": ["regurgitation", "emesis"],
        "constipation": ["reduced_fecal_output", "straining_to_defecate", "small_fecal_pellets", "decreased_fecal_output"],
        "reduced_fecal_output": ["constipation", "small_fecal_pellets", "decreased_fecal_output"],
        "decreased_fecal_output": ["reduced_fecal_output", "constipation", "small_fecal_pellets"],
        "small_fecal_pellets": ["reduced_fecal_output", "constipation"],
        "teeth_grinding": ["bruxism", "dental_pain"],
        "abdominal_pain": ["abdominal_distension", "hunched_posture", "bloating"],
        "bloating": ["abdominal_distension", "abdominal_distention", "distended_abdomen", "abdominal_pain"],
        "abdominal_distension": ["bloating", "abdominal_distention", "distended_abdomen", "abdominal_pain"],
        # Neuro
        "seizures": ["convulsions", "fits", "epileptic_episodes"],
        "fainting": ["collapse", "syncope"],
        "collapse": ["fainting", "syncope"],
        "paralysis_or_paresis": ["paralysis", "paresis", "hind_limb_weakness", "hind_limb_paralysis", "posterior_paresis", "progressive_paralysis", "hindlimb_weakness", "hind_leg_weakness"],
        "paralysis": ["paralysis_or_paresis", "paresis", "hind_limb_weakness", "hind_limb_paralysis"],
        "hind_leg_weakness": ["hind_limb_weakness", "hindlimb_weakness", "posterior_paresis"],
        "hind_limb_weakness": ["hind_leg_weakness", "hindlimb_weakness", "posterior_paresis", "progressive_paralysis"],
        "jaundice": ["icterus", "yellow_skin", "yellow_mucous_membranes"],
        # Weight / body
        "weight_loss": ["emaciation", "wasting", "cachexia", "rough_coat", "poor_growth"],
        "weight_gain": ["obesity", "overweight"],
        "emaciation": ["weight_loss", "wasting", "cachexia"],
        # Skin / coat
        "excessive_drooling": ["drooling", "hypersalivation", "ptyalism"],
        "drooling": ["excessive_drooling", "hypersalivation"],
        "bad_breath": ["halitosis", "oral_odor"],
        "oral_ulcers": ["mouth_lesions", "stomatitis", "gingivitis"],
        "excessive_licking": ["itching", "pruritus", "scratching", "overgrooming", "ear_scratching", "scratching_ears"],
        "pop_eye": ["exophthalmia", "exophthalmos", "eye_protrusion", "bulging_eye", "eye_swelling", "eye_bulging", "enlarged_eye"],
        "eye_protrusion": ["pop_eye", "exophthalmia", "exophthalmos", "eye_bulging", "bulging_eye", "eye_swelling", "enlarged_eye", "proptosis"],
        "eye_swelling": ["pop_eye", "exophthalmia", "exophthalmos", "periorbital_swelling", "swollen_eyes", "bulging_eye", "eye_swollen", "eye_bulging", "enlarged_eye", "eye_protrusion"],
        "eye_bulging": ["pop_eye", "exophthalmia", "exophthalmos", "eye_protrusion", "eye_swelling", "bulging_eye", "enlarged_eye", "proptosis"],
        "exophthalmos": ["pop_eye", "eye_protrusion", "eye_bulging", "eye_swelling", "bulging_eye", "enlarged_eye", "proptosis"],
        "enlarged_eye": ["eye_bulging", "eye_swelling", "exophthalmos", "pop_eye", "eye_protrusion"],
        "ear_discharge": ["ear_infection", "ear_inflammation", "otitis", "ear_mites"],
        "blood_in_urine": ["hematuria", "bloody_urine", "uterine_bleeding", "blood_urine"],
        "blood_urine": ["blood_in_urine", "hematuria", "bloody_urine"],
        "blood_in_stool": ["melena", "hematochezia", "bloody_stool", "bleeding_gums"],
        "itching": ["pruritus", "scratching", "scratching_ears", "ear_scratching", "excessive_grooming", "excessive_licking", "overgrooming"],
        "pruritus": ["itching", "scratching", "excessive_licking"],
        "lameness_or_limping": ["lameness", "limping", "joint_swelling", "joint_pain", "leg_swelling", "foot_swelling", "reluctance_to_move"],
        "lumps_and_bumps": ["lumps_nodules", "skin_masses", "tumors", "skin_lumps"],
        # Hair
        "hair_loss": ["alopecia", "fur_loss", "feather_loss", "bald_patches", "quill_loss", "severe_quill_loss", "scaling", "circular_hair_loss"],
        "circular_hair_loss": ["hair_loss", "alopecia", "fur_loss", "bald_patches"],
        "alopecia": ["hair_loss", "fur_loss", "bald_patches", "circular_hair_loss"],
        "feather_loss": ["hair_loss", "feather_plucking", "alopecia"],
        "skin_lesions": ["scaling", "dermatitis", "skin_rash", "crusting", "thick_crusting", "flaky_skin", "dry_skin", "shell_discoloration", "shell_pitting", "skin_crusting"],
        "scaly_skin": ["scaling", "dandruff", "skin_crusting", "dry_skin", "flaky_skin"],
        "skin_crusting": ["scaling", "scaly_skin", "dandruff", "crusting"],
        "scaling": ["skin_lesions", "dandruff", "scaly_skin", "skin_crusting"],
        "dandruff": ["scaling", "scaly_skin", "skin_crusting"],
        # Eyes
        "cloudiness_in_eyes": ["cloudy_eyes", "eye_cloudiness", "corneal_opacity", "cloudy_eye", "corneal_cloudiness"],
        "cloudy_eyes": ["cloudiness_in_eyes", "eye_cloudiness", "corneal_opacity", "cloudy_eye", "corneal_cloudiness"],
        "cloudy_eye": ["cloudy_eyes", "cloudiness_in_eyes", "eye_cloudiness", "corneal_cloudiness"],
        "corneal_opacity": ["corneal_cloudiness", "cloudy_eyes", "cloudy_eye", "cloudiness_in_eyes"],
        "corneal_cloudiness": ["corneal_opacity", "cloudy_eyes", "cloudy_eye", "cloudiness_in_eyes"],
        "redness_in_eyes": ["red_eyes", "conjunctivitis", "eye_redness"],
        "eye_discharge": ["ocular_discharge", "eye_secretion", "epiphora"],
        "squinting": ["blepharospasm", "eye_squinting"],
        "tearing": ["excessive_tearing", "epiphora", "eye_discharge"],
        "excessive_tearing": ["tearing", "epiphora", "eye_discharge"],
        "vision_loss": ["blindness", "cloudy_eye", "cloudy_eyes", "cataracts"],
        # Respiratory
        "labored_breathing": ["respiratory_distress", "dyspnea", "open_mouth_breathing", "difficulty_breathing"],
        "respiratory_distress": ["labored_breathing", "dyspnea", "open_mouth_breathing"],
        "open_mouth_breathing": ["labored_breathing", "respiratory_distress", "mouth_breathing"],
        "rapid_breathing": ["tachypnea", "panting", "labored_breathing"],
        "coughing": ["cough", "kennel_cough"],
        "wheezing": ["coughing", "labored_breathing", "respiratory_distress"],
        "sneezing": ["reverse_sneezing", "nasal_irritation", "nasal_discharge"],
        "nasal_discharge": ["runny_nose", "rhinorrhea", "nasal_secretion", "sneezing"],
        # Urinary
        "straining_to_urinate": ["dysuria", "urinary_straining", "difficulty_urinating", "stranguria", "straining_urinate"],
        "straining_urinate": ["straining_to_urinate", "dysuria", "urinary_straining", "difficulty_urinating"],
        "frequent_urination": ["pollakiuria", "polyuria", "excessive_urination", "increased_urination"],
        "excessive_urination": ["frequent_urination", "polyuria", "pollakiuria", "increased_urination"],
        "increased_urination": ["excessive_urination", "frequent_urination", "polyuria", "pollakiuria"],
        "cloudy_urine": ["turbid_urine", "murky_urine"],
        "foul_smelling_urine": ["malodorous_urine", "urine_odor"],
        "incontinence": ["urine_leakage", "urinary_incontinence"],
        "increased_thirst": ["excessive_thirst", "polydipsia"],
        "excessive_thirst": ["increased_thirst", "polydipsia"],
        "polydipsia": ["excessive_thirst", "increased_thirst"],
        "polyuria": ["excessive_urination", "frequent_urination", "increased_urination"],
        # Musculoskeletal
        "joint_pain_or_stiffness": ["joint_pain", "arthritis", "stiffness"],
        # Behavior
        "anxiety": ["restlessness", "pacing", "nervousness"],
        "self_mutilation": ["self_chewing", "self_harm", "overgrooming", "feather_plucking"],
        "self_chewing": ["self_mutilation", "self_harm"],
        "behavioral_change": ["behavioral_changes", "aggression", "depression", "restlessness"],
        "behavioral_changes": ["behavioral_change", "aggression", "depression"],
        # Head
        "head_tilt": ["vestibular_signs", "torticollis", "wry_neck", "nystagmus"],
        "nystagmus": ["head_tilt", "vestibular_signs", "rolling"],
        "ataxia": ["tremors", "incoordination", "wobbling", "unsteady_gait"],
        "tremors": ["shaking", "trembling", "muscle_tremors", "ataxia"],
        "wobbling": ["ataxia", "incoordination", "unsteady_gait", "stumbling"],
        # Reptile-specific
        "dysecdysis": ["abnormal_shedding", "retained_shed", "shedding_problems", "retained_skin"],
        "retained_shed": ["dysecdysis", "retained_skin", "shedding_problems"],
        "retained_skin": ["dysecdysis", "retained_shed", "shedding_problems"],
        "soft_bones": ["bone_weakness", "jaw_softening", "shell_soft_spots", "fractures", "bone_deformity", "shell_softening", "soft_shell"],
        "bone_deformity": ["bone_swelling", "limb_deformity", "soft_bones", "shell_deformity", "fractures"],
        "shell_softening": ["soft_shell", "soft_bones", "shell_soft_spots", "shell_deformity"],
        "soft_shell": ["shell_softening", "soft_bones", "shell_soft_spots", "shell_deformity"],
        "shell_deformity": ["bone_deformity", "soft_shell", "shell_softening"],
        "mouth_lesions": ["oral_lesions", "stomatitis", "mouth_rot"],
        "mucus_in_mouth": ["oral_mucus", "mouth_discharge"],
        # Limbs / extremities
        "cold_limbs": ["cold_extremities", "poor_circulation"],
        "cold_extremities": ["cold_limbs", "poor_circulation"],
        # Bird-specific
        "fluffed_feathers": ["feather_fluffing", "puffed_up", "ruffled_feathers"],
        "feather_plucking": ["feather_loss", "self_mutilation", "feather_destructive_behavior"],
        "crop_swelling": ["crop_stasis", "ingluvitis", "crop_distension"],
        "crop_stasis": ["crop_swelling", "ingluvitis"],
        # Fish fin
        "frayed_fins": ["fin_rot", "fin_erosion", "ragged_fins"],
        "fin_rot": ["frayed_fins", "fin_erosion"],
        "redness_skin": ["skin_redness", "hemorrhage", "fin_hemorrhage"],
        "skin_redness": ["redness_skin", "hemorrhage", "red_legs", "red_ventrum"],
        "fin_hemorrhage": ["redness_skin", "hemorrhage"],
        # Hamster
        "wet_tail": ["diarrhea", "watery_diarrhea"],
        # Skin / coat additional
        "thinning_skin": ["skin_fragility", "thin_skin", "fragile_skin"],
        "poor_coat": ["dry_skin", "rough_coat", "dull_coat"],
        "rough_coat": ["poor_coat", "dry_skin", "dull_coat"],
        # Ferret reproductive
        "vulvar_swelling": ["vulvar_discharge", "genital_swelling"],
        "prostatic_enlargement": ["prostate_enlargement", "enlarged_prostate"],
        # Cardiac
        "bradycardia": ["slow_heart_rate"],
        # Cheek / oral
        "cheek_swelling": ["bloating", "cheek_pouch_prolapse", "facial_swelling"],
        "cheek_pouch_prolapse": ["cheek_swelling"],
        "jaw_swelling": ["facial_swelling", "swelling"],
        "abscess": ["discharge", "swelling"],
        "overgrown_teeth": ["dental_overgrowth", "incisor_overgrowth", "molar_overgrowth", "tooth_overgrowth", "malocclusion", "visible_tooth_overgrowth"],
        "dental_overgrowth": ["overgrown_teeth", "incisor_overgrowth", "molar_overgrowth", "malocclusion", "visible_tooth_overgrowth"],
        "visible_tooth_overgrowth": ["overgrown_teeth", "dental_overgrowth", "malocclusion"],
        "scaly_legs": ["leg_scales", "scaly_face"],
        "leg_scales": ["scaly_legs", "scaly_face"],
        # Pain
        "pain": ["lethargy", "vocalization"],
        # Oral
        "stomatitis": ["oral_ulcers", "bad_breath", "excessive_drooling"],
        # Perianal
        "perineal_swelling": ["perianal_irritation", "swelling"],
        # Guinea pig scurvy
        "bleeding_gums": ["swollen_gums", "oral_bleeding"],
        "swollen_joints": ["joint_swelling", "lameness_or_limping", "lameness"],
        # Fish
        "darkened_coloration": ["dark_coloration", "discoloration"],
        "dark_coloration": ["darkened_coloration", "discoloration"],
        # Amphibian
        "red_legs": ["red_ventrum", "skin_redness", "hemorrhage"],
        "red_ventrum": ["red_legs", "skin_redness", "hemorrhage"],
        "edema": ["swelling", "bloating", "ascites"],
        # Effusion
        "effusion": ["pleural_effusion", "abdominal_distension", "ascites"],
        "pleural_effusion": ["effusion", "labored_breathing"],
        "ascites": ["effusion", "abdominal_distension", "bloating", "dropsy"],
        "dropsy": ["bloating", "edema", "ascites", "abdominal_distension"],
        # Swelling (generic)
        "swelling": ["facial_swelling", "eye_swelling", "edema"],
    }

    def _resolve_id(sid: str) -> str | None:
        """Return the symptom ID that exists in this species' SYMPTOM_NAMES."""
        if sid in symptom_names:
            return sid
        for alt in _ID_SYNONYMS.get(sid, []):
            if alt in symptom_names:
                return alt
        return None

    # Phase 1: Longest-match-first alias matching (aliases → species symptom IDs)
    # Track consumed character positions to avoid substring double-matching
    # (e.g. "外陰部が腫れてる" should not also match "腫れてる")
    _sorted_aliases = sorted(SYMPTOM_ALIASES.keys(), key=len, reverse=True)
    _consumed: set[int] = set()
    for alias in _sorted_aliases:
        pos = text_lower.find(alias)
        if pos >= 0:
            alias_range = set(range(pos, pos + len(alias)))
            if alias_range & _consumed:
                continue
            symptom_id = SYMPTOM_ALIASES[alias]
            resolved = _resolve_id(symptom_id)
            if resolved:
                matched.add(resolved)
                _consumed |= alias_range

    # Phase 2: Direct symptom name matches (ja/en)
    for sym_id, names in symptom_names.items():
        ja = names.get("ja", "").lower()
        en = names.get("en", "").lower()
        if (ja and ja in text_lower) or (en and en in text_lower):
            matched.add(sym_id)

    # Phase 3: Fragment splitting for compound Japanese phrases
    if not matched:
        import re as _re
        fragments = _re.split(r'[、。,.と！!？?\s]+', text_lower)
        fragments = [f.strip() for f in fragments if len(f.strip()) >= 1]
        for frag in fragments:
            for alias in _sorted_aliases:
                if alias in frag:
                    sid = SYMPTOM_ALIASES[alias]
                    if sid in symptom_names:
                        matched.add(sid)
                        break
            for sym_id, names in symptom_names.items():
                ja = names.get("ja", "").lower()
                en = names.get("en", "").lower()
                if (ja and ja in frag) or (en and en in frag):
                    matched.add(sym_id)

    return list(matched)


