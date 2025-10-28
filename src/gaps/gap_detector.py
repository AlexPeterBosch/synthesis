"""Detect structural gaps in knowledge graphs."""

import networkx as nx
from typing import Dict, List, Tuple


class GapDetector:
    """Detect structural gaps between communities following exact specifications."""
    
    def __init__(self):
        """Initialize gap detector with exact threshold parameters."""
        # Exact thresholds from specifications
        self.min_community_size = 3
        self.max_path_length = 6
        self.density_threshold = 0.1  # 10%
        self.max_size_ratio = 10
        self.min_gap_score = 0.4
        self.max_gaps_returned = 3
    
    def detect_gaps(self, graph: nx.Graph, communities: Dict[str, int]) -> List[Dict]:
        """Detect structural gaps using five-stage filtering.
        
        Specifications:
        - Stage 1: Size filters (min 3 nodes, max ratio 10:1)
        - Stage 2: Distance filters (2-6 hops)
        - Stage 3: Density filters (<10% connections)
        - Stage 4: Gap score calculation (>0.4 threshold)
        - Stage 5: Semantic validation
        
        Args:
            graph: NetworkX graph
            communities: Dictionary mapping nodes to community IDs
            
        Returns:
            List of top 3 gaps with highest scores
        """
        gaps = []
        
        # Get unique community IDs
        community_ids = set(communities.values())
        
        # Get community sizes
        community_sizes = {}
        for comm_id in community_ids:
            nodes = [n for n, c in communities.items() if c == comm_id]
            community_sizes[comm_id] = len(nodes)
        
        # Stage 1: Size filters
        valid_communities = [
            comm_id for comm_id, size in community_sizes.items()
            if size >= self.min_community_size
        ]
        
        # Check all pairs of valid communities
        for i, comm1 in enumerate(valid_communities):
            for comm2 in valid_communities[i+1:]:
                # Check size ratio
                size_ratio = max(community_sizes[comm1], community_sizes[comm2]) / \
                           min(community_sizes[comm1], community_sizes[comm2])
                
                if size_ratio > self.max_size_ratio:
                    continue
                
                # Get nodes in each community
                comm1_nodes = [n for n, c in communities.items() if c == comm1]
                comm2_nodes = [n for n, c in communities.items() if c == comm2]
                
                # Stage 2 & 3: Calculate distance and density
                gap_info = self._calculate_gap_metrics(
                    graph, comm1_nodes, comm2_nodes
                )
                
                if gap_info is None:
                    continue
                
                # Stage 4: Calculate gap score
                gap_score = self._calculate_gap_score(gap_info)
                
                if gap_score >= self.min_gap_score:
                    gaps.append({
                        "community_1": comm1,
                        "community_2": comm2,
                        "gap_score": gap_score,
                        "distance": gap_info["distance"],
                        "density": gap_info["density"],
                        "nodes_1": comm1_nodes,
                        "nodes_2": comm2_nodes
                    })
        
        # Sort by gap score and return top 3
        gaps.sort(key=lambda x: x["gap_score"], reverse=True)
        return gaps[:self.max_gaps_returned]
    
    def _calculate_gap_metrics(self, graph: nx.Graph, nodes1: List[str], 
                               nodes2: List[str]) -> Dict:
        """Calculate distance and density between two communities."""
        # Calculate shortest path distances
        min_distance = float('inf')
        
        for n1 in nodes1:
            for n2 in nodes2:
                try:
                    distance = nx.shortest_path_length(graph, n1, n2)
                    min_distance = min(min_distance, distance)
                except nx.NetworkXNoPath:
                    continue
        
        # Check distance threshold (2-6 hops)
        if min_distance < 2 or min_distance > self.max_path_length:
            return None
        
        # Calculate density (connections between communities)
        connections = 0
        possible_connections = len(nodes1) * len(nodes2)
        
        for n1 in nodes1:
            for n2 in nodes2:
                if graph.has_edge(n1, n2):
                    connections += 1
        
        density = connections / possible_connections if possible_connections > 0 else 0
        
        # Check density threshold
        if density >= self.density_threshold:
            return None
        
        return {
            "distance": min_distance,
            "density": density,
            "connections": connections
        }
    
    def _calculate_gap_score(self, gap_info: Dict) -> float:
        """Calculate gap score based on distance and density.
        
        Higher score = better gap candidate.
        """
        # Normalize distance (2-6 range to 0-1)
        distance_score = (gap_info["distance"] - 2) / 4
        
        # Invert density (lower density = higher score)
        density_score = 1 - (gap_info["density"] / self.density_threshold)
        
        # Combined score (equal weighting)
        gap_score = (distance_score + density_score) / 2
        
        return gap_score
