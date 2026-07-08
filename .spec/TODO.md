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

## フェーズ1.5：T108 薬品リンク種ガード（🟡 可逆・データ非改変）— **完了・PR #709**
- [x] `vetdict_api`: 2つの薬品マッチャを「その種の投与量(`species_info`)を持つ薬のみ」に（net-new）
- [x] 検出器 T108 にガード後残存カウント（目標0）を追加 + rollout 再生成
- [x] 回帰テスト（薬品ガード）+ 既存スイート pass、ruff clean
- 備考: **出典（citation）の種ガードは main の T110 v2 に統合**（`get_references_for_disease_v2`）。
  当初の v1 パッチは撤回し、検出器はガード判定に T110 の `REFERENCE_SPECIES` を参照。

## フェーズ2：スキーマ/不変ID（🟡 前提整備）
- [ ] `schema_migrations` テーブル + 冪等 ADD COLUMN（canonical_id, status, …）
- [ ] 全疾患エントリへ **不変 `id`（スラッグ）を付与**するマイグレーション（位置依存ID脱却）
      ※ 旧位置ID → 新IDの `aliases` を記録し、既存URLを保全

## フェーズ3：論理統合（🔴 承認必須）
- [x] degu 統合レビューワークシート提示 → `.spec/DEGU_CONSOLIDATION_REVIEW.md`（**承認待ち**）
- [ ] **T103** `canonical_id`+`status(active/merged/archived)` で非破壊統合（承認行のみ適用）
- [ ] 旧URL → canonical へのリダイレクト
- [ ] **提示単位：1動物種/1カテゴリのバッチ**で Kentaro 承認 → 実行

## フェーズ4：治療投与量（🟡ドラフト / 🔴公開）— **基盤完了（main）**
- [x] **T105/T106 fail-closed 公開ゲート＋ワークリスト**（main, merged）→ `.spec/T105_T106_DOSAGE_GATE.md`
      `api/species/treatment_overrides.py` + `api/data/treatment_overrides/<species>.json`
      （`review_status=published` かつ `sources` 有りの行のみ配信・**自動公開は構造的に不可能**）
- [x] degu 26件トリアージ（薬物要否分類）→ `.spec/DEGU_DOSAGE_DRAFT_TRIAGE.md`（main の worklist を補完）
- [ ] **獣医の人手作業待ち**: `treatment_overrides/degu.json` の各エントリに出典付き用量を記入 → `published`
- [ ] 出典 source-of-truth（Carpenter 6th 等）の指定 + evidence_grade 定義

## フェーズ5：付随品質（🟡）
- [x] **T107** NMN/ECVN ブロックを「自社製品・PR」枠へラベル分離（main, merged）→ `.spec/T107_NMN_PR_LABEL.md`
- [x] **T110** 出典紐付けv2（疾患単位キュレーション＋種ガード、v1は残す）（main, merged）→ `.spec/T110_CITATION_BINDING_V2.md`
- [x] **(D) 予防文の異種汚染修正**: 非companion 544件の prevention_ja に犬猫助言（リード散歩/短頭種/FLUTD等）
      が焼き込まれていた既存バグを修正。`_is_contaminated` をマーカー語検出で補強し種クラス対応版で再生成。
      544→0、`test_no_template_disease_content` 177 pass。
- [ ] **EN 予防文の残汚染**（'leash walk' 191件・非dogcat）: EN 種クラス別 base 生成器が未整備（follow-up）
- [ ] T109 機械翻訳臭の置換適用（`scripts/quality/apply_mt_smell.py` を段階適用、臨床用語は要レビュー）

## いま承認を求める項目
1. **(B) degu 統合判断**（`.spec/DEGU_CONSOLIDATION_REVIEW.md` を1件ずつ ✅/❌/✏️）→ 承認行のみ canonical 反映
2. **(C) 投与量の出典基準**（source-of-truth formulary + evidence_grade）→ 指定後に degu worklist を獣医記入
3. 🔴（T103 統合の本適用・T106 公開）は承認まで未実行、で合意か
