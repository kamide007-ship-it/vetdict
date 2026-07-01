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
