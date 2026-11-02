"""Drug batch 91 – 2026-11 第83弾.

Two referenced-but-absent drugs found by the dose-context sweep: the
disease content names them with explicit mg/kg doses, but the dictionary had
no monograph, so the treatment chip, reverse lookup and interaction checker
could not resolve them.

* Metoprolol tartrate — beta-1 selective blocker named in the canine/feline
  supraventricular-tachyarrhythmia and hypertrophic-cardiomyopathy rate-control
  protocols ("atenolol 0.5-1 mg/kg ..., metoprolol 0.1-0.5 mg/kg PO q12h").
* Clonazepam — benzodiazepine named for distemper-associated myoclonus
  ("clonazepam 0.5 mg/kg PO q8h — limited efficacy") and as an adjunct
  anticonvulsant / anxiolytic.

Evidence: Budde JA, McCluskey DM, eds. Plumb's Veterinary Drug Handbook,
10th ed. 2023; Ettinger SJ, Feldman EC, Côté E. Textbook of Veterinary
Internal Medicine, 9th ed.; Côté E et al. Feline Cardiology 2011;
Podell M et al. 2015 ACVIM Small Animal Consensus Statement on Seizure
Management in Dogs. J Vet Intern Med 2016;30:477-490; Center SA et al.
Fulminant hepatic failure associated with oral administration of diazepam
in 11 cats. J Am Vet Med Assoc 1996;209:618-625.
"""

DRUGS_BATCH_91 = [
    {
        "id": "metoprolol",
        "search_aliases": [
            "メトプロロール",
            "酒石酸メトプロロール",
            "セロケン",
            "ロプレソール",
            "Lopressor",
            "Seloken",
            "metoprolol tartrate",
        ],
        "name": "Metoprolol Tartrate",
        "name_ja": "メトプロロール酒石酸塩",
        "category": "cardiovascular",
        "mechanism": "Beta-1 selective adrenergic blocker: slows sinus rate and AV-nodal conduction and reduces myocardial oxygen demand. Hepatically metabolised (unlike atenolol, which is renally excreted), so it is an alternative for rate control in animals with renal insufficiency.",
        "mechanism_ja": "β1選択的アドレナリン受容体遮断薬: 洞調律と房室結節伝導を遅くし心筋酸素需要を下げる。肝代謝（腎排泄のアテノロールと異なる）のため、腎機能低下例の心拍数コントロールの代替となる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.2-1 mg/kg PO q8-12h (supraventricular tachyarrhythmias, rate control, adjunct for hyperthyroid/pheochromocytoma tachycardia after alpha-blockade). Start at the low end and titrate to heart rate over 1-2 weeks.",
                "dosage_ja": "0.2〜1 mg/kg PO q8〜12h（上室性頻拍性不整脈の心拍数コントロール、甲状腺機能亢進症の頻脈、褐色細胞腫ではα遮断後の補助）。低用量から開始し1〜2週かけて心拍数を指標に漸増する。",
                "notes": "Do not start during decompensated congestive heart failure. Taper over 1-2 weeks when stopping (abrupt withdrawal can cause rebound tachycardia).",
                "notes_ja": "非代償性のうっ血性心不全の最中には開始しない。中止時は1〜2週かけて漸減する（急な中止で反跳性頻脈）。",
            },
            "cat": {
                "safe": True,
                "dosage": "2-15 mg/cat PO q8-12h (start low, e.g. 2-5 mg/cat q12h); rate control in hypertrophic cardiomyopathy with LVOT obstruction or tachyarrhythmia, and hyperthyroid tachycardia while awaiting euthyroidism.",
                "dosage_ja": "2〜15 mg/頭 PO q8〜12h（低用量 2〜5 mg/頭 q12h から開始）。左室流出路閉塞や頻拍性不整脈を伴う肥大型心筋症の心拍数コントロール、甲状腺機能亢進症の正常化までの頻脈管理。",
                "notes": "Atenolol is more commonly used in cats; metoprolol is an option when renal excretion is a concern. Avoid in cats with congestive heart failure that is not yet controlled.",
                "notes_ja": "猫ではアテノロールが一般的。腎排泄が問題になる場合の選択肢。うっ血性心不全が未コントロールの猫には使わない。",
            },
        },
        "contraindications": "Sinus bradycardia, second/third-degree AV block, sick sinus syndrome, decompensated congestive heart failure, cardiogenic shock. Use cautiously in bronchospastic disease (feline asthma) and diabetes mellitus (masks hypoglycaemia).",
        "contraindications_ja": "洞徐脈、第2〜3度房室ブロック、洞不全症候群、非代償性うっ血性心不全、心原性ショック。気管支攣縮性疾患（猫喘息）と糖尿病（低血糖の徴候を隠す）では慎重に使用する。",
        "side_effects": [
            "Bradycardia",
            "Lethargy",
            "Hypotension",
            "Worsening heart failure",
            "Bronchospasm (high doses)",
        ],
        "side_effects_ja": ["徐脈", "元気消失", "低血圧", "心不全の悪化", "気管支攣縮（高用量）"],
        "drug_interactions": [
            {
                "drug": "Diltiazem",
                "effect": "Additive negative chronotropy/dromotropy — profound bradycardia or AV block.",
                "effect_ja": "陰性変時・変伝導作用の相加 — 高度な徐脈・房室ブロック。",
                "severity": "major",
            },
            {
                "drug": "Verapamil",
                "effect": "Additive AV-nodal block and myocardial depression.",
                "effect_ja": "房室結節遮断と心筋抑制の相加。",
                "severity": "major",
            },
            {
                "drug": "Atenolol",
                "effect": "Duplicate beta-blockade — use one beta-blocker only.",
                "effect_ja": "β遮断の重複 — β遮断薬はどちらか一方のみ。",
                "severity": "major",
            },
            {
                "drug": "Insulin",
                "effect": "Beta-blockade masks tachycardia/tremor of hypoglycaemia.",
                "effect_ja": "β遮断が低血糖時の頻脈・振戦を隠す。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Budde JA, McCluskey DM, eds. Plumb's Veterinary Drug Handbook. 10th ed. Wiley-Blackwell; 2023.",
            "Côté E, MacDonald KA, Meurs KM, Sleeper MM. Feline Cardiology. Wiley-Blackwell; 2011.",
            "Ettinger SJ, Feldman EC, Côté E. Textbook of Veterinary Internal Medicine. 9th ed. Elsevier.",
        ],
    },
    {
        "id": "clonazepam",
        "search_aliases": ["クロナゼパム", "リボトリール", "ランドセン", "Klonopin", "Rivotril"],
        "name": "Clonazepam",
        "name_ja": "クロナゼパム",
        "category": "neurological",
        "mechanism": "Long-acting benzodiazepine: positive allosteric modulator of the GABA-A receptor (anticonvulsant, myorelaxant, anxiolytic). Tolerance to the anticonvulsant effect develops within weeks, so it is an adjunct, not a maintenance antiepileptic.",
        "mechanism_ja": "長時間作用型ベンゾジアゼピン: GABA-A受容体の正のアロステリック調節薬（抗痙攣・筋弛緩・抗不安）。抗痙攣作用には数週間で耐性ができるため、維持の抗てんかん薬ではなく補助として使う。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Adjunct for myoclonus (e.g. distemper-associated) or seizures: 0.5 mg/kg PO q8-12h (efficacy for distemper myoclonus is limited). Situational anxiety/panic: 0.1-0.5 mg/kg PO q8-12h, given 1-2 hours before the trigger.",
                "dosage_ja": "ミオクローヌス（ジステンパー後遺症など）・発作の補助: 0.5 mg/kg PO q8〜12h（ジステンパーのミオクローヌスへの効果は限定的）。状況性の不安・パニック: 0.1〜0.5 mg/kg PO q8〜12h、誘因の1〜2時間前に投与。",
                "notes": "Tolerance and physical dependence develop — taper over weeks after long-term use (abrupt withdrawal can precipitate seizures). Not a substitute for phenobarbital/levetiracetam maintenance (ACVIM 2015 consensus). Paradoxical excitation is possible.",
                "notes_ja": "耐性と身体依存が生じる — 長期使用後は数週間かけて漸減する（急な中止で発作を誘発しうる）。フェノバルビタール・レベチラセタムによる維持療法の代わりにはならない（ACVIM 2015）。奇異性興奮がありうる。",
            },
            "cat": {
                "safe": False,
                "dosage": "No validated feline dose — avoid oral benzodiazepines for routine use: idiosyncratic fulminant hepatic necrosis has been reported after oral diazepam in cats (Center 1996). Use phenobarbital/levetiracetam for seizures and gabapentin for situational anxiety.",
                "dosage_ja": "猫で検証された用量はなく、経口ベンゾジアゼピンの常用は避ける（猫で経口ジアゼパム後の特異体質性の劇症肝壊死の報告 — Center 1996）。発作にはフェノバルビタール・レベチラセタム、状況性不安にはガバペンチンを用いる。",
                "notes": "If any oral benzodiazepine is used in a cat, check liver enzymes within the first week.",
                "notes_ja": "猫に経口ベンゾジアゼピンを使う場合は、投与開始後1週間以内に肝酵素を確認する。",
            },
        },
        "contraindications": "Severe hepatic disease, acute narrow-angle glaucoma, respiratory depression. Controlled substance (Japan: psychotropic schedule III).",
        "contraindications_ja": "重度の肝疾患、急性閉塞隅角緑内障、呼吸抑制。規制薬（日本: 第三種向精神薬）。",
        "side_effects": ["Sedation", "Ataxia", "Polyphagia", "Paradoxical excitation", "Tolerance and dependence"],
        "side_effects_ja": ["鎮静", "運動失調", "多食", "奇異性興奮", "耐性・依存"],
        "drug_interactions": [
            {
                "drug": "Phenobarbital",
                "effect": "Additive CNS depression; phenobarbital induces clonazepam metabolism (shorter effect).",
                "effect_ja": "中枢抑制の相加。フェノバルビタールはクロナゼパムの代謝を誘導する（作用短縮）。",
                "severity": "moderate",
            },
            {
                "drug": "Opioids",
                "effect": "Additive sedation and respiratory depression.",
                "effect_ja": "鎮静・呼吸抑制の相加。",
                "severity": "moderate",
            },
            {
                "drug": "Ketoconazole",
                "effect": "CYP3A inhibition raises clonazepam levels.",
                "effect_ja": "CYP3A阻害で血中濃度が上昇する。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Budde JA, McCluskey DM, eds. Plumb's Veterinary Drug Handbook. 10th ed. Wiley-Blackwell; 2023.",
            "Podell M, Volk HA, Berendt M, et al. 2015 ACVIM Small Animal Consensus Statement on Seizure Management in Dogs. J Vet Intern Med 2016;30:477-490.",
            "Center SA, Elston TH, Rowland PH, et al. Fulminant hepatic failure associated with oral administration of diazepam in 11 cats. J Am Vet Med Assoc 1996;209:618-625.",
        ],
    },
]
