"""GraphRAG Context Builder

Builds structured context for AI from graph data:
- Top 10 concepts (by betweenness)
- Top 15 relations (by weight)
- Top 5 gaps
- Graph metrics (modularity, entropy, cognitive state)
"""

import networkx as nx
from typing import Dict, List, Any


class ContextBuilder:
    """Build structured context for AI from graph."""
    
    # Context limits from specifications
    TOP_CONCEPTS_COUNT = 10
    TOP_RELATIONS_COUNT = 15
    TOP_GAPS_COUNT = 5
    
    def __init__(self, graph: nx.Graph, 
                 betweenness: Dict[str, float] = None,
                 communities: Dict[str, int] = None):
        """Initialize context builder.
        
        Args:
            graph: NetworkX graph
            betweenness: Optional betweenness centrality values
            communities: Optional community assignments
        """
        self.graph = graph
        self.betweenness = betweenness or {}
        self.communities = communities or {}
    
    def build_context(self, subgraph: nx.Graph = None, 
                     gaps: List[Dict] = None,
                     metrics: Dict[str, float] = None) -> Dict[str, Any]:
        """Build complete context for AI.
        
        Args:
            subgraph: Optional subgraph (uses full graph if None)
            gaps: Optional detected gaps
            metrics: Optional graph metrics
        
        Returns:
            Structured context dictionary
        """
        graph_to_use = subgraph if subgraph else self.graph
        
        # Get top concepts
        top_concepts = self._get_top_concepts(graph_to_use)
        
        # Get top relations
        top_relations = self._get_top_relations(graph_to_use)
        
        # Get main topics (by community)
        main_topics = self._get_main_topics(graph_to_use)
        
        # Build context
        context = {
            "main_topics": main_topics,
            "top_concepts": top_concepts,
            "top_relations": top_relations,
            "top_gaps": gaps[:self.TOP_GAPS_COUNT] if gaps else [],
            "metrics": metrics or {},
            "graph_size": {
                "nodes": graph_to_use.number_of_nodes(),
                "edges": graph_to_use.number_of_edges()
            }
        }
        
        return context
    
    def _get_top_concepts(self, graph: nx.Graph) -> List[Dict[str, Any]]:
        """Get top concepts by betweenness centrality.
        
        Args:
            graph: Graph to analyze
        
        Returns:
            List of top concept dictionaries
        """
        # Get betweenness values for nodes in graph
        concepts = []
        
        for node in graph.nodes():
            bc = self.betweenness.get(node, 0)
            comm = self.communities.get(node, -1)
            
            concepts.append({
                "lemma": str(node),
                "betweenness": bc,
                "community": comm,
                "degree": graph.degree(node)
            })
        
        # Sort by betweenness and take top N
        concepts.sort(key=lambda x: x['betweenness'], reverse=True)
        return concepts[:self.TOP_CONCEPTS_COUNT]
    
    def _get_top_relations(self, graph: nx.Graph) -> List[Dict[str, Any]]:
        """Get top relations by edge weight.
        
        Args:
            graph: Graph to analyze
        
        Returns:
            List of top relation dictionaries
        """
        relations = []
        
        for source, target, data in graph.edges(data=True):
            weight = data.get('weight', 1)
            
            relations.append({
                "source": str(source),
                "target": str(target),
                "weight": weight
            })
        
        # Sort by weight and take top N
        relations.sort(key=lambda x: x['weight'], reverse=True)
        return relations[:self.TOP_RELATIONS_COUNT]
    
    def _get_main_topics(self, graph: nx.Graph) -> List[str]:
        """Get main topics from communities.
        
        Args:
            graph: Graph to analyze
        
        Returns:
            List of main topic labels (one per community)
        """
        if not self.communities:
            return []
        
        # Group nodes by community
        community_nodes = {}
        for node in graph.nodes():
            comm = self.communities.get(node, -1)
            if comm not in community_nodes:
                community_nodes[comm] = []
            community_nodes[comm].append(node)
        
        # Get top node from each community (by betweenness)
        main_topics = []
        for comm, nodes in community_nodes.items():
            if comm == -1:  # Skip uncategorized
                continue
            
            # Find node with highest betweenness in community
            top_node = max(nodes, key=lambda n: self.betweenness.get(n, 0))
            main_topics.append(str(top_node))
        
        return main_topics
    
    def format_context_for_ai(self, context: Dict[str, Any]) -> str:
        """Format context as text for AI input.
        
        Args:
            context: Context dictionary
        
        Returns:
            Formatted text string
        """
        formatted = []
        
        formatted.append("GRAPH CONTEXT:")
        formatted.append(f"\nGraph size: {context['graph_size']['nodes']} nodes, {context['graph_size']['edges']} edges")
        
        if context['main_topics']:
            formatted.append(f"\nMain topics: {', '.join(context['main_topics'])}")
        
        formatted.append(f"\nTop {len(context['top_concepts'])} concepts:")
        for concept in context['top_concepts']:
            formatted.append(f"  - {concept['lemma']} (BC: {concept['betweenness']:.3f}, community: {concept['community']})")
        
        formatted.append(f"\nTop {len(context['top_relations'])} relations:")
        for rel in context['top_relations']:
            formatted.append(f"  - {rel['source']} ↔ {rel['target']} (weight: {rel['weight']})")
        
        if context['top_gaps']:
            formatted.append(f"\nTop {len(context['top_gaps'])} structural gaps:")
            for i, gap in enumerate(context['top_gaps'], 1):
                formatted.append(f"  {i}. Gap between communities {gap.get('community_a_id', '?')} and {gap.get('community_b_id', '?')} (score: {gap.get('gap_score', 0):.2f})")
        
        if context['metrics']:
            formatted.append("\nGraph metrics:")
            for key, value in context['metrics'].items():
                formatted.append(f"  - {key}: {value}")
        
        return "\n".join(formatted)
