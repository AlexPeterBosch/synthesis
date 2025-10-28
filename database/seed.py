"""Database Seeding Script

Creates test data for development and testing:
- Test user account
- Sample context
- Sample nodes and edges
- Sample graph metrics
"""

import asyncio
from prisma import Prisma
import json
from datetime import datetime


async def seed_database():
    """Seed database with test data."""
    
    db = Prisma()
    await db.connect()
    
    print("Seeding database...")
    
    try:
        # Create test user
        user = await db.user.create(
            data={
                "username": "testuser",
                "email": "test@synthesis.ai",
                "subscriptionTier": "free"
            }
        )
        print(f"Created user: {user.username}")
        
        # Create test context
        context = await db.context.create(
            data={
                "contextName": "@test_context",
                "userId": user.id,
                "visibility": "private",
                "metadata": json.dumps({"description": "Test context for development"})
            }
        )
        print(f"Created context: {context.contextName}")
        
        # Create sample nodes
        nodes_data = [
            {
                "nodeId": "node_research",
                "label": "research",
                "type": "concept",
                "userId": user.id,
                "contextId": context.id,
                "properties": json.dumps({
                    "lemma": "research",
                    "frequency": 5,
                    "betweenness_centrality": 0.45,
                    "degree": 8,
                    "community_id": 1,
                    "color": "#FF5733",
                    "size": 25
                })
            },
            {
                "nodeId": "node_ai",
                "label": "ai",
                "type": "concept",
                "userId": user.id,
                "contextId": context.id,
                "properties": json.dumps({
                    "lemma": "ai",
                    "frequency": 8,
                    "betweenness_centrality": 0.62,
                    "degree": 12,
                    "community_id": 1,
                    "color": "#FF5733",
                    "size": 30
                })
            },
            {
                "nodeId": "node_tool",
                "label": "tool",
                "type": "concept",
                "userId": user.id,
                "contextId": context.id,
                "properties": json.dumps({
                    "lemma": "tool",
                    "frequency": 4,
                    "betweenness_centrality": 0.38,
                    "degree": 6,
                    "community_id": 2,
                    "color": "#33C3FF",
                    "size": 20
                })
            }
        ]
        
        created_nodes = []
        for node_data in nodes_data:
            node = await db.node.create(data=node_data)
            created_nodes.append(node)
            print(f"Created node: {node.label}")
        
        # Create sample edges
        edges_data = [
            {
                "edgeId": "edge_1",
                "sourceNodeId": created_nodes[0].id,
                "targetNodeId": created_nodes[1].id,
                "relationshipType": ":TO",
                "weight": 15  # ADDITIVE weight
            },
            {
                "edgeId": "edge_2",
                "sourceNodeId": created_nodes[1].id,
                "targetNodeId": created_nodes[2].id,
                "relationshipType": ":TO",
                "weight": 8
            }
        ]
        
        for edge_data in edges_data:
            edge = await db.edge.create(data=edge_data)
            print(f"Created edge: {edge.edgeId} (weight: {edge.weight})")
        
        # Create sample statement
        statement = await db.statement.create(
            data={
                "statementId": "stmt_1",
                "text": "AI research tools are revolutionizing scientific discovery.",
                "sentiment": "positive",
                "topics": ["AI", "research", "tools"],
                "contextId": context.id,
                "userId": user.id
            }
        )
        print(f"Created statement: {statement.statementId}")
        
        # Create sample graph metrics
        metrics = await db.graphmetric.create(
            data={
                "contextId": context.id,
                "modularity": 0.52,
                "influenceEntropy": 0.61,
                "nodeCount": 3,
                "edgeCount": 2,
                "communityCount": 2,
                "avgBetweenness": 0.48,
                "cognitiveState": "diversified_fractal"
            }
        )
        print(f"Created graph metrics (modularity: {metrics.modularity})")
        
        print("\nDatabase seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        raise
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_database())
