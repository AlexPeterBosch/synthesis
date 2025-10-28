# Phase 6: GraphRAG Implementation

**Duration:** 3 weeks  
**Complexity:** 9/10

## Overview

Build n8n GraphRAG workflow with 2-hop subgraph extraction and AI integration.

## Deliverables

- [ ] Complete n8n workflow JSON
- [ ] Query tokenization
- [ ] Subgraph extraction (2-hop)
- [ ] Context builder
- [ ] Claude integration
- [ ] Gap bridging workflow

## Critical Specifications

**Workflow Steps:**
1. Tokenize query
2. Find overlapping nodes
3. Extract 2-hop neighborhood
4. Build context (top 10 concepts, top 15 relations, top 5 gaps)
5. Send to Claude
6. Return insights

## Validation

- [ ] Workflow imports to n8n
- [ ] Query processing works
- [ ] Context properly formatted
- [ ] AI responds with insights

## Reference

- Specifications: `specs/parameters.json` (graphrag section)
- Development Plan: `docs/research/development-plan-part2.md`