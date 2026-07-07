# T105/T106 — 治療投与量ドラフト & 公開ゲート（fail-closed）

Branch: `claude/vibrant-newton-np00um`

## 結論（重要）: 自動生成できる投与量ドラフトは 0 件 → SPEC の停止条件に従い停止
全21種を走査した結果、治療セクションに投与量パターンが無い疾患は **916件**。そのうち
**既存の院内コンテンツ（英語フィールド等）から出典付きで引ける投与量は 0 件**。
→ すべて外部ソーシングが必要 = 自動生成は**投与量の捏造**になる。

SPEC の失敗時挙動「投与量ドラフトの出典が過半引けない → 自動実行を止めて Kentaro に報告」に
**完全に該当**（100%）。よって**投与量は一切自動生成しない**。代わりに:
- **公開ゲート（T106）を fail-closed で実装**し、将来ドラフトができても獣医承認まで絶対に配信しない。
- **レビュー用ワークリスト（T105）を生成**（degu 25件、全て空・draft）。獣医が出典付き用量を記入 → 承認 → 公開。

## T106 公開ゲート（`api/species/treatment_overrides.py`）
- ドラフトは `api/data/treatment_overrides/<species>.json` に `review_status: draft/approved/published`。
- **`published` かつ `sources` がある行のみ配信**。`draft`/`approved`、および出典なし `published` は**配信拒否（fail-closed）**。
- 配信3パス（`enrich_diseases` / `_load_diseases` / `get_diseases`）に適用。canonical の後段。
- **自動公開は構造的に不可能**：公開は人間が `review_status=published` + `sources` 記入で行う操作のみ。

## T105 ドラフト生成器（`scripts/quality/build_treatment_drafts.py`）
- 投与量欠落疾患をワークリスト化（`review_status: draft`、`treatment_ja: ""`、`sources: []`）。**用量は生成しない**。
- 院内英語フィールドに用量がある場合のみ `en_reference`（翻訳+検証用）として提示。degu は該当0。
- 冪等: 既存の人手編集（非draft or 用量/出典記入済み）は上書きしない。バックアップ付き。
- バッチの過半が外部ソーシング必要なら停止条件を報告。

## 検証
- 公開ゲート回帰テスト `tests/test_treatment_publish_gate.py` 6件:
  draft/approved 非配信、出典なし published 拒否、出典あり published 配信、no-map no-op、degu ワークリストは何も公開しない。
- disease/API スイート 263件 pass。ruff 通過。

## Kentaro への依頼（公開に必要な人手作業）
1. `api/data/treatment_overrides/<species>.json` の各エントリに **出典付き投与量**（`treatment_ja` + `sources`）を記入。
2. レビュー完了後 `review_status` を `published` に。→ 次回配信から反映。
3. degu 25件が最初のバッチ（`api/data/treatment_overrides/degu.json`）。他種は同ジェネレーターで生成可。

**PubMed 連携（任意の補助）**: 候補文献の自動取得は可能だが、用量の自動生成は安全上行わない
（用量は必ず獣医が出典と照合して記入）。
