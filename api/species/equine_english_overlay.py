"""English clinical narrative for Japanese-first horse disease records.

A subset of the equine :class:`~api.species.equine_diseases.Disease` records were
authored with curated *Japanese* clinical text only (repro/gastric/toxic
syndromes added JA-first).  Their English narrative columns therefore fell back
to the Japanese string, so an English viewer of the disease browser or a
differential-diagnosis result saw Japanese text in the causes / pathophysiology
/ clinical-signs / prevention / prognosis sections.

This module holds faithful English translations of that already-curated
Japanese narrative — the *non-dosing* fields only.  Treatment protocols (which
carry drug doses) are intentionally excluded: per project policy, dosing text is
not machine-translated for patient safety and remains Japanese pending
veterinary human translation.

Each value is keyed by the ``Disease.id`` and applied onto the matching
dataclass instance's ``*_en`` fields by ``equine_diseases._apply_horse_english``.
The migrate step and the runtime serving paths prefer the ``*_en`` field and
fall back to the Japanese one, so untranslated records are unaffected.
"""

from __future__ import annotations

# id -> {etiology_en, pathophysiology_en, clinical_signs_detail_en,
#        prevention_en, prognosis_en}
HORSE_ENGLISH: dict[str, dict[str, str]] = {
    "rp_red_bag": {
        "etiology_en": (
            "The most common cause is ascending placentitis (Streptococcus, Nocardioform "
            "actinomycetes, fungi) producing chorioallantoic thickening and impaired adherence. "
            "Fescue toxicosis (placental thickening from ingestion of ergovaline-producing "
            "Festuca arundinacea), twin pregnancy, prolonged gestation, endometrial scarring and "
            "EHV-1 placentitis are additional causes. All lead to premature separation of the "
            "endometrium from the chorioallantois."
        ),
        "pathophysiology_en": (
            "In normal delivery the chorioallantois (CA) ruptures at the cervical star and the "
            "white amnion is exposed. In a red-bag delivery the placenta separates from the uterus "
            "prematurely, the CA fails to rupture, and the red velvety chorionic surface prolapses "
            "through the vulva. Placental separation cuts off maternal oxygen and nutrient supply, "
            "producing rapidly progressive fetal hypoxia; the interval from complete separation to "
            "fetal death is only about 5-10 minutes. Triggers: placentitis (most common — "
            "Streptococcus equi zooepidemicus, E. coli, Nocardioform, fungi), fescue toxicosis "
            "(ergovaline), twin pregnancy, endometrial scarring, prolonged gestation (>360 days), "
            "and maternal fever or systemic disease."
        ),
        "clinical_signs_detail_en": (
            "(1) During second-stage labour a red velvety chorionic surface protrudes from the "
            "vulva instead of the white amnion — this is the 'red bag'. (2) The foal's forelimbs "
            "and nose are not visible, or malposition is present. (3) Labour stalls: the mare "
            "strains strongly but the foal does not advance. (4) As separation progresses the "
            "mare's abdomen drops and fetal movement weakens. (5) After delivery the foal shows "
            "delayed standing (>1 hour), weak suckle, cyanosis, brady- or tachycardia, "
            "hypothermia, seizures and aimless wandering (neonatal maladjustment signs). "
            "(6) The mare may show premature udder development and lactation in the preceding days, "
            "purulent/bloody vulvar discharge and fever (signs of placentitis)."
        ),
        "prevention_en": (
            "(1) Late-gestation (>270 days) transrectal ultrasound to measure combined thickness of "
            "uterus and placenta (CTUP) at the ventral cervical pole — >11.5 mm at 330 days or "
            ">15 mm at 370 days suggests placentitis; treat with altrenogest 0.044 mg/kg PO SID "
            "(until 30 days pre-foaling) plus trimethoprim-sulfa and fluconazole. (2) Twin "
            "management: diagnose by ultrasound at 14-16 days and reduce to a single conceptus by "
            "manual crush or transcervical aspiration. (3) Remove the Caslick suture before "
            "foaling (vulvar restoration in mares >320 days). (4) Remove the dam from fescue "
            "pasture 90 days before foaling (ergot-alkaloid avoidance). (5) Attended foaling "
            "(24-hour watch, CCTV, foaling-alert systems). (6) Clean, non-slip, warm (>25°C) "
            "foaling stall. (7) Keep a foaling kit ready: sterile scissors (to open the CA), iodine, "
            "a neonatal resuscitation kit (mask O2, endotracheal tube, adrenaline, dextrose, "
            "naloxone) and mare oxytocin, prostaglandin and antimicrobials."
        ),
        "prognosis_en": (
            "Guarded and highly time-dependent: because the CA has already separated, the attendant "
            "must tear it open immediately and deliver the foal within minutes. With prompt "
            "intervention many foals survive, but any delay causes severe hypoxic-ischaemic "
            "encephalopathy or stillbirth. Survivors need intensive neonatal care and monitoring "
            "for maladjustment syndrome; the underlying placentitis also affects mare fertility."
        ),
    },
    "rp_uterine_artery_rupture": {
        "etiology_en": (
            "The condition is rupture of the middle uterine, ovarian or iliac artery in older "
            "multiparous mares (>15 years). Age-related degeneration of the elastic fibres of the "
            "vessel wall, together with reduced lysyl oxidase activity from copper deficiency "
            "(defective elastin cross-linking), underlies the vascular fragility; prolonged or "
            "difficult labour, an oversized foal and forceful traction are the triggers for "
            "rupture."
        ),
        "pathophysiology_en": (
            "In older multiparous mares, degeneration of the vessel-wall elastic fibres (copper "
            "deficiency and age-related arteriosclerosis) makes the artery rupture under the "
            "stretching stress of parturition. The commonest site is the middle uterine artery "
            "(within the broad ligament, ventral to L4-L5), followed by the ovarian, external "
            "iliac arteries and the aortic bifurcation. Three bleeding patterns occur: (A) a "
            "contained broad-ligament haematoma (initially self-limiting), (B) intra-abdominal "
            "haemorrhage (after broad-ligament rupture), and (C) intra-uterine haemorrhage (blood "
            "pooling visible on examination). Blood loss can reach 20-40 L within a short time, "
            "exceeding 50% of circulating volume. Compensation — sympathetic drive, peripheral "
            "vasoconstriction and tachycardia — maintains blood pressure for 2-6 hours, then "
            "circulatory collapse is sudden. Re-bleeding risk is highest within 48-72 hours, and "
            "strict rest with blood-pressure control determines the outcome."
        ),
        "clinical_signs_detail_en": (
            "(1) Sudden onset during labour to within 72 hours postpartum (acute peak 12-24 hours "
            "after foaling). (2) Early: abrupt severe colic-like signs (abdominal pain, pawing, "
            "repeated recumbency, rolling). (3) Circulatory shock: tachycardia (>80 bpm), "
            "tachypnoea (>40 breaths/min), pale mucous membranes, CRT >3 s, cold extremities, "
            "sweating. (4) Depression, collapse, difficulty rising. (5) Transrectal palpation of a "
            "broad-ligament haematoma (a 30-50 cm spherical, fluctuant mass ventral to L4-L5 "
            "narrowing the pelvic canal). (6) With ongoing intra-abdominal bleeding: abdominal "
            "distension, dyspnoea, cyanosis, loss of consciousness. (7) Mucous membranes: pale "
            "early, yellow-white with severe anaemia, finally blue-white with collapse. "
            "(8) Temperature normal to low (haemorrhagic shock). (9) A stance with the forelimbs "
            "spread to avoid abdominal tension and the neck flexed. (10) Sudden death (within hours "
            "of apparent normality, especially with aortic-bifurcation rupture)."
        ),
        "prevention_en": (
            "Breeding management: (1) Consider retiring mares >15 years from breeding after weighing "
            "foaling risk, longevity and quality of life; stop breeding by ~20 years as a rule. "
            "(2) Pre-breeding work-up: endometrial biopsy (avoid breeding with Kenney category III / "
            "copper-deficiency findings), CBC, biochemistry and coagulation profile, Cu/Se/Vit E "
            "measurement, and documentation of any prior dystocia or haemorrhage. (3) Nutrition: "
            "Cu 100-150 mg/day (organic copper preferred), Zn 200-400 mg/day (Cu:Zn 3:1), Vit E "
            "2,000-3,000 IU/day, Se 3-5 mg/day, Vit K1 200-400 mg/day (with dicoumarol exposure in "
            "pasture). Foaling management: (4) 24-hour foaling surveillance, with prompt "
            "intervention if second stage is prolonged (>30-40 min). (5) Assist with minimal force, "
            "avoiding excessive traction (pull in time with the mare's straining, not against the "
            "birth canal). (6) Consider early caesarean for malposition in second stage (after "
            ">40 min of failed intervention). (7) Foaling kit: sterile gloves, lubricant, "
            "obstetric chains, neonatal resuscitation kit, and blood-typed blood products or "
            "Oxyglobin. Postpartum: (8) Strict rest for 72 hours (avoid unnecessary handling and "
            "transport; keep foal contact in a quiet environment). (9) Monitor vitals every 4-6 h "
            "(palpate transrectally if HR >60, mucous-membrane change or behavioural change). "
            "(10) Low-dose oxytocin postpartum (10 IU IM q6h); use prostaglandin sparingly "
            "(10 mg q12h, ≤3 doses) as overdose raises re-bleeding risk. (11) In multiparous mares, "
            "screen broad ligament and abdomen by transrectal ultrasound 3-7 days postpartum for "
            "early detection of subclinical haematoma."
        ),
        "prognosis_en": (
            "Guarded to poor and highly dependent on the bleeding pattern. A contained "
            "broad-ligament haematoma managed with strict rest, sedation and blood-pressure "
            "control carries a fair prognosis, whereas free intra-abdominal haemorrhage frequently "
            "causes fatal hypovolaemic shock. Re-bleeding risk is greatest in the first 48-72 hours; "
            "survivors that stabilise past this window generally recover, though future breeding "
            "carries a high recurrence risk."
        ),
    },
    "fl_shaker_foal": {
        "etiology_en": (
            "A toxico-infectious botulism: spores of Clostridium botulinum (mainly type B) "
            "germinate and proliferate within the gut and produce botulinum neurotoxin in situ. It "
            "occurs in foals 2-8 weeks old — whose intestinal flora is still immature — in regions "
            "with a high density of soil spores (the US Mid-Atlantic; rare in Japan)."
        ),
        "pathophysiology_en": (
            "Aetiology: Clostridium botulinum type B (the Mid-Atlantic soil spore, with types A and "
            "C rare) enters by the oral or wound route, proliferates in the foal's gut (favourable "
            "pH and oxygen tension), produces exotoxin (BoNT-B) that is absorbed across the "
            "intestinal mucosa and blocks acetylcholine release at peripheral neuromuscular "
            "junctions and autonomic nerve endings, causing flaccid paralysis. Foals aged 2-8 weeks "
            "are most susceptible because: (1) higher gut pH (less gastric acid than adults), "
            "(2) immature colicin production, (3) immature resident gut flora (weak competitive "
            "exclusion), and (4) coincidence with the nadir of passive immunoglobulin. Clinical "
            "progression: (1) pharyngeal and tongue paralysis (dysphagia, drooling), (2) limb and "
            "trunk paralysis (trembling, falling), (3) flaccid eyelids and nictitans (ptosis), "
            "(4) sphincter paralysis (urine retention, ileus), (5) respiratory-muscle paralysis "
            "leading to death. Recovery of neuromuscular function requires formation of new motor "
            "end-plates (weeks to months), so acute-phase supportive care is critical."
        ),
        "clinical_signs_detail_en": (
            "Onset at 2-8 weeks of age (typically 3-5 weeks), with progressive signs. "
            "(1) Early (day 1-2): reduced desire to nurse and reduced intake, excessive drooling "
            "(saliva dribbling from the commissures because of dysphagia), mild neck weakness. "
            "(2) Progressive (days 2-5): shortened standing time, frequent recumbency, trembling "
            "(especially shoulder, limb and tail muscles), reduced tongue tone (the tongue extends "
            "easily and retracts weakly when drawn out), nictitans protrusion, mydriasis, "
            "pharyngeal paralysis (aspiration on nasogastric intubation). (3) Terminal (days 5-7, "
            "untreated): complete recumbency, limb paralysis, respiratory-muscle paralysis with "
            "abdominal breathing, abnormal heart rate (tachy- or bradycardia), hypothermia, and "
            "death from respiratory arrest or aspiration pneumonia. (4) Diagnostic features: "
            "consciousness is preserved to the end (normal cerebral function); sensory responses "
            "are preserved but motor responses are reduced; autonomic signs (mydriasis, urine "
            "retention, ileus) are present; seizures are usually absent. (5) Differentials: "
            "hypoxic-ischaemic encephalopathy / neonatal maladjustment (onset right after birth, "
            "seizures, altered consciousness), sepsis (fever, inflammatory markers), hypoglycaemia "
            "(improves with correction of low blood glucose), tetanus (spastic paralysis), "
            "organophosphate toxicosis (miosis, salivation, frequent urination), nutritional "
            "myopathy (markedly elevated CK), Lyme disease (seasonal, seropositive)."
        ),
        "prevention_en": (
            "Vaccination (most important): (1) Mare type B toxoid (BotVax-B): essential in endemic "
            "areas — two doses in late gestation at 4 and 2 weeks pre-foaling (a 3-dose course for "
            "the first pregnancy), then annually; passive immunity transfers to the foal via "
            "colostral IgG (effective for 2-3 months of age). (2) Foal type B toxoid: in endemic "
            "areas, two doses at 2 and 4 months of age (or as colostral IgG wanes), then annually. "
            "(3) Vaccination of imported stallions and broodmares is advised even in non-endemic "
            "areas. Environmental management: (4) Clean pastures and stables — promptly remove "
            "decomposing carcasses (dogs, rodents, birds), remove faeces, and manage soil pH "
            "(neutral to mildly acidic; pH <6.5 suppresses C. botulinum). (5) Feed management: "
            "absolutely avoid damp fermented feed and mouldy hay, store feed well dried, and "
            "inspect before feeding. (6) Test and protect ground/well water from contamination. "
            "(7) Foal wound care: umbilical disinfection (2% iodine), early cleaning of wounds; be "
            "cautious with prophylactic antibiotics because of their effect on gut flora. Early "
            "detection: (8) Observe foals daily and record any change in nursing, behaviour or "
            "gait immediately. (9) Seek veterinary advice at once for abnormal signs (drooling, "
            "trembling, difficulty rising, dysphagia). (10) With clustered cases (multiple "
            "littermates or nearby farms) monitor other foals prophylactically. Farm-level: "
            "(11) On farms with a history, intensify vaccination of all broodmares and neonates, "
            "test soil, water and feed, sample and monitor, and follow AAEP foal-health guidelines."
        ),
        "prognosis_en": (
            "Guarded; heavily dependent on early recognition and access to intensive supportive "
            "care. With mechanical ventilation and botulinum antitoxin, survival can reach "
            "50-70% at referral centres, but on-farm cases that progress to respiratory paralysis "
            "have a poor outcome. Survivors need weeks of nursing while new motor end-plates form; "
            "with successful recovery, long-term function is usually good."
        ),
    },
    "dg_phytobezoar": {
        "etiology_en": (
            "The cause is aggregation and dehydration of poorly chewed long-fibre roughage "
            "(long-stemmed straw or cut grass) within the colon or caecum to form a fibrous "
            "concretion. Impaired mastication from dental disease, inadequate water intake (frozen "
            "water sources in winter), lack of exercise and chronic constipation are predisposing "
            "factors; this is a distinct entity from a persimmon-tannin gastric phytobezoar."
        ),
        "pathophysiology_en": (
            "Undigested fibre gradually enlarges in the small (descending) colon — the "
            "narrowest-diameter segment — as ingesta dehydrate and motility falls, mechanically "
            "obstructing the lumen. Distension and stretching of the bowel wall proximal to the "
            "obstruction cause colic, and progression carries a risk of wall ischaemia and rupture."
        ),
        "clinical_signs_detail_en": (
            "Chronic, recurrent mild colic; reduced or absent defecation; straining to defecate; "
            "abdominal distension (partial obstruction); tachycardia, sweating and acute colic with "
            "complete obstruction; a palpable mass on rectal examination with small-colon "
            "obstruction; secondary gastric reflux is a terminal finding."
        ),
        "prevention_en": (
            "Regular dental checks (every 6 months), a clean and adequate water supply, appropriate "
            "management of roughage length, prophylactic psyllium, sand management, and individual "
            "feeding management of older horses."
        ),
        "prognosis_en": (
            "Good with successful medical management; horses treated by surgical removal also survive "
            "at 70-85% with appropriate care. Cases with progressive small-colon ischaemia or "
            "perforation carry a poor prognosis. There is a risk of recurrence, so ongoing "
            "husbandry management is essential."
        ),
    },
    "rp_lactation_failure": {
        "etiology_en": (
            "Peripartum malnutrition, primiparity or advanced age (>20 years), trace-element "
            "deficiency (Se, Cu, Zn), endocrine disorders (hypothyroidism, PPID), fescue toxicosis "
            "(prolactin suppression by ergot alkaloids), a history of mastitis and stress can all "
            "cause failure of milk production or let-down."
        ),
        "pathophysiology_en": (
            "Equine lactation depends on a rapid rise in prolactin immediately after foaling. It is "
            "primary (mammary hypoplasia, hormonal abnormality) or secondary (mastitis, "
            "malnutrition, stress). Prolactin secretion is promoted by dopamine antagonism "
            "(metoclopramide), domperidone (a selective dopamine-receptor antagonist) and "
            "Saccharomyces boulardii (a probiotic). Peripartum vitamin/mineral deficiency (Se, Cu, "
            "Zn, Mg) causes deficient prolactin production. The foal must obtain passive immunity "
            "(IgG) by colostral intake within 24 hours; IgG <800 mg/dL indicates failure of passive "
            "transfer (FPT) with a 16-fold increase in infection risk."
        ),
        "clinical_signs_detail_en": (
            "Indistinct mammary enlargement after foaling; scant milk (no drip from the teat); weak "
            "suckle and low nursing frequency in the foal (normal is hourly); foal depression; "
            "weight loss (a 10-15% loss of birth weight is normal but >20% is abnormal); a firm, "
            "cool mammary gland on palpation; and abnormal milk composition (watery, low fat)."
        ),
        "prevention_en": (
            "6-8 weeks pre-foaling: nutritional assessment leading to a balanced ration (protein "
            "12-14%, Se 3-5 mg/day, Cu 80-160 mg/day, Zn 400-600 mg/day, Mg 3-5 g/day). 3-4 weeks "
            "pre-foaling: selenium plus vitamin E (veterinary prescription). 1-2 weeks pre-foaling: "
            "monitor mammary development (onset of waxing as a guide). Immediately after foaling: "
            "provide fresh drinking water and freeze-dried banked colostrum (freeze-drying retains "
            ">90% of IgG)."
        ),
        "prognosis_en": (
            "Variable and dependent on the underlying cause: nutritional and stress-related cases "
            "usually respond to domperidone plus improved husbandry, whereas primary mammary "
            "hypoplasia responds poorly. The critical determinant is ensuring the foal receives "
            "adequate colostrum or a substitute within the first 24 hours; failure of passive "
            "transfer sharply worsens the foal's outlook."
        ),
    },
    "dg_gastric_ulcer_squamous": {
        "etiology_en": (
            "Unlike the glandular region, the squamous mucosa lacks a mucus-bicarbonate barrier, so "
            "direct exposure to gastric acid (hydrochloric acid), volatile fatty acids and bile "
            "acids is the cause. Intermittent fasting (an empty stomach for >6 hours), "
            "high-intensity exercise (raised abdominal pressure splashing acid onto the squamous "
            "region), high-grain/low-roughage feeding and transport or social stress aggravate acid "
            "exposure; concurrent NSAIDs secondarily raise the risk."
        ),
        "pathophysiology_en": (
            "During fasting or exercise, acidic gastric contents contact the poorly protected "
            "squamous mucosa above the margo plicatus and chemically erode it, forming erosions and "
            "ulcers. When salivary bicarbonate from chewing roughage and the calcium buffering of "
            "alfalfa fall, intragastric pH drops and the disease progresses. ESGD is essentially "
            "acid-induced and responds well to acid suppression (omeprazole), which distinguishes "
            "it from glandular disease (EGGD)."
        ),
        "clinical_signs_detail_en": (
            "Chronic mild colic (30 min-2 h after eating), inappetence (especially leaving grain), "
            "weight loss, a poor coat, reduced performance, bruxism, flehmen, excessive salivation "
            "and postural change (arched back). Chronic anaemia in severe cases. Many cases are "
            "asymptomatic and can only be diagnosed by gastroscopy."
        ),
        "prevention_en": (
            "24-hour access to forage, at least six small meals a day, grain <2 g/kg/day, alfalfa "
            "supplementation, feeding before exercise, stress reduction, and prophylactic "
            "omeprazole (1-2 mg/kg SID) during transport and racing."
        ),
        "prognosis_en": (
            "Good — with appropriate medication and improved husbandry, 70-90% heal within 4 weeks. "
            "Without improved management the recurrence rate exceeds 30%. ECEIM grade-4 and "
            "complicated cases take longer to heal."
        ),
    },
    "dg_gastric_ulcer_glandular": {
        "etiology_en": (
            "The glandular mucosa is normally protected from acid by a mucus-bicarbonate layer and "
            "prostaglandin-dependent mucosal blood flow; in EGGD the cause is breakdown of this "
            "mucosal defence (not acid excess alone). Exercise stress of five or more days a week, "
            "NSAIDs (which suppress prostaglandin production) and social stress are involved, and a "
            "role for Helicobacter-like organisms is suggested but unconfirmed."
        ),
        "pathophysiology_en": (
            "A decline in defensive factors (mucus and bicarbonate secretion, mucosal blood flow, "
            "epithelial regeneration) makes the glandular mucosa vulnerable to endogenous acid and "
            "bile, forming inflammatory and ulcerative lesions in the pyloric antrum and gastric "
            "body. It heals more slowly than ESGD, and because acid suppression alone is "
            "insufficient the requirement for concurrent mucosal protectants (e.g. sucralfate) is a "
            "characteristic feature of its pathophysiology."
        ),
        "clinical_signs_detail_en": (
            "Chronic colic (especially after eating), reduced appetite (especially grain "
            "avoidance), weight loss, a poor coat, temperament change (increased aggression or "
            "sensitivity), reduced performance, bruxism, flehmen and girth/saddle sensitivity. "
            "Similar to ESGD but responds poorly to treatment and tends to become chronic. "
            "Gastroscopy shows reddening, linear ulcers and fibrin adherence in the pyloric antrum "
            "and gastric body."
        ),
        "prevention_en": (
            "Stress management (one full rest day a week, a consistent exercise schedule, a stable "
            "social environment), avoidance of long-term NSAID use, switching to a COX-2 selective "
            "NSAID, appropriate roughage feeding, and continued maintenance therapy in chronically "
            "affected horses."
        ),
        "prognosis_en": (
            "Guarded — the treatment response is slower than ESGD, with a healing rate of 55-70%. "
            "Without removal of environmental factors the recurrence rate is high, and cases "
            "complicated by pyloric stenosis have a poor prognosis."
        ),
    },
    "dg_right_dorsal_colitis": {
        "etiology_en": (
            "The main cause is COX-1 inhibition from overdose, prolonged use or dehydrated "
            "administration of NSAIDs (especially phenylbutazone). The right dorsal colon is "
            "anatomically poor in collateral blood supply and is therefore particularly vulnerable "
            "to prostaglandin-dependent reductions in mucosal blood flow."
        ),
        "pathophysiology_en": (
            "Deficiency of COX-1-derived prostaglandins reduces mucosal blood flow, mucus secretion "
            "and epithelial repair, producing ulcerative and granulomatous inflammation of the "
            "right dorsal colon. Breakdown of the mucosal barrier causes protein loss "
            "(hypoalbuminaemia), diarrhoea and weight loss, and chronic cases progress to fibrosis "
            "and stricture of the bowel wall."
        ),
        "clinical_signs_detail_en": (
            "Chronic mild colic (recurrent, with a history of NSAID use), watery to mucoid "
            "diarrhoea, weight loss, abdominal distension from ascites, ventral oedema "
            "(hypoalbuminaemia), a poor coat, inappetence and intermittent fever. Onset ranges "
            "widely from 1-2 weeks to several months after starting NSAIDs. The acute phase can "
            "cause severe colic and shock."
        ),
        "prevention_en": (
            "Lowest NSAID dose for the shortest time; phenylbutazone <4.4 mg/kg BID for a maximum "
            "of 5-7 days; avoid dosing during dehydration; switch to a COX-2 selective NSAID "
            "(firocoxib 0.1 mg/kg SID); combine gabapentin/tramadol for long-term pain management; "
            "and periodically assess renal function and hydration status."
        ),
        "prognosis_en": (
            "With early diagnosis and NSAID discontinuation, 60-80% improve on medical management. "
            "Chronic cases and those forming strictures carry a poor prognosis. Complete healing "
            "takes 3-6 months; there is a recurrence risk, and lifelong NSAID avoidance is "
            "recommended."
        ),
    },
    "dg_colitis_x": {
        "etiology_en": (
            "Historically an idiopathic peracute colitis syndrome, most cases are now reclassified "
            "under specific causes such as Clostridioides difficile/perfringens, Salmonella and "
            "Neorickettsia risticii (Potomac horse fever). Acute severe stress (long-distance "
            "transport, surgery, foaling, racing), antibiotics, NSAIDs and disruption of the gut "
            "flora by high-carbohydrate feed act as triggers."
        ),
        "pathophysiology_en": (
            "Severe colonic mucosal injury by a pathogen or toxin breaks down the intestinal "
            "barrier, and large amounts of endotoxin (LPS) and inflammatory mediators are absorbed. "
            "Within hours the systemic inflammatory response progresses to endotoxic shock "
            "(vasodilation, DIC, multi-organ failure), and massive fluid loss into the bowel lumen "
            "accelerates circulatory collapse."
        ),
        "clinical_signs_detail_en": (
            "Acute onset (minutes to hours): severe abdominal pain, collapse and depression; "
            "profuse watery diarrhoea (soon after onset); tachycardia >100; dark-red to purple "
            "mucous membranes; CRT >6 s; cold peripheral sweat; fever (40-41°C) or hypothermia "
            "(as shock progresses); and rapid deterioration in consciousness with inability to "
            "stand."
        ),
        "prevention_en": (
            "Stress management, judicious antibiotic use, avoidance of abrupt changes to "
            "high-carbohydrate feed, early treatment of underlying disease, and reduction of stress "
            "during competition and transport."
        ),
        "prognosis_en": (
            "Survival <20%; aggressive treatment within 24 hours of onset can improve this to "
            "30-40%. Once shock has progressed, or with concurrent laminitis, the prognosis is "
            "poor."
        ),
    },
    "rp_anestrus_ovarian_inactivity": {
        "etiology_en": (
            "(1) Seasonal anoestrus (winter, Dec-Feb in the northern hemisphere): shortening "
            "daylight raises pineal melatonin, weakening hypothalamic GnRH pulses, lowering FSH/LH "
            "and arresting follicular development; prolonged at latitudes above 35°N. "
            "(2) Prolonged spring transition (Mar-May): several medium follicles (20-35 mm) develop "
            "but fail to ovulate and repeatedly regress. (3) Persistent corpus luteum "
            "(pseudo-anoestrus): failure of luteolysis (deficient PGF2alpha, reduced endogenous PG "
            "from endometritis, or luteal maintenance after early embryonic loss) keeps P4 "
            ">4 ng/mL and suppresses GnRH. (4) Age-related ovarian failure (>20 years): depleted "
            "follicle pool, AMH <0.05 ng/mL, elevated FSH. (5) Nutritional anoestrus: BCS <4 "
            "(thin) or >8 (obese), rapid weight loss, Se/Cu/Zn deficiency, beta-carotene "
            "deficiency. (6) Endocrine: PPID (GnRH suppression by excess cortisol), hypothyroidism "
            "(rare, usually chronic non-thyroidal illness), adrenal dysfunction. (7) Pathological "
            "ovary: granulosa-cell tumour (suppresses the contralateral ovary), ovarian cyst, "
            "post-traumatic ovarian atrophy. (8) Chromosomal abnormality: 63,XO (Turner-like), X "
            "mosaicism, SRY-positive XY sex reversal — primary anoestrus in young mares with small "
            "ovaries (<2 cm) and very low AMH. (9) Silent (quiet) ovulation: ovulation occurs but "
            "behavioural oestrus is not observed (young, primiparous or suppressed mares). "
            "(10) Pseudo-anoestrus of ongoing pregnancy. (11) Chronic disease or heavy training "
            "stress."
        ),
        "pathophysiology_en": (
            "Physiological cycle: 21-22 days (5-7 days oestrus plus a 15-16-day luteal phase). "
            "Hypothalamic GnRH pulses drive pituitary FSH/LH, follicular growth, a rise in "
            "oestradiol, the LH surge, ovulation, corpus-luteum formation and P4 secretion; "
            "endometrial PGF2alpha at day 14-15 causes luteolysis. Anoestrus is a breakdown at one "
            "of these stages. Seasonal: melatonin suppresses GnRH KNDy neurons and follicular "
            "activity ceases — ovaries are small (2-3 cm), flat, follicles <10 mm, the uterus is "
            "atonic and the endometrium inactive. Persistent CL: functional P4 >4 ng/mL persists "
            "under GnRH suppression, with a large residual CL on ultrasound and suppressed new "
            "follicles. Senile failure: depleted primordial follicles, AMH <0.05 ng/mL, elevated "
            "FSH, loss of follicular responsiveness. GCT-associated: high tumour inhibin secretion "
            "(>0.7 ng/mL) suppresses FSH and atrophies the contralateral ovary; testosterone "
            ">50-100 pg/mL adds stallion-like behaviour. 63,XO: streak ovary, primary anoestrus, "
            "uterine hypoplasia, very low AMH. Nutritional: low leptin suppresses KNDy neurons and "
            "GnRH (the negative-energy-balance mechanism)."
        ),
        "clinical_signs_detail_en": (
            "(1) Absence of oestrous signs (>30-45 days): no tail-raising, squatting stance, "
            "mucoid vulvar discharge or winking (vulvar flicker). (2) Behavioural change: lack of "
            "response to the stallion, mild depression, a calmer temperament (normal in seasonal "
            "cases) or aggression/stallion-like behaviour (with a GCT). (3) Transrectal palpation: "
            "(a) seasonal — bilateral small flat ovaries (2-3 cm), atonic uterus; (b) persistent "
            "CL — a large CL (30-40 mm) palpable on one side; (c) senile — bilateral tiny ovaries "
            "(<2 cm); (d) GCT — marked unilateral enlargement (10-30 cm) with contralateral "
            "atrophy. (4) Transrectal ultrasound: (a) inactive ovary — only follicles <15 mm; "
            "(b) transitional — multiple medium follicles (20-35 mm); (c) persistent CL — a "
            "residual CL echotexture (35-40 mm); (d) GCT — a multicystic 'honeycomb' pattern; "
            "(e) uterus — absence of oestrous 'cartwheel' oedema. (5) Abnormal body condition "
            "(BCS <4 or >8). (6) Associated findings: PPID (hypertrichosis, laminitis, PU/PD), "
            "hypothyroidism (poor coat, cold intolerance), signs of chronic disease. "
            "(7) Chromosomal (63,XO) — small size, growth retardation, juvenile appearance."
        ),
        "prevention_en": (
            "(1) Breeding records: detailed records of oestrus, ovulation, insemination and "
            "pregnancy for early detection. (2) Pre-season preparation: start artificial long days "
            "(16 hours light) from December and maintain BCS 5-6/9 from 60-70 days pre-season. "
            "(3) Nutrition: Se 3 mg/day, Vit E 2,000 IU/day, Cu 100-150 mg/day, Zn 300-400 mg/day, "
            "beta-carotene 200-400 mg/day, good-quality protein (especially lactating and young "
            "mares). (4) Evaluate broodmares >15 years each pre-season by transrectal ultrasound, "
            "endometrial biopsy and culture, with AMH to assess ovarian reserve. (5) Prevent "
            "persistent CL: if the pregnancy check at 14-16 days post-cover is negative, promptly "
            "move to the next cycle with PGF2alpha (shortening empty cycles). (6) Early PPID "
            "screening (>15 years, ACTH measurement). (7) Investigate primary anoestrus in young "
            "mares by 3 years (karyotype, AMH, ultrasound). (8) Concentrate increases in transport "
            "and training load outside the breeding season. (9) A high-quality oestrus-detection "
            "system with an experienced teaser stallion."
        ),
        "prognosis_en": (
            "Highly cause-dependent. (1) Seasonal: artificial light plus progestin priming achieves "
            "planned ovulation in 90-95% with normal subsequent pregnancy rates. (2) Prolonged "
            "spring transition: 85-90% manageable with drug intervention. (3) Persistent CL: a "
            "single PGF2alpha dose is >95% effective. (4) Nutritional: 80-90% recover with improved "
            "BCS over 2-4 months. (5) Senile failure: spontaneous return of oestrus <10%; limited "
            "pregnancy via assisted reproduction. (6) 63,XO: zero fertility. (7) GCT: 80% can "
            "conceive 3-12 months after unilateral ovariectomy. (8) Concurrent PPID: 50-70% resume "
            "cycling after 6-12 months of pergolide therapy."
        ),
    },
    "rp_early_embryonic_death": {
        "etiology_en": (
            "Maternal factors (most common): (1) Older mares (2-3x EED rate at >15 years, 3-4x at "
            ">20) — oocyte ageing, increased aneuploidy, reduced oviductal function, mitochondrial "
            "decline. (2) Endometrosis (Kenney III/IV) — periglandular fibrosis, glandular cysts "
            "and angiopathy disrupting the intrauterine environment. (3) Chronic endometritis and "
            "biofilm formation (Pseudomonas, Klebsiella, E. coli, beta-haemolytic Streptococcus, "
            "fungi). (4) Persistent post-mating endometritis ('susceptible mare'): impaired uterine "
            "clearance, fluid accumulation and an embryo-hostile environment. (5) Luteal "
            "insufficiency: P4 <4 ng/mL (days 14-30), deficient secondary luteal formation. "
            "(6) Uterine capacity limits: twin pregnancy. (7) PPID / cortisol excess: embryotoxic "
            "and altered uterine environment. Embryonic factors: (8) chromosomal abnormality "
            "(aneuploidy, an estimated 30-40% of EED, especially >15 years); (9) developmental "
            "anomaly (absent heartbeat, persistent yolk sac, abnormal vesicle shape). Stallion / "
            "insemination factors: (10) high sperm DNA fragmentation (>20-25%); (11) semen "
            "infection (CEM, Pseudomonas, Klebsiella); (12) mismatch between ovulation timing and "
            "insemination. Infection: (13) EHV-1/4; (14) equine viral arteritis; (15) Leptospira "
            "(interrogans serovars Pomona, Bratislava). Environment/management: (16) heat stress "
            "(ambient >32°C); (17) transport stress (especially days 8-15); (18) extreme BCS or "
            "rapid weight loss; (19) toxins (fescue endophyte, phyto-oestrogen excess, ergot "
            "alkaloids); (20) late season (higher EED rate in Jul-Aug)."
        ),
        "pathophysiology_en": (
            "Normal development: fertilisation, oviductal descent over 3-4 days, entry to the "
            "uterus at days 5-6 (late morula to blastocyst), intrauterine mobility at days 11-15 "
            "(to signal maternal recognition and suppress PGF2alpha), fixation at day 16, heartbeat "
            "at day 21 (85-100 bpm), and endometrial-cup formation with eCG secretion and secondary "
            "CL formation at days 40-45. Maternal recognition of pregnancy: an embryo-derived signal "
            "(putative conceptus oestradiol plus PGE2 and mobility) suppresses PGF2alpha, maintains "
            "the CL and sustains P4. Impaired embryo mobility or an insufficient signal fails to "
            "suppress PGF2alpha, causing luteolysis, falling P4 and EED. Main mechanisms of EED: "
            "(1) failed maternal recognition (early, days 14-16); (2) luteal insufficiency "
            "(abnormal endogenous PGF2alpha from inflammation/infection, or deficient secondary CL, "
            "especially days 40-100); (3) an abnormal uterine environment (endometrosis with "
            "glandular hypofunction, hypoxia, poor nutrient supply); (4) direct embryotoxicity "
            "(infection, toxins, heat stress); (5) intrinsic embryonic abnormality (developmental "
            "arrest from chromosomal defects)."
        ),
        "clinical_signs_detail_en": (
            "(1) Often asymptomatic (especially early EED at days 14-25, found on routine "
            "ultrasound). (2) Early warning signs (24-72 h before loss): abnormal vesicle "
            "echogenicity, irregular vesicle shape, absent heartbeat or bradycardia after day 25 "
            "(<80 bpm; normal 100-120 bpm at day 25), a small embryo (<10 mm at day 25, <14 mm at "
            "day 30), a persistent yolk sac after day 35, a vesicle diameter lagging gestational "
            "age (>3-5 days behind), intrauterine free fluid and abnormal endometrial oedema "
            "('cartwheel' appearance). (3) Early return to oestrus: a short cycle at days 14-25, "
            "irregular oestrus at days 25-40, or — after endometrial-cup formation past day 40 — "
            "persistent eCG causing an anovulatory pseudo-pregnancy with prolonged anoestrus "
            "(60-120 days), an important management distinction. (4) A mild mucoid (not "
            "haemorrhagic) vulvar discharge, days 14-30. (5) P4: falls to <2 ng/mL within 72 h of "
            "EED (may not fall past day 40 while a secondary CL is maintained). (6) The mare is "
            "usually asymptomatic, but infectious EED (leptospirosis, EHV) may bring fever, malaise "
            "and systemic signs."
        ),
        "prevention_en": (
            "Pre-breeding: (1) a comprehensive breeding examination at least annually (twice for "
            ">15 years) — endometrial biopsy, culture, cytology, ultrasound, AMH. (2) With Kenney "
            "III/IV, consider using the mare as an embryo-transfer donor and counsel that carrying "
            "her own pregnancy is guarded. (3) Caslick assessment and repair. (4) Stallion fertility "
            "assessment (DNA fragmentation, past pregnancy rates). (5) Infectious-disease "
            "vaccination: EHV-1 (at 5, 7 and 9 months of gestation), EVA (before covering shedders), "
            "rotavirus (at 8, 9 and 10 months). At covering: (6) identify the ovulatory period "
            "(ultrasound plus hormones) and inseminate 24-48 h before ovulation (frozen semen within "
            "6 h after ovulation). (7) Induce ovulation (deslorelin 1.5 mg IM or hCG 2,500 IU IV) to "
            "improve timing. (8) Post-mating lavage and oxytocin in susceptible mares. Early "
            "pregnancy (days 0-45): (9) altrenogest 0.044 mg/kg PO SID for a history of EED or "
            "luteal insufficiency (days 5-120). (10) Twin check at days 14-16 — manually crush a "
            "unilateral fixation (>90% success). (11) Avoid transport, hard exercise and heat "
            "(especially days 8-21), and keep the stall below 25°C with fans. (12) Nutrition: BCS "
            "5-6/9, Se 3 mg / Vit E 2,000 IU / Cu 100 mg / Zn 300 mg per day, omega-3 50 mg/kg PO "
            "SID. (13) Ultrasound schedule at days 14-16, 25-30 and 40-45. (14) Early PPID "
            "screening and treatment. (15) Manage infectious exposure (21-day quarantine of new "
            "arrivals, avoid covering shedder stallions, leptospira vector control). Consider "
            "switching to assisted reproduction from the third cycle in recurrent cases."
        ),
        "prognosis_en": (
            "Single EED: the pregnancy rate on the next cycle is usually normal (50-65% per cycle). "
            "Recurrent EED (two consecutive): next-pregnancy maintenance 40-50%, improvable by "
            "identifying and treating the cause. Three or more consecutive: 20-30% per cycle, "
            "improvable to 30-50% with embryo transfer or ICSI. Older mares (>20 years) with "
            "endometrosis III: 15-25% per cycle. A double pregnancy reduced to a single: next EED "
            "risk 10-15% (normal range). After endometrial-cup formation and loss, no pregnancy is "
            "possible until the next season (pseudo-pregnancy 60-120 days). Infectious causes "
            "(after treatment): next-pregnancy maintenance 70-85% with control of the underlying "
            "disease."
        ),
    },
    "rp_pregnancy_luteal_insufficiency": {
        "etiology_en": (
            "Primary CL (days 0-40) abnormality: (1) early luteolysis of the primary CL from "
            "endogenous PGF2alpha of endometritis/post-mating endometritis; (2) poor ovarian "
            "responsiveness (age, malnutrition). Deficient accessory-CL (days 40-100) formation: "
            "(3) endometrial-cup dysfunction with insufficient eCG (<20 IU/mL at days 60-80), so no "
            "new follicles / ovulation / accessory CL form and P4 drops at days 40-100; (4) PPID / "
            "high cortisol suppressing the hypothalamic-pituitary axis. Placental progestogen "
            "insufficiency (from day 100): (5) ascending placentitis (Streptococcus equi "
            "zooepidemicus 60-70%, E. coli, Leptospira, Nocardioform actinomycetes, fungi) reducing "
            "placental function and progestogen synthesis; (6) focal nocardioform placentitis; "
            "(7) placental hypoplasia (small placenta, ET-derived or inbred foals); (8) unreduced "
            "twins competing for placental capacity; (9) fetal stress (IUGR, hypoxia) disturbing "
            "the fetal adrenal-placental axis. Maternal endocrine/systemic factors: (10) PPID; "
            "(11) thyroid dysfunction; (12) marked obesity (BCS >8) with excess inflammatory "
            "cytokines. Toxic/nutritional: (13) fescue toxicosis (Festuca arundinacea with "
            "Neotyphodium coenophialum producing ergovaline) causing prolactin suppression, "
            "agalactia, prolonged gestation, placental thickening and weak neonates; (14) ergot "
            "contamination of grain; (15) dietary phyto-oestrogens. Stress: (16) transport, abrupt "
            "temperature change, group changes; (17) heavy exercise. Infection: (18) EHV-1 "
            "(neuropathogenic strain); (19) EVA; (20) Leptospira spp. (especially Pomona, "
            "Bratislava, Hardjo, Grippotyphosa)."
        ),
        "pathophysiology_en": (
            "The progestogen source shifts over gestation: (a) days 0-40 the primary CL is the sole "
            "P4 source (P4 6-15 ng/mL); (b) days 40-100 eCG (equine chorionic gonadotropin) from "
            "the endometrial cups (formed days 36-38, unique to the horse) induces new ovulations "
            "and luteinisation, forming 5-15 accessory (secondary) CLs, so primary plus accessory "
            "CLs coexist and P4 peaks at 8-25 ng/mL (days 80-90); (c) days 100-150 the cups regress "
            "(gone by days 120-180), ovarian P4 falls, and the placenta begins synthesising "
            "5-alpha-pregnanes — the transition window after which pregnancy can be maintained even "
            "after ovariectomy; (d) from day 150 the placenta is the sole progestogen source, and "
            "total progestogens (HPLC) cross-react on P4 immunoassay (true P4 may be <1 ng/mL while "
            "total >5 ng/mL maintains pregnancy); (e) from day 300 progestogens rise, surging in "
            "the 72 hours before foaling (the fetal cortisol surge triggering parturition), then "
            "falling sharply after birth. Pathology: progestogen deficiency de-represses "
            "endometrial PGF2alpha, increasing myometrial contraction and cervical softening and "
            "causing abortion or premature birth. In placentitis, inflammatory cytokines (IL-1beta, "
            "IL-6, TNF-alpha, PGE2) directly suppress placental progestogen synthesis after a "
            "paradoxical early rise. In fescue toxicosis ergovaline agonises D2 dopamine receptors, "
            "suppressing prolactin and relaxin and causing agalactia, prolonged gestation (>360 "
            "days), placental thickening and retained placenta. Clinical thresholds: minimum P4 for "
            "maintenance (days 14-100) >2 ng/mL (safe margin >4); total progestogens (days 100-300) "
            ">4 ng/mL (safe margin >6)."
        ),
        "clinical_signs_detail_en": (
            "(1) Often asymptomatic early (found on routine examination). (2) Threatened-abortion "
            "signs: vulvar discharge (mucoid/purulent/bloody), abnormally early vulvar relaxation "
            "(>30 days early), slackening of the hindquarter muscles. (3) Premature mammary "
            "development / lactation: typical of placentitis, with udder enlargement, teat waxing "
            "and pre-foaling milk before day 300; abrupt changes in milk electrolytes (Ca, Mg, K, "
            "Na) signal foaling within 48 hours. (4) Transrectal ultrasound: an accessory-CL count "
            "<5 (days 60-80) and size <3 cm with reduced blood flow; a fetal heart rate <60 or "
            ">120 bpm (abnormal); and CTUP (combined utero-placental thickness cranial to the "
            "cervical star) — normal <8 mm at 271-300 days, >10 mm mild inflammation, >15 mm severe "
            "placentitis — plus placental detachment or hypoechoic areas. (5) Prolonged gestation "
            "(>340-360 days, typical of fescue toxicosis). (6) Agalactia (fescue toxicosis): no "
            "udder development or colostrum even at term. (7) Maternal condition: mild fever "
            "(38.5-39.5°C), malaise and inappetence with placentitis or systemic infection. "
            "(8) Leptospiral abortion is asymptomatic with sudden loss (days 170-310). (9) EHV-1 "
            "abortion peaks after day 300 with sudden clustered losses (abortion storm)."
        ),
        "prevention_en": (
            "Pre-breeding: (1) endometrial biopsy (Kenney), culture, cytology, ultrasound and AMH "
            "each season for mares >15 years or with a history of abortion. (2) Caslick assessment "
            "and repair (prevents pneumovagina and ascending placentitis). (3) Assess stallion "
            "fertility and infection history. (4) PPID screening (>15 years: baseline autumn ACTH, "
            "TRH-stimulation test) and start pergolide. (5) Thyroid evaluation in suspect cases. "
            "(6) Maintain BCS 5-6/9, Se 3 mg/day, Vit E 2,000-5,000 IU/day, Cu 100 mg/day, Zn "
            "300 mg/day, omega-3 50 mg/kg/day. Covering / early pregnancy: (7) precise ovulation "
            "timing (deslorelin 1.5 mg IM or hCG 2,500 IU IV trigger). (8) Manage post-mating "
            "endometritis in susceptible mares (lavage plus oxytocin 4-8 h post-breeding). "
            "(9) Twin reduction at days 14-16. (10) For a history of luteal insufficiency or EED, "
            "start altrenogest 0.044-0.088 mg/kg PO SID from days 2-5 after ovulation. Mid "
            "gestation: (11) ultrasound screening at days 14-16, 25-30, 40-45 and 60 (CL count, "
            "accessory CL, fetal heartbeat). (12) Continue altrenogest in high-risk cases or "
            "reassess at day 120. (13) Restrict transport and hard exercise from days 40-100. Late "
            "gestation (from day 270): (14) transrectal ultrasound every 14 days measuring CTUP "
            "(normal <8 mm at 271-300, <10 mm at 331-360, <12 mm at 361+; higher warns of "
            "placentitis). (15) Daily vulvar and udder checks with 24-hour monitoring for early "
            "mammary development, milk leakage or vulvar discharge. (16) Pre-foaling electrolyte "
            "monitoring (Ca, Mg) to predict foaling 48-72 h ahead. (17) Switch completely to "
            "endophyte-free fescue pasture 90 days before foaling. (18) EHV-1 vaccine (killed "
            "Pneumabort-K or Prodigy) at 5, 7 and 9 months plus herd biosecurity. (19) EVA vaccine "
            "before covering as indicated. (20) Leptospira vaccine in endemic regions. (21) Rotavirus "
            "vaccine at 8, 9 and 10 months. (22) Maintain the Caslick stitch until day 320 and "
            "remove 7-14 days before foaling."
        ),
        "prognosis_en": (
            "(1) Single previous luteal insufficiency with early altrenogest from days 2-5 of the "
            "next pregnancy: maintenance 75-85%. (2) Recurrent (>=2 consecutive abortions): 50-70% "
            "with comprehensive work-up and aggressive treatment. (3) Ascending placentitis with "
            "early diagnosis plus trimethoprim-sulfa, altrenogest and pentoxifylline: live foal "
            "60-80% when started early (CTUP <15 mm), falling to 30-50% with delayed diagnosis "
            "(CTUP >20 mm). (4) Nocardioform placentitis: hard to diagnose (body-pole location), "
            "abortion rate 60-80% and survivors often IUGR. (5) Fescue toxicosis: 80-90% foal and "
            "lactate normally if endophyte exposure is removed 90 days before foaling and "
            "domperidone is given; without intervention, maternal and foal mortality is high. "
            "(6) EHV-1 abortion: clustered losses (abortion storm), with vaccination and isolation "
            "the mainstay of prevention. (7) Leptospiral abortion: many mares carry a subsequent "
            "pregnancy after oxytetracycline, and vaccination reduces risk. (8) Concurrent PPID: "
            "maintenance 70-85% under pergolide control, 40-60% if poorly controlled. (9) Unreduced "
            "twins: natural-delivery survival <10%."
        ),
    },
    "dg_gastric_impaction": {
        "etiology_en": (
            "The cause is polymerisation, in the acidic gastric environment, of soluble tannins "
            "(shibuol) contained in persimmon skin, seeds and unripe fruit; these bind dietary "
            "fibre and gastric contents to form a hard concretion (phytobezoar). Autumn (Sep-Dec) "
            "pasture access to persimmon trees and ingestion of windfall fruit, and large intake "
            "while fasting or dehydrated, are the triggers."
        ),
        "pathophysiology_en": (
            "Tannins aggregate protein and fibre in the stomach, and over time a large, dehydrated, "
            "hardened phytobezoar occupies the gastric lumen and obstructs outflow. Compression and "
            "stretching of the gastric wall cause colic, and chronicity carries a risk of gastric "
            "ulceration and perforation. It resists medical dissolution and often requires "
            "laparotomy for removal."
        ),
        "clinical_signs_detail_en": (
            "Onset days to weeks after eating persimmon fruit; persistent inappetence; chronic "
            "colic; large, sustained reflux on nasogastric intubation (characteristically "
            "brown-green and foul-smelling); abdominal distension; weight loss; dehydration; "
            "tachycardia; vomiting-like salivation in advanced cases; and acute deterioration with "
            "gastric rupture."
        ),
        "prevention_en": (
            "Remove persimmon trees from pastures, collect windfall fruit daily, restrict grazing "
            "during persimmon season, secure alternative pasture, and educate owners to seek early "
            "veterinary attention within 48 hours of persimmon ingestion."
        ),
        "prognosis_en": (
            "50-70% survive with early diagnosis and laparotomy. Successful conservative treatment "
            "is <30%. Gastric rupture carries a fatality rate >95%. Post-operative management "
            "determines the long-term outcome."
        ),
    },
    "dg_gastric_squamous_ulcer": {
        "etiology_en": (
            "An advanced, severe form of long-untreated, recurrent ESGD. Chronic acid exposure "
            "under continued training, combined use of multiple NSAIDs, concurrent systemic disease "
            "(sepsis, severe inflammation) and a poor treatment response from inappropriate "
            "omeprazole use (post-prandial dosing, low dose) form the background."
        ),
        "pathophysiology_en": (
            "Sustained acid injury progresses squamous lesions from large multiple ulcers (ECEIM "
            "grade 3) to deep ulcers with active bleeding (grade 4). Chronic blood loss causes "
            "anaemia and hypoproteinaemia, and reduced intake from pain causes weight loss and "
            "reduced performance; deep ulcers carry a risk of gastric perforation and septic "
            "peritonitis."
        ),
        "clinical_signs_detail_en": (
            "Marked weight loss (>5%), a poor lustreless coat, markedly reduced performance from "
            "chronic anaemia, easy fatigue, pale mucous membranes, chronic recurrent colic, markedly "
            "reduced appetite (especially grain refusal), persistent bruxism, occasionally "
            "haematemesis or melaena (with progressive bleeding), a mildly raised heart rate, and — "
            "in racehorses — a marked decline in performance. Unlike mild ESGD, signs often persist "
            "after standard treatment."
        ),
        "prevention_en": (
            "Early detection of ESGD (6-monthly endoscopic screening of high-risk horses), "
            "appropriate treatment at grade 1-2, cautious NSAID use with concurrent gastroprotectants, "
            "prophylactic dosing during stress events (omeprazole 1-2 mg/kg PO SID during "
            "competition), and continued appropriate husbandry."
        ),
        "prognosis_en": (
            "With appropriate high-dose, prolonged treatment 60-80% improve over 8-12 weeks. The "
            "recurrence rate is higher than grade 1-2 (>50%). Perforated cases carry a fatality "
            "rate >90%. Complete rest during treatment greatly improves the prognosis in racehorses."
        ),
    },
    "dg_gastric_glandular_ulcer": {
        "etiology_en": (
            "A focal severe form of EGGD, characterised by a deep ulcer and scarring localised to "
            "the pylorus. A history of untreated or inadequately treated EGGD, long-term NSAID use "
            "and chronic stress form the background, and a predisposition is suggested in Warmbloods "
            "and Thoroughbreds."
        ),
        "pathophysiology_en": (
            "Deep ulceration from breakdown of pyloric mucosal defence forms fibrous scarring and "
            "wall thickening during healing, narrowing the gastric outflow. Delayed gastric "
            "emptying causes post-prandial colic and weight loss; it resists standard EGGD "
            "treatment, and progressive stenosis requires pyloroplasty."
        ),
        "clinical_signs_detail_en": (
            "Chronic mild-to-moderate colic (30 min-2 h after eating, recurrent), reduced appetite "
            "(especially grain and hay), increased water intake, weight loss, small-volume reflux "
            "on nasogastric intubation, gastric distension and persistent reflux in severe cases, "
            "temperament change (increased sensitivity or aggression), reduced performance, "
            "girth/saddle sensitivity and bruxism. Chronic course with gradual worsening."
        ),
        "prevention_en": (
            "Early diagnosis and complete appropriate treatment of EGGD, cautious NSAID use "
            "(preferring COX-2 selective), stress management, an evened-out exercise schedule, one "
            "full rest day a week, and continued maintenance therapy in chronically affected horses."
        ),
        "prognosis_en": (
            "50-70% improve with early medical therapy. Cases with progressive pyloric stenosis "
            "carry a poor prognosis. Long-term outcome after surgery is 60-80% (facility-dependent). "
            "Complete healing may take 6-12 months."
        ),
    },
    "dg_right_dorsal_colitis_nsaid": {
        "etiology_en": (
            "The cause is COX-1 inhibition from overdose, prolonged use, dehydrated administration "
            "or combined use of NSAIDs (especially phenylbutazone and flunixin). Reduced "
            "prostaglandin-dependent gastric and duodenal mucosal defence underlies it, and older "
            "horses, pre-existing ulcers, renal impairment, hypoalbuminaemia and dosing while "
            "fasted are aggravating factors."
        ),
        "pathophysiology_en": (
            "Deficiency of COX-1-derived prostaglandins (PGE2, PGI2) impairs mucus-bicarbonate "
            "secretion, mucosal blood flow and epithelial repair, producing ulcers in the glandular "
            "region, pylorus and duodenum (a different mechanism from acid-induced ESGD). Deep "
            "ulcers cause bleeding, perforation and duodenal stricture, and the same COX-1 "
            "mechanism can produce concurrent right dorsal colitis."
        ),
        "clinical_signs_detail_en": (
            "Chronic recurrent colic (especially after eating), inappetence (grain avoidance), "
            "weight loss, ventral oedema (hypoalbuminaemia), diarrhoea or soft faeces (duodenal/colonic "
            "involvement), reflux on nasogastric intubation (impaired emptying), bruxism, flehmen, "
            "chronic anaemia (GI bleeding), epistaxis (rare, with severe platelet dysfunction) and "
            "reduced performance. A history of NSAID use (a week or more) is the clue."
        ),
        "prevention_en": (
            "Lowest NSAID dose for the shortest time (phenylbutazone <4.4 mg/kg SID for a maximum "
            "of 5 days), prefer a COX-2 selective NSAID (firocoxib 0.1 mg/kg PO SID), combine "
            "gastroprotectants with prolonged dosing, avoid dosing during dehydration, monitor "
            "renal function regularly, and use alternative analgesia (acupuncture, physiotherapy)."
        ),
        "prognosis_en": (
            "With immediate NSAID discontinuation and appropriate treatment 60-80% improve over "
            "4-6 weeks. Severe GI bleeding or deep ulcers take more than 3 months. Cases with "
            "concurrent renal impairment and chronic cases carry a poor prognosis. Prevention of "
            "recurrence requires permanent NSAID avoidance or COX-2 selective use."
        ),
    },
    "fl_gastric_ulcer_foal": {
        "etiology_en": (
            "Foals begin secreting gastric acid from day 2 of life while their mucosal defence is "
            "still immature, so they readily develop ulcers. Serious illness (neonatal sepsis, "
            "pneumonia, diarrhoea), stress from hospitalisation and mare-foal separation, NSAIDs, "
            "shock/hypotension and insufficient nursing or fasting are the main causes."
        ),
        "pathophysiology_en": (
            "Reduced mucosal blood flow from stress or hypoperfusion, together with acid exposure, "
            "forms ulcers in the squamous region, glandular region and duodenum. The clinical "
            "picture ranges across four forms — from asymptomatic (silent), through colic and "
            "drooling (impaired gastric emptying from duodenal ulcers), perforation and peritonitis, "
            "to gastro-oesophageal reflux from duodenal stricture. Duodenal stricture is a sequela "
            "of scar healing."
        ),
        "clinical_signs_detail_en": (
            "Bruxism (most characteristic), drooling and salivary frothing, a dorsal-recumbent "
            "posture (lying on the back — a behaviour that eases the pain of acid reflux), reduced "
            "nursing volume and desire, depression, diarrhoea (duodenal involvement), mild colic "
            "(worse after eating), poor weight gain, epistaxis or haematemesis (severe bleeding) "
            "and acute deterioration with signs of peritonitis (perforation). Signs vary with age "
            "and the underlying disease."
        ),
        "prevention_en": (
            "Prophylactic acid-suppression in critically ill/NICU foals, cautious NSAID use "
            "(preferring firocoxib), maintaining adequate nursing volume (minute-by-minute "
            "monitoring), stress reduction (maintaining mare-foal contact), ensuring adequate "
            "colostrum intake (IgG >800 mg/dL), avoiding unnecessary nasogastric intubation, and "
            "early treatment of the underlying disease."
        ),
        "prognosis_en": (
            "Silent and symptomatic forms heal in >90% with appropriate treatment. The perforated "
            "form carries a poor prognosis (<30% survival). The duodenal-stricture form has 50-70% "
            "survival with surgery but requires chronic management. Prophylactic dosing "
            "significantly lowers the incidence in hospitalised NICU foals."
        ),
    },
    "metabolic_atypical_myopathy": {
        "etiology_en": (
            "Caused by ingestion of hypoglycin A (HGA, a non-protein amino acid) contained in the "
            "seeds, seedlings and young leaves of sycamore maple (Acer pseudoplatanus, Europe and "
            "eastern North America) or box elder (Acer negundo, North America). HGA is metabolised "
            "in vivo to methylenecyclopropylacetic acid (MCPA), whose MCPA-CoA ester inhibits "
            "acyl-CoA dehydrogenases (especially isovaleryl-CoA and short-chain dehydrogenases), "
            "blocking fatty-acid beta-oxidation, causing mitochondrial dysfunction and acute "
            "necrosis of skeletal, cardiac and respiratory muscle. Onset clusters in autumn (seed "
            "dispersal) and spring (seedling growth). It is distinct from red maple (Acer rubrum) "
            "toxicosis, which causes haemolytic anaemia and contains no HGA."
        ),
        "pathophysiology_en": (
            "HGA ingestion, hepatic and renal metabolism to MCPA, MCPA-CoA formation, inhibition of "
            "acyl-CoA dehydrogenases, blockade of fatty-acid beta-oxidation, accumulation of "
            "acylcarnitines (C5, C5-OH, C8-DC), reduced mitochondrial energy production and ATP "
            "deficiency. Necrosis is most marked in the highest-demand slow-twitch oxidative fibres "
            "(postural, cardiac and respiratory muscle). Rhabdomyolysis causes myoglobinuria and "
            "acute kidney injury; cardiac necrosis causes arrhythmia and heart failure; respiratory "
            "necrosis causes ventilatory failure. Histology: diffuse necrosis of type I (oxidative) "
            "muscle fibres, vacuolar degeneration and lipid accumulation."
        ),
        "clinical_signs_detail_en": (
            "(1) Sudden severe muscle weakness, stumbling and recumbency (appetite often preserved, "
            "sensation normal); (2) dark red-brown to almost black urine (myoglobinuria); "
            "(3) tachycardia (>60 bpm), arrhythmia, abnormal heart sounds; (4) sweating and "
            "trembling; (5) dyspnoea (respiratory-muscle involvement); (6) sometimes concurrent "
            "laminitis; (7) temperature normal to mildly low; (8) an expression of distress; "
            "(9) progressive deterioration and death often within 24-72 hours. Differentials: "
            "PSSM, RER, botulism, tetanus, neurological disease. Acute muscle weakness with "
            "myoglobinuria after autumn or spring grazing should raise this as the prime suspicion."
        ),
        "prevention_en": (
            "(1) Remove sycamore maple and box elder from pastures, or fence them off at least 100 m "
            "away. (2) Monitor pastures in autumn (Oct-Dec) and spring (Mar-May) — do not use "
            "pastures littered with seeds, seedlings or young leaves. (3) Provide ample hay and "
            "feed (avoid a starvation state). (4) Optimise grazing density. (5) Educate on tree "
            "identification (leaf shape: sycamore five symmetrical lobes; seeds: paired samaras at "
            "~90°). (6) Susceptibility genetic testing is not established. (7) In outbreak areas, "
            "stop grazing during the spring and autumn seasons. (8) Serum CK/AST pre-screening can "
            "assess exposure by abnormal values."
        ),
        "prognosis_en": (
            "Grave — mortality 70-90%; survivors require 4-12 weeks of intensive care and often "
            "retain permanent muscle and myocardial damage. Favourable indicators: early "
            "presentation (within 24 hours), remaining able to walk, CK <200,000 U/L, normal "
            "respiration and heart rate, and early improvement in plasma acylcarnitines. Fatal "
            "factors: respiratory-muscle paralysis, myocardial injury (fatal arrhythmia), "
            "progressive AKI, recumbency beyond 48 hours, and CK >500,000 U/L."
        ),
    },
}
