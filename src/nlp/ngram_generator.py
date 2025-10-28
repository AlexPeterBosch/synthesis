"""N-gram Generation Module

Implements exact TWO-PASS 4-gram window algorithm:
- Pass 1: Bigrams (adjacent words) → weight = 3
- Pass 2: 4-gram window scanning
  - Distance 1 (1 word apart) → weight = 2
  - Distance 2 (2 words apart) → weight = 1

CRITICAL: Paragraph breaks (\\n\\n) STOP the algorithm!
"""

from typing import List, Tuple


class NGramGenerator:
    """TWO-PASS n-gram generator following exact InfraNodus specifications."""
    
    def __init__(self, paragraph_delimiter: str = "\n\n"):
        """Initialize n-gram generator.
        
        Args:
            paragraph_delimiter: Delimiter that stops n-gram scanning
        """
        self.paragraph_delimiter = paragraph_delimiter
    
    def generate(self, tokens: List[str]) -> List[Tuple[str, str, int]]:
        """Generate n-grams using TWO-PASS algorithm.
        
        Args:
            tokens: List of lemmatized tokens
        
        Returns:
            List of (source, target, weight) tuples
        """
        ngrams = []
        
        # PASS 1: Bigrams (adjacent words, weight = 3)
        for i in range(len(tokens) - 1):
            ngrams.append((tokens[i], tokens[i+1], 3))
        
        # PASS 2: 4-gram window
        for i in range(len(tokens) - 3):
            window = tokens[i:i+4]
            
            # Distance 1 (1 word apart, weight = 2)
            ngrams.append((window[0], window[2], 2))
            ngrams.append((window[1], window[3], 2))
            
            # Distance 2 (2 words apart, weight = 1)
            ngrams.append((window[0], window[3], 1))
        
        return ngrams
    
    def generate_from_paragraphs(self, text: str, tokens_per_para: List[List[str]]) -> List[Tuple[str, str, int]]:
        """Generate n-grams respecting paragraph boundaries.
        
        Args:
            text: Original text
            tokens_per_para: List of token lists (one per paragraph)
        
        Returns:
            Combined n-grams from all paragraphs
        """
        all_ngrams = []
        
        for para_tokens in tokens_per_para:
            para_ngrams = self.generate(para_tokens)
            all_ngrams.extend(para_ngrams)
        
        return all_ngrams
