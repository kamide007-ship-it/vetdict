"""clinical_reasoning.py - 構造化された臨床意思決定支援エンジン

Vetlexiconスタイルの臨床推論を生成する：
- 各鑑別疾患について支持/否定証拠を構造化
- 次の診断ステップ（未実施推奨検査）を提示
- レッドフラグ症状の警告
- "Bottom Line" サマリ

設計原則:
- 入力された症状と疾患の症状リストを照合
- 該当疾患の典型症状で「未報告」のものをミッシングとして提示
- urgency=emergency疾患は強調
- 鑑別を絞り込む追加質問を提案
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# レッドフラグ症状 - これらが入力された場合は緊急疾患を優先
RED_FLAG_SYMPTOMS = {
    "respiratory_distress",
    "severe_dyspnea",
    "cyanosis",
    "collapse",
    "seizure",
    "seizures",
    "status_epilepticus",
    "unconsciousness",
    "coma",
    "uncontrolled_bleeding",
    "hemorrhage",
    "shock",
    "abdominal_distension_acute",
    "bloat",
    "gdv",
    "sudden_blindness",
    "anuria",
    "obstruction",
    "urinary_obstruction",
    "trauma",
    "hyperthermia_severe",
    "hypothermia_severe",
    "anaphylaxis",
}


@dataclass
class DiseaseReasoning:
    """単一鑑別疾患に関する構造化された推論"""

    disease_id: str
    disease_name: str
    disease_name_ja: str
    confidence: float
    urgency: str
    matching_symptoms: list[dict[str, Any]] = field(default_factory=list)  # 入力で支持する症状
    missing_typical_symptoms: list[dict[str, Any]] = field(default_factory=list)  # 該疾患の典型症状で未確認
    next_diagnostic_steps: list[dict[str, Any]] = field(default_factory=list)  # 推奨検査
    red_flags: list[str] = field(default_factory=list)  # 当該疾患でのレッドフラグ
    rule_out_questions: list[str] = field(default_factory=list)  # 鑑別絞り込み質問


@dataclass
class ClinicalReasoningResult:
    """全体の臨床推論結果"""

    bottom_line: dict[str, str]  # {ja, en}
    bottom_line_evidence: str = "C"  # エビデンスグレード
    differentials: list[DiseaseReasoning] = field(default_factory=list)
    next_steps: list[dict[str, str]] = field(default_factory=list)  # 全体的な次のステップ
    emergency_alert: bool = False
    needs_more_info: bool = False
    confidence_warning: str = ""


# Common diagnostic test IDs → JA/EN labels. Used only as a fallback when the
# caller doesn't supply a richer name_map. Keep the list short and obvious.
_DEFAULT_TEST_NAMES: dict[str, dict[str, str]] = {
    "cbc": {"ja": "血球計算（CBC）", "en": "CBC"},
    "complete_blood_count": {"ja": "血球計算（CBC）", "en": "Complete Blood Count (CBC)"},
    "biochemistry": {"ja": "血液生化学", "en": "Biochemistry"},
    "biochem": {"ja": "血液生化学", "en": "Biochemistry"},
    "biochemistry_panel": {"ja": "血液生化学検査", "en": "Biochemistry Panel"},
    "chemistry_panel": {"ja": "血液生化学検査", "en": "Chemistry Panel"},
    "serum_chemistry": {"ja": "血清生化学検査", "en": "Serum Chemistry"},
    "blood_work": {"ja": "血液検査", "en": "Blood Work"},
    "blood_panel": {"ja": "血液検査", "en": "Blood Panel"},
    "blood_smear": {"ja": "血液塗抹", "en": "Blood Smear"},
    "blood_glucose": {"ja": "血糖測定", "en": "Blood Glucose"},
    "ammonia_level": {"ja": "アンモニア測定", "en": "Ammonia Level"},
    "bile_acids": {"ja": "胆汁酸検査", "en": "Bile Acids"},
    "bile_acids_test": {"ja": "胆汁酸検査", "en": "Bile Acids Test"},
    "blood_culture": {"ja": "血液培養", "en": "Blood Culture"},
    "blood_typing": {"ja": "血液型判定", "en": "Blood Typing"},
    "blood_gas_analysis": {"ja": "血液ガス分析", "en": "Blood Gas Analysis"},
    "arterial_blood_gas": {"ja": "動脈血液ガス分析", "en": "Arterial Blood Gas"},
    "crp": {"ja": "CRP測定", "en": "C-reactive Protein"},
    "urinalysis": {"ja": "尿検査", "en": "Urinalysis"},
    "xray": {"ja": "レントゲン検査", "en": "X-ray"},
    "x_ray": {"ja": "レントゲン検査", "en": "X-ray"},
    "radiograph": {"ja": "レントゲン検査", "en": "Radiograph"},
    "radiography": {"ja": "レントゲン検査", "en": "Radiography"},
    "ultrasound": {"ja": "超音波検査", "en": "Ultrasound"},
    "abdominal_ultrasound": {"ja": "腹部超音波", "en": "Abdominal ultrasound"},
    "echocardiography": {"ja": "心エコー", "en": "Echocardiography"},
    "ecg": {"ja": "心電図", "en": "ECG"},
    "ekg": {"ja": "心電図", "en": "ECG"},
    "ct": {"ja": "CT検査", "en": "CT"},
    "mri": {"ja": "MRI検査", "en": "MRI"},
    "endoscopy": {"ja": "内視鏡", "en": "Endoscopy"},
    "biopsy": {"ja": "生検", "en": "Biopsy"},
    "skin_biopsy": {"ja": "皮膚生検", "en": "Skin Biopsy"},
    "histopathology": {"ja": "病理組織検査", "en": "Histopathology"},
    "cytology": {"ja": "細胞診", "en": "Cytology"},
    "fine_needle_aspirate": {"ja": "細針吸引細胞診（FNA）", "en": "Fine Needle Aspirate (FNA)"},
    "bone_marrow_aspirate": {"ja": "骨髄穿刺", "en": "Bone Marrow Aspirate"},
    "bone_marrow_biopsy": {"ja": "骨髄生検", "en": "Bone Marrow Biopsy"},
    "fecal_exam": {"ja": "糞便検査", "en": "Fecal exam"},
    "fecal": {"ja": "糞便検査", "en": "Fecal exam"},
    "fecal_examination": {"ja": "糞便検査", "en": "Fecal Examination"},
    "fecal_culture": {"ja": "糞便培養", "en": "Fecal Culture"},
    "fecal_smear": {"ja": "糞便塗抹", "en": "Fecal Smear"},
    "bacterial_culture": {"ja": "細菌培養", "en": "Bacterial Culture"},
    "serology": {"ja": "血清抗体検査", "en": "Serology"},
    "culture_sensitivity": {"ja": "培養・感受性試験", "en": "Culture & Sensitivity"},
    "sensitivity_testing": {"ja": "感受性試験", "en": "Sensitivity Testing"},
    "behavioral_assessment": {"ja": "行動評価", "en": "Behavioral Assessment"},
    "neurological_exam": {"ja": "神経学的検査", "en": "Neurological Exam"},
    "hormone_panel": {"ja": "ホルモン検査", "en": "Hormone Panel"},
    "abdominal_radiograph": {"ja": "腹部レントゲン", "en": "Abdominal Radiograph"},
    "thoracic_radiograph": {"ja": "胸部レントゲン", "en": "Thoracic Radiograph"},
    "chest_xray": {"ja": "胸部レントゲン", "en": "Chest X-ray"},
    "skull_radiographs": {"ja": "頭部レントゲン", "en": "Skull Radiographs"},
    "ct_scan": {"ja": "CT検査", "en": "CT Scan"},
    "bronchoscopy": {"ja": "気管支鏡", "en": "Bronchoscopy"},
    "rhinoscopy": {"ja": "鼻鏡検査", "en": "Rhinoscopy"},
    "gastroscopy": {"ja": "胃内視鏡", "en": "Gastroscopy"},
    "colonoscopy": {"ja": "大腸内視鏡", "en": "Colonoscopy"},
    "thoracocentesis": {"ja": "胸腔穿刺", "en": "Thoracocentesis"},
    "abdominocentesis": {"ja": "腹腔穿刺", "en": "Abdominocentesis"},
    "csf_analysis": {"ja": "脳脊髄液検査", "en": "CSF Analysis"},
    "synovial_fluid_analysis": {"ja": "関節液検査", "en": "Synovial Fluid Analysis"},
    "snap_test": {"ja": "SNAPテスト", "en": "SNAP Test"},
    "barium_study": {"ja": "バリウム造影検査", "en": "Barium Study"},
    "barium_swallow": {"ja": "バリウム嚥下造影", "en": "Barium Swallow"},
    "contrast_radiography": {"ja": "造影レントゲン検査", "en": "Contrast Radiography"},
    "fluoroscopy": {"ja": "X線透視検査", "en": "Fluoroscopy"},
    "tracheal_wash_culture": {"ja": "気管洗浄液培養", "en": "Tracheal Wash Culture"},
    "bronchoalveolar_lavage": {"ja": "気管支肺胞洗浄（BAL）", "en": "Bronchoalveolar Lavage (BAL)"},
    "schirmer_tear_test": {"ja": "シルマー涙液試験", "en": "Schirmer Tear Test"},
    "fundic_examination": {"ja": "眼底検査", "en": "Fundic Examination"},
    "fructosamine": {"ja": "フルクトサミン", "en": "Fructosamine"},
    "cortisol_level": {"ja": "コルチゾール測定", "en": "Cortisol Level"},
    "insulin_level": {"ja": "インスリン測定", "en": "Insulin Level"},
    "rt_pcr": {"ja": "RT-PCR検査", "en": "RT-PCR"},
    "pcr_testing": {"ja": "PCR検査", "en": "PCR Testing"},
    "gram_stain": {"ja": "グラム染色", "en": "Gram Stain"},
    "acid_fast_stain": {"ja": "抗酸菌染色", "en": "Acid-fast Stain"},
    "urine_specific_gravity": {"ja": "尿比重測定", "en": "Urine Specific Gravity"},
    "urine_protein_creatinine_ratio": {"ja": "尿蛋白/クレアチニン比（UPC）", "en": "Urine Protein/Creatinine Ratio (UPC)"},
    "upc_ratio": {"ja": "尿蛋白/クレアチニン比（UPC）", "en": "UPC Ratio"},
    "blood_pressure_measurement": {"ja": "血圧測定", "en": "Blood Pressure Measurement"},
    "tracheal_wash_cytology": {"ja": "気管洗浄細胞診", "en": "Tracheal Wash Cytology"},
    "oral_exam": {"ja": "口腔検査", "en": "Oral Exam"},
    "otoscopic_exam": {"ja": "耳鏡検査", "en": "Otoscopic Exam"},
    "pcr": {"ja": "PCR検査", "en": "PCR"},
    "elisa": {"ja": "ELISA検査", "en": "ELISA"},
    "culture": {"ja": "培養検査", "en": "Culture"},
    "acth_stimulation": {"ja": "ACTH刺激試験", "en": "ACTH stimulation"},
    "ldds": {"ja": "低用量デキサメサゾン抑制試験", "en": "LDDS"},
    "tracheal_wash": {"ja": "気管洗浄", "en": "Tracheal wash"},
    "bal": {"ja": "気管支肺胞洗浄", "en": "BAL"},
    "blood_pressure": {"ja": "血圧測定", "en": "Blood pressure"},
    "fna": {"ja": "細針吸引（FNA）", "en": "FNA"},
    "blood_chemistry": {"ja": "血液生化学", "en": "Blood chemistry"},
    "liver_enzymes": {"ja": "肝酵素検査", "en": "Liver enzymes"},
    "liver_biopsy": {"ja": "肝生検", "en": "Liver biopsy"},
    "kidney_panel": {"ja": "腎機能検査", "en": "Kidney panel"},
    "coagulation_panel": {"ja": "凝固機能検査", "en": "Coagulation panel"},
    "thoracic_radiography": {"ja": "胸部レントゲン", "en": "Thoracic radiograph"},
    "abdominal_radiography": {"ja": "腹部レントゲン", "en": "Abdominal radiograph"},
    "thoracic_xray": {"ja": "胸部レントゲン", "en": "Thoracic X-ray"},
    "abdominal_xray": {"ja": "腹部レントゲン", "en": "Abdominal X-ray"},
    "lactate": {"ja": "血中乳酸", "en": "Lactate"},
    "blood_gas": {"ja": "血液ガス", "en": "Blood gas"},
    "spec_cpl": {"ja": "Spec cPL（膵特異リパーゼ）", "en": "Spec cPL"},
    "spec_fpl": {"ja": "Spec fPL（猫膵特異リパーゼ）", "en": "Spec fPL"},
    "feline_pancreatic_lipase": {"ja": "猫膵特異リパーゼ", "en": "Feline pancreatic lipase"},
    "tli": {"ja": "TLI（トリプシン様免疫反応）", "en": "TLI"},
    "fecal_flotation": {"ja": "糞便浮遊検査", "en": "Fecal flotation"},
    "skin_scraping": {"ja": "皮膚掻爬検査", "en": "Skin scraping"},
    "wood_lamp": {"ja": "ウッド灯検査", "en": "Wood's lamp"},
    "fungal_culture": {"ja": "真菌培養", "en": "Fungal culture"},
    "free_t4": {"ja": "遊離T4", "en": "Free T4"},
    "tsh": {"ja": "TSH（甲状腺刺激ホルモン）", "en": "TSH"},
    "fiv_felv_test": {"ja": "FIV/FeLV検査", "en": "FIV/FeLV test"},
    "uti_culture": {"ja": "尿培養", "en": "Urine culture"},
    "urine_culture": {"ja": "尿培養", "en": "Urine culture"},
    "ophthalmic_exam": {"ja": "眼科検査", "en": "Ophthalmic exam"},
    "fluorescein_stain": {"ja": "フルオレセイン染色", "en": "Fluorescein stain"},
    "schirmer_test": {"ja": "シルマー試験", "en": "Schirmer test"},
    "tonometry": {"ja": "眼圧測定", "en": "Tonometry"},
    "dental_radiograph": {"ja": "歯科レントゲン", "en": "Dental radiograph"},
    "dental_exam": {"ja": "歯科検査", "en": "Dental exam"},
    "neurologic_exam": {"ja": "神経学的検査", "en": "Neurologic exam"},
    "orthopedic_exam": {"ja": "整形外科検査", "en": "Orthopedic exam"},
    "physical_exam": {"ja": "身体検査", "en": "Physical exam"},
}


def _humanize_id(
    sid: str,
    name_map: dict[str, dict[str, str]] | None = None,
) -> dict[str, str]:
    """症状/検査IDを人間可読化。

    name_map（{id: {ja, en}}）が与えられた場合、そこから優先的に翻訳する。
    なければ _DEFAULT_TEST_NAMES、最後に ID から派生した英語表現にフォールバック。
    Japanese fallback は ID をそのまま返さず、英語と同じ表記にする。
    """
    if not sid:
        return {"id": "", "name_ja": "", "name_en": ""}
    if name_map and sid in name_map:
        entry = name_map[sid]
        ja = entry.get("ja") or entry.get("name_ja")
        en = entry.get("en") or entry.get("name_en")
        if ja or en:
            fallback_en = sid.replace("_", " ").strip().capitalize()
            return {
                "id": sid,
                "name_ja": ja or en or fallback_en,
                "name_en": en or fallback_en,
            }
    if sid in _DEFAULT_TEST_NAMES:
        entry = _DEFAULT_TEST_NAMES[sid]
        return {"id": sid, "name_ja": entry["ja"], "name_en": entry["en"]}
    en = sid.replace("_", " ").strip().capitalize()
    return {"id": sid, "name_ja": en, "name_en": en}


def _detect_red_flags_in_input(input_symptom_ids: list[str]) -> list[str]:
    """入力症状にレッドフラグが含まれているか"""
    return [s for s in input_symptom_ids if s in RED_FLAG_SYMPTOMS]


def _generate_bottom_line(
    differentials: list[DiseaseReasoning],
    has_emergency: bool,
    n_input_symptoms: int,
    lang: str = "ja",
) -> tuple[dict[str, str], str]:
    """臨床推論のサマリを生成し、エビデンスグレードを返す"""
    if not differentials:
        return (
            {
                "ja": "現時点では鑑別を絞り込むには情報が不足しています。さらに症状や経過を追加してください。",
                "en": "Insufficient information to narrow differentials. Add more symptoms or history.",
            },
            "D",
        )

    top = differentials[0]
    if has_emergency:
        return (
            {
                "ja": f"⚠ 緊急対応を要する可能性があります（{top.disease_name_ja}: 信頼度{top.confidence:.0%}）。安定化処置と並行した精査を推奨します。",
                "en": f"⚠ Emergency presentation possible ({top.disease_name}: {top.confidence:.0%} confidence). Stabilize while pursuing diagnostics.",
            },
            "B" if top.confidence > 0.7 else "C",
        )

    if top.confidence > 0.85 and n_input_symptoms >= 3:
        return (
            {
                "ja": f"最も可能性が高いのは {top.disease_name_ja}（信頼度{top.confidence:.0%}）です。次の診断ステップで確定診断に向けて進めてください。",
                "en": f"Most likely: {top.disease_name} ({top.confidence:.0%}). Proceed with next diagnostic steps to confirm.",
            },
            "B",
        )

    if top.confidence > 0.6:
        return (
            {
                "ja": f"上位鑑別: {top.disease_name_ja}（{top.confidence:.0%}）。確定にはさらなる検査・追加の症状情報が有用です。",
                "en": f"Top differential: {top.disease_name} ({top.confidence:.0%}). Further diagnostics or symptom history would help confirm.",
            },
            "C",
        )

    return (
        {
            "ja": f"複数の鑑別が拮抗しています（上位: {top.disease_name_ja} {top.confidence:.0%}）。症状の追加・経過観察・追加検査が必要です。",
            "en": f"Multiple competing differentials (top: {top.disease_name} {top.confidence:.0%}). More symptoms, observation, or diagnostics needed.",
        },
        "D",
    )


def build_reasoning(
    input_symptoms: list[str],
    differentials: list[dict[str, Any]],
    diseases_data: dict[str, dict[str, Any]] | None = None,
    species: str = "",
    lang: str = "ja",
    max_differentials: int = 5,
    name_map: dict[str, dict[str, str]] | None = None,
) -> ClinicalReasoningResult:
    """
    鑑別診断結果から構造化された臨床推論を構築する。

    Args:
        input_symptoms: ユーザーが入力した症状ID
        differentials: 鑑別疾患（{name, name_ja, confidence, urgency, symptoms, recommended_tests, ...}）
        diseases_data: 疾患データ全体（typical_symptoms 検索用、任意）
        species: 動物種
        lang: 言語
        max_differentials: 推論を生成する最大鑑別数
    """
    input_set = set(input_symptoms)
    red_flags_in_input = _detect_red_flags_in_input(input_symptoms)
    has_emergency = False

    reasonings: list[DiseaseReasoning] = []
    for d in differentials[:max_differentials]:
        # Pre-computed structures from diagnostic_chat (preferred)
        pre_matched = d.get("matched_symptoms") or []
        pre_missing = d.get("missing_key_symptoms") or []
        pre_additional = d.get("additional_disease_symptoms") or []

        def _ids(items):
            out = []
            for x in items:
                if isinstance(x, str):
                    out.append(x)
                elif isinstance(x, dict):
                    sid = x.get("id") or x.get("symptom_id") or x.get("name")
                    if sid:
                        out.append(sid)
            return out

        if pre_matched or pre_missing:
            # Use the chat engine's pre-computed analysis
            matching_ids = _ids(pre_matched)
            missing_ids = _ids(pre_missing)[:3]
            disease_symptom_set = set(matching_ids) | set(missing_ids) | set(_ids(pre_additional))
        else:
            # Fallback: use disease.symptoms
            disease_symptoms = d.get("symptoms") or []
            if isinstance(disease_symptoms, dict):
                disease_symptom_ids = list(disease_symptoms.keys())
            elif isinstance(disease_symptoms, list):
                disease_symptom_ids = _ids(disease_symptoms)
            else:
                disease_symptom_ids = []
            disease_symptom_set = {s for s in disease_symptom_ids if s}
            matching_ids = sorted(input_set & disease_symptom_set)
            missing_ids = sorted(disease_symptom_set - input_set)[:3]

        # 推奨検査
        rec_tests = d.get("recommended_tests") or d.get("recommended_tests_display") or []
        if isinstance(rec_tests, str):
            rec_tests = [rec_tests]
        rec_test_ids = _ids(rec_tests) if rec_tests else []

        urgency = (d.get("urgency") or "").lower()
        if urgency == "emergency":
            has_emergency = True

        # 信頼度: confidence (0-1) または confidence_percent (0-100) を統一
        conf_raw = d.get("confidence", d.get("confidence_percent", 0))
        try:
            conf_val = float(conf_raw)
            if conf_val > 1.0:
                conf_val /= 100.0
        except (TypeError, ValueError):
            conf_val = 0.0

        # レッドフラグ抽出
        red_flags = sorted(disease_symptom_set & RED_FLAG_SYMPTOMS)

        # 鑑別絞り込み質問
        rule_out_q: list[str] = []
        for sid in missing_ids[:2]:
            hsym = _humanize_id(sid, name_map)
            if lang == "ja":
                rule_out_q.append(f"{hsym['name_ja']} は確認できますか？")
            else:
                rule_out_q.append(f"Is {hsym['name_en']} present?")

        reasoning = DiseaseReasoning(
            disease_id=d.get("id") or d.get("disease_id") or d.get("name", ""),
            disease_name=d.get("name") or d.get("name_en", ""),
            disease_name_ja=d.get("name_ja") or d.get("name", ""),
            confidence=conf_val,
            urgency=urgency,
            matching_symptoms=[_humanize_id(s, name_map) for s in matching_ids],
            missing_typical_symptoms=[_humanize_id(s, name_map) for s in missing_ids],
            next_diagnostic_steps=[_humanize_id(t, name_map) for t in rec_test_ids[:5]],
            red_flags=red_flags,
            rule_out_questions=rule_out_q,
        )
        reasonings.append(reasoning)

    # 全体の次のステップ: 上位鑑別の検査の和集合 (上位3鑑別から)
    next_steps_set: set[str] = set()
    for r in reasonings[:3]:
        for t in r.next_diagnostic_steps:
            next_steps_set.add(t["id"])
    next_steps = [_humanize_id(t, name_map) for t in sorted(next_steps_set)][:6]

    # Bottom Line
    bottom_line, bl_evidence = _generate_bottom_line(reasonings, has_emergency, len(input_symptoms), lang=lang)

    # 信頼度警告
    confidence_warning = ""
    if len(input_symptoms) < 3:
        confidence_warning = (
            "症状入力が少ないため信頼度は限定的です。詳細な病歴・症状追加で精度向上。"
            if lang == "ja"
            else "Limited symptom input — confidence is constrained. Add more symptoms/history to improve accuracy."
        )

    return ClinicalReasoningResult(
        bottom_line=bottom_line,
        bottom_line_evidence=bl_evidence,
        differentials=reasonings,
        next_steps=next_steps,
        emergency_alert=has_emergency or bool(red_flags_in_input),
        needs_more_info=len(input_symptoms) < 3 or (reasonings and reasonings[0].confidence < 0.5),
        confidence_warning=confidence_warning,
    )


def to_dict(result: ClinicalReasoningResult) -> dict[str, Any]:
    """JSON返却用に辞書化"""
    return {
        "bottom_line": result.bottom_line,
        "bottom_line_evidence": result.bottom_line_evidence,
        "emergency_alert": result.emergency_alert,
        "needs_more_info": result.needs_more_info,
        "confidence_warning": result.confidence_warning,
        "next_steps": result.next_steps,
        "differentials": [
            {
                "disease_id": r.disease_id,
                "disease_name": r.disease_name,
                "disease_name_ja": r.disease_name_ja,
                "confidence": round(r.confidence, 4),
                "urgency": r.urgency,
                "matching_symptoms": r.matching_symptoms,
                "missing_typical_symptoms": r.missing_typical_symptoms,
                "next_diagnostic_steps": r.next_diagnostic_steps,
                "red_flags": r.red_flags,
                "rule_out_questions": r.rule_out_questions,
            }
            for r in result.differentials
        ],
    }
