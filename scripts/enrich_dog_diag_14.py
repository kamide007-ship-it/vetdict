#!/usr/bin/env python3
import json
import os
import time

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diseases_all_species.json")

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_salivary_mucocele_sialocele"] = {"diagnosis_ja": (
    "身体検査で顎下/舌下の波動性腫脹を確認。FNA（穿刺吸引）で粘稠な透明～淡黄色液体（ムチン含有）。"
    "細胞診で少数のマクロファージ・好中球と粘液を確認。培養で感染性を除外。"
    "X線/超音波で唾液腺の原発部位（舌下腺が最多）を同定。CT/MRIで複雑例の範囲評価。"
    "舌下型（ranula）、頸部型、咽頭型を臨床所見で分類。唾液腺摘出（下顎腺+舌下腺）が根治療法。"
)}

ENRICHMENTS["dog_sinonasal_aspergillosis"] = {"diagnosis_ja": (
    "鼻腔内視鏡で白色～緑色の真菌プラーク（fungal plaques）を直接確認。壊死性の鼻甲介破壊。"
    "CT/MRIで鼻甲介の骨溶解・篩板の状態を評価。篩板破壊→頭蓋内進展のリスク。"
    "血清Aspergillus抗体価上昇（AGID/ELISA: 感度60-90%）。鼻腔スワブ/生検の培養。"
    "PCRでAspergillus属を同定。鼻出血・慢性膿性鼻汁・鼻鏡色素脱失の臨床症状。局所クロトリマゾール注入が第一選択。"
)}

ENRICHMENTS["dog_peritonitis"] = {"diagnosis_ja": (
    "腹腔穿刺で腹水を回収。腹腔液分析: 細胞数>500/μL、蛋白>2.5 g/dL、細菌培養陽性は敗血性腹膜炎。"
    "腹腔液/血漿クレアチニン比>2.0で尿腹を確認。腹腔液ビリルビン/血漿比>2.0で胆汁性腹膜炎。"
    "CBC/CRP/乳酸で全身性炎症反応を評価。腹部超音波で遊離液体・原因（穿孔/破裂）を検索。"
    "CT/造影CTで消化管穿孔・膿瘍を評価。血液培養で菌血症を確認。緊急外科的探索が必要。"
)}

ENRICHMENTS["dog_hemoabdomen"] = {"diagnosis_ja": (
    "腹腔穿刺でPCV>10%の血性液を回収（peritoneoccentesis）。腹腔液PCVと末梢血PCVの比較。"
    "腹部超音波で遊離液体と原因（脾臓腫瘤/肝臓腫瘤/副腎腫瘤）を検索。FAST scan。"
    "CBC/凝固検査で貧血の程度・DICを評価。血液ガスで乳酸・酸塩基を評価。"
    "外傷性vs非外傷性を鑑別。非外傷性の最多原因はHSA（脾臓/肝臓）。緊急安定化+輸血+外科的止血。"
)}

ENRICHMENTS["dog_urinary_bladder_tumor_tcc"] = {"diagnosis_ja": (
    "尿検査で血尿、尿沈渣で異型細胞を検出。BRAF V595E変異検査（尿: 感度85%）で非侵襲的診断。"
    "腹部超音波で膀胱三角部の腫瘤を確認。超音波ガイド下カテーテル生検（TCC播種リスクに注意）。"
    "CT/MRIで腫瘍の範囲・尿管閉塞・リンパ節転移を評価。X線で肺転移スクリーニング。"
    "スコティッシュ・テリア、ウエスト・ハイランド・ホワイト・テリアに好発。ピロキシカム+ミトキサントロン/カルボプラチン。"
)}

ENRICHMENTS["dog_pancreatic_adenocarcinoma"] = {"diagnosis_ja": (
    "腹部超音波で膵臓の低エコー腫瘤を確認。肝転移・リンパ節転移を評価。"
    "CT/造影CTで腫瘍の範囲・血管浸潤・遠隔転移を三次元評価。"
    "超音波ガイド下FNA/生検で腺癌細胞を確認。cPLI/リパーゼは正常～上昇。"
    "CBC/生化学でALP/ALT/GGT上昇（胆管閉塞時）、低血糖（インスリノーマとの鑑別）。予後極めて不良。"
)}

ENRICHMENTS["dog_adrenal_gland_tumor"] = {"diagnosis_ja": (
    "腹部超音波で副腎腫大（長径>2 cm/犬の体格依存）を確認。対側副腎の萎縮で機能性を示唆。"
    "ACTH刺激試験/LDDSTでクッシング症候群を精査。UCCRスクリーニング。"
    "CT/MRIで腫瘍サイズ・後大静脈浸潤（腫瘍血栓）・肺転移を評価。"
    "血圧測定で高血圧（褐色細胞腫を鑑別）。尿中カテコールアミン/メタネフリン（褐色細胞腫）。副腎摘出術。"
)}

ENRICHMENTS["dog_canine_hemotropic_mycoplasmosis"] = {"diagnosis_ja": (
    "血液PCRでMycoplasma haemocanisを検出（ゴールドスタンダード）。"
    "血液塗抹で赤血球表面の小さな好塩基性の球状体を確認（感度低い: 30-50%）。"
    "CBC/血液塗抹で再生性溶血性貧血（PCV低下、網赤血球増加、球状赤血球）。クームス試験陽性の場合あり。"
    "脾摘後犬・免疫抑制犬で臨床発症リスク上昇。ダニ媒介感染。ドキシサイクリンが治療。"
)}

ENRICHMENTS["dog_fibrotic_myopathy"] = {"diagnosis_ja": (
    "触診で罹患筋の索状硬化・短縮を確認。関節可動域の制限（ROM制限）を定量化。"
    "超音波で筋組織のエコー輝度上昇・線維化パターンを確認。MRIでT1低信号/T2低信号の線維化。"
    "筋生検で結合組織の増生と筋線維の変性・萎縮を確認。CK値は概ね正常。"
    "薄筋・半腱様筋（ジャーマン・シェパード）、大腿四頭筋、棘下筋に好発。反復性損傷/虚血が原因。"
)}

ENRICHMENTS["dog_oronasal_fistula"] = {"diagnosis_ja": (
    "口腔検査で歯周ポケットから鼻腔への交通を確認。歯周プローブで瘻孔を探索。"
    "歯科X線で上顎犬歯/切歯部の歯槽骨溶解と口蓋骨の欠損を確認。"
    "鼻腔からの食物・液体の逆流、慢性片側性膿性鼻汁が臨床症状。"
    "CT三次元再構成で瘻孔のサイズと骨欠損を評価。原因歯の抜歯+粘膜フラップによる瘻孔閉鎖。"
)}

ENRICHMENTS["dog_hypertensive_retinopathy"] = {"diagnosis_ja": (
    "眼底検査で網膜出血、網膜剥離、網膜浮腫、網膜血管の蛇行/狭小化を確認。"
    "血圧測定（ドプラ法/HDO）で全身性高血圧（収縮期>160 mmHg、重度>180 mmHg）を確認。"
    "基礎疾患の精査: CKD（BUN/Cre/SDMA）、副腎腫瘍（ACTH刺激）、褐色細胞腫、甲状腺機能亢進症。"
    "尿検査で蛋白尿（UPC）。OCT（光干渉断層計）で網膜層の評価。降圧療法で視力回復の可能性。"
)}

ENRICHMENTS["dog_chronic_otitis_media"] = {"diagnosis_ja": (
    "CT/MRIで鼓室胞内の軟部組織密度/液体貯留を確認。鼓室胞壁の肥厚・硬化を評価。"
    "耳鏡検査で鼓膜の膨隆・穿孔・変色を確認。ビデオ耳鏡でより詳細な観察。"
    "鼓室胞穿刺/洗浄で内容物を回収→細菌培養+感受性試験（嫌気性菌含む）。細胞診。"
    "神経学的検査でホーナー症候群、顔面神経麻痺、前庭徴候を評価。外耳炎の慢性化が主因。"
)}

ENRICHMENTS["dog_inner_ear_infection_otitis_interna"] = {"diagnosis_ja": (
    "神経学的検査で末梢性前庭徴候（斜頸、眼振、運動失調、転倒）を確認。中枢性との鑑別。"
    "CT/MRIで鼓室胞・内耳の軟部組織密度を確認。内耳のT2高信号（炎症/膿瘍）。"
    "耳鏡で鼓膜穿孔を確認。中耳洗浄液の細菌培養+感受性試験。"
    "BAER（脳幹聴覚誘発反応）で聴覚障害を定量化。CBC/CRPで炎症を評価。中耳炎からの進展が最多原因。"
)}

ENRICHMENTS["dog_acanthomatous_ameloblastoma"] = {"diagnosis_ja": (
    "口腔内検査で歯肉の浸潤性腫瘤を確認。歯のずれ・動揺を伴う。"
    "歯科X線/CT三次元再構成で骨溶解の範囲を評価。「soap bubble」様の骨透亮パターンが特徴的。"
    "生検で棘細胞型のエナメル上皮腫を確認。核分裂像は少ない（良性だが局所浸潤性）。"
    "遠隔転移は極めて稀だが、骨浸潤により広範切除（下顎/上顎部分切除）が必要。放射線療法も有効。"
)}

ENRICHMENTS["dog_tracheal_perforation"] = {"diagnosis_ja": (
    "頸部X線で皮下気腫・縦隔気腫・気胸を確認。気管ルーメンの不連続性。"
    "気管支鏡で穿孔部位を直接確認。穿孔サイズ・位置・気管壁の状態を評価。"
    "CT三次元再構成で穿孔の範囲と周囲組織の損傷を評価。縦隔膿瘍の合併を検索。"
    "原因: 外傷性（咬傷、過度の気管チューブカフ圧）、医原性（気管内挿管、生検）。緊急外科的修復。"
)}

ENRICHMENTS["dog_masticatory_myositis_acute"] = {"diagnosis_ja": (
    "血清2M線維抗体（抗type 2M myosin抗体）検査陽性が確定診断。ELISA法で測定。"
    "身体検査で咀嚼筋（側頭筋、咬筋）の急性腫脹・疼痛・開口障害を確認。"
    "CK値著増（急性期）。CBC/CRPで白血球増多・炎症マーカー上昇。"
    "筋生検で2M線維に対するリンパ球性浸潤・壊死を確認。MRIで筋肉のT2高信号。慢性期は筋萎縮・線維化。"
)}

ENRICHMENTS["dog_polymyositis"] = {"diagnosis_ja": (
    "CK/AST著増。EMGで異常自発電位（線維自発電位、陽性鋭波、複合反復放電）を検出。"
    "筋生検で多発性のリンパ球性/形質細胞性筋炎を確認。壊死・再生像。"
    "MRIで罹患筋のT2高信号（浮腫/炎症）を確認。多部位のサンプリングが重要。"
    "ANA/抗核抗体で全身性自己免疫疾患との関連を評価。SLE、重症筋無力症の合併を除外。"
)}

ENRICHMENTS["dog_polyradiculoneuritis_coonhound_paralysis"] = {"diagnosis_ja": (
    "神経学的検査で急性上行性LMN不全麻痺を確認。後肢から始まり前肢・呼吸筋へ進行。"
    "EMGで脱神経電位。神経伝導速度検査で運動神経伝導速度低下（脱髄型）。"
    "CSF検査でアルブミノ細胞学的解離（蛋白上昇、細胞数正常）。"
    "アライグマ咬傷/接触歴の確認（北米）。GBSに相当。脊髄反射低下～消失。支持療法で2-6週で回復。"
)}

ENRICHMENTS["dog_central_diabetes_insipidus"] = {"diagnosis_ja": (
    "尿検査で低比重尿（USG<1.005）を確認。多飲多尿（PU/PD: 飲水量>100 mL/kg/日）。"
    "水制限試験で尿の濃縮不能。DDAVP（デスモプレシン）反応試験: 中枢性では尿比重上昇（>1.015）。"
    "腎性尿崩症との鑑別: DDAVP無反応=腎性、反応あり=中枢性。"
    "頭部MRI/CTで下垂体・視床下部の腫瘤/外傷/炎症を評価。血漿浸透圧/尿浸透圧比を測定。"
)}

ENRICHMENTS["dog_nephrogenic_diabetes_insipidus"] = {"diagnosis_ja": (
    "尿検査で低比重尿（USG<1.005）を確認。水制限試験で尿濃縮不能。"
    "DDAVP反応試験: 腎性では尿比重の上昇なし（ADH受容体/AQP2の異常）。"
    "血液検査で高Ca血症、低K血症、肝不全等の二次性原因を精査。"
    "腎臓超音波で腎髄質のウォッシュアウト（慢性PU/PD）を評価。先天性は極めて稀。二次性が圧倒的多数。"
)}

ENRICHMENTS["dog_cervical_spondylomyelopathy_wobbler_-_disc_associated"] = {"diagnosis_ja": (
    "MRIで頸部椎間板の突出/脱出と脊髄圧迫を確認。T2高信号の脊髄病変（脊髄浮腫/軟化）。"
    "頸部X線で椎間板腔の狭小化、椎体の変形を確認。ストレスビュー（屈曲/伸展）で動的圧迫。"
    "脊髄造影+CT myelographyで圧迫部位の三次元評価。CSF検査で感染・炎症を除外。"
    "ドーベルマン、グレート・デーン等の大型犬。後肢不全麻痺+頸部疼痛。保存療法or外科的減圧固定。"
)}

ENRICHMENTS["dog_discospondylitis"] = {"diagnosis_ja": (
    "X線で椎体終板の不整・溶解と椎間板腔の狭小化を確認。反応性の骨硬化像。"
    "MRIで椎体のT1低信号/T2高信号、椎間板の造影増強を確認。脊髄圧迫の有無。"
    "血液培養+尿培養で起炎菌を同定（Staphylococcus 多い）。CBC/CRPで炎症マーカー上昇。"
    "心エコーで心内膜炎（感染源）を除外。椎体生検/吸引培養で確定。長期抗生剤療法（6-12ヶ月）。"
)}

ENRICHMENTS["dog_atlantoaxial_subluxation"] = {"diagnosis_ja": (
    "頸部X線（ラテラル）で環椎-軸椎間の間隙拡大と歯突起の欠如/低形成を確認。"
    "CT三次元再構成で歯突起の形態異常と環椎の位置関係を評価。"
    "MRIで脊髄圧迫と脊髄病変（T2高信号）を確認。CSFは通常正常。"
    "小型犬（ヨークシャー・テリア、チワワ、トイプードル）に好発。先天性。頸部疼痛+四肢不全麻痺。外科的固定。"
)}

ENRICHMENTS["dog_cutaneous_lymphoma_epitheliotropic"] = {"diagnosis_ja": (
    "皮膚生検で表皮向性のT細胞リンパ腫を確認（Pautrier微小膿瘍が特徴的）。"
    "免疫組織化学でCD3+/CD8+のT細胞表現型を確認。クローナリティ解析（PCR for TCRG）。"
    "臨床ステージング: 紅皮症（erythroderma）→プラーク→腫瘤→脱色素/潰瘍への進行パターン。"
    "CBC/生化学/リンパ節FNAで全身性リンパ腫への進展を評価。菌状息肉症（MF）=最多型。"
)}

ENRICHMENTS["dog_digital_squamous_cell_carcinoma"] = {"diagnosis_ja": (
    "患肢X線で指骨の骨溶解を確認。FNA/生検で扁平上皮癌細胞を確認。"
    "胸部X線/CTで肺転移スクリーニング。所属リンパ節のFNAで転移を評価。"
    "CBC/生化学は概ね正常。同一犬での多指再発リスクを確認。"
    "黒色被毛の大型犬（ジャイアント・シュナウザー、スタンダード・プードル、ラブラドール）に好発。指切断が第一選択。"
)}

ENRICHMENTS["dog_gastric_polyps"] = {"diagnosis_ja": (
    "内視鏡で胃粘膜の有茎性/広基性ポリープを直接確認。生検で過形成性/炎症性/腺腫性を鑑別。"
    "X線造影検査で充満欠損を確認。超音波で胃壁の限局性肥厚を評価。"
    "CBC/生化学は概ね正常。便潜血で慢性出血を評価。"
    "悪性転化リスクは腺腫性で最も高い。過形成性は最多で予後良好。内視鏡的ポリペクトミーで摘出。"
)}

ENRICHMENTS["dog_megacolon_acquired"] = {"diagnosis_ja": (
    "腹部X線で著明な結腸拡張と便塊貯留を確認。直腸触診で便塊の硬度・量を評価。"
    "腹部超音波で結腸壁肥厚と拡張を確認。バリウム注腸で結腸運動の低下を評価。"
    "直腸生検で神経節細胞の有無を確認（先天性メガコロン/Hirschsprung 除外）。"
    "CBC/生化学で電解質異常（低K⁺）、甲状腺機能低下症を除外。骨盤狭窄（外傷後）の有無をX線で確認。"
)}

ENRICHMENTS["dog_keratoacanthoma"] = {"diagnosis_ja": (
    "身体検査で皮膚の角化性結節（中央に角栓を有するクレーター状）を確認。急速増大。"
    "FNA/生検で高分化型扁平上皮の増殖と中央の角化物質を確認。"
    "SCCとの鑑別が重要: KAは辺縁が明瞭で底部に浸潤性成長を欠く。病理でエラスチン層を評価。"
    "ジャーマン・シェパード、ケシュホンドに好発。ノルウェジアン・エルクハウンドでは多発性。外科切除で根治。"
)}

ENRICHMENTS["dog_apocrine_gland_adenocarcinoma"] = {"diagnosis_ja": (
    "身体検査で皮膚/皮下の腫瘤を確認。FNAで上皮性腫瘍細胞を検出。"
    "病理組織検査でアポクリン腺由来の腺癌を確定。免疫組織化学でCK7/CK19陽性。"
    "所属リンパ節FNAで転移を評価。胸部X線/CTで肺転移スクリーニング。"
    "腹部超音波で遠隔転移を検索。肛門嚢型は高Ca血症を伴うことあり。広範切除+リンパ節郭清。"
)}

ENRICHMENTS["dog_cranial_cruciate_ligament_disease_partial_tear"] = {"diagnosis_ja": (
    "整形外科検査で前方引き出し試験（cranial drawer test）で軽度の不安定性を確認。"
    "脛骨圧迫試験（tibial compression test）陽性。完全断裂より微妙な陽性所見。"
    "X線で関節液貯留、脂肪パッドの変位を確認。MRIで靭帯の部分断裂・信号変化を確認。"
    "関節液検査で非感染性炎症（単核球優位、WBC<5,000/μL）。進行性で最終的に完全断裂に至ることが多い。"
)}

ENRICHMENTS["dog_septic_arthritis"] = {"diagnosis_ja": (
    "関節穿刺で混濁した関節液を回収。関節液分析: WBC>40,000/μL、好中球>90%、細菌検出。"
    "関節液の細菌培養+感受性試験（好気性+嫌気性）。血液培養で菌血症を評価。"
    "X線で関節周囲の軟部組織腫脹、関節腔拡大、進行例で骨溶解を確認。"
    "CBC/CRP/SAAで全身性炎症。原因: 血行性、外傷性、医原性（関節穿刺・手術後）。関節洗浄+長期抗生剤。"
)}

ENRICHMENTS["dog_bone_cyst_aneurysmal"] = {"diagnosis_ja": (
    "X線で骨幹端の膨隆性骨溶解と皮質菲薄化を確認。「soap bubble」様の多房性パターン。"
    "CT/MRIで嚢胞の範囲・液面形成（fluid-fluid level）を確認。造影MRIで固形成分を評価。"
    "超音波ガイド下FNA/生検で血性液と線維性組織を確認。巨細胞を含む。"
    "骨肉腫・線維肉腫等の悪性腫瘍との鑑別に生検が必須。掻爬+骨移植が治療。"
)}

ENRICHMENTS["dog_chronic_bronchitis"] = {"diagnosis_ja": (
    "胸部X線で気管支壁肥厚（doughnut sign/tram line sign）を確認。びまん性気管支間質パターン。"
    "BAL（気管支肺胞洗浄）で好中球・マクロファージ優位の細胞診。培養で感染を評価。"
    "気管支鏡で気管支粘膜の充血・浮腫・粘液過分泌を直接確認。気管支虚脱の合併を評価。"
    "動脈血ガスで低酸素血症。定義: 連続2ヶ月以上の咳（他の原因を除外）。小型犬中高齢に好発。"
)}

ENRICHMENTS["dog_bronchiectasis"] = {"diagnosis_ja": (
    "HRCT（高分解能CT）で気管支の不可逆的拡張（signet ring sign）を確認。"
    "胸部X線で気管支壁肥厚・拡張を確認（CTより感度低い）。BAL液の細菌培養。"
    "気管支鏡で拡張した気管支と粘液貯留を直接確認。BAL細胞診で好中球増多。"
    "慢性気管支炎、原発性線毛機能不全症、異物吸引後の続発として発生。コッカー・スパニエルに好発。"
)}

ENRICHMENTS["dog_myxomatous_mitral_valve_degeneration_early_stage"] = {"diagnosis_ja": (
    "聴診で左心尖部の収縮期雑音（grade I-III/VI）を検出。心エコーで僧帽弁の軽度肥厚を確認。"
    "カラードプラで軽度の僧帽弁逆流。左房・左室サイズは正常範囲内（ACVIM stage B1）。"
    "X線で心臓サイズ正常（VHS正常範囲）。NT-proBNP正常～軽度上昇。"
    "小型犬中高齢に好発（キャバリア、ダックスフンド、マルチーズ）。EPIC試験に基づきB2でピモベンダン開始。"
)}

ENRICHMENTS["dog_canine_brucellosis_reproductive"] = {"diagnosis_ja": (
    "血清学的検査: RSAT（迅速スライド凝集試験）でスクリーニング。偽陽性あり→AGID/TAT/iELISAで確認。"
    "血液培養でBrucella canisを分離（確定診断だが感度60-70%）。PCRで検出。"
    "精液検査で精子形態異常・炎症細胞を確認。雄: 精巣上体炎・精巣萎縮。雌: 後期流産（45-55日）。"
    "全身臓器へのスクリーニング: 脊椎X線（椎間板脊椎炎）、眼科検査（前部ぶどう膜炎）。人獣共通感染症。"
)}

ENRICHMENTS["dog_pituitary_dwarfism"] = {"diagnosis_ja": (
    "血清IGF-1（インスリン様成長因子）低値が最も信頼性の高いスクリーニング。"
    "GH刺激試験（GHRH/クロニジン投与後のGH測定）で反応低値を確認。"
    "頭部MRI/CTで下垂体嚢胞（Rathke嚢胞）・下垂体低形成を確認。"
    "甲状腺機能検査（T4低値: 二次性甲状腺機能低下症）。ジャーマン・シェパードに好発。遺伝子検査（LHX3変異）。"
)}

ENRICHMENTS["dog_canine_familial_nephropathy"] = {"diagnosis_ja": (
    "若齢（数ヶ月～3歳）でのBUN/Cre上昇で腎不全を確認。SDMA上昇は早期検出に有用。"
    "尿検査で低比重尿・蛋白尿。UPC>0.5で蛋白漏出。腎臓超音波で小型・不整な腎臓を確認。"
    "腎生検で犬種特異的な組織学的パターンを確認。電子顕微鏡でGBM（糸球体基底膜）異常を評価。"
    "遺伝子検査（犬種特異的変異: COL4A3/A4/A5等）。英国コッカー・スパニエル、ブル・テリア等に好発。"
)}

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
