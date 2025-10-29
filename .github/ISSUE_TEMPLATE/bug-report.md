---
name: Bug Report
about: Report a bug or unexpected behavior
title: '[BUG] Brief description'
labels: bug
assignees: ''
---

## Bug Description

**Brief Summary:**  
[Clear and concise description of the bug]

**Phase/Component:**  
[e.g., Phase 2 - NLP Processing, Phase 4 - Louvain Algorithm]

## Expected Behavior

[What should happen]

## Actual Behavior

[What actually happens]

## Steps to Reproduce

1. [First step]
2. [Second step]
3. [Third step]

## Environment

- **OS:** [e.g., Ubuntu 24.04, macOS 14]
- **Python Version:** [e.g., 3.10.12]
- **Node Version:** [e.g., 18.17.0]
- **PostgreSQL Version:** [e.g., 15.4]
- **Branch:** [e.g., main, feature/phase-2]

## Code Example

```python
# Minimal code that reproduces the issue
def example():
    pass
```

## Error Messages

```bash
# Full error traceback
Traceback (most recent call last):
  ...
```

## Specification Deviation?

- [ ] This bug represents a deviation from specs/parameters.json
- [ ] This bug represents incorrect algorithm implementation
- [ ] This bug is unrelated to specifications

**If specification deviation, provide details:**
- **Parameter affected:** [e.g., node_sizing formula]
- **Expected value:** [e.g., LINEAR: 5 + (bc_normalized * 35)]
- **Actual implementation:** [e.g., Using logarithmic scaling]

## Impact

**Severity:**  
- [ ] Critical - System broken
- [ ] High - Major functionality affected
- [ ] Medium - Minor functionality affected
- [ ] Low - Cosmetic issue

**Affected Features:**
- [List features affected]

## Possible Solution

[If you have ideas about how to fix this]

## Additional Context

[Any other context about the problem]

## Screenshots/Logs

[If applicable, add screenshots or log files]

---

**For Maintainers:**
- [ ] Bug confirmed
- [ ] Specification checked
- [ ] Fix assigned to: @username
- [ ] Priority set