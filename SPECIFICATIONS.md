# Synthesis: Complete Technical Specifications

**Last Updated:** October 28, 2025  
**Version:** 1.0.0  
**Source:** Comprehensive research analysis

---

## NLP Processing Pipeline

### Processing Order (CRITICAL)
1. Tokenize sentences/paragraphs
2. Remove special characters
3. Remove URLs
4. Remove standalone numbers
5. **Remove stopwords** ← BEFORE lemmatization!
6. **Lemmatize** ← AFTER stopwords!
7. Extract entities (if mode != 'lemmas')

### N-gram Algorithm: TWO-PASS

**Pass 1: Bigrams**
- Weight: 3
- Distance: 0 (adjacent words)

**Pass 2: 4-gram Window**
- Distance 1 (1 word apart) → weight = 2
- Distance 2 (2 words apart) → weight = 1

**CRITICAL:** Paragraph breaks (\\n\\n) STOP scanning!

### Stopwords
- Count: 180+ words
- Applied BEFORE lemmatization
- See: `specs/stopwords.json`

## Graph Construction

### Edge Weights
```python
# ADDITIVE, NO NORMALIZATION
edge_weight = sum(all co-occurrence weights)
# If appears 5 times as bigram: 3+3+3+3+3 = 15
```

**Example:**
- "AI" and "tools" appear together 3 times as bigrams → weight = 9
- They also appear 2 times with 1 word between → weight += 4
- Total edge weight: 13

## Core Algorithms

### Louvain Community Detection
```python
resolution = 1.0  # Default
weighted = True   # Use edge weights
stopping = ΔQ < 0.0001
```

### ForceAtlas2 Layout
```python
gravity = 1.0
scalingRatio = 20.0
strongGravityMode = True
linLogMode = False
edgeWeightInfluence = 1.0
barnesHutOptimize = True
barnesHutTheta = 1.2
iterations = 500-2000  # Based on graph size
```

### Betweenness Centrality
- Algorithm: Brandes' algorithm
- Weighted: True
- Normalized: True (range 0-1)

### Modularity (Newman-Girvan)
```python
Q = 1/(2m) Σ[Aᵢⱼ - (kᵢkⱼ)/(2m)]δ(cᵢ,cⱼ)

Thresholds:
Q > 0.4  = Strong community structure ✓
Q < 0.4  = Too interconnected
Q > 0.7  = Very strong (possibly disconnected)
```

## Visualization

### Node Sizing (LINEAR - NOT logarithmic!)
```python
min_size = 5   # pixels
max_size = 40  # pixels
size = 5 + (bc_normalized * 35)

# Ratio: 8:1 (max/min)
```

### Node Labels
- Display only for nodes with size > 20 pixels
- Approximately top 30% of nodes

### Edge Thickness
```python
thickness = log(weight + 1)
```

### Colors
- Community-based coloring
- HSL color space
- Saturation: 75%
- Lightness: 55%

## Gap Detection

### Thresholds
```python
MIN_COMMUNITY_SIZE = 3      # nodes
MAX_PATH_LENGTH = 6         # hops
DENSITY_THRESHOLD = 0.1     # 10%
MAX_SIZE_RATIO = 10         # 10:1
MIN_GAP_SCORE = 0.4

Return: Top 3 gaps maximum
```

### Five-Stage Filtering
1. Size filters (min 3 nodes, max ratio 10:1)
2. Distance filters (2-6 hops)
3. Density filters (<10% connections)
4. Gap score calculation (>0.4 threshold)
5. Semantic validation

## Cognitive States

### State Definitions
```python
Biased Uniform:
  modularity < 0.4, entropy < 0.5
  → 80% explore, 20% exploit

Focused Regular:
  modularity < 0.4, density > 0.7
  → 30% explore, 70% exploit

Diversified Fractal (OPTIMAL):
  0.4 ≤ modularity ≤ 0.7
  0.4 ≤ entropy ≤ 0.7
  → 50% explore, 50% exploit

Dispersed Complex:
  modularity > 0.7, entropy > 0.7
  → 20% explore, 80% exploit
```

### Mind Viral Immunity
```python
immunity = modularity × entropy

High:   > 0.28
Medium: 0.16 - 0.28
Low:    < 0.16
```

## GraphRAG

### Context Format
- Main topics (by community)
- Top 10 concepts (by betweenness)
- Top 15 relations (by weight)
- Top 5 gaps
- Graph metrics

### Subgraph Extraction
- 2-hop neighborhood from overlapping nodes

## Database Schema

See: `database/schema.sql` for complete specification

**Core Tables:**
- users
- contexts
- nodes (with JSONB properties)
- edges (with weights)
- statements
- graph_metrics

**Critical Indexes:**
- GIN index on nodes.properties
- Composite index on edges(source_node_id, target_node_id)

## Visualization

### Sigma.js Settings
```javascript
{
  "labelSize": 12,
  "renderEdgeLabels": false,
  "defaultNodeColor": "#666",
  "defaultEdgeColor": "#ccc"
}
```

### Node Labels
- Show only for nodes with size > 20 pixels (top ~30%)

## Performance Targets

- Text processing: < 5 seconds (500 words)
- Graph construction: < 10 seconds (500 nodes)
- Louvain: < 2 seconds (1000 nodes)
- ForceAtlas2: < 30 seconds (1000 nodes)
- Betweenness: < 5 seconds (500 nodes)
- GraphRAG query: < 3 seconds

## Technology Requirements

**Python:** 3.10+  
**Node.js:** 18+  
**PostgreSQL:** 15+  
**spaCy Model:** en_core_web_sm

---

**Source:** All specifications derived from comprehensive research analysis.

**Validation:** All implementations must pass specs/validation-rules.json checks.

**Last Updated:** October 28, 2025
