# Reptile (generic) cross-species 汚染 修正ワークシート（提示のみ・🟡未適用）

対象: `scan_cross_species.py` が検出した **reptile 3フィールド（within-class 3）**。
「reptile」は汎用爬虫類バケツ。トカゲ（lizard）⊂爬虫類だが、generic reptile レコードに
「トカゲにおける」ラベルは不適切。**本ドキュメントは read-only・データ非改変。** 自種ラベルは「爬虫類」。

## 修正対象ファイル
全レコードとも **module `api/species/reptile_diseases.py` のみ**（JSONオーバーレイ無し）。

---

## reptile_0121 — イベルメクチン中毒（Ivermectin Toxicosis）
- description_ja: 「特に**カメや小型トカゲにおける**イベルメクチン過剰投与による神経毒性。」
- 判定 **❌ 現状維持を推奨（＝スキャナの弱い within-class ヒット）**:
  「カメや小型トカゲ」は**感受性の高い亜群を列挙した記述**であり、種ラベルの誤りではない。
  イベルメクチンはカメ・小型トカゲで特に致死的という**臨床的に正しい記載**。改変不要。
  （厳密化したい場合のみ「爬虫類、特にカメや小型トカゲでは…」と主語を爬虫類に補う程度。）

---

## reptile_0143 — 慢性呼吸器疾患複合（Chronic Respiratory Disease Complex）
- causes_ja **L**: 「**トカゲにおける**慢性呼吸器疾患複合の原因: 多因子性慢性呼吸器疾患。」→ ラベル「爬虫類」。
- pathophysiology_ja **T**: 「…**トカゲにおける**呼吸器疾患である…」（generic 呼吸器テンプレ）→ ラベル「爬虫類」。
  （任意の獣医追記: 爬虫類は横隔膜を欠き、低POTZ・低湿度・低換気・ビタミンA欠乏が慢性気道感染を助長。）

---

## 適用手順（承認後・🟡）
1. バックアップ: `api/species/reptile_diseases.py`。 2. 承認行のみ patch。
3. `scan_cross_species.py` 再実行で reptile 0件（reptile_0121 を ❌ 維持とする場合は 1件残＝許容 or COMPARATIVE 拡張で除外）。

## 承認を求める項目
- reptile_0143 の L/T ラベル置換は一括承認可。
- reptile_0121 は **❌現状維持** を推奨（正しい亜群記述）。スキャナ側で「カメや小型トカゲ」の様な列挙を
  除外したい場合は COMPARATIVE 相当の許容パターン追加も可（read-only 調整）。
