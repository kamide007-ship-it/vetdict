# ShowDog Analysis Platform - Algorithm Declaration

**Version:** 1.0.0
**Effective Date:** 2026-02-06
**Authority:** ShowDog Analysis Platform Development Team
**Classification:** Authoritative System Declaration

---

## 1. Purpose and Scope

This document serves as the **authoritative declaration** of the scoring algorithm used by the ShowDog Analysis Platform. All numeric evaluations produced by the system MUST conform to the specifications defined herein.

**This algorithm is IMMUTABLE** and may only be modified through a formal versioning process with full audit trail.

---

## 2. Evaluation Axes

The system evaluates dogs across **five (5) primary axes**, each derived from FCI (Fédération Cynologique Internationale) breed standards and veterinary evaluation criteria.

### 2.1 Skeletal Structure (骨格構造)
- **FCI Mapping:** Body proportions, bone structure, angulation
- **Evaluation Criteria:**
  - Skeletal proportions relative to breed standard
  - Joint angles (shoulder, hip, stifle)
  - Overall structural soundness
- **Score Range:** 0-100

### 2.2 Gait (歩様)
- **FCI Mapping:** Movement, reach, drive, balance
- **Evaluation Criteria:**
  - Stride length and consistency
  - Front and rear coordination
  - Side gait efficiency
  - Topline stability during movement
- **Score Range:** 0-100

### 2.3 Muscle Development (筋肉発達)
- **FCI Mapping:** Condition, muscle tone, fitness
- **Evaluation Criteria:**
  - Muscle definition appropriate to breed
  - Body condition score
  - Athletic development
- **Score Range:** 0-100

### 2.4 Coat Quality (被毛品質)
- **FCI Mapping:** Coat texture, density, condition
- **Evaluation Criteria:**
  - Texture conformity to breed standard
  - Coat health and shine
  - Grooming condition
- **Score Range:** 0-100

### 2.5 Temperament (気質)
- **FCI Mapping:** Character, behavior, expression
- **Evaluation Criteria:**
  - Confidence level
  - Alertness and attention
  - Composure under evaluation
- **Score Range:** 0-100

---

## 3. Fixed Weights

The following weights are **IMMUTABLE** and **HARD-CODED** into the system.

```
WEIGHTS = {
    "skeletal":    0.25,   # 25%
    "gait":        0.25,   # 25%
    "muscle":      0.20,   # 20%
    "coat":        0.20,   # 20%
    "temperament": 0.10    # 10%
}

Sum = 1.00 (100%)
```

### 3.1 Weight Rationale

| Axis        | Weight | Rationale |
|-------------|--------|-----------|
| Skeletal    | 25%    | Foundation of breed type; structural soundness is paramount |
| Gait        | 25%    | Direct indicator of functional correctness and soundness |
| Muscle      | 20%    | Reflects health, conditioning, and breed-appropriate development |
| Coat        | 15%    | Important breed characteristic, but less critical than structure |
| Temperament | 10%    | Essential for show ring, but partially situational |

### 3.2 Prohibition on Weight Modification

**It is STRICTLY PROHIBITED to:**
- Modify weights via database configuration
- Modify weights via user interface
- Modify weights via environment variables
- Allow any runtime modification of weights

All weight changes MUST be:
1. Documented in this declaration
2. Reviewed by authorized personnel
3. Implemented as a new algorithm version
4. Deployed with full audit trail

---

## 4. Age Adjustment

A deterministic age adjustment is applied to account for developmental stages.

### 4.1 Age Adjustment Table

| Age (months) | Adjustment |
|--------------|------------|
| 0-6          | -5         |
| 7-12         | -3         |
| 13-24        | -1         |
| 25-84        | 0          |
| 85-108       | -1         |
| 109-132      | -3         |
| 133+         | -5         |

### 4.2 Rationale

- **Puppies (0-12 months):** Incomplete development; scores adjusted downward
- **Young adults (13-24 months):** Near maturity; minimal adjustment
- **Prime adults (25-84 months / 2-7 years):** Peak condition; no adjustment
- **Veterans (85+ months / 7+ years):** Age-related changes; adjusted accordingly

---

## 5. Final Score Calculation

```
weighted_sum = Σ(axis_score × axis_weight)
age_adj = get_age_adjustment(age_months)
final_score = clamp(weighted_sum + age_adj, 0, 100)
```

### 5.1 Grade Mapping

| Score Range | Grade |
|-------------|-------|
| 95-100      | S     |
| 90-94       | A+    |
| 85-89       | A     |
| 80-84       | B+    |
| 70-79       | B     |
| 0-69        | C     |

---

## 6. Determinism Guarantee

**The system guarantees that:**

Given identical inputs:
- Same axis scores
- Same age
- Same algorithm version

The output will ALWAYS be identical.

**No randomness, no LLM-based numeric decisions, no external dependencies affect the final score calculation.**

---

## 7. Role of AI Vision Analysis

The OpenAI Vision API is used ONLY for:
- **Feature detection** (identifying anatomical features)
- **Qualitative assessment** (describing conditions)
- **Score suggestion** (providing initial axis scores)

The AI does NOT:
- Determine final weights
- Override the scoring algorithm
- Make non-reproducible calculations

All AI-suggested scores are passed through the deterministic scoring core before being finalized.

---

## 8. Audit Requirements

Every analysis MUST record:
- Algorithm version
- Model version
- Weights hash
- Input type (photo/video)
- Timestamp
- All axis scores
- Final calculated score

---

## 9. Version History

| Version | Date       | Changes |
|---------|------------|---------|
| 1.0.0   | 2026-02-06 | Initial algorithm declaration |

---

## 10. Certification

This algorithm declaration is certified as the authoritative specification for the ShowDog Analysis Platform scoring system.

Any deviation from this specification is a **system defect** and must be reported immediately.

---

*Document Hash: SHA256 to be computed at deployment*
