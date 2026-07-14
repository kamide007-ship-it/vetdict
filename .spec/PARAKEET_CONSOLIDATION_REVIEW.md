# parakeet（インコ）論理統合レビューワークシート（T103）— 提示のみ・未適用

> **状態**: プレゼンテーションのみ。**B/C はまだ適用していない**（✅/❌/✏️ 待ち）。
> A（auto tier）は serve 時に適用済み＝**追認の可否**を確認したい。物理削除ゼロ・301・即ロールバック可。
> 元データ: parakeet 459件 → auto 適用後 **437 served**。B を全承認すると **≈415 served**。

インコの重複は「種タグ（インコ）・重症度（進行型/初期）・略語（TB↔Tuberculosis, PTFE）・表記ゆれ（単数↔複数）」分割が中心。
毒物系（テフロン/アボカド/亜鉛/鉛/銅）と尾脂腺（膿瘍/腫瘍）は分散が多い。眼球突出系の Proptosis/Exophthalmos ペアは本種には無し。
一方で **ダニ（Mite）↔マダニ（Tick）**、**そ嚢うっ滞（Stasis）↔そ嚢閉塞（Impaction）**、**肝炎↔肝リピドーシス** は別病態で分離維持。

---

## A. auto tier（既に適用済み — 追認可否）21件
| canonical（残す） | 統合済み | id |
|---|---|---|
| 甲状腺腫 Goiter (Thyroid Hyperplasia) | + Goiter | 0028 ← 0253 |
| ビタミンA欠乏症 Hypovitaminosis A | + Vitamin A Deficiency | 0031 ← 0275 |
| アボカド中毒 Avocado Toxicosis | + Toxicosis(Parakeet) + Toxicity | 0039 ← 0197, 0326 |
| 腎腫瘍 Renal Tumors | + Renal Tumor | 0040 ← 0307 |
| 脂肪腫 Lipomas | + Lipoma | 0041 ← 0315 |
| 精巣腫瘍 Testicular Tumors | + Testicular Tumor | 0042 ← 0305 |
| 黄色腫 Xanthomas | + Xanthoma | 0043 ← 0317 |
| 卵黄性腹膜炎 Egg Yolk Peritonitis | + Egg Peritonitis | 0048 ← 0302 |
| 脚骨折 Leg Fractures | + Fracture (Leg) | 0051 ← 0292 |
| 翼骨折 Wing Fractures | + Fracture (Wing) | 0052 ← 0291 |
| 総排泄腔炎 Cloacitis | + Cloacitis | 0069 ← 0301 |
| 動脈硬化症 Atherosclerosis | + Arteriosclerosis | 0080 ← 0311 |
| 熱中症 Heatstroke | + Heat Stroke | 0085 ← 0327 |
| 尾脂腺膿瘍 Uropygial Gland Abscess | + Preen Gland Abscess | 0240 ← 0092 |
| 毛細線虫症 Capillariasis | + Capillaria Infection | 0107 ← 0286 |
| 尾脂腺腫瘍 Preen Gland Tumor | + Preen Gland Tumor | 0134 ← 0261 |
| 銅中毒 Copper Poisoning | + Copper Toxicosis | 0166 ← 0451 |
| 腎腺癌 Renal Adenocarcinoma | + Renal Adenocarcinoma(Parakeet) | 0216 ← 0174 |
| 嘴骨折 Beak Fracture | + Beak Fracture (Parakeet) | 0296 ← 0190 |
| 甲状腺癌 Thyroid Carcinoma | + Thyroid Carcinoma(Parakeet) | 0230 ← 0192 |
| 鉛中毒 Lead Toxicosis | + Lead Poisoning | 0242 ← 0324 |

---

## B. curated 同一疾患候補（承認で統合 — 未適用）
| # | canonical（残す） | 統合候補 | id | 判定根拠 |
|--:|---|---|---|---|
| 1 | マイコバクテリア症（鳥結核）Mycobacteriosis | + Avian TB | 0011 ← 0300 | 略語違い（TB↔Tuberculosis）＋種タグ＝同一 |
| 2 | 条虫症 Tapeworm Infection | + (Parakeet) | 0023 ← 0186 | 種タグ違い＝同一 |
| 3 | メガバクテリア症 Megabacteriosis (AGY/Macrorhabdus) | + Megabacteriosis + (AGY) | 0027 ← 0252, 0272 | AGY=Macrorhabdus＝同一疾患。種タグ/略語違い |
| 4 | 肝リピドーシス（脂肪肝）Hepatic Lipidosis | + (Seed Diet) | 0034 ← 0257 | 病因修飾（種子食）違いで同一。**下記クロス（肝脂肪変性4ラベル）参照** ✏️ |
| 5 | テフロン中毒（PTFE）Teflon Toxicosis | + Toxicosis(Parakeet) | 0038 ← 0196 | 種タグ違い＝同一。**0325 Teflon/PTFE も同一の疑い（下記クロス）** ✏️ |
| 6 | 精巣腫瘍 Testicular Tumors | + (Cere Color Change) | 0042 ← 0256 | ろう膜変色は精巣腫瘍の典型徴候＝同一。0042 は A で 0305 統合済＝0256 を追加 ✏️ |
| 7 | 黄色腫 Xanthomas | + (Advanced) + (Wing) | 0043 ← 0177, 0263 | 重症度（進行型）/部位（翼）違いで同一。0043 は A で 0317 統合済。翼＝部位のみ ✏️ |
| 8 | 開脚症 Splay Leg | + Splayed Legs(Neonatal) ×2 | 0053 ← 0203, 0254 | 新生児型＝開脚症の典型発症＝同一 |
| 9 | 羽嚢腫 Feather Cysts | + Feather Cyst | 0058 ← 0264 | 単複/種タグ違い＝同一。**0133/0455 羽包嚢胞との整理は下記クロス** |
| 10 | 毛引き症 Feather Plucking | + Feather Plucking | 0059 ← 0268 | 種タグ違い＝同一（ホルモン性 0159 は別要因で分離） |
| 11 | そ嚢停滞（サワークロップ）Crop Stasis | + (Neonatal) + Crop Stasis | 0067 ← 0265, 0270 | うっ滞＝同一（新生児は発症状況）。**閉塞 0206/0334 は C で分離** |
| 12 | 熱傷・化学熱傷 Burns | + Burns | 0082 ← 0330 | 種タグ違い＝同一 |
| 13 | 大腸菌感染症 E. coli (Colibacillosis) | + E. coli Infection | 0113 ← 0299 | 同義（Colibacillosis）＋種タグ＝同一 |
| 14 | 腺胃潰瘍 Proventricular Ulceration | + (Budgerigar) | 0127 ← 0226 | セキセイ＝インコの一種＝同一（腺胃/前胃は同義）✏️ |
| 15 | 慢性羽包嚢胞 Feather Follicle Cyst (Chronic) | + Feather Follicle Cyst | 0133 ← 0455 | 慢性修飾/種タグ違い＝同一 |
| 16 | 亜鉛中毒 Zinc Toxicosis | + (Advanced) | 0241 ← 0195 | 重症度（進行型）違いで同一。canonical は無タグ 0241 |
| 17 | 慢性呼吸器疾患 CRD | + Chronic Respiratory Disease | 0228 ← 0362 | 略語（CRD）/種タグ違い＝同一 |
| 18 | 蝋膜肥大（褐色肥大症）Cere Hypertrophy | + Cere Hypertrophy | 0235 ← 0262 | 種タグ違い＝同一 |

---

## C. 分離維持（統合しない推奨）
| 疾患ペア | id | 論点 |
|---|---|---|
| ダニ寄生症 Mite Infestation / ダニ寄生症 Tick Infestation | 0024 / 0155 | name_ja は同一「ダニ寄生症」だが Mite（ワクモ・羽ダニ）≠ Tick（マダニ）＝別寄生虫。統合ではなく **0155 のリネーム候補**（マダニ寄生症）|
| 内臓痛風 Gout(Visceral) / 関節痛風 Gout(Articular) | 0029 / 0030 | 内臓型（尿酸塩内臓沈着）vs 関節型＝別病態・別予後。分離維持。0274「痛風（内臓型/関節型）」は統合エントリ ✏️要確認 |
| そ嚢うっ滞 Crop Stasis / 嗉嚢閉塞 Crop Impaction | 0067 / 0206, 0334 | 機能性うっ滞 vs 異物閉塞（Ileus vs Obstruction ガード相当）＝別病態。0334 は EN「Impaction」/JA「そ嚢停滞」の **ラベル不整合 ✏️** |
| 肝疾患（肝炎）Hepatitis / 肝疾患（肝リピドーシス） | 0072 / 0273 | name_ja は同一「肝疾患」だが 肝炎（炎症）vs 肝リピドーシス（脂肪沈着）＝別病態。分離維持 |
| 乳頭腫症 Papillomatosis / 内臓乳頭腫症 Papillomatosis(Internal) | 0070 / 0335 | 内臓型は総排泄腔/消化管の別エンティティ。**0170 Internal Papillomatosis と重複の恐れ** ✏️（統合先の整理が必要）|

---

## クロスクラスタ注意
- **肝の脂肪変性が4ラベルに分散**: 肝リピドーシス 0034（+0257 種子食 #B4）、セキセイインコ肝リピドーシス 0202、
  肝疾患（肝リピドーシス）0273（#C）。同一病態を「種子食/セキセイ/肝疾患」で別クラスタ化した可能性＝横断統合の候補（獣医判断）。
- **テフロン中毒3ラベル**: 0038（PTFE）+0196（#B5）に加え **0325 Teflon/PTFE Toxicosis（テフロン/PTFE中毒）** が toxico family に存在。
  name_ja が僅差で exact_dup 外だが実質同一＝0038 へ折込む候補 ✏️。
- **羽（毛包）嚢胞が2クラスタ**: 羽嚢腫 0058/0264（#B9）と 羽包嚢胞 0133/0455（#B15）。Feather Cyst と Feather Follicle Cyst は
  同一の可能性あり＝4件集約も要検討（獣医判断）。反復性羽嚢腫 0213 も近縁。
- **そ嚢カンジダ／真菌症**: 0017 Crop Candidiasis / 0163 Crop Mycosis / 0271 Candidiasis(Crop Mycosis) / 0221 新生児型 は
  exact_dup 外だが近縁＝将来整理候補（本ワークシートでは提示せず）。
- **精巣腫瘍/セルトリ細胞腫**: 0042（+0256 #B6）と 0214 Sertoli Cell / 0306 Sertoli Cell Tumor は組織型が異なり分離が妥当。

---

## 集計
- **A（追認）**: 21統合（適用済み・459→**437 served**、records_merged_away=22）。
- **B（承認で適用）**: #1–#18（22件を統合）。全承認で **≈415 served**。✏️ は #4/#5/#6/#7/#14。
- **C（分離維持）**: ダニ/マダニ・内臓/関節痛風・うっ滞/閉塞・肝炎/肝リピ・乳頭腫/内臓乳頭腫 の5論点。
- 適用: `_CURATED_MERGE["parakeet"]` に B 承認行を追記 → `build_canonical.py parakeet --apply`。**未適用。**
