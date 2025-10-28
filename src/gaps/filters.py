"""Filtering utilities for gap detection."""

from typing import List, Dict


class GapFilters:
    """Filtering utilities for five-stage gap detection process."""
    
    @staticmethod
    def size_filter(community_sizes: Dict[int, int], 
                   min_size: int = 3, 
                   max_ratio: float = 10.0) -> List[int]:
        """Stage 1: Filter communities by size.
        
        Args:
            community_sizes: Dictionary mapping community IDs to sizes
            min_size: Minimum community size
            max_ratio: Maximum size ratio between communities
            
        Returns:
            List of valid community IDs
        """
        return [
            comm_id for comm_id, size in community_sizes.items()
            if size >= min_size
        ]
    
    @staticmethod
    def distance_filter(distance: int, min_hops: int = 2, max_hops: int = 6) -> bool:
        """Stage 2: Filter by distance.
        
        Args:
            distance: Shortest path distance
            min_hops: Minimum hop count
            max_hops: Maximum hop count
            
        Returns:
            True if distance is valid
        """
        return min_hops <= distance <= max_hops
    
    @staticmethod
    def density_filter(density: float, max_density: float = 0.1) -> bool:
        """Stage 3: Filter by density.
        
        Args:
            density: Connection density between communities
            max_density: Maximum allowed density
            
        Returns:
            True if density is below threshold
        """
        return density < max_density
