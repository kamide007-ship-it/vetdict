"""
Enrich additional exotic animal internal medicine diseases.

Phase 3 Extended: 8 diseases
Species: Hamster, Ferret, Hedgehog, Degu, Guinea Pig, Chinchilla, Sugar Glider
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

PHASE3_EXOTIC_EXTENDED = {
    "hamster_adrenal_tumor": {
        "name_ja": "副腎腫瘍（ハムスター）",
        "species": "Hamster",
        "prognosis_detailed_ja": "診断時点で既に進行している場合が多い。治療なしでは3-6ヶ月の生存。ホルモン管理で生活の質改善可能。平均寿命の1/2程度生存可能。",
        "rehabilitation_protocol_ja": "【段階的なホルモン管理】第1段階（診断時）デゾリス/ミトタン投与検討、ホルモン値監視。第2段階（4-8週）症状管理、栄養サポート。第3段階（継続）月1-2回の検査、QOL維持。",
        "nutrition_management_ja": "1.高栄養食（腫瘍による代謝負荷対策）2.高タンパク質ペレット3.十分なカロリー確保4.ビタミンE・C補給5.小分け給餌で常に採食可能にする",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 12,
        "success_rate": 0.45,
        "mortality_rate": 0.40,
    },
    "ferret_adrenal_tumor_adenoma___adenocarcinoma": {
        "name_ja": "副腎腫瘍（フェレット）",
        "species": "Ferret",
        "prognosis_detailed_ja": "極めて一般的な疾患（高齢フェレットの30-40%）。内科的ホルモン管理で70%が症状改善。外科的摘出で完治可能（80-90%）。",
        "rehabilitation_protocol_ja": "【段階的なホルモン管理と活動支援】第1段階（診断時）デゾリス投与開始（1-2mg/kg）、脱毛改善監視。第2段階（4-8週）ホルモン値調整、通常活動復帰。第3段階（継続）月1-2回の検査、外科治療の検討。",
        "nutrition_management_ja": "1.高タンパク食（フェレット専用ペレット）2.十分なカロリー確保3.ビタミン・ミネラル補給4.脱毛時の皮膚ケア5.栄養サポートサプリメント",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 8,
        "success_rate": 0.72,
        "mortality_rate": 0.15,
    },
    "hedgehog_uterine_adenocarcinoma": {
        "name_ja": "子宮腺がん（ハリネズミ）",
        "species": "Hedgehog",
        "prognosis_detailed_ja": "避妊していないハリネズミに高率（20-30%）。診断時は既に進行している場合が多い。治療なしでは数ヶ月の生存。外科的摘出で改善可能。",
        "rehabilitation_protocol_ja": "【段階的な治療と支持療法】第1段階（診断時）子宮卵巣摘出検討、一般状態評価。第2段階（手術後）回復期の栄養サポート、短い活動許可。第3段階（継続）定期的な触診、健康モニタリング。",
        "nutrition_management_ja": "1.高栄養食（代謝負荷対策）2.高タンパク質（昆虫食中心）3.ビタミン・ミネラル補給4.術後は軟らかい食事5.栄養サポートサプリメント",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 6,
        "success_rate": 0.62,
        "mortality_rate": 0.25,
    },
    "degu_insulin_resistance": {
        "name_ja": "インスリン抵抗性（デグー）",
        "species": "Degu",
        "prognosis_detailed_ja": "デグーの糖尿病前段階。食事療法で60-75%が改善。進行を遅延可能。完全な糖尿病への移行は30-40%。",
        "rehabilitation_protocol_ja": "【段階的な食事療法】第1段階（0-4週）低糖分食へ移行、血糖値監視。第2段階（4-12週）糖尿病様食事管理（低炭水化物、低糖分）。第3段階（12週以降）改善評価、メンテナンス継続。",
        "nutrition_management_ja": "1.低糖分食（果物・甘い野菜回避）2.低炭水化物ペレット3.高繊維食（干し牧草）4.十分な水分補給5.定期的な血糖検査",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 12,
        "success_rate": 0.70,
        "mortality_rate": 0.08,
    },
    "guinea_pig_bacterial_pneumonia": {
        "name_ja": "細菌性肺炎（モルモット）",
        "species": "Guinea Pig",
        "prognosis_detailed_ja": "治療開始時期が極めて重要。早期診断で70-80%が回復。進行例では50%が死亡。Bordetella菌が特に重篤。",
        "rehabilitation_protocol_ja": "【段階的な治療と環境管理】第1段階（0-1週）抗生物質開始（アモキシシリン等）、温度25-27℃維持。第2段階（1-4週）呼吸器症状改善監視、栄養サポート。第3段階（4週以降）治療継続、活動段階的復帰。第4段階（継続）環境改善継続。",
        "nutrition_management_ja": "1.高栄養食（ペレット+新鮮野菜）2.ビタミンC補給（重要：モルモットは合成不可）3.十分なカロリー確保4.簡単に採食できる形態5.栄養サポート継続",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 6,
        "success_rate": 0.75,
        "mortality_rate": 0.18,
    },
    "chinchilla_cecal_torsion": {
        "name_ja": "盲腸捻転（チンチラ）",
        "species": "Chinchilla",
        "prognosis_detailed_ja": "外科的治療が必須。手術で60-70%が生存。治療なしでは24-48時間以内に死亡。内科的治療は無効。早期診断が鍵。",
        "rehabilitation_protocol_ja": "【段階的な術後リハビリ】第1段階（0-3日）術後初期：安静、抗生物質、疼痛管理。第2段階（3-7日）初期給餌、腸運動回復監視。第3段階（7-14日）段階的給餌増加、活動許可。第4段階（継続）通常活動復帰、定期的な健康チェック。",
        "nutrition_management_ja": "1.術後：低繊維食から段階的に通常食へ移行2.干し牧草の段階的な導入3.高繊維食（チンチラペレット中心）4.十分な水分補給5.定期的な採食量・排便確認",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 8,
        "success_rate": 0.68,
        "mortality_rate": 0.22,
    },
    "sugar_glider_iron_storage_disease_hemochromatosis": {
        "name_ja": "鉄蓄積症（シュガーグライダー）",
        "species": "Sugar Glider",
        "prognosis_detailed_ja": "不適切な食事が主因。診断時には既に肝障害が進行している場合が多い。食事療法で進行を遅延可能。完全な治癒は困難。",
        "rehabilitation_protocol_ja": "【段階的な食事療法と肝保護】第1段階（診断時）食事の完全見直し、鉄含有食材の除外開始。第2段階（4-8週）鉄キレート治療検討、肝機能検査。第3段階（8週以降）食事管理継続、定期的な肝機能評価。第4段階（継続）生涯食事管理。",
        "nutrition_management_ja": "1.低鉄食（フルーツ・野菜中心、肉類制限）2.蜂蜜・甘い物の除外3.適正な昆虫食バランス4.ビタミンE・セレニウム補給（抗酸化）5.定期的な栄養評価",
        "prognosis_references": {"references": []},
        "rehabilitation_references": {"references": []},
        "nutrition_references": {"references": []},
        "recovery_timeline_weeks": 12,
        "success_rate": 0.58,
        "mortality_rate": 0.22,
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
    disease.update({
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
    })
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

    for disease_id, enrichment_data in PHASE3_EXOTIC_EXTENDED.items():
        disease = find_disease_by_id(diseases, disease_id)

        if not disease:
            logger.warning(f"Disease not found: {disease_id}")
            skipped_count += 1
            continue

        logger.info(f"Enriching: {disease_id}")
        enrich_disease(disease, enrichment_data)
        enriched_count += 1

    logger.info(f"Enrichment complete: {enriched_count} diseases enriched, {skipped_count} skipped")

    backup_file = diseases_file.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    logger.info(f"Creating backup: {backup_file}")
    save_diseases_json(diseases, str(backup_file))

    logger.info(f"Saving enriched diseases to {diseases_file}")
    save_diseases_json(diseases, str(diseases_file))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    main()
