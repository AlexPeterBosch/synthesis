# Synthesis Frontend

React-based frontend for Synthesis knowledge graph system.

## Technology Stack

- **React 18**: UI framework
- **Sigma.js v2**: WebGL graph visualization
- **Graphology**: Graph data structure
- **Tailwind CSS**: Styling
- **Axios**: HTTP client

## Setup

```bash
cd src/frontend
npm install
npm start
```

## Visualization Specifications

### Node Sizing
- **Formula**: size = 5 + (bc_normalized × 35)
- **Range**: 5-40 pixels
- **Type**: LINEAR (NOT logarithmic)

### Node Labels
- Display threshold: > 20 pixels
- Shows approximately top 30% of nodes

### Edge Thickness
- **Formula**: thickness = log(weight + 1)

### Colors
- Community-based coloring
- HSL color space
- Saturation: 75%
- Lightness: 55%

## Components

- `GraphVisualization`: Main Sigma.js visualization
- `TextInput`: Text processing interface
- `GapDisplay`: Structural gap visualization
- `MetricsPanel`: Graph metrics display
- `QueryInterface`: GraphRAG query interface

## API Integration

Base URL: `http://localhost:8000/api/v1`

Endpoints:
- POST `/nlp/process` - Process text
- POST `/graph/build` - Build graph
- POST `/gaps/detect` - Detect gaps
- POST `/graphrag/query` - Query with AI
- GET `/viz/graph/:id` - Get visualization data
