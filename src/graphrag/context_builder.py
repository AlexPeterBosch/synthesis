"""Build context for AI prompts from graph data."""

import networkx as nx
from typing import Dict, List


class ContextBuilder:
    """Build structured context for GraphRAG prompts."""
    
    def __init__(self):
        """Initialize context builder with exact specifications."""
        self.top_concepts_count = 10   # Exact specification
        self.top_relations_count = 15  # Exact specification
        self.top_gaps_count = 5        # Exact specification
    
    def build_context(self, 
                     subgraph: nx.Graph, 
                     betweenness: Dict[str, float],
                     communities: Dict[str, int],
                     gaps: List[Dict],
                     metrics: Dict) -> Dict:
        """Build complete context for AI prompt.
        
        Context Format:
        - Main topics (by community)
        - Top 10 concepts (by betweenness)
        - Top 15 relations (by weight)
        - Top 5 gaps
        - Graph metrics
        
        Args:
            subgraph: Relevant subgraph
            betweenness: Betweenness centrality values
            communities: Community assignments
            gaps: Detected gaps
            metrics: Graph metrics
            
        Returns:
            Structured context dictionary
        """
        context = {
            "main_topics": self._get_main_topics(subgraph, communities),
            "top_concepts": self._get_top_concepts(subgraph, betweenness),
            "top_relations": self._get_top_relations(subgraph),
            "top_gaps": gaps[:self.top_gaps_count],
            "metrics": metrics
        }
        
        return context
    
    def _get_main_topics(self, subgraph: nx.Graph, communities: Dict[str, int]) -> List[Dict]:
        """Get main topics organized by community.
        
        Args:
            subgraph: Graph
            communities: Community assignments
            
        Returns:
            List of topic dictionaries
        """
        topics = {}
        
        for node in subgraph.nodes():
            if node in communities:
                comm_id = communities[node]
                if comm_id not in topics:
                    topics[comm_id] = []
                topics[comm_id].append(node)
        
        return [
            {"community_id": comm_id, "concepts": concepts}
            for comm_id, concepts in topics.items()
        ]
    
    def _get_top_concepts(self, subgraph: nx.Graph, betweenness: Dict[str, float]) -> List[Dict]:
        """Get top concepts by betweenness centrality.
        
        Specification: Top 10 concepts
        
        Args:
            subgraph: Graph
            betweenness: Betweenness centrality values
            
        Returns:
            List of top concepts with their betweenness values
        """
        # Filter betweenness for nodes in subgraph
        subgraph_bc = {
            node: bc for node, bc in betweenness.items()
            if node in subgraph.nodes()
        }
        
        # Sort by betweenness
        sorted_concepts = sorted(
            subgraph_bc.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {"concept": node, "betweenness": bc}
            for node, bc in sorted_concepts[:self.top_concepts_count]
        ]
    
    def _get_top_relations(self, subgraph: nx.Graph) -> List[Dict]:
        """Get top relations by edge weight.
        
        Specification: Top 15 relations
        
        Args:
            subgraph: Graph with weighted edges
            
        Returns:
            List of top relations with their weights
        """
        # Get all edges with weights
        edges_with_weights = [
            (u, v, data.get('weight', 1))
            for u, v, data in subgraph.edges(data=True)
        ]
        
        # Sort by weight
        sorted_edges = sorted(
            edges_with_weights,
            key=lambda x: x[2],
            reverse=True
        )
        
        return [
            {"source": u, "target": v, "weight": w}
            for u, v, w in sorted_edges[:self.top_relations_count]
        ]
    
    def format_for_llm(self, context: Dict) -> str:
        """Format context as text for LLM prompt.
        
        Args:
            context: Structured context dictionary
            
        Returns:
            Formatted text for prompt injection
        """
        sections = []
        
        # Main topics
        sections.append("Main Topics:")
        for topic in context["main_topics"]:
            concepts = ", ".join(topic["concepts"][:5])  # Top 5 per community
            sections.append(f"- Community {topic['community_id']}: {concepts}")
        
        # Top concepts
        sections.append("\nKey Concepts:")
        for concept in context["top_concepts"]:
            sections.append(f"- {concept['concept']} (importance: {concept['betweenness']:.3f})")
        
        # Top relations
        sections.append("\nKey Relationships:")
        for rel in context["top_relations"]:
            sections.append(f"- {rel['source']} ↔ {rel['target']} (strength: {rel['weight']})")
        
        # Gaps
        if context["top_gaps"]:
            sections.append("\nStructural Gaps:")
            for gap in context["top_gaps"]:
                sections.append(
                    f"- Gap between communities {gap['community_1']} and {gap['community_2']} "
                    f"(score: {gap['gap_score']:.2f})"
                )
        
        return "\n".join(sections)
