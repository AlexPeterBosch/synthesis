"""Sample graph data for testing"""

import networkx as nx


def create_sample_graph():
    """Create a simple test graph."""
    G = nx.Graph()
    
    # Add nodes
    G.add_node("research", betweenness_centrality=0.45, community=1)
    G.add_node("ai", betweenness_centrality=0.62, community=1)
    G.add_node("tool", betweenness_centrality=0.38, community=2)
    G.add_node("customer", betweenness_centrality=0.51, community=2)
    G.add_node("feedback", betweenness_centrality=0.33, community=2)
    
    # Add weighted edges (ADDITIVE weights)
    G.add_edge("research", "ai", weight=15)  # High co-occurrence
    G.add_edge("ai", "tool", weight=8)
    G.add_edge("tool", "customer", weight=5)
    G.add_edge("customer", "feedback", weight=12)
    G.add_edge("research", "customer", weight=3)  # Gap bridge
    
    return G


def create_disconnected_graph():
    """Create graph with clear gaps for testing gap detection."""
    G = nx.Graph()
    
    # Community 1 (AI/Research)
    G.add_node("ai", betweenness_centrality=0.5, community=1)
    G.add_node("research", betweenness_centrality=0.4, community=1)
    G.add_node("algorithm", betweenness_centrality=0.3, community=1)
    G.add_edge("ai", "research", weight=10)
    G.add_edge("research", "algorithm", weight=8)
    
    # Community 2 (Business/Customer) - disconnected
    G.add_node("business", betweenness_centrality=0.45, community=2)
    G.add_node("customer", betweenness_centrality=0.5, community=2)
    G.add_node("marketing", betweenness_centrality=0.35, community=2)
    G.add_edge("business", "customer", weight=12)
    G.add_edge("customer", "marketing", weight=9)
    
    # Weak bridge (creates a gap)
    G.add_edge("ai", "business", weight=1)
    
    return G
