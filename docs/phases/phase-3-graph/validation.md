# Phase 3 Validation

## Weight Accumulation Test

```python
# Input n-grams
ngrams = [
    ("ai", "tool", 3),
    ("ai", "tool", 3),  # Same pair twice
    ("ai", "data", 2)
]

# Expected edge weights
# ai-tool: 3 + 3 = 6 (NOT normalized!)
# ai-data: 2
```

## Validation Commands

```bash
pytest src/graph/tests/test_weight_accumulation.py
```

## Success Criteria

Edge weights are raw sums, no normalization applied.