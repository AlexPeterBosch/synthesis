"""Structural Gap Detection Module

Detects gaps between communities using five-stage filtering:
1. Size filters (min 3 nodes, max ratio 10:1)
2. Distance filters (2-6 hops)
3. Density filters (<10% connections)
4. Gap score calculation (>0.4 threshold)
5. Semantic validation

Returns maximum 3 gaps.
"""

from .gap_detector import GapDetector
from .filters import GapFilters

__all__ = ["GapDetector", "GapFilters"]
