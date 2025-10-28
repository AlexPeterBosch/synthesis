"""Stopwords management and filtering."""

import json
from pathlib import Path
from typing import List, Set


class StopwordsFilter:
    """Filter stopwords from text following exact specifications."""
    
    def __init__(self, language: str = "en"):
        """Initialize stopwords filter.
        
        Args:
            language: Language code
        """
        self.language = language
        self.stopwords = self._load_stopwords()
    
    def _load_stopwords(self) -> Set[str]:
        """Load stopwords from specs/stopwords.json.
        
        Returns:
            Set of stopwords
        """
        stopwords_file = Path("specs/stopwords.json")
        if stopwords_file.exists():
            with open(stopwords_file, 'r') as f:
                data = json.load(f)
                return set(data.get('stopwords', []))
        return set()
    
    def filter(self, words: List[str]) -> List[str]:
        """Remove stopwords from word list.
        
        CRITICAL: Must be applied BEFORE lemmatization.
        
        Args:
            words: List of words
            
        Returns:
            Filtered word list
        """
        return [word for word in words if word.lower() not in self.stopwords]
