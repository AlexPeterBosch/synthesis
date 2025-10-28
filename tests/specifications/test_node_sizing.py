"""Test node sizing calculations match exact specifications

Validates:
- LINEAR scaling (NOT logarithmic)
- Formula: size = 5 + (bc_normalized * 35)
- Min size: 5 pixels
- Max size: 40 pixels
- Ratio: 8:1
"""

import pytest
from src.algorithms.betweenness import BetweennessCentrality


def test_linear_scaling():
    """Test that node sizing uses LINEAR scaling."""
    bc_values = {
        "node_a": 0.0,   # Min BC
        "node_b": 0.5,   # Mid BC
        "node_c": 1.0    # Max BC
    }
    
    sizes = BetweennessCentrality.calculate_node_sizes(bc_values)
    
    # Check linear progression
    assert sizes["node_a"] == 5.0   # Min size
    assert sizes["node_c"] == 40.0  # Max size
    assert sizes["node_b"] == 22.5  # Exactly midpoint (linear)


def test_size_range():
    """Test size range is 5-40 pixels."""
    bc_values = {
        f"node_{i}": i / 100 for i in range(100)
    }
    
    sizes = BetweennessCentrality.calculate_node_sizes(bc_values)
    
    # All sizes must be in range
    assert all(5 <= size <= 40 for size in sizes.values())
    
    # Min and max should be at boundaries
    assert min(sizes.values()) == 5.0
    assert max(sizes.values()) == 40.0


def test_size_ratio():
    """Test max:min ratio is 8:1."""
    bc_values = {"min_node": 0.0, "max_node": 1.0}
    
    sizes = BetweennessCentrality.calculate_node_sizes(bc_values)
    
    ratio = sizes["max_node"] / sizes["min_node"]
    assert ratio == 8.0, f"Expected 8:1 ratio, got {ratio}:1"


def test_not_logarithmic():
    """Test that sizing is NOT logarithmic."""
    import math
    
    bc_values = {
        "node_a": 0.0,
        "node_b": 0.5,
        "node_c": 1.0
    }
    
    sizes = BetweennessCentrality.calculate_node_sizes(bc_values)
    
    # If logarithmic, midpoint would be: 5 + log(0.5+1) * 35 ≈ 29.6
    # But linear gives: 5 + 0.5 * 35 = 22.5
    log_size = 5 + math.log(0.5 + 1) * 35
    
    assert sizes["node_b"] == 22.5, "Sizing is not linear!"
    assert abs(sizes["node_b"] - log_size) > 5, "Sizing appears logarithmic!"
