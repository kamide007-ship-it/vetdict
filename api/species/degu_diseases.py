"""Degu disease dictionary and symptom analysis module.

Degus (Octodon degus) are small rodents native to Chile with unique health
concerns.  They are notably unable to metabolize sugar, making diabetes
mellitus and secondary cataracts extremely common.  This module catalogues
50+ diseases across endocrine, dental, dermatological, respiratory,
gastrointestinal, musculoskeletal, neurological, ophthalmological, renal,
hepatic, reproductive, and neoplastic categories.
"""

from __future__ import annotations

from typing import Any, Dict, List

from . import prevalence_data
from .helpers import ADVICE, analyze_symptoms_generic, enrich_diseases

# ---------------------------------------------------------------------------
# Disease database
# ---------------------------------------------------------------------------

DISEASES: List[Dict[str, Any]] = [
    # ── Endocrine / Metabolic ──────────────────────────────────────────────
    {
        "name": "Diabetes Mellitus",
        "name_ja": "糖尿病",
        "symptoms": {"polyuria", "polydipsia", "weight_loss", "lethargy", "hyperglycemia"},
        "description": "Diabetes Mellitus in degus is a serious metabolic disorder with exceptionally high prevalence (30-50% of degus develop clinical diabetes during lifetime). CRITICAL: Degus have poor tolerance for dietary sugars—unlike most rodents, degus have limited fructose absorption capacity and minimal ability to regulate glucose homeostasis in response to sugar intake. Even small amounts of fruit or high-carbohydrate foods trigger sustained hyperglycemia. The disease presents as Type 2 diabetes (insulin resistance with secondary beta-cell failure) in most cases, resulting from genetic predisposition combined with dietary carbohydrate exposure. Early detection through screening and strict dietary management can prevent or delay onset in susceptible animals.",
        "description_ja": "デグーの糖尿病は非常に高い有病率（デグーの30-50%が生涯中に臨床糖尿病発展）の深刻な代謝疾患。重大：デグーは食事糖に対する貧弱な耐性—ほとんどげっ歯類と異なり、デグーは限定的な果糖吸収能と糖摂取応答における最小限のグルコース恒常性調節能。わずかな量の果物または高炭水化物食でも持続的高血糖を誘発。ほとんどの症例でtype 2糖尿病（インスリン抵抗、続発性ベータ細胞失敗）として提示、遺伝学的素因と食事炭水化物曝露による。早期検出を通じた検査と厳格食事管理は易感受性動物の発症を防止または遅延可能。",
        "urgency": "high",
        "recommended_tests": ["blood_glucose", "urinalysis", "fructosamine", "blood_chemistry", "insulin_level"],
        "causes": "DEGU-SPECIFIC GENETIC PREDISPOSITION: degus have inherited inability to metabolize sugars efficiently (genetic insulin resistance; some lines >50% lifetime diabetes prevalence vs. others 20-30%, suggesting heritable component). DIETARY RISK FACTORS (PRIMARY triggers in genetically susceptible degus): (1) DIRECT SUGAR CONTENT—fruit intake is major risk factor (even 'healthy' fruits like apples contain 10-15% sugars; 10-20g daily fruit intake significantly increases diabetes risk; some degus develop glucose intolerance after single exposure to high-sugar foods). (2) HIGH-CARBOHYDRATE PELLETS—commercial rodent/squirrel pellets often 15-20% carbohydrates (targeted toward rodents with sugar tolerance); degu-specific pellets with <2% carbohydrates essential (hay-based, not grain-based). Standard rodent pellets with >5% carbohydrate content pose risk. (3) TREATS—yogurt drops, honey sticks, granola, any sweetened foods PROHIBITED (directly cause hyperglycemic episodes). (4) HIDDEN SUGARS—some vegetables contain moderate sugars (carrots 5-7% sugar; degus can tolerate limited quantities but accumulation causes problems with high fruit + vegetable combination). SECONDARY RISK FACTORS: (1) OBESITY—excess body weight 20-30% above ideal correlates with insulin resistance progression (target body weight 200-260g for adult; obesity >280g significantly increases diabetes risk). Sedentary housing (small cages, inadequate exercise space) promotes weight gain. (2) AGING—diabetes incidence increases significantly after age 4 years (pancreatic beta-cell senescence, increasing insulin resistance with age). (3) STRESS—chronic stress (inadequate enrichment, social conflict, frequent handling) promotes insulin resistance via cortisol elevation. (4) CONCURRENT ILLNESS—respiratory infections, parasites, other diseases impair glucose tolerance, may unmask diabetes in borderline animals. (5) PREVIOUS KETOACIDOSIS EPISODE—pancreatic damage from prior DKA increases subsequent diabetes severity/recurrence risk.",
        "causes_ja": "デグー特異的遺伝学的素因：デグーは糖を効率的に代謝するための遺伝的能力欠損（遺伝学的インスリン抵抗；一部ラインは>50%生涯糖尿病有病率対他の20-30%、可遺伝成分を示唆）。食事リスク要因（遺伝学的易感受性デグーの主要トリガー）：(1) 直接糖含量—果物摂取は重大リスク要因（'健康的'果物でも10-15%糖含む；毎日10-20g果物摂取で有意に糖尿病リスク増加）。(2) 高炭水化物ペレット—商業げっ歯類/リス用ペレットは多くの場合15-20%炭水化物（糖耐性げっ歯類向け）；デグー特異的ペレット<2%炭水化物必須。(3) トリート—ヨーグルトドロップ、はちみつスティック、グラノーラ、いかなる甘い食べ物も禁止。(4) 隠れた糖—一部野菜は中程度の糖含む。二次的リスク要因：(1) 肥満。(2) 加齢。(3) ストレス。(4) 併発疾患。(5) 先行ケトアシドーシス。",
        "pathophysiology": "DEGU DIABETES PATHOPHYSIOLOGY—distinct from typical Type 2 in other species: (1) GENETIC INSULIN RESISTANCE PHASE (present from birth, asymptomatic)—pancreatic beta-cells are congenitally less responsive to glucose stimulation (insulin secretory defect; normal fasting blood glucose 100-110 mg/dL in healthy degus vs. 80-100 in other rodents). Baseline fasting insulin levels elevated 2-3× normal rodents (compensation for resistance). Glucose tolerance severely impaired: oral glucose load (1 g/kg) causes peak blood glucose >250 mg/dL at 30 min in predisposed degus vs. <180 mg/dL in most other rodents (delayed glucose clearance, insulin secretory inadequacy). (2) DIETARY CARBOHYDRATE EXPOSURE PHASE (days to weeks with sugar intake)—each sugar exposure triggers β-cell stress; hyperglycemic episodes (blood glucose 150-300 mg/dL) lasting 2-6 hours occur postprandial, then improve. Repeated episodes cause β-cell exhaustion (upregulation then downregulation of glucose transporters, mitochondrial dysfunction, eventual apoptosis). Fasting glucose progressively increases: first episode ~120 mg/dL (still normal-ish), by 10-20 episodes ~140-160 mg/dL (prediabetic range). (3) PROGRESSION TO OVERT DIABETES (weeks to months with continued sugar exposure)—fasting blood glucose rises above 140 mg/dL persistently (diagnostic threshold for diabetes in degus; >200 mg/dL common at diagnosis). Insulin levels paradoxically may decrease (β-cell failure) or remain elevated (combined resistance + inadequate secretion). (4) CHRONIC HYPERGLYCEMIA PHASE (established diabetes, months to years if untreated)—sustained blood glucose 150-400+ mg/dL causes osmotic diuresis (glucose >180 mg/dL exceeds renal threshold, spills into urine, pulls fluid, causing polyuria). Cellular dehydration despite polydipsia. Glycosuria fosters urinary tract infections (high glucose urine supports bacterial growth; 20-40% diabetic degus develop UTI). Hyperglycemia also causes: (a) PROTEIN GLYCATION—non-enzymatic glucose binding to proteins (hemoglobin, albumin, collagen) alters function; glycated hemoglobin (HbA1c) >7.5-8% indicates poor control over prior 8-12 weeks. (b) VASCULAR COMPLICATIONS—hyperglycemia damages endothelial cells via oxidative stress, aldose reductase pathway activation, advanced glycation end-product (AGE) accumulation. Microangiopathy develops: basement membrane thickening, capillary occlusion, reduced perfusion. Affected tissues: kidneys (glomerular capillary damage → proteinuria, progressive renal dysfunction), eyes (retinal capillary damage → retinopathy, vision loss in chronic cases), peripheral nerves (dorsal root ganglion degeneration, axonal loss, loss of vibration/proprioception sensation; manifests as hindlimb paresis in severe cases). (c) NEUROPATHY—hyperglycemia + ischemia cause demyelination, axonal degeneration. Clinically manifests as: mild ataxia/hindlimb weakness (early signs, weeks 2-4 of overt DM), severe paralysis (if uncontrolled >6 months, peripheral nerve damage becomes irreversible). (d) METABOLIC DERANGEMENT—hyperglycemia also causes muscle/fat catabolism (despite hyperglycemia, cells cannot take up glucose efficiently due to insulin resistance, leading to cellular energy deficit and weight loss despite normalization with insulin therapy taking days). Ketone production increases if severe (though fulminant DKA less common in Type 2 than Type 1, can occur if sudden withdrawal of carbs in strict diet creates acute caloric deficit). (5) COMPENSATORY PHASE IF DIET CORRECTED—if carbohydrate intake eliminated and dietary management tightens early (within weeks of diabetes onset), some degus show partial β-cell recovery (insulin secretion increases, fasting glucose drops 20-50 mg/dL below peak but may not normalize fully). If diet correction delayed >3-6 months, β-cell damage largely irreversible.",
        "pathophysiology_ja": "デグー糖尿病病態生理—他の種の典型的なタイプ2と異なる：(1) 遺伝学的インスリン抵抗相（出生時から存在、無症候）—膵ベータ細胞は先天的にブドウ糖刺激への反応性低下。基礎空腹時インスリン値は他のげっ歯類の2-3倍に上昇（抵抗補償）。グルコース耐性は重症傷害：経口グルコース負荷で易感受性デグーで血糖250 mg/dL以上で30分ピーク対他のげっ歯類でほぼ180 mg/dL未満。(2) 食事炭水化物曝露相（糖摂取で日から週）—各糖曝露がβ細胞ストレス誘発；高血糖エピソード発生、繰り返しエピソードでβ細胞疲弊。(3) 明白な糖尿病への進行（持続糖曝露で週から月）—空腹時血糖は140 mg/dL以上で持続上昇。(4) 慢性高血糖相（確立糖尿病、未治療で月から年）—持続血糖150-400+ mg/dL。(5) 食事が補正された場合の代償相。",
        "treatment": "DEGU DIABETES TREATMENT PROTOCOL: (1) IMMEDIATE DIAGNOSTIC CONFIRMATION & BASELINE EVALUATION: Fasting blood glucose (aim <100 mg/dL healthy, 100-140 mg/dL prediabetic, >140 mg/dL diagnostic for diabetes in degus). Fructosamine level (reflects glucose control over prior 2-3 weeks; target <300 µmol/L, >350 indicates poor control). Urinalysis (check for glycosuria [urine glucose >0], ketonuria, signs of UTI [WBC/bacteria]). Blood chemistry (BUN/creatinine assess renal function; serum glucose, triglycerides; electrolytes), Blood pressure (assess for hypertensive complications). Goal: establish diabetes severity (mild fasting 140-180 mg/dL vs. moderate 180-250 mg/dL vs. severe >250 mg/dL; determines treatment intensity). (2) DIETARY MANAGEMENT (CORNERSTONE of therapy—dietary intervention alone may reverse early diabetes): STRICT CARBOHYDRATE RESTRICTION: eliminate ALL fruits (including 'healthy' options; zero fruit is standard in diabetic degu diets), restrict vegetables to low-carbohydrate options only (lettuce, spinach, arugula, celery <1-2% carbs), eliminate all treats/seeds (nuts are high in fat, seeds too calorie-dense). TARGET DIET COMPOSITION: timothy hay-based hay 70-80% (target 18-20% crude fiber, <2% carbohydrate), degu-specific low-carb pellets 15-20% (brands: Oxbow Cavy Cuisine, Science Selective with <2% carbs; verify carbohydrate <2%), low-carb vegetables 5-10% (leafy greens only), NO fruit. Alternative: high-hay diet with minimal pellets (70-80% timothy hay + 15-20% low-carb pellets + 5-10% greens); some degus achieve glucose control on hay-only diets if diet switch early. (3) INSULIN THERAPY (if dietary management insufficient): Rapid-acting insulin analogs preferred (lispro, aspart); intermediate-acting human insulin NPH acceptable alternative. DOSING PROTOCOL: Start 0.5-1 IU/kg BID (twice daily), titrate based on glucose curves (measure fasting glucose day 3-5, adjust by 0.1-0.2 IU/kg increments weekly if needed). TARGET GLUCOSE: fasting 100-150 mg/dL (prevent hypoglycemia risk; degu hypoglycemia can cause seizures >20mg/kg below 40 mg/dL), peak postprandial <250 mg/dL. Glucose curves: measure at 0, 2, 4, 6, 8 hours post-injection on day 5 to assess insulin effect (peak effect typically 2-4 hours). Most diabetic degus require 0.5-1 IU BID for control once diet corrected; some require only 0.25 IU if caught early with strict diet. Some degus achieve remission (normal fasting glucose without insulin) if diet corrected within 3 months of diagnosis (true remission rare but possible in early Type 2). (4) ORAL HYPOGLYCEMIC AGENTS (limited use in degus but sometimes tried): Metformin 50-100 mg/kg/day PO might help with insulin sensitivity in early stages; limited evidence in degus, not standard therapy but worth trying if insulin unavailable or as adjunct. Acarbose (α-glucosidase inhibitor, 1-2 mg/kg PO before meals) delays carbohydrate absorption, may help if some carbohydrate treats unavoidable; not a substitute for dietary restriction. (5) ROUTINE MONITORING (CRITICAL for dose adjustment and complication detection): Fructosamine every 2-3 weeks during insulin titration period (guides dose adjustments). Monthly blood glucose (fasting only, or glucose curve if signs suggest inadequate control). Monthly urinalysis (monitor glycosuria improvement, detect UTI early). Serum creatinine q3-6 months (track renal function). Weight monthly (should stabilize/improve on treatment). Home glucose monitoring: if owner capable/willing, home glucometer readings (AlphaTrack 2 or Contour meters work in small animals) help guide therapy; not essential but helpful for optimal control. (6) COMPLICATION MANAGEMENT: Urinary tract infection (40-50% diabetic degus develop UTI; glycosuria creates favorable bacterial growth; treat with enrofloxacin 10-15 mg/kg q12h or trimethoprim-sulfa 15-30 mg/kg q12h × 10-14 days once diagnosed on culture). Peripheral neuropathy (if hind limb weakness develops, consider severe chronic hyperglycemia damage; thiamine supplementation 10-50 mg/kg/day might help neurological recovery, physical therapy/ramps assist mobility). Diabetic retinopathy (monitor vision; no specific treatment for retinopathy, good glycemic control prevents progression). (7) TREATMENT DURATION & GOALS: Lifelong management expected in most cases (remission possible only in minority with very early diagnosis + aggressive dietary intervention). Some owners discontinue insulin after 2-3 months if glucose normalizes and diet maintained; feasible if monthly glucose monitoring confirms continued control without insulin. Relapses common if diet loosens (even single fruit exposure can trigger relapse in susceptible degus). (8) SUPPORTIVE CARE: hydration—ensure fresh water always available (polydipsia should improve on treatment as glucose control improves). Prevent/manage obesity—weight loss if overweight (2-3% body weight loss/month acceptable, aim to reach 200-260g from obese baseline >280g). Environmental enrichment—exercise aids metabolic control (wheels, tunnels, play areas improve insulin sensitivity).",
        "treatment_ja": "デグー糖尿病治療プロトコル：(1) 直ちに診断確認と基礎評価—空腹時血糖、フルクトサミン、尿分析、血液化学。(2) 食事管理—厳密な炭水化物制限：全果物除去、野菜を低炭水化物オプションのみに制限。目標食事組成。(3) インスリン療法—迅速作用インスリン類似体が優先。(4) 経口低血糖薬。(5) 日常的監視—重大。(6) 合併症管理。(7) 治療期間と目標。(8) 支持療法。",
        "prevention": "CRITICAL PREVENTION in degus (can prevent diabetes in 50-70% of genetically susceptible animals with aggressive dietary management): (1) DEGU-SPECIFIC DIET FROM WEANING—implement strict carbohydrate-restricted diet from 4-6 weeks age (key: establish feeding habits before insulin resistance fully manifests). CORE DIET: timothy hay 75-85%, degu-specific pellets <2% carbohydrate 15-20%, vegetables only leafy greens <2% carbohydrate (spinach, romaine, arugula, kale, parsley) 0-5%, ZERO fruit at any age (not even 'small pieces' or 'occasional treats'; any fruit increases risk in susceptible degus). NO seeds (too calorie-dense, encourage snacking behavior). NO nuts (high fat, calorie-dense). NO treats (yogurt drops lethal—single treat can cause hyperglycemic spike >150 mg/dL above baseline). NO processed foods. Ensure degu-specific pellets (Oxbow Cavy Cuisine, Science Selective, Supreme Petfoods with verified <2% carbohydrate); verify carbohydrate content on label (some 'healthy' rodent pellets misleadingly labeled but contain 5-10% carbs). (2) WEIGHT MANAGEMENT—maintain ideal body weight 200-260g in adults (monthly weighing recommended; weigh at same time of day for consistency). Obesity >20% above ideal (>280g) significantly increases diabetes risk. Exercise critical: minimum 2-3 hours daily free-roaming/play outside main cage (wheels, tunnels, enrichment items), multiple degus encouraged (social play increases activity). (3) STRESS REDUCTION—minimize handling/disturbance, maintain stable daily routine, compatible pair/group housing (social housing reduces stress compared to isolation), avoid loud noises, maintain temperature 65-75°F (temperature stress impairs glucose tolerance). (4) GENETIC SCREENING/SELECTION (if breeding)—avoid animals with history of diabetes in parents/siblings; select breeding animals from lower-incidence lines if available (some breeders maintain colonies with <20% lifetime diabetes incidence vs. others >50%). (5) ROUTINE HEALTH SCREENING—quarterly physical exams in healthy degus, monthly in those >3 years age (early detection of weight changes, signs of illness affecting glucose tolerance). Fasting blood glucose screening: baseline at 6-12 months age (confirm not prediabetic), then annually for degus >2 years age (yearly screening in susceptible adults allows early detection before severe hyperglycemia develops). Fructosamine levels if concerned (reflects glucose control over prior weeks, may catch impending diabetes before overt signs appear). (6) TREAT SUGAR INTAKE AS TOXIC—client education critical: degus are NOT like hamsters/mice; sugar is not safe 'occasional treat'; even trace amounts in some vegetables (carrot treats) or from inadvertent exposure (shared food with other pets) increase risk. Single exposure studies show some degus develop hyperglycemic episodes lasting >3 hours after 5-10g fruit exposure, indicating pancreatic stress even in non-diabetic animals. (7) WATER QUALITY—ensure fresh water always available; dehydration impairs renal glucose clearance, worsens hyperglycemia if consumed carbohydrates. (8) REPRODUCTIVE MANAGEMENT—spay/neuter non-breeding degus by 4-6 months (reproductive hormones in intact animals, especially females, may influence insulin sensitivity; altered reproductive status post-spay/neuter reduces hormonal variability affecting glucose metabolism). (9) CONCURRENT DISEASE PREVENTION—promptly treat respiratory infections, GI disease, parasites (any intercurrent illness impairs glucose tolerance, may unmask diabetes; prevention of other illness indirectly prevents diabetes unmasking). (10) POST-DIAGNOSIS PREVENTION (for managing newly diagnosed diabetic degu to prevent relapse/worsening)—strict dietary adherence indefinitely (no 'occasional fruits' after diagnosis; risk of sudden hyperglycemic crisis + insulin decompensation), monthly monitoring (catch control drift early), weight management, exercise maintenance. Some degus achieve remission if diet strict from diagnosis; continuous monitoring essential as relapses occur if diet loosens.",
        "prevention_ja": "デグーの重大予防（積極的食事管理で遺伝学的易感受性動物の50-70%で糖尿病を防止可能）：(1) デグー特異的食事—離乳から厳密な炭水化物制限食を実装。(2) 体重管理。(3) ストレス低減。(4) 遺伝学的スクリーニング。(5) 日常的健康スクリーニング。(6) 砂糖摂取を毒性として扱う。(7) 水質。(8) 生殖管理。(9) 併発疾患予防。(10) 診断後予防。",
        "prognosis": "EXCELLENT (>95% long-term quality of life) if diagnosed EARLY (<4 weeks of symptoms) with IMMEDIATE dietary management to <2% carbohydrate. Fasting glucose may normalize fully (true remission) if diet intervention within 1-3 months of onset; 30-40% of early-diagnosed degus achieve remission and discontinue insulin after 2-6 months of strict diet + glucose monitoring confirming sustained normal values. Even without remission, most degus with good dietary compliance achieve stable glucose control on low-dose insulin (0.25-0.5 IU BID); life expectancy normal (4-5 years post-diagnosis with average degu lifespan 5-6 years). GOOD (80-85% quality of life) if diagnosed at 4-8 weeks symptoms but prompt dietary + insulin management. Remission unlikely at this stage (beta-cell damage more established), but control typically achieved within 2-3 weeks (fasting glucose 100-150 mg/dL, polydipsia/polyuria resolve). Lifespan slightly shortened (3-4 years post-diagnosis average, though depends on concurrent complications). GUARDED (50-70% quality of life) if diagnosis DELAYED >2 months or POOR dietary compliance after diagnosis. Glucose control more difficult (require higher insulin doses 1-2 IU BID), complications more common (UTI in 40-50%, peripheral neuropathy in 10-20% with hindlimb weakness/ataxia developing). Lifespan shortened (2-3 years post-diagnosis; renal disease complications from chronic hyperglycemia may accelerate decline). POOR (<30% quality of life or euthanasia consideration) if: (1) PRESENTATION WITH DKA (acute, severe, life-threatening). (2) SEVERE UNCONTROLLED DIABETES (persistent fasting >300 mg/dL despite insulin, indicating extreme insulin resistance or poor compliance). (3) DEVELOPMENT OF IRREVERSIBLE NEUROPATHY (severe hindlimb paralysis preventing movement; quality of life severely compromised; euthanasia often considered by owners). (4) CONCURRENT SEVERE RENAL DISEASE (BUN >80 mg/dL, creatinine >2 mg/dL; indicates advanced diabetic nephropathy; progressive renal failure likely, lifespan weeks to months without intensive intervention). SPECIAL CONSIDERATIONS: (1) DIABETIC REMISSION—true remission (normal fasting glucose without insulin after discontinuation) occurs in 30-40% of early-diagnosed degus with aggressive dietary management. Remission requires: (a) diagnosis within 4 weeks of symptom onset, (b) immediate implementation of <2% carb diet, (c) sustained excellent dietary compliance for 2-6 months before attempting insulin discontinuation, (d) documented normal fasting glucose on monthly monitoring ×3 consecutive months before declaring remission. Once remission achieved, diet must remain strict indefinitely (relapses occur if carbs reintroduced; >60% relapse rate if diet loosens). (2) RECURRENT HYPERGLYCEMIA EPISODES—even in well-controlled diabetics or those in remission, single fruit exposure or dietary deviation triggers acute hyperglycemia (blood glucose spike 100-150 mg/dL above baseline) lasting 3-6 hours; demonstrates exquisite sensitivity to carbohydrate in degu metabolism (different from other rodents). (3) AGING WITH DIABETES—degus >5 years age with diabetes show accelerated decline in control (increasing insulin requirements, more frequent glucose monitoring needed); lifespan often limited by diabetes-related complications (renal disease, infection) rather than primary aging. (4) LIFESPAN TRAJECTORY—untreated diabetes: median survival 3-4 months (progression to DKA or severe complications). Treated diabetes with good control: 3-5 years (2-4 years more than natural degu lifespan <6 years). Remission cases: normal 5-6 year lifespan possible if diabetes truly reversed and sustained dietary management.",
        "prognosis_ja": "優秀（>95%長期生活の質）—早期診断（<4週症状）で直ちに食事管理。血糖値は完全に正常化する可能性（真の寛解）；早期診断デグーの30-40%が寛解を達成、2-6ヶ月厳密食+ 監視後インスリン中止。良好（80-85%）—診断4-8週症状で急速。慎重（50-70%）—診断遅延>2ヶ月または不良食事遵守。不良（<30%）—DKA提示、重症未制御。特別な考慮：(1) 糖尿病寛解。(2) 反復的高血糖エピソード。(3) 糖尿病に伴う老化。(4) 寿命軌跡。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Diabetic Ketoacidosis",
        "name_ja": "糖尿病性ケトアシドーシス",
        "symptoms": {"lethargy", "vomiting", "dehydration", "rapid_breathing", "collapse"},
        "description": "Diabetic Ketoacidosis is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "未治療の糖尿病が悪化しケトン体が蓄積する致命的な合併症。",
        "urgency": "emergency",
        "recommended_tests": ["blood_glucose", "blood_gas", "ketone_test", "urinalysis"],
        "causes": "Occurs as a life-threatening complication of uncontrolled diabetes mellitus when ketone bodies accumulate due to severe insulin deficiency and metabolic decompensation.",
        "causes_ja": "デグーにおける糖尿病性ケトアシドーシスの原因: 未治療の糖尿病が悪化しケトン体が蓄積する致命的な合併症。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "糖尿病性ケトアシドーシスはデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "Aggressive IV fluid therapy, regular insulin infusion with close glucose monitoring, electrolyte correction (especially potassium), bicarbonate if severely acidotic, and treatment of precipitating cause.",
        "treatment_ja": "糖尿病性ケトアシドーシスはdeguでは非常に稀。報告例ではインスリン依存性で、プロジンク 0.5-1 IU/動物 SC q12h から開始、家庭での血糖モニタ（耳介穿刺、CGM試験的）と組み合わせる。低糖質・高繊維食。インスリン抵抗性をきたす副腎疾患・甲状腺疾患・肥満を除外。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "糖尿病性ケトアシドーシスの予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Guarded. With aggressive treatment, many patients recover, but mortality remains significant. Recurrence risk is high without proper long-term diabetes management.",
        "prognosis_ja": "糖尿病性ケトアシドーシスの予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Insulin Resistance",
        "name_ja": "インスリン抵抗性",
        "symptoms": {"obesity", "polyuria", "polydipsia", "hyperglycemia"},
        "description": "Insulin Resistance is a metabolic disorder affecting glucose regulation and energy metabolism.",
        "description_ja": "慢性的なインスリン抵抗性により、正常なインスリン値にもかかわらず持続的な高血糖が起こる。",
        "urgency": "moderate",
        "recommended_tests": ["blood_glucose", "insulin_level", "fructosamine"],
        "causes": "Chronic high-sugar diet leads to peripheral insulin resistance, where tissues fail to respond to normal insulin levels despite adequate pancreatic secretion.",
        "causes_ja": "デグーにおけるインスリン抵抗性の原因: 慢性的なインスリン抵抗性により、正常なインスリン値にもかかわらず持続的な高血糖が起こる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "インスリン抵抗性はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "DIETARY MANAGEMENT (CORNERSTONE): Degus are uniquely susceptible to insulin resistance due to "
        "evolutionary adaptation to arid, low-sugar environments. STRICT elimination of all simple "
        "sugars — no fruit, no commercial treats with sugar/molasses/honey, no root vegetables "
        "(carrots, sweet potato). Diet: unlimited timothy hay (≥80% of diet), small amount of "
        "degu-specific pellets (sugar-free formulation), limited fresh vegetables (dark leafy "
        "greens only — kale, dandelion, chicory). WEIGHT MANAGEMENT: Target body weight 170-300g "
        "(Syrian degu/O. degus). Weigh weekly on gram scale. Increase exercise opportunities — "
        "running wheel (≥25 cm diameter, solid surface), supervised out-of-cage time. MONITORING: "
        "Blood glucose measurement via glucometer (ear vein or tail prick) — target <200 mg/dL "
        "fasting. Fructosamine level reflects 2-3 week glycemic control. Urine dipstick for "
        "glucosuria (early indicator). PHARMACOLOGICAL: Insulin therapy is NOT recommended in "
        "degus — dietary management alone is the standard approach. Glipizide and other oral "
        "hypoglycemics have not been validated and risk severe hypoglycemia. COMPLICATION "
        "MANAGEMENT: Monitor for cataracts (bilateral lens opacity — common sequela of chronic "
        "hyperglycemia in degus, reported in up to 30% of diabetic individuals). Peripheral "
        "neuropathy may present as hind limb weakness. Hepatic lipidosis from chronic metabolic "
        "derangement. References: Edwards (2009) Vet Clin North Am Exot Anim Pract; Jekl et al. "
        "(2011) J Small Anim Pract; Quesenberry & Carpenter (2012) Ferrets, Rabbits, and "
        "Rodents 3rd ed.",
        "treatment_ja": "【食事管理（最重要）】デグーは乾燥・低糖環境への進化的適応により、インスリン抵抗性に"
        "非常に罹患しやすい。全ての単糖類を厳格に排除 — 果物、糖分/糖蜜/蜂蜜を含む市販おやつ、"
        "根菜類（ニンジン・サツマイモ）は全て禁忌。食事: チモシー牧草を無制限（食事の≥80%）、"
        "デグー専用ペレット少量（無糖配合）、限定的な新鮮野菜（葉野菜のみ — ケール、タンポポ、"
        "チコリ）。【体重管理】目標体重170-300g。週1回グラム秤で計量。運動機会の増加 — "
        "回し車（直径≥25cm、無隙間表面）、ケージ外の監視下自由時間。【モニタリング】血糖値測定"
        "（耳静脈または尾尖穿刺） — 空腹時目標<200 mg/dL。フルクトサミンで2-3週間の血糖管理を"
        "反映。尿糖検査（早期指標）。【薬物療法】デグーにインスリン療法は推奨されない — "
        "食事管理単独が標準的アプローチ。グリピジド等の経口血糖降下薬は検証されておらず、"
        "重篤な低血糖のリスクあり。【合併症管理】白内障モニタリング（両側水晶体混濁 — "
        "慢性高血糖デグーの最大30%で報告）。末梢神経障害は後肢虚弱として発現しうる。"
        "参考文献: Edwards (2009); Jekl et al. (2011); Quesenberry & Carpenter (2012).",
        "prevention": "STRICT DIETARY CONTROL is the primary prevention strategy. No fruit, no sugar-containing "
        "treats, no root vegetables, no commercial rodent treats with added sugars. Timothy hay-based "
        "diet (≥80%). Sugar-free degu-specific pellets only. Regular blood glucose screening at "
        "veterinary visits (every 6-12 months). Maintain healthy body weight through adequate exercise "
        "(running wheel, supervised play time). Owner education is critical — many owners unknowingly "
        "feed inappropriate high-sugar foods. Avoid sudden dietary changes. "
        "Reference: Edwards (2009) Vet Clin North Am Exot Anim Pract.",
        "prevention_ja": "厳格な食事管理が最も重要な予防策。果物、糖分含有おやつ、根菜類、糖分添加の市販ラット/マウス"
        "用おやつは全て禁忌。チモシー牧草ベースの食事（≥80%）。無糖デグー専用ペレットのみ。"
        "獣医診察時の定期的血糖スクリーニング（6-12ヶ月ごと）。適切な運動による健康体重維持。"
        "飼い主教育が不可欠 — 多くの飼い主が知らずに不適切な高糖食を与えている。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "インスリン抵抗性の予後: 多くの内分泌疾患は適切な薬物療法で長期管理可能。定期的なホルモン値モニタリングと用量調整が重要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Obesity",
        "name_ja": "肥満",
        "symptoms": {"weight_gain", "lethargy", "reduced_activity", "obesity"},
        "description": "Obesity is a condition of excessive body fat accumulation affecting overall health and longevity.",
        "description_ja": "過食や高糖質食による体重過多。糖尿病の素因となる。",
        "urgency": "moderate",
        "recommended_tests": ["body_condition_score", "blood_glucose"],
        "causes": "Caused by overfeeding, excessive treats, high-carbohydrate or high-fat diets, and insufficient exercise. Predisposes degus to diabetes mellitus.",
        "causes_ja": "内分泌/代謝機能に影響する食事の欠乏または過剰が原因。デグーの食性は特定の栄養バランスを必要とする。不適切な食事が主要栄養素の欠乏・過剰をもたらす。紫外線・温度・水質などの飼育因子も栄養状態に影響しうる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "デグーの内分泌/代謝機能に影響する栄養欠乏または過剰は食事の不均衡に起因する。必須栄養素の不十分な摂取が細胞機能・組織修復・免疫能を障害する。デグーの食性は特定の栄養バランスを必要とし、不適切な給餌が臨床疾患を引き起こす。慢性的な栄養不均衡は進行性の組織損傷・代謝機能障害・二次合併症をもたらす。",
        "treatment": "Treatment includes gradual caloric restriction, increased exercise, dietary reformulation, regular weight monitoring, and addressing any underlying endocrine causes.",
        "treatment_ja": "デグーにおける肥満の治療: 原因の鑑別診断に基づく特異的治療。支持療法（輸液・栄養・疼痛管理）。環境管理。定期的なモニタリングと治療調整。",
        "prevention": "Prevention includes maintaining appropriate body weight through balanced diet and adequate exercise, regular health monitoring, and avoiding high-sugar/high-fat foods.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "栄養疾患の予後は欠乏/過剰の程度と是正の速やかさに依存する。早期発見と食事是正で予後良好。重度の栄養障害や不可逆的な組織損傷がある場合は予後慎重。適切な食事指導が再発予防の鍵。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Heat Stroke",
        "name_ja": "熱中症",
        "symptoms": {"rapid_breathing", "lethargy", "collapse", "drooling", "seizures"},
        "description": "Heat Stroke is a life-threatening condition caused by failure of thermoregulatory mechanisms due to excessive heat exposure.",
        "description_ja": "デグーは暑さに弱く、30℃以上で熱中症を起こしやすい。",
        "urgency": "emergency",
        "recommended_tests": ["body_temperature", "physical_exam", "blood_work"],
        "causes": "Degus are highly susceptible to heat; environmental temperatures above 30°C can cause thermoregulatory failure. Poor ventilation and direct sunlight exposure increase risk.",
        "causes_ja": "デグーにおける熱中症の原因: 環境的危険、落下、不適切な取り扱い、同種間攻撃、捕食者攻撃、温度極端による物理的損傷。不適切な飼育環境がリスクを高める。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "熱中症はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "Treatment includes immediate cooling (cool water, fans, evaporative cooling), IV fluid therapy, monitoring for DIC and organ damage, and avoiding overcooling.",
        "treatment_ja": "デグーにおける熱中症の治療は安定化、疼痛管理、創傷ケアを優先する。生命を脅かす損傷を最初に評価・対処する（気道、呼吸、循環）。種に適した鎮痛薬（NSAIDs、オピオイド、局所麻酔薬）による鎮痛が不可欠である。創傷を洗浄・デブリードマンし、一次閉鎖、二次治癒、再建手術を適宜行う。汚染創には広域抗菌薬を使用する。骨折には副子固定または外科的固定を行う。遅発性合併症をモニタリングする。",
        "prevention": "Prevention includes maintaining appropriate ambient temperature, providing adequate shade and ventilation, ensuring water availability, and avoiding transport during extreme heat.",
        "prevention_ja": "熱中症の予防には安全で種に適した飼育環境の整備、鋭利物・危険物の除去、適切な取り扱い技術、他の動物との接触時の監視、温度管理、落下防止策が含まれる。",
        "prognosis": "Guarded to poor depending on severity and speed of treatment. DIC and multi-organ failure carry a grave prognosis. Neurological damage may be permanent.",
        "prognosis_ja": "熱中症の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Hypothermia",
        "name_ja": "低体温症",
        "symptoms": {"lethargy", "shivering", "cold_extremities", "collapse"},
        "description": "Hypothermia is a condition of dangerously low body temperature requiring immediate warming and supportive care.",
        "description_ja": "低温環境や重篤な疾患による危険な低体温。",
        "urgency": "emergency",
        "recommended_tests": ["body_temperature", "blood_glucose", "physical_exam"],
        "causes": "Caused by exposure to dangerously low ambient temperatures, drafts, or severe systemic illness leading to impaired thermoregulation.",
        "causes_ja": "デグーにおける低体温症の原因: 環境的危険、落下、不適切な取り扱い、同種間攻撃、捕食者攻撃、温度極端による物理的損傷。不適切な飼育環境がリスクを高める。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "低体温症はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "Gradual warming over 1-2h (warm hands, room 20-22°C). SC warmed fluids once responsive. Syringe feed sugar water, then recovery diet. Maintain ambient temp 18-22°C. Prognosis depends on duration.",
        "treatment_ja": "デグー低体温症の治療: ① 小型・体表/体積比大—急速低体温化。正常体温は種別（37-39℃）。② 加温: ICU/温風器26-30℃、温水パッド、温毛布。③ 温輸液: 温乳酸リンゲル 80-100 mL/kg/日 SC/IV、低血糖時は5%デキストロース併用。④ 急速加温は心電図異常リスク—0.5-1℃/h 漸進的に。⑤ 経口給餌は意識・嚥下反射回復後（シリンジ Critical Care 少量）。⑥ 原因検索: 麻酔覚醒中、ショック、敗血症、低栄養、長時間屋外曝露。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "低体温症の予防には安全で種に適した飼育環境の整備、鋭利物・危険物の除去、適切な取り扱い技術、他の動物との接触時の監視、温度管理、落下防止策が含まれる。",
        "prognosis": "Prognosis depends on severity, underlying cause, and timeliness of treatment. Early aggressive intervention generally improves outcomes. Delayed presentation carries a guarded to poor prognosis.",
        "prognosis_ja": "低体温症の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    # ── Ophthalmological ───────────────────────────────────────────────────
    {
        "name": "Diabetic Cataracts",
        "name_ja": "糖尿病性白内障",
        "symptoms": {"cloudy_eyes", "vision_loss", "bumping_into_objects", "hyperglycemia"},
        "description": "Diabetic Cataracts is an ophthalmic condition affecting the eye or surrounding structures.",
        "description_ja": "慢性的な高血糖に続発する水晶体の混濁。デグーでは非常に多い。",
        "urgency": "moderate",
        "recommended_tests": ["ophthalmic_exam", "blood_glucose", "slit_lamp_exam"],
        "causes": "Secondary to chronic hyperglycemia from diabetes mellitus, causing sorbitol accumulation in the lens via the polyol pathway, leading to osmotic swelling and opacity.",
        "causes_ja": "デグーにおける糖尿病性白内障の原因: 慢性的な高血糖に続発する水晶体の混濁。デグーでは非常に多い。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "糖尿病性白内障はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "Topical ophthalmic medication (antibiotics, anti-inflammatories, lubricants as indicated), pain management, protection from self-trauma, and monitoring for complications.",
        "treatment_ja": "糖尿病性白内障はdeguでは非常に稀。報告例ではインスリン依存性で、プロジンク 0.5-1 IU/動物 SC q12h から開始、家庭での血糖モニタ（耳介穿刺、CGM試験的）と組み合わせる。低糖質・高繊維食。インスリン抵抗性をきたす副腎疾患・甲状腺疾患・肥満を除外。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "糖尿病性白内障の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "糖尿病性白内障の予後: 早期治療で視機能温存可能。慢性疾患は長期管理が必要。網膜疾患は不可逆的な場合がある。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Senile Cataracts",
        "name_ja": "老年性白内障",
        "symptoms": {"cloudy_eyes", "vision_loss", "bumping_into_objects"},
        "description": "Senile Cataracts is an ophthalmic condition affecting the eye or surrounding structures.",
        "description_ja": "加齢に伴う水晶体の混濁で、糖尿病とは無関係に高齢デグーに見られる。",
        "urgency": "low",
        "recommended_tests": ["ophthalmic_exam", "slit_lamp_exam"],
        "causes": "Age-related progressive lens opacification unrelated to diabetes, occurring in elderly degus due to cumulative oxidative damage to lens proteins.",
        "causes_ja": "デグーにおける老年性白内障の原因: 加齢に伴う水晶体の混濁で、糖尿病とは無関係に高齢デグーに見られる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "老年性白内障はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "Topical ophthalmic medication (antibiotics, anti-inflammatories, lubricants as indicated), pain management, protection from self-trauma, and monitoring for complications.",
        "treatment_ja": "【デグーにおける老年性白内障】\n老年性白内障はデグーにおける正確な臨床評価（病歴、身体検査、CBC・生化学、画像）から治療方針を決定。\n基礎疾患の特定→特異的治療＋支持療法の組み合わせが原則。\n経過モニタリング: 主訴の改善、検査値の変化、QOLを2-4週毎に再評価。\n複雑症例はデグー専門医（ACZMまたはAVMAエキゾチック分科会等）に紹介を検討。\n支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。\n【鑑別と経過観察】類似症候を呈する疾患の除外と、治療4-8週後の再評価が予後改善の鍵。重症度・併発症によってはデグーの専門医紹介を考慮する。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "老年性白内障の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "老年性白内障の予後: 早期治療で視機能温存可能。慢性疾患は長期管理が必要。網膜疾患は不可逆的な場合がある。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Conjunctivitis",
        "name_ja": "結膜炎",
        "symptoms": {"eye_discharge", "eye_redness", "squinting", "eye_swelling"},
        "description": "Conjunctivitis is an ophthalmic condition affecting the eye or surrounding structures.",
        "description_ja": "刺激物、床材の粉塵、感染による結膜の炎症。",
        "urgency": "moderate",
        "recommended_tests": ["ophthalmic_exam", "bacterial_culture", "fluorescein_stain"],
        "causes": "Caused by irritants (dusty bedding, ammonia), bacterial or viral infection, foreign bodies, or secondary to dental disease affecting the nasolacrimal duct.",
        "causes_ja": "デグーにおける結膜炎の原因: 感染性病原体、外傷、先天性欠損、免疫介在性過程、変性変化、眼に影響する全身疾患による眼科疾患。環境因子（粉塵、UV）が寄与する。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "結膜炎はデグーにおける眼科疾患である。眼球、付属器、または視覚経路に影響を及ぼす炎症性、変性、または構造的変化を伴う。眼内炎症は血液房水関門・血液網膜関門を破壊し、蛋白漏出、細胞浸潤、視力喪失の可能性がある。眼圧上昇は視神経と網膜神経節細胞を損傷する。角膜潰瘍はデスメ膜瘤や穿孔に進行しうる。",
        "treatment": "Topical ophthalmic medication (antibiotics, anti-inflammatories, lubricants as indicated), pain management, protection from self-trauma, and monitoring for complications.",
        "treatment_ja": "デグーにおける結膜炎の治療: 点眼薬が第一選択。細菌性: オフロキサシン点眼液0.3% 1滴 q6-8h（7-14日間）。全身療法（重症例）: エンロフロキサシン5-10mg/kg PO q12h。培養感受性に基づき調整。疼痛・炎症管理: メロキシカム1-2mg/kg PO/SC q24h。歯科疾患が原因の場合は歯科処置を併行。環境改善: 低粉塵床材への変更、アンモニア濃度の低減。フルオレセイン染色で角膜潰瘍を除外。注: 経口βラクタム系抗菌薬は禁忌（致死的腸内細菌叢崩壊）。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "結膜炎の予防: 定期的な眼科検査。環境中の刺激物（粉塵、アンモニア）の低減。外傷予防。基礎疾患（高血圧等）の管理。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "結膜炎の予後: 早期治療で視機能温存可能。慢性疾患は長期管理が必要。網膜疾患は不可逆的な場合がある。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Corneal Ulcer",
        "name_ja": "角膜潰瘍",
        "symptoms": {"squinting", "eye_discharge", "eye_redness", "cloudy_eyes", "pawing_at_eye"},
        "description": "Corneal Ulcer is an ophthalmic condition affecting the eye or surrounding structures.",
        "description_ja": "外傷や感染による角膜表面の損傷。",
        "urgency": "high",
        "recommended_tests": ["fluorescein_stain", "ophthalmic_exam"],
        "causes": "Caused by trauma (bedding material, cage wire, conspecific scratches), foreign bodies, or secondary bacterial infection of the corneal epithelium.",
        "causes_ja": "眼科組織への物理的外傷が原因。転落・ケージ損傷・取扱い事故・同居個体や捕食者からの咬傷・環境危険物が一般的原因。デグーの解剖学的特性が特定の損傷タイプへの素因となりうる。二次合併症として感染・治癒遅延・慢性疼痛がある。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "デグーの眼科組織への外傷性損傷は、挫傷・裂傷・骨折を含む直接的な機械的組織損傷を引き起こす。急性炎症反応により浮腫・出血・疼痛が生じる。二次合併症として細菌汚染・感染・治癒遅延がある。デグーでは損傷からのストレスが追加の全身合併症を引き起こしうる。",
        "treatment": "Topical ofloxacin or ciprofloxacin q6-8h. Topical atropine 1% q12-24h for pain. Meloxicam 0.2 mg/kg PO q24h. No topical steroids. Fluorescein recheck in 5-7d.",
        "treatment_ja": "デグーにおける角膜潰瘍の治療: 原因の鑑別（フルオレセイン染色/シルマー試験/眼圧測定）。局所抗菌薬点眼。抗炎症薬。基礎疾患の管理。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "外傷の予後は損傷の重症度と合併症の有無に依存する。軽度外傷は適切な創傷管理で予後良好。重度外傷、多発骨折、脊髄損傷は予後慎重〜不良。早期治療と適切な疼痛管理が回復を促進する。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    # ── Dental ─────────────────────────────────────────────────────────────
    {
        "name": "Dental Malocclusion",
        "name_ja": "不正咬合",
        "symptoms": {"drooling", "appetite_loss", "weight_loss", "facial_swelling", "teeth_grinding"},
        "description": "Dental Malocclusion is a dental condition affecting tooth structure, alignment, or oral health.",
        "description_ja": "常生歯の噛み合わせ不良により痛みや摂食困難を生じる。",
        "urgency": "high",
        "recommended_tests": ["oral_exam", "skull_radiographs"],
        "causes": "Multifactorial etiology including infectious, environmental, immune, and host-related factors. Specific risk factors and triggers vary by individual case.",
        "causes_ja": "デグーにおける不正咬合の原因: デグーは常生歯（切歯・臼歯とも生涯伸長）を持つ齧歯類であり、不適切な食事（低繊維食）による咬合面の摩耗不足、遺伝的素因、外傷、カルシウム・ビタミンD代謝異常が主な原因。糖尿病を併発しやすいデグーでは代謝障害が歯質にも影響しうる。",
        "pathophysiology": "Abnormal tooth growth or alignment creates points of pressure on opposing dental surfaces and oral soft tissues, leading to pain, mucosal ulceration, and secondary infection with progressive inability to eat.",
        "pathophysiology_ja": "不正咬合はデグーにおける歯科・口腔疾患である。デグーは全ての歯が常生歯であり、歯の構造、配列、または支持組織の正常な機能が障害される。異常な歯の成長・摩耗パターンは不正咬合、歯根伸長、根尖膿瘍形成を引き起こしうる。臼歯の過成長は舌や頬粘膜への棘状突起を形成し、激しい疼痛と摂食困難を引き起こす。歯科疾患による疼痛は食欲低下、選択的摂食、体重減少、流涎として現れることが多い。",
        "treatment": "Dental correction under anesthesia (trimming, filing, extraction as needed), pain management, dietary modification to promote natural wear, and regular follow-up examinations.",
        "treatment_ja": "デグーにおける不正咬合の治療には鎮静または麻酔下での歯科検査が必要である。切歯・臼歯の過成長に対しては歯のトリミング・研磨を行い、根尖膿瘍には排膿、デブリードマン、全身性抗菌薬が必要である。メロキシカム等の鎮痛薬による疼痛管理が不可欠である。チモシー牧草主体の高繊維食への変更により自然な歯の摩耗を促進し再発を予防する。定期的な歯科検診（3-6ヶ月毎）が推奨される。",
        "prevention": "Prevention includes providing appropriate high-fiber diet to promote natural dental wear, regular dental examinations, and avoiding selective feeding.",
        "prevention_ja": "不正咬合の予防には自然な歯の摩耗を促進する適切な咀嚼材と食事、定期的な歯科検査、発生しつつある不正咬合の早期矯正、種に適した食物繊維の提供が含まれる。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "不正咬合の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Incisor Overgrowth",
        "name_ja": "切歯過長",
        "symptoms": {"drooling", "appetite_loss", "visible_tooth_overgrowth", "weight_loss"},
        "description": "Incisor Overgrowth is a dental condition affecting tooth structure, alignment, or oral health.",
        "description_ja": "切歯の過度な伸長により正常な食物の把持ができなくなる。",
        "urgency": "high",
        "recommended_tests": ["oral_exam", "skull_radiographs"],
        "causes": "Caused by congenital incisor misalignment, trauma, or insufficient gnawing material preventing normal wear of continuously growing teeth.",
        "causes_ja": "胚発生中の歯科/口腔発達異常が原因。遺伝子変異（常染色体優性・劣性・多因子性）・染色体異常・催奇形物質曝露に起因しうる。近親交配が先天性欠損のリスクを増加。特定のデグー系統に品種特異的素因が存在しうる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "デグーの歯科/口腔の先天性異常は、胚発生中の発達エラーに起因し、遺伝子変異・染色体異常・催奇形物質曝露が関与しうる。構造的または機能的欠損は出生時に明らかか、成長に伴い臨床的に顕在化する。一部のデグー系統では遺伝的要因による品種特異的素因が存在する。",
        "treatment": "Trim incisors under light isoflurane sedation using high-speed dental burr (NOT nail clippers — risk of fracture). Provide unlimited timothy hay and chew items. Check q4-8 weeks.",
        "treatment_ja": "デグーにおける切歯過長の治療: 原因の鑑別診断に基づく特異的治療。支持療法（輸液・栄養・疼痛管理）。環境管理。定期的なモニタリングと治療調整。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "先天性疾患の予後は異常の種類と重症度に依存する。軽度の機能的異常は管理可能で予後良好。重度の構造的異常は外科的介入が必要な場合があり、予後は変動的。遺伝性疾患の場合、罹患個体の繁殖は避けるべき。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Molar Spurs",
        "name_ja": "臼歯棘",
        "symptoms": {"drooling", "appetite_loss", "weight_loss", "facial_swelling"},
        "description": "Molar Spurs is a dental condition affecting tooth structure, alignment, or oral health.",
        "description_ja": "臼歯にできる鋭い突起が舌や頬を傷つける。",
        "urgency": "high",
        "recommended_tests": ["oral_exam", "skull_radiographs", "endoscopy"],
        "causes": "Caused by insufficient dietary fiber and abrasive food, leading to uneven molar wear and formation of sharp enamel points that lacerate the tongue and buccal mucosa.",
        "causes_ja": "デグーにおける臼歯棘の原因: 臼歯にできる鋭い突起が舌や頬を傷つける。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "臼歯棘はデグーにおける歯科・口腔疾患である。歯の構造、配列、または支持組織の正常な機能が障害される。異常な歯の成長・摩耗パターンは不正咬合、歯根伸長、根尖膿瘍形成を引き起こしうる。歯周病は細菌バイオフィルムの蓄積、歯肉炎症、歯周付着の進行性喪失を伴う。歯科疾患による疼痛は食欲低下、選択的摂食、体重減少、流涎として現れることが多い。",
        "treatment": "Burring under isoflurane with otoscope visualization. Syringe feed Critical Care. Meloxicam 0.2 mg/kg PO q24h. Skull radiographs for root assessment. Repeat q4-8 weeks. Provide unlimited hay.",
        "treatment_ja": "デグーにおける臼歯棘の治療には鎮静または麻酔下での歯科検査が必要である。不正咬合は種と重症度に応じて歯のトリミング、研磨、抜歯が必要となる。根尖膿瘍には排膿、デブリードマン、全身性抗菌薬が必要である。歯周病治療にはスケーリング、研磨、重度罹患歯の抜歯を含む。種に適した鎮痛薬による疼痛管理が不可欠である。食事の調整により回復を促進し再発を予防する。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "臼歯棘の予防には自然な歯の摩耗を促進する適切な咀嚼材と食事、定期的な歯科検査、発生しつつある不正咬合の早期矯正、種に適した食物繊維の提供が含まれる。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "臼歯棘の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Tooth Root Abscess",
        "name_ja": "歯根膿瘍",
        "symptoms": {"facial_swelling", "appetite_loss", "eye_discharge", "nasal_discharge", "weight_loss"},
        "description": "Tooth Root Abscess is a dental condition affecting tooth structure, alignment, or oral health.",
        "description_ja": "歯根の感染により腫脹し、副鼻腔に波及することがある。",
        "urgency": "high",
        "recommended_tests": ["skull_radiographs", "CT_scan", "bacterial_culture"],
        "causes": "Caused by bacterial infection of the tooth root, often secondary to dental malocclusion, periodontal disease, or tooth fracture allowing oral flora to invade periapical tissues.",
        "causes_ja": "デグーにおける歯根膿瘍の原因: 歯根の感染により腫脹し、副鼻腔に波及することがある。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "歯根膿瘍はデグーにおける細菌感染症である。病原菌は付着因子を通じて組織にコロニーを形成し、毒素産生、酵素分泌、免疫回避戦略などの病原性メカニズムを介して侵入する。好中球浸潤、サイトカイン放出、補体活性化を含む炎症カスケードが生じる。組織損傷は細菌の直接作用と宿主の炎症反応の両方に起因する。菌種と宿主の免疫状態に応じて、膿瘍形成、敗血症、または慢性肉芽腫性炎症が発生しうる。",
        "treatment": "Surgical debridement and extraction under isoflurane. Enrofloxacin 5-10 mg/kg PO q12h x 14d. Meloxicam 0.2 mg/kg PO q24h. Skull radiographs. Syringe feed.",
        "treatment_ja": "デグーにおける歯根膿瘍の治療には、可能であれば培養感受性試験に基づく標的抗菌薬療法が必要である。結果待ちの間は経験的広域抗菌薬を開始する。抗菌薬治療期間は感染の排除と耐性予防に十分な期間とする。膿瘍や壊死組織には外科的排膿またはデブリードマンが必要な場合がある。支持療法として輸液、鎮痛薬、抗炎症薬、栄養サポートを行う。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "歯根膿瘍の予防には適切な衛生管理・消毒、利用可能なワクチン接種、創傷の迅速な処置、ストレス軽減、適切な換気、感染動物の隔離が含まれる。",
        "prognosis": "Generally good with appropriate antimicrobial therapy and source control. Chronic or deep-seated infections may require prolonged treatment. Immunocompromised patients have a more guarded prognosis.",
        "prognosis_ja": "歯根膿瘍の予後: 多くの皮膚疾患は適切な治療で予後良好。感染性疾患は抗菌薬/抗真菌薬で治癒可能。アレルギー性は長期管理が必要。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    # ── Dermatological ─────────────────────────────────────────────────────
    {
        "name": "Ringworm (Dermatophytosis)",
        "name_ja": "皮膚糸状菌症",
        "symptoms": {"hair_loss", "crusty_skin", "itching", "circular_lesions"},
        "description": "Ringworm (Dermatophytosis) is a fungal infection that can affect skin, respiratory, or systemic organs.",
        "description_ja": "真菌による皮膚感染症で、円形の脱毛斑が生じる。",
        "urgency": "moderate",
        "recommended_tests": ["fungal_culture", "skin_scraping", "wood_lamp"],
        "treatment": "Topical and/or systemic antifungal therapy, environmental decontamination, and isolation of affected individuals. Treatment duration typically 4-8 weeks.",
        "treatment_ja": "degu皮膚糸状菌症: 局所2%ミコナゾールクリーム q12h、全身でイトラコナゾール 5-10 mg/kg PO q24h × 4-6週またはテルビナフィン 20-40 mg/kg PO q24h × 4-6週。肝酵素q2週モニタ。長毛種は毛刈り。 環境消毒（次亜塩素酸1:10）、寝床完全交換。⚠人獣共通感染症。 支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prognosis": "Good with appropriate antifungal therapy, though treatment course may be prolonged. Environmental recontamination can cause recurrence.",
        "prognosis_ja": "適切な抗真菌療法で予後良好。治療期間は長期化することがある。環境の再汚染による再発に注意。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Fur Mites (Demodex / Notoedres)",
        "name_ja": "毛包虫症",
        "symptoms": {"itching", "hair_loss", "crusty_skin", "scaly_skin", "scratching"},
        "description": "Fur Mites (Demodex / Notoedres) is a parasitic condition that causes clinical signs ranging from subclinical to severe systemic disease.",
        "description_ja": "外部寄生虫による激しいかゆみと脱毛。",
        "urgency": "moderate",
        "recommended_tests": ["skin_scraping", "microscopy"],
        "causes": "Ectoparasitic infestation causing intense itching and hair loss.",
        "causes_ja": "デグーにおける毛包虫症の原因: 外部寄生虫による激しいかゆみと脱毛。",
        "pathophysiology": "Fur Mites (Demodex / Notoedres) is a parasitic condition. Ectoparasitic infestation causing intense itching and hair loss. The parasite establishes infection through ingestion, percutaneous penetration, or vector-mediated transmission. It exploits host resources for nutrition and reproduction while evading immune defenses through antigenic variation, immunomodulation, or intracellular sequestration. Tissue damage results from direct parasitic feeding, mechanical disruption, toxic metabolic byproducts, and the host's inflammatory and immune responses. Heavy parasite burdens can lead to anemia, malnutrition, organ dysfunction, and secondary infections.",
        "pathophysiology_ja": "毛包虫症はデグーにおける寄生虫疾患である。寄生虫は経口摂取、経皮的侵入、またはベクター媒介伝播を通じて感染を確立する。抗原変異、免疫調節、細胞内隔離により宿主の免疫防御を回避しながら、宿主の栄養と資源を利用して増殖する。組織損傷は寄生虫の直接的な摂食、機械的破壊、有毒代謝副産物、宿主の炎症・免疫応答に起因する。重度の寄生虫感染は貧血、栄養失調、臓器機能障害、二次感染を引き起こしうる。",
        "treatment": "Treatment of fur mites (demodex / notoedres) in degu requires appropriate antiparasitic medication selected based on the specific parasite identified. Species-appropriate dosing is critical as some antiparasitics are toxic to certain species. Treatment may require multiple doses to eliminate all life stages. Environmental decontamination and in-contact animal treatment prevent reinfection. Supportive care addresses secondary complications such as anemia, dehydration, or malnutrition.",
        "treatment_ja": "デグーにおける毛包虫症の治療には、同定された寄生虫に応じた適切な駆虫薬が必要である。一部の駆虫薬は特定の種に有毒であるため、種に適した用量設定が重要である。全てのライフステージを排除するため複数回投与が必要な場合がある。環境消毒と接触動物の治療で再感染を防止する。貧血、脱水、栄養失調などの二次的合併症に対する支持療法を行う。",
        "prevention": "Prevention includes regular parasite screening and treatment, environmental sanitation, quarantine of new animals, and avoiding overcrowding.",
        "prevention_ja": "毛包虫症の予防には定期的な予防駆虫、環境衛生と糞便除去、新規動物の隔離・検査、ベクター防除、中間宿主や汚染環境への曝露回避が含まれる。",
        "prognosis": "Good with appropriate antiparasitic treatment. Reinfection is possible without environmental management.",
        "prognosis_ja": "毛包虫症の予後: 多くの皮膚疾患は適切な治療で予後良好。感染性疾患は抗菌薬/抗真菌薬で治癒可能。アレルギー性は長期管理が必要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Tail Degloving Injury",
        "name_ja": "尾部脱皮損傷",
        "symptoms": {"tail_injury", "bleeding", "exposed_bone", "pain"},
        "description": "Tail Degloving Injury involves traumatic injury requiring assessment of damage extent and appropriate stabilization and repair.",
        "description_ja": "尻尾を掴まれると皮膚が剥がれる。デグーの防御機構だが、再生しない。",
        "urgency": "high",
        "recommended_tests": ["physical_exam", "radiographs"],
        "causes": "Caused by grasping or restraining the degu by its tail. The tail skin is loosely attached as a predator-escape mechanism and does not regenerate once shed.",
        "causes_ja": "デグーにおける尾部脱皮損傷の原因: 尻尾を掴まれると皮膚が剥がれる。デグーの防御機構だが、再生しない。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "尾部脱皮損傷はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "Clean wound with warm saline. Topical silver sulfadiazine. If bone exposed: tail amputation under isoflurane at next viable segment. Enrofloxacin 5-10 mg/kg PO q12h x 7d. Meloxicam 0.2 mg/kg SC. NEVER grab degus by tail.",
        "treatment_ja": "デグーにおける尾部脱皮損傷の治療は安定化、疼痛管理、創傷ケアを優先する。生命を脅かす損傷を最初に評価・対処する（気道、呼吸、循環）。種に適した鎮痛薬（NSAIDs、オピオイド、局所麻酔薬）による鎮痛が不可欠である。創傷を洗浄・デブリードマンし、一次閉鎖、二次治癒、再建手術を適宜行う。汚染創には広域抗菌薬を使用する。骨折には副子固定または外科的固定を行う。遅発性合併症をモニタリングする。",
        "prevention": "Prevention includes providing safe housing, appropriate handling techniques, supervised exercise, and removal of environmental hazards.",
        "prevention_ja": "尾部脱皮損傷の予防には安全で種に適した飼育環境の整備、鋭利物・危険物の除去、適切な取り扱い技術、他の動物との接触時の監視、温度管理、落下防止策が含まれる。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "尾部脱皮損傷の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Barbering (Over-grooming)",
        "name_ja": "バーバリング（過剰毛繕い）",
        "symptoms": {"hair_loss", "patchy_fur", "stress_behavior"},
        "description": "Barbering (Over-grooming) is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "ストレスや退屈による過度な毛繕いで、自身や同居個体の毛が薄くなる。",
        "urgency": "low",
        "recommended_tests": ["behavioral_assessment", "skin_scraping"],
        "treatment": "Barbering in degus is primarily a behavioral/psychogenic condition — medical treatment alone "
        "is insufficient without addressing underlying causes. BEHAVIORAL ASSESSMENT: (1) Identify "
        "stressor — overcrowding, insufficient enrichment, social hierarchy conflicts, small cage "
        "size, boredom. Degus are highly social and require group housing (minimum 2, ideally 3-4), "
        "but social stress can trigger barbering. (2) Differentiate self-barbering from allo-barbering "
        "(dominant degu barbering cage-mates — observe interactions). ENVIRONMENTAL MODIFICATION: "
        "Larger cage (minimum 80×50×100 cm for 2-3 degus), multiple levels, running wheel (≥25 cm "
        "solid surface), dust bath (chinchilla sand) 2-3× weekly, foraging opportunities (scatter "
        "feed in hay), tunnels, chew toys (untreated wood blocks, pumice stone). SOCIAL MANAGEMENT: "
        "If allo-barbering identified, separate aggressor temporarily. Reintroduce after cage "
        "rearrangement. If persistent, permanent separation may be needed. MEDICAL RULE-OUT: "
        "Skin scraping to exclude Demodex/dermatophytosis. Fungal culture (DTM). If pruritus "
        "present — treat underlying dermatological cause rather than behavior. PHARMACOLOGICAL "
        "(LAST RESORT): Not well studied in degus. Fluoxetine 1-2 mg/kg PO q24h has been "
        "extrapolated from other rodent species for refractory cases, but evidence is anecdotal. "
        "References: Jekl & Redrobe (2013) BSAVA Manual of Rodents and Ferrets; "
        "Quesenberry & Carpenter (2012).",
        "treatment_ja": "バーバリングは主に行動学的/心因性の状態であり、根本原因への対処なしに薬物療法だけでは"
        "不十分。【行動評価】(1) ストレス源の特定 — 過密飼育、エンリッチメント不足、社会的"
        "順位争い、小さなケージ、退屈。デグーは高度に社会的で群れ飼育が必要（最低2頭、理想は"
        "3-4頭）だが、社会的ストレスがバーバリングを誘発しうる。(2) 自己バーバリングと他個体"
        "バーバリング（優位個体が同居個体を毛繕い）の鑑別 — 行動観察。【環境修正】大型ケージ"
        "（2-3頭で最低80×50×100cm）、多段構造、回し車（≥25cm無隙間表面）、砂浴び（チンチラ用"
        "サンド）週2-3回、フォレージング（牧草に餌を散布）、トンネル、かじり木。【社会管理】"
        "他個体バーバリングが判明したら攻撃者を一時的に隔離。ケージ再配置後に再導入。持続する"
        "場合は恒久的分離。【医学的除外】皮膚掻爬でデモデックス/皮膚糸状菌症を除外。真菌培養"
        "（DTM）。掻痒がある場合は行動ではなく基礎皮膚疾患を治療。【薬物療法（最終手段）】"
        "デグーでは十分に研究されていない。フルオキセチン1-2 mg/kg PO q24hが他の齧歯類から"
        "外挿されているが、エビデンスは逸話的。",
        "prognosis": "Good prognosis when underlying behavioral/environmental cause is identified and corrected. "
        "Hair regrowth occurs within 4-6 weeks after stressor removal. Refractory cases with "
        "persistent self-barbering despite environmental modification carry a guarded prognosis — "
        "may indicate underlying chronic pain or anxiety disorder. Allo-barbering usually resolves "
        "with social restructuring. No direct impact on lifespan unless secondary skin infections "
        "develop from excoriated areas.",
        "prognosis_ja": "行動学的/環境的原因が特定・是正されれば予後良好。ストレス源除去後4-6週間で毛の再生。"
        "環境修正にもかかわらず持続する自己バーバリングは予後慎重 — 慢性疼痛や不安障害が基礎に"
        "ある可能性。他個体バーバリングは社会的再構築で通常改善。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Bite Wounds / Abscess",
        "name_ja": "咬傷・膿瘍",
        "symptoms": {"swelling", "pain", "discharge", "lethargy", "fever"},
        "description": "Bite Wounds / Abscess involves traumatic injury requiring assessment of damage extent and appropriate stabilization and repair.",
        "description_ja": "同居個体との争いによる咬傷が感染し膿瘍を形成する。",
        "pathophysiology_ja": "咬傷・膿瘍は咬傷や外傷を介して細菌が皮下・組織内に侵入して形成される膿瘍である。侵入した細菌が増殖すると好中球が動員され、組織壊死と膿（死滅した好中球・細菌・壊死組織）が被膜に包まれて貯留する。膿瘍は周囲組織を圧迫し、破裂・全身播種により蜂窩織炎や敗血症へ進展しうる。外科的な切開排膿とドレナージが治癒に不可欠である。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam", "bacterial_culture", "cytology"],
        "treatment": "Antimicrobial therapy based on culture and sensitivity, wound care or drainage as needed, pain management, and monitoring for resolution.",
        "treatment_ja": "【デグーにおける咬傷・膿瘍】\n咬傷・膿瘍は培養感受性試験を診療指針とし、empiricalにはエンロフロキサシン 5-15 mg/kg PO/IM q12-24h またはアモキシシリン・クラブラン酸 12.5-25 mg/kg PO q12h（小型哺乳類除く）を開始。\n膿瘍形成例は外科的切開・排膿・洗浄（生食または0.05%クロルヘキシジン）が抗菌薬単独より治癒率高い。\n発熱・全身症状時は炎症マーカー（SAA、CRP）と血液培養。\n再発リスクの高い症例ではバイオフィルム形成菌（Pseudomonas, Staphylococcus pseudintermedius MRSP）を疑い、長期抗菌薬を6-8週継続。\n支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。\n【鑑別と経過観察】類似症候を呈する疾患の除外と、治療4-8週後の再評価が予後改善の鍵。重症度・併発症によってはデグーの専門医紹介を考慮する。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "適切な抗菌薬療法と感染源制御で予後良好。慢性または深部感染は長期管理が必要。免疫不全の個体はより予後要注意。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Contact Dermatitis",
        "name_ja": "接触性皮膚炎",
        "symptoms": {"skin_redness", "itching", "hair_loss", "crusty_skin"},
        "description": "Contact Dermatitis is a dermatological condition affecting the skin, coat, or integumentary system.",
        "description_ja": "床材や洗浄剤などとの接触による皮膚の炎症。",
        "urgency": "low",
        "recommended_tests": ["physical_exam", "skin_scraping", "allergy_testing"],
        "causes": "Skin disease from infectious agents (bacterial, fungal, parasitic), allergic reactions, autoimmune processes, hormonal imbalances, environmental irritants, or nutritional deficiencies.",
        "causes_ja": "デグーにおける接触性皮膚炎の原因: 感染性病原体（細菌、真菌、寄生虫）、アレルギー反応、自己免疫過程、ホルモン異常、環境刺激物、栄養欠乏による皮膚疾患。",
        "pathophysiology": "Contact Dermatitis is a dermatological condition. Contact Dermatitis The skin pathology involves disruption of the epidermal barrier, dermal inflammation, or adnexal dysfunction. Compromised barrier function permits transepidermal water loss, allergen penetration, and microbial colonization. Inflammatory mediators (histamine, prostaglandins, cytokines) drive pruritus, erythema, and secondary excoriation. Chronic disease leads to epidermal hyperplasia, lichenification, hyperpigmentation, and fibrosis.",
        "pathophysiology_ja": "接触性皮膚炎はデグーにおける皮膚疾患である。表皮バリア、真皮炎症、または付属器機能の障害を伴う。バリア機能の低下により経表皮水分喪失、アレルゲン浸透、微生物コロニー形成が促進される。炎症メディエーター（ヒスタミン、プロスタグランジン、サイトカイン）が掻痒、紅斑、二次的な擦過傷を駆動する。慢性疾患では表皮過形成、苔癬化、色素沈着、線維化が生じる。",
        "treatment": "Topical treatment, systemic therapy if indicated, environmental modification (appropriate substrate, weight management), and addressing underlying cause.",
        "treatment_ja": "デグーにおける接触性皮膚炎の治療: 原因物質の同定と除去が最重要（刺激性の床材、洗浄剤、塗料等）。床材を紙系やアスペン材に変更。抗炎症: メロキシカム1-2mg/kg PO/SC q24h（3-5日間）。局所療法: クロルヘキシジン0.05%で患部洗浄、必要に応じてミコナゾール/クロルヘキシジンシャンプー。二次感染がある場合: エンロフロキサシン5-10mg/kg PO q12h（7-14日間）。掻痒が著しい場合は環境エンリッチメントで気を逸らす。注: 経口βラクタム系抗菌薬は禁忌。",
        "prevention": "Prevention of contact dermatitis includes appropriate husbandry, balanced species-specific nutrition, regular veterinary health checks, stress minimization, maintaining clean living conditions, and prompt attention to early clinical signs.",
        "prevention_ja": "接触性皮膚炎の予防: 定期的な被毛・皮膚チェック。適切な飼育環境の衛生管理。寄生虫の定期的な予防駆虫。バランスの取れた食事。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "接触性皮膚炎の予後: 多くの皮膚疾患は適切な治療で予後良好。感染性疾患は抗菌薬/抗真菌薬で治癒可能。アレルギー性は長期管理が必要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    # ── Musculoskeletal ────────────────────────────────────────────────────
    {
        "name": "Bumblefoot (Pododermatitis)",
        "name_ja": "趾瘤症（バンブルフット）",
        "symptoms": {"swollen_feet", "lameness", "foot_sores", "reluctance_to_move"},
        "description": "Bumblefoot (Pododermatitis) is a dermatological condition affecting the skin, coat, or integumentary system.",
        "description_ja": "金網の床や不衛生な環境による足底の感染と炎症。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam", "radiographs", "bacterial_culture"],
        "causes": "Caused by pressure necrosis and secondary bacterial infection of the foot pad, typically from wire-mesh flooring, unsanitary conditions, obesity, or rough substrates.",
        "causes_ja": "デグーの筋骨格系組織における炎症過程が原因。感染・外傷・自己免疫応答・中毒曝露・異物反応が誘因。慢性炎症は持続的な抗原刺激や免疫調節異常に起因しうる。デグーの種特異的炎症反応は家畜種と異なりうる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "デグーの筋骨格系組織における炎症過程は、自然免疫および適応免疫応答の活性化を伴う。炎症性サイトカイン（TNF-α、IL-1、IL-6）とケモカインが好中球・マクロファージ・リンパ球を患部組織に動員する。持続的炎症は組織浮腫・血管透過性変化・進行性組織損傷をもたらす。デグーの生理学的特性が炎症反応パターンと治癒能力に影響しうる。",
        "treatment": "Debride necrotic tissue. Topical silver sulfadiazine. Bandage q48h. Enrofloxacin 5-10 mg/kg PO q12h x 14d if systemic. Meloxicam 0.2 mg/kg PO q24h. Improve bedding (soft, clean). Remove wire mesh floors.",
        "treatment_ja": "デグー足底皮膚炎（バンブルフット/Pododermatitis）: 環境改善が治療の根幹。① 環境改善: 床材を柔らかいもの（タオル、Vetbed、人工芝）に変更、湿潤回避、止まり木の太さ・形状を見直す（鳥）。② 局所処置: ぬるま湯と0.05%クロルヘキシジン洗浄 q12h、外用シルバースルファジアジン or Manuka honey、患部包帯（鳥はballブートやテープシューズ）。③ 重症例（潰瘍・骨髄炎）: 培養感受性後の全身抗菌薬—エンロフロキサシン 10-15 mg/kg PO/IM q12-24h、アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h（鳥含む）、4-8週継続。④ 外科的デブリードマン（壊死組織除去）必要例あり。⑤ 鎮痛: メロキシカム 0.5-1 mg/kg PO q12-24h。⑥ 肥満は最大のリスク因子—体重管理（特に飛ばない大型鳥、ウサギ、モルモット）。⑦ ビタミンA欠乏（鳥）も誘因—食事改善（種子食偏重を脱却）。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "炎症性疾患の予後は原因の特定と除去、治療反応に依存する。急性炎症は適切な治療で予後良好な場合が多い。慢性炎症は長期管理が必要で、進行性臓器障害のリスクがある。抗炎症療法と原因治療の併用が予後改善に重要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Limb Fracture",
        "name_ja": "四肢骨折",
        "symptoms": {"lameness", "swelling", "pain", "limb_deformity", "reluctance_to_move"},
        "description": "Limb Fracture involves traumatic injury requiring assessment of damage extent and appropriate stabilization and repair.",
        "description_ja": "落下、回し車の事故、ケージへの挟まりによる骨折。",
        "urgency": "high",
        "recommended_tests": ["radiographs", "physical_exam"],
        "causes": "Caused by falls from height, exercise wheel entrapment, cage bar injuries, or improper handling. Metabolic bone disease may predispose to pathological fractures.",
        "causes_ja": "筋骨格系組織への物理的外傷が原因。転落・ケージ損傷・取扱い事故・同居個体や捕食者からの咬傷・環境危険物が一般的原因。ウサギの解剖学的特性が特定の損傷タイプへの素因となりうる。二次合併症として感染・治癒遅延・慢性疼痛がある。",
        "pathophysiology": "Mechanical force exceeds bone strength, causing cortical disruption. Associated soft tissue damage, hemorrhage, and inflammation follow. Healing proceeds through hematoma formation, callus development, and remodeling.",
        "pathophysiology_ja": "デグーの筋骨格系組織への外傷性損傷は、挫傷・裂傷・骨折を含む直接的な機械的組織損傷を引き起こす。急性炎症反応により浮腫・出血・疼痛が生じる。二次合併症として細菌汚染・感染・治癒遅延がある。デグーでは損傷からのストレスが追加の全身合併症を引き起こしうる。",
        "treatment": "Fracture stabilization (splinting, surgical fixation), pain management with multimodal analgesia, restricted activity, and monitoring for healing complications.",
        "treatment_ja": "デグー四肢折: ① 小型・骨脆弱性が外科的固定を難しくする—保存的治療（副木）が多い。四肢骨折は副木またはTape splint、長管骨は外科固定検討、関節を跨ぐ場合は早期可動域訓練。② 安定化: 副木（Robert Jones、軽量副木）またはケージ制限、4-6週で癒合。③ 重症・長管骨は外科的固定（mini IM pin、外固定）—専門医推奨。④ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h。⑤ 開放骨折: 培養感受性後の抗菌薬（草食種は経口β-ラクタム禁忌、エンロフロキサシン 5-10 mg/kg PO q12-24h）。⑥ ケージ制限: ステップ・ハンモック撤去、床に柔らかいパッド、シリンジ給餌で活動を最小化。⑦ 経過: X線3-4週毎、若齢は癒合早い（2-4週）。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes providing safe housing, appropriate handling techniques, supervised exercise, and removal of environmental hazards.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Good for uncomplicated fractures with appropriate stabilization. Open fractures and those with concurrent injuries carry a more guarded prognosis.",
        "prognosis_ja": "外傷の予後は損傷の重症度と合併症の有無に依存する。軽度外傷は適切な創傷管理で予後良好。重度外傷、多発骨折、脊髄損傷は予後慎重〜不良。早期治療と適切な疼痛管理が回復を促進する。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Spinal Fracture",
        "name_ja": "脊椎骨折",
        "symptoms": {"hind_leg_paralysis", "pain", "incontinence", "reluctance_to_move"},
        "description": "Spinal Fracture involves traumatic injury requiring assessment of damage extent and appropriate stabilization and repair.",
        "description_ja": "落下や外傷による脊椎の骨折で麻痺を引き起こす。",
        "urgency": "emergency",
        "recommended_tests": ["radiographs", "neurological_exam"],
        "causes": "Caused by falls, traumatic handling, or cage accidents resulting in vertebral fracture with potential spinal cord compression and paralysis.",
        "causes_ja": "デグーにおける脊椎骨折の原因: 落下や外傷による脊椎の骨折で麻痺を引き起こす。",
        "pathophysiology": "Mechanical force exceeds bone strength, causing cortical disruption. Associated soft tissue damage, hemorrhage, and inflammation follow. Healing proceeds through hematoma formation, callus development, and remodeling.",
        "pathophysiology_ja": "脊椎骨折はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "Treatment includes fracture stabilization (splinting, pinning, or plating), pain management, restricted activity, and monitoring for healing. Physical rehabilitation may be beneficial.",
        "treatment_ja": "デグー脊椎折: ① 小型・骨脆弱性が外科的固定を難しくする—保存的治療（副木）が多い。脊椎骨折は厳格な ケージ制限・脊柱安定化、神経学的評価（運動・感覚・尿便）必須、損傷高位の特定で予後判断。② 安定化: 副木（Robert Jones、軽量副木）またはケージ制限、4-6週で癒合。③ 重症・長管骨は外科的固定（mini IM pin、外固定）—専門医推奨。④ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h。⑤ 開放骨折: 培養感受性後の抗菌薬（草食種は経口β-ラクタム禁忌、エンロフロキサシン 5-10 mg/kg PO q12-24h）。⑥ ケージ制限: ステップ・ハンモック撤去、床に柔らかいパッド、シリンジ給餌で活動を最小化。⑦ 経過: X線3-4週毎、若齢は癒合早い（2-4週）。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes providing safe housing, appropriate handling techniques, supervised exercise, and removal of environmental hazards.",
        "prevention_ja": "脊椎骨折の予防には安全で種に適した飼育環境の整備、鋭利物・危険物の除去、適切な取り扱い技術、他の動物との接触時の監視、温度管理、落下防止策が含まれる。",
        "prognosis": "Generally good for isolated fractures with appropriate fixation. Prognosis worsens with concurrent soft tissue injury, open fractures, or delayed treatment.",
        "prognosis_ja": "脊椎骨折の予後: 骨折は適切な固定で予後良好。変性性疾患は進行性だが疼痛管理でQOL維持可能。若齢動物は回復力が高い。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Osteoarthritis",
        "name_ja": "変形性関節症",
        "symptoms": {"lameness", "reduced_activity", "stiffness", "reluctance_to_move"},
        "description": "Osteoarthritis is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "加齢に伴う関節の変性疾患。",
        "urgency": "low",
        "recommended_tests": ["radiographs", "physical_exam"],
        "causes": "Progressive degenerative joint disease caused by aging, chronic wear, genetic predisposition, and prior joint trauma or obesity.",
        "causes_ja": "加齢・慢性的摩耗・累積的損傷による筋骨格系組織の進行性劣化が原因。遺伝的素因・慢性炎症・酸化ストレス・不適切な飼育条件が寄与。デグーの飼育管理と食事因子が変性変化を加速しうる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "デグーの筋骨格系組織における進行性変性変化は、細胞構造と機能の漸進的喪失を伴う。酸化ストレス・慢性炎症・細胞老化・組織修復障害が関与する。加齢変化・累積的環境侵襲・遺伝的素因が疾患進行に寄与する。飼育管理と食事要因が変性疾患を悪化させうる。",
        "treatment": "PAIN MANAGEMENT (PRIMARY GOAL): Meloxicam 1-2 mg/kg PO/SC q24h — first-line NSAID for "
        "degus, well tolerated for long-term use. Start at lower dose and titrate based on response. "
        "Tramadol 5-10 mg/kg PO q12h for additional analgesia in moderate-severe cases. "
        "Buprenorphine 0.05-0.1 mg/kg SC q8-12h for acute flare-ups. WEIGHT MANAGEMENT: Obesity "
        "exacerbates joint disease — target ideal body weight (170-300g). Strict timothy hay diet, "
        "no sugar/fruit (diabetes prevention AND weight control). ENVIRONMENTAL MODIFICATION: "
        "Lower cage platforms (reduce jumping height to ≤15 cm between levels). Ramps instead of "
        "ladders between levels. Soft bedding (paper-based, deep layer). Remove running wheel if "
        "lameness is severe — replace with gentle exercise opportunities. Maintain ambient "
        "temperature 20-22°C (cold worsens joint stiffness). JOINT SUPPORT SUPPLEMENTS: "
        "Glucosamine/chondroitin (extrapolated from other species — limited evidence in degus). "
        "Omega-3 fatty acids (flaxseed, minimal amount). RADIOGRAPHIC MONITORING: Periodic "
        "radiographs to assess disease progression. Differentiate from metabolic bone disease "
        "(MBD) — check calcium, phosphorus, vitamin D status. SURGICAL INTERVENTION: Rarely "
        "indicated in degus due to small size and anesthesia risk. Joint luxation may require "
        "reduction. Severe cases with poor quality of life — consider humane euthanasia. "
        "NOTE: Oral β-lactam antibiotics are CONTRAINDICATED in degus (fatal dysbiosis). "
        "References: Quesenberry & Carpenter (2012); Jekl & Redrobe (2013) BSAVA Manual.",
        "treatment_ja": "【疼痛管理（主要目標）】メロキシカム1-2 mg/kg PO/SC q24h — デグーの第一選択NSAID、"
        "長期使用で忍容性良好。低用量から開始し反応に基づき漸増。トラマドール5-10 mg/kg "
        "PO q12h（中等度〜重度の追加鎮痛）。ブプレノルフィン0.05-0.1 mg/kg SC q8-12h"
        "（急性増悪時）。【体重管理】肥満は関節疾患を悪化 — 理想体重（170-300g）を目標。"
        "チモシー牧草厳格食（糖尿病予防＋体重管理）。【環境修正】ケージ段差を低く（レベル間"
        "≤15cm）。梯子の代わりにスロープ。柔らかい床材（紙製、厚い層）。重度跛行時は回し車を"
        "撤去。室温20-22°C維持（寒冷は関節硬直を悪化）。【関節サポート】グルコサミン/"
        "コンドロイチン（他種からの外挿）。オメガ3脂肪酸（亜麻仁、少量）。【画像モニタリング】"
        "定期的X線で進行評価。代謝性骨疾患（MBD）との鑑別 — Ca/P/VitD確認。【外科】"
        "デグーでは小型サイズと麻酔リスクにより稀。注: 経口βラクタム系抗菌薬は禁忌。",
        "prevention": "Maintain healthy body weight through appropriate timothy hay-based diet and regular exercise. "
        "Provide cage with appropriate platform heights (reduce impact on joints). Avoid obesity — "
        "the most modifiable risk factor. No sugar/fruit (prevents diabetes which exacerbates "
        "degenerative conditions). Adequate calcium and vitamin D for bone health. Regular "
        "veterinary checkups including mobility assessment in senior degus (>4 years). "
        "Reference: Jekl & Redrobe (2013) BSAVA Manual of Rodents and Ferrets.",
        "prevention_ja": "チモシー牧草ベースの適切な食事と運動による健康体重維持。適切な段差のケージ設計。"
        "肥満回避（最も修正可能なリスク因子）。糖分/果物禁止（変性疾患を悪化させる糖尿病予防）。"
        "骨の健康のための適切なカルシウムとビタミンD。高齢デグー（>4歳）の定期健診で運動機能評価。",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "変性疾患の予後は進行速度と管理可能性に依存する。緩徐進行性の場合、適切な対症療法とQOL管理で長期生存が可能。急速進行性の場合は予後不良。定期的な再評価と治療調整が重要。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    # ── Respiratory ────────────────────────────────────────────────────────
    {
        "name": "Upper Respiratory Infection",
        "name_ja": "上部気道感染症",
        "symptoms": {"sneezing", "nasal_discharge", "lethargy", "appetite_loss"},
        "description": "Upper Respiratory Infection is a bacterial infection that causes systemic or localized inflammatory disease requiring prompt antimicrobial therapy.",
        "description_ja": "細菌またはウイルスによる上部気道の感染症。",
        "urgency": "moderate",
        "recommended_tests": ["nasal_culture", "physical_exam", "radiographs"],
        "causes": "Caused by bacterial pathogens (Pasteurella, Bordetella, Streptococcus) or viral agents, often precipitated by stress, overcrowding, poor ventilation, or immunosuppression.",
        "causes_ja": "デグーにおける上部気道感染症の原因: デグーにおける細菌性の呼吸器系疾患。上部気道感染症は適切な診断と治療管理が重要である。早期発見と適切な介入が予後改善の鍵となる。",
        "pathophysiology": "Bacterial organisms invade host tissues, triggering inflammatory cascades with neutrophil recruitment, cytokine release, and potential tissue necrosis. Systemic spread may lead to bacteremia and multi-organ dysfunction.",
        "pathophysiology_ja": "上部気道感染症はデグーにおける呼吸器疾患である。気道、肺実質、または胸膜腔の炎症、閉塞、または機能障害を伴う。ガス交換の障害により低酸素血症および高炭酸ガス血症の可能性がある。炎症性滲出液、粘液蓄積、構造変化が有効な換気を低下させる。代償性頻呼吸により呼吸仕事量と代謝要求が増加する。重症例は呼吸不全に進行し緊急介入が必要となりうる。",
        "treatment": "Antimicrobial therapy based on culture and sensitivity, wound care or drainage as needed, pain management, and monitoring for resolution.",
        "treatment_ja": "デグーにおける上部気道感染症の治療: 第一選択抗菌薬: エンロフロキサシン5-10mg/kg PO q12h（14-21日間）。代替: トリメトプリム-スルファメトキサゾール30mg/kg PO q12h。鼻汁培養感受性に基づき調整。抗炎症・疼痛管理: メロキシカム1-2mg/kg PO/SC q24h。ネブライザー療法: 生理食塩水 15分 q8-12h（鼻閉改善）。食欲低下時は強制給餌（クリティカルケア）。脱水がある場合は皮下補液（維持量100ml/kg/日）。環境改善: 換気、低粉塵床材、適切な温度20-22℃、湿度40-60%。注: 経口βラクタム系抗菌薬は禁忌。",
        "prevention": "Prevention includes maintaining proper hygiene, appropriate husbandry, stress reduction, quarantine of new animals, and prompt treatment of wounds or primary conditions.",
        "prevention_ja": "上部気道感染症の予防: 適切な換気と空気質管理。粉塵の少ない床材。過密飼育の回避。適切な温湿度管理。ストレス軽減。",
        "prognosis": "Good with appropriate antimicrobial therapy. Most infections resolve with proper treatment. Chronic or recurrent cases may require longer management.",
        "prognosis_ja": "上部気道感染症の予後: 軽度の上部気道感染は治療に良好に反応。肺炎は早期治療で予後改善。慢性呼吸器疾患は長期管理が必要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Pneumonia",
        "name_ja": "肺炎",
        "symptoms": {"labored_breathing", "nasal_discharge", "lethargy", "appetite_loss", "cyanosis"},
        "description": "Pneumonia is a respiratory condition affecting the airways or lungs, causing breathing difficulty.",
        "description_ja": "肺の感染または炎症で、しばしば上部気道感染に続発する。",
        "urgency": "high",
        "recommended_tests": ["chest_radiographs", "blood_work", "bacterial_culture"],
        "causes": "Caused by bacterial, viral, or fungal pathogens infecting the lung parenchyma, often secondary to upper respiratory infection. Environmental factors such as poor ventilation and ammonia exposure increase risk.",
        "causes_ja": "デグーにおける肺炎の原因: 感染性病原体（ウイルス、細菌、真菌）、環境刺激物（粉塵、アンモニア）、アレルギー反応、異物誤嚥、解剖学的異常による呼吸器疾患。換気不良がリスクを高める。",
        "pathophysiology": "Inflammation and exudate accumulation in airways or alveoli impair gas exchange, leading to hypoxemia. Mucosal damage reduces clearance mechanisms, promoting secondary infection.",
        "pathophysiology_ja": "肺炎はデグーにおける呼吸器疾患である。気道、肺実質、または胸膜腔の炎症、閉塞、または機能障害を伴う。ガス交換の障害により低酸素血症および高炭酸ガス血症の可能性がある。炎症性滲出液、粘液蓄積、構造変化が有効な換気を低下させる。代償性頻呼吸により呼吸仕事量と代謝要求が増加する。重症例は呼吸不全に進行し緊急介入が必要となりうる。",
        "treatment": "Enrofloxacin 5-10 mg/kg PO/SC q12h x 14-21d. Nebulization with 0.9% NaCl q8-12h. SC fluids. Keep at 18-22°C. Oxygen supplementation.",
        "treatment_ja": "デグーにおける肺炎の治療: 外科的介入（肺炎に対する適切な術式）。術前安定化: 輸液療法、メロキシカム1-2mg/kg PO/SC q24h（疼痛管理）。周術期抗菌薬: エンロフロキサシン5-10mg/kg PO q12h（経口βラクタム禁忌）。栄養サポート、環境温度管理、定期的モニタリング。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "肺炎の予防: 適切な換気と空気質管理。粉塵の少ない床材。過密飼育の回避。適切な温湿度管理。ストレス軽減。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "肺炎の予後: 軽度の上部気道感染は治療に良好に反応。肺炎は早期治療で予後改善。慢性呼吸器疾患は長期管理が必要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Aspiration Pneumonia",
        "name_ja": "誤嚥性肺炎",
        "symptoms": {"labored_breathing", "coughing", "lethargy", "fever", "nasal_discharge"},
        "description": "Aspiration Pneumonia is a respiratory condition affecting the airways or lungs, causing breathing difficulty.",
        "description_ja": "食物や液体の誤嚥による肺感染。不適切なシリンジ給餌が原因になりやすい。",
        "urgency": "emergency",
        "recommended_tests": ["chest_radiographs", "blood_work"],
        "causes": "Caused by accidental inhalation of food, water, or oral secretions into the lungs, commonly from improper syringe feeding technique.",
        "causes_ja": "呼吸器系組織への物理的外傷が原因。転落・ケージ損傷・取扱い事故・同居個体や捕食者からの咬傷・環境危険物が一般的原因。デグーの解剖学的特性が特定の損傷タイプへの素因となりうる。二次合併症として感染・治癒遅延・慢性疼痛がある。",
        "pathophysiology": "Inflammation and exudate accumulation in airways or alveoli impair gas exchange, leading to hypoxemia. Mucosal damage reduces clearance mechanisms, promoting secondary infection.",
        "pathophysiology_ja": "デグーの呼吸器系組織への外傷性損傷は、挫傷・裂傷・骨折を含む直接的な機械的組織損傷を引き起こす。急性炎症反応により浮腫・出血・疼痛が生じる。二次合併症として細菌汚染・感染・治癒遅延がある。デグーでは損傷からのストレスが追加の全身合併症を引き起こしうる。",
        "treatment": "Treatment includes oxygen supplementation, antimicrobial or antifungal therapy as indicated, bronchodilators, nebulization, and supportive care. Severe cases may require hospitalization.",
        "treatment_ja": "デグーにおける誤嚥性肺炎の治療: 抗菌薬（培養感受性に基づく）。ネブライゼーション。酸素療法（重症時）。保温。栄養サポート。環境改善（換気・粉塵低減）。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "外傷の予後は損傷の重症度と合併症の有無に依存する。軽度外傷は適切な創傷管理で予後良好。重度外傷、多発骨折、脊髄損傷は予後慎重〜不良。早期治療と適切な疼痛管理が回復を促進する。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    # ── Gastrointestinal ───────────────────────────────────────────────────
    {
        "name": "Gastrointestinal Stasis",
        "name_ja": "消化管うっ滞",
        "symptoms": {"appetite_loss", "bloating", "reduced_fecal_output", "lethargy", "teeth_grinding"},
        "description": "Gastrointestinal Stasis is a gastrointestinal condition affecting digestive function and nutrient absorption.",
        "description_ja": "ストレスや食事、痛みによる腸管運動の低下または停止。",
        "urgency": "high",
        "recommended_tests": ["abdominal_radiographs", "physical_exam"],
        "causes": "Caused by stress, pain, low-fiber diet, dehydration, or concurrent illness leading to decreased or absent gastrointestinal motility.",
        "causes_ja": "デグーにおける消化管うっ滞の原因: ストレスや食事、痛みによる腸管運動の低下または停止。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "消化管うっ滞はデグーにおける消化器疾患である。粘膜の完全性、運動性、分泌機能、またはマイクロバイオームバランスの障害を伴う。炎症により上皮バリアが損傷し、吸収不良、体液喪失、細菌トランスロケーションの可能性がある。運動障害（低運動性/うっ滞または亢進）により通過時間と消化効率が変化する。後腸発酵動物では盲腸/結腸フローラの破壊が致死的ディスバイオーシスと腸管毒素症を引き起こしうる。",
        "treatment": "SC fluids (LRS). Metoclopramide 0.5 mg/kg SC q8h. Syringe feed Critical Care q4-6h. Simethicone 20 mg/kg PO q8h for gas. Meloxicam 0.2 mg/kg SC. Provide unlimited timothy hay once eating.",
        "treatment_ja": "デグーにおける消化管うっ滞の治療: 外科的介入（消化管うっ滞に対する適切な術式）。術前安定化: 輸液療法、メロキシカム1-2mg/kg PO/SC q24h（疼痛管理）。周術期抗菌薬: エンロフロキサシン5-10mg/kg PO q12h（経口βラクタム禁忌）。栄養サポート、環境温度管理、定期的モニタリング。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "消化管うっ滞の予防: 適切な食事管理（急激な食事変更を避ける）。繊維質の適切な摂取。異物誤食の予防。定期的な糞便検査。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "消化管うっ滞の予後: 急性消化器疾患は多くが治療に良好に反応。閉塞性疾患は早期外科介入で予後良好。慢性疾患は食事管理で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Bloat (Gastric Dilation)",
        "name_ja": "鼓脹症",
        "symptoms": {"bloating", "pain", "lethargy", "rapid_breathing", "appetite_loss"},
        "description": "Bloat (Gastric Dilation) is a gastrointestinal condition affecting digestive function and nutrient absorption.",
        "description_ja": "胃内のガス蓄積により膨満と痛みが生じる。",
        "urgency": "emergency",
        "recommended_tests": ["abdominal_radiographs", "physical_exam"],
        "causes": "Caused by excessive gas production from dietary imbalance, rapid dietary changes, or fermentable carbohydrate intake leading to acute gastric distension.",
        "causes_ja": "デグーにおける鼓脹症の原因: 胃内のガス蓄積により膨満と痛みが生じる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "鼓脹症はデグーにおける消化器疾患である。粘膜の完全性、運動性、分泌機能、またはマイクロバイオームバランスの障害を伴う。炎症により上皮バリアが損傷し、吸収不良、体液喪失、細菌トランスロケーションの可能性がある。運動障害（低運動性/うっ滞または亢進）により通過時間と消化効率が変化する。後腸発酵動物では盲腸/結腸フローラの破壊が致死的ディスバイオーシスと腸管毒素症を引き起こしうる。",
        "treatment": "Emergency stabilization with IV fluids and shock management, gastric decompression (trocarization or orogastric tube), followed by surgical correction if torsion is present. Post-operative monitoring for reperfusion injury and cardiac arrhythmias.",
        "treatment_ja": "デグーにおける鼓脹症の緊急治療: 重度の腹部膨満には25G針による経皮的ガス減圧。シメチコン経口投与（消泡剤）。皮下補液（温めた乳酸リンゲル液、体重の3-4%量）で循環維持。鎮痛としてメロキシカム1-2mg/kg SC SID。保温（24-26℃）と静かな環境に安置。腹部レントゲンでガス分布・閉塞の評価。回復期は消化管運動促進薬（メトクロプラミド0.5mg/kg SC q8h）を検討。シリンジによる強制給餌（草食動物用流動食）。再発防止のため高繊維食（チモシー主体）への食事改善、発酵性の高い食物（糖分の多い野菜・果物）の制限。再発をモニタリング。",
        "prevention": "Prevention includes providing a high-fiber diet, ensuring adequate hydration, regular exercise, stress reduction, and maintaining proper environmental conditions.",
        "prevention_ja": "鼓脹症の予防: 適切な食事管理（急激な食事変更を避ける）。繊維質の適切な摂取。異物誤食の予防。定期的な糞便検査。",
        "prognosis": "Prognosis depends on severity, underlying cause, and timeliness of treatment. Early aggressive intervention generally improves outcomes. Delayed presentation carries a guarded to poor prognosis.",
        "prognosis_ja": "鼓脹症の予後: 急性消化器疾患は多くが治療に良好に反応。閉塞性疾患は早期外科介入で予後良好。慢性疾患は食事管理で長期管理可能。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Diarrhea (Non-specific)",
        "name_ja": "下痢（非特異的）",
        "symptoms": {"diarrhea", "dehydration", "lethargy", "appetite_loss"},
        "description": "Diarrhea (Non-specific) is a gastrointestinal condition affecting digestive function and nutrient absorption.",
        "description_ja": "食事の変更、ストレス、感染による軟便。",
        "urgency": "moderate",
        "recommended_tests": ["fecal_exam", "fecal_culture", "physical_exam"],
        "causes": "Multifactorial etiology including infectious, environmental, immune, and host-related factors. Specific risk factors and triggers vary by individual case.",
        "causes_ja": "Exotic Otherにおける非特異的下痢（Exotic Other）の原因: その他エキゾチックにおける代謝性の消化器系疾患。非特異的下痢は適切な診断と治療管理が重要である。早期発見と適切な介入が予後改善の鍵となる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "非特異的下痢（Exotic Other）はExotic Otherにおける消化器疾患である。粘膜の完全性、運動性、分泌機能、またはマイクロバイオームバランスの障害を伴う。炎症により上皮バリアが損傷し、吸収不良、体液喪失、細菌トランスロケーションの可能性がある。運動障害（低運動性/うっ滞または亢進）により通過時間と消化効率が変化する。後腸発酵動物では盲腸/結腸フローラの破壊が致死的ディスバイオーシスと腸管毒素症を引き起こしうる。",
        "treatment": "FLUID RESUSCITATION (PRIORITY): Subcutaneous fluids — warmed lactated Ringer's solution "
        "50-100 mL/kg/day in divided doses (2-3 sites, maximum 10 mL per site). Reassess hydration "
        "q6-8h. Severe dehydration (>8%): IV access via lateral tail vein or jugular — 0.9% NaCl "
        "or LRS at maintenance + deficit replacement. DIETARY MANAGEMENT: Return to strict timothy "
        "hay-based diet — eliminate all sugar-containing foods (CRITICAL in degus due to diabetes "
        "predisposition — hyperglycemia worsens GI dysbiosis). Offer fresh water ad libitum. "
        "If anorexic: syringe-feeding with Critical Care for Herbivores (Oxbow) 50-80 mL/kg/day "
        "in divided doses q4-6h. PROBIOTICS: Saccharomyces boulardii or Lactobacillus spp. — "
        "help restore hindgut fermentation microbiome. ANTIBIOTICS (if bacterial etiology "
        "suspected): Enrofloxacin 5-10 mg/kg PO/SC q12h × 7-10 days (first-line). "
        "Trimethoprim-sulfa 15-30 mg/kg PO q12h (alternative). CONTRAINDICATED: Oral β-lactam "
        "antibiotics (penicillins, cephalosporins, amoxicillin) — cause fatal Clostridial "
        "dysbiosis and enterotoxemia in degus and other hindgut fermenters. PAIN MANAGEMENT: "
        "Meloxicam 1-2 mg/kg PO/SC q24h for abdominal discomfort. Simethicone 1-2 mL/kg PO "
        "q8h for gas accumulation. DIAGNOSTIC WORKUP: Fecal flotation and direct smear for "
        "parasites (Giardia, coccidia, helminths). Fecal culture if persistent or bloody. "
        "Dietary change must be gradual (>7 days transition). Daily body weight monitoring "
        "(>2% daily loss warrants aggressive intervention). References: Quesenberry & "
        "Carpenter (2012); Jekl & Redrobe (2013) BSAVA Manual.",
        "treatment_ja": "【脱水補正（最優先）】皮下補液 — 加温乳酸リンゲル液50-100 mL/kg/日を分割投与"
        "（2-3箇所、1箇所最大10mL）。水和状態をq6-8hで再評価。重度脱水（>8%）: 外側尾静脈"
        "または頸静脈からIVアクセス。【食事管理】チモシー牧草ベースの厳格食に戻す — 糖分を"
        "含む食品は全て排除（デグーの糖尿病素因により極めて重要 — 高血糖が腸内細菌叢異常を"
        "悪化）。食欲がない場合: 草食動物用クリティカルケア（Oxbow）50-80 mL/kg/日をシリンジ"
        "給餌。【プロバイオティクス】後腸発酵マイクロバイオームの回復を補助。【抗菌薬（細菌性"
        "が疑われる場合）】エンロフロキサシン5-10 mg/kg PO/SC q12h × 7-10日（第一選択）。"
        "TMS 15-30 mg/kg PO q12h（代替）。禁忌: 経口βラクタム系抗菌薬（ペニシリン、"
        "セファロスポリン、アモキシシリン） — デグーで致死的なクロストリジウム性腸管毒素症を"
        "引き起こす。【疼痛管理】メロキシカム1-2 mg/kg PO/SC q24h。シメチコン1-2 mL/kg "
        "PO q8h（ガス貯留時）。【検査】糞便浮遊法・直接塗抹で寄生虫検索。食事変更は段階的に"
        "（>7日間の移行期間）。毎日の体重モニタリング。",
        "prevention": "Maintain stable timothy hay-based diet — avoid sudden dietary changes (transition over "
        "≥7 days). Ensure adequate fiber intake (timothy hay ad libitum). Strictly avoid sugar "
        "and fruit (diabetes predisposition disrupts GI microbiome). Fresh water always available. "
        "Regular fecal examination (every 6-12 months). Quarantine new degus for 2-4 weeks before "
        "introduction. Stress reduction through appropriate group housing and environmental "
        "enrichment. Clean cage regularly (every 3-5 days). "
        "Reference: Quesenberry & Carpenter (2012) Ferrets, Rabbits, and Rodents 3rd ed.",
        "prevention_ja": "チモシー牧草ベースの安定した食事維持 — 急激な食事変更を避ける（≥7日間の移行期間）。"
        "適切な繊維質摂取（チモシー牧草の自由摂取）。糖分と果物の厳格な回避。新鮮な水を常時"
        "提供。定期的な糞便検査（6-12ヶ月ごと）。新規個体は2-4週間の隔離。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "下痢（非特異的）の予後: 急性消化器疾患は多くが治療に良好に反応。閉塞性疾患は早期外科介入で予後良好。慢性疾患は食事管理で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Constipation",
        "name_ja": "便秘",
        "symptoms": {"reduced_fecal_output", "straining", "bloating", "appetite_loss"},
        "description": "Constipation is a gastrointestinal condition affecting digestive function and nutrient absorption.",
        "description_ja": "脱水、低繊維食、閉塞による排便困難。",
        "urgency": "moderate",
        "recommended_tests": ["abdominal_radiographs", "physical_exam"],
        "causes": "Caused by dehydration, low-fiber diet, intestinal obstruction, or reduced gastrointestinal motility from pain, stress, or concurrent illness.",
        "causes_ja": "デグーにおける便秘の原因: 食事性失調、感染性病原体、寄生虫、ストレス、異物摂取、毒素、腸内細菌叢の破綻による消化器疾患。急な食事変更と不適切な食物が一般的な誘因。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "便秘はデグーにおける消化器疾患である。粘膜の完全性、運動性、分泌機能、またはマイクロバイオームバランスの障害を伴う。炎症により上皮バリアが損傷し、吸収不良、体液喪失、細菌トランスロケーションの可能性がある。運動障害（低運動性/うっ滞または亢進）により通過時間と消化効率が変化する。後腸発酵動物では盲腸/結腸フローラの破壊が致死的ディスバイオーシスと腸管毒素症を引き起こしうる。",
        "treatment": "Dietary modification (increased fiber/water), prokinetics if indicated, pain management, hydration support, and treatment of underlying cause.",
        "treatment_ja": "デグーにおける便秘の治療: 水分補給が第一: 皮下補液（乳酸リンゲル液）50-100ml/kg/日。食事改善: チモシー干し草の自由摂取を確保（繊維質増加）。消化管運動促進: メトクロプラミド0.5mg/kg PO/SC q8-12h（閉塞を除外後）。腹部疼痛管理: メロキシカム1-2mg/kg PO/SC q24h。腹部X線で閉塞・ガス貯留を評価。シメチコン1-2ml/kg PO q8h（ガス貯留がある場合）。運動促進: ケージ外での運動時間を増やす。経口流動食補助。注: 経口βラクタム系抗菌薬は禁忌。",
        "prevention": "Prevention includes providing a high-fiber diet, ensuring adequate hydration, regular exercise, stress reduction, and maintaining proper environmental conditions.",
        "prevention_ja": "便秘の予防: 適切な食事管理（急激な食事変更を避ける）。繊維質の適切な摂取。異物誤食の予防。定期的な糞便検査。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "便秘の予後: 急性消化器疾患は多くが治療に良好に反応。閉塞性疾患は早期外科介入で予後良好。慢性疾患は食事管理で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Intestinal Parasites",
        "name_ja": "腸内寄生虫症",
        "symptoms": {"diarrhea", "weight_loss", "bloating", "rough_coat"},
        "description": "Intestinal Parasites is a parasitic condition that causes clinical signs ranging from subclinical to severe systemic disease.",
        "description_ja": "原虫や蠕虫の寄生により下痢や状態悪化を引き起こす。",
        "urgency": "moderate",
        "recommended_tests": ["fecal_flotation", "fecal_smear"],
        "causes": "Caused by protozoal (coccidia, Giardia) or helminth (pinworm, tapeworm) infestation acquired through ingestion of contaminated food, water, or fecal-oral transmission.",
        "causes_ja": "デグーにおける腸内寄生虫症の原因: 原虫や蠕虫の寄生により下痢や状態悪化を引き起こす。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "腸内寄生虫症はデグーにおける寄生虫疾患である。寄生虫は経口摂取、経皮的侵入、またはベクター媒介伝播を通じて感染を確立する。抗原変異、免疫調節、細胞内隔離により宿主の免疫防御を回避しながら、宿主の栄養と資源を利用して増殖する。組織損傷は寄生虫の直接的な摂食、機械的破壊、有毒代謝副産物、宿主の炎症・免疫応答に起因する。重度の寄生虫感染は貧血、栄養失調、臓器機能障害、二次感染を引き起こしうる。",
        "treatment": "Treatment includes appropriate antiparasitic medication, environmental decontamination, and supportive care. Repeat treatments may be necessary to address lifecycle stages.",
        "treatment_ja": "デグーにおける腸内寄生虫症の治療には、同定された寄生虫に応じた適切な駆虫薬が必要である。一部の駆虫薬は特定の種に有毒であるため、種に適した用量設定が重要である。全てのライフステージを排除するため複数回投与が必要な場合がある。環境消毒と接触動物の治療で再感染を防止する。貧血、脱水、栄養失調などの二次的合併症に対する支持療法を行う。",
        "prevention": "Prevention includes regular parasite screening and treatment, environmental sanitation, quarantine of new animals, and avoiding overcrowding.",
        "prevention_ja": "腸内寄生虫症の予防には定期的な予防駆虫、環境衛生と糞便除去、新規動物の隔離・検査、ベクター防除、中間宿主や汚染環境への曝露回避が含まれる。",
        "prognosis": "Good with appropriate antiparasitic treatment. Reinfection is possible without environmental management.",
        "prognosis_ja": "腸内寄生虫症の予後: 急性消化器疾患は多くが治療に良好に反応。閉塞性疾患は早期外科介入で予後良好。慢性疾患は食事管理で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Giardiasis",
        "name_ja": "ジアルジア症",
        "symptoms": {"diarrhea", "weight_loss", "bloating", "dehydration"},
        "description": "Giardiasis is a parasitic condition that causes clinical signs ranging from subclinical to severe systemic disease.",
        "description_ja": "ジアルジア原虫による腸管感染で慢性的な水様下痢を引き起こす。",
        "urgency": "moderate",
        "recommended_tests": ["fecal_flotation", "giardia_antigen_test"],
        "causes": "Caused by Giardia spp. protozoan infection acquired through ingestion of cysts from contaminated water, food, or fecal-oral transmission in unsanitary conditions.",
        "causes_ja": "消化器系組織に感染する寄生虫が原因。感染期（卵・オーシスト・幼虫）の経口摂取・直接接触・ベクター・経皮侵入で伝播。不衛生・屋外曝露・免疫抑制・ストレスが素因。デグーの食性が特定の寄生虫生活環への曝露を増加させうる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "寄生虫は経口摂取・皮膚穿通・ベクター媒介によりデグーの消化器系組織に感染を確立する。寄生体は直接的な機械的損傷・栄養競合・免疫病理学的反応を通じて宿主組織を損傷する。寄生体段階の周囲に好酸球性・肉芽腫性炎症が発生する。慢性感染は組織線維化と臓器機能障害に至る。",
        "treatment": "Treatment includes appropriate antiparasitic medication, environmental decontamination, and supportive care. Repeat treatments may be necessary to address lifecycle stages.",
        "treatment_ja": "デグー鞭毛原虫感染症（Giardia、Tritrichomonas、Spironucleus）: ① 第一選択: メトロニダゾール 15-25 mg/kg PO q12h × 5-7日（神経毒性注意）、フェンベンダゾール 20-50 mg/kg PO q24h × 5日（Giardiaに有効）。② 環境消毒: 次亜塩素酸1:32、給水器・床面毎日洗浄。③ ⚠人獣共通感染症（Giardia）—家族の手洗い徹底。④ プロバイオティクスで腸内細菌叢回復。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes regular parasite screening and treatment, environmental sanitation, quarantine of new animals, and avoiding overcrowding.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "適切な駆虫薬治療で予後は一般的に良好。重度感染や免疫不全デグーでは予後不良となりうる。環境消毒と再感染予防が長期的な予後改善に重要。定期的な糞便検査と予防的駆虫が推奨される。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Intestinal Obstruction",
        "name_ja": "腸閉塞",
        "symptoms": {"appetite_loss", "bloating", "pain", "lethargy", "reduced_fecal_output"},
        "description": "Intestinal Obstruction is a gastrointestinal condition affecting digestive function and nutrient absorption.",
        "description_ja": "異物や腫瘤による腸管の閉塞。",
        "urgency": "emergency",
        "recommended_tests": ["abdominal_radiographs", "ultrasound"],
        "causes": "Caused by foreign body ingestion (bedding material, fabric), intussusception, or neoplastic masses obstructing the intestinal lumen.",
        "causes_ja": "消化器系組織への物理的外傷が原因。転落・ケージ損傷・取扱い事故・同居個体や捕食者からの咬傷・環境危険物が一般的原因。デグーの解剖学的特性が特定の損傷タイプへの素因となりうる。二次合併症として感染・治癒遅延・慢性疼痛がある。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "デグーの消化器系組織への外傷性損傷は、挫傷・裂傷・骨折を含む直接的な機械的組織損傷を引き起こす。急性炎症反応により浮腫・出血・疼痛が生じる。二次合併症として細菌汚染・感染・治癒遅延がある。デグーでは損傷からのストレスが追加の全身合併症を引き起こしうる。",
        "treatment": "Emergency exploratory laparotomy under isoflurane. SC fluids pre/post-op. Meloxicam 0.2 mg/kg SC. Syringe feed post-op. Prognosis guarded.",
        "treatment_ja": "デグーにおける腸閉塞の治療: 輸液で脱水補正。消化管運動促進薬。制吐薬。疼痛管理。食事管理（繊維質の確保）。原因に応じた特異的治療。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "外傷の予後は損傷の重症度と合併症の有無に依存する。軽度外傷は適切な創傷管理で予後良好。重度外傷、多発骨折、脊髄損傷は予後慎重〜不良。早期治療と適切な疼痛管理が回復を促進する。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    # ── Hepatic ────────────────────────────────────────────────────────────
    {
        "name": "Hepatic Lipidosis (Fatty Liver Disease)",
        "name_ja": "肝リピドーシス（脂肪肝）",
        "symptoms": {"appetite_loss", "lethargy", "weight_loss", "jaundice", "abdominal_distension"},
        "description": "Hepatic Lipidosis (Fatty Liver Disease) is a hepatic condition affecting liver function and metabolism.",
        "description_ja": "肝臓への過度な脂肪蓄積。肥満や食欲不振と関連することが多い。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "liver_enzymes", "ultrasound"],
        "causes": "Multifactorial etiology including infectious, environmental, immune, and host-related factors. Specific risk factors and triggers vary by individual case.",
        "causes_ja": "デグーにおける肝リピドーシス（脂肪肝）の原因: 高脂肪・高糖質の不適切な食事、肥満、食欲不振による急激な脂肪動員が主因。デグーは糖代謝能が低く糖尿病を発症しやすいため、インスリン抵抗性や高血糖に伴う脂質代謝異常が肝臓への脂肪蓄積を促進する。運動不足やストレスもリスク因子となる。",
        "pathophysiology": "Hepatocellular damage impairs metabolic, synthetic, and detoxification functions. Progressive injury leads to inflammation, fibrosis, and potential hepatic failure with systemic consequences.",
        "pathophysiology_ja": "肝リピドーシス（脂肪肝）はデグーにおける代謝・肝臓疾患である。食欲不振や高脂肪食により末梢脂肪組織から遊離脂肪酸が大量に肝臓へ動員され、肝細胞内にトリグリセリドが過剰蓄積する。デグーは糖代謝能が低いため、インスリン抵抗性に伴う脂質代謝異常が肝脂肪蓄積を加速させる。進行すると肝細胞機能障害、胆汁うっ滞、肝不全に至る。",
        "treatment": "Nutritional support (assisted feeding for hepatic lipidosis), hepatoprotectants (SAMe, ursodiol), IV fluid therapy, anti-emetics, and treatment of underlying cause.",
        "treatment_ja": "デグー肝リピドーシス（脂肪肝）: 原因（感染性・中毒・免疫介在性・腫瘍・代謝）特定が治療方針を決定。① 検査: CBC・生化学（ALT/AST/ALP/GGT/T-Bil/Alb）、胆汁酸負荷試験、凝固系（PT/aPTT）、超音波、肝生検（細胞診/組織学/培養）。② 原因別治療: 細菌→培養に基づく抗菌薬4-6週、寄生虫→駆虫、ウイルス→支持療法、免疫介在性→プレドニゾロン 1-2 mg/kg PO q12h漸減、薬剤性→暴露除去。③ 肝庇護: ウルソデオキシコール酸 10-15 mg/kg PO q24h、SAMe 20 mg/kg PO q24h（空腹時）、シリマリン 4-15 mg/kg PO q24h、ビタミンE 10-15 IU/kg PO q24h。④ 栄養: 高品質中等量蛋白、十分なカロリー（脂肪は耐容性で調整）、ビタミンK1補充。⑤ モニタ: 肝酵素 q2-4週、Alb・凝固系、必要なら肝生検でstaging。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "肝リピドーシス（脂肪肝）の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Variable. Hepatic lipidosis has a fair prognosis with early aggressive nutritional support. Chronic liver disease is guarded depending on underlying cause and degree of fibrosis.",
        "prognosis_ja": "肝リピドーシス（脂肪肝）の予後: 原因と重症度による。急性肝疾患は早期治療で回復可能。慢性肝疾患は長期管理で QOL 維持可能。肝不全は予後不良。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Liver Disease (Chronic)",
        "name_ja": "慢性肝疾患",
        "symptoms": {"jaundice", "weight_loss", "lethargy", "abdominal_distension", "appetite_loss"},
        "description": "Liver Disease (Chronic) is a hepatic condition affecting liver function and metabolism.",
        "description_ja": "毒素、感染、代謝性疾患による進行性の肝機能障害。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "liver_enzymes", "ultrasound", "biopsy"],
        "treatment": "Nutritional support (assisted feeding for hepatic lipidosis), hepatoprotectants (SAMe, ursodiol), IV fluid therapy, anti-emetics, and treatment of underlying cause.",
        "treatment_ja": "【デグーにおける慢性肝疾患】\n慢性肝疾患はデグーにおける正確な臨床評価（病歴、身体検査、CBC・生化学、画像）から治療方針を決定。\n基礎疾患の特定→特異的治療＋支持療法の組み合わせが原則。\n経過モニタリング: 主訴の改善、検査値の変化、QOLを2-4週毎に再評価。\n複雑症例はデグー専門医（ACZMまたはAVMAエキゾチック分科会等）に紹介を検討。\n支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。\n【鑑別と経過観察】類似症候を呈する疾患の除外と、治療4-8週後の再評価が予後改善の鍵。重症度・併発症によってはデグーの専門医紹介を考慮する。",
        "prognosis": "Variable. Hepatic lipidosis has a fair prognosis with early aggressive nutritional support. Chronic liver disease is guarded depending on underlying cause and degree of fibrosis.",
        "prognosis_ja": "予後は原因と重症度により異なる。肝リピドーシスは早期の積極的栄養サポートで予後やや良好。慢性肝疾患は線維化の程度により予後要注意。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    # ── Renal ──────────────────────────────────────────────────────────────
    {
        "name": "Chronic Kidney Disease",
        "name_ja": "慢性腎臓病",
        "symptoms": {"polyuria", "polydipsia", "weight_loss", "lethargy", "dehydration"},
        "description": "Chronic Kidney Disease is a renal condition affecting kidney function and fluid-electrolyte balance.",
        "description_ja": "加齢に伴う進行性の腎機能低下。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "urinalysis", "ultrasound"],
        "causes": "Caused by progressive deterioration of urogenital tissue due to aging, chronic wear, or cumulative damage. Contributing factors include genetic predisposition, chronic inflammation, oxidative stress, and suboptimal husbandry conditions. In degu, captive management practices and dietary factors may accelerate degenerative changes.",
        "causes_ja": "加齢・慢性的摩耗・累積的損傷による泌尿器系組織の進行性劣化が原因。遺伝的素因・慢性炎症・酸化ストレス・不適切な飼育条件が寄与。デグーの飼育管理と食事因子が変性変化を加速しうる。",
        "pathophysiology": "Progressive degenerative changes in urogenital tissue of degu involve gradual loss of cellular structure and function. Mechanisms include oxidative stress, chronic inflammation, cellular senescence, and impaired tissue repair. Age-related changes, cumulative environmental insults, and genetic predisposition contribute to disease progression. In degu, degenerative conditions may be exacerbated by captive management practices and dietary factors.",
        "pathophysiology_ja": "デグーの泌尿器系組織における進行性変性変化は、細胞構造と機能の漸進的喪失を伴う。酸化ストレス・慢性炎症・細胞老化・組織修復障害が関与する。加齢変化・累積的環境侵襲・遺伝的素因が疾患進行に寄与する。飼育管理と食事要因が変性疾患を悪化させうる。",
        "treatment": "SC fluids (LRS) 50-100 mL/kg every 1-3 days. Phosphate binder if hyperphosphatemic. Syringe feed renal-appropriate diet. Monitor BUN/creatinine. Prognosis guarded; common in older degus.",
        "treatment_ja": "デグー慢性腎臓病の治療: ① 評価—BUN・クレアチニン・SDMA・尿比重・尿蛋白、超音波（腎構造）。② 食事療法: 低タンパク・低リン処方食（種別、入手可能性で）、新鮮野菜中心（草食種）。③ Pバインダー: aluminum hydroxide 30-100 mg/kg PO q12h（必要時）。④ 輸液: SC 80-100 mL/kg/日（脱水時）—在宅維持輸液有効。⑤ 高血圧（測定困難だが）: アムロジピン 0.1-0.2 mg/kg PO q24h。⑥ 蛋白尿: ベナゼプリル 0.1-0.25 mg/kg PO q24h（種別データ限定的）。⑦ 制吐: メトクロプラミド 0.5 mg/kg SC/PO q6-8h、マロピタント（試験的）。⑧ ⚠ NSAIDs回避、定期モニタ q1-3ヶ月。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes ensuring adequate hydration, balanced diet, regular health screening, and avoiding nephrotoxic substances.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis is guarded to poor long-term. Disease progression can be slowed with appropriate management, but CKD is ultimately irreversible.",
        "prognosis_ja": "変性疾患の予後は進行速度と管理可能性に依存する。緩徐進行性の場合、適切な対症療法とQOL管理で長期生存が可能。急速進行性の場合は予後不良。定期的な再評価と治療調整が重要。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Urolithiasis (Bladder Stones)",
        "name_ja": "尿路結石症",
        "symptoms": {"straining", "blood_in_urine", "frequent_urination", "pain"},
        "description": "Urolithiasis (Bladder Stones) is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "尿路内でのミネラル結石の形成。",
        "urgency": "high",
        "recommended_tests": ["urinalysis", "radiographs", "ultrasound"],
        "causes": "Multifactorial etiology including infectious, environmental, immune, and host-related factors. Specific risk factors and triggers vary by individual case.",
        "causes_ja": "デグーにおける尿路結石症の原因: カルシウム代謝異常、不適切な食事（高カルシウム食・低水分摂取）、遺伝的素因が主な原因。デグーは糖尿病を併発しやすく、多飲多尿による尿濃縮変化や代謝異常が結石形成リスクを高める。炭酸カルシウム結石が多い。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "尿路結石症はデグーにおける腎・泌尿器疾患である。尿中のカルシウム濃度上昇や尿pH変化により、膀胱や尿道内で炭酸カルシウム等のミネラル結晶が析出・凝集し結石を形成する。結石は尿路粘膜を機械的に損傷し、炎症・血尿・疼痛を引き起こす。尿道閉塞が生じると急性腎後性腎不全に至り、緊急処置が必要となる。",
        "treatment": "Cystotomy under isoflurane. SC fluids. Meloxicam 0.2 mg/kg SC. Submit stones for analysis. Dietary modification (reduce calcium). Increase water intake.",
        "treatment_ja": "デグーにおける尿路結石症の治療は、食事中のカルシウム含有量の適正化と十分な水分摂取の確保が基本。閉塞を伴う場合は外科的摘出が必要。鎮痛薬（メロキシカム等）による疼痛管理、二次感染に対する抗菌薬投与を行う。糖尿病の併存がある場合はその管理も並行して行い、定期的な尿検査・画像検査でモニタリングする。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "尿路結石症の予防: 飲水量の増加（ウェットフード、複数の水場）。適切な食事管理。定期的な尿検査。排尿パターンの日常観察。ストレス軽減。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "尿路結石症の予後: 早期治療で予後良好。再発予防には食事管理と定期検査が重要。閉塞性疾患は緊急対応で予後改善。慢性腎疾患はステージにより予後が異なる。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Urinary Tract Infection",
        "name_ja": "尿路感染症",
        "symptoms": {"frequent_urination", "blood_in_urine", "straining", "lethargy"},
        "description": "Urinary Tract Infection is a bacterial infection that causes systemic or localized inflammatory disease requiring prompt antimicrobial therapy.",
        "description_ja": "膀胱または尿道の細菌感染。",
        "urgency": "moderate",
        "recommended_tests": ["urinalysis", "urine_culture"],
        "causes": "Caused by ascending bacterial infection of the lower urinary tract, predisposed by poor hygiene, urolithiasis, anatomical abnormalities, or immunosuppression.",
        "causes_ja": "デグーにおける尿路感染症の原因: 感染性病原体、毒素、免疫学的過程、尿石症、先天性欠損、慢性脱水による腎病理。加齢、食事、種特異的感受性が寄与因子。",
        "pathophysiology": "Bacterial organisms invade host tissues, triggering inflammatory cascades with neutrophil recruitment, cytokine release, and potential tissue necrosis. Systemic spread may lead to bacteremia and multi-organ dysfunction.",
        "pathophysiology_ja": "尿路感染症はデグーにおける腎・泌尿器疾患である。腎臓、尿管、膀胱、または尿道の構造的・機能的障害を伴う。腎疾患は糸球体濾過、尿細管再吸収・分泌、およびホルモン機能（エリスロポエチン、カルシトリオール、レニン）を障害する。進行性のネフロン喪失により高窒素血症、電解質異常、酸塩基障害が生じる。下部尿路疾患は閉塞、尿石症、上行感染を引き起こしうる。",
        "treatment": "Antimicrobial therapy based on culture and sensitivity, wound care or drainage as needed, pain management, and monitoring for resolution.",
        "treatment_ja": "デグーにおける尿路感染症の治療: 第一選択抗菌薬: エンロフロキサシン5-10mg/kg PO q12h（14-21日間）。代替: トリメトプリム-スルファメトキサゾール30mg/kg PO q12h。尿培養感受性に基づき調整。疼痛管理: メロキシカム1-2mg/kg PO/SC q24h。水分摂取量の増加（新鮮な水の常時提供、ウェットフード追加）。尿石症の併発を除外するために腹部X線/超音波検査。治療後の尿検査でクリアランスを確認。ケージの清潔維持。注: 経口βラクタム系抗菌薬は禁忌。",
        "prevention": "Prevention includes maintaining proper hygiene, appropriate husbandry, stress reduction, quarantine of new animals, and prompt treatment of wounds or primary conditions.",
        "prevention_ja": "尿路感染症の予防: 飲水量の増加（ウェットフード、複数の水場）。適切な食事管理。定期的な尿検査。排尿パターンの日常観察。ストレス軽減。",
        "prognosis": "Good with appropriate antimicrobial therapy. Most infections resolve with proper treatment. Chronic or recurrent cases may require longer management.",
        "prognosis_ja": "尿路感染症の予後: 早期治療で予後良好。再発予防には食事管理と定期検査が重要。閉塞性疾患は緊急対応で予後改善。慢性腎疾患はステージにより予後が異なる。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    # ── Neoplasia ──────────────────────────────────────────────────────────
    {
        "name": "Mammary Tumor",
        "name_ja": "乳腺腫瘍",
        "symptoms": {"mammary_mass", "swelling", "weight_loss", "lethargy"},
        "description": "Mammary Tumor is a neoplastic condition characterized by abnormal cell proliferation that may be benign or malignant.",
        "description_ja": "乳腺組織の良性または悪性腫瘍。",
        "urgency": "high",
        "recommended_tests": ["fine_needle_aspirate", "radiographs", "histopathology"],
        "causes": "Caused by neoplastic transformation of mammary gland tissue, with hormonal influences (estrogen, progesterone), aging, and genetic predisposition as risk factors.",
        "causes_ja": "デグーにおける乳腺腫瘍の原因: 癌遺伝子・腫瘍抑制遺伝子の遺伝子変異蓄積による腫瘍性形質転換。加齢、慢性炎症、ウイルス感染、ホルモン影響、UV曝露、遺伝的素因がリスク因子。",
        "pathophysiology": "Accumulated genetic mutations lead to uncontrolled cell proliferation, evasion of apoptosis, and potential metastatic spread. Tumor growth causes tissue compression, invasion, and paraneoplastic effects.",
        "pathophysiology_ja": "乳腺腫瘍はデグーにおける腫瘍性疾患である。癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積により腫瘍性形質転換が生じる。制御不能な細胞増殖により腫瘍が形成され、局所組織への浸潤・破壊の可能性がある。悪性腫瘍はリンパ行性または血行性に転移しうる。高カルシウム血症、悪液質、免疫調節障害などの腫瘍随伴症候群が原発腫瘍に伴い、罹患率に寄与することがある。",
        "treatment": "Surgical excision under isoflurane if mass is accessible and patient stable. Meloxicam 1-2 mg/kg PO SID for pain. Avoid dexamethasone (diabetes risk). Palliative care preferred for large/inoperable tumors due to small body size and limited surgical options.",
        "treatment_ja": "腫瘤が外科的にアクセス可能で全身状態が安定していればイソフルラン麻酔下で切除。メロキシカム1-2 mg/kg PO SIDで疼痛管理。デキサメタゾンは糖尿病リスクのため禁忌。大型・切除不能腫瘍は体格の小ささから緩和ケアを優先。",
        "prevention": "Prevention is limited for most neoplastic conditions. Regular health examinations facilitate early detection. Spaying/neutering may reduce risk of hormone-dependent tumors.",
        "prevention_ja": "乳腺腫瘍の予防は限定的であるが、ホルモン依存性腫瘍軽減のための避妊・去勢手術、既知の発癌物質の回避、早期発見のための定期健診、適正体型の維持、該当する場合は遺伝的素因軽減のための責任ある繁殖が含まれる。",
        "prognosis": "Prognosis depends on tumor type, staging, and response to treatment. Complete surgical excision of localized tumors improves outcomes. Metastatic disease carries a guarded to poor prognosis.",
        "prognosis_ja": "乳腺腫瘍の予後: 腫瘍の種類、病期、転移の有無により予後は大きく異なる。早期発見・早期治療で予後改善。悪性腫瘍は一般的に予後要注意〜不良。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Skin Tumor",
        "name_ja": "皮膚腫瘍",
        "symptoms": {"skin_mass", "ulceration", "hair_loss", "swelling"},
        "description": "Skin Tumor is a neoplastic condition characterized by abnormal cell proliferation that may be benign or malignant.",
        "description_ja": "皮膚表面や皮下組織の腫瘍性増殖。",
        "urgency": "moderate",
        "recommended_tests": ["fine_needle_aspirate", "histopathology"],
        "causes": "Caused by neoplastic proliferation of cutaneous or subcutaneous cells, with aging, chronic inflammation, UV exposure, and genetic predisposition as contributing factors.",
        "causes_ja": "デグーにおける皮膚腫瘍の原因: 皮膚表面や皮下組織の腫瘍性増殖。",
        "pathophysiology": "Accumulated genetic mutations lead to uncontrolled cell proliferation, evasion of apoptosis, and potential metastatic spread. Tumor growth causes tissue compression, invasion, and paraneoplastic effects.",
        "pathophysiology_ja": "皮膚腫瘍はデグーにおける腫瘍性疾患である。癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積により腫瘍性形質転換が生じる。制御不能な細胞増殖により腫瘍が形成され、局所組織への浸潤・破壊の可能性がある。悪性腫瘍はリンパ行性または血行性に転移しうる。高カルシウム血症、悪液質、免疫調節障害などの腫瘍随伴症候群が原発腫瘍に伴い、罹患率に寄与することがある。",
        "treatment": "Surgical excision with margins under isoflurane for accessible masses. FNA/biopsy for histological grading. Meloxicam 1-2 mg/kg PO SID post-op. Avoid dexamethasone (diabetes-prone species). Palliative care for inoperable lesions; monitor for ulceration and secondary infection.",
        "treatment_ja": "アクセス可能な腫瘤はイソフルラン麻酔下でマージン付き切除。FNA/生検で組織学的グレーディング。術後メロキシカム1-2 mg/kg PO SID。デキサメタゾンは糖尿病リスクで禁忌。切除不能例は緩和ケア、潰瘍化・二次感染をモニタリング。",
        "prevention": "Prevention is limited for most neoplastic conditions. Regular health examinations facilitate early detection. Spaying/neutering may reduce risk of hormone-dependent tumors.",
        "prevention_ja": "皮膚腫瘍の予防は限定的であるが、ホルモン依存性腫瘍軽減のための避妊・去勢手術、既知の発癌物質の回避、早期発見のための定期健診、適正体型の維持、該当する場合は遺伝的素因軽減のための責任ある繁殖が含まれる。",
        "prognosis": "Prognosis depends on tumor type and staging. Benign tumors with complete excision have good prognosis. Malignant tumors require further assessment.",
        "prognosis_ja": "皮膚腫瘍の予後: 腫瘍の種類、病期、転移の有無により予後は大きく異なる。早期発見・早期治療で予後改善。悪性腫瘍は一般的に予後要注意〜不良。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Abdominal Tumor",
        "name_ja": "腹腔内腫瘍",
        "symptoms": {"abdominal_distension", "weight_loss", "appetite_loss", "lethargy"},
        "description": "Abdominal Tumor is a neoplastic condition characterized by abnormal cell proliferation that may be benign or malignant.",
        "description_ja": "腹腔内の腫瘍により腹部膨満と全身状態の悪化が生じる。",
        "urgency": "high",
        "recommended_tests": ["ultrasound", "radiographs", "blood_work", "biopsy"],
        "causes": "Caused by neoplastic growth within the abdominal cavity arising from various organ tissues, with aging and genetic predisposition as primary risk factors.",
        "causes_ja": "デグーにおける腹腔内腫瘍の原因: 腹腔内の腫瘍により腹部膨満と全身状態の悪化が生じる。",
        "pathophysiology": "Accumulated genetic mutations lead to uncontrolled cell proliferation, evasion of apoptosis, and potential metastatic spread. Tumor growth causes tissue compression, invasion, and paraneoplastic effects.",
        "pathophysiology_ja": "腹腔内腫瘍はデグーにおける腫瘍性疾患である。癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積により腫瘍性形質転換が生じる。制御不能な細胞増殖により腫瘍が形成され、局所組織への浸潤・破壊の可能性がある。悪性腫瘍はリンパ行性または血行性に転移しうる。高カルシウム血症、悪液質、免疫調節障害などの腫瘍随伴症候群が原発腫瘍に伴い、罹患率に寄与することがある。",
        "treatment": "Exploratory laparotomy under isoflurane if patient stable and mass appears resectable on imaging. Meloxicam 1-2 mg/kg PO SID for pain. Avoid dexamethasone (diabetes risk). Palliative management often preferred due to small body size; supportive care with syringe feeding.",
        "treatment_ja": "全身状態が安定し画像で切除可能と判断されればイソフルラン麻酔下で試験開腹。メロキシカム1-2 mg/kg PO SIDで疼痛管理。デキサメタゾンは糖尿病リスクで禁忌。体格の小ささから緩和的管理が多い。シリンジ給餌で栄養サポート。",
        "prevention": "Prevention is limited for most neoplastic conditions. Regular health examinations facilitate early detection. Spaying/neutering may reduce risk of hormone-dependent tumors.",
        "prevention_ja": "腹腔内腫瘍の予防は限定的であるが、ホルモン依存性腫瘍軽減のための避妊・去勢手術、既知の発癌物質の回避、早期発見のための定期健診、適正体型の維持、該当する場合は遺伝的素因軽減のための責任ある繁殖が含まれる。",
        "prognosis": "Prognosis depends on tumor type, staging, and response to treatment. Complete surgical excision of localized tumors improves outcomes. Metastatic disease carries a guarded to poor prognosis.",
        "prognosis_ja": "腹腔内腫瘍の予後: 腫瘍の種類、病期、転移の有無により予後は大きく異なる。早期発見・早期治療で予後改善。悪性腫瘍は一般的に予後要注意〜不良。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    # ── Reproductive ───────────────────────────────────────────────────────
    {
        "name": "Pyometra",
        "name_ja": "子宮蓄膿症",
        "symptoms": {"vaginal_discharge", "lethargy", "appetite_loss", "abdominal_distension", "polydipsia"},
        "description": "Pyometra is a reproductive condition affecting fertility, gestation, or parturition.",
        "description_ja": "子宮内に膿が蓄積する感染症。未避妊の雌で致命的になりうる。",
        "urgency": "emergency",
        "recommended_tests": ["ultrasound", "blood_work", "radiographs"],
        "causes": "Caused by bacterial infection of the progesterone-primed uterus in intact female degus, typically by opportunistic organisms such as E. coli ascending from the vaginal flora.",
        "causes_ja": "デグーにおける子宮蓄膿症の原因: 創傷汚染、経口摂取、吸入、日和見的過剰増殖による細菌コロニー形成。ストレス、免疫抑制、不衛生、過密飼育、併発疾患が素因となる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "子宮蓄膿症はデグーにおける細菌感染症である。病原菌は付着因子を通じて組織にコロニーを形成し、毒素産生、酵素分泌、免疫回避戦略などの病原性メカニズムを介して侵入する。好中球浸潤、サイトカイン放出、補体活性化を含む炎症カスケードが生じる。組織損傷は細菌の直接作用と宿主の炎症反応の両方に起因する。菌種と宿主の免疫状態に応じて、膿瘍形成、敗血症、または慢性肉芽腫性炎症が発生しうる。",
        "treatment": "DIAGNOSIS & CLASSIFICATION (CRITICAL—determines treatment pathway): distinguish OPEN-TYPE pyometra (uterine drainage via cervix; vaginal discharge visible) vs CLOSED-TYPE (uterine rupture occurring or imminent; no drainage). Ultrasound essential: fluid-filled uterus (>5 mm diameter = pyometra), uterine wall thickness, free abdominal fluid (peritonitis indicator). Closed-type pyometra = MEDICAL MANAGEMENT FUTILE—proceed directly to emergency OVE. MEDICAL MANAGEMENT (OPEN-TYPE ONLY, if stable, <48 hours pre-diagnosis): Prostaglandin F2α analogues (cloprostenol 1-2 μg/kg SC q12h × 5-7 days) to promote uterine contractions and drainage. Response rate 30-50% in degus (lower than larger animals due to small uterine size). HOWEVER, NOT RECOMMENDED in degus due to severe adverse effects (gasping, hyperthermia, seizures at therapeutic doses reported). IV crystalloid fluids (LRS 50-100 mL/kg bolus), analgesia (meloxicam 0.3-0.5 mg/kg SC q24h × 5-7 days), broad-spectrum antibiotics (NEVER β-LACTAMS—fatal dysbiosis): Enrofloxacin 10-15 mg/kg SC/PO q12h × 14-21 days (first-line), OR trimethoprim-sulfamethoxazole 30 mg/kg PO q12h × 14-21 days. Add metronidazole 20 mg/kg PO q12h × 10-14 days (anaerobic coverage). Vitamin C 50-100 mg/kg/day SC/PO (immune support). Culture sensitivity testing MANDATORY—adjust antibiotics based on results. CRITICAL MONITORING: daily temperature (fever should resolve 3-5 days; persistent fever = treatment failure), vaginal discharge (should clear significantly; purulent/hemorrhagic = failure sign), blood work daily × 3 (WBC normalization), urine output (catheterization if critical). Fever persisting >5 days OR worsening discharge = EMERGENCY OVE. SURGICAL MANAGEMENT (DEFINITIVE): Ovariohysterectomy (OHE) is treatment of choice for closed-type, failed medical management, or if rupture suspected. PRE-OPERATIVE ASSESSMENT: blood chemistry (hepatic/renal function), CBC (baseline WBC/platelets), radiographs (assess peritoneal free fluid). ANESTHESIA: isoflurane chamber induction preferred (reduces handling stress in small animals); if injectable needed, dexmedetomidine 2-3 μg/kg IM + buprenorphine 0.03-0.05 mg/kg IM. Temperature maintenance critical: 28-32°C (degus metabolically active but small). SURGICAL TECHNIQUE: ventral midline laparotomy (1.5-2.0 cm incision), carefully assess uterus for rupture/peritonitis (purulent exudate = severe infection, high mortality), ligate ovarian and uterine vessels with 5-0 absorbable suture, excise entire ovary and uterus (critical—remnant hysterectomy not acceptable; recurrence risk high in degus), close fascia (5-0 absorbable), skin with tissue adhesive or 6-0 absorbable suture. Surgery time <15 minutes critical. Send uterus for culture if ruptured/aspirate. POST-OPERATIVE CARE (CRITICAL): 1) Timothy hay ad libitum immediately (GI stasis prevention). 2) NO FASTING post-op (degus have continuous GI motility). 3) Metoclopramide 0.5-1.0 mg/kg PO q8h × 5-7 days (GI stasis prevention). 4) Meloxicam 0.3-0.5 mg/kg SC q24h × 5-7 days (NSAID, not buprenorphine alone—opioids risk GI stasis). 5) Probiotics (FortiFlora 250 mg/kg/day × 14 days). 6) IV/SC fluids: LRS 15-25 mL/kg/day × 48-72h. 7) Monitor appetite hourly first 24h (anorexia = GI stasis emergency). 8) Strict isolation from other animals 5-7 days post-op. 9) Blood glucose monitoring q2h × 24h (post-operative stress hyperglycemia common). 10) Antibiotic continuation × 10-14 days post-op. PERITONITIS MANAGEMENT (if rupture occurred): aggressive fluid resuscitation, multiple antibiotic coverage, supportive care intensive. Prognosis poor if rupture present; mortality 60-80% even with surgery.",
        "treatment_ja": "診断・分類（重大）：開放型（子宮排液子宮頸部経由；膣分泌物可見）vs 閉鎖型（子宮破裂発生または切迫；排液なし）。超音波重大：液体満杯子宮（>5 mm直径=子宮蓄膿症）、子宮壁厚、腹腔遊離液（腹膜炎指標）。閉鎖型=医学的管理無益—緊急OVEに進行。医学的管理（開放型のみ、安定時、<48時間診断前）：プロスタグランジンF2α類似体（クロプロステノール 1-2 μg/kg SC q12h × 5-7日）で子宮収縮と排液促進。応答率30-50%（より小体積）。非推奨デグーで：重篤有害効果（喘鳴、体温上昇、けいれん治療用量で報告）。IV結晶質（乳酸リンガー50-100 mL/kg bolus）、鎮痛（メロキシカム0.3-0.5 mg/kg SC q24h × 5-7日）、広域抗菌薬（βラクタム禁止—致死的dysbiosis）：エンロフロキサシン10-15 mg/kg SC/PO q12h × 14-21日（第一選択）または TMS 30 mg/kg PO q12h × 14-21日。メトロニダゾール20 mg/kg PO q12h × 10-14日追加。ビタミンC 50-100 mg/kg/日 SC/PO。培養感受性試験必須。重大監視：毎日体温（解決予期3-5日；遷延発熱=失敗）、膣分泌物（著しく明確；化膿性/出血性=失敗兆候）、血液検査毎日 × 3（好中球正常化）。遷延発熱>5日またはオプト悪化=緊急OVE。外科管理（根治）：OVEが治療第一選択閉鎖型、失敗医学、または破裂疑い時。術前評価：血液化学、CBC、X線。麻酔：イソフルラン吸入導入推奨；注射必要時、デクスメデトミジン2-3 μg/kg IM + ブプレノルフィン0.03-0.05 mg/kg IM。温度28-32°C。外科技術：腹部正中線開腹（1.5-2.0 cm切開）、子宮慎重評価（破裂/腹膜炎で化膿性浸出液=重症感染高死亡率）、卵巣と子宮血管結紮、全卵巣と子宮切除。筋膜5-0吸収性、皮膚接着剤または6-0吸収性。手術時間<15分。子宮培養送付。術後管理（重大）：1) チモシーヘイ即座。2) 絶食なし。3) メトクロプラミド0.5-1.0 mg/kg PO q8h × 5-7日。4) メロキシカム0.3-0.5 mg/kg SC q24h × 5-7日。5) プロバイオティクス × 14日。6) IV/SC輸液 × 48-72h。7) 食欲監視時間。8) 厳密隔離5-7日。9) 血糖監視q2h × 24h。10) 抗菌薬継続 × 術後10-14日。腹膜炎管理（破裂発生時）：攻撃的輸液、複数抗菌薬、集約的支持。予後不良破裂存在；死亡率60-80%手術後でも。",
        "prevention": 'CRITICAL PREVENTION (100% effective): 1) SPAY all females not intended for breeding by age 12 months maximum (eliminates pyometra risk entirely; 80-90% of intact females develop pyometra by age 3-4 years in captive colonies). Early spaying (6-12 months) is optimal. 2) STRICT HYGIENE: daily bedding changes (use aspen or paper-based substrate, NEVER cedar/pine—toxic to degus), spot-clean soiled areas, disinfect cage biweekly (bleach solution 1:10, allow air-dry), quarantine infected animals immediately. 3) MAINTAIN OPTIMAL BODY WEIGHT: 300-350g is target; obesity >400g increases dystocia/endometritis/pyometra risk dramatically. Monthly weight monitoring critical. 4) STRESS REDUCTION: minimize handling during estrous cycles (swollen vulva = high hormonal stimulation), maintain cool temperature (15-22°C—heat stress worsens immunosuppression), avoid overcrowding (>1 degu per 40L cage minimum). 5) MONITOR INTACT FEMALES: monthly abdominal palpation (detect early uterine enlargement), quarterly ultrasound if >18 months old (detect pre-symptomatic pyometra). 6) PROMPT ENDOMETRITIS TREATMENT: treat bacterial infection/endometritis aggressively within 24-48 hours (prevents progression to pyometra; see Endometritis entry). 7) BREEDING MANAGEMENT: if breeding, restrict to 2-3 litters maximum, retire females by age 3 years, ensure adequate nutrition (calcium 1,000-1,500 mg/kg diet, vitamin C 50-100 mg/kg/day), space litters minimum 3-4 weeks apart. 8) AVOID PROLONGED ESTROUS CYCLING: degus cycling 24-48 hour intervals without breeding continuously stimulate endometrium with estrogen—breeding females should breed or be spayed (no perpetual "virgin" cycling). 9) ANTIBIOTIC STEWARDSHIP: avoid prolonged antibiotic courses that disrupt microbiota (increase secondary pyometra risk); use appropriate narrow-spectrum agents when possible. 10) NEONATAL CARE POST-DYSTOCIA: dystocia carries high risk of secondary endometritis/pyometra—monitor immediately post-partum females closely (fever, discharge, lethargy = emergency OVE).',
        "prevention_ja": "重大予防（100%有効）：1) 育種意図なし全雌を12ヶ月最大で避妘（子宮蓄膿症リスク完全消失；飼育下で完全雌の80-90%が3-4年齢までに子宮蓄膿症発症）。早期避妘（6-12ヶ月）最適。2) 厳密衛生：毎日床材変更（アスペンまたは紙ベース、スギ松禁止—デグーに毒性）、汚れた領域spot-clean、ケージ消毒隔週（ブリーチ液1:10、空気乾燥）、感染動物隔離即座。3) 最適体重維持：300-350g目標；肥満>400g が難産/子宮内膜炎/子宮蓄膿症リスク激増。月1回体重監視。4) ストレス低減：発情周期中取扱い最小化、温度15-22°C維持、過密回避。5) 完全雌監視：月1回腹部触診、>18ヶ月齢なら四半期超音波。6) 迅速子宮内膜炎治療：バクテリア感染/子宮内膜炎を24-48時間以内に積極治療（子宮蓄膿症進行予防）。7) 育種管理：育種なら2-3産仔上限、3年齢でリタイア、適切栄養。8) 延長発情周期回避：デグーが連続24-48時間サイクル育種無しで子宮エストロゲン刺激連続—育種雌は繁殖または避妘（永遠の処女性サイクル無し）。9) 抗菌薬管理：延長コース回避microbiota破壊で二次子宮蓄膿症リスク増加。10) 新仔管理難産後：難産は二次子宮内膜炎/子宮蓄膿症高リスク—即座産後雌監視（発熱、分泌物、無気力=緊急OVE）。",
        "prognosis": "PROGNOSIS DEPENDS CRITICALLY ON PYOMETRA TYPE & TIMING: OPEN-TYPE PYOMETRA (drainage via cervix): IF diagnosed <48 hours: medical management success 40-60% (fluid drainage usually effective). IF open-type with systemic signs (fever, lethargy): OVE recommended (safer/faster than medical attempt in debilitated animal); surgical mortality <3% in healthy animals. Medical management failure (fever persisting >5 days, worsening discharge, anorexia): proceed to OVE; mortality then 10-20% (septic shock has begun). CLOSED-TYPE PYOMETRA (rupture occurring/imminent): MEDICAL MANAGEMENT FUTILE—OVE mandatory emergency procedure. Surgical mortality <5% if ruptured <6 hours (minimal peritonitis). Mortality 10-20% if ruptured 6-24 hours (peritonitis established but not yet overwhelming). Mortality 50-80% if ruptured >24 hours (septic shock, endotoxemia severe). POST-OPERATIVE OUTCOMES: open-type treated with OVE: 95%+ survival if sepsis not advanced. Closed-type treated with OVE within 24 hours: 80-85% survival. Closed-type treated after 48 hours: 30-40% survival (peritonitis/septic shock irreversible). WITHOUT TREATMENT: mortality 100% within 3-7 days in closed-type pyometra. Degus deteriorate rapidly due to small body mass (300-350g); endotoxin load quickly becomes lethal. Delayed diagnosis common because degu pyometra can be SILENT—no vaginal discharge visible in closed-type; owners may not notice lethargy until very late (collapse/shock). POST-RECOVERY OUTCOMES: if survive OVE, fertility permanently lost (endometrial scarring prevents implantation). Long-term survival normal (8+ years expected) if no other complications. Recurrence without OVE: 100% (all survivors develop pyometra within 3-6 months if both ovaries retained). Post-operative GI stasis: complication in 5-10% even with prevention protocols; most respond to medical management.",
        "prognosis_ja": "子宮蓄膿症の予後：型とタイミング重大依存。開放型（子宮頸部経由排液）：診断<48時間で医学的管理成功40-60%。全身兆候（発熱、無気力）で開放型：OVE推奨；手術死亡率<3% 健全動物。医学的失敗（遷延発熱>5日、悪化分泌物、食欲不振）：OVEに進行；死亡率10-20%（敗血症ショック開始）。閉鎖型（破裂発生/切迫）：医学的管理無益—OVE必須緊急。手術死亡率<5%破裂<6時間（腹膜炎最小）。死亡率10-20% >6-24時間（腹膜炎確立）。死亡率50-80% >24時間（敗血症ショック重症）。術後：開放型OVE治療：>95%生存敗血症進行なし。閉鎖型OVE<24時間：80-85%生存。>48時間後：30-40%生存。無治療：死亡率100% 3-7日以内。デグー急速悪化小体格；エンドトキシン負荷迅速に致死。遅延診断一般的閉鎖型で無言—膣分泌物可見なし；飼主は無気力注意不足（collapse/shock非常に遅い）。回復後：受胎率永遠に喪失（endometrial scarring）。長期生存正常（8+年予期）。OVE無し再発：100% 3-6ヶ月以内。術後GI停滞合併症5-10%。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Dystocia",
        "name_ja": "難産",
        "symptoms": {"straining", "lethargy", "vaginal_discharge", "pain", "restlessness"},
        "description": "Dystocia in degus is an obstetric emergency often complicated by maternal obesity and fetal size. Degus have short gestation (~93 days) producing precocial, relatively large young; dystocia carries high maternal mortality (20-30% even with treatment).",
        "description_ja": "デグーの難産は産科緊急事態で、母体肥満と胎児サイズ負荷が複雑。デグーは短妊娠期間（~93日）で早成性の比較的大型新仔出産。難産は治療時でも母体死亡率高い（20-30%）。",
        "urgency": "emergency",
        "recommended_tests": ["radiographs", "ultrasound", "physical_exam", "blood_panel"],
        "causes": "Maternal obesity (pelvic canal narrowing >70% of cases), inadequate calcium intake (uterine inertia), fetal malpresentation (breech/transverse), large fetal size relative to maternal pelvis, poor dam condition, or metabolic disorders (hypocalcemia, hypoglycemia). Degus bred as first litter after 6+ months show increased risk if pelvic fusion has occurred.",
        "causes_ja": "母体肥満（骨盤管狭窄 >70%症例）、カルシウム摂取不足（子宮無力症）、胎児奇異位（骨盤位/横位）、母体骨盤に対する大型胎児、不良母体体況、代謝障害（低カルシウム血症・低血糖症）。6ヶ月齢以上での初回育種で骨盤融合が進行している場合リスク増加。",
        "pathophysiology": "Dystocia develops when large precocial degus fetuses obstruct the pelvic canal. Myometrial contractions (oxytocin-driven) attempt progression, but prolonged obstruction (>4-6 hours) causes uterine ischemia. Extended labor (>12 hours) results in maternal metabolic acidosis, hypoglycemia, and fetal hypoxia. Degu fetuses are fully furred and developmentally advanced at birth; delayed delivery rapidly leads to fetal death and maceration. Degus show high susceptibility to obstetric shock (maternal mortality 20-30% despite treatment).",
        "pathophysiology_ja": "大型早成性デグー胎児が骨盤管に嵌入すると難産発生。筋層収縮（オキシトシン駆動）が進行試行するが、延長閉塞（>4-6時間）で子宮虚血。長期分娩（>12時間）で母体代謝性アシドーシス・低血糖・胎児低酸素血症。デグー胎児は完全に毛皮で覆われ発達進行；遅延分娩で胎児死亡・腐敗急速。デグーは産科ショックへの高感受性を示し、母体死亡率 20-30% （治療にもかかわらず）。",
        "treatment": "STABILIZATION: IV fluids (lactated Ringer's 50-100 mL/kg), analgesia (meloxicam 0.3-0.5 mg/kg SC q12h). MEDICAL MANAGEMENT: Calcium gluconate 50-100 mg/kg SC with slow infusion and cardiac monitoring. After 30 min, oxytocin 0.5-2 IU/kg SC/IM (once; may repeat × 1 at 20-30 min if non-obstructive dystocia suspected). If obstruction confirmed or no progress >30-60 min: EMERGENCY CESAREAN SECTION under isoflurane anesthesia (avoid injectables due to degu anesthetic sensitivity). Surgical technique: low ventral midline incision, carefully exteriorize uterus, incise antimesentric border, remove all kits carefully, close uterine incision with 4-0 or 5-0 absorbable simple interrupted sutures, abdominal wall with 4-0 absorbable, skin with 4-0 non-absorbable or tissue adhesive. POST-OPERATIVE: analgesia (meloxicam 0.3-0.5 mg/kg SC q12h × 5-7 days), antibiotics (enrofloxacin 5-10 mg/kg SC/IM q12h × 10 days; NEVER β-lactams—fatal GI dysbiosis in degus), IV fluids × 24-48 hours, maintain kit warmth, monitor nursing capacity.",
        "treatment_ja": "安定化：IV輸液（乳酸リンガー 50-100 mL/kg）、鎮痛（メロキシカム 0.3-0.5 mg/kg SC q12h）。医学的管理：グルコン酸カルシウム 50-100 mg/kg SC（緩徐投与、心拍モニタリング）。30分後、オキシトシン 0.5-2 IU/kg SC/IM 1回；非閉塞性難産疑い時は 20-30分間隔で最大1回繰返。閉塞確認または 30-60分無進行：緊急帝王切開術（イソフルラン麻酔；注射薬回避—デグー麻酔感受性）。低腹部正中切開、子宮外転、反中間膜部切開、新仔慎重除去。子宮縫合：4-0または5-0吸収性簡単割符。腹壁：4-0吸収性。皮膚：4-0非吸収性または接着剤。術後：鎮痛（メロキシカム 0.3-0.5 mg/kg SC q12h × 5-7日）、抗菌薬（エンロフロキサシン 5-10 mg/kg SC/IM q12h × 10日；βラクタム禁止—デグーで致死的GI dysbiosis）、IV輸液 × 24-48h、新仔保温、哺乳能力モニタリング。",
        "prevention": "CRITICAL PREVENTION STRATEGY: 1) Weight management: maintain pre-breeding weight 180-220g (obesity dramatically increases dystocia risk; body condition score >3/5 is contraindication to breeding). 2) Breeding age: breed only 3-6 months old (avoid first breeding after 6 months when pelvic fusion may occur). 3) Adequate pre-breeding nutrition: timothy hay ad libitum, balanced pellets 15-20g/day, vitamin C 100+ mg/kg/day (degus cannot synthesize vitamin C—CRITICAL supplementation), calcium 1-1.5%, phosphorus 0.6-1%. 4) Pregnancy nutrition: increase pellet intake to 20-30g/day, maintain vitamin C supplementation. 5) Pair selection: avoid breeding large males with large females; select for maternal-fetal size matching. 6) Minimize stress during late pregnancy (reduce handling, maintain temperature 65-75°F). 7) Monitor for dystocia signs; immediate intervention if dystocia suspected.",
        "prevention_ja": "重大な予防戦略：1) 体重管理：育種前体重 180-220g 維持（肥満が難産リスク劇増；ボディ・コンディション・スコア >3/5 は育種禁忌）。2) 育種年齢：3-6ヶ月齢のみ育種（6ヶ月後の初回育種回避—骨盤融合リスク）。3) 育種前栄養十分：ティモシーヘイ給与量制限なし、バランスペレット 15-20g/日、ビタミンC 100+ mg/kg/日（デグーはビタミンC 合成不可—重大補充必要）、カルシウム 1-1.5%、リン 0.6-1%。4) 妊娠栄養：ペレット摂取 20-30g/日に増量、ビタミンC補充継続。5) ペア選抜：大雄と大雌の交配回避；母体-胎児サイズマッチング選抜。6) 妊娠後期ストレス最小化（取扱い軽減、温度 65-75°F 維持）。7) 難産兆候モニタリング；難産疑い時の直ちの介入。",
        "prognosis": "Maternal survival 50-70% with prompt emergency cesarean (within 1-2 hours of symptom onset); mortality >80% if delayed >4-6 hours. High inherent mortality (20-30%) even with optimal treatment due to degu obstetric shock susceptibility. Fetal mortality increases exponentially with labor duration >12 hours. Kit survival depends on dam recovery; if dam too weak to nurse, supplemental feeding necessary. Post-recovery recurrence risk 50-70%—recommend spay after recovery.",
        "prognosis_ja": "迅速帝王切開（症状発現1-2時間以内）で母体生存率 50-70%；遅延 >4-6時間で死亡率 >80%。最適治療でも固有の死亡率 20-30% （デグー産科ショック感受性）。労働期間 >12時間で胎児死亡率指数関数的増加。新仔生存は母体回復依存；母体虚弱で哺乳不可なら補足給餌必要。産後再発リスク 50-70%—回復後の避妊推奨。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young"},
    },
    {
        "name": "Testicular Tumor",
        "name_ja": "精巣腫瘍",
        "symptoms": {"testicular_swelling", "asymmetric_testes", "lethargy"},
        "description": "Testicular Tumor is a neoplastic condition characterized by abnormal cell proliferation that may be benign or malignant.",
        "description_ja": "片側または両側の精巣に生じる腫瘍。",
        "urgency": "moderate",
        "recommended_tests": ["ultrasound", "fine_needle_aspirate", "histopathology"],
        "causes": "Caused by neoplastic transformation of testicular tissue, with aging, cryptorchidism, and genetic predisposition as primary risk factors.",
        "causes_ja": "デグーにおける精巣腫瘍の原因: 癌遺伝子・腫瘍抑制遺伝子の遺伝子変異蓄積による腫瘍性形質転換。加齢、慢性炎症、ウイルス感染、ホルモン影響、UV曝露、遺伝的素因がリスク因子。",
        "pathophysiology": "Accumulated genetic mutations lead to uncontrolled cell proliferation, evasion of apoptosis, and potential metastatic spread. Tumor growth causes tissue compression, invasion, and paraneoplastic effects.",
        "pathophysiology_ja": "精巣腫瘍はデグーにおける腫瘍性疾患である。癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積により腫瘍性形質転換が生じる。制御不能な細胞増殖により腫瘍が形成され、局所組織への浸潤・破壊の可能性がある。悪性腫瘍はリンパ行性または血行性に転移しうる。高カルシウム血症、悪液質、免疫調節障害などの腫瘍随伴症候群が原発腫瘍に伴い、罹患率に寄与することがある。",
        "treatment": "Orchiectomy (castration) under isoflurane anesthesia is curative for most testicular tumors. Meloxicam 1-2 mg/kg PO SID post-op. Avoid dexamethasone (diabetes risk). Pre-op staging with radiographs if malignancy suspected. Palliative meloxicam if inoperable.",
        "treatment_ja": "イソフルラン麻酔下の精巣摘出術（去勢）がほとんどの精巣腫瘍に根治的。術後メロキシカム1-2 mg/kg PO SID。デキサメタゾンは糖尿病リスクで禁忌。悪性疑いには術前X線で病期評価。切除不能例はメロキシカムで緩和。",
        "prevention": "Prevention is limited for most neoplastic conditions. Regular health examinations facilitate early detection. Spaying/neutering may reduce risk of hormone-dependent tumors.",
        "prevention_ja": "精巣腫瘍の予防は限定的であるが、ホルモン依存性腫瘍軽減のための避妊・去勢手術、既知の発癌物質の回避、早期発見のための定期健診、適正体型の維持、該当する場合は遺伝的素因軽減のための責任ある繁殖が含まれる。",
        "prognosis": "Prognosis depends on tumor type and staging. Benign tumors with complete excision have good prognosis. Malignant tumors require further assessment.",
        "prognosis_ja": "精巣腫瘍の予後: 腫瘍の種類、病期、転移の有無により予後は大きく異なる。早期発見・早期治療で予後改善。悪性腫瘍は一般的に予後要注意〜不良。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    # ── Neurological ───────────────────────────────────────────────────────
    {
        "name": "Seizures (Epilepsy)",
        "name_ja": "てんかん発作",
        "symptoms": {"seizures", "collapse", "disorientation", "drooling"},
        "description": "Seizures (Epilepsy) is a neurological condition affecting the central or peripheral nervous system.",
        "description_ja": "特発性または代謝性疾患に続発する反復性のてんかん発作。",
        "urgency": "high",
        "recommended_tests": ["blood_work", "blood_glucose", "neurological_exam"],
        "causes": "May be idiopathic or secondary to metabolic disorders (hypoglycemia from diabetes), toxin exposure, brain lesions, infection, or electrolyte imbalances.",
        "causes_ja": "デグーの神経系に影響する正確な原因は不明または多因子性。遺伝的素因・環境因子・免疫調節異常・不顕性感染・代謝障害が寄与因子として考えられる。個々の症例での主原因特定にはさらなる調査が必要。",
        "pathophysiology": "Abnormal synchronized neuronal discharge causes involuntary motor activity, autonomic dysfunction, and altered consciousness. Prolonged seizures risk cerebral hypoxia and permanent neurological damage.",
        "pathophysiology_ja": "デグーの神経系に影響する正確な病態生理は完全には解明されていない。遺伝的素因・環境因子・免疫調節異常を含む多因子性メカニズムが関与すると考えられる。神経系組織における炎症性・代謝性・構造的変化が進行性の臨床徴候をもたらす。デグーにおける疾患メカニズムの完全な解明にはさらなる研究が必要。",
        "treatment": "Midazolam 1-2 mg/kg IM/intranasal for acute seizures. Investigate cause (metabolic, toxin, CNS). Phenobarbital 10-15 mg/kg PO q12h for maintenance. Common in degus — may be idiopathic.",
        "treatment_ja": "デグー痙攣の治療: ① 原因鑑別重要—低血糖、低Ca、肝性脳症、感染（E. cuniculi、リステリア）、頭部外傷、毒物。② 緊急: ジアゼパム 0.5-2 mg/kg IM/IV、midazolam 0.2-0.5 mg/kg IM/IN。③ 持続: phenobarbital 2-5 mg/kg IM/IV、levetiracetam 20-30 mg/kg PO/SC q8h。④ 原因治療: 低血糖は5%デキストロース slow IV、低Caはグルコン酸Ca 50-100 mg/kg slow IV、E. cuniculi疑いはfenbendazole 20 mg/kg PO q24h × 28日（ウサギ）、肝性脳症はラクツロース、Hill's l/d、ジアゼパム回避（GABA作動性悪化）。⑤ 検査: 血糖、Ca、ALT、BUN、E. cuniculi抗体、MRI。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "特発性疾患の予後は個々の症例により変動する。自然寛解する場合もあるが、慢性再発性の経過をたどることもある。対症療法と支持療法が治療の中心。定期的な再評価により治療方針を調整する。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Stroke (Cerebrovascular Accident)",
        "name_ja": "脳卒中",
        "symptoms": {"head_tilt", "circling", "loss_of_balance", "seizures", "disorientation"},
        "description": "Stroke (Cerebrovascular Accident) is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "脳内の血管障害により急性の神経症状が出現する。",
        "urgency": "emergency",
        "recommended_tests": ["neurological_exam", "blood_work", "MRI"],
        "causes": "Caused by cerebrovascular ischemia or hemorrhage, potentially secondary to hypertension, atherosclerosis, or coagulopathy.",
        "causes_ja": "デグーにおける脳卒中の原因: 脳内の血管障害により急性の神経症状が出現する。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "脳卒中はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "Supportive care: SC fluids, syringe feed, warmth. Meloxicam 0.2 mg/kg PO q24h. Minimize stress. Prognosis variable.",
        "treatment_ja": "デグーにおける脳卒中の治療は安定化、疼痛管理、創傷ケアを優先する。生命を脅かす損傷を最初に評価・対処する（気道、呼吸、循環）。種に適した鎮痛薬（NSAIDs、オピオイド、局所麻酔薬）による鎮痛が不可欠である。創傷を洗浄・デブリードマンし、一次閉鎖、二次治癒、再建手術を適宜行う。汚染創には広域抗菌薬を使用する。骨折には副子固定または外科的固定を行う。遅発性合併症をモニタリングする。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "脳卒中の予防には安全で種に適した飼育環境の整備、鋭利物・危険物の除去、適切な取り扱い技術、他の動物との接触時の監視、温度管理、落下防止策が含まれる。",
        "prognosis": "Prognosis depends on severity, underlying cause, and timeliness of treatment. Early aggressive intervention generally improves outcomes. Delayed presentation carries a guarded to poor prognosis.",
        "prognosis_ja": "脳卒中の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Vestibular Disease",
        "name_ja": "前庭疾患",
        "symptoms": {"head_tilt", "loss_of_balance", "circling", "nystagmus"},
        "description": "Vestibular Disease is a neurological condition affecting the central or peripheral nervous system.",
        "description_ja": "前庭系の機能障害によるバランス異常。",
        "urgency": "moderate",
        "recommended_tests": ["neurological_exam", "otoscopic_exam", "radiographs"],
        "causes": "Caused by inner ear infection (otitis interna), idiopathic vestibular syndrome, brain lesions, or E. cuniculi infection affecting the vestibular apparatus.",
        "causes_ja": "デグーの神経系に影響する正確な原因は不明または多因子性。遺伝的素因・環境因子・免疫調節異常・不顕性感染・代謝障害が寄与因子として考えられる。個々の症例での主原因特定にはさらなる調査が必要。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "デグーの神経系に影響する正確な病態生理は完全には解明されていない。遺伝的素因・環境因子・免疫調節異常を含む多因子性メカニズムが関与すると考えられる。神経系組織における炎症性・代謝性・構造的変化が進行性の臨床徴候をもたらす。デグーにおける疾患メカニズムの完全な解明にはさらなる研究が必要。",
        "treatment": "IDENTIFY UNDERLYING CAUSE: (1) Otitis interna/media — most common treatable cause. "
        "Otoscopic examination, skull radiographs, ideally CT/MRI for bulla assessment. Treat with "
        "systemic antibiotics: enrofloxacin 5-10 mg/kg PO/SC q12h × 21-28 days (excellent CNS "
        "penetration), or trimethoprim-sulfa 15-30 mg/kg PO q12h. Topical ear treatment if "
        "tympanic membrane intact. (2) Encephalitozoon cuniculi — reported in degus; treat with "
        "fenbendazole 20 mg/kg PO q24h × 28 days (inhibits microsporidial replication). "
        "(3) Central causes (cerebrovascular accident, neoplasia) — poor prognosis, supportive "
        "care only. SUPPORTIVE CARE: Anti-nausea/vertigo: maropitant (Cerenia) 1 mg/kg SC q24h "
        "× 3-5 days (reduces vestibular nausea). Meclizine 2-12 mg/kg PO q24h (antihistamine "
        "vestibular suppressant — extrapolated). Maintain hydration: SC fluids 50-100 mL/kg/day "
        "if not eating/drinking. Syringe feeding if anorexic: Critical Care for Herbivores q4-6h. "
        "ENVIRONMENTAL SAFETY: Padded cage with low platforms (prevent fall injuries during "
        "ataxia). Remove running wheel temporarily. Place food/water at floor level. Quiet, "
        "dim environment reduces vestibular stimulation. PAIN MANAGEMENT: Meloxicam 1-2 mg/kg "
        "PO/SC q24h. RECOVERY: Vestibular compensation typically occurs over 2-4 weeks even "
        "without complete resolution of underlying cause. Residual head tilt may persist "
        "permanently but does not affect quality of life. NOTE: Oral β-lactam antibiotics are "
        "CONTRAINDICATED in degus. References: Quesenberry & Carpenter (2012); Jekl & "
        "Redrobe (2013) BSAVA Manual.",
        "treatment_ja": "デグー前庭疾患: 鑑別—中耳炎/内耳炎、脳炎、外傷、腫瘍、特発性。① 診断: 神経学的検査、耳鏡、X線/CT（耳道・bulla）、CBC・血清化学・血液培養。② 細菌性中耳炎/内耳炎: 培養感受性に基づく全身抗菌薬3-6週（エンロフロキサシン 5-15 mg/kg PO q12-24h）、重症例は鼓室洗浄。③ 対症療法: メクリジン 2-12 mg/kg PO q8-24h、メロキシカム 0.5-1 mg/kg PO q12-24h、輸液 80 mL/kg/日 SC。④ 自傷・転倒防止のためパッド入りケージ、シリンジ給餌で栄養維持。⑤ 重症・進行性は脳腫瘍・脳症の鑑別にMRI/CT。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。"
        "理想的にはCT/MRIで鼓室評価。全身性抗菌薬: エンロフロキサシン5-10 mg/kg PO/SC q12h "
        "× 21-28日（優れたCNS浸透性）、またはTMS 15-30 mg/kg PO q12h。(2) エンセファリト"
        "ゾーン・クニクリ — デグーでも報告あり; フェンベンダゾール20 mg/kg PO q24h × 28日。"
        "(3) 中枢性（脳血管障害、腫瘍）— 予後不良、支持療法のみ。【支持療法】制吐/めまい: "
        "マロピタント1 mg/kg SC q24h × 3-5日。メクリジン2-12 mg/kg PO q24h。水和維持: "
        "食欲がなければ皮下補液。シリンジ給餌。【環境安全】パッド付きケージ、低い段差（運動失調"
        "中の転落防止）。回し車を一時的に撤去。食餌・水を床面に配置。静かで薄暗い環境。"
        "【回復】前庭代償は通常2-4週間で起こる。残存する斜頸は永続する場合があるがQOLに影響"
        "しない。注: 経口βラクタム系抗菌薬はデグーでは禁忌。",
        "prevention": "Prompt treatment of ear infections (otitis externa) before progression to otitis media/"
        "interna. Maintain clean, well-ventilated cage to reduce respiratory and ear infection risk. "
        "Quarantine new animals for 2-4 weeks (E. cuniculi transmission risk). Avoid overcrowding "
        "and stress. Regular health checks — early detection of head tilt or balance abnormalities. "
        "Reference: Quesenberry & Carpenter (2012).",
        "prevention_ja": "耳感染症（外耳炎）の迅速な治療で中耳炎/内耳炎への進行を予防。清潔で換気の良いケージ"
        "維持。新規動物の2-4週間隔離（E. cuniculi伝播リスク）。過密飼育とストレスの回避。"
        "定期健診 — 斜頸やバランス異常の早期発見。",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "特発性疾患の予後は個々の症例により変動する。自然寛解する場合もあるが、慢性再発性の経過をたどることもある。対症療法と支持療法が治療の中心。定期的な再評価により治療方針を調整する。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Hind Limb Paralysis",
        "name_ja": "後肢麻痺",
        "symptoms": {"hind_leg_paralysis", "incontinence", "dragging_legs", "pain"},
        "description": "Hind Limb Paralysis is a neurological condition affecting the central or peripheral nervous system.",
        "description_ja": "脊髄損傷、脳卒中、椎間板疾患による後肢機能の喪失。",
        "urgency": "emergency",
        "recommended_tests": ["radiographs", "neurological_exam", "MRI"],
        "causes": "Caused by spinal cord injury (fracture, disc disease), cerebrovascular accident, peripheral neuropathy (diabetic), or degenerative myelopathy.",
        "causes_ja": "デグーにおける後肢麻痺の原因: 脊髄損傷、脳卒中、椎間板疾患による後肢機能の喪失。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "後肢麻痺はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "Dexamethasone 1-2 mg/kg SC single dose if acute spinal injury. Cage rest on padded surface. Meloxicam 0.2 mg/kg PO q24h. R/O IVDD, fracture, neoplasia. Radiographs. Quality of life assessment.",
        "treatment_ja": "デグーにおける後肢麻痺の治療は安定化、疼痛管理、創傷ケアを優先する。生命を脅かす損傷を最初に評価・対処する（気道、呼吸、循環）。種に適した鎮痛薬（NSAIDs、オピオイド、局所麻酔薬）による鎮痛が不可欠である。創傷を洗浄・デブリードマンし、一次閉鎖、二次治癒、再建手術を適宜行う。汚染創には広域抗菌薬を使用する。骨折には副子固定または外科的固定を行う。遅発性合併症をモニタリングする。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "後肢麻痺の予防には安全で種に適した飼育環境の整備、鋭利物・危険物の除去、適切な取り扱い技術、他の動物との接触時の監視、温度管理、落下防止策が含まれる。",
        "prognosis": "Prognosis depends on severity, underlying cause, and timeliness of treatment. Early aggressive intervention generally improves outcomes. Delayed presentation carries a guarded to poor prognosis.",
        "prognosis_ja": "後肢麻痺の予後: 原因により予後が大きく異なる。炎症性疾患は治療に反応する場合がある。変性性疾患は進行性で予後要注意〜不良。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    # ── Cardiac ────────────────────────────────────────────────────────────
    {
        "name": "Congestive Heart Failure",
        "name_ja": "うっ血性心不全",
        "symptoms": {"labored_breathing", "lethargy", "cyanosis", "reduced_activity", "collapse"},
        "description": "Congestive Heart Failure is a cardiovascular condition affecting cardiac function and hemodynamic stability.",
        "description_ja": "心臓のポンプ機能低下による体液貯留。",
        "urgency": "emergency",
        "recommended_tests": ["chest_radiographs", "echocardiography", "blood_work"],
        "causes": "Caused by progressive cardiac degeneration from aging, valvular disease, cardiomyopathy, or chronic hypertension, often exacerbated by high-sugar diets.",
        "causes_ja": "加齢・慢性的摩耗・累積的損傷による心血管系組織の進行性劣化が原因。遺伝的素因・慢性炎症・酸化ストレス・不適切な飼育条件が寄与。デグーの飼育管理と食事因子が変性変化を加速しうる。",
        "pathophysiology": "Myocardial dysfunction impairs cardiac output through reduced contractility, abnormal relaxation, or rhythm disturbances. Compensatory mechanisms eventually fail, leading to congestive heart failure.",
        "pathophysiology_ja": "デグーの心血管系組織における進行性変性変化は、細胞構造と機能の漸進的喪失を伴う。酸化ストレス・慢性炎症・細胞老化・組織修復障害が関与する。加齢変化・累積的環境侵襲・遺伝的素因が疾患進行に寄与する。飼育管理と食事要因が変性疾患を悪化させうる。",
        "treatment": "Treatment includes diuretics, ACE inhibitors, positive inotropes, antiarrhythmics as indicated, dietary sodium restriction, and activity modification. Regular monitoring of cardiac function is essential.",
        "treatment_ja": "デグーにおけるうっ血性心不全の治療: 心エコーで基礎心疾患を評価。利尿薬（フロセミド）で肺水腫管理。ACE阻害薬で後負荷軽減。不整脈があれば抗不整脈薬。安静・低Na食。定期心エコーでモニタリング。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis varies by disease severity and response to treatment. Early-stage disease may be managed for extended periods, while advanced failure carries a guarded prognosis.",
        "prognosis_ja": "変性疾患の予後は進行速度と管理可能性に依存する。緩徐進行性の場合、適切な対症療法とQOL管理で長期生存が可能。急速進行性の場合は予後不良。定期的な再評価と治療調整が重要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Cardiomyopathy",
        "name_ja": "心筋症",
        "symptoms": {"labored_breathing", "lethargy", "reduced_activity", "collapse"},
        "description": "Cardiomyopathy is a cardiovascular condition affecting cardiac function and hemodynamic stability.",
        "description_ja": "心筋の疾患により心機能が障害される。",
        "urgency": "high",
        "recommended_tests": ["echocardiography", "chest_radiographs", "ECG"],
        "causes": "Caused by progressive degeneration of the myocardium due to aging, genetic predisposition, nutritional deficiencies, or chronic metabolic disease including diabetes.",
        "causes_ja": "加齢・慢性的摩耗・累積的損傷による心血管系組織の進行性劣化が原因。遺伝的素因・慢性炎症・酸化ストレス・不適切な飼育条件が寄与。デグーの飼育管理と食事因子が変性変化を加速しうる。",
        "pathophysiology": "Myocardial dysfunction impairs cardiac output through reduced contractility, abnormal relaxation, or rhythm disturbances. Compensatory mechanisms eventually fail, leading to congestive heart failure.",
        "pathophysiology_ja": "デグーの心血管系組織における進行性変性変化は、細胞構造と機能の漸進的喪失を伴う。酸化ストレス・慢性炎症・細胞老化・組織修復障害が関与する。加齢変化・累積的環境侵襲・遺伝的素因が疾患進行に寄与する。飼育管理と食事要因が変性疾患を悪化させうる。",
        "treatment": "Treatment includes diuretics, ACE inhibitors, positive inotropes, antiarrhythmics as indicated, dietary sodium restriction, and activity modification. Regular monitoring of cardiac function is essential.",
        "treatment_ja": "デグーにおける心筋症の治療: 心エコーで基礎心疾患を評価。利尿薬（フロセミド）で肺水腫管理。ACE阻害薬で後負荷軽減。不整脈があれば抗不整脈薬。安静・低Na食。定期心エコーでモニタリング。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis varies by disease severity and response to treatment. Early-stage disease may be managed for extended periods, while advanced failure carries a guarded prognosis.",
        "prognosis_ja": "変性疾患の予後は進行速度と管理可能性に依存する。緩徐進行性の場合、適切な対症療法とQOL管理で長期生存が可能。急速進行性の場合は予後不良。定期的な再評価と治療調整が重要。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    # ── Additional conditions ──────────────────────────────────────────────
    {
        "name": "Ear Infection (Otitis)",
        "name_ja": "耳感染症（外耳炎）",
        "symptoms": {"head_tilt", "scratching_ear", "ear_discharge", "loss_of_balance"},
        "description": "Ear Infection (Otitis) is a bacterial infection that causes systemic or localized inflammatory disease requiring prompt antimicrobial therapy.",
        "description_ja": "細菌やダニによる外耳または中耳の感染。",
        "urgency": "moderate",
        "recommended_tests": ["otoscopic_exam", "ear_cytology", "bacterial_culture"],
        "causes": "Multifactorial etiology including infectious, environmental, immune, and host-related factors. Specific risk factors and triggers vary by individual case.",
        "causes_ja": "爬虫類における耳感染症（中耳炎）の原因: カメや一部のトカゲに多い中耳・内耳感染症。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "耳感染症（中耳炎）は爬虫類における細菌感染症である。病原菌は付着因子を通じて組織にコロニーを形成し、毒素産生、酵素分泌、免疫回避戦略などの病原性メカニズムを介して侵入する。好中球浸潤、サイトカイン放出、補体活性化を含む炎症カスケードが生じる。組織損傷は細菌の直接作用と宿主の炎症反応の両方に起因する。菌種と宿主の免疫状態に応じて、膿瘍形成、敗血症、または慢性肉芽腫性炎症が発生しうる。",
        "treatment": "Antimicrobial therapy based on culture and sensitivity, wound care or drainage as needed, pain management, and monitoring for resolution.",
        "treatment_ja": "爬虫類における耳感染症（中耳炎）の治療には、可能であれば培養感受性試験に基づく標的抗菌薬療法が必要である。結果待ちの間は経験的広域抗菌薬を開始する。抗菌薬治療期間は感染の排除と耐性予防に十分な期間とする。膿瘍や壊死組織には外科的排膿またはデブリードマンが必要な場合がある。支持療法として輸液、鎮痛薬、抗炎症薬、栄養サポートを行う。",
        "prevention": "Prevention includes maintaining proper hygiene, appropriate husbandry, stress reduction, quarantine of new animals, and prompt treatment of wounds or primary conditions.",
        "prevention_ja": "耳感染症（中耳炎）の予防には適切な衛生管理・消毒、利用可能なワクチン接種、創傷の迅速な処置、ストレス軽減、適切な換気、感染動物の隔離が含まれる。",
        "prognosis": "Good with appropriate antimicrobial therapy. Most infections resolve with proper treatment. Chronic or recurrent cases may require longer management.",
        "prognosis_ja": "耳感染症（外耳炎）の予後: 適切な抗菌薬療法で多くが治癒可能。慢性・深在性感染は長期治療が必要。敗血症は予後要注意。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Vitamin C Deficiency (Scurvy)",
        "name_ja": "ビタミンC欠乏症（壊血病）",
        "symptoms": {"lethargy", "swollen_joints", "lameness", "rough_coat", "bleeding_gums"},
        "description": "Vitamin C Deficiency (Scurvy) is a nutritional or metabolic disorder caused by dietary imbalance or deficiency.",
        "description_ja": "食事中のビタミンC不足により壊血病を発症することがある。",
        "urgency": "moderate",
        "recommended_tests": ["blood_work", "physical_exam"],
        "causes": "Caused by insufficient dietary vitamin C intake. Unlike guinea pigs, degus can synthesize some vitamin C, but deficiency may occur under stress or with inadequate diet.",
        "causes_ja": "デグーにおけるビタミンC欠乏症（壊血病）の原因: 食事中のビタミンC不足により壊血病を発症することがある。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "ビタミンC欠乏症（壊血病）はデグーにおける栄養障害である。特定の栄養素の不十分な摂取、吸収不良、または過剰摂取により生じる。欠乏状態では、影響を受けた栄養素を補因子または基質として必要とする生化学的経路が障害され、細胞機能障害を引き起こす。過剰状態では組織への蓄積や栄養素間相互作用の障害により毒性が生じる。種特異的な食事要求により、適切な栄養管理が予防に不可欠である。",
        "treatment": "IMPORTANT NOTE: Unlike guinea pigs, degus CAN synthesize vitamin C endogenously. True scurvy "
        "is rare in degus but may occur under severe stress, chronic illness, or extremely poor diet. "
        "ACUTE SUPPLEMENTATION: Ascorbic acid 50-100 mg/kg PO q24h × 7-14 days (dissolve in water "
        "or administer directly via syringe — vitamin C degrades rapidly in water, replace daily). "
        "Alternatively, injectable vitamin C 50 mg/kg SC q24h × 5-7 days for severe cases with "
        "anorexia. DIETARY CORRECTION: Ensure access to vitamin C-rich vegetables — dark leafy "
        "greens (kale, parsley, dandelion greens), bell peppers (GREEN only — red/yellow have more "
        "sugar, AVOID in degus due to diabetes risk). Timothy hay should remain the dietary "
        "base (≥80%). Small amounts of fresh herbs (cilantro, basil). CRITICAL: NO fruit — even "
        "citrus fruits that are vitamin C-rich are CONTRAINDICATED in degus due to high sugar "
        "content. PAIN MANAGEMENT: Meloxicam 1-2 mg/kg PO/SC q24h for joint pain/swelling. "
        "SUPPORTIVE CARE: SC fluids if dehydrated. Syringe feeding with Critical Care for "
        "Herbivores if anorexic. RULE OUT: Concurrent diabetes (blood glucose), dental disease "
        "(oral exam), and other nutritional deficiencies (calcium, vitamin D). Differential "
        "diagnosis includes MBD, osteoarthritis, and periodontal disease. "
        "References: Quesenberry & Carpenter (2012); Edwards (2009) Vet Clin Exot Anim.",
        "treatment_ja": "【重要】モルモットと異なり、デグーは内因性にビタミンCを合成可能。真の壊血病はまれだが、"
        "重度のストレス・慢性疾患・極端な食事不良で発生しうる。【急性補充】アスコルビン酸"
        "50-100 mg/kg PO q24h × 7-14日（水に溶解またはシリンジで直接投与 — ビタミンCは水中で"
        "急速に分解、毎日交換）。重症例: 注射用ビタミンC 50 mg/kg SC q24h × 5-7日。"
        "【食事是正】ビタミンC豊富な野菜: 葉野菜（ケール、パセリ、タンポポ）、ピーマン（緑のみ"
        " — 赤/黄は糖分が多くデグーでは糖尿病リスクにより回避）。チモシー牧草を食事の基盤に"
        "維持（≥80%）。重要: 果物は禁忌 — 柑橘類もビタミンC豊富だが高糖分のためデグーでは禁忌。"
        "【疼痛管理】メロキシカム1-2 mg/kg PO/SC q24h。【鑑別診断】MBD、変形性関節症、"
        "歯周病との鑑別。",
        "prevention": "Prevention includes providing a balanced, species-appropriate diet with adequate vitamins and minerals, appropriate UVB lighting where needed, and regular nutritional assessment.",
        "prevention_ja": "ビタミンC欠乏症（壊血病）の予防には全ての栄養要求を満たす種に適した食事設計、単一食品のみの食事の回避、獣医師との定期的な食事内容の見直し、必要時の適切なサプリメンテーション、種固有の栄養ニーズに関する知識が必要である。",
        "prognosis": "Good with dietary correction and supplementation. Clinical signs typically improve within weeks of appropriate nutrition. Severe cases may have residual deficits.",
        "prognosis_ja": "ビタミンC欠乏症（壊血病）の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Septicemia",
        "name_ja": "敗血症",
        "symptoms": {"fever", "lethargy", "rapid_breathing", "collapse", "dehydration"},
        "description": "Septicemia is a bacterial infection that causes systemic or localized inflammatory disease requiring prompt antimicrobial therapy.",
        "description_ja": "血流への細菌侵入を伴う全身性の細菌感染。",
        "urgency": "emergency",
        "recommended_tests": ["blood_culture", "blood_work", "physical_exam"],
        "causes": "Caused by systemic bacterial invasion of the bloodstream, often secondary to wound infection, dental disease, urinary tract infection, or pyometra.",
        "causes_ja": "デグーにおける敗血症の原因: 創傷汚染、経口摂取、吸入、日和見的過剰増殖による細菌コロニー形成。ストレス、免疫抑制、不衛生、過密飼育、併発疾患が素因となる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "敗血症はデグーにおける細菌感染症である。病原菌は付着因子を通じて組織にコロニーを形成し、毒素産生、酵素分泌、免疫回避戦略などの病原性メカニズムを介して侵入する。好中球浸潤、サイトカイン放出、補体活性化を含む炎症カスケードが生じる。組織損傷は細菌の直接作用と宿主の炎症反応の両方に起因する。菌種と宿主の免疫状態に応じて、膿瘍形成、敗血症、または慢性肉芽腫性炎症が発生しうる。",
        "treatment": "Aggressive IV fluid resuscitation, broad-spectrum IV antibiotics, vasopressor support if hypotensive, source control (drainage of abscess/infected focus), and intensive monitoring. Consider blood culture before antibiotic initiation.",
        "treatment_ja": "デグーにおける敗血症の治療には、可能であれば培養感受性試験に基づく標的抗菌薬療法が必要である。結果待ちの間は経験的広域抗菌薬を開始する。抗菌薬治療期間は感染の排除と耐性予防に十分な期間とする。膿瘍や壊死組織には外科的排膿またはデブリードマンが必要な場合がある。支持療法として輸液、鎮痛薬、抗炎症薬、栄養サポートを行う。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "敗血症の予防には適切な衛生管理・消毒、利用可能なワクチン接種、創傷の迅速な処置、ストレス軽減、適切な換気、感染動物の隔離が含まれる。",
        "prognosis": "Guarded prognosis. Mortality rates are significant even with aggressive treatment. Early intervention improves survival. Multi-organ dysfunction carries a poor prognosis.",
        "prognosis_ja": "敗血症の予後: 適切な抗菌薬療法で多くが治癒可能。慢性・深在性感染は長期治療が必要。敗血症は予後要注意。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Dehydration",
        "name_ja": "脱水症",
        "symptoms": {"dehydration", "lethargy", "sunken_eyes", "reduced_activity"},
        "description": "Dehydration is a condition of inadequate body fluid volume requiring fluid replacement therapy.",
        "description_ja": "水分摂取不足や疾病による過度な水分喪失。",
        "urgency": "moderate",
        "recommended_tests": ["skin_turgor_test", "blood_work", "physical_exam"],
        "causes": "Caused by insufficient water intake (malfunctioning water bottle, unfamiliarity with sipper), excessive fluid loss from diarrhea, or concurrent illness reducing drinking behavior.",
        "causes_ja": "デグーにおける脱水の原因: 必須栄養素の欠乏・過剰・吸収不良を含む食事バランスの異常。不適切な食事組成、単調な給餌、種に不適切な食物、吸収障害が主要因。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "脱水はデグーにおける栄養障害である。特定の栄養素の不十分な摂取、吸収不良、または過剰摂取により生じる。欠乏状態では、影響を受けた栄養素を補因子または基質として必要とする生化学的経路が障害され、細胞機能障害を引き起こす。過剰状態では組織への蓄積や栄養素間相互作用の障害により毒性が生じる。種特異的な食事要求により、適切な栄養管理が予防に不可欠である。",
        "treatment": "SC fluids: LRS 50-100 mL/kg bolus. Syringe water/electrolytes PO. Offer fresh vegetables for moisture. Treat underlying cause.",
        "treatment_ja": "デグー脱水症の治療: ① 評価—皮膚弾力（小型では限定的）、体重トレンド、PCV/TS、粘膜湿潤。② 輸液製剤: 温乳酸リンゲルまたはノルモソルR。③ 投与経路: 軽-中等度はSC（背中皮下 80-100 mL/kg/日 分割）、重度・ショックはIO（脛骨近位 10-20 mL/kg q4-6h）または小型でもIV試行。④ 保温（26-28℃）が吸収・代謝に必須。⑤ シリンジ給餌（Critical Care 50-90 mL/kg/日）併用で経口水分も補給。⑥ K補正注意深く、Ca補正（Hypocalcemia時）50-100 mg/kg PO/IV。⑦ 原疾患治療: 草食種のGI stasis、肉食種の嘔吐/下痢、高体温の制御。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "脱水の予防には全ての栄養要求を満たす種に適した食事設計、単一食品のみの食事の回避、獣医師との定期的な食事内容の見直し、必要時の適切なサプリメンテーション、種固有の栄養ニーズに関する知識が必要である。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "脱水症の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Rectal Prolapse",
        "name_ja": "直腸脱",
        "symptoms": {"tissue_protrusion_anus", "straining", "bloody_stool", "lethargy"},
        "description": "Rectal Prolapse involves protrusion of an organ or tissue from its normal anatomical position.",
        "description_ja": "いきみや寄生虫により直腸粘膜が肛門から突出する。",
        "urgency": "high",
        "recommended_tests": ["physical_exam", "fecal_exam"],
        "causes": "Caused by excessive straining from diarrhea, intestinal parasites, constipation, or colitis leading to eversion of rectal mucosa through the anus.",
        "causes_ja": "消化器系組織への物理的外傷が原因。転落・ケージ損傷・取扱い事故・同居個体や捕食者からの咬傷・環境危険物が一般的原因。デグーの解剖学的特性が特定の損傷タイプへの素因となりうる。二次合併症として感染・治癒遅延・慢性疼痛がある。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "デグーの消化器系組織への外傷性損傷は、挫傷・裂傷・骨折を含む直接的な機械的組織損傷を引き起こす。急性炎症反応により浮腫・出血・疼痛が生じる。二次合併症として細菌汚染・感染・治癒遅延がある。デグーでは損傷からのストレスが追加の全身合併症を引き起こしうる。",
        "treatment": "Gentle reduction under isoflurane using sugar solution. Purse-string suture (4-0 absorbable) 48-72h. Treat underlying cause (parasites, enteritis). Meloxicam 0.2 mg/kg SC.",
        "treatment_ja": "デグーにおける直腸脱の治療: 輸液で脱水補正。消化管運動促進薬。制吐薬。疼痛管理。食事管理（繊維質の確保）。原因に応じた特異的治療。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "外傷の予後は損傷の重症度と合併症の有無に依存する。軽度外傷は適切な創傷管理で予後良好。重度外傷、多発骨折、脊髄損傷は予後慎重〜不良。早期治療と適切な疼痛管理が回復を促進する。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Diabetes-related Neuropathy",
        "name_ja": "糖尿病性神経障害",
        "symptoms": {"hind_leg_paralysis", "dragging_legs", "loss_of_balance", "hyperglycemia"},
        "description": "Diabetes-related Neuropathy is a metabolic disorder affecting glucose regulation and energy metabolism.",
        "description_ja": "慢性的な高血糖による神経障害で後肢の衰弱が生じる。",
        "urgency": "high",
        "recommended_tests": ["blood_glucose", "neurological_exam"],
        "causes": "Caused by chronic hyperglycemia-induced damage to peripheral nerves through polyol pathway activation and advanced glycation end-product accumulation.",
        "causes_ja": "デグーにおける糖尿病性神経障害の原因: 慢性的な高血糖による神経障害で後肢の衰弱が生じる。",
        "pathophysiology": "Impaired insulin production or action leads to persistent hyperglycemia, causing osmotic diuresis, cellular energy deficit, and progressive damage to vascular endothelium, nerves, and organs.",
        "pathophysiology_ja": "糖尿病性神経障害はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "Insulin therapy with dose titration based on glucose curves, dietary management with consistent high-fiber meals, regular blood glucose monitoring, and management of concurrent conditions.",
        "treatment_ja": "糖尿病性神経障害はdeguでは非常に稀。報告例ではインスリン依存性で、プロジンク 0.5-1 IU/動物 SC q12h から開始、家庭での血糖モニタ（耳介穿刺、CGM試験的）と組み合わせる。低糖質・高繊維食。インスリン抵抗性をきたす副腎疾患・甲状腺疾患・肥満を除外。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes maintaining appropriate body weight through balanced diet and adequate exercise, regular health monitoring, and avoiding high-sugar/high-fat foods.",
        "prevention_ja": "糖尿病性神経障害の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Fair to good with dedicated owner compliance and proper insulin management. Uncontrolled diabetes leads to serious complications including ketoacidosis.",
        "prognosis_ja": "糖尿病性神経障害の予後: 原因により予後が大きく異なる。炎症性疾患は治療に反応する場合がある。変性性疾患は進行性で予後要注意〜不良。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Diabetes Mellitus - Type 1 (Juvenile Onset)",
        "name_ja": "糖尿病 - 1型（若年発症）",
        "symptoms": {"excessive_hunger", "lethargy", "polydipsia", "polyuria", "weight_loss"},
        "description": "Diabetes Mellitus - Type 1 (Juvenile Onset) is a metabolic disorder affecting glucose regulation and energy metabolism.",
        "description_ja": "ベータ細胞の自己免疫破壊による若いデグーのインスリン依存性糖尿病。デグーは糖尿病研究で最も一般的な齧歯類モデルです。",
        "urgency": "high",
        "recommended_tests": ["blood_glucose", "fructosamine", "urinalysis"],
        "treatment": "Insulin therapy with dose titration based on glucose curves, dietary management with consistent high-fiber meals, regular blood glucose monitoring, and management of concurrent conditions.",
        "treatment_ja": "糖尿病 - 1型（若年発症）はdeguでは非常に稀。報告例ではインスリン依存性で、プロジンク 0.5-1 IU/動物 SC q12h から開始、家庭での血糖モニタ（耳介穿刺、CGM試験的）と組み合わせる。低糖質・高繊維食。インスリン抵抗性をきたす副腎疾患・甲状腺疾患・肥満を除外。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prognosis": "Fair to good with dedicated owner compliance and proper insulin management. Uncontrolled diabetes leads to serious complications including ketoacidosis.",
        "prognosis_ja": "飼い主の協力と適切なインスリン管理があれば予後やや良好〜良好。管理不良の糖尿病はケトアシドーシス等の重篤な合併症を招く。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Diabetes Mellitus - Type 2 (Diet-Induced)",
        "name_ja": "糖尿病 - 2型（食事誘発性）",
        "symptoms": {"lethargy", "obesity", "polydipsia", "polyuria", "poor_coat"},
        "description": "Diabetes Mellitus - Type 2 (Diet-Induced) is a metabolic disorder affecting glucose regulation and energy metabolism.",
        "description_ja": "高糖質食による非インスリン依存性糖尿病。デグーは食事中の糖に非常に敏感で、容易に糖尿病を発症します。",
        "urgency": "high",
        "recommended_tests": ["blood_glucose", "fructosamine", "diet_review"],
        "treatment": "Insulin therapy with dose titration based on glucose curves, dietary management with consistent high-fiber meals, regular blood glucose monitoring, and management of concurrent conditions.",
        "treatment_ja": "糖尿病 - 2型（食事誘発性）はdeguでは非常に稀。報告例ではインスリン依存性で、プロジンク 0.5-1 IU/動物 SC q12h から開始、家庭での血糖モニタ（耳介穿刺、CGM試験的）と組み合わせる。低糖質・高繊維食。インスリン抵抗性をきたす副腎疾患・甲状腺疾患・肥満を除外。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prognosis": "Fair to good with dedicated owner compliance and proper insulin management. Uncontrolled diabetes leads to serious complications including ketoacidosis.",
        "prognosis_ja": "飼い主の協力と適切なインスリン管理があれば予後やや良好〜良好。管理不良の糖尿病はケトアシドーシス等の重篤な合併症を招く。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Diabetic Retinopathy",
        "name_ja": "糖尿病性網膜症",
        "symptoms": {"bumping_into_objects", "dilated_pupils", "vision_loss"},
        "description": "Diabetic Retinopathy is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "慢性高血糖による進行性の網膜損傷で失明を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["ophthalmic_exam", "blood_glucose", "fundoscopy"],
        "causes": "Progressive retinal damage from chronic hyperglycaemia causing blindness.",
        "causes_ja": "デグーにおける糖尿病性網膜症の原因: 慢性高血糖による進行性の網膜損傷で失明を引き起こします。",
        "pathophysiology": "Diabetic Retinopathy is a metabolic/endocrine disorder. Progressive retinal damage from chronic hyperglycaemia causing blindness. The underlying pathology involves dysregulation of hormonal feedback loops, enzyme activity, or substrate metabolism. This leads to imbalances in circulating hormone levels, electrolytes, or metabolic intermediates that affect cellular function across multiple organ systems. Compensatory mechanisms may temporarily maintain homeostasis but eventually decompensate, leading to progressive clinical deterioration and multi-organ effects.",
        "pathophysiology_ja": "糖尿病性網膜症はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "NO DIRECT TREATMENT for retinopathy itself — focus on glycemic control to halt progression. "
        "GLYCEMIC MANAGEMENT (PRIMARY): Strict dietary control — eliminate ALL sugar-containing foods, "
        "timothy hay-based diet (≥80%), no fruit, no root vegetables, no commercial treats with "
        "added sugars. Target fasting blood glucose <200 mg/dL. Monitor fructosamine levels q4-8 "
        "weeks (reflects 2-3 week average glycemic control). NOTE: Insulin therapy is not standard "
        "practice in degus — dietary management alone is the approach. OPHTHALMIC MONITORING: "
        "Fundoscopic examination every 2-3 months to track retinal changes. Slit lamp examination "
        "for concurrent diabetic cataracts (reported in up to 30% of diabetic degus — bilateral "
        "lens opacity). ENVIRONMENTAL ADAPTATION: If visual impairment confirmed — maintain "
        "consistent cage layout, avoid rearranging furniture, use auditory/olfactory cues, pad "
        "sharp edges. Degus compensate well for vision loss using whiskers, auditory, and "
        "olfactory senses (highly social communication). Remove dangerous heights/drops from cage. "
        "CONCURRENT COMPLICATIONS: Screen for diabetic nephropathy (urinalysis for proteinuria), "
        "peripheral neuropathy (hind limb proprioception), hepatic lipidosis. PROGNOSIS: Retinal "
        "damage is largely irreversible once established. Early glycemic control is the ONLY "
        "effective intervention. References: Edwards (2009) Vet Clin Exot Anim; Jekl et al. "
        "(2011) J Small Anim Pract.",
        "treatment_ja": "糖尿病性網膜症はdeguでは非常に稀。報告例ではインスリン依存性で、プロジンク 0.5-1 IU/動物 SC q12h から開始、家庭での血糖モニタ（耳介穿刺、CGM試験的）と組み合わせる。低糖質・高繊維食。インスリン抵抗性をきたす副腎疾患・甲状腺疾患・肥満を除外。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。"
        "【血糖管理（最重要）】厳格な食事管理 — 糖分を含む全食品の排除、チモシー牧草ベース食"
        "（≥80%）、果物・根菜・糖分添加おやつ禁忌。空腹時血糖<200 mg/dLを目標。フルクトサミン"
        "を4-8週ごとにモニタリング。注: デグーではインスリン療法は標準的実践ではない — "
        "食事管理が唯一のアプローチ。【眼科モニタリング】眼底検査を2-3ヶ月ごとに実施。細隙灯"
        "検査で併発する糖尿病性白内障を確認（糖尿病デグーの最大30%で報告）。【環境適応】視覚"
        "障害が確認されたら — ケージレイアウトを一定に維持、聴覚/嗅覚の手がかりを利用、"
        "危険な高さ/落下を排除。【併存症スクリーニング】糖尿病性腎症、末梢神経障害、肝リピドーシス。"
        "網膜損傷は確立後はほぼ不可逆 — 早期血糖管理が唯一の有効介入。",
        "prevention": "Prevention of diabetic retinopathy includes appropriate diet formulation, regular health monitoring with blood work, maintaining healthy body weight, avoiding excessive treats or inappropriate foods, and early intervention when subclinical changes are detected.",
        "prevention_ja": "糖尿病性網膜症の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "糖尿病性網膜症の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Diabetic Nephropathy",
        "name_ja": "糖尿病性腎症",
        "symptoms": {"edema", "lethargy", "polydipsia", "polyuria", "weight_loss"},
        "description": "Diabetic Nephropathy is a renal condition affecting kidney function and fluid-electrolyte balance.",
        "description_ja": "慢性糖尿病による進行性の腎障害で、タンパク尿と最終的な腎不全を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "urinalysis", "renal_ultrasound"],
        "causes": "Caused by chronic hyperglycemia leading to progressive glomerular damage, mesangial expansion, and eventual renal failure.",
        "causes_ja": "デグーにおける糖尿病性腎症の原因: 慢性糖尿病による進行性の腎障害で、タンパク尿と最終的な腎不全を引き起こします。",
        "pathophysiology": "Progressive loss of functional nephrons impairs glomerular filtration, tubular reabsorption, and endocrine function. Uremic toxin accumulation and fluid-electrolyte imbalance lead to systemic complications.",
        "pathophysiology_ja": "糖尿病性腎症はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "Insulin therapy with dose titration based on glucose curves, dietary management with consistent high-fiber meals, regular blood glucose monitoring, and management of concurrent conditions.",
        "treatment_ja": "糖尿病性腎症はdeguでは非常に稀。報告例ではインスリン依存性で、プロジンク 0.5-1 IU/動物 SC q12h から開始、家庭での血糖モニタ（耳介穿刺、CGM試験的）と組み合わせる。低糖質・高繊維食。インスリン抵抗性をきたす副腎疾患・甲状腺疾患・肥満を除外。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "糖尿病性腎症の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Fair to good with dedicated owner compliance and proper insulin management. Uncontrolled diabetes leads to serious complications including ketoacidosis.",
        "prognosis_ja": "糖尿病性腎症の予後: 早期治療で予後良好。再発予防には食事管理と定期検査が重要。閉塞性疾患は緊急対応で予後改善。慢性腎疾患はステージにより予後が異なる。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Diabetic Foot Ulcer",
        "name_ja": "糖尿病性足潰瘍",
        "symptoms": {"swollen_feet", "foot_ulceration", "lameness", "slow_wound_healing"},
        "description": "Diabetic Foot Ulcer is an erosive lesion of tissue requiring treatment to promote healing and prevent complications.",
        "description_ja": "糖尿病性神経障害と循環障害による非治癒性足潰瘍。二次感染により複雑化することが多いです。",
        "urgency": "high",
        "recommended_tests": ["blood_glucose", "wound_culture", "foot_xray"],
        "causes": "Caused by diabetic neuropathy reducing sensation and diabetic vasculopathy impairing circulation, leading to non-healing foot wounds prone to secondary infection.",
        "causes_ja": "デグーにおける糖尿病性足潰瘍の原因: 糖尿病性神経障害と循環障害による非治癒性足潰瘍。二次感染により複雑化することが多いです。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "糖尿病性足潰瘍はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "Insulin therapy with dose titration based on glucose curves, dietary management with consistent high-fiber meals, regular blood glucose monitoring, and management of concurrent conditions.",
        "treatment_ja": "糖尿病性足潰瘍はdeguでは非常に稀。報告例ではインスリン依存性で、プロジンク 0.5-1 IU/動物 SC q12h から開始、家庭での血糖モニタ（耳介穿刺、CGM試験的）と組み合わせる。低糖質・高繊維食。インスリン抵抗性をきたす副腎疾患・甲状腺疾患・肥満を除外。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "糖尿病性足潰瘍の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Fair to good with dedicated owner compliance and proper insulin management. Uncontrolled diabetes leads to serious complications including ketoacidosis.",
        "prognosis_ja": "糖尿病性足潰瘍の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Dental Malocclusion - Molar (Acquired)",
        "name_ja": "不正咬合 - 臼歯（後天性）",
        "symptoms": {"appetite_loss", "drooling", "eye_discharge", "selective_eating", "weight_loss"},
        "description": "Dental Malocclusion - Molar (Acquired) is a dental condition affecting tooth structure, alignment, or oral health.",
        "description_ja": "適切な摩耗の不足による後天性臼歯過長とスパー形成。適切な研磨性食事を欠く飼育下デグーに非常に多いです。",
        "urgency": "high",
        "recommended_tests": ["oral_exam", "skull_xray", "dental_endoscopy"],
        "causes": "Caused by insufficient dietary abrasion from lack of long-stem hay and fibrous foods, leading to abnormal molar wear patterns and spur formation.",
        "causes_ja": "デグーにおける不正咬合 - 臼歯（後天性）の原因: 適切な摩耗の不足による後天性臼歯過長とスパー形成。適切な研磨性食事を欠く飼育下デグーに非常に多いです。",
        "pathophysiology": "Abnormal tooth growth or alignment creates points of pressure on opposing dental surfaces and oral soft tissues, leading to pain, mucosal ulceration, and secondary infection with progressive inability to eat.",
        "pathophysiology_ja": "不正咬合 - 臼歯（後天性）はデグーにおける歯科・口腔疾患である。歯の構造、配列、または支持組織の正常な機能が障害される。異常な歯の成長・摩耗パターンは不正咬合、歯根伸長、根尖膿瘍形成を引き起こしうる。歯周病は細菌バイオフィルムの蓄積、歯肉炎症、歯周付着の進行性喪失を伴う。歯科疾患による疼痛は食欲低下、選択的摂食、体重減少、流涎として現れることが多い。",
        "treatment": "Treatment includes dental trimming or filing under anesthesia, pain management, dietary modification to encourage natural wear, and regular dental monitoring.",
        "treatment_ja": "デグーにおける不正咬合 - 臼歯（後天性）の治療には鎮静または麻酔下での歯科検査が必要である。不正咬合は種と重症度に応じて歯のトリミング、研磨、抜歯が必要となる。根尖膿瘍には排膿、デブリードマン、全身性抗菌薬が必要である。歯周病治療にはスケーリング、研磨、重度罹患歯の抜歯を含む。種に適した鎮痛薬による疼痛管理が不可欠である。食事の調整により回復を促進し再発を予防する。",
        "prevention": "Prevention includes providing appropriate high-fiber diet to promote natural dental wear, regular dental examinations, and avoiding selective feeding.",
        "prevention_ja": "不正咬合 - 臼歯（後天性）の予防には自然な歯の摩耗を促進する適切な咀嚼材と食事、定期的な歯科検査、発生しつつある不正咬合の早期矯正、種に適した食物繊維の提供が含まれる。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "不正咬合 - 臼歯（後天性）の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Dental Malocclusion - Incisor (Congenital)",
        "name_ja": "不正咬合 - 切歯（先天性）",
        "symptoms": {"difficulty_eating", "drooling", "visible_tooth_overgrowth", "weight_loss"},
        "description": "Dental Malocclusion - Incisor (Congenital) is a dental condition affecting tooth structure, alignment, or oral health.",
        "description_ja": "先天性の切歯不整列で、正常な齧りを妨げ、定期的なトリミングが必要です。",
        "urgency": "moderate",
        "recommended_tests": ["dental_exam", "skull_xray", "physical_exam"],
        "causes": "Caused by congenital misalignment of the incisors due to genetic factors or developmental abnormalities, preventing normal gnawing and requiring periodic trimming.",
        "causes_ja": "デグーにおける不正咬合 - 切歯（先天性）の原因: 先天性の切歯不整列で、正常な齧りを妨げ、定期的なトリミングが必要です。",
        "pathophysiology": "Abnormal tooth growth or alignment creates points of pressure on opposing dental surfaces and oral soft tissues, leading to pain, mucosal ulceration, and secondary infection with progressive inability to eat.",
        "pathophysiology_ja": "不正咬合 - 切歯（先天性）はデグーにおける歯科・口腔疾患である。歯の構造、配列、または支持組織の正常な機能が障害される。異常な歯の成長・摩耗パターンは不正咬合、歯根伸長、根尖膿瘍形成を引き起こしうる。歯周病は細菌バイオフィルムの蓄積、歯肉炎症、歯周付着の進行性喪失を伴う。歯科疾患による疼痛は食欲低下、選択的摂食、体重減少、流涎として現れることが多い。",
        "treatment": "Treatment includes dental trimming or filing under anesthesia, pain management, dietary modification to encourage natural wear, and regular dental monitoring.",
        "treatment_ja": "デグーにおける不正咬合 - 切歯（先天性）の治療には鎮静または麻酔下での歯科検査が必要である。不正咬合は種と重症度に応じて歯のトリミング、研磨、抜歯が必要となる。根尖膿瘍には排膿、デブリードマン、全身性抗菌薬が必要である。歯周病治療にはスケーリング、研磨、重度罹患歯の抜歯を含む。種に適した鎮痛薬による疼痛管理が不可欠である。食事の調整により回復を促進し再発を予防する。",
        "prevention": "Prevention includes providing appropriate high-fiber diet to promote natural dental wear, regular dental examinations, and avoiding selective feeding.",
        "prevention_ja": "不正咬合 - 切歯（先天性）の予防には自然な歯の摩耗を促進する適切な咀嚼材と食事、定期的な歯科検査、発生しつつある不正咬合の早期矯正、種に適した食物繊維の提供が含まれる。",
        "prognosis": "Fair to good with regular dental management. Hereditary malocclusion requires lifelong monitoring and periodic correction.",
        "prognosis_ja": "不正咬合 - 切歯（先天性）の予後: 疾患の重症度による。軽度の先天性異常は手術で矯正可能。重度は長期管理またはQOL考慮。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"young"},
    },
    {
        "name": "Tooth Root Elongation",
        "name_ja": "歯根伸長",
        "symptoms": {"appetite_loss", "drooling", "epiphora", "jaw_swelling", "nasal_discharge"},
        "description": "Tooth Root Elongation is a dental condition affecting tooth structure, alignment, or oral health.",
        "description_ja": "歯根の根尖伸長で、鼻腔（上顎）または下顎を貫通します。",
        "urgency": "high",
        "recommended_tests": ["skull_xray", "ct_scan", "dental_exam"],
        "causes": "Caused by chronic dental malocclusion leading to apical elongation of tooth roots that may penetrate the nasal cavity (maxillary teeth) or mandible.",
        "causes_ja": "デグーにおける歯根伸長の原因: 歯根の根尖伸長で、鼻腔（上顎）または下顎を貫通します。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "歯根伸長はデグーにおける歯科・口腔疾患である。歯の構造、配列、または支持組織の正常な機能が障害される。異常な歯の成長・摩耗パターンは不正咬合、歯根伸長、根尖膿瘍形成を引き起こしうる。歯周病は細菌バイオフィルムの蓄積、歯肉炎症、歯周付着の進行性喪失を伴う。歯科疾患による疼痛は食欲低下、選択的摂食、体重減少、流涎として現れることが多い。",
        "treatment": "Skull radiographs for assessment. Burring of crowns under isoflurane. Syringe feed Critical Care. Meloxicam 0.2 mg/kg q24h. Progressive condition — requires long-term management.",
        "treatment_ja": "デグーにおける歯根伸長の治療には鎮静または麻酔下での歯科検査が必要である。不正咬合は種と重症度に応じて歯のトリミング、研磨、抜歯が必要となる。根尖膿瘍には排膿、デブリードマン、全身性抗菌薬が必要である。歯周病治療にはスケーリング、研磨、重度罹患歯の抜歯を含む。種に適した鎮痛薬による疼痛管理が不可欠である。食事の調整により回復を促進し再発を予防する。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "歯根伸長の予防には自然な歯の摩耗を促進する適切な咀嚼材と食事、定期的な歯科検査、発生しつつある不正咬合の早期矯正、種に適した食物繊維の提供が含まれる。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "歯根伸長の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Mandibular Abscess (Dental Origin)",
        "name_ja": "下顎膿瘍（歯原性）",
        "symptoms": {"appetite_loss", "draining_tract", "drooling", "jaw_swelling", "weight_loss"},
        "description": "Mandibular Abscess (Dental Origin) is a dental condition affecting tooth structure, alignment, or oral health.",
        "description_ja": "感染した歯根から発生する下顎の膿瘍。積極的な長期治療が必要です。",
        "urgency": "high",
        "recommended_tests": ["skull_xray", "culture_sensitivity", "ct_scan"],
        "causes": "Caused by bacterial infection spreading from diseased tooth roots into the mandibular bone, forming encapsulated abscesses requiring aggressive treatment.",
        "causes_ja": "デグーにおける下顎膿瘍（歯原性）の原因: 感染した歯根から発生する下顎の膿瘍。積極的な長期治療が必要です。",
        "pathophysiology": "Abnormal tooth growth or alignment creates points of pressure on opposing dental surfaces and oral soft tissues, leading to pain, mucosal ulceration, and secondary infection with progressive inability to eat.",
        "pathophysiology_ja": "下顎膿瘍（歯原性）はデグーにおける細菌感染症である。病原菌は付着因子を通じて組織にコロニーを形成し、毒素産生、酵素分泌、免疫回避戦略などの病原性メカニズムを介して侵入する。好中球浸潤、サイトカイン放出、補体活性化を含む炎症カスケードが生じる。組織損傷は細菌の直接作用と宿主の炎症反応の両方に起因する。菌種と宿主の免疫状態に応じて、膿瘍形成、敗血症、または慢性肉芽腫性炎症が発生しうる。",
        "treatment": "Surgical debridement and tooth extraction under isoflurane. Enrofloxacin 5-10 mg/kg PO q12h x 14-21d. Meloxicam 0.2 mg/kg PO q24h. Skull radiographs. Culture abscess material.",
        "treatment_ja": "デグーにおける下顎膿瘍（歯原性）の治療には、可能であれば培養感受性試験に基づく標的抗菌薬療法が必要である。結果待ちの間は経験的広域抗菌薬を開始する。抗菌薬治療期間は感染の排除と耐性予防に十分な期間とする。膿瘍や壊死組織には外科的排膿またはデブリードマンが必要な場合がある。支持療法として輸液、鎮痛薬、抗炎症薬、栄養サポートを行う。",
        "prevention": "Prevention includes providing appropriate high-fiber diet to promote natural dental wear, regular dental examinations, and avoiding selective feeding.",
        "prevention_ja": "下顎膿瘍（歯原性）の予防には適切な衛生管理・消毒、利用可能なワクチン接種、創傷の迅速な処置、ストレス軽減、適切な換気、感染動物の隔離が含まれる。",
        "prognosis": "Generally good with appropriate antimicrobial therapy and source control. Chronic or deep-seated infections may require prolonged treatment. Immunocompromised patients have a more guarded prognosis.",
        "prognosis_ja": "下顎膿瘍（歯原性）の予後: 多くの皮膚疾患は適切な治療で予後良好。感染性疾患は抗菌薬/抗真菌薬で治癒可能。アレルギー性は長期管理が必要。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Enamel Hypoplasia",
        "name_ja": "エナメル質形成不全",
        "symptoms": {"difficulty_eating", "drooling", "tooth_discoloration", "tooth_fracture"},
        "description": "Enamel Hypoplasia is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "エナメル質形成の発達障害で、骨折しやすい弱く変色した歯になります。",
        "urgency": "moderate",
        "recommended_tests": ["dental_exam", "skull_xray", "physical_exam"],
        "causes": "Caused by developmental disturbance of ameloblast function during tooth formation, resulting from nutritional deficiency, infection, or genetic factors.",
        "causes_ja": "デグーにおけるエナメル質形成不全の原因: エナメル質形成の発達障害で、骨折しやすい弱く変色した歯になります。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "エナメル質形成不全はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "Degus have open-rooted (elodont) teeth that grow continuously — enamel hypoplasia affects "
        "tooth integrity and wear patterns. DENTAL MANAGEMENT: Regular dental examination under "
        "isoflurane anesthesia (chamber induction 3-4%, nose cone maintenance 1.5-2.5%, body "
        "temperature maintenance on 37°C heated pad — degus are prone to hypothermia at <200g). "
        "Trim overgrown or maloccluded teeth with high-speed dental burr (NEVER use nail clippers "
        "— causes longitudinal fractures). File sharp enamel points causing oral trauma. DIETARY "
        "SUPPORT: Unlimited timothy hay — essential for continuous tooth wear. Providing hard "
        "chewing materials (untreated wood blocks, pumice stone, hay cubes) to promote natural "
        "wear. If unable to eat due to dental pain: syringe feeding with Critical Care for "
        "Herbivores (Oxbow) 50-80 mL/kg/day. PAIN MANAGEMENT: Meloxicam 1-2 mg/kg PO/SC q24h. "
        "Buprenorphine 0.05-0.1 mg/kg SC q8-12h for acute dental pain. INFECTION PREVENTION: "
        "If fractured teeth expose pulp — antibiotics: enrofloxacin 5-10 mg/kg PO q12h × 7-14 "
        "days (oral β-lactams CONTRAINDICATED). NUTRITIONAL CORRECTION: Ensure adequate calcium "
        "(0.6-1.0% of diet), phosphorus (correct Ca:P ratio 1.5-2:1), and vitamin D for proper "
        "enamel mineralization. Affected teeth may need periodic trimming every 4-8 weeks. "
        "MONITORING: Regular oral exams every 2-3 months. Watch for weight loss, drooling, "
        "food dropping, teeth grinding (bruxism) as signs of dental pain. "
        "References: Crossley (2003) Vet Clin Exot Anim; Jekl & Redrobe (2013) BSAVA Manual.",
        "treatment_ja": "デグーは常生歯（開放歯根）を持ち、歯は継続的に伸長 — エナメル質形成不全は歯の完全性と"
        "摩耗パターンに影響。【歯科管理】イソフルラン麻酔下での定期歯科検査（チャンバー導入"
        "3-4%、ノーズコーン維持1.5-2.5%、37℃加温パッドで体温維持）。過成長/不正咬合歯は"
        "高速歯科バーでトリミング（爪切りは絶対に使用しない — 縦断骨折の原因）。口腔外傷を"
        "引き起こす鋭いエナメルポイントを研磨。【食事支持】チモシー牧草の無制限提供 — 継続的な"
        "歯の摩耗に不可欠。硬いかじり材（無処理木材、軽石、牧草キューブ）。歯痛で食事困難な"
        "場合: クリティカルケアのシリンジ給餌。【疼痛管理】メロキシカム1-2 mg/kg PO/SC q24h。"
        "ブプレノルフィン0.05-0.1 mg/kg SC q8-12h。【感染予防】歯牙破折で歯髄露出時: "
        "エンロフロキサシン5-10 mg/kg PO q12h × 7-14日（経口βラクタム系は禁忌）。"
        "【栄養是正】適切なCa（0.6-1.0%）、P（Ca:P比1.5-2:1）、VitDの確保。4-8週ごとの"
        "定期トリミングが必要な場合あり。",
        "prevention": "Ensure timothy hay-based diet for continuous natural tooth wear. Provide appropriate "
        "chewing materials (untreated wood, pumice, hay cubes). Adequate dietary calcium, "
        "phosphorus, and vitamin D for proper enamel development. Avoid breeding from animals "
        "with known dental abnormalities (genetic component). Regular oral examinations every "
        "3-6 months — early detection of malocclusion allows timely intervention. "
        "Reference: Crossley (2003) Vet Clin Exot Anim; Jekl & Redrobe (2013).",
        "prevention_ja": "チモシー牧草ベースの食事で継続的な自然摩耗を確保。適切なかじり材の提供。"
        "エナメル質発育のための適切なCa/P/VitD。既知の歯科異常を持つ個体の繁殖回避"
        "（遺伝的要素）。3-6ヶ月ごとの定期口腔検査。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "エナメル質形成不全の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Bumblefoot - Advanced (Osteomyelitis)",
        "name_ja": "趾瘤症 - 進行型（骨髄炎）",
        "symptoms": {"bone_infection", "foot_ulceration", "lameness", "reluctance_to_move", "severe_foot_swelling"},
        "description": "Bumblefoot - Advanced (Osteomyelitis) is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "骨に及ぶ深部感染を伴う進行した趾瘤症で骨髄炎を引き起こします。指切断が必要な場合があります。",
        "urgency": "high",
        "recommended_tests": ["foot_xray", "culture_sensitivity", "physical_exam"],
        "causes": "Caused by progression of pododermatitis with deep bacterial infection extending into bone, resulting in osteomyelitis. Wire-mesh flooring and obesity are predisposing factors.",
        "causes_ja": "デグーにおける趾瘤症 - 進行型（骨髄炎）の原因: 骨に及ぶ深部感染を伴う進行した趾瘤症で骨髄炎を引き起こします。指切断が必要な場合があります。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "趾瘤症 - 進行型（骨髄炎）はデグーにおける皮膚疾患である。表皮バリア、真皮炎症、または付属器機能の障害を伴う。バリア機能の低下により経表皮水分喪失、アレルゲン浸透、微生物コロニー形成が促進される。炎症メディエーター（ヒスタミン、プロスタグランジン、サイトカイン）が掻痒、紅斑、二次的な擦過傷を駆動する。慢性疾患では表皮過形成、苔癬化、色素沈着、線維化が生じる。",
        "treatment": "Surgical debridement under isoflurane. Enrofloxacin 5-10 mg/kg PO q12h x 21-28d. Meloxicam 0.2 mg/kg PO q24h. Bandage changes q48h. Improve substrate (soft bedding). Prognosis guarded.",
        "treatment_ja": "デグーにおける趾瘤症 - 進行型（骨髄炎）の治療: 外科的介入（趾瘤症 - 進行型（骨髄炎）に対する適切な術式）。術前安定化: 輸液療法、メロキシカム1-2mg/kg PO/SC q24h（疼痛管理）。周術期抗菌薬: エンロフロキサシン5-10mg/kg PO q12h（経口βラクタム禁忌）。栄養サポート、環境温度管理、定期的モニタリング。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "趾瘤症 - 進行型（骨髄炎）の予防: 定期的な健康診断。適切な栄養管理。ストレスの軽減。清潔な飼育環境の維持。異常の早期発見・早期受診。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "趾瘤症 - 進行型（骨髄炎）の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Tail Degloving - Complete",
        "name_ja": "尾部皮膚剥離 - 完全型",
        "symptoms": {"bleeding", "exposed_tail_bone", "pain", "tail_necrosis"},
        "description": "Tail Degloving - Complete is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "尾の皮膚が完全に剥離し椎骨が露出。デグーの尾は防衛機構として非常にもろく容易に剥離します。",
        "urgency": "high",
        "recommended_tests": ["tail_xray", "physical_exam", "wound_assessment"],
        "causes": "Caused by grasping the tail during handling or entrapment. The degu tail skin is extremely fragile as a predator-escape adaptation and does not regenerate.",
        "causes_ja": "デグーにおける尾部皮膚剥離 - 完全型の原因: 尾の皮膚が完全に剥離し椎骨が露出。デグーの尾は防衛機構として非常にもろく容易に剥離します。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "尾部皮膚剥離 - 完全型はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "Tail amputation at next viable segment under isoflurane. Enrofloxacin 5-10 mg/kg PO q12h x 7d. Meloxicam 0.2 mg/kg SC. Topical silver sulfadiazine. NEVER handle degus by tail.",
        "treatment_ja": "デグーにおける尾部皮膚剥離 - 完全型の治療は安定化、疼痛管理、創傷ケアを優先する。生命を脅かす損傷を最初に評価・対処する（気道、呼吸、循環）。種に適した鎮痛薬（NSAIDs、オピオイド、局所麻酔薬）による鎮痛が不可欠である。創傷を洗浄・デブリードマンし、一次閉鎖、二次治癒、再建手術を適宜行う。汚染創には広域抗菌薬を使用する。骨折には副子固定または外科的固定を行う。遅発性合併症をモニタリングする。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "尾部皮膚剥離 - 完全型の予防には安全で種に適した飼育環境の整備、鋭利物・危険物の除去、適切な取り扱い技術、他の動物との接触時の監視、温度管理、落下防止策が含まれる。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "尾部皮膚剥離 - 完全型の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Tail Amputation Stump Infection",
        "name_ja": "尾切断部感染",
        "symptoms": {"discharge", "fever", "lethargy", "swelling_at_tail_stump"},
        "description": "Tail Amputation Stump Infection is a bacterial infection that causes systemic or localized inflammatory disease requiring prompt antimicrobial therapy.",
        "description_ja": "皮膚剥離損傷または外科的切断後の尾断端の感染で、抗生物質療法が必要です。",
        "urgency": "moderate",
        "recommended_tests": ["wound_culture", "physical_exam", "tail_xray"],
        "causes": "Caused by bacterial contamination of the exposed tail stump following degloving injury or surgical amputation, requiring antibiotic therapy.",
        "causes_ja": "デグーにおける尾切断部感染の原因: 皮膚剥離損傷または外科的切断後の尾断端の感染で、抗生物質療法が必要です。",
        "pathophysiology": "Bacterial organisms invade host tissues, triggering inflammatory cascades with neutrophil recruitment, cytokine release, and potential tissue necrosis. Systemic spread may lead to bacteremia and multi-organ dysfunction.",
        "pathophysiology_ja": "尾切断部感染はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "Treatment includes appropriate antimicrobial therapy based on culture and sensitivity, supportive care, fluid therapy, and surgical drainage if indicated. Monitor for treatment response and complications.",
        "treatment_ja": "デグーにおける尾切断部感染の治療は安定化、疼痛管理、創傷ケアを優先する。生命を脅かす損傷を最初に評価・対処する（気道、呼吸、循環）。種に適した鎮痛薬（NSAIDs、オピオイド、局所麻酔薬）による鎮痛が不可欠である。創傷を洗浄・デブリードマンし、一次閉鎖、二次治癒、再建手術を適宜行う。汚染創には広域抗菌薬を使用する。骨折には副子固定または外科的固定を行う。遅発性合併症をモニタリングする。",
        "prevention": "Prevention includes maintaining proper hygiene, appropriate husbandry, stress reduction, quarantine of new animals, and prompt treatment of wounds or primary conditions.",
        "prevention_ja": "尾切断部感染の予防には安全で種に適した飼育環境の整備、鋭利物・危険物の除去、適切な取り扱い技術、他の動物との接触時の監視、温度管理、落下防止策が含まれる。",
        "prognosis": "Good with appropriate antimicrobial therapy. Most infections resolve with proper treatment. Chronic or recurrent cases may require longer management.",
        "prognosis_ja": "尾切断部感染の予後: 適切な抗菌薬療法で多くが治癒可能。慢性・深在性感染は長期治療が必要。敗血症は予後要注意。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Fur Chewing (Barbering) - Severe",
        "name_ja": "毛噛み（バーバリング）- 重症型",
        "symptoms": {"extensive_hair_loss", "rough_coat", "skin_lesions", "stress_signs"},
        "description": "Fur Chewing (Barbering) - Severe is a dermatological condition affecting the skin, coat, or integumentary system.",
        "description_ja": "広範な脱毛を引き起こす重度の自己または社会的バーバリング。ストレス、退屈、栄養欠乏を示す可能性があります。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam", "behavioral_assessment", "diet_review"],
        "treatment": "Severe barbering in degus indicates significant behavioral distress or underlying medical condition "
        "requiring comprehensive intervention. MEDICAL RULE-OUT (FIRST): Skin scraping for mites "
        "(Demodex, Sarcoptes). Dermatophyte culture (DTM) — Trichophyton mentagrophytes most common "
        "in degus. Skin biopsy if pruritic lesions present. Blood glucose (diabetes-related "
        "dermatopathy). Diet review for nutritional deficiencies. ENVIRONMENTAL OVERHAUL: Larger "
        "cage (minimum 80×50×100 cm), multiple levels with ramps, ≥2 running wheels (solid surface, "
        "≥25 cm diameter), dust bath (chinchilla sand) 2-3× weekly, foraging enrichment (scatter "
        "timothy hay/herbs), multiple hiding spots, chew toys. SOCIAL MANAGEMENT: Degus are "
        "obligately social — single housing causes severe stress. Minimum pair, ideally 3-4 "
        "same-sex group. If allo-barbering: identify dominant aggressor via video observation, "
        "temporary separation with visual/olfactory contact, reintroduce in neutral territory. "
        "PHARMACOLOGICAL (LAST RESORT, limited evidence): Fluoxetine 1-2 mg/kg PO q24h "
        "(extrapolated from rodent models — monitor for anorexia). WOUND CARE for excoriated "
        "areas: Chlorhexidine 0.05% topical. If secondary infection: enrofloxacin 5-10 mg/kg "
        "PO q12h × 7-14 days (oral β-lactams CONTRAINDICATED). Elizabethan collar rarely "
        "practical in degus due to small size. References: Jekl & Redrobe (2013) BSAVA Manual; "
        "Quesenberry & Carpenter (2012).",
        "treatment_ja": "重度のバーバリングは著しい行動学的ストレスまたは基礎疾患を示唆し、包括的介入が必要。"
        "【医学的除外（最優先）】皮膚掻爬でダニ検査。皮膚糸状菌培養（DTM）。血糖（糖尿病関連"
        "皮膚症）。食事レビュー。【環境の全面改善】大型ケージ（最低80×50×100cm）、スロープ付き"
        "多段構造、回し車≥2台、砂浴び週2-3回、フォレージング、複数の隠れ場所、かじり木。"
        "【社会管理】デグーは社会性が必須 — 単独飼育は重度ストレス。最低ペア、理想は3-4頭の"
        "同性グループ。他個体バーバリング: ビデオ観察で優位個体を特定、一時隔離。【薬物療法"
        "（最終手段）】フルオキセチン1-2 mg/kg PO q24h（齧歯類モデルからの外挿）。"
        "【創傷ケア】擦過部位のクロルヘキシジン0.05%。二次感染: エンロフロキサシン"
        "5-10 mg/kg PO q12h × 7-14日（経口βラクタム系禁忌）。",
        "prognosis": "Guarded to fair depending on chronicity and underlying cause. Recent-onset barbering with "
        "identifiable stressor has good prognosis after environmental correction (hair regrowth in "
        "4-8 weeks). Chronic self-barbering (>6 months) may become a stereotypic behavior pattern "
        "that persists even after stressor removal. Allo-barbering from dominant cage-mates may "
        "require permanent social restructuring. Secondary skin infections are manageable but may "
        "recur if barbering continues. No impact on lifespan unless severe self-mutilation occurs.",
        "prognosis_ja": "慢性度と原因により予後慎重〜やや良好。最近発症でストレス源が特定できれば環境是正後に"
        "予後良好（4-8週間で毛の再生）。慢性自己バーバリング（>6ヶ月）はストレス源除去後も"
        "持続する常同行動パターンとなりうる。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Sarcoptic Mange",
        "name_ja": "疥癬",
        "symptoms": {"hair_loss", "intense_itching", "skin_crusting", "skin_thickening", "weight_loss"},
        "description": "Sarcoptic Mange is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "ヒゼンダニの寄生で、重度の掻痒、痂皮形成、二次感染を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["skin_scraping", "microscopy", "physical_exam"],
        "causes": "Sarcoptes scabiei mite infestation causing severe pruritus, crusting, and secondary infection.",
        "causes_ja": "デグーにおける疥癬の原因: ヒゼンダニの寄生で、重度の掻痒、痂皮形成、二次感染を引き起こします。",
        "pathophysiology": "Sarcoptic Mange is a parasitic condition. Sarcoptes scabiei mite infestation causing severe pruritus, crusting, and secondary infection. The parasite establishes infection through ingestion, percutaneous penetration, or vector-mediated transmission. It exploits host resources for nutrition and reproduction while evading immune defenses through antigenic variation, immunomodulation, or intracellular sequestration. Tissue damage results from direct parasitic feeding, mechanical disruption, toxic metabolic byproducts, and the host's inflammatory and immune responses. Heavy parasite burdens can lead to anemia, malnutrition, organ dysfunction, and secondary infections.",
        "pathophysiology_ja": "疥癬はデグーにおける寄生虫疾患である。寄生虫は経口摂取、経皮的侵入、またはベクター媒介伝播を通じて感染を確立する。抗原変異、免疫調節、細胞内隔離により宿主の免疫防御を回避しながら、宿主の栄養と資源を利用して増殖する。組織損傷は寄生虫の直接的な摂食、機械的破壊、有毒代謝副産物、宿主の炎症・免疫応答に起因する。重度の寄生虫感染は貧血、栄養失調、臓器機能障害、二次感染を引き起こしうる。",
        "treatment": "Ivermectin 0.2-0.4 mg/kg SC q7-14d x 3-4 treatments. Selamectin topical as alternative. Treat all contacts. Environmental cleaning.",
        "treatment_ja": "デグーにおける疥癬の治療には、同定された寄生虫に応じた適切な駆虫薬が必要である。一部の駆虫薬は特定の種に有毒であるため、種に適した用量設定が重要である。全てのライフステージを排除するため複数回投与が必要な場合がある。環境消毒と接触動物の治療で再感染を防止する。貧血、脱水、栄養失調などの二次的合併症に対する支持療法を行う。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "疥癬の予防には定期的な予防駆虫、環境衛生と糞便除去、新規動物の隔離・検査、ベクター防除、中間宿主や汚染環境への曝露回避が含まれる。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "疥癬の予後: 多くの皮膚疾患は適切な治療で予後良好。感染性疾患は抗菌薬/抗真菌薬で治癒可能。アレルギー性は長期管理が必要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Lice Infestation",
        "name_ja": "シラミ寄生症",
        "symptoms": {"hair_loss", "pruritus", "restlessness", "visible_lice"},
        "description": "Lice Infestation is a parasitic condition that causes clinical signs ranging from subclinical to severe systemic disease.",
        "description_ja": "種特異的なシラミの寄生で、掻痒と被毛状態の悪化を引き起こします。",
        "urgency": "low",
        "recommended_tests": ["coat_exam", "microscopy", "physical_exam"],
        "causes": "Caused by species-specific louse infestation transmitted through direct contact with infested animals or contaminated bedding.",
        "causes_ja": "デグーにおけるシラミ寄生症の原因: 種特異的なシラミの寄生で、掻痒と被毛状態の悪化を引き起こします。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "シラミ寄生症はデグーにおける皮膚疾患である。表皮バリア、真皮炎症、または付属器機能の障害を伴う。バリア機能の低下により経表皮水分喪失、アレルゲン浸透、微生物コロニー形成が促進される。炎症メディエーター（ヒスタミン、プロスタグランジン、サイトカイン）が掻痒、紅斑、二次的な擦過傷を駆動する。慢性疾患では表皮過形成、苔癬化、色素沈着、線維化が生じる。",
        "treatment": "Appropriate antiparasitic medication, environmental cleaning, and repeat treatments as needed to address all lifecycle stages.",
        "treatment_ja": "デグーにおけるシラミ寄生症の治療: 駆虫薬: イベルメクチン0.2-0.4mg/kg SC、2週間間隔で2-3回投与（ライフサイクル全段階を対応）。代替: セラメクチン（レボリューション）15mg/kg 頸背部滴下、月1回×3回。環境消毒: ケージ・備品の熱水消毒、床材の全交換（週1回×4週間）。掻痒がひどい場合: メロキシカム1-2mg/kg PO/SC q24h（3-5日間）。二次的な皮膚感染がある場合: エンロフロキサシン5-10mg/kg PO q12h。同居動物も同時治療。",
        "prevention": "Prevention includes regular parasite screening and treatment, environmental sanitation, quarantine of new animals, and avoiding overcrowding.",
        "prevention_ja": "シラミ寄生症の予防: 定期的な健康診断。適切な栄養管理。ストレスの軽減。清潔な飼育環境の維持。異常の早期発見・早期受診。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "シラミ寄生症の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Trichophyton mentagrophytes (Ringworm) - Extensive",
        "name_ja": "白癬菌感染 - 広範囲型",
        "symptoms": {"circular_hair_loss", "crusty_skin", "skin_scaling", "widespread_lesions"},
        "description": "Trichophyton mentagrophytes (Ringworm) - Extensive is a fungal infection that can affect skin, respiratory, or systemic organs.",
        "description_ja": "体の広い範囲に及ぶ広範な皮膚糸状菌感染。ヒトへの人獣共通感染症です。",
        "urgency": "moderate",
        "recommended_tests": ["fungal_culture", "wood_lamp", "skin_scraping"],
        "causes": "Caused by extensive dermatophyte infection with Trichophyton mentagrophytes, a zoonotic fungal pathogen transmitted by direct contact or fomites.",
        "causes_ja": "デグーにおける白癬菌感染 - 広範囲型の原因: 体の広い範囲に及ぶ広範な皮膚糸状菌感染。ヒトへの人獣共通感染症です。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "白癬菌感染 - 広範囲型はデグーにおける真菌感染症である。真菌は胞子吸入、直接接種、または粘膜コロニー形成を通じて感染を確立する。菌糸または酵母形態が酵素分解と機械的圧力により組織に侵入し、肉芽腫性炎症反応を惹起する。免疫不全個体は特に感受性が高い。感染は局所にとどまるか、血行性に遠隔臓器へ播種される可能性がある。慢性感染は線維化、組織リモデリング、進行性臓器機能障害を引き起こしうる。",
        "treatment": "Treatment includes systemic antifungal therapy (azoles or amphotericin B), topical antifungal agents, environmental decontamination, and supportive care. Monitor hepatic function during prolonged therapy.",
        "treatment_ja": "degu皮膚糸状菌症: 局所2%ミコナゾールクリーム q12h、全身でイトラコナゾール 5-10 mg/kg PO q24h × 4-6週またはテルビナフィン 20-40 mg/kg PO q24h × 4-6週。肝酵素q2週モニタ。長毛種は毛刈り。 環境消毒（次亜塩素酸1:10）、寝床完全交換。⚠人獣共通感染症。 支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "白癬菌感染 - 広範囲型の予防には適切な環境湿度・温度の維持、良好な換気、過密の回避、定期的な清掃・消毒、罹患個体の隔離、適切な栄養による免疫機能の維持が含まれる。",
        "prognosis": "Good with appropriate antifungal therapy, though treatment course may be prolonged. Environmental recontamination can cause recurrence.",
        "prognosis_ja": "白癬菌感染 - 広範囲型の予後: 多くの皮膚疾患は適切な治療で予後良好。感染性疾患は抗菌薬/抗真菌薬で治癒可能。アレルギー性は長期管理が必要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Bacterial Pneumonia (Acute)",
        "name_ja": "細菌性肺炎（急性）",
        "symptoms": {"appetite_loss", "fever", "lethargy", "nasal_discharge", "respiratory_distress"},
        "description": "Bacterial Pneumonia (Acute) is a bacterial infection that causes systemic or localized inflammatory disease requiring prompt antimicrobial therapy.",
        "description_ja": "ストレス、過密飼育、ウイルス性上気道感染に続発することが多い急性細菌性肺感染です。",
        "urgency": "high",
        "recommended_tests": ["chest_xray", "tracheal_wash", "culture_sensitivity"],
        "causes": "Caused by bacterial lung infection, often secondary to stress, overcrowding, poor ventilation, or viral upper respiratory infection compromising mucosal defenses.",
        "causes_ja": "デグーにおける細菌性肺炎（急性）の原因: ストレス、過密飼育、ウイルス性上気道感染に続発することが多い急性細菌性肺感染です。",
        "pathophysiology": "Bacterial organisms invade host tissues, triggering inflammatory cascades with neutrophil recruitment, cytokine release, and potential tissue necrosis. Systemic spread may lead to bacteremia and multi-organ dysfunction.",
        "pathophysiology_ja": "細菌性肺炎（急性）はデグーにおけるウイルス感染症である。ウイルスは特定の受容体を介して宿主細胞に侵入し、細胞内機構を利用して複製する。直接的な細胞変性効果（細胞溶解、アポトーシス、標的臓器の組織壊死）を引き起こす。自然免疫（インターフェロン、NK細胞）および適応免疫（抗体、細胞性免疫）の宿主免疫応答が免疫病理に寄与することがある。ウイルス血症により病原体が複数の臓器系に播種される可能性があり、免疫抑制により二次的な細菌・真菌感染のリスクが高まる。",
        "treatment": "Enrofloxacin 5-10 mg/kg PO/SC q12h x 14-21d. Nebulization q8-12h. SC fluids. Keep at 18-22°C. Oxygen supplementation. Prognosis guarded.",
        "treatment_ja": "培養感受性に基づく抗菌薬療法：エンロフロキサシン5-10 mg/kg PO q12hまたはトリメトプリム-スルファ15-30 mg/kg PO q12h。輸液（温生理食塩水SC）。メロキシカム0.2-1 mg/kg PO q24hで疼痛管理。シリンジによる強制給餌。膿瘍の場合は外科的排膿・洗浄。",
        "prevention": "Prevention includes maintaining proper hygiene, appropriate husbandry, stress reduction, quarantine of new animals, and prompt treatment of wounds or primary conditions.",
        "prevention_ja": "細菌性肺炎（急性）の予防にはワクチン接種（利用可能な場合）、新規・病気動物の隔離、厳格なバイオセキュリティ対策、適切な消毒プロトコル、既知のキャリアや汚染環境との接触回避が含まれる。",
        "prognosis": "Generally good with appropriate antimicrobial therapy and source control. Chronic or deep-seated infections may require prolonged treatment. Immunocompromised patients have a more guarded prognosis.",
        "prognosis_ja": "細菌性肺炎（急性）の予後: 軽度の上部気道感染は治療に良好に反応。肺炎は早期治療で予後改善。慢性呼吸器疾患は長期管理が必要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Mycoplasma Infection",
        "name_ja": "マイコプラズマ感染症",
        "symptoms": {"chronic_sneezing", "conjunctivitis", "nasal_discharge", "respiratory_distress"},
        "description": "Mycoplasma Infection is a bacterial infection that causes systemic or localized inflammatory disease requiring prompt antimicrobial therapy.",
        "description_ja": "マイコプラズマ・プルモニスによる慢性呼吸器感染で、持続的な鼻炎と肺炎の可能性があります。",
        "urgency": "moderate",
        "recommended_tests": ["pcr_testing", "chest_xray", "nasal_swab"],
        "causes": "Caused by Mycoplasma pulmonis infection transmitted via aerosol or direct contact, causing chronic respiratory disease with persistent rhinitis and potential pneumonia.",
        "causes_ja": "デグーにおけるマイコプラズマ感染症の原因: マイコプラズマ・プルモニスによる慢性呼吸器感染で、持続的な鼻炎と肺炎の可能性があります。",
        "pathophysiology": "Bacterial organisms invade host tissues, triggering inflammatory cascades with neutrophil recruitment, cytokine release, and potential tissue necrosis. Systemic spread may lead to bacteremia and multi-organ dysfunction.",
        "pathophysiology_ja": "マイコプラズマ感染症はデグーにおける細菌感染症である。病原菌は付着因子を通じて組織にコロニーを形成し、毒素産生、酵素分泌、免疫回避戦略などの病原性メカニズムを介して侵入する。好中球浸潤、サイトカイン放出、補体活性化を含む炎症カスケードが生じる。組織損傷は細菌の直接作用と宿主の炎症反応の両方に起因する。菌種と宿主の免疫状態に応じて、膿瘍形成、敗血症、または慢性肉芽腫性炎症が発生しうる。",
        "treatment": "Antimicrobial therapy based on culture and sensitivity, wound care or drainage as needed, pain management, and monitoring for resolution.",
        "treatment_ja": "デグーにおけるマイコプラズマ感染症の治療には、可能であれば培養感受性試験に基づく標的抗菌薬療法が必要である。結果待ちの間は経験的広域抗菌薬を開始する。抗菌薬治療期間は感染の排除と耐性予防に十分な期間とする。膿瘍や壊死組織には外科的排膿またはデブリードマンが必要な場合がある。支持療法として輸液、鎮痛薬、抗炎症薬、栄養サポートを行う。",
        "prevention": "Prevention includes maintaining proper hygiene, appropriate husbandry, stress reduction, quarantine of new animals, and prompt treatment of wounds or primary conditions.",
        "prevention_ja": "マイコプラズマ感染症の予防には適切な衛生管理・消毒、利用可能なワクチン接種、創傷の迅速な処置、ストレス軽減、適切な換気、感染動物の隔離が含まれる。",
        "prognosis": "Good with appropriate antimicrobial therapy. Most infections resolve with proper treatment. Chronic or recurrent cases may require longer management.",
        "prognosis_ja": "マイコプラズマ感染症の予後: 適切な抗菌薬療法で多くが治癒可能。慢性・深在性感染は長期治療が必要。敗血症は予後要注意。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Bordetella Pneumonia",
        "name_ja": "ボルデテラ肺炎",
        "symptoms": {"coughing", "fever", "lethargy", "nasal_discharge", "respiratory_distress"},
        "description": "Bordetella Pneumonia is a respiratory condition affecting the airways or lungs, causing breathing difficulty.",
        "description_ja": "ボルデテラ・ブロンキセプティカによる重症肺炎で、若齢や免疫不全のデグーに致死的になり得ます。",
        "urgency": "high",
        "recommended_tests": ["chest_xray", "tracheal_wash", "culture_sensitivity"],
        "causes": "Caused by Bordetella bronchiseptica infection, producing severe pneumonia especially in young or immunocompromised degus. Transmitted via aerosol from infected animals.",
        "causes_ja": "デグーにおけるボルデテラ肺炎の原因: ボルデテラ・ブロンキセプティカによる重症肺炎で、若齢や免疫不全のデグーに致死的になり得ます。",
        "pathophysiology": "Inflammation and exudate accumulation in airways or alveoli impair gas exchange, leading to hypoxemia. Mucosal damage reduces clearance mechanisms, promoting secondary infection.",
        "pathophysiology_ja": "ボルデテラ肺炎はデグーにおける細菌感染症である。病原菌は付着因子を通じて組織にコロニーを形成し、毒素産生、酵素分泌、免疫回避戦略などの病原性メカニズムを介して侵入する。好中球浸潤、サイトカイン放出、補体活性化を含む炎症カスケードが生じる。組織損傷は細菌の直接作用と宿主の炎症反応の両方に起因する。菌種と宿主の免疫状態に応じて、膿瘍形成、敗血症、または慢性肉芽腫性炎症が発生しうる。",
        "treatment": "Enrofloxacin 5-10 mg/kg PO q12h + Doxycycline 5 mg/kg PO q12h x 14d. Nebulization. SC fluids. Isolate from guinea pigs (carriers).",
        "treatment_ja": "デグーにおけるボルデテラ肺炎の治療には、可能であれば培養感受性試験に基づく標的抗菌薬療法が必要である。結果待ちの間は経験的広域抗菌薬を開始する。抗菌薬治療期間は感染の排除と耐性予防に十分な期間とする。膿瘍や壊死組織には外科的排膿またはデブリードマンが必要な場合がある。支持療法として輸液、鎮痛薬、抗炎症薬、栄養サポートを行う。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "ボルデテラ肺炎の予防には適切な衛生管理・消毒、利用可能なワクチン接種、創傷の迅速な処置、ストレス軽減、適切な換気、感染動物の隔離が含まれる。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "ボルデテラ肺炎の予後: 軽度の上部気道感染は治療に良好に反応。肺炎は早期治療で予後改善。慢性呼吸器疾患は長期管理が必要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Clostridial Enteritis",
        "name_ja": "クロストリジウム腸炎",
        "symptoms": {"abdominal_distension", "dehydration", "diarrhea", "lethargy", "sudden_death"},
        "description": "Clostridial Enteritis is a gastrointestinal condition affecting digestive function and nutrient absorption.",
        "description_ja": "クロストリジウム属菌による毒素介在性腸炎で、抗生物質使用や食事変更に続発することが多いです。",
        "urgency": "emergency",
        "recommended_tests": ["fecal_culture", "fecal_toxin_assay", "blood_chemistry"],
        "causes": "Caused by toxin-producing Clostridium spp. overgrowth in the cecum, often triggered by antibiotic use, abrupt dietary changes, or stress disrupting normal gut flora.",
        "causes_ja": "デグーにおけるクロストリジウム腸炎の原因: クロストリジウム属菌による毒素介在性腸炎で、抗生物質使用や食事変更に続発することが多いです。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "クロストリジウム腸炎は抗菌薬投与や急激な食事変化による腸内細菌叢の撹乱を契機に、Clostridium 属菌（C. perfringens、C. difficile、C. spiroforme 等）が異常増殖し、外毒素（toxin A/B、α・ι・ε毒素など）を産生することで発症する。毒素は腸上皮細胞を傷害して粘膜壊死・透過性亢進・体液漏出を引き起こし、重度の下痢・腸毒素血症・毒素性ショックへ進展する。草食小動物では特に急速に致死的となる。",
        "treatment": "EMERGENCY: Metronidazole 20 mg/kg PO q12h. SC fluids aggressively. Syringe feed. Probiotic. NEVER use penicillins orally (hindgut fermenter). Prognosis guarded.",
        "treatment_ja": "デグーにおけるクロストリジウム感染症: ① 第一選択: メトロニダゾール 15-25 mg/kg PO q12h × 5-10日 （神経毒性に注意、長期投与は避ける）、または アモキシシリン 11-22 mg/kg PO q12h（C. perfringens）。② C. difficile: バンコマイシン 10 mg/kg PO q8h × 7-10日（耐性例）。③ 重症腸毒血症: 抗毒素血清（入手可能な場合）、輸液・電解質補正、嫌気性ショック対応。④ 食事性管理: 高繊維食、急激な食変えを避け、プロバイオティクスで腸内細菌叢回復。⑤ 草食動物（ウサギ・モルモット）はC. difficile腸炎リスクが極めて高い—ペニシリン系・セファロスポリン系経口禁忌。⑥ 環境芽胞対策: 次亜塩素酸1:10で消毒、乾燥環境維持。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "クロストリジウム腸炎の予防には適切な衛生管理・消毒、利用可能なワクチン接種、創傷の迅速な処置、ストレス軽減、適切な換気、感染動物の隔離が含まれる。",
        "prognosis": "Prognosis depends on severity, underlying cause, and timeliness of treatment. Early aggressive intervention generally improves outcomes. Delayed presentation carries a guarded to poor prognosis.",
        "prognosis_ja": "クロストリジウム腸炎の予後: 急性消化器疾患は多くが治療に良好に反応。閉塞性疾患は早期外科介入で予後良好。慢性疾患は食事管理で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Salmonellosis",
        "name_ja": "サルモネラ症",
        "symptoms": {"appetite_loss", "diarrhea", "fever", "lethargy", "sudden_death"},
        "description": "Salmonellosis is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "サルモネラ属による細菌感染で、腸炎と敗血症を引き起こします。人獣共通感染症のリスクがあります。",
        "urgency": "high",
        "recommended_tests": ["fecal_culture", "blood_culture", "blood_chemistry"],
        "causes": "Caused by Salmonella spp. bacterial infection acquired through contaminated food, water, or fecal-oral transmission. Zoonotic risk to humans.",
        "causes_ja": "デグーにおけるサルモネラ症の原因: 創傷汚染、経口摂取、吸入、日和見的過剰増殖による細菌コロニー形成。ストレス、免疫抑制、不衛生、過密飼育、併発疾患が素因となる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "サルモネラ症はデグーにおける細菌感染症である。病原菌は付着因子を通じて組織にコロニーを形成し、毒素産生、酵素分泌、免疫回避戦略などの病原性メカニズムを介して侵入する。好中球浸潤、サイトカイン放出、補体活性化を含む炎症カスケードが生じる。組織損傷は細菌の直接作用と宿主の炎症反応の両方に起因する。菌種と宿主の免疫状態に応じて、膿瘍形成、敗血症、または慢性肉芽腫性炎症が発生しうる。",
        "treatment": "Enrofloxacin 5-10 mg/kg PO q12h based on C&S. SC fluids. Zoonotic. Carrier state possible.",
        "treatment_ja": "デグーにおけるサルモネラ症の治療: ① 健常成獣の無症候性キャリアは抗菌薬を控え自然排菌待ち（抗菌薬は耐性化・キャリア化リスク）。② 重症臨床例（敗血症・下血・脱水）には培養感受性後の抗菌薬: エンロフロキサシン 10-20 mg/kg PO/IM q12-24h（鳥類）/ 5-10 mg/kg PO q12-24h（小型哺乳類） × 14-21日、または トリメトプリム・スルファ 15-30 mg/kg PO q12h。③ 輸液療法 + 電解質補正、制吐・止瀉対症療法。④ ⚠人獣共通感染症—家族（特に小児・免疫不全者）の手洗い・接触予防徹底。⑤ 環境消毒は塩素系（次亜塩素酸 1:10）または過酢酸が有効。⑥ 群飼育では感染源（飼料・水・媒介動物）の検索と隔離。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "サルモネラ症の予防には適切な衛生管理・消毒、利用可能なワクチン接種、創傷の迅速な処置、ストレス軽減、適切な換気、感染動物の隔離が含まれる。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "サルモネラ症の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "E. coli Enteritis",
        "name_ja": "大腸菌性腸炎",
        "symptoms": {"appetite_loss", "dehydration", "diarrhea", "lethargy"},
        "description": "E. coli Enteritis is a gastrointestinal condition affecting digestive function and nutrient absorption.",
        "description_ja": "病原性大腸菌感染による急性下痢で、特に若齢やストレス下のデグーに多いです。",
        "urgency": "high",
        "recommended_tests": ["fecal_culture", "blood_chemistry", "physical_exam"],
        "causes": "Caused by pathogenic Escherichia coli strains colonizing the intestinal tract, particularly in young or stressed degus with compromised gut flora.",
        "causes_ja": "デグーにおける大腸菌性腸炎の原因: 創傷汚染、経口摂取、吸入、日和見的過剰増殖による細菌コロニー形成。ストレス、免疫抑制、不衛生、過密飼育、併発疾患が素因となる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "大腸菌性腸炎はデグーにおける細菌感染症である。病原菌は付着因子を通じて組織にコロニーを形成し、毒素産生、酵素分泌、免疫回避戦略などの病原性メカニズムを介して侵入する。好中球浸潤、サイトカイン放出、補体活性化を含む炎症カスケードが生じる。組織損傷は細菌の直接作用と宿主の炎症反応の両方に起因する。菌種と宿主の免疫状態に応じて、膿瘍形成、敗血症、または慢性肉芽腫性炎症が発生しうる。",
        "treatment": "Fluid therapy: warmed lactated Ringer's 10-15 mL/kg SC q8-12h or IP for moderate-severe dehydration. Antibiotics (culture-guided preferred): enrofloxacin 5-10 mg/kg PO/SC q12h or trimethoprim-sulfa 15-30 mg/kg PO q12h as first-line (AVOID oral beta-lactams — fatal dysbiosis risk in hindgut fermenters). GI protectants: sucralfate 25-50 mg/kg PO q8h. Pain management: meloxicam 1-2 mg/kg PO/SC q24h. Probiotics: Lactobacillus spp. or Saccharomyces boulardii to restore cecal flora. Syringe feeding with Critical Care for Herbivores if anorexic — maintain gut motility. Environmental warming to 25-28°C. Strict cage hygiene with daily bedding changes. Isolate affected animals. Monitor hydration status (skin turgor, mucous membranes) and fecal output q8-12h.",
        "treatment_ja": "輸液: 加温乳酸リンゲル液 10-15mL/kg SC q8-12h、中等度-重度脱水にはIP投与。抗菌薬（培養感受性試験に基づく選択推奨）: エンロフロキサシン 5-10mg/kg PO/SC q12h、またはトリメトプリム-スルファ 15-30mg/kg PO q12h（第一選択）。経口βラクタム系は禁忌 — 後腸発酵動物では致死的ディスバイオーシスのリスク。消化管保護: スクラルファート 25-50mg/kg PO q8h。疼痛管理: メロキシカム 1-2mg/kg PO/SC q24h。プロバイオティクス: Lactobacillus属またはSaccharomyces boulardiiで盲腸フローラ回復。食欲廃絶時はシリンジ給餌（草食動物用クリティカルケア）で腸管運動維持。環境保温25-28℃。ケージの厳格な衛生管理（毎日の床材交換）。罹患動物の隔離。水和状態（皮膚ツルゴール、粘膜）と糞便排出量をq8-12hモニタリング。",
        "prevention": "Strict cage hygiene with regular cleaning and disinfection. Avoid overcrowding and social stress. Provide fresh, clean water and high-quality timothy hay-based diet. Quarantine new animals for 2-4 weeks. Minimize handling stress in young degus. Maintain stable environmental temperature.",
        "prevention_ja": "ケージの厳格な衛生管理（定期清掃・消毒）。過密飼育・社会的ストレスの回避。新鮮な水とチモシー主体の良質な食事の提供。新規導入動物の2-4週間検疫。若齢デグーのハンドリングストレス最小化。環境温度の安定維持。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "大腸菌性腸炎の予後: 急性消化器疾患は多くが治療に良好に反応。閉塞性疾患は早期外科介入で予後良好。慢性疾患は食事管理で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Cecal Dysbiosis",
        "name_ja": "盲腸内細菌叢異常",
        "symptoms": {"abdominal_pain", "appetite_loss", "diarrhea", "gas", "soft_stool"},
        "description": "Cecal Dysbiosis is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "不適切な食事や抗生物質使用による盲腸の正常な微生物叢の撹乱です。",
        "urgency": "moderate",
        "recommended_tests": ["fecal_exam", "physical_exam", "diet_review"],
        "causes": "Caused by disruption of normal cecal microflora from inappropriate diet (low fiber, high sugar), antibiotic use, or stress, leading to pathogenic bacterial overgrowth.",
        "causes_ja": "デグーにおける盲腸細菌叢異常の原因: 経口摂取、吸入、経皮接触による有毒物質への曝露。有毒植物、化学物質、重金属、汚染食物/水、不適切な薬物使用が原因。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "盲腸細菌叢異常はデグーにおける中毒性疾患である。有害物質の経口摂取、吸入、または経皮吸収により中毒障害が生じる。毒素は酵素阻害、受容体干渉、酸化的損傷、直接的な細胞毒性などの特定のメカニズムを通じて細胞プロセスを障害する。標的臓器は毒素により異なるが、肝臓（生体内変換）、腎臓（排泄）、神経系、消化管が一般的である。用量依存的に無症候性変化から劇症型臓器不全まで幅広い影響を及ぼす。",
        "treatment": "Cecal dysbiosis is a potentially life-threatening condition in degus as hindgut fermenters — "
        "disruption of the cecal microbiome leads to pathogenic Clostridial overgrowth and "
        "enterotoxemia. IMMEDIATE MANAGEMENT: (1) FLUID RESUSCITATION: SC fluids — warmed LRS "
        "50-100 mL/kg/day in divided doses. IV access for severe cases. (2) DIETARY CORRECTION "
        "(CRITICAL): Eliminate ALL offending foods — return to strict timothy hay-based diet. "
        "No sugar, no fruit, no commercial treats, no starchy foods. Timothy hay should constitute "
        "≥80% of diet. Fresh water ad libitum. If anorexic: syringe feeding with Critical Care "
        "for Herbivores (Oxbow) 50-80 mL/kg/day q4-6h. (3) PROBIOTICS: Saccharomyces boulardii "
        "or mixed Lactobacillus/Bifidobacterium preparations to restore commensal flora. Transfaunation "
        "(cecal contents from healthy degu) has been described anecdotally. (4) GI MOTILITY SUPPORT: "
        "Simethicone 1-2 mL/kg PO q8h for gas accumulation. Metoclopramide 0.5 mg/kg PO/SC "
        "q8-12h if ileus suspected (rule out obstruction first). (5) PAIN MANAGEMENT: Meloxicam "
        "1-2 mg/kg PO/SC q24h for abdominal discomfort. (6) ANTIBIOTICS — USE WITH EXTREME "
        "CAUTION: Only if secondary bacterial infection confirmed. Metronidazole 10-20 mg/kg "
        "PO q12h × 5-7 days (targets anaerobic Clostridial overgrowth specifically). "
        "ABSOLUTELY CONTRAINDICATED: Oral β-lactam antibiotics (amoxicillin, ampicillin, "
        "penicillin, cephalosporins) — these are the most common CAUSE of cecal dysbiosis "
        "in degus and other hindgut fermenters, causing fatal Clostridial enterotoxemia. "
        "References: Quesenberry & Carpenter (2012); Harkness et al. (2010) Biology and "
        "Medicine of Rabbits and Rodents 5th ed.",
        "treatment_ja": "盲腸内細菌叢異常はデグーのような後腸発酵動物では致死的になりうる — 盲腸マイクロバイオーム"
        "の撹乱が病原性クロストリジウムの過剰増殖と腸管毒素症を引き起こす。【即時管理】"
        "(1) 皮下補液: 加温LRS 50-100 mL/kg/日。(2) 食事是正（最重要）: 原因食品の全排除 — "
        "チモシー牧草厳格食に戻す。糖分・果物・おやつ・でんぷん質食品は全て禁忌。食欲がない場合: "
        "クリティカルケアのシリンジ給餌。(3) プロバイオティクス: S. boulardiiまたは混合乳酸菌。"
        "健康デグーの盲腸内容物の移植（トランスファウネーション）も報告あり。"
        "(4) 消化管運動支持: シメチコン1-2 mL/kg PO q8h。メトクロプラミド0.5 mg/kg "
        "PO/SC q8-12h（閉塞を除外後）。(5) 疼痛管理: メロキシカム1-2 mg/kg PO/SC q24h。"
        "(6) 抗菌薬 — 極度に慎重に使用: メトロニダゾール10-20 mg/kg PO q12h × 5-7日"
        "（嫌気性クロストリジウムに特異的）。絶対禁忌: 経口βラクタム系抗菌薬 — これらは"
        "デグーの盲腸内細菌叢異常の最も一般的な原因であり、致死的な腸管毒素症を引き起こす。",
        "prevention": "Strict timothy hay-based diet (≥80%) — the single most important preventive measure. "
        "No sugar, no fruit, no starchy treats (critical for diabetes AND cecal health). Gradual "
        "dietary changes only (≥7 day transition). AVOID oral β-lactam antibiotics at all costs — "
        "use enrofloxacin or trimethoprim-sulfa for infections requiring antibiotics. Minimize "
        "stress (appropriate group housing, environmental enrichment). Fresh water always available. "
        "Reference: Quesenberry & Carpenter (2012); Harkness et al. (2010).",
        "prevention_ja": "チモシー牧草ベースの厳格食（≥80%）が最も重要な予防策。糖分・果物・でんぷん質おやつ禁忌"
        "（糖尿病予防と盲腸健康の両方に重要）。食事変更は段階的に（≥7日間の移行期間）。"
        "経口βラクタム系抗菌薬は絶対に避ける。ストレス軽減（適切な群れ飼育、環境エンリッチメント）。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "盲腸内細菌叢異常の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Gastric Ulceration",
        "name_ja": "胃潰瘍",
        "symptoms": {"abdominal_pain", "appetite_loss", "dark_stool", "teeth_grinding", "weight_loss"},
        "description": "Gastric Ulceration is an erosive lesion of tissue requiring treatment to promote healing and prevent complications.",
        "description_ja": "ストレス、NSAID使用、ヘリコバクター感染による胃粘膜の糜爛と潰瘍です。",
        "urgency": "high",
        "recommended_tests": ["physical_exam", "fecal_occult_blood", "blood_chemistry"],
        "causes": "Multifactorial etiology including infectious, environmental, immune, and host-related factors. Specific risk factors and triggers vary by individual case.",
        "causes_ja": "デグーにおける胃潰瘍の原因: 慢性的なストレス（不適切な飼育環境・単独飼育・過密飼育）、不適切な食事（高糖質食・低繊維食）、NSAIDの不適切な使用が主な原因。デグーは社会性の高い動物であり、社会的ストレスが消化管に影響しやすい。糖尿病併発時の代謝異常も胃粘膜障害のリスク因子となる。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "胃潰瘍はデグーにおける消化器疾患である。胃酸分泌と粘膜防御因子のバランスが崩れ、胃粘膜の糜爛・潰瘍が形成される。ストレスによる交感神経亢進が胃粘膜血流を減少させ、粘膜バリアを脆弱化する。進行すると出血（黒色便）、穿孔、腹膜炎を引き起こしうる。デグーは後腸発酵動物であり、消化管機能障害は腸内細菌叢の破綻と全身状態の悪化に直結する。",
        "treatment": "Stress factor elimination is primary: ensure adequate social housing (degus are colonial), environmental enrichment, and stable routine. GI protectants: sucralfate 25-50 mg/kg PO q8h (30 min before other oral medications, provides mucosal coating). Acid suppression: ranitidine 2-5 mg/kg PO q12h or omeprazole 0.5-1 mg/kg PO q24h. Pain management: meloxicam 1-2 mg/kg PO/SC q24h (use cautiously — NSAIDs can worsen ulcers; limit to 3-5 days, discontinue if GI signs worsen). Fluid therapy: warmed lactated Ringer's 10-15 mL/kg SC q12h if dehydrated. Diet: transition to high-fiber timothy hay-based diet, avoid all sugary treats (degus are highly prone to diabetes). If Helicobacter suspected: triple therapy with metronidazole 20 mg/kg PO q12h + amoxicillin (PARENTERAL ONLY — 15 mg/kg SC q12h, oral amoxicillin contraindicated) + bismuth subsalicylate 0.5-1 mL/kg PO q8-12h for 14 days. Manage concurrent diabetes if present (blood glucose monitoring, strict diet control). Provide social companionship — single housing causes chronic stress exacerbating ulcers.",
        "treatment_ja": "ストレス因子の除去が最優先: 適切な集団飼育（デグーは群居性）、環境エンリッチメント、安定した日課の確保。消化管保護: スクラルファート 25-50mg/kg PO q8h（他経口薬の30分前、粘膜被覆効果）。酸分泌抑制: ラニチジン 2-5mg/kg PO q12h、またはオメプラゾール 0.5-1mg/kg PO q24h。疼痛管理: メロキシカム 1-2mg/kg PO/SC q24h（慎重使用 — NSAIDsは潰瘍を悪化させうる。3-5日に限定し消化器症状悪化時は中止）。輸液: 脱水時に加温乳酸リンゲル液 10-15mL/kg SC q12h。食事: 高繊維チモシー主体食に移行、糖分を含む全てのおやつを禁止（デグーは糖尿病好発種）。ヘリコバクター感染疑い時: 3剤併用療法 — メトロニダゾール 20mg/kg PO q12h + アモキシシリン（非経口のみ — 15mg/kg SC q12h、経口アモキシシリンは禁忌）+ 次サリチル酸ビスマス 0.5-1mL/kg PO q8-12h、14日間。糖尿病併発時は血糖モニタリングと厳格な食事管理。社会的パートナーの提供 — 単独飼育は慢性ストレスとなり潰瘍を悪化させる。",
        "prevention": "Provide social housing (groups of 2-4+). Minimize environmental stressors (sudden changes, loud noises, predator presence). High-fiber timothy hay-based diet without sugar-containing treats. Avoid prolonged NSAID use. Regular fecal occult blood testing in at-risk animals. Environmental enrichment (wheels, tunnels, foraging opportunities).",
        "prevention_ja": "集団飼育（2-4頭以上）の提供。環境ストレス因子の最小化（急激な変化、騒音、捕食者の存在の回避）。糖分を含まない高繊維チモシー主体食。NSAIDの長期使用回避。リスク動物の定期的な便潜血検査。環境エンリッチメント（ホイール、トンネル、採食機会の提供）。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "胃潰瘍の予後: 急性消化器疾患は多くが治療に良好に反応。閉塞性疾患は早期外科介入で予後良好。慢性疾患は食事管理で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Cecal Impaction",
        "name_ja": "盲腸嵌頓",
        "symptoms": {"abdominal_distension", "appetite_loss", "lethargy", "reduced_fecal_output"},
        "description": "Cecal Impaction involves blockage of a body passage or organ requiring intervention to restore normal flow.",
        "description_ja": "脱水や低繊維食による乾燥した内容物の盲腸嵌頓です。",
        "urgency": "high",
        "recommended_tests": ["abdominal_xray", "physical_exam", "abdominal_palpation"],
        "causes": "Caused by dehydration and low-fiber diet leading to desiccation and compaction of cecal contents, impairing normal fermentation and motility.",
        "causes_ja": "デグーにおける盲腸嵌頓の原因: 脱水や低繊維食による乾燥した内容物の盲腸嵌頓です。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "盲腸嵌頓はデグーにおける栄養障害である。特定の栄養素の不十分な摂取、吸収不良、または過剰摂取により生じる。欠乏状態では、影響を受けた栄養素を補因子または基質として必要とする生化学的経路が障害され、細胞機能障害を引き起こす。過剰状態では組織への蓄積や栄養素間相互作用の障害により毒性が生じる。種特異的な食事要求により、適切な栄養管理が予防に不可欠である。",
        "treatment": "EMERGENCY MANAGEMENT: Cecal impaction in degus is a potentially life-threatening condition "
        "requiring immediate intervention. (1) AGGRESSIVE REHYDRATION: SC fluids — warmed LRS "
        "60-100 mL/kg/day in divided doses q6-8h. Severely dehydrated: IV access (lateral tail "
        "vein) for fluid bolus 10-15 mL/kg over 15-20 min, then maintenance. Oral hydration via "
        "syringe if conscious and able to swallow. (2) GI MOTILITY STIMULATION: Metoclopramide "
        "0.5 mg/kg PO/SC q8-12h (ONLY after ruling out complete obstruction on radiographs). "
        "Cisapride 0.5-1 mg/kg PO q8-12h (prokinetic — may be more effective for large bowel "
        "motility). Simethicone 1-2 mL/kg PO q8h for gas accumulation. (3) DIETARY MANAGEMENT: "
        "Unlimited timothy hay ad libitum (fiber drives cecal motility). Syringe feeding with "
        "Critical Care for Herbivores (Oxbow) 50-80 mL/kg/day if anorexic — adding water to "
        "increase moisture content. Fresh leafy greens for hydration (romaine, cilantro — NO "
        "sugar-containing foods). (4) PAIN MANAGEMENT: Meloxicam 1-2 mg/kg PO/SC q24h. "
        "Buprenorphine 0.05-0.1 mg/kg SC q8-12h for severe abdominal pain. (5) GENTLE ABDOMINAL "
        "MASSAGE: May help break up impacted cecal contents. (6) WARM WATER/SALINE ENEMA: "
        "5-10 mL warmed saline via soft rubber catheter (extreme care — fragile intestinal wall). "
        "SURGICAL INTERVENTION: Rarely successful in degus due to small body size and anesthetic "
        "risk. Consider only if medical management fails after 24-48h and imaging confirms "
        "complete obstruction. NOTE: Oral β-lactam antibiotics CONTRAINDICATED. "
        "References: Quesenberry & Carpenter (2012); Harkness et al. (2010).",
        "treatment_ja": "【緊急管理】盲腸嵌頓は致死的になりうる緊急状態。(1) 積極的な水分補給: 皮下補液 — "
        "加温LRS 60-100 mL/kg/日を6-8時間ごとに分割。重度脱水: IVアクセス。経口補水も可能なら"
        "併用。(2) 消化管運動促進: メトクロプラミド0.5 mg/kg PO/SC q8-12h（X線で完全閉塞を"
        "除外後のみ）。シサプリド0.5-1 mg/kg PO q8-12h。シメチコン1-2 mL/kg PO q8h。"
        "(3) 食事管理: チモシー牧草の無制限提供。食欲がなければクリティカルケアのシリンジ給餌"
        "（水分を多めに混合）。(4) 疼痛管理: メロキシカム1-2 mg/kg PO/SC q24h。ブプレノルフィン"
        "0.05-0.1 mg/kg SC q8-12h。(5) 腹部マッサージ。(6) 温生理食塩水浣腸: 5-10mLを"
        "軟質カテーテルで（腸壁が脆弱なため極度の注意）。外科は体サイズと麻酔リスクにより稀。"
        "経口βラクタム系は禁忌。",
        "prevention": "Unlimited timothy hay access at all times (fiber drives cecal motility). Adequate fresh water "
        "always available (multiple water sources). No sugar/fruit/starchy treats (dysbiosis risk). "
        "Regular exercise to stimulate GI motility. Avoid dehydration — water bottle should be "
        "checked daily for function. Monitor fecal output daily — decreased pellet size/quantity is "
        "an early warning sign. Reference: Quesenberry & Carpenter (2012).",
        "prevention_ja": "チモシー牧草の常時無制限提供（繊維が盲腸運動を駆動）。新鮮な水の常時提供（複数の"
        "水源）。糖分/果物/でんぷん質おやつ禁忌。定期的な運動。脱水回避。毎日の糞便量モニタリング。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "盲腸嵌頓の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Intussusception",
        "name_ja": "腸重積症",
        "symptoms": {"abdominal_pain", "bloody_stool", "dehydration", "lethargy", "vomiting"},
        "description": "Intussusception is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "腸の一部が別の部分に陥入し、閉塞と虚血を引き起こします。",
        "urgency": "emergency",
        "recommended_tests": ["abdominal_ultrasound", "abdominal_xray", "physical_exam"],
        "causes": "Caused by telescoping of one intestinal segment into another, often triggered by severe enteritis, parasitism, or intestinal masses causing abnormal peristalsis.",
        "causes_ja": "デグーにおける腸重積症の原因: 腸の一部が別の部分に陥入し、閉塞と虚血を引き起こします。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "腸重積症はデグーにおける消化器疾患である。粘膜の完全性、運動性、分泌機能、またはマイクロバイオームバランスの障害を伴う。炎症により上皮バリアが損傷し、吸収不良、体液喪失、細菌トランスロケーションの可能性がある。運動障害（低運動性/うっ滞または亢進）により通過時間と消化効率が変化する。後腸発酵動物では盲腸/結腸フローラの破壊が致死的ディスバイオーシスと腸管毒素症を引き起こしうる。",
        "treatment": "Surgical emergency. Pre-operative stabilization: warmed lactated Ringer's 10-15 mL/kg SC/IP, pain management with buprenorphine 0.05-0.1 mg/kg SC q8-12h. Emergency exploratory laparotomy under isoflurane inhalation anesthesia; attempt manual reduction of intussusception. If viable bowel: reduce and anchor with serosal sutures. If necrotic bowel: intestinal resection and end-to-end anastomosis. Post-operative antibiotics: enrofloxacin 5-10 mg/kg SC q12h + metronidazole 20 mg/kg PO q12h (AVOID oral beta-lactams). Post-operative analgesia: meloxicam 1-2 mg/kg PO/SC q24h for 3-5 days, buprenorphine 0.05 mg/kg SC q8-12h for first 24-48h. Early assisted feeding with Critical Care for Herbivores via syringe to maintain gut motility. Monitor for peritonitis and anastomotic dehiscence (fever, abdominal pain, worsening lethargy). Treat underlying cause: fecal parasitology (fenbendazole 20 mg/kg PO q24h × 5 days if parasites detected), bacterial enteritis. Environmental warming to 28-30°C post-operatively. Degus are prone to hypothermia under anesthesia.",
        "treatment_ja": "外科的緊急疾患。術前安定化: 加温乳酸リンゲル液 10-15mL/kg SC/IP、疼痛管理にブプレノルフィン 0.05-0.1mg/kg SC q8-12h。イソフルラン吸入麻酔下で緊急開腹術、腸重積の用手整復を試みる。腸管が生存可能な場合: 整復後漿膜縫合で固定。壊死腸管がある場合: 腸管切除・端々吻合術。術後抗菌薬: エンロフロキサシン 5-10mg/kg SC q12h + メトロニダゾール 20mg/kg PO q12h（経口βラクタム系禁忌）。術後鎮痛: メロキシカム 1-2mg/kg PO/SC q24h 3-5日間、ブプレノルフィン 0.05mg/kg SC q8-12h 最初の24-48時間。草食動物用クリティカルケアによるシリンジ給餌を早期に開始し腸管運動維持。腹膜炎・吻合部離開の徴候（発熱、腹痛、活動性低下の悪化）をモニタリング。基礎疾患の治療: 糞便寄生虫検査（寄生虫検出時フェンベンダゾール 20mg/kg PO q24h×5日間）、細菌性腸炎。術後は環境温度28-30℃に保温。デグーは麻酔下で低体温に陥りやすい。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "腸重積症の予防: 定期的な健康診断。適切な栄養管理。ストレスの軽減。清潔な飼育環境の維持。異常の早期発見・早期受診。",
        "prognosis": "Prognosis depends on severity, underlying cause, and timeliness of treatment. Early aggressive intervention generally improves outcomes. Delayed presentation carries a guarded to poor prognosis.",
        "prognosis_ja": "腸重積症の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"young"},
    },
    {
        "name": "Hepatic Coccidiosis",
        "name_ja": "肝コクシジウム症",
        "symptoms": {"abdominal_distension", "appetite_loss", "jaundice", "lethargy", "weight_loss"},
        "description": "Hepatic Coccidiosis is a hepatic condition affecting liver function and metabolism.",
        "description_ja": "肝臓に影響するコクシジウム感染で、胆管過形成と肝不全の可能性があります。",
        "urgency": "high",
        "recommended_tests": ["fecal_flotation", "blood_chemistry", "liver_ultrasound"],
        "causes": "Caused by Eimeria spp. coccidia infecting hepatic tissue, leading to bile duct hyperplasia and potential liver failure. Transmitted via fecal-oral route.",
        "causes_ja": "デグーにおける肝コクシジウム症の原因: 肝臓に影響するコクシジウム感染で、胆管過形成と肝不全の可能性があります。",
        "pathophysiology": "Hepatocellular damage impairs metabolic, synthetic, and detoxification functions. Progressive injury leads to inflammation, fibrosis, and potential hepatic failure with systemic consequences.",
        "pathophysiology_ja": "肝コクシジウム症はデグーにおける寄生虫疾患である。寄生虫は経口摂取、経皮的侵入、またはベクター媒介伝播を通じて感染を確立する。抗原変異、免疫調節、細胞内隔離により宿主の免疫防御を回避しながら、宿主の栄養と資源を利用して増殖する。組織損傷は寄生虫の直接的な摂食、機械的破壊、有毒代謝副産物、宿主の炎症・免疫応答に起因する。重度の寄生虫感染は貧血、栄養失調、臓器機能障害、二次感染を引き起こしうる。",
        "treatment": "ANTICOCCIDIAL THERAPY: Toltrazuril 25 mg/kg PO q24h × 3 days, repeat after 7-day "
        "interval (first-line for Eimeria spp. — targets all intracellular stages). Alternative: "
        "sulfadimethoxine 25-50 mg/kg PO q24h × 10-14 days (bacteriostatic, less effective against "
        "hepatic forms than toltrazuril). Trimethoprim-sulfa 15-30 mg/kg PO q12h × 14-21 days "
        "(alternative sulfonamide). HEPATIC SUPPORT: Hepatoprotective agents — silymarin (milk "
        "thistle extract) 4-15 mg/kg PO q12h (antioxidant, anti-inflammatory, stabilizes "
        "hepatocyte membranes). SAMe (S-adenosylmethionine) 20 mg/kg PO q24h on empty stomach "
        "(hepatic glutathione precursor). Ursodiol 10-15 mg/kg PO q24h (choleretic, reduces "
        "bile duct obstruction from hyperplasia). SUPPORTIVE CARE: SC fluids 50-100 mL/kg/day "
        "for dehydration. Syringe feeding if anorexic. Meloxicam 1-2 mg/kg PO/SC q24h for "
        "discomfort. MONITORING: Blood chemistry (ALT, ALP, bilirubin, albumin) q2-4 weeks to "
        "assess hepatic function and treatment response. Fecal flotation q2 weeks to confirm "
        "oocyst elimination. ENVIRONMENTAL DECONTAMINATION: Remove all bedding, clean cage with "
        "10% ammonia solution or steam (oocysts are resistant to most disinfectants), daily "
        "fecal removal to break reinfection cycle. Treat ALL in-contact degus simultaneously. "
        "NOTE: Oral β-lactam antibiotics CONTRAINDICATED. "
        "References: Quesenberry & Carpenter (2012); Taylor et al. (2016) Veterinary Parasitology.",
        "treatment_ja": "【抗コクシジウム療法】トルトラズリル25 mg/kg PO q24h × 3日間、7日後に再投与（Eimeria "
        "spp.の第一選択 — 全細胞内ステージを標的）。代替: スルファジメトキシン25-50 mg/kg "
        "PO q24h × 10-14日。TMS 15-30 mg/kg PO q12h × 14-21日。【肝保護】シリマリン（ミルク"
        "シスル）4-15 mg/kg PO q12h。SAMe 20 mg/kg PO q24h（空腹時）。ウルソジオール"
        "10-15 mg/kg PO q24h（胆管過形成による閉塞軽減）。【支持療法】皮下補液、シリンジ"
        "給餌、メロキシカム1-2 mg/kg。【モニタリング】血液化学（ALT/ALP/ビリルビン/アルブミン）"
        "を2-4週ごと。糞便浮遊法を2週ごと。【環境除染】10%アンモニア溶液またはスチームで消毒"
        "（オーシストは大部分の消毒剤に耐性）。全接触デグーを同時治療。経口βラクタム系禁忌。",
        "prevention": "Strict hygiene — daily fecal removal from cage to prevent oocyst sporulation (requires "
        "24-48h in environment to become infective). Clean cage thoroughly with steam or 10% "
        "ammonia (oocysts resist most chemical disinfectants). Quarantine new degus for 2-4 weeks "
        "with fecal flotation examination before introduction. Avoid overcrowding (increases "
        "fecal-oral transmission). Stress reduction (stress-induced immunosuppression increases "
        "susceptibility). Regular fecal screening every 6-12 months. "
        "Reference: Taylor et al. (2016) Veterinary Parasitology.",
        "prevention_ja": "厳格な衛生管理 — 毎日の糞便除去（オーシストが感染性になるのに環境中で24-48時間必要）。"
        "スチームまたは10%アンモニアでケージ消毒。新規デグーの2-4週間隔離と糞便検査。"
        "過密飼育回避。ストレス軽減。6-12ヶ月ごとの定期糞便検査。",
        "prognosis": "Variable. Hepatic lipidosis has a fair prognosis with early aggressive nutritional support. Chronic liver disease is guarded depending on underlying cause and degree of fibrosis.",
        "prognosis_ja": "肝コクシジウム症の予後: 原因と重症度による。急性肝疾患は早期治療で回復可能。慢性肝疾患は長期管理で QOL 維持可能。肝不全は予後不良。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Pinworm Infection (Syphacia)",
        "name_ja": "蟯虫感染（シファシア）",
        "symptoms": {"perianal_irritation", "poor_coat", "restlessness", "weight_loss"},
        "description": "Pinworm Infection (Syphacia) is a bacterial infection that causes systemic or localized inflammatory disease requiring prompt antimicrobial therapy.",
        "description_ja": "通常軽度の症状を引き起こす一般的な腸管線虫感染ですが、免疫不全動物では重要です。",
        "urgency": "low",
        "recommended_tests": ["fecal_flotation", "perianal_tape_test", "physical_exam"],
        "causes": "Multifactorial etiology including infectious, environmental, immune, and host-related factors. Specific risk factors and triggers vary by individual case.",
        "causes_ja": "デグーにおける蟯虫症の原因: Syphacia属蟯虫の感染期虫卵の経口摂取（糞口感染）による。集団飼育環境での感染拡大が特徴的で、床材や飼育用品を介した間接的伝播も起こる。不衛生な飼育環境、過密飼育、ストレス、免疫抑制が感染リスクを高める。",
        "pathophysiology": "Bacterial organisms invade host tissues, triggering inflammatory cascades with neutrophil recruitment, cytokine release, and potential tissue necrosis. Systemic spread may lead to bacteremia and multi-organ dysfunction.",
        "pathophysiology_ja": "Syphacia属蟯虫の感染期虫卵が経口摂取されると、幼虫は盲腸・結腸に定着し成虫へと発育する。成熟した雌虫は夜間に肛門周囲に移動して産卵し、肛門周囲の掻痒と炎症を引き起こす。重度感染では腸粘膜への機械的損傷と栄養競合により、体重減少や被毛粗剛が生じる。集団飼育環境では糞口感染サイクルにより急速に感染が拡大する。",
        "treatment": "Antimicrobial therapy based on culture and sensitivity, wound care or drainage as needed, pain management, and monitoring for resolution.",
        "treatment_ja": "デグーにおける蟯虫症（Syphacia）の治療は、フェンベンダゾール（20-50mg/kg経口、5-10日間）またはイベルメクチン（0.2-0.4mg/kg皮下注射、2週間隔で2-3回）による駆虫が基本。飼育ケージ・床材の徹底的な清掃・消毒を同時に行い再感染を防止する。同居個体も同時に治療し、糞便検査で駆虫効果を確認する。",
        "prevention": "Prevention includes maintaining proper hygiene, appropriate husbandry, stress reduction, quarantine of new animals, and prompt treatment of wounds or primary conditions.",
        "prevention_ja": "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）；定期的な獣医師の健康診断；新規動物の検疫；ストレス軽減；種特異的予防措置が含まれる",
        "prognosis": "Good with appropriate antimicrobial therapy. Most infections resolve with proper treatment. Chronic or recurrent cases may require longer management.",
        "prognosis_ja": "適切な駆虫薬治療で予後は一般的に良好。重度感染や免疫不全のデグーでは予後不良となりうる。環境消毒と再感染予防が長期的な予後改善に重要。定期的な糞便検査と予防的駆虫が推奨される。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Tapeworm Infection",
        "name_ja": "条虫感染症",
        "symptoms": {"perianal_irritation", "poor_coat", "visible_proglottids", "weight_loss"},
        "description": "Tapeworm Infection is a bacterial infection that causes systemic or localized inflammatory disease requiring prompt antimicrobial therapy.",
        "description_ja": "条虫感染で、重度寄生では体重減少と腸閉塞の可能性があります。",
        "urgency": "moderate",
        "recommended_tests": ["fecal_flotation", "fecal_exam", "physical_exam"],
        "causes": "Caused by cestode parasites acquired through ingestion of intermediate hosts (arthropods) or contaminated food containing infective larvae.",
        "causes_ja": "デグーにおける条虫感染症の原因: 条虫感染で、重度寄生では体重減少と腸閉塞の可能性があります。",
        "pathophysiology": "Bacterial organisms invade host tissues, triggering inflammatory cascades with neutrophil recruitment, cytokine release, and potential tissue necrosis. Systemic spread may lead to bacteremia and multi-organ dysfunction.",
        "pathophysiology_ja": "条虫感染症はデグーにおける寄生虫疾患である。寄生虫は経口摂取、経皮的侵入、またはベクター媒介伝播を通じて感染を確立する。抗原変異、免疫調節、細胞内隔離により宿主の免疫防御を回避しながら、宿主の栄養と資源を利用して増殖する。組織損傷は寄生虫の直接的な摂食、機械的破壊、有毒代謝副産物、宿主の炎症・免疫応答に起因する。重度の寄生虫感染は貧血、栄養失調、臓器機能障害、二次感染を引き起こしうる。",
        "treatment": "Treatment includes appropriate antimicrobial therapy based on culture and sensitivity, supportive care, fluid therapy, and surgical drainage if indicated. Monitor for treatment response and complications.",
        "treatment_ja": "デグーにおける条虫感染症の治療には、同定された寄生虫に応じた適切な駆虫薬が必要である。一部の駆虫薬は特定の種に有毒であるため、種に適した用量設定が重要である。全てのライフステージを排除するため複数回投与が必要な場合がある。環境消毒と接触動物の治療で再感染を防止する。貧血、脱水、栄養失調などの二次的合併症に対する支持療法を行う。",
        "prevention": "Prevention includes maintaining proper hygiene, appropriate husbandry, stress reduction, quarantine of new animals, and prompt treatment of wounds or primary conditions.",
        "prevention_ja": "条虫感染症の予防には定期的な予防駆虫、環境衛生と糞便除去、新規動物の隔離・検査、ベクター防除、中間宿主や汚染環境への曝露回避が含まれる。",
        "prognosis": "Good with appropriate antimicrobial therapy. Most infections resolve with proper treatment. Chronic or recurrent cases may require longer management.",
        "prognosis_ja": "条虫感染症の予後: 適切な抗菌薬療法で多くが治癒可能。慢性・深在性感染は長期治療が必要。敗血症は予後要注意。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Nephrolithiasis",
        "name_ja": "腎結石症",
        "symptoms": {"appetite_loss", "back_pain", "blood_in_urine", "polydipsia"},
        "description": "Nephrolithiasis is a renal condition affecting kidney function and fluid-electrolyte balance.",
        "description_ja": "腎臓内の結石形成で、閉塞と進行性の腎障害を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["abdominal_xray", "renal_ultrasound", "urinalysis"],
        "causes": "Caused by mineral crystallization and stone formation within the renal pelvis, predisposed by dietary calcium-phosphorus imbalance, dehydration, and urinary pH abnormalities.",
        "causes_ja": "デグーにおける腎結石症の原因: 腎臓内の結石形成で、閉塞と進行性の腎障害を引き起こします。",
        "pathophysiology": "Progressive loss of functional nephrons impairs glomerular filtration, tubular reabsorption, and endocrine function. Uremic toxin accumulation and fluid-electrolyte imbalance lead to systemic complications.",
        "pathophysiology_ja": "腎結石症はデグーにおける腎・泌尿器疾患である。腎臓、尿管、膀胱、または尿道の構造的・機能的障害を伴う。腎疾患は糸球体濾過、尿細管再吸収・分泌、およびホルモン機能（エリスロポエチン、カルシトリオール、レニン）を障害する。進行性のネフロン喪失により高窒素血症、電解質異常、酸塩基障害が生じる。下部尿路疾患は閉塞、尿石症、上行感染を引き起こしうる。",
        "treatment": "Stone analysis is essential for targeted prevention. Surgical intervention for obstructive or large stones: nephrolithotomy/pyelolithotomy under isoflurane anesthesia. Pre-operative stabilization: warmed lactated Ringer's 10-15 mL/kg SC/IP, correct azotemia and electrolyte imbalances. Pain management: meloxicam 1-2 mg/kg PO/SC q24h (limit to 3-5 days if concurrent renal compromise). Perioperative antibiotics: enrofloxacin 5-10 mg/kg PO/SC q12h or trimethoprim-sulfa 15-30 mg/kg PO q12h (AVOID oral beta-lactams). Medical management: increase water intake (multiple water sources, water-rich vegetables in small amounts — avoid sugary items), high-quality timothy hay-based diet with appropriate Ca:P ratio (1.5-2:1). Urine monitoring: pH, sediment, culture q2-4 weeks initially. Repeat imaging (radiograph/ultrasound) q3-6 months for recurrence. Calcium oxalate stones are most common in degus (associated with diabetes and metabolic derangement). Manage concurrent diabetes aggressively — hyperglycemia promotes urinary mineral supersaturation.",
        "treatment_ja": "結石分析が標的予防に不可欠。閉塞性・大型結石には外科的介入: イソフルラン麻酔下で腎切石術/腎盂切石術。術前安定化: 加温乳酸リンゲル液 10-15mL/kg SC/IP、高窒素血症・電解質異常の補正。疼痛管理: メロキシカム 1-2mg/kg PO/SC q24h（腎障害併発時は3-5日に制限）。周術期抗菌薬: エンロフロキサシン 5-10mg/kg PO/SC q12h、またはトリメトプリム-スルファ 15-30mg/kg PO q12h（経口βラクタム系禁忌）。内科管理: 飲水量増加（複数の水場、少量の水分豊富な野菜 — 糖分を含むものは禁止）、適切なCa:P比（1.5-2:1）のチモシー主体食。尿モニタリング: pH、沈渣、培養をq2-4週（初期）。画像検査（レントゲン/エコー）q3-6ヶ月で再発チェック。デグーではシュウ酸カルシウム結石が最多（糖尿病・代謝異常に関連）。糖尿病の積極的管理 — 高血糖は尿中ミネラル過飽和を促進。",
        "prevention": "Ensure adequate water intake: multiple clean water sources, consider water fountain. Provide appropriate timothy hay-based diet with balanced Ca:P ratio. Avoid high-oxalate foods. Strict sugar avoidance (diabetes prevention/management). Regular urinalysis monitoring in at-risk animals. Environmental enrichment to reduce stress. Monitor body weight and metabolic parameters.",
        "prevention_ja": "十分な飲水量の確保: 複数の清潔な水場、循環式給水器の検討。適切なCa:P比のチモシー主体食。シュウ酸含有量の高い食品の回避。糖分の厳格な禁止（糖尿病予防/管理）。リスク動物の定期的尿検査。ストレス軽減のための環境エンリッチメント。体重と代謝パラメータのモニタリング。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "腎結石症の予後: 早期治療で予後良好。再発予防には食事管理と定期検査が重要。閉塞性疾患は緊急対応で予後改善。慢性腎疾患はステージにより予後が異なる。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Pyelonephritis",
        "name_ja": "腎盂腎炎",
        "symptoms": {"appetite_loss", "back_pain", "fever", "lethargy", "polydipsia"},
        "description": "Pyelonephritis is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "下部尿路疾患からの上行性腎臓細菌感染です。",
        "urgency": "high",
        "recommended_tests": ["urinalysis", "urine_culture", "renal_ultrasound"],
        "causes": "Caused by ascending bacterial infection from the lower urinary tract reaching the renal pelvis, often secondary to cystitis or urolithiasis.",
        "causes_ja": "デグーにおける腎盂腎炎の原因: 下部尿路疾患からの上行性腎臓細菌感染です。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "腎盂腎炎はデグーにおける細菌感染症である。病原菌は付着因子を通じて組織にコロニーを形成し、毒素産生、酵素分泌、免疫回避戦略などの病原性メカニズムを介して侵入する。好中球浸潤、サイトカイン放出、補体活性化を含む炎症カスケードが生じる。組織損傷は細菌の直接作用と宿主の炎症反応の両方に起因する。菌種と宿主の免疫状態に応じて、膿瘍形成、敗血症、または慢性肉芽腫性炎症が発生しうる。",
        "treatment": "Urine culture and sensitivity BEFORE starting antibiotics (cystocentesis preferred for uncontaminated sample). Empiric antibiotics pending culture: enrofloxacin 5-10 mg/kg PO/SC q12h or trimethoprim-sulfa 15-30 mg/kg PO q12h (AVOID oral beta-lactams — fatal dysbiosis in hindgut fermenters). Treatment duration: minimum 4-6 weeks for pyelonephritis (longer than simple cystitis). Fluid therapy: warmed lactated Ringer's 10-15 mL/kg SC q8-12h to maintain renal perfusion and correct dehydration. Pain management: meloxicam 1-2 mg/kg PO/SC q24h (use cautiously with renal compromise — monitor BUN/creatinine, limit to 3-5 days if GFR reduced). Nutritional support: syringe feeding with Critical Care for Herbivores if anorexic. Monitor renal parameters (BUN, creatinine, electrolytes) q3-7 days during treatment. Repeat urine culture 5-7 days after starting antibiotics and 1 week post-completion to confirm clearance. Renal ultrasound to assess for pyelectasia, abscess formation, or concurrent urolithiasis. Address predisposing factors: urolithiasis removal, improve hygiene, increase water intake.",
        "treatment_ja": "抗菌薬開始前に尿培養・感受性試験（膀胱穿刺による無汚染サンプル推奨）。培養結果待ちの経験的抗菌薬: エンロフロキサシン 5-10mg/kg PO/SC q12h、またはトリメトプリム-スルファ 15-30mg/kg PO q12h（経口βラクタム系は禁忌 — 後腸発酵動物で致死的ディスバイオーシス）。治療期間: 腎盂腎炎は最低4-6週間（単純性膀胱炎より長い）。輸液: 加温乳酸リンゲル液 10-15mL/kg SC q8-12h（腎灌流維持・脱水補正）。疼痛管理: メロキシカム 1-2mg/kg PO/SC q24h（腎障害時は慎重使用 — BUN/クレアチニンモニタリング、GFR低下時は3-5日に制限）。食欲廃絶時はシリンジ給餌（草食動物用クリティカルケア）。腎パラメータ（BUN、クレアチニン、電解質）をq3-7日でモニタリング。抗菌薬開始5-7日後と終了1週間後に尿培養再検で除菌確認。腎エコーで腎盂拡張、膿瘍形成、併存尿石症を評価。素因への対処: 尿石症の除去、衛生環境改善、飲水量増加。",
        "prevention": "Maintain clean cage environment with regular bedding changes. Ensure adequate water intake. Treat lower urinary tract infections promptly and completely. Monitor for and manage urolithiasis. Regular urinalysis in at-risk animals (older, diabetic, history of UTI). Avoid immunosuppressive stressors.",
        "prevention_ja": "清潔なケージ環境の維持（定期的な床材交換）。十分な飲水量の確保。下部尿路感染症の迅速かつ完全な治療。尿石症のモニタリングと管理。リスク動物（高齢、糖尿病、UTI既往）の定期的尿検査。免疫抑制的ストレスの回避。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "腎盂腎炎の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Urethral Obstruction",
        "name_ja": "尿道閉塞",
        "symptoms": {"abdominal_pain", "lethargy", "straining_to_urinate", "vocalization"},
        "description": "Urethral Obstruction involves blockage of a body passage or organ requiring intervention to restore normal flow.",
        "description_ja": "結石による尿道の閉塞で排尿不能。完全閉塞は生命を脅かします。",
        "urgency": "emergency",
        "recommended_tests": ["physical_exam", "abdominal_xray", "urinalysis"],
        "causes": "Caused by urinary calculi lodging in the urethra, preventing urination. Complete obstruction is a life-threatening emergency requiring immediate intervention.",
        "causes_ja": "デグーにおける尿道閉塞の原因: 結石による尿道の閉塞で排尿不能。完全閉塞は生命を脅かします。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "尿石・結晶・粘液栓が尿道に嵌頓し、尿の流出が機械的に閉塞される。デグーは草食性で食事性カルシウムを効率的に吸収し腎から排泄するため尿が結晶化しやすく、結石形成の素因となる。閉塞により膀胱が過伸展し、背圧が尿管・腎へ伝わって腎後性高窒素血症を生じ、排泄されないカリウムの蓄積による高カリウム血症で致死的となりうる。雄は尿道が細く屈曲するため閉塞しやすく、膀胱破裂・尿毒症に至る緊急疾患で、閉塞解除と全身状態の補正を要する。",
        "treatment": "Stabilization with IV fluids, pain management, radiographic assessment. Surgical intervention (enterotomy/gastrotomy) for confirmed obstruction. Post-operative monitoring for dehiscence, peritonitis, and ileus.",
        "treatment_ja": "緊急処置: 輸液療法（乳酸リンゲル液 10mL/kg SC/IP）でショック管理と高カリウム血症の補正。膀胱穿刺（経皮的: 25G針で一時的減圧）が必要な場合あり。尿道カテーテル挿入を試みる（デグーの体格では非常に困難）。外科的尿道切開術/膀胱切開術による結石摘出が根治的治療。疼痛管理: ブプレノルフィン 0.05-0.1mg/kg SC q8-12h + メロキシカム 0.2-0.5mg/kg PO q24h。抗菌薬（エンロフロキサシン 5-10mg/kg PO/SC q12h）。高カリウム血症が重度の場合はカルシウムグルコン酸 50-100mg/kg IP。術後は食事改善（低カルシウム食）と水分摂取促進。糖尿病の併存時はその管理も並行。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "尿道閉塞の予防: 定期的な健康診断。適切な栄養管理。ストレスの軽減。清潔な飼育環境の維持。異常の早期発見・早期受診。",
        "prognosis": "Good with timely surgical intervention. Delayed treatment increases risk of intestinal necrosis, perforation, and peritonitis, which carry a guarded to poor prognosis.",
        "prognosis_ja": "尿道閉塞の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Ovarian Cysts",
        "name_ja": "卵巣嚢胞",
        "symptoms": {"abdominal_distension", "behavioral_changes", "hair_loss", "vulvar_swelling"},
        "description": "Ovarian Cysts is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "未避妊の雌のホルモン障害と両側性脱毛を引き起こす液体で満たされた卵巣嚢胞です。",
        "urgency": "moderate",
        "recommended_tests": ["abdominal_ultrasound", "hormone_panel", "physical_exam"],
        "causes": "Multifactorial etiology including infectious, environmental, immune, and host-related factors. Specific risk factors and triggers vary by individual case.",
        "causes_ja": "デグーにおける卵巣嚢胞の原因: 未避妊の雌デグーにおけるホルモンバランス異常が主因。加齢に伴う卵巣機能の変化、持続的な性ホルモン刺激、遺伝的素因が嚢胞形成を促進する。繁殖歴のない高齢雌で発症リスクが高い。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "卵巣嚢胞はデグーにおける生殖器疾患である。未避妊の雌デグーでは、卵胞の正常な排卵・退縮が障害されると液体貯留性の嚢胞が形成される。嚢胞からのエストロゲン持続分泌により、両側性の対称性脱毛、外陰部腫脹、行動変化が生じる。嚢胞の増大に伴い腹部膨満が認められ、他の腹腔内臓器への圧迫や、まれに嚢胞破裂による腹膜炎を引き起こしうる。",
        "treatment": "MEDICAL MANAGEMENT (initial): GnRH agonist deslorelin (Suprelorin) 4.7 mg SC implant (lasts 3-6 months in rodents)—induces initial FSH surge followed by pituitary downregulation, reducing estrogen production. Response rate 50-70% in small rodents; monitor clinical signs (vulvar swelling, hair loss resolution) monthly. hCG 500-1,000 IU/kg IM once (triggers ovulation if FSH-responsive cysts)—use 10-14 days after deslorelin injection or if cysts are confirmed FSH-responsive. Percutaneous needle aspiration (18-22 gauge needle under ultrasound) for temporary cyst decompression if rapid clinical deterioration; provides 1-3 weeks symptomatic relief only. SURGICAL MANAGEMENT (definitive): Emergency ovariohysterectomy (OVE) recommended for large/rapidly enlarging cysts, cyst rupture, or medical failure. PRE-OPERATIVE ASSESSMENT CRITICAL: blood glucose measurement mandatory (degus have 30-50% diabetes predisposition; >150 mg/dL = significant anesthetic risk), liver panel, creatinine (anesthetic drug metabolism). Fasting 4-6 hours pre-op. ANESTHESIA: isoflurane chamber induction preferred (avoid handling stress in small bodies); if injectable required, dexmedetomidine 2-3 μg/kg IM + isoflurane (lower dex dose due to body weight 300-350g; titrate to effect). Warm IV fluids (LRS 20-30 mL/kg/day) at body temperature (37°C). Maintain temperature 28-32°C (degus metabolically active but small mass = rapid heat loss). SURGICAL TECHNIQUE: ventral midline laparotomy (1.5-2.0 cm incision in 300g animal), identify both ovaries and uterine horns, ligate ovarian and uterine vessels (suture tie with 5-0 or 6-0 absorbable suture), excise ovaries and uterus, close fascia (5-0 absorbable), skin with tissue adhesive or 6-0 absorbable suture. Surgery time <15 minutes critical (anesthesia complications increase exponentially >15 min in degus). POST-OPERATIVE: meloxicam 0.3-0.5 mg/kg SC q24h × 5-7 days (NOT buprenorphine—opioids risk GI stasis in degus); blood glucose monitoring q2h × 24h (post-operative stress hyperglycemia common; insulin may be needed transiently), enrofloxacin 10-15 mg/kg SC/PO q12h × 10-14 days, timothy hay ad libitum immediately post-op (GI stasis prevention critical), probiotics (FortiFlora 250 mg/kg/day × 14 days). IV/SC fluids: LRS 15-25 mL/kg/day × 48-72h depending on urine output. Strict isolation from other animals 5-7 days post-op (stress increases metabolic complications). MONITORING: daily temperature (fever = infection), abdominal incision (watch for swelling, discharge), appetite (anorexia indicates serious complication), blood glucose daily × 7 days if pre-operative glucose abnormal.",
        "treatment_ja": "医学的管理（初期）：GnRHアゴニスト デスロレリン（スプレソリン）4.7 mg SC インプラント（げっ歯類で3-6ヶ月効果）—初期FSH上昇その後下垂体ダウンレギュレーション、エストロゲン産生低下。応答率50-70%；月1回臨床症状（外陰腫脹、脱毛解決）監視。hCG 500-1,000 IU/kg IM 1回（デスロレリン後10-14日またはFSH応答嚢胞確認時）。経皮針吸引（18-22ゲージ針、超音波下）で迅速臨床悪化時一時的嚢胞減圧；1-3週間症状緩和のみ。外科管理（根治）：大型/急速増大嚢胞、嚢胞破裂、医学的失敗時に緊急OVE推奨。術前評価重大：血糖測定必須（デグーは30-50%糖尿病素因；>150 mg/dL=有意な麻酔リスク）、肝機能パネル、クレアチニン。絶食4-6時間。麻酔：イソフルラン吸入導入推奨（小体の取扱いストレス回避）；注射が必要な場合、デクスメデトミジン2-3 μg/kg IM + イソフルラン（低デックス用量、体重300-350g；効果に滴定）。温かいIV輸液（乳酸リンガー20-30 mL/kg/日）体温（37°C）。温度28-32°C維持。外科技術：腹部正中線開腹（300g動物で1.5-2.0 cm切開）、両側卵巣と子宮角同定、卵巣と子宮血管結紮（5-0または6-0吸収性縫合糸）、卵巣と子宮切除、筋膜閉鎖（5-0吸収性）、皮膚は組織接着剤または6-0吸収性縫合糸。手術時間<15分重大。術後：メロキシカム0.3-0.5 mg/kg SC q24h × 5-7日、血糖監視q2h × 24時間、エンロフロキサシン10-15 mg/kg SC/PO q12h × 10-14日、チモシーヘイ無制限即座、プロバイオティクス。IV/SC輸液：乳酸リンガー15-25 mL/kg/日 × 48-72時間。厳密隔離5-7日。監視：毎日体温、腹部切開部位、食欲、血糖（異常時）。",
        "prevention": "CRITICAL PREVENTION (100% effective if performed): 1) SPAY all females not intended for breeding by age 12-18 months (before ovarian pathology develops); ovarian cysts essentially eliminated post-spay. Breeding females spay by age 3-4 years maximum (risk increases exponentially >3 years). 2) WEIGHT MANAGEMENT (unique to degus—diabetes linkage): maintain optimal weight 300-350g pre-breeding, maximum 400g (obesity >400g dramatically increases dystocia, endometritis, AND metabolic cyst formation). Monthly weight monitoring critical. Avoid high-calorie treats; timothy hay, limited pellets (15-20 g/kg/day), restricted fruit (1-2x weekly). 3) BREED SELECTION: select females with normal estrous cycles (4-5 day swelling only); avoid females with prolonged/irregular vulvar swelling (estrogen dysregulation predictor). Family history of diabetes or ovarian pathology = breeding exclusion criterion. 4) BREEDING MANAGEMENT: restrict breeding to 2-3 litters lifetime (repeated estrogen surges increase cyst risk; degus with >3 litters 60% higher ovarian disease incidence). Breed females only age 6-36 months (optimal window; avoid >36 months when estrogen sensitivity increases). 5) GLUCOSE MONITORING in intact females: random blood glucose checks at annual veterinary visits (normal <100 mg/dL fasting, <150 mg/dL non-fasting); >110 mg/dL fasting = pre-diabetes warning (cyst risk increases). 6) STRESS REDUCTION: minimize cage disturbance during estrous cycles (vulvar swelling indicates hormonal sensitivity), maintain cool temperature (15-22°C—heat stress worsens metabolic hormonal dysregulation), avoid overcrowding. 7) QUARTERLY ULTRASOUND SCREENING if breeding colony (females age 18-36 months): detect cysts <10 mm before symptoms; early intervention prevents rupture/complications. 8) POSTPARTUM MONITORING: monthly abdominal palpation first 2 years post-breeding to detect enlargement early (asymmetric ovaries = abnormal). 9) AVOID PROGESTERONE-ONLY CONTRACEPTIVES in degus (data sparse; megestrol acetate and levonorgestrel contraindicated due to dysbiosis risk).",
        "prevention_ja": "重大予防（100%有効—実行時）：1) 育種意図なし全雌を12-18ヶ月齢までに避妘（卵巣病理発展前）；卵巣嚢胞本質的に避妘後消失。育種雌は3-4年齢最大時に避妘（リスク>3年齢で指数関数的増加）。2) 体重管理（デグー固有—糖尿病連携）：最適体重300-350g育種前、最大400g（肥満>400g劇的に難産増加、子宮内膜炎、代謝嚢胞形成）。月1回体重監視重大。高カロリーおやつ回避；チモシーヘイ、限定ペレット（15-20 g/kg/日）、制限フルーツ（週1-2回）。3) 繁殖選択：正常発情周期の雌選択（4-5日腫脹のみ）；延長/不規則外陰腫脹回避（エストロゲン不調和予測）。糖尿病または卵巣病理の家族歴=育種除外基準。4) 育種管理：生涯2-3産仔に限定（繰り返すエストロゲンサージ嚢胞リスク増加；>3産仔デグーは卵巣疾患60%高い）。育種雌のみ6-36ヶ月齢（最適窓；>36ヶ月回避エストロゲン感受性増加時）。5) 完全雌での血糖監視：年1回獣医訪問でランダム血糖チェック（正常<100 mg/dL絶食、<150 mg/dL非絶食）；>110 mg/dL絶食=前糖尿病警告（嚢胞リスク増加）。6) ストレス低減：発情周期中ケージ物乱最小化、温度15-22°C維持、過密回避。7) 四半期超音波スクリーニング育種植民地で（雌18-36ヶ月齢）：嚢胞<10 mm症状前検出；早期介入破裂/合併症予防。8) 産後監視：月1回腹部触診育種後最初2年で早期腫大検出。9) デグーのプロゲステロン単独避妊薬回避。",
        "prognosis": "EXCELLENT with early OVE (>95% cure rate in degus <3 years); POOR without intervention. Medical management success rate 50-70% (cyst recurrence 60-80% within 6-12 months if ovaries retained). Surgical OVE: 95%+ cure if performed <2 hours from anesthesia induction (most degus tolerate brief anesthesia well given strict temperature control and glucose monitoring). CRITICAL RISK FACTORS for surgical mortality: pre-operative blood glucose >150 mg/dL (3-4× increased mortality risk; pre-operative insulin or dextrose titration may be needed), age >4 years (anesthetic complications increase), obesity >400g (anesthetic drug metabolism unpredictable; dosing errors common), pre-existing liver/kidney disease. Rupture risk without treatment: 5-10% spontaneous cyst rupture (mortality 30-50% from peritonitis + septic shock). Degus deteriorate rapidly once ruptured due to small body mass (300-350g) and high metabolic rate; endotoxin load quickly becomes lethal. Recurrence WITHOUT OVE: 60-80% (all survivors develop persistent or recurrent cysts within 6-12 months if both ovaries retained). Post-operative fertility: eliminated after OVE (expected, non-breeding procedure). Lifespan expectation post-OVE: unaffected (no difference vs spayed colony; 5-8 year potential).",
        "prognosis_ja": "卵巣嚢胞の予後：早期OVEで優秀（>95%治癒率デグー<3年齢）；介入無しで不良。医学的管理成功率50-70%（>60%再発6-12ヶ月以内）。外科OVE：95%+治癒率<2時間麻酔導入（厳密温度制御と血糖監視で）。重大手術死亡リスク因子：術前血糖>150 mg/dL（3-4×死亡リスク増加）、年齢>4年（麻酔合併症）、肥満>400g、既存肝/腎疾患。破裂リスク無治療：5-10%自然嚢胞破裂（死亡率30-50%腹膜炎+敗血症ショック）。デグー急速悪化小体格（300-350g）と高代謝；エンドトキシン負荷迅速に致死。再発OVE無し：60-80%。術後受胎率：消失OVE後。寿命予期術後：未影響（避妘植民地との差なし；5-8年可能性）。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Endometritis",
        "name_ja": "子宮内膜炎",
        "symptoms": {"appetite_loss", "fever", "lethargy", "vaginal_discharge"},
        "description": "Endometritis is acute inflammation and bacterial infection of the uterine endometrium, often postpartum or secondary to hormonal imbalances. Progresses to pyometra within 48-96 hours if untreated. Degus show high susceptibility to septic shock due to precocial large fetuses and maternal obesity risk.",
        "description_ja": "子宮内膜の炎症と感染で、子宮蓄膿症に進行する可能性があります。デグーは妊娠と産後に高い敗血症ショックリスク。",
        "urgency": "high",
        "recommended_tests": [
            "abdominal_ultrasound",
            "vaginal_cytology",
            "blood_chemistry",
            "culture_sensitivity",
            "complete_blood_count",
        ],
        "causes": "Bacterial colonization of the uterine endometrium, often postpartum (retained placenta, dystocia trauma) or secondary to hormonal imbalances (prolonged estrus, ovarian cysts). Common bacteria: Staphylococcus aureus, E. coli, Pasteurella multocida, Streptococcus spp., Enterococcus. Risk factors: multiparous females (>3-4 litters), maternal obesity (pelvic narrowing increases dystocia risk), dystocia history, poor hygiene, stress, immune suppression, inadequate nutrition (calcium/vitamin C deficiency). Degus have precocial young (fully furred) requiring large gestational investment; postpartum endometrial stress high.",
        "causes_ja": "デグーにおける子宮内膜炎の原因：産後細菌コロニー化（胎盤貯留、難産外傷）またはホルモン不均衡に二次的（延長発情、卵巣嚢胞）。黄色ブドウ球菌、E. coli、多様性パスツレラ、連鎖球菌、腸球菌が最多。危険因子：多産雌（>3-4産仔）、母体肥満（骨盤狭窄で難産リスク増加）、難産既往、不衛生、ストレス、免疫抑制、栄養不足（カルシウム/ビタミンC欠乏）。デグーは早成性新仔（完全に毛皮）で大きな妊娠投資を要求；産後子宮内膜ストレス高い。",
        "pathophysiology": "Endometritis develops when bacteria colonize the endometrium, triggering acute inflammatory cascade: endotoxins (LPS) → neutrophil infiltration → cytokine release (TNF-α, IL-6, IL-8) → endometrial edema/hyperemia. Myometrial contractions attempt clearance but impaired by endotoxemia. In degus, postpartum endometrium is especially vulnerable due to precocial neonate burden: large fetuses (precocial young with full development) cause extensive placental implantation sites. If untreated >48-96 hours, endometritis progresses to closed-type pyometra (no drainage)→explosive sepsis. Degus show high susceptibility to obstetric shock (20-30% mortality even with treatment of dystocia)—endometritis risk mirrors this vulnerability.",
        "pathophysiology_ja": "子宮内膜炎はデグーにおける生殖器疾患で、細菌が子宮内膜にコロニー化して急性炎症カスケード発動。エンドトキシン（LPS）→好中球浸潤→サイトカイン放出（TNF-α、IL-6、IL-8）→子宮内膜浮腫/充血。筋層収縮が排液を試みるがエンドトキシム血症で障害。デグーでは産後子宮内膜が特に脆弱（早成性新仔負荷：大型胎児で広範な胎盤着床部位）。無治療で>48-96時間、子宮内膜炎が閉鎖型子宮蓄膿症に進行→爆発的敗血症。デグーは産科ショック易感受性を示す（難産でも治療時20-30%死亡率）—子宮内膜炎リスクがこの脆弱性を反映。",
        "treatment": "EARLY MEDICAL MANAGEMENT (optimal if caught within 24-48 hours before pyometra develops): IV crystalloid fluids (LRS 50-100 mL/kg bolus), analgesia (meloxicam 0.3-0.5 mg/kg SC q24h × 5-7 days), broad-spectrum antibiotics (NO β-LACTAMS—fatal dysbiosis in degus): Enrofloxacin 10-15 mg/kg PO/SC q12h × 14-21 days (first-line) OR trimethoprim-sulfamethoxazole (TMS) 30 mg/kg PO q12h × 14-21 days. Add metronidazole 20 mg/kg PO q12h × 10-14 days (anaerobic coverage). Vitamin C 50-100 mg/kg/day SC/PO (degus synthesize C but stress depletes). Hepatic support: silymarin 20-40 mg/kg/day PO × 14 days. Culture sensitivity testing essential—adjust antibiotics based on results. Uterine drainage: if ultrasound shows significant purulent accumulation (>5 mm), consider transcervical flush (0.9% saline via small catheter under sedation) to remove uterine contents. CRITICAL MONITORING: daily temperature (fever resolution expected within 3-5 days), vaginal discharge character (should clear), blood work at days 7 and 14 (WBC normalization). Persistent fever >5 days or worsening discharge = treatment failure→EMERGENCY OVE. SURGICAL MANAGEMENT (if medical management fails or closed-type pyometra suspected): Emergency OVE under isoflurane anesthesia (see Pyometra entry for anesthesia protocol). Post-operative: continue IV fluids, antibiotics, analgesia × 10-14 days post-op.",
        "treatment_ja": "早期医学的管理（最適—子宮蓄膿症発展前24-48時間で捕捉時）：IV結晶質輸液（乳酸リンガー50-100 mL/kg bolus）、鎮痛（メロキシカム0.3-0.5 mg/kg SC q24h × 5-7日）、広域抗菌薬（βラクタム禁止—デグーで致死的dysbiosis）：エンロフロキサシン10-15 mg/kg PO/SC q12h × 14-21日（第一選択）OR TMS 30 mg/kg PO q12h × 14-21日。メトロニダゾール20 mg/kg PO q12h × 10-14日を追加。ビタミンC 50-100 mg/kg/日 SC/PO。肝臓支持：シリマリン20-40 mg/kg/日 PO × 14日。培養感受性試験必須。子宮排液：超音波で著しい化膿性蓄積（>5 mm）を示す場合、経頸部洗浄（0.9%生食小カテーテル、鎮静下）で子宮内容物除去を考慮。重大監視：毎日体温（発熱解決予期3-5日以内）、膣分泌物文字（明白で）、血液検査（好中球正常化）。発熱遷延>5日または悪化分泌物=治療失敗→緊急OVE。外科管理：イソフルラン麻酔下緊急OVE（子宮蓄膿症エントリ参照）。術後：IV輸液、抗菌薬、鎮痛を × 術後10-14日継続。",
        "prevention": "CRITICAL PREVENTION: 1) Spay all females not intended for breeding by 12 months age (prevents estrogen-induced endometrial damage, obstetric complications). 2) Maintain strict hygiene: clean bedding daily (aspen/paper-based, NOT cedar/pine), spot-clean soiled areas, disinfect cage biweekly. 3) Optimize nutrition: vitamin C 50-100 mg/kg/day (immune support; degus synthesize C but stress depletes), calcium 1,000-1,500 mg/kg diet, quality timothy hay unlimited. 4) Weight management: CRITICAL in degus—maintain pre-breeding weight 300-350g (avoid obesity; >400g = high dystocia/endometritis risk). 5) Stress reduction: minimize handling of intact females, maintain cool temperature (15-22°C—heat increases metabolic stress in degus), avoid overcrowding. 6) Monitor breeding females: monthly abdominal palpation, quarterly ultrasound if >18 months old (detect early endometrial changes). 7) Prompt postpartum care: monitor placental passage (complete within 24h post-parturition), watch for vaginal discharge (clear mucus <48h normal; purulent discharge = endometritis). 8) Avoid prolonged estrus cycles: degus with extended genital swelling (>4-5 days) may develop estrogen toxicity and secondary endometrial damage—ovarian ultrasound assessment needed. 9) Mandatory OVE post-treatment (60-80% recurrence risk if attempt rebreeding without OVE).",
        "prevention_ja": "重大予防：1) 12ヶ月齢までに育種意図なし全雌を避妘。2) 厳密衛生管理：毎日清潔床材、汚れた部位spot-clean、隔週ケージ消毒。3) 栄養最適化：ビタミンC 50-100 mg/kg/日、カルシウム1,000-1,500 mg/kg食、チモシーヘイ無制限。4) 体重管理：デグーで重大—育種前体重300-350g（肥満回避；>400g=高難産/子宮内膜炎リスク）。5) ストレス低減：避妘されない雌取扱い最小化、温度15-22°C、過密防止。6) 育種雌監視：月1回腹部触診、>18ヶ月齢なら四半期超音波。7) 迅速産後管理：胎盤脱出監視（完全<24時間）、膣分泌物監視（透明粘液<48時間正常；化膿性=子宮内膜炎）。8) 延長発情周期回避：延長外陰腫脹（>4-5日）のデグーはエストロゲン毒性と二次子宮内膜損傷の可能性—卵巣超音波評価必要。9) 回復後OVE必須（再発リスク60-80%）。",
        "prognosis": "GUARDED to GOOD if medical management initiated within 24-48 hours: success rate 60-75% with appropriate antibiotics. Fever resolution within 3-7 days = good prognostic sign. If endometritis persists >5-7 days or converts to pyometra: prognosis becomes POOR (see Pyometra—mortality 80-95% without OVE, <8% with medical management). Degus deteriorate rapidly due to precocial fetal burden and obesity predisposition; small body mass (300-350g typical) means endotoxin load rapidly causes systemic effects. Recurrence risk without OVE: 60-80% (all survivors develop pyometra or repeat endometritis within 6-12 months). Mandatory OVE post-recovery (endometrial damage is permanent; future pregnancy risks life-threatening pyometra). Fertility lost after endometritis (endometrial scarring prevents implantation).",
        "prognosis_ja": "子宮内膜炎の予後：慎重〜良好—医学的管理を24-48時間以内に開始した場合：成功率60-75%。発熱解決3-7日以内=良好予後。子宮内膜炎遷延>5-7日または子宮蓄膿症転換の場合：予後不良（子宮蓄膿症参照—OVEなし死亡率80-95%）。デグーは早成性胎児負荷と肥満素因で急速悪化；小体格（典型300-350g）でエンドトキシン負荷が急速に全身効果。OVE無し再発リスク：60-80%。回復後OVE必須。受胎率喪失。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Pregnancy Toxemia",
        "name_ja": "妊娠中毒症",
        "symptoms": {"appetite_loss", "lethargy", "rapid_breathing", "seizures", "weakness"},
        "description": "Pregnancy toxemia in degus is a metabolic emergency in late pregnancy (day 85+) or early lactation caused by negative energy balance. Complicated by degu predisposition to diabetes: pregnancy toxemia can unmask subclinical diabetes or trigger overt hyperglycemia in susceptible individuals (20-30% of captive degus are diabetes-prone).",
        "description_ja": "デグーの妊娠毒血症は妊娠後期（85日以上）または産後初期の代謝緊急事態で、負のエネルギーバランスが原因。デグーは糖尿病易発性があり（飼育下デグーの20-30%が糖尿病易発）、妊娠毒血症が不顕性糖尿病を顕性化させたり易感受性個体で顕性高血糖を誘発しうる。",
        "urgency": "emergency",
        "recommended_tests": ["blood_glucose", "blood_chemistry", "blood_gas", "urine_ketones", "HbA1c"],
        "causes": "Negative energy balance in late pregnancy or lactation, exacerbated by obesity (primary risk factor; >25% above ideal weight dramatically increases risk), inadequate pre-pregnancy nutrition, large litter size (high milk demand), stress from dystocia, or rapid weight loss post-partum. Degus cannot metabolize simple sugars effectively—dietary fruit/sugar intake during pregnancy worsens metabolic stability. Subclinical diabetes or borderline glucose intolerance may manifest as toxemia during pregnancy metabolic stress.",
        "causes_ja": "妊娠後期または乳汁分泌期の負のエネルギーバランス。肥満が悪化因子（最大リスク；理想体重の>25%超過で劇増）。育種前栄養不良、大産仔数（高乳汁需要）、難産ストレス、または産後急速体重低下。デグーは単純糖の代謝が効率的でない—妊娠中の食事果実/砂糖摂取が代謝安定性悪化。不顕性糖尿病または境界線糖耐性が妊娠代謝ストレス時に毒血症として顕現化しうる。",
        "pathophysiology": "During late pregnancy and lactation, degu metabolic demands exponentially increase. If hepatic gluconeogenesis cannot match demand, animals increasingly rely on ketone metabolism (β-hydroxybutyrate, acetoacetate, acetone production). In degu diabetes-prone individuals, concurrent insulin dysfunction exacerbates hyperglycemia and impairs ketone metabolism, creating dual metabolic crisis: hypoglycemic and ketotic simultaneously, or hyperglycemic-ketotic if insulin-insufficient. Metabolic acidosis develops (pH <7.25 = severe), triggering neurological dysfunction, seizures, and potential cardiovascular collapse within 24-48 hours.",
        "pathophysiology_ja": "妊娠後期と乳汁分泌期、デグー代謝需要は指数関数的増加。肝性糖新生が需要に応じられなければケトン代謝に依存（β-ヒドロキシ酪酸、アセト酢酸、アセトン産生）。デグー糖尿病易発個体では、併存インスリン機能障害で高血糖が悪化し、ケトン代謝が障害され、双方代謝危機：低血糖ケトーシス同時または高血糖ケトーシス（インスリン不足時）。代謝性アシドーシス発生（pH <7.25 = 重症）で神経機能障害・けいれん・24-48時間内に心血管虚脱。",
        "treatment": "EMERGENCY INTERVENTION: 1) GLUCOSE SUPPORT: IV dextrose 50% bolus (0.5-1.0 g/kg IV rapid), THEN 5% dextrose continuous infusion (50-100 mL/kg/day × 24-48 hours). Monitor blood glucose q4h target 100-150 mg/dL (higher target than other species due to degu diabetes tendency). 2) AGGRESSIVE SYRINGE FEEDING: q3-4h with high-energy, SUGAR-FREE food (timothy hay paste, vegetable puree—NOT fruit, avoid all sugars), minimum 100 kcal/kg/day × 5-7 days. CRITICAL: NEVER offer fruit, honey, or sugary treats during recovery. 3) SUPPORTIVE FLUIDS: IV or SC lactated Ringer's 50-100 mL/kg/day × 48-72h for acidosis and electrolyte correction. Monitor electrolytes q12h. 4) VITAMIN C SUPPLEMENTATION: Ascorbic acid 100 mg/kg SC/PO q12h × 5-7 days (degus cannot synthesize vitamin C; stress and lactation deplete reserves). 5) PAIN MANAGEMENT: Meloxicam 0.3-0.5 mg/kg SC q12h × 5 days. 6) METABOLIC MONITORING: Blood glucose q4h (target 100-150 mg/dL, avoid both hypoglycemia and hyperglycemia), blood gas/electrolytes q12h (pH >7.25 indicates improving acidosis), urine ketones daily, HbA1c at 1 week post-recovery (screen for underlying diabetes). 7) DIABETES SCREENING: If hyperglycemia (>200 mg/dL) develops despite treatment, consider concurrent diabetes mellitus—may require long-term insulin therapy post-recovery. 8) OBSTETRIC: If near term and rapidly deteriorating, emergency cesarean under isoflurane may be lifesaving.",
        "treatment_ja": "緊急対応：1) ブドウ糖支持：50%デキストロース急速ボーラス（0.5-1.0 g/kg IV 急速）THEN 5%デキストロース継続IV（50-100 mL/kg/day × 24-48時間）。血糖 q4h モニタリング目標 100-150 mg/dL（デグー糖尿病傾向で他種より高目標）。2) 積極的シリンジ給餌：q3-4h で高エネルギー無砂糖食（ティモシーヘイペースト、野菜ピュレ—果実なし、全砂糖回避）、最小100 kcal/kg/day × 5-7日。重大：回復中は果実・蜂蜜・甘い食べ物禁止。3) 支持輸液：IV or SC 乳酸リンガー 50-100 mL/kg/day × 48-72h でアシドーシス・電解質異常是正。電解質 q12h モニタリング。4) ビタミンC補充：アスコルビン酸 100 mg/kg SC/PO q12h × 5-7日（デグーはビタミンC 合成不可；ストレス・乳汁分泌で枯渇）。5) 鎮痛：メロキシカム 0.3-0.5 mg/kg SC q12h × 5日。6) 代謝モニタリング：血糖 q4h（目標100-150 mg/dL、低血糖と高血糖両方回避）、血液ガス/電解質 q12h（pH >7.25 = アシドーシス改善）、尿ケトン日1回、HbA1c 1週後（糖尿病潜在性スクリーニング）。7) 糖尿病スクリーニング：治療にもかかわらず高血糖（>200 mg/dL）発症時は併存糖尿病を検討—産後長期インスリン療法必要な場合あり。8) 産科的：妊娠末期で急速悪化時、緊急帝王切開（イソフルラン麻酔）は生命救助可能。",
        "prevention": "CRITICAL PREVENTION: 1) Weight management: maintain pre-breeding weight 180-220g (obesity is PRIMARY RISK FACTOR; >240g at breeding contraindication). 2) Breeding age: 3-6 months only (avoid late-age breeding; first breeding should occur <6 months). 3) PRE-BREEDING NUTRITION CRITICAL: timothy hay ad libitum, balanced pellets 15-20g/day WITHOUT fruit/treats, vitamin C 100+ mg/kg/day (mandatory—degus require exogenous vitamin C), calcium 1-1.5%, NO SUGARS of any kind (degus are genetically poor glucose metabolizers). 4) PREGNANCY DIET: increase pellets to 20-25g/day, CONTINUE to avoid all fruits/sugars, maintain vitamin C supplementation. 5) Large litter size minimization: avoid breeding large males with large females. 6) Pre-breeding glucose screening: HbA1c or random fasting glucose in suspected diabetes-prone individuals (family history of diabetes). If HbA1c >5.5% or glucose >120 mg/dL fasting, defer breeding—spay if not intended for breeding. 7) Stress minimization during late pregnancy (reduce handling, maintain 65-75°F). 8) Immediate dystocia intervention (increases toxemia risk 3-5×).",
        "prevention_ja": "重大な予防：1) 体重管理：育種前体重 180-220g 維持（肥満が最大リスク因子；>240g は育種禁忌）。2) 育種年齢：3-6ヶ月齢のみ（遅延育種回避；初回育種は <6ヶ月）。3) 育種前栄養重大：ティモシーヘイ給与量制限なし、バランスペレット 15-20g/日（果実/食べ物なし）、ビタミンC 100+ mg/kg/日（必須—デグーは外因性ビタミンC必要）、カルシウム 1-1.5%、砂糖禁止（デグー遺伝的糖代謝不良）。4) 妊娠食：ペレット 20-25g/日に増量、全果実/砂糖回避継続、ビタミンC補充継続。5) 大産仔数最小化：大雄と大雌交配回避。6) 育種前血糖スクリーニング：糖尿病易発疑い個体で HbA1c または空腹時ランダム血糖。HbA1c >5.5% または空腹時血糖 >120 mg/dL なら育種延期—育種予定ないなら避妊。7) 妊娠後期ストレス最小化（取扱い軽減、温度 65-75°F 維持）。8) 直ちの難産介入（毒血症リスク 3-5倍）。",
        "prognosis": "40-60% mortality if untreated or delayed >24 hours. With immediate emergency intervention (IV glucose, aggressive syringe feeding, IV fluids), 50-70% survival if treatment initiated within 12 hours of symptom onset. Prognosis worsens dramatically if seizures develop (pH <7.15 on blood gas) or if concurrent hyperglycemia (>300 mg/dL) indicates unmasked diabetes—mortality >80%. Kits: if dam survives, hand-rearing may be necessary. POST-RECOVERY CRITICAL: screen dam for diabetes (HbA1c, repeat fasting glucose); if HbA1c >5.5% or glucose >120 mg/dL fasting, dam has diabetes mellitus—SPAY (40-80% recurrence risk if breeding attempted again).",
        "prognosis_ja": "無治療または遅延 >24時間で死亡率 40-60%。直ちの緊急対応（IV ブドウ糖、積極的シリンジ給餌、IV 輸液）で症状発現12時間以内の治療開始なら50-70%生存。けいれん発症（血液ガス pH <7.15）または併存高血糖（>300 mg/dL = 顕在化糖尿病）で予後劇悪化—死亡率 >80%。新仔：母体生存で人工哺乳可能。産後重大：母体の糖尿病スクリーニング（HbA1c、空腹時血糖反復）；HbA1c >5.5% または空腹時血糖 >120 mg/dL なら母体は糖尿病—避妊実施（育種再試行で40-80%再発）。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult"},
    },
    {
        "name": "Mastitis",
        "name_ja": "乳腺炎",
        "symptoms": {"appetite_loss", "fever", "mammary_redness", "mammary_swelling", "pain"},
        "description": "Mastitis in degus is post-partum bacterial infection of mammary tissue during lactation, ascending through lactiferous ducts. Dystocia complications and stress increase susceptibility. CRITICAL: Degus cannot tolerate β-lactam antibiotics (fatal GI dysbiosis); choose fluoroquinolones only.",
        "description_ja": "デグーの乳腺炎は産後授乳期の乳腺細菌感染症で、ラクティフェラスダクト経由の上行感染。難産合併症やストレスがリスク因子。重大：デグーはβラクタム抗菌薬不耐（致死的GI dysbiosis）；フルオロキノロン単独選択。",
        "urgency": "high",
        "recommended_tests": ["physical_exam", "milk_culture", "culture_sensitivity", "blood_panel"],
        "causes": "Post-partum bacterial infection (Staphylococcus aureus primary). Risk factors: dystocia complications, contaminated nesting environment, compromised nipple integrity, stress, dehydration, poor nutrition. Environmental: unsanitary bedding, excessive handling post-partum. Degus are susceptible to secondary diabetes during systemic infection stress.",
        "causes_ja": "産後黄色ブドウ球菌による上行感染（ラクティフェラスダクト経由）。危険因子：難産合併症、汚染営巣環境、乳頭損傷、ストレス、脱水、栄養不良。環境：不潔なベッディング、産後過剰取扱い。デグーは全身感染ストレス中に二次糖尿病易発。",
        "pathophysiology": "Bacteria colonize mammary tissue, triggering acute inflammatory cascade: neutrophil infiltration, cytokine release, tissue edema, abscess formation. Untreated >3-5 days, systemic spread causes bacteremia, sepsis, septic shock. Lactiferous duct blockade compounds inflammation, milk stasis promotes secondary infection. Concurrent degu metabolic stress (lactation demand) increases systemic infection risk.",
        "pathophysiology_ja": "乳腺組織への細菌コロニー形成が急性炎症カスケード（好中球浸潤、サイトカイン放出、組織浮腫、膿瘍形成）惹起。未治療 >3-5日で全身播種、敗血症、敗血症性ショック。ラクティフェラスダクト閉塞で炎症複合、乳汁貯留が二次感染促進。並存デグー代謝ストレス（乳汁分泌需要）が全身感染リスク増加。",
        "treatment": "EMPIRIC ANTIBIOTICS: Enrofloxacin 5-10 mg/kg PO q12h × 10-14 days (preferred; good mammary penetration, safe in degus). Alternative: TMS 30 mg/kg PO q12h × 10-14 days. CRITICAL: NEVER use β-lactams, macrolides (GI dysbiosis risk), or linezolid (myelo/hemato-toxicity). SUPPORTIVE CARE: warm compresses to affected glands × 10-15 min q6-8h; SC fluids if dehydrated (50-100 mL/kg/day); meloxicam 0.3-0.5 mg/kg SC q12h × 5-7 days (SC preferred—degu PO absorption unreliable when febrile). NUTRITION SUPPORT: Vitamin C 100 mg/kg/day PO (degus require exogenous vitamin C; infection/stress depletes reserves). NURSING MANAGEMENT: If pups <7 days old, supplemental syringe-feeding; if older, can wean at day 18-20. Monitor pups for diarrhea. CULTURE-GUIDED THERAPY once available (typically 2-3 days). SURGICAL INTERVENTION if abscess develops: ultrasound-guided needle aspiration or incision and drainage under brief isoflurane anesthesia, debridement of necrotic tissue, local antibiotic irrigation (enrofloxacin 10 mg/mL in sterile saline), leave drain × 3-5 days. Monitor for abscess recurrence (5-10% with needle aspiration alone).",
        "treatment_ja": "経験的抗菌薬：エンロフロキサシン 5-10 mg/kg PO q12h × 10-14日（第1選択；乳腺透過性良好、デグーで安全）。代替：TMS 30 mg/kg PO q12h × 10-14日。重大：βラクタム禁止、マクロライド禁止（GI dysbiosis リスク）、リネゾリド禁止（骨髄・血液毒性）。支持療法：患部乳腺に温湿布 × 10-15分 q6-8h；SC輸液（脱水時 50-100 mL/kg/day）；メロキシカム 0.3-0.5 mg/kg SC q12h × 5-7日（SC優先—デグーPO吸収は発熱時不安定）。栄養支持：ビタミンC 100 mg/kg/日 PO（デグーは外因性ビタミンC必要；感染/ストレスで枯渇）。授乳管理：新仔 <7日齢なら人工哺乳；老齢なら18-20日齢で離乳可。新仔下痢モニタリング。培養結果判明後（通常2-3日）は標的治療。膿瘍形成時：超音波ガイド針吸引または切開排膿（イソフルラン麻酔短時間）、壊死組織デブリードマン、局所抗菌薬灌流（エンロフロキサシン 10 mg/mL 生理食塩水）、3-5日ドレーン留置。膿瘍再発モニタリング（針吸引単独で 5-10%）。",
        "prevention": "Prevention includes meticulous periparturient hygiene (clean nesting substrate, minimal handling during labor/post-partum), adequate pre-breeding and pregnancy nutrition (vitamin C 100+ mg/kg/day MANDATORY, timothy hay ad libitum, balanced pellets WITHOUT fruits/sugars, calcium 1-1.5%), regular pre-breeding and post-parturition physical examinations with nipple assessment, prompt dystocia treatment (minimizes stress and tissue trauma), spay after weaning if recurrent mastitis (40-50% recurrence risk without spay).",
        "prevention_ja": "予防：分娩周辺期の厳密な衛生管理（清潔な営巣基質、分娩時/直後は最小限取扱い）、育種前・妊娠期の十分な栄養管理（ビタミンC 100+ mg/kg/日 必須、ティモシーヘイ給与量制限なし、バランスペレット 無果実/砂糖、カルシウム 1-1.5%）、定期的な育種前・産後身体検査と乳頭評価、難産迅速治療（ストレス・組織損傷最小化）、反復性乳腺炎では離乳後避妊（避妊なしで40-50%再発）。",
        "prognosis": "75-85% cure rate with early treatment (within 24-48 hours) and appropriate antibiotics. Prognosis worsens with delayed treatment (3-5 days: 40-60% mortality if sepsis develops); abscess complicates treatment (30-50% mortality). Septic shock carries >90% mortality. Without intervention, systemic spread occurs within 7-10 days. Pups <7 days may survive with prompt supplemental feeding if dam recovers; older pups typically wean successfully.",
        "prognosis_ja": "早期治療（発症24-48時間以内）と適切な抗菌薬で75-85%治癒率。遅延治療で予後悪化（3-5日：敗血症発症で死亡率40-60%）。膿瘍形成は治療複雑化（死亡率30-50%）。敗血症性ショックで死亡率>90%。無治療で7-10日で全身播種。新仔 <7日齢は迅速な人工哺乳で母体回復時生存可能；老齢新仔は通常離乳成功。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult"},
    },
    {
        "name": "Retained Fetus",
        "name_ja": "胎児残留",
        "symptoms": {"abdominal_distension", "fever", "lethargy", "vaginal_discharge"},
        "description": "Retained Fetus is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "分娩時にすべての子を排出できない状態で、感染と毒血症に至ります。",
        "urgency": "emergency",
        "recommended_tests": ["abdominal_xray", "abdominal_ultrasound", "physical_exam"],
        "causes": "Caused by uterine inertia, fetal malpresentation, or oversized fetuses preventing complete expulsion during parturition, leading to infection and toxemia.",
        "causes_ja": "デグーにおける胎児残留の原因: 分娩時にすべての子を排出できない状態で、感染と毒血症に至ります。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "分娩時に胎仔の一部または全部が娩出されずに子宮内に停滞する病態。子宮無力症（低カルシウム血症・肥満・高齢・栄養不良）、胎仔の過大・胎位異常、胎仔死による分娩停止が原因となる。遺残した胎仔・胎盤は子宮内で変性・ミイラ化または腐敗し、細菌感染による子宮蓄膿・子宮炎、毒素吸収による敗血症に進行する。母体は食欲廃絶・元気消失・努責を示し、放置すると致死的となるため、オキシトシンによる娩出または帝王切開を要する緊急疾患である。",
        "treatment": "EMERGENCY: Stabilize with SC/IP lactated Ringer's 10-15 mL/kg/hr (IV rarely achievable in degus; IP absorption adequate), oxygen supplementation (nasal prongs), and analgesia (buprenorphine 0.05-0.1 mg/kg SC q8-12h or meloxicam 0.2-0.5 mg/kg PO q24h). CRITICAL NOTE: Degus (300-350g body mass) progress to septic shock in 36-48 hours (faster than rabbits/guinea pigs); delays are fatal. EXTREME CAUTION with anesthesia in septic degus (increased cardiovascular collapse risk). Attempt MEDICAL management ONLY if <12 hours post-parturition: Oxytocin 0.5-2 IU/kg IM (max 2 doses, 15-30 minute intervals). Response expected within 30-60 minutes. If no response OR sepsis signs (fever, vaginal hemorrhage, lethargy, anorexia, shock signs), PROCEED TO EMERGENCY SURGICAL INTERVENTION. ANESTHESIA: Use MINIMAL dexmedetomidine (1-3 μg/kg IM only—higher doses cause severe bradycardia/collapse). Atropine 0.01-0.05 mg/kg SC 10-15 min prior. Isoflurane mask induction preferred. Emergency ovariohysterectomy (OVE) only; cesarean not recommended in septic/shock state. POST-OPERATIVE PROTOCOL: Maintain strict temperature control (15-22°C); hypothermia accelerates cardiovascular collapse in tiny animals. Keep in incubator or heat lamp. Metoclopramide 0.5-1 mg/kg SC/PO q8h × 7 days. Antibiotics: Enrofloxacin 5-10 mg/kg SC/PO q12h × 10-14 days (MANDATORY—NO β-lactams/sulfa which cause fatal dysbiosis). Consider metronidazole 10-20 mg/kg PO q12h × 5-7 days if anaerobic infection suspected. CRITICAL: ZERO sugar/fruit post-operatively for 4-6 weeks (degus have innate diabetes predisposition; surgery/sepsis induce hyperglycemia/glycosuria; monitor for diabetes insipidus/mellitus). Soft timothy hay only diet post-op. Supportive fluids SC/IP until stable. Pain management: meloxicam 0.2-0.5 mg/kg PO q24h × 7 days. Monitor blood glucose if possible (hyperglycemia common post-sepsis). Monitor for DIC (petechiae, hematuria). Transfusion rarely possible at this body mass; manage shock medically. Prognosis: 60-70% survival with OVE <36 hours + temperature management + sugar avoidance; 30-40% if 36-48 hours; <5% if delayed >48 hours.",
        "treatment_ja": "緊急安定化: 輸液療法（乳酸リンゲル液 10mL/kg SC/IP）、酸素補給、保温管理。オキシトシン（0.5-2 IU/kg IM、15-30分間隔で最大2回）で排出促進を試みる。カルシウムグルコン酸（50-100mg/kg SC）で子宮収縮を補助。反応がない場合や敗血症徴候がある場合は緊急帝王切開術/卵巣子宮摘出術（イソフルラン吸入麻酔）。抗菌薬（エンロフロキサシン 5-10mg/kg PO/SC q12h）。疼痛管理（ブプレノルフィン 0.05-0.1mg/kg SC q8-12h、メロキシカム 0.2-0.5mg/kg PO q24h）。術後の敗血症・DIC徴候をモニタリング。デグーの糖尿病傾向に留意し血糖値管理。強制給餌と保温。",
        "prevention": "Prevention of retained fetus requires stringent pre-breeding screening given degus' precocial neonate burden (large gestational investment in small body mass, 300-350g) and rapid septic progression (36-48 hour window). Pre-breeding MANDATORY weight assessment: exclude females >400g (obesity = dystocia contraindication). Ideal weight 300-350g pre-breeding. Assess pelvic anatomy (ultrasound/radiographs). Nutrition: timothy hay-based diet with calcium minimum 0.4% throughout gestation. Temperature control 15-22°C (heat stress worsens dystocia progression). Avoid sugar/fruit for 6-8 weeks pre-breeding (normalize blood glucose for pregnancy). During labor: Monitor actively—normal labor <1-2 hours with complete delivery of all kits. Count kits before breeding to verify litter size matches expected count. Actively manage dystocia: if straining without fetal delivery >30 minutes, intervene with cesarean (do NOT delay). Post-parturition: Verify complete placental expulsion. Monitor for vaginal discharge (purulent = emergency). Maintain 15-22°C temperature post-partum (cold stress delays uterine involution). Weight cycling post-partum: restrict food slightly if >420g post-birth (prevents future obesity-related dystocia). OVE recommended for non-breeding females.",
        "prevention_ja": "胎児残留の予防: デグーの前置胎盤負担と36-48時間の急速敗血症進行を考慮。繁殖前MANDATORY体重評価: 400g以上のメスは除外（肥満=難産禁忌）。理想体重300-350g。骨盤解剖評価。妊娠期のカルシウム十分摂取。温度管理（15-22°C）。繁殖6-8週間前に糖/フルーツ制限。分娩中の積極的モニタリング（正常分娩<1-2時間）。胎児数確認。難産後30分以内に帝王切開。分娩後の完全な胎盤排出確認。膣排膿の監視。産後の温度管理。非繁殖メスはOVE推奨。",
        "prognosis": "Prognosis depends on severity, underlying cause, and timeliness of treatment. Early aggressive intervention generally improves outcomes. Delayed presentation carries a guarded to poor prognosis.",
        "prognosis_ja": "胎児残留の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Neonatal Mortality",
        "name_ja": "新生児死亡",
        "symptoms": {"failure_to_thrive", "hypothermia", "weakness"},
        "description": "Neonatal Mortality is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "母親の育児放棄、低温、先天性欠陥による生後1週間以内の子の死亡です。",
        "urgency": "high",
        "recommended_tests": ["physical_exam", "necropsy", "environmental_review"],
        "causes": "Caused by maternal neglect, hypothermia, inadequate milk production, congenital defects, or infectious disease in newborn degus.",
        "causes_ja": "デグーにおける新生児死亡の原因: ホルモンバランス異常、感染性病原体、難産、栄養欠乏、加齢、遺伝的要因による生殖器病理。不適切な繁殖管理がリスクを高める。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "新生児死亡はデグーにおける生殖器疾患である。ホルモンバランスの異常、構造異常、または生殖器への感染過程を伴う。性ホルモンの調節障害は生殖器官の嚢胞性変化、過形成、または腫瘍形成を引き起こしうる。産科的合併症は機械的閉塞や代謝異常を引き起こし、母体と産子の両方を脅かす。生殖器の二次細菌感染は全身性敗血症に進行しうる。",
        "treatment": "For surviving neonates: environmental warming is critical — maintain nest temperature 30-32°C with supplemental heating pad (covered to prevent burns). Hand-rearing if maternal neglect: kitten milk replacer (KMR) diluted 1:2 initially, fed via 1 mL syringe or small paintbrush every 2-3 hours for first week. Degu pups are precocial (born furred with open eyes) but still require milk for 4-6 weeks. Supplement weak neonates with warmed 5% dextrose 0.05-0.1 mL PO q2-4h for first 24-48 hours if hypoglycemic. Monitor body weight daily — expect 1-2 g/day gain. Cross-fostering to another lactating dam is ideal if available. For dam with inadequate milk: ensure high-quality timothy hay + degu pellets, fresh water ad libitum, calcium supplementation if deficient. If infectious cause: enrofloxacin 5-10 mg/kg PO q12h to dam (excreted in milk). Necropsy of deceased neonates recommended to identify cause and prevent recurrence. Congenital defects: genetic counseling — remove affected breeding pairs from colony.",
        "treatment_ja": "生存新生児への対応: 環境保温が最重要 — 巣箱温度30-32℃を補助ヒーティングパッドで維持（火傷防止のためカバー）。母親の育児放棄時の人工哺育: キトンミルクリプレーサー（KMR）を初期1:2に希釈、1mLシリンジまたは小筆で最初の1週間はq2-3h給餌。デグー新生児は早熟性（被毛あり・開眼で出生）だが乳は4-6週間必要。衰弱新生児に低血糖があれば加温5%デキストロース 0.05-0.1mL PO q2-4h 最初の24-48時間。体重を毎日測定 — 1-2g/日の増加を期待。里親（他の泌乳中の母親）への委託が理想的。母親の泌乳不良時: 高品質チモシー+デグーペレット、新鮮な水自由摂取、カルシウム不足時は補充。感染性原因の場合: 母親にエンロフロキサシン 5-10mg/kg PO q12h（乳汁中に排泄）。死亡新生児の剖検を推奨し原因特定・再発防止。先天性欠陥: 遺伝カウンセリング — 罹患繁殖ペアをコロニーから除外。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "新生児死亡の予防: 定期的な健康診断。適切な栄養管理。ストレスの軽減。清潔な飼育環境の維持。異常の早期発見・早期受診。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "新生児死亡の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"young"},
    },
    {
        "name": "Pericardial Effusion",
        "name_ja": "心嚢液貯留",
        "symptoms": {"exercise_intolerance", "lethargy", "muffled_heart_sounds", "respiratory_distress"},
        "description": "Pericardial Effusion is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "心臓周囲の液体蓄積で心タンポナーデと拍出量低下を引き起こします。",
        "urgency": "emergency",
        "recommended_tests": ["echocardiography", "chest_xray", "pericardiocentesis"],
        "causes": "Caused by accumulation of fluid in the pericardial sac from cardiac disease, infection, neoplasia, or metabolic disorders.",
        "causes_ja": "デグーの心血管系に影響する正確な原因は不明または多因子性。遺伝的素因・環境因子・免疫調節異常・不顕性感染・代謝障害が寄与因子として考えられる。個々の症例での主原因特定にはさらなる調査が必要。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "デグーの心血管系に影響する正確な病態生理は完全には解明されていない。遺伝的素因・環境因子・免疫調節異常を含む多因子性メカニズムが関与すると考えられる。心血管系組織における炎症性・代謝性・構造的変化が進行性の臨床徴候をもたらす。デグーにおける疾患メカニズムの完全な解明にはさらなる研究が必要。",
        "treatment": "EMERGENCY if cardiac tamponade (obstructive shock, collapse, severe dyspnea). "
        "PERICARDIOCENTESIS: Under isoflurane anesthesia (chamber induction 3-4%, maintenance "
        "1.5-2.5%, body temperature maintenance 37°C heated pad), ultrasound-guided needle "
        "aspiration of pericardial fluid (22-25G needle). Submit fluid for cytology and culture. "
        "TECHNICALLY VERY CHALLENGING in degus due to small body size (<300g) — referral to "
        "exotic specialist strongly recommended. MEDICAL MANAGEMENT: Furosemide 1-4 mg/kg "
        "PO/SC/IM q8-12h (reduce preload/fluid accumulation). Enalapril 0.5 mg/kg PO q24h "
        "(ACE inhibitor, afterload reduction). Pimobendan 0.1-0.3 mg/kg PO q12h (positive "
        "inotrope/vasodilator — if concurrent systolic dysfunction). TREAT UNDERLYING CAUSE: "
        "Infectious pericarditis: enrofloxacin 5-10 mg/kg PO q12h × 14-21 days (oral β-lactams "
        "CONTRAINDICATED). Neoplastic: palliative care, prognosis poor. Metabolic (diabetic "
        "cardiomyopathy): optimize glycemic control. OXYGEN SUPPLEMENTATION: Flow-by O2 "
        "at 1-2 L/min during acute respiratory distress. MONITORING: Echocardiography q2-4 "
        "weeks to assess effusion recurrence. Activity restriction — minimize stress and "
        "exertion. References: Quesenberry & Carpenter (2012); Keeble & Meredith (2009) "
        "BSAVA Manual of Rodents and Ferrets.",
        "treatment_ja": "心タンポナーデ（閉塞性ショック、虚脱、重度呼吸困難）は緊急。【心嚢穿刺】イソフルラン"
        "麻酔下で超音波ガイド下でのニードル吸引。デグーの小さい体サイズ（<300g）により"
        "技術的に非常に困難 — エキゾチック専門医への紹介を強く推奨。【内科管理】フロセミド"
        "1-4 mg/kg PO/SC/IM q8-12h。エナラプリル0.5 mg/kg PO q24h。ピモベンダン"
        "0.1-0.3 mg/kg PO q12h（収縮機能障害併発時）。【原因治療】感染性: エンロフロキサシン"
        "5-10 mg/kg PO q12h × 14-21日（経口βラクタム系禁忌）。腫瘍性: 緩和ケア。代謝性: "
        "血圧管理最適化。【酸素】フローバイO2 1-2 L/min。心エコーで2-4週ごとモニタリング。",
        "prevention": "No specific prevention for idiopathic pericardial effusion. Optimal glycemic control in "
        "diabetic degus reduces risk of diabetic cardiomyopathy. Regular health monitoring in "
        "senior degus (>4 years). Prompt treatment of respiratory and systemic infections. "
        "Maintain appropriate environmental temperature (20-22°C) — cold stress may exacerbate "
        "cardiac conditions. Reference: Quesenberry & Carpenter (2012).",
        "prevention_ja": "特発性心嚢液貯留の特異的予防法はない。糖尿病デグーでは最適な血糖管理で糖尿病性"
        "心筋症リスクを軽減。高齢デグー（>4歳）の定期健康モニタリング。適切な環境温度維持"
        "（20-22°C）。",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "特発性疾患の予後は個々の症例により変動する。自然寛解する場合もあるが、慢性再発性の経過をたどることもある。対症療法と支持療法が治療の中心。定期的な再評価により治療方針を調整する。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Aortic Calcification",
        "name_ja": "大動脈石灰化",
        "symptoms": {"exercise_intolerance", "hind_limb_weakness", "lethargy", "sudden_death"},
        "description": "Aortic Calcification is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "主要血管の石灰化で、糖尿病デグーやカルシウム-リンバランス不均衡のデグーに多いです。",
        "urgency": "high",
        "recommended_tests": ["chest_xray", "blood_chemistry", "echocardiography"],
        "causes": "Caused by mineralization of the aortic wall, commonly associated with diabetes mellitus and calcium-phosphorus imbalance in the diet.",
        "causes_ja": "デグーにおける大動脈石灰化の原因: 主要血管の石灰化で、糖尿病デグーやカルシウム-リンバランス不均衡のデグーに多いです。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "大動脈石灰化はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "No effective treatment to reverse established vascular calcification. Management focuses on underlying diabetes and metabolic control. Strict dietary management: eliminate ALL sugar-containing foods (fruit, treats, honey, molasses); provide timothy hay-based diet with low-glycemic degu-specific pellets. Blood glucose monitoring: fasting glucose target <200 mg/dL (degus are naturally insulin-resistant). Cardiovascular support: enalapril 0.5 mg/kg PO q24h for afterload reduction if heart failure develops. Phosphate binders: aluminum hydroxide 30-90 mg/kg PO q8-12h with food if hyperphosphatemia present. Correct calcium-phosphorus imbalance: dietary Ca:P ratio 1.5-2:1, avoid excessive calcium supplementation (can worsen calcification). Exercise promotion: large enclosure with running wheel to improve cardiovascular fitness and glucose regulation. Regular radiographic monitoring q3-6 months to assess progression. Echocardiography if cardiac involvement suspected. Prognosis: guarded — calcification is irreversible, but progression can be slowed with strict metabolic control.",
        "treatment_ja": "確立した血管石灰化を元に戻す有効な治療法はない。管理は基礎糖尿病と代謝コントロールに重点。厳格な食事管理: 糖分を含む全食品（果物、おやつ、蜂蜜、糖蜜）の排除、低GIデグー専用ペレットのチモシー主体食。血糖モニタリング: 空腹時血糖目標値<200mg/dL（デグーは生来インスリン抵抗性）。心血管サポート: 心不全発症時はエナラプリル 0.5mg/kg PO q24h（後負荷軽減）。リン結合薬: 高リン血症があれば水酸化アルミニウム 30-90mg/kg PO q8-12h 食事と共に。Ca:P不均衡の補正: 食事Ca:P比1.5-2:1、過剰カルシウム補充は禁止（石灰化を悪化させうる）。運動促進: 大型ケージにランニングホイールで心血管フィットネスと血糖調節を改善。定期的なレントゲンモニタリングq3-6ヶ月で進行評価。心臓関与の疑いがあれば心エコー。予後: 要注意 — 石灰化は不可逆だが、厳格な代謝管理で進行を遅延可能。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "大動脈石灰化の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "大動脈石灰化の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Lymphoma",
        "name_ja": "リンパ腫",
        "symptoms": {"appetite_loss", "lethargy", "lymph_node_swelling", "splenomegaly", "weight_loss"},
        "description": "Lymphoma is a neoplastic condition characterized by abnormal cell proliferation that may be benign or malignant.",
        "description_ja": "リンパ節、脾臓、他の臓器に影響するリンパ球の腫瘍性増殖です。",
        "urgency": "high",
        "recommended_tests": ["fine_needle_aspirate", "cbc", "abdominal_ultrasound"],
        "causes": "Caused by neoplastic proliferation of lymphoid cells, with aging, chronic immune stimulation, and genetic predisposition as contributing factors.",
        "causes_ja": "デグーにおけるリンパ腫の原因: 癌遺伝子・腫瘍抑制遺伝子の遺伝子変異蓄積による腫瘍性形質転換。加齢、慢性炎症、ウイルス感染、ホルモン影響、UV曝露、遺伝的素因がリスク因子。",
        "pathophysiology": "Accumulated genetic mutations lead to uncontrolled cell proliferation, evasion of apoptosis, and potential metastatic spread. Tumor growth causes tissue compression, invasion, and paraneoplastic effects.",
        "pathophysiology_ja": "リンパ腫はデグーにおける腫瘍性疾患である。癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積により腫瘍性形質転換が生じる。制御不能な細胞増殖により腫瘍が形成され、局所組織への浸潤・破壊の可能性がある。悪性腫瘍はリンパ行性または血行性に転移しうる。高カルシウム血症、悪液質、免疫調節障害などの腫瘍随伴症候群が原発腫瘍に伴い、罹患率に寄与することがある。",
        "treatment": "Prednisolone 0.5-2 mg/kg PO SID (avoid dexamethasone due to diabetes risk). Palliative management is mainstay given limited chemo data in degus. Meloxicam 1-2 mg/kg PO SID for comfort. Supportive care with syringe feeding and fluid therapy SC as needed.",
        "treatment_ja": "デグー白血病/リンパ腫: ① エキゾチック小型哺乳類でのリンパ系腫瘍は症例報告レベル—フェレット以外では治療プロトコル未確立。② 確定: リンパ節/腫瘤FNA・生検＋IHC、CBC（リンパ球数、白血球分画）、画像診断（超音波・X線）、骨髄穿刺。③ 緩和的化学療法: プレドニゾロン 1-2 mg/kg PO q24h（多くで第一選択、QOL改善）、クロラムブシル 0.1-0.2 mg/kg PO q24-48h、L-asparaginase 10,000 IU/m² IM/SC q週（試験的）。④ 外科切除: 孤立性腫瘤型に限定的—多発性・全身性は化学療法。⑤ 支持療法: シリンジ給餌（Critical Care 50-90 mL/kg/日）、輸液 80-100 mL/kg/日 SC、温熱管理、メロキシカム 0.5-1.5 mg/kg PO q12-24h（疼痛・炎症）。⑥ 個別意思決定—QOL中心の緩和ケアを優先する場合が多い。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention is limited for most neoplastic conditions. Regular health examinations facilitate early detection. Spaying/neutering may reduce risk of hormone-dependent tumors.",
        "prevention_ja": "リンパ腫の予防は限定的であるが、ホルモン依存性腫瘍軽減のための避妊・去勢手術、既知の発癌物質の回避、早期発見のための定期健診、適正体型の維持、該当する場合は遺伝的素因軽減のための責任ある繁殖が含まれる。",
        "prognosis": "Variable prognosis depending on type, staging, and treatment response. Chemotherapy can achieve remission in many cases, but relapse is common.",
        "prognosis_ja": "リンパ腫の予後: 腫瘍の種類、病期、転移の有無により予後は大きく異なる。早期発見・早期治療で予後改善。悪性腫瘍は一般的に予後要注意〜不良。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Fibrosarcoma",
        "name_ja": "線維肉腫",
        "symptoms": {"rapid_growth", "skin_masses", "ulceration", "weight_loss"},
        "description": "Fibrosarcoma is a neoplastic condition characterized by abnormal cell proliferation that may be benign or malignant.",
        "description_ja": "悪性結合組織腫瘍。体のどの部位にも発生し得ます。",
        "urgency": "high",
        "recommended_tests": ["biopsy", "histopathology", "chest_xray"],
        "causes": "Caused by malignant transformation of fibroblasts, with aging, chronic inflammation, and genetic predisposition as risk factors.",
        "causes_ja": "デグーにおける線維肉腫の原因: 癌遺伝子・腫瘍抑制遺伝子の遺伝子変異蓄積による腫瘍性形質転換。加齢、慢性炎症、ウイルス感染、ホルモン影響、UV曝露、遺伝的素因がリスク因子。",
        "pathophysiology": "Accumulated genetic mutations lead to uncontrolled cell proliferation, evasion of apoptosis, and potential metastatic spread. Tumor growth causes tissue compression, invasion, and paraneoplastic effects.",
        "pathophysiology_ja": "線維肉腫はデグーにおける腫瘍性疾患である。癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積により腫瘍性形質転換が生じる。制御不能な細胞増殖により腫瘍が形成され、局所組織への浸潤・破壊の可能性がある。悪性腫瘍はリンパ行性または血行性に転移しうる。高カルシウム血症、悪液質、免疫調節障害などの腫瘍随伴症候群が原発腫瘍に伴い、罹患率に寄与することがある。",
        "treatment": "Wide surgical excision under isoflurane if mass is resectable. Meloxicam 1-2 mg/kg PO SID post-op. Avoid dexamethasone (diabetes-prone species). High local recurrence rate; re-excision may be needed. Palliative care with meloxicam and gabapentin if inoperable.",
        "treatment_ja": "切除可能であればイソフルラン麻酔下で広範切除。術後メロキシカム1-2 mg/kg PO SID。デキサメタゾンは糖尿病リスクで禁忌。局所再発率が高く再切除が必要になることあり。切除不能例はメロキシカムとガバペンチンで緩和ケア。",
        "prevention": "Prevention is limited for most neoplastic conditions. Regular health examinations facilitate early detection. Spaying/neutering may reduce risk of hormone-dependent tumors.",
        "prevention_ja": "線維肉腫の予防は限定的であるが、ホルモン依存性腫瘍軽減のための避妊・去勢手術、既知の発癌物質の回避、早期発見のための定期健診、適正体型の維持、該当する場合は遺伝的素因軽減のための責任ある繁殖が含まれる。",
        "prognosis": "Prognosis depends on tumor type, staging, and response to treatment. Complete surgical excision of localized tumors improves outcomes. Metastatic disease carries a guarded to poor prognosis.",
        "prognosis_ja": "線維肉腫の予後: 腫瘍の種類、病期、転移の有無により予後は大きく異なる。早期発見・早期治療で予後改善。悪性腫瘍は一般的に予後要注意〜不良。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Lipoma",
        "name_ja": "脂肪腫",
        "symptoms": {"slow_growing_lump", "subcutaneous_mass"},
        "description": "Lipoma is a neoplastic condition characterized by abnormal cell proliferation that may be benign or malignant.",
        "description_ja": "皮下に一般的に見られる良性脂肪腫瘍。通常問題ありません。",
        "urgency": "low",
        "recommended_tests": ["fine_needle_aspirate", "physical_exam"],
        "causes": "Caused by benign proliferation of adipocytes forming encapsulated subcutaneous masses, more common in obese or older degus.",
        "causes_ja": "デグーにおける脂肪腫の原因: 癌遺伝子・腫瘍抑制遺伝子の遺伝子変異蓄積による腫瘍性形質転換。加齢、慢性炎症、ウイルス感染、ホルモン影響、UV曝露、遺伝的素因がリスク因子。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "脂肪腫はデグーにおける腫瘍性疾患である。癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積により腫瘍性形質転換が生じる。制御不能な細胞増殖により腫瘍が形成され、局所組織への浸潤・破壊の可能性がある。悪性腫瘍はリンパ行性または血行性に転移しうる。高カルシウム血症、悪液質、免疫調節障害などの腫瘍随伴症候群が原発腫瘍に伴い、罹患率に寄与することがある。",
        "treatment": "CONSERVATIVE MANAGEMENT (most cases): Lipomas are benign and typically require no treatment "
        "if small, non-growing, and not interfering with movement or function. Monitor size monthly — "
        "measure with calipers or photograph for comparison. SURGICAL EXCISION: Indicated when: "
        "mass is rapidly growing, restricting movement, ulcerated, or causing discomfort; if FNA "
        "cytology is equivocal (must rule out liposarcoma). Procedure under isoflurane anesthesia "
        "(chamber induction 3-4%, nose cone maintenance 1.5-2.5%, 37°C heated pad — hypothermia "
        "risk in degus <200g). Blunt dissection along capsule plane for complete excision. Submit "
        "for histopathology to confirm benign diagnosis. DIAGNOSTIC: FNA (fine needle aspirate) "
        "for initial assessment — expect mature adipocytes with no atypia. If spindle cells or "
        "pleomorphic cells present → excisional biopsy to rule out liposarcoma or infiltrative "
        "lipoma. WEIGHT MANAGEMENT: Obesity predisposes to lipoma formation — maintain ideal body "
        "weight (170-300g) on strict timothy hay-based diet, no sugar/fruit. POST-OPERATIVE: "
        "Meloxicam 1-2 mg/kg PO/SC q24h × 3-5 days. Wound check at 5-7 days. Skin sutures "
        "(if used) removal at 10-14 days. Recurrence at same site is uncommon for simple lipomas. "
        "References: Quesenberry & Carpenter (2012); Percy & Barthold (2007).",
        "treatment_ja": "デグー脂肪腫: ① 多くは老齢肥満個体に発生する良性皮下腫瘤。② 確定診断: 細胞診（FNA）で脂肪細胞確認、急速増大例は針生検または切除生検で脂肪肉腫/腺癌/膿瘍を除外。③ 手術適応: 機能障害（歩行・摂食・排泄阻害）、皮膚潰瘍、急速増大、整容的要請。④ 切除: 局所麻酔 + 軽鎮静で対応可能な小型腫瘤、全身麻酔が必要な深部・大型は周術期低体温・絶食管理を厳格に。⑤ 鎮痛: メロキシカム 0.5-1.5 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h、術後5-7日継続。⑥ 食事/体重管理: 高繊維低脂肪（チモシー主体、ペレット制限）、運動空間の確保、四半期毎の体重トレンド評価。⑦ 浸潤性脂肪腫（infiltrative lipoma）—筋層に浸潤、不完全切除で再発—に注意。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。"
        "通常治療不要。月1回のサイズモニタリング。【外科的切除】適応: 急速増大、運動制限、"
        "潰瘍化、不快感がある場合; FNA細胞診が不確定の場合（脂肪肉腫の除外必須）。"
        "イソフルラン麻酔下で被膜に沿った鈍的剥離による完全切除。病理組織検査に提出。"
        "【診断】FNAで成熟脂肪細胞を確認（異型性なし）。紡錘形細胞や多形性細胞がある場合は"
        "切除生検。【体重管理】肥満は脂肪腫の素因 — チモシー牧草ベースの厳格食で理想体重維持。"
        "【術後】メロキシカム1-2 mg/kg PO/SC q24h × 3-5日。5-7日で創傷チェック。",
        "prevention": "Maintain ideal body weight (170-300g) through timothy hay-based diet and regular exercise. "
        "Obesity is the most significant modifiable risk factor for lipoma development. No "
        "sugar/fruit (diabetes AND obesity prevention). Regular physical examination to detect "
        "new masses early. No specific pharmacological prevention available. "
        "Reference: Percy & Barthold (2007) Pathology of Laboratory Rodents 3rd ed.",
        "prevention_ja": "チモシー牧草ベース食と運動による理想体重（170-300g）の維持。肥満は脂肪腫の最も重要な"
        "修正可能リスク因子。糖分/果物禁忌（糖尿病と肥満の両方を予防）。新しい腫瘤の早期発見"
        "のための定期身体検査。",
        "prognosis": "Good prognosis. Benign condition that may be managed conservatively or with surgical excision.",
        "prognosis_ja": "脂肪腫の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Squamous Cell Carcinoma",
        "name_ja": "扁平上皮癌",
        "symptoms": {"bleeding_from_mass", "skin_masses", "ulceration", "weight_loss"},
        "description": "Squamous Cell Carcinoma is a neoplastic condition characterized by abnormal cell proliferation that may be benign or malignant.",
        "description_ja": "皮膚や口腔の悪性上皮腫瘍です。",
        "urgency": "high",
        "recommended_tests": ["biopsy", "histopathology", "chest_xray"],
        "causes": "Caused by malignant transformation of squamous epithelial cells, with UV exposure, chronic irritation, and aging as risk factors.",
        "causes_ja": "デグーにおける扁平上皮癌の原因: 癌遺伝子・腫瘍抑制遺伝子の遺伝子変異蓄積による腫瘍性形質転換。加齢、慢性炎症、ウイルス感染、ホルモン影響、UV曝露、遺伝的素因がリスク因子。",
        "pathophysiology": "Accumulated genetic mutations lead to uncontrolled cell proliferation, evasion of apoptosis, and potential metastatic spread. Tumor growth causes tissue compression, invasion, and paraneoplastic effects.",
        "pathophysiology_ja": "扁平上皮癌はデグーにおける腫瘍性疾患である。癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積により腫瘍性形質転換が生じる。制御不能な細胞増殖により腫瘍が形成され、局所組織への浸潤・破壊の可能性がある。悪性腫瘍はリンパ行性または血行性に転移しうる。高カルシウム血症、悪液質、免疫調節障害などの腫瘍随伴症候群が原発腫瘍に伴い、罹患率に寄与することがある。",
        "treatment": "Surgical excision with wide margins under isoflurane if localized. Meloxicam 1-2 mg/kg PO SID for pain. Avoid dexamethasone (diabetes risk). Cryotherapy for small superficial lesions. Palliative wound care and meloxicam if inoperable or metastatic.",
        "treatment_ja": "局所型であればイソフルラン麻酔下で広範マージン切除。メロキシカム1-2 mg/kg PO SIDで疼痛管理。デキサメタゾンは糖尿病リスクで禁忌。小型表在性病変には凍結療法。切除不能・転移例は創傷ケアとメロキシカムで緩和。",
        "prevention": "Prevention is limited for most neoplastic conditions. Regular health examinations facilitate early detection. Spaying/neutering may reduce risk of hormone-dependent tumors.",
        "prevention_ja": "扁平上皮癌の予防は限定的であるが、ホルモン依存性腫瘍軽減のための避妊・去勢手術、既知の発癌物質の回避、早期発見のための定期健診、適正体型の維持、該当する場合は遺伝的素因軽減のための責任ある繁殖が含まれる。",
        "prognosis": "Prognosis depends on tumor type, staging, and response to treatment. Complete surgical excision of localized tumors improves outcomes. Metastatic disease carries a guarded to poor prognosis.",
        "prognosis_ja": "扁平上皮癌の予後: 腫瘍の種類、病期、転移の有無により予後は大きく異なる。早期発見・早期治療で予後改善。悪性腫瘍は一般的に予後要注意〜不良。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Hepatocellular Carcinoma",
        "name_ja": "肝細胞癌",
        "symptoms": {"abdominal_distension", "jaundice", "lethargy", "weight_loss"},
        "description": "Hepatocellular Carcinoma is a neoplastic condition characterized by abnormal cell proliferation that may be benign or malignant.",
        "description_ja": "予後不良の原発性悪性肝臓腫瘍です。",
        "urgency": "high",
        "recommended_tests": ["liver_ultrasound", "blood_chemistry", "fine_needle_aspirate"],
        "causes": "Caused by malignant transformation of hepatocytes, often associated with chronic liver disease, toxin exposure, or aging.",
        "causes_ja": "デグーにおける肝細胞癌の原因: 癌遺伝子・腫瘍抑制遺伝子の遺伝子変異蓄積による腫瘍性形質転換。加齢、慢性炎症、ウイルス感染、ホルモン影響、UV曝露、遺伝的素因がリスク因子。",
        "pathophysiology": "Accumulated genetic mutations lead to uncontrolled cell proliferation, evasion of apoptosis, and potential metastatic spread. Tumor growth causes tissue compression, invasion, and paraneoplastic effects.",
        "pathophysiology_ja": "肝細胞癌はデグーにおける腫瘍性疾患である。癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積により腫瘍性形質転換が生じる。制御不能な細胞増殖により腫瘍が形成され、局所組織への浸潤・破壊の可能性がある。悪性腫瘍はリンパ行性または血行性に転移しうる。高カルシウム血症、悪液質、免疫調節障害などの腫瘍随伴症候群が原発腫瘍に伴い、罹患率に寄与することがある。",
        "treatment": "Surgical lobectomy under isoflurane only if single lobe affected and patient stable. Meloxicam 1-2 mg/kg PO SID for pain. Avoid dexamethasone (diabetes risk). Prognosis usually poor; palliative care with syringe feeding, SC fluids, and meloxicam is typical approach.",
        "treatment_ja": "単葉病変で全身状態安定ならイソフルラン麻酔下で肝葉切除も検討。メロキシカム1-2 mg/kg PO SIDで疼痛管理。デキサメタゾンは糖尿病リスクで禁忌。予後は通常不良で、シリンジ給餌・皮下輸液・メロキシカムによる緩和ケアが主体。",
        "prevention": "Prevention is limited for most neoplastic conditions. Regular health examinations facilitate early detection. Spaying/neutering may reduce risk of hormone-dependent tumors.",
        "prevention_ja": "肝細胞癌の予防は限定的であるが、ホルモン依存性腫瘍軽減のための避妊・去勢手術、既知の発癌物質の回避、早期発見のための定期健診、適正体型の維持、該当する場合は遺伝的素因軽減のための責任ある繁殖が含まれる。",
        "prognosis": "Prognosis depends on tumor type, staging, and response to treatment. Complete surgical excision of localized tumors improves outcomes. Metastatic disease carries a guarded to poor prognosis.",
        "prognosis_ja": "肝細胞癌の予後: 腫瘍の種類、病期、転移の有無により予後は大きく異なる。早期発見・早期治療で予後改善。悪性腫瘍は一般的に予後要注意〜不良。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Osteosarcoma",
        "name_ja": "骨肉腫",
        "symptoms": {"lameness", "limb_swelling", "pain", "pathological_fracture"},
        "description": "Osteosarcoma is a neoplastic condition characterized by abnormal cell proliferation that may be benign or malignant.",
        "description_ja": "転移能を持つ悪性骨腫瘍で、主に長管骨に発生します。",
        "urgency": "high",
        "recommended_tests": ["limb_xray", "chest_xray", "biopsy"],
        "causes": "Caused by malignant transformation of osteoblasts, with genetic predisposition and prior bone trauma as potential risk factors.",
        "causes_ja": "デグーにおける骨肉腫の原因: 癌遺伝子・腫瘍抑制遺伝子の遺伝子変異蓄積による腫瘍性形質転換。加齢、慢性炎症、ウイルス感染、ホルモン影響、UV曝露、遺伝的素因がリスク因子。",
        "pathophysiology": "Accumulated genetic mutations lead to uncontrolled cell proliferation, evasion of apoptosis, and potential metastatic spread. Tumor growth causes tissue compression, invasion, and paraneoplastic effects.",
        "pathophysiology_ja": "骨肉腫はデグーにおける腫瘍性疾患である。癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積により腫瘍性形質転換が生じる。制御不能な細胞増殖により腫瘍が形成され、局所組織への浸潤・破壊の可能性がある。悪性腫瘍はリンパ行性または血行性に転移しうる。高カルシウム血症、悪液質、免疫調節障害などの腫瘍随伴症候群が原発腫瘍に伴い、罹患率に寄与することがある。",
        "treatment": "Limb amputation under isoflurane if no pulmonary metastasis; degus can adapt to 3 legs. Meloxicam 1-2 mg/kg PO SID and tramadol for post-op pain. Avoid dexamethasone (diabetes risk). Palliative meloxicam and gabapentin if inoperable. Prognosis generally poor.",
        "treatment_ja": "肺転移がなければイソフルラン麻酔下で患肢切断（デグーは3本脚に適応可能）。術後メロキシカム1-2 mg/kg PO SIDとトラマドールで疼痛管理。デキサメタゾンは糖尿病リスクで禁忌。切除不能例はメロキシカムとガバペンチンで緩和。予後は通常不良。",
        "prevention": "Prevention is limited for most neoplastic conditions. Regular health examinations facilitate early detection. Spaying/neutering may reduce risk of hormone-dependent tumors.",
        "prevention_ja": "骨肉腫の予防は限定的であるが、ホルモン依存性腫瘍軽減のための避妊・去勢手術、既知の発癌物質の回避、早期発見のための定期健診、適正体型の維持、該当する場合は遺伝的素因軽減のための責任ある繁殖が含まれる。",
        "prognosis": "Prognosis depends on tumor type, staging, and response to treatment. Complete surgical excision of localized tumors improves outcomes. Metastatic disease carries a guarded to poor prognosis.",
        "prognosis_ja": "骨肉腫の予後: 腫瘍の種類、病期、転移の有無により予後は大きく異なる。早期発見・早期治療で予後改善。悪性腫瘍は一般的に予後要注意〜不良。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Nutritional Secondary Hyperparathyroidism",
        "name_ja": "栄養性二次性副甲状腺機能亢進症",
        "symptoms": {"bone_pain", "lameness", "pathological_fracture", "soft_jaw"},
        "description": "Nutritional Secondary Hyperparathyroidism is a nutritional or metabolic disorder caused by dietary imbalance or deficiency.",
        "description_ja": "カルシウム-リン食事不均衡による副甲状腺ホルモンの過剰分泌で、骨の脱灰を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "xray", "diet_review"],
        "causes": "Caused by dietary calcium-phosphorus imbalance (low calcium, high phosphorus) or vitamin D deficiency, leading to compensatory parathyroid hormone hypersecretion and bone demineralization.",
        "causes_ja": "デグーにおける栄養性二次性副甲状腺機能亢進症の原因: カルシウム-リン食事不均衡による副甲状腺ホルモンの過剰分泌で、骨の脱灰を引き起こします。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "栄養性二次性副甲状腺機能亢進症はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "Acute hypocalcemia (tetany, seizures): calcium gluconate 50-100 mg/kg IV/IO slowly over 10-15 min with ECG monitoring (stop if bradycardia). Maintenance calcium supplementation: calcium glubionate syrup 1-2 mL/kg PO q12h until dietary correction established. Vitamin D3 supplementation: cholecalciferol 200-400 IU/kg PO q24h for 2-4 weeks, then reduce to maintenance. Dietary correction is the cornerstone: transition to high-quality timothy hay-based diet with appropriate Ca:P ratio (1.5-2:1). Add calcium-rich foods: dark leafy greens (dandelion greens, romaine lettuce — avoid excess oxalates like spinach). Degu-specific pellets with adequate calcium content. Avoid seeds and nuts (high phosphorus, low calcium). UVB lighting: 10-12% UVB bulb for 10-12 hours/day to enable endogenous vitamin D3 synthesis. Pain management for pathological fractures: meloxicam 1-2 mg/kg PO/SC q24h. Cage rest and padded enclosure to prevent further fractures during bone healing (4-8 weeks). Monitor ionized calcium and phosphorus levels q1-2 weeks initially, then monthly. Blood chemistry panel q3 months for long-term monitoring. Recovery of bone density is slow — may take 3-6 months with appropriate correction.",
        "treatment_ja": "急性低カルシウム血症（テタニー、痙攣）: グルコン酸カルシウム 50-100mg/kg IV/IO 10-15分かけてゆっくり投与、ECGモニタリング（徐脈出現時は中止）。維持カルシウム補充: グルビオン酸カルシウムシロップ 1-2mL/kg PO q12h（食事補正が確立するまで）。ビタミンD3補充: コレカルシフェロール 200-400 IU/kg PO q24h 2-4週間、以後維持量に減量。食事補正が治療の要: 適切なCa:P比（1.5-2:1）の高品質チモシー主体食への移行。カルシウム豊富な食品の追加: 濃緑色葉野菜（タンポポ葉、ロメインレタス — ほうれん草等シュウ酸の多いものは避ける）。適切なカルシウム含有量のデグー専用ペレット。種子・ナッツ類の回避（高リン・低カルシウム）。UVBライト: 10-12% UVB球を1日10-12時間照射し内因性ビタミンD3合成を促進。病的骨折の疼痛管理: メロキシカム 1-2mg/kg PO/SC q24h。骨癒合中（4-8週間）のケージレストとパッド付きケージでさらなる骨折を予防。イオン化カルシウム・リン値を初期q1-2週、以後月1回モニタリング。血液化学パネルq3ヶ月（長期モニタリング）。骨密度の回復は遅く、適切な補正で3-6ヶ月かかることがある。",
        "prevention": "Prevention includes providing a balanced, species-appropriate diet with adequate vitamins and minerals, appropriate UVB lighting where needed, and regular nutritional assessment.",
        "prevention_ja": "栄養性二次性副甲状腺機能亢進症の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "栄養性二次性副甲状腺機能亢進症の予後: 多くの内分泌疾患は適切な薬物療法で長期管理可能。定期的なホルモン値モニタリングと用量調整が重要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Alzheimer's-like Disease",
        "name_ja": "アルツハイマー様疾患",
        "symptoms": {"behavioral_changes", "confusion", "disorientation", "lethargy", "memory_loss"},
        "description": "Alzheimer's-like Disease is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "ヒトのアルツハイマー病に類似したベータアミロイド斑を持つデグーの加齢性神経変性疾患。デグーはこの疾患の自然モデルです。",
        "urgency": "moderate",
        "recommended_tests": ["neurological_exam", "behavioral_assessment", "physical_exam"],
        "causes": "Caused by age-related neurodegenerative processes with beta-amyloid plaque and tau protein accumulation similar to human Alzheimer's disease. Degus are a natural model for this condition.",
        "causes_ja": "デグーにおけるアルツハイマー様疾患の原因: ヒトのアルツハイマー病に類似したベータアミロイド斑を持つデグーの加齢性神経変性疾患。デグーはこの疾患の自然モデルです。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "アルツハイマー様疾患はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "NO CURATIVE TREATMENT — degus are a natural model of Alzheimer's-like disease, developing "
        "beta-amyloid plaques and tau protein hyperphosphorylation with aging (Inestrosa et al. 2005). "
        "SUPPORTIVE/PALLIATIVE MANAGEMENT: (1) ENVIRONMENTAL ENRICHMENT: Maintain social housing "
        "(cognitive stimulation through social interaction is critical in this highly social species). "
        "Provide novel objects, foraging opportunities, running wheel — cognitive enrichment may slow "
        "decline. Maintain CONSISTENT cage layout — disoriented degus rely on spatial memory; avoid "
        "rearranging. (2) GLYCEMIC CONTROL: Chronic hyperglycemia accelerates beta-amyloid "
        "deposition and cognitive decline in degus. Strict timothy hay-based diet, no sugar/fruit. "
        "Monitor blood glucose regularly. (3) ANTIOXIDANT SUPPLEMENTATION: Vitamin E "
        "(alpha-tocopherol) 1-5 mg/degu PO q24h (reduces oxidative stress associated with "
        "neurodegeneration — extrapolated from rodent AD models). Omega-3 fatty acids (DHA) — "
        "limited evidence but potential neuroprotective effects. (4) PHARMACOLOGICAL (EXPERIMENTAL, "
        "limited clinical evidence in degus): Selegiline (MAO-B inhibitor) — used in canine "
        "cognitive dysfunction, not validated in degus. Memantine (NMDA antagonist) — studied "
        "in degu research models. No approved treatments for companion degus. (5) QUALITY OF LIFE "
        "MONITORING: Assess eating, drinking, social interaction, grooming, mobility regularly. "
        "Progressive loss of function may warrant humane euthanasia discussion. "
        "References: Inestrosa et al. (2005) Mol Neurodegener; van Groen et al. (2011) "
        "Curr Alzheimer Res; Ardiles et al. (2012) Neurobiol Aging.",
        "treatment_ja": "【根治的治療法なし】デグーはアルツハイマー様疾患の自然モデルであり、加齢とともに"
        "βアミロイド斑とタウタンパク質のリン酸化亢進を発症する（Inestrosa et al. 2005）。"
        "【支持/緩和管理】(1) 環境エンリッチメント: 社会的飼育の維持（この高度に社会的な種では"
        "社会的相互作用による認知刺激が重要）。新規物品、フォレージング、回し車の提供。一貫した"
        "ケージレイアウト維持 — 見当識障害のあるデグーは空間記憶に依存。(2) 血糖管理: 慢性"
        "高血糖がβアミロイド沈着と認知機能低下を加速。チモシー牧草厳格食。(3) 抗酸化サプリ: "
        "ビタミンE 1-5 mg/個体 PO q24h。オメガ3脂肪酸（DHA）— エビデンス限定的だが神経保護"
        "効果の可能性。(4) 薬物療法（実験的、デグーでの臨床エビデンス限定的）: セレギリン、"
        "メマンチン — 研究モデルで検討。コンパニオンデグーでの承認治療はない。(5) QOL "
        "モニタリング: 食餌・飲水・社会的交流・毛繕い・運動能力を定期評価。",
        "prevention": "No proven prevention for age-related beta-amyloid accumulation. However, glycemic control "
        "is strongly associated with reduced neurodegeneration — strict sugar-free, timothy hay-based "
        "diet throughout life. Environmental enrichment and social housing may provide cognitive "
        "reserve that delays clinical onset. Regular exercise (running wheel). Antioxidant-rich "
        "diet components (dark leafy greens, herbs). Avoid chronic stress and social isolation. "
        "References: Inestrosa et al. (2005); Ardiles et al. (2012) Neurobiol Aging.",
        "prevention_ja": "加齢に伴うβアミロイド蓄積の確立された予防法はない。ただし血糖管理は神経変性の減少と"
        "強く関連 — 生涯を通じた無糖・チモシー牧草ベース食。環境エンリッチメントと社会的"
        "飼育が認知予備能を提供し臨床発症を遅延させる可能性。定期的な運動。抗酸化物質豊富な"
        "食事成分。慢性ストレスと社会的孤立の回避。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "アルツハイマー様疾患の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Cognitive Dysfunction (Senile)",
        "name_ja": "認知機能障害（老齢性）",
        "symptoms": {"decreased_social_interaction", "disorientation", "repetitive_behavior", "sleep_pattern_changes"},
        "description": "Cognitive Dysfunction (Senile) is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "高齢デグーの加齢関連認知機能低下で、行動変化と社会的引きこもりを引き起こします。",
        "urgency": "low",
        "recommended_tests": ["neurological_exam", "physical_exam", "behavioral_assessment"],
        "causes": "Caused by age-related neurodegeneration with progressive cognitive decline, potentially accelerated by chronic hyperglycemia and oxidative stress in diabetic degus.",
        "causes_ja": "デグーにおける認知機能障害（老齢性）の原因: 高齢デグーの加齢関連認知機能低下で、行動変化と社会的引きこもりを引き起こします。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "認知機能障害（老齢性）はデグーにおける神経疾患である。炎症、変性、圧迫、または血管障害による中枢・末梢神経系の損傷を伴う。解剖学的位置に応じて運動機能、感覚処理、自律神経調節、認知状態に影響を及ぼす。脱髄、軸索変性、ニューロン喪失は不可逆的な場合がある。浮腫や腫瘤性病変による頭蓋内圧亢進は脳幹ヘルニアを引き起こしうる。",
        "treatment": "NO CURATIVE TREATMENT — management is palliative, focused on slowing decline and maintaining "
        "quality of life. Closely related to Alzheimer's-like disease but represents the clinical "
        "syndrome in aged degus. (1) ENVIRONMENTAL ENRICHMENT: Novel objects rotated weekly, "
        "foraging puzzles (scatter food in hay to stimulate searching behavior), multiple levels "
        "with safe access (ramps, not ladders). Maintain CONSISTENT basic cage layout — disoriented "
        "degus need familiar spatial cues. (2) SOCIAL HOUSING: Continue group housing — social "
        "interaction is the most potent cognitive stimulus for this colonial species. Do NOT isolate "
        "a cognitively declining degu from its group unless aggression occurs. (3) DIETARY "
        "MANAGEMENT: Antioxidant supplementation — vitamin E (alpha-tocopherol) 1-5 mg/degu PO "
        "q24h. Omega-3 (DHA) supplementation. STRICT sugar-free, timothy hay-based diet — chronic "
        "hyperglycemia accelerates cognitive decline. (4) COMORBIDITY MANAGEMENT: Joint pain: "
        "meloxicam 1-2 mg/kg PO/SC q24h. Dental issues: regular dental check (elodont teeth may "
        "overgrow if reduced chewing activity). Weight monitoring: cognitive decline often "
        "accompanied by reduced food intake. (5) SAFETY MODIFICATIONS: Reduce platform heights "
        "(≤10 cm between levels), pad edges, remove hazardous obstacles. Place food/water at "
        "multiple accessible locations. (6) QUALITY OF LIFE ASSESSMENT: Regular monitoring of "
        "eating, drinking, grooming, social interaction, response to stimuli. Progressive "
        "unresponsiveness or inability to eat/drink warrants euthanasia discussion. "
        "References: Inestrosa et al. (2005); van Groen et al. (2011) Curr Alzheimer Res.",
        "treatment_ja": "【根治的治療なし — 進行緩和とQOL維持が目標】(1) 環境エンリッチメント: 新規物品の"
        "週1回ローテーション、フォレージングパズル。基本的ケージレイアウトは一貫性維持。"
        "(2) 社会的飼育の継続: 群れ飼育が最も強力な認知刺激。認知機能低下個体を群れから"
        "隔離しない。(3) 食事管理: ビタミンE 1-5 mg/個体 q24h。オメガ3（DHA）。"
        "厳格な無糖・チモシー牧草ベース食。(4) 併存症管理: 関節痛にメロキシカム"
        "1-2 mg/kg PO/SC q24h。常生歯の定期チェック。体重モニタリング。"
        "(5) 安全性改善: 段差≤10cm、パッド付きエッジ。食餌・水を複数箇所に配置。"
        "(6) QOL評価: 食餌・飲水・毛繕い・社会的交流・刺激への反応を定期監視。",
        "prevention": "Lifelong glycemic control through sugar-free, timothy hay-based diet (chronic hyperglycemia "
        "is the most significant modifiable risk factor for accelerated cognitive decline in degus). "
        "Environmental enrichment throughout life (cognitive reserve hypothesis). Social housing "
        "mandatory. Regular exercise. Antioxidant-rich dietary components. Avoid chronic stress "
        "and social isolation. Regular health monitoring in senior degus (>5 years). "
        "Reference: Inestrosa et al. (2005); Ardiles et al. (2012).",
        "prevention_ja": "生涯を通じた血糖管理（無糖・チモシー牧草ベース食 — 慢性高血糖がデグーの認知機能低下"
        "を加速する最も重要な修正可能リスク因子）。生涯を通じた環境エンリッチメント。"
        "社会的飼育必須。定期運動。抗酸化物質豊富な食事。高齢デグー（>5歳）の定期健康モニタリング。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "認知機能障害（老齢性）の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Peripheral Neuropathy (Diabetic)",
        "name_ja": "末梢神経障害（糖尿病性）",
        "symptoms": {"abnormal_gait", "hind_limb_weakness", "muscle_wasting", "reduced_reflexes"},
        "description": "Peripheral Neuropathy (Diabetic) is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "慢性高血糖による神経損傷で、進行性の後肢脱力と運動失調を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["neurological_exam", "blood_glucose", "physical_exam"],
        "treatment": "PRIMARY: Glycemic control through STRICT dietary management — this is the ONLY validated "
        "approach for managing diabetic neuropathy in degus. Eliminate ALL sugar-containing foods. "
        "Timothy hay ≥80% of diet, sugar-free degu pellets, dark leafy greens only. Target fasting "
        "blood glucose <200 mg/dL. Monitor fructosamine q4-8 weeks. NOTE: Insulin therapy is NOT "
        "standard in degus — dietary management alone is the approach. NEUROPATHIC PAIN MANAGEMENT: "
        "Gabapentin 5-10 mg/kg PO q8-12h (first-line for neuropathic pain — extrapolated from "
        "other species; start low, titrate based on response). Meloxicam 1-2 mg/kg PO/SC q24h "
        "(anti-inflammatory, addresses concurrent musculoskeletal pain). SUPPORTIVE CARE: "
        "B-vitamin supplementation (B1/thiamine, B6/pyridoxine, B12/cobalamin) — extrapolated "
        "from human diabetic neuropathy management. Physical therapy: gentle massage, passive "
        "range of motion exercises for affected limbs. ENVIRONMENTAL MODIFICATION: Lower cage "
        "platforms (≤10 cm between levels), ramps instead of ladders, soft padded bedding. Remove "
        "running wheel if severe ataxia (fall risk). Place food/water at floor level. MONITORING: "
        "Neurological assessment q2-4 weeks — check proprioception, withdrawal reflexes, muscle "
        "mass. Concurrent screening for diabetic cataracts, retinopathy, nephropathy. "
        "PROGNOSIS NOTE: Nerve damage is often partially irreversible once established; early "
        "glycemic control is critical to prevent progression. "
        "References: Edwards (2009) Vet Clin Exot Anim; Jekl et al. (2011).",
        "treatment_ja": "末梢神経障害（糖尿病性）はdeguでは非常に稀。報告例ではインスリン依存性で、プロジンク 0.5-1 IU/動物 SC q12h から開始、家庭での血糖モニタ（耳介穿刺、CGM試験的）と組み合わせる。低糖質・高繊維食。インスリン抵抗性をきたす副腎疾患・甲状腺疾患・肥満を除外。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。"
        "≥80%。空腹時血糖<200 mg/dL目標。デグーではインスリン療法は標準的でない。"
        "【神経障害性疼痛管理】ガバペンチン5-10 mg/kg PO q8-12h（神経障害性疼痛の第一選択 — "
        "他種からの外挿）。メロキシカム1-2 mg/kg PO/SC q24h。【補助】ビタミンB群サプリメント。"
        "理学療法。【環境修正】ケージ段差≤10cm、スロープ、パッド付き床材。重度運動失調時は"
        "回し車撤去。食餌・水を床面に配置。【モニタリング】神経学的評価q2-4週。白内障・"
        "網膜症・腎症の併存症スクリーニング。神経損傷は確立後は部分的に不可逆 — 早期血糖管理が重要。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "疾患の重症度、治療開始の早さ、治療反応により異なる。早期の適切な治療介入で一般に予後改善。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Femoral Fracture",
        "name_ja": "大腿骨骨折",
        "symptoms": {"lameness", "limb_swelling", "non_weight_bearing", "pain"},
        "description": "Femoral Fracture involves traumatic injury requiring assessment of damage extent and appropriate stabilization and repair.",
        "description_ja": "落下、ケージ内外傷、代謝性骨疾患による大腿骨の骨折です。",
        "urgency": "high",
        "recommended_tests": ["limb_xray", "physical_exam", "blood_chemistry"],
        "causes": "Fracture of the femur from falls, cage injuries, or metabolic bone disease.",
        "causes_ja": "デグーにおける大腿骨骨折の原因: 落下、ケージ内外傷、代謝性骨疾患による大腿骨の骨折です。",
        "pathophysiology": "Femoral Fracture is a metabolic/endocrine disorder. Fracture of the femur from falls, cage injuries, or metabolic bone disease. The underlying pathology involves dysregulation of hormonal feedback loops, enzyme activity, or substrate metabolism. This leads to imbalances in circulating hormone levels, electrolytes, or metabolic intermediates that affect cellular function across multiple organ systems. Compensatory mechanisms may temporarily maintain homeostasis but eventually decompensate, leading to progressive clinical deterioration and multi-organ effects.",
        "pathophysiology_ja": "大腿骨骨折はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "Fracture stabilization (splinting, surgical fixation), pain management with multimodal analgesia, restricted activity, and monitoring for healing complications.",
        "treatment_ja": "【デグーにおける大腿骨骨折】\n大腿骨骨折は受傷直後のABCDE評価（気道・呼吸・循環・意識・全身露出）と等張輸液 60-90 mL/kg/h IVボーラスから開始。\n鎮痛：オピオイド（メサドン 0.1-0.3 mg/kg IM, ブプレノルフィン 0.02 mg/kg IM）、安定後にメロキシカム 0.2-0.5 mg/kg PO/SC q24h。\n創傷洗浄（温乳酸リンゲル、低圧パルス）、外科的デブリードマン、創閉鎖または開放管理。\n骨折はデグーの体重と骨質に応じてプレート・ピン・外固定を選択。術後8-12週で画像評価。\n支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。\n【鑑別と経過観察】類似症候を呈する疾患の除外と、治療4-8週後の再評価が予後改善の鍵。重症度・併発症によってはデグーの専門医紹介を考慮する。",
        "prevention": "Prevention of femoral fracture includes appropriate diet formulation, regular health monitoring with blood work, maintaining healthy body weight, avoiding excessive treats or inappropriate foods, and early intervention when subclinical changes are detected.",
        "prevention_ja": "大腿骨骨折の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Good for uncomplicated fractures with appropriate stabilization. Open fractures and those with concurrent injuries carry a more guarded prognosis.",
        "prognosis_ja": "大腿骨骨折の予後: 骨折は適切な固定で予後良好。変性性疾患は進行性だが疼痛管理でQOL維持可能。若齢動物は回復力が高い。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Tibial Fracture",
        "name_ja": "脛骨骨折",
        "symptoms": {"crepitus", "lameness", "limb_swelling", "pain"},
        "description": "Tibial Fracture involves traumatic injury requiring assessment of damage extent and appropriate stabilization and repair.",
        "description_ja": "回し車の怪我や落下による脛骨の骨折です。",
        "urgency": "high",
        "recommended_tests": ["limb_xray", "physical_exam"],
        "causes": "Caused by falls, exercise wheel entrapment, or cage injuries resulting in tibial fracture. Metabolic bone disease may predispose to pathological fractures.",
        "causes_ja": "デグーにおける脛骨骨折の原因: 回し車の怪我や落下による脛骨の骨折です。",
        "pathophysiology": "Mechanical force exceeds bone strength, causing cortical disruption. Associated soft tissue damage, hemorrhage, and inflammation follow. Healing proceeds through hematoma formation, callus development, and remodeling.",
        "pathophysiology_ja": "脛骨骨折はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "Treatment includes fracture stabilization (splinting, pinning, or plating), pain management, restricted activity, and monitoring for healing. Physical rehabilitation may be beneficial.",
        "treatment_ja": "デグー骨折: ① 小型・骨脆弱性が外科的固定を難しくする—保存的治療（副木）が多い。② 安定化: 副木（Robert Jones、軽量副木）またはケージ制限、4-6週で癒合。③ 重症・長管骨は外科的固定（mini IM pin、外固定）—専門医推奨。④ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h。⑤ 開放骨折: 培養感受性後の抗菌薬（草食種は経口β-ラクタム禁忌、エンロフロキサシン 5-10 mg/kg PO q12-24h）。⑥ ケージ制限: ステップ・ハンモック撤去、床に柔らかいパッド、シリンジ給餌で活動を最小化。⑦ 経過: X線3-4週毎、若齢は癒合早い（2-4週）。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。",
        "prevention": "Prevention includes providing safe housing, appropriate handling techniques, supervised exercise, and removal of environmental hazards.",
        "prevention_ja": "脛骨骨折の予防には安全で種に適した飼育環境の整備、鋭利物・危険物の除去、適切な取り扱い技術、他の動物との接触時の監視、温度管理、落下防止策が含まれる。",
        "prognosis": "Good for uncomplicated fractures with appropriate stabilization. Open fractures and those with concurrent injuries carry a more guarded prognosis.",
        "prognosis_ja": "脛骨骨折の予後: 骨折は適切な固定で予後良好。変性性疾患は進行性だが疼痛管理でQOL維持可能。若齢動物は回復力が高い。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Patellar Luxation",
        "name_ja": "膝蓋骨脱臼",
        "symptoms": {"abnormal_gait", "intermittent_lameness", "limb_stiffness"},
        "description": "Patellar Luxation is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "膝蓋骨の脱臼で間欠的な跛行を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["orthopedic_exam", "limb_xray"],
        "causes": "Caused by congenital or acquired displacement of the patella from the trochlear groove, resulting in intermittent lameness.",
        "causes_ja": "デグーにおける膝蓋骨脱臼の原因: 膝蓋骨の脱臼で間欠的な跛行を引き起こします。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "膝蓋骨脱臼はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "CONSERVATIVE MANAGEMENT (Grade I-II): Meloxicam 1-2 mg/kg PO/SC q24h for pain and "
        "inflammation (first-line). Weight management — obesity exacerbates luxation. Environmental "
        "modification: reduce jumping heights, provide ramps, soft bedding. Activity restriction "
        "during acute episodes (cage rest in single-level cage × 2-4 weeks). Most grade I-II "
        "luxations in degus are managed conservatively. SURGICAL MANAGEMENT (Grade III-IV or "
        "refractory): Technically challenging in degus due to small body size (<300g). Trochlear "
        "sulcoplasty, tibial tuberosity transposition, or lateral imbrication — referral to "
        "exotic orthopedic specialist recommended. Isoflurane anesthesia (chamber induction 3-4%, "
        "maintenance 1.5-2.5%, 37°C heated pad). Post-operative: meloxicam 1-2 mg/kg q24h × "
        "7-14 days, cage rest × 4-6 weeks, gradual return to activity. CONCURRENT ASSESSMENT: "
        "Radiographs to evaluate trochlear groove depth and bony abnormalities. Assess for "
        "concurrent metabolic bone disease (MBD) — check calcium, phosphorus, vitamin D (poor "
        "mineralization contributes to patellar instability). Rule out diabetic neuropathy "
        "as contributing factor for hind limb dysfunction. NOTE: Oral β-lactam antibiotics "
        "CONTRAINDICATED if perioperative antibiotics needed — use enrofloxacin 5-10 mg/kg. "
        "References: Quesenberry & Carpenter (2012); Jekl & Redrobe (2013).",
        "treatment_ja": "【保存的管理（Grade I-II）】メロキシカム1-2 mg/kg PO/SC q24h。体重管理。環境修正: "
        "ジャンプ高さ低減、スロープ、柔らかい床材。急性期は活動制限（単段ケージで2-4週間の"
        "ケージレスト）。大多数のGrade I-IIは保存的管理。【外科（Grade III-IV）】デグーの"
        "小型体サイズにより技術的困難 — エキゾチック整形外科専門医への紹介推奨。イソフルラン"
        "麻酔。術後: メロキシカム7-14日、ケージレスト4-6週。【併存評価】X線で滑車溝深度評価。"
        "MBD（Ca/P/VitD）の除外。糖尿病性神経障害の鑑別。周術期抗菌薬が必要な場合は"
        "エンロフロキサシン（経口βラクタム系禁忌）。",
        "prevention": "Maintain ideal body weight through timothy hay-based diet (obesity worsens patellar "
        "instability). Provide cage with appropriate platform heights to reduce impact on joints. "
        "Adequate dietary calcium, phosphorus, and vitamin D for strong bone mineralization. "
        "Avoid breeding from animals with known orthopedic abnormalities. Safe cage design — "
        "no gaps where limbs could get trapped. Reference: Quesenberry & Carpenter (2012).",
        "prevention_ja": "チモシー牧草ベース食による理想体重維持（肥満が膝蓋骨不安定性を悪化）。適切な段差の"
        "ケージ設計。適切なCa/P/VitDの食事摂取。既知の整形外科的異常を持つ個体の繁殖回避。"
        "四肢が挟まるような隙間のない安全なケージ設計。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "膝蓋骨脱臼の予後: 骨折は適切な固定で予後良好。変性性疾患は進行性だが疼痛管理でQOL維持可能。若齢動物は回復力が高い。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Exercise Wheel Injury",
        "name_ja": "回し車による外傷",
        "symptoms": {"lameness", "limb_fracture", "skin_abrasion", "tail_injury"},
        "description": "Exercise Wheel Injury involves traumatic injury requiring assessment of damage extent and appropriate stabilization and repair.",
        "description_ja": "不適切な回し車（金網、スポーク付き）による尾の皮膚剥離、四肢骨折、擦過傷です。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam", "xray", "wound_assessment"],
        "causes": "Caused by inappropriate exercise wheels (wire mesh, spoked designs) leading to tail degloving, limb fractures, and abrasions during use.",
        "causes_ja": "デグーにおける回し車による外傷の原因: 不適切な回し車（金網、スポーク付き）による尾の皮膚剥離、四肢骨折、擦過傷です。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "回し車による外傷はデグーにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "treatment": "THREE COMMON INJURY TYPES require different management: (1) TAIL DEGLOVING (most common): "
        "Clean wound with warm saline irrigation. If only skin/fur lost (no bone exposed): topical "
        "silver sulfadiazine cream q12-24h, non-adherent dressing if tolerated, systemic antibiotics "
        "— enrofloxacin 5-10 mg/kg PO q12h × 7-14 days (oral β-lactams CONTRAINDICATED). If bone "
        "exposed: tail amputation under isoflurane anesthesia at next viable vertebral segment "
        "(chamber induction 3-4%, maintenance 1.5-2.5%, 37°C heated pad). Tail skin does NOT "
        "regenerate in degus (similar to tail degloving — the fur sheath strips off). Pain: "
        "meloxicam 1-2 mg/kg PO/SC q24h × 5-7 days, buprenorphine 0.05-0.1 mg/kg SC q8-12h "
        "acutely. (2) LIMB FRACTURE: Radiographs to assess fracture type and location. Simple "
        "fractures: external coaptation with padded splint or tape splint × 3-4 weeks. Complex/ "
        "comminuted: surgical fixation (intramedullary pin or external fixator — referral to "
        "exotic specialist). Amputation may be necessary for severely comminuted fractures — degus "
        "function well on 3 limbs. (3) FOOT/LIMB ABRASIONS: Clean with chlorhexidine 0.05%, "
        "topical antibiotic ointment, soft padded bedding until healed. CRITICAL: Immediately "
        "REPLACE the offending wheel with a solid-surface wheel ≥25 cm diameter (no mesh, no "
        "spokes, no rungs). References: Quesenberry & Carpenter (2012); Jekl & Redrobe (2013).",
        "treatment_ja": "3つの一般的な外傷タイプの管理: (1) 尾部脱皮（最多）: 温生理食塩水で洗浄。皮膚/毛のみ"
        "喪失（骨露出なし）: 銀スルファジアジンクリーム局所 q12-24h、エンロフロキサシン"
        "5-10 mg/kg PO q12h × 7-14日（経口βラクタム系禁忌）。骨露出: イソフルラン麻酔下で"
        "次の viable椎骨セグメントでの尾切断。デグーの尾皮膚は再生しない。疼痛: メロキシカム"
        "1-2 mg/kg q24h、ブプレノルフィン0.05-0.1 mg/kg SC q8-12h。(2) 四肢骨折: "
        "X線評価。単純骨折: パッド付き副子 × 3-4週。複雑骨折: 外科的固定または断脚。"
        "デグーは3本脚で十分機能可能。(3) 足/四肢擦過傷: クロルヘキシジン0.05%で清拭、"
        "抗菌軟膏。重要: 原因となった回し車を直ちに無隙間表面の≥25cm径回し車に交換。",
        "prevention": "USE ONLY SOLID-SURFACE EXERCISE WHEELS — ≥25 cm diameter for degus (30 cm preferred for "
        "adults). NEVER use wire mesh wheels, spoked wheels, or slatted wheels — these cause tail "
        "degloving, limb entrapment, and foot abrasions. Check wheel daily for damage or wobbling. "
        "Saucer-style wheels are a safe alternative. Running track should be wide enough for the "
        "animal (≥8 cm running surface). Multiple degus may need multiple wheels to prevent "
        "competition-related injuries. Reference: Jekl & Redrobe (2013) BSAVA Manual.",
        "prevention_ja": "無隙間表面の回し車のみ使用 — 直径≥25cm（成体は30cm推奨）。金網・スポーク・スラットの"
        "回し車は絶対に使用しない。毎日の車両点検。ソーサー型回し車も安全な代替。走行面幅"
        "≥8cm。複数のデグーには複数の回し車。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "回し車による外傷の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Toxicosis (Plant Poisoning)",
        "name_ja": "中毒症（植物中毒）",
        "symptoms": {"diarrhea", "drooling", "lethargy", "seizures", "sudden_death"},
        "description": "Toxicosis (Plant Poisoning) is a toxicological condition caused by exposure to harmful substances.",
        "description_ja": "ケージ外での活動中に有毒な観葉植物や処理済み木材を摂取することによる中毒です。",
        "urgency": "emergency",
        "recommended_tests": ["physical_exam", "blood_chemistry", "toxicology_screen"],
        "treatment": "Immediate decontamination if ingestion is recent, activated charcoal if appropriate, specific antidote administration where available, aggressive IV fluid therapy, and intensive monitoring of organ function. Seizure control and thermoregulation as needed.",
        "treatment_ja": "直ちに除染処置（摂取直後の場合）、活性炭投与（適応あれば）、特異的解毒剤の投与、積極的な輸液療法、臓器機能のモニタリング。痙攣コントロールと体温管理を必要に応じて実施。",
        "prognosis": "Prognosis depends on the toxin, amount ingested, and time to treatment. Early decontamination and aggressive supportive care improve outcomes. Severe organ damage may be irreversible.",
        "prognosis_ja": "毒物の種類、摂取量、治療開始までの時間により異なる。早期の除染と積極的な支持療法で予後改善。重度の臓器障害は不可逆的な場合がある。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Zinc Toxicosis",
        "name_ja": "亜鉛中毒",
        "symptoms": {"anemia", "appetite_loss", "jaundice", "lethargy"},
        "description": "Zinc Toxicosis is a toxicological condition caused by exposure to harmful substances.",
        "description_ja": "亜鉛メッキされたケージ部品を齧ることによる溶血性貧血を伴う中毒です。",
        "urgency": "high",
        "recommended_tests": ["cbc", "serum_zinc_level", "blood_chemistry"],
        "causes": "Poisoning from chewing galvanised cage components causing haemolytic anaemia.",
        "causes_ja": "デグーにおける亜鉛中毒の原因: 亜鉛メッキされたケージ部品を齧ることによる溶血性貧血を伴う中毒です。",
        "pathophysiology": "Zinc Toxicosis is a toxicological condition. Poisoning from chewing galvanised cage components causing haemolytic anaemia. Toxic injury occurs through ingestion, inhalation, or dermal absorption of the offending agent. The toxin disrupts cellular processes through specific mechanisms such as enzyme inhibition, receptor interference, oxidative damage, or direct cytotoxicity. Target organs vary by toxin but commonly include the liver (biotransformation), kidneys (excretion), nervous system, and GI tract. Dose-dependent effects range from subclinical changes to fulminant organ failure.",
        "pathophysiology_ja": "亜鉛中毒はデグーにおける中毒性疾患である。有害物質の経口摂取、吸入、または経皮吸収により中毒障害が生じる。毒素は酵素阻害、受容体干渉、酸化的損傷、直接的な細胞毒性などの特定のメカニズムを通じて細胞プロセスを障害する。標的臓器は毒素により異なるが、肝臓（生体内変換）、腎臓（排泄）、神経系、消化管が一般的である。用量依存的に無症候性変化から劇症型臓器不全まで幅広い影響を及ぼす。",
        "treatment": "Treatment of zinc toxicosis in degu requires rapid decontamination and supportive care. If ingestion was recent, emesis induction (where safe for the species) or gastric lavage may reduce absorption. Activated charcoal adsorbs many toxins. Specific antidotes should be administered when available (e.g., vitamin K1 for anticoagulant rodenticides, N-acetylcysteine for acetaminophen). Aggressive IV fluid therapy supports renal excretion and maintains perfusion. Monitor and treat organ-specific damage (hepatic, renal, neurological).",
        "treatment_ja": "デグーにおける亜鉛中毒の治療には迅速な除染と支持療法が必要である。摂取直後であれば催吐（種にとって安全な場合）または胃洗浄により吸収を低減する。活性炭は多くの毒素を吸着する。特異的解毒剤がある場合は投与する（例：抗凝固性殺鼠剤にビタミンK1、アセトアミノフェンにN-アセチルシステイン）。積極的な輸液療法で腎排泄を促進し灌流を維持する。臓器特異的障害（肝、腎、神経）をモニタリングし治療する。",
        "prevention": "Prevention includes removing access to toxic substances, using pet-safe products, proper storage of medications and chemicals, and educating owners about common toxins.",
        "prevention_ja": "亜鉛中毒の予防には有毒物質へのアクセス制限・除去、ペット安全な製品の使用、環境からの有毒植物の除去、薬剤・化学物質の適切な保管、屋外アクセス時の監視、種固有の中毒に関する飼い主教育が必要である。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "亜鉛中毒の予後: 中毒物質と摂取量、治療開始までの時間により予後が大きく異なる。早期除染・解毒で予後改善。",
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Sand Bath Impaction",
        "name_ja": "砂浴びによる閉塞",
        "symptoms": {"abdominal_distension", "appetite_loss", "lethargy", "reduced_fecal_output"},
        "description": "Sand Bath Impaction involves blockage of a body passage or organ requiring intervention to restore normal flow.",
        "description_ja": "砂浴び材料の摂取による消化管閉塞。デグーは砂浴びの砂を食べることがあります。",
        "urgency": "high",
        "recommended_tests": ["abdominal_xray", "physical_exam", "abdominal_palpation"],
        "causes": "Caused by ingestion of sand bath material (chinchilla sand) leading to gastrointestinal obstruction.",
        "causes_ja": "デグーにおける砂浴びによる閉塞の原因: 砂浴び材料の摂取による消化管閉塞。デグーは砂浴びの砂を食べることがあります。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "砂浴びによる閉塞はデグーにおける消化器疾患である。粘膜の完全性、運動性、分泌機能、またはマイクロバイオームバランスの障害を伴う。炎症により上皮バリアが損傷し、吸収不良、体液喪失、細菌トランスロケーションの可能性がある。運動障害（低運動性/うっ滞または亢進）により通過時間と消化効率が変化する。後腸発酵動物では盲腸/結腸フローラの破壊が致死的ディスバイオーシスと腸管毒素症を引き起こしうる。",
        "treatment": "Medical management trial first for partial obstruction: fluid therapy (warmed lactated Ringer's 10-15 mL/kg SC q8-12h), prokinetics (metoclopramide 0.5-1 mg/kg PO/SC q8h — use cautiously, contraindicated if complete obstruction suspected), simethicone 20-40 mg/kg PO q8-12h for gas. Gentle abdominal massage may help mobilize sand. Pain management: meloxicam 1-2 mg/kg PO/SC q24h, buprenorphine 0.05-0.1 mg/kg SC q8-12h for acute pain. Mineral oil or lactulose 0.5 mL/kg PO q12h as lubricant laxative for partial obstruction. If medical management fails (no improvement in 12-24 hours) or complete obstruction confirmed on radiograph: surgical intervention — gastrotomy/enterotomy under isoflurane anesthesia. Post-operative antibiotics: enrofloxacin 5-10 mg/kg SC q12h (AVOID oral beta-lactams). Early assisted feeding with Critical Care for Herbivores post-operatively to restore gut motility. Environmental warming 28-30°C. Monitor fecal output closely — return of normal pellet production indicates resolution.",
        "treatment_ja": "部分閉塞にはまず内科管理を試行: 輸液（加温乳酸リンゲル液 10-15mL/kg SC q8-12h）、消化管運動促進薬（メトクロプラミド 0.5-1mg/kg PO/SC q8h — 慎重使用、完全閉塞疑い時は禁忌）、シメチコン 20-40mg/kg PO q8-12h（ガス対策）。穏やかな腹部マッサージが砂の移動を助ける場合がある。疼痛管理: メロキシカム 1-2mg/kg PO/SC q24h、急性痛にブプレノルフィン 0.05-0.1mg/kg SC q8-12h。部分閉塞に対し鉱油またはラクツロース 0.5mL/kg PO q12h（潤滑性下剤）。内科管理で改善なし（12-24時間）または完全閉塞がレントゲンで確認された場合: 外科的介入 — イソフルラン麻酔下で胃切開/腸切開術。術後抗菌薬: エンロフロキサシン 5-10mg/kg SC q12h（経口βラクタム系禁忌）。術後に草食動物用クリティカルケアによる早期シリンジ給餌で腸管運動回復。環境保温28-30℃。糞便排出を注意深くモニタリング — 正常糞ペレットの産生再開は改善の指標。",
        "prevention": "Supervise sand bath sessions (15-30 min maximum, then remove sand container). Use appropriate chinchilla-grade sand (not fine powder or dusty material). Ensure adequate dietary fiber (timothy hay ad libitum) to reduce pica behavior. Monitor for sand ingestion behavior — some degus are habitual sand eaters and may need restricted access. Do not use clumping cat litter as sand bath substitute. Provide environmental enrichment to reduce boredom-related ingestion.",
        "prevention_ja": "砂浴びセッションの監視（最長15-30分で砂容器を撤去）。適切なチンチラ用砂の使用（微粉末やホコリの多い素材は避ける）。異食行動を減らすため十分な食物繊維の提供（チモシー自由摂取）。砂の摂取行動のモニタリング — 常習的に砂を食べるデグーにはアクセス制限が必要。固まる猫砂を砂浴び代用品として使用しない。退屈に起因する摂取行動を減らすための環境エンリッチメント。",
        "prognosis": "Prognosis depends on disease severity, timeliness of intervention, and response to treatment. Early diagnosis and appropriate therapy generally improve outcomes.",
        "prognosis_ja": "砂浴びによる閉塞の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Social Stress (Single Housing)",
        "name_ja": "社会的ストレス（単独飼育）",
        "symptoms": {"aggression", "barbering", "lethargy", "poor_coat", "stereotypic_behavior"},
        "description": "Social Stress (Single Housing) is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "単独飼育による慢性ストレス。デグーは高度に社会的な動物で、群れで飼育する必要があります。",
        "urgency": "moderate",
        "recommended_tests": ["behavioral_assessment", "environmental_review", "physical_exam"],
        "causes": "Caused by chronic psychological stress from solitary housing. Degus are highly social colonial animals that require group housing for normal behavioral well-being.",
        "causes_ja": "デグーにおける社会的ストレス（単独飼育）の原因: 単独飼育による慢性ストレス。デグーは高度に社会的な動物で、群れで飼育する必要があります。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "社会的ストレス（単独飼育）はデグーにおける行動疾患である。情動調節、ストレス応答、学習行動を制御する脳回路における神経化学的シグナル伝達（セロトニン、ドーパミン、ノルエピネフリン、GABA）の調節障害を伴う。環境ストレス、不適切な社会化、不適切な飼育管理、基礎疾患が行動異常を惹起・悪化させることがある。慢性ストレスは視床下部-下垂体-副腎系を活性化し、コルチゾール上昇と免疫抑制を引き起こす。",
        "treatment": "THE MOST IMPORTANT TREATMENT IS COMPANION INTRODUCTION — degus are obligately social "
        "colonial animals and single housing is a welfare concern. (1) COMPANION INTRODUCTION "
        "(PRIMARY): Introduce a same-sex companion (to prevent breeding). Use split-cage method: "
        "mesh divider allowing visual, olfactory, and auditory contact for 1-2 weeks before full "
        "contact. Swap sides daily to mix scents. Neutral territory for first meeting (clean, "
        "unfamiliar cage with new bedding). Supervise initial interactions — mild chasing/mounting "
        "is normal dominance behavior; separate only if drawing blood. Ideal: introduce young degu "
        "(3-6 months) to established adult. Group of 3-4 is optimal (natural colony size). "
        "(2) ENVIRONMENTAL ENRICHMENT: Large cage (minimum 80×50×100 cm for 2-3 degus), multiple "
        "levels with ramps, ≥2 running wheels (≥25 cm solid surface), dust bath (chinchilla sand) "
        "2-3× weekly, foraging opportunities (scatter feed), tunnels, chew toys, multiple hiding "
        "spots. (3) DIETARY IMPROVEMENT: Timothy hay ad libitum, appropriate sugar-free pellets, "
        "fresh water. Vitamin supplementation if immunocompromised. (4) SYMPTOMATIC TREATMENT: "
        "Self-barbering: meloxicam 1-2 mg/kg PO/SC q24h if skin lesions present. Weight loss: "
        "syringe feeding with Critical Care if needed. (5) BEHAVIORAL MONITORING: Assess "
        "improvement over 4-8 weeks after companion introduction. Look for resumption of "
        "grooming, vocalizations (degus have >15 distinct calls), and play behavior. "
        "If companion introduction is truly impossible (severe aggression): maximize environmental "
        "enrichment and human interaction — but this is SUBOPTIMAL and not recommended long-term. "
        "References: Ebensperger & Caiozzi (2002) Rev Chilena Hist Nat; Long (2007) The Degu "
        "Handbook; Quesenberry & Carpenter (2012).",
        "treatment_ja": "【最も重要な治療はコンパニオンの導入】デグーは社会性が義務的な群れ動物であり、単独飼育は"
        "動物福祉上の問題。(1) 仲間の導入（最重要）: 同性の個体を導入。スプリットケージ法: "
        "メッシュ仕切りで1-2週間の視覚/嗅覚/聴覚接触後にフルコンタクト。毎日側面を交換して"
        "匂いを混合。初対面は中立領域で。軽い追いかけ/マウンティングは正常な優位行動。"
        "理想: 若い個体（3-6ヶ月）を成体に紹介。3-4頭が最適。(2) 環境エンリッチメント: "
        "大型ケージ（最低80×50×100cm）、回し車≥2台、砂浴び週2-3回、フォレージング。"
        "(3) 食事改善: チモシー牧草自由摂取。(4) 対症療法: 自己バーバリングにメロキシカム"
        "1-2 mg/kg。体重減少にクリティカルケア。(5) 行動モニタリング: 仲間導入後4-8週間で"
        "評価。毛繕い、発声（デグーは15種以上の異なる鳴き声を持つ）、遊び行動の再開を確認。"
        "仲間導入が不可能な場合: 環境エンリッチメント最大化 — だし長期的には次善策であり"
        "推奨されない。",
        "prevention": "NEVER house degus alone — they are obligately social colonial animals. Minimum pair, ideally "
        "3-4 same-sex group. When one member of a pair dies, introduce a new companion within 2-4 "
        "weeks (grieving degus decline rapidly). Obtain degus in established pairs/groups from "
        "breeders when possible. Provide adequate space, enrichment, and resources (food bowls, "
        "water bottles, hiding spots) to prevent social stress even in groups. "
        "Reference: Ebensperger & Caiozzi (2002); Long (2007) The Degu Handbook.",
        "prevention_ja": "デグーを絶対に単独飼育しない — 社会性が義務的な群れ動物。最低ペア、理想は3-4頭の"
        "同性グループ。ペアの一方が死亡したら2-4週間以内に新しい仲間を導入（喪に服すデグーは"
        "急速に衰退）。可能であればブリーダーから確立されたペア/グループで入手。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "社会的ストレス（単独飼育）の予後: 早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Corneal Dystrophy",
        "name_ja": "角膜ジストロフィー",
        "symptoms": {"corneal_opacity", "eye_discharge", "vision_loss"},
        "description": "Corneal Dystrophy is an ophthalmic condition affecting the eye or surrounding structures.",
        "description_ja": "遺伝性または加齢性の変性性角膜疾患。糖尿病と関連する可能性があります。",
        "urgency": "low",
        "recommended_tests": ["ophthalmic_exam", "blood_glucose", "physical_exam"],
        "causes": "Caused by hereditary or age-related degenerative changes in the cornea, potentially associated with diabetes mellitus and chronic metabolic derangement.",
        "causes_ja": "デグーにおける角膜ジストロフィーの原因: 遺伝性または加齢性の変性性角膜疾患。糖尿病と関連する可能性があります。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "角膜ジストロフィーはデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "Topical ophthalmic medication (antibiotics, anti-inflammatories, lubricants as indicated), pain management, protection from self-trauma, and monitoring for complications.",
        "treatment_ja": "【デグーにおける角膜ジストロフィー】\n角膜ジストロフィーに対し、フルオレセイン染色・シルマー試験・眼圧測定・スリットランプ検査で病変を評価。\n細菌性疑い: 抗菌点眼（オフロキサシン 3%, トブラマイシン 0.3%）q4-6h × 7-14日、培養感受性で調整。\nぶどう膜炎・角膜炎: 抗炎症点眼（ジクロフェナク 0.1%, デキサメサゾン 0.1%）、原疾患検索。\n自傷防止: エリザベスカラーまたは透明アイガード、近隣表面のクリーンチェック。\n閉塞性または重度症例は眼科専門医紹介を推奨。\n支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。\n【鑑別と経過観察】類似症候を呈する疾患の除外と、治療4-8週後の再評価が予後改善の鍵。重症度・併発症によってはデグーの専門医紹介を考慮する。",
        "prevention": "Prevention includes appropriate husbandry, balanced nutrition, regular veterinary examinations, stress reduction, and prompt treatment of early signs of illness.",
        "prevention_ja": "角膜ジストロフィーの予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "角膜ジストロフィーの予後: 早期治療で視機能温存可能。慢性疾患は長期管理が必要。網膜疾患は不可逆的な場合がある。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Glaucoma",
        "name_ja": "緑内障",
        "symptoms": {"enlarged_eye", "eye_pain", "eye_redness", "vision_loss"},
        "description": "Glaucoma is an ophthalmic condition affecting the eye or surrounding structures.",
        "description_ja": "眼内圧の上昇による視神経損傷と進行性視力喪失です。",
        "urgency": "high",
        "recommended_tests": ["tonometry", "ophthalmic_exam", "physical_exam"],
        "causes": "Caused by impaired aqueous humor drainage leading to elevated intraocular pressure, potentially secondary to uveitis, lens luxation, or congenital drainage angle abnormalities.",
        "causes_ja": "デグーの眼科に影響する正確な原因は不明または多因子性。遺伝的素因・環境因子・免疫調節異常・不顕性感染・代謝障害が寄与因子として考えられる。個々の症例での主原因特定にはさらなる調査が必要。",
        "pathophysiology": "The pathological process involves tissue injury, inflammatory response, and progressive functional impairment. Without intervention, compensatory mechanisms may be overwhelmed, leading to clinical deterioration.",
        "pathophysiology_ja": "デグーの眼科に影響する正確な病態生理は完全には解明されていない。遺伝的素因・環境因子・免疫調節異常を含む多因子性メカニズムが関与すると考えられる。眼科組織における炎症性・代謝性・構造的変化が進行性の臨床徴候をもたらす。デグーにおける疾患メカニズムの完全な解明にはさらなる研究が必要。",
        "treatment": "EMERGENCY — elevated IOP causes irreversible retinal/optic nerve damage within hours. "
        "MEDICAL MANAGEMENT (FIRST-LINE): Topical latanoprost 0.005% — 1 drop affected eye q12-24h "
        "(prostaglandin analog, increases uveoscleral outflow; may not be effective in all rodent "
        "species). Topical dorzolamide 2% — 1 drop q8-12h (carbonic anhydrase inhibitor, reduces "
        "aqueous production). Topical timolol 0.5% — 1 drop q12h (beta-blocker, reduces aqueous "
        "production; use with caution in small rodents due to systemic absorption). Systemic "
        "mannitol 1-2 g/kg IV over 20 min (osmotic diuretic for acute IOP crisis — only in "
        "hospital setting). PAIN MANAGEMENT: Meloxicam 1-2 mg/kg PO/SC q24h. Buprenorphine "
        "0.05-0.1 mg/kg SC q8-12h for acute ocular pain. RULE OUT UNDERLYING CAUSE: Uveitis "
        "(anterior chamber flare, miosis) — topical prednisolone acetate 1% q6-8h if uveitis "
        "confirmed. Lens luxation — may require surgical intervention. Diabetic cataracts — "
        "common in degus, may contribute to lens-induced uveitis → secondary glaucoma. SURGICAL: "
        "Enucleation for end-stage painful blind eye — definitive treatment for unresponsive "
        "glaucoma. Under isoflurane anesthesia (37°C heated pad). Degus adapt well to monocular "
        "vision. Post-operative: meloxicam × 5-7 days, enrofloxacin 5-10 mg/kg PO q12h × 7 days "
        "(oral β-lactams CONTRAINDICATED). MONITORING: Tonometry at each visit to track IOP "
        "response. Normal IOP in rodents approximately 10-20 mmHg. "
        "References: Williams (2012) Vet Ophthalmol; Quesenberry & Carpenter (2012).",
        "treatment_ja": "【緊急 — 眼圧上昇は数時間以内に不可逆的な網膜/視神経損傷を引き起こす】"
        "【内科管理（第一選択）】ラタノプロスト0.005%点眼 q12-24h。ドルゾラミド2%点眼 "
        "q8-12h。チモロール0.5%点眼 q12h（小型齧歯類では全身吸収に注意）。急性IOP危機: "
        "マンニトール1-2 g/kg IV（入院下のみ）。【疼痛管理】メロキシカム1-2 mg/kg。"
        "ブプレノルフィン0.05-0.1 mg/kg SC q8-12h。【原因除外】ぶどう膜炎（プレドニゾロン"
        "点眼）。水晶体脱臼。糖尿病性白内障（デグーで一般的 → 水晶体誘発性ぶどう膜炎 → "
        "続発性緑内障）。【外科】末期の有痛性盲目眼には眼球摘出が根治的治療。イソフルラン"
        "麻酔（37℃加温パッド）。デグーは単眼視でよく適応。術後: メロキシカム5-7日、"
        "エンロフロキサシン5-10 mg/kg q12h × 7日（経口βラクタム系禁忌）。",
        "prevention": "No specific prevention for primary glaucoma. Prompt treatment of uveitis and ocular "
        "infections reduces secondary glaucoma risk. Optimal glycemic control prevents diabetic "
        "cataracts which can lead to lens-induced uveitis and secondary glaucoma. Regular "
        "ophthalmic examination in senior degus and diabetic degus. "
        "Reference: Williams (2012) Vet Ophthalmol.",
        "prevention_ja": "原発性緑内障の特異的予防法はない。ぶどう膜炎と眼感染症の迅速な治療で続発性緑内障"
        "リスクを軽減。最適な血糖管理で糖尿病性白内障を予防。高齢デグーと糖尿病デグーの"
        "定期眼科検査。",
        "prognosis": "Prognosis depends on severity, timeliness of treatment, and response to therapy. Early intervention generally improves outcomes.",
        "prognosis_ja": "特発性疾患の予後は個々の症例により変動する。自然寛解する場合もあるが、慢性再発性の経過をたどることもある。対症療法と支持療法が治療の中心。定期的な再評価により治療方針を調整する。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Cage Aggression (Territorial)",
        "name_ja": "ケージ攻撃性（縄張り）",
        "symptoms": {"aggression", "bite_wounds", "hair_loss", "stress_signs"},
        "description": "Cage Aggression (Territorial) is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "デグー間の縄張り攻撃性で、特に確立されたグループに新しいメンバーを導入する際に見られます。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam", "wound_assessment", "behavioral_assessment"],
        "treatment": "IMMEDIATE: Separate fighting degus to prevent further injury. Assess all involved animals "
        "for bite wounds. WOUND MANAGEMENT: Clean wounds with warm saline irrigation. Chlorhexidine "
        "0.05% for superficial wounds. Deep puncture wounds or abscesses: lance and drain under "
        "isoflurane anesthesia if needed, flush with saline. Systemic antibiotics for infected "
        "wounds: enrofloxacin 5-10 mg/kg PO/SC q12h × 7-14 days (oral β-lactams CONTRAINDICATED). "
        "Pain: meloxicam 1-2 mg/kg PO/SC q24h × 3-5 days. BEHAVIORAL MANAGEMENT — ROOT CAUSE: "
        "(1) Improper introduction: Reintroduce using split-cage method (mesh divider × 1-2 weeks, "
        "swap sides daily, neutral territory for first full contact). (2) Overcrowding: Ensure "
        "adequate cage size (minimum 80×50×100 cm for 2-3 degus). Provide multiple of each resource "
        "(food bowls, water bottles, hiding spots, wheels) — resource competition triggers aggression. "
        "(3) Hormonal: Intact males may fight — consider castration (reduces territorial aggression "
        "within 4-8 weeks). (4) Insufficient enrichment: Boredom increases aggression — add foraging "
        "opportunities, tunnels, multiple levels. (5) Established hierarchy disruption: Adding or "
        "removing a member destabilizes group dynamics — monitor closely for 2-4 weeks. If aggression "
        "is severe and persistent despite reintroduction attempts, permanent separation is necessary. "
        "Do NOT leave fighting degus together — injuries can be fatal. "
        "References: Long (2007) The Degu Handbook; Quesenberry & Carpenter (2012).",
        "treatment_ja": "【即時】争っているデグーを分離し更なる外傷を防止。全関係個体の咬傷を評価。"
        "【創傷管理】温生理食塩水で洗浄。クロルヘキシジン0.05%。深い刺傷/膿瘍: イソフルラン"
        "麻酔下で切開排膿。感染創: エンロフロキサシン5-10 mg/kg PO/SC q12h × 7-14日"
        "（経口βラクタム系禁忌）。疼痛: メロキシカム1-2 mg/kg q24h。【行動管理 — 根本原因】"
        "(1) 不適切な導入: スプリットケージ法で再導入。(2) 過密飼育: 適切なケージサイズ確保、"
        "各リソースを複数設置。(3) ホルモン: 未去勢雄は争い — 去勢検討（4-8週間で縄張り攻撃性"
        "低減）。(4) エンリッチメント不足。(5) 確立された序列の撹乱。重度で持続的な攻撃性は"
        "恒久的分離が必要。争っているデグーを一緒にしない — 外傷は致死的になりうる。",
        "prognosis": "Good prognosis for bite wound healing with appropriate treatment. Behavioral prognosis "
        "depends on underlying cause: improper introduction (good with proper split-cage method), "
        "resource competition (good with environmental modification), hormonal aggression (good "
        "with castration). Some individuals are temperamentally incompatible and require permanent "
        "separation. Severe bite wounds with deep tissue involvement carry risk of abscess formation "
        "and sepsis if untreated.",
        "prognosis_ja": "適切な治療で咬傷治癒の予後良好。行動学的予後は原因による: 不適切な導入（適切な"
        "スプリットケージ法で良好）、リソース競合（環境修正で良好）、ホルモン性攻撃（去勢で"
        "良好）。一部の個体は気質的に不適合で恒久的分離が必要。",
        "onset_pattern": {"acute", "subacute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Hypothyroidism",
        "name_ja": "甲状腺機能低下症",
        "symptoms": {"cold_intolerance", "lethargy", "obesity", "poor_coat"},
        "description": "Hypothyroidism is a clinical condition requiring veterinary evaluation, diagnosis, and appropriate treatment.",
        "description_ja": "甲状腺ホルモン産生の低下による代謝低下と体重増加です。",
        "urgency": "low",
        "recommended_tests": ["thyroid_panel", "blood_chemistry", "physical_exam"],
        "causes": "Reduced thyroid hormone production causing metabolic slowdown and weight gain.",
        "causes_ja": "デグーにおける甲状腺機能低下症の原因: 甲状腺ホルモン産生の低下による代謝低下と体重増加です。",
        "pathophysiology": "Hypothyroidism is a metabolic/endocrine disorder. Reduced thyroid hormone production causing metabolic slowdown and weight gain. The underlying pathology involves dysregulation of hormonal feedback loops, enzyme activity, or substrate metabolism. This leads to imbalances in circulating hormone levels, electrolytes, or metabolic intermediates that affect cellular function across multiple organ systems. Compensatory mechanisms may temporarily maintain homeostasis but eventually decompensate, leading to progressive clinical deterioration and multi-organ effects.",
        "pathophysiology_ja": "甲状腺機能低下症はデグーにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "treatment": "IMPORTANT NOTE: True hypothyroidism is rare and poorly documented in degus. Differential "
        "diagnosis of lethargy, obesity, and poor coat should first rule out diabetes mellitus "
        "(much more common in degus), malnutrition, chronic stress, and aging-related decline. "
        "DIAGNOSTIC CONFIRMATION: Total T4 and free T4 measurement (reference ranges not well "
        "established for degus — interpret cautiously; extrapolate from rat/guinea pig reference "
        "ranges). TSH stimulation test (limited availability for exotic species). THYROID HORMONE "
        "REPLACEMENT: Levothyroxine (L-thyroxine) 10-20 μg/kg PO q24h — starting dose, titrate "
        "based on clinical response and T4 monitoring q2-4 weeks. Administer on empty stomach "
        "30-60 minutes before feeding for optimal absorption. MONITORING: T4 levels q4-8 weeks "
        "during dose adjustment, then q3-6 months once stable. Watch for signs of iatrogenic "
        "hyperthyroidism (tachycardia, weight loss, restlessness, polyphagia). WEIGHT MANAGEMENT: "
        "Timothy hay-based diet (≥80%), no sugar/fruit (concurrent diabetes risk). Increased "
        "exercise as activity improves with treatment. CONCURRENT DISEASE: Screen for diabetes "
        "mellitus (blood glucose, fructosamine) — hypothyroidism may worsen insulin resistance. "
        "Skin/coat condition should improve within 4-8 weeks of adequate replacement. Lifelong "
        "treatment is typically required. "
        "References: Quesenberry & Carpenter (2012); Edwards (2009) Vet Clin Exot Anim.",
        "treatment_ja": "deguでの甲状腺機能低下症は稀で診断は慎重に。低T4のみでは診断不確実（病気個体は普遍的にT4低下＝euthyroid sick syndrome）。TSH刺激試験で確認後、レボチロキシン 0.01-0.02 mg/kg PO q12-24h試用。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。"
        "被毛不良の鑑別診断として、まず糖尿病（デグーで遥かに一般的）、栄養不良、慢性ストレス、"
        "加齢変化を除外すべき。【診断確定】総T4と遊離T4測定（デグーの基準値は確立されていない "
        "— ラット/モルモットの基準値から外挿して慎重に解釈）。TSH刺激試験。"
        "【甲状腺ホルモン補充】レボチロキシン10-20 μg/kg PO q24h — 開始用量、臨床反応と"
        "T4モニタリングに基づき漸増（q2-4週）。空腹時投与（給餌30-60分前）。"
        "【モニタリング】用量調整中はT4をq4-8週、安定後q3-6ヶ月。医原性甲状腺機能亢進症の"
        "徴候に注意（頻脈、体重減少、多食）。【体重管理】チモシー牧草ベース食、糖分禁忌。"
        "【併存症】糖尿病スクリーニング — 甲状腺機能低下がインスリン抵抗性を悪化させうる。"
        "生涯にわたる治療が通常必要。",
        "prevention": "Prevention of hypothyroidism includes appropriate diet formulation, regular health monitoring with blood work, maintaining healthy body weight, avoiding excessive treats or inappropriate foods, and early intervention when subclinical changes are detected.",
        "prevention_ja": "甲状腺機能低下症の予防には適切な食事設計、血液検査を含む定期的な健康モニタリング、健康体重の維持、過剰なおやつや不適切な食事の回避、無症候性変化の早期発見時の迅速な介入が含まれる。",
        "prognosis": "Generally good to fair with appropriate treatment and follow-up care. Prognosis improves with early diagnosis and owner compliance.",
        "prognosis_ja": "甲状腺機能低下症の予後: 多くの内分泌疾患は適切な薬物療法で長期管理可能。定期的なホルモン値モニタリングと用量調整が重要。",
        "onset_pattern": {"chronic"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    # =========================================================================
    # ADDITIONAL DISEASES — DERMATOLOGICAL, TRAUMATIC
    # =========================================================================
    {
        "name": "Bumblefoot (Pododermatitis)",
        "name_ja": "趾瘤症（バンブルフット）",
        "symptoms": {"lameness", "swollen_feet", "foot_lesions", "lethargy", "appetite_loss"},
        "description": "Pressure sore infection of the plantar surface of the feet, common in caged rodents.",
        "description_ja": "足底面の圧迫性潰瘍・感染症。硬い床材、肥満、不活動がリスク因子。"
        "初期は発赤・腫脹、進行すると深部感染・骨髄炎。"
        "ケージ飼育のデグーで比較的多い。",
        "pathophysiology": "Chronic pressure on plantar surface causes ischemic necrosis of skin, secondary bacterial infection (Staphylococcus spp.), and potential deep tissue involvement.",
        "pathophysiology_ja": "硬い床面での持続的圧迫→足底皮膚の虚血性壊死→"
        "Staphylococcus属等の二次細菌感染→蜂窩織炎→膿瘍形成→"
        "重症例では腱・骨への波及（骨髄炎）。肥満個体でリスク上昇。",
        "causes": "Wire-bottom cages, hard surfaces, obesity, inactivity, poor hygiene.",
        "causes_ja": "金網底ケージ、硬い床材、肥満、運動不足、不衛生な飼育環境。爪の過長も寄与。",
        "treatment": "Wound care, antibiotics, padding, address husbandry issues.",
        "treatment_ja": "デグー足底皮膚炎（バンブルフット/Pododermatitis）: 環境改善が治療の根幹。① 環境改善: 床材を柔らかいもの（タオル、Vetbed、人工芝）に変更、湿潤回避、止まり木の太さ・形状を見直す（鳥）。② 局所処置: ぬるま湯と0.05%クロルヘキシジン洗浄 q12h、外用シルバースルファジアジン or Manuka honey、患部包帯（鳥はballブートやテープシューズ）。③ 重症例（潰瘍・骨髄炎）: 培養感受性後の全身抗菌薬—エンロフロキサシン 10-15 mg/kg PO/IM q12-24h、アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h（鳥含む）、4-8週継続。④ 外科的デブリードマン（壊死組織除去）必要例あり。⑤ 鎮痛: メロキシカム 0.5-1 mg/kg PO q12-24h。⑥ 肥満は最大のリスク因子—体重管理（特に飛ばない大型鳥、ウサギ、モルモット）。⑦ ビタミンA欠乏（鳥）も誘因—食事改善（種子食偏重を脱却）。支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。"
        "中等度：全身性抗菌薬（エンロフロキサシン5mg/kg BID）＋NSAIDs。"
        "重度（膿瘍・骨髄炎）：外科的デブリードマン＋長期抗菌薬。"
        "床材を柔らかいもの（フリース等）に変更が必須。",
        "prevention": "Soft bedding, avoid wire-bottom cages, maintain healthy weight, exercise.",
        "prevention_ja": "柔らかい床材の使用（金網底禁止）。適切な体重管理。"
        "十分な運動スペース。爪の定期的トリミング。衛生管理。",
        "prognosis": "Good if mild; guarded with deep infection or osteomyelitis.",
        "prognosis_ja": "軽度は床材改善＋治療で予後良好。骨髄炎に進行した場合は予後慎重（断趾が必要な場合あり）。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam", "bacterial_culture_sensitivity", "radiographs"],
        "onset_pattern": {"subacute", "chronic"},
        "age_predisposition": {"adult", "senior"},
    },
    {
        "name": "Tail Degloving Injury",
        "name_ja": "尾部皮膚剥脱損傷（テイルスリップ）",
        "symptoms": {"tail_injury", "bleeding", "pain", "tail_abnormality"},
        "description": "Traumatic loss of tail skin when grabbed improperly, a common and unique injury in degus.",
        "description_ja": "デグー特有の防御機構で、尾を掴まれると皮膚が容易に剥離する。"
        "不適切な保定や取り扱い事故で発生。露出した尾骨は壊死→"
        "断尾が必要。デグー飼育で最も注意すべき外傷。",
        "pathophysiology": "Degu tail skin has a unique structure allowing degloving as a predator-escape mechanism. Exposed tail tissue desiccates and undergoes avascular necrosis.",
        "pathophysiology_ja": "デグーの尾部皮膚は捕食者からの逃避機構として容易に剥離する構造。"
        "皮膚剥離→露出した皮下組織・骨の乾燥→無血管性壊死→"
        "二次感染のリスク。自然治癒はせず、壊死部位の断尾が必要。",
        "causes": "Improper handling (grabbing by tail), cage-related accidents, fighting.",
        "causes_ja": "不適切な保定（尾を掴む）、ケージ回し車での事故、同居個体との喧嘩、ケージの隙間に尾が挟まる。",
        "treatment": "Tail amputation proximal to the injury site under general anesthesia.",
        "treatment_ja": "損傷部位より近位での断尾術（全身麻酔下）が標準治療。"
        "術後：抗菌薬（エンロフロキサシン5mg/kg BID、5〜7日間）、"
        "疼痛管理（メロキシカム0.2mg/kg SID）、エリザベスカラー。"
        "皮膚のみの部分剥離：清浄＋抗菌軟膏で保存的に管理可能な場合あり。",
        "prevention": "Never grab a degu by the tail; proper handling technique education.",
        "prevention_ja": "絶対に尾を掴まない。両手で体を包み込む保定法の習得。"
        "ケージの回し車は尾が挟まらないソリッドタイプを使用。"
        "ケージの隙間を確認・修正。",
        "prognosis": "Good after amputation; degus adapt well to tail loss.",
        "prognosis_ja": "断尾後の予後は良好。デグーは尾の喪失に良く適応する。"
        "バランス能力への影響は軽微。感染予防が重要。",
        "urgency": "high",
        "recommended_tests": ["physical_exam", "radiographs"],
        "onset_pattern": {"acute"},
        "age_predisposition": {"adult", "young", "senior"},
    },
    {
        "name": "Degu Diabetes-Induced Cataracts",
        "name_ja": "デグー糖尿病性白内障",
        "symptoms": {"vision_loss", "eye_cloudy", "weight_loss", "lethargy", "excessive_thirst", "excessive_urination"},
        "description": "Common degu eye disease secondary to diabetes mellitus, which is highly prevalent in pet degus due to their unique sugar intolerance. Bilateral progressive cataracts develop within months of dietary sugar exposure. PREVENTION through strict no-sugar diet is critical - degus evolved to digest fibrous Andean plants, NOT fruit or sweet treats.",
        "description_ja": "ペットデグーで高頻度の糖尿病に続発する一般的眼疾患（独特の糖不耐性のため）。食事糖暴露後数ヶ月以内に両側進行性白内障発症。厳格な無糖食による予防が決定的 — デグーはフルーツや甘い食物でなく繊維質アンデス植物消化に進化。",
        "pathophysiology": "Degus (Octodon degus) have UNIQUE GLUCOSE INTOLERANCE - their pancreatic beta cells produce a low-affinity insulin variant (degu-specific insulin) that is poorly recognized by mammalian insulin receptors. Even minimal dietary sugar (fruits, treats, sweet vegetables, dairy) overwhelms compensatory mechanisms -> persistent hyperglycemia -> formation of cataracts via polyol pathway: glucose -> aldose reductase -> sorbitol accumulates in lens -> osmotic damage to lens fibers + protein denaturation -> opacification. Cataract progression: clear lens -> peripheral haziness -> cortical vacuolation -> mature cataract -> hypermature lens with leakage; usually bilateral, symmetric. Other diabetes complications: weight loss despite polyphagia, polyuria/polydipsia, weakness, recurrent infections, cardiomyopathy, glomerulopathy. Onset of cataracts: as early as 3-6 months after sugar introduction; commonly diagnosed in degus 1-3 years old (after months of inappropriate feeding). Pathognomonic: degu + bilateral cataracts = diabetes-related almost universally. Distinguished from senile cataracts (rare, occur in older animals only) by age and bilateral symmetric pattern.",
        "pathophysiology_ja": "デグー（Octodon degus）は独特のグルコース不耐性 — 膵β細胞は哺乳類インスリン受容体に認識されにくい低親和性インスリン変異体（デグー特異的インスリン）を産生。最小限の食事糖（果物、おやつ、甘い野菜、乳製品）でも代償機序を超え→持続性高血糖→ポリオール経路で白内障形成：グルコース→アルドース還元酵素→ソルビトールが水晶体蓄積→水晶体線維への浸透圧損傷＋タンパク質変性→混濁。白内障進行：透明水晶体→末梢混濁→皮質空胞化→成熟白内障→漏出を伴う過熟水晶体；通常両側、対称。他糖尿病合併症：多食にも関わらず体重減少、多尿/多飲、衰弱、反復感染、心筋症、糸球体症。白内障発症：糖導入後3-6ヶ月という早さ；通常1-3歳デグーで診断（数ヶ月の不適切給餌後）。病態的：デグー＋両側白内障＝ほぼ普遍的に糖尿病関連。年齢と両側対称パターンで老人性白内障（稀、高齢動物のみ）と鑑別。",
        "causes": "Type 2-like diabetes mellitus from dietary sugar exposure in glucose-intolerant species. Specific dietary causes: fruits (any kind - sweet potatoes, carrots when given regularly, apples, banana, berries), commercial 'treats' marketed for small pets, sweetened cereals, dried fruit in seed mixes, dairy products, honey/sugar in any form, even some pellets containing sugar/molasses. Risk factors: pet store/commercial diet inadequacy, owner unfamiliarity with degu-specific dietary needs, multi-degu cages where treats given to one cause exposure to all.",
        "causes_ja": "グルコース不耐性種における食事糖暴露からの2型様糖尿病。具体的食事原因：果物（任意の種類 — 定期給餌時のサツマイモ、ニンジン、リンゴ、バナナ、ベリー）、小動物用市販「おやつ」、甘味添加シリアル、種子ミックス中のドライフルーツ、乳製品、任意形式の蜂蜜/砂糖、糖/糖蜜含むペレットさえも。リスク：ペットストア/市販食不足、デグー特異的食事ニーズへの飼い主不慣れ、おやつ与えで全体暴露の多頭ケージ。",
        "treatment": "(1) IMMEDIATE DIET CONVERSION (essential): eliminate ALL sugar sources - no fruit, no treats, no sweet vegetables; provide chinchilla pellets (or guinea pig/rabbit pellets without molasses), unlimited timothy hay, leafy greens (romaine, dandelion, broccoli), occasional rolled oats or sunflower seeds (limited as fat treat). Read all ingredient labels carefully. (2) Monitor blood glucose: target fasting glucose <200 mg/dL (degu fasting normal 90-150 mg/dL); check 1-2 weeks after diet change. (3) Insulin therapy if hyperglycemia persists despite diet (advanced diabetes): controversial in degus due to insulin variant interaction with mammalian insulin; some success reported with NPH insulin 0.5-1 IU SC q12h, monitor blood glucose curves. (4) Cataract management: NO MEDICAL TREATMENT REVERSES established cataracts; surgical phacoemulsification possible but rarely performed in degus due to cost, anesthesia risk, expertise needed; most owners accept blindness with good quality of life adaptation. (5) Aldose reductase inhibitors (research only - not commonly available): may slow cataract progression if used early. (6) Dietary cinnamon supplementation 0.5 g/kg PO q24h - some evidence for blood glucose modulation in glucose-intolerant species. (7) Encourage weight loss if obese (insulin resistance contributor). (8) Bedside care for blind degus: stable cage layout (no movements), familiar smells/voice cues, ramps for elevation, no upper levels (fall risk), companion degu for guidance. (9) Treat secondary complications: UTIs (common), corneal ulcers (from facial trauma when blind), dental disease (poor grooming).",
        "treatment_ja": "(1)即時食事転換（必須）：全糖源除去 — 果物なし、おやつなし、甘い野菜なし；チンチラペレット（または糖蜜なしのモルモット/ウサギペレット）、無制限ティモシー乾草、葉物野菜（ロメイン、タンポポ、ブロッコリー）、時折ロールドオート/ヒマワリ種（脂肪おやつとして制限）提供。全成分表示注意深く読む。(2)血糖モニタ：目標空腹時血糖<200 mg/dL（デグー空腹時正常90-150 mg/dL）；食事変更1-2週後にチェック。(3)食事にも関わらず高血糖持続時のインスリン療法（進行糖尿病）：哺乳類インスリンとのデグーインスリン変異体相互作用のため議論あり；NPHインスリン 0.5-1 IU SC q12hで一部成功報告、血糖カーブモニタ。(4)白内障管理：確立白内障を内科治療で逆転不可；外科的水晶体乳化術可能だがコスト・麻酔リスク・専門性のためデグーで稀；飼い主多くは良好QOL適応で失明受容。(5)アルドース還元酵素阻害薬（研究のみ — 一般的入手不可）：早期使用で白内障進行減速可能性。(6)食事シナモン補充 0.5 g/kg PO q24h — グルコース不耐性種での血糖調節エビデンス一部あり。(7)肥満時の体重減少促進（インスリン抵抗性寄与因子）。(8)失明デグーのベッドサイドケア：安定ケージレイアウト（移動なし）、慣れた匂い/声合図、高度ランプ、上層なし（落下リスク）、誘導用同伴デグー。(9)二次合併症治療：UTI（頻発）、角膜潰瘍（失明時の顔面外傷から）、歯科疾患（グルーミング不良）。",
        "prognosis": "Cataracts are irreversible once established. With strict diet conversion early in disease (mild hyperglycemia, no cataracts yet): may prevent cataract development. Established cataracts: blindness permanent; degus adapt well, normal lifespan possible (5-8 years) if other diabetes complications managed. Late-stage uncontrolled diabetes: cardiomyopathy, kidney disease, recurrent infections shorten lifespan to 2-4 years.",
        "prognosis_ja": "確立後の白内障は不可逆。疾患早期での厳格食事転換（軽度高血糖、白内障未発症）：白内障発症予防可能性。確立白内障：永続的失明；デグーは良好適応、他糖尿病合併症管理で正常寿命可能（5-8歳）。後期コントロール不良糖尿病：心筋症、腎疾患、反復感染で寿命2-4歳に短縮。",
        "prevention": "STRICT NO-SUGAR DIET FROM ACQUISITION - cannot be overemphasized. Specifically: NO fruit (any), NO commercial 'treats,' NO sweet vegetables (carrots, sweet potato, beets except occasional small pieces), NO dairy, NO honey, NO molasses-containing pellets. APPROPRIATE diet: chinchilla pellets, unlimited timothy hay, leafy greens (romaine, dandelion, plantain weeds), small amounts of broccoli/kale, occasional rolled oats/sunflower seeds as treats only. Read all labels for hidden sugars. Owner education AT POINT OF PURCHASE - many cataract cases preventable with proper initial guidance. Annual veterinary exam with eye examination + blood glucose check >2 years old. Weigh annually (sudden weight loss may indicate diabetes). Single-degu cages or controlled feeding to prevent treat-sharing exposure.",
        "prevention_ja": "取得時からの厳格無糖食 — 強調しすぎることはない。具体的に：果物（任意）禁止、市販「おやつ」禁止、甘い野菜（ニンジン、サツマイモ、ビートは時折小片以外禁止）禁止、乳製品禁止、蜂蜜禁止、糖蜜含むペレット禁止。適切食事：チンチラペレット、無制限ティモシー乾草、葉物野菜（ロメイン、タンポポ、オオバコ雑草）、ブロッコリー/ケール少量、ロールドオート/ヒマワリ種を時折のおやつとしてのみ。全ラベルで隠れた糖を読む。購入時の飼い主教育 — 多くの白内障症例は適切な初期指導で予防可能。眼科検査＋>2歳での血糖チェック含む年次獣医検査。年次体重測定（急速体重減少は糖尿病示唆）。おやつ共有暴露防止のため単独デグーケージまたはコントロール給餌。",
        "recommended_tests": [
            "blood_glucose",
            "ophthalmologic_exam",
            "urinalysis_glucose",
            "fructosamine",
            "complete_blood_count",
            "serum_chemistry",
        ],
        "urgency": "urgent",
        "onset_pattern": {"chronic", "subacute"},
        "age_predisposition": {"young", "adult", "senior"},
    },
]


# ---------------------------------------------------------------------------
# Symptom name lookup
# ---------------------------------------------------------------------------

# Category mapping for symptom checkbox UI
SYMPTOM_CATEGORIES: Dict[str, str] = {
    # 皮膚・体表
    "bumping_into_objects": "skin",
    "hair_loss": "skin",
    "crusty_skin": "skin",
    "scaly_skin": "skin",
    "itching": "skin",
    "scratching": "skin",
    "circular_lesions": "skin",
    "patchy_fur": "skin",
    "skin_redness": "skin",
    "skin_mass": "skin",
    "ulceration": "skin",
    "tail_injury": "skin",
    "swollen_feet": "skin",
    "foot_sores": "skin",
    "rough_coat": "skin",
    "scratching_ear": "skin",
    "barbering": "skin",
    "bite_wounds": "skin",
    "bleeding_from_mass": "skin",
    "circular_hair_loss": "skin",
    "draining_tract": "skin",
    "exposed_tail_bone": "skin",
    "extensive_hair_loss": "skin",
    "foot_lesions": "skin",
    "foot_ulceration": "skin",
    "intense_itching": "skin",
    "poor_coat": "skin",
    "pruritus": "skin",
    "severe_foot_swelling": "skin",
    "skin_abrasion": "skin",
    "skin_crusting": "skin",
    "skin_lesions": "skin",
    "skin_masses": "skin",
    "skin_scaling": "skin",
    "skin_thickening": "skin",
    "slow_growing_lump": "skin",
    "slow_wound_healing": "skin",
    "subcutaneous_mass": "skin",
    "tail_necrosis": "skin",
    "visible_lice": "skin",
    "widespread_lesions": "skin",
    # 眼
    "cloudy_eyes": "eyes",
    "vision_loss": "eyes",
    "eye_discharge": "eyes",
    "eye_redness": "eyes",
    "eye_swelling": "eyes",
    "pawing_at_eye": "eyes",
    "sunken_eyes": "eyes",
    "conjunctivitis": "eyes",
    "corneal_opacity": "eyes",
    "dilated_pupils": "eyes",
    "enlarged_eye": "eyes",
    "epiphora": "eyes",
    "eye_pain": "eyes",
    # 耳
    "ear_discharge": "ears",
    # 呼吸器
    "sneezing": "respiratory",
    "nasal_discharge": "respiratory",
    "labored_breathing": "respiratory",
    "rapid_breathing": "respiratory",
    "coughing": "respiratory",
    "chronic_sneezing": "respiratory",
    "respiratory_distress": "respiratory",
    # 消化器・口腔
    "drooling": "digestive",
    "appetite_loss": "digestive",
    "teeth_grinding": "digestive",
    "visible_tooth_overgrowth": "digestive",
    "diarrhea": "digestive",
    "bloating": "digestive",
    "reduced_fecal_output": "digestive",
    "straining": "digestive",
    "vomiting": "digestive",
    "bloody_stool": "digestive",
    "tissue_protrusion_anus": "digestive",
    "dark_stool": "digestive",
    "difficulty_eating": "digestive",
    "excessive_hunger": "digestive",
    "gas": "digestive",
    "perianal_irritation": "digestive",
    "selective_eating": "digestive",
    "soft_jaw": "digestive",
    "soft_stool": "digestive",
    "tooth_discoloration": "digestive",
    "tooth_fracture": "digestive",
    "visible_proglottids": "digestive",
    # 骨格・四肢
    "exposed_bone": "musculoskeletal",
    "lameness": "musculoskeletal",
    "limb_deformity": "musculoskeletal",
    "stiffness": "musculoskeletal",
    "swollen_joints": "musculoskeletal",
    "bone_infection": "musculoskeletal",
    "bone_pain": "musculoskeletal",
    "crepitus": "musculoskeletal",
    "hind_limb_weakness": "musculoskeletal",
    "intermittent_lameness": "musculoskeletal",
    "limb_fracture": "musculoskeletal",
    "limb_stiffness": "musculoskeletal",
    "limb_swelling": "musculoskeletal",
    "non_weight_bearing": "musculoskeletal",
    "pathological_fracture": "musculoskeletal",
    # 神経
    "hind_leg_paralysis": "neurological",
    "dragging_legs": "neurological",
    "seizures": "neurological",
    "disorientation": "neurological",
    "head_tilt": "neurological",
    "circling": "neurological",
    "nystagmus": "neurological",
    "abnormal_gait": "neurological",
    "memory_loss": "neurological",
    "reduced_reflexes": "neurological",
    # 泌尿器・生殖器
    "polyuria": "urinary",
    "incontinence": "urinary",
    "blood_in_urine": "urinary",
    "frequent_urination": "urinary",
    "vaginal_discharge": "urinary",
    "mammary_mass": "urinary",
    "testicular_swelling": "urinary",
    "asymmetric_testes": "urinary",
    "mammary_redness": "urinary",
    "mammary_swelling": "urinary",
    "straining_to_urinate": "urinary",
    "vulvar_swelling": "urinary",
    # 循環器
    "cold_extremities": "cardiovascular",
    "cyanosis": "cardiovascular",
    "collapse": "cardiovascular",
    "exercise_intolerance": "cardiovascular",
    "muffled_heart_sounds": "cardiovascular",
    # 体型・全身
    "weight_loss": "body",
    "weight_gain": "body",
    "obesity": "body",
    "dehydration": "body",
    "facial_swelling": "body",
    "swelling": "body",
    "abdominal_distension": "body",
    "abdominal_pain": "body",
    "edema": "body",
    "failure_to_thrive": "body",
    "jaw_swelling": "body",
    "lymph_node_swelling": "body",
    "muscle_wasting": "body",
    "rapid_growth": "body",
    "splenomegaly": "body",
    "swelling_at_tail_stump": "body",
    "tail_abnormality": "body",
    # 行動・活動
    "lethargy": "behavior",
    "shivering": "behavior",
    "squinting": "behavior",
    "stress_behavior": "behavior",
    "reluctance_to_move": "behavior",
    "pain": "behavior",
    "reduced_activity": "behavior",
    "restlessness": "behavior",
    "loss_of_balance": "behavior",
    "aggression": "behavior",
    "back_pain": "behavior",
    "behavioral_changes": "behavior",
    "cold_intolerance": "behavior",
    "confusion": "behavior",
    "decreased_social_interaction": "behavior",
    "repetitive_behavior": "behavior",
    "sleep_pattern_changes": "behavior",
    "stereotypic_behavior": "behavior",
    "stress_signs": "behavior",
    "vocalization": "behavior",
    "weakness": "behavior",
    # 緊急
    "sudden_death": "emergency",
    # 内科・血液
    "polydipsia": "internal",
    "hyperglycemia": "internal",
    "fever": "internal",
    "bleeding_gums": "internal",
    "bleeding": "internal",
    "discharge": "internal",
    "jaundice": "internal",
    "anemia": "internal",
    "hypothermia": "internal",
}

SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    # Endocrine / Metabolic
    "polyuria": {"ja": "多尿", "en": "Polyuria"},
    "polydipsia": {"ja": "多飲", "en": "Polydipsia"},
    "hyperglycemia": {"ja": "高血糖", "en": "Hyperglycemia"},
    "weight_loss": {"ja": "体重減少", "en": "Weight Loss"},
    "weight_gain": {"ja": "体重増加", "en": "Weight Gain"},
    "obesity": {"ja": "肥満", "en": "Obesity"},
    "lethargy": {"ja": "無気力・元気消失", "en": "Lethargy"},
    "dehydration": {"ja": "脱水", "en": "Dehydration"},
    "fever": {"ja": "発熱", "en": "Fever"},
    "shivering": {"ja": "震え", "en": "Shivering"},
    "cold_extremities": {"ja": "四肢の冷感", "en": "Cold Extremities"},
    # Ophthalmological
    "cloudy_eyes": {"ja": "眼の白濁", "en": "Cloudy Eyes"},
    "vision_loss": {"ja": "視力低下", "en": "Vision Loss"},
    "bumping_into_objects": {"ja": "物にぶつかる", "en": "Bumping into Objects"},
    "eye_discharge": {"ja": "眼脂・目やに", "en": "Eye Discharge"},
    "eye_redness": {"ja": "眼の充血", "en": "Eye Redness"},
    "eye_swelling": {"ja": "眼の腫脹", "en": "Eye Swelling"},
    "squinting": {"ja": "眼を細める", "en": "Squinting"},
    "pawing_at_eye": {"ja": "眼を前足で掻く", "en": "Pawing at Eye"},
    "sunken_eyes": {"ja": "眼の陥没", "en": "Sunken Eyes"},
    # Dental
    "drooling": {"ja": "流涎・よだれ", "en": "Drooling"},
    "appetite_loss": {"ja": "食欲不振", "en": "Appetite Loss"},
    "teeth_grinding": {"ja": "歯ぎしり", "en": "Teeth Grinding"},
    "visible_tooth_overgrowth": {"ja": "歯の過長が目視できる", "en": "Visible Tooth Overgrowth"},
    "facial_swelling": {"ja": "顔面の腫脹", "en": "Facial Swelling"},
    "bleeding_gums": {"ja": "歯肉出血", "en": "Bleeding Gums"},
    # Dermatological
    "hair_loss": {"ja": "脱毛", "en": "Hair Loss"},
    "crusty_skin": {"ja": "痂皮形成", "en": "Crusty Skin"},
    "scaly_skin": {"ja": "鱗屑", "en": "Scaly Skin"},
    "itching": {"ja": "かゆみ", "en": "Itching"},
    "scratching": {"ja": "引っ掻き行動", "en": "Scratching"},
    "circular_lesions": {"ja": "円形の病変", "en": "Circular Lesions"},
    "patchy_fur": {"ja": "まだらな被毛", "en": "Patchy Fur"},
    "skin_redness": {"ja": "皮膚の発赤", "en": "Skin Redness"},
    "skin_mass": {"ja": "皮膚の腫瘤", "en": "Skin Mass"},
    "ulceration": {"ja": "潰瘍", "en": "Ulceration"},
    "stress_behavior": {"ja": "ストレス行動", "en": "Stress Behavior"},
    # Tail
    "tail_injury": {"ja": "尾部の損傷", "en": "Tail Injury"},
    "bleeding": {"ja": "出血", "en": "Bleeding"},
    "exposed_bone": {"ja": "骨の露出", "en": "Exposed Bone"},
    "foot_lesions": {"ja": "足部病変", "en": "Foot lesions"},
    # Musculoskeletal
    "swollen_feet": {"ja": "足の腫脹", "en": "Swollen Feet"},
    "foot_sores": {"ja": "足底の傷", "en": "Foot Sores"},
    "lameness": {"ja": "跛行", "en": "Lameness"},
    "limb_deformity": {"ja": "四肢の変形", "en": "Limb Deformity"},
    "reluctance_to_move": {"ja": "動きたがらない", "en": "Reluctance to Move"},
    "stiffness": {"ja": "硬直・こわばり", "en": "Stiffness"},
    "swollen_joints": {"ja": "関節の腫脹", "en": "Swollen Joints"},
    "hind_leg_paralysis": {"ja": "後肢麻痺", "en": "Hind Leg Paralysis"},
    "dragging_legs": {"ja": "後肢を引きずる", "en": "Dragging Hind Legs"},
    # Respiratory
    "sneezing": {"ja": "くしゃみ", "en": "Sneezing"},
    "nasal_discharge": {"ja": "鼻汁", "en": "Nasal Discharge"},
    "labored_breathing": {"ja": "努力性呼吸", "en": "Labored Breathing"},
    "rapid_breathing": {"ja": "頻呼吸", "en": "Rapid Breathing"},
    "coughing": {"ja": "咳", "en": "Coughing"},
    "cyanosis": {"ja": "チアノーゼ", "en": "Cyanosis"},
    # Gastrointestinal
    "diarrhea": {"ja": "下痢", "en": "Diarrhea"},
    "bloating": {"ja": "膨満", "en": "Bloating"},
    "reduced_fecal_output": {"ja": "排便量の減少", "en": "Reduced Fecal Output"},
    "straining": {"ja": "いきみ・排便困難", "en": "Straining"},
    "rough_coat": {"ja": "被毛の荒れ", "en": "Rough Coat"},
    "vomiting": {"ja": "嘔吐", "en": "Vomiting"},
    "bloody_stool": {"ja": "血便", "en": "Bloody Stool"},
    "tissue_protrusion_anus": {"ja": "肛門からの組織突出", "en": "Tissue Protrusion from Anus"},
    # General
    "pain": {"ja": "疼痛", "en": "Pain"},
    "swelling": {"ja": "腫脹", "en": "Swelling"},
    "discharge": {"ja": "分泌物・排膿", "en": "Discharge"},
    "collapse": {"ja": "虚脱", "en": "Collapse"},
    "reduced_activity": {"ja": "活動量の低下", "en": "Reduced Activity"},
    "restlessness": {"ja": "落ち着きのなさ", "en": "Restlessness"},
    "jaundice": {"ja": "黄疸", "en": "Jaundice"},
    "incontinence": {"ja": "失禁", "en": "Incontinence"},
    # Urinary
    "blood_in_urine": {"ja": "血尿", "en": "Blood in Urine"},
    "frequent_urination": {"ja": "頻尿", "en": "Frequent Urination"},
    # Reproductive
    "vaginal_discharge": {"ja": "膣分泌物", "en": "Vaginal Discharge"},
    "mammary_mass": {"ja": "乳腺の腫瘤", "en": "Mammary Mass"},
    "testicular_swelling": {"ja": "精巣の腫脹", "en": "Testicular Swelling"},
    "asymmetric_testes": {"ja": "精巣の左右差", "en": "Asymmetric Testes"},
    # Neurological
    "seizures": {"ja": "痙攣・発作", "en": "Seizures"},
    "disorientation": {"ja": "見当識障害", "en": "Disorientation"},
    "head_tilt": {"ja": "斜頸", "en": "Head Tilt"},
    "circling": {"ja": "旋回運動", "en": "Circling"},
    "loss_of_balance": {"ja": "平衡感覚の喪失", "en": "Loss of Balance"},
    "nystagmus": {"ja": "眼振", "en": "Nystagmus"},
    # Ear
    "scratching_ear": {"ja": "耳を掻く", "en": "Scratching Ear"},
    "ear_discharge": {"ja": "耳漏", "en": "Ear Discharge"},
    # --- 追加症状 (DISEASES内で使用されている未登録項目) ---
    "abdominal_distension": {"ja": "腹部膨満", "en": "Abdominal distension"},
    "abdominal_pain": {"ja": "腹痛", "en": "Abdominal pain"},
    "abnormal_gait": {"ja": "異常歩行", "en": "Abnormal gait"},
    "aggression": {"ja": "攻撃性", "en": "Aggression"},
    "anemia": {"ja": "貧血", "en": "Anemia"},
    "back_pain": {"ja": "背部痛", "en": "Back Pain"},
    "barbering": {"ja": "バーバリング（毛噛み）", "en": "Barbering"},
    "behavioral_changes": {"ja": "行動変化", "en": "Behavioral changes"},
    "bite_wounds": {"ja": "咬傷", "en": "Bite Wounds"},
    "bleeding_from_mass": {"ja": "腫瘤からの出血", "en": "Bleeding From Mass"},
    "bone_infection": {"ja": "骨感染", "en": "Bone Infection"},
    "bone_pain": {"ja": "骨痛", "en": "Bone Pain"},
    "chronic_sneezing": {"ja": "慢性くしゃみ", "en": "Chronic Sneezing"},
    "circular_hair_loss": {"ja": "円形脱毛", "en": "Circular Hair Loss"},
    "cold_intolerance": {"ja": "寒冷不耐", "en": "Cold Intolerance"},
    "confusion": {"ja": "混乱", "en": "Confusion"},
    "conjunctivitis": {"ja": "結膜炎", "en": "Conjunctivitis"},
    "corneal_opacity": {"ja": "角膜混濁", "en": "Corneal Opacity"},
    "crepitus": {"ja": "捻髪音", "en": "Crepitus"},
    "dark_stool": {"ja": "黒色便", "en": "Dark Stool"},
    "decreased_social_interaction": {"ja": "社会的交流の減少", "en": "Decreased Social Interaction"},
    "difficulty_eating": {"ja": "食事困難", "en": "Difficulty Eating"},
    "dilated_pupils": {"ja": "散瞳", "en": "Dilated Pupils"},
    "draining_tract": {"ja": "瘻管", "en": "Draining Tract"},
    "edema": {"ja": "浮腫", "en": "Edema"},
    "enlarged_eye": {"ja": "眼球肥大", "en": "Enlarged Eye"},
    "epiphora": {"ja": "流涙", "en": "Epiphora"},
    "excessive_hunger": {"ja": "過食", "en": "Excessive Hunger"},
    "exercise_intolerance": {"ja": "運動不耐性", "en": "Exercise Intolerance"},
    "exposed_tail_bone": {"ja": "尾骨露出", "en": "Exposed Tail Bone"},
    "extensive_hair_loss": {"ja": "広範囲の脱毛", "en": "Extensive Hair Loss"},
    "eye_pain": {"ja": "眼痛", "en": "Eye Pain"},
    "failure_to_thrive": {"ja": "発育不良", "en": "Failure To Thrive"},
    "foot_ulceration": {"ja": "足の潰瘍形成", "en": "Foot Ulceration"},
    "gas": {"ja": "鼓腸", "en": "Gas"},
    "hind_limb_weakness": {"ja": "後肢の衰弱", "en": "Hind limb weakness"},
    "hypothermia": {"ja": "低体温", "en": "Hypothermia"},
    "intense_itching": {"ja": "激しい掻痒", "en": "Intense Itching"},
    "intermittent_lameness": {"ja": "間欠性跛行", "en": "Intermittent Lameness"},
    "jaw_swelling": {"ja": "顎腫脹", "en": "Jaw Swelling"},
    "limb_fracture": {"ja": "四肢骨折", "en": "Limb Fracture"},
    "limb_stiffness": {"ja": "四肢硬直", "en": "Limb Stiffness"},
    "limb_swelling": {"ja": "四肢腫脹", "en": "Limb swelling"},
    "lymph_node_swelling": {"ja": "リンパ節腫脹", "en": "Lymph Node Swelling"},
    "mammary_redness": {"ja": "乳腺の発赤", "en": "Mammary Redness"},
    "mammary_swelling": {"ja": "乳腺の腫脹", "en": "Mammary Swelling"},
    "memory_loss": {"ja": "記憶喪失", "en": "Memory Loss"},
    "muffled_heart_sounds": {"ja": "心音減弱", "en": "Muffled Heart Sounds"},
    "muscle_wasting": {"ja": "筋萎縮", "en": "Muscle wasting"},
    "non_weight_bearing": {"ja": "患肢非負重", "en": "Non Weight Bearing"},
    "pathological_fracture": {"ja": "病的骨折", "en": "Pathological Fracture"},
    "perianal_irritation": {"ja": "肛門周囲の刺激", "en": "Perianal Irritation"},
    "poor_coat": {"ja": "被毛質の低下", "en": "Poor Coat"},
    "pruritus": {"ja": "掻痒", "en": "Pruritus"},
    "rapid_growth": {"ja": "急速増大", "en": "Rapid Growth"},
    "reduced_reflexes": {"ja": "反射低下", "en": "Reduced Reflexes"},
    "repetitive_behavior": {"ja": "反復行動", "en": "Repetitive Behavior"},
    "respiratory_distress": {"ja": "呼吸窮迫", "en": "Respiratory distress"},
    "selective_eating": {"ja": "えり好み", "en": "Selective Eating"},
    "severe_foot_swelling": {"ja": "重度の足腫脹", "en": "Severe Foot Swelling"},
    "skin_abrasion": {"ja": "皮膚擦過傷", "en": "Skin Abrasion"},
    "skin_crusting": {"ja": "皮膚の痂皮形成", "en": "Skin Crusting"},
    "skin_lesions": {"ja": "皮膚病変", "en": "Skin Lesions"},
    "skin_masses": {"ja": "皮膚腫瘤", "en": "Skin masses"},
    "skin_scaling": {"ja": "皮膚の落屑", "en": "Skin Scaling"},
    "skin_thickening": {"ja": "皮膚の肥厚", "en": "Skin Thickening"},
    "sleep_pattern_changes": {"ja": "睡眠パターンの変化", "en": "Sleep Pattern Changes"},
    "slow_growing_lump": {"ja": "緩徐に増大するしこり", "en": "Slow Growing Lump"},
    "slow_wound_healing": {"ja": "創傷治癒遅延", "en": "Slow Wound Healing"},
    "soft_jaw": {"ja": "軟化した顎骨", "en": "Soft Jaw"},
    "soft_stool": {"ja": "軟便", "en": "Soft Stool"},
    "splenomegaly": {"ja": "脾腫", "en": "Splenomegaly"},
    "stereotypic_behavior": {"ja": "常同行動", "en": "Stereotypic Behavior"},
    "straining_to_urinate": {"ja": "排尿困難", "en": "Straining to urinate"},
    "stress_signs": {"ja": "ストレス徴候", "en": "Stress Signs"},
    "subcutaneous_mass": {"ja": "皮下腫瘤", "en": "Subcutaneous Mass"},
    "sudden_death": {"ja": "突然死", "en": "Sudden death"},
    "swelling_at_tail_stump": {"ja": "尾の断端の腫脹", "en": "Swelling At Tail Stump"},
    "tail_abnormality": {"ja": "尾の異常", "en": "Tail abnormality"},
    "tail_necrosis": {"ja": "尾の壊死", "en": "Tail Necrosis"},
    "tooth_discoloration": {"ja": "歯の変色", "en": "Tooth Discoloration"},
    "tooth_fracture": {"ja": "歯の破折", "en": "Tooth Fracture"},
    "visible_lice": {"ja": "肉眼的なシラミ", "en": "Visible Lice"},
    "visible_proglottids": {"ja": "肉眼的な片節", "en": "Visible Proglottids"},
    "vocalization": {"ja": "鳴き声", "en": "Vocalization"},
    "vulvar_swelling": {"ja": "外陰部腫脹", "en": "Vulvar swelling"},
    "weakness": {"ja": "衰弱", "en": "Weakness"},
    "widespread_lesions": {"ja": "広範囲の病変", "en": "Widespread Lesions"},
}


# ---------------------------------------------------------------------------
# Public analysis function
# ---------------------------------------------------------------------------

# Enrich DISEASES with content from diseases_all_species.json
enrich_diseases(DISEASES, "Degu")


def analyze_symptoms(
    symptoms: List[str],
    age_stage: str = "",
    breed: str | None = None,
    *,
    onset: str | None = None,
    age_years: float | None = None,
    species: str | None = None,
    lab_values: dict | None = None,
    gender: str | None = None,
    vaccines=None,
    vaccination_status=None,
) -> Dict[str, Any]:
    """Run differential diagnosis for degus based on reported symptoms."""
    return analyze_symptoms_generic(
        symptoms,
        DISEASES,
        SYMPTOM_NAMES,
        ADVICE,
        onset=onset,
        age_years=age_years,
        breed=breed,
        species=species,
        lab_values=lab_values,
        gender=gender,
        vaccines=vaccines,
        vaccination_status=vaccination_status,
        prevalence_map=prevalence_data.SPECIES_PREVALENCE.get("degu", {}),
    )
