# snake（ヘビ）論理統合レビューワークシート（T103）— 提示のみ・未適用

> **状態**: プレゼンテーションのみ。**B/C はまだ適用していない**（✅/❌/✏️ 待ち）。
> A（auto tier）は serve 時に適用済み＝**追認の可否**を確認したい。物理削除ゼロ・301・即ロールバック可。
> 元データ: snake 248件 → auto 適用後 **243 served**。B（コア）を全承認すると **≈231 served**（family ✏️ も全承認なら ≈224）。

ヘビの重複は「英名の（ヘビ）種タグ分割」「無タグ正式名 vs 省略名」が中心。真菌症（SFD/Ophidiomycosis）は3件に分散、
痛風・脊椎・パラミクソ・鞭毛虫・半陰茎脱・ダニは exact_dup 外の family cluster にも真の重複が残る（クロス注意参照）。
熱傷（熱/化学）、痛風（内臓/関節）、拒食（非特異/行動/ストレス）、骨折（四肢/甲羅）は別病態として分離維持。

---

## A. auto tier（既に適用済み — 追認可否）5件
| canonical（残す） | 統合済み | id |
|---|---|---|
| 熱傷 Thermal Burns | + Burns（種タグ） | 0023 ← 0236 |
| 皮膚糸状菌症 Dermatophytosis | + Dermatophytosis（種タグ） | 0024 ← 0160 |
| 敗血症 Septicemia | + Septicemia（種タグ） | 0037 ← 0234 |
| 高体温症 Hyperthermia | + Hyperthermia（種タグ） | 0062 ← 0231 |
| 鉛中毒 Lead Toxicosis | + Lead Poisoning（種タグ） | 0108 ← 0232 |

---

## B. curated 同一疾患候補（承認で統合 — 未適用）
### コア（exact_dup・高信頼）
| # | canonical（残す） | 統合候補 | id | 判定根拠 |
|--:|---|---|---|---|
| 1 | 肺炎（下部呼吸器感染症） Pneumonia | + Pneumonia（種タグ） | 0008 ← 0201 | 種タグ違いで同一。0008 が richer/無タグ |
| 2 | ヘビダニ Snake Mites (Ophionyssus natricis) | + Snake Mite（種タグ） | 0012 ← 0148 | 単複＋種タグ違いで同一（同一起因ダニ） |
| 3 | アメーバ感染症 (Entamoeba invadens) | + Amoebic Infection（種タグ） | 0014 ← 0170 | 種タグ違いで同一 |
| 4 | 舌虫症 Pentastomid (Tongue Worms) | + Pentastomid Infection（種タグ） | 0016 ← 0167 | 種タグ違いで同一 |
| 5 | 水疱症（水疱性皮膚炎） Blister Disease | + Blister Disease（種タグ） | 0019 ← 0172 | 種タグ違いで同一 |
| 6 | スケイルロット（潰瘍性皮膚炎） Scale Rot | + Scale Rot（種タグ） | 0020 ← 0174 | 種タグ違いで同一。※Ulcerative Dermatitis 0178 はクロス注意 |
| 7 | 吻部擦過傷（ノーズラブ） Rostral Abrasion | + Rostral Abrasion（種タグ） | 0026 ← 0171 | 種タグ違いで同一 |
| 8 | 肝リピドーシス（脂肪肝） Hepatic Lipidosis | + Hepatic Lipidosis（種タグ） | 0030 ← 0190 | 種タグ違いで同一 |
| 9 | 排卵後卵停滞（スラグ残留） Post-ovulatory Egg Stasis | + Post-Ovulatory Egg Stasis（種タグ） | 0044 ← 0185 | 種タグ違いで同一 |
| 10 | ヘビ真菌症（SFD） Ophidiomyces ophiodiicola | + Ophidiomycosis/SFD + Ophidiomyces（種タグ） | 0082 ← 0142, 0143 | 3件とも同一 SFD（Ophidiomyces ophiodiicola）。0082 が最若番 |
| 11 | 条虫感染症 Cestode (Tapeworm) Infection | + Cestode Infection（種タグ） | 0088 ← 0165 | 種タグ違いで同一 |

### family cluster 由来（✏️要確認 — exact_dup 外だが name_ja ほぼ同一）
| # | canonical（残す） | 統合候補 | id | 判定根拠 |
|--:|---|---|---|---|
| 12 | パラミクソウイルス感染症 Paramyxovirus Infection | + Paramyxovirus（種タグ） | 0001 ← 0156 | 種タグ違いで同一。※Paramyxovirus Pneumonia 0145 は分離 |
| 13 | 脊椎骨症/脊椎症 Spinal Osteopathy/Spondylosis | + Spinal Osteopathy（種タグ） | 0051 ← 0151 | 種タグ違いで同一 |
| 14 | 半陰茎脱出 Hemipenal Prolapse | + Penile/Hemipenal Prolapse（種タグ） | 0045 ← 0187 | 種タグ違いで同一。※Retained Hemipenes 0153（停滞≠脱出）は分離 |
| 15 | 鞭毛虫感染症 Flagellate Protozoal Infection | + Flagellate Protozoan Infection（種タグ） | 0089 ← 0169 | 種タグ違いで同一。※Ciliate 0090 は分離 |
| 16 | ヘビダニ（#2 に統合先） | + Mite Infestation (Ophionyssus)（種タグ） | 0012 ← 0163 | #2 と同一起因（Ophionyssus）。#2 canonical に追加統合 |

---

## C. 分離維持（統合しない推奨）
| 疾患ペア | id | 論点 |
|---|---|---|
| サンシャインウイルス感染症 / サンシャインウイルス（ヘビ） | 0005 / 0147 | name_ja 同一だが病原体が別。0005=Sunshinevirus（パラミクソ近縁）、0147 括弧内=**Reptarenavirus＝封入体病(IBD)の起因体**。**ラベル誤り＝リネーム候補（0147 を IBD/Reptarenavirus 名に）であって統合しない** |
| 熱傷 Thermal Burns / 化学熱傷 Burns (Chemical) | 0023 / 0131 | 熱傷 vs 化学熱傷＝病因別。分離維持 |
| 食欲不振（非特異的） / 拒食（行動性） / ストレス性拒食 | 0033 / 0197 / 0241 | 非特異 vs 行動性 vs ストレス性＝病態別サブタイプ。分離維持 |
| 痛風（内臓型） / 痛風（関節型） | 0180 / 0181 | 内臓型 vs 関節型＝沈着部位で別病態。分離維持。※各々が 0049/0048 と重複（クロス注意） |
| 四肢骨折 Fracture (Limb) / 甲羅骨折 Fracture (Shell/Carapace) | 0211 / 0212 | 部位別で別だが**双方ともヘビに存在しない部位（四肢・甲羅）の汎用爬虫類テンプレ誤流入**。統合ではなく要リネーム/削除検討 |

---

## クロスクラスタ注意（exact_dup 外・family cluster 由来の要検討）
- **痛風の二重重複**: 内臓痛風 0049 ↔ 痛風（内臓型）0180、関節痛風 0048 ↔ 痛風（関節型）0181 が各々同一。
  → **0049 ← 0180 / 0048 ← 0181** を統合候補（✏️要確認）。統合後は内臓型/関節型の2疾患に整理。
- **上部呼吸器の3ラベル**: URI 0007 / Upper Respiratory Tract Disease 0202 / Respiratory Infection 0154。
  0007↔0202 は同一（上部気道）候補、0154 は下部含む汎用で分離寄り。獣医判断（✏️要確認）。
- **外傷・咬傷**: Trauma/Bite Wounds 0058 ↔ Bite Wounds 0177 は近同一（0058 は外傷を包含し広め）。
  Prey Bite Injury 0059・Wound Infection 0235 は別。0058↔0177 は ✏️要確認。
- **スケイルロット↔潰瘍性皮膚炎**: Scale Rot 0020 の括弧内＝Ulcerative Dermatitis、0178 Ulcerative Dermatitis（ヘビ）と同一機序の可能性。B#6 統合後に 0178 も横断検討（✏️要確認）。
- family_clusters（defici/hepati/absces/prolap/dermat 等）の残メンバーは部位・病因が異なる真の別疾患が大半（例: 肝リピドーシス/肝炎/肝腫瘍/肝線維症、口腔/皮下/スペクタクル下/耳/毒腺の各膿瘍）。統合対象外。

## 集計
- **A（追認）**: 5統合（適用済み・**243 served**）。
- **B（承認で適用）**: コア #1–#11（12レコード統合）で **≈231 served**。family ✏️ #12–#16＋クロス痛風/呼吸/咬傷まで全承認で **≈224 served**。
- **C（分離維持）**: 5組。うち 0147（Sunshine/Reptarena）と 0211/0212（四肢/甲羅）は**リネーム/削除の別対応候補**。
- 適用: `_CURATED_MERGE["snake"]` に承認行を追記 → `build_canonical.py snake --apply`。**未適用。**
