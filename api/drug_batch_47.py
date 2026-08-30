"""Drug batch 47 – referenced-but-absent agents surfaced by the 2026-08 audit (16th sweep).

The dose-context katakana token audit (treatment texts cross-checked against
find_drugs_in_text) found three agents that VetDict's own disease content
instructs clinicians to use — with explicit doses — yet were absent from the
formulary:

  - オクトレオチド (octreotide, Sandostatin): the canine gastrinoma entry
    prescribes "1-5 μg/kg SC q8-12h", the insulinoma entry lists
    "10-50 mcg SC q8-12h" and the idiopathic chylothorax entry cites
    "10 μg/kg SC q8h" — 8+ references, no somatostatin analogue existed.
  - デコキネート (decoquinate, Deccox): the Hepatozoon americanum entries
    prescribe the ACVIM-standard relapse-suppression phase "10-20 mg/kg PO
    q12h long-term after 14 days of TCP" — the drug that defines American
    canine hepatozoonosis maintenance therapy was absent.
  - ビオチン (biotin): 21 references — the equine hoof-quality supplement
    ("15-25 mg/日 PO、6-12ヶ月" across hoof wall crack, sand crack, coronary
    band dystrophy entries) and the canine dermatology adjunct — absent.

References:
  - Altschul M et al. J Small Anim Pract 1997 / Hughes SM, N Z Vet J 2006 —
    canine gastrinoma: octreotide 1-5 μg/kg SC q8-12h suppresses gastrin
    secretion and clinical signs.
  - Robben JH et al. J Vet Intern Med 2006 — somatostatin-receptor imaging /
    octreotide response in canine insulinoma is variable (receptor-subtype
    dependent); hypoglycemia palliation inconsistent.
  - Fossum TW (chylothorax reviews); Sicard GK, JAVMA 2005 — octreotide
    10 μg/kg SC q8h reduced chyle flow in some canine chylothorax cases
    (evidence limited).
  - Peterson ME — feline acromegaly: short-acting octreotide is largely
    ineffective in cats (somatostatin-receptor profile); long-acting
    analogues/hypophysectomy preferred.
  - Macintire DK et al. JAVMA 2001;218:77 — Hepatozoon americanum: TCP
    (trimethoprim-sulfa + clindamycin + pyrimethamine) ×14 days, then
    decoquinate 10-20 mg/kg PO q12h in food ≥2 years prevents relapse and
    markedly prolongs survival.
  - Allen KE et al. Vet Parasitol 2011 — hepatozoonosis review confirming
    decoquinate maintenance.
  - Josseck H et al. Equine Vet J 1995;27:175 — biotin 20 mg/day PO improved
    hoof horn quality in Lipizzaners over 9-19 months (placebo-controlled).
  - Zenker W et al. Equine Vet J 1995;27:183 — histological confirmation of
    biotin effect on hoof horn.
  - Frigg M et al. Schweiz Arch Tierheilkd 1989 — biotin in dogs with fur
    and skin conditions (adjunct-level evidence).
"""

DRUGS_BATCH_47: list[dict] = [
    {
        "id": "octreotide",
        "search_aliases": [
            "オクトレオチド",
            "サンドスタチン",
            "Octreotide",
            "Sandostatin",
        ],
        "name": "Octreotide (Sandostatin)",
        "name_ja": "オクトレオチド（サンドスタチン）",
        "category": "endocrine",
        "mechanism": "Synthetic somatostatin analogue that binds somatostatin receptors (predominantly SSTR2/5) and suppresses secretion of gastrin, insulin, glucagon and growth hormone, and reduces splanchnic/lymphatic flow. Veterinary uses: gastrinoma (best-supported), insulinoma palliation (variable, receptor-dependent), and adjunctive reduction of chyle flow in chylothorax.",
        "mechanism_ja": "ソマトスタチン受容体（主にSSTR2/5）に結合し、ガストリン・インスリン・グルカゴン・成長ホルモンの分泌を抑制、内臓血流・リンパ流も減少させる合成ソマトスタチンアナログ。獣医領域ではガストリノーマ（最もエビデンスが確立）、インスリノーマの緩和（受容体依存性で反応不定）、乳糜胸のリンパ流量減少補助に用いる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Gastrinoma: 1-5 μg/kg SC q8-12h (with PPI; long-acting depot 10-20 mg IM q4wk for chronic control). Insulinoma (unresectable, refractory): 10-50 μg/dog SC q8-12h — response is variable and receptor-dependent (Robben 2006). Chylothorax adjunct: 10 μg/kg SC q8h ×2-3 weeks (evidence limited).",
                "dosage_ja": "ガストリノーマ: 1-5 μg/kg 皮下 8-12時間毎（PPI併用。慢性管理は長時間作用デポ 10-20 mg 筋注 4週毎）。インスリノーマ（切除不能・難治例）: 10-50 μg/頭 皮下 8-12時間毎 — 反応は受容体サブタイプ依存で不定（Robben 2006）。乳糜胸補助: 10 μg/kg 皮下 8時間毎×2-3週（エビデンス限定的）。",
                "notes": "Monitor glucose when used for insulinoma — paradoxical worsening of hypoglycemia is possible if glucagon suppression outweighs insulin suppression. GI signs (inappetence, diarrhea) are the main adverse effects. Expensive; reserve for refractory/palliative cases.",
                "notes_ja": "インスリノーマで使用する際は血糖を必ずモニタリング — グルカゴン抑制がインスリン抑制を上回ると逆説的な低血糖悪化がありうる。主な副作用は消化器症状（食欲低下・下痢）。高価なため難治例・緩和目的に温存。",
            },
            "cat": {
                "safe": True,
                "dosage": "Acromegaly: short-acting octreotide is largely INEFFECTIVE in cats (receptor profile — Peterson); hypophysectomy/radiation preferred. Gastrinoma (rare): extrapolated 1-5 μg/kg SC q8-12h.",
                "dosage_ja": "先端巨大症: 短時間作用型オクトレオチドは猫ではほぼ無効（受容体プロファイル — Peterson）。下垂体切除/放射線が優先。ガストリノーマ（稀）: 外挿で 1-5 μg/kg 皮下 8-12時間毎。",
                "notes": "Do not present octreotide as an acromegaly treatment option in cats — trial only when definitive options are unavailable, with IGF-1 monitoring.",
                "notes_ja": "猫の先端巨大症の治療選択肢としては提示しないこと — 根治的選択肢が使えない場合の試験的投与に限り、IGF-1をモニタリング。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Insulinoma (refractory to prednisolone + diazoxide): 1-2 μg/kg SC q8-12h reported (case-level evidence).",
                "dosage_ja": "インスリノーマ（プレドニゾロン＋ジアゾキシド不応例）: 1-2 μg/kg 皮下 8-12時間毎の報告あり（症例報告レベル）。",
                "notes": "Third-line only; frequent small meals, prednisolone and diazoxide remain the medical backbone.",
                "notes_ja": "第三選択に限る。頻回少量給餌・プレドニゾロン・ジアゾキシドが内科管理の基本であることは不変。",
            },
        },
        "side_effects": "GI signs (inappetence, vomiting, diarrhea), injection-site pain, altered glucose regulation (hypo- or hyperglycemia), rarely biliary sludge with chronic use",
        "side_effects_ja": "消化器症状（食欲低下・嘔吐・下痢）、注射部位痛、血糖調節の変動（低血糖・高血糖の両方向）、慢性投与でまれに胆泥",
        "contraindications": "Monitor glucose closely in insulinoma — paradoxical hypoglycemia possible. Reduce expectations in cats (acromegaly) — largely ineffective",
        "contraindications_ja": "インスリノーマでは血糖を厳密にモニタリング — 逆説的低血糖がありうる。猫の先端巨大症にはほぼ無効であることを前提とする",
        "drug_interactions": [
            {
                "drug": "Insulin / oral hypoglycemics / diazoxide",
                "effect": "Octreotide alters insulin and glucagon secretion — glucose-regulating co-medication requires dose re-titration under monitoring",
                "effect_ja": "オクトレオチドはインスリン・グルカゴン分泌の両方を変動させる — 血糖調節薬の併用は監視下での再滴定が必要",
                "severity": "moderate",
            },
            {
                "drug": "Cyclosporine",
                "effect": "Octreotide reduces cyclosporine absorption (human data) — monitor levels",
                "effect_ja": "オクトレオチドはシクロスポリンの吸収を低下させる（ヒトデータ）— 血中濃度をモニタリング",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "decoquinate",
        "search_aliases": [
            "デコキネート",
            "デコックス",
            "Decoquinate",
            "Deccox",
        ],
        "name": "Decoquinate (Deccox)",
        "name_ja": "デコキネート（デコックス）",
        "category": "antiparasitics",
        "mechanism": "Quinolone coccidiostat that blocks protozoal mitochondrial electron transport (cytochrome b), arresting sporozoite/merozoite development. In dogs it is the ACVIM-standard long-term suppression phase for Hepatozoon americanum: it does not clear tissue cysts but prevents merozoite release and relapse after triple therapy (TCP).",
        "mechanism_ja": "原虫ミトコンドリア電子伝達系（チトクロムb）を阻害しスポロゾイト・メロゾイトの発育を停止させるキノロン系コクシジウム抑制薬。犬ではHepatozoon americanum（アメリカ型ヘパトゾーン症）のACVIM標準・長期再発抑制フェーズを担う: 組織シストは排除しないが、TCP三剤併用後のメロゾイト放出と再発を抑止する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Hepatozoon americanum: after 14 days of TCP (trimethoprim-sulfa + clindamycin + pyrimethamine), decoquinate 10-20 mg/kg PO q12h mixed in food, continued ≥2 years (Macintire 2001 JAVMA — relapse prevention and markedly prolonged survival).",
                "dosage_ja": "アメリカ型ヘパトゾーン症: TCP三剤併用（TMS＋クリンダマイシン＋ピリメタミン）14日間の後、デコキネート 10-20 mg/kg 経口 12時間毎（餌に混和）を2年以上継続（Macintire 2001 JAVMA — 再発抑止と生存期間の大幅延長）。",
                "notes": "Wide safety margin (livestock feed-additive origin). Discontinuation before 2 years commonly leads to relapse — owner compliance counseling is part of the protocol. Combine with year-round tick control (Amblyomma maculatum).",
                "notes_ja": "安全域は広い（家畜飼料添加物由来）。2年未満での中止は高率に再発する — 飼い主のコンプライアンス指導もプロトコルの一部。通年のマダニ対策（Amblyomma maculatum）を併用。",
            },
            "cat": {
                "safe": True,
                "dosage": "Hepatozoon felis (extrapolated): 10-20 mg/kg PO q12h in food as a relapse-suppression phase — feline evidence is limited to case-level reports.",
                "dosage_ja": "Hepatozoon felis（外挿）: 再発抑制フェーズとして 10-20 mg/kg 経口 12時間毎（餌に混和）— 猫のエビデンスは症例報告レベル。",
                "notes": "Feline hepatozoonosis is usually subclinical; treat only confirmed clinical cases.",
                "notes_ja": "猫のヘパトゾーン症は通常不顕性。治療は臨床症状が確認された症例に限る。",
            },
        },
        "side_effects": "Rare at therapeutic doses (GI upset); wide margin of safety",
        "side_effects_ja": "治療用量では稀（軽度の消化器症状）。安全域は広い",
        "contraindications": "Not a stand-alone acute therapy — it suppresses relapse only; acute H. americanum requires the TCP induction phase first",
        "contraindications_ja": "単独での急性期治療薬ではない — 再発抑制のみ。急性期のH. americanumはまずTCP導入フェーズが必要",
        "drug_interactions": [],
    },
    {
        "id": "biotin",
        "search_aliases": [
            "ビオチン",
            "バイオチン",
            "ビタミンB7",
            "Biotin",
        ],
        "name": "Biotin (Vitamin B7)",
        "name_ja": "ビオチン（ビタミンB7）",
        "category": "supplements",
        "mechanism": "Water-soluble B vitamin serving as a carboxylase cofactor in fatty-acid synthesis and keratinization. Supra-nutritional supplementation improves hoof horn tensile strength and growth quality in horses (placebo-controlled: Josseck 1995, Zenker 1995 Equine Vet J) and is used as a coat/skin adjunct in canine dermatology.",
        "mechanism_ja": "脂肪酸合成と角化に関わるカルボキシラーゼ補酵素の水溶性ビタミンB群。栄養要求量を超える補充で馬の蹄角質の強度・成長品質が改善する（プラセボ対照試験: Josseck 1995・Zenker 1995 Equine Vet J）。犬の皮膚科では被毛・皮膚の補助療法として用いる。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Hoof quality (hoof wall cracks, poor horn, coronary band dystrophy): 15-25 mg/head/day PO, continued 6-12 months minimum — the hoof wall grows ~6-9 mm/month, so effects appear only in new horn (Josseck 1995: 20 mg/day ×9-19 months).",
                "dosage_ja": "蹄質改善（裂蹄・蹄角質不良・冠状帯ジストロフィー）: 15-25 mg/頭/日 経口、最低6-12ヶ月継続 — 蹄壁の伸長は月6-9 mmのため効果は新生角質にのみ現れる（Josseck 1995: 20 mg/日×9-19ヶ月）。",
                "notes": "An adjunct to corrective farriery, never a replacement. Combine with balanced trimming q4-6wk. Methionine/zinc co-supplementation is common in hoof formulas.",
                "notes_ja": "矯正装蹄の補助であり代替ではない。4-6週毎のバランストリミングと併用。蹄用サプリではメチオニン・亜鉛の同時配合が一般的。",
            },
            "dog": {
                "safe": True,
                "dosage": "Coat/skin adjunct (hypothyroid coat recovery, follicular dysplasias, dull brittle coat): 2.5-5 mg/day PO (Frigg 1989 — adjunct-level evidence).",
                "dosage_ja": "被毛・皮膚の補助（甲状腺機能低下症の被毛回復・毛包形成異常・被毛脆弱）: 2.5-5 mg/日 経口（Frigg 1989 — 補助療法レベルのエビデンス）。",
                "notes": "Water-soluble — excess is excreted; toxicity is not a practical concern. Address the primary disease first (e.g. levothyroxine for hypothyroidism).",
                "notes_ja": "水溶性で過剰分は排泄されるため実務上の毒性懸念はない。まず基礎疾患の治療を優先（甲状腺機能低下症ならレボチロキシン等）。",
            },
        },
        "side_effects": "None expected at therapeutic doses (water-soluble vitamin)",
        "side_effects_ja": "治療用量では想定されない（水溶性ビタミン）",
        "contraindications": "None specific. Raw egg white feeding (avidin) antagonizes biotin — correct the diet rather than merely supplementing",
        "contraindications_ja": "特異的禁忌なし。生卵白給餌（アビジン）はビオチンを拮抗阻害する — 補充だけでなく食事自体を是正する",
        "drug_interactions": [],
    },
]
