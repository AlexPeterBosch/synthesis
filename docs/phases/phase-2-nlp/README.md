# Phase 2: NLP Processing Pipeline

**Duration:** 2 weeks  
**Complexity:** 6/10  
**English-Only**

## Overview

Build NLP service with exact TWO-PASS n-gram algorithm and spaCy lemmatization.

## Deliverables

- [ ] text_processor.py with TextProcessor class
- [ ] stopwords.py with 180+ word list
- [ ] ngram_generator.py with TWO-PASS algorithm
- [ ] FastAPI service with /process endpoint
- [ ] Unit tests for each function

## Critical Specifications

**Processing Order:**
1. Tokenize
2. Remove URLs, special chars, numbers
3. **Remove stopwords** (BEFORE lemmatization!)
4. **Lemmatize** (AFTER stopwords!)
5. Generate n-grams

**N-gram Algorithm:** TWO-PASS
- PASS 1: Bigrams → weight = 3
- PASS 2: 4-gram window → weights 2, 1
- **Paragraph breaks STOP scanning!**

## Validation

- [ ] Stopwords applied before lemmatization
- [ ] N-gram weights correct (3, 2, 1)
- [ ] Paragraph breaks handled
- [ ] Tests pass

## Reference

- Specifications: `specs/parameters.json` (nlp section)
- Stopwords: `specs/stopwords.json`