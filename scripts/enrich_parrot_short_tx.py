#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# Parrot Phase 3: De-duplicate viral disease template (14件)
# ============================================================

ENRICHMENTS["parrot_0018"] = {
    "treatment_ja": (
        "オウムの鳥インフルエンザ（AI）。★HPAIは法定伝染病・殺処分対象★。"
        "■臨床症状: 急性死、沈鬱、呼吸困難、神経症状。"
        "■治療（LPAI/コンパニオンバード）: "
        "  保温28-30℃。輸液（温乳酸リンゲルSC/IO）。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO/IM q12h。"
        "  強制給餌。オセルタミビル 2 mg/kg PO q12h（研究段階）。"
        "■感染管理: HPAI疑い→獣医当局に通報。厳格隔離。"
        "■予後: HPAI→致死的。LPAI→回復可能。"
        "参考文献: Swayne DE (2020); Speer BL (2016)."
    ),
}

ENRICHMENTS["parrot_0019"] = {
    "treatment_ja": (
        "オウムのポリオーマウイルス感染症（APV — Avian Polyomavirus）。"
        "幼鳥で急性致死的。成鳥は不顕性キャリア。"
        "■臨床症状: "
        "  幼鳥: 急性死、皮下出血、腹水、肝腫大。羽毛異常（フレンチモルト）。"
        "  成鳥: 通常無症状。免疫抑制で発症。"
        "■診断: 血液/糞便/羽毛PCR。組織病理: 核内封入体。"
        "■治療（支持療法 — 特異的治療なし）: "
        "  保温28-30℃。輸液SC/IO。"
        "  出血傾向: ビタミンK1 0.5-2.5 mg/kg IM。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO/IM q12h。"
        "  強制給餌。"
        "■感染管理: "
        "  糞口/エアロゾル/羽毛粉塵から感染。環境安定なウイルス。"
        "  繁殖施設: PCRスクリーニング。陽性鳥の隔離。"
        "■予後: 幼鳥→不良。成鳥キャリア→多くは無症状で長期生存。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parrot_0022"] = {
    "treatment_ja": (
        "オウムの鳥ボルナウイルス感染症（ABV）/腺胃拡張症（PDD）。"
        "オウム目全般に感染。慢性消耗性疾患。"
        "■臨床症状: 未消化穀物排泄、嘔吐、体重減少、腺胃拡張。神経症状（運動失調、痙攣）。"
        "■診断: 造影X線（腺胃拡張）。PCR。嗉嚢生検（リンパ球性神経節炎）。"
        "■治療（根治不能 — 長期管理）: "
        "  メロキシカム 0.5-1.0 mg/kg PO q12-24h（中心的治療 — 神経節炎抑制）。"
        "  セレコキシブ 10-20 mg/kg PO q12h（長期使用に優位性の報告）。"
        "  消化しやすい食餌。強制給餌。"
        "  二次感染（カンジダ）: ニスタチン 300,000 IU/kg PO q8-12h。"
        "■感染管理: 糞口/エアロゾル感染。不顕性キャリア多い。PCR+抗体スクリーニング。"
        "■予後: 慎重〜不良。抗炎症療法で数ヶ月-数年延命可能。"
        "参考文献: Hoppes S et al. (2013); Speer BL (2016)."
    ),
}

ENRICHMENTS["parrot_0024"] = {
    "treatment_ja": (
        "オウムの鳥痘（Avian Pox）。蚊媒介/接触感染。"
        "■乾燥型: 無毛部に丘疹→痂皮。自然治癒2-4週。"
        "■湿潤型: 口腔/喉頭に偽膜。★気道閉塞リスク★。"
        "■治療: "
        "  乾燥型: 局所消毒（ポビドンヨード）。自然治癒を待つ。"
        "  湿潤型: 偽膜除去。呼吸困難→酸素/エアサックチューブ。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO/IM q12h。"
        "  保温。輸液。強制給餌。"
        "  ビタミンA 5,000-10,000 IU/kg IM（粘膜修復）。"
        "■感染管理: 蚊対策。隔離。"
        "■予後: 乾燥型→良好。湿潤型→慎重。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parrot_0136"] = {
    "treatment_ja": (
        "オウムの肝炎ウイルス感染症。ヘルペスウイルス（パケコ病）、"
        "ポリオーマウイルス、アデノウイルス等が原因。"
        "■臨床症状: 食欲廃絶、嗜眠、黄疸（蝋膜の変色で確認）。"
        "■治療（支持療法）: 保温28-30℃。輸液SC/IO。"
        "  肝保護: シリマリン 50-100 mg/kg PO q24h。SAMe 20 mg/kg PO q24h。"
        "  ウルソデオキシコール酸 10-15 mg/kg PO q24h。"
        "  ビタミンK1（凝固障害時）。強制給餌。"
        "  パケコ病疑い: アシクロビル 80 mg/kg PO q8h。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "■予後: パケコ病→致死率高い。他の原因→支持療法で管理可能。"
        "参考文献: Speer BL (2016); Ritchie BW et al. (1994)."
    ),
}

ENRICHMENTS["parrot_0142"] = {
    "treatment_ja": (
        "オウムの消化管ウイルス感染症。ロタウイルス、"
        "ボルナウイルス（PDD）、アデノウイルス等。"
        "■臨床症状: 下痢、嘔吐、体重減少。未消化穀物排泄（PDD）。"
        "■治療（支持療法）: 保温28-30℃。"
        "  脱水補正: 輸液SC/IO。"
        "  消化管保護: スクラルファート 25-50 mg/kg PO q8h。"
        "  少量頻回給餌。消化しやすい食餌。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "  PDD疑い: メロキシカム 0.5-1.0 mg/kg PO q12-24h。"
        "■予後: ロタウイルス→回復可能。PDD→慎重〜不良。"
        "参考文献: Speer BL (2016)."
    ),
}

ENRICHMENTS["parrot_0150"] = {
    "treatment_ja": (
        "オウムの呼吸器ウイルス感染症。ヘルペスウイルス、PMV、"
        "メタニューモウイルス等。"
        "■臨床症状: 鼻汁、くしゃみ、開口呼吸、気管ラ音、副鼻腔腫脹。"
        "■治療（支持療法）: 保温28-30℃。"
        "  ネブライゼーション: 生理食塩水 ± ゲンタマイシン q12h 15分。"
        "  副鼻腔炎: 生理食塩水洗浄（鎮静下）。"
        "  輸液SC/IO。強制給餌。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO/IM q12h。"
        "  重度呼吸困難: 酸素投与。エアサックチューブ（気管閉塞時）。"
        "■予後: 軽度→支持療法で回復。重度肺炎→慎重。"
        "参考文献: Speer BL (2016); Ritchie BW et al. (1994)."
    ),
}

ENRICHMENTS["parrot_0158"] = {
    "treatment_ja": (
        "オウムの皮膚ウイルス感染症。ポックスウイルス、"
        "パピローマウイルス、サーコウイルス（PBFD — 嘴羽毛病）等。"
        "■臨床症状: 皮膚痂皮、羽毛異常、嘴変形（PBFD）。"
        "■治療: "
        "  ポックス: 自然治癒。局所消毒。"
        "  パピローマ: 外科切除/レーザー焼灼。"
        "  PBFD: 特異的治療なし。支持療法＋QOL管理。"
        "  保温。輸液。栄養支持。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "■予後: ポックス→良好。PBFD→不良（進行性）。"
        "参考文献: Speer BL (2016); Ritchie BW et al. (1994)."
    ),
}

ENRICHMENTS["parrot_avian_poxvirus"] = {
    "treatment_ja": (
        "オウムの鳥痘ウイルス。parrot_0024参照。"
        "乾燥型（皮膚痂皮）と湿潤型（口腔偽膜）。"
        "■治療: 乾燥型→自然治癒。湿潤型→偽膜除去、気道確保。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "  保温。輸液。強制給餌。ビタミンA。"
        "■予後: 乾燥型→良好。湿潤型→慎重。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parrot_paramyxovirus_infection_pmv"] = {
    "treatment_ja": (
        "オウムのパラミクソウイルス感染症（PMV）。PMV-1（ニューカッスル病関連）等。"
        "★PMV-1はNDV（ニューカッスル病ウイルス）と同義 — 法定伝染病の可能性★。"
        "■臨床症状: 神経（斜頸、振戦、運動失調）、呼吸器（鼻汁、肺炎）、消化器（緑色下痢）。"
        "■治療（支持療法）: 保温28-30℃。輸液SC/IO。"
        "  痙攣: ジアゼパム 0.5-1.0 mg/kg IM。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。強制給餌。"
        "■感染管理: NDV疑い→当局通報。厳格隔離。"
        "■予後: 神経症状→慎重。軽症→回復例あり。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parrot_circovirus_infection_non-pbfd_strains"] = {
    "treatment_ja": (
        "オウムのサーコウイルス感染症（非PBFD株）。"
        "PBFD（嘴羽毛病）以外のサーコウイルス株。免疫抑制を引き起こす。"
        "■臨床症状: 免疫抑制（二次感染に易感受性）、軽度の羽毛異常。"
        "■治療（支持療法）: 保温。輸液。栄養支持。"
        "  二次感染（細菌/真菌）の積極的治療。"
        "  エンロフロキサシン 15 mg/kg PO q12h + 抗真菌薬（必要時）。"
        "■予後: PBFD株より良好。免疫回復で自然クリアランスの可能性。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parrot_avian_herpesvirus_non-pacheco's"] = {
    "treatment_ja": (
        "オウムのヘルペスウイルス感染症（パケコ病以外）。"
        "粘膜型（口腔潰瘍）、皮膚型等。PsHV-1の軽症型/異なる遺伝子型。"
        "■治療: アシクロビル 80 mg/kg PO q8h × 7-14日。"
        "  口腔潰瘍: クロルヘキシジン0.05%洗浄。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "  保温。輸液。強制給餌。"
        "■感染管理: 潜伏感染→終生キャリア。ストレス時の再活性化に注意。"
        "■予後: 粘膜限局型→管理可能。"
        "参考文献: Tomaszewski EK et al. (2003); Speer BL (2016)."
    ),
}

ENRICHMENTS["parrot_reovirus_infection"] = {
    "treatment_ja": (
        "オウムのレオウイルス感染症。肝炎、腸炎の原因。"
        "■臨床症状: 食欲不振、下痢、肝腫大。幼鳥で重症化。"
        "■治療（支持療法）: 保温。輸液SC/IO。"
        "  肝保護: シリマリン 50-100 mg/kg PO q24h。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。強制給餌。"
        "■予後: 幼鳥→慎重。成鳥→回復例あり。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parrot_adenovirus_infection"] = {
    "treatment_ja": (
        "オウムのアデノウイルス感染症。肝炎の原因。"
        "■臨床症状: 食欲廃絶、嗜眠、黄疸。急性死（幼鳥）。"
        "■治療（支持療法）: 保温。輸液SC/IO。"
        "  肝保護: シリマリン 50-100 mg/kg PO q24h。SAMe 20 mg/kg PO q24h。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。強制給餌。"
        "■予後: 幼鳥→不良。成鳥→支持療法で回復例。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} parrot entries")


if __name__ == "__main__":
    apply_enrichments()
