"""Gap Detection Algorithm

Five-stage filtering process with exact thresholds:
- MIN_COMMUNITY_SIZE: 3 nodes
- MAX_PATH_LENGTH: 6 hops
- DENSITY_THRESHOLD: 0.1 (10%)
- MAX_SIZE_RATIO: 10:1
- MIN_GAP_SCORE: 0.4
- MAX_GAPS_RETURNED: 3
"""

import networkx as nx
from typing import List, Dict, Tuple, Any
from .filters import GapFilters


class GapDetector:
    """Detect structural gaps between communities."""
    
    # Exact thresholds from specifications
    MIN_COMMUNITY_SIZE = 3
    MAX_PATH_LENGTH = 6
    DENSITY_THRESHOLD = 0.1
    MAX_SIZE_RATIO = 10
    MIN_GAP_SCORE = 0.4
    MAX_GAPS_RETURNED = 3
    
    def __init__(self, graph: nx.Graph, communities: Dict[str, int]):
        """Initialize gap detector.
        
        Args:
            graph: NetworkX graph
            communities: Node to community ID mapping
        """
        self.graph = graph
        self.communities = communities
        self.filters = GapFilters()
    
    def detect_gaps(self) -> List[Dict[str, Any]]:
        """Detect gaps using five-stage filtering process.
        
        Returns:
            List of gap dictionaries (max 3), sorted by gap score
        """
        # Get community pairs
        community_sets = self._get_community_sets()
        community_pairs = self._get_community_pairs(community_sets)
        
        gaps = []
        
        for comm_a_id, comm_b_id in community_pairs:
            comm_a = community_sets[comm_a_id]
            comm_b = community_sets[comm_b_id]
            
            # Stage 1: Size filters
            if not self.filters.size_filter(comm_a, comm_b, 
                                            self.MIN_COMMUNITY_SIZE, 
                                            self.MAX_SIZE_RATIO):
                continue
            
            # Stage 2: Distance filters
            path_length = self._get_shortest_path_length(comm_a, comm_b)
            if not self.filters.distance_filter(path_length, 2, self.MAX_PATH_LENGTH):
                continue
            
            # Stage 3: Density filter
            density = self._calculate_density(comm_a, comm_b)
            if not self.filters.density_filter(density, self.DENSITY_THRESHOLD):
                continue
            
            # Stage 4: Gap score calculation
            gap_score = self._calculate_gap_score(comm_a, comm_b, path_length, density)
            if gap_score < self.MIN_GAP_SCORE:
                continue
            
            # Stage 5: Semantic validation (simplified for now)
            # TODO: Implement semantic validation
            
            gaps.append({
                "community_a_id": comm_a_id,
                "community_b_id": comm_b_id,
                "community_a_nodes": list(comm_a),
                "community_b_nodes": list(comm_b),
                "gap_score": gap_score,
                "path_length": path_length,
                "density": density,
                "size_a": len(comm_a),
                "size_b": len(comm_b)
            })
        
        # Sort by gap score (descending) and return top 3
        gaps.sort(key=lambda x: x['gap_score'], reverse=True)
        return gaps[:self.MAX_GAPS_RETURNED]
    
    def _get_community_sets(self) -> Dict[int, set]:
        """Convert communities dict to sets."""
        community_sets = {}
        for node, comm_id in self.communities.items():
            if comm_id not in community_sets:
                community_sets[comm_id] = set()
            community_sets[comm_id].add(node)
        return community_sets
    
    def _get_community_pairs(self, community_sets: Dict[int, set]) -> List[Tuple[int, int]]:
        """Get all pairs of communities."""
        comm_ids = list(community_sets.keys())
        pairs = []
        for i in range(len(comm_ids)):
            for j in range(i + 1, len(comm_ids)):
                pairs.append((comm_ids[i], comm_ids[j]))
        return pairs
    
    def _get_shortest_path_length(self, comm_a: set, comm_b: set) -> float:
        """Get shortest path between two communities."""
        min_path = float('inf')
        
        for node_a in comm_a:
            for node_b in comm_b:
                try:
                    path_length = nx.shortest_path_length(self.graph, node_a, node_b)
                    min_path = min(min_path, path_length)
                except nx.NetworkXNoPath:
                    continue
        
        return min_path if min_path != float('inf') else -1
    
    def _calculate_density(self, comm_a: set, comm_b: set) -> float:
        """Calculate density of connections between communities."""
        actual_edges = 0
        possible_edges = len(comm_a) * len(comm_b)
        
        for node_a in comm_a:
            for node_b in comm_b:
                if self.graph.has_edge(node_a, node_b):
                    actual_edges += 1
        
        return actual_edges / possible_edges if possible_edges > 0 else 0
    
    def _calculate_gap_score(self, comm_a: set, comm_b: set, 
                            path_length: float, density: float) -> float:
        """Calculate gap score.
        
        Formula: (1 - density) * (1/path_length) * community_similarity
        """
        if path_length <= 0:
            return 0
        
        # Simplified gap score (can be enhanced with semantic similarity)
        gap_score = (1 - density) * (1 / path_length)
        
        return gap_score
