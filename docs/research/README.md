# Research Documentation

This directory contains all the research-backed specifications and development plans for the Synthesis project.

## 📚 Documentation Overview

### Core Documents

- **[quick-reference.md](quick-reference.md)** - Essential specifications at a glance. Print this!
- **[development-plan-part1.md](development-plan-part1.md)** - Phases 1-5 (Database through Gap Detection)
- **[development-plan-part2.md](development-plan-part2.md)** - Phases 6-9 (GraphRAG through Integrations)

### Research Foundation

All specifications in this project are based on comprehensive research that answered 50 critical implementation questions about:

- NLP processing algorithms
- Graph construction methods
- Community detection parameters
- Layout algorithm settings
- Gap detection strategies
- GraphRAG implementation
- Cognitive state analysis

## 🎯 Quick Reference

### Key Parameters

**N-gram Algorithm:**
- Pass 1: Bigrams (weight=3)
- Pass 2: 4-gram window (weights 2 and 1)
- Paragraph breaks STOP scanning

**Graph Algorithms:**
- Louvain: resolution=1.0, weighted=true
- ForceAtlas2: gravity=1.0, scalingRatio=20.0
- Betweenness: Brandes' algorithm, normalized

**Node Sizing:**
- Linear: size = 5 + (bc_normalized * 35)
- Range: 5-40 pixels (8:1 ratio)

**Gap Detection:**
- Min community size: 3 nodes
- Max path length: 6 hops
- Density threshold: 0.1 (10%)
- Return top 3 gaps

### Processing Order (CRITICAL)

1. Tokenize
2. Remove special chars
3. Remove URLs
4. Remove numbers
5. **Remove stopwords** ← BEFORE lemmatization!
6. **Lemmatize** ← AFTER stopwords!
7. Extract entities (optional)

## 📋 Development Phases

### Phase 1: Database Architecture (Weeks 1-2)
- PostgreSQL schema with JSONB properties
- Prisma ORM setup
- Critical indexes (GIN, composite)

### Phase 2: NLP Processing (Weeks 3-4)
- spaCy English pipeline
- 180+ stopwords
- TWO-PASS n-gram algorithm
- Entity extraction (3 modes)

### Phase 3: Graph Construction (Weeks 5-6)
- NetworkX graph building
- ADDITIVE edge weights (no normalization)
- Database persistence

### Phase 4: Core Algorithms (Weeks 7-9)
- Louvain community detection
- ForceAtlas2 layout
- Brandes' betweenness centrality
- Newman-Girvan modularity

### Phase 5: Gap Detection (Weeks 9-10)
- 5-stage filtering
- Topological distance
- Connection density
- Bridging concepts

### Phase 6: GraphRAG (Weeks 10-12)
- n8n workflow orchestration
- 2-hop subgraph extraction
- Claude API integration
- Context building

### Phase 7: Visualization (Weeks 12-14)
- React + Sigma.js
- Community colors (HSL)
- Interactive exploration
- 60 FPS target

### Phase 8: Cognitive Analysis (Week 14-15)
- State detection (biased/focused/diversified/dispersed)
- Mind viral immunity score
- Exploration suggestions

### Phase 9: Integrations (Weeks 15-16)
- CSV/Excel import
- GEXF export for Gephi
- Batch processing

## ⚠️ Critical Implementation Rules

### DO:
✅ Use EXACT parameters from specs/parameters.json
✅ Remove stopwords BEFORE lemmatization
✅ Use ADDITIVE edge weights (no normalization)
✅ Use LINEAR node sizing (not logarithmic)
✅ Apply all 5 gap detection filters
✅ Stop n-gram scanning at paragraph breaks

### DON'T:
❌ Normalize edge weights
❌ Use logarithmic node sizing
❌ Lemmatize before stopwords
❌ Connect across paragraphs
❌ Skip validation rules
❌ Approximate parameters

## 🧪 Testing Requirements

Before marking any phase complete:

1. All deliverables checked off
2. Unit tests passing
3. Spec validator shows 100% compliance
4. Performance targets met
5. Code committed to GitHub
6. PROGRESS.md updated

## 📊 Performance Targets

- Text processing: <5s (500 words)
- Graph construction: <10s (500 nodes)
- Louvain: <2s (1000 nodes)
- ForceAtlas2: <30s (1000 nodes)
- Betweenness: <5s (500 nodes)
- GraphRAG query: <3s total

## 🔗 Technology Stack

**Backend:**
- Python 3.10+, FastAPI
- spaCy (en_core_web_sm)
- NetworkX, python-louvain, fa2
- PostgreSQL 15+, Prisma

**Frontend:**
- React 18, Sigma.js v2
- Graphology, Tailwind CSS

**Orchestration:**
- n8n with Super Code Node
- Claude API

## 📖 How to Use This Documentation

1. **Starting a Phase?** Read the relevant development plan section
2. **Need Quick Info?** Check the quick reference
3. **Implementing an Algorithm?** Refer to SPECIFICATIONS.md in root
4. **Validation?** Use specs/parameters.json for exact values

## 🎓 Research Methodology

All specifications were derived through:
- Analysis of InfraNodus source code patterns
- Algorithm parameter validation
- Performance benchmarking
- Best practices from NLP and graph theory
- 50 comprehensive research questions answered

## 💡 Notes

- English-only implementation (simplifies NLP)
- All specs must be followed exactly
- No approximations allowed
- Timeline: 12-14 weeks total
- Use Phase 0 for project setup

---

**Last Updated:** October 28, 2025
**Status:** Complete research, ready for implementation
