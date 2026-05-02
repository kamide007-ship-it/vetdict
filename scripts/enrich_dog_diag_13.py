#!/usr/bin/env python3
import json
import os
import time

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diseases_all_species.json")

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_cholangitis_cholangiohepatitis"] = {"diagnosis_ja": (
    "血液検査でALP/GGT/ALT/TBil上昇（胆汁うっ滞パターン）。腹部超音波で胆管拡張・胆嚢壁肥厚を確認。"
    "超音波ガイド下FNA/肝生検で胆管周囲の炎症性浸潤を確認。培養で細菌性を評価。"
    "CBC/CRPで炎症マーカーを評価。凝固検査でPT延長（肝不全進行）。"
    "膵炎（cPLI）、IBD（内視鏡生検）との合併（triaditis）を精査。胆石/胆泥の有無を超音波で確認。"
)}

ENRICHMENTS["dog_chronic_hepatitis"] = {"diagnosis_ja": (
    "血液検査でALT持続上昇（>3ヶ月）、ALP/GGT上昇。低アルブミン血症・BUN低値は肝合成能低下を示す。"
    "超音波ガイド下肝生検（Tru-cut）で門脈周囲の炎症・線維化・肝硬変を評価（確定診断に必須）。"
    "腹部超音波で肝臓のサイズ・エコー輝度・辺縁不整を確認。腹水・門脈高血圧の有無。"
    "銅定量（肝生検）でCSH（銅蓄積性肝症）を鑑別。食前後胆汁酸上昇。コッカー・スパニエル等に好発。"
)}

ENRICHMENTS["dog_hepatic_lipidosis"] = {"diagnosis_ja": (
    "血液検査でALP/ALT/GGT上昇、高コレステロール血症、高トリグリセリド血症を確認。"
    "腹部超音波で肝臓のびまん性高エコー化（diffuse hyperechogenicity）を確認。"
    "超音波ガイド下FNA/生検で肝細胞内の脂肪空胞沈着を確認（Oil Red O染色）。"
    "基礎疾患の精査: 糖尿病、クッシング、甲状腺機能低下症、膵炎。体重減少歴・食欲不振の確認。"
)}

ENRICHMENTS["dog_small_intestinal_bacterial_overgrowth_sibo"] = {"diagnosis_ja": (
    "十二指腸液培養で細菌数>10⁵ CFU/mLを確認（ゴールドスタンダードだが侵襲的）。"
    "血清コバラミン低値（B12吸収障害）、葉酸上昇（細菌産生）のパターンが示唆的。"
    "cTLI正常でEPI除外。血清コバラミン/葉酸比の逆転。内視鏡+十二指腸生検でIBDを除外。"
    "慢性下痢・体重減少・ガス貯留の臨床症状。抗生剤（メトロニダゾール/チロシン）反応性で支持的診断。"
)}

ENRICHMENTS["dog_antibiotic-responsive_diarrhea"] = {"diagnosis_ja": (
    "抗生剤（チロシン25 mg/kg BID or メトロニダゾール15 mg/kg BID）への反応性で診断。"
    "血清コバラミン低値、葉酸上昇のパターン。cTLI正常（EPI除外）。"
    "内視鏡+腸生検でIBD・リンパ腫との鑑別。糞便培養でClostridium等の過増殖を評価。"
    "食事療法無効後に試験的抗生剤投与。再発性のため長期管理が必要な場合あり。ジャーマン・シェパードに好発。"
)}

ENRICHMENTS["dog_lymphangiectasia"] = {"diagnosis_ja": (
    "血液検査で低アルブミン血症（<2.0 g/dL）、低グロブリン血症、低コレステロール血症、リンパ球減少症。"
    "内視鏡生検で十二指腸/空腸絨毛内のリンパ管拡張（乳糜槽の拡張）を確認。全層生検がより信頼性高い。"
    "腹部超音波で腸壁の高エコーストリエーション。腹水・胸水（低蛋白性漏出液）の合併。"
    "α1-PI（α1プロテアーゼ阻害因子）クリアランス上昇はPLEの証拠。ヨークシャー・テリアに好発。"
)}

ENRICHMENTS["dog_esophageal_stricture"] = {"diagnosis_ja": (
    "X線造影検査（バリウム嚥下）で食道の限局性狭窄と造影剤の停滞を確認。"
    "内視鏡で狭窄部位の直接観察と重症度評価。生検で悪性腫瘍を除外。"
    "透視下で嚥下動態を評価。胸部X線で吸引性肺炎の合併を確認。"
    "原因: 全身麻酔後の胃食道逆流（最多）、異物、腐食剤、食道炎。バルーン拡張術が治療。"
)}

ENRICHMENTS["dog_gastroesophageal_reflux_disease_gerd"] = {"diagnosis_ja": (
    "内視鏡で食道粘膜のびらん・潰瘍・紅斑を確認。食道下部括約筋の弛緩を評価。"
    "食道pHモニタリングで酸逆流エピソードを定量化（犬では限定的）。"
    "X線造影で食道ヘルニア・逆流を確認。胸部X線で吸引性肺炎を除外。"
    "嘔吐・吐出・嚥下困難・流涎の臨床症状。全身麻酔後に悪化。PPI/H2ブロッカー+消化管運動促進薬。"
)}

ENRICHMENTS["dog_pulmonary_thromboembolism_pte"] = {"diagnosis_ja": (
    "CT肺動脈造影（CTPA）で肺動脈内の充満欠損を確認（ゴールドスタンダード）。"
    "動脈血ガスで低酸素血症（PaO₂<80 mmHg）、A-aDO₂勾配上昇。D-ダイマー上昇（感度高いが特異度低い）。"
    "胸部X線で楔状陰影（非特異的）、肺血管減少、右心拡大を評価。心エコーで右心負荷所見。"
    "基礎疾患: IMHA、クッシング、腎症、DIC、敗血症、腫瘍。凝固検査でAT III低下。抗凝固療法開始。"
)}

ENRICHMENTS["dog_eosinophilic_bronchopneumopathy"] = {"diagnosis_ja": (
    "BAL（気管支肺胞洗浄）で好酸球優位の細胞診（>20%が好酸球）を確認。"
    "胸部X線でびまん性の気管支間質パターン。CT/HRCTで気管支壁肥厚・気管支拡張を評価。"
    "CBC/血液塗抹で末梢血好酸球増加。糞便検査で肺虫・回虫幼虫移行を除外（Baermann法）。"
    "フィラリア抗原検査で犬糸状虫症を除外。IgE上昇。プレドニゾロン反応性で支持的診断。"
)}

ENRICHMENTS["dog_lung_lobe_consolidation"] = {"diagnosis_ja": (
    "胸部X線で肺葉の均一な軟部組織濃度（air bronchogram陽性）を確認。"
    "CTで硬化肺葉の範囲・気管支内異物・腫瘤を三次元評価。BAL/経気管吸引で細菌培養+感受性。"
    "細胞診で感染性/腫瘍性/炎症性を鑑別。CBC/CRPで全身性炎症反応を評価。"
    "原因: 吸引性肺炎（最多）、細菌性肺炎、肺葉捻転、腫瘍。抗生剤療法or肺葉切除。"
)}

ENRICHMENTS["dog_nasopharyngeal_polyp"] = {"diagnosis_ja": (
    "口腔内検査で軟口蓋後方に突出するポリープを直接確認。後鼻鏡検査で鼻咽頭内の腫瘤を視覚化。"
    "CT/MRIで鼓室胞内の軟部組織密度を確認（中耳原発の場合）。耳鏡検査で鼓膜の膨隆。"
    "生検で炎症性ポリープ（良性）を確認。悪性腫瘍との鑑別に病理。"
    "鼻閉、ストライダー、嚥下困難、中耳炎の症状。猫に多いが犬でも発生。牽引摘出+鼓室胞切開。"
)}

ENRICHMENTS["dog_allergic_rhinitis"] = {"diagnosis_ja": (
    "臨床症状（漿液性鼻汁、くしゃみ、鼻鏡の色素脱失）と季節性から臨床診断。"
    "鼻腔内視鏡で粘膜の浮腫・充血を確認。鼻腔ラベージの細胞診で好酸球優位。"
    "CT/MRIで鼻腔内腫瘍・アスペルギルス症を除外。鼻腔X線で骨溶解の有無を確認。"
    "アレルゲン特異的IgE血清検査/皮内テストで原因アレルゲンを同定。アトピー性皮膚炎の合併を評価。"
)}

ENRICHMENTS["dog_tracheal_foreign_body"] = {"diagnosis_ja": (
    "X線（頸部/胸部ラテラル）で気管内の異物を確認。透視で呼吸時の動きを評価。"
    "気管支鏡で異物の直接確認と位置・性状の評価。同時に内視鏡的摘出を試みる。"
    "CT三次元再構成で異物の正確な位置と気管壁損傷を評価。"
    "急性の咳・喘鳴・チアノーゼの臨床症状。胸部X線で続発性肺炎・無気肺を確認。緊急気管支鏡的摘出。"
)}

ENRICHMENTS["dog_renal_dysplasia"] = {"diagnosis_ja": (
    "血液検査でBUN/Cre上昇（若齢での腎不全は本疾患を強く疑う）。SDMA上昇は早期腎障害指標。"
    "腹部超音波で腎臓の小型化・不整な辺縁・皮髄境界不明瞭を確認。"
    "腎生検で組織学的に胎児型腎構造（原始糸球体/尿細管）を確認（確定診断）。"
    "尿検査で低比重尿（等張尿）、蛋白尿。ラサ・アプソ、シー・ズー、コッカー・スパニエルに好発。先天性。"
)}

ENRICHMENTS["dog_renal_amyloidosis"] = {"diagnosis_ja": (
    "腎生検でアミロイド沈着を確認（コンゴーレッド染色→偏光顕微鏡でapple-green birefringence）。"
    "尿検査でネフローゼ症候群（著明な蛋白尿>3+ UPC>3.5）。血液検査で低アルブミン血症、高コレステロール。"
    "BUN/Cre上昇（進行性CKD）。腹部超音波で腎臓のエコー輝度上昇。"
    "シャーペイ（家族性アミロイドーシス+シャーペイ熱）に好発。基礎疾患（慢性感染/腫瘍）の精査。"
)}

ENRICHMENTS["dog_nephrolithiasis_kidney_stones"] = {"diagnosis_ja": (
    "腹部X線で腎盂/尿管内の放射線不透過性結石を確認（ストルバイト、シュウ酸Ca）。"
    "腹部超音波で腎盂拡張と結石エコー（音響陰影付き高エコー構造）を確認。水腎症の合併を評価。"
    "尿検査で結晶尿、血尿、尿培養で感染性結石を評価。尿pH・比重を測定。"
    "血液検査でBUN/Cre、Ca、P、PTHを評価。CT/IVPで尿管閉塞の有無。結石分析で成分同定。"
)}

ENRICHMENTS["dog_urethral_prolapse"] = {"diagnosis_ja": (
    "身体検査で包皮先端からの赤色～暗赤色の粘膜突出を確認。浮腫・壊死の有無を評価。"
    "尿道カテーテル挿入で尿道の開存性を確認。尿検査で血尿・感染を評価。"
    "超音波で前立腺・膀胱の異常を除外。CBC/生化学は概ね正常。"
    "英国ブルドッグ、ボストン・テリア等の短頭種の若齢未去勢雄に好発。性的興奮時に発生。外科的切除（amputation）。"
)}

ENRICHMENTS["dog_uterine_stump_pyometra"] = {"diagnosis_ja": (
    "腹部超音波でOVH術後の子宮断端部の液体貯留と壁肥厚を確認。膿瘍形成の有無。"
    "CBC/CRPで白血球増多、左方移動、炎症マーカー上昇。生化学で腎機能・電解質を評価。"
    "X線で腹腔内腫瘤影を確認。CT/造影CTで断端膿瘍の範囲を評価。"
    "避妊手術歴にもかかわらず発情兆候（残存卵巣組織）。再手術での断端切除+ドレナージが治療。"
)}

ENRICHMENTS["dog_testicular_torsion"] = {"diagnosis_ja": (
    "身体検査で急性の精巣腫大・疼痛を確認。陰嚢の発赤・浮腫。腹腔内精巣では急性腹症を呈する。"
    "超音波（カラードプラ）で精巣内血流の減少～消失を確認。対側精巣との比較。"
    "CBC/生化学で炎症マーカーを評価。停留精巣（腹腔内/鼠径部）での発生リスクが高い。"
    "精巣腫瘍（セルトリ細胞腫、精上皮腫）の合併・鑑別。緊急精巣摘出（去勢）が治療。"
)}

ENRICHMENTS["dog_penile_preputial_tumor"] = {"diagnosis_ja": (
    "身体検査で包皮/陰茎からの腫瘤、出血、排尿障害を確認。腫瘤の可動性・浸潤を触診。"
    "FNA/生検で腫瘍型を確定（TVT、SCC、乳頭腫、線維肉腫が多い）。"
    "TVT: 特徴的な円形細胞の細胞診。ビンクリスチン化学療法に高反応。"
    "X線/CTで鼠径リンパ節転移・肺転移を評価。尿道の閉塞・圧排を尿道造影で評価。"
)}

ENRICHMENTS["dog_fear_aggression"] = {"diagnosis_ja": (
    "行動診察で恐怖誘発刺激への攻撃行動パターンを評価。ボディランゲージ（耳後方、尾下垂、体重後方移動）。"
    "身体検査・神経学的検査で疼痛性疾患・甲状腺機能低下症を除外。CBC/T4/fT4を測定。"
    "行動歴の詳細聴取: 誘発要因、標的、頻度、重症度をスコアリング。咬傷歴の確認。"
    "認知機能検査で学習障害の有無を評価。脳MRIは器質的疾患疑い時のみ。行動修正+薬物療法。"
)}

ENRICHMENTS["dog_resource_guarding"] = {"diagnosis_ja": (
    "行動診察で資源（食物、おもちゃ、場所、人）防衛時の攻撃行動を体系的に評価。"
    "誘発テスト（模擬手を使用）で防衛行動の閾値と重症度をスコアリング。"
    "身体検査で疼痛性疾患を除外。CBC/生化学/甲状腺機能で医学的原因を除外。"
    "行動歴: 発症年齢、頻度、エスカレーションパターン、咬傷歴。脱感作+拮抗条件付けが治療の中心。"
)}

ENRICHMENTS["dog_storm_noise_anxiety"] = {"diagnosis_ja": (
    "行動診察で雷・騒音（花火等）に対する恐怖反応を評価。パニック、逃走、破壊行動、流涎。"
    "聴覚検査（BAER）で聴覚過敏/難聴を除外。甲状腺機能検査で内分泌性を評価。"
    "身体検査で疼痛・神経学的異常を除外。併存不安障害（分離不安、全般性不安）の評価。"
    "気圧変化・静電気への感受性も関与。トラゾドン/アルプラゾラム＋環境管理＋脱感作プログラム。"
)}

ENRICHMENTS["dog_canine_fly-snapping_syndrome"] = {"diagnosis_ja": (
    "神経学的検査で空中を噛む反復行動を確認。局所てんかんとの鑑別が最重要。"
    "脳MRIで構造的病変（Chiari様奇形、脳腫瘍）を除外。EEGでてんかん性放電を評価。"
    "眼科検査で硝子体浮遊物（muscae volitantes）を除外。消化器検査でGERDを除外。"
    "ビデオ撮影で行動の詳細パターンを分析。CKCS/キャバリアでCM/SMとの関連。抗てんかん薬or行動薬。"
)}

ENRICHMENTS["dog_territorial_aggression"] = {"diagnosis_ja": (
    "行動診察で特定の場所（自宅、車、庭）への侵入者に対する攻撃行動パターンを評価。"
    "身体検査・神経学的検査で疼痛性疾患を除外。CBC/生化学/甲状腺で内科的原因を除外。"
    "行動歴: 防衛範囲、標的（見知らぬ人/動物）、頻度、エスカレーション。郵便配達員パターン。"
    "恐怖性攻撃行動との鑑別（ボディランゲージが異なる）。環境管理+脱感作+拮抗条件付けが治療。"
)}

ENRICHMENTS["dog_hyperkinesis_canine_adhd"] = {"diagnosis_ja": (
    "行動診察で持続的な過活動、注意散漫、衝動性を評価。通常の運動では軽減しない活動レベル。"
    "メチルフェニデート診断的投与試験（0.2-1.0 mg/kg PO）: 真の過活動症では逆説的に鎮静。"
    "心拍数モニタリング: メチルフェニデート投与後に心拍低下=真の過活動症を支持。"
    "甲状腺機能亢進症、疼痛、不安障害を除外。運動不足・環境刺激不足との鑑別。犬種素因を確認。"
)}

ENRICHMENTS["dog_canine_adenovirus_type_1_cav-1"] = {"diagnosis_ja": (
    "血清学的検査でCAV-1抗体価上昇（ペア血清で4倍以上）。PCRで血液/肝組織からウイルスDNA検出。"
    "血液検査でALT/AST著増（急性肝壊死）、白血球減少→増多。凝固検査でDIC（PT/APTT延長）。"
    "腹部超音波で肝腫大・エコー輝度変化。眼科検査で「blue eye」（角膜浮腫: 回復期に20%で発生）。"
    "ワクチン未接種の若齢犬に急性肝炎。剖検で肝細胞内のintranuclear inclusion bodyが特徴的。"
)}

ENRICHMENTS["dog_canine_parainfluenza_virus"] = {"diagnosis_ja": (
    "鼻腔/咽頭スワブからのRT-PCRでCPIVを検出。ペア血清でHI抗体価の4倍以上上昇。"
    "ウイルス分離培養（Vero/MDCK細胞）。鼻汁の蛍光抗体法（DFA）。"
    "胸部X線で気管支間質パターン（二次性細菌感染時はびまん性肺野浸潤）を確認。"
    "ケンネルカフ複合体の一成分。Bordetella bronchisepticaとの混合感染が多い。集団飼育歴の確認。"
)}

ENRICHMENTS["dog_canine_respiratory_coronavirus"] = {"diagnosis_ja": (
    "鼻腔/咽頭スワブからのRT-PCRでCRCoV（グループ2コロナウイルス）を検出。"
    "血清学的検査で抗体価上昇。ウイルス分離はHRT-18G細胞を使用。"
    "胸部X線で軽度の気管支間質パターン。CBC/生化学は概ね正常（軽度白血球増多）。"
    "ケンネルカフ複合体の一成分。CPIV、Bordetella、マイコプラズマとの混合感染を評価。集団飼育歴。"
)}

ENRICHMENTS["dog_streptococcal_toxic_shock_syndrome"] = {"diagnosis_ja": (
    "血液培養で溶血性レンサ球菌（Group A/G Streptococcus）を検出。CBC/CRPで重度炎症反応。"
    "生化学で多臓器不全の指標: BUN/Cre上昇（腎）、ALT/AST上昇（肝）、低アルブミン血症。"
    "凝固検査でDIC（PT/APTT延長、FDP上昇、血小板低下）。血液ガスで代謝性アシドーシス。"
    "壊死性筋膜炎の合併: 筋膜の腫脹・壊死（MRI/CT/外科的探索で確認）。緊急デブリドマン+集中治療。"
)}

ENRICHMENTS["dog_pythiosis"] = {"diagnosis_ja": (
    "病変部の生検/FNAで広い幅の非隔壁菌糸（GMS/PAS染色: 菌糸幅2-7μm）を確認。"
    "ELISA血清検査で抗Pythium insidiosum抗体を検出（感度/特異度90%以上）。"
    "培養でPythium insidiosumを分離（特殊培地: corn meal agar）。PCRで同定。"
    "腹部超音波/内視鏡で消化管型の腸壁肥厚を確認。皮膚型は潰瘍性の肉芽腫性病変。南部の温暖な水域。"
)}

ENRICHMENTS["dog_protothecosis"] = {"diagnosis_ja": (
    "病変部の生検/FNAで特徴的なmorula（内生胞子を含む球形体: 8-25μm）を確認。"
    "GMS/PAS染色で藻類を同定。培養でPrototheca wickerhamii/zopfiiを分離。"
    "CSF検査で細胞数増多（CNS型）。眼科検査で網膜炎・失明（眼型）を確認。"
    "血便・慢性下痢（消化管型）。播種性感染では多臓器病変。犬の予後は不良。コリーに好発。"
)}

ENRICHMENTS["dog_hepatic_abscess"] = {"diagnosis_ja": (
    "腹部超音波で肝臓内の低エコー/混合エコーの嚢胞性病変を確認。壁の不整・ガスエコーが膿瘍を示唆。"
    "超音波ガイド下穿刺で膿を吸引→細菌培養+感受性試験。嫌気性菌の培養も必須。"
    "CBC/CRPで白血球増多（左方移動）、CRP著増。生化学でALP/ALT上昇、低アルブミン血症。"
    "血液培養で菌血症を評価。CT/造影CTで膿瘍の範囲・多発性を確認。胆管炎・門脈炎からの波及が多い。"
)}

ENRICHMENTS["dog_splenic_torsion"] = {"diagnosis_ja": (
    "腹部超音波で脾臓の著明な腫大と実質のエコー輝度低下を確認。脾門部血管のドプラ信号減少～消失。"
    "腹部X線で左腹腔内の巨大な軟部組織腫瘤影。腹腔液（血性）の穿刺。"
    "CBC/生化学で溶血性貧血、血小板低下、凝固障害を評価。DICの合併を精査。"
    "急性腹症（嘔吐、腹痛、虚脱）。グレート・デーン等の大型犬に好発。胃捻転との合併を評価。緊急脾摘出。"
)}

ENRICHMENTS["dog_diaphragmatic_hernia"] = {"diagnosis_ja": (
    "胸部X線で心臓シルエットの消失・腹腔臓器の胸腔内描出を確認。ガス含有腸管ループの胸腔内影。"
    "造影X線で消化管の胸腔内逸脱を確認。超音波で肝臓・消化管の胸腔内存在を評価。"
    "動脈血ガスで低酸素血症・高CO₂血症。CBC/生化学で全身状態を評価。"
    "外傷性（最多）vs先天性（腹膜心膜横隔膜ヘルニア: PPDH）を鑑別。安定化後に外科的整復。"
)}

ENRICHMENTS["dog_perineal_hernia"] = {"diagnosis_ja": (
    "身体検査で会陰部の両側/片側の腫脹を確認。直腸触診でヘルニア輪と脱出臓器を評価。"
    "X線/造影X線で膀胱の会陰部逸脱（膀胱後方変位）を確認。前立腺の逸脱も評価。"
    "腹部超音波で膀胱・前立腺の位置を確認。排尿困難時は尿道カテーテルで排尿。"
    "CBC/生化学で全身状態を評価。未去勢高齢雄犬に好発。会陰ヘルニア整復術+去勢が治療。"
)}

ENRICHMENTS["dog_inguinal_hernia"] = {"diagnosis_ja": (
    "身体検査で鼠径部の軟性腫脹を確認。還納性/非還納性/嵌頓性を評価。"
    "腹部超音波で脱出臓器（子宮、腸管、膀胱、網嚢）を同定。嵌頓時の血流評価。"
    "X線で腸管ガスパターン（イレウス）の有無を確認。CBC/生化学で全身状態を評価。"
    "先天性（幼若犬）vs後天性（妊娠末期/肥満犬）を鑑別。嵌頓時は緊急手術。"
)}

ENRICHMENTS["dog_umbilical_hernia"] = {"diagnosis_ja": (
    "身体検査で臍部の軟性腫脹を確認。還納性・ヘルニア輪径を評価。"
    "腹部超音波で脱出臓器（網嚢、腸管）を確認。嵌頓の有無を評価。"
    "X線は通常不要（臨床診断で十分）。嵌頓疑い時はCBC/生化学で全身状態を評価。"
    "先天性が大部分。小型（<1-2 cm）は自然閉鎖の可能性。大型/嵌頓は外科的閉鎖。避妊手術時に同時閉鎖。"
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
