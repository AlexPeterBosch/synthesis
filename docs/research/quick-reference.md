# InfraNodus Replica: QUICK REFERENCE GUIDE
## Essential Specifications at a Glance

---

## 🎯 NLP PROCESSING

### **Processing Order:**
1. Tokenize sentences/paragraphs
2. Remove special characters
3. Remove URLs
4. Remove standalone numbers
5. **Remove stopwords** ← BEFORE lemmatization!
6. **Lemmatize** ← AFTER stopwords!
7. Extract entities (if mode != 'lemmas')

### **N-gram Algorithm:**
```
PASS 1: Bigrams → weight = 3
PASS 2: 4-gram window
  - Distance 1 (1 word apart) → weight = 2
  - Distance 2 (2 words apart) → weight = 1

CRITICAL: Paragraph breaks (\n\n) STOP scanning!
```

---

## 📢 EXACT PARAMETERS

### **Edge Weights:**
```python
# ADDITIVE, NO NORMALIZATION
edge_weight = sum(all co-occurrence weights)
# If appears 5 times as bigram: 3+3+3+3+3 = 15
```

### **Louvain:**
```python
resolution = 1.0  # Default
weighted = True   # Use edge weights
stopping = ΔQ < 0.0001
```

### **ForceAtlas2:**
```python
gravity = 1.0
scalingRatio = 20.0
strongGravityMode = True
linLogMode = False
edgeWeightInfluence = 1.0
barnesHutOptimize = True
barnesHutTheta = 1.2
iterations = 500-2000  # Based on size
```

### **Node Sizing:**
```python
# LINEAR scaling (NOT logarithmic!)
min_size = 5   # pixels
max_size = 40  # pixels
size = 5 + (bc_normalized * 35)
```

### **Modularity Thresholds:**
```
Q > 0.4  = Strong community structure ✓
Q < 0.4  = Too interconnected
Q > 0.7  = Very strong (possibly disconnected)
```

### **Gap Detection:**
```python
MIN_COMMUNITY_SIZE = 3      # nodes
MAX_PATH_LENGTH = 6         # hops
DENSITY_THRESHOLD = 0.1     # 10%
MAX_SIZE_RATIO = 10         # 10:1
MIN_GAP_SCORE = 0.4

Return: Top 3 gaps maximum
```

### **Cognitive States:**
```
Biased:      modularity <0.4, entropy <0.5  → 80% explore
Focused:     modularity <0.4, density >0.7  → 30% explore
Diversified: 0.4≤mod≤0.7, 0.4≤ent≤0.7       → 50% explore (OPTIMAL)
Dispersed:   modularity >0.7, entropy >0.7  → 20% explore

Mind Viral Immunity = modularity × entropy
  High:   >0.28
  Medium: 0.16-0.28
  Low:    <0.16
```

---

## 🗄️ DATABASE TABLES

```
users          → id, username, email, api_key, tier
contexts       → id, name, user_id, visibility, metadata
nodes          → id, node_id, label, type, properties (JSONB), context_id
edges          → id, edge_id, source_id, target_id, type, weight, properties
statements     → id, statement_id, text, sentiment, topics, context_id
graph_metrics  → id, context_id, modularity, entropy, cognitive_state
```

**Critical Indexes:**
```sql
CREATE INDEX idx_nodes_properties ON nodes USING GIN(properties);
CREATE INDEX idx_edges_composite ON edges(source_node_id, target_node_id);
```

---

## 🎨 VISUALIZATION

### **Sigma.js Settings:**
```javascript
{
  labelSize: 12,
  renderEdgeLabels: false,
  defaultNodeColor: '#666',
  defaultEdgeColor: '#ccc',
  nodeReducer: (node, data) => ({
    ...data,
    label: data.size > 20 ? data.label : ''  // Top 30% only
  })
}
```

### **Node Properties:**
```javascript
{
  size: 5-40,  // Linear by BC
  color: community_color,  // HSL color space
  label: lemma,
  x: position_x,
  y: position_y
}
```

### **Edge Properties:**
```javascript
{
  weight: co_occurrence_count,
  size: Math.log(weight + 1)  // Thickness
}
```

---

## 🤖 GRAPHRAG WORKFLOW

```
1. Tokenize query → lemmas
2. Find overlapping nodes (SQL)
3. Extract 2-hop subgraph
4. Get communities + metrics
5. Format context:
   - Main topics (by community)
   - Top 10 concepts (by BC)
   - Top 15 relations (by weight)
   - Top 5 gaps
6. Send to Claude with system prompt
7. Return answer
```

---

## 📊 PERFORMANCE TARGETS

```
Text processing:  <5 seconds for 500 words
Graph construction: <10 seconds for 500 nodes
Louvain: <2 seconds for 1000 nodes
ForceAtlas2: <30 seconds for 1000 nodes
Betweenness: <5 seconds for 500 nodes
GraphRAG query: <3 seconds total
Visualization: 60 FPS smooth
```

---

## 🔧 TECHNOLOGY STACK

### **Backend:**
```
Python 3.10+
FastAPI
spaCy (en_core_web_sm)
NetworkX
python-louvain
fa2
PostgreSQL 15+
Prisma ORM
```

### **Frontend:**
```
React 18
Sigma.js v2
Graphology
Tailwind CSS
Axios
```

### **Orchestration:**
```
n8n
Super Code Node
AI Agent Node (Claude)
```

---

## ⚠️ COMMON MISTAKES TO AVOID

❌ **Normalizing edge weights** → Use raw sums  
❌ **Logarithmic node sizing** → Use linear  
❌ **Lemmatizing before stopwords** → Stopwords first!  
❌ **Connecting across paragraphs** → Paragraph breaks stop scanning  
❌ **Using Louvain defaults** → Use resolution=1.0  
❌ **Skipping gap filters** → Use all 5 stages  
❌ **Wrong ForceAtlas2 params** → Use InfraNodus values  

---

## ✅ TESTING CHECKLIST

```python
# Test 1: N-grams
Input: "AI tools analyze data"
Expected: [("ai", "tool", 3), ("tool", "analyze", 3), ("analyze", "data", 3), ("ai", "analyze", 2), ...]

# Test 2: Weight accumulation
Input: [("ai", "tool", 3), ("ai", "tool", 3)]
Expected: edge weight = 6 (not normalized)

# Test 3: Node sizing
BC = 0.5, min_bc = 0, max_bc = 1
Expected: size = 5 + (0.5 * 35) = 22.5 ≈ 23 pixels

# Test 4: Modularity
Typical text graph
Expected: Q > 0.4

# Test 5: Gap detection
Graph with 2 disconnected communities
Expected: 1-3 gaps detected

# Test 6: Cognitive state
modularity = 0.5, entropy = 0.6
Expected: state = "diversified_fractal"
```

---

## 🚀 GETTING STARTED

**Week 1-2: Database**
```bash
createdb synthesis
psql synthesis < schema.sql
npx prisma migrate dev
```

**Week 3-4: NLP**
```bash
pip install spacy
python -m spacy download en_core_web_sm
uvicorn nlp_processor:app --reload
```

**Week 5-6: Graph**
```bash
pip install networkx
python test_graph_construction.py
```

**Week 7-9: Algorithms**
```bash
pip install python-louvain fa2
python test_algorithms.py
```

**Week 10-12: GraphRAG**
```bash
# Import n8n workflow
# Configure Claude API
# Test queries
```

**Week 12-14: Visualization**
```bash
cd src/frontend
npm install sigma graphology
npm start
```

---

## 💡 QUICK WINS

**Day 1:** Database schema working  
**Week 2:** N-grams generating correctly  
**Week 4:** Graph visualization showing  
**Week 6:** Communities colored properly  
**Week 8:** GraphRAG answering questions  
**Week 12:** Full system operational  

---

## 🆘 TROUBLESHOOTING

**Problem:** Weights not accumulating  
**Solution:** Check edge_weights dict, ensure using sorted tuple as key

**Problem:** Node sizes all the same  
**Solution:** Verify BC calculation, check min/max range

**Problem:** Communities not detected  
**Solution:** Check modularity >0.4, verify weighted graph

**Problem:** ForceAtlas2 not converging  
**Solution:** Increase iterations, check parameter values

**Problem:** Gaps all false positives  
**Solution:** Apply all 5 filter stages, check thresholds

**Problem:** GraphRAG not relevant  
**Solution:** Verify 2-hop extraction, check context format

---

**Print this page for your desk!** 📄

Last updated: Based on 50 research questions answered
