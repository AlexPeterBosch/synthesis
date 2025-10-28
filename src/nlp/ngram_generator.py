"""N-gram generation using TWO-PASS algorithm."""

from typing import List, Dict, Tuple
from collections import defaultdict


class NgramGenerator:
    """Generate n-grams using exact TWO-PASS algorithm from specifications."""
    
    def __init__(self):
        """Initialize n-gram generator with exact parameters."""
        # Pass 1: Bigram weights
        self.bigram_weight = 3
        
        # Pass 2: 4-gram window weights
        self.distance_weights = {
            0: 3,  # Adjacent (handled by Pass 1)
            1: 2,  # 1 word apart
            2: 1   # 2 words apart
        }
        
        self.window_size = 4
    
    def generate(self, lemmas: List[str]) -> Dict[Tuple[str, str], int]:
        """Generate n-grams using TWO-PASS algorithm.
        
        PASS 1: Bigrams (adjacent words) with weight 3
        PASS 2: 4-gram window with distance-based weights
        
        Args:
            lemmas: List of lemmatized words
            
        Returns:
            Dictionary mapping (word1, word2) tuples to weights
        """
        edges = defaultdict(int)
        
        # PASS 1: Bigram scan
        for i in range(len(lemmas) - 1):
            word1 = lemmas[i]
            word2 = lemmas[i + 1]
            # Always store as sorted tuple for undirected graph
            edge = tuple(sorted([word1, word2]))
            edges[edge] += self.bigram_weight
        
        # PASS 2: 4-gram window scan
        for i in range(len(lemmas) - self.window_size + 1):
            window = lemmas[i:i + self.window_size]
            
            # Generate all pairs in window with distance-based weights
            for j in range(len(window)):
                for k in range(j + 1, len(window)):
                    distance = k - j - 1  # Distance between words
                    
                    if distance in self.distance_weights:
                        word1 = window[j]
                        word2 = window[k]
                        edge = tuple(sorted([word1, word2]))
                        
                        # Skip if distance is 0 (already handled by Pass 1)
                        if distance > 0:
                            edges[edge] += self.distance_weights[distance]
        
        return dict(edges)
    
    def process_paragraphs(self, paragraphs: List[List[str]]) -> Dict[Tuple[str, str], int]:
        """Process multiple paragraphs, resetting at paragraph breaks.
        
        CRITICAL: Paragraph breaks (\\n\\n) STOP scanning.
        
        Args:
            paragraphs: List of paragraph lemma lists
            
        Returns:
            Combined edge dictionary
        """
        all_edges = defaultdict(int)
        
        for paragraph_lemmas in paragraphs:
            paragraph_edges = self.generate(paragraph_lemmas)
            for edge, weight in paragraph_edges.items():
                all_edges[edge] += weight
        
        return dict(all_edges)
