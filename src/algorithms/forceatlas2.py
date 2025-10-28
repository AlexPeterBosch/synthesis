"""ForceAtlas2 layout algorithm."""

import networkx as nx
from fa2 import ForceAtlas2
from typing import Dict, Tuple


class ForceAtlas2Layout:
    """ForceAtlas2 force-directed layout with exact specifications."""
    
    def __init__(self):
        """Initialize ForceAtlas2 with exact parameters from specifications."""
        self.forceatlas2 = ForceAtlas2(
            # Behavior alternatives
            outboundAttractionDistribution=False,  # Per specs
            linLogMode=False,                      # Per specs
            adjustSizes=False,                     # Per specs
            edgeWeightInfluence=1.0,              # Per specs
            
            # Performance
            jitterTolerance=1.0,                   # Per specs
            barnesHutOptimize=True,                # Per specs
            barnesHutTheta=1.2,                    # Per specs
            
            # Tuning
            scalingRatio=20.0,                     # Per specs
            strongGravityMode=True,                # Per specs
            gravity=1.0,                           # Per specs
            
            # Log
            verbose=False
        )
    
    def calculate_layout(self, graph: nx.Graph, iterations: int = None) -> Dict[str, Tuple[float, float]]:
        """Calculate node positions using ForceAtlas2.
        
        Specifications:
        - Iterations: 1000 for small graphs (<1000 nodes), 2000 for larger
        - All other parameters as defined in __init__
        
        Args:
            graph: NetworkX graph
            iterations: Number of iterations (auto-determined if None)
            
        Returns:
            Dictionary mapping node names to (x, y) positions
        """
        # Determine iterations based on graph size
        if iterations is None:
            node_count = graph.number_of_nodes()
            iterations = 1000 if node_count < 1000 else 2000
        
        # Calculate positions
        positions = self.forceatlas2.forceatlas2_networkx_layout(
            graph,
            pos=None,
            iterations=iterations,
            weight_attr='weight'
        )
        
        return positions
