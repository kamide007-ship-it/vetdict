# Cross-species 汚染スキャン（全21種・read-only 横展開）

degu 外耳炎で見つけた「`<他種>における…`」テンプレ混入を全種に横展開。
スキャナ: `scripts/quality/scan_cross_species.py`（read-only・冪等）／
機械可読: `reports/quality/_cross_species_contamination.json`。

## 検出ロジック
enrichment が各レコードに「`<種>における<疾患>…`」の枠組み文を焼き込んでいる。この `<種>` が
**そのレコード自身の種と異なる**場合、JA 内容が別種クラスからコピーされた汚染。比較表現
（「モルモットと異なり」等）は除外。

## サマリー: **9種・65フィールドが汚染**（うち cross-class 36＝高重症度）
| 種 | 汚染フィールド | cross-class | 主な誤ラベル | 修正ワークシート |
|---|--:|--:|---|---|
| bird | 13 | 5 | 両生類・トカゲ（Candidiasis/Mucormycosis/Egg Binding）＋インコ/オウム(within) | `BIRD_CONTAMINATION_FIX_REVIEW.md` |
| parakeet | 8 | 4 | 両生類（痛風 内臓/関節）＋オウム(within) | `PARAKEET_CONTAMINATION_FIX_REVIEW.md` |
| parrot | 8 | 2 | 両生類（Candidiasis）＋インコ(within) | `PARROT_CONTAMINATION_FIX_REVIEW.md` |
| tortoise | 8 | 4 | 鳥（痛風）＋トカゲ(within) | `TORTOISE_CONTAMINATION_FIX_REVIEW.md` |
| lizard | 8 | 8 | フクロモモンガ(NSHP)・鳥(痛風)・両生類(UV欠乏) | `LIZARD_CONTAMINATION_FIX_REVIEW.md` |
| hamster | 7 | 5 | **オウム(糖尿病)・インコ(熱中症)・フクロモモンガ(腎アミロイド)** | `HAMSTER_CONTAMINATION_FIX_REVIEW.md` |
| snake | 6 | 4 | 鳥(痛風)＋トカゲ(within) | `SNAKE_CONTAMINATION_FIX_REVIEW.md` |
| sugar_glider | 4 | 4 | **トカゲ(眼球突出)・リクガメ(栄養性骨異栄養症)** | `SUGAR_GLIDER_CONTAMINATION_FIX_REVIEW.md` |
| reptile | 3 | 3※ | トカゲ（イベルメクチン中毒/慢性呼吸器） | `REPTILE_CONTAMINATION_FIX_REVIEW.md` |

※reptile の「トカゲにおける」は lizard⊂reptile だが generic reptile レコードには不適切な種名ラベル。

### スキャナ精度改善（read-only・偽陽性除去、68→65）
単字ラベル「鳥/犬/猫/馬/魚」は複合名詞（**幼鳥・成鳥・子犬・野鳥…**）の語尾でもあり、これらは
別種ラベルではない。真の別種ラベルは文頭 or 助詞/句読点の直後に置かれるのに対し、複合名詞では
漢字/カタカナが直前で結合する。`scan_cross_species.py` に「単字ラベルの直前が漢字/カタカナなら
除外」ガードを追加し、偽陽性 **3件**（parakeet `幼鳥における`×2 / parrot `新生鳥における`×1）を除去
（parakeet 10→8・parrot 9→8）。真の別種ラベル（例: リクガメ痛風の文頭「鳥における」）は温存。
回帰テスト `tests/test_scan_cross_species_guard.py`（4件）。cross-class 36 は不変（偽陽性は全て within-class）。

**全9種にワークシート完備**（提示のみ・🟡未適用）。修正は種別1バッチで承認後に適用。

## 重症度の考え方
- **cross-class（36件・要優先修正）**: 哺乳類レコードに鳥/爬虫類の枠組み、鳥レコードに両生類の枠組み等。
  臨床内容が**別クラスからの丸ごとコピー**の可能性が高い（例: ハムスター糖尿病が「オウムにおける…」、
  トカゲ NSHP が「フクロモモンガにおける…」）。degu 外耳炎（爬虫類混入）と同型。
- **within-class（32件・ラベル主体）**: bird↔インコ↔オウム、reptile↔トカゲ等。枠組みラベルは誤りだが、
  内容はクラス的には近い場合が多い（例: リクガメ痛風が「鳥における痛風」＝鳥/爬虫類で病態が類似）。
  それでも種名ラベルは訂正対象。

## 顕著な cross-class 例（獣医が即発見する類）
- **hamster Diabetes**: causes/patho が「**オウム**における糖尿病…」（鳥の膵島記述が齧歯類に）
- **hamster Heatstroke**: 「**インコ**における熱中症…」
- **bird Candidiasis / parrot Candidiasis**: 「**両生類**における真菌感染症…」
- **tortoise/snake/lizard Gout**: 「**鳥**における…代謝・内分泌疾患…」（鳥痛風の枠組みが爬虫類に）
- **lizard NSHP**: 「**フクロモモンガ**における…」　**sugar_glider Proptosis**: 「**トカゲ**における眼球突出症…」

## 修正方針（提案・🟡 データ改変＝承認後）
degu 外耳炎と同じ手法で:
1. **cross-class 36件を優先**。各フィールドの `<他種>における` 枠組みを当該種に訂正し、別クラス固有の
   記述（解剖・病態）を当該種向けに是正（最小改変 or 種特異内容に書き換え）。
2. **within-class 32件**はラベル訂正主体（例「鳥における」→「リクガメにおける」）＋クラス内で内容妥当性を確認。
3. **種別1バッチ**で提示→承認→適用（既存の 🟡 ワークフロー）。回帰は本スキャナで0件を確認。
4. スキャナを rollout に組み込み CI 回帰ガード化（`における`混入を将来検出）も可能。

**このスキャンは read-only・データ非改変。** 修正は承認後に種別バッチで実施。
どの種から着手するか指定ください（cross-class 8件で最悪の **lizard**、または齧歯類で目立つ **hamster** を推奨）。
