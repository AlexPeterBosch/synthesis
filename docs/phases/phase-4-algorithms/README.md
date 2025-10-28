# Phase 4: Core Algorithms

**Duration:** 3 weeks  
**Complexity:** 8/10

## Overview

Implement Louvain, ForceAtlas2, Betweenness, Modularity with EXACT parameters.

## Deliverables

- [ ] louvain.py (resolution=1.0)
- [ ] forceatlas2.py (gravity=1.0, scalingRatio=20.0)
- [ ] betweenness.py (Brandes, weighted)
- [ ] modularity.py (Newman-Girvan weighted)
- [ ] Community color assignment (HSL)
- [ ] BC-to-size conversion (LINEAR 5-40px)

## Critical Specifications

**Louvain:** resolution=1.0, weighted=True  
**ForceAtlas2:** gravity=1.0, scalingRatio=20.0, linLogMode=False  
**Node Sizing:** LINEAR (NOT logarithmic!)  
```python
size = 5 + (bc_normalized * 35)  # 5-40 pixels
```

## Validation

- [ ] Modularity >0.4 for typical texts
- [ ] Node sizes 5-40 pixels
- [ ] Communities colored distinctly
- [ ] Layout converges

## Reference

- Specifications: `specs/parameters.json` (algorithms section)