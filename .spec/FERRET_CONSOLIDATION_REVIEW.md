# ferret 論理統合レビューワークシート（T103）— 提示のみ・未適用

> **状態**: プレゼンテーションのみ。**B/C はまだ適用していない**（あなたの ✅/❌ 待ち）。
> A（auto tier）は既に全16種と同じく serve 時に適用済み＝**追認の可否**を確認したい。
> 物理削除ゼロ・301リダイレクト・サイドカー編集で即ロールバック可。
> 元データ: ferret 277件 → auto 適用後 **267 served**。B を全承認すると **≈248 served**。

ferret の重複はほぼ「種タグ **（フェレット）** の二重登録」または「起因菌・部位の修飾語違い」で、
英語名は同一かほぼ同一。rabbit/cat/horse と同じく builder の strict key は自動統合しないため、
獣医レビュー承認後に curated 統合する候補として提示する。

---

## A. auto tier（既に serve 時に適用済み — 追認可否）10件
strict key（種タグ除去後に英語名が一致）で自動統合。全16種で同じ扱い。

| canonical | 統合済みエントリ | id |
|---|---|---|
| 副腎疾患 Adrenal Disease | + Adrenal Gland Disease | 0001 ← 0163 |
| ヘリコバクター胃炎 | + Helicobacter Gastritis | 0005 ← 0172 |
| 上部気道感染症 (URI) | + Upper Respiratory Infection | 0020 ← 0200 |
| 皮膚扁平上皮癌 Skin SCC | + Squamous Cell Carcinoma | 0026 ← 0180 |
| 皮膚糸状菌症 Ringworm | + Dermatophytosis | 0032 ← 0177 |
| 尿路結石症 Urolithiasis | + Urolithiasis | 0036 ← 0189 |
| 尿路感染症 (UTI) | + Urinary Tract Infection | 0039 ← 0188 |
| 腎嚢胞 Renal Cysts | + Renal Cyst | 0040 ← 0243 |
| 後肢不全麻痺 Posterior Paresis | + Posterior Paresis | 0045 ← 0208 |
| 骨折 Fractures | + Fracture | 0046 ← 0210 |

> ⚠️ 1点だけ確認: **皮膚扁平上皮癌 ← 一般 SCC**（0026←0180）は「一般 SCC＝皮膚型」と仮定した統合。
> フェレットの SCC は皮膚・口腔が主だが、一般 SCC を口腔/他部位として分けたい場合はここだけ ❌ にできます。

---

## B. curated 同一疾患候補（承認で統合 — 未適用）19クラスタ
大半は **（フェレット）タグの二重登録**。英語名同一 or 起因菌/部位の修飾違いで、臨床的に同一疾患。

| # | canonical（残す） | 統合候補 | id | 判定根拠 |
|--:|---|---|---|---|
| 1 | 副腎皮質機能亢進症（クッシング） | + Hyperadrenocorticism | 0003 ← 0193 | 同一・タグ違い |
| 2 | 炎症性腸疾患 (IBD) | + Inflammatory Bowel Disease | 0006 ← 0170 | 同一・タグ違い |
| 3 | 肝リピドーシス | + Hepatic Lipidosis | 0010 ← 0174 | 同一・タグ違い |
| 4 | 流行性カタル性腸炎 (ECE) | + ECE | 0012 ← 0166 | 同一（腸コロナ FRECV） |
| 5 | 拡張型心筋症 (DCM) | + Dilated Cardiomyopathy | 0014 ← 0183 | 同一・タグ違い |
| 6 | 肥大型心筋症 (HCM) | + Hypertrophic Cardiomyopathy | 0015 ← 0184 | 同一・タグ違い |
| 7 | インフルエンザ（ヒト由来） | + Influenza (Human Influenza) | 0018 ← 0164 | 同一 |
| 8 | 肥満細胞腫（皮膚型） | + Mast Cell Tumor | 0025 ← 0179 | フェレット MCT は皮膚型＝同一 |
| 9 | 耳ダニ症 (Otodectes) | + Ear Mites (Otodectes) | 0031 ← 0176 | 同一 |
| 10 | 皮膚糸状菌症 Ringworm【3-way】 | + Dermatophytosis (Microsporum) | 0032 ← 0274 | A の統合をさらに1件拡張 |
| 11 | 尾部脱毛（ラットテイル） | + Tail Alopecia (Adrenal) | 0034 ← 0178 | ラットテイル＝副腎性脱毛で同一 |
| 12 | 前立腺嚢胞（副腎関連） | + Prostatic Cyst | 0037 ← 0195 | 同一・タグ違い |
| 13 | 陰門腫脹（副腎関連） | + Vulvar Swelling (Adrenal) | 0042 ← 0196 | 同一・表記ゆれ |
| 14 | 前立腺疾患（副腎関連） | + Prostatic Disease | 0043 ← 0190 | 同一・タグ違い |
| 15 | アリューシャン病 (ADV) | + Aleutian Disease | 0050 ← 0165 | 同一・タグ違い |
| 16 | フェレット全身性コロナ (FRSCV) | + Ferret Systemic Coronavirus | 0054 ← 0167 | 同一（ECE=FRECV とは別クラスタ・分離維持） |
| 17 | 低血糖症（インスリノーマ関連） | + Hypoglycemia (Insulinoma) | 0066 ← 0194 | 同一・表記ゆれ |
| 18 | 増殖性大腸炎 | + Proliferative Colitis (Desulfovibrio) | 0078 ← 0129 | Desulfovibrio/Lawsonia＝起因菌名違いで同一 |
| 19 | 播種性特発性筋膜炎 (DIM) | + Disseminated Idiopathic Myofasciitis | 0082 ← 0213 | 同一・タグ違い |

> 注: #4 ECE(腸コロナ FRECV) と #16 FRSCV(全身性コロナ) は**別疾患**として分離維持。各クラスタ内は同一。

---

## C. 分離維持（要判断・統合しない推奨）2件
臨床的に別挙動の可能性があり、**あなたの指示があるまで統合しない**。

| 疾患ペア | id | 論点 |
|---|---|---|
| 消化管異物 / 消化管異物（**線状**） | 0004 / 0147 | 線状異物は腸重積・腸間膜切創リスクで**外科緊急度が異なる**。別エントリ維持が妥当か？ |
| 骨腫 / 骨腫（**頭蓋骨**） | 0088 / 0143 | フェレット骨腫は頭蓋が古典的。部位変異＝統合可か、部位別に残すか。 |

---

## 集計
- **A（追認）**: 10統合（適用済み・267 served）。SCC の1点のみ要確認。
- **B（承認で適用）**: 19クラスタ（うち #10 は3-way でA拡張）→ 承認すると ≈248 served。
- **C（分離維持）**: 2件（消化管異物・骨腫）。
- 適用方法（承認後）: `_CURATED_MERGES["ferret"]` に B の承認行を追記 → `build_canonical.py ferret --apply`
  （実行前に `backups/` へ自動ダンプ・冪等・即ロールバック可）。**このワークシートでは未適用。**
