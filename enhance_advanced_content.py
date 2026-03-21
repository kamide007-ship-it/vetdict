#!/usr/bin/env python3
"""
Advanced enhancement of veterinary disease content.

This script performs second-pass enrichment:
1. Generate symptoms from clinical_signs
2. Add medication-specific dosing information
3. Enhance diagnostic criteria
4. Add differential diagnosis
5. Reduce generic phrase repetition
"""

import json
import re
from typing import Dict, List, Optional, Set
from collections import defaultdict


class AdvancedEnhancer:
    """Advanced disease content enhancement"""

    def __init__(self):
        self.medication_db = self._build_medication_database()
        self.differential_templates = self._build_differential_templates()

    def _build_medication_database(self) -> Dict[str, Dict]:
        """Build database of common veterinary medications"""
        return {
            # Antibiotics
            'amoxicillin': {'dosage': '20-40 mg/kg BID-TID', 'category': 'antibiotic'},
            'amoxicillin-clavulanate': {'dosage': '20-40 mg/kg BID', 'category': 'antibiotic'},
            'enrofloxacin': {'dosage': '5-20 mg/kg once daily', 'category': 'antibiotic'},
            'fluoroquinolone': {'dosage': '5-20 mg/kg daily', 'category': 'antibiotic'},
            'cephalosporin': {'dosage': '20-40 mg/kg daily', 'category': 'antibiotic'},
            'tetracycline': {'dosage': '20-40 mg/kg BID-TID', 'category': 'antibiotic'},
            'doxycycline': {'dosage': '5-10 mg/kg BID', 'category': 'antibiotic'},

            # Antivirals
            'acyclovir': {'dosage': '15 mg/kg TID', 'category': 'antiviral'},

            # Antifungals
            'fluconazole': {'dosage': '2.5-5 mg/kg daily', 'category': 'antifungal'},
            'terbinafine': {'dosage': '10-40 mg/kg daily', 'category': 'antifungal'},

            # Antiparasitics
            'ivermectin': {'dosage': '0.2-0.4 mg/kg', 'category': 'antiparasitic'},
            'selamectin': {'dosage': 'topical monthly', 'category': 'antiparasitic'},
            'fenbendazole': {'dosage': '50 mg/kg daily', 'category': 'antiparasitic'},
            'praziquantel': {'dosage': '5-10 mg/kg', 'category': 'antiparasitic'},

            # Corticosteroids
            'prednisone': {'dosage': '0.5-2 mg/kg BID', 'category': 'corticosteroid'},
            'prednisolone': {'dosage': '0.5-2 mg/kg BID', 'category': 'corticosteroid'},
            'dexamethasone': {'dosage': '0.1-0.5 mg/kg daily', 'category': 'corticosteroid'},

            # NSAIDs
            'carprofen': {'dosage': '4.4 mg/kg BID', 'category': 'nsaid'},
            'meloxicam': {'dosage': '0.1-0.2 mg/kg daily', 'category': 'nsaid'},
            'ketoprofen': {'dosage': '2 mg/kg TID', 'category': 'nsaid'},

            # Cardiac medications
            'enalapril': {'dosage': '0.5 mg/kg BID', 'category': 'cardiac'},
            'furosemide': {'dosage': '2-4 mg/kg daily', 'category': 'cardiac'},
            'pimobendan': {'dosage': '0.25 mg/kg BID', 'category': 'cardiac'},

            # GI medications
            'metoclopramide': {'dosage': '0.25-0.5 mg/kg TID', 'category': 'antiemetic'},
            'maropitant': {'dosage': '1 mg/kg daily', 'category': 'antiemetic'},
            'famotidine': {'dosage': '0.5-1 mg/kg BID', 'category': 'protectant'},
            'sucralfate': {'dosage': '250 mg per animal BID-TID', 'category': 'protectant'},

            # Seizure medications
            'phenobarbital': {'dosage': '2-6 mg/kg BID', 'category': 'anticonvulsant'},
            'levetiracetam': {'dosage': '10-20 mg/kg TID', 'category': 'anticonvulsant'},
            'zonisamide': {'dosage': '5-10 mg/kg BID', 'category': 'anticonvulsant'},

            # Insulin
            'insulin': {'dosage': '0.5-1.5 units/kg BID', 'category': 'metabolic'},

            # Thyroid
            'levothyroxine': {'dosage': '20 mcg/kg BID', 'category': 'thyroid'},
            'methimazole': {'dosage': '2.5-5 mg/cat BID', 'category': 'thyroid'},
        }

    def _build_differential_templates(self) -> Dict[str, List[str]]:
        """Build differential diagnosis templates by category"""
        return {
            'respiratory': [
                'Consider feline asthma, pneumonia, pleural effusion, and airway obstruction.',
                'Differential diagnosis includes upper respiratory infection, lower airway disease, and cardiac disease.',
                'Rule out infectious causes (viral, bacterial, fungal) and non-infectious causes (allergic, traumatic).',
            ],
            'gastrointestinal': [
                'Consider dietary indiscretion, food intolerance, infectious enteritis, and obstruction.',
                'Differential diagnosis includes inflammatory bowel disease, neoplasia, and parasitism.',
                'Rule out dietary causes, infectious agents, and mechanical obstruction.',
            ],
            'neurological': [
                'Consider central versus peripheral nervous system involvement.',
                'Differential diagnosis includes infectious, metabolic, neoplastic, and idiopathic etiologies.',
                'Rule out trauma, toxins, and metabolic disorders.',
            ],
            'dermatological': [
                'Consider parasitic, allergic, infectious, and autoimmune etiologies.',
                'Differential diagnosis includes mange, ringworm, bacterial pyoderma, and allergic dermatitis.',
                'Rule out secondary infections and nutritional deficiencies.',
            ],
            'cardiovascular': [
                'Consider primary cardiac disease versus systemic causes.',
                'Differential diagnosis includes cardiomyopathy, valve disease, and arrhythmia.',
                'Rule out secondary causes and systemic disease.',
            ],
            'urogenital': [
                'Consider urinary tract infection, obstruction, and systemic disease.',
                'Differential diagnosis includes stone formation, neoplasia, and infectious disease.',
                'Rule out behavioral and anatomical causes.',
            ],
            'metabolic': [
                'Consider primary metabolic disorder versus secondary changes.',
                'Differential diagnosis includes endocrine disease, nutritional deficiency, and organ dysfunction.',
                'Rule out iatrogenic causes and secondary metabolic derangements.',
            ],
        }

    def _extract_symptoms_from_clinical_signs(self, clinical_signs: str) -> Set[str]:
        """Extract symptom keywords from clinical_signs field"""
        clinical_signs_lower = clinical_signs.lower()

        # Common symptom keywords
        symptom_keywords = {
            'lethargy', 'fatigue', 'weakness', 'depression',
            'appetite_loss', 'anorexia', 'decreased appetite',
            'vomiting', 'diarrhea', 'constipation',
            'fever', 'elevated temperature',
            'coughing', 'cough', 'sneezing', 'nasal discharge',
            'labored breathing', 'dyspnea', 'respiratory distress',
            'exercise intolerance', 'activity loss',
            'weight loss', 'weight gain', 'obesity',
            'behavior change', 'behavioral changes', 'aggression',
            'polyuria', 'polydipsia', 'increased urination', 'increased thirst',
            'icterus', 'jaundice', 'pale mucous', 'cyanosis',
            'bleeding', 'hemorrhage', 'bruising',
            'seizure', 'tremor', 'ataxia', 'paralysis',
            'pain', 'lameness', 'limping', 'stiffness',
            'itching', 'pruritus', 'scratching',
            'hair loss', 'alopecia', 'coat changes',
            'skin lesion', 'pustule', 'ulcer', 'scab',
            'swelling', 'edema', 'lymphadenopathy',
            'discharge', 'ocular discharge', 'nasal discharge',
            'odor', 'foul smell', 'bad breath',
            'dehydration', 'sunken eyes',
            'pale gums', 'white gums', 'cyanotic gums',
            'rapid heartbeat', 'tachycardia', 'arrhythmia',
            'abdominal pain', 'abdominal distension', 'bloating',
            'difficulty urinating', 'dysuria', 'straining',
            'difficulty defecating', 'tenesmus',
        }

        symptoms = set()
        for keyword in symptom_keywords:
            if keyword in clinical_signs_lower:
                # Normalize to underscore format
                normalized = keyword.replace(' ', '_')
                symptoms.add(normalized)

        return symptoms

    def _generate_differential_diagnosis(self, disease_name: str, description: str) -> str:
        """Generate differential diagnosis section"""
        disease_lower = disease_name.lower()
        desc_lower = description.lower()

        # Categorize disease
        category = 'metabolic'  # default

        if any(word in disease_lower or word in desc_lower
               for word in ['respiratory', 'cough', 'asthma', 'pneumonia', 'bronch']):
            category = 'respiratory'
        elif any(word in disease_lower or word in desc_lower
                 for word in ['gastrointestinal', 'diarrhea', 'vomiting', 'enteritis', 'colitis']):
            category = 'gastrointestinal'
        elif any(word in disease_lower or word in desc_lower
                 for word in ['neurological', 'seizure', 'paralysis', 'encephalitis', 'stroke']):
            category = 'neurological'
        elif any(word in disease_lower or word in desc_lower
                 for word in ['dermat', 'skin', 'alopecia', 'mange', 'ringworm']):
            category = 'dermatological'
        elif any(word in disease_lower or word in desc_lower
                 for word in ['cardiac', 'heart', 'cardiomyopathy', 'valve']):
            category = 'cardiovascular'
        elif any(word in disease_lower or word in desc_lower
                 for word in ['urinary', 'kidney', 'cystitis', 'urolithiasis']):
            category = 'urogenital'

        templates = self.differential_templates.get(category, [])
        if not templates:
            return "Rule out alternative diagnoses and consider underlying causes."

        # Select template based on hash for consistency
        template = templates[hash(disease_name) % len(templates)]
        return template

    def _enhance_with_medications(self, treatment: str, disease_name: str) -> str:
        """Enhance treatment with specific medication information"""
        enhanced = treatment

        # Find medication mentions in treatment
        for med_name, med_info in self.medication_db.items():
            pattern = re.compile(f'\\b{med_name}\\b', re.IGNORECASE)
            if pattern.search(treatment):
                # Add dosage information if not already present
                if med_info['dosage'] not in treatment:
                    enhanced = pattern.sub(
                        f'{med_name} ({med_info["dosage"]})',
                        enhanced
                    )

        return enhanced

    def enhance_advanced(self, input_file: str, output_file: str) -> Dict:
        """Perform advanced enrichment"""
        print(f"Loading data from {input_file}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            diseases = json.load(f)

        symptoms_added = 0
        differentials_added = 0
        medications_enhanced = 0
        early_diagnosis_reduced = 0

        print(f"Processing {len(diseases)} disease records...")

        for i, disease in enumerate(diseases):
            if (i + 1) % 500 == 0:
                print(f"  Progress: {i + 1}/{len(diseases)}")

            # 1. Generate symptoms from clinical_signs
            clinical_signs = disease.get('clinical_signs', '')
            if clinical_signs and not disease.get('symptoms'):
                extracted_symptoms = self._extract_symptoms_from_clinical_signs(clinical_signs)
                if extracted_symptoms:
                    disease['symptoms'] = sorted(list(extracted_symptoms))  # Convert set to sorted list
                    symptoms_added += 1

            # 2. Add differential diagnosis if not present
            if not disease.get('differential_diagnosis'):
                disease_name = disease.get('name', '')
                description = disease.get('description', '')
                diff_diag = self._generate_differential_diagnosis(disease_name, description)
                disease['differential_diagnosis'] = diff_diag
                differentials_added += 1

            # 3. Enhance treatment with medication information
            treatment = disease.get('treatment', '')
            if treatment:
                enhanced_treatment = self._enhance_with_medications(treatment, disease['name'])
                if enhanced_treatment != treatment:
                    disease['treatment'] = enhanced_treatment
                    medications_enhanced += 1

            # 4. Reduce "early diagnosis" repetition in prognosis
            prognosis = disease.get('prognosis', '')
            if 'early diagnosis' in prognosis.lower():
                # Only keep one instance
                if prognosis.count('early diagnosis') > 1 or prognosis.count('Early diagnosis') > 1:
                    # Remove redundant mentions
                    prognosis = re.sub(r'(?i)\s*[,.]?\s*early diagnosis[^.]*\.?\s*', ' ', prognosis)
                    disease['prognosis'] = prognosis.strip()
                    early_diagnosis_reduced += 1

        print(f"\nSaving {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(diseases, f, ensure_ascii=False, indent=2)

        return {
            'total': len(diseases),
            'symptoms_added': symptoms_added,
            'differentials_added': differentials_added,
            'medications_enhanced': medications_enhanced,
            'early_diagnosis_reduced': early_diagnosis_reduced,
        }


def main():
    """Main entry point"""
    input_file = '/home/user/vetdict/diseases_all_species.json'
    output_file = '/home/user/vetdict/diseases_all_species_advanced.json'

    enhancer = AdvancedEnhancer()

    print("=" * 70)
    print("Advanced Disease Content Enhancement")
    print("=" * 70)

    results = enhancer.enhance_advanced(input_file, output_file)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total records:                {results['total']}")
    print(f"Symptoms fields added:        {results['symptoms_added']}")
    print(f"Differential diagnoses added: {results['differentials_added']}")
    print(f"Treatment medications enhanced: {results['medications_enhanced']}")
    print(f"Early diagnosis mentions reduced: {results['early_diagnosis_reduced']}")
    print("=" * 70)


if __name__ == '__main__':
    main()
