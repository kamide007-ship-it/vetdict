#!/usr/bin/env python3
"""馬の163件のテンプレート疾患を臨床的に充実した日本語内容で置換。

対象: diagnosis_jaがテンプレート文の疾患 + treatment_jaが短い疾患。

データソース:
- Reed SM, Bayly WM, Sellon DC: Equine Internal Medicine (4th ed, 2018)
- Auer JA, Stick JA: Equine Surgery (5th ed, 2019)
- Robinson NE, Sprayberry KA: Current Therapy in Equine Medicine (6th ed, 2009)
- Hinchcliff KW, Kaneps AJ, Geor RJ: Equine Sports Medicine and Surgery (2nd ed, 2014)
- Gilger BC: Equine Ophthalmology (3rd ed, 2017)
"""

import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# 主要臨床疾患 バッチ1 (Top Clinical Diseases)
# ============================================================

ENRICHMENTS["horse_0001"] = {
    "diagnosis_ja": (
        "【確定診断】Coggins試験（寒天ゲル免疫拡散法: AGID）が国際標準 — 血清中の抗EIAVp26抗体を検出。"
        "ELISA法（スクリーニング）→AGID確認の二段階検査。"
        "PCR（ウイルスRNA検出）は急性期・AGID陰性期に有用。"
        "血液検査: 貧血（PCV↓）、血小板減少、高ガンマグロブリン血症。"
        "肝機能: GGT↑、ビリルビン↑（慢性例）。"
        "鑑別: EHV-1、バベシア症、免疫介在性溶血性貧血、馬ウイルス性動脈炎。"
        "日本では家畜伝染病予防法に基づく検査が義務付けられる。"
    ),
    "treatment_ja": (
        "【特異的治療なし — レトロウイルス感染のため根治不能】"
        "急性期: 支持療法（輸液、NSAIDs: フルニキシンメグルミン1.1 mg/kg IV q12h）。"
        "重度貧血: 輸血（同種全血）。血小板減少: 安静・出血リスク管理。"
        "慢性キャリア: 臨床的に安定していれば対症療法のみ。"
        "ストレス・併発疾患・コルチコステロイドによるウイルス再活性化を回避。"
        "【法的義務】日本・米国とも届出義務疾病。陽性馬は隔離または殺処分が法的に求められる。"
        "同居馬の検査（Coggins）を実施。厩舎消毒（次亜塩素酸ナトリウム）。"
        "吸血昆虫（アブ・サシバエ）の管理が二次感染予防に重要。"
    ),
}

ENRICHMENTS["horse_0002"] = {
    "diagnosis_ja": (
        "【跛行検査】屈曲試験（distal limb flexion test）陽性、硬い地面での跛行増悪。"
        "診断的神経ブロック: 掌側指神経ブロック（palmar digital nerve block）で60-80%が改善。"
        "【画像診断】X線（65° dorsoproximal-palmarodistal oblique view）: "
        "舟状骨の硬化、嚢胞様病変、遠位縁の骨棘形成、屈腱面の侵食。"
        "MRI（standing low-field or high-field under GA）が最も感度高い — "
        "舟状骨髄浮腫、DDFT損傷、舟状骨靱帯病変、滑液嚢炎を評価。"
        "超音波（経蹄骨アプローチ）: DDFT評価に補助的。"
        "舟状骨滑液嚢造影（contrast bursography）: 滑液嚢-DDFT間の交通評価。"
        "鑑別: DDFT腱鞘炎、蹄関節炎、蹄骨骨折、側副靱帯損傷。"
    ),
}

ENRICHMENTS["horse_0003"] = {
    "diagnosis_ja": (
        "【系統的評価】心拍数（>60 bpm: 重度疼痛/循環障害）、CRT、粘膜色、腸蠕動音（4象限聴診）。"
        "直腸検査: 大結腸変位・嵌頓・捻転の触知、小腸拡張、砂の触知。"
        "経鼻胃管: 胃内逆流量（>2L: 小腸閉塞示唆）。"
        "腹部超音波: 小腸壁厚（>3mm異常）、腹水、大結腸壁浮腫、腸重積。"
        "腹腔穿刺: 腹水色・蛋白・白血球数（>10,000/μL: 腸壊死示唆、血性: 絞扼）。"
        "血液検査: PCV/TP（血液濃縮）、乳酸（>4 mmol/L: 手術適応の指標）、電解質。"
        "腹部X線（砂疝: 砂の蓄積像、foalの胎便停滞）。"
        "鑑別: 疝痛の原因は70+あり、系統的除外が必須。"
    ),
}

ENRICHMENTS["horse_0004"] = {
    "diagnosis_ja": (
        "【眼科検査】細隙灯顕微鏡: 角膜沈着物（keratic precipitates: KPs）、前房フレア、"
        "虹彩後癒着（posterior synechiae）、虹彩脱色素。"
        "眼底検査（散瞳後）: 硝子体混濁（vitreous opacities/floaters）、"
        "視神経乳頭周囲の脈絡膜瘢痕（butterfly lesion）、網膜変性。"
        "眼圧測定（トノメトリー）: 急性期は低眼圧、慢性期は続発性緑内障で高眼圧。"
        "超音波（B-mode）: 硝子体混濁、水晶体亜脱臼、網膜剥離の評価。"
        "Leptospira血清学（MAT）: L. interrogans serovar Pomona等の抗体価。"
        "前房穿刺（aqueous humor）: Leptospira PCR/MAT（確定診断に有用）。"
        "鑑別: 外傷性ぶどう膜炎、感染性角膜炎、緑内障、IMMK。"
    ),
    "treatment_ja": (
        "【急性期（炎症制御）】アトロピン1%点眼 q4-6h（散瞳・虹彩後癒着予防・毛様体弛緩）→反応後q12-24h。"
        "局所NSAIDs: ジクロフェナク0.1%点眼 q6-8h。"
        "局所ステロイド: プレドニゾロン酢酸エステル1%点眼 q4-6h（角膜潰瘍除外後）。"
        "全身NSAIDs: フルニキシンメグルミン1.1 mg/kg IV q12h × 5-7日 → 0.5 mg/kg PO q12h × 7-14日。"
        "重症: 結膜下トリアムシノロン4-8 mg注射。"
        "【再発予防】シクロスポリン徐放デバイス（suprachoroidal cyclosporine implant: SCDI）— "
        "臨床試験で再発率を50%以上低下（Gilger BC, Vet Ophthalmol 2010）。"
        "硝子体内ゲンタマイシン注射（4 mg、Leptospira陽性例）— 議論あり。"
        "【慢性管理】再発のモニタリング（飼い主教育: 流涙・瞼裂狭小・結膜充血の早期発見）。"
        "続発性白内障→水晶体摘出術。続発性緑内障→義眼術。"
        "最終的に失明する症例が多く（約50%）、早期かつ積極的な治療が視力温存の鍵。"
    ),
}

# ============================================================
# 主要臨床疾患 バッチ2 (Laminitis, Tendinitis, Thrush, Renal)
# ============================================================

ENRICHMENTS["horse_0008"] = {
    "diagnosis_ja": (
        "【臨床診断】Obel跛行グレード（I-IV）で重症度分類。特徴的な前肢負重姿勢（後方荷重）。"
        "蹄検査器: 蹄尖部の圧痛。指動脈拍動の亢進（bounding digital pulse）。"
        "X線（lateral view必須）: 蹄骨回転角度（rotation）、蹄骨沈下（sinking/distal displacement）、"
        "蹄骨-蹄壁間距離の増大、蹄骨先端のremodeling。"
        "Venogram（蹄造影）: 蹄葉血管の灌流評価（重症度・予後判定）。"
        "MRI: 蹄葉組織の詳細評価（standing MRI可能）。"
        "基礎疾患の検索: ACTH・インスリン（PPID/EMS）、敗血症スクリーニング。"
        "鑑別: 蹄膿瘍、蹄骨骨折、舟状骨病、DDFT損傷。"
    ),
    "treatment_ja": (
        "【急性期（最初の72時間が最重要）】冷却療法（cryotherapy）: 蹄を氷水に浸漬（0-5°C）× 48-72時間連続 — "
        "予防的にも高リスク馬（デンプン過食、対側肢跛行）に推奨（van Eps AW, JAVMA 2004）。"
        "鎮痛: フェニルブタゾン4.4 mg/kg PO/IV q12h（急性期）→2.2 mg/kg q12h（維持）。"
        "フルニキシンメグルミン1.1 mg/kg IV q12h（代替）。AcepromazineR 0.02-0.04 mg/kg IV（末梢血管拡張）。"
        "DMSO 1 g/kg IV（10%溶液、抗炎症・フリーラジカル除去）× 3日間。"
        "【蹄のサポート】ソフトフォーティング（深いおが屑・砂地）。スタイロフォームパッド（蹄叉荷重促進）。"
        "リリーパッド/ファログパッド。治療装蹄: ハートバーシュー（蹄叉荷重）。"
        "【慢性期】X線フォローアップ（蹄骨回転の進行評価）。"
        "矯正装蹄（therapeutic shoeing）: ブレイクオーバー短縮、蹄叉荷重。"
        "蹄壁切除術（dorsal wall resection）: 慢性回転症例。"
        "【基礎疾患の管理】PPID: ペルゴリド0.002 mg/kg PO q24h。"
        "EMS: 食事管理（NSC<10%）、運動療法、体重管理。"
        "敗血症: 原発疾患の治療。"
        "【予後】Obel I-II: 良好。蹄骨沈下・蹄骨先端穿通: 予後不良→安楽死検討。"
    ),
}

ENRICHMENTS["horse_0009"] = {
    "diagnosis_ja": (
        "【臨床検査】患肢の熱感・腫脹・圧痛（metacarpal region/metatarsal region）。"
        "屈曲試験陽性。歩様: 中等度跛行（急性期）。"
        "【超音波検査（Gold Standard）】SDFT/DDFTの横断・縦断像で "
        "腱線維の低エコー病変、腱断面積の増大、腱輪郭の不整を評価。"
        "損傷の分類: Type I（牽引損傷）、Type II（中心部壊死）、Type III（辺縁部損傷）。"
        "経時的超音波フォローアップ（月1回）で治癒過程を評価。"
        "MRI: 超音波で不明確な場合、足根部・蹄部の腱損傷評価に有用。"
        "鑑別: 繋靱帯炎、副管骨骨折、骨膜炎（shin soreness）。"
    ),
}

ENRICHMENTS["horse_0010"] = {
    "diagnosis_ja": (
        "【臨床診断】蹄叉（frog）の視診: 溝の深化、黒色の壊死組織・悪臭分泌物、"
        "蹄叉の軟化・崩壊。蹄叉中心溝（central sulcus）の深部感染。"
        "蹄検査器で蹄叉圧痛（重症例）。"
        "鑑別: 蹄癌（canker: 過剰肉芽組織）、蹄皮膚炎（mud fever）、白線膿瘍。"
        "基礎要因の評価: 蹄管理歴、飼養環境（湿潤・不衛生な条件）。"
    ),
    "treatment_ja": (
        "【局所治療】壊死組織のデブリードマン（蹄叉の腐敗・軟化部位を蹄ナイフで除去）。"
        "消毒: 2%ヨードチンキ or クロルヘキシジン0.05%で洗浄。"
        "局所抗菌薬: 10%ヨードホルム粉末充填、または過酸化銅ペースト。"
        "重症例: メトロニダゾール粉末の蹄叉溝内充填（嫌気性菌対策）。"
        "蹄叉中心溝の深部感染: 溝を切開して排膿、消毒液を充填しガーゼでパッキング。"
        "【環境改善（最重要）】乾燥した清潔な馬房維持。敷料の定期交換。"
        "蹄の日常的清掃（1日1回以上の裏掘り）。放牧地の排水改善。"
        "【装蹄管理】6-8週間隔の定期的削蹄・装蹄。蹄叉荷重の適正化。"
        "通常1-2週間の局所治療で改善する。慢性例は基礎要因の是正が不可欠。"
    ),
}

ENRICHMENTS["horse_0012"] = {
    "diagnosis_ja": (
        "【腎臓の炎症性疾患の診断】血液検査: BUN↑、クレアチニン↑（腎機能低下）、"
        "電解質異常（Ca↓、P↑、K↑）、代謝性アシドーシス。"
        "尿検査: 蛋白尿、円柱尿、等張尿（腎濃縮能低下）、血尿。"
        "GFR（糸球体濾過量）: クレアチニンクリアランスで定量評価。"
        "直腸検査: 左腎の触知（腎腫大・疼痛の評価）。"
        "超音波: 腎サイズ・腎実質エコー性（腎炎では高輝度化）・腎盂拡張の評価。"
        "腎生検: 確定診断（超音波ガイド下経皮生検、組織病理でGN/TINを分類）。"
        "鑑別: 腎前性高窒素血症（脱水）、腎後性（尿路閉塞）、腎毒性薬物。"
    ),
    "treatment_ja": (
        "【原因治療】感染性腎炎: 抗菌薬（TMS 15-30 mg/kg PO q12h、ペニシリンG 22,000 IU/kg IV q6h）。"
        "免疫介在性糸球体腎炎: コルチコステロイド（デキサメタゾン0.05-0.1 mg/kg IV q24h × 3-5日）— 馬での有効性は限定的。"
        "【支持療法】積極的輸液（等張液10-20 mL/kg/hr）で腎灌流維持。"
        "電解質補正（低Ca: カルシウムボログルコン酸、高K: ブドウ糖＋インスリン）。"
        "NSAIDs回避（腎血流低下リスク）。アミノグリコシド禁忌（腎毒性）。"
        "蛋白尿管理: ACE阻害薬（ベナゼプリル — 馬での使用は限定的）。"
        "慢性腎不全: 食事管理（低蛋白・低P）、水分アクセス確保。"
        "予後: 急性腎炎で早期介入→予後中程度。慢性腎不全→予後不良。"
    ),
}

ENRICHMENTS["horse_0013"] = {
    "diagnosis_ja": (
        "【腎腫瘍の診断】直腸検査: 左腎の腫大・不整形触知。"
        "超音波: 腎実質内の腫瘤像（不均一エコー、正常構造の消失）。"
        "CT/MRI: 腫瘍の範囲・浸潤・転移評価（大学病院レベル）。"
        "血液検査: BUN↑、Cr↑（両側腎障害時）、高Ca血症（腫瘍随伴症候群）、貧血。"
        "尿検査: 血尿（腎細胞癌で多い）、蛋白尿。"
        "腎生検: 腫瘍型の組織学的確定（腎細胞癌、リンパ腫、腎芽腫）。"
        "馬で最多: 腎細胞癌（renal cell carcinoma）。仔馬: 腎芽腫（nephroblastoma）。"
        "鑑別: 腎膿瘍、腎嚢胞、水腎症、腎周囲血腫。"
    ),
    "treatment_ja": (
        "【外科的治療】腎摘出術（nephrectomy）: 片側性腫瘍で対側腎機能正常時に考慮。"
        "standing laparoscopy or flank laparotomyでアプローチ。"
        "腎動脈・腎静脈の結紮が技術的に困難で出血リスク高い。"
        "【腎芽腫（仔馬）】外科的切除で治癒可能な場合あり。"
        "【リンパ腫】全身化学療法の選択肢は馬では限定的。コルチコステロイド単独で一時的寛解。"
        "【緩和療法】NSAIDs（フェニルブタゾン2.2 mg/kg PO q12h）で疼痛管理。"
        "高Ca血症: 輸液＋フロセミド1 mg/kg IV q12h。"
        "予後: 腎細胞癌は転移が多く予後不良。腎芽腫は摘出で予後中程度。"
    ),
}

ENRICHMENTS["horse_0014"] = {
    "diagnosis_ja": (
        "【代謝性腎疾患の診断】血液生化学: BUN↑、Cr↑、電解質異常（Ca/P/K）。"
        "尿検査: 等張尿、蛋白尿、糖尿（尿細管障害）。"
        "分別排泄率（FE）: Na、K、P、Caの腎排泄能評価。"
        "超音波: 腎サイズ、実質エコー性、腎石灰化（nephrocalcinosis）。"
        "直腸検査: 左腎の触知（腫大・萎縮・形態異常）。"
        "基礎疾患スクリーニング: PPID（ACTH）、EMS（インスリン）、中毒歴。"
        "鑑別: 急性腎障害（AKI）vs 慢性腎疾患（CKD）の区別が予後判定に重要。"
    ),
    "treatment_ja": (
        "【急性腎障害（AKI）】積極的輸液療法（等張液10-20 mL/kg/hr IV）が最優先。"
        "腎毒性物質の即時中止（NSAIDs、アミノグリコシド、ビタミンD過剰）。"
        "電解質補正。尿量モニタリング（0.5-2 mL/kg/hr目標）。"
        "乏尿期: フロセミド1-2 mg/kg IV → CRI 0.12 mg/kg/hr。"
        "マンニトール0.5-1 g/kg IV（15-20分かけて）— 反応なければ中止。"
        "【慢性腎疾患（CKD）】食事管理（低蛋白・低P — 馬では実践困難）。"
        "水分アクセス確保（塩ブロック提供で自発的飲水促進）。"
        "高P: 水酸化アルミニウム90 mg/kg PO q12h（リン結合剤）。"
        "貧血: エリスロポエチン（EPO）— 馬での使用は限定的、抗体産生リスク。"
        "予後: AKIは早期輸液で回復可能例あり。CKDは進行性で予後不良。"
    ),
}

ENRICHMENTS["horse_0005"] = {
    "diagnosis_ja": (
        "【系統的跛行検査】歩様検査（直線硬地・円運動・軟地）、屈曲試験（各関節個別）、"
        "蹄検査器（hoof tester）。AAEP跛行グレード（0-5）で重症度分類。"
        "診断的神経ブロック: 末梢→近位への系統的麻酔（掌側指→掌側中手→低四点→高四点）。"
        "関節内麻酔（蹄関節、球節、手根関節、飛節）。"
        "【画像診断】X線（標準4方向）: 骨折、関節炎、骨嚢胞、骨膜反応。"
        "超音波: 腱・靱帯損傷（SDFT/DDFT/SL）、関節液貯留。"
        "MRI（standing or under GA）: 骨髄浮腫、軟部組織病変の gold standard。"
        "核医学（骨シンチグラフィー）: 不顕性骨折、ストレス骨折の検出。"
        "CT: 蹄骨・舟状骨・手根骨の詳細評価。"
        "鑑別: 運動器以外の跛行（神経性、疼痛回避行動）も考慮。"
    ),
    "treatment_ja": (
        "【原因により治療が大きく異なる — 跛行は症候であり診断名ではない】"
        "関節炎: 関節内コルチコステロイド（トリアムシノロン6-12 mg or メチルプレドニゾロン40 mg）"
        "＋ヒアルロン酸（HA 20 mg）。全身NSAIDs: フェニルブタゾン2.2-4.4 mg/kg PO q12h。"
        "腱・靱帯損傷: 急性期の冷却・圧迫・安静、コントロールされた運動療法（6-12ヶ月）。"
        "PRP（多血小板血漿）・幹細胞療法の検討。体外衝撃波療法（ESWT）。"
        "骨折: タイプにより安静～外科的内固定。ストレス骨折は安静3-6ヶ月。"
        "蹄疾患: 装蹄療法（corrective shoeing）、蹄管理。"
        "感染性関節炎: 関節洗浄＋関節内＋全身抗菌薬。"
        "神経性跛行: 原因疾患の治療。"
    ),
}

ENRICHMENTS["horse_0006"] = {
    "diagnosis_ja": (
        "【臨床診断】特徴的三徴: 発熱→鼻汁（粘液膿性）→顎下リンパ節膿瘍。"
        "鼻腔スワブまたは膿瘍穿刺液の Streptococcus equi subsp. equi 培養（確定）。"
        "PCR（SeM遺伝子）: 培養より迅速（24h以内）。"
        "内視鏡: 咽頭・喉頭嚢（guttural pouch）の評価（慢性化・喉頭嚢蓄膿の確認）。"
        "喉頭嚢洗浄液の培養/PCR: キャリア検出に重要（喉頭嚢に長期残存）。"
        "血液検査: 白血球増多、フィブリノーゲン↑（>4 g/L）、SAA↑。"
        "SeM抗体価（ELISA）: ワクチン接種歴との鑑別が必要。"
        "腹部超音波: bastard strangles（転移性膿瘍）の評価。"
        "鑑別: 馬インフルエンザ、EHV-1/4、Rhodococcus equi（仔馬）、腺腫様歯牙嚢胞。"
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} horse disease entries")


if __name__ == "__main__":
    apply_enrichments()
