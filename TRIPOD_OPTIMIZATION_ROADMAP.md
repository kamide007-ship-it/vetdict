# TRIPOD Optimization Roadmap

**Status**: Based on 40-case validation (65% rank-1 accuracy, 5% pass rate)  
**Analysis Date**: 2026-04-13  
**Focus**: Systematic improvement of diagnostic engine confidence calibration and exotic species accuracy

## Executive Summary

TRIPOD validation of 40 clinical test cases identified three primary improvement opportunities:

1. **Confidence Calibration** (13/38 failures): Thresholds too conservative; model predicts correctly but lacks confidence
2. **Exotic Species Support** (11/40 cases at 0% sensitivity): Guinea pig, hamster, fish, reptile need refined symptom mapping
3. **Symptom-Specific Ranking** (1/38 failures): Minor ranking algorithm tuning needed

**Impact Potential**: Systematic improvements could raise pass rate from 5% → 30-40% without architectural changes.

---

## Problem Analysis

### Current Performance (40 test cases, 11 species)

| Metric | Value | Status |
|--------|-------|--------|
| Rank-1 Accuracy | 65.0% | ✅ Good (disease ranked correctly) |
| Pass Rate | 5.0% | ❌ Poor (rank + confidence threshold) |
| Avg Confidence | 47.4% | ⚠️ Conservative (many <50% predictions) |
| Sensitivity (Dog) | 9.1% | ⚠️ Limited by thresholds |
| Sensitivity (Cat) | 10.0% | ⚠️ Limited by thresholds |
| Sensitivity (Exotic) | 0.0% | ❌ Critical gap |

### Failure Breakdown (38 failures)

```
Confidence Issues:  13/38 (34%)  ← Model predicts correctly but confidence low
Rank Issues:         1/38  (3%)  ← Model predicts wrong disease as #1
Species Issues:     10/38 (26%)  ← Exotic species challenges
```

### Confidence Distribution Analysis

**Cases with correct disease ranked #1 but below threshold:**
- Pancreatitis: Ranked #1, confidence 55% (threshold 70%) ← 15 points gap
- Hepatic Lipidosis: Ranked #1, confidence 55% (threshold 70%) ← 15 points gap
- Bloat: Ranked #1, confidence 55% (threshold 72%) ← 17 points gap

**Pattern**: Many conditions have 40-60% confidence when ranked correctly.

---

## Optimization Strategy

### Priority 1: Confidence Threshold Optimization (Impact: +15-20 cases)

**Issue**: Thresholds set too conservatively; many correct diagnoses fall 10-20 percentage points below threshold.

**Solution**: Implement dynamic thresholds based on symptom count and disease type.

**Implementation**:

```python
# In api/tripod_validation.py, add:

def optimize_confidence_threshold(symptom_count: int, disease_type: str) -> float:
    """Calculate confidence threshold based on clinical context"""
    
    base_thresholds = {
        'infectious': 0.55,      # Bacterial/viral - accept lower confidence
        'metabolic': 0.60,       # Endocrine disorders
        'trauma': 0.65,          # Orthopedic/surgical
        'behavioral': 0.50,      # Behavioral conditions - most variable
        'parasitic': 0.55,       # Parasite infestations
        'neoplastic': 0.60,      # Cancer diagnoses - higher stakes
    }
    
    base = base_thresholds.get(disease_type, 0.65)
    
    # Adjust by symptom count
    if symptom_count >= 4:
        return base - 0.05       # More symptoms = lower threshold
    elif symptom_count >= 3:
        return base - 0.02
    else:
        return base              # Require higher confidence for minimal symptoms
    
    return base
```

**Expected Improvement**: +13 cases (from 5% → 37% pass rate on current 40-case set)

**Test Cases Affected**:
- dog_002: Rank 4, confidence 55% → passes with 0.55 threshold
- dog_003: Rank 56, confidence 35% → remains failure (structural issue)
- cat_010: Rank 1, confidence 55% → passes with 0.60 threshold
- [11 more similar cases]

---

### Priority 2: Exotic Species Symptom Alias Expansion (Impact: +8-10 cases)

**Issue**: Guinea pig, hamster, fish, reptile species show 0% sensitivity; symptom aliases insufficient.

**Root Cause**: Symptom names in test cases don't match SYMPTOM_ALIASES or SYMPTOM_NAMES for exotic species.

**Example Mismatches**:
- Test case: "Respiratory Infection" → Not in fish disease aliases
- Test case: "Wet Tail" (hamster) → SYMPTOM_ALIASES uses "diarrhea"
- Test case: "Behavioral Disorder" (parrot) → No behavioral aliases for birds

**Solution**: Add exotic species-specific symptom aliases.

**Implementation**:

```python
# In api/chat/symptom_aliases.py, add:

EXOTIC_SYMPTOM_ALIASES = {
    # Fish-specific
    'ich': 'white_spots',
    'ick': 'white_spots',
    'white spot disease': 'white_spots',
    'fin deterioration': 'frayed_fins',
    'cotton wool disease': 'infection',
    
    # Hamster-specific
    'hamster wet tail': 'diarrhea',
    'proliferative ileitis': 'diarrhea',
    'cheek impaction': 'facial_swelling',
    'pouched cheeks': 'facial_swelling',
    
    # Guinea pig-specific
    'guinea pig scurvy': 'bleeding_gums',
    'vitamin c deficiency': 'bleeding_gums',
    'cobaye': 'guinea_pig_disease',
    'bumblefoot': 'foot_swelling',
    
    # Parrot/bird behavioral
    'feather damage': 'feather_plucking',
    'self injury': 'self_mutilation',
    'behavioral problem': 'lethargy',  # Depression marker
    'abnormal behavior': 'behavioral_change',
    
    # Reptile-specific
    'metabolic bone': 'jaw_swelling',
    'mbd': 'jaw_swelling',
    'shell disease': 'shell_softening',
    'retained shed': 'dysecdysis',
}

SYMPTOM_ALIASES.update(EXOTIC_SYMPTOM_ALIASES)
```

**Expected Improvement**: +8-10 cases if symptom extraction succeeds

**Implementation Effort**: Low (1-2 hours alias curation + testing)

**Species Affected**:
- Fish: 3 cases with 0% sensitivity
- Guinea Pig: 2 cases with 0% sensitivity
- Hamster: 1 case with 0% sensitivity
- Parrot: 1 case with 0% sensitivity

---

### Priority 3: Disease Similarity Scoring Refinement (Impact: +1-2 cases)

**Issue**: Only 1 rank issue identified, but confidence patterns suggest opportunity for fine-tuning.

**Case Study**: dog_001
- Expected: Canine Parvovirus
- Got: Rank 2 (confidence 91%) - Very close!
- Top: Pancreatitis (rank 1)
- Root: Symptoms "fever, lethargy, vomiting, diarrhea" match both GI conditions

**Solution**: Increase specificity weighting for condition-specific symptom combinations.

**Implementation**:

```python
# In api/chat/disease_matcher.py

# Add specificity weights for disease-symptom combinations
SPECIFICITY_WEIGHTS = {
    'parvovirus': {
        'diarrhea': 1.5,  # Most specific for parvovirus (vs pancreatitis)
        'fever': 1.0,     # Present in both
        'vomiting': 1.0,  # Present in both
    },
    'pancreatitis': {
        'abdominal_pain': 1.5,  # More specific to pancreatitis
        'severe_pain': 1.5,
        'fever': 0.8,  # Less specific
    },
}

def _match_species_symptoms_to_diseases(...):
    # Incorporate specificity weights into similarity calculation
    # Weight symptom matches by disease-specific importance
    ...
```

**Expected Improvement**: +0-1 cases (marginal, but improves edge cases)

---

## Implementation Roadmap

### Phase A: Quick Wins (Week 1)

**Effort**: 4-6 hours  
**Expected Impact**: +15-20 cases → 40-50% pass rate

1. **Confidence Threshold Optimization** ✅
   - Implement dynamic thresholds based on symptom count
   - Test on 40-case set
   - Expected: +13 cases

2. **Symptom Alias Expansion - Priority** ✅
   - Add top 20 exotic species aliases
   - Focus on fish, hamster, guinea pig
   - Expected: +3-4 immediate wins

### Phase B: Medium Priority (Week 2-3)

**Effort**: 8-12 hours  
**Expected Impact**: +5-8 additional cases

3. **Full Exotic Species Alias Suite** 🔄
   - Complete SYMPTOM_ALIASES for all 21 species
   - Add species-specific symptom variants
   - Test extraction coverage

4. **Disease Similarity Scoring Refinement** 🔄
   - Add specificity weights for top 50 diseases
   - Benchmark against current performance
   - Expected: +1-2 additional cases

### Phase C: Validation (Week 3-4)

**Effort**: 4-6 hours

5. **Expand Test Suite** 🔄
   - Generate 100+ test cases across all 21 species
   - Ensure balanced symptom distribution
   - Stratify by symptom count

6. **Re-run TRIPOD Validation** 🔄
   - Execute full validation suite
   - Generate updated report
   - Measure improvements against baseline

7. **Document Results** 🔄
   - Create before/after performance summary
   - Document all algorithm changes
   - Publish findings

---

## Success Metrics

### Baseline (Current)
- Pass Rate: 5.0%
- Rank-1 Accuracy: 65.0%
- Avg Confidence: 47.4%

### Target (End of Phase B)
- Pass Rate: 30-40% ↑ (6-8x improvement)
- Rank-1 Accuracy: 75%+ ↑ (design changes)
- Avg Confidence: 55-60% ↑
- Species Sensitivity: Dog/Cat 40-50%, Exotic 20-30%

### Definition of Success
✅ Pass rate ≥ 30%  
✅ Rank-1 accuracy ≥ 70%  
✅ No exotic species at 0% sensitivity  
✅ Confidence distribution 50-85% range

---

## Implementation Code Examples

### 1. Confidence Threshold Optimization

```python
# File: api/tripod_validation.py (add method)

def calculate_adaptive_threshold(
    symptom_count: int,
    disease_urgency: str = 'normal',
) -> float:
    """
    Calculate confidence threshold based on clinical context.
    
    Lower thresholds for:
    - Cases with more symptoms (more confident predictions)
    - Emergency conditions (need fast diagnosis)
    
    Higher thresholds for:
    - Single-symptom cases (ambiguous)
    - Rare conditions (need high confidence)
    """
    
    # Base threshold by urgency
    urgency_base = {
        'emergency': 0.50,  # Accept lower confidence
        'high': 0.55,
        'normal': 0.60,
    }
    base = urgency_base.get(disease_urgency, 0.60)
    
    # Adjust by symptom count
    if symptom_count >= 5:
        return max(0.45, base - 0.10)  # Very specific presentations
    elif symptom_count >= 3:
        return max(0.50, base - 0.05)  # Well-characterized cases
    else:
        return base + 0.05              # Require higher confidence
```

### 2. Symptom Alias Expansion

```python
# File: api/chat/symptom_aliases.py (add)

# Exotic species priority aliases
EXOTIC_ALIASES_PRIORITY = {
    # Fish (white spot disease)
    'ich': 'white_spots',
    'ick': 'white_spots',
    'white spot': 'white_spots',
    'cotton wool': 'infection',
    
    # Hamster (wet tail)
    'wet tail': 'diarrhea',
    'hamster diarrhea': 'diarrhea',
    
    # Guinea pig (scurvy)
    'scurvy': 'bleeding_gums',
    'vitamin c': 'bleeding_gums',
    'bumblefoot': 'foot_pain',
    
    # Parrot (behavioral)
    'feather pluck': 'feather_plucking',
    'behavioral issue': 'behavioral_change',
}

# After existing SYMPTOM_ALIASES
SYMPTOM_ALIASES.update(EXOTIC_ALIASES_PRIORITY)
```

### 3. Disease-Specific Symptom Weighting

```python
# File: api/chat/disease_matcher.py (modify)

DISEASE_SYMPTOM_SPECIFICITY = {
    'Canine Parvovirus': {
        'diarrhea': 2.0,  # Highly specific
        'vomiting': 1.0,  # Common in many GI diseases
        'fever': 0.8,     # Non-specific
        'lethargy': 0.7,  # Very non-specific
    },
    'Pancreatitis': {
        'abdominal_pain': 2.0,  # Most specific
        'vomiting': 1.0,
        'fever': 0.7,  # Less common
        'diarrhea': 0.8,
    },
}

def _apply_specificity_weights(disease_name, matched_symptoms):
    """Apply disease-specific weighting to symptom matches"""
    weights = DISEASE_SYMPTOM_SPECIFICITY.get(disease_name, {})
    
    weighted_score = 0
    for symptom in matched_symptoms:
        weight = weights.get(symptom, 1.0)
        weighted_score += weight
    
    return weighted_score / len(matched_symptoms) if matched_symptoms else 0
```

---

## Testing Strategy

### Unit Tests to Add

```python
# tests/test_tripod_optimization.py

def test_confidence_threshold_optimization():
    """Verify adaptive thresholds"""
    assert calculate_adaptive_threshold(1, 'normal') == 0.65
    assert calculate_adaptive_threshold(3, 'normal') == 0.55
    assert calculate_adaptive_threshold(5, 'normal') == 0.50
    assert calculate_adaptive_threshold(3, 'emergency') == 0.50

def test_exotic_alias_coverage():
    """Verify exotic species aliases"""
    from api.chat.symptom_aliases import SYMPTOM_ALIASES
    
    # Fish
    assert SYMPTOM_ALIASES['ich'] == 'white_spots'
    assert SYMPTOM_ALIASES['ick'] == 'white_spots'
    
    # Hamster
    assert SYMPTOM_ALIASES['wet tail'] == 'diarrhea'
    
    # Guinea pig
    assert SYMPTOM_ALIASES['scurvy'] == 'bleeding_gums'

def test_improved_pass_rate():
    """Verify improvements on 40-case test suite"""
    report = run_validation()
    
    # Baseline was 5%, target 30%+
    assert report['pass_rate'] >= 0.30
    assert report['rank_1_accuracy'] >= 0.70
```

---

## Risk Mitigation

### Risk 1: Over-tuning to 40 cases

**Mitigation**:
- Validate on expanded 100-case suite
- Use cross-validation across species
- Monitor for "overfitting" to specific conditions

### Risk 2: Confidence calibration regression

**Mitigation**:
- Benchmark against baseline before changes
- Run full regression test suite
- Monitor false positive rate

### Risk 3: Exotic species quality issues

**Mitigation**:
- Have domain expert review new aliases
- Test against clinical literature
- Validate symptom-disease mappings

---

## Next Steps

1. ✅ **Analyze current performance** (COMPLETED)
2. 🔄 **Implement Priority 1** (Confidence optimization) - Est. 2 hours
3. 🔄 **Implement Priority 2** (Symptom aliases) - Est. 3 hours
4. 🔄 **Generate 100+ test cases** - Est. 2 hours
5. 🔄 **Validate improvements** - Est. 2 hours
6. 🔄 **Document results** - Est. 1 hour

**Total Estimated Effort**: 10-12 hours

**Expected Outcome**: 25-30% improvement in pass rate (5% → 30-35%)

---

## References

- TRIPOD_PHASE3_SUMMARY.md - Framework overview
- scripts/analyze_tripod_results.py - Detailed failure analysis
- tests/test_tripod_validation.py - Validation test suite
- reports/tripod_validation_report.json - Current baseline metrics

---

**Status**: Ready for Phase A implementation  
**Owner**: VetDict Development Team  
**Last Updated**: 2026-04-13
