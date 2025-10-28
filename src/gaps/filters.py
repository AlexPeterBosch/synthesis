"""Gap Detection Filters

Five-stage filtering system:
1. Size filters
2. Distance filters
3. Density filters
4. Gap score calculation
5. Semantic validation
"""

from typing import Set


class GapFilters:
    """Filters for gap detection pipeline."""
    
    @staticmethod
    def size_filter(comm_a: Set, comm_b: Set, 
                   min_size: int = 3, 
                   max_ratio: int = 10) -> bool:
        """Filter by community size.
        
        Args:
            comm_a: First community
            comm_b: Second community
            min_size: Minimum community size
            max_ratio: Maximum size ratio
        
        Returns:
            True if passes filter
        """
        size_a = len(comm_a)
        size_b = len(comm_b)
        
        # Check minimum size
        if size_a < min_size or size_b < min_size:
            return False
        
        # Check size ratio
        ratio = max(size_a, size_b) / min(size_a, size_b)
        if ratio > max_ratio:
            return False
        
        return True
    
    @staticmethod
    def distance_filter(path_length: float, 
                       min_hops: int = 2, 
                       max_hops: int = 6) -> bool:
        """Filter by path length.
        
        Args:
            path_length: Shortest path between communities
            min_hops: Minimum hops (default: 2)
            max_hops: Maximum hops (default: 6)
        
        Returns:
            True if passes filter
        """
        if path_length < 0:  # No path
            return False
        
        return min_hops <= path_length <= max_hops
    
    @staticmethod
    def density_filter(density: float, threshold: float = 0.1) -> bool:
        """Filter by density.
        
        Args:
            density: Connection density between communities
            threshold: Maximum allowed density (default: 0.1 = 10%)
        
        Returns:
            True if passes filter (density below threshold)
        """
        return density < threshold
    
    @staticmethod
    def semantic_validation(comm_a_labels: list, comm_b_labels: list) -> bool:
        """Validate semantic relevance of gap.
        
        TODO: Implement semantic similarity checking
        
        Args:
            comm_a_labels: Node labels from community A
            comm_b_labels: Node labels from community B
        
        Returns:
            True if semantically relevant
        """
        # Placeholder: always pass for now
        return True
