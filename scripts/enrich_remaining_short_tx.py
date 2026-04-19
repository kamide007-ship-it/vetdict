#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# Amphibian (11件)
# ============================================================

ENRICHMENTS["amphibian_0028"] = {
    "treatment_ja": (
        "代謝性骨疾患（MBD）/栄養性二次性上皮小体機能亢進症（両生類）。"
        "★両生類は皮膚からのCa吸収能があるが、食事Ca:P比が最重要★。"
        "急性（低Ca痙攣/振戦）: "
        "  グルコン酸カルシウム10%: 50-100 mg/kg ICe（体腔内）or 経皮吸収（薄めた溶液に浸漬）。"
        "  ★両生類はIM注射困難な小型種が多い — 浸漬法が実用的★。"
        "維持療法: "
        "  昆虫へのCaパウダーダスティング（毎回の給餌時）。"
        "  Ca:P比2:1以上。D3含有/非含有を使い分け。"
        "  UVB照射: 昼行性種（ヤドクガエル等）には有用。"
        "  ★夜行性種（ツノガエル等）: UVB要求量は低いがCaダスティングは必須★。"
        "食事改善: "
        "  ガットローディング（昆虫にCa豊富飼料を24h前に給餌）。"
        "  ★コオロギ/ミルワームはCa:P比が悪い — 必ずダスティング★。"
        "予後: 早期+食事改善で良好。骨変形（下顎ゴム様化）は不可逆。"
    ),
}

ENRICHMENTS["amphibian_0127"] = {
    "treatment_ja": (
        "カルシウム欠乏症（両生類）。"
        "★MBDの初期段階。昆虫食両生類ではCaダスティング不足が主因★。"
        "急性（低Ca痙攣/四肢硬直）: "
        "  グルコン酸カルシウム10%: 50-100 mg/kg ICe。"
        "  小型種: Ca含有溶液（40 mg/L）への浸漬（経皮吸収）。"
        "カルシウム補充: "
        "  昆虫へのCaパウダーダスティング（毎回）。"
        "  ガットローディング: 昆虫にCa豊富飼料を給餌後に与える。"
        "  Ca:P比2:1以上を目標。"
        "UVB照射（種による）: "
        "  昼行性種: UVB 5%ランプが有用。"
        "  夜行性種: UVBの必要性は低いが害はない。"
        "水質管理: 水中Ca濃度の維持（水棲種）。"
        "予後: 早期補正+食事管理で良好。骨変形は不可逆。"
    ),
}

ENRICHMENTS["amphibian_0061"] = {
    "treatment_ja": (
        "膿瘍（両生類）。"
        "★両生類の皮膚は非常に薄く透過性が高い — 局所薬剤の全身吸収に注意★。"
        "外科的切除: "
        "  MS-222（トリカイン）浸漬麻酔下で膿瘍を切開/切除。"
        "  腔内洗浄: 滅菌生理食塩水（★クロルヘキシジンは両生類に毒性あり — 使用禁忌★）。"
        "  開放創管理。湿潤環境維持。"
        "抗菌薬: "
        "  エンロフロキサシン 5-10 mg/kg PO/IM/浸漬 q24h。"
        "  ★セフタジジムは両生類にも有効 — 20 mg/kg IM q72h★。"
        "  嫌気性菌: メトロニダゾール 10-20 mg/kg PO q24-48h。"
        "  ★アミノグリコシド: 腎毒性高い — 十分な水和下のみ★。"
        "環境管理: 清潔な水（水棲種）。適正温度。"
        "  ★水質悪化が両生類の感染症の最大のリスク因子★。"
        "予後: 表在性は良好。深部/全身播種は予後不良。"
    ),
}

ENRICHMENTS["amphibian_0098"] = {
    "treatment_ja": (
        "眼鏡鱗下膿瘍（両生類）。"
        "★両生類は眼鏡鱗（spectacle）を持たない — 眼周囲膿瘍/結膜膿瘍として扱う★。"
        "外科的処置: "
        "  MS-222浸漬麻酔下で膿瘍を慎重に切開。"
        "  乾酪状/膿性物質を除去。眼球損傷回避。"
        "  洗浄: 滅菌生理食塩水（★クロルヘキシジン禁忌★）。"
        "局所療法: "
        "  抗菌点眼: オフロキサシン0.3%点眼 q8-12h。"
        "  ★点眼薬は経皮吸収されるため用量に注意★。"
        "全身抗菌薬: "
        "  エンロフロキサシン 5-10 mg/kg PO/IM q24h。"
        "  セフタジジム 20 mg/kg IM q72h。"
        "環境管理: 水質管理（水棲種）。湿度管理（陸棲種）。"
        "予後: 早期処置で良好。眼球浸潤時は眼球摘出検討。"
    ),
}

ENRICHMENTS["amphibian_0064"] = {
    "treatment_ja": (
        "潰瘍性皮膚炎（両生類）。"
        "★両生類の皮膚は呼吸・水分調節に関与 — 皮膚損傷は致命的になりうる★。"
        "原因精査: "
        "  細菌培養+感受性試験。真菌培養。"
        "  ★ツボカビ（Batrachochytrium dendrobatidis: Bd）PCR検査を必ず実施★。"
        "  水質検査（アンモニア/亜硝酸/pH）。"
        "局所管理: "
        "  滅菌生理食塩水で洗浄（★クロルヘキシジン/ポビドンヨードは両生類に毒性★）。"
        "  SSDクリーム: 限局的に使用可（広範囲は経皮吸収リスク）。"
        "全身療法: "
        "  細菌性: エンロフロキサシン 5-10 mg/kg PO/浸漬 q24h。"
        "  ツボカビ: イトラコナゾール浸漬（0.01% 5分/日×10日）。"
        "  真菌性: ボリコナゾール 5 mg/kg PO q24h。"
        "環境管理: 水質改善（最重要）。適正温度。清潔基材。"
        "予後: 水質改善+早期治療で良好。ツボカビ/広範囲壊死は予後不良。"
    ),
}

ENRICHMENTS["amphibian_bacterial_dermatitis"] = {
    "treatment_ja": (
        "細菌性皮膚炎（両生類）。"
        "主要原因菌: Aeromonas hydrophila, Pseudomonas, Citrobacter, Flavobacterium。"
        "★「red leg syndrome」はAeromonas/Pseudomonasによる敗血症性皮膚炎★。"
        "軽度（限局性紅斑/点状出血）: "
        "  水質改善（最重要）: アンモニア/亜硝酸ゼロ、適正pH。"
        "  塩水浴（両生類用低濃度: 0.1-0.3%）短時間。"
        "  SSD局所（限局的に）。"
        "中等度-重度（red leg/全身性紅斑/潰瘍）: "
        "  エンロフロキサシン 5-10 mg/kg PO/IM/浸漬 q24h。"
        "  セフタジジム 20 mg/kg IM q72h。C&Sで調整。"
        "  輸液: 両生類用リンゲル液（哺乳類用より低浸透圧）。"
        "環境管理: 水質維持。適正温度。過密飼育回避。"
        "  ★ストレス（取扱い/輸送/環境変化）が免疫抑制→発症の主因★。"
        "予後: 水質改善+早期治療で良好。敗血症（red leg重症型）は予後不良。"
    ),
}


def apply_enrichments() -> None:
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for entry in data:
        eid = entry.get("id")
        if eid in ENRICHMENTS:
            patch = ENRICHMENTS[eid]
            for k, v in patch.items():
                entry[k] = v
            updated += 1

    missing = set(ENRICHMENTS) - {e.get("id") for e in data}
    if missing:
        print(f"WARNING: {len(missing)} IDs in ENRICHMENTS not found in JSON:")
        for m in sorted(missing):
            print(f"  {m}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {updated}/{len(ENRICHMENTS)} remaining-species entries")


if __name__ == "__main__":
    apply_enrichments()
