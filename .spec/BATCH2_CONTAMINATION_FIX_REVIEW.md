# Batch-2 cross-species 汚染修正（残り7種）— 適用ログ＋要獣医レビュー2件

## サマリー
残り7種（bird/parakeet/parrot/tortoise/snake/sugar_glider/reptile）の cross-species 汚染を、
**安全な relabel（種名ラベルのみの誤り・臨床内容は当該種に妥当）45フィールドを一括自動適用**し、
**臨床内容の書き換えが要る2件だけ**を本ワークシートに退避（未適用・要獣医レビュー）。

- スキャナ改良（false-positive除去）: 「幼鳥／新生鳥／小型トカゲ」等、**種名を部分文字列に含むだけの複合語**
  （直前が漢字＝複合語）を除外。53→49フィールドに精緻化。read-only。
- 適用: `scripts/quality/fix_cross_species_batch2.py`（冪等・バックアップ `backups/2026-07-21-1000/`・
  module `.py` を修正／JSONオーバーレイは該当0＝module-only記録のため source-species の正当エントリは無改変）。
- 検証: `scan_cross_species.py` が **9種→2種**（残りは下記C-2件のみ）、再実行でバイト同一（冪等）、
  回帰テスト16 pass、ruff clean。

## 自動適用した安全 relabel（45フィールド・種名スワップのみ）
| 種 | 疾患（フィールド） | 誤ラベル→正 |
|---|---|---|
| bird | Candidiasis / Mucormycosis / Egg Binding / Atoxoplasmosis / Avian Nephropathy / Smoke Inhalation / Cloacal Papillomatosis | 両生類・トカゲ・インコ・オウム → **鳥** |
| parakeet | Gout(内臓/関節) / Feather Follicle Cyst / Vitamin E・Se Deficiency | 両生類・オウム → **インコ** |
| parrot | Candidiasis / Heavy Metal Poisoning / Cloacal Papilloma | 両生類・インコ → **オウム** |
| tortoise | Articular/Visceral Gout / Follicular Stasis / Chronic Resp. Disease | 鳥・トカゲ → **リクガメ** |
| snake | Articular/Visceral Gout / Spinal Osteopathy | 鳥・トカゲ → **ヘビ** |
| sugar_glider | Nutritional Osteodystrophy | リクガメ → **フクロモモンガ** |
| reptile | Chronic Resp. Disease Complex | トカゲ → **爬虫類** |

いずれも「当該種で実際に起こる疾患＋汎用的な病因/病態テキスト」で、種名ラベルのみが誤り。
スワップは新たな臨床的主張を導入しない純粋な訂正（degu/lizard/hamster の L 型と同じ）。

**残存の一般課題（今回対象外・別軸）**: 一部の病態文は汎用テンプレート（例 tortoise Follicular Stasis の
patho が「消化器疾患」と誤カテゴリ、痛風 causes が尿酸に触れない汎用代謝文）。種汚染は解消済みだが、
疾患固有化は別途（lizard 痛風で行ったような尿酸代謝への書き換え）。

---

## 要獣医レビュー（🟡未適用・✅/❌/✏️ 待ち）

### 1. sugar_glider — Proptosis (Eye Prolapse) / 眼球突出症（眼球脱出）★cross-class
- **現在（爬虫類の内容が哺乳類に）**:
  - causes_ja: 「**トカゲにおける**眼球突出症の原因: 感染、膿瘍、占拠性病変による眼球の異常突出です。」
  - treatment_ja: 「**トカゲにおける**…培養感受性試験に基づく標的抗菌薬療法…膿瘍や壊死組織には外科的排膿またはデブリードマン…」
  - 問題: 爬虫類の眼球突出は**眼窩後方の膿瘍・占拠性病変**が主因で抗菌薬・排膿が中心。一方フクロモモンガ（哺乳類）の
    眼球突出は**外傷性の眼球前方脱出**が典型で、救急整復／眼瞼一時縫合／摘出が要点。内容が別クラスからのコピー。
- **提案ドラフト（要獣医レビュー）**:
  - causes_ja: 「フクロモモンガにおける眼球突出症（眼球脱出）の原因: 多くは外傷（咬傷・拘束・落下）による急性の眼球前方脱出。
    眼窩後方の占拠性病変（膿瘍・腫瘍）が誘因となることもある。」
  - treatment_ja: 「フクロモモンガにおける眼球突出症（眼球脱出）は救急疾患である。角膜乾燥を防ぐため直ちに眼表面を湿潤・
    保護し、鎮痛下で可及的に眼球整復と一時的眼瞼縫合（tarsorrhaphy）を試みる。整復不能・眼球破裂・視覚予後不良例は
    眼球摘出を行う。全身状態の安定化・鎮痛・二次感染予防の抗菌薬・原因（外傷／占拠性病変）の検索を併せて行う。」
  - ※末尾の `[ECVN:Block]`（PR・自社製品ラベル）はベース治療文と分離済みのため保持。

### 2. parrot — Atherosclerosis / 動脈硬化症（within-class＋種特異疫学）
- **現在**:
  - causes_ja: 「**インコにおける**動脈硬化症の原因: 動脈内のコレステロールプラーク蓄積による血流低下で、**種子食の高齢セキセイインコに多発**。」
  - pathophysiology_ja: 「動脈硬化症は**インコにおける代謝・内分泌疾患である。**基礎病態はホルモンのフィードバックループ…」（汎用テンプレ＋誤カテゴリ）
  - 問題: オウムのエントリなのに疫学が「セキセイインコ（＝インコ）に多発」。かつ病態が「代謝・内分泌疾患」テンプレで
    循環器疾患として不正確。単純 relabel だと「オウムにおける…セキセイインコに多発」と内部矛盾するため C 扱い。
- **提案ドラフト（要獣医レビュー）**:
  - causes_ja: 「オウムにおける動脈硬化症の原因: 大動脈・主要動脈へのコレステロール／脂質プラーク蓄積による血管壁肥厚・
    内腔狭窄。高脂肪・種子食、運動不足、加齢、脂質代謝異常が危険因子で、ヨウム・ボウシインコ等の高齢オウム類や
    セキセイインコに多い。」
  - pathophysiology_ja: 「動脈硬化症はオウムにおける心血管疾患である。慢性の脂質蓄積と血管内皮傷害により大動脈・
    腕頭動脈などにアテローム様プラークが形成され、血管壁の肥厚・硬化・内腔狭窄を来す。進行すると後負荷増大・組織灌流
    低下により運動不耐性・虚脱・神経症状（脳虚血）・突然死につながりうる。」

---

## 適用手順（承認後・🟡）
1. バックアップ → `backups/YYYY-MM-DD-HHMM/`（parrot/sugar_glider module）。
2. 承認された行のみ patch（`fix_cross_species_batch2.py` の `C_EXCLUDE` から外し、専用 override として反映）。
3. `scan_cross_species.py` で全21種 **0件**（＝汚染撲滅完了）を確認。
4. 冪等性確認。

## 承認を求める項目
- 上記2件（sugar_glider Proptosis の2フィールド／parrot Atherosclerosis の2フィールド）の ✅/❌/✏️。
- 承認後、`scan_cross_species.py` を rollout/CI に組み込み **将来の「〜における」混入を回帰ガード化**するかも判断ください。
