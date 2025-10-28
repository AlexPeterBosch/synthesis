-- Synthesis Database Schema
-- PostgreSQL 15+
-- Complete schema with exact specifications from research

-- USERS TABLE
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    api_key VARCHAR(500),
    subscription_tier VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- CONTEXTS TABLE (Graph instances)
CREATE TABLE contexts (
    id SERIAL PRIMARY KEY,
    context_name VARCHAR(255) UNIQUE NOT NULL,  -- @private, @public, custom
    user_id INTEGER REFERENCES users(id),
    visibility VARCHAR(50),  -- public, private, shared
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

-- NODES TABLE (All 5 node types)
CREATE TABLE nodes (
    id SERIAL PRIMARY KEY,
    node_id VARCHAR(255) UNIQUE NOT NULL,  -- UUID or custom ID
    label VARCHAR(500),                     -- Node display name (lemma)
    type VARCHAR(50),                       -- concept/statement/context/user/narrative
    properties JSONB,                       -- Flexible attributes
    user_id INTEGER REFERENCES users(id),
    context_id INTEGER REFERENCES contexts(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- EDGES TABLE (All 7 relationship types)
CREATE TABLE edges (
    id SERIAL PRIMARY KEY,
    edge_id VARCHAR(255) UNIQUE NOT NULL,
    source_node_id INTEGER REFERENCES nodes(id) ON DELETE CASCADE,
    target_node_id INTEGER REFERENCES nodes(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50),  -- :TO, :AT, :OF, :IN, :BY, :INTO, :THRU
    weight INTEGER DEFAULT 1,       -- Co-occurrence weight
    properties JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_edge UNIQUE(source_node_id, target_node_id, relationship_type)
);

-- STATEMENTS TABLE (Original text segments)
CREATE TABLE statements (
    id SERIAL PRIMARY KEY,
    statement_id VARCHAR(255) UNIQUE NOT NULL,
    text TEXT NOT NULL,                     -- Original sentence/paragraph
    sentiment VARCHAR(20),                   -- positive, negative, neutral
    topics TEXT[],                          -- Array of topic tags
    context_id INTEGER REFERENCES contexts(id),
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- GRAPH METRICS TABLE
CREATE TABLE graph_metrics (
    id SERIAL PRIMARY KEY,
    context_id INTEGER REFERENCES contexts(id),
    modularity FLOAT,                       -- Newman-Girvan modularity
    influence_entropy FLOAT,                -- Jenks natural breaks entropy
    node_count INTEGER,
    edge_count INTEGER,
    community_count INTEGER,
    avg_betweenness FLOAT,
    cognitive_state VARCHAR(50),            -- biased/focused/diversified/dispersed
    calculated_at TIMESTAMP DEFAULT NOW()
);

-- INDEXES FOR PERFORMANCE
CREATE INDEX idx_nodes_node_id ON nodes(node_id);
CREATE INDEX idx_nodes_type ON nodes(type);
CREATE INDEX idx_nodes_user_id ON nodes(user_id);
CREATE INDEX idx_nodes_context_id ON nodes(context_id);
CREATE INDEX idx_nodes_properties ON nodes USING GIN(properties);  -- JSONB index

CREATE INDEX idx_edges_source ON edges(source_node_id);
CREATE INDEX idx_edges_target ON edges(target_node_id);
CREATE INDEX idx_edges_type ON edges(relationship_type);
CREATE INDEX idx_edges_weight ON edges(weight);
CREATE INDEX idx_edges_composite ON edges(source_node_id, target_node_id);

CREATE INDEX idx_statements_context ON statements(context_id);
CREATE INDEX idx_statements_topics ON statements USING GIN(topics);

CREATE INDEX idx_metrics_context ON graph_metrics(context_id);
CREATE INDEX idx_metrics_calculated ON graph_metrics(calculated_at DESC);

-- COMMENTS
COMMENT ON TABLE nodes IS 'Stores all 5 node types: concept, statement, context, user, narrative';
COMMENT ON TABLE edges IS 'Stores all 7 relationship types: :TO, :AT, :OF, :IN, :BY, :INTO, :THRU';
COMMENT ON COLUMN edges.weight IS 'Co-occurrence weight using ADDITIVE method (NO normalization)';
COMMENT ON COLUMN nodes.properties IS 'JSONB field for flexible node attributes: betweenness, community_id, size, position, etc.';
COMMENT ON COLUMN graph_metrics.modularity IS 'Newman-Girvan weighted modularity: Q > 0.4 = strong structure';
