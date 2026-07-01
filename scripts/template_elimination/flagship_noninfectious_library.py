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
