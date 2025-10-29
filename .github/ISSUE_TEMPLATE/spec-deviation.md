---
name: Specification Deviation
about: Report implementation that deviates from research specifications
title: '[SPEC] Component - Deviation Description'
labels: specification-deviation, high-priority
assignees: ''
---

## ⚠️ CRITICAL: Specification Deviation Detected

**Component:** [e.g., NLP Processor, Louvain Algorithm, Node Sizing]  
**File(s):** [e.g., src/nlp/ngram_generator.py, src/algorithms/louvain.py]  
**Discovered:** [YYYY-MM-DD]

## Specification Reference

**Source Document:**  
- [ ] specs/parameters.json
- [ ] SPECIFICATIONS.md
- [ ] docs/research/development-plan-part1.md
- [ ] docs/research/development-plan-part2.md

**Relevant Specification:**
```json
{
  "parameter": "value",
  "from": "specs/parameters.json"
}
```

## Deviation Details

### What the Specification Says
[Exact text from specification documents]

**Expected Implementation:**
```python
# What the code SHOULD look like
def correct_implementation():
    # According to research: LINEAR scaling
    size = 5 + (bc_normalized * 35)
    return size
```

### What the Code Actually Does
[Describe current implementation]

**Actual Implementation:**
```python
# What the code ACTUALLY does
def current_implementation():
    # WRONG: Using logarithmic scaling
    size = 5 + math.log(bc_normalized * 35)
    return size
```

## Impact Analysis

**Severity:**
- [ ] CRITICAL - Completely breaks specification (e.g., additive→normalized weights)
- [ ] HIGH - Major deviation (e.g., linear→logarithmic scaling)
- [ ] MEDIUM - Parameter value wrong (e.g., resolution=1.2 instead of 1.0)
- [ ] LOW - Minor deviation with minimal impact

**Affected Components:**
- [List all components affected by this deviation]

**Downstream Effects:**
- [How this affects other parts of the system]

## Specification Validation

Run validation script:
```bash
python scripts/check-specs.py --component [component_name]
```

**Validation Results:**
```
❌ FAILED: Parameter X does not match specification
   Expected: [value from spec]
   Found: [value in code]
```

## Why This Deviation Occurred

**Root Cause:**
- [ ] Approximation used (NOT ALLOWED)
- [ ] Misunderstanding of specification
- [ ] Typo in implementation
- [ ] Specification not consulted
- [ ] Other: [describe]

## Correction Required

**Steps to Fix:**
1. [First step to correct the code]
2. [Second step]
3. [Verify with validation script]
4. [Update tests]

**Modified Files:**
- `path/to/file1.py`
- `path/to/file2.py`

## Testing Requirements

Before closing this issue:
- [ ] Spec validation passes 100%
- [ ] Unit tests updated and passing
- [ ] Integration tests passing
- [ ] Specification tests passing (tests/specifications/)
- [ ] Manual verification performed

## Research Cross-Reference

**Research Questions Answered:**
- [e.g., Q16: Node sizing is LINEAR, not logarithmic]
- [e.g., Q8: Edge weights are ADDITIVE, not normalized]

**Research Source:**
- [Link to specific section in research documentation]

## Prevention

**How to prevent similar deviations:**
- [ ] Add specification test for this parameter
- [ ] Update validation rules
- [ ] Document in SPECIFICATIONS.md
- [ ] Add to scripts/check-specs.py

---

## ⚠️ REMINDER: NO APPROXIMATIONS ALLOWED

All implementations MUST use EXACT values from:
- specs/parameters.json
- SPECIFICATIONS.md  
- Research documentation

**Zero tolerance for:**
- Approximations (e.g., 1.0 → 1.2)
- "Improvements" (e.g., linear → logarithmic)
- Deviations "for performance"
- Undocumented changes

---

**For Maintainers:**
- [ ] Deviation confirmed
- [ ] Specification verified
- [ ] Fix prioritized
- [ ] Assigned to: @username
- [ ] Timeline: [date]