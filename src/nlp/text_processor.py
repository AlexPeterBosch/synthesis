"""Text processing with exact InfraNodus specifications

Processing order (CRITICAL):
1. Tokenization
2. Special character removal
3. URL removal
4. Standalone number removal
5. **Stopwords removal** <- BEFORE lemmatization!
6. **Lemmatization** <- AFTER stopwords!
7. Entity extraction (if mode != 'lemmas')
"""

import spacy
from typing import List, Dict, Tuple
from .stopwords import ENGLISH_STOPWORDS


class TextProcessor:
    """Process text with exact specifications from research"""
    
    def __init__(self, language: str = "en"):
        """Initialize with spaCy model
        
        Args:
            language: Language code (currently only 'en' supported)
        """
        if language != "en":
            raise ValueError("Only English ('en') is currently supported")
        
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")
        self.stopwords = set(ENGLISH_STOPWORDS)
    
    def process(self, text: str, mode: str = "lemmas") -> Dict:
        """Process text through complete pipeline
        
        Args:
            text: Input text to process
            mode: NER mode - 'lemmas', 'mixed', or 'entities'
        
        Returns:
            Dictionary with tokens, entities, and metadata
        """
        # TODO: Implement complete processing pipeline
        # 1. Split by paragraph breaks
        # 2. Process each paragraph
        # 3. Apply stopwords BEFORE lemmatization
        # 4. Lemmatize
        # 5. Extract entities if needed
        
        raise NotImplementedError("To be implemented in Phase 2")
    
    def _remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stopwords - MUST be before lemmatization"""
        return [token for token in tokens if token.lower() not in self.stopwords]
    
    def _lemmatize(self, tokens: List[str]) -> List[str]:
        """Lemmatize tokens using spaCy"""
        # TODO: Implement lemmatization
        raise NotImplementedError("To be implemented in Phase 2")
