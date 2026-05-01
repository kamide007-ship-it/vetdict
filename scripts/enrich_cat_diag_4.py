#!/usr/bin/env python3
import json, os, time

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diseases_all_species.json")

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["cat_dermatophytosis_ringworm"] = {"diagnosis_ja": (
    "ウッド灯検査でM. canis感染毛の蛍光（apple-green: 感度50%）。毛の直接鏡検（KOH法）で外毛根鞘の分節節を確認。"
    "真菌培養（DTM/Sabouraud培地: 7-14日）で皮膚糸状菌を同定。PCRで迅速同定（Microsporum canis/T. mentagrophytes）。"
    "Mackenzieブラシ法で保菌の有無をスクリーニング。CBC/生化学は正常。"
    "円形脱毛・鱗屑・痂皮の特徴的皮膚病変。ペルシャに好発。人獣共通感染症。イトラコナゾール経口+局所療法。"
)}

ENRICHMENTS["cat_flea_allergy_dermatitis"] = {"diagnosis_ja": (
    "身体検査で背部・尾根部・内股の粟粒性皮膚炎、脱毛、痂皮を確認。ノミ・ノミ糞の検出。"
    "皮内テストでノミ唾液抗原に対するアレルギー反応（即時型+遅延型）。"
    "血清アレルゲン特異的IgE検査。皮膚生検で好酸球性皮膚炎パターン。"
    "食物アレルギー、アトピー性皮膚炎との鑑別に除去食試験。ノミ駆除+環境処理で症状消失が確定的。"
)}

ENRICHMENTS["cat_eosinophilic_granuloma_complex_-_eosinophilic_ulcer"] = {"diagnosis_ja": (
    "口腔/口唇検査で上唇のくぼんだ潰瘍（rodent ulcer/indolent ulcer）を確認。"
    "FNA/生検で好酸球浸潤と肉芽腫性炎症を確認。SCC（扁平上皮癌）との鑑別に病理が必須。"
    "CBC/血液塗抹で末梢血好酸球増加。糞便検査で寄生虫を除外。"
    "アレルギー精査: ノミアレルギー（駆除試験）、食物アレルギー（除去食）、アトピー（IgE検査）。ステロイド反応性。"
)}

ENRICHMENTS["cat_eosinophilic_granuloma_complex_-_eosinophilic_plaque"] = {"diagnosis_ja": (
    "身体検査で腹部・内股の隆起した紅斑性プラーク（湿潤、自傷痕）を確認。"
    "FNA/生検で好酸球の著明な浸潤を確認。皮膚型肥満細胞腫との鑑別に病理。"
    "CBC/血液塗抹で末梢血好酸球増加。糞便検査で寄生虫を除外。"
    "アレルギー精査: ノミ/食物/アトピーの段階的除外。皮膚掻爬検査で疥癬を除外。プレドニゾロン2 mg/kg/日で反応。"
)}

ENRICHMENTS["cat_eosinophilic_granuloma_complex_-_linear_granuloma"] = {"diagnosis_ja": (
    "身体検査で後肢内側の線状に隆起した黄白色～ピンク色のプラーク/結節を確認。口腔内結節も。"
    "FNA/生検で好酸球性肉芽腫とコラーゲン変性（flame figure）を確認。"
    "CBC/血液塗抹で末梢血好酸球増加。CBC/生化学は概ね正常。"
    "若齢猫に好発。アレルギー精査（ノミ/食物/アトピー）。自然退縮する場合あり。ステロイド/シクロスポリン。"
)}

ENRICHMENTS["cat_pemphigus_foliaceus"] = {"diagnosis_ja": (
    "皮膚生検で表皮内の棘融解と好中球/好酸球の角層下膿疱を確認。"
    "直接免疫蛍光法（DIF）で角化細胞間のIgG沈着を確認。"
    "臨床症状: 耳介・鼻梁・爪床の痂皮・膿疱・びらん。CBC/生化学は概ね正常。"
    "細菌培養で二次感染を評価。SLE・薬剤性天疱瘡を鑑別。プレドニゾロン+クロラムブシル/シクロスポリン。"
)}

ENRICHMENTS["cat_feline_acne"] = {"diagnosis_ja": (
    "身体検査で下顎の面疱（comedone: 黒い点状丘疹）と毛包炎を確認。"
    "皮膚掻爬検査でDemodexを除外。細菌培養で二次感染（Staphylococcus/Malassezia）を評価。"
    "皮膚生検で毛包の角化異常（follicular keratosis）を確認。CBC/生化学は正常。"
    "アレルギー・甲状腺機能亢進症を除外。プラスチック食器から陶器/ステンレスへ変更。クリンダマイシン/BPO局所。"
)}

ENRICHMENTS["cat_atopic_dermatitis"] = {"diagnosis_ja": (
    "除外診断: ノミアレルギー（駆除試験8週）、食物アレルギー（除去食8-12週）、寄生虫を順次除外。"
    "皮内テスト（IDT）またはアレルゲン特異的IgE血清検査で環境アレルゲンを同定。"
    "皮膚生検で好酸球性皮膚炎/界面皮膚炎パターン。CBC/血液塗抹で好酸球増加。"
    "好発部位: 頭頸部の自傷性脱毛、粟粒性皮膚炎、EGC。シクロスポリン7 mg/kg/日 or ロキベトマブ（off-label）。"
)}

ENRICHMENTS["cat_food_allergy_dermatitis"] = {"diagnosis_ja": (
    "除去食試験（8-12週間の新奇蛋白質/加水分解蛋白質食）→負荷試験で症状再燃が確定診断。"
    "血清アレルゲン特異的IgE検査は食物アレルギーへの感度/特異度が低い（参考のみ）。"
    "皮膚生検で好酸球性皮膚炎パターン。消化器症状（嘔吐/下痢）の合併を確認。"
    "頭頸部の掻痒、自傷性脱毛、粟粒性皮膚炎が猫で多い。アトピーとの併発が40-50%。"
)}

ENRICHMENTS["cat_psychogenic_alopecia"] = {"diagnosis_ja": (
    "除外診断: アレルギー（ノミ/食物/アトピー）、皮膚糸状菌、外部寄生虫を全て除外。"
    "毛の顕微鏡検査（trichogram）で毛先の折れ（self-barbering）パターンを確認。"
    "皮膚生検で原発性皮膚疾患を除外。甲状腺機能検査（T4）、FeLV/FIV検査。"
    "左右対称性の過剰グルーミングによる脱毛。腹部・内股・前肢が好発。環境ストレスの評価。行動修正+薬物療法。"
)}

ENRICHMENTS["cat_miliary_dermatitis"] = {"diagnosis_ja": (
    "身体検査で背部・頸部の小さな痂皮性丘疹（粟粒様: 触診で砂利のような感触）を確認。"
    "皮膚掻爬検査でDemodex/Notoedresを除外。真菌培養で皮膚糸状菌を除外。"
    "ノミ駆除試験で改善→FADの確定。CBC/血液塗抹で好酸球増加。"
    "原因: FAD（最多）、食物/アトピーアレルギー、寄生虫、真菌。段階的除外で原因特定。"
)}

ENRICHMENTS["cat_solar_dermatitis___squamous_cell_carcinoma_in_situ"] = {"diagnosis_ja": (
    "皮膚生検で表皮内のSCC in situ（Bowen様病変）を確認。表皮全層の異型角化細胞。"
    "耳介辺縁・鼻鏡・眼瞼の色素欠乏部位の紅斑・痂皮・潰瘍を確認。進行するとSCCに。"
    "FNA/生検で浸潤性SCCへの進行を評価。所属リンパ節のFNAで転移を確認。"
    "白猫に好発（メラニン欠乏部位）。紫外線暴露歴の確認。耳介切除/凍結療法/放射線療法。"
)}

ENRICHMENTS["cat_demodicosis"] = {"diagnosis_ja": (
    "皮膚掻爬検査で深部掻爬によりDemodex cati（毛包型）またはDemodex gatoi（表皮型）を検出。"
    "D. gatoi: 表在性掻爬で検出可能。掻痒性。同居猫にうつる。"
    "D. cati: 深部掻爬。非掻痒性。FeLV/FIV/糖尿病等の基礎免疫抑制の精査が必須。"
    "毛の顕微鏡検査（trichogram）でも検出可。CBC/生化学/FeLV/FIV/T4を測定。石灰硫黄水浴が治療。"
)}

ENRICHMENTS["cat_feline_epilepsy"] = {"diagnosis_ja": (
    "MRI/CTで構造的脳病変を除外（特発性てんかんの診断に必須）。"
    "血液検査でCBC/生化学/T4/NH3/FeLV/FIVで代謝性・感染性原因を除外。"
    "尿検査で有機酸代謝異常を除外。CSF検査で炎症性脳疾患を除外。"
    "発作のビデオ記録。発作型（部分vs全般）の分類。特発性は除外診断。フェノバルビタール/レベチラセタムが第一選択。"
)}

ENRICHMENTS["cat_vestibular_disease"] = {"diagnosis_ja": (
    "神経学的検査で末梢性（斜頸、水平/回旋眼振、落下）vs中枢性（変向性眼振、意識障害、不全麻痺）を鑑別。"
    "CT/MRIで中耳/内耳の病変（末梢性）、脳幹/小脳の病変（中枢性）を評価。"
    "耳鏡で鼓膜の異常（中耳炎）を確認。CBC/生化学/T4/FeLV/FIVを測定。"
    "特発性前庭症候群は高齢猫に多い。NP（鼻咽頭ポリープ）・中耳炎を除外。中枢性は予後不良。"
)}

ENRICHMENTS["cat_meningioma"] = {"diagnosis_ja": (
    "MRI（造影T1）で硬膜付着性の均一に強い造影増強腫瘤を確認。dural tail signが特徴的。"
    "CT（造影）でも確認可能。猫では多発性の場合あり（犬より多い）。"
    "CSF検査で蛋白上昇、軽度細胞数増多。CBC/生化学は概ね正常。"
    "猫の脳腫瘍の最多（60%）。高齢猫に好発。外科切除が第一選択で予後良好（犬より容易に摘出可能）。"
)}

ENRICHMENTS["cat_fip_neurological_form"] = {"diagnosis_ja": (
    "MRIで脳室周囲の造影増強、水頭症、髄膜の肥厚・造影増強を確認。"
    "CSF検査で蛋白著増（>2.0 g/dL）、混合型細胞数増多。CSF中の抗FCoV抗体/RT-PCR。"
    "血液検査で高γグロブリン血症、A/G比<0.8、高ビリルビン血症。"
    "運動失調、発作、麻痺、行動変化の神経症状。組織の免疫組織化学が確定診断。GS-441524抗ウイルス療法。"
)}

ENRICHMENTS["cat_thiamine_deficiency_vitamin_b1"] = {"diagnosis_ja": (
    "食餌歴の確認: 生魚食（チアミナーゼ）、不完全食、加熱不十分な商業食。"
    "神経学的検査で頸部腹屈（ventroflexion）、運動失調、散瞳、痙攣を確認。"
    "MRIで脳幹核の両側対称性T2高信号を確認（特に尾側丘: 人のWernicke脳症に類似）。"
    "血中チアミン濃度測定（低値で確認）。チアミン注射（100-250 mg IM/SC）への劇的な反応が診断的。"
)}

ENRICHMENTS["cat_feline_hyperesthesia_syndrome"] = {"diagnosis_ja": (
    "ビデオ記録で特徴的な行動パターンを確認: 背部の皮膚波打ち、突然の自傷、激しい走り回り、瞳孔散大。"
    "MRI/CTで脊髄・脳の構造的病変を除外。皮膚検査でアレルギー・皮膚糸状菌を除外。"
    "甲状腺機能検査（T4）で甲状腺機能亢進症を除外。CBC/生化学/FeLV/FIVを測定。"
    "てんかんとの鑑別にEEG。ストレス/不安の環境評価。ガバペンチン/フルオキセチンが治療的。"
)}

ENRICHMENTS["cat_polyneuropathy"] = {"diagnosis_ja": (
    "EMGで脱神経電位を検出。神経伝導速度検査で運動/感覚神経の伝導速度低下。"
    "筋/神経生検で軸索変性または脱髄を確認。CBC/生化学/T4/FeLV/FIVで基礎疾患を精査。"
    "糖尿病性ニューロパチー（最多）: 後肢の跛行足歩行（plantigrade stance）が特徴的。血糖管理で改善。"
    "特発性、腫瘍随伴、有機リン中毒も鑑別。進行性の四肢筋萎縮・反射低下。"
)}

ENRICHMENTS["cat_spinal_cord_lymphoma"] = {"diagnosis_ja": (
    "MRIで脊髄/硬膜外の造影増強腫瘤を確認。T2高信号の脊髄圧迫・浮腫。"
    "CSF検査でリンパ芽球を検出。フローサイトメトリーでT/B細胞型を分類。"
    "CT myelographyで脊髄圧迫の位置と範囲を評価。FeLV/FIV検査。"
    "全身ステージング: CBC/生化学、胸腹部画像、骨髄穿刺。進行性の後肢不全麻痺で疑う。化学療法+放射線療法。"
)}

ENRICHMENTS["cat_intervertebral_disc_disease_ivdd"] = {"diagnosis_ja": (
    "MRIで椎間板の突出/脱出と脊髄圧迫を確認。T2高信号の脊髄病変（浮腫/壊死）。"
    "CT/CT myelographyで石灰化椎間板と脊柱管内の圧迫物質を確認。"
    "X線で椎間板腔の狭小化、石灰化を確認（感度限定的）。CSF検査で炎症を除外。"
    "猫では犬より稀。急性の疼痛+神経学的欠損で疑う。Hansen type Iが猫では多い。外科的減圧or保存療法。"
)}

ENRICHMENTS["cat_cerebral_ischemic_encephalopathy_stroke"] = {"diagnosis_ja": (
    "MRIで脳実質のT2/FLAIR高信号、DWI（拡散強調画像）高信号（急性期の細胞性浮腫）を確認。"
    "血管領域に一致した病変分布。MRAで血管閉塞を評価。"
    "CBC/生化学/T4/凝固検査で基礎疾患を精査。血圧測定で高血圧を確認。"
    "心エコーで心筋症（血栓塞栓源）を評価。急性の局所神経症状（片側性）。猫では虚血性が多い。"
)}

ENRICHMENTS["cat_osteoarthritis_degenerative_joint_disease"] = {"diagnosis_ja": (
    "X線で関節腔の狭小化、骨棘形成（osteophyte）、軟骨下骨硬化を確認。"
    "身体検査で関節の可動域制限、関節腫脹、クレピタスを確認。疼痛スコアリング。"
    "猫のOA有病率は高い（12歳以上で90%）が、症状の表出が乏しい（行動変化のみ）。"
    "活動量低下、ジャンプ拒否、グルーミング減少の飼い主アンケート。フルネベトマブ（Solensia）/メロキシカム。"
)}

ENRICHMENTS["cat_fracture"] = {"diagnosis_ja": (
    "X線（2方向以上: AP+lateral）で骨折線、転位、粉砕の程度を確認。"
    "身体検査で腫脹、疼痛、クレピタス、異常可動性を確認。開放骨折のグレーディング。"
    "CBC/生化学で全身状態・麻酔リスクを評価。胸部X線で気胸/肺挫傷（外傷時）を確認。"
    "高所落下（high-rise syndrome）: 横隔膜破裂、口蓋裂、膀胱破裂の合併を検索。外科的/保存的固定。"
)}

ENRICHMENTS["cat_luxating_patella"] = {"diagnosis_ja": (
    "整形外科検査で膝蓋骨の脱臼（内方/外方）を確認。Putnamグレーディング（I-IV）で重症度評価。"
    "X線で膝蓋骨の位置異常、脛骨粗面の内側変位、大腿骨溝の浅さを確認。"
    "触診で膝蓋骨の可動性・還納性を評価。関節液検査で感染性関節炎を除外。"
    "猫では犬より稀だが発生する。デボンレックスに好発。Grade III-IVで外科的矯正（滑車溝深化+脛骨粗面移動）。"
)}

ENRICHMENTS["cat_hip_dysplasia"] = {"diagnosis_ja": (
    "X線（VD extended view）でNorberg角の減少、関節の緩み（subluxation）、二次性OA変化を確認。"
    "PennHIP法（distraction index）で関節弛緩度を定量化。DI>0.3で異常。"
    "触診でOrtolani sign陽性（脱臼→還納のクリック）を確認。ROM制限。"
    "メインクーン、ペルシャに好発。X線的異常と臨床症状の相関は猫では弱い。体重管理+NSAIDs/フルネベトマブ。"
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
