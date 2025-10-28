# Synthesis Scripts

Utility scripts for development, testing, and validation.

## Scripts

### setup.sh
**Purpose:** Set up development environment

**Usage:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**What it does:**
- Checks Python version (3.10+ required)
- Installs Python dependencies
- Downloads spaCy English model
- Sets up Prisma
- Creates .env file template
- Installs frontend dependencies

### validate-phase.py
**Purpose:** Validate that a development phase is complete

**Usage:**
```bash
python scripts/validate-phase.py --phase 1
```

**What it checks:**
- Required files exist
- Specification tests pass
- Deliverables are complete

**Example output:**
```
Validating Phase 2: NLP Processing
==================================================

Checking required files...
  ✅ src/nlp/text_processor.py
  ✅ src/nlp/stopwords.py
  ✅ src/nlp/ngram_generator.py

Checking specification tests...
  ✅ tests/specifications/test_ngram_weights.py exists
    ✅ Tests pass

==================================================
✅ Phase 2 validation PASSED
Estimated duration: 2 weeks
```

### check-specs.py
**Purpose:** Validate implementations against specifications

**Usage:**
```bash
python scripts/check-specs.py
```

**What it checks:**
- specs/parameters.json values
- specs/stopwords.json count (180+ words)
- Critical constants in source code
- No approximations or deviations

**Example output:**
```
Checking parameters.json...
  ✅ Pass 1 bigram weight must be 3
  ✅ Pass 2 distance-1 weight must be 2
  ✅ Edge weights must NOT be normalized
  ✅ Min node size must be 5 pixels
  ✅ Max node size must be 40 pixels

Checking stopwords.json...
  ✅ Stopwords count: 182 (>= 180 required)

✅ All specification checks passed!
```

## Development Workflow

1. **Setup environment:**
   ```bash
   ./scripts/setup.sh
   ```

2. **Work on phase:**
   - Implement features according to specifications
   - Write tests
   - Run tests: `pytest`

3. **Validate phase:**
   ```bash
   python scripts/validate-phase.py --phase N
   ```

4. **Check specifications:**
   ```bash
   python scripts/check-specs.py
   ```

5. **Mark phase complete when:**
   - Phase validation passes
   - Specification checks pass
   - All tests pass
   - Code reviewed

## Continuous Integration

These scripts should be integrated into CI/CD pipeline:

```yaml
# .github/workflows/test.yml
steps:
  - name: Setup
    run: ./scripts/setup.sh
  
  - name: Run tests
    run: pytest
  
  - name: Check specifications
    run: python scripts/check-specs.py
```
