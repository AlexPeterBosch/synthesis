"""NLP Processing Module

Components:
- text_processor: Main text processing pipeline
- stopwords: English stopwords management
- ngram_generator: TWO-PASS 4-gram window algorithm

Processing order (CRITICAL):
1. Tokenization
2. Special character removal
3. URL removal
4. Number filtering
5. Stopwords removal (BEFORE lemmatization!)
6. Lemmatization (AFTER stopwords!)
7. Entity extraction (if enabled)
"""

from .text_processor import TextProcessor
from .stopwords import ENGLISH_STOPWORDS
from .ngram_generator import NGramGenerator

__all__ = ["TextProcessor", "ENGLISH_STOPWORDS", "NGramGenerator"]
