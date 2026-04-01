"""VetDict diagnostic chat subpackage.

Splits the monolithic diagnostic_chat.py into focused modules:
- symptom_aliases: JP/EN symptom alias dictionary (SYMPTOM_ALIASES)
- species_data: Species module loading and _SPECIES_DATA
- symptom_extractor: Symptom extraction from text
- disease_matcher: Disease matching algorithm
- supplements: Disease supplement data
- constants: Shared constants (species labels, generic species list)
- helpers: Chat helper functions
"""
