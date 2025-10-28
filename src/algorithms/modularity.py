"""Modularity Calculator

Newman-Girvan weighted modularity:
Q = (1/2m) Σ [Aᵢⱼ - (kᵢkⱼ)/(2m)] δ(cᵢ,cⱼ)

Thresholds:
- Q > 0.4: Strong community structure
- Q > 0.7: Very strong (possibly disconnected)
"""

import networkx as nx
from typing import Dict


class ModularityCalculator:
    """Calculate Newman-Girvan modularity with exact thresholds."""
    
    # Threshold constants
    STRONG_THRESHOLD = 0.4
    VERY_STRONG_THRESHOLD = 0.7
    
    @staticmethod
    def calculate(graph: nx.Graph, communities: Dict[str, int]) -> float:
        """Calculate weighted modularity.
        
        Args:
            graph: NetworkX graph with weighted edges
            communities: Node to community ID mapping
        
        Returns:
            Modularity value Q
        """
        # Convert community dict to list of sets format
        community_sets = {}
        for node, comm_id in communities.items():
            if comm_id not in community_sets:
                community_sets[comm_id] = set()
            community_sets[comm_id].add(node)
        
        community_list = list(community_sets.values())
        
        # Calculate modularity using NetworkX
        modularity = nx.community.modularity(graph, community_list, weight='weight')
        
        return modularity
    
    @staticmethod
    def interpret_modularity(modularity: float) -> Dict[str, any]:
        """Interpret modularity value.
        
        Args:
            modularity: Modularity value Q
        
        Returns:
            Dictionary with interpretation
        """
        if modularity < 0.4:
            strength = "weak"
            description = "Graph is too interconnected or poorly structured"
        elif modularity < 0.7:
            strength = "strong"
            description = "Good community structure - optimal range"
        else:
            strength = "very_strong"
            description = "Very strong communities - may be disconnected"
        
        return {
            "modularity": modularity,
            "strength": strength,
            "description": description,
            "thresholds": {
                "strong": ModularityCalculator.STRONG_THRESHOLD,
                "very_strong": ModularityCalculator.VERY_STRONG_THRESHOLD
            }
        }
