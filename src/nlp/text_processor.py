"""Text preprocessing and tokenization."""

import re
from typing import List
import spacy


class TextProcessor:
    """Process text for graph construction following exact specifications."""
    
    def __init__(self, language: str = "en"):
        """Initialize text processor with spaCy model.
        
        Args:
            language: Language code (currently only 'en' supported)
        """
        self.nlp = spacy.load("en_core_web_sm")
        self.language = language
    
    def preprocess(self, text: str) -> str:
        """Preprocess text following exact order from specifications.
        
        Processing order:
        1. Tokenize sentences/paragraphs
        2. Remove special characters
        3. Remove URLs
        4. Remove standalone numbers
        
        Args:
            text: Raw input text
            
        Returns:
            Preprocessed text
        """
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove special characters (keep alphanumeric, spaces, and basic punctuation)
        text = re.sub(r'[^a-zA-Z0-9\s.,!?\n-]', '', text)
        
        # Remove standalone numbers but preserve numbers in words (e.g., COVID-19)
        text = re.sub(r'\b\d+\b', '', text)
        
        return text
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """Tokenize text into sentences.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        doc = self.nlp(text)
        return [sent.text for sent in doc.sents]
