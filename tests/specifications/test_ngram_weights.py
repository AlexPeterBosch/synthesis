"""Test n-gram weight calculations match exact specifications

Validates:
- Pass 1: Bigrams have weight 3
- Pass 2: Distance 1 has weight 2
- Pass 2: Distance 2 has weight 1
- Paragraph breaks stop scanning
"""

import pytest
from src.nlp.ngram_generator import NGramGenerator


def test_bigram_weights():
    """Test Pass 1: Adjacent words have weight 3."""
    generator = NGramGenerator()
    tokens = ["research", "laboratory", "experiment"]
    
    ngrams = generator.generate(tokens)
    
    # Check bigram weights
    bigrams = [(s, t, w) for s, t, w in ngrams if w == 3]
    assert len(bigrams) == 2  # 2 adjacent pairs
    assert ("research", "laboratory", 3) in ngrams
    assert ("laboratory", "experiment", 3) in ngrams


def test_distance_1_weights():
    """Test Pass 2: 1 word apart has weight 2."""
    generator = NGramGenerator()
    tokens = ["research", "laboratory", "experiment", "analysis"]
    
    ngrams = generator.generate(tokens)
    
    # Check distance-1 weights
    distance_1 = [(s, t, w) for s, t, w in ngrams if w == 2]
    assert ("research", "experiment", 2) in ngrams
    assert ("laboratory", "analysis", 2) in ngrams


def test_distance_2_weights():
    """Test Pass 2: 2 words apart has weight 1."""
    generator = NGramGenerator()
    tokens = ["research", "laboratory", "experiment", "analysis"]
    
    ngrams = generator.generate(tokens)
    
    # Check distance-2 weights
    distance_2 = [(s, t, w) for s, t, w in ngrams if w == 1]
    assert ("research", "analysis", 1) in ngrams


def test_paragraph_breaks_stop_scanning():
    """Test that paragraph breaks prevent n-gram scanning across boundaries."""
    generator = NGramGenerator(paragraph_delimiter="\n\n")
    
    # Two paragraphs
    para1_tokens = ["research", "laboratory"]
    para2_tokens = ["experiment", "analysis"]
    
    # Process separately
    ngrams = generator.generate_from_paragraphs(
        text="research laboratory\n\nexperiment analysis",
        tokens_per_para=[para1_tokens, para2_tokens]
    )
    
    # Should NOT have connection between "laboratory" and "experiment"
    invalid_connections = [
        ("laboratory", "experiment", 3),
        ("laboratory", "experiment", 2),
        ("laboratory", "experiment", 1)
    ]
    
    for invalid in invalid_connections:
        assert invalid not in ngrams, "Paragraph break was not respected!"


def test_two_pass_algorithm_completeness():
    """Test that TWO-PASS algorithm generates all expected n-grams."""
    generator = NGramGenerator()
    tokens = ["a", "b", "c", "d"]
    
    ngrams = generator.generate(tokens)
    
    expected_count = (
        3 +  # Pass 1: 3 bigrams (a-b, b-c, c-d)
        2 +  # Pass 2 distance-1: 2 pairs
        1    # Pass 2 distance-2: 1 pair
    )
    
    assert len(ngrams) == expected_count, f"Expected {expected_count} n-grams, got {len(ngrams)}"
