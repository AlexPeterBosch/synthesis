"""Test n-gram weight calculations against exact specifications."""

import pytest
from src.nlp.ngram_generator import NgramGenerator


def test_bigram_weight():
    """Test that bigrams have exact weight of 3."""
    generator = NgramGenerator()
    
    # Test: adjacent words should have weight 3
    lemmas = ["research", "innovation"]
    edges = generator.generate(lemmas)
    
    expected_edge = tuple(sorted(["research", "innovation"]))
    assert expected_edge in edges
    assert edges[expected_edge] == 3, "Bigram weight must be exactly 3"


def test_distance_1_weight():
    """Test that words 1 position apart have weight 2."""
    generator = NgramGenerator()
    
    # Test: words with 1 word between them should have weight 2
    lemmas = ["research", "innovation", "technology"]
    edges = generator.generate(lemmas)
    
    expected_edge = tuple(sorted(["research", "technology"]))
    assert expected_edge in edges
    # research-innovation: 3 (bigram)
    # research-technology: 2 (distance 1)
    # innovation-technology: 3 (bigram)
    assert edges[expected_edge] == 2, "Distance-1 weight must be exactly 2"


def test_distance_2_weight():
    """Test that words 2 positions apart have weight 1."""
    generator = NgramGenerator()
    
    # Test: words with 2 words between them should have weight 1
    lemmas = ["research", "innovation", "technology", "development"]
    edges = generator.generate(lemmas)
    
    expected_edge = tuple(sorted(["research", "development"]))
    assert expected_edge in edges
    # From first window [research, innovation, technology, development]:
    # research-development: 1 (distance 2)
    assert edges[expected_edge] == 1, "Distance-2 weight must be exactly 1"


def test_weight_accumulation():
    """Test that repeated co-occurrences ADD weights."""
    generator = NgramGenerator()
    
    # Test: same pair appearing multiple times should accumulate
    lemmas = ["research", "innovation", "research", "innovation"]
    edges = generator.generate(lemmas)
    
    expected_edge = tuple(sorted(["research", "innovation"]))
    # Should appear twice as bigram: 3 + 3 = 6
    assert edges[expected_edge] == 6, "Weights must accumulate (additive)"


def test_no_normalization():
    """Test that weights are NOT normalized."""
    generator = NgramGenerator()
    
    # Test: raw weights should be preserved
    lemmas = ["a", "b"] * 5  # Repeat 5 times
    edges = generator.generate(lemmas)
    
    expected_edge = tuple(sorted(["a", "b"]))
    # Should be 5 * 3 = 15 (not normalized to 1.0 or any fraction)
    assert edges[expected_edge] == 15, "Weights must NOT be normalized"
    assert isinstance(edges[expected_edge], int), "Weights must be integers"
