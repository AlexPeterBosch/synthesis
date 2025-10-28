"""Text Processing Pipeline

Implements exact InfraNodus NLP specifications:
- spaCy-based lemmatization
- Custom stopwords (applied BEFORE lemmatization)
- Three-mode entity extraction
- Preprocessing: URLs, special chars, numbers
"""

import spacy
from typing import List, Dict, Any, Tuple
import re


class TextProcessor:
    """Main text processing class following exact InfraNodus pipeline."""
    
    def __init__(self, model: str = "en_core_web_sm", stopwords: List[str] = None):
        """Initialize text processor.
        
        Args:
            model: spaCy model name (default: en_core_web_sm)
            stopwords: Custom stopwords list (default: load from config)
        """
        self.nlp = spacy.load(model)
        self.stopwords = set(stopwords) if stopwords else set()
    
    def process(self, text: str, mode: str = "lemmas") -> Dict[str, Any]:
        """Process text through complete pipeline.
        
        Args:
            text: Input text to process
            mode: Entity extraction mode ("lemmas", "mixed", "entities")
        
        Returns:
            Dictionary with tokens, entities, and processed text
        """
        # TODO: Implement processing pipeline
        # 1. Tokenization
        # 2. Special character removal
        # 3. URL removal
        # 4. Number filtering
        # 5. Stopwords removal (BEFORE lemmatization)
        # 6. Lemmatization (AFTER stopwords)
        # 7. Entity extraction
        
        return {
            "tokens": [],
            "entities": [],
            "mode": mode
        }
