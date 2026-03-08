"""Drug dictionary batch 2 - additional drugs for VetDict"""
from __future__ import annotations
from typing import Any, Dict, List

DRUGS_BATCH_2: List[Dict[str, Any]] = [
    {
        "id": "digoxin",
        "name": "Digoxin",
        "name_ja": "ジゴキシン",
        "category": "cardiovascular",
        "mechanism": "Cardiac glycoside that inhibits Na+/K+-ATPase, increasing intracellular calcium to enhance cardiac contractility and slow AV conduction",
        "mechanism_ja": "Na+/K+-ATPaseを阻害し、細胞内カルシウムを増加させて心収縮力を増強し、房室伝導を遅延させる強心配糖体",
        "species_info": {
            "dog": {"safe": True, "dosage": "0.005-0.01 mg/kg PO q12h", "dosage_ja": "0.005-0.01 mg/kg 経口 12時間ごと", "notes": "Monitor serum digoxin levels (1-2 ng/mL therapeutic). Narrow therapeutic index. Reduce dose in renal insufficiency.", "notes_ja": "血中ジゴキシン濃度をモニタリング（治療域1-2 ng/mL）。治療域が狭い。腎不全では減量。"},
            "cat": {"safe": True, "dosage": "0.005-0.01 mg/kg PO q48h or 1/4 of 0.125 mg tablet q48h", "dosage_ja": "0.005-0.01 mg/kg 経口 48時間ごと", "notes": "Cats are more sensitive to digoxin toxicity. Use with extreme caution and monitor levels closely.", "notes_ja": "猫はジゴキシン中毒に対してより感受性が高い。極めて慎重に使用し、血中濃度を綿密にモニタリング。"},
            "horse": {"safe": True, "dosage": "0.011 mg/kg IV loading, then 0.0055 mg/kg IV q12h", "dosage_ja": "0.011 mg/kg 静注負荷量、その後0.0055 mg/kg 静注 12時間ごと", "notes": "Used for atrial fibrillation and CHF. Monitor ECG and serum levels.", "notes_ja": "心房細動およびうっ血性心不全に使用。心電図と血中濃度をモニタリング。"},
            "rabbit": {"safe": False, "dosage": "Not recommended", "dosage_ja": "推奨されない", "notes": "Very narrow therapeutic index in rabbits; avoid use.", "notes_ja": "ウサギでは治療域が非常に狭い。使用を避ける。"},
            "ferret": {"safe": True, "dosage": "0.005-0.01 mg/kg PO q12-24h", "dosage_ja": "0.005-0.01 mg/kg 経口 12-24時間ごと", "notes": "Used for dilated cardiomyopathy. Monitor levels carefully.", "notes_ja": "拡張型心筋症に使用。血中濃度を慎重にモニタリング。"},
            "bird": {"safe": True, "dosage": "0.02-0.05 mg/kg PO q12h", "dosage_ja": "0.02-0.05 mg/kg 経口 12時間ごと", "notes": "Used in avian cardiology. Therapeutic monitoring essential.", "notes_ja": "鳥類の心臓病学で使用。治療薬物モニタリングが必須。"},
        },
        "side_effects": ["Anorexia", "Vomiting", "Diarrhea", "Cardiac arrhythmias", "Bradycardia", "AV block"],
        "side_effects_ja": ["食欲不振", "嘔吐", "下痢", "心不整脈", "徐脈", "房室ブロック"],
        "contraindications": "Contraindicated in hypokalemia, hypercalcemia, hypertrophic cardiomyopathy, ventricular tachycardia, and severe renal failure. Do not use with quinidine or verapamil without dose adjustment.",
        "contraindications_ja": "低カリウム血症、高カルシウム血症、肥大型心筋症、心室頻拍、重度腎不全では禁忌。キニジンやベラパミルとの併用時は用量調整が必要。",
    },
]
