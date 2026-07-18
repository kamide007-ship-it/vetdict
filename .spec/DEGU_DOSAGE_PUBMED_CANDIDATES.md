# degu 投与量 — PubMed 候補調査（T105 ドラフト補助）

出典: すべて PubMed（According to PubMed）。**用量は AI が生成せず、実在論文に記載された値のみを転記**。
degu 特異的な用量が引けないものは「PubMed になし → フォーミュラリ要（獣医記入）」と明示。
**このファイルは read-only レポート。実配信ゲート（T106）は `review_status=published` まで一切配信しない。**

## 調査方法
`Octodon degus` を軸に、12薬物疾患の薬効領域（駆虫/抗菌/循環/駆虫薬/中毒）を横断検索（`mcp__PubMed__search_articles`）。
degu 特異ヒットは metadata / 全文で用量記載の有無を確認。degu 特異が無い領域はフォーミュラリ（Carpenter 6th＝grade B）に委ねる。

## 結論（12薬物疾患のうち PubMed で degu 特異的用量が引けたのは 1件）
| # | 疾患 | PubMed degu特異的用量 | grade | 出典 |
|---|---|---|---|---|
| 1 | 毛包虫症 Fur Mites (Demodex/Notoedres) | **あり** — セラメクチン 30 mg/kg + サロラネル 5 mg/kg、局所（背頸部）、週1回×4〜6回 | **A** | Beck 2021 |
| 2 | 誤嚥性肺炎 Aspiration Pneumonia | なし | — | フォーミュラリ要 |
| 3 | 腸内寄生虫症 Intestinal Parasites | なし（病原の記載はあり＝下記参照） | — | フォーミュラリ要 |
| 4 | うっ血性心不全 CHF | なし | — | フォーミュラリ要 |
| 5 | 心筋症 Cardiomyopathy | なし（病因の記載はあり＝下記参照） | — | フォーミュラリ要 |
| 6 | 耳感染症（外耳炎） Otitis | なし | — | フォーミュラリ要 |
| 7 | 敗血症 Septicemia | なし | — | フォーミュラリ要 |
| 8 | 尾切断部感染 Tail Stump Infection | なし | — | フォーミュラリ要 |
| 9 | マイコプラズマ感染症 Mycoplasma | なし | — | フォーミュラリ要 |
| 10 | 条虫感染症 Tapeworm | なし（degu の鞭虫記載＝別種寄生虫） | — | フォーミュラリ要 |
| 11 | 中毒症（植物中毒） Plant Toxicosis | なし | — | フォーミュラリ要 |
| 12 | 亜鉛中毒 Zinc Toxicosis | なし | — | フォーミュラリ要 |

→ SPEC の停止条件「出典が過半引けない」に**引き続き該当**（12件中11件は PubMed に degu 特異的用量なし）。
   自動生成せず、grade-A の1件のみをドラフト化。残りは獣医が Carpenter 参照で記入（grade B）。

---

## 採用したドラフト（1件・grade A・fail-closed draft）
### 毛包虫症 Fur Mites (Demodex / Notoedres)
**According to PubMed**, Beck W, Hora F, Pantchev N (2021). *Case series: Efficacy of a formulation containing
selamectin and sarolaner against naturally acquired mite infestations (Demodex sp., Ornithonyssus bacoti)
in degus (Octodon degus).* Vet Parasitol 293:109430. [DOI](https://doi.org/10.1016/j.vetpar.2021.109430) (PMID 33901932)
- **degu 実症例（n=9）** で自然発生の Demodex sp. / Ornithonyssus bacoti に対し、
  **セラメクチン 30 mg/kg ＋ サロラネル 5 mg/kg**（Stronghold® Plus / Revolution® Plus）を
  **背頸部にスポット局所、週1回**投与。**Demodex は計6回、Ornithonyssus は計4回**で駆虫。良好な忍容性。
- grade **A**（degu 特異的臨床データ）。`review_status=draft`（獣医レビュー→publish で初めて配信）。
- ⚠️ 獣医確認事項: 併合剤の入手性・体重測定精度（小型個体）・Notoedres への外挿妥当性（本症例は Demodex/Ornithonyssus）。

---

## degu 特異的な「病因・病原」参照（用量ではない・T110 出典キュレーション候補）
用量ではないが degu 特異的で臨床的に有用なため記録（該当疾患の causes/etiology の出典に使える）:
- **心筋症/心筋炎**: **According to PubMed**, Mack ZE et al. (2025). *Investigation of carditis and an associated
  Helicobacter sp. in common degus.* J Zoo Wildl Med 56(2):272-280. [DOI](https://doi.org/10.1638/2024-0031) (PMID 40638167)
  — Bronx Zoo の degu 剖検 242 例中 109 例にリンパ組織球性心筋炎、新規 Helicobacter sp. と有意な相関。
  degu 心筋症の**病因**候補（用量なし）。
- **腸内寄生虫症**: **According to PubMed**, Babero BB et al. (1975). *Trichuris bradleyi sp. n., a whipworm
  from Octodon degus in Chile.* J Parasitol 61(6):1061-3. (PMID 1195067) — degu の鞭虫（Trichuris）記載。
  **病原**の裏付け（用量なし・条虫とは別種）。

## degu 特異的な麻酔データ（12疾患外・麻酔プロトコルモジュール向け）
- **According to PubMed**, Ikai Y et al. (2024). *Optimization of inhaled anesthesia for Octodon degus using
  electroencephalography.* Exp Anim 74(1):93-103. [DOI](https://doi.org/10.1538/expanim.24-0017) (PMID 39168618)
  — degu の **MAC: イソフルラン 1.75%、セボフルラン 2.25%**。degu 特異的（grade A）。
  麻酔タブ（`anesthesia_protocols.py`）の degu 維持濃度エビデンスとして採用候補。

## 検索の網羅性（除外した非該当ヒット）
degu の PubMed 文献の大半は**疾患モデル**（自然発症糖尿病・白内障、アルツハイマー/パーキンソン〈MPTP〉、
概日リズム、神経科学）で、臨床用量を含まない。確認した代表例:
- 糖尿病/白内障モデル、Andrographolide 神経炎症（IP 2/4 mg/kg・**モデル実験用量**で治療推奨ではない）
- MPTP パーキンソン病モデル（PMID 33919373）、NPFF 受容体分布（PMID 14696013）
- 歯科解剖・内視鏡（Mans 2016, Jekl 2007/2011）＝用量なし

## 次アクション（Kentaro）
1. **毛包虫症ドラフト**（`treatment_overrides/degu.json`、grade A）を確認 → 妥当なら `review_status` を `published` に。
2. 残り11件は Carpenter 6th 等で用量＋出典を記入（grade B）→ `published`。雛形は同 JSON に整備済み。
3. 病因参照（Helicobacter 心筋炎・Trichuris）は T110 出典キュレーションへ回す場合は指示を。
