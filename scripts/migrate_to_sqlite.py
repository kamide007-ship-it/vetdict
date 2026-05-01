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

from api.database import get_connection, init_db, upsert_disease, upsert_drug, upsert_symptom

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

    # Build a lookup by normalised English name for name-based matching.
    import re

    def _norm(name: str) -> str:
        return re.sub(r"\s+", " ", name.strip().lower())

    json_by_name: dict[str, dict] = {}
    for entry in entries:
        name = entry.get("name", "")
        if name:
            json_by_name[_norm(name)] = entry

    def _clean(value: str | None) -> str | None:
        """Return None for template text so COALESCE keeps existing data."""
        if _is_template_text(value):
            return None
        return value

    # Iterate over all diseases currently in SQLite and enrich where names match.
    rows = conn.execute("SELECT id, name FROM diseases").fetchall()
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
        db_id, db_name = row["id"], row["name"]
        entry = json_by_name.get(_norm(db_name))
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
        "keywords": ["bacteria", "bacterial", "abscess", "cellulitis", "sepsis", "streptococ", "staphylococ", "leptospir", "pasteurell", "bordetella", "mycoplasm"],
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
        "keywords": ["parasite", "parasitic", "worm", "helminth", "mite", "lice", "tick", "flea", "coccidia", "giardia", "mange", "scabies", "tapeworm", "pinworm", "roundworm"],
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
        "keywords": ["diabetes", "obesity", "thyroid", "hyperthyroid", "hypothyroid", "cushing", "addison", "metabolic", "ketoacid", "lipidosis", "hepatic lipid"],
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
        "keywords": ["cancer", "tumor", "tumour", "neoplasm", "carcinoma", "lymphoma", "melanoma", "sarcoma", "adenocarcinoma", "fibrosarcoma", "mast cell"],
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
        "keywords": ["deficiency", "malnutrition", "nutritional", "vitamin", "calcium", "phosphorus", "metabolic bone", "rickets", "scurvy"],
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
        "keywords": ["respiratory", "lung", "pneumonia", "bronch", "asthma", "airway", "pleural", "trachea", "rhinitis", "sinusitis", "dyspnea"],
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
        "keywords": ["gastrointestinal", "diarrhea", "vomiting", "enteritis", "colitis", "ibd", "pancreatitis", "gastritis", "bloat", "obstruction", "ileus", "constipation", "prolapse", "intussusception", "megacolon"],
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
        "keywords": ["dermatitis", "skin", "allergic", "mange", "ringworm", "fungal", "alopecia", "pyoderma", "pododermatitis", "bumblefoot"],
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
        "keywords": ["urinary", "kidney", "renal", "bladder", "calculi", "urolithiasis", "cystitis", "nephritis", "flutd"],
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
        "keywords": ["cardiac", "heart", "cardiovascular", "cardiomyopathy", "murmur", "arrhythmia", "thromboembolism", "endocard"],
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
        "keywords": ["seizure", "epilepsy", "neurologic", "neurological", "paralysis", "paresis", "vestibular", "neuropathy", "encephalitis", "meningitis"],
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
        "keywords": ["fracture", "arthritis", "osteo", "bone", "joint", "luxation", "dislocation", "dysplasia", "spondyl", "ligament", "tendon", "lameness"],
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
        "keywords": ["eye", "ocular", "conjunctiv", "cataract", "glaucoma", "ulcer", "keratitis", "uveitis", "proptosis", "entropion", "ectropion"],
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
        "keywords": ["reproductive", "uterine", "pyometra", "dystocia", "mastitis", "testicular", "ovarian", "pregnancy", "prolapse"],
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
        "neoplastic", "metabolic", "musculoskeletal", "ophthalmic", "dental",
        "reproductive", "neurologic", "cardiovascular", "urinary",
        "dermatologic", "gastrointestinal", "respiratory", "nutritional",
        "infectious_viral", "infectious_bacterial", "parasitic",
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

        # Drugs
        print("\n[drugs] migrating drug dictionary...")
        n = migrate_drugs(conn)
        print(f"  → {n} drugs")

        # Summary
        total_count = conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
        drug_count = conn.execute("SELECT COUNT(*) FROM drugs").fetchone()[0]
        symptom_count = conn.execute("SELECT COUNT(*) FROM symptoms").fetchone()[0]

        # Field coverage report
        t_count = conn.execute("SELECT COUNT(*) FROM diseases WHERE treatment IS NOT NULL AND treatment != ''").fetchone()[0]
        p_count = conn.execute("SELECT COUNT(*) FROM diseases WHERE prevention IS NOT NULL AND prevention != ''").fetchone()[0]
        pr_count = conn.execute("SELECT COUNT(*) FROM diseases WHERE prognosis IS NOT NULL AND prognosis != ''").fetchone()[0]

        print("\n" + "=" * 60)
        print("Migration complete!")
        print(f"  Diseases:    {total_count}")
        print(f"  Symptoms:    {symptom_count}")
        print(f"  Drugs:       {drug_count}")
        print(f"  Treatment:   {t_count}/{total_count} ({100*t_count//total_count}%)")
        print(f"  Prevention:  {p_count}/{total_count} ({100*p_count//total_count}%)")
        print(f"  Prognosis:   {pr_count}/{total_count} ({100*pr_count//total_count}%)")
        print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate VetDict data to SQLite")
    parser.add_argument("--db-path", default=None, help="SQLite database path")
    args = parser.parse_args()
    main(args.db_path)
