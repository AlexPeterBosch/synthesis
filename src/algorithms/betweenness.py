"""Betweenness centrality calculation."""

import networkx as nx
from typing import Dict


class BetweennessCentrality:
    """Calculate betweenness centrality using Brandes' algorithm."""
    
    @staticmethod
    def calculate(graph: nx.Graph) -> Dict[str, float]:
        """Calculate betweenness centrality for all nodes.
        
        Specifications:
        - Algorithm: Brandes' algorithm
        - Weighted: True (use edge weights)
        - Normalized: True (range 0-1)
        
        Args:
            graph: NetworkX graph with weighted edges
            
        Returns:
            Dictionary mapping node names to betweenness centrality values (0-1)
        """
        # Use Brandes' algorithm with edge weights and normalization
        betweenness = nx.betweenness_centrality(
            graph,
            weight='weight',
            normalized=True  # Range [0, 1]
        )
        
        return betweenness
    
    @staticmethod
    def calculate_node_sizes(betweenness: Dict[str, float]) -> Dict[str, float]:
        """Calculate node sizes based on betweenness centrality.
        
        Specifications:
        - Formula: size = 5 + (bc_normalized × 35)
        - Min size: 5 pixels
        - Max size: 40 pixels
        - Ratio: 8:1
        - Type: LINEAR (not logarithmic)
        
        Args:
            betweenness: Dictionary of betweenness centrality values
            
        Returns:
            Dictionary mapping node names to sizes in pixels
        """
        sizes = {}
        
        for node, bc_value in betweenness.items():
            # LINEAR formula (not logarithmic!)
            size = 5 + (bc_value * 35)
            sizes[node] = size
        
        return sizes
