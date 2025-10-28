# Database

PostgreSQL database schema and configuration for Synthesis.

## 📋 Schema Overview

The database uses PostgreSQL 15+ with the following tables:

- **users** - User accounts and API keys
- **contexts** - Graph instances (workspaces)
- **nodes** - Concept nodes with JSONB properties
- **edges** - Relationships between nodes with weights
- **statements** - Original text segments
- **graph_metrics** - Calculated metrics per context

## 🚀 Setup

### Create Database

```bash
# Create database
createdb synthesis

# Run schema
psql synthesis < database/schema.sql
```

### Prisma Setup

```bash
# Generate Prisma client
npx prisma generate

# Run migrations
npx prisma migrate dev
```

## 📊 Key Features

### JSONB Properties
Nodes use JSONB for flexible properties:
```json
{
  "lemma": "research",
  "betweenness_centrality": 0.045,
  "degree": 12,
  "community_id": 3,
  "color": "#FF5733",
  "size": 15,
  "position_x": 123.45,
  "position_y": 67.89
}
```

### Critical Indexes
- GIN index on `nodes.properties` for fast JSONB queries
- Composite index on `edges(source_node_id, target_node_id)`
- All foreign keys indexed

### Performance
- Optimized for graphs up to 2000 nodes
- Query response <1 second
- Efficient subgraph extraction

## 📖 Files

- `schema.sql` - Complete SQL schema
- `schema.prisma` - Prisma ORM schema
- `migrations/` - Database migrations
- `seed.py` - Test data generator

## 🔧 Configuration

Set environment variable:
```bash
DATABASE_URL="postgresql://user:password@localhost:5432/synthesis"
```

---

**Status:** Phase 0 - Schema defined, implementation in Phase 1
