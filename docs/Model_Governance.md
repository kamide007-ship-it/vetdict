# ShowDog Analysis Platform - Model Governance

**Version:** 1.0.0
**Effective Date:** 2026-02-06
**Authority:** ShowDog Analysis Platform Development Team
**Classification:** Governance Policy Document

---

## 1. Purpose

This document establishes the governance framework for:
- Algorithm version control
- Model version control
- Change management procedures
- Audit and compliance requirements

---

## 2. Version Control Requirements

### 2.1 Algorithm Versioning

Algorithm versions follow Semantic Versioning (SemVer):

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes to scoring logic
MINOR: New features, backward compatible
PATCH: Bug fixes, no logic changes
```

**Current Version:** `1.0.0`

### 2.2 Model Versioning

Model versions track the AI model used for feature detection:

```
Format: MODEL_NAME-YYYYMMDD

Example: gpt-4o-20260206
```

### 2.3 Weights Hash

A SHA256 hash of the weights dictionary MUST be computed and logged:

```python
weights_hash = sha256(json.dumps(WEIGHTS, sort_keys=True))
```

This hash serves as a tamper-detection mechanism.

---

## 3. Change Management

### 3.1 Prohibited Changes

The following changes are **STRICTLY PROHIBITED** without formal review:

1. **Weight modifications** - Any change to axis weights
2. **Axis additions/removals** - Changing the evaluation axes
3. **Score calculation formula** - Modifying how final score is computed
4. **Age adjustment table** - Changing age-based adjustments
5. **Grade boundaries** - Modifying score-to-grade mapping

### 3.2 Change Request Process

All algorithm changes MUST follow this process:

1. **Proposal** - Document the proposed change with rationale
2. **Review** - Technical and veterinary review
3. **Testing** - Regression testing on historical data
4. **Approval** - Formal approval by authorized personnel
5. **Implementation** - New version deployment
6. **Documentation** - Update Algorithm_Declaration.md

### 3.3 Emergency Changes

Emergency changes (critical bug fixes) may bypass full review but MUST:
- Be documented within 24 hours
- Receive retroactive review within 7 days
- Not affect scoring logic unless absolutely necessary

---

## 4. Audit Requirements

### 4.1 Per-Analysis Audit Log

Every analysis MUST record:

| Field            | Description                    | Required |
|------------------|--------------------------------|----------|
| analysis_id      | Unique identifier              | Yes      |
| timestamp        | ISO 8601 datetime              | Yes      |
| algorithm_version| Current algorithm version      | Yes      |
| model_version    | AI model version used          | Yes      |
| weights_hash     | SHA256 hash of weights         | Yes      |
| input_type       | "photo" or "video" or "both"   | Yes      |
| axis_scores      | JSON object of all axis scores | Yes      |
| final_score      | Calculated final score         | Yes      |
| grade            | Assigned grade                 | Yes      |

### 4.2 Audit Log Retention

- **Minimum retention:** 7 years
- **Storage:** Secure, append-only database table
- **Access:** Read-only for audit purposes

### 4.3 Audit Log Integrity

Audit logs MUST NOT be:
- Modified after creation
- Deleted under normal circumstances
- Accessible for modification via API

---

## 5. Reproducibility Requirements

### 5.1 Determinism Guarantee

The scoring system MUST be deterministic:

```
f(input, version) = output

Where:
- Same input + same version = same output (always)
- No random number generation in scoring
- No external dependencies that vary
```

### 5.2 Reproducibility Verification

Periodic verification MUST be performed:

1. Select random historical analyses
2. Re-run scoring with recorded axis scores
3. Verify final score matches recorded value
4. Report any discrepancies as critical issues

---

## 6. AI Model Governance

### 6.1 Model Selection

AI models used for feature detection MUST:
- Be documented with exact version/date
- Be stable and reproducible
- Not introduce randomness into scoring

### 6.2 Model Output Handling

AI outputs are treated as **suggestions only**:
- Axis scores from AI are validated
- Scores are clamped to valid range (0-100)
- Final calculation uses deterministic algorithm

### 6.3 Model Change Procedure

When changing AI models:

1. Document the change with rationale
2. Test on representative sample
3. Verify scoring consistency
4. Update model_version string
5. Deploy with new model version

---

## 7. Compliance Monitoring

### 7.1 Automated Checks

The system MUST automatically verify:
- Weights hash matches expected value
- Algorithm version is valid
- All required audit fields are populated

### 7.2 Manual Audits

Quarterly audits MUST verify:
- Reproducibility of historical scores
- Integrity of audit logs
- Compliance with this governance document

---

## 8. Incident Response

### 8.1 Scoring Discrepancy

If a scoring discrepancy is detected:

1. **Isolate** - Identify affected analyses
2. **Investigate** - Determine root cause
3. **Document** - Record findings
4. **Remediate** - Fix if algorithm bug
5. **Notify** - Inform affected users if necessary

### 8.2 Non-Retroactive Principle

**Past scores are NEVER recalculated retroactively.**

If an algorithm bug is found:
- Fix applies to future analyses only
- Historical scores remain unchanged
- Documentation notes the issue period

---

## 9. Roles and Responsibilities

### 9.1 Algorithm Owner
- Approves algorithm changes
- Reviews governance compliance
- Signs off on version releases

### 9.2 Technical Team
- Implements algorithm changes
- Maintains audit logging
- Monitors system health

### 9.3 Veterinary Advisor
- Reviews medical/scientific rationale
- Validates FCI standard compliance
- Advises on evaluation criteria

---

## 10. Version History

| Version | Date       | Changes |
|---------|------------|---------|
| 1.0.0   | 2026-02-06 | Initial governance document |

---

*This document is subject to the same change management process it defines.*
