"""Modularity calculation."""

import networkx as nx
from typing import Dict


class ModularityCalculator:
    """Calculate Newman-Girvan weighted modularity."""
    
    @staticmethod
    def calculate(graph: nx.Graph, communities: Dict[str, int]) -> float:
        """Calculate modularity score for community partition.
        
        Specifications:
        - Formula: Newman-Girvan weighted modularity
        - Q > 0.4: Strong community structure
        - Q > 0.7: Very strong community structure
        
        Args:
            graph: NetworkX graph with weighted edges
            communities: Dictionary mapping nodes to community IDs
            
        Returns:
            Modularity score Q
        """
        # Convert communities dict to list of sets
        community_sets = {}
        for node, comm_id in communities.items():
            if comm_id not in community_sets:
                community_sets[comm_id] = set()
            community_sets[comm_id].add(node)
        
        communities_list = list(community_sets.values())
        
        # Calculate weighted modularity
        modularity = nx.algorithms.community.modularity(
            graph,
            communities_list,
            weight='weight'
        )
        
        return modularity
    
    @staticmethod
    def interpret_modularity(modularity: float) -> str:
        """Interpret modularity score.
        
        Args:
            modularity: Modularity score
            
        Returns:
            Interpretation string
        """
        if modularity > 0.7:
            return "very_strong"
        elif modularity > 0.4:
            return "strong"
        else:
            return "weak"
