# Phase 2 Deliverables

## Required Files

### 1. text_processor.py
**Location:** `src/nlp/text_processor.py`  
**Contains:** TextProcessor class with preprocessing pipeline

### 2. stopwords.py
**Location:** `src/nlp/stopwords.py`  
**Contains:** ENGLISH_STOPWORDS list (180+ words)

### 3. ngram_generator.py
**Location:** `src/nlp/ngram_generator.py`  
**Contains:** TWO-PASS n-gram algorithm

### 4. main.py
**Location:** `src/nlp/main.py`  
**Contains:** FastAPI service with /process endpoint

### 5. Unit Tests
**Location:** `src/nlp/tests/`  
**Contains:**
- test_text_processor.py
- test_ngrams.py
- test_stopwords.py

## Completion Criteria

- ✅ All preprocessing steps work
- ✅ TWO-PASS algorithm implemented
- ✅ Weights are 3, 2, 1
- ✅ Paragraph breaks stop scanning
- ✅ FastAPI service responds
- ✅ All tests pass