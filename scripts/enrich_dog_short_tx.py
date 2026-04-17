#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# --- Batch 1: IMHA, DM, 核硬化, 網膜形成不全 ---

ENRICHMENTS["dog_immune-mediated_hemolytic_anemia"] = {
    "treatment_ja": (
        "免疫抑制療法: プレドニゾロン2 mg/kg PO q12h（初期）→ 4-6週で漸減。"
        "第二免疫抑制薬（プレドニゾロン不応or漸減困難時）: "
        "  ミコフェノール酸モフェチル（MMF）10 mg/kg PO q12h、"
        "  シクロスポリン5 mg/kg PO q12h、"
        "  アザチオプリン2 mg/kg PO q24h（犬のみ — 猫禁忌）。"
        "急性重症: hIVIG（ヒト免疫グロブリン）0.5-1.5 g/kg IV single dose。"
        "輸血: PCV<15%で適応。交差適合試験実施。DEA 1.1陰性血を推奨。"
        "血栓予防: クロピドグレル1-2 mg/kg PO q24h +"
        "  低分子ヘパリン（LMWH）150-200 IU/kg SC q8h（高リスク期）。"
        "胃保護: オメプラゾール1 mg/kg PO q12h + スクラルファート。"
        "モニタリング: PCV/TS q6-12h（入院中）、網状赤血球数、球状赤血球、"
        "  自己凝集試験、Coombs試験。"
        "予後: 初回寛解率60-80%。再発率30-40%。血栓塞栓症が主要死因。"
    ),
}

ENRICHMENTS["dog_degenerative_myelopathy_dm"] = {
    "treatment_ja": (
        "根治療法なし。SOD1遺伝子変異（常染色体劣性）。"
        "好発: ジャーマンシェパード、ウェルシュコーギー、ボクサー。"
        "理学療法（進行遅延に最も有効）: "
        "  水中トレッドミル週3-5回、バランスボード、ROM（関節可動域）運動、"
        "  マッサージ、神経筋電気刺激（NMES）。"
        "補助器具: 後肢サポートハーネス（早期）、車椅子（後肢麻痺進行時）。"
        "  ブーツ/ソックス（ナックリング — 爪摩耗予防）。"
        "褥瘡予防: 低反発マット、定期的な体位変換。"
        "失禁管理: おむつ、膀胱の手圧排（必要時）。"
        "サプリメント: ビタミンE/C、EPA/DHA（エビデンス限定的）。"
        "QOL評価: 飼い主と定期的にQOLスケール（Lap of Love等）で評価。"
        "予後: 進行性。発症から起立不能まで6-12ヶ月。治癒不可。"
        "遺伝子検査: 繁殖プログラムでのスクリーニング推奨。"
    ),
}

ENRICHMENTS["dog_nuclear_sclerosis"] = {
    "treatment_ja": (
        "加齢性変化であり治療不要。水晶体核の圧縮・硬化による青白い外観。"
        "6-8歳以上の犬で生理的に発生。"
        "視力への影響は最小限（軽度の近視化）。"
        "白内障との鑑別が最も重要: "
        "  核硬化 — 直接検眼鏡で網膜タペタム反射が透見可能。"
        "  白内障 — 水晶体混濁で網膜が透見不可能。"
        "スリットランプ検査: 核硬化は水晶体核のみの均一な混濁、皮質は透明。"
        "  白内障は皮質・核・嚢の不均一な混濁。"
        "定期的眼科検査: 年1回（核硬化自体は進行しても視力に重大な影響なし）。"
        "  白内障への移行をモニタリング（特にDM犬で白内障リスク高）。"
        "飼い主への説明: 良性の加齢変化であり、手術は不要。"
    ),
}

ENRICHMENTS["dog_retinal_dysplasia"] = {
    "treatment_ja": (
        "根治療法なし。先天性（遺伝性 and/or 子宮内感染 — CHV, CAV-1）。"
        "重症度分類: "
        "  局所型（focal）: 網膜皺襞/ロゼット — 視力への影響最小、治療不要。"
        "  地理的型（geographic）: 不整な網膜菲薄化 — 軽度〜中等度視力障害。"
        "  完全型（complete）: 網膜全剥離 — 失明。治療不可。"
        "好発品種: ラブラドール、コッカースパニエル、ベドリントンテリア、"
        "  イングリッシュスプリンガースパニエル。"
        "環境適応: 失明犬の安全な生活環境整備（家具配置固定、階段ゲート）。"
        "遺伝子検査: 一部犬種で利用可能（繁殖プログラムからの除外）。"
        "合併症: 硝子体変性、二次性緑内障、水晶体脱臼のモニタリング。"
        "  完全型 + 硝子体変性 → 網膜前膜形成 → 牽引性網膜剥離。"
        "予後: 局所型は良好（機能的視力維持）。完全型は永久失明。"
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} dog disease entries")


if __name__ == "__main__":
    apply_enrichments()
