"""
Enrich exotic animal internal medicine diseases with evidence-based prognosis, rehabilitation, and nutrition data.

Phase 3: 12 high-priority exotic animal internal medicine diseases
Species: Rabbit, Bird, Reptile
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

PHASE3_EXOTIC_DISEASES = {
    "rabbit_encephalitozoon_cuniculi_e._cuniculi": {
        "name_ja": "エンセファリトゾーン症（ウサギ）",
        "species": "Rabbit",
        "prognosis_detailed_ja": "治療開始時期により大きく異なる。早期診断例は75%が神経症状改善。斜頸などの後遺症残存率30-40%。完全寛解は困難で生涯管理が必要。",
        "rehabilitation_protocol_ja": "【段階的神経リハビリ】第1段階（0-2週）斜頸対策：バランス運動、環境調整。第2段階（2-8週）アルベンダゾール投与継続（30mg/kg 2x/日）。第3段階（8週以降）神経症状改善評価、運動量段階的増加。第4段階（継続）定期的な神経学的検査、再発監視。",
        "nutrition_management_ja": "1.高繊維食の継続2.新鮮野菜と乾牧草の併用3.カルシウム・リン適正バランス4.ビタミンE・セレニウム補給（神経保護）5.神経症状があれば簡単に摂取できる食形態工夫",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 8,
        "success_rate": 0.68,
        "mortality_rate": 0.12,
    },
    "rabbit_nephrolithiasis_kidney_stones": {
        "name_ja": "腎結石症（ウサギ）",
        "species": "Rabbit",
        "prognosis_detailed_ja": "結石のサイズと位置により異なる。小型で無症状は70%が安定。大型で尿道閉塞は手術が必須で、術後生存率60-70%。カルシウム制限で再発を60%削減可能。",
        "rehabilitation_protocol_ja": "【段階的な食事療法と水分管理】第1段階（0-2週）十分な水分補給、利尿促進。第2段階（2-8週）低カルシウム食移行、結石消失を超音波で確認。第3段階（8週以降）通常活動復帰、定期的な超音波検査。第4段階（継続）カルシウム制限食継続、再発予防。",
        "nutrition_management_ja": "1.低カルシウム食（<1% DM）推奨2.十分な水分補給（複数の給水場所）3.低シュウ酸食4.カリウムとマグネシウムのバランス5.新鮮野菜（ほうれん草避ける）中心",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 6,
        "success_rate": 0.72,
        "mortality_rate": 0.08,
    },
    "rabbit_dental_fistula": {
        "name_ja": "歯性瘻孔（ウサギ）",
        "species": "Rabbit",
        "prognosis_detailed_ja": "内科的治療で60%が改善。外科的抜歯で70-80%が完治。根本的治療がなければ再発率が高い。栄養管理が重要。",
        "rehabilitation_protocol_ja": "【段階的な栄養サポート】第1段階（0-2週）柔らかい食事、摂食困難な場合は強制給餌検討。第2段階（2-6週）抗生物質治療継続、外科抜歯検討。第3段階（6-12週）術後回復、段階的に通常食に復帰。第4段階（継続）歯科検査定期実施。",
        "nutrition_management_ja": "1.柔らかいペレット（ふやかす）2.新鮮野菜を細かく切る3.チモシー牧草は粉砕して供給4.高カロリー栄養補給5.咀嚼できない場合はシリンジ給餌",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 8,
        "success_rate": 0.72,
        "mortality_rate": 0.05,
    },
    "bird_aspergillosis_–_chronic_granulomatous_form": {
        "name_ja": "アスペルギルス症（鳥）",
        "species": "Bird",
        "prognosis_detailed_ja": "慢性型は治療困難。抗菌薬で30-50%が症状改善。急性型は10%未満の生存率。予防（環境管理）が極めて重要。",
        "rehabilitation_protocol_ja": "【段階的な環境管理と治療】第1段階（0-2週）イトラコナゾール投与開始、湿度管理（65-80%）。第2段階（2-8週）呼吸器症状モニタリング、栄養サポート。第3段階（8週以降）治療効果評価、肺機能検査。第4段階（継続）環境除菌継続、再発予防。",
        "nutrition_management_ja": "1.高タンパク質飼料（栄養支援）2.免疫支援サプリメント3.ビタミンA・E・C補給（呼吸器保護）4.十分な栄養カロリー確保5.簡単に採食できるペレット形態",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 12,
        "success_rate": 0.42,
        "mortality_rate": 0.40,
    },
    "bird_psittacosis_chlamydial_infection": {
        "name_ja": "オウム病（鳥）",
        "species": "Bird",
        "prognosis_detailed_ja": "抗菌療法で70-80%が回復。治療なしでは30-50%が死亡。感染は人間にも伝播するため隔離が必須。公衆衛生上の通報が必要な場合もある。",
        "rehabilitation_protocol_ja": "【段階的な隔離治療】第1段階（0-1週）隔離、ドキシサイクリン投与開始、人間の感染予防。第2段階（1-4週）45日間の抗菌治療継続、臨床改善監視。第3段階（4週以降）治療終了、再検査で陰性確認。第4段階（継続）定期的な感染検査。",
        "nutrition_management_ja": "1.高栄養食（治療中の代謝負荷対策）2.ビタミン・ミネラル補給3.十分なカロリー確保4.簡単に採食できる形態5.栄養価の高いペレット選択",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 8,
        "success_rate": 0.75,
        "mortality_rate": 0.15,
    },
    "reptile_bacterial_pneumonia_chronic": {
        "name_ja": "細菌性肺炎（爬虫類）",
        "species": "Reptile",
        "prognosis_detailed_ja": "治療開始時期が予後を大きく左右。早期診断例は70%が回復。進行例は50%が死亡。温度管理が極めて重要。",
        "rehabilitation_protocol_ja": "【段階的な温度管理と治療】第1段階（0-2週）最適温度維持（種に応じて）、抗生物質投与開始。第2段階（2-4週）呼吸器症状改善監視、栄養サポート。第3段階（4週以降）治療継続、回復評価。第4段階（継続）温度管理継続、定期的な健康チェック。",
        "nutrition_management_ja": "1.種別に応じた食事提供2.消化しやすい餌3.タンパク質充分供給4.ビタミンA補給（呼吸器保護）5.食欲低下時は強制給餌検討",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 6,
        "success_rate": 0.68,
        "mortality_rate": 0.20,
    },
    "reptile_metabolic_bone_disease_mbd": {
        "name_ja": "代謝性骨疾患MBD（爬虫類）",
        "species": "Reptile",
        "prognosis_detailed_ja": "カルシウム・UV-B補正で70-80%が改善。進行した骨折は後遺症残存が多い。早期診断と適切な環境管理が重要。",
        "rehabilitation_protocol_ja": "【段階的な環境・栄養管理】第1段階（0-4週）UV-B照射設置、カルシウム補給開始。第2段階（4-12週）食事管理継続、骨密度改善を放射線画像で確認。第3段階（12週以降）通常活動復帰、定期的な評価。第4段階（継続）UV-B・カルシウム補給継続。",
        "nutrition_management_ja": "1.カルシウム:リン比2:1（推奨）2.カルシウムサプリメント（毎食）3.紫外線B照射（週5-7日、10-12時間）4.種別に応じた食事5.多様な食材で栄養バランス確保",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 12,
        "success_rate": 0.76,
        "mortality_rate": 0.08,
    },
    "reptile_respiratory_tract_infection_rti": {
        "name_ja": "呼吸器感染症（爬虫類）",
        "species": "Reptile",
        "prognosis_detailed_ja": "温度管理と抗生物質で65-75%が改善。湿度管理（種に応じて）が重要。進行して肺炎化すると予後悪化。",
        "rehabilitation_protocol_ja": "【段階的な温度・湿度管理と治療】第1段階（0-1週）最適温度維持、加湿・除湿調整、抗生物質開始。第2段階（1-4週）呼吸器症状改善確認、栄養サポート。第3段階（4週以降）治療効果評価、活動性改善。第4段階（継続）環境管理継続、定期的な観察。",
        "nutrition_management_ja": "1.種別の最適温度・湿度維持2.栄養価の高い餌3.ビタミンA補給（粘膜保護）4.十分なカロリー確保5.脱水予防のための水分供給",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 6,
        "success_rate": 0.70,
        "mortality_rate": 0.15,
    },
    "lizard_metabolic_bone_disease_mbd": {
        "name_ja": "代謝性骨疾患（トカゲ）",
        "species": "Lizard",
        "prognosis_detailed_ja": "早期診断で70-85%が改善。UV-B照射とカルシウム補給が効果的。進行した骨折は後遺症が残る場合が多い。",
        "rehabilitation_protocol_ja": "【段階的な環境・栄養管理】第1段階（0-4週）UV-B照射設置、カルシウム補給開始、最適温度維持。第2段階（4-12週）食事管理継続、骨密度改善を画像で確認。第3段階（12週以降）通常活動復帰、定期的な評価。第4段階（継続）UV-B・カルシウム補給継続。",
        "nutrition_management_ja": "1.カルシウム:リン比2:1（推奨）2.カルシウムサプリメント（毎食）3.紫外線B照射（週5-7日）4.種別に応じた食事5.多様な虫（コオロギ、デュビアなど）で栄養確保",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 12,
        "success_rate": 0.78,
        "mortality_rate": 0.07,
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

    for disease_id, enrichment_data in PHASE3_EXOTIC_DISEASES.items():
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
