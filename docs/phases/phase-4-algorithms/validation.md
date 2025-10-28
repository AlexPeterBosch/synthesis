# Phase 4 Validation

## Parameter Verification

```python
# Louvain
assert resolution == 1.0
assert weighted == True

# ForceAtlas2
assert gravity == 1.0
assert scalingRatio == 20.0
assert linLogMode == False

# Node sizing (CRITICAL!)
assert formula == "5 + (bc_normalized * 35)"
assert NOT using math.log()  # Must be LINEAR!
```

## Validation Commands

```bash
pytest src/algorithms/tests/test_node_sizing.py
pytest src/algorithms/tests/test_modularity.py
```

## Success Criteria

All parameters match specs/parameters.json exactly.