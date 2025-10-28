"""N-gram generation with exact two-pass algorithm

Two-pass 4-gram window algorithm:
- Pass 1: Bigrams (adjacent words) -> weight = 3
- Pass 2: 4-gram window:
  - Distance 1 (1 word apart) -> weight = 2
  - Distance 2 (2 words apart) -> weight = 1

CRITICAL: Paragraph breaks (\\n\\n) STOP scanning!
"""

from typing import List, Tuple


class NgramGenerator:
    """Generate n-grams with exact weighted algorithm"""
    
    def generate(self, tokens: List[str]) -> List[Tuple[str, str, int]]:
        """Generate n-grams with two-pass algorithm
        
        Args:
            tokens: List of processed tokens from single paragraph
        
        Returns:
            List of (source, target, weight) tuples
        """
        ngrams = []
        
        # PASS 1: Bigrams (adjacent words, weight=3)
        for i in range(len(tokens) - 1):
            ngrams.append((tokens[i], tokens[i+1], 3))
        
        # PASS 2: 4-gram window
        for i in range(len(tokens) - 3):
            window = tokens[i:i+4]
            
            # Distance 1 (1 word apart) -> weight = 2
            ngrams.append((window[0], window[2], 2))
            ngrams.append((window[1], window[3], 2))
            
            # Distance 2 (2 words apart) -> weight = 1
            ngrams.append((window[0], window[3], 1))
        
        return ngrams
    
    def process_text(self, text: str, tokens_by_paragraph: List[List[str]]) -> List[Tuple[str, str, int]]:
        """Process entire text respecting paragraph boundaries
        
        CRITICAL: Paragraphs separated by \\n\\n do NOT connect
        
        Args:
            text: Original text
            tokens_by_paragraph: List of token lists, one per paragraph
        
        Returns:
            Combined n-grams from all paragraphs
        """
        all_ngrams = []
        
        for paragraph_tokens in tokens_by_paragraph:
            paragraph_ngrams = self.generate(paragraph_tokens)
            all_ngrams.extend(paragraph_ngrams)
        
        return all_ngrams
