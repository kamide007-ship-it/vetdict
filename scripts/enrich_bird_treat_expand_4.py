#!/usr/bin/env python3
"""Bird treatment_ja expansion — batch 4."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["bird_erysipelas"] = {
    "treatment_ja": (
        "ペニシリンG（100 mg/kg IM q12h×7-10日）が第一選択で高い感受性を示す。"
        "アモキシシリン（100-150 mg/kg PO q12h）も有効。急性期は積極的輸液と保温。"
        "七面鳥群にはワクチン接種が有効。人獣共通感染症のため取り扱い時の個人防護を徹底。"
        "敗血症型では集中的な支持療法を要し、慢性関節炎型には3-4週間の長期投与が必要。"
    )
}

ENRICHMENTS["bird_gastrointestinal_foreign_body"] = {
    "treatment_ja": (
        "レントゲンで異物の位置・大きさを確認。腸管内小異物は流動パラフィン（1-2 mL/kg PO）で通過促進。"
        "金属異物はキレーション療法と内視鏡的/外科的除去。腸閉塞は緊急手術（腸切開術）。"
        "術後管理として抗菌薬、鎮痛薬（メロキシカム0.5 mg/kg PO SID）、段階的経口摂食再開。"
        "術後48時間は少量頻回給餌とし、消化管運動の回復を確認する。"
    )
}

ENRICHMENTS["bird_heavy_metal_poisoning_–_mixed_lead_and_zinc"] = {
    "treatment_ja": (
        "異物の除去（レントゲンで金属片確認→内視鏡的/外科的摘出）が最優先。"
        "CaEDTA（35 mg/kg IM BID×5日、休薬2日、反復）が鉛・亜鉛両方に有効。"
        "D-ペニシラミン（55 mg/kg PO BID）を経口で併用。痙攣管理にジアゼパム（0.5-1 mg/kg IM）。"
        "輸液、保温、血中鉛・亜鉛濃度の定期モニタリング。環境中の金属源を完全除去し再発を防止する。"
    )
}

ENRICHMENTS["bird_hepatic_amyloidosis"] = {
    "treatment_ja": (
        "根治療法はない。基礎疾患（慢性感染症）の治療でアミロイド沈着の進行を抑制。"
        "コルヒチン（0.04 mg/kg PO SID）がアミロイド形成抑制に使用される。"
        "肝保護療法（シリマリン、ラクツロース0.3 mL/kg PO BID）を併用。"
        "腹水管理にフロセミド（2 mg/kg PO BID）。肝破裂リスクがあるため激しい保定は避ける。"
        "予後不良だが基礎疾患治療で進行遅延が期待できる。"
    )
}

ENRICHMENTS["bird_hexamitosis"] = {
    "treatment_ja": (
        "メトロニダゾール（25-50 mg/kg PO q12h×7-10日）が第一選択。"
        "ロニダゾール（10 mg/kg PO q24h×7日）も有効。脱水補正のための輸液療法（10-25 mL/kg SC BID）。"
        "保温（28-30℃）と栄養支持（経管栄養含む）。飲水器の毎日洗浄・消毒で再感染を防止。"
        "群全体の同時治療が蔓延防止に重要。回復後の定期的糞便検査で再発を監視する。"
    )
}

ENRICHMENTS["bird_histoplasmosis"] = {
    "treatment_ja": (
        "鳥類が臨床症状を示すことは稀だが、発症例にはイトラコナゾール（5-10 mg/kg PO BID×3-6ヶ月）を投与。"
        "重症例にはアムホテリシンB（1.5 mg/kg IV SID×3-5日）で導入後、アゾール系で維持。"
        "飼育環境の消毒（糞便除去、石灰散布）を実施。人獣共通感染症として飼い主への注意喚起が重要で、"
        "鳥舎清掃時のN95マスク着用を推奨する。肝機能モニタリングを定期的に行う。"
    )
}

ENRICHMENTS["bird_hypervitaminosis_a"] = {
    "treatment_ja": (
        "ビタミンA投与の即時中止が最優先。支持療法として輸液と肝保護療法（シリマリン、ラクツロース）。"
        "食事をバランスの良いペレット食に変更し、βカロテン豊富な野菜で安全にビタミンAを供給。"
        "皮膚症状への対症療法（保湿剤塗布）。骨格異常は不可逆的な場合がある。"
        "メロキシカム（0.5 mg/kg PO SID）で骨痛管理。回復には数週間～数ヶ月を要する。"
    )
}

ENRICHMENTS["bird_hypervitaminosis_d"] = {
    "treatment_ja": (
        "ビタミンD投与の即時中止。積極的輸液（生理食塩水10-25 mL/kg SC BID）で高Ca血症を希釈・排泄促進。"
        "フロセミド（2-4 mg/kg IM BID）でCa排泄促進。低Ca食への変更。"
        "重度の高Ca血症にはカルシトニン（50 IU/kg SC SID×3日）。軟部組織石灰化は不可逆的であり、"
        "腎機能モニタリング（尿酸・電解質）を継続。UVBライト照射時間の適正化指導も行う。"
    )
}

ENRICHMENTS["bird_infectious_laryngotracheitis_ilt_advanced"] = {
    "treatment_ja": (
        "緊急気道管理が最優先。偽膜の愛護的除去（内視鏡下が理想）。"
        "気嚢チューブ設置が必要になる場合あり。デキサメタゾン（2-4 mg/kg IM）で気道浮腫軽減。"
        "酸素吸入と保温。二次感染予防にエンロフロキサシン（15 mg/kg PO BID）。ネブライゼーション（生理食塩水）で気道加湿。"
        "感染群の隔離と環境消毒。ワクチンプログラムの導入で群内の再発を防止する。"
    )
}

ENRICHMENTS["bird_ingluvitis_crop_infection"] = {
    "treatment_ja": (
        "カンジダ性：ナイスタチン（300,000 IU/kg PO BID×7-14日）。"
        "トリコモナス性：メトロニダゾール（25 mg/kg PO BID×7日）またはロニダゾール（10 mg/kg PO SID×7日）。"
        "細菌性：培養感受性に基づく抗菌薬。嗉嚢洗浄と少量頻回給餌で嗉嚢の回復を促進。"
        "基礎疾患（免疫抑制、栄養不良）の治療が再発防止に重要。さし餌の温度管理（38-40℃）を指導。"
    )
}

ENRICHMENTS["bird_intestinal_intussusception"] = {
    "treatment_ja": (
        "外科的治療が原則。整復可能であれば用手整復、壊死が生じていれば腸管切除吻合術を実施。"
        "術前安定化として輸液、保温、鎮痛（メロキシカム0.5 mg/kg IM）を行う。"
        "術後管理：抗菌薬（エンロフロキサシン15 mg/kg IM BID）、段階的経口摂食再開。"
        "基礎疾患（寄生虫、腸炎）の駆除・治療。再発リスクの評価と術後モニタリングを継続する。"
    )
}

ENRICHMENTS["bird_leucocytozoonosis"] = {
    "treatment_ja": (
        "ピリメタミン（0.5 mg/kg PO BID）＋スルファジアジン（30 mg/kg PO BID×14日）が標準治療。"
        "支持療法として輸血（重度貧血時、同種血1-2 mL/100g BW）、輸液、保温を行う。"
        "重度貧血にはFe-dextran（10 mg/kg IM）。媒介昆虫（ブユ）の駆除と飛来防止（防虫ネット）。"
        "屋内飼育への切替が効果的。定期的な血液塗抹検査で寄生虫血症をモニタリングする。"
    )
}

ENRICHMENTS["bird_lice_mallophaga"] = {
    "treatment_ja": (
        "イベルメクチン（0.2 mg/kg PO/SC/経皮、14日後に再投与）が第一選択。"
        "小型鳥にはセラメクチン経皮投与（スポットオン6 mg/kg）が安全で使いやすい。"
        "ピレスリン系スプレー（0.03%）を直接噴霧。環境消毒（止まり木、巣箱の熱湯消毒）が必須。"
        "同居鳥全羽の同時治療で再寄生を防止。卵（ニット）の孵化サイクルに合わせ2-3回反復治療する。"
    )
}

ENRICHMENTS["bird_malnutrition___cachexia"] = {
    "treatment_ja": (
        "段階的な栄養回復が重要で、急速な再栄養はリフィーディング症候群のリスクがある。"
        "経管栄養（市販流動食を嗉嚢チューブで投与、体重の3-5%/日から開始し徐々に増量）。"
        "ビタミン・ミネラルの補給（総合ビタミン注射を初期に）。保温（28-30℃）と安静。"
        "食事改善としてペレット食への移行を指導。基礎疾患の特定と治療を並行して進める。"
    )
}

ENRICHMENTS["bird_microsporidiosis"] = {
    "treatment_ja": (
        "フェンベンダゾール（20 mg/kg PO SID×28日）が第一選択。"
        "アルベンダゾール（15 mg/kg PO SID×28日）も使用可能。腎保護療法として輸液（10-25 mL/kg SC BID）と"
        "アロプリノール（10 mg/kg PO SID）を併用。二次感染予防の抗菌薬投与。"
        "免疫状態の改善（栄養管理、ストレス軽減）が治療成功の鍵。環境消毒を徹底。"
        "長期治療が必要で完全根治は困難な場合がある。"
    )
}

ENRICHMENTS["bird_mycoplasmosis"] = {
    "treatment_ja": (
        "ドキシサイクリン（25-50 mg/kg PO q24h×14-21日）またはエンロフロキサシン（15 mg/kg PO q12h）が第一選択。"
        "チルミコシン（20 mg/kg PO q24h）も有効。副鼻腔洗浄（生理食塩水）で局所症状を緩和。"
        "眼科症状にはオフロキサシン点眼（0.3% q6-8h）。完全除菌は困難でキャリア化しやすく、"
        "ストレス軽減と免疫状態の維持が再発防止に重要。同居鳥の検査・治療も検討する。"
    )
}

ENRICHMENTS["bird_myiasis_fly_strike"] = {
    "treatment_ja": (
        "全ての幼虫の物理的除去（ピンセット使用）が最優先。創傷の徹底洗浄（生理食塩水＋希釈クロルヘキシジン0.05%）。"
        "壊死組織のデブリードメント。抗菌薬（エンロフロキサシン15 mg/kg PO BID×7-10日）で二次感染治療。"
        "メロキシカム（0.5 mg/kg PO SID）で鎮痛。創傷管理として銀スルファジアジン軟膏を局所塗布。"
        "飼育環境のハエ対策（防虫ネット、清掃の徹底）で再発を防止する。"
    )
}

ENRICHMENTS["bird_myopathy_nutritional___capture"] = {
    "treatment_ja": (
        "栄養性ミオパチー：ビタミンE（100-200 IU/kg IM/PO）＋セレン（0.06 mg/kg IM 単回）を投与。"
        "捕獲性ミオパチー：積極的輸液（25 mL/kg SC BID）で腎灌流維持とミオグロビン排泄促進。"
        "メロキシカム（0.5 mg/kg PO SID）で鎮痛。保温、絶対安静。"
        "重度の腎障害ではアロプリノール（10 mg/kg PO SID）併用。血中CK値でモニタリング。"
        "捕獲性は予防が最重要で、保定時間を最小限に抑える。"
    )
}

ENRICHMENTS["bird_nail_overgrowth___nail_injury"] = {
    "treatment_ja": (
        "爪トリミング（適切な長さに爪切りで切断、血管ラインの手前で止める）。"
        "出血時はスタイプティックパウダーまたは硝酸銀棒で止血。"
        "重度の爪根損傷にはエンロフロキサシン局所塗布と全身抗菌薬投与を検討。"
        "粗い表面の止まり木（コンクリートパーチ等）の提供で自然な爪摩耗を促進。"
        "基礎疾患（肝疾患、栄養不良、疥癬）があれば併せて治療し根本原因を解決する。"
    )
}

ENRICHMENTS["bird_nephritis"] = {
    "treatment_ja": (
        "輸液療法（10-25 mL/kg SC BID）で腎灌流維持と脱水補正が基本。"
        "細菌性にはエンロフロキサシン（15 mg/kg PO BID×14-21日）。"
        "アロプリノール（10 mg/kg PO SID）で高尿酸血症を管理。"
        "腎毒性薬剤（アミノグリコシド等）の即時中止。低蛋白食への変更。"
        "定期的な尿酸・電解質モニタリングで腎機能を評価。慢性腎不全への進行を防ぐため早期治療が重要。"
    )
}

ENRICHMENTS["bird_niacin_deficiency_pellagra"] = {
    "treatment_ja": (
        "ナイアシン補給（50-100 mg/kg 飼料に添加、または10 mg/kg BW PO SID）。"
        "重症例では注射投与（ニコチン酸アミド10 mg/kg IM SID×5日）で速やかに改善。"
        "食事改善としてペレット食、魚粉・酵母含有飼料への変更。"
        "滑腱症が進行した場合は矯正困難であり、早期発見と栄養改善が極めて重要。"
        "成長期の幼鳥では特に注意が必要で、バランス食への早期移行を推奨する。"
    )
}

ENRICHMENTS["bird_ornithobacterium_rhinotracheale_ort_infection"] = {
    "treatment_ja": (
        "アモキシシリン（100-150 mg/kg PO q12h×10日）が比較的有効。"
        "ドキシサイクリン（25-50 mg/kg PO q24h）も使用される。"
        "感受性試験が推奨で、多くのORT株はエンロフロキサシンに耐性を示す点に注意。"
        "ネブライゼーション療法（生理食塩水＋F10 1:250希釈）で気道症状を緩和。"
        "環境改善（換気、粉塵低減、飼育密度低下）。家禽群ではワクチン接種が有効。"
    )
}

ENRICHMENTS["bird_ornithobacterium_rhinotracheale_ort_pneumonia"] = {
    "treatment_ja": (
        "アモキシシリン/クラブラン酸（125 mg/kg PO BID×7-10日）が感受性が高い。"
        "テトラサイクリン系（ドキシサイクリン25-50 mg/kg PO BID）も有効。"
        "培養感受性試験が推奨で、多剤耐性株が報告されている。ネブライゼーション（生理食塩水）で気道加湿。"
        "保温（28-30℃）と栄養管理（経管栄養含む）。環境の換気改善と粉塵除去。"
        "重症例では酸素吸入を併用し、呼吸状態を継続モニタリングする。"
    )
}

ENRICHMENTS["bird_papillomatosis_–_oral_form"] = {
    "treatment_ja": (
        "外科的切除（レーザー蒸散・電気焼灼）を繰り返し実施。再発率が高いため定期的な内視鏡フォローアップが必須。"
        "インターフェロン療法（1000-10000 IU/kg SC 週3回）の併用を検討。"
        "自家ワクチン療法（切除組織由来）の試みが報告されている。重度の口腔内病変では経管栄養が必要。"
        "胆管浸潤の有無を画像検査（超音波、X線造影）で確認し、予後評価を行う。"
    )
}

ENRICHMENTS["bird_phallus_prolapse"] = {
    "treatment_ja": (
        "脱出組織の洗浄（生理食塩水温水）と浮腫軽減（砂糖水浸漬または50%ブドウ糖液塗布）。"
        "愛護的に用手整復し、総排泄腔に巾着縫合を設置。壊死が進行した場合は陰茎切断術を実施。"
        "抗菌薬（エンロフロキサシン15 mg/kg PO BID）とメロキシカム（0.5 mg/kg PO SID）で感染予防と鎮痛。"
        "再発例では外科的切断を積極的に検討する。水禽では比較的多く見られる。"
    )
}

ENRICHMENTS["bird_pituitary_adenoma"] = {
    "treatment_ja": (
        "外科的切除は技術的に極めて困難。緩和療法が中心。"
        "デキサメタゾン（0.5-1 mg/kg PO SID）で腫瘍周囲浮腫軽減。"
        "プロラクチン産生腫瘍にはカベルゴリン（0.01 mg/kg PO BID）の試み。"
        "視力喪失例では環境調整（ケージレイアウト固定、餌・水の位置を変えない）。"
        "セキセイインコでの報告が多い。予後は不良だが数ヶ月の延命は可能で、QOL維持に注力する。"
    )
}

ENRICHMENTS["bird_plant_toxicity"] = {
    "treatment_ja": (
        "活性炭（1-3 g/kg PO）で消化管内毒素吸着（摂取後2時間以内が理想）。"
        "アボカド中毒：支持療法（輸液、心不全管理にフロセミド2-6 mg/kg IM）、特異的解毒薬なし。"
        "ジギタリス中毒：不整脈管理。全般的に支持療法（輸液、保温、栄養支持）が中心。"
        "有毒植物の同定と環境からの完全除去が最重要。放鳥時の室内植物管理を飼い主に指導する。"
    )
}

ENRICHMENTS["bird_preen_gland_carcinoma"] = {
    "treatment_ja": (
        "広範囲外科的切除（尾脂腺摘出＋周囲組織のマージン確保）が第一選択。"
        "転移スクリーニング（全身レントゲン、超音波検査）を実施。"
        "術後の病理検査で切除マージン評価を行い、不完全切除なら再手術を検討。"
        "メロキシカム（0.5 mg/kg PO SID）で鎮痛。転移例では緩和ケア主体。"
        "術後の定期的な再発チェック（月1回×6ヶ月）を推奨する。"
    )
}

ENRICHMENTS["bird_proventricular_impaction"] = {
    "treatment_ja": (
        "原因疾患の治療が根本対策。PDD（鳥類ボルナウイルス感染症）にはセレコキシブ等の抗炎症療法、"
        "重金属中毒にはキレーション療法を実施。"
        "メトクロプラミド（0.5 mg/kg PO/IM BID-TID）で消化管運動促進。輸液で脱水補正。"
        "少量頻回の流動食による経管栄養と保温。異物が原因の場合は内視鏡的または外科的除去を行う。"
    )
}

ENRICHMENTS["bird_proventricular_nematodes"] = {
    "treatment_ja": (
        "フェンベンダゾール（20-50 mg/kg PO SID×5日）が第一選択。レバミゾール（20 mg/kg PO 単回）も有効。"
        "重度の腺胃損傷には抗潰瘍薬（スクラルファート30 mg/kg PO TID）を併用し粘膜保護を図る。"
        "中間宿主への曝露制限（屋外アクセス管理）。栄養支持と消化管保護。"
        "駆虫後2-3週間で糞便再検査を実施し、駆虫効果を確認。再感染予防に環境消毒を徹底する。"
    )
}

ENRICHMENTS["bird_proventricular_ulceration"] = {
    "treatment_ja": (
        "スクラルファート（30 mg/kg PO TID）で粘膜保護。プロトンポンプ阻害薬（オメプラゾール1 mg/kg PO SID）で胃酸分泌抑制。"
        "NSAIDの即時中止。重金属中毒ではキレーション療法（CaEDTA 35 mg/kg IM BID）を併用。"
        "出血性にはビタミンK1（2.5 mg/kg IM）。経管栄養で消化管安静を維持。"
        "穿孔例は緊急外科対応。原因除去後の定期的な内視鏡検査で治癒を確認する。"
    )
}

ENRICHMENTS["bird_psittacine_poxvirus_canarypox_variant"] = {
    "treatment_ja": (
        "特異的抗ウイルス療法はない。皮膚型：痂皮の保護（抗菌軟膏塗布）、二次感染予防の抗菌薬投与。"
        "粘膜型：偽膜の愛護的除去、気道確保、ネブライゼーション（生理食塩水）。"
        "ビタミンA（20,000 IU/kg IM 単回）で粘膜修復を促進。軽症の皮膚型は2-4週間で自然治癒。"
        "感染鳥の隔離と環境消毒。ワクチンが予防に最も有効で、流行地域では接種を推奨する。"
    )
}

ENRICHMENTS["bird_ptfe___teflon_toxicosis"] = {
    "treatment_ja": (
        "新鮮空気への即時移動が最緊急処置。酸素吸入（40-60%）。"
        "フロセミド（2-6 mg/kg IM BID-TID）で肺水腫軽減。デキサメタゾン（2-4 mg/kg IM）で肺炎症管理。"
        "保温と安静。予後は曝露量と時間に依存し、重度暴露では治療に反応しないことが多い。"
        "予防が最重要で、鳥のいる環境からテフロン製品（調理器具・暖房器具含む）を完全撤去する。"
    )
}

ENRICHMENTS["bird_renal_cystadenocarcinoma"] = {
    "treatment_ja": (
        "外科的切除は腎臓の解剖学的位置から極めて困難。緩和療法が中心。"
        "メロキシカム（0.5 mg/kg PO SID）で鎮痛、デキサメタゾン（0.5 mg/kg IM）で神経周囲浮腫軽減。"
        "輸液で腎機能維持。ガバペンチン（10 mg/kg PO BID）で神経痛管理。"
        "セキセイインコに好発し、片脚挙上が特徴的。予後不良だがQOL維持の対症療法を継続する。"
    )
}

ENRICHMENTS["bird_riemerella_anatipestifer_infection"] = {
    "treatment_ja": (
        "ペニシリン系（アモキシシリン150 mg/kg PO q12h×7-10日）が有効。"
        "エンロフロキサシン（15 mg/kg PO q12h）、リンコマイシン（100 mg/kg PO q12h）も使用。"
        "急性期は注射投与で速やかに血中濃度を確保。ワクチン接種（弱毒生/不活化）が予防に有効。"
        "飼育密度低減と環境改善（衛生管理、換気）。水禽に好発し、若齢鳥での死亡率が高い。"
    )
}

ENRICHMENTS["bird_rodenticide_poisoning"] = {
    "treatment_ja": (
        "ビタミンK1（2.5-5 mg/kg IM 初回、以後2.5 mg/kg PO BID×2-4週間）が特異的解毒療法。"
        "第2世代抗凝固薬では4-6週間の長期投与が必要。重度出血には輸血（新鮮全血1-2 mL/100g BW）。"
        "摂取直後なら活性炭（1-3 g/kg PO）で吸着。輸液療法。"
        "凝固能の定期検査（PT/APTT）で投与期間を決定し、正常化後7日間は追加投与を継続する。"
    )
}

ENRICHMENTS["bird_seminoma"] = {
    "treatment_ja": (
        "外科的精巣摘出が根治的治療で、片側摘出で十分な場合が多い。"
        "デスロレリンインプラント（4.7 mg SC）でGnRH抑制の試みが報告されている。"
        "腹水が伴う場合は穿刺排液で呼吸困難を緩和。緩和療法としてメロキシカム（0.5 mg/kg PO SID）で鎮痛。"
        "術後は蝋膜色の正常化で治療効果を判定。セキセイインコに好発し、蝋膜の褐色変化が特徴的所見。"
    )
}

ENRICHMENTS["bird_sour_crop_fermentative_ingluvitis"] = {
    "treatment_ja": (
        "嗉嚢洗浄（温水で内容物を排出）が初期対応。"
        "ナイスタチン（300,000 IU/kg PO BID×7-14日）でカンジダ治療。"
        "メトクロプラミド（0.5 mg/kg PO BID）で嗉嚢運動促進。少量頻回給餌で嗉嚢を休ませる。"
        "食事内容の見直し（過剰な炭水化物・糖分を制限）。基礎疾患（栄養不良、免疫抑制）の治療。"
        "幼鳥ではさし餌の温度管理（38-40℃）と希釈濃度の適正化が再発防止に重要。"
    )
}

ENRICHMENTS["bird_splay_leg_spraddle_leg"] = {
    "treatment_ja": (
        "早期介入（孵化後48-72時間以内）が治療成功の鍵。"
        "両脚を適正幅でテープ固定（ホブル法：バンドエイドや柔らかいテープで両脚を正常幅に維持）。"
        "滑りにくい床材（ペーパータオル等）に変更。カルシウム・VitD3補給。"
        "7-14日間の固定で多くの症例が矯正可能。重症例や介入遅延例では予後不良。"
        "予防として適切な巣箱床材と親鳥の栄養管理を指導する。"
    )
}

ENRICHMENTS["bird_splenic_disease_splenitis"] = {
    "treatment_ja": (
        "原因感染症の治療が根本対策。細菌性：エンロフロキサシン（15 mg/kg PO BID×14-21日）。"
        "クラミジア性：ドキシサイクリン（25-50 mg/kg PO BID×45日間）。"
        "マイコバクテリア性：リファンピシン＋エタンブトール（長期、6ヶ月以上）。"
        "支持療法と免疫状態の改善。脾腫の定期モニタリング（超音波検査）で治療効果を評価する。"
        "脾破裂のリスクに注意し保定は愛護的に行う。"
    )
}

ENRICHMENTS["bird_streptococcal_infection"] = {
    "treatment_ja": (
        "ペニシリン系が第一選択。アモキシシリン（100-150 mg/kg PO q12h×10-14日）。"
        "セファレキシン（75-100 mg/kg PO q8h）も有効。"
        "敗血症にはアンピシリン（100 mg/kg IM/IV q6-8h）を注射で投与。"
        "関節炎が合併している場合は3-4週間の長期投与が必要。"
        "輸液・保温による支持療法。培養感受性試験に基づく薬剤選択が理想的。環境消毒を徹底する。"
    )
}

ENRICHMENTS["bird_syngamus_gapeworm"] = {
    "treatment_ja": (
        "フェンベンダゾール（20-50 mg/kg PO SID×3-5日）が第一選択。"
        "レバミゾール（20 mg/kg PO 単回）は速効性がある。イベルメクチン（0.2 mg/kg PO）も有効。"
        "重度気管閉塞時は内視鏡下での虫体除去を検討。酸素吸入と保温で呼吸状態を安定化。"
        "屋外飼育でのミミズ摂取制限が再感染防止に重要。駆虫後の糞便再検査で効果を確認する。"
    )
}

ENRICHMENTS["bird_syngamus_trachea_gapeworm_advanced"] = {
    "treatment_ja": (
        "緊急駆虫：フェンベンダゾール（50 mg/kg PO SID×5日）。レバミゾール（20 mg/kg PO）は速効性。"
        "重度閉塞では内視鏡下での虫体直接除去を検討。酸素吸入、デキサメタゾン（2 mg/kg IM）で気道浮腫軽減。"
        "死滅虫体による気道閉塞にも注意しネブライゼーションで排出促進。"
        "屋外アクセス管理で中間宿主への曝露を制限し再感染を防止する。"
    )
}

ENRICHMENTS["bird_tapeworms_cestodes"] = {
    "treatment_ja": (
        "プラジカンテル（5-10 mg/kg PO or IM 単回、14日後反復）が第一選択。"
        "ニクロサミド（250 mg/kg PO 単回）も有効。駆虫後2-3週間で糞便再検査を実施し効果を確認。"
        "中間宿主への曝露制限（屋外アクセス管理、昆虫駆除）が再感染防止に重要。"
        "反復感染が多い場合は定期的な駆虫プログラム（3-6ヶ月毎）と環境管理の徹底が必要。"
    )
}

ENRICHMENTS["bird_thiamine_deficiency_star-gazing"] = {
    "treatment_ja": (
        "チアミン緊急投与（1-2 mg/kg IM/SC）で速やかに神経症状が改善する場合が多い。"
        "維持療法として経口チアミン補給（1-2 mg/kg PO SID×7-14日）。"
        "食事改善が根本治療で、生魚食の加熱処理（チアミナーゼ失活）やチアミン含有飼料への変更を行う。"
        "痙攣が持続する場合はジアゼパム（0.5 mg/kg IM）で緊急制御。魚食鳥での発生が多い。"
        "迅速な治療で劇的に改善し予後良好。"
    )
}

ENRICHMENTS["bird_thyroid_carcinoma"] = {
    "treatment_ja": (
        "外科的切除が可能な場合は甲状腺片側切除を実施。完全切除困難例では緩和療法が中心。"
        "デキサメタゾン（0.5-1 mg/kg IM）で腫瘍周囲浮腫軽減。"
        "放射性ヨウ素治療は鳥類でのエビデンスが限定的。術後の甲状腺ホルモン補充（レボチロキシン0.02 mg/kg PO BID）。"
        "呼吸困難管理として酸素吸入と保温。QOL維持の対症療法を継続する。"
    )
}

ENRICHMENTS["bird_tracheal_obstruction"] = {
    "treatment_ja": (
        "緊急気道確保が最優先。気嚢チューブの設置（腹部気嚢に18-20Gカテーテル挿入）が救命処置。"
        "安定化後に内視鏡下で閉塞原因を除去（異物摘出、肉芽腫デブリードメント）。"
        "デキサメタゾン（2-4 mg/kg IM）で気道浮腫軽減。酸素吸入と保温を継続。"
        "原因に応じた根治治療（感染症→抗菌薬、アスペルギルス→抗真菌薬、腫瘍→外科的切除）を実施する。"
    )
}

ENRICHMENTS["bird_tracheal_papilloma"] = {
    "treatment_ja": (
        "内視鏡下でのレーザー蒸散・電気焼灼が標準治療。再発が多いため定期的な内視鏡検査が必要。"
        "インターフェロン療法（1000-10000 IU/kg SC 週3回）の併用を検討。"
        "重度狭窄時は気嚢チューブで気道確保。アシクロビル（80 mg/kg PO TID）は抗ウイルス効果が限定的。"
        "内部乳頭腫症との関連を評価するため、消化管の内視鏡スクリーニングも推奨する。"
    )
}

ENRICHMENTS["bird_uropygial_gland_impaction"] = {
    "treatment_ja": (
        "温罨法と愛護的な腺管マッサージで閉塞物の排出を試みる。"
        "排出不能な場合は鎮静下に小切開して貯留物を除去。"
        "ビタミンA（20,000 IU/kg IM 単回）で腺上皮の正常化を促進。局所抗菌薬（ムピロシン軟膏等）で二次感染予防。"
        "食事改善（βカロテン豊富な緑黄色野菜の追加）。反復例では腺摘出術を検討するが、"
        "羽毛の防水性低下に留意する。"
    )
}

ENRICHMENTS["bird_visceral_gout_–_acute_form"] = {
    "treatment_ja": (
        "緊急輸液（ボーラス25 mL/kg IO/IV後、維持輸液10 mL/kg/h）が最優先。"
        "アロプリノール（10 mg/kg PO BID）を速やかに開始。腎毒性薬剤の即時中止。"
        "保温（30-32℃）、酸素吸入。メロキシカム（0.5 mg/kg IM）で鎮痛。"
        "急性型は死亡率が極めて高く、集中治療を要する。食事を低蛋白食に変更し腎負荷を軽減。"
        "原因（脱水、腎毒性薬、高蛋白食）の特定と再発防止が重要。"
    )
}

ENRICHMENTS["bird_vitamin_d_toxicosis_hypervitaminosis_d_–_renal_form"] = {
    "treatment_ja": (
        "VitD投与の即時中止。積極的輸液で高Ca血症希釈と腎灌流維持。"
        "フロセミド（2-4 mg/kg IM BID）でCa排泄促進。カルシトニン（50 IU/kg SC SID×3日）で骨からのCa動員抑制。"
        "低Ca食への変更。アロプリノール（10 mg/kg PO SID）で腎保護。"
        "腎機能（尿酸・電解質）の継続的モニタリング。軟部組織石灰化は不可逆的であり、予防が重要。"
    )
}

ENRICHMENTS["bird_vitamin_e___selenium_deficiency"] = {
    "treatment_ja": (
        "ビタミンE（100 IU/kg PO SID×14日、以後維持量）とセレン（亜セレン酸ナトリウム0.06 mg/kg IM 単回）を投与。"
        "急性脳軟化症にはビタミンE高用量（200 IU/kg IM）を緊急投与するが、脳病変は不可逆的な場合がある。"
        "食事改善として新鮮な種子、ペレット食、緑葉野菜に変更。酸化した古い飼料は廃棄。"
        "維持的なビタミンEサプリメント継続で再発を防止する。"
    )
}

ENRICHMENTS["bird_vitamin_k_deficiency"] = {
    "treatment_ja": (
        "ビタミンK1（フィトメナジオン）2.5 mg/kg IM/SCで緊急止血に有効。"
        "殺鼠剤中毒による場合は2-4週間の経口ビタミンK1投与が必要（第2世代では4-6週間）。"
        "重度出血には輸血（新鮮全血1-2 mL/100g BW）で凝固因子を補充。"
        "肝疾患が原因の場合は肝保護療法を併用。長期抗菌薬投与中はビタミンK予防的補給を検討。"
        "凝固能（PT/APTT）の定期モニタリングで投与期間を決定する。"
    )
}

ENRICHMENTS["bird_zinc-responsive_dermatosis"] = {
    "treatment_ja": (
        "亜鉛補給（亜鉛グルコン酸塩2 mg/kg PO SID×4-6週間）が第一選択。"
        "食事改善として亜鉛含有量の適切なペレット食への変更を行う。"
        "局所治療（保湿・軟化剤の塗布）で過角化病変を緩和。改善には2-4週間を要する。"
        "フィチン酸を多く含む種子食は亜鉛吸収を阻害するため制限。"
        "ビタミンA欠乏の併発が多いためビタミンA（5,000-10,000 IU/kg IM）の補給も検討する。"
    )
}

ENRICHMENTS["bird_zinc_poisoning"] = {
    "treatment_ja": (
        "異物の除去（レントゲンで金属片確認→内視鏡的/外科的摘出）が最優先。"
        "CaEDTA（35 mg/kg IM BID×5日、休薬2日、反復）でキレーション療法。"
        "D-ペニシラミン（55 mg/kg PO BID）の経口キレーションも使用。"
        "輸液療法で腎灌流維持と亜鉛排泄促進。溶血性貧血にはデキストラン鉄と必要時輸血。"
        "亜鉛メッキケージをステンレス製またはパウダーコーティング製に変更し再発を防止する。"
    )
}


def apply_enrichments() -> None:
    """Apply treatment_ja enrichments to diseases JSON."""
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
