# Test Coverage Analysis — VetDict

**Date**: 2026-03-14
**Overall Coverage**: **65%** (2,842 / 8,146 statements missed)
**Test Suite**: 783 collected tests → 1,042 passed, 10 failed, 1 skipped

---

## Current Coverage Summary

| Module | Stmts | Miss | Cover |
|--------|-------|------|-------|
| **api/ai/** (30 modules) | 3,347 | 893 | 73% |
| **api/ core** (17 modules) | 1,862 | 849 | 54% |
| **api/data/** (6 modules) | 168 | 54 | 68% |
| **api/species/** (22 modules) | 607 | 283 | 53% |
| **reco2/** (13 modules) | 985 | 140 | 86% |

---

## Modules With 0% Coverage (No Tests At All)

| Module | Statements | Description |
|--------|-----------|-------------|
| `api/ai/adaptive_question_ranker.py` | 113 | Question ranking for adaptive diagnostic flow |
| `api/ai/diagnostic_questionnaire.py` | 105 | Questionnaire generation for diagnostics |
| `api/ai/multidisease_benchmarks.py` | 167 | Benchmark suite for multi-disease detection |
| `api/ai/question_features.py` | 95 | Feature extraction for question optimization |
| `api/ai/question_optimization.py` | 92 | ML-based question selection optimization |
| `api/disease_batch_enricher.py` | 95 | Batch enrichment pipeline for disease data |
| `api/disease_content_enricher.py` | 71 | Content enrichment for disease records |
| `api/errors.py` | 3 | Error handling utilities |
| `api/showdog_api.py` | 267 | ShowDog breed API integration |
| **Total uncovered** | **1,008** | |

---

## Critical Areas Needing Improved Coverage

### 1. **API Routes & Endpoints** — `api/routes/clinical_api.py` (15% coverage)

This is the main HTTP routing layer. Nearly all route handlers are untested.
Testing endpoints with Flask's test client would catch request validation, error
handling, and response format issues.

**Recommended tests:**
- Request validation (missing/invalid parameters)
- Error responses (404, 400, 500)
- Response schema validation
- CORS and auth integration

### 2. **Drug Dictionary** — `api/drug_dictionary.py` (27% coverage)

Core feature with species-specific drug data. Only the data constants are
"covered" by import; the lookup functions are untested.

**Recommended tests:**
- Drug lookup by name (English and Japanese)
- Species-specific dosing retrieval
- Drug interaction checks
- Edge cases: unknown drugs, empty queries

### 3. **Veterinary API Main App** — `api/vetdict_api.py` (54% coverage)

The Flask app setup and route registration. Missing coverage on many endpoint
handlers.

**Recommended tests:**
- Integration tests for all registered routes
- Middleware behavior (CORS, error handlers)
- Static file serving

### 4. **Species Helpers** — `api/species/helpers.py` (17% coverage)

Shared logic for multi-species symptom analysis — only 37 of 215 statements
covered. This is core diagnostic logic used by all non-dog species.

**Recommended tests:**
- `analyze_symptoms_generic()` for each species
- Breed risk lookup
- Symptom pair/triple boost calculations
- Gender prevalence multipliers

### 5. **ShowDog API** — `api/showdog_api.py` (0% coverage, 267 lines)

Entire module untested. Handles breed data from external API.

**Recommended tests:**
- API response parsing
- Error handling for unavailable external service
- Caching behavior

### 6. **Learning Insights** — `api/learning_insights.py` (23% coverage)

Tracks diagnostic learning patterns. Most functions untested.

**Recommended tests:**
- Insight generation from session data
- Statistics calculation
- Edge cases with empty/minimal data

### 7. **Diagnostic Chat** — `api/diagnostic_chat.py` (57% coverage)

Core conversational diagnostic feature. Several important code paths are
uncovered (lines 2193-2589), including differential analysis and treatment
planning.

**Recommended tests:**
- Multi-turn conversation flows
- Treatment plan generation
- Differential analysis between diseases
- Edge cases: unknown species, empty symptom lists

### 8. **Health Checker** — `api/health_checker.py` (55% coverage)

Disease database and diagnostic test mapping. Missing coverage in endpoint
handlers and test result formatting.

**Recommended tests:**
- Diagnostic test mapping (`DIAGNOSTIC_TEST_MAP`) lookups
- Disease list API responses
- Search and filter functionality

### 9. **AI Question Optimization Pipeline** (0% coverage across 3 modules)

`adaptive_question_ranker.py`, `question_features.py`, `question_optimization.py`
together total 300 uncovered statements. These form the intelligent question
selection pipeline.

**Recommended tests:**
- Question ranking by information gain
- Feature extraction correctness
- Optimization convergence

### 10. **Evidence Calculator** — `api/ai/evidence_calculator.py` (34% coverage)

Computes evidence-based scores for diagnoses. Critical for diagnostic accuracy.

**Recommended tests:**
- Score calculation with various evidence types
- Edge cases: missing evidence, conflicting evidence
- Integration with symptom checker

---

## Existing Test Failures (10 tests)

| Test | Issue |
|------|-------|
| `test_ai_disabled_by_default` | Assertion on AI config default |
| `test_cache_hit` | Cache mechanism not working |
| `test_japanese_lameness` | Japanese symptom extraction |
| `test_japanese_paralysis` | Japanese symptom extraction |
| `test_no_hardcoded_secrets` | Case-sensitive string check |
| `test_proper_error_handling` | Code quality validation |
| `test_no_sql_injection_vulnerabilities` | Security validation |
| `test_no_debug_mode_in_production` | Production config check |
| `test_security_checklist_complete` | Documentation validation |
| `test_production_ready_summary` | File path assertion |

**Priority**: Fix the 2 Japanese symptom extraction failures and the cache hit
test, as these indicate real functional regressions. The production validation
tests appear to be stale assertions that need updating.

---

## Recommended Test Improvement Plan

### Phase 1 — High Impact (close critical gaps)
1. Add tests for `api/routes/clinical_api.py` (endpoint integration tests)
2. Add tests for `api/species/helpers.py` (core multi-species logic)
3. Improve `api/diagnostic_chat.py` coverage (differential + treatment paths)
4. Fix the 10 failing tests

### Phase 2 — Medium Impact (improve reliability)
5. Add tests for `api/drug_dictionary.py` (drug lookup functions)
6. Add tests for `api/ai/evidence_calculator.py` (scoring accuracy)
7. Add tests for `api/learning_insights.py` (learning analytics)
8. Add tests for `api/health_checker.py` endpoint handlers

### Phase 3 — Completeness
9. Add tests for `api/showdog_api.py` (external API integration)
10. Add tests for AI question optimization pipeline (3 modules)
11. Add tests for disease enrichment pipeline (2 modules)
12. Add species-specific integration tests for exotic species

### Target
Raise overall coverage from **65% → 85%** by completing Phases 1-2.
