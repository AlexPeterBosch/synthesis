"""Test node sizing calculations against exact specifications."""

import pytest
from src.algorithms.betweenness import BetweennessCentrality


def test_node_size_formula():
    """Test that node size follows exact linear formula."""
    # Specification: size = 5 + (bc_normalized × 35)
    
    betweenness = {
        "node1": 0.0,    # Min BC
        "node2": 0.5,    # Mid BC
        "node3": 1.0,    # Max BC
    }
    
    sizes = BetweennessCentrality.calculate_node_sizes(betweenness)
    
    # Test minimum size
    assert sizes["node1"] == 5, "Minimum size must be exactly 5 pixels"
    
    # Test mid-range size (linear)
    assert sizes["node2"] == 5 + (0.5 * 35), "Mid-range size must follow linear formula"
    assert sizes["node2"] == 22.5, "Size calculation must be precise"
    
    # Test maximum size
    assert sizes["node3"] == 40, "Maximum size must be exactly 40 pixels"


def test_size_ratio():
    """Test that max:min size ratio is exactly 8:1."""
    min_size = 5
    max_size = 40
    
    ratio = max_size / min_size
    assert ratio == 8.0, "Size ratio must be exactly 8:1"


def test_linear_not_logarithmic():
    """Test that sizing is LINEAR, not logarithmic."""
    import math
    
    betweenness = {
        "node1": 0.2,
        "node2": 0.4,
    }
    
    sizes = BetweennessCentrality.calculate_node_sizes(betweenness)
    
    # Linear: doubling BC should roughly double the size increase
    size_increase_1 = sizes["node1"] - 5  # 0.2 * 35 = 7
    size_increase_2 = sizes["node2"] - 5  # 0.4 * 35 = 14
    
    # In linear formula, doubling BC doubles the increase
    assert abs(size_increase_2 - (size_increase_1 * 2)) < 0.01, "Sizing must be linear"
    
    # If it were logarithmic, this would NOT hold
    log_size_1 = 5 + (math.log(0.2 + 1) * 35)
    log_size_2 = 5 + (math.log(0.4 + 1) * 35)
    
    # Our implementation should NOT match logarithmic
    assert sizes["node1"] != pytest.approx(log_size_1), "Must NOT use logarithmic sizing"
