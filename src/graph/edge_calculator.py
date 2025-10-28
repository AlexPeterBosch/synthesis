"""Edge weight calculation and management."""

from typing import Dict, Tuple


class EdgeCalculator:
    """Calculate and manage edge weights following exact specifications."""
    
    @staticmethod
    def calculate_weight(co_occurrences: list) -> int:
        """Calculate edge weight using ADDITIVE method (NO normalization).
        
        CRITICAL: Sum all co-occurrence weights, NO normalization.
        
        Args:
            co_occurrences: List of individual co-occurrence weights
            
        Returns:
            Total weight (sum of all co-occurrences)
        """
        return sum(co_occurrences)
    
    @staticmethod
    def merge_edge_dictionaries(dict1: Dict[Tuple[str, str], int], 
                                dict2: Dict[Tuple[str, str], int]) -> Dict[Tuple[str, str], int]:
        """Merge two edge dictionaries, adding weights for duplicate edges.
        
        Args:
            dict1: First edge dictionary
            dict2: Second edge dictionary
            
        Returns:
            Merged dictionary with summed weights
        """
        merged = dict1.copy()
        
        for edge, weight in dict2.items():
            if edge in merged:
                merged[edge] += weight
            else:
                merged[edge] = weight
        
        return merged
