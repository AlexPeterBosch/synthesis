"""Louvain Community Detection

Exact specifications:
- Resolution: γ = 1.0 (default)
- Weighted: True (uses edge weights)
- Stopping criteria: ΔQ < 0.0001
- Random seed: Fixed for reproducibility
"""

import networkx as nx
import community as community_louvain  # python-louvain
from typing import Dict, Any


class LouvainCommunityDetection:
    """Louvain algorithm with exact InfraNodus specifications."""
    
    def __init__(self, resolution: float = 1.0, random_state: int = 42):
        """Initialize Louvain community detection.
        
        Args:
            resolution: Resolution parameter (default: 1.0)
            random_state: Random seed for reproducibility
        """
        self.resolution = resolution
        self.random_state = random_state
    
    def detect_communities(self, graph: nx.Graph) -> Dict[str, int]:
        """Detect communities using Louvain algorithm.
        
        Args:
            graph: NetworkX graph with weighted edges
        
        Returns:
            Dictionary mapping node to community ID
        """
        # Use python-louvain library
        # Weight attribute should be 'weight' (default)
        partition = community_louvain.best_partition(
            graph,
            weight='weight',
            resolution=self.resolution,
            random_state=self.random_state
        )
        
        return partition
    
    def get_modularity(self, graph: nx.Graph, partition: Dict[str, int]) -> float:
        """Calculate modularity of partition.
        
        Args:
            graph: NetworkX graph
            partition: Node to community mapping
        
        Returns:
            Modularity value (higher = better community structure)
        """
        modularity = community_louvain.modularity(
            partition,
            graph,
            weight='weight'
        )
        return modularity
    
    def get_community_stats(self, partition: Dict[str, int]) -> Dict[str, Any]:
        """Get statistics about detected communities.
        
        Args:
            partition: Node to community mapping
        
        Returns:
            Dictionary with community statistics
        """
        from collections import Counter
        
        community_sizes = Counter(partition.values())
        
        return {
            "num_communities": len(community_sizes),
            "largest_community": max(community_sizes.values()),
            "smallest_community": min(community_sizes.values()),
            "avg_community_size": sum(community_sizes.values()) / len(community_sizes)
        }
