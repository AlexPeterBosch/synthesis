# API Architecture

## FastAPI Structure

### Core Endpoints

**POST /api/analyze**
- Input: text, user_id
- Process: NLP → Graph → Algorithms → Database
- Output: graph_id, metrics

**GET /api/graph/{graph_id}**
- Returns: nodes, edges for visualization

**POST /api/graphrag/query**
- Input: query, graph_id
- Process: Tokenize → Extract subgraph → AI insights
- Output: AI response

**GET /api/gaps/{graph_id}**
- Returns: Top 3 structural gaps

### API Flow

```
Client Request
  ↓
FastAPI Router
  ↓
NLP Service → Graph Builder → Algorithms
  ↓
Database (via Prisma)
  ↓
Response
```

## Reference

- Implementation: `src/api/main.py`