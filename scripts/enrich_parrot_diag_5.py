#!/usr/bin/env python3
"""Enrich diagnosis_ja for Parrot entries (batch 5: remaining 53 entries)."""
import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 1. parrot_reovirus_infection — Reovirus Infection / レオウイルス感染症
ENRICHMENTS["parrot_reovirus_infection"] = {
    "diagnosis_ja": "幼鳥の急性肝炎・脾臓壊死・関節炎・下痢からレオウイルス感染を疑う。RT-PCRでAvian Reovirusを検出。ウイルス分離（鶏胚・細胞培養）で確定。血清学的検査（ELISA/AGID）で抗体を検出。CBC/生化学で肝酵素著増・白血球減少を確認。剖検で肝壊死・脾壊死・腱鞘炎を確認。大型オウム類の幼鳥で重症化しやすく、成鳥は不顕性感染で排泄源となる。鑑別にパチェコ病・PDD・ポリオーマを考慮。"
}

# 2. parrot_adenovirus_infection — Adenovirus Infection / アデノウイルス感染症
ENRICHMENTS["parrot_adenovirus_infection"] = {
    "diagnosis_ja": "急性肝炎・消化管出血・沈鬱・突然死からアデノウイルス感染を疑う。PCRでAvian Adenovirusを検出。肝生検で好塩基性核内封入体（大型で特徴的）を確認。ウイルス分離で確定。CBC/生化学で肝酵素著増・凝固異常・白血球減少を評価。剖検で肝腫大・点状出血・腸管出血を確認。大型オウム類の幼鳥で致死的経過をとることがあり、成鳥の不顕性感染が感染源となる。鑑別にパチェコ病・レオウイルス・PBFDを考慮。"
}

# 3. parrot_avian_malaria_plasmodium_spp. — Avian Malaria / 鳥マラリア
ENRICHMENTS["parrot_avian_malaria_plasmodium_spp."] = {
    "diagnosis_ja": "沈鬱・食欲不振・貧血・脾腫・呼吸困難から鳥マラリアを疑う。血液塗抹のギムザ染色でPlasmodium属の赤血球内ガメトサイト・メロゾイトを確認。PCRで種特定（P. relictum等）。CBC/生化学で再生性貧血（PCV低下）・肝酵素上昇を確認。剖検で脾腫・肝腫大・ヘモジデリン沈着を確認。蚊媒介感染であり、屋外飼育・蚊の季節性・地域の流行状況を聴取。大型オウム類（特に旧世界種）は感受性が高く急性経過で死亡しうる。"
}

# 4. parrot_haemoproteus_infection — Haemoproteus Infection / ヘモプロテウス症
ENRICHMENTS["parrot_haemoproteus_infection"] = {
    "diagnosis_ja": "軽度の貧血・沈鬱・食欲不振からヘモプロテウス症を疑う。血液塗抹のギムザ染色でHaemoproteus属の特徴的なハルテレ形ガメトサイト（赤血球内の半月形寄生体）を確認。PCRで種特定。CBC/生化学で軽度貧血・肝酵素上昇を評価。Plasmodium（鳥マラリア）との鑑別が重要で、赤血球内メロゾイトの有無で区別。ヌカカ（Culicoides）媒介であり、屋外飼育歴を聴取。大型オウム類では通常軽症だが、免疫抑制状態で重症化しうる。"
}

# 5. parrot_cryptosporidiosis — Cryptosporidiosis / クリプトスポリジウム症
ENRICHMENTS["parrot_cryptosporidiosis"] = {
    "diagnosis_ja": "慢性下痢・体重減少・呼吸器症状（鳥類では呼吸器型も多い）からクリプトスポリジウム症を疑う。糞便の酸抗性染色（Ziehl-Neelsen変法）でオーシストを検出。糞便PCRでCryptosporidium種を確認。そ嚢洗浄液・気管洗浄液の検査で呼吸器型を診断。組織生検で消化管・呼吸器上皮表面の寄生体を確認。CBC/生化学で低蛋白血症・電解質異常を評価。大型オウム類では免疫抑制（PBFD等）が合併すると慢性難治性となる。"
}

# 6. parrot_hexamitiasis_spironucleosis — Hexamitiasis / ヘキサミタ症
ENRICHMENTS["parrot_hexamitiasis_spironucleosis"] = {
    "diagnosis_ja": "慢性下痢・体重減少・羽毛粗剛・削痩からヘキサミタ症を疑う。新鮮糞便の直接塗抹で特徴的な鞭毛運動を示すSpironucleus/Hexamita栄養体を確認（温度維持が重要）。糞便PCRで確定。そ嚢洗浄液にも栄養体が検出される場合がある。CBC/生化学で低蛋白血症・脱水を評価。大型オウム類ではストレス・免疫低下時に増殖し臨床症状を呈する。鑑別にジアルジア・トリコモナス・コクシジウムを考慮する。"
}

# 7. parrot_toxoplasmosis — Toxoplasmosis / トキソプラズマ症
ENRICHMENTS["parrot_toxoplasmosis"] = {
    "diagnosis_ja": "急性神経症状（運動失調・振戦・旋回）・沈鬱・呼吸困難・突然死からトキソプラズマ症を疑う。血清学的検査（IFA・ELISA）でToxoplasma gondii抗体を検出。組織PCRで病原体DNAを確認。剖検・生検で脳・肝・肺の壊死性炎症とタキゾイトを確認。CBC/生化学で白血球増多・肝酵素上昇を評価。猫（終宿主）との接触歴・オーシスト汚染環境への曝露を聴取。大型オウム類は中間宿主として感受性が高く急性致死的経過をとりうる。"
}

# 8. parrot_capillariasis_hairworm — Capillariasis / 毛細線虫症
ENRICHMENTS["parrot_capillariasis_hairworm"] = {
    "diagnosis_ja": "体重減少・食欲不振・口腔内白色病変・下痢からCapillaria感染を疑う。糞便浮遊法で特徴的な両端栓（bipolar plug）を持つ樽型虫卵を検出。口腔・そ嚢の肉眼検査で粘膜の肥厚・白色斑（虫体穿入部）を確認。内視鏡でそ嚢・食道粘膜の虫体を直接観察。CBC/生化学で好酸球増多・低蛋白血症を評価。ミミズが中間宿主となる種があり屋外飼育歴を聴取。大型オウム類では上部消化管型が多く、重度感染で削痩・貧血を呈する。"
}

# 9. parrot_syngamus_gapeworm — Syngamus (Gapeworm) / 気管虫症
ENRICHMENTS["parrot_syngamus_gapeworm"] = {
    "diagnosis_ja": "開口呼吸・呼吸困難・頭振り・咳嗽様動作からSyngamus trachea（気管虫）感染を疑う。気管内視鏡で気管内のY字型交尾虫体を直接確認し確定。糞便浮遊法で楕円形の厚殻虫卵を検出。X線で気管内軟部組織陰影を確認。CBC/生化学で好酸球増多を評価。中間宿主（ミミズ・カタツムリ）への曝露歴を聴取。屋外飼育・地面との接触がリスク因子。大型オウム類では重度感染で気道閉塞を起こし致死的となりうる。"
}

# 10. parrot_mycoplasmosis — Mycoplasmosis / マイコプラズマ症
ENRICHMENTS["parrot_mycoplasmosis"] = {
    "diagnosis_ja": "慢性呼吸器症状（くしゃみ・鼻汁・副鼻腔腫脹）・結膜炎から鳥マイコプラズマ症を疑う。気管・鼻腔スワブのPCRでMycoplasma属を検出。培養は特殊培地（PPLO培地）が必要で時間を要する。血清学的検査（急性期・回復期のペア血清）で抗体上昇を確認。CBC/生化学でヘテロフィル軽度増多を確認。X線で副鼻腔の液体貯留を評価。他の呼吸器病原体（Chlamydia・Aspergillus）との混合感染を除外。大型オウム類では慢性経過をたどりやすい。"
}

# 11. parrot_pseudomonas_infection — Pseudomonas Infection / 緑膿菌感染症
ENRICHMENTS["parrot_pseudomonas_infection"] = {
    "diagnosis_ja": "慢性副鼻腔炎・耳炎・皮膚感染・敗血症から緑膿菌感染を疑う。患部の培養・感受性試験でPseudomonas aeruginosaを分離同定。グラム染色でグラム陰性桿菌を確認。CBC/生化学でヘテロフィル増多・肝酵素上昇を評価。正常なオウム類の消化管はグラム陽性菌優勢であり、緑膿菌検出は病的意義が高い。多剤耐性株が多く感受性試験が治療方針決定に不可欠。大型オウム類では水飲み場・環境の衛生管理歴を聴取する。"
}

# 12. parrot_bordetella_infection — Bordetella Infection / ボルデテラ感染症
ENRICHMENTS["parrot_bordetella_infection"] = {
    "diagnosis_ja": "急性呼吸器症状（くしゃみ・鼻汁・喘鳴・呼吸困難）からBordetella avium感染を疑う。気管・鼻腔スワブの培養でBordetella属を分離同定。PCRで迅速検出。気管洗浄液の細胞診でヘテロフィル浸潤を確認。CBC/生化学でヘテロフィル増多を評価。X線で気管壁肥厚・肺野陰影を確認。幼鳥で重症化しやすく気管虚脱を合併しうる。大型オウム類では他の呼吸器病原体（Chlamydia・Aspergillus・Mycoplasma）との混合感染を除外する。"
}

# 13. parrot_pasteurellosis — Pasteurellosis / パスツレラ症
ENRICHMENTS["parrot_pasteurellosis"] = {
    "diagnosis_ja": "猫・齧歯類による咬傷後の急性敗血症・突然死からパスツレラ症を疑う。血液培養・創傷培養でPasteurella multocidaを分離同定。CBC/生化学でヘテロフィル著増・肝酵素上昇・凝固異常を評価。剖検で多臓器の出血性壊死・敗血症所見を確認。咬傷歴（特に猫の口腔内常在菌として高率に保菌）の聴取が診断の鍵。大型オウム類では猫との同居環境が最大のリスク因子であり、軽微な咬傷でも数時間〜24時間以内に致死的敗血症に進展しうる。"
}

# 14. parrot_erysipelas — Erysipelas / 丹毒
ENRICHMENTS["parrot_erysipelas"] = {
    "diagnosis_ja": "急性敗血症・皮膚の暗赤色斑・沈鬱・突然死から丹毒を疑う。血液培養・臓器培養でErysipelothrix rhusiopathiaeを分離同定。グラム染色で細いグラム陽性桿菌を確認。CBC/生化学でヘテロフィル著増・肝酵素上昇を評価。剖検で脾腫・肝腫大・皮膚の出血性壊死を確認。環境中の汚染源（魚粉飼料・土壌）への曝露歴を聴取。人獣共通感染症であり取扱い注意。大型オウム類では急性致死的経過をたどることが多い。"
}

# 15. parrot_mucormycosis_zygomycosis — Mucormycosis / ムコール症
ENRICHMENTS["parrot_mucormycosis_zygomycosis"] = {
    "diagnosis_ja": "呼吸困難・副鼻腔腫脹・皮膚壊死性病変から接合菌症（ムコール症）を疑う。病変部の直接鏡検でKOH処理後に太く分岐の少ない無隔壁菌糸を確認。培養でRhizopus・Mucor等を同定。組織生検でPAS・GMS染色陽性の菌糸と血管浸潤・組織壊死を確認。CBC/生化学でヘテロフィル増多を評価。CT検査で骨破壊・深部組織浸潤を精査。免疫抑制（PBFD・慢性ストレス）が重要な素因。大型オウム類では環境中のカビ胞子への高濃度曝露で発症リスク上昇。"
}

# 16. parrot_dermatophytosis_ringworm — Dermatophytosis / 皮膚糸状菌症
ENRICHMENTS["parrot_dermatophytosis_ringworm"] = {
    "diagnosis_ja": "環状脱羽・鱗状痂皮・嘴/脚部の白色粉状病変から皮膚糸状菌症を疑う。患部のKOH直接鏡検で菌糸・分節胞子を確認。DTM培地での培養でMicrosporum/Trichophyton属を同定。ウッド灯検査で一部のM. canisが蛍光を示す。皮膚生検でPAS染色陽性の毛包内菌糸を確認。CBC/生化学で基礎疾患（免疫抑制）を評価。大型オウム類では高湿度環境が素因となり、人獣共通感染症として飼い主への感染リスクにも注意する。"
}

# 17. parrot_histoplasmosis — Histoplasmosis / ヒストプラズマ症
ENRICHMENTS["parrot_histoplasmosis"] = {
    "diagnosis_ja": "呼吸困難・体重減少・肝脾腫・下痢からヒストプラズマ症を疑う。組織生検（肝・脾・肺）のGMS・PAS染色で小型酵母（2-4μm）のマクロファージ内寄生を確認。培養でHistoplasma capsulatumを同定（BSL-3施設必要）。尿中・血清中抗原検査（EIA）。PCRで確定。CBC/生化学で貧血・肝酵素上昇・低蛋白血症を評価。鳥糞が蓄積する環境（洞窟・古建築物）への曝露歴を聴取。鳥類自体は感受性が低いが保菌・環境散布源となりうる。"
}

# 18. parrot_mycotic_pneumonia — Mycotic Pneumonia / 真菌性肺炎
ENRICHMENTS["parrot_mycotic_pneumonia"] = {
    "diagnosis_ja": "呼吸困難・開口呼吸・尾振り呼吸・運動不耐性から真菌性肺炎を疑う。X線・CTで肺野結節影・気嚢壁肥厚・びまん性陰影を評価。気管洗浄液の細胞診でマクロファージ内の真菌菌糸・胞子を確認。培養でAspergillus fumigatus等を同定。β-D-グルカン・ガラクトマンナン抗原で補助的診断。内視鏡で気嚢内の白色プラークを直視下確認。CBC/生化学でヘテロフィル増多・低アルブミンを評価。大型オウム類は気嚢系が発達しており真菌感染が拡散しやすい。"
}

# 19. parrot_valvular_heart_disease — Valvular Heart Disease / 心臓弁膜症
ENRICHMENTS["parrot_valvular_heart_disease"] = {
    "diagnosis_ja": "運動不耐性・呼吸困難・チアノーゼ・腹水から心臓弁膜症を疑う。聴診で心雑音を検出。X線で心陰影拡大・肺うっ血を評価。超音波心臓検査（心エコー）で弁の形態異常・逆流・心腔拡大を確認。ドプラーで逆流の重症度を定量。CBC/生化学で肝酵素上昇（右心不全による肝うっ血）を確認。心電図で不整脈を検出。大型オウム類は長寿命（20-80年）のため加齢性弁膜変性が多く、動脈硬化症との合併に注意する。"
}

# 20. parrot_aortic_rupture — Aortic Rupture / 大動脈破裂
ENRICHMENTS["parrot_aortic_rupture"] = {
    "diagnosis_ja": "突然死・急性虚脱・呼吸困難からの急死で大動脈破裂を疑う。剖検で大動脈壁の破裂部位と体腔内大量出血を確認し確定。病理組織検査で動脈硬化性プラーク・中膜壊死を評価。血中コレステロール・トリグリセリド値で脂質代謝異常を評価（生前）。X線で大動脈石灰化を確認。超音波で動脈壁肥厚・プラークを検出。大型オウム類（特にヨウム・アマゾン）は動脈硬化症の好発種であり、高脂肪食・運動不足が主要なリスク因子。"
}

# 21. parrot_coelomic_effusion_ascites — Coelomic Effusion / 体腔液貯留
ENRICHMENTS["parrot_coelomic_effusion_ascites"] = {
    "diagnosis_ja": "腹部膨満・呼吸困難・体重変化から体腔液貯留を疑う。X線で腹腔内液体陰影・臓器辺縁の不明瞭化を確認。超音波で液体の量・分布・内部エコーを評価。診断的腹腔穿刺で液体を採取し、細胞診（漏出液vs滲出液vs変性漏出液）・培養・生化学分析を実施。CBC/生化学で低蛋白血症・肝酵素上昇・腎機能障害を評価。原因疾患（心不全・肝疾患・卵黄性腹膜炎・腫瘍・感染症）の鑑別が不可欠。大型オウム類では卵管疾患と肝疾患が最多原因。"
}

# 22. parrot_hepatic_amyloidosis — Hepatic Amyloidosis / 肝アミロイドーシス
ENRICHMENTS["parrot_hepatic_amyloidosis"] = {
    "diagnosis_ja": "慢性体重減少・肝腫大・腹水・沈鬱から肝アミロイドーシスを疑う。生化学で肝酵素上昇（AST・LDH）・低アルブミン血症・胆汁酸上昇を確認。X線・超音波で肝腫大・エコー輝度変化を評価。肝生検のコンゴレッド染色で偏光顕微鏡下にアップルグリーンの複屈折を示すアミロイド沈着を確認し確定。CBC/生化学で貧血・凝固異常を評価。大型オウム類（特にアヒル科・アマゾン）では慢性炎症性疾患に続発するAA型アミロイドーシスが多い。"
}

# 23. parrot_proventricular_ulceration — Proventricular Ulceration / 腺胃潰瘍
ENRICHMENTS["parrot_proventricular_ulceration"] = {
    "diagnosis_ja": "嘔吐（血液混入）・タール便・食欲不振・体重減少から腺胃潰瘍を疑う。X線で前胃壁の不整・ガス像を確認。造影X線で粘膜面の充満欠損を描出。内視鏡で前胃粘膜の潰瘍・びらん・出血を直視下確認し生検を採取。病理組織検査で潰瘍の深達度・腫瘍性病変を評価。CBC/生化学で貧血・低蛋白血症を確認。ABV-PCRでPDDを除外。大型オウム類ではNSAIDs投与・ストレス・重金属中毒・Megabacteriaが潰瘍の原因となる。"
}

# 24. parrot_tracheal_stenosis — Tracheal Stenosis / 気管狭窄症
ENRICHMENTS["parrot_tracheal_stenosis"] = {
    "diagnosis_ja": "吸気性喘鳴・呼吸困難・運動不耐性から気管狭窄症を疑う。X線で気管内腔の局所的狭窄を確認。CT検査で狭窄の範囲・程度を精密に評価。気管内視鏡で狭窄部位を直視下確認し、肉芽腫・瘢痕・腫瘤を鑑別。気管洗浄液の培養・細胞診で感染性原因を評価。CBC/生化学でヘテロフィル増多を確認。先天性（完全気管輪異常）と後天性（挿管後瘢痕・感染・異物）を鑑別。大型オウム類（特にアマゾン）では気管の解剖学的特徴から好発する。"
}

# 25. parrot_pulmonary_edema — Pulmonary Edema / 肺水腫
ENRICHMENTS["parrot_pulmonary_edema"] = {
    "diagnosis_ja": "急性呼吸困難・チアノーゼ・湿性ラ音・開口呼吸から肺水腫を疑う。X線で肺野のびまん性陰影増強・気管支周囲のカフィング像を確認。超音波心臓検査で心不全の有無を評価。血液ガス分析で低酸素血症を確認。CBC/生化学で低蛋白血症・腎機能障害・心筋マーカーを評価。原因鑑別（心原性 vs 非心原性：中毒・感染・吸入障害）が治療方針決定に不可欠。大型オウム類ではPTFE中毒による急性肺水腫が致死率極めて高い。気嚢系の評価も必要。"
}

# 26. parrot_air_sac_rupture — Air Sac Rupture / 気嚢破裂
ENRICHMENTS["parrot_air_sac_rupture"] = {
    "diagnosis_ja": "皮下気腫（頸部・胸部の風船状膨張）・呼吸困難から気嚢破裂を疑う。視診・触診で皮下の捻髪感（気腫）を確認。X線で皮下気腫・縦隔気腫・気嚢の異常ガス像を確認。透視検査で呼吸動態と破裂部位を推定。内視鏡で気嚢壁の裂傷を直視下確認。CBC/生化学で基礎感染を評価。外傷歴（衝突・過度の保定）を聴取。大型オウム類は気嚢システムが発達しているため破裂時の皮下気腫が顕著で、頸部気嚢・鎖骨間気嚢が好発部位。"
}

# 27. parrot_hemangiosarcoma — Hemangiosarcoma / 血管肉腫
ENRICHMENTS["parrot_hemangiosarcoma"] = {
    "diagnosis_ja": "急性虚脱・貧血・腹腔内出血・皮膚の暗赤色腫瘤から血管肉腫を疑う。X線・超音波で肝・脾の腫瘤・腹腔液貯留を確認。FNA細胞診で紡錘形〜多形性の腫瘍細胞と血液成分を確認。組織生検で不規則な血管腔形成と内皮細胞の異型性を確定。CBC/生化学で貧血・血小板減少・肝酵素上昇を評価。凝固検査でDICの合併を確認。CT検査で転移の有無を精査。大型オウム類では長寿命のため悪性腫瘍の発生率が高い。"
}

# 28. parrot_melanoma — Melanoma / メラノーマ
ENRICHMENTS["parrot_melanoma"] = {
    "diagnosis_ja": "皮膚・口腔粘膜・眼瞼の黒色〜暗褐色の腫瘤・色素沈着病変からメラノーマを疑う。FNA細胞診でメラニン顆粒を含む紡錘形〜多形性腫瘍細胞を確認。組織生検で確定し悪性度（核分裂像・浸潤パターン）を評価。免疫組織化学（Melan-A・S-100）で確認。X線・超音波で内臓転移を精査。CBC/生化学で全身状態を評価。大型オウム類では皮膚型が多く、嘴基部・眼周囲に好発。長寿命種のため経年変化する色素病変のモニタリングが重要。"
}

# 29. parrot_osteosarcoma — Osteosarcoma / 骨肉腫
ENRICHMENTS["parrot_osteosarcoma"] = {
    "diagnosis_ja": "脚部・翼の腫脹・跛行・病的骨折から骨肉腫を疑う。X線で骨溶解性〜骨産生性の混合パターン・periosteal reactionを確認。CT検査で腫瘤の範囲と軟部組織浸潤を精査。FNA細胞診で骨基質を産生する腫瘍細胞を確認。組織生検で確定し組織亜型を分類。X線（全身）で肺転移を評価。CBC/生化学でALP上昇・Ca異常を確認。大型オウム類では長寿命のため骨腫瘍の発生率が比較的高く、脛足根骨・上腕骨に好発する。"
}

# 30. parrot_cholangiocellular_carcinoma — Cholangiocellular Carcinoma / 胆管細胞癌
ENRICHMENTS["parrot_cholangiocellular_carcinoma"] = {
    "diagnosis_ja": "慢性体重減少・腹部膨満・沈鬱・黄色〜緑色尿酸塩排泄から胆管細胞癌を疑う。超音波で肝内の腫瘤・胆管拡張を確認。X線で肝腫大を評価。FNA細胞診で腺管構造を形成する腫瘍細胞を確認。組織生検で確定し胆管上皮由来を確認。CBC/生化学で肝酵素著増（ALP・GGT・AST）・胆汁酸上昇・高ビリルビン血症を評価。CT検査で転移を精査。大型オウム類（特にアマゾン）では慢性ヘルペスウイルス（内部乳頭腫症）からの悪性転化が報告されている。"
}

# 31. parrot_thyroid_carcinoma — Thyroid Carcinoma / 甲状腺癌
ENRICHMENTS["parrot_thyroid_carcinoma"] = {
    "diagnosis_ja": "頸部腫瘤・嚥下困難・呼吸困難・体重変化から甲状腺癌を疑う。X線で頸部軟部組織腫瘤・気管偏位を確認。超音波で甲状腺の腫大・内部構造異常を評価。FNA細胞診で腫瘍細胞を確認。組織生検で確定し組織亜型（濾胞癌・乳頭癌等）を分類。甲状腺機能検査（T4）で機能性腫瘍の有無を評価。CBC/生化学で高Ca血症を確認。CT検査で局所浸潤・遠隔転移を精査。大型オウム類では慢性ヨウ素欠乏が甲状腺腫瘍の素因となりうる。"
}

# 32. parrot_preen_gland_tumor — Preen Gland Tumor / 尾脂腺腫瘍
ENRICHMENTS["parrot_preen_gland_tumor"] = {
    "diagnosis_ja": "尾部背側の尾脂腺部位の腫瘤・腫大・変形を視診で確認。FNA細胞診で腫瘍細胞の性状（腺癌 vs 腺腫 vs 扁平上皮癌）を評価。組織生検で確定し悪性度を判定。X線・超音波で局所浸潤・遠隔転移を精査。CBC/生化学で全身状態を評価。尾脂腺は鳥類で唯一の外分泌腺であり、腫大・分泌物異常・出血は腫瘍を疑う所見。大型オウム類ではアマゾン属で腺癌の発生が報告されている。鑑別に膿瘍・嚢胞・肉芽腫を考慮する。"
}

# 33. parrot_reproductive_tract_infection_salpingitis — Reproductive Tract Infection (Salpingitis) / 卵管炎
ENRICHMENTS["parrot_reproductive_tract_infection_salpingitis"] = {
    "diagnosis_ja": "雌鳥の腹部膨満・沈鬱・食欲不振・産卵停止・クロアカ排泄物異常から卵管炎を疑う。X線・超音波で卵管腫大・腹腔液貯留・卵殻異常を確認。腹腔穿刺で膿性〜卵黄混濁液を採取し培養・感受性試験を実施。CBC/生化学でヘテロフィル著増・高Ca血症・肝酵素上昇を評価。E. coliが最も一般的な起因菌。慢性産卵・卵管脱の既往が素因。大型オウム類（特に単独飼育雌）では慢性産卵に伴う卵管炎が多く、卵黄性腹膜炎への進展に注意。"
}

# 34. parrot_feather_follicle_cyst_chronic — Feather Follicle Cyst (Chronic) / 慢性羽包嚢胞
ENRICHMENTS["parrot_feather_follicle_cyst_chronic"] = {
    "diagnosis_ja": "皮下の膨隆・腫瘤（ケラチン・羽毛片を含む嚢胞）を触診・視診で確認。FNA細胞診でケラチン物質・変性羽毛組織を確認し腫瘍を除外。組織生検で嚢胞壁の扁平上皮裏層と内腔のケラチンを確認し確定。X線で皮下軟部組織腫瘤を評価。CBC/生化学で基礎疾患を除外。二次感染時は培養・感受性試験を実施。大型オウム類では翼・胸部の羽包で好発し、外傷・PBFD・慢性炎症が嚢胞形成の素因。再発率が高く外科的完全摘出が推奨される。"
}

# 35. parrot_nutritional_secondary_hyperparathyroidism — Nutritional Secondary Hyperparathyroidism / 栄養性二次性上皮小体機能亢進症
ENRICHMENTS["parrot_nutritional_secondary_hyperparathyroidism"] = {
    "diagnosis_ja": "骨軟化・病的骨折・嘴軟化・けいれん（低Ca血症）から栄養性二次性上皮小体機能亢進症を疑う。血清Ca低値・P上昇・ALP上昇を確認。PTH測定で上皮小体機能亢進を評価。X線で全身性骨密度低下・皮質菲薄化・病的骨折を確認。食餌歴の詳細聴取（Ca:P比不均衡・種子食偏重・ビタミンD3不足）が診断の核心。UVB照射不足の有無を確認。大型オウム類（特にヨウム・コンゴウインコ）の室内飼育鳥で好発する。"
}

# 36. parrot_vitamin_e___selenium_deficiency — Vitamin E / Selenium Deficiency / ビタミンE・セレン欠乏症
ENRICHMENTS["parrot_vitamin_e___selenium_deficiency"] = {
    "diagnosis_ja": "筋力低下・運動失調・白色筋症・免疫低下からビタミンE・セレン欠乏を疑う。血清ビタミンE・セレン濃度測定で確認。CK・AST上昇で筋障害を評価。CBC/生化学で貧血・免疫グロブリン低値を確認。組織生検で白色筋症（筋線維のZenker変性・石灰化）を確認。食餌歴（古い種子・酸化脂肪の摂取・ペレット未使用）の聴取が重要。大型オウム類では種子食偏重で酸化脂肪によるビタミンE消費亢進が主因。鑑別に多発性神経炎・PDD・重金属中毒を考慮。"
}

# 37. parrot_vitamin_k_deficiency — Vitamin K Deficiency / ビタミンK欠乏症
ENRICHMENTS["parrot_vitamin_k_deficiency"] = {
    "diagnosis_ja": "自発性出血（皮下出血・血便・出血斑）・凝固時間延長からビタミンK欠乏を疑う。凝固検査でPT延長（APTT正常〜延長）を確認。ビタミンK投与後の凝固時間改善で診断的治療が確定的。CBC/生化学で貧血を確認。X線で消化管出血・金属異物を除外。抗凝固薬（殺鼠剤・ワルファリン）への曝露歴を聴取。長期抗生物質投与による腸内細菌叢破壊（ビタミンK産生低下）も原因となる。鑑別に殺鼠剤中毒・肝不全・DICを考慮する。"
}

# 38. parrot_thiamine_deficiency — Thiamine Deficiency / チアミン欠乏症
ENRICHMENTS["parrot_thiamine_deficiency"] = {
    "diagnosis_ja": "神経症状（運動失調・後弓反張・けいれん・星座凝視姿勢）・脚麻痺からチアミン（ビタミンB1）欠乏を疑う。血中チアミン濃度または赤血球トランスケトラーゼ活性測定で確認。チアミン投与後の劇的な症状改善（数時間以内）で診断的治療が確定的。CBC/生化学で乳酸アシドーシスを評価。食餌歴（加熱処理過多・チアミナーゼ含有魚の摂取・古い飼料）を聴取。大型オウム類では不適切な食餌管理が主因。鑑別にPDD・重金属中毒・低Ca血症を考慮。"
}

# 39. parrot_biotin_deficiency — Biotin Deficiency / ビオチン欠乏症
ENRICHMENTS["parrot_biotin_deficiency"] = {
    "diagnosis_ja": "皮膚炎・羽毛異常（脱羽・発育不良・変色）・嘴/脚の鱗状痂皮からビオチン欠乏を疑う。血清ビオチン濃度測定で確認。ビオチン補給後の症状改善で診断的治療が確定的。CBC/生化学で基礎疾患を除外。食餌歴の聴取で生卵白（アビジンがビオチンに結合）の摂取、不適切な食餌構成を確認。大型オウム類では種子食偏重・ペレット未使用が主因。鑑別にPBFD・甲状腺機能低下症・亜鉛欠乏・皮膚糸状菌症を考慮する。"
}

# 40. parrot_hypervitaminosis_d — Hypervitaminosis D / ビタミンD過剰症
ENRICHMENTS["parrot_hypervitaminosis_d"] = {
    "diagnosis_ja": "多飲多尿・食欲不振・削痩・軟部組織石灰化からビタミンD過剰症を疑う。血清Ca著増・P上昇・25(OH)D3高値を確認。X線で軟部組織（腎・血管・消化管）の石灰化を評価。超音波で腎石灰化・腎腫大を確認。CBC/生化学でBUN/UA上昇（腎障害）を確認。サプリメント・ペレットの過剰投与歴・UVBランプの過度使用を聴取。大型オウム類では飼い主の善意による過剰サプリメントが主因。鑑別に腎疾患・上皮小体腫瘍を考慮する。"
}

# 41. parrot_protein_deficiency — Protein Deficiency / タンパク質欠乏症
ENRICHMENTS["parrot_protein_deficiency"] = {
    "diagnosis_ja": "羽毛異常（ストレスバー・変色・脆弱・脱羽）・筋萎縮・成長遅延・免疫低下からタンパク質欠乏を疑う。生化学で低アルブミン血症・低総蛋白を確認。CBC/生化学でリンパ球減少（免疫低下）を評価。食餌歴の詳細聴取（種子食偏重：タンパク質含有量不足、必須アミノ酸欠乏）が診断の核心。羽毛分析でアミノ酸組成異常を評価可能。大型オウム類ではメチオニン・リジン等の含硫アミノ酸欠乏が羽毛品質に直接影響する。"
}

# 42. parrot_rodenticide_poisoning — Rodenticide Poisoning / 殺鼠剤中毒
ENRICHMENTS["parrot_rodenticide_poisoning"] = {
    "diagnosis_ja": "自発性出血（皮下出血・血便・クロアカ出血）・沈鬱・虚脱から抗凝固性殺鼠剤中毒を疑う。凝固検査でPT・APTT著延長を確認。ビタミンK1投与後の凝固時間改善で診断的治療が確定的。CBC/生化学で貧血（出血性）を確認。環境での殺鼠剤使用歴・中毒したネズミへの接触歴を聴取。血中抗凝固薬濃度測定（専門ラボ）で確定可能。第二世代抗凝固薬（ブロジファコウム等）は半減期が長く長期治療が必要。鑑別に肝不全・DICを考慮。"
}

# 43. parrot_essential_oil_toxicity — Essential Oil Toxicity / エッセンシャルオイル中毒
ENRICHMENTS["parrot_essential_oil_toxicity"] = {
    "diagnosis_ja": "エッセンシャルオイル・アロマディフューザーへの曝露後の呼吸困難・沈鬱・運動失調・嘔吐から中毒を疑う。曝露歴（使用製品・期間・換気状況）の詳細聴取が診断の核心。鳥類は気嚢システムにより揮発性有機化合物の感受性が哺乳類より極めて高い。CBC/生化学で肝酵素上昇・腎機能障害を評価。X線で肺野浮腫を確認。ティーツリー・ペパーミント・ユーカリ等のフェノール系成分は特に肝毒性が強い。原因物質除去と支持療法による改善で臨床的に確認。"
}

# 44. parrot_myiasis_fly_strike — Myiasis (Fly Strike) / 蝿蛆症
ENRICHMENTS["parrot_myiasis_fly_strike"] = {
    "diagnosis_ja": "創傷部位・クロアカ周囲・皮膚損傷部の蛆虫（幼虫）を視診で確認し診断。幼虫の形態学的特徴から蝿種を同定。創傷の深達度・組織壊死の範囲を評価。培養・感受性試験で二次細菌感染を確認。CBC/生化学で炎症マーカー・敗血症所見を評価。屋外飼育・不衛生な環境・開放創・クロアカ汚染が素因。大型オウム類では自咬による皮膚損傷部や下痢によるクロアカ周囲汚染が蝿の産卵誘因となる。早期発見・幼虫除去が重要。"
}

# 45. parrot_tick_infestation — Tick Infestation / ダニ寄生症
ENRICHMENTS["parrot_tick_infestation"] = {
    "diagnosis_ja": "羽毛間・皮膚のダニ虫体を視診・拡大鏡検で確認。虫体の形態学的特徴でダニ種を同定（マダニ・ワクモ・トリサシダニ等）。CBC/生化学で貧血（大量寄生時）・好酸球増多を評価。血液塗抹でダニ媒介性血液寄生虫（Borrelia・Anaplasma等）を確認。環境検査でケージ・止まり木のダニ汚染を確認。屋外飼育歴・野鳥との接触歴を聴取。大型オウム類では夜間吸血するワクモ（Dermanyssus gallinae）が問題となりやすい。"
}

# 46. parrot_subcutaneous_emphysema — Subcutaneous Emphysema / 皮下気腫
ENRICHMENTS["parrot_subcutaneous_emphysema"] = {
    "diagnosis_ja": "皮下の風船状膨張・捻髪感から皮下気腫を視診・触診で確認。X線で皮下ガス像・気嚢の破損部位を評価。透視検査で呼吸動態と空気漏出部位を推定。CT検査で気嚢壁の裂傷部位を精密に特定。内視鏡で気嚢壁損傷を直視下確認。CBC/生化学で基礎感染を評価。外傷歴（衝突・過度の保定・犬猫による咬傷）を聴取。気嚢系の広範な連通により空気が皮下に拡散。穿刺による一時的減圧と原因部位の修復が治療の核心。"
}

# 47. parrot_ingluvoliths_crop_stones — Ingluvoliths (Crop Stones) / 素嚢結石
ENRICHMENTS["parrot_ingluvoliths_crop_stones"] = {
    "diagnosis_ja": "そ嚢の膨満・触診での硬い異物触知・食欲不振・嘔吐からそ嚢結石を疑う。X線でそ嚢内の高密度腫瘤影を確認。造影X線でそ嚢通過障害を評価。そ嚢の触診で結石の大きさ・数・硬度を評価。内視鏡でそ嚢内の結石を直視下確認。CBC/生化学で脱水・低蛋白血症を評価。そ嚢うっ滞の基礎疾患（PDD・神経障害・異物摂取）を鑑別。大型オウム類ではそ嚢運動機能低下による食餌残渣の石灰化が原因。外科的摘出が適応となることが多い。"
}

# 48. parrot_copper_poisoning — Copper Poisoning / 銅中毒
ENRICHMENTS["parrot_copper_poisoning"] = {
    "diagnosis_ja": "急性嘔吐・緑色下痢・沈鬱・溶血性貧血から銅中毒を疑う。血中銅濃度測定で確認。CBC/生化学で溶血性貧血（PCV低下・ビリベルジン上昇）・肝酵素著増・腎機能障害を評価。X線で消化管内の金属異物を確認。肝生検で銅沈着（ロダニン染色陽性）を確認。銅含有製品（銅線・銅貨・銅製飼育器具）への曝露歴を聴取。大型オウム類は嘴が強力で金属片を容易に摂取しうる。鑑別に鉛中毒・亜鉛中毒を考慮する。"
}

# 49. parrot_nail_overgrowth___injury — Nail Overgrowth / Injury / 爪過長・損傷
ENRICHMENTS["parrot_nail_overgrowth___injury"] = {
    "diagnosis_ja": "爪の過度な伸長・変形・出血・脱落を視診で確認。止まり木や指への引っかかりによる外傷の有無を評価。出血爪では血管・神経の損傷範囲を確認。X線で趾骨の骨折・骨病変（痛風・腫瘍）を除外。CBC/生化学で基礎疾患（肝疾患・栄養欠乏）を評価。爪過長の原因として不適切な止まり木（滑らかすぎる素材）・運動不足を聴取。大型オウム類では定期的な爪のトリミングが必要で、血管の位置確認が重要。"
}

# 50. parrot_wing_tip_edema — Wing Tip Edema / 翼端浮腫
ENRICHMENTS["parrot_wing_tip_edema"] = {
    "diagnosis_ja": "翼端（初列風切羽基部）の腫脹・浮腫・変色から翼端浮腫を疑う。視診・触診で浮腫の範囲・温度・疼痛を評価。X線で骨折・骨膜反応・骨溶解を除外。超音波で軟部組織の液体貯留を確認。CBC/生化学で低蛋白血症・肝酵素異常・腎機能障害を評価。心臓超音波で右心不全（うっ血性）を除外。循環障害・外傷（バンド・リング等による絞扼）の有無を確認。大型オウム類では翼クリッピング後の不適切な止血や外傷が原因となることが多い。"
}

# 51. parrot_avian_nephropathy — Avian Nephropathy / 鳥腎症
ENRICHMENTS["parrot_avian_nephropathy"] = {
    "diagnosis_ja": "多飲多尿・脚麻痺（腎腫大による坐骨神経圧迫）・痛風結節・沈鬱から鳥腎症を疑う。生化学でUA著増・Ca/P異常・電解質異常を確認。X線で腎腫大・腎石灰化を評価。超音波で腎実質のエコー変化・構造異常を確認。尿検査で尿酸塩結晶の異常排泄パターンを評価。腎生検で間質性腎炎・痛風結節・腎腫瘍・アミロイド沈着を鑑別し確定。大型オウム類（特にヨウム）では腎腫瘍が好発し、長寿命のため慢性腎疾患の発生率が高い。"
}

# 52. parrot_fracture_wing — Wing Fracture (Parrot) / 翼骨折（オウム類）
ENRICHMENTS["parrot_fracture_wing"] = {
    "diagnosis_ja": "翼の下垂・非対称姿勢・飛行不能・腫脹・疼痛から翼骨折を疑う。触診で骨折部位の軋轢音・異常可動性を確認。X線（2方向：VD・lateral）で骨折の部位（上腕骨・橈骨・尺骨・手根中手骨）・型（横骨折・斜骨折・粉砕骨折）・転位を確認。開放骨折の有無を評価し、創傷培養を実施。CBC/生化学で失血性貧血・Ca異常を評価。大型オウム類ではパニック飛行（ナイトフライト）・落下・衝突が主要原因。骨髄内ピンニングまたは外固定による整復が標準的治療。"
}

# 53. cockatoo_fracture_wing — Wing Fracture (Cockatoo) / 翼骨折（コッカチュー）
ENRICHMENTS["cockatoo_fracture_wing"] = {
    "diagnosis_ja": "翼の下垂・飛行不能・腫脹・疼痛からバタン（コッカトゥー）の翼骨折を疑う。触診で骨折部位の軋轢音・異常可動性を確認。X線（2方向）で骨折の部位・型・転位を評価。バタン属は大型で体重が重く（300-1000g）、含気骨が脆弱なため粉砕骨折のリスクが高い。開放骨折では創傷培養を実施。CBC/生化学で失血性貧血・代謝性骨疾患（Ca/P異常）を評価。ナイトフライトが主要原因であり、飼育環境のリスク評価が重要。外固定・骨髄内ピンニングで整復する。"
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
