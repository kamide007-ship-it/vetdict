# VetDict — Claude Code Project Guide

## プロジェクト概要
獣医学疾患データベース・薬品辞書・AI診断チャットを搭載した獣医学総合プラットフォーム。
- **URL**: https://vetdict.info
- **デプロイ**: Render (gunicorn)
- **開発者**: 上手 健太郎 DVM（南相馬アニマルクリニック）
- **運営**: Equine Vet Synapse

## 技術スタック
- **Backend**: Flask (Python 3.11) + SQLite
- **Frontend**: バニラJS (SPA) + CSS (single file)
- **テスト**: pytest (2,471テスト)
- **Lint**: ruff (pyproject.toml)
- **CI/CD**: GitHub Actions (lint → test → security audit)
- **PWA**: manifest.json + ServiceWorker (sw.js, CACHE_NAME=vetdict-v2)
- **Analytics**: GA4 (G-D8LSEGW9ZX) + カスタムイベント5種
- **決済**: PayPal Subscriptions API (Plan: P-5FB7289813535813HNHCF4OA)
- **現状**: OPEN_BETA=true（全機能無料）

## ディレクトリ構造
```
api/
  vetdict_api.py          — メインFlaskアプリ + ルーティング + CSPヘッダー
  diagnostic_chat.py      — チャット診断エンジン (症状抽出 + 疾患マッチング)
                            SYMPTOM_ALIASES (500+), _ID_SYNONYMS (80+),
                            _extract_species_symptoms(), _match_species_symptoms_to_diseases()
  health_checker.py       — 犬用症状チェッカー (チェックボックス)
  drug_dictionary.py      — 薬品辞書API + Blueprint
  drug_batch_1.py         — 薬品データ batch 1
  drug_batch_2.py         — 薬品データ batch 2
  drug_batch_3.py         — 動物種別投与量パッチ (SPECIES_INFO_PATCH)
  drug_batch_4.py         — 魚用薬品 (FISH_DRUGS + FISH_SPECIES_INFO_PATCH)
  disease_store.py        — SQLite疾患ストア + fallback（未マイグレーション種は自動fallback）
  species_analyzer.py     — マルチ種の症状解析ルーティング (SPECIES_HANDLERS: 21種)
  paypal_api.py           — PayPalサブスク + waitlist + メール復元
  auth.py                 — API認証
  species/
    fish_diseases.py      — 魚病 25疾患 48症状 + SYMPTOM_CATEGORIES
    cat_diseases.py       — 猫
    rabbit_diseases.py    — ウサギ
    ... (21種)
    helpers.py            — 共通解析関数 (analyze_symptoms_generic)
    prevalence_data.py    — 種別有病率（猫: FHV-1=very_common, Chlamydia=common 等）
templates/
  index.html              — メインSPA (GA4, PWA, OGP, Schema.org, defer JS)
  partials/
    _hero.html            — ヒーローセクション
    _species.html         — 動物種カード (21種)
    _main_content.html    — チェッカー/DB/チャット/薬品タブ
    _pricing.html         — オープンベータ（全機能無料）+ メールリスト収集
    _sponsors.html        — スポンサー
    _references.html      — 参考文献 (66+ citations, 魚病文献含む)
    _footer.html          — SNSシェア + 免責事項 + FDA/農水省未認証表記
  tokushoho.html          — 特商法
  terms.html / privacy.html
static/
  js/app.js               — 統合JS (I18N + UI + チャット + GA4 + admin/pro制御)
  css/main.css            — 統合CSS (app.cssは削除済み — 絶対に復活させないこと)
  manifest.json           — PWA
  sw.js                   — ServiceWorker (CACHE_NAME=vetdict-v2)
  robots.txt / sitemap.xml
  og-image.svg            — OGP画像 (1200x630)
scripts/
  migrate_to_sqlite.py    — SQLiteマイグレーション (SPECIES_MODULESにfish含む)
```

## データ規模
- **疾患**: 6,400+ (21動物種)
- **薬品**: 187 (12種が魚専用)
- **症状エイリアス**: 500+ (SYMPTOM_ALIASES) + 80+ (ID同義語)
- **対応動物種**: 21 (犬,猫,馬,ウサギ,ハムスター,モルモット,チンチラ,フェレット,ハリネズミ,フクロモモンガ,デグー,鳥,インコ,オウム,爬虫類,リクガメ,ヘビ,トカゲ,両生類,魚,その他)

## 診断エンジン
### チェックボックス式 (全種)
- `species_analyzer.py` → `SPECIES_HANDLERS` で種別にルーティング
- 各種モジュールの `analyze_symptoms()` → `analyze_symptoms_generic()` (helpers.py)

### チャット式 (diagnostic_chat.py)
- **症状抽出**: `_extract_species_symptoms()` — 最長一致優先 + フラグメント分割
- **ID同義語解決**: `_ID_SYNONYMS` (80+マッピング) — loss_of_appetite ↔ appetite_loss 等
  - pop_eye ↔ exophthalmos/eye_bulging/enlarged_eye
  - eye_swelling ↔ exophthalmia/bulging_eye
  - sneezing ↔ nasal_discharge（爬虫類用）
  - bloating ↔ vulvar_swelling（フェレット副腎用）
- **疾患マッチング**: `_match_species_symptoms_to_diseases()` — IDF重み付き調和平均
  - 特異度ボーナス、陰性証拠ペナルティ、緊急度安全ブースト
  - ロジスティック信頼度校正 (0-95%)
  - シノニム展開 (_SYN辞書: frayed_fins → fin_rot も疾患マッチ対象)
  - 有病率補正 (prevalence_data.py から読み込み)
- **SYMPTOM_ALIASES**: 500+のJP/EN口語表現→症状IDマッピング
  - 犬用 + 魚用 + 全種共通 (毛が抜ける, 首が傾いてる, 羽を膨らませてる 等)
  - 獣医師監査3回実施済み

### 精度実績 (50テストケース、500+エイリアス)
| テストケース | 信頼度 |
|------------|--------|
| 魚 白点病 (3症状) | 95.0% |
| 魚 松かさ病 (3症状) | 94.2% |
| 魚 ヘキサミタ | 95.0% |
| 魚 KHV | 77.5% |
| 猫 FHV-1/URI | 91.7% |
| 猫 FIP/胸水 | 76.9% |
| 猫 動脈血栓症 | 72.5% |
| 猫 肝リピドーシス | 85.0% |
| 猫 角膜潰瘍 | 91.1% |
| 猫 貧血/出血 | 92.3% |
| ウサギ 斜頸 | 85.8% |
| ウサギ パスツレラ | 88.7% |
| ウサギ 消化管うっ滞 | 90.5% |
| 鳥 そのう炎 | 83.2% |
| 鳥 呼吸器 | 66.7% |
| 爬虫類 呼吸器 | 95.0% |
| 爬虫類 甲羅/MBD | 72.1% |
| 爬虫類 ビタミンA欠乏 | 71.2% |
| ハリネズミ WHS | 61.9% |
| ハリネズミ ダニ | 66.0% |
| ハリネズミ 眼球突出 | 64.3% |
| ハムスター 眼球突出 | 64.3% |
| モルモット 呼吸器 | 95.0% |
| モルモット 壊血病 | 83.5% |
| フェレット インスリノーマ | 67.5% |

### 診断アルゴリズムの構成
- IDF重み付き調和平均（weighted recall × coverage）
- 特異度ボーナス（希少症状マッチ: +3-6%）
- 陰性証拠ペナルティ（重要症状の欠如: -3-6%）
- 緊急度安全ブースト（emergency: +5%, high: +2%）
- 有病率補正（very_common: ×1.20, uncommon: ×0.90, rare: ×0.80）
- カバレッジボーナス（3+症状マッチ: +5%, 4+: +10%）
- シノニム展開（frayed_fins→fin_rot, sneezing→nasal_discharge 等80+）
- ロジスティック信頼度校正（0-95%スケール）

## アクセス制御
- **Admin**: `?admin=kamide007` でフルアクセス (localStorage永続化)
- **Pro**: PayPal決済 or メール復元 (現在OPEN_BETA=true: 全員Pro)
- **app.jsの`OPEN_BETA`**: `true`=全機能無料, `false`=有料プラン有効化

## 重要な設定
### PayPal
- Client ID: `AX7kp51y...VTUE` (フロントエンドに設定済み)
- Secret: 環境変数 `PAYPAL_SECRET` (Renderダッシュボードで設定)
- Plan ID: `P-5FB7289813535813HNHCF4OA` (¥980/月)
- Webhook: `https://vetdict.info/api/paypal/webhook` (ID: 5DH235157M131750H)

### Stripe (未使用/将来用)
- Account: acct_1T0Tw86CJtNyrrE8
- Product: prod_UDPNfbWfIgPNHI (VetDict Pro)
- Price: price_1TEyln6CJtNyrrE8uM1mtNbZ (¥980/月)

### GA4
- Measurement ID: G-D8LSEGW9ZX
- カスタムイベント: select_species, analyze_symptoms, switch_view, chat_message, waitlist_signup

## CSPヘッダー
`script-src`: self + unsafe-inline + googletagmanager.com + paypal.com
`connect-src`: self + google-analytics.com + paypal.com + api-m.paypal.com
`frame-src`: paypal.com + sandbox.paypal.com

## テスト実行
```bash
python3 -m pytest tests/ -x -q          # 全テスト (2,471)
python3 -m pytest tests/test_diagnostic_chat.py -x -q  # チャット診断テスト
python3 -m pytest tests/test_drug_dictionary.py -x -q   # 薬品辞書テスト
```

## 新しい動物種を追加する手順
1. `api/species/{species}_diseases.py` を作成 (DISEASES, SYMPTOM_NAMES, SYMPTOM_CATEGORIES, analyze_symptoms)
2. `api/species_analyzer.py`: import + SPECIES_HANDLERS に追加
3. `api/diagnostic_chat.py`: _GENERIC_SPECIES + SPECIES_LABELS に追加
4. `api/disease_store.py`: SPECIES_META + _MODULE_MAP に追加
5. `scripts/migrate_to_sqlite.py`: SPECIES_MODULES に追加
6. `static/js/app.js`: SPECIES_ICONS + SPECIES配列 + pendingStats更新
7. テスト: `tests/test_disease_store.py` と `tests/test_vetdict_api.py` の種数アサーション更新

## 薬品投与量を追加する手順
- 既存薬品に種別投与量を追加: `api/drug_batch_3.py` の SPECIES_INFO_PATCH
- 新規薬品を追加: `api/drug_batch_4.py` の FISH_DRUGS (または新バッチファイル)
- `api/drug_dictionary.py` でインポート + マージロジック

## 診断精度を改善する手順
1. `api/diagnostic_chat.py` の `SYMPTOM_ALIASES` に口語表現を追加
2. `_ID_SYNONYMS` にID間の同義語を追加（種ごとにIDが異なる場合）
3. `_match_species_symptoms_to_diseases()` 内の `_SYN` にマッチング用シノニムを追加
4. `api/species/prevalence_data.py` に有病率データを追加
5. **重複チェック必須**: ruff F601 — 3つの辞書 (SYMPTOM_ALIASES, _ID_SYNONYMS, _SYN) の重複キーを確認

## 注意事項
- CSS/JSは全て統合済み (main.css, app.js) — 個別ファイルの参照を追加しないこと
- **app.cssは削除済み** — 復活させるとヘッダーが水色グラデーションになるバグが再発
- `data-i18n` は textContent で設定 → HTMLエンティティ不可 (Unicode文字を使用)
- `data-i18n-html` は innerHTML で設定 → HTMLエンティティ可
- ruff F601 (重複dictキー) に注意 — SYMPTOM_ALIASES, _ID_SYNONYMS, _SYN は巨大dictなので重複チェック必須
- SQLiteにデータがない種は `get_symptoms_for_species()` がPythonモジュールからfallback
- ServiceWorkerのキャッシュ更新時は `sw.js` の `CACHE_NAME` をインクリメント
- エイリアスキーは全て小文字 (ruffテストで検証済み)

## 既知の課題（次セッションで対応可能）
- フェレット副腎疾患の診断精度がまだ低い（44.6%）— 疾患DB側のsymptom IDを拡充必要
- 猫甲状腺機能低下症（48.8%）— 同上
- ハムスターウェットテイル（48.3%）— diarrhea + lethargy の2症状では特異性が低い
- Renderフリープランのスリープ問題（15分無操作→初回アクセス遅延）
