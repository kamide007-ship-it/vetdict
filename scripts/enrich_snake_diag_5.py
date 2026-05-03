#!/usr/bin/env python3
"""Enrich diagnosis_ja for Snake diseases (batch 5: 15 entries)."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["snake_chronic_dehydration"] = {
    "diagnosis_ja": "皮膚ツルゴール検査（体側の皮膚テント持続>2-3秒で脱水示唆）・粘膜乾燥を評価。ヘビは眼瞼がなく眼鏡鱗（spectacle/brille）で覆われているため、眼鏡鱗の陥凹・皺が脱水の指標。尾腹側静脈（腎門脈系を避けた前半身での採血推奨）からCBC・血液生化学（PCV上昇=血液濃縮、BUN・尿酸上昇、電解質異常）を評価。尿酸塩の沈着（痛風：関節・内臓）を確認。飼育環境の湿度（種に適した40-80%）・水容器の設置・浸水行動の聴取が重要"
}

ENRICHMENTS["snake_uv_light_deficiency"] = {
    "diagnosis_ja": "飼育環境のUVB照射量（μW/cm²）を紫外線計で測定し、種に適した照射が確保されているか評価。X線で骨密度低下・病的骨折・代謝性骨疾患（MBD）の兆候を確認。血液生化学（Ca・P・ALP・Ca/P比）で代謝異常を評価。ヘビは夜行性種ではUVB要求量が低いが、昼行性種では不可欠。採血は尾腹側静脈から実施（腎門脈系があるため尾側1/3からの薬剤投与は避けるが、採血は可能）。食餌中のビタミンD3含有量の評価。不活発・食欲低下・脱皮不全が臨床徴候"
}

ENRICHMENTS["snake_constriction_band_necrosis"] = {
    "diagnosis_ja": "絞扼帯による皮膚・軟部組織の壊死範囲を視診で評価（脱皮不全の残存皮膚が尾部・体幹を絞扼する症例が多い）。壊死部位の遠位側の血流・感覚・運動機能を確認。X線で骨折・脊椎損傷を除外。細菌培養で二次感染菌を同定。ヘビは全身を一度に脱皮（ecdysis）するため、不完全脱皮の残存皮膚が絞扼帯となる。POTZ（至適環境温度帯）管理下で体温を維持しつつ評価。CBC・血液生化学で全身性感染と組織壊死の影響を評価"
}

ENRICHMENTS["snake_chronic_respiratory_disease_complex"] = {
    "diagnosis_ja": "開口呼吸・頭部挙上・口腔内粘液蓄積・呼吸音の視聴診。ヘビは横隔膜がなく肋間筋の収縮で呼吸するため、呼吸器疾患の評価は全身の呼吸運動パターンを観察。口腔・気管スワブの細菌培養・感受性試験（Pseudomonas・Aeromonas等のグラム陰性菌が多い）。気管洗浄液の細胞診でヘテロフィル・マクロファージ増多を確認。PCR検査でニドウイルス・パラミクソウイルスを除外。X線で肺野の浸潤影を確認（ヘビは単肺構造が多い）。POTZ管理が治療効果に直結"
}

ENRICHMENTS["snake_disseminated_granulomatous_disease"] = {
    "diagnosis_ja": "複数臓器（肝・脾・腎・肺）からの生検で非乾酪性/乾酪性肉芽腫を病理組織学的に確認。特殊染色（PAS・GMS・Ziehl-Neelsen・グラム）で真菌・抗酸菌・細菌を検索。尾腹側静脈からCBC（ヘテロフィル/リンパ球比の変化・単球増加）・血液生化学（肝酵素上昇・尿酸上昇）で全身性炎症と臓器障害を評価。腹腔鏡検査で臓器表面の結節性病変を直接観察・生検。X線・超音波で多臓器の結節性病変を確認。POTZ管理下で全身評価を実施"
}

ENRICHMENTS["snake_nephrocalcinosis"] = {
    "diagnosis_ja": "腹部超音波で腎実質内の高エコー構造（石灰化沈着）を確認。X線で腎領域の石灰化を評価（ヘビの腎臓は体腔後方1/3に位置し、右腎が左腎より頭側にある非対称配置）。尾腹側静脈から採血し血液生化学（尿酸・Ca・P・K）で腎機能と電解質異常を評価。ヘビは尿酸排泄型のため、高尿酸血症が腎石灰沈着の主因。尿検査で尿酸結晶を確認。POTZ管理の確認（低温は代謝・排泄機能を低下させ尿酸蓄積を促進）。食餌中のタンパク質含有量と水分摂取を聴取"
}

ENRICHMENTS["snake_hemolytic_anemia"] = {
    "diagnosis_ja": "尾腹側静脈から採血しCBC・PCV測定で貧血を確認（ヘビの正常PCV：20-35%）。末梢血塗抹で赤血球形態（ヘビの赤血球は有核楕円形）・多染性・ハインツ小体を評価。血漿/血清の色調で溶血を確認（ヘモグロビン遊離による赤色/黄色）。血液寄生虫（ヘモグレガリナ・ヘパトゾーン）のギムザ染色鏡検。血液生化学（尿酸・AST・LDH上昇）で組織障害を評価。感染症（IBD・パラミクソウイルス等の免疫介在性溶血）を除外。POTZ管理下での評価必須"
}

ENRICHMENTS["snake_hemoparasites_blood_parasites"] = {
    "diagnosis_ja": "尾腹側静脈からの末梢血塗抹をギムザ/ライト染色で鏡検し、赤血球内（Hepatozoon・Haemogregarina・Haemoproteus等）・白血球内・血漿中の寄生虫を検出。PCR検査で寄生虫種を同定。CBC・PCV（正常20-35%）で貧血の程度を評価。血液生化学で臓器障害（肝：AST上昇、腎：尿酸上昇）を確認。脾臓超音波で脾腫を評価。ダニ・蚊等のベクター寄生虫の検索。POTZ管理下で採血・評価を実施。野生捕獲個体では保菌率が高い"
}

ENRICHMENTS["snake_organ_prolapse_gastric_intestinal"] = {
    "diagnosis_ja": "総排泄腔からの臓器脱出を視診で確認し、脱出臓器の同定（胃・小腸・大腸・卵管のプローブ挿入鑑別）。脱出組織の生存性（色調・浮腫・壊死・乾燥）を評価。ヘビは横隔膜がなく腹腔臓器の固定が緩いため臓器脱が発生しやすい。X線で腹腔内の残存臓器の位置・異物を確認。尾腹側静脈からCBC・血液生化学（尿酸・電解質）で全身状態を評価。原因検索（寄生虫・腸閉塞・産卵異常・テネスムス）を実施。POTZ管理下での処置と脱出組織の湿潤維持が必須"
}

ENRICHMENTS["snake_drowning___near-drowning"] = {
    "diagnosis_ja": "水中からの救出後、開口部からの液体排出・呼吸パターン（ヘビは横隔膜がなく肋間筋で呼吸）の異常を評価。X線で肺野の液体貯留・浸潤影を確認（ヘビは単肺構造が多いため片肺障害でも致死的）。尾腹側静脈からCBC・血液生化学（電解質・乳酸・血糖）で低酸素障害と代謝異常を評価。水槽の水深・水温・逃避可能な陸地の有無を確認。POTZ管理で体温維持しつつ酸素補給。水棲種でも長時間の水没では溺水が発生する。気管洗浄液の培養で吸引性肺炎を評価"
}

ENRICHMENTS["snake_corneal_disease"] = {
    "diagnosis_ja": "ヘビは眼瞼がなく眼鏡鱗（spectacle/brille）で眼球が覆われているため、角膜疾患は眼鏡鱗下空間の異常として評価。眼鏡鱗の混濁・膨隆（subspectacular abscess）・癒着（retained spectacle）を視診。細隙灯検査（利用可能な場合）で眼鏡鱗下液の貯留を確認。眼鏡鱗下穿刺・培養で感染性膿瘍を評価。X線/CTで眼窩周囲の骨構造を確認。CBC・血液生化学で全身性感染を評価。脱皮（ecdysis）歴の確認が重要（眼鏡鱗の不完全脱皮が原因となる）"
}

ENRICHMENTS["snake_proliferative_osteoarthritis"] = {
    "diagnosis_ja": "X線で脊椎・肋骨関節の骨増殖性変化（骨棘形成・関節面不整・骨膜反応）を確認。ヘビの脊椎は200-400個の椎骨から構成され、多数の関節が変性しうる。CT検査で椎骨の詳細評価。患部の触診で腫脹・変形・疼痛反応を確認。尾腹側静脈からCBC・血液生化学（Ca・P・尿酸・ALP）で代謝異常を評価。病理組織検査で腫瘍性骨増殖（骨肉腫）との鑑別。POTZ管理（代謝と治癒に至適温度が不可欠）。体幹の異常な曲がり・運動障害・食欲低下が臨床徴候"
}

ENRICHMENTS["snake_papillomavirus_infection"] = {
    "diagnosis_ja": "皮膚/粘膜の乳頭腫様病変（疣贅状増殖）からの生検で病理組織検査（表皮の乳頭腫症・コイロサイトーシス・角化亢進）を確認。PCR検査で爬虫類パピローマウイルスDNAを検出し確定診断。電子顕微鏡で組織内のウイルス粒子を確認。鱗の変形・増殖性病変の分布パターンを視診で記録。尾腹側静脈からCBC・血液生化学で全身状態を評価。悪性転化（扁平上皮癌）の鑑別に生検が重要。POTZ管理下で免疫機能を最適化。同居個体への伝播リスクを評価"
}

ENRICHMENTS["snake_dermal_mycosis_non-canv_sfd"] = {
    "diagnosis_ja": "皮膚病変（鱗下結節・痂皮・色調変化・壊死）からのスワブ真菌培養（SDA培地、24-30℃）で菌種同定。PCR検査でOphidiomyces ophidiicola以外の真菌（Chrysosporium・Nannizziopsis等）を特異的に検出し、SFD（Snake Fungal Disease）との鑑別。皮膚生検でPAS/GMS染色陽性の菌糸浸潤を確認。眼鏡鱗（spectacle）の病変は視覚障害を引き起こすため注意深く評価。尾腹側静脈からCBC・血液生化学で全身性波及を確認。POTZ管理下での評価必須"
}

ENRICHMENTS["snake_fracture_spine"] = {
    "diagnosis_ja": "X線（lateral・DV）で脊椎骨折の部位・型（圧迫骨折・破裂骨折・脱臼）を確認。ヘビの脊椎は200-400個の椎骨で構成され、骨折部位により予後が大きく異なる（頭側1/3は予後不良）。骨折部位の遠位側の深部痛覚・運動機能を段階的に評価。CT検査で脊髄管の圧迫・断裂を詳細確認。尾腹側静脈からCBC・血液生化学で全身状態を評価。受傷機転（落下・挟み込み・不適切な保定・ケージ衝突）の聴取。POTZ管理下での安定化が必須。MBDの併存をCa・P測定で除外"
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
