# フェーズ2 — schema_migrations + 不変ID凍結（🟡・非破壊・可逆）

Branch: `claude/vibrant-newton-e9sdex`

## 目的
論理統合(T103)の前提。位置依存ID（`{species}_{i:04d}`）を脱却し、疾患リストの
並び替え・削除で既存URLが壊れない状態にする。**現行IDを凍結**するため、今日の
配信IDは1件も変わらない（URL不変）。

## 実装（すべて追加・可逆）
| 追加/変更 | 役割 |
|---|---|
| `api/database.py` `schema_migrations` テーブル | 適用済みマイグレーションの台帳（`INSERT OR IGNORE`＝冪等） |
| `api/database.py` `_run_migrations` の `quality_cols` | 冪等 ADD COLUMN 7列: `canonical_id/status/merged_into/merged_reason/aliases/evidence_grade/review_status`（全て default NULL＝既存行に無影響） |
| `api/data/id_locks/<species>.json`（20種・6,434件） | `stable_key(name␟name_ja) → 凍結id` の append-only マップ |
| `api/species/id_locks.py::stable_id_for()` | 純関数リゾルバ（read-only・`lru_cache`）。lock無ければ位置idにフォールバック |
| `scripts/quality/build_id_locks.py` | 凍結マップ生成器（冪等・append-only・`--check`対応） |
| `scripts/migrate_to_sqlite.py` id採番2箇所 | generic + dog を `stable_id_for` 経由に（1行差分×2） |
| `tests/test_id_locks.py` | 純Python回帰テスト5件（flask不要） |

**馬（equine）は対象外** — dataclass に明示 `id` を既に保持し位置依存でない。

## 安全設計
- **append-only 凍結**: 既存キーのidは絶対に変更しない。新疾患のみ現行位置id（衝突時は
  content-hash id）を採番。→ 冪等（再生成で0件new）。
- **バイト同一**: lockは今日のidから生成されるため、全既存疾患で `stable_id_for` は
  現行idをそのまま返す。効果は**将来リストが並び替わった時**に発現。
- **可逆**: `api/data/id_locks/` を削除すれば位置依存idに即フォールバック。

## 検証（このブランチ・ローカル、flask/pytest無し環境）
- Part A: 一時DBに `init_db` を2回 → 7列全存在・ledger 2件・エラー無し（冪等）。
- Part B: degu で ①今日のid=バイト同一 ②リスト逆順時 base==reordered（198/199 は本来変動するidが pin）
  ③再生成0件new ④全20種で凍結id重複0。
- ruff check / format 通過。**フルスイートは CI で検証**（本環境は flask が Debian 競合で不可）。

## バックアップ（NFR）
`backups/YYYY-MM-DD-HHMM/` に編集前の `database.py` / `migrate_to_sqlite.py` を保存済み。

## 次（承認後）
- T103 を SQLite ビルドパスにも適用する際、`canonical_id/status/…` 列へ統合状態を書き込む
  （現状 canonical はサイドカー適用＝低メモリ本番のモジュール直配信で有効）。
- 他20種の統合レビュー（degu と同手順、獣医レビュー前提）。
