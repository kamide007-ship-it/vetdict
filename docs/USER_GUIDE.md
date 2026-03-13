# Multi-Disease Diagnostic System - User Guide

## For Veterinary Professionals

**Version**: 1.0.0
**Date**: 2024-03-13

---

## Introduction

The Multi-Disease Diagnostic System is a clinical decision support tool that helps veterinarians identify potential disease combinations when presented with complex symptom presentations.

### What It Does

✅ Identifies when multiple diseases might be present
✅ Highlights ambiguous symptoms that are difficult to differentiate
✅ Calculates probability of different diagnoses
✅ Generates clarifying questions to narrow the differential
✅ Provides confidence scores for diagnosis combinations

### What It Does NOT Do

❌ Make definitive diagnoses
❌ Replace clinical examination
❌ Triage patients
❌ Determine treatment
❌ Substitute for professional judgment

---

## Getting Started

### 1. Access the System

Navigate to the diagnostic interface in Vet Dict:
- Main URL: `https://vetdict.example.com/`
- Diagnosis Section: Select species → Symptom entry

### 2. Select Species

Click the appropriate species icon:
- 🐕 Dog
- 🐈 Cat
- 🐴 Horse
- 🐰 Rabbit
- Other (available species)

### 3. Enter Symptoms

#### Method A: Checkbox Selection
- Browse symptom list by category
- Click symptoms as you identify them
- Selected symptoms appear in "Selected Symptoms" area

#### Method B: Search
- Type symptom name in search box
- Results filter as you type
- Click to add matching symptom

#### Method C: Description
- Provide written symptom description
- System helps identify relevant symptoms
- Suggests additional symptoms to consider

### 4. Review Initial Assessment

The system shows:
- Number of symptoms entered
- Single vs. multi-disease mode indication
- Any obvious high-confidence diagnoses

---

## Understanding Multi-Disease Mode

### When It Activates

Multi-disease mode appears when:
✓ 2+ symptoms entered
✓ 2+ diseases have significant likelihood
✓ Symptoms overlap between diseases
✓ Ambiguity is present

Visual Indicator: **🔍 Multi-Disease Mode Active** (blue badge)

### What You See

```
┌─────────────────────────────────────┐
│ 🔍 Multi-Disease Mode Active       │
├─────────────────────────────────────┤
│ ⚕ Possible Disease Combinations:    │
│                                     │
│ ▶ Hip Dysplasia + Osteoarthritis   │
│   Confidence: 72%  [████████░░]    │
│   Shared symptoms: 3               │
│                                     │
│ ▶ Osteoarthritis + Injury          │
│   Confidence: 58%  [██████░░░░]    │
│   Shared symptoms: 2               │
└─────────────────────────────────────┘
```

### Disease Combinations

Each combination shows:

| Element | Meaning |
|---------|---------|
| Disease names | Conditions that might occur together |
| Confidence % | Probability this combination is present |
| Confidence bar | Visual representation of probability |
| Shared symptoms | How many symptoms appear in both diseases |

**Interpretation**:
- **70%+**: Strong likelihood (pursue diagnosis)
- **50-70%**: Moderate likelihood (needs clarification)
- **<50%**: Low likelihood (but possible)

---

## Ambiguity Analysis

### What It Shows

```
┌─────────────────────────────────────┐
│ ⚠ Ambiguous Symptoms Detected      │
├─────────────────────────────────────┤
│ limping (⭕ 80)                     │
│ pain    (⭕ 75)                     │
│                                     │
│ Recommendations:                    │
│ • Assess gait abnormality pattern   │
│ • Palpate joints for response       │
│ • Consider orthopedic imaging       │
└─────────────────────────────────────┘
```

### Understanding Ambiguity Scores

The circle with number indicates:
- **80**: 80% of disease candidates have this symptom
- **50**: 50% of candidates have this symptom
- **20**: Only 20% of candidates have this symptom

**Higher scores** = More ambiguous (less differentiating)
**Lower scores** = More specific (more diagnostic)

### How to Address Ambiguity

1. **Ask clarifying questions** (system provides these)
2. **Perform specific tests** (system may recommend)
3. **Physical examination** focus on:
   - Specific physical signs of each disease
   - Severity and distribution patterns
   - Associated findings

---

## Clarifying Questions

### Purpose

Questions help differentiate between similar diagnoses by:
- Testing specific features of each disease
- Assessing symptom nuances
- Gathering disease-specific information
- Reducing diagnostic uncertainty

### Example

**Question**: "Is pain worse after rest or after exercise?"

**Why**:
- Osteoarthritis worsens with activity
- Hip dysplasia worsens with rest initially
- Answer helps differentiate the two

**How to Answer**:
- Based on owner observation
- Consider recent changes
- Note response over time

### Responding to Questions

1. Read the question carefully
2. Select or type your answer
3. System updates probability calculations
4. New questions generated based on answers
5. Continue until confident

---

## Confidence Breakdown

### What It Shows

```
┌──────────────────────────────────────┐
│ 📊 Confidence Analysis               │
├──────────────────────────────────────┤
│ Hip Dysplasia:    68% [████████░░░░] │
│ Osteoarthritis:   72% [█████████░░░] │
│ Ligament Injury:  34% [███░░░░░░░░░] │
│                                      │
│ Final Combined:   70% [███████░░░░░] │
└──────────────────────────────────────┘
```

### Interpreting Percentages

Each disease shows individual confidence, plus final combination score.

**Decision Guide**:
```
Combined Score: 70%

Interpretation:
→ Two diseases likely occurring together
→ Requires both to be treated
→ Diagnostic tests should confirm both
→ Treatment plan must address both
→ Prognosis affected by both conditions
```

---

## Decision Making Guide

### Confidence 70-100%: High Likelihood

✓ **Action**: Pursue diagnosis aggressively
- Order confirmatory diagnostic tests
- Prepare treatment plan for both conditions
- Monitor for complications
- Brief owner on implications

✓ **Example**: Hip Dysplasia + Osteoarthritis (72%)
- Order hip radiographs + orthopedic evaluation
- Plan physical therapy + pain management
- Discuss long-term management
- Address both conditions in treatment

### Confidence 50-70%: Moderate Likelihood

⚠️ **Action**: Continue investigation
- Ask more clarifying questions
- Consider selective diagnostic testing
- Observe patient over time
- Prepare differential diagnosis list

⚠️ **Example**: Gastroenteritis + Pancreatitis (58%)
- Ask about vomit character, pain location
- Consider fecal analysis first
- May progress to lipase/amylase if needed
- Adjust diet cautiously to assess response

### Confidence <50%: Low Likelihood

❓ **Action**: Consider alternatives
- Don't assume this combination
- Explore other disease combinations
- Rule out more likely diagnoses first
- Return to this only if other tests negative

---

## Common Scenarios

### Scenario 1: Limping Dog

**Symptoms Entered**: Limping, pain, rear limb weakness

**System Response**:
- Multi-disease mode activated
- Combinations shown:
  - Hip Dysplasia + Osteoarthritis (72%)
  - Ligament injury alone (68%)

**Your Decision**:
1. Ask clarifying questions:
   - Onset gradual vs. sudden? (→ dysplasia = gradual)
   - Pain location front vs. rear? (→ hip = rear)
   - Swelling visible? (→ injury = yes)

2. Physical examination:
   - Ortolani test (hip dysplasia)
   - Drawer test (ACL injury)
   - Palpate for pain, swelling

3. Next steps:
   - If both likely: Radiographs + consider advanced imaging
   - If one likely: Targeted diagnostics
   - Follow-up examination if uncertain

### Scenario 2: Vomiting Cat

**Symptoms Entered**: Vomiting, diarrhea, lethargy

**System Response**:
- Combinations:
  - Gastroenteritis + Pancreatitis (62%)
  - Parasitic infection (58%)
  - Viral syndrome (71%)

**Your Decision**:
1. Ask questions about:
   - Vomit appearance (bile vs. undigested food)
   - Diarrhea character (bloody vs. normal)
   - Food intake (decreased vs. absent)

2. Physical examination:
   - Abdominal palpation (pain location)
   - Hydration status
   - Temperature (fever suggests infectious)

3. Diagnostics:
   - Baseline: Fecal exam, CBC
   - If needed: Pancreatitis markers, ultrasound
   - Culture if suspected infectious

---

## Best Practices

### ✓ DO

1. **Enter all relevant symptoms**
   - Even mild or incidental findings
   - Negative findings help exclude conditions

2. **Consider patient context**
   - Age, breed, medical history
   - Environmental exposures
   - Medication history
   - Vaccination status

3. **Use clarifying questions**
   - Answer thoughtfully based on observations
   - Ask owner for details if needed
   - Update information as you examine

4. **Verify with clinical examination**
   - Physical findings confirm/refute AI suggestions
   - Special orthopedic tests matter
   - Palpation findings are crucial

5. **Order confirmatory tests**
   - Don't rely on AI alone
   - Use tests to confirm suspected diagnoses
   - Rule out emergencies first

6. **Document your thinking**
   - Note why you accept/reject AI suggestions
   - Record clinical reasoning
   - Build knowledge from cases

### ❌ DON'T

1. **Don't use without clinical exam**
   - AI is supplementary only
   - Physical examination is essential
   - Visual/palpation findings override AI

2. **Don't skip rule-outs**
   - Always rule out emergencies
   - Don't miss life-threatening conditions
   - High confidence doesn't mean certainty

3. **Don't over-interpret low scores**
   - Low confidence doesn't mean wrong
   - Unusual presentations have low scores
   - Rare diseases naturally score low

4. **Don't rely on single AI output**
   - Ask follow-up questions
   - Incorporate all information
   - Update diagnosis as data changes

5. **Don't ignore conflicting signs**
   - Physical findings that contradict AI
   - Trust the examination
   - Modify AI interpretation accordingly

6. **Don't delay critical care**
   - If emergency suspected, treat first
   - Don't wait for AI confirmation
   - Patient welfare paramount

---

## Troubleshooting

### Problem: No Multi-Disease Mode Appearing

**Possible Causes**:
1. Need 2+ symptoms → Enter more
2. Need 2+ diseases → Add more suspected diagnoses
3. Single clear diagnosis → System shows best match instead

**Solution**: Enter additional symptoms to enable multi-disease comparison

### Problem: Confidence Scores Seem Wrong

**Possible Causes**:
1. Incomplete symptom list → Add missing findings
2. Patient context not entered → Add age, breed, history
3. Unusual presentation → System scores atypically
4. Data mismatch → Symptom may be miscategorized

**Solution**:
- Add more clinical information
- Review ambiguity section
- Ask clarifying questions
- Consult specialist if unsure

### Problem: Questions Don't Match My Case

**Possible Causes**:
1. Your suspected diagnoses differ from system
2. Symptom interpretation varies
3. Patient factors not captured in system
4. Unusual case variation

**Solution**:
- Ignore irrelevant questions
- Focus on high-ranking questions
- Use clinical judgment
- Adapt questions to your case

### Problem: System Suggests Unlikely Combination

**Possible Causes**:
1. Rare but real combination
2. Misinterpreted symptoms
3. Data entry error
4. System limitation

**Solution**:
1. Verify symptom entry
2. Check disease definitions match your interpretation
3. Trust clinical judgment if you disagree
4. Use feedback mechanism to report

---

## Feedback & Reporting

### How to Provide Feedback

**Positive Feedback**:
- Feature works well
- Accurate diagnosis
- Helpful suggestions

**Bug Reports**:
- Incorrect behavior
- Missing information
- Performance issues

**Medical Feedback**:
- Accuracy of disease combinations
- Appropriateness of questions
- Missing common diseases

### How to Report

1. Click "Feedback" button (if available)
2. Select feedback type
3. Describe your experience
4. Include case details (anonymized)
5. Submit

Your feedback helps improve the system!

---

## Support & Resources

### Getting Help

**System Issues**: support@vetdict.example.com
**Medical Questions**: veterinary@vetdict.example.com
**Technical Issues**: tech@vetdict.example.com

### Additional Resources

- API Documentation: `/docs/MULTIDISEASE_API.md`
- Deployment Guide: `/docs/DEPLOYMENT.md`
- Medical Validation: `/docs/MEDICAL_VALIDATION.md`
- System Architecture: GitHub repository

### Training

- Video tutorials available
- Case study examples
- Live demonstrations
- Q&A sessions

---

## Frequently Asked Questions

**Q: Can I trust the confidence scores completely?**
A: Use them as a guide, not absolute truth. Always verify with clinical examination and testing.

**Q: What if the system suggests something I disagree with?**
A: Trust your clinical judgment. The system is a tool to consider, not dictate diagnosis.

**Q: How often is the system updated?**
A: Medical knowledge is reviewed quarterly. Updates deployed as needed.

**Q: Is patient data private?**
A: Yes. No patient identifiers stored. Local analysis only (no cloud backup).

**Q: Can I use this for triage?**
A: No. Only use after proper examination. Triage requires direct assessment.

---

## Disclaimer

This system is a **clinical decision support tool** designed to assist veterinary professionals in diagnosis. It:

✓ Helps identify potential diagnoses
✓ Highlights diagnostic uncertainty
✓ Suggests questions to ask
✓ Provides additional perspective

It does NOT:

❌ Replace veterinary examination
❌ Provide definitive diagnosis
❌ Recommend specific treatments
❌ Substitute for professional judgment
❌ Determine medical necessity

**Always use professional veterinary judgment and perform appropriate clinical assessment.**

---

**For questions, contact: veterinary@vetdict.example.com**

**Last Updated**: 2024-03-13
**Version**: 1.0.0
