#!/usr/bin/env python3
"""Dog diagnosis_ja expansion — 12 entries under 150 chars."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_benign_prostatic_hyperplasia"] = {
    "diagnosis_ja": "腹部超音波で前立腺の対称性腫大と小嚢胞を確認。エコー輝度は均一（不均一なら膿瘍・腫瘍を疑う）。直腸触診で前立腺の対称性腫大・非疼痛性を確認。血尿・排便困難が臨床症状。前立腺液/精液の細胞診で感染・腫瘍を除外。尿培養で感染性前立腺炎を除外。未去勢雄犬の加齢性変化（6歳以上の95%に認められる）。去勢が最も効果的な治療で、去勢後4-8週で著明に縮小。"
}

ENRICHMENTS["dog_esophageal_stricture"] = {
    "diagnosis_ja": "X線造影検査（バリウム嚥下）で食道の限局性狭窄と造影剤の停滞を確認。内視鏡で狭窄部位の直接観察と重症度評価（狭窄径の測定）。生検で悪性腫瘍を除外。透視下で嚥下動態を評価。胸部X線で吸引性肺炎の合併を確認。原因: 全身麻酔後の胃食道逆流（最多）、異物、腐食剤、食道炎。バルーン拡張術が標準治療（複数回施行が必要なこともある）。"
}

ENRICHMENTS["dog_eyelid_mass_meibomian_gland_adenoma"] = {
    "diagnosis_ja": "眼科検査で眼瞼縁の結節性腫瘤を確認。多くは白～黄色の有茎性腫瘤で、マイボーム腺開口部から発生。FNA（細針吸引）で脂腺由来の細胞（脂質空胞を含む大型細胞）を確認。悪性（脂腺癌）との鑑別に病理組織検査。細隙灯検査で角膜への機械的刺激（潰瘍）を評価。フルオレセイン染色で角膜びらんを確認。老齢犬に最も多い眼瞼腫瘍。腫瘤が大きく角膜に接触する場合はV字切除術で根治。"
}

ENRICHMENTS["dog_fragmented_coronoid_process"] = {
    "diagnosis_ja": "CT三次元再構成で内側鉤状突起の骨折・断片化を確認（X線より高感度で確定診断に最も有用）。X線で二次性OA変化（骨棘形成、関節硬化像）を確認するが、直接的な断片描出はX線では困難。関節鏡で断片の直接確認と同時摘出が可能。関節液検査で非感染性炎症（単核球優位）。肘関節形成不全の一型（他にUAP、OCD）。ラブラドール、ゴールデン、ロットワイラーの成長期（5-9ヶ月）に好発。"
}

ENRICHMENTS["dog_gastric_polyps"] = {
    "diagnosis_ja": "内視鏡で胃粘膜の有茎性/広基性ポリープを直接確認し生検が確定診断。組織学的に過形成性/炎症性/腺腫性を鑑別（腺腫性は悪性転化リスクが最も高い）。X線造影検査で充満欠損を確認。超音波で胃壁の限局性肥厚を評価。CBC/生化学は概ね正常。便潜血で慢性出血を評価。過形成性ポリープが最多で予後良好。内視鏡的ポリペクトミーで摘出し、定期的な経過観察を推奨。"
}

ENRICHMENTS["dog_gastroesophageal_reflux_disease_gerd"] = {
    "diagnosis_ja": "内視鏡で食道粘膜のびらん・潰瘍・紅斑を確認。食道下部括約筋の弛緩を評価。食道pHモニタリングで酸逆流エピソードを定量化（犬では実施施設が限定的）。X線造影で食道ヘルニア・逆流を確認。胸部X線で吸引性肺炎を除外。嘔吐・吐出・嚥下困難・流涎・食欲低下の臨床症状。全身麻酔後に悪化することが多い。PPI/H2ブロッカー+消化管運動促進薬（メトクロプラミド等）で内科管理。"
}

ENRICHMENTS["dog_inguinal_hernia"] = {
    "diagnosis_ja": "身体検査で鼠径部の軟性腫脹を確認。還納性/非還納性/嵌頓性を評価（嵌頓時は疼痛・硬結・発赤あり）。腹部超音波で脱出臓器（子宮、腸管、膀胱、網嚢）を同定。嵌頓時の血流評価（カラードプラ）。X線で腸管ガスパターン（イレウス）の有無を確認。CBC/生化学で全身状態を評価。先天性（幼若犬）vs後天性（妊娠末期/肥満犬）を鑑別。嵌頓時は緊急手術適応。鼠径輪の修復を併施。"
}

ENRICHMENTS["dog_oronasal_fistula"] = {
    "diagnosis_ja": "口腔検査で歯周ポケットから鼻腔への交通を確認。歯周プローブで瘻孔を探索（上顎犬歯の口蓋側に好発）。歯科X線で上顎犬歯/切歯部の歯槽骨溶解と口蓋骨の欠損を確認。鼻腔からの食物・液体の逆流、慢性片側性膿性鼻汁、くしゃみが臨床症状。CT三次元再構成で瘻孔のサイズと骨欠損を詳細評価。原因歯の抜歯+粘膜フラップ（single/double layer）による瘻孔閉鎖が標準治療。"
}

ENRICHMENTS["dog_penile_preputial_tumor"] = {
    "diagnosis_ja": "身体検査で包皮/陰茎からの腫瘤、出血、排尿障害を確認。腫瘤の可動性・浸潤を触診。FNA/生検で腫瘍型を確定（TVT、SCC、乳頭腫、線維肉腫が多い）。TVT: 特徴的な円形細胞の細胞診で暫定診断可能、ビンクリスチン化学療法に高反応（完全寛解率>90%）。X線/CTで鼠径リンパ節転移・肺転移を評価。尿道の閉塞・圧排を尿道造影で評価。SCC/線維肉腫は外科切除が第一選択。"
}

ENRICHMENTS["dog_sesamoid_disease"] = {
    "diagnosis_ja": "X線で種子骨の骨折・断片化・変形・石灰化を確認（DPa、oblique viewが有用）。屈曲・伸展ストレスビューで評価。触診で中手骨パッド部の腫脹・疼痛を検出。デジタルX線で微細骨折を検出。CTで複雑な骨折パターンを三次元評価。超音波で周囲軟部組織の炎症を評価。関節液検査で二次性関節炎の有無を確認。歩様解析で荷重異常を定量化。グレイハウンド等の競走犬に好発。"
}

ENRICHMENTS["dog_thelazia_eye_worm"] = {
    "diagnosis_ja": "眼科検査で結膜嚢・涙管内の半透明な線虫（成虫: 7-17 mm）を直接確認（細隙灯下で蠕動する虫体が観察される）。細隙灯検査で角膜潰瘍・結膜充血・流涙を評価。結膜スワブで虫卵を検出。涙液分泌検査（STT）で乾性角結膜炎（KCS）の合併を確認。媒介者はショウジョウバエ（Phortica/Amiota属）。虫体の物理的除去+イベルメクチン/ミルベマイシンの全身投与で治療。欧州で増加傾向。"
}

ENRICHMENTS["dog_tracheal_foreign_body"] = {
    "diagnosis_ja": "X線（頸部/胸部ラテラル）で気管内の異物を確認（不透過性異物はX線で直接描出可能）。透視で呼吸時の異物の動きを評価。気管支鏡で異物の直接確認と位置・性状の評価、同時に内視鏡的摘出を試みる。CT三次元再構成で異物の正確な位置と気管壁損傷を評価。急性の咳・喘鳴・チアノーゼの臨床症状。胸部X線で続発性肺炎・無気肺を確認。緊急気管支鏡的摘出が第一選択。抜去困難な場合は外科的摘出。"
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
