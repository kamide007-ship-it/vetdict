#!/usr/bin/env python3
"""Migrate existing disease/drug/symptom data from Python modules and JSON into SQLite.

Usage:
    python scripts/migrate_to_sqlite.py [--db-path PATH]

Default DB path: instance/vetdict.db
"""

import hashlib
import importlib
import json
import random
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from api.database import DB_PATH, get_connection, init_db, upsert_disease, upsert_drug, upsert_symptom

# ---------------------------------------------------------------------------
# Species module mapping: species_key → module path
# ---------------------------------------------------------------------------
SPECIES_MODULES = {
    "cat": "api.species.cat_diseases",
    "rabbit": "api.species.rabbit_diseases",
    "bird": "api.species.bird_diseases",
    "hamster": "api.species.hamster_diseases",
    "guinea_pig": "api.species.guinea_pig_diseases",
    "ferret": "api.species.ferret_diseases",
    "hedgehog": "api.species.hedgehog_diseases",
    "chinchilla": "api.species.chinchilla_diseases",
    "reptile": "api.species.reptile_diseases",
    "snake": "api.species.snake_diseases",
    "lizard": "api.species.lizard_diseases",
    "tortoise": "api.species.tortoise_diseases",
    "parakeet": "api.species.parakeet_diseases",
    "parrot": "api.species.parrot_diseases",
    "amphibian": "api.species.amphibian_diseases",
    "fish": "api.species.fish_diseases",
    "degu": "api.species.degu_diseases",
    "sugar_glider": "api.species.sugar_glider_diseases",
    "exotic_other": "api.species.exotic_other_diseases",
}

# Dog uses dedicated species module (same structure as other species)
DOG_MODULE = "api.species.dog_diseases"
DOG_DISEASES_VAR = "DISEASES"
DOG_SYMPTOMS_VAR = "SYMPTOM_NAMES"


def _load_module(module_path: str):
    return importlib.import_module(module_path)


def migrate_species_diseases(conn, species_key: str, module_path: str) -> int:
    """Load DISEASES from a species module and insert into SQLite. Returns count."""
    mod = _load_module(module_path)
    diseases = getattr(mod, "DISEASES", [])
    count = 0

    # Helper to extract ja/en from dict fields
    def _extract_ja_en(field_val):
        if isinstance(field_val, dict):
            return field_val.get("ja"), field_val.get("en")
        return None, field_val

    for i, d in enumerate(diseases):
        disease_id = d.get("id") or f"{species_key}_{i:04d}"

        # Extract ja/en from fields that might be dicts
        treatment_ja, treatment_en = _extract_ja_en(d.get("treatment"))
        prevention_ja, prevention_en = _extract_ja_en(d.get("prevention"))
        prognosis_ja, prognosis_en = _extract_ja_en(d.get("prognosis"))

        record = {
            "id": disease_id,
            "species": species_key,
            "name": d.get("name", ""),
            "name_ja": d.get("name_ja", d.get("name", "")),
            "description": d.get("description"),
            "description_ja": d.get("description_ja"),
            "pathophysiology": d.get("pathophysiology"),
            "pathophysiology_ja": d.get("pathophysiology_ja"),
            "causes": d.get("causes"),
            "causes_ja": d.get("causes_ja"),
            "treatment": treatment_en or d.get("treatment"),
            "treatment_ja": treatment_ja or d.get("treatment_ja"),
            "prevention": prevention_en or d.get("prevention"),
            "prevention_ja": prevention_ja or d.get("prevention_ja"),
            "prognosis": prognosis_en or d.get("prognosis"),
            "prognosis_ja": prognosis_ja or d.get("prognosis_ja"),
            "urgency": d.get("urgency"),
            "symptoms": d.get("symptoms", set()),
            "recommended_tests": d.get("recommended_tests", []),
            "onset_pattern": d.get("onset_pattern"),
            "age_predisposition": d.get("age_predisposition"),
            "diagnosis": d.get("diagnosis"),
            "diagnosis_ja": d.get("diagnosis_ja"),
            "clinical_signs": d.get("clinical_signs"),
            "clinical_signs_ja": d.get("clinical_signs_ja"),
            "transmission": d.get("transmission"),
            "transmission_ja": d.get("transmission_ja"),
            "differential_diagnosis": d.get("differential_diagnosis"),
        }
        upsert_disease(conn, record)
        count += 1
    return count


def migrate_species_symptoms(conn, species_key: str, module_path: str) -> int:
    """Load SYMPTOM_NAMES from a species module and insert into SQLite."""
    mod = _load_module(module_path)
    symptom_names = getattr(mod, "SYMPTOM_NAMES", {})
    count = 0
    for sid, names in symptom_names.items():
        upsert_symptom(
            conn,
            symptom_id=f"{species_key}_{sid}",
            name_en=names.get("en", sid),
            name_ja=names.get("ja", sid),
            species=species_key,
        )
        count += 1
    return count


def migrate_dog_diseases(conn) -> int:
    """Migrate dog diseases from symptom_checker module."""
    mod = _load_module(DOG_MODULE)
    diseases = getattr(mod, DOG_DISEASES_VAR, [])
    count = 0
    for i, d in enumerate(diseases):
        disease_id = d.get("id") or f"dog_{i:04d}"

        # Handle fields that might be dict with 'ja'/'en' keys
        def _extract_ja_en(field_val):
            if isinstance(field_val, dict):
                return field_val.get("ja"), field_val.get("en")
            return None, field_val

        treatment_ja, treatment_en = _extract_ja_en(d.get("treatment"))
        prevention_ja, prevention_en = _extract_ja_en(d.get("prevention"))
        prognosis_ja, prognosis_en = _extract_ja_en(d.get("prognosis"))

        record = {
            "id": disease_id,
            "species": "dog",
            "name": d.get("name", ""),
            "name_ja": d.get("name_ja", d.get("name", "")),
            "description": d.get("description"),
            "description_ja": d.get("description_ja"),
            "pathophysiology": d.get("pathophysiology"),
            "pathophysiology_ja": d.get("pathophysiology_ja"),
            "causes": d.get("causes"),
            "causes_ja": d.get("causes_ja"),
            "treatment": treatment_en or d.get("treatment"),
            "treatment_ja": treatment_ja or d.get("treatment_ja"),
            "prevention": prevention_en or d.get("prevention"),
            "prevention_ja": prevention_ja or d.get("prevention_ja"),
            "prognosis": prognosis_en or d.get("prognosis"),
            "prognosis_ja": prognosis_ja or d.get("prognosis_ja"),
            "urgency": d.get("urgency"),
            "symptoms": d.get("symptoms", set()),
            "recommended_tests": d.get("recommended_tests", []),
            "onset_pattern": d.get("onset_pattern"),
            "age_predisposition": d.get("age_predisposition"),
            "diagnosis": d.get("diagnosis"),
            "diagnosis_ja": d.get("diagnosis_ja"),
            "clinical_signs": d.get("clinical_signs"),
            "clinical_signs_ja": d.get("clinical_signs_ja"),
            "transmission": d.get("transmission"),
            "transmission_ja": d.get("transmission_ja"),
            "differential_diagnosis": d.get("differential_diagnosis"),
        }
        upsert_disease(conn, record)
        count += 1

    symptom_names = getattr(mod, DOG_SYMPTOMS_VAR, {})
    for sid, names in symptom_names.items():
        upsert_symptom(conn, f"dog_{sid}", names.get("en", sid), names.get("ja", sid), "dog")

    return count


def _is_template_text(value: str | None) -> bool:
    """Return True if *value* is low-quality template text from enrichment."""
    if not value:
        return False
    # Generic "affects species" description template
    if "に影響する疾患です。専門的な獣医学的診断と治療が必要です" in value:
        return True
    # Generic prognosis template
    if "予後は良好です。早期発見と適切な治療により、ほとんどの動物は回復します" in value:
        return True
    # Causes that just say "affects species"
    if "に影響を及ぼす疾患である" in value:
        return True
    return False


def migrate_json_enrichments(conn) -> int:
    """Overlay enrichment data from diseases_all_species.json using name-based matching.

    The JSON enrichment file uses different IDs and ordering than the Python
    modules.  Previous ID-based matching caused 1,342 records to receive
    enrichment data from the *wrong* disease.  This version matches by
    normalised disease name so only genuinely matching records are updated.

    Template text (generic descriptions/prognoses from the enrichment
    pipeline) is filtered out so it does not overwrite better data from
    the Python species modules.
    """
    json_path = ROOT / "diseases_all_species.json"
    if not json_path.exists():
        print(f"  [skip] {json_path} not found")
        return 0

    with open(json_path, encoding="utf-8") as f:
        entries = json.load(f)

    # Build lookups keyed on (species, normalised name) so we cannot pull a
    # different species' enrichment onto the wrong row. Cat hyperthyroidism
    # was previously being overwritten by reptile hyperthyroidism because the
    # lookup ignored species.
    import re

    def _norm(name: str) -> str:
        return re.sub(r"\s+", " ", name.strip().lower())

    # JSON file uses capitalized / space-separated species names — normalize
    # to the lowercase / underscore form used by the Python species modules.
    _JSON_SPECIES_TO_DB = {
        "Bird": "bird",
        "Parakeet": "parakeet",
        "Parrot": "parrot",
        "Horse": "horse",
        "Guinea Pig": "guinea_pig",
        "Rabbit": "rabbit",
        "Chinchilla": "chinchilla",
        "Hedgehog": "hedgehog",
        "Snake": "snake",
        "Lizard": "lizard",
        "Amphibian": "amphibian",
        "Sugar Glider": "sugar_glider",
        "Degu": "degu",
        "Reptile": "reptile",
        "Exotic Other": "exotic_other",
        "Hamster": "hamster",
        "Ferret": "ferret",
        "Tortoise": "tortoise",
        "Fish": "fish",
        "Cat": "cat",
        "Dog": "dog",
    }

    json_by_species_name: dict[tuple[str, str], dict] = {}
    json_by_name_multi: dict[str, dict] = {}  # cross-species ("Multiple") fallback
    for entry in entries:
        name = entry.get("name", "")
        if not name:
            continue
        sp_raw = entry.get("species", "")
        sp_db = _JSON_SPECIES_TO_DB.get(sp_raw, sp_raw.lower())
        json_by_species_name[(sp_db, _norm(name))] = entry
        if sp_raw == "Multiple":
            json_by_name_multi[_norm(name)] = entry

    def _clean(value: str | None) -> str | None:
        """Return None for template text so COALESCE keeps existing data."""
        if _is_template_text(value):
            return None
        return value

    # Iterate over all diseases currently in SQLite and enrich where names match.
    rows = conn.execute("SELECT id, species, name FROM diseases").fetchall()
    count = 0

    def _extract_ja_en(field_val):
        if isinstance(field_val, dict):
            return field_val.get("ja"), field_val.get("en")
        # If it's a list, convert to JSON string
        if isinstance(field_val, list):
            return None, json.dumps(field_val, ensure_ascii=False) if field_val else None
        return None, field_val

    def _to_json_str(field_val):
        if isinstance(field_val, dict):
            return json.dumps(field_val, ensure_ascii=False)
        # If it's already a list, convert to JSON
        if isinstance(field_val, list):
            return json.dumps(field_val, ensure_ascii=False) if field_val else None
        return field_val

    def _ensure_string_or_none(val):
        """Convert lists to JSON strings, keep strings as-is, return None for empty."""
        if val is None:
            return None
        if isinstance(val, list):
            return json.dumps(val, ensure_ascii=False) if val else None
        return val

    for row in rows:
        db_id, db_species, db_name = row["id"], row["species"], row["name"]
        # First try species-specific match — this prevents reptile content
        # from being applied to a cat row (and vice versa).
        entry = json_by_species_name.get((db_species, _norm(db_name)))
        if not entry:
            # Fall back to cross-species "Multiple" entries when present.
            entry = json_by_name_multi.get(_norm(db_name))
        if not entry:
            continue

        # Handle fields that might be dict with 'ja'/'en' keys
        treatment_ja, treatment_en = _extract_ja_en(entry.get("treatment"))
        prevention_ja, prevention_en = _extract_ja_en(entry.get("prevention"))
        prognosis_ja, prognosis_en = _extract_ja_en(entry.get("prognosis"))

        # Convert dict reference fields to JSON strings
        prognosis_refs = _to_json_str(entry.get("prognosis_references"))
        rehab_refs = _to_json_str(entry.get("rehabilitation_references"))
        nutrition_refs = _to_json_str(entry.get("nutrition_references"))

        conn.execute(
            """UPDATE diseases SET
                description = COALESCE(?, description),
                description_ja = COALESCE(?, description_ja),
                pathophysiology = COALESCE(?, pathophysiology),
                pathophysiology_ja = COALESCE(?, pathophysiology_ja),
                causes = COALESCE(?, causes),
                causes_ja = COALESCE(?, causes_ja),
                treatment = COALESCE(?, treatment),
                treatment_ja = COALESCE(?, treatment_ja),
                prevention = COALESCE(?, prevention),
                prevention_ja = COALESCE(?, prevention_ja),
                prognosis = COALESCE(?, prognosis),
                prognosis_ja = COALESCE(?, prognosis_ja),
                prognosis_detailed = COALESCE(?, prognosis_detailed),
                prognosis_detailed_ja = COALESCE(?, prognosis_detailed_ja),
                rehabilitation_protocol = COALESCE(?, rehabilitation_protocol),
                rehabilitation_protocol_ja = COALESCE(?, rehabilitation_protocol_ja),
                nutrition_management = COALESCE(?, nutrition_management),
                nutrition_management_ja = COALESCE(?, nutrition_management_ja),
                clinical_signs = COALESCE(?, clinical_signs),
                clinical_signs_ja = COALESCE(?, clinical_signs_ja),
                transmission = COALESCE(?, transmission),
                transmission_ja = COALESCE(?, transmission_ja),
                diagnosis = COALESCE(?, diagnosis),
                diagnosis_ja = COALESCE(?, diagnosis_ja),
                prognosis_references = COALESCE(?, prognosis_references),
                rehabilitation_references = COALESCE(?, rehabilitation_references),
                nutrition_references = COALESCE(?, nutrition_references),
                recovery_timeline_weeks = COALESCE(?, recovery_timeline_weeks),
                success_rate = COALESCE(?, success_rate),
                mortality_rate = COALESCE(?, mortality_rate),
                enriched_at = ?,
                enrichment_phase = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?""",
            (
                _clean(entry.get("description")),
                _clean(entry.get("description_ja")),
                _ensure_string_or_none(entry.get("pathophysiology")),
                _ensure_string_or_none(entry.get("pathophysiology_ja")),
                _clean(entry.get("causes")),
                _clean(entry.get("causes_ja")),
                _ensure_string_or_none(treatment_en or entry.get("treatment")),
                _ensure_string_or_none(treatment_ja or entry.get("treatment_ja")),
                _ensure_string_or_none(prevention_en or entry.get("prevention")),
                _ensure_string_or_none(prevention_ja or entry.get("prevention_ja")),
                _clean(_ensure_string_or_none(prognosis_en or entry.get("prognosis"))),
                _clean(_ensure_string_or_none(prognosis_ja or entry.get("prognosis_ja"))),
                _ensure_string_or_none(entry.get("prognosis_detailed")),
                _ensure_string_or_none(entry.get("prognosis_detailed_ja")),
                _ensure_string_or_none(entry.get("rehabilitation_protocol")),
                _ensure_string_or_none(entry.get("rehabilitation_protocol_ja")),
                _ensure_string_or_none(entry.get("nutrition_management")),
                _ensure_string_or_none(entry.get("nutrition_management_ja")),
                _ensure_string_or_none(entry.get("clinical_signs")),
                _ensure_string_or_none(entry.get("clinical_signs_ja")),
                _ensure_string_or_none(entry.get("transmission")),
                _ensure_string_or_none(entry.get("transmission_ja")),
                _ensure_string_or_none(entry.get("diagnosis")),
                _ensure_string_or_none(entry.get("diagnosis_ja")),
                prognosis_refs,
                rehab_refs,
                nutrition_refs,
                entry.get("recovery_timeline_weeks"),
                entry.get("success_rate"),
                entry.get("mortality_rate"),
                entry.get("enriched_at"),
                entry.get("enrichment_phase"),
                db_id,
            ),
        )
        if conn.execute("SELECT changes()").fetchone()[0] > 0:
            count += 1
    return count


# ---------------------------------------------------------------------------
# Template-based enrichment for diseases still missing clinical fields
# ---------------------------------------------------------------------------

# Disease category keywords → treatment/prevention/prognosis templates
_ENRICHMENT_TEMPLATES = {
    "infectious_viral": {
        "keywords": ["virus", "viral", "influenza", "distemper", "herpes", "corona", "parvo", "calici", "pox"],
        "treatment": [
            "Supportive care including fluid therapy and nutritional support",
            "Antiviral medications where available and appropriate",
            "Anti-inflammatory therapy to manage symptoms",
            "Antibiotics for secondary bacterial infections",
            "Isolation of affected animals to prevent spread",
            "Immunostimulant therapy in chronic cases",
        ],
        "treatment_ja": "支持療法（輸液・栄養管理）；利用可能な場合は抗ウイルス薬；二次感染に対する抗菌薬；感染動物の隔離",
        "prevention": [
            "Vaccination against the causative virus where available",
            "Strict hygiene and sanitation protocols",
            "Quarantine of newly acquired or exposed animals",
            "Minimize stress to maintain immune function",
            "Regular health monitoring for early detection",
        ],
        "prevention_ja": "ワクチン接種；衛生管理の徹底；新規導入動物の検疫；ストレス管理；定期健診",
        "prognosis": [
            "Variable depending on viral strain and host immune status",
            "Early treatment improves outcome significantly",
            "Young, elderly, or immunocompromised animals at higher risk",
            "Some viral infections may become chronic carriers",
        ],
        "prognosis_ja": "ウイルス株と免疫状態に依存；早期治療で予後改善；若齢・高齢・免疫不全動物はリスク高",
    },
    "infectious_bacterial": {
        "keywords": [
            "bacteria",
            "bacterial",
            "abscess",
            "cellulitis",
            "sepsis",
            "streptococ",
            "staphylococ",
            "leptospir",
            "pasteurell",
            "bordetella",
            "mycoplasm",
        ],
        "treatment": [
            "Appropriate antibiotic therapy based on culture and sensitivity testing",
            "Surgical drainage of abscesses when indicated",
            "Supportive care including fluid therapy",
            "Anti-inflammatory medications for pain and swelling",
            "Wound care and hygiene management",
        ],
        "treatment_ja": "感受性試験に基づく適切な抗菌薬療法；必要に応じた外科的排膿；支持療法（輸液）；消炎鎮痛薬",
        "prevention": [
            "Vaccination against common bacterial pathogens where available",
            "Maintain strict sanitation and hygiene practices",
            "Ensure clean drinking water and food sources",
            "Quarantine and treat infected individuals promptly",
            "Regular disinfection of living areas",
        ],
        "prevention_ja": "利用可能なワクチンの接種；衛生環境の維持；清潔な飲食物の提供；感染動物の迅速な隔離・治療",
        "prognosis": [
            "Generally good with early and appropriate antibiotic therapy",
            "Complications may arise if treatment is delayed",
            "Systemic infections carry a more guarded prognosis",
        ],
        "prognosis_ja": "適切な抗菌薬の早期投与で一般的に良好；治療遅延で合併症リスク増大",
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
            "mange",
            "scabies",
            "tapeworm",
            "pinworm",
            "roundworm",
        ],
        "treatment": [
            "Appropriate antiparasitic medications targeting the specific parasite",
            "Environmental decontamination to break the parasite lifecycle",
            "Supportive care for anemia or dehydration if severe infestation",
            "Treatment of secondary skin infections from self-trauma",
            "Repeat treatments as needed to clear all lifecycle stages",
        ],
        "treatment_ja": "対象寄生虫に対する適切な駆虫薬；環境の除染；重度の場合は支持療法；二次感染の治療",
        "prevention": [
            "Regular parasite screening and preventive treatment",
            "Maintain clean living environments and bedding",
            "Proper waste management and sanitation",
            "Regular grooming and inspection for external parasites",
            "Appropriate prophylactic antiparasitic medications",
        ],
        "prevention_ja": "定期的な寄生虫検査と予防投薬；生活環境の清潔保持；適切な廃棄物管理；定期グルーミング",
        "prognosis": [
            "Generally good with appropriate antiparasitic treatment",
            "Prognosis depends on parasite burden and organ involvement",
            "Chronic infestations may cause lasting damage if untreated",
        ],
        "prognosis_ja": "適切な駆虫治療で一般的に良好；寄生虫量と臓器障害の程度に依存",
    },
    "metabolic": {
        "keywords": [
            "diabetes",
            "obesity",
            "thyroid",
            "hyperthyroid",
            "hypothyroid",
            "cushing",
            "addison",
            "metabolic",
            "ketoacid",
            "lipidosis",
            "hepatic lipid",
        ],
        "treatment": [
            "Medical management targeting the specific metabolic imbalance",
            "Dietary modification with species-appropriate therapeutic diet",
            "Hormone replacement or suppression therapy as indicated",
            "Regular monitoring of blood values and clinical response",
            "Long-term management plan with periodic reassessment",
        ],
        "treatment_ja": "代謝異常に対する薬物療法；食事療法；必要に応じたホルモン補充・抑制療法；定期的な血液検査モニタリング",
        "prevention": [
            "Provide balanced, species-appropriate diet",
            "Maintain healthy body weight through portion control",
            "Regular exercise and physical activity",
            "Regular metabolic and nutritional assessments",
            "Monitor for early signs of metabolic imbalance",
        ],
        "prevention_ja": "バランスの取れた食事；適正体重の維持；適度な運動；定期的な代謝・栄養評価",
        "prognosis": [
            "Many metabolic conditions are manageable with lifelong therapy",
            "Prognosis depends on early detection and owner compliance",
            "Regular monitoring improves long-term outcome",
        ],
        "prognosis_ja": "多くの代謝疾患は生涯管理で制御可能；早期発見と飼い主の協力が予後を左右",
    },
    "neoplastic": {
        "keywords": [
            "cancer",
            "tumor",
            "tumour",
            "neoplasm",
            "carcinoma",
            "lymphoma",
            "melanoma",
            "sarcoma",
            "adenocarcinoma",
            "fibrosarcoma",
            "mast cell",
        ],
        "treatment": [
            "Surgical excision with wide margins where feasible",
            "Chemotherapy protocols appropriate for the tumor type",
            "Radiation therapy for localized or non-resectable tumors",
            "Palliative care and pain management in advanced cases",
            "Regular staging and monitoring for recurrence or metastasis",
        ],
        "treatment_ja": "外科的切除（十分なマージンを確保）；腫瘍タイプに応じた化学療法；放射線療法；進行例の緩和ケア",
        "prevention": [
            "Regular physical examinations and health screening",
            "Spay/neuter to reduce hormone-dependent cancers where appropriate",
            "Minimize exposure to known carcinogens",
            "Early detection through routine health monitoring",
            "Genetic screening where breed predisposition exists",
        ],
        "prevention_ja": "定期的な健康診断；適切な避妊・去勢手術；発がん物質への曝露回避；遺伝的スクリーニング",
        "prognosis": [
            "Highly variable depending on tumor type, grade, and stage",
            "Early detection and complete excision offer best outcomes",
            "Metastatic disease carries a guarded to poor prognosis",
        ],
        "prognosis_ja": "腫瘍の種類・グレード・ステージにより大きく異なる；早期発見と完全切除が最良の結果",
    },
    "nutritional": {
        "keywords": [
            "deficiency",
            "malnutrition",
            "nutritional",
            "vitamin",
            "calcium",
            "phosphorus",
            "metabolic bone",
            "rickets",
            "scurvy",
        ],
        "treatment": [
            "Dietary correction with balanced, species-appropriate nutrition",
            "Supplementation of deficient vitamins or minerals",
            "Supportive care for secondary complications",
            "Gradual reintroduction of proper diet to avoid refeeding syndrome",
            "Monitoring of blood values to confirm recovery",
        ],
        "treatment_ja": "バランスの取れた適切な食事への変更；不足ビタミン・ミネラルの補給；合併症への支持療法",
        "prevention": [
            "Provide complete and balanced diet appropriate for the species",
            "Ensure adequate protein, vitamins, and minerals",
            "Regular nutritional assessment and monitoring",
            "Educate owners on proper nutritional requirements",
        ],
        "prevention_ja": "種に適した完全でバランスの取れた食事；栄養評価の定期実施；飼い主への栄養教育",
        "prognosis": [
            "Generally good if detected early and dietary corrections are made promptly",
            "Chronic deficiencies may cause irreversible damage",
            "Full recovery expected with appropriate supplementation in most cases",
        ],
        "prognosis_ja": "早期発見と食事改善で一般的に良好；慢性欠乏は不可逆的損傷の可能性あり",
    },
    "respiratory": {
        "keywords": [
            "respiratory",
            "lung",
            "pneumonia",
            "bronch",
            "asthma",
            "airway",
            "pleural",
            "trachea",
            "rhinitis",
            "sinusitis",
            "dyspnea",
        ],
        "treatment": [
            "Oxygen therapy for respiratory distress",
            "Bronchodilators for airway constriction",
            "Anti-inflammatory therapy (corticosteroids) for airway inflammation",
            "Antibiotics if bacterial infection is confirmed or suspected",
            "Nebulization and coupage for secretion clearance",
            "Thoracocentesis for pleural effusion if indicated",
        ],
        "treatment_ja": "呼吸困難に対する酸素療法；気管支拡張薬；抗炎症薬（コルチコステロイド）；細菌感染に対する抗菌薬；ネブライゼーション",
        "prevention": [
            "Maintain good air quality and avoid respiratory irritants",
            "Ensure adequate ventilation in living areas",
            "Vaccination against common respiratory pathogens",
            "Minimize stress and overcrowding",
        ],
        "prevention_ja": "良好な空気環境の維持；十分な換気；呼吸器病原体に対するワクチン接種；ストレスと過密飼育の回避",
        "prognosis": [
            "Variable depending on underlying cause and severity",
            "Acute respiratory conditions generally respond well to treatment",
            "Chronic respiratory disease may require lifelong management",
        ],
        "prognosis_ja": "原因と重症度に依存；急性呼吸器疾患は治療反応良好；慢性疾患は長期管理が必要な場合あり",
    },
    "gastrointestinal": {
        "keywords": [
            "gastrointestinal",
            "diarrhea",
            "vomiting",
            "enteritis",
            "colitis",
            "ibd",
            "pancreatitis",
            "gastritis",
            "bloat",
            "obstruction",
            "ileus",
            "constipation",
            "prolapse",
            "intussusception",
            "megacolon",
        ],
        "treatment": [
            "Fluid therapy to correct dehydration and electrolyte imbalances",
            "Dietary management with easily digestible food",
            "Anti-emetics and gastroprotectants as needed",
            "Antibiotics if bacterial overgrowth or infection is suspected",
            "Surgical intervention for obstructions or severe conditions",
            "Probiotics to restore normal gut flora",
        ],
        "treatment_ja": "輸液療法（脱水・電解質補正）；消化の良い食事管理；制吐薬・胃粘膜保護薬；必要に応じた抗菌薬；閉塞等の外科的介入",
        "prevention": [
            "Feed high-quality, species-appropriate diet",
            "Maintain clean water and food bowls",
            "Prevent access to spoiled or toxic foods",
            "Minimize dietary changes and maintain consistency",
            "Regular deworming and parasite control",
        ],
        "prevention_ja": "高品質で種に適した食事；清潔な飲食環境；有害食物へのアクセス防止；急な食事変更の回避；定期駆虫",
        "prognosis": [
            "Generally good for acute, uncomplicated gastrointestinal disease",
            "Chronic conditions may require ongoing dietary management",
            "Surgical conditions carry variable prognosis depending on severity",
        ],
        "prognosis_ja": "急性・合併症のない消化器疾患は一般的に良好；慢性疾患は継続的な食事管理が必要",
    },
    "dermatologic": {
        "keywords": [
            "dermatitis",
            "skin",
            "allergic",
            "mange",
            "ringworm",
            "fungal",
            "alopecia",
            "pyoderma",
            "pododermatitis",
            "bumblefoot",
        ],
        "treatment": [
            "Topical and/or systemic medications targeting the underlying cause",
            "Antifungal therapy for fungal infections",
            "Antibiotics for bacterial skin infections",
            "Anti-pruritic therapy for allergic conditions",
            "Environmental and dietary modification for allergies",
            "Regular wound care and hygiene",
        ],
        "treatment_ja": "原因に対する局所・全身薬物療法；真菌感染に対する抗真菌薬；細菌感染に対する抗菌薬；アレルギーの環境・食事管理",
        "prevention": [
            "Regular grooming and skin hygiene",
            "Identify and avoid allergens or irritants",
            "Maintain clean and dry living environment",
            "Proper nutrition for healthy coat and skin",
        ],
        "prevention_ja": "定期的なグルーミングと皮膚衛生；アレルゲンの特定と回避；清潔で乾燥した環境の維持；適切な栄養管理",
        "prognosis": [
            "Good for most treatable skin conditions with appropriate therapy",
            "Allergic skin disease often requires lifelong management",
            "Fungal infections generally resolve with complete treatment courses",
        ],
        "prognosis_ja": "適切な治療で多くの皮膚疾患は良好；アレルギー性皮膚疾患は長期管理が必要なことが多い",
    },
    "urinary": {
        "keywords": [
            "urinary",
            "kidney",
            "renal",
            "bladder",
            "calculi",
            "urolithiasis",
            "cystitis",
            "nephritis",
            "flutd",
        ],
        "treatment": [
            "Fluid therapy to support renal function and hydration",
            "Dietary modification with therapeutic renal or urinary diets",
            "Pain management and anti-spasmodic medications",
            "Antibiotics for confirmed urinary tract infections",
            "Surgical intervention for obstructive uroliths if necessary",
            "Long-term monitoring of kidney function values",
        ],
        "treatment_ja": "腎機能維持のための輸液療法；治療食（腎臓・泌尿器用）；疼痛管理；尿路感染に対する抗菌薬；必要時の外科的介入",
        "prevention": [
            "Ensure adequate water intake and hydration",
            "Feed appropriate diet with balanced minerals",
            "Regular urinalysis and kidney function monitoring",
            "Prevent obesity and maintain healthy weight",
        ],
        "prevention_ja": "十分な水分摂取の確保；ミネラルバランスの取れた食事；定期的な尿検査・腎機能モニタリング；肥満防止",
        "prognosis": [
            "Variable depending on the specific condition and stage",
            "Acute urinary conditions often respond well to treatment",
            "Chronic kidney disease requires lifelong management with guarded long-term prognosis",
        ],
        "prognosis_ja": "疾患の種類とステージにより異なる；急性泌尿器疾患は治療反応良好なことが多い；慢性腎臓病は長期管理が必要",
    },
    "cardiovascular": {
        "keywords": [
            "cardiac",
            "heart",
            "cardiovascular",
            "cardiomyopathy",
            "murmur",
            "arrhythmia",
            "thromboembolism",
            "endocard",
        ],
        "treatment": [
            "Cardiac medications (ACE inhibitors, diuretics, positive inotropes) as indicated",
            "Antiarrhythmic therapy for rhythm disturbances",
            "Anticoagulation therapy for thromboembolic risk",
            "Dietary sodium restriction",
            "Exercise restriction in symptomatic patients",
            "Regular cardiac monitoring with echocardiography",
        ],
        "treatment_ja": "心臓薬（ACE阻害薬・利尿薬・強心薬）；抗不整脈薬；抗凝固療法；食事ナトリウム制限；運動制限；定期心エコー検査",
        "prevention": [
            "Regular cardiac screening and monitoring",
            "Maintain healthy body weight",
            "Balanced low-sodium diet",
            "Genetic screening where breed predisposition exists",
        ],
        "prevention_ja": "定期的な心臓検診；健康的な体重維持；低ナトリウム食；品種素因がある場合の遺伝的スクリーニング",
        "prognosis": [
            "Variable depending on type and stage of cardiac disease",
            "Early detection and medical management can significantly extend survival",
            "Advanced heart failure carries a guarded prognosis",
        ],
        "prognosis_ja": "心疾患の種類とステージに依存；早期発見と内科管理で生存期間を大幅に延長可能；進行した心不全は予後不良",
    },
    "neurologic": {
        "keywords": [
            "seizure",
            "epilepsy",
            "neurologic",
            "neurological",
            "paralysis",
            "paresis",
            "vestibular",
            "neuropathy",
            "encephalitis",
            "meningitis",
        ],
        "treatment": [
            "Anticonvulsant therapy for seizure control",
            "Anti-inflammatory therapy for inflammatory CNS disease",
            "Supportive care and physical rehabilitation",
            "Pain management as needed",
            "Surgical intervention for compressive lesions",
            "Emergency stabilization for status epilepticus",
        ],
        "treatment_ja": "抗けいれん薬；中枢神経系炎症に対する抗炎症療法；支持療法とリハビリテーション；疼痛管理；圧迫性病変の外科的介入",
        "prevention": [
            "Prevent head trauma and injuries",
            "Maintain steady blood glucose levels",
            "Avoid toxin exposure and poisoning",
            "Regular health monitoring for early detection",
        ],
        "prevention_ja": "頭部外傷の防止；安定した血糖値の維持；毒物への曝露回避；早期発見のための定期健診",
        "prognosis": [
            "Variable depending on underlying neurological condition",
            "Idiopathic epilepsy is generally manageable with medication",
            "Structural brain lesions carry a more guarded prognosis",
        ],
        "prognosis_ja": "基礎疾患により異なる；特発性てんかんは投薬で一般的に管理可能；構造的脳病変は予後不良の場合あり",
    },
    "musculoskeletal": {
        "keywords": [
            "fracture",
            "arthritis",
            "osteo",
            "bone",
            "joint",
            "luxation",
            "dislocation",
            "dysplasia",
            "spondyl",
            "ligament",
            "tendon",
            "lameness",
        ],
        "treatment": [
            "Pain management with analgesics and anti-inflammatories",
            "Surgical stabilization for fractures and luxations",
            "Joint supplements (glucosamine, chondroitin) for degenerative conditions",
            "Physical therapy and controlled exercise rehabilitation",
            "Weight management to reduce joint stress",
        ],
        "treatment_ja": "鎮痛薬・抗炎症薬による疼痛管理；骨折・脱臼の外科的整復；関節サプリメント；理学療法；体重管理",
        "prevention": [
            "Provide appropriate exercise and avoid overexertion",
            "Maintain healthy body weight",
            "Ensure proper nutrition for bone and joint health",
            "Provide safe housing to prevent traumatic injuries",
        ],
        "prevention_ja": "適度な運動と過度の負荷回避；適正体重の維持；骨・関節の健康のための適切な栄養；外傷防止のための安全な飼育環境",
        "prognosis": [
            "Variable depending on condition and treatment approach",
            "Simple fractures generally heal well with proper stabilization",
            "Degenerative joint disease requires lifelong management",
        ],
        "prognosis_ja": "疾患と治療法に依存；単純骨折は適切な固定で良好に治癒；変性性関節疾患は長期管理が必要",
    },
    "ophthalmic": {
        "keywords": [
            "eye",
            "ocular",
            "conjunctiv",
            "cataract",
            "glaucoma",
            "ulcer",
            "keratitis",
            "uveitis",
            "proptosis",
            "entropion",
            "ectropion",
        ],
        "treatment": [
            "Topical ophthalmic medications (antibiotics, anti-inflammatories, lubricants)",
            "Systemic medications for severe or systemic ophthalmic disease",
            "Surgical intervention for structural conditions",
            "Pain management and protective measures (e.g., E-collar)",
        ],
        "treatment_ja": "点眼薬（抗菌薬・抗炎症薬・潤滑薬）；重症例の全身薬物療法；構造的疾患の外科的治療；疼痛管理",
        "prevention": [
            "Regular eye examinations",
            "Protect eyes from trauma and irritants",
            "Maintain good hygiene around the face and eyes",
            "Prompt treatment of early signs of eye disease",
        ],
        "prevention_ja": "定期的な眼科検診；外傷や刺激物からの保護；顔面・眼周囲の衛生管理；初期症状の早期治療",
        "prognosis": [
            "Variable depending on condition severity and time to treatment",
            "Many ophthalmic conditions respond well to prompt treatment",
            "Delayed treatment may result in permanent vision impairment",
        ],
        "prognosis_ja": "疾患の重症度と治療開始時期に依存；多くの眼疾患は早期治療で良好；治療遅延は永続的な視力障害の可能性",
    },
    "dental": {
        "keywords": ["dental", "tooth", "teeth", "malocclusion", "gingivitis", "periodontal", "stomatitis", "abscess"],
        "treatment": [
            "Dental examination under sedation or anesthesia",
            "Professional dental cleaning and scaling",
            "Extraction of diseased or maloccluded teeth",
            "Antibiotics for dental infections and abscesses",
            "Pain management post-procedure",
            "Dietary modification to soft foods during recovery",
        ],
        "treatment_ja": "鎮静・麻酔下での歯科検査；専門的なスケーリング；罹患歯・不正咬合歯の抜歯；感染に対する抗菌薬；術後疼痛管理",
        "prevention": [
            "Regular dental health checks",
            "Provide appropriate chew items for dental wear",
            "Balanced diet with proper fiber content",
            "Monitor for signs of dental disease (drooling, appetite loss)",
        ],
        "prevention_ja": "定期的な歯科健診；適切な咀嚼物の提供；バランスの取れた食事；歯科疾患の兆候モニタリング",
        "prognosis": [
            "Good with regular dental care and early intervention",
            "Untreated dental disease can lead to systemic infection",
            "Some species require lifelong dental management",
        ],
        "prognosis_ja": "定期的な歯科ケアと早期介入で良好；未治療の歯科疾患は全身感染に進展する可能性あり",
    },
    "reproductive": {
        "keywords": [
            "reproductive",
            "uterine",
            "pyometra",
            "dystocia",
            "mastitis",
            "testicular",
            "ovarian",
            "pregnancy",
            "prolapse",
        ],
        "treatment": [
            "Surgical intervention (ovariohysterectomy for pyometra, C-section for dystocia)",
            "Antibiotics for reproductive tract infections",
            "Hormonal therapy where medically indicated",
            "Supportive care and fluid therapy",
            "Neonatal care if applicable",
        ],
        "treatment_ja": "外科的介入（子宮蓄膿症の卵巣子宮摘出、難産の帝王切開）；生殖器感染に対する抗菌薬；支持療法",
        "prevention": [
            "Spay/neuter to prevent reproductive diseases where appropriate",
            "Proper breeding management and prenatal care",
            "Regular reproductive health monitoring",
            "Maintain good hygiene during and after parturition",
        ],
        "prevention_ja": "適切な避妊・去勢手術；適正な繁殖管理と妊娠ケア；定期的な生殖器健診；分娩時の衛生管理",
        "prognosis": [
            "Generally good with prompt surgical or medical intervention",
            "Delayed treatment of reproductive emergencies can be life-threatening",
        ],
        "prognosis_ja": "迅速な外科的・内科的介入で一般的に良好；生殖器緊急疾患の治療遅延は致命的になりうる",
    },
    "default": {
        "keywords": [],
        "treatment": [
            "Specific treatment based on definitive diagnosis",
            "Supportive care including fluid therapy and nutritional support",
            "Pain management as appropriate",
            "Address underlying cause when identified",
            "Regular follow-up monitoring to assess treatment response",
        ],
        "treatment_ja": "確定診断に基づく特異的治療；支持療法（輸液・栄養管理）；適切な疼痛管理；原因疾患の治療；定期フォローアップ",
        "prevention": [
            "Regular veterinary health check-ups",
            "Provide balanced nutrition and clean water",
            "Maintain good hygiene and sanitation",
            "Minimize stress and maintain optimal living conditions",
            "Early detection and prompt treatment of disease signs",
        ],
        "prevention_ja": "定期的な獣医師による健康診断；バランスの取れた栄養と清潔な水の提供；衛生管理；ストレス軽減；早期発見・治療",
        "prognosis": [
            "Variable depending on the specific condition and response to treatment",
            "Early diagnosis and appropriate treatment improve outcomes",
            "Consult with a veterinarian for disease-specific prognosis",
        ],
        "prognosis_ja": "疾患の種類と治療反応に依存；早期診断と適切な治療で予後改善；詳細な予後は獣医師にご相談ください",
    },
}


def _classify_disease(name: str, description: str) -> str:
    """Classify a disease into a template category by keyword matching."""
    text = f"{name} {description}".lower()
    category_order = [
        "neoplastic",
        "metabolic",
        "musculoskeletal",
        "ophthalmic",
        "dental",
        "reproductive",
        "neurologic",
        "cardiovascular",
        "urinary",
        "dermatologic",
        "gastrointestinal",
        "respiratory",
        "nutritional",
        "infectious_viral",
        "infectious_bacterial",
        "parasitic",
    ]
    for cat in category_order:
        if cat in _ENRICHMENT_TEMPLATES:
            for kw in _ENRICHMENT_TEMPLATES[cat]["keywords"]:
                if kw in text:
                    return cat
    return "default"


def _generate_text(templates: list[str], seed_key: str, count: int = 3) -> str:
    """Select and join template sentences deterministically."""
    seed = int(hashlib.md5(seed_key.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    selected = rng.sample(templates, min(count, len(templates)))
    return "; ".join(selected) + "."


def enrich_missing_fields(conn) -> dict[str, int]:
    """Fill treatment/prevention/prognosis for diseases still missing them.

    Uses category-based templates to generate clinically appropriate text.
    Only updates NULL or empty fields — existing data from Python modules
    or JSON enrichment is preserved.
    """
    rows = conn.execute(
        """SELECT id, name, description FROM diseases
           WHERE (treatment IS NULL OR treatment = '')
              OR (prevention IS NULL OR prevention = '')
              OR (prognosis IS NULL OR prognosis = '')"""
    ).fetchall()

    stats = {"treatment": 0, "prevention": 0, "prognosis": 0}
    for row in rows:
        did, name, desc = row["id"], row["name"], row["description"] or ""
        cat = _classify_disease(name, desc)
        tmpl = _ENRICHMENT_TEMPLATES[cat]

        updates = {}
        current = conn.execute(
            "SELECT treatment, treatment_ja, prevention, prevention_ja, prognosis, prognosis_ja FROM diseases WHERE id = ?",
            (did,),
        ).fetchone()

        if not current["treatment"]:
            updates["treatment"] = _generate_text(tmpl["treatment"], f"{did}_treatment")
            updates["treatment_ja"] = tmpl["treatment_ja"]
            stats["treatment"] += 1
        if not current["prevention"]:
            updates["prevention"] = _generate_text(tmpl["prevention"], f"{did}_prevention")
            updates["prevention_ja"] = tmpl["prevention_ja"]
            stats["prevention"] += 1
        if not current["prognosis"]:
            updates["prognosis"] = _generate_text(tmpl["prognosis"], f"{did}_prognosis")
            updates["prognosis_ja"] = tmpl["prognosis_ja"]
            stats["prognosis"] += 1

        if updates:
            set_clauses = ", ".join(f"{k} = ?" for k in updates)
            conn.execute(
                f"UPDATE diseases SET {set_clauses}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (*updates.values(), did),
            )

    return stats


def migrate_drugs(conn) -> int:
    """Migrate drugs from drug_dictionary module."""
    mod = _load_module("api.drug_dictionary")
    drugs = getattr(mod, "DRUGS", [])
    count = 0
    for drug in drugs:
        upsert_drug(conn, drug)
        count += 1
    return count


def migrate_equine(conn) -> int:
    """Migrate equine diseases (Disease dataclass with different field names)."""
    mod = _load_module("api.species.equine_diseases")
    disease_db = getattr(mod, "DISEASE_DATABASE", [])
    count = 0

    def _extract_ja_en(field_val):
        if isinstance(field_val, dict):
            return field_val.get("ja"), field_val.get("en")
        return None, field_val

    for d in disease_db:
        treatment_ja, treatment_en = _extract_ja_en(d.treatment_protocol)
        prevention_ja, prevention_en = _extract_ja_en(d.prevention)
        prognosis_ja, prognosis_en = _extract_ja_en(d.prognosis)

        record = {
            "id": d.id,
            "species": "horse",
            "name": d.name_en,
            "name_ja": d.name_ja,
            "description": d.description_ja,
            "description_ja": d.description_ja,
            "pathophysiology": d.pathophysiology,
            "causes": d.etiology,
            "treatment": treatment_en or d.treatment_protocol,
            "treatment_ja": treatment_ja or getattr(d, "treatment_ja", None),
            "prevention": prevention_en or d.prevention,
            "prevention_ja": prevention_ja or getattr(d, "prevention_ja", None),
            "prognosis": prognosis_en or d.prognosis,
            "prognosis_ja": prognosis_ja or getattr(d, "prognosis_ja", None),
            "urgency": d.urgency or d.severity,
            "symptoms": set(d.associated_findings),
            "recommended_tests": [(e[1] if len(e) > 1 else str(e)) for e in (d.recommended_exams or [])],
            "diagnosis": None,
            "diagnosis_ja": None,
            "clinical_signs": getattr(d, "clinical_signs_detail", None),
            "clinical_signs_ja": getattr(d, "clinical_signs_detail", None),
            "transmission": None,
            "transmission_ja": None,
            "differential_diagnosis": None,
        }
        upsert_disease(conn, record)
        count += 1
    return count


def migrate_equine_symptoms(conn) -> int:
    """Migrate horse symptoms from HEALTH_CHECK_ITEMS (category-aware)."""
    mod = _load_module("api.species.equine_diseases")
    health_items = getattr(mod, "HEALTH_CHECK_ITEMS", {})
    count = 0
    for _category, items in health_items.items():
        for symptom_id, name_ja, name_en in items:
            upsert_symptom(conn, f"horse_{symptom_id}", name_en, name_ja, "horse")
            count += 1
    return count


def regenerate_cross_disease_templates(conn) -> dict[str, int]:
    """Replace cross-disease template clinical fields in the served DB.

    Some diseases live only in the Python species modules (no JSON overlay) and
    still carry short category-level template text shared verbatim by many
    unrelated diseases — e.g. one prognosis sentence on 186 different diseases
    spanning chytridiomycosis, dysecdysis and anorexia. Those read as generic
    boilerplate to a clinician.

    A field value is treated as a cross-disease template when the same text is
    shared by >= ``MIN_SHARE`` entries spanning >= ``MIN_NAMES`` distinct base
    disease names. Such values are regenerated into disease-specific text with
    ``clinical_fields_generator`` (which embeds the disease name and resolves
    the true category from the name). Genuine same-disease variants (e.g.
    fracture subtypes) span too few distinct names and are left untouched.
    """
    import re as _re
    from collections import defaultdict

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.clinical_fields_generator import generate_clinical_fields

    fields = [
        "prognosis_ja",
        "prognosis",
        "causes_ja",
        "pathophysiology_ja",
        "prevention_ja",
        "clinical_signs_ja",
        "clinical_signs",
        "transmission_ja",
        "transmission",
        "diagnosis_ja",
        "diagnosis",
    ]
    # Short category one-liners (e.g. a 28-char mite prognosis shared by 25
    # different parasites) are templates too, so the floor is low; the
    # distinct-name guard below is what protects genuine same-disease variants.
    MIN_LEN = 20
    MIN_SHARE = 3
    MIN_NAMES = 3
    _paren = _re.compile(r"[（(][^（）()]*[）)]\s*$")

    def _base(name: str) -> str:
        return _paren.sub("", name or "").strip()

    # Dog/cat prevention advice must never sit on another species' entry. The
    # legacy generator emitted dog/cat category templates (DCM-predisposed
    # breeds, puppy/kitten deworming, BCS 4-5/9, FLUTD, 子宮蓄膿症リスク...) for
    # every species. Rather than hand-maintaining a fragment list, derive the
    # companion template bodies straight from the generator: any non-companion
    # entry whose text contains one of those bodies has been contaminated and is
    # regenerated into species-appropriate text — even when its name-prefixed
    # text is otherwise unique.
    _COMPANION = {"dog", "cat"}
    from scripts.template_elimination.clinical_fields_generator import gen_prevention_ja as _gen_prev

    _PREVENT_CATEGORIES = (
        "viral_infection",
        "bacterial_infection",
        "respiratory_infection",
        "fungal_infection",
        "parasitic",
        "neoplasia",
        "endocrine_metabolic",
        "renal_urinary",
        "cardiac",
        "respiratory_other",
        "gastrointestinal",
        "neurological",
        "ophthalmic",
        "musculoskeletal",
        "dental",
        "dermatological",
        "hematological",
        "reproductive",
        "toxicity",
        "trauma",
        "autoimmune",
        "nutritional",
        "behavioral",
        "generic",
    )

    def _companion_body(text: str) -> str:
        # Strip the "犬における<name>の予防は/には" lead to leave the shared body.
        for sep in ("の予防には", "の予防は"):
            idx = text.find(sep)
            if idx != -1:
                return text[idx + len(sep) :].strip()
        return text.strip()

    _COMPANION_BODIES = {
        body
        for cat in _PREVENT_CATEGORIES
        for body in (_companion_body(_gen_prev(cat, "ZZ", "dog")),)
        if len(body) >= 25
    }

    def _is_contaminated(species: str, val: str) -> bool:
        if (species or "").lower() in _COMPANION:
            return False
        return any(body in val for body in _COMPANION_BODIES)

    counts: dict[str, int] = {f: 0 for f in fields}
    rows = conn.execute("SELECT id, species, name, name_ja, " + ", ".join(fields) + " FROM diseases").fetchall()

    for field in fields:
        groups: dict[str, list] = defaultdict(list)
        for row in rows:
            val = (row[field] or "").strip()
            if val and len(val) >= MIN_LEN:
                groups[val].append(row)
        template_texts = {
            val
            for val, items in groups.items()
            if len(items) >= MIN_SHARE and len({_base(r["name_ja"] or r["name"]) for r in items}) >= MIN_NAMES
        }
        # Collect the rows to regenerate: cross-disease templates (all fields)
        # plus, for prevention, any non-companion entry carrying dog/cat markers.
        targets: dict[int, object] = {}
        for val in template_texts:
            for row in groups[val]:
                targets[row["id"]] = row
        if field == "prevention_ja":
            for row in rows:
                val = (row[field] or "").strip()
                if val and _is_contaminated(row["species"], val):
                    targets[row["id"]] = row

        for row in targets.values():
            val = (row[field] or "").strip()
            new = generate_clinical_fields(
                (row["species"] or "").lower(),
                row["name_ja"] or "",
                row["name"] or "",
                "",
                [field],
            )
            text = new.get(field)
            if text and text != val:
                conn.execute(
                    f"UPDATE diseases SET {field} = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (text, row["id"]),
                )
                counts[field] += 1
    return counts


def ground_templated_fields_with_signs(conn) -> dict[str, int]:
    """Make templated prevention_ja / prognosis_ja disease-specific via own signs.

    ``regenerate_cross_disease_templates`` only replaces *exact* duplicates, and
    its replacement generators are keyed on (species, category) — so prevention
    and prognosis text stays byte-identical across every disease of a category
    once the disease name is normalised out. A clinician opening several diseases
    of a species sees the identical paragraph, the classic "generic AI" tell.

    This pass keeps the vetted category base but appends a disease-specific
    clause built from the record's *own* curated presenting signs (resolved to
    Japanese): prevention gets early-detection surveillance targets, prognosis
    gets treatment-response monitoring targets. Only entries whose text is shared
    verbatim (modulo disease name) by >= ``MIN_SHARE`` records spanning >=
    ``MIN_NAMES`` distinct disease names are grounded; genuinely unique/curated
    text is left untouched. It only restates signs already on the record, so no
    new medical claim is introduced.
    """
    import json as _json
    import re as _re
    from collections import defaultdict

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.clinical_fields_generator import (
        compose_grounded_pathophysiology,
        compose_grounded_pathophysiology_ja,
        compose_grounded_prevention,
        compose_grounded_prevention_ja,
        compose_grounded_prognosis,
        compose_grounded_prognosis_ja,
    )

    try:
        from api.health_checker import _get_species_symptom_names
    except ImportError:
        from health_checker import _get_species_symptom_names  # type: ignore

    _cjk = _re.compile(r"[぀-ヿ㐀-鿿]")
    _paren = _re.compile(r"[（(][^（）()]*[）)]\s*$")
    MIN_LEN = 20
    MIN_SHARE = 3
    MIN_NAMES = 3

    # Japanese fields take Japanese sign names; English fields take English sign
    # names. Each maps to its grounding composer + which language of signs to feed.
    composers = {
        "prevention_ja": (compose_grounded_prevention_ja, "ja"),
        "prognosis_ja": (compose_grounded_prognosis_ja, "ja"),
        "pathophysiology_ja": (compose_grounded_pathophysiology_ja, "ja"),
        "prevention": (compose_grounded_prevention, "en"),
        "prognosis": (compose_grounded_prognosis, "en"),
        "pathophysiology": (compose_grounded_pathophysiology, "en"),
    }

    def _base(name: str) -> str:
        return _paren.sub("", name or "").strip()

    _signs_cache: dict[tuple[int, str], list[str]] = {}

    def _signs(row, lang: str) -> list[str]:
        ck = (row["id"], lang)
        if ck in _signs_cache:
            return _signs_cache[ck]
        try:
            ids = _json.loads(row["symptoms"] or "[]")
        except (ValueError, TypeError):
            ids = []
        lut = _get_species_symptom_names((row["species"] or "").lower())
        out: list[str] = []
        for sid in ids:
            entry = lut.get(sid)
            if not isinstance(entry, dict):
                continue
            val = entry.get(lang)
            if not val:
                continue
            # Japanese clauses want CJK sign names; English clauses want the
            # English label (skip if it is only a raw snake_case id fallback).
            if lang == "ja" and not _cjk.search(val):
                continue
            if val not in out:
                out.append(val)
        _signs_cache[ck] = out
        return out

    def _strip_name(text: str, name_ja: str, name: str) -> str:
        for nm in (name_ja, _base(name_ja), name, _base(name)):
            if nm:
                text = text.replace(nm, "※")
        return text

    fields = list(composers)
    rows = conn.execute(
        "SELECT id, species, name, name_ja, symptoms, " + ", ".join(fields) + " FROM diseases"
    ).fetchall()

    counts = {f: 0 for f in fields}
    for field in fields:
        groups: dict[str, list] = defaultdict(list)
        for row in rows:
            val = (row[field] or "").strip()
            if val and len(val) >= MIN_LEN:
                key = _strip_name(val, row["name_ja"] or "", row["name"] or "")
                groups[key].append(row)
        templated_ids = {
            r["id"]
            for items in groups.values()
            if len(items) >= MIN_SHARE and len({_base(r["name_ja"] or r["name"]) for r in items}) >= MIN_NAMES
            for r in items
        }
        compose, lang = composers[field]
        for row in rows:
            if row["id"] not in templated_ids:
                continue
            new = compose(row[field] or "", _signs(row, lang))
            if new and new != (row[field] or "").strip():
                conn.execute(
                    f"UPDATE diseases SET {field} = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (new, row["id"]),
                )
                counts[field] += 1
    return counts


def fix_prognosis_possessive_en(conn) -> int:
    """Repair the ``"... in <species>s's prognosis ..."`` double-possessive bug.

    ``gen_prognosis_en`` historically joined the subject ``"<disease> in
    <species>s"`` with catalog clauses beginning ``"'s prognosis ..."``, giving
    ungrammatical text like ``"Acute Enteritis in rabbits's prognosis varies
    ..."`` that reads as machine output to an English visitor. The generator is
    now fixed; this pass repairs any such text already materialised in the served
    DB from module/supplementary sources. It only rewrites the possessive to
    ``"The prognosis of <disease> in <species> ..."`` — no clinical content
    changes.
    """
    import re as _re

    pat = _re.compile(r"^(.+?) in ([A-Za-z][A-Za-z ]*?)'s prognosis")
    rows = conn.execute('SELECT id, prognosis FROM diseases WHERE prognosis LIKE "%\'s prognosis%"').fetchall()
    n = 0
    for row in rows:
        val = row["prognosis"] or ""
        new = pat.sub(r"The prognosis of \1 in \2", val, count=1)
        if new != val:
            conn.execute("UPDATE diseases SET prognosis = ? WHERE id = ?", (new, row["id"]))
            n += 1
    return n


def localize_english_species_in_served_db(conn) -> int:
    """Replace English species placeholders that leaked into Japanese DB fields.

    Module-sourced and supplementary entries occasionally carry the *English*
    species name inside Japanese text (``Hamsterにおける…`` / ``…（Amphibian）``),
    which reads as broken localisation to a Japanese clinician. This sweeps the
    served database so the delivered content is clean regardless of which source
    introduced the token. Breed/proper names (``Quarter Horse``) are preserved by
    the localiser's lookbehind.
    """
    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.fix_english_species_in_ja import JA_FIELDS, localise

    existing = {r["name"] for r in conn.execute("PRAGMA table_info(diseases)").fetchall()}
    fields = [f for f in JA_FIELDS if f in existing]
    rows = conn.execute("SELECT id, " + ", ".join(fields) + " FROM diseases").fetchall()
    total = 0
    for row in rows:
        updates = {}
        for f in fields:
            v = row[f]
            if not v:
                continue
            new, n = localise(v)
            if n:
                updates[f] = new
                total += n
        if updates:
            sets = ", ".join(f"{f} = ?" for f in updates)
            conn.execute(
                f"UPDATE diseases SET {sets}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (*updates.values(), row["id"]),
            )
    return total


def fix_dangerous_treatment_in_served_db(conn) -> dict[str, int]:
    """Replace clinically dangerous treatment templates on the served DB.

    Module-sourced and supplementary entries can carry a category-specific
    treatment template whose category contradicts the disease, producing
    recommendations that would harm a patient if published:

    * a *deworming* protocol on tick-borne / hemotropic bacteria (ehrlichiosis,
      anaplasmosis, spotted fever, hemoplasmosis — doxycycline-responsive);
    * a *deworming* protocol on a toxicosis (permethrin / Teflon);
    * a *chemotherapy / TNM-staging* protocol on a benign cyst or polyp.

    This sweeps the served database so the delivered content is corrected
    regardless of which source introduced the template. The replacement is gated
    on the corrected name-priority class (``_disease_class_hint``), so genuine
    parasites and genuine tumours are never touched.
    """
    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.eliminate_templates import SPECIES_NORM
    from scripts.template_elimination.fallback_generator import (
        _disease_class_hint,
        generate_fallback_content,
    )

    ONCO_SIG = "腫瘍の組織学的型・グレード"
    DEWORM_OVERRIDE = {"rickettsial", "toxic", "nutritional"}
    NAME_EXCLUDE = ("サーモン中毒", "サケ中毒")

    def _has_deworm_template(tx: str) -> bool:
        # Matches the parasitic deworming protocols ("適切な駆虫薬が必要" /
        # "駆虫薬を選択") but never the doxycycline text that *warns* dewormers
        # are ineffective ("フルオロキノロン・駆虫薬は無効").
        return "駆虫薬" in tx and "駆虫薬は無効" not in tx

    rows = conn.execute("SELECT id, name_ja, name, species, treatment_ja, treatment FROM diseases").fetchall()
    stats: dict[str, int] = {}
    for row in rows:
        tx = row["treatment_ja"] or ""
        if not tx:
            continue
        name_ja = row["name_ja"] or ""
        name_en = row["name"] or ""
        klass = _disease_class_hint(name_ja or name_en)

        target = None
        if _has_deworm_template(tx) and klass in DEWORM_OVERRIDE:
            if not any(x in (name_ja + name_en) for x in NAME_EXCLUDE):
                target = klass
        elif ONCO_SIG in tx and klass == "cyst_polyp":
            target = "cyst_polyp"
        if target is None:
            continue

        species = SPECIES_NORM.get(row["species"], row["species"]).lower()
        new = generate_fallback_content(species, name_ja, name_en, en_treatment=row["treatment"])
        new_tx = new.get("treatment_ja")
        if not new_tx or new_tx == tx:
            continue
        conn.execute(
            "UPDATE diseases SET treatment_ja = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (new_tx, row["id"]),
        )
        stats[target] = stats.get(target, 0) + 1
    return stats


def apply_curated_dangerous_treatments(conn) -> int:
    """Replace dangerous category-mismatched treatments with curated protocols.

    Handles the residual cases ``fix_dangerous_treatment_in_served_db`` cannot:
    diseases that resolve to the generic ``general`` class but carry a
    toxin-decontamination or deworming template that is clinically wrong for them
    (cecal dysbiosis, haemolytic anaemia, proventricular ulceration, a gizzard
    foreign body, a cerebral infarct, rectal prolapse, fibrotic myopathy,
    neonatal conjunctivitis). Gated on a dangerous fingerprint AND a curated
    entry matching the disease, so no other record is touched.
    """
    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_dangerous_treatments import (
        curated_dangerous_treatment,
    )

    rows = conn.execute("SELECT id, species, name, name_ja, treatment_ja FROM diseases").fetchall()
    n = 0
    for row in rows:
        new_tx = curated_dangerous_treatment(
            row["species"] or "", row["name_ja"] or "", row["name"] or "", row["treatment_ja"] or ""
        )
        if new_tx:
            conn.execute(
                "UPDATE diseases SET treatment_ja = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (new_tx, row["id"]),
            )
            n += 1
    return n


def regenerate_protozoal_treatments(conn) -> dict[str, int]:
    """Replace the deworming template on protozoal diseases with antiprotozoal protocols.

    Protozoa (Babesia, Toxoplasma, Leishmania, Hepatozoon, Cytauxzoon,
    Encephalitozoon, coccidia, Sarcocystis, Atoxoplasma, Leucocytozoon, avian
    malaria) are not treated with anthelmintics, yet ~40 records carry the generic
    deworming treatment template. This served-database safety net corrects
    module-sourced records the JSON-overlay pass cannot reach. ``treatment_ja`` /
    ``treatment`` are always replaced (the dewormer text is clinically wrong);
    ``pathophysiology_ja`` / ``pathophysiology`` are replaced only when empty, a
    category template, or a recognised stub, so curated mechanism prose that names
    the pathogen is preserved.
    """
    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.antiprotozoal_library import (
        PATHO_EN_STUB_MARKS,
        PATHO_JA_STUB_MARKS,
        protozoal_clinical_fields,
    )
    from scripts.template_elimination.clinical_fields_generator import (
        build_etiology_fingerprints,
        fingerprint_etiology,
        gen_pathophysiology_ja,
    )
    from scripts.template_elimination.curated_etiology import STUB_SIGNATURES

    patho_fps = build_etiology_fingerprints(gen_pathophysiology_ja)

    def _ja_replaceable(text: str) -> bool:
        if not text:
            return True
        if fingerprint_etiology(text, patho_fps) is not None:
            return True
        if any(sig in text for sig in STUB_SIGNATURES):
            return True
        return any(m in text for m in PATHO_JA_STUB_MARKS)

    def _en_replaceable(text: str) -> bool:
        if not text:
            return True
        low = text.lower()
        return any(m in low for m in PATHO_EN_STUB_MARKS)

    rows = conn.execute(
        "SELECT id, species, name, name_ja, treatment_ja, pathophysiology_ja, pathophysiology FROM diseases"
    ).fetchall()
    stats = {"treatment": 0, "pathophysiology_ja": 0, "pathophysiology": 0}
    for row in rows:
        fields = protozoal_clinical_fields(
            row["species"] or "", row["name_ja"] or "", row["name"] or "", row["treatment_ja"] or ""
        )
        if not fields:
            continue
        conn.execute(
            "UPDATE diseases SET treatment_ja = ?, treatment = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (fields["treatment_ja"], fields["treatment"], row["id"]),
        )
        stats["treatment"] += 1
        if _ja_replaceable(row["pathophysiology_ja"] or ""):
            conn.execute(
                "UPDATE diseases SET pathophysiology_ja = ? WHERE id = ?",
                (fields["pathophysiology_ja"], row["id"]),
            )
            stats["pathophysiology_ja"] += 1
        if _en_replaceable(row["pathophysiology"] or ""):
            conn.execute(
                "UPDATE diseases SET pathophysiology = ? WHERE id = ?",
                (fields["pathophysiology"], row["id"]),
            )
            stats["pathophysiology"] += 1
    return stats


def apply_curated_etiology(conn) -> int:
    """Supply curated causes_ja / pathophysiology_ja for multifactorial diseases.

    Laminitis (predominantly endocrinopathic/inflammatory, not orthopaedic) and
    hepatic fibrosis (the fibrotic end-stage of chronic liver injury, with no
    dedicated hepatic etiology bucket) cannot be templated into one category, so
    the recategoriser can only swap one imperfect template for another. This pass
    writes concise, textbook-accurate, disease-specific etiology — but ONLY over a
    field that is empty, a recognised category template, or a vague stub, so
    genuine curated prose (e.g. the existing laminitis pathophysiology) is kept.
    """
    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.clinical_fields_generator import (
        build_etiology_fingerprints,
        fingerprint_etiology,
        gen_causes_ja,
        gen_pathophysiology_ja,
    )
    from scripts.template_elimination.curated_etiology import STUB_SIGNATURES, curated_etiology

    fps = {
        "causes_ja": build_etiology_fingerprints(gen_causes_ja),
        "pathophysiology_ja": build_etiology_fingerprints(gen_pathophysiology_ja),
    }

    def _replaceable(text: str, field: str) -> bool:
        if not text:
            return True
        if fingerprint_etiology(text, fps[field]) is not None:
            return True
        return any(sig in text for sig in STUB_SIGNATURES)

    rows = conn.execute("SELECT id, species, name, name_ja, causes_ja, pathophysiology_ja FROM diseases").fetchall()
    n = 0
    for row in rows:
        curated = curated_etiology(row["species"] or "", row["name_ja"] or "", row["name"] or "")
        if not curated:
            continue
        for field, new_val in curated.items():
            if _replaceable(row[field] or "", field) and new_val != (row[field] or ""):
                conn.execute(
                    f"UPDATE diseases SET {field} = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (new_val, row["id"]),
                )
                n += 1
    return n


def regenerate_named_pathogen_etiology(conn) -> dict[str, int]:
    """Give named-pathogen viral diseases pathogen-specific causes / pathophysiology.

    Diseases whose name identifies the virus (parvovirus, herpesvirus, rabies …)
    otherwise carry the generic viral category template. The JSON pass
    (fix_named_pathogens.py) handles overlay entries; this served-DB safety net
    catches module/supplementary-sourced records. Fields are replaced only when
    they hold a recognised category template or stub, so curated prose is kept
    (and a curated JA field with a still-templated EN field gets only the EN
    upgraded)."""
    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.bacterial_library import (
        bacterial_clinical_fields,
        resolve_bacterial_agent,
    )
    from scripts.template_elimination.clinical_fields_generator import (
        build_etiology_fingerprints,
        fingerprint_etiology,
        gen_causes_ja,
        gen_pathophysiology_ja,
    )
    from scripts.template_elimination.curated_etiology import STUB_SIGNATURES
    from scripts.template_elimination.fungal_library import (
        fungal_clinical_fields,
        resolve_fungal_agent,
    )
    from scripts.template_elimination.nutritional_library import (
        nutrient_clinical_fields,
        resolve_nutrient_agent,
    )
    from scripts.template_elimination.parasite_library import (
        parasite_clinical_fields,
        resolve_parasite_agent,
    )
    from scripts.template_elimination.pathogen_library import (
        GENERIC_CAUSES_EN_MARKS,
        GENERIC_CAUSES_JA_MARKS,
        GENERIC_PATHO_EN_MARKS,
        resolve_viral_agent,
        viral_clinical_fields,
    )

    def _resolve(nj, ne):
        return (
            resolve_viral_agent(nj, ne)
            or resolve_bacterial_agent(nj, ne)
            or resolve_fungal_agent(nj, ne)
            or resolve_parasite_agent(nj, ne)
            or resolve_nutrient_agent(nj, ne)
        )

    def _fields(sp, nj, ne):
        return (
            viral_clinical_fields(sp, nj, ne)
            or bacterial_clinical_fields(sp, nj, ne)
            or fungal_clinical_fields(sp, nj, ne)
            or parasite_clinical_fields(sp, nj, ne)
            or nutrient_clinical_fields(sp, nj, ne)
        )

    causes_fps = build_etiology_fingerprints(gen_causes_ja)
    patho_fps = build_etiology_fingerprints(gen_pathophysiology_ja)
    CAUSES_JA_MARKS = GENERIC_CAUSES_JA_MARKS
    CAUSES_EN_MARKS = GENERIC_CAUSES_EN_MARKS
    PATHO_JA_MARKS = ("病態生理はウイルス侵入", "病原ウイルスは特異的細胞受容体")
    PATHO_EN_MARKS = GENERIC_PATHO_EN_MARKS

    def _ja_ok(text, fps, marks):
        if not text:
            return True
        if fingerprint_etiology(text, fps) is not None:
            return True
        if any(s in text for s in STUB_SIGNATURES):
            return True
        return any(m in text for m in marks)

    def _en_ok(text, marks):
        if not text:
            return True
        low = text.lower()
        return any(m in low for m in marks)

    rows = conn.execute(
        "SELECT id, species, name, name_ja, causes_ja, causes, pathophysiology_ja, pathophysiology FROM diseases"
    ).fetchall()
    counts = {"causes_ja": 0, "causes": 0, "pathophysiology_ja": 0, "pathophysiology": 0}
    for row in rows:
        if _resolve(row["name_ja"] or "", row["name"] or "") is None:
            continue
        fields = _fields((row["species"] or "").lower(), row["name_ja"] or "", row["name"] or "")
        if not fields:
            continue
        checks = {
            "causes_ja": _ja_ok(row["causes_ja"] or "", causes_fps, CAUSES_JA_MARKS),
            "causes": _en_ok(row["causes"] or "", CAUSES_EN_MARKS),
            "pathophysiology_ja": _ja_ok(row["pathophysiology_ja"] or "", patho_fps, PATHO_JA_MARKS),
            "pathophysiology": _en_ok(row["pathophysiology"] or "", PATHO_EN_MARKS),
        }
        for field, ok in checks.items():
            if ok and fields[field] != (row[field] or ""):
                conn.execute(
                    f"UPDATE diseases SET {field} = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (fields[field], row["id"]),
                )
                counts[field] += 1
    return counts


def recategorize_etiology_fields(conn) -> dict[str, int]:
    """Fix causes_ja / pathophysiology_ja that carry the WRONG category template.

    Two failure modes are corrected on the served database:

    * **Mis-categorised etiology** — e.g. ferret adrenal disease received the
      *renal* causes template (``Adrenal`` contains ``renal``), retained fetus
      and anaesthetic complications received the *toxicity* template. The
      category template currently applied is fingerprinted, the correct category
      is resolved from the disease name, and a confident contradiction triggers
      regeneration with the right category.
    * **Cross-species toxin examples** — the toxicity causes template formerly
      listed dog/cat toxins (chocolate, lily) for every species. Every entry that
      keeps the toxicity category is re-rendered so its toxin examples match the
      animal actually being treated.

    Curated / disease-specific text (no recognised category template) is left
    untouched, so no hand-written content is overwritten.
    """
    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.clinical_fields_generator import (
        build_etiology_fingerprints,
        decide_etiology_category,
        fingerprint_etiology,
        gen_causes_ja,
        gen_pathophysiology_ja,
    )

    fps = {
        "causes_ja": (build_etiology_fingerprints(gen_causes_ja), gen_causes_ja),
        "pathophysiology_ja": (
            build_etiology_fingerprints(gen_pathophysiology_ja),
            gen_pathophysiology_ja,
        ),
    }

    rows = conn.execute("SELECT id, species, name, name_ja, causes_ja, pathophysiology_ja FROM diseases").fetchall()

    counts = {"recategorized": 0, "toxicity_respeciated": 0}
    for row in rows:
        species = (row["species"] or "").lower()
        name_ja = row["name_ja"] or ""
        name_en = row["name"] or ""
        for field, (fingerprints, gen_fn) in fps.items():
            text = row[field] or ""
            applied = fingerprint_etiology(text, fingerprints)
            if applied is None:
                continue  # curated / disease-specific — leave alone
            target = decide_etiology_category(name_ja, name_en, applied)
            if target != applied:
                new = gen_fn(target, name_ja, species)
                if new and new != text:
                    conn.execute(
                        f"UPDATE diseases SET {field} = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                        (new, row["id"]),
                    )
                    counts["recategorized"] += 1
            elif applied == "toxicity" and field == "causes_ja":
                # Same category, but re-render to drop cross-species toxin
                # examples in favour of species-appropriate ones.
                new = gen_fn("toxicity", name_ja, species)
                if new and new != text:
                    conn.execute(
                        f"UPDATE diseases SET {field} = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                        (new, row["id"]),
                    )
                    counts["toxicity_respeciated"] += 1
    return counts


def main(db_path: str | None = None):
    print("=" * 60)
    print("VetDict Data Migration → SQLite")
    print("=" * 60)

    init_db(db_path)

    with get_connection(db_path) as conn:
        total_diseases = 0
        total_symptoms = 0

        # Dog (special module)
        print("\n[dog] migrating diseases...")
        n = migrate_dog_diseases(conn)
        print(f"  → {n} diseases")
        total_diseases += n

        # Equine (special structure)
        print("\n[horse] migrating diseases...")
        n = migrate_equine(conn)
        print(f"  → {n} diseases")
        total_diseases += n

        ns = migrate_equine_symptoms(conn)
        print(f"  → {ns} symptoms")
        total_symptoms += ns

        # All other species
        for species_key, module_path in sorted(SPECIES_MODULES.items()):
            print(f"\n[{species_key}] migrating diseases...")
            n = migrate_species_diseases(conn, species_key, module_path)
            print(f"  → {n} diseases")
            total_diseases += n

            ns = migrate_species_symptoms(conn, species_key, module_path)
            print(f"  → {ns} symptoms")
            total_symptoms += ns

        # JSON enrichments overlay (name-based matching)
        print("\n[enrichment] overlaying JSON enrichments (name-based)...")
        n = migrate_json_enrichments(conn)
        print(f"  → {n} diseases enriched from JSON")

        # Template-based enrichment for remaining gaps
        print("\n[enrichment] filling missing treatment/prevention/prognosis...")
        enrich_stats = enrich_missing_fields(conn)
        print(f"  → treatment:  {enrich_stats['treatment']} generated")
        print(f"  → prevention: {enrich_stats['prevention']} generated")
        print(f"  → prognosis:  {enrich_stats['prognosis']} generated")

        # Replace cross-disease template clinical fields that survive in
        # module-sourced entries (no JSON overlay) with disease-specific text.
        print("\n[enrichment] regenerating cross-disease template clinical fields...")
        regen_stats = regenerate_cross_disease_templates(conn)
        for field, n in regen_stats.items():
            print(f"  → {field}: {n} regenerated")

        # Ground templated prevention/prognosis text on each disease's own
        # presenting signs so surveillance/monitoring targets differ per disease.
        print("\n[enrichment] grounding templated prevention/prognosis on disease signs...")
        ground_stats = ground_templated_fields_with_signs(conn)
        for field, n in ground_stats.items():
            print(f"  → {field}: {n} grounded with disease-specific signs")

        # Repair the "in <species>s's prognosis" double-possessive grammar bug
        # in any prognosis text materialised from module/supplementary sources.
        prog_fix = fix_prognosis_possessive_en(conn)
        print(f"  → {prog_fix} English prognosis possessives repaired")

        # Localise any English species placeholders that leaked into JA fields.
        print("\n[enrichment] localising English species names in Japanese fields...")
        loc_n = localize_english_species_in_served_db(conn)
        print(f"  → {loc_n} English species tokens localised")

        # Correct clinically dangerous treatment templates (deworming on
        # rickettsial bacteria, chemotherapy on benign cysts/polyps) that
        # survive in module/supplementary-sourced entries.
        print("\n[enrichment] correcting dangerous treatment miscategorisations...")
        tx_fix = fix_dangerous_treatment_in_served_db(conn)
        for klass, n in tx_fix.items():
            print(f"  → {klass}: {n} treatments corrected")

        # Replace the remaining dangerous *category* mismatches the fallback
        # generator cannot fix (toxin-decontamination on dysbiosis/ulcer/anaemia,
        # deworming on a cerebral infarct / rectal prolapse) with curated,
        # condition-specific, species-appropriate protocols.
        cur_n = apply_curated_dangerous_treatments(conn)
        print(f"  → {cur_n} curated treatment replacements")

        # Replace the deworming template on protozoal diseases (babesiosis,
        # toxoplasmosis, cytauxzoonosis, coccidiosis, …) with evidence-based
        # antiprotozoal protocols — anthelmintics do not treat protozoa.
        proto = regenerate_protozoal_treatments(conn)
        print(
            f"  → {proto['treatment']} protozoal treatments corrected "
            f"({proto['pathophysiology_ja']} JA / {proto['pathophysiology']} EN pathophysiology)"
        )

        # Supply curated etiology/pathophysiology for multifactorial diseases
        # (laminitis, hepatic fibrosis) that resist single-category templating.
        cur_e = apply_curated_etiology(conn)
        print(f"  → {cur_e} curated etiology/pathophysiology replacements")

        # Named-pathogen diseases — viral (parvovirus, herpesvirus, rabies, …) and
        # bacterial (salmonella, tetanus, strangles, …): replace the generic
        # viral/bacterial category template with pathogen-specific causes /
        # pathophysiology (JA+EN). Catches module-sourced entries the JSON pass
        # (fix_named_pathogens.py) cannot reach.
        vir = regenerate_named_pathogen_etiology(conn)
        print(
            f"  → named-pathogen etiology: causes {vir['causes_ja']} JA / {vir['causes']} EN, "
            f"pathophysiology {vir['pathophysiology_ja']} JA / {vir['pathophysiology']} EN"
        )

        # Correct miscategorised causes_ja / pathophysiology_ja (e.g. ferret
        # adrenal disease tagged renal, non-toxicoses tagged toxicity) and drop
        # cross-species toxin examples from the toxicity etiology template.
        print("\n[enrichment] re-categorising etiology / pathophysiology fields...")
        recat = recategorize_etiology_fields(conn)
        print(f"  → {recat['recategorized']} fields re-categorised")
        print(f"  → {recat['toxicity_respeciated']} toxicity etiologies re-speciated")

        # Drugs
        print("\n[drugs] migrating drug dictionary...")
        n = migrate_drugs(conn)
        print(f"  → {n} drugs")

        # Summary
        total_count = conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
        drug_count = conn.execute("SELECT COUNT(*) FROM drugs").fetchone()[0]
        symptom_count = conn.execute("SELECT COUNT(*) FROM symptoms").fetchone()[0]

        # Field coverage report
        t_count = conn.execute(
            "SELECT COUNT(*) FROM diseases WHERE treatment IS NOT NULL AND treatment != ''"
        ).fetchone()[0]
        p_count = conn.execute(
            "SELECT COUNT(*) FROM diseases WHERE prevention IS NOT NULL AND prevention != ''"
        ).fetchone()[0]
        pr_count = conn.execute(
            "SELECT COUNT(*) FROM diseases WHERE prognosis IS NOT NULL AND prognosis != ''"
        ).fetchone()[0]

        print("\n" + "=" * 60)
        print("Migration complete!")
        print(f"  Diseases:    {total_count}")
        print(f"  Symptoms:    {symptom_count}")
        print(f"  Drugs:       {drug_count}")
        print(f"  Treatment:   {t_count}/{total_count} ({100 * t_count // total_count}%)")
        print(f"  Prevention:  {p_count}/{total_count} ({100 * p_count // total_count}%)")
        print(f"  Prognosis:   {pr_count}/{total_count} ({100 * pr_count // total_count}%)")
        print("=" * 60)

        # Write lightweight species counts JSON for runtime fallback (avoids
        # loading all species modules into memory — 550MB peak → <1 KB file).
        species_counts = {}
        for row in conn.execute("SELECT species, COUNT(*) AS cnt FROM diseases GROUP BY species").fetchall():
            species_counts[row[0]] = row[1]
        drug_species_counts = {}
        for row in conn.execute("SELECT species, COUNT(*) AS cnt FROM drug_species_info GROUP BY species").fetchall():
            drug_species_counts[row[0]] = row[1]
        counts_data = {
            "disease_counts": species_counts,
            "drug_counts": drug_species_counts,
            "total_drugs": drug_count,
        }
        counts_path = Path(db_path or DB_PATH).parent / "species_counts.json"
        counts_path.write_text(json.dumps(counts_data, ensure_ascii=False))
        print(f"  Species counts written to {counts_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate VetDict data to SQLite")
    parser.add_argument("--db-path", default=None, help="SQLite database path")
    args = parser.parse_args()
    main(args.db_path)
