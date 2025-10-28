"""GraphRAG (Graph Retrieval-Augmented Generation) Module

Provides AI-powered insights based on graph structure:
- query_processor: Process user queries and extract relevant subgraphs
- context_builder: Build structured context for AI from graph data

Process:
1. User submits query
2. Extract relevant subgraph (2-hop neighborhood)
3. Build context: top concepts, relations, gaps, metrics
4. Send to AI with structured context
5. Return insight with sources
"""

from .query_processor import QueryProcessor
from .context_builder import ContextBuilder

__all__ = ["QueryProcessor", "ContextBuilder"]
