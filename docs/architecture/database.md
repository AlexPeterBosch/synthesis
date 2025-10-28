# Database Architecture

## Schema Overview

**Tables:** 7 total
- users
- contexts (graph instances)
- nodes (5 types: concept, statement, context, user, narrative)
- edges (7 relationship types)
- statements (original text)
- graph_metrics

## Critical Design Decisions

### JSONB for Properties
Node and edge properties stored as JSONB for flexibility:
```json
{
  "betweenness_centrality": 0.045,
  "community_id": 3,
  "color": "#FF5733",
  "size": 15,
  "position_x": 123.45,
  "position_y": 67.89
}
```

### Indexes
**Performance critical:**
- GIN index on nodes.properties (fast JSONB queries)
- Composite index on edges(source_node_id, target_node_id)
- All foreign keys indexed

## Complete Schema

See: `database/schema.sql`

## Reference

- Specifications: `SPECIFICATIONS.md`
- Parameters: `specs/parameters.json`