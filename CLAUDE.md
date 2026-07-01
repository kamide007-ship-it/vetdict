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
