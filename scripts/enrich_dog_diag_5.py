#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_mast_cell_tumor"] = {
    "diagnosis_ja": (
        "皮膚腫瘤のFNA（細針吸引細胞診）でメタクロマジー陽性の顆粒を含む円形細胞を確認。"
        "Patnaik分類（Grade I-III）またはKiupel 2分類（low/high grade）で悪性度判定。"
        "Buffy coatスメア、腹部エコー（脾臓・肝臓・リンパ節）、"
        "所属リンパ節FNAでステージング。c-KIT変異検査（エクソン11）で分子標的薬適応判定。"
        "Ki-67増殖指数・AgNOR・有糸分裂指数で予後予測。好発犬種: ボクサー、パグ、ボストンテリア。"
    )
}

ENRICHMENTS["dog_melanoma"] = {
    "diagnosis_ja": (
        "口腔内・皮膚・爪床の色素性（時に無色素性）腫瘤のFNAまたは生検で診断。"
        "免疫組織化学（Melan-A、PNL2、S-100）で無色素性メラノーマの確定。"
        "胸部3方向X線、腹部エコー、所属リンパ節FNA/生検でステージング（WHO Stage I-IV）。"
        "口腔メラノーマは高度悪性で転移率80%以上。皮膚型は良性が多いが爪床型は悪性。"
        "メラノーマワクチン（Oncept）の適応評価。"
    )
}

ENRICHMENTS["dog_squamous_cell_carcinoma"] = {
    "diagnosis_ja": (
        "皮膚・口腔・爪床の潰瘍性/増殖性病変の生検で角化を伴う扁平上皮の異型性を確認。"
        "日光性角化症からの進展を評価（色素欠乏部位、紫外線曝露歴）。"
        "胸部X線、所属リンパ節FNAで転移評価。口腔SCCは骨浸潤が多くCT推奨。"
        "爪床SCCは大型犬（黒色被毛犬種）に好発、多発性の場合は全爪床の精査が必要。"
        "扁桃原発SCCは早期転移率が高い。"
    )
}

ENRICHMENTS["dog_mammary_tumor"] = {
    "diagnosis_ja": (
        "乳腺腫瘤のFNA（細胞診）で上皮系腫瘍を示唆、確定は切除生検による組織学的分類。"
        "約50%が悪性（腺癌、固形癌、炎症性乳癌）。腫瘤サイズ・リンパ節転移・組織学的グレードでステージング。"
        "胸部3方向X線（肺転移）、腹部エコー（腹腔内転移）。"
        "エストロゲン/プロゲステロン受容体発現評価で内分泌療法適応判定。"
        "未避妊雌に好発（初回発情前避妊で乳腺腫瘍リスク0.5%）。炎症性乳癌は予後不良。"
    )
}

ENRICHMENTS["dog_transitional_cell_carcinoma"] = {
    "diagnosis_ja": (
        "膀胱三角部の腫瘤をエコーで描出（典型的に乳頭状/浸潤性）。"
        "カテーテル吸引細胞診またはトラウマティックカテーテル洗浄で移行上皮の異型細胞を検出。"
        "尿中BRAF V595E変異検査（感度85%、非侵襲的）。膀胱鏡下生検が確定診断。"
        "腹部エコーで腎盂拡張・尿管閉塞評価、胸部X線・リンパ節FNAでステージング。"
        "好発犬種: スコティッシュテリア、ウエストハイランドホワイトテリア、ビーグル。"
    )
}

ENRICHMENTS["dog_thrombocytopenia"] = {
    "diagnosis_ja": (
        "CBC（自動血球計算+血液塗抹確認）で血小板数<150,000/μL（重度<50,000/μL）。"
        "大型血小板の有無で骨髄反応性を評価。点状・斑状出血、歯肉出血、メレナが臨床徴候。"
        "鑑別: 免疫介在性（ITP）、DIC（PT/APTT/フィブリノゲン/FDP/D-dimer）、"
        "感染症（Ehrlichia/Anaplasma/Babesia PCR・抗体検査）、骨髄疾患（骨髄穿刺）、薬剤性。"
        "Coombsテスト併施でEvans症候群を除外。"
    )
}

ENRICHMENTS["dog_hemophilia_a"] = {
    "diagnosis_ja": (
        "若齢雄犬の過剰出血（関節内出血、筋肉内血腫、抜歯後止血困難）で疑診。"
        "APTT延長+PT正常のパターン。第VIII因子活性測定で確定（<50%で診断、<5%で重症型）。"
        "vWF抗原正常でvWDを除外。X連鎖劣性遺伝のため雌はキャリアー。"
        "好発犬種: ジャーマンシェパード、ゴールデンレトリバー、チェサピークベイレトリバー。"
        "遺伝子検査（FVIII遺伝子）でキャリアー検出可能。"
    )
}

ENRICHMENTS["dog_autoimmune_thrombocytopenia_itp"] = {
    "diagnosis_ja": (
        "急性の点状/斑状出血、歯肉出血、血尿、メレナとCBCで血小板<50,000/μL（しばしば<10,000/μL）。"
        "大型血小板（網状血小板）増加は骨髄の代償反応を示唆。"
        "感染症除外（Ehrlichia/Anaplasma/Babesia PCR、4DX SNAP）、骨髄穿刺で巨核球増加確認。"
        "抗血小板抗体検査（間接フローサイトメトリー）。"
        "Coombsテストで同時IMHA（Evans症候群）を評価。好発: 中年雌、コッカースパニエル。"
    )
}

ENRICHMENTS["dog_periodontal_disease"] = {
    "diagnosis_ja": (
        "口腔内診察で歯肉発赤・腫脹・退縮、歯石沈着、口臭を確認。"
        "全身麻酔下でプロービング（歯周ポケット深度測定、正常<3mm）、歯の動揺度評価（Grade 0-3）。"
        "歯科X線（全顎）で歯槽骨吸収の程度・パターン（水平/垂直）を評価。"
        "Stage 1（歯肉炎）～Stage 4（骨吸収>50%+歯根露出）の4段階分類。"
        "小型犬は大型犬より進行が早い。口鼻瘻管、下顎骨折のリスク評価。"
    )
}

ENRICHMENTS["dog_tooth_abscess"] = {
    "diagnosis_ja": (
        "顔面腫脹（特に眼窩下：上顎第4前臼歯根尖膿瘍）、眼下排膿瘻管、食欲低下、片側咀嚼。"
        "口腔内診察で罹患歯の変色・破折・歯肉腫脹。歯科X線で根尖周囲の透過性亢進（ハロー）を確認。"
        "歯髄活力テスト（冷刺激/電気的）。CBC/生化学で炎症マーカー確認。"
        "上顎臼歯根尖膿瘍は眼窩蜂窩織炎、鼻腔内浸潤との鑑別が必要。"
        "細菌培養・感受性試験で嫌気性菌を含む起因菌同定。"
    )
}

ENRICHMENTS["dog_insulinoma"] = {
    "diagnosis_ja": (
        "空腹時低血糖（<60 mg/dL）と同時測定の血清インスリン高値（不適切分泌）で強く疑診。"
        "修正インスリン/グルコース比（AIGR）>30で診断的。72時間絶食試験で低血糖を誘発し確認。"
        "腹部エコー/造影CTで膵臓腫瘤描出（しばしば<2cm、検出困難）。"
        "術中エコーで膵臓全体の精査。肝転移の有無を評価。"
        "中～大型犬の中高齢に好発。発作、後肢虚脱、振戦が主徴。"
    )
}

ENRICHMENTS["dog_hyperparathyroidism"] = {
    "diagnosis_ja": (
        "持続的な高Ca血症（iCa>1.4 mmol/L、総Ca>12 mg/dL）で疑診。"
        "intact PTH高値+高Ca=原発性副甲状腺機能亢進症（PHPT）。頸部エコーで副甲状腺腫大を描出。"
        "腎性二次性ではPTH高値+低Ca+高P+BUN/Cre上昇。栄養性ではCa/P不均衡の食餌歴。"
        "尿中Ca排泄（Ca/Cre比）、腎臓エコー（腎石灰化）、骨密度評価。"
        "PTHrP測定で悪性腫瘍関連高Ca血症（HHM：リンパ腫、肛門嚢腺癌）を除外。"
    )
}

ENRICHMENTS["dog_fanconi_syndrome"] = {
    "diagnosis_ja": (
        "多飲多尿、体重減少、筋力低下で受診。血液ガスで代謝性アシドーシス（非AG型）。"
        "尿検査: 糖尿（血糖正常）、アミノ酸尿、リン酸尿、重炭酸尿、低比重尿。"
        "尿中電解質（Na, K, P, 重炭酸）排泄亢進。血清: 低P、低K、代謝性アシドーシス。"
        "バセンジーに好発（遺伝性、遺伝子検査利用可能）。後天性の原因: 銅蓄積症、"
        "薬剤性（ゲンタマイシン）、腫瘍関連。腎生検で近位尿細管変性を確認。"
    )
}

ENRICHMENTS["dog_ectopic_ureter"] = {
    "diagnosis_ja": (
        "若齢犬（特に雌）の持続性/間欠性尿失禁で疑診。通常の排尿行動も認める場合がある。"
        "腹部エコーで水腎症・拡張尿管の有無を評価。排泄性静脈性尿路造影（IVP）で尿管走行を確認。"
        "CT尿路造影が最も正確（尿管開口部の位置同定、感度95%）。膀胱鏡で尿管口の直接観察。"
        "片側性約60%、両側性約40%。好発犬種: ゴールデンレトリバー、ラブラドール、"
        "シベリアンハスキー。尿培養で二次的UTIの評価。"
    )
}

ENRICHMENTS["dog_rabies"] = {
    "diagnosis_ja": (
        "狂犬病ウイルス曝露歴（野生動物咬傷、渡航歴）と進行性神経症状で臨床的に疑診。"
        "生前確定診断は困難：皮膚生検（後頸部毛包）のDFA（蛍光抗体法）、唾液のRT-PCR。"
        "死後診断: 脳組織（海馬、小脳）のDFAが標準法。Negri小体（細胞質内封入体）の組織学的確認。"
        "日本では1957年以降国内発生なし（清浄国）だが、輸入症例に注意。"
        "狂犬病予防法に基づく届出義務あり。人畜共通感染症として公衆衛生上最重要。"
    )
}

ENRICHMENTS["dog_canine_herpesvirus_chv"] = {
    "diagnosis_ja": (
        "新生子犬（<3週齢）の突然の衰弱、鳴き声、低体温、出血性下痢、無乳で疑診。"
        "剖検で腎臓・肝臓・肺の点状出血・壊死巣が特徴的。PCR（口腔・鼻腔スワブ、臓器）で確定。"
        "血清学: VN法で母犬の抗体価測定（感染歴確認）。成犬では不顕性～軽度上気道症状。"
        "妊娠犬の感染は流産・死産・胎児奇形の原因。成犬の潜伏感染は三叉神経節に持続。"
        "繁殖犬舎での新生子致死率は極めて高い（無治療で80-100%）。"
    )
}

ENRICHMENTS["dog_canine_papillomatosis"] = {
    "diagnosis_ja": (
        "若齢犬（<2歳）の口腔内・口唇・舌の多発性乳頭状腫瘤で臨床診断。"
        "典型的なカリフラワー様外観。組織学的にコイロサイトーシス（空胞化細胞）を確認。"
        "PCR/ISHでイヌパピローマウイルス（CPV-1が最多）の型同定。"
        "免疫抑制犬では退縮遅延・悪性転化（SCC）のリスクあり。"
        "通常6-12週で自然退縮（免疫応答）。眼瞼・趾間・性器型の鑑別。"
    )
}

ENRICHMENTS["dog_brucellosis"] = {
    "diagnosis_ja": (
        "繁殖犬の流産（妊娠45-55日目）、死産、精巣上体炎、椎間板脊椎炎で疑診。"
        "スクリーニング: RSAT（迅速スライド凝集試験）またはIDEXX 4Dx内部抗体。"
        "確定: 血液培養（Brucella canis、培養4-6週）、定量的ME-TAT（2-メルカプトエタノール管凝集試験）。"
        "PCR（血液）で迅速確認可能。偽陽性が多いため連続検査が必要。"
        "人畜共通感染症（ヒトへの感染リスク）。繁殖犬の検査プログラムが重要。"
    )
}

ENRICHMENTS["dog_rocky_mountain_spotted_fever"] = {
    "diagnosis_ja": (
        "ダニ曝露歴+急性発熱、点状出血、関節痛、浮腫、血小板減少で疑診。"
        "急性期/回復期ペア血清のIFA（間接蛍光抗体法）で4倍以上の抗体価上昇で確定。"
        "全血PCR（Rickettsia rickettsii）で急性期の早期診断。"
        "CBC: 血小板減少、白血球減少→白血球増加。生化学: 低Na、低Alb、ALP/ALT上昇。"
        "CRP著増。皮膚生検で血管炎・免疫蛍光法で菌体検出。"
        "北米（特に東部）の流行地域での発生。日本では紅斑熱群リケッチア症との鑑別が重要。"
    )
}

ENRICHMENTS["dog_tetanus"] = {
    "diagnosis_ja": (
        "外傷歴（特に穿通創・壊死組織）と進行性筋硬直で臨床診断。牙関緊急（開口困難）、"
        "痙笑（耳直立・口角後退）、四肢伸展硬直、後弓反張が特徴的。"
        "確定診断検査は通常不要（臨床徴候で診断）。創傷部の嫌気性培養でC. tetaniを分離可能だが感度低い。"
        "血清中抗毒素抗体は犬では通常低値。CK上昇（筋障害）、血液ガスで呼吸不全評価。"
        "犬は人やウマに比べ感受性が低いが、発症時の致死率は高い。"
    )
}

ENRICHMENTS["dog_nocardiosis"] = {
    "diagnosis_ja": (
        "慢性排膿性病変（皮膚、胸腔、腹腔）で疑診。免疫抑制状態が素因。"
        "膿汁の細胞学: 化膿性肉芽腫性炎症、フィラメント状分岐グラム陽性桿菌。"
        "修正Kinyoun（弱抗酸性）染色陽性がActinomycesとの鑑別に有用。"
        "好気性培養（Nocardia spp.、培養2-4週要）。"
        "胸部X線/CTで膿胸、肺結節、胸壁洞管を評価。生検組織のPCRで菌種同定。"
    )
}

ENRICHMENTS["dog_actinomycosis"] = {
    "diagnosis_ja": (
        "顎顔面部の慢性腫脹・瘻管形成、胸腔/腹腔の膿瘍で疑診。植物の芒刺（awn）吸入・嚥下歴。"
        "膿汁中の硫黄顆粒（sulfur granules）を肉眼/顕微鏡で確認。"
        "嫌気性培養（Actinomyces spp.、培養5-14日）。Nocardiaと異なり弱抗酸性染色陰性。"
        "CT/エコーで膿瘍の範囲・洞管の走行を評価。胸腔穿刺液のシトロジー。"
        "口腔内外傷、歯科疾患が入口門となることが多い。"
    )
}

ENRICHMENTS["dog_blastomycosis"] = {
    "diagnosis_ja": (
        "肺結節/間質パターン（X線）、ブドウ膜炎、皮膚排膿性結節、リンパ節腫大で疑診。"
        "FNA/生検の細胞学: 広基底出芽（broad-based budding）を示す厚壁酵母（8-20μm）が特徴的。"
        "尿中Blastomyces抗原検査（EIA、感度93%）が非侵襲的で有用。"
        "血清抗体検査（寒天ゲル内拡散法）は感度が低い。培養は危険（BSL-3）で通常行わない。"
        "北米五大湖・オハイオ/ミシシッピ渓谷の流行地域。日本での発生は稀。"
    )
}

ENRICHMENTS["dog_histoplasmosis"] = {
    "diagnosis_ja": (
        "慢性下痢（大腸性）、体重減少、発熱、肝脾腫、貧血で疑診。肺型は咳・呼吸困難。"
        "直腸掻爬/結腸生検の細胞学: マクロファージ内に2-4μmの小型酵母（Histoplasma capsulatum）を検出。"
        "FNA（リンパ節、肝臓、脾臓、骨髄）でも検出可能。"
        "尿中/血清中Histoplasma抗原検査（EIA）で迅速診断。胸部X線でびまん性間質パターン。"
        "北米オハイオ/ミシシッピ渓谷の流行地域。日本では稀だが輸入症例に注意。"
    )
}

ENRICHMENTS["dog_coccidioidomycosis_valley_fever"] = {
    "diagnosis_ja": (
        "骨溶解性病変（長骨・椎体）、慢性咳嗽、発熱、リンパ節腫大、ブドウ膜炎で疑診。"
        "FNA/生検の細胞学: 内生胞子を含む球状体（spherule、20-200μm）が病理学的に確定的。"
        "血清学: AGID（寒天ゲル内拡散）でTP抗体・CF抗体。IgM（急性期）→IgG（慢性期）。"
        "CF抗体価は疾患活動性と相関し治療モニタリングに有用。"
        "骨X線でびまん性骨膜反応・溶解性病変。米国南西部の流行地域。日本では輸入症例のみ。"
    )
}

ENRICHMENTS["dog_cryptococcosis"] = {
    "diagnosis_ja": (
        "鼻腔内腫瘤、中枢神経症状（発作、旋回、失明）、皮膚結節で疑診。犬では鼻腔型が最多。"
        "ラテックス凝集試験（血清/CSF中莢膜抗原）が高感度・高特異度のスクリーニング。"
        "FNA/生検: 墨汁染色で厚い莢膜に囲まれた酵母を確認。PAS/GMS染色でも検出可能。"
        "培養（Cryptococcus neoformans/gattii）で菌種同定。CSF分析（CNS型）: 単核球優位の細胞増多。"
        "頭部CT/MRIで鼻腔内腫瘤・脳病変を評価。C. gattiiは免疫正常犬でも発症。"
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
