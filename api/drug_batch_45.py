"""Drug batch 45 – referenced-but-absent agents surfaced by the 2026-08 audit (14th sweep).

A dose-context katakana/English token sweep of disease treatment protocols,
cross-checked against the real text matcher (find_drugs_in_text), found three
agents that VetDict's own content instructs clinicians to use — with explicit
doses — yet were absent from the formulary:

  - フィナステリド (finasteride): the canine BPH entries cite
    "フィナステリド 0.1-0.5 mg/kg 経口 24時間ごと" / "Finasteride 0.1-0.5
    mg/kg PO" verbatim (Prostate Disease, Benign Prostatic Hyperplasia ×2)
    yet no 5α-reductase inhibitor existed in the dictionary.
  - 酢酸オサテロン (osaterone acetate, Ypozane): the same BPH entries cite
    "酢酸オサテロン（Ypozane 0.25-0.5 mg/kg PO 7日間）" — the EU-registered
    veterinary anti-androgen for canine BPH, absent from the dictionary.
    One BPH entry had even lost the drug name ("acetate 0.25-0.5 mg/kg PO"),
    fixed alongside this batch.
  - フィルグラスチム (filgrastim, rhG-CSF): referenced with dosing in 7
    entries (canine parvovirus ×2, immune-mediated neutropenia dog+cat,
    Border Collie trapped neutrophil syndrome, methimazole ADR, ferret
    hyperestrogenism) — "G-CSF（フィルグラスチム 5 μg/kg SC q24h）" — yet no
    colony-stimulating factor existed in the dictionary.

References:
  - Sirinarumitr K et al. JAVMA 2001;218:1275-1280 — finasteride 16 weeks in
    BPH dogs: ~43% prostatic volume reduction, semen quality and libido
    preserved.
  - Iguer-Ouada M, Verstegen JP. Theriogenology 1997 — finasteride effects on
    canine prostatic fluid and semen.
  - Albouy M et al. Vet Rec 2008;163:179-183 — osaterone acetate (Ypozane)
    0.25-0.5 mg/kg PO ×7 days: onset within 2 weeks, efficacy maintained
    ~5-6 months, fertility preserved; comparison with delmadinone.
  - Ypozane EU SPC (Virbac) — transient attenuation of the ACTH-stimulated
    cortisol response for several weeks after treatment.
  - Plumb's Veterinary Drug Handbook, 10th ed — filgrastim 5 µg/kg SC q24h;
    anti-rhG-CSF antibody formation with prolonged use in dogs and cats.
  - Hammond WP et al. Blood 1991 / Reagan WJ et al. 1995 — neutralising
    antibodies against rhG-CSF in dogs cross-react with endogenous G-CSF and
    can cause persistent neutropenia after prolonged dosing.
  - Duffy A et al. J Vet Emerg Crit Care 2010 — rhG-CSF in parvoviral
    enteritis: no clear survival benefit; reserve for severe prolonged
    neutropenia.
"""

DRUGS_BATCH_45: list[dict] = [
    {
        "id": "finasteride",
        "search_aliases": [
            "フィナステリド",
            "プロスカー",
            "Finasteride",
            "Proscar",
        ],
        "name": "Finasteride",
        "name_ja": "フィナステリド（プロスカー）",
        "category": "reproductive",
        "mechanism": "Type II 5α-reductase inhibitor. Blocks conversion of testosterone to dihydrotestosterone (DHT), the androgen driving prostatic hyperplasia, causing gradual prostatic involution without lowering circulating testosterone — libido, semen quality and fertility are preserved, which is why it is the medical option of choice for breeding dogs with BPH.",
        "mechanism_ja": "II型5α-還元酵素阻害薬。前立腺肥大を駆動するアンドロゲンであるジヒドロテストステロン（DHT）へのテストステロン変換を阻害し、血中テストステロンを下げずに前立腺を緩徐に退縮させる — 性欲・精液性状・繁殖能が温存されるため、繁殖犬のBPH内科治療の第一候補となる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Benign prostatic hyperplasia: 0.1-0.5 mg/kg PO q24h (practical: 5 mg/dog q24h for most dogs; Sirinarumitr 2001 — ~43% prostatic volume reduction at 16 weeks). Onset over several weeks; prostate re-enlarges after discontinuation, so treat long-term or until castration.",
                "dosage_ja": "良性前立腺肥大症: 0.1-0.5 mg/kg 経口 24時間毎（実用量: 多くの犬で5 mg/頭 24時間毎; Sirinarumitr 2001 — 16週で前立腺体積約43%減少）。効果発現は数週間かけて緩徐。中止後は再腫大するため、去勢しない限り長期継続。",
                "notes": "Castration remains the definitive treatment. Preserves semen quality/fertility (unlike castration or osaterone in some protocols) — suited to breeding sires. Rule out prostatitis, abscess and neoplasia before medical management.",
                "notes_ja": "根治治療は去勢。精液性状・繁殖能が温存されるため種雄犬に適する。内科管理の前に前立腺炎・膿瘍・腫瘍を除外すること。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not indicated — clinically significant BPH does not occur in cats.",
                "dosage_ja": "適応なし — 猫では臨床的に問題となる前立腺肥大は起こらない。",
                "notes": "No feline indication; do not extrapolate.",
                "notes_ja": "猫への適応はなく外挿しない。",
            },
        },
        "side_effects": "Well tolerated; occasional transient decrease in semen volume (quality preserved); rare lethargy",
        "side_effects_ja": "忍容性良好。時に精液量の一過性減少（性状は保たれる）。まれに元気低下",
        "contraindications": "Teratogenic — pregnant women must not handle crushed or broken tablets (absorbed transdermally; feminises male fetuses). Never administer to pregnant or breeding females. Not for cats",
        "contraindications_ja": "催奇形性 — 破損・粉砕した錠剤を妊娠中の飼い主が素手で扱わないこと（経皮吸収され雄胎子を女性化させる）。妊娠中・繁殖用の雌には絶対に投与しない。猫には使用しない",
        "drug_interactions": [
            {
                "drug": "Osaterone acetate / deslorelin",
                "effect": "Alternative medical options for BPH — use one modality at a time; no evidence for combining anti-androgen strategies",
                "effect_ja": "BPH内科治療の代替選択肢同士 — 併用せずいずれか単独で使用。抗アンドロゲン戦略の併用エビデンスはない",
                "severity": "info",
            },
        ],
    },
    {
        "id": "osaterone",
        "search_aliases": [
            "オサテロン",
            "酢酸オサテロン",
            "オサテロン酢酸エステル",
            "イポザン",
            "Osaterone",
            "Ypozane",
        ],
        "name": "Osaterone Acetate (Ypozane)",
        "name_ja": "酢酸オサテロン（イポザン）",
        "category": "reproductive",
        "mechanism": "Steroidal anti-androgen (progestogen derivative). Competitively blocks prostatic androgen receptors and inhibits testosterone uptake into the prostate, shrinking benign prostatic hyperplasia after a single 7-day oral course. The EU-registered veterinary treatment for canine BPH; clinical signs improve within 2 weeks and the effect persists for about 5-6 months per course.",
        "mechanism_ja": "ステロイド性抗アンドロゲン薬（プロゲストーゲン誘導体）。前立腺のアンドロゲン受容体を競合的に遮断し、前立腺へのテストステロン取り込みを阻害して、7日間の経口投与1コースで良性前立腺肥大を退縮させる。犬BPHに対するEU承認の動物用医薬品で、臨床症状は2週間以内に改善し、効果は1コースあたり約5-6ヶ月持続する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Benign prostatic hyperplasia: 0.25-0.5 mg/kg PO q24h for 7 days (single course). Clinical improvement within 2 weeks; repeat course when signs recur (typically ~5-6 months; Albouy 2008). Semen quality is preserved.",
                "dosage_ja": "良性前立腺肥大症: 0.25-0.5 mg/kg 経口 24時間毎 × 7日間（1コース）。2週間以内に臨床改善。症状再燃時に再投与（通常約5-6ヶ月後; Albouy 2008）。精液性状は温存される。",
                "notes": "Transiently attenuates the ACTH-stimulated cortisol response for several weeks (SPC) — use caution in dogs with adrenal disease or diabetes mellitus and interpret post-treatment ACTH stimulation tests carefully. Transient polyphagia possible. Rule out prostatic neoplasia/abscess first.",
                "notes_ja": "投与後数週間はACTH刺激コルチゾール反応が一過性に減弱（SPC）— 副腎疾患・糖尿病の犬では慎重に使用し、投与後のACTH刺激試験の解釈に注意。一過性の食欲亢進がありうる。前立腺腫瘍・膿瘍をまず除外すること。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not indicated — no feline BPH.",
                "dosage_ja": "適応なし — 猫にBPHは生じない。",
            },
        },
        "side_effects": "Transient polyphagia; transient behavioural change; mammary hyperplasia (rare); transient attenuation of adrenal cortisol response",
        "side_effects_ja": "一過性の食欲亢進・行動変化。まれに乳腺過形成。副腎コルチゾール反応の一過性減弱",
        "contraindications": "Caution in hepatic impairment (hepatic metabolism) and in dogs with adrenal insufficiency or diabetes mellitus; not for pregnant/breeding females; rule out prostatic carcinoma before use",
        "contraindications_ja": "肝機能障害では慎重投与（肝代謝）。副腎機能低下・糖尿病の犬では注意。妊娠・繁殖用の雌には使用しない。使用前に前立腺癌を除外",
        "drug_interactions": [
            {
                "drug": "ACTH stimulation testing / trilostane monitoring",
                "effect": "Attenuates ACTH-stimulated cortisol for several weeks after a course — schedule adrenal function tests accordingly",
                "effect_ja": "投与後数週間はACTH刺激コルチゾール値が低下 — 副腎機能検査のタイミングに配慮する",
                "severity": "moderate",
            },
            {
                "drug": "Finasteride / deslorelin",
                "effect": "Alternative medical options for BPH — use one modality at a time",
                "effect_ja": "BPH内科治療の代替選択肢同士 — 併用せずいずれか単独で使用",
                "severity": "info",
            },
        ],
    },
    {
        "id": "filgrastim",
        "search_aliases": [
            "フィルグラスチム",
            "G-CSF",
            "顆粒球コロニー刺激因子",
            "グラン",
            "ノイトロジン",
            "Filgrastim",
            "Neupogen",
        ],
        "name": "Filgrastim (rhG-CSF)",
        "name_ja": "フィルグラスチム（遺伝子組換えヒトG-CSF）",
        "category": "biologics",
        "mechanism": "Recombinant human granulocyte colony-stimulating factor. Stimulates proliferation, differentiation and marrow release of neutrophil precursors, raising circulating neutrophil counts within 24-72 h. Used for severe neutropenia (chemotherapy-induced, parvoviral, immune-mediated, toxic). Because it is a heterologous human protein, dogs and cats form neutralising antibodies after ~2-3 weeks of dosing that cross-react with endogenous G-CSF and can cause persistent neutropenia — courses must stay short.",
        "mechanism_ja": "遺伝子組換えヒト顆粒球コロニー刺激因子。好中球前駆細胞の増殖・分化・骨髄からの放出を刺激し、24-72時間で末梢好中球数を上昇させる。重度好中球減少症（化学療法性・パルボウイルス性・免疫介在性・中毒性）に用いる。ヒト由来の異種蛋白のため、犬猫では投与約2-3週間で中和抗体が形成され、内因性G-CSFと交差反応して遷延性好中球減少を起こしうる — 投与は短期間に限定すること。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Severe neutropenia (<1,000/µL): 5 µg/kg SC q24h until neutrophil recovery, typically 3-5 days (chemotherapy-induced) — do not exceed ~2 weeks (antibody formation). Parvoviral neutropenia: same dose; evidence for survival benefit is equivocal (Duffy 2010) — reserve for severe prolonged cytopenia.",
                "dosage_ja": "重度好中球減少（<1,000/µL）: 5 µg/kg 皮下 24時間毎、好中球回復まで（化学療法性では通常3-5日）— 抗体形成のため約2週間を超えないこと。パルボウイルス性好中球減少: 同用量。生存率改善のエビデンスは限定的（Duffy 2010）— 重度・遷延例に限って使用。",
                "notes": "Monitor CBC q24-48h and stop once neutrophils >3,000/µL. In chemotherapy patients, do not give within 24 h of cytotoxic dosing (stimulated precursors are chemosensitive).",
                "notes_ja": "CBCを24-48時間毎にモニタし、好中球>3,000/µLで中止。化学療法中は細胞傷害薬投与の前後24時間以内の投与を避ける（刺激された前駆細胞が薬剤感受性になる）。",
            },
            "cat": {
                "safe": True,
                "dosage": "Severe neutropenia (methimazole ADR, chemotherapy, immune-mediated): 5 µg/kg SC q24h until recovery; keep the course short (<2 weeks) — anti-rhG-CSF antibodies form in cats as in dogs.",
                "dosage_ja": "重度好中球減少（メチマゾール副反応・化学療法性・免疫介在性）: 5 µg/kg 皮下 24時間毎、回復まで。抗体形成は猫でも起こるため2週間未満の短期投与に留める。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Hyperestrogenism-associated pancytopenia (adjunct): 5 µg/kg SC q24h alongside definitive therapy (deslorelin implant or adrenal/ovarian source removal) and transfusion support.",
                "dosage_ja": "高エストロジェン血症性汎血球減少の補助: 5 µg/kg 皮下 24時間毎。根本治療（デスロレリンインプラント・原因摘出）と輸血支持療法に併用する。",
            },
        },
        "side_effects": "Bone pain (marrow expansion); injection-site reactions; splenomegaly with prolonged use; neutralising antibody formation → persistent neutropenia after prolonged courses",
        "side_effects_ja": "骨痛（骨髄拡大による）。注射部位反応。長期投与で脾腫。中和抗体形成 → 長期投与後の遷延性好中球減少",
        "contraindications": "Do not use beyond ~2 weeks (heterologous protein — antibody-mediated neutropenia). Not a substitute for antibiotics in febrile neutropenia. Avoid in myeloid leukemia (stimulates the malignant clone)",
        "contraindications_ja": "約2週間を超える投与は不可（異種蛋白 — 抗体介在性好中球減少）。発熱性好中球減少症では抗菌薬の代替にならない。骨髄性白血病では禁忌（腫瘍クローンを刺激）",
        "drug_interactions": [
            {
                "drug": "Cytotoxic chemotherapy",
                "effect": "Separate filgrastim from cytotoxic dosing by at least 24 h — G-CSF-stimulated precursors are more chemosensitive",
                "effect_ja": "細胞傷害性化学療法とは24時間以上あける — G-CSFで刺激された前駆細胞は薬剤感受性が高まる",
                "severity": "moderate",
            },
        ],
    },
]
