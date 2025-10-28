"""Graph Construction

Builds NetworkX graph from n-grams with EXACT weight calculation:
- ADDITIVE weighting (sum all co-occurrences)
- NO normalization
- Raw weights used in all algorithms
"""

import networkx as nx
from typing import List, Tuple, Dict
from collections import defaultdict


class GraphBuilder:
    """Build graph from n-grams following exact InfraNodus specifications."""
    
    def __init__(self):
        """Initialize graph builder."""
        self.graph = None
    
    def build_from_ngrams(self, ngrams: List[Tuple[str, str, int]]) -> nx.Graph:
        """Build graph from n-grams with ADDITIVE weights.
        
        Critical: NO normalization applied!
        
        Args:
            ngrams: List of (source, target, weight) tuples
        
        Returns:
            NetworkX graph with weighted edges
        """
        edge_weights = defaultdict(int)
        
        # Accumulate weights (ADDITIVE)
        for source, target, weight in ngrams:
            # Create undirected edge key (sorted order)
            edge_key = tuple(sorted([source, target]))
            edge_weights[edge_key] += weight
        
        # Build NetworkX graph
        graph = nx.Graph()
        
        for (source, target), final_weight in edge_weights.items():
            graph.add_edge(source, target, weight=final_weight)
        
        self.graph = graph
        return graph
    
    def get_graph_stats(self) -> Dict[str, int]:
        """Get basic graph statistics.
        
        Returns:
            Dictionary with node count, edge count, etc.
        """
        if not self.graph:
            return {}
        
        return {
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges(),
            "avg_degree": sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes(),
            "density": nx.density(self.graph)
        }
