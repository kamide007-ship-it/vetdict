#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# Parakeet Phase 3: De-duplicate viral disease template (22件)
# ============================================================

ENRICHMENTS["parakeet_0009"] = {
    "treatment_ja": (
        "セキセイインコのヘルペスウイルス感染症（Budgerigar herpesvirus, BHV）。"
        "パケコ病関連（PsHV-1とは異なる株 — BHV固有）。"
        "■臨床症状: 肝壊死（急性死）、口内炎、結膜炎。"
        "  幼鳥で致死率が高い。成鳥は不顕性キャリア。"
        "■治療: アシクロビル 80 mg/kg PO q8h × 7-14日（有効性報告あり）。"
        "  保温28-30℃。輸液SC/IO。"
        "  肝保護: シリマリン 50-100 mg/kg PO q24h。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。強制給餌。"
        "■感染管理: 潜伏感染→終生キャリア。ストレス時再活性化。隔離。"
        "■予後: 急性肝壊死型→不良。粘膜限局型→管理可能。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_0019"] = {
    "treatment_ja": (
        "インコの鳥インフルエンザ。★HPAIは法定伝染病・殺処分対象★。"
        "■臨床症状: 急性死、沈鬱、呼吸困難。"
        "■治療（LPAI）: 保温28-30℃。輸液SC/IO。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO/IM q12h。強制給餌。"
        "■感染管理: HPAI疑い→獣医当局通報。厳格隔離。"
        "■予後: HPAI→致死的。LPAI→回復可能。"
        "参考文献: Swayne DE (2020); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_0020"] = {
    "treatment_ja": (
        "インコのポリオーマウイルス感染症（APV）。"
        "★セキセイインコでは「フレンチモルト」の原因★。幼鳥で致死的。"
        "■臨床症状: "
        "  幼鳥: 急性死、腹水、皮下出血、肝腫大。"
        "  フレンチモルト: 風切羽/尾羽の異常脱落（羽毛嚢壊死）。"
        "  成鳥: 通常無症状キャリア。"
        "■診断: 血液/糞便/羽毛PCR。組織病理: 核内封入体。"
        "■治療（支持療法）: 保温28-30℃。輸液SC/IO。"
        "  出血: ビタミンK1 0.5-2.5 mg/kg IM。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。強制給餌。"
        "■感染管理: 糞口/エアロゾル/羽毛粉塵感染。環境安定。"
        "  繁殖施設: PCRスクリーニング。"
        "■予後: 幼鳥→不良。フレンチモルト→美容的問題だが飛行能力に影響。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_0023"] = {
    "treatment_ja": (
        "インコの鳥ボルナウイルス/腺胃拡張症（ABV/PDD）。"
        "■臨床症状: 未消化穀物排泄、嘔吐、体重減少。神経症状。"
        "■治療（長期管理）: "
        "  メロキシカム 0.5-1.0 mg/kg PO q12-24h（神経節炎抑制）。"
        "  セレコキシブ 10-20 mg/kg PO q12h。"
        "  消化しやすい食餌。強制給餌。"
        "  カンジダ合併: ニスタチン 300,000 IU/kg PO q8-12h。"
        "■感染管理: 不顕性キャリア多い。PCR+抗体スクリーニング。"
        "■予後: 慎重〜不良。抗炎症療法で延命可能。"
        "参考文献: Hoppes S et al. (2013); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_0025"] = {
    "treatment_ja": (
        "インコの鳥痘。蚊媒介/接触感染。"
        "■乾燥型: 痂皮。自然治癒。■湿潤型: 口腔偽膜。★気道閉塞リスク★。"
        "■治療: 乾燥型→局所消毒。湿潤型→偽膜除去、呼吸確保。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "  保温。輸液。強制給餌。ビタミンA。"
        "■予後: 乾燥型→良好。湿潤型→慎重。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_0134"] = {
    "treatment_ja": (
        "インコの肝炎ウイルス感染症。ヘルペス、ポリオーマ、アデノウイルス等。"
        "■治療: 保温28-30℃。輸液SC/IO。"
        "  肝保護: シリマリン 50-100 mg/kg PO q24h。SAMe 20 mg/kg PO q24h。"
        "  ウルソデオキシコール酸 10-15 mg/kg PO q24h。"
        "  ヘルペス疑い: アシクロビル 80 mg/kg PO q8h。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。強制給餌。"
        "■予後: 原因ウイルスと肝障害の重症度による。"
        "参考文献: Speer BL (2016); Ritchie BW et al. (1994)."
    ),
}

ENRICHMENTS["parakeet_0140"] = {
    "treatment_ja": (
        "インコの消化管ウイルス感染症。ロタウイルス、ボルナウイルス（PDD）、アデノウイルス等。"
        "■治療: 保温28-30℃。脱水補正（輸液SC/IO）。"
        "  消化管保護: スクラルファート 25-50 mg/kg PO q8h。"
        "  少量頻回給餌。消化しやすい食餌。"
        "  PDD疑い: メロキシカム 0.5-1.0 mg/kg PO q12-24h。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "■予後: ロタウイルス→回復可能。PDD→慎重〜不良。"
        "参考文献: Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_0148"] = {
    "treatment_ja": (
        "インコの呼吸器ウイルス感染症。ヘルペス、PMV、メタニューモウイルス等。"
        "■治療: 保温28-30℃。"
        "  ネブライゼーション: 生理食塩水 ± ゲンタマイシン q12h。"
        "  副鼻腔炎: 生理食塩水洗浄。"
        "  輸液SC/IO。強制給餌。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO/IM q12h。"
        "  重度: 酸素投与。エアサックチューブ。"
        "■予後: 軽度→回復可能。重度肺炎→慎重。"
        "参考文献: Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_0156"] = {
    "treatment_ja": (
        "インコの皮膚ウイルス感染症。ポックス、パピローマ、サーコウイルス（PBFD）等。"
        "■治療: ポックス→自然治癒。パピローマ→外科切除。"
        "  PBFD→特異的治療なし（支持療法＋QOL管理）。"
        "  保温。栄養支持。二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "■予後: ポックス→良好。PBFD→不良。"
        "参考文献: Speer BL (2016); Ritchie BW et al. (1994)."
    ),
}

ENRICHMENTS["parakeet_0168"] = {
    "treatment_ja": (
        "インコの神経性ウイルス感染症。ボルナウイルス（PDD）、PMV、ポリオーマ等。"
        "■治療: "
        "  痙攣: ジアゼパム 0.5-1.0 mg/kg IM/IN。ミダゾラム 0.3-0.5 mg/kg IN。"
        "  PDD: メロキシカム 0.5-1.0 mg/kg PO q12-24h。"
        "  保温。輸液。強制給餌。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "■予後: PDD→慎重〜不良。PMV→回復例あり。"
        "参考文献: Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_0176"] = {
    "treatment_ja": (
        "インコの眼科ウイルス感染症。ヘルペス、マイコプラズマ、PMV等。"
        "■治療: "
        "  二次感染予防: オフロキサシン点眼 0.3% q6-8h。"
        "  ヘルペス疑い: アシクロビル眼軟膏 3% 5回/日。"
        "  保温。輸液。強制給餌。"
        "■予後: 結膜炎→良好。角膜潰瘍→治療反応による。"
        "参考文献: Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_0203"] = {
    "treatment_ja": (
        "インコの生殖器ウイルス感染症。ヘルペスウイルス等が卵管炎の原因。"
        "■治療: 支持療法。保温。輸液。"
        "  卵管炎/卵詰まり合併: Ca補充 + オキシトシン投与 or 外科的介入。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "  繁殖抑制: 光周期管理（暗期12-14h/日）、デスロレリン/ロイプロリド。"
        "■予後: 支持療法で管理可能。卵管破裂→緊急。"
        "参考文献: Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_0208"] = {
    "treatment_ja": (
        "インコの全身性ウイルス感染症。ポリオーマ、サーコウイルス、アデノウイルス等。"
        "多臓器障害。幼鳥で致死率が高い。"
        "■治療（支持療法）: 保温28-30℃。輸液SC/IO。"
        "  肝保護: シリマリン。ビタミンK1（凝固障害時）。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。強制給餌。"
        "■予後: 幼鳥→不良。成鳥→原因ウイルスによる。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_0241"] = {
    "treatment_ja": (
        "セキセイインコのサーコウイルス（Budgerigar Circovirus）。"
        "PBFD（嘴羽毛病ウイルス — BFDV）とは異なる株。免疫抑制を引き起こす。"
        "■臨床症状: 免疫抑制（二次感染に易感受性）、"
        "  羽毛異常（軽度 — PBFDほど重篤でない）。"
        "■診断: PCR（血液/羽毛）。"
        "■治療（支持療法）: 保温。輸液。栄養支持。"
        "  二次感染の積極的治療（細菌: エンロフロキサシン、真菌: イトラコナゾール）。"
        "■感染管理: 糞口/羽毛粉塵感染。環境消毒。隔離。"
        "■予後: PBFDより良好。免疫回復で自然クリアランスの可能性。"
        "参考文献: Raue R et al. (2004); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_polyomavirus_infection"] = {
    "treatment_ja": (
        "インコのポリオーマウイルス感染症。parakeet_0020参照。"
        "幼鳥で致死的。フレンチモルト。成鳥は不顕性キャリア。"
        "■治療: 保温。輸液。ビタミンK1（出血時）。"
        "  セフタジジム or エンロフロキサシン（二次感染）。強制給餌。"
        "■感染管理: PCRスクリーニング。環境消毒。"
        "■予後: 幼鳥→不良。成鳥→無症状キャリア。"
        "参考文献: Ritchie BW et al. (1994)."
    ),
}

ENRICHMENTS["parakeet_paramyxovirus_infection_pmv"] = {
    "treatment_ja": (
        "インコのパラミクソウイルス感染症（PMV）。"
        "★PMV-1（NDV関連）は法定伝染病の可能性★。"
        "■臨床症状: 神経（斜頸、振戦）、呼吸器（鼻汁）、消化器（緑色下痢）。"
        "■治療: 保温。輸液SC/IO。"
        "  痙攣: ジアゼパム 0.5-1.0 mg/kg IM。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。強制給餌。"
        "■感染管理: NDV疑い→当局通報。隔離。"
        "■予後: 神経症状→慎重。軽症→回復例あり。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_circovirus_infection_non-pbfd"] = {
    "treatment_ja": (
        "インコのサーコウイルス（非PBFD株）。免疫抑制が主。"
        "■治療: 支持療法。二次感染の積極治療。"
        "  エンロフロキサシン 15 mg/kg PO q12h。栄養支持。"
        "■予後: PBFDより良好。免疫回復で改善可能。"
        "参考文献: Raue R et al. (2004); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_avian_herpesvirus_infection"] = {
    "treatment_ja": (
        "インコのヘルペスウイルス感染症。パケコ病/口内炎型。"
        "■治療: アシクロビル 80 mg/kg PO q8h × 7-14日。"
        "  口腔潰瘍: クロルヘキシジン0.05%洗浄。"
        "  保温。輸液。肝保護（シリマリン）。強制給餌。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "■感染管理: 潜伏感染→終生キャリア。隔離。"
        "■予後: 粘膜型→管理可能。劇症型→致死的。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_reovirus_infection"] = {
    "treatment_ja": (
        "インコのレオウイルス感染症。肝炎・腸炎の原因。幼鳥で重症化。"
        "■治療: 保温。輸液SC/IO。"
        "  肝保護: シリマリン 50-100 mg/kg PO q24h。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。強制給餌。"
        "■予後: 幼鳥→慎重。成鳥→回復例あり。"
        "参考文献: Ritchie BW et al. (1994)."
    ),
}

ENRICHMENTS["parakeet_adenovirus_infection"] = {
    "treatment_ja": (
        "インコのアデノウイルス感染症。肝壊死。幼鳥で急性死。"
        "■治療: 保温。輸液SC/IO。"
        "  肝保護: シリマリン 50-100 mg/kg PO q24h。SAMe 20 mg/kg PO q24h。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。強制給餌。"
        "■予後: 幼鳥→不良。成鳥→回復例。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_psittacine_poxvirus_parakeet"] = {
    "treatment_ja": (
        "インコの鳥痘ウイルス（Psittacine poxvirus）。parakeet_0025参照。"
        "乾燥型（痂皮）と湿潤型（口腔偽膜）。"
        "■治療: 乾燥型→自然治癒。湿潤型→偽膜除去、気道確保。"
        "  二次感染: エンロフロキサシン 15 mg/kg PO q12h。"
        "  保温。輸液。強制給餌。ビタミンA。"
        "■予後: 乾燥型→良好。湿潤型→慎重。"
        "参考文献: Ritchie BW et al. (1994); Speer BL (2016)."
    ),
}

ENRICHMENTS["parakeet_papillomavirus_infection"] = {
    "treatment_ja": (
        "インコのパピローマウイルス感染症。"
        "総排泄腔、消化管の乳頭腫（疣贅）が特徴。"
        "■治療: 外科的切除（レーザー/電気焼灼）。"
        "  凍結療法（液体窒素）。"
        "  再発率が高い — 定期的モニタリング。"
        "  メロキシカム 0.5 mg/kg PO q12-24h（術後疼痛管理）。"
        "■予後: 良好だが再発しやすい。悪性転化は稀。"
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} parakeet entries")


if __name__ == "__main__":
    apply_enrichments()
