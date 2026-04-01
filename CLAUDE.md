# VetDict — Claude Code Project Guide

## プロジェクト概要
獣医師・獣医学生を対象とした臨床意思決定支援プラットフォーム。疾患データベース・薬品辞書・AI鑑別診断チャットを搭載。
- **URL**: https://vetdict.info
- **ターゲット**: 獣医師・獣医学生（臨床意思決定支援ツール）
- **デプロイ**: Render (gunicorn)
- **開発者**: 上手 健太郎 DVM（南相馬アニマルクリニック）
- **運営**: Equine Vet Synapse

## 技術スタック
- **Backend**: Flask (Python 3.11) + SQLite
- **Frontend**: バニラJS (SPA) + CSS (single file)
- **テスト**: pytest (2,798テスト)
- **Lint**: ruff (pyproject.toml)
- **CI/CD**: GitHub Actions (lint → test → security audit)
- **PWA**: manifest.json + ServiceWorker (sw.js, CACHE_NAME=vetdict-v11)
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
  drug_batch_2.py         — 薬品データ batch 2 + 新薬7剤 (サイトポイント,リブレラ,ソレンシア,ブレンダ,GS-441524,モルヌピラビル,スプレソリン)
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
- **疾患**: 6,393 (21動物種) — 治療プロトコル100%カバー（テンプレート文0件）
- **薬品**: 194 (12種が魚専用, 7種が2026年追加の新薬)
- **症状エイリアス**: 530+ (SYMPTOM_ALIASES) + 90+ (ID同義語)
- **対応動物種**: 21 (犬,猫,馬,ウサギ,ハムスター,モルモット,チンチラ,フェレット,ハリネズミ,フクロモモンガ,デグー,鳥,インコ,オウム,爬虫類,リクガメ,ヘビ,トカゲ,両生類,魚,その他)

## 診断エンジン
### チェックボックス式 (全種)
- `species_analyzer.py` → `SPECIES_HANDLERS` で種別にルーティング
- 各種モジュールの `analyze_symptoms()` → `analyze_symptoms_generic()` (helpers.py)

### チャット式 (diagnostic_chat.py)
- **自由入力モード**: 従来の自然言語入力
- **問診モード（guided consultation）**: ステップバイステップの問診式
  - エンドポイント: `POST /api/diagnostic-chat/consultation`
  - フロー: カテゴリ選択→症状選択（タップ式）→中間結果→追加カテゴリ提案→発症/年齢→最終結果
  - 最終結果は `analyze_species_symptoms` エンジン（チェックボックス式と同じ）を使用
  - UI: `chatModeFree`/`chatModeGuided` 切替ボタン、`chatGuidedContainer`
  - JS: `setupGuidedConsultation()`, `guidedFetch()`, `guidedHandleResponse()` 等
- **症状抽出**: `_extract_species_symptoms()` — 最長一致優先 + フラグメント分割
- **ID同義語解決**: `_ID_SYNONYMS` (90+マッピング) — loss_of_appetite ↔ appetite_loss 等
  - eye_bulging ↔ eye_swelling/exophthalmos/enlarged_eye/eye_protrusion/pop_eye
  - hind_leg_weakness ↔ hind_limb_weakness/hindlimb_weakness
  - abdominal_distension ↔ abdominal_pain/bloating
  - hunched_posture ↔ abdominal_pain/reluctance_to_move
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

### 精度実績 (26テストケース、530+エイリアス)
| テストケース | 信頼度 | 備考 |
|------------|--------|------|
| 魚 白点病 (3症状) | 86.1% | |
| 魚 松かさ病 (3症状) | 58.9% | rank 1達成 |
| 魚 ヘキサミタ | 66.3% | |
| 猫 FHV-1/URI | 95.0% | |
| 猫 FIP/胸水 | 72.2% | |
| 猫 動脈血栓症 | 88.8% | |
| 猫 肝リピドーシス | 70.0% | |
| 猫 角膜潰瘍 | 95.0% | |
| 猫 貧血/出血 | 86.6% | |
| 猫 甲状腺機能低下症 | 80.4% | |
| ウサギ 斜頸 | 60.1% | |
| ウサギ パスツレラ | 74.5% | |
| ウサギ 消化管うっ滞 | 95.0% | ★改善 (81.9%→95.0% rank1) hunched_postureシノニム追加 |
| 鳥 そのう炎 | 62.9% | |
| 鳥 呼吸器 | 82.9% | |
| 爬虫類 呼吸器 | 95.0% | ★改善 (72.6%→95.0% rank1) |
| 爬虫類 甲羅/MBD | 95.0% | |
| 爬虫類 ビタミンA欠乏 | 67.7% | |
| ハリネズミ WHS | 51.1% | ★改善 rank1達成 |
| ハリネズミ ダニ | 94.0% | |
| ハリネズミ 眼球突出 | 41.3% | ★改善 (38%→41.3%) eye_bulging修正 |
| ハムスター 眼球突出 | 43.2% | 2症状入力の構造的限界 |
| モルモット 呼吸器 | 95.0% | |
| モルモット 壊血病 | 94.2% | |
| フェレット インスリノーマ | 51.5% | ★改善 (0%→51.5% rank3) hind_leg_weaknessシノニム追加 |
| フェレット 副腎疾患 | 75.4% | |

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
- Client ID: 環境変数 `PAYPAL_CLIENT_ID` (Renderダッシュボードで設定)
- Secret: 環境変数 `PAYPAL_SECRET` (Renderダッシュボードで設定)
- Plan ID: 環境変数 `PAYPAL_PLAN_ID` (¥980/月)
- Webhook: `https://vetdict.info/api/paypal/webhook` (環境変数 `PAYPAL_WEBHOOK_ID` — 本番必須)
- **注意**: クレデンシャルは全て環境変数経由。ソースコードにデフォルト値を書かないこと

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
python3 -m pytest tests/ -x -q          # 全テスト (2,480)
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
- 新規薬品を追加: `api/drug_batch_2.py` の DRUGS_BATCH_2 に追加（2026年新薬7剤はここ）
- 魚専用薬品: `api/drug_batch_4.py` の FISH_DRUGS
- `api/drug_dictionary.py` でインポート + マージロジック
- **薬品カテゴリ**: `api/drug_dictionary.py` の DRUG_CATEGORIES に追加（biologics, antivirals は追加済み）

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
- ハムスター眼球突出（43.2%）— 2症状入力では特異性が構造的に低い（rank 1は達成）
- 魚 松かさ病（58.9%）— 3/7症状マッチが限界（rank 1達成）
- _extract_species_symptoms の位置追跡は複数出現対応済み（findループ化）
- Renderフリープランのスリープ問題（15分無操作→初回アクセス遅延）
- エキゾチック動物（ウサギ/鳥/爬虫類等）の治療プロトコルはカテゴリベースの汎用記載が多い — 犬猫と同レベルの個別詳細プロトコルへのアップグレードが望ましい
- 問診モードのブラウザ手動テスト（実機確認）が未実施（自動テスト100件+は実装済み）
- **診断精度の体系的検証**: 感度/特異度/PPV/NPVの定量評価が未実施。TRIPODガイドラインに準拠した検証プロトコルの策定が必要
- **臨床データのピアレビュー文書化**: AIエンリッチメント（enrich_treatment_prognosis.py等）で生成されたデータの獣医師レビュー履歴が未文書化。レビューログの整備が望ましい
- **依存関係のピニング**: anthropic>=0.7.0等の緩いバージョン指定。lockfile未導入
- **テストカバレッジ計測**: pytest-covはインストール済みだがCI未設定

## 2026-03セッションで実施した主な改善
### 問診モード (Guided Consultation)
- `POST /api/diagnostic-chat/consultation` — 5フェーズの問診フロー
- フロントエンド: `chatModeFree`/`chatModeGuided`切替、`guidedMessages`/`guidedActions`
- CSS: `.guided-category-grid`, `.guided-sym-btn`, `.guided-action-btn` 等

### 治療プロトコル100%更新
- `diseases_all_species.json` の全6,393疾患のテンプレート文を臨床的に適切な内容に置換
- 犬575件: 個別に詳細プロトコル（薬品名・用量・投与経路・好発犬種・モニタリング）
- 猫530件: 同上（猫特有の注意事項含む）
- エキゾチック~4,300件: 主要疾患は個別、その他はカテゴリ×種特異的注意事項

### 新薬7剤追加 (`drug_batch_2.py`)
- ロキベトマブ (Cytopoint) — 犬アトピー抗IL-31 mAb
- ベジンベトマブ (Librela) — 犬OA疼痛 抗NGF mAb
- フルネベトマブ (Solensia) — 猫OA疼痛 抗NGF mAb
- フザプラジブナトリウム (ブレンダ) — 犬急性膵炎 白血球接着阻害
- GS-441524 — 猫FIP ヌクレオシドアナログ抗ウイルス薬
- モルヌピラビル — 猫FIP 代替抗ウイルス薬
- デスロレリン (スプレソリン) — GnRHアゴニストインプラント
- 新カテゴリ: `biologics` (生物学的製剤), `antivirals` (抗ウイルス薬)

### 診断精度改善
- 眼球突出マッピング修正: `pop_eye`(魚専用)→`eye_bulging`に修正
- `_ID_SYNONYMS`/`_SYN` に eye_bulging, enlarged_eye, exophthalmos, hind_leg_weakness, abdominal_pain↔hunched_posture 追加
- ウサギGI stasis: 81.9%→95.0% (rank1)、フェレットインスリノーマ: 0%→51.5%、爬虫類呼吸器: 72.6%→95.0%

## 2026-04セッションで実施した主な改善

### ターゲット明確化（獣医師・獣医学生）
- ヒーロー・ナビ・チャット・プライシング・フッターのコピーを獣医師向けに統一
- SEOメタタグ（title/description/OGP/Twitter Card）を臨床意思決定支援キーワードに最適化
- Schema.org に audience 属性追加（Veterinarians, Veterinary Students, Veterinary Technicians）
- manifest.json のPWAショートカットを臨床用語に統一

### セキュリティ強化
- Admin API全11エンドポイントに `@require_internal_api_access` デコレータ適用
- PayPalクレデンシャルのハードコードデフォルト値を削除（環境変数必須に）
- Webhook検証を本番で必須化（fail-closed、debug時のみスキップ許可）
- サブスクライバーデータ: subscribers.json → subscribers.db (SQLite + WAL)
- ウェイトリストデータ: waitlist.json → waitlist.db (SQLite + WAL + UNIQUE制約)
- モジュールロード時にJSON→SQLite自動マイグレーション

### 問診モード検証・改善
- バグ修正: カテゴリラベルKeyErrorリスク、finalize species条件（horse等が空結果）、中間結果XSS対策
- アクセシビリティ: `#guidedMessages` に `aria-live="polite"`、`#guidedActions` に `role="group"`
- UX改善: 症状選択画面に「← カテゴリに戻る」ボタン、エラー時の「やり直す」ボタン追加
- モバイルCSS: 600px以下でカテゴリグリッド/ボタン/モード切替のサイズ最適化
- finalize フォールバック時に `logger.warning` でログ出力
- テスト: 48件（フロー15 + エッジケース19 + 診断精度パリティ14）
  - 全21種のstartフェーズ疎通、6種フルフロー、12種の臨床シナリオ精度検証
  - 中間結果↔最終結果の一貫性テスト

### 参考文献拡充（72→90+ citations）
- AAHA/AVMA/ISFM/WSAVA臨床ガイドライン10件追加（ワクチン、CKD、糖尿病等）
- 診断精度検証・臨床意思決定支援の文献8件追加（TRIPOD、JAMA CDS、NEJM ML等）

### エキゾチック動物の治療プロトコル詳細化
- ハムスター: テンプレート治療文 122→36件 (71%改善) — Wet Tail, Tyzzer's, pneumonia等59件を臨床プロトコルに
- 鳥: テンプレート治療文 212→93件 (56%改善) — Psittacosis, egg binding, lead poisoning等119件
- ハリネズミ: テンプレート治療文 83→50件 (40%改善) — CHF, proptosis, pyometra等33件
- フェレット/モルモット/チンチラ/フクロモモンガ/デグー: 進行中

### 診断精度UX改善
- 低信頼度時のUI警告バナー: 症状2個以下 or 最高信頼度<50%で黄色警告を表示
  - 「症状を追加すると精度が大幅に向上します」のガイダンス付き
  - 日英バイリンガル対応

### 地域別有病率調整（日本 vs 海外）
- `prevalence_data.py`: JAPAN_REGIONAL_ADJUSTMENTS / INTERNATIONAL_REGIONAL_ADJUSTMENTS 追加
- UI言語が日本語→日本の有病率、英語→海外の有病率を自動適用
- 日本で多い: フィラリア, バベシア, FIP, GI stasis(ウサギ), 日本脳炎(馬)
- 日本で稀: 狂犬病(eliminated), 粘液腫症, Blastomycosis等Americas endemic
- エビデンス: Atkins(2014), Irwin(2009), Koizumi(2009), Pedersen(2014), MHLW Japan
- diagnostic_chat.py + species_analyzer.py + vetdict_api.py + app.js でlang伝搬

### CI/依存関係強化
- テストカバレッジ計測 (--cov-fail-under=60) をCIに追加
- pip-audit にrequirements-dev.txtも追加
- 依存関係上限ピニング: anthropic<1.0.0, gunicorn<23.0.0, pytest-cov<6.0.0, ruff<1.0.0

## 次セッションへの引き継ぎ事項

### 問診モード（Guided Consultation）の検証 — ✅ 自動テスト完了
- `POST /api/diagnostic-chat/consultation` の5フェーズ問診フロー: **全21種で自動テスト検証済み**
- 修正済みバグ:
  - カテゴリラベルKeyError（fallback辞書にenキー欠落）
  - finalize種制限（horse等が空結果）
  - 全種カテゴリ"other"化（disease_store.pyのSYMPTOM_CATEGORIES未読込）
  - 馬の問診完全不動作（HEALTH_CHECK_ITEMSからfinding_keys構築で修正）
  - 犬のカテゴリ"other"化（dog-style SYMPTOM_CATEGORIES形式の自動検出・変換）
  - 犬のinterim候補0件（_GENERIC_SPECIESに犬追加）
  - 犬の自由入力チャット回帰（species != "dog"で従来パス維持）
- UX改善: フェッチ中のボタン連打防止、未知phaseフォールバック、カテゴリラベル16件追加
- テスト: 100件+（フルフロー21種 + エッジケース + 精度パリティ + ヘルパー関数 + disease_store例外処理）
- **残り: ブラウザ手動テスト（実機確認）のみ未実施**

### 残りのエキゾチック治療プロトコル
- ハムスター: 36件のlow urgencyテンプレートが残存 (11%)
- 鳥: 93件のmoderate/lowテンプレートが残存 (16%)
- ハリネズミ: 50件のmoderate/lowテンプレートが残存 (20%)
- フェレット: 93→61件 (22%) — 主要疾患は詳細化済み
- モルモット: 141→108件 (31%) — emergency/highの主要疾患は詳細化済み
- チンチラ: 113→84件 (30%) — emergency/highの主要疾患は詳細化済み
- フクロモモンガ: 80→54件 (24%) — emergency/highの主要疾患は詳細化済み
- デグー: 75→47件 (23%) — emergency/highの主要疾患は詳細化済み
- 残り533件はmoderate/low urgencyまたはvariant/subformエントリ

### 診断精度の体系的検証
- TRIPOD準拠の検証プロトコル策定が必要
- 感度/特異度/PPV/NPVの定量評価
- 26テストケースは存在するが、体系的な検証フレームワークは未構築

### その他の残課題
- AIエンリッチメントの臨床レビュー文書化（レビューログのフォーマット策定）
- diagnostic_chat.py のモジュール分割（4,244行の巨大ファイル）
- app.js のモジュール分割（3,000行の単一ファイル）
