# Phase 6 Validation

## Context Format Verification

```
Context should include:
- Main topics (by community)
- Top 10 concepts (by betweenness)
- Top 15 relations (by weight)
- Top 5 gaps
- Graph metrics
```

## Test Query

```
Query: "How are AI tools and customer feedback related?"

Expected:
- Find nodes with "ai", "tool", "customer", "feedback"
- Extract 2-hop subgraph
- Provide contextual answer
```

## Success Criteria

Workflow responds with relevant, contextual insights.