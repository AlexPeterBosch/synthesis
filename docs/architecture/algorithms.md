# Algorithm Architecture

## Pipeline

```
Text Input
  ↓
NLP Processing (spaCy)
  ↓
N-gram Generation (TWO-PASS)
  ↓
Graph Construction (NetworkX)
  ↓
Community Detection (Louvain)
  ↓
Layout (ForceAtlas2)
  ↓
Betweenness Centrality (Brandes)
  ↓
Gap Detection (5-stage filter)
  ↓
Cognitive Analysis
  ↓
Visualization (Sigma.js)
```

## Key Algorithms

### 1. TWO-PASS N-gram
- PASS 1: Bigrams (weight=3)
- PASS 2: 4-gram window (weights 2,1)

### 2. Louvain Community Detection
- Resolution: 1.0
- Weighted: True
- Stopping: ΔQ < 0.0001

### 3. ForceAtlas2 Layout
- gravity: 1.0
- scalingRatio: 20.0
- Barnes-Hut optimization

### 4. Betweenness Centrality
- Brandes algorithm
- Weighted, normalized

### 5. Gap Detection
- 5-stage filtering
- Return top 3 gaps

## Reference

- All parameters: `specs/parameters.json`
- Implementations: `src/algorithms/`