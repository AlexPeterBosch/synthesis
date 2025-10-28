"""ForceAtlas2 Layout Algorithm

Exact specifications from research:
- gravity: 1.0
- scalingRatio: 20.0
- strongGravityMode: True
- linLogMode: False
- edgeWeightInfluence: 1.0
- barnesHutOptimize: True
- barnesHutTheta: 1.2
- jitterTolerance: 1.0
- iterations: 500-2000 (based on graph size)
"""

import networkx as nx
from fa2 import ForceAtlas2
from typing import Dict, Tuple


class ForceAtlas2Layout:
    """ForceAtlas2 layout with exact InfraNodus configuration."""
    
    def __init__(self):
        """Initialize ForceAtlas2 with exact parameters."""
        self.forceatlas2 = ForceAtlas2(
            # Behavior alternatives
            outboundAttractionDistribution=False,
            linLogMode=False,
            adjustSizes=False,
            edgeWeightInfluence=1.0,
            
            # Performance
            jitterTolerance=1.0,
            barnesHutOptimize=True,
            barnesHutTheta=1.2,
            
            # Tuning
            scalingRatio=20.0,
            strongGravityMode=True,
            gravity=1.0
        )
    
    def compute_layout(self, graph: nx.Graph, iterations: int = None) -> Dict[str, Tuple[float, float]]:
        """Compute ForceAtlas2 layout for graph.
        
        Args:
            graph: NetworkX graph with weighted edges
            iterations: Number of iterations (auto-determined if None)
        
        Returns:
            Dictionary mapping node to (x, y) coordinates
        """
        # Auto-determine iterations based on graph size
        if iterations is None:
            num_nodes = graph.number_of_nodes()
            if num_nodes < 500:
                iterations = 1000
            else:
                iterations = 2000
        
        # Compute positions
        positions = self.forceatlas2.forceatlas2_networkx_layout(
            graph,
            pos=None,
            iterations=iterations,
            weight_attr='weight'
        )
        
        return positions
    
    def apply_layout_to_graph(self, graph: nx.Graph, positions: Dict[str, Tuple[float, float]]) -> nx.Graph:
        """Apply computed positions to graph node attributes.
        
        Args:
            graph: NetworkX graph
            positions: Node to (x, y) mapping
        
        Returns:
            Graph with position attributes added
        """
        for node, (x, y) in positions.items():
            graph.nodes[node]['x'] = x
            graph.nodes[node]['y'] = y
        
        return graph
