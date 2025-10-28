"""Test gap detection thresholds match exact specifications

Validates:
- MIN_COMMUNITY_SIZE: 3 nodes
- MAX_PATH_LENGTH: 6 hops
- DENSITY_THRESHOLD: 0.1 (10%)
- MAX_SIZE_RATIO: 10:1
- MIN_GAP_SCORE: 0.4
- MAX_GAPS_RETURNED: 3
"""

import pytest
import networkx as nx
from src.gaps.gap_detector import GapDetector
from src.gaps.filters import GapFilters


def test_min_community_size():
    """Test communities must have at least 3 nodes."""
    filters = GapFilters()
    
    comm_a = {"n1", "n2"}  # Too small
    comm_b = {"n3", "n4", "n5"}  # OK
    
    assert not filters.size_filter(comm_a, comm_b, min_size=3)
    assert filters.size_filter(comm_b, comm_b, min_size=3)


def test_max_size_ratio():
    """Test size ratio must not exceed 10:1."""
    filters = GapFilters()
    
    comm_a = set(range(3))   # 3 nodes
    comm_b = set(range(31))  # 31 nodes (ratio > 10:1)
    comm_c = set(range(30))  # 30 nodes (ratio = 10:1, OK)
    
    assert not filters.size_filter(comm_a, comm_b, max_ratio=10)
    assert filters.size_filter(comm_a, comm_c, max_ratio=10)


def test_path_length_range():
    """Test gaps must be 2-6 hops apart."""
    filters = GapFilters()
    
    assert not filters.distance_filter(1, min_hops=2, max_hops=6)  # Too close
    assert filters.distance_filter(2, min_hops=2, max_hops=6)      # OK
    assert filters.distance_filter(6, min_hops=2, max_hops=6)      # OK
    assert not filters.distance_filter(7, min_hops=2, max_hops=6)  # Too far


def test_density_threshold():
    """Test density must be < 10%."""
    filters = GapFilters()
    
    assert filters.density_filter(0.05, threshold=0.1)   # 5% < 10%, OK
    assert filters.density_filter(0.09, threshold=0.1)   # 9% < 10%, OK
    assert not filters.density_filter(0.11, threshold=0.1)  # 11% > 10%, fail


def test_max_gaps_returned():
    """Test maximum 3 gaps are returned."""
    # Create graph with many potential gaps
    G = nx.Graph()
    
    # Create 5 small communities
    for i in range(5):
        nodes = [f"c{i}_n{j}" for j in range(3)]
        for n in nodes:
            G.add_node(n)
        # Connect within community
        G.add_edge(nodes[0], nodes[1], weight=5)
        G.add_edge(nodes[1], nodes[2], weight=5)
    
    # Create weak connections between communities
    G.add_edge("c0_n0", "c1_n0", weight=1)
    G.add_edge("c1_n0", "c2_n0", weight=1)
    G.add_edge("c2_n0", "c3_n0", weight=1)
    G.add_edge("c3_n0", "c4_n0", weight=1)
    
    # Assign communities
    communities = {}
    for i in range(5):
        for j in range(3):
            communities[f"c{i}_n{j}"] = i
    
    detector = GapDetector(G, communities)
    gaps = detector.detect_gaps()
    
    assert len(gaps) <= 3, f"Should return max 3 gaps, got {len(gaps)}"


def test_min_gap_score():
    """Test gap score must be > 0.4."""
    # This test validates the threshold constant
    assert GapDetector.MIN_GAP_SCORE == 0.4
