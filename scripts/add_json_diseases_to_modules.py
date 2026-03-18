#!/usr/bin/env python3
"""Generate symptom sets for JSON-only diseases and inject them into species modules.

Uses category-based symptom patterns learned from existing module diseases,
combined with keyword-based refinement from disease names, to infer appropriate
symptom IDs for diseases that currently lack them.
"""

import json
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# Force reimport
for key in list(sys.modules.keys()):
    if "api" in key:
        del sys.modules[key]

from scripts.enrich_all_diseases import classify_disease

# ============================================================================
# Step 1: Learn category→symptom patterns from each species module
# ============================================================================

EXOTIC_MODULES = [
    ("rabbit_diseases", "Rabbit"),
    ("hamster_diseases", "Hamster"),
    ("guinea_pig_diseases", "Guinea Pig"),
    ("chinchilla_diseases", "Chinchilla"),
    ("ferret_diseases", "Ferret"),
    ("hedgehog_diseases", "Hedgehog"),
    ("sugar_glider_diseases", "Sugar Glider"),
    ("degu_diseases", "Degu"),
    ("bird_diseases", "Bird"),
    ("parakeet_diseases", "Parakeet"),
    ("parrot_diseases", "Parrot"),
    ("reptile_diseases", "Reptile"),
    ("tortoise_diseases", "Tortoise"),
    ("snake_diseases", "Snake"),
    ("lizard_diseases", "Lizard"),
    ("amphibian_diseases", "Amphibian"),
    ("exotic_other_diseases", "Exotic Other"),
]


def load_species_module(mod_name):
    """Load a species module and return (DISEASES, SYMPTOM_NAMES)."""
    mod = __import__("api.species." + mod_name, fromlist=["DISEASES", "SYMPTOM_NAMES"])
    return mod.DISEASES, getattr(mod, "SYMPTOM_NAMES", {})


def learn_patterns(diseases):
    """Learn category→symptom frequency from existing diseases."""
    cat_symptoms = defaultdict(Counter)
    for d in diseases:
        cat = classify_disease(d["name"], d.get("description", ""))
        for s in d.get("symptoms", set()):
            cat_symptoms[cat][s] += 1
    return cat_symptoms


# ============================================================================
# Step 2: Keyword→symptom refinement
# ============================================================================
# Disease name keywords that strongly suggest specific symptoms

NAME_KEYWORD_SYMPTOMS = {
    # Respiratory keywords
    "pneumonia": ["respiratory_distress", "coughing", "nasal_discharge", "dyspnea", "lethargy", "fever"],
    "respiratory": ["respiratory_distress", "nasal_discharge", "lethargy", "sneezing"],
    "rhinitis": ["nasal_discharge", "sneezing", "facial_swelling"],
    "sinusitis": ["nasal_discharge", "sneezing", "facial_swelling", "lethargy"],
    # GI keywords
    "enteritis": ["diarrhea", "appetite_loss", "lethargy", "dehydration", "abdominal_pain"],
    "gastritis": ["vomiting", "appetite_loss", "abdominal_pain", "lethargy"],
    "colitis": ["diarrhea", "blood_in_stool", "abdominal_pain", "straining"],
    "hepatitis": ["jaundice", "lethargy", "appetite_loss", "vomiting"],
    "stasis": ["appetite_loss", "reduced_fecal_output", "abdominal_pain", "lethargy"],
    "bloat": ["abdominal_distension", "appetite_loss", "lethargy", "abdominal_pain"],
    "impaction": ["constipation", "appetite_loss", "abdominal_distension", "lethargy"],
    "obstruction": ["vomiting", "appetite_loss", "abdominal_pain", "lethargy"],
    "diarrhea": ["diarrhea", "dehydration", "appetite_loss", "lethargy"],
    "coccidiosis": ["diarrhea", "weight_loss", "appetite_loss", "lethargy", "dehydration"],
    # Dermatological keywords
    "dermatitis": ["skin_lesions", "itching", "hair_loss", "skin_redness"],
    "alopecia": ["hair_loss", "skin_lesions"],
    "ringworm": ["hair_loss", "skin_lesions", "scaling", "itching"],
    "mange": ["hair_loss", "itching", "skin_lesions", "crusting"],
    "pyoderma": ["skin_lesions", "pustules", "hair_loss", "itching"],
    "bumblefoot": ["foot_swelling", "lameness", "reduced_activity"],
    "pododermatitis": ["foot_swelling", "lameness", "reduced_activity"],
    # Neurological keywords
    "encephalitis": ["seizures", "ataxia", "head_tilt", "lethargy", "fever"],
    "vestibular": ["head_tilt", "nystagmus", "ataxia", "circling"],
    "paralysis": ["paralysis", "hind_limb_weakness", "urinary_incontinence"],
    "seizure": ["seizures", "tremors", "lethargy"],
    "epilepsy": ["seizures", "tremors", "lethargy"],
    # Ophthalmic keywords
    "conjunctivitis": ["eye_discharge", "eye_redness", "swollen_eyes"],
    "cataract": ["cloudy_eyes", "vision_loss"],
    "glaucoma": ["eye_swelling", "eye_pain", "vision_loss"],
    "uveitis": ["eye_redness", "eye_pain", "photophobia"],
    "keratitis": ["eye_discharge", "eye_redness", "corneal_opacity"],
    # Renal keywords
    "nephritis": ["increased_urination", "increased_thirst", "lethargy", "weight_loss"],
    "cystitis": ["straining_to_urinate", "blood_in_urine", "frequent_urination"],
    "urolithiasis": ["straining_to_urinate", "blood_in_urine", "abdominal_pain"],
    "kidney": ["increased_urination", "increased_thirst", "weight_loss", "lethargy"],
    # Cardiovascular keywords
    "cardiomyopathy": ["exercise_intolerance", "respiratory_distress", "lethargy", "collapse"],
    "heart failure": ["exercise_intolerance", "coughing", "respiratory_distress", "lethargy"],
    "endocarditis": ["fever", "lethargy", "heart_murmur", "exercise_intolerance"],
    # Neoplastic keywords
    "carcinoma": ["weight_loss", "lethargy", "appetite_loss", "swelling"],
    "lymphoma": ["weight_loss", "lethargy", "swelling", "appetite_loss"],
    "sarcoma": ["swelling", "lameness", "weight_loss", "lethargy"],
    "adenoma": ["swelling", "lethargy"],
    "tumor": ["swelling", "weight_loss", "lethargy", "appetite_loss"],
    "fibroma": ["swelling", "skin_mass"],
    "lipoma": ["swelling", "skin_mass"],
    # Reproductive keywords
    "dystocia": ["straining", "lethargy", "abdominal_contractions"],
    "mastitis": ["mammary_swelling", "fever", "appetite_loss", "lethargy"],
    "pyometra": ["vaginal_discharge", "lethargy", "increased_thirst", "fever"],
    "egg binding": ["straining", "lethargy", "abdominal_distension"],
    # Metabolic/Endocrine keywords
    "diabetes": ["increased_thirst", "increased_urination", "weight_loss", "lethargy"],
    "hypothyroid": ["weight_gain", "lethargy", "hair_loss"],
    "hyperthyroid": ["weight_loss", "increased_appetite", "hyperactivity"],
    "cushing": ["increased_thirst", "increased_urination", "hair_loss", "pot_belly"],
    "adrenal": ["hair_loss", "lethargy", "weight_loss"],
    # Nutritional keywords
    "deficiency": ["lethargy", "weight_loss", "appetite_loss"],
    "vitamin": ["lethargy", "weight_loss", "appetite_loss"],
    "mbd": ["tremors", "weakness", "soft_bones", "lethargy"],
    "metabolic bone": ["tremors", "weakness", "soft_bones", "lethargy"],
    "scurvy": ["lethargy", "joint_swelling", "lameness", "weight_loss"],
    "obesity": ["weight_gain", "lethargy", "reduced_activity"],
    # Dental keywords
    "malocclusion": ["appetite_loss", "weight_loss", "drooling", "difficulty_eating"],
    "dental": ["appetite_loss", "drooling", "difficulty_eating", "weight_loss"],
    "abscess": ["swelling", "fever", "appetite_loss", "lethargy"],
    # Parasitic keywords
    "mite": ["itching", "hair_loss", "skin_lesions", "scratching"],
    "flea": ["itching", "scratching", "hair_loss"],
    "worm": ["weight_loss", "diarrhea", "appetite_loss"],
    "tapeworm": ["weight_loss", "diarrhea"],
    "heartworm": ["coughing", "exercise_intolerance", "lethargy"],
    # Toxic keywords
    "toxicosis": ["lethargy", "vomiting", "seizures", "diarrhea"],
    "poisoning": ["lethargy", "vomiting", "seizures", "diarrhea"],
    # Behavioral keywords
    "anxiety": ["overgrooming", "hiding", "aggression", "appetite_loss"],
    "feather pluck": ["feather_loss", "self_mutilation", "skin_lesions"],
    "self-mutilation": ["self_mutilation", "skin_lesions", "hair_loss"],
    "stress": ["appetite_loss", "hiding", "lethargy"],
    # Traumatic keywords
    "fracture": ["lameness", "swelling", "pain", "reduced_activity"],
    "wound": ["bleeding", "swelling", "lethargy"],
    "burn": ["skin_lesions", "lethargy", "appetite_loss"],
    "prolapse": ["visible_tissue", "straining", "lethargy"],
}

# Urgency mapping
URGENCY_FROM_CATEGORY = {
    "viral": "high",
    "bacterial": "high",
    "fungal": "moderate",
    "parasitic": "moderate",
    "neoplastic": "high",
    "metabolic": "moderate",
    "nutritional": "moderate",
    "toxic": "emergency",
    "traumatic": "high",
    "dental": "moderate",
    "autoimmune": "moderate",
    "cardiovascular": "high",
    "respiratory": "high",
    "renal": "high",
    "gastrointestinal": "moderate",
    "reproductive": "high",
    "neurological": "high",
    "dermatological": "low",
    "ophthalmic": "moderate",
    "orthopedic": "moderate",
    "congenital": "moderate",
    "behavioral": "low",
    "general": "moderate",
}


def infer_symptoms(disease_name, description, category, species_patterns, species_symptom_ids):
    """Infer a set of symptom IDs for a disease based on category and name keywords."""
    symptoms = set()

    # 1. Get top symptoms from the category pattern (species-specific)
    if category in species_patterns:
        top_cat = species_patterns[category].most_common(8)
        for symptom_id, _count in top_cat:
            if symptom_id in species_symptom_ids:
                symptoms.add(symptom_id)

    # 2. Refine with name keyword matching
    name_lower = disease_name.lower()
    desc_lower = description.lower()
    combined = name_lower + " " + desc_lower

    for keyword, keyword_symptoms in NAME_KEYWORD_SYMPTOMS.items():
        if keyword in combined:
            for s in keyword_symptoms:
                if s in species_symptom_ids:
                    symptoms.add(s)

    # 3. Ensure minimum symptom count (at least 3)
    if len(symptoms) < 3:
        # Add common general symptoms
        general_fallbacks = ["lethargy", "appetite_loss", "weight_loss"]
        for s in general_fallbacks:
            if s in species_symptom_ids:
                symptoms.add(s)

    # 4. Cap at reasonable maximum
    if len(symptoms) > 10:
        # Keep the most relevant (intersection of category + keyword)
        symptoms = set(list(symptoms)[:10])

    return symptoms


def generate_module_entry(json_disease, category, symptoms, species_symptom_ids):
    """Generate a module-compatible disease dict from JSON data + inferred symptoms."""
    name = json_disease["name"]
    urgency = URGENCY_FROM_CATEGORY.get(category, "moderate")

    # Refine urgency based on name keywords
    name_lower = name.lower()
    if any(w in name_lower for w in ["acute", "hemorrhagic", "septic", "fulminant"]):
        urgency = "emergency"
    elif any(w in name_lower for w in ["chronic", "mild", "benign"]) and urgency in ("emergency", "high"):
        urgency = "moderate"

    entry = {
        "name": name,
        "name_ja": json_disease.get("name_ja", name),
        "symptoms": symptoms,
        "description": json_disease.get("description", ""),
        "description_ja": json_disease.get("description_ja", ""),
        "urgency": urgency,
    }

    return entry


def main():
    # Load JSON database
    json_path = os.path.join(ROOT, "diseases_all_species.json")
    with open(json_path, encoding="utf-8") as f:
        json_data = json.load(f)

    # Load all species modules and their patterns
    species_data = {}
    for mod_name, sp in EXOTIC_MODULES:
        diseases, symptom_names = load_species_module(mod_name)
        patterns = learn_patterns(diseases)
        existing_names = {d["name"] for d in diseases}
        symptom_ids = set(symptom_names.keys())
        species_data[sp] = {
            "mod_name": mod_name,
            "diseases": diseases,
            "symptom_names": symptom_names,
            "patterns": patterns,
            "existing_names": existing_names,
            "symptom_ids": symptom_ids,
        }

    # Also handle Cat
    from api.species.cat_diseases import DISEASES as cat_diseases
    from api.species.cat_diseases import SYMPTOM_NAMES as cat_symptoms
    cat_patterns = learn_patterns(cat_diseases)
    species_data["Cat"] = {
        "mod_name": "cat_diseases",
        "diseases": cat_diseases,
        "symptom_names": cat_symptoms,
        "patterns": cat_patterns,
        "existing_names": {d["name"] for d in cat_diseases},
        "symptom_ids": set(cat_symptoms.keys()),
    }

    # Find JSON-only diseases and generate entries
    new_entries_by_species = defaultdict(list)
    total_generated = 0

    for jd in json_data:
        sp = jd["species"]
        name = jd["name"]

        if sp not in species_data:
            continue  # Skip species without modules (Horse, Multiple, etc.)

        sd = species_data[sp]
        if name in sd["existing_names"]:
            continue  # Already in module

        category = classify_disease(name, jd.get("description", ""))
        symptoms = infer_symptoms(
            name, jd.get("description", ""), category,
            sd["patterns"], sd["symptom_ids"]
        )

        entry = generate_module_entry(jd, category, symptoms, sd["symptom_ids"])
        new_entries_by_species[sp].append(entry)
        total_generated += 1

    print(f"Generated {total_generated} new module entries")
    print()

    # Write new entries to module files
    for sp, entries in sorted(new_entries_by_species.items()):
        sd = species_data[sp]
        mod_name = sd["mod_name"]
        mod_path = os.path.join(ROOT, "api", "species", f"{mod_name}.py")

        print(f"  {sp}: +{len(entries)} diseases (was {len(sd['existing_names'])}, now {len(sd['existing_names']) + len(entries)})")

        # Generate Python code for new entries
        new_code_lines = []
        new_code_lines.append("")
        new_code_lines.append(f"# --- Auto-generated entries ({len(entries)} diseases) ---")
        new_code_lines.append("# Added by scripts/add_json_diseases_to_modules.py")

        for entry in sorted(entries, key=lambda e: e["name"]):
            symptoms_str = ", ".join(f'"{s}"' for s in sorted(entry["symptoms"]))
            name_escaped = entry["name"].replace('"', '\\"')
            name_ja_escaped = entry["name_ja"].replace('"', '\\"')
            desc_escaped = entry["description"].replace('"', '\\"').replace("\n", " ")

            new_code_lines.append("    {")
            new_code_lines.append(f'        "name": "{name_escaped}",')
            new_code_lines.append(f'        "name_ja": "{name_ja_escaped}",')
            new_code_lines.append(f"        \"symptoms\": {{{symptoms_str}}},")
            new_code_lines.append(f'        "description": "{desc_escaped}",')
            new_code_lines.append(f'        "urgency": "{entry["urgency"]}",')
            new_code_lines.append("    },")

        # Find insertion point: before the closing ] of DISEASES list
        with open(mod_path, encoding="utf-8") as f:
            content = f.read()

        import re

        # Strategy: find "DISEASES" assignment, then find "enrich_diseases" call.
        # Between them, the DISEASES list's closing "]" sits on its own line.
        diseases_start = content.find("DISEASES")
        enrich_match = re.search(r"\nenrich_diseases\(DISEASES,", content)

        if enrich_match and diseases_start >= 0:
            segment = content[diseases_start : enrich_match.start()]
            # Find the last "]" in the segment (closing of DISEASES list)
            bracket_offset = segment.rfind("]")
            if bracket_offset >= 0:
                bracket_pos = diseases_start + bracket_offset
                insert_code = "\n".join(new_code_lines) + "\n"
                content = content[:bracket_pos] + insert_code + content[bracket_pos:]

                with open(mod_path, "w", encoding="utf-8") as f:
                    f.write(content)
            else:
                print(f"    WARNING: Could not find closing ] for {sp}")
        else:
            print(f"    WARNING: Could not find enrich_diseases call for {sp}")

    print(f"\nDone. Total new entries: {total_generated}")


if __name__ == "__main__":
    main()
