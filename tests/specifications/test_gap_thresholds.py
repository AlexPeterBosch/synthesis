"""Test gap detection thresholds against exact specifications."""

import pytest
from src.gaps.gap_detector import GapDetector
from src.gaps.filters import GapFilters


def test_min_community_size():
    """Test that minimum community size is exactly 3."""
    detector = GapDetector()
    assert detector.min_community_size == 3, "Min community size must be exactly 3"


def test_max_path_length():
    """Test that maximum path length is exactly 6 hops."""
    detector = GapDetector()
    assert detector.max_path_length == 6, "Max path length must be exactly 6 hops"


def test_density_threshold():
    """Test that density threshold is exactly 0.1 (10%)."""
    detector = GapDetector()
    assert detector.density_threshold == 0.1, "Density threshold must be exactly 0.1"


def test_max_size_ratio():
    """Test that max size ratio is exactly 10:1."""
    detector = GapDetector()
    assert detector.max_size_ratio == 10, "Max size ratio must be exactly 10:1"


def test_min_gap_score():
    """Test that minimum gap score is exactly 0.4."""
    detector = GapDetector()
    assert detector.min_gap_score == 0.4, "Min gap score must be exactly 0.4"


def test_max_gaps_returned():
    """Test that maximum gaps returned is exactly 3."""
    detector = GapDetector()
    assert detector.max_gaps_returned == 3, "Max gaps returned must be exactly 3"


def test_distance_filter_range():
    """Test that distance filter accepts only 2-6 hops."""
    # Test valid distances
    assert GapFilters.distance_filter(2) == True, "Distance 2 must be valid"
    assert GapFilters.distance_filter(6) == True, "Distance 6 must be valid"
    assert GapFilters.distance_filter(4) == True, "Distance 4 must be valid"
    
    # Test invalid distances
    assert GapFilters.distance_filter(1) == False, "Distance 1 must be invalid"
    assert GapFilters.distance_filter(7) == False, "Distance 7 must be invalid"


def test_density_filter_threshold():
    """Test that density filter rejects >= 0.1 (10%)."""
    assert GapFilters.density_filter(0.05) == True, "Density 5% must be valid"
    assert GapFilters.density_filter(0.09) == True, "Density 9% must be valid"
    assert GapFilters.density_filter(0.1) == False, "Density 10% must be invalid"
    assert GapFilters.density_filter(0.15) == False, "Density 15% must be invalid"
