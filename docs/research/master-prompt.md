# InfraNodus Replica: UPDATED Master Prompt
## Ready-to-Use Prompts with Exact Specifications
## English-Only Implementation

---
# Synthesis: UPDATED Master Prompt
## Ready-to-Use Prompts with Exact Specifications
## English-Only Implementation

**Based on comprehensive research answering all 50 critical questions**

---

## 🎯 PROJECT OVERVIEW

**Goal:** Build InfraNodus replica with EXACT specifications from research  
**Timeline:** 12-14 weeks  
**Focus:** English-only (simplified from multi-language)  
**Status:** All implementation details confirmed

---

## 📋 PHASE 1: DATABASE SETUP

### Prompt for Claude Code:

```
TASK: Create PostgreSQL database schema for InfraNodus replica

EXACT SPECIFICATIONS (from research):

1. Create the following tables with EXACT schema:

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    api_key VARCHAR(500),
    subscription_tier VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Contexts table (graph instances)
CREATE TABLE contexts (
    id SERIAL PRIMARY KEY,
    context_name VARCHAR(255) UNIQUE NOT NULL,  -- @private, @public
    user_id INTEGER REFERENCES users(id),
    visibility VARCHAR(50),  -- public, private, shared
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

-- Nodes table (5 node types: concept, statement, context, user, narrative)
CREATE TABLE nodes (
    id SERIAL PRIMARY KEY,
    node_id VARCHAR(255) UNIQUE NOT NULL,
    label VARCHAR(500),
    type VARCHAR(50),  -- concept/statement/context/user/narrative
    properties JSONB,  -- Store: BC, degree, community_id, color, size, position, etc.
    user_id INTEGER REFERENCES users(id),
    context_id INTEGER REFERENCES contexts(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Edges table (7 relationship types)
CREATE TABLE edges (
    id SERIAL PRIMARY KEY,
    edge_id VARCHAR(255) UNIQUE NOT NULL,
    source_node_id INTEGER REFERENCES nodes(id) ON DELETE CASCADE,
    target_node_id INTEGER REFERENCES nodes(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50),  -- :TO, :AT, :OF, :IN, :BY, :INTO, :THRU
    weight INTEGER DEFAULT 1,  -- Co-occurrence weight (ADDITIVE, no normalization)
    properties JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_edge UNIQUE(source_node_id, target_node_id, relationship_type)
);

-- Statements table (original text segments)
CREATE TABLE statements (
    id SERIAL PRIMARY KEY,
    statement_id VARCHAR(255) UNIQUE NOT NULL,
    text TEXT NOT NULL,
    sentiment VARCHAR(20),
    topics TEXT[],
    context_id INTEGER REFERENCES contexts(id),
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Graph metrics table
CREATE TABLE graph_metrics (
    id SERIAL PRIMARY KEY,
    context_id INTEGER REFERENCES contexts(id),
    modularity FLOAT,  -- Newman-Girvan weighted modularity
    influence_entropy FLOAT,  -- Jenks natural breaks entropy
    node_count INTEGER,
    edge_count INTEGER,
    community_count INTEGER,
    avg_betweenness FLOAT,
    cognitive_state VARCHAR(50),  -- biased/focused/diversified/dispersed
    calculated_at TIMESTAMP DEFAULT NOW()
);

-- CRITICAL INDEXES for performance
CREATE INDEX idx_nodes_node_id ON nodes(node_id);
CREATE INDEX idx_nodes_type ON nodes(type);
CREATE INDEX idx_nodes_context_id ON nodes(context_id);
CREATE INDEX idx_nodes_properties ON nodes USING GIN(properties);  -- JSONB index

CREATE INDEX idx_edges_source ON edges(source_node_id);
CREATE INDEX idx_edges_target ON edges(target_node_id);
CREATE INDEX idx_edges_composite ON edges(source_node_id, target_node_id);
CREATE INDEX idx_edges_weight ON edges(weight);

CREATE INDEX idx_statements_context ON statements(context_id);
CREATE INDEX idx_metrics_context ON graph_metrics(context_id);
```

2. Create Prisma schema (schema.prisma file)

3. Generate migrations

4. Create seed data with test user

5. Test database connection with FastAPI

DELIVERABLES:
- schema.sql file
- schema.prisma file
- migration files
- seed.py with test data
- test_connection.py FastAPI script

TECHNOLOGY:
- PostgreSQL 15+
- Prisma ORM
- Python FastAPI
```

---

## 📋 PHASE 2: NLP PIPELINE

### Prompt for Claude Code:

```
TASK: Build English-only NLP processing service with EXACT InfraNodus specifications

EXACT ALGORITHM (from research):

1. **Stopwords List** (use this EXACT list):
```python
ENGLISH_STOPWORDS = [
    "a", "an", "the",
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "doesn't",
    "will", "would", "should", "could", "may", "might", "must", "can", "cannot", "can't",
    "of", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from",
    "up", "down", "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there", "when", "where",
    "why", "how", "all", "both", "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
    "too", "very", "and", "but", "or", "because", "as", "until", "while",
    "necessary", "really", "just", "quite", "rather", "actually", "basically",
    "thing", "things", "something", "anything", "everything", "nothing"
]
```

2. **Processing Order** (EXACT from research):
   1. Sentence/paragraph tokenization
   2. Special character removal
   3. Number filtering (remove standalone numbers, keep "COVID-19")
   4. URL removal
   5. **Stopwords removal** (BEFORE lemmatization)
   6. **Lemmatization** (AFTER stopwords) using spaCy en_core_web_sm
   7. Entity extraction (if mode != 'lemmas')

3. **N-gram Algorithm** (TWO-PASS, EXACT from research):

```python
def create_ngrams(tokens: List[str]) -> List[Tuple[str, str, int]]:
    \"\"\"
    TWO-PASS 4-gram window algorithm
    
    PASS 1: Bigrams (adjacent words) → weight = 3
    PASS 2: 4-gram window → weights 2 and 1
    
    CRITICAL: Paragraph breaks STOP the algorithm!
    \"\"\"
    ngrams = []
    
    # PASS 1: Bigrams (adjacent = weight 3)
    for i in range(len(tokens) - 1):
        ngrams.append((tokens[i], tokens[i+1], 3))
    
    # PASS 2: 4-gram window
    for i in range(len(tokens) - 3):
        window = tokens[i:i+4]
        
        # Distance 1 (1 word apart) → weight = 2
        ngrams.append((window[0], window[2], 2))
        ngrams.append((window[1], window[3], 2))
        
        # Distance 2 (2 words apart) → weight = 1
        ngrams.append((window[0], window[3], 1))
    
    return ngrams
```

4. **Paragraph Break Handling** (CRITICAL):
- Split text by double newline (\n\n)
- Process each paragraph independently
- DO NOT connect last word of paragraph to first word of next

5. **Entity Extraction Modes** (3 modes):
- **lemmas**: No entity extraction
- **mixed**: Preserve multi-word entities + lemmas
- **entities**: Only entities with root canonical form

CREATE:
1. nlp_processor.py with TextProcessor class
2. FastAPI service with /process endpoint
3. requirements.txt with: spacy, fastapi, uvicorn
4. Unit tests for each function
5. Docker file for deployment

TEST INPUT:
"Companies are analyzing customer feedback using AI tools."

EXPECTED OUTPUT:
- Tokens: ["company", "analyze", "customer", "feedback", "use", "ai", "tool"]
- Entities: ["Companies" (ORG), "AI" (ORG)]
- N-grams with weights (company→analyze: 3, company→customer: 2, etc.)

TECHNOLOGY:
- spaCy en_core_web_sm
- Python 3.10+
- FastAPI
- Pydantic
```

---

## 📋 PHASE 3: GRAPH CONSTRUCTION

### Prompt for Claude Code:

```
TASK: Build graph construction engine with EXACT weight calculation

EXACT EDGE WEIGHT FORMULA (from research):

**ADDITIVE weighting WITHOUT normalization**

```python
def build_from_ngrams(ngrams: List[Tuple[str, str, int]]) -> nx.Graph:
    \"\"\"
    Accumulate weights - NO NORMALIZATION
    
    If "research" and "laboratory" appear:
    - 5 times as bigrams (adjacent): weight = 3+3+3+3+3 = 15
    - 3 times with 1 word between: weight = 2+2+2 = 6
    
    Final edge weight = sum of all co-occurrences
    Raw weights used directly in all algorithms
    \"\"\"
    edge_weights = defaultdict(int)
    
    for source, target, weight in ngrams:
        edge_key = tuple(sorted([source, target]))  # Undirected
        edge_weights[edge_key] += weight  # ADDITIVE
    
    graph = nx.Graph()
    for (source, target), final_weight in edge_weights.items():
        graph.add_edge(source, target, weight=final_weight)
    
    return graph
```

**CRITICAL:** NO normalization by max weight, total weight, or node degree!

DELIVERABLES:
1. graph_builder.py with GraphBuilder class
2. build_from_ngrams() method
3. export_to_database() method using Prisma
4. Test with sample n-grams
5. Verify weight accumulation works correctly

TEST:
Input: [("research", "lab", 3), ("research", "lab", 3), ("research", "data", 2)]
Expected: 
- Edge research-lab: weight = 6
- Edge research-data: weight = 2

TECHNOLOGY:
- NetworkX 3.x
- Prisma ORM
- Python
```

---

## 📋 PHASE 4: CORE ALGORITHMS

### Prompt for Claude Code:

```
TASK: Implement graph analysis algorithms with EXACT InfraNodus parameters

1. **LOUVAIN COMMUNITY DETECTION**

EXACT PARAMETERS (from research):
- Resolution: γ = 1.0 (default)
- Weighted: Use edge weights from co-occurrence
- Stopping: ΔQ < 0.0001 or stable iteration

```python
import community as community_louvain

def detect_communities(graph: nx.Graph) -> Tuple[dict, float]:
    \"\"\"
    Louvain with resolution=1.0
    Returns: (partition, modularity)
    \"\"\"
    partition = community_louvain.best_partition(
        graph,
        weight='weight',
        resolution=1.0,
        randomize=False  # Deterministic
    )
    
    modularity = community_louvain.modularity(
        partition, 
        graph, 
        weight='weight'
    )
    
    return partition, modularity
```

2. **FORCEATLAS2 LAYOUT**

EXACT PARAMETERS (from research):
```python
from fa2 import ForceAtlas2

forceatlas2 = ForceAtlas2(
    gravity=1.0,                  # Stronger gravity for compact layout
    scalingRatio=20.0,            # 10-50 range, use 20
    strongGravityMode=True,
    linLogMode=False,             # Linear-linear model
    edgeWeightInfluence=1.0,      # Fully respect edge weights
    outboundAttractionDistribution=False,
    adjustSizes=False,
    barnesHutOptimize=True,       # For large graphs
    barnesHutTheta=1.2,
    jitterTolerance=1.0
)

positions = forceatlas2.forceatlas2_networkx_layout(
    graph,
    pos=random_positions,  # Random initial positions
    iterations=1000        # 500-2000 depending on size
)
```

3. **BETWEENNESS CENTRALITY**

```python
def calculate_betweenness_centrality(graph: nx.Graph) -> dict:
    \"\"\"
    Brandes' algorithm with edge weights
    Normalized to 0-1 range
    \"\"\"
    bc = nx.betweenness_centrality(
        graph,
        normalized=True,
        weight='weight'
    )
    return bc
```

4. **BC TO NODE SIZE CONVERSION** (EXACT formula):

```python
def bc_to_node_size(bc_value: float, min_bc: float, max_bc: float) -> int:
    \"\"\"
    LINEAR SCALING (NOT logarithmic)
    
    Min size: 5 pixels
    Max size: 40 pixels
    8:1 ratio for visual hierarchy
    \"\"\"
    if max_bc == min_bc:
        return 22  # Midpoint
    
    # Linear scaling
    bc_normalized = (bc_value - min_bc) / (max_bc - min_bc)
    node_size = 5 + (bc_normalized * 35)  # 5 to 40 pixels
    
    return int(node_size)
```

5. **WEIGHTED MODULARITY** (Newman-Girvan formula):

```python
from networkx.algorithms import community as nx_comm

def calculate_modularity(graph: nx.Graph, communities: dict) -> float:
    \"\"\"
    Q = 1/(2m) Σ [w_ij - (k_i * k_j)/(2m)] * δ(c_i, c_j)
    
    Interpretation:
    - Q > 0.4: Strong community structure ✓
    - Q < 0.4: Too interconnected
    \"\"\"
    community_list = convert_partition_to_list(communities)
    modularity = nx_comm.modularity(graph, community_list, weight='weight')
    return modularity
```

6. **COMMUNITY COLOR ASSIGNMENT**:

```python
def assign_community_colors(num_communities: int) -> List[str]:
    \"\"\"
    HSL color space for maximum distinction
    \"\"\"
    colors = []
    hue_step = 360 / num_communities
    
    for i in range(num_communities):
        hue = (i * hue_step) % 360
        saturation = 75  # High saturation
        lightness = 55
        colors.append(hsl_to_hex(hue, saturation, lightness))
    
    return colors
```

DELIVERABLES:
- algorithms.py with all 6 functions
- Test with sample graph
- Verify modularity > 0.4 for typical texts
- Verify node sizes in 5-40 range

TECHNOLOGY:
- NetworkX
- python-louvain
- fa2
- NumPy
```

---

## 📋 PHASE 5: GAP DETECTION

### Prompt for Claude Code:

```
TASK: Implement structural gap detection with EXACT thresholds

EXACT PARAMETERS (from research):

```python
class GapDetector:
    MIN_COMMUNITY_SIZE = 3        # Minimum 3 nodes
    MAX_PATH_LENGTH = 6           # Max shortest path
    DENSITY_THRESHOLD = 0.1       # 10% connection threshold
    MAX_SIZE_RATIO = 10           # 10:1 max size difference
    MIN_GAP_SCORE = 0.4           # Minimum gap score
```

MULTI-STAGE FILTERING (EXACT from research):

**Stage 1: Size Filters**
- Community A size >= 3 nodes
- Community B size >= 3 nodes
- Size ratio <= 10:1

**Stage 2: Topological Distance**
- Average shortest path: 2 to 6 hops
- If >6: completely disconnected (not a gap)
- If <2: already connected (not a gap)

**Stage 3: Connection Density**
- Density = actual_edges / possible_edges
- Only flag if density < 10%

**Stage 4: Gap Score**
```python
gap_score = expected_connection - actual_connection

expected_connection = size_a * size_b * global_density
actual_connection = density * size_a * size_b
```

**Stage 5: Bridging Concepts**
- Find nodes connecting both communities
- Sort by betweenness centrality
- Return top 5 as potential bridges

ALGORITHM:
1. Get all community pairs
2. Apply 5-stage filter
3. Sort by gap_score
4. Return top 3 gaps (max)

DELIVERABLES:
- gap_detector.py with GapDetector class
- Multi-stage filtering pipeline
- Bridging concept identifier
- Test with sample graph
- Verify 1-3 gaps detected typically

EXPECTED BEHAVIOR:
- Most texts: 1-3 significant gaps
- Highly connected: 0 gaps
- Incoherent: >5 gaps (rare)

TECHNOLOGY:
- NetworkX
- Python
```

---

## 📋 PHASE 6: GRAPHRAG

### Prompt for Claude Code:

```
TASK: Create n8n GraphRAG workflow with EXACT specifications

WORKFLOW STEPS (from research):

1. **Webhook Trigger**: Receive query + graph_id
2. **Process Query**: Tokenize and lemmatize using NLP service
3. **Find Overlapping Nodes**: SQL query for nodes with query tokens
4. **Extract Subgraph**: Get 2-hop neighborhood of overlapped nodes
5. **Get Metrics**: Fetch communities, gaps, modularity
6. **Build Context**: Format graph structure for prompt
7. **AI Query**: Send to Claude with context
8. **Respond**: Return AI response

EXACT CONTEXT FORMAT:

```javascript
const promptContext = `
# Knowledge Graph Context

## Main Topics
${mainTopics.map(t => `- ${t.topic}: ${t.concepts.join(', ')}`).join('\n')}

## Key Concepts (by influence)
${topConcepts.map(c => `- ${c.concept} (${c.influence.toFixed(3)})`).join('\n')}

## Important Relations
${topEdges.map(r => `- ${r.from} ←→ ${r.to} (strength: ${r.strength})`).join('\n')}

## Structural Gaps
${gaps.map(g => `- Gap between "${g.comm_a}" and "${g.comm_b}"`).join('\n')}

## Graph Metrics
- Nodes: ${nodeCount}
- Modularity: ${modularity.toFixed(3)}
- Cognitive state: ${cognitiveState}
`;
```

SYSTEM PROMPT for Claude:
```
You are analyzing a knowledge graph to answer questions. Use the graph structure, main topics, key concepts, and relations provided to give insightful, contextually-aware responses. Focus on connections, patterns, and structural insights rather than just keyword matching.
```

DELIVERABLES:
1. Complete n8n workflow JSON
2. Super Code nodes for processing
3. Postgres query nodes
4. AI Agent node configuration
5. Test with sample query

TEST QUERY:
"How are AI tools and customer feedback related?"

EXPECTED:
- Finds nodes related to both concepts
- Extracts subgraph
- Provides structured context to Claude
- Returns insightful answer based on graph

TECHNOLOGY:
- n8n
- Super Code Node (JavaScript)
- Postgres nodes
- AI Agent node (Claude)
```

---

## 📋 PHASE 7: VISUALIZATION

### Prompt for Claude Code:

```
TASK: Build React + Sigma.js visualization with EXACT specifications

REACT COMPONENT (from research):

```javascript
import React, { useEffect, useRef } from 'react';
import Graph from 'graphology';
import Sigma from 'sigma';

const GraphVisualization = ({ graphData }) => {
  const containerRef = useRef(null);
  
  useEffect(() => {
    const graph = new Graph();
    
    // Add nodes with EXACT sizing formula
    graphData.nodes.forEach(node => {
      const bc = node.properties.betweenness_centrality;
      const min_bc = Math.min(...graphData.nodes.map(n => n.properties.betweenness_centrality));
      const max_bc = Math.max(...graphData.nodes.map(n => n.properties.betweenness_centrality));
      
      // LINEAR SCALING: 5-40 pixels
      const size = 5 + ((bc - min_bc) / (max_bc - min_bc)) * 35;
      
      graph.addNode(node.node_id, {
        label: node.properties.lemma,
        size: size,
        color: node.properties.color,
        x: node.properties.position_x || Math.random() * 100,
        y: node.properties.position_y || Math.random() * 100
      });
    });
    
    // Add edges with weight-based thickness
    graphData.edges.forEach(edge => {
      const thickness = Math.log(edge.weight + 1);
      graph.addEdge(edge.source_node_id, edge.target_node_id, {
        weight: edge.weight,
        size: thickness
      });
    });
    
    // Sigma.js configuration
    const sigma = new Sigma(graph, containerRef.current, {
      renderEdgeLabels: false,
      defaultNodeColor: '#666',
      defaultEdgeColor: '#ccc',
      labelSize: 12,
      nodeReducer: (node, data) => ({
        ...data,
        // Show labels only for top 30% nodes
        label: data.size > 20 ? data.label : ''
      })
    });
    
    return () => sigma.kill();
  }, [graphData]);
  
  return <div ref={containerRef} style={{ width: '100%', height: '600px' }} />;
};
```

DELIVERABLES:
1. GraphVisualization.jsx component
2. App.jsx with routing
3. API integration (axios)
4. Tailwind CSS styling
5. package.json
6. Test with sample graph

FEATURES:
- Zoom and pan
- Node size by BC (5-40px)
- Edge thickness by weight
- Community colors
- Label threshold (top 30%)

TECHNOLOGY:
- React 18
- Sigma.js v2
- Graphology
- Tailwind CSS
```

---

## 📋 PHASE 8: COGNITIVE ANALYSIS

### Prompt for Claude Code:

```
TASK: Implement cognitive state classifier with EXACT thresholds

EXACT STATE CLASSIFICATION (from research):

```python
def analyze_cognitive_state(modularity, influence_entropy, edge_density):
    \"\"\"
    Four cognitive states with EXACT thresholds
    \"\"\"
    
    # State 1: Biased/Uniform
    if modularity < 0.4 and influence_entropy < 0.5:
        state = 'biased_uniform'
        advice = 'Add diverse topics'
        explore_ratio = 80
    
    # State 2: Focused/Regular
    elif modularity < 0.4 and edge_density > 0.7:
        state = 'focused_regular'
        advice = 'Consider branching out'
        explore_ratio = 30
    
    # State 3: Diversified/Fractal (OPTIMAL)
    elif 0.4 <= modularity <= 0.7 and 0.4 <= influence_entropy <= 0.7:
        state = 'diversified_fractal'
        advice = 'Excellent balance!'
        explore_ratio = 50
    
    # State 4: Dispersed/Complex
    elif modularity > 0.7 and influence_entropy > 0.7:
        state = 'dispersed_complex'
        advice = 'Consider focusing themes'
        explore_ratio = 20
    
    # Mind Viral Immunity
    immunity = modularity * influence_entropy
    if immunity > 0.28:
        immunity_level = 'high'
    elif immunity > 0.16:
        immunity_level = 'medium'
    else:
        immunity_level = 'low'
    
    return {
        'state': state,
        'advice': advice,
        'explore_ratio': explore_ratio,
        'immunity_score': immunity,
        'immunity_level': immunity_level
    }
```

DELIVERABLES:
- cognitive_analyzer.py
- State classifier function
- Immunity calculator
- Influence entropy function
- Test with sample metrics

TECHNOLOGY:
- Python
- NumPy
```

---

## ✅ QUALITY CHECKLIST

Before completing each phase:

- [ ] Code matches EXACT specifications from research
- [ ] All parameters are correct (no approximations)
- [ ] Tested with sample data
- [ ] Unit tests pass
- [ ] Integration with previous phases works
- [ ] Performance acceptable (<2s for 1000 nodes)
- [ ] Database operations optimized
- [ ] Documentation complete

---

## 🚀 QUICK START COMMANDS

```bash
# Setup database
createdb infranodus_replica
psql infranodus_replica < schema.sql

# Install Python dependencies
pip install fastapi uvicorn prisma networkx python-louvain fa2 spacy --break-system-packages
python -m spacy download en_core_web_sm

# Run NLP service
uvicorn nlp_processor:app --host 0.0.0.0 --port 8000

# Run graph service
uvicorn graph_api:app --host 0.0.0.0 --port 8001

# Install frontend
npx create-react-app infranodus-ui
cd infranodus-ui
npm install sigma graphology tailwindcss axios

# Run frontend
npm start
```

---

## 📊 TESTING COMMANDS

```python
# Test NLP
import requests
response = requests.post('http://localhost:8000/process', json={
    'text': 'Companies are analyzing customer feedback using AI tools.',
    'mode': 'lemmas'
})
print(response.json())

# Test graph construction
# Should show: {"company": "analyze": 3, "company": "customer": 2, ...}

# Test community detection
# Should show: modularity > 0.4 for typical text

# Test ForceAtlas2
# Should converge in 500-1000 iterations for small graphs

# Test betweenness
# Should return values in 0-1 range
# Node sizes should be 5-40 pixels
```

---

## 🎯 SUCCESS CRITERIA

✅ **Phase 1:** Database created, Prisma working  
✅ **Phase 2:** N-grams generated correctly with weights 1, 2, 3  
✅ **Phase 3:** Edges accumulate weights properly (no normalization)  
✅ **Phase 4:** Modularity >0.4, node sizes 5-40px, communities colored  
✅ **Phase 5:** 1-3 gaps detected with meaningful scores  
✅ **Phase 6:** GraphRAG returns contextual answers  
✅ **Phase 7:** Graph renders smoothly at 60 FPS  
✅ **Phase 8:** Cognitive state classified correctly  

---

## 🔄 ITERATIVE DEVELOPMENT

1. Build → Test → Verify against research specs
2. If wrong, check research document for EXACT specification
3. Never approximate - use EXACT values from research
4. Test each component before moving to next phase

**You have ALL the specifications needed. Start building!** 🚀
