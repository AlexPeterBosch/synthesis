"""Build knowledge graphs from text."""

import networkx as nx
from typing import Dict, Tuple


class GraphBuilder:
    """Build NetworkX graphs from n-gram edges."""
    
    def __init__(self):
        """Initialize graph builder."""
        self.graph = None
    
    def build_from_edges(self, edges: Dict[Tuple[str, str], int]) -> nx.Graph:
        """Build undirected graph from weighted edges.
        
        Edge weights follow additive principle (NO normalization).
        
        Args:
            edges: Dictionary mapping (node1, node2) to weight
            
        Returns:
            NetworkX Graph with weighted edges
        """
        G = nx.Graph()
        
        for (node1, node2), weight in edges.items():
            G.add_edge(node1, node2, weight=weight)
        
        self.graph = G
        return G
    
    def get_graph_metrics(self) -> Dict:
        """Calculate basic graph metrics.
        
        Returns:
            Dictionary of graph metrics
        """
        if self.graph is None:
            return {}
        
        return {
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
            "is_connected": nx.is_connected(self.graph)
        }
