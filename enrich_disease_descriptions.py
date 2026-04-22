#!/usr/bin/env python3
"""
Enrich veterinary disease descriptions with disease-specific content.

This script generates disease-specific descriptions for diseases that currently
have generic/template descriptions. It leverages existing fields (pathophysiology,
causes, symptoms, clinical_signs) to create more detailed descriptions.
"""

import json
import re
from typing import Dict


class DescriptionEnricher:
    """Generate disease-specific descriptions from existing fields"""

    def __init__(self):
        self.disease_keywords = self._build_disease_keywords()

    def _build_disease_keywords(self) -> Dict[str, Dict]:
        """Build disease category detection keywords"""
        return {
            "infectious_viral": {
                "keywords": [
                    "virus",
                    "viral",
                    "infection",
                    "influenza",
                    "distemper",
                    "parvovirus",
                    "coronavirus",
                    "feline",
                    "felv",
                    "fiv",
                    "herpes",
                    "calicivirus",
                    "herpesvirus",
                    "rotavirus",
                    "reovirus",
                    "paramyxovirus",
                    "togavirus",
                    "encephalitis",
                ],
                "description_template": "A {severity} viral {condition} affecting {species}. {pathophysiology_summary} {clinical_importance}",
            },
            "infectious_bacterial": {
                "keywords": [
                    "bacteria",
                    "bacterial",
                    "infection",
                    "streptococcus",
                    "staphylococcus",
                    "leptospirosis",
                    "brucellosis",
                    "pyoderma",
                    "otitis",
                    "enteritis",
                    "coli",
                    "bordetella",
                    "chlamydia",
                    "mycobacter",
                    "corynebacter",
                ],
                "description_template": "A {severity} bacterial {condition} affecting {species}. {pathophysiology_summary} Early diagnosis and appropriate antimicrobial therapy are essential.",
            },
            "parasitic": {
                "keywords": [
                    "parasite",
                    "parasitic",
                    "worm",
                    "helminth",
                    "mite",
                    "lice",
                    "tick",
                    "flea",
                    "coccidia",
                    "giardia",
                    "toxoplasma",
                    "heartworm",
                    "hookworm",
                    "tapeworm",
                    "roundworm",
                    "nematode",
                ],
                "description_template": "A {severity} parasitic {condition} affecting {species}. {pathophysiology_summary} Proper diagnosis and targeted antiparasitic therapy are critical.",
            },
            "inflammatory": {
                "keywords": [
                    "inflammation",
                    "inflammatory",
                    "dermatitis",
                    "colitis",
                    "gastritis",
                    "pancreatitis",
                    "enteritis",
                    "hepatitis",
                    "nephritis",
                    "myositis",
                    "arthritis",
                    "stomatitis",
                    "gingivitis",
                    "esophagitis",
                ],
                "description_template": "A {severity} inflammatory {condition} affecting {species}. {pathophysiology_summary} Anti-inflammatory therapy and management of underlying triggers are important.",
            },
            "neoplastic": {
                "keywords": [
                    "cancer",
                    "carcinoma",
                    "lymphoma",
                    "sarcoma",
                    "tumor",
                    "malignant",
                    "metastasis",
                    "neoplastic",
                    "leukemia",
                    "myeloma",
                ],
                "description_template": "A {severity} neoplastic {condition} affecting {species}. {pathophysiology_summary} Early detection and multimodal treatment improve outcomes.",
            },
            "metabolic": {
                "keywords": [
                    "diabetes",
                    "obesity",
                    "thyroid",
                    "metabolism",
                    "hyperthyroid",
                    "hypothyroid",
                    "electrolyte",
                    "ketoacidosis",
                    "liver",
                    "kidney",
                    "hyperparathyroid",
                    "hypoparathyroid",
                    "adrenal",
                ],
                "description_template": "A {severity} metabolic/endocrine {condition} affecting {species}. {pathophysiology_summary} Long-term management and monitoring of metabolic parameters are essential.",
            },
            "cardiovascular": {
                "keywords": [
                    "heart",
                    "cardiac",
                    "hypertension",
                    "arrhythmia",
                    "myocarditis",
                    "valve",
                    "cardiomyopathy",
                    "edema",
                    "chf",
                    "thrombosis",
                    "pericarditis",
                    "endocarditis",
                    "vasculitis",
                ],
                "description_template": "A {severity} cardiovascular {condition} affecting {species}. {pathophysiology_summary} Cardiac monitoring and appropriate medical management are essential.",
            },
            "neurological": {
                "keywords": [
                    "seizure",
                    "epilepsy",
                    "neurological",
                    "encephalitis",
                    "myelitis",
                    "stroke",
                    "paralysis",
                    "tremor",
                    "ataxia",
                    "neuropathy",
                    "meningitis",
                    "vestibular",
                    "brain",
                    "spinal",
                ],
                "description_template": "A {severity} neurological {condition} affecting {species}. {pathophysiology_summary} Supportive care and targeted therapy based on underlying etiology are critical.",
            },
            "respiratory": {
                "keywords": [
                    "asthma",
                    "bronchitis",
                    "pneumonia",
                    "respiratory",
                    "pulmonary",
                    "cough",
                    "dyspnea",
                    "laryngitis",
                    "tracheitis",
                    "rhinitis",
                    "sinusitis",
                    "pleurisy",
                    "pneumothorax",
                ],
                "description_template": "A {severity} respiratory {condition} affecting {species}. {pathophysiology_summary} Oxygen therapy and supportive care are essential during acute episodes.",
            },
            "gastrointestinal": {
                "keywords": [
                    "diarrhea",
                    "vomiting",
                    "gastroenteritis",
                    "bowel",
                    "intestinal",
                    "esophageal",
                    "gastric",
                    "ulcer",
                    "obstruction",
                    "colitis",
                    "enteritis",
                    "ileitis",
                    "cecitis",
                    "ileo-cecocolic",
                ],
                "description_template": "A {severity} gastrointestinal {condition} affecting {species}. {pathophysiology_summary} Dietary management and supportive care are important for recovery.",
            },
            "urogenital": {
                "keywords": [
                    "urinary",
                    "kidney",
                    "renal",
                    "cystitis",
                    "pyelonephritis",
                    "uti",
                    "bladder",
                    "prostate",
                    "reproductive",
                    "urolithiasis",
                    "nephritis",
                    "ureteritis",
                    "urethritis",
                ],
                "description_template": "A {severity} urogenital {condition} affecting {species}. {pathophysiology_summary} Appropriate diagnostics and management of underlying causes are essential.",
            },
            "dermatological": {
                "keywords": [
                    "skin",
                    "dermat",
                    "alopecia",
                    "pruritus",
                    "mange",
                    "ringworm",
                    "seborrhea",
                    "otitis",
                    "erythema",
                    "eczema",
                    "pustule",
                    "folliculitis",
                    "pyoderma",
                    "lichenoid",
                    "acanthosis",
                ],
                "description_template": "A {severity} dermatological {condition} affecting {species}. {pathophysiology_summary} Treatment requires identification and management of underlying causes.",
            },
            "traumatic": {
                "keywords": [
                    "trauma",
                    "traumatic",
                    "injury",
                    "fracture",
                    "laceration",
                    "wound",
                    "contusion",
                    "sprain",
                    "strain",
                    "heat stroke",
                    "burn",
                ],
                "description_template": "A {severity} traumatic {condition} affecting {species}. {pathophysiology_summary} Supportive care, pain management, and monitoring for complications are critical.",
            },
            "genetic": {
                "keywords": [
                    "genetic",
                    "hereditary",
                    "inherited",
                    "congenital",
                    "dysplasia",
                    "polycystic",
                    "lysosomial",
                    "storage",
                    "degeneration",
                ],
                "description_template": "A {severity} genetic/inherited {condition} affecting {species}. {pathophysiology_summary} Supportive care and genetic counseling are important considerations.",
            },
        }

    def _detect_disease_category(self, disease_name: str) -> str:
        """Detect disease category from name"""
        name_lower = disease_name.lower()
        for category, data in self.disease_keywords.items():
            for keyword in data["keywords"]:
                if keyword in name_lower:
                    return category
        return "infectious_viral"  # Default

    def _extract_condition_type(self, disease_name: str, pathophysiology: str = "") -> str:
        """Extract the condition type (e.g., 'infection', 'disease', 'disorder')"""
        name_lower = disease_name.lower()
        pathophysiology_lower = pathophysiology.lower()

        if any(word in name_lower or word in pathophysiology_lower for word in ["infection", "infectious"]):
            return "infection"
        elif any(
            word in name_lower or word in pathophysiology_lower for word in ["inflammation", "inflammatory", "itis"]
        ):
            return "inflammatory disorder"
        elif any(
            word in name_lower or word in pathophysiology_lower
            for word in ["cancer", "tumor", "carcinoma", "lymphoma", "sarcoma"]
        ):
            return "neoplastic disorder"
        elif any(
            word in name_lower or word in pathophysiology_lower
            for word in ["paralysis", "seizure", "encephalitis", "myelitis", "stroke"]
        ):
            return "neurological condition"
        elif any(
            word in name_lower or word in pathophysiology_lower
            for word in ["dermat", "skin", "alopecia", "mange", "ringworm"]
        ):
            return "dermatological condition"
        elif any(
            word in name_lower or word in pathophysiology_lower for word in ["arthritis", "osteoarthritis", "bone"]
        ):
            return "musculoskeletal condition"
        else:
            return "disease"

    def _assess_severity(self, disease_name: str) -> str:
        """Assess disease severity"""
        name_lower = disease_name.lower()

        if any(
            word in name_lower
            for word in ["severe", "advanced", "acute", "hemorrhagic", "septic", "acute respiratory", "fulminant"]
        ):
            return "severe"
        elif any(word in name_lower for word in ["chronic", "progressive", "resistant", "complicated", "idiopathic"]):
            return "chronic"
        else:
            return "common"

    def _extract_pathophysiology_summary(self, pathophysiology: str, disease_name: str) -> str:
        """Extract a concise summary from pathophysiology field"""
        if not pathophysiology or len(pathophysiology) < 20:
            return f"{disease_name} involves complex pathophysiological changes that require veterinary expertise to manage."

        # Take first sentence or first 150 characters
        sentences = re.split(r"[.!?]", pathophysiology)
        first_sentence = sentences[0].strip()

        if len(first_sentence) > 150:
            # Truncate to a reasonable length
            words = first_sentence.split()
            truncated = " ".join(words[:25])
            return truncated.rstrip(".,;:") + "."
        else:
            return first_sentence.rstrip(".,;:") + "." if first_sentence else ""

    def generate_description(self, disease: Dict) -> str:
        """Generate disease-specific description"""
        name = disease.get("name", "Unknown Disease")
        species = disease.get("species", "animal")
        pathophysiology = disease.get("pathophysiology", "")
        clinical_signs = disease.get("clinical_signs", "")

        # Determine severity and condition type
        severity = self._assess_severity(name)
        condition_type = self._extract_condition_type(name, pathophysiology)
        category = self._detect_disease_category(name)

        # Extract pathophysiology summary
        patho_summary = self._extract_pathophysiology_summary(pathophysiology, name)

        # Build clinical importance statement
        clinical_importance = ""
        if clinical_signs:
            signs_preview = clinical_signs[:100]
            if "respiratory" in signs_preview.lower():
                clinical_importance = "Early recognition of clinical signs is critical for timely intervention."
            elif "lethargy" in signs_preview.lower() or "appetite" in signs_preview.lower():
                clinical_importance = (
                    "Owner observation of behavioral and dietary changes is essential for early diagnosis."
                )
            else:
                clinical_importance = "Recognition of clinical manifestations enables prompt veterinary intervention."
        else:
            clinical_importance = "Early diagnosis and treatment significantly improve outcomes."

        # Use category template
        template = self.disease_keywords[category]["description_template"]

        description = template.format(
            severity=severity,
            condition=condition_type,
            species=species,
            pathophysiology_summary=patho_summary,
            clinical_importance=clinical_importance,
        )

        return description

    def enrich_diseases(self, input_file: str, output_file: str) -> Dict[str, int]:
        """Enrich diseases with specific descriptions"""
        print(f"Loading data from {input_file}...")
        with open(input_file, "r", encoding="utf-8") as f:
            diseases = json.load(f)

        # Identify diseases with generic descriptions
        generic_patterns = [
            "involves dysfunction of metabolic processes",
            "involves inflammation of specific tissues or organ systems",
            "involving dysfunction of the nervous system",
            "involving dysfunction of the cardiovascular system",
            "involving impairment of the musculoskeletal system",
            "involves disruption of integumentary integrity",
            "involves dysfunction of the respiratory system",
            "involves disruption of normal gastrointestinal",
        ]

        updated_count = 0
        skipped_count = 0

        print(f"Processing {len(diseases)} disease records...")

        for i, disease in enumerate(diseases):
            if (i + 1) % 500 == 0:
                print(f"  Progress: {i + 1}/{len(diseases)}")

            description = disease.get("description", "")

            # Check if this disease has a generic description
            if any(pattern in description for pattern in generic_patterns):
                new_description = self.generate_description(disease)
                disease["description"] = new_description

                # Generate Japanese version
                disease["description_ja"] = self._translate_description(disease, new_description)

                updated_count += 1

        print(f"\nSaving {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(diseases, f, ensure_ascii=False, indent=2)

        return {"total": len(diseases), "updated": updated_count, "skipped": skipped_count}

    def _translate_description(self, disease: Dict, english_desc: str) -> str:
        """Generate Japanese translation of description"""
        name = disease.get("name", "")
        species = disease.get("species", "")
        category = self._detect_disease_category(name)

        # Build a Japanese description
        category_ja = {
            "infectious_viral": "ウイルス感染症",
            "infectious_bacterial": "細菌感染症",
            "parasitic": "寄生虫感染症",
            "inflammatory": "炎症性疾患",
            "neoplastic": "腫瘍性疾患",
            "metabolic": "代謝内分泌疾患",
            "cardiovascular": "心血管疾患",
            "neurological": "神経疾患",
            "respiratory": "呼吸器疾患",
            "gastrointestinal": "消化器疾患",
            "urogenital": "泌尿生殖器疾患",
            "dermatological": "皮膚疾患",
            "traumatic": "外傷性疾患",
            "genetic": "遺伝性疾患",
        }.get(category, "疾患")

        desc_ja = f"{name}は{species}に影響を与える{category_ja}です。"
        desc_ja += "早期診断と適切な獣医学的管理が重要です。"

        return desc_ja


def main():
    """Main entry point"""
    input_file = "/home/user/vetdict/diseases_all_species.json"
    output_file = "/home/user/vetdict/diseases_all_species_desc_enriched.json"

    enricher = DescriptionEnricher()

    print("=" * 70)
    print("Disease Description Enrichment - Replace Generic Descriptions")
    print("=" * 70)

    results = enricher.enrich_diseases(input_file, output_file)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total records:           {results['total']}")
    print(f"Descriptions updated:    {results['updated']}")
    print(f"Records skipped:         {results['skipped']}")
    print(f"Output file:             {output_file}")
    print("=" * 70)

    # Show a few examples
    print("\nEXAMPLES OF UPDATED DESCRIPTIONS:")
    print("-" * 70)

    with open(output_file, "r", encoding="utf-8") as f:
        updated_diseases = json.load(f)

    # Find and display examples
    shown = 0
    for disease in updated_diseases:
        original = disease.get("description", "")
        if any(
            pattern in original
            for pattern in [
                "involves dysfunction of metabolic processes",
                "involves inflammation of specific tissues",
                "involving dysfunction of the nervous system",
            ]
        ):
            print(f"\nDisease: {disease['name']} ({disease['species']})")
            print(f"New description:\n  {original[:200]}...")
            shown += 1
            if shown >= 5:
                break


if __name__ == "__main__":
    main()
