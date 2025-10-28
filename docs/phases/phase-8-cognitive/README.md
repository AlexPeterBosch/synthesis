# Phase 8: Cognitive Variability Analysis

**Duration:** 1.5 weeks  
**Complexity:** 6/10

## Overview

Implement cognitive state classifier with exact thresholds.

## Deliverables

- [ ] cognitive_analyzer.py
- [ ] State classifier (4 states)
- [ ] Immunity calculator
- [ ] Influence entropy
- [ ] Recommendations engine

## Critical Specifications

**States:**
- Biased: mod<0.4, ent<0.5 → 80% explore
- Focused: mod<0.4, dens>0.7 → 30% explore
- Diversified: 0.4≤mod≤0.7, 0.4≤ent≤0.7 → 50% explore (OPTIMAL)
- Dispersed: mod>0.7, ent>0.7 → 20% explore

**Immunity:** modularity × entropy
- High: >0.28
- Medium: 0.16-0.28
- Low: <0.16

## Validation

- [ ] Thresholds exact
- [ ] Classifications correct
- [ ] Recommendations appropriate

## Reference

- Specifications: `specs/parameters.json` (cognitive section)