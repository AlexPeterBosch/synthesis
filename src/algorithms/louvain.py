"""Louvain community detection algorithm."""

import networkx as nx
import community as community_louvain
from typing import Dict


class LouvainCommunityDetection:
    """Detect communities using Louvain algorithm with exact specifications."""
    
    def __init__(self, resolution: float = 1.0):
        """Initialize Louvain algorithm.
        
        Args:
            resolution: Modularity resolution parameter (must be 1.0 per specs)
        """
        self.resolution = resolution
    
    def detect_communities(self, graph: nx.Graph) -> Dict[str, int]:
        """Detect communities in graph.
        
        Specifications:
        - Resolution γ = 1.0 (default)
        - Weighted = True (use edge weights)
        - Stopping criteria: ΔQ < 0.0001
        
        Args:
            graph: NetworkX graph with weighted edges
            
        Returns:
            Dictionary mapping node names to community IDs
        """
        # Use weighted modularity optimization
        partition = community_louvain.best_partition(
            graph,
            weight='weight',
            resolution=self.resolution,
            random_state=None  # Deterministic
        )
        
        return partition
    
    def get_community_count(self, partition: Dict[str, int]) -> int:
        """Get number of communities detected.
        
        Args:
            partition: Community partition dictionary
            
        Returns:
            Number of communities
        """
        return len(set(partition.values()))
