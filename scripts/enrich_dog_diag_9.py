#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_snakebite_envenomation"] = {
    "diagnosis_ja": (
        "ヘビ咬傷歴+咬傷部位の急速な腫脹、疼痛、出血。マムシ（日本で最多）: "
        "咬傷2点（牙痕）、局所腫脹→壊死。全身症状: 嘔吐、DIC、横紋筋融解、AKI。"
        "CBC: 血小板減少、赤血球形態異常（echinocyte）。凝固パネル: PT/APTT延長、FDP上昇。"
        "CK著増（横紋筋融解）、BUN/Cre上昇（腎障害）。腫脹の進展をマーキング・時間記録。"
        "抗毒素血清投与の適応判定。日本ではマムシ・ヤマカガシが臨床上重要。"
    )
}

ENRICHMENTS["dog_bee_wasp_sting_anaphylaxis"] = {
    "diagnosis_ja": (
        "ハチ刺傷歴+急性アナフィラキシー: 顔面腫脹（血管浮腫）、蕁麻疹、嘔吐、虚脱、"
        "循環虚脱（低血圧、頻脈、蒼白粘膜→チアノーゼ）。犬の標的臓器は肝臓・消化管。"
        "刺傷部位の確認と毒針除去。CBC: 好酸球増加（遅延型）。"
        "多数刺傷: 溶血、横紋筋融解（CK）、AKI（BUN/Cre）、DIC、肝障害（ALT/ALP）。"
        "反復曝露で感作→アナフィラキシーリスク上昇。エピネフリン即時投与が救命的。"
    )
}

ENRICHMENTS["dog_foreign_body_in_ear"] = {
    "diagnosis_ja": (
        "急性の頭部振盪、耳搔き、頭部傾斜。耳鏡検査で異物（植物芒刺/awn、毛、昆虫等）を直視確認。"
        "鼓膜の評価が必須（異物が中耳に穿通した場合の二次的中耳炎リスク）。"
        "二次的外耳炎の合併評価: 耳垢細胞診で細菌/酵母を確認。"
        "全身麻酔下での摘出が安全（深部異物の場合）。ビデオオトスコープで詳細な可視化。"
        "草むら散歩後の発症が多い（ノギ: foxtail/awn）。反復性の場合は基礎疾患を検索。"
    )
}

ENRICHMENTS["dog_gastric_foreign_body"] = {
    "diagnosis_ja": (
        "嘔吐（間欠的）、食欲不振、腹部不快感。腹部X線で放射線不透過性異物を確認。"
        "X線透過性異物: 造影（バリウム/イオヘキソール）で充填欠損として描出。"
        "腹部エコーで胃内容の異常エコー源を検出。"
        "上部消化管内視鏡で直視確認と非観血的摘出（把持鉗子/バスケット/スネア）。"
        "穿孔リスク評価: 異物の形状（鋭利/鈍/線状）、滞留時間。腹膜炎徴候の評価。"
        "線状異物（紐/糸）は腸管plicationの原因→X線で特徴的なパターン。"
    )
}

ENRICHMENTS["dog_histiocytic_sarcoma"] = {
    "diagnosis_ja": (
        "急速進行性の多臓器病変: 脾腫、肝腫大、リンパ節腫大、肺結節。"
        "FNA/生検+免疫組織化学: CD18+/CD11d+/MHC II+の大型多形性細胞。"
        "播種型（disseminated）vs局所型（localized）の病型分類。"
        "CBC: 非再生性貧血、血小板減少。生化学: ALP/ALT上昇、低Alb。"
        "胸部/腹部CT+PETで全身的ステージング。"
        "好発犬種: バーニーズマウンテンドッグ（遺伝的素因）、フラットコーテッドレトリバー。"
    )
}

ENRICHMENTS["dog_fibrosarcoma"] = {
    "diagnosis_ja": (
        "皮下/口腔内の硬い浸潤性腫瘤。FNAでは診断困難な場合が多い（低い細胞剥離性）。"
        "切開生検（incisional biopsy）で組織学的確定: 紡錘形細胞のherringbone pattern。"
        "グレーディング（Grade I-III）で悪性度評価。CT/MRIで腫瘤の浸潤範囲を術前評価。"
        "胸部X線/CTで肺転移評価（高グレードで転移率25-40%）。所属リンパ節FNA。"
        "口腔型は骨浸潤が多い。ワクチン接種部位肉腫（猫で典型的だが犬でも報告あり）の鑑別。"
    )
}

ENRICHMENTS["dog_anal_sac_adenocarcinoma"] = {
    "diagnosis_ja": (
        "直腸内指診で肛門嚢内の硬い腫瘤を触知。約25%で高Ca血症（PTHrP産生）で発見。"
        "FNA+細胞診: 基底様細胞のクラスター。免疫組織化学で確定。"
        "腸腰リンパ節の著明な腫大（腹部エコー/CT）→FNAでステージング。"
        "胸部X線/CTで肺転移評価。iCa、PTHrP測定。"
        "腫瘍サイズ、リンパ節転移、遠隔転移でステージ分類（T1-3, N0-1, M0-1）。"
        "早期発見（直腸内指診）が予後改善の鍵。"
    )
}

ENRICHMENTS["dog_insulinoma_pancreatic_beta_cell_tumor"] = {
    "diagnosis_ja": (
        "空腹時低血糖（<60mg/dL）+同時測定の不適切なインスリン高値で強く疑診。"
        "修正インスリン/グルコース比（AIGR）>30で診断的。72時間絶食負荷試験。"
        "腹部エコー/造影CTで膵臓腫瘤を描出（多くは<2cm、検出困難）。"
        "術中超音波で膵臓全体の精査+肝転移の有無。"
        "フルクトサミンは慢性低血糖を反映（低値）。"
        "中～大型犬の中高齢に好発。発作、後肢虚脱、振戦が主徴。"
    )
}

ENRICHMENTS["dog_thyroid_carcinoma"] = {
    "diagnosis_ja": (
        "頸部腹側の腫瘤を触診で発見。可動性vs固着性で手術適否を評価。"
        "FNA+細胞診で甲状腺上皮由来の腫瘍細胞を確認。T4/fT4測定（機能性vs非機能性）。"
        "頸部エコーで腫瘤のサイズ・血管浸潤・リンパ節転移を評価。"
        "胸部3方向X線/CTで肺転移評価（診断時30-40%で遠隔転移）。"
        "99mTcシンチグラフィーで機能性甲状腺腫瘍の局在診断。CT血管造影で頸動脈/静脈の巻き込み評価。"
        "サイログロブリン測定は術後モニタリングに有用。"
    )
}

ENRICHMENTS["dog_perianal_adenoma"] = {
    "diagnosis_ja": (
        "肛門周囲の単発/多発性の隆起性腫瘤。未去勢雄犬に好発（テストステロン依存性）。"
        "FNA/生検で肝様細胞（hepatoid cells）の腺腫を確認。"
        "良性（腺腫）vs悪性（腺癌）の鑑別: 腺癌は浸潤性で局所再発率が高い。"
        "テストステロン/エストラジオール測定。直腸内指診で直腸壁浸潤を評価。"
        "去勢歴の確認（去勢犬の肛門周囲腫瘤は腺癌を疑う）。"
        "所属リンパ節FNA、胸部X線/腹部エコーでステージング。"
    )
}

ENRICHMENTS["dog_hepatocellular_carcinoma"] = {
    "diagnosis_ja": (
        "肝腫大/腹部膨満、食欲不振、体重減少。偶発的エコー所見として発見されることもある。"
        "腹部エコーで肝腫瘤の形態分類: massive型（単葉性、手術適応最良）、nodular型、diffuse型。"
        "エコーガイド下FNA→細胞学: 大型肝細胞のクラスター、核異型。"
        "生化学: ALT/ALP/GGT上昇、低血糖（paraneoplastic）、赤血球増加症。"
        "AFP（αフェトプロテイン）上昇。腹部CT造影で三相評価（動脈相での造影効果）。"
        "胸部X線+腹腔リンパ節FNAでステージング。"
    )
}

ENRICHMENTS["dog_chemodectoma_heart_base_tumor"] = {
    "diagnosis_ja": (
        "心基底部腫瘤による心嚢水貯留→心タンポナーデ（右心不全徴候: 腹水、頸静脈怒張）。"
        "心エコーで心嚢液+心基底部のmassを描出。心嚢穿刺で血性液を採取→細胞診。"
        "心嚢液のpH、LDH、トロポニン測定。CT造影で腫瘤の範囲・大血管との関係を評価。"
        "心電図: 電位低下（心嚢液）、ST変化。胸部X線: 球形心影（globoid heart）。"
        "好発犬種: ボクサー、ブルドッグ、ボストンテリア（短頭種に顕著）。"
    )
}

ENRICHMENTS["dog_nasal_adenocarcinoma"] = {
    "diagnosis_ja": (
        "慢性片側性鼻汁（血性→膿性）、くしゃみ、顔面変形、エピスタキシス。"
        "頭部CT/MRIで腫瘤の範囲・篩板浸潤・眼窩浸潤・頭蓋内進展を評価。"
        "鼻腔鏡で直視下生検→組織学的確定（腺癌が鼻腔腫瘍の60%）。"
        "Modified Adams staging: T1（片側限局）→T4（篩板破壊+頭蓋内浸潤）。"
        "胸部X線/CTで肺転移評価。所属リンパ節（下顎、咽頭後）FNA。"
        "長頭種に好発。放射線治療が主要な治療選択肢。"
    )
}

ENRICHMENTS["dog_soft_tissue_sarcoma"] = {
    "diagnosis_ja": (
        "皮下/筋膜の硬い、境界不明瞭な腫瘤。FNAは低い細胞剥離性のため生検推奨。"
        "切開生検+組織学: 紡錘形細胞腫瘍のスペクトラム（末梢神経鞘腫瘍、血管周皮腫、"
        "線維肉腫、粘液肉腫等）。グレーディング（I-III）で予後・治療方針決定。"
        "CT/MRIで浸潤範囲の術前マッピング。胸部X線/CTで肺転移評価。"
        "Grade I/II: 転移率<20%だが局所再発率高い。Grade III: 転移率>40%。"
        "外科的マージン（≥3cm lateral, 1 fascial plane deep）の術前計画。"
    )
}

ENRICHMENTS["dog_lipoma"] = {
    "diagnosis_ja": (
        "皮下の軟らかい可動性の腫瘤。FNA: 成熟脂肪細胞のクラスター+油滴→良性脂肪腫の診断。"
        "浸潤性脂肪腫の鑑別: 可動性制限、筋膜/筋層への浸潤→MRI/CTで浸潤範囲評価。"
        "脂肪肉腫（liposarcoma）との鑑別: 急速増大、硬い質感、固着性→生検推奨。"
        "多発性脂肪腫: 甲状腺機能低下症の合併を検索（T4/TSH）。"
        "中高齢の過体重犬に好発。ラブラドール、ダックスフンド。"
    )
}

ENRICHMENTS["dog_plasmacytoma"] = {
    "diagnosis_ja": (
        "皮膚/口腔/消化管の孤立性腫瘤。FNA: 円形細胞腫瘍、核偏在+明瞭な核周明庭（Golgi zone）。"
        "免疫組織化学: CD79a+/MUM1+/CD20-で形質細胞系を確認。"
        "皮膚型: 通常良性（外科的切除で治癒的）。口腔/消化管型: 転移リスク高い。"
        "全身検索: 血清蛋白電気泳動（M蛋白=多発性骨髄腫の除外）、骨格X線（溶骨性病変）、"
        "骨髄穿刺（骨髄形質細胞>5%で骨髄腫）。尿中Bence Jones蛋白。"
    )
}

ENRICHMENTS["dog_separation_anxiety"] = {
    "diagnosis_ja": (
        "飼い主不在時の破壊行動、過剰な吠え/鳴き声、不適切な排泄。帰宅直前にエスカレート。"
        "行動歴の詳細聴取: 発症時期、トリガー、飼い主の出発/帰宅ルーチン。"
        "留守中のビデオ撮影で行動パターンを客観的に評価（最重要な診断ツール）。"
        "身体検査/CBC/生化学/T4で器質的疾患を除外。認知機能障害との鑑別（高齢犬）。"
        "鑑別: 運動不足、退屈、不完全な家庭内トレーニング、雷恐怖症、分離関連問題の亜型。"
    )
}

ENRICHMENTS["dog_compulsive_disorder_canine_ocd"] = {
    "diagnosis_ja": (
        "繰り返し行動（尾追い、影追い、空噛み、わき腹吸引、過剰舐め）が増悪し、"
        "日常機能を障害する段階で診断。行動の文脈外での反復が定義的。"
        "ビデオ記録による行動頻度・持続時間の定量化。"
        "神経学的検査で発作性疾患を除外（特に尾追い: 部分発作との鑑別にEEG/MRI）。"
        "CBC/生化学/T4で内分泌・代謝性疾患を除外。皮膚検査でアレルギー性原因を除外。"
        "品種素因: ドーベルマン（わき腹吸引）、ブルテリア（尾追い/旋回）。"
    )
}

ENRICHMENTS["dog_noise_phobia"] = {
    "diagnosis_ja": (
        "特定の音刺激（雷、花火、銃声等）に対する過剰な恐怖反応: 振戦、パンティング、"
        "逃走行動（破壊的脱出試行）、隠れ、凍結。"
        "行動歴: 発症時期、トリガー音の特定、反応の重症度スケーリング（0-10）。"
        "ビデオ記録で反応パターンの客観的評価。併存症の評価: 分離不安、全般性不安。"
        "身体検査/聴覚検査で疼痛性疾患・聴覚異常を除外。"
        "T4/コルチゾールで内分泌性の不安要因を除外。"
    )
}

ENRICHMENTS["dog_pica"] = {
    "diagnosis_ja": (
        "非食品素材（石、布、紙、木、土等）の反復的摂取行動。"
        "行動歴: 摂取対象の特定、頻度、状況（留守中/飼い主在宅時）。"
        "消化管異物合併の評価: 腹部X線/エコーで閉塞徴候を確認。"
        "CBC/生化学（鉄、亜鉛）で栄養欠乏・代謝異常を除外。糞便検査で寄生虫を除外。"
        "膵外分泌不全（TLI低値）、IBD、EPI等の消化器疾患スクリーニング。"
        "鑑別: 強迫性障害、分離不安、注目獲得行動、探索行動。"
    )
}

ENRICHMENTS["dog_disseminated_intravascular_coagulation_dic"] = {
    "diagnosis_ja": (
        "基礎疾患（敗血症、IMHA、GDV、膵炎、熱中症、腫瘍等）に伴う凝固異常。"
        "凝固パネル: PT/APTT延長、フィブリノゲン低値、FDP/D-dimer著増、AT III低下。"
        "CBC: 血小板急速低下（<100,000→<50,000/μL）、血小板消費パターン。"
        "血液塗抹: 破砕赤血球（schistocyte）、低血小板。TEG/ROTEM（粘弾性凝固検査）で"
        "凝固亢進→低凝固の動的変化を評価。出血相vs過凝固相の病期判定が治療方針に重要。"
    )
}

ENRICHMENTS["dog_anemia_of_chronic_disease"] = {
    "diagnosis_ja": (
        "慢性炎症/感染/腫瘍に伴う軽度～中等度の正球性正色素性非再生性貧血。"
        "CBC: PCV 20-30%、網赤血球数低～正常。鉄代謝: 血清鉄低値、TIBC低値、"
        "フェリチン高値（鉄欠乏性貧血との重要な鑑別点）。"
        "基礎疾患の検索: CRP/SAA、全身画像検査、感染症スクリーニング、骨髄穿刺。"
        "EPO（エリスロポエチン）は相対的低値。ヘプシジン過剰が病態の中心（鉄利用障害）。"
    )
}

ENRICHMENTS["dog_evan's_syndrome"] = {
    "diagnosis_ja": (
        "IMHA+ITPの同時発症: 貧血+血小板減少+自己免疫性。CBC: PCV急速低下+PLT<50,000/μL。"
        "Coombs試験（直接）陽性+抗血小板抗体陽性。血液塗抹: 球状赤血球+自己凝集（スライド凝集試験）。"
        "網赤血球: 通常増加（再生性）だが非再生性の場合は骨髄検査。"
        "基礎疾患除外: ANA（SLE）、感染症パネル（Ehrlichia/Anaplasma/Babesia PCR）、"
        "腹部エコー（リンパ腫、脾臓疾患）。コッカースパニエル、オールドイングリッシュシープドッグに好発。"
    )
}

ENRICHMENTS["dog_glomerulonephritis"] = {
    "diagnosis_ja": (
        "持続性蛋白尿（UPC>2.0）がスクリーニングの鍵。浮腫、腹水（低Alb血症）。"
        "尿検査: 蛋白尿+沈渣正常（活性尿沈渣がないことがIGN vs tubular の鑑別）。"
        "生化学: 低Alb、高コレステロール（ネフローゼ症候群）、BUN/Cre上昇（進行期）。"
        "腎生検（エコーガイド下/腹腔鏡）: LM+IF+EMで免疫複合体型/膜性/増殖性を分類。"
        "血圧測定（全身性高血圧の合併）。基礎疾患検索: 感染症（Ehrlichia/Leishmania/Borrelia）、"
        "SLE、腫瘍関連。AT III測定（血栓塞栓リスク評価）。"
    )
}

ENRICHMENTS["dog_pyelonephritis"] = {
    "diagnosis_ja": (
        "発熱、腰背部痛（腎臓触診時の疼痛）、元気消失、多飲多尿。"
        "尿検査: 膿尿+細菌尿+円柱（白血球円柱が上部尿路感染に特異的）。尿培養+感受性試験。"
        "CBC: 好中球増加+左方移動。生化学: BUN/Cre上昇（急性腎障害合併時）。"
        "腹部エコー: 腎盂拡張、腎皮質輝度亢進、尿管拡張。"
        "造影CT: 腎実質の造影不良域（線条型パターン）。"
        "素因検索: 尿路結石、先天性異常（異所性尿管）、DM、Cushing。"
    )
}

ENRICHMENTS["dog_urethral_obstruction"] = {
    "diagnosis_ja": (
        "排尿姿勢+排尿不能/滴下状排尿、しぶり、腹部膨満（膀胱緊満）。"
        "膀胱触診で緊満した膀胱を確認。尿道カテーテル挿入で閉塞部位の特定。"
        "腹部X線: 放射線不透過性結石（ストルバイト、シュウ酸Ca）。エコーで膀胱緊満+結石。"
        "生化学: 高K+高BUN/Cre+代謝性アシドーシス（閉塞後腎不全）。心電図: 高K性変化。"
        "閉塞原因: 尿路結石（最多）、尿道栓子、腫瘍、狭窄、前立腺肥大。"
        "緊急カテーテル減圧+電解質補正が優先。"
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
