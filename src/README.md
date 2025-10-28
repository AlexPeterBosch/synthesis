# Source Code

This directory contains all the implementation code for the Synthesis project.

## 📁 Directory Structure

```
src/
├── nlp/              # NLP processing pipeline
│   ├── text_processor.py
│   ├── stopwords.py
│   ├── ngram_generator.py
│   └── tests/
│
├── graph/            # Graph construction
│   ├── graph_builder.py
│   ├── edge_calculator.py
│   └── tests/
│
├── algorithms/       # Core algorithms
│   ├── louvain.py
│   ├── forceatlas2.py
│   ├── betweenness.py
│   ├── modularity.py
│   └── tests/
│
├── gaps/             # Gap detection
│   ├── gap_detector.py
│   ├── filters.py
│   └── tests/
│
├── graphrag/         # GraphRAG system
│   ├── query_processor.py
│   ├── context_builder.py
│   └── tests/
│
├── api/              # FastAPI backend
│   ├── main.py
│   ├── routes/
│   └── models/
│
└── frontend/         # React frontend
    ├── package.json
    ├── public/
    └── src/
```

## 🚀 Getting Started

### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run FastAPI server
uvicorn src.api.main:app --reload
```

### Frontend Setup

```bash
cd src/frontend
npm install
npm start
```

## 📋 Implementation Order

Follow the development plan phases:

1. **Phase 2:** Implement NLP pipeline
2. **Phase 3:** Build graph construction
3. **Phase 4:** Add core algorithms
4. **Phase 5:** Implement gap detection
5. **Phase 6:** Build GraphRAG system
6. **Phase 7:** Create visualization frontend

## ✅ Testing

Each module includes tests. Run with:

```bash
pytest src/
```

## 📖 Documentation

- See `docs/research/` for specifications
- See `SPECIFICATIONS.md` for technical details
- See `specs/parameters.json` for exact values

---

**Status:** Phase 0 - Structure created, implementation pending
