# bird（鳥）論理統合レビューワークシート（T103）— 提示のみ・未適用

> **状態**: プレゼンテーションのみ。**B/C はまだ適用していない**（✅/❌/✏️ 待ち）。
> A（auto tier）は serve 時に適用済み＝**追認の可否**を確認したい。物理削除ゼロ・301・即ロールバック可。
> 元データ: bird 551件 → auto 適用後 **530 served**。B を全承認すると **≈499 served**（B推奨で -31件）。

鳥の重複は「種タグ（鳥）分割・重症度/病型分割・略号/表記ゆれ・同義語（Toxicosis↔Poisoning、Prolapse↔脱）」が中心。
メガバクテリア症・毛引き/羽毛破壊行動・卵停滞/卵詰まり・鉛/亜鉛中毒・甲状腺腫/ヨウ素欠乏が複数ラベルに分散。

---

## A. auto tier（既に適用済み — 追認可否）21件
| canonical（残す） | 統合済み | id |
|---|---|---|
| 鳥痘 Avian Poxvirus | + Avian Pox（鳥） | 0003 ← 0402 |
| オウム病（クラミジア症） Psittacosis | + Psittacosis (Chlamydiosis)（鳥） | 0010 ← 0398 |
| メガバクテリア症（AGY） | + Megabacteriosis (AGY)（鳥） | 0024 ← 0410 |
| ムコール症 Mucormycosis | + Mucormycosis（鳥） | 0026 ← 0347 |
| 筋胃炎 Ventriculitis | + Ventriculitis（鳥） | 0038 ← 0324 |
| 総排泄腔脱 Cloacal Prolapse | + Prolapse of Cloaca（鳥） | 0039 ← 0326 |
| 甲状腺腫 Thyroid Goiter | + Goiter (Thyroid Enlargement)（鳥） | 0053 ← 0313 |
| ビタミンA欠乏症 | + Vitamin A Deficiency（鳥） | 0055 ← 0413 |
| フレンチモルト French Molt | + French Molt（鳥） | 0064 ← 0333 |
| 羽毛嚢胞 Feather Cysts | + Feather Cyst（鳥） | 0067 ← 0454 |
| 黄色腫 Xanthomas | + Xanthoma（鳥） | 0068 ← 0453 |
| 鉛中毒 Lead Poisoning | + Lead Poisoning（鳥） | 0111 ← 0460 |
| 卵黄性腹膜炎 Egg Yolk Peritonitis | + Egg Peritonitis（鳥） | 0083 ← 0440 |
| 胆管癌 Bile Duct Carcinoma | + Bile Duct Carcinoma（鳥） | 0094 ← 0317 |
| 条虫症 Tapeworms | + Tapeworm Infection（鳥） | 0099 ← 0425 |
| 動脈硬化症 Atherosclerosis | + Arteriosclerosis（鳥） | 0106 ← 0448 |
| 亜鉛中毒 Zinc Poisoning | + Zinc Toxicosis（鳥） | 0112 ← 0461 |
| 羽毛破壊行動 FDB | + Feather Destructive Behavior（鳥） | 0115 ← 0329 |
| 眼窩周囲膿瘍 Periorbital Abscess | + Periorbital Abscess（鳥） | 0122 ← 0363 |
| 植物中毒 Plant Toxicity | + Plant Toxicosis（鳥） | 0191 ← 0391 |
| 卵管炎 Salpingitis | + Salpingitis（鳥） | 0283 ← 0384 |

---

## B. curated 同一疾患候補（承認で統合 — 未適用）
| # | canonical（残す） | 統合候補 | id | 判定根拠 |
|--:|---|---|---|---|
| 1 | 嘴羽毛病（PBFD） | + Beak and Feather Disease (Circovirus)（鳥） | 0000 ← 0341 | PBFD＝サーコウイルス病＝同一。名の別表記のみ |
| 2 | 腺胃拡張症（PDD／ボルナウイルス） | + PDD（鳥） | 0001 ← 0400 | 同一疾患（PDD）。名_ja「腺胃／前胃」表記ゆれ |
| 3 | パチェコ病（オウム目ヘルペスウイルス） | + Pacheco's Disease（鳥） | 0006 ← 0403 | 種タグ違い＝同一 |
| 4 | パラミクソウイルス感染症 | + Paramyxovirus Infection（鳥） | 0007 ← 0343 | 種タグ違い＝同一（両者PMV総称） |
| 5 | 大腸菌感染症（Colibacillosis） | + E. coli Infection（鳥） | 0013 ← 0437 | 同義語（Colibacillosis）＝同一 |
| 6 | カンジダ症 | + Candidiasis (Crop Mycosis) | 0023 ← 0308 | 括弧補足（そのう真菌症）＝同一 |
| 7 | メガバクテリア症（AGY） | + Megabacteriosis (Macrorhabdus ornithogaster) | 0024 ← 0307 | AGY＝Macrorhabdus＝同一（同義語）。A の 0410 に加え 0307 も統合 |
| 8 | 肺炎 Pneumonia | + Pneumonia (Bacterial)（鳥） | 0031 ← 0417 | ✏️要確認：総称 vs 細菌性。umbrella に集約するか病因を残すか獣医判断 |
| 9 | 嗉嚢停滞 Crop Stasis | + Crop Stasis（鳥） | 0033 ← 0408 | 種タグ違い＝同一 |
| 10 | 嗉嚢火傷 Crop Burn | + Crop Burns（鳥） | 0034 ← 0409 | 単複表記＋種タグ＝同一 |
| 11 | 腎不全（急性／慢性） | + Renal Failure (Acute)（鳥） | 0048 ← 0445 | ✏️要確認：急性のみ 0445 は 0048（急性/慢性 umbrella）の部分集合 |
| 12 | 腎腫瘍（腎腺癌） Renal Tumor | + Renal Tumor（鳥） | 0052 ← 0444 | 種タグ違い＝同一。0206 も要横断確認（下記クロス） |
| 13 | ヨウ素欠乏症 Iodine Deficiency | + Iodine Deficiency (Thyroid Hyperplasia)（鳥） | 0058 ← 0414 | 括弧補足（甲状腺過形成）＝同一 |
| 14 | 毛引き症（羽毛破壊行動） | + Feather Plucking（鳥） | 0063 ← 0404 | 種タグ違い＝同一。FDB(0115) との横断整理は下記クロス |
| 15 | 扁平上皮癌（皮膚） SCC | + Squamous Cell Carcinoma（鳥） | 0069 ← 0452 | 部位補足（皮膚）付き総称と一致＝同一 |
| 16 | 代謝性骨疾患（くる病） MBD | + Metabolic Bone Disease（鳥） | 0071 ← 0431 | 種タグ違い＝同一 |
| 17 | 卵詰まり（難産） Egg Binding | + Egg Binding（鳥） | 0073 ← 0405 | 種タグ違い＝同一。卵停滞(0295)との横断は下記 |
| 18 | 鉛中毒 Lead Poisoning | + Lead Poisoning (Neurological) | 0111 ← 0079 | ✏️要確認：神経型は鉛中毒の一発現。病型を残すなら分離 |
| 19 | ワクモ（赤ダニ） Red Mites | + Red Mite (Dermanyssus)（鳥） | 0096 ← 0421 | 単複＋種タグ＝同一（Dermanyssus gallinae） |
| 20 | 回虫症（アスカリディア） Roundworms | + Roundworm (Ascaridia)（鳥） | 0098 ← 0423 | 単複＋種タグ＝同一 |
| 21 | 毛細線虫症（キャピラリア） Capillaria | + Capillaria (Hairworm, Severe) + Capillaria Infection（鳥） | 0100 ← 0232, 0424 | 重症度/種タグ違い＝同一（3件） |
| 22 | 亜鉛中毒 Zinc Poisoning | + Zinc Toxicosis (Hardware Disease)（鳥） | 0112 ← 0387 | 同義語（Toxicosis/金属中毒）＝同一。A の 0461 に加え 0387 も統合 |
| 23 | 鳥脳脊髄炎 Avian Encephalomyelitis | + Avian Encephalomyelitis (Epidemic Tremor) | 0126 ← 0227 | 括弧補足（流行性振戦＝AEの別名）＝同一 |
| 24 | マレック病 Marek's Disease | + Marek's Disease (Avian) | 0127 ← 0224 | 種タグ違い＝同一 |
| 25 | 伝染性喉頭気管炎 ILT | + ILT Advanced（重度） | 0130 ← 0233 | 重症度違い＝同一 |
| 26 | 鳥スピロヘータ症 | + Avian Spirochetosis (Borrelia) | 0133 ← 0235 | 病原体補足（Borrelia＝スピロヘータ）＝同一 |
| 27 | 総排泄腔炎（ベントグリート） Cloacitis | + Cloacitis（鳥） | 0174 ← 0439 | 種タグ違い＝同一 |
| 28 | 素嚢結石 Ingluvoliths (Crop Stones) | + Ingluvoliths (Crop Concretions) | 0176 ← 0292 | 同義語（Stones/Concretions）＝同一。名_ja 素嚢/嗉嚢表記ゆれ |
| 29 | 卵停滞（産卵前） Egg Retention | + Retained Egg（鳥） | 0295 ← 0383 | ✏️要確認：卵停滞＝同一。卵詰まり(0073)との境界は下記クロス |
| 30 | バンブルフット（足底皮膚炎） Pododermatitis | + Bumblefoot (Advanced/Surgical)（鳥） | 0406 ← 0349 | ✏️要確認：0349は進行/外科ステージ。病期を残すなら分離。canonical は基本名 0406 推奨 |

---

## C. 分離維持（統合しない推奨）
| 疾患ペア | id | 論点 |
|---|---|---|
| 翼骨折 Fracture (Wing) / 脚骨折 Fracture (Leg) | 0428 / 0429 | 骨折**部位**が異なる（翼 vs 脚）＝別エントリで維持 |
| 鉄蓄積症（non-hemochromatosis） / 鉄蓄積症（Hemochromatosis） | 0059 / 0415 | 英名が「non-hemochromatosis」と「Hemochromatosis」で**矛盾**。名_ja は同一。おそらく同一疾患だがラベルが対立＝**RENAME 候補**（獣医が整合を確認、silent merge は不可） |

---

## クロスクラスタ注意（≥3ラベルに分散）
- **メガバクテリア症/鳥胃酵母（Macrorhabdus）**: 0024(AGY), 0307(Macrorhabdus), 0410(A済) に加え family に 0141「Avian Gastric Yeast Refractory（難治性）」、0310「Avian Gastric Yeast (Macrorhabdus)（鳥）」が分散。B#7 で 0307 統合後も 0141/0310 の横断集約可否を要確認。
- **毛引き/羽毛破壊行動（FDB）**: 0063+0404(B#14), 0115+0329(A済) に加え 0201「Hormonal Feather Plucking」、0263「FDB – Hormonal」が別ラベル。0063 と 0115 は病態同一（毛引き＝FDB）の可能性大＝横断統合の最有力候補。ホルモン型 2件は病因分離の余地。
- **卵関連（卵詰まり/卵停滞/卵管）**: 卵詰まり 0073(B#17), 卵停滞 0295+0383(B#29) が近接。Egg Binding と Egg Retention/Retained Egg の境界（産卵前 vs 産卵時停滞）を獣医が整理。卵管炎 0283/卵黄性腹膜炎 0083 は別病態で分離維持。
- **鉛中毒**: 0079(神経型), 0111(総称), 0460(A済)。B#18 で神経型を集約するか病型分離か要判断。
- **甲状腺腫/ヨウ素欠乏/甲状腺過形成**: 0053(甲状腺腫,A済に 0313), 0058+0414(B#13 ヨウ素欠乏), family 0207「Avian Thyroid Hyperplasia」。ヨウ素欠乏→甲状腺腫（過形成）は病因-結果関係。集約範囲を獣医判断。
- **腎腫瘍**: 0052+0444(B#12), family 0206「Avian Renal Tumor（鳥類腎腫瘍）」。0206 も同一の可能性＝横断確認。

## 集計
- **A（追認）**: 21統合（適用済み・530 served）。
- **B（承認で適用）**: #1–#30（merged-away 計31件。#8/#11/#18/#29/#30 は ✏️要確認）。全承認で **≈499 served**。
- **C（分離維持）**: 骨折部位（翼/脚）、鉄蓄積症ラベル矛盾（RENAME 候補）。
- 適用: `_CURATED_MERGE["bird"]` に承認行を追記 → `build_canonical.py bird --apply`。**未適用。**
