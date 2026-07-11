# horse 論理統合レビューワークシート（T103）

> **更新（適用状況）**: 「T103をその後に続ける」を受けて、**略称/別名の同一疾患21クラスタ**を
> `api/data/canonical/horse.json` に curated 統合（**621→598 served・301リダイレクト・即ロールバック可**）。
> horse は明示 slug id 保持のため URL 安定。臨床的に別の2件は分離維持（review）。
> ❌ にしたい統合行があれば言ってください。

## ✅ 適用（同一疾患の略称/別名 — curated 統合21件）
horse の重複は「種タグ違い」ではなく**略称・記載ゆれ・別名**で分かれた同一疾患。builder の strict key は
自動統合しないため、獣医レビュー済みとして curated 統合:

| 疾患 | 統合したエントリ |
|---|---|
| 喉頭片麻痺 (Roaring) | Laryngeal Hemiplegia + (Roaring) |
| 軟口蓋背方変位 (DDSP) | DDSP + Dorsal Displacement of Soft Palate |
| 腺疫 | Strangles + (Streptococcus equi) |
| ピロプラズマ症 | Piroplasmosis + Equine Piroplasmosis + (Babesiosis/Theileriosis)【3件】 |
| 馬再発性ぶどう膜炎 (ERU) | ERU + (Moon Blindness) |
| 馬原虫性脊髄脳炎 (EPM) | EPM + (Extended) |
| 馬メタボリック症候群 (EMS) | EMS + (EMS) |
| 下垂体中葉機能障害 (PPID) | PPID + (Cushing's) |
| 横紋筋融解症 | Exertional Rhabdomyolysis + (Tying Up) |
| バックドシン | Bucked Shin + Bucked Shins |
| ロドコッカス肺炎 | Rhodococcus equi Pneumonia + (Foal) |
| 馬ウイルス性動脈炎 (EVA) | EVA + (EVA) |
| ドングリ中毒 | Acorn Toxicity + Acorn/Oak Toxicosis (Tannin) |
| フェスク中毒 | Fescue Toxicity + Toxicosis + (Reproductive)【3件】 |
| 肢軸異常 (ALD) | Angular Limb Deformities + Deformity |
| 肘腫 | Capped Elbow + Elbow Hygroma (Shoe Boil) |
| 浅指屈腱炎 | SDFT + (Bowed Tendon) |
| 潰瘍性リンパ管炎 | + (Corynebacterium pseudotuberculosis) |
| EHV-1 脊髄脳症 | EHV-1 Myeloencephalopathy + (EHM) |
| 低カルシウム血症 | Hypocalcemia + (Transport/Lactation Tetany) |
| 周産期仮死 | Perinatal Asphyxia + Syndrome (Dummy Foal/NMS) |

## ⏳ 分離維持（要判断・review 保留）
- **扁平上皮癌**: `on_scc`（非眼性）/ `on_squamous_cell_carcinoma`（皮膚）— 皮膚は非眼性の部分集合だが完全一致ではない。部位で挙動が異なるため**分離維持**（統合するなら要指示）。
- **鼠径ヘルニア**: `dg_inguinal_hernia`（一般）/ `rp_inguinal_hernia_stallion`（種馬）— 先天性(子馬)と後天性(種馬)で病態が別。**分離維持**。

## 集計
- 適用: **21統合**（621→598 served、うち2クラスタは3件統合）。SCC・鼠径ヘルニアは分離維持。
- 物理削除なし・301リダイレクト・サイドカー編集で即ロールバック可。loader 実測 621→598 一致。
