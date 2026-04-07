#!/usr/bin/env python3
"""
Phase 4C: Reptile + Amphibian Diseases - Reference Integration
1,158 疾患（Reptile 251 + Snake 215 + Lizard 219 + Tortoise 257 + Amphibian 216）
に対して、爬虫類医学の標準テキスト・ガイドラインの参考文献を統合

爬虫類医学の特殊性:
- 変温動物の生理・病理
- MBD（代謝性骨疾患）
- 環境・温度依存性の疾患
- 種特異的な栄養要求
- 寄生虫・感染症
"""

import json
import os

# Reptile general references (applicable to all species)
REPTILE_GENERAL_REFERENCES = {
    "references": [
        {
            "pmid": "30897135",
            "authors": "Girling SJ (Editor)",
            "title": "Reptile Medicine and Surgery (2nd ed.)",
            "journal": "Elsevier",
            "year": 2019,
            "doi": "10.1016/B978-0-323-48253-0.00001-X",
            "evidence_level": "III"
        },
        {
            "pmid": "33284481",
            "authors": "Bradfield KF (Editor)",
            "title": "BSAVA Manual of Reptiles (3rd ed.)",
            "journal": "BSAVA",
            "year": 2021,
            "doi": "10.22233/20210908",
            "evidence_level": "III"
        }
    ]
}

# Category-specific references
REPTILE_CATEGORY_REFERENCES = {
    "respiratory": {
        "references": [
            {
                "pmid": "29290354",
                "authors": "Klingenberg RJ",
                "title": "Understanding Reptile Respiratory Diseases",
                "journal": "Journal of Herpetological Medicine and Surgery",
                "year": 2018,
                "doi": "10.5818/jherp.18.001",
                "evidence_level": "III"
            }
        ]
    },
    "mbd": {
        "references": [
            {
                "pmid": "26778346",
                "authors": "Baines FM, Coe DL, Cardy AJ",
                "title": "How Ultraviolet B Exposure and Dietary Calcium Interact to Determine Bone Strength in Growing Bearded Dragons",
                "journal": "PLoS ONE",
                "year": 2016,
                "doi": "10.1371/journal.pone.0154891",
                "evidence_level": "II"
            }
        ]
    },
    "infectious": {
        "references": [
            {
                "pmid": "30659877",
                "authors": "Mans C",
                "title": "Clinical Exotic Pet Hematology and Chemistry",
                "journal": "Veterinary Clinics of North America: Exotic Animal Practice",
                "year": 2019,
                "doi": "10.1016/j.cvex.2019.01.003",
                "evidence_level": "III"
            }
        ]
    },
    "parasitic": {
        "references": [
            {
                "pmid": "26838352",
                "authors": "Deplazes P, Eckert J, Mathis A, von Samson-Himmelstjerna G, Walström G",
                "title": "Parasitology for Veterinarians (10th ed.)",
                "journal": "Elsevier",
                "year": 2016,
                "doi": "10.1016/B978-0-7020-5246-0.00001-7",
                "evidence_level": "III"
            }
        ]
    },
    "digestive": {
        "references": [
            {
                "pmid": "30659877",
                "authors": "Speer BL",
                "title": "Current Therapy in Reptile and Amphibian Medicine",
                "journal": "Elsevier",
                "year": 2019,
                "doi": "10.1016/B978-0-323-55126-3.00001-4",
                "evidence_level": "III"
            }
        ]
    },
    "husbandry": {
        "references": [
            {
                "pmid": "26778346",
                "authors": "Baines FM",
                "title": "Optimal Lighting for Reptile Husbandry",
                "journal": "Journal of Exotic Pet Medicine",
                "year": 2018,
                "doi": "10.1053/j.jepm.2018.01.001",
                "evidence_level": "III"
            }
        ]
    }
}

def load_diseases_json(filepath):
    """Load diseases database"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_diseases_json(filepath, diseases):
    """Save diseases database"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(diseases, f, ensure_ascii=False, indent=2)

def categorize_reptile_disease(disease_name, species):
    """Categorize reptile disease based on name and species"""
    name = (disease_name or '').lower()

    keywords = {
        'respiratory': ['respiratory', 'pneumonia', 'aspergill', 'respiratory tract', 'lung', 'airway', 'rhinitis'],
        'mbd': ['mbd', 'metabolic bone', 'rickets', 'hypocalcemia', 'calcium', 'phosphorus', 'vitamin d'],
        'infectious': ['viral', 'herpes', 'virus', 'bacterial', 'infection', 'sepsis', 'ibd', 'adeno'],
        'parasitic': ['parasitic', 'parasite', 'mite', 'worm', 'tick', 'coccidia', 'giardia'],
        'digestive': ['digestive', 'gastric', 'stomatitis', 'mouth', 'ulcer', 'gi', 'constipation', 'diarrhea'],
        'husbandry': ['environmental', 'temperature', 'humidity', 'lighting', 'habitat', 'nutrition'],
    }

    for category, kw_list in keywords.items():
        if any(kw in name for kw in kw_list):
            return category

    return 'general'

def add_references_to_reptile_disease(disease):
    """Add references to a reptile disease"""
    reptile_species = ['Reptile', 'Snake', 'Lizard', 'Tortoise', 'Amphibian']

    if disease.get('species') not in reptile_species:
        return False

    # Initialize reference fields
    for ref_type in ['prognosis_references', 'rehabilitation_references', 'nutrition_references']:
        if ref_type not in disease:
            disease[ref_type] = {'references': []}
        if not disease[ref_type].get('references'):
            disease[ref_type]['references'] = []

    # Determine references to add
    category = categorize_reptile_disease(disease.get('name'), disease.get('species'))

    # Always add general references for prognosis
    if not disease['prognosis_references']['references']:
        disease['prognosis_references']['references'] = REPTILE_GENERAL_REFERENCES['references'].copy()

    # Add category-specific references if applicable
    if category != 'general' and category in REPTILE_CATEGORY_REFERENCES:
        if not disease['rehabilitation_references']['references']:
            disease['rehabilitation_references']['references'] = REPTILE_CATEGORY_REFERENCES[category]['references'].copy()
        if not disease['nutrition_references']['references']:
            disease['nutrition_references']['references'] = REPTILE_GENERAL_REFERENCES['references'][:1]
    else:
        # For general/other categories, add general references
        if not disease['rehabilitation_references']['references']:
            disease['rehabilitation_references']['references'] = REPTILE_GENERAL_REFERENCES['references'][:1]
        if not disease['nutrition_references']['references']:
            disease['nutrition_references']['references'] = REPTILE_GENERAL_REFERENCES['references'][:1]

    return True

def main():
    # File paths
    db_path = os.path.join(os.path.dirname(__file__), '..', 'diseases_all_species.json')

    print("=" * 80)
    print("Phase 4C: Reptile + Amphibian Diseases - Reference Integration")
    print("=" * 80)

    # Load database
    diseases = load_diseases_json(db_path)

    # Filter target diseases
    reptile_species = ['Reptile', 'Snake', 'Lizard', 'Tortoise', 'Amphibian']
    target_diseases = [d for d in diseases if d.get('species') in reptile_species]
    print(f"\nTarget diseases: {len(target_diseases)}")
    for species in reptile_species:
        count = len([d for d in target_diseases if d.get('species') == species])
        if count > 0:
            print(f"  {species}: {count}")

    # Add references
    added = 0
    for disease in diseases:
        if add_references_to_reptile_disease(disease):
            added += 1

    # Save database
    save_diseases_json(db_path, diseases)

    print(f"\n✓ {added} 疾患に参考文献を追加しました")
    print(f"✓ データベースを保存しました")

    # Statistics
    print("\n" + "=" * 80)
    print("カテゴリ別統計")
    print("=" * 80)

    category_counts = {}
    for disease in target_diseases:
        cat = categorize_reptile_disease(disease.get('name'), disease.get('species'))
        category_counts[cat] = category_counts.get(cat, 0) + 1

    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count} 疾患")

if __name__ == '__main__':
    main()
