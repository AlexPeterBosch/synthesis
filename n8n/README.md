# n8n Workflows for Synthesis

Automation workflows for graph processing and AI integration.

## Workflows

### 1. graphrag-query.json
**Purpose:** Process GraphRAG queries with AI insights

**Flow:**
1. Receive query via webhook
2. Extract relevant subgraph from database
3. Build context (top concepts, relations, gaps)
4. Send to Claude API with context
5. Return AI-generated insights

**Trigger:** POST to /webhook/graphrag-query

**Payload:**
```json
{
  "query": "How are AI tools and customer feedback related?",
  "context_id": 1
}
```

### 2. gap-bridging.json
**Purpose:** Detect and provide insights on structural gaps

**Flow:**
1. Load graph from database
2. Run gap detection algorithm
3. Generate AI insights on bridging gaps
4. Return recommendations

**Trigger:** POST to /webhook/gap-bridging

### 3. csv-import.json
**Purpose:** Import and process CSV data

**Flow:**
1. Receive CSV file
2. Parse rows
3. Process each row through NLP pipeline
4. Build graph
5. Save to database

**Trigger:** POST to /webhook/csv-import

## Setup

1. Install n8n:
```bash
npm install -g n8n
```

2. Start n8n:
```bash
n8n start
```

3. Import workflows:
- Open n8n web interface (http://localhost:5678)
- Click "Import from File"
- Select workflow JSON files

4. Configure credentials:
- Add PostgreSQL credentials
- Add Claude API key
- Configure webhook URLs

## Testing

Test GraphRAG query:
```bash
curl -X POST http://localhost:5678/webhook/graphrag-query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main themes in this discourse?",
    "context_id": 1
  }'
```

## Notes

- Workflows use Super Code nodes for custom JavaScript
- PostgreSQL nodes connect to Synthesis database
- AI Agent nodes use Claude API (via n8n credentials)
- All workflows follow exact specifications from research
