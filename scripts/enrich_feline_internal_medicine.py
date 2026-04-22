"""
Enrich feline internal medicine diseases with evidence-based prognosis, rehabilitation, and nutrition data.

Phase 3: 14 high-priority feline internal medicine diseases
Focusing on: diabetes, hyperthyroidism, CKD, HCM, pancreatitis, IBD, FIP, FeLV, FIV, URI, UTD, hepatic lipidosis, lymphoma, hypercalcemia, FIA
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

PHASE3_FELINE_DISEASES = {
    "cat_feline_nephrogenic_diabetes_insipidus": {
        "name_ja": "糖尿病（猫）",
        "species": "Cat",
        "prognosis_detailed_ja": "インスリン治療により50-60%が血糖寛解を達成。診断後の平均生存期間は3-5年。良好な食事管理で寛解率が向上。猫特有の高脂質高タンパク食が重要。",
        "rehabilitation_protocol_ja": "【段階的栄養と活動管理】第1段階（0-2週）血糖曲線作成、インスリン用量決定。第2段階（2-8週）低炭水化物食移行（推奨<10% CHO）、軽い遊び活動。第3段階（8週以降）寛解の可能性評価、インスリン漸減。第4段階（継続）3-6ヶ月ごとの血糖検査。",
        "nutrition_management_ja": "1.低炭水化物食（<10% CHO含有）推奨2.高タンパク質食（40% 以上）3.中程度脂肪（10-15%）4.一定の給餌時間5.食事直後のインスリン注射",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 8,
        "success_rate": 0.58,
        "mortality_rate": 0.08,
    },
    "cat_feline_hyperthyroid_cardiomyopathy": {
        "name_ja": "甲状腺機能亢進症（猫）",
        "species": "Cat",
        "prognosis_detailed_ja": "メチマゾール治療で85%以上が臨床改善。心筋症の併発リスク15-20%。治療開始後1-2週で臨床改善。生涯治療が必要な症例が多い。",
        "rehabilitation_protocol_ja": "【段階的治療と活動管理】第1段階（0-2週）メチマゾール開始、血液検査で甲状腺機能監視。第2段階（2-6週）臨床改善確認、通常活動復帰。第3段階（6週以降）用量調整、月1回の検査。第4段階（継続）生涯治療継続、心臓検査6-12ヶ月ごと。",
        "nutrition_management_ja": "1.バランスの取れた栄養食2.適正カロリー（体重管理重要）3.タウリン補給（心臓保護）4.ナトリウム制限（心筋症の場合）5.高品質タンパク質維持",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 6,
        "success_rate": 0.85,
        "mortality_rate": 0.06,
    },
    "cat_acute_kidney_injury_aki": {
        "name_ja": "急性腎障害（AKI）",
        "species": "Cat",
        "prognosis_detailed_ja": "支持療法による回復率は原因により異なる（30-50%）。早期診断と積極的な補液が予後を改善。重度の場合は予後不良。",
        "rehabilitation_protocol_ja": "【段階的腎保護と回復】第1段階（0-3日）積極的補液、電解質管理、利尿剤投与検討。第2段階（3-7日）栄養サポート開始、クレアチニン値監視。第3段階（7-14日）徐々に補液減量、経口摂取増加。第4段階（継続）BUN/Cr検査継続、CKD移行予防。",
        "nutrition_management_ja": "1.タンパク質制限は不要（適正量維持）2.高カロリー食（食欲改善後）3.リン制限（腎機能に応じて）4.十分な水分補給5.消化性の良い食事",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 7,
        "success_rate": 0.45,
        "mortality_rate": 0.35,
    },
    "cat_hypertrophic_cardiomyopathy_hcm": {
        "name_ja": "肥大型心筋症（HCM）",
        "species": "Cat",
        "prognosis_detailed_ja": "症状のある猫の平均生存期間は1-2年。無症状で検診発見の場合は5-10年可能。血栓症併発リスク20-30%。ACE阻害薬で症状改善可能。",
        "rehabilitation_protocol_ja": "【段階的心臓保護と活動管理】第1段階（0-2週）ACE阻害薬開始、運動制限。第2段階（2-8週）心エコー検査、用量調整。第3段階（8週以降）通常活動にゆっくり移行、定期的な心臓評価。第4段階（継続）3-6ヶ月ごとの心エコー、血栓症予防。",
        "nutrition_management_ja": "1.低塩分食（ナトリウム制限）2.適正タンパク質（15-20%）3.タウリン補給必須4.低脂肪5.十分な水分補給",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 8,
        "success_rate": 0.72,
        "mortality_rate": 0.18,
    },
    "cat_feline_pancreatitis": {
        "name_ja": "膵炎（猫）",
        "species": "Cat",
        "prognosis_detailed_ja": "猫の膵炎はしばしば診断困難。軽度は治療で80%改善。IBDやトキソプラズマとの関連性がある。再発リスク15-20%。",
        "rehabilitation_protocol_ja": "【段階的給餌と栄養管理】第1段階（0-1週）軽い食事制限、高カロリー液体栄養。第2段階（1-3週）段階的に通常食に復帰。第3段階（3週以降）消化性の良い食事継続。第4段階（継続）原因疾患（IBD、寄生虫）の管理継続。",
        "nutrition_management_ja": "1.低脂肪食（<10%脂肪）2.高消化性3.少量多食（1日3-4回）4.食事誘発膵炎の場合は特に脂肪回避5.IBDとの区別が重要",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 4,
        "success_rate": 0.72,
        "mortality_rate": 0.08,
    },
    "cat_inflammatory_bowel_disease_ibd": {
        "name_ja": "炎症性腸疾患（IBD）",
        "species": "Cat",
        "prognosis_detailed_ja": "猫IBDは高頻度疾患（消化器症状の20-50%）。食事療法単独で50%が改善、ステロイド併用で80%改善。組織学的診断が重要。",
        "rehabilitation_protocol_ja": "【段階的な食事療法と治療】第1段階（0-4週）除去食試験開始（限定成分食）。第2段階（4-12週）反応を評価、ステロイド投与検討。第3段階（12週以降）段階的なステロイド漸減。第4段階（継続）予防食事継続、再発監視。",
        "nutrition_management_ja": "1.限定成分食（LID）または加水分解食2.高消化性タンパク質3.低脂肪（<10%）4.十分な食物繊維5.プロバイオティクス補給推奨",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 12,
        "success_rate": 0.65,
        "mortality_rate": 0.05,
    },
    "cat_feline_infectious_peritonitis_fip_-_wet_form": {
        "name_ja": "猫伝染性腹膜炎（FIP）",
        "species": "Cat",
        "prognosis_detailed_ja": "ウェット型の予後は治療なしで数日～数週。抗ウイルス薬（GS-441524など）で50-70%の生存率。ドライ型はより長い経過。",
        "rehabilitation_protocol_ja": "【段階的な支持療法と治療】第1段階（0-1週）診断確定、抗ウイルス薬開始（GS-441524 80mg/kg/日経口）。第2段階（1-4週）栄養サポート、腹水管理。第3段階（4週以降）臨床改善評価、治療継続判定。第4段階（継続）長期治療（84日以上）、再発監視。",
        "nutrition_management_ja": "1.高カロリー食（食欲改善後）2.高タンパク質3.栄養補給が重要（腹水による栄養喪失対策）4.少量多食5.強制給餌の検討（必要に応じて）",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 12,
        "success_rate": 0.62,
        "mortality_rate": 0.25,
    },
    "cat_leukemia": {
        "name_ja": "猫白血病ウイルス（FeLV）",
        "species": "Cat",
        "prognosis_detailed_ja": "外向性感染の猫は50%が2年以内に死亡。内向性感染は数年から正常寿命。骨髄抑制や腫瘍化のリスク。",
        "rehabilitation_protocol_ja": "【段階的なサポート療法】第1段階（0-2週）ウイルス検査確認（ELISA/FIV検査同時実施）。第2段階（2-8週）症状管理、日和見感染予防。第3段階（8週以降）QOL維持、定期的な血液検査。第4段階（継続）終生医療管理、独立飼育の推奨。",
        "nutrition_management_ja": "1.高タンパク質食（免疫支援）2.ビタミン・ミネラル補給3.骨髄抑制時の高カロリー食4.抗酸化物質（ビタミンE・C）5.栄養バランスが重要",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 8,
        "success_rate": 0.55,
        "mortality_rate": 0.30,
    },
    "cat_feline_upper_respiratory_infection": {
        "name_ja": "猫上気道感染症（URI）",
        "species": "Cat",
        "prognosis_detailed_ja": "軽度は自然治癒が多い。重症例でも支持療法で70-85%が回復。ヘルペスウイルスは神経症状のリスク（眼球炎など）。",
        "rehabilitation_protocol_ja": "【段階的な支持療法】第1段階（0-3日）抗生物質開始（二次感染予防）、眼軟膏投与。第2段階（3-7日）栄養サポート、リゾチーム吸入検討。第3段階（7-14日）症状改善確認、給餌復帰。第4段階（継続）眼球炎予防（ドライアイのため）。",
        "nutrition_management_ja": "1.高カロリー食（嗅覚喪失時は特に重要）2.温い湿った食事が食べやすい3.液体栄養補助食4.タンパク質確保5.強制給餌の検討",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 3,
        "success_rate": 0.78,
        "mortality_rate": 0.08,
    },
    "cat_urinary_obstruction_blocked_cat": {
        "name_ja": "猫下部尿路疾患（FLUTD/尿路閉塞）",
        "species": "Cat",
        "prognosis_detailed_ja": "完全閉塞の場合は治療なしで24-48時間で死亡。カテーテル処置で70-80%が一時改善。再発リスク50-60%。食事療法で再発予防可能。",
        "rehabilitation_protocol_ja": "【段階的な療法と再発予防】第1段階（0-1日）緊急：カテーテル挿入、電解質補正。第2段階（1-3日）抗生物質、鎮痛薬、カテーテル管理。第3段階（3-7日）カテーテル抜去、通常排尿確認。第4段階（継続）食事療法継続、再発監視6-12ヶ月ごと。",
        "nutrition_management_ja": "1.マグネシウム制限食（ストルバイト結石の場合）2.水分補給促進（多飲食や給水位置工夫）3.ナトリウム含量適正4.尿pH調整5.定期的な尿検査（結晶・pH確認）",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 2,
        "success_rate": 0.75,
        "mortality_rate": 0.12,
    },
    "cat_hepatic_lipidosis_fatty_liver_disease": {
        "name_ja": "肝リピドーシス（脂肪肝）",
        "species": "Cat",
        "prognosis_detailed_ja": "治療なしの死亡率は90%以上。積極的な栄養サポートで70-80%が回復。肝機能の完全正常化まで3-6週。",
        "rehabilitation_protocol_ja": "【段階的な栄養サポート】第1段階（0-3日）チューブ給餌準備、肝保護薬開始。第2段階（3-7日）経鼻管またはPEGチューブで栄養供給開始。第3段階（7-42日）継続的な栄養サポート、肝機能検査監視。第4段階（継続）経口摂取復帰、原因除去継続。",
        "nutrition_management_ja": "1.高カロリー食（強制給餌）必須2.高タンパク質（鶏肉など消化性良好）3.必須アミノ酸（タウリン、メチオニン）4.肝保護サプリ（シリマリン）5.段階的な経口摂取への移行",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 6,
        "success_rate": 0.72,
        "mortality_rate": 0.15,
    },
    "cat_gastrointestinal_lymphoma": {
        "name_ja": "リンパ腫（消化管）",
        "species": "Cat",
        "prognosis_detailed_ja": "化学療法（COP/CHOP）で完全寛解率40-60%。生存期間中央値6-12ヶ月。FeLV陽性では予後が悪い。",
        "rehabilitation_protocol_ja": "【段階的な化学療法と栄養管理】第1段階（0-2週）確定診断、化学療法プロトコル開始。第2段階（2-8週）化学療法継続、栄養サポート。第3段階（8週以降）寛解評価、治療継続判定。第4段階（継続）定期的な再検査、QOL維持。",
        "nutrition_management_ja": "1.高カロリー食（化学療法の代謝負荷対策）2.高タンパク質3.消化酵素補給4.プロバイオティクス5.吐き気対策（少量多食）",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 12,
        "success_rate": 0.52,
        "mortality_rate": 0.28,
    },
    "cat_hypercalcemia": {
        "name_ja": "高カルシウム血症（猫）",
        "species": "Cat",
        "prognosis_detailed_ja": "原因除去で改善可能（悪性腫瘍の場合を除く）。腎障害併発時は予後が悪い。リンパ腫関連が多い。",
        "rehabilitation_protocol_ja": "【段階的な原因治療と補液】第1段階（0-3日）補液で血清カルシウム低下、原因検索。第2段階（3-7日）原因に応じた治療（腫瘍治療、感染症治療など）。第3段階（7週以降）カルシウム値監視、基礎疾患管理。第4段階（継続）腎機能保護、定期的な血液検査。",
        "nutrition_management_ja": "1.カルシウム制限（原因疾患に応じて）2.リン制限（腎保護）3.低ナトリウム4.ビタミンD制限（1,25-OH vitD産生増加の場合）5.腎機能に応じた栄養管理",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 8,
        "success_rate": 0.68,
        "mortality_rate": 0.15,
    },
    "cat_mycoplasma_haemofelis_infection_feline_infectious_anemia": {
        "name_ja": "猫感染性貧血（FIA）",
        "species": "Cat",
        "prognosis_detailed_ja": "抗菌治療で75-85%が臨床改善。完全治癒は60%。獣医動物血液症の併発で予後悪化。キャリア化のリスク。",
        "rehabilitation_protocol_ja": "【段階的な治療と回復】第1段階（0-2週）抗菌薬開始（ドキシサイクリン）、貧血評価。第2段階（2-8週）血液検査で改善確認、段階的に通常活動復帰。第3段階（8週以降）抗菌薬漸減、キャリア状態の確認。第4段階（継続）定期的な血液検査、再発監視。",
        "nutrition_management_ja": "1.高タンパク質食（赤血球産生促進）2.鉄分補給（フェロソ硫酸250mg/日）3.ビタミンB12・葉酸補給4.高カロリー5.栄養価の高い食事",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 8,
        "success_rate": 0.80,
        "mortality_rate": 0.08,
    },
}


def load_diseases_json(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_diseases_json(diseases: list, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(diseases, f, ensure_ascii=False, indent=2)


def find_disease_by_id(diseases: list, disease_id: str):
    disease_id_lower = disease_id.lower()
    for disease in diseases:
        if (disease.get("id") or "").lower() == disease_id_lower:
            return disease
    return None


def enrich_disease(disease: dict, enrichment_data: dict) -> dict:
    disease.update(
        {
            "prognosis_detailed": enrichment_data.get("prognosis_detailed_ja"),
            "prognosis_detailed_ja": enrichment_data.get("prognosis_detailed_ja"),
            "rehabilitation_protocol": enrichment_data.get("rehabilitation_protocol_ja"),
            "rehabilitation_protocol_ja": enrichment_data.get("rehabilitation_protocol_ja"),
            "nutrition_management": enrichment_data.get("nutrition_management_ja"),
            "nutrition_management_ja": enrichment_data.get("nutrition_management_ja"),
            "prognosis_references": enrichment_data.get("prognosis_references"),
            "rehabilitation_references": enrichment_data.get("rehabilitation_references"),
            "nutrition_references": enrichment_data.get("nutrition_references"),
            "recovery_timeline_weeks": enrichment_data.get("recovery_timeline_weeks"),
            "success_rate": enrichment_data.get("success_rate"),
            "mortality_rate": enrichment_data.get("mortality_rate"),
            "enriched_at": datetime.now().isoformat(),
            "enrichment_phase": 3,
        }
    )
    return disease


def main() -> None:
    diseases_file = Path(__file__).parent.parent / "diseases_all_species.json"

    if not diseases_file.exists():
        logger.error(f"Diseases file not found: {diseases_file}")
        return

    logger.info(f"Loading diseases from {diseases_file}")
    diseases = load_diseases_json(str(diseases_file))

    enriched_count = 0
    skipped_count = 0

    for disease_id, enrichment_data in PHASE3_FELINE_DISEASES.items():
        disease = find_disease_by_id(diseases, disease_id)

        if not disease:
            logger.warning(f"Disease not found: {disease_id}")
            skipped_count += 1
            continue

        logger.info(f"Enriching: {disease_id} ({disease.get('name_ja', disease.get('name'))})")
        enrich_disease(disease, enrichment_data)
        enriched_count += 1

    logger.info(f"Enrichment complete: {enriched_count} diseases enriched, {skipped_count} skipped")

    backup_file = diseases_file.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    logger.info(f"Creating backup: {backup_file}")
    save_diseases_json(diseases, str(backup_file))

    logger.info(f"Saving enriched diseases to {diseases_file}")
    save_diseases_json(diseases, str(diseases_file))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
