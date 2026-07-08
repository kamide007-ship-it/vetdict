# T111 — 薬品リンク整合性修正（キーワード自動マッチのノイズ除去）

Branch: `claude/vibrant-newton-np00um`

## 問題
「治療に関連する薬品」（`find_drugs_for_disease` → `find_drugs_in_text`）と
サーバー側 `mentioned_drugs` / `_attach_mentioned_drugs` は、薬品名キーワードを
治療テキストに**単純部分一致**で拾う。2つの実害を確認：

1. **自社(ECVN)製品が「薬品」として混入**: 薬品辞書に ECVN 11製品が登録され、
   汎用な先頭語 `amino`（Amino Complete）・`canine`（Canine Vet …）・`kamide` が
   インデックス化。→ degu 糖尿病の関連薬品に **「Canine Vet Relax & CBD」** が出る等、
   PR 製品がエビデンス薬品リンクに漏れる（T107 の分離方針に反する）。
   `canine` は犬疾患テキスト全般に一致し広範囲を汚染。
2. **短キーワードの部分一致誤爆**: `iron`（Iron Dextran）が "env**iron**ment" に、
   `amino` が "amino acids" に一致。

## 修正（`api/drug_dictionary.py`）
- **ECVN/自社製品を薬品マッチャから除外**（`id` が `ecvn` で始まるものを索引しない）。
  製品は T107 の PR ブロックで別途表示されるため、エビデンス薬品リンクには出さない。
- **ラテン文字キーワードは単語境界マッチ**（`(?<![a-z0-9])kw(?![a-z0-9])`）。
  日本語キーワード（カタカナ）は識別性が高いため部分一致のまま。
- `find_drugs_in_text` を境界マッチャ `_DRUG_KEYWORD_MATCHERS` 経由に変更。
- サーバーの2マッチャ（`disease_detail` の `mentioned_drugs`、`_attach_mentioned_drugs`）も
  同じ `find_drugs_in_text` 経由に統一（ECVN除外・境界マッチが全経路で有効）。

## 効果（実測）
- degu 糖尿病 関連薬品: `['Canine Vet Relax & CBD', 'Insulin Glargine']` → **`['Insulin Glargine']`**。
- `environment` に Iron、`amino acids` に ECVN 製品が**もう一致しない**。
- 正規の薬品（amoxicillin, meloxicam 等）は引き続き一致。索引は依然 >100 件。

## テスト
- `tests/test_drug_link_integrity.py` 5件（ECVN除外・境界マッチ・正規一致維持・
  索引健全・degu糖尿病にPR製品なし）。
- 回帰: drug_dictionary / SEO / diagnostic / vetdict_api 計 **836件 pass**。ruff 通過。

## 補足（種別投与量の欠落について）
T108 は「治療に記載はあるが当該種の用量データが無い薬品」も57件/degu 検出するが、
その多くは**臨床的に妥当な薬品**（Glipizide→インスリン抵抗、Ofloxacin→結膜炎 等）で、
degu 用量が辞書に無いだけ。よって**除去せず維持**（除くと有用な薬品を隠す）。種別用量の
拡充は薬品辞書側の別タスク。本 T111 は「無関係な自社製品・誤爆の除去」に限定。
