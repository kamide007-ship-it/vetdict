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
