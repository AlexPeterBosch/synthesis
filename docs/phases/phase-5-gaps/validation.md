# Phase 5 Validation

## Threshold Verification

```python
assert MIN_COMMUNITY_SIZE == 3
assert MAX_PATH_LENGTH == 6
assert DENSITY_THRESHOLD == 0.1
assert MAX_SIZE_RATIO == 10
assert MIN_GAP_SCORE == 0.4
assert max_gaps_returned == 3
```

## Validation Commands

```bash
pytest src/gaps/tests/test_thresholds.py
pytest src/gaps/tests/test_filters.py
```

## Success Criteria

Gaps are meaningful, no false positives, thresholds exact.