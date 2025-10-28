# Contributing to Synthesis

Thank you for your interest in contributing to Synthesis! This guide will help you get started.

## 🎯 Project Philosophy

Synthesis is built on **exact specifications** from comprehensive research. All implementations must:

1. Follow specs in `specs/parameters.json` exactly (no approximations)
2. Pass validation rules in `specs/validation-rules.json`
3. Include comprehensive tests
4. Update documentation when complete

## 📋 Development Process

### 1. Choose a Phase

Development follows a strict phase order (see `PROGRESS.md`):

- Phase 1: Database Architecture
- Phase 2: NLP Processing
- Phase 3: Graph Construction
- Phase 4: Core Algorithms
- Phase 5: Gap Detection
- Phase 6: GraphRAG
- Phase 7: Visualization
- Phase 8: Cognitive Analysis
- Phase 9: Integrations

**Do not skip phases.** Each phase builds on the previous.

### 2. Read the Documentation

Before coding:

1. Read the phase documentation in `docs/phases/phase-X/`
2. Review `docs/research/quick-reference.md` for exact parameters
3. Check `SPECIFICATIONS.md` for technical details
4. Understand the deliverables required

### 3. Implement with Exact Specs

**Critical Rules:**

✅ **DO:**
- Use exact values from `specs/parameters.json`
- Remove stopwords BEFORE lemmatization
- Use ADDITIVE edge weights (no normalization)
- Use LINEAR node sizing (not logarithmic)
- Follow the processing order exactly
- Write comprehensive tests

❌ **DON'T:**
- Approximate or round parameters
- Skip validation steps
- Normalize edge weights
- Use logarithmic sizing
- Connect n-grams across paragraphs
- Commit untested code

### 4. Test Everything

```bash
# Run tests
pytest src/

# Run validation
python scripts/validate-phase.py --phase 1

# Check specs compliance
python scripts/check-specs.py
```

### 5. Update Progress

When complete:

1. Check off all deliverables in phase README
2. Update `PROGRESS.md`
3. Commit with descriptive message
4. Create PR if working on fork

## 🧪 Testing Standards

### Unit Tests Required For:

- All NLP processing functions
- N-gram generation
- Edge weight calculation
- All algorithms (Louvain, ForceAtlas2, etc.)
- Gap detection logic
- GraphRAG components

### Test Data

Use fixtures in `tests/fixtures/`:
- Sample texts
- Expected n-grams
- Graph structures
- Community assignments

### Example Test

```python
def test_ngram_weights():
    """Test that weights accumulate correctly"""
    ngrams = [("ai", "tool", 3), ("ai", "tool", 3)]
    graph = build_graph(ngrams)
    
    edge_weight = graph["ai"]["tool"]["weight"]
    assert edge_weight == 6  # 3 + 3, not normalized
```

## 📊 Performance Requirements

All implementations must meet these targets:

- Text processing: <5s (500 words)
- Graph construction: <10s (500 nodes)
- Louvain: <2s (1000 nodes)
- ForceAtlas2: <30s (1000 nodes)
- Betweenness: <5s (500 nodes)
- GraphRAG query: <3s total

## 📝 Commit Message Format

```
type: Brief description

Detailed explanation if needed

- Specific change 1
- Specific change 2

Closes #issue
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

Examples:
- `feat: Implement TWO-PASS n-gram algorithm`
- `fix: Correct edge weight accumulation logic`
- `docs: Add Phase 2 deliverables documentation`
- `test: Add unit tests for gap detection filters`

## 🚫 Code Review Checklist

Before submitting:

- [ ] Follows exact specifications
- [ ] All tests pass
- [ ] Performance targets met
- [ ] Documentation updated
- [ ] No hardcoded values (use config)
- [ ] Error handling included
- [ ] Type hints added (Python)
- [ ] Comments explain "why" not "what"

## 🤝 Getting Help

- Check `docs/research/quick-reference.md` first
- Review the development plan for your phase
- Look at `SPECIFICATIONS.md` for details
- Search existing issues
- Create new issue if stuck

## 🎓 Learning Resources

Understanding the algorithms:

- **Louvain:** Newman-Girvan modularity optimization
- **ForceAtlas2:** Force-directed graph layout
- **Brandes:** Betweenness centrality algorithm
- **spaCy:** NLP pipeline and lemmatization
- **NetworkX:** Graph algorithms in Python

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Every contribution helps make Synthesis better. Whether it's:

- Implementing a phase
- Fixing a bug
- Improving documentation
- Adding tests
- Reporting issues

Your work is appreciated!

---

**Remember:** Exact specifications, comprehensive tests, clear documentation. 🎯
