# ShowDog 技術仕様書 (Architecture Document)

Version 4.2.1 | 2026-03-06 | 引き継ぎ用技術文書

---

## 1. システム概要

ShowDogは犬のコンフォメーション評価・健康管理・遺伝子解析・診察記録を統合したWebプラットフォームです。

```
┌─────────────────────────────────────────────────────┐
│                    Client (Browser)                   │
│  Vanilla HTML/CSS/JS · PWA · Service Worker          │
└──────────────┬───────────────────────┬───────────────┘
               │ HTTPS                 │ WebSocket(SSE)
┌──────────────▼───────────────────────▼───────────────┐
│              Reverse Proxy (Render)                    │
└──────────────┬───────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────┐
│         Gunicorn (2 workers × 2 threads)              │
│  ┌─────────────────────────────────────────────────┐ │
│  │              Flask Application                    │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │ │
│  │  │ Auth     │ │ Analysis │ │ Health/Genetic    │ │ │
│  │  │ Module   │ │ Pipeline │ │ Modules           │ │ │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────────────┘ │ │
│  │       │            │            │                 │ │
│  │  ┌────▼────────────▼────────────▼─────┐          │ │
│  │  │         Database Layer              │          │ │
│  │  │    (SQLite / PostgreSQL dual)       │          │ │
│  │  └────────────────────────────────────┘          │ │
│  └─────────────────────────────────────────────────┘ │
│         │                    │                        │
│    ┌────▼──────┐       ┌────▼──────┐                 │
│    │ Claude    │       │ OpenAI    │                 │
│    │ API       │       │ API       │                 │
│    │ (Primary) │       │ (Fallback)│                 │
│    └───────────┘       └───────────┘                 │
└──────────────────────────────────────────────────────┘
```

---

## 2. バックエンド アーキテクチャ

### 2.1 エントリーポイント

| ファイル | 役割 |
|---------|------|
| `app.py` | エントリーポイント。`api.showdog_api.app` を import して起動 |
| `api/showdog_api.py` | Flask アプリ本体（6,065行）。全50+ルートを定義 |
| `Procfile` | Render用。`gunicorn api.showdog_api:app` |

### 2.2 モジュール依存関係

```
showdog_api.py (メインアプリ)
├── database.py          # DB CRUD（SQLite/PostgreSQL）
├── scoring.py           # ShowScore Engine（決定論的コア）
├── local_analysis.py    # OpenCV/Pillow 画像・動画解析
├── breeds.py            # 360犬種マスタデータ
├── breed_coefficients.py # 犬種別評価係数
├── health_checker.py    # Blueprint: /api/health-check/*
├── diagnostic_chat.py   # Blueprint: /api/diagnostic-chat/*
├── passport.py          # Blueprint: /api/passport/*
├── genetic_scoring.py   # 遺伝子解析・COI
├── growth_prediction.py # 成長予測モデル
├── pose_estimation.py   # 3D骨格推定
├── judge_validation.py  # 審査一致性検証
├── finetuning.py        # モデルファインチューニング
├── config_constants.py  # 定数（タイムアウト・レート制限等）
├── errors.py            # カスタム例外（AnalysisError等）
├── validation.py        # 内部整合性検証（5層バリデーション）
└── reco3_photo_video.py # RECO3 AI整合性チェック
```

全モジュールは **graceful degradation** 設計。importに失敗しても `*_AVAILABLE = False` フラグでフォールバックし、コア機能は動作継続。

### 2.3 データベース

#### デュアルバックエンド (`database.py`)

```python
# 環境変数 DATABASE_URL の有無で自動切替
if DATABASE_URL contains 'postgres':
    → PostgreSQL (psycopg2, ThreadedConnectionPool 1-10)
else:
    → SQLite (data/showdog.db)
```

PostgreSQL互換レイヤー: `_PGCursorWrapper` が `?` → `%s` 変換、`datetime('now')` → `NOW()` 変換、`INSERT ... RETURNING id` 自動付加を行う。

#### テーブル構成

| テーブル | 主要カラム | 用途 |
|---------|-----------|------|
| `users` | email, password_hash, subscription_plan | ユーザー管理 |
| `sessions` | token_hash, expires_at | セッション（SHA-256ハッシュ保存） |
| `dogs` | user_id, name, breed_id, birth_date, weight | 犬プロフィール |
| `analyses` | dog_id, overall_score, results_json | 解析結果 |
| `audit_logs` | algorithm_version, weights_hash, final_score | アルゴリズム監査証跡 |
| `dog_medical_records` | microchip_number, owner_name | 医療記録 |
| `dog_export_applications` | destination_country, embarkation_date | 輸出申請 |
| `password_reset_tokens` | token, expires_at, used | パスワードリセット |

マイグレーション: `init_db()` 内で `ALTER TABLE ADD COLUMN` によるインクリメンタル移行。

### 2.4 認証フロー

```
[ユーザー] → POST /api/auth/login {email, password}
   → verify_user(email, password)  # werkzeug check_password_hash
   → create_session(user_id)       # secrets.token_urlsafe(32)
   → SHA-256 ハッシュをDBに保存
   → Set-Cookie: session_token (HttpOnly, Secure, SameSite=Lax)
   → Response: {token, csrf_token}

[以降のリクエスト]
   → Authorization: Bearer <token>  (SPA)
   → または Cookie: session_token   (ブラウザ)
   → verify_session(token)
      → SHA-256(token) をDBで照合
      → expires_at 確認
   → request.current_user = user
```

レート制限:
- グローバル: 200/日, 50/時 (Flask-Limiter, IP単位)
- 認証: 5回/10分 (IP+email, カスタム実装)

### 2.5 ShowScore Engine (`scoring.py`)

```
Layer 1: 決定論的スコアリング（アルゴリズム主導）
  Base = Σ(Axis_i × Weight_i) + AgeAdjustment
    骨格(0.25) + 歩様(0.25) + 筋肉(0.20) + 被毛(0.20) + 気質(0.10) = 1.00
    WEIGHTS_HASH = SHA-256 でハッシュ化 → 改ざん検出

Layer 2: AI補正（AI伴走）
  犬種別感度プロファイル → 360犬種×5軸のマトリクス
  AI_Correction = Σ(axis_correction × breed_sensitivity)
  cap = ±8点  # 過補正防止

Layer 3: 検証
  信頼度 = f(data_completeness, consistency, sub_score_depth)
  軸間整合性チェック（異常パターン検出）

出力:
  final_score: 0-100
  grade: S(90+) / A+(80+) / A(70+) / B+(60+) / B(50+) / C(<50)
  fci_grade: Excellent / Very Good / Good / Sufficient / Disqualify
```

### 2.6 解析パイプライン

```
POST /api/analyze-comprehensive-stream

[1] 写真アップロード → UUID保存 → 拡張子/サイズ検証
[2] 画像圧縮 → base64エンコード
[3] SSE開始（event: progress）

[4] 写真解析（並列）:
    ├── OpenCV 骨格解析 → structure score + sub_scores
    │   └── 角度検出 → 犬種別理想値との偏差スコア
    └── OpenCV/Pillow 被毛解析 → coat score + sub_scores
        └── テクスチャ/ボリューム/手入れ状態

[5] 動画解析（ある場合）:
    ├── ffmpeg変換（MOV→MP4）
    ├── OpenCV フレーム抽出（12フレーム）
    ├── 動的区間選抜 → 安定歩行区間
    ├── 歩様解析 → gait score (stride, balance, fluidity)
    └── 気質解析 → temperament score

[6] AI Vision API 呼び出し（Claude/OpenAI）:
    └── 犬種特性を考慮した詳細評価 → JSON応答

[7] ShowScore Engine:
    └── Layer1 算出 → Layer2 AI補正 → Layer3 検証

[8] DB保存 + 監査ログ
[9] SSE送信（event: result）
```

### 2.7 セキュリティ実装

| 対策 | 実装場所 | 方式 |
|------|---------|------|
| SQL Injection | database.py 全関数 | パラメータ化クエリ (`?` プレースホルダ) |
| パスワード | database.py `create_user` | `generate_password_hash()` |
| セッション | database.py `create_session` | `secrets.token_urlsafe(32)` + SHA-256ハッシュ保存 |
| Cookie | showdog_api.py `_set_session_cookie` | HttpOnly, Secure, SameSite=Lax |
| CORS | showdog_api.py L492-507 | デフォルト無効（同一オリジンのみ） |
| セキュリティヘッダ | showdog_api.py `@app.after_request` | HSTS, CSP, X-Content-Type-Options, X-Frame-Options |
| レート制限 | showdog_api.py L532-566 | Flask-Limiter + カスタムIP+email制限 |
| ファイルアップロード | showdog_api.py 各解析エンドポイント | 拡張子ホワイトリスト + filetype検証 + UUID名 |
| SECRET_KEY | showdog_api.py L465-477 | 本番環境で未設定時 RuntimeError |

---

## 3. フロントエンド アーキテクチャ

### 3.1 ページ構成

| ページ | URL | 認証 | 主な機能 |
|--------|-----|:----:|---------|
| ランディング | `/` | - | サービス紹介、犬種選択 |
| ログイン | `/login.html` | - | 登録・ログイン・パスワードリセット |
| ダッシュボード | `/dashboard.html` | 要 | 犬一覧、クイック解析 |
| 犬詳細 | `/dog-detail.html?id=X` | 要 | プロフィール、解析、履歴、フード計算 |
| 症状チェック | `/health-check.html` | 要 | 60+項目チェックリスト |
| AI診断 | `/diagnostic-chat.html` | 要 | チャットベース診断 |
| パスポート | `/passport.html` | 要 | PDF生成、遺伝子テスト |
| 診察記録 | `/visit-form.html` | 要 | 診察データ入力・PDF |
| 犬種図鑑 | `/breeds.html` | - | 360犬種ブラウザ |
| 疾患DB | `/diseases.html` | - | 疾患一覧・症状マッピング |

### 3.2 共有モジュール

| ファイル | 役割 | グローバル名 |
|---------|------|-------------|
| `auth.js` | 認証状態管理・Navbar更新 | `SD_Auth` |
| `api.js` | API通信ラッパー | `SD_API` |
| `common.js` | ユーティリティ（escapeHtml等） | `SD_Utils` |
| `lang.js` | 多言語切替（ja/en） | `SD_i18n` |
| `tap-feedback.js` | モバイルUXフィードバック | - |
| `design-system.css` | 統一UIコンポーネント | CSS変数 |
| `sw.js` | Service Worker（PWA） | - |

### 3.3 デザインシステム

```css
/* 主要CSS変数 (design-system.css) */
--purple: #8B2FC0;
--gradient-brand: linear-gradient(135deg, #8B2FC0 0%, #5B7EC2 100%);
--radius-md: 12px;
--radius-xl: 20px;
--shadow-brand: 0 4px 24px rgba(139, 47, 192, 0.3);
```

グラスモーフィズムベース。モバイルファースト、レスポンシブ対応。

### 3.4 PWA

- `manifest.json`: アイコン (192/512px)、テーマカラー `#8B2FC0`
- `sw.js`: Cache-first戦略、オフラインフォールバック (`offline.html`)
- `CACHE_VERSION`: サーバーVERSIONと手動同期が必要

---

## 4. デプロイメント

### 4.1 CI/CD パイプライン

```
[PR作成 (claude/* ブランチ)]
    ↓
[GitHub Actions: auto-merge-deploy.yml]
    ├── Step 1: スモークテスト
    │   └── import チェック + /api/health 200確認
    ├── Step 2: 自動マージ (gh pr merge --auto)
    ├── Step 3: Render デプロイフック (curl)
    ├── Step 4: ヘルスチェック (120s待機 + 6回リトライ)
    └── Step 5: 失敗時自動ロールバック (git reset --hard + force push)
```

### 4.2 Render 構成

- **Runtime**: Python 3.11
- **Build**: `apt install ffmpeg && pip install -r requirements.txt`
- **Start**: `gunicorn api.showdog_api:app --workers 2 --threads 2 --timeout 120`
- **永続ディスク**: `/var/data` (SQLite DB)
- **ヘルスチェック**: `/api/health`

### 4.3 Docker

```dockerfile
FROM python:3.11-slim
RUN apt-get install -y ffmpeg
EXPOSE 5001
CMD ["python", "app.py"]
```

---

## 5. テスト

### 5.1 テスト実行

```bash
pytest tests/ -v              # 全テスト
pytest tests/ -x --tb=short   # 最初の失敗で停止
pytest tests/test_scoring.py  # 個別モジュール
```

### 5.2 テストカバレッジ

| カテゴリ | ファイル数 | テスト数 | 状態 |
|---------|-----------|---------|------|
| APIルート | 3 | ~120 | Pass |
| スコアリング | 1 | ~72 | Pass |
| ヘルスチェッカー | 2 | ~170 | Pass |
| 遺伝子解析 | 1 | ~45 | Pass |
| 成長予測 | 1 | ~30 | Pass |
| 姿勢推定 | 1 | ~35 | Pass |
| 審査検証 | 1 | ~25 | Pass |
| データベース | 1 | ~40 | Pass |
| 整合性検証 | 1 | ~63 | Pass |
| リファレンスデータ | 1 | ~200 | Pass |
| RECO エージェント | 5 | ~50 | Pass |
| その他 | 6 | ~220 | Pass |
| **合計** | **27** | **1076** | **0 fail, 6 skip** |

### 5.3 conftest.py のフィクスチャ

```python
@pytest.fixture
def client():      # Flask テストクライアント
def auth_token():  # 認証済みトークン
def sample_dog():  # テスト用犬データ
```

---

## 6. 既知の技術的負債と改善提案

### 6.1 優先度: 高

| # | 項目 | 詳細 | 工数目安 |
|---|------|------|---------|
| 1 | CSRF検証の有効化 | `_verify_csrf()` は定義済みだが未使用。状態変更エンドポイントに適用すべき | 2h |
| 2 | フロントエンドのXSSリスク | `innerHTML` に未エスケープデータ挿入箇所あり（app.js, treatment-plan.js等）。`SD_Utils.escapeHtml()` に統一 | 4h |
| 3 | 言語キーの不統一 | `localStorage` キーが `'lang'`, `'showdog_language'`, `'showdog_lang'` の3種混在。`'lang'` に統一 | 1h |
| 4 | アップロードファイルの清掃 | 処理後のファイル削除が不完全。バックグラウンドタスクまたは `finally` ブロック追加 | 2h |

### 6.2 優先度: 中

| # | 項目 | 詳細 |
|---|------|------|
| 5 | `escapeHtml` 重複 | 9箇所に独立実装。`SD_Utils.escapeHtml()` に統一 |
| 6 | 認証コード重複 | 各HTMLページが個別に認証チェック。`SD_Auth.requireAuth()` に統一 |
| 7 | showdog_api.py の分割 | 6,065行の単一ファイル。Blueprint化による分割を検討 |
| 8 | `requirements.txt` のロック | バージョン上限なし。`pip-compile` で lockfile 生成推奨 |
| 9 | CSP `unsafe-inline` 除去 | インラインスクリプト/スタイルを外部ファイル化 |
| 10 | Service Worker バージョン同期 | `sw.js` の `CACHE_VERSION` が手動管理 |

### 6.3 優先度: 低

| # | 項目 | 詳細 |
|---|------|------|
| 11 | レート制限のRedis化 | ワーカー間共有＋永続化 |
| 12 | パスワードポリシー強化 | 大文字・数字・記号の複雑性要件 |
| 13 | CSS @import → link | `design-system.css` のフォント読み込み最適化 |
| 14 | Dead code 除去 | `index.html` の `#authBar` 等 |

---

## 7. 運用ガイド

### 7.1 起動時の正常ログ

```
ShowDog Analysis Platform v4.2.1 - 2026-03-06
Algorithm Version: 2.2.0
Vision: Enabled (Primary: claude)
  Claude: Ready
  OpenAI: Ready
  Breeds: 360 FCI breeds loaded
Deterministic Scoring: Enabled
```

### 7.2 起動時警告（正常）

```
WARNING: Passport module not available      # reportlab未インストール
WARNING: OpenAI library not available       # openai未インストール
WARNING: ffmpeg: NOT FOUND                  # 動画変換不可
WARNING: SECRET_KEY is not set              # 開発環境のみ許容
```

### 7.3 ヘルスチェック

```bash
curl https://showdog-app.onrender.com/api/health
# → {"status": "healthy", "version": "4.2.1", "db_enabled": true, ...}
```

### 7.4 データベースバックアップ

```bash
# SQLite
cp data/showdog.db data/showdog_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### 7.5 環境変数チェック

```bash
curl https://showdog-app.onrender.com/api/auth/status
# → cookie/session/db の診断情報
```

---

## 8. 依存関係

### 必須

| パッケージ | バージョン | 用途 |
|-----------|-----------|------|
| flask | >=3.0 | Web フレームワーク |
| flask-cors | >=4.0 | CORS |
| flask-limiter | >=3.8 | レート制限 |
| gunicorn | >=21.2 | WSGIサーバー |
| werkzeug | >=3.0 | HTTPユーティリティ |
| python-dotenv | >=1.0 | 環境変数 |

### AI（任意）

| パッケージ | 用途 |
|-----------|------|
| anthropic | Claude API (AI伴走補正) |
| openai | OpenAI API (フォールバック) |

### 解析（任意）

| パッケージ | 用途 |
|-----------|------|
| opencv-python-headless | 画像・動画解析 |
| numpy | 数値計算 |
| pillow | 画像処理 (OpenCVフォールバック) |

### PDF（任意）

| パッケージ | 用途 |
|-----------|------|
| reportlab | PDF生成 |
| qrcode[pil] | QRコード |

### DB（任意）

| パッケージ | 用途 |
|-----------|------|
| psycopg2-binary | PostgreSQL接続 |

---

© 2026 ShowDog Analysis Platform. Internal Technical Document.
