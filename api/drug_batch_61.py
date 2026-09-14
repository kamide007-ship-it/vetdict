"""Drug batch 61 – referenced-but-absent agent surfaced by the 2026-09 audit (26th sweep).

A dose-context English/katakana token sweep found one true monograph gap:

  - Indomethacin — the formulary's own disease entries prescribe it by name
    with doses: canine nephrogenic diabetes insipidus ("Indomethacin 1-2 mg/kg
    PO q12h — reduces prostaglandin-mediated renal blood flow, limited use")
    and equine neonatal patent ductus arteriosus ("indomethacin 0.2 mg/kg IV
    q12h ×3 — prostaglandin inhibitor promotes ductal closure, limited equine
    data"). Neither indication is analgesic: indomethacin is one of the most
    ulcerogenic NSAIDs known in dogs (fatal GI hemorrhage reported at low
    doses), so the monograph exists to document the two niche referenced uses
    WITH their guardrails, not to offer indomethacin as a pain reliever.

References:
  - Plumb's Veterinary Drug Handbook 10th ed — indomethacin: not recommended
    as an analgesic in dogs/cats (severe GI toxicity).
  - Nelson & Couto, Small Animal Internal Medicine 6th ed — prostaglandin
    synthetase inhibitors as thiazide adjuncts in nephrogenic DI.
  - Ewing GO, JAVMA 1972 — fatal indomethacin gastropathy in dogs.
  - Human neonatology standard of care (indomethacin PDA closure),
    extrapolated to foals with limited data (equine cardiology references).
"""

DRUGS_BATCH_61 = [
    {
        "id": "indomethacin",
        "search_aliases": [
            "インドメタシン",
            "indomethacin",
        ],
        "name": "Indomethacin",
        "name_ja": "インドメタシン",
        "category": "nsaids",
        "mechanism": "Potent non-selective COX-1/COX-2 inhibitor (indole-acetic-acid NSAID). Profound prostaglandin synthesis blockade underlies both niche veterinary uses: reducing prostaglandin-mediated renal free-water excretion in nephrogenic diabetes insipidus, and promoting closure of a patent ductus arteriosus (ductal patency is PGE2-dependent) in neonates.",
        "mechanism_ja": "強力な非選択的COX-1/COX-2阻害薬（インドール酢酸系NSAID）。強度のプロスタグランジン合成阻害が2つのニッチな獣医学的用途の基盤: 腎性尿崩症でのプロスタグランジン介在性自由水排泄の抑制、および新生子の動脈管開存（開存はPGE2依存性）の閉鎖促進。",
        "species_info": {
            "dog": {
                "safe": False,
                "dosage": "NOT an analgesic option — dogs are exquisitely sensitive to indomethacin GI ulceration (fatal hemorrhagic gastropathy reported at low doses; Ewing JAVMA 1972; Plumb's 10th ed). The single referenced niche use is refractory nephrogenic diabetes insipidus as a thiazide adjunct: 1-2 mg/kg PO q12h WITH gastroprotection (omeprazole + sucralfate ± misoprostol), the lowest effective dose, and owner counselling on melena; discontinue at any GI sign (Nelson & Couto 6th ed).",
                "dosage_ja": "鎮痛薬としての選択肢ではない — 犬はインドメタシンによる消化管潰瘍に極めて感受性が高い（低用量でも致死的出血性胃症の報告; Ewing JAVMA 1972; Plumb's 10th ed）。参照される唯一のニッチ用途は難治性腎性尿崩症でのサイアザイド補助: 1-2 mg/kg PO q12h を必ず消化管保護（オメプラゾール+スクラルファート±ミソプロストール）併用・最小有効量で行い、飼い主にメレナを指導。消化器徴候が出れば即中止（Nelson & Couto 6th ed）。",
                "notes": "First-line NDI management remains thiazides + low-sodium diet; indomethacin is a last-resort adjunct. Never combine with corticosteroids or other NSAIDs.",
                "notes_ja": "腎性尿崩症の第一選択は依然サイアザイド+低ナトリウム食であり、インドメタシンは最後の手段の補助。ステロイド・他のNSAIDsとの併用は絶対不可。",
            },
            "cat": {
                "safe": False,
                "dosage": "Contraindicated — no accepted feline indication; feline glucuronidation deficiency plus indomethacin's ulcerogenicity make toxicity risk unacceptable (Plumb's 10th ed).",
                "dosage_ja": "禁忌 — 猫に確立した適応はなく、グルクロン酸抱合能の低さとインドメタシンの高い潰瘍原性から毒性リスクが許容できない（Plumb's 10th ed）。",
            },
            "horse": {
                "safe": True,
                "dosage": "Neonatal foal PDA closure attempt: 0.2 mg/kg IV q12h ×3 doses (prostaglandin inhibitor promotes ductal closure — extrapolated from human neonatology; limited equine data, so reserve for a persistent hemodynamically significant PDA beyond the first days of life). Monitor renal values and GI signs; ensure adequate hydration.",
                "dosage_ja": "新生子馬のPDA閉鎖トライアル: 0.2 mg/kg IV q12h×3回（プロスタグランジン阻害で動脈管閉鎖を促進 — ヒト新生児医療からの外挿で馬でのデータは限定的。生後数日を超えて持続する血行動態的に有意なPDAに温存）。腎数値・消化器徴候をモニタリングし、十分な水和を確保。",
                "notes": "Most foal PDAs close spontaneously within days of birth — auscultate serially before treating. Surgical ligation at a referral center for medical failures. In adult horses flunixin/phenylbutazone remain the NSAIDs of use; indomethacin has no adult indication.",
                "notes_ja": "子馬のPDAの多くは生後数日で自然閉鎖する — 治療前に連日聴診で確認。内科的閉鎖失敗例は専門施設での外科的結紮。成馬のNSAIDsはフルニキシン/フェニルブタゾンであり、インドメタシンに成馬適応はない。",
            },
        },
        "drug_interactions": [
            {
                "drug": "Corticosteroids",
                "effect": "Greatly increased risk of GI ulceration/perforation — never combine",
                "effect_ja": "消化管潰瘍・穿孔リスクの大幅増加 — 併用絶対不可",
                "severity": "major",
            },
            {
                "drug": "Other NSAIDs",
                "effect": "Additive GI and renal toxicity — never combine; observe washout when switching",
                "effect_ja": "消化管・腎毒性の相加 — 併用不可。切替時はウォッシュアウトを設ける",
                "severity": "major",
            },
            {
                "drug": "Furosemide",
                "effect": "Prostaglandin blockade blunts diuretic/natriuretic response and increases renal risk",
                "effect_ja": "プロスタグランジン阻害により利尿・ナトリウム利尿反応が減弱し腎リスクが増加",
                "severity": "moderate",
            },
        ],
    },
]
