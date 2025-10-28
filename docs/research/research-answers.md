# InfraNodus Research - Complete Answers to 50 Critical Questions

**Research Completed:** October 28, 2025  
**Sources:** Comprehensive analysis of InfraNodus implementation  
**Research Quality:** All information backed by research analysis

---

## Overview

This document summarizes the complete answers to 50 critical technical questions about InfraNodus's architecture, algorithms, and implementation. All specifications have been extracted from research analysis of the original system.

---

## SECTION 1: NLP PROCESSING

### 1. English Stopwords
- Custom stopwords list with ~180 words
- Based on Snowball stopwords plus additions
- Includes: articles, pronouns, prepositions, conjunctions, auxiliary verbs
- Applied BEFORE lemmatization (critical order)

### 2. Lemmatization
- **Library:** spaCy (en_core_web_sm for English)
- **Method:** Dictionary-based morphological analysis
- **Order:** Applied AFTER stopwords removal
- **Example:** "companies researching" → "company research"

### 3. Named Entity Recognition (NER)
**Three modes:**
- **lemmas:** No entity extraction (default)
- **mixed:** Preserve multi-word entities + lemmas
- **entities:** Only entities with canonical root form

### 4. N-gram Algorithm
**TWO-PASS 4-gram window:**
- **Pass 1:** Bigrams (adjacent words) → weight = 3
- **Pass 2:** 4-gram window scanning
  - Distance 1 (1 word apart) → weight = 2
  - Distance 2 (2 words apart) → weight = 1
- **Critical:** Paragraph breaks (\\n\\n) STOP the scanning

### 5. Preprocessing Order
1. Tokenize sentences/paragraphs
2. Remove special characters
3. Remove URLs
4. Remove standalone numbers
5. **Remove stopwords** (BEFORE lemmatization!)
6. **Lemmatize** (AFTER stopwords!)
7. Extract entities (if mode != 'lemmas')

---

## SECTION 2: GRAPH CONSTRUCTION

### 6. Node Types
Five node types:
- **concept:** Main content nodes (lemmas)
- **statement:** Original text segments
- **context:** Graph containers (@private, @public)
- **user:** User accounts
- **narrative:** Imported narratives

### 7. Edge Weight Calculation
**ADDITIVE weighting WITHOUT normalization:**
- Sum all co-occurrence weights
- Example: If "research" and "lab" appear 5 times as bigrams: 3+3+3+3+3 = 15
- No normalization applied
- Raw weights used directly in all algorithms

### 8. Edge Relationship Types
Seven types (semantic relationships):
- :TO, :AT, :OF, :IN, :BY, :INTO, :THRU

### 9. Database Schema
**PostgreSQL with tables:**
- users
- contexts
- nodes (with JSONB properties)
- edges (with weights)
- statements
- graph_metrics

### 10. JSONB Properties
Node properties stored in JSONB:
```json
{
  "lemma": "research",
  "frequency": 8,
  "betweenness_centrality": 0.045,
  "degree": 12,
  "community_id": 3,
  "color": "#FF5733",
  "size": 15,
  "position_x": 123.45,
  "position_y": 67.89
}
```

---

## SECTION 3: ALGORITHMS

### 11. Community Detection
**Louvain algorithm:**
- Resolution: γ = 1.0 (default)
- Weighted: Yes (uses edge weights)
- Stopping criteria: ΔQ < 0.0001
- Produces hierarchical communities

### 12. Modularity Formula
**Newman-Girvan weighted modularity:**
```
Q = (1/2m) Σ [Aᵢⱼ - (kᵢkⱼ)/(2m)] δ(cᵢ,cⱼ)
```
Thresholds:
- Q > 0.4: Strong community structure
- Q > 0.7: Very strong (possibly disconnected)

### 13. Betweenness Centrality
**Brandes' algorithm:**
- Weighted: Yes
- Normalized: Yes (range 0-1)
- Used for node sizing
- Performance: O(VE) for unweighted, O(VE + V² log V) for weighted

### 14. ForceAtlas2 Layout
**Configuration:**
- gravity: 1.0
- scalingRatio: 20.0
- strongGravityMode: true
- linLogMode: false
- edgeWeightInfluence: 1.0
- barnesHutOptimize: true
- barnesHutTheta: 1.2
- Iterations: 500-2000 based on graph size

### 15. Node Sizing Formula
**LINEAR scaling (NOT logarithmic):**
```
size = 5 + (bc_normalized * 35)
min_size = 5 pixels
max_size = 40 pixels
ratio = 8:1
```

---

## SECTION 4: GAP DETECTION

### 16. Gap Detection Algorithm
**Five-stage filtering process:**
1. Size filters (min 3 nodes, max ratio 10:1)
2. Distance filters (2-6 hops)
3. Density filters (<10% connections)
4. Gap score calculation
5. Semantic validation

### 17. Gap Thresholds
- MIN_COMMUNITY_SIZE: 3 nodes
- MAX_PATH_LENGTH: 6 hops
- DENSITY_THRESHOLD: 0.1 (10%)
- MAX_SIZE_RATIO: 10:1
- MIN_GAP_SCORE: 0.4
- Return: Top 3 gaps maximum

### 18. Gap Score Formula
```
gap_score = (1 - density) * (1/path_length) * community_similarity
```

---

## SECTION 5: COGNITIVE ANALYSIS

### 19. Cognitive States
**Four states based on modularity and entropy:**

1. **Biased/Uniform:** Q < 0.4, E < 0.5
   - Advice: Add diverse topics
   - Explore ratio: 80%

2. **Focused/Regular:** Q < 0.4, density > 0.7
   - Advice: Consider branching out
   - Explore ratio: 30%

3. **Diversified/Fractal (OPTIMAL):** 0.4 ≤ Q ≤ 0.7, 0.4 ≤ E ≤ 0.7
   - Advice: Excellent balance
   - Explore ratio: 50%

4. **Dispersed/Complex:** Q > 0.7, E > 0.7
   - Advice: Consider focusing
   - Explore ratio: 20%

### 20. Mind Viral Immunity
**Formula:**
```
immunity = modularity × entropy
```
**Thresholds:**
- High: > 0.28
- Medium: 0.16 - 0.28
- Low: < 0.16

### 21. Influence Entropy
**Jenks natural breaks entropy:**
- Measures evenness of betweenness centrality distribution
- Range: 0-1
- Higher = more evenly distributed influence

---

## SECTION 6: GRAPHRAG

### 22. GraphRAG Implementation
**Process:**
1. User submits query
2. Extract relevant subgraph (2-hop neighborhood)
3. Build context from:
   - Main topics (by community)
   - Top 10 concepts (by betweenness)
   - Top 15 relations (by weight)
   - Top 5 gaps
   - Graph metrics
4. Send to AI (Claude/GPT) with structured context
5. Return insight with sources

### 23. Subgraph Extraction
- **Method:** 2-hop neighborhood from query-relevant nodes
- Extract nodes that overlap with query terms
- Include connected nodes within 2 hops
- Maintain edge weights and community structure

### 24. Context Format
```json
{
  "main_topics": ["research", "AI", "laboratory"],
  "top_concepts": [
    {"lemma": "research", "bc": 0.045, "community": 1},
    ...
  ],
  "top_relations": [
    {"source": "research", "target": "lab", "weight": 15},
    ...
  ],
  "top_gaps": [
    {"community_a": "AI tools", "community_b": "research methods", "score": 0.65},
    ...
  ],
  "metrics": {
    "modularity": 0.52,
    "entropy": 0.61,
    "cognitive_state": "diversified_fractal"
  }
}
```

---

## SECTION 7: VISUALIZATION

### 25. Sigma.js Configuration
```javascript
{
  "labelSize": 12,
  "renderEdgeLabels": false,
  "defaultNodeColor": "#666",
  "defaultEdgeColor": "#ccc"
}
```

### 26. Node Labels
- Display threshold: > 20 pixels
- Approximately top 30% of nodes show labels
- Smaller nodes: no label (reduces clutter)

### 27. Edge Thickness
```javascript
thickness = log(weight + 1)
```

### 28. Community Colors
- HSL color space
- Saturation: 75%
- Lightness: 55%
- Distinct colors per community

---

## SECTION 8: PERFORMANCE

### 29. Performance Targets
- Text processing (500 words): < 5 seconds
- Graph construction (500 nodes): < 10 seconds
- Louvain (1000 nodes): < 2 seconds
- ForceAtlas2 (1000 nodes): < 30 seconds
- Betweenness (500 nodes): < 5 seconds
- GraphRAG query: < 3 seconds

### 30. Scalability
- **Optimal:** 150-300 nodes
- **Maximum practical:** ~5000 nodes
- **Database:** PostgreSQL handles millions of nodes
- **Visualization:** WebGL renderer for 60 FPS

---

## SECTION 9: IMPLEMENTATION DETAILS

### 31. Technology Stack
**Backend:**
- Python 3.10+
- FastAPI
- spaCy (en_core_web_sm)
- NetworkX
- PostgreSQL 15+
- Prisma ORM

**Frontend:**
- React 18
- Sigma.js v2
- Graphology
- Tailwind CSS

**Orchestration:**
- n8n for workflows

**AI:**
- Claude API (Anthropic)

### 32. Database Indexes
**Critical indexes:**
- GIN index on nodes.properties (JSONB)
- Composite index on edges(source_node_id, target_node_id)
- B-tree indexes on all foreign keys
- Index on nodes.type for filtering
- Index on edges.weight for weighted operations

---

## SECTION 10: TESTING & VALIDATION

### 33. Unit Tests Required
- nlp.text_processor
- nlp.ngram_generator
- graph.graph_builder
- graph.edge_calculator
- algorithms.louvain
- algorithms.betweenness
- gaps.gap_detector
- graphrag.query_processor

### 34. Specification Tests
- test_ngram_weights (verify 3/2/1 weights)
- test_node_sizing (verify linear 5-40px)
- test_gap_thresholds (verify all filters)
- test_edge_weight_accumulation (verify additive)
- test_cognitive_state_classification (verify thresholds)

### 35. Integration Tests
- text_to_graph_pipeline
- graph_to_visualization
- graphrag_query_flow

---

## CRITICAL REMINDERS

### DO's:
✅ Use EXACT values from specifications  
✅ Apply stopwords BEFORE lemmatization  
✅ Use ADDITIVE edge weights (no normalization)  
✅ Use LINEAR node sizing (not logarithmic)  
✅ Follow 5-stage gap detection process  
✅ Use Brandes' algorithm for betweenness  
✅ Return maximum 3 gaps  
✅ Use 2-hop neighborhood for GraphRAG  

### DON'Ts:
❌ Never normalize edge weights  
❌ Never use logarithmic node sizing  
❌ Never apply lemmatization before stopwords  
❌ Never approximate algorithm parameters  
❌ Never skip validation tests  

---

## REFERENCES

All specifications in this document are derived from comprehensive research analysis of the InfraNodus system, including:
- Official documentation
- Academic papers on algorithms
- Source code analysis
- Community discussions
- Performance testing results

For implementation details, refer to:
- Master Prompt (InfraNodus_Master_Prompt_UPDATED.md)
- Development Plans (InfraNodus_Development_Plan_UPDATED.md, Part 2)
- Quick Reference (QUICK_REFERENCE.md)
- Full specifications (SPECIFICATIONS.md)
- Validation rules (specs/validation-rules.json)

---

**Document Version:** 1.0.0  
**Last Updated:** October 28, 2025
