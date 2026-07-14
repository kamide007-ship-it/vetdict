# tortoise（リクガメ）論理統合レビューワークシート（T103）— 提示のみ・未適用

> **状態**: プレゼンテーションのみ。**B/C はまだ適用していない**（✅/❌/✏️ 待ち）。
> A（auto tier）は serve 時に適用済み＝**追認の可否**を確認したい。物理削除ゼロ・301・即ロールバック可。
> 元データ: tortoise 288件 → auto 適用後 **279 served**。B を全承認すると最大 **≈255 served**（24件統合、うち ✏️ 要確認 8件）。

リクガメの重複は「**種タグ（リクガメ）付きの重複バッチ**（0162〜0287）」が中心で、基幹疾患セット（0000〜0161）と
同一疾患が二重登録されている。加えて痛風（内臓/関節）・骨折（四肢/甲羅）・卵胞停滞（排卵前/後/慢性）など
**病態別に正しく分離すべきペア**と、**臓器×病因のテンプレート合成エントリ**（呼吸器/消化管/肝/皮膚 × 細菌/ウイルス/真菌…）が混在。

---

## A. auto tier（既に適用済み — 追認可否）9件
| canonical（残す） | 統合済み | id |
|---|---|---|
| 蟯虫感染 Pinworm (Oxyurid) Infection | + Oxyurid Infection | 0015 ← 0173 |
| ビタミンA欠乏症 Vitamin A Deficiency | + Vitamin A Deficiency | 0023 ← 0249 |
| 腎不全 Renal Failure (CKD) | + Renal Failure | 0039 ← 0207 |
| 膀胱結石 Bladder Stones (Urolithiasis) | + Bladder Stone | 0040 ← 0209 |
| 熱傷 Thermal Burns | + Burns | 0046 ← 0257 |
| 耳膿瘍 Aural Abscess | + Ear Abscess | 0051 ← 0169 |
| 四肢骨折 Bone Fracture (Limb) | + Fracture (Limb) | 0092 ← 0232 |
| 卵巣腫瘍 Ovarian Neoplasia | + Ovarian Tumor | 0124 ← 0214 |
| 鉛中毒 Lead Toxicosis | + Lead Poisoning | 0126 ← 0254 |

---

## B. curated 同一疾患候補（承認で統合 — 未適用）
`exact_dup_clusters`（name_ja 一致＝強シグナル）で A 未収載のもの＋ family cluster 由来の明白な種タグ同義。canonical＝タグ無し／低ID／内容充実。

| # | canonical（残す） | 統合候補 | id | 判定根拠 |
|--:|---|---|---|---|
| 1 | 甲羅腐敗症 Shell Rot (Ulcerative Shell Disease) | + Shell Rot | 0000 ← 0167 | 種タグ違いで同一（SCUD 別ラベルは非存在＝統合可） |
| 2 | 肺炎 Pneumonia (Lower Resp. Infection) | + Pneumonia | 0006 ← 0224 | 種タグ違い |
| 3 | 肝リピドーシス Hepatic Lipidosis (脂肪肝) | + Hepatic Lipidosis | 0032 ← 0215 | 種タグ違い |
| 4 | 卵塞 Egg Binding (Dystocia) | + Egg Binding (Dystocia) | 0043 ← 0162 | 英名完全一致・括弧内表記ゆれ（難産/卵詰まり） |
| 5 | 皮下膿瘍 Abscess (Subcutaneous) | + 膿瘍 Abscess | 0050 ← 0201 | ✏️ 一般「膿瘍」＝既定で皮下。部位不特定なら統合、他部位膿瘍とは分離（C参照） |
| 6 | 高体温症 Hyperthermia (Heat Stroke) | + Hyperthermia | 0063 ← 0253 | 種タグ違い（熱傷 0046 とは別病態） |
| 7 | カルシウム欠乏症 Calcium Deficiency | + Calcium Deficiency | 0072 ← 0250 | 種タグ違い |
| 8 | 眼感染症 Eye Infection (Ophthalmitis) | + Eye Infection | 0075 ← 0231 | 種タグ違い |
| 9 | ダニ寄生 Mite Infestation | + Mite Infestation (Ophionyssus) | 0079 ← 0190 | ✏️ Ophionyssus＝リクガメ主要ダニ。属名特定のみの差＝同一 |
| 10 | マイコバクテリア症 Mycobacteriosis | + Mycobacteriosis | 0097 ← 0186 | 表記ゆれ（〜症/〜ウム症）・種タグ違い（人獣共通注意は本文で） |
| 11 | 慢性濾胞停滞 Follicular Stasis (Chronic) | + Follicular Stasis | 0116 ← 0178 | ✏️ 慢性型と汎用型。排卵前/後型（0044/0210）は分離（C参照） |
| 12 | 関節痛風 Articular Gout | + 痛風（関節型） | 0041 ← 0206 | 種タグ違いの同型（関節型どうし） |
| 13 | 内臓痛風 Visceral Gout | + 痛風（内臓型） | 0042 ← 0205 | 種タグ違いの同型（内臓型どうし）。※関節型と内臓型は分離（C参照） |
| 14 | 膀胱結石（尿酸塩型）Cystic Calculi - Urate | + Bladder Stone (Urate) | 0158 ← 0176 | 尿酸塩型どうし・種タグ違い。一般 0040 への統合は ✏️（クロス参照） |
| 15 | 甲羅骨折・外傷 Shell Fracture / Trauma | + Fracture (Shell/Carapace) | 0002 ← 0233 | **甲羅骨折どうし**。exact_dup が四肢骨折(0092)と誤クラスタ化＝実際は甲羅側へ統合 |
| 16 | 拒食（行動性）Anorexia (Behavioral) | + ストレス性拒食 | 0221 ← 0262 | ✏️ 行動性/ストレス性は実質同一（非器質性拒食）。慢性/冬眠後(0076/0087)は別 |
| 17 | 鞭毛虫感染症 Flagellate Protozoa Infection | + Protozoal/Protozoan Infection | 0017 ← 0172, 0196 | ✏️ 3件が同一（Protozoa/Protozoal/Protozoan の綴り差＋種タグ） |
| 18 | マイコプラズマ症 Mycoplasmosis | + Mycoplasma Infection | 0008 ← 0185 | ✏️ 種タグ同義。M. agassizii URTD(0166) も同一菌属＝統合候補（要確認） |
| 19 | コクシジウム症 Coccidia Infection | + Coccidia | 0018 ← 0195 | ✏️ 種タグ違い。**核内コクシジウム TINC(0013) は別病原体＝分離**（C参照） |
| 20 | 陰茎脱出 Penile Prolapse | + Penile/Hemipenal Prolapse | 0057 ← 0212 | ✏️ 陰茎/半陰茎脱＝同一。他脱出臓器とは分離（C参照） |
| 21 | 総排泄腔脱 Cloacal Prolapse | + Rectal/Cloacal Prolapse | 0056 ← 0222 | ✏️ 直腸/総排泄腔脱＝同一 |
| 22 | 嘴の過成長・不正咬合 Beak Overgrowth/Malocclusion | + Beak Overgrowth | 0035 ← 0170 | 種タグ違い。爪過成長(0171)は別 |
| 23 | 卵関連体腔炎 Egg-related Coelomitis | + Egg Yolk Coelomitis | 0115 ← 0211 | ✏️ 卵黄性体腔炎＝同一。一般腹膜炎(0067)・腹水(0088)は別（C参照） |

**統合対象レコード**: 24件（firm 13件・✏️ 要確認 11件 — 下記集計参照）。

---

## C. 分離維持（統合しない推奨）
| 疾患ペア | id | 論点 |
|---|---|---|
| 痛風 内臓型 / 関節型 | 0042,0205 / 0041,0206 | 内臓型＝尿酸塩の内臓沈着・予後不良 vs 関節型＝関節沈着。別病態・別予後 |
| 骨折 四肢 / 甲羅 / 脊椎 | 0092 / 0002,0233 / 0139 | 発生部位・整復法が別。種タグ dup は各部位内で統合（B15） |
| 卵胞停滞 排卵前 / 慢性 / 排卵後卵停滞 / 生殖停滞 | 0044 / 0116,0178 / 0210 / 0177 | 排卵前後で病態が別。慢性型のみ統合（B11）、汎用「生殖停滞」は上位概念 |
| 膿瘍 皮下 / 耳 / 甲羅 / 眼周囲 / 眼鏡鱗下 | 0050 / 0051 / 0112 / 0037 / 0228 | 発生部位別で治療・予後が異なる。一般膿瘍(0201)のみ皮下へ（B5） |
| コクシジウム TINC核内 / 一般コクシジウム | 0013 / 0018,0195 | TINC＝核内コクシジア（重症・全身性）vs 腸管コクシジウム。別病原体・別重症度 |
| 中毒 亜鉛 / 鉛 / イベルメクチン / メトロニダゾール / 一般 | 0125 / 0126 / 0127 / 0128 / 0066 | 起因物質別で機序・解毒が別 |
| ヘルペス 一般 / カメHV1 / カメHV2 / リクガメHV | 0010 / 0095 / 0096 / 0165 | 型別に病原性が異なる。※0165 はカメHVの種タグ同義の可能性（✏️、クロス参照） |
| 脱出 総排泄腔 / 陰茎 / 腸 / 膀胱 | 0056 / 0057 / 0078 / 0157 | 脱出臓器別。種タグ dup は各臓器内で統合（B20/B21） |
| 腸閉塞 / 腸捻転 / 消化管閉塞(便秘) / 消化管部分閉塞 | 0218 / 0144 / 0029 / 0275 | 機序別（obstruction / volvulus / impaction）。Ileus 相当は非存在だが obstruction と volvulus は区別維持 |
| 欠乏症 ビタミンA / D3 / C / カルシウム / 紫外線 / ビオチン / タンパク質 | 0023 / 0025 / 0151 / 0072 / 0134 / 0135 / 0136 | 栄養素別で別疾患（種タグ dup のみ B2/B7 で統合） |

---

## クロスクラスタ注意
- **膀胱結石が4〜5ラベルに分散**: 一般 0040（A で 0209 統合）／尿酸塩型 0158・0176（B14 で 0176→0158）／リクガメ尿石症
  0163（`tortoi` cluster, リクガメ尿石症（膀胱結石））。リクガメの膀胱結石は大半が**尿酸塩型**のため、
  尿酸塩型(0158)を一般(0040)へ集約するか、0163 を 0040 へ種タグ統合するかは獣医判断（✏️、B外）。
- **ヘルペス4クラスタ**: リクガメHV(0165) は カメHV1/2(0095/0096) の種タグ同義の可能性。型が特定できれば統合、
  不明なら分離維持。一般ヘルペス(0010) とは別扱い。
- **臓器×病因のテンプレート合成エントリ**: 呼吸器(0276〜0283)・消化管(0268〜0275)・肝(0263〜0267)・皮膚(0284〜0287) を
  「細菌/ウイルス/真菌/寄生虫/腫瘍/炎症」で機械的に分割した（リクガメ）タグ付きエントリが多数。病因別には別だが
  低情報量の合成疾患。**本ワークシートでは統合非推奨（C相当）**、データモデル整理の候補として別途要検討。
- **ガード確認**: Proptosis / Exophthalmos 対は非存在。Dermatophytosis(0187 真菌) はあるが Dermatophilosis(細菌) 非存在＝
  誤ラベルなし。Ileus / Intestinal Obstruction は obstruction(0218) と volvulus(0144)・impaction(0029) を分離維持（上記C）。

## 集計
- **A（追認）**: 9統合（適用済み・279 served）。
- **B（承認で適用）**: 23行。統合対象 **24レコード**（firm 13件＝B1,2,3,4,6,7,8,10,12,13,14,15,22；✏️ 要確認 11件＝B5,9,11,16,18,19,20,21,23 各1＋B17 の2件）。
  全承認で **279 → ≈255 served**。firm のみなら **≈266**。
- **C（分離維持）**: 痛風型別・骨折部位別・卵胞停滞病期別・膿瘍部位別・TINC/コクシジウム・中毒起因物質別・ヘルペス型別・脱出臓器別・腸閉塞機序別・欠乏症栄養素別。
- 適用: `_CURATED_MERGE["tortoise"]` に承認行を追記 → `build_canonical.py tortoise --apply`。**未適用。**
