#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_tooth_fracture"] = {
    "diagnosis_ja": (
        "口腔内診察で歯冠/歯根の破折を確認。複雑性（歯髄露出）vs非複雑性の分類。"
        "歯科X線で歯根破折・根尖周囲病変（ハロー）を評価。"
        "歯髄活力テスト（冷刺激/電気的）で歯髄壊死を評価。"
        "変色歯（灰色/ピンク）は歯髄壊死/内部吸収を示唆。"
        "外傷犬種: 噛み犬遊び、硬いおもちゃ（鹿角、蹄）、交通事故。第4前臼歯に最多。"
    )
}

ENRICHMENTS["dog_oral_melanoma"] = {
    "diagnosis_ja": (
        "口腔内の色素性（時に無色素性）腫瘤。FNA+細胞診で円形～紡錘形細胞+メラニン顆粒。"
        "免疫組織化学（Melan-A、PNL2、S-100）で無色素性メラノーマの確定。"
        "口腔メラノーマは犬の最も悪性な口腔腫瘍: 転移率80%以上。"
        "ステージング: 所属リンパ節FNA/生検、胸部3方向X線/CT（肺転移）。"
        "WHO Stage I-IV（腫瘤サイズ+リンパ節+遠隔転移）。Oncept ワクチンの適応評価。"
    )
}

ENRICHMENTS["dog_epulis_gingival_mass"] = {
    "diagnosis_ja": (
        "歯肉の限局性腫瘤。線維性エプリス（非腫瘍性）、骨形成性エプリス、"
        "棘細胞性エナメル上皮腫（acanthomatous ameloblastoma: 局所浸潤性、骨破壊性）の鑑別が重要。"
        "生検で組織学的分類。歯科X線/CTで骨浸潤の評価。"
        "棘細胞性エナメル上皮腫は転移しないが局所浸潤が強い→広範囲切除が必要。"
        "ボクサー、その他短頭種に好発。"
    )
}

ENRICHMENTS["dog_stomatitis"] = {
    "diagnosis_ja": (
        "口腔粘膜の広範な炎症: 発赤、潰瘍、出血、口臭、流涎、摂食拒否。"
        "口腔内診察で病変の分布・程度を評価。生検で組織学的分類（リンパ球プラスマ細胞性等）。"
        "基礎疾患: 腎不全（BUN/Cre→尿毒症性口内炎）、DM、免疫介在性、"
        "薬剤性、接触性、感染性（カンジダ）。CBC/生化学/尿検査で全身性疾患をスクリーニング。"
    )
}

ENRICHMENTS["dog_cleft_palate"] = {
    "diagnosis_ja": (
        "新生子犬の哺乳時に鼻からの乳汁漏出、くしゃみ、吸啜困難で発見。"
        "口腔内診察で硬口蓋/軟口蓋の裂隙を直視確認。口蓋裂の範囲（片側/両側、硬/軟口蓋）を評価。"
        "鼻腔鏡で口鼻瘻管の有無を確認。胸部X線で誤嚥性肺炎の合併を評価。"
        "先天性: 短頭種に好発。遺伝的素因、催奇形物質曝露、栄養欠乏が原因。"
        "外傷性: 電気コード咬傷、交通事故。手術は8-12週齢以降。"
    )
}

ENRICHMENTS["dog_portosystemic_shunt_congenital"] = {
    "diagnosis_ja": (
        "若齢犬の発育不良、食後の神経症状（旋回、失見当、発作、流涎）、多飲多尿。"
        "生化学: BUN低値、Alb低値、血糖低値。食前/食後胆汁酸ペア検査（食後>100μmol/Lで診断的）。"
        "血中アンモニア上昇（食後に顕著）。腹部エコーで異常血管を検出（感度80-95%）。"
        "門脈造影CT（CTA）でシャント血管の走行・形態を3D評価（術前計画に必須）。"
        "尿検査: 尿酸アンモニウム結晶。肝外シャント（小型犬に多い）vs肝内シャント（大型犬）。"
    )
}

ENRICHMENTS["dog_congenital_deafness"] = {
    "diagnosis_ja": (
        "子犬の呼びかけ/音刺激に対する無反応、しつけ困難で疑診。"
        "BAER検査（脳幹聴覚誘発反応）が確定診断: 片側性/両側性を客観的に判定。"
        "生後5週齢以降にBAER検査可能。耳鏡検査で外耳道/鼓膜の形態評価。"
        "白色被毛遺伝子（merle、piebald）と関連: ダルメシアン（有病率30%）、"
        "オーストラリアンシェパード、ブルドッグ、ボクサー。片側性は行動観察では検出困難。"
    )
}

ENRICHMENTS["dog_atlantoaxial_instability"] = {
    "diagnosis_ja": (
        "頸部痛（頸部の低頭位保持、頸部触診時の疼痛）、四肢不全麻痺/麻痺、呼吸障害。"
        "頸部X線（側面、屈曲位は慎重に）で環軸間の亜脱臼・歯突起の欠損/低形成を確認。"
        "CT/MRIで歯突起・横靭帯の評価、脊髄圧迫の程度を詳細に評価。"
        "小型犬（ヨークシャーテリア、チワワ、ポメラニアン、トイプードル）に好発。"
        "神経学的検査: UMN四肢不全麻痺、頸部過屈曲回避。頸部の愛護的取り扱いが必須。"
    )
}

ENRICHMENTS["dog_persistent_right_aortic_arch_praa"] = {
    "diagnosis_ja": (
        "離乳後の固形食嘔吐（逆流: 食道由来、腹圧なし）。液体は正常に通過。"
        "胸部X線: 心基底部での食道拡張（造影で確認）。"
        "食道造影（バリウム）で心基底部での狭窄+その前方の食道拡張を描出。"
        "CT血管造影で血管輪の走行を詳細評価。食道鏡で狭窄の程度確認。"
        "ジャーマンシェパード、アイリッシュセッター、グレートデーンに好発。"
        "誤嚥性肺炎の合併評価（胸部X線: 肺胞パターン）。"
    )
}

ENRICHMENTS["dog_mucopolysaccharidosis"] = {
    "diagnosis_ja": (
        "発育異常（矮小体型）、顔面異形、角膜混濁、骨格異常（椎体変形）、心臓弁膜症。"
        "尿中GAG（グリコサミノグリカン）排泄増加のスクリーニング。"
        "白血球/リンパ球内の異染性顆粒（Alder-Reilly小体）を血液塗抹で確認。"
        "特異的酵素活性測定（MPS I: α-L-iduronidase、MPS VI: arylsulfatase B等）で型同定。"
        "遺伝子検査で変異確認。X線で多発性骨異形成（dysostosis multiplex）。"
        "品種特異的: ミニチュアピンシャー（MPS VI）、プロットハウンド（MPS I）。"
    )
}

ENRICHMENTS["dog_glycogen_storage_disease"] = {
    "diagnosis_ja": (
        "若齢犬の運動不耐性、筋力低下、肝腫大、低血糖。型により症状が異なる。"
        "GSD III（Curly-coated Retriever）: 肝+筋（CK上昇、肝酵素上昇）。"
        "GSD Ia（Maltese）: 低血糖発作、肝腫大。筋生検/肝生検で過剰グリコーゲン蓄積確認。"
        "特異的酵素活性測定で型同定。遺伝子検査が利用可能な品種あり。"
        "空腹時低血糖→乳酸アシドーシス。肝エコーで肝腫大+高輝度。"
    )
}

ENRICHMENTS["dog_malignant_hyperthermia"] = {
    "diagnosis_ja": (
        "麻酔中（吸入麻酔薬/サクシニルコリン曝露後）の急速な体温上昇（>42°C）、"
        "筋硬直、頻脈、CO2産生著増（ETCO2>60mmHg）、代謝性/呼吸性アシドーシス。"
        "血液ガスで混合型アシドーシス。CK急速上昇（横紋筋融解）。高K、ミオグロビン尿。"
        "カフェイン・ハロタン筋収縮試験（生検筋）が確定だが実用的でない。"
        "RYR1遺伝子変異検査。グレイハウンド、ボーダーコリーで報告。ダントロレンが特異的治療。"
    )
}

ENRICHMENTS["dog_juvenile_cellulitis_puppy_strangles"] = {
    "diagnosis_ja": (
        "3週-6ヶ月齢の子犬の急性顔面（口唇、眼瞼、耳介）の腫脹+下顎リンパ節の"
        "著明な腫大（時に排膿）。無菌性の化膿性肉芽腫性炎症。"
        "FNA/皮膚生検: 肉芽腫性/化膿性皮膚炎、細菌培養陰性（免疫介在性）。"
        "CBC: 白血球増加、好中球増加。体温上昇。耳介の膿疱・痂皮。"
        "ゴールデンレトリバー、ダックスフンド、ラブラドールに好発。"
        "鑑別: ブドウ球菌性膿皮症、蜂窩織炎、アンギオエデマ、デモデックス症。"
    )
}

ENRICHMENTS["dog_chylothorax"] = {
    "diagnosis_ja": (
        "呼吸困難、運動不耐性、咳嗽。胸部X線: 両側性胸水貯留。"
        "胸水穿刺: 乳白色混濁液、TG>100mg/dL（胸水TG>血清TGが診断的）。"
        "胸水のスーダンIII染色で脂肪滴。リンパ球優位の細胞診（慢性では好中球増加）。"
        "原因検索: 心エコー（心膜心筋症、先天性心疾患）、胸部CT/リンパ管造影で胸管の走行、"
        "前縦隔腫瘤（リンパ腫、胸腺腫）。特発性が約50%。アフガンハウンド、柴犬に好発。"
    )
}

ENRICHMENTS["dog_megacolon"] = {
    "diagnosis_ja": (
        "慢性便秘→便秘→巨大結腸。直腸内指診で結腸内の石様硬い宿便。"
        "腹部X線で結腸の著明な拡張+宿便貯留を確認。骨盤骨折後の骨盤狭窄（二次性）の鑑別。"
        "神経学的検査で脊髄/腰仙部の異常を除外。甲状腺機能低下（T4/TSH）で鑑別。"
        "電解質（低K→腸運動低下）。犬では猫と異なり原因疾患が同定できることが多い。"
        "二次性: 骨盤狭窄、前立腺肥大、会陰ヘルニア、脊髄疾患、薬剤性。"
    )
}

ENRICHMENTS["dog_cutaneous_histiocytoma"] = {
    "diagnosis_ja": (
        "若齢犬（<3歳）の急速成長する単発性の赤色半球状結節（button tumor）。"
        "FNA: 均一な円形細胞、楕円形核、淡い細胞質。免疫組織化学: CD18+/CD1a+/MHC II+。"
        "ランゲルハンス細胞由来の良性腫瘍。4-8週で自然退縮（T細胞介在性免疫応答）。"
        "鑑別: 肥満細胞腫（メタクロマジー顆粒）、リンパ腫（CD3/CD79a）、形質細胞腫。"
        "頭部、耳介、四肢に好発。多発性の場合は免疫異常を検索。"
    )
}

ENRICHMENTS["dog_myocarditis"] = {
    "diagnosis_ja": (
        "急性の頻脈性不整脈、運動不耐性、虚脱、突然死。心電図: VPC、VT、ST変化。"
        "心エコー: 心筋壁運動異常、左室収縮機能低下（FS低下）。"
        "心筋トロポニンI（cTnI）著増が心筋障害の高感度マーカー。"
        "原因検索: パルボウイルス（子犬）、トリパノソーマ（Chagas病/輸入症例）、Bartonella、"
        "免疫介在性、薬剤性（ドキソルビシン）。心臓MRIで心筋浮腫・造影増強。"
        "心内膜心筋生検は確定だが侵襲的でリスクがある。"
    )
}

ENRICHMENTS["dog_hemolytic_uremic_syndrome"] = {
    "diagnosis_ja": (
        "微小血管障害性溶血性貧血（MAHA）+血小板減少+急性腎障害の三徴。"
        "CBC: 貧血+血小板減少。血液塗抹: 破砕赤血球（schistocyte）が特徴的。"
        "生化学: BUN/Cre急速上昇、高K、LDH上昇、間接ビリルビン上昇。ハプトグロビン低値。"
        "尿検査: ヘモグロビン尿、蛋白尿。凝固パネルでDICとの鑑別（HUSではPT/APTT正常のことが多い）。"
        "原因: EHEC（Shiga毒素産生大腸菌）、ヘビ毒、銅中毒、犬バベシア症。"
    )
}

ENRICHMENTS["dog_aural_hematoma"] = {
    "diagnosis_ja": (
        "耳介の急性腫脹（波動性、温感）。穿刺で血性/漿液血性液を確認。"
        "外耳炎/耳ダニの基礎疾患検索が必須（耳鏡検査、耳垢細胞診）: 掻痒→頭部振盪→血腫形成。"
        "穿刺液の細胞診: 赤血球、マクロファージ。慢性化で線維化→耳介変形（カリフラワー耳）。"
        "免疫介在性の関与も示唆されている。ラブラドール等の垂れ耳犬種に好発。"
    )
}

ENRICHMENTS["dog_carpal_hyperextension_injury"] = {
    "diagnosis_ja": (
        "高所からの落下/交通事故後の手根関節の過伸展（掌側が接地）。"
        "ストレスX線（荷重下）で手根関節の過伸展角度を評価。"
        "非荷重X線で手根骨の骨折・亜脱臼を確認。MRI/関節鏡で靭帯損傷の程度を評価。"
        "掌側支持構造（掌側線維軟骨パッド、靭帯群）の断裂。"
        "中～大型犬の高エネルギー外傷。手根関節固定術（パンカルパル/パーシャル）の適応判定。"
    )
}

ENRICHMENTS["dog_fragmented_medial_coronoid_process_fmcp"] = {
    "diagnosis_ja": (
        "若齢大型犬（5-18ヶ月）の前肢跛行、肘関節の疼痛・腫脹。"
        "肘関節X線: 鉤状突起のsclerosis、関節内段差（incongruity）、二次性OAの徴候。"
        "CT（関節内造影/非造影）でFMCPの骨片を直視的に検出（X線より高感度）。"
        "関節鏡で内側鉤状突起の破片・軟骨損傷を直視確認+除去。"
        "犬の肘異形成症（elbow dysplasia）の最も多い型。ラブラドール、ロットワイラー、バーニーズに好発。"
    )
}

ENRICHMENTS["dog_ununited_anconeal_process_uap"] = {
    "diagnosis_ja": (
        "若齢大型犬（5-12ヶ月）の前肢跛行、肘関節の腫脹・伸展制限。"
        "肘関節X線（屈曲側面像）で肘頭突起の癒合不全（透過線）を確認。"
        "通常5ヶ月齢までに癒合（ジャーマンシェパードでは遅延しうる）。CTで確定評価。"
        "肘異形成症の一型: 橈尺骨の不整合（incongruity）が原因機序として重要。"
        "関節鏡/外科的除去＋尺骨切り術の適応評価。二次性OAの程度も予後に影響。"
    )
}

ENRICHMENTS["dog_temporomandibular_joint_tmj_dysplasia"] = {
    "diagnosis_ja": (
        "開口困難、閉口不全（open-mouth jaw locking）、咀嚼時の疼痛、関節雑音。"
        "頭部X線で顎関節の形態異常（関節窩の浅平化、下顎頭の変形）を評価。"
        "CTで顎関節の骨形態を3D評価（X線より正確）。MRIで関節円板の位置・変性を評価。"
        "アイリッシュセッター、バセットハウンド、キャバリアに報告。"
        "鑑別: 咀嚼筋炎、三叉神経炎、顎関節脱臼、CMO、破傷風。"
    )
}

ENRICHMENTS["dog_bicipital_tenosynovitis"] = {
    "diagnosis_ja": (
        "前肢跛行、肩関節屈曲・伸展時の疼痛。上腕二頭筋腱の直接触診で圧痛。"
        "肩関節の屈曲+前方牽引テスト（biceps stretch test）で疼痛誘発。"
        "肩関節エコーで腱の腫脹、腱鞘内液貯留、石灰化。"
        "MRIで腱の信号変化・断裂・関節唇損傷を評価。関節鏡で腱+関節内の直視確認。"
        "中～大型犬の中年に好発。ラブラドール、ロットワイラー。慢性跛行の重要な原因。"
    )
}

ENRICHMENTS["dog_infraspinatus_contracture"] = {
    "diagnosis_ja": (
        "前肢の外旋+肘関節の外転位固定。肩関節の内旋・内転が制限。"
        "歩行では circumduction（外回し歩行）+肘外方偏位。"
        "肩関節X線: 通常正常（軟部組織性病変）。エコーで棘下筋の線維化・萎縮を確認。"
        "MRIで筋肉の信号変化（線維化→T1低信号、T2低信号）。"
        "典型的に外傷/過度の運動後に急性筋炎→慢性線維化拘縮として発症。"
        "作業犬、スポーツ犬に好発。棘下筋腱切断術が治療的。"
    )
}

ENRICHMENTS["dog_hypertrophic_osteodystrophy_hod_-_severe"] = {
    "diagnosis_ja": (
        "3-7ヶ月の大型犬の急性発熱（40-41°C）、四肢遠位の腫脹・疼痛、跛行、食欲廃絶。"
        "長骨X線で骨幹端のdouble physis line（成長板に平行な放射線透過帯+その遠位の硬化帯）が特徴的。"
        "重度: 骨幹端の不規則な骨膜反応、骨溶解。"
        "CBC: 好中球増加+左方移動、CRP著増。ジステンパーワクチン後の発症報告あり。"
        "グレートデーン、ワイマラナー、アイリッシュセッターに好発。栄養過多/Ca過剰が素因。"
    )
}


def apply_enrichments() -> None:
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    updated = 0
    for entry in data:
        eid = entry.get("id")
        if eid in ENRICHMENTS:
            for k, v in ENRICHMENTS[eid].items():
                entry[k] = v
            updated += 1
    missing = set(ENRICHMENTS) - {e.get("id") for e in data}
    if missing:
        print(f"WARNING: {len(missing)} IDs not found: {sorted(missing)}")
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {updated}/{len(ENRICHMENTS)} entries")


if __name__ == "__main__":
    apply_enrichments()
