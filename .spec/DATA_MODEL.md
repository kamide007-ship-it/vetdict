# VetDict データ格納形式 — 確定事項（実装前の必須確認）

> このドキュメントは「Postgres or 静的JSON」の確認結果。**検出器・修正器の
> コードはここで確定した形式に基づく。**

## 結論：**Postgres は存在しない。** 3層構造。

| 層 | 実体 | 役割 | 本番での状態 |
|---|---|---|---|
| **① Python モジュール** | `api/species/<species>_diseases.py` の `DISEASES`（馬のみ `DISEASE_DATABASE`） | **一次ソース・オブ・トゥルース**。全21種。degu は 201 エントリ | 常に存在 |
| **② JSON オーバーレイ** | `diseases_all_species.json`（98MB, フラットな list, 6,449 エントリ） | ①を `(species, name)` で実行時オーバーライド | 常に存在 |
| **③ SQLite（派生）** | `scripts/migrate_to_sqlite.py` がビルド時に①+②から生成 → `instance/vetdict.db` | 配信用の読み取り最適化DB | **512MB 本番ではマイグレーションをスキップ**（OOM回避）→ 空 → ①+② にフォールバック |

補助: `api/data/disease_search_index.json`（横断検索用の軽量名前インデックス）。

### degu の実データ経路（重要）
- **degu は JSON オーバーレイに 0 エントリ**。→ degu の配信内容 = **Python モジュール `api/species/degu_diseases.py` そのもの**。
- したがって degu の検出器はモジュールを読み、**degu の修正はモジュール `.py` に対して行う**（他種は JSON オーバーレイ側が優先されるため種ごとに要判断）。

## ID は「位置依存」— canonical_id 設計の最重要制約
`migrate_to_sqlite.py:81`:
```python
disease_id = d.get("id") or f"{species_key}_{i:04d}"
```
- 疾患エントリに **明示的 `id` フィールドは無い**（degu 全201件が `id` 無し）。
- ID は **list のインデックス由来**（`degu_0000`, `degu_0001`, …）。
- ⇒ **リストの並び替え・削除で既存URLが壊れる。** 物理削除が禁止なのはこのため。
- ⇒ 論理統合には「安定した明示的 `id`」の導入が前提。**まず全エントリに不変の
  `id`（またはスラッグ）を付与するマイグレーションが T103 の前提条件**になる。

## スキーマとマイグレーション方針
`api/database.py` の `diseases` テーブルは既に **冪等 ADD COLUMN** パターンを持つ
（`init_db()` 内 `ALTER TABLE diseases ADD COLUMN ...`）。追加予定カラム:

| カラム | 型 | 用途 |
|---|---|---|
| `canonical_id` | TEXT | 論理統合の代表ID（自分自身 or 統合先） |
| `status` | TEXT | `active` / `merged` / `archived`（default `active`） |
| `merged_into` | TEXT | 統合先 id（status=merged 時） |
| `merged_reason` | TEXT | 統合理由（監査用） |
| `aliases` | TEXT(JSON) | 旧名称・旧ID（リダイレクト解決用） |
| `evidence_grade` | TEXT | 出典グレード（治療ドラフト用） |
| `review_status` | TEXT | `draft` / `approved` / `published`（投与量レビュー用） |

- Python モジュール/JSON 側にも同等のキー（`canonical_id`, `status`, `merged_into`,
  `aliases`）を持たせ、**SQLite が空の本番でも論理統合が効く**ようにする。
- マイグレーション履歴は `schema_migrations` テーブルで管理（新規）。

## バックアップ方針（非機能要件）
改変系スクリプトは実行前に対象を `backups/YYYY-MM-DD-HHMM/` へダンプ:
- Python モジュール修正 → 対象 `.py` をコピー
- JSON 修正 → 対象種の抽出JSONをコピー
- SQLite 変更 → テーブルダンプ（該当種）
検出器（T101/T102/T104/…）は **読み取り専用**につきバックアップ不要。
