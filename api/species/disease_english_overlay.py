"""English clinical narrative for Japanese-first dict-based disease records.

A handful of records in the fish, dog and exotic-mammal modules were authored
with their English narrative field copied verbatim from the Japanese text, so an
English viewer saw Japanese in the causes / pathophysiology / prevention /
prognosis sections of the disease browser.

This module holds faithful English translations of that already-curated Japanese
narrative (non-dosing fields only) keyed by ``(species, disease name)``.
``apply_english_overlay`` writes each translation onto the plain-dict record's
English field only when that field currently contains Japanese characters, so a
record that already has real English is never overwritten and the pass is
idempotent. The Japanese ``*_ja`` companion field is left untouched.
"""

from __future__ import annotations

import re

_CJK = re.compile(r"[぀-ヿ一-鿿]")


def _has_cjk(value) -> bool:
    return bool(value) and bool(_CJK.search(str(value)))


# (species, name) -> {field: english_text}
DISEASE_ENGLISH: dict[tuple[str, str], dict[str, str]] = {
    # ---------------------------------------------------------------- fish
    ("fish", "Ichthyophthirius (White Spot Disease / Ich)"): {
        "prevention": (
            "Quarantine new fish for at least 2 weeks, avoid temperature swings and overcrowding, "
            "maintain good water quality, and treat at the first white spots. The parasite is only "
            "vulnerable in its free-swimming theront stage, so treatment must be sustained across "
            "the life cycle."
        ),
        "prognosis": (
            "Good with early treatment. Heavy gill infestation or secondary bacterial infection "
            "significantly worsens the outlook."
        ),
    },
    ("fish", "Columnaris Disease"): {
        "prevention": (
            "Rigorous water-quality management, avoidance of overcrowding, stress reduction and "
            "prevention of skin injury."
        ),
    },
    ("fish", "Aeromonas / Motile Aeromonad Septicemia"): {
        "prevention": (
            "Water-quality management, appropriate stocking density, good nutrition and stress "
            "reduction; promptly isolate and treat injured fish."
        ),
    },
    ("fish", "Saprolegnia (Water Mold / Cotton Wool Disease)"): {
        "prevention": (
            "Prevent injury, manage water quality, maintain an appropriate temperature and avoid overcrowding."
        ),
    },
    ("fish", "Velvet Disease (Oodinium / Piscinoodinium)"): {
        "prevention": (
            "Quarantine new fish (2+ weeks), give a freshwater dip on introduction (marine fish), "
            "manage water quality and reduce stress."
        ),
    },
    ("fish", "Swim Bladder Disorder"): {
        "prevention": (
            "Use sinking food, feed appropriate amounts and manage water temperature. Fancy "
            "goldfish are structurally predisposed, so prevention has its limits."
        ),
    },
    ("fish", "Dropsy (Pinecone Disease)"): {
        "prevention": (
            "Appropriate water-quality management, stress reduction and appropriate stocking "
            "density. Early intervention at the first signs (mild abdominal swelling) is important."
        ),
        "prognosis": (
            "Generally poor. Early mild cases may recover, but severe scale protrusion "
            "(pineconing) and ascites are difficult to treat."
        ),
    },
    ("fish", "Anchor Worm (Lernaea)"): {
        "prevention": (
            "Quarantine newly introduced fish, treat live food, monitor ponds regularly, and detect "
            "and remove infected fish early."
        ),
    },
    ("fish", "Fish Lice (Argulus)"): {
        "prevention": (
            "Quarantine new fish, prevent wild fish from entering the pond, and carry out regular visual inspection."
        ),
    },
    ("fish", "Gill Flukes (Dactylogyrus)"): {
        "prevention": (
            "Quarantine new fish, maintain good water quality, avoid overcrowding, and give "
            "prophylactic praziquantel during quarantine."
        ),
    },
    ("fish", "Skin Flukes (Gyrodactylus)"): {
        "prevention": (
            "Quarantine new fish (a praziquantel bath is recommended), avoid overcrowding and manage water quality."
        ),
    },
    ("fish", "Hole-in-the-Head Disease (HITH / HLLE)"): {
        "prevention": (
            "A nutrient-rich, varied diet (vitamin- and mineral-enriched), regular water changes, "
            "and avoidance of prolonged activated-carbon use."
        ),
    },
    ("fish", "Hexamita / Spironucleus (Internal Flagellates)"): {
        "prevention": (
            "A balanced, nutrient-rich diet, avoidance of overcrowding, regular water changes and "
            "quarantine of new fish."
        ),
    },
    ("fish", "Mycobacteriosis (Fish Tuberculosis)"): {
        "prevention": (
            "Quarantine and observe new fish, promptly remove dead fish, and disinfect equipment. "
            "Avoid bare-handed work in a suspect tank (wear gloves) — this is a zoonotic organism."
        ),
        "prognosis": "Poor. It is chronic and progressive, and cure is difficult.",
    },
    ("fish", "Ammonia Poisoning"): {
        "prevention": (
            "Proper tank cycling, avoidance of overcrowding, adequate filtration and regular water testing."
        ),
    },
    ("fish", "Nitrite Poisoning (Brown Blood Disease)"): {
        "prevention": (
            "Proper tank cycling, regular water testing (especially NO2-), avoidance of "
            "overcrowding, and adequate biological filtration."
        ),
    },
    ("fish", "pH Shock"): {
        "prevention": (
            "Match pH when changing water, fit a safety device (solenoid valve) on CO2 systems, and "
            "monitor pH regularly with a meter."
        ),
    },
    ("fish", "Costia (Ichthyobodo)"): {
        "prevention": (
            "Water-quality management, stress reduction, avoidance of overcrowding, and quarantine of new fish."
        ),
    },
    ("fish", "Trichodina"): {
        "prevention": (
            "Appropriate water-quality management (especially ammonia and nitrite), avoidance of "
            "overcrowding and regular water changes."
        ),
    },
    ("fish", "Lymphocystis"): {
        "prevention": "Quarantine and observe new fish, reduce stress and prevent injury.",
    },
    ("fish", "Koi Herpesvirus Disease (KHV / CyHV-3)"): {
        "prevention": (
            "Strict quarantine of new koi (3-4 weeks at 18-25°C), isolation of the water system and "
            "disinfection of equipment. Vaccines are available in some countries but carry a "
            "carrier risk."
        ),
        "prognosis": "Extremely poor. Survivors become carriers and a source of infection.",
    },
    ("fish", "Spring Viremia of Carp (SVC)"): {
        "prevention": (
            "Quarantine imported fish, avoid new introductions in the 10-17°C temperature range, "
            "and control external parasites (to prevent transmission)."
        ),
    },
    ("fish", "Neon Tetra Disease (Pleistophora)"): {
        "prevention": (
            "Promptly remove dead fish (to prevent transmission by cannibalism), quarantine and "
            "observe new tetras, and isolate equipment from infected tanks."
        ),
        "prognosis": "Poor. Cure is not expected.",
    },
    ("fish", "Egg Binding (Dystocia)"): {
        "prevention": (
            "Keep an appropriate sex ratio, provide a suitable spawning temperature and substrate, "
            "and feed a balanced diet."
        ),
    },
    ("fish", "Marine Ich (Cryptocaryon irritans)"): {
        "prevention": (
            "Strict quarantine of all new fish (4-6 weeks) and pre-introduction copper treatment or "
            "hyposalinity. In reef tanks, isolate invertebrates for at least 72 hours as well."
        ),
    },
    # ---------------------------------------------------------------- dog
    ("dog", "Fading Puppy Syndrome"): {
        "causes": (
            "Infectious: canine herpesvirus type 1 (CHV-1, causing acute systemic infection in a "
            "cold environment with a near-100% fatality rate), E. coli and Streptococcus "
            "(umbilical infection and sepsis), Campylobacter and Salmonella (enteritis), "
            "Cryptosporidium, Giardia. Non-infectious: low birth weight (LBW) and VLBW, "
            "hypothermia, hypoglycaemia, dehydration, congenital anomalies (cleft palate, cardiac "
            "malformation, hypospadias), inadequate colostrum intake (failure of maternal antibody "
            "transfer), maternal agalactia and mastitis, large litters (competition for milk per "
            "puppy) and maternal rejection. Maternal risk factors: post-partum eclampsia, "
            "dystocia, post-caesarean exhaustion and drug-induced sedation."
        ),
        "pathophysiology": (
            "Neonatal puppies have immature thermoregulation; rectal temperature at birth is "
            "35-37°C, approaching adult temperature (38-39°C) by 3-4 weeks as they mature. In "
            "hypothermia (<34°C) intestinal peristalsis stops, so nursed milk ferments in the "
            "stomach and cannot be digested, compounding dehydration and hypoglycaemia. Main "
            "cascade: (1) hypothermia leads to intestinal ileus, inability to suckle, "
            "hypoglycaemia and CNS depression; (2) hypoglycaemia (BG <50 mg/dL) alone can cause "
            "disease (especially LBW puppies and large litters); (3) infection (CHV-1, E. coli, "
            "Streptococcus, Campylobacter, Cryptosporidium, etc.) progresses to intestinal injury "
            "and sepsis; (4) congenital anatomical anomalies (cleft palate, cardiac malformation, "
            "inguinal hernia) cause inability to suckle, aspiration and undernutrition; "
            "(5) maternal factors (agalactia from mastitis, poor maternal behaviour, inadequate "
            "colostrum intake with failure of passive immunity) synergistically raise the risk."
        ),
        "prevention": (
            "Pre-breeding: infection screening (CHV-1 titre, Brucella, roundworm/hookworm "
            "deworming), BCS optimisation, and a complete breeding diet (25-30% protein) from "
            "before mating through the end of lactation. Foaling environment: keep the whelping box "
            "clean (change bedding every 6-12 h) and manage temperature (neonatal ambient 32-34°C "
            "in the first week, then lowering 1-2°C per week to 25°C at 4 weeks). Colostrum "
            "management: confirm colostrum intake within 1-2 hours of birth; if the dam is "
            "agalactic, consider a canine immunoglobulin product or a colostrum substitute "
            "(commercial colostrum supplement). With a large litter (>8-10), use rotational nursing "
            "or supplemental feeding. Daily weighing: record every puppy's birth weight and monitor "
            "24-hour weight gain. Perform at least two daily health checks (colour, nursing, "
            "vocalisation, elimination on anogenital stimulation) for early detection of "
            "hypothermia and hypoglycaemia."
        ),
        "prognosis": (
            "Good when the cause can be identified and addressed quickly (60-80% survival). Poor "
            "with CHV-1 infection, severe congenital anomalies or severe sepsis (80-100% fatality). "
            "Low birth weight (LBW) is an independent mortality risk factor — VLBW puppies have "
            "2-4 times the mortality of normal-weight puppies (Mila 2015, Tønnessen 2012). Puppies "
            "that gain weight within the first 12-24 hours generally have a good prognosis. With "
            "recurrent losses across successive litters in a kennel, screen for infectious causes "
            "(CHV-1, E. coli serotypes) and review the facility's disinfection protocol."
        ),
    },
    ("dog", "Neonatal Puppy Mortality / Perinatal Death"): {
        "causes": (
            "Perinatal: asphyxia from dystocia or prolonged labour (perinatal hypoxia), premature "
            "placental separation, umbilical-cord compression, and neonatal depression from "
            "caesarean anaesthetics. Immediately after birth: hypothermia (insufficient ambient "
            "warmth, heat loss while wet), hypoglycaemia (LBW, agalactia, no colostrum intake) and "
            "congenital anomalies (cleft palate, atresia ani, cardiac malformation, umbilical "
            "hernia). Infectious: CHV-1 (clustered at 3 days to 3 weeks of age, with hypothermia an "
            "important trigger), E. coli and Streptococcus (omphalitis progressing to sepsis), "
            "Campylobacter and Salmonella (enteritis), Cryptosporidium and Giardia (diarrhoea and "
            "malabsorption), roundworm and hookworm (transplacental/transmammary infection). "
            "Maternal: agalactia and mastitis, maternal rejection, post-eclampsia debility, and "
            "post-partum metritis (maternal deterioration leading to reduced lactation)."
        ),
        "pathophysiology": (
            "Timeline of clustered mortality — 0-48 hours: perinatal asphyxia (cord compression, "
            "placental separation, prolonged dystocia during labour), hypothermia (immature "
            "thermoregulation), congenital anomalies, hypoglycaemia. 3-7 days: acute CHV-1 "
            "infection (a latently infected dam infects the puppy via the birth canal or "
            "environment, with fatal systemic infection in a cold environment), sepsis (E. coli and "
            "Streptococcus from umbilical infection), malnutrition (agalactia, large litter). 1-4 "
            "weeks: malabsorption syndrome, enteritis (Cryptosporidium, Giardia, rotavirus), "
            "inborn metabolic errors, anaemia (hookworm). Risk stratification — LBW: below 75% of "
            "breed standard, ~2x the mortality of normal-weight puppies (Tønnessen 2012); VLBW: "
            "below 60% of breed standard, 4-6x mortality; litter-size interaction: larger litters "
            "dilute milk and maternal immunity per puppy and increase LBW puppies; delivery mode: "
            "caesarean raises early mortality risk through delayed maternal behaviour and "
            "anaesthetic-induced neonatal depression."
        ),
        "prevention": (
            "Pre-breeding: infection screening (CHV-1, Brucella, heartworm, gastrointestinal "
            "parasites), BCS optimisation (3-4/5), a complete breeding diet (25-30% protein, AAFCO "
            "growth/reproduction standard) from before mating through the end of lactation, and "
            "deworming (fenbendazole from day 40 of pregnancy to 14 days post-partum). Pre-foaling "
            "and environment: clean and disinfect the whelping box (0.5% hypochlorite), change "
            "bedding frequently (every 6-12 h), set ambient temperature (33-35°C at foaling, 32°C "
            "in the first 1-2 weeks), and prepare a resuscitation set (bulb suction, clean towels, "
            "5% dextrose, doxapram, naloxone). Systematic post-birth monitoring: record every "
            "puppy's birth weight and weigh at the same time daily. Checkpoints within 48 hours: "
            "temperature (target rectal 35-37°C), suckle strength, vocalisation (a non-crying puppy "
            "warrants attention), abdominal distension (gas, diarrhoea), urination/defecation (does "
            "not eliminate spontaneously without stimulation — rule out atresia ani), maternal "
            "acceptance and milk output per teat. Begin supplemental feeding within 24 hours for "
            "any puppy not gaining 5-10%/day; with a large litter (>8-10), use rotational nursing "
            "or hand-rearing. With continued losses in a kennel: CHV-1 serology and virus "
            "isolation, bacterial culture (omphalitis discharge, necropsy of dead puppies), review "
            "of the disinfection protocol, and isolation of the whelping box (to prevent horizontal "
            "spread within the facility)."
        ),
        "prognosis": (
            "Large epidemiological studies (Tønnessen 2012, 224,512 dogs across 224 breeds) put "
            "canine neonatal mortality at 4-8% on average (varying widely by breed). 50-80% of "
            "deaths cluster within the first 7 days (Mila 2015). LBW is an independent mortality "
            "risk factor, with VLBW mortality 4-6x that of normal-weight puppies (Indrebø 2007). In "
            "cases where the cause is identified and addressed quickly, survival improves to "
            "60-80%. Acute CHV-1 infection, severe congenital anomalies and puppies resuscitated "
            "after prolonged perinatal asphyxia carry a poor prognosis (80-100% fatality). "
            "Introducing a systematic breeding-management programme (ambient-temperature "
            "management, colostrum management, weight monitoring) can significantly reduce neonatal "
            "mortality in a kennel (Tønnessen 2012, Mila 2019)."
        ),
    },
    # ------------------------------------------------------------- exotic
    ("exotic_other", "Mammary Tumors (Exotic Mammal)"): {
        "prognosis": (
            "The prognosis depends on tumour type and stage. Benign tumours have a good prognosis "
            "after complete excision; malignant tumours require further evaluation, and metastatic "
            "disease carries a guarded to poor prognosis."
        ),
    },
    ("exotic_other", "Hedgehog Oral Squamous Cell Carcinoma"): {
        "prognosis": (
            "The prognosis depends on tumour type, stage and treatment response. Complete excision "
            "of a localised tumour improves the outcome; metastatic disease carries a guarded to "
            "poor prognosis."
        ),
    },
}


def apply_english_overlay(diseases: list, species: str) -> int:
    """Set English narrative fields on Japanese-first records of ``species``.

    Mutates the plain-dict records in place, replacing an English field that
    currently holds Japanese text with the curated English translation. Returns
    the number of fields updated. Idempotent: a field already in English (no CJK)
    is skipped, so re-running is a no-op.
    """
    updated = 0
    for d in diseases:
        if not isinstance(d, dict):
            continue
        overlay = DISEASE_ENGLISH.get((species, d.get("name", "")))
        if not overlay:
            continue
        for field_name, english in overlay.items():
            if english and _has_cjk(d.get(field_name)):
                d[field_name] = english
                updated += 1
    return updated
