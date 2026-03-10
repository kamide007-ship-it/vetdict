# 疾患データベース拡張 + 本番監査 設計書（実装前・統合改訂版）

> 目的: 「全疾患で 病態生理 / 予防 / 治療 / 原因 / 予後 を引用付きで必須化」し、既存アプリを壊さず本番品質に到達させる。  
> 制約: 既存 route/URL、認証ロジック、フォーム識別子、既存計算ロジックは変更しない（差分のみ）。

---

## 1. 要件整理（実装機能リスト）

### 1-1. 必須機能
- 全疾患レコードに以下5セクションを必須フィールドとして追加/整備する。
  - `pathophysiology`（病態生理）
  - `prevention`（予防）
  - `treatment`（治療）
  - `etiology`（原因）
  - `prognosis`（予後）
- 各セクションに、提示済み文献 `[1]..[42]` の**出典番号配列**を必須で持たせる。
- APIレスポンスで、本文だけでなく**セクション単位の引用番号**を返す。
- UI（疾患データベース表示）で、5セクションを固定順で表示し、出典番号を併記する。
- バリデーションを導入し、以下を検出する。
  - 5セクション欠落
  - citation配列が空
  - citation番号がマスター外
  - 重複・不正型（文字列混入など）
- 監査ログを追加し、欠落データを把握可能にする。

### 1-2. 完了条件（DoD）
- 全speciesモジュールの全疾患エントリで、5セクション + citationsが有効。
- `/api/species-stats` の総疾患数に対して、スキーマ適合率100%。
- 既存の主要API (`/api/health`, `/api/species/<species>/symptoms`, `/api/analyze-symptoms`) の互換性維持。
- テストで「欠落レコードが1件でもあればfail」。

### 1-3. 不足情報（要確認）
1. 「引用」は逐語引用まで必要か、要約 + 出典番号でよいか。
2. 各疾患セクションの最小文字数（例: 120字以上）を設けるか。
3. 英語版（name_en/description_en）も同時に5セクション化するか。
4. 文献[14][15]のようなWeb資料は「取得日」固定を行うか。

---

## 2. コンポーネント設計（UI分割 / Props / State）

### 2-1. 追加/改修コンポーネント
- `DiseaseDetailPanel`
  - 役割: 疾患詳細の外枠。既存詳細描画を維持しつつ新5セクションを統合。
  - Props: `disease`, `referenceCatalog`, `lang`
  - State: `expandedSections`, `renderWarnings`

- `DiseaseSectionBlock`
  - 役割: 単一セクション（病態生理など）の本文 + 引用表示。
  - Props: `title`, `text`, `citations`, `referenceCatalog`
  - State: なし（純表示）

- `CitationChips`
  - 役割: `[1][2][27]` のような番号チップ表示。
  - Props: `citations`, `onSelect`
  - State: `activeCitation`

- `CitationDrawer`（任意）
  - 役割: 選択された文献の書誌情報を展開表示。
  - Props: `citationId`, `reference`
  - State: `isOpen`

### 2-2. 既存UI互換性ポリシー
- `templates/index.html` の既存ID・タブ構造は変更しない。
- 既存JS初期化に重複登録を入れない（イベント多重を禁止）。
- 表示追加は「疾患詳細の内部」に限定し、既存ナビを破壊しない。

---

## 3. データ設計・状態管理

### 3-1. データスキーマ（疾患）
```json
{
  "id": "canine_ckd",
  "name": "慢性腎臓病",
  "name_en": "Chronic Kidney Disease",
  "species": "dog",
  "sections": {
    "pathophysiology": { "text": "...", "citations": [1, 2, 27] },
    "prevention": { "text": "...", "citations": [7, 13] },
    "treatment": { "text": "...", "citations": [2, 12, 27] },
    "etiology": { "text": "...", "citations": [1, 2] },
    "prognosis": { "text": "...", "citations": [2, 27] }
  },
  "schema_version": "2.0"
}
```

### 3-2. 出典マスター
- サーバ側に `reference_catalog` を単一管理（番号→書誌）。
- 疾患レコードは番号のみ保持して重複文字列を持たない。
- `reference_catalog_version` を導入し、Renderキャッシュクリア後も不整合を防ぐ。

### 3-3. 状態管理
- 取得時: 疾患データを normalize → validate → render。
- 種別差異（`DISEASE_DATABASE` / `DISEASES`）は、`api/normalization.py`（実装予定）の正規化関数（例: `normalize_disease_record()`）で吸収し、読み込み時に共通 `sections` 形式へ変換する。
- 失敗時: UIに汎用警告、サーバに詳細ログ。
- APIは `warnings[]` を返せる形にして監査可能化。

---

## 4. 懸念点・エッジケース

### 4-1. 技術的懸念
- 種別ごとにデータ形式が異なり、正規化時に欠落が大量発生しうる。
- 馬疾患（`DISEASE_DATABASE`）と他種（`DISEASES`）で構造が異なる。
- 引用番号の手入力ミスにより、存在しない出典が混入しうる。

### 4-2. パフォーマンス
- 全件ロード時にバリデーションを毎回実行すると遅延。
  - 対策: 起動時プリチェック + キャッシュ済み検証結果を利用。

### 4-3. エラーハンドリング
- 欠落セクション: 表示を止めず「情報整備中」表示。
- citation不正: 対象セクションのみ警告表示 + 監査ログ。
- 外部依存失敗時（LLM/外部API）: 疾患DB閲覧機能は継続。

---

## 5. 全アプリ監査（現行コードに対する評価）

> 評価基準: A=問題なし / B=軽微修正 / C=本番不可レベル
> 以下の判定は**現行コードベースの監査結果**であり、この設計書自体の変更差分を指すものではない。

### 5-1. アーキテクチャ健全性: **B**
- 指摘1: `api/vetdict_api.py` に責務が集中（ルーティング + セキュリティヘッダ + 集計 + 静的配信）。分割不足。
- 指摘2: route定義が単一巨大ファイル化し、変更衝突リスクが高い。
- 修正案（コードレベル）:
```python
# api/routes/species.py に分離
species_bp = Blueprint("species", __name__)

@species_bp.route('/api/species-stats', methods=['GET'])  # 既存の decorator / auth 条件を維持
def api_species_stats():
    ...

# api/vetdict_api.py
app.register_blueprint(species_bp)
```

### 5-2. キャッシュ & 更新制御: **B**
- 指摘1: `/static/` は `max-age=3600`。ファイル名ハッシュ運用が未確認。
- 指摘2: Service Worker見当たらず（意図通りなら明示が必要）。
- 修正案:
```python
# 例: ビルド番号をレスポンスヘッダに埋め込み
response.headers['X-App-Build'] = BUILD
```

### 5-3. 認証 & 認可: **B**
- 指摘1: `INTERNAL_API_TOKEN` 未設定時、内部APIが実質オープンになる設計。
- 指摘2: IPベースのレート制限はNAT配下で誤制限/回避の両リスク。
- 修正案:
```python
if not expected_token:
    logger.error("INTERNAL_API_TOKEN is not configured")
    return jsonify({'success': False, 'error': 'Service temporarily unavailable', 'version': VERSION}), 503
```

### 5-4. セキュリティ: **B**
- 指摘1: `CORS(app)` がデフォルト許可（全オリジン）で広い。
- 指摘2: 入力バリデーションはエンドポイントごとに強弱がある。
- 修正案:
```python
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [origin.strip() for origin in os.getenv("CORS_ORIGINS", "https://vetdict.onrender.com").split(",")]
        }
    },
)
```

### 5-5. 例外耐性: **B**
- 指摘1: 広域 `except Exception: pass` が散見され、原因が埋もれる。
- 修正案:
```python
except (ImportError, AttributeError) as e:
    logger.warning("species import failed: %s", e)
```

### 5-6. パフォーマンス: **B**
- 指摘1: `/api/species-stats` で毎回 `importlib.import_module` と件数集計を行う。
- 修正案: 起動時にカタログを生成し、TTL付きキャッシュを返す。

### 5-7. UX安定性: **B**
- 指摘1: データ欠落時のユーザー向け理由表示が弱い（空配列返却中心）。
- 修正案: エラーコード + ユーザ文言の分離。

### 5-8. 本番可否判定: **B（条件付き可）**
- 重大バグ: **Yes（設定依存で内部APIがオープンになりうる）**
- 本番投入可否: **No（上記修正まで不可）**
- 技術的負債: **Yes（巨大ルートファイル、例外握りつぶし、入力検証の不均一）**

---

## 6. 実装前チェックリスト（本件適用）
- [x] 変更予定ファイル確認（`git status`）
- [x] DOMイベント重複候補確認（`DOMContentLoaded`, `setInterval`）
- [x] テンプレートID確認
- [x] ルーティング定義確認
- [x] DBスキーマ確認（`app.db` 不在のためスキップ: "app.db not found (schema check skipped)"）

---

## 7. 承認依頼（ここで停止）
この設計は、あなたの指示どおり**実装前の計画提示のみ**です。  
コード実装はまだ開始していません。  

**承認文言:** 「設計に合意します。実装を開始してください」  
この指示を受けてから、差分実装（データ正規化・引用必須化・バリデーション・テスト）に進みます。
