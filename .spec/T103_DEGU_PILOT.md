# T103 — 論理統合（非破壊・可逆）— degu パイロット + 全種展開

Branch: `claude/vibrant-newton-np00um`

## 何をしたか
重複・非臨床エントリを **物理削除せず** 論理統合。ソース（`api/species/*_diseases.py`）は無改変。
統合は **ロード時に適用されるサイドカー** `api/data/canonical/<species>.json`
（獣医レビュー可能な単一アーティファクト）で表現。

- 代表エントリは**きれいな名前**を維持し、統合された重複から**豊富な内容を継承**（欠落/短いフィールドのみ補完、非破壊）
- 旧URL（統合された疾患のスラッグ）は代表スラッグへ **301 リダイレクト** → URL は壊れない

## 厳格な自動適用基準（重要な安全設計）
検出器（`detect.py`）の「完全一致重複」は **括弧内をすべて除去して**クラスタ化するため、
臨床サブタイプを混同する（例: ウサギ「パスツレラ症（結膜型／生殖器型／敗血症型）」、
チンチラ「便秘（巨大結腸症）」）。これらを自動統合すると**臨床区別を失う**。

そこで自動適用は **種タグ「（<種>）」を除いても同一** の場合のみ（または完全同名）に限定：
- **auto-merge**: 「皮膚糸状菌症」←「皮膚糸状菌症（デグー）」、「鳥痘」←「鳥痘（鳥）」等。同一疾患。
- **auto-archive**: **名前が明示的にモデルを宣言**する場合のみ（「様疾患」「-like」「model」）。
  例: degu「アルツハイマー様疾患」。**キーワード一致だけでは archive しない**
  （例: 「馬パーキンソニズム」は黄色スターシスル中毒による実疾患 → review 送り、誤 archive 回避）。

**レビュー保留（未適用・`review` セクション）** — 獣医判断待ち：
- `oversplit_subtypes`: 括弧付きサブタイプ（（慢性）（敗血症型）等）— サブタイプか重複か1件ずつ判断。
- `split_families`: 分割ファミリー（`diabet×11` 等）。
- `nonclinical_transplants`: ヒト医学移植・キーワード誤検出候補（網膜症・足潰瘍・馬パーキンソニズム等）。

## 全種展開の実績（厳格基準）
`python3 -m scripts.quality.build_canonical <species> --apply` で17種にマップ生成。
DB全体で **176件を非破壊統合 + 1件 archive**（degu Alzheimer）。cat/rabbit/fish/horse は
安全自動統合ゼロ（全て subtype 差 → review）。degu は 8 merges + 1 archive（201→192 served）。

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
