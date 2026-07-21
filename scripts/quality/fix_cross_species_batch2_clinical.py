#!/usr/bin/env python3
"""Vet-approved clinical rewrites for the 2 cross-class cases held back from the
batch-2 relabels (approved by Kentaro, '☑️').

  - sugar_glider Proptosis (Eye Prolapse): reptile abscess/culture content ->
    mammalian traumatic globe-prolapse emergency management
  - parrot Atherosclerosis: budgerigar epidemiology + endocrine template ->
    parrot cardiovascular disease

Both records are module-only (JSON overlay has 0 entries), so only the module
source-of-truth is patched. treatment_ja carries a runtime ECVN suffix that is
NOT in the source, so we replace the source *base* string (the suffix is added
at import). Backed up, idempotent (old absent / new present -> skip).

    python3 scripts/quality/fix_cross_species_batch2_clinical.py --ts <ts> [--apply]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

# module path -> list of (field_label, old_exact, new_exact)
FIXES = {
    REPO / "api/species/sugar_glider_diseases.py": [
        (
            "Proptosis.causes_ja",
            "トカゲにおける眼球突出症の原因: 感染、膿瘍、占拠性病変による眼球の異常突出です。",
            "フクロモモンガにおける眼球突出症（眼球脱出）の原因: 多くは外傷（咬傷・拘束・落下）による急性の眼球前方脱出。眼窩後方の占拠性病変（膿瘍・腫瘍）が誘因となることもある。",
        ),
        (
            "Proptosis.treatment_ja",
            "トカゲにおける眼球突出症の治療には、可能であれば培養感受性試験に基づく標的抗菌薬療法が必要である。結果待ちの間は経験的広域抗菌薬を開始する。抗菌薬治療期間は感染の排除と耐性予防に十分な期間とする。膿瘍や壊死組織には外科的排膿またはデブリードマンが必要な場合がある。支持療法として輸液、鎮痛薬、抗炎症薬、栄養サポートを行う。",
            "フクロモモンガにおける眼球突出症（眼球脱出）は救急疾患である。角膜乾燥を防ぐため直ちに眼表面を湿潤・保護し、鎮痛下で可及的に眼球整復と一時的眼瞼縫合（tarsorrhaphy）を試みる。整復不能・眼球破裂・視覚予後不良例は眼球摘出を行う。全身状態の安定化・鎮痛・二次感染予防の抗菌薬・原因（外傷／占拠性病変）の検索を併せて行う。",
        ),
    ],
    REPO / "api/species/parrot_diseases.py": [
        (
            "Atherosclerosis.causes_ja",
            "インコにおける動脈硬化症の原因: 動脈内のコレステロールプラーク蓄積による血流低下で、種子食の高齢セキセイインコに多発。",
            "オウムにおける動脈硬化症の原因: 大動脈・主要動脈へのコレステロール／脂質プラーク蓄積による血管壁肥厚・内腔狭窄。高脂肪・種子食、運動不足、加齢、脂質代謝異常が危険因子で、ヨウム・ボウシインコ等の高齢オウム類やセキセイインコに多い。",
        ),
        (
            "Atherosclerosis.pathophysiology_ja",
            "動脈硬化症はインコにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
            "動脈硬化症はオウムにおける心血管疾患である。慢性の脂質蓄積と血管内皮傷害により大動脈・腕頭動脈などにアテローム様プラークが形成され、血管壁の肥厚・硬化・内腔狭窄を来す。進行すると後負荷増大・組織灌流低下により運動不耐性・虚脱・神経症状（脳虚血）・突然死につながりうる。",
        ),
    ],
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ts", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if args.apply:
        bdir = REPO / "backups" / args.ts
        bdir.mkdir(parents=True, exist_ok=True)
        for path in FIXES:
            shutil.copy2(path, bdir / path.name)
        print(f"backup → {bdir}")

    for path, items in FIXES.items():
        text = path.read_text(encoding="utf-8")
        orig = text
        for label, old, new in items:
            if old in text:
                text = text.replace(old, new)
                print(f"{path.name}: {label} rewritten")
            elif new in text:
                print(f"{path.name}: {label} already-applied (skip)")
            else:
                print(f"⚠️ {path.name}: {label} neither old nor new — SKIP")
        if args.apply and text != orig:
            path.write_text(text, encoding="utf-8")
    print("APPLIED" if args.apply else "DRY-RUN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
