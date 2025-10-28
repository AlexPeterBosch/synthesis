# InfraNodus Replica: UPDATED Development Plan
## With Concrete Implementation Specifications from Research
## English-Only Implementation

**Based on comprehensive Perplexity research answering all 50 critical questions**

---
# Synthesis: UPDATED Development Plan
## With Concrete Implementation Specifications from Research
## English-Only Implementation

**Based on comprehensive Perplexity research answering all 50 critical questions**

---

## 🎯 EXECUTIVE SUMMARY

**Timeline:** 12-14 weeks (reduced from 16 due to English-only focus)  
**Complexity:** 7/10 (reduced with concrete specs)  
**Status:** All critical research gaps filled with specific implementation details

**Key Changes from Original Plan:**
- ✅ Exact algorithms and parameters now specified
- ✅ English-only simplifies NLP (no multi-language complexity)
- ✅ Database schema fully defined
- ✅ All algorithm parameters confirmed
- ✅ ForceAtlas2 configuration specified
- ✅ GraphRAG implementation detailed

---

## PHASE 1: DATABASE ARCHITECTURE (Weeks 1-2)
**Complexity:** 5/10 | **Duration:** 2 weeks

### 1.1 PostgreSQL Schema - EXACT SPECIFICATION

Based on research Q7-Q8, here's the complete schema:

```sql
-- USERS TABLE
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    api_key VARCHAR(500),
    subscription_tier VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- CONTEXTS TABLE (Graph instances)
CREATE TABLE contexts (
    id SERIAL PRIMARY KEY,
    context_name VARCHAR(255) UNIQUE NOT NULL,  -- @private, @public, custom
    user_id INTEGER REFERENCES users(id),
    visibility VARCHAR(50),  -- public, private, shared
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

-- NODES TABLE (All 5 node types)
CREATE TABLE nodes (
    id SERIAL PRIMARY KEY,
    node_id VARCHAR(255) UNIQUE NOT NULL,  -- UUID or custom ID
    label VARCHAR(500),                     -- Node display name (lemma)
    type VARCHAR(50),                       -- concept/statement/context/user/narrative
    properties JSONB,                       -- Flexible attributes
    user_id INTEGER REFERENCES users(id),
    context_id INTEGER REFERENCES contexts(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- EDGES TABLE (All 7 relationship types)
CREATE TABLE edges (
    id SERIAL PRIMARY KEY,
    edge_id VARCHAR(255) UNIQUE NOT NULL,
    source_node_id INTEGER REFERENCES nodes(id) ON DELETE CASCADE,
    target_node_id INTEGER REFERENCES nodes(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50),  -- :TO, :AT, :OF, :IN, :BY, :INTO, :THRU
    weight INTEGER DEFAULT 1,       -- Co-occurrence weight
    properties JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_edge UNIQUE(source_node_id, target_node_id, relationship_type)
);

-- STATEMENTS TABLE (Original text segments)
CREATE TABLE statements (
    id SERIAL PRIMARY KEY,
    statement_id VARCHAR(255) UNIQUE NOT NULL,
    text TEXT NOT NULL,                     -- Original sentence/paragraph
    sentiment VARCHAR(20),                   -- positive, negative, neutral
    topics TEXT[],                          -- Array of topic tags
    context_id INTEGER REFERENCES contexts(id),
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- GRAPH METRICS TABLE
CREATE TABLE graph_metrics (
    id SERIAL PRIMARY KEY,
    context_id INTEGER REFERENCES contexts(id),
    modularity FLOAT,                       -- Newman-Girvan modularity
    influence_entropy FLOAT,                -- Jenks natural breaks entropy
    node_count INTEGER,
    edge_count INTEGER,
    community_count INTEGER,
    avg_betweenness FLOAT,
    cognitive_state VARCHAR(50),            -- biased/focused/diversified/dispersed
    calculated_at TIMESTAMP DEFAULT NOW()
);

-- INDEXES FOR PERFORMANCE
CREATE INDEX idx_nodes_node_id ON nodes(node_id);
CREATE INDEX idx_nodes_type ON nodes(type);
CREATE INDEX idx_nodes_user_id ON nodes(user_id);
CREATE INDEX idx_nodes_context_id ON nodes(context_id);
CREATE INDEX idx_nodes_properties ON nodes USING GIN(properties);  -- JSONB index

CREATE INDEX idx_edges_source ON edges(source_node_id);
CREATE INDEX idx_edges_target ON edges(target_node_id);
CREATE INDEX idx_edges_type ON edges(relationship_type);
CREATE INDEX idx_edges_weight ON edges(weight);
CREATE INDEX idx_edges_composite ON edges(source_node_id, target_node_id);

CREATE INDEX idx_statements_context ON statements(context_id);
CREATE INDEX idx_statements_topics ON statements USING GIN(topics);

CREATE INDEX idx_metrics_context ON graph_metrics(context_id);
CREATE INDEX idx_metrics_calculated ON graph_metrics(calculated_at DESC);
```

### 1.2 Node Properties JSONB Structure

```json
{
  "lemma": "research",
  "original_words": ["Research", "researching", "researches"],
  "frequency": 8,
  "betweenness_centrality": 0.045,
  "degree": 12,
  "community_id": 3,
  "color": "#FF5733",
  "size": 15,
  "position_x": 123.45,
  "position_y": 67.89,
  "tf_idf": 0.23
}
```

### 1.3 Prisma Schema

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id                Int       @id @default(autoincrement())
  username          String    @unique
  email             String    @unique
  apiKey            String?   @map("api_key")
  subscriptionTier  String?   @map("subscription_tier")
  createdAt         DateTime  @default(now()) @map("created_at")
  
  nodes     Node[]
  contexts  Context[]
  statements Statement[]
  
  @@map("users")
}

model Context {
  id          Int      @id @default(autoincrement())
  contextName String   @unique @map("context_name")
  userId      Int      @map("user_id")
  visibility  String?
  createdAt   DateTime @default(now()) @map("created_at")
  metadata    Json?
  
  user        User     @relation(fields: [userId], references: [id])
  nodes       Node[]
  statements  Statement[]
  metrics     GraphMetric[]
  
  @@map("contexts")
}

model Node {
  id         Int      @id @default(autoincrement())
  nodeId     String   @unique @map("node_id")
  label      String?
  type       String
  properties Json?
  userId     Int?     @map("user_id")
  contextId  Int?     @map("context_id")
  createdAt  DateTime @default(now()) @map("created_at")
  updatedAt  DateTime @updatedAt @map("updated_at")
  
  user       User?    @relation(fields: [userId], references: [id])
  context    Context? @relation(fields: [contextId], references: [id])
  
  outgoingEdges Edge[] @relation("SourceNode")
  incomingEdges Edge[] @relation("TargetNode")
  
  @@index([nodeId])
  @@index([type])
  @@index([contextId])
  @@map("nodes")
}

model Edge {
  id               Int      @id @default(autoincrement())
  edgeId           String   @unique @map("edge_id")
  sourceNodeId     Int      @map("source_node_id")
  targetNodeId     Int      @map("target_node_id")
  relationshipType String   @map("relationship_type")
  weight           Int      @default(1)
  properties       Json?
  createdAt        DateTime @default(now()) @map("created_at")
  
  sourceNode Edge[] @relation("SourceNode", fields: [sourceNodeId], references: [id], onDelete: Cascade)
  targetNode Node   @relation("TargetNode", fields: [targetNodeId], references: [id], onDelete: Cascade)
  
  @@unique([sourceNodeId, targetNodeId, relationshipType])
  @@index([sourceNodeId])
  @@index([targetNodeId])
  @@map("edges")
}

model Statement {
  id          Int      @id @default(autoincrement())
  statementId String   @unique @map("statement_id")
  text        String
  sentiment   String?
  topics      String[]
  contextId   Int?     @map("context_id")
  userId      Int?     @map("user_id")
  createdAt   DateTime @default(now()) @map("created_at")
  
  context     Context? @relation(fields: [contextId], references: [id])
  user        User?    @relation(fields: [userId], references: [id])
  
  @@index([contextId])
  @@map("statements")
}

model GraphMetric {
  id                Int      @id @default(autoincrement())
  contextId         Int      @map("context_id")
  modularity        Float?
  influenceEntropy  Float?   @map("influence_entropy")
  nodeCount         Int?     @map("node_count")
  edgeCount         Int?     @map("edge_count")
  communityCount    Int?     @map("community_count")
  avgBetweenness    Float?   @map("avg_betweenness")
  cognitiveState    String?  @map("cognitive_state")
  calculatedAt      DateTime @default(now()) @map("calculated_at")
  
  context           Context  @relation(fields: [contextId], references: [id])
  
  @@index([contextId])
  @@map("graph_metrics")
}
```

**Deliverables:**
- ✅ Complete SQL schema
- ✅ Prisma schema with migrations
- ✅ Seed data with test users
- ✅ FastAPI connection pool setup

---

## PHASE 2: NLP PROCESSING PIPELINE (Weeks 3-4)
**Complexity:** 6/10 | **Duration:** 2 weeks | **English-Only**

### 2.1 Exact Stopwords List (Research Q1)

```python
# stopwords_english.py
ENGLISH_STOPWORDS = [
    # Articles
    "a", "an", "the",
    
    # Pronouns
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", 
    "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", 
    "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", 
    "their", "theirs", "themselves",
    
    # Verbs (auxiliaries & common)
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", 
    "do", "does", "did", "doesn't", "will", "would", "should", "could", "may", 
    "might", "must", "can", "cannot", "can't",
    
    # Prepositions
    "of", "at", "by", "for", "with", "about", "against", "between", "into", 
    "through", "during", "before", "after", "above", "below", "to", "from", 
    "up", "down", "in", "out", "on", "off", "over", "under",
    
    # Adverbs & Conjunctions
    "again", "further", "then", "once", "here", "there", "when", "where", 
    "why", "how", "all", "both", "each", "few", "more", "most", "other", 
    "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", 
    "too", "very", "and", "but", "or", "because", "as", "until", "while",
    
    # Common fillers
    "necessary", "really", "just", "quite", "rather", "actually", "basically",
    
    # InfraNodus custom additions
    "thing", "things", "something", "anything", "everything", "nothing",
    "someone", "anyone", "everyone", "person", "people"
]

# User can add custom stopwords via settings
# Can remove default stopwords using minus prefix: "-did", "-do"
```

### 2.2 NLP Processor - EXACT Implementation (Research Q2-Q5)

```python
# nlp_processor.py
import spacy
from typing import List, Dict, Tuple
import re

class TextProcessor:
    def __init__(self, language='en'):
        self.language = language
        # Load spaCy English model
        self.nlp = spacy.load('en_core_web_sm')
        self.stopwords = set(ENGLISH_STOPWORDS)
    
    def preprocess(self, text: str, mode: str = 'mixed') -> Dict:
        """
        Complete preprocessing pipeline
        
        Order (from Q5):
        1. Sentence/paragraph tokenization
        2. Special character removal
        3. Number filtering
        4. URL removal
        5. Stopwords removal
        6. Lemmatization
        7. Entity extraction (if mode != 'lemmas')
        
        Args:
            text: Input text
            mode: 'lemmas', 'mixed', 'entities' (from Q3)
        
        Returns:
            Dict with tokens, lemmas, entities, statements
        """
        # Step 1: Parse with spaCy
        doc = self.nlp(text)
        
        # Step 2-4: Clean text
        cleaned_tokens = []
        statements = []  # Original sentences
        
        for sent in doc.sents:
            statements.append(sent.text)
            sent_tokens = []
            
            for token in sent:
                # Skip punctuation
                if token.is_punct:
                    continue
                
                # Skip URLs (Q5)
                if token.like_url:
                    continue
                
                # Skip standalone numbers (Q5)
                if token.is_digit and token.text.isdigit():
                    continue
                
                # Skip special characters (Q5)
                if not token.text.isalnum() and not '-' in token.text:
                    continue
                
                sent_tokens.append(token)
            
            cleaned_tokens.extend(sent_tokens)
        
        # Step 5: Remove stopwords (BEFORE lemmatization per Q1)
        tokens_no_stopwords = [
            token for token in cleaned_tokens 
            if token.text.lower() not in self.stopwords
        ]
        
        # Step 6: Lemmatization (AFTER stopwords per Q2)
        lemmatized = [token.lemma_.lower() for token in tokens_no_stopwords]
        
        # Step 7: Entity extraction (Q3)
        entities = []
        if mode in ['mixed', 'entities']:
            entities = self._extract_entities(doc, mode)
        
        return {
            'tokens': lemmatized,
            'entities': entities,
            'statements': statements,
            'mode': mode
        }
    
    def _extract_entities(self, doc, mode: str) -> List[Dict]:
        """
        Extract named entities with [[wiki links]] tagging
        
        Three modes (Q3):
        - lemmas: No entity extraction
        - mixed: Preserve entities, add lemmas
        - entities: Only entities with root form
        """
        entities = []
        
        for ent in doc.ents:
            entity_data = {
                'text': ent.text,
                'label': ent.label_,  # PERSON, ORG, GPE, DATE, MONEY, etc.
                'wiki_link': f"[[{ent.text}]]"
            }
            
            if mode == 'entities':
                # Use root canonical form
                # "the USA" → "United States"
                entity_data['canonical'] = ent.text  # Could enhance with KB lookup
            
            entities.append(entity_data)
        
        return entities
    
    def create_ngrams(self, tokens: List[str]) -> List[Tuple[str, str, int]]:
        """
        TWO-PASS 4-gram window algorithm (Q4)
        
        PASS 1: Bigram scan (adjacent words) - weight = 3
        PASS 2: 4-gram window - weights 2 and 1 based on distance
        
        Paragraph breaks STOP the algorithm (Q4)
        
        Returns: List of (source, target, weight) tuples
        """
        ngrams = []
        
        # PASS 1: Bigrams (adjacent words)
        for i in range(len(tokens) - 1):
            ngrams.append((tokens[i], tokens[i+1], 3))
        
        # PASS 2: 4-gram window
        for i in range(len(tokens) - 3):
            window = tokens[i:i+4]
            
            # Distance 1 (1 word apart): weight = 2
            ngrams.append((window[0], window[2], 2))
            ngrams.append((window[1], window[3], 2))
            
            # Distance 2 (2 words apart): weight = 1
            ngrams.append((window[0], window[3], 1))
        
        return ngrams
    
    def process_with_paragraph_breaks(self, text: str) -> List[Tuple[str, str, int]]:
        """
        Handle paragraph breaks correctly (Q4)
        
        Paragraph breaks STOP n-gram scanning
        Last word of paragraph NOT connected to first word of next
        """
        paragraphs = text.split('\n\n')  # Double newline = paragraph break
        all_ngrams = []
        
        for para in paragraphs:
            if not para.strip():
                continue
            
            # Process each paragraph independently
            para_result = self.preprocess(para)
            para_ngrams = self.create_ngrams(para_result['tokens'])
            all_ngrams.extend(para_ngrams)
        
        return all_ngrams
```

### 2.3 FastAPI Service

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple

app = FastAPI(title="InfraNodus NLP Service")

class TextInput(BaseModel):
    text: str
    mode: str = 'mixed'  # lemmas, mixed, entities
    custom_stopwords: List[str] = []

class ProcessedOutput(BaseModel):
    tokens: List[str]
    entities: List[dict]
    ngrams: List[Tuple[str, str, int]]
    statements: List[str]

@app.post("/process", response_model=ProcessedOutput)
async def process_text(input: TextInput):
    """
    Complete text processing pipeline
    """
    try:
        processor = TextProcessor()
        
        # Add custom stopwords if provided
        if input.custom_stopwords:
            processor.stopwords.update(input.custom_stopwords)
        
        # Process text
        result = processor.preprocess(input.text, mode=input.mode)
        
        # Generate n-grams
        ngrams = processor.create_ngrams(result['tokens'])
        
        return ProcessedOutput(
            tokens=result['tokens'],
            entities=result['entities'],
            ngrams=ngrams,
            statements=result['statements']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Deliverables:**
- ✅ Complete NLP service with spaCy
- ✅ Exact stopwords list
- ✅ TWO-PASS 4-gram algorithm
- ✅ Paragraph break handling
- ✅ Three entity extraction modes
- ✅ FastAPI endpoints
- ✅ Unit tests for each function

---

## PHASE 3: GRAPH CONSTRUCTION (Weeks 5-6)
**Complexity:** 7/10 | **Duration:** 2 weeks

### 3.1 Edge Weight Calculation - EXACT Formula (Research Q6)

```python
# graph_builder.py
import networkx as nx
from collections import defaultdict
from typing import List, Tuple
import uuid

class GraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()
    
    def build_from_ngrams(self, ngrams: List[Tuple[str, str, int]], context_id: int) -> dict:
        """
        Build graph from weighted n-grams
        
        ADDITIVE edge weighting WITHOUT normalization (Q6)
        Weights accumulate across multiple co-occurrences
        """
        # Accumulate weights for same edge pairs
        edge_weights = defaultdict(int)
        
        for source, target, weight in ngrams:
            # Normalize edge key (undirected)
            edge_key = tuple(sorted([source, target]))
            edge_weights[edge_key] += weight
        
        # Create nodes and edges
        for (source, target), final_weight in edge_weights.items():
            # Add nodes if not exist
            if not self.graph.has_node(source):
                self.graph.add_node(source, label=source, type='concept')
            
            if not self.graph.has_node(target):
                self.graph.add_node(target, label=target, type='concept')
            
            # Add edge with accumulated weight
            # NO NORMALIZATION - use raw weights directly
            self.graph.add_edge(source, target, weight=final_weight)
        
        return {
            'node_count': self.graph.number_of_nodes(),
            'edge_count': self.graph.number_of_edges(),
            'graph': self.graph
        }
    
    def export_to_database(self, graph, context_id: int, user_id: int) -> dict:
        """
        Save graph to PostgreSQL using Prisma
        """
        from prisma import Prisma
        
        prisma = Prisma()
        await prisma.connect()
        
        node_mapping = {}  # lemma → database ID
        
        # Create nodes
        for node_id, data in graph.nodes(data=True):
            db_node = await prisma.node.create(
                data={
                    'nodeId': str(uuid.uuid4()),
                    'label': node_id,
                    'type': 'concept',
                    'contextId': context_id,
                    'userId': user_id,
                    'properties': {
                        'lemma': node_id,
                        'frequency': graph.degree(node_id),
                        'original_words': [node_id]  # Will enhance later
                    }
                }
            )
            node_mapping[node_id] = db_node.id
        
        # Create edges
        for source, target, data in graph.edges(data=True):
            await prisma.edge.create(
                data={
                    'edgeId': str(uuid.uuid4()),
                    'sourceNodeId': node_mapping[source],
                    'targetNodeId': node_mapping[target],
                    'relationshipType': ':TO',  # concept-concept co-occurrence
                    'weight': data['weight'],
                    'properties': {
                        'co_occurrence_count': data['weight']
                    }
                }
            )
        
        await prisma.disconnect()
        
        return {
            'context_id': context_id,
            'nodes_created': len(node_mapping),
            'edges_created': graph.number_of_edges()
        }
```

**Deliverables:**
- ✅ Graph builder with exact weight formula
- ✅ NetworkX graph construction
- ✅ Database persistence with Prisma
- ✅ Node/edge deduplication
- ✅ Weight accumulation logic

---

## PHASE 4: CORE ALGORITHMS (Weeks 7-9)
**Complexity:** 8/10 | **Duration:** 3 weeks

### 4.1 Louvain Community Detection - EXACT Parameters (Research Q9)

```python
# algorithms.py
import community as community_louvain
import networkx as nx

def detect_communities(graph: nx.Graph) -> Tuple[dict, float]:
    """
    Louvain algorithm with exact InfraNodus parameters
    
    Resolution parameter: γ = 1.0 (default, Q9)
    Stopping criteria: ΔQ < 0.0001 or stable iteration
    Weighted graph: Uses edge weights from co-occurrence
    
    Returns: (partition dict, modularity score)
    """
    # Apply Louvain algorithm
    # python-louvain library with default resolution=1.0
    partition = community_louvain.best_partition(
        graph, 
        weight='weight',  # Use edge weights
        resolution=1.0,   # Default resolution (Q9)
        randomize=False   # Deterministic results
    )
    
    # Calculate modularity score
    modularity = community_louvain.modularity(partition, graph, weight='weight')
    
    # Group nodes by community
    communities = defaultdict(list)
    for node, comm_id in partition.items():
        communities[comm_id].append(node)
    
    return partition, modularity, dict(communities)

def assign_community_colors(num_communities: int, palette: str = "colorful") -> List[str]:
    """
    Generate distinct colors for communities (Q11)
    
    Uses HSL color space for maximum perceptual distinction
    """
    colors = []
    hue_step = 360 / num_communities
    
    for i in range(num_communities):
        hue = (i * hue_step) % 360
        
        if palette == "colorful":
            saturation = 75  # High saturation
            lightness = 55
        elif palette == "subdued":
            saturation = 45  # Lower saturation
            lightness = 65
        
        # Convert HSL to HEX
        color_hex = hsl_to_hex(hue, saturation, lightness)
        colors.append(color_hex)
    
    return colors

def hsl_to_hex(h, s, l):
    """Convert HSL to HEX color"""
    import colorsys
    r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
```

### 4.2 ForceAtlas2 Layout - EXACT Parameters (Research Q12-Q14)

```python
# layout_engine.py
from fa2 import ForceAtlas2

def calculate_layout(graph: nx.Graph, iterations: int = 1000) -> dict:
    """
    ForceAtlas2 layout with InfraNodus-specific parameters
    
    Based on research Q12-Q14
    """
    forceatlas2 = ForceAtlas2(
        # Core Forces
        gravity=1.0,                          # Stronger gravity for compact layout (Q12)
        scalingRatio=20.0,                    # Global scaling, 10-50 range (Q12)
        
        # Force Model
        strongGravityMode=True,               # Stronger pull to center (Q12)
        linLogMode=False,                     # Linear-linear model (Q12)
        
        # Edge Weights
        edgeWeightInfluence=1.0,              # Fully respect edge weights (Q12)
        
        # Hub Handling
        outboundAttractionDistribution=False,  # Don't penalize hubs (Q12)
        
        # Performance
        adjustSizes=False,                    # Don't adjust for node overlap (Q12)
        barnesHutOptimize=True,               # Use Barnes-Hut for speed (Q12)
        barnesHutTheta=1.2,                   # Precision parameter (Q12)
        
        # Adaptive Speed
        jitterTolerance=1.0,                  # Swinging tolerance (Q12)
        
        # Convergence
        verbose=False
    )
    
    # Initial positions: Random (Q14)
    import random
    pos = {node: (random.uniform(-100, 100), random.uniform(-100, 100)) 
           for node in graph.nodes()}
    
    # Run ForceAtlas2
    positions = forceatlas2.forceatlas2_networkx_layout(
        graph,
        pos=pos,
        iterations=iterations
    )
    
    return positions

def layout_for_large_graphs(graph: nx.Graph) -> dict:
    """
    Optimized layout for graphs >1000 nodes (Q13)
    
    Strategy:
    - Server-side computation only
    - Barnes-Hut optimization mandatory
    - Adaptive iteration count
    """
    node_count = graph.number_of_nodes()
    
    if node_count < 500:
        iterations = 1000
    elif node_count < 2000:
        iterations = 1500
    else:
        iterations = 2000
    
    # Use Barnes-Hut for all large graphs
    positions = calculate_layout(graph, iterations=iterations)
    
    return positions
```

### 4.3 Betweenness Centrality - EXACT Formula (Research Q15-Q17)

```python
# centrality.py
import networkx as nx

def calculate_betweenness_centrality(graph: nx.Graph, weighted: bool = True) -> dict:
    """
    Brandes' algorithm for betweenness centrality (Q15)
    
    Weighted: Uses edge weights for shortest paths
    Normalized: Values in 0-1 range
    """
    if weighted:
        # Use edge weights (inverse: higher weight = shorter distance)
        # Convert co-occurrence weights to distances
        weight_fn = lambda u, v, d: 1.0 / (d['weight'] + 1)
        bc = nx.betweenness_centrality(
            graph,
            normalized=True,
            weight='weight'
        )
    else:
        bc = nx.betweenness_centrality(graph, normalized=True)
    
    return bc

def bc_to_node_size(bc_value: float, min_bc: float, max_bc: float, 
                     min_size: int = 5, max_size: int = 40) -> int:
    """
    Convert betweenness centrality to node size (Q16)
    
    LINEAR SCALING (Q16):
    - Minimum size: 5 pixels (lowest BC nodes)
    - Maximum size: 40 pixels (highest BC nodes)
    - 8:1 ratio for clear visual hierarchy
    """
    # Avoid division by zero
    if max_bc == min_bc:
        return (min_size + max_size) // 2
    
    # Linear scaling
    bc_normalized = (bc_value - min_bc) / (max_bc - min_bc)
    node_size = min_size + (bc_normalized * (max_size - min_size))
    
    return int(node_size)

def calculate_with_caching(graph: nx.Graph, context_id: int) -> dict:
    """
    BC calculation with caching strategy (Q17)
    
    1. Check if cached in database
    2. If not, calculate and cache
    3. Background processing for large graphs
    """
    from prisma import Prisma
    import json
    
    prisma = Prisma()
    await prisma.connect()
    
    # Check cache (stored in node properties)
    cached_nodes = await prisma.node.find_many(
        where={'contextId': context_id},
        select={'nodeId': True, 'properties': True}
    )
    
    # Check if BC is cached and recent
    all_have_bc = all(
        node.properties.get('betweenness_centrality') is not None 
        for node in cached_nodes
    )
    
    if all_have_bc:
        # Use cached values
        bc = {
            node.properties['lemma']: node.properties['betweenness_centrality']
            for node in cached_nodes
        }
        return bc
    
    # Calculate BC
    bc = calculate_betweenness_centrality(graph, weighted=True)
    
    # Cache results in database
    for node_lemma, bc_value in bc.items():
        await prisma.node.update_many(
            where={
                'contextId': context_id,
                'properties': {'path': ['lemma'], 'equals': node_lemma}
            },
            data={
                'properties': {
                    'betweenness_centrality': bc_value
                }
            }
        )
    
    await prisma.disconnect()
    
    return bc
```

### 4.4 Modularity Score - EXACT Formula (Research Q10)

```python
# modularity.py
import networkx as nx
from networkx.algorithms import community as nx_comm

def calculate_modularity(graph: nx.Graph, communities: dict) -> float:
    """
    Weighted Newman-Girvan modularity (Q10)
    
    Formula:
    Q = 1/(2m) Σ [w_ij - (k_i * k_j)/(2m)] * δ(c_i, c_j)
    
    Where:
    - m = total edge weight in graph
    - w_ij = weight of edge between i and j
    - k_i = weighted degree of node i
    - c_i = community of node i
    - δ(c_i, c_j) = 1 if same community, else 0
    
    Interpretation (Q10):
    - Q > 0.4: Pronounced community structure ✓
    - Q < 0.4: Too interconnected
    - Q < 0: Anti-modular
    """
    # Convert partition dict to community list
    community_list = []
    comm_dict = defaultdict(set)
    
    for node, comm_id in communities.items():
        comm_dict[comm_id].add(node)
    
    community_list = list(comm_dict.values())
    
    # Calculate weighted modularity
    modularity = nx_comm.modularity(graph, community_list, weight='weight')
    
    return modularity

def interpret_modularity(modularity: float) -> str:
    """
    Interpret modularity score (Q10)
    """
    if modularity > 0.7:
        return "Very strong community structure (possibly disconnected)"
    elif modularity > 0.5:
        return "Strong community structure (typical for InfraNodus)"
    elif modularity > 0.3:
        return "Moderate community structure"
    else:
        return "Weak community structure (too interconnected)"
```

**Deliverables:**
- ✅ Louvain with γ=1.0 resolution
- ✅ ForceAtlas2 with exact parameters
- ✅ Betweenness centrality with Brandes
- ✅ Modularity calculation (weighted)
- ✅ Community color assignment
- ✅ BC-to-size conversion formula
- ✅ Caching strategy for BC

---

## PHASE 5: STRUCTURAL GAP DETECTION (Weeks 9-10)
**Complexity:** 8/10 | **Duration:** 2 weeks

### 5.1 Gap Detection Algorithm - EXACT Implementation (Research Q18-Q20)

```python
# gap_detector.py
import networkx as nx
from itertools import combinations
from typing import List, Dict
import numpy as np

class GapDetector:
    def __init__(self, graph: nx.Graph, communities: dict):
        self.graph = graph
        self.communities = communities
        self.MIN_COMMUNITY_SIZE = 3        # Q20: Minimum 3 nodes
        self.MAX_PATH_LENGTH = 6           # Q20: Max shortest path
        self.DENSITY_THRESHOLD = 0.1       # Q20: 10% connection density
        self.MAX_SIZE_RATIO = 10           # Q20: 10:1 size ratio
        self.SEMANTIC_SIMILARITY_MIN = 0.3 # Q20: Minimum similarity
        self.SEMANTIC_SIMILARITY_MAX = 0.5 # Q20: Maximum similarity
    
    def detect_gaps(self) -> List[Dict]:
        """
        Multi-stage gap detection with false positive filtering (Q20)
        
        Returns top 1-3 significant gaps
        """
        candidate_gaps = []
        
        # Get all community pairs
        comm_ids = list(set(self.communities.values()))
        
        for comm_a, comm_b in combinations(comm_ids, 2):
            gap = self._analyze_community_pair(comm_a, comm_b)
            
            if gap is not None:
                candidate_gaps.append(gap)
        
        # Filter false positives
        significant_gaps = self._filter_false_positives(candidate_gaps)
        
        # Sort by gap score, return top 3
        significant_gaps.sort(key=lambda x: x['gap_score'], reverse=True)
        return significant_gaps[:3]
    
    def _analyze_community_pair(self, comm_a: int, comm_b: int) -> Dict:
        """
        Analyze gap between two communities (Q18)
        """
        # Get nodes in each community
        nodes_a = [n for n, c in self.communities.items() if c == comm_a]
        nodes_b = [n for n, c in self.communities.items() if c == comm_b]
        
        # Stage 1: Size filters (Q20)
        if len(nodes_a) < self.MIN_COMMUNITY_SIZE:
            return None
        if len(nodes_b) < self.MIN_COMMUNITY_SIZE:
            return None
        
        size_ratio = max(len(nodes_a), len(nodes_b)) / min(len(nodes_a), len(nodes_b))
        if size_ratio > self.MAX_SIZE_RATIO:
            return None
        
        # Stage 2: Topological distance (Q18)
        avg_distance = self._calculate_avg_distance(nodes_a, nodes_b)
        
        if avg_distance > self.MAX_PATH_LENGTH:
            return None  # Disconnected, not a gap
        if avg_distance < 2:
            return None  # Already connected
        
        # Stage 3: Connection density (Q20)
        density = self._calculate_connection_density(nodes_a, nodes_b)
        
        if density > self.DENSITY_THRESHOLD:
            return None  # Already well connected
        
        # Stage 4: Calculate gap score (Q18)
        expected_connection = self._calculate_expected_connection(nodes_a, nodes_b)
        actual_connection = density * len(nodes_a) * len(nodes_b)
        gap_score = expected_connection - actual_connection
        
        # Stage 5: Identify bridging concepts (Q19)
        bridging_concepts = self._find_bridging_concepts(nodes_a, nodes_b)
        
        return {
            'community_a': comm_a,
            'community_b': comm_b,
            'concepts_a': nodes_a[:10],  # Top 10 concepts
            'concepts_b': nodes_b[:10],
            'avg_distance': avg_distance,
            'density': density,
            'gap_score': gap_score,
            'bridging_concepts': bridging_concepts
        }
    
    def _calculate_avg_distance(self, nodes_a: List, nodes_b: List) -> float:
        """
        Average shortest path between communities (Q18)
        """
        distances = []
        
        for node_a in nodes_a[:20]:  # Sample for speed
            for node_b in nodes_b[:20]:
                try:
                    path_length = nx.shortest_path_length(
                        self.graph, 
                        source=node_a, 
                        target=node_b,
                        weight='weight'
                    )
                    distances.append(path_length)
                except nx.NetworkXNoPath:
                    distances.append(float('inf'))
        
        if not distances or all(d == float('inf') for d in distances):
            return float('inf')
        
        # Filter out infinite distances
        finite_distances = [d for d in distances if d != float('inf')]
        return np.mean(finite_distances) if finite_distances else float('inf')
    
    def _calculate_connection_density(self, nodes_a: List, nodes_b: List) -> float:
        """
        Connection density between communities (Q20)
        
        density = actual_edges / possible_edges
        """
        actual_edges = 0
        
        for node_a in nodes_a:
            for node_b in nodes_b:
                if self.graph.has_edge(node_a, node_b):
                    actual_edges += 1
        
        possible_edges = len(nodes_a) * len(nodes_b)
        density = actual_edges / possible_edges if possible_edges > 0 else 0
        
        return density
    
    def _calculate_expected_connection(self, nodes_a: List, nodes_b: List) -> float:
        """
        Expected connection based on community sizes (Q18)
        
        Uses global graph density as baseline
        """
        global_density = self.graph.number_of_edges() / (self.graph.number_of_nodes() ** 2)
        expected_edges = len(nodes_a) * len(nodes_b) * global_density
        
        return expected_edges
    
    def _find_bridging_concepts(self, nodes_a: List, nodes_b: List) -> List[str]:
        """
        Identify potential bridging concepts (Q19)
        
        These are nodes with high betweenness that connect both communities
        """
        bridging = []
        
        # Get nodes with shortest paths to both communities
        for node in self.graph.nodes():
            if node in nodes_a or node in nodes_b:
                continue
            
            # Check if node connects both communities
            connects_a = any(nx.has_path(self.graph, node, na) for na in nodes_a[:5])
            connects_b = any(nx.has_path(self.graph, node, nb) for nb in nodes_b[:5])
            
            if connects_a and connects_b:
                bc = self.graph.nodes[node].get('betweenness_centrality', 0)
                bridging.append((node, bc))
        
        # Sort by betweenness, return top 5
        bridging.sort(key=lambda x: x[1], reverse=True)
        return [concept for concept, _ in bridging[:5]]
    
    def _filter_false_positives(self, gaps: List[Dict]) -> List[Dict]:
        """
        Multi-stage false positive filtering (Q20)
        """
        filtered = []
        
        for gap in gaps:
            # Skip if gap score too low
            if gap['gap_score'] < 0.4:
                continue
            
            # Skip if communities completely disconnected (not a gap)
            if gap['avg_distance'] == float('inf'):
                continue
            
            # Skip if density already high
            if gap['density'] > self.DENSITY_THRESHOLD:
                continue
            
            filtered.append(gap)
        
        return filtered
```

**Deliverables:**
- ✅ Gap detection with exact thresholds
- ✅ Multi-stage filtering (5 filters from Q20)
- ✅ Topological distance calculation
- ✅ Connection density analysis
- ✅ Bridging concept identification
- ✅ False positive avoidance

---

Due to length constraints, I'll continue in the next file with Phases 6-9 and the Master Prompt update...

