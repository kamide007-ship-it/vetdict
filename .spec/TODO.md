# TODO — VetDict 品質改善（承認ゲート付き）

凡例: 🟢 読み取り専用（自由実行） / 🟡 可逆改変（バックアップ必須・種/カテゴリ単位で承認） / 🔴 承認まで実行禁止

## フェーズ0：基盤（確定済み）
- [x] データ格納形式の確定 → `.spec/DATA_MODEL.md`
- [x] SPEC 確定 → `.spec/SPEC.md`
- [x] 検出器フレームワーク `scripts/quality/detect.py`（read-only）

## フェーズ1：検出器（🟢 read-only）— **最初の実作業**
- [x] **T101** 重複/過分割 検出器（degu で実行済み）
- [x] **T102** 非臨床エントリ 検出器（degu で実行済み）
- [x] **T104** 空/見出しのみ治療 検出器（degu で実行済み）
- [x] **T108** 出典/薬品リンク整合性 検出器（request-time マッチャを再現し種不整合を検出）
- [x] **T109** 機械翻訳臭 検出器（curated lexicon: safe/review 2区分）
- [x] 全21種へ検出器を横展開（`scripts/quality/rollout.py` → `reports/quality/_rollout_summary.md`）
- [x] **検出器の「配信ビュー」モード**（`--served`）: 生ソースだけでなく統合適用後（dedup + canonical map =
      T103 適用済み＝サイトが実配信する状態）でも検出可能に。`load_species_records(species, served=True)` が
      本番の `dedupe_disease_list` + `apply_canonical_map` を再利用（再実装せず）。
      `scripts/quality/rollout.py --served` → `reports/quality/_rollout_summary_served.md`（生ベースラインは温存）。
      **成果（統合の実効果が可視化）**: 総疾患 7094→**6836 served**、完全重複クラスタ 545→**338**
      （horse 23→2 / rabbit 42→13 / degu 17→8 / dog 35→23）、非臨床 4→**1**（degu ヒト移植3件 archived）。
      詳細は `.spec/SERVED_VIEW_ROLLOUT.md`。回帰テスト `tests/test_detect_served_view.py`（5件）。read-only・データ非改変。
- [x] **検出器堅牢化：T108 コーパス未読み込みガード**（🟢 read-only・データ非改変）
      薬品/出典コーパスの import 失敗時、旧検出器は `except: return []` で黙って空リストを返し、T108 の誤リンク
      件数が 0 に落ちて「クリーン」と誤読される穴があった（依存未導入の新規コンテナで実際に発生を確認）。
      - loader を `(items, loaded_ok)` に変更し「正当に空」と「ロード失敗」を区別（コーパスは本来~600薬品で空にならない）。
      - `detect_source_integrity` に `drug_corpus_loaded/citation_corpus_loaded/corpus_incomplete/corpus_warning` を追加。
      - レポート md に参照コーパス件数を常時表示＋未読み込み時は ⚠️ 明示バナー（「0件でも未計測＝クリーンではない」）。
      - `detect.py`/`rollout.py` の `main()` はコーパス未読み込み時に **exit code 3**（自動実行が false-clean を検知可能に）。
      - `rollout.py` サマリーに対象種バナー＋stderr 警告を追加（ceiling ガードの逆＝過少計測を検知）。
      - 全21種×2ビューのレポート再生成（差分は純加算＝コーパス行/フィールドのみ、既存カウント不変を検証）。
      - 回帰テスト `tests/test_detect_corpus_guard.py`（5件）。ruff clean。

## フェーズ1.5：T108 薬品リンク種ガード（🟡 可逆・データ非改変）— **完了・PR #709**
- [x] `vetdict_api`: 2つの薬品マッチャを「その種の投与量(`species_info`)を持つ薬のみ」に（net-new）
- [x] 検出器 T108 にガード後残存カウント（目標0）を追加 + rollout 再生成
- [x] 回帰テスト（薬品ガード）+ 既存スイート pass、ruff clean
- 備考: **出典（citation）の種ガードは main の T110 v2 に統合**（`get_references_for_disease_v2`）。
  当初の v1 パッチは撤回し、検出器はガード判定に T110 の `REFERENCE_SPECIES` を参照。

## フェーズ1.6：カテゴリ分類改善（🟡 表示ロジック・データ非改変）— 完了
- [x] `_DISEASE_CAT_PATTERNS` にスコープ付きキーワード追加（感染/循環/消化/腎/皮膚/神経/運動器/歯科/生殖/行動）。
      衝突を実測監査で発見・修正（嵌頓→盲腸嵌頓、新生児→新生児死亡、脳卒中は熱中症衝突回避）。
- [x] **栄養・環境カテゴリ新設**（末尾フォールバック位置）＋落ちた正当エントリ回収（大網孔嵌頓→消化器等）。
      全21種で「その他」**1925→1255（670件・約35%再分類）**、有害な回帰0。**degu その他 39→3**、
      栄養5・環境3。実機描画で確認（栄養/環境チップ表示・その他3）。ruff clean・test_vetdict_api 145 pass。

## フェーズ2：スキーマ/不変ID（🟡 前提整備）— **完了（main, PR #711）**
- [x] `schema_migrations` テーブル + 冪等 ADD COLUMN（canonical_id, status, merged_into,
      merged_reason, aliases, evidence_grade, review_status）→ `api/database.py`
      （stdlib sqlite3 で冪等・列存在・ledger 記録を検証済み。データ非改変）
- [x] 全疾患エントリへ **不変 `id` を凍結**（位置依存ID脱却）
      - `api/data/id_locks/<species>.json`（20種・6,434件）= `name→現行id` の凍結マップ（append-only）
      - `api/species/id_locks.py::stable_id_for()`（純関数・read-only・キャッシュ）
      - `scripts/quality/build_id_locks.py`（生成器・冪等・バックアップ不要=新規サイドカーのみ）
      - `scripts/migrate_to_sqlite.py` の id 採番2箇所（generic+dog）を `stable_id_for` 経由に
      - **馬は既に明示 `id` 保持のため対象外**
      - 検証: ①今日のidは**バイト同一**（URL不変） ②リスト逆順でも **198/199 が pin**（本来なら全変動）
        ③再生成で0件new（冪等） ④全種で凍結id重複0
      - `tests/test_id_locks.py`（純Python・flask不要の回帰テスト5件）
      - **可逆**: `api/data/id_locks/` を削除すれば位置依存idにフォールバック
      ※ `aliases` 列は用意済み（統合時の旧名/旧id記録用）。今回のid凍結は**現行idの保存**なので
        リダイレクト不要（idが変わらない）。

## フェーズ3：論理統合（承認済み・degu 適用）
- [x] degu 統合レビューワークシート → `.spec/DEGU_CONSOLIDATION_REVIEW.md`
- [x] **T103 degu 適用**（承認「BC」）: 同一疾患重複＋糖尿病サブタイプを非破壊サイドカーに統合
      （白内障×4/尾脱皮×4/歯科膿瘍×3/咬傷×2/糖尿病サブタイプ2/神経障害重複1＋ヒト移植2アーカイブ）。
      **201→180 served**、301リダイレクト、別疾患は分離維持、即ロールバック可。canonical/dedup テスト29 pass。
- [x] **rabbit 適用**（承認「A一括・Bは表記のみ・D分離維持」）→ `.spec/RABBIT_CONSOLIDATION_REVIEW.md`
      `api/data/canonical/rabbit.json`（**452→421 served**、31統合＝auto 20＋curated 11、301リダイレクト、即ロールバック可）。
      - builder の kana バグ修正（`_SPECIES_JA["rabbit"]` うさぎ→ウサギ、（ウサギ）タグ未認識で0統合だった）
      - **do-not-merge ガード**: ウマバエ幼虫症(Hypoderma) と Cuterebra は name_ja 共有だが別寄生虫→誤統合を阻止（review へ退避）
      - **curated 同一疾患統合**: strict key が保留した vet 承認済み11ペア（胃拡張/涙嚢炎/DIC/増殖性腸症 等）を idempotent に反映
      - パスツレラ症/粘液腫症/妊娠中毒症のサブタイプ・全ファミリー79は review（未適用）
      - 純Python で loader 検証済み（452→421、31リダイレクト解決、Cuterebra/Warble 両方 served 維持）
- [x] **誤ラベル rename（承認済み・適用）**: `rabbit_0162 Dermatophilosis` name_ja 皮膚糸状菌症（＝真菌白癬と誤）→ **デルマトフィルス症**（7フィールド、entry自身の causes/treatment は既に細菌 Dermatophilus と正記載＝整合）、
      `rabbit_0298 Cuterebra` name_ja ウマバエ幼虫症（ウサギ）→ **クテレブラ症（ウサギ）**（5フィールド）。
      - **英語 `name` は不変**（slug/SEO URL 保全）、`name_ja` のみ変更。
      - **id 保全**: `id_locks/rabbit.json` に新キー→同id（rabbit_0162/0298）を追加。`stable_id_for` でid不変を検証。
      - 真の白癬エントリ（皮膚糸状菌症（白癬））は無改変、rabbit_0212 Warble Fly も無改変。
      - `disease_search_index.json` 再生成（差分＝当該2件のみ）。canonical 再ビルドで Cuterebra は自然に分離（31統合維持）。
      - バックアップ: `backups/2026-07-11-1138/`（改変前3ファイル）。
- [x] **cat 適用**（「続けてください」）→ `.spec/CAT_CONSOLIDATION_REVIEW.md`
      `api/data/canonical/cat.json`（**550→547 served**、curated統合3＝CKD/アセトアミノフェン/ビタミンA過剰症）。
      - FIP/EGC/SCC/MCT/髄膜腫サブタイプは分離維持（review）。**FIC は英語名一致→dedup層で既に解消**（canonical不要・実測確認）。
      - ⚠️ **cat も Dermatophytosis(真菌)/Dermatophilosis(細菌) 誤ラベル**あり（builder は非統合）。rename は別バッチ推奨。
- [x] **全canonical 監査（read-only）** + **要判断マージの分離適用（承認「1・2分離」）**:
      既存17種のauto統合を「英語名乖離」で検査→大半は正当なsynonym統合。要判断2種を分離:
      - **① Proptosis vs Exophthalmos**（別病態）→ hamster/chinchilla/hedgehog/sugar_glider の統合を **do-not-merge ガードで分離**、
        review へ退避（各種 merges −1、両疾患を個別 served）。実測で分離確認。
      - **② Ileus(機能性) vs Intestinal Obstruction(機械性)**（別病態）→ guinea_pig を同様に**分離**。
      - 注: 分離後は両者とも name_ja 基底が「眼球突出」「腸閉塞」で表示が近い。将来的な relabel（眼球突出/眼球脱出、機能性/機械性）が UX 上望ましい（follow-up）。
- [x] **horse T103 適用**（「T103をその後に続ける」）→ `.spec/HORSE_CONSOLIDATION_REVIEW.md`
      `api/data/canonical/horse.json`（**621→598 served**、curated統合21＝略称/別名の同一疾患）。
      Strangles/DDSP/ERU/EPM/EMS/PPID/Piroplasmosis(3件)/Fescue(3件)/EHV-1/低Ca 等。明示slug id保持でURL安定・loader実測一致。
      **分離維持（review）**: 扁平上皮癌(非眼性/皮膚)・鼠径ヘルニア(一般/種馬)。fish は重複0で対象外。
- [~] 残り species（ferret/bird/parakeet 等）の既存 auto canonical（**17種がライブ＝`apply_canonical_map`で
      serve時適用済み**、全ライブ統合175件中173件が `same disease modulo species tag / identical name` の安全ティア。
      サブタイプ/病型の不確実クラスタは各サイドカーの `review` に未適用退避）に加え、rabbit/cat 同様の
      **curated 同一疾患ペア（略称・修飾語違い）の掘り起こし**が可能（獣医レビュー前提）。
      - **要判断（Kentaro）**: 既存16種の重複ティア dedup を **(a)追認 / (b)ロールバック / (c)種別に再レビュー** のいずれにするか。
        物理削除なし・301・サイドカー編集で即ロールバック可。
      - 上記「全canonical監査」で surface した **Proptosis/Exophthalmos・Ileus/腸閉塞** の要判断マージも同枠。
- [x] **ferret curated レビューワークシート（提示のみ・未適用）** → `.spec/FERRET_CONSOLIDATION_REVIEW.md`
      auto tier 10（追認可否）＋ curated 同一疾患候補19（（フェレット）タグ二重登録が大半・承認で ≈248 served）
      ＋分離維持2（消化管異物 線状/一般・骨腫 頭蓋/一般）。**未適用**＝承認後に `_CURATED_MERGES["ferret"]` へ追記して apply。
- [x] **小型エキゾ哺乳類5種の curated レビューワークシート（提示のみ・未適用）** — degu/ferret/rabbit と同型の
      「水増し（病期/病型/重症度/臓器/種タグ分割）」を builder dry-run から抽出し提示。**いずれも未適用**（✅/❌/✏️ 待ち）:
      - `.spec/HAMSTER_CONSOLIDATION_REVIEW.md`（auto 9 / B 15+要確認4 / C 眼球突出ガード。承認で 312→≈286 served。
        **クロス**: ウェットテイル＝増殖性回腸炎 計5件が同一疾患）
      - `.spec/GUINEA_PIG_CONSOLIDATION_REVIEW.md`（auto 15 / B 15+要確認1 / C 腸閉塞ガード・毛包腫mislabel・干し草刺傷部位別。
        承認で 331→≈310 served。妊娠中毒症4件・壊血病4件が同一）
      - `.spec/CHINCHILLA_CONSOLIDATION_REVIEW.md`（auto 16 / B 16+要確認1 / C 眼球突出ガード・歯科4病変は別疾患。
        承認で 260→≈240 served。毛噛み5件が同一。**クロス**: 陰茎毛輪/ファーリング、ケトーシス/妊娠中毒症）
      - `.spec/SUGAR_GLIDER_CONSOLIDATION_REVIEW.md`（auto 6 / B 15+要確認1 / C 眼球突出ガード。承認で 215→≈198 served。
        Proptosis3クラスタ＝0165統合/0188分離。MBD複合は相互参照推奨）
      - `.spec/HEDGEHOG_CONSOLIDATION_REVIEW.md`（auto 6 / B 11 / C 眼球突出ガード。承認で 238→≈227 served。
        皮膚糸状菌症4件が同一。**クロス**: 肝リピドーシス/脂肪肝が肥満/非肥満で分散）
      - degu/ferret/rabbit と共通の設計: auto は追認可否のみ、B は承認後 `_CURATED_MERGE["<species>"]` に追記し
        `build_canonical.py <species> --apply`（バックアップ・冪等・301・即ロールバック）。**このバッチでは未適用。**
- [x] **残り全11種の curated レビューワークシート（提示のみ・未適用）** — これで**全21種にワークシート完備**。
      grounded data（builder auto-tier ＋ name_ja exact-dup クラスタ ＋ family クラスタ）から生成。全ワークシートで
      **引用 id を実レコードと照合済み（invented id ゼロ）**。read-only・データ非改変（`.spec/*.md` のみ）。
      - `.spec/DOG_CONSOLIDATION_REVIEW.md`（auto 12 / B 20〈firm 16+✏️4〉/ C 4。623→611 served、B全承認で ≈591。
        ガード非該当。PSS 先天/後天・HSA 脾/心は分離）
      - `.spec/BIRD_CONSOLIDATION_REVIEW.md`（auto 21 / B 30〈+✏️5〉/ C 2。551→530、B全承認で ≈499。
        鉄蓄積症 name_ja 矛盾は**rename候補**、翼/脚骨折は分離）
      - `.spec/PARAKEET_CONSOLIDATION_REVIEW.md`（auto 21 / B 18〈+✏️5〉/ C 5。459→437、B全承認で ≈415。
        ダニ/マダニ mislabel は rename、Crop stasis/impaction は腸閉塞ガード）
      - `.spec/PARROT_CONSOLIDATION_REVIEW.md`（auto 8 / B 11〈+✏️2〉/ C。283→275、B全承認で ≈263。PDD 4ラベル散在）
      - `.spec/REPTILE_CONSOLIDATION_REVIEW.md`（auto 6 / B 14〈+✏️2〉/ C 3。286→280、B全承認で ≈265。
        Shell Rot/SCUD は近似 name_ja だが別病態でクロス統合しない）
      - `.spec/TORTOISE_CONSOLIDATION_REVIEW.md`（auto 9 / B 23〈firm 13+✏️11〉/ C。288→279、firm-only ≈266。
        殻骨折 exact-dup 誤群を甲羅骨折へ訂正、痛風 内臓/関節は分離。臓器×病因テンプレ 0263-0287 はデータモデル課題）
      - `.spec/SNAKE_CONSOLIDATION_REVIEW.md`（auto 5 / B 11〈+✏️5〉/ C 5。248→243、B全承認で ≈231。
        SFD/Ophidiomycosis 3件統合、Sunshine Virus=Reptarenavirus/IBD mislabel、四肢/殻骨折は誤テンプレ→rename）
      - `.spec/LIZARD_CONSOLIDATION_REVIEW.md`（auto 9 / B 21〈+✏️3〉/ C。250→241、B全承認で ≈219。
        痛風二重登録・Yellow Fungus/CANV 3件、殻骨折 0217 は誤テンプレ→rename、5系統アデノは要獣医レビュー）
      - `.spec/AMPHIBIAN_CONSOLIDATION_REVIEW.md`（auto 4 / B 3 / C 8。254→251。**脱皮不全≠ツボカビ**ガード遵守、
        Bd/Bsal 別病原体で分離、殻骨折 mislabel→rename。Bsal 3ラベル散在は最有力の追加統合候補）
      - `.spec/EXOTIC_OTHER_CONSOLIDATION_REVIEW.md`（**混在種バケツ**・auto 3 / B 24〈+✏️6〉/ C 13。292→289、
        B全承認で ≈264。汎用タグ×汎用タグのみ統合、別宿主〈豚/ヤギ/プレーリードッグ等〉は分離、臓器×病因スタブは除外）
      - `.spec/FISH_CONSOLIDATION_REVIEW.md`（**統合対象ゼロ**。45件・重複0・過分割0。T103対象外）
      - 適用は全て未実行。auto は追認可否のみ、B は承認後 `_CURATED_MERGE["<species>"]` に追記し
        `build_canonical.py <species> --apply`。**このバッチでは未適用（✅/❌/✏️ 待ち）。**
- [x] **残り16種の firm-B 統合を一括適用（承認「全て承認」）** — degu/rabbit/cat/horse に続き、
      ferret/hamster/guinea_pig/chinchilla/sugar_glider/hedgehog/dog/bird/parakeet/parrot/
      reptile/tortoise/snake/lizard/amphibian/exotic_other の**各ワークシートの firm 行のみ**を
      `_CURATED_MERGE` に追記し `build_canonical.py <sp> --apply`。全21種で T103 適用完了。
      - **配信ビュー実測: 7,094 → 6,574 served**（16種で −262、完全重複クラスタ served 338→**125**）。
      - builder 拡張: curated グループが auto クラスタを**延長**できるよう修正（例 `0002←0093,0149`。
        既適用 rabbit/cat/horse はバイト同一で回帰なし＝挙動保存を検証）。冪等（連続適用でバイト同一）。
      - 物理削除ゼロ・301リダイレクト・サイドカー編集で即ロールバック可。dedup+canonical 適用後の
        重複スラッグ 0（全種）。回帰スイート 280 pass・ruff clean。
      - **明示的に保留（✏️要確認 / C分離維持）**: 親子・形態病型・umbrella×病因・別病態の各行は
        **未統合のまま**（例 dog アトピー⊂アレルギー性・Wobbler病型・HCC massive、chinchilla 巨大結腸症、
        parrot/exotic 肺炎 umbrella、bird 鉛神経型/卵停滞境界、snake Sunshine/Reptarena・四肢/甲羅骨折の
        リネーム、tortoise/lizard の✏️群）。獣医の1件ずつの ✅ で追加適用可。
- [x] **第2波: ✏️同一疾患行の追加適用（承認「進みます」）** — `_CURATED_MERGE_VETFLAGGED`（独立tier）で
      hamster/guinea_pig/chinchilla/reptile/tortoise/snake/lizard/parakeet/parrot/bird の
      病期・重症度・種タグ・綴り・umbrella包含・合併症注記＝同一疾患の✏️行のみを適用。served 6,574→6,529。
- [x] **(a) リネーム/アーカイブ（承認「a」）**:
      - name_ja リネーム（rabbit方式・id保全・slug/URL不変）: parakeet_0155 ダニ寄生症→**マダニ寄生症**（マダニ≠ワクモ/羽ダニ 0024）、
        snake_0147 サンシャインウイルス（ヘビ）→**封入体病（レプタレナウイルス）（ヘビ）**（真のSunshine 0005 と区別）。
        supplementary/module のソース修正＋id_locks 新キー＋検索インデックス再生成。バックアップ済み。
      - **アーカイブ**（`_CURATED_ARCHIVE`・配信から除外・非破壊）: 甲羅の無い種の「甲羅骨折」テンプレ汚染
        snake_0212 / lizard_0217 / amphibian_0236（reptile/tortoise は甲羅ありで温存）。
      - **保留**: bird 鉄蓄積症 0059/0415（non-hemochromatosis vs Hemochromatosis の英名矛盾＝獣医の命名整合が必要）。
- [x] **(b) 同一スラッグ重複の解消（承認「b」）**: `dedupe_disease_list` に英名スラッグ一致キーを追加
      （「A / B」vs「A (B)」など句読点/空白差で同一URLになる対を畳む）。全21種で重複スラッグ **0**。
      served 総数 −約6件のみ（過剰畳み無し）。
- [x] **(c) 親子/病型・umbrella の✏️（承認「c」）**: 臨床的に**別管理/別粒度**のため全て**分離維持**を推奨・現状維持
      （dog アトピー⊂アレルギー性・Wobbler 椎間板/骨性・HCC massive型、parrot/exotic/bird 肺炎 umbrella vs 病因、
      parrot GI閉塞 部分/完全）。統合すると「別疾患を1件に潰す」問題の再発になるため未統合。獣医の指示で個別に上書き可。

## フェーズ4：治療投与量（🟡ドラフト / 🔴公開）— **基盤完了（main）**
- [x] **T105/T106 fail-closed 公開ゲート＋ワークリスト**（main, merged）→ `.spec/T105_T106_DOSAGE_GATE.md`
      `api/species/treatment_overrides.py` + `api/data/treatment_overrides/<species>.json`
      （`review_status=published` かつ `sources` 有りの行のみ配信・**自動公開は構造的に不可能**）
- [x] degu 26件トリアージ（薬物要否分類）→ `.spec/DEGU_DOSAGE_DRAFT_TRIAGE.md`
- [x] **出典基準確定（承認「BC」）**: Carpenter 6th を source-of-truth に、evidence_grade A/B/C。
      `treatment_overrides/degu.json` に記入枠（`pharmacologic`/`evidence_grade`/`dosage_sources`）＋ `source_of_truth` を整備
      （薬物12・非薬物13、用量は空・`review_status=draft`・公開ゲート維持）。
- [x] **PubMed 用量調査（承認「用量はpubmedを調べて欲しい」）** → `.spec/DEGU_DOSAGE_PUBMED_CANDIDATES.md`
      `Octodon degus` 横断検索。12薬物疾患のうち **degu 特異的用量が引けたのは 1件のみ**:
      - **毛包虫症**: セラメクチン 30 mg/kg + サロラネル 5 mg/kg 局所・週1回×4-6（Beck 2021, Vet Parasitol,
        DOI 10.1016/j.vetpar.2021.109430, PMID 33901932）= **grade A**。`treatment_overrides/degu.json` に
        **draft で記入**（sources 付き・`review_status=draft` 維持＝**未配信**、獣医が publish で初めて配信）。
      - 残り11件は PubMed に degu 特異的用量なし → Carpenter 6th 等のフォーミュラリ要（grade B・獣医記入）。
        SPEC 停止条件「出典が過半引けない」に引き続き該当＝自動生成せず。
      - 副産物（用量ではない degu 特異的参照）: Helicobacter 心筋炎（Mack 2025）・Trichuris 鞭虫（Babero 1975）＝
        病因の出典候補。麻酔 MAC iso1.75%/sevo2.25%（Ikai 2024）＝麻酔モジュール向け。
      - fail-closed ゲート維持（`test_treatment_publish_gate` 6 pass、served 公開0件）。
- [ ] **獣医の人手作業待ち**: 毛包虫症ドラフト（grade A）をレビュー→ `published`；残り11件は Carpenter 参照で
      用量＋出典を記入 → `approved` → `published`（🔴・自動公開しない）

## フェーズ5：付随品質（🟡）
- [x] **T107** NMN/ECVN ブロックを「自社製品・PR」枠へラベル分離（main, merged）→ `.spec/T107_NMN_PR_LABEL.md`
- [x] **T110** 出典紐付けv2（疾患単位キュレーション＋種ガード、v1は残す）（main, merged）→ `.spec/T110_CITATION_BINDING_V2.md`
- [x] **(D) 予防文の異種汚染修正（JA）**: 非companion 544件の prevention_ja に犬猫助言（リード散歩/短頭種/FLUTD等）
      が焼き込まれていた既存バグを修正。`_is_contaminated` をマーカー語検出で補強し種クラス対応版で再生成。544→0。
- [x] **(D) 予防文の異種汚染修正（EN）**: 英語版 種クラス対応 prevention 生成器を新設
      （`_PREVENT_CLASS_CORE_EN`/`_prevention_overlay_en`/`gen_prevention_en_noncompanion`）。
      EN 汚染 387→0。回帰テスト追加。`test_no_template_disease_content` 178 pass。
- [x] T109 機械翻訳臭の置換適用: safe 語（葡萄糖→ブドウ糖等）は適用済み。
      文脈依存の誤フレーズ（遺伝学的インスリン抵抗→遺伝的等6種12件）を `apply_mt_smell_phrases.py` で
      フレーズ単位に安全修正（正当な 遺伝学的スクリーニング/背景/異常 は温存）。degu review 17→8。
- [x] 残る T109 review 語適用（承認済み）: `易感受性`×6→「感受性が高い/罹患しやすい」、`貧弱な耐性`→「乏しい耐性」を
      `apply_mt_smell_phrases.py` にフレーズ単位で追加・適用（degu_diseases.py 7件、文脈別に正しい助詞処理）。
      `遺伝学的スクリーニング`は正当用語のため温存。**degu T109 8→1**。

## いま承認を求める項目
1. **(B) degu 統合判断**（`.spec/DEGU_CONSOLIDATION_REVIEW.md` を1件ずつ ✅/❌/✏️）→ 承認行のみ canonical 反映
2. **(C) 投与量の出典基準**（source-of-truth formulary + evidence_grade）→ 指定後に degu worklist を獣医記入
3. 🔴（T103 統合の本適用・T106 公開）は承認まで未実行、で合意か
