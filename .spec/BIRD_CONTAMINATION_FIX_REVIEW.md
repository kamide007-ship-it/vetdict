# Bird cross-species 汚染 修正ワークシート（提示のみ・🟡未適用）

> ✅ **適用済み（2026-07-22・獣医師承認「AB採用」）**: A（ラベル置換）+ B（臨床ドラフト）を scripts/quality/apply_cross_species_fix.py で当該モジュールに反映。scan_cross_species.py 実測で本種 0 件。バックアップ backups/2026-07-22-0845/。冪等・可逆。C（T106投与量公開）は承認外のため未実行。

対象: `scan_cross_species.py` が検出した **bird 13フィールド（cross-class 5・within-class 8）**。
種別1バッチ提示 → 承認 → 適用。**本ドキュメントは read-only・データ非改変。** bird の自種ラベルは「鳥」。

## 修正タイプの凡例
- **L**: `<他種>における` の種名ラベルのみ誤り（→「鳥」）。内容は鳥に妥当。
- **T**: `pathophysiology_ja` が全種共通テンプレ＋誤ラベル。最小＝ラベル置換／理想＝鳥特異。
- **C**: 別クラスの臨床記述コピー。獣医レビュー必須。

## 修正対象ファイル
全レコードとも **module `api/species/bird_diseases.py` のみ**（JSONオーバーレイ無し）。

---

## cross-class（優先・5フィールド）

### bird_0023 — カンジダ症（Candidiasis）
- causes_ja **T**: 「**両生類における**カンジダ症の原因: 胞子吸入、直接接種、粘膜コロニー形成…」→ ラベル「鳥」。
  理想（要獣医レビュー）: 鳥カンジダは *Candida albicans* のそ嚢（crop）過剰増殖が主。免疫抑制・長期抗菌薬・雛の挿し餌で好発。
- pathophysiology_ja **T**: 「…**両生類における**真菌感染症である。」（generic 真菌テンプレ）→ ラベル「鳥」／理想＝そ嚢炎主体の病態。

### bird_0026 — ムコール症（Mucormycosis / Zygomycosis）
- causes_ja **L**: 「**トカゲにおける**ムコール症の原因: 接合菌による肉芽腫性疾患。」→ ラベル「鳥」（内容は簡潔だが妥当）。
- pathophysiology_ja **T**: generic 真菌テンプレ＋トカゲ → ラベル「鳥」。

### bird_0073 — 卵詰まり（Egg Binding / Dystocia）
- pathophysiology_ja **T**: 「卵詰まり（難産）は**両生類における**生殖器疾患である…」（generic 生殖テンプレ）→ ラベル「鳥」。
  理想（要獣医レビュー）: 産卵鳥の卵停滞は低Ca・肥満・卵形成異常・寒冷が誘因、総排泄腔閉塞→虚脱・敗血症の病態。

---

## within-class（ラベル主体・8フィールド）

### bird_0040 — 総排泄腔乳頭腫症（Cloacal Papillomatosis）
- causes_ja **L**: 「**オウム**における…ウイルス病原体による感染…」→ ラベル「鳥」（内容 generic ウイルス、鳥に妥当）。

### bird_0104 — アトキソプラズマ症（Atoxoplasmosis）
- treatment_ja **L/T**: 「**インコ**における…適切な駆虫薬…」→ ラベル「鳥」。⚠️ 末尾 `[ECVN:Block]` は不改変。
- causes_ja **L**: 「**インコ**における…イソスポラ（アトキソプラズマ）…小型鳥やインコに発症。」→ ラベル「鳥」（Atoxoplasma はスズメ目/カナリアで重要。「小型鳥」記述は妥当）。
- pathophysiology_ja **T**: generic 寄生虫テンプレ＋インコ → ラベル「鳥」。

### bird_0177 — 鳥腎症（Avian Nephropathy）
- causes_ja **L**: 「**オウム**における鳥腎症の原因: 進行性腎疾患による腎不全。」→ ラベル「鳥」。
- pathophysiology_ja **T**: generic 腎テンプレ＋オウム → ラベル「鳥」。

### bird_0193 — 煙吸入症（Smoke Inhalation）
- causes_ja **L**: 「**インコ**における煙吸入症の原因: 煙や煙霧の吸入による呼吸器損傷。」→ ラベル「鳥」。
- pathophysiology_ja **T**: generic 呼吸器テンプレ＋インコ → ラベル「鳥」。
  （任意の獣医追記: 鳥は気嚢システムのため煙・エアロゾル〈PTFE 等〉に極めて脆弱で致死的になりやすい。）

---

## 適用手順（承認後・🟡）
1. バックアップ: `api/species/bird_diseases.py` を `backups/YYYY-MM-DD-HHMM/` へ。
2. 承認行のみ patch。ECVN ブロックは不改変。
3. `scan_cross_species.py` 再実行で bird 0件を確認。name 不変＝検索インデックス再生成不要。冪等性確認。

## 承認を求める項目
- 各フィールド ✅/❌/✏️。**L（ラベル置換）7〜8件は一括承認可**。**T の書き換え・cross-class 3疾患（Candidiasis/Mucormycosis/Egg Binding）の病態記述は獣医レビュー必須**。
