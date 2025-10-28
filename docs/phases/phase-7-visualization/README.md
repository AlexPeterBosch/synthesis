# Phase 7: Visualization

**Duration:** 2 weeks  
**Complexity:** 7/10

## Overview

Build React + Sigma.js frontend with exact visualization specifications.

## Deliverables

- [ ] GraphVisualization.jsx component
- [ ] Sigma.js configuration
- [ ] Node sizing (5-40px LINEAR)
- [ ] Edge thickness by weight
- [ ] Community colors
- [ ] API integration

## Critical Specifications

**Node Sizing:** LINEAR (5-40 pixels)
```javascript
size = 5 + (bc_normalized * 35)
```

**Labels:** Show only for nodes >20px (top 30%)

**Edge Thickness:** `Math.log(weight + 1)`

## Validation

- [ ] Graph renders smoothly (60 FPS)
- [ ] Node sizes correct
- [ ] Colors match communities
- [ ] Zoom/pan working

## Reference

- Specifications: `specs/parameters.json` (visualization section)