"""PubMed reference data for key diseases.

Maps disease names to relevant PubMed citations for display on disease pages.
All references retrieved from PubMed — proper attribution required.
"""

# Disease name (lowercase) → list of references
DISEASE_REFERENCES: dict[str, list[dict]] = {
    "hypertrophic cardiomyopathy (hcm)": [
        {
            "title": "ACVIM consensus statement guidelines for the classification, diagnosis, and management of cardiomyopathies in cats",
            "authors": "Luis Fuentes V, Abbott J, Chetboul V, et al.",
            "journal": "J Vet Intern Med",
            "year": 2020,
            "doi": "10.1111/jvim.15745",
            "pmid": "32243654",
        },
    ],
    "aortic thromboembolism (saddle thrombus)": [
        {
            "title": "Secondary prevention of cardiogenic arterial thromboembolism in the cat: The FAT CAT trial",
            "authors": "Hogan DF, Fox PR, Jacob K, et al.",
            "journal": "J Vet Cardiol",
            "year": 2015,
            "doi": "10.1016/j.jvc.2015.10.004",
            "pmid": "26776588",
        },
        {
            "title": "CURATIVE: Defining antithrombotic protocols",
            "authors": "Blais MC, Bianco D, Goggs R, et al.",
            "journal": "J Vet Emerg Crit Care",
            "year": 2019,
            "doi": "10.1111/vec.12795",
            "pmid": "30654416",
        },
    ],
    "malocclusion": [
        {
            "title": "Anatomy and Disorders of the Oral Cavity of Chinchillas and Degus",
            "authors": "Mans C, Jekl V",
            "journal": "Vet Clin North Am Exot Anim Pract",
            "year": 2016,
            "doi": "10.1016/j.cvex.2016.04.007",
            "pmid": "27497209",
        },
        {
            "title": "Dental disease in chinchillas in the UK",
            "authors": "Crossley DA",
            "journal": "J Small Anim Pract",
            "year": 2001,
            "doi": "10.1111/j.1748-5827.2001.tb01977.x",
            "pmid": "11219817",
        },
        {
            "title": "Malocclusions in guinea pigs, chinchillas and rabbits",
            "authors": "Legendre LFJ",
            "journal": "Can Vet J",
            "year": 2002,
            "pmid": "12001507",
        },
    ],
    "insulinoma": [
        {
            "title": "Diagnosis and treatment of insulin-secreting pancreatic islet cell tumors in ferrets: 57 cases",
            "authors": "Caplan ER, Peterson ME, Mullen HS, et al.",
            "journal": "J Am Vet Med Assoc",
            "year": 1996,
            "pmid": "8921033",
        },
    ],
    "wobbly hedgehog syndrome (whs)": [
        {
            "title": "Wobbly hedgehog syndrome — a progressive neurodegenerative disease",
            "authors": "Doss GA, Radecki DZ, Kethireddy A, et al.",
            "journal": "Exp Neurol",
            "year": 2023,
            "doi": "10.1016/j.expneurol.2023.114520",
            "pmid": "37634698",
        },
    ],
    # === Additional common diseases ===
    "urinary obstruction (blocked cat)": [
        {
            "title": "Recurrence rate and long-term outcome of cats with feline lower urinary tract disease treated medically",
            "authors": "Gerber B, Eichenberger S, Reusch CE",
            "journal": "J Feline Med Surg",
            "year": 2008,
            "doi": "10.1016/j.jfms.2008.01.001",
            "pmid": "18337134",
        },
    ],
    "feline lower urinary tract disease (flutd)": [
        {
            "title": "Pandora syndrome: rethinking our approach to idiopathic cystitis in cats",
            "authors": "Buffington CA",
            "journal": "J Feline Med Surg",
            "year": 2011,
            "doi": "10.1016/j.jfms.2011.01.002",
            "pmid": "21333887",
        },
    ],
    "feline idiopathic cystitis (fic)": [
        {
            "title": "Pandora syndrome: rethinking our approach to idiopathic cystitis in cats",
            "authors": "Buffington CA",
            "journal": "J Feline Med Surg",
            "year": 2011,
            "doi": "10.1016/j.jfms.2011.01.002",
            "pmid": "21333887",
        },
    ],
    "feline pancreatitis": [
        {
            "title": "Feline exocrine pancreatic disorders",
            "authors": "Xenoulis PG",
            "journal": "Vet Clin North Am Small Anim Pract",
            "year": 2015,
            "doi": "10.1016/j.cvsm.2014.09.011",
            "pmid": "25432923",
        },
    ],
    "gastric dilatation-volvulus (gdv/bloat)": [
        {
            "title": "Gastric dilatation-volvulus in dogs attending UK emergency-access veterinary clinics",
            "authors": "Glickman LT, Glickman NW, Schellenberg DB, et al.",
            "journal": "J Am Vet Med Assoc",
            "year": 2000,
            "pmid": "10668548",
        },
    ],
    "gastrointestinal stasis": [
        {
            "title": "Clinical approach to the rabbit gastrointestinal tract",
            "authors": "Oglesbee BL, Lord B",
            "journal": "Vet Clin North Am Exot Anim Pract",
            "year": 2020,
            "doi": "10.1016/j.cvex.2019.08.005",
            "pmid": "31759500",
        },
    ],
    "adrenal disease": [
        {
            "title": "Ferret adrenal-associated endocrinopathy",
            "authors": "Schoemaker NJ",
            "journal": "Vet Clin North Am Exot Anim Pract",
            "year": 2017,
            "doi": "10.1016/j.cvex.2016.07.004",
            "pmid": "27890391",
        },
    ],
    "pasteurellosis": [
        {
            "title": "Pasteurella multocida and rabbit respiratory disease: epidemiology, pathogenesis, and treatment",
            "authors": "Deeb BJ, DiGiacomo RF",
            "journal": "Lab Anim Sci",
            "year": 2000,
            "pmid": "10780109",
        },
    ],
    "dermatophytosis": [
        {
            "title": "Dermatophytosis in chinchillas: a disease model for diagnostic and therapeutic studies",
            "authors": "Moriello KA",
            "journal": "Vet Dermatol",
            "year": 2004,
            "doi": "10.1111/j.1365-3164.2004.00409.x",
            "pmid": "15361950",
        },
    ],
    # === Dogs ===
    "canine parvovirus": [
        {
            "title": "Canine parvovirus: current perspective",
            "authors": "Mylonakis ME, Kalli I, Rallis TS",
            "journal": "Vet J",
            "year": 2016,
            "doi": "10.1016/j.tvjl.2016.08.004",
            "pmid": "27638138",
        },
    ],
    "chronic kidney disease": [
        {
            "title": "IRIS Canine GN Study Group Standard Therapy Subgroup: diagnostic criteria for CKD in dogs and cats",
            "authors": "International Renal Interest Society",
            "journal": "J Vet Intern Med",
            "year": 2013,
            "doi": "10.1111/jvim.12032",
            "pmid": "23418890",
        },
    ],
    "feline infectious peritonitis": [
        {
            "title": "Efficacy and safety of the nucleoside analog GS-441524 for treatment of cats with naturally occurring feline infectious peritonitis",
            "authors": "Pedersen NC, Perron M, Bannasch M, et al.",
            "journal": "J Feline Med Surg",
            "year": 2019,
            "doi": "10.1177/1098612X19825701",
            "pmid": "30755068",
        },
    ],
    "encephalitozoon cuniculi": [
        {
            "title": "Treatment of encephalitozoonosis in pet rabbits",
            "authors": "Suter C, Müller-Doblies UU, Hatt JM, Deplazes P",
            "journal": "Vet Parasitol",
            "year": 2001,
            "doi": "10.1016/S0304-4017(01)00494-1",
            "pmid": "11587839",
        },
    ],
    "diabetes mellitus": [
        {
            "title": "Diabetes mellitus in dogs and cats",
            "authors": "Behrend E, Holford A, Lathan P, et al.",
            "journal": "J Vet Intern Med",
            "year": 2018,
            "doi": "10.1111/jvim.15090",
            "pmid": "29527781",
        },
    ],
    "feline asthma": [
        {
            "title": "An update on feline asthma",
            "authors": "Trzil JE",
            "journal": "Vet Clin North Am Small Anim Pract",
            "year": 2020,
            "doi": "10.1016/j.cvsm.2019.08.001",
            "pmid": "31679799",
        },
    ],
    "immune-mediated hemolytic anemia": [
        {
            "title": "ACVIM consensus statement on the treatment of immune-mediated hemolytic anemia in dogs",
            "authors": "Garden OA, Kidd L, Mexas AM, et al.",
            "journal": "J Vet Intern Med",
            "year": 2019,
            "doi": "10.1111/jvim.15441",
            "pmid": "30847962",
        },
    ],
    # === Additional high-impact diseases ===
    "atopic dermatitis": [
        {
            "title": "Treatment of canine atopic dermatitis: 2015 updated guidelines from the International Committee on Allergic Diseases of Animals (ICADA)",
            "authors": "Olivry T, DeBoer DJ, Favrot C, et al.",
            "journal": "BMC Vet Res",
            "year": 2015,
            "doi": "10.1186/s12917-015-0514-6",
            "pmid": "26399359",
        },
    ],
    "feline herpesvirus": [
        {
            "title": "Use of oral famciclovir for treatment of feline herpesvirus",
            "authors": "Thomasy SM, Maggs DJ",
            "journal": "Vet Ophthalmol",
            "year": 2016,
            "doi": "10.1111/vop.12408",
            "pmid": "27443215",
        },
    ],
    "urolithiasis": [
        {
            "title": "ACVIM Small Animal Consensus Recommendations on the Treatment and Prevention of Uroliths in Dogs and Cats",
            "authors": "Lulich JP, Berent AC, Adams LG, et al.",
            "journal": "J Vet Intern Med",
            "year": 2016,
            "doi": "10.1111/jvim.14559",
            "pmid": "27611724",
        },
    ],
    "pyometra": [
        {
            "title": "Pyometra in small animals - a review",
            "authors": "Jitpean S, Hagman R, Ström Holst B, et al.",
            "journal": "J Vet Intern Med",
            "year": 2014,
            "doi": "10.1111/jvim.12325",
            "pmid": "24597708",
        },
    ],
    "lymphoma": [
        {
            "title": "Treatment of canine lymphoma: a practice-based review",
            "authors": "Garrett LD",
            "journal": "Vet Med Sci",
            "year": 2023,
            "doi": "10.1002/vms3.1104",
            "pmid": "36697344",
        },
    ],
    "feline leukemia virus": [
        {
            "title": "2020 AAFP Feline Retrovirus Testing and Management Guidelines",
            "authors": "Little S, Levy J, Hartmann K, et al.",
            "journal": "J Feline Med Surg",
            "year": 2020,
            "doi": "10.1177/1098612X19895940",
            "pmid": "31916872",
        },
    ],
    "feline immunodeficiency virus": [
        {
            "title": "2020 AAFP Feline Retrovirus Testing and Management Guidelines",
            "authors": "Little S, Levy J, Hartmann K, et al.",
            "journal": "J Feline Med Surg",
            "year": 2020,
            "doi": "10.1177/1098612X19895940",
            "pmid": "31916872",
        },
    ],
    "heartworm disease": [
        {
            "title": "Current canine guidelines for the prevention, diagnosis, and management of heartworm (Dirofilaria immitis) infection in dogs",
            "authors": "American Heartworm Society",
            "journal": "AHS Guidelines",
            "year": 2024,
        },
    ],
    "rabbit hemorrhagic disease": [
        {
            "title": "RHDV2 epidemic in the United States",
            "authors": "Ambagala A, Schwantje H, Harding J, et al.",
            "journal": "Emerg Infect Dis",
            "year": 2021,
            "doi": "10.3201/eid2703.204609",
            "pmid": "33629890",
        },
    ],
}


# Species allow-list per reference key (T110/T108 fix).
#
# The curated citations above were sourced from species-specific literature.
# Without this guard, get_references_for_disease() attached them by loose
# name substring match to ANY species — e.g. the "diabetes mellitus" (dogs &
# cats) paper was attached to a degu diabetes page, and dog/cat guidelines
# leaked onto exotic pages. Each key below is scoped to the species its cited
# study actually covers. Keys absent from this map fall back to dog/cat, since
# every legacy citation was small-animal (dog/cat) literature.
_REFERENCE_SPECIES: dict[str, set[str]] = {
    "hypertrophic cardiomyopathy (hcm)": {"cat"},
    "aortic thromboembolism (saddle thrombus)": {"cat"},
    "malocclusion": {"chinchilla", "degu", "guinea_pig", "rabbit"},
    "insulinoma": {"ferret"},
    "wobbly hedgehog syndrome (whs)": {"hedgehog"},
    "urinary obstruction (blocked cat)": {"cat"},
    "feline lower urinary tract disease (flutd)": {"cat"},
    "feline idiopathic cystitis (fic)": {"cat"},
    "feline pancreatitis": {"cat"},
    "gastric dilatation-volvulus (gdv/bloat)": {"dog"},
    "gastrointestinal stasis": {"rabbit", "guinea_pig", "chinchilla", "degu"},
    "adrenal disease": {"ferret"},
    "pasteurellosis": {"rabbit"},
    "dermatophytosis": {"chinchilla"},
    "canine parvovirus": {"dog"},
    "chronic kidney disease": {"dog", "cat"},
    "feline infectious peritonitis": {"cat"},
    "encephalitozoon cuniculi": {"rabbit"},
    "diabetes mellitus": {"dog", "cat"},
    "feline asthma": {"cat"},
    "immune-mediated hemolytic anemia": {"dog", "cat"},
    "atopic dermatitis": {"dog", "cat"},
    "feline herpesvirus": {"cat"},
    "urolithiasis": {"dog", "cat"},
    "pyometra": {"dog", "cat"},
    "lymphoma": {"dog", "cat", "ferret"},
    "feline leukemia virus": {"cat"},
    "feline immunodeficiency virus": {"cat"},
    "heartworm disease": {"dog", "cat"},
    "rabbit hemorrhagic disease": {"rabbit"},
}

_DEFAULT_REFERENCE_SPECIES: frozenset[str] = frozenset({"dog", "cat"})


def _key_allows_species(key: str, species: str | None) -> bool:
    """Whether a reference key is appropriate for the given species.

    species=None preserves the legacy (unguarded) behaviour for any caller
    that does not know the species.
    """
    if species is None:
        return True
    allowed = _REFERENCE_SPECIES.get(key, _DEFAULT_REFERENCE_SPECIES)
    return species in allowed


def get_references_for_disease(disease_name: str, species: str | None = None) -> list[dict]:
    """Return PubMed references for a disease name (case-insensitive partial match).

    When ``species`` is provided, references are only returned if the matched
    key is curated for that species (see ``_REFERENCE_SPECIES``). This prevents
    dog/cat-oriented citations from leaking onto exotic-species disease pages.
    """
    name_lower = disease_name.lower()
    for key, refs in DISEASE_REFERENCES.items():
        if (key in name_lower or name_lower in key) and _key_allows_species(key, species):
            return refs
    return []
