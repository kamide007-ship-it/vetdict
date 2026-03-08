"""Drug dictionary batch 1 - additional drugs for VetDict"""
from __future__ import annotations
from typing import Any, Dict, List

DRUGS_BATCH_1: List[Dict[str, Any]] = [
    # ======================================================================
    # Antibiotics
    # ======================================================================
    {
        "id": "cefazolin",
        "name": "Cefazolin",
        "name_ja": "セファゾリン",
        "category": "antibiotics",
        "mechanism": "First-generation cephalosporin; inhibits bacterial cell wall synthesis by binding to penicillin-binding proteins. Bactericidal with good gram-positive coverage.",
        "mechanism_ja": "第一世代セファロスポリン系。ペニシリン結合蛋白に結合し細菌の細胞壁合成を阻害する。グラム陽性菌に良好な殺菌作用。",
        "species_info": {
            "dog": {"safe": True, "dosage": "20-35 mg/kg IV/IM q6-8h", "dosage_ja": "20-35 mg/kg 静注/筋注 6-8時間毎", "notes": "Excellent perioperative antibiotic. Give IV 30 min before surgery.", "notes_ja": "優れた周術期抗菌薬。手術前30分に静注投与。"},
            "cat": {"safe": True, "dosage": "20-35 mg/kg IV/IM q6-8h", "dosage_ja": "20-35 mg/kg 静注/筋注 6-8時間毎", "notes": "Safe for perioperative use in cats", "notes_ja": "猫の周術期に安全に使用可能"},
            "horse": {"safe": True, "dosage": "11-22 mg/kg IV q6-8h", "dosage_ja": "11-22 mg/kg 静注 6-8時間毎", "notes": "Used perioperatively; short half-life requires frequent dosing", "notes_ja": "周術期に使用。半減期が短く頻回投与が必要"},
            "rabbit": {"safe": True, "dosage": "20-30 mg/kg IV/IM/SC q8h", "dosage_ja": "20-30 mg/kg 静注/筋注/皮下 8時間毎", "notes": "Injectable cephalosporins are safe for rabbits unlike oral penicillins", "notes_ja": "注射用セファロスポリンは経口ペニシリンと異なりウサギに安全"},
            "hamster": {"safe": True, "dosage": "20-30 mg/kg SC/IM q8h", "dosage_ja": "20-30 mg/kg 皮下/筋注 8時間毎", "notes": "Injectable route safe; avoid oral cephalosporins", "notes_ja": "注射経路は安全。経口セファロスポリンは避ける"},
            "guinea_pig": {"safe": True, "dosage": "20-30 mg/kg SC/IM q8h", "dosage_ja": "20-30 mg/kg 皮下/筋注 8時間毎", "notes": "Injectable route safe; avoid oral route", "notes_ja": "注射経路は安全。経口投与は避ける"},
            "ferret": {"safe": True, "dosage": "15-25 mg/kg IV/IM/SC q8h", "dosage_ja": "15-25 mg/kg 静注/筋注/皮下 8時間毎", "notes": "Safe perioperative choice", "notes_ja": "安全な周術期の選択肢"},
            "bird": {"safe": True, "dosage": "50-100 mg/kg IM q6-8h", "dosage_ja": "50-100 mg/kg 筋注 6-8時間毎", "notes": "Higher doses needed due to rapid clearance in birds", "notes_ja": "鳥類では排泄が速いため高用量が必要"},
            "reptile": {"safe": True, "dosage": "20 mg/kg IM q12-24h", "dosage_ja": "20 mg/kg 筋注 12-24時間毎", "notes": "Adjust interval based on ambient temperature", "notes_ja": "環境温度により投与間隔を調整"},
        },
        "side_effects": ["pain at injection site", "hypersensitivity reactions", "GI upset", "thrombophlebitis"],
        "side_effects_ja": ["注射部位の痛み", "過敏反応", "消化器症状", "血栓性静脈炎"],
        "contraindications": "Hypersensitivity to cephalosporins or penicillins (cross-reactivity possible). Caution with renal impairment.",
        "contraindications_ja": "セファロスポリンまたはペニシリン過敏症（交差反応の可能性）。腎機能障害には注意。",
    },
