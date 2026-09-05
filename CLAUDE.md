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
- **テスト**: pytest (3,094テスト)
- **Lint**: ruff (pyproject.toml)
- **CI/CD**: GitHub Actions (lint → test → security audit)
- **PWA**: manifest.json + ServiceWorker (sw.js, CACHE_NAME=vetdict-v25)
- **Analytics**: GA4 (G-D8LSEGW9ZX) + カスタムイベント5種
- **決済**: PayPal Subscriptions API (Plan: P-5FB7289813535813HNHCF4OA)
- **現状**: OPEN_BETA=true（全機能無料）

## ディレクトリ構造
```
api/
  vetdict_api.py          — メインFlaskアプリ + ルーティング + CSPヘッダー
  diagnostic_chat.py      — チャット診断エンジン（api/chat/ パッケージに分割済み）
  health_checker.py       — 症状チェッカー (全21種対応、_build_symptoms_display/_build_recommended_tests_display ヘルパー)
  drug_dictionary.py      — 薬品辞書API + Blueprint (250薬品、ECVN 11種含む)
  drug_batch_1.py         — 薬品データ batch 1
  drug_batch_2.py         — 薬品データ batch 2 + 新薬7剤 (サイトポイント,リブレラ,ソレンシア,ブレンダ,GS-441524,モルヌピラビル,スプレソリン)
  drug_batch_3.py         — 動物種別投与量パッチ (SPECIES_INFO_PATCH)
  drug_batch_4.py         — 魚用薬品 (FISH_DRUGS + FISH_SPECIES_INFO_PATCH)
  drug_batch_9.py         — ISCAID 2019 UTIガイドライン薬品8剤 + UTI投与ノートパッチ12薬品
  anesthesia_protocols.py — 鎮静・麻酔プロトコルデータ (21種, 188プロトコル)
  anesthesia_api.py       — 鎮静・麻酔API Blueprint (4エンドポイント)
  anesthesia_contraindications.py — 薬品-疾患禁忌ルール (31ルール, check_contraindications())
  disease_store.py        — SQLite疾患ストア + fallback（未マイグレーション種は自動fallback）
  species_analyzer.py     — マルチ種の症状解析ルーティング (SPECIES_HANDLERS: 21種、symptom_names_lookupも返却)
  content_quality.py      — 疾患コンテンツ補完 (SPECIES_NAME_JA/EN、_symptom_text lang対応)
  paypal_api.py           — PayPalサブスク + waitlist + メール復元
  auth.py                 — API認証
  chat/
    symptom_aliases.py    — SYMPTOM_ALIASES 530+ 口語表現マッピング
    disease_matcher.py    — 疾患マッチングアルゴリズム
    symptom_extractor.py  — 症状抽出エンジン
    supplements.py        — サプリメントデータ
    constants.py          — 種ラベル・定数
    species_data.py       — 種モジュール読み込み
  data/
    sponsor_adjuncts.py   — ECVNスポンサー製品注入 (9製品、_PRODUCTS レジストリ、コンパクトブロック [ECVN:Block])
    supplementary_diseases.json — 猫等の補足疾患データ
  species/
    fish_diseases.py      — 魚病 28疾患 + SYMPTOM_CATEGORIES
    cat_diseases.py       — 猫 543疾患
    rabbit_diseases.py    — ウサギ 453疾患
    equine_diseases.py    — 馬 737疾患（Disease dataclass + HEALTH_CHECK_ITEMS + _enrich_horse_diseases）
    ... (全21種)
    helpers.py            — 共通解析関数 (analyze_symptoms_generic, enrich_diseases)
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
  sw.js                   — ServiceWorker (CACHE_NAME=vetdict-v25)
  robots.txt / sitemap.xml
  og-image.svg            — OGP画像 (1200x630)
scripts/
  migrate_to_sqlite.py    — SQLiteマイグレーション (SPECIES_MODULESにfish含む)
```

## データ規模
- **疾患**: 7,146 (21動物種) — 治療プロトコル100%カバー（テンプレート文0件）
- **薬品**: 250 (12種が魚専用, 7種が2026年追加の新薬, 8種がISCAID 2019 UTIガイドライン薬品, ECVN 11種)
- **症状エイリアス**: 530+ (SYMPTOM_ALIASES) + 90+ (ID同義語)
- **対応動物種**: 21 (犬,猫,馬,ウサギ,ハムスター,モルモット,チンチラ,フェレット,ハリネズミ,フクロモモンガ,デグー,鳥,インコ,オウム,爬虫類,リクガメ,ヘビ,トカゲ,両生類,魚,その他)
- **鎮静・麻酔プロトコル**: 188 (全21種対応、全21種が全8カテゴリ完備、犬猫各14プロトコル、馬13プロトコル、ウサギ11プロトコル、ASA分類付き)

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
python3 -m pytest tests/ -x -q          # 全テスト (2,700+)
python3 -m pytest tests/test_diagnostic_chat.py -x -q  # チャット診断テスト
python3 -m pytest tests/test_drug_dictionary.py -x -q   # 薬品辞書テスト
```

## 新しい動物種を追加する手順
1. `api/species/{species}_diseases.py` を作成 (DISEASES, SYMPTOM_NAMES, SYMPTOM_CATEGORIES, analyze_symptoms)
2. `api/species_analyzer.py`: import + SPECIES_HANDLERS に追加
3. `api/diagnostic_chat.py`: _GENERIC_SPECIES + SPECIES_LABELS に追加
4. `api/disease_store.py`: SPECIES_META + _MODULE_MAP に追加
5. `scripts/migrate_to_sqlite.py`: SPECIES_MODULES に追加
6. `scripts/build_disease_search_index.py`: SPECIES_MODULE_MAP に追加 → `python3 scripts/build_disease_search_index.py` で `api/data/disease_search_index.json` を再生成（全種横断検索 `/api/diseases?q=` が空SQLite環境でも動くための軽量名前インデックス）
7. `static/js/app.js`: SPECIES_ICONS + SPECIES配列 + pendingStats更新
8. テスト: `tests/test_disease_store.py` と `tests/test_vetdict_api.py` の種数アサーション更新

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
- `diseases_all_species.json` の全疾患（2026-03時点）のテンプレート文を臨床的に適切な内容に置換
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
- ハムスター: テンプレート治療文 122→36件 (71%改善)
- 鳥: テンプレート治療文 212→93件 (56%改善)
- ハリネズミ: テンプレート治療文 83→50件 (40%改善)
- フェレット: 93→61件 (34%改善) — ECE, insulinoma, lymphoma, ADV等
- モルモット: 141→108件 (23%改善) — scurvy, GI stasis, dysbiosis等（ペニシリン禁忌明記）
- チンチラ: 113→84件 (26%改善) — dental, fur ring, heatstroke等（フィプロニル致死明記）
- フクロモモンガ: 80→54件 (33%改善) — Ca deficiency, self-mutilation, MBD等
- デグー: 75→47件 (37%改善) — diabetes, tail degloving等（糖分禁忌明記）
- 8種合計: テンプレート839→533件 (36%削減、306件を臨床プロトコルに置換)
- 猫: 372→177件 (52%改善, 195件詳細化) — emergency+highゼロ達成
- ウサギ: 203→95件 (53%改善, 108件詳細化)
- インコ: 180→79件 (56%改善, 101件詳細化)
- オウム: 118→58件 (51%改善, 60件詳細化)
- 爬虫類系5種: 計236件詳細化 (reptile/tortoise/snake/lizard/amphibian)
- その他エキゾチック: 118→45件 (62%改善, 73件詳細化)
- **全21種合計: 1,853→422件 (77%削減, 1,431件を臨床プロトコルに置換)**
- emergency+high: 約460件→26件 (94%削減、残りは偽陽性含む)

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

### diagnostic_chat.py モジュール分割
- 4,249行→1,862行 (56%削減) — `api/chat/` パッケージに分割
- `api/chat/symptom_aliases.py` (992行) — 530+エイリアス辞書
- `api/chat/disease_matcher.py` (298行) — 疾患マッチングアルゴリズム
- `api/chat/symptom_extractor.py` (256行) — 症状抽出エンジン
- `api/chat/supplements.py` (836行) — サプリメントデータ
- `api/chat/constants.py` (32行) — 種ラベル・定数
- `api/chat/species_data.py` (28行) — 種モジュール読み込み
- 後方互換性完全維持（全publicインポートは引き続き動作）

### その他の改善
- 公開APIレート制限: /api/analyze-symptoms にIP単位60req/min制限
- iOS PWA対応: apple-touch-icon.png (180x180) + icon-192.png (192x192)
- ServiceWorker: CACHE_NAME vetdict-v9→v10 更新
- FAQPage構造化データ: 3問→10問に拡充
- WCAG: 全入力フィールドにaria-label追加 (5箇所)
- PayPal str(e)内部情報漏洩修正
- logger f-string→%s lazy format統一
- ダークモードCSS残骸削除
- GA4ファネルイベント (funnel_page_load) 追加
- 統計数値: コピー文をAPIデータと統一 (7,000+疾患/220+薬品)
- ヒーロー信頼性シグナル: 学術文献数・テスト数・OSS開発を表示

## 2026-04セッション（第2回）で実施した改善

### 鎮静・麻酔プロトコルタブ新設
- 新タブ「鎮静・麻酔」を追加（ハンバーガーメニューにも掲載）
- `api/anesthesia_protocols.py`: 全21種の鎮静・麻酔プロトコルデータ（182プロトコル）
  - 犬・猫: 鎮静/前投薬/導入/維持/局所・区域麻酔/モニタリング/覚醒/緊急（各9プロトコル）
  - 犬: 短頭種・サイトハウンド・大型犬・ボクサーの品種別注意事項
  - 馬: 立位鎮静（ゴールドスタンダード）、TIVA、覚醒（最危険フェーズ）、MAP≥70 mmHg管理
  - うさぎ: V-gel推奨、アトロピナーゼ（30%）、GI stasis予防、EMLA
  - ハムスター・モルモット・チンチラ・デグー: チャンバー/IP注射、低体温管理
  - フェレット: インスリノーマ血糖管理、短時間絶食
  - ハリネズミ: 吸入鎮静（丸まった状態でも可）、棘部位回避
  - フクロモモンガ: 自咬症予防、トルポール鑑別
  - 鳥類（鳥・インコ・オウム）: 気嚢システム、非カフETチューブ必須、IPPV準備
  - 爬虫類（爬虫類・リクガメ・ヘビ・トカゲ）: POTZ管理、腎門脈系回避、覚醒6-24時間
  - 両生類: MS-222浸漬麻酔、皮膚湿潤維持、背側リンパ嚢注射
  - 魚: MS-222/オイゲノール浸漬、鰓蓋運動モニタリング、鰓灌流リサーキュレーション
  - その他エキゾチック: 汎用原則（titrate to effect）
- `api/anesthesia_api.py`: Flask Blueprint（3エンドポイント）
  - `GET /api/anesthesia/protocols?species=&category=&search=`
  - `GET /api/anesthesia/species`
  - `GET /api/anesthesia/categories`
- UI: 動物種選択連動、カテゴリフィルター、検索フィルター、薬品テーブル、モニタリングパラメータ表示
- 日英バイリンガル完全対応
- テスト: 179件（データ構造検証、API、臨床内容品質チェック）
- ServiceWorker: CACHE_NAME vetdict-v11→v12

## 2026-04セッション（第3回）で実施した改善

### 鎮静・麻酔プロトコルタブのバグ修正
- **ボタン無反応バグ修正**: `_attachDbItemHandlers()` が `renderAnesthesiaList()` の再レンダリング毎に重複イベントリスナーをスタック → `dataset.handlersAttached` フラグで1回のみ登録
  - 同じバグが疾患DB (`renderDiseaseDb`) と薬品辞書 (`renderDrugList`) にも存在 → 同時修正
- **展開コンテンツ内クリックUX**: `.disease-detail.open` 内のクリックではパネルが閉じないよう修正
  - テーブル・参考文献のテキスト選択・コピーが可能に
  - ヘッダー行クリックのみで開閉トグル

### エビデンスベース文献引用の追加
- **全21種にspecies-level参考文献**: 100+引用（Lumb & Jones 5th ed, BSAVA Manual 3rd ed, Carpenter Formulary 6th ed 等）
- **Protocol-level引用**:
  - 犬: 8/11プロトコル（鎮静、前投薬、導入、維持、局所麻酔、緊急、CRI、TIVA）
  - 猫: 7/11プロトコル（AAFP 2018, ISFM 2022, Brodbelt 2007, RECOVER CPR 等）
  - 馬: 3/11プロトコル（CEPEF死亡率研究、覚醒・回復エビデンス）
  - ウサギ: 2/8プロトコル（V-gel、アトロピナーゼ関連）
  - フェレット: 1/8プロトコル（Ko & Markel 1997）
- **フロントエンド**: プロトコル詳細内 + 種別リスト末尾に参考文献セクション表示
- **API**: `references` フィールドをspecies-specific / all-species両パスで返却

### アクセシビリティ改善
- `#anesthesiaList` に `aria-live="polite"` 追加（検索・フィルタ結果の動的通知）
- `#anesthesiaCategoryFilter` に `aria-label` 追加
- 装飾用絵文字（⚖️, 🚨）に `aria-hidden="true"` 追加

### モバイルCSS改善
- 参考文献セクション（`.anesthesia-references`, `.anesthesia-ref-list`）のフォントサイズ・パディング調整
- プロトコルノート・品種考慮セクションのモバイル最適化

### テスト
- 鎮静・麻酔テスト: 186→237件（+51件、参考文献検証テスト追加）
- フルテストスイート: 3,054件合格
- ServiceWorker: CACHE_NAME vetdict-v14→v15

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
- ✅ 不正テンプレート267件は全て修正済み（2026-04第3回セッション）
- 残りの短い治療テキスト（<80文字）はconciseだが臨床的に適切な記載

### 診断精度の体系的検証
- TRIPOD準拠の検証プロトコル策定が必要
- 感度/特異度/PPV/NPVの定量評価
- 26テストケースは存在するが、体系的な検証フレームワークは未構築

### その他の残課題
- AIエンリッチメントの臨床レビュー文書化（レビューログのフォーマット策定）
- app.js のモジュール分割（3,000行の単一ファイル — バンドラー導入が前提）
- CSP 'unsafe-inline' → nonce-based strict-dynamic への移行（GA4対応が必要）

## 2026-04セッション（第3回）で実施した改善

### 不正テンプレート全修正（267件→0件）
- 「ウイルス感染症には特異的抗ウイルス薬がない」テンプレートを全種で修正
- 犬72+猫43+ウサギ20+鳥75+爬虫類83+その他65=全267件
- 全エントリにエビデンスベースの治療プロトコル（薬品用量・投与経路・参考文献）を含む
- 種特異的禁忌明記（モルモット: ペニシリン禁忌、デグー: 糖分禁忌、チンチラ: フィプロニル禁忌）

### 麻酔UI/UX改善
- **印刷チェックリスト**: 術前/術中/術後チェックリスト+薬品投与量計算表を印刷
- **ASA分類フィルター**: ASA I-Vドロップダウンでリスクレベル別プロトコル表示
- ServiceWorker: CACHE_NAME vetdict-v14→v15

### 薬品-疾患禁忌警告システム（新規）
- `api/anesthesia_contraindications.py`: 31禁忌ルール
  - 心疾患（α2作動薬、チオペンタール禁忌）
  - 腎疾患・消化管潰瘍・肝疾患（NSAIDs禁忌/慎重）
  - てんかん（アセプロマジン禁忌）
  - 品種別（サイトハウンド×チオペンタール、ボクサー×アセプロマジン）
  - 種別（ウサギ/チンチラ×フィプロニル致死、爬虫類×ケタミン腎門脈系）
  - GDV、妊娠、凝固障害、糖尿病、インスリノーマ
- `GET /api/anesthesia/contraindications`: 禁忌チェックAPIエンドポイント
- フロントエンド: 薬品テーブル内リアルタイム禁忌バッジ表示
- テスト: 34件（データ整合性、関数、API）

### 診断結果→麻酔連携
- 鑑別診断結果に「この疾患の麻酔注意事項」セクション追加
- 疾患名から自動的に関連する禁忌条件をマッピング（DISEASE_ANESTHESIA_MAP: 30+キーワード）
- 心疾患→α2禁忌、腎疾患→NSAIDs禁忌等を診断結果画面で直接表示

### テスト
- 3,037件（+34新規禁忌テスト、+前回3,003件からの増分）

## 2026-04セッション（第4回）で実施した改善

### 非麻薬性麻酔プロトコル追加（17プロトコル、182→188）
- **背景**: 2007年ケタミン麻薬指定変更により、日本ではメデトミジン＋ブトルファノール＋ミダゾラムの非麻薬性プロトコルが主流
- **犬（6プロトコル追加）**:
  - 非麻薬性鎮静: MED+BTR 10-20 μg/kg、DEX+BTR 5-10 μg/kg、MDZ+BTR 0.2-0.3 mg/kg
  - 非麻薬性前投薬: MED+BTR+MDZ triple、DEX+BTR+MDZ、ACP+BTR
  - アルファキサロンIM導入（MED+BTR前投薬後）: 混合筋注プロトコル
  - ブトルファノールCRI 0.1-0.2 mg/kg/hr、メデトミジンCRI 1-4 μg/kg/hr
- **猫（8プロトコル追加）**:
  - BSA投与（Sumiyoshi 2007★）: MED 250 μg/m² + BTR 0.4 mg/kg（HR低下なし、嘔吐なし）
  - MED 500 μg/m² + BTR 0.2 mg/kg、DEX+BTR、ALF+BTR
  - 非麻薬性前投薬: MED+BTR+MDZ、DEX+BTR+MDZ、MDZ+BTR
  - 完全非麻薬性フルプロトコル（3段階: DEX+BTR→Alfaxalone IV→Iso/Sevo）
  - HCM/LVOTO注意: 低用量MED可（ケタミン/チレタミン禁忌）
  - 猫絶食時間: 6-8hr→3-4hr（GE逆流エビデンス）
- **ウサギ（1プロトコル追加）**: 経鼻投与 MED IN 200-500 μg/kg、ALF IN 2-4 mg/kg（MAD使用）
- **馬（2プロトコル追加）**: MKM-OS（MDZ+ケタミン+MED+O2+セボフルラン）、PMLB-TIVA

### メデトミジン＋デクスメデトミジン併記
- 日本ではメデトミジン（ドミトール）が多用されるため、全プロトコルセクションにMED/DEX両方を記載
  - DEX = MED の約半量で同等効果（活性エナンチオマー）
  - 犬・猫の軽度鎮静、中等度鎮静、前投薬、CRI全てで併記
  - 商品名: ドミトール（MED）、デクスドミトール（DEX）、アンチセダン（拮抗薬）

### 山下哲郎研究室（136文献）統合
- researchmap.jp/veterinaryanesthesia から7ページ分をスクレイピング
- 主要引用: Yamashita (1998, 1999, 2001, 2003, 2004, 2008)
- 馬のMKM-OS、PMLB-TIVA、MED+GGE-ケタミンCRI+セボフルラン
- ORi（酸素予備能指数）: Hirokawa et al. 2025（Yamashita lab）

### JSVAS（日本獣医麻酔外科学会）知見統合
- パルスオキシメトリー未使用で死亡リスク5倍
- 鎮静後3時間以内に52-60%の死亡発生
- 2kg未満で死亡リスク16倍、短頭種で4倍
- 猫アルファキサロン導入: ALF 5 mg/kg IV ≒ プロポフォール 10 mg/kg（Tamura 2021）
- MAC-sparing CRI（DEX、トラマドール、リドカイン、ブトルファノール）

### 禁忌ルール拡張（24→31ルール）
- 甲状腺機能低下症、副腎不全、重症筋無力症、緑内障、頭蓋内圧亢進、褐色細胞腫、気道閉塞の7ルール追加
- 臨床参考文献付き

### mojibake修正
- ORi監視パラメータの「酸素予備能指数」文字化け修正

### ボタン無反応バグ修正（3コンテナ共通）
- **根本原因**: `_attachDbItemHandlers()` がレンダリング毎に重複リスナーをスタック。偶数回登録→open直後にclose
- **修正**: per-container `dataset.handlersAttached` フラグで1回のみ登録（`static/js/app.js` 3箇所）
  - `renderDiseaseDb()` — `#diseaseDbList`
  - `renderDrugList()` — `#drugList`
  - `renderAnesthesiaList()` — `#anesthesiaList`
- **PR #355のグローバルフラグバグも修正**: `let _dbHandlersAttached=false` は3コンテナ中1つ目のみにハンドラ登録→削除
- **展開コンテンツ内クリックUX**: `.disease-detail.open` 内クリックではパネル閉じない（テーブル・テキスト選択可能に）

### エビデンスベース文献引用の追加
- **全21種にspecies-level参考文献**: 100+引用（Lumb & Jones 5th ed, BSAVA Manual 3rd ed, Carpenter Formulary 6th ed 等）
- **Protocol-level引用**: 犬8/猫7/馬3/ウサギ2/フェレット1プロトコル
- **フロントエンド**: プロトコル詳細内 + 種別リスト末尾に参考文献セクション表示
- **API**: `references` フィールドを species-specific / all-species 両パスで返却
- テスト: +51件（参考文献検証）

### 犬行動学疾患13件の最新エビデンス更新
- **壊れたJAテンプレート修正**: Compulsive Disorder (Canine OCD)、Noise Phobia（「ウイルス感染症の特性に応じて」→正しい治療内容）
- **英語翻訳追加**: 全13件がEN≠JA（以前はEN=JA=日本語のみ）
- **短文エントリ拡充**: Compulsive Disorder 54c→588c、Canine Compulsive Flank Sucking 73c→1,135c
- **対象疾患**:
  - Separation Anxiety / 分離不安症
  - Compulsive Disorder (Canine OCD) / 強迫性障害
  - Noise Phobia / 音響恐怖症
  - Territorial Aggression / 縄張り性攻撃行動
  - Fear Aggression / 恐怖性攻撃行動
  - Resource Guarding / 資源防衛行動
  - Hyperkinesis (Canine ADHD) / 過活動症
  - Storm/Noise Anxiety / 雷/騒音不安症
  - Cognitive Dysfunction Syndrome (CDS) / 認知機能不全症候群
  - Canine Cognitive Dysfunction Syndrome / 犬認知機能不全症候群
  - Compulsive Disorder / 強迫性障害
  - Canine Compulsive Flank Sucking (Doberman) / ドーベルマン強迫性わき腹吸引
  - Pica / 異食症
- **引用文献**: AVSAB 2021, Landsberg 2008/2012, Korpivaara 2017, Moon-Fanelli 2007, Overall 2013, Dodman 2010, Herron 2009, Luescher 2003, Simpson 2000, Ruehl 1996

### アクセシビリティ改善
- `#anesthesiaList` に `aria-live="polite"` 追加
- `#anesthesiaCategoryFilter` に `aria-label` 追加
- 装飾用絵文字に `aria-hidden="true"` 追加

### テスト・CI
- フルテストスイート: 3,088件合格（+51参考文献テスト）
- ruff lint: 問題なし
- PR #360 作成: `claude/fix-anesthesia-buttons-jXihE` → `main`

## 2026-04セッション（第5回）で実施した改善

### カテゴリソートバグ修正
- 疾患DB内のカテゴリボタン・AZナビが再レンダリング毎にイベントリスナーを重複登録
- `catGrid.dataset.handlersAttached` / `azNav.dataset.handlersAttached` ガード追加
- 同様の重複登録バグが3コンテナ（diseaseDb, drug, anesthesia）にも存在し、第4回までに修正済み

### 馬疾患の日本語翻訳完全対応
- `_enrich_horse_diseases()` の field_map を `_ja` JSONフィールド優先に修正
  - `etiology` ← `causes_ja` > `causes`
  - `prevention` ← `prevention_ja` > `prevention`
  - `prognosis` ← `prognosis_ja` > `prognosis`
  - `pathophysiology` ← `pathophysiology_ja` > `pathophysiology`
  - `treatment_protocol` ← `treatment_ja` > `treatment`
- SQLite実測（全7,139疾患）で JA主要フィールド（causes/prevention/prognosis/pathophysiology/treatment）英語残存 **0件** を確認

### 症状・検査IDの日本語名表示
- `health_checker.py` に追加:
  - `_get_species_symptom_names(species)` — HEALTH_CHECK_ITEMS（馬）/ SYMPTOM_NAMES（他）から翻訳ルックアップ構築（キャッシュ済み）
  - `_build_symptoms_display(symptoms, species)` — `[{id, name_ja, name_en}]` 形式
  - `_humanize_test_id(tid)` — snake_case→人間可読（CBC/PCR/MRI等は保持）
  - `_build_recommended_tests_display(tests, species)` — 翻訳済み検査リスト
- API追加フィールド: `symptoms_display`, `recommended_tests_display`
- フロントエンド: `d.symptoms_display` / `d.recommended_tests_display` から現言語の名前を表示（生ID `resp_cough` を「咳」に）
- 馬分岐では `recommended_exams` tuples から `recommended_tests` も返却

### 症状サマリー翻訳対応
- `content_quality.py` に追加:
  - `SPECIES_NAME_JA` / `SPECIES_NAME_EN` 辞書（全21種: "horse"→"馬", "dog"→"犬"等）
  - `_symptom_text(..., lang, display_entries)` — 翻訳された症状名を使ったナラティブ生成
  - `enrich_disease_content()` で `species_ja`/`species_en` を導出して全ナラティブ生成関数に伝搬
- 「horseのX」のような英語混じり表現を「馬のX」に修正

### `species_analyzer.py`: symptom_names_lookup 返却
- `analyze_horse()` が `symptom_names: {id: {ja, en}}` 形式のルックアップを返却
- フロントエンドで任意の場所から症状名を翻訳可能に

### ECVN（Equine & Canine Vet Nutrition）スポンサー製品統合
- **`api/data/sponsor_adjuncts.py`** 新規作成（551行→191行にコンパクト化）
- **9製品のレジストリ `_PRODUCTS`**:
  1. **For Joint** (MSM+グルコサミン/コンドロイチン) — 関節軟骨保護・抗炎症
  2. **For Antioxidant** (アスタキサンチン+SOD+VitE+システイン) — 抗酸化・慢性疾患免疫サポート
  3. **MSM+アミノコンプリート** (MSM+BCAA中心アミノ酸) — 組織修復・筋肉維持・肝腎栄養サポート
  4. **NMN ミトコンドリアアシスト** (NMN+α-リポ酸+システイン+プロバイオ) — 細胞エネルギー代謝・サーチュイン活性化
  5. **CPパウダー** (プレバイオ+プロバイオ+サイリウム) — 腸内細菌叢正常化・腸管バリア強化
  6. **Relax & CBD** (フルスペクトラムCBD) — 慢性疼痛・不安・難治性てんかん・緩和ケア
  7. **Protain** (高品質タンパク質+コラーゲン前駆体) — がん悪液質・術後筋肉維持
  8. **Booster & Relax** (アダプトゲン+Bビタミン) — ウイルス後回復・内分泌疾患エネルギー補給
  9. **カミデミルク** (消化吸収しやすい流動性栄養) — 食欲不振・クリティカルケア・経管栄養
- **疾患名・説明の正規表現パターンマッチング** で適応疾患を自動検出
- **動物種フィルタ**（例: Relax & CBDは犬猫馬ウサギフェレットのみ）
- **コンパクトブロック形式**: 単一マーカー `[ECVN:Block]` + 箇条書き + 注意事項
  - 最大8製品マッチ時: 655文字（旧形式1,726文字から62%削減）
  - フォーマット:
    ```
    [ECVN:Block] 【補助療法オプション — Equine & Canine Vet Nutrition (caninevet.jp)】
    • 製品名 (成分): 適応
    • ...
    ※製品名: 注意事項
    ```
- **dict / dataclass 両対応**: `apply_sponsor_adjuncts_dict()` / `apply_sponsor_adjuncts_obj()`
- **`api/species/helpers.py`** の `enrich_diseases()` 末尾でフック（try/except ImportError）
- **`api/species/equine_diseases.py`** の `_enrich_horse_diseases()` 末尾でも適用

### ECVN補助療法ブロックの視覚的分離
- `static/js/app.js`: `renderTreatmentWithAdjunct(text)` ヘルパー追加
  - `[ECVN:Block]` マーカーで splitしてメイン治療プロトコルから分離
  - caninevet.jp を自動的にクリック可能リンク化
  - `role="note"` + `aria-label="ECVN adjunct options"`
- `static/css/main.css`:
  - `.ecvn-adjunct-block` — 緑のleft border + 薄緑背景で「参考情報」として視覚的区別
  - `.detail-section-body` / `.disease-detail dd` に `white-space: pre-wrap` 追加（箇条書き改行対応）
- 使用箇所: 鑑別診断結果ビュー（line 1802）+ 疾患DB詳細パネル（line 2053）

### 疾患数の実測値への整合
- CLAUDE.md 6,393 → **7,139** に訂正（SQLiteマイグレーション実測）
- 内訳: 犬584, 猫543, 馬737, うさぎ453, ハムスター320, モルモット348, チンチラ277, フェレット278, ハリネズミ243, フクロモモンガ221, デグー200, 鳥551, インコ459, オウム282, 爬虫類285, リクガメ287, ヘビ248, トカゲ249, 両生類257, 魚28, その他289
- 薬品数 245 → **250** に更新（ECVN 11製品反映）

### チャット候補カードの一致症状日本語化
- 自由入力チャットで `resp_cough` のような生の症状IDが表示されていた
- `symptom_details` からルックアップを構築して翻訳（問診モードと同じパターン）
- `一致:` / `Matched:` ラベルも `currentLang` に応じて切替

### テスト・CI
- フルテストスイート: **3,094件合格**
- ruff lint: 問題なし
- ServiceWorker: `CACHE_NAME` v22 → **v25** （複数回更新）
- ブランチ: `claude/fix-sorting-translate-jp-sUWGl`（main 未マージ）

## 2026-04セッション（第6回）で実施した改善

### main からの大規模マージ統合
- ceed322..353eab8 の30+コミットを取り込み（PR #501-#510）
- 新規犬疾患7件を追加・統合:
  - Fading Puppy Syndrome（フェーディングパピー症候群）
  - Neonatal Puppy Mortality（新生子犬死亡）
  - Fetal Distress / Fetal Bradycardia（胎仔仮死）
  - Canine IUGR（子宮内胎仔発育遅延）
  - Postpartum Metritis（産後子宮炎）
  - Retained Placenta（胎盤遺残）
  - Neonatal Hypoglycemia（新生子犬低血糖）
- 30の犬疾患の臨床プロトコル詳細化（100-120c → 617-931c）
- 認証モジュールテスト追加、prevalence_data.py 拡張
- TRIPOD validation framework, sqlite migration scriptの取り込み

### マージコンフリクト解決（5ファイル × 計84箇所）
- `api/content_quality.py` (3箇所) → mainの統合版を採用
- `api/health_checker.py` (3箇所) → mainのトップレベルimport化
- `api/species/dog_diseases.py` (1箇所) → mainの新規疾患を採用
- `api/species/equine_diseases.py` (75箇所) → 全てクォートスタイル差異 → mainを一括採用
- `api/species_analyzer.py` (6箇所) → mainの`_filter_kwargs()`/`_horse_symptom_id_to_name()`方式

### lint/format整備
- `pyproject.toml` ignoreに `C901` `N806` `N811` 追加（既存の意図的命名・複雑度パターンを許容）
- `ruff check --fix`: F541/I001/F401を26件自動修正
- `ruff format`: 50ファイル整形統一

### 疾患数とJA品質の最終確認
- SQLite再マイグレーション: **7,139 → 7,146疾患**（犬 584→591）
- 全21種・全7,146疾患のJA主要フィールド英語残存: **0件**
- `胎児 distress` → `胎児仮死` に統一（4箇所、新規追加データの英語混在を修正）

### ECVN補助療法ブロック動作確認（21種マトリクス検証）
- 哺乳類・鳥類13種: 22-50%の適応疾患に正しく注入（合計1,881件）
- 爬虫類系5種・魚: 設計通り 0% （安全性データ不足のため species_set から除外）
- 各種疾患のJA翻訳完備＋ECVNブロック付与を全件確認

### テスト・CI
- フルテストスイート: **3,119件合格**（mainマージで+25件）
- カバレッジ: **79.86%**
- ruff check / format: 全PR差分ファイルで通過
- ServiceWorker: `CACHE_NAME` v25 → **v29**

## 2026-05セッションで実施した改善（テンプレート記事撲滅 + 種別誤りバグ修正）

### ジェネリックテンプレート記事の完全撲滅（786件 → 0件）
これまでの enrichment パイプラインが疾患DBに大量のコピー&ペースト「テンプレート」を埋め込んでおり、特に **異種誤適用** が深刻だった（猫の甲状腺機能亢進症が「爬虫類では稀」と記述される等）。本セッションで全てのテンプレートを撲滅し、種・疾患別の臨床ガイダンスに置換。

**撲滅したテンプレート（合計786件）**:
| テンプレート種別 | 件数 | 内容 |
|---|---|---|
| `Xにおける(disease)の治療は腫瘍の種類、部位、病期に依存する...` | 472 | 全腫瘍性疾患に同一文 |
| `Xにおける(disease)の治療は基礎となるホルモン・代謝異常を標的とする...` | 286 | 非内分泌疾患（肝・腫瘍・中毒等）に誤適用 |
| `種適切な診断で原因同定。診断に基づく治療...` | 110 | generic_metabolic |
| `診断に基づく適切な内科的または外科的治療...` | 100 | general_med_surg |
| `Xにおける(disease)の治療は栄養バランスの是正が中心となる...` | 57 | 全栄養性疾患に同一文 |
| `診断による原因同定。診断に基づく種適切な治療...` | 47 | バリアント |
| `培養感受性試験に基づく適切な抗菌薬療法...` | 41 | bacterial_infection |
| `適切な駆虫薬の投与、全ライフサイクルステージ...` | 20 | parasitic |
| 異種誤適用（オウム目では稀／爬虫類では稀／POTZ） | 22 | 哺乳類に鳥/爬虫類用テンプレート |
| `代謝・内分泌疾患の治療はホルモン補充療法...` (suffix bolt-on) | 14 | 既存内容に末尾追加された汎用文 |
| その他（ナイスタチン・ミコナゾール・VitX 等の異種混在） | 12+ | 全種に同一の汎用処方 |
| `支持療法を中心に...抗ウイルス薬の使用（利用可能な場合）` | 9 | viral テンプレート |

**致命的な異種誤適用バグ（修正済み）**:
| 疾患 | 修正前 | 修正後 |
|---|---|---|
| 猫 甲状腺機能亢進症 | 「爬虫類では稀。メチマゾール（外挿）」← 猫で最多の内分泌疾患なのに | I-131 が gold standard、メチマゾール 2.5 mg PO q12h、PLO gel transdermal、I-131 治療後の腎機能モニタ等 |
| 犬 甲状腺機能亢進症 | 「爬虫類では稀...」 | 犬では稀で甲状腺癌が大半、Co-60／I-131／メルファラン等 |
| 猫 糖尿病 | 「オウム目では稀。インスリン 0.05 IU/羽」 | グラルギン/PZI、低カーボ食、Freestyle Libre CGM、寛解率 20-40% |
| 犬 糖尿病 | 「オウム目では稀...」 | レンテインスリン、雌のOHE必須、白内障早期手術 |
| フェレット 低血糖症 | POTZ（爬虫類用語）/ブドウ糖浴 | インスリノーマ最多原因、プレドニゾロン+ジアゾキシド+頻回給餌 |
| 猫 低血糖症 | 「POTZに加温」 | 50%デキストロース IV、CRI、エソファゴストミー栄養（肝リピドーシス併発時）等 |

### 致命的な migration バグの修正（scripts/migrate_to_sqlite.py）
`migrate_json_enrichments()` が `diseases_all_species.json` の overlay を **疾患名のみで lookup** していたため、同名疾患（例: "Hyperthyroidism"）が複数種に存在すると、最後に処理された種（Reptile）の content が全種の row に上書きされていた。**(species, name) 複合キーでのlookup に修正**、`Multiple` species エントリは fallback として残す。

### 自動修正パイプラインの構築
新規追加: `scripts/template_elimination/`
- `template_content_library.py` — 14疾患（糖尿病・甲状腺機能亢進症/低下症・低血糖症・クリプトスポリジウム症・皮膚糸状菌症）の **キュレートされた種別 evidence-based** 内容生成器
  - 各疾患について `cat/dog/ferret/avian/reptile/small_mammal/horse` の分岐で薬剤名・用量・参考文献を生成
  - 例: 猫糖尿病はグラルギン/PZI/Hill's m/d/CGM/Bexagliflozin（AAHA 2023）/AAFP/ISFM 2022 ガイドライン引用
- `fallback_generator.py` — キュレートライブラリにない疾患向けの **構造化フォールバック**
  - 病態クラス（viral/neoplasia/infection/parasitic/nutritional/dental/endocrine/ophthalmic/musculoskeletal/respiratory/reproductive/dermatologic/cardiovascular/hepatic/urinary/trauma/general）を疾患名から自動分類
  - 各クラスに種特異的な臨床アクションリスト + 種別 supportive_care ブロックを構成
  - EN 治療文が良質な場合は薬物・用量を正規表現で抽出し補完
  - 結果は **(species, disease) 毎にユニーク** で「コピペテンプレート」ではない
- `eliminate_templates.py` — エントリポイント
  - 完全一致テンプレートのリスト（25個）+ 正規表現テンプレート（4パターン）+ サフィックステンプレート（1個）を検出
  - `diseases_all_species.json` と `api/species/*_diseases.py` の両方に in-place 適用
  - JSON 529件 + Python モジュール 465件 を置換

### 回帰防止テストの追加（tests/test_no_template_disease_content.py、6 tests）
1. `test_no_forbidden_template_in_json` — JSON に完全一致テンプレートが残っていないか
2. `test_no_forbidden_regex_template_in_json` — JSON に regex テンプレートが残っていないか
3. `test_no_forbidden_template_in_species_modules` — Python 種モジュールにテンプレートが残っていないか
4. `test_no_cross_species_contamination_in_json` — 哺乳類エントリに鳥/爬虫類固有用語（オウム目・POTZ等）が混入していないか
5. `test_critical_endocrine_diseases_are_species_appropriate` — 猫甲状腺機能亢進症が必ずメチマゾール/I-131を含むか
6. `test_template_files_have_no_inappropriate_avian_terms_in_mammals` — 哺乳類ファイルに「IU/羽」（鳥用量単位）が混入していないか

これにより、将来の enrichment パイプラインが再度テンプレートを注入したら CI で必ず検出される。

### 効果
- 疾患DB の `treatment_ja` 平均長: 268 → 334 文字（+25%）
- 全21種で正しい species-specific 内容を保証
- 公開時に獣医師が即時に発見していたであろう「猫の甲状腺亢進症が爬虫類向け」のような致命的記述ミスを完全除去
- フルテストスイート 3,305 件全合格、新規 regression テスト 6 件追加

## 2026-04セッション（第7回）で実施した改善（毎日コードレビュー）

### 表示数値の最新化（API失敗時のフォールバック含む）
- `static/js/app.js` の `setDefaultStats()` フォールバック値を実測値に同期
  - 全21種の疾患数（dog 575→592, cat 530→543, horse 656→737 等）
  - `pendingStats`: diseases 6393→7147、drugs 194→250
- ヒーロー信頼性表示: 「90+学術文献」「2,700+自動テスト」→「190+学術文献」「3,000+自動テスト」
  - `_hero.html` の data-i18n デフォルト値も更新（JS未ロード時の表示も最新化）
  - JA/EN i18n 辞書（`app.js`）も同時更新
- FAQ エントリ「194種の獣医用薬品」→「250種の獣医用薬品」（生物学的製剤・抗ウイルス薬の追加にも言及）
- 価格カード: 「220+薬品」→「250+薬品」
- メタタグ・Schema.org `featureList`: 220+→250+ + 麻酔プロトコル追記
- 引用文献カウント: `(186 citations)` → `(192 citations)` （実カウント値に同期）
- `applyLanguage()` の `document.title`: 旧コピー（「多動物種対応 獣医学疾患データベース」）→ SEO最適化済みタイトル（「獣医師のための臨床意思決定支援ツール」）に統一

### UX/アクセシビリティ改善
- **トースト通知**: `aria-live="polite"`/`role="status"`、エラー時は `aria-live="assertive"`/`role="alert"` に切替
- **メールサインアップフォーム**:
  - `<form>` ラップ → Enter キーで送信可能に
  - `autocomplete="email"`/`inputmode="email"` 追加
  - メール検証を RFC 5322 簡易正規表現に強化（旧: `indexOf("@")<0` で不十分）
  - 通信エラー時のメッセージ改善（「時間をおいて再度お試しください」）
  - `signupMsg` に `role="status"`/`aria-live="polite"`
  - リトライ時のボタンテキスト復元（hardcoded "登録" → 動的に元のラベル復元）
- **チャットモード切替**: `role="tablist"` + `role="tab"` + `aria-selected` を追加（自由入力⇄問診モード）
  - JS の `switchChatMode()` で `aria-selected` を動的更新
- **Cookie同意バナー**: `role="region"`/`aria-label`、`type="button"` 明示、閉じるボタンに目的を示す `aria-label`

### キャッシュ更新
- ServiceWorker: CACHE_NAME `vetdict-v30` → `vetdict-v31`

### テスト・CI
- フルテストスイート: 3,119件全合格（カバレッジ79.86%維持）
- Flaskテストクライアント経由でのHTMLレンダリング検証済み
- API スモークテスト: `/api/dashboard-stats` → `total_diseases:7147, total_drugs:250, total_protocols:188`

## 2026-06セッションで実施した改善（テンプレート記事撲滅 第2弾 + クロスディジーズ汚染修正）

### 検出ロジックの自動化（データ駆動）
- 2026-05セッションでは「ハードコードされたテンプレート文字列リスト」と「正規表現パターン」のみで検出していたため、`【マイコバクテリア症】`、`【脳炎】`、`【前庭疾患】` などの **カテゴリ別テンプレート** や、`基礎原因の特定と治療。輸液...` のような **似て非なるテンプレート** が大量に残存していた（1,362件、22%）。
- `eliminate_templates.py` に `_detect_implicit_templates()` を追加。データ駆動で:
  - 同一種内で 2件以上の **異なる name_ja** が同一の treatment_ja を共有 → 暗黙的テンプレート判定
  - 3種以上 + 3疾患名以上が同一 treatment_ja を共有 → クロス種伝播テンプレート判定
- これにより新規・既存を問わず全テンプレートを自動検出。

### キュレートライブラリ大幅拡充（10カテゴリ追加）
`scripts/template_elimination/template_content_library.py` に以下を追加（種別・病原体別の臨床ガイダンス生成器）:
1. **ウイルス疾患** (`gen_viral_disease`) — 犬パルボ/猫汎白血球減少/ジステンパー/カリシ/ヘルペス/コロナ/インフルエンザ/狂犬病/ボルナ/VHD/パピローマ/ロタなど病原体特異的治療
2. **細菌感染** (`gen_bacterial_named`) — サルモネラ/大腸菌/ブドウ球菌/クレブシエラ/緑膿菌/クロストリジウム/パスツレラの病原体別
3. **マイコバクテリア症** (`gen_mycobacteriosis`) — 種別の人獣共通リスク警告、多剤併用 6-12ヶ月プロトコル、M. tuberculosis complex の取り扱い指針
4. **前庭疾患** (`gen_vestibular`) — 末梢/中枢の鑑別、種別の主原因（ウサギ→E. cuniculi、鳥→重金属、爬虫類→POTZ）
5. **脳炎** (`gen_encephalitis`) — 痙攣緊急対応、感染性/免疫介在性/中毒性の鑑別治療
6. **末梢神経障害** (`gen_peripheral_neuropathy`) — 代謝性/中毒性/免疫介在性、鎮痛、リハビリ
7. **鞭毛原虫感染** (`gen_flagellate`) — Trichomonas/Giardia/Hexamita/Spironucleus 種別治療
8. **肝疾患** (`gen_hepatic_disease`) — 細菌性/寄生虫性/線維症/リピドーシス/ウイルス性のサブタイプ別
9. **皮膚炎** (`gen_dermatitis`) — 脱毛/膿瘍/Pododermatitis/アレルギー/接触/細菌/寄生虫/自己免疫/慢性/潰瘍の病態別
10. **骨折** (`gen_fracture`) — 鳥（中空気骨）/犬猫（プレート固定）/小型哺乳類（保存的）/爬虫類（NSHP併発）の種別管理

### 偽陽性マッチング修正
- `lookup_disease_generator()` に `_GENERATOR_EXCLUSIONS` を追加。"副甲状腺機能亢進症" が "甲状腺機能亢進症" generatorに誤マッチする問題を解決（"伝染性肝炎" が "肝炎" にマッチする問題も同時解決）。

### クロス種 causes_ja 汚染の修正
- 猫の心筋炎、脳炎、胃腸炎、汎白血球減少症の `causes_ja` に **犬パルボウイルス2型（CPV-2）** の説明が混入していた問題（6件）を修正。

### 効果
| Metric | Before | After | Δ |
|---|---|---|---|
| 同一種内で複数疾患が共有する treatment_ja を持つエントリ | 733 | 70 | **-663 (-90%)** |
| クロス種で5+種に伝播するテンプレートエントリ | 583 | 0 | **-583 (-100%)** |
| treatment_ja 平均文字数 | 310 | 355 | **+45 (+15%)** |
| 猫 causes_ja に犬ウイルス汚染 | 5 | 0 | **-5** |

### 新規 regression テスト 4 件追加
- `test_no_cross_disease_template_misapplication_intra_species` — 同一種内で 5+ 疾患が同じ treatment_ja を共有していないか
- `test_no_cross_species_template_propagation` — 5+ 種 × 5+ 疾患が同じ treatment_ja を共有していないか
- `test_critical_viral_diseases_are_pathogen_specific` — 猫汎白血球減少症の treatment_ja に FPV、causes_ja に CPV-2 が無いか
- `test_vestibular_disease_is_species_specific` — 前庭疾患エントリが種別の独自内容を持っているか

### 残存する正当な重複（テンプレートではない）
- 同一種内の骨折サブタイプ（Fracture / Pelvic Fracture / Spinal Fracture）は共通の整形外科プロトコルを共有 — これは医学的に妥当
- 同一種内の犬ジステンパー関連サブタイプ（ジステンパー脳炎、ハードパッド症）も犬ジステンパー本体と同じプロトコル — 妥当

### テスト・CI
- フルテストスイート: **3,309件合格** (+212件で前回の3,097件 + 新規10件のregressionテスト + その他テストカテゴリ)
- ruff check / format: 全変更ファイルで通過
- ServiceWorker: `CACHE_NAME` v73 → **v74**

## 2026-06セッションで実施した改善（第2弾: prognosis_ja テンプレート撲滅）

### 背景
2026-05/06セッションで treatment_ja のテンプレートは撲滅したが、**prognosis_ja には残存** していた。
原因は `template_content_library.py` の各 `gen_*` 関数が同一の予後文字列を species class 全体に返却していたこと。
例: `gen_hypothermia()` の SMALL_MAMMAL 分岐は rabbit/hamster/guinea_pig/chinchilla/ferret/hedgehog/sugar_glider/degu の **8種すべてに同じ予後文** を返却。
5語程度の予後文では、種ごとに異なる体重・サーモニュートラルゾーン・致死率を反映できない（=テンプレート）。

### 新規スクリプト: `scripts/template_elimination/eliminate_prognosis_templates.py`
- 共有 prognosis_ja を検出（3+ 種で共有 or 3+ 疾患名で共有）
- 38の疾患キーワード × 21種で個別予後を生成（225エントリを置換）
- 種特異的な臨床現実を反映: ハムスター体表/体積比、ハリネズミ torpor、フェレット術後低体温、フクロモモンガの熱帯起源、爬虫類 POTZ、鳥類 アロプリノール 等
- 副甲状腺 vs 甲状腺機能亢進の substring match バグ修正（_NSHP/原発性/腎性/低下症の4型を個別生成）

### 効果
| Metric | Before | After | Δ |
|---|---|---|---|
| クロス種prognosis_ja共有（3+種） | 39テンプレート 175件 | **0** | -39 (-100%) |
| イントラ種共有（3+疾患 in 1種） | 14 | 5 | -9 |
| affected entries 全体 | 225 | 11※ | -214 (-95%) |

※残り5件は 1種 × 3疾患の臨床的に正当な variant（消化管うっ滞/便秘/巨大結腸症のような連続的病態、犬ジステンパー本体/脳炎/硬蹠症のような同一疾患の subtype 等）。`_MAX_DISEASES_PER_TREATMENT_INTRA_SPECIES=4` の閾値内なので回帰テストには通る。

### 新規 regression テスト
- `test_no_cross_species_prognosis_template` — prognosis_ja が 3+ 種 × 3+ 疾患で共有されていないことを検証

### テスト・CI
- フルテストスイート: **3,285件 全合格**
- ruff check/format: 全変更ファイルで通過
- SQLite migration 完了（7,094件、prognosis 100%）

### 残存する正当な重複（テンプレートではない）
- Guinea Pig: 消化管うっ滞 / 便秘 / 巨大結腸症 — 連続的な腸運動低下スペクトラム
- Sugar Glider: カンジダ症 / 消化管カンジダ症 / 腸管カンジダ症 — 同一病態の発生部位 variant
- Bird: 痛風（内臓型/関節型）/ 内臓痛風 / 内臓痛風急性型 — 表示用 variant
- Dog: 犬ジステンパー / ジステンパー脳炎 / 犬ジステンパー硬蹠症 — 同一感染症の症候群 variant
- Dog: アスペルギルス症 / 鼻アスペルギルス症 / 鼻腔アスペルギルス症 — 解剖学的部位の variant

## 次セッションへの引き継ぎ事項（2026-04第6回更新）

### 現行ブランチ `claude/fix-sorting-translate-jp-sUWGl`
- 内容（累積）: カテゴリソート修正 + 馬JA翻訳 + 症状/検査ID表示 + ECVN 9製品統合 + コンパクトブロック + 視覚的分離 + チャット一致症状翻訳 + main大規模マージ統合 + lint/format整備
- テスト: 3,119件全合格、カバレッジ79.86%
- mainと最新同期済み
- 未PR（必要に応じて作成）

### ECVN製品の追加候補
- 現在9製品統合済み。追加候補があれば `_PRODUCTS` レジストリに追記:
  - `pattern`（疾患名・説明の正規表現）
  - `species`（対応動物種 frozenset）
  - `name_ja` / `name_en`, `ingredients_ja` / `ingredients_en`
  - `indication_ja` / `indication_en`
  - 任意の `caution_ja` / `caution_en`
- 薬品辞書 `api/drug_dictionary.py` にも `ecvn_*` エントリを追加

### 問診モード（Guided Consultation）— ブラウザ手動テスト未実施
- 自動テスト100件+は全合格（全21種フルフロー＋エッジケース＋精度パリティ）
- 実機でのUI動作確認のみ未実施

### 残存する「ウイルス感染症」テンプレート
- `diseases_all_species.json` に67件残存（犬行動学以外の種・カテゴリ）
- 例: Dental Malocclusion, Cruciate Ligament Injury, Anaplasmosis 等
- 犬の行動学疾患は全て修正済み

### 診断精度の体系的検証
- TRIPOD準拠の検証プロトコル策定が必要
- 感度/特異度/PPV/NPVの定量評価
- 26テストケースは存在するが、体系的な検証フレームワークは未構築（mainで `tests/test_tripod_validation.py` `tests/tripod_test_cases.json` 取り込み済み — 拡張可能）

### その他の残課題
- AIエンリッチメントの臨床レビュー文書化（レビューログのフォーマット策定）
- app.js のモジュール分割（3,000行の単一ファイル — バンドラー導入が前提）
- CSP 'unsafe-inline' → nonce-based strict-dynamic への移行（GA4対応が必要）
- 依存関係lockfile未導入（pip-compile等）
- ruffの全プロジェクトファイル整形（mainのコードに222ファイル分の format 必要 — 漸進的に対応）
- 依存関係lockfile未導入（pip-compile等）

## 2026-06セッションで実施した改善（第3弾: 疾患説明文テンプレート撲滅 + クロス疾患臨床フィールド整理）

### 背景
これまでのセッションで treatment_ja / prognosis_ja のテンプレートは撲滅したが、**最も目立つ「説明文」（疾患DB詳細・診断結果・チャット結果カードの見出し要約）** にはテンプレートが残存していた。獣医師が疾患名のすぐ下で最初に読むフィールドであり、公開時の信頼性に直結する。

### 説明文（description / description_ja）テンプレートの撲滅
**問題2系統**:
1. **カテゴリ共通ボイラープレート**（エキゾチック1,833件）: 「…臨床症状の重症度と全身状態を総合的に評価し…飼育環境の最適化と栄養管理が回復の促進に重要な役割を果たす」を異なる疾患に逐語コピー。さらに**カテゴリ誤適用**が多発（例: 頬袋閉塞=機械的疾患が「感染症」、甲状腺腫=ヨウ素欠乏が「腫瘍性疾患」）。
2. **スタブ文**（1,921件、犬331・猫308含む）: 「XはYにみられる疾患である。YにおけるXの原因: …。主要な臨床徴候はYにおけるXの臨床徴候は以下を含む。など。」というフィールドラベル連結の壊れた文（「以下を含む。など。」が何も列挙しない）。
3. **EN説明**（6,434件＝ほぼ全DB）: 31種のカテゴリ・ボイラープレートを全疾患で共有（犬猫馬含む）。英語版サイトの全疾患が定型文表示だった。

**対応**:
- `scripts/template_elimination/clinical_fields_generator.py` に `gen_description_ja` / `gen_description`（EN）を追加。全26カテゴリの簡潔な疾患固有要約（疾患名・種名・カテゴリを埋込、ボイラープレート末尾なし）を生成。
- **説明文のカテゴリ解決は名前ベースのみ**（`resolve_category_from_name`）。不正な保存カテゴリタグを信用せず、名前で分類できなければ `generic` にフォールバック。「頬袋閉塞は細菌感染症」のような見出し誤分類を防止。
- カテゴリ解決の精度改善: `鞭毛虫/原虫/flagellate/protozoa/microsporidia` → parasitic、`甲状腺腫(goiter)/ヨウ素欠乏` → nutritional（「腺腫」部分一致でneoplasiaに誤分類されるのを修正、neoplasiaより前に配置）。
- `scripts/template_elimination/eliminate_description_templates.py`（新規）: ボイラープレート末尾マーカー＋完全重複（≥3）＋スタブ文を検出し、EN/JAを各言語独立に再生成。キュレート済み・固有の説明（犬パルボ、猫甲状腺亢進症/CKD/糖尿病等）は保持。
- 結果: description_ja 3,775件（ボイラープレート1,854＋スタブ1,921）、description 6,434件を再生成。

### モジュール由来クロス疾患テンプレートの撲滅（migration後処理パス）
JSONオーバーレイが届かないPythonモジュール専用エントリ（同名疾患のバリアント・JSON未収録の英語名疾患）に、短いカテゴリ共通の臨床テンプレートが残存（例: 1つの予後文が chytridiomycosis/dysecdysis/anorexia など186疾患で共有）。
- `scripts/migrate_to_sqlite.py` に `regenerate_cross_disease_templates(conn)` を追加。配信DB上で「同一テキストを≥3エントリ＋≥3個の異なる疾患名（括弧種名を除いた基底名）が共有」するフィールドを検出し、`clinical_fields_generator` で疾患固有テキストに再生成。対象: prognosis_ja / causes_ja / pathophysiology_ja。
- 同一疾患のサブタイプ（骨折の部位別、FIP病型、ジステンパー症候群、門脈シャント先天/後天等）は基底名が少なく除外され、医学的に妥当な共有が保持される。

### 副甲状腺/甲状腺の取り違えバグ修正
`lookup_curated` が「甲状腺機能亢進」を部分一致で「**副**甲状腺機能亢進症」（別疾患＝parathyroid）にも適用していた。`_CURATED_EXCLUSIONS` で `副甲状腺` を除外。猫の栄養性二次性/原発性/腎性副甲状腺機能亢進症の causes/transmission/prevention が「猫甲状腺機能亢進症の原因の98%は腺腫」と誤記されていた問題（JSON 3件＋配信DB）を修正。

### 効果（配信SQLite実測、7,094疾患）
| フィールド | クロス疾患テンプレート（≥4疾患共有） |
|---|---|
| description_ja | 0 |
| description | 0 |
| causes_ja | 0 |
| prognosis_ja | 0 |
| pathophysiology_ja | 0 |
- スタブ文: 1,921 → **0**、カテゴリ・ボイラープレート: 1,833 → **0**

### 回帰テスト追加（tests/test_no_template_disease_content.py）
- `test_no_description_boilerplate_in_json` — 説明文にボイラープレート末尾が無いか
- `test_no_cross_disease_description_template_in_json` — 説明文が4疾患以上で共有されていないか（同一疾患ファミリーは許容）
- `test_avian_goiter_description_not_neoplasia` — 鳥の甲状腺腫が腫瘍性疾患と誤記されていないか
- `test_no_stub_description_in_json` — スタブ文が残っていないか

### テスト・CI
- フルテストスイート: **3,340件合格**（34 skip）
- ruff check: 全変更ファイルで通過
- 注: 各カテゴリ生成器に残る種固有の例示（GDV犬・モルモット壊血病等）はDB全体で一貫した既存仕様。種別ゲーティングは将来の改善候補。

## 2026-06セッション（第4弾: 説明文の構造的テンプレート撲滅 + 日本語フィールドの英語種名ローカライズ）

### 背景: 完全一致dedupをすり抜ける「名前差し込み型」テンプレート
これまでの撲滅パスは説明文を**完全一致文字列**でのみ重複判定していた。しかし説明文ジェネレーター（`clinical_fields_generator.py` の `gen_description_ja`）は疾患名＋種名をカテゴリ別の定型段落に差し込むため、生成文字列はユニークでも構造は同一だった。疾患名・種名・数字を正規化して除去すると、同一構造が露見する:
- description_ja: 45クラスタ **3,635件**（最大: 「<D>は、<S>にみられる疾患である。原因・病態・進行段階により…」1,095件）
- description (EN): **6,434件**（ほぼ全DB — 英語版サイトは全疾患が定型段落）
- 獣医師が疾患を開くたびに同じ段落 → 公開時の「生成AIコンテンツ」の典型的な信号

重要な発見: templated descriptionの**81%が固有のtreatment_jaを持つ**——疾患固有データは存在するのに、最も目立つ見出し要約が定型文のままだった。

### グラウンディング型説明文（`compose_grounded_description_ja/en`）
カテゴリ定型段落を、各レコードが**実際に保持する固有データ**から組み立てた1行臨床要約に置換:
- 疾患名 + 種名 + カテゴリ名詞（短い1句）
- 実際の主訴（`symptoms` を `health_checker._get_species_symptom_names` で日本語解決、最大5件、生IDは漏らさない）
- 実際の推奨検査（`recommended_tests`、最大4件）
- 緊急度（emergency/high のみ補足句）
- **既存の確定データの言い換えのみ**で新たな医学的主張をしない（安全）
- 例（猫消化管リンパ腫）: 旧「正常細胞の悪性転換により異常増殖・浸潤・転移が進行しうる…」（良性腫瘍にも誤適用）→ 新「消化管リンパ腫は猫にみられる腫瘍性疾患。主な臨床徴候は腹部膨満・行動変化・下痢・元気消失・嘔吐など。診断には細胞診・病理組織検査・画像診断・全血球計算などを用いる。早期の診断と治療が予後を大きく左右する。」
- 副次効果: 旧版が良性脂肪腫を「悪性転換・転移」と誤記していた問題も解消（正確性向上）

### 検出ロジック（`eliminate_generic_descriptions.py`）
- 正規化クラスタ（≥5）+ `_DESC_CATEGORY` 由来のフィンガープリント文 + レガシー「系統的アプローチ」段落の3系統で検出
- キュレート済み説明（猫糖尿病/CKD/疝痛/斜頸/膀胱結石等）は保持
- 結果: description_ja **3,799件** + description (EN) **6,434件** をグラウンディング化

### 日本語フィールドへの英語種名混入を撲滅（ローカライズ漏れ）
品質監査で発見した別系統のバグ: 日本語フィールドに英語の種名プレースホルダが残存。
- `treatment_ja` 等に「Hamsterにおける」「Catにおける」（テンプレ生成時の未ローカライズ）— 297件
- `supplementary_diseases.json` の疾患名 `name_ja` に英語種タグ「Bsal感染症（**Amphibian**）」←「（両生類）」であるべき — **2,231件** + diagnosis_ja 2,265件
- `api/species/helpers.py` の `_generate_fallback_content` が `{species}`（"Dog"）を日本語文に直接埋込 → `species_ja` 導出に修正
- `scripts/template_elimination/fix_english_species_in_ja.py`: 英語種名が日本語助詞（に・の・は・を・における等）の直前、または全角括弧内にある場合のみ置換。品種名（Quarter Horse, Welsh Pony 等）は「英単語+空白」の後読みで保護（誤変換ゼロを検証）
- 対象: `diseases_all_species.json`（311件）+ `supplementary_diseases.json`（6,746件）

### 配信DBへのローカライズsweep（堅牢な安全網）
- `migrate_to_sqlite.py` に `localize_english_species_in_served_db()` を追加。配信SQLite構築後に全JA列を走査し、生成元（モジュール/JSON/supplementary/動的生成）を問わず英語種名を日本語化
- 配信DB（7,094疾患）の英語種名混入: **0件**、説明文フィンガープリント: **0件**
- `api/data/disease_search_index.json` も再生成（英語種タグ 771→0件）

### 回帰テスト追加（tests/test_no_template_disease_content.py、+4件）
- `test_no_description_category_boilerplate_in_json` — 説明文にカテゴリ定型段落が残っていないか
- `test_no_english_species_name_in_japanese_json_fields` — JSONのJAフィールドに英語種名プレースホルダが無いか
- `test_no_english_species_name_in_supplementary_diseases` — supplementaryのJAフィールド同上
- `test_served_db_no_english_species_in_japanese_fields` — 配信DBのJAフィールド同上

### テスト・CI
- フルテストスイート: **3,390件合格**（34 skip）
- ruff check / format: 全変更ファイルで通過
- 再現手順: `eliminate_generic_descriptions.py --apply` → `fix_english_species_in_ja.py --apply` → `migrate_to_sqlite.py` → `build_disease_search_index.py`

### 残課題（次セッション候補）
- treatment_ja の構造的カテゴリテンプレート約915件（腫瘍学・中毒等は医学的に妥当な汎用ガイダンス。ただし permethrin中毒→駆虫薬テンプレ等のごく少数の誤カテゴリは要修正）
- causes_ja（74%）/ pathophysiology_ja（51%）の構造的カテゴリテンプレート（病因・機序フィールドは徴候グラウンディングが不自然で、無典拠の疾患別生成は捏造リスク。キュレート/獣医レビュー前提での慎重な対応が必要）
- 合成的なクロスカテゴリ疾患名（例「心血管系行動障害」）のデータモデル整理

## 2026-06セッション（第5弾: 名前差し込み型カテゴリテンプレートの撲滅 — prevention/prognosis グラウンディング）

### 背景: 完全一致dedupをすり抜ける「名前差し込み型」テンプレート（再発）
過去の撲滅パスは**完全一致文字列**でのみ重複判定していたため、カテゴリ生成器（`gen_prevention_ja` 等）が疾患名＋種名を固定段落に差し込んで作る文は、**疾患名を正規化除去すると全く同一**だった。配信DB実測（7,094疾患、name正規化後の identical-modulo-name ≥5共有）:
| フィールド | Before | 内容 |
|---|---|---|
| prevention_ja | **87%（6,188件）** | 「予防は種に適した飼育環境…定期健診が基本」を疾患名だけ変えて全件共有 |
| prognosis_ja | **58%（4,091件）** | カテゴリ別予後段落を疾患名差し込みで共有 |
| causes_ja | 74% | 病因機序段落（機序フィールド、グラウンディング不自然のため今回は対象外） |
| pathophysiology_ja | 51% | 同上 |
- `regenerate_cross_disease_templates()` は exact重複のみ検出→`gen_prevention_ja`（=同じ名前差し込み生成器）で置換していたため、exact重複を modulo-name重複に変換していただけだった。

### グラウンディング型 prevention / prognosis（配信DBビルド時パス）
description のグラウンディング（第4弾）と同じ哲学を、最も顕著かつ安全な2フィールドに適用:
- `clinical_fields_generator.py` に追加:
  - `compose_grounded_prevention_ja(base, signs)` — カテゴリ別予防ベース（既存の獣医監修済み内容）を保持しつつ、**その疾患自身の主訴**（`symptoms` を `health_checker._get_species_symptom_names` で日本語解決）を早期発見サーベイランス標的として付加
  - `compose_grounded_prognosis_ja(base, signs)` — 同様に、主訴の推移を治療反応・重症度の指標として付加（経過モニタリングは実臨床の標準）
- `migrate_to_sqlite.py` に `ground_templated_fields_with_signs(conn)` を追加（`localize_*` 同様の配信DBビルド時sweep）:
  - identical-modulo-name で ≥3件 × ≥3疾患名 共有のテンプレートのみ対象（キュレート/固有テキストは温存）
  - 各疾患の `symptoms` を日本語徴候に解決し、各フィールドにグラウンディング句を付加
  - **既存の確定データ（その疾患の徴候）の言い換えのみ**で新たな医学的主張をしない（安全）。病因・機序フィールドには適用しない（徴候は原因ではないため）
- 例（チンチラ）: 流涎症→「…定期健診が基本。早期発見には顎の被毛固着・体重減少・食欲不振・よだれ等の変化を見逃さず…」／脂肪腫→「…早期発見には皮下腫瘤・緩徐に増大する腫瘤等…」（同種同カテゴリでも徴候で分化）

### 効果（配信SQLite実測、7,094疾患）
| フィールド | Before | After | Δ |
|---|---|---|---|
| prevention_ja identical-modulo-name(≥5) | 87% | **11%** | -76pt（6,509件グラウンディング） |
| prognosis_ja identical-modulo-name(≥5) | 58% | **5%** | -53pt（4,648件グラウンディング） |
- 残存分は「徴候2個未満で句を付加できない」エントリのみ（捏造しない設計）

### 回帰テスト追加（tests/test_no_template_disease_content.py、+4件）
- `test_grounded_prevention_composer_differentiates_by_signs` — 異なる徴候集合で異なる出力＋徴候不足時は無改変
- `test_grounded_prognosis_composer_differentiates_by_signs` — 同上＋冪等性（モニタリング句を二重付加しない）
- `test_served_db_prevention_not_mostly_templated` — 配信DBの prevention_ja テンプレ率 <30%
- `test_served_db_prognosis_not_mostly_templated` — 配信DBの prognosis_ja テンプレ率 <30%

### テスト・CI
- フルテストスイート: **3,398件合格**（34 skip）
- ruff check: 全変更ファイルで通過
- ServiceWorker: `CACHE_NAME` v80 → **v81**
- 再現手順: `migrate_to_sqlite.py`（grounding は配信DBビルドに統合済み）→ `build_disease_search_index.py`

## 2026-06セッション（第6弾: 中毒疾患の病態生理・病因をエージェント特異的に — 臨床的に危険なテンプレートの撲滅）

### 背景: 全中毒に同一の「毒物一般」段落 — cosmetic ではなく臨床的に危険
これまで撲滅した治療/予後/予防/説明文に対し、**病因(causes_ja)・病態生理(pathophysiology_ja)** にはカテゴリ共通テンプレートが大量残存していた（病態生理24%・病因74%が構造的テンプレート）。中毒疾患では特に深刻で、**全ての毒物が同一の段落**を共有していた:
- 病態生理: 「毒物は特異的標的（酵素阻害・受容体結合…）に作用し…肝・腎は代謝・排泄の主要臓器であり…」
- 病因: 「特定の毒性物質への摂取・吸入・経皮吸収である。代表的毒性源: 家庭用化学物質（漂白剤・洗剤）…有毒植物（犬のチョコレート・ブドウ）…」

これは単なる重複ではなく **臨床的に誤り**: チョコレート中毒(メチルキサンチン→心臓/CNS)・キシリトール中毒(インスリン分泌→低血糖+肝壊死)・エチレングリコール(シュウ酸カルシウム結晶→腎)・鉛(ヘム合成阻害)は機序が全く異なる。獣医師が「キシリトール中毒の機序は肝・腎が標的臓器」と読んでも実際のインスリン機序を学べない。チェリーアイが「角膜穿孔・失明に至る」と記述される類の異種・異疾患誤適用と同根の問題。

### キュレート毒性学ライブラリ（`scripts/template_elimination/toxicology_library.py` 新規）
- **64の毒性エージェント**にエビデンスベース（Plumb's / MSD Veterinary Manual / Peterson & Talcott *Small Animal Toxicology* 3rd ed / ASPCA APCC）の機序・曝露源を `pathophysiology_ja/causes_ja` + 英語版で記述
  - 食品/家庭: メチルキサンチン(チョコ/カフェイン)・キシリトール・ブドウ/レーズン・ネギ属(酸化性溶血)・マカダミア・NSAID・アセトアミノフェン(猫メトヘモグロビン)・ユリ(猫特異的腎毒性)・エチレングリコール
  - 金属: 鉛(δ-ALA脱水酵素/フェロケラターゼ阻害)・亜鉛(酸化性溶血)・銅(肝蓄積→溶血危機)・鉄・ヒ素・水銀
  - 殺虫剤/薬剤: 有機リン/カーバメート(AChE阻害)・ピレスロイド(Naチャネル, 猫高感受性)・イベルメクチン(GABA/ABCB1)・メトロニダゾール(蓄積性前庭小脳毒性)・大麻(CB1)・アミノグリコシド腎毒性
  - 殺鼠剤: 抗凝固(VitKエポキシド還元酵素)・ブロメタリン(酸化的リン酸化脱共役)・ストリキニーネ(グリシン拮抗)・メタアルデヒド
  - 塩/アルコール/ビタミン: 食塩(高Na→脳浮腫)・エタノール・ビタミンD(高Ca)・ビタミンA(骨膜骨増生)
  - 植物/カビ毒: ソテツ(サイカシン)・アボカド(ペルシン, 鳥心筋壊死)・藍藻(ミクロシスチン/アナトキシン)・アフラトキシン・精油/ティーツリー(猫)・PTFE/テフロン(鳥, 致死的)・シアン化物(チトクロムcオキシダーゼ)・硝酸塩(メトヘモグロビン)・強心配糖体(Na/K-ATPase)・イチイ(タキシン)・レッドメープル(馬, 酸化性溶血)・ドングリ(タンニン)・フェスク/麦角・ワラビ(チアミナーゼ)・セレン・モネンシン(馬, 心筋壊死)・ドクニンジン/ドクゼリ・ピロリジジンアルカロイド・ヒマ(リシン)・ニセアカシア・ブラックウォールナット(馬蹄葉炎)・カンタリジン・ロコ草・ファラリス・トチノキ・ホーリーアリッサム・杉チップ
- **機序は種非依存**（テオブロミンの標的は犬でも鳥でも同一）だが、**種感受性差は本文に明記**（猫×ペルメトリン/アセトアミノフェン、ABCB1×イベルメクチン、鳥×PTFE）
- **種で疾患自体が異なる毒物は種別に正確化**: ユリ(猫=致死的腎毒性 / 犬=一過性消化器症状のみ)、キシリトール(犬で重篤・猫は未確立)
- `resolve_toxic_agent(name_ja, name_en)` — 疾患名→正規エージェントキー解決。**部分文字列衝突を厳密に処理**:
  - 亜鉛(zinc)は鉛(lead)を含む → zinc を先に判定
  - 硝酸塩は塩(salt)を含む → nitrate を先に判定
  - 混合重金属(鉛・亜鉛)は単一金属より heavy_metal_generic 優先
  - サケ中毒症(=感染症)・中毒性表皮壊死症(=薬疹)・塩素/クロラミン(別機序)は None で除外（誤適用防止）

### 撲滅スクリプト（`scripts/template_elimination/eliminate_toxicology_templates.py` 新規）
- `diseases_all_species.json` を走査し、(a)汎用毒物テンプレートを持ち (b)キュレートエージェントに解決する エントリのみ書換（キュレート済み内容は温存）
- 種別プレフィックス「<種>における<疾患>は、<機序>」を付与、JA/EN両対応
- 冪等（書換後はテンプレートマーカーに非マッチ）。`--apply` で適用、ソースの compact JSON 形式を維持
- 適用: pathophysiology_ja 209件 + causes_ja 230件 + 英語 patho 234件 + causes 217件（246疾患・64エージェント）

### 効果（配信SQLite実測、7,094疾患）
| フィールド | Before | After |
|---|---|---|
| pathophysiology_ja 汎用毒物テンプレート | 212 | **3** |
| causes_ja 汎用毒物テンプレート | 279 | **16** |
- 残存はサケ中毒症(感染症)・中毒性表皮壊死症(薬疹)・全身性中毒/毒素吸収疾患(汎用)・抗生物質毒性/油汚染/フッ素症(ニッチ)等、設計通り除外/温存したもの

### 回帰テスト追加（tests/test_no_template_disease_content.py、+6件）
- `test_critical_toxins_have_agent_specific_pathophysiology` — 主要毒物が真の機序キーワードを持つ（チョコ→メチルキサンチン、キシリトール→インスリン、鉛→ヘム等）
- `test_no_generic_toxin_template_on_curated_agents_in_json` — キュレートエージェントに汎用テンプレートが残っていない
- `test_toxin_resolver_does_not_confuse_zinc_and_lead` — 亜鉛/鉛・硝酸塩/塩の部分文字列衝突回帰防止
- `test_toxin_resolver_ignores_non_chemical_toxicoses` — サケ中毒症(感染症)を None 解決
- `test_lily_toxicosis_is_species_accurate` — 犬ユリ中毒が「猫特異的腎毒性」と誤記されない

### テスト・CI
- フルテストスイート: **3,419件合格**（34 skip）
- ruff check / format: 全変更ファイルで通過
- 再現手順: `eliminate_toxicology_templates.py --apply` → `migrate_to_sqlite.py`

## 2026-06セッション（第7弾: 臨床的に危険なカテゴリ誤適用の撲滅 — 治療・病因の取り違え修正）

### 背景: JSONオーバーレイ（配信本体）に残る危険な誤カテゴリ
低メモリ本番（512MB）では migrate がスキップされ SQLite が空のまま、各種ページは
`helpers.enrich_diseases()` が `diseases_all_species.json` をモジュールへ**実行時オーバーレイ**して配信する。
従って migrate の served-DB パスだけに置いた修正はユーザーに届かない。本セッションでは
JSONオーバーレイ自体を修正し、served-DB パスは安全網として併設した。

### 治療フィールド（treatment_ja）の危険な誤適用 15件を修正
あるカテゴリの治療テンプレートが別カテゴリの疾患に適用され、公開時に有害となる記述を是正：
- **毒物除染テンプレート（催吐・胃洗浄・活性炭）が非中毒疾患に**: 盲腸内細菌叢異常（草食小動物4種）、
  溶血性貧血（ウサギ）、抗生物質関連腸内細菌叢異常、急性盲腸鼓腸、腺胃/前胃潰瘍（鳥2種）、
  筋胃異物（鳥）、ヤドカリ入手後症候群
- **駆虫薬テンプレートが非寄生虫疾患に**: 猫虚血性脳症（脳梗塞）、直腸脱（猫）、
  薄筋・半腱様筋ミオパチー（犬）、新生児粘着眼（ハムスター）
- いずれも `scripts/template_elimination/curated_dangerous_treatments.py` に獣医学的に正確で
  種特異的なプロトコルを記述（Carpenter Formulary 6th, Quesenberry & Carpenter 4th 等）
- EN治療フィールドは元々正確だったため、本修正でJA=ENの品質に到達

### 病因/病態生理（causes_ja / pathophysiology_ja）の誤カテゴリ 182件を再分類
`resolve_category_from_name`（NAME_CATEGORY_PATTERNS）のバグを修正し、名前から正しいカテゴリを解決：
- **くる病/Rickets**: musculoskeletal → **nutritional**（ビタミンD/Ca/P欠乏症）
- **蹄叉腐爛/Thrush・蹄膿瘍・蹄底膿瘍・蹄腐敗・蹄冠瘻**: musculoskeletal → **bacterial_infection**
  （細菌性蹄感染。「骨折・脱臼・股関節形成不全」という誤病因を撲滅）
- **動脈硬化症・大動脈疾患・心疾患**: musculoskeletal/None → **cardiac**（約40件、血管疾患）
- **腎疾患**: None → **renal_urinary**、**副腎過形成**: renal → **endocrine_metabolic**（"ad-renal"部分一致バグ）
- **ふらつき症候群（WHS）**: musculoskeletal → **neurological**（神経変性疾患）
- **動脈瘤(?!様)** で「骨嚢腫（動脈瘤様）」が cardiac に誤分類されるのを防止
- 偽陽性に注意（Bone Spavin/Kissing Spines/Collateral Ligament 等は正しく musculoskeletal を維持）

### 実装（JSON本体 + served-DB安全網）
- `scripts/template_elimination/fix_category_miscategorization.py`（新規）— JSONオーバーレイに
  治療キュレーション＋病因再分類を冪等適用（compact JSON形式を保持）
- `scripts/migrate_to_sqlite.py` に `apply_curated_dangerous_treatments()` を追加（served-DB安全網、
  ソースを問わず危険テンプレートを補正）
- JSON修正後は served-DB パスの再分類対象が 233 → 50（モジュール専用エントリのみ）に減少

### 回帰テスト追加（tests/test_no_template_disease_content.py、+5件）
- `test_resolve_category_landmark_miscategorisations_fixed` — 動脈硬化症/くる病/蹄叉腐爛/腎疾患/WHS等の解決
- `test_resolve_category_genuine_musculoskeletal_unaffected` — 骨折/十字靭帯/舟状骨等のMSK維持
- `test_curated_dangerous_treatment_replaces_mismatch` — キュレーターの動作（非該当はNone）
- `test_served_db_no_toxin_decontamination_on_non_toxicoses` — 配信DBの除染テンプレート不在
- `test_served_db_thrush_etiology_is_not_musculoskeletal` — 蹄叉腐爛の骨折病因不在

### テスト・CI
- フルテストスイート: **3,424件合格**（34 skip、+5回帰テスト）
- ruff check / format: 全変更ファイルで通過
- 再現手順: `fix_category_miscategorization.py --apply` → `migrate_to_sqlite.py` → `build_disease_search_index.py`（名前不変のためno-op）

### 蹄葉炎・肝線維症のキュレート病因（単一カテゴリに収まらない疾患）
カテゴリ再分類では「誤テンプレを別の誤テンプレに置換」するだけになる多因子疾患を、
教科書準拠の疾患固有の病因・病態生理に置換（`scripts/template_elimination/curated_etiology.py`、新規）。
- **蹄葉炎/Laminitis（馬3件）**: 病因を内分泌性（EMS/PPID高インスリン血症 — 現在の最多原因）・
  敗血症/炎症性（SIRS）・過重負重性に正確化。「骨折・脱臼・股関節形成不全」という誤病因を撲滅。
  病態生理は葉層機能不全→蹄骨回転・沈下の機序（MMP活性化・微小循環障害）を記述。
  既存の良質な病態生理（基本の蹄葉炎エントリ）は**上書きせず温存**（置換は空/テンプレ/スタブのみ）。
- **肝線維症/Hepatic Fibrosis（全8種）**: 慢性肝傷害→肝星細胞活性化→コラーゲン沈着→門脈圧亢進/肝不全の
  病態生理と、胆汁うっ滞・栄養性・毒性（カビ毒/重金属）・感染・鉄過剰・慢性うっ血の病因を種名込みで記述。
- 実装: `fix_category_miscategorization.py` に curated etiology パスを追加（JSON本体、置換可能フィールドのみ）。
  `migrate_to_sqlite.py` に `apply_curated_etiology()` を served-DB安全網として追加。
- 回帰テスト +3件（curated_etiology のユニット + 配信DBで蹄葉炎/肝線維症が骨折病因を持たないこと）。
- フルテストスイート: **3,427件合格**（34 skip）、ruff clean。

### 行動・電解質・不整脈・泌尿器疾患の残存誤カテゴリを撲滅（120件）
resolver が None を返すため recat パスが補正できなかった「臓器系テンプレートの誤適用」を、
NAME_CATEGORY_PATTERNS への精密トークン追加で解決（causes_ja 107 + pathophysiology_ja 84 再分類）:
- **行動障害（55件）→ behavioral**: 羽毛破壊行動・常同行動・毛引き/毛噛み・過剰グルーミング・
  ケージ噛み・自己塗布・マーキング/尿スプレー・共食い/子拒絶・過活動症(ADHD)・異食症・心因性多飲・
  各種ストレス症候群等。心筋症/ネフロン損傷という誤病因を撲滅
- **電解質異常（21件）→ endocrine_metabolic**: 高リン血症・高/低カリウム血症・高/低ナトリウム血症・
  高/低マグネシウム血症（`血症` 必須で HYPP は neurological を維持）
- **不整脈・血管（10件）→ cardiac**: 房室ブロック・洞不全症候群・心嚢水貯留・全身性/動脈性高血圧
- **泌尿器（34件）→ renal_urinary**: 腎炎・間質性腎炎・尿管/尿道閉塞・異所性尿管・腎石灰化・腎アミロイドーシス
- **偽陽性回避を検証**: 既存の精密トークン方針（不安症≠不安、攻撃行動≠攻撃）に倣い、
  環軸椎不安定症（不安定）・ケージ麻痺（VE/Se欠乏）・捕食者攻撃損傷・HYPP は誤って behavioral/metabolic 化しないことを確認
- 全種 before/after 比較で category→category の変化 0 件（純粋に None→正カテゴリの 120件のみ）
- 回帰テスト +4件、フルスイート 3,431件合格

### 産卵・神経筋・鼻涙管疾患の残存誤カテゴリを撲滅（113件）
resolver が None を返すため recat が補正できなかった残りの臓器系テンプレート誤適用を、精密トークンで解決
（causes_ja 65 + pathophysiology_ja 48 再分類）:
- **産卵・卵管疾患（65件）→ reproductive**: 卵詰まり（egg binding）・卵胞停滞/卵停滞（follicular/egg stasis）・
  卵管炎/卵管脱/卵管閉塞（salpingitis/oviduct）・卵巣嚢胞（ovarian cyst）・卵黄性腹膜炎（yolk coelomitis）・
  慢性産卵症候群（chronic egg laying）等。鳥・爬虫類の頻発する生殖器救急が呼吸器/内分泌/細菌テンプレートだった
- **神経筋（1件）→ neurological**: 筋無力症クリーゼ（重症筋無力症だけでなく筋無力症を捕捉）
- **鼻涙管（3件）→ ophthalmic**: 鼻涙管/涙管/涙小管閉塞
- **偽陽性回避**: 卵巣腺癌/奇形腫/顆粒膜細胞腫は neoplasia 維持（`卵巣嚢胞` 等の精密語のみ使用、bare `卵巣` 不使用）。
  カルシウム欠乏症繁殖型（産卵鳥）は nutritional 維持（bare `産卵` を除外し `産卵鳥` 記述子の誤マッチを回避）
- before/after 全種比較で category→category の変化 0 件（69件すべて None→正カテゴリ）
- 回帰テスト +4件、フルスイート 3,435件合格

### 歯科・行動の残存誤カテゴリを撲滅（24件）
- **歯科（流涎・頬棘）→ dental**: 流涎/スロバーズ（齧歯類・ウサギの流涎は歯科徴候）、頬棘状突起潰瘍（buccal spur）。
  `頬棘` のみ追加（`臼歯棘` は `臼歯`→`歯` で既に dental、bare `棘` は使わず 棘下筋/棘突起＝筋・脊椎を誤判定しない）
- **行動 → behavioral**: 行動障害（心血管系/内分泌系/腎 等の合成名含む）、拒食（行動性）、ストレス関連疾患（全種）
- 流涎症（重度・皮膚炎合併）は derm→dental（流涎の原因は歯科で、皮膚炎は二次性のため改善）
- 回帰テスト +1件、フルスイート 全合格

### 主要犬猫疾患のキュレート病因・病態生理（カテゴリテンプレートの疾患固有化・第1弾）
名前解決で「正しいカテゴリ」にはなったが同カテゴリ内で汎用文だった causes_ja/pathophysiology_ja を、
最頻出・最重要の犬猫疾患について教科書準拠（Ettinger 8th, Nelson & Couto 6th, ACVIM consensus）の
疾患固有テキストに置換（`curated_etiology.py` に16疾患を追加、配信DB実測で計49フィールド置換）:
- **犬（11疾患）**: GDV・膵炎・甲状腺機能低下症・クッシング症候群・慢性腎臓病・アトピー性皮膚炎・
  変形性関節症・椎間板ヘルニア(IVDD)・特発性てんかん・拡張型心筋症(DCM)・粘液腫様僧帽弁変性症(MMVD)
- **猫（5疾患）**: 肥大型心筋症(HCM)・膵炎・炎症性腸疾患(IBD)・喘息・慢性腎臓病・慢性歯肉口内炎(FCGS)
- 品種バリアント（CKCS早期発症僧帽弁疾患、ドーベルマン潜在性DCM等）も親疾患のキュレート文を継承
- **偽陽性回避（exclusion対応）**: 副甲状腺（≠甲状腺）、僧帽弁形成不全＝先天性（≠MMVD変性）、
  猫口内炎非リンパ形質細胞性（≠FCGS）、膵外分泌不全（≠膵炎）はキュレート対象外
- **既存の良質な内容は温存**: 置換は空/テンプレ/スタブのフィールドのみ（例: GDVの既存の疾患固有
  病態生理は保持され、テンプレートだった causes_ja のみ置換）
- 回帰テスト +3件、フルスイート全合格

### 主要犬猫疾患のキュレート病因・病態生理（第2弾）
さらに20疾患を `curated_etiology.py` に追加（配信DB実測で計93フィールド置換、品種・解剖型バリアント含む）:
- **犬（12疾患）**: 糖尿病・緑内障・乾性角結膜炎(KCS)・子宮蓄膿症・免疫介在性溶血性貧血(IMHA)・
  レプトスピラ症・ケンネルコフ(CIRDC)・良性前立腺肥大症(BPH)・骨肉腫(OSA)・肥満細胞腫(MCT)・
  血管肉腫(HSA)・リンパ腫
- **猫（8疾患）**: 糖尿病・リンパ腫・肝リピドーシス・胆管炎(triaditis)・特発性膀胱炎(FIC)・
  上部呼吸器感染症(URI)・カリシウイルス・ヘルペスウイルス感染症
- 緑内障/KCSは犬猫両対応（species_ja を文中に織り込み）。リンパ腫・血管肉腫・胆管炎は解剖型バリアントにも適用
- **偽陽性回避（exclusion）**: 糖尿病性ケトアシドーシス（≠糖尿病）、軟骨肉腫（≠骨肉腫、部分一致回避）、
  ヘルペス性角膜炎/皮膚炎（≠URI型）、前立腺膿瘍（≠BPH）はキュレート対象外
- 回帰テスト +2件、フルスイート全合格
- 注: causes_ja/pathophysiology_ja は cross-disease テンプレート検出の対象外フィールドのため、
  同一疾患の解剖型バリアント間でのキュレート文共有は許容（医学的に妥当）

### 主要犬猫疾患のキュレート病因・病態生理（第3弾）
内分泌・神経・消化器・泌尿器の主要疾患をさらに23疾患追加（配信DB実測で計49フィールド置換）:
- **犬（9疾患）**: アジソン病・副甲状腺機能低下症・膵外分泌不全(EPI)・気管虚脱・喉頭麻痺(GOLPP)・
  変性性脊髄症(DM/SOD1)・蛋白漏出性腸症(PLE)・胆嚢粘液嚢腫・肛門嚢疾患
- **猫（14疾患）**: 尿道閉塞(blocked cat)・巨大結腸症/便秘・多発性嚢胞腎(PKD)・三叉神経炎・
  タウリン欠乏性/拡張型心筋症・拘束型心筋症(RCM)・シュウ酸Ca/ストルバイト尿路結石症・トキソプラズマ症・
  副甲状腺機能亢進症3型（栄養性二次性/原発性/腎性二次性を**個別に**正確化）
- FeLV/FIP/FIVは既にキュレート済みのため対象外（テンプレートでないことを確認）
- **偽陽性回避**: 肛門嚢腺癌（≠肛門嚢疾患）はキュレート対象外。副甲状腺亢進3型は接頭辞で厳密に分離
- **3弾累計: 59疾患・配信DBで約190フィールドを汎用カテゴリ文→疾患固有テキストに置換**

### 主要犬猫疾患のキュレート病因・病態生理（第4弾: 眼科・整形・皮膚・肝・血液）
さらに25疾患を追加（配信DB実測で計81フィールド置換、変異・両種対応含む）:
- **犬（13疾患）**: 股関節/肘関節形成不全・膝蓋骨脱臼・前十字靭帯断裂・白内障・進行性網膜萎縮(PRA)・
  チェリーアイ・膿皮症・巨大食道症・門脈体循環シャント(PSS)・慢性肝炎(銅関連)・会陰ヘルニア・停留精巣
- **猫（8疾患）**: 結膜炎・ぶどう膜炎・角膜分離症・好酸球性角結膜炎・ヘモプラズマ症・免疫介在性血小板減少症・心筋炎
- **両種（2疾患）**: 角膜潰瘍・尿崩症（species_ja を文中に織り込み、中枢性/腎性等の変異対応）
- **カテゴリ誤り是正**: 猫伝染性貧血/ヘモプラズマ症は viral/fungal テンプレートだったが、
  実際は細菌（ヘモトロピック・マイコプラズマ）であるため病因を細菌性に正確化
- **偽陽性回避**: 心筋挫傷（≠心筋炎）、癒着性/好酸球性角結膜炎（≠一般結膜炎）は分離
- 回帰テスト +2件
- **4弾累計: 84疾患・配信DBで約270フィールドを汎用カテゴリ文→疾患固有テキストに置換**

### main の並行キュレート作業（PR #683 / mg3pzq）との統合
別セッション（branch mg3pzq）が `curated_common_diseases.py`（29疾患）を追加して main にマージされ、
本ブランチの batch 1-4 と重複・衝突した。マージで解決:
- `curated_etiology()` が `COMMON_DISEASES`（mg3pzq、優先）→ 本モジュールの `_CURATED`（4-tuple）の順で参照
- 重複疾患は mg3pzq の文言が優先、本ブランチ固有疾患は本モジュールが適用（どちらも非テンプレなので二重置換なし）
- JSON は main 版を基に本パイプラインを再適用（重複は非テンプレのためスキップ＝mg3pzq維持、固有のみ適用）
- 副甲状腺機能低下症/EPIは本ブランチが独立キュレートしたため mg3pzq テストの除外アサーションを更新。
  先天性甲状腺機能低下症（クレチン症）は別病態のため甲状腺機能低下キュレートから除外
- バッチテストは重複疾患で文言が変わるため「キュレート済み＋実質的内容」検証に変更（文言非依存）

### 主要疾患のキュレート病因・病態生理（第5弾: 馬）
馬の主要疾患21件を追加（配信DB実測で計66フィールド置換）。開発者が馬獣医師のため特に重視:
- **疝痛（コリック）・胃潰瘍(EGUS)・馬喘息(IAD/RAO)・大腸炎・食道閉塞(チョーク)・喉嚢疾患**（消化器/呼吸器）
- **PPID（下垂体中葉機能障害）・EMS（馬代謝症候群）**（内分泌）— **PPIDは細菌感染テンプレートだった誤分類を是正**
- **浅指屈腱炎(SDFT)・蹄舟骨症候群・OCD・PSSM/横紋筋融解症**（運動器）
- **馬再発性ぶどう膜炎(ERU/月盲)・EPM・腺疫・EHV・ピロプラズマ症**（眼科/神経/感染症）
- **子宮内膜炎・胎盤炎**（繁殖）
- 回帰テスト +2件（PPIDが細菌でないことを含む）
- **5弾累計: 105疾患・配信DBで約340フィールドを汎用カテゴリ文→疾患固有テキストに置換**

### 主要疾患のキュレート病因・病態生理（第6弾: エキゾチック）
エキゾチック伴侶動物の主要疾患を追加（配信DB実測で計148フィールド置換）:
- **草食小型哺乳類共通（species_ja織込）**: 消化管うっ滞(GI stasis)・不正咬合(常生歯)・毛球症
  （ウサギ/チンチラ/モルモット/デグー）
- **ウサギ**: パスツレラ症(スナッフル)・E.cuniculi・斜頸・子宮腺癌・ソアホック
- **フェレット**: インスリノーマ・副腎疾患・リンパ腫・アリューシャン病・ECE・心筋症
- **チンチラ**: 熱中症・陰茎毛輪　**モルモット**: 壊血病(ビタミンC欠乏)・卵巣嚢胞
- **カテゴリ誤り是正**: アリューシャン病=パルボウイルス(細菌テンプレート誤り)、チンチラ熱中症=
  栄養テンプレート誤り、毛球症=寄生虫テンプレート誤り(実際はGI stasisの一徴候)
- 回帰テスト +2件
- **6弾累計: 約127疾患・配信DBで約490フィールドを汎用カテゴリ文→疾患固有テキストに置換**

### レビューで発見・修正した不具合
- **PRA→PRAA 部分文字列衝突**: bare `PRA` が右大動脈弓遺残(PRAA)に誤マッチ→網膜萎縮テキスト適用。
  bare `PRA`削除＋PRAAキュレート追加で修正（PR #685、main マージ済み）。
  全頭字語トークン(EMS/EPM/ERU/OCD/PPID/PRA/PSSM/haemo)の衝突監査済み

### 残課題（次セッション候補）
- 主要疾患キュレート第7弾（鳥/爬虫類の主要疾患、犬猫の残り）
- causes_ja/pathophysiology_ja の残りカテゴリテンプレートの疾患固有化（獣医レビュー前提で漸進的に）

## 2026-06セッション（第8弾: 原虫症の「駆虫薬」テンプレート撲滅 — 臨床的に危険な治療誤りの是正）

### 背景: 原虫に駆虫薬を処方する致命的なテンプレート
配信DB監査で、40件の**原虫症**（バベシア症・トキソプラズマ症・リーシュマニア症・ヘパトゾーン症・
サイトークスゾーン症・エンセファリトゾーン症・コクシジウム症・サルコシスティス症・アトキソプラズマ症・
ロイコチトゾーン症・鳥マラリア）が、蠕虫用の汎用「駆虫薬」治療テンプレート
（「…同定された寄生虫に応じた適切な駆虫薬が必要…全てのライフステージを排除するため複数回投与…」）を
保持していた。これは単なるテンプレートではなく**臨床的に誤り**: 駆虫薬（anthelmintic）は赤血球内・組織内・
細胞内の原虫を治療しない。獣医師が「バベシア症やサイトークスゾーン症に駆虫薬」と読めば信頼を失う致命的な誤記。

### キュレート抗原虫薬ライブラリ（`scripts/template_elimination/antiprotozoal_library.py` 新規）
- 11の原虫エージェント別にエビデンスベース（Solano-Gallego/ESCCAP・LeishVet・ACVIM・Baneth・
  Cohn & Birkenheuer・Künzel & Fisher・Carpenter Formulary 6th・Greene 4th）の**種特異的**治療＋
  病態生理を JA/EN で記述:
  - バベシア: 大型(イミドカルブ6.6 mg/kg IM×2)/小型B. gibsoni(アトバコン＋アジスロマイシン)/猫(プリマキン)
  - トキソプラズマ: クリンダマイシン10-12.5 mg/kg PO q12h×4週（鳥はサルファ＋ピリメタミン＋支持療法）
  - リーシュマニア: メグルミンアンチモン酸/ミルテホシン＋アロプリノール長期、腎症モニタリング必須
  - ヘパトゾーン: H. canis(イミドカルブ)/American型H. americanum(TCP→デコキネート長期)
  - サイトークスゾーン: アトバコン15 mg/kg q8h＋アジスロマイシン10日（最高生存率）＋集中支持療法
  - エンセファリトゾーン(E. cuniculi): フェンベンダゾール20 mg/kg PO q24h×28日（微胞子虫＝ベンズイミダゾール正解）
  - コクシジウム: サルファジメトキシン/ポナズリル/トルトラズリル（ウサギ肝コクシE. stiedae注記）
  - サルコシスティス/アトキソプラズマ/ロイコチトゾーン/鳥マラリア: 各々の標準治療＋媒介昆虫防除
- `resolve_protozoal_agent()` で疾患名→原虫エージェント解決。**蠕虫・外部寄生虫（回虫・条虫・ノミ・
  ダニ・糞線虫）は None を返し駆虫薬テンプレートを維持**（正しいため）
- `protozoal_clinical_fields()` は駆虫薬フィンガープリント＋原虫解決の両方を満たす場合のみ返却

### 適用（JSON本体 + 配信DB安全網）
- `scripts/template_elimination/fix_antiprotozoal.py --apply`（新規）— JSONオーバーレイに適用（39件）
  - treatment_ja/treatment(EN): 駆虫薬テンプレート＋原虫解決で**常に**置換（臨床的に危険なため）
  - pathophysiology_ja/(EN): 空/カテゴリテンプレート/スタブの場合のみ置換。**病原体名を明記した
    キュレート病態生理（Babesia属・Toxoplasma gondii・Cytauxzoon felis・Encephalitozoon cuniculi）は温存**
- `migrate_to_sqlite.py` に `regenerate_protozoal_treatments()` を追加（配信DB安全網、モジュール由来1件を捕捉）
- 配信DB（7,094疾患）: 原虫症の駆虫薬テンプレート **40→0件**

### 回帰テスト追加（tests/test_no_template_disease_content.py、+5件）
- `test_protozoal_resolver_maps_agents_and_ignores_helminths` — 原虫は解決、蠕虫/外部寄生虫はNone
- `test_protozoal_curated_treatments_name_the_correct_drug` — 各原虫が正しい抗原虫薬を含み「駆虫薬」を含まない
- `test_no_deworming_template_on_protozoal_diseases_in_json` — JSONに原虫×駆虫薬テンプレートが残っていない
- `test_served_db_protozoal_diseases_are_not_dewormed` — 配信DBに原虫×駆虫薬テンプレートが残っていない

### テスト・CI
- フルテストスイート: **3,455件合格**（34 skip）
- ruff check / format: 全変更ファイルで通過
- 再現手順: `fix_antiprotozoal.py --apply` → `migrate_to_sqlite.py`

## 2026-07セッション（英語フィールドの構造的テンプレート撲滅 + 予後の二重所有格バグ修正 + i18n整合）

### 背景: 英語版サイトが構造的テンプレートに埋もれていた
これまでのテンプレート撲滅は日本語フィールド（主対象＝日本の獣医師）に集中しており、**英語フィールドは grounding パスの対象外**だった。名前を正規化して除去する監査（identical-modulo-name、5+疾患名で共有）を英語版に対して初めて実施した結果、英語版は公開レベルに達していないことが判明:
| フィールド | JA (before) | EN (before) |
|---|---|---|
| prevention | 13% | **89%** |
| prognosis | 17% | **88%** |
| pathophysiology | **61%** | **88%** |
| causes | 81% | 93% |
- 英語圏の閲覧者が疾患を数件開くと、prevention/prognosis/pathophysiology が category 単位でバイト単位一致の同一段落だった（英語 causes は 604 distinct / 7,094 疾患＝疾患名すら差し込まれていない生テンプレート）。
- 監査バグも修正: 従来の内部監査は JA フィールドの正規化に英語疾患名を使っていたため、JA のテンプレート率を実際より低く見積もっていた（causes_ja は 2% ではなく実測 81%）。正しくは JA フィールドは name_ja、EN フィールドは name で正規化する。

### grounding パスの英語対応 + 病態生理への拡張（捏造ゼロ）
実証済みの JA grounding（疾患自身の確定データ＝症状のみを言い換え、新規の医学的主張をしない）を英語へ横展開し、さらに病態生理フィールドにも適用:
- `clinical_fields_generator.py` に英語版 composer を追加:
  - `compose_grounded_prevention` / `compose_grounded_prognosis`（英語）— category ベースに疾患自身の徴候を早期発見・経過観察標的として付加
  - `compose_grounded_pathophysiology_ja` / `compose_grounded_pathophysiology`（日英）— 病態生理は定義上「機序→臨床発現」の連鎖なので、その疾患自身の記録済み徴候を発現として付記するのは医学的に自然かつ捏造ゼロ
  - **causes（病因）は徴候 grounding の対象外**: 臨床徴候は病因ではないため。病因は named-agent キュレーション（toxicology/antiprotozoal/curated_etiology バッチ）に委ねる方針を維持
- `migrate_to_sqlite.py` の `ground_templated_fields_with_signs` を **バイリンガル化**（JA フィールドは JA 徴候、EN フィールドは EN 徴候で解決）+ pathophysiology_ja / pathophysiology を追加
- 徴候が2個未満で有意なリストを作れない場合は base のまま（捏造しない設計の下限）

### 効果（配信SQLite実測、7,094疾患）
| フィールド | before | after |
|---|---|---|
| prevention (EN) | 89% | **13%** |
| prognosis (EN) | 88% | **19%** |
| pathophysiology (EN) | 88% | **11%** |
| pathophysiology (JA) | 61% | **15%** |
- キュレート済みフラグシップ疾患（猫喘息・PBFD 等）は grounding が上書きせず温存されることを確認

### 英語予後の二重所有格バグ修正（5,665件）
`gen_prognosis_en` が主語 `"<disease> in <species>s"` に `"'s prognosis ..."` で始まる clause を連結していたため、`"Acute Enteritis in rabbits's prognosis varies ..."` という非文法的・機械翻訳的な英語を **5,665件** 生成していた。
- `_combine_prognosis_en()` を追加し `"The prognosis of <disease> in <species> ..."` 形式に修正（generator + fallback 両方）
- `diseases_all_species.json` の既存 5,665件を一括修正（compact JSON 形式維持）
- `migrate_to_sqlite.py` に `fix_prognosis_possessive_en()` を配信DB安全網として追加（module/supplementary 由来を捕捉）
- 配信DB実測: `s's prognosis` **0件**

### i18n 整合（英語UXの日本語混入除去）
- `renderDiseaseDb()` の enrichment ラベル（リハビリ/栄養管理/回復期間/成功率/死亡率）が `"リハビリテーション/Rehabilitation"` のように **言語問わず日英併記** され、他の全ラベル（`t()` / `currentLang` 準拠）と不整合だった → `currentLang` 準拠に統一（英語ユーザーに日本語が混じらない）
- 回復期間の値 `"N週間 / N weeks"` も言語別表示に修正

### 回帰テスト追加（tests/test_no_template_disease_content.py、+5件）
- `test_grounded_en_prevention_prognosis_differentiate_by_signs` — 英語 composer が徴候で分化＋徴候不足時は無改変＋冪等
- `test_grounded_en_pathophysiology_manifestation_clause` — 日英 pathophysiology composer の分化＋冪等
- `test_gen_prognosis_en_has_no_double_possessive` — generator が `s's prognosis` を生成しない
- `test_served_db_no_double_possessive_prognosis` — 配信DBに二重所有格が残っていない
- `test_served_db_en_prognosis_prevention_pathophysiology_grounded` — 英語3フィールドのテンプレート率 <40%（回帰ガード）

### テスト・CI
- フルテストスイート: **3,466件合格**（34 skip、+5回帰テスト）
- ruff check / format: 全変更ファイルで通過
- ServiceWorker: `CACHE_NAME` v82 → **v83**
- 再現手順: JSON修正は適用済み → `migrate_to_sqlite.py`（grounding/possessive-fix は配信DBビルドに統合済み）

### 残課題（次セッション候補）
- causes（病因）: JA 81% / EN 93% が構造的カテゴリテンプレート。徴候 grounding 不可（徴候≠病因）のため named-agent キュレーションの継続が必要（毒物64・原虫11・curated_etiology 100+ 済み。ウイルス/細菌の named-pathogen 疾患の拡充が最大の残メイン）
- 英語 causes/pathophysiology のフラグシップ・キュレーション: 現状キュレート済み病因は JA のみ（curated_etiology は JA 専用）。最頻閲覧疾患の英語 causes/patho をバイリンガル化するには curated_etiology の EN 対応が望ましい（textbook 事実ベース、獣医レビュー前提）
- treatment（EN 35%）: 腫瘍学・中毒等の医学的に妥当な汎用カテゴリガイダンスが中心。危険な誤カテゴリは既に是正済み

## 2026-07セッション（第2弾: named-agent キュレーション継続 — ウイルス病因の疾患特異化）

### 背景
causes（病因）フィールドは徴候 grounding が不可能（臨床徴候≠病因）なため、named-agent キュレーションでのみ撲滅できる。カテゴリ生成器は全ウイルス疾患に同一の汎用病因を付与していた（JA「…の原因はウイルス感染である。特異的ウイルス病原体が…」245件、EN "Viral infection. Transmission via…" 200件超）。疾患名が病原体を示す疾患（犬パルボ・猫ヘルペス・狂犬病等）では、病因は名称から導ける教科書的事実なので捏造リスクゼロで疾患特異化できる。

### `scripts/template_elimination/pathogen_library.py`（新規）
- 13のウイルス病原体ファミリー生成器（herpes/parvo/distemper/calici/corona/influenza/adeno/papilloma/pox/rabies/rota/FeLV/FIV）が causes・pathophysiology を **JA+EN** で返却。
- **宿主適応型ウイルスは種別に正しい株名**を記載: 猫→FHV-1/FPV/FCV/FCoV、犬→CHV-1/CPV-2/CDV/CAV、馬→EHV-1/4、鳥→アビポックス/サイタシドヘルペス、ウサギ→RHDV。
- 誤マッチ防止（レビューで発見・修正）:
  - `adeno`（bare）→ `adenovirus`（腺腫/腺癌 adenoma/adenocarcinoma を誤検出しない）
  - `カリシ`→`カリシウイルス`（「カリシン過敏症」＝Culicoides を誤検出しない）
  - `corona`→`coronavirus`、`pox`(bare)→`痘`/`poxvirus`/named pox（hypoxia 等を回避）
  - `immunodeficiency`→`immunodeficiency virus`（複合免疫不全症を回避）
  - 否定名（`非ヘルペス性`/`Non-Herpetic`）は `_neutralise_negations` で除外
  - FeLV/FIV は cat 限定（サル免疫不全ウイルス等の非猫レンチウイルスに猫用文を付与しない）

### 適用（JSON本体 + 配信DB安全網）
- `scripts/template_elimination/fix_named_pathogens.py`（新規, `--apply`）: JSONオーバーレイに適用。カテゴリテンプレート/スタブのフィールドのみ置換（キュレート済み prose は温存 — フラグシップの curated JA を残しつつ、templated だった **EN** のみアップグレード）。適用実績: 152疾患（causes 135 JA/133 EN, pathophysiology 72 JA/130 EN）。
- `migrate_to_sqlite.py` に `regenerate_named_pathogen_etiology()` を追加（配信DB安全網, モジュール由来 causes 65 JA / patho 61 JA を捕捉）。

### 効果（配信SQLite実測）
- 汎用ウイルス病因: **EN 201→98件 / JA 245→129件**（約50%削減）
- ウイルス名を持つ疾患のうち causes が具体的病原体を明記: 95/248
- 猫汎白血球減少症の病因は **FPV**（CPV-2 ではない）、CHV-1、avipoxvirus 等を正しく記載
- 注: modulo-name テンプレート率（causes_ja 81→80%）はほぼ不変。papillomavirus が14種で共有される等、病原体ファミリーの共有は**医学的に正当**（テンプレートではない）ため。本バッチの価値は率ではなく**病因の正確性・疾患特異性**にある。

### 回帰テスト追加（+6件）
- `test_pathogen_library_resolver_precision` — 非ウイルス（腺腫/夏癬）・否定名・非猫レンチウイルスを除外
- `test_named_pathogen_causes_cite_correct_pathogen` — 汎白血球減少症=FPV(≠CPV-2)、FHV-1/CHV-1/EHV/lyssavirus を明記
- `test_no_generic_viral_causes_on_named_pathogens_in_json` / `test_served_db_named_pathogen_etiology_is_specific`

### テスト・CI
- フルテストスイート: **3,470件合格**（34 skip、+4新規）
- ruff check / format: 全変更ファイルで通過
- 再現手順: `fix_named_pathogens.py --apply` → `migrate_to_sqlite.py`

### 次バッチ候補
- 残る汎用ウイルス病因 EN 98 / JA 129（paramyxo/reo/circo/borna 非フラグシップ、fish/reptile の iridovirus・birnavirus 等）
- 細菌 named-pathogen（salmonella/E.coli/staph/strep/pseudomonas/clostridium/pasteurella/bordetella/leptospira/chlamydia — スキャンで ~120フィールド）

## 2026-07セッション（第3弾: named-agent キュレーション拡充 — 細菌 + 残ウイルス）

### 細菌 named-pathogen ライブラリ（`scripts/template_elimination/bacterial_library.py` 新規）
汎用細菌テンプレート（JA「…の原因は特定の細菌病原体の感染である…」/ EN "Bacterial infection. Transmission via…" / "Infectious diseases are caused by pathogenic organisms…"）を、疾患名が示す菌に基づき疾患特異化。
- **24の細菌属生成器**（causes + pathophysiology を JA+EN）: salmonella / E.coli / staph / strep / pseudomonas / clostridium / pasteurella / mycoplasma / chlamydia / bordetella / mycobacterium / leptospira / klebsiella / listeria / abscess / lawsonia / helicobacter / campylobacter / brucella / borrelia / actinomyces。
- **臨床的に重要な分岐**: クロストリジウム＝毒素別（C. tetani テタノスパスミン / C. botulinum ボツリヌス毒素 / C. perfringens 腸毒血症）、マイコプラズマ＝ヘモトロピック vs 呼吸器、クラミジア＝オウム病(鳥) vs C. felis(猫)、レンサ球菌＝馬腺疫 S. equi、マイコバクテリア＝結核/らい/非定型。
- **部分文字列衝突をレビューで発見・回避**: `coli`(bare)→大腸炎/疝痛を誤検出 → `大腸菌`/`escherichia`/`e. coli`/`colibacill`；`listeri`→「blistering(水疱症)」→ `listeria`/`listerio`；属名は全綴りで指定。
- **abscess 除外**: 二次性/非細菌一次性の膿瘍（ビタミンA欠乏性口腔膿瘍、Corynebacterium 鳩熱）は `_ABSCESS_EXCLUSIONS` で除外。

### 残ウイルスの拡充（`pathogen_library.py`）
汎用ウイルステンプレートに残っていた named-pathogen を追加（13→28生成器）:
- 追加: パラミクソ(Newcastle/PMV/Sendai) / イリドウイルス(Ranavirus/FV3/ATV) / サーコ / ポリオーマ / レオ / ボルナ(ABV) / アリューシャン病(amdoparvovirus) / アレナ(LCMV, 人獣共通) / フラビ(West Nile/日本脳炎) / EIA(馬伝染性貧血, 届出) / EVA(馬ウイルス性動脈炎) / ビルナ(ガンボロ) / ヘニパ(Hendra/Nipah) / ハンタ。
- 既存生成器へキー追加: Marek病/伝染性喉頭気管炎/サイトメガロ → herpes；伝染性気管支炎(IBV) → corona；ノロウイルス → calici。

### 検出ロジックの汎用化（`GENERIC_CAUSES_*_MARKS` / `GENERIC_PATHO_EN_MARKS`）
named-pathogen 疾患に付いた**任意のカテゴリテンプレート**を検出（例: West Nile 脳炎の EN causes が「Neurological etiology…」= 神経カテゴリ）。EN病態生理は全て "The pathophysiology of …" で始まるため1マーカーで捕捉。マーカーを `pathogen_library.py` に集約し JSON パス・配信DB安全網の両方で共有。

### 適用と効果（配信SQLite実測）
- `fix_named_pathogens.py` を viral+bacterial 両対応化（`_clinical_fields`/`_resolves`）。`migrate_to_sqlite.py` の `regenerate_named_pathogen_etiology` も両対応。
- **583疾患**（viral+bacterial）を疾患特異的病因・病態生理に置換。
- 汎用ウイルス causes: JA 245→63 / EN 201→25。EN pathophysiology の distinct 値: 896→**5730**（grounding と併せて大幅にユニーク化）。
- 残る汎用細菌テンプレート（375 JA）は「細菌性皮膚炎」等、**菌名を持たない汎用細菌疾患**で、named-agent 化の対象外（設計通り）。

### 回帰テスト（+8件）
- ウイルス: resolver 精度（腺腫/否定名/非猫レンチ除外）、正病原体名、汎用テンプレート不在
- 細菌: resolver 精度（coli/listeri 衝突・abscess 除外）、正病原体名（S. equi / C. tetani+tetanospasmin / botulinum / haemoplasma）、汎用テンプレート不在
- フルスイート **3,473件合格**（34 skip）、ruff clean

## 2026-07セッション（第4弾: named-agent キュレーション拡充 — 真菌）

### 真菌 named-pathogen ライブラリ（`scripts/template_elimination/fungal_library.py` 新規）
汎用真菌テンプレート（JA「…の原因は真菌感染である…」/ EN "Fungal infection. Inhalation or contact…" / "Fungal infections are caused by pathogenic or opportunistic fungi…"）を、疾患名が示す真菌に基づき疾患特異化。
- **14の真菌属生成器**（causes + pathophysiology を JA+EN、宿主特異的分岐あり）:
  - 皮膚糸状菌（犬猫→Microsporum canis / げっ歯類→Trichophyton）、アスペルギルス（鳥→気嚢型 / 犬→鼻腔型 / 馬→喉嚢真菌症）、カンジダ（鳥→そ嚢真菌症）、クリプトコッカス（猫→鼻腔・CNS）、マラセチア、ヒストプラズマ、ブラストミセス、コクシジオイデス（渓谷熱）、スポロトリックス（人獣共通）、接合菌（ムコール、血管侵襲）、ピシウム（卵菌）、サプロレグニア（水カビ、魚・両生類）、マクロラブダス（鳥胃酵母、旧メガバクテリア）、ニューモシスチス。
- **致命的な部分文字列衝突をレビューで回避**:
  - `coccidio`(bare)→原虫コクシジウム症 → `coccidioidomyc`/`coccidioides`
  - `microspor`→微胞子虫（Encephalitozoon）→ `microsporum`（全綴り）
  - `crypto`→クリプトスポリジウム(原虫) → `cryptococc`
  - `pythi`→python（ヘビ）は非衝突を確認（pythi≠pytho）
- キュレート済み JA（フラグシップのアスペルギルス・カンジダ）は fingerprint 検出で温存し、テンプレートだった英語のみアップグレード。

### 統合
- `fix_named_pathogens.py` の `_clinical_fields`/`_resolves` を viral→bacterial→fungal の3段に拡張。`migrate_to_sqlite.py` の配信DB安全網も同様。
- EN 第2真菌テンプレート "Fungal infections are caused by pathogenic or opportunistic fungi" を `GENERIC_CAUSES_EN_MARKS` に追加（"Fungal infection. Inhalation…" は既収載）。

### 効果（配信SQLite実測）
- **133真菌疾患**を疾患特異的病因・病態生理に置換。
- 残る汎用 "Fungal infection" EN（73件）は「全身性真菌症」等、菌名を持たない汎用真菌疾患で対象外（設計通り）。

### 回帰テスト（+3件）
- `test_fungal_library_resolver_precision` — コクシジウム症/微胞子虫/クリプトスポリジウム/python を除外
- `test_named_fungal_causes_cite_correct_organism` — Microsporum canis(犬猫)/Trichophyton(げっ歯類)、鳥アスペルギルス=気嚢、馬=喉嚢、Macrorhabdus 明記
- `test_no_generic_fungal_causes_on_named_fungi_in_json`

### テスト・CI
- フルスイート **3,476件合格**（34 skip、+3新規）、ruff clean
- 再現手順: `fix_named_pathogens.py --apply` → `migrate_to_sqlite.py`

### named-agent キュレーション累計（第2〜4弾）
毒物64 + 原虫11 + ウイルス28 + 細菌24 + 真菌14 = **141病原体生成器**。ウイルス+細菌+真菌で計 **約720疾患**の病因・病態生理を汎用テンプレートから疾患特異的記述（日英）に置換。

## 2026-07セッション（第5弾: named-agent キュレーション拡充 — 寄生虫）

### 寄生虫 named-parasite ライブラリ（`scripts/template_elimination/parasite_library.py` 新規）
汎用寄生虫テンプレート（JA「…の原因は寄生虫（蠕虫・原虫・節足動物）の感染である…」/ EN "Caused by parasites infecting affected tissues…" / "External parasite infestation…" / "Endoparasitic infection…" / "Parasitic diseases are caused by infection with…"）を、疾患名が示す寄生虫に基づき疾患特異化。
- **22の寄生虫生成器**（causes + pathophysiology を JA+EN）:
  - 線虫: 回虫/鉤虫/鞭虫/蟯虫/円虫(馬)/肺虫/毛細線虫/犬糸状虫(フィラリア, 猫は非好適宿主分岐)
  - 条虫/鉤頭虫、吸虫(肝蛭・肺吸虫・住血吸虫)
  - 腸管原虫: コクシジウム/ジアルジア/トリコモナス（causes/病態のみ。治療は antiprotozoal_library が担当）
  - 外部寄生虫: ダニ(疥癬/毛包虫/耳ダニ)/マダニ/ノミ/シラミ/ハエ幼虫症
  - 水生: 白点病/単生虫(ギロダクチルス・ダクチロギルス)/甲殻類(イカリムシ・ウオジラミ)
- **致命的な部分文字列衝突をレビューで発見・回避**:
  - `包虫`→「毛**包虫**症」(demodicosis, ダニ疾患) → `エキノコックス`/`hydatid`/`echinococc`
  - `ich`→itch/which → `ichthyophthirius`/`白点病`/`cryptocaryon`
  - `lice`→police/slice → `louse`/`pediculosis`/`シラミ`
  - `coccidia`≠`coccidioides`(真菌)、`tick`(マダニ寄生)≠tick-borne病原体疾患（ehrlichia/babesia/lyme は resolve せず）
- 検出マーカーを `GENERIC_CAUSES_*_MARKS` に集約（寄生虫EN 4変種 + JA 2変種を追加）。

### 統合
- `fix_named_pathogens.py` / `migrate_to_sqlite.py` を viral→bacterial→fungal→parasite の4段に拡張。

### 効果（配信SQLite実測）
- **281寄生虫疾患**を疾患特異的病因・病態生理に置換。
- EN causes の distinct 値: **604（全バッチ前）→ 1,004**（named-agent 全5系統で +66%）。
- 解決した寄生虫疾患で汎用テンプレートが残るものは **0件**。
- 残る汎用寄生虫テンプレート（EN ~90 / JA ~200）は「腸管寄生虫症」等、**寄生虫名を持たない汎用疾患**で対象外（設計通り）。

### 回帰テスト（+3件）
- `test_parasite_library_resolver_precision` — 毛包虫≠包虫、lice≠police、coccidia≠coccidioides、tick-borne病原体を除外
- `test_named_parasite_causes_cite_correct_parasite` — Dirofilaria/hookworm/Trichuris、猫フィラリア=非好適宿主、coccidia=原虫
- `test_no_generic_parasite_causes_on_named_parasites_in_json`

### テスト・CI
- フルスイート **3,479件合格**（34 skip、+3新規）、ruff clean

### named-agent キュレーション累計（第2〜5弾）
毒物64 + 原虫treatment11 + ウイルス28 + 細菌24 + 真菌14 + 寄生虫22 = **163病原体生成器**。感染症の全系統（ウイルス・細菌・真菌・寄生虫）の named-pathogen 化が完了し、計 **約1,000疾患**の病因・病態生理を汎用テンプレートから日英の疾患特異的記述に置換。

## 2026-07セッション（第6弾: named-agent キュレーション拡充 — 栄養性欠乏/過剰）

### 栄養性 named-nutrient ライブラリ（`scripts/template_elimination/nutritional_library.py` 新規）
感染症に続く最後の「名前が決定論的に原因を示す」病因クラス。汎用栄養テンプレート（JA「…栄養バランスの是正が中心…」/ EN "Caused by dietary deficiency or excess…" / "Nutritional imbalance…" / "Nutritional diseases result from…"）を、疾患名が示す栄養素に基づき疾患特異化。
- **12の栄養素生成器**（causes + pathophysiology を JA+EN、種特異的分岐あり）:
  - カルシウム/NSHP・代謝性骨疾患（爬虫類 UV-B 分岐）、ビタミンA、ビタミンD/くる病、ビタミンE/セレン（白筋症）、ビタミンC/壊血病（モルモット等の合成不能種）、ビタミンB群、チアミン(B1)、ヨウ素/甲状腺腫、亜鉛、タウリン（猫特異的）、蛋白エネルギー栄養失調/悪液質、肥満
- **致命的な誤適用をレビューで回避**:
  - `中毒`/`toxicosis`（亜鉛中毒・ビタミンD中毒＝毒性で toxicology 管轄）を欠乏症と誤記しないよう除外
  - `原発性`/`腎性`上皮小体機能亢進症（腫瘍性/腎性で非栄養性）を NSHP と誤適用しないよう除外
  - `肥満細胞腫`(mast cell tumor)≠`肥満`(obesity)、`甲状腺癌`/`甲状腺腫瘍`≠`甲状腺腫`(goiter=ヨウ素欠乏)
  - タウリン欠乏は猫のみ（非猫には猫用文を付与しない）

### 統合
- `fix_named_pathogens.py` / `migrate_to_sqlite.py` を viral→bacterial→fungal→parasite→nutrient の5段に拡張。

### 効果（配信SQLite実測）
- **205栄養性疾患**を疾患特異的病因・病態生理に置換。
- EN causes の distinct 値: 1,004（第5弾後）→ **1,126**（全バッチ前 604 から +86%）。

### 回帰テスト（+3件）
- `test_nutritional_library_resolver_precision` — 中毒/原発性HPT/甲状腺癌/肥満細胞腫を除外、タウリン猫限定
- `test_named_nutrient_causes_cite_correct_nutrient` — 壊血病=ビタミンC/コラーゲン、NSHP=Ca/PTH、鳥甲状腺腫=ヨウ素
- `test_no_generic_nutritional_causes_on_named_nutrients_in_json`

### テスト・CI
- フルスイート **3,482件合格**（34 skip、+3新規）、ruff clean

### named-agent キュレーション累計（第2〜6弾）
毒物64 + 原虫11 + ウイルス28 + 細菌24 + 真菌14 + 寄生虫22 + 栄養素12 = **175病原体/病因生成器**。感染症の全系統＋栄養性まで、名前が決定論的に原因を示す病因クラスを網羅し、計 **約1,200疾患**の病因・病態生理を汎用テンプレートから日英の疾患特異的記述に置換。

## 2026-07セッション（第7弾: 非感染性フラグシップの bilingual キュレーション）

### 背景: 既存フラグシップは JA のみ、EN は category テンプレートのまま
`curated_etiology` / `curated_common_diseases` は ~120 のフラグシップ疾患に優れた JA 病因・病態を供給するが **JA 専用**のため、これらのレコードの **英語 causes は "Cardiac etiology…"/"Endocrine or metabolic dysfunction…" 等の category テンプレートのまま**だった。加えて、名前が原因を一意に決めない非感染性フラグシップ（猫甲状腺機能亢進症・PDA・サドル血栓・レッグペルテス・BOAS 等）は未キュレートだった。

### `scripts/template_elimination/flagship_noninfectious_library.py`（新規、日英両対応）
非感染性の病因は病原体のように name-deterministic ではないため、明確に定義された高頻度フラグシップに限り教科書的知識を**日英両方**でキュレート。既存 pipeline（`fix_named_pathogens`）に接続し、category テンプレート/スタブのフィールドのみ置換するので、**JA がキュレート済みのレコードは英語のみアップグレード**され JA は温存される。
- **20の生成器**（causes + pathophysiology を JA+EN）:
  - 内分泌（猫）: 甲状腺機能亢進症・原発性アルドステロン症・先端巨大症、全身性高血圧（続発性）
  - 心臓: 猫サドル血栓、犬先天性（PDA・大動脈弁下狭窄・肺動脈狭窄）
  - 運動器/発育（犬）: レッグ・カルベ・ペルテス病・OCD・汎骨炎・HOD・ウォブラー症候群
  - 気道（犬）: 短頭種気道症候群(BOAS)
  - 神経（犬）: 認知機能不全症候群(CDS)・肉芽腫性髄膜脳脊髄炎(GME/MUO)
  - 皮膚/免疫: 脂腺炎・落葉状天疱瘡・脱毛症X（犬）、好酸球性肉芽腫群（猫）
- **頭字語の部分文字列衝突をレビューで回避**:
  - bare `ocd` → 「Compulsive Disorder (Canine OCD)」（行動疾患）を誤検出 → `osteochondritis dissecans`/`骨軟骨症`
  - bare `gme` → 「pi**gme**ntary uveitis」を誤検出 → `granulomatous meningoencephal`/`肉芽腫性髄膜脳`
  - `類天疱瘡`(pemphigoid)≠`天疱瘡`(pemphigus)、`副甲状腺`/`甲状腺機能低下`除外、`肺高血圧`≠全身性高血圧
  - 種ゲーティング（猫内分泌・犬先天性心疾患等）+ 多種生成器は英語に英語種名を使用

### 効果（配信SQLite実測）
- **50疾患**（品種・解剖・種別バリアント含む）を日英の疾患特異的病因・病態に置換。既存 JA キュレート済みフラグシップの**英語 causes をテンプレート→キュレートに昇格**。

### 回帰テスト（+3件）
- `test_flagship_library_resolver_precision` — ocd/gme頭字語衝突・pemphigoid・種ゲーティング除外
- `test_flagship_causes_are_bilingual_and_specific` — 日英両方が疾患特異的、多種生成器の英語種名検証
- `test_served_db_flagship_english_causes_curated` — 配信DBで PDA/サドル血栓等の英語 causes が category テンプレートでない

### テスト・CI
- フルスイート **3,485件合格**（34 skip、+3新規）、ruff clean

### 非感染性フラグシップ拡充 第2弾（既存JAキュレート済み疾患の英語 backfill）
`curated_etiology` の~120フラグシップは JA 専用のため英語 causes が category テンプレートのままだった。`flagship_noninfectious_library.py` に高頻度の内科フラグシップ16件を**日英**で追加。JSON は既に curated JA を持つ（テンプレートでない）ため、pipeline は**英語のみ**を安全に置換し、curated JA は温存される。
- 追加（犬猫）: GDV・膵炎・甲状腺機能低下症・クッシング症候群・慢性腎臓病・アトピー性皮膚炎・変形性関節症・椎間板ヘルニア・特発性てんかん・拡張型心筋症・粘液腫様僧帽弁変性症・糖尿病・炎症性腸疾患(猫)・肝リピドーシス(猫)・喘息(猫)
- curated_etiology と同じ除外を踏襲（甲状腺機能低下←副甲状腺/先天性、糖尿病←ケトアシドーシス/尿崩症、膵炎←膵外分泌不全/膵癌、僧帽弁←形成不全）
- flagship 解決数: 50→**78疾患**。回帰テストは既存3件でカバー（頭字語衝突・種ゲーティング・英語 causes 非テンプレート）。
- フルスイート **3,485件合格**、ruff clean。

### 非感染性フラグシップ拡充 第3弾（大規模拡張: 犬猫馬の主要疾患83件を追加）
既存 JAキュレート済みだが英語が未対応だった主要疾患群を大規模に追加。1つの生成器が複数の名称バリアント（解剖学的部位・品種特異的変異）を広範な部分文字列マッチでカバーする設計（既存のリンパ腫方式を踏襲）。
- **共通（種問わず）**: 緑内障・乾性角結膜炎(KCS)・角膜潰瘍・尿崩症（各種のsp引数で種名を動的挿入）
- **犬（29疾患）**: 股関節/肘関節形成不全・前十字靭帯断裂・白内障・進行性網膜萎縮(PRA)・チェリーアイ・膿皮症・巨大食道症・門脈体循環シャント(PSS)・慢性肝炎(銅関連)・会陰ヘルニア・停留精巣・アジソン病・IMHA・血管肉腫・骨肉腫・肥満細胞腫・リンパ腫・EPI・胆嚢粘液嚢腫・副甲状腺機能低下・変性性脊髄症・喉頭麻痺(GOLPP)・BPH・膝蓋骨脱臼・PRAA・肛門嚢疾患・PLE・食道炎/GERD・馬尾症候群・顔面神経麻痺
- **猫（22疾患）**: HCM/DCM/RCM・胆管炎(リンパ球性/好中球性)・巨大結腸症/便秘・尿道閉塞・PKD・結膜炎・ぶどう膜炎・好酸球性角結膜炎・角膜分離症・慢性歯肉口内炎・ITP・三叉神経炎・心筋炎・尿路結石(シュウ酸カルシウム/ストルバイト)・副甲状腺機能亢進(原発性/腎性二次性の2型を区別)
- **馬（14疾患）**: 屈腱炎・胃潰瘍(EGUS)・ピロプラズマ症・EPM・EMS・PPID・PSSM・横紋筋融解症・子宮内膜炎・大腸炎・食道閉塞(チョーク)・喉嚢疾患群・夏季牧草喘息・胎盤炎・馬再発性ぶどう膜炎(ERU)
- **部分文字列衝突をレビューで発見・回避**: 膵外分泌不全(EPI)は bare `epi` を使うと特発性てんかん(idiopathic **epi**lepsy)を誤検出するため full phrase 限定。門脈体循環シャント(PSS)は bare `pss` を使うと馬の PSSM（多糖類蓄積性ミオパシー）を誤検出するため full phrase 限定。猫の原発性/腎性二次性副甲状腺機能亢進症は病因が全く異なる（腺腫 vs CKD続発）ため2つの独立した生成器に分離。癒着性角結膜炎（症候性ぶどう膜癒着）は一般結膜炎と区別して除外。
- 効果: flagship 解決数 78→**245疾患**（品種/解剖バリアント含む）。英語 causes の distinct 値: 1,126（栄養バッチ後）→**1,262**。
- 回帰テスト +2件（衝突回避・原発性/腎性副甲状腺機能亢進の区別・尿路結石の溶解性コントラスト）
- フルスイート **3,488件合格**（34 skip）、ruff clean。


### 非感染性フラグシップ拡充 第4弾（エキゾチック伴侶動物 + PDD/ECE 病原体キー修正）
`flagship_noninfectious_library.py` にエキゾチック伴侶動物の高頻度フラグシップを追加（草食小型哺乳類・フェレット・鳥・爬虫類・両生類）。既存 JAキュレート済みだが英語未対応だった疾患群の bilingual backfill。
- **草食小型哺乳類共通**（ウサギ/チンチラ/モルモット/デグー、species引数で動的種名挿入）: 消化管うっ滞(GI stasis)・毛球症(トリコベゾア)
- **ウサギ固有**: エンセファリトゾーン症（腎/眼/神経の3型を1テキストで統合、既存curated_etiology設計を踏襲）・斜頸（前庭疾患）・潰瘍性足底皮膚炎（ソアホック、グレード共有）・子宮腺癌
- **モルモット固有**: 卵巣嚢胞（機能性/漿液性/濾胞性）　**ハリネズミ固有**: 針毛包炎
- **フェレット**: 副腎疾患(FAD、名称バリアント10件超を1生成器で統合)・インスリノーマ・心筋症(DCM/HCM統合)・リンパ腫
- **鳥類（鳥/インコ/オウム共通）**: 痛風（内臓型/関節型統合）・黄色腫
- **爬虫類（爬虫類/リクガメ/ヘビ/トカゲ共通）**: 脱皮不全(ディセクダイシス)・スペクタクル(アイキャップ)脱皮不全・甲羅疾患(甲羅腐敗症/SCUD)・敗血症
- **両生類固有**: 浮腫症候群(リンパ嚢浮腫)
- **種問わず共通**: 肝線維症（既存curated_etiologyのJA generic entryに英語をbackfill）

### PDD/ECE の pathogen_library 統合 + 頭字語衝突の追加是正
- **鳥ボルナウイルス(PDD)**: 「前胃拡張症」full phrase + 「PDD神経型」/「PDD Neurological」の精密複合キーで解決。**bare `pdd` は使用禁止**と判明: 「Gastric Dilatation (Non-PDD)」の日本語名「胃拡張（PDD以外）」は共有否定トークン`non-pdd`（英語のみ想定）でカバーされず、bare `pdd` だと誤マッチすることをレビューで発見。
- 共有 `_NEGATION_TOKENS`（`clinical_fields_generator.py`）に `非pdd`/`non-pdd` を追加（全 resolver 共通で恩恵）。
- **フェレット流行性カタル性腸炎(ECE)**: フェレット腸コロナウイルス(FRECV)であることを`pathogen_library.py`の`_coronavirus`にフェレット分岐として追加、「流行性カタル性腸炎」/「epizootic catarrhal enteritis」full phrase キーで解決（bare `ece` は"niece"等に誤爆するため不使用）。

### 真菌性甲羅疾患の誤カテゴリ発見・是正
爬虫類の甲羅疾患フラグシップ生成器（`_shell_disease_reptile`）は細菌性病因（Citrobacter等）を記述するため、「真菌性甲羅疾患」に適用すると誤り。`fungal_library.py`に`_fungal_shell_disease`（Fusarium/Paecilomyces）を新設し、flagship側は`真菌性`/`fungal`を除外して二重適用・誤適用を防止。

### 効果（配信SQLite実測）
- **99疾患**を疾患特異的病因・病態生理に追加置換。flagship 累計解決数: 245→**330疾患**。
- 英語 causes の distinct 値: 1,262→**1,307**。

### 回帰テスト（+3件）
- `test_flagship_batch4_exotic_resolver_precision` — エキゾチック解決精度、真菌性甲羅疾患の除外
- `test_flagship_batch4_pdd_bornavirus_and_ferret_ece_coronavirus` — PDD/Non-PDD衝突・ECE=コロナウイルス
- `test_served_db_flagship_batch4_exotic_english_causes_curated`

### テスト・CI
- フルスイート **3,491件合格**（34 skip）、ruff clean

### 既知の残課題（次セッション候補）
- 鳥/爬虫類の残りフラグシップ（PBFD以外の羽毛疾患、爬虫類代謝性骨疾患の個別種対応等）
- causes_ja/pathophysiology_ja の残りカテゴリテンプレートの疾患固有化（獣医レビュー前提で漸進的に）

## 2026-07セッション（第8弾: 両生類ツボカビ混入バグ + 爬虫類スペクタクル誤カテゴリの修正）

### 背景: データ汚染バグ（テンプレートではなく「具体的に間違った内容」）
前セッションで発見した「両生類の脱皮不全（Dysecdysis）」2件の causes_ja が、無関係なツボカビ症（Batrachochytrium dendrobatidis/Bd、B. salamandrivorans/Bsal）の感染経路テキストで完全に置き換わっていた（"Batrachochytrium dendrobatidis（Bd）またはB. salamandrivorans（Bsal）の遊走子が水中を介して皮膚に感染する…"）。これは汎用カテゴリテンプレートではなく「別疾患の具体的に正しい内容が誤った疾患に紛れ込んだ」データ汚染で、既存の置換可否判定（フィンガープリント/STUB_SIGNATURES/汎用マーク）のいずれにも該当せず、標準の名前解決パスでは検出も修正もできなかった。pathophysiology_ja は既に正しい内容（低湿度・ビタミンA欠乏・甲状腺機能異常を主因とし、ツボカビ感染は数ある基礎疾患の一つとして適切に言及）だったため、これは温存が必須だった。

### 両生類専用の脱皮不全ジェネレーターを追加
`scripts/template_elimination/flagship_noninfectious_library.py` に `_dysecdysis_amphibian()` を新規追加し、`_FLAGSHIPS` に `frozenset({"amphibian"})` 限定のレジストリエントリを追加（既存の爬虫類用 `_dysecdysis_reptile`（POTZ等の爬虫類専門用語を含む）とは完全に分離）。内容は既存の正しい pathophysiology_ja のフレーミング（低湿度・ビタミンA欠乏・甲状腺機能異常が主因、ツボカビ感染は基礎疾患の一つとして言及するが唯一の原因ではない）と整合させ、両生類の皮膚呼吸・皮膚からの水分吸収への依存という両生類特有の生理も明記。
- 汚染された causes_ja はテンプレートではなく特定の間違った内容だったため、`GENERIC_CAUSES_JA_MARKS`（`pathogen_library.py`）に汚染テキストのフィンガープリント `"の遊走子が水中を介して皮膚に感染する"` を追加。このマークは脱皮不全の名前キーに一致したエントリでのみ評価されるため、無関係な本物のツボカビ症エントリ（このマークにはヒットしない別文言）を誤って上書きするリスクはない。
- `fix_named_pathogens.py --apply` → JSON上の "Dysecdysis (Retained Shed)"（両生類）を修正。「Dysecdysis (Abnormal Shedding)」はJSONオーバーレイに存在せずPythonモジュール（`amphibian_diseases.py`）にも causes_ja/pathophysiology_ja が定義されていない（=NULL）ため、`migrate_to_sqlite.py` の `regenerate_named_pathogen_etiology()` 安全網が両エントリとも正しく修正。

### 副産物として発見・修正した既存バグ: 爬虫類「スペクタクル脱皮不全（アイキャップ残留）」のカテゴリ誤り
調査中に、`curated_etiology.py` の爬虫類 `_DYSECDYSIS`（`("脱皮不全",)` キー、除外なし）が "Retained Spectacle (Retained Eye Cap)"（name_ja: "スペクタクル脱皮不全（アイキャップ残留）"）にも部分一致し、本来の眼科疾患特異的内容ではなく汎用の脱皮不全文で上書きしていたことを発見（過去のセッションでこのキーに対する除外漏れがあった）。
- `curated_etiology.py` の爬虫類 `_DYSECDYSIS` キーに除外 `("スペクタクル", "spectacle")` を追加（他の類似キー、例: 鳥ビタミンA欠乏の `("過剰",)` 除外と同じパターン）。
- 汚染された causes_ja は既に `diseases_all_species.json`（Reptile種）に静的テキストとして焼き込まれていたため、コード修正だけでは反映されない。`flagship_clinical_fields()`（`_retained_spectacle_reptile` ジェネレーター）の出力で該当 JSON エントリの `causes_ja` と `pathophysiology_ja`（同様に汎用外傷カテゴリ文で誤っていた）を直接置換する一回限りの修正を実施。

### 効果（配信SQLite実測）
- 両生類脱皮不全2件: causes_ja のツボカビ混入 **完全除去**（"Batrachochytrium" 0件）、EN causes/pathophysiology も汎用感染症テンプレートから疾患特異的文に更新
- 爬虫類「スペクタクル脱皮不全（アイキャップ残留）」: causes_ja/pathophysiology_ja がスペクタクル特異的な眼科内容に修正（汎用脱皮不全文・汎用外傷文が残存 0件）

### 回帰テスト追加（tests/test_no_template_disease_content.py、+4件）
- `test_amphibian_dysecdysis_not_chytrid_contaminated` — Batrachochytrium不在、湿度/水質記述あり、POTZ用語不在、"Abnormal Shedding"も同様に解決、爬虫類ジェネレーターとの分離確認
- `test_reptile_spectacle_retention_not_mislabelled_as_generic_dysecdysis` — curated_etiology が None を返す、flagship がスペクタクル特異的内容を返す
- `test_served_db_amphibian_dysecdysis_and_reptile_spectacle_fixed` — 配信DBで両方の修正を確認

### テスト・CI
- フルテストスイート: **3,494件合格**（34 skip、+4新規）、ruff check/format 全て通過
- 再現手順: `fix_named_pathogens.py --apply` → 一回限りのJSON直接修正（スペクタクル） → `migrate_to_sqlite.py`

### 既知の残課題（次セッション候補）
- 鳥/爬虫類の残りフラグシップ（PBFD以外の羽毛疾患、爬虫類代謝性骨疾患の個別種対応等）
- causes_ja/pathophysiology_ja の残りカテゴリテンプレートの疾患固有化（獣医レビュー前提で漸進的に）
- 腫瘍学・多因子性疾患のcauses/pathophysiologyに残る汎用カテゴリガイダンス（医学的に妥当な内容だが疾患固有化の余地あり）

## 2026-07セッション（第9弾: 構造的・機械的疾患の感染テンプレート撲滅 + 英語説明文の日本語混入除去）

### 背景: 機械的疾患に「細菌が体内に侵入」— 臨床的に危険な誤り
配信DB監査で、**101件の構造的・機械的疾患**（膀胱結石・臓器脱・そ嚢うっ滞・盲腸/頬袋閉塞・臓器捻転・異物・卵塞等）が、causes_ja/pathophysiology_ja（および英語patho）に**感染症・中毒・寄生虫のカテゴリテンプレート**を保持していた。例: 犬「膀胱結石」の病因が「特定の細菌病原体の感染である。病原性細菌が体内に侵入…」（尿石症＝ミネラル析出なのに）、英語pathophysiologyが "The pathophysiology of infectious/parasitic/fungal/toxicosis diseases…" を機械的疾患に適用。獣医師が即座に発見する信頼失墜レベルの記述。根本原因は誤った保存カテゴリタグ（infectious等）をpathophysiology生成器が信用していたこと + 疾患名のタイプミス（膨胱結石←膀胱結石）。

### 構造的・機械的キュレートライブラリ（`scripts/template_elimination/structural_library.py` 新規）
病原体ライブラリの姉妹版。機械的機序は教科書的・種横断的な事実（結石＝凝固物、脱出＝突出、閉塞＝通過障害）なので捏造リスクゼロでキュレート。17機序生成器（causes + pathophysiology を JA+EN、種名補間・種特異的注記付き）:
- 尿石症（腎/膀胱/総排泄腔、爬虫類=脱水/温度勾配、草食=炭酸Ca）・臓器脱（直腸/総排泄腔/子宮/膣/陰茎/卵管）・異物（消化管/鼻腔/蹄/砂嚢）・そ嚢うっ滞（サワークロップ=二次発酵）・頬袋閉塞・盲腸停滞・消化管うっ滞（草食=肝リピドーシスリスク）・毛球症・臓器捻転（子宮/肝葉）・腺閉塞（肛門腺/臭腺/大腿孔）・嘴不正咬合・蹄過長・卵塞/卵胞停滞・披裂軟骨炎
- **機序修飾語を必須とするキー設計**（…閉塞/…stasis/…prolapse）で、同一臓器の腫瘍/膿瘍/壊死/カンジダ変異（肛門腺癌・頬袋膿瘍・嘴腐敗・陰茎壊死）は解決させない。加えて neoplasia/abscess/necrosis/mycosis/dysbiosis 等の除外リストを二重の安全網に。
- SIBO・繊毛虫過増殖（＝dysbiosis）は設計通り除外（機械的でない）。

### 統合と効果
- `fix_named_pathogens.py`／`migrate_to_sqlite.py` の `_clinical_fields` チェーン末尾に `structural_clinical_fields` を追加（named-agent・flagship の後）。fallback生成器の感染patho（「病原体（細菌・ウイルス・真菌・原虫）の感染が直接的な原因」）を捕捉する PATHO_JA_MARKS も追加。
- 疾患名タイプミス「膨胱結石」→「膀胱結石」を全11箇所修正（`diseases_all_species.json`、name_ja含む）→ 検索インデックス再生成。
- 効果: 構造的疾患の感染テンプレート **101→1**（残り1は Cryptosporidium/MBD/膀胱結石起因の努責を記述した**正当な種別キュレート**で、検出器の偽陽性）。副次的に named-pathogen 疾患の fallback感染patho も疾患固有化（増殖性腸症=L. intracellularis、各種膿瘍=好中球集積機序）。
- キュレート済みコンテンツ（ウサギ肝葉捻転patho、猫直腸脱patho）は温存を確認。

### 英語説明文（description）の日本語混入を撲滅（193件）
最も目立つ見出し要約フィールドで、モジュール/補足由来の**193件**が英語未対応だった:
- 170件: 内容空虚な英語スタブ "…is a clinical condition requiring veterinary evaluation…"（症状は記録済み）
- 23件: 完全日本語（新規追加疾患でENが未翻訳）または英語文に日本語検査名混入（"Work-up typically uses 身体検査…"）
- `migrate_to_sqlite.py` に `ground_stub_descriptions()` を追加。CJK混入または空スタブの英語説明を、その疾患自身の症状・推奨検査（**Latin文字のみにフィルタ**しCJK漏出を防止）・緊急度・名前ベースカテゴリから `compose_grounded_description` で再構築（記録済みデータの言い換えのみ、新規医学的主張なし）。
- 効果: 英語説明のCJK混入 **0件**。英語causes のCJK混入も構造的修正の副次効果で 115→20。

### バグ修正（本セッションで作り込んだものを検出・是正）
- 構造的生成器の一部が英語文に `nj`（日本語名）を使用（"脾捻転 in dogs is…"）→ 全5箇所を英語名 `_en_name(ne, fallback)`（CJKガード付き）に修正。JSONをリセットして修正後生成器で再適用。
- 種名サフィックスの重複（"トカゲの膀胱結石（トカゲ）は…"）を `_strip_species_suffix` で除去。

### 回帰テスト追加（tests/test_no_template_disease_content.py、+4件）
- `test_structural_library_resolver_precision` — 機械的名は解決、同一臓器の腫瘍/膿瘍/壊死/カンジダ/SIBO は非解決
- `test_structural_causes_name_the_mechanism_not_infection` — 結石=ミネラル/尿石、脱出=努責/straining、そ嚢=運動低下
- `test_served_db_structural_diseases_not_infection_templated` — 配信DBで機械的疾患に感染patho（EN/JA）が残っていない
- `test_served_db_english_description_has_no_japanese` — 英語説明にCJKが残っていない

### テスト・CI
- フルテストスイート: **3,498件合格**（34 skip、+4新規）、カバレッジ81.15%
- ruff check / format: 全変更ファイルで通過
- 再現手順: `fix_named_pathogens.py --apply` → `migrate_to_sqlite.py` → `build_disease_search_index.py`

### 既知の残課題（次セッション候補・要人手翻訳）
- **52疾患の英語臨床フィールドが完全日本語**（新規追加のJA-first コンテンツ: 観賞魚26疾患、馬の胃潰瘍/繁殖疾患、新生児症候群、マムシ咬傷等）。causes/treatment/prevention/prognosis/clinical_signs/pathophysiology が未翻訳。**臨床用量プロトコルの機械翻訳は患者安全上のリスク**があるため本セッションでは自動翻訳せず、獣医監修下での人手翻訳を推奨（description は英語グラウンディング済み）。

## 2026-07セッション（第10弾: 英語 causes の日英カテゴリ・パリティ — 内容空虚な catch-all の撲滅）

### 背景: 英語 causes だけが日本語と非同期の「単一 catch-all」だった
過去セッションで日本語 `causes_ja` は `gen_causes_ja`（獣医監修済みのカテゴリ対応生成器、25カテゴリ）で正しいカテゴリに解決済みだった。しかし**英語 `causes` にはカテゴリ対応の生成器が存在せず**（`gen_causes_ja` はあるが `gen_causes`(EN) は欠落）、836疾患が単一の**内容空虚な catch-all**「Multifactorial etiology depending on disease type. Includes infectious agents, environmental factors…」を、残りが日本語カテゴリと**非同期**の英語カテゴリテンプレートを保持していた。
- 実測（配信DB 7,094疾患）: 英語 causes の modulo-name テンプレート率 **86%**、distinct 値わずか **886**。
- バイリンガル臨床ツールとして致命的: 英語ユーザーが *Heart Disease* を開くと「Multifactorial etiology depending on disease type」（無内容）、日本語ユーザーは正しい循環器病因を見る、という日英不一致。「一般公開しても評価の高いUX」を損なう最大要因。

### `gen_causes`(EN) の実装 — `gen_causes_ja` の忠実な英語ミラー
`clinical_fields_generator.py` に `gen_causes(category, name_en, species)` を追加（25カテゴリ、`gen_causes_ja` と同一の医学内容を英訳、新たな医学的主張なし）。英語版の毒性ソース辞書 `TOXIN_SOURCES_EN` / `_toxin_sources_en` も追加（種別に適切な毒物例を列挙）。既存の英語生成器（`gen_clinical_signs`/`gen_transmission`/`gen_diagnosis`/`gen_description`）と同じクリーンなスタイル。

### 日英パリティを保証する検出・置換ロジック（`generic_english_causes.py` 新規）
「捏造ゼロ」で日英を一致させる設計:
- **検出**: 英語 causes が汎用カテゴリテンプレート（`GENERIC_CATEGORY_CAUSES_EN_MARKS`、47マーク）にマッチ。内容空虚な catch-all・`<system> etiology. includes…`・`<Category> diseases result from…`・`Caused by progressive deterioration of…` 等を網羅。**名前付き病原体（Salmonella等）・機序特異的（Urolithiasis causes:等）は除外**（正当な共有）。
- **名前付き病原体の保護**: `viral/bacterial/fungal/parasite/nutrient/flagship/structural` の各 `_clinical_fields` に解決する疾患は**スキップ**（named-pathogen パスが所有）。
- **カテゴリ決定**: 既にレビュー済みで正しい `causes_ja` を `fingerprint_etiology` でカテゴリ判定し、**同一カテゴリ**の英語文を適用 → 日英カテゴリが完全一致。JA がキュレート済み（fingerprint None）の場合のみ `resolve_true_category` にフォールバック。
- JSONパス `eliminate_generic_english_causes.py --apply`（4,060件置換）+ 配信DB安全網 `ground_english_causes_to_category`（`migrate_to_sqlite.py`、named-pathogen/re-categorisation の**後**に実行しモジュール由来6件を捕捉）。

### 効果（配信SQLite実測、7,094疾患）
| Metric | Before | After |
|---|---|---|
| 内容空虚な「Multifactorial」catch-all | 836 | **0** |
| distinct な英語 causes | 886 | **5,366**（6倍） |
| 英語 causes modulo-name テンプレート率 | 86% | 75%※ |
- ※残る75%は**正しいカテゴリに解決済み**の許容可能なカテゴリテンプレート（腫瘍/前庭→神経/肝→消化器 等）＋名前付き病原体の正当な共有。内容空虚・誤カテゴリはゼロ。確立された方針（causes のカテゴリレベル記述は許容、無内容 catch-all と誤カテゴリは不許容）に完全準拠。
- 手動サンプル10疾患で日英カテゴリ完全一致を確認（Heart Disease→cardiac, von Willebrand→genetic_congenital, IBD→gastrointestinal, SLE→autoimmune, OCD→behavioral 等）。

### エンドツーエンド検証
- API: `/api/diseases/<id>` が更新後の英語 causes を配信（status 200、正しい循環器病因テキスト）を確認。
- フロントエンド: `app.js` の言語ピック `(ja,en)=>currentLang==="ja"?...:(en||ja)` が英語UIで英語 causes を表示（鑑別診断結果ビュー + 疾患DB詳細パネルの両表示箇所）を確認。

### 回帰テスト追加（tests/test_no_template_disease_content.py、+4件）
- `test_no_contentless_multifactorial_causes_in_json` / `test_served_db_no_contentless_multifactorial_causes` — 内容空虚 catch-all の不在（JSON + 配信DB）
- `test_english_causes_matches_japanese_category` — `gen_causes`(EN) が各カテゴリで正しいキーワードを含み catch-all を生成しない
- `test_generic_english_causes_skips_named_agents` — 名前付き病原体疾患は上書きされない、非病原体は昇格される

### テスト・CI
- フルテストスイート: **3,508件合格**（34 skip、+4新規）
- ruff check / format: 全変更ファイルで通過
- 再現手順: `eliminate_generic_english_causes.py --apply` → `migrate_to_sqlite.py`

### 次セッション候補
- 英語 pathophysiology の残りカテゴリテンプレート（9%、grounding で対応可能）
- Ehrlichia/Anaplasma/Babesia 等の named-agent 化（現状はカテゴリ解決で日英一致だが、病原体特異化の余地あり）
- 52疾患の完全日本語な英語臨床フィールド（要人手翻訳、患者安全上の理由で自動翻訳せず）
## 2026-07セッション（第11弾: 疾患重複カードの撲滅 + 可視フィールドのクロス種テンプレート除去）

### 背景: 同一疾患が2枚のカードで表示される公開品質バグ
複数の種モジュールが同一疾患を2エントリで保持しており、疾患ブラウザに**同一カードが2枚**表示されていた（例: dog「特発性てんかん」×2、chinchilla「熱中症」「難産」「子宮蓄膿症」各×2）。原因は英名の綴り違い（Xylitol Poisoning / Xylitol Toxicosis）や冗長な種サフィックス（Heat Stroke / Heat Stroke - Chinchilla）で同一疾患が重複登録されていたこと。監査で(species,name)完全重複11組＋(species,name_ja)重複33組を検出。

### 中央集約的な重複排除（`dedupe_disease_list`、非破壊）
`api/species/helpers.py` に `dedupe_disease_list(diseases)` を追加。同一種内で **英名 OR name_ja が一致**する2エントリを同一疾患とみなし（UIは name_ja(JA)/name(EN)を表示するため、どちらか一致すれば見た目は同一カード）、内容が最も充実したエントリ（非空フィールド数→総文字数→先頭優先）を残す。union-findで推移的にマージ。dict/dataclass両対応、入力非破壊。
- 全読み込み経路に適用（ソース.pyは無改変・可逆）:
  - `vetdict_api._load_diseases`（SEO詳細ページ/ハブ/サイトマップ/横断検索）
  - `health_checker.get_diseases`（SPA疾患ブラウザ）
  - `migrate_to_sqlite`（配信DB、生成idの安定性のため元indexを保持）
  - `helpers.enrich_diseases` 末尾（低メモリ本番の実行時オーバーレイ経路）
- 効果: 配信DB **7,094→7,055疾患**（39重複を統合）。全21種でブラウザに重複カード **0**。残す方は常により充実したエントリ（39件全て検証）。

### 可視フィールドのクロス種テンプレート除去（`strip_cross_species_clauses`）
可視JAフィールド（prevention_ja/causes_ja/treatment_ja等）に、古いenrichmentが焼き込んだ**多種列挙ボイラープレート**が残存（監査で999件）。ジェネレータ自体は既に種別対応済みで、これは**過去生成の残留汚染**。7種類の識別可能な文が大半を占めた:
- 「支持療法（爬虫類）: 種別POTZ…」が非爬虫類の治療に548件（POTZは爬虫類概念）
- 「甲状腺機能亢進症（猫）: ヨウ素…」「喘息（猫）: …」が非猫の予防に計380件超
- 「⑤ アトピー性（犬）: シクロスポリン…」等
`strip_cross_species_text(text, species)` を追加。**文頭（リスト記号・改行を除去後）が既知のクロス種マーカーで始まる文のみ**を除去し、コンマ列挙内のインライン言及（「…、甲状腺機能亢進症（猫）、…」）は温存。フィールドを空にしない安全ガード付き。
- `health_checker.get_diseases`（SPAブラウザ）+ `migrate_to_sqlite` 配信DBスイープ `strip_cross_species_clauses_in_served_db` に適用。
- 効果: 配信DBのクロス種文 **753→0**（爬虫類自身のPOTZ・猫自身の予防文は温存を確認）。dog甲状腺機能低下症の予防文が「糖尿病:…。クッシング:…。アジソン:…」と自然に流れることを確認。

### 表示数値の同期
`static/js/app.js` の `setDefaultStats()` フォールバック（API失敗時のみ表示）を重複排除後の実測値に同期（dog 622→611, chinchilla 278→266 等13種、総数 7093→7055）。

### 回帰テスト（tests/test_disease_dedup.py、22件）
- dedup単体: 英名/name_ja/推移マージ、順序保持、dataclass対応、非破壊
- dedup統合: 7種のSPAブラウザ応答に重複英名/JA名が無い
- cross-species: 爬虫類ブロックを哺乳類から除去し爬虫類では温存、猫予防文を犬から除去、インライン言及は温存、改行前置クラウス対応、空にしない
- `test_enrich_diseases.py::test_multiple_diseases`: プレースホルダ name_ja 衝突を回避するため2疾患に個別 name_ja を付与

### テスト・CI
- フルテストスイート: **3,526件合格**（34 skip）
- ruff check/format: 全変更ファイルで通過
- ServiceWorker: `CACHE_NAME` v86 → **v87**
- 再現手順: `migrate_to_sqlite.py`（dedup/cross-species strip は配信DBビルドに統合済み）

## 2026-07セッション（第10弾: 英語 causes/pathophysiology の組織系パリティ + リゾルバ衝突バグ修正）

### 背景: 英語 causes が組織系テンプレートに埋もれ、危険な誤カテゴリを含んでいた
日本語 causes は多セッションのキュレートで category-correct になっていたが、**英語 causes は旧 exotic-enrichment の組織系テンプレートのまま**（identical-modulo-name で87%）。単なる generic ではなく、**炎症性「-itis」疾患159件が「Caused by exposure to toxic substances（毒物曝露が原因）」と記述**される致命的な誤り（角膜炎・肝炎・心筋炎・皮膚炎等）。獣医師が即座に発見する信頼失墜レベル。日本語側は同レコードで正しく眼科/心臓/消化器と記述されていた。

### 英語カテゴリ生成器の新設（`clinical_fields_generator.py`）
- `gen_causes_en(category, name_en, species)` — `gen_causes_ja` の26カテゴリ英語ミラー（獣医監修済みの日本語と同一の医学内容）
- `gen_pathophysiology_en(category, name_en, species)` — `gen_pathophysiology_ja` の英語ミラー
- `TOXIN_SOURCES_EN` / `_toxin_sources_en` — 種別の毒性源例（英語）

### 修正スクリプト `scripts/template_elimination/fix_english_causes_category.py`（新規）
- 40+の generic 英語 causes テンプレート fingerprint を検出 → 疾患**名**から category を解決（信頼済み name-based resolver）→ `gen_causes_en` で再生成。キュレート/named-agent 文（fingerprint非該当）は不変。名前が category に解決しない場合は不変（捏造しない）。
- 多因子疾患は flagship 生成器を優先（例: 蹄葉炎は musculoskeletal ではなく内分泌性）。`flagship_noninfectious_library.py` に **蹄葉炎の bilingual 生成器 `_laminitis_horse`** を追加（EMS/PPID高インスリン血症・敗血症性・過重負重性）。
- **pathophysiology の誤カテゴリ修正**: 「The pathophysiology of {parasitic/viral/fungal/toxicosis} diseases…」を、名前が当該 category を示さない疾患（心筋炎=parasitic 等）でのみ再生成。**genuinely parasitic/toxic な疾患（名前が当該 category に一致）は温存**（Thelazia眼虫/Syngamusガペ虫/Cryptosporidium/マムシ咬傷等）。bacterial/infectious テンプレートは骨髄炎・心内膜炎・髄膜炎等が真に細菌性のため対象外。

### リゾルバ衝突バグ4件を修正（`resolve_category_from_name`、JA description/migration にも波及）
| バグ | 修正前 | 修正 |
|---|---|---|
| `カリシ` が `カリシン` を誤検出 | 夏癬（カリシン=Culicoides過敏症）→ viral | `カリシ(?!ン)` |
| bare `cystitis` 部分一致 | 胆嚢炎(Cholecystitis)・涙嚢炎(Dacryocystitis) → renal | `\bcystitis`（語境界） |
| `lens` 欠落 | 水晶体脱臼(Lens Luxation) → musculoskeletal | ophthalmic に `水晶体|lens` 追加 |
| worm 疾患の組織系誤解決 | Gapeworm→呼吸器, Eyeworm→眼科（実は寄生虫） | parasitic に `eyeworm|gapeworm|Syngamus|lungworm` 等追加（bare `worm` は ringworm=真菌のため不使用） |
- 追加の精密トークン: 鼻炎/副鼻腔炎→respiratory_infection、心膜炎/心内膜炎→cardiac、口内炎→dental、筋炎/腱炎→musculoskeletal、envenom/snakebite→toxicity。組織系フォールバック（心血管/消化管/生殖器等、**最低優先度**で合成複合名「Gastrointestinal Inflammatory Disease」等を捕捉、特異的パターンが常に優先）。

### 配信DB安全網（`migrate_to_sqlite.py`）
- `regenerate_english_category_causes(conn)` + `regenerate_english_pathophysiology_miscat(conn)` を追加（recategorize の後）。JSON overlay が届かないモジュール専用エントリを捕捉。

### 効果（配信SQLite実測、7,094疾患）
- 炎症性疾患の毒物テンプレート（EN causes）: **159 → 0**
- 英語 causes 再生成: **2,942件**（category-correct パリティ）。Colic の誤 parasitic causes、Cholecystitis の誤 renal 等を是正
- 英語 pathophysiology 誤カテゴリ修正: **280件**（心筋炎/Pica/脳炎/貧血/脱毛症の誤 parasitic 等）
- 残207 parasitic/toxicosis patho は genuinely parasitic（Dourine/Surra/鳥マラリア=トリパノソーマ/Plasmodium）またはリゾルバ None の pre-existing（保守的に温存）

### 回帰テスト（+9件）
- 毒物テンプレートが -itis 疾患に無い（JSON/配信DB）、リゾルバ衝突（カリシ/cystitis/lens）、炎症性の system 解決、gen_causes_en の category 正確性・冪等性、蹄葉炎=内分泌、pathophysiology fixer が genuine parasitic を温存し心筋炎を修正、worm 疾患=parasitic/ringworm=fungal

### テスト・CI
- フルテストスイート: **3,510件+ 合格**（新規9件）、ruff check/format 全変更ファイル通過
- 再現手順: `fix_english_causes_category.py --apply` → `migrate_to_sqlite.py`

### 既知の残課題（次セッション候補）
- 英語 causes/pathophysiology の category-generic は依然クラスタ化（causes は徴候グラウンディング不可のため named-agent/flagship キュレートの継続が本質的改善）。`curated_etiology`（JA専用100+疾患）の bilingual 化が英語ユニーク性の最大レバー
- リゾルバ None の pre-existing patho 誤テンプレート（Erysipelas→toxicity 等、数十件）— 名前が category に解決しないため要キュレート

## 2026-08セッション（エラーチェック + 薬用量マニュアルの欠落是正 + 相互作用参照のクリック導線）

### 全域エラーチェック（結果: 既存データは健全）
- ruff（変更ファイル）clean、フルテスト **3643 passed / 68 skipped**、カバレッジ 81.66%
- 監査で確認した完全性（いずれも欠落0）:
  - 薬用量: safe=true エントリで dosage 欠落 0（571→573薬品）
  - 麻酔: 全21種 × 全8カテゴリ完備、全プロトコルに用量あり、緊急対応は RECOVER 準拠（エピネフリン 0.01 mg/kg IV 低用量、アトロピン 0.02-0.04 mg/kg）
  - 疾患: 配信ビュー6529件・JSON6449件で主要臨床フィールド（治療/病因/予後/予防/病態/説明）の空欄 0
  - 種致死薬の安全フラグ正常（猫ペルメトリン/アセトアミノフェン、ウサギフィプロニル = safe:False）

### 薬用量マニュアルの欠落是正（自己参照的ギャップ2件）
薬品辞書が「自分が収載する薬品」から参照する薬剤を収載していない欠落を is-referenced-but-absent 監査で検出し補完:
- **ネオスチグミン**（新規, `drug_batch_11.py`）: アトラクリウム（収載済み・非脱分極性NMBA）の notes が「ネオスチグミン（＋グリコピロレート）で拮抗」と指示するのに本体が未収載だった。可逆的AChE阻害によるNMBA拮抗機序、犬猫馬ウサギの用量（0.02-0.05 mg/kg 緩徐静注＋抗コリン薬必須）、脱分極性遮断への非適応・機械的閉塞での禁忌を明記（Plumb's / Lumb & Jones 5th ed）
- **アスピリン（アセチルサリチル酸）**（新規, `drug_batch_11.py`, category=cardiovascular）: 相互作用参照4回・獣医の主力薬（猫ATE予防・犬過凝固）なのに未収載だった。犬（抗血小板0.5-1 mg/kg q24h）・猫（低用量5 mg/頭 q72h、**毎日投与禁止**＝グルクロン酸抱合能低下による蓄積回避、クロピドグレルが第一選択 FATCAT 2015）・馬。COX不可逆アセチル化機序、消化管潰瘍・サリチル酸中毒の警告付き
- 回帰テスト +2件（`test_nondepolarizing_nmba_reversal_agent_is_documented`, `test_aspirin_present_with_feline_dosing_caution` — 猫が q48-72h でありq24hでないことを検証）

### UX: 相互作用参照のワンタップ導線
薬品詳細の drug_interactions は参照薬剤名を素のテキスト表示していた。参照薬剤が辞書に収載されている場合のみ `.drug-nav-link` 化し、タップでその薬品へ移動・自動展開（既存の `navigateToDrug` + 委譲ハンドラを再利用）。「reverse with X」から X まで1タップ。薬品クラス参照（aminoglycosides 等）は解決せず素のテキストのまま（`_resolveInteractionDrug` が id/name 完全一致のみ解決）。
- `static/css/main.css`: リンク化された `.interaction-drug` にドット下線＋ポインタのアフォーダンス
- ServiceWorker: `CACHE_NAME` v99 → **v100**

### UX: 「よくみられる疾患」チップから疾患詳細へのワンタップ導線
`/api/species/<species>/common-diseases` が返す「この動物種でよくみられる疾患」チップ（種選択画面・チャット結果の両方）を素のテキスト表示からクリック可能な `<button>` 化。タップで疾患DBの該当詳細へ移動・自動展開（`navigateToDiseaseDb` 再利用）。
- **安全なクリック時解決** `_resolveCommonDiseaseName()`: prevalence_data のラベルが正規疾患名と異なる場合でも、ロード済みの `allDiseases`（閲覧可能な実データ）に対して ①完全一致（name/name_ja）②トークン集合一致（"Gout (Articular)" ↔ "Articular Gout" のような語順違いを安全に解決、内臓型/関節型は区別）③一意な部分一致（"(CKD)"/"(BPH)" 等の接尾辞）で解決。曖昧・不一致時は生の名前で検索にフォールバックし、**誤った疾患を開かない**（獣医向けの安全性）。
- カバレッジ実測: 全21種897件中843件（94%）が正しい疾患へ移動。残り54件（6%）は prevalence_data と疾患名の既存不整合（例: "Xylitol Toxicosis" vs "Xylitol Poisoning"、"GI Stasis" vs "Gastrointestinal Stasis"、"Snuffles (Bordetella)"=臨床的にも誤り→実際は Pasteurella）で、フィルタ検索に graceful フォールバック。→ **次セッション候補: prevalence_data の 199 dead key（疾患名不一致）の正規名への突合。これらは診断時の有病率補正でも現状 inert なため、突合すれば診断精度にも寄与**。
- ServiceWorker: `CACHE_NAME` v100 → **v101**

## 2026-08セッション（第2弾: prevalence_data の dead key 突合 — 診断有病率補正の活性化 + よくみられる疾患チップの正規化）

### 背景: prevalence キーの疾患名不一致で有病率補正が inert だった
`SPECIES_PREVALENCE`（種別の「よくみられる疾患」＝有病率ティア）のキーは、診断エンジン（`disease_matcher._match_species_symptoms_to_diseases`）でも `/api/species/<species>/common-diseases` エンドポイントでも**英語疾患名の完全一致**で照合される。キーが実際の疾患名と綴り違い（例 "Xylitol Toxicosis" vs 正規 "Xylitol Poisoning"）だと、そのエントリは**完全に inert**: 診断スコアの有病率補正が一切効かず、チップは name_ja 空欄で表示され、クリック時のみ fuzzy 解決にフォールバックしていた（前セッションで next-session 候補として明記）。

### 監査と是正
配信SQLite（7,058疾患）の実疾患名に対し全 prevalence キーを照合し、**85 dead key**（どの疾患名にも一致しない）を検出。臨床的に同一疾患と確信できるもののみを是正（有病率ティアは curated 判断なので不変、キー文字列だけを正規名に合わせる）:
- **40 key を正規疾患名に rename**（inert だった有病率 prior を活性化）
  例: dog "Xylitol Toxicosis"→"Xylitol Poisoning"、cat "Feline Pulmonary Edema"→"Pulmonary Edema"、bird "Trichomoniasis (Canker)"→"Trichomoniasis"、"Avian Mycobacteriosis"→"Mycobacteriosis (Avian TB)"、snake "Retained Spectacle"→"Retained Spectacle (Retained Eye Cap)"、chinchilla "Diabetes Mellitus"→"Diabetes Mellitus - Chinchilla" 等
- **12 key を削除**（既に active な正規キーの重複＝二重の inert エントリ。壊れた重複チップの原因）
  例: dog "Immune-Mediated Hemolytic Anemia (IMHA)"（"Immune-Mediated Hemolytic Anemia" が既に active）、rabbit "Snuffles (Bordetella)"（**臨床的にも誤り**＝スナッフルは Pasteurella。正規 "Pasteurellosis (Snuffles)"=very_common が既に active）、guinea_pig "Ovarian Cystic Disease"（"Ovarian Cysts"=very_common が既に active）
- **合計52 key を是正、dead key 85→33**（総キー数 1,302→1,290）

### 効果
- **診断精度**: 是正した40疾患で有病率 prior（very_common ×1.20 〜 rare ×0.80）が診断ランキングに実効化（従来は乗数1.0のまま）。
- **クリックUX**: `/common-diseases` チップの name_ja 空欄が主要種で解消（dog/cat/snake/reptile/hamster 等で残0）。チップ名が正規疾患名と一致するため、クリック時は fuzzy 解決を経ず**疾患DB詳細へ完全一致で移動・自動展開**。
- 残33 dead key は当該種のDBに疾患エントリ自体が存在しないもの（例: `exotic_other` の観賞魚疾患 Ich/Fin Rot/KHV、chinchilla Fatty Liver Disease、bird Renal Disease、amphibian Parasitic Dermatitis 等）。強制マッピングせず温存（獣医向けの安全性 — 誤った疾患に紐付けない）。→ **次セッション候補: これら真の欠落疾患の DB エントリ新規追加（エビデンスベース、獣医監修前提）**。

### エラーチェック（結果: 既存データは健全）
- ruff（変更ファイル）clean、フルテスト全合格 + 新規回帰テスト3件
- 完全性再監査（欠落0を再確認）:
  - 薬用量: safe 薬品の dosage 欠落 0（573薬品、species_info 3,459エントリ全て dosage あり）
  - 麻酔: 全21種×全8カテゴリ完備、薬剤行の用量欠落 0（monitoring/recovery はガイドライン記述で drugs 無しが設計通り）
  - 疾患: treatment/prevention/prognosis 100%（配信7,058疾患）

### 回帰テスト（tests/test_prevalence_data.py、+3件）
- `test_previously_dead_keys_now_resolve` — 是正した主要キーが実疾患名に一致すること
- `test_removed_duplicate_keys_stay_removed` — 削除した重複キーが復活しないこと
- `test_dead_key_count_stays_capped` — dead key 総数を ≤40 に上限ガード（将来の inert キー再混入を検出）

### 注記
- 変更は Python データ（`api/species/prevalence_data.py`）のみ。static 資産は不変のため ServiceWorker `CACHE_NAME` は据え置き。

## 2026-08セッション（第3弾: 診断/臨床徴候セクションの実行時グラウンディング + SGLT2阻害薬2剤 + 疾患ナビの完全一致着地）

### エラーチェック
- **repo全体の ruff エラー10件を是正**（CIは変更ファイルのみlintするため main に混入していた）:
  - `reco2/engine.py` の数学記法（I, P, T_base, D, T_final）→ pyproject に per-file-ignore `"reco2/*" = ["N803"]` を追加（意図的記法として許容）
  - camelCase テスト関数名1件（N802）・非CapWordsテストクラス名4件（N801）をリネーム
- **フルテストスイートの「36失敗」は環境アーティファクトと特定**: 監査スクリプトの app import が空の `instance/vetdict.db`（24KB スキーマのみ）を自動生成 → `test_served_db_*` のスキップガード（存在チェック）を欺いて失敗。`migrate_to_sqlite.py` で実DBを構築（7,058疾患、treatment/prevention/prognosis 100%）して全36件が合格。実回帰ゼロ。

### 疾患内容: 診断（diagnosis）/臨床徴候（clinical_signs）の実行時グラウンディング
- **ギャップ**: 733疾患が diagnosis/diagnosis_ja 両方空、多数が clinical_signs 両言語空。SQLiteビルドは `ground_missing_clinical_signs_and_diagnosis` で充填済みだが、**低メモリ本番はPythonモジュール直配信のためこのパスを通らず**、SPA疾患詳細・SEOページで該当セクションが黙って消えていた
- `api/health_checker.py` に `_ground_missing_supplementary_fields()` を追加（migrate の composer と同一の文テンプレートをローカル実装 — `scripts` パッケージが全ての本番レイアウトで import 可能とは限らないため）:
  - clinical_signs: 両言語空の場合のみ、レコード自身の `symptoms_display` から日英を構築
  - diagnosis: 言語別に独立して空側のみ、`recommended_tests_display` から構築（英語側はCJK混入ガード付き）
  - キュレート済み prose は決して上書きしない。徴候/検査が無いレコードは空のまま（捏造しない）
- `/api/health-check/diseases`（SPA疾患ブラウザのデータ源）で dedupe 前に適用
- SEOページ（`vetdict_api.py` disease_detail ルート）にも適用 — **モジュールdictは共有オブジェクトのためコピーしてから充填**（in-place 汚染なし）
- 効果（フォールバック配信パス実測、6,529疾患）: diagnosis_ja 空 **733→0**、diagnosis(EN) 空 **733→21**（残21は日本語先行レコードでLatin検査名が無いもの＝設計通り空維持）、clinical_signs 両言語空 **→0**。馬にも diagnosis セクションが初めて付与（`recommended_exams` タプル由来）

### 薬用量マニュアル: SGLT2阻害薬2剤の欠落是正（referenced-but-absent、`drug_batch_32.py` 新規）
- 猫糖尿病の疾患エントリが「Bexagliflozin (Bexacat) and velagliflozin — SGLT2 inhibitors」（AAHA 2023）を推奨するのに**両剤とも薬品辞書に未収載**だった:
  - **ベキサグリフロジン（Bexacat）**: 15 mg/頭 PO q24h 固定用量（体重3kg以上・インスリン未治療猫のみ）。FDA NADA 141-568、Hadd 2023 JVIM（治療成功率84%）
  - **ベラグリフロジン（Senvelgo）**: 1 mg/kg PO q24h 液剤。FDA NADA 141-576、Niessen 2024 JVIM（インスリングラルギン非劣性RCT）
- クラス定義の安全警告を両剤に明記: **正常血糖DKA**（血糖正常でもケトン監視必須）、インスリン併用/使用歴は禁忌、犬は safe:False（犬糖尿病はインスリン依存性でSGLT2単剤はDKAリスク）
- 薬品総数: 579 → **581**
- 回帰テスト: `test_sglt2_inhibitors_present_with_edka_warning`（用量・insulin-naive 制限・eDKA/ケトン警告・insulin 相互作用・犬 safe:False を検証）

### UX: 疾患クロスリンクの完全一致着地（薬品ナビ修正と同型のバグ）
- `navigateToDiseaseDb`（関連疾患チップ・よくみられる疾患チップ）と `openDiseaseAcrossSpecies`（横断検索結果）が**フィルタ結果の先頭行を無条件展開**していた。フィルタは部分一致のため「Gastritis」クリックで「Chronic Gastritis」が開く等、**意図と違う疾患に着地**
- 共有ヘルパー `_pickListItemByName(list, query)` を新設: 括弧サフィックス前の基底名の完全一致（日英・大文字小文字無視）を優先し、無ければ先頭行にフォールバック。`navigateToDrug` の同一インラインロジックも本ヘルパーに統合（3ナビゲーション全てが同じ着地規則）
- 疾患行テンプレートに `data-name` / `data-name-ja` を付与（薬品行と同形式）
- 回帰テスト: `test_app_js_navigation_lands_on_exact_match` + グラウンディングの `test_api_diseases_diagnosis_grounded_at_read_time` / `test_api_diseases_grounding_never_overwrites_curated_prose`

### 麻酔データ監査（結果: 健全）
- 全21種×全8カテゴリ完備、188プロトコル、薬剤行の用量欠落0、参考文献全種あり
- 主要用量のエビデンス照合: RECOVER（エピネフリン 0.01 mg/kg 低用量・アトロピン 0.02-0.04）、ウサギ アトロピン 0.05（アトロピナーゼ考慮）、猫 ALF 5 mg/kg IV（Tamura 2021）、犬猫プロポフォール 2-6 mg/kg 等 — 逸脱なし

### テスト・CI
- ruff check: repo全体 clean（従来は変更ファイルのみ）、ruff format: 変更ファイル通過
- ServiceWorker: `CACHE_NAME` v105 → **v106**

## 2026-08セッション（第4弾: referenced-but-absent 薬品14剤の大規模補完 + チャット候補カードのクリック導線）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,755件合格**（34 skip、カバレッジ81.74%）
- 配信SQLite再構築: 7,058疾患、treatment/prevention/prognosis 100%
- 薬用量: safe薬品の dosage 欠落 **0**（全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備、プロトコル薬剤行の用量欠落 **0**、ベース薬剤は
  EMLA・50%ブドウ糖を除き全て薬品辞書に収載済み（本セッションで両者を補完）

### 薬用量マニュアル: referenced-but-absent 14剤の補完（`drug_batch_33.py` 新規、581→595薬品）
相互作用の後方参照・疾患治療プロトコル・麻酔プロトコルの3系統を突合する
is-referenced-but-absent 監査で、コンテンツが参照するのに未収載だった14剤を検出・補完:
- **ピリメタミン** — EPM 22疾患エントリが参照（スルファジアジン20+ピリメタミン1 mg/kg
  = FDA承認ReBalance、ACVIMコンセンサス Reed 2016）。トキソ/ネオスポラ/鳥アトキソプラズマ。
  葉酸拮抗骨髄抑制の監視・妊娠馬回避を明記
- **キニジン硫酸塩** — 馬AFの古典的第一選択（22 mg/kg NGT q2h、QRS 25%延長で中止、
  Reef 2014）。ジゴキシン濃度倍化の相互作用。8馬疾患エントリが参照
- **バラシクロビル** — 馬EHV-1/EHM（27 mg/kg q8h負荷→18 mg/kg q12h、Maxwell 2017）。
  **猫は致死的（絶対禁忌）** — 劇症肝腎壊死（Nasisse 1997）、猫はファムシクロビル
- **メクリジン** — 前庭疾患の悪心（11種の疾患エントリが参照、Carpenter用量）
- **コルヒチン** — シャーペイ熱/腎アミロイドーシス・肝線維症・鳥/爬虫類痛風補助
- **リュープロレリン（ルプロンデポ）** — 鳥慢性産卵 700-800 μg/kg IM、フェレット副腎
  100-250 μg/kg IM（Wagner 2005）。7種が参照
- **ナイアシンアミド** — テトラサイクリン/ドキシ併用で犬DLE/天疱瘡/SLO（White 1992）
- **デクスラゾキサン** — ドキソルビシン血管外漏出解毒（10倍量IV 6時間以内+24/48h、
  Venable 2012）・心保護。ドキソルビシン entry が参照するのに未収載だった
- **メトトレキサート** — 相互作用後方参照10件（ペニシリン/サルファ/PPI/L-アスパラギナーゼ/
  レフルノミド）の解決。免疫介在性疾患 2.5 mg/m² 週2-3回
- **チアミン（B1）** — 猫欠乏症（頸部腹側屈曲）、冷凍魚チアミナーゼ（爬虫類は魚1kgあたり
  30 mg補給）、馬ワラビ中毒。22疾患エントリが参照
- **L-カルニチン** — 犬DCM 50-100 mg/kg q8-12h、猫肝リピドーシス補助
- **パロモマイシン** — クリプトスポリジウム症17種が参照。**猫は障害腸粘膜からの全身吸収で
  急性腎不全・難聴の報告（Gookin 1999）→ safe:False+機序明記**
- **EMLAクリーム** — ウサギ/モルモット麻酔プロトコルが参照（カテーテル留置前 30-60分密封）。
  **猫プリロカイン・メトヘモグロビン血症の警告**
- **50%ブドウ糖** — フェレット・インスリノーマ緊急プロトコル＋19種の低血糖治療が参照。
  **末梢静脈は1:2〜1:4希釈必須（静脈炎/組織壊死）**・インスリノーマの反跳性低血糖警告
- 回帰テスト+6件（14剤の存在・完全用量、猫致死フラグ3剤、馬AFプロトコル・EPMレジメンの
  エビデンス値、希釈/メトヘモグロビン警告）

### UX: チャット候補カードのクリック導線（クリックで使いやすい位置に着地）
- **バグ**: チャット3コンテナ（自由入力 `chatMessages`・ランディング `landingChatMessages`・
  問診 `guidedMessages`）に委譲クリックハンドラが無く、候補カード内の関連薬品リンク
  （renderMentionedDrugs の点線下線 `.drug-nav-link`）が素の `#drugs` ハッシュジャンプに
  フォールスルー → 薬品タブの先頭に着地するだけで目的の薬品が開かなかった
- **修正**: `_attachChatNavHandlers()` を新設し3コンテナに1回だけ委譲登録
  （innerHTMLリセットでも維持）。薬品リンクは `navigateToDrug`（完全一致着地+自動展開）へ
- **新機能**: 自由入力チャット・問診モード最終結果の候補カードに
  「🔍 疾患DBで詳細を開く」ボタンを追加。`openDiseaseAcrossSpecies(name, species)` 経由で
  **チャットの動物種とDBのロード済み種が違っても正しく種切替→完全一致着地→自動展開→
  読みやすいスクロール位置**（チェッカー結果カードと同等の導線をチャットにも）
  - 種はカード自身の `data-species`（自由入力=chatSpecies、問診=guidedState.species）から取得
  - 問診の中間結果カードには付けない（症状選択の途中で離脱を誘発しないため）
- CSS: `.chat-disease-nav`/`.chat-disease-open`（点線下線・min-height 32px タップ領域）
- 回帰テスト+1件（ハンドラ定義・3コンテナ登録・navigateToDrug/openDiseaseAcrossSpecies 経由・
  両レンダラーのボタン存在）

### 表示数値の同期
- `setDefaultStats()` フォールバック: 全21種の diseases/drugs を現行API実測値に同期
  （dog 593→600疾患/551→536薬品 等）、pendingStats 6520→6529疾患・571→595薬品

### テスト・CI
- フルテストスイート合格（+7新規回帰テスト）、ruff check/format 変更ファイル通過
- ServiceWorker: `CACHE_NAME` v106 → **v107**

### 薬用量ローカライザの文末ピリオドバグ修正（副産物）
- `drug_dosage_localizer.py` のトークン接尾辞剥がし正規表現が `.` を含まず、
  「... PO q24h.」のような文末ピリオド付き頻度略号が頻度辞書にマッチせず数値保持パスを
  通って **英語の頻度略号が日本語出力に漏れる** バグを検出（新規メクリジンentryの
  統合テストで発覚）。接尾辞クラスに `.` を追加（小数点はトークン内部のため影響なし）。
  回帰テスト+1件

## 2026-08セッション（第5弾: referenced-but-absent 薬品11剤の補完 + 関連チップ・ナビゲーションの委譲修正）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,763件合格**（34 skip、カバレッジ81.75%）
- 薬用量: safe薬品の dosage/dosage_ja 欠落 **0**（全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、プロトコル薬剤行の用量欠落 **0**、
  麻酔薬剤行→薬品辞書の未解決参照 **0**
- 注: 初回フルランの1失敗は並行 migrate_to_sqlite 実行との自前レースが原因（DB安定後の再実行で全合格）

### 薬用量マニュアル: referenced-but-absent 11剤の補完（`drug_batch_34.py` 新規、595→606薬品）
疾患治療テキスト（カタカナ薬品トークンの頻度解析）と相互作用後方参照を突合する第2回監査で検出:
- **ビンブラスチン** — 治療テキスト408件が参照（肥満細胞腫標準治療: VBL+プレドニゾロン、Thamm 2006
  2 mg/m² 週1×4→隔週×4）のにビンクリスチンのみ収載だった。vesicant温罨法（ドキソルビシンの冷罨法と
  逆）・好中球3,000ゲート付き
- **乳酸リンゲル液**（710件）+ **ノルモソルR/プラズマライトA**（1,059件） — 輸液はDB中最多参照の
  介入なのに晶質液エントリがゼロだった（コロイドのみ収載）。犬ショック10-20 mL/kg滴定・
  猫5-10 mL/kg（容量過負荷注意）・小型哺乳類80-100 mL/kg/日加温SC・爬虫類POTZ等の種別流量
  （AAHA/AAFP 2013）。LRS=血液製剤と同一ライン禁止（Ca凝固）、ノルモソル=Ca非含有で血液適合・
  肝不全時選択（酢酸筋代謝）のクラス定義的安全事実を明記
- **L-テアニン**（Anxitane、犬2.5-5 mg/kg q12h・猫25 mg q12h）+ **α-カソゼピン**（Zylkene、
  15 mg/kg q24h、Beata 2007）— 行動疾患治療74件が参照
- **ポビドンヨード** — 創傷0.1-1%希釈（>1%は線維芽細胞毒性）、爬虫類甲羅腐敗1:10浸漬
- **葉酸** — EPMピリメタミン治療の葉酸モニタリング。**妊娠馬への経口葉酸は子馬先天奇形と関連
  （Toribio 1998）の警告を用量欄に明記**。MTX中毒はフォリン酸（葉酸無効）
- **DMSO** — 馬0.5-1 g/kg IV ≤10%希釈（超で溶血）・局所90%・ドキソルビシン漏出補助
- **ミネラルオイル** — 馬大結腸便秘2-4 L NGT（**チューブ留置確認必須・誤嚥=致死的脂質性肺炎**）、
  犬猫はフード混和のみ（直接シリンジ禁止）
- **ルゴール液** — セキセイ甲状腺腫: ストック（原液2 mL+水30 mL）1滴/飲水250 mL（Carpenter 6th、
  DB内治療テキストの記載と一致）
- **フルオレセイン** — 132件参照の最多眼科診断薬。デスメ膜瘤は中心不染・FHV-1樹枝状潰瘍・
  馬フルオレセイン陽性眼へのステロイド禁忌・ヘビspectacle不可を種別に記載
- 回帰テスト+5件（11剤の存在・完全バイリンガル用量、VBL vesicant/好中球ゲート、輸液の種別流量と
  血液製剤ライン警告、妊娠馬葉酸警告、ミネラルオイル誤嚥・DMSO溶血警告）

### UX: 関連チップ・ナビゲーションの委譲修正（キャッシュ再描画で死んでいたリンクを是正）
- **バグ1**: 「治療に関連する薬品」チップ（疾患詳細・チェッカー結果）と「この薬品を使う疾患」チップ
  （薬品詳細）は、2回目以降の展開でキャッシュから同期レンダリングされるが、このパスでは per-node
  リスナーが付与されず、**クリックが無効な `#diseases` ハッシュに落ちて何も起きなかった**
- **バグ2**: hydrate経由の「この薬品を使う疾患」チップは selectSpecies + navigateToDiseaseDb
  （350ms後に行選択）を直接呼び、**種切替の非同期ロードとレースして前種のリストの先頭行など
  誤った疾患に着地**しえた
- **修正**: `_attachDbItemHandlers`（diseaseDbList/drugList/anesthesiaList/emergencyList共通）と
  チェッカー結果エリアの委譲ハンドラに `.treatment-drug-chip`→`navigateToDrug`、
  `.drug-disease-chip`→`openDiseaseAcrossSpecies`（種リスト到着を待つ readiness poll + 完全一致着地 +
  読みやすいスクロール位置）を追加。二重発火する per-node リスナーは削除。フォールバック href を
  `#database`（実在ビュー）に修正
- 回帰テスト+1件（委譲ハンドラ存在・openDiseaseAcrossSpecies経由・per-node配線の不在・dead href不在）

### 表示数値の同期
- `setDefaultStats()` フォールバック: 種別薬品数を606薬品の実測値に同期（dog 536→546、cat 515→525、
  horse 340→345、bird系 218→223 等14種）、pendingStats drugs 595→606
- ServiceWorker: `CACHE_NAME` v107 → **v108**

### 治療テキスト→薬品マッチャーの精度・再現率修正（関連チップの品質、副産物）
- **再現率**: キーワード索引が完全名のみだったため、治療テキストの実際の表記
  （「乳酸リンゲル」= 液なし、「ノルモソルR」= スラッシュ代替名の片方、「フルオレセイン」=
  括弧サフィックス無し）が新輸液・診断薬エントリに一致しなかった → 索引を3段階
  （完全名 > 括弧除去ステム・スラッシュ分割・語尾「液」除去 > 先頭語）で構築し解決
- **精度（既存バグ）**: 複合名の先頭語が裸のまま索引されており、"sodium restriction"→ニトロプルシド、
  "critical care monitoring"→オックスボウ製品、"vitamin supplementation"→ビタミンK1 のような
  誤チップが全治療テキストで発生していた → 汎用英単語25語の先頭語ストップリストで遮断
  （完全複合名は引き続き一致）。製品参照の大文字 "Critical Care"（1,000+件）は
  ケースセンシティブ特例で維持
- 回帰テスト+1件（再現率5ケース・精度2ケース・完全名2ケース）

## 2026-08セッション（第4弾: ID衝突バグ修正 + 馬の有病率データ新設 + prevalence dead key 33→10 + 薬5剤追加）

### エラーチェック
- ruff: repo全体 clean、フルテストスイート **3,755件合格**（34 skip、カバレッジ81.74%）— 既存コードは健全
- 薬用量監査: safe薬品の dosage 欠落 **0**（581薬品）
- 麻酔監査: 全21種×全8カテゴリ完備・188プロトコル・薬剤行の用量欠落 **0**
- 疾患監査: 配信7,058疾患で treatment/prevention/prognosis **100%**

### 致命的バグ発見・修正: IDロック位置衝突で新規疾患が配信DBから消失
- **症状**: 種モジュール末尾に新規疾患を追加すると、migrate は「+1件」と報告するのに配信SQLiteに存在しない
- **根本原因**: 新規（未ロック）エントリの位置由来ID（例 `degu_0123`）が、IDロックサイドカー生成時にその位置にいた既存エントリのロック済みIDと衝突。`INSERT OR REPLACE` が後勝ちで一方の行を黙って消していた
- **修正**: `scripts/migrate_to_sqlite.py` に `_resolve_collision_free_ids()` を新設（species/dog両パスで使用）。明示ID・ロック済みIDを先に確保し、未ロックエントリは位置IDが取得済みなら決定論的に次の空き番号へバンプ。`api/species/id_locks.py` に `locked_id_for()`（ロック有無を区別する公開ヘルパー）を追加
- **運用**: 新規疾患追加後は `python3 -m scripts.quality.build_id_locks <species>` でロック再生成（append-only、衝突時は content-hash ID を発行 — 今回の3疾患は `degu_x0a3259ee` 等で凍結済み）。`instance/vetdict.db` は増分upsertのため、ID変更を伴う再構築時は削除してクリーンビルドすること（残留した旧位置ID行が重複カードになる）
- 回帰テスト: `tests/test_id_collision_free_migration.py`（4件 — ユニット2 + 全種衝突ゼロ検証 + 配信DB実在検証）。`tests/test_id_locks.py` の「ロックID＝現在位置ID」テストは前提が中間挿入で崩れるため「全エントリがロック済み かつ 配信ID割当がロックと一致」の検証に置換

### prevalence dead key の是正（基礎 33→10、地域補正 15→0）
- **リネーム（正規疾患名へ、有病率priorとチップ導線を活性化）**: chinchilla Dental Abscess→Tooth Root Abscess・Rectal Prolapse→Prolapsed Rectum、guinea_pig Skin Abscess→Subcutaneous Abscess・Pneumonia (Viral)→Adenovirus Pneumonia、bird Papillomatosis→Cloacal Papillomatosis・Renal Disease→Renal Failure (Acute / Chronic)、amphibian Renal Disease→Renal Failure、reptile Fungal Dermatitis→Dermal Mycosis (Non-CANV)、exotic_other Skin Infection→Dermatological Bacterial Infection・Heatstroke→Heat Stroke・Mite Infestation→(Tarantula)・Trauma / Fracture→Fracture (Limb)+Trauma / Wound Infection (Exotic)
- **削除（active正規キーとの重複・誤配置）**: chinchilla Fatty Liver Disease（=Hepatic Lipidosis）、degu Heatstroke（=Heat Stroke）、rabbit Diarrhea (Acute)（症状レベルキー）、exotic_other Gastrointestinal Parasites（=Intestinal Parasitism）+ 魚病4キー（Ich/Fin Rot/Swim Bladder/KHV — fish種が正規キーで担当）
- **追加**: fish 'Fin Rot (Bacterial/Fungal)': very_common（最頻出の観賞魚疾患なのにティア欠落だった）
- **地域補正の dead key 15件を全修正**（JP補正が inert だった）: 犬 Coccidioidomycosis (Valley Fever)/Leishmaniasis、猫 FIP Wet/Dry Form 分割・Feline Histoplasmosis・Cytauxzoon felis、ウサギ Pasteurellosis (Snuffles)・E. cuniculi・Gastrointestinal Stasis・RHD、魚 KHV/Ich 正規名。犬 Chagas Disease は該当疾患なしのため削除
- 残10件は当該種DBに疾患自体が無いもの（rare/uncommon中心）— cap テストを 40→15 に強化

### 新規疾患エントリ3件（common ティアの真の欠落、エビデンスベース・日英完備）
- **degu Elodontoma（エロドントーマ/歯牙腫瘍）**: デグー・プレーリードッグの代表的歯科腫瘤。気道閉塞の病態、頭部X線/CT診断、歯冠整形+鎮痛+抗菌薬の緩和管理（Jekl in Quesenberry & Carpenter 4th ed）
- **guinea_pig Intestinal Torsion（腸捻転）**: 甚急性外科救急。X線ダブルバブル、安定化→減圧→緊急開腹、絞扼中の運動促進薬禁忌を明記（Dudás-Györki 2011）
- **amphibian Parasitic Dermatitis（寄生虫性皮膚炎）**: Trichodina/Costia/Epistylis/Oodinium等。皮膚呼吸障害の病態、ウェットマウント診断、塩浴/メチレンブルー/プラジクアンテル（Wright & Whitaker; Mader 3rd ed）
- 配信DB: 7,058 → **7,061疾患**

### 馬の有病率データ新設（69キー — 唯一 prevalence が無い種だった）
- 馬は基礎 prevalence ゼロ → 「よくみられる疾患」チップが空・チャット有病率priorが不動作（開発者自身の専門種なのに）
- Reed & Bayly 4th ed / NAHMS 2015 / Sykes 2015 EGUS consensus / Wylie 2011 / McIlwraith 2012 / McFarlane 2011 準拠で69キーをキュレート（全キーが equine DB 名に完全一致することを検証済み）
  - very_common: 疝痛・EGUS・OA・内部寄生虫・蹄膿瘍・蹄叉腐爛
  - common: 蹄葉炎・馬喘息・サルコイド・メラノーマ・ERU・PPID・EMS・屈腱炎・ナビキュラー・タイイングアップ・腺疫・インフルエンザ・EHV・チョーク・子宮内膜炎・胎盤停滞 等33
  - JP補正: Getah Virus/日本脳炎/Babesiosis=common、EPM/West Nile=rare（オポッサム・WNV不在）
- `/api/species/horse/common-diseases`: 0 → **38チップ**（equine モジュールから name_ja 解決するフォールバックを `vetdict_api.py` に追加 — 疝痛・胃潰瘍・蹄膿瘍等が日本語表示）

### 薬品5剤追加（referenced-but-absent 監査、`drug_batch_33.py` 新規、581→586）
- **メトトレキサート**: 相互作用10回参照（NSAIDs/ペニシリン/サリチル酸が警告）なのに本体未収載。多剤リンパ腫プロトコル用量・ロイコボリンレスキュー・腎不全禁忌
- **キニジン硫酸塩**: 馬の心房細動の薬理学的第一選択が未収載だった。22 mg/kg NGT q2h・QRS 25%延長で中止・ジゴキシン倍増相互作用（Reed & Bayly; ACVIM consensus 2014）
- **ピリメタミン**: 馬EPMの主軸（+スルファジアジン 20 mg/kg、ReBalance NADA 141-240）。妊娠馬への葉酸補充警告（先天異常報告）。鳥トキソ/サルコシスティス用量
- **EMLAクリーム**: ウサギ麻酔プロトコルが名指しするのに未収載。耳介辺縁静脈の密封30-60分、猫プリロカインMetHb警告（Flecknell BSAVA）
- **ニコチン酸アミド**: テトラサイクリン/ドキシサイクリン併用の犬DLE標準療法（White 1992 JAVMA）。>10kg 500mg q8h
- 回帰テスト4件（batch33存在+用量、キニジンAFプロトコル、EPM併用+妊娠警告、EMLA MetHb警告）

### UX: クリック導線の強化
- **複合相互作用参照のリンク化**: "Ketoconazole/itraconazole"・"metoclopramide/cisapride/mosapride" 等の複合表記は全体では解決不能でデッドテキストだった → `_interactionDrugCell()` が「/」で分割し、辞書収載の各成分を個別リンク化（1タップで該当薬品へ移動・自動展開）。CSS `.interaction-drug-part` 追加
- **EMLA→薬品辞書リンク**: `ANES_AGENTS` に EMLA を追加（麻酔プロトコル本文から新設エントリへ1タップ）
- 回帰テスト: `test_app_js_compound_interaction_refs_are_linkified`

### 表示数値の同期・キャッシュ
- `setDefaultStats()` フォールバック21種を `/api/species-stats` 実測値に全同期、pendingStats: diseases 6520→6532・drugs 571→586
- `build_disease_search_index.py` 再生成（6,532エントリ）
- ServiceWorker: `CACHE_NAME` v106 → **v107**

### テスト・CI（セッション終了時）
- フルテストスイート: **3,768件合格**（34 skip、+13新規回帰テスト）、カバレッジ81.72%
- ruff check/format: repo全体 clean
- 配信DB: クリーンビルドで **7,061疾患**・586薬品、treatment/prevention/prognosis 100%

## 2026-08セッション（第6弾: 薬用量ローカライザのフレーズ拡張 + 馬の頭字語重複カード統合 + 緊急薬リンク化）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,785件合格**（34 skip、カバレッジ81.77%）
- 薬用量: safe薬品の dosage 欠落 **0**（606薬品）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose/route/name_ja/notes_ja 欠落 **0**、全種 references あり
- 疾患: 配信7,061疾患で treatment/prevention/prognosis/causes/description/pathophysiology/clinical_signs 空欄 **0**

### 薬用量ローカライザのフレーズ拡張（JA UIの英語露出 659→510件、-149）
- `drug_dosage_localizer.py` に**管理語彙フレーズ層**を追加（プレースホルダ保護方式）:
  - フレーズ置換（"repeat in 14 days"→「14日後に再投与」等）を先に適用し、置換結果を私用領域文字で保護。
    残りトークンには従来どおり fail-closed 語彙判定を適用するため、**未知語が1語でもあれば全体 None**（安全性不変）
  - 期間（for/over N min/days/weeks、× N days）、点眼（N drops→N滴、眼軟膏リボン）、吸入
    （nebulized/via spacer/with mask）、食事（per meal/with food/in food/empty stomach）、
    希釈（in N ml saline/in N L water）、頻度（qN days/once daily）、単回投与/N回注射 等 60+ フレーズ
  - 固定フレーズ追加: "Not recommended due to toxicity"→「毒性のため非推奨」等5種
  - 単語追加: solution/ointment/shampoo/monthly/weekly/empirical 等15語、"+"を保持トークンに
  - 末尾コロン剥がし（"PO:"/"nebulized:" がラベル用法で頻度・経路辞書にマッチしなかった）
  - 区切り記号前の余分な空白除去（"用量未確立 ;"→"用量未確立;"）
- **英日併記文字列の分割**: "Not established in this species 本種では確立されていない"（20件）を
  dosage=EN / dosage_ja=JA に分割（完全一致のみ、`_BILINGUAL_EXACT`）。英語UIの日本語露出も同時解消
- モジュールロード時の自動補完: 614→**763件**。回帰テスト+11件（フレーズ変換10 + fail-closed更新1）
- 残510件は自由文（"titrate to effect"等）で設計通り未変換。全変換結果に経路/頻度略号の残存0を全数検証

### 馬の頭字語重複カード統合（HYPP/DDSP/PSSM/EOTRH、737→617... 実測621→617）
- **バグ**: 馬モジュールに裸の頭字語エントリ（"HYPP"）と正式名エントリ（"Hyperkalemic Periodic
  Paralysis (HYPP)"）が併存し、疾患ブラウザに**同一疾患が2枚のカード**で表示されていた（4組8枚）。
  さらに ms_hypp 側は「HYPPの原因は感染性（脳炎・髄膜炎）・腫瘍性…」という**臨床的に誤った**
  汎用テンプレート病因を保持（HYPPはSCN4A変異による純遺伝性チャネロパチー）
- `dedupe_disease_list`（helpers.py）に**頭字語ブリッジ**を追加: 裸の頭字語名エントリは、その頭字語を
  括弧サフィックスに持つ正式名エントリが**種内に一意**に存在する場合のみ統合。曖昧な頭字語
  （"(DM)"=糖尿病/変性性脊髄症）は決して統合しない。統合時は**正式名側が常に残る**
  （正式名がカードの正準タイトルであり、JSON overlay・prevalence のキーでもあるため。
  richness はモジュール段階では信頼できない — 誤テンプレートで水増しされた裸エントリが勝っていた）
- `migrate_to_sqlite.py` の `migrate_equine()` に dedupe を追加（equine パスだけ未適用だった）
- 検証: 配信DB 7,061→**7,057疾患**（馬621→617）、horse prevalence の dead key 0、正式名側の
  キュレート内容（SCN4A等）が全4組で残存。回帰テスト+5件（ブリッジ/曖昧头字語/配信DB検証）

### Cyrillic homoglyph 汚染の修正
- 馬HYPPの causes_ja/description_ja で Quarter Horse 種牡馬 "Impressive" が "Imprессive"
  （キリル文字 е/с 混入）と綴られていた（検索・コピペ破壊）→ JSON 2箇所修正
- 回帰テスト: 全疾患フィールドに キリル文字 0 を検証（`test_no_cyrillic_homoglyphs_in_disease_json`）

### 小文字種名プレースホルダの日本語化（"hamsterにおける" 等 68+291件）
- `fix_english_species_in_ja.py` の EN_TO_JA に**小文字・snake_case 種ID**（hamster/guinea_pig/
  amphibian等21種）+ 欠落していた **Fish/fish** を追加
- JSON 68トークン + 種モジュール .py **291トークン**（exotic_other 202含む）を日本語化。
  モジュールパッチは**particle パターンのみ**適用（paren パターンは英語フィールドの "(fish)" を
  誤変換するため除外 — レビューで発見し回避。配信DBスイープはJAフィールド限定なので従来どおり両方適用）
- "Amazon parrotに" 等の品種・固有名は lookbehind 保護で不変。回帰テスト: 検証種リストを
  小文字snake_case+Fishに拡張（JSON+配信DBの両テストが自動カバー）

### UX: 麻酔緊急薬のワンタップ導線（デッドテキスト40行の解消）
- **エピネフリン（20行）・ドキサプラム（17行）・ドブタミン・50%デキストロース・メロキシカム**が
  `ANES_AGENTS` に無く、麻酔タブの**緊急（RECOVER CPR）カテゴリ**で素のテキストのまま —
  用量に最速でたどり着きたい最高スティクスの場所でリンク切れだった
- 5剤を追加（全て薬品辞書に収載済み、`navigateToDrug` の完全一致着地で正しい行に展開）。
  裸の「アドレナリン」はエイリアスにしない（カタカナ部分一致が「ノルアドレナリン」の尾部に誤マッチ）
- 未リンク残: Triple Drip (GKX) 1行のみ（混合物のため設計通り）
- 回帰テスト+2件: 緊急5剤の存在・解決、**全プロトコル薬剤行のリンク可能性**（新規プロトコル追加時に
  辞書エントリ/エイリアス欠落があればCIで検出）

### 表示数値の同期・キャッシュ
- `setDefaultStats()`: horse 598→594、pendingStats diseases 6532→6528（重複統合を反映）
- `build_disease_search_index.py` 再生成（6,528エントリ）
- ServiceWorker: `CACHE_NAME` v109 → **v110**

## 2026-08セッション（第7弾: referenced-but-absent 薬品15剤 + 表記ゆれエイリアス機構 + 麻酔注意事項のクリック導線）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,803件合格**（34 skip、カバレッジ81.82%）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose/name_ja 欠落 **0**、全種 references あり
- 疾患: 配信7,057疾患で主要臨床フィールド（治療/病因/予後/予防/病態/説明）の空欄 **0**
- prevalence dead key: **10**（当該種DBに疾患自体が無い既知の残、上限15のガード内）
- 薬用量: safe薬品の dosage 欠落 0（dosage_ja 未変換分は自由文の設計通り fail-closed）

### 薬用量マニュアル: referenced-but-absent 15剤の補完（`drug_batch_35.py` 新規、606→621薬品）
カタカナ/英語トークン頻度解析（治療テキスト）+ 解毒薬相互参照監査の第3回スイープで検出:
- **プラリドキシム（2-PAM）** — 有機リン中毒の標準解毒薬なのに未収載（**184参照**で最多）。20 mg/kg IM/緩徐IV q8-12h＋アトロピン併用、エージング前の早期投与、カーバメート相対禁忌
- **レギュラーインスリン** — DKA CRI 0.05-0.1 U/kg/h・高K血症シフト 0.25-0.5 U/kg IV+ブドウ糖（16参照: 尿道閉塞・AKI・アジソンクリーゼ）。輸液チューブ吸着・低K血症未補正時の開始禁止を明記。馬高脂血症（McKenzie 2011）
- **トリアムシノロンアセトニド** — 馬関節内 6-18 mg/関節（31参照）、EMS/PPID/蹄葉炎既往馬の注意
- **イミドカルブ** — 大型バベシア 6.6 mg/kg IM×2・馬ピロプラズマ（T. equi 4 mg/kg q72h×4、**ロバ致死感受性**）・H. canis。アトロピン前処置。B. gibsoni 効果不良（アトバコン+アジスロ推奨）を明記
- **サクシマー（DMSA）** — 鳥鉛/亜鉛中毒の経口キレート 25-35 mg/kg q12h（Denver 2000、**80 mg/kg超で死亡**の安全域警告）。CaEDTA・ペニシラミン・BALと合わせ重金属解毒薬セット完備
- **シドフォビル0.5%点眼** — FHV-1 q12h（Fontenelle 2008、イドクスウリジンq4-6hに対する利点）
- **アルベンダゾール** — E. cuniculi代替/ジアルジア。**猫 safe:False**（再生不良性貧血）、ウサギ骨髄抑制警告、フェンベンダゾール優先
- **エニルコナゾール（イマベロール）** — 犬馬の皮膚糸状菌0.2%リンス。**猫 safe:False**（グルーミング摂取毒性）
- **エスモロール** — 超短時間β1遮断 0.05-0.1 mg/kg IV→CRI 25-200 µg/kg/分（SVT診断・鳥メチルキサンチン中毒）
- **オセルタミビル** — フェレットインフルエンザ 5 mg/kg q12h。**犬 safe:False（パルボ使用は Savigny 2010 で利益なしと明記）**
- **フルルビプロフェン0.03%点眼**・**イドクスウリジン0.1%点眼** — ぶどう膜炎NSAID/FHV-1抗ウイルス
- **トリクラベンダゾール** — 肝蛭（未成熟虫にも有効な唯一の吸虫駆除薬）
- **ジメルカプロール（BAL）** — ヒ素解毒。**鉄・Cd・Se中毒禁忌（複合体がより毒性）**・BAL中の鉄剤禁止
- **セレコキシブ** — 鳥PDD/ABVの経験的COX-2阻害（Dahlhausen 2002、10-20 mg/kg q24h）。PDD/ABV等の既存参照も解決

### 表記ゆれエイリアス機構（`_KATAKANA_VARIANT_ALIASES` + `search_aliases` フィールド）
- 治療テキストの正当な表記ゆれが関連薬品チップの解決を静かに壊していた（デキサメサゾン64回・ニスタチン21回・シルバースルファジアジン55回等）→ `_build_drug_keyword_index` が中央レジストリ＋薬品エントリの `search_aliases` を tier-2 で索引
- 対応: デキサメサゾン→dexamethasone、ニスタチン→nystatin、シルバースルファジアジン→silver_sulfadiazine、スルファサラジン→sulfasalazine、フォメピゾール→fomepizole、チアマゾール（INN）→methimazole、プロカインペニシリン→penicillin_g。batch35 新薬にも短縮エイリアス付与（2-PAM/DMSA/イミドカルブ等）

### 疾患コンテンツの garbled 薬品名・タイポ修正（JSON+モジュール）
- **塩化セレストデロン**（実在しない薬品名、鳥脳炎/PDDの3件）→ セレコキシブ 10-20 mg/kg PO q24h（Dahlhausen 2002）
- **ジルクトヘキシジン**（両生類口内炎）→ クロルヘキシジン0.05%（低濃度・短時間限定の注記付き）
- タイポ修正: ファンベンダゾール→フェンベンダゾール、イミダカルブ→イミドカルブ、エナイルコナゾール→エニルコナゾール（JSON+cat_diseases.py）、フルビプロフェン→フルルビプロフェン、シスアプリド→シサプリド

### UX: 麻酔注意事項ボックスのクリック導線 + 表示バグ修正
- **バグ修正**: `anesthesiaContraRules` は麻酔タブを開いた時のみフェッチされていたため、チェッカー直行ユーザーには「🏥 この疾患の麻酔注意事項」ボックスが**一度も表示されなかった** → `ensureAnesthesiaContraRules()`（fetch-once）を新設し `doAnalyze()` で解析と並行フェッチ
- **薬品名リンク化**: `/api/anesthesia/contraindications?all=true` が各ルールに `drug_links`（drug_patterns→薬品辞書解決、複合名 Tiletamine/Zolazepam (Telazol/Zoletil) の base/括弧/スラッシュ分割対応）を付与。フロントは解決した薬品名のみ `.drug-nav-link` 化（クラス語 nsaid・製造中止 halothane は素のテキスト維持 — 誤着地防止）。30ルール中29がリンク付き
- **麻酔タブへのジャンプ**: ボックス末尾に「💉 この動物種の麻酔プロトコルを見る」（species連動）。チェッカー結果の委譲ハンドラに `.anesthesia-nav-link` ルーティング追加（従来はDBリストのみ）

### 回帰テスト（+12件）
- batch35 15剤の存在・完全バイリンガル用量、2-PAM/アトロピン対とカーバメート禁忌、レギュラーインスリンのDKA/高K血症プロトコル、イミドカルブのロバ警告、重金属解毒薬セット完備、種別安全ゲート（猫アルベンダゾール/エニルコナゾール・犬オセルタミビル）
- 表記ゆれ17ケースの text-matcher 解決、garbled薬品名の再発防止（JSON走査）
- drug_links API（複合名解決・クラス語非リンク）、フロントの considerations リンク化＋fetch-once 配線

### テスト・CI
- フルテストスイート: 全件合格（+12新規）、ruff check/format clean
- 配信DB: 7,057疾患・**621薬品**、treatment/prevention/prognosis 100%
- `setDefaultStats()` 種別薬品数を実測同期（dog 546→558, cat 525→537, horse 345→353, 鳥系 223→232 等）、pendingStats drugs 606→621
- ServiceWorker: `CACHE_NAME` v110 → **v111**

## 2026-08セッション（第8弾: 臨床相談チャットの診断精度修正 — 有病率補正の欠落是正）

### 背景: UIが提案する入力例自体が正しくヒットしなかった
臨床相談（自由入力チャット）の「タップで入力」例とプレースホルダ例を全て実測検証した結果:
- **犬 嘔吐 食欲不振** → 1位が肥満細胞腫（急性胃腸炎エントリがレガシーDBに存在しなかった）
- **犬 多飲多尿 体重減少** → 1位が家族性腎症（稀な若齢遺伝病）で糖尿病・CKDを上回る
- **ウサギ 食べない お腹が張っている** → 「お腹が張っている」が未抽出（エイリアスは「お腹が張ってる」のみ）、
  消化管うっ滞が21位で子宮外妊娠（症例報告レベルの稀少疾患）が1位

### 根因と修正
1. **犬チャットパスに有病率補正が無かった**: レガシー62疾患DB（health_checker.DISEASES）の
   チャットスコアラー（match_symptoms_to_diseases）は coverage 有利な「症状リストが短い稀少疾患」を
   そのまま上位に出していた。チェックボックス側スコアラーは prevalence_tier フィールドを参照する
   設計だったが、**62エントリ中0件しか tier を持っていなかった**（全て common=1.08 のフラット扱い）
   → 全62（+新規1）エントリに evidence-based の prevalence_tier を付与（SPECIES_PREVALENCE との
   name join 44件 + Ettinger 8th 準拠キュレート19件: 家族性腎症/ARVC/CEA/パグ脳炎等=rare）。
   チャットスコアラーには汎用種パスと同一の _PREVALENCE_MULTIPLIER（1.35/1.125/0.875/0.70）を適用
2. **急性胃腸炎エントリ新設**: GP最多のGI主訴なのにレガシーDBに存在せず。
   acute_gastroenteritis（食餌性・非特異性、very_common、Ettinger 8th）を追加（62→63疾患）
3. **エイリアス追加**: 「お腹が張っている」「腹が張っている」「おなかが張っている/張ってる」→ bloating
4. **ウサギ消化管うっ滞の症状セット**: bloating/abdominal_distension を追加（ガス貯留・腹部膨満は
   GI stasis の hallmark — Oglesbee, Quesenberry & Carpenter 4th）。修正前は「食欲不振+腹部膨満」で
   21位だった
5. **ウサギ有病率**: Gastric Dilation (Bloat)=common、Intestinal Obstruction=common、
   Peritonitis=uncommon、Ectopic Pregnancy=rare を追加（全て配信DB実在名、dead-key 0維持）
6. **similarity_score の1.0キャップ**（disease_matcher）: 乗算ブーストで1.068になり
   フロントの match_percent が107%表示になりうるバグを修正

### 修正後の実測（全例で臨床的に正しい順位）
| 入力 | Before 1位 | After 上位 |
|---|---|---|
| 犬 嘔吐 食欲不振 | 肥満細胞腫 | **急性胃腸炎** > MCT > IBD > 膵炎 |
| 犬 多飲多尿 体重減少 | 家族性腎症 | **糖尿病 > CKD** > 家族性腎症 |
| 犬 嘔吐 下痢 血便 | — | パルボ / 急性胃腸炎 / IBD |
| ウサギ 食べない お腹が張っている | 子宮外妊娠(抽出1症状のみ) | **消化管うっ滞** > 胃拡張 > 腸閉塞 |
| 猫 くしゃみ 鼻水 目やに | (元々正しい) | 猫URI > FHV-1 > クラミジア ✓ |
| 猫 血尿 頻尿 | (元々正しい) | UTI / FIC / FLUTD ✓ |
| 3歳猫 嘔吐 食欲廃絶 黄疸 | (元々正しい) | 肝リピドーシス > 胆管炎 ✓ |

### 回帰テスト（tests/test_diagnostic_chat.py TestChatClinicalAccuracyAudit、+5件）
- 全レガシー犬疾患が有効な prevalence_tier を持つこと
- PU/PD+体重減少で糖尿病>家族性腎症、嘔吐+食欲不振で急性胃腸炎1位
- ウサギ・タップ例の抽出（distension必須）と消化管うっ滞1位・子宮外妊娠top5圏外
- 汎用マッチャーの similarity_score ≤ 1.0
- tests/test_health_checker.py の件数アサーション 62→63 更新

### 静的コピーの数値同期（同セッション第1コミット）
- ヒーローカウンターはAPI駆動で正しい（本番の薬品606表示は旧コードのデプロイ待ち→自動的に621へ）
- 静的コピー8箇所の「590+薬品」→「600+薬品」（メタ/OGP/Schema.org/料金/使い方ガイド）、
  「3,000+自動テスト」→「3,800+」。ServiceWorker CACHE_NAME v111→**v112**

## 2026-08セッション（第9弾: 薬品マッチャーの大規模リコール修正 + チャットのクイック入力全数検証 + エノキサパリン補完）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,820件合格**（34 skip、カバレッジ81.87%）
- 疾患: 配信7,057疾患で treatment/prevention/prognosis **100%**
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**

### 薬品テキストマッチャーのリコール修正（973参照が新たにチップ化）
katakana トークン頻度監査で「収載済みなのに treatment テキストの表記から解決できない」薬品を大量検出。
不足していたのは薬品ではなく **インデックスの正規化ルール** だった:
- **JA剤形・塩サフィックス剥がし**（`_strip_ja_form_suffixes`）: 点眼/配合点眼/注射/吸入/軟膏等の剤形、
  酢酸塩/塩酸塩/硫酸塩/リン酸塩/アルファ の塩・接尾辞、末尾の濃度数値(5%等)を反復剥離して tier-2 索引
  - オフロキサシン点眼→オフロキサシン(100参照)、キニジン硫酸塩→キニジン、リュープロレリン酢酸塩→リュープロレリン、
    ダルベポエチンアルファ→ダルベポエチン、シスプラチン注射→シスプラチン、ナタマイシン点眼5%→ナタマイシン
- **・区切り配合剤の分割**: トリメトプリム・スルファメトキサゾール→両半、イミペネム・シラスタチン、
  ピペラシリン・タゾバクタム（既存の／分割と同格の tier-2）
- **バリアントエイリアス追加**: ペニシリン→penicillin_g（**732参照** — モルモット禁忌注記等）、
  カルニチン→l_carnitine、アルブテロール→salbutamol、リュープロリド→leuprolide、
  ダーベポエチン→darbepoetin、ビタミンB1→thiamine_b1（B12誤マッピング防止）
- **精度ガード**: `_GENERIC_STEM_STOPLIST` に ジョイント/アンチオキシダント（ECVN製品名断片が一般文からスポンサーチップ化するのを防止）、
  ビタミンb（B1テキスト→B12誤チップ防止）を追加
- 効果: **973 treatment 参照**が新たに関連薬品チップとして解決（ペニシリン698+オフロキサシン100+ビタミンB1 48+...）

### referenced-but-absent 薬品の補完（`drug_batch_36.py` 新規、621→622薬品）
- **エノキサパリン（クレキサン）** — DIC・血栓塞栓症の13疾患エントリが用量付きで参照するのに未収載だった
  唯一のLMWH欠落。犬 0.8 mg/kg SC q6h（Lunsford 2009: ヒトの1日1回では犬に不足）、
  猫 1.25 mg/kg SC q6h（Alwood 2007 抗Xa準拠、長期ATE予防はクロピドグレル第一選択を明記）、
  馬 40-80 抗Xa IU/kg SC q24h（Feige 2003）、ウサギ/フェレット/鳥。DIC低凝固期禁忌・プロタミン部分中和(~60%)を明記

### チャットのクイック入力（タップボタン）全数検証 — 6フレーズが完全不動作だった
UI自身が提案する per-species クイック症状ボタン（JA 9種54フレーズ + EN 3種18フレーズ）を全数
エンドツーエンド検証。**6フレーズで症状抽出ゼロ**（タップしても何も起きない）を検出・修正:
| フレーズ | 原因 | 修正 |
|---|---|---|
| 犬「足を引きずる」/ "limping" | エイリアス→lameness_or_limping が legacy 犬語彙(limping)にも checkbox 語彙(limping_fl等)にも解決不能 | `_LEGACY_FALLBACK` に lameness_or_limping→limping、ID_SYNONYMS に per-leg フォールバック追加 |
| 犬 "itchy skin" | エイリアス→scratching(魚語彙)が legacy 犬語彙に解決不能 | `_LEGACY_FALLBACK` に scratching/flashing→itching |
| ハリネズミ「目が出ている」 | 「目が出てる」(pop_eye)はあるが「〜ている」形が欠落 | エイリアス追加→eye_bulging |
| 鳥「羽を膨らませている」 | 「〜てる」形のみ収載 | エイリアス追加→fluffed_feathers |
| 猫 "can't urinate" | "unable to urinate"のみ収載 | can't/cant urinate→straining_to_urinate |
| ウサギ "small feces" | JA「糞が小さい」のみ収載 | small feces/droppings/poops→small_fecal_pellets |
- **犬跛行のクロス肢展開**: チャット入力は肢を特定しないため、`_SYN` の limping_fl/fr/rl/rr が相互参照するよう拡張
  （肘関節形成不全=前肢のみ、CCL/股関節形成不全=後肢のみの疾患も等しくマッチ）。
  修正後: 足を引きずる→膝蓋骨脱臼/肘関節形成不全/前十字靭帯断裂/骨肉腫が上位

### ウサギ診断精度: 「糞が小さい」の順位反転を修正
- 「糞が小さい 食べない」（GI stasis の教科書的最早期症状）で**稀な先天性巨大結腸症が1位**、消化管うっ滞4位だった
- 根因1: ウサギGI stasis の症状セットに `small_fecal_pellets` が欠落（最古典的な owner-reported 徴候なのに。
  Oglesbee, Quesenberry & Carpenter 4th ed）→ GI stasis と毛球症（stasis の一表現型）に追加
- 根因2: Megacolon の有病率ティア uncommon → **rare** に修正（En/En スポット遺伝型限定の先天症候群で実臨床では真に稀）
- 修正後: 毛球症(0.702)>消化管うっ滞(0.672)>巨大結腸症(0.563) — stasis スペクトラムが上位2位を占有

### UX: 相互作用参照のベース名解決（+28参照がリンク化）
- `_resolveInteractionDrug`（app.js）が完全一致のみで、"Insulin"(17参照)・"Vitamin K1"・"Heparin"・
  "N-acetylcysteine (oral)" 等が dead text だった
- 両側の括弧サフィックスを剥がしたベース名同士の**等価比較**を追加（fuzzy にはしない — クラス語は素のテキスト維持）

### 回帰テスト（+7件）
- `test_ja_form_suffix_and_combination_stems_resolve_in_text_matcher` — 15解決ケース + 3精度ガード
- `test_enoxaparin_present_with_anti_xa_based_dosing` — 用量・バイリンガル・DIC禁忌・テキスト解決
- `TestQuickTapPhraseExtraction` — 全72クイックタップフレーズの抽出保証（JA54+EN18、経路別ルーティングをミラー）
  + 犬跛行の整形外科上位 + ウサギ小糞粒の stasis スペクトラム上位
- ServiceWorker: `CACHE_NAME` v112 → **v113**、`setDefaultStats()`/pendingStats を622薬品に同期

## 2026-08セッション（第10弾: 鑑別診断+チャット精度 第2弾 — 種横断36症例スイープと4エンジン修正）

### 背景: 現実的な主訴36例の体系スイープ（7種）で13例が臨床的に誤った上位
第8弾（UI入力例7件）に続き、犬15・猫8・ウサギ4・小型哺乳類4・鳥2・爬虫類1・馬2の
現実的な主訴でスイープ。当初 13/36 MISS → 全修正後 **36/36 合格**。

### エンジン修正（4系統）
1. **馬エンジン（equine_diseases.generate_differential_diagnosis）**: 有病率prior無し・純カバレッジ型で、
   「疝痛サイン」をチェックしても疝痛が**67位3%**・子宮捻転が1位だった
   - 有病率prior追加（horse 69キー、_EQ_PREVALENCE_MULTIPLIER 1.35/1.125/0.875/0.70）
   - **症候群フロア**（_SYNDROME_FINDING_FLOORS）: 症候群を定義する所見そのもの
     （dig_colic_signs→Colic、hoof_laminitis_signs→Laminitis等5種）チェック時に base 0.62×prior を保証
   - **症候群ペアブースト**（_SYNDROME_PAIR_BOOSTS）: 前肢跛行+蹄熱感（またはデジタルパルス）→蹄葉炎×1.5
     （Adams & Stashak 7th ed。所見2個のDDF腱炎がカバレッジ1.0で88%と過信勝ちしていた）
   - 疝痛サイン単独→疝痛84%1位、蹄熱+跛行+起立嫌悪→急性蹄葉炎92%1位に
2. **馬チャットの旧Jaccardマッチャーを廃止**: _match_equine_symptoms_to_diseases が
   チェックボックスエンジンへ委譲（チャットと鑑別診断が同一ランキングに）。
   低情報キャップ（1症状35%/2症状55%）は維持
3. **汎用マッチャーのシノニム二重カウント修正（disease_matcher）**: 同一主訴のシノニム展開が
   recall の分子・分母両方に複数計上され、同義語を3表記併記した疾患（ウサギ巨大結腸症）が
   本命（消化管うっ滞）に勝っていた → ソース症状単位のグループで recall を1回だけ計上
4. **汎用マッチャーにパトグノモニック・ペア（_PATHOGNOMONIC_PAIRS）**: 教科書的
   「X until proven otherwise」ペアのみ最小限（rabbit 食欲不振+糞減少→GI stasis×1.45、
   cat 排尿障害+啼鳴→尿道閉塞×1.35・後肢麻痺+冷感/啼鳴→ATE×1.35、
   ferret 後肢虚弱+流涎/凝視→インスリノーマ×1.35）

### レガシー犬DB（health_checker）
- **外耳炎エントリ新設**（very_common、コッカー2.5×等）— 犬で最多レベルの主訴なのに
  疾患も耳の症状語彙も存在しなかった。耳症状4種（ear_scratching/head_shaking/
  ear_discharge/ear_odor）+ unproductive_retching を語彙に追加（52→57症状、63→64疾患）
- GDVに unproductive_retching 追加 + パトグノモニック・クラスタ
  {bloating, unproductive_retching}→GDV×1.8（Ettinger: 膨満+空嘔吐=GDVの定義的ペア）

### エイリアス・シノニム・症状セット
- エイリアス追加: 後ろ足が突然動かない/後肢が動かない→hind_limb_paralysis、痛がって鳴く/鳴く→
  vocalization_changes、吐きたそうで吐けない等4種→unproductive_retching、頭を振る→head_shaking、
  食べるのに痩せる→weight_loss、後ろ足のふらつき→hind_leg_weakness、ぼーっと→staring、
  お腹が膨れて（前方形）→bloating、羽を膨らませて（前方形）→fluffed_feathers、甲羅がやわらかい→soft_bones
- **おしっこが出ない/尿が出ない**: straining_to_urinate→**decreased_urination** に是正（無尿の直訳）
  + _SYN に decreased_urination↔straining_to_urinate ブリッジ（飼い主は区別できない）
- _SYN: lumps に subcutaneous_mass/lumps_and_bumps を追加（猫「しこり」が稀な肉腫ばかり
  上位だったのを脂肪腫/皮膚型MCT等の日常ddxに）
- EQUINE_SYMPTOM_ALIASES: 前掻き/転がる/寝転がる/お腹を蹴る/pawing/rolling→dig_colic_signs、
  立ちたがらない→gen_recumbent
- 症状セット: リクガメMBD 2エントリに bone_weakness、馬蹄葉炎に limb_lameness_fore、
  急性蹄葉炎に gen_recumbent（いずれも教科書的所見）

### 有病率追加（全キー配信DB実在名を検証済み）
- horse: 疝痛サブタイプ（腎脾間膜変位/腸重積/有茎脂肪腫=uncommon、子宮捻転/胎水過多=rare）、
  深趾屈腱炎=uncommon、Black Walnut Toxicity=rare
- 鳥3種（bird/parakeet/parrot）: 銅中毒/PTFE中毒=rare（曝露歴依存）、ヘモプロテウス=uncommon
- cat: FISS=uncommon、非注射部位肉腫/メラノーマ/コレカルシフェロール殺鼠剤=rare、心因性多飲=uncommon

### 回帰テスト（TestChatClinicalAccuracyAuditRound2、+11件）
外耳炎/GDV空嘔吐/馬疝痛1位/蹄葉炎ペア/馬チャット委譲/シノニム二重カウント/
ブロック猫+ATEペア/フェレット・インスリノーマ/リクガメMBD/鳥中毒デモート/猫しこり日常ddx

### テスト・CI
- 36症例スイープ 36/36、フルテストスイート合格（症状数52→57・疾患数63→64のアサーション更新）
- pendingStats symptoms 52→57、ServiceWorker CACHE_NAME v112→**v113**

### 第9弾フォローアップ（フルスイートで発覚した2件の回帰を是正）
- **similarity_score 1.0キャップのソート前適用**で上位スコア差が潰れ、猫FHV-1が
  URI傘下エントリと同点タイ（挿入順）になっていた → 表示は1.0キャップ・
  **ソートは非キャップ値**（_rank_score、返却前にpop）に分離
- **チンチラ「Fur Mites=very_common」の事実誤り**を発見（チンチラは密被毛で
  外部寄生虫は稀 — Quesenberry & Carpenter 4th ed。ウサギCheyletiellaのtierの混入）
  → rare に是正 + Trichophyton mentagrophytes (Ringworm)=common 追加。
  皮膚糸状菌クエリでリングワーム群がtop3を回復
- フルテストスイート: **3,831件合格**（34 skip）、カバレッジ81.88%

## 2026-08セッション（第10弾: 薬品辞書の商品名検索対応 — 「バイトリル」0件バグの修正）

### 背景: 利用者報告バグ — 商品名で検索すると0件
利用者スクリーンショットで「バイトリル」（エンロフロキサシンの商品名）検索が 0/621件。
根因は2段構え:
1. `drug_dictionary.py` のベースエントリ `enrofloxacin`（name_ja「エンロフロキサシン」のみ）が先に
   登録され、商品名入りの batch_19 エントリ「エンロフロキサシン（バイトリル）」は**重複IDとして
   スキップ**されるため、配信データに「バイトリル」が一切含まれなかった
2. フロント検索（renderDrugList）・API検索（search_drugs）とも name / name_ja のみ照合で、
   別名フィールドを見ない + かな・全角半角ゆれも非対応だった

### 商品名エイリアス登録簿（`api/drug_brand_names.py` 新規、約160薬品・280別名）
- 日本の獣医臨床で流通する商品名 → 薬品ID の中央登録簿 `BRAND_NAME_ALIASES`
  - 獣医用: バイトリル・ビクタス・マルボシル・ベラフロックス・クラバモックス・メタカム・
    ガリプラント・デラマックス・ドミトール・デクスドミトール・アンチセダン・セラクタール・
    パナクール・ドロンシット/ドロンタール・ネクスガード・シンパリカ・インターセプター・
    アイボメック/カルドメック・バイコックス・マーキス・デクトマックス・プロフェンダー・
    ピモベハート・アドレスタン・プラセンド・オプティミューン・ニューフロール・エクセネル 等
  - ヒト用で獣医転用が定着: メルカゾール・チラーヂン・プレドニン・デカドロン・ガスター・
    プリンペラン・ラシックス(既収載)・アルダクトン・ヘルベッサー・ワソラン・ジゴシン・
    フェノバール・エクセグラン/コンセーブ・リリカ・ガバペン・ケタラール・ドルミカム・
    セルシン/ホリゾン・キシロカイン・マーカイン・イソジン・ヒビテン/ノルバサン・ST合剤 等
- **一般語と衝突する商品名は設計上除外**（「プログラム」「ランダ」等 — 治療テキストスキャンで
  「リハビリプログラム」「ランダム化試験」に誤チップが付くため）。回帰テストでガード
- 適用は重複統合（_consolidate_duplicate_drugs）後・キーワード索引構築前に `search_aliases` へ
  マージ（name/name_ja に既に含まれる別名は自動スキップ）。これにより
  (a) 辞書検索、(b) 治療テキスト→関連薬品チップ（tier-2索引）の両方で商品名が解決される

### 検索の正規化（かな・全角半角ゆれ吸収、Python + JS 同一仕様）
- `_normalize_search_text`（drug_dictionary.py）/ `normalizeDrugSearchText`（app.js）:
  NFKC正規化 + 小文字化 + ひらがな→カタカナ変換
- 「ばいとりる」「ﾊﾞｲﾄﾘﾙ」「Ｂａｙｔｒｉｌ」いずれも「バイトリル」に一致
- `search_drugs()` は search_aliases + aliases（統合時の旧名）も照合、
  `_drug_list_payload` が search_aliases / aliases を配信（フロント検索が参照）

### 薬品辞書のアクセス性UX改善（app.js / main.css）
- **商品名ヒット表示**: 別名でヒットした結果カードに「商品名: バイトリル」タグ
  （`.drug-brand-hit`）を表示 — なぜその薬品が出たかを明示
- **0件時のフィルタ解除導線**: 検索語はヒットするのにカテゴリ/動物種フィルタで0件の場合、
  「フィルタを解除して N 件を表示」ボタンを提示（スクリーンショットの
  「抗菌薬カテゴリ選択+検索で0件」のようなハマり状態から1タップで復帰）
- **0件時ヒント**: 一般名・商品名・英語名のどれでも検索できる旨を表示
- **プレースホルダ更新**: 「薬品名・商品名で検索... (例: バイトリル, メロキシカム)」（日英）
- ServiceWorker: `CACHE_NAME` v113 → **v114**（mainの第9弾も v113 を使用していたため、マージ時に改番）

### 回帰テスト（tests/test_drug_brand_search.py 新規、14件）
- バイトリル→enrofloxacin（利用者報告ケースの再現）、入力ゆれ3種の正規化
- 主要商品名15種の解決テーブル、カテゴリフィルタ併用
- 登録簿の完全性: 全キーが実在ID・別名の正規化後衝突ゼロ・一般語除外の維持
- APIペイロードの search_aliases 配信、キーワード索引到達
- フロント配線（正規化関数・別名照合・0件UX・商品名タグ・CSS）

## 2026-08セッション（第11弾: 診断チャット精度 第3弾 + referenced-but-absent 薬品3剤 + 疾患→チェッカー鑑別ピボット）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,851件合格**（34 skip）
- 配信SQLiteクリーンビルド: **7,057疾患**、主要臨床フィールド（治療/病因/予後/予防/説明）空欄 **0**
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり

### 臨床的に誤った薬品記述の修正（データ汚染2系統）
- **プラジコフロキサシン（実在しない薬品名）**: 猫マイコバクテリア症3エントリの多剤併用プロトコルが
  「プラジカンテルではなく プラジコフロキサシン」という二重に壊れた記述だった（プラジクアンテル=駆虫薬は
  マイコバクテリア症に無関係、プラジコフロキサシンは garbled）→ **プラドフロキサシン 3-5 mg/kg PO q24h
  （ISFM推奨フルオロキノロン、Gunn-Moore JFMS 2013）** に修正（JSON 3件 + cat_diseases.py）
- **サルバクタム（スルバクタムのタイポ）**: 犬パルボ2件・猫汎白血球減少症の敗血症予防
  「アンピシリン/サルバクタム」→「アンピシリン・スルバクタム」に修正（JSON 3件 + cat_diseases.py）
- 回帰テスト: JSON+モジュール走査で両 corruption の再発を検出（`test_no_garbled_pradofloxacin_or_sulbactam_typo_in_disease_json`）

### referenced-but-absent 薬品3剤の補完（`drug_batch_37.py` 新規、622→625薬品）
katakana トークン頻度監査（第5回スイープ）で検出:
- **タウリン** — **768参照**で最多欠落。猫タウリン欠乏性DCMの根本治療（250-500 mg/頭 PO q12h、
  Pion 1987 Science、3-6ヶ月で心筋機能可逆）、犬食事関連DCM（500-1000 mg q8-12h、Freeman 2018、
  コッカーはL-カルニチン併用 MUST試験）、フェレット・モルモット心筋症の補助
- **カルシトニン（サケ）** — ウサギ/鳥/インコのビタミンD中毒エントリが用量付きで参照（4-6 IU/kg SC）。
  犬猫コレカルシフェロール殺鼠剤中毒、**爬虫類NSHP 50 IU/kg IM 週1×2-3（正常Ca血症の確認が絶対条件 —
  低Ca血症のまま投与すると致死的テタニー、Mader 3rd ed）** を明記
- **アンピシリン・スルバクタム（ユナシン）** — パルボ/汎白血球減少症プロトコルが参照する敗血症の
  経験的静注第一選択（22-30 mg/kg IV q8h）。**ウサギ/モルモット/ハムスター/チンチラ safe:False
  （致死的腸性毒血症）**、経口ステップダウンはアモキシシリン・クラブラン酸への切替を明記
- search_aliases: スルバクタム/ユナシン等 → テキストマッチャーで治療文から解決可能

### 診断チャット精度 第3弾（24症例スイープ → 全実用症例合格）
**系統的バグ発見: 縮約形「〜てる」のみ登録され完全形「〜ている」を取りこぼし（125キー）**
- `symptom_aliases.py` にモジュールロード時の**双方向自動展開**を追加（てる⇄ている、でる⇄でいる、
  setdefault なので既存のキュレート済みマッピングは不変）
- これにより「首が傾いて目が揺れている」「目が白く濁っている」「膨らんでいる」等の完全形入力が全て解決

**誤マッピング修正（モルモット壊血病が抽出不能だった）**:
- `歯茎から出血` → blood_in_stool（誤り）→ **bleeding_gums** に修正
- `関節が腫れてる` → lameness_or_limping（誤り）→ **swollen_joints** に修正
- 修正後: 「関節が腫れて痛がる 歯茎から出血」→ 壊血病がrank 1

**レガシー犬DBに歯周病を新設（64→65疾患、57→58症状）**:
- 犬で最有病率の疾患（3歳以上の80-90%、AAHA 2019）なのに歯科エントリ・口臭語彙ともに欠落し、
  「口臭がひどい よだれ 食べにくそう」がてんかん/GDV上位だった → bad_breath 症状 + periodontal_disease
  （very_common、トイ種 breed_risks）を追加 → rank 1
- `_LEGACY_FALLBACK` 追加: foul_breath→bad_breath、cloudy_eye/cloudy_eyes→cloudiness_in_eyes
  （「目が白く濁っている」→ 白内障が top-4 に）

**新規エイリアス**: 首が傾いて/目が揺れて（前方形）、口の中に膿/口が閉じない→mouth_lesions
（爬虫類マウスロット: 感染性口内炎が top-5 に）、歯ぐき系4種
**ID_SYNONYMS**: constipation→straining 追加（鳥/爬虫類は「いきみ」を bare straining で保持 —
「卵が出ない お尻でいきんでいる」で卵詰まり（難産）rank 1。哺乳類は constipation 直接解決で不変）

### UX: 疾患詳細→症状チェッカーの鑑別ピボット（新規クリック導線）
- 疾患詳細パネルの症状リストに「🔍 この症状セットで鑑別チェック（似た疾患を探す）」ボタンを追加
- タップでその疾患の症状IDセットをチェッカーに事前選択→チェッカービューへ切替→**自動解析実行**→
  結果エリアへ自動スクロール（「この疾患と同じ症状を示す他の疾患は？」の逆引きが1タップ）
- 症状IDは現在ロード中の種のチェッカー語彙でフィルタ（解決不能セットはトースト警告で無害化）
- 委譲ハンドラ（`_attachDbItemHandlers`）でキャッシュ再描画後も動作、`.disease-detail.open` ガードより
  前に配置。CSS `.differential-check-btn`。GA4 `differential_from_disease` イベント
- ServiceWorker: `CACHE_NAME` v114 → **v115**

### 表示数値の同期
- `setDefaultStats()` 種別薬品数17種を実測同期（dog 559→562, cat 538→541 等）、
  pendingStats drugs 622→**625**・symptoms 57→**58**

### 回帰テスト（+12件）
- 薬品: batch37 3剤の存在・完全バイリンガル用量・爬虫類カルシトニン正常Ca前提・後腸発酵4種 safe:False・
  テキスト解決 / garbled 名の再発防止
- チャット: てる⇄ている双方向展開の網羅検証、ウサギ前庭・モルモット壊血病・犬白内障・犬歯周病・
  爬虫類マウスロット・鳥卵詰まりの抽出+ランキング、哺乳類 constipation 非影響
- UX: 鑑別ピボットの配線（ビルダー・ランナー・委譲ルーティング・checker切替）

## 2026-08セッション（第12弾: referenced-but-absent 薬品3剤 + 痒み/多食/乾酪様の抽出是正 + チェッカー→問診モード動線）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,861件合格**（34 skip。初回ランの1失敗は並行 migrate_to_sqlite との既知のレース — 単独再実行で合格）
- 薬用量: safe薬品の dosage 欠落 **0**（625薬品時点。dosage_ja 未変換502件は自由文の設計通り fail-closed）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- 疾患: 配信7,057疾患で主要臨床フィールド（治療/病因/予後/予防/説明/病態）の空欄 **0**
- prevalence dead key: **10**（当該種DBに疾患自体が無い uncommon/rare の既知残。上限15ガード内）

### referenced-but-absent 薬品3剤の補完（`drug_batch_38.py` 新規、625→628薬品）
katakana トークン頻度監査（第6回スイープ、実マッチャー突合）で検出:
- **パンクレリパーゼ（パンクレアチン/膵酵素製剤）** — 犬猫EPIフラグシップが「粉末状膵酵素 1 tsp/10kg/食」と
  用量指示するのにPERT製剤が未収載だった。犬（German 2012: 事前インキュベーション不要、高用量で歯肉出血）、
  猫（Steiner 2010: コバラミン欠乏ほぼ必発 → B12 250 μg SC 週1併用、三臓器炎評価）。
  エイリアス「膵酵素補充」は治療文を解決し、診断所見「膵酵素上昇」は誤チップしないことを検証
- **ベンズブロマロン（ウリノーム）** — 鳥/爬虫類痛風プロトコルが 5 mg/kg PO q24h で参照（Poffers & Lumeij 2002
  ハトで尿酸降下実証、アカオノスリのアロプリノール毒性の代替）。水和必須・ヒト肝毒性による一部販売中止を明記。
  bird→インコ/オウム、reptile→トカゲ/ヘビ/リクガメへ自動外挿
- **メトホルミン（メトグルコ）** — 馬EMS/インスリン抵抗性/慢性蹄葉炎が 15-30 mg/kg で参照（Durham 2008 EVJ、
  経口BA約4-7%→給餌30-60分前投与）。**犬は safe:False**（インスリン依存性DMに適応なし）、
  猫は歴史的位置づけ（SGLT2/インスリン優先）、腎不全での乳酸アシドーシス警告

### 表記ゆれエイリアス9薬品（`_KATAKANA_VARIANT_ALIASES`、約550参照がチップ化）
- フルニキシン(198 bare refs)→flunixin、アセチルシステイン(131)→n_acetylcysteine、デキストロース(81)→dextrose_50、
  リファンピシン(39, INN)→rifampin、インターフェロンオメガ/ω(44)→interferon_omega、アンホテリシンB→amphotericin_b、
  サルファジメトキシン→sulfadimethoxine、ピリメサミン→pyrimethamine、α-カソゼピン(ハイフン形)→alpha_casozepine

### 診断チャット精度 第4弾（4系統の抽出・語彙バグ）
1. **痒み系エイリアスの誤マッピング是正**: 痒い/痒がる/かゆがる/体を掻く/掻いてる → excessive_licking（舐め行動）
   だったのを **itching に直接解決**（itching↔excessive_licking は _ID_SYNONYMS で双方向ブリッジ済み）。
   前方形「痒がって」追加で「痒がっている」も抽出。_LEGACY_FALLBACK に skin_lesions→skin_rashes 追加。
   修正後: 犬「皮膚が赤くて痒がっている 毛が抜ける」→ 毛包虫症/膿皮症/アトピーが top-3
   （舐め行動の表現「しきりに舐める」は excessive_licking を維持）
2. **多食（polyphagia）の口語表現が全欠落**: 「食欲はすごくある/食欲旺盛/食欲が増えた/たくさん食べる/よく食べる」
   → increased_appetite を追加。**レガシー犬DBに increased_appetite 語彙自体が無かった**（58→59症状)ため追加し、
   糖尿病（loss_of_appetite=DKA徴候を除去し多食に置換 — 非複雑性DMの古典像）・クッシング・EPIの症状セットに付与。
   修正後: 猫「水をよく飲む 痩せてきた 食欲はすごくある」→ 糖尿病+甲状腺機能亢進症が top-2（三徴の完全抽出）
3. **乾酪様（チーズ状）口腔滲出物**: 爬虫類マウスロットの教科書的所見なのに未収載 → 「口の中に/口の周りにチーズ状」等
   → mucus_in_mouth（爬虫類系語彙のみ保有 → 他種は抽出段階で安全に脱落）。
   修正後: ヘビ「口の周りにチーズ状のもの 口が閉じない」→ 感染性口内炎（マウスロット）rank 1（82%）
4. **耳の痒み**: 「耳が痒い/耳をかく」→ ear_scratching に統一し、_ID_SYNONYMS に ear_scratching↔scratching_ears
   ブリッジ追加（猫等の語彙は scratching_ears 表記）。修正後: 猫/犬/ウサギの耳の主訴で外耳炎・耳ダニが rank 1-2

### UX: チェッカー低信頼度バナー→問診モードのワンタップ動線
- 低信頼度警告（症状≤2個 or 最高信頼度<50%）は「症状を追加すると精度が向上」と案内するだけだった →
  バナー内に「🩺 問診モードで症状を段階的に確認する」ボタンを追加。タップで chat ビューへ切替→
  **問診モード自動起動（種はチェッカーの currentSpecies を継承）**→チャットパネルへスクロール。
  構造化された段階的問診はバナーが推奨する対処そのもの（鑑別チェッカー⇄相談チャットの双方向動線が完成）
- 委譲ハンドラでルーティング（`.guided-consult-link`）、GA4 `guided_consult_from_checker` イベント
- CSS `.guided-consult-link`（アンバー系、min-height 32px タップ領域）

### 回帰テスト（+10件）
- 薬品: batch38 3剤の存在・完全バイリンガル用量・犬メトホルミン safe:False・膵酵素上昇の誤チップ防止・
  鳥爬虫類外挿、表記ゆれ9薬品×10ケースのテキスト解決
- チャット: 痒み→itching（舐めは licking 維持）、多食口語4表現、猫内分泌三徴 top-2、レガシー犬DB多食語彙、
  ヘビ乾酪様→口内炎 rank1、非爬虫類での安全脱落、耳主訴の外耳炎/耳ダニランキング（猫/犬/ウサギ）
- UX: 低信頼度バナー→問診モードピボットの配線検証

### 表示数値の同期・キャッシュ
- `setDefaultStats()` 種別 diseases/drugs を `/api/species-stats` 実測に同期（dog 564薬品, cat 543, horse 356,
  鳥系 235, degu 158 等15種）、pendingStats drugs 625→**628**・symptoms 58→**59**
- ServiceWorker: `CACHE_NAME` v115 → **v116**

## 2026-08セッション（第13弾: レガシー犬DBの最頻疾患4件補完 + 薬品3剤 + B1/B12誤チップ修正 + 薬品→麻酔動線）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,872件合格**（34 skip）
- 薬用量: safe薬品の dosage 欠落 **0**（628薬品時点）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**
- 疾患: 配信7,057疾患で主要臨床フィールド（治療/病因/予後/予防/説明/病態）の空欄 **0**

### referenced-but-absent 薬品3剤の補完（`drug_batch_39.py` 新規、628→631薬品）
片仮名トークン頻度監査（第7回）+ 拮抗薬相互参照監査で検出:
- **プロタミン硫酸塩** — 辞書収載のヘパリン/エノキサパリン/ダルテパリン各entryが拮抗薬として名指しするのに
  本体未収載（プラリドキシム・デクスラゾキサンと同型の自己参照ギャップ）。残存ヘパリン100 IUあたり1 mg
  緩徐静注・時間減衰減量・LMWHは約60%部分中和のみ・急速静注のアナフィラキシー様反応警告（Plumb's 10th）
- **ヒドロコルチゾンコハク酸エステル（ソル・コーテフ）** — アジソンクリーゼの標準（0.5 mg/kg/h CRI、
  Lathan 2018）が未収載。ミネラルコルチコイド作用を持つ点でデキサメタゾンと使い分け、
  ACTH刺激試験前採血の必須注記、敗血症CIRCI生理量。フェレット両側副腎摘出後も記載
- **高張食塩水 7.2-7.5%** — ショック/GDV/頭部外傷が参照する少量蘇生輸液（犬4-7 mL/kg・猫2-4・馬2-4+疝痛
  搬送前安定化、Silverstein & Hopper 3rd）。脱水・高Na血症禁忌、迷走神経反射の速度上限を明記。
  batch 34 の LRS/ノルモソルと合わせ輸液セット完備

### 薬品マッチャー修正
- **表記ゆれエイリアス6件**: ドーパミン(19refs)→dopamine、重炭酸ナトリウム→sodium_bicarbonate、
  フィトナジオン→vitamin_k1、カルシウムグルコネート→calcium_gluconate、ウルソジオール→ursodiol、
  炭酸カルシウム(13refs)→calcium_supplement_reptile（「粉末」サフィックスでstem索引が届かなかった）
- **数字境界ガード（精度バグ修正）**: ビタミンB1エイリアスが「ビタミンB12」に部分一致し、全B12言及に
  チアミンの誤チップが付いていた → 数字で終わるキーワードは直後が数字でないことを検証（B1単独は解決維持）

### 診断チャット精度 第5弾（新規スイープ25症例 → 全合格）
**レガシー犬DBに最頻レベルの疾患4件が欠落**（チャットで該当主訴が全て誤ランキング）:
- **肛門嚢疾患**（very_common、O'Neill 2021 VetCompass 年間4.4%）— スクーティング語彙自体が無く
  「おしりを地面にこすりつける」が**抽出ゼロ**だった。scooting症状+エイリアス9種を新設 → rank 1
- **角膜潰瘍**（very_common、短頭種2.5-11×）— 「目が赤い 目を細めてまぶしそう」が眼瞼疾患ばかり上位。
  て形「目を細めて」「まぶしそう」エイリアス追加 → top-3
- **変形性関節症**（very_common、犬整形最多）— 「立ち上がりにくい」エイリアス+difficulty_standing→stiffness
  ブリッジ、後ろ足がふらつく→hind_leg_weakness→limpingブリッジ（従来は「ふらつく」→ataxia→tremorsに
  誤フォールバック）→ top-3
- **認知機能不全症候群**（common、8歳以上の14.2% Salvin 2010）— DISHA徴候で構成。
  ぼーっと→staring→disorientation、夜鳴き→vocalization_changes→anxiety ブリッジ → rank 1
- レガシーDB: 65→**69疾患**、59→**60症状**
**猫**: 甲状腺機能亢進症に vocalization_changes を追加（夜間の大声はAAFP/Carney 2016記載の徴候）。
「夜中に大声で鳴く 高齢 痩せてきた」→ 甲状腺機能亢進症 rank 1（従来は尿道栓子が1位）。
夜鳴きエイリアスを anxiety→vocalization_changes に是正
**鳥**: 「そのうが膨らんでいる」エイリアス5種→crop_distension 新設。「吐き戻し+そのう膨満」で
嗉嚢停滞・素嚢結石等のクロップ疾患がtop独占（従来は消化管異物が1位）

### UX: 薬品詳細→麻酔プロトコルの逆リンク（双方向動線の完成）
- 麻酔→薬品辞書リンク（ANES_AGENTS linkify）は既存だが**逆方向が dead end** だった
- 薬品詳細に「💉 この薬品を使う麻酔プロトコルを見る」ボタンを追加（`_anesQueryForDrug` が
  ANES_AGENTS 46剤と名前照合、略語エイリアスは誤マッチ防止のため不使用）
- タップで麻酔タブへ切替+検索欄に薬剤名を自動入力+フィルタ済みリストへスクロール
  （未ロード時もfetch完了時に検索値を反映）。GA4 `anesthesia_from_drug` イベント

### 回帰テスト（+11件）
- 薬品: batch39 3剤の存在・完全バイリンガル用量・定義的安全事実（プロタミン60%部分中和・
  ヒドロコルチゾンACTH採血先行・高張食塩水の脱水禁忌）、表記ゆれ6種の解決、B1/B12数字境界
- チャット: Round 5 クラス7件（スクーティング/CDS/角膜潰瘍/整形/猫夜鳴き/鳥クロップ/新規エントリ検証）
- UX: 薬品→麻酔リンクの配線検証（ヘルパー・テンプレート・委譲ハンドラ・検索プリフィル）

### 表示数値の同期・キャッシュ
- `setDefaultStats()` 種別薬品数5種を実測同期（dog 567, cat 546, horse 358, rabbit 270, ferret 204）、
  pendingStats drugs 628→**631**・symptoms 59→**60**
- ServiceWorker: `CACHE_NAME` v116 → **v117**

## 2026-08セッション（第14弾: 重複カード197件の大規模統合 + 治療テンプレートのオーバーレイ上書きバグ修正 + 薬品2剤 + チャット精度第6弾）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,883件合格**（34 skip）
- 疾患: 配信DBクリーンビルドで主要臨床フィールド（治療/病因/予後/予防/説明/病態）の空欄 **0**
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- 薬用量: safe薬品の dosage 欠落 **0**

### 疾患重複カードの大規模統合（197件 — dedupe第2弾）
第11弾の完全一致dedupeをすり抜けていた重複カード2クラスを、`dedupe_disease_list` の保守的な拡張で統合:
- **JA種タグサフィックス**: 「羽毛嚢胞」vs「羽毛嚢胞（鳥）」のような、name_ja が表示ノイズの種タグ
  （（鳥）（両生類）等21種+鳥類/小鳥）だけ違うペア。**臨床的修飾語（（重度）（ヘモクロマトーシス）等）は
  決して剥がさない**ため、意図的なサブタイプ（Bd/Bsal、鉄蓄積症の2型、熱中症重度型等）は温存
- **EN綴り/複数形フォールド**: Heatstroke/Heat Stroke・Tularaemia/Tularemia・Hypoglycaemia/Hypoglycemia・
  Mammary Tumors/Tumor 等（英米綴り ae→e, oe→e, our→or + 末尾語の複数形フォールド + 所有格 's）。
  **括弧内修飾語はフォールドに残す**ため (Wing)/(Leg)・(Bd)/(Bsal) は衝突しない
- 全197ペアを目視レビューして全て同一疾患であることを確認（Dermatophytosis≠Dermatophilosis のような
  別疾患ペアは修飾語差で自動的に除外されることを検証）
- **richness にテンプレート減点を追加**: 汎用ワークアップ雛形（「正確な臨床評価…から治療方針を決定」）を
  含むフィールドは非カウント。従来はボイラープレートの文字数がキュレート済みエントリに勝ってしまい、
  モルモット・イレウスの輸液/鎮痛プロトコルがテンプレートに置き換わるところだった
- 配信DB: 7,057 → **6,892疾患**（横断検索インデックス 6,528→6,431）
- **prevalence キー37件を存続エントリ名にリネーム**（有病率priorとチップ導線を維持、dead key は既知の10のみ）

### 治療テンプレートのオーバーレイ上書きバグ修正（256件復元）
- migrate の JSON オーバーレイは COALESCE で**キュレート済みモジュール治療文を汎用ワークアップ雛形で
  上書き**していた（低メモリ本番の実行時パス helpers.enrich_diseases は「空/テンプレートのみ置換」で正しく、
  SQLiteパスだけが劣化していた = 2つの配信パスで内容が食い違っていた）
- `migrate_json_enrichments` に `_guard_treatment` を追加: ワークアップ雛形は空/雛形行の充填のみ可、
  情報のある既存治療文は決して置換しない → **256件の治療文がキュレート内容に復元**
  （残る雛形499件は代替となるキュレート文が存在しないもの — 将来のキュレーション候補）

### 馬バックドシン（管骨骨膜炎）の重複統合 + 誤病因修正
- Bucked Shin / Bucked Shins の2枚カードをEN複数形フォールドで統合（テンプレート側が消え、
  キュレート治療文側 ms_bucked_shins が存続）
- **臨床的に誤った急性外傷テンプレート病因**（「落下・衝突・咬傷・交通事故」）を、
  疲労性障害の正しい病因に置換: 若齢競走馬の高速調教による第三中手骨背側皮質への反復性高ひずみ負荷、
  リモデリング遅延→骨膜反応、Nunamaker改良調教プログラム（EN pathophysiology のスタブも詳述化、
  saucer fracture への進行と再発予防を記載。Adams & Stashak 7th ed）

### referenced-but-absent 薬品2剤の補完（`drug_batch_40.py` 新規、631→633薬品）
- **エタンブトール** — 鳥/爬虫類/犬猫の抗酸菌症多剤プロトコル13エントリが参照するのに未収載。
  arabinosyl transferase 阻害機序、犬15/猫10-25/鳥20-30 mg/kg（Greene 4th・Gunn-Moore JFMS 2013・
  Carpenter 6th）、**単剤使用禁止**（耐性）・視神経炎・人獣共通(MTBC)の行政相談を明記
- **ジヒドロストレプトマイシン** — 犬ブルセラ症の古典的標準（ドキシサイクリン併用 10 mg/kg IM、
  Wanke 2004）が9エントリで参照するのに未収載。**アミノグリコシド中最強の前庭毒性**・
  入手不能時のゲンタマイシン代替・B. canis 完全除菌困難（避妊去勢+生涯モニタリング）を明記
- **garbled 薬品名修正**: 鳥結核プロトコルの「エチオブトール」（実在しない）→「エタンブトール」
  （JSON+bird/parrotモジュール+テンプレートライブラリの5箇所）
- 表記ゆれエイリアス: アティパメゾール（ティ形）→atipamezole、裸のミルベマイシン→milbemycin_oxime

### 診断チャット精度 第6弾（12症例スイープ → 全合格）
- **エイリアス誤マッピング修正**: 「口を痛がる」→excessive_drooling（流涎、誤り）→ **difficulty_eating** に是正
  → 猫の口腔痛主訴で歯周病/FCGS/歯肉炎がtop5独占。「足の裏が赤い/腫れている」→lameness（非特異）→
  **foot_sores**（足特異ID、ID_SYNONYMS で pododermatitis_signs/foot_lesions/bumblefoot→跛行の順に解決）
- **新規エイリアス**: 脱皮がうまくできない（できない形が欠落）→dysecdysis、吐きそうにする→
  unproductive_retching、止まり木から落ちる→falling_off_perch、毛が円形に抜ける/円形脱毛→
  circular_hair_loss、歩きたがらない→reluctance_to_move
- **ID_SYNONYMS 追加**: foot_sores/unproductive_retching(→retching/nausea/vomiting)/falling_off_perch
  (→inability_to_perch/ataxia)/reluctance_to_move/difficulty_eating の5系統
- **_SYN マッチングブリッジ**: pododermatitis_signs↔foot_lesions↔foot_swelling（ウサギのソアホック本体
  エントリは foot_lesions キーで、ブリッジ無しでは妊娠中毒症が1位だった）、circular_hair_loss↔
  fur_loss_patches、dry_skin→skin_scaling/scaling_skin（チンチラ白癬）
- 修正後: モルモット足底皮膚炎 rank1、ウサギ・ソアホック rank1 (1.0)、ヘビ・スペクタクル脱皮不全 top2、
  フェレット・ヘリコバクター胃炎 rank1、チンチラ白癬菌感染 top2、猫歯科疾患 top5独占

### UX: 問診モード最終結果→チェッカーのピボット（双方向動線の完成）
- チェッカー低信頼度バナー→問診モード（第12弾）の**逆方向が dead end** だった: 問診の最終結果から
  症状を微調整するには問診を最初からやり直すしかなかった
- 最終結果のアクション行に「🧪 チェッカーで症状を微調整して再解析」ボタンを追加。
  `runCheckerFromGuided()` が問診で確定した症状セットをチェッカーに事前選択→ビュー切替→自動解析。
  問診の種とロード済みの種が違う場合は selectSpecies + readiness poll で語彙ロードを待ってから適用
  （解決不能セットはトースト警告で無害化）。GA4 `checker_from_guided` イベント

### 回帰テスト（+15件）
- 薬品: batch40 2剤の存在・完全バイリンガル用量・定義的安全事実（単剤禁止/前庭毒性）・テキスト解決、
  エチオブトール再発防止（4ファイル走査）、表記ゆれ2種
- dedupe: JA種タグ統合・臨床修飾語の非統合・EN綴りフォールド・括弧修飾語の非衝突・
  テンプレートエントリがキュレート双子に勝てないこと・配信DBのバックドシン統合+正病因
- チャット: Round 6 クラス8件（猫口腔痛/モルモット・ウサギ足底/ヘビ脱皮/フェレット空吐き/
  鳥落下/チンチラ円形脱毛/歩きたがらない）
- UX: 問診→チェッカーピボットの配線検証

### 表示数値の同期・キャッシュ
- `setDefaultStats()` 全21種の diseases/drugs を実測同期（dog 618疾患/569薬品 等）、
  pendingStats diseases 6528→**6431**（API実測値）・drugs 631→**633**
- ServiceWorker: `CACHE_NAME` v117 → **v118**
- 再現手順: `migrate_to_sqlite.py`（dedupe/ガードは配信DBビルドに統合済み）→ `build_disease_search_index.py`

## 2026-08セッション（第15弾: リーシュマニア第一選択2剤+IVIG+IFN-α補完 + 15症例精度スイープ + 犬レガシーDBの頻出疾患2件補完）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,828件合格**（78 skip、カバレッジ81.96%）
- 薬用量: safe薬品の dosage 欠落 **0**（632薬品時点で全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**
- 疾患: 配信7,057疾患で treatment/prevention/prognosis **100%**
- prevalence dead key: 10（全て uncommon/rare tier で当該種DBに疾患自体が無い既知残、上限15ガード内）

### referenced-but-absent 薬品4剤の補完（`drug_batch_41.py` 新規、633→637薬品 — mainのbatch_39/40とのマージで2回改番）
用量文脈フィルタ付きカタカナ/英語トークン監査（第8回スイープ、実マッチャー突合）で検出。
マッチャー自体はほぼ健全（ノルモソル/乳酸リンゲル/グルコン酸カルシウム等は文脈スニペットで全て解決）で、真の欠落は4剤:
- **ミルテホシン（ミルテフォラン）** — 犬リーシュマニア症エントリが「2 mg/kg PO q24h（28日）」と用量指示する
  LeishVet第一選択2剤の一方なのに未収載。催奇形性・妊娠飼い主の手袋着用指導・アロプリノール併用必須
  （単剤=耐性リスク）を明記（Solano-Gallego 2011; Miró 2009 比較試験）
- **メグルミンアンチモン酸塩（グルカンチーム）** — 同エントリのもう一方の第一選択（75-100 mg/kg SC q24h×4-8週）。
  投与前腎機能評価必須・注射部位反応・IRIS≥2ではミルテホシン/アロプリノール単独優先を明記
- **ヒト免疫グロブリン（hIVIG）** — IMHA/ITP/重症皮膚薬物反応の難治例レスキューとして30-40参照で最多欠落。
  0.5-1.5 g/kg IV 6-12時間単回（Whelan 2009 RCT; Spurlock 2011）。**単回使用限定**（抗ヒト蛋白感作→再投与
  アナフィラキシー）・IMHA過凝固への血栓予防併用（クロピドグレル）・容量過負荷を明記
- **インターフェロンα（組換えヒト）** — 鳥PBFD/ポリオーマ（1-10万IU/kg SC）+ 猫レトロウイルス経口低用量
  （30 IU/頭 週交代サイクル）で33参照、ω型のみ収載だった。高用量非経口は3-7週で中和抗体形成・
  ネコIFN-ω優先（同種蛋白）を明記。エイリアスがinterferon_omega参照を奪わないことを検証済み

### 診断チャット精度 第5弾（15症例スイープ 9 MISS → 15/15 合格）
現実的な飼い主主訴15例（犬6・猫2・ウサギ1・ハムスター1・鳥2・トカゲ1・フェレット2）で系統検証:
1. **犬レガシーDBに肛門嚢疾患が完全欠落**: 犬の最頻出主訴の一つ（VetCompass 年間有病率4.4% — O'Neill 2021）
   なのに疾患もscooting語彙も無く「おしりを地面にこすりつける」が抽出ゼロだった → scooting症状（59→60）+
   anal_sac_disease エントリ（65→66疾患、common tier）を新設。既存エイリアス「お尻を引きずる」→scooting も活性化
2. **犬レガシーDBにCDS（認知機能不全症候群）が欠落**: 8歳以上の14-35%（Salvin 2010）なのに
   「夜鳴き・ぐるぐる回る・老犬」が小脳失調症/PSS上位だった → cognitive_dysfunction エントリ新設（66→67疾患、
   DISHA徴候・セレギリン/抗酸化食記載）→ rank 1
3. **MMVD tier 是正**: common→**very_common**（Keene 2019 ACVIM: 犬後天性心疾患の~75%、日本の小型犬
   人口構成）+ CHF徴候 labored_breathing を症状セットに追加。「散歩の途中で座り込む」→exercise_intolerance
   エイリアス追加で心疾患主訴が top-3 に
4. **毛引きエイリアスの誤マッピング是正**: 羽を抜いてる/毛引き/自分で羽を抜く→hair_loss（受動的脱羽）だったのを
   行動学的IDの **feather_plucking** に是正（ID_SYNONYMSでfeather_loss/self_mutilationへフォールバック維持）。
   自咬→self_mutilation に是正。「羽を抜いてしまう」形も抽出可能に
5. **テイルボビング**: 鳥の呼吸困難の教科書的所見なのにエイリアス皆無 → 尾が上下に動/テイルボビング等→tail_bobbing
6. **口の痛み**: 口を痛がる→excessive_drooling（よだれと二重計上）だったのを **pain** に是正 +「食べられない」→
   difficulty_eating 新設（ID_SYNONYMS: dysphagia/appetite_loss、犬レガシー: loss_of_appetite フォールバック）。
   猫FCGS（口を痛がって食べられない+よだれ+口臭）が top-3 に
7. **爬虫類MBDの四肢弯曲**: 「脚が曲がって」→limb_deformity エイリアス + ID_SYNONYMS limb_deformity→
   soft_bones/swollen_limbs ブリッジ新設（トカゲMBDがrank 1に）。「足が震え」→tremors も追加
8. **直腸脱の_SYNブリッジ**: 抽出ID rectal_prolapse がフェレット語彙に実在するため ID_SYNONYMS を通らず、
   疾患側の rectal_protrusion と永遠にマッチしなかった → _SYN に rectal_prolapse↔rectal_protrusion↔
   cloacal_prolapse + constipation↔straining_to_defecate を追加（フェレット直腸脱 rank 1）。
   お尻から赤いもの/肛門から何か出て/脱腸→rectal_prolapse エイリアス新設
9. **フェレット副腎**: 「陰部が腫れて」→vulvar_swelling（従来は「外陰部が腫れてる」のみで取りこぼし）+
   尻尾がハゲ→hair_loss → 副腎疾患群が top-3 に
- その他: 背中を丸めて→hunched_posture + _LEGACY_FALLBACK→reluctance_to_move（犬IVDD top-3）、
  左右対称に抜け/毛が薄くなって→hair_loss（クッシング）、座り込む→exercise_intolerance
- 回帰テスト: `TestChatClinicalAccuracyAuditRound5`（10件）+ 薬品4剤テスト3件

### チェックボックス/問診モード経路にも scooting を追加（犬 dog_diseases モジュール）
- 犬のチェックボックスUI・問診モードはレガシーDBではなく `dog_diseases` モジュール語彙（64症状）を使用しており、
  肛門周囲症状が皆無だった（肛門嚢疾患は constipation/pain_on_touch 経由でしか到達不能）
- VALID_SYMPTOMS/SYMPTOM_NAMES/SYMPTOM_CATEGORIES(digestive) に scooting を追加（64→65症状）、
  Anal Sac Disease / Perianal Fistula の症状セットに scooting を追加
- 検証: チェックボックス engine で scooting→肛門嚢疾患 rank1、問診モード digestive カテゴリに表示、
  配信SQLite再構築で dog 65症状に反映。回帰テスト `TestScootingVocabulary`（2件）
- これでチャット（レガシーDB）・チェックボックス・問診モードの3経路全てが同一主訴を扱える

### UX: クイック入力ボタンの拡充（新規対応フレーズを1タップ導線に）
- 犬「おしりを地面にこすりつける」・フェレット「陰部が腫れている」・鳥「自分で羽を抜く」を quick-tap に追加
  （全て本セッションで抽出保証済み、ミラーテスト `TestQuickTapPhraseExtraction` も同期更新）
- 新規薬品4剤は既存の治療チップ/相互作用リンク機構で自動的にワンタップ到達可能（マッチャー解決を検証済み）

### 表示数値の同期・キャッシュ
- `setDefaultStats()`: 全種をマージ後実測に同期（dog 570薬品・cat 550・馬358・鳥系236）、pendingStats drugs →**637**・symptoms →**60**
- ServiceWorker: `CACHE_NAME` → **v119**（並行セッションとv117/v118が衝突したため改番）

## 2026-08セッション（第16弾: 臨床フィードバック対応 — ホットスポット新設 + 亜鉛反応性皮膚症の是正 + excellent-matchティア）

### 背景（開発者・馬獣医師からの直接フィードバック）
「犬の亜鉛反応性皮膚炎もあるが、ただ暑がって皮膚炎にうつることもある」— 暑熱→掻破→湿潤性皮膚炎
（ホットスポット）という日常的な移行が鑑別に出ず、亜鉛反応性皮膚症との描き分けができなかった。

### 急性湿性皮膚炎（ホットスポット）の新設 — 犬の夏の代表的皮膚救急が全DBに未収載だった
- **犬モジュール（チェックボックス/問診用）**: フルキュレートエントリを新規追加（618→619疾患）。
  病態（高温多湿+密被毛+湿り+掻痒トリガー→自己外傷→表在性膿皮症、深在型=化膿性外傷性毛包炎の鑑別）、
  治療（クリッピング+クロルヘキシジン、短期プレドニゾロン0.5-1 mg/kg、全身抗菌薬は毛包炎型のみ
  セファレキシン3-4週）、Muller & Kirk 7th ed / Holm 2004 Vet Dermatol 準拠
- **レガシーチャットDB（自由入力用）**: hot_spots 症状IDは語彙に存在したのに疾患エントリが無かった
  → acute_moist_dermatitis（tier=common、ゴールデン2.5×等）+ zinc_responsive_dermatosis
  （tier=uncommon、ハスキー/マラミュート5.0×）を追加（69→71疾患）
- **prevalence**: SPECIES_PREVALENCE/dog + 犬チェッカー専用 _DISEASE_PREVALENCE（85→88キー）の両方に登録、
  JAPAN補正で very_common（梅雨〜盛夏の高温多湿）

### 亜鉛反応性皮膚症の内容是正
- 両エントリの clinical_signs が**皮膚科カテゴリ汎用テンプレート**（「分布パターンが診断に有用: 顔面・指趾
  （アトピー）…」）だった → 疾患特異的所見（**皮膚粘膜移行部の固着性痂皮・鱗屑、肉球過角化・亀裂**、
  I型=北方犬種の若齢成犬・発情/ストレス増悪、II型=急成長大型犬の子犬）に日英とも置換
  （White SD JAVMA 2001; Colombini Vet Clin North Am 1999）
- 症状セットに skin_lesions を追加（「鼻の周りにかさぶた」がこのエントリに届かなかった）

### チャット精度・クラスタ再編
- **クラスタ再編**: 旧 {itching, skin_rashes, hot_spots}→アレルギー性皮膚炎×1.8 はホットスポット疾患が
  無かった時代の代替設定で、病変診断より基礎疾患を上位にしていた → 食物アレルギーの特徴である
  **掻痒+消化器徴候** {itching, skin_rashes, vomiting/diarrhea}×1.6 に置換。
  {hot_spots, itching}→acute_moist_dermatitis×1.4 を新設（病変を直接描写する主訴は病変診断が第一）
- **チャットスコアラーのキャップ後ソートバグ修正**: composite を min(...,1.0) してからソートしていたため
  1.0超のブースト差が挿入順タイに潰れていた（第9弾で disease_matcher に入れたのと同型）→
  非キャップ値 _rank_score でソート、表示はキャップ維持
- **新規エイリアス**: 皮膚がジュクジュク/ホットスポット/急に皮膚がただれた→hot_spots、暑がる→
  excessive_panting、皮膚が赤く（連用形）、舐めている、発疹/湿疹/ブツブツ→skin_rashes
- **ID_SYNONYMS**: hot_spots→[skin_lesions, skin_rashes...]（他種フォールバック）、
  crusting→[crusty_skin, skin_lesions...]（「かさぶたがある」が犬で死んでいた）、skin_rashes→[skin_lesions...]

### excellent-match ティア（チェックボックス両実装共通）
- 同tier内で有病率優先の既存ソートにより、**ホットスポット96%（4症状一致）がノミアレルギー52%の下**に
  表示されていた → pct≥80 かつ 3症状以上一致は有病率シャッフルより上位の excellent tier に
  （2症状セットの稀少疾患の「100%」ジャンプは cnt≥3 条件で防止）。symptom_checker.py と helpers.py の両方

### 検証結果
| 入力 | Before | After |
|---|---|---|
| 暑がって皮膚が赤くジュクジュク 痒がって舐める（チャット） | アトピー1位/HS圏外 | **ホットスポット1位** |
| 皮膚がジュクジュクしていて痒がる | （抽出不能） | ホットスポット1位 |
| 痒み+発疹+嘔吐（食物アレルギー像） | — | アレルギー性皮膚炎1位（GIクラスタ発火）|
| チェッカー {itching,skin_redness,skin_lesions,pain_on_touch} | ノミアレルギー52%が1位 | **ホットスポット96%が1位** |
| 鼻周りかさぶた+フケ+脱毛 | 亜鉛は候補外 | 亜鉛反応性皮膚症 top3（ハスキー入力でさらに上昇）|
| 皮膚が赤くて痒い+脱毛（第12弾ガード） | 毛包虫/膿皮症top | 不変 ✓ |

### テスト・CI
- フルテストスイート合格（+6新規回帰テスト、レガシー疾患数 69→71 更新、ソート仕様テスト更新）
- ruff check/format clean、ServiceWorker v118→**v119**、dog id_locks 再生成（619ロック、+1新規）
- 検索インデックス 6,431→6,432
## 2026-08セッション（第17弾: 稀少疾患乗っ取り監査 — クローン症状セットのマッチングガード + 46セットのキュレート修正）

### 背景（開発者・獣医師からの指示）
「一般的な疾患が下手に難しい疾患に誘導されないか注意」— 全種の common/very_common 疾患887件について
「その疾患自身の教科書的症状セット」での自己検索監査（self-retrieval）と稀少疾患乗っ取り監査を実施。

### 発見1: supplementary のコピペ・クローン症状セット（1,191エントリ）
旧エンリッチメントが**1つの症状セットを無関係な疾患ブロックに一括スタンプ**していた:
- ウサギ47疾患（RHD・乳頭腫症・緑膿菌感染…）が {red_urine, sudden_death, normal_behavior…} を共有
- インコ43・鳥39・両生類27（脱皮不全に「沈めない」!）・ハムスター23 等、≥5共有グループが123
- 害は двое: (a) ありふれた主訴に無関係な稀少疾患が並ぶ（虚脱したデグーの鑑別に「爪過成長」）、
  (b) 本当の症状では見つからない（卵黄性腹膜炎が {anemia, feather_loss, lameness} でしか引けない）

### 対策1: クローンセット・マッチングガード（`unreliable_clone_set_names`、helpers.py）
- 同一種内で**≥5エントリが同一症状セットを共有**し、かつ **supplementary 由来**（enrich時に
  `_supplementary` タグ付与）のエントリを**マッチングからのみ除外**（1,095件。ブラウズ/検索/SEOは不変）
- **モジュールエントリは決して除外しない**: モジュール内の同一セットは正当な臨床ファミリー
  （犬の赤目トライアド12疾患・尿石症サブタイプ5種・猫胆管炎ファミリー等）
- **レビュー済みホワイトリスト32件**: 共有セットがその疾患の教科書的症状であるシード
  （ウサギE.cuniculi・便秘系・チンチラ歯科ペア・インコそ嚢ペア・鳥重金属ペア・爬虫類肺炎等）は除外しない

### 対策2: 46+3件の症状セットをキュレート修正（種語彙で全ID検証済み）
- **雌雄取り違え級の汚染**: チンチラ「妊娠中毒症」に雄の陰茎毛輪の症状
  （fur_ring_penis/paraphimosis/penile_swelling）→ ケトーシス系の正しい徴候に置換
- デグー3件（尾剥脱/耳感染症/爪過成長が全て虚脱セット共有）、鳥 気管ダニ（ワクモの症状が混入）、
  夜間パニック損傷、卵黄性腹膜炎（鳥/インコ/オウム）、インコ疥癬（クヌドコプテス）、
  ハムスター擬似冬眠/熱中症/低体温/臭腺系4件、ウサギ盲腸便秘（abnormal_cecotropes等の正確なID使用）/
  ハエウジ症/歯周病/腸毒血症/ボルデテラ（スナッフルのクローン化を回避し咳・頻呼吸系に）、
  リクガメ嘴/爪過長・蟯虫・口内炎、痛風（爬虫類/トカゲ、「rubber_jaw=MBDの症状」を関節腫脹系に）、
  スペクタクル残留（ヘビ/爬虫類）、両生類エロモナス（red_legs!）他
- ウサギ「脱水」は状態であり主診断でないため fecal 系徴候を外し GI stasis スペクトラムの上位独占を回復

### 発見2・対策3: 犬マダニ麻痺の是正
- 症状セットが**4×跛行+こわばり**（=整形外科的疼痛歩行）で、全ての後肢跛行主訴の top-3 に
  マダニ麻痺が出現していた → 上行性弛緩性麻痺の正しい表現 {reluctance_move, lethargy, collapse,
  difficulty_breathing} に置換（散文は元々正確: ホロシクロトキシン・除去後24-72h回復等）
- tier: common → **uncommon**、JAPAN補正 **rare**（豪Ixodes holocyclus/北米Dermacentorの現象）

### エイリアス追加
- 体が冷たい→cold_body、呼吸がゆっくり/遅い→slow_breathing、反応がない/薄い→unresponsiveness
  （ハムスター/ハリネズミの擬似冬眠主訴が抽出ゼロだった → 擬似冬眠 rank1 に）

### 検証結果
| 監査/入力 | Before | After |
|---|---|---|
| 自己検索監査（common系887件、top-3） | 26 miss + 蔓延するクローン汚染 | live miss 14（全て同等以上の頻度の正当な鑑別に負けたもの）|
| rare-tier 疾患による乗っ取り | 0件（確認） | 0件維持 |
| 犬「後ろ足を引きずる 触ると痛がる」 | マダニ麻痺 top-3 | 整形外科ddxのみ（パテラ/CCL/OA…）|
| デグー「ぐったり 呼吸が速い よだれ」 | 爪過成長・耳感染症が上位 | 熱中症等の妥当なddx |
| ハムスター「体が冷たい 呼吸がゆっくり 反応がない」 | 抽出ゼロ | 擬似冬眠 rank1 |
| 鳥「お腹が膨れて呼吸が苦しそう」 | 卵黄性腹膜炎 引けない | 卵黄性腹膜炎 rank1 |

### テスト・CI
- 新規回帰テスト `tests/test_clone_set_guard.py`（13件: ガード単体3+キュレートセット3+ランキング7）
- フルテストスイート全合格、ruff check/format clean
- 静的アセット変更なし（全てサーバーサイド）— ServiceWorker 据え置き

### 次セッション候補
- supplementary の <5共有グループ（266グループ）の漸進的キュレート
- モジュール側クローンファミリーの鑑別力向上（同一セット内は品種/年齢/発症様式でしか差が付かない）

## 2026-08セッション（第18弾: ECVNスポンサーブロックの控えめ化 + 製品別リンク導線）

### 背景（開発者からの直接フィードバック）
「スポンサーのサプリメントの項目 — 目立たせすぎず、他の検索時の邪魔にもなるので、
クリックしたらこちら（caninevet.jp）の各リンクに飛べるように」

### 変更内容
- **デフォルト折りたたみ化**: ECVN補助療法ブロックを `<details>`/`<summary>` に変更。
  閉時はコンパクトなPRラベル1行（「PR・自社製品（補助療法オプション）▸」）のみ表示され、
  治療プロトコルの読解・結果スキャンを妨げない。タップで展開
- **製品別ダイレクトリンク**: `PRODUCT_URLS`（api/data/sponsor_adjuncts.py、正準マップ）を新設し、
  ブロック本文の9製品名（For Joint / For Antioxidant / MSM+アミノコンプリート /
  NMNミトコンドリアアシスト / CPパウダー / Relax & CBD / Protain / Booster & Relax /
  カミデミルク）を各 caninevet.jp 製品ページへの `<a>` に変換（percent-encoded URL、
  `rel="sponsored noopener noreferrer"` — 有償リンクのGoogleガイドライン準拠）
- **両配信パスを同期**: SPA（app.js renderTreatmentWithAdjunct、ECVN_PRODUCT_URLS ミラー）+
  SEOページ（vetdict_api._render_treatment_adjunct_html、PRODUCT_URLS import）。
  マップの一致はテストで固定（app.js が全URLを含むことを検証）
- **検索汚染の確認**: 疾患ブラウザ検索は name/description のみ対象（treatment 非対象）で
  ECVN本文は検索にヒットしない、関連薬品チップのECVN断片は既存ストップリストで遮断済みを確認
- CSS: summary のカスタム開閉マーカー（▸/回転）、閉時の控えめな背景・パディング
- PRラベル・免責文言（「標準治療・エビデンスに基づく治療ではありません」）は維持

### テスト
- tests/test_ecvn_pr_label.py に +2件（details折りたたみ+製品リンク+レジストリ網羅、
  app.js のURLマップミラー検証）。既存のPRラベル/免責/マーカー非漏出テストは全て維持
- フルテストスイート 3,937件合格、ruff clean
- ServiceWorker: CACHE_NAME v120 → **v121**

## 2026-08セッション（第11弾: タブクリック→検索入力欄への直接着地）

### 背景: 利用者要望「クリックしたら直ぐ検索入力へ移動するように」
薬品タブはパネル先頭に「他の獣医薬リファレンスとの比較」「薬品相互作用チェッカー」の
アコーディオンがあり、タブタップ後の着地（scrollToAnchor(panel)＝パネル先頭）では
**検索入力欄が画面外に残り**、毎回スクロールが必要だった。フォーカス自体は既存の
`switchView(view,{focusSearch:true})` でタップ同期コンテキストで当たっていた
（モバイルでキーボードは開くが入力欄が見えない状態）。

### 修正（static/js/app.js）
- `_navLandingTarget(view)` ヘルパー新設: 検索主体のビュー
  （drugs/database/anesthesia/emergency）は検索入力欄の `.symptom-search` ラッパーを、
  checker は speciesSection を、その他はパネルを着地点として返す
- ナビの3経路すべてを helper 経由に統一:
  1. デスクトップ nav クリック（setupNavigation）
  2. モバイル下部 nav クリック（mobileBottomNav）
  3. ハンバーガーメニュー閉時のスクロール（switchView 内）
- 既存の `focusSearch:true`（タップ→キーボード起動）はそのまま活き、
  「タブをタップ → 検索欄が画面最上部に見えた状態でキーボードが開く」導線が完成
- 回帰テスト: `test_tab_click_lands_on_search_input`（3経路の helper 経由・focusSearch 維持）
- ServiceWorker: `CACHE_NAME` v121 → **v122**

## 2026-08セッション（第12弾: 全タブ・全項目クリックのスムーズな導線化 — スマホ対応）

### 背景: 利用者要望「他の薬品以外も各々の項目をクリックでスムーズに進むように、スマホでも」
第11弾で薬品/疾患DB/麻酔/救急タブは「タップ→検索入力欄へ直接着地」になったが、
監査の結果、以下の導線がまだパネル先頭着地 or 位置無変更のままだった。

### 修正（static/js/app.js）
- **相談（チャット）タブの着地**: `_navLandingTarget` に chat を追加 —
  モード切替（自由入力/問診）＋チャット欄が見える `.chat-mode-toggle` に着地
  （従来はパネル先頭＝カードヘッダで、チャットUIが下に残っていた）
- **ヒーロー統計カード（疾患数/薬品数/プロトコル数）・ヒーロー「疾患データベースを見る」ボタン**:
  パネル先頭ではなく `_navLandingTarget` 経由で検索入力欄へ着地（タブタップと同じ挙動に統一）
- **救急のカテゴリ/動物種フィルタ**: 変更時に `_revealFilteredList("emergencyList")` で
  絞り込み結果の先頭へ再アンカー（薬品/麻酔/疾患DBと同じパリティ）。
  検索入力のタイピングでは位置を動かさない（キーボード表示中のページ移動を避ける）
- 監査で確認済みの既存カバレッジ（変更不要）: 動物種カードタップ→症状選択へスクロール、
  解析→結果へスクロール、リスト行展開→読みやすい位置（全4リスト共通 toggleDbItem）、
  カテゴリカード/A-Zタップ→リスト再アンカー、in-pageアンカーの sticky-offset 補正、
  チャット/問診のメッセージ追記→最下部へ自動スクロール
- 回帰テスト: `test_all_entry_points_land_smoothly`（chat着地・helper 6箇所以上・
  救急フィルタ再アンカー・既存リスト再アンカーと行展開スクロールの維持）
- ServiceWorker: `CACHE_NAME` v122 → **v123**

## 2026-08セッション（第19弾: 馬PPID重複カード統合+誤治療是正 + 輸液/ビタミンD3補完 + チャット精度第8弾）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,937件合格**（34 skip）
- 配信SQLiteクリーンビルド: treatment/prevention/prognosis **100%**
- 薬用量: safe薬品の dosage 欠落 **0**（637薬品時点）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- prevalence dead key: **10**（当該種DBに疾患自体が無い既知残、上限15ガード内）

### 馬PPIDの重複カード統合 + 臨床的に危険な誤治療の是正（開発者専門種）
- **重複カード**: `mt_ppid`（下垂体中葉機能障害 (PPID)）と `mt_ppid2`（同(クッシング病)）が併存し
  疾患ブラウザに2枚表示。所見セットを mt_ppid に統合（hirsutism+多飲多尿+筋萎縮の8所見）、
  mt_ppid2 を削除（馬 621→620モジュール疾患）。prevalence キーも存続名にリネーム（prior維持）
- **臨床誤り是正（JSONオーバーレイ）**: 削除した重複行の予後は「トリロスタン・ミトタンで管理」
  （犬クッシング用 — 馬PPIDはペルゴリドが第一選択）、存続行の予後・予防は感染症テンプレート
  （「抗病原体療法」「ワクチネーションプログラム」）だった → ペルゴリド 2 μg/kg・65-85%改善
  （Ireland & McGowan 2018）・秋のACTH季節変動・EEG 2021年次スクリーニング・蹄葉炎管理を
  日英で正確に記述。病態生理はドパミン神経変性/POMC の具体的内容へ差し替え
- **hirsutism 症候群フロア**: 多毛・換毛不全はPPIDのpathognomonic（McFarlane 2011）なのに
  希少疾患がカバレッジで上回っていた → `_SYNDROME_FINDING_FLOORS` に body_hirsutism→PPID を追加。
  hirsutismエイリアス新設（毛が長く/換毛しない/毛が生え変わらない/巻き毛 等）
- 修正後: 「毛が長くて換毛しない 痩せてきた 水をよく飲む」→ PPID rank 1（70%）

### referenced-but-absent 薬品2剤の補完（`drug_batch_42.py` 新規、637→639薬品）
- **生理食塩水（0.9%塩化ナトリウム）** — **293参照**で最多欠落の輸液。高張7.2%のみ収載で等張液が
  無かった（高Ca血症の第一選択・血液製剤ライン・ネブライゼーション溶媒・低Cl性アルカローシス）。
  AAHA/AAFP 2013のショックボーラス（犬10-20 mL/kg・猫5-10）・希釈性高Cl性アシドーシス・
  慢性低Na血症の緩徐補正（≤0.5 mEq/L/h）・**7.2%高張液との混同厳禁**（severity: major）を明記
- **コレカルシフェロール（ビタミンD3）** — 96参照（上皮小体機能低下症 4,000-6,000 IU/kg・爬虫類NSHP
  200-400 IU/kg 週1）。活性型カルシトリオールのみ収載だった。作用発現遅延・数週間の組織半減期・
  殺鼠剤と同一分子の狭い治療域・爬虫類はUV-B/食餌是正が主治療である旨を明記
- **表記ゆれエイリアス**: 硫酸亜鉛/グルコン酸亜鉛→zinc_acetate（亜鉛反応性皮膚症の治療文が解決）、
  TMP-スルファ/TMP/S→trimethoprim_sulfa、リンゲル液（裸）→lactated_ringers

### 診断チャット精度 第8弾（22症例スイープ 10 MISS → 全実用症例合格）
- **レガシー犬DBに語彙3件+疾患1件を追加**（60→63症状、71→72疾患）:
  - `epistaxis`（鼻血）+ **鼻腔内腫瘍エントリ新設**（鼻出血の教科書的鑑別 — Withrow & MacEwen 6th。
    vWDにも epistaxis 追加で凝固障害鑑別も並ぶ）→「鼻血が出た 鼻がつまる くしゃみ」rank 1
  - `vision_loss`（物にぶつかる）を白内障/緑内障/PRA/網膜形成不全に付与 →「目が白く見える
    夜に物にぶつかる」で白内障 top-3
  - `voluminous_stool`（便の量が多い）をEPIに付与 →「食べているのに痩せる 便の量が多い 軟便」で
    EPI rank 1（従来はIBD/リンパ腫上位）
- **エイリアス新設**: スキップするように歩く/けんけん歩き→跛行（膝蓋骨脱臼 rank 1）、
  顔が腫れて/目の下から膿→facial_swelling/eye_discharge（猫歯根膿瘍 rank 1）、
  ジャンプしなくなった→reluctance_to_jump に是正（猫DJD top-3 — Lascelles 2010。
  従来の reluctance_to_move への誤マッピングを修正）、毛づくろいしすぎ→excessive_grooming
  （心因性脱毛症 rank 1）、鼻血/物にぶつかる/便の量が多い 等
- **ID_SYNONYMS**: epistaxis/voluminous_stool/reluctance_to_jump/excessive_grooming の4系統
  フォールバック、_LEGACY_FALLBACK に reluctance_to_jump/excessive_grooming/facial_swelling
- **ウサギ**: 歯ぎしり+食欲不振（糞変化前の stasis 古典像 — Oglesbee）の pathognomonic ペア追加
  → 消化管うっ滞 rank 1（従来は鼓脹症が1位）

### UX: 馬のクイック入力ボタン新設 + 新規対応主訴の1タップ導線
- **馬にクイック入力ボタンが1つも無かった** → 6ボタン新設（疝痛/前肢跛行/蹄熱感/PPID多毛/
  食欲不振/咳 — 全て抽出保証済み、ミラーテストに horse 分岐追加）
- 疝痛の連用形エイリアス（お腹を痛がっている/蹴っている/転がって）、前脚をかばって→前肢跛行
- 犬「鼻血が出た」・猫「ジャンプしなくなった」をクイック入力に追加（本セッションの新規対応主訴）
- ServiceWorker: `CACHE_NAME` v121 → **v122** → mainマージ後 **v124**（第11/12弾と同版衝突のため改番）

### 薬品辞書リストのサプリメント先頭表示を是正（利用者フィードバック対応）
- 「薬品辞書をクリックするとサプリメントが見えて違和感」— `renderDrugList()` がスポンサー
  （ECVN 11製品）を**リスト先頭に**ソートしていた → 昇順に反転し**末尾**へ（臨床薬が先頭）。
  検索・カテゴリフィルタでの到達性と Sponsor バッジ（透明性表示）は維持
- 回帰テスト: `test_drug_list_sorts_sponsor_supplements_to_bottom`（旧sponsor-first順の再発防止）
- ServiceWorker: `CACHE_NAME` v124 → **v125**

### 回帰テスト（+14件）
- Round 8 クラス11件（鼻血→鼻腔内腫瘍、視覚喪失→白内障、スキップ歩行→パテラ、EPI大量便、
  猫歯根膿瘍/DJD/心因性脱毛、ウサギ歯ぎしり、馬hirsutism→PPID rank1、馬PPID単一エントリ+
  prevalence解決、PPID JSONが内分泌内容で感染/トリロスタン記述なし）
- 薬品3件（生理食塩水の種別用量+高張液混同ガード、コレカルシフェロールの狭治療域警告+B12境界、
  表記ゆれ5ケース）
- クイックタップミラーテストに horse 分岐＋新フレーズ同期

### 表示数値の同期
- `setDefaultStats()` 薬品数11種を実測同期（dog 574, cat 554, horse 360, 鳥系 239, 爬虫類系 105-113）、
  horse diseases 616→615、pendingStats drugs 637→**639**・symptoms 60→**63**

## 2026-08セッション（第20弾: 猫レトロウイルス汚染の全域撲滅 + 馬皮膚腫瘍の病因是正 + シタラビン/イミキモド補完 + チャット精度第9弾 + 全21種クイック入力）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,954件合格**（34 skip、カバレッジ80.68%）
- 薬用量: safe薬品の dosage 欠落 **0**（639薬品時点、species_info 3,769エントリ全数検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- 疾患: 配信6,892疾患で主要臨床フィールド（治療/病因/予後/予防/説明/病態/臨床徴候）の空欄 **0**
- prevalence dead key: **10**（当該種DBに疾患自体が無い既知残、上限15ガード内）

### 猫レトロウイルス（FeLV/FIV）汚染の全域撲滅（約4,000フィールド — 臨床的に危険なクロス種混入）
配信内容の全域監査で、**猫のレトロウイルスであるFeLV/FIVが非猫種のテンプレートに大量残存**していたことを発見:
- 腫瘍病因テンプレート「発癌性ウイルス感染（FeLV関連リンパ腫等の特異的例を除く）」— 馬・鳥・爬虫類等 全20非猫種 1,100+件
- **予防テンプレートが非猫種にFeLVワクチン接種を推奨**（611件 — 馬・ウサギに存在しない猫用ワクチン）
- 貧血予後リスト「基礎疾患（FeLV・FIV・CKD・出血等）」・ITP/貧血の感染性原因リスト・眼科鑑別テンプレート
  「FIP・FeLV・甲状腺機能亢進症」・ウサギトキソプラズマの「FIV/FeLV併発」（猫エントリのコピー）・
  馬ロドコッカスの免疫評価「FIV」等、計9系統のクローズ変種
- 修正: `diseases_all_species.json` 3,646フィールド + `api/data/supplementary_diseases.json` 197フィールド +
  `ferret_diseases.py` 1件 + **生成器自体**（`clinical_fields_generator.py` の neoplasia causes / lymphoid prognosis
  テンプレートからFeLV文を除去 — 再生成での再混入を根絶）。置換は種中立の言い換えのみ（新規の医学的主張なし）
- 配信SQLite実測: 非猫種のFeLV/FIV言及 **0件**（猫レコードの正当な言及は全て温存）
- 回帰テスト+3件（JSON全フィールド走査・配信DB安全網・馬サルコイド病因）

### 馬皮膚腫瘍の病因・治療の是正（開発者専門種のフラグシップ）
- **馬サルコイド（馬で最多の皮膚腫瘍）**: 病因が汎用腫瘍テンプレート（FeLV言及）だった → **BPV-1/2**
  （ウシパピローマウイルス、E5癌タンパク・PDGFR-β活性化・6臨床型・非産生性感染）の教科書的内容に置換（日英）
- **芦毛馬メラノーマ**: → **STX17遺伝子4.6kb重複**（芦毛遺伝子、15歳以上芦毛馬の70-80%）に置換
- **耳介プラーク**: → **EcPV-3/4**（ブユ媒介）に置換　**皮膚SCC**: → UV+**EcPV-2**（外性器型）に置換
- **汎用皮膚科ワークアップテンプレートの撲滅**: 馬モジュールの skin カテゴリ44疾患の `treatment_protocol` が
  「抗真菌シャンプー・グリセオフルビン・ペルメトリン」の汎用皮膚炎テンプレートを共有（サルコイド・メラノーマ・
  SCC等の腫瘍にも適用）→ `_horse_template_markers` に3マーカー追加（皮膚科ワークアップ・腫瘍病因・腫瘍病態）で
  JSON のキュレート済みテキストが必ず優先されるように修正。44件全てが正しい治療文に置換されたことを検証
- 効果: サルコイドの関連薬品チップが ケトコナゾール/グリセオフルビン（誤り）→ **イミキモド/シスプラチン**（正しい）に

### referenced-but-absent 薬品2剤の補完（`drug_batch_43.py` 新規、639→641薬品）
- **シタラビン（Ara-C）** — MUO（GME/NME/NLE）の標準ステロイド補助療法「50 mg/m² SC q12h × 2日間、4週毎」が
  犬猫神経病エントリ8件で逐語参照されるのに未収載（Zarfoss 2006; Lowrie 2013 CRI代替も記載）。
  血液脳関門通過（本剤の存在意義）・骨髄抑制nadir 5-7日・細胞傷害性取扱注意を明記
- **イミキモド5%クリーム** — 馬サルコイド/耳介プラーク（週3回、Nogueira 2006: 80%で75%超縮小、
  塗布時疼痛→鎮静 Torres 2010）・猫SCC in situ（週3回×4-16週、奏効率40-70% Gill 2008、
  グルーミング摂取防止エリザベスカラー）の5参照。TLR7アゴニスト機序
- **MMFは既収載と判明**（id=mycophenolate）— 重複追加を回避し、SARDSエントリの裸表記
  「ミコフェノール酸 20 mg/kg」が解決しないエイリアス欠落のみ `_KATAKANA_VARIANT_ALIASES` で是正
- 回帰テスト+3件（MUOサイクル・血液脳関門・サルコイド/SCC用量・MMF単一エントリ検証）

### 診断チャット精度 第9弾（20症例フレッシュスイープ 9 MISS → 全実用症例合格）
- **エイリアス追加**: 目が赤く（連用形）/目が大きく見える（緑内障・眼球突出）、疲れやすい/舌が紫/舌が青い/歯茎が紫
  （心不全・チアノーゼ）、キャンと鳴/首を動かさない/首を触ると痛がる（頸部IVDD）、便が緑/緑色の便（鳥ビリベルジン尿）、
  呼吸のたびに音/鼻の周りが汚れ（セキセイ副鼻腔炎）、口をあけて呼吸/口をあけたまま/鼻から泡（爬虫類肺炎、かな表記）、
  毛が円形に抜けてる（て形 — チンチラ白癬）
- **ID_SYNONYMS追加**: exercise_intolerance/cyanosis/neck_stiffness/diarrhea_green/white_patches_skin の5系統新設、
  lumps_and_bumps→lumps、wheezing→clicking_breathing_sounds等、**frequent_urination をstraining優先に並べ替え**
  （頻尿=pollakiuria はLUTD徴候 — 従来は polyuria系に解決され尿崩症/糖尿病が上位だった → 膀胱炎/結石/前立腺が上位に）
- **レガシー犬DBに neck_pain 症状を新設**（63→64症状)し IVDD/ウォブラーに付与 →「急にキャンと鳴いて首を動かさない」で
  椎間板ヘルニア top-2（従来は抽出1IDで整形外科のみ）
- **ヘビ感染性口内炎に stomatitis ID を追加**（自身の症状セットに欠落）+ Ophidian Herpesvirus=rare tier →
  「口の中が赤い 食べない よだれ」でマウスロット rank 1（従来は稀なヘルペスが1位）
- **鳥オウム病に fluffed_feathers 追加** + Psittacosis / Chlamydiosis（モジュール正準名）のprevalenceキー新設 +
  Leucocytozoonosis=uncommon + Avocado Toxicity=rare →「羽を膨らませている 便が緑色 元気がない」の
  シックバード三徴でオウム病 rank 1（従来はアボカド中毒/ロイコチトゾーンが上位）
- 回帰テスト: `TestChatClinicalAccuracyAuditRound9`（10件）

### UX: 全21種にクイック入力ボタン（相談チャット導線の完成）
- クイック入力（タップで入力）が10種のみだった → **未対応11種**（インコ・オウム・爬虫類・リクガメ・ヘビ・トカゲ・
  両生類・魚・デグー・フクロモモンガ・その他）に各4-6フレーズを新設。全フレーズが抽出保証済み
  （例: リクガメ「甲羅に傷がある」→shell_lesions、ヘビ「ダニがついている」→visible_mites、
  両生類「皮膚に白いもの」→white_patches_skin、デグー「尻尾の皮がむけた」→tail_injury、
  フクロモモンガ「自分を噛んでしまう」→self_mutilation — 不足エイリアス8種を同時新設）
- ミラーテスト `TestQuickTapPhraseExtraction` の JA_QUICK を21種に同期（新規フレーズ全数の抽出をCIで保証）
- 新薬2剤は既存の治療チップ機構で鑑別診断・チャット結果カードから自動到達（NME→シタラビン、猫SCC→イミキモド、
  サルコイド→イミキモド/シスプラチンのチップ解決を検証済み）

### 表示数値の同期・キャッシュ
- `setDefaultStats()`: dog 574→576・cat 554→556・horse 360→361薬品、pendingStats drugs 639→**641**・
  symptoms 63→**64**（neck_pain追加）
- ServiceWorker: `CACHE_NAME` v125 → **v126**
- 再現手順: FeLV修正はJSON/モジュール/生成器に適用済み → `migrate_to_sqlite.py`（検索インデックスは名前不変のためno-op）

### 疾患消失バグの発見・修正（dedupe×canonical マップの相互作用 — 17疾患を復元）
- **根本原因**: dedupe の生存者選択は「内容の文字数」に敏感な richness スコアのみで決まり、無関係なテキスト編集
  1文字で生存者が canonical マップの「merged側」の双子に反転しうる。反転すると `apply_canonical_map` が
  その生存者を非表示にし、**疾患がブラウズから silently 消失**していた（本セッションのFeLV文削除で
  モルモット乳腺腫瘍が消えかけたことから発見。ベースラインでも同機序で複数疾患が既に消失していた）
- **修正**: `dedupe_disease_list` に **near-tie canonical stabiliser** を追加 — richness がほぼ同等
  （フィールド数同等・文字数差≤300）の場合のみ、レビュー済み canonical マップ（T103）が canonical と
  宣言する側を優先。決定的に充実した側（キュレート vs テンプレート）は従来通り richness が勝つ
  （マップの方向性を内容より信頼しない）。全種マップの union から衝突slug（47件）は中立化
- **復元された疾患（全て追加のみ・削除ゼロを before/after 全種diffで検証）**: 馬 Bucked Shins（キュレート済み
  反復性骨膜炎）、鳥 ビタミンA欠乏症(!)、モルモット 胃潰瘍・皮下膿瘍、フェレット 尿石症・腎嚢胞、
  インコ 卵黄性腹膜炎・甲状腺癌・銅中毒等、リクガメ 膀胱結石、ウサギ ビタミンD中毒 ほか計17件 +
  フクロモモンガ Exophthalmos→Proptosis (Eye Prolapse)（canonical名への正規化1件）
- **馬 canonical マップの方向バグ修正**: bucked-shin ペアの canonical が「Bucked Shin」（急性外傷テンプレート側 —
  第14弾で撲滅した誤病因）を指し、キュレート済み「Bucked Shins」（反復負荷リモデリング）を merged 扱いしていた
  → `api/data/canonical/horse.json` の方向を交換
- **id ロック再生成**: 復元疾患の位置ID衝突を防ぐため全種の `build_id_locks` を再実行（+7新規ロック、append-only）
- 配信ブラウザブル数: 6,432 → **6,449**（検索インデックス 6,449 に再生成、id 重複 0）
- 回帰テスト: `TestCanonicalAwareSurvivorSelection`（3件 — near-tie優先・決定的richness差の維持・
  モルモット乳腺の配信検証・インデックス整合）

### 有病率priorのトークンセット・フォールバック（disease_matcher）
- prevalence キーは1疾患1正準表記（"Psittacosis (Chlamydiosis)"）だが、モジュール側の表記ゆれ
  （"Psittacosis / Chlamydiosis"）では完全一致せず prior が不発だった → 語順・区切り記号非依存の
  トークンセット一致でフォールバック解決（フロントの `_resolveCommonDiseaseName` と同方針。
  "Gout (Articular)" vs "(Visceral)" はトークンが異なり誤マージしない。曖昧セットは棄却）
- これにより過去に削除済みの dead key（"Psittacosis / Chlamydiosis"）を復活させることなく prior が有効化

### 表示数値の同期（第2弾）
- `setDefaultStats()` 全21種を `/api/species-stats` の**ブラウズ可能数**基準に同期（dog 619→601疾患 等 —
  従来のフォールバック値は canonical 適用前の基準でAPIと乖離していた）、pendingStats diseases 6432→**6449**

### テスト・CI（セッション終了時）
- フルテストスイート: **3,973件合格**（34 skip、+19新規回帰テスト）、ruff check/format clean
- 再現手順: `migrate_to_sqlite.py` → `build_disease_search_index.py`（id ロックは append-only 再生成済み）

### 既知の残課題（次セッション候補）
- canonical マップに「canonical側の疾患名がモジュールに既に存在しない」dangling merge が残存
  （richness差が大きく near-tie 帯で救済されないもの — 例: guinea_pig 'Pneumonia (Bacterial)'→'bacterial-pneumonia'）。
  `scripts/quality/build_canonical.py` によるマップ再生成＋獣医レビューで解消するのが本筋
- SQLite配信パス（6,892行）と fallback/canonical パス（6,449件）のブラウズ集合の差（canonical はread時適用）の一元化

## 2026-08セッション（第21弾: prevalence正準名リネーム第2波 + シメチコン/トリエンチン/オロパタジン補完 + チャット精度第10弾 + 犬レガシー膀胱炎/声変化）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,973件合格**（34 skip、カバレッジ82.14%）
- 薬用量: safe薬品の dosage 欠落 **0**（641薬品時点、全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- 疾患: 配信6,892疾患で主要臨床フィールド（治療/病因/予後/予防/説明/病態/臨床徴候）の空欄 **0**

### prevalence 正準名リネーム第2波（dead key 17→9、第20弾dedupe復元の後追い同期）
第20弾の canonical stabiliser で復元された疾患は**正準名側**が生存するため、旧名で張られた
prevalence キーが配信DB完全一致で不発化していた（chip name_ja 欠落・fuzzy解決落ち）:
- bird 'Vitamin A Deficiency'→'Vitamin A Deficiency (Hypovitaminosis A)'、
  guinea_pig 'Subcutaneous Abscess'→'Abscess (Subcutaneous)'・'Gastric Ulcer'→'Gastric Ulcers'、
  parakeet 'Copper Toxicosis'→'Copper Poisoning'・'Egg Peritonitis'→'Egg Yolk Peritonitis'・
  'Renal Adenocarcinoma (Parakeet)'→'Renal Adenocarcinoma'、tortoise 'Bladder Stone'→
  'Bladder Stones (Urolithiasis)'、degu 'Uterine Tumor'→'Uterine Adenocarcinoma'（真の dead key を活性化）
- モジュール生名（チャットprior経路）でも全キー解決を検証。残9件は当該種DBに疾患が無い既知残
- 回帰テスト: fixed_round3 セット追加（tests/test_prevalence_data.py）

### referenced-but-absent 薬品3剤の補完（`drug_batch_44.py` 新規、641→644薬品）
用量文脈フィルタ付きカタカナトークン監査（第12回スイープ、実マッチャー突合）で検出:
- **シメチコン（ガスコン）** — 草食小型哺乳類6種のGIうっ滞/鼓脹プロトコルが「40-50mg/kg PO q6-8h」等の
  用量付きで**37参照**するのに未収載。腔内限局・全身吸収なしの消泡界面活性剤（Carpenter 6th:
  ウサギ65-130 mg/kg）。閉塞/GDVで経口投与のため減圧を遅らせない旨を禁忌に明記
- **トリエンチン** — 犬銅関連性肝障害エントリが名指しする第二選択銅キレート剤（ペニシラミン不耐例、
  10-15 mg/kg PO q12h 空腹時、ACVIM 2019）。亜鉛との2時間間隔・併用不可を明記
- **オロパタジン0.1%点眼（パタノール）** — アレルギー性結膜炎プロトコル参照。猫はFHV-1優先鑑別を明記
- **DOCP頭字語エイリアス** — アジソン病テキストの「DOCP 2.2 mg/kg IM q25日」が既収載
  desoxycorticosterone に解決しなかった → _KATAKANA_VARIANT_ALIASES に DOCP/デソキシ/デスオキシ追加
- 回帰テスト4件（TestBatch44）。新薬は治療チップ機構で鑑別診断・チャット結果カードから自動到達
  （rabbit GI stasis→simethicone、dog銅蓄積症→trientine のチップ解決を検証済み）

### 診断チャット精度 第10弾（26症例フレッシュスイープ 10 MISS → 全実用症例合格）
- **犬レガシーDBに細菌性膀胱炎（UTI）を新設**（72→73疾患）: 犬で最頻の泌尿器主訴なのにエントリが無く、
  頻尿主訴が多飲多尿疾患（糖尿病/CKD/家族性腎症）ばかり上位だった（ISCAID 2019; ~14%生涯発生率、tier=very_common）
- **犬レガシーDBに voice_change 症状を新設**（64→65症状）し喉頭麻痺に付与: 「水を飲むとむせる 声がかすれる」
  →喉頭麻痺 rank 1（むせる→coughing、声がかすれる→voice_change エイリアス新設）
- **エイリアス追加（約30件）**: GDV「お腹が膨らんで/吐こうとしても吐けない」、ブロック猫「砂が濡れていない/
  鳴きながらいきむ」、ポラキウリア連用形「おしっこの回数が多く/少ししか出ない」、趾間皮膚炎「足の裏を舐め/
  指の間が赤い」、テイルボビング「尾が上下する/呼吸のたびに尾」、趾瘤症「足の裏が腫れて/タコのようになって」、
  フェレット副腎「毛が尻尾から抜け/皮膚が薄い→thinning_skin」、ノトエドレス「耳の先が黒く→crusting」、
  進行形「目が白く濁ってきた」、ボルボリグミ「お腹がキュルキュル→stomach_gurgling」、悪心プロキシ「草を食べたがる→nausea」
- **ID_SYNONYMSブリッジ**: stomach_gurgling→[nausea,bloating]、nausea→[vomiting,retching]、
  voice_change→[vocalization_changes,wheezing,stridor]、dry_skin→[scaling,...]（猫はscaling表記のため）、
  cloudy_eye/cloudy_eyes→cataracts 追加（**ウサギ語彙に濁眼IDが無く「目が白く濁って」系が全滅していた** → 白内障が解決）
- **_LEGACY_FALLBACK**: stomach_gurgling→bloating、nausea→vomiting、decreased_urination→straining、skin_redness→skin_rashes
- **有病率是正**: ferret Botulism=rare（未ティアでインスリノーマ低血糖主訴の1位を奪っていた）、
  guinea_pig Aortic Calcification=uncommon（壊血病を上回っていた）、cat 抗凝固殺鼠剤=common→uncommon
  （猫は摂食習性から犬より顕著に稀 — 開口呼吸主訴の2位に出ていた）
- 回帰テスト: TestChatClinicalAccuracyAuditRound10（13件）

### UX: クイック入力にGDV救急主訴を追加
- 犬に「お腹が膨らんで吐こうとしても吐けない」（GDV=分単位の救急。タップ→胃拡張捻転が即rank 1）
- ミラーテスト JA_QUICK 同期（全フレーズ抽出保証をCIで維持）

### 表示数値の同期・キャッシュ
- `setDefaultStats()`: dog 579/cat 558/rabbit 272/guinea_pig 139/chinchilla 93/hamster 71薬品、
  pendingStats drugs 641→**644**・symptoms 64→**65**
- ServiceWorker: `CACHE_NAME` v126 → **v127**
- 再現手順: `migrate_to_sqlite.py`（644薬品反映。疾患名不変のため検索インデックスno-op）

## 2026-08セッション（第22弾: 犬レガシーDBに寄生虫症・子癇を新設 + 嘴過長エイリアス誤マッピング修正 + CaEDTA/UDCAエイリアス + 自由入力チャット→チェッカーピボット）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,990件合格**（34 skip）
- 配信SQLiteクリーンビルド: 6,892疾患、treatment/prevention/prognosis **100%**、主要臨床フィールド空欄 **0**
- 薬用量: safe薬品の dosage 欠落 **0**（644薬品、全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- prevalence dead key: **9**（当該種DBに疾患自体が無い既知残、上限15ガード内）

### 薬品マッチャー: 頭字語・語順ゆれエイリアス4件（sweep #13、約120参照がチップ化）
用量文脈フィルタ付きカタカナ/英語トークン監査（第13回スイープ、find_drugs_in_text 実マッチャー突合）。
今回は referenced-but-absent の新薬ゼロ（辞書は充足）で、真の欠落は全てエイリアス層:
- **CaEDTA**（51参照）→ calcium_edta — 馬鉛中毒「CaEDTA 75 mg/kg IV slow」等の頭字語表記が解決不能だった
- **UDCA**（41参照）→ ursodiol — 「UDCA 10-15 mg/kg PO q24h」の標準臨床略号
- **ヘタスターチ**（8参照）→ hetastarch — 正準名はヒドロキシエチルデンプン
- **カルシウムグルコン酸(塩)**（21参照）→ calcium_gluconate — グルコン酸カルシウムの語順逆転形
  （馬低Ca血症・両生類MBDの治療文）。プレフィックス一致で 酸/酸塩 両形をカバー
- 回帰テスト: `test_sweep13_acronym_and_word_order_aliases_resolve`（5解決+2精度ガード）

### 診断チャット精度 第11弾（20症例フレッシュスイープ 7 MISS → 全症例合格）
- **エイリアス誤マッピング修正**: 「嘴が伸びてる/嘴過長/嘴が長い」→ **loss_of_appetite**（食欲不振!）に
  誤マッピングされていた → **overgrown_beak** に是正 +「くちばしが伸びすぎ」追加。
  鳥「くちばしが伸びすぎて変形」→ 嘴過長症/シザービーク top-3（従来は抽出ゼロ）
- **犬レガシーDBに腸管寄生虫症を新設**（73→75疾患、65→67症状）: 子犬で最頻レベルの主訴なのに
  内部寄生虫エントリも便中虫体語彙も皆無で、「便に白い米粒のようなもの」（瓜実条虫片節のパトグノモニック
  主訴）が抽出ゼロだった → worms_in_stool 症状 + intestinal_parasites エントリ（very_common、
  ESCCAP GL1/CAPC、人獣共通・ノミ中間宿主を明記）+ 単独パトグノモニック・クラスタ×1.8 → rank 1
- **犬レガシーDBに子癇（産褥テタニー）を新設**: 治療テキストが参照するのにエントリが無く
  「産後に震えて痙攣しそう 授乳中」が特発性てんかん1位だった → postpartum_lactating 文脈フラグ症状
  （産後/出産後/授乳中エイリアス）+ eclampsia エントリ（10%グルコン酸Ca 0.5-1.5 mL/kg 緩徐IV、
  小型犬・多頭産リスク、Plumb's/Ettinger 8th）+ {postpartum, tremors/seizures}→子癇×1.8 クラスタ
  → rank 1（産後文脈なしの痙攣は従来どおり てんかん1位を維持 — 回帰テストで固定）
- **ハムスター頬袋インパクション**: 既存キー「頬袋が戻らない」は「膨らんだまま」が間に挟まると
  不一致 → 「頬袋が膨らんだまま/膨らんで」→cheek_swelling 追加 → 頬袋膿瘍/頬袋閉塞 top-3
- **トカゲ総排泄腔脱**: 「お尻から何か出て」→rectal_prolapse は抽出できたがトカゲ語彙に
  rectal_prolapse系IDが無く解決不能だった → _ID_SYNONYMS を tissue_protruding_from_cloaca/
  tissue_prolapse/cloacal_swelling へ拡張 → 臓器脱 top-5
- **ヘビ・スペクタクル残留**: 「脱皮した皮が目に残って」等4形→retained_spectacle 新設 → 眼鏡鱗停滞 rank 1
- **モルモット白内障**: 「目が白く濁って」素の連用形（てる/てきた形のみ収載だった）→ cloudy_eye → 白内障 rank 1
- **猫の条虫片節**: worms_in_stool→visible_worms/visible_parasites ブリッジで猫「便に白い米粒」→ 瓜実条虫症 rank 1
- 回帰テスト: `TestChatClinicalAccuracyAuditRound11`（10件）

### UX: 自由入力チャット→チェッカーの微調整ピボット（双方向動線の最終ピース）
- 問診モード最終結果には「チェッカーで症状を微調整して再解析」があるが（第14弾）、**自由入力チャットの
  結果には無く**、1症状変えるには主訴全文を打ち直すしかなかった
- `_runCheckerWithSymptoms(sp, ids, evName)` 共有ヘルパーに引き継ぎロジックを集約
  （runCheckerFromGuided は委譲に）。自由入力チャット結果カード末尾に「🧪 チェッカーで症状を微調整して
  再解析」ボタンを追加 — 抽出済み症状ID（data-ids）とチャット種（data-species）を運び、
  種切替の readiness poll → チェッカー事前選択 → 自動解析。語彙で解決不能なIDは安全に脱落
  （全て解決不能ならトースト警告）。GA4 `checker_from_chat` イベント
- 委譲ハンドラ（`_attachChatNavHandlers`）でルーティング — innerHTMLリセット後も動作
- CSS `.chat-checker-refine`（アンバー系、min-height 32px タップ領域）
- 回帰テスト: `test_app_js_free_chat_results_pivot_to_checker` + 既存 guided ピボットテストを
  共有ヘルパー構造に更新

### UX: クイック入力に新規対応主訴を追加（1タップ導線）
- 犬「便に白い米粒のようなもの」・ハムスター「頬袋が膨らんだまま戻らない」・
  ヘビ「脱皮した皮が目に残っている」（全て本セッションで抽出保証済み、ミラーテスト同期）

### 表示数値の同期・キャッシュ
- `pendingStats` symptoms 65→**67**（worms_in_stool/postpartum_lactating 追加）
- ServiceWorker: `CACHE_NAME` v127 → **v128**

## 2026-08セッション（第23弾: タイロシン誤表記の是正 + BPH/G-CSF薬品3剤 + チャット精度第12弾 + 自由チャット低情報警告→問診モード動線）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **4,002件合格**（34 skip、カバレッジ80.78%）
- 配信SQLiteクリーンビルド: 6,892疾患、treatment/prevention/prognosis **100%**、主要臨床フィールド空欄 **0**
- 薬用量: safe薬品の dosage 欠落 **0**（644薬品、全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- prevalence dead key: **9**（当該種DBに疾患自体が無い既知残、上限15ガード内）

### 臨床的に誤った薬品名の修正: チロシン→タイロシン（アミノ酸≠抗菌薬）
- 犬のIBD/EPI/SIBO/抗菌薬反応性下痢/慢性腸症と猫EPIの計6疾患群で、抗菌薬タイロシン（tylosin）が
  **アミノ酸チロシン（tyrosine）と誤表記**されていた（「チロシン 25 mg/kg PO q12h×6週」等、JSON 9フィールド+
  dog/cat モジュール6箇所+enrichmentスクリプト3件）。チロシンキナーゼ阻害薬（トセラニブ等）の正当な言及と、
  馬・無汗症のチロシン（神経伝達物質前駆体=本物のアミノ酸）は温存
- 修正により SIBO 等の関連薬品チップが tylosin に正しく解決（従来は誤表記で不達）
- 回帰テスト: `test_no_tyrosine_typo_for_tylosin_in_disease_content`（用量文脈の非キナーゼチロシンをJSON+モジュール走査で検出）

### referenced-but-absent 薬品3剤の補完（`drug_batch_45.py` 新規、644→647薬品）
用量文脈カタカナ/英語トークン監査（第14回スイープ、find_drugs_in_text 実マッチャー突合）で検出:
- **フィナステリド（プロスカー）** — 犬BPHエントリ3件が「0.1-0.5 mg/kg PO q24h」で参照する5α-還元酵素阻害薬。
  精液性状・繁殖能温存（Sirinarumitr 2001 JAVMA: 16週で前立腺体積43%減）。**催奇形性 — 妊娠中の飼い主が
  破損錠剤を素手で扱わない**警告を明記。猫は適応なし（safe:False）
- **酢酸オサテロン（Ypozane/イポザン）** — EU承認の犬BPH動物用医薬品（0.25-0.5 mg/kg PO×7日、効果5-6ヶ月、
  Albouy 2008）。**投与後数週間のACTH刺激コルチゾール反応減弱**（SPC）を明記。BPHエントリの
  garbled 参照「acetate 0.25-0.5 mg/kg PO」（薬品名脱落）も正しい名称+用量に修正
- **フィルグラスチム（rhG-CSF）** — パルボ×2・免疫介在性好中球減少（犬猫）・ボーダーコリーTNS・
  メチマゾール副反応・フェレット高エストロジェン血症の7エントリが「5 μg/kg SC q24h」で参照。
  **異種蛋白のため約2-3週で中和抗体形成→遷延性好中球減少 — 短期投与限定**が定義的安全事実。
  「G-CSF」裸頭字語も解決（GM-CSFには誤マッチしない境界ガード検証済み）
- 3剤とも治療チップ機構で鑑別診断・チャット結果カードから1タップ到達を検証
  （BPH→finasteride/osaterone、好中球減少→filgrastim）

### 診断チャット精度 第12弾（16症例フレッシュスイープ 6 MISS → 全症例合格）
- **犬レガシーDBに耳血腫・KCSを新設**（75→77疾患、67→70症状）:
  - 耳血腫: 外耳炎の頻発続発症なのに耳介腫脹語彙が無く「耳が腫れてぷよぷよ」が head_shaking のみ抽出→
    外耳炎単独1位だった。ear_swelling 症状+エイリアス5種（耳がぷよぷよ/耳血腫等）+ ID_SYNONYMS
    （猫は ear_inflammation 表記へブリッジ）→ rank 1
  - 乾性角結膜炎（KCS）: 犬の高頻度眼科疾患（好発犬種2-2.5×）なのにドライアイ語彙ゼロで眼瞼疾患が上位
    だった。dry_eye 症状+エイリアス（目が乾いて/ドライアイ/目やにがベタベタ）→ rank 1
- **膵炎の祈りのポーズ主訴**: abdominal_pain 症状を新設し（お腹を触ると痛がる エイリアス追加）、
  {vomiting, abdominal_pain}→膵炎 ×1.5 パトグノモニック・クラスタ追加（Ettinger 8th; Xenoulis 2015）→
  「背中を丸めて震えて嘔吐 お腹を触ると痛がる」で膵炎 rank 1（従来アジソン/IVDD上位）。
  産後文脈なしの痙攣=てんかん1位は回帰テストで固定
- **馬・食道閉塞（チョーク）が抽出ゼロだった**: 「飲み込め（ない）」「鼻から餌/食べ物/飼料」→
  dig_salivation / resp_bilateral_discharge エイリアス新設 + **症候群ペアブースト**
  {dig_salivation, resp_bilateral_discharge}→チョーク×1.5（流涎+鼻孔からの飼料逆流=チョークの definitional pair、
  Reed & Bayly 4th ed）+ 食道憩室=rare/食道狭窄=uncommon/唾石症=rare/巨大食道症=uncommon の有病率是正
  （稀な2所見エントリがカバレッジ1.0でチョーク自身を上回っていた）→ rank 1
- **フェレット**: ニューモシスチス肺炎=rare（未ティアで咳+呼吸困難+腹水の心筋症/CHF三徴1位を奪っていた）
- **鳥3種**: エッセンシャルオイル中毒=rare（曝露依存毒性、産卵後振戦でカルシウム欠乏症繁殖型を上回っていた）
- **リクガメ/爬虫類**: {eye_swelling/swollen_eyes + anorexia}→ビタミンA欠乏症×1.45 パトグノモニック・ペア
  （両側眼瞼腫脹はカメでhypovitaminosis A until proven otherwise — Mader 3rd ed）→ rank 5→2
- **素のて形「毛が抜けて」**が全種で抽出不能だった（〜抜ける/〜抜けてきた のみ収載）→ エイリアス追加
- 回帰テスト: `TestChatClinicalAccuracyAuditRound12`（9件）

### UX: 自由入力チャットの低情報警告→問診モードのワンタップ動線
- 自由チャットの低情報警告（症状1-2個のみ）は**テキストのみ**で、チェッカーの低信頼度バナー（問診ピボット付き）と
  非対称だった → 警告ボックス内に「🩺 問診モードで症状を段階的に確認する」ボタンを追加。
  委譲ハンドラ（`.chat-guided-pivot`）で chat ビュー切替+guided モード起動+モード切替へスクロール
  （ランディングチャットからも動作）。GA4 `guided_from_chat_low_info` イベント
- 回帰テスト: `test_app_js_free_chat_low_info_warning_pivots_to_guided_mode`

### UX: クイック入力に新規対応主訴を追加（1タップ導線）
- 犬「耳が腫れてぷよぷよしている」（→耳血腫 rank 1）、馬「飲み込めず鼻から餌が出てくる」
  （→チョーク即 rank 1）。ミラーテスト JA_QUICK 同期（全フレーズ抽出保証をCIで維持）

### 表示数値の同期・キャッシュ
- `setDefaultStats()`: dog 582/cat 561/ferret 205/degu 159薬品、pendingStats drugs 644→**647**・
  symptoms 67→**70**
- ServiceWorker: `CACHE_NAME` v128 → **v129**

### テスト・CI
- フルテストスイート: **4,016件合格**（34 skip、+14新規回帰テスト）、カバレッジ82.16%
- ruff check/format: repo全体 clean
- 配信DB: クリーンビルドで 6,892疾患・**647薬品**、treatment/prevention/prognosis 100%

## 2026-08セッション（第24弾: スマホの鑑別診断文字サイズ修正 — モバイル・フォントインフレーションの無効化）

### 背景（開発者からの直接フィードバック）
「スマホにて鑑別診断時の文字が大きい」— カードのフォント指定は小さい（見出し.88rem・本文.8rem）のに、
スマホでは鑑別診断結果の長文（治療プロトコル・病態生理等）だけが拡大表示されていた。

### 根本原因: text-size-adjust 未設定によるモバイルブラウザのフォント自動拡大
- スタイルシートに `text-size-adjust` が一切無く、Android Chrome の Font Boosting / iOS Safari の
  自動テキスト拡大が「幅制約のない長文ブロック」を勝手に拡大していた
- 鑑別診断カードの `.detail-section-body`（white-space:pre-wrap の長い日本語段落）がまさに対象で、
  ヘッダーは小さいまま長文だけ大きくなる = 報告症状と一致
- 修正: `html` ルールに `-webkit-text-size-adjust:100%;-moz-text-size-adjust:100%;text-size-adjust:100%`
  を追加（normalize.css 標準の修正）。**拡大ヒューリスティックのみ無効化** — ユーザーのピンチズームと
  ブラウザのアクセシビリティ文字サイズ設定は影響を受けない。サイト全域（チャット結果・疾患DB詳細含む）に適用
- 回帰テスト: `test_main_css_disables_mobile_font_inflation`（html ルール内の text-size-adjust を検証）
- ServiceWorker: `CACHE_NAME` v129 → **v130**

## 2026-08セッション（第25弾: 括弧内商品名インデックス + 薬品→疾患逆引きのオーバーレイ対応と起動時ウォーム + チャット精度第13弾 + 犬レガシー乳腺/精巣腫瘍新設）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **3,970件合格**（80 skip — 初回はDB未構築のためのskip含む）
- 薬用量: safe薬品の dosage 欠落 **0**（647薬品、全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- 疾患: 配信SQLiteクリーンビルド 6,892疾患、treatment/prevention/prognosis **100%**

### 薬品マッチャー: 括弧内商品名の tier-4 インデックス（sweep #15、約200+参照がチップ化）
- **バグ発見**: 商品名エイリアス（drug_brand_names.py）のマージは「name/name_ja に既出の別名をスキップ」
  するが、キーワード索引は括弧内を剥がすため、**括弧の中だけに存在する商品名は永遠に解決不能**だった
  （プロジンク 19refs・コバラミン 22・アポキル/サイトポイント 各9・セレニア・バナミン・ガスコン等）
- `_build_drug_keyword_index` に **tier-4（純カタカナの括弧内パート）** を追加。Latin括弧パートは
  汎用英単語（oral/renal/saline等）が支配的なため対象外。`_PAREN_PART_STOPLIST` で一般語を遮断:
  エキゾチック・インプラント・プログラム・メトロノミック・**バリウム**（=造影のバリウム。Valium音写が
  diazepam の括弧内にあり、104件の造影文脈に誤チップするところをレビューで検出・遮断）
- `_KATAKANA_VARIANT_ALIASES` 追加: tiludronate（ティルドロネート/チルドロネート — 正準はチルドロン酸、
  馬ナビキュラー9refs）、insulin_glargine（グラルギン）、insulin_detemir（デテミル）、
  insulin_pzi（プロジンク — 傘エントリ insulin_vetsulin の括弧リストとの tier 衝突を専用エントリ優先で解決）
- `BRAND_NAME_ALIASES` 追加: プロジンク/ベトスリン/カニンスリン/ランタス/レベミル（インスリン製剤5ブランド）
- 回帰テスト: `test_sweep15_paren_brand_names_resolve_in_text_matcher`（12解決+5精度ガード）

### 薬品→疾患逆引き（この薬品を使う疾患）のJSONオーバーレイ対応 + 起動時ウォーム
- **バグ**: `_build_drug_to_diseases_index` はPythonモジュールの治療文のみ走査していたため、
  **JSONオーバーレイにしか治療文が無い薬品の逆引きカードが空**だった（例: tiludronate は
  順方向チップは出るのに「この薬品を使う疾患」が0件）→ `diseases_all_species.json` も走査
  （(species,name) dedup で二重ヒットは収束）。tiludronate 0→5疾患、insulin_pzi 20→30
- **レイテンシ改善**: 走査は corpus 連結+キーワード毎の C-speed `str.find` スイープに書き換え
  （旧: 26k texts × 1.9k keywords の Python ループ）。さらに**インポート時デーモンスレッドで
  事前構築**（従来は初回リクエストが数十秒ブロックし本番 worker timeout 圏内だった。
  ロックレス設計 — fork でスレッドが死んでも同期ビルドにフォールバックしデッドロックしない）

### 診断チャット精度 第13弾（22症例フレッシュスイープ 5 MISS → 全症例合格）
- **犬レガシーDBに乳腺腫瘍・精巣腫瘍を新設**（77→79疾患、70→71症状）:
  - 乳腺腫瘍: 未避妊雌犬で最多の腫瘍（Sorenmo, Withrow & MacEwen 6th）なのにエントリも乳腺語彙も無く
    「乳腺にしこり」が汎用 lumps のみ抽出だった。mammary_swelling 症状+very_common tier → rank 1
  - 精巣腫瘍（セルトリ細胞腫・女性化症候群）: 「オスなのに乳首が腫れて毛が抜ける」が脱毛症X上位だった。
    女性化ペア {mammary_swelling, hair_loss}→×1.5 クラスタ → rank 1。
    **症状セットは女性化ペアに限定**（pale_gums/lethargy を持たせると貧血主訴を乗っ取ることを検証で発見・回避）
- **黄疸の複合表現**: 「白目と歯茎が黄色い」が抽出ゼロ（「白目が黄色い」完全形のみ収載）→
  歯茎が黄色い/目が黄色い/皮膚が黄色い を追加 → 肝臓病/IMHA/溶血性貧血が top-3
- **「呼吸が速い」（速表記）が全種で抽出不能だった**（「呼吸が早い」のみ収載）→ 速い/速く/息が速い を追加
- **フェレット低血糖の口掻き**: 「口を前足で掻く」→ 掻く→itching で耳ダニに誤誘導 →
  pawing_at_mouth 直接解決（最長一致で勝つ、て形も追加）+ ID_SYNONYMS [pawing_at_face, drooling,
  difficulty_eating] + 泡を吹く→drooling → インスリノーマ top-3
- **チンチラ熱中症**: 「耳が赤くて」連用形欠落 + rapid_breathing↔excessive_panting/dyspnea の
  マッチング側ブリッジ欠落 → _SYN 拡張 + パトグノモニック・ペア {red_ears, rapid_breathing}×1.45 /
  {red_ears, lethargy}×1.35（充血耳=チンチラ高体温の cardinal sign、Quesenberry & Carpenter 4th）→ rank 1
  （耳掻き主訴は外耳炎/白癬 first を回帰テストで固定）
- **猫乳腺しこり**: 「乳腺にしこり」が同長タイの「しこりがある」に消費され lumps のみ抽出 →
  7文字形エイリアスで最長一致を確実化 + ID_SYNONYMS mammary_swelling→[mammary_masses,...] →
  乳腺グループが top-3 独占。有病率是正: Triple Negative乳癌=分子亜型でcommonは過大→uncommon、
  猫顕性偽妊娠=rare（誘発排卵のため犬と異なり稀 — Little, The Cat）
- 回帰テスト: `TestChatClinicalAccuracyAuditRound13`（8件）

### UX: クイック入力に新規対応主訴を追加（1タップ導線）
- 犬「乳腺にしこりがある」・チンチラ「耳が赤くて呼吸が速い」（熱中症=分単位の救急）・
  フェレット「口を前足で掻いてよだれ」（低血糖）— 全て抽出保証済み、ミラーテスト JA_QUICK 同期
- 新設疾患は疾患DBの dog モジュール「Mammary Tumor/乳腺腫瘍」「Testicular Tumor/精巣腫瘍」に
  base-name 完全一致するため、チャット候補カードの「疾患DBで詳細を開く」ピボットがそのまま機能

### 表示数値の同期・キャッシュ
- pendingStats symptoms 70→**71**、ServiceWorker: `CACHE_NAME` v130 → **v131**（第24弾のv130と衝突したため改番）

## 2026-08セッション（第26弾: 否定表現ガード + ジアゾキシド/リバロキサバン/マムシ抗毒素/グルカゴン補完 + 救急key drugリンク化 + チャット精度第13弾）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **4,016件合格**（34 skip）
- 配信SQLiteクリーンビルド: 6,892疾患、treatment/prevention/prognosis **100%**、主要臨床フィールド空欄 **0**
- 薬用量: safe薬品の dosage 欠落 **0**（647薬品時点、全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- prevalence dead key: **9**（当該種DBに疾患自体が無い既知残、上限15ガード内）

### 症状抽出の否定表現ガード（新規・系統的修正）
- **バグ**: 「咳はない」「嘔吐はしていない」「下痢なし」のような**除外情報のつもりの入力が、
  逆に症状として抽出され鑑別を汚染**していた（例: 猫「呼吸が速くて…咳はない」で coughing 抽出
  → 呼吸器より咳疾患が上位）
- `symptom_extractor.py` に `is_negated_mention()` を新設: 症状語の直後（は/も + まだ/特に を許容）に
  否定語（ない/無い/なし/ありません/出ていない/していない/見られない等）が続く場合のみ発火する保守的設計。
  「食欲がない」「飲み込めない」のような否定形を内包するエイリアス自体はマッチ範囲の後ろを検査するため不変
  （正属性の単独症状名が存在しないことを全種+レガシーで検証済み）
- 種別抽出（Phase1/2）・レガシー犬抽出（Phase1/2）の両経路に適用

### referenced-but-absent 薬品4剤の補完（`drug_batch_46.py` 新規、647→651薬品）
救急タブkey drugリンク化監査 × 治療テキスト参照の突合（第15回スイープ）で検出:
- **ジアゾキシド（プログリセム）** — インスリノーマ標準第二選択（44参照）なのに未収載。
  フェレット/犬 5-30 mg/kg PO q12h（Quesenberry & Carpenter 4th; Goutal 2012 JVECC）。
  食事と共に投与・低血糖クリーゼの緊急対応は50%ブドウ糖であり本剤で代替しない旨を明記
- **リバロキサバン（イグザレルト）** — 猫ATE救急プロトコルのkey drugなのに経口Xa阻害薬が皆無だった。
  猫 2.5 mg/頭 PO q24h（Dixon-Jimenez 2016; CURATIVE合意 Blais 2019）・犬 1-2 mg/kg PO q24h。
  猫第一選択は依然クロピドグレル（FATCAT）・治療量抗凝固薬同士の併用禁止（major）を明記
- **マムシ抗毒素血清（乾燥まむしウマ抗毒素）** — マムシ咬傷救急プロトコルのkey drug、日本臨床で
  最重要の抗毒素なのに未収載。1バイアル6,000単位・咬傷後4-6時間以内（Hifumi 2015）・
  ウマ由来血清のアナフィラキシー前処置・多くの犬咬傷は支持療法単独で回復（重症例に温存）を明記
- **グルカゴン** — 難治性低血糖CRI（20参照 + 救急key drug）。50 ng/kg IVボーラス→CRI 5-40 ng/kg/分
  （Plumb's 10th; Fischer JAVMA 2000）。急な中止での反跳性低血糖を明記

### 商品名エイリアスの括弧内スキップバグ修正（系統的） + sweep #15
- **バグ**: 商品名マージは「name/name_ja に含まれる別名」をスキップするが、キーワード索引は
  括弧サフィックスを剥がすため、**括弧内にだけ載る商品名（PZIインスリン（プロジンク））は
  検索にもテキストマッチにも永久に到達不能**だった → スキップ判定を括弧前ステムに限定
  （プロジンク41参照・ランタス・レベミル等が解決）
- BRAND_NAME_ALIASES にインスリン5製剤（プロジンク/ランタス/レベミル/ヒューマリンR/カニンスリン）追加
- _KATAKANA_VARIANT_ALIASES: ティルドロネート（チルドロン酸の表記ゆれ）、セレン酸ナトリウム（白筋症9参照）、
  銀スルファジアジン（語順逆転47参照 — 従来は全身投与用スルファジアジンに誤チップ）、
  プラズマライト/グルコン酸Ca（救急key drug表記）

### UX: 救急プロトコルkey drugのワンタップ導線（最高緊急度画面のデッドテキスト解消）
- 救急タブのkey drugsリスト（117行）は**素のテキスト**で、分単位で用量詳細に到達したい画面から
  薬品辞書への導線が無かった
- `emergency_api.py` に `_resolve_key_drug_links()` 新設: find_drugs_in_text で辞書解決し、
  **英語名トークン重なり最大**のエントリを選択（"Ampicillin/sulbactam" が素の ampicillin ではなく
  ampicillin_sulbactam に着地）。解決行にのみ `link_name` 付与 → フロントは解決行だけを
  `.drug-nav-link` 化（誤着地・デッドリンクゼロ設計）。**117行中113行がリンク化**
  （残4行はFFP/tPA — 辞書対象外の血液製剤・血栓溶解薬で設計通り素のテキスト維持）

### 診断チャット精度 第13弾（22症例フレッシュスイープ 7 MISS + 誤抽出1 → 全症例合格）
- **エイリアス誤マッピング修正**: 「キーキー鳴く/鳴き声が変」→ **lethargy**（悲鳴が「元気消失」に化ける
  明白な誤り）→ vocalization_changes に是正 + ID_SYNONYMS で vocalization/screaming/
  pain_vocalization/distress_vocalizations へブリッジ
- **レガシー犬DBに吐出・褐色尿を新設**（70→72症状）:
  - regurgitation（未消化物の吐き戻し = 巨大食道症の定義的徴候）を巨大食道症に付与 →
    「食べた後すぐに未消化のまま吐く 痩せた」で巨大食道症 rank 1（従来は寄生虫/IBD上位・rank5）
  - dark_urine（ヘモグロビン尿/ビリルビン尿）をIMHA・溶血性貧血に付与 + エイリアス
    （おしっこが茶色い/コーラ色の尿）→ 溶血性貧血+IMHAが top2
- **フェレット・インスリノーマ発作**: 「急にキーキー鳴いて足を伸ばして硬直」が抽出ゼロ →
  seizures/vocalization 抽出 + パトグノモニック・ペア {seizures, vocalization}→Insulinoma×1.35
  （フェレットの発作の最多原因は低血糖 — Quesenberry & Carpenter 4th）+ 原発性てんかん=rare tier +
  インスリノーマ症状セットに vocalization 追加 → rank 1（0.886）
- **新規エイリアス**: 粗相する/トイレ以外で排尿（猫 inappropriate_urination → FIC/UTI/マーキングがtop5）、
  口をくちゃくちゃ（猫 jaw_chattering → 歯の吸収病変 rank 1）、呼吸が速い（速い表記 — 従来は早いのみ）、
  あごが濡れている（かな表記 → ウサギ不正咬合群がtop3）、目が飛び出してきた（てきた形 → 眼球突出 rank 1-2）、
  首が片方に傾いて（斜頸）、止まり木を握れない/脚に力が入らない（鳥）、鰓の動きが速い（かな/漢字表記）、
  お腹のうろこが赤い（ヘビ・スケールロット → 鱗腐敗 top2）、未消化のまま吐く 等
- **ID_SYNONYMSブリッジ**: wet_chin→[drooling,salivation,dewlap_wetness,facial_wetness]、
  vocalization_changes→[vocalization,screaming,...]、dark_urine→[red_urine,blood_in_urine]、
  inability_to_perch→[difficulty_perching,falling_off_perch,leg_weakness]、
  jaw_chattering→[difficulty_eating,drooling,mouth_pain]

### UX: クイック入力の拡充（新規対応主訴の1タップ導線）
- 犬「食べた後すぐに未消化のまま吐く」、猫「トイレ以外の場所で粗相する」「口をくちゃくちゃさせる」、
  ウサギ「あごが濡れている」、フェレット「足を伸ばして硬直する」（ミラーテスト JA_QUICK 同期済み）

### 回帰テスト（+19件）
- チャット: TestChatClinicalAccuracyAuditRound13（12件 — 否定ガード両経路+正常系不変、吐出→巨大食道、
  褐色尿→溶血、猫粗相/くちゃくちゃ、ウサギ流涎/眼球突出、モルモット斜頸、鳥握力、フェレット発作→
  インスリノーマ、キーキー鳴く誤マッピング再発防止、魚鰓/ヘビ腹側発赤）
- 薬品: test_sweep15（商品名括弧バグ+表記ゆれ5ケース+精度ガード3）、TestBatch46（5件 — 4剤の存在・
  用量・定義的安全事実、救急リンク解決率≥90%+複合名着地+血液製剤の非リンク維持）
- UX: test_app_js_emergency_key_drugs_are_linkified（レンダラー+CSS+非解決行のフォールバック）

### 表示数値の同期・キャッシュ
- `setDefaultStats()`: dog 586/cat 565/ferret 207/sugar_glider 76薬品、pendingStats drugs 647→**651**・
  symptoms 70→**72**
- ServiceWorker: `CACHE_NAME` v131 → **v132**（第24/25弾との同版衝突のため2回改番）

## 2026-08セッション（第27弾: 薬品重複カード56件の統合 + referenced-but-absent 6剤 + チャット精度第15弾）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **4,045件合格**（34 skip）
- 配信SQLiteクリーンビルド: 6,892疾患、treatment/prevention/prognosis **100%**、主要臨床フィールド空欄 **0**
- 薬用量: safe薬品の dosage 欠落 **0**（全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- prevalence dead key: **9**（当該種DBに疾患自体が無い既知残、上限15ガード内）

### 薬品重複カード56件の統合（651→601薬品 — 疾患T103と同型の重複解消・第2弾）
括弧サフィックス（商品名・化学同義語・薬剤自体と同一の剤形記述）だけが違う同一薬の
重複カードを監査で56件検出し、`_DRUG_CURATED_MERGE` を1件（ガバペンチン）→53グループに拡張:
- **純粋な商品名違い**: Spironolactone / (Aldactone)、Clopidogrel / (Plavix)、Pergolide / (Prascend)、
  Toceranib / Phosphate / (Palladia) Oral、Budesonide / (Entocort) 等
- **化学同義語**: Calcitriol と「Calcitriol (1,25-Dihydroxyvitamin D3)」（=同一薬の2枚目カード。
  **別薬のコレカルシフェロールは独立エントリのまま維持**）、SAMe 2枚、シリマリン 2枚、
  Vitamin B12 (Cobalamin) と Cobalamin Injectable（SC用量同一）、PGF2α と Dinoprost（用量同一）
- **適応名分割**: ベナゼプリル4枚（Fortekor/猫CKD/腎保護/フィラリアPH — 同一用量帯）等
- **統合規則**（既存の安全規則に準拠）: 正規側（種数最多）の用量は**絶対に上書きしない**。
  変種からは欠落種のみ取り込み（例: calcitriol が爬虫類カバレッジを獲得）。旧IDは
  `_DRUG_ALIAS_TO_ID` で解決（ブックマーク・ナビゲーション維持）、商品名検索も維持
  （アルダクトン→spironolactone 等を検証）
- **意図的に統合しないもの**（用量が本質的に異なる変種、コメントで文書化）:
  maropitant_travel（酔い止め8 mg/kg≠制吐2 mg/kg）、chlorambucil_low_dose（メトロノミック）、
  piroxicam_bladder（TCCプロトコル）、diltiazem_oral（徐放）、melatonin_implant、
  calcium_gluconate_oral（経口≠IV）、lidocaine_systemic、TXA topical/IV、heparin_laminitis、
  prednisolone_lymphoma、tramadol_lactation 等
- **ドンペリドンの正準名タイポ修正**: name_ja「ドメペリドン」→ 標準カナ「**ドンペリドン**」
  （INN標準表記）。旧表記はエイリアスで解決維持（馬乳汁分泌不全テキストの9参照）

### referenced-but-absent 薬品6剤の補完（`drug_batch_47.py` 新規、+6剤）
用量文脈カタカナトークン監査（第16回スイープ）で、治療テキストが用量付きで指示するのに
未収載だった6剤を検出・補完:
- **ハロペリドール**（17参照）— 鳥の難治性羽毛破壊行動・自咬症 0.1-0.2 mg/kg PO q12-24h
  （Carpenter 6th; Iglauer & Rasim 1993）。バタン類は低用量開始。犬は safe:False（現行行動学に適応なし）
- **アトバコン**（12参照）— **自サイトのキュレート済みプロトコル（B. gibsoni: アトバコン+アジスロ、
  Cytauxzoon: Cohn 2011 生存率60%）が名指しする第一選択なのに未収載だった**。
  脂肪食との同時投与必須（空腹時投与=治療失敗の代表的原因）・M121I耐性を明記
- **プリマキン**（20参照）— 鳥マラリア組織型/ガメトサイト + **猫バベシア唯一の有効薬**。
  猫の致死量（約1 mg/kg）が治療量（0.5 mg/kg）のわずか2倍という**猫の抗原虫薬で最狭の治療域**を
  用量・禁忌の両方に明記
- **クロロキン**（20参照）— 鳥マラリア赤内型第一選択（25→15 mg/kg at 12/24/48h、プリマキン併用必須）
- **ナルトレキソン**（9参照）— 肢端舐性皮膚炎・毛引き・馬自傷のオピオイド拮抗補助
  （White 1990 JAVMA; Dodman 1987/1988）。**オピオイド鎮痛薬を無効化**する相互作用を major で明記
- **ブチルスコポラミン（ブスコパン）**（10参照）— 馬の痙攣性疝痛・チョークのFDA承認鎮痙薬
  0.3 mg/kg 緩徐IV。**投与前の心拍数記録必須**（一過性頻脈が疝痛重症度指標をマスク）・
  効果消失後の疼痛再燃は外科的病変を示唆、を明記（Plumb's 10th; Reed & Bayly 4th）

### 表記ゆれエイリアス（sweep #16、約200参照がチップ化）
- プラジクアンテル（25参照、正準はプラジカンテル）、ミルクシスル（19）、トコフェロール（20）、
  アスコルビン酸（9）、ロイプロリド（20）/リュープロライド（4）、流動パラフィン（16）/
  パラフィンオイル（11、括弧内漢字混じりで tier-4 索引対象外だった）、パモ酸ピランテル（10、語順逆転）/
  ピランテル（裸名）、硫酸鉄（20、正準は硫酸第一鉄）
- **索引の3文字漢字許可**: 全漢字3文字（「硫酸鉄」）はラテン4文字以上と同等に特異的なため、
  キュレート済みエイリアスに限り長さ制限を緩和

### 診断チャット精度 第15弾（20症例フレッシュスイープ 8 MISS → 全症例合格）
- **辞書形・連用形エイリアスギャップ**: 「関節が腫れる」（てる/て形のみ収載 — モルモット壊血病の
  教科書的主訴が抽出不能）、「口の中が赤く」「チーズ状のもの」（ヘビ・マウスロット）、
  「便に血が混じる/お尻から血」（血便系）、「骨が弱い/もろい」（フクロモモンガMBD）
- **フェレット黒色便ブリッジ**: 飼い主は鮮血便と黒色便を区別できないのに、胃潰瘍
  （black_tarry_stool/tarry_stool）が「血便」主訴でマッチせず**エストロゲン性骨髄抑制・
  妊娠毒血症が血便+元気消失の上位を占めていた** → _SYN に bloody_stool→black_tarry_stool等の
  ブリッジ + ferret prevalence 6キー追加（Gastric Ulcer=common、H. mustelae潰瘍=common、
  Ibuprofen Toxicosis/Pregnancy Toxemia/Parvovirus Enteritis=rare）→ GI鑑別がtop5独占
- **擬音語**: 「呼吸のたびにプチプチ音」→clicking_breathing_sounds（鳥の気嚢ダニ/アスペルギルス）
- **サワークロップ**: 「そのうから酸っぱい臭い」→sour_crop_odor 新設（bird専用ID、
  parrot/parakeet は ID_SYNONYMS で crop_stasis/crop_distension にフォールバック）
- **犬の整形外科主訴**: 「階段を上れない」「後ろ足が震える」が抽出不能で
  「散歩を嫌がる+階段+後ろ足が震える」の典型的OA主訴がてんかん1位だった →
  階段系→stiffness、後ろ足が震える→hind_leg_weakness（「足が震え」→tremorsより長い最長一致）
  → 膝蓋骨脱臼/OA/椎間板ヘルニアがtop3
- **馬タイイングアップ**: 「後肢が突っ張って歩く 運動後に尿が茶色い」が抽出ゼロ →
  突っ張っ→body_stiffness、尿が茶色/コーラ色の尿→body_dark_urine（語順ゆれ）→
  横紋筋融解症ファミリーがtop4独占（労作後ミオグロビン尿の教科書的ペア — Reed & Bayly 4th）
- 回帰テスト: `TestChatClinicalAccuracyAuditRound15`（10件）

### UX: クイック入力の拡充 + 新規薬品の双方向動線検証
- クイック入力に新規対応主訴を追加: 馬「後肢が突っ張って歩き尿が茶色い」（タイイングアップ）、
  モルモット「関節が腫れる」（壊血病）、フェレット「便に血が混じる」— ミラーテスト JA_QUICK 同期
- 新規6剤の動線を検証: 疾患→薬品チップ（治療テキスト解決）と薬品→「この薬品を使う疾患」
  逆引き（アトバコン12疾患・ブスコパン15疾患・ハロペリドール24疾患等）の双方向を確認 —
  鑑別診断結果・チャット候補カードから1タップ到達

### 表示数値の同期・キャッシュ
- `setDefaultStats()` 全21種の薬品数を統合後実測に同期（dog 545, cat 529, horse 347 等）、
  pendingStats drugs 651→**601**（静的コピー「600+薬品」は据え置きで整合）
- ServiceWorker: `CACHE_NAME` v132 → **v133**

### テスト・CI
- フルテストスイート合格（+13新規回帰テスト: batch47/エイリアス6 + 統合4 + チャット10 + 既存1調整）
- ruff check: repo全体 clean、変更ファイル format 済み
- 配信DB: クリーンビルドで 6,892疾患・**601薬品**、treatment/prevention/prognosis 100%

## 2026-08セッション（第28弾: イソクスプリン/ビスマス/ビオチン補完 + チャット精度第15弾 + 疾患DB詳細に麻酔注意ボックス）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **4,045件合格**（34 skip）
- 配信SQLiteクリーンビルド: 6,892疾患、主要臨床フィールド（治療/病因/予後/予防/説明/病態）の空欄 **0**
- 薬用量: safe薬品の dosage 欠落 **0**（651薬品時点、species_info 3,802エントリ全数検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**
- prevalence dead key: **9**（当該種DBに疾患自体が無い既知残、上限15ガード内）
- 初回フルランの1失敗（test_chelonian_and_jp_antiparasitics）は並行 migrate_to_sqlite との既知のレース — 単独再実行で合格

### referenced-but-absent 薬品3剤の補完（並行セッションが47枠を先取したため `drug_batch_48.py` として収載）
用量文脈カタカナトークン監査（第16回スイープ、find_drugs_in_text 実マッチャー突合）で検出:
- **イソクスプリン** — 馬蹄舟骨症候群2エントリが「0.6 mg/kg PO q12h（末梢血管拡張）」で参照する古典的血管拡張薬
  （Rose 1983 EVJ）。経口BA不良でエビデンス限定的（Erkert 2002）・装蹄矯正+NSAIDsが第一選択・
  FEI/競馬禁止薬物を明記。犬 safe:False
- **次サリチル酸ビスマス（ペプトビスモル）** — フェレット/ハムスターHelicobacter三剤併用の第三の柱
  （17.5 mg/kg PO q8h ×14日、Quesenberry & Carpenter 4th; Marini 1999）が7参照なのに未収載。
  **猫 safe:False**（サリチル酸グルクロン酸抱合能低下 — アスピリン中毒と同一機序）、糞便黒色化=メレナ誤認・
  X線不透過・テトラサイクリン/キノロンのキレート相互作用（2時間間隔）を明記
- **ビオチン（ビタミンB7）** — 28参照（馬蹄質改善 15-25 mg/日 Josseck/Zenker 1995 EVJ ×6-9ヶ月継続、
  犬被毛サプリ、爬虫類の生卵白アビジン欠乏症）。ビタミンB12との数字境界ガードを検証
- bare「ビスマス」エイリアス追加（フェレット胃潰瘍の裸表記を解決）。3剤とも治療チップ・逆引き
  「この薬品を使う疾患」（isoxsuprine 2/bismuth 24/biotin 30疾患）双方の導線を検証済み

### 診断チャット精度 第15弾（22症例フレッシュスイープ 8 MISS → 全症例合格）
- **急性後肢不全**: 「後ろ足が立たなくなった」が legacy 犬パスで抽出ゼロ（hind_limb_paralysis の legacy
  fallback 欠落）→ _LEGACY_FALLBACK に paralysis/limping 追加 + 変化形エイリアス3種
  （立たなく/で立てなく/で立てない）→ IVDD/変性性脊髄症/ウォブラーが top-3
- **いびき語彙が全パスに皆無**: BOAS の代表的主訴なのに legacy 犬 DB に snoring が無く、「いびきがひどい」
  抽出ゼロで短頭種気道症候群が自身の主訴でランクインしなかった → legacy 語彙に snoring 追加（73→74症状）+
  BOAS 症状セット + 「いびき」「すぐばてる」「暑さに弱い」エイリアス + ID_SYNONYMS
  snoring→noisy_breathing/wheezing（「ガーガー」は気管虚脱のガチョウ様咳として coughing を維持）
- **白猫の耳介先端SCC**: 「耳の先にかさぶたができて治らない」抽出ゼロ → ear_tip_lesions /
  non_healing_wound エイリアス4種 → 皮膚扁平上皮癌/ボーエン病が top-2
- **瞳孔不同**: 「片方の瞳孔だけ大きさが違う」抽出ゼロ → dilated_pupils エイリアス4種 →
  網膜剥離/高血圧性網膜症が top-3
- **ウサギ後肢麻痺**: 「後ろ足を引きずって立てない」が lameness のみ → て形エイリアス + ID_SYNONYMS
  hind_limb_paralysis 系ブリッジ → 後肢不全麻痺/脊髄圧迫/脊椎亜脱臼が top-4
- **爬虫類ラバージョー**: 「あごが柔らかくてぶよぶよ」（かな表記）が抽出ゼロ → jaw_softening エイリアス3種 +
  ID_SYNONYMS → トカゲMBDが rank 1
- **フェレット腹水**: 「お腹がパンパンに膨れている」が「パンパンに膨れている」→edema の最長一致に負けて
  腹部文脈消失 → 11文字キー「お腹がパンパンに膨れて」→bloating で腹部文脈を確実に勝たせる → 心筋症 top-5
- **ヘビ食後吐出**: 「吐き戻す」動詞形が皆無 + 「吐き戻し」→vomiting 誤マッピング → regurgitation に是正
  （legacy fallback regurgitation→vomiting と ID_SYNONYMS で他種は不変 — 鳥クロップ疾患の回帰テストで固定）
  → 吐出症候群/クリプトスポリジウム症が top-4
- 回帰テスト: `TestChatClinicalAccuracyAuditRound15`（9件）+ `TestBatch48IsoxsuprineBismuthBiotin`（5件）

### UX: 疾患DB詳細パネルに麻酔注意ボックス（チェッカー結果とのパリティ）
- 「🏥 この疾患の麻酔注意事項」ボックス（禁忌薬品のワンタップリンク + 種別麻酔プロトコルへのジャンプ付き）は
  **チェッカー結果カードのみ**に表示され、疾患DBで拡張型心筋症を開いた獣医師にはα2作動薬禁忌が出なかった →
  DB詳細テンプレートに `anes-considerations-slot` プレースホルダを追加し、`toggleDbItem` 展開時に
  `hydrateAnesthesiaConsiderations()` で遅延ハイドレート（fetch-once の ensureAnesthesiaContraRules を
  起動、ルール未着時は短時間ポーリング）。リンクは既存の委譲ハンドラ（drug-nav-link/anesthesia-nav-link）で
  完全一致着地
- 回帰テスト: `test_app_js_disease_db_detail_surfaces_anesthesia_considerations`

### UX: クイック入力の拡充（新規対応主訴の1タップ導線）
- 犬「いびきがひどく呼吸がガーガー鳴る」（→短頭種気道症候群）、猫「耳の先にかさぶたができて治らない」
  （→扁平上皮癌の早期発見導線）。ミラーテスト JA_QUICK 同期済み

### 表示数値の同期・キャッシュ（第27弾マージ後の実測に同期）
- `setDefaultStats()`: dog 548/cat 530/horse 349/ferret 195/reptile 101/tortoise 108/snake 107/lizard 103薬品、
  pendingStats drugs **604**（第27弾dedup後601+本セッション3剤）・symptoms 73→**74**
- ServiceWorker: `CACHE_NAME` v133 → **v134**（両セッションが v133 を使用したため改番）

### テスト・CI
- フルテストスイート: **4,060件合格**（34 skip、+15新規回帰テスト）、ruff check/format clean
- 配信DB: クリーンビルドで 6,892疾患・**654薬品**、treatment/prevention/prognosis 100%

## 2026-08セッション（第27弾・並行セッション分: 薬品重複カード4組の統合 + referenced-but-absent 4剤 + チャット精度第15弾 + チェッカー0件時のチャット動線）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **4,045件合格**（34 skip）
- 配信SQLiteクリーンビルド: 6,892疾患、treatment/prevention/prognosis **100%**、主要臨床フィールド空欄 **0**
- 薬用量: safe薬品の dosage 欠落 **0**（651薬品、全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- prevalence dead key: **9**（当該種DBに疾患自体が無い既知残、上限15ガード内）

### 薬品辞書: 表示同一の重複カード4組を統合（`_DRUG_CURATED_MERGE` 拡張）
基底名重複監査（括弧サフィックス除去後の name/name_ja 照合）で、括弧バリアントで用途が区別される
意図的な分割（meloxicam_exotic 等 60組）とは別に、**表示がほぼ同一で内容が片方のサブセット**の
真の重複カード4組を検出・統合（既存の非破壊マージ機構を使用、旧IDは aliases に保存され検索・
ナビゲーションは維持）:
- **hydrocodone ← hydrocodone_antitussive**（両方 name_ja「ヒドロコドン」で2枚の同名カード。
  正規側は猫の安全注記=オピオイド興奮のためブトルファノール代替を保持）
- **milk_thistle ← silymarin**（シリマリン 6種収載 ⊃ 犬猫のみ）
- **same ← s_adenosylmethionine**（SAMe 4種収載 ⊃ 犬猫のみ）
- **calcitriol ← vitamin_d3**（両entry とも活性型VitD3の ng/kg 用量であることを確認済み —
  爬虫類行は「UVB第一選択」注記のみでコレカルシフェロール用量の混入なし。爬虫類・リクガメ等
  6種の行が正規サイドに統合）

### referenced-but-absent 薬品4剤の補完（`drug_batch_47.py` 新規、統合4減+新規4増=651維持）
用量文脈付き薬品接尾辞トークン監査（第16回スイープ、find_drugs_in_text 実マッチャー突合）で検出:
- **メマンチン** — 犬強迫性障害エントリが「0.3-0.5 mg/kg PO q12h — NMDA拮抗薬」と用量指示するのに
  NMDA拮抗薬が皆無だった（Schneider 2009 J Vet Behav: 11/11頭改善）。CDS補助にも同用量
- **プロカルバジン** — MUO/GMEレスキュー「25-50 mg/m² PO q24h」（Coates & Jeffery 2014）と
  リンパ腫再発MOPPの「P」（Northrup 2009）。BBB通過細胞傷害薬が辞書に無かった。
  骨髄抑制ナディア2-3週・出血性胃腸炎・細胞傷害性取扱を明記
- **フェニトイン** — ジギタリス中毒性心室性不整脈の古典的選択薬 5-10 mg/kg 緩徐IV（リドカイン
  不応例、Plumb's 10th）。**猫は safe:False**（半減期24-108hの蓄積肝毒性・血小板減少）
- **ビオチン** — 馬蹄角質の質改善 15-20 mg/頭/日（Josseck 1995 Equine Vet J 対照試験、
  新生角質伸長まで6-9ヶ月継続）・鳥の羽毛/嘴角質障害 0.5-1.0 mg/kg（生卵白アビジン排除を明記）
- **表記ゆれエイリアス**: メタドン→methadone（正準メサドン）、ハイドロコドン→hydrocodone
  （正準ヒドロコドン）、SSDクリーム→silver_sulfadiazine、Ca-EDTA（ハイフン形）→calcium_edta

### 診断チャット精度 第15弾（18症例フレッシュスイープ 6 MISS → 全症例合格）
- **犬レガシーDBに口腔内腫瘍を新設**（79→80疾患、73→74症状）: 「口の中にできものがある 口臭」が
  **乳腺腫瘍1位**だった（口腔腫瘤語彙もエントリも皆無）。oral_mass 症状 + oral_tumor エントリ
  （メラノーマ=悪性最多/エプリス/SCC、common、チャウチャウ2.0×等、Withrow & MacEwen 6th）+
  単独パトグノモニック・クラスタ {oral_mass}→×1.6（口腔内の腫瘤は部位診断的 — 乳腺/皮膚腫瘤は
  鑑別に入らない）→ rank 1。乳腺主訴の順位は不変を回帰テストで固定
- **犬チェックボックス/問診経路にもパリティ**: dog_diseases モジュールに oral_mass/bad_breath
  語彙を追加（65→67症状）、Oral Melanoma/Epulis/Oral Papillomatosis/Periodontal Disease の
  症状セットに付与 → チェックボックスで口腔メラノーマ rank 1
- **クッシング三徴の連用形取りこぼし**: 「水をたくさん飲んで」（〜飲む形のみ収載）
  「お腹だけ膨れてきた」（助詞「だけ」で不一致）→ エイリアス追加で3/3抽出 → クッシング rank 1
- **馬の後肢跛行口語が皆無**: 「後ろ足を痛がる 蹄が熱い」が**抽出ゼロ**だった → 後ろ足を痛がる/
  かばう/引きずる→limb_lameness_hind 等6エイリアス + **症候群ペアブースト**
  {hoof_heat, limb_lameness_hind}→蹄膿瘍×1.5（急性跛行+局所蹄熱感は蹄膿瘍 until proven
  otherwise — Adams & Stashak 7th。馬の急性重度跛行の最多原因）→ 蹄膿瘍 rank 1
- **猫の成猫黄疸を新生児溶血が乗っ取り**: 未ティアの新生子溶血性疾患2エントリ（B型母猫×A型子猫の
  血液型不適合・新生子限定）が「元気がない 白目が黄色い」で1位 → rare tier 付与 + 
  「おしっこの色が濃い」→dark_urine エイリアス → IMHA/肝溶血群が上位
- **ウサギ眼球突出のて形**: 「目が飛び出してきて」（〜てきた形のみ収載）→ エイリアス追加。
  加えて**エロドントーマ=rare**（デグー/プレーリードッグの疾患でウサギでは稀 — Capello & Lennox）
  **球後膿瘍（歯科由来）=common**（Harcourt-Brown）の有病率是正 → 稀な歯牙腫瘍の1位を解消
- **鳥の疥癬（クヌドコプテス）語彙が皆無**: 「脚に白いかさぶた ガサガサ」が抽出ゼロ →
  脚に白いかさぶた/脚がガサガサ等5エイリアス→crusty_lesions_on_legs + _ID_SYNONYMS ブリッジ
  （インコは leg_scales/scaly_face 表記）→ bird/parakeet とも疥癬ダニ症 rank 1

### UX: チェッカー0件時のデッドエンド解消（鑑別⇄相談チャットの動線完成）
- 「該当する疾患が見つかりませんでした」の空状態は改善ヒントのテキストのみで**行き止まり**だった →
  ヒントが推奨する2つの対処をワンタップ化:
  - 「🩺 問診モードで段階的に絞り込む」→ chat ビュー + guided モード起動
  - 「💬 相談チャットで自由入力で相談する」→ chat ビュー + free モード + **選択済み症状名を
    チャット入力欄にプリフィル**（530+口語エイリアスがチェックボックス語彙で表現できない
    言い回しを解釈する — ユーザーは打ち直しでなく言い換えから始められる）
  - GA4: `guided_from_checker_empty` / `chat_from_checker_empty`
- クイック入力ボタン追加: 犬「口の中にできものがある」・馬「後ろ足を痛がる」・鳥「脚に白いかさぶた」
  （全て抽出保証済み、ミラーテスト JA_QUICK 同期）

### 回帰テスト（+14件）
- 薬品: TestBatch47AndSweep16（5件 — 4剤の存在・完全バイリンガル用量・猫フェニトイン safe:False・
  プロカルバジンMUO/MOPPレジメン・重複統合の維持とcalcitriol爬虫類行・エイリアス7ケース解決）
- チャット: TestChatClinicalAccuracyAuditRound15（8件 — クッシング三徴/口腔腫瘍rank1/乳腺ガード/
  チェックボックスパリティ/馬蹄膿瘍/猫NI降格/ウサギ・エロドントーマ降格/鳥疥癬rank1）
- UX: test_app_js_checker_zero_results_pivot_to_guided_and_chat（空状態ピボット+プリフィル配線）

### 表示数値の同期・キャッシュ
- `setDefaultStats()`: horse 361→362薬品、pendingStats symptoms 73→**74**（oral_mass追加）
- ServiceWorker: `CACHE_NAME` v132 → **v133**
- 再現手順: `migrate_to_sqlite.py` → `build_disease_search_index.py`（名前不変のためno-op）

### mainの並行第27弾（56件dedup+6剤）とのマージ統合
- 本セッションのbatch_47はmainの並行セッションが先にスロットを取得したため **batch_49に改番**
  （メマンチン/プロカルバジン/フェニトインの3剤。ビオチンはmainのbatch_48が収載済みのため削除）
- 重複カード統合4組（hydrocodone/シリマリン/SAMe/カルシトリオール）はmainの56件統合に**全て包含**
  されていたため、mainの `_DRUG_CURATED_MERGE` をそのまま採用
- テストクラス改名: TestBatch47AndSweep16→TestBatch49AndSweep16Parallel、
  TestChatClinicalAccuracyAuditRound15（衝突）→Round16Parallel、レガシー犬DBは両セッション合算で
  **80疾患・75症状**（+oral_mass/oral_tumor 本セッション、+snoring/BOAS系 main）
- ServiceWorker: v133/v134 衝突 → **v135** に改番、setDefaultStats/pendingStats はマージ後実測
  （**607薬品**）に同期

### 第2回マージ統合（mainの第29弾: 5-FU=batch_49 と再衝突）
- 本セッションの3剤は **batch_50 に再改番**（47/48/49全てが並行セッションで使用済み）
- SW: v135同版衝突 → **v136**、pendingStats はマージ後実測 **608薬品** に同期

## 2026-08セッション（第29弾: 相互作用スキーマ破損の修正 + 5-FU補完 + 硫酸鉄/生食エイリアス + チャット精度第17弾 + 疾患DBパネルの麻酔注意事項）
（第27/28弾と並行実施。batch番号47→49、チャット監査回番号15→17、SW版数はマージ時に改番）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **4,045件合格**（34 skip、並行セッション前の基準）
- 配信SQLiteクリーンビルド: 6,892疾患、treatment/prevention/prognosis **100%**、主要臨床フィールド空欄 **0**
- 薬用量: safe薬品の dosage 欠落 **0** ／ 麻酔: 全21種×全8カテゴリ完備、薬剤行の dose 欠落 **0**
- prevalence dead key: **9**（既知残、上限15ガード内）

### 相互作用スキーマ破損の修正（ユーザー可視の表示バグ）
- **バグ**: batch 40 の `ethambutol` と `dihydrostreptomycin` が `drug_interactions` を**プレーン文字列**で
  持っていた。フロントの `renderDrugInteractionsList` は配列前提でスプレッドするため、**文字列が1文字ずつ
  展開され、約130個の壊れた1文字相互作用バッジ**が両薬品の詳細に表示されていた
- 構造化リスト（drug/effect/effect_ja/severity）に変換。DHS のループ利尿薬×耳毒性は major、
  NSAIDs/AmB/シスプラチンの腎毒性相加も major に明記（既収載の各薬品へ自動リンク）
- 回帰テスト: `test_no_drug_has_string_typed_interactions` — 全薬品のスキーマをrepo-wideでガード

### referenced-but-absent 薬品1剤の補完（`drug_batch_49.py` 新規 — 47/48は並行セッションが使用）
- **フルオロウラシル（5-FU）** — 馬サルコイド・耳介プラーク・皮膚/眼SCCプロトコル11参照
  （開発者専門種のフラグシップ治療）が「5-FU局所」「局所5-FU軟膏」を名指しするのに未収載。
  外用5%クリーム（Fortier 1994）・腫瘍内50 mg/mL（Stewart 2006 JAVMA: 61.5%消退）、
  犬全身150 mg/m2 IV週1（Withrow & Vail 6th）。**猫は経路を問わず致死的（safe:False、
  Dorman 1990: 生存例なし）**、飼い主のエフディックス誤摂取＝犬猫の有名な致死中毒を明記
- **硫酸鉄は重複追加を回避**: 監査で「絶対」と思われた欠落は既存 `ferrous_sulfate_oral`
  （名称=硫酸第一鉄）のエイリアス欠落と判明 → search_aliases（硫酸鉄等）+ 馬（**静注鉄は致死的
  アナフィラキシー様反応で禁止**・新生子馬不可）・フェレット行を batch_21 に追加

### 薬品マッチャー: 純漢字ショートエイリアス + 負文脈ガード（新機構）
- エイリアス索引の `len ≥ 4` フィルタが**純漢字の複合語**（硫酸鉄=3字、生食=2字）を黙って
  落としていた → 純漢字エイリアスは2字から索引（並行セッションの「3字ちょうど」条件を≥2字に一般化。
  カタカナ/Latin は部分文字列誤爆リスクがあるため4字のまま）
- **生食**（生理食塩水の臨床略記、437治療文で使用）が解決可能に。ただし「ガス**産生食**物」
  （鼓脹症の食事指導）に誤爆することをレビューで発見 → `_KEYWORD_NEGATIVE_CONTEXTS`
  （キーワード単位の負文脈: 産生食/生食物/生食用）を新設し、負文脈内の出現のみの場合は
  チップ化しない（数字境界ガードと同型の機構）

### 診断チャット精度 第17弾（40症例フレッシュスイープ → 全症例合格）
- **犬クッシング主訴が抽出ゼロだった**: 「水をたくさん飲んでおしっこも多い お腹だけ膨れてきた
  毛が左右対称に薄い」— 4フレーズ全てが既存エイリアスの僅かな変化形（飲んで/も多い/だけ膨れて/
  に薄い）で不一致 → 4エイリアス追加でクッシング rank 1
- **犬外耳炎**: 「耳から悪臭」「茶色い耳垢」が未収載で耳血腫が1位だった → 追加で外耳炎 rank 1
- **セキセイ疥癬ダニ（Knemidokoptes/scaly face）**: セキセイの代表的皮膚疾患なのに飼い主表現
  （くちばしの周りにかさぶた・白い粉をふいた）が皆無で線維腫が1位だった → エイリアス6種 +
  ID_SYNONYMS（crusty_beak/scaly_face → bird系 crusty_lesions_on_face フォールバック）で
  疥癬群が top 独占（parakeet/bird 両方）
- **ウサギ・ソアホック連用形**: 「足の裏が赤く腫れて」が不一致（〜赤い/〜腫れてる のみ収載）→
  潰瘍性足底皮膚炎 rank 1
- **猫ノトエドレス**: 「耳の先が黒いかさぶた」（黒い形・かさぶた形）→ crusting 抽出
- **馬「足を引きずる」が equine エイリアスに無かった**（犬猫用 lameness 側のみ）→ 追加

### 馬・熱蹄鑑別の是正（開発者専門種）
- **深趾屈腱炎（DDFT）が所見2個 [前肢跛行, 蹄熱感] のみで、この2所見の全入力に対し
  カバレッジ1.0＝87.5%で常勝**していた（蹄膿瘍・蹄葉炎という圧倒的高頻度ddxを恒常的に抑圧）
- DDFT自身の clinical_signs_detail が挙げる**冠部拍動亢進・屈曲試験陽性**を所見セットに反映
  （Adams & Stashak 7th ed）→ 過剰カバレッジを解消
- **蹄膿瘍を hot-hoof ペアブーストに追加**: {蹄熱感+前肢跛行}/{蹄熱感+指動脈拍動} →
  Laminitis/Acute Laminitis/**Hoof Abscess** ×1.5（急性跛行+熱蹄は膿瘍か蹄葉炎 until proven
  otherwise — 膿瘍は実臨床で急性重度跛行の最多原因）
- 修正後: 2所見では膿瘍・蹄葉炎を含む正直な足部鑑別リスト（独走なし）、+指動脈拍動で
  蹄葉炎97%・膿瘍78%が上位

### UX: 疾患DBパネルの麻酔注意事項（並行セッション第28弾と同一機能を独立実装 → マージで統合）
- 実装は第28弾の `.anes-considerations-slot` + ポーリング型ハイドレータを採用。本セッション分は
  `ensureAnesthesiaContraRules` の **promise返却（メモ化）** 化と `loadDiseaseDb` プリフェッチ
  （初回展開から即時表示）を寄与。回帰テスト
  `test_app_js_contra_rules_loader_is_promise_returning_and_prewarmed` を追加

### 薬用量ローカライザの全角括弧リークバグ修正（副産物）
- 「q24h（Carpenter）」のように**全角括弧の引用が頻度略号に密着**すると、数値保持パス
  （digit-containing token は改変しない）を通って英語の頻度略号が日本語出力に漏れることを
  新規フェレット鉄剤行の統合テストで検出 → 全角括弧を独立トークン化（括弧内の未知語が
  fail-closed を正しく発火、既存の変換済み文字列への影響は実測0件）。回帰テスト+1件

### 動線の確認（新規薬品→鑑別・チャット）
- 馬サルコイドの関連薬品チップ: imiquimod/cisplatin/**fluorouracil** を解決（鑑別診断・チャット
  結果カード・疾患DBの3ビュー共通レンダラー経由で自動到達）
- 犬・慢性疾患性貧血チップ: iron_dextran + **ferrous_sulfate_oral** を解決

### テスト・CI（マージ後）
- ServiceWorker: `CACHE_NAME` v133/v134 → **v135**（並行セッションと同版衝突のため改番）

## 2026-09セッション（第30弾: CBD/トリプトファン/hCG補完 + 相互作用チェッカーの自然言語入力対応 + チャット精度第18弾）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **4,107件合格**（34 skip）
- 配信SQLiteクリーンビルド: 6,892疾患、treatment/prevention/prognosis **100%**、主要臨床フィールド空欄 **0**、キリル文字混入 **0**
- 薬用量: safe薬品の dosage 欠落 **0**（608薬品時点、全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- prevalence dead key: **9**（当該種DBに疾患自体が無い既知残、上限15ガード内）

### referenced-but-absent 薬品3剤の補完（`drug_batch_51.py` 新規、608→611薬品）
用量文脈トークン監査（第17回スイープ、スニペット文脈で find_drugs_in_text 突合）で検出:
- **カンナビジオール（CBD）** — **260参照で最多の欠落**。行動学・OA・難治てんかんエントリが
  「CBD 2 mg/kg PO q12h（McGrath 2019）」等の用量付きで参照するのにECVNスポンサー製品しか無く、
  中立的なモノグラフ（エビデンス用量+CYP450/ALT安全情報）が欠落していた。犬（OA: Gamble 2018 /
  てんかん補助: McGrath 2019 JAVMA RCT 2.5 mg/kg）・猫（Deabold 2019 PK）・馬（FEI禁止物質明記）・
  ウサギ。**鳥・爬虫類は safe:False**（自サイトの行動学コンテンツ自身が非推奨と明記 — データ皆無）。
  フェノバルビタールCYP450相互作用・ALT/ALPモニタリング・THCフリー限定を明記
- **L-トリプトファン** — 行動学49参照のセロトニン前駆体（姉妹サプリのL-テアニン/αカソゼピンは収載済み）。
  DeNapoli 2000 JAVMA。**馬の静注は溶血のため絶対禁止**（Grimmett & Sillence 2005）・
  セレギリン併用のセロトニン症候群リスクを明記
- **hCG（ヒト絨毛性ゴナドトロピン）** — 48参照。小型草食獣の卵巣嚢胞（100 IU/kg IM、
  モルモットの漿液性嚢胞は反応不良でOHEが根治的と明記）・**フェレット発情持続/エストロジェン中毒**
  （100 IU/頭、72時間で外陰退縮確認 — 自サイトの再生不良性貧血エントリが名指し）・
  馬の排卵誘起（1,500-3,000 IU、反復投与での抗hCG抗体形成→デスロレリン代替を明記）
- **エイリアス**: 鉱物油（純漢字3字）→mineral_oil（15参照）、hCG は **case-sensitive キーワード**
  として索引（3文字Latinは通常索引対象外だが、小文字h+大文字CGの混在は自然文に出現しないため精密）。
  bare「ゴナドトロピン」は GnRH（ゴナドトロピン放出ホルモン）誤爆のため不使用
- 動線検証: 逆引き「この薬品を使う疾患」= cannabidiol 50疾患 / l_tryptophan 22 / hcg 46 —
  鑑別診断・チャット候補カードの関連薬品チップと双方向で自動接続

### 相互作用チェッカーの自然言語入力対応 + ワンタップ動線（UX）
- **バグ**: 相互作用チェッカーは「半角英数小文字の drug id」完全一致のみ受け付け、
  「バイトリル」「メロキシカム」のような臨床現場の自然な表記が**全て unknown** になっていた
  （プレースホルダ自体が "meloxicam, prednisolone" と id 入力を要求）
- **バックエンド**: `resolve_drug_reference()` 新設 — id/統合旧id → name/name_ja/括弧前ステム/
  search_aliases（商品名含む）の正規化完全一致（ひらがな・全角半角吸収）→ 一意な部分一致（4文字以上）
  の3段解決。`/api/drugs/check-interactions` が各入力トークンを解決し `resolved`
  （input→id/name/name_ja のマッピング）を返却。「ばいとりる」「メタカム」「ラシックス」
  「クラバモックス」等が全て解決
- **フロントエンド**: クライアント側の小文字/アンダースコア変換（非idを全滅させていた）を廃止し
  生トークンを送信。結果に「認識: バイトリル→エンロフロキサシン」確認行を表示。
  unknown ヒントを「一般名・商品名・日英いずれも可」に更新、プレースホルダを
  「例: バイトリル, メロキシカム」に変更（i18n: interactionInputPh）
- **ワンタップ動線**: 薬品詳細カードに「⚠️ 相互作用チェックに追加」ボタンを新設
  （`.drug-interaction-add`、委譲ハンドラでキャッシュ再描画後も動作）。タップで薬品名を
  チェッカー入力に追加（重複除去）→アコーディオンを開いて着地→2剤以上で自動チェック実行。
  タイピング不要で2枚の薬品カードをタップするだけで併用チェックが完了。
  GA4 `interaction_check_add` イベント。CSS `.drug-interaction-add`（アンバー系）

### 診断チャット精度 第18弾（24症例フレッシュスイープ 4 MISS → 全症例合格）
- **エイリアス誤マッピング修正**: 「便に虫がいる」→ **diarrhea**（爬虫類セクションの粗いプロキシ）に
  誤マッピングされ、正しい短キー「便に虫」→worms_in_stool に最長一致で勝っていた →
  worms_in_stool に是正（爬虫類は ID_SYNONYMS フォールバック鎖 […→diarrhea] で従来どおり安全）。
  「虫が出た」も同様に是正
- **新規エイリアス**: ひも状の虫/ひも状の白い虫/便に白い虫（条虫片節・回虫 — 抽出ゼロだった）、
  腫れもの/腫れ物→lumps_and_bumps、ケージの底でうずくまる→sitting_on_cage_floor、
  うずくまる→hunched_posture、力んで→straining、自分の尾を噛む/尻尾を噛む→tail_chewing、
  回転する動き/同じ動きを繰り返す→circling
- **extractor ID_SYNONYMS 追加**: fur_loss_patches→[hair_loss,…]（「毛が抜けた」（過去形）が
  斑状脱毛IDを持たないハムスター等で脱落していた）、hunched_posture→[abdominal_pain,
  reluctance_to_move, sitting_on_cage_floor, fluffed_feathers, lethargy]（哺乳類の腹痛姿勢と
  鳥のケージ底うずくまりを1つの主訴語で両立）、tail_chewing→[self_mutilation, tail_injury]、
  sitting_on_cage_floor→[fluffed_feathers, lethargy]
- 修正後: 犬「便にひも状の白い虫」→腸管寄生虫症 rank1、ハムスター「体に腫れもの 毛が抜けた」→
  皮膚腫瘤ddx、鳥「産卵後にケージの底でうずくまる 力んでいる」→**卵詰まり rank1**、
  フクロモモンガ「回転する動きを繰り返す 自分の尾を噛む」→自己損傷-尾 rank1。
  ガード検証: ウサギうずくまり→GI stasis rank1 維持・猫「白い米粒」→瓜実条虫 rank1 維持・
  爬虫類の虫目撃→寄生虫ddx維持
- 回帰テスト: `TestChatClinicalAccuracyAuditRound18`（6件）

### 表示数値の同期・キャッシュ
- `setDefaultStats()` 17種の薬品数を実測同期（dog 555, cat 536, horse 354, rabbit 259, 鳥系 234 等）、
  pendingStats drugs 608→**611**
- ServiceWorker: `CACHE_NAME` v136 → **v137**
- 再現手順: `migrate_to_sqlite.py`（611薬品反映。疾患名不変のため検索インデックス no-op）

## 2026-08セッション（第28弾: 犬急性蕁麻疹・血管性浮腫の新設 + オクトレオチド/デコキネート補完 + 連用形スイープ第14弾 + 疾患→緊急対応プロトコル動線）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **4,045件合格**（34 skip）
- 配信SQLiteクリーンビルド: 6,892疾患、treatment/prevention/prognosis **100%**、主要臨床フィールド空欄 **0**
- 薬用量: safe薬品の dosage 欠落 **0**（651薬品時点、全species_info検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり。
  RECOVER準拠用量（エピネフリン低用量0.01・アトロピン0.02-0.04）・猫ALF 5 mg/kg（Tamura 2021）の逸脱なしを再確認
- prevalence dead key: **9**（当該種DBに疾患自体が無い既知残、上限15ガード内）

### referenced-but-absent 薬品2剤の補完（`drug_batch_52.py` 新規 — 並行セッションが47-51を先取したため52に改番）
用量文脈カタカナトークン監査（第16回スイープ、find_drugs_in_text 実マッチャー突合）で検出:
- **オクトレオチド（サンドスタチン）** — ガストリノーマ「1-5 μg/kg SC q8-12h」・インスリノーマ
  「10-50 mcg SC q8-12h」・特発性乳糜胸「10 μg/kg SC q8h」の8+参照なのにソマトスタチンアナログが皆無だった。
  猫先端巨大症には短時間作用型はほぼ無効（Peterson）を dosage 欄に明記（過大評価防止）、
  インスリノーマでの逆説的低血糖リスクを注記（Altschul 1997; Robben 2006 JVIM）
- **デコキネート（デコックス）** — Hepatozoon americanum の ACVIM標準・再発抑制フェーズ
  「TCP 14日→デコキネート 10-20 mg/kg PO q12h 餌混和 2年以上」（Macintire 2001 JAVMA）が参照するのに未収載。
  単独急性期治療ではない（TCP導入が先）を禁忌欄に明記
- 本セッションでも検出したビオチンは並行セッションの batch_48 が先に収載（重複追加を回避）
- **表記ゆれエイリアス2件**: ロイプロリド（ロイ音写、鳥生殖器疾患20参照）→leuprolide、
  Ca-EDTA（ハイフン形、重金属25参照）→calcium_edta
- 逆引き（この薬品を使う疾患）も自動解決を確認: octreotide 11疾患・biotin 30疾患・decoquinate 3疾患

### 新規疾患: 犬「急性蕁麻疹・血管性浮腫」（エビデンスベース、dog module + レガシーチャットDB両対応）
- **ギャップ**: ワクチン接種後・虫刺され後の蕁麻疹/血管性浮腫は犬の最頻出救急皮膚科主訴なのに、
  疾患DBには重症端の「ハチ刺傷アナフィラキシー」しか存在せず、チャットで「顔が腫れてじんましんが出た」が
  眼瞼疾患ばかり上位だった（じんましん/蕁麻疹の語彙自体が皆無）
- **dog module**（619→620疾患、`dog_x9176df51`）: I型過敏反応の病態、ジフェンヒドラミン 2-4 mg/kg ±
  デキサメタゾン、アナフィラキシー進行時エピネフリン 0.01 mg/kg IM エスカレーション、二相性反応の
  12-24時間観察（Shmuel & Cortes JVECC 2013; Ettinger 8th）。id_locks 再生成（+1、append-only）
- **レガシーチャットDB**（79→80疾患、73→75症状）: hives/facial_swelling 症状を新設、
  パトグノモニック・ペア {hives, facial_swelling}→×1.8。**名前はmoduleエントリと整合**
  （「急性蕁麻疹・血管性浮腫（急性アレルギー反応）」）— チャット候補カードの「疾患DBで詳細を開く」
  ピボットが base-name 完全一致で着地
- ID_SYNONYMS: hives→[urticaria, wheals, skin_rashes, skin_lesions, swelling]（種経路フォールバック）
- 配信DB: 6,892 → **6,893疾患**、検索インデックス 6,449→**6,450**

### 診断チャット精度 第14弾（30症例フレッシュスイープ 12 MISS → 実質全合格）
系統的根因: **連用形・語順ゆれ**が substring マッチをすり抜け（「水をたくさん飲んで」vs 飲む、
「後ろ足が動かなくなって」vs なった、「そのうが膨らんで」vs 膨らんでいる、「羽を自分で抜く」語順）:
- **猫ATE救急**: 「急に後ろ足が動かなくなって大声で鳴いている」が抽出ゼロ → 「後ろ足が動かなくな」stem +
  「大声で鳴」→vocalization_changes 追加 → 大動脈血栓塞栓症 rank 1
- **犬OA**: 「散歩を嫌がって階段を登らなくなった 後ろ足が硬い」が抽出ゼロ → 階段回避3形+「足が硬い」→
  stiffness、「散歩を嫌がって」連用形 → 変形性関節症 top-3（階段回避は犬OAの古典的主訴）
- **犬PU/PD多食**: 「水をたくさん飲んでおしっこも多い ご飯も食べるのに痩せる」→ 3ID抽出で糖尿病 top-3
- **猫甲状腺機能亢進**: 「食欲はあるのに痩せ」→increased_appetite → 甲状腺機能亢進症 top-2
- **ハリネズミWHS**: 「後ろ足がふらつ」stem + 「震える」辞書形 → WHS top-3
- **フクロモモンガ自咬**: 「自分のお腹を噛」「自分の体を噛」（部位介在形）→ 自己損傷群 top-3
- **鳥そのう/毛引き**: 「そのうが膨らん」stem・「吐き戻す」・「羽を自分で抜」・「皮膚が見えて」→
  クロップ疾患群/毛引き rank 1
- 回帰テスト: `TestChatClinicalAccuracyAuditRound15`（10件 — 既存Round14と番号衝突のため15に改番）+
  `TestAcuteUrticariaDiseaseEntry`（3件）+ `TestBatch47ReferencedDrugs`（4件）

### UX: 疾患→緊急対応プロトコルのクロスリンク（麻酔連携と対の新動線）
- **ギャップ**: 救急クラスの疾患（GDV・アナフィラキシー・尿道閉塞・熱中症・DKA・子癇・マムシ咬傷等）を
  閲覧しても、対応する緊急対応プロトコルへの動線が無かった（麻酔注意事項リンクは既存なのに）
- `DISEASE_EMERGENCY_MAP`（20エントリ、疾患名正規表現→プロトコルid+種ゲート）を新設。
  **種配列はサーバーデータのサブセットであることをミラーテストで固定**（犬猫用量のプロトコルを
  非対応種に提示しない）
- チェッカー結果カード + 疾患DB詳細パネルに「🚨 この疾患の緊急対応プロトコルを開く」を条件表示。
  `navigateToEmergencyProtocol()` が emergencyデータの readiness poll → フィルタクリア →
  `data-proto-id` 完全一致で該当プロトコルを展開・スクロール（既存 toggleDbItem 再利用）。
  両委譲ハンドラ（チェッカー結果・DBリスト共通）にルーティング追加。GA4 `emergency_from_disease`
- 回帰テスト: `test_app_js_disease_to_emergency_protocol_cross_link` +
  `test_app_js_emergency_map_mirrors_server_protocols`（マップ⇄サーバー同期ガード）

### UX: クイック入力に新規対応主訴を追加
- 犬「顔が腫れてじんましんが出た」「階段を登らなくなった」、猫「急に後ろ足が動かなくなった」（ATE救急）
- ミラーテスト JA_QUICK 同期（全フレーズ抽出保証をCIで維持）

### 表示数値の同期・キャッシュ
- `setDefaultStats()`: dog 602疾患/589薬品・cat 567・horse 362・ferret 208薬品、
  pendingStats diseases 6449→**6450**・drugs 651→**654**・symptoms 73→**75**
- ServiceWorker: `CACHE_NAME` → **v138**（並行セッションと4回衝突のため改番）
- 再現手順: `build_id_locks dog` → `migrate_to_sqlite.py`（クリーンビルド）→ `build_disease_search_index.py`

### mainマージ統合（並行第27弾×2セッションとの衝突解決）
- `drug_batch_47` 衝突: mainの6剤（ハロペリドール等）を採用し、本セッションの2剤
  （オクトレオチド/デコキネート）は **batch_52** に改番（47-51は並行セッションが使用）。ビオチンは mainの batch_48 が
  先に収載していたため重複追加を回避（本文の参照解決は batch_48 で機能）
- `TestChatClinicalAccuracyAuditRound15/17/18` クラス名衝突（3回） → 本セッション分を **Round19** に改番、
  `TestBatch47ReferencedDrugs` → **TestBatch52ReferencedDrugs**
- SYMPTOM_ALIASES 両セッションのユニオン統合。重複キー「吐き戻す」は mainの
  **regurgitation** マッピングを採用（クロップ疾患には臨床的により正確）
- **マージ回帰の検出・修正**: 吐き戻す→regurgitation 化により旧経路
  （vomiting→crop_stasis ブリッジ）が切れ、「そのうが膨らんで吐き戻す」で
  クロップ疾患群がtop8圏外に落ちた → `_SYN` に **crop_distension→crop_stasis/
  crop_swelling/ingluvitis** ブリッジ + regurgitation→crop_stasis を追加
  （甲状腺腫/酸敗嗉嚢が top2 を回復、哺乳類の吐出主訴は不変を検証）
- レガシー犬DB統合後: **76症状**（+hives/facial_swelling/snoring）・**80疾患**

## 2026-09セッション（第31弾: 硫酸マグネシウム全身投与の補完 + チャット精度第19弾 + 馬眼科/神経tierの是正）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **4,140件合格**（34 skip）
- 配信SQLiteクリーンビルド: 6,893疾患、主要臨床フィールド（治療/病因/予後/予防/説明/病態）の空欄 **0**
- 薬用量: safe薬品の dosage 欠落 **0**（613薬品、species_info 3,661エントリ全数検証）
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- 薬品マッチャー飽和度検証: 用量文脈トークン監査の上位候補15フレーズ
  （ノルモソルR 1,089参照・ウルソデオキシコール酸・ミコフェノール酸モフェチル・
  水酸化アルミニウム・ラクツロース・セフタジジム等）を実フレーズで全数突合 — **全て解決済み**

### referenced-but-absent 薬品1剤の補完（`drug_batch_53.py` 新規、613→614薬品）
第19回スイープで、**全身投与用マグネシウム**が唯一の真の欠落と判明（41参照:
MgSO4×18 + MgO×19 + マグネシウム補充×4 が魚用薬浴エントリ「エプソムソルト」にしか解決しなかった）:
- **硫酸マグネシウム（全身投与）** — RECOVER のトルサード/難治性心室細動 30 mg/kg 緩徐IV
  （Fletcher JVECC 2012; Plumb's 10th）、低Mg血症 CRI 0.75-1 mEq/kg/日、
  馬大結腸便秘の浸透圧下剤 0.5-1 g/kg NGT（Reed & Bayly 4th ed、チューブ確認・反復投与時のMg中毒警告）、
  馬グラステタニーの希釈緩徐IV（急速静注=心停止）、ヘッドシェイキング維持 MgO 10-20 g/日、
  鳥卵詰まり併発Mg欠乏 1-5 mg/kg ICe（Carpenter）
- 定義的安全事実: 急速静注禁止・腎排泄（腎不全で減量/回避）・**解毒=グルコン酸カルシウム**・
  Ca含有輸液と同一ライン配合変化・非脱分極性NMBA（アトラクリウム）増強=major
- エイリアス: 硫酸マグネシウム/MgSO4/酸化マグネシウム/マグネシウム補充 → magnesium_sulfate
  （魚用エプソムソルト薬浴は独立エントリのまま温存 — 相互不干渉をテストで固定）
- 動線: 逆引き「この薬品を使う疾患」**50疾患**（馬中毒群・殺鼠剤中毒・心筋挫傷等）、
  相互作用チェッカー自然言語解決、治療チップの双方向を検証済み

### 診断チャット精度 第19弾（25症例フレッシュスイープ 13 MISS → 25/25 合格）
- **失神の飼い主表現が皆無だった**: 「散歩中に急に倒れて意識を失った」が抽出ゼロ →
  倒れて（連用形）/意識を失っ/意識がなくなっ/気を失っ→collapse 追加 → MMVD/大動脈弁下狭窄/DCM がtop3。
  **ガードテストが正しく検出した回帰を是正**: 「痙攣した 意識がなくなった」で心臓性失神がてんかんを
  上回った → てんかんの症状セットに発作時意識消失（ictal collapse=fainting、Ettinger 8th）を追加し、
  痙攣+意識消失→てんかん1位・失神単独→心疾患群の両立を回帰テストで固定
- **GDVに labored_breathing 追加**（横隔膜圧迫性呼吸窮迫 — Ettinger; Monnet 2003）+
  副詞挿入形「お腹が突然/急にパンパン」→bloating（従来は「パンパンに膨れて」→edema に敗北）→ GDV top3
- **慢性アトピー苔癬化の語彙が皆無**: 掻きむしっ/皮膚が黒ずん/皮膚がゴワゴワ/皮膚が厚く →
  itching/skin_thickening（新設ID_SYNONYMS: thickened_skin/skin_rashes、legacy fallback）→ 毛包虫/膿皮/アトピー top3
- **多飲の「量が増えた」形＋被毛粗剛**: 水を飲む量が増え/飲水量が増え→excessive_thirst、
  毛づやが悪/毛艶が悪/毛並みが悪→poor_coat（ID_SYNONYMS拡張: greasy_coat/unkempt_coat）→ 猫CKD/甲状腺 top3
- **前庭疾患の「頭が」形**: 頭が傾い→head_tilt、目が回っ→nystagmus、グルグル回る（カタカナ）→circling
  → ウサギ前庭疾患/斜頸/E.cuniculi top3
- **甲羅軟化の漢字形**: 甲羅が柔らか→soft_shell、甲羅が凹/へこ→shell_deformity → リクガメMBD群 top3
- **腹腔内腫瘤の触知**: お腹にしこり/お腹を触るとしこり→abdominal_masses（新設ID_SYNONYMS）+
  痩せてきて（て形）→weight_loss → フェレット・リンパ腫/腎細胞癌 top3
- **鳥**: 便が水っぽ/水っぽい便→diarrhea + **家禽病原体の tier 是正**（ORT感染症/ORT肺炎/
  鳥メタニューモウイルス感染症/鼻気管炎=rare — ペットバードでは実質不在なのに未tierで
  副鼻腔炎(common)を抑えていた）→ くしゃみ+鼻水で副鼻腔炎 rank1
- **馬エイリアス**（EQUINE_SYMPTOM_ALIASES）: 皮膚にしこり/しこりが多数/イボ状のできもの→skin_sarcoid、
  皮膚にボコボコ/じんましん→skin_hives、目を細め/まぶしそう/まぶしがる→eye_squinting、涙が多い→eye_tearing、
  振り回すように歩/ふらついて歩→neuro_ataxia → サルコイド rank1（蕁麻疹・メラノーマ併記）

### 馬の眼科・神経バリアントエントリの構造的順位是正（開発者専門種）
- **未tierバリアントが2所見 coverage 1.0 で高頻度疾患を常時抑圧**していた（DDFT熱蹄と同型）:
  羞明+流涙で水晶体脱臼（稀）が表在性角膜潰瘍（馬の最多眼科救急 — Brooks）に、
  失調で馬神経軸索ジストロフィー（2所見のみ）がCVSM/Wobbler（最多の非感染性脊髄失調 — Reed & Bayly）に勝っていた
- **horse prevalence に27キー追加**: Superficial Corneal Ulcer=very_common、Anterior Uveitis/
  ERU(Moon Blindness)/CVSM/CVM=common、Deep-Melting潰瘍/真菌性角膜炎/実質膿瘍/IMMK/鼻涙管閉塞/
  眼ハブロネマ/EHM×2/EDM/eNAD/低Na血症=uncommon、水晶体脱臼/眼虫症/神経線維腫/WEE/EEE-WEE/
  馬脳症ウイルス（アフリカ）/ニパ/クリプトコッカス=rare（全キー equine モジュール実在名で検証）
- **所見セットの教科書的補完**（2所見エントリの過剰カバレッジ解消）:
  水晶体脱臼に eye_cloudiness（内皮接触性角膜浮腫）+ eye_uveitis_signs（ERU続発 — 自身の
  clinical_signs_detail 記載を反映）、eNAD に neuro_behavior_change + gen_chronic_fatigue
  （鈍麻/行動変化・パフォーマンス低下 — Finno 2011 JVIM; Aleman）
- 修正後: 羞明+流涙→表在性角膜潰瘍 rank1・前部ぶどう膜炎 top3、失調→頸椎奇形(Wobbler) rank1

### UX: クイック入力の拡充（検証済み新主訴の1タップ導線）
- 犬「散歩中に急に倒れて意識を失った」（失神→心疾患）、猫「水を飲む量が増えて痩せてきた」（老猫スクリーン）、
  馬「皮膚にイボ状のできものがある」（サルコイド）「目を細めて涙が多い」（角膜潰瘍）、
  フェレット「お腹を触るとしこりがある」（リンパ腫）— ミラーテスト JA_QUICK 同期（CI保証）
- 新規薬品は既存チップ機構で鑑別診断・チャット結果カード・疾患DBの3ビューから自動到達

### 回帰テスト（+15件）
- `TestBatch53MagnesiumSulfate`（3件 — 存在・完全バイリンガル用量・RECOVER/馬用量・
  定義的安全事実・エプソムソルト分離）
- `TestChatClinicalAccuracyAuditRound20`（12件 — 失神/てんかんLOC両立ガード・苔癬化・GDV呼吸窮迫・
  猫多飲量表現・ウサギ前庭・リクガメ甲羅軟化・フェレット腹部腫瘤・鳥副鼻腔炎vs家禽病原体・
  馬サルコイド/角膜潰瘍vs水晶体脱臼/Wobbler vs NAD）

### 表示数値の同期・キャッシュ
- `setDefaultStats()`: dog 558/cat 539/horse 355/鳥系 235薬品、pendingStats drugs 613→**614**
- ServiceWorker: `CACHE_NAME` v138 → **v139**
- 再現手順: `migrate_to_sqlite.py`（クリーンビルド）— 疾患名不変のため検索インデックス no-op

## 2026-09セッション(第32弾: 犬子宮蓄膿症の新設 + 馬背部痛/quidding対応 + トカゲstick tail + チャット精度第21弾)

### エラーチェック(結果: ベースライン健全)
- repo全体 ruff check clean、フルテスト **4,155件合格**(34 skip、カバレッジ82.38%)
- 配信SQLiteクリーンビルド: 6,893疾患・614薬品、treatment/prevention/prognosis **100%**
- 麻酔: 全21種×全8カテゴリ完備(188プロトコル)、薬剤行の dose 欠落 **0**、全種 references あり
- 薬用量: safe薬品の dosage 欠落 **0**、prevalence dead key **9**(既知残、上限15ガード内)
- 薬品マッチャー第20回スイープ: 実フレーズ全解決 — 真の欠落は空白区切り「カルシウム グルコネート」
  (爬虫類NSHP 13参照)のみ → calcium_gluconate エイリアス追加(bare グルコネートは
  キニジングルコネート部分文字列衝突のため不使用、回帰テストで固定)

### 診断チャット精度 第21弾(29症例フレッシュスイープ 5 MISS → 全症例合格)
- **犬レガシーDBに子宮蓄膿症を新設**(81→82疾患、77→78症状): 未避妊雌の最重要救急疾患なのに
  エントリも陰部分泌物語彙も皆無で「陰部から膿が出る 水をよく飲む」が腸管寄生虫1位だった
  (Egenvall 2001; Hagman 2018: 10歳までの未避妊雌の19-25%)。**分泌物ゲート型設計**:
  全身徴候(PU/PD・嘔吐・食欲不振・膨満)は全て非特異的で、セットに持たせると PU/PD+体重減少や
  嘔吐+食欲不振の主訴を乗っ取ることを検証で発見(糖尿病/急性胃腸炎の1位を奪った)→
  症状セットは vulvar_discharge のみに限定し(精巣腫瘍の女性化ペアと同型のガード)、
  単独{vulvar_discharge}×1.6 / PU/PDペア×2.0 / 膨満ペア×1.8 のクラスタで分泌物明記時の rank 1 を保証
- **genital_discharge のID-シノニム鎖を新設**: 「陰部からの出血」等のエイリアス標的なのに
  ID_SYNONYMS 鎖が無く全種語彙で脱落していた → vaginal_discharge(猫/GP/ハムスター)・
  vulvar_discharge(フェレット/レガシー犬)・bloody_vaginal_discharge(ウサギ)へ解決。
  陰部から膿/おりものが出/外陰部から膿 等エイリアス7種追加。猫の同主訴も子宮蓄膿症 rank 1、
  フェレット副腎(vulvar_swelling経路)は不変を回帰テストで固定
- **馬・背部痛/quiddingの飼い主表現が皆無だった**(所見 body_back_pain/dental_quidding と
  疾患群は既存で語彙のみ欠落): 背中を触ると痛がる/乗ると嫌がる/鞍を置くと嫌がる→body_back_pain、
  口から餌をこぼす/餌をこぼ/食べるのが遅く→dental_quidding。歯科・背部の未tier 20件を
  エビデンスで是正(歯の鋭利点=very_common・波状歯/ジアステマ/歯周病/乳歯遺残=common:
  Baker & Easley Equine Dentistry 3rd ed、仙腸関節疾患=common: Dyson、椎間板脊椎炎/フッ素症/
  過剰歯=rare)。症候群フロアに dental_quidding→Sharp Enamel Points、body_back_pain→
  Back Pain/Kissing Spines を追加(1所見エントリのカバレッジ飽和対策 — hirsutism→PPIDと同型)。
  修正後: 背部痛主訴=背部痛1位+キッシングスパイン2位、quidding主訴=歯科ddxがtop5独占
- **トカゲ stick tail**: 「尻尾が細くなって食べない」(レオパードゲッコーの尾脂肪消耗=
  Cryptosporidium varanii の hallmark — Mader 3rd ed; Deming 2008)が抽出ゼロ →
  tail_thinning 症状IDをトカゲ語彙に新設し Cryptosporidiosis(モジュール)+
  Gecko Cryptosporidiosis(supplementary JSON)の症状セットに付与、tier=common 追加 →
  クリプトが rank 1-2。他種は ID_SYNONYMS で weight_loss にフォールバック(ハムスター検証済み)
- **モルモット眼球突出**: 修飾語割り込み形「目が白く飛び出している」が既存の
  「目が飛び出し…」キー群に不一致で抽出ゼロ → 眼球が飛び出/目玉が飛び出/片目が飛び出/
  目が白く(stem) エイリアス + eye_bulging→swollen_eyes 鎖(GP語彙)追加

### UX動線
- クイック入力に検証済み新主訴を追加: 犬「陰部から膿が出て水をよく飲む」(救急)、
  馬「口から餌をこぼす」「背中を触ると痛がる」、トカゲ「尻尾が細くなってきた」
  (ミラーテスト JA_QUICK 同期、全フレーズ抽出保証をCIで維持)
- 新設疾患はチャット候補カード「疾患DBで詳細を開く」ピボットが base-name 完全一致で着地
  (子宮蓄膿症=dogモジュール Pyometra、クリプトスポリジウム症=lizardモジュール)を検証

### テスト・CI
- フルテストスイート: **4,166件合格**(34 skip、+11新規回帰テスト: Round21×10 + sweep20×1)、
  カバレッジ82.40%
- ruff check/format: repo全体 clean
- 配信SQLite再構築: 6,893疾患・3,648症状・614薬品
- ServiceWorker: CACHE_NAME v139 → **v140**、pendingStats symptoms 77→**78**
- PR #788(draft): claude/eager-bardeen-bhylx9 → main

## 2026-09セッション（第32弾・並行セッション分: シスチン尿症/EPM/房室ブロック/バベシア症の薬品4剤補完 + チャット精度第21弾 + 馬の背部痛主訴対応）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **4,155件合格**（34 skip）
- 配信SQLiteクリーンビルド: 6,893疾患、treatment/prevention/prognosis **100%**、主要臨床フィールド空欄 **0**
- 薬用量: safe薬品の dosage 欠落 **0**（614→618薬品、species_info全数検証）、文字列型相互作用スキーマ **0**
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- prevalence dead key: **9**（当該種DBに疾患自体が無い既知残、上限15ガード内）
- 薬品マッチャー飽和度検証: 用量文脈トークン監査の上位候補20フレーズ（アムホテリシンB綴りゆれ・
  ノルモソルR・ウルソデオキシコール酸・TMP-スルファ・ミコフェノール酸モフェチル等）を実フレーズで
  全数突合 — 表記ゆれ含め全て解決済み

### referenced-but-absent 薬品4剤の補完（`drug_batch_54.py` 新規、614→618薬品）
用量文脈トークン監査（第20回スイープ、find_drugs_in_text 実マッチャー突合）で検出:
- **チオプロニン（2-MPG）** — 犬シスチン尿症の第一選択溶解薬「15-20 mg/kg PO q12h」が
  Cystinuria/腎結石/膀胱結石の3エントリで用量付き参照なのに、代替のD-ペニシラミンしか収載
  されていなかった（ACVIMコンセンサス Lulich 2016 JVIM; Hoppe & Denneberg 2001）。
  アルカリ化低蛋白食の併用必須・未去勢雄のアンドロゲン依存型は去勢を先に評価、を明記
- **ジクラズリル（Protazil）** — 馬EPMのFDA承認代替（1 mg/kg PO q24h × 28日、NADA 141-268）が
  EPM 2エントリ+鳥サルコシスティス症で参照。トリアジン系はポナズリルのみだった
- **イソプロテレノール** — 第3度房室ブロックのペースメーカーまでのブリッジCRI
  （0.04-0.08 μg/kg/min）が犬・猫・馬の3エントリ全てで用量付き参照。ジギタリス感作心筋との
  併用=major・根治はペーシングであることを明記（Plumb's 10th; Ettinger 8th; Reed & Bayly 4th）
- **ジミナゼン（ガナゼック）** — 日本で犬バベシア症に承認され最も使われる薬剤なのに未収載。
  猫サイトークスゾーン/バベシア3エントリ+馬媾疫エントリ（3.5 mg/kg IM×2回）が参照。
  **犬の狭い安全域（3.5 mg/kg超・24-48時間内反復で中脳/小脳出血性壊死）** と
  B. gibsoni はアトバコン+アジスロマイシンが第一選択（Birkenheuer 2004）を明記
- **エイリアス2件**: フェニルエフリン（表記ゆれ→正規フェニレフリン、馬の腎脾間膜変位CRI 2参照）、
  「カルシウム グルコネート」空白区切り形（爬虫類NSHP 4参照）
- 動線検証: 逆引き「この薬品を使う疾患」= tiopronin 5/diclazuril 4/isoproterenol 5/diminazene 6疾患、
  相互作用チェッカー自然言語解決（ガナゼック/ちおぷろにん等）、治療チップ双方向を確認済み

### 診断チャット精度 第21弾（36症例フレッシュスイープ 8 MISS → 全症例合格）
- **ウサギ「糞が小さくなって食欲がない」が抽出ゼロ**: GIうっ滞の最古典的主訴の連用形が
  終止形キー「糞が小さい」に不一致 → 語幹キー「糞が小さく」等3種を追加 → 消化管うっ滞 rank 1
- **馬「背中を痛がって鞍をつけると嫌がる」が抽出ゼロ**: キッシングスパイン/背部痛の代表的主訴
  なのに背部痛エイリアスが「背中痛い/背部痛」のみ → 「背中を痛が」「鞍をつけると嫌が」等5種を
  EQUINE_SYMPTOM_ALIASES に追加 → 背部疾患ファミリー（頚椎椎間関節症/仙腸関節損傷/背部痛/
  キッシングスパイン）が top-5 独占
- **馬「発熱+鼻汁」でアスペルギルス症が腺疫より上位**: 肺型=免疫不全馬の稀な日和見感染・
  喉嚢型の主徴は鼻出血であり発熱鑑別ではない → Aspergillosis=rare、Hendra Virus=rare
  （豪州限定）を horse prevalence に追加 → 腺疫 rank 1
- **ヘビ「脱皮した皮が体に残ってしまっている」が抽出ゼロ**: 「皮が残ってる」キーが
  「残ってしまって」形に不一致 → 語幹キー「皮が残って」等3種 → 脱皮不全 rank 1
  （目に残る主訴は最長一致で retained_spectacle を維持 — 回帰テストで固定）
- **ウサギ「あごの下が腫れている」が汎用swellingのみで粘液腫症1位**: 歯根膿瘍の古典的主訴 →
  「あごの下が腫れ」等4種→jaw_swelling + _SYN に jaw_swelling↔facial_swelling ブリッジ
  （歯根膿瘍は facial_swelling 表記のため）→ 下顎膿瘍 rank 1・歯根膿瘍 top-5
- **爬虫類「口の周りが腫れて膿」が抽出ゼロ**: 「口の周りが腫れ」→facial_swelling、
  「口の周りに膿/口から膿」→oral_discharge（ID_SYNONYMS 新設: mouth_lesions→drooling
  フォールバック）→ マウスロット/口腔膿瘍が top-5
- ガード検証: トカゲ「あごが柔らかくてぶよぶよ」→MBD rank 1 維持、痙攣+意識消失→てんかん維持

### UX: クイック入力の拡充（検証済み新主訴の1タップ導線）
- 馬「背中を痛がって鞍を嫌がる」、ウサギ「あごの下が腫れている」（歯根膿瘍）、
  ヘビ「脱皮した皮が体に残っている」— ミラーテスト JA_QUICK 同期（全フレーズ抽出保証をCIで維持）
- 新規薬品4剤は既存の治療チップ/逆引き/相互作用チェッカー機構で鑑別診断・チャット結果カード・
  疾患DBの3ビューから自動到達（検証済み）

### 回帰テスト（+11件）
- `TestBatch54ReferencedAgents`（4件 — 4剤の存在・完全バイリンガル用量・定義的安全事実
  （ジミナゼン3.5上限+神経毒性・イソプロテレノール×ジゴキシンmajor・チオプロニン食事療法併用）・
  テキスト解決8ケース・相互作用チェッカー解決）
- `TestChatClinicalAccuracyAuditRound21`（7件 — ウサギ小糞粒連用形/馬背部痛/馬発熱鼻汁の腺疫優先/
  ヘビ体側脱皮残留+眼変異体ガード/ウサギ顎膿瘍ファミリー/爬虫類口周囲腫脹/トカゲMBDガード）

### 表示数値の同期・キャッシュ
- `setDefaultStats()`: dog 561/cat 541/horse 358/鳥系 236薬品、pendingStats drugs 614→**618**
- ServiceWorker: `CACHE_NAME` v139 → **v140**
- 再現手順: `migrate_to_sqlite.py`（クリーンビルド）— 疾患名不変のため検索インデックス no-op

### mainの並行第32弾（PR #788: 犬子宮蓄膿症+馬quidding+トカゲstick tail）とのマージ統合
- 両セッションが「第32弾」「チャット精度第21弾」「SW v140」を並行使用し5ファイルで衝突 → 解決:
  - EQUINE_SYMPTOM_ALIASES の背部痛キーは両セッションのユニオン（背中を触ると痛が/背中を痛が/
    背中が硬い/鞍をつけると嫌が/鞍を置くと嫌が/鞍を嫌が/乗ると嫌が/騎乗を嫌が/saddle resentment）
  - クイック入力: horse/lizard は main側（口から餌をこぼす・背中を触ると痛がる・尻尾が細くなってきた）、
    rabbit/snake は本セッション側（あごの下が腫れている・脱皮した皮が体に残っている）を採用し
    ミラーテスト JA_QUICK を同期
  - テストクラス衝突: 本セッションの Round21 を **TestChatClinicalAccuracyAuditRound21Parallel** に改名
    （main側の Round21=犬子宮蓄膿症/quidding/stick tail と共存）
  - 「カルシウム グルコネート」空白形エイリアスは両セッションが同一解決（キー重複なし）
  - CLAUDE.md は両セッションログを併記、pendingStats は合算実測（618薬品・78症状）に同期
- ServiceWorker: 両セッションが v140 を使用 → **v141** に改番
- マージ後フルテストスイート: **4,177件合格**（34 skip、両セッションの回帰テスト合算）、ruff clean

## 2026-09セッション（第33弾: ベザフィブラート/MPA/Onceptの補完 + Oncept用法誤記是正 + チャット精度第22弾 + 救急→疾患DB逆リンク）

### エラーチェック（結果: ベースライン健全）
- repo全体 ruff check clean、フルテスト **4,177件合格**（34 skip、ベースライン）
- 配信SQLiteクリーンビルド: 6,893疾患・618→621薬品、treatment/prevention/prognosis **100%**、
  主要臨床フィールド（治療/病因/予後/予防/説明/病態/臨床徴候）の空欄 **0**、キリル文字混入 **0**
- 薬用量: safe薬品の dosage 欠落 **0**、文字列型相互作用スキーマ **0**
- 麻酔: 全21種×全8カテゴリ完備（188プロトコル）、薬剤行の dose 欠落 **0**、全種 references あり
- prevalence dead key: **10**（当該種DBに疾患自体が無い既知残、上限15ガード内）
- 薬品マッチャー飽和度検証: 用量文脈トークン監査の上位20フレーズ（UDCA・フルニキシン・メグルミン・
  ミコフェノール酸モフェチル・アモキシシリン/クラブラン酸・乳酸リンゲル等）全て解決済み

### referenced-but-absent 薬品3剤の補完（`drug_batch_55.py` 新規、618→621薬品）
用量文脈トークン監査（第21回スイープ、find_drugs_in_text 実マッチャー突合 + 薬品様語尾フィルタ）で検出:
- **ベザフィブラート** — 犬ミニチュアシュナウザー高脂血症エントリが「5-10 mg/kg PO q24h
  （フィブラート系 — PPAR-α作動）」、胆汁性腹膜炎エントリが粘液嚢腫の高脂血症管理で参照するのに
  **フィブラート系が辞書に皆無**だった（De Marco 2017 JVIM: 30日以内に90%超でTG正常化）。
  代替ゲムフィブロジル 150-300 mg/頭 q12h も同エントリに収載（search_aliases で解決）。
  続発性原因（甲状腺機能低下/クッシング/糖尿病）の除外が先・低脂肪食は継続、を明記
- **メドロキシプロゲステロン酢酸塩（MPA/Depo）** — 猫好酸球性角結膜炎（デポ・レスキュー）、
  ハムスター子宮内膜過形成「50 mg/kg SC 単回」（Quesenberry & Carpenter 4th）が参照。
  **鳥は safe:False**（自サイトの慢性産卵エントリ自身が糖尿病・肝障害のため非推奨と明記 —
  GnRHアゴニストへ誘導）。糖尿病誘発・乳腺腫瘍・副腎抑制・未避妊雌のCEH/子宮蓄膿症という
  クラス定義的リスクと、インスリン不安定化=major 相互作用を収載。
  **「プロゲスチン」クラス語はエイリアスにしない**（馬繁殖エントリのプロゲスチン言及=実剤は
  アルトレノゲストを誤チップするため — 回帰テストで固定）
- **Oncept 犬メラノーマワクチン** — USDA承認の異種チロシナーゼDNAワクチン（獣医療初の治療用
  がんワクチン）が犬メラノーマ/口腔メラノーマの5エントリで参照されるのに未収載。
  Grosenbaugh 2011（MST 389-589日）と **Ottnod 2013（有意差なし）のエビデンス両論を正直に併記**。
  馬は非承認・試験的（Lembcke 2012）を species_info で区別
- **疾患テキストの用法誤記を是正**: 配信テキストの「Oncept 1 mL IM」は**ラベル（0.4 mL 経皮
  ニードルフリーデバイス VET JET、大腿内側）と異なる**ため、犬メラノーマ2エントリ×日英4フィールドを修正
- **garbled 薬品名修正**: 猫分離不安の「アルファカソジン」→「アルファカソゼピン（Zylkene/ジルケーン）」
  （既収載 alpha_casozepine に解決するように）。ティルドロン酸（Tildren表記ゆれ第3形）→ tiludronate

### 診断チャット精度 第22弾（25症例フレッシュスイープ 3 MISS → 全症例合格）
- **レガシー犬DBに cyanosis 語彙が皆無だった**（78→79症状）: 「舌が紫色になる」が抽出後に
  legacy 語彙で脱落し、チアノーゼ＋呼吸器主訴が定義的徴候を失っていた → cyanosis 症状を新設し
  気管虚脱・喉頭麻痺・BOAS・DCM・MMVD に付与（重度上気道閉塞・進行CHFの文書化された徴候 —
  Ettinger 8th）。**犬チェックボックス/問診経路にもパリティ追加**（dog_diseases モジュール
  respiratory カテゴリ + 同5疾患、checkbox で DCM/気管虚脱が上位）
- **レガシー犬DBに結膜炎エントリが無かった**（82→83疾患）: 一次診療で最多の犬眼科主訴なのに
  「目やにがひどくて目が開かない」がチェリーアイ/水晶体脱臼上位だった → conjunctivitis
  （very_common、Maggs, Slatter's 6th ed）を新設 → rank 1。KCS のベタつき乾燥主訴は不変
  （回帰テストで固定）
- **鳥の急性翼骨折主訴が抽出ゼロ**: 「急に飛べなくなって片方の翼が下がっている」→
  飛べなくなっ/飛べない→inability_to_fly、翼が下がっ/羽が垂れ等→wing_droop エイリアス新設 +
  ID_SYNONYMS（wing_droop→drooping_wing はインコ語彙表記、inability_to_fly→difficulty_flying
  等）→ bird/parakeet とも骨折ファミリーが rank 1
- **逆くしゃみの飼い主表現**: 「しゃっくりのような呼吸」「ブタのような音」→reverse_sneezing
  （legacy 犬はBOASが native 保有、他種は sneezing/wheezing へフォールバック）→
  逆くしゃみ＋チアノーゼで短頭種気道症候群 rank 1

### UX: 救急プロトコル→疾患DBの逆リンク（双方向動線の完成）
- 疾患詳細→緊急対応プロトコル（第28弾）の**逆方向が dead end** だった: 救急タブで GDV を開いても
  疾患DB の完全エントリ（病態生理・詳細治療・関連薬品チップ・鑑別チェック/麻酔ピボット）への
  導線が無かった
- `EMERGENCY_TO_DISEASE_MAP`（20プロトコル×種別、**配信DB実在名を全数検証**）を新設。展開した
  救急プロトコル末尾に「🔍 この疾患の詳細を疾患DBで開く」ボタン（`.emergency-disease-link`、
  currentSpecies 優先の種選択）→ `openDiseaseAcrossSpecies` で種切替+完全一致着地+自動展開。
  そこから既存の鑑別チェック・麻酔注意・相談チャットピボットに接続。GA4 `disease_from_emergency`
- マップ名の実在は served-DB 突合テストで固定（リネーム/dedupe で名前が変わったらCIで検出）

### UX: クイック入力の拡充（新規対応主訴の1タップ導線）
- 犬「目やにがひどくて目が開かない」（→結膜炎）、鳥「急に飛べなくなって翼が下がっている」
  （→骨折）。ミラーテスト JA_QUICK 同期（全フレーズ抽出保証をCIで維持）

### 回帰テスト（+15件）
- 薬品: TestBatch55（5件 — 3剤の存在・完全バイリンガル用量・定義的安全事実（MPA鳥 safe:False+
  インスリンmajor・Oncept 0.4 mL 経皮+局所制御前提・ベザフィブラート続発性除外）・テキスト解決・
  プロゲスチン非エイリアスガード・Oncept 1 mL IM/アルファカソジンの再発防止JSONスキャン）
- チャット: TestChatClinicalAccuracyAuditRound22（7件 — チアノーゼ→心肺ddx・結膜炎rank1・
  KCSガード・鳥/インコ翼骨折・猫チアノーゼ胸腔ガード・チェックボックスパリティ）
- UX: 救急→疾患DB逆リンク配線 + マップ名の served-DB 実在検証（2件）

### 表示数値の同期・キャッシュ
- `setDefaultStats()` 種別薬品数9種を実測同期（dog 563/cat 542/horse 359/鳥系 237/ferret 198 等）、
  pendingStats drugs 618→**621**・symptoms 78→**79**
- ServiceWorker: `CACHE_NAME` v141 → **v142**
- 再現手順: `migrate_to_sqlite.py`（クリーンビルド）→ `build_disease_search_index.py`（名前不変のため no-op）

### レビューで発見・是正した自作リグレッション（第33弾内）
- **喉頭麻痺への cyanosis 付与を撤回**: 7所見に増えたカバレッジ希釈で GOLPP 主訴
  （むせ+嗄声）がケンネルコフに逆転していた → 6所見に戻し（チアノーゼ付与は
  気管虚脱/BOAS/DCM/MMVD の4疾患のみ維持）、GOLPP→喉頭麻痺 rank 1 を回復
- **急性緑内障主訴の副詞挿入形**: 「片目が急に赤くて」が「目が赤く」キーに不一致 →
  目が急に赤/片目が赤/目が充血 エイリアス追加（緑内障が top-4 を回復、結膜炎新設と共存）
- 旧 Round 9 CHFテストの期待値を native cyanosis に更新（labored_breathing ブリッジは廃止）
- レガシー件数アサーション更新（79症状・83疾患）、結膜炎 severity は有効値 "low" を使用
