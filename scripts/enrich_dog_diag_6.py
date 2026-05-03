#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_aspergillosis"] = {
    "diagnosis_ja": (
        "鼻腔型: 慢性片側性鼻汁（粘液膿性→出血性）、鼻鏡脱色素。鼻腔X線/CTで鼻甲介融解・前頭洞混濁。"
        "鼻腔鏡で白色～緑色の真菌プラーク（fungal plaque）を直視確認+生検。"
        "Aspergillus抗体検査（AGID/ELISA）。播種型（ジャーマンシェパードに好発）は椎間板脊椎炎、"
        "腎炎、眼病変を呈し、尿中ガラクトマンナン抗原やβ-D-グルカン測定が有用。"
    )
}

ENRICHMENTS["dog_sporotrichosis"] = {
    "diagnosis_ja": (
        "皮膚リンパ管型: 外傷部位から所属リンパ節に沿った結節性病変・瘻管形成。"
        "FNA/生検の細胞学: 化膿性肉芽腫性炎症内にシガー型酵母（2-6μm、検出困難）。"
        "PAS/GMS染色で検出率向上。培養（Sporothrix schenckii、25℃で糸状菌、37℃で酵母）が確定。"
        "PCRで菌種同定。人畜共通感染症で飼い主への感染リスクあり。"
        "猫からの伝播が最も多い（犬は比較的抵抗性）。"
    )
}

ENRICHMENTS["dog_leishmaniasis"] = {
    "diagnosis_ja": (
        "皮膚症状（非掻痒性鱗屑性皮膚炎、潰瘍、爪過長）+全身症状（体重減少、リンパ節腫大、脾腫）で疑診。"
        "血清学: IFAT（抗体価≥1:160で陽性）、定量的ELISA。骨髄/リンパ節/皮膚FNAで"
        "マクロファージ内にLeishmania amastigotes（2-4μm、キネトプラスト保有）を検出。"
        "リアルタイムPCR（血液/骨髄）で高感度検出。CBC: 非再生性貧血、血小板減少。"
        "生化学: 高グロブリン血症（γ-グロブリン）、低アルブミン、蛋白尿。地中海沿岸の流行地域。"
    )
}

ENRICHMENTS["dog_neosporosis"] = {
    "diagnosis_ja": (
        "子犬の進行性後肢麻痺（上行性LMN→UMN）、筋萎縮、関節拘縮（hyperextension）が特徴的。"
        "成犬では多巣性CNS疾患（発作、旋回、脳幹徴候）。"
        "血清学: IFA（抗Neospora caninum抗体）、ペア血清で4倍上昇。CSF分析で単核球増多。"
        "筋生検でタキゾイト/シストの組織学的確認、免疫組織化学（抗Nc抗体）で確定。"
        "PCR（CSF、血液、組織）で遺伝子検出。垂直感染（経胎盤）が主経路。"
    )
}

ENRICHMENTS["dog_toxoplasmosis"] = {
    "diagnosis_ja": (
        "免疫抑制犬の発熱、筋炎、肺炎、肝炎、脳炎で疑診。犬での臨床発症は稀。"
        "血清学: IgM上昇（急性感染）+IgG（慢性/曝露歴）。ペア血清で4倍以上のIgG上昇で活動性感染。"
        "CSF分析で単核球増多、蛋白上昇。筋生検/臓器生検でタキゾイトの組織学的確認。"
        "PCR（血液、CSF、組織）でToxoplasma gondii DNA検出。"
        "鑑別: Neospora caninumとの血清学的交差反応に注意（種特異的抗体検査で鑑別）。"
    )
}

ENRICHMENTS["dog_hepatozoonosis"] = {
    "diagnosis_ja": (
        "H. canis型: 無症状～軽度。H. americanum型: 高熱、筋痛（背部過敏）、"
        "骨膜増殖（X線で骨幹部骨膜反応）、好中球著増（20,000-200,000/μL）。"
        "血液塗抹で好中球内のgamont（楕円形、11×5μm）を検出（感度低い）。"
        "筋生検（半腱様筋/大腿二頭筋）でメロゾイトのオニオンスキン型シスト確認（H. americanum）。"
        "PCR（18S rRNA）で種同定。ALP著増、低アルブミン。マダニ（ヘモフィサリス）の経口摂取で感染。"
    )
}

ENRICHMENTS["dog_roundworm_infection_toxocara"] = {
    "diagnosis_ja": (
        "糞便検査（浮遊法: 硫酸亜鉛/飽和食塩水）でToxocara canis虫卵を検出（亜球形、75-90μm、暗色厚殻）。"
        "子犬: 腹部膨満、発育不良、嘔吐（成虫嘔出あり）、下痢、被毛粗剛。"
        "重度感染で腸閉塞・腸穿孔のリスク。肺移行期に咳嗽。"
        "CBC: 好酸球増加。経胎盤・経乳感染で生後2-3週から感染。"
        "人畜共通感染症（幼虫移行症: VLM/OLM）としての公衆衛生的意義。"
    )
}

ENRICHMENTS["dog_hookworm_infection"] = {
    "diagnosis_ja": (
        "糞便検査（浮遊法）でAncylostoma caninum虫卵を検出（楕円形、56-75×34-47μm、桑実期）。"
        "子犬: 重度鉄欠乏性貧血（PCV<15%）、タール便/血便、衰弱。成犬: 慢性体重減少、軟便。"
        "CBC: 小球性低色素性貧血、網赤血球増加。血清鉄低値、TIBC上昇。"
        "経皮感染で足底皮膚炎（地面回虫幼虫移行症）。経乳感染あり。"
        "便潜血検査陽性。重度感染子犬では輸血が必要な場合あり。"
    )
}

ENRICHMENTS["dog_whipworm_infection_trichuris"] = {
    "diagnosis_ja": (
        "糞便検査（浮遊法、硫酸亜鉛推奨）でTrichuris vulpis虫卵を検出（レモン型/樽型、"
        "72-90×32-40μm、両極栓）。間欠的排卵のため複数回検査推奨。"
        "慢性大腸性下痢（粘液血便）、体重減少、しぶり。"
        "重度感染: 低Na/高K（Addison病様電解質異常、偽アジソン）→ACTH刺激試験で鑑別。"
        "盲腸の大腸鏡検査で虫体（鞭状）の直接確認も可能。"
    )
}

ENRICHMENTS["dog_tapeworm_infection_dipylidium_echinococcus"] = {
    "diagnosis_ja": (
        "肛門周囲/糞便中のDipylidium caninum片節（米粒様、運動性あり）を肉眼確認で診断。"
        "虫卵は卵嚢内に15-25個集合（浮遊法では検出困難）。"
        "Echinococcus granulosus/multilocularis: 糞便抗原検査（コプロ抗原ELISA）、糞便PCR。"
        "虫卵の形態はTaenia属と区別不能。駆虫後の虫体同定で確定。"
        "エキノコックスは人畜共通感染症として極めて重要（北海道で流行）。届出義務あり。"
    )
}

ENRICHMENTS["dog_ear_mite_infestation_otodectes"] = {
    "diagnosis_ja": (
        "激しい耳掻痒、頭部振盪、暗褐色～黒色のコーヒー残渣様耳垢。"
        "耳垢の直接鏡検（ミネラルオイル法）でOtodectes cynotis成虫/幼虫/虫卵を確認。"
        "耳鏡検査で外耳道内に白色の運動する虫体を直視可能。"
        "二次的細菌/酵母性外耳炎の合併評価（耳垢細胞診）。"
        "同居動物への伝播が高い。外耳以外の異所性感染（頸部、臀部）にも注意。"
    )
}

ENRICHMENTS["dog_flea_allergy_dermatitis"] = {
    "diagnosis_ja": (
        "腰背部～尾根部の激しい掻痒、脱毛、丘疹性皮膚炎が特徴的分布。"
        "ノミ糞（黒色粒子を湿らせると赤褐色に溶出）の検出、ノミ成虫の確認。"
        "皮内反応試験（ノミ抗原）で即時型+遅延型反応。血清IgE検査（ノミ特異的）。"
        "皮膚掻爬/毛検でDemodex/Sarcoptes等の外部寄生虫を除外。"
        "1匹のノミ刺咬で症状誘発（アレルギー個体）。同居動物・環境中のノミ駆除が必須。"
    )
}

ENRICHMENTS["dog_sarcoptic_mange_scabies"] = {
    "diagnosis_ja": (
        "激しい掻痒（ステロイド不応性）、耳介辺縁・肘・飛節の痂皮性皮膚炎。"
        "耳介-足反射（pinnalpedal reflex）陽性が高度に示唆的（感度82%）。"
        "皮膚掻爬（複数部位、深部）でSarcoptes scabiei虫体/虫卵/糞粒を検出（感度20-50%と低い）。"
        "血清抗Sarcoptes IgG（ELISA）が陰性掻爬例で有用（感度92%、発症3-5週後に陽性化）。"
        "試験的駆虫（イベルメクチン/セラメクチン）への反応で間接的に診断。人畜共通。"
    )
}

ENRICHMENTS["dog_cheyletiellosis_walking_dandruff"] = {
    "diagnosis_ja": (
        "背部の大量のフケ（鱗屑）、軽度掻痒。「歩くフケ」の異名（虫体の移動）。"
        "セロファンテープ法/浅層皮膚掻爬でCheyletiella yasguri虫体（大型、380μm、"
        "特徴的な鉤爪状付属肢）/虫卵を検出。ノミ櫛でも回収可能。"
        "ルーペ/拡大鏡でフケの中の虫体移動を直視確認。人畜共通（飼い主の丘疹性皮膚炎）。"
        "同居動物（犬猫ウサギ）全頭の検査・治療が必要。"
    )
}

ENRICHMENTS["dog_ectropion"] = {
    "diagnosis_ja": (
        "下眼瞼の外反による結膜露出、慢性結膜炎、流涙、角膜乾燥/色素沈着。"
        "眼科検査: シルマー涙液試験、フルオレセイン染色（角膜潰瘍除外）、前眼部検査。"
        "品種素因（セントバーナード、ブラッドハウンド、バセットハウンド等の大型犬）と"
        "後天性（瘢痕性、神経性、加齢性）の鑑別。"
        "瞼裂の長さ・弛緩度の評価。エントロピオンとの複合型（ダイヤモンドアイ）にも注意。"
    )
}

ENRICHMENTS["dog_distichiasis"] = {
    "diagnosis_ja": (
        "マイボーム腺開口部からの異常睫毛（distichia）を細隙灯顕微鏡で確認。"
        "流涙、眼瞼痙攣、結膜充血が主徴。フルオレセイン染色で角膜上皮障害を評価。"
        "アメリカンコッカースパニエル、イングリッシュコッカースパニエル、"
        "ミニチュアダックスフンド等に好発。毛の太さ・剛性・数で症状の重症度が異なる。"
        "異所性睫毛（ectopic cilia：結膜面から生える単一の剛毛）との鑑別が重要。"
    )
}

ENRICHMENTS["dog_nuclear_sclerosis"] = {
    "diagnosis_ja": (
        "6歳以上の犬で左右対称性の水晶体核部の青灰色混濁。散瞳下で直接検眼鏡にて"
        "眼底透見可能（白内障との重要な鑑別点）。細隙灯検査で核部の圧縮硬化を確認。"
        "視力は通常維持される。加齢性の水晶体線維圧縮による正常な変化。"
        "白内障（眼底透見不能、視力低下）との鑑別が最も重要。"
        "治療不要だが飼い主への説明（白内障ではない）が必要。"
    )
}

ENRICHMENTS["dog_retinal_dysplasia"] = {
    "diagnosis_ja": (
        "散瞳下の眼底検査で網膜のひだ状変化（fold）、ロゼット形成、網膜剥離を確認。"
        "ERG（網膜電図）で網膜機能を客観的に評価。エコー検査で完全網膜剥離を確認。"
        "多巣性型（folds）は軽度で視力影響少。地理的型は局所的視野欠損。"
        "完全型は両側性網膜剥離で失明。遺伝性（ラブラドール、スプリンガースパニエル、"
        "ベドリントンテリア）と後天性（子宮内感染: ヘルペス、パルボ）の鑑別。"
    )
}

ENRICHMENTS["dog_pannus_chronic_superficial_keratitis"] = {
    "diagnosis_ja": (
        "角膜辺縁（通常腹外側→中心に進展）からの血管新生+色素沈着+肉芽組織浸潤。"
        "両側性。細隙灯検査で角膜浅層の血管新生・混濁・色素沈着の程度を評価。"
        "角膜細胞診でリンパ球・形質細胞浸潤（免疫介在性角膜炎）。"
        "ジャーマンシェパード、ベルジアンシェパードに好発。紫外線曝露（高地居住）が増悪因子。"
        "瞬膜型（plasmoma：瞬膜の色素沈着・肥厚）の合併を評価。生涯にわたる治療管理。"
    )
}

ENRICHMENTS["dog_uveitis"] = {
    "diagnosis_ja": (
        "縮瞳、眼痛（眼瞼痙攣）、前房フレア/蓄膿、結膜・毛様充血、眼圧低下。"
        "細隙灯検査で前房内フレア/細胞（Tyndall現象）、虹彩後癒着（posterior synechia）を評価。"
        "眼圧測定（通常低値、<10mmHg）。原因検索: CBC/生化学、"
        "感染症スクリーニング（Ehrlichia/Leishmania/Brucella/Leptospira/Toxoplasma抗体/PCR）、"
        "胸部X線（リンパ腫、真菌症）、レンズ誘発性（白内障関連）、外傷性、特発性の鑑別。"
    )
}

ENRICHMENTS["dog_corneal_dystrophy"] = {
    "diagnosis_ja": (
        "角膜中央～傍中央の両側対称性の白色～灰白色混濁。非炎症性、非進行性（または緩徐進行）。"
        "細隙灯検査で上皮型/実質型/内皮型を分類。実質型が最多（脂質/コレステロール沈着）。"
        "血清脂質パネル（コレステロール、TG）で高脂血症の除外。"
        "内皮型は進行性角膜浮腫を呈し、スペキュラーマイクロスコピーで内皮細胞密度低下を確認。"
        "好発犬種: シベリアンハスキー（実質型）、ボストンテリア（内皮型）、シェルティ。"
    )
}

ENRICHMENTS["dog_collie_eye_anomaly_cea"] = {
    "diagnosis_ja": (
        "生後6-8週の散瞳下眼底検査で脈絡膜低形成（CRH: 視神経乳頭外側の淡色/菲薄化領域）を確認。"
        "重度: コロボーマ（視神経乳頭のpit/ectasia）、網膜剥離、眼内出血。"
        "遺伝子検査（NHEJ1/CEA変異: OptiGen）で保因者/罹患犬を同定。常染色体劣性遺伝。"
        "好発犬種: コリー（有病率70-90%）、シェルティ、ボーダーコリー、オーストラリアンシェパード。"
        "「Go normal」現象（色素沈着で8-12週以降にCRHが隠される）に注意→早期検査が重要。"
    )
}

ENRICHMENTS["dog_horner's_syndrome"] = {
    "diagnosis_ja": (
        "縮瞳（miosis）、眼瞼下垂（ptosis）、眼球陥凹（enophthalmos）、瞬膜突出の4徴候。"
        "フェニレフリン点眼試験: 0.1%希釈→20分以内に散瞳=節後性（3次ニューロン）、"
        "1%→散瞳=節前性（2次）、不応=中枢性（1次）。"
        "原因検索: 耳鏡検査（中耳炎が犬で最多原因）、頸部/胸部X線/CT（腫瘤、外傷）、"
        "脳幹MRI（中枢性）。約50%が特発性（ゴールデンレトリバーに多い）。"
    )
}

ENRICHMENTS["dog_sudden_acquired_retinal_degeneration_sards"] = {
    "diagnosis_ja": (
        "急性（数日～2週間）の完全失明で受診。散瞳（対光反射消失）だが眼底は初期正常。"
        "ERG（網膜電図）で消失型（flat ERG）が確定診断—最も重要な検査。"
        "眼底検査は初期正常→数週～数ヶ月後にタペタム反射亢進、血管狭細化、視神経乳頭蒼白。"
        "全身症状（多飲多尿、多食、肥満）を30-50%で伴う→副腎機能検査でCushing様を除外。"
        "中高齢の雌犬（ダックスフンド、ミニチュアシュナウザー、パグ）に好発。視力回復なし。"
    )
}

ENRICHMENTS["dog_sick_sinus_syndrome"] = {
    "diagnosis_ja": (
        "失神/虚脱発作+心電図で洞徐脈、洞停止、洞房ブロックの単独または複合。"
        "ホルター心電図（24時間）で間欠的不整脈の検出・定量化。"
        "徐脈-頻脈症候群（Brady-tachy syndrome）: 洞停止後に上室性頻脈が出現するパターン。"
        "アトロピン反応試験: 0.04mg/kg IV→HR上昇<150bpmで洞結節機能不全を示唆。"
        "好発犬種: ミニチュアシュナウザー、ウエストハイランドホワイトテリア、コッカースパニエル。"
        "心エコーで器質的心疾患を除外。"
    )
}

ENRICHMENTS["dog_ventricular_septal_defect_vsd"] = {
    "diagnosis_ja": (
        "聴診で右胸骨縁の全収縮期雑音（grade III-V/VI）。小欠損ほど高調・大音量。"
        "心エコー（2D+カラードプラ）で欠損孔の位置（膜性部が最多）、サイズ、シャント方向を評価。"
        "Qp/Qs比でシャント量を定量。胸部X線: 小欠損は正常、大欠損は肺過灌流+左房/左室拡大。"
        "心電図: 大欠損で左室肥大パターン。心臓カテーテル検査で肺動脈圧・肺血管抵抗測定。"
        "アイゼンメンジャー症候群（シャント逆転→チアノーゼ）への進展を評価。"
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
