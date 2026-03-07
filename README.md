# ShowDog — Canine Intelligence Platform

**評価 × 健康 × 遺伝 × 記録 — 犬の生涯をAIで統合管理**

Powered by ShowScore Engine — アルゴリズムが主導、AIが伴走

Version 4.2.1 | Build 2026-03-06

---

## このアプリケーションの価値

### 世界に競合が存在しない

ショードッグのコンフォメーション評価、健康管理、遺伝子解析、診察記録を **一つのプラットフォームに統合した製品は世界に存在しません。**

既存サービスとの比較：

| 機能 | ShowDog | PetLooks | TTcare | C-BARQ | 従来の審査 |
|------|---------|----------|--------|--------|-----------|
| FCI基準コンフォメーション評価 | **5軸AI解析** | 外見のみ | なし | 行動のみ | 人間の主観 |
| 症状チェック・類症鑑別 | **43疾患DB** | なし | 一部 | なし | なし |
| 遺伝子解析・COI算出 | **8遺伝子型** | なし | なし | なし | なし |
| 繁殖ペア最適化 | **スコアリング** | なし | なし | なし | 経験則 |
| 国際ペットパスポートPDF | **自動生成** | なし | なし | なし | 手書き |
| 診察記録・PDF出力 | **60+チェック項目** | なし | なし | なし | 紙カルテ |
| 3D姿勢推定・骨格解析 | **17キーポイント** | なし | なし | なし | 目視 |
| 成長予測・発達追跡 | **3モデル** | なし | なし | なし | なし |
| 科学的根拠 | **18+査読済み論文** | なし | なし | 学術研究 | FCI基準のみ |

### 解決する課題

**ブリーダー・ハンドラーにとって：**
- ドッグショーの審査は人間の主観に依存 → **アルゴリズムによる再現性100%の客観的評価**
- 繁殖計画は経験と勘に頼る → **COI算出・遺伝子型解析による科学的な繁殖最適化**
- 犬の成長を定量的に追跡できない → **3モデルによる成長曲線予測とピーク年齢推定**

**飼い主にとって：**
- 愛犬の症状から病気を調べられない → **42+症状から43疾患をAIが自動鑑別、推奨検査リスト付き**
- 獣医に伝えたいことをまとめられない → **60+項目の診察記録を自動PDF化、そのまま獣医に提出**
- 海外渡航の書類準備が煩雑 → **国際ペットパスポートPDFをワンクリック生成**

**獣医師にとって：**
- 飼い主からの情報が断片的 → **構造化された健康チェックリストと解析履歴**
- 品種別の遺伝的疾患リスクを毎回調べる → **360犬種の遺伝的疾患データベース搭載**

---

## ShowScore Engine

「アルゴリズムが主導、AIが伴走」するハイブリッド評価エンジン。

```
Step 1: アルゴリズム → Base = Σ(Axis_i × Weight_i) + AgeAdj
Step 2: AI伴走     → Final = Base + AI_Correction (±8 cap)
```

- **5軸評価**: 骨格25% / 歩様25% / 筋肉20% / 被毛20% / 気質10%
- **再現性**: 同じ入力 → 同じベーススコア（100%決定論的）
- **AI補正**: 犬種ごとの特性を理解し、360犬種×5軸の感度プロファイルで精密補正
- **信頼度スコア**: 軸間整合性を自動検証し、結果の透明性を確保

### 検証精度

| 指標 | 値 |
|------|-----|
| スコア範囲の正確性 | **100%** |
| グレード判定の正確性 | **100%** |
| FCI国際基準との一致率 | **91.7%** |
| スコア精度 | **99.0%** |

---

## 実装済み機能（50+）

### AI解析・評価
- 写真解析（骨格・被毛）/ 動画解析（歩様・気質・被毛）
- FCI基準 S〜C の6段階グレード判定
- リアルタイムSSEストリーミング解析
- 信頼度スコア＆改善ガイド
- 犬種別感度プロファイル
- 歩様解析: 主軸投影ストライド計測 + IQR外れ値除去（12フレーム解析）
- 撮影角度推定（AngleCheck）: マスクのアスペクト比・面積率からfront/side/oblique判定
- 比較適格性ゲート（AngleGate）: 角度・信頼度に基づく比較可否判定
- 撮影ガイド（CaptureGuide）: 判定結果に応じた3行の撮影アドバイス自動生成
- 動的区間選抜（DynamicSegment）: 停止フレーム除去による歩行区間抽出
- 速度正規化区間（SpeedSegment）: 速度変動の少ない安定歩行区間の自動選択
- 入力品質判定（Quality PASS/HOLD）: 写真・動画の解析適合性を1つのステータスに集約
- 犬詳細ページ内解析（ページ遷移不要のインライン解析フロー）
- 健康チェック結果のバイリンガル出力（日本語/英語）

### 健康・医療
- 42+症状カタログから43疾患の類症鑑別（Jaccard類似度）
- 品種別遺伝的疾患リスク評価
- 年齢別重み付け類症鑑別
- 推奨検査リスト自動生成
- 10カテゴリ60+項目の健康チェックリスト
- 診察記録PDF自動生成

### 遺伝・繁殖
- 8種の遺伝子型解析（vWD1, PRA, DM, EIC, MDR1, HUU, DCM, CEA）
- Wright法COI（近親交配係数）算出
- 毛色遺伝学（E, B, D, K の4ローカス）
- 繁殖ペア適合性スコアリング
- EPD（期待される子孫改良量）推定

### 骨格・姿勢
- 17キーポイント解剖学的位置検出
- 2Dから3D骨格構造再構成
- 関節角度計算・品種別理想値比較
- マルチフレーム歩様解析

### 成長・追跡
- Modified Gompertz / 多項式 / Von Bertalanffy の3成長モデル
- ピーク年齢予測
- 発達段階判定（幼犬期・成犬期・シニア期）
- 異常パターン自動検出

### 記録・文書
- 国際ペットパスポートPDF（A4印刷対応）
- 健康報告書PDF
- MAAFエクスポートPDF
- 解析履歴ダッシュボード

### 検証・統計
- Cohen's Kappa / 加重Kappa / ICC / Bland-Altman / Pearson相関
- ブートストラップ95%信頼区間
- FCI公式ショーレポート基準による検証データセット

---

## 対応犬種

**360犬種** — FCI（国際畜犬連盟）登録犬種を網羅

---

## 技術スタック

| レイヤー | 技術 |
|---------|------|
| バックエンド | Python 3.11 / Flask / Gunicorn / ProxyFix |
| AI | Claude API + OpenAI API（フォールバック） |
| データベース | SQLite / PostgreSQL（デュアルバックエンド、SHA-256トークンハッシュ） |
| 認証 | カスタムセッション管理（HttpOnly / Secure / SameSite=Lax / CSRF対応） |
| フロントエンド | Vanilla HTML/CSS/JS（PWA対応・モバイルレスポンシブ） |
| ホスティング | Render（自動デプロイ+ヘルスチェック+ロールバック） |
| 決済 | PayPal（主要）/ Stripe（バックアップ） |
| CI/CD | GitHub Actions（スモークテスト → 自動マージ → デプロイ → ヘルスチェック） |
| セキュリティ | Flask-Limiter / HSTS / CSP / XSS防止 / インジェクション対策 |
| テスト | pytest 1076テスト（ユニット・インテグレーション） |

---

## クイックスタート

### ローカル開発

```bash
# 1. 依存関係インストール
pip install -r requirements.txt

# 2. 環境変数設定
cp .env.example .env
# .env を編集（最小構成: SECRET_KEY のみ）

# 3. 起動
python app.py
# → http://localhost:5000
```

### Docker

```bash
docker-compose up --build
# → http://localhost:5001
```

### 本番環境（Render）

```bash
# Procfile による自動起動:
gunicorn api.showdog_api:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120
```

---

## テスト

```bash
pytest tests/ -v
```

| テスト種別 | 内容 |
|-----------|------|
| ユニットテスト | scoring, health_checker, genetic_scoring, growth_prediction, pose_estimation, judge_validation, symptom_checker, reference_dataset, validation |
| インテグレーションテスト | API routes, database, auto_cycle, analysis_page, diagnostic_chat |
| エージェントテスト | RECO2/RECO3 agent gate, state, analyzer, input/output gate |
| **合計** | **27ファイル / 1076テスト / 0 fail** |

---

## 環境変数

### 必須（本番環境）

| 変数名 | 説明 |
|--------|------|
| `SECRET_KEY` | Flaskセッション署名キー（`python -c "import secrets; print(secrets.token_hex(32))"`で生成） |
| `RENDER` or `PRODUCTION` | 本番フラグ（エラーメッセージのサニタイズ、Secure Cookie有効化） |

### 認証・セッション

| 変数名 | デフォルト | 説明 |
|--------|-----------|------|
| `COOKIE_SECURE` | `1` | HTTPS専用Cookie（ローカル開発時 `0`） |
| `CSRF_SECRET` | 自動生成 | CSRFトークン生成用シークレット |
| `ALLOWED_ORIGINS` | 空（同一オリジンのみ） | CORS許可オリジン（カンマ区切り） |

### データベース

| 変数名 | 説明 |
|--------|------|
| `DATABASE_URL` | PostgreSQL接続URL（設定時PGバックエンド使用） |
| `DATABASE_PATH` | SQLiteデータベースのディレクトリパス |
| `RENDER_DISK_PATH` | Render永続ディスクパス（優先） |

### AI・外部サービス

| 変数名 | 説明 |
|--------|------|
| `ANTHROPIC_API_KEY` | Claude API キー（主AI） |
| `OPENAI_API_KEY` | OpenAI API キー（フォールバック） |
| `PAYPAL_CLIENT_ID` | PayPal決済クライアントID |
| `PAYPAL_CLIENT_SECRET` | PayPal決済シークレット |
| `STRIPE_SECRET_KEY` | Stripe決済キー |
| `STRIPE_WEBHOOK_SECRET` | Stripeウェブフックシークレット |

### メール（パスワードリセット）

| 変数名 | 説明 |
|--------|------|
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD` / `SMTP_FROM` | SMTP設定 |

### デバッグ

| 変数名 | 説明 |
|--------|------|
| `ALLOW_RESET_TOKEN_RESPONSE` | `1` でリセットトークンをレスポンスに含める（開発専用） |
| `FLASK_DEBUG` | `1` でFlaskデバッグモード |

---

## API エンドポイント一覧

### 認証 (8)

| メソッド | パス | 認証 | レート制限 |
|----------|------|:----:|-----------|
| POST | `/api/auth/register` | - | 5/h |
| POST | `/api/auth/login` | - | 10/h |
| POST | `/api/auth/logout` | 要 | - |
| GET | `/api/auth/me` | 要 | - |
| GET | `/api/auth/status` | - | - |
| POST | `/api/auth/security-question` | - | - |
| POST | `/api/auth/forgot-password` | - | 3/h |
| POST | `/api/auth/reset-password` | - | 5/h |

### 解析 (4)

| メソッド | パス | 認証 | 説明 |
|----------|------|:----:|------|
| POST | `/api/pre-analyze-photo` | 任意 | 写真の先行解析（骨格・被毛） |
| POST | `/api/pre-analyze-video` | 任意 | 動画の先行解析（歩様・気質） |
| POST | `/api/analyze-comprehensive` | 要 | 総合解析（写真+動画） |
| POST | `/api/analyze-comprehensive-stream` | 要 | SSEストリーミング解析 |

### 犬・解析履歴 (7)

| メソッド | パス | 認証 | 説明 |
|----------|------|:----:|------|
| GET/POST | `/api/dogs` | 要 | 犬一覧取得 / 新規登録 |
| GET/PUT/DELETE | `/api/dogs/<id>` | 要 | 犬の詳細・編集・削除 |
| GET | `/api/dogs/<id>/analyses` | 要 | 犬の解析履歴 |
| GET | `/api/analyses/<id>` | 要 | 解析詳細 |

### 健康・遺伝 (6)

| メソッド | パス | 説明 |
|----------|------|------|
| POST | `/api/analyze-symptoms` | 症状チェック |
| POST | `/api/genetic-test/analyze` | 遺伝子解析 |
| POST | `/api/genetic-scoring/breeding-compatibility` | 繁殖適合性 |
| POST | `/api/genetic-scoring/coi` | COI算出 |
| POST | `/api/growth-prediction/predict` | 成長予測 |
| POST | `/api/judge-validation/compute` | 審査検証 |

### 文書生成 (4)

| メソッド | パス | 説明 |
|----------|------|------|
| POST | `/api/generate-passport-pdf` | パスポートPDF |
| POST | `/api/generate-health-report-pdf` | 健康報告書PDF |
| POST | `/api/save-medical-visit` | 診察記録保存 |
| GET | `/api/medical-visit/<id>/pdf` | 診察記録PDF |

### 決済 (5)

| メソッド | パス | 説明 |
|----------|------|------|
| POST | `/api/paypal/create-order` | PayPal注文作成 |
| POST | `/api/paypal/capture` | PayPal決済確定 |
| POST | `/api/stripe/create-checkout-session` | Stripeセッション |
| POST | `/api/stripe/webhook` | Stripeウェブフック |
| GET | `/api/stripe/subscription-status` | サブスク状態 |

### システム (3)

| メソッド | パス | 説明 |
|----------|------|------|
| GET | `/api/health` | ヘルスチェック |
| GET | `/api/breeds` | 犬種一覧（360種） |
| GET | `/api/algorithm` | アルゴリズム情報 |

全APIは `application/json` レスポンスを保証。エラー時:
```json
{"success": false, "error": "エラーメッセージ", "version": "4.2.1"}
```

---

## セキュリティ

### 実装済み

| 対策 | 詳細 |
|------|------|
| SQL Injection | 全クエリでパラメータ化プレースホルダ使用 |
| パスワード | werkzeug.security（bcrypt相当）でハッシュ化 |
| セッション | `secrets.token_urlsafe(32)` 生成、SHA-256ハッシュ保存 |
| Cookie | HttpOnly / Secure / SameSite=Lax |
| CORS | デフォルト同一オリジンのみ（明示設定必要） |
| セキュリティヘッダ | HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy |
| レート制限 | Flask-Limiter（グローバル）+ IP+email 粒度の認証エンドポイント制限 |
| ファイルアップロード | 拡張子ホワイトリスト + マジックナンバー検証 + UUIDファイル名 |
| エラーマスキング | 本番環境でスタックトレース非表示 |
| 環境変数 | API キーは全て環境変数経由、本番でのSECRET_KEY必須チェック |

### 既知の制限事項（次期改善対象）

| 項目 | 状態 | 影響 |
|------|------|------|
| CSRF enforcement | トークン生成済み、検証未適用 | Cookie認証時にCSRF脆弱性あり（SPA Bearer方式では影響なし） |
| CSP `unsafe-inline` | `script-src`/`style-src` に含む | インラインスクリプト/スタイル使用のため |
| レート制限ストレージ | インメモリ | ワーカー間で共有されない、再起動でリセット |
| パスワードポリシー | 6文字以上のみ | 複雑性要件なし |
| 依存関係ロック | `requirements.txt` にバージョン上限なし | lockfile 導入推奨 |

---

## プロジェクト構成

```
showdog-app/
├── app.py                    # エントリーポイント
├── api/
│   ├── showdog_api.py        # Flask アプリ（全API 50+ルート, 6000行）
│   ├── database.py           # DB層（SQLite/PostgreSQL デュアル対応）
│   ├── scoring.py            # ShowScore Engine（決定論的5軸評価）
│   ├── local_analysis.py     # OpenCV/Pillow 写真・動画解析
│   ├── health_checker.py     # 症状チェッカー（43疾患）
│   ├── genetic_scoring.py    # 遺伝子解析・COI・繁殖最適化
│   ├── growth_prediction.py  # 成長予測（3モデル）
│   ├── pose_estimation.py    # 3D姿勢推定（17キーポイント）
│   ├── judge_validation.py   # 審査一致性検証（Kappa/ICC）
│   ├── diagnostic_chat.py    # AI診断チャット
│   ├── passport_pdf.py       # パスポートPDF生成
│   ├── breeds.py             # 360犬種データベース
│   ├── validation.py         # 内部整合性検証
│   ├── config_constants.py   # 定数定義
│   └── errors.py             # カスタム例外
├── static/                   # フロントエンド
│   ├── *.html                # 30ページ
│   ├── *.js                  # 14モジュール
│   ├── *.css                 # 4スタイルシート
│   ├── i18n/                 # 多言語（ja/en）
│   ├── sw.js                 # Service Worker（PWA）
│   └── manifest.json         # PWAマニフェスト
├── tests/                    # 27テストファイル / 1076テスト
├── .github/workflows/        # CI/CD（自動マージ・デプロイ・ヘルスチェック）
├── Dockerfile                # Dockerイメージ
├── Procfile                  # Render起動コマンド
└── requirements.txt          # Python依存関係
```

詳細な技術仕様は [`ARCHITECTURE.md`](./ARCHITECTURE.md) を参照。

---

## 料金プラン

| プラン | 月額（税込） | 主な機能 |
|--------|------------|---------|
| Free | ¥0 | 月3回解析、写真のみ、診察記録 |
| Standard | ¥980 | 月15回、写真+動画、パスポートPDF、診察記録 |
| Pro | ¥1,980 | 月50回、遺伝性疾患、交配・COI |
| MAX | ¥2,980 | 無制限、全機能解放、優先解析 |

Global版（USD）も対応。

---

## 運営

**Equine Vet Group / Equine Vet Synapse事業部**
- 代表: 上手 健太郎
- 所在地: 〒979-2123 福島県南相馬市小高区大町2丁目45番
- TEL: 0244-32-1583
- Email: minamisoma.vet@gmail.com

---

## リンク

- アプリ: https://showdog-app.onrender.com
- Instagram: https://www.instagram.com/k.kamide.canine_vet_nutrition
- 南相馬アニマルクリニック: https://www.minamisoma-vet.com
- Canine Vet: https://www.caninevet.jp

---

© 2026 ShowDog Analysis Platform. Powered by ShowScore Engine.
