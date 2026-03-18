#!/usr/bin/env python3
"""Enrich Horse (equine) diseases with treatment_protocol, clinical_signs_detail, risk_factors.

Reads equine_diseases.py, identifies Disease entries missing these fields,
generates category-appropriate content, and writes the updated file.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.species.equine_diseases import DISEASE_DATABASE

# ============================================================================
# Category-specific templates for treatment protocols
# ============================================================================

TREATMENT_TEMPLATES: dict[str, str] = {
    "musculoskeletal": (
        "Initial management includes rest, controlled exercise restriction, and cryotherapy. "
        "NSAIDs (phenylbutazone 2.2-4.4 mg/kg PO BID or flunixin meglumine 1.1 mg/kg IV) for pain and inflammation. "
        "Intra-articular corticosteroid injections (triamcinolone 6-12 mg or methylprednisolone 40-80 mg) for joint disease. "
        "Hyaluronic acid and polysulfated glycosaminoglycans (Adequan) for cartilage support. "
        "Extracorporeal shockwave therapy or PRP/IRAP for tendon/ligament injuries. "
        "Surgical intervention (arthroscopy, internal fixation) when indicated. "
        "Rehabilitation: progressive exercise program, controlled turnout."
    ),
    "hoof": (
        "Immediate stabilization with therapeutic shoeing or hoof casting. "
        "Cryotherapy (continuous digital hypothermia) in acute laminitis. "
        "NSAIDs (phenylbutazone 2.2-4.4 mg/kg PO BID) for pain management. "
        "Corrective farriery: heart bar shoes, pads, pour-in materials for support. "
        "Digital venography to assess perfusion in severe cases. "
        "Hoof wall resection for subsolar abscesses or white line disease. "
        "Strict stall rest with deep bedding for acute cases. "
        "Regular farrier visits (4-6 week cycle) for chronic management."
    ),
    "respiratory": (
        "Environmental management: reduce dust, improve ventilation, soak/steam hay. "
        "Bronchodilators (clenbuterol 0.8 μg/kg PO BID or inhaled albuterol) for airway obstruction. "
        "Corticosteroids (dexamethasone 0.04-0.1 mg/kg IV/IM or inhaled fluticasone/beclomethasone). "
        "Antimicrobials based on culture/sensitivity for bacterial pneumonia (TMS, penicillin, gentamicin). "
        "Antivirals not routinely available; supportive care for viral respiratory disease. "
        "Nebulization with saline ± mucolytics. Tracheostomy for upper airway emergencies. "
        "Rest from exercise during active respiratory disease."
    ),
    "digestive": (
        "Colic management: nasogastric intubation for gastric decompression, IV fluid therapy (LRS or hypertonic saline). "
        "Analgesics: flunixin meglumine 1.1 mg/kg IV, xylazine 0.3-0.5 mg/kg IV, butorphanol 0.02-0.04 mg/kg IV. "
        "Mineral oil via nasogastric tube for impactions. Prokinetics (lidocaine 1.3 mg/kg IV bolus then 0.05 mg/kg/min CRI). "
        "Surgical exploration (celiotomy) for strangulating lesions, large colon volvulus, or unresponsive impactions. "
        "Post-surgical: IV fluids, antibiotics, gradual refeeding. Gastric ulcer management: omeprazole 4 mg/kg PO SID."
    ),
    "skin": (
        "Topical therapy: antimicrobial shampoos (chlorhexidine 2-4%), antifungal washes (miconazole/ketoconazole). "
        "Systemic antimicrobials: TMS 15-30 mg/kg PO BID for bacterial dermatitis. "
        "Griseofulvin 10 mg/kg PO SID or systemic azoles for dermatophytosis. "
        "Corticosteroids (prednisolone 1 mg/kg PO SID tapering) for allergic/immune-mediated conditions. "
        "Fly control: permethrin sprays, fly sheets, fly masks. Wound management: lavage, debridement, bandaging. "
        "Proud flesh prevention/treatment with topical corticosteroids or surgical excision."
    ),
    "eye": (
        "Ophthalmic examination with sedation and nerve blocks (auriculopalpebral, supraorbital). "
        "Topical antibiotics: chloramphenicol, ciprofloxacin, or triple antibiotic for corneal ulcers. "
        "Topical atropine 1% for ciliary spasm and pain. Subpalpebral lavage system for frequent medication delivery. "
        "Systemic NSAIDs (flunixin meglumine 1.1 mg/kg IV) for uveitis. "
        "Topical corticosteroids ONLY for non-ulcerative conditions. Cyclosporine for immune-mediated keratitis. "
        "Enucleation for end-stage painful eyes. Fly mask for UV protection."
    ),
    "neurological": (
        "Supportive care: sling support for recumbent horses, deep bedding, nutritional support. "
        "Anti-inflammatories: flunixin meglumine 1.1 mg/kg IV or DMSO 1 g/kg IV in 10% solution for cerebral edema. "
        "Anticonvulsants: diazepam 0.05-0.4 mg/kg IV for seizures, phenobarbital for maintenance. "
        "Antimicrobials: high-dose penicillin + gentamicin for bacterial meningitis/encephalitis. "
        "Tetanus antitoxin + toxoid, penicillin, and sedation (acepromazine/diazepam) for tetanus. "
        "Physical therapy and controlled exercise during recovery. Prognosis varies significantly by etiology."
    ),
    "cardiovascular": (
        "Medical management: digoxin 0.011 mg/kg PO BID for atrial fibrillation with hemodynamic compromise. "
        "Quinidine sulfate 22 mg/kg PO q2h via nasogastric tube for conversion of atrial fibrillation. "
        "Lidocaine 0.25-0.5 mg/kg IV bolus for ventricular arrhythmias. "
        "ACE inhibitors (benazepril 0.5 mg/kg PO SID) for congestive heart failure. "
        "Furosemide 1-2 mg/kg IV/IM for acute pulmonary edema. "
        "Echocardiographic monitoring of cardiac function. Exercise restriction for significant cardiac disease."
    ),
    "reproductive": (
        "Uterine lavage with warm saline for post-breeding endometritis. "
        "Oxytocin 10-20 IU IM/IV for uterine clearance and retained fetal membranes. "
        "Prostaglandin F2α (cloprostenol 250 μg IM) for luteolysis/uterine clearance. "
        "Progesterone supplementation (altrenogest 0.044 mg/kg PO SID) for pregnancy maintenance. "
        "Deslorelin or hCG for ovulation induction. Antibiotics: intrauterine infusion (gentamicin, amikacin) or systemic. "
        "Surgical intervention: cesarean section, cryptorchid castration, ovariectomy when indicated."
    ),
    "infectious": (
        "Isolation and quarantine of affected animals. "
        "Antimicrobial therapy based on culture/sensitivity: penicillin, gentamicin, TMS, enrofloxacin. "
        "Antifungal therapy: systemic azoles or amphotericin B for mycotic infections. "
        "Supportive care: IV fluid therapy, nutritional support, fever management (flunixin 1.1 mg/kg IV). "
        "Vaccination post-exposure when applicable (tetanus, strangles). "
        "Environmental decontamination, vector control. Report notifiable diseases to authorities."
    ),
    "metabolic": (
        "Dietary management: low-NSC (non-structural carbohydrate) diet, grazing muzzle, controlled pasture access. "
        "IV fluid therapy (LRS with potassium supplementation) for metabolic derangements. "
        "Insulin regulation: levothyroxine 0.1 mg/kg PO SID, metformin 15-30 mg/kg PO BID for insulin dysregulation. "
        "Electrolyte correction: calcium borogluconate for hypocalcemia, magnesium sulfate for hypomagnesemia. "
        "Hepatic support: IV dextrose, branched-chain amino acids for hepatic encephalopathy. "
        "Exercise program for equine metabolic syndrome. Regular metabolic panel monitoring."
    ),
    "dental": (
        "Sedation (detomidine 0.01-0.02 mg/kg IV + butorphanol 0.01-0.02 mg/kg IV) for oral examination. "
        "Dental floating (rasping): correction of sharp enamel points, hooks, ramps, and wave mouth. "
        "Extraction of diseased, fractured, or supernumerary teeth under standing sedation or general anesthesia. "
        "Oral lavage and debridement for periodontal disease. Antibiotics (TMS, metronidazole) for dental abscesses. "
        "Regular dental examinations every 6-12 months. Dietary modifications for horses with significant dental disease."
    ),
    "toxic": (
        "Immediate removal from toxin source. Gastric decontamination: activated charcoal 1-3 g/kg via nasogastric tube "
        "(within 2-4 hours of ingestion). Cathartics (mineral oil, magnesium sulfate) to hasten GI transit. "
        "Specific antidotes when available: atropine for organophosphates, vitamin K1 for anticoagulant rodenticides, "
        "dimercaprol or succimer for heavy metals. IV fluid therapy for renal support and toxin excretion. "
        "Hepatoprotectants: N-acetylcysteine, S-adenosylmethionine for hepatotoxins. "
        "Serial monitoring of organ function (hepatic, renal, hematologic panels)."
    ),
    "foal": (
        "Neonatal ICU care: thermal support (heat lamps, blankets), IV catheterization, fluid therapy. "
        "Colostrum/plasma transfusion for failure of passive transfer (IgG <800 mg/dL). "
        "Broad-spectrum antimicrobials: penicillin + amikacin or ceftiofur for neonatal sepsis. "
        "Nutritional support: nasogastric tube feeding of mare's milk/milk replacer every 1-2 hours. "
        "Oxygen supplementation: intranasal insufflation 5-10 L/min. "
        "Ulcer prophylaxis: omeprazole 4 mg/kg PO SID. Ophthalmic exam for entropion and ulcers. "
        "Monitoring: serial blood glucose, IgG, lactate, sepsis scoring."
    ),
    "immune": (
        "Immunosuppressive therapy: dexamethasone 0.04-0.2 mg/kg IV/IM tapering or prednisolone 1-2 mg/kg PO SID. "
        "Azathioprine 3 mg/kg PO SID as steroid-sparing agent for chronic immune-mediated disease. "
        "Blood transfusion for severe immune-mediated hemolytic anemia (IMHA). "
        "Pentoxifylline 8.5 mg/kg PO BID as adjunctive anti-inflammatory. "
        "Topical immunomodulators for localized conditions. Supportive care: IV fluids, nutrition. "
        "Monitor: CBC, chemistry panel, immune markers. Gradual steroid taper to prevent relapse."
    ),
    "oncology": (
        "Surgical excision with wide margins where anatomically feasible. "
        "Cisplatin beads or intralesional chemotherapy for sarcoids and squamous cell carcinoma. "
        "Radiation therapy (brachytherapy) for periocular and localized tumors. "
        "Cryotherapy or laser ablation for superficial lesions. BCG immunotherapy for sarcoids. "
        "Systemic chemotherapy (rarely used): carboplatin for melanoma. "
        "Palliative care: NSAIDs for pain, nutritional support. "
        "Prognosis depends on tumor type, location, and stage."
    ),
    "urinary": (
        "IV fluid therapy (LRS, 0.9% NaCl) for renal support and diuresis. "
        "Antimicrobials based on urine culture/sensitivity for urinary tract infections. "
        "Dietary management: reduce calcium intake for calcium carbonate urolithiasis. "
        "Surgical: cystotomy for bladder calculi, urethrostomy for obstructive urolithiasis. "
        "Acidification of urine generally not effective in horses. "
        "Monitor: serial urinalysis, BUN/creatinine, electrolytes. "
        "Chronic renal failure: supportive care, dietary protein management."
    ),
    "misc": (
        "Treatment depends on the specific condition. General principles include: "
        "species-appropriate pain management (NSAIDs, opioids), IV fluid therapy for dehydration/shock, "
        "antimicrobial therapy guided by culture/sensitivity when infection is present, "
        "nutritional support including assisted feeding if anorexic, "
        "environmental modification for comfort and safety, "
        "and close monitoring with serial clinical and laboratory assessment."
    ),
}

# ============================================================================
# Category-specific templates for clinical signs
# ============================================================================

CLINICAL_SIGNS_TEMPLATES: dict[str, str] = {
    "musculoskeletal": (
        "跛行（前肢/後肢）、関節腫脹・熱感・疼痛、屈曲試験陽性、"
        "運動時の硬さ・歩様異常、患肢の挙上・免荷、筋萎縮、"
        "触診での圧痛、可動域制限"
    ),
    "hoof": (
        "跛行（急性/慢性）、蹄の熱感、指動脈拍動亢進、"
        "蹄壁の変形・亀裂・離層、蹄底の圧痛（ヒッテスター反応陽性）、"
        "ソリヤリング（蹄輪の不整）、陥蹄姿勢、歩様短縮"
    ),
    "respiratory": (
        "鼻汁（漿液性/粘液膿性）、咳嗽、呼吸困難・努力性呼吸、"
        "鼻翼呼吸、腹式呼吸（ヒーブライン）、運動不耐性、"
        "喘鳴・異常呼吸音、発熱、頸部リンパ節腫脹"
    ),
    "digestive": (
        "腹痛徴候（パーリング、フランク注視、転がり、起臥反復）、"
        "食欲不振、排便減少・停止、下痢、腹部膨満、"
        "腸蠕動音異常（減弱/亢進/消失）、脱水、頻脈"
    ),
    "skin": (
        "脱毛、鱗屑、痂皮形成、掻痒（擦り付け）、"
        "蕁麻疹、結節・腫瘤、皮膚潰瘍、浮腫、"
        "創傷の治癒不全（過剰肉芽・proud flesh）、光過敏症"
    ),
    "eye": (
        "流涙、眼瞼痙攣（羞明）、結膜充血、角膜混濁・潰瘍、"
        "前房フレア・蓄膿、瞳孔縮瞳/散瞳、眼球突出/陥没、"
        "視力低下（障害物回避困難）、眼周囲腫脹"
    ),
    "neurological": (
        "運動失調、旋回運動、頭部傾斜、眼振、"
        "起立不能・沈鬱、筋痙攣・強直、嚥下困難、"
        "顔面神経麻痺、尾や肛門の弛緩、異常行動"
    ),
    "cardiovascular": (
        "運動不耐性、頻脈/徐脈、不整脈（聴診で検出）、"
        "頸静脈怒張・拍動、末梢浮腫（腹下・四肢）、"
        "粘膜蒼白/チアノーゼ、呼吸促迫、発汗、虚脱"
    ),
    "reproductive": (
        "外陰部からの排出物（膿性/血性）、乳房腫脹・乳汁漏出、"
        "妊娠馬の早産徴候、陣痛異常（微弱/強直）、"
        "後産停滞、外陰部の損傷、行動変化（落ち着きのなさ）"
    ),
    "infectious": (
        "発熱、沈鬱、食欲不振、リンパ節腫脹、"
        "鼻汁・眼脂、下痢、体重減少、"
        "皮膚病変（潰瘍・結節・膿瘍）、跛行、呼吸困難"
    ),
    "metabolic": (
        "多飲多尿、体重減少/肥満、被毛粗剛・脱毛、"
        "異常脂肪沈着（馬首）、陥蹄（続発性蹄葉炎）、"
        "筋痙攣・横臥、異常発汗、沈鬱・元気消失"
    ),
    "dental": (
        "咀嚼困難（キッディング）、流涎、口臭、"
        "採食速度低下・選り好み、体重減少、"
        "頭部の傾斜摂食、鼻汁（片側性）、顔面腫脹"
    ),
    "toxic": (
        "急性：流涎、疝痛症状、下痢、震顫、痙攣、虚脱。"
        "慢性：体重減少、被毛粗剛、光過敏症、黄疸、"
        "沈鬱、運動失調、肝/腎機能障害の徴候"
    ),
    "foal": (
        "哺乳意欲低下・吸啜力低下、沈鬱、発熱/低体温、"
        "関節腫脹（化膿性多関節炎）、臍帯異常（臍炎・膿瘍）、"
        "下痢（子馬下痢）、呼吸促迫、歩行異常"
    ),
    "immune": (
        "反復性蕁麻疹、全身性浮腫、紫斑（皮膚出血斑）、"
        "貧血（粘膜蒼白）、黄疸、発熱、"
        "皮膚潰瘍・壊死、関節炎、体重減少"
    ),
    "oncology": (
        "局所腫脹・腫瘤、潰瘍化、出血、"
        "体重減少（悪液質）、臓器特異的症状、"
        "リンパ節腫脹、疼痛、運動制限"
    ),
    "urinary": (
        "排尿困難・頻尿・血尿、尿流の途絶・尿閉、"
        "腎部の圧痛、多飲多尿、体重減少、"
        "浮腫、口臭（尿毒症臭）、沈鬱"
    ),
    "misc": (
        "疾患特異的な臨床徴候に加え、"
        "一般的所見として発熱、食欲不振、沈鬱、体重減少、"
        "脱水、粘膜色調変化が認められることがある"
    ),
}

# ============================================================================
# Risk factors by category
# ============================================================================

RISK_FACTORS_TEMPLATES: dict[str, str] = {
    "musculoskeletal": (
        "若齢馬の急速な成長、高強度トレーニング、不適切な蹄管理、"
        "体格・骨格の構造的弱点、過体重、硬い地面での運動、遺伝的素因"
    ),
    "hoof": (
        "不適切な装蹄・削蹄間隔、高糖質飼料（穀類過給）、肥満、"
        "クッシング病・EMS（馬メタボリックシンドローム）、"
        "湿潤環境、蹄壁の外傷、品種的素因"
    ),
    "respiratory": (
        "密集飼育・換気不良、埃っぽい飼料・敷料、輸送ストレス、"
        "混合飼育（異なる施設の馬の接触）、ワクチン未接種、"
        "免疫低下（幼齢/高齢/ストレス）"
    ),
    "digestive": (
        "急な飼料変更、砂地での採食、歯科疾患、寄生虫感染、"
        "ストレス（輸送・環境変化）、運動不足、脱水、"
        "NSAIDs長期投与（胃潰瘍リスク）"
    ),
    "skin": (
        "湿潤環境、不衛生な飼育条件、昆虫曝露、"
        "免疫低下、アレルギー体質、外傷、"
        "日光曝露（白い皮膚部位）、ストレス"
    ),
    "eye": (
        "Appaloosa品種（ERU好発）、外傷（牧草片・埃）、"
        "昆虫媒介感染（Onchocerca）、UV曝露、"
        "レプトスピラ感染既往、免疫介在性素因"
    ),
    "neurological": (
        "ワクチン未接種（EHV、WNV、狂犬病、EEE/WEE）、"
        "蚊媒介ウイルスの流行地域、頸椎の先天的狭窄、"
        "外傷、寄生虫感染（Halicephalobus）、中毒植物への曝露"
    ),
    "cardiovascular": (
        "高齢馬、激しい運動（競走馬）、先天性心疾患、"
        "感染症の併発（心内膜炎リスク）、電解質異常、"
        "ストレス、品種的素因"
    ),
    "reproductive": (
        "高齢繁殖牝馬、不適切な衛生管理（交配・分娩時）、"
        "子宮内膜症の既往、栄養不良、双子妊娠、"
        "感染症（CEM、EHV-1）、難産既往"
    ),
    "infectious": (
        "ワクチン未接種、密集飼育、新規馬の導入（隔離不足）、"
        "免疫低下（幼齢/高齢/ストレス/クッシング病）、"
        "汚染された水・飼料、昆虫ベクターの多い環境"
    ),
    "metabolic": (
        "肥満、品種的素因（ポニー、モーガン、アラブ）、"
        "高糖質飼料・豊富な牧草、加齢、クッシング病併発、"
        "運動不足、季節変動（春の牧草増加）"
    ),
    "dental": (
        "加齢（歯の摩耗パターン変化）、品種的素因（短頭種）、"
        "不適切な飼料形態、定期的歯科検診の欠如、"
        "外傷、先天的歯列異常"
    ),
    "toxic": (
        "毒性植物へのアクセス（セネシオ、キョウチクトウ、イチイ等）、"
        "殺虫剤・除草剤への曝露、カビ毒汚染飼料、"
        "不適切な薬物投与、汚染水源、過放牧による毒草摂食"
    ),
    "foal": (
        "初乳摂取不足（受動免疫移行不全）、難産、未熟/過熟出生、"
        "不衛生な分娩環境、臍帯処理不適切、"
        "Rh不適合（新生子溶血性疾患）、先天性異常"
    ),
    "immune": (
        "遺伝的素因、ストレス、感染症の先行、"
        "ワクチン接種後の免疫反応、寄生虫感染、"
        "薬物投与（ペニシリン等による免疫介在性反応）"
    ),
    "oncology": (
        "灰色馬（メラノーマ好発）、日光曝露（白い皮膚部位のSCC）、"
        "BPV（ウシパピローマウイルス：サルコイド関連）、"
        "加齢、遺伝的素因、慢性刺激/炎症"
    ),
    "urinary": (
        "高齢馬、高カルシウム飼料、脱水傾向、"
        "尿路感染の既往、膀胱麻痺（馬尾症候群）、"
        "長期安静（横臥）、品種的素因"
    ),
    "misc": (
        "個々の疾患に特異的なリスク因子に依存。"
        "一般的に免疫低下、ストレス、不適切な飼育環境、"
        "栄養不良、加齢が共通リスク因子となる"
    ),
}


def main():
    """Generate enrichment and patch the equine_diseases.py file."""
    filepath = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "api", "species", "equine_diseases.py",
    )

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    new_lines = []
    i = 0
    patched = 0
    in_disease_block = False
    current_disease_id = ""
    current_category = ""
    disease_map = {d.id: d for d in DISEASE_DATABASE}

    while i < len(lines):
        line = lines[i]

        # Detect Disease( opening
        m = re.match(r'^(\s*)Disease\(\s*$', line)
        if m:
            in_disease_block = True
            # Next line should be the ID
            if i + 1 < len(lines):
                id_match = re.match(r'^\s*"([^"]+)"', lines[i + 1])
                if id_match:
                    current_disease_id = id_match.group(1)
                    disease_obj = disease_map.get(current_disease_id)
                    if disease_obj:
                        current_category = disease_obj.category
            new_lines.append(line)
            i += 1
            continue

        # Detect closing of Disease( block - the ")," or ")" line
        if in_disease_block and re.match(r'^\s*\),?\s*$', line):
            # Check if we need to add missing fields
            disease_obj = disease_map.get(current_disease_id)
            if disease_obj:
                field_indent = "        "  # 8 spaces
                additions = []

                if not disease_obj.treatment_protocol:
                    tmpl = TREATMENT_TEMPLATES.get(current_category, TREATMENT_TEMPLATES["misc"])
                    # Escape for Python string
                    tmpl_escaped = tmpl.replace('"', '\\"')
                    additions.append(f'{field_indent}treatment_protocol="{tmpl_escaped}",')

                if not disease_obj.clinical_signs_detail:
                    tmpl = CLINICAL_SIGNS_TEMPLATES.get(current_category, CLINICAL_SIGNS_TEMPLATES["misc"])
                    tmpl_escaped = tmpl.replace('"', '\\"')
                    additions.append(f'{field_indent}clinical_signs_detail="{tmpl_escaped}",')

                if not disease_obj.risk_factors:
                    tmpl = RISK_FACTORS_TEMPLATES.get(current_category, RISK_FACTORS_TEMPLATES["misc"])
                    tmpl_escaped = tmpl.replace('"', '\\"')
                    additions.append(f'{field_indent}risk_factors="{tmpl_escaped}",')

                if additions:
                    new_lines.extend(additions)
                    patched += 1

            in_disease_block = False
            current_disease_id = ""
            current_category = ""
            new_lines.append(line)
            i += 1
            continue

        new_lines.append(line)
        i += 1

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    print(f"Patched {patched} Disease entries with missing fields")


if __name__ == "__main__":
    main()
