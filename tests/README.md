# Synthesis Tests

Comprehensive test suite for Synthesis system.

## Test Structure

### Unit Tests (`unit/`)
Test individual functions and classes in isolation.

### Integration Tests (`integration/`)
Test complete workflows and component interactions.

### Specification Tests (`specifications/`)
Validate that implementations match exact research specifications.

**Critical specification tests:**
- `test_ngram_weights.py` - Validates TWO-PASS algorithm with weights 3/2/1
- `test_node_sizing.py` - Validates LINEAR sizing (5-40 pixels)
- `test_gap_thresholds.py` - Validates all gap detection thresholds

### Fixtures (`fixtures/`)
Reusable test data and sample graphs.

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/specifications/test_ngram_weights.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run only specification tests
pytest tests/specifications/
```

## Test Requirements

All tests must:
1. Follow exact specifications from research
2. Use fixtures for consistency
3. Include docstrings explaining what is tested
4. Validate edge cases
5. Check for common mistakes (e.g., logarithmic instead of linear)

## Coverage Target

Minimum 80% code coverage required.

Critical modules requiring 100% coverage:
- nlp.ngram_generator
- graph.edge_calculator
- algorithms.betweenness
- gaps.gap_detector

## Specification Validation

Before marking any phase complete:
- ✅ All specification tests pass
- ✅ Manual validation against research specs
- ✅ No approximations or deviations
- ✅ Performance targets met
