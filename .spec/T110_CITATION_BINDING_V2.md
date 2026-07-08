# T110 — 出典紐付け v2（キーワード自動マッチ廃止 → 疾患単位キュレーション、v1保持）

Branch: `claude/vibrant-newton-np00um`

## 問題（v1）
`api/pubmed_references.py::get_references_for_disease(name)` は疾患名の**部分一致**のみで
出典を付与し、**種を考慮しない**。そのため「malocclusion」「insulinoma」「gastrointestinal stasis」
等の汎用キーがエキゾ疾患にヒットし、**犬猫の論文が無印でエキゾ疾患に付く**（T108検出器で
degu だけで19件の種不適合出典を確認：例 degu 心筋症 → 猫HCMのACVIM論文、degu CKD → 猫CKD論文）。

## v2（`get_references_for_disease_v2(name, species)`）— v1は無改変で残置
優先順位:
1. **疾患単位キュレーション**: `api/data/citations_v2/<species>.json` の `bindings: {disease_slug: [refs]}`
   が存在すれば最優先（獣医が疾患ごとに正しい出典を束ねられる。空リスト束ねで出典抑制も可能）。
2. **種ガード**: キーワード一致しても、その出典が**実際に該当する種**（`REFERENCE_SPECIES`、全30キーに
   付与）に現在の種が含まれなければ**付与しない**。→ 犬猫論文のエキゾへの漏れを抑止。
- `species=None` は v1 と同じ挙動（後方互換）。

## 効果（実測）
- degu 心筋症 / CKD / 糖尿病 / … の犬猫出典 → **抑制（0件）**。
- 一方、種適合は維持: 猫HCM→猫論文、フェレット insulinoma、ハリネズミWHS、
  **degu/ウサギ等の草食エキゾには GI stasis・不正咬合の草食エキゾ文献を付与**（degu は herbivore-exotic）。
- 呼び出し元 `api/vetdict_api.py::disease_detail` を v2（species_key 付き）に更新。

## `REFERENCE_SPECIES` の割当（要点）
- 猫: HCM / saddle thrombus / FLUTD / FIC / 猫膵炎 / 猫喘息 / FHV / FeLV / FIV / FIP / blocked cat
- 犬: GDV / 犬パルボ
- 犬猫: CKD / 糖尿病 / 尿石症 / 子宮蓄膿症 / リンパ腫 / IMHA / アトピー / 皮膚糸状菌症
- フェレット: insulinoma / 副腎疾患　ハリネズミ: WHS
- ウサギ: パスツレラ / E.cuniculi / RHD　草食エキゾ: 不正咬合 / GI stasis
- 犬猫フェレット: フィラリア

## テスト
- `tests/test_citation_binding_v2.py` 6件: v1不変、v2の種ガード抑制、種適合維持、
  species=Noneでv1同等、キュレーション最優先、空束ねで抑制。
- SEO疾患詳細ページ回帰 47件 pass。ruff 通過。

## 今後のキュレーション（獣医）
`api/data/citations_v2/<species>.json` に `{"bindings": {"<disease-slug>": [{title,authors,journal,year,doi,pmid}, ...]}}`
を追記 → 該当疾患は種ガードよりも優先してその出典を配信。段階的に v1 依存を縮小可能（v1はフォールバックとして残置）。
