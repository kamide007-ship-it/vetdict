#!/usr/bin/env python3
"""Enrich all diseases in diseases_all_species.json with category-specific content.

This script classifies each disease into a veterinary category and generates
detailed, disease-specific pathophysiology, causes, treatment, diagnosis,
prevention, and prognosis content in both English and Japanese.
"""

import json
import os
import re
import sys
from collections import Counter
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, "diseases_all_species.json")

# ============================================================================
# Disease category classifier
# ============================================================================

_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "viral": [
        "virus", "viral", "herpes", "parvo", "corona", "distemper", "influenza",
        "calici", "retrovirus", "adenovirus", "polyoma", "pox", "borna",
        "paramyxo", "rotavirus", "nidovirus", "reovirus", "fiv", "felv",
        "hiv", "rabies", "myxomato", "ebola", "west nile", "encephalomyelit",
    ],
    "bacterial": [
        "bacterial", "bacteria", "streptococc", "staphylococc", "clostrid",
        "pasteurell", "bordetella", "mycobacter", "salmonell", "leptospir",
        "chlamyd", "bartonell", "helicobacter", "campylobacter", "e. coli",
        "escherichia", "borrelios", "tyzzer", "abscess", "pyometra", "septic",
        "otitis", "kennel cough", "strangles", "glanders", "actinomyc",
        "nocardia", "erysipel", "brucell", "listeria", "psittacosis",
    ],
    "fungal": [
        "fungal", "fungus", "mycosis", "aspergill", "candida", "dermatophyt",
        "ringworm", "malassezia", "cryptococcus", "histoplasm", "blastomyc",
        "sporotrich", "zygomyc", "mucormyc", "saprolegn", "chromomyc",
        "megabacteriosis", "macrorhabdus",
    ],
    "parasitic": [
        "parasit", "mite", "flea", "tick", "worm", "coccidia", "giardia",
        "cryptosporid", "toxoplasm", "mange", "demodex", "sarcoptes",
        "encephalitozoon", "nematode", "cestode", "trematode", "hookworm",
        "roundworm", "whipworm", "heartworm", "pinworm", "tapeworm",
        "strongyl", "ascarid", "cuterebra", "myiasis", "flystrike",
        "acariasis", "cheyletiella", "caparinia", "ixodes", "babesia",
        "leishmania", "trypanosoma", "theileria", "haemoproteus",
    ],
    "neoplastic": [
        "tumor", "tumour", "cancer", "neoplas", "carcinoma", "lymphoma",
        "sarcoma", "melanoma", "adenoma", "fibroma", "lipoma", "mesothelioma",
        "hemangio", "mast cell", "leukemia", "malignant", "benign mass",
        "thymoma", "insulinoma", "pheochromocytoma", "osteosarcoma",
        "chondrosarcoma", "squamous cell", "basal cell", "schwannoma",
        "meningioma", "glioma", "seminoma", "leiomyoma",
    ],
    "metabolic": [
        "metaboli", "diabet", "hypothyroid", "hyperthyroid", "cushing",
        "addison", "hypoglycemia", "hyperglycemia", "ketoacidosis",
        "hypercalcemia", "hypocalcemia", "hyperkalemia", "hypokalemia",
        "acidosis", "alkalosis", "gout", "amyloid", "hemochromatosis",
        "insulin", "adrenal", "pituitary", "thyroid", "hyperparathyroid",
        "hypoparathyroid", "hepatic lipidosis", "fatty liver", "lipidosis",
    ],
    "nutritional": [
        "deficien", "nutrit", "vitamin", "malnutrit", "hypovitamin",
        "hypervitamin", "scurvy", "rickets", "mbd", "calcium", "phosphorus",
        "iodine", "iron storage", "obesity", "anorexia", "cachexia",
        "thiamine", "selenium", "copper", "zinc defic",
    ],
    "toxic": [
        "toxic", "poison", "toxicosis", "intoxicat", "envenomation",
        "aflatoxin", "lead poison", "zinc toxic", "organophosph",
        "anticoagulant rodenticide", "plant toxic", "heavy metal",
        "pyrethrin", "ivermectin toxic", "nsaid toxic", "chocolate",
        "xylitol", "lily toxic", "acetaminophen",
    ],
    "traumatic": [
        "trauma", "fracture", "injury", "wound", "burn", "bite wound",
        "laceration", "contusion", "luxation", "dislocation", "prolapse",
        "rupture", "perforation", "tear", "avulsion", "foreign body",
        "heatstroke", "hypothermia", "frostbite", "drowning", "electrocution",
        "shell fracture", "beak fracture", "tail degloving",
    ],
    "dental": [
        "dental", "tooth", "molar", "incisor", "periodontal", "malocclusion",
        "slobbers", "stomatitis", "gingivitis", "oral mass", "epulis",
        "tooth root", "dental abscess", "jaw", "mandibular", "maxillary",
    ],
    "autoimmune": [
        "autoimmun", "immune-mediat", "pemphigus", "lupus", "immunodeficien",
        "allergic", "allergy", "atopic", "anaphyla", "hypersensitiv",
        "immune thrombocytopenia", "imha", "itp", "myasthenia",
    ],
    "cardiovascular": [
        "cardiac", "heart", "cardiomyopath", "arrhythm", "murmur",
        "pericardial", "endocardit", "congestive", "hypertension",
        "thromboembol", "aortic", "mitral", "tricuspid", "atrial",
        "ventricular", "myocarditis", "vasculitis",
    ],
    "respiratory": [
        "pneumonia", "respiratory", "bronchit", "asthma", "pleural",
        "rhinitis", "sinusitis", "tracheitis", "dyspnea", "pulmonary",
        "pneumothorax", "pyothorax", "aspiration", "tracheal collapse",
        "laryngeal", "brachycephalic airway",
    ],
    "renal": [
        "renal", "kidney", "nephrit", "urolithiasis", "cystitis", "urinary",
        "bladder", "urolith", "nephropathy", "glomerulo", "pyelonephrit",
        "hydronephrosis", "polycystic kidney", "ckd", "aki",
    ],
    "gastrointestinal": [
        "gastric", "intestin", "enteritis", "colitis", "bloat", "stasis",
        "ileus", "obstruct", "impaction", "constipat", "diarrhea",
        "gastroenter", "pancreatit", "hepatic", "liver", "cholangitis",
        "megacolon", "intussusception", "cecal", "crop", "proventric",
        "cloac", "esophag", "megaesophagus", "regurgit",
    ],
    "reproductive": [
        "reproduct", "dystocia", "mastitis", "metritis", "pregnancy",
        "testicular", "ovarian", "uterine", "mammary", "eclampsia",
        "infertil", "egg binding", "egg yolk", "penile", "vaginal",
        "vulvar", "cryptorchid", "phimosis", "paraphimosis",
    ],
    "neurological": [
        "neurolog", "seizure", "epilepsy", "vestibular", "encephalit",
        "meningit", "neuropath", "paralysis", "paresis", "ataxia",
        "myelopath", "intervertebral", "ivdd", "disc disease", "spondylosis",
        "head tilt", "tremor", "torticollis", "hydrocephalus", "syringomyelia",
    ],
    "dermatological": [
        "dermatit", "skin", "alopecia", "pyoderma", "folliculit",
        "acne", "sebaceous", "eczema", "pruritus", "hot spot",
        "pododermatit", "bumblefoot", "shell rot", "scale rot",
        "feather cyst", "xanthoma", "cutaneous",
    ],
    "ophthalmic": [
        "ophthalm", "cataract", "glaucoma", "uveitis", "corneal",
        "conjunctivit", "keratitis", "eye", "retinal", "proptosis",
        "entropion", "ectropion", "cherry eye", "iris", "lens luxation",
        "panophthalmitis", "dacryocystitis",
    ],
    "orthopedic": [
        "arthrit", "osteo", "dysplasia", "luxat", "tendon", "ligament",
        "lameness", "laminitis", "navicular", "spavin", "splint",
        "bone", "joint", "synovitis", "bursitis", "cruciate",
        "patellar", "hip", "elbow", "spondyl", "kyphosis", "lordosis",
        "pyramiding",
    ],
    "congenital": [
        "congeni", "genetic", "heredit", "inherited", "developmental",
        "portosystemic shunt", "cleft", "atresia", "ectopic", "patent ductus",
        "megaesophagus congenital", "polydactyly",
    ],
    "behavioral": [
        "behavior", "stress", "anxiety", "aggression", "self-mutilat",
        "feather pluck", "fur chew", "bar chew", "pica", "stereotyp",
        "overgrooming", "compulsive", "phobia", "separation anxiety",
    ],
}


def classify_disease(name: str, desc: str) -> str:
    """Classify a disease into a veterinary category."""
    combined = (name + " " + desc).lower()
    for category, keywords in _CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in combined:
                return category
    return "general"


# ============================================================================
# Category-specific content templates
# ============================================================================

# Each category has templates for: pathophysiology, causes, treatment,
# diagnosis, prevention, prognosis (English + Japanese)

_PATHO_TEMPLATES: dict[str, tuple[str, str]] = {
    "viral": (
        "{name} is caused by viral infection in {species}. {desc} "
        "The virus enters host cells through specific receptor-mediated mechanisms, "
        "hijacking cellular machinery for replication. This leads to direct cytopathic effects "
        "including cell lysis, apoptosis, and tissue necrosis in target organs. "
        "The host immune response—involving both innate (interferons, NK cells) and "
        "adaptive (antibody, cell-mediated) pathways—may contribute to immunopathology. "
        "Viremia can disseminate the pathogen to multiple organ systems, and immunosuppression "
        "may predispose to secondary bacterial or fungal infections.",
        "{name_ja}は{species}におけるウイルス感染症である。"
        "ウイルスは特定の受容体を介して宿主細胞に侵入し、細胞内機構を利用して複製する。"
        "直接的な細胞変性効果（細胞溶解、アポトーシス、標的臓器の組織壊死）を引き起こす。"
        "自然免疫（インターフェロン、NK細胞）および適応免疫（抗体、細胞性免疫）の宿主免疫応答が"
        "免疫病理に寄与することがある。ウイルス血症により病原体が複数の臓器系に播種される可能性があり、"
        "免疫抑制により二次的な細菌・真菌感染のリスクが高まる。"
    ),
    "bacterial": (
        "{name} is a bacterial infection in {species}. {desc} "
        "Pathogenic bacteria colonize tissues through adhesion factors and invade "
        "via virulence mechanisms including toxin production, enzyme secretion, and "
        "immune evasion strategies. The resulting inflammatory cascade involves "
        "neutrophil infiltration, cytokine release, and complement activation. "
        "Tissue damage results from both direct bacterial action and the host's "
        "inflammatory response. Abscess formation, septicemia, or chronic granulomatous "
        "inflammation may develop depending on the organism and host immune status.",
        "{name_ja}は{species}における細菌感染症である。"
        "病原菌は付着因子を通じて組織にコロニーを形成し、毒素産生、酵素分泌、"
        "免疫回避戦略などの病原性メカニズムを介して侵入する。"
        "好中球浸潤、サイトカイン放出、補体活性化を含む炎症カスケードが生じる。"
        "組織損傷は細菌の直接作用と宿主の炎症反応の両方に起因する。"
        "菌種と宿主の免疫状態に応じて、膿瘍形成、敗血症、または慢性肉芽腫性炎症が発生しうる。"
    ),
    "fungal": (
        "{name} is a fungal infection in {species}. {desc} "
        "Fungal organisms establish infection through spore inhalation, direct inoculation, "
        "or mucosal colonization. Hyphae or yeast forms penetrate tissues via enzymatic "
        "degradation and mechanical pressure, eliciting a granulomatous inflammatory response. "
        "Immunocompromised individuals are particularly susceptible. The infection may remain "
        "localized or disseminate hematogenously to distant organs. Chronic infections can "
        "lead to fibrosis, tissue remodeling, and progressive organ dysfunction.",
        "{name_ja}は{species}における真菌感染症である。"
        "真菌は胞子吸入、直接接種、または粘膜コロニー形成を通じて感染を確立する。"
        "菌糸または酵母形態が酵素分解と機械的圧力により組織に侵入し、"
        "肉芽腫性炎症反応を惹起する。免疫不全個体は特に感受性が高い。"
        "感染は局所にとどまるか、血行性に遠隔臓器へ播種される可能性がある。"
        "慢性感染は線維化、組織リモデリング、進行性臓器機能障害を引き起こしうる。"
    ),
    "parasitic": (
        "{name} is a parasitic condition in {species}. {desc} "
        "The parasite establishes infection through ingestion, percutaneous penetration, "
        "or vector-mediated transmission. It exploits host resources for nutrition and "
        "reproduction while evading immune defenses through antigenic variation, "
        "immunomodulation, or intracellular sequestration. Tissue damage results from "
        "direct parasitic feeding, mechanical disruption, toxic metabolic byproducts, "
        "and the host's inflammatory and immune responses. Heavy parasite burdens can "
        "lead to anemia, malnutrition, organ dysfunction, and secondary infections.",
        "{name_ja}は{species}における寄生虫疾患である。"
        "寄生虫は経口摂取、経皮的侵入、またはベクター媒介伝播を通じて感染を確立する。"
        "抗原変異、免疫調節、細胞内隔離により宿主の免疫防御を回避しながら、"
        "宿主の栄養と資源を利用して増殖する。組織損傷は寄生虫の直接的な摂食、"
        "機械的破壊、有毒代謝副産物、宿主の炎症・免疫応答に起因する。"
        "重度の寄生虫感染は貧血、栄養失調、臓器機能障害、二次感染を引き起こしうる。"
    ),
    "neoplastic": (
        "{name} is a neoplastic condition in {species}. {desc} "
        "Neoplastic transformation occurs through accumulated genetic mutations in "
        "oncogenes, tumor suppressor genes, and DNA repair mechanisms. Uncontrolled "
        "cellular proliferation leads to tumor formation with potential for local "
        "tissue invasion and destruction. Malignant neoplasms may metastasize via "
        "lymphatic or hematogenous routes. Paraneoplastic syndromes—including "
        "hypercalcemia, cachexia, and immune dysregulation—may accompany the "
        "primary tumor and contribute to morbidity.",
        "{name_ja}は{species}における腫瘍性疾患である。"
        "癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積により"
        "腫瘍性形質転換が生じる。制御不能な細胞増殖により腫瘍が形成され、"
        "局所組織への浸潤・破壊の可能性がある。悪性腫瘍はリンパ行性または"
        "血行性に転移しうる。高カルシウム血症、悪液質、免疫調節障害などの"
        "腫瘍随伴症候群が原発腫瘍に伴い、罹患率に寄与することがある。"
    ),
    "metabolic": (
        "{name} is a metabolic/endocrine disorder in {species}. {desc} "
        "The underlying pathology involves dysregulation of hormonal feedback loops, "
        "enzyme activity, or substrate metabolism. This leads to imbalances in "
        "circulating hormone levels, electrolytes, or metabolic intermediates that "
        "affect cellular function across multiple organ systems. Compensatory mechanisms "
        "may temporarily maintain homeostasis but eventually decompensate, leading to "
        "progressive clinical deterioration and multi-organ effects.",
        "{name_ja}は{species}における代謝・内分泌疾患である。"
        "基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の"
        "調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が"
        "複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に"
        "恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と"
        "多臓器への影響を引き起こす。"
    ),
    "nutritional": (
        "{name} is a nutritional disorder in {species}. {desc} "
        "The condition results from inadequate intake, malabsorption, or excessive "
        "supplementation of specific nutrients. Deficiency states impair biochemical "
        "pathways dependent on the affected nutrient as cofactor or substrate, leading "
        "to cellular dysfunction. Excess states cause toxicity through accumulation in "
        "tissues or disruption of nutrient interactions. Species-specific dietary "
        "requirements make proper nutritional management critical for prevention.",
        "{name_ja}は{species}における栄養障害である。"
        "特定の栄養素の不十分な摂取、吸収不良、または過剰摂取により生じる。"
        "欠乏状態では、影響を受けた栄養素を補因子または基質として必要とする"
        "生化学的経路が障害され、細胞機能障害を引き起こす。"
        "過剰状態では組織への蓄積や栄養素間相互作用の障害により毒性が生じる。"
        "種特異的な食事要求により、適切な栄養管理が予防に不可欠である。"
    ),
    "toxic": (
        "{name} is a toxicological condition in {species}. {desc} "
        "Toxic injury occurs through ingestion, inhalation, or dermal absorption of "
        "the offending agent. The toxin disrupts cellular processes through specific "
        "mechanisms such as enzyme inhibition, receptor interference, oxidative damage, "
        "or direct cytotoxicity. Target organs vary by toxin but commonly include the "
        "liver (biotransformation), kidneys (excretion), nervous system, and GI tract. "
        "Dose-dependent effects range from subclinical changes to fulminant organ failure.",
        "{name_ja}は{species}における中毒性疾患である。"
        "有害物質の経口摂取、吸入、または経皮吸収により中毒障害が生じる。"
        "毒素は酵素阻害、受容体干渉、酸化的損傷、直接的な細胞毒性などの"
        "特定のメカニズムを通じて細胞プロセスを障害する。"
        "標的臓器は毒素により異なるが、肝臓（生体内変換）、腎臓（排泄）、"
        "神経系、消化管が一般的である。用量依存的に無症候性変化から"
        "劇症型臓器不全まで幅広い影響を及ぼす。"
    ),
    "traumatic": (
        "{name} is a traumatic/mechanical condition in {species}. {desc} "
        "Tissue damage results from external mechanical forces exceeding the structural "
        "tolerance of affected tissues. The injury triggers an acute inflammatory cascade "
        "with hemorrhage, edema, and pain. Depending on severity, there may be disruption "
        "of vascular supply leading to ischemia, contamination with environmental organisms "
        "leading to infection, and progressive tissue necrosis. The healing response involves "
        "hemostasis, inflammation, proliferation, and remodeling phases.",
        "{name_ja}は{species}における外傷性・機械的疾患である。"
        "罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。"
        "損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。"
        "重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、"
        "進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、"
        "リモデリングの各段階を経る。"
    ),
    "dental": (
        "{name} is a dental/oral condition in {species}. {desc} "
        "Dental pathology in this species involves disruption of normal tooth structure, "
        "alignment, or supporting tissues. Abnormal tooth growth or wear patterns can lead "
        "to malocclusion, root elongation, and periapical abscess formation. "
        "Periodontal disease involves bacterial biofilm accumulation, gingival inflammation, "
        "and progressive loss of periodontal attachment. Pain from dental disease often "
        "manifests as reduced food intake, selective eating, weight loss, and ptyalism.",
        "{name_ja}は{species}における歯科・口腔疾患である。"
        "歯の構造、配列、または支持組織の正常な機能が障害される。"
        "異常な歯の成長・摩耗パターンは不正咬合、歯根伸長、根尖膿瘍形成を"
        "引き起こしうる。歯周病は細菌バイオフィルムの蓄積、歯肉炎症、"
        "歯周付着の進行性喪失を伴う。歯科疾患による疼痛は食欲低下、"
        "選択的摂食、体重減少、流涎として現れることが多い。"
    ),
    "autoimmune": (
        "{name} is an immune-mediated condition in {species}. {desc} "
        "The immune system mounts an aberrant response against self-antigens or "
        "environmental allergens. In autoimmune disease, loss of self-tolerance leads "
        "to antibody- or cell-mediated destruction of host tissues. In allergic disease, "
        "IgE-mediated or delayed-type hypersensitivity reactions cause tissue inflammation. "
        "The chronic inflammatory process involves T-cell dysregulation, autoantibody "
        "production, complement activation, and progressive tissue damage in target organs.",
        "{name_ja}は{species}における免疫介在性疾患である。"
        "免疫系が自己抗原または環境アレルゲンに対して異常な応答を起こす。"
        "自己免疫疾患では自己寛容の喪失により抗体または細胞性免疫による"
        "宿主組織の破壊が生じる。アレルギー疾患ではIgE介在性または"
        "遅延型過敏反応により組織炎症が生じる。慢性炎症過程はT細胞調節障害、"
        "自己抗体産生、補体活性化、標的臓器の進行性組織損傷を伴う。"
    ),
    "cardiovascular": (
        "{name} is a cardiovascular disorder in {species}. {desc} "
        "The cardiac pathology involves structural or functional abnormalities of the "
        "heart, great vessels, or peripheral vasculature. Impaired cardiac output, "
        "valvular dysfunction, or rhythm disturbances compromise tissue perfusion. "
        "Compensatory mechanisms (neurohormonal activation, ventricular remodeling) "
        "may temporarily maintain function but lead to progressive myocardial "
        "deterioration. Heart failure, thromboembolism, and sudden death are "
        "potential consequences of advanced disease.",
        "{name_ja}は{species}における循環器疾患である。"
        "心臓、大血管、または末梢血管系の構造的・機能的異常を伴う。"
        "心拍出量の低下、弁膜機能障害、調律異常により組織灌流が障害される。"
        "代償機構（神経ホルモン活性化、心室リモデリング）が一時的に機能を維持するが、"
        "進行性の心筋劣化を引き起こす。心不全、血栓塞栓症、突然死が"
        "進行期疾患の潜在的結果である。"
    ),
    "respiratory": (
        "{name} is a respiratory disorder in {species}. {desc} "
        "The pathology involves inflammation, obstruction, or compromise of the "
        "airways, lung parenchyma, or pleural space. Impaired gas exchange leads to "
        "hypoxemia and potential hypercapnia. Inflammatory exudates, mucus "
        "accumulation, or structural changes reduce effective ventilation. "
        "Compensatory tachypnea increases work of breathing and metabolic demand. "
        "Severe cases may progress to respiratory failure requiring emergency intervention.",
        "{name_ja}は{species}における呼吸器疾患である。"
        "気道、肺実質、または胸膜腔の炎症、閉塞、または機能障害を伴う。"
        "ガス交換の障害により低酸素血症および高炭酸ガス血症の可能性がある。"
        "炎症性滲出液、粘液蓄積、構造変化が有効な換気を低下させる。"
        "代償性頻呼吸により呼吸仕事量と代謝要求が増加する。"
        "重症例は呼吸不全に進行し緊急介入が必要となりうる。"
    ),
    "renal": (
        "{name} is a renal/urinary disorder in {species}. {desc} "
        "The pathology involves structural or functional impairment of the kidneys, "
        "ureters, bladder, or urethra. Renal disease disrupts glomerular filtration, "
        "tubular reabsorption/secretion, and hormonal functions (erythropoietin, "
        "calcitriol, renin). Progressive nephron loss leads to azotemia, electrolyte "
        "imbalances, and acid-base disturbances. Lower urinary tract disease may "
        "cause obstruction, urolithiasis, or ascending infection.",
        "{name_ja}は{species}における腎・泌尿器疾患である。"
        "腎臓、尿管、膀胱、または尿道の構造的・機能的障害を伴う。"
        "腎疾患は糸球体濾過、尿細管再吸収・分泌、およびホルモン機能"
        "（エリスロポエチン、カルシトリオール、レニン）を障害する。"
        "進行性のネフロン喪失により高窒素血症、電解質異常、酸塩基障害が生じる。"
        "下部尿路疾患は閉塞、尿石症、上行感染を引き起こしうる。"
    ),
    "gastrointestinal": (
        "{name} is a gastrointestinal disorder in {species}. {desc} "
        "The GI pathology involves disruption of mucosal integrity, motility, "
        "secretory function, or microbiome balance. Inflammation damages the epithelial "
        "barrier, leading to malabsorption, fluid loss, and potential bacterial "
        "translocation. Motility disorders (hypomotility/stasis or hypermotility) alter "
        "transit time and digestion efficiency. In hindgut fermenters, disruption of "
        "cecal/colonic flora can trigger fatal dysbiosis and enterotoxemia.",
        "{name_ja}は{species}における消化器疾患である。"
        "粘膜の完全性、運動性、分泌機能、またはマイクロバイオームバランスの"
        "障害を伴う。炎症により上皮バリアが損傷し、吸収不良、体液喪失、"
        "細菌トランスロケーションの可能性がある。運動障害（低運動性/うっ滞または"
        "亢進）により通過時間と消化効率が変化する。後腸発酵動物では盲腸/結腸"
        "フローラの破壊が致死的ディスバイオーシスと腸管毒素症を引き起こしうる。"
    ),
    "reproductive": (
        "{name} is a reproductive disorder in {species}. {desc} "
        "The reproductive pathology involves hormonal imbalances, structural "
        "abnormalities, or infectious processes affecting the reproductive tract. "
        "Dysregulated sex hormones can lead to cystic changes, hyperplasia, or "
        "neoplasia of reproductive organs. Obstetric complications may cause "
        "mechanical obstruction or metabolic derangements threatening both mother "
        "and offspring. Secondary bacterial infection of the reproductive tract "
        "can progress to systemic sepsis.",
        "{name_ja}は{species}における生殖器疾患である。"
        "ホルモンバランスの異常、構造異常、または生殖器への感染過程を伴う。"
        "性ホルモンの調節障害は生殖器官の嚢胞性変化、過形成、または腫瘍形成を"
        "引き起こしうる。産科的合併症は機械的閉塞や代謝異常を引き起こし、"
        "母体と産子の両方を脅かす。生殖器の二次細菌感染は全身性敗血症に"
        "進行しうる。"
    ),
    "neurological": (
        "{name} is a neurological disorder in {species}. {desc} "
        "The neuropathology involves damage to the central or peripheral nervous "
        "system through inflammation, degeneration, compression, or vascular "
        "compromise. Disrupted neural signaling affects motor function, sensory "
        "processing, autonomic regulation, or cognitive status depending on the "
        "anatomical location. Demyelination, axonal degeneration, or neuronal loss "
        "may be irreversible. Increased intracranial pressure from edema or mass "
        "lesions can cause brainstem herniation.",
        "{name_ja}は{species}における神経疾患である。"
        "炎症、変性、圧迫、または血管障害による中枢・末梢神経系の損傷を伴う。"
        "解剖学的位置に応じて運動機能、感覚処理、自律神経調節、"
        "認知状態に影響を及ぼす。脱髄、軸索変性、ニューロン喪失は"
        "不可逆的な場合がある。浮腫や腫瘤性病変による頭蓋内圧亢進は"
        "脳幹ヘルニアを引き起こしうる。"
    ),
    "dermatological": (
        "{name} is a dermatological condition in {species}. {desc} "
        "The skin pathology involves disruption of the epidermal barrier, "
        "dermal inflammation, or adnexal dysfunction. Compromised barrier function "
        "permits transepidermal water loss, allergen penetration, and microbial "
        "colonization. Inflammatory mediators (histamine, prostaglandins, cytokines) "
        "drive pruritus, erythema, and secondary excoriation. Chronic disease leads "
        "to epidermal hyperplasia, lichenification, hyperpigmentation, and fibrosis.",
        "{name_ja}は{species}における皮膚疾患である。"
        "表皮バリア、真皮炎症、または付属器機能の障害を伴う。"
        "バリア機能の低下により経表皮水分喪失、アレルゲン浸透、微生物コロニー形成が"
        "促進される。炎症メディエーター（ヒスタミン、プロスタグランジン、サイトカイン）が"
        "掻痒、紅斑、二次的な擦過傷を駆動する。慢性疾患では表皮過形成、"
        "苔癬化、色素沈着、線維化が生じる。"
    ),
    "ophthalmic": (
        "{name} is an ophthalmic condition in {species}. {desc} "
        "The ocular pathology involves inflammatory, degenerative, or structural "
        "changes affecting the globe, adnexa, or visual pathways. Intraocular "
        "inflammation disrupts the blood-aqueous or blood-retinal barriers, leading "
        "to protein leakage, cellular infiltration, and potential vision loss. "
        "Elevated intraocular pressure damages the optic nerve and retinal ganglion "
        "cells. Corneal ulceration may progress to descemetocele or perforation.",
        "{name_ja}は{species}における眼科疾患である。"
        "眼球、付属器、または視覚経路に影響を及ぼす炎症性、変性、"
        "または構造的変化を伴う。眼内炎症は血液房水関門・血液網膜関門を破壊し、"
        "蛋白漏出、細胞浸潤、視力喪失の可能性がある。眼圧上昇は視神経と"
        "網膜神経節細胞を損傷する。角膜潰瘍はデスメ膜瘤や穿孔に進行しうる。"
    ),
    "orthopedic": (
        "{name} is an orthopedic/musculoskeletal condition in {species}. {desc} "
        "The musculoskeletal pathology involves structural damage, degenerative "
        "changes, or developmental abnormalities of bones, joints, or supporting "
        "soft tissues. Cartilage degradation, subchondral bone remodeling, and "
        "synovial inflammation characterize joint disease. Tendon and ligament "
        "injuries disrupt mechanical stability. Pain, lameness, and reduced "
        "mobility are hallmark clinical features that significantly impact quality of life.",
        "{name_ja}は{species}における整形外科・筋骨格系疾患である。"
        "骨、関節、または支持軟部組織の構造的損傷、変性変化、"
        "発達異常を伴う。軟骨変性、軟骨下骨リモデリング、滑膜炎が"
        "関節疾患を特徴づける。腱・靭帯損傷は機械的安定性を障害する。"
        "疼痛、跛行、運動性低下がQOLに大きく影響する特徴的な臨床徴候である。"
    ),
    "congenital": (
        "{name} is a congenital/genetic condition in {species}. {desc} "
        "The condition results from developmental abnormalities during embryogenesis "
        "or inherited genetic mutations. Structural malformations disrupt normal "
        "organ development and function. Genetic mutations may affect enzyme activity, "
        "structural proteins, or regulatory pathways. Expression may be present at "
        "birth or manifest later as the animal matures. Selective breeding practices "
        "may increase the prevalence of inherited conditions in certain breeds or lines.",
        "{name_ja}は{species}における先天性・遺伝性疾患である。"
        "胚発生中の発達異常または遺伝子変異に起因する。構造的奇形により"
        "正常な臓器の発達と機能が障害される。遺伝子変異は酵素活性、"
        "構造タンパク質、調節経路に影響しうる。出生時に存在するか、"
        "動物の成長に伴い発現する場合がある。選択的交配により"
        "特定の品種・系統で遺伝性疾患の有病率が高まることがある。"
    ),
    "behavioral": (
        "{name} is a behavioral condition in {species}. {desc} "
        "The behavioral pathology involves dysregulation of neurochemical signaling "
        "(serotonin, dopamine, norepinephrine, GABA) in brain circuits governing "
        "emotional regulation, stress response, and learned behaviors. Environmental "
        "stressors, inadequate socialization, inappropriate husbandry, or underlying "
        "medical conditions may trigger or exacerbate behavioral abnormalities. "
        "Chronic stress activates the hypothalamic-pituitary-adrenal axis, leading to "
        "elevated cortisol and immunosuppression.",
        "{name_ja}は{species}における行動疾患である。"
        "情動調節、ストレス応答、学習行動を制御する脳回路における"
        "神経化学的シグナル伝達（セロトニン、ドーパミン、ノルエピネフリン、GABA）の"
        "調節障害を伴う。環境ストレス、不適切な社会化、不適切な飼育管理、"
        "基礎疾患が行動異常を惹起・悪化させることがある。"
        "慢性ストレスは視床下部-下垂体-副腎系を活性化し、"
        "コルチゾール上昇と免疫抑制を引き起こす。"
    ),
}

_TREAT_TEMPLATES: dict[str, tuple[str, str]] = {
    "viral": (
        "Treatment of {name_l} in {species_l} is primarily supportive, as most viral infections "
        "lack specific antiviral therapy. Fluid therapy maintains hydration and corrects "
        "electrolyte imbalances. Antipyretics and analgesics manage fever and discomfort. "
        "Broad-spectrum antibiotics prevent or treat secondary bacterial infections. "
        "Nutritional support—including assisted feeding if anorexic—is essential. "
        "Immunostimulants or interferons may be beneficial in some cases. "
        "Isolation of affected individuals prevents transmission to susceptible contacts.",
        "{species}における{name_ja}の治療は主に支持療法であり、多くのウイルス感染症には"
        "特異的抗ウイルス薬がない。輸液療法により水分補給と電解質補正を行う。"
        "解熱鎮痛薬で発熱と不快感を管理する。広域抗菌薬で二次細菌感染を予防・治療する。"
        "食欲不振時の補助給餌を含む栄養サポートが不可欠である。"
        "免疫賦活剤やインターフェロンが有効な場合がある。"
        "感受性個体への伝播防止のため罹患個体を隔離する。"
    ),
    "bacterial": (
        "Treatment of {name_l} in {species_l} requires targeted antimicrobial therapy based on "
        "culture and sensitivity testing when possible. Empirical broad-spectrum antibiotics are "
        "initiated pending results. Duration of antibiotic therapy should be sufficient to "
        "eliminate infection and prevent resistance. Surgical drainage or debridement may be "
        "necessary for abscesses or necrotic tissue. Supportive care includes fluid therapy, "
        "analgesics, anti-inflammatories, and nutritional support.",
        "{species}における{name_ja}の治療には、可能であれば培養感受性試験に基づく"
        "標的抗菌薬療法が必要である。結果待ちの間は経験的広域抗菌薬を開始する。"
        "抗菌薬治療期間は感染の排除と耐性予防に十分な期間とする。"
        "膿瘍や壊死組織には外科的排膿またはデブリードマンが必要な場合がある。"
        "支持療法として輸液、鎮痛薬、抗炎症薬、栄養サポートを行う。"
    ),
    "fungal": (
        "Treatment of {name_l} in {species_l} requires systemic antifungal therapy. Azole "
        "antifungals (fluconazole, itraconazole, ketoconazole) or amphotericin B may be used "
        "depending on the organism and severity. Treatment duration is typically prolonged "
        "(weeks to months) to ensure complete clearance. Topical antifungal agents may be "
        "used adjunctively for superficial infections. Environmental decontamination reduces "
        "reinfection risk. Monitor hepatic function during prolonged azole therapy.",
        "{species}における{name_ja}の治療には全身性抗真菌薬療法が必要である。"
        "アゾール系抗真菌薬（フルコナゾール、イトラコナゾール、ケトコナゾール）または"
        "アムホテリシンBが菌種と重症度に応じて使用される。治療期間は完全な除菌のため"
        "通常長期間（数週間〜数ヶ月）を要する。表在性感染には局所抗真菌剤を併用する。"
        "環境消毒により再感染リスクを低減する。長期アゾール療法中は肝機能をモニタリングする。"
    ),
    "parasitic": (
        "Treatment of {name_l} in {species_l} requires appropriate antiparasitic medication "
        "selected based on the specific parasite identified. Species-appropriate dosing is critical "
        "as some antiparasitics are toxic to certain species. Treatment may require multiple "
        "doses to eliminate all life stages. Environmental decontamination and in-contact "
        "animal treatment prevent reinfection. Supportive care addresses secondary "
        "complications such as anemia, dehydration, or malnutrition.",
        "{species}における{name_ja}の治療には、同定された寄生虫に応じた適切な"
        "駆虫薬が必要である。一部の駆虫薬は特定の種に有毒であるため、"
        "種に適した用量設定が重要である。全てのライフステージを排除するため"
        "複数回投与が必要な場合がある。環境消毒と接触動物の治療で再感染を防止する。"
        "貧血、脱水、栄養失調などの二次的合併症に対する支持療法を行う。"
    ),
    "neoplastic": (
        "Treatment of {name_l} in {species_l} depends on tumor type, location, and stage. "
        "Surgical excision with adequate margins is the primary treatment for accessible solid "
        "tumors. Chemotherapy may be indicated for systemic neoplasia, incompletely excised "
        "tumors, or metastatic disease. Radiation therapy can provide local tumor control. "
        "Palliative care focuses on pain management, nutritional support, and maintaining "
        "quality of life when curative treatment is not feasible.",
        "{species}における{name_ja}の治療は腫瘍の種類、部位、病期に依存する。"
        "アクセス可能な固形腫瘍には十分なマージンを確保した外科的切除が第一選択である。"
        "全身性腫瘍、不完全切除、転移性疾患には化学療法が適応となりうる。"
        "放射線療法は局所的な腫瘍制御を提供できる。根治療法が困難な場合は"
        "疼痛管理、栄養サポート、QOL維持に焦点を当てた緩和ケアを行う。"
    ),
    "metabolic": (
        "Treatment of {name_l} in {species_l} targets the underlying hormonal or metabolic "
        "imbalance. Hormone replacement or suppression therapy restores physiological balance. "
        "Dietary modifications address nutritional components of metabolic disease. Regular "
        "monitoring of hormone levels, blood glucose, electrolytes, or organ function markers "
        "guides dose adjustments. Concurrent management of secondary complications "
        "(organ damage, infections) is essential. Long-term or lifelong therapy may be required.",
        "{species}における{name_ja}の治療は基礎となるホルモン・代謝異常を標的とする。"
        "ホルモン補充療法または抑制療法により生理的バランスを回復する。"
        "食事療法で代謝疾患の栄養面に対処する。ホルモンレベル、血糖、電解質、"
        "臓器機能マーカーの定期的モニタリングにより用量調整を行う。"
        "二次的合併症（臓器障害、感染）の併行管理が不可欠である。"
        "長期または生涯にわたる治療が必要な場合がある。"
    ),
    "nutritional": (
        "Treatment of {name_l} in {species_l} centers on correcting the nutritional imbalance. "
        "Deficiency states require supplementation of the specific nutrient through dietary "
        "correction or therapeutic supplementation. Excess states require dietary restriction "
        "and supportive care for organ damage. Gradual correction prevents refeeding syndrome "
        "in malnourished animals. Species-specific dietary requirements must guide long-term "
        "nutritional planning. Regular reassessment ensures adequate without excessive intake.",
        "{species}における{name_ja}の治療は栄養バランスの是正が中心となる。"
        "欠乏状態では食事の改善または治療的サプリメンテーションにより特定の栄養素を補充する。"
        "過剰状態では食事制限と臓器障害に対する支持療法を行う。"
        "栄養不良動物ではリフィーディング症候群予防のため段階的に是正する。"
        "種特異的な食事要求に基づく長期栄養計画を立案する。"
        "過不足のない摂取を確保するため定期的に再評価する。"
    ),
    "toxic": (
        "Treatment of {name_l} in {species_l} requires rapid decontamination and supportive "
        "care. If ingestion was recent, emesis induction (where safe for the species) or "
        "gastric lavage may reduce absorption. Activated charcoal adsorbs many toxins. "
        "Specific antidotes should be administered when available (e.g., vitamin K1 for "
        "anticoagulant rodenticides, N-acetylcysteine for acetaminophen). "
        "Aggressive IV fluid therapy supports renal excretion and maintains perfusion. "
        "Monitor and treat organ-specific damage (hepatic, renal, neurological).",
        "{species}における{name_ja}の治療には迅速な除染と支持療法が必要である。"
        "摂取直後であれば催吐（種にとって安全な場合）または胃洗浄により吸収を低減する。"
        "活性炭は多くの毒素を吸着する。特異的解毒剤がある場合は投与する"
        "（例：抗凝固性殺鼠剤にビタミンK1、アセトアミノフェンにN-アセチルシステイン）。"
        "積極的な輸液療法で腎排泄を促進し灌流を維持する。"
        "臓器特異的障害（肝、腎、神経）をモニタリングし治療する。"
    ),
    "traumatic": (
        "Treatment of {name_l} in {species_l} prioritizes stabilization, pain management, "
        "and wound care. Assess and address life-threatening injuries first (airway, breathing, "
        "circulation). Analgesia is essential—use species-appropriate agents (NSAIDs, opioids, "
        "local anesthetics). Clean and debride wounds; primary closure, second-intention healing, "
        "or reconstructive surgery as indicated. Broad-spectrum antibiotics for contaminated "
        "wounds. Splinting or surgical fixation for fractures. Monitor for delayed complications.",
        "{species}における{name_ja}の治療は安定化、疼痛管理、創傷ケアを優先する。"
        "生命を脅かす損傷を最初に評価・対処する（気道、呼吸、循環）。"
        "種に適した鎮痛薬（NSAIDs、オピオイド、局所麻酔薬）による鎮痛が不可欠である。"
        "創傷を洗浄・デブリードマンし、一次閉鎖、二次治癒、再建手術を適宜行う。"
        "汚染創には広域抗菌薬を使用する。骨折には副子固定または外科的固定を行う。"
        "遅発性合併症をモニタリングする。"
    ),
    "dental": (
        "Treatment of {name_l} in {species_l} requires dental examination under sedation "
        "or anesthesia for thorough assessment. Malocclusion may require tooth trimming, "
        "burring, or extraction depending on species and severity. Periapical abscesses "
        "require drainage, debridement, and systemic antibiotics. Periodontal disease "
        "treatment includes scaling, polishing, and extraction of severely affected teeth. "
        "Pain management with species-appropriate analgesics is essential. "
        "Dietary modifications support recovery and prevent recurrence.",
        "{species}における{name_ja}の治療には鎮静または麻酔下での歯科検査が必要である。"
        "不正咬合は種と重症度に応じて歯のトリミング、研磨、抜歯が必要となる。"
        "根尖膿瘍には排膿、デブリードマン、全身性抗菌薬が必要である。"
        "歯周病治療にはスケーリング、研磨、重度罹患歯の抜歯を含む。"
        "種に適した鎮痛薬による疼痛管理が不可欠である。"
        "食事の調整により回復を促進し再発を予防する。"
    ),
    "autoimmune": (
        "Treatment of {name_l} in {species_l} involves immunosuppressive or immunomodulatory "
        "therapy. Corticosteroids (prednisolone, dexamethasone) at immunosuppressive doses are "
        "first-line for most autoimmune conditions. Steroid-sparing agents (azathioprine, "
        "cyclosporine, mycophenolate) may be added for refractory cases or to reduce steroid "
        "side effects. Allergen avoidance, antihistamines, or immunotherapy for allergic "
        "conditions. Monitor for iatrogenic immunosuppression complications. "
        "Gradual dose tapering prevents relapse.",
        "{species}における{name_ja}の治療は免疫抑制療法または免疫調節療法を行う。"
        "副腎皮質ステロイド（プレドニゾロン、デキサメタゾン）の免疫抑制用量が"
        "多くの自己免疫疾患の第一選択である。難治例やステロイド副作用軽減のため"
        "ステロイド温存薬（アザチオプリン、シクロスポリン、ミコフェノール酸モフェチル）を"
        "併用する場合がある。アレルギー疾患にはアレルゲン回避、抗ヒスタミン薬、"
        "免疫療法を行う。医原性免疫抑制の合併症をモニタリングする。"
        "再発防止のため段階的に減量する。"
    ),
}

_PREV_TEMPLATES: dict[str, tuple[str, str]] = {
    "viral": (
        "Prevention of {name_l} includes vaccination where available, quarantine of new "
        "or sick animals, strict biosecurity measures, proper disinfection protocols, "
        "and avoiding contact with known carriers or contaminated environments.",
        "{name_ja}の予防にはワクチン接種（利用可能な場合）、新規・病気動物の隔離、"
        "厳格なバイオセキュリティ対策、適切な消毒プロトコル、"
        "既知のキャリアや汚染環境との接触回避が含まれる。"
    ),
    "bacterial": (
        "Prevention of {name_l} includes maintaining good hygiene and sanitation, "
        "appropriate vaccination where available, prompt treatment of wounds, "
        "stress reduction, proper ventilation, and quarantine of infected animals.",
        "{name_ja}の予防には適切な衛生管理・消毒、利用可能なワクチン接種、"
        "創傷の迅速な処置、ストレス軽減、適切な換気、感染動物の隔離が含まれる。"
    ),
    "fungal": (
        "Prevention of {name_l} includes maintaining appropriate environmental humidity "
        "and temperature, good ventilation, avoiding overcrowding, regular cleaning "
        "and disinfection, quarantine of affected individuals, and supporting immune "
        "health through proper nutrition.",
        "{name_ja}の予防には適切な環境湿度・温度の維持、良好な換気、"
        "過密の回避、定期的な清掃・消毒、罹患個体の隔離、"
        "適切な栄養による免疫機能の維持が含まれる。"
    ),
    "parasitic": (
        "Prevention of {name_l} includes regular prophylactic antiparasitic treatment, "
        "environmental hygiene and fecal removal, quarantine and testing of new animals, "
        "vector control measures, and avoiding exposure to intermediate hosts "
        "or contaminated environments.",
        "{name_ja}の予防には定期的な予防駆虫、環境衛生と糞便除去、"
        "新規動物の隔離・検査、ベクター防除、中間宿主や汚染環境への"
        "曝露回避が含まれる。"
    ),
    "neoplastic": (
        "Prevention of {name_l} is limited but includes spaying/neutering to reduce "
        "hormone-dependent tumors, avoiding known carcinogens, regular health screening "
        "for early detection, maintaining optimal body condition, and responsible "
        "breeding to reduce genetic predisposition where applicable.",
        "{name_ja}の予防は限定的であるが、ホルモン依存性腫瘍軽減のための"
        "避妊・去勢手術、既知の発癌物質の回避、早期発見のための定期健診、"
        "適正体型の維持、該当する場合は遺伝的素因軽減のための責任ある繁殖が含まれる。"
    ),
    "metabolic": (
        "Prevention of {name_l} includes appropriate diet formulation, regular health "
        "monitoring with blood work, maintaining healthy body weight, avoiding excessive "
        "treats or inappropriate foods, and early intervention when subclinical changes "
        "are detected.",
        "{name_ja}の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、"
        "健康体重の維持、過剰なおやつや不適切な食事の回避、"
        "無症候性変化の早期発見時の迅速な介入が含まれる。"
    ),
    "nutritional": (
        "Prevention of {name_l} requires species-appropriate diet formulation meeting "
        "all nutritional requirements, avoiding exclusive single-food diets, regular "
        "dietary review with a veterinarian, appropriate supplementation when indicated, "
        "and education on species-specific nutritional needs.",
        "{name_ja}の予防には全ての栄養要求を満たす種に適した食事設計、"
        "単一食品のみの食事の回避、獣医師との定期的な食事内容の見直し、"
        "必要時の適切なサプリメンテーション、種固有の栄養ニーズに関する知識が必要である。"
    ),
    "toxic": (
        "Prevention of {name_l} requires removing or securing access to toxic substances, "
        "using pet-safe products, avoiding toxic plants in the animal's environment, "
        "proper storage of medications and chemicals, supervision during outdoor access, "
        "and owner education on species-specific toxicities.",
        "{name_ja}の予防には有毒物質へのアクセス制限・除去、ペット安全な製品の使用、"
        "環境からの有毒植物の除去、薬剤・化学物質の適切な保管、"
        "屋外アクセス時の監視、種固有の中毒に関する飼い主教育が必要である。"
    ),
    "traumatic": (
        "Prevention of {name_l} includes providing a safe, species-appropriate enclosure, "
        "removing sharp objects and hazards, appropriate handling techniques, supervised "
        "interactions with other animals, temperature regulation, and fall prevention.",
        "{name_ja}の予防には安全で種に適した飼育環境の整備、鋭利物・危険物の除去、"
        "適切な取り扱い技術、他の動物との接触時の監視、"
        "温度管理、落下防止策が含まれる。"
    ),
    "dental": (
        "Prevention of {name_l} includes providing appropriate chewing materials and diet "
        "to promote natural tooth wear, regular dental examinations, early correction of "
        "developing malocclusion, and dietary roughage appropriate for the species.",
        "{name_ja}の予防には自然な歯の摩耗を促進する適切な咀嚼材と食事、"
        "定期的な歯科検査、発生しつつある不正咬合の早期矯正、"
        "種に適した食物繊維の提供が含まれる。"
    ),
    "autoimmune": (
        "Prevention of {name_l} is limited as the underlying immune dysregulation may "
        "have genetic components. Risk reduction includes minimizing environmental triggers "
        "and stressors, avoiding known allergens, maintaining optimal nutrition, "
        "regular health monitoring, and early treatment of flares.",
        "{name_ja}の予防は基礎となる免疫調節障害に遺伝的要素がある場合は限定的である。"
        "環境トリガーとストレスの最小化、既知アレルゲンの回避、"
        "最適な栄養の維持、定期的な健康モニタリング、フレアの早期治療で"
        "リスクを低減する。"
    ),
}

# Default templates for categories without specific ones
_DEFAULT_TREAT = (
    "Treatment of {name_l} in {species_l} involves addressing the underlying cause, "
    "providing appropriate supportive care, and managing clinical signs. "
    "Species-appropriate medication, dietary optimization, and environmental "
    "modifications are key components. Regular follow-up assessment ensures "
    "treatment efficacy and allows dose adjustments.",
    "{species}における{name_ja}の治療は原因への対処、適切な支持療法、"
    "臨床徴候の管理を行う。種に適した薬物療法、食事の最適化、"
    "環境調整が主要な治療要素である。定期的なフォローアップにより"
    "治療効果を確認し用量調整を行う。"
)

_DEFAULT_PREV = (
    "Prevention of {name_l} includes appropriate husbandry, balanced species-specific "
    "nutrition, regular veterinary health checks, stress minimization, maintaining "
    "clean living conditions, and prompt attention to early clinical signs.",
    "{name_ja}の予防には適切な飼育管理、種に合ったバランスの取れた栄養、"
    "定期的な健康診断、ストレスの最小化、清潔な生活環境の維持、"
    "初期臨床徴候への迅速な対応が含まれる。"
)

# Urgency-specific prognosis
_PROGNOSIS: dict[str, tuple[str, str]] = {
    "emergency": (
        "Prognosis for {name_l} is guarded to poor without immediate veterinary "
        "intervention. With aggressive, timely treatment, survival rates improve but "
        "may vary depending on the specific etiology, severity at presentation, "
        "and host immune status. Long-term sequelae may occur in survivors. "
        "Mortality can be significant in severe or untreated cases.",
        "{name_ja}の予後は即座の獣医学的介入がなければ慎重〜不良である。"
        "積極的かつ迅速な治療により生存率は改善するが、原因、"
        "来院時の重症度、宿主免疫状態により異なる。"
        "生存例でも長期後遺症が生じうる。重症例や未治療例では死亡率が高い。"
    ),
    "high": (
        "Prognosis for {name_l} depends on the rapidity of diagnosis and initiation of "
        "appropriate therapy. With prompt treatment, many cases show significant "
        "improvement within days to weeks. Delayed treatment increases the risk of "
        "complications and may worsen the outcome. Some cases require prolonged "
        "management or may recur.",
        "{name_ja}の予後は診断の迅速さと適切な治療の開始に依存する。"
        "迅速な治療により多くの症例が数日〜数週間で著明な改善を示す。"
        "治療の遅延は合併症リスクを高め予後を悪化させうる。"
        "長期管理が必要な場合や再発する場合がある。"
    ),
    "moderate": (
        "Prognosis for {name_l} is generally fair to good with appropriate management. "
        "Most cases respond well to treatment when diagnosed early. Chronic or "
        "recurrent cases may require long-term management but generally maintain "
        "acceptable quality of life. Regular monitoring helps detect and address "
        "complications early.",
        "{name_ja}の予後は適切な管理により一般的にやや良好〜良好である。"
        "早期診断された症例の多くは治療に良好に反応する。"
        "慢性例や再発例では長期管理が必要だが、概ね許容できるQOLを維持できる。"
        "定期的なモニタリングにより合併症の早期発見・対処が可能となる。"
    ),
    "low": (
        "Prognosis for {name_l} is generally good to excellent with appropriate care. "
        "Most cases resolve completely with treatment, and recurrence can be "
        "prevented with proper management changes. Long-term complications are "
        "uncommon when the condition is addressed promptly.",
        "{name_ja}の予後は適切なケアにより一般的に良好〜優秀である。"
        "治療により多くの症例が完全に回復し、適切な管理変更により"
        "再発を予防できる。迅速に対処された場合、長期合併症は稀である。"
    ),
}


def enrich_disease(d: dict) -> dict:
    """Enrich a single disease entry with category-specific content."""
    name = d.get("name", "")
    name_ja = d.get("name_ja", name)
    species = d.get("species", "")
    desc = d.get("description", "")
    urgency = d.get("urgency", "moderate")

    # Skip if already truly rich (not template-based)
    patho = d.get("pathophysiology") or ""
    template_markers = [
        "involves pathological changes",
        "disorder in",
        "Metabolic dysfunction in",
        "Pathogenic bacteria colonize",
        "Neoplastic transformation",
        "Fungal organisms invade",
        "The causative virus targets",
        "Parasitic organism establishes",
        "Autoimmune-mediated attack",
        "Traumatic force applied",
    ]
    is_template = any(m in patho for m in template_markers) or not patho
    if not is_template and len(patho) > 200:
        return d  # Already rich, skip

    category = classify_disease(name, desc)

    name_l = name.lower()
    species_l = species.lower()

    fmt = {
        "name": name,
        "name_l": name_l,
        "name_ja": name_ja,
        "species": species,
        "species_l": species_l,
        "desc": desc,
    }

    # Pathophysiology
    pt = _PATHO_TEMPLATES.get(category, _PATHO_TEMPLATES.get("general"))
    if pt:
        d["pathophysiology"] = pt[0].format(**fmt)
        d["pathophysiology_ja"] = pt[1].format(**fmt)
    else:
        # Fallback for truly unclassified
        d["pathophysiology"] = (
            f"{name} is a clinical condition in {species_l}. {desc} "
            f"The underlying pathological process involves tissue-level changes "
            f"that disrupt normal physiological function. Without appropriate "
            f"intervention, the condition may progress and affect overall health."
        )
        d["pathophysiology_ja"] = (
            f"{name_ja}は{species}における臨床疾患である。"
            f"基礎となる病理過程は正常な生理機能を障害する組織レベルの変化を伴う。"
            f"適切な介入がなければ、全体的な健康に影響を及ぼす可能性がある。"
        )

    # Treatment
    tt = _TREAT_TEMPLATES.get(category, _DEFAULT_TREAT)
    d["treatment"] = tt[0].format(**fmt)
    d["treatment_ja"] = tt[1].format(**fmt)

    # Causes
    d["causes"] = f"Causes of {name_l} in {species_l}: {desc}"
    d["causes_ja"] = (
        f"{species}における{name_ja}の原因: "
        f"{d.get('description_ja') or desc}"
    )

    # Diagnosis
    tests = d.get("recommended_tests") or []
    if tests and isinstance(tests, list):
        test_str = ", ".join(str(t) for t in tests[:5])
        d["diagnosis"] = (
            f"Diagnosis of {name_l} is based on clinical signs, thorough history, "
            f"and physical examination. Recommended diagnostics include: {test_str}. "
            f"Differential diagnosis should consider other conditions presenting "
            f"with similar clinical signs in {species_l}."
        )
        d["diagnosis_ja"] = (
            f"{name_ja}の診断は臨床徴候、詳細な病歴、身体検査に基づく。"
            f"推奨される検査: {test_str}。"
            f"{species}における類似の臨床徴候を呈する他疾患との鑑別が必要である。"
        )
    else:
        d["diagnosis"] = (
            f"Diagnosis of {name_l} is based on clinical presentation, "
            f"thorough history, physical examination, and appropriate diagnostic "
            f"workup. Findings guide selection of confirmatory tests."
        )
        d["diagnosis_ja"] = (
            f"{name_ja}の診断は臨床像、詳細な病歴、身体検査、"
            f"および適切な検査に基づく。所見により確定検査を選択する。"
        )

    # Prevention
    pv = _PREV_TEMPLATES.get(category, _DEFAULT_PREV)
    d["prevention"] = pv[0].format(**fmt)
    d["prevention_ja"] = pv[1].format(**fmt)

    # Prognosis (urgency-based)
    pg = _PROGNOSIS.get(urgency, _PROGNOSIS["moderate"])
    d["prognosis"] = pg[0].format(**fmt)
    d["prognosis_ja"] = pg[1].format(**fmt)

    # Clinical signs
    d.setdefault("clinical_signs", "")
    d.setdefault("clinical_signs_ja", "")

    d["enrichment_phase"] = 4
    d["enriched_at"] = datetime.utcnow().isoformat()

    return d


def main():
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} diseases")

    enriched_count = 0
    skipped_count = 0
    category_counts: Counter = Counter()

    for d in data:
        name = d.get("name", "")
        desc = d.get("description", "")
        category = classify_disease(name, desc)
        category_counts[category] += 1

        old_patho = d.get("pathophysiology", "")
        enrich_disease(d)
        new_patho = d.get("pathophysiology", "")

        if new_patho != old_patho:
            enriched_count += 1
        else:
            skipped_count += 1

    print(f"Enriched: {enriched_count}, Skipped (already rich): {skipped_count}")
    print(f"\nCategory distribution:")
    for cat, cnt in category_counts.most_common():
        print(f"  {cat:<20}: {cnt}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to {JSON_PATH}")


if __name__ == "__main__":
    main()
