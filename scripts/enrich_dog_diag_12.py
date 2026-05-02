#!/usr/bin/env python3
import json
import os
import time

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diseases_all_species.json")

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_leiomyosarcoma_intestinal"] = {"diagnosis_ja": (
    "腹部超音波で腸管壁の筋層由来の低エコー腫瘤を確認。超音波ガイド下FNAで紡錘形細胞を検出。"
    "CT/造影CTで腫瘍の範囲・リンパ節転移・肝転移を評価。X線で肺転移スクリーニング。"
    "病理組織検査で平滑筋分化を確認（SMA陽性、desmin陽性、c-kit陰性でGISTと鑑別）。"
    "核分裂像数で悪性度判定。腸閉塞・穿孔・腹膜炎の合併を評価。外科的腸管切除が第一選択。"
)}

ENRICHMENTS["dog_multiple_myeloma"] = {"diagnosis_ja": (
    "血清蛋白電気泳動でM-spike（モノクローナルガンモパチー）を確認。多くはIgG/IgA産生。"
    "骨髄穿刺で形質細胞≧20%を確認。X線全身骨格調査で打ち抜き像（punched-out lesions）を検出。"
    "尿検査でベンス・ジョーンズ蛋白尿。CBC/生化学で貧血、高Ca血症、腎不全、高粘稠度症候群を評価。"
    "凝固検査（PT/APTT延長）で出血傾向を確認。確定は形質細胞腫瘍+M-spike+骨溶解の3要件。"
)}

ENRICHMENTS["dog_meningioma"] = {"diagnosis_ja": (
    "MRI（造影T1）で硬膜付着性の均一に強い造影増強腫瘤を確認。硬膜尾徴候（dural tail sign）が特徴的。"
    "T2で等～高信号。CT（造影）でも確認可能。頭蓋内圧亢進徴候（乳頭浮腫）を眼底検査で評価。"
    "CSF検査で蛋白上昇、軽度細胞数増多。CBC/生化学は概ね正常。"
    "犬では全脳腫瘍の約30%。ゴールデン・レトリーバー、ボクサーに好発。外科切除が根治療法。"
)}

ENRICHMENTS["dog_perianal_gland_adenocarcinoma"] = {"diagnosis_ja": (
    "直腸触診で肛門周囲の硬い腫瘤を確認。FNAで腺癌細胞を検出。"
    "腹部超音波/CTで腸骨下リンパ節転移を評価。胸部X線で肺転移スクリーニング。"
    "血液検査で高Ca血症（PTHrP産生腫瘍）の有無。イオン化Ca・PTH・PTHrPを測定。"
    "肛門腺腫（良性）との鑑別に病理。去勢犬・雌犬でも発生（ホルモン非依存性）。広範切除+化学療法。"
)}

ENRICHMENTS["dog_nasal_lymphoma"] = {"diagnosis_ja": (
    "CT/MRIで鼻腔内の軟部組織腫瘤と骨溶解を確認。篩板破壊・頭蓋内進展の有無を評価。"
    "鼻腔内生検/FNAでリンパ腫細胞を確認。フローサイトメトリーでT/B細胞型分類。"
    "全身ステージングにCBC、生化学、胸腹部画像、骨髄穿刺。LDH・カルシウムを評価。"
    "鼻出血・鼻汁・顔面変形の臨床症状。鼻腔癌（腺癌、SCC）との鑑別に病理。放射線療法が第一選択。"
)}

ENRICHMENTS["dog_splenic_hemangiosarcoma"] = {"diagnosis_ja": (
    "腹部超音波で脾臓の不均一エコー腫瘤（低エコー/高エコー混在、液体成分）を確認。腹腔内遊離液体。"
    "穿刺液がPCV>腹腔PCV（血腹）。胸部X線/CTで肺転移、心エコーで心臓HSA（右房腫瘤）を同時評価。"
    "CBC/凝固検査でDIC（FDP上昇、血小板低下、PT/APTT延長）を評価。生化学で肝転移を示唆する異常。"
    "ゴールデン・レトリーバー、ジャーマン・シェパードに好発。FNA/病理で確定。緊急脾摘+化学療法。"
)}

ENRICHMENTS["dog_cardiac_hemangiosarcoma"] = {"diagnosis_ja": (
    "心エコーで右房壁の不均一エコー腫瘤と心嚢液貯留を確認。右房虚脱で心タンポナーデ。"
    "心嚢穿刺で血性液を回収。PCV測定。液体細胞診は感度低い（腫瘍細胞検出率<30%）。"
    "胸部X線/CTで肺転移、腹部超音波で脾臓・肝臓の同時HSAを評価。"
    "CBC/凝固検査でDIC・貧血。トロポニンI上昇は心筋障害を示唆。ゴールデン・レトリーバーに好発。"
)}

ENRICHMENTS["dog_immune-mediated_neutropenia"] = {"diagnosis_ja": (
    "CBC/血液塗抹で好中球数著減（<1,000/μL）を確認。赤血球・血小板は正常（純粋好中球減少）。"
    "骨髄穿刺で骨髄球系の成熟停止（maturation arrest）を確認。巨核球・赤芽球系は正常。"
    "抗好中球抗体検査（感度限定的）。薬剤性（TMP-SMX等）の除外に薬歴確認。"
    "感染症（パルボ、エールリヒア、Hepatozoon）をPCR/血清学で除外。発熱・敗血症リスクの評価。"
)}

ENRICHMENTS["dog_bullous_pemphigoid"] = {"diagnosis_ja": (
    "皮膚生検で表皮下水疱（subepidermal vesicle）を確認。真皮表皮接合部のPAS染色で基底膜の解離。"
    "直接免疫蛍光法（DIF）で基底膜へのIgG/C3の線状沈着を確認。"
    "間接免疫蛍光法（IIF）で血清中の抗BP180抗体を検出。抗BP230抗体。"
    "口腔粘膜・皮膚の弛緩性水疱・びらん。ニコルスキー現象陽性。天疱瘡との鑑別に免疫蛍光法が必須。"
)}

ENRICHMENTS["dog_immune-mediated_meningitis"] = {"diagnosis_ja": (
    "CSF検査で好中球優位の細胞数増多と蛋白上昇を確認。CSF培養で細菌性を除外。"
    "MRIで髄膜の造影増強を確認。CRP/SAA著増。CBC/生化学で白血球増多。"
    "血清IgA上昇の有無を評価。SRMAとの鑑別に臨床経過とステロイド反応性を評価。"
    "発熱・頸部疼痛・頸部硬直の臨床症状。感染性髄膜炎を培養で除外後、免疫抑制療法を開始。"
)}

ENRICHMENTS["dog_vogt-koyanagi-harada-like_syndrome_vkh"] = {"diagnosis_ja": (
    "眼科検査で両側性の肉芽腫性汎ぶどう膜炎を確認。漿液性網膜剥離、前房フレア。"
    "皮膚検査で鼻鏡・口唇・眼瞼の色素脱失（poliosis/vitiligo）。毛色の白色化。"
    "皮膚生検で界面皮膚炎パターンとメラノサイトへのリンパ球浸潤。眼内生検で肉芽腫性炎症。"
    "秋田犬、サモエド、シベリアン・ハスキーに好発。CSF検査で単核球増多。早期積極的免疫抑制が視力保存に重要。"
)}

ENRICHMENTS["dog_cold_agglutinin_disease"] = {"diagnosis_ja": (
    "血液検査で再生性貧血（PCV低下、網赤血球増加）。クームス試験で4℃での凝集反応陽性。"
    "血液塗抹で赤血球自己凝集（EDTA抗凝固血でも残存）を確認。温めると消失。"
    "寒冷暴露後の耳介・尾端・四肢末端のチアノーゼ・壊死。末梢血管閉塞症状。"
    "基礎疾患（リンパ腫、マイコプラズマ感染）の精査。抗IgM型冷式自己抗体の確認。環境温管理+免疫抑制。"
)}

ENRICHMENTS["dog_macadamia_nut_toxicosis"] = {"diagnosis_ja": (
    "病歴聴取でマカダミアナッツの摂取を確認。摂取量を推定（中毒量: 2.4 g/kg以上）。"
    "身体検査で後肢不全麻痺・振戦・発熱（39.5-40.5℃）・腹痛を確認。"
    "CBC/生化学でCK上昇（筋障害）、白血球増多。凝固検査で異常なし。"
    "嘔吐・軟便の有無。通常12-48時間で自然回復。チョコレート同時摂取の場合はテオブロミン中毒も考慮。"
)}

ENRICHMENTS["dog_ibuprofen_toxicosis"] = {"diagnosis_ja": (
    "病歴聴取でイブプロフェン（NSAIDs）の誤食を確認。摂取量・時間を推定。"
    "中毒量: >25 mg/kgで消化管症状、>100 mg/kgで腎障害、>400 mg/kgでCNS症状。"
    "血液検査でBUN/Cre上昇（急性腎不全）、電解質異常。便潜血/吐血で消化管出血を確認。"
    "尿検査で尿沈渣（腎尿細管壊死）。内視鏡で胃潰瘍・穿孔を評価。催吐+活性炭+腎保護療法。"
)}

ENRICHMENTS["dog_acetaminophen_toxicosis"] = {"diagnosis_ja": (
    "病歴聴取でアセトアミノフェン（パラセタモール）の誤食を確認。犬の中毒量: >100 mg/kg。"
    "血液検査でメトヘモグロビン上昇（チョコレート色血液）、ハインツ小体を血液塗抹で確認。"
    "生化学でALT/AST著増（肝毒性）。凝固検査でPT延長（肝不全進行）。"
    "顔面・四肢の浮腫（犬特有）。パルスオキシメトリーで偽高値に注意。N-アセチルシステイン（NAC）が拮抗薬。"
)}

ENRICHMENTS["dog_mushroom_toxicosis"] = {"diagnosis_ja": (
    "病歴聴取でキノコ摂取を確認。種類同定が最重要（写真・残存検体を保存）。"
    "肝毒性キノコ（Amanita属）: ALT/AST/ALP著増、凝固障害（PT/APTT延長）、低血糖。摂取後6-24時間で症状。"
    "神経毒性キノコ（Inocybe/Clitocybe）: 流涎、縮瞳、徐脈（ムスカリン症状）→アトロピン。"
    "消化器型（多くのキノコ）: 嘔吐・下痢、通常6-24時間で自然回復。腎毒性型はBUN/Cre上昇。催吐+支持療法。"
)}

ENRICHMENTS["dog_snail_bait_metaldehyde_poisoning"] = {"diagnosis_ja": (
    "病歴聴取でナメクジ駆除剤（メタアルデヒド）へのアクセスを確認。摂取量を推定（致死量: 100-250 mg/kg）。"
    "身体検査で全身性振戦・痙攣・高体温（>41℃）・頻脈・過敏反応を確認。"
    "血液ガスで代謝性アシドーシス（乳酸上昇）。生化学でALT/AST上昇（肝障害）、CK上昇。"
    "尿/胃内容物のメタアルデヒド検出（ガスクロマトグラフィー）。ペレット状の嘔吐物。緊急痙攣管理が最優先。"
)}

ENRICHMENTS["dog_lily_toxicosis"] = {"diagnosis_ja": (
    "病歴聴取でユリ科植物の摂取を確認。犬では猫ほどの腎毒性は稀だが、消化管症状は発生。"
    "血液検査でBUN/Cre測定（腎機能モニタリング）。尿検査で尿比重・尿沈渣を評価。"
    "嘔吐・下痢・食欲不振の消化管症状を確認。スズラン（Convallaria）は心毒性（強心配糖体）。"
    "心電図で徐脈・不整脈をモニタリング（スズラン摂取時）。催吐+活性炭+輸液支持療法。"
)}

ENRICHMENTS["dog_sago_palm_toxicosis"] = {"diagnosis_ja": (
    "病歴聴取でソテツ（Cycas revoluta）の種子・葉の摂取を確認。全部位が有毒、特に種子。"
    "血液検査でALT/AST著増（肝毒性: cycasin）。凝固検査でPT/APTT延長、血小板低下（DIC）。"
    "血糖値低下。腹部超音波で肝臓のエコー輝度変化を評価。2-3日後に急性肝不全の進行。"
    "嘔吐（摂取後1-3時間）が初期症状。致死率30-50%。早期催吐+活性炭+集中肝保護療法が必須。"
)}

ENRICHMENTS["dog_blue-green_algae_cyanobacteria_toxicosis"] = {"diagnosis_ja": (
    "病歴聴取でアオコ（藍藻/シアノバクテリア）を含む水の摂取歴を確認。"
    "肝毒素型（microcystin）: ALT/AST著増、凝固障害、低血糖。摂取後数時間で急性肝不全。"
    "神経毒素型（anatoxin-a）: 筋硬直、痙攣、呼吸麻痺。摂取後分～時間で急性発症。"
    "水質検査でシアノバクテリア/毒素の同定。血液ガスで代謝性アシドーシス。致死率高く、早期積極治療が必要。"
)}

ENRICHMENTS["dog_permethrin_toxicosis"] = {"diagnosis_ja": (
    "病歴聴取でペルメトリン含有製品（猫用を犬に誤用は稀、大量経口摂取）の暴露歴を確認。"
    "身体検査で全身性振戦・筋痙攣・過敏反応を確認。犬では猫より耐性が高い。"
    "神経学的検査で小脳症状（運動失調、振戦）を評価。血液検査は概ね正常。"
    "体温上昇（振戦に伴う）。痙攣がある場合はジアゼパムで管理。脂質乳剤（ILE）療法を検討。"
)}

ENRICHMENTS["dog_caffeine_toxicosis"] = {"diagnosis_ja": (
    "病歴聴取でカフェイン含有製品（コーヒー、エナジードリンク、カフェイン錠剤）の摂取を確認。"
    "中毒量: >20 mg/kg（興奮）、>40 mg/kg（心毒性）、致死量: 140-150 mg/kg。"
    "心電図で頻脈性不整脈（洞性頻脈、VPC、心室頻拍）を確認。血圧上昇。"
    "身体検査で興奮、振戦、多尿、嘔吐、下痢。血液検査は概ね正常。メチルキサンチン検出可。催吐+活性炭。"
)}

ENRICHMENTS["dog_corn_cob_foreign_body"] = {"diagnosis_ja": (
    "腹部X線でトウモロコシの芯の異物（軟部組織密度で描出困難な場合あり）を確認。腸閉塞パターン。"
    "腹部超音波で腸管拡張・異物エコー・腸液貯留を確認。造影検査で通過障害を評価。"
    "CBC/生化学で脱水、電解質異常、炎症マーカーを評価。腹膜炎の有無（穿孔時）。"
    "嘔吐・食欲不振・腹痛の臨床症状。トウモロコシの芯は消化されず、腸管に嵌頓。外科的腸切開が必要。"
)}

ENRICHMENTS["dog_cuterebra_infestation"] = {"diagnosis_ja": (
    "身体検査で皮膚の腫脹性結節と呼吸孔（warble）を確認。多くは頭部・頸部・前胸部。"
    "切開排膿で結節内の幼虫（Cuterebra larva）を摘出・同定。幼虫を潰さないよう注意。"
    "二次感染の有無を創傷培養で評価。CBC/生化学は概ね正常（重度感染以外）。"
    "夏～秋の季節性。眼窩/鼻腔/脳内移行（異所性寄生）の神経症状に注意。MRIで脳内移行を確認。"
)}

ENRICHMENTS["dog_toxascaris_infection"] = {"diagnosis_ja": (
    "糞便検査で卵径75-85μmの亜球形虫卵を検出（浮遊法: ZnSO₄/NaCl飽和溶液）。"
    "Toxocara canis との鑑別: T. leonina卵は滑らかな外殻。T. canisは粗い外殻+亜球形。"
    "糞便中への成虫排出で肉眼的に確認可能。CBC/生化学は概ね正常（軽度好酸球増加）。"
    "内臓幼虫移行症のリスクはT. canisより低い。定期的糞便検査と予防的駆虫。"
)}

ENRICHMENTS["dog_spirocerca_lupi_infection"] = {"diagnosis_ja": (
    "内視鏡検査で食道壁の結節性腫瘤を確認（成虫が結節内に寄生）。生検で虫体断面を確認。"
    "糞便検査で特徴的な小型（30-38×11-15μm）の含幼虫卵を検出（浮遊法は感度低い→遠心沈殿法）。"
    "胸部X線/CTで尾側食道壁の腫瘤、大動脈瘤（幼虫移行路）、脊椎腹側の骨増殖を確認。"
    "食道骨肉腫への悪性転化のリスク。嚥下障害、吐出、喀血が臨床症状。ドラメクチンが治療。"
)}

ENRICHMENTS["dog_lungworm_angiostrongylus_vasorum"] = {"diagnosis_ja": (
    "Baermann法で糞便中のL1幼虫を検出（尾部にnotch/kinkあり）。ELISA/抗原検査（Angio Detect™）。"
    "BAL（気管支肺胞洗浄）で幼虫を検出。胸部X線でびまん性肺胞/間質パターン。"
    "CBC/凝固検査でPT延長、血小板低下（出血傾向）、好酸球増加。"
    "咳・運動不耐性・出血傾向の臨床症状。心エコーで肺高血圧・右心負荷を評価。フェンベンダゾール/イミダクロプリドが治療。"
)}

ENRICHMENTS["dog_thelazia_eye_worm"] = {"diagnosis_ja": (
    "眼科検査で結膜嚢・涙管内の半透明な線虫（成虫: 7-17 mm）を直接確認。"
    "細隙灯検査で角膜潰瘍・結膜充血・流涙を評価。結膜スワブで虫卵を検出。"
    "涙液分泌検査（STT）で乾性角結膜炎（KCS）の合併を確認。"
    "媒介者はショウジョウバエ。虫体の物理的除去+イベルメクチン/ミルベマイシンの全身投与。"
)}

ENRICHMENTS["dog_canine_schistosomiasis"] = {"diagnosis_ja": (
    "糞便検査でHeterobilvol虫卵を検出（沈殿法）。直腸粘膜生検で虫卵を含む肉芽腫を確認。"
    "CBC/生化学で好酸球増加、低アルブミン血症、高Ca血症を評価。"
    "腹部超音波で腸壁肥厚・リンパ節腫大を確認。X線で肝臓・腸管の石灰化を検出。"
    "テキサス・ルイジアナの淡水域で感染。慢性血便・下痢・体重減少。プラジカンテル/フェンベンダゾールが治療。"
)}

ENRICHMENTS["dog_portosystemic_shunt_acquired"] = {"diagnosis_ja": (
    "血液検査で食前・食後胆汁酸上昇（食前>25、食後>50 μmol/L）。血清アンモニア上昇。"
    "生化学でBUN低値、アルブミン低値、血糖低値、コレステロール低値。"
    "腹部超音波で門脈系の異常血管・複数の後天性側副血管を確認。門脈圧亢進の徴候（腹水）。"
    "造影CT（CTA）で門脈血管系の三次元評価。先天性PSSとの鑑別は年齢・基礎肝疾患で判断。基礎疾患治療が主。"
)}

ENRICHMENTS["dog_ciliary_dyskinesia_primary"] = {"diagnosis_ja": (
    "鼻腔/気管粘膜の生検で線毛の超微細構造異常を電子顕微鏡で確認（外腕ダイニン欠損が最多）。"
    "鼻腔ブラッシング/バイオプシーでの線毛運動解析（高速度ビデオ顕微鏡）。"
    "胸部X線/CTでびまん性気管支拡張、鼻副鼻腔炎、中耳炎を確認。内臓逆位（situs inversus: 50%）。"
    "CBC/BAL液で好中球増多（慢性気道感染）。精液検査で精子運動能低下。若齢発症の慢性鼻汁・咳。"
)}

ENRICHMENTS["dog_pulmonic_valve_dysplasia"] = {"diagnosis_ja": (
    "心エコー検査で肺動脈弁の肥厚・石灰化・運動制限を確認。連続波ドプラで圧較差を測定。"
    "M-モードで右室壁肥厚を定量化。カラードプラで肺動脈弁逆流を評価。"
    "聴診で左心基底部の駆出性収縮期雑音。X線で右心拡大・主肺動脈後拡張を確認。"
    "心電図で右軸偏位、右室肥大パターン。ビーグル、ボクサー、サモエドに好発。バルーン弁形成術を検討。"
)}

ENRICHMENTS["dog_mitral_valve_dysplasia"] = {"diagnosis_ja": (
    "心エコー検査で僧帽弁の形態異常（弁葉肥厚、腱索伸長/短縮、乳頭筋異常）と僧帽弁逆流を確認。"
    "カラードプラで逆流ジェットの重症度を半定量評価。左房・左室の拡大を計測。"
    "聴診で左心尖部の汎収縮期雑音。X線で左心系拡大・肺静脈うっ血を確認。"
    "心電図でP-mitrale、心房細動の有無。グレート・デーン、ブル・テリア等に好発。先天性心疾患。"
)}

ENRICHMENTS["dog_phosphofructokinase_pfk_deficiency"] = {"diagnosis_ja": (
    "CBC/血液塗抹で再生性溶血性貧血（PCV低下、網赤血球増加）を確認。発作性の溶血クリーゼ。"
    "PFK酵素活性測定で低値を確認。遺伝子検査でPFK-M遺伝子変異を同定。"
    "運動・興奮・過換気後に暗色尿（ヘモグロビン尿/ミオグロビン尿）。筋障害でCK上昇。"
    "イングリッシュ・スプリンガー・スパニエル、コッカー・スパニエルに好発。常染色体劣性遺伝。"
)}

ENRICHMENTS["dog_pyruvate_kinase_deficiency"] = {"diagnosis_ja": (
    "CBC/血液塗抹で重度の再生性溶血性貧血を確認。網赤血球著増、有核赤血球出現。"
    "PK酵素活性測定で低値。遺伝子検査でPKLR遺伝子変異を同定（犬種特異的変異）。"
    "骨髄穿刺で赤芽球系の過形成。進行例では骨髄線維症・骨硬化症。"
    "ベースンジー、ビーグル、ウエスト・ハイランド・ホワイト・テリア等に好発。常染色体劣性遺伝。1-5歳で発症。"
)}

ENRICHMENTS["dog_gastric_carcinoma"] = {"diagnosis_ja": (
    "内視鏡で胃壁の潰瘍性/浸潤性腫瘤を確認。生検で腺癌（最多）/未分化癌を確定。"
    "腹部超音波で胃壁肥厚と層構造の消失を確認。CT/造影CTで転移（リンパ節、肝臓）を評価。"
    "CBC/生化学で貧血（慢性出血）、低アルブミン血症を確認。便潜血陽性。"
    "慢性嘔吐・体重減少・食欲不振の臨床症状。ベルジアン・シェパードに好発。予後不良（MST 2-3ヶ月）。"
)}

ENRICHMENTS["dog_intestinal_adenocarcinoma"] = {"diagnosis_ja": (
    "腹部超音波で腸壁の限局性肥厚と層構造の消失を確認。超音波ガイド下FNA/生検で腺癌細胞を検出。"
    "内視鏡（十二指腸/大腸）で腫瘤を確認し生検。CT/造影CTで腸間膜リンパ節転移を評価。"
    "CBC/生化学で貧血、低アルブミン血症、電解質異常。便潜血・タール便。X線で腸閉塞パターン。"
    "大腸は直腸ポリープからの進展も。外科的腸管切除+吻合。化学療法の効果は限定的。"
)}

ENRICHMENTS["dog_pyloric_stenosis"] = {"diagnosis_ja": (
    "X線透視/造影検査で胃排出遅延とバリウムの幽門部停滞を確認。胃内ガス貯留。"
    "内視鏡で幽門部の肥厚・狭窄を直接確認。生検で肥厚性胃症（粘膜/筋層）か腫瘍かを鑑別。"
    "腹部超音波で幽門壁の著明な肥厚（>9 mm）を確認。CT/MRIで浸潤性病変を除外。"
    "慢性間欠性嘔吐（特に食後数時間）。短頭種（ボストン・テリア、ボクサー）に好発。幽門形成術が根治療法。"
)}

ENRICHMENTS["dog_gallbladder_mucocele"] = {"diagnosis_ja": (
    "腹部超音波で胆嚢内の星形/キウイフルーツ様の不動性エコー（immobile stellate pattern）を確認。"
    "胆嚢壁の肥厚・浮腫。総胆管閉塞の有無を評価。胆嚢穿孔/胆汁性腹膜炎の合併を腹腔液で評価。"
    "血液検査でALP/GGT/ALT/TBil上昇（胆汁うっ滞）。CBC/CRPで炎症・白血球増多。"
    "甲状腺機能検査・副腎機能検査で内分泌性素因を評価。シェットランド・シープドッグに好発。胆嚢切除術が治療。"
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
