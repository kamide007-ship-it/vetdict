#!/usr/bin/env python3
"""Enrich Parakeet diagnosis_ja — batch 9 (final 22 entries)."""
import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 51. parakeet_hepatocellular_carcinoma — Hepatocellular Carcinoma / 肝細胞癌
ENRICHMENTS["parakeet_hepatocellular_carcinoma"] = {
    "diagnosis_ja": "腹部膨満・食欲低下・体重減少・黄色尿酸塩（ビリベルジン尿：肝障害示唆）の臨床評価。腹部超音波で肝実質の不均一な腫瘤を検出。CT/MRIで腫瘤の範囲・転移を評価。血液生化学（採血量≤体重の1%）で肝酵素著増（AST・LDH・GGT）・胆汁酸上昇・アルブミン低下を確認。FNA細胞診/肝生検で肝細胞癌を確定。CBC で貧血を評価。インコ類では肝細胞癌はセキセイインコ・オカメインコの高齢鳥で報告があり、進行期には体腔液貯留を伴う"
}

# 52. parakeet_bile_duct_carcinoma — Bile Duct Carcinoma / 胆管癌
ENRICHMENTS["parakeet_bile_duct_carcinoma"] = {
    "diagnosis_ja": "食欲低下・体重減少・腹部膨満・黄色尿酸塩の臨床評価。腹部超音波で肝内の結節性腫瘤を検出。血液生化学（採血量≤体重の1%）で肝酵素著増（AST・GGT・LDH）・胆汁酸上昇を確認。CT検査で腫瘤の範囲・転移を評価。FNA細胞診で腺管構造を形成する腫瘍細胞を確認。病理組織検査で胆管癌を確定。CBC で全身状態を評価。インコ類では内部乳頭腫症（PsHV関連）からの胆管癌への悪性転化が報告されており、乳頭腫症の既往がある場合はリスクが高い"
}

# 53. parakeet_proventricular_ulceration_budgerigar — Proventricular Ulceration (Budgerigar)
ENRICHMENTS["parakeet_proventricular_ulceration_budgerigar"] = {
    "diagnosis_ja": "嘔吐・食欲低下・体重減少・メレナ（暗色便）の臨床評価。内視鏡で前胃粘膜の潰瘍・びらん・出血を直視確認し生検。糞便のグラム染色でMacrorhabdus ornithogasterを検索（AGY合併の評価）。糞便潜血検査。CBC（採血量≤体重の1%）で貧血を評価。血液生化学でTP・アルブミン低下を測定。腹部X線で前胃拡張を確認。セキセイインコの前胃潰瘍はAGY感染・ストレス・NSAIDs・重金属中毒が原因であり、穿孔→腹膜炎が致死的となりうる。AGY治療と並行して胃粘膜保護を行う"
}

# 54. parakeet_air_sac_mite_–_chronic_infestation — Air Sac Mite – Chronic Infestation
ENRICHMENTS["parakeet_air_sac_mite_–_chronic_infestation"] = {
    "diagnosis_ja": "慢性の呼吸困難・開口呼吸・テイルボビング・声の変化・運動不耐性の臨床評価。透照法（transillumination）で気管内のSternostoma tracheacolum（気管ダニ）を検出。気管内視鏡で気管・気嚢内のダニ虫体を直視確認。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。胸部X線で気嚢混濁を検出。インコ類（特にセキセイインコ・カナリア・フィンチ）では気嚢ダニの慢性寄生が呼吸困難・声の消失を引き起こす。イベルメクチン投与を2週間隔で3-4回反復し、環境消毒を併用する"
}

# 55. parakeet_sour_crop — Sour Crop / 酸敗嗉嚢
ENRICHMENTS["parakeet_sour_crop"] = {
    "diagnosis_ja": "嗉嚢の触診で膨満・液体波動を確認。嗉嚢液の逆流・酸臭を確認。嗉嚢洗浄液の鏡検で酵母（Candida）・細菌過増殖を検索。嗉嚢液のpH測定（正常pH 5-6、酸敗ではpH<4）。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。腹部X線で嗉嚢拡張・消化管通過遅延を確認。インコ類の酸敗嗉嚢は嗉嚢運動障害・カンジダ過増殖・不適切な手差し給餌（温度不足・過濃度）が原因で、幼鳥の手差し飼育で多発する。嗉嚢洗浄とカンジダ治療が基本"
}

# 56. parakeet_thyroid_carcinoma — Thyroid Carcinoma / 甲状腺癌
ENRICHMENTS["parakeet_thyroid_carcinoma"] = {
    "diagnosis_ja": "頸部腫脹・嚥下困難・呼吸困難（気管圧迫）の臨床評価。頸部触診で甲状腺領域の硬い腫瘤を確認。頸部X線・CTで腫瘤のサイズ・気管偏位・浸潤を判定。FNA細胞診で甲状腺腫瘍細胞の形態を評価。組織生検・病理組織検査で甲状腺癌を確定。血液生化学（採血量≤体重の1%）でT4値を測定。CBC で全身状態を評価。インコ類ではヨード欠乏性甲状腺腫（良性過形成）との鑑別が最も重要であり、ヨード補充で退縮しない場合は甲状腺癌を強く疑う。外科的切除は困難なことが多い"
}

# 57. parakeet_choanal_papilloma — Choanal Papilloma / 後鼻孔乳頭腫
ENRICHMENTS["parakeet_choanal_papilloma"] = {
    "diagnosis_ja": "後鼻孔（choana）検査で乳頭状腫瘤を確認。片側性鼻閉・鼻汁の臨床評価。生検・病理組織検査で乳頭腫の組織パターンを確認。PCR検査でヘルペスウイルスDNAを検索。CBC（採血量≤体重の1%）で全身状態を評価。頭部X線・CTで腫瘤の範囲を評価。内視鏡で口腔内・食道への進展を検索。インコ類では後鼻孔乳頭腫はアマゾンで好発するが、セキセイインコでも報告がある。内部乳頭腫症との関連を考慮し、消化管の精査も推奨される"
}

# 58. parakeet_intestinal_lymphoma — Intestinal Lymphoma / 腸リンパ腫
ENRICHMENTS["parakeet_intestinal_lymphoma"] = {
    "diagnosis_ja": "慢性下痢・体重減少・食欲低下・腹部膨満の臨床評価。腹部超音波で腸管壁の瀰漫性肥厚・腸管腫瘤を検出。CBC（採血量≤体重の1%）で異型リンパ球・白血球変動を確認。血液生化学でTP低下・AST・LDH変動を測定。腸管生検の病理組織検査でリンパ腫の組織型（B細胞/T細胞）を確定。免疫組織化学でCD3/CD79a等の発現を評価。インコ類ではリンパ腫は比較的多い腫瘍であり、消化管型は慢性消耗性疾患として呈する。REV等のレトロウイルスとの関連も疑われている"
}

# 59. parakeet_egg_yolk_peritonitis_–_chronic — Egg Yolk Peritonitis – Chronic / 卵黄性腹膜炎慢性型
ENRICHMENTS["parakeet_egg_yolk_peritonitis_–_chronic"] = {
    "diagnosis_ja": "慢性的な腹部膨満・体重変動・間欠的沈鬱の臨床評価。腹部超音波で体腔液貯留・線維素性被包・卵黄塊を検出。体腔穿刺液の細胞診で卵黄物質・マクロファージ・ヘテロフィルを確認。細菌培養で二次感染菌を同定。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。血液生化学でTP上昇・Ca変動・AST上昇を測定。X線で腹腔内軟部組織陰影・石灰化卵殻を検出。インコ類の慢性卵黄性腹膜炎は慢性産卵鳥で好発し、卵巣からの卵黄が体腔内に遊離して慢性炎症を惹起する"
}

# 60. parakeet_oviductal_impaction — Oviductal Impaction / 卵管閉塞
ENRICHMENTS["parakeet_oviductal_impaction"] = {
    "diagnosis_ja": "産卵困難・腹部膨満・テネスムス（いきみ）・沈鬱の臨床評価。腹部触診で卵管内の硬い腫瘤を触知。X線で卵管内の石灰化卵殻・異常卵を検出。腹部超音波で卵管腫大・卵管内容物の性状を評価。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。血液生化学でCa低下・TP変動を測定。インコ類の卵管閉塞は異常卵（軟殻卵・癒着卵）の停滞・卵管炎後の瘢痕狭窄・卵管筋力低下（低Ca血症）が原因で発生し、保存的治療で排出されない場合は外科的卵管切開/卵管摘出が必要"
}

# 61. parakeet_cloacal_papilloma — Cloacal Papilloma / 総排泄腔乳頭腫
ENRICHMENTS["parakeet_cloacal_papilloma"] = {
    "diagnosis_ja": "排便困難・血便・総排泄腔の腫瘤を身体検査で確認。総排泄腔検査で乳頭状〜カリフラワー状腫瘤を直視。生検・病理組織検査で乳頭腫を確定。PCR検査でヘルペスウイルスDNAを検索。CBC（採血量≤体重の1%）で全身状態を評価。内視鏡で消化管内への進展を検索。インコ類の総排泄腔乳頭腫はPsittacid herpesvirus関連の内部乳頭腫症の一部として発現することが多く、胆管癌・膵管癌への悪性転化リスクがある。外科的切除後の再発率が高い"
}

# 62. parakeet_psittacine_proventricular_nematodes — Psittacine Proventricular Nematodes
ENRICHMENTS["parakeet_psittacine_proventricular_nematodes"] = {
    "diagnosis_ja": "慢性嘔吐・体重減少・未消化便・食欲低下の臨床評価。糞便検査（浮遊法・沈殿法）でDispharynx・Ascaridia等の線虫卵を検出。嗉嚢/前胃洗浄液の鏡検で幼虫・虫卵を検索。内視鏡で前胃粘膜の虫体を直視確認。CBC（採血量≤体重の1%）で好酸球増加を確認。血液生化学でTP低下を測定。腹部X線で前胃拡張を評価。インコ類ではDispharynx nasutaが嗉嚢・前胃に寄生し、中間宿主（等脚類）を介して感染する。フェンベンダゾール/イベルメクチンによる駆虫が第一選択"
}

# 63. parakeet_budgerigar_amyloidosis — Budgerigar Amyloidosis / セキセイインコアミロイドーシス
ENRICHMENTS["parakeet_budgerigar_amyloidosis"] = {
    "diagnosis_ja": "慢性消耗・肝腫大・体重減少の臨床評価。血液生化学（採血量≤体重の1%）で肝酵素上昇（AST・LDH）・アルブミン低下・胆汁酸上昇を確認。腹部超音波で肝腫大を検出。肝FNA/生検のコンゴーレッド染色で偏光顕微鏡下にapple-green複屈折のアミロイド沈着を確認。CBC で慢性変化を評価。セキセイインコのアミロイドーシスはAA型アミロイドーシスであり、慢性炎症性疾患に続発する。進行性・不可逆的で予後不良であるが、原発性炎症の制御が進行抑制に寄与する可能性がある"
}

# 64. parakeet_ventral_hernia — Ventral Hernia / 腹壁ヘルニア
ENRICHMENTS["parakeet_ventral_hernia"] = {
    "diagnosis_ja": "腹部の軟性膨隆（腹壁欠損を通じた腸管・卵管等の脱出）を身体検査で確認。ヘルニア内容物の還納性を評価。腹部X線で腹壁欠損を通じた腸管ガスの体壁外脱出を検出。超音波でヘルニア門のサイズ・内容物を評価。CBC（採血量≤体重の1%）で全身状態を確認。血液生化学でTP・UA変動を測定。インコ類の腹壁ヘルニアは慢性産卵・肥満・腹圧上昇が素因であり、腸管絞扼のリスクがある。外科的腹壁修復が根治的治療で、ホルモン療法による産卵抑制も並行する"
}

# 65. parakeet_uropygial_gland_abscess — Uropygial Gland Abscess / 尾脂腺膿瘍
ENRICHMENTS["parakeet_uropygial_gland_abscess"] = {
    "diagnosis_ja": "尾部背側の尾脂腺の腫脹・発赤・疼痛・排膿を身体検査で確認。FNA/切開排膿液の細胞診・培養で起炎菌を同定し感受性試験を実施。グラム染色で菌種を推定。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。X線で尾椎への波及を除外。インコ類の尾脂腺膿瘍は導管閉塞→分泌物貯留→二次感染が病態であり、外科的切開排膿が治療の基本。腺腫瘍との鑑別に病理組織検査が重要。セキセイインコでは尾脂腺は小さいが存在し、膿瘍形成は稀ではない"
}

# 66. parakeet_lead_toxicosis — Lead Toxicosis / 鉛中毒
ENRICHMENTS["parakeet_lead_toxicosis"] = {
    "diagnosis_ja": "急性嘔吐・下痢・神経症状（痙攣・運動失調・失明）・多飲多尿の臨床評価。全血鉛濃度測定（正常<20μg/dL、中毒>40μg/dL）。腹部X線で消化管内の金属片を検出（鉛は高密度異物として描出）。CBC（採血量≤体重の1%）で貧血（PCV低下）・赤血球の好塩基性斑点を確認。血液生化学でUA上昇（腎障害）・AST上昇を測定。インコ類では鉛含有塗料・はんだ・カーテンウェイト・ステンドグラスの咬傷が主要曝露源。CaEDTAキレーション療法と消化管内金属異物の除去が治療の基本"
}

# 67. parakeet_vitamin_a_deficiency_–_respiratory — Vitamin A Deficiency – Respiratory
ENRICHMENTS["parakeet_vitamin_a_deficiency_–_respiratory"] = {
    "diagnosis_ja": "くしゃみ・鼻汁・呼吸困難の臨床評価。後鼻孔（choana）検査で乳頭の鈍化・消失（正常鋭利な乳頭→扁平上皮化生で鈍化）を確認。口腔内の白色結節（唾液腺の扁平上皮化生による管開口部閉塞→膿瘍形成）を検索。食餌歴の聴取（種子食偏重→VitA不足）。血液生化学（採血量≤体重の1%）でVitA値を測定。CBC でヘテロフィル変動を確認。X線で気嚢混濁（二次感染）を評価。インコ類のVitA欠乏呼吸器型は粘膜のバリア機能低下→二次感染（アスペルギルス・細菌）の素因となる"
}

# 68. parakeet_mite_infestation_–_feather_mites — Mite Infestation – Feather Mites / 羽ダニ寄生症
ENRICHMENTS["parakeet_mite_infestation_–_feather_mites"] = {
    "diagnosis_ja": "羽毛損傷（羽軸の小孔・羽枝の断裂・羽毛表面の擦過痕）・掻痒行動を身体検査で確認。羽毛の直接鏡検で羽ダニ（Dermoglyphus・Proctophyllodes等）の虫体・卵を検出。粘着テープ法で体表のダニを採集。虫体の形態学的同定。CBC（採血量≤体重の1%）で好酸球増加を確認。インコ類の羽ダニは多くの場合共生的（軽度の羽毛損傷のみ）であるが、免疫低下個体では大量寄生が羽毛の著明な劣化を引き起こす。イベルメクチン局所投与と環境消毒で管理する"
}

# 69. parakeet_endocarditis — Endocarditis / 心内膜炎
ENRICHMENTS["parakeet_endocarditis"] = {
    "diagnosis_ja": "運動不耐性・呼吸困難・突然死の臨床評価。聴診で心雑音を評価（鳥類の高心拍数のため聴診困難なことあり）。心エコー検査で弁膜上の疣贅性病変（vegetation）を検出。血液培養で起炎菌（Staphylococcus・Streptococcus・E. coli等）を分離。CBC（採血量≤体重の1%）でヘテロフィル著増・毒性顆粒を確認。血液生化学でAST・LDH・cTnI上昇を測定。インコ類の心内膜炎は菌血症に続発する感染性心内膜炎が主であり、弁膜破壊→心不全・全身性血栓塞栓症が致死的となる"
}

# 70. parakeet_hypothyroidism — Hypothyroidism / 甲状腺機能低下症
ENRICHMENTS["parakeet_hypothyroidism"] = {
    "diagnosis_ja": "肥満・羽毛異常（換羽遅延・光沢消失）・沈鬱・運動不耐性・脂質異常の臨床評価。血液生化学（採血量≤体重の1%）でT4低下（鳥類の正常T4値は種により異なる）・コレステロール上昇・トリグリセリド上昇を確認。TSH刺激試験でT4反応低下を確認（利用可能な場合）。CBC で全身状態を評価。X線で甲状腺腫大の有無を確認。食餌歴の聴取（ヨード欠乏はgoiterの原因）。インコ類（特にセキセイインコ）ではヨード欠乏性甲状腺機能低下が最も多く、レボチロキシン補充療法とヨード補充が治療の基本"
}

# 71. parakeet_cloacal_calculus — Cloacal Calculus / 総排泄腔結石
ENRICHMENTS["parakeet_cloacal_calculus"] = {
    "diagnosis_ja": "排便困難（テネスムス）・腹部膨満・総排泄腔周囲の腫脹の臨床評価。総排泄腔の視診・触診で硬い結石を触知。X線で総排泄腔内の高密度結石影を確認。血液生化学（採血量≤体重の1%）でUA著増（高尿酸血症→尿酸塩結石）を確認。腎機能評価。CBC でヘテロフィル変動を評価。インコ類の総排泄腔結石は高尿酸血症（脱水・腎疾患・高蛋白食）に伴う尿酸塩析出が原因で形成される。結石の物理的除去と原因治療（腎疾患管理・食餌改善・適切な水分摂取）が必要"
}

# 72. parakeet_egg_peritonitis_–_acute_septic — Egg Peritonitis – Acute Septic
ENRICHMENTS["parakeet_egg_peritonitis_–_acute_septic"] = {
    "diagnosis_ja": "急性沈鬱・膨羽・腹部膨満・呼吸困難・食欲廃絶の臨床評価。腹部超音波で体腔液貯留・卵管腫大を検出。体腔穿刺液の細胞診でヘテロフィル著増・細菌・卵黄物質を確認。細菌培養でE. coli等の起炎菌を分離し感受性試験を実施。CBC（採血量≤体重の1%）でヘテロフィル著増・H/L比上昇・毒性顆粒を確認。血液生化学でTP上昇・グルコース低下・AST著増を測定。インコ類の急性敗血症型卵黄性腹膜炎は卵管破裂→卵黄の腹腔内遊離→E. coli上行感染による敗血症で致死率が高い。緊急的な抗菌薬投与と支持療法が救命に不可欠"
}


def apply_enrichments() -> None:
    for attempt in range(3):
        try:
            with open(JSON_PATH, encoding="utf-8") as f:
                content = f.read()
            decoder = json.JSONDecoder()
            data, _ = decoder.raw_decode(content)
            break
        except (json.JSONDecodeError, ValueError):
            if attempt < 2:
                time.sleep(5)
            else:
                raise

    updated = 0
    for entry in data:
        eid = entry.get("id")
        if eid in ENRICHMENTS:
            for k, v in ENRICHMENTS[eid].items():
                entry[k] = v
            updated += 1

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {updated}/{len(ENRICHMENTS)} entries")


if __name__ == "__main__":
    apply_enrichments()
