"""Database seeding script for Synthesis."""

import asyncio
from datetime import datetime
from prisma import Prisma
import uuid


async def seed_database():
    """Seed database with test data."""
    db = Prisma()
    await db.connect()
    
    try:
        # Create test user
        user = await db.user.create(
            data={
                "username": "testuser",
                "email": "test@synthesis.example.com",
                "subscriptionTier": "free"
            }
        )
        print(f"Created user: {user.username}")
        
        # Create test context
        context = await db.context.create(
            data={
                "contextName": "@test_graph",
                "userId": user.id,
                "visibility": "private",
                "metadata": {"description": "Test knowledge graph"}
            }
        )
        print(f"Created context: {context.contextName}")
        
        # Create test nodes
        nodes_data = [
            {"label": "research", "type": "concept"},
            {"label": "innovation", "type": "concept"},
            {"label": "technology", "type": "concept"},
            {"label": "development", "type": "concept"},
            {"label": "analysis", "type": "concept"},
        ]
        
        created_nodes = []
        for node_data in nodes_data:
            node = await db.node.create(
                data={
                    "nodeId": str(uuid.uuid4()),
                    "label": node_data["label"],
                    "type": node_data["type"],
                    "userId": user.id,
                    "contextId": context.id,
                    "properties": {
                        "lemma": node_data["label"],
                        "frequency": 1,
                        "betweenness_centrality": 0.0
                    }
                }
            )
            created_nodes.append(node)
            print(f"Created node: {node.label}")
        
        # Create test edges
        edges = [
            (0, 1, 5),  # research -> innovation
            (1, 2, 4),  # innovation -> technology
            (2, 3, 3),  # technology -> development
            (3, 4, 2),  # development -> analysis
            (0, 4, 2),  # research -> analysis
        ]
        
        for source_idx, target_idx, weight in edges:
            edge = await db.edge.create(
                data={
                    "edgeId": str(uuid.uuid4()),
                    "sourceNodeId": created_nodes[source_idx].id,
                    "targetNodeId": created_nodes[target_idx].id,
                    "relationshipType": ":TO",
                    "weight": weight
                }
            )
            print(f"Created edge: {created_nodes[source_idx].label} -> {created_nodes[target_idx].label} (weight: {weight})")
        
        # Create test statement
        statement = await db.statement.create(
            data={
                "statementId": str(uuid.uuid4()),
                "text": "Research and innovation drive technology development and analysis.",
                "sentiment": "positive",
                "topics": ["research", "innovation", "technology"],
                "contextId": context.id,
                "userId": user.id
            }
        )
        print(f"Created statement: {statement.text[:50]}...")
        
        # Create test metrics
        metric = await db.graphmetric.create(
            data={
                "contextId": context.id,
                "modularity": 0.45,
                "influenceEntropy": 0.6,
                "nodeCount": 5,
                "edgeCount": 5,
                "communityCount": 2,
                "avgBetweenness": 0.1,
                "cognitiveState": "diversified_fractal"
            }
        )
        print(f"Created metrics: modularity={metric.modularity}")
        
        print("\nDatabase seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        raise
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_database())
