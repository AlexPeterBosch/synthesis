# Phase 8 Validation

## Threshold Verification

```python
# Biased
assert modularity_max == 0.4
assert entropy_max == 0.5
assert explore_ratio == 80

# Focused
assert modularity_max == 0.4
assert density_min == 0.7
assert explore_ratio == 30

# Diversified (OPTIMAL)
assert 0.4 <= modularity <= 0.7
assert 0.4 <= entropy <= 0.7
assert explore_ratio == 50

# Dispersed
assert modularity_min == 0.7
assert entropy_min == 0.7
assert explore_ratio == 20

# Immunity
assert formula == "modularity * entropy"
assert high_threshold == 0.28
assert medium_threshold == 0.16
```

## Success Criteria

All thresholds exact, classifications accurate.