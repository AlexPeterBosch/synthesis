"""Edge Weight Calculator

CRITICAL: ADDITIVE weighting WITHOUT normalization.

Example:
- "research" and "laboratory" appear 5 times as bigrams: 3+3+3+3+3 = 15
- They also appear 3 times with 1 word between: 2+2+2 = 6
- Final weight = 15 + 6 = 21 (NO normalization)
"""

from typing import List, Tuple, Dict
from collections import defaultdict


class EdgeCalculator:
    """Calculate edge weights with ADDITIVE method (no normalization)."""
    
    @staticmethod
    def calculate_weights(ngrams: List[Tuple[str, str, int]]) -> Dict[Tuple[str, str], int]:
        """Calculate final edge weights from n-grams.
        
        Args:
            ngrams: List of (source, target, weight) tuples
        
        Returns:
            Dictionary mapping edge to final weight
        """
        edge_weights = defaultdict(int)
        
        for source, target, weight in ngrams:
            # Undirected edge (sorted order for consistency)
            edge_key = tuple(sorted([source, target]))
            # ADDITIVE: sum all weights
            edge_weights[edge_key] += weight
        
        return dict(edge_weights)
    
    @staticmethod
    def validate_no_normalization(edge_weights: Dict[Tuple[str, str], int]) -> bool:
        """Verify that weights are not normalized.
        
        Normalized weights would typically be in 0-1 range.
        Our weights should be integers >= 1.
        
        Args:
            edge_weights: Dictionary of edge weights
        
        Returns:
            True if weights appear non-normalized (all >= 1)
        """
        if not edge_weights:
            return True
        
        return all(weight >= 1 for weight in edge_weights.values())
