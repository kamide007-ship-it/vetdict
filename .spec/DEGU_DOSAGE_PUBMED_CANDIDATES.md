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

---

# 追補: grade-B 外挿候補（チンチラ/モルモット published PK・承認「拾ってください」）

出典: すべて PubMed（According to PubMed）。**degu 特異ではないため grade B（外挿）**。実在論文に記載の用量のみ転記。
degu 疾患エントリへは**未記入**（データ非改変）。獣医が Carpenter と照合の上で `treatment_overrides/degu.json` に記入する際の候補。

## 実在する grade-B 候補（チンチラ/モルモットの獣医文献）
| 薬剤 | 種 | 用量（論文記載） | 用途→degu疾患 | 出典 |
|---|---|---|---|---|
| **メロキシカム** | モルモット | 1.5 mg/kg PO/IV（PK: F=0.54, t½ 3.7h）※用量論争あり | 鎮痛・抗炎症**補助**（外耳炎/尾切断部感染 等の疼痛） | Moeremans 2019 / レビュー Evans 2024 |
| **イベルメクチン** | モルモット | 400 µg/kg SC、10日毎×3（疥癬） | 外部寄生虫/線虫（**毒性注意↓**） | Nath 2015 |
| イベルメクチン（忍容性） | チンチラ | SC 投与で腸内細菌叢への影響最小 | 上記の安全性補強 | Ma 2023 |
| **アフォキソラネル** | モルモット | 2.5 mg/kg PO 単回（Trixacarus） | 外部寄生虫（イソキサゾリン系代替） | Deak 2024 |
| **静注脂肪乳剤(ILE)** | モルモット | 脂溶性中毒に対する救命（イベルメクチン中毒） | 中毒症（植物・脂溶性毒）**支持療法** | Ebel 2022 |

**引用（According to PubMed）**:
- Moeremans I et al. *Pharmacokinetics and absolute oral bioavailability of meloxicam in guinea pigs.* Vet Anaesth Analg 2019;46(4):548-555. [DOI](https://doi.org/10.1016/j.vaa.2018.11.011) (PMID 31153785)
- Evans E, Benato L. *Pain management in pet guinea pigs: review of limitations.* Vet Anaesth Analg 2024;52(2):145-152. [DOI](https://doi.org/10.1016/j.vaa.2024.11.042) (PMID 39924411)
- Nath AJ. *Treatment and control of Trixacarus caviae in a guinea pig breeding colony.* J Parasit Dis 2015;40(4):1213-1216. [DOI](https://doi.org/10.1007/s12639-015-0652-6) (PMID 27876917)
- Ma X et al. *Short term effect of ivermectin on the bacterial microbiota in chinchillas.* Vet Sci 2023;10(2):169. [DOI](https://doi.org/10.3390/vetsci10020169) (PMID 36851473)
- Deak G et al. *Effective treatment with afoxolaner (NexGard) of Trixacarus caviae in a pet guinea pig.* Vet Med Sci 2024;10(5):e70039. [DOI](https://doi.org/10.1002/vms3.70039) (PMID 39239737)
- Ebel JJ et al. *Intralipid emulsion therapy for status epilepticus in a guinea pig secondary to ivermectin toxicity.* J Vet Emerg Crit Care 2022;33(1):107-111. [DOI](https://doi.org/10.1111/vec.13254) (PMID 36082409)

⚠️ **イベルメクチン安全性**: モルモットで経口イベルメクチン過量→てんかん重積（Ebel 2022）。用量厳守・体重精密測定・ILE 準備。

## degu疾患11件への当てはめ
| # | 疾患 | grade-B PubMed 候補 | 一次治療の状況 |
|---|---|---|---|
| 3 | 腸内寄生虫症 | イベルメクチン 400 µg/kg SC（疥癬用量からの外挿） | 線虫一次薬フェンベンダゾールは**exotic PK なし→フォーミュラリ** |
| 6 | 耳感染症 | メロキシカム**補助鎮痛**のみ | 抗菌薬本体は**フォーミュラリ** |
| 8 | 尾切断部感染 | メロキシカム**補助鎮痛**のみ | 抗菌薬本体は**フォーミュラリ** |
| 11 | 中毒症（植物） | ILE（脂溶性）＋除染・支持療法 | grade-B/C 支持療法として妥当 |
| 2,5,7,9,10,12 | 肺炎/心筋症/敗血症/マイコ/条虫/亜鉛 | **なし** | 抗菌薬・強心薬・プラジカンテル・キレート（CaEDTA）は exotic PK が PubMed に**皆無→フォーミュラリ必須** |

## 結論
- **degu 疾患データには未記入**（外挿の当てはめは stacked extrapolation を含み、獣医判断＋フォーミュラリ照合が必要なため）。
- 一次治療の主軸（抗菌薬・強心薬・駆虫薬プラジカンテル・キレート）は **PubMed に exotic-rodent PK が存在せず**、Carpenter 6th 等の**フォーミュラリでのみ**引ける（grade B）。
- 明確に有用な補助（メロキシカム鎮痛・ILE 中毒支持）と外部寄生虫オプション（イベルメクチン/アフォキソラネル、毒性注意付き）は上表の通り。
- **次アクション（Kentaro）**: どの候補を draft 記入するか指定 → 私が `evidence_grade=B`＋出典付きで `review_status=draft` 記入（公開はあなたの承認後）。
