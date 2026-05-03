#!/usr/bin/env python3
"""Enrich Bird diagnosis_ja — batch 9 (entries 151-200 of remaining)."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 151. bird_subcutaneous_emphysema — Subcutaneous Emphysema / 皮下気腫
ENRICHMENTS["bird_subcutaneous_emphysema"] = {
    "diagnosis_ja": "体表の触診で皮下のcrepitus（捻髪音）を確認し、気腫の範囲を評価。外傷歴（衝突・咬傷・過度の保定・手術後）を聴取。X線で皮下ガス像・気嚢壁の不連続・縦隔気腫を検出。CT検査で破裂気嚢の正確な同定。CBC（採血量≤体重の1%）で二次感染の有無を確認。血液生化学でAST・LDH変動を測定。鳥類では気嚢破裂が皮下気腫の最も一般的な原因であり、経皮的穿刺脱気で一時的減圧が可能。軽度例は安静で自然治癒するが、再発性・進行性の場合は気嚢壁の外科的修復を検討する"
}

# 152. bird_psittacine_poxvirus_canarypox_variant — Psittacine Poxvirus (Canarypox Variant)
ENRICHMENTS["bird_psittacine_poxvirus_canarypox_variant"] = {
    "diagnosis_ja": "皮膚型：嘴基部・眼周囲・脚の痘疹性結節・痂皮を視診で確認。粘膜型：口腔・上部気道のジフテリア様偽膜を観察。病変部の組織生検でBollinger小体（細胞質内封入体）を確認。電子顕微鏡でPoxウイルス粒子を同定。PCR検査でカナリア痘ウイルスDNAを検出し型別。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。鳥類のカナリア痘変異型はオウム目に感染し、皮膚型は予後良好だが粘膜型は上気道閉塞・二次感染で重篤化する。蚊等の媒介昆虫による伝播が主経路"
}

# 153. bird_avian_adenovirus_hepatitis — Avian Adenovirus Hepatitis
ENRICHMENTS["bird_avian_adenovirus_hepatitis"] = {
    "diagnosis_ja": "急性沈鬱・食欲廃絶・黄色尿酸塩（ビリベルジン尿）の臨床評価。血液生化学（採血量≤体重の1%）で肝酵素著増（AST・LDH・GGT）・胆汁酸上昇を確認。CBC でヘテロフィル変動・リンパ球減少を評価。腹部超音波で肝腫大・肝実質エコー変化を検出。PCR検査でAdenovirus DNAを検出。病理組織検査で肝細胞壊死・核内封入体（basophilic intranuclear inclusion body）を確認。鳥類のアデノウイルス性肝炎はオウム目の幼鳥で急性致死性であり、免疫抑制個体で重篤化する"
}

# 154. bird_avian_paramyxovirus-3_pmv-3 — Avian Paramyxovirus-3 (PMV-3)
ENRICHMENTS["bird_avian_paramyxovirus-3_pmv-3"] = {
    "diagnosis_ja": "神経症状（斜頸・旋回運動・振戦・麻痺）・呼吸器症状（鼻汁・くしゃみ）・膵炎症状（嘔吐・消化不良）の臨床評価。RT-PCR検査でPMV-3 RNAを検出。血清学検査（HI試験・ELISA）でペア血清の抗体上昇を確認。ウイルス分離で確定。CBC（採血量≤体重の1%）でリンパ球変動を評価。血液生化学でアミラーゼ・リパーゼ上昇（膵炎合併時）を測定。鳥類のPMV-3はオウム目・フィンチ類に感染し、PMV-1（ニューカッスル病）より病原性は低いが膵臓親和性を示す"
}

# 155. bird_duck_plague_anatid_herpesvirus — Duck Plague (Anatid Herpesvirus)
ENRICHMENTS["bird_duck_plague_anatid_herpesvirus"] = {
    "diagnosis_ja": "水禽類（アヒル・ガチョウ・白鳥）の急性大量死・出血性食道炎・血液性下痢の臨床評価。剖検で消化管粘膜の帯状出血性壊死（食道・総排泄腔が特徴的）・肝脾腫大・腹膜出血を確認。PCR検査でAnatid herpesvirus-1（Duck plague virus）DNAを検出。組織病理で核内好酸性封入体を確認。ウイルス分離で確定。CBC（採血量≤体重の1%）でリンパ球減少を評価。鳥類のDuck plagueは届出疾病であり、高致死率（最大90%）の急性ヘルペスウイルス感染症である"
}

# 156. bird_avian_erysipelas — Avian Erysipelas / 鳥類丹毒
ENRICHMENTS["bird_avian_erysipelas"] = {
    "diagnosis_ja": "急性死・沈鬱・皮膚チアノーゼ（顔面・肉垂の暗赤色変化）の臨床評価。血液・脾臓・肝臓の細菌培養でErysipelothrix rhusiopathiaeを分離。グラム染色で細い非運動性グラム陽性桿菌を確認。感受性試験（ペニシリン系が第一選択）。PCR検査で菌種確定。CBC（採血量≤体重の1%）でヘテロフィル著増を確認。剖検で脾腫・心内膜疣贅・腎出血を確認。鳥類の丹毒は七面鳥・アヒル・エミューに好発し、土壌汚染・皮膚創傷からの感染が主経路。人獣共通感染症として注意が必要"
}

# 157. bird_avian_e._coli_septicemia — Avian E. coli Septicemia / 鳥類大腸菌敗血症
ENRICHMENTS["bird_avian_e._coli_septicemia"] = {
    "diagnosis_ja": "急性沈鬱・呼吸困難・緑色下痢・多臓器不全徴候の臨床評価。血液培養でE. coliを分離し薬剤感受性試験を実施。グラム染色でグラム陰性桿菌を確認。CBC（採血量≤体重の1%）でヘテロフィル著増・毒性顆粒を確認。血液生化学でAST・LDH著増・UA上昇を測定。胸部X線で気嚢混濁・肝腫大を検出。剖検で線維素性心囊炎・気嚢炎・肝被膜炎（colisepticemiaの三徴）を確認。鳥類では呼吸器感染（ウイルス・マイコプラズマ等）に続発するE. coli敗血症が多臓器不全の主要死因となる"
}

# 158. bird_avian_listeriosis — Avian Listeriosis / 鳥類リステリア症
ENRICHMENTS["bird_avian_listeriosis"] = {
    "diagnosis_ja": "神経症状（斜頸・旋回運動・運動失調・痙攣）または敗血症症状（急性死・沈鬱）の臨床評価。血液・脳・肝臓の細菌培養でListeria monocytogenesを分離（4℃cold enrichment法）。PCR検査で菌種確定。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多を確認。血液生化学でAST・LDH上昇を測定。病理組織検査で脳幹の微小膿瘍・壊死巣（脳炎型）または肝脾の壊死性肉芽腫（敗血症型）を確認。鳥類のリステリア症は汚染飼料・土壌からの経口感染が主因で人獣共通感染症"
}

# 159. bird_syngamus_trachea_gapeworm_advanced — Syngamus trachea (Gapeworm) Advanced / 気管開口虫症（重度）
ENRICHMENTS["bird_syngamus_trachea_gapeworm_advanced"] = {
    "diagnosis_ja": "重度の開口呼吸・窒息様症状・頸部伸展・体重著減の臨床評価。気管内視鏡で多数のSyngamus trachea成虫（Y字型交尾虫体が気管内腔を広範に占拠）を直視確認。気管洗浄液の鏡検で虫卵・幼虫を検出。糞便浮遊法で虫卵を確認。CBC（採血量≤体重の1%）で重度貧血（PCV著低）・好酸球増加を評価。X線で気管内軟部組織充填・肺野異常を検出。重度例では気管閉塞→窒息死のリスクがあり、イベルメクチン/フェンベンダゾールによる緊急駆虫と支持療法が必要"
}

# 160. bird_avian_schistosomiasis — Avian Schistosomiasis / 鳥類住血吸虫症
ENRICHMENTS["bird_avian_schistosomiasis"] = {
    "diagnosis_ja": "肝腫大・腹水・体重減少・下痢の臨床評価。糞便検査（沈殿法）で住血吸虫卵（側棘・終棘の有無で種同定）を検出。肝生検の病理組織検査で門脈域の虫卵肉芽腫を確認。CBC（採血量≤体重の1%）で好酸球増加・貧血を評価。血液生化学で肝酵素上昇・アルブミン低下を測定。腹部超音波で肝腫大・門脈拡張・腹水を検出。鳥類の住血吸虫症はTrichobilharzia等の種が鳥類終宿主に寄生し、淡水巻貝を中間宿主とする。水禽類で多発する"
}

# 161. bird_avian_filarial_infection — Avian Filarial Infection / 鳥類フィラリア感染症
ENRICHMENTS["bird_avian_filarial_infection"] = {
    "diagnosis_ja": "皮下結節・関節腫脹・体腔液貯留の臨床評価。末梢血塗抹のギムザ染色でミクロフィラリア（sheathed/unsheathed、頭尾の形態で種同定）を検出。Knott法で血中ミクロフィラリアを濃縮検出。PCR検査で種同定。CBC（採血量≤体重の1%）で好酸球増加を確認。血液生化学で全身状態を評価。皮下結節のFNA/生検で成虫を確認。鳥類ではSarconema・Pelecitus・Chandlerella等のフィラリアが報告され、吸血昆虫（蚊・ヌカカ・シラミバエ）を媒介とする"
}

# 162. bird_avian_leukosis — Avian Leukosis / 鳥類白血病
ENRICHMENTS["bird_avian_leukosis"] = {
    "diagnosis_ja": "慢性消耗・腹部腫瘤・肝脾腫大の臨床評価。CBC（採血量≤体重の1%）で白血球数の異常増加（リンパ球性・骨髄球性の型による）を確認。末梢血塗抹で異常リンパ球の形態を評価。ELISA検査でALV（Avian Leukosis Virus）抗原（p27）を検出。PCR検査でALV proviral DNAを検出。血液生化学でAST・LDH著増を測定。腹部超音波で肝脾腫・腫瘤を検出。病理組織検査でリンパ腫の組織型を確定。鳥類のALVはレトロウイルスであり、垂直伝播（卵内感染）が主要伝播経路"
}

# 163. bird_marek's_disease_avian — Marek's Disease (Avian) / マレック病（鳥類）
ENRICHMENTS["bird_marek's_disease_avian"] = {
    "diagnosis_ja": "末梢神経障害（片脚麻痺→前後方向開脚姿勢・翼下垂）・内臓リンパ腫・皮膚腫瘍の臨床評価。PCR検査でマレック病ウイルス（MDV: Gallid alphaherpesvirus 2）DNAを検出。羽包上皮のPCRが非侵襲的検体として有用。CBC（採血量≤体重の1%）で異型リンパ球を検索。病理組織検査で末梢神経（坐骨神経・迷走神経）のリンパ球浸潤・腫大を確認。内臓腫瘍の細胞診・生検でT細胞リンパ腫を確定。鳥類のマレック病は鶏に好発するT細胞リンパ増殖性疾患であり、ワクチンで予防可能"
}

# 164. bird_reticuloendotheliosis — Reticuloendotheliosis / 細網内皮症
ENRICHMENTS["bird_reticuloendotheliosis"] = {
    "diagnosis_ja": "慢性消耗・免疫抑制症状・リンパ腫形成の臨床評価。PCR検査でReticuloendotheliosis virus（REV）proviral DNAを検出。ELISA検査でREV抗原・抗体を測定。CBC（採血量≤体重の1%）で異型リンパ球・リンパ球減少（免疫抑制型）を評価。血液生化学でAST・LDH変動を測定。病理組織検査で脾臓・肝臓・ファブリキウス嚢のリンパ増殖性病変を確認。鳥類のREVはレトロウイルスで免疫抑制と腫瘍形成の両方を引き起こし、マレック病ワクチンへの混入汚染が歴史的に問題となった"
}

# 165. bird_avian_nephritis_virus_infection — Avian Nephritis Virus Infection / 鳥腎炎ウイルス感染症
ENRICHMENTS["bird_avian_nephritis_virus_infection"] = {
    "diagnosis_ja": "多飲多尿・水様性下痢・沈鬱・成長遅延の臨床評価。血液生化学（採血量≤体重の1%）でUA著増・電解質異常（K上昇・Na低下）を確認。CBC でヘテロフィル変動を評価。RT-PCR検査でAvian nephritis virus（ANV: Astroviridae）RNAを検出。腎臓超音波で腎腫大・エコー異常を検出。剖検で腎臓の腫大・蒼白化を確認。病理組織検査で尿細管上皮壊死・間質性腎炎を確認。鳥類のANVは鶏のヒナで急性腎炎を引き起こし、アストロウイルス科に分類される"
}

# 166. bird_avian_encephalomyelitis_epidemic_tremor — Avian Encephalomyelitis (Epidemic Tremor)
ENRICHMENTS["bird_avian_encephalomyelitis_epidemic_tremor"] = {
    "diagnosis_ja": "幼鳥の振戦（特に頭部・頸部の微細振戦）・運動失調・起立不能の臨床評価。PCR検査でAvian encephalomyelitis virus（AEV: Tremovirus A）RNAを検出。血清学検査（ELISA）で抗体価を測定。CBC（採血量≤体重の1%）でリンパ球変動を評価。病理組織検査で中枢神経系（脳幹・脊髄）のリンパ球性血管周囲炎・神経細胞壊死を確認。鳥類のAEVは1-3週齢の幼鳥で流行性振戦を引き起こし、経卵伝播と水平伝播（経口-糞便）の両方で拡散する"
}

# 167. bird_avian_hepatitis_e_virus — Avian Hepatitis E Virus / 鳥類E型肝炎ウイルス
ENRICHMENTS["bird_avian_hepatitis_e_virus"] = {
    "diagnosis_ja": "肝脾腫大・腹水・産卵低下・卵巣退行の臨床評価。血液生化学（採血量≤体重の1%）で肝酵素著増（AST・LDH・GGT）・胆汁酸上昇を確認。CBC でヘテロフィル変動・リンパ球減少を評価。RT-PCR検査でAvian hepatitis E virus RNAを検出（糞便・胆汁・肝臓検体）。血清学検査（ELISA）で抗体価を測定。腹部超音波で肝腫大・腹水を検出。病理組織検査で肝細胞壊死・リンパ球浸潤を確認。鳥類のHEVは産卵鶏の肝脾腫大症候群の原因として重要"
}

# 168. bird_riemerella_anatipestifer_infection — Riemerella anatipestifer Infection
ENRICHMENTS["bird_riemerella_anatipestifer_infection"] = {
    "diagnosis_ja": "水禽類（アヒル・ガチョウ）の急性沈鬱・振戦・斜頸・緑色下痢の臨床評価。脳・肝臓・心囊液の細菌培養でRiemerella anatipestiferを分離（5% CO2・血液寒天・48時間）。グラム染色でグラム陰性桿菌を確認。AGID法・ELISA法で血清型を判定。PCR検査で菌種を確定。CBC（採血量≤体重の1%）でヘテロフィル著増を確認。剖検で線維素性心囊炎・肝被膜炎・気嚢炎を確認。鳥類のR. anatipestifer感染は水禽類の主要細菌性疾患であり、21血清型が知られ交差免疫は限定的"
}

# 169. bird_brachyspira_infection_avian_intestinal_spirochetosis — Brachyspira Infection
ENRICHMENTS["bird_brachyspira_infection_avian_intestinal_spirochetosis"] = {
    "diagnosis_ja": "産卵低下・汚卵増加・泡沫性褐色下痢・慢性消耗の臨床評価。新鮮糞便の暗視野顕微鏡で運動性スピロヘータを検出。選択培養培地（血液寒天+抗菌薬添加・嫌気条件）でBrachyspira属を分離。PCR検査で種同定（B. pilosicoli・B. intermedia等）。盲腸内容物の塗抹のギムザ染色でスピロヘータを確認。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。鳥類の腸管スピロヘータ症は産卵鶏の産卵性低下・飼料効率低下の原因として経済的に重要"
}

# 170. bird_macrorhabdus_ornithogaster_refractory_infection — Macrorhabdus ornithogaster Refractory
ENRICHMENTS["bird_macrorhabdus_ornithogaster_refractory_infection"] = {
    "diagnosis_ja": "治療抵抗性の慢性削痩・嘔吐・未消化粒状便・膨羽の臨床評価。糞便のグラム染色・ギムザ染色で大型棒状酵母体（Macrorhabdus ornithogaster: 20-90μm）の持続的排出を確認。定量的糞便スコアで菌量を評価。腹部X線で前胃拡張・筋胃菲薄化を検出。内視鏡で前胃粘膜の白色結節・びらんを確認・生検。血液生化学（採血量≤体重の1%）でTP低下・グルコース低下を測定。難治例ではアムホテリシンB単独抵抗性を考慮し、NaHCO3併用・長期治療（6-8週間）・免疫状態の再評価を行う"
}

# 171. bird_infectious_laryngotracheitis_ilt_advanced — Infectious Laryngotracheitis (ILT) Advanced
ENRICHMENTS["bird_infectious_laryngotracheitis_ilt_advanced"] = {
    "diagnosis_ja": "重度呼吸困難・血液混入痰の喀出・開口呼吸・頸部伸展の臨床評価。気管スワブのPCR検査でGallid alphaherpesvirus 1（ILTV）DNAを検出。気管組織の病理組織検査で気管上皮の合胞体形成・核内好酸性封入体を確認。血清学検査（ELISA）で抗体価上昇を確認。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。気管内視鏡で粘膜の出血性壊死・偽膜形成を直視。鳥類のILT重症型は気管内の血性滲出物による窒息が致死的であり、致死率は最大70%に達する"
}

# 172. bird_ornithobacterium_rhinotracheale_ort_pneumonia — ORT Pneumonia
ENRICHMENTS["bird_ornithobacterium_rhinotracheale_ort_pneumonia"] = {
    "diagnosis_ja": "重度呼吸困難・湿性ラ音・開口呼吸・産卵低下の臨床評価。気管洗浄液・気嚢穿刺液の培養でOrnithobacterium rhinotrachealeを分離（5% CO2・血液寒天）。PCR検査でORT特異的遺伝子を検出。胸部X線で肺野浸潤影・気嚢混濁を確認。CBC（採血量≤体重の1%）でヘテロフィル著増を確認。剖検で線維素性肺炎・気嚢炎を確認。血清学検査（ELISA）で抗体上昇を確認。鳥類のORT肺炎はE. coli等との混合感染で重篤化し、七面鳥では致死率が高い"
}

# 173. bird_avian_spirochetosis_borrelia — Avian Spirochetosis (Borrelia)
ENRICHMENTS["bird_avian_spirochetosis_borrelia"] = {
    "diagnosis_ja": "急性沈鬱・発熱・チアノーゼ・緑色粘液性下痢・貧血の臨床評価。末梢血塗抹のギムザ染色でBorrelia anserina（長鎖らせん状スピロヘータ）を検出。暗視野顕微鏡で特徴的な螺旋運動を確認。PCR検査でBorrelia属の16S rRNA遺伝子を増幅し種同定。CBC（採血量≤体重の1%）で貧血（PCV低下）・血小板減少を確認。血液生化学でAST・LDH上昇（肝障害）を測定。鳥類のB. anserina感染はArgasダニ（軟ダニ）を介して伝播し、未治療の急性型は致死率30-60%に達する"
}

# 174. bird_avian_metapneumovirus_rhinotracheitis — Avian Metapneumovirus Rhinotracheitis
ENRICHMENTS["bird_avian_metapneumovirus_rhinotracheitis"] = {
    "diagnosis_ja": "上部気道症状（鼻汁・くしゃみ・副鼻腔腫脹・涙液増加）・産卵低下の臨床評価。RT-PCR検査で鳥メタニューモウイルス（aMPV）RNAを検出し亜型（A/B/C/D）を判定。血清学検査（ELISA）でペア血清の抗体上昇を確認。気管・副鼻腔スワブのウイルス分離。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。X線で副鼻腔混濁を検出。鳥類のaMPVは七面鳥のSwollen Head Syndrome・鶏のTRT（Turkey Rhinotracheitis）の原因であり、二次的細菌感染で重篤化する"
}

# 175. bird_psittacine_herpesvirus_–_mucosal_form — Psittacine Herpesvirus – Mucosal Form
ENRICHMENTS["bird_psittacine_herpesvirus_–_mucosal_form"] = {
    "diagnosis_ja": "口腔・食道粘膜の白色〜黄色壊死性プラーク（ジフテリア様偽膜）・嚥下困難・食欲廃絶の臨床評価。病変部の組織生検で上皮細胞の膨大化・核内好酸性封入体（Cowdry type A）を確認。PCR検査でPsittacid alphaherpesvirus（PsHV）DNAを検出。CBC（採血量≤体重の1%）でリンパ球減少・ヘテロフィル増加を評価。血液生化学でAST・LDH変動を測定。鳥類のPsHV粘膜型はアマゾン・ヨウムで報告が多く、Pacheco's diseaseの粘膜限局型として発現する"
}

# 176. bird_chlamydiosis_–_chronic_latent_form — Chlamydiosis – Chronic Latent Form
ENRICHMENTS["bird_chlamydiosis_–_chronic_latent_form"] = {
    "diagnosis_ja": "無症状〜軽度の間欠的症状（軽度鼻汁・体重減少傾向）の臨床評価。排泄腔・後鼻孔スワブのPCR検査でChlamydia psittaci DNAを検出（間欠的排菌のため3回以上の検査を推奨）。血清学検査（ELISA・CF）で抗体価を測定。CBC（採血量≤体重の1%）で軽度の単球増多を確認。血液生化学でAST・LDH軽度上昇を評価。肝超音波で慢性肝変化を検索。鳥類の慢性潜伏型クラミジア症はストレス時に再活性化して排菌し、飼い主への感染（オウム病: 人獣共通感染症）リスクとなる"
}

# 177. bird_chlamydiosis_–_ocular_form — Chlamydiosis – Ocular Form / クラミジア症眼型
ENRICHMENTS["bird_chlamydiosis_–_ocular_form"] = {
    "diagnosis_ja": "片側性〜両側性の結膜炎（結膜充血・腫脹・漿液性〜粘液膿性分泌物）・眼瞼腫脹の臨床評価。結膜スワブのPCR検査でChlamydia psittaci DNAを検出。結膜掻爬の細胞診でマクロファージ内の封入体を確認（ギムザ染色）。排泄腔スワブPCRで全身感染を評価。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多を確認。血液生化学でAST上昇を測定。鳥類の眼型クラミジア症は全身感染の一部として発現し、呼吸器型・肝型との合併を常に考慮する"
}

# 178. bird_chlamydiosis_–_hepatic_form — Chlamydiosis – Hepatic Form / クラミジア症肝型
ENRICHMENTS["bird_chlamydiosis_–_hepatic_form"] = {
    "diagnosis_ja": "沈鬱・食欲廃絶・黄色〜緑色尿酸塩（ビリベルジン尿）・肝腫大の臨床評価。排泄腔・後鼻孔スワブのPCR検査でChlamydia psittaci DNAを検出。血液生化学（採血量≤体重の1%）で肝酵素著増（AST・LDH・GGT）・胆汁酸上昇・アルブミン低下を確認。CBC でヘテロフィル著増・単球増多・毒性変化を評価。腹部超音波で肝腫大・肝実質エコー異常を検出。肝生検でクラミジア封入体を確認。鳥類の肝型クラミジア症はオカメインコ・セキセイインコで急性肝不全として発現し致死的となりうる"
}

# 179. bird_sour_crop_fermentative_ingluvitis — Sour Crop (Fermentative Ingluvitis)
ENRICHMENTS["bird_sour_crop_fermentative_ingluvitis"] = {
    "diagnosis_ja": "嗉嚢の触診で膨満・液体波動を確認。嗉嚢液の逆流・酸臭の確認。嗉嚢洗浄液の鏡検で酵母（Candida albicans等）・細菌過増殖を検索。グラム染色で出芽酵母・菌糸を確認。嗉嚢液のpH測定（正常pH 5-6、酸敗嗉嚢ではpH<4）。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。腹部X線で嗉嚢拡張・消化管通過遅延を確認。鳥類の酸敗嗉嚢は嗉嚢運動障害・カンジダ感染・不適切な手差し給餌（温度不足・過濃度）が原因であり、幼鳥の手差し飼育で多発する"
}

# 180. bird_rhinolithiasis_rhinolith — Rhinolithiasis (Rhinolith) / 鼻石症
ENRICHMENTS["bird_rhinolithiasis_rhinolith"] = {
    "diagnosis_ja": "片側性鼻閉・鼻汁・くしゃみ・鼻孔周囲の腫脹を臨床評価。頭部X線で鼻腔内の高密度異物（鼻石: mineral concretion）を検出。CT検査で鼻石のサイズ・位置・骨浸食を詳細評価。内視鏡で鼻石を直視確認。CBC（採血量≤体重の1%）でヘテロフィル変動を確認。血液生化学で全身状態を評価。鼻汁培養で二次感染菌を同定。鳥類の鼻石は慢性鼻炎・VitA欠乏による鼻腔粘膜扁平上皮化生・分泌物の乾燥固化が原因で形成され、外科的摘出とVitA補充が治療の基本"
}

# 181. bird_aspergillosis_–_acute_fulminant_form — Aspergillosis – Acute Fulminant Form
ENRICHMENTS["bird_aspergillosis_–_acute_fulminant_form"] = {
    "diagnosis_ja": "急性の重度呼吸困難・開口呼吸・チアノーゼ・急速な衰弱の臨床評価。胸部X線で肺野のびまん性浸潤影・気嚢混濁を検出。CBC（採血量≤体重の1%）でヘテロフィル著増・単球増多を確認。血清ガラクトマンナン抗原（β-D-グルカン）上昇を確認。気管洗浄液の培養でAspergillus fumigatusを分離。細胞診で分枝隔壁菌糸を確認。鳥類の急性劇症型アスペルギルス症は免疫抑制個体（幼鳥・輸送ストレス・PBFD合併）で大量の胞子吸入後に発症し、数日以内に致死的となる"
}

# 182. bird_aspergillosis_–_chronic_granulomatous_form — Aspergillosis – Chronic Granulomatous Form
ENRICHMENTS["bird_aspergillosis_–_chronic_granulomatous_form"] = {
    "diagnosis_ja": "慢性の体重減少・運動不耐性・呼吸困難・声の変化（鳴管病変）の臨床評価。胸部X線・CTで気嚢壁肥厚・結節性肉芽腫・石灰化病変を検出。内視鏡で気嚢内の白色〜黄緑色真菌腫を直視確認・生検。CBC（採血量≤体重の1%）で慢性炎症パターン（単球増多・軽度ヘテロフィル増加）を確認。血清ガラクトマンナン抗原検査。真菌培養でAspergillus属を同定。鳥類の慢性肉芽腫型は最も一般的なアスペルギルス症の病型で、気嚢・鳴管・肺に肉芽腫を形成し長期治療を要する"
}

# 183. bird_aspergillosis_–_syringeal_form — Aspergillosis – Syringeal Form
ENRICHMENTS["bird_aspergillosis_–_syringeal_form"] = {
    "diagnosis_ja": "声の変化（嗄声・失声）・吸気性呼吸困難（鳴管レベルの気道閉塞）の臨床評価。気管内視鏡で鳴管（syrinx）の真菌腫・肉芽腫による気道狭窄を直視確認。気管洗浄液の真菌培養でAspergillus属を分離。細胞診で分枝隔壁菌糸・分生子を検出。胸部X線・CTで鳴管レベルの軟部組織腫瘤を検出。CBC（採血量≤体重の1%）で慢性炎症変化を確認。鳥類の鳴管型アスペルギルス症は声の変化が初発症状であり、進行すると気道閉塞による窒息リスクがある。外科的デブリードマン+全身抗真菌療法が必要"
}

# 184. bird_vitamin_d_toxicosis_hypervitaminosis_d_–_renal_form — Vitamin D Toxicosis (Renal Form)
ENRICHMENTS["bird_vitamin_d_toxicosis_hypervitaminosis_d_–_renal_form"] = {
    "diagnosis_ja": "多飲多尿・食欲低下・体重減少・沈鬱の臨床評価。血液生化学（採血量≤体重の1%）でCa著増（>15 mg/dL）・P上昇・UA著増（腎不全）を確認。腹部超音波で腎実質の高エコー領域（石灰化）を検出。X線で腎臓・大動脈・消化管壁の軟部組織石灰化を評価。サプリメント・食餌歴の詳細聴取（VitD3過剰補充）。病理組織検査で腎尿細管壊死・間質石灰化を確認。鳥類ではVitD3過剰による腎Ca沈着→腎不全→痛風の連鎖が致死的経過をたどる"
}

# 185. bird_conure_bleeding_syndrome — Conure Bleeding Syndrome / コニュア出血症候群
ENRICHMENTS["bird_conure_bleeding_syndrome"] = {
    "diagnosis_ja": "コニュア（コニュアインコ属）での自然出血（皮下出血・粘膜出血・消化管出血）の臨床評価。凝固検査でPT延長・APTT延長を確認。CBC（採血量≤体重の1%）で重度貧血（PCV低下）を評価。血液生化学で肝酵素（AST・LDH）上昇・Ca・K変動を測定。肝超音波・X線で肝疾患を検索。VitK欠乏・肝不全（DIC）・重金属中毒を鑑別。鳥類ではConure bleeding syndromeはコニュア属に特異的な出血性疾患であり、VitK依存性凝固因子の低下が病態の中心。VitK1補充への反応で診断を確認"
}

# 186. bird_psittacine_beak_and_feather_disease_–_peracute_neonatal_form — PBFD Peracute Neonatal Form
ENRICHMENTS["bird_psittacine_beak_and_feather_disease_–_peracute_neonatal_form"] = {
    "diagnosis_ja": "新生幼鳥の急性沈鬱・膨羽・食欲廃絶・急速な衰弱・急性死の臨床評価。PCR検査でBeak and Feather Disease Virus（BFDV: Circovirus）DNAを検出（血液・羽毛・排泄腔スワブ）。CBC（採血量≤体重の1%）でリンパ球著減（重度免疫抑制）・貧血・ヘテロフィル減少を確認。病理組織検査でファブリキウス嚢・胸腺のリンパ球枯渇・壊死を確認。鳥類のPBFD超急性新生児型は幼鳥の免疫系が未成熟な時期にBFDVに感染し、重篤な免疫抑制による敗血症で急性死する"
}

# 187. bird_cryptosporidiosis — Cryptosporidiosis / クリプトスポリジウム症
ENRICHMENTS["bird_cryptosporidiosis"] = {
    "diagnosis_ja": "慢性下痢・体重減少・呼吸器症状（気管クリプトスポリジウム症の場合）の臨床評価。糞便の特殊染色（ショ糖浮遊法後の抗酸染色）でCryptosporidiumオーシスト（4-6μm、赤色に染色）を検出。PCR検査で種同定（C. baileyi: 呼吸器型、C. meleagridis: 消化管型）。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。気管洗浄液の検査で気管型を確認。鳥類のクリプトスポリジウム症は免疫抑制個体で重篤化し、特にC. baileyiによる気管感染が呼吸困難を引き起こす"
}

# 188. bird_cochlosomosis — Cochlosomosis / コクロソーマ症
ENRICHMENTS["bird_cochlosomosis"] = {
    "diagnosis_ja": "水様性下痢・体重減少・成長遅延（特にフィンチ類幼鳥）の臨床評価。新鮮糞便の直接塗抹鏡検でCochlosoma原虫（5-12μm・楕円形・特徴的な腹側吸着盤）の運動性栄養体を検出。検体は採取後30分以内に鏡検（原虫の運動性が急速に低下するため）。ギムザ染色で形態を確認しTrichomonasと鑑別。CBC（採血量≤体重の1%）でヘテロフィル変動を確認。鳥類のCochlosoma感染は文鳥・キンカチョウ等のフィンチ類に好発し、経口-糞便経路で容易に群内伝播する"
}

# 189. bird_avian_malaria_–_acute_form — Avian Malaria – Acute Form / 鳥マラリア急性型
ENRICHMENTS["bird_avian_malaria_–_acute_form"] = {
    "diagnosis_ja": "急性の沈鬱・食欲廃絶・呼吸困難・貧血（粘膜蒼白）の臨床評価。末梢血塗抹のギムザ染色でPlasmodium属のトロフォゾイト・シゾント・ガメトサイトを赤血球内に検出。PCR検査でPlasmodium属の種同定。CBC（採血量≤体重の1%）で重度再生性貧血（PCV<20%）・網状赤血球増加を確認。血液生化学でAST・LDH上昇（溶血・肝障害）を測定。鳥類のPlasmodium感染は蚊（Culex・Aedes属）を媒介とし、ペンギン等の免疫学的にナイーブな種で急性大量死を引き起こす"
}

# 190. bird_avian_leucocytozoonosis — Avian Leucocytozoonosis / 鳥ロイコチトゾーン症
ENRICHMENTS["bird_avian_leucocytozoonosis"] = {
    "diagnosis_ja": "急性貧血（粘膜蒼白・呼吸困難）・沈鬱・緑色下痢の臨床評価。末梢血塗抹のギムザ染色でLeucocytozoon属の大型ガメトサイト（宿主細胞を著しく変形させる丸形体）を白血球/赤血球内に検出。PCR検査で種同定。CBC（採血量≤体重の1%）で重度貧血（PCV著低）・好酸球増加を確認。血液生化学でAST・LDH上昇を測定。脾臓超音波で脾腫を検出。鳥類のLeucocytozoon感染はブユ（Simulium属）媒介で、水禽類・猛禽類の急性致死性貧血の重要な原因である"
}

# 191. bird_feather_follicle_tumor_feather_folliculoma — Feather Follicle Tumor (Feather Folliculoma)
ENRICHMENTS["bird_feather_follicle_tumor_feather_folliculoma"] = {
    "diagnosis_ja": "皮膚の結節性腫瘤（毛包周囲の硬い結節・表面に異常羽毛を伴うことあり）を身体検査で確認。FNA細胞診で角化上皮細胞・毛根鞘成分を確認。外科切除検体の病理組織検査で毛包上皮由来の腫瘍（毛包腫：folliculoma）を確定・悪性度を評価。X線で骨浸潤の有無を確認。CBC（採血量≤体重の1%）で全身状態を評価。鳥類では毛包腫瘍はセキセイインコ・カナリアで報告があり、良性の毛包腫が最多だが稀に悪性化する。完全切除で予後は良好"
}

# 192. bird_renal_cystadenocarcinoma — Renal Cystadenocarcinoma / 腎嚢胞腺癌
ENRICHMENTS["bird_renal_cystadenocarcinoma"] = {
    "diagnosis_ja": "片脚麻痺（腎腫瘤による坐骨神経叢圧迫）・腹部膨満・多飲多尿の臨床評価。腹部超音波で腎臓の嚢胞性腫瘤を検出。CT検査で腫瘤の範囲・対側腎・転移を評価。血液生化学（採血量≤体重の1%）でUA著増・電解質異常を確認。CBC で貧血・白血球変動を確認。FNA細胞診または生検で腺癌細胞を確認し病理組織検査で確定。鳥類の腎嚢胞腺癌はセキセイインコに好発する悪性腎腫瘍であり、片脚麻痺が初発症状となることが多い。予後は一般に不良"
}

# 193. bird_liposarcoma — Liposarcoma / 脂肪肉腫
ENRICHMENTS["bird_liposarcoma"] = {
    "diagnosis_ja": "皮下の軟性〜硬性腫瘤（脂肪腫との触感の鑑別は困難）を身体検査で確認。FNA細胞診で異型脂肪芽細胞を検出（脂肪腫との鑑別が重要）。外科切除検体の病理組織検査で脂肪肉腫を確定し、組織亜型（高分化型・粘液型・多形型等）を分類。X線・CT検査で局所浸潤・転移を評価。CBC・血液生化学（採血量≤体重の1%）で全身状態を評価。鳥類では脂肪肉腫は脂肪腫より稀であるが、セキセイインコ・アマゾンで報告がある。局所浸潤性で再発率が高く、広範囲切除が推奨される"
}

# 194. bird_leiomyosarcoma — Leiomyosarcoma / 平滑筋肉腫
ENRICHMENTS["bird_leiomyosarcoma"] = {
    "diagnosis_ja": "消化管腫瘤による通過障害（嘔吐・食欲低下・体重減少）・腹部膨満の臨床評価。腹部超音波で消化管壁・腹腔内の腫瘤を検出。FNA細胞診で紡錘形細胞腫瘍を確認。外科切除検体の病理組織検査・免疫組織化学（SMA・desmin陽性）で平滑筋肉腫を確定。X線・CTで転移（肝臓・肺）を検索。CBC・血液生化学（採血量≤体重の1%）で貧血・AST変動を評価。鳥類の平滑筋肉腫は消化管・子宮・血管壁から発生し、外科的完全切除が唯一の根治的治療"
}

# 195. bird_beak_malocclusion_–_mandibular_prognathism — Beak Malocclusion – Mandibular Prognathism
ENRICHMENTS["bird_beak_malocclusion_–_mandibular_prognathism"] = {
    "diagnosis_ja": "下嘴の上嘴に対する前方偏位（アンダーバイト）を視診で確認。嘴の咬合パターン・嘴角度・対称性を評価。頭部X線・CTで骨格構造の異常・嘴根部の変形を描出。口腔内検査で舌・口蓋への嘴先端の外傷を検索。CBC（採血量≤体重の1%）で二次感染を評価。飼育歴・繁殖歴の聴取（遺伝的素因・不適切な手差し給餌による嘴変形）。鳥類ではコッカトゥー・マコーの幼鳥で下顎前突が多く報告され、早期の嘴矯正（物理的補正器具・定期的トリミング）で改善可能な場合がある"
}

# 196. bird_egg_peritonitis_–_chronic_form — Egg Peritonitis – Chronic Form / 卵黄性腹膜炎慢性型
ENRICHMENTS["bird_egg_peritonitis_–_chronic_form"] = {
    "diagnosis_ja": "慢性的な腹部膨満・体重減少・間欠的な沈鬱の臨床評価。腹部超音波で体腔液貯留・卵管腫大・卵黄塊を検出。体腔穿刺液の細胞診で卵黄物質・炎症細胞を確認。細菌培養で二次感染菌（E. coli等）を同定。CBC（採血量≤体重の1%）でヘテロフィル増加・慢性炎症変化を確認。血液生化学でTP上昇・Ca変動・AST上昇を測定。X線で腹腔内石灰化卵殻・軟部組織腫瘤を検出。鳥類の慢性卵黄性腹膜炎は慢性産卵鳥で多発し、卵黄の腹腔内遊離→線維素性被包が慢性経過をたどる"
}

# 197. bird_papillomatosis_–_oral_form — Papillomatosis – Oral Form / 乳頭腫症口腔型
ENRICHMENTS["bird_papillomatosis_–_oral_form"] = {
    "diagnosis_ja": "口腔内の乳頭状〜カリフラワー状腫瘤を口腔内検査で確認。嚥下困難・食欲変化・流涎の臨床評価。病変部の生検・病理組織検査で乳頭腫（papilloma）の組織パターンを確認。PCR検査でPsittacid herpesvirus関連のパピローマウイルスDNAを検出。CBC（採血量≤体重の1%）で全身状態を評価。内視鏡で食道・そのう・総排泄腔への進展を検索。鳥類の口腔乳頭腫症はアマゾン・マコーで好発し、内部乳頭腫症（Internal Papillomatosis）との関連でヘルペスウイルスが疑われている"
}

# 198. bird_avian_herpesvirus_–_internal_papillomatosis — Avian Herpesvirus – Internal Papillomatosis
ENRICHMENTS["bird_avian_herpesvirus_–_internal_papillomatosis"] = {
    "diagnosis_ja": "嘔吐・テネスムス（排便困難）・血便・総排泄腔脱出の臨床評価。総排泄腔検査・内視鏡で消化管内（総排泄腔・食道・そのう・腺胃）の乳頭状腫瘤を確認。生検・病理組織検査で乳頭腫の組織パターンを確認し悪性転化を評価。PCR検査でPsittacid herpesvirus DNAを検出。CBC（採血量≤体重の1%）で貧血（消化管出血）を評価。血液生化学でAST変動を測定。鳥類の内部乳頭腫症はアマゾン・マコー・コニュアに好発し、胆管癌・膵管癌への悪性転化リスクがある"
}

# 199. bird_lead_toxicosis_–_chronic — Lead Toxicosis – Chronic / 鉛中毒慢性型
ENRICHMENTS["bird_lead_toxicosis_–_chronic"] = {
    "diagnosis_ja": "慢性的な体重減少・間欠的嘔吐・多飲多尿・神経症状（痙攣・運動失調・視力低下）の臨床評価。全血鉛濃度測定（正常<20μg/dL、中毒>40μg/dL）。腹部X線で消化管内の金属片（高密度異物）を検索。CBC（採血量≤体重の1%）で貧血（PCV低下）・赤血球の好塩基性斑点を確認。血液生化学でUA上昇（腎障害）・AST上昇を測定。鳥類の慢性鉛中毒は微量の鉛持続摂取で進行し、急性型より神経症状が顕著。鉛含有塗料・はんだ・カーテンウェイトが主要曝露源"
}

# 200. bird_heavy_metal_poisoning_–_mixed_lead_and_zinc — Heavy Metal Poisoning – Mixed
ENRICHMENTS["bird_heavy_metal_poisoning_–_mixed_lead_and_zinc"] = {
    "diagnosis_ja": "急性〜慢性の嘔吐・下痢・多飲多尿・神経症状・貧血の臨床評価。全血鉛濃度（>40μg/dL）および血清亜鉛濃度（>200μg/dL: 中毒域）の測定。腹部X線で消化管内の金属異物を検出。CBC（採血量≤体重の1%）で貧血・赤血球形態異常を確認。血液生化学でUA上昇（腎障害）・膵酵素上昇（亜鉛毒性）を測定。鳥類では亜鉛メッキケージ・はんだ・金属玩具の咬傷が混合重金属中毒の原因であり、鉛と亜鉛の相乗毒性により臨床症状が増悪する。キレーション療法が治療の基本"
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
