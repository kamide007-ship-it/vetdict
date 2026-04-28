#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# Lizard Phase 2 (5件)
# ============================================================

# --- Batch 1: MBD, Limb Fracture, Shell/Carapace Fracture ---

ENRICHMENTS["lizard_0019"] = {
    "treatment_ja": (
        "トカゲの代謝性骨疾患（MBD/NSHP）。Ca欠乏・UVB不足・ビタミンD3不足が原因。"
        "特にフトアゴヒゲトカゲ、カメレオン、イグアナに多い。"
        "■急性期（低Ca痙攣/振戦）: "
        "  グルコン酸カルシウム10%: 50-100 mg/kg IM/ICe（緩徐投与）。"
        "  — 心拍モニタリング（徐脈に注意）。"
        "  経口投与不可能な場合: 骨髄内（ICe）ルート。"
        "  保温: POTZ内（免疫・Ca代謝に必須）。"
        "■維持療法: "
        "  カルシウム補充: 炭酸Ca粉末を食事にダスティング q24-48h。"
        "  ビタミンD3: 経口補充（UVB不足時のみ）。過剰→高Ca血症リスク。"
        "  ★UVB照射が最重要★: "
        "    10-12% UVBランプ（砂漠種: フトアゴ、ウロマスティクス等）。"
        "    5-6% UVBランプ（森林種: カメレオン、ヤモリ等）。"
        "    照射距離: 30-45cm。1日10-12時間。6ヶ月毎にランプ交換。"
        "    — メッシュ蓋はUVBを30-50%減衰 → 直接照射が理想。"
        "■食事改善: "
        "  昆虫食種: Caダスティング済みコオロギ/デュビア。ガットローディング実施。"
        "  草食種（イグアナ等）: コマツナ、チンゲン菜、タンポポ葉（高Ca野菜）。"
        "  ★ホウレンソウ/リンゴはシュウ酸含有でCa吸収を阻害 → 制限★。"
        "  Ca:P比2:1以上を維持。"
        "■リハビリ: 骨折例は6-12週のケージレスト。浅い温浴で浮力を利用した運動。"
        "■予後: 早期（骨変形前）→良好。重度の骨変形・病的骨折は不可逆的。下顎ゴム化は回復困難。"
        "参考文献: Mader (2006); Divers & Stahl (2019); de Vosjoli P (2012) The Bearded Dragon Manual."
    ),
}

ENRICHMENTS["lizard_0095"] = {
    "treatment_ja": (
        "トカゲの四肢骨折。外傷（ケージ落下、ドア挟み）またはMBDによる病的骨折。"
        "自切後の断端外傷も含む（尾椎は再生するが四肢は再生しない）。"
        "■初期評価: "
        "  X線: 骨折型。MBDの有無（骨密度低下、皮質菲薄化）。"
        "  血液検査: Ca, P, ALP。"
        "■疼痛管理: "
        "  メロキシカム 0.1-0.2 mg/kg PO/IM q24-48h。"
        "  トラマドール 5-10 mg/kg PO q48-72h。"
        "  — 後肢注射は避ける（腎門脈系で薬物が直接腎臓を通過）。"
        "■保存療法: "
        "  小型種（ヤモリ、アノール等）: テープスプリント or ボールバンデージ。"
        "  固定6-12週（爬虫類は哺乳類より骨治癒が遅い）。"
        "  ケージレスト: 登攀を制限。"
        "■外科療法: "
        "  中-大型種（イグアナ、フトアゴ等）: "
        "    髄内ピン＋サークラージュワイヤー。"
        "    創外固定器（mini ESF）。"
        "  截肢: 粉砕骨折 or 壊死時。"
        "    — トカゲは3肢で良好なQOLを維持可能。"
        "■感染予防: セフタジジム 20 mg/kg IM q72h（開放骨折）。"
        "■MBD是正: UVB照射＋Ca補充（病的骨折の根本原因を治療しないと再骨折）。"
        "■予後: 単純骨折→良好。MBD+多発骨折→慎重（飼育環境改善が前提）。"
        "参考文献: Divers & Stahl (2019); Mitchell & Tully (2016); Mader (2006)."
    ),
}

ENRICHMENTS["lizard_0096"] = {
    "treatment_ja": (
        "トカゲの骨折（甲羅/体壁）。"
        "★トカゲには甲羅がないため、この項目は肋骨骨折/体壁損傷として扱う★。"
        "犬咬傷・踏みつけ・圧迫事故が原因。"
        "■臨床症状: "
        "  呼吸困難（肋骨骨折→肺損傷の可能性）。"
        "  腹壁の膨隆・変形。触診で捻髪音。"
        "  体腔臓器の脱出（重度の体壁損傷）。"
        "■初期安定化: "
        "  疼痛: メロキシカム 0.1-0.2 mg/kg IM q24-48h。"
        "  輸液: 乳酸リンゲル 10-20 mL/kg/day SC。"
        "  呼吸困難: 酸素投与。"
        "  POTZ維持。"
        "■治療: "
        "  肋骨骨折: 通常は保存療法（ケージレスト4-8週）。"
        "  体壁損傷: 外科的修復（筋層＋皮膚縫合）。"
        "  体腔露出/臓器脱出: 緊急手術。洗浄→臓器還納→体壁閉鎖。"
        "■感染管理: "
        "  セフタジジム 20 mg/kg IM q72h。"
        "  咬傷例: 嫌気性菌カバー（メトロニダゾール 20 mg/kg PO q48h）。"
        "■環境: 清潔な基材（ペーパータオル）。登攀制限。温度勾配維持。"
        "■予後: 単純肋骨骨折→良好。体腔露出→慎重。"
        "参考文献: Divers & Stahl (2019); Mader (2006)."
    ),
}

# --- Batch 2: Spinal Fracture, Intestinal Volvulus ---

ENRICHMENTS["lizard_spinal_fracture___vertebral_luxation"] = {
    "treatment_ja": (
        "トカゲの脊椎骨折/椎骨脱臼。外傷（落下・犬咬傷・ドア挟み）、MBDによる病的骨折。"
        "■神経学的評価: "
        "  後肢反射、総排泄腔反射、尾反射、深部痛覚。"
        "  ★尾の自切は脊髄損傷の評価を複雑にする — 尾より近位の反射で評価★。"
        "  X線: 骨折部位・転位。CT/MRI（利用可能なら）。"
        "■急性期: "
        "  安静: 最小限のケージ（登攀不可に設定）。"
        "  疼痛: メロキシカム 0.1-0.2 mg/kg IM q24-48h。"
        "  脊髄浮腫: デキサメタゾン 0.5-1.0 mg/kg IM（受傷8時間以内）。"
        "  輸液: 乳酸リンゲル SC（前肢から投与 — 腎門脈系回避）。"
        "■保存療法（不完全麻痺/安定骨折）: "
        "  ケージレスト 6-12週。床面積のみの平置きケージ。"
        "  膀胱管理: 温浴で排泄促進。用手圧迫。"
        "■外科療法: "
        "  不安定骨折: 髄内ピン＋PMMA＋サークラージュワイヤー。"
        "  — トカゲの脊椎手術は体格が許す場合のみ実施可能。"
        "■MBD評価・是正: 血液Ca/P、UVB、食事改善。"
        "■截肢: 後肢完全麻痺＋排泄制御不能の場合、後肢截肢も選択肢。"
        "  — 前肢が正常なら前肢のみで移動可能。"
        "■予後: 深部痛覚あり→回復の余地。深部痛覚消失→歩行回復困難。"
        "参考文献: Divers & Stahl (2019); Mader (2006); Mitchell & Tully (2016)."
    ),
}

ENRICHMENTS["lizard_intestinal_volvulus___intussusception"] = {
    "treatment_ja": (
        "トカゲの腸捻転/腸重積。異物摂取（基材の誤食: 砂、バークチップ）、寄生虫、腫瘍が原因。"
        "■臨床症状: "
        "  急性食欲廃絶、排便停止、腹部膨満。"
        "  嗜眠、暗い体色変化（ストレスサイン — カメレオン等）。"
        "  総排泄腔からの腸管脱出（腸重積進行例）。"
        "■診断: "
        "  X線: 腸管拡張、基材による放射線不透過像。"
        "  超音波: target sign（腸重積の特徴像）。"
        "  造影: バリウム通過遅延。"
        "■初期安定化: "
        "  輸液: 乳酸リンゲル 10-25 mL/kg/day SC（前肢側から）。"
        "  POTZ維持。"
        "  疼痛: メロキシカム 0.1-0.2 mg/kg IM + ブトルファノール 0.4 mg/kg IM。"
        "  抗菌薬: セフタジジム 20 mg/kg IM + メトロニダゾール 20 mg/kg PO。"
        "■外科療法: "
        "  開腹術（coeliotomy）。"
        "  腸重積: 用手的整復を試行。壊死→腸切除吻合。"
        "  捻転: 整復。壊死部分は切除。"
        "  基材性イレウス: 腸切開で基材除去。"
        "  — 4-0〜5-0 PDS単層結節縫合。"
        "■術後管理: "
        "  絶食48-72h。少量の流動食（昆虫ペースト）から再開。"
        "  環境改善: 砂/バーク基材をペーパータオル or タイル等に変更（再発予防）。"
        "■予後: 早期手術→良好。壊死/腹膜炎→不良。基材性イレウスは再発しやすい。"
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} lizard entries")


if __name__ == "__main__":
    apply_enrichments()
