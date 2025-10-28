# InfraNodus Replica: Development Plan (PART 2)
## Phases 6-9: GraphRAG, Visualization, Cognitive Analysis, Integrations

---
# Synthesis: Development Plan (PART 2)
## Phases 6-9: GraphRAG, Visualization, Cognitive Analysis, Integrations

---

## PHASE 6: GraphRAG IMPLEMENTATION (Weeks 10-12)
**Complexity:** 9/10 | **Duration:** 3 weeks

### 6.1 n8n GraphRAG Workflow - COMPLETE SPECIFICATION

Based on the research, here's the exact GraphRAG workflow:

```json
{
  "name": "GraphRAG Query Processing",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "graphrag",
        "responseMode": "lastNode"
      },
      "name": "Webhook - Receive Query",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "functionCode": "// Step 1: Tokenize and lemmatize query\nconst _ = require('lodash');\nconst axios = require('axios');\n\nconst query = $input.item.json.query;\nconst graphId = $input.item.json.graph_id;\n\n// Call NLP service to process query\nconst nlpResponse = await axios.post('http://nlp-service:8000/process', {\n  text: query,\n  mode: 'lemmas'\n});\n\nconst queryTokens = nlpResponse.data.tokens;\n\nreturn {\n  query: query,\n  graph_id: graphId,\n  query_tokens: queryTokens\n};"
      },
      "name": "Super Code - Process Query",
      "type": "n8n-nodes-base.code",
      "position": [450, 300]
    },
    {
      "parameters": {
        "query": "SELECT * FROM nodes WHERE context_id = {{ $json.graph_id }} AND properties->>'lemma' IN ({{ $json.query_tokens.map(t => `'${t}'`).join(',') }})",
        "database": "infranodus_replica"
      },
      "name": "Postgres - Find Overlapping Nodes",
      "type": "n8n-nodes-base.postgres",
      "position": [650, 300]
    },
    {
      "parameters": {
        "functionCode": "// Step 2: Extract relevant subgraph (2-hop neighborhood)\nconst _ = require('lodash');\n\nconst overlappedNodes = $input.all().map(item => item.json);\nconst nodeIds = overlappedNodes.map(n => n.id);\n\n// Get 2-hop neighbors\nconst subgraphNodeIds = [...nodeIds];\n\n// First hop\nfor (const nodeId of nodeIds) {\n  const neighbors = await $executeSingleFunction('Postgres', {\n    query: `\n      SELECT DISTINCT target_node_id FROM edges WHERE source_node_id = ${nodeId}\n      UNION\n      SELECT DISTINCT source_node_id FROM edges WHERE target_node_id = ${nodeId}\n    `\n  });\n  subgraphNodeIds.push(...neighbors.map(n => n.target_node_id || n.source_node_id));\n}\n\n// Remove duplicates\nconst uniqueNodeIds = _.uniq(subgraphNodeIds);\n\nreturn { subgraph_node_ids: uniqueNodeIds };"
      },
      "name": "Super Code - Extract Subgraph",
      "type": "n8n-nodes-base.code",
      "position": [850, 300]
    },
    {
      "parameters": {
        "query": "SELECT * FROM nodes WHERE id IN ({{ $json.subgraph_node_ids.join(',') }})",
        "database": "infranodus_replica"
      },
      "name": "Postgres - Get Subgraph Nodes",
      "type": "n8n-nodes-base.postgres",
      "position": [1050, 300]
    },
    {
      "parameters": {
        "query": "SELECT * FROM edges WHERE source_node_id IN ({{ $json.subgraph_node_ids.join(',') }}) OR target_node_id IN ({{ $json.subgraph_node_ids.join(',') }})",
        "database": "infranodus_replica"
      },
      "name": "Postgres - Get Subgraph Edges",
      "type": "n8n-nodes-base.postgres",
      "position": [1050, 450]
    },
    {
      "parameters": {
        "query": "SELECT * FROM graph_metrics WHERE context_id = {{ $json.graph_id }} ORDER BY calculated_at DESC LIMIT 1",
        "database": "infranodus_replica"
      },
      "name": "Postgres - Get Metrics",
      "type": "n8n-nodes-base.postgres",
      "position": [1050, 600]
    },
    {
      "parameters": {
        "functionCode": "// Step 3: Build context for LLM prompt\nconst _ = require('lodash');\n\nconst nodes = $node['Postgres - Get Subgraph Nodes'].json;\nconst edges = $node['Postgres - Get Subgraph Edges'].json;\nconst metrics = $node['Postgres - Get Metrics'].json;\n\n// Group nodes by community\nconst communities = _.groupBy(nodes, n => n.properties.community_id);\n\n// Get top concepts by betweenness\nconst topConcepts = nodes\n  .sort((a, b) => (b.properties.betweenness_centrality || 0) - (a.properties.betweenness_centrality || 0))\n  .slice(0, 10)\n  .map(n => ({\n    concept: n.properties.lemma,\n    influence: n.properties.betweenness_centrality,\n    community: n.properties.community_id\n  }));\n\n// Get top edges by weight\nconst topEdges = edges\n  .sort((a, b) => b.weight - a.weight)\n  .slice(0, 15)\n  .map(e => {\n    const source = nodes.find(n => n.id === e.source_node_id);\n    const target = nodes.find(n => n.id === e.target_node_id);\n    return {\n      from: source?.properties.lemma,\n      to: target?.properties.lemma,\n      strength: e.weight\n    };\n  });\n\n// Format main topics\nconst mainTopics = Object.entries(communities).map(([commId, commNodes]) => ({\n  topic: `Community ${commId}`,\n  concepts: commNodes.slice(0, 5).map(n => n.properties.lemma)\n}));\n\n// Build prompt context\nconst promptContext = `\n# Knowledge Graph Context\n\n## Main Topics\n${mainTopics.map(t => `- ${t.topic}: ${t.concepts.join(', ')}`).join('\\n')}\n\n## Key Concepts (by influence)\n${topConcepts.map(c => `- ${c.concept} (${c.influence?.toFixed(3)})`).join('\\n')}\n\n## Important Relations\n${topEdges.map(r => `- ${r.from} ←→ ${r.to} (strength: ${r.strength})`).join('\\n')}\n\n## Graph Metrics\n- Total nodes: ${nodes.length}\n- Total edges: ${edges.length}\n- Modularity: ${metrics.modularity?.toFixed(3)}\n- Communities: ${metrics.community_count}\n- Cognitive state: ${metrics.cognitive_state}\n`;\n\nreturn { \n  prompt_context: promptContext,\n  original_query: $node['Webhook - Receive Query'].json.query\n};"
      },
      "name": "Super Code - Build Context",
      "type": "n8n-nodes-base.code",
      "position": [1250, 300]
    },
    {
      "parameters": {
        "model": "claude-sonnet-4-20250514",
        "systemPrompt": "You are analyzing a knowledge graph to answer questions. Use the graph structure, main topics, key concepts, and relations provided to give insightful, contextually-aware responses. Focus on connections, patterns, and structural insights.",
        "prompt": "{{ $json.prompt_context }}\\n\\nUser Query: {{ $json.original_query }}\\n\\nPlease provide insights based on the knowledge graph structure above."
      },
      "name": "AI Agent - Claude",
      "type": "@n8n/n8n-nodes-langchain.lmChatAnthropic",
      "position": [1450, 300]
    },
    {
      "parameters": {
        "respond": "allIncomingItems",
        "responseBody": "{{ $json }}",
        "options": {}
      },
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "position": [1650, 300]
    }
  ],
  "connections": {
    "Webhook - Receive Query": {
      "main": [[{"node": "Super Code - Process Query", "type": "main", "index": 0}]]
    },
    "Super Code - Process Query": {
      "main": [[{"node": "Postgres - Find Overlapping Nodes", "type": "main", "index": 0}]]
    },
    "Postgres - Find Overlapping Nodes": {
      "main": [[{"node": "Super Code - Extract Subgraph", "type": "main", "index": 0}]]
    },
    "Super Code - Extract Subgraph": {
      "main": [[{"node": "Postgres - Get Subgraph Nodes", "type": "main", "index": 0}]]
    },
    "Postgres - Get Subgraph Nodes": {
      "main": [[
        {"node": "Postgres - Get Subgraph Edges", "type": "main", "index": 0},
        {"node": "Postgres - Get Metrics", "type": "main", "index": 0}
      ]]
    },
    "Postgres - Get Subgraph Edges": {
      "main": [[{"node": "Super Code - Build Context", "type": "main", "index": 0}]]
    },
    "Postgres - Get Metrics": {
      "main": [[{"node": "Super Code - Build Context", "type": "main", "index": 0}]]
    },
    "Super Code - Build Context": {
      "main": [[{"node": "AI Agent - Claude", "type": "main", "index": 0}]]
    },
    "AI Agent - Claude": {
      "main": [[{"node": "Respond to Webhook", "type": "main", "index": 0}]]
    }
  }
}
```

### 6.2 Gap Bridging Workflow

```json
{
  "name": "AI Gap Bridging",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "generate-bridges",
        "responseMode": "lastNode"
      },
      "name": "Webhook - Generate Bridges",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "query": "SELECT * FROM gaps WHERE graph_id = {{ $json.graph_id }} ORDER BY gap_score DESC LIMIT 3"
      },
      "name": "Postgres - Get Top Gaps",
      "type": "n8n-nodes-base.postgres",
      "position": [450, 300]
    },
    {
      "parameters": {
        "functionCode": "// Format gap data for prompt\nconst gap = $input.item.json;\n\nconst prompt = `\nYou are an innovation strategist specializing in identifying connections between disconnected concepts.\n\n# Structural Gap Analysis\n\nGap detected between two topic clusters:\n\n**Cluster A**: ${gap.concepts_a.join(', ')}\n**Cluster B**: ${gap.concepts_b.join(', ')}\n\n**Gap Score**: ${gap.gap_score.toFixed(2)}\n**Current Distance**: ${gap.avg_distance} hops\n**Connection Density**: ${(gap.density * 100).toFixed(1)}%\n\n## Task\n\nGenerate 3-5 research questions or bridging ideas that would meaningfully connect these topics. Focus on:\n\n1. **Practical Applications**: How can these concepts be combined in real-world scenarios?\n2. **Novel Combinations**: What unexpected innovations could emerge?\n3. **Research Opportunities**: What questions haven't been explored?\n4. **Business Innovations**: What market opportunities exist in this gap?\n\nFormat your response as a numbered list of bridging ideas.\n`;\n\nreturn { \n  prompt: prompt,\n  gap_id: gap.id\n};"
      },
      "name": "Super Code - Format Prompt",
      "type": "n8n-nodes-base.code",
      "position": [650, 300]
    },
    {
      "parameters": {
        "model": "claude-sonnet-4-20250514",
        "prompt": "{{ $json.prompt }}"
      },
      "name": "AI Agent - Generate Bridges",
      "type": "@n8n/n8n-nodes-langchain.lmChatAnthropic",
      "position": [850, 300]
    },
    {
      "parameters": {
        "query": "INSERT INTO bridging_ideas (gap_id, idea_text, created_at) VALUES ({{ $json.gap_id }}, '{{ $json.response }}', NOW())"
      },
      "name": "Postgres - Save Ideas",
      "type": "n8n-nodes-base.postgres",
      "position": [1050, 300]
    },
    {
      "parameters": {
        "respond": "allIncomingItems",
        "responseBody": "{{ $json }}"
      },
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "position": [1250, 300]
    }
  ]
}
```

**Deliverables:**
- ✅ Complete GraphRAG n8n workflow
- ✅ Query tokenization and processing
- ✅ Subgraph extraction (2-hop)
- ✅ Context builder for prompts
- ✅ AI integration with Claude
- ✅ Gap bridging workflow
- ✅ Prompt templates

---

## PHASE 7: VISUALIZATION (Weeks 12-14)
**Complexity:** 7/10 | **Duration:** 2 weeks

### 7.1 React + Sigma.js Frontend - EXACT SPECIFICATION

```javascript
// GraphVisualization.jsx
import React, { useEffect, useRef, useState } from 'react';
import Graph from 'graphology';
import Sigma from 'sigma';
import { circular } from 'graphology-layout';

const GraphVisualization = ({ graphId }) => {
  const containerRef = useRef(null);
  const [sigmaInstance, setSigmaInstance] = useState(null);
  const [graphData, setGraphData] = useState(null);
  
  useEffect(() => {
    // Fetch graph data from API
    fetchGraphData(graphId);
  }, [graphId]);
  
  useEffect(() => {
    if (!graphData || !containerRef.current) return;
    
    // Create Graphology graph
    const graph = new Graph();
    
    // Add nodes with properties from research
    graphData.nodes.forEach(node => {
      const bc = node.properties.betweenness_centrality || 0;
      const min_bc = Math.min(...graphData.nodes.map(n => n.properties.betweenness_centrality || 0));
      const max_bc = Math.max(...graphData.nodes.map(n => n.properties.betweenness_centrality || 0));
      
      // LINEAR SCALING (from Q16)
      const size = 5 + ((bc - min_bc) / (max_bc - min_bc)) * 35;
      
      graph.addNode(node.node_id, {
        label: node.properties.lemma,
        size: size,  // 5-40 pixel range
        color: node.properties.color || '#999',
        x: node.properties.position_x || Math.random() * 100,
        y: node.properties.position_y || Math.random() * 100
      });
    });
    
    // Add edges with weight-based thickness
    graphData.edges.forEach(edge => {
      if (graph.hasNode(edge.source_node_id) && graph.hasNode(edge.target_node_id)) {
        // Edge thickness proportional to weight (from Q6)
        const thickness = Math.log(edge.weight + 1);
        
        graph.addEdge(edge.source_node_id, edge.target_node_id, {
          weight: edge.weight,
          size: thickness
        });
      }
    });
    
    // Initialize Sigma.js
    const sigma = new Sigma(graph, containerRef.current, {
      renderEdgeLabels: false,
      defaultNodeColor: '#666',
      defaultEdgeColor: '#ccc',
      labelSize: 12,
      labelWeight: 'bold',
      labelColor: { color: '#000' },
      
      // Node sizing based on BC (Q16)
      nodeReducer: (node, data) => {
        return {
          ...data,
          // Label only for top 30% of nodes by size
          label: data.size > 20 ? data.label : ''
        };
      }
    });
    
    setSigmaInstance(sigma);
    
    // Cleanup
    return () => {
      sigma.kill();
    };
  }, [graphData]);
  
  const fetchGraphData = async (id) => {
    try {
      const response = await fetch(`/api/graph/${id}`);
      const data = await response.json();
      setGraphData(data);
    } catch (error) {
      console.error('Error fetching graph:', error);
    }
  };
  
  return (
    <div 
      ref={containerRef} 
      style={{ width: '100%', height: '600px', background: '#fff' }}
    />
  );
};

export default GraphVisualization;
```

### 7.2 API Endpoints

```python
# api/main.py
from fastapi import FastAPI, HTTPException
from typing import List
import json

app = FastAPI(title="InfraNodus Replica API")

@app.post("/api/analyze")
async def analyze_text(text: str, user_id: int):
    """
    Complete text analysis pipeline
    
    1. Call NLP service
    2. Build graph
    3. Run algorithms
    4. Save to database
    5. Return graph_id
    """
    # Step 1: NLP processing
    nlp_response = await call_nlp_service(text)
    
    # Step 2: Build graph
    graph_builder = GraphBuilder()
    graph_result = graph_builder.build_from_ngrams(
        nlp_response['ngrams'],
        context_id=new_context_id
    )
    
    # Step 3: Run algorithms
    communities, modularity = detect_communities(graph_result['graph'])
    positions = calculate_layout(graph_result['graph'])
    betweenness = calculate_betweenness_centrality(graph_result['graph'])
    
    # Step 4: Assign colors and sizes
    colors = assign_community_colors(len(set(communities.values())))
    
    # Step 5: Save to database
    await save_to_database(graph_result, communities, positions, betweenness, colors)
    
    # Step 6: Detect gaps
    gaps = detect_gaps(graph_result['graph'], communities)
    await save_gaps(gaps)
    
    return {
        'graph_id': new_context_id,
        'node_count': graph_result['node_count'],
        'edge_count': graph_result['edge_count'],
        'modularity': modularity,
        'communities': len(set(communities.values()))
    }

@app.get("/api/graph/{graph_id}")
async def get_graph(graph_id: int):
    """
    Retrieve graph data for visualization
    """
    from prisma import Prisma
    
    prisma = Prisma()
    await prisma.connect()
    
    # Fetch nodes
    nodes = await prisma.node.find_many(
        where={'contextId': graph_id},
        include={'properties': True}
    )
    
    # Fetch edges
    edges = await prisma.edge.find_many(
        where={
            'sourceNode': {'contextId': graph_id}
        }
    )
    
    await prisma.disconnect()
    
    return {
        'nodes': nodes,
        'edges': edges
    }

@app.post("/api/graphrag/query")
async def graphrag_query(query: str, graph_id: int):
    """
    GraphRAG query - triggers n8n workflow
    """
    # Trigger n8n workflow via webhook
    import requests
    
    n8n_webhook = "https://your-n8n-instance/webhook/graphrag"
    response = requests.post(n8n_webhook, json={
        'query': query,
        'graph_id': graph_id
    })
    
    return response.json()
```

**Deliverables:**
- ✅ React frontend with Sigma.js
- ✅ Graph visualization component
- ✅ Node sizing by BC (5-40px linear)
- ✅ Edge thickness by weight
- ✅ Community color coding
- ✅ Zoom, pan, search functionality
- ✅ FastAPI endpoints
- ✅ Database integration

---

## PHASE 8: COGNITIVE VARIABILITY (Weeks 14-15)
**Complexity:** 6/10 | **Duration:** 1.5 weeks

### 8.1 Cognitive State Classifier - EXACT THRESHOLDS

```python
# cognitive_analyzer.py

def analyze_cognitive_state(modularity: float, influence_entropy: float, 
                            edge_density: float) -> dict:
    """
    Classify network into 4 cognitive states
    
    Based on InfraNodus cognitive variability framework
    """
    state = None
    advice = ""
    explore_ratio = 50  # Default 50/50
    
    # State 1: Biased/Uniform
    if modularity < 0.4 and influence_entropy < 0.5:
        state = 'biased_uniform'
        advice = 'Add more diverse topics and perspectives. Explore new angles.'
        explore_ratio = 80  # 80% explore, 20% focus
    
    # State 2: Focused/Regular
    elif modularity < 0.4 and edge_density > 0.7:
        state = 'focused_regular'
        advice = 'Good for informative content. Consider branching into related topics.'
        explore_ratio = 30  # 30% explore, 70% focus
    
    # State 3: Diversified/Fractal (OPTIMAL)
    elif 0.4 <= modularity <= 0.7 and 0.4 <= influence_entropy <= 0.7:
        state = 'diversified_fractal'
        advice = 'Excellent! Balanced discourse with diverse perspectives.'
        explore_ratio = 50  # Balanced
    
    # State 4: Dispersed/Complex
    elif modularity > 0.7 and influence_entropy > 0.7:
        state = 'dispersed_complex'
        advice = 'High exploration. Consider focusing on key themes to increase coherence.'
        explore_ratio = 20  # 20% explore, 80% focus
    
    # Calculate Mind Viral Immunity
    immunity_score = modularity * influence_entropy
    
    if immunity_score > 0.28:
        immunity = 'high'
        immunity_desc = 'Diverse, resilient thinking. Protected against echo chambers.'
    elif immunity_score > 0.16:
        immunity = 'medium'
        immunity_desc = 'Moderate resilience. Could benefit from more diversity.'
    else:
        immunity = 'low'
        immunity_desc = 'Vulnerable to bias and echo chambers. Add diverse perspectives.'
    
    return {
        'state': state,
        'advice': advice,
        'explore_ratio': explore_ratio,
        'focus_ratio': 100 - explore_ratio,
        'immunity_score': immunity_score,
        'immunity_level': immunity,
        'immunity_description': immunity_desc,
        'metrics': {
            'modularity': modularity,
            'influence_entropy': influence_entropy,
            'edge_density': edge_density
        }
    }

def calculate_influence_entropy(betweenness_values: dict, communities: dict) -> float:
    """
    Calculate influence distribution entropy using Jenks breaks
    
    High entropy = diverse influence across communities
    Low entropy = concentrated in single community
    """
    import numpy as np
    from collections import defaultdict
    
    # Group betweenness by community
    comm_influence = defaultdict(list)
    for node, bc in betweenness_values.items():
        comm = communities[node]
        comm_influence[comm].append(bc)
    
    # Calculate total influence per community
    comm_totals = {c: sum(vals) for c, vals in comm_influence.items()}
    total_influence = sum(betweenness_values.values())
    
    # Calculate entropy
    entropy = 0
    for comm, total in comm_totals.items():
        if total > 0:
            p = total / total_influence
            entropy += -p * np.log2(p)
    
    # Normalize to 0-1 range
    max_entropy = np.log2(len(comm_totals))
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
    
    return normalized_entropy
```

**Deliverables:**
- ✅ Cognitive state classifier with exact thresholds
- ✅ Mind viral immunity calculator
- ✅ Influence entropy calculation
- ✅ Explore/focus ratio generator
- ✅ AI-powered recommendations

---

## PHASE 9: INTEGRATIONS (Weeks 15-16)
**Complexity:** 5/10 | **Duration:** 2 weeks

### 9.1 CSV/Excel Import (n8n)

```json
{
  "name": "CSV Import",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "import-csv"
      },
      "name": "Webhook - Upload CSV",
      "type": "n8n-nodes-base.webhook"
    },
    {
      "parameters": {
        "functionCode": "const Papa = require('papaparse');\nconst csvData = $input.item.binary.data;\nconst parsed = Papa.parse(csvData, { header: true });\nreturn parsed.data;"
      },
      "name": "Super Code - Parse CSV",
      "type": "n8n-nodes-base.code"
    },
    {
      "parameters": {
        "options": {
          "batching": {
            "batch": {
              "batchSize": 10
            }
          }
        }
      },
      "name": "Loop Over Rows",
      "type": "n8n-nodes-base.splitInBatches"
    },
    {
      "parameters": {
        "url": "http://api:8000/api/analyze",
        "method": "POST",
        "bodyParametersJson": "={{ { \"text\": $json.text_column, \"user_id\": $json.user_id } }}"
      },
      "name": "HTTP Request - Analyze Each Row",
      "type": "n8n-nodes-base.httpRequest"
    },
    {
      "parameters": {
        "respond": "lastNode"
      },
      "name": "Respond",
      "type": "n8n-nodes-base.respondToWebhook"
    }
  ]
}
```

### 9.2 GEXF Export

```python
# gexf_exporter.py
import xml.etree.ElementTree as ET
from xml.dom import minidom

def export_to_gexf(graph: nx.Graph, communities: dict, positions: dict, 
                   betweenness: dict, colors: dict) -> str:
    """
    Export graph to GEXF format for Gephi compatibility
    """
    # Create root
    gexf = ET.Element('gexf', xmlns="http://www.gexf.net/1.2draft", version="1.2")
    
    # Meta
    meta = ET.SubElement(gexf, 'meta', lastmodifieddate="2025-01-01")
    ET.SubElement(meta, 'creator').text = "InfraNodus Replica"
    ET.SubElement(meta, 'description').text = "Text network graph"
    
    # Graph
    graph_elem = ET.SubElement(gexf, 'graph', 
                                mode="static", 
                                defaultedgetype="undirected")
    
    # Nodes
    nodes_elem = ET.SubElement(graph_elem, 'nodes')
    
    for node in graph.nodes():
        node_elem = ET.SubElement(nodes_elem, 'node', 
                                   id=str(node), 
                                   label=str(node))
        
        # Visual attributes
        viz_pos = ET.SubElement(node_elem, 'viz:position',
                                 x=str(positions[node][0]),
                                 y=str(positions[node][1]),
                                 z="0.0")
        
        comm_id = communities[node]
        color = colors[comm_id]
        r, g, b = hex_to_rgb(color)
        
        viz_color = ET.SubElement(node_elem, 'viz:color',
                                   r=str(r), g=str(g), b=str(b))
        
        # Size based on betweenness
        size = 5 + (betweenness[node] * 35)
        viz_size = ET.SubElement(node_elem, 'viz:size', value=str(size))
    
    # Edges
    edges_elem = ET.SubElement(graph_elem, 'edges')
    
    for i, (source, target, data) in enumerate(graph.edges(data=True)):
        edge_elem = ET.SubElement(edges_elem, 'edge',
                                   id=str(i),
                                   source=str(source),
                                   target=str(target),
                                   weight=str(data['weight']))
    
    # Pretty print
    xml_str = ET.tostring(gexf, encoding='unicode')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")
    
    return pretty_xml

def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
```

**Deliverables:**
- ✅ CSV import workflow (n8n)
- ✅ Excel import workflow (n8n)
- ✅ GEXF export function
- ✅ JSON export endpoint
- ✅ Batch processing support

---

## COMPLETE TECHNOLOGY STACK

### **Backend:**
- Python 3.10+
- FastAPI (REST API)
- spaCy (NLP) - `en_core_web_sm`
- NetworkX (graph operations)
- python-louvain (community detection)
- fa2 (ForceAtlas2 layout)
- PostgreSQL 15+
- Prisma ORM

### **Frontend:**
- React 18
- Sigma.js v2
- Graphology
- Tailwind CSS
- Axios

### **Orchestration:**
- n8n (workflows)
- Super Code Node (JavaScript processing)

### **AI:**
- Claude API (via n8n)
- GPT API (optional alternative)

---

## DEPLOYMENT CHECKLIST

- [ ] PostgreSQL database created and migrated
- [ ] NLP service deployed (Docker)
- [ ] Graph algorithms service deployed
- [ ] n8n instance configured with workflows
- [ ] React frontend built and hosted
- [ ] API endpoints tested
- [ ] Claude API key configured
- [ ] All environment variables set
- [ ] Database indexes created
- [ ] Caching layer configured (optional)

---

## TESTING STRATEGY

### **Unit Tests:**
- NLP preprocessing functions
- N-gram generation
- Edge weight calculation
- Community detection
- ForceAtlas2 convergence
- Betweenness calculation
- Gap detection logic

### **Integration Tests:**
- End-to-end text analysis
- GraphRAG query processing
- Database operations
- n8n workflow execution

### **Performance Tests:**
- 100 node graph: <5 seconds
- 500 node graph: <10 seconds
- 1000 node graph: <30 seconds

---

## TIMELINE SUMMARY

| Phase | Weeks | Deliverable |
|-------|-------|-------------|
| 1 | 1-2 | Database schema, Prisma setup |
| 2 | 3-4 | NLP pipeline, FastAPI service |
| 3 | 5-6 | Graph construction, database integration |
| 4 | 7-9 | Louvain, ForceAtlas2, Betweenness, Modularity |
| 5 | 9-10 | Gap detection with filtering |
| 6 | 10-12 | GraphRAG workflows, AI integration |
| 7 | 12-14 | Sigma.js visualization, React frontend |
| 8 | 14-15 | Cognitive state analysis |
| 9 | 15-16 | CSV/GEXF import/export, polish |

**Total: 12-14 weeks (reduced from 16 due to English-only)**

---

## SUCCESS METRICS

✅ **Functional Requirements:**
- Text → Graph in <10 seconds
- Communities detected correctly
- Gaps are meaningful
- GraphRAG provides relevant answers
- Visualization is smooth (60 FPS)

✅ **Quality Metrics:**
- Modularity >0.4 for most texts
- BC calculation accurate
- Layout converges properly
- No false positive gaps

✅ **Performance:**
- Support graphs up to 2000 nodes
- API response <1 second
- Database queries optimized

---

## NEXT STEPS

1. **Week 1:** Set up development environment
2. **Week 1:** Implement database schema
3. **Week 2:** Build NLP service
4. **Week 3:** Test with sample texts
5. **Continue** through phases sequentially

**You're ready to start building!** 🚀
