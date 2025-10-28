# Phase 3: Graph Construction

**Duration:** 2 weeks  
**Complexity:** 7/10

## Overview

Build graph construction engine with ADDITIVE edge weighting (NO normalization).

## Deliverables

- [ ] graph_builder.py with GraphBuilder class
- [ ] build_from_ngrams() method
- [ ] export_to_database() using Prisma
- [ ] Edge weight accumulation
- [ ] Tests

## Critical Specifications

**Edge Weight Formula:** ADDITIVE (NO normalization!)
```python
edge_weight = sum(all co-occurrence weights)
# If appears 5x as bigram: 3+3+3+3+3 = 15
# NO division by max, total, or degree!
```

## Validation

- [ ] Weights accumulate correctly
- [ ] No normalization applied
- [ ] Graph exports to database
- [ ] Node/edge deduplication works

## Reference

- Specifications: `specs/parameters.json` (graph section)