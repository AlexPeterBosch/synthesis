# Phase 2 Validation

## Pre-Completion Checklist

### Preprocessing
- [ ] URLs removed
- [ ] Special characters removed
- [ ] Standalone numbers removed
- [ ] Stopwords removed BEFORE lemmatization
- [ ] Lemmatization working

### N-gram Algorithm
- [ ] PASS 1 creates bigrams with weight=3
- [ ] PASS 2 creates distance-1 pairs with weight=2
- [ ] PASS 2 creates distance-2 pairs with weight=1
- [ ] Paragraph breaks stop scanning
- [ ] Weight accumulation working

### Testing
```python
# Test input
text = "Companies are analyzing customer feedback."

# Expected tokens
["company", "analyze", "customer", "feedback"]

# Expected n-grams
[("company", "analyze", 3),  # bigram
 ("company", "customer", 2),  # distance 1
 ("analyze", "feedback", 3),  # bigram
 ...]
```

## Validation Commands

```bash
# Install dependencies
pip install spacy fastapi uvicorn --break-system-packages
python -m spacy download en_core_web_sm

# Run tests
pytest src/nlp/tests/

# Start service
uvicorn src.nlp.main:app --reload

# Test endpoint
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "AI tools analyze data.", "mode": "lemmas"}'
```

## Success Criteria

All tests pass, service responds, n-gram weights are exact.