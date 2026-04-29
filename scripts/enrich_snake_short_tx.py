#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# Snake Phase 2 (4件)
# ============================================================

ENRICHMENTS["snake_0093"] = {
    "treatment_ja": (
        "ヘビの骨折。"
        "★ヘビには四肢がないため、この項目は肋骨骨折/椎骨骨折として扱う★。"
        "外傷（圧迫、蓋挟み）、MBD、不適切なハンドリングが原因。"
        "■臨床症状: "
        "  局所腫脹、体幹の異常な角度（キンク）、移動時の疼痛反応。"
        "  肋骨骨折: 呼吸異常、体側の膨隆。"
        "  触診で捻髪音 or 不安定性。"
        "■診断: X線（骨折部位、MBDの有無）。ヘビは椎骨が200-400個あるため部位特定に全身撮影が必要。"
        "■疼痛管理: "
        "  メロキシカム 0.1-0.2 mg/kg PO/IM q24-48h。"
        "  トラマドール 5-10 mg/kg PO q48-72h。"
        "  — 前半身に投与（腎門脈系 — 後半身注射は薬物が腎臓を直接通過）。"
        "■保存療法（大半の症例）: "
        "  ケージレスト: 体長の1/3程度の小さいケージ。登攀物除去。"
        "  固定: テープスプリント（体幹に沿わせる）。6-12週。"
        "  基材: ペーパータオル（清潔維持）。"
        "■外科療法（重度の不安定骨折）: "
        "  髄内ピン（椎骨）。サークラージュワイヤー。"
        "  — ヘビの外科的骨折修復は技術的に困難（小さい椎骨が多数）。"
        "■MBD是正: UVB照射（夜行性種でも必要とする報告あり）、Ca補充、ビタミンD3。"
        "■感染予防: セフタジジム 20 mg/kg IM q72h（前半身に投与）。"
        "■予後: 単純骨折→良好（自然治癒力あり）。脊髄損傷合併→不良。多発骨折(MBD)→飼育改善が前提。"
        "参考文献: Divers & Stahl (2019); Jacobson ER (2007); Mader (2006)."
    ),
}

ENRICHMENTS["snake_0094"] = {
    "treatment_ja": (
        "ヘビの骨折（甲羅/背甲）。"
        "★ヘビには甲羅がないため、この項目は体壁損傷/肋骨骨折として扱う★。"
        "咬傷（生き餌の反撃、同居個体間の闘争）、圧迫事故が原因。"
        "■臨床症状: "
        "  体側の腫脹・変形、開放創、内臓露出（重度）。"
        "  移動困難、防御姿勢。"
        "■初期安定化: "
        "  疼痛: メロキシカム 0.1-0.2 mg/kg IM q24-48h（前半身投与）。"
        "  輸液: 乳酸リンゲル 10-20 mL/kg/day SC（前半身）。"
        "  POTZ維持。"
        "■創傷管理: "
        "  洗浄: 0.05%クロルヘキシジン or 生理食塩水。"
        "  壊死組織デブリードマン。湿潤療法（ハイドロゲル）。"
        "  ヘビの鱗は治癒後に瘢痕鱗として再生。"
        "■体壁修復: "
        "  筋層＋皮膚の縫合（4-0 PDS or ナイロン）。"
        "  内臓露出: 腹腔洗浄→臓器還納→体壁閉鎖。"
        "■感染管理: "
        "  セフタジジム 20 mg/kg IM q72h。"
        "  咬傷（生き餌由来）: Pseudomonas等のグラム陰性菌カバー。"
        "■予防: 冷凍/解凍餌への切替（生き餌のげっ歯類はヘビを重傷させうる）。"
        "■予後: 表層→良好。内臓損傷→慎重。次の脱皮で瘢痕鱗に置換。"
        "参考文献: Divers & Stahl (2019); Mader (2006)."
    ),
}

ENRICHMENTS["snake_spinal_fracture___vertebral_luxation"] = {
    "treatment_ja": (
        "ヘビの脊椎骨折/椎骨脱臼。外傷（蓋挟み、落下）、MBDが原因。"
        "ヘビは200-400個の椎骨を持つため骨折部位の特定が重要。"
        "■神経学的評価: "
        "  骨折部位より尾側の反射消失（体幹-尾反射、総排泄腔反射）。"
        "  痛覚テスト: 鉗子による尾部刺激への反応。"
        "  ★ヘビの脊髄損傷は骨折部位から尾側が完全麻痺 → 移動能力の喪失★。"
        "■診断: 全身X線（骨折部位特定）。CT（利用可能なら）。"
        "■急性期: "
        "  疼痛: メロキシカム 0.1-0.2 mg/kg IM q24-48h（前半身投与）。"
        "  脊髄浮腫: デキサメタゾン 0.5-1.0 mg/kg IM（受傷8時間以内）。"
        "  輸液: 乳酸リンゲル SC（前半身）。"
        "■保存療法: "
        "  小さいケージでケージレスト 6-12週。"
        "  テープスプリントで骨折部固定。"
        "  基材: ペーパータオル（清潔維持）。"
        "■外科療法: "
        "  椎骨固定: 髄内ピン or 骨セメント（技術的に非常に困難）。"
        "  — 大型ボア・パイソンでのみ現実的。小型種は保存療法が主。"
        "■長期管理: "
        "  排泄: 温浴で排泄促進。"
        "  給餌: 骨折が体幹前半→嚥下困難の可能性 → アシスト給餌。"
        "  褥瘡予防: 柔らかい基材。"
        "■予後: 頭部に近い骨折→不良（呼吸筋影響）。尾部寄り→生活の質維持可能。"
        "参考文献: Divers & Stahl (2019); Jacobson (2007); Mader (2006)."
    ),
}

ENRICHMENTS["snake_intestinal_volvulus___intussusception"] = {
    "treatment_ja": (
        "ヘビの腸捻転/腸重積。基材誤食（アスペンチップ、ヤシガラ）、寄生虫（Cryptosporidium等）、腫瘍が原因。"
        "■臨床症状: "
        "  吐き戻し（regurgitation — ヘビに多い）、排便停止。"
        "  体幹中央部の腫脹 or 硬結（触診）。"
        "  食欲廃絶、嗜眠。"
        "■診断: "
        "  X線: 腸管拡張、基材の放射線不透過像。"
        "  超音波: target sign。"
        "  造影: バリウム通過遅延。"
        "■初期安定化: "
        "  輸液: 乳酸リンゲル 10-25 mL/kg/day SC（前半身）。"
        "  POTZ維持。"
        "  疼痛: メロキシカム 0.1-0.2 mg/kg IM + ブトルファノール 0.4 mg/kg IM。"
        "  抗菌薬: セフタジジム 20 mg/kg IM + メトロニダゾール 20 mg/kg PO。"
        "■外科療法: "
        "  体側アプローチで開腹（coeliotomy）。"
        "  ★ヘビの消化管は非常に長い（体長の90%）→ 全消化管の触診が必須★。"
        "  腸重積: 用手的整復。壊死→腸切除吻合。"
        "  捻転: 整復＋viability評価。"
        "  基材性閉塞: 腸切開で除去。"
        "■術後管理: "
        "  絶食7-14日（ヘビの正常消化期間は長い）。"
        "  小型餌から再開（通常の1/2サイズ）。"
        "  基材変更: 新聞紙 or ペーパータオル。"
        "■予後: 単純閉塞→良好。壊死/穿孔→不良。Cryptosporidium合併→予後不良。"
        "参考文献: Divers & Stahl (2019); Mader (2006)."
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} snake entries")


if __name__ == "__main__":
    apply_enrichments()
