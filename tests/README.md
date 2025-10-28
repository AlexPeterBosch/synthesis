# Synthesis Tests

Comprehensive test suite for Synthesis knowledge graph system.

## Test Structure

### Unit Tests (`tests/unit/`)
Tests for individual components in isolation.

### Integration Tests (`tests/integration/`)
Tests for combined functionality across modules.

### Specification Tests (`tests/specifications/`)
Validation tests ensuring exact compliance with research specifications.
- `test_ngram_weights.py` - N-gram weight calculations
- `test_node_sizing.py` - Node sizing formulas
- `test_gap_thresholds.py` - Gap detection thresholds

### Fixtures (`tests/fixtures/`)
Test data and sample files.

## Running Tests

```bash
# Run all tests
pytest

# Run specific test category
pytest tests/unit/
pytest tests/specifications/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/specifications/test_ngram_weights.py
```

## Test Requirements

All tests must:
1. Follow exact specifications from research
2. Validate against specs/validation-rules.json
3. Achieve 100% pass rate before phase completion
4. Include clear documentation

## Critical Tests

The specification tests are **critical** and enforce:
- Exact n-gram weights (3/2/1)
- Linear node sizing (5 + BC×35)
- Gap detection thresholds (min 3, max 6 hops, <10% density)
- No approximations allowed
