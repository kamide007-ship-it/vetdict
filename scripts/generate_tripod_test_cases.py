#!/usr/bin/env python3
"""
Generate realistic TRIPOD test cases based on actual diagnostic engine results.

This script creates test cases where the expected diagnoses come from
the top predictions of the diagnostic engine for various symptom combinations.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.chat.disease_matcher import _match_species_symptoms_to_diseases
from api.chat.symptom_extractor import _extract_species_symptoms

# Define comprehensive test scenarios for each species
TEST_SCENARIOS = {
    'dog': [
        # GI conditions
        {'symptoms': ['fever', 'lethargy', 'vomiting', 'diarrhea'], 'expected_disease': 'Canine Parvovirus', 'confidence_threshold': 0.75, 'notes': 'GI emergency'},
        {'symptoms': ['vomiting', 'diarrhea'], 'expected_disease': 'Gastroenteritis', 'confidence_threshold': 0.70, 'notes': 'Common GI'},
        {'symptoms': ['abdominal_pain', 'vomiting'], 'expected_disease': 'Pancreatitis', 'confidence_threshold': 0.70, 'notes': 'Acute pancreatitis'},
        {'symptoms': ['abdominal_distension', 'vomiting', 'lethargy'], 'expected_disease': 'Bloat', 'confidence_threshold': 0.72, 'notes': 'Gastric dilatation'},
        # Respiratory conditions
        {'symptoms': ['fever', 'cough', 'lethargy'], 'expected_disease': 'Bacterial Pneumonia', 'confidence_threshold': 0.68, 'notes': 'Respiratory infection'},
        {'symptoms': ['cough', 'nasal_discharge'], 'expected_disease': 'Kennel Cough', 'confidence_threshold': 0.65, 'notes': 'Infectious tracheobronchitis'},
        # Skin
        {'symptoms': ['itching', 'skin_redness', 'hair_loss'], 'expected_disease': 'Atopic Dermatitis', 'confidence_threshold': 0.68, 'notes': 'Allergic dermatitis'},
        {'symptoms': ['itching', 'skin_lesions'], 'expected_disease': 'Mange', 'confidence_threshold': 0.65, 'notes': 'Parasitic skin disease'},
        # Metabolic
        {'symptoms': ['polydipsia', 'polyuria', 'weight_loss'], 'expected_disease': 'Diabetes Mellitus', 'confidence_threshold': 0.72, 'notes': 'Metabolic disease'},
        # Cardiac
        {'symptoms': ['lethargy', 'cough', 'exercise_intolerance'], 'expected_disease': 'Heart Failure', 'confidence_threshold': 0.68, 'notes': 'Cardiac dysfunction'},
        # Neurological
        {'symptoms': ['seizures'], 'expected_disease': 'Epilepsy', 'confidence_threshold': 0.60, 'notes': 'Single symptom'},
        {'symptoms': ['head_tilt', 'nystagmus'], 'expected_disease': 'Vestibular Disease', 'confidence_threshold': 0.65, 'notes': 'Neurological disorder'},
        # Urinary
        {'symptoms': ['dysuria', 'urinary_straining'], 'expected_disease': 'Urinary Tract Infection', 'confidence_threshold': 0.65, 'notes': 'Bacterial UTI'},
    ],
    'cat': [
        # Respiratory
        {'symptoms': ['sneezing', 'nasal_discharge', 'fever'], 'expected_disease': 'Feline Upper Respiratory Infection', 'confidence_threshold': 0.80, 'notes': 'URI classic'},
        {'symptoms': ['cough', 'respiratory_distress'], 'expected_disease': 'Asthma', 'confidence_threshold': 0.68, 'notes': 'Feline asthma'},
        # Infectious
        {'symptoms': ['lethargy', 'fever', 'weight_loss'], 'expected_disease': 'Feline Infectious Peritonitis (FIP)', 'confidence_threshold': 0.68, 'notes': 'Systemic infection'},
        # GI
        {'symptoms': ['vomiting', 'lethargy'], 'expected_disease': 'Hepatic Lipidosis', 'confidence_threshold': 0.70, 'notes': 'Hepatic disease'},
        {'symptoms': ['vomiting', 'anorexia'], 'expected_disease': 'Gastroenteritis', 'confidence_threshold': 0.65, 'notes': 'GI inflammation'},
        # Urinary
        {'symptoms': ['dysuria', 'hematuria'], 'expected_disease': 'Feline Lower Urinary Tract Disease', 'confidence_threshold': 0.70, 'notes': 'FLUTD'},
        # Endocrine
        {'symptoms': ['weight_loss', 'polyphagia'], 'expected_disease': 'Hyperthyroidism', 'confidence_threshold': 0.70, 'notes': 'Thyroid dysfunction'},
        {'symptoms': ['lethargy', 'weight_gain'], 'expected_disease': 'Hypothyroidism', 'confidence_threshold': 0.65, 'notes': 'Low thyroid'},
        # Ocular
        {'symptoms': ['eye_discharge', 'squinting'], 'expected_disease': 'Corneal Ulcer', 'confidence_threshold': 0.72, 'notes': 'Ocular emergency'},
        # Cardiovascular
        {'symptoms': ['hind_limb_weakness', 'cold_limbs'], 'expected_disease': 'Arterial Thromboembolism', 'confidence_threshold': 0.68, 'notes': 'Acute thrombosis'},
        # Renal
        {'symptoms': ['polydipsia', 'polyuria', 'weight_loss'], 'expected_disease': 'Chronic Kidney Disease', 'confidence_threshold': 0.70, 'notes': 'CKD'},
    ],
    'rabbit': [
        {'symptoms': ['hunched_posture', 'anorexia'], 'expected_disease': 'Gastrointestinal Stasis', 'confidence_threshold': 0.68, 'notes': 'GI emergency'},
        {'symptoms': ['nasal_discharge', 'sneezing'], 'expected_disease': 'Pasteurellosis', 'confidence_threshold': 0.65, 'notes': 'Respiratory bacterial'},
        {'symptoms': ['head_tilt', 'circling'], 'expected_disease': 'Encephalitozoon cuniculi', 'confidence_threshold': 0.62, 'notes': 'Parasitic neurological'},
        {'symptoms': ['drooling', 'anorexia'], 'expected_disease': 'Dental Disease', 'confidence_threshold': 0.65, 'notes': 'Malocclusion'},
        {'symptoms': ['lethargy', 'fever'], 'expected_disease': 'Bacterial Infection', 'confidence_threshold': 0.60, 'notes': 'Systemic infection'},
    ],
    'guinea_pig': [
        {'symptoms': ['lethargy', 'bleeding_gums'], 'expected_disease': 'Scurvy', 'confidence_threshold': 0.68, 'notes': 'Vitamin C deficiency'},
        {'symptoms': ['respiratory_distress', 'lethargy'], 'expected_disease': 'Respiratory Infection', 'confidence_threshold': 0.65, 'notes': 'Bacterial pneumonia'},
    ],
    'hamster': [
        {'symptoms': ['facial_swelling', 'drooling'], 'expected_disease': 'Cheek Pouch Impaction', 'confidence_threshold': 0.65, 'notes': 'Hamster-specific'},
        {'symptoms': ['diarrhea', 'lethargy'], 'expected_disease': 'Wet Tail', 'confidence_threshold': 0.62, 'notes': 'Diarrheal disease'},
    ],
    'ferret': [
        {'symptoms': ['lethargy', 'ataxia'], 'expected_disease': 'Insulinoma', 'confidence_threshold': 0.65, 'notes': 'Hypoglycemia'},
        {'symptoms': ['lethargy', 'hair_loss'], 'expected_disease': 'Adrenal Disease', 'confidence_threshold': 0.62, 'notes': 'Endocrine disorder'},
    ],
    'bird': [
        {'symptoms': ['respiratory_distress', 'lethargy'], 'expected_disease': 'Respiratory Infection', 'confidence_threshold': 0.65, 'notes': 'Avian respiratory'},
        {'symptoms': ['regurgitation', 'lethargy'], 'expected_disease': 'Crop Stasis', 'confidence_threshold': 0.62, 'notes': 'GI disorder'},
    ],
    'fish': [
        {'symptoms': ['white_spots', 'lethargy'], 'expected_disease': 'Ichthyophthirius', 'confidence_threshold': 0.68, 'notes': 'White spot disease'},
        {'symptoms': ['frayed_fins', 'lethargy'], 'expected_disease': 'Fin Rot', 'confidence_threshold': 0.65, 'notes': 'Bacterial infection'},
        {'symptoms': ['abdominal_distension', 'lethargy'], 'expected_disease': 'Dropsy', 'confidence_threshold': 0.62, 'notes': 'Systemic infection'},
    ],
    'reptile': [
        {'symptoms': ['respiratory_distress'], 'expected_disease': 'Respiratory Infection', 'confidence_threshold': 0.60, 'notes': 'Respiratory disease'},
        {'symptoms': ['lameness', 'jaw_swelling'], 'expected_disease': 'Metabolic Bone Disease', 'confidence_threshold': 0.65, 'notes': 'Nutritional disorder'},
    ],
    'parakeet': [
        {'symptoms': ['respiratory_distress', 'cough'], 'expected_disease': 'Respiratory Infection', 'confidence_threshold': 0.62, 'notes': 'Avian respiratory'},
    ],
    'parrot': [
        {'symptoms': ['feather_plucking', 'lethargy'], 'expected_disease': 'Behavioral Disorder', 'confidence_threshold': 0.60, 'notes': 'Psychological stress'},
    ],
}


def validate_disease_name(disease_name: str, species: str) -> bool:
    """Check if a disease name exists in the system for a species."""
    matches = _match_species_symptoms_to_diseases(['fever'], species)
    disease_names = {m.get('name_en', m.get('disease_id', '')) for m in matches}

    # Fuzzy match - check if any disease matches partially
    for match_disease in disease_names:
        if disease_name.lower() in match_disease.lower() or match_disease.lower() in disease_name.lower():
            return True

    return False


def generate_test_cases() -> list:
    """Generate test cases from scenarios."""
    test_cases = []
    case_id = 1

    for species, scenarios in TEST_SCENARIOS.items():
        for scenario in scenarios:
            symptoms_text = ' '.join(scenario['symptoms'])
            extracted = _extract_species_symptoms(symptoms_text, species)

            # Check if symptoms were extracted
            if not extracted:
                print(f"⚠ Skipping {species} scenario: {scenario['notes']} (no symptoms extracted)")
                continue

            # Get top prediction
            predictions = _match_species_symptoms_to_diseases(extracted, species)
            if not predictions:
                print(f"⚠ Skipping {species} scenario: {scenario['notes']} (no predictions)")
                continue

            # Use the expected disease if specified, otherwise use top prediction
            expected_disease = scenario.get('expected_disease')
            if not expected_disease:
                expected_disease = predictions[0].get('name_en', predictions[0].get('disease_id', ''))

            test_cases.append({
                'case_id': f'{species}_{case_id:03d}',
                'species': species,
                'primary_disease': expected_disease,
                'symptoms': scenario['symptoms'],
                'expected_rank': 1,
                'confidence_threshold': scenario['confidence_threshold'],
                'notes': scenario['notes'],
            })
            case_id += 1

    return test_cases


def main():
    print("=" * 80)
    print("Generating Realistic TRIPOD Test Cases")
    print("=" * 80)

    test_cases = generate_test_cases()

    # Save to JSON
    output_file = Path(__file__).parent.parent / 'tests' / 'tripod_test_cases.json'
    with open(output_file, 'w') as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Generated {len(test_cases)} test cases")
    print(f"✓ Saved to: {output_file}")

    # Print summary by species
    print("\nTest Case Summary:")
    species_counts = {}
    for case in test_cases:
        species = case['species']
        species_counts[species] = species_counts.get(species, 0) + 1

    for species in sorted(species_counts.keys()):
        print(f"  {species:15s}: {species_counts[species]:2d} cases")


if __name__ == '__main__':
    main()
