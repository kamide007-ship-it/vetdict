# T103 — degu 論理統合パイロット（非破壊・可逆）

Branch: `claude/vibrant-newton-np00um`

## 何をしたか
degu の重複・非臨床エントリを **物理削除せず** 論理統合した。ソースの
`api/species/degu_diseases.py` は無改変。統合は **ロード時に適用されるサイドカー**
`api/data/canonical/degu.json`（獣医レビュー可能な単一アーティファクト）で表現。

- **201 → 181 served**（17クラスタを統合 = 17件を代表エントリへ集約 + 1件をアーカイブ）
- 代表エントリは**きれいな名前**を維持し、統合された重複から**豊富な内容を継承**（欠落/短いフィールドのみ補完、非破壊）
- 旧URL（統合された疾患のスラッグ）は代表スラッグへ **301 リダイレクト**（`/diseases/degu/<slug>`）→ URL は壊れない

## 適用範囲（保守的・安全側）
自動適用したのは **曖昧さのないもののみ**：
- **merges（17）**: `（デグー）` サフィックス付きの正書法重複（例: 「熱中症」← 「熱中症（呼吸器型）（デグー）」）。同一疾患。
- **archives（1）**: 「アルツハイマー様疾患」— デグーはアルツハイマー研究モデルであり、自然発生の臨床疾患ではない。

**レビュー保留（未適用）** — `review` セクションに記録、獣医判断待ち：
- 分割ファミリー **30**（`diabet×11`, `catara×5`, `absces×6` 等）— 臨床的に別疾患か過分割かは1件ずつ判断。
- ヒト医学移植 **2**（糖尿病性網膜症・糖尿病性足潰瘍）— 親疾患へ統合 or アーカイブを要判断。

## 実装（すべて可逆）
| 追加/変更 | 役割 |
|---|---|
| `api/data/canonical/degu.json` | 統合マップ（レビュー用アーティファクト） |
| `scripts/quality/build_canonical.py` | マップ生成器（冪等・バックアップ付き） |
| `api/species/canonical.py` | ロード時適用 `apply_canonical_map()` + `resolve_redirect()` |
| `api/species/helpers.py::enrich_diseases` | 差分診断/SPA解析パスに適用 |
| `api/vetdict_api.py::_load_diseases` | SEO詳細ページ/サイトマップに適用 |
| `api/health_checker.py::get_diseases` | SPA疾患ブラウザに適用 |
| `api/vetdict_api.py::disease_detail` | 旧スラッグ→代表スラッグ 301 リダイレクト |
| `tests/test_canonical_degu.py` | 回帰テスト7件 |

**元に戻す**: `api/data/canonical/degu.json` を削除 or 編集すれば即座に反映（サイドカー方式）。

## 未対応（follow-up）
- **SQLite ビルドパス**（`migrate_to_sqlite.py`）への canonical 適用。degu は低メモリ本番で
  モジュール直配信のため今回のパイロットは実サービング経路をカバー済み。SQLite をビルドする
  環境との一貫性のため、migrate にも同フックを追加予定（別バッチ）。
- 分割ファミリー/ヒト移植の統合は **獣医レビュー後**（`review` セクション参照）。
- スキーマ列（canonical_id/status/…）の SQLite ADD COLUMN は SQLite パス対応時に併せて追加。

## 他種への展開
`python3 -m scripts.quality.build_canonical <species> --apply` でマップ生成 →
獣医レビュー → コミット、で1種ずつ。マップが無い種は全パスで no-op。
