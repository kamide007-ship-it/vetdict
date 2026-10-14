"""Drug batch 74 – 2026-10 session: three licensed veterinary products that
were absent from the dictionary although the surgical/oncology content they
belong to was present.

1. Liposomal bupivacaine (NOCITA, Elanco) — extended-release (up to 72 h)
   local anaesthetic. FDA approval: dogs 2016 (single infiltration at
   incisional closure for cranial cruciate ligament surgery, 5.3 mg/kg =
   0.4 mL/kg) and cats 2018 (four-point peripheral nerve block before
   onychectomy, 5.3 mg/kg per forelimb). Off-label infiltration in other
   orthopaedic/soft-tissue wounds: Power et al. Vet Surg 2022 (incisional
   complications 19.7%, more after soft-tissue surgery).
2. Transdermal buprenorphine solution (ZORBIUM, Elanco) — single
   pre-operative dose to the dorsal cervical skin of cats provides ~4 days
   of post-operative analgesia. Label unit dose: 8 mg (0.4 mL) for cats
   1.2-3 kg, 20 mg (1 mL) for cats >3-7.5 kg, applied 1-2 h before surgery
   (Clark et al. J Vet Pharmacol Ther 2022 phase 3: success 81% vs 40%
   placebo; margin-of-safety study, same issue).
3. Verdinexor (LAVERDIA-CA1, Anivive) — oral selective inhibitor of nuclear
   export (XPO1) with FDA conditional approval (2021) for canine lymphoma.
   Phase II (Sadowski et al. BMC Vet Res 2018): ORR 37%, T-cell lymphoma
   71%; anorexia the commonest adverse event. Label: 1.25 mg/kg PO twice
   weekly (>= 72 h apart), increased to 1.5 mg/kg after 2 weeks if
   tolerated.

None is approved in Japan at the time of entry.
"""

DRUGS_BATCH_74 = [
    {
        "id": "bupivacaine_liposomal",
        "search_aliases": ["ノシタ", "Nocita", "NOCITA", "リポソーム化ブピバカイン", "リポソームブピバカイン"],
        "name": "Bupivacaine Liposome Injectable Suspension (Nocita)",
        "name_ja": "リポソーム化ブピバカイン（ノシタ）",
        "category": "anesthetics",
        "mechanism": "Amide local anaesthetic (sodium-channel blockade) encapsulated in multivesicular liposomes that release bupivacaine gradually at the injection site — local analgesia for up to 72 hours from a single administration.",
        "mechanism_ja": "アミド型局所麻酔薬（Naチャネル遮断）を多胞性リポソームに封入し、投与部位で緩徐に放出する徐放製剤。単回投与で最長72時間の局所鎮痛。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5.3 mg/kg (0.4 mL/kg of 13.3 mg/mL) as a single infiltration injection into the tissue layers at the time of incisional closure (label: cranial cruciate ligament surgery). The volume may be expanded with an equal volume of sterile saline or LRS for large incisions. Dogs >= 5 months of age (NOCITA US label, FDA 2016).",
                "dosage_ja": "5.3 mg/kg（13.3 mg/mL製剤 0.4 mL/kg）を閉創時に組織層へ単回浸潤投与（ラベル適応: 前十字靭帯断裂の手術）。大きな切開では等量の生理食塩水または乳酸リンゲル液で容量を増やしてよい。5ヶ月齢以上（NOCITA 米国ラベル、FDA 2016年）。",
                "notes": "Infiltrate with a moving-needle technique into every tissue layer — analgesia only reaches tissue the suspension contacts. Do not give within the same session as other amide local anaesthetics (lidocaine can trigger immediate bupivacaine release from the liposomes). Not for intravenous, intra-arterial, intra-articular, epidural or intrathecal use. Off-label infiltration of other orthopaedic and soft-tissue wounds is reported (Power 2022 Vet Surg: short-term incisional complications 19.7%, more after soft-tissue than orthopaedic surgery). Part of a multimodal plan — continue NSAIDs/opioids as indicated. Not approved in Japan.",
                "notes_ja": "針を進めながら全ての組織層へ浸潤させる（懸濁液が接した組織にしか鎮痛は及ばない）。同一処置内で他のアミド型局所麻酔薬と併用しない（リドカインはリポソームからのブピバカインの即時放出を誘発しうる）。静脈内・動脈内・関節内・硬膜外・脊髄くも膜下には投与しない。他の整形外科・軟部組織手術創への適応外浸潤の報告あり（Power 2022 Vet Surg: 短期の創部合併症19.7%、軟部組織手術でより多い）。多角的鎮痛の一部として使用し、NSAIDs・オピオイドは適応に応じて継続。国内未承認。",
            },
            "cat": {
                "safe": True,
                "dosage": "5.3 mg/kg per forelimb (0.4 mL/kg per forelimb; total 10.6 mg/kg) as a four-point peripheral nerve block (superficial branches of the radial nerve and the median, ulnar and dorsal/palmar branches) before onychectomy. Cats >= 5 months of age (NOCITA US label, FDA 2018).",
                "dosage_ja": "前肢1本あたり5.3 mg/kg（前肢1本あたり0.4 mL/kg、総量10.6 mg/kg）を、抜爪術前の4点末梢神経ブロック（橈骨神経浅枝・正中神経・尺骨神経背側/掌側枝）として投与。5ヶ月齢以上（NOCITA 米国ラベル、FDA 2018年）。",
                "notes": "Labelled only for the four-point forelimb block; other feline uses are off-label. Aspirate before each injection to avoid intravascular placement. Same mixing and route restrictions as in dogs. Not approved in Japan.",
                "notes_ja": "ラベル上は前肢4点ブロックのみ。その他の猫での使用は適応外。各注入前に吸引し血管内投与を避ける。混合・投与経路の制限は犬と同じ。国内未承認。",
            },
        },
        "contraindications": "Intravenous, intra-arterial, intra-articular, epidural or intrathecal administration. Patients < 5 months. Known amide local anaesthetic hypersensitivity. Concurrent administration with other amide local anaesthetics (a safe interval has not been established).",
        "contraindications_ja": "静脈内・動脈内・関節内・硬膜外・脊髄くも膜下投与。5ヶ月齢未満。アミド型局所麻酔薬への過敏症。他のアミド型局所麻酔薬との併用（安全な投与間隔は未確立）。",
        "side_effects": [
            "Incisional complications (swelling, seroma, discharge) — mostly self-limiting",
            "Local anaesthetic systemic toxicity if injected intravascularly (CNS signs, arrhythmias)",
        ],
        "side_effects_ja": [
            "創部合併症（腫脹・漿液腫・滲出） — 多くは自然消退",
            "血管内誤投与時の局所麻酔薬中毒（中枢神経症状・不整脈）",
        ],
        "drug_interactions": [
            {
                "drug": "Lidocaine / other amide local anaesthetics",
                "effect": "May cause immediate release of bupivacaine from the liposomes and additive systemic toxicity — do not co-administer in the same procedure.",
                "effect_ja": "リポソームからのブピバカイン即時放出と全身毒性の相加を起こしうる — 同一処置内で併用しない。",
                "severity": "major",
            },
            {
                "drug": "Bupivacaine HCl (plain)",
                "effect": "Additive total bupivacaine exposure; dose plain bupivacaine separately and account for the cumulative dose.",
                "effect_ja": "ブピバカイン総曝露量の相加 — 通常製剤を併用する場合は累積量を計算する。",
                "severity": "moderate",
            },
        ],
        "references": [
            "NOCITA (bupivacaine liposome injectable suspension) US label, Elanco — FDA NADA 141-461 (dogs 2016; cats 2018)",
            "Power AM et al. Incidence and severity of short-term incisional complications after intraoperative local infiltration of liposomal bupivacaine in dogs. Vet Surg 2022;51:674-681. doi:10.1111/vsu.13803",
        ],
    },
    {
        "id": "buprenorphine_transdermal",
        "search_aliases": ["ゾルビウム", "Zorbium", "ZORBIUM", "経皮ブプレノルフィン", "ブプレノルフィン経皮"],
        "name": "Buprenorphine Transdermal Solution (Zorbium)",
        "name_ja": "ブプレノルフィン経皮溶液（ゾルビウム）",
        "category": "analgesics",
        "mechanism": "Partial mu-opioid agonist formulated as a 20 mg/mL transdermal solution with a permeation enhancer; a single topical dose forms a skin depot that maintains analgesic plasma concentrations for about 4 days in cats.",
        "mechanism_ja": "μオピオイド受容体部分作動薬を浸透促進剤含有の20 mg/mL経皮溶液としたもの。単回塗布で皮膚内にデポを形成し、猫で約4日間鎮痛血中濃度を維持する。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Single unit dose applied to the unclipped dorsal cervical skin 1-2 h before surgery: 8 mg (0.4 mL) for cats 1.2-3 kg; 20 mg (1 mL) for cats >3-7.5 kg (2.7-6.7 mg/kg). Provides up to 4 days of post-operative analgesia; do not re-apply on the label (ZORBIUM US label; Clark 2022 J Vet Pharmacol Ther — treatment success 81% vs 40% placebo).",
                "dosage_ja": "手術1-2時間前に、毛刈りしない頸背部皮膚へ単位用量を1回塗布: 1.2-3 kgの猫は8 mg（0.4 mL）、3 kg超-7.5 kgの猫は20 mg（1 mL）（2.7-6.7 mg/kg相当）。術後最長4日間の鎮痛。ラベル上は再塗布しない（ZORBIUM 米国ラベル、Clark 2022 J Vet Pharmacol Ther — 治療成功率81% 対 プラセボ40%）。",
                "notes": "Opioid class effects in cats: hyperthermia (mean +0.35 °C in the pivotal study — monitor temperature post-operatively), mydriasis, euphoria/sedation. Prevent licking of the site and contact with other pets/people until dry; wear gloves — human exposure can cause opioid effects (controlled substance). Simbadol (injectable, 0.24 mg/kg SC q24h up to 3 days) and OTM buprenorphine are alternatives. Not for cats < 1.2 kg or > 7.5 kg (no unit dose). Not approved in Japan.",
                "notes_ja": "猫のオピオイド共通作用: 高体温（ピボタル試験で平均+0.35 °C — 術後に体温を監視）・散瞳・多幸/鎮静。乾燥するまで塗布部位の舐め・他の動物や人との接触を防ぐ。手袋を着用（人の曝露でオピオイド作用 — 規制薬物）。代替はシンバドール（注射 0.24 mg/kg SC q24h 最長3日）や口腔粘膜投与ブプレノルフィン。1.2 kg未満・7.5 kg超の猫には単位用量がない。国内未承認。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not licensed for dogs — no canine dose established.",
                "dosage_ja": "犬には未承認 — 犬の用量は確立していない。",
                "notes": "Use injectable buprenorphine or full mu agonists in dogs.",
                "notes_ja": "犬では注射用ブプレノルフィンや完全μ作動薬を用いる。",
            },
        },
        "contraindications": "Cats < 1.2 kg or > 7.5 kg, or < 4 months of age (label). Concurrent use of other opioids without dose consideration. Application to broken or diseased skin.",
        "contraindications_ja": "1.2 kg未満・7.5 kg超、4ヶ月齢未満の猫（ラベル）。用量配慮なしの他のオピオイドとの併用。損傷・病変のある皮膚への塗布。",
        "side_effects": [
            "Hyperthermia (opioid-associated, cats)",
            "Mydriasis, euphoria or sedation",
            "Transient constipation",
        ],
        "side_effects_ja": [
            "高体温（猫のオピオイド関連）",
            "散瞳・多幸または鎮静",
            "一過性の便秘",
        ],
        "drug_interactions": [
            {
                "drug": "Full mu-opioid agonists (methadone, hydromorphone, fentanyl)",
                "effect": "Buprenorphine's high receptor affinity can blunt rescue full agonists for the duration of the depot — plan escalation (higher full-agonist doses, multimodal adjuncts).",
                "effect_ja": "ブプレノルフィンの高い受容体親和性により、デポ持続中は完全作動薬のレスキュー効果が減弱しうる — 増量や多角的鎮痛を計画する。",
                "severity": "moderate",
            },
            {
                "drug": "Sedatives / CNS depressants",
                "effect": "Additive sedation and respiratory depression.",
                "effect_ja": "鎮静・呼吸抑制の相加。",
                "severity": "moderate",
            },
        ],
        "references": [
            "ZORBIUM (buprenorphine transdermal solution) US label, Elanco — FDA NADA 141-547",
            "Clark TP et al. Multicentered masked placebo-controlled phase 3 clinical study of an extended duration transdermal buprenorphine solution for post-operative pain in cats. J Vet Pharmacol Ther 2022;45 Suppl 1:S52-S66. doi:10.1111/jvp.13060",
            "Clark TP et al. Margin of safety of extended-duration transdermal buprenorphine solution following multiple-dose administrations to cats. J Vet Pharmacol Ther 2022;45 Suppl 1:S67-S84. doi:10.1111/jvp.13051",
        ],
    },
    {
        "id": "verdinexor",
        "search_aliases": ["ラバーディア", "Laverdia", "LAVERDIA", "Laverdia-CA1", "KPT-335", "ベルジネクソル"],
        "name": "Verdinexor (Laverdia-CA1)",
        "name_ja": "ベルジネクソル（ラバーディア）",
        "category": "antineoplastics",
        "mechanism": "Oral selective inhibitor of nuclear export (SINE): blocks exportin-1 (XPO1/CRM1), trapping tumour-suppressor and growth-regulatory proteins in the nucleus and inducing apoptosis of lymphoma cells.",
        "mechanism_ja": "経口の選択的核外輸送阻害薬（SINE）。エクスポーチン1（XPO1/CRM1）を阻害し、腫瘍抑制・増殖制御タンパクを核内に留めてリンパ腫細胞のアポトーシスを誘導する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1.25 mg/kg PO twice weekly (e.g. Monday/Thursday, at least 72 h apart) with food; if tolerated after 2 weeks, increase to 1.5 mg/kg twice weekly (LAVERDIA-CA1 US label, FDA conditional approval 2021). Phase II: objective response rate 37%, 71% in T-cell lymphoma (Sadowski 2018 BMC Vet Res).",
                "dosage_ja": "1.25 mg/kg PO 週2回（例: 月・木曜、間隔72時間以上）、食事と共に投与。2週間忍容できれば1.5 mg/kg 週2回に増量（LAVERDIA-CA1 米国ラベル、FDA条件付き承認2021年）。第II相試験: 客観的奏効率37%、T細胞性リンパ腫で71%（Sadowski 2018 BMC Vet Res）。",
                "notes": "Conditional approval — efficacy is at the 'reasonable expectation' stage; a single-agent option for dogs whose owners decline or cannot pursue multi-agent chemotherapy, not a replacement for CHOP when cure-intent remission is sought. Anorexia, weight loss, vomiting and diarrhoea are the commonest adverse events — weigh weekly, use anti-emetics/appetite stimulants and dose holidays; prednisone was used to manage anorexia in the phase II study. Monitor CBC and liver enzymes. Cytotoxic-handling precautions; pregnant people should not handle tablets or wastes. Not approved in Japan.",
                "notes_ja": "条件付き承認 — 有効性は「合理的期待」段階。多剤併用化学療法を選択しない・できない飼い主向けの単剤選択肢であり、寛解を目指すCHOPの代替ではない。最多の副作用は食欲不振・体重減少・嘔吐・下痢 — 毎週体重を測定し、制吐薬・食欲増進剤・休薬で管理（第II相試験では食欲不振にプレドニゾンが用いられた）。CBC・肝酵素を監視。抗がん剤の取扱い注意 — 妊娠中の人は錠剤や排泄物を扱わない。国内未承認。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not licensed for cats — no feline dose established.",
                "dosage_ja": "猫には未承認 — 猫の用量は確立していない。",
                "notes": "Feline lymphoma: COP/CHOP or chlorambucil-prednisolone protocols.",
                "notes_ja": "猫のリンパ腫はCOP/CHOP、またはクロラムブシル＋プレドニゾロン療法。",
            },
        },
        "contraindications": "Pregnant, lactating or breeding dogs; dogs with significant hepatic dysfunction or uncontrolled concurrent illness. Do not split or crush tablets.",
        "contraindications_ja": "妊娠・授乳・繁殖予定の犬。重度の肝機能障害やコントロール不良の併発疾患がある犬。錠剤を分割・粉砕しない。",
        "side_effects": [
            "Anorexia and weight loss (most common)",
            "Vomiting, diarrhoea",
            "Lethargy; elevated liver enzymes",
        ],
        "side_effects_ja": [
            "食欲不振・体重減少（最多）",
            "嘔吐・下痢",
            "嗜眠・肝酵素上昇",
        ],
        "drug_interactions": [
            {
                "drug": "Other myelosuppressive/cytotoxic chemotherapy",
                "effect": "Combination not evaluated on the label — specialist-supervised use only.",
                "effect_ja": "ラベル上併用は未評価 — 腫瘍科専門医の管理下に限る。",
                "severity": "moderate",
            },
        ],
        "references": [
            "LAVERDIA-CA1 (verdinexor tablets) US label, Anivive Lifesciences — FDA conditional approval CA1-022 (2021)",
            "Sadowski AR et al. Phase II study of the oral selective inhibitor of nuclear export (SINE) KPT-335 (verdinexor) in dogs with lymphoma. BMC Vet Res 2018;14:250. doi:10.1186/s12917-018-1587-9",
        ],
    },
]
