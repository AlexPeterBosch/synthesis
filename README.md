# Synthesis

Transform text into interactive knowledge graphs with AI-powered insights.

## Overview

Synthesis analyzes text to create visual knowledge networks, detects structural gaps in thinking, and provides contextual insights through GraphRAG (Graph Retrieval-Augmented Generation).

**Key Features:**
- 📊 Text-to-Knowledge-Graph conversion
- 🔍 Structural gap detection in discourse
- 🤖 AI-powered insights (GraphRAG)
- 🧠 Cognitive variability analysis
- 📈 Community detection and network analysis
- 🎨 Interactive visualization

## Project Status

**Current Phase:** 0 - Repository Setup  
**Progress:** See [PROGRESS.md](PROGRESS.md)

## Architecture

Built with research-backed specifications:
- **NLP:** spaCy (English), TWO-PASS n-gram algorithm
- **Graph:** NetworkX, PostgreSQL + Prisma
- **Algorithms:** Louvain, ForceAtlas2, Brandes' betweenness
- **AI:** Claude API (via n8n)
- **Frontend:** React + Sigma.js

## Quick Start
```bash
# Clone repository
git clone https://github.com/AlexPeterBosch/synthesis.git
cd synthesis

# Setup (coming soon)
./scripts/setup.sh
```

## Documentation

- [Full Specifications](SPECIFICATIONS.md)
- [Development Plans](docs/research/)
- [Quick Reference](docs/research/quick-reference.md)
- [Phase Documentation](docs/phases/)

## Development Timeline

**Estimated:** 12-14 weeks (English-only)

- **Phase 1:** Database Architecture (2 weeks)
- **Phase 2:** NLP Processing (2 weeks)
- **Phase 3:** Graph Construction (2 weeks)
- **Phase 4:** Core Algorithms (3 weeks)
- **Phase 5:** Gap Detection (2 weeks)
- **Phase 6:** GraphRAG (3 weeks)
- **Phase 7:** Visualization (2 weeks)
- **Phase 8:** Cognitive Analysis (1.5 weeks)
- **Phase 9:** Integrations (2 weeks)

## Technology Stack

**Backend:** Python 3.10+, FastAPI, spaCy, NetworkX, PostgreSQL, Prisma  
**Frontend:** React 18, Sigma.js, Graphology, Tailwind CSS  
**Orchestration:** n8n  
**AI:** Claude API

## License

MIT License - See [LICENSE](LICENSE)

## Acknowledgments

Built with exact specifications from comprehensive research into text network analysis and knowledge graph systems.
