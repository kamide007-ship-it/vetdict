"""Drug batch 87 – 2026-10 第79弾.

1. 2.5% cross-linked polyacrylamide hydrogel (Arthramid Vet) — a permanent,
   non-resorbable intra-articular viscoelastic implant for equine
   osteoarthritis (CE-marked medical device; marketed in the EU, UK, US and
   Australia). The dictionary had corticosteroid, hyaluronan, PSGAG,
   pentosan and IRAP-type options for equine OA but no hydrogel, and the
   horse OA treatment text could not point to it.
   Evidence: Tnibar M, Schougaard H, Camitz L et al. An international
   multi-centre prospective study on the efficacy of an intraarticular
   polyacrylamide hydrogel in horses with osteoarthritis: a 24 months
   follow-up. Acta Vet Scand 2015;57:20 (lameness improved in most horses,
   effect sustained at 24 months); Tnibar M et al. Vet Comp Orthop
   Traumatol 2013 (histology: synovial integration of the gel);
   McIlwraith, Frisbie, Kawcak & van Weeren, Joint Disease in the Horse
   2nd ed (2016).
"""

DRUGS_BATCH_87 = [
    {
        "id": "polyacrylamide_hydrogel",
        "search_aliases": [
            "アースラミド",
            "アーサラミド",
            "Arthramid",
            "Arthramid Vet",
            "ポリアクリルアミドハイドロゲル",
            "ポリアクリルアミドゲル",
            "polyacrylamide gel",
            "PAAG",
            "iPAAG",
        ],
        "name": "2.5% Polyacrylamide Hydrogel (Arthramid Vet)",
        "name_ja": "2.5%ポリアクリルアミドハイドロゲル（アースラミド・ベット）",
        "category": "musculoskeletal",
        "mechanism": "A 2.5% cross-linked polyacrylamide hydrogel (97.5% water) injected into the joint. It is not resorbed: the gel integrates into the synovial membrane (sub-intimal layer), increasing synovial viscoelasticity and reducing joint effusion and capsular stiffness. It is a medical device, not a pharmacological agent — it has no anti-inflammatory drug effect and no withdrawal time.",
        "mechanism_ja": "関節内に注入する2.5%架橋ポリアクリルアミドハイドロゲル（97.5%が水）。吸収されず、滑膜（内膜下層）に組み込まれて滑膜の粘弾性を高め、関節液貯留と関節包のこわばりを軽減する。薬理作用を持つ薬剤ではなく医療機器で、抗炎症薬としての作用や休薬期間はない。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Intra-articular, single injection under strict aseptic technique: typically 1-2 mL per joint according to joint size and the manufacturer's guidance (e.g. small joints such as the distal interphalangeal or pastern joint toward the lower volume, the fetlock or carpus toward the upper volume). Box/stall rest 24-48 h then walking; effect develops over 2-6 weeks. Repeat only after re-evaluation if response is incomplete.",
                "dosage_ja": "関節内に単回注入（厳密な無菌操作）: 関節の大きさと製造元の指示に従い、通常1関節あたり1〜2 mL（蹄関節・冠関節など小関節は少なめ、球節・手根関節は多め）。注入後24〜48時間は馬房内安静、その後は常歩から再開。効果は2〜6週かけて現れる。反応が不十分な場合のみ再評価の上で追加注入を検討する。",
                "notes": "Option for chronic OA when intra-articular corticosteroids give only short-lived relief or should be limited (e.g. horses with equine metabolic syndrome/PPID and laminitis risk). Not for septic arthritis, unstable joints or fractures; rule out infection before injection. A transient post-injection flare can occur — distinguish from iatrogenic sepsis (synovial fluid analysis if lameness worsens after 24-48 h). The implant is permanent and cannot be removed. Not a doping substance, but follow the competition rules for intra-articular procedures before an event.",
                "notes_ja": "関節内コルチコステロイドの効果が短い、または使用を控えたい慢性OA（馬代謝症候群/PPIDで蹄葉炎リスクのある馬など）の選択肢。化膿性関節炎・不安定関節・骨折には使用しない（注入前に感染を除外）。注入後に一過性のフレア（関節炎の再燃）が起こることがあり、医原性の化膿性関節炎との鑑別が必要（24〜48時間後に跛行が悪化すれば関節液検査）。注入物は永続的で除去できない。ドーピング物質ではないが、競技前の関節内処置に関する規則に従う。",
            },
        },
        "contraindications": "Septic arthritis or any infection at the injection site; joint instability or intra-articular fracture; within 2-4 weeks of a previous intra-articular injection at the same site without re-evaluation.",
        "contraindications_ja": "化膿性関節炎や注入部位の感染、関節の不安定性・関節内骨折。同じ関節への前回の関節内注射から2〜4週以内（再評価なしでの注入）。",
        "side_effects": [
            "Transient joint flare (heat, effusion, increased lameness) for 24-48 h",
            "Iatrogenic septic arthritis (rare — aseptic technique is essential)",
        ],
        "side_effects_ja": [
            "注入後24〜48時間の一過性の関節フレア（熱感・関節液増加・跛行の増悪）",
            "医原性の化膿性関節炎（まれ — 無菌操作が必須）",
        ],
        "drug_interactions": [
            {
                "drug": "Triamcinolone",
                "effect": "Concurrent intra-articular corticosteroid may be used, but simultaneous injection is not well studied — follow the manufacturer's guidance and avoid stacking injections in the same joint without re-evaluation.",
                "effect_ja": "関節内コルチコステロイドとの併用は可能だが、同時注入のデータは限られる。製造元の指示に従い、再評価なしに同じ関節へ注射を重ねない。",
                "severity": "minor",
            },
        ],
        "references": [
            "Tnibar M, Schougaard H, Camitz L, et al. An international multi-centre prospective study on the efficacy of an intraarticular polyacrylamide hydrogel in horses with osteoarthritis: a 24 months follow-up. Acta Vet Scand 2015;57:20.",
            "McIlwraith CW, Frisbie DD, Kawcak CE, van Weeren PR. Joint Disease in the Horse, 2nd ed. Elsevier, 2016.",
        ],
    },
]
