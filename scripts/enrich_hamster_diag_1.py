#!/usr/bin/env python3
"""Enrich diagnosis_ja for the first 50 Hamster diseases with disease-specific
diagnostic protocols.  Each entry uses hamster-specific considerations:
- Small blood volume (max 0.5-1 mL; safe limit <1% BW = ~0.3-0.4 mL for 30-40g)
- Rapid metabolism and short anesthesia windows
- Hibernation vs hypothermia distinction (torpor at <15 C)
- Cheek pouch impaction/eversion
- Wet tail (proliferative ileitis / Lawsonia intracellularis)
- Adrenal tumors (common in aged hamsters)
- Species: Syrian (120-150g) vs Dwarf (30-50g) size differences
"""

import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ── hamster_fracture_limb  Limb Fracture ──────────────────────────────────
ENRICHMENTS["hamster_fracture_limb"] = {
    "diagnosis_ja": (
        "身体検査で患肢の腫脹・疼痛・不自然な可動性・捻髪音を評価。"
        "全身X線（VD・lateral）で骨折部位・骨折型（横骨折・螺旋骨折・粉砕骨折）を確認。"
        "CT検査は複雑骨折や関節内骨折の評価に有用。CBC・血液生化学（採血量は体重の1%以下、"
        "ドワーフ種で最大0.3-0.4 mL）で全身状態・感染兆候を評価。"
        "開放骨折では創傷スワブの細菌培養・感受性試験を実施。"
        "飼育環境（回し車・ケージ金網・落下事故）の聴取が原因特定に重要"
    )
}

# ── hamster_0133  Pneumocystis Infection ───────────────────────────────────
ENRICHMENTS["hamster_0133"] = {
    "diagnosis_ja": (
        "呼吸困難・体重減少の臨床評価。胸部X線でびまん性間質性肺パターンを確認。"
        "気管洗浄液のギムザ染色またはGMS（グロコット）染色でPneumocystis嚢子体を検出。"
        "PCR検査でPneumocystis carinii/murina DNAを確認。CBC（採血量≤体重の1%、"
        "最大0.5-1 mL）でリンパ球減少・免疫抑制状態を評価。血液生化学でTP低下・"
        "Alb低下を確認。基礎疾患（副腎腫瘍・リンパ腫等の免疫抑制原因）の精査が重要。"
        "剖検例では肺の泡沫状好酸性滲出物中の嚢子体確認が確定診断"
    )
}

# ── hamster_cryptorchidism  Cryptorchidism ────────────────────────────────
ENRICHMENTS["hamster_cryptorchidism"] = {
    "diagnosis_ja": (
        "身体検査で陰嚢内精巣の触診を実施（シリアンハムスターの精巣は体格に比して大きく、"
        "正常では明瞭に触知可能）。鼠径管・腹腔内の停留精巣を触診で検索。"
        "腹部超音波で腹腔内停留精巣の位置・サイズ・エコーパターンを評価（腫瘍化の有無）。"
        "CBC・血液生化学（採血量≤体重の1%）で全身状態を確認。"
        "テストステロン測定で性腺機能を評価。腹腔内停留精巣はセルトリ細胞腫・"
        "精上皮腫のリスクが高いため、超音波での定期モニタリングまたは早期去勢を検討"
    )
}

# ── hamster_0084  Pyometra ────────────────────────────────────────────────
ENRICHMENTS["hamster_0084"] = {
    "diagnosis_ja": (
        "陰部からの膿性～血性分泌物・腹部膨満・多飲多尿・沈鬱の臨床評価。"
        "腹部超音波で子宮角の液体貯留・子宮壁肥厚を確認。腹部X線で拡張した子宮陰影を評価。"
        "CBC（採血量≤体重の1%、最大0.5-1 mL）で好中球増加（左方移動）・毒性変化を確認。"
        "血液生化学でBUN・Cre上昇（腎障害合併）・肝酵素上昇を評価。"
        "分泌物の細菌培養・感受性試験でE. coli等の原因菌を同定。"
        "高齢未避妊メスに好発（1.5歳以上）。敗血症のリスク評価が重要"
    )
}

# ── hamster_0085  Endometritis ────────────────────────────────────────────
ENRICHMENTS["hamster_0085"] = {
    "diagnosis_ja": (
        "陰部分泌物（膿性・血性）・不正出血の臨床評価。腹部超音波で子宮壁肥厚・"
        "子宮内液体貯留を確認（蓄膿症との鑑別）。CBC（採血量≤体重の1%）で"
        "好中球増加・左方移動を確認。血液生化学で炎症マーカー・肝腎機能を評価。"
        "分泌物の細胞診でヘテロフィル・変性好中球・細菌を確認。"
        "細菌培養・感受性試験で原因菌（E. coli, Streptococcus等）を同定。"
        "ホルモン検査でプロゲステロン値を評価（黄体期の子宮感受性亢進）。"
        "未避妊高齢メスでの発症が多く、子宮蓄膿症への進行リスクを考慮"
    )
}

# ── hamster_0086  Ovarian Cyst ────────────────────────────────────────────
ENRICHMENTS["hamster_0086"] = {
    "diagnosis_ja": (
        "腹部膨満・対称性脱毛・陰部腫脹の臨床評価。腹部超音波で卵巣領域の"
        "無エコー～低エコー嚢胞性病変を確認しサイズ・両側性を評価。"
        "腹部X線で軟部組織陰影の占拠を確認。CBC・血液生化学（採血量≤体重の1%）で"
        "全身状態を評価。エストラジオール・プロゲステロン測定で機能性嚢胞"
        "（ホルモン産生性）を判定。脱毛パターンが対称性の場合はエストロゲン産生性嚢胞を示唆。"
        "卵巣腫瘍（顆粒膜細胞腫等）との鑑別が重要で、外科切除検体の病理組織検査が確定診断"
    )
}

# ── hamster_0101  Uterine Leiomyoma ───────────────────────────────────────
ENRICHMENTS["hamster_0101"] = {
    "diagnosis_ja": (
        "腹部腫瘤触知・腹部膨満・陰部出血の臨床評価。腹部超音波で子宮壁由来の"
        "均一な低エコー腫瘤を確認しサイズ・血流を評価。腹部X線で骨盤腔～腹腔内の"
        "軟部組織陰影を確認。CBC・血液生化学（採血量≤体重の1%、最大0.5-1 mL）で"
        "貧血（慢性出血時PCV低下）・全身状態を評価。FNA細胞診で紡錘形平滑筋細胞を"
        "確認（悪性の平滑筋肉腫との鑑別が必要）。確定診断は切除検体の病理組織検査。"
        "高齢未避妊メスに好発し、卵巣子宮摘出術が根治的治療"
    )
}

# ── hamster_0120  Wound Infection ─────────────────────────────────────────
ENRICHMENTS["hamster_0120"] = {
    "diagnosis_ja": (
        "創傷部の視診で発赤・腫脹・排膿・壊死組織を評価。創傷の深度・範囲を測定。"
        "創傷スワブの細菌培養・感受性試験で原因菌（Staphylococcus, Pasteurella等）を同定。"
        "CBC（採血量≤体重の1%、最大0.5-1 mL）で好中球増加・左方移動を確認。"
        "血液生化学で全身性炎症に伴う変化を評価。深部感染が疑われる場合はX線で"
        "骨髄炎・膿瘍形成を検索。咬傷歴（同居個体の攻撃性）の聴取が重要。"
        "ハムスターは闘争による咬傷創が多く、頬袋損傷の合併も確認"
    )
}

# ── hamster_0136  Cystic Ovary Disease ────────────────────────────────────
ENRICHMENTS["hamster_0136"] = {
    "diagnosis_ja": (
        "腹部膨満・対称性脱毛・持続的発情兆候の臨床評価。腹部超音波で卵巣の"
        "多嚢胞性変化（複数の無エコー嚢胞）を確認しサイズ・両側性を評価。"
        "腹部X線で占拠性病変の範囲を確認。CBC・血液生化学（採血量≤体重の1%）で"
        "貧血（エストロゲン過剰による骨髄抑制）・肝機能を評価。"
        "エストラジオール測定で機能性嚢胞を判定。"
        "エストロゲン過剰による再生不良性貧血のリスクがあり、PCV低下（<30%）時は緊急対応。"
        "卵巣腫瘍との鑑別に超音波ガイド下FNAまたは外科切除・病理が必要"
    )
}

# ── hamster_pregnancy_toxemia  Pregnancy Toxemia ──────────────────────────
ENRICHMENTS["hamster_pregnancy_toxemia"] = {
    "diagnosis_ja": (
        "妊娠末期～産後の急性沈鬱・食欲廃絶・運動失調・痙攣の臨床評価。"
        "血液生化学（採血量≤体重の1%）で低血糖（<60 mg/dL）・高ケトン血症・"
        "肝酵素上昇（ALT・AST）・高脂血症を確認。尿検査でケトン尿を検出。"
        "腹部超音波で胎仔の生存確認・肝臓のエコーパターン（脂肪肝）を評価。"
        "CBC で脱水に伴うPCV上昇を確認。血液ガスでアシドーシスを評価。"
        "肥満・多胎妊娠・ストレス・急激な食餌変更が誘因。"
        "シリアンハムスターに好発し、致死率が高いため早期発見が重要"
    )
}

# ── hamster_retained_fetus  Retained Fetus ────────────────────────────────
ENRICHMENTS["hamster_retained_fetus"] = {
    "diagnosis_ja": (
        "分娩後の持続的努責・陰部分泌物（血性・悪臭）・沈鬱・食欲不振の臨床評価。"
        "腹部X線で子宮内の胎仔骨格陰影を確認（分娩後24-48時間経過で疑診）。"
        "腹部超音波で残留胎仔の数・位置・生存兆候（心拍の有無）を評価。"
        "CBC（採血量≤体重の1%）で好中球増加・左方移動（子宮感染合併時）を確認。"
        "血液生化学でBUN・Cre・肝酵素・血糖値を評価。"
        "体温測定で発熱（感染）を確認。分娩歴・頭数の聴取で残留の推定。"
        "シリアンハムスターの妊娠期間（15-18日）を考慮して介入タイミングを判断"
    )
}

# ── hamster_uterine_endometrial_hyperplasia  Uterine Endometrial Hyperplasia ──
ENRICHMENTS["hamster_uterine_endometrial_hyperplasia"] = {
    "diagnosis_ja": (
        "不正出血・陰部分泌物・腹部膨満の臨床評価。腹部超音波で子宮内膜の"
        "びまん性肥厚・子宮内液体貯留を確認。腹部X線で子宮拡張像を評価。"
        "CBC・血液生化学（採血量≤体重の1%）で貧血（慢性出血時PCV低下）・全身状態を確認。"
        "分泌物の細胞診で上皮細胞の増殖パターンを評価。"
        "エストラジオール・プロゲステロン測定でホルモン異常を検索。"
        "確定診断は卵巣子宮摘出後の病理組織検査（嚢胞性過形成の程度・異型性の有無）。"
        "高齢未避妊メスに好発し、子宮内膜癌への進行リスクを考慮"
    )
}

# ── hamster_testicular_abscess  Testicular Abscess ────────────────────────
ENRICHMENTS["hamster_testicular_abscess"] = {
    "diagnosis_ja": (
        "陰嚢の片側性腫大・発赤・疼痛・波動感の臨床評価。精巣超音波で膿瘍腔"
        "（低エコー領域・辺縁高エコー被膜）を確認。CBC（採血量≤体重の1%、"
        "最大0.5-1 mL）で好中球増加・左方移動を確認。血液生化学で全身性炎症の"
        "マーカーを評価。膿汁のFNA・細菌培養・感受性試験で原因菌を同定"
        "（Staphylococcus, Pasteurella, E. coli等）。精巣腫瘍との鑑別が重要で、"
        "超音波所見の不均一性・壊死像を精査。咬傷創からの上行感染が多い"
    )
}

# ── hamster_spinal_compression  Spinal Cord Compression ──────────────────
ENRICHMENTS["hamster_spinal_compression"] = {
    "diagnosis_ja": (
        "後肢不全麻痺～完全麻痺・排尿障害・疼痛反応の神経学的検査。"
        "全身X線（VD・lateral）で椎体骨折・脱臼・椎間板変性・腫瘤性病変を検索。"
        "CT/MRI検査で脊髄圧迫の部位・程度・原因（椎間板ヘルニア・腫瘍・膿瘍）を特定。"
        "CBC・血液生化学（採血量≤体重の1%）で感染・腫瘍随伴症候群を評価。"
        "深部痛覚の有無が予後判定に重要（消失は予後不良）。"
        "膀胱触診で尿貯留を確認（神経原性膀胱）。外傷歴（落下・回し車の事故）の聴取。"
        "高齢ハムスターでは脊椎腫瘍の可能性も考慮"
    )
}

# ── hamster_0014  Dermatophytosis (Ringworm) ──────────────────────────────
ENRICHMENTS["hamster_0014"] = {
    "diagnosis_ja": (
        "円形脱毛・鱗屑・痂皮の皮膚所見を評価。Wood灯検査でMicrosporum canis感染時の"
        "黄緑色蛍光を確認（Trichophyton mentagrophytesは蛍光陰性）。"
        "皮膚掻破・被毛検査でKOH直接鏡検にて分節分生子・菌糸を検出。"
        "DTM培地（Dermatophyte Test Medium）またはSDA培地で真菌培養し菌種を同定。"
        "CBC（採血量≤体重の1%）で二次感染に伴う好中球増加を評価。"
        "皮膚生検・PAS染色で毛包内の菌糸・分生子を確認（慢性例）。"
        "人獣共通感染症のためハンドリング後の衛生管理と飼育者の皮膚病変の有無を確認"
    )
}

# ── hamster_0017  Sebaceous Gland Hyperplasia ─────────────────────────────
ENRICHMENTS["hamster_0017"] = {
    "diagnosis_ja": (
        "体側（腰部）の色素沈着・脂性分泌物・脱毛領域の視診。シリアンハムスターの"
        "腰部臭腺（flank glands / costovertebral glands）の肥大・分泌亢進を確認。"
        "オスに好発し、性ホルモン依存性の正常変異と病的過形成の鑑別が必要。"
        "FNA細胞診で脂腺細胞の増殖パターンを確認し腫瘍性変化を除外。"
        "皮膚生検・病理組織検査で脂腺の過形成と腺腫・腺癌を鑑別。"
        "CBC・血液生化学（採血量≤体重の1%）で全身状態を評価。"
        "テストステロン測定で性ホルモン依存性を確認（去勢による改善が期待される場合）"
    )
}

# ── hamster_0021  Contact Dermatitis ──────────────────────────────────────
ENRICHMENTS["hamster_0021"] = {
    "diagnosis_ja": (
        "腹部・四肢末端・口周囲の発赤・腫脹・痂皮形成の皮膚所見を評価。"
        "飼育環境の詳細聴取：床敷材（杉・松チップのフェノール刺激）・消毒剤・"
        "新しいケージ素材との接触歴を確認。皮膚掻破検査で寄生虫・真菌を除外。"
        "細菌培養で二次感染菌を検索。CBC（採血量≤体重の1%）で好酸球増加"
        "（アレルギー性）を評価。皮膚生検で表皮のスポンジオーシス・"
        "好酸球浸潤を確認（アレルギー性接触皮膚炎）。"
        "疑わしい刺激物を除去後の改善で臨床的に確認"
    )
}

# ── hamster_0108  Dental Abscess ──────────────────────────────────────────
ENRICHMENTS["hamster_0108"] = {
    "diagnosis_ja": (
        "顔面腫脹・流涎・食欲不振・体重減少の臨床評価。口腔内検査（短時間鎮静下）で"
        "歯肉腫脹・排膿・歯の動揺を確認。頭部X線で歯根周囲の骨溶解像・歯根膿瘍を評価。"
        "CT検査で膿瘍の範囲・骨破壊・眼窩/鼻腔への波及を精密評価。"
        "膿汁のFNA・細菌培養・感受性試験で原因菌を同定。"
        "CBC（採血量≤体重の1%、最大0.5-1 mL）で好中球増加を確認。"
        "血液生化学で全身状態を評価。頬袋の膿瘍との鑑別が必要（頬袋反転検査）。"
        "切歯過長・不正咬合の合併を評価"
    )
}

# ── hamster_0132  Ringworm (Trichophyton) ─────────────────────────────────
ENRICHMENTS["hamster_0132"] = {
    "diagnosis_ja": (
        "鼻先・耳介・四肢末端の円形脱毛・鱗屑・痂皮を評価。Wood灯検査は"
        "Trichophyton mentagrophytesでは蛍光陰性のため培養が必須。"
        "KOH直接鏡検で被毛の分節分生子（ectothrix型）を確認。"
        "DTM/SDA培地の真菌培養でT. mentagrophytesのコロニーを確認（白色粉状、2-3週間）。"
        "皮膚掻破検査でDemodex等の寄生虫を除外。CBC（採血量≤体重の1%）で"
        "二次感染の有無を評価。皮膚生検・PAS染色で毛包感染を確認。"
        "人獣共通感染症（ズーノーシス）のため飼育者・同居動物の皮膚検査も推奨"
    )
}

# ── hamster_dental_malocclusion  Dental Malocclusion ──────────────────────
ENRICHMENTS["hamster_dental_malocclusion"] = {
    "diagnosis_ja": (
        "食欲低下・流涎・体重減少・前歯の視認可能な変形の臨床評価。"
        "無麻酔での切歯の視診で過長・交叉・彎曲を確認。頭部X線で歯根の伸長方向・"
        "臼歯列の不整・歯根膿瘍を評価。CT検査で臼歯の鋭縁（スパー）・"
        "舌損傷・眼窩への歯根波及を精密評価。短時間鎮静下で耳鏡を用いた"
        "臼歯の直視検査（頬側・舌側のスパー）を実施。"
        "CBC・血液生化学（採血量≤体重の1%）で低栄養・脱水を評価。"
        "ハムスターは常生歯のため定期的な歯科検診が推奨される"
    )
}

# ── hamster_staphylococcal_dermatitis  Staphylococcal Dermatitis ──────────
ENRICHMENTS["hamster_staphylococcal_dermatitis"] = {
    "diagnosis_ja": (
        "皮膚の膿疱・痂皮・脱毛・びらんの臨床評価。皮膚スワブまたは膿汁の"
        "細菌培養・感受性試験でStaphylococcus aureus/S. xylosusを同定。"
        "皮膚掻破検査でDemodex等の合併寄生虫を除外。"
        "細胞診（スタンプ塗抹）でグラム陽性球菌・変性好中球を確認。"
        "CBC（採血量≤体重の1%）で好中球増加を評価。皮膚生検で"
        "膿疱・毛包炎の組織像を確認。飼育環境の清潔性・ストレス因子を聴取。"
        "免疫抑制（副腎腫瘍・クッシング病・高齢）が基礎にある場合は精査が必要"
    )
}

# ── hamster_fur_mites_demodex_criceti  Fur Mites (Demodex criceti) ────────
ENRICHMENTS["hamster_fur_mites_demodex_criceti"] = {
    "diagnosis_ja": (
        "背部・臀部の脱毛・鱗屑・乾燥した被毛の臨床評価。深部皮膚掻破検査で"
        "毛包内のDemodex criceti（短体型、犬のD. caniと異なる形態）を検出。"
        "毛抜き法（trichography）で毛包内の虫体を確認。"
        "CBC（採血量≤体重の1%）で好酸球増加を評価。"
        "免疫抑制状態（高齢・クッシング病・副腎腫瘍・栄養不良）の有無を精査"
        "（健常ハムスターでは不顕性感染が多く、免疫低下時に臨床症状が顕在化）。"
        "二次細菌感染の評価に細胞診・培養を実施。D. aurati との混合感染も考慮"
    )
}

# ── hamster_demodex_mange_-_localized  Demodex Mange - Localized ──────────
ENRICHMENTS["hamster_demodex_mange_-_localized"] = {
    "diagnosis_ja": (
        "臀部・背部・頭部の限局性脱毛・鱗屑の臨床評価（全身の5%未満の範囲）。"
        "深部皮膚掻破検査でDemodex criceti/D. aurati虫体を検出（出血するまで掻破）。"
        "虫体の形態観察でD. criceti（短体型）とD. aurati（長体型）を鑑別。"
        "CBC（採血量≤体重の1%）で全身状態を評価。"
        "限局型では免疫抑制の背景がない場合が多いが、全身型への進行を監視。"
        "二次感染の細菌培養・感受性試験を実施。"
        "飼育環境のストレス因子（過密飼育・温度変動）を聴取"
    )
}

# ── hamster_demodex_mange_-_generalized  Demodex Mange - Generalized ──────
ENRICHMENTS["hamster_demodex_mange_-_generalized"] = {
    "diagnosis_ja": (
        "広範囲（体表の5%以上）の脱毛・鱗屑・痂皮・紅斑の臨床評価。"
        "複数部位の深部皮膚掻破検査でDemodex虫体の大量検出を確認。"
        "毛抜き法で毛包内寄生密度を評価。CBC（採血量≤体重の1%）で"
        "免疫抑制マーカー（リンパ球減少）・二次感染の好中球増加を評価。"
        "血液生化学で副腎皮質機能亢進（クッシング病）・肝疾患・腫瘍性疾患を検索。"
        "副腎超音波で副腎腫大を確認。皮膚生検で毛包内虫体の大量寄生・"
        "毛包周囲の炎症を確認。全身型は基礎疾患の存在を強く示唆"
    )
}

# ── hamster_dental_overgrowth_molar  Dental Overgrowth (Molar) ────────────
ENRICHMENTS["hamster_dental_overgrowth_molar"] = {
    "diagnosis_ja": (
        "食欲低下・流涎・体重減少・頬の腫脹の臨床評価。短時間鎮静下で"
        "耳鏡を用いた臼歯の直視検査：頬側・舌側の鋭縁（スパー）・"
        "舌捕捉・頬粘膜潰瘍を確認。頭部X線（VD・lateral oblique）で"
        "臼歯列の不整・歯根の伸長・歯根膿瘍を評価。CT検査で歯根の"
        "骨貫通・眼窩/鼻腔への波及を精密評価。CBC・血液生化学"
        "（採血量≤体重の1%）で低栄養・脱水・感染を評価。"
        "ハムスターの臼歯は常生歯であり、不正咬合は進行性のため定期検診が必須"
    )
}

# ── hamster_pyoderma  Pyoderma ────────────────────────────────────────────
ENRICHMENTS["hamster_pyoderma"] = {
    "diagnosis_ja": (
        "皮膚の膿疱・表皮小環（epidermal collarette）・痂皮・脱毛の臨床評価。"
        "皮膚スワブの細胞診（スタンプ塗抹）で変性好中球・細胞内球菌を確認。"
        "細菌培養・感受性試験で原因菌（Staphylococcus aureus等）を同定。"
        "皮膚掻破検査で寄生虫（Demodex等）の合併を除外。"
        "CBC（採血量≤体重の1%）で好中球増加を確認。"
        "深在性膿皮症では皮膚生検で毛包炎・蜂窩織炎の組織像を確認。"
        "免疫抑制の基礎疾患（クッシング病・副腎腫瘍・高齢）の精査が重要"
    )
}

# ── hamster_0026  Squamous Cell Carcinoma ─────────────────────────────────
ENRICHMENTS["hamster_0026"] = {
    "diagnosis_ja": (
        "皮膚・口腔・頬袋の潰瘍性～増殖性腫瘤の臨床評価。FNA細胞診で"
        "角化傾向を伴う異型扁平上皮細胞を確認。切除生検・病理組織検査で"
        "組織型（高分化～低分化）・浸潤深度・脈管侵襲を確定。"
        "CBC・血液生化学（採血量≤体重の1%、最大0.5-1 mL）で全身状態・Ca値"
        "（腫瘍随伴性高Ca血症）を評価。頭部CT（口腔内発生時）で骨浸潤を精査。"
        "胸部X線で肺転移をスクリーニング。所属リンパ節のFNAで転移を評価。"
        "頬袋発生例は反転検査で腫瘤の全容を確認"
    )
}

# ── hamster_0035  Clostridiosis ───────────────────────────────────────────
ENRICHMENTS["hamster_0035"] = {
    "diagnosis_ja": (
        "急性水様性～血性下痢・腹部膨満・沈鬱・急死の臨床評価。"
        "糞便のグラム染色で大型グラム陽性芽胞桿菌（Clostridium属）を確認。"
        "糞便の嫌気性培養でClostridium difficile/C. perfringensを同定。"
        "毒素検査（C. difficile toxin A/B ELISA）で毒素産生を確認。"
        "CBC（採血量≤体重の1%）で好中球増加・脱水に伴うPCV上昇を確認。"
        "血液生化学で電解質異常・血糖低下・BUN上昇を評価。"
        "抗菌薬投与歴の聴取が重要（抗菌薬関連性腸炎としてペニシリン系・"
        "リンコマイシン系が誘因となる）"
    )
}

# ── hamster_tyzzer's_disease  Tyzzer's Disease ────────────────────────────
ENRICHMENTS["hamster_tyzzer's_disease"] = {
    "diagnosis_ja": (
        "急性水様性下痢・沈鬱・被毛粗剛・急死の臨床評価（特に離乳前後の若齢個体）。"
        "CBC（採血量≤体重の1%）で好中球増加を確認。血液生化学で肝酵素著増"
        "（ALT・AST）・血糖低下を評価。糞便PCRでClostridium piliforme DNAを検出。"
        "確定診断は剖検時の肝臓・腸管の病理組織検査：Warthin-Starry銀染色で"
        "肝細胞・腸上皮細胞内の細長いフィラメント状菌体を確認。"
        "肝臓の巣状壊死が特徴的。ストレス・過密飼育・不衛生環境が誘因。"
        "C. piliformeは培養困難なため病理・PCRが診断の主軸"
    )
}

# ── hamster_mycoplasma_infection  Mycoplasma Infection ────────────────────
ENRICHMENTS["hamster_mycoplasma_infection"] = {
    "diagnosis_ja": (
        "鼻汁・くしゃみ・呼吸促迫・ポルフィリン涙（赤色涙）の臨床評価。"
        "胸部X線で気管支周囲パターン・間質性肺パターン・肺胞パターンを評価。"
        "鼻腔・気管スワブのPCRでMycoplasma pulmonis DNAを検出。"
        "培養はPPLO培地（長期培養3-4週間必要）で実施。"
        "CBC（採血量≤体重の1%）で好中球増加・リンパ球増加を確認。"
        "血液生化学で全身状態を評価。中耳炎合併時は頭部X線/CTで鼓室の混濁を確認。"
        "慢性進行性であり、ストレス・アンモニア暴露が増悪因子"
    )
}

# ── hamster_pasteurellosis  Pasteurellosis ────────────────────────────────
ENRICHMENTS["hamster_pasteurellosis"] = {
    "diagnosis_ja": (
        "鼻汁・くしゃみ・眼周囲の膿性分泌物・皮下膿瘍の臨床評価。"
        "患部スワブの細菌培養・感受性試験でPasteurella pneumotropicaを同定。"
        "CBC（採血量≤体重の1%）で好中球増加・左方移動を確認。"
        "血液生化学で全身性感染に伴う変化を評価。"
        "胸部X線で肺炎合併を検索。膿瘍のFNA細胞診で変性好中球・"
        "グラム陰性短桿菌を確認。中耳炎/内耳炎合併時は頭部X線/CTで"
        "鼓室の混濁を確認。ストレス・過密飼育・他の呼吸器感染との合併が多い"
    )
}

# ── hamster_streptococcal_infection  Streptococcal Infection ──────────────
ENRICHMENTS["hamster_streptococcal_infection"] = {
    "diagnosis_ja": (
        "頸部リンパ節腫脹（頸部膿瘍）・皮下膿瘍・敗血症症状の臨床評価。"
        "膿汁の細菌培養・感受性試験でStreptococcus属を同定。"
        "FNA細胞診で変性好中球・グラム陽性連鎖球菌を確認。"
        "CBC（採血量≤体重の1%、最大0.5-1 mL）で好中球著増・左方移動を確認。"
        "血液生化学で全身性炎症・臓器障害を評価。"
        "頸部X線/超音波でリンパ節膿瘍の範囲・深部波及を評価。"
        "心内膜炎・腎炎の合併精査（心エコー・尿検査）。"
        "同居個体のスクリーニングと飼育環境の衛生評価が重要"
    )
}

# ── hamster_pseudomonas_infection  Pseudomonas Infection ──────────────────
ENRICHMENTS["hamster_pseudomonas_infection"] = {
    "diagnosis_ja": (
        "創傷感染・中耳炎・肺炎の臨床評価。患部スワブの細菌培養・感受性試験で"
        "Pseudomonas aeruginosaを同定（多剤耐性パターンの確認が重要）。"
        "CBC（採血量≤体重の1%）で好中球増加を確認。血液生化学で全身状態を評価。"
        "緑色膿汁の排出が特徴的臨床所見。"
        "胸部X線で肺炎合併を検索。中耳炎/内耳炎では頭部X線/CTで"
        "鼓室の混濁・骨溶解を確認。飲水ボトルの細菌汚染検査"
        "（Pseudomonasは水系環境に常在）。バイオフィルム形成による難治性感染に注意"
    )
}

# ── hamster_tyzzer's_disease_-_subclinical  Tyzzer's Disease - Subclinical ─
ENRICHMENTS["hamster_tyzzer's_disease_-_subclinical"] = {
    "diagnosis_ja": (
        "臨床症状は乏しく、ストレス負荷時の急性増悪がリスク。"
        "糞便PCRでClostridium piliforme DNAの低レベル検出を試みる。"
        "血清学的検査（ELISA・IFA）で抗C. piliforme抗体を検出。"
        "CBC・血液生化学（採血量≤体重の1%）で軽度の肝酵素上昇を検索。"
        "定期的な糞便検査で菌体排出のモニタリング。"
        "飼育環境ストレス因子（過密・温度変動・輸送）の評価。"
        "確定診断は困難で、剖検時の肝臓Warthin-Starry銀染色が最も信頼性が高い。"
        "同居集団の抗体スクリーニングで浸淫度を把握"
    )
}

# ── hamster_0034  Salmonellosis ───────────────────────────────────────────
ENRICHMENTS["hamster_0034"] = {
    "diagnosis_ja": (
        "急性水様性～粘液性下痢・沈鬱・脱水・急死の臨床評価。"
        "糞便培養（SS寒天・XLD寒天等の選択培地）でSalmonella属を分離・同定。"
        "血液培養（敗血症の場合、採血量≤体重の1%）で菌血症を確認。"
        "PCR検査でSalmonella属特異的遺伝子（invA等）を検出。"
        "CBC で好中球増加（重症時は好中球減少）・脱水に伴うPCV上昇を確認。"
        "血液生化学で電解質異常・BUN上昇・低血糖を評価。"
        "人獣共通感染症のため飼育者への感染リスク説明が必須。"
        "抗菌薬感受性試験で多剤耐性パターンを確認"
    )
}

# ── hamster_0025  Melanoma ────────────────────────────────────────────────
ENRICHMENTS["hamster_0025"] = {
    "diagnosis_ja": (
        "皮膚の色素性腫瘤の視診：サイズ・形状・固着性・色素沈着パターンを記録。"
        "FNA細胞診でメラニン顆粒含有細胞・紡錘形～類上皮細胞の異型性を確認。"
        "切除生検・病理組織検査で有糸分裂指数（>3/10 HPFで高悪性度）・浸潤深度を評価。"
        "Melan-A・S-100免疫染色で無色素性メラノーマを確定。"
        "CBC・血液生化学（採血量≤体重の1%）で全身状態を評価。"
        "胸部X線で肺転移をスクリーニング。所属リンパ節のFNAで転移を検索。"
        "腹部超音波で内臓転移を評価"
    )
}

# ── hamster_0123  Hypothermia ─────────────────────────────────────────────
ENRICHMENTS["hamster_0123"] = {
    "diagnosis_ja": (
        "体温測定（直腸温）で低体温（<36.5℃）を確認。ハムスター特有の冬眠様状態"
        "（torpor/hibernation）との鑑別が重要：環境温度15℃以下・短日照で誘発される"
        "トーパーは徐々に回復するが、病的低体温は基礎疾患を伴う。"
        "呼吸数・心拍数の測定（トーパーでは著明に減少するが規則的）。"
        "血液ガス・電解質検査で代謝性アシドーシスを評価。血糖値測定（低血糖の有無）。"
        "心電図で不整脈（低体温性徐脈・心室細動リスク）を確認。"
        "CBC・血液生化学（採血量≤体重の1%）で基礎疾患を検索。"
        "飼育環境の温度管理状況を聴取（適正20-24℃）"
    )
}

# ── hamster_0002  Hamster Polyomavirus ────────────────────────────────────
ENRICHMENTS["hamster_0002"] = {
    "diagnosis_ja": (
        "皮膚腫瘤（上皮性腫瘍）・リンパ腫・内臓腫瘍の臨床評価。"
        "血液PCRでHamster Polyomavirus（HaPyV）DNAを検出。"
        "腫瘤のFNA細胞診で異型細胞を確認。切除生検・病理組織検査で"
        "腫瘍型を確定しウイルス関連性を評価（免疫組織化学でT抗原検出）。"
        "CBC・血液生化学（採血量≤体重の1%、最大0.5-1 mL）で全身状態を評価。"
        "腹部超音波・X線で内臓腫瘍（肝臓・腎臓・脾臓）を検索。"
        "血清学的検査（HI試験）で抗体価を測定。"
        "若齢シリアンハムスターに好発し、垂直・水平感染の両経路に注意"
    )
}

# ── hamster_0079  Sticky Eye (Neonatal) ───────────────────────────────────
ENRICHMENTS["hamster_0079"] = {
    "diagnosis_ja": (
        "新生仔の眼瞼癒着・眼周囲の分泌物固着の臨床評価。"
        "温湿布で軟化後に眼瞼を愛護的に開放し、角膜・結膜の状態を確認。"
        "眼脂のグラム染色・細菌培養で二次感染菌（Staphylococcus等）を同定。"
        "フルオレセイン染色で角膜潰瘍の有無を確認。"
        "母獣の健康状態・飼育環境の清潔性を評価。"
        "CBC は新生仔では採血量制限（体重の1%以下、数μL）のため困難な場合が多い。"
        "巣材の種類・湿度管理を聴取（過乾燥環境で分泌物が固着しやすい）。"
        "先天性眼瞼閉鎖との鑑別が必要"
    )
}

# ── hamster_0114  Fatty Liver Disease ─────────────────────────────────────
ENRICHMENTS["hamster_0114"] = {
    "diagnosis_ja": (
        "食欲不振・体重変動・沈鬱の臨床評価。血液生化学（採血量≤体重の1%）で"
        "肝酵素上昇（ALT>200 IU/L、AST上昇）・高脂血症（コレステロール・中性脂肪上昇）・"
        "胆汁酸上昇・Alb低下を確認。腹部超音波で肝臓のびまん性高エコー化"
        "（脂肪浸潤パターン）・肝腫大を評価。凝固検査（PT延長）で肝合成能を評価。"
        "超音波ガイド下FNA/肝生検で脂肪変性の程度を確認（病理：肝細胞内脂肪滴）。"
        "食餌歴の聴取：高脂肪食（ヒマワリの種過多）・肥満との関連を確認。"
        "ドワーフハムスターでは糖尿病合併による脂肪肝も考慮"
    )
}

# ── hamster_hepatic_amyloidosis  Hepatic Amyloidosis ──────────────────────
ENRICHMENTS["hamster_hepatic_amyloidosis"] = {
    "diagnosis_ja": (
        "慢性の体重減少・腹部膨満・沈鬱の臨床評価。血液生化学（採血量≤体重の1%）で"
        "肝酵素上昇（ALT・AST）・Alb低下・胆汁酸上昇を確認。"
        "腹部超音波で肝腫大・エコーパターン異常を評価。"
        "肝生検・病理組織検査でコンゴーレッド染色陽性のアミロイド沈着を確認"
        "（偏光顕微鏡で緑色複屈折が特徴的）。CBC で慢性炎症に伴う変化を評価。"
        "尿検査で蛋白尿（腎アミロイドーシス合併）を検索。"
        "高齢シリアンハムスターに好発（AA型アミロイドーシス）。"
        "基礎の慢性炎症性疾患の検索が重要"
    )
}

# ── hamster_tapeworm_rodentolepis_nana  Tapeworm (Rodentolepis nana) ──────
ENRICHMENTS["hamster_tapeworm_rodentolepis_nana"] = {
    "diagnosis_ja": (
        "多くは無症状で糞便検査時の偶発的発見。重度感染では軟便・体重減少を評価。"
        "糞便浮遊法（飽和食塩水法・硫酸亜鉛法）で特徴的な六鉤幼虫を含む虫卵"
        "（直径30-47μm、極糸付き）を検出。糞便直接塗抹で虫卵または片節を確認。"
        "粘着テープ法で肛門周囲の虫卵を検索。"
        "CBC（採血量≤体重の1%）で好酸球増加を評価。"
        "腸管内の成虫は体長20-40mmで肉眼的に確認困難な場合が多い。"
        "人獣共通感染症（特に小児への感染リスク）のため衛生指導が必須"
    )
}

# ── hamster_hamster_polyomavirus_-_clinical_form  HaPyV Clinical ──────────
ENRICHMENTS["hamster_hamster_polyomavirus_-_clinical_form"] = {
    "diagnosis_ja": (
        "多発性皮膚腫瘤（上皮性腫瘍・トリコエピセリオーマ）・リンパ腫の臨床評価。"
        "血液PCRでHamster Polyomavirus（HaPyV）DNAの高ウイルス量を検出。"
        "腫瘤のFNA細胞診・切除生検で組織型を確定。病理組織検査で"
        "免疫組織化学（T抗原）によるウイルス関連腫瘍の証明。"
        "CBC・血液生化学（採血量≤体重の1%）で全身状態・リンパ腫に伴う異常を評価。"
        "腹部超音波・X線で内臓腫瘍（肝・腎・脾）をスクリーニング。"
        "若齢（3-12ヶ月）シリアンハムスターに好発。免疫不全個体での重症化に注意"
    )
}

# ── hamster_hamster_polyomavirus_-_subclinical_carrier  HaPyV Subclinical ─
ENRICHMENTS["hamster_hamster_polyomavirus_-_subclinical_carrier"] = {
    "diagnosis_ja": (
        "臨床症状なく、スクリーニング検査で偶発的に発見。"
        "血液または尿PCRでHamster Polyomavirus（HaPyV）DNAの低レベル検出。"
        "血清学的検査（HI試験・ELISA）で抗HaPyV抗体を検出。"
        "CBC・血液生化学（採血量≤体重の1%）で異常所見なしを確認。"
        "定期的な身体検査で皮膚腫瘤の早期発見をモニタリング。"
        "尿中ウイルス排出による同居個体への水平感染リスクを評価。"
        "ストレス・免疫抑制時に臨床型への移行リスクがあるため経過観察が重要"
    )
}

# ── hamster_amyloidosis_-_renal  Amyloidosis - Renal ──────────────────────
ENRICHMENTS["hamster_amyloidosis_-_renal"] = {
    "diagnosis_ja": (
        "多飲多尿・体重減少・浮腫の臨床評価。血液生化学（採血量≤体重の1%）で"
        "BUN・Cre上昇（腎不全）・Alb低下（蛋白漏出性腎症）・高コレステロール血症を確認。"
        "尿検査で蛋白尿（尿蛋白/クレアチニン比上昇）を検出。"
        "腹部超音波で腎臓のサイズ・エコーパターン異常（高エコー化・腎盂拡張）を評価。"
        "CBC で慢性腎不全に伴う非再生性貧血（PCV低下）を確認。"
        "腎生検・コンゴーレッド染色で糸球体・間質のアミロイド沈着を確認"
        "（偏光顕微鏡で緑色複屈折）。高齢シリアンハムスターに好発するAA型"
    )
}

# ── hamster_amyloidosis_-_hepatic  Amyloidosis - Hepatic ──────────────────
ENRICHMENTS["hamster_amyloidosis_-_hepatic"] = {
    "diagnosis_ja": (
        "体重減少・腹部膨満・沈鬱・食欲不振の臨床評価。血液生化学（採血量≤体重の1%）で"
        "肝酵素上昇（ALT・AST）・Alb低下・胆汁酸上昇・凝固時間延長を確認。"
        "腹部超音波で肝腫大・びまん性エコーパターン変化を評価。"
        "CBC で非再生性貧血・慢性炎症パターンを確認。"
        "肝生検・コンゴーレッド染色で類洞壁・門脈域のアミロイド沈着を確認。"
        "腎機能検査で腎アミロイドーシスの合併を検索（BUN・Cre・尿蛋白）。"
        "慢性炎症性疾患（歯科疾患・皮膚感染等）がAA型アミロイドの産生誘因"
    )
}

# ── hamster_0008  Hamster Diabetes Mellitus ───────────────────────────────
ENRICHMENTS["hamster_0008"] = {
    "diagnosis_ja": (
        "多飲多尿・多食・体重減少の臨床評価（特にチャイニーズハムスター・キャンベルハムスターに好発）。"
        "血液生化学（採血量≤体重の1%、ドワーフ種は最大0.3-0.4 mL）で持続的高血糖"
        "（>250 mg/dL）を確認。尿検査で糖尿・ケトン尿を検出（ディップスティック使用可）。"
        "フルクトサミン測定で過去1-2週間の平均血糖を評価。"
        "血漿インスリン測定で1型（インスリン低値）・2型（正常～高値）を鑑別。"
        "腹部超音波で膵臓の変性を検索。白内障の眼科検査。"
        "遺伝的素因が強いため家系歴の聴取が有用"
    )
}

# ── hamster_0009  Cushing's Disease (Hyperadrenocorticism) ────────────────
ENRICHMENTS["hamster_0009"] = {
    "diagnosis_ja": (
        "多飲多尿・対称性脱毛・皮膚菲薄化・腹部膨満・筋萎縮の臨床評価。"
        "血液生化学（採血量≤体重の1%）で高血糖・高コレステロール・ALP上昇を確認。"
        "尿比重低下・尿糖を評価。副腎超音波で副腎腫大・腫瘤を確認"
        "（シリアンハムスターでは副腎腺腫/腺癌が多い）。"
        "デキサメサゾン抑制試験（小型齧歯類では実施困難な場合あり）で"
        "コルチゾール分泌動態を評価。CBC で好中球増加・リンパ球減少"
        "（ストレスロイコグラム）を確認。Demodex毛包虫の合併検査"
        "（免疫抑制による日和見感染）。皮膚生検で副腎性脱毛パターンを確認"
    )
}

# ── hamster_0028  Lipoma ──────────────────────────────────────────────────
ENRICHMENTS["hamster_0028"] = {
    "diagnosis_ja": (
        "皮下の軟性・可動性・無痛性腫瘤の触診評価。FNA細胞診で成熟脂肪細胞の"
        "集塊を確認（核異型・有糸分裂像がないことで脂肪肉腫を除外）。"
        "腫瘤のサイズ・成長速度・固着性を経時的に記録。"
        "CBC・血液生化学（採血量≤体重の1%）で全身状態を評価。"
        "急速増大・硬性・固着性の場合は浸潤性脂肪腫または脂肪肉腫を考慮し"
        "切除生検・病理組織検査で確定診断。"
        "腹部超音波で腹腔内脂肪腫の有無を検索。"
        "高齢ハムスターに多く、体重管理・食餌歴（高脂肪食）の聴取が参考"
    )
}

# ── hamster_0073  Exophthalmos ────────────────────────────────────────────
ENRICHMENTS["hamster_0073"] = {
    "diagnosis_ja": (
        "眼球突出の程度・左右差・進行速度の臨床評価。スリットランプ検査で角膜・"
        "前房・水晶体を評価。フルオレセイン染色で露出性角膜潰瘍を確認。"
        "眼圧測定で緑内障を除外。シルマー涙液試験で乾燥性角結膜炎を評価。"
        "眼窩超音波で球後膿瘍・腫瘤を検索。頭部X線/CTで眼窩内占拠性病変・"
        "歯根膿瘍の眼窩波及を精査。CBC・血液生化学（採血量≤体重の1%）で"
        "感染・腫瘍を評価。ハムスターでは球後膿瘍（歯科疾患由来）と"
        "頬袋の反転による眼球圧迫が特徴的原因。頬袋の検査を必ず実施"
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
