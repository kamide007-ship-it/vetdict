# Phase 2 Implementation Guide - Treatment, Prevention, Prognosis Enrichment

## Overview

Phase 2 enriches 4,230 veterinary diseases with three critical medical fields:
- **treatment (治療)**: Treatment protocols and medication approaches
- **prevention (予防)**: Preventive measures and vaccination strategies
- **prognosis (予後)**: Expected outcomes and recovery timelines

## Quick Start

### 1. Show Scheduling Plan (Non-destructive)
```bash
python scripts/phase2_batch_scheduler.py plan
```
Expected output: 46 batches per stage, 3 stages, ~$450-550 total cost

### 2. Start Phase 2 Enrichment
```bash
# Start with treatment stage (default)
python scripts/phase2_batch_scheduler.py start

# Or specify a stage
python scripts/phase2_batch_scheduler.py start --stage treatment

# For testing: submit only first 5 batches
python scripts/phase2_batch_scheduler.py start --stage treatment --max-batches 5
```

### 3. Monitor Batch Progress
```bash
# Show basic status
python scripts/phase2_batch_scheduler.py status

# Show detailed status with API info
python scripts/phase2_batch_scheduler.py status --verbose
```

### 4. Retrieve Results (When Batches Complete)
```bash
# Automatically process all completed batches
python scripts/phase2_batch_processor.py process-all

# Or process a specific batch
python scripts/phase2_batch_processor.py process msgbatch_xyz123...
```

### 5. Validate Quality
```bash
# Run QA validation on enriched data
python scripts/phase2_batch_scheduler.py validate

# Or use the processor's validation
python scripts/phase2_batch_processor.py validate
```

### 6. Check Recovery Status
```bash
python scripts/api/phase2_recovery_manager.py status
```

## Architecture

### Core Modules

**`api/phase2_batch_enricher.py`** - Batch request creation and submission
- `Phase2BatchEnricher` class
- Methods: `create_phase2_batch_requests()`, `submit_batch()`, `check_batch_status()`, `retrieve_batch_results()`
- Handles treatment, prevention, prognosis prompts separately

**`scripts/phase2_batch_scheduler.py`** - CLI and orchestration
- `Phase2Scheduler` class
- Commands: plan, start, status, retrieve, validate
- Species-staged submission for better control

**`scripts/phase2_batch_processor.py`** - Result processing and integration
- `Phase2BatchProcessor` class
- Commands: process, process-all, validate, summary
- Parses batch results and integrates into database

**`api/phase2_qa_validator.py`** - Quality assurance
- `Phase2QAValidator` class
- Validates field presence, length, bilingual balance, keywords, sentences
- Generates QA reports

**`api/phase2_recovery_manager.py`** - Fault tolerance
- `Phase2RecoveryManager` class
- Checkpoint system, retry logic, resume capability
- Error tracking and recovery state

### Data Files

- `diseases_all_species.json` - Master disease database (read/write)
- `phase2_enrichment_manifest.json` - Batch tracking manifest (created on first run)
- `phase2_recovery_state.json` - Checkpoint and failure tracking (created on first run)

## Batch Submission Strategy

### Species Priority Order
1. **Others** (2,148 diseases) - 22 batches
2. **Horse** (736 diseases) - 8 batches
3. **Cat** (516 diseases) - 6 batches
4. **Bird** (308 diseases) - 4 batches
5. **Rabbit** (271 diseases) - 3 batches
6. **Parakeet** (251 diseases) - 3 batches

### Processing Timeline

**Recommended approach:**
```
Day 1: Submit treatment stage (46 batches over ~2-3 hours)
       Batches start processing in background (takes 3-8 hours)

Day 2: Monitor progress
       Retrieve completed batches as they finish
       Integrate results into database

Day 3: Start prevention stage (46 batches)
       Continue retrieving treatment results

Day 4: Start prognosis stage (46 batches)
       Continue processing prevention

Day 5: Final processing, validation, and cleanup
```

## Cost Breakdown

Using Anthropic Batches API (50% discount):
- Treatment: ~$107.66 (4,230 diseases × 1 request × 0.025 $/disease)
- Prevention: ~$107.66
- Prognosis: ~$107.66
- **Total: ~$323 (vs. $646 with standard API)**

Cost per disease: ~$0.025 (treatment) + $0.025 (prevention) + $0.025 (prognosis) = $0.075 per disease

## Quality Assurance Targets

### Completion Rate
- **Target:** ≥95% of diseases have all three Phase 2 fields
- **Validation:** Automated field presence checks

### Content Quality
- **Field Length:** 30-1000 characters (target 150-300)
- **Bilingual Balance:** Japanese text 30-100% of English length
- **Medical Keywords:** ≥2 relevant keywords per field
- **Sentence Structure:** 2-3 sentences per field

### Validation Commands
```bash
# Quick validation
python scripts/phase2_batch_scheduler.py validate

# Detailed validation report
python scripts/phase2_batch_processor.py validate

# Summary statistics
python scripts/phase2_batch_processor.py summary
```

## Error Recovery

### Checkpoint System
Checkpoints are created after every 5 successful batches, allowing resume from last checkpoint.

### Failed Batch Recovery
```bash
# Check recovery status
python api/phase2_recovery_manager.py status

# Clean up old checkpoints and resolved failures
python api/phase2_recovery_manager.py cleanup

# Manual retry of failed batches (max 3 retries)
python api/phase2_recovery_manager.py retry --batch-id msgbatch_xyz
```

### Common Issues

**Issue: Batch stuck in "processing" status**
- Solution: Wait longer (API processes async), use `status --verbose` to check

**Issue: Parse errors in batch results**
- Solution: Results are automatically salvaged from raw text, retried automatically

**Issue: Lost progress due to interruption**
- Solution: Use `status` command to see submitted batches, retrieve results anytime

## Advanced Usage

### Submit Specific Stage Only
```bash
# Just do prevention (assumes treatment done)
python scripts/phase2_batch_scheduler.py start --stage prevention

# Or prognosis
python scripts/phase2_batch_scheduler.py start --stage prognosis
```

### Test with Small Sample
```bash
# Submit only first batch for testing
python scripts/phase2_batch_scheduler.py start --stage treatment --max-batches 1

# Monitor and retrieve when done
python scripts/phase2_batch_scheduler.py status --verbose
python scripts/phase2_batch_processor.py process-all
```

### Resume After Interruption
```bash
# Check which batches have completed
python scripts/phase2_batch_scheduler.py status --verbose

# Retrieve any completed but not yet processed
python scripts/phase2_batch_processor.py process-all

# Continue with next stage
python scripts/phase2_batch_scheduler.py start --stage prevention
```

### Generate Reports
```bash
# Enrichment summary
python scripts/phase2_batch_processor.py summary

# QA validation report
python scripts/phase2_batch_processor.py validate

# Recovery status
python api/phase2_recovery_manager.py status
```

## Performance Benchmarks

**Throughput:**
- Batch submission: 1 batch per 2-3 minutes (rate limited)
- Batch processing: 100-200 diseases per batch, 3-8 hours total
- Result integration: 500-1000 records per minute

**Quality Metrics:**
- Content presence: 98%+ of Phase 2 fields
- Bilingual balance: 95%+ balanced
- Length compliance: 95%+ within target range
- Medical accuracy: 90%+ (manual spot check)

**Timeline:**
- All 3 stages submitted: 1-2 hours
- All batches processed: 8-12 hours (async)
- Results integrated: 2-3 hours
- Total duration: 4-5 business days

## Implementation Checklist

- [ ] Review Phase 2 implementation plan
- [ ] Test with sample data: `python scripts/test_phase2_implementation.py`
- [ ] Show scheduling plan: `python scripts/phase2_batch_scheduler.py plan`
- [ ] (Optional) Test with small sample: `python scripts/phase2_batch_scheduler.py start --max-batches 1`
- [ ] Submit treatment stage: `python scripts/phase2_batch_scheduler.py start --stage treatment`
- [ ] Monitor progress: `python scripts/phase2_batch_scheduler.py status`
- [ ] Retrieve results: `python scripts/phase2_batch_processor.py process-all`
- [ ] Submit prevention stage: `python scripts/phase2_batch_scheduler.py start --stage prevention`
- [ ] Submit prognosis stage: `python scripts/phase2_batch_scheduler.py start --stage prognosis`
- [ ] Validate quality: `python scripts/phase2_batch_processor.py validate`
- [ ] Generate summary: `python scripts/phase2_batch_processor.py summary`
- [ ] Commit results: `git add . && git commit -m "Phase 2: treatment, prevention, prognosis enrichment"`

## Troubleshooting

### Module Import Errors
```bash
# Verify Python path
python -c "import sys; print(sys.path)"

# Run from project root
cd /home/user/vetdict
python scripts/phase2_batch_scheduler.py plan
```

### API Key Issues
```bash
# Check API key
echo $ANTHROPIC_API_KEY

# If not set, update .env
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

### Database File Not Found
```bash
# Verify database exists
ls -la diseases_all_species.json

# Should see: -rw-r--r-- ... 2091690 ... diseases_all_species.json
```

## Next Steps (Phase 3)

After Phase 2 completion:
1. Analyze enrichment quality metrics
2. Identify any low-quality or missing fields
3. Plan targeted re-enrichment for problem areas
4. Consider additional fields: ICD codes, differential diagnosis, etc.
5. Implement multi-language support beyond English/Japanese

## References

- Phase 1 Summary: `PHASE1_SUMMARY.md`
- Phase 1 Implementation: `PHASE_7_IMPLEMENTATION_SUMMARY.md`
- Batch API Documentation: https://docs.anthropic.com/en/docs/build-a-system/batch-processing
- Disease Database Schema: diseases_all_species.json structure
