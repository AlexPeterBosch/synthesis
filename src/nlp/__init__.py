"""NLP Processing Module

Handles text preprocessing, tokenization, stopword removal,
lemmatization, entity extraction, and n-gram generation.

Exact specifications from research:
- Stopwords applied BEFORE lemmatization
- spaCy en_core_web_sm for English
- Two-pass 4-gram window algorithm (weights: 3/2/1)
- Paragraph breaks (\n\n) stop n-gram scanning
"""

from .text_processor import TextProcessor
from .stopwords import ENGLISH_STOPWORDS
from .ngram_generator import NgramGenerator

__all__ = ['TextProcessor', 'ENGLISH_STOPWORDS', 'NgramGenerator']
