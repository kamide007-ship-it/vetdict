#!/usr/bin/env python3
"""Cat treatment_ja expansion."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["cat_0015"] = {
    "treatment_ja": (
        "タウリン欠乏性拡張型心筋症：タウリン補充（250-500 mg/cat PO q12h）が根本治療で、"
        "心筋機能は3-6ヶ月で可逆的に回復する。心不全併発時はフロセミド（1-2 mg/kg PO q12h）、"
        "ピモベンダン（0.625-1.25 mg/cat PO q12h、SAM非存在下）、ACE阻害薬（ベナゼプリル0.5 mg/kg PO q24h）で管理。"
        "血漿タウリン濃度（正常>60 nmol/mL）で治療効果をモニタリング。現在は市販猫フードにタウリン添加が義務付けられており発生は稀だが、"
        "自家調理食・ベジタリアン食の猫では依然としてリスクがある。心エコーで左室内径短縮率（FS）の回復を確認する。"
    )
}

ENRICHMENTS["cat_restrictive_cardiomyopathy"] = {
    "treatment_ja": (
        "拘束型心筋症は心内膜/心筋の線維化により拡張障害を呈し、根治不可。"
        "心不全管理：フロセミド（1-2 mg/kg PO q12h、急性期2-4 mg/kg IV）で肺水腫/胸水をコントロール。"
        "ピモベンダン（0.625-1.25 mg/cat PO q12h）はSAM非存在下で使用。"
        "ACE阻害薬（ベナゼプリル0.5 mg/kg PO q24h）。血栓塞栓症予防にクロピドグレル（18.75 mg/cat PO q24h）が必須。"
        "不整脈にはソタロール（2 mg/kg PO q12h）またはアテノロール。"
        "胸水貯留時は胸腔穿刺。心エコーで定期的に拡張機能を評価。ストレス最小化が重要で、予後はHCMより不良（MST 3-12ヶ月）。"
    )
}

ENRICHMENTS["cat_esophagitis"] = {
    "treatment_ja": (
        "酸分泌抑制：オメプラゾール（1 mg/kg PO q24h）またはファモチジン（0.5 mg/kg PO q12-24h）。"
        "粘膜保護：スクラルファート（0.25-0.5 g PO q8h、他剤と2時間ずらす）。"
        "制吐薬：マロピタント（1 mg/kg SC/PO q24h）で嘔吐による二次損傷を防止。"
        "食事管理：少量頻回の軟食を高い位置で給餌し、逆流を軽減。"
        "原因別対応：全身麻酔後の逆流性食道炎、異物除去後、腐食性物質摂取後で治療期間が異なる。"
        "食道狭窄予防にプレドニゾロン（1 mg/kg PO q24h×2-3週→漸減）。狭窄形成時はバルーン拡張術を実施し、複数回の拡張が必要な場合がある。"
    )
}

ENRICHMENTS["cat_feline_hyperesthesia_syndrome"] = {
    "treatment_ja": (
        "ガバペンチン（5-10 mg/kg PO q8-12h）が第一選択で神経性疼痛/過敏を抑制。"
        "行動性要素にはフルオキセチン（0.5-1 mg/kg PO q24h）またはクロミプラミン（0.25-0.5 mg/kg PO q24h）。"
        "発作性要素が疑われる場合はフェノバルビタール（2-3 mg/kg PO q12h）またはレベチラセタム（20 mg/kg PO q8h）。"
        "環境エンリッチメント：フェリウェイ拡散器、垂直空間の確保、定期的な遊び時間でストレス軽減。"
        "皮膚疾患（アレルギー性皮膚炎、ノミアレルギー、皮膚糸状菌症）の鑑別除外が必須。"
        "原因不明（行動性/神経性の複合）であり、多モーダル治療が奏功することが多い。"
    )
}

ENRICHMENTS["cat_feline_chronic_gingivostomatitis"] = {
    "treatment_ja": (
        "全臼歯抜歯（部分顎抜歯）が最も有効な治療（60-80%が改善/治癒）。犬歯は温存可能な場合もあるが、"
        "難治例では全顎抜歯を検討。歯科X線で残根がないことを確認することが治癒の鍵。"
        "抜歯不十分時の免疫調節：シクロスポリン（5-7 mg/kg PO q24h、トキソプラズマIgG陰性確認後）。"
        "プレドニゾロン（1-2 mg/kg PO q24h→漸減）は短期使用に留める。"
        "疼痛管理：ブプレノルフィン頬粘膜投与（0.02 mg/kg q8-12h）、ガバペンチン（5-10 mg/kg PO q8-12h）。"
        "猫IFN-ω局所注射。FeLV/FIV検査を実施し、陽性例は予後不良。レーザー治療が補助的に使用されることもある。"
    )
}

ENRICHMENTS["cat_nocardiosis"] = {
    "treatment_ja": (
        "Nocardia spp.感染症。長期抗菌薬療法が必須で、TMP/SMX（トリメトプリム/スルファメトキサゾール15 mg/kg PO q12h）が第一選択。"
        "最低6-12ヶ月の継続投与が必要で、早期中断は再発の原因となる。"
        "TMP/SMX不耐時はアミカシン（10 mg/kg IV/SC q24h）＋イミペネム（5 mg/kg IV q8h）の併用を検討。"
        "膿胸・皮下膿瘍には外科的ドレナージとデブリドマンが不可欠。"
        "FeLV/FIV検査を含む免疫状態の精査を行い、免疫抑制薬使用中であれば減量/中止を検討する。"
        "培養・感受性試験に基づく抗菌薬選択が重要。予後は免疫状態と病変の範囲に依存する。"
    )
}

ENRICHMENTS["cat_heartworm-associated_respiratory_disease_hard"] = {
    "treatment_ja": (
        "猫にはメラルソミン（犬用成虫駆除薬）使用不可 — 致死的な肺血栓塞栓症を引き起こす。"
        "支持療法が中心：プレドニゾロン（1-2 mg/kg PO q24h×2週→漸減→0.5 mg/kg q48h維持）で肺炎症を抑制。"
        "急性呼吸窮迫時は酸素療法＋テルブタリン（0.01 mg/kg SC/IM）で気管支拡張。"
        "成虫の自然消退を待つ（猫体内の成虫寿命は2-3年）。この間、定期的な胸部X線と抗体/抗原検査でモニタリング。"
        "予防が最重要：イベルメクチン/セラメクチン/モキシデクチンの月1回投与を生涯継続。"
        "HARDは成虫不在（L5幼虫のみ）でも好酸球性肺炎を起こす。抗原検査偽陰性に注意。"
    )
}

ENRICHMENTS["cat_dysautonomia_key-gaskell_syndrome"] = {
    "treatment_ja": (
        "特異的治療法は存在せず、自律神経系の広範な変性に対する支持療法が中心。"
        "消化管運動低下：メトクロプラミド（0.2-0.5 mg/kg PO/SC q8h）またはシサプリド（0.5 mg/kg PO q8-12h）。"
        "角膜乾燥（KCS）：人工涙液を頻回点眼し、シクロスポリン点眼薬（0.2%）で涙液分泌を促進。"
        "散瞳にはフェニレフリン0.1%点眼。膀胱アトニーには用手的圧迫排尿を1日3-4回実施し、尿路感染を予防。"
        "経管栄養（経鼻食道チューブ/食道瘻チューブ）による栄養管理。輸液で脱水補正。"
        "予後不良で死亡率70%以上。一部の症例は数ヶ月かけて部分的に自律神経機能が回復する。原因は不明だがClostridium botulinum毒素の関与が疑われている。"
    )
}

ENRICHMENTS["cat_dermatophilosis"] = {
    "treatment_ja": (
        "Dermatophilus congolensis（放線菌の一種）による皮膚感染症。"
        "痂皮除去が治療の鍵 — 痂皮下に菌体が存在するため、クロルヘキシジン2%またはポビドンヨードシャンプーで物理的に除去。"
        "全身性抗菌薬：アモキシシリン/クラブラン酸（12.5-25 mg/kg PO q12h×3-4週）が第一選択。"
        "代替薬：ペニシリンG（22,000 IU/kg IM q24h×5-7日）、エリスロマイシン（10-15 mg/kg PO q8h）。"
        "免疫状態の評価が重要で、FeLV/FIV検査、ステロイド使用歴、基礎疾患を確認。"
        "環境管理：多湿環境の改善、外傷予防。再発防止には免疫力の維持と皮膚バリアの保護が必要。"
    )
}

ENRICHMENTS["cat_hypertensive_retinopathy"] = {
    "treatment_ja": (
        "高血圧の迅速な降圧が最優先。アムロジピン（0.625 mg/cat PO q24h→必要に応じて1.25 mg/catに増量）が猫の第一選択降圧薬。"
        "目標SBP<160 mmHg。SBP>180 mmHgは標的臓器障害（TOD）リスクが極めて高い。"
        "網膜出血・剥離が発生した場合、降圧開始から24-48時間以内の治療で視力回復の可能性あり — 急性失明は緊急対応。"
        "基礎疾患の治療が不可欠：CKD（IRIS分類に基づく管理）、甲状腺機能亢進症（メチマゾール）。"
        "定期モニタリング：ドプラー血圧測定q2-4週（安定後q3-6ヶ月）、眼底検査で網膜/脈絡膜病変を評価。"
        "テルミサルタン（1 mg/kg PO q24h）の追加も検討。蛋白尿併発時はACE阻害薬を併用。"
    )
}

ENRICHMENTS["cat_feline_mitral_valve_disease"] = {
    "treatment_ja": (
        "猫の僧帽弁疾患は犬と異なり粘液腫様変性よりも弁膜線維症や先天性異形成が多い。"
        "無症候期はモニタリング中心：心エコーで僧帽弁逆流の重症度、左房拡大（LA/Ao比）、E/A比を定期評価。"
        "心不全顕性化時：フロセミド（1-2 mg/kg PO q12-24h、急性肺水腫は2-4 mg/kg IV）。"
        "ピモベンダン（0.625-1.25 mg/cat PO q12h）はSAM非存在下で使用し、LVEDP低下と収縮力増強を図る。"
        "ACE阻害薬（ベナゼプリル0.5 mg/kg PO q24h）で後負荷軽減。"
        "血栓塞栓症予防：クロピドグレル（18.75 mg/cat PO q24h）は左房拡大（>16 mm）で開始。"
        "心房細動/上室性頻拍にはアテノロール（6.25 mg/cat PO q12h）またはジルチアゼム。猫はストレスで急変するため最小限のハンドリングで管理。"
    )
}

ENRICHMENTS["cat_feline_cutaneous_lymphoma"] = {
    "treatment_ja": (
        "上皮向性T細胞リンパ腫（菌状息肉症/セザリー症候群様）が猫で最多の皮膚リンパ腫形態。"
        "皮膚生検＋免疫組織化学（CD3/CD79a）で確定診断し、T細胞性/B細胞性を鑑別。"
        "単剤療法：ロムスチン（CCNU 50-60 mg/m² PO q3週、CBC2-3週間隔でモニタリング — 累積肝毒性に注意）。"
        "レチノイド（イソトレチノイン2 mg/kg PO q24h）は孤立性/初期病変に有効な場合あり。"
        "多剤化学療法：COP（シクロホスファミド＋ビンクリスチン＋プレドニゾロン）またはCHOP。"
        "局所病変には放射線療法。疼痛管理にガバペンチン/ブプレノルフィン。予後不良でMST 3-6ヶ月。全身播種型はさらに短い。"
    )
}

ENRICHMENTS["cat_feline_chronic_colitis"] = {
    "treatment_ja": (
        "食事療法が第一：新奇蛋白食（鹿肉、カンガルー等）または加水分解蛋白食を8-12週間厳格に試行。"
        "メトロニダゾール（10-15 mg/kg PO q12h×2-4週）は抗菌＋免疫調節作用で初期治療に有用。"
        "内視鏡＋全層生検でIBD確定後、プレドニゾロン（1-2 mg/kg PO q24h×2-4週→漸減4-8週）。"
        "ステロイド副作用軽減にブデソニド（0.5-1 mg/cat PO q24h）が代替。"
        "難治性にはクロラムブシル（0.1-0.2 mg/kg PO q48-72h）追加。"
        "コバラミン（250 μg/cat SC q週×6週→q2週）は回腸病変で必須。プロバイオティクス補助。"
        "膵炎（fPLI）・胆管炎との合併（triaditis）を常に考慮。定期的な体重・アルブミン・便性状のモニタリング。"
    )
}

ENRICHMENTS["cat_feline_allergic_bronchopulmonary_disease"] = {
    "treatment_ja": (
        "猫喘息と類似の病態で好酸球性気道炎症が特徴。吸入ステロイド（フルチカゾン110 μg MDI＋AeroKatスペーサー q12h）が長期管理の推奨。"
        "急性増悪：プレドニゾロン（1-2 mg/kg PO q24h×1-2週→漸減）。"
        "気管支拡張薬：アルブテロール吸入（1-2パフ、レスキュー使用のみ）。テルブタリン（0.01 mg/kg SC/IM 急性時）。"
        "テオフィリン徐放剤（10 mg/kg PO q24h evening）の追加も考慮。"
        "環境管理が不可欠：低粉塵猫砂への変更、空気清浄機設置、芳香剤/煙草煙の除去。"
        "BAL（気管支肺胞洗浄）で好酸球増多を確認し確定。胸部X線で気管支パターン（ドーナツ/トラムライン像）を評価。シクロスポリンが難治例に。"
    )
}

ENRICHMENTS["cat_feline_bile_duct_obstruction"] = {
    "treatment_ja": (
        "完全閉塞は外科的介入が必須。胆嚢十二指腸吻合術（cholecystoduodenostomy）が標準術式で、"
        "総胆管探索＋T-tubeドレナージまたはステント留置も選択肢。"
        "術前安定化：輸液療法（脱水/電解質補正）、ビタミンK1（0.5-1.5 mg/kg SC/IM q12h×3回 — 凝固能回復に24-48時間）、"
        "広域抗菌薬（アンピシリン/スルバクタム30 mg/kg IV q8h＋メトロニダゾール10 mg/kg IV q12h）で胆管炎合併に対応。"
        "内科管理：UDCA（10-15 mg/kg PO q24h）で胆汁うっ滞改善、SAMe（90 mg/cat PO q24h空腹時）で肝保護。"
        "原因精査：胆管炎、膵炎、triaditis（胆管炎＋膵炎＋IBD）、胆石、胆管癌。エコー＋肝酵素（ALP/GGT/T-Bil）で評価。"
    )
}

ENRICHMENTS["cat_feline_alopecia_areata"] = {
    "treatment_ja": (
        "自己免疫性の非瘢痕性脱毛で、毛包周囲のリンパ球浸潤が特徴。自然寛解する場合があり（数ヶ月〜1年）、"
        "美容的問題のみなら無治療の経過観察も妥当な選択肢。"
        "局所療法：タクロリムス0.1%軟膏を脱毛部に1日2回塗布（免疫調節）。"
        "全身療法（重症/広範囲例）：プレドニゾロン（1-2 mg/kg PO q24h×4週→漸減、長期使用は糖尿病リスク）。"
        "シクロスポリン（5-7 mg/kg PO q24h×8-12週）はステロイド代替。"
        "ミノキシジル2%局所は猫に心毒性リスク（メトヘモグロビン血症、ハインツ小体貧血）があり原則使用不可。"
        "皮膚生検で確定診断し、皮膚糸状菌症・心因性脱毛・好酸球性肉芽腫群を鑑別除外する。"
    )
}

ENRICHMENTS["cat_feline_tricuspid_valve_dysplasia"] = {
    "treatment_ja": (
        "先天性三尖弁異形成で、弁尖の奇形・腱索短縮・乳頭筋異常により三尖弁逆流（TR）を生じる。"
        "右心不全管理が治療の主軸：フロセミド（1-2 mg/kg PO q12-24h）で腹水・胸水・末梢浮腫を軽減。"
        "重度腹水には腹腔穿刺による排液。スピロノラクトン（1-2 mg/kg PO q12h）をフロセミドに追加して利尿効果を増強。"
        "ACE阻害薬（ベナゼプリル0.5 mg/kg PO q24h）で後負荷軽減。ピモベンダン（0.625-1.25 mg/cat PO q12h）は右室機能不全に。"
        "心房細動/上室性頻拍にはジルチアゼム（1.5-2.5 mg/kg PO q8h）。"
        "低ナトリウム食。定期心エコーで右房/右室サイズと TR重症度をモニタリング。外科的弁形成術は猫では現実的でない。"
    )
}

ENRICHMENTS["cat_feline_myocardial_contusion"] = {
    "treatment_ja": (
        "外傷性心筋挫傷 — 交通事故・高所落下等の鈍的胸部外傷後に発生。"
        "最初の24-72時間はICU管理でECG連続モニタリングが必須 — 心室性不整脈（VPC/VT）が最大のリスク。"
        "抗不整脈薬：心室性頻拍にはリドカイン（0.25-0.5 mg/kg IV slow bolus→10-40 μg/kg/min CRI）。"
        "疼痛管理：ブプレノルフィン（0.02 mg/kg IV/IM q6-8h）またはフェンタニルCRI。NSAIDsは出血リスクがあり急性期は避ける。"
        "心膜液貯留時は心嚢穿刺。酸素療法。輸液は慎重に（心機能低下下での容量負荷は肺水腫を誘発）。"
        "胸部X線・FAST echo・トロポニンI測定で心筋損傷の範囲を評価。多くは2-4週間で心筋機能が回復するが、重症例は急性心不全に進行しうる。"
    )
}

ENRICHMENTS["cat_feline_congestive_heart_failure"] = {
    "treatment_ja": (
        "急性期：酸素療法＋フロセミド（2-4 mg/kg IV、効果不十分なら1-2時間後に再投与）で肺水腫/胸水を軽減。"
        "猫はストレスで急変するため、最小限のハンドリングで処置。胸水にはエコーガイド下胸腔穿刺。"
        "維持療法：フロセミド（1-2 mg/kg PO q12-24h、最低有効量を探索）。"
        "ピモベンダン（0.625-1.25 mg/cat PO q12h — SAM非存在確認後に開始）で収縮力増強＋血管拡張。"
        "ACE阻害薬（ベナゼプリル0.5 mg/kg PO q24h）で前負荷/後負荷軽減。"
        "血栓塞栓症予防：クロピドグレル（18.75 mg/cat PO q24h）は左房拡大時に開始。"
        "呼吸数モニタリング（安静時RR>40回/分は再代償不全を示唆）。腎機能モニタリング（BUN/Cre q2-4週）。低ナトリウム食。"
    )
}

ENRICHMENTS["cat_feline_chronic_vomiting_idiopathic"] = {
    "treatment_ja": (
        "除外診断が前提 — 膵炎（fPLI測定）、甲状腺機能亢進症（T4）、CKD、消化管異物、リンパ腫を除外。"
        "食事試験が第一選択：新奇蛋白食（鹿肉/カンガルー）または加水分解蛋白食を8-12週間厳格に試行。"
        "制吐薬：マロピタント（1 mg/kg SC/PO q24h）は中枢性・末梢性嘔吐を抑制。"
        "酸分泌抑制：オメプラゾール（1 mg/kg PO q24h×4週）で胃酸関連の嘔吐を管理。"
        "IBD精査（内視鏡＋生検が確定診断に不可欠）後にプレドニゾロン（1-2 mg/kg PO q24h→漸減）。"
        "プロバイオティクス＋コバラミン補充（250 μg/cat SC q週×6週）で消化管環境改善。"
        "食欲低下時はミルタザピン（1.88 mg/cat PO q48h）またはカプロモレリン。体重と嘔吐頻度を継続記録。"
    )
}

ENRICHMENTS["cat_feline_oral_squamous_cell_carcinoma_sublingual"] = {
    "treatment_ja": (
        "舌下SCCは猫の口腔腫瘍で最も予後不良 — 早期発見でもMST 1-3ヶ月。"
        "外科切除は解剖学的位置から根治的マージン確保が極めて困難。舌部分切除は嚥下障害を伴う。"
        "緩和的放射線療法（8 Gy×4回 weekly等）で一時的な腫瘍縮小と疼痛軽減。"
        "化学療法：カルボプラチン（200-240 mg/m² IV q3週）は単剤で部分奏効率10-20%。"
        "COX-2阻害薬：メロキシカム（0.05 mg/kg PO q24h）で抗腫瘍＋鎮痛効果。"
        "疼痛管理が重要：ブプレノルフィン頬粘膜（0.02 mg/kg q8-12h）、ガバペンチン（5-10 mg/kg PO q8h）、フェンタニルパッチ（12.5-25 μg/hr）。"
        "食道瘻チューブで栄養管理。QOL評価スコアを用いた定期的な安楽死時期の検討が不可欠。"
    )
}

ENRICHMENTS["cat_feline_right-sided_congestive_heart_failure"] = {
    "treatment_ja": (
        "右心不全では腹水・胸水・末梢浮腫が主徴。利尿薬：フロセミド（1-2 mg/kg PO q12h）が基本で、"
        "スピロノラクトン（1-2 mg/kg PO q12h）を追加してRAAS過剰活性を抑制。"
        "大量腹水にはエコーガイド下腹腔穿刺で症状緩和（1回で大量排液は避け、循環動態に注意）。"
        "胸水貯留時は胸腔穿刺を実施。ピモベンダン（0.625-1.25 mg/cat PO q12h）で右室収縮力を支持。"
        "ACE阻害薬（ベナゼプリル0.5 mg/kg PO q24h）。"
        "原因精査が不可欠：三尖弁異形成、ARVC、肺高血圧症、心膜疾患、フィラリア症。"
        "心エコーで右房/右室拡大・TR重症度・肺動脈圧を評価。低ナトリウム食。安静時RRモニタリング。"
        "猫の右心不全は左心不全より稀であり、先天性心疾患や心筋症の鑑別が重要。"
    )
}

ENRICHMENTS["cat_feline_chronic_progressive_polyarthritis"] = {
    "treatment_ja": (
        "免疫介在性多発性関節炎。免疫抑制療法：プレドニゾロン（2 mg/kg PO q12h×2-4週→漸減して維持量0.5-1 mg/kg q48h）。"
        "ステロイド単独で不十分時はクロラムブシル（0.1-0.2 mg/kg PO q48-72h）を追加し、"
        "CBC q2-4週で骨髄抑制をモニタリング。シクロスポリン（5-7 mg/kg PO q24h）も代替。"
        "疼痛管理：ブプレノルフィン（0.02 mg/kg 頬粘膜 q8-12h）急性期に。ガバペンチン（5-10 mg/kg PO q8-12h）長期鎮痛。"
        "フルネベトマブ（ソレンシア 1 mg/kg SC q月）は抗NGF抗体でOA疼痛に承認されているが免疫介在性にも補助的。"
        "FeLV/FIV関連の場合があるため検査必須。X線で関節びらん/骨増殖を経時的に評価。理学療法/温罨法で関節可動域を維持。"
    )
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
