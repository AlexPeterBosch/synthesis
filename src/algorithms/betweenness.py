"""Betweenness Centrality

Exact specifications:
- Algorithm: Brandes' algorithm
- Weighted: True
- Normalized: True (range 0-1)

Used for node sizing: size = 5 + (bc_normalized * 35)
"""

import networkx as nx
from typing import Dict


class BetweennessCentrality:
    """Brandes' betweenness centrality with normalization."""
    
    @staticmethod
    def calculate(graph: nx.Graph, weighted: bool = True, normalized: bool = True) -> Dict[str, float]:
        """Calculate betweenness centrality for all nodes.
        
        Args:
            graph: NetworkX graph
            weighted: Use edge weights (default: True)
            normalized: Normalize to 0-1 range (default: True)
        
        Returns:
            Dictionary mapping node to betweenness centrality value
        """
        bc = nx.betweenness_centrality(
            graph,
            weight='weight' if weighted else None,
            normalized=normalized
        )
        
        return bc
    
    @staticmethod
    def calculate_node_sizes(bc_values: Dict[str, float], 
                            min_size: int = 5, 
                            max_size: int = 40) -> Dict[str, float]:
        """Calculate node sizes from betweenness centrality.
        
        CRITICAL: LINEAR scaling (NOT logarithmic)
        Formula: size = 5 + (bc_normalized * 35)
        
        Args:
            bc_values: Betweenness centrality values
            min_size: Minimum node size in pixels (default: 5)
            max_size: Maximum node size in pixels (default: 40)
        
        Returns:
            Dictionary mapping node to size in pixels
        """
        if not bc_values:
            return {}
        
        # Get min and max BC for normalization
        min_bc = min(bc_values.values())
        max_bc = max(bc_values.values())
        
        # Avoid division by zero
        bc_range = max_bc - min_bc if max_bc > min_bc else 1
        
        node_sizes = {}
        for node, bc in bc_values.items():
            # Normalize BC to 0-1 range
            bc_normalized = (bc - min_bc) / bc_range
            # LINEAR scaling: min_size + (bc_normalized * (max_size - min_size))
            size = min_size + (bc_normalized * (max_size - min_size))
            node_sizes[node] = size
        
        return node_sizes
    
    @staticmethod
    def get_top_nodes(bc_values: Dict[str, float], n: int = 10) -> list:
        """Get top N nodes by betweenness centrality.
        
        Args:
            bc_values: Betweenness centrality values
            n: Number of top nodes to return
        
        Returns:
            List of (node, bc_value) tuples, sorted by BC descending
        """
        sorted_nodes = sorted(bc_values.items(), key=lambda x: x[1], reverse=True)
        return sorted_nodes[:n]
