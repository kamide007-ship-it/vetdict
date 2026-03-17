# VetDict 商用化計画（詳細版）

**作成日**: 2026-03-16
**対象**: VetDict v5.0.0
**目標**: 最低限の商用化レベルに到達する

---

## 全体構成

```
Step 1: セキュリティ修正（致命的）        ← 即座に対応
Step 2: インフラ・CI/CD整備              ← 商用運用の土台
Step 3: データ層の改善                    ← プロトタイプ脱却
Step 4: フロントエンド改善               ← 保守性・UX向上
Step 5: 商用化必須機能                    ← 法務・分析・SEO
```

---

## Step 1: セキュリティ修正（致命的）

### 1-1. APIキーの除去（.github/workflows/main.yml）

**現状**: Anthropic APIキー `sk-ant-api03-...` がファイルに平文で記載
**ファイル**: `.github/workflows/main.yml`

**対応**:
- `main.yml` の内容を手順書に書き換え、APIキーを完全に除去
- Anthropicコンソールで当該キーを失効（revoke）
- 新しいキーを発行し、GitHub Secrets に `ANTHROPIC_API_KEY` として登録
- git履歴にもキーが残るため、`git filter-branch` または BFG Repo-Cleaner で履歴からも除去を検討

**変更後の main.yml**:
```yaml
name: VetDict CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v --tb=short
```

### 1-2. デバッグモードのデフォルト値修正（api/debug_config.py）

**現状**: `os.getenv('FLASK_DEBUG', '1')` — デフォルトでデバッグON
**リスク**: 本番でFlask対話デバッガーが有効化 → リモートコード実行が可能

**修正**:
```python
def is_debug_mode_enabled():
    return os.getenv('FLASK_DEBUG', '0').strip().lower() in {'1', 'true', 'yes', 'on'}
```

### 1-3. シークレットキーのフォールバック除去（api/vetdict_api.py:43）

**現状**: `app.secret_key = os.getenv('SECRET_KEY') or os.getenv('FLASK_SECRET_KEY') or 'dev-key-change-me'`
**リスク**: 環境変数未設定時にセッション偽造が可能

**修正**:
```python
_secret = os.getenv('SECRET_KEY') or os.getenv('FLASK_SECRET_KEY')
if not _secret:
    raise RuntimeError(
        "SECRET_KEY environment variable is required. "
        "Set SECRET_KEY or FLASK_SECRET_KEY before starting the application."
    )
app.secret_key = _secret
```

### 1-4. 認証バイパスの修正（api/auth.py:258-260）

**現状**: `INTERNAL_API_TOKEN` 未設定時に全リクエストを認証なしで通過
**対応**: 警告ログを出力し、開発環境でのみ許可

**修正**:
```python
if not current_config.internal_token:
    if os.getenv('FLASK_DEBUG', '0').strip().lower() in {'1', 'true', 'yes', 'on'}:
        logger.warning("INTERNAL_API_TOKEN not set — allowing unauthenticated access (debug mode)")
        return f(*args, **kwargs)
    else:
        logger.error("INTERNAL_API_TOKEN not configured in production")
        return jsonify({'success': False, 'error': 'Server misconfiguration'}), 500
```

---

## Step 2: インフラ・CI/CD整備

### 2-1. 依存関係のバージョン固定

**現状**: `Flask>=2.3.0` のような緩い指定
**対応**: `pip freeze` で現在の環境を固定し、`requirements.lock` を作成

**requirements.txt（本番用）**:
```
Flask==3.1.1
flask-cors==5.0.1
Werkzeug==3.1.3
gunicorn==23.0.0
anthropic==0.49.0
```

**requirements-dev.txt（開発用）**:
```
-r requirements.txt
pytest==8.3.5
pytest-cov==6.1.1
ruff==0.9.10
```

### 2-2. CI/CDパイプライン（GitHub Actions）

**新規作成**: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install ruff
      - run: ruff check .

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: python -m pytest tests/ -v --tb=short --cov=api --cov-report=term-missing

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pip-audit
      - run: pip-audit -r requirements.txt
```

### 2-3. Dockerfile作成

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_DEBUG=0
ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120"]
```

**`.dockerignore`**:
```
.git
.github
__pycache__
tests/
docs/
*.pyc
.env
.env.example
```

---

## Step 3: データ層の改善

### 3-1. SQLiteへの移行

**目的**: JSONファイル＋Pythonモジュールからの脱却。デプロイなしでデータ更新可能に。

**新規ファイル**: `api/database.py`

**スキーマ設計**:
```sql
-- 疾患テーブル
CREATE TABLE diseases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    species TEXT NOT NULL,
    name_ja TEXT NOT NULL,
    name_en TEXT,
    description_ja TEXT,
    description_en TEXT,
    pathophysiology TEXT,
    causation TEXT,
    clinical_signs TEXT,        -- JSON array
    symptoms TEXT,              -- JSON array (症状タグ)
    diagnostic_procedures TEXT, -- JSON
    treatment TEXT,
    prognosis TEXT,
    prevention TEXT,
    onset_type TEXT,            -- acute/subacute/chronic
    age_stages TEXT,            -- JSON array
    breed_predispositions TEXT, -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_diseases_species ON diseases(species);
CREATE INDEX idx_diseases_name_ja ON diseases(name_ja);

-- 薬剤テーブル
CREATE TABLE drugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    species_data TEXT,          -- JSON: species-specific dosage/safety
    interactions TEXT,          -- JSON array
    contraindications TEXT,     -- JSON array
    references TEXT,            -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_drugs_name ON drugs(name);
CREATE INDEX idx_drugs_category ON drugs(category);
```

**移行スクリプト**: `scripts/migrate_to_sqlite.py`
- 既存のPythonモジュール（20種）とJSONファイルからデータを読み込み
- SQLiteデータベースに挿入
- データ整合性の検証（移行前後のレコード数一致確認）

**段階的移行**:
1. まずSQLiteに全データを投入し、読み取りAPIを新設
2. 既存のPythonモジュールベースのAPIと並行運用
3. 動作確認後、旧APIを廃止

### 3-2. データ管理API

```
POST   /api/admin/diseases          — 疾患追加
PUT    /api/admin/diseases/:id      — 疾患更新
DELETE /api/admin/diseases/:id      — 疾患削除
POST   /api/admin/drugs             — 薬剤追加
PUT    /api/admin/drugs/:id         — 薬剤更新
POST   /api/admin/import            — 一括インポート
```

※ 管理APIには `require_internal_api_access` デコレーターを適用

---

## Step 4: フロントエンド改善

### 4-1. HTMLファイルの分割

**現状**: `templates/index.html` — 1,548行（CSS 285行 + HTML 400行 + JS 850行）

**分割方針**:
```
templates/
  index.html              ← 骨格のみ（〜100行）
  _header.html            ← ヘッダー・ナビゲーション
  _hero.html              ← ヒーローセクション
  _checker.html           ← 症状チェッカー
  _database.html          ← 疾患データベース
  _chat.html              ← 診断チャット
  _drugs.html             ← 薬剤辞書
  _footer.html            ← フッター

static/
  css/
    main.css              ← インラインCSSを抽出（285行分）
    (既存6ファイルはそのまま)
  js/
    app.js                ← インラインJSを抽出・整理（850行分）
    i18n.js               ← 翻訳システム
    checker.js            ← 症状チェッカーロジック
    database.js           ← 疾患検索
    chat.js               ← チャットUI
    drugs.js              ← 薬剤辞書
    (既存6ファイルはそのまま)
```

**Flaskテンプレート化**:
```python
# Jinja2のincludeを使用
# index.html
{% include '_header.html' %}
{% include '_hero.html' %}
...
```

### 4-2. 最低限のビルド

- CSS/JSの結合・minify（Flask-Assets または手動ビルドスクリプト）
- 本番では結合済みファイルを配信
- 開発時は分割ファイルのまま作業

---

## Step 5: 商用化必須機能

### 5-1. 法務ページ

**新規作成**:
- `/terms` — 利用規約（獣医師法への言及、免責事項、データ利用条件）
- `/privacy` — プライバシーポリシー（個人情報保護法・GDPR対応の基本条項）

**内容のポイント**:
- 本サービスは診断を行うものではなく、獣医師の臨床判断を支援する参考ツールである旨
- 収集するデータの範囲（アクセスログ、検索クエリ等）
- データの保存期間・削除方針
- 第三者提供の有無

### 5-2. アクセス分析

**最小構成**: サーバーサイドの利用統計

```python
# api/analytics.py
# 以下の情報をSQLiteに記録（PII不要）:
# - エンドポイント別アクセス数
# - 種別検索頻度
# - 鑑別診断の使用回数
# - 日別・時間帯別トラフィック
```

**ダッシュボード**: `/api/admin/analytics` で基本統計を返すAPI

### 5-3. SEO・メタデータ

**index.html に追加**:
```html
<meta name="description" content="20種4,800以上の疾患に対応する獣医学鑑別診断プラットフォーム。症状から疾患候補を瞬時に特定。">
<meta property="og:title" content="VetDict — 獣医学疾患データベース">
<meta property="og:description" content="20動物種、4,800疾患、175薬剤。獣医師のための臨床意思決定支援ツール。">
<meta property="og:type" content="website">
<link rel="canonical" href="https://vetdict.com/">

<!-- 構造化データ -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "VetDict",
  "description": "多動物種対応 獣医学疾患データベース",
  "applicationCategory": "HealthApplication",
  "operatingSystem": "Web"
}
</script>
```

### 5-4. エラー監視

**最小構成**: 構造化ログ + 基本的なヘルスチェック強化

```python
# 既存の /api/health を強化
@app.route('/api/health')
def health():
    checks = {
        'database': check_db_connection(),
        'disk_space': check_disk_space(),
        'memory': check_memory_usage(),
    }
    status = 'healthy' if all(checks.values()) else 'degraded'
    return jsonify({'status': status, 'checks': checks, 'version': VERSION})
```

将来的にはSentry等の外部サービスを検討。

### 5-5. APIバージョニング

**対応**: 既存APIはそのまま動作させつつ、新APIは `/api/v1/` プレフィクスを追加

```python
# 既存: /api/analyze-symptoms（互換性維持）
# 新規: /api/v1/analyze-symptoms（バージョン管理対象）
```

---

## 実行順序と依存関係

```
Step 1 セキュリティ修正
 ├── 1-1 APIキー除去          ← 独立、即座に実行
 ├── 1-2 デバッグモード修正    ← 独立
 ├── 1-3 シークレットキー修正  ← 独立
 └── 1-4 認証バイパス修正      ← 独立
         │
Step 2 インフラ整備
 ├── 2-1 依存関係固定          ← Step 1完了後
 ├── 2-2 CI/CD構築            ← 2-1 に依存
 └── 2-3 Dockerfile           ← 2-1 に依存
         │
Step 3 データ層改善
 ├── 3-1 SQLite移行           ← Step 2完了後
 └── 3-2 管理API              ← 3-1 に依存
         │
Step 4 フロントエンド改善
 ├── 4-1 HTML分割             ← Step 2完了後（並行可）
 └── 4-2 ビルド整備           ← 4-1 に依存
         │
Step 5 商用化機能
 ├── 5-1 法務ページ           ← 独立（並行可）
 ├── 5-2 分析機能             ← Step 3 に依存
 ├── 5-3 SEO                 ← Step 4 に依存
 ├── 5-4 エラー監視           ← Step 2 に依存
 └── 5-5 APIバージョニング    ← Step 3 に依存
```

---

## 対象外（今回のスコープに含めないもの）

以下は商用化後のフェーズで対応:
- PostgreSQL移行（SQLiteで十分な規模の間は不要）
- マイクロサービス分割
- モバイルアプリ
- ユーザー登録・課金システム
- 多言語拡張（日英以外）
- 臨床検証・感度特異度測定
- コンテンツマーケティング・SNS展開

---

*本計画はVetDict v5.0.0のコードベース分析に基づきます。*
