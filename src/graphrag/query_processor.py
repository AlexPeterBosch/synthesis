"""GraphRAG Query Processor

Processes user queries and extracts relevant subgraphs.

Subgraph extraction:
- Method: 2-hop neighborhood
- Find nodes overlapping with query terms
- Include connected nodes within 2 hops
- Maintain edge weights and community structure
"""

import networkx as nx
from typing import List, Dict, Set, Any


class QueryProcessor:
    """Process queries and extract relevant subgraphs."""
    
    def __init__(self, graph: nx.Graph, communities: Dict[str, int] = None):
        """Initialize query processor.
        
        Args:
            graph: NetworkX graph
            communities: Optional node to community ID mapping
        """
        self.graph = graph
        self.communities = communities or {}
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process query and extract relevant information.
        
        Args:
            query: User query string
        
        Returns:
            Dictionary with query results
        """
        # Tokenize and clean query
        query_terms = self._tokenize_query(query)
        
        # Find relevant nodes
        relevant_nodes = self._find_relevant_nodes(query_terms)
        
        # Extract subgraph (2-hop neighborhood)
        subgraph = self._extract_subgraph(relevant_nodes, hops=2)
        
        return {
            "query": query,
            "query_terms": query_terms,
            "relevant_nodes": relevant_nodes,
            "subgraph": subgraph,
            "subgraph_size": len(subgraph.nodes())
        }
    
    def _tokenize_query(self, query: str) -> List[str]:
        """Tokenize query into terms.
        
        Args:
            query: Query string
        
        Returns:
            List of query terms
        """
        # Simple tokenization (can be enhanced with NLP)
        terms = query.lower().split()
        # Remove common question words
        stopwords = {'how', 'what', 'when', 'where', 'why', 'are', 'is', 'the', 'a', 'an'}
        terms = [t for t in terms if t not in stopwords]
        return terms
    
    def _find_relevant_nodes(self, query_terms: List[str]) -> List[str]:
        """Find nodes that match query terms.
        
        Args:
            query_terms: List of query terms
        
        Returns:
            List of relevant node IDs
        """
        relevant_nodes = []
        
        for node in self.graph.nodes():
            # Check if node label contains any query term
            node_label = str(node).lower()
            for term in query_terms:
                if term in node_label:
                    relevant_nodes.append(node)
                    break
        
        return relevant_nodes
    
    def _extract_subgraph(self, seed_nodes: List[str], hops: int = 2) -> nx.Graph:
        """Extract subgraph around seed nodes.
        
        Uses 2-hop neighborhood as specified.
        
        Args:
            seed_nodes: Starting nodes
            hops: Number of hops to expand (default: 2)
        
        Returns:
            Subgraph as NetworkX graph
        """
        if not seed_nodes:
            return nx.Graph()
        
        # Get all nodes within N hops
        subgraph_nodes = set(seed_nodes)
        
        for node in seed_nodes:
            # Use ego_graph for N-hop neighborhood
            if node in self.graph:
                ego = nx.ego_graph(self.graph, node, radius=hops)
                subgraph_nodes.update(ego.nodes())
        
        # Extract subgraph
        subgraph = self.graph.subgraph(subgraph_nodes).copy()
        
        return subgraph
