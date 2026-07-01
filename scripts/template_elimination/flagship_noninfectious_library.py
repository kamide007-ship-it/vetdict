"""Curated bilingual etiology / pathophysiology for high-traffic NON-infectious flagships.

The existing ``curated_etiology`` / ``curated_common_diseases`` supply excellent
Japanese causes/pathophysiology for ~120 flagship diseases, but they are
JA-only, so those records still show the English *category* template ("Cardiac
etiology…", "Endocrine or metabolic dysfunction…"). Many other high-traffic
non-infectious flagships (feline hyperthyroidism, PDA, saddle thrombus,
Legg-Calvé-Perthes, BOAS …) are not curated at all.

Non-infectious aetiology is not name-deterministic like the pathogen libraries,
so this module encodes established textbook knowledge for a curated set of
well-defined flagships, in BOTH languages. It plugs into the same
``fix_named_pathogens`` pipeline, which only overwrites recognised
category-template / stub fields — so it upgrades the templated English of an
already-JA-curated record without touching its curated Japanese.

References: Ettinger & Feldman, *Textbook of Veterinary Internal Medicine* 8th ed;
Nelson & Couto, *Small Animal Internal Medicine* 6th ed; ACVIM consensus
statements; Stashak, *Adams' Lameness in Horses* 6th ed.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    SPECIES_EN,
    SPECIES_JA,
    _neutralise_negations,
)


def _sp(sp: str) -> str:
    return SPECIES_JA.get(sp, sp)


def _spe(sp: str) -> str:
    return SPECIES_EN.get(sp, sp)


# Each generator returns (causes_ja, causes_en, patho_ja, patho_en).
def _feline_hyperthyroid(sp):
    return (
        "猫の甲状腺機能亢進症は、中高齢猫で最も多い内分泌疾患で、原因の大半は良性の甲状腺結節性過形成／腺腫（機能性）による甲状腺ホルモンの自律的過剰産生である。悪性の甲状腺癌は1〜3%と稀。環境・食餌要因（ゴイトロゲン、缶詰食）の関与も示唆される。",
        "Feline hyperthyroidism, the most common feline endocrinopathy of older cats, is caused in the great majority by benign nodular hyperplasia/adenoma of the thyroid autonomously oversecreting thyroid hormone; malignant thyroid carcinoma accounts for only 1-3%. Dietary/environmental factors (goitrogens, canned diets) are implicated.",
        "自律性に分泌された過剰な甲状腺ホルモンが全身の代謝を亢進させ、体重減少・多食・多飲多尿・活動性亢進・頻脈を生じる。慢性的な高代謝・高血圧により肥大型心筋症様変化・全身性高血圧・腎血流変化（隠れたCKDの顕在化）を招く。",
        "Autonomously secreted excess thyroid hormone raises whole-body metabolic rate, causing weight loss despite polyphagia, PU/PD, hyperactivity and tachycardia; chronic hypermetabolism and hypertension drive HCM-like changes, systemic hypertension and altered renal perfusion (unmasking occult CKD).",
    )


def _feline_hyperaldosteronism(sp):
    return (
        "猫の原発性アルドステロン症（コーン症候群）は、副腎皮質の機能性腺腫または過形成によるアルドステロンの自律的過剰分泌による。中高齢猫でみられる。",
        "Feline primary hyperaldosteronism (Conn's syndrome) is caused by autonomous aldosterone oversecretion from a functional adrenocortical adenoma or hyperplasia, seen in older cats.",
        "過剰なアルドステロンが腎遠位尿細管でのNa再吸収とK・H排泄を促進し、低カリウム血症（頸部腹屈・脱力・筋症）と難治性の全身性高血圧（網膜剥離・失明）を起こす。",
        "Excess aldosterone drives renal distal Na retention and K/H excretion, producing hypokalaemia (cervical ventroflexion, weakness, myopathy) and refractory systemic hypertension (retinal detachment, blindness).",
    )


def _feline_acromegaly(sp):
    return (
        "猫の先端巨大症（成長ホルモン過剰症）は、下垂体前葉のソマトトロフ腺腫による成長ホルモン(GH)の過剰分泌による。中高齢の雄猫に多い。",
        "Feline acromegaly (hypersomatotropism) is caused by excess growth-hormone secretion from a pituitary somatotroph adenoma, most often in older male cats.",
        "過剰なGHは末梢でインスリン抵抗性を誘発してインスリン抵抗性糖尿病を起こし、IGF-1を介して結合組織・骨・臓器の過形成（下顎前突・臓器巨大化・肥大型心筋症・変形性関節症）を生じる。",
        "Excess GH induces peripheral insulin resistance causing insulin-resistant diabetes, and via IGF-1 drives overgrowth of connective tissue, bone and organs (prognathia, organomegaly, HCM, degenerative arthropathy).",
    )


def _saddle_thrombus(sp):
    return (
        "猫の大動脈血栓塞栓症（サドル血栓）は、基礎心疾患（多くは肥大型心筋症）による左心房拡大・血流うっ滞から生じた血栓が遠位大動脈分岐部に塞栓することによる。",
        "Feline aortic thromboembolism (saddle thrombus) is caused by a thrombus that forms in a dilated, stasis-prone left atrium (usually secondary to cardiomyopathy, chiefly HCM) and embolises to the distal aortic trifurcation.",
        "塞栓が後肢への血流とセロトニン等による側副血行を遮断し、急性の後肢麻痺・疼痛・無脈・冷感・肉球チアノーゼを起こす。再灌流時の高カリウム血症と基礎心不全が予後を左右する。",
        "The embolus and vasoactive mediators (serotonin) occlude hindlimb arterial and collateral flow, causing acute painful paraparesis with absent femoral pulses, cold limbs and cyanotic pads; reperfusion hyperkalaemia and the underlying heart failure govern the outcome.",
    )


def _systemic_hypertension(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の全身性高血圧は、多くが基礎疾患に続発する（続発性）。主な原因は慢性腎臓病、甲状腺機能亢進症（猫）、副腎皮質機能亢進症・褐色細胞腫・原発性アルドステロン症などの内分泌疾患である。",
        f"Systemic hypertension in {e} is most often secondary to an underlying disease — chronic kidney disease, hyperthyroidism (cats), and endocrine disorders (hyperadrenocorticism, phaeochromocytoma, primary hyperaldosteronism).",
        "持続的な血圧上昇が標的臓器（眼・腎・心・脳）の細動脈を傷害し、網膜出血・剥離による急性失明、腎障害の進行、左室肥大、高血圧性脳症を起こす。",
        "Sustained pressure injures the arterioles of target organs (eye, kidney, heart, brain), causing retinal haemorrhage/detachment with acute blindness, progressive renal injury, left-ventricular hypertrophy and hypertensive encephalopathy.",
    )


def _pda(sp):
    return (
        "犬の動脈管開存症（PDA）は、出生後に閉鎖すべき動脈管（胎子期に肺動脈と大動脈をつなぐ血管）が閉じ残る先天性心疾患である。遺伝的素因があり、雌・特定犬種に多い。",
        "Patent ductus arteriosus (PDA) in dogs is a congenital defect in which the ductus arteriosus (the fetal connection between pulmonary artery and aorta) fails to close after birth; it is heritable, over-represented in females and certain breeds.",
        "大動脈から肺動脈への左→右短絡により肺循環・左心の容量負荷が生じ、左心拡大・肺水腫・左心不全に進行する。長期・重度では肺高血圧により短絡が逆転（右→左、Eisenmenger）し予後不良となる。",
        "The left-to-right shunt from aorta to pulmonary artery volume-overloads the pulmonary circulation and left heart, progressing to left-atrial enlargement, pulmonary oedema and left-sided heart failure; severe chronic cases develop pulmonary hypertension with shunt reversal (right-to-left, Eisenmenger) and a grave prognosis.",
    )


def _subaortic_stenosis(sp):
    return (
        "犬の（大動脈弁）下狭窄症は、左室流出路に線維性の隆起・輪状狭窄を生じる先天性心疾患で、遺伝性素因があり大型犬種に多い。",
        "Subaortic stenosis in dogs is a congenital narrowing of the left-ventricular outflow tract by a fibrous ridge/ring; it is heritable and over-represented in large breeds.",
        "流出路狭窄に対する圧負荷で求心性の左室肥大が進み、心筋虚血・不整脈・失神・突然死のリスクを高める。狭窄後乱流はジェット病変・大動脈弁閉鎖不全・心内膜炎の素因となる。",
        "Pressure overload against the obstruction drives concentric left-ventricular hypertrophy, raising the risk of myocardial ischaemia, arrhythmia, syncope and sudden death; post-stenotic turbulence predisposes to jet lesions, aortic insufficiency and endocarditis.",
    )


def _pulmonic_stenosis(sp):
    return (
        "犬の肺動脈狭窄症は、右室流出路・肺動脈弁の先天性狭窄（多くは弁の形成異常・癒合）による。遺伝性素因があり短頭種等に多い。",
        "Pulmonic stenosis in dogs is a congenital narrowing of the right-ventricular outflow tract/pulmonic valve (usually valve dysplasia/fusion), heritable and common in brachycephalic breeds.",
        "右室の圧負荷により求心性右室肥大が進み、右心不全・不整脈・運動不耐・失神を生じる。重度例では突然死のリスクがある。冠動脈奇形（R2A）を伴う型は治療上の注意を要する。",
        "Right-ventricular pressure overload causes concentric hypertrophy with right-sided heart failure, arrhythmia, exercise intolerance and syncope; severe cases risk sudden death, and an aberrant coronary artery (type R2A) complicates intervention.",
    )


def _legg_calve_perthes(sp):
    return (
        "犬のレッグ・カルベ・ペルテス病は、大腿骨頭への血行が途絶えて生じる無菌性（虚血性）壊死である。若齢の小型・トイ犬種に好発し、遺伝的素因が示唆される。",
        "Legg-Calvé-Perthes disease in dogs is aseptic (ischaemic) necrosis of the femoral head due to interrupted blood supply, occurring in young small/toy breeds with a suspected heritable basis.",
        "骨端の虚血性壊死後、修復過程で骨頭が変形・崩壊して股関節の適合不全・二次性変形性関節症を起こし、進行性の跛行・疼痛・患肢の筋萎縮を生じる。",
        "Ischaemic necrosis of the epiphysis is followed by collapse and deformation of the femoral head during repair, producing hip incongruity and secondary osteoarthritis with progressive lameness, pain and muscle atrophy.",
    )


def _ocd(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の離断性骨軟骨症（OCD）は、成長期の軟骨内骨化の異常により関節軟骨が肥厚・壊死し、軟骨弁が剥離する疾患である。急速な成長・遺伝・過剰栄養（Ca/エネルギー過多）・外傷・運動が関与する。",
        f"Osteochondritis dissecans (OCD) in {e} arises from defective endochondral ossification during growth, thickening and necrosing articular cartilage so a cartilage flap separates; rapid growth, genetics, dietary excess (calcium/energy), trauma and exercise contribute.",
        "肥厚した軟骨の深層が栄養障害で壊死し、亀裂・軟骨弁（関節ネズミ）を形成する。露出した軟骨下骨と遊離片が滑膜炎・疼痛・跛行と二次性変形性関節症を起こす。",
        "The deep layer of thickened cartilage becomes necrotic from impaired nutrition, fissuring to form a flap/joint mouse; exposed subchondral bone and the free fragment cause synovitis, pain, lameness and secondary osteoarthritis.",
    )


def _panosteitis(sp):
    return (
        "犬の汎骨炎（パノステオティス）は、若齢の大型・超大型犬種にみられる自己限定性の長骨疾患で、原因は不明（遺伝・急速成長・高蛋白/高カロリー食・ストレスの関与が示唆される）。",
        "Panosteitis in dogs is a self-limiting long-bone disease of young large/giant breeds of unknown cause (genetics, rapid growth, high-protein/high-energy diet and stress are implicated).",
        "骨髄・骨内膜の脂肪髄が線維化・骨新生に置換され、髄腔内圧の上昇と骨膜・栄養孔の刺激により、複数の長骨を移動する（shifting leg lameness）急性の疼痛・跛行を生じる。",
        "Marrow fat is replaced by fibrous tissue and new bone, and the raised intramedullary pressure with periosteal/nutrient-foramen irritation produces acute pain and a characteristic shifting-leg lameness across several long bones.",
    )


def _hod(sp):
    return (
        "犬の肥大性骨異栄養症（HOD）は、若齢の大型・急速成長犬種にみられる代謝性骨疾患で、原因は不明（血管障害・ワクチン反応・栄養・感染との関連が議論される）。",
        "Hypertrophic osteodystrophy (HOD) in dogs is a metabolic bone disease of young, rapidly growing large breeds of unknown cause (vascular, post-vaccinal, nutritional and infectious associations are debated).",
        "長骨骨幹端の成長板近傍で化膿性でない炎症・壊死が生じて特徴的な二重骨端線像を呈し、強い骨幹端の腫脹・疼痛・発熱・跛食欲不振を起こす。全身性炎症を伴い再発しうる。",
        "Non-septic inflammation and necrosis in the metaphyses adjacent to the growth plate produce the characteristic 'double physis' sign with painful metaphyseal swelling, fever, lameness and anorexia; systemic inflammation and relapses occur.",
    )


def _wobbler(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}のウォブラー症候群（頸部脊椎症性脊髄症）は、頸部の椎骨・椎間板・靭帯の構造的異常による頸髄の圧迫による。大型犬（椎間板関連型）・ドーベルマン等、馬（頸椎奇形/不安定）でみられ、遺伝・急速成長・栄養が関与する。",
        f"Wobbler syndrome (cervical spondylomyelopathy) in {e} is caused by compression of the cervical spinal cord from structural abnormality of the cervical vertebrae, discs and ligaments — in large-breed dogs (disc-associated), Dobermanns, and horses (cervical malformation/instability); genetics, rapid growth and nutrition contribute.",
        "慢性の脊髄圧迫が白質の脱髄・軸索変性を起こし、後肢優位の対称性の運動失調・不全麻痺（ワブリング歩様）を進行性に生じる。動的圧迫では頸部の姿勢で症状が変動する。",
        "Chronic cord compression causes white-matter demyelination and axonal degeneration, producing progressive symmetric ataxia and paresis worse in the hindlimbs (a 'wobbling' gait); with dynamic compression, signs vary with neck posture.",
    )


def _boas(sp):
    return (
        "犬の短頭種気道症候群（BOAS）は、短頭種の選択的育種による頭蓋・軟部組織の解剖学的異常（外鼻孔狭窄・軟口蓋過長・喉頭小嚢外反・気管低形成）の複合による上気道閉塞である。",
        "Brachycephalic obstructive airway syndrome (BOAS) in dogs is upper-airway obstruction from the combined anatomical abnormalities of selectively bred brachycephaly — stenotic nares, elongated soft palate, everted laryngeal saccules and hypoplastic trachea.",
        "解剖学的狭窄による吸気抵抗の増大が慢性的な陰圧を生み、軟部組織の浮腫・二次的な喉頭虚脱を進行させる悪循環を形成する。運動・興奮・高温で呼吸困難・チアノーゼ・熱中症・失神を起こし、慢性の消化器症状も伴う。",
        "Anatomical narrowing raises inspiratory resistance and the chronic negative pressure oedematises soft tissue and drives secondary laryngeal collapse in a vicious cycle; exertion, excitement and heat precipitate dyspnoea, cyanosis, heatstroke and syncope, often with concurrent GI signs.",
    )


def _cds(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の認知機能不全症候群（CDS）は、加齢に伴う神経変性疾患で、ヒトのアルツハイマー病に類似したβアミロイド沈着・酸化ストレス・神経細胞脱落による。",
        f"Cognitive dysfunction syndrome (CDS) in {e} is an age-related neurodegenerative disease driven by beta-amyloid deposition, oxidative stress and neuronal loss, analogous to human Alzheimer's disease.",
        "脳内のβアミロイド斑蓄積・血流低下・酸化傷害により神経伝達が障害され、見当識障害・社会交流の変化・睡眠覚醒周期の乱れ・粗相・活動性変化（DISHAA）が進行性に現れる。",
        "Amyloid-plaque accumulation, reduced cerebral perfusion and oxidative injury impair neurotransmission, producing progressive disorientation, altered social interaction, disrupted sleep-wake cycles, house-soiling and activity change (the DISHAA signs).",
    )


def _gme(sp):
    return (
        "犬の肉芽腫性髄膜脳脊髄炎（GME）は、原因不明の免疫介在性・非感染性の中枢神経炎症で、若〜中年の小型犬種の雌に好発する。",
        "Granulomatous meningoencephalomyelitis (GME) in dogs is an idiopathic, immune-mediated, non-infectious inflammation of the CNS, over-represented in young-to-middle-aged small-breed females.",
        "T細胞を主体とする血管周囲性の肉芽腫性炎症巣が脳・脊髄・髄膜に多巣性〜局所性に形成され、病変部位に応じた発作・運動失調・脳神経障害・頸部痛など多彩で進行性の神経症状を起こす。",
        "Perivascular, predominantly T-cell granulomatous infiltrates form multifocally or focally in brain, spinal cord and meninges, causing diverse progressive signs (seizures, ataxia, cranial-nerve deficits, neck pain) according to lesion location.",
    )


def _sebaceous_adenitis(sp):
    return (
        "犬の脂腺炎は、皮脂腺に対する免疫介在性の破壊性炎症による原因不明の皮膚疾患で、遺伝的素因があり（スタンダードプードル・秋田等）中年で発症する。",
        "Sebaceous adenitis in dogs is an idiopathic skin disease of immune-mediated destructive inflammation targeting the sebaceous glands, with a heritable predisposition (Standard Poodle, Akita) and middle-age onset.",
        "皮脂腺が炎症により破壊・消失すると皮脂の欠乏で角化・被毛が異常となり、対称性の脱毛・銀白色の粘着性鱗屑・毛包円柱・二次性膿皮症を生じる。",
        "Inflammatory destruction and loss of sebaceous glands deprives the skin of sebum, disturbing keratinisation and the hair coat to cause symmetric alopecia, adherent silvery scale, follicular casts and secondary pyoderma.",
    )


def _pemphigus_foliaceus(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の落葉状天疱瘡は、表皮角化細胞の細胞間接着蛋白（デスモソーム）に対する自己抗体による自己免疫性水疱性皮膚疾患である。特発性が多く、薬剤・慢性皮膚疾患が誘因となることもある。",
        f"Pemphigus foliaceus in {e} is an autoimmune blistering skin disease caused by autoantibodies against the intercellular adhesion proteins (desmosomes) of epidermal keratinocytes; most cases are idiopathic, sometimes drug- or chronic-dermatosis-triggered.",
        "自己抗体が角化細胞間接着を破壊（棘融解）して表在性の膿疱を形成し、破れて痂皮・鱗屑・脱毛となる。顔面・耳介・肉球に好発し、左右対称性に進行する。",
        "Autoantibodies disrupt keratinocyte adhesion (acantholysis) forming superficial pustules that rupture into crusts, scale and alopecia, characteristically affecting the face, pinnae and footpads in a symmetric distribution.",
    )


def _alopecia_x(sp):
    return (
        "犬の脱毛症X（Alopecia X）は、毛周期の停止による非炎症性・非掻痒性の脱毛で、性ホルモン・副腎ステロイド合成経路の局所的異常が関与すると考えられる（原因は完全には解明されていない）。ポメラニアン等の有毛犬種に多い。",
        "Alopecia X in dogs is a non-inflammatory, non-pruritic alopecia from arrested hair-follicle cycling, thought to involve a local abnormality of sex-hormone/adrenal-steroid synthesis pathways (cause not fully defined), common in plush-coated breeds (Pomeranian).",
        "毛包が成長期に移行できず休止期で停止するため、二次毛から進行する左右対称性の体幹脱毛と色素沈着を生じるが、頭部・四肢は保たれる。全身状態は正常。",
        "Follicles fail to re-enter anagen and arrest in telogen, producing symmetric truncal alopecia (starting with secondary hairs) and hyperpigmentation while the head and limbs are spared, with an otherwise normal general condition.",
    )


def _eosinophilic_granuloma(sp):
    return (
        "猫の好酸球性肉芽腫群（EGC）は、単一疾患ではなく過敏反応を背景とした皮膚反応パターンで、ノミ・食物・環境アレルゲンに対するアレルギーが主な誘因となる（遺伝的素因もある）。",
        "Feline eosinophilic granuloma complex (EGC) is not a single disease but a cutaneous reaction pattern driven by hypersensitivity — flea, food and environmental allergy are the main triggers (with a genetic predisposition).",
        "アレルゲンに対する好酸球主体の炎症反応が皮膚・口腔粘膜に生じ、好酸球性潰瘍（無痛性潰瘍）・好酸球性プラーク・線状肉芽腫として現れる。掻破・自己損傷が病変を悪化させる。",
        "An eosinophil-driven inflammatory response to allergens develops in skin and oral mucosa, presenting as the eosinophilic (indolent) ulcer, eosinophilic plaque and linear granuloma; self-trauma worsens the lesions.",
    )


# ---------------------------------------------------------------------------
# Batch 2 — bilingual backfill for high-traffic flagships already curated in
# Japanese by curated_etiology (which is JA-only): these supply the still-missing
# ENGLISH causes/pathophysiology. Because the JSON already carries the curated
# Japanese (not a template), the pipeline overwrites only the templated English.
# ---------------------------------------------------------------------------
def _gdv(sp):
    return (
        "犬の胃拡張捻転症候群（GDV）は、胃内のガス貯留（拡張）に胃の軸捻転が加わって生じる急性疾患。大型・胸深の犬種、早食い・一度の大量給餌・食後運動・第一度近親のGDV歴が主なリスク因子。",
        "Gastric dilatation-volvulus (GDV) in dogs is an acute condition in which gas accumulation (dilatation) is compounded by rotation of the stomach on its axis; risk factors are large, deep-chested breeds, rapid eating, a single large daily meal, post-prandial exercise and a first-degree relative with GDV.",
        "胃の捻転が噴門・幽門を閉塞してガス・液体を貯留し、胃壁と門脈・後大静脈を圧迫する。静脈還流の低下で閉塞性ショック・胃壁虚血/壊死・不整脈・エンドトキシン血症・DICに進行する致死的病態。",
        "Rotation occludes the cardia and pylorus, trapping gas and fluid and compressing the gastric wall and the portal vein/caudal vena cava; the fall in venous return produces obstructive shock, gastric-wall ischaemia/necrosis, arrhythmia, endotoxaemia and DIC — a life-threatening cascade.",
    )


def _pancreatitis(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の膵炎は、膵酵素の膵内での早期活性化による膵臓の自己消化性炎症。誘因は高脂肪食・食事の不適切（犬）、胆管系疾患・炎症性腸疾患・胆管炎の併発（猫の三臓器炎）、肥満・高脂血症・特定薬剤・腹部外傷など。",
        f"Pancreatitis in {e} is auto-digestive inflammation of the pancreas from premature intrapancreatic activation of pancreatic enzymes; triggers include dietary indiscretion/high fat (dogs), concurrent biliary/inflammatory-bowel disease (feline triaditis), obesity, hyperlipidaemia, certain drugs and abdominal trauma.",
        "活性化されたトリプシン等の消化酵素が膵実質・周囲脂肪を消化して局所の壊死・炎症・浮腫を起こし、放出されたサイトカイン・酵素が全身に波及するとSIRS・多臓器障害・DICに進行する。",
        "Prematurely activated trypsin and other enzymes digest pancreatic parenchyma and peripancreatic fat causing local necrosis, inflammation and oedema; systemic release of cytokines and enzymes can progress to SIRS, multi-organ dysfunction and DIC.",
    )


def _hypothyroid_dog(sp):
    return (
        "犬の甲状腺機能低下症は90%以上が後天性原発性で、最多はリンパ球性甲状腺炎（自己免疫性、遺伝的素因あり）、次いで特発性甲状腺萎縮による甲状腺ホルモン産生の低下。",
        "Canine hypothyroidism is over 90% acquired primary disease, most often from lymphocytic thyroiditis (autoimmune, heritable) or idiopathic thyroid atrophy, reducing thyroid-hormone production.",
        "甲状腺ホルモンの欠乏が全身の基礎代謝を低下させ、無気力・体重増加・寒がり・左右対称性脱毛・皮膚の色素沈着/脂漏・徐脈・高コレステロール血症・神経筋徴候を生じる。",
        "Thyroid-hormone deficiency lowers basal metabolic rate throughout the body, causing lethargy, weight gain, cold intolerance, symmetric alopecia, skin hyperpigmentation/seborrhoea, bradycardia, hypercholesterolaemia and neuromuscular signs.",
    )


def _cushing_dog(sp):
    return (
        "犬の副腎皮質機能亢進症（クッシング症候群）は、大半（約85%）が下垂体腺腫によるACTH過剰分泌（下垂体依存性）、残りが副腎腫瘍による自律的コルチゾール分泌。医原性（長期ステロイド）もある。",
        "Canine hyperadrenocorticism (Cushing's syndrome) is most often (~85%) pituitary-dependent (ACTH-secreting pituitary adenoma), with the remainder from an autonomously cortisol-secreting adrenal tumour; an iatrogenic form (chronic steroids) also occurs.",
        "慢性的なコルチゾール過剰が蛋白異化・脂質再分布・免疫抑制・水利尿を引き起こし、多飲多尿・多食・腹部膨満（ポットベリー）・左右対称性脱毛・菲薄化した皮膚・易感染性・筋力低下を生じる。",
        "Chronic cortisol excess drives protein catabolism, fat redistribution, immunosuppression and water diuresis, producing PU/PD, polyphagia, a pot-bellied abdomen, symmetric alopecia, thin skin, susceptibility to infection and muscle weakness.",
    )


def _ckd(sp):
    return (
        f"{'犬' if sp == 'dog' else '猫'}の慢性腎臓病は、多くが特発性の慢性尿細管間質性腎炎で、加齢・遺伝（多発性嚢胞腎等）・慢性腎盂腎炎・糸球体腎炎・腎毒性物質・尿路閉塞後の変化などが背景となる不可逆的なネフロン喪失による。",
        f"Chronic kidney disease in {'dogs' if sp == 'dog' else 'cats'} results from irreversible nephron loss, most often idiopathic chronic tubulointerstitial nephritis, with age, inherited disease (e.g. PKD), chronic pyelonephritis, glomerulonephritis, nephrotoxins and post-obstructive change contributing.",
        "機能ネフロンの進行性喪失に対し残存ネフロンが過剰濾過で代償するが、やがて限界に達して尿濃縮力低下（多尿）・尿毒素蓄積・二次性上皮小体機能亢進症・高血圧・貧血（EPO低下）・代謝性アシドーシスを生じる。",
        "As functioning nephrons are progressively lost, surviving nephrons hyperfilter to compensate until they too fail, producing loss of concentrating ability (polyuria), uraemic-toxin retention, renal secondary hyperparathyroidism, hypertension, anaemia (low erythropoietin) and metabolic acidosis.",
    )


def _atopic_dermatitis_dog(sp):
    return (
        "犬のアトピー性皮膚炎は、遺伝的素因を背景に環境アレルゲン（ハウスダストマイト・花粉・カビ等）に対して生じるIgE介在性のアレルギー性・炎症性皮膚疾患。皮膚バリア機能の異常も関与する。",
        "Canine atopic dermatitis is a genetically predisposed, IgE-mediated allergic inflammatory skin disease directed against environmental allergens (house-dust mites, pollens, moulds), with impaired skin-barrier function also contributing.",
        "アレルゲンへの過敏反応と皮膚バリア破綻により、掻痒を主徴とする慢性炎症が顔・耳・肢端・腋窩・鼠径に生じ、掻破・二次性の細菌/マラセチア感染・苔癬化を繰り返す。",
        "Hypersensitivity to allergens and a defective skin barrier produce chronic, intensely pruritic inflammation of the face, ears, paws, axillae and groin, with self-trauma and recurrent secondary bacterial/Malassezia infection and lichenification.",
    )


def _osteoarthritis(sp):
    j = _sp(sp)
    return (
        f"{j}の変形性関節症は、関節軟骨の進行性変性・摩耗による慢性の退行性関節疾患。素因となる関節疾患（形成不全・靭帯損傷・OCD・外傷）に続発する二次性が多く、加齢・肥満・過負荷が進行を早める。",
        f"Osteoarthritis in {_spe(sp)} is a chronic degenerative joint disease from progressive degeneration and wear of articular cartilage; it is usually secondary to a predisposing joint disorder (dysplasia, ligament injury, OCD, trauma), with age, obesity and overload accelerating it.",
        "軟骨基質の分解が軟骨下骨の露出・硬化・骨棘形成・滑膜炎を招き、関節の疼痛・可動域制限・跛行・筋萎縮を進行性に生じる。炎症と機械的ストレスの悪循環で不可逆的に進む。",
        "Breakdown of the cartilage matrix leads to subchondral bone exposure and sclerosis, osteophyte formation and synovitis, causing progressive joint pain, reduced range of motion, lameness and muscle atrophy in a self-perpetuating cycle of inflammation and mechanical stress.",
    )


def _ivdd_dog(sp):
    return (
        "犬の椎間板ヘルニアは、椎間板の変性（軟骨異栄養性犬種ではHansen I型の急性髄核逸脱、非軟骨異栄養性ではHansen II型の慢性線維輪突出）により椎間板物質が脊柱管内へ逸脱し脊髄を圧迫する疾患。",
        "Intervertebral disc disease in dogs occurs when disc degeneration (Hansen type I acute nucleus pulposus extrusion in chondrodystrophic breeds; Hansen type II chronic annular protrusion in non-chondrodystrophic breeds) displaces disc material into the vertebral canal, compressing the spinal cord.",
        "逸脱した椎間板物質による脊髄の圧迫・挫傷が浮腫・虚血・炎症を起こし、疼痛から不全麻痺・完全麻痺・深部痛覚消失まで重症度に応じた神経症状を生じる。急性重度例では脊髄軟化のリスクがある。",
        "Cord compression and contusion by extruded disc material cause oedema, ischaemia and inflammation, producing signs graded from pain to paresis, paralysis and loss of deep pain; acute severe cases risk progressive myelomalacia.",
    )


def _epilepsy_dog(sp):
    return (
        "犬の特発性てんかんは、構造的脳病変や代謝異常を伴わない、反復する発作を特徴とする脳疾患で、遺伝的素因が強く関与する（多くの犬種で家族性）。1〜5歳での発症が典型的。",
        "Canine idiopathic epilepsy is a brain disorder of recurrent seizures without structural brain lesions or metabolic disturbance, with a strong genetic (familial in many breeds) basis, typically starting at 1-5 years of age.",
        "興奮性と抑制性の神経伝達バランスの破綻により大脳皮質ニューロンが過剰同期発火し、全般または焦点発作を生じる。発作の反復（キンドリング）は将来の発作閾値を低下させうる。",
        "An imbalance between excitatory and inhibitory neurotransmission causes excessive synchronous firing of cortical neurons, producing generalised or focal seizures; recurrent seizures (kindling) can lower the threshold for future seizures.",
    )


def _dcm_dog(sp):
    return (
        "犬の拡張型心筋症は、心筋収縮力の一次的低下と全心室拡張を特徴とする心筋疾患。ドーベルマン・大型犬種で遺伝性素因が強く、一部はタウリン/カルニチン欠乏・非伝統的（グレインフリー）食との関連が示唆される。",
        "Canine dilated cardiomyopathy is a myocardial disease of primary systolic dysfunction with dilation of all chambers; there is a strong heritable predisposition in Dobermanns and large breeds, and some cases are linked to taurine/carnitine deficiency or non-traditional (grain-free) diets.",
        "心筋収縮力の低下が心拍出量減少と代償性の心室拡張・容量負荷を招き、うっ血性心不全（肺水腫・腹水）へ進行する。心室拡張と心筋病変は致死的不整脈・突然死の基盤ともなる。",
        "Reduced myocardial contractility lowers cardiac output and drives compensatory ventricular dilation and volume overload, progressing to congestive heart failure (pulmonary oedema, ascites); the dilated, diseased myocardium also predisposes to fatal arrhythmia and sudden death.",
    )


def _mmvd_dog(sp):
    return (
        "犬の粘液腫様僧帽弁変性症は、小型犬（キャバリア等）に好発する加齢性・遺伝性の弁膜変性で、僧帽弁尖・腱索のムコ多糖沈着・肥厚により弁閉鎖不全（逆流）を生じる、犬で最も多い後天性心疾患。",
        "Canine myxomatous mitral valve disease is an age-related, heritable valve degeneration common in small breeds (e.g. Cavaliers) in which mucopolysaccharide deposition thickens the mitral leaflets and chordae, causing valvular insufficiency (regurgitation) — the most common acquired heart disease of dogs.",
        "僧帽弁逆流による左心房・左心室の慢性容量負荷が左房拡大・左室拡張を招き、代償の破綻とともにうっ血性心不全（肺水腫）へ進行する。左房圧上昇・左房破裂・肺高血圧を合併しうる。",
        "Mitral regurgitation chronically volume-overloads the left atrium and ventricle, causing left-atrial enlargement and ventricular dilation that, once compensation fails, progresses to congestive heart failure (pulmonary oedema), with possible left-atrial rupture and pulmonary hypertension.",
    )


def _diabetes(sp):
    if sp == "cat":
        return (
            "猫の糖尿病は大半がヒトの2型に類似し、肥満・身体不活動・加齢を背景としたインスリン抵抗性と膵β細胞の機能不全（アミロイド沈着による）による相対的インスリン欠乏で発症する。",
            "Feline diabetes mellitus most resembles human type 2, arising from insulin resistance (obesity, inactivity, age) combined with pancreatic beta-cell dysfunction (islet amyloid deposition) causing relative insulin deficiency.",
            "インスリンの作用不足で細胞がグルコースを取り込めず高血糖・糖尿・浸透圧利尿（多飲多尿）を生じ、末梢では糖利用ができず脂肪・蛋白異化が進んで体重減少・多食を起こす。持続高血糖はβ細胞毒性（糖毒性）を悪化させる。",
            "Insufficient insulin action prevents cellular glucose uptake, causing hyperglycaemia, glycosuria and osmotic diuresis (PU/PD); the periphery cannot use glucose so fat and protein catabolism cause weight loss despite polyphagia, and sustained hyperglycaemia worsens beta-cell glucotoxicity.",
        )
    return (
        "犬の糖尿病は大半がインスリン依存性で、免疫介在性または慢性膵炎による膵β細胞の破壊に起因する絶対的インスリン欠乏による。雌では発情黄体期のプロゲステロン/成長ホルモンによるインスリン抵抗性が誘因となる。",
        "Canine diabetes mellitus is mostly insulin-dependent, from absolute insulin deficiency due to immune-mediated or chronic-pancreatitis-related destruction of pancreatic beta cells; in bitches, dioestrus progesterone/growth-hormone-driven insulin resistance is a trigger.",
        "インスリンの絶対的欠乏で高血糖・糖尿・浸透圧利尿（多飲多尿）と、末梢での糖利用不能による脂肪・蛋白異化（多食下の体重減少）を生じる。未治療では白内障・ケトアシドーシスに進行する。",
        "Absolute insulin deficiency causes hyperglycaemia, glycosuria and osmotic diuresis (PU/PD) and, from failure of peripheral glucose use, fat and protein catabolism (weight loss despite polyphagia); untreated it progresses to cataracts and ketoacidosis.",
    )


def _ibd_cat(sp):
    return (
        "猫の炎症性腸疾患は、腸内細菌叢・食事抗原に対する異常な免疫応答を背景とした慢性の特発性腸管炎症で、遺伝・環境・粘膜免疫の相互作用が関与する（真の原因は多因子で完全には解明されていない）。",
        "Feline inflammatory bowel disease is chronic idiopathic intestinal inflammation driven by an aberrant immune response to the gut microbiota and dietary antigens, arising from an interplay of genetic, environmental and mucosal-immune factors (multifactorial, not fully defined).",
        "腸粘膜へのリンパ球・形質細胞等の慢性浸潤が粘膜構造と消化吸収・バリア機能を障害し、慢性の嘔吐・下痢・体重減少・食欲変化を生じる。低悪性度消化器型リンパ腫との連続性が議論される。",
        "Chronic infiltration of the intestinal mucosa by lymphocytes and plasma cells disrupts mucosal architecture, digestion/absorption and barrier function, causing chronic vomiting, diarrhoea, weight loss and appetite change; a continuum with low-grade alimentary lymphoma is debated.",
    )


def _hepatic_lipidosis_cat(sp):
    return (
        "猫の肝リピドーシス（脂肪肝）は、食欲不振・絶食による負のエネルギーバランスで末梢脂肪が急速に肝へ動員され、肝細胞での脂肪処理能を超えて中性脂肪が過剰蓄積することによる。肥満猫が食欲不振に陥った際に多い。",
        "Feline hepatic lipidosis occurs when anorexia/fasting creates a negative energy balance that rapidly mobilises peripheral fat to the liver, overwhelming hepatocyte fat handling so triglyceride accumulates excessively; it is common when an obese cat becomes anorexic.",
        "肝細胞内への過剰な中性脂肪蓄積が細胞を膨化させて胆汁うっ滞・肝機能障害を起こし、黄疸・進行性の肝不全に至る。適切な栄養（カロリー）供給がなければ致死的となる。",
        "Massive intrahepatocellular triglyceride accumulation swells the cells causing cholestasis and hepatic dysfunction with icterus and progressive liver failure; without adequate nutritional (caloric) support it is fatal.",
    )


def _feline_asthma(sp):
    return (
        "猫の喘息（アレルギー性気管支炎）は、吸入アレルゲンに対するI型過敏反応を背景とした下部気道の慢性好酸球性炎症による、可逆性の気管支収縮を特徴とする疾患。",
        "Feline asthma (allergic bronchitis) is a disease of reversible bronchoconstriction from chronic eosinophilic lower-airway inflammation driven by a type-I hypersensitivity response to inhaled allergens.",
        "アレルゲンへの過敏反応が気道平滑筋の攣縮・粘液過分泌・気道壁の浮腫と好酸球浸潤を起こし、可逆性の気道狭窄による発作性の呼気性呼吸困難・咳・喘鳴を生じる。慢性化で気道リモデリングを来す。",
        "Hypersensitivity to allergens causes airway smooth-muscle spasm, mucus hypersecretion, and airway-wall oedema with eosinophilic infiltration, producing reversible airflow obstruction with paroxysmal expiratory dyspnoea, cough and wheeze; chronicity leads to airway remodelling.",
    )


# ---------------------------------------------------------------------------
# Batch 3 — bilingual backfill for the remaining high-traffic dog/cat/horse
# flagships already curated in Japanese by curated_etiology. Broad substring
# keys deliberately cover anatomical/breed-specific name variants that share
# the same underlying aetiology (e.g. all lymphoma anatomic forms), mirroring
# how curated_etiology's own JA generators are already keyed.
# ---------------------------------------------------------------------------


# --- Shared across species (species_set=None) -------------------------------
def _glaucoma_biling(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の緑内障は眼房水の流出障害による眼圧上昇で、原発性（隅角形成異常・開放隅角；犬種/猫種による遺伝的素因）と、続発性（ぶどう膜炎・水晶体脱臼・眼内腫瘍・眼内出血・白内障過熟）に分類される。猫では慢性ぶどう膜炎による続発性が大半を占める。",
        f"Glaucoma in {e} is elevated intraocular pressure from impaired aqueous outflow, classified as primary (anomalous/open drainage angle, with breed-specific heritable predisposition) or secondary (uveitis, lens luxation, intraocular neoplasia, haemorrhage, hypermature cataract); in cats most cases are secondary to chronic uveitis.",
        "毛様体で産生される眼房水の隅角からの流出が障害されて眼圧が上昇する。持続的な高眼圧は網膜神経節細胞と視神経乳頭を進行性に障害し、不可逆的な視覚喪失をきたす。急性発症は眼痛・角膜浮腫・散瞳を呈する眼科緊急疾患であり、長期化すると眼球拡大（牛眼）に至る。",
        "Outflow of aqueous humour (produced by the ciliary body) through the drainage angle is impeded, raising intraocular pressure; sustained hypertension progressively damages retinal ganglion cells and the optic disc, causing irreversible vision loss. Acute onset is an ophthalmic emergency with ocular pain, corneal oedema and mydriasis, and chronicity leads to globe enlargement (buphthalmos).",
    )


def _kcs_biling(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の乾性角結膜炎（KCS）は涙液（水層）の産生低下による。最多は免疫介在性の涙腺・第三眼瞼腺の破壊で、犬種素因がある。その他、第三眼瞼腺（チェリーアイ）摘出後、神経原性、薬剤性、内分泌性（甲状腺機能低下症）、犬ジステンパー、先天性が原因となる。",
        f"Keratoconjunctivitis sicca (KCS, dry eye) in {e} results from deficient tear (aqueous) production, most often immune-mediated destruction of the lacrimal/third-eyelid glands with a breed predisposition; other causes include prior third-eyelid gland (cherry eye) excision, neurogenic disease, certain drugs, hypothyroidism, canine distemper and congenital lacrimal hypoplasia.",
        "涙液水層の不足により角結膜の湿潤・栄養・抗菌・洗浄機能が破綻する。角膜上皮の乾燥・微小外傷から慢性角結膜炎、血管新生・色素沈着・角化、粘液膿性眼脂、再発性角膜潰瘍を生じ、重症例では角膜穿孔に至る。",
        "The tear-film deficiency deprives the cornea and conjunctiva of moisture, nutrition, antimicrobial defence and cleansing; corneal epithelial drying and microtrauma lead to chronic keratoconjunctivitis, vascularisation, pigmentation, keratinisation, mucopurulent discharge and recurrent corneal ulceration, with corneal perforation in severe cases.",
    )


def _corneal_ulcer_biling(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の角膜潰瘍は、外傷（自傷・異物・睫毛異常）、感染（細菌・ヘルペスウイルス）、乾性角結膜炎、眼瞼異常（内反症・兎眼）、角膜知覚低下など角膜上皮バリアを破綻させる要因による。",
        f"Corneal ulceration in {e} follows a breach of the corneal epithelial barrier from trauma (self-trauma, foreign body, aberrant eyelashes), infection (bacterial, herpesvirus), keratoconjunctivitis sicca, eyelid conformation defects (entropion, lagophthalmos) or reduced corneal sensation.",
        "上皮欠損部に細菌・宿主由来の蛋白分解酵素（コラゲナーゼ）が作用すると間質の融解が急速に進行し（メルティング潰瘍）、深部化・穿孔のリスクが高まる。慢性の表在性潰瘍は治癒が遅延し（indolent ulcer）、慢性創縁の上皮化不全を伴う。",
        "Bacterial and host-derived proteolytic enzymes (collagenases) acting on the epithelial defect can rapidly liquefy stroma ('melting' ulcer), raising the risk of deepening and perforation; chronic superficial (indolent) ulcers instead show delayed healing from failure of epithelial adhesion at the wound edge.",
    )


# --- Dog ---------------------------------------------------------------------
def _hip_dysplasia_dog(sp):
    return (
        "犬の股関節形成不全は、大腿骨頭と寛骨臼の適合不全（関節弛緩）を特徴とする多因子性の遺伝性疾患で、大型犬種に好発する。急速な成長・過栄養・過度な運動が発症・重症化を助長する。",
        "Canine hip dysplasia is a polygenic heritable disease of femoral head-acetabular incongruity (joint laxity), predominantly in large breeds; rapid growth, overnutrition and excessive exercise in puppyhood promote its onset and severity.",
        "関節弛緩により大腿骨頭が寛骨臼内で異常な負重・摩耗を受け、関節軟骨の変性と二次性変形性関節症が進行する。若齢では亜脱臼による疼痛性跛行を、成犬では慢性の変形性関節症による跛行・筋萎縮を呈する。",
        "Joint laxity subjects the femoral head to abnormal loading and wear within the acetabulum, driving cartilage degeneration and progressive secondary osteoarthritis; young dogs show painful lameness from subluxation, while adults develop chronic osteoarthritic lameness and muscle atrophy.",
    )


def _elbow_dysplasia_dog(sp):
    return (
        "犬の肘関節形成不全は、肘関節の複数の発生異常（内側鉤状突起の分離・内側鉤環状突起の解離・上腕骨内顆離断性骨軟骨症・関節不適合）の総称で、遺伝性素因が強く大型犬種に好発する。",
        "Canine elbow dysplasia is a collective term for several developmental abnormalities of the elbow (fragmented medial coronoid process, ununited anconeal process, osteochondritis dissecans of the medial humeral condyle, joint incongruity), strongly heritable and common in large breeds.",
        "関節面の不適合が局所的な異常負重を生じさせ、軟骨損傷・骨片形成・滑膜炎を招いて進行性の変形性関節症に至る。前肢跛行、特に運動後や起立後に増悪する跛行を特徴とする。",
        "Joint incongruity creates focal abnormal loading that damages cartilage, generates bone fragments and provokes synovitis, progressing to osteoarthritis; the hallmark is forelimb lameness, typically worse after exercise or rising.",
    )


def _cruciate_dog(sp):
    return (
        "犬の前十字靭帯断裂（部分/完全）は、多くが変性性（加齢・肥満・内分泌・免疫介在性・遺伝的な靭帯脆弱化を背景とした進行性変性）により生じ、軽微な外力で断裂する。若齢の急性外傷性断裂は少数派。",
        "Cranial cruciate ligament rupture (partial or complete) in dogs is usually degenerative — progressive ligament weakening from age, obesity, endocrine, immune-mediated and genetic factors — such that rupture follows only minor trauma; acute traumatic rupture in young dogs is the minority.",
        "靭帯の脆弱化が脛骨の前方引き出し（tibial thrust）に対する制御を失わせ、大腿骨に対する脛骨の異常な前方movement・回旋不安定性を生じる。関節不安定性は半月板損傷・滑膜炎を誘発し、急速に二次性変形性関節症へ進行する。",
        "Weakening of the ligament removes restraint against cranial tibial thrust, producing abnormal cranial translation and rotational instability of the tibia relative to the femur; the resulting instability predisposes to meniscal injury and synovitis and progresses rapidly to secondary osteoarthritis.",
    )


def _cataracts_dog(sp):
    return (
        "犬の白内障は水晶体蛋白の変性による混濁で、遺伝性（若齢発症、多犬種で報告）が最多。糖尿病性（ソルビトール経路による急速進行）、加齢性、外傷性、ぶどう膜炎続発性、先天性も原因となる。",
        "Canine cataracts are opacification from lens-protein degeneration, most often heritable (early-onset, reported in many breeds); diabetic cataracts (rapid progression via the sorbitol pathway), age-related, traumatic, uveitis-secondary and congenital forms also occur.",
        "水晶体線維蛋白の変性・凝集が透明性を喪失させ視覚障害を生じる。膨化した水晶体皮質は水晶体誘発性ぶどう膜炎を惹起しやすく、過熟白内障では水晶体嚢の脆弱化により水晶体脱臼・緑内障のリスクが高まる。",
        "Degeneration and aggregation of lens fibre proteins cause loss of transparency and visual impairment; a swelling cortex readily provokes lens-induced uveitis, and in hypermature cataracts capsular fragility raises the risk of lens luxation and secondary glaucoma.",
    )


def _pra_dog(sp):
    return (
        "犬の進行性網膜萎縮症（PRA）は、光受容体（桿体・錐体）の遺伝性変性疾患群の総称で、原因遺伝子・遺伝形式は犬種により異なる（多くは常染色体劣性）。",
        "Progressive retinal atrophy (PRA) in dogs is a group of inherited photoreceptor (rod and cone) degenerations, with the causative gene and mode of inheritance varying by breed (most commonly autosomal recessive).",
        "遺伝子変異により光受容体の代謝・構造が障害され、まず桿体（夜間視力）が変性して夜盲を生じ、後に錐体変性が進んで昼間視力も失われ、最終的に両側性の不可逆的失明に至る。二次性白内障を合併することが多い。",
        "The mutation disrupts photoreceptor metabolism/structure; rods (night vision) degenerate first causing nyctalopia, followed by cone degeneration and loss of day vision, progressing to irreversible bilateral blindness — often complicated by secondary cataract formation.",
    )


def _cherry_eye_dog(sp):
    return (
        "犬のチェリーアイ（第三眼瞼腺脱出）は、第三眼瞼腺を眼窩内に固定する結合組織の脆弱性・断裂による腺の逸脱で、若齢の特定犬種（ビーグル・ブルドッグ・コッカー・スパニエル等）に好発する遺伝性素因が示唆される疾患。",
        "Cherry eye (prolapse of the third-eyelid gland) in dogs results from weakness or rupture of the connective tissue anchoring the gland within the orbit, occurring in young dogs of predisposed breeds (Beagle, Bulldog, Cocker Spaniel) with a suspected heritable basis.",
        "支持組織の破綻により腺が眼瞼縁を越えて逸脱し、露出した腺組織が乾燥・摩擦・二次感染により腫脹・充血する。逸脱腺は涙液（水層）産生の大部分を担うため、摘出（整復ではなく）は将来の乾性角結膜炎リスクを高める。",
        "Failure of the supporting tissue lets the gland prolapse beyond the lid margin; the exposed tissue becomes swollen and congested from drying, friction and secondary infection. Because the gland provides most aqueous tear production, excision (rather than surgical repositioning) raises the future risk of dry eye.",
    )


def _pyoderma_dog(sp):
    return (
        "犬の膿皮症は、常在/日和見のブドウ球菌（主にStaphylococcus pseudintermedius）による皮膚の細菌感染で、多くはアレルギー性皮膚炎・内分泌疾患・寄生虫症・皮膚バリア異常など基礎疾患に続発する。",
        "Canine pyoderma is bacterial skin infection by commensal/opportunistic staphylococci (chiefly Staphylococcus pseudintermedius), usually secondary to an underlying disease — allergic dermatitis, endocrinopathy, ectoparasitism or a defective skin barrier.",
        "基礎疾患による皮膚バリア破綻・掻痒・免疫調節異常を背景に、細菌が毛包内または表皮内で増殖して膿疱・表皮小環・丘疹を形成する。掻破により病変が拡大し、再発を繰り返す場合は基礎疾患の特定と管理が不可欠。",
        "Against a background of barrier disruption, pruritus and immune dysregulation from the underlying disease, bacteria proliferate within follicles or the epidermis forming pustules, epidermal collarettes and papules; self-trauma extends the lesions, and recurrent disease demands identification and control of the primary cause.",
    )


def _addison_dog(sp):
    return (
        "犬のアジソン病（副腎皮質機能低下症）は、大半が免疫介在性の副腎皮質破壊による糖質・電解質コルチコイドの欠乏。医原性（急なステロイド中止）や下垂体性ACTH欠乏による続発性も稀にある。",
        "Canine Addison's disease (hypoadrenocorticism) is most often immune-mediated destruction of the adrenal cortex causing glucocorticoid and mineralocorticoid deficiency; iatrogenic (abrupt steroid withdrawal) and rare secondary (pituitary ACTH deficiency) forms also occur.",
        "アルドステロン欠乏がNa喪失・K貯留（高カリウム血症による致死的不整脈のリスク）と循環血液量減少を、コルチゾール欠乏がストレス耐性低下・低血糖・消化器症状を招く。急性発症（副腎クリーゼ）は低血圧性ショックを呈する内科緊急疾患。",
        "Aldosterone deficiency causes sodium loss and potassium retention (risking fatal hyperkalaemic arrhythmia) with hypovolaemia, while cortisol deficiency reduces stress tolerance and causes hypoglycaemia and GI signs; acute presentation (Addisonian crisis) is a medical emergency with hypotensive shock.",
    )


def _imha_dog(sp):
    return (
        "犬の免疫介在性溶血性貧血（IMHA）は、赤血球膜抗原に対する自己抗体産生による免疫介在性の赤血球破壊で、原発性（特発性）が最多。感染・腫瘍・薬剤・ワクチン接種を契機とする続発性もある。",
        "Canine immune-mediated haemolytic anaemia (IMHA) is immune-mediated red-cell destruction from autoantibodies against erythrocyte membrane antigens, most often primary (idiopathic); secondary forms follow infection, neoplasia, drugs or vaccination.",
        "自己抗体に感作された赤血球が脾臓のマクロファージに貪食される（血管外溶血）か、補体活性化により血管内で直接破壊される（血管内溶血）。急速な貧血・黄疸・血色素尿を生じ、しばしば二次性の血栓塞栓症（肺血栓塞栓症）を合併して致死的となる。",
        "Antibody-coated red cells are phagocytosed by splenic macrophages (extravascular haemolysis) or directly lysed intravascularly by complement activation; the result is rapid anaemia, icterus and haemoglobinuria, often complicated by fatal secondary thromboembolism (pulmonary).",
    )


def _hemangiosarcoma_dog(sp):
    return (
        "犬の血管肉腫は、血管内皮由来の高悪性度腫瘍で、脾臓・心臓（右心耳）・肝臓・皮下に好発する。品種素因（大型犬）があり、紫外線曝露が皮膚型のリスク因子となる。",
        "Canine haemangiosarcoma is a highly malignant tumour of vascular endothelial origin, most often arising in the spleen, heart (right auricle), liver and subcutis; large breeds are predisposed, and UV exposure is a risk factor for the dermal form.",
        "腫瘍血管は構造的に脆弱で自然破裂しやすく、腹腔内・心嚢内への大量出血による急性の虚脱・貧血性ショックを繰り返す（脾臓型・心臓型）。転移能が極めて高く、診断時には肺・肝・大網等への微小転移が既に成立していることが多い。",
        "Tumour vessels are structurally fragile and rupture spontaneously, causing recurrent massive intra-abdominal or pericardial haemorrhage with acute collapse and haemorrhagic shock (splenic and cardiac forms); metastatic potential is extremely high, and micrometastasis to lung, liver and omentum is usually already established at diagnosis.",
    )


def _osteosarcoma_dog(sp):
    return (
        "犬の骨肉腫は、大型・超大型犬種の四肢長骨（橈骨遠位端・上腕骨近位端・脛骨・大腿骨）に好発する原発性骨腫瘍で、成長板近傍の骨代謝が活発な部位に多い。品種特異的な遺伝的素因が強く関与する。",
        "Canine osteosarcoma is a primary bone tumour of large/giant breeds, arising chiefly in appendicular long bones (distal radius, proximal humerus, tibia, femur) near metabolically active growth-plate regions, with a strong breed-specific genetic predisposition.",
        "腫瘍細胞が皮質骨を破壊しながら急速に増殖し、著明な骨溶解と骨膜反応（Codman三角・sunburst像）を伴う病的骨折リスクの高い病変を形成する。診断時に90%以上で微小肺転移が既に成立しているとされる高悪性度腫瘍。",
        "Tumour cells proliferate rapidly while destroying cortical bone, producing marked osteolysis and periosteal reaction (Codman's triangle, sunburst pattern) with a high risk of pathological fracture; over 90% of dogs are thought to already have micrometastatic pulmonary disease at diagnosis.",
    )


def _mct_dog(sp):
    return (
        "犬の肥満細胞腫は、皮膚・皮下の肥満細胞由来腫瘍で、犬で最も多い皮膚悪性腫瘍。特定犬種（ボクサー・パグ・ラブラドール等）に好発し、c-KIT遺伝子変異が一部の腫瘍化に関与する。",
        "Canine mast cell tumour, a neoplasm of dermal/subcutaneous mast cells, is the most common malignant skin tumour of dogs; certain breeds (Boxer, Pug, Labrador) are predisposed, and c-KIT mutations drive a subset of tumours.",
        "腫瘍細胞の脱顆粒によりヒスタミン・ヘパリン・プロテアーゼが放出され、局所の腫脹・発赤・潰瘍化（Darier徴候）や、触診・切除操作による全身性のヒスタミン放出症候群（低血圧・胃十二指腸潰瘍・凝固障害）を引き起こしうる。悪性度により転移性が大きく異なる。",
        "Degranulation releases histamine, heparin and proteases, causing local swelling, erythema and ulceration (Darier's sign) and, with palpation or surgical manipulation, a systemic histamine-release syndrome (hypotension, gastroduodenal ulceration, coagulopathy); metastatic behaviour varies widely with tumour grade.",
    )


def _lymphoma_dog(sp):
    return (
        "犬のリンパ腫は、リンパ系組織由来の造血器腫瘍で、多中心型が最多。特定犬種での発生率上昇や環境要因（除草剤曝露等）の関与が示唆されるが、多くは原因不明。",
        "Canine lymphoma is a haematopoietic malignancy of lymphoid tissue, most often multicentric; certain breeds show increased incidence and environmental factors (e.g. herbicide exposure) are implicated, though most cases are of unknown cause.",
        "腫瘍性リンパ球がリンパ節・脾臓・肝臓・骨髄・節外部位（皮膚・消化管・鼻腔・中枢神経等）にクローン性に浸潤・増殖し、正常組織構築と機能を置換・破壊する。無治療での中央生存期間は数週間と短いが、化学療法への反応性は高い。",
        "Clonal neoplastic lymphocytes infiltrate and proliferate within lymph nodes, spleen, liver, bone marrow and extranodal sites (skin, gut, nasal cavity, CNS), replacing and destroying normal tissue architecture and function; median untreated survival is only weeks, but responsiveness to chemotherapy is high.",
    )


def _pss_dog(sp):
    return (
        "犬の門脈体循環シャント（肝シャント）は、門脈血が肝臓を迂回して全身循環に流入する血管異常。先天性（単一血管の異常、特定小型犬種に好発）と後天性（門脈圧亢進症に続発する多発性後天性シャント）に大別される。",
        "Canine portosystemic shunt (liver shunt) is an abnormal vessel through which portal blood bypasses the liver into systemic circulation; it is either congenital (a single anomalous vessel, common in certain small breeds) or acquired (multiple vessels secondary to portal hypertension).",
        "門脈血が肝実質を通らず全身循環に入るため、腸管由来の毒素（アンモニア等）が解毒されずに脳症を起こし（肝性脳症）、肝臓は栄養血流不足で萎縮・機能低下する。低蛋白血症・尿酸アンモニウム結石・発育不良を合併する。",
        "Because portal blood reaches systemic circulation without passing through hepatic parenchyma, gut-derived toxins (notably ammonia) go undetoxified and cause hepatic encephalopathy, while the liver atrophies and loses function from inadequate trophic portal flow; hypoproteinaemia, ammonium urate uroliths and stunted growth are common sequelae.",
    )


def _megaesophagus_dog(sp):
    return (
        "犬の巨大食道症は、食道の蠕動運動障害による拡張・機能不全で、先天性（特発性の神経筋未成熟、特定犬種に好発）と後天性（重症筋無力症・アジソン病・鉛中毒・食道閉塞後等に続発する特発性が最多）に分けられる。",
        "Canine megaesophagus is oesophageal dilation and dysmotility from failure of peristalsis; it is congenital (idiopathic neuromuscular immaturity, breed-predisposed) or acquired (most often idiopathic, otherwise secondary to myasthenia gravis, Addison's disease, lead toxicosis or prior oesophageal obstruction).",
        "食道の推進性蠕動が失われ、食物・液体が拡張した食道内に貯留する。貯留物の逆流・誤嚥により誤嚥性肺炎を高頻度に合併し、慢性的な栄養不良・削痩を招く致死率の高い疾患。",
        "Loss of propulsive peristalsis lets food and liquid pool in the dilated oesophagus; regurgitated material is frequently aspirated, causing a high rate of aspiration pneumonia and chronic malnutrition/wasting — a disease with a substantial mortality.",
    )


def _epi_dog(sp):
    return (
        "犬の膵外分泌不全（EPI）は、膵腺房細胞の消化酵素産生が90%以上失われることによる消化不良症候群。大半が膵腺房萎縮（若齢の特定犬種に好発、免疫介在性が疑われる）で、慢性膵炎の終末像として生じることもある。",
        "Canine exocrine pancreatic insufficiency (EPI) is a maldigestion syndrome from loss of over 90% of pancreatic acinar digestive-enzyme output, most often pancreatic acinar atrophy (young, breed-predisposed, suspected immune-mediated) or, less commonly, the end stage of chronic pancreatitis.",
        "消化酵素（リパーゼ・トリプシン・アミラーゼ）の欠乏により脂肪・蛋白・炭水化物の消化・吸収ができず、大量の未消化便・脂肪便・体重減少・多食を生じる。小腸内細菌の異常増殖やコバラミン欠乏を合併しやすい。",
        "Deficiency of digestive enzymes (lipase, trypsin, amylase) prevents digestion and absorption of fat, protein and carbohydrate, causing voluminous undigested/fatty stools, weight loss and polyphagia despite eating; small-intestinal bacterial overgrowth and cobalamin deficiency are common complications.",
    )


def _chronic_hepatitis_dog(sp):
    return (
        "犬の慢性肝炎は、持続する肝実質の炎症・壊死・線維化で、銅蓄積性（特定犬種の遺伝性銅代謝異常）、特発性、薬剤性、感染後（レプトスピラ・犬アデノウイルス1型後遺症）が主な原因。",
        "Canine chronic hepatitis is persistent hepatic inflammation, necrosis and fibrosis; copper-associated (heritable copper-metabolism defects in certain breeds), idiopathic, drug-induced and post-infectious (leptospirosis, canine adenovirus-1 sequela) forms predominate.",
        "持続する肝細胞傷害と炎症が線維化を進行させ、肝小葉構築の改築（架橋線維化・偽小葉形成）を経て肝硬変に至る。銅蓄積型では過剰な銅が酸化ストレスを介して肝細胞を直接傷害する。門脈圧亢進・腹水・肝性脳症へ進行しうる。",
        "Ongoing hepatocyte injury and inflammation drive progressive fibrosis, remodelling lobular architecture (bridging fibrosis, nodule formation) towards cirrhosis; in the copper-associated form, excess copper directly injures hepatocytes via oxidative stress. Progression to portal hypertension, ascites and hepatic encephalopathy can follow.",
    )


def _gb_mucocele_dog(sp):
    return (
        "犬の胆嚢粘液嚢腫は、胆嚢上皮の異常な粘液産生亢進により胆汁がゼリー状粘液に置換される疾患。内分泌疾患（副腎皮質機能亢進症・甲状腺機能低下症）、高脂血症、特定犬種の遺伝的素因が関与する。",
        "Canine gallbladder mucocele is abnormal hypersecretion of mucus by gallbladder epithelium that replaces bile with gelatinous mucus; endocrinopathy (hyperadrenocorticism, hypothyroidism), hyperlipidaemia and a breed-related genetic predisposition contribute.",
        "過剰な粘液が胆嚢内に蓄積して胆嚢を進行性に拡張させ、胆汁うっ滞・胆嚢壁の血流障害（虚血性壊死）を招く。壁の菲薄化・壊死が胆嚢破裂・胆汁性腹膜炎に至ると致死的な外科緊急疾患となる。",
        "Accumulating mucus progressively distends the gallbladder, causing bile stasis and compromised wall perfusion (ischaemic necrosis); thinning and necrosis of the wall can progress to gallbladder rupture and bile peritonitis — a life-threatening surgical emergency.",
    )


def _diabetes_insipidus(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の尿崩症は、抗利尿ホルモン（ADH/バソプレシン）の分泌不足（中枢性：下垂体・視床下部の腫瘍・外傷・特発性）または腎臓でのADH反応性低下（腎性：先天性または続発性）による尿濃縮障害。",
        f"Diabetes insipidus in {e} is a urine-concentrating defect from either deficient secretion of antidiuretic hormone (ADH/vasopressin) — central, from pituitary/hypothalamic tumour, trauma or idiopathic disease — or renal unresponsiveness to ADH (nephrogenic, congenital or acquired).",
        "腎集合管でのADH作用不足により水の再吸収が行われず、著明な低張多尿と代償性の多飲を生じる。飲水を制限されると急速に高張性脱水・高ナトリウム血症に陥る危険な病態。",
        "Insufficient ADH action at the renal collecting ducts prevents water reabsorption, producing marked hyposthenuric polyuria with compensatory polydipsia; if water access is restricted, rapid hypertonic dehydration and hypernatraemia result.",
    )


def _hypoparathyroidism_dog(sp):
    return (
        "犬の副甲状腺機能低下症は、大半が免疫介在性の上皮小体破壊によるパラトルモン（PTH）分泌不足。医原性（甲状腺摘出時の偶発的上皮小体切除）もある。",
        "Canine hypoparathyroidism is most often immune-mediated destruction of the parathyroid glands causing deficient parathyroid-hormone (PTH) secretion; an iatrogenic form follows inadvertent parathyroidectomy during thyroidectomy.",
        "PTH欠乏により骨からのCa動員と腎でのCa再吸収・リン排泄が低下し、重度の低カルシウム血症を生じる。神経筋興奮性の亢進により筋振戦・強直性痙攣・顔面掻痒・発作などの急性徴候を呈する内科緊急疾患。",
        "PTH deficiency impairs calcium mobilisation from bone and renal calcium reabsorption/phosphate excretion, causing severe hypocalcaemia; heightened neuromuscular excitability produces muscle tremors, tetany, facial rubbing and seizures — a medical emergency.",
    )


def _degenerative_myelopathy_dog(sp):
    return (
        "犬の変性性脊髄症は、SOD1遺伝子変異を主因とする脊髄白質の進行性変性疾患で、中高齢の大型犬種（特にジャーマン・シェパード等）に好発する遺伝性疾患。ヒトの家族性ALSに類似する。",
        "Canine degenerative myelopathy is a progressive spinal white-matter degeneration caused chiefly by SOD1 gene mutation, occurring in older large breeds (notably German Shepherds); it is heritable and analogous to human familial ALS.",
        "脊髄白質（特に胸腰髄の上行・下行伝導路）の軸索・髄鞘が進行性に変性し、非疼痛性・進行性の後肢の運動失調から不全麻痺、最終的に四肢麻痺・呼吸筋麻痺に至る。診断は他の脊髄疾患の除外による。",
        "Progressive axonal and myelin degeneration of spinal white matter (chiefly ascending/descending tracts of the thoracolumbar cord) causes non-painful, progressive hindlimb ataxia and paresis, eventually tetraplegia and respiratory muscle paralysis; diagnosis is by exclusion of other myelopathies.",
    )


def _laryngeal_paralysis_dog(sp):
    return (
        "犬の喉頭麻痺は、反回喉頭神経支配の披裂軟骨外転筋の機能不全による喉頭開大障害。大半は特発性（高齢大型犬種、末梢性の多発ニューロパチーの一部＝GOLPP）で、先天性（若齢特定犬種）・外傷性・腫瘍性もある。",
        "Canine laryngeal paralysis is failure of laryngeal abduction from dysfunction of the recurrent-laryngeal-nerve-innervated arytenoid abductor muscles; most cases are idiopathic (older large breeds, as part of a generalised peripheral polyneuropathy — GOLPP), with congenital (young, breed-specific), traumatic and neoplastic forms also occurring.",
        "披裂軟骨の外転不能により吸気時に声門が十分に開大できず、上気道抵抗が増大する。運動時・興奮時・高温時に喘鳴性の吸気性呼吸困難・チアノーゼ・虚脱を生じ、慢性の喉頭浮腫が悪循環的に閉塞を悪化させる。",
        "Failure of arytenoid abduction prevents adequate glottic opening on inspiration, raising upper-airway resistance; exertion, excitement and heat precipitate stridorous inspiratory dyspnoea, cyanosis and collapse, and chronic laryngeal oedema worsens the obstruction in a vicious cycle.",
    )


def _bph_dog(sp):
    return (
        "犬の良性前立腺肥大症（BPH）は、未去勢雄犬の加齢に伴うテストステロン/ジヒドロテストステロンとエストロゲンのバランス変化による前立腺腺組織の良性過形成。5歳以上の未去勢犬でほぼ必発とされる。",
        "Canine benign prostatic hyperplasia (BPH) is benign glandular hyperplasia of the prostate from age-related shifts in the testosterone/dihydrotestosterone-to-oestrogen balance in intact male dogs; it is near-universal in intact dogs over five years old.",
        "アンドロゲン依存性に腺房上皮・間質が過形成し、前立腺が対称性に腫大する。直腸圧迫による排便困難・テネスムス、尿道圧迫による排尿障害、被膜下出血による血様前立腺液・血尿を生じる。去勢により退縮する。",
        "Androgen-dependent hyperplasia of glandular epithelium and stroma symmetrically enlarges the prostate, causing tenesmus/constipation from rectal compression, dysuria from urethral compression, and haemorrhagic prostatic fluid/haematuria from subcapsular bleeding; it regresses after castration.",
    )


def _patellar_luxation_dog(sp):
    return (
        "犬の膝蓋骨脱臼（多くは内方）は、大腿四頭筋腱-膝蓋骨-膝蓋靭帯の伸筋機構の解剖学的アライメント異常（浅い滑車溝、脛骨粗面の内方偏位、大腿骨内反）による先天性/発育性疾患。小型犬種に好発するが大型犬種の外方脱臼も存在する。",
        "Canine patellar luxation (usually medial) is a congenital/developmental malalignment of the quadriceps-patella-patellar-ligament extensor mechanism (shallow trochlear groove, medially displaced tibial tuberosity, femoral varus), most common in small breeds, though lateral luxation occurs in large breeds.",
        "膝蓋骨が滑車溝から逸脱すると伸筋機構の力線が変化し、慢性的な異常摩耗により滑車溝の平坦化・軟骨損傷が進行する。間欠的な後肢挙上（skipping）から、重度例では慢性疼痛性跛行・二次性変形性関節症・前十字靭帯断裂の合併に至る。",
        "Once the patella escapes the trochlear groove, the line of pull of the extensor mechanism shifts, and chronic abnormal wear progressively flattens the groove and damages cartilage; signs range from intermittent hindlimb skipping to, in severe cases, chronic painful lameness with secondary osteoarthritis and concurrent cruciate ligament rupture.",
    )


def _praa_dog(sp):
    return (
        "犬の右大動脈弓遺残（PRAA）は、胎生期の大動脈弓形成過程で本来退縮すべき右第4大動脈弓が遺残し、左第4大動脈弓の代わりに大動脈弓を形成する先天性血管輪異常。",
        "Persistent right aortic arch (PRAA) in dogs is a congenital vascular ring anomaly in which the right fourth aortic arch, which should normally regress during fetal development, persists and forms the aortic arch in place of the left.",
        "遺残大動脈弓・動脈管索・肺動脈が食道を取り囲む血管輪を形成して食道を絞扼し、離乳食開始後の固形食通過障害による巨食道症・反復性の逆流/嘔吐（吐出）・誤嚥性肺炎を生じる。外科的な血管輪離断が根本治療となる。",
        "The persistent arch, ligamentum arteriosum and pulmonary artery form a vascular ring that constricts the oesophagus, causing megaoesophagus at the constriction with recurrent regurgitation of solid food (after weaning) and aspiration pneumonia; surgical division of the ring is the definitive treatment.",
    )


def _anal_sac_disease_dog(sp):
    return (
        "犬の肛門嚢疾患（貯留・嵌頓・炎症・膿瘍）は、肛門嚢分泌物の排出障害による貯留・粘稠化が発端となり、細菌の二次感染で炎症・膿瘍に進展する。肥満・軟便・アレルギー性皮膚炎が誘因となる。",
        "Canine anal sac disease (impaction, sacculitis, abscessation) begins with impaired emptying and thickening of anal sac secretion, which progresses to inflammation and abscessation with secondary bacterial infection; obesity, soft stool and allergic dermatitis are predisposing factors.",
        "貯留した分泌物が細菌増殖の培地となり、嚢壁の炎症（嚢炎）から化膿性膿瘍を形成する。疼痛による排便忌避・肛門周囲を舐める/擦る行動・「尻もち」歩行を呈し、膿瘍破裂で皮下～会陰部の瘻孔形成に至ることがある。",
        "Retained secretion becomes a medium for bacterial overgrowth, progressing from sacculitis to suppurative abscessation; dogs show pain-avoidant defecation, licking/scooting of the perianal area, and abscess rupture can create a draining perineal fistula.",
    )


def _ple_dog(sp):
    return (
        "犬の蛋白漏出性腸症（PLE）は単一疾患ではなく、腸粘膜からの過剰な血漿蛋白漏出を来す病態の総称で、リンパ管拡張症、重度の炎症性腸疾患、腸リンパ腫、真菌感染などが基礎疾患となる。特定犬種（ヨークシャー・テリア等）に遺伝性リンパ管拡張症の素因がある。",
        "Canine protein-losing enteropathy (PLE) is not a single disease but a syndrome of excessive plasma-protein loss across the intestinal mucosa, underlain by lymphangiectasia, severe inflammatory bowel disease, intestinal lymphoma or fungal infection; certain breeds (Yorkshire Terrier) have a heritable predisposition to lymphangiectasia.",
        "腸リンパ管の拡張・破綻や重度の粘膜炎症がアルブミン等の血漿蛋白の腸管腔への漏出を招き、低アルブミン血症による膠質浸透圧低下から腹水・胸水・皮下浮腫を生じる。しばしば低ガンマグロブリン血症・低カルシウム血症・凝固異常を合併する。",
        "Dilated/ruptured intestinal lymphatics or severe mucosal inflammation allow plasma proteins (albumin etc.) to leak into the gut lumen; the resulting hypoalbuminaemia lowers oncotic pressure, causing ascites, pleural effusion and subcutaneous oedema, often with concurrent hypogammaglobulinaemia, hypocalcaemia and coagulopathy.",
    )


def _esophagitis_dog(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の食道炎は、胃酸の逆流（麻酔中の胃食道逆流・慢性嘔吐）、異物・薬剤（ドキシサイクリン等の錠剤停滞）による直接刺激、感染、熱傷が主な原因。",
        f"Oesophagitis in {e} is chiefly caused by acid reflux (anaesthesia-associated gastro-oesophageal reflux, chronic vomiting), direct mucosal injury from foreign bodies or lodged medication (e.g. doxycycline tablets), infection, or thermal injury.",
        "酸・消化酵素や異物による粘膜傷害が炎症・びらん・潰瘍を起こし、疼痛による摂食拒否・嚥下障害・流涎を生じる。重度/慢性例では線維性瘢痕化による食道狭窄に進行しうる。",
        "Mucosal injury from acid, digestive enzymes or a foreign body causes inflammation, erosion and ulceration, producing pain-driven food refusal, dysphagia and ptyalism; severe or chronic cases can progress to fibrotic oesophageal stricture.",
    )


def _gerd_dog(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の胃食道逆流症（GERD）は、下部食道括約筋の弛緩不全/機能低下により胃内容物（酸・胆汁）が食道内に逆流する疾患。麻酔・鎮静、裂孔ヘルニア、慢性嘔吐性疾患が誘因となる。",
        f"Gastroesophageal reflux disease (GERD) in {e} occurs when a weak or inappropriately relaxing lower oesophageal sphincter allows gastric contents (acid, bile) to reflux into the oesophagus; anaesthesia/sedation, hiatal hernia and chronic vomiting disorders are precipitating factors.",
        "逆流した酸性内容物が食道粘膜を繰り返し傷害して食道炎を起こし、慢性化すると狭窄・バレット様化生のリスクが生じる。麻酔関連例では覚醒後の誤嚥性肺炎のリスクも重要。",
        "Repeated mucosal injury from refluxed acidic contents causes oesophagitis, with chronic cases risking stricture; in anaesthesia-associated reflux, aspiration pneumonia on recovery is an important additional risk.",
    )


def _cauda_equina_dog(sp):
    return (
        "犬の馬尾症候群（腰仙部狭窄症）は、腰仙関節の加齢性変性（椎間板変性・靭帯肥厚・関節突起症・脊椎すべり症）による馬尾（L7-仙骨神経根）の圧迫。大型犬種、特に使役犬種で運動性の腰仙部不安定性が関与する。",
        "Cauda equina syndrome (lumbosacral stenosis) in dogs is compression of the cauda equina (L7-sacral nerve roots) from age-related degeneration of the lumbosacral junction (disc degeneration, ligament hypertrophy, facet arthropathy, spondylolisthesis); large working breeds are predisposed, with dynamic lumbosacral instability contributing.",
        "神経根の慢性圧迫・虚血が疼痛・軸索障害を起こし、腰仙部痛・後肢跛行・尾の下垂/振れ低下・排尿排便障害（神経因性膀胱・便失禁）を生じる。伸展位で症状が悪化する動的圧迫のことが多い。",
        "Chronic compression and ischaemia of the nerve roots cause pain and axonal injury, producing lumbosacral pain, hindlimb lameness, reduced tail carriage/wag and urinary/faecal dysfunction (neurogenic bladder, incontinence); compression is often dynamic, worsening with lumbosacral extension.",
    )


def _facial_paralysis_dog(sp):
    return (
        "犬の顔面神経麻痺は、大半が特発性（末梢性顔面神経の変性、老齢犬・特定犬種に好発）で、中耳炎・外傷・腫瘍・多発ニューロパチーの一部としても生じる。",
        "Canine facial nerve paralysis is mostly idiopathic (peripheral facial nerve degeneration, occurring in older dogs and certain breeds), with otitis media, trauma, neoplasia and generalised polyneuropathy as other causes.",
        "顔面神経（表情筋）の運動機能喪失により患側の眼瞼閉鎖不全（兎眼・角膜潰瘍リスク）、耳介/口唇の下垂、流涎を生じる。特発性は非対称の突発性顔面下垂として気づかれることが多く、しばしば同時にKCSを合併する。",
        "Loss of facial-nerve motor function causes ipsilateral inability to close the eyelid (lagophthalmos, risking corneal ulceration), drooping of the ear/lip and drooling; the idiopathic form typically presents as sudden asymmetric facial droop and often coexists with KCS.",
    )


# --- Cat -----------------------------------------------------------------
def _hcm_cat(sp):
    return (
        "猫の肥大型心筋症（HCM）は猫で最も多い心疾患で、原発性は遺伝性（メインクーン・ラグドールでミオシン結合蛋白C遺伝子変異が同定）の心筋細胞肥大による左室壁肥厚。続発性は全身性高血圧・先端巨大症・甲状腺機能亢進症による心筋肥大（偽性HCM）。",
        "Feline hypertrophic cardiomyopathy (HCM), the most common feline heart disease, is primarily heritable (myosin-binding protein C mutations identified in Maine Coon and Ragdoll) myocyte hypertrophy causing left-ventricular wall thickening; secondary forms follow systemic hypertension, acromegaly or hyperthyroidism (pseudo-HCM).",
        "肥厚した心筋は拡張能が低下（拡張障害）し、左房圧上昇による肺水腫・胸水を来す。左房拡大は血流うっ滞を招いて左房内血栓を形成しやすく（サドル血栓の原因）、流出路閉塞を伴う型では収縮期雑音・失神リスクが加わる。",
        "The thickened myocardium has impaired relaxation (diastolic dysfunction), raising left-atrial pressure and causing pulmonary oedema/pleural effusion; left-atrial enlargement promotes stasis and thrombus formation (the cause of saddle thrombus), and the obstructive form adds a systolic murmur and syncope risk.",
    )


def _dcm_cat(sp):
    return (
        "猫の拡張型心筋症は、歴史的にはタウリン欠乏食が主因であったが（1987年以降のフード強化で激減）、現在は特発性または他の心筋疾患（HCMの拡張相）に続発する稀な疾患。",
        "Feline dilated cardiomyopathy was historically caused mainly by taurine-deficient diets (now rare since diet fortification from 1987); it is now an uncommon disease, either idiopathic or secondary to another cardiomyopathy (the dilated end-stage of HCM).",
        "心筋収縮蛋白の機能不全により収縮力が低下し、代償性の心室拡張と容量負荷が生じてうっ血性心不全（肺水腫・胸水）に進行する。タウリン欠乏例は補充により可逆的なことがある。",
        "Dysfunction of myocardial contractile proteins reduces systolic function, driving compensatory ventricular dilation and volume overload that progresses to congestive heart failure (pulmonary oedema, pleural effusion); taurine-deficiency cases can be reversible with supplementation.",
    )


def _rcm_cat(sp):
    return (
        "猫の拘束型心筋症は、心内膜下線維化により心室壁の伸展性が低下する心筋疾患で、原因は不明（心筋炎の既往との関連が示唆される）。",
        "Feline restrictive cardiomyopathy is a myocardial disease of endocardial fibrosis reducing ventricular wall compliance, of unknown cause (a link to prior myocarditis is suggested).",
        "線維化した心室壁が拡張期の充満を制限し（拡張障害）、正常な収縮機能にもかかわらず心房圧が著明に上昇して左房拡大・うっ血性心不全・血栓塞栓症を生じる。",
        "The fibrotic ventricular wall restricts diastolic filling (diastolic dysfunction); despite preserved systolic function, atrial pressure rises markedly, causing left-atrial enlargement, congestive heart failure and thromboembolism.",
    )


def _cholangitis_cat(sp):
    return (
        "猫の胆管炎・胆管肝炎は、好中球性型（上行性細菌感染、大腸菌が主体）とリンパ球性型（免疫介在性が疑われる慢性型）に大別される。猫は膵管・胆管・十二指腸への共通開口部の解剖学的特徴から、膵炎・炎症性腸疾患を合併しやすい（三臓器炎）。",
        "Feline cholangitis/cholangiohepatitis is broadly neutrophilic (ascending bacterial infection, chiefly E. coli) or lymphocytic (a chronic, suspected immune-mediated form); the feline anatomy — a shared opening of pancreatic and bile ducts into the duodenum — predisposes to concurrent pancreatitis and inflammatory bowel disease (triaditis).",
        "好中球性型は上行感染により胆管上皮に急性の化膿性炎症を起こし、未治療では膿瘍・敗血症に進展しうる。リンパ球性型は慢性のリンパ球浸潤と門脈域の線維化が進行し、胆汁うっ滞・肝硬変に至ることがある。",
        "The neutrophilic form causes acute suppurative inflammation of the biliary epithelium from ascending infection and, untreated, can progress to abscessation and sepsis; the lymphocytic form involves chronic lymphocytic infiltration and portal fibrosis that can progress to cholestasis and cirrhosis.",
    )


def _megacolon_cat(sp):
    return (
        "猫の巨大結腸症・便秘/宿便は、特発性の結腸平滑筋機能不全（大半）を筆頭に、骨盤骨折後の管腔狭窄、仙尾部神経損傷、脱水、疼痛による排便回避、Manx猫の脊髄奇形などが原因となる、便排出障害の連続的病態。",
        "Feline megacolon and constipation/obstipation form a continuum of defecatory dysfunction, most often idiopathic colonic smooth-muscle dysfunction, with pelvic-fracture luminal narrowing, sacrocaudal nerve injury, dehydration, pain-avoidant withholding and Manx spinal dysraphism as other causes.",
        "結腸平滑筋の収縮能低下により糞便の通過が遅延し、水分吸収が進んで便がさらに硬化する悪循環（便秘→巨大結腸）が生じる。慢性の結腸拡張は平滑筋の不可逆的な変性を招き、内科治療抵抗性の巨大結腸症に至る。",
        "Reduced colonic smooth-muscle contractility slows faecal transit, allowing further water absorption and hardening the stool in a self-perpetuating cycle (constipation leading to megacolon); chronic colonic distension causes irreversible smooth-muscle degeneration, producing medically refractory megacolon.",
    )


def _feline_urethral_obstruction(sp):
    return (
        "猫の尿道閉塞（ブロックドキャット）は、尿道栓子（結晶・粘液・細胞からなるプラグ）または尿路結石による物理的閉塞で、特発性膀胱炎（FIC）に伴う炎症・痙攣が誘因となる。去勢雄猫で尿道が細く長いため好発する。",
        "Feline urethral obstruction ('blocked cat') is physical obstruction by a urethral plug (crystals, mucus and cells) or a urolith, precipitated by the inflammation and spasm of feline idiopathic cystitis; castrated males are predisposed by their narrow, long urethra.",
        "閉塞により膀胱内圧が上昇して尿の排出が完全に途絶え、急性腎後性腎不全・高カリウム血症・代謝性アシドーシスが急速に進行する。高カリウム血症による致死的不整脈のリスクがある内科緊急疾患。",
        "Obstruction raises intravesical pressure and completely halts urine outflow, rapidly producing post-renal acute kidney injury, hyperkalaemia and metabolic acidosis; the resulting hyperkalaemia risks fatal arrhythmia, making this a medical emergency.",
    )


def _pkd_cat(sp):
    return (
        "猫の多発性嚢胞腎（PKD）は、PKD1遺伝子変異による常染色体優性遺伝性疾患で、ペルシャ・エキゾチックショートヘア等に好発する。出生時から嚢胞形成が始まる先天性疾患。",
        "Feline polycystic kidney disease (PKD) is an autosomal dominant disorder caused by a PKD1 gene mutation, common in Persian and Exotic Shorthair cats; cyst formation begins at birth (congenital).",
        "腎尿細管上皮の異常増殖により多数の嚢胞が形成・増大し、正常な腎実質を圧迫・置換して進行性に腎機能を低下させる。中高齢での慢性腎臓病としての発症が典型的で、稀に肝嚢胞を合併する。",
        "Aberrant proliferation of tubular epithelium forms numerous enlarging cysts that compress and replace normal renal parenchyma, progressively reducing renal function; disease typically presents as chronic kidney disease in middle-aged to older cats, occasionally with concurrent hepatic cysts.",
    )


def _conjunctivitis_cat(sp):
    return (
        "猫の結膜炎は、感染性（猫ヘルペスウイルス・クラミジア・マイコプラズマが主体）が最多だが、アレルギー性・異物性・好酸球性など非感染性の原因もある。",
        "Feline conjunctivitis is most often infectious (chiefly feline herpesvirus, Chlamydia felis, Mycoplasma), though allergic, foreign-body and eosinophilic non-infectious causes also occur.",
        "結膜上皮への直接感染または過敏反応が血管拡張・浮腫・滲出を伴う炎症を起こし、充血・眼脂・眼瞼腫脹・掻痒/違和感を生じる。原因により漿液性から粘液膿性まで眼脂の性状が異なる。",
        "Direct infection of the conjunctival epithelium, or a hypersensitivity reaction, causes vasodilation, oedema and exudation, producing hyperaemia, discharge, lid swelling and pruritus/discomfort; discharge character ranges from serous to mucopurulent depending on cause.",
    )


def _uveitis_cat(sp):
    return (
        "猫のぶどう膜炎は、原因不明の特発性が最多だが、感染性（猫伝染性腹膜炎・トキソプラズマ・眼内寄生虫）、腫瘍性（リンパ腫の眼内浸潤）、外傷性、水晶体誘発性など多岐にわたる。中高齢での新規発症時は全身性腫瘍・感染症のスクリーニングが重要。",
        "Feline uveitis is most often idiopathic, but infectious (FIP, toxoplasmosis, intraocular parasites), neoplastic (intraocular lymphoma infiltration), traumatic and lens-induced causes are also common; new-onset disease in an older cat warrants screening for systemic neoplasia and infection.",
        "血液房水柵の破綻により炎症細胞・蛋白が前房内に漏出し（フレア・cells）、虹彩の充血・毛様体痛・縮瞳・眼圧変化（低眼圧または続発緑内障）を生じる。慢性化すると虹彩後癒着・白内障・網膜剥離を合併しうる。",
        "Breakdown of the blood-aqueous barrier lets inflammatory cells and protein leak into the anterior chamber (flare and cells), causing iridal hyperaemia, ciliary pain, miosis and altered intraocular pressure (hypotony or secondary glaucoma); chronicity can bring posterior synechiae, cataract and retinal detachment.",
    )


def _eosinophilic_kcj_cat(sp):
    return (
        "猫の好酸球性角結膜炎は、猫ヘルペスウイルス感染や過敏反応を背景とした角結膜への好酸球主体の免疫介在性炎症。慢性・再発性の経過をとる。",
        "Feline eosinophilic keratoconjunctivitis is eosinophil-predominant, immune-mediated inflammation of the cornea and conjunctiva, arising against a background of feline herpesvirus infection and/or hypersensitivity, with a chronic, relapsing course.",
        "好酸球・肥満細胞が角膜実質・結膜に浸潤して白色〜ピンク色の隆起性プラークを形成し、血管新生・角膜混濁を伴う。掻痒・眼脂を生じ、放置すると視覚に影響する角膜病変に進行しうる。",
        "Eosinophils and mast cells infiltrate the cornea and conjunctiva forming raised white-to-pink plaques with vascularisation and corneal opacity; pruritus and discharge occur, and untreated lesions can progress to vision-affecting corneal disease.",
    )


def _corneal_sequestrum_cat(sp):
    return (
        "猫の角膜分離症（角膜壊死）は、慢性の角膜刺激・損傷（猫ヘルペスウイルス角膜炎、慢性乾性角結膜炎、眼瞼異常、短頭種の兎眼）を背景に角膜実質が壊死する猫特有の疾患。ペルシャ等の短頭種猫種に好発する。",
        "Feline corneal sequestrum (corneal necrosis) is a feline-specific condition of stromal necrosis arising from chronic corneal irritation/injury (feline herpetic keratitis, chronic KCS, eyelid conformation defects, brachycephalic lagophthalmos); brachycephalic breeds (Persian) are predisposed.",
        "慢性刺激による角膜実質の壊死組織にヘモグロビン由来色素が沈着し、特徴的な琥珀色〜黒色の角膜病変（分離体）を形成する。周囲に血管新生・疼痛・角膜穿孔のリスクを伴い、多くは外科的除去を要する。",
        "Chronically irritated stroma undergoes necrosis and accumulates haemoglobin-derived pigment, forming the characteristic amber-to-black corneal lesion (the sequestrum); it is surrounded by vascularisation, causes pain and risks perforation, usually requiring surgical removal.",
    )


def _fcgs_cat(sp):
    return (
        "猫の慢性歯肉口内炎（FCGS）は、口腔内の抗原（歯垢細菌・猫カリシウイルス等）に対する過剰な免疫応答による重度の口腔内炎症。基礎に猫カリシウイルス・FIV・FeLV感染や免疫調節異常が関与すると考えられる。",
        "Feline chronic gingivostomatitis (FCGS) is severe oral inflammation from an exaggerated immune response to oral antigens (dental plaque bacteria, feline calicivirus); underlying feline calicivirus, FIV/FeLV infection and immune dysregulation are implicated.",
        "口腔粘膜・歯肉・口蓋舌弓に著明なリンパ球形質細胞浸潤を伴う炎症が生じ、強い疼痛による摂食困難・流涎・体重減少を起こす。歯周組織の炎症コントロールが困難で、多くは全臼歯抜去が最も確実な治療となる。",
        "Marked lymphoplasmacytic infiltration develops in the oral mucosa, gingiva and glossopalatine arches, and the resulting severe pain causes difficulty eating, ptyalism and weight loss; periodontal inflammation is difficult to control, and full-mouth extraction is usually the most reliable treatment.",
    )


def _itp_cat(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の免疫介在性血小板減少症（ITP）は、血小板膜抗原に対する自己抗体産生による免疫介在性の血小板破壊で、原発性（特発性）が最多。感染・腫瘍・薬剤を契機とする続発性もある。",
        f"Immune-mediated thrombocytopenia (ITP) in {e} is immune-mediated platelet destruction from autoantibodies against platelet membrane antigens, most often primary (idiopathic); secondary forms follow infection, neoplasia or drugs.",
        "抗体に感作された血小板が脾臓のマクロファージに貪食・破壊され、著明な血小板減少により止血能が失われる。点状出血・斑状出血・粘膜出血を生じ、重度例では致死的な体腔内出血のリスクがある。",
        "Antibody-coated platelets are phagocytosed and destroyed by splenic macrophages, and the resulting marked thrombocytopenia impairs haemostasis; petechiae, ecchymoses and mucosal bleeding occur, with severe cases risking fatal internal haemorrhage.",
    )


def _trigeminal_neuritis_cat(sp):
    return (
        "猫の三叉神経炎は、原因不明の急性・特発性の三叉神経炎症で、多くは自然回復する一過性の疾患。",
        "Feline trigeminal neuritis is an acute, idiopathic inflammation of the trigeminal nerve of unknown cause, typically a self-limiting, transient condition.",
        "三叉神経の運動枝の炎症により咀嚼筋（側頭筋・咬筋）が麻痺し、急性の開口不能（下顎下垂）・摂食困難を生じるが、知覚は概ね保たれる。数週間で自然回復することが多い。",
        "Inflammation of the motor branch of the trigeminal nerve paralyses the muscles of mastication (temporalis, masseter), causing acute inability to close the jaw (dropped jaw) and difficulty eating, while sensory function is largely preserved; spontaneous recovery within a few weeks is typical.",
    )


def _myocarditis_cat(sp):
    j, e = _sp(sp), _spe(sp)
    return (
        f"{j}の心筋炎は、ウイルス感染・全身性感染症・免疫介在性機序・毒素/薬剤による心筋の炎症で、原因不明の特発性例も多い。",
        f"Myocarditis in {e} is inflammation of the myocardium from viral or systemic infection, immune-mediated mechanisms, or toxin/drug exposure, though many cases remain idiopathic.",
        "炎症性細胞浸潤が心筋細胞を直接傷害・壊死させ、収縮機能低下・不整脈を生じる。急性期は突然死のリスクがあり、遷延すると拡張型心筋症様の慢性心不全に移行しうる。",
        "Inflammatory cell infiltration directly injures and necroses myocytes, impairing contractility and provoking arrhythmia; the acute phase carries a risk of sudden death, and persistent disease can progress to dilated-cardiomyopathy-like chronic heart failure.",
    )


def _calcium_oxalate_urolith_cat(sp):
    return (
        "猫のシュウ酸カルシウム尿路結石症は、尿中のシュウ酸カルシウムの過飽和により結晶・結石が形成される疾患。酸性尿、高カルシウム尿、特定の食事・品種素因（ヒマラヤン等）が関与し、近年の酸性化フードの普及に伴い増加傾向。",
        "Feline calcium oxalate urolithiasis arises from urinary supersaturation with calcium oxalate forming crystals and stones; acidic urine, hypercalciuria, certain diets and breed predisposition (Himalayan) contribute, with an increasing incidence linked to widespread urine-acidifying diets.",
        "過飽和状態からシュウ酸カルシウム結晶が核形成・成長して結石化し、尿路粘膜を機械的に刺激・損傷して血尿・排尿障害を生じる。閉塞すれば急性腎後性腎不全を、溶解療法が無効なため外科的除去または食事管理による予防が中心となる。",
        "Supersaturation drives nucleation and growth of calcium oxalate crystals into stones that mechanically irritate and injure the urothelium, causing haematuria and dysuria; obstruction causes post-renal acute kidney injury, and because the stones cannot be dissolved medically, surgical removal or dietary prevention is central to management.",
    )


def _struvite_urolith_cat(sp):
    return (
        "猫のストルバイト（リン酸マグネシウムアンモニウム）尿路結石症は、アルカリ尿環境でのストルバイト過飽和により生じる。多くは無菌性（食事性のミネラル過剰・pH上昇が主因）で、犬と異なり尿路感染関連は少数。",
        "Feline struvite (magnesium ammonium phosphate) urolithiasis results from struvite supersaturation in alkaline urine; most cases are sterile (driven by dietary mineral excess and elevated urinary pH), unlike dogs where urinary tract infection is a common trigger.",
        "アルカリ尿中でストルバイトが結晶化・凝集して結石化する。溶解性の結石であるため、尿の酸性化と低マグネシウム/低リン食による食事療法で内科的溶解が可能な点がシュウ酸カルシウム結石と対照的。",
        "Struvite crystallises and aggregates into stones within alkaline urine; unlike calcium oxalate, struvite is dissolvable, so urinary acidification and a magnesium/phosphorus-restricted diet can achieve medical dissolution.",
    )


def _hyperparathyroidism_primary_cat(sp):
    return (
        "猫の原発性副甲状腺機能亢進症は、上皮小体の機能性腺腫（大半）または過形成・稀に癌によるパラトルモン（PTH）の自律的過剰分泌。中高齢猫にみられる。",
        "Feline primary hyperparathyroidism is autonomous parathyroid-hormone (PTH) oversecretion from a functional parathyroid adenoma (most cases), hyperplasia, or rarely carcinoma, occurring in older cats.",
        "自律的なPTH過剰が骨からのCa動員と腎でのCa再吸収を亢進させ、高カルシウム血症を生じる。慢性の高カルシウム血症は腎障害・尿路結石・多飲多尿・消化器症状・筋力低下を招く。",
        "Autonomous PTH excess increases calcium mobilisation from bone and renal calcium reabsorption, causing hypercalcaemia; chronic hypercalcaemia leads to renal injury, urolithiasis, PU/PD, GI signs and muscle weakness.",
    )


def _hyperparathyroidism_renal_cat(sp):
    return (
        "猫の腎性二次性副甲状腺機能亢進症は、慢性腎臓病による腎でのリン排泄低下・活性型ビタミンD産生低下が招く低カルシウム血症/高リン血症に反応した上皮小体の代償性過形成・PTH分泌亢進。",
        "Feline renal secondary hyperparathyroidism is compensatory parathyroid hyperplasia and increased PTH secretion in response to the hypocalcaemia/hyperphosphataemia caused by chronic kidney disease's reduced phosphate excretion and activated-vitamin-D synthesis.",
        "腎機能低下によるリン蓄積とビタミンD活性化障害が慢性的にPTH分泌を刺激し、線維性骨異栄養症（腎性骨異栄養症）や軟部組織の異所性石灰化を招く。CKDの進行とともに悪化する二次的な内分泌異常。",
        "Phosphate retention and impaired vitamin-D activation from declining renal function chronically stimulate PTH secretion, causing fibrous osteodystrophy (renal osteodystrophy) and ectopic soft-tissue mineralisation — a secondary endocrinopathy that worsens as CKD progresses.",
    )


# --- Horse -----------------------------------------------------------------
def _tendinitis_horse(sp):
    return (
        "馬の屈腱炎（浅指屈腱炎・深指屈腱損傷）は、運動時の反復・過剰な腱への機械的負荷による腱線維の微小損傷の蓄積（変性性）で生じる、競走馬に好発する腱の炎症・損傷。急激な高強度運動や不整地での運動が急性発症の契機となる。",
        "Tendinitis of the flexor tendons (superficial digital flexor, deep digital flexor) in horses arises from accumulated microdamage to tendon fibres under repetitive/excessive mechanical loading during exercise (a degenerative process), common in racehorses; sudden high-intensity work or uneven footing precipitates acute injury.",
        "腱線維の断裂・出血・炎症が腱の腫大（bowed tendon）を生じ、治癒過程で形成される瘢痕組織は正常腱に比べ弾性が劣るため再断裂のリスクが高い。治癒には長期間（6か月以上）を要し、パフォーマンスへの復帰率は損傷の重症度に依存する。",
        "Fibre rupture, haemorrhage and inflammation cause tendon enlargement ('bowed tendon'); the scar tissue formed during healing is less elastic than normal tendon, carrying a high risk of re-injury. Healing takes many months (6+), and return-to-performance rates depend on injury severity.",
    )


def _egus_horse(sp):
    return (
        "馬の胃潰瘍（EGUS）は、非腺部（扁平上皮）胃潰瘍と腺部胃潰瘍で機序が異なる。非腺部は保護機構を欠く扁平上皮への胃酸の長時間曝露（絶食時間の長さ・高濃縮飼料・激しい運動による酸の跳ね上げ）、腺部は粘液・重炭酸バリアの破綻（NSAIDs・ストレス）による。",
        "Equine gastric ulcer syndrome (EGUS) has distinct mechanisms for the two regions: squamous (non-glandular) ulcers follow prolonged acid exposure of unprotected squamous epithelium (long fasting intervals, concentrate-heavy diets, acid splashing during intense exercise), while glandular ulcers follow breakdown of the mucus-bicarbonate barrier (NSAIDs, stress).",
        "扁平上皮部では胃酸による直接的な化学的損傷が、腺部では防御機構破綻による自己消化が粘膜傷害を起こし、疼痛による摂食不良・パフォーマンス低下・疝痛・毛づやの悪化を生じる。断続的な絶食パターンが最大の危険因子。",
        "In the squamous region, direct chemical injury from acid damages the mucosa; in the glandular region, breakdown of protective mechanisms allows auto-digestion — both causing pain-related inappetence, reduced performance, colic and a poor coat. Intermittent fasting patterns are the greatest risk factor.",
    )


def _ems_horse(sp):
    return (
        "馬メタボリック症候群（EMS）は、肥満・インスリン抵抗性・蹄葉炎素因を三徴とする内分泌代謝疾患で、特定品種（ポニー種等）の遺伝的素因と、過剰な糖質・エネルギー摂取、運動不足が発症要因となる。",
        "Equine metabolic syndrome (EMS) is an endocrine-metabolic disorder characterised by the triad of obesity, insulin resistance and laminitis predisposition; a genetic predisposition in certain breeds (ponies) combines with excess carbohydrate/energy intake and inadequate exercise.",
        "内臓脂肪から分泌される炎症性アディポカインがインスリン抵抗性を助長し、代償性の高インスリン血症が持続する。高インスリン血症は蹄葉層の細胞増殖・接着異常を介して蹄葉炎を誘発する主要な機序である。",
        "Inflammatory adipokines secreted by visceral fat promote insulin resistance, driving sustained compensatory hyperinsulinaemia; hyperinsulinaemia is the principal mechanism triggering laminitis, via effects on lamellar epithelial cell proliferation and adhesion.",
    )


def _ppid_horse(sp):
    return (
        "馬の下垂体中葉機能障害（PPID、馬クッシング病）は、加齢に伴う視床下部ドパミン作動性神経の変性により下垂体中葉への抑制が失われ、中葉のメラノトロフ細胞が過形成・腺腫化してACTH関連ペプチドを過剰分泌する高齢馬の内分泌疾患。",
        "Pituitary pars intermedia dysfunction (PPID, equine Cushing's disease) in horses is an age-related endocrinopathy in which degeneration of hypothalamic dopaminergic neurons removes inhibitory control of the pituitary pars intermedia, causing melanotroph hyperplasia/adenoma formation and oversecretion of ACTH-related peptides.",
        "過剰なホルモン分泌が全身の代謝・免疫・皮膚に影響し、多毛症（治りにくい厚く縮れた被毛）・筋萎縮・多飲多尿・易感染性・慢性蹄葉炎を生じる。インスリン抵抗性を合併する例では蹄葉炎リスクがさらに高まる。",
        "Excess hormone secretion affects systemic metabolism, immunity and skin, causing hirsutism (a thick, curly coat that fails to shed), muscle wasting, PU/PD, susceptibility to infection and chronic laminitis; concurrent insulin resistance further raises laminitis risk.",
    )


def _rhabdomyolysis_horse(sp):
    return (
        "馬の運動誘発性横紋筋融解症（タイングアップ）は、散発性（過度な運動・電解質異常・ビタミンE/セレン欠乏）と、遺伝性の反復性型（RER：カルシウム調節異常、PSSM：糖原蓄積異常）に大別される骨格筋の急性壊死性疾患。",
        "Exertional rhabdomyolysis (tying-up) in horses is acute skeletal-muscle necrosis, either sporadic (excessive exercise, electrolyte imbalance, vitamin E/selenium deficiency) or a heritable recurrent form (RER: abnormal calcium regulation; PSSM: abnormal glycogen storage).",
        "筋細胞内Ca調節異常またはエネルギー代謝異常により筋線維が過収縮・壊死し、ミオグロビンが血中・尿中に大量放出される（ミオグロビン尿）。重度例ではミオグロビンによる腎尿細管閉塞から急性腎障害に進展しうる。",
        "Abnormal intracellular calcium regulation or energy metabolism causes muscle fibres to over-contract and undergo necrosis, releasing large amounts of myoglobin into blood and urine (myoglobinuria); severe cases can progress to acute kidney injury from myoglobin-induced tubular obstruction.",
    )


def _endometritis_horse(sp):
    return (
        "馬の子宮内膜炎は、交配・分娩後の一過性生理的炎症が遷延する持続性交配後子宮内膜炎（PMIE：子宮排出機能低下が背景）と、慢性感染性子宮内膜炎（子宮内リンパ管拡張・加齢による子宮防御機構低下）に大別される繁殖成績を左右する疾患。",
        "Equine endometritis is broadly persistent mating-induced endometritis (PMIE, from impaired uterine clearance of the normal post-breeding/foaling inflammatory response) or chronic infectious endometritis (uterine lymphatic lacunae, age-related decline in uterine defence) — a major determinant of fertility.",
        "子宮内の炎症性滲出物・病原体が胚の着床環境を障害し、早期胚死滅・不受胎を招く。慢性化した子宮内膜は線維化（子宮内膜周囲線維症）により胎盤形成能が低下し、繰り返す繁殖不全の原因となる。",
        "Intrauterine inflammatory exudate/pathogens create a hostile environment for embryo implantation, causing early embryonic death and failure to conceive; chronically inflamed endometrium develops periglandular fibrosis that impairs placentation, underlying recurrent breeding failure.",
    )


def _colitis_horse(sp):
    return (
        "馬の大腸炎（急性下痢症）は、大結腸・盲腸の重度炎症を来す生命を脅かす疾患群で、サルモネラ・Clostridioides difficile/perfringens、抗菌薬関連の腸内細菌叢異常、寄生虫、砂による刺激、NSAIDs毒性など多様な原因がある。",
        "Equine colitis (acute diarrhoeal disease) is a life-threatening group of conditions causing severe inflammation of the large colon and caecum, with diverse causes including Salmonella, Clostridioides difficile/perfringens, antimicrobial-associated dysbiosis, parasites, sand irritation and NSAID toxicity.",
        "結腸粘膜の炎症・壊死により水分・電解質の吸収能が失われ、大量の水様下痢と急速な脱水・低蛋白血症・低循環血液量性ショックを生じる。内毒素の吸収により全身性炎症反応・DIC・蹄葉炎を合併しうる致死率の高い疾患。",
        "Colonic mucosal inflammation and necrosis abolish water/electrolyte absorption, causing profuse watery diarrhoea with rapid dehydration, hypoproteinaemia and hypovolaemic shock; endotoxin absorption can trigger SIRS, DIC and laminitis, making this a highly fatal condition.",
    )


def _choke_horse(sp):
    return (
        "馬の食道閉塞（チョーク）は、乾燥した飼料塊（乾草キューブ・ペレット）や異物による食道内腔の閉塞で、早食い・不十分な咀嚼（歯科疾患）・脱水が誘因となる。",
        "Oesophageal obstruction (choke) in horses is luminal blockage by a bolus of dry feed (hay cubes, pellets) or a foreign body, precipitated by rapid eating, inadequate mastication (dental disease) and dehydration.",
        "閉塞部より近位に唾液・飼料が貯留し、鼻腔からの流出（両側性鼻漏）や誤嚥性肺炎のリスクを生じる。閉塞の圧迫・停滞時間が長引くと食道粘膜の圧迫壊死・穿孔、治癒後の狭窄に至ることがある。",
        "Saliva and feed accumulate proximal to the obstruction, causing nasal reflux (bilateral) and a risk of aspiration pneumonia; prolonged compression can cause pressure necrosis and perforation of the oesophageal mucosa, with stricture as a healing sequela.",
    )


def _guttural_pouch_disease_horse(sp):
    return (
        "馬の喉嚢疾患群（喉嚢蓄膿症・喉嚢鼓脹・喉嚢真菌症）は、馬に特有の耳管憩室（喉嚢）に生じる疾患群で、蓄膿は腺疫後の膿・膿石貯留、鼓脹は幼駒の耳管開口部弁機能異常による空気貯留、真菌症は喉嚢内壁への日和見感染による。",
        "Equine guttural pouch diseases (empyema, tympany, mycosis) affect the horse-specific auditory tube diverticulum: empyema is pus/chondroid accumulation after strangles, tympany is air trapping in foals from a malfunctioning pharyngeal-opening valve, and mycosis is opportunistic fungal infection of the pouch lining.",
        "蓄膿は貯留膿汁による膨隆・鼻漏・咽頭圧迫を、鼓脹は空気貯留による非疼痛性の頬部膨隆・呼吸/嚥下障害を生じる。真菌症は内頸動脈等の血管壁を侵食して致死的な鼻出血や、隣接脳神経障害（嚥下障害・喉頭麻痺・ホルネル症候群）を招く最も重篤な型。",
        "Empyema causes swelling, nasal discharge and pharyngeal compression from retained pus; tympany causes non-painful cheek distension with respiratory/swallowing difficulty from trapped air; mycosis is the most serious form, eroding vessel walls (e.g. internal carotid) to cause life-threatening epistaxis and adjacent cranial-nerve deficits (dysphagia, laryngeal paralysis, Horner's syndrome).",
    )


def _spaopd_horse(sp):
    return (
        "馬の夏季牧草喘息（SPAOPD）は、夏季の温暖湿潤環境での放牧中に牧草・カビ胞子・花粉等の環境アレルゲンに対する過敏反応で生じる下部気道の好中球性炎症疾患で、冬季の馬舎内飼育で生じるIAD/RAOの夏季放牧型に相当する。",
        "Summer pasture-associated obstructive pulmonary disease (SPAOPD) in horses is neutrophilic lower-airway inflammation from a hypersensitivity response to environmental allergens (pasture grasses, mould spores, pollens) encountered on summer pasture in warm, humid regions — the pasture-based summer counterpart of stable-associated IAD/RAO.",
        "アレルゲン曝露が気道の好中球性炎症・気管支攣縮・粘液分泌過多を起こし、可逆的な気道閉塞による労作時呼吸困難・慢性咳嗽・鼻漏を生じる。放牧地からの隔離（畜舎管理への切替）で改善する点が診断の手がかりとなる。",
        "Allergen exposure provokes neutrophilic airway inflammation, bronchospasm and mucus hypersecretion, causing reversible airway obstruction with exertional dyspnoea, chronic cough and nasal discharge; improvement on removal from pasture (switching to stable management) is a diagnostic clue.",
    )


def _piroplasmosis_horse(sp):
    return (
        "馬ピロプラズマ症（バベシア症・タイレリア症）は、原虫 Babesia caballi・Theileria equi のマダニ媒介感染。国内は清浄地域だが、輸入検疫上重要な届出感染症。",
        "Equine piroplasmosis (babesiosis/theileriosis) is a tick-borne protozoal infection with Babesia caballi and/or Theileria equi; Japan is considered free of the disease, but it is a notifiable condition of major importance for import quarantine.",
        "原虫が赤血球内に侵入・増殖して血管内外の溶血を起こし、発熱・貧血・黄疸・血色素尿を生じる。重症例では播種性血管内凝固・多臓器障害に進行しうる。回復後も長期の不顕性キャリア化がみられる。",
        "The protozoa invade and multiply within red cells causing intra/extravascular haemolysis, producing fever, anaemia, icterus and haemoglobinuria; severe cases can progress to disseminated intravascular coagulation and multi-organ dysfunction, and recovered horses often become long-term subclinical carriers.",
    )


def _eru_horse(sp):
    return (
        "馬再発性ぶどう膜炎（ERU、月盲）は、免疫介在性の反復性ぶどう膜炎で、Leptospira感染への交差反応性自己免疫が主要な機序として関与するとされる、馬で最も多い失明原因疾患。特定品種（アパルーサ等）に好発する。",
        "Equine recurrent uveitis (ERU, moon blindness) is immune-mediated recurrent uveitis, thought to arise chiefly from a cross-reactive autoimmune response following Leptospira infection; it is the leading cause of blindness in horses, with certain breeds (Appaloosa) predisposed.",
        "自己免疫反応が反復して眼内炎症の再燃・寛解を繰り返し、そのたびに前房蓄膿・虹彩癒着・白内障・硝子体混濁・網膜剥離が蓄積的に進行する。反復発作の結果、緑内障や眼球癆に至り最終的に失明する。",
        "Repeated autoimmune flares of intraocular inflammation with intervening remission cause cumulative damage — hypopyon, iridal synechiae, cataract, vitreal opacity and retinal detachment accruing with each episode — ultimately leading to secondary glaucoma, phthisis bulbi and blindness.",
    )


def _epm_horse(sp):
    return (
        "馬原虫性脊髄脳炎（EPM）は、主にオポッサムを終宿主とする原虫 Sarcocystis neurona（稀にNeospora hughesi）の感染による。オポッサムの糞に汚染された飼料・水を介して馬（異常宿主）に感染する。",
        "Equine protozoal myeloencephalitis (EPM) is caused chiefly by the protozoan Sarcocystis neurona (rarely Neospora hughesi), whose definitive host is the opossum; horses (aberrant hosts) become infected via feed/water contaminated with opossum faeces.",
        "原虫が血液脳関門を越えて中枢神経に侵入し、脳・脊髄の非対称性の炎症・壊死巣を形成する。病変部位に応じて非対称性の運動失調・筋萎縮・脳神経障害など多彩な神経症状を呈し、進行性かつ非対称性であることが臨床的特徴。",
        "The protozoa cross the blood-brain barrier and invade the CNS, forming asymmetric foci of inflammation and necrosis in brain and spinal cord; the resulting signs — asymmetric ataxia, muscle atrophy, cranial-nerve deficits — vary with lesion location, with progressive, asymmetric involvement being the clinical hallmark.",
    )


def _pssm_horse(sp):
    return (
        "馬の多糖類蓄積性ミオパシー（PSSM）は、骨格筋でのグリコーゲン/異常多糖の異常蓄積を来す遺伝性代謝性筋疾患。1型はグリコーゲン合成酵素（GYS1）遺伝子変異、2型は原因遺伝子未同定で、クォーターホースやドラフト種等に好発する。",
        "Polysaccharide storage myopathy (PSSM) in horses is a heritable metabolic muscle disease causing abnormal accumulation of glycogen/abnormal polysaccharide in skeletal muscle; type 1 is caused by a glycogen synthase (GYS1) gene mutation, type 2 has no identified gene, and both are common in Quarter Horses and draft breeds.",
        "異常な糖代謝により筋細胞内に過剰なグリコーゲンまたは異常多糖が蓄積し、エネルギー産生効率が低下する。運動時にエネルギー需要を満たせず筋線維が壊死し、反復性の運動誘発性横紋筋融解（筋硬直・発汗・ミオグロビン尿）を生じる。",
        "Abnormal glucose metabolism causes excess glycogen or abnormal polysaccharide to accumulate within myocytes, impairing energy production efficiency; muscle fibres cannot meet exercise energy demand and undergo necrosis, producing recurrent exertional rhabdomyolysis (muscle stiffness, sweating, myoglobinuria).",
    )


def _placentitis_horse(sp):
    return (
        "馬の胎盤炎は、大半が子宮頸管を介した上行性細菌感染（Streptococcus equi subsp. zooepidemicus等）による胎盤の炎症で、子宮頸管閉鎖不全・双子妊娠・過去の分娩損傷が誘因となる。血行性感染（ノカルジア型胎盤炎）は稀。",
        "Equine placentitis is most often ascending bacterial infection through the cervix (chiefly Streptococcus equi subsp. zooepidemicus) causing placental inflammation, predisposed by cervical incompetence, twin pregnancy and prior parturition injury; haematogenous (nocardioform) placentitis is less common.",
        "感染が絨毛尿膜の炎症・剥離を起こして胎子への酸素・栄養供給を障害し、早産・死産・虚弱子（敗血症性新生子）を招く。慢性の低悪性度感染は乳房早期発育・早産兆候として現れることがあり、早期発見と黄体機能維持治療が胎子救命の鍵となる。",
        "Infection inflames and separates the chorioallantois, impairing oxygen/nutrient delivery to the fetus and causing premature birth, stillbirth or a weak, septic neonate; low-grade chronic infection can present as premature udder development, and early detection with luteal-support therapy is key to fetal survival.",
    )


# name-pattern -> generator. species_set restricts host; exclusions guard collisions.
_FLAGSHIPS: tuple[tuple[frozenset | None, tuple[str, ...], tuple[str, ...], object], ...] = (
    (frozenset({"cat"}), ("甲状腺機能亢進", "hyperthyroid"), ("副甲状腺",), _feline_hyperthyroid),
    (frozenset({"cat"}), ("アルドステロン", "aldosteron", "conn"), (), _feline_hyperaldosteronism),
    (
        frozenset({"cat"}),
        ("先端巨大症", "先端巨大", "acromegaly", "somatotrop", "成長ホルモン"),
        (),
        _feline_acromegaly,
    ),
    (
        frozenset({"cat"}),
        ("大動脈血栓", "サドル血栓", "aortic thromboembolism", "saddle thrombus"),
        (),
        _saddle_thrombus,
    ),
    (
        None,
        ("全身性高血圧", "systemic hypertension", "高血圧症"),
        ("肺高血圧", "pulmonary hyperten"),
        _systemic_hypertension,
    ),
    (frozenset({"dog"}), ("動脈管開存", "patent ductus", "pda"), (), _pda),
    (
        frozenset({"dog"}),
        ("大動脈弁下狭窄", "大動脈弁狭窄", "subaortic stenosis", "aortic stenosis"),
        (),
        _subaortic_stenosis,
    ),
    (
        frozenset({"dog"}),
        ("肺動脈狭窄", "肺動脈弁狭窄", "pulmonic stenosis", "pulmonary stenosis"),
        (),
        _pulmonic_stenosis,
    ),
    (frozenset({"dog"}), ("レッグ", "ペルテス", "perthes", "legg-calv"), (), _legg_calve_perthes),
    (None, ("離断性骨軟骨症", "骨軟骨症", "osteochondritis dissecans", "osteochondrosis"), (), _ocd),
    (frozenset({"dog"}), ("汎骨炎", "パノステ", "panosteitis", "汎発性骨炎", "好酸球性汎骨炎"), (), _panosteitis),
    (frozenset({"dog"}), ("肥大性骨異栄養症", "骨異栄養症", "hypertrophic osteodystrophy", " hod"), (), _hod),
    (
        None,
        ("ウォブラー", "頸部脊椎症性脊髄症", "頚部脊椎症", "wobbler", "cervical spondylomyelopathy", "頸椎不安定"),
        (),
        _wobbler,
    ),
    (frozenset({"dog"}), ("短頭種気道", "短頭種上部気道", "brachycephalic", "boas"), (), _boas),
    (None, ("認知機能不全", "認知障害", "cognitive dysfunction", "cds"), (), _cds),
    (
        frozenset({"dog"}),
        (
            "肉芽腫性髄膜脳",
            "肉芽腫性髄膜炎",
            "granulomatous meningoencephal",
            "壊死性髄膜脳炎",
            "necrotizing meningoencephal",
            "meningoencephalitis of unknown",
        ),
        (),
        _gme,
    ),
    (frozenset({"dog"}), ("脂腺炎", "皮脂腺炎", "sebaceous adenitis"), (), _sebaceous_adenitis),
    (None, ("落葉状天疱瘡", "天疱瘡", "pemphigus"), ("類天疱瘡",), _pemphigus_foliaceus),
    (frozenset({"dog"}), ("脱毛症x", "脱毛症X", "alopecia x", "毛周期停止", "成長ホルモン反応性脱毛"), (), _alopecia_x),
    (
        frozenset({"cat"}),
        (
            "好酸球性肉芽腫",
            "好酸球性局面",
            "好酸球性プラーク",
            "無痛性潰瘍",
            "eosinophilic granuloma",
            "eosinophilic plaque",
            "eosinophilic ulcer",
            "indolent ulcer",
            "linear granuloma",
        ),
        (),
        _eosinophilic_granuloma,
    ),
    # --- Batch 2: bilingual backfill of high-traffic JA-curated flagships ---
    (frozenset({"dog"}), ("胃拡張", "gastric dilatation", "gastric dilatation-volvulus"), (), _gdv),
    (
        frozenset({"dog", "cat"}),
        ("膵炎", "pancreatitis"),
        ("膵外分泌不全", "exocrine pancreatic", "膵癌", "膵臓癌", "pancreatic carcinoma", "pancreatic adenocarcinoma"),
        _pancreatitis,
    ),
    (frozenset({"dog"}), ("甲状腺機能低下", "hypothyroid"), ("副甲状腺", "先天性"), _hypothyroid_dog),
    (frozenset({"dog"}), ("クッシング", "副腎皮質機能亢進", "cushing", "hyperadrenocorticism"), (), _cushing_dog),
    (frozenset({"dog", "cat"}), ("慢性腎臓病", "慢性腎不全", "chronic kidney", "chronic renal"), (), _ckd),
    (frozenset({"dog"}), ("アトピー性皮膚炎", "atopic dermatitis"), (), _atopic_dermatitis_dog),
    (
        frozenset({"dog", "cat"}),
        ("変形性関節症", "骨関節炎", "osteoarthritis", "degenerative joint disease"),
        (),
        _osteoarthritis,
    ),
    (frozenset({"dog"}), ("椎間板ヘルニア", "intervertebral disc", "ivdd"), (), _ivdd_dog),
    (frozenset({"dog"}), ("特発性てんかん", "若年性てんかん", "idiopathic epilepsy"), (), _epilepsy_dog),
    (frozenset({"dog"}), ("拡張型心筋症", "dilated cardiomyopathy"), (), _dcm_dog),
    (
        frozenset({"dog"}),
        (
            "粘液腫様僧帽弁",
            "僧帽弁閉鎖不全",
            "僧帽弁逆流",
            "僧帽弁変性",
            "myxomatous mitral",
            "degenerative mitral valve",
        ),
        ("形成不全",),
        _mmvd_dog,
    ),
    (
        frozenset({"dog", "cat"}),
        ("糖尿病", "diabetes mellitus"),
        ("ケトアシドーシス", "ketoacidosis", "尿崩症", "insipidus"),
        _diabetes,
    ),
    (frozenset({"cat"}), ("炎症性腸疾患", "inflammatory bowel"), (), _ibd_cat),
    (frozenset({"cat"}), ("肝リピドーシス", "脂肪肝", "hepatic lipidosis"), (), _hepatic_lipidosis_cat),
    (frozenset({"cat"}), ("喘息", "asthma"), (), _feline_asthma),
    # --- Batch 3: further bilingual backfill of high-traffic JA-curated flagships ---
    # Shared across species.
    (None, ("緑内障", "glaucoma"), (), _glaucoma_biling),
    (None, ("乾性角結膜炎", "ドライアイ", "keratoconjunctivitis sicca", " kcs"), (), _kcs_biling),
    (None, ("角膜潰瘍", "corneal ulcer"), (), _corneal_ulcer_biling),
    (None, ("尿崩症", "diabetes insipidus"), (), _diabetes_insipidus),
    # Dog.
    (frozenset({"dog"}), ("股関節形成不全", "hip dysplasia"), (), _hip_dysplasia_dog),
    (frozenset({"dog"}), ("肘関節形成不全", "elbow dysplasia"), (), _elbow_dysplasia_dog),
    (frozenset({"dog"}), ("十字靭帯", "十字靴帯", "cruciate ligament", "cranial cruciate"), (), _cruciate_dog),
    (frozenset({"dog"}), ("白内障", "cataract"), (), _cataracts_dog),
    (
        frozenset({"dog"}),
        ("進行性網膜萎縮", "progressive retinal atrophy"),
        (),
        _pra_dog,
    ),
    (frozenset({"dog"}), ("チェリーアイ", "第三眼瞼腺脱出", "cherry eye"), (), _cherry_eye_dog),
    (frozenset({"dog"}), ("膿皮症", "pyoderma"), (), _pyoderma_dog),
    (frozenset({"dog"}), ("アジソン", "副腎皮質機能低下", "addison", "hypoadrenocorticism"), (), _addison_dog),
    (
        frozenset({"dog"}),
        ("免疫介在性溶血性貧血", "immune-mediated hemolytic anemia", "immune-mediated haemolytic anaemia", "imha"),
        (),
        _imha_dog,
    ),
    (frozenset({"dog"}), ("血管肉腫", "hemangiosarcoma", "haemangiosarcoma"), (), _hemangiosarcoma_dog),
    (frozenset({"dog"}), ("骨肉腫", "osteosarcoma"), ("軟骨",), _osteosarcoma_dog),
    (frozenset({"dog"}), ("肥満細胞腫", "mast cell tumor", "mast cell tumour"), (), _mct_dog),
    (frozenset({"dog"}), ("リンパ腫", "lymphoma"), (), _lymphoma_dog),
    (
        frozenset({"dog"}),
        ("門脈体循環シャント", "肝シャント", "portosystemic shunt", "liver shunt"),
        (),
        _pss_dog,
    ),
    (frozenset({"dog"}), ("巨大食道症", "megaesophagus", "megaoesophagus"), (), _megaesophagus_dog),
    (
        frozenset({"dog"}),
        ("膵外分泌不全", "exocrine pancreatic insufficiency"),
        (),
        _epi_dog,
    ),
    (frozenset({"dog"}), ("慢性肝炎", "chronic hepatitis"), (), _chronic_hepatitis_dog),
    (frozenset({"dog"}), ("胆嚢粘液嚢腫", "gallbladder mucocele"), (), _gb_mucocele_dog),
    (frozenset({"dog"}), ("副甲状腺機能低下", "hypoparathyroidism"), ("栄養性",), _hypoparathyroidism_dog),
    (frozenset({"dog"}), ("変性性脊髄症", "degenerative myelopathy"), (), _degenerative_myelopathy_dog),
    (frozenset({"dog"}), ("喉頭麻痺", "laryngeal paralysis"), (), _laryngeal_paralysis_dog),
    (frozenset({"dog"}), ("前立腺肥大", "benign prostatic hyperplasia", "bph"), (), _bph_dog),
    (frozenset({"dog"}), ("膝蓋骨脱臼", "パテラ", "patellar luxation"), (), _patellar_luxation_dog),
    (frozenset({"dog"}), ("右大動脈弓遺残", "persistent right aortic arch", "praa"), (), _praa_dog),
    (frozenset({"dog"}), ("肛門嚢", "anal sac"), ("癌", "carcinoma"), _anal_sac_disease_dog),
    (
        frozenset({"dog"}),
        ("蛋白漏出性腸症", "protein-losing enteropathy", "protein losing enteropathy"),
        (),
        _ple_dog,
    ),
    (frozenset({"dog"}), ("胃食道逆流症", "gastroesophageal reflux", "gerd"), (), _gerd_dog),
    (frozenset({"dog"}), ("食道炎", "esophagitis", "oesophagitis"), (), _esophagitis_dog),
    (
        frozenset({"dog"}),
        ("馬尾症候群", "腰仙部狭窄症", "cauda equina", "lumbosacral stenosis"),
        (),
        _cauda_equina_dog,
    ),
    (frozenset({"dog"}), ("顔面神経麻痺", "facial nerve paralysis", "facial paralysis"), (), _facial_paralysis_dog),
    # Cat.
    (frozenset({"cat"}), ("肥大型心筋症", "hypertrophic cardiomyopathy", "hcm"), (), _hcm_cat),
    (frozenset({"cat"}), ("拡張型心筋症", "dilated cardiomyopathy"), (), _dcm_cat),
    (frozenset({"cat"}), ("拘束型心筋症", "restrictive cardiomyopathy"), (), _rcm_cat),
    (
        frozenset({"cat"}),
        ("胆管炎", "胆管肝炎", "cholangitis", "cholangiohepatitis"),
        (),
        _cholangitis_cat,
    ),
    (
        frozenset({"cat"}),
        ("巨大結腸症", "便秘", "宿便", "megacolon", "constipation", "obstipation"),
        (),
        _megacolon_cat,
    ),
    (
        frozenset({"cat"}),
        ("尿道閉塞", "urinary obstruction", "urethral obstruction", "blocked cat"),
        (),
        _feline_urethral_obstruction,
    ),
    (frozenset({"cat"}), ("多発性嚢胞腎", "polycystic kidney", "pkd"), (), _pkd_cat),
    # Excludes symblepharon (癒着性角結膜炎/adhesive keratoconjunctivitis) — a distinct
    # cicatricial sequela of severe neonatal herpetic conjunctivitis, not simple conjunctivitis.
    (
        frozenset({"cat"}),
        ("結膜炎", "conjunctivitis"),
        ("癒着性", "symblepharon"),
        _conjunctivitis_cat,
    ),
    (frozenset({"cat"}), ("ぶどう膜炎", "uveitis"), ("好酸球性角結膜炎",), _uveitis_cat),
    (
        frozenset({"cat"}),
        ("好酸球性角結膜炎", "eosinophilic keratoconjunctivitis"),
        (),
        _eosinophilic_kcj_cat,
    ),
    (
        frozenset({"cat"}),
        ("角膜壊死", "角膜分離症", "corneal sequestrum"),
        (),
        _corneal_sequestrum_cat,
    ),
    (frozenset({"cat"}), ("歯肉口内炎", "gingivostomatitis"), (), _fcgs_cat),
    (
        frozenset({"cat"}),
        ("免疫介在性血小板減少症", "immune-mediated thrombocytopenia", "itp"),
        (),
        _itp_cat,
    ),
    (frozenset({"cat"}), ("三叉神経炎", "trigeminal neuritis"), (), _trigeminal_neuritis_cat),
    (frozenset({"cat"}), ("心筋炎", "myocarditis"), (), _myocarditis_cat),
    (
        frozenset({"cat"}),
        ("シュウ酸カルシウム", "calcium oxalate"),
        (),
        _calcium_oxalate_urolith_cat,
    ),
    (frozenset({"cat"}), ("ストルバイト", "struvite"), (), _struvite_urolith_cat),
    (
        frozenset({"cat"}),
        ("原発性副甲状腺機能亢進", "primary hyperparathyroidism"),
        (),
        _hyperparathyroidism_primary_cat,
    ),
    (
        frozenset({"cat"}),
        ("腎性二次性副甲状腺機能亢進", "renal secondary hyperparathyroidism"),
        (),
        _hyperparathyroidism_renal_cat,
    ),
    # Horse.
    (
        frozenset({"horse"}),
        ("屈腱炎", "屈腱損傷", "tendonitis", "tendinitis", "flexor tendon"),
        (),
        _tendinitis_horse,
    ),
    (frozenset({"horse"}), ("胃潰瘍", "gastric ulcer", "egus"), (), _egus_horse),
    (frozenset({"horse"}), ("ピロプラズマ症", "piroplasmosis"), (), _piroplasmosis_horse),
    (
        frozenset({"horse"}),
        ("再発性ぶどう膜炎", "回帰性ぶどう膜炎", "月盲", "recurrent uveitis", "moon blindness"),
        (),
        _eru_horse,
    ),
    (
        frozenset({"horse"}),
        ("原虫性脊髄脳炎", "protozoal myeloencephalitis", "epm"),
        (),
        _epm_horse,
    ),
    (
        frozenset({"horse"}),
        ("多糖類蓄積性ミオパシー", "多糖体蓄積性ミオパチー", "polysaccharide storage myopathy", "pssm"),
        (),
        _pssm_horse,
    ),
    (frozenset({"horse"}), ("メタボリック症候群", "metabolic syndrome", "ems"), (), _ems_horse),
    (
        frozenset({"horse"}),
        ("下垂体中葉機能障害", "pituitary pars intermedia", "ppid"),
        (),
        _ppid_horse,
    ),
    (
        frozenset({"horse"}),
        ("横紋筋融解症", "タイングアップ", "exertional rhabdomyolysis", "tying up", "tying-up", "tying up (er)"),
        (),
        _rhabdomyolysis_horse,
    ),
    (frozenset({"horse"}), ("子宮内膜炎", "endometritis"), (), _endometritis_horse),
    (frozenset({"horse"}), ("大腸炎", "colitis"), (), _colitis_horse),
    (frozenset({"horse"}), ("食道閉塞", "チョーク", "esophageal obstruction", "choke"), (), _choke_horse),
    (
        frozenset({"horse"}),
        ("喉嚢蓄膿", "喉嚢鼓脹", "喉嚢鼓張", "guttural pouch empyema", "guttural pouch tympany"),
        (),
        _guttural_pouch_disease_horse,
    ),
    (
        frozenset({"horse"}),
        ("夏季牧草喘息", "summer pasture", "spaopd"),
        (),
        _spaopd_horse,
    ),
    (frozenset({"horse"}), ("胎盤炎", "placentitis"), (), _placentitis_horse),
)


def resolve_flagship(name_ja: str, name_en: str, species: str):
    """Return the generator for a curated non-infectious flagship, or None."""
    name = _neutralise_negations(f"{name_ja or ''} {name_en or ''}").lower()
    sp = (species or "").lower()
    for species_set, subs, excl, gen in _FLAGSHIPS:
        if species_set is not None and sp not in species_set:
            continue
        if not any(s.lower() in name for s in subs):
            continue
        if any(b.lower() in name for b in excl):
            continue
        return gen
    return None


def flagship_clinical_fields(species: str, name_ja: str, name_en: str) -> dict | None:
    """Curated bilingual causes / pathophysiology for a non-infectious flagship."""
    gen = resolve_flagship(name_ja, name_en, species)
    if gen is None:
        return None
    cja, cen, pja, pen = gen((species or "").lower())
    return {
        "causes_ja": cja,
        "causes": cen,
        "pathophysiology_ja": pja,
        "pathophysiology": pen,
    }
