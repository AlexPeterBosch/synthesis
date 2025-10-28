"""Process queries for GraphRAG."""

import networkx as nx
from typing import Dict, List, Set


class QueryProcessor:
    """Process user queries and extract relevant subgraphs."""
    
    def __init__(self):
        """Initialize query processor."""
        self.hops = 2  # Exact specification: 2-hop neighborhood
    
    def process_query(self, query: str, graph: nx.Graph) -> Dict:
        """Convert query to graph and find overlapping nodes.
        
        GraphRAG Process:
        1. Query graph construction from user query
        2. Overlap analysis with knowledge base graph
        3. Graph traversal (2-hop neighborhood)
        4. Context extraction
        
        Args:
            query: User query text
            graph: Knowledge base graph
            
        Returns:
            Dictionary with overlapping nodes and subgraph
        """
        # Extract keywords from query (simplified)
        query_keywords = self._extract_keywords(query)
        
        # Find overlapping nodes
        overlapping_nodes = self._find_overlapping_nodes(query_keywords, graph)
        
        if not overlapping_nodes:
            return {
                "overlapping_nodes": [],
                "subgraph": nx.Graph(),
                "context": {}
            }
        
        # Extract 2-hop neighborhood subgraph
        subgraph = self._extract_subgraph(graph, overlapping_nodes)
        
        return {
            "overlapping_nodes": list(overlapping_nodes),
            "subgraph": subgraph,
            "query_keywords": query_keywords
        }
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract keywords from query text.
        
        Args:
            query: Query text
            
        Returns:
            List of keywords
        """
        # Simplified keyword extraction (should use NLP pipeline)
        words = query.lower().split()
        # Remove common words
        stopwords = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or'}
        keywords = [w for w in words if w not in stopwords]
        return keywords
    
    def _find_overlapping_nodes(self, keywords: List[str], graph: nx.Graph) -> Set[str]:
        """Find nodes in graph that match query keywords.
        
        Args:
            keywords: Query keywords
            graph: Knowledge base graph
            
        Returns:
            Set of overlapping node names
        """
        overlapping = set()
        
        for node in graph.nodes():
            for keyword in keywords:
                if keyword.lower() in node.lower():
                    overlapping.add(node)
                    break
        
        return overlapping
    
    def _extract_subgraph(self, graph: nx.Graph, seed_nodes: Set[str]) -> nx.Graph:
        """Extract 2-hop neighborhood subgraph from seed nodes.
        
        Specification: 2-hop neighborhood extraction
        
        Args:
            graph: Full knowledge graph
            seed_nodes: Overlapping nodes to start from
            
        Returns:
            Subgraph containing 2-hop neighborhood
        """
        subgraph_nodes = set(seed_nodes)
        
        # Add 1-hop neighbors
        for node in seed_nodes:
            if node in graph:
                subgraph_nodes.update(graph.neighbors(node))
        
        # Add 2-hop neighbors
        one_hop_neighbors = subgraph_nodes.copy()
        for node in one_hop_neighbors:
            if node in graph:
                subgraph_nodes.update(graph.neighbors(node))
        
        # Extract subgraph
        return graph.subgraph(subgraph_nodes).copy()
