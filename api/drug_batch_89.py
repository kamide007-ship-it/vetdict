"""Drug batch 89 – 2026-10 第81弾.

Recombinant human thyrotropin alfa (rhTSH; Thyrogen) — the TSH-stimulation
test agent. Twenty-five disease entries (canine/feline hypothyroidism work-up,
exotic thyroid disease) tell the reader to "confirm with a TSH stimulation
test", but the dictionary had no entry for the only practical stimulating
agent (bovine TSH is no longer marketed), so its dose, sampling time and
handling could not be looked up.
Evidence: Boretti FS, Sieber-Ruckstuhl NS, Favrot C, et al. Evaluation of
recombinant human thyroid-stimulating hormone to test thyroid function in
dogs suspected of having hypothyroidism. Am J Vet Res 2006;67:2012-2016;
De Roover K, Duchateau L, Carmichael N, et al. Effect of storage of
reconstituted recombinant human thyroid-stimulating hormone (rhTSH) on
thyroid-stimulating hormone (TSH) response testing in euthyroid dogs. J Vet
Intern Med 2006;20:812-817; Stegeman JR, Graham PA, Hauptman JG. Use of
recombinant human thyroid-stimulating hormone for thyrotropin-stimulation
testing of euthyroid cats. Am J Vet Res 2003;64:149-152; Scott-Moncrieff JC,
in Ettinger SJ et al. Textbook of Veterinary Internal Medicine 8th ed.
"""

DRUGS_BATCH_89 = [
    {
        "id": "thyrotropin_alfa",
        "search_aliases": [
            "タイロゲン",
            "Thyrogen",
            "rhTSH",
            "組換えヒトTSH",
            "組換えヒト甲状腺刺激ホルモン",
            "ヒト組換えTSH",
            "TSH刺激試験",
            "thyrotropin alfa",
        ],
        "name": "Thyrotropin Alfa (recombinant human TSH, Thyrogen)",
        "name_ja": "ヒトチロトロピン アルファ（組換えヒトTSH・タイロゲン）",
        "category": "endocrine",
        "mechanism": "Recombinant human thyroid-stimulating hormone. Binds the TSH receptor on thyroid follicular cells and stimulates T4 release; the rise in serum total T4 after injection measures thyroid reserve. Used only as a diagnostic agent (TSH-stimulation test) in animals.",
        "mechanism_ja": "組換えヒト甲状腺刺激ホルモン。甲状腺濾胞細胞のTSH受容体に結合してT4の放出を促し、投与後の血清総T4の上昇で甲状腺の予備能を評価する。動物では診断薬（TSH刺激試験）としてのみ使う。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "TSH-stimulation test: 75-150 µg/dog IV (Boretti 2006 used 75 µg; use 150 µg in dogs on drugs or with illness that may blunt the response). Measure serum total T4 immediately before and 6 hours after injection. A post-TSH T4 that stays low (does not rise into the reference interval) supports primary hypothyroidism; a clear rise into or above the reference interval argues against it — interpret against the laboratory's/study cut-offs.",
                "dosage_ja": "TSH刺激試験: 1頭あたり 75〜150 µg を静注（Boretti 2006 は 75 µg。反応を鈍らせる薬剤投与中や併発疾患のある犬では 150 µg）。投与直前と投与6時間後に血清総T4を測定する。投与後T4が低値のまま（基準範囲に入らない）であれば原発性甲状腺機能低下症を支持し、基準範囲内〜以上へ明らかに上昇すれば否定的 — 検査機関・文献のカットオフ値で判定する。",
                "notes": "Reserve for dogs in which basal T4/fT4/cTSH are inconclusive — it is the most discriminating functional test but costly. Euthyroid sick syndrome (non-thyroidal illness) and glucocorticoids, phenobarbital, sulfonamides or clomipramine can blunt the T4 response; test after recovery or after withdrawing the drug where possible. Reconstituted Thyrogen (0.9 mg vial) can be divided into single-dose aliquots: stable about 4 weeks refrigerated and 8 weeks frozen at -20 °C (De Roover 2006). Human product, used off-label.",
                "notes_ja": "基礎T4・fT4・cTSHで判断がつかない犬に限って使う（最も識別力の高い機能検査だが高価）。甲状腺外疾患（euthyroid sick syndrome）やグルココルチコイド・フェノバルビタール・サルファ剤・クロミプラミンはT4の反応を鈍らせるため、可能なら回復後や休薬後に検査する。溶解したタイロゲン（0.9 mg バイアル）は1回量ずつ小分けでき、冷蔵で約4週間、-20 °Cの冷凍で約8週間安定（De Roover 2006）。ヒト用製剤の適応外使用。",
            },
            "cat": {
                "safe": True,
                "dosage": "TSH-stimulation test: 25-200 µg/cat IV (Stegeman 2003 compared 25-200 µg in euthyroid cats); measure total T4 before and 6-8 hours after injection.",
                "dosage_ja": "TSH刺激試験: 1頭あたり 25〜200 µg を静注（Stegeman 2003 が健常猫で25〜200 µgを比較）。投与直前と6〜8時間後に総T4を測定する。",
                "notes": "Mainly used to confirm iatrogenic hypothyroidism after radioiodine, thyroidectomy or over-treatment with methimazole (failure of T4 to rise). Not useful for diagnosing hyperthyroidism (use total T4, fT4, or T3 suppression / scintigraphy).",
                "notes_ja": "主に放射性ヨウ素治療・甲状腺摘出・メチマゾール過量後の医原性甲状腺機能低下症の確認に使う（T4が上昇しない）。甲状腺機能亢進症の診断には有用でない（総T4・fT4・T3抑制試験・シンチグラフィを用いる）。",
            },
        },
        "contraindications": "Not for treatment. Hypersensitivity to the product. Interpretation is unreliable during significant non-thyroidal illness or with drugs that suppress the thyroid axis.",
        "contraindications_ja": "治療目的には使わない。本剤への過敏症。重い甲状腺外疾患の最中や甲状腺系を抑制する薬剤の投与中は判定の信頼性が低い。",
        "side_effects": [
            "Rare hypersensitivity or vomiting after injection",
        ],
        "side_effects_ja": [
            "まれに注射後の過敏反応・嘔吐",
        ],
        "drug_interactions": [
            {
                "drug": "Prednisolone",
                "effect": "Glucocorticoids suppress the thyroid axis and blunt the post-TSH T4 rise (false 'hypothyroid' result).",
                "effect_ja": "グルココルチコイドは甲状腺系を抑制し、TSH投与後のT4上昇を鈍らせる（偽の機能低下判定）。",
                "severity": "moderate",
            },
            {
                "drug": "Phenobarbital",
                "effect": "Lowers T4 and can blunt the response to TSH — interpret with caution.",
                "effect_ja": "T4を低下させTSHへの反応を鈍らせうる — 判定に注意。",
                "severity": "moderate",
            },
            {
                "drug": "Levothyroxine",
                "effect": "Thyroid supplementation suppresses endogenous thyroid function — withdraw for 6-8 weeks before testing a supplemented dog.",
                "effect_ja": "甲状腺ホルモン補充は内因性甲状腺機能を抑制する — 補充中の犬を検査する場合は6〜8週間休薬してから行う。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Boretti FS, Sieber-Ruckstuhl NS, Favrot C, et al. Evaluation of recombinant human thyroid-stimulating hormone to test thyroid function in dogs suspected of having hypothyroidism. Am J Vet Res 2006;67:2012-2016.",
            "De Roover K, Duchateau L, Carmichael N, et al. Effect of storage of reconstituted recombinant human thyroid-stimulating hormone (rhTSH) on thyroid-stimulating hormone (TSH) response testing in euthyroid dogs. J Vet Intern Med 2006;20:812-817.",
            "Stegeman JR, Graham PA, Hauptman JG. Use of recombinant human thyroid-stimulating hormone for thyrotropin-stimulation testing of euthyroid cats. Am J Vet Res 2003;64:149-152.",
            "Scott-Moncrieff JC. Hypothyroidism. In: Ettinger SJ, Feldman EC, Côté E, eds. Textbook of Veterinary Internal Medicine. 8th ed. Elsevier; 2017.",
        ],
    },
]
