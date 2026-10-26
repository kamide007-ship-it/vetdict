"""Curated treatments for mammal records that carried the exotic nutrition template.

The nutrition fallback (「…は栄養素過不足の特定と食事処方の見直しが治療の根幹…
Quesenberry & Carpenter (Exotic Animal Medicine…) を参照」) was stamped on the
Japanese treatment of mammal records it does not fit: emergency hypercalcaemia
(dog/cat/rabbit vitamin D toxicosis) presented as a 4-8 week diet change, an
equine dental condition (supernumerary tooth) given a nutrition protocol, and a
small-mammal reference text cited for dogs, cats and horses. Several English
fields were also wrong — the cat NSHP overlay carried the feline
*hyperthyroidism* protocol, and the small-mammal vitamin A deficiency text
described birds and reptiles.

Japanese entries follow the existing curated English protocol where that was
sound (doses unchanged); the remaining entries are written from the cited
references. ``en`` is set only where the English field also needed fixing.
"""

ENTRIES: dict[tuple[str, str], dict[str, str]] = {
    ("dog", "Vitamin D Toxicosis"): {
        "ja": (
            "【救急 — 高カルシウム血症→腎不全・軟部組織石灰化】"
            "除染: 早期なら催吐・活性炭。輸液: 0.9%生理食塩水 4-6 mL/kg/h でカルシウム利尿を促進"
            "（乳酸リンゲルはCa含有のため避ける）。フロセミド 2-5 mg/kg IV q8-12h（脱水補正後に開始）。"
            "コルチコステロイド: デキサメタゾン 0.1-0.2 mg/kg IV q12h（腸管Ca吸収の抑制）。"
            "パミドロネート 1-2 mg/kg IV（2時間かけて点滴、破骨細胞抑制）。"
            "カルシトニン 4-6 IU/kg SC/IM q8h（急性重症例）。水酸化アルミニウム 30-90 mg/kg/日 PO（リン吸着）。"
            "原因: コレカルシフェロール系殺鼠剤、乾癬用軟膏（カルシポトリオール）、サプリメント。"
            "監視: イオン化Ca・リン・腎機能を q12-24h。作用は2-3週間持続しうる。"
            "予後: 早期治療で中程度、腎不全・石灰化が成立後は不良（Talcott 2013; Rumbeiha 2000）。"
        ),
    },
    ("cat", "Feline Vitamin D Toxicosis"): {
        "ja": (
            "【救急 — 高カルシウム血症＋急性腎障害＋軟部組織石灰化】"
            "除染: 摂取後2時間以内なら催吐、活性炭 1-2 g/kg PO。輸液: 0.9%生理食塩水 4-6 mL/kg/h"
            "（積極的利尿が必須）。フロセミド 2-4 mg/kg IV q8h。プレドニゾロン 1-2 mg/kg PO q12h。"
            "ビスホスホネート: パミドロネート 1-2 mg/kg IV（2時間かけて、5-7日後に再投与可 — 重症・難治例の第一選択）。"
            "カルシトニン 4-7 U/kg SC q6-8h（短時間作用、タキフィラキシーあり）。"
            "ビタミンD源の除去: コレカルシフェロール系殺鼠剤、カルシポトリエン（乾癬用軟膏）、サプリメント。"
            "監視: Ca・リン・BUN・クレアチニン・尿量・心電図。予後: 軽症は中程度、石灰化を伴う急性腎障害は慎重"
            "（Rumbeiha 2000; Peterson 1991）。"
        ),
    },
    ("rabbit", "Vitamin D Toxicity"): {
        "ja": (
            "ビタミンD中毒は軟部組織（腎・大動脈・胃粘膜）の石灰化を伴う高カルシウム血症を起こす。"
            "すべてのビタミンD補給とカルシウムの多い食品を直ちに中止。0.9%生理食塩水 10-15 mL/kg/h IV で"
            "カルシウム利尿（乳酸リンゲルはCa含有のため避ける）。フロセミド 1-4 mg/kg IV/IM q4-6h。"
            "プレドニゾロン 1-2 mg/kg PO q12h（短期間 — ウサギではステロイドが消化管うっ滞を誘発するため"
            "メトクロプラミド 0.5-1.0 mg/kg SC q6-8h を併用）。急性重症例はカルシトニン 4-6 IU/kg SC q8-12h。"
            "血清総Ca・イオン化Caを正常化まで q6-12h、腎機能（BUN・クレアチニン）を監視 — 腎石灰化は不可逆の"
            "腎障害を残しうる。食事はチモシー乾草（低Ca）へ移行しアルファルファを恒久的に除去、十分な飲水を確保。"
            "処方されたもの以外のビタミン・ミネラル補給は行わない。ウサギは食餌中のCaを摂取量に比例して吸収し"
            "腎から排泄するため、ビタミンD/Ca過剰に特に弱い（Harcourt-Brown 2002; Quesenberry & Carpenter 4th ed）。"
        ),
    },
    ("cat", "Nutritional Secondary Hyperparathyroidism"): {
        "ja": (
            "食事の是正が治療の中心: 肉のみの手作り食・生肉食をやめ、総合栄養食の市販キャットフードへ切り替える"
            "（Ca:P比 約1.1-1.4:1）。重度例は炭酸カルシウム 50-100 mg/kg/日 PO を短期間併用し、血清Ca・リンを監視"
            "（総合栄養食に切り替えた後のビタミンD3追加は高Ca血症の危険があり通常不要）。"
            "病的骨折予防のため骨の再石灰化（3-6週）までケージレスト。鎮痛: ブプレノルフィン 0.01-0.02 mg/kg 口腔粘膜/IM"
            "（脱水・腎機能低下時はNSAIDsを避ける）。折れ曲がり骨折は骨質が回復するまで外科固定を急がない。"
            "骨盤変形による便秘にはラクツロース等で排便管理。予後: 食事是正で通常良好、骨盤狭窄が残ると慢性便秘の原因に"
            "（Tomsa 1999 J Small Anim Pract; Ettinger 8th ed）。"
        ),
        "en": (
            "Dietary correction is the core of treatment: stop all-meat home-made or raw meat diets and switch to a "
            "complete and balanced commercial cat food (Ca:P approx. 1.1-1.4:1). In severe cases add calcium carbonate "
            "50-100 mg/kg/day PO short-term while monitoring serum calcium and phosphorus (extra vitamin D3 is usually "
            "unnecessary once on a complete diet and risks hypercalcaemia). Cage rest until bone remineralises (3-6 weeks) "
            "to prevent pathological fractures. Analgesia: buprenorphine 0.01-0.02 mg/kg OTM/IM (avoid NSAIDs if "
            "dehydrated or azotaemic). Do not rush surgical fixation of folding fractures before bone quality recovers. "
            "Manage constipation from pelvic deformity (lactulose). Prognosis: usually good with dietary correction; "
            "residual pelvic narrowing can cause chronic obstipation (Tomsa 1999 J Small Anim Pract; Ettinger 8th ed)."
        ),
    },
    ("cat", "Feline Niacin Deficiency (Pellagra)"): {
        "ja": (
            "ナイアシン補給: ナイアシンアミド（ニコチンアミド）10-15 mg/頭 PO q24h（ニコチン酸より副作用が少ない）。"
            "食事是正: 総合栄養食の市販キャットフードを給与（猫はトリプトファンから十分なナイアシンを合成できず、"
            "食事からの摂取が必須）。生魚のみの食事は避ける。臨床徴候: 皮膚炎（特に口腔・舌の潰瘍）、下痢、精神症状"
            "（ペラグラの3D）。補給後1-2週間で速やかに改善。予防: AAFCO/FEDIAF の最低ナイアシン要求量"
            "（乾物40 mg/kg）を満たす食事。予後: 補給と食事是正で極めて良好（NRC 2006）。"
        ),
    },
    ("horse", "Supernumerary Tooth"): {
        "ja": (
            "立位鎮静（デトミジン＋ブトルファノール）下の口腔検査・口腔内視鏡、頭部X線（必要に応じCT）で過剰歯の位置と"
            "咬合・歯周への影響を評価する。対合歯の過長（過剰歯の対側に生じる）はモーター式フロートで定期的に整復し、"
            "食片の詰まりによる歯周病は洗浄・管理する。無症状なら抜歯せず経過観察。歯周病・重度の咬合異常・"
            "食片嵌入を起こす場合は抜歯（口腔内抜歯、困難例は外科的抜歯）を検討。"
            "鎮痛・抗炎症: フルニキシン・メグルミン 1.1 mg/kg IV/PO q12-24h（短期）。"
            "6-12ヶ月毎の歯科検診で再過長を防ぐ（Dixon & du Toit, Equine Dentistry 3rd ed; Easley 2011）。"
        ),
        "en": (
            "Oral examination and oral endoscopy under standing sedation (detomidine + butorphanol), with skull "
            "radiographs (CT where needed) to locate the supernumerary tooth and assess its effect on occlusion and the "
            "periodontium. Reduce the overgrowth that develops on the opposing tooth with a motorised float at regular "
            "intervals, and lavage/manage food packing and periodontal disease. Asymptomatic teeth are monitored, not "
            "extracted; extraction (oral, or surgical when difficult) is considered for periodontal disease, severe "
            "malocclusion or food impaction. Analgesia: flunixin meglumine 1.1 mg/kg IV/PO q12-24h short-term. "
            "Dental re-examination every 6-12 months prevents recurrent overgrowth (Dixon & du Toit, Equine Dentistry "
            "3rd ed; Easley 2011)."
        ),
    },
    ("guinea_pig", "Hypovitaminosis C - Dental"): {
        "ja": (
            "【採食できない場合は救急】ビタミンC 50-100 mg/kg SC q24h×7日。コラーゲン形成障害による切歯・臼歯の"
            "不正咬合は麻酔下で歯の整復（バーリング）。採食不能なら強制給餌（クリティカルケア）が必須。"
            "歯肉炎: 0.12%クロルヘキシジン口腔洗浄。鎮痛: メロキシカム 0.3-0.5 mg/kg q24h。"
            "長期管理: ビタミンC 最低50 mg/kg/日、歯の摩耗のための牧草。予後: ビタミンC補正と歯科管理で中程度、"
            "慢性変化は完全には戻らないことがある（Quesenberry & Carpenter 4th ed）。"
        ),
    },
}

_VITA_MAMMAL_JA = (
    "{sp}のビタミンA欠乏は緑黄色野菜を欠く単調な食事で起こり、眼（結膜炎・角膜障害）、皮膚、呼吸器・生殖器の"
    "上皮障害（繁殖障害・新生子の異常）として現れる。食事の是正が根本治療: {diet}。"
    "重症例のみビタミンA 1,000-5,000 IU/kg IM を単回投与し、7-14日後に再評価（過剰症も同様の繁殖障害・"
    "肝毒性を起こすため反復投与や経口サプリメントの併用はしない。妊娠個体では特に慎重に）。"
    "二次的な眼・呼吸器感染は培養に基づき治療（{abx}）。予後: 食事是正で良好、慢性の上皮変化は残ることがある"
    "（Quesenberry & Carpenter 4th ed; Carpenter Exotic Animal Formulary 6th ed）。"
)
_VITA_MAMMAL_EN = (
    "Vitamin A deficiency in {sp_en} follows monotonous diets lacking leafy greens and orange vegetables and presents "
    "as ocular (conjunctivitis, corneal disease), skin, respiratory and reproductive epithelial disease (infertility, "
    "neonatal abnormalities). Dietary correction is the definitive treatment: {diet_en}. Only severe cases receive a "
    "single dose of vitamin A 1,000-5,000 IU/kg IM, re-evaluated at 7-14 days (hypervitaminosis A causes the same "
    "reproductive failure and hepatotoxicity — do not repeat doses or add oral supplements; take particular care in "
    "pregnant animals). Treat secondary ocular/respiratory infection on culture ({abx_en}). Prognosis: good with "
    "dietary correction; chronic epithelial changes may persist (Quesenberry & Carpenter 4th ed; Carpenter Exotic "
    "Animal Formulary 6th ed)."
)
_HERBIVORE_DIET_JA = "良質の牧草を主体に、にんじん・葉物野菜などβカロテンを含む新鮮な野菜と専用ペレットを給与"
_HERBIVORE_DIET_EN = (
    "grass hay as the staple with fresh beta-carotene vegetables (carrot, leafy greens) and species pellets"
)
for _sp, _ja, _en, _abx_ja, _abx_en in (
    ("rabbit", "ウサギ", "rabbits", "ペニシリン系の経口投与は禁忌", "never oral penicillins"),
    (
        "chinchilla",
        "チンチラ",
        "chinchillas",
        "経口のペニシリン・セファロスポリンは禁忌",
        "never oral penicillins or cephalosporins",
    ),
    (
        "guinea_pig",
        "モルモット",
        "guinea pigs",
        "経口のペニシリン・セファロスポリンは禁忌",
        "never oral penicillins or cephalosporins",
    ),
):
    ENTRIES[(_sp, "Vitamin A Deficiency" if _sp != "guinea_pig" else "Vitamin A Deficiency - Ocular")] = {
        "ja": _VITA_MAMMAL_JA.format(sp=_ja, diet=_HERBIVORE_DIET_JA, abx=_abx_ja),
        "en": _VITA_MAMMAL_EN.format(sp_en=_en, diet_en=_HERBIVORE_DIET_EN, abx_en=_abx_en),
    }
ENTRIES[("hamster", "Vitamin A Deficiency")] = {
    "ja": _VITA_MAMMAL_JA.format(
        sp="ハムスター",
        diet="ハムスター用ペレットを主食に、にんじん・ブロッコリー等の野菜を少量加える（種子のみの食事を避ける）",
        abx="エンロフロキサシン等。経口のペニシリン系・リンコマイシン系は禁忌",
    ),
    "en": _VITA_MAMMAL_EN.format(
        sp_en="hamsters",
        diet_en="hamster pellets as the staple with small amounts of carrot/broccoli (avoid seed-only diets)",
        abx_en="e.g. enrofloxacin; never oral penicillins or lincosamides",
    ),
}
ENTRIES[("hedgehog", "Vitamin A Deficiency")] = {
    "ja": _VITA_MAMMAL_JA.format(
        sp="ハリネズミ",
        diet="ハリネズミ用フードまたは高品質の低脂肪キャットフードを主食に、昆虫（ガットローディング済み）と少量の野菜を加える",
        abx="エンロフロキサシン等",
    ),
    "en": _VITA_MAMMAL_EN.format(
        sp_en="hedgehogs",
        diet_en="hedgehog diet or a high-quality low-fat cat food as the staple, with gut-loaded insects and some vegetables",
        abx_en="e.g. enrofloxacin",
    ),
}
ENTRIES[("hedgehog", "Vitamin E Deficiency")] = {
    "ja": (
        "ハリネズミのビタミンE欠乏は酸化した高脂肪食（古い魚・脂肪の多い餌）で起こり、筋障害・脂肪組織炎・"
        "ふらつきとして現れる。ビタミンE 10-15 IU/kg IM（または経口）＋必要に応じセレン 0.05-0.1 mg/kg IM"
        "（セレンは安全域が狭いため反復は慎重に）。酸化した餌を除き、新鮮なハリネズミ用フード/低脂肪キャットフードと"
        "昆虫へ食事を是正。ふらつき症候群（WHS）など神経疾患の鑑別を忘れない。予後: 早期の補給と食事是正で良好"
        "（Carpenter Exotic Animal Formulary 6th ed; Quesenberry & Carpenter 4th ed）。"
    ),
    "en": (
        "Vitamin E deficiency in hedgehogs follows oxidised high-fat diets (stale fish, fatty foods) and presents as "
        "myopathy, steatitis and ataxia. Give vitamin E 10-15 IU/kg IM (or PO) plus, where indicated, selenium "
        "0.05-0.1 mg/kg IM (narrow safety margin — repeat with caution). Remove oxidised food and correct the diet to "
        "fresh hedgehog food/low-fat cat food with insects. Keep wobbly hedgehog syndrome and other neurological "
        "disease in the differential. Prognosis: good with early supplementation and dietary correction (Carpenter "
        "Exotic Animal Formulary 6th ed; Quesenberry & Carpenter 4th ed)."
    ),
}
ENTRIES[("sugar_glider", "Iron Storage Disease (Hemochromatosis)")] = {
    "ja": (
        "瀉血（体重・PCVに応じ少量を反復）とキレート療法: デフェロキサミン 100 mg/kg IM を5-7日。"
        "鉄の少ない食事に切り替え、鉄の吸収を高めるビタミンCの多い果物・サプリメントを制限する。"
        "肝機能・PCVを監視。予後: 慎重（Brust 2009）。"
    ),
}
ENTRIES[("sugar_glider", "Vitamin A Toxicity")] = {
    "ja": (
        "ビタミンA過剰症は肝臓・レバーの多給や複数のサプリメントの重複で起こる。すべてのビタミンA源"
        "（レバー、ビタミン剤、強化フード）を直ちに中止し、バランスの取れたフクロモモンガ用の食事へ戻す。"
        "支持療法: 皮下輸液、疼痛（骨・関節の過形成）にメロキシカム 0.1-0.2 mg/kg PO q24h、採食不能時は強制給餌。"
        "肝酵素を監視し、骨・関節の変化はX線で評価。予後: 早期に原因を除けば良好、骨の過形成は残ることがある"
        "（Quesenberry & Carpenter 4th ed; Carpenter Exotic Animal Formulary 6th ed）。"
    ),
    "en": (
        "Hypervitaminosis A follows over-feeding of liver or overlapping supplements. Stop every vitamin A source "
        "(liver, vitamin products, fortified foods) at once and return to a balanced sugar glider diet. Supportive care: "
        "SC fluids, meloxicam 0.1-0.2 mg/kg PO q24h for bone/joint pain from hyperostosis, assisted feeding if "
        "anorexic. Monitor liver enzymes and assess skeletal changes radiographically. Prognosis: good if the cause is "
        "removed early; bony proliferation may persist (Quesenberry & Carpenter 4th ed; Carpenter Exotic Animal "
        "Formulary 6th ed)."
    ),
}

NUTRITION_TEMPLATE_MARKER = "栄養素過不足の特定と食事処方の見直しが治療の根幹"


def curated_treatment(species: str, name: str) -> dict[str, str] | None:
    return ENTRIES.get(((species or "").lower().replace(" ", "_"), name or ""))
