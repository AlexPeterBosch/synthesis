/**
 * Graph Visualization Component using Sigma.js
 * 
 * Exact specifications:
 * - Node sizing: LINEAR (5-40 pixels)
 * - Node labels: Show only for size > 20 pixels (top ~30%)
 * - Edge thickness: log(weight + 1)
 * - Community colors: HSL color space
 */

import React, { useEffect, useRef } from 'react';
import Graph from 'graphology';
import Sigma from 'sigma';

const GraphVisualization = ({ graphData }) => {
  const containerRef = useRef(null);
  const sigmaRef = useRef(null);

  useEffect(() => {
    if (!graphData || !containerRef.current) return;

    // Create graph
    const graph = new Graph();

    // Add nodes with EXACT sizing formula
    graphData.nodes.forEach((node) => {
      const bc = node.properties.betweenness_centrality;
      const minBc = Math.min(...graphData.nodes.map((n) => n.properties.betweenness_centrality));
      const maxBc = Math.max(...graphData.nodes.map((n) => n.properties.betweenness_centrality));

      // LINEAR SCALING: 5-40 pixels
      const bcNormalized = (bc - minBc) / (maxBc - minBc);
      const size = 5 + bcNormalized * 35;

      graph.addNode(node.node_id, {
        label: node.properties.lemma,
        size: size,
        color: node.properties.color || '#666',
        x: node.properties.position_x || Math.random() * 100,
        y: node.properties.position_y || Math.random() * 100,
      });
    });

    // Add edges with weight-based thickness
    graphData.edges.forEach((edge) => {
      const thickness = Math.log(edge.weight + 1);
      graph.addEdge(edge.source_node_id, edge.target_node_id, {
        weight: edge.weight,
        size: thickness,
      });
    });

    // Sigma.js configuration
    const sigma = new Sigma(graph, containerRef.current, {
      renderEdgeLabels: false,
      defaultNodeColor: '#666',
      defaultEdgeColor: '#ccc',
      labelSize: 12,
      nodeReducer: (node, data) => ({
        ...data,
        // Show labels only for top 30% nodes (size > 20 pixels)
        label: data.size > 20 ? data.label : '',
      }),
    });

    sigmaRef.current = sigma;

    return () => {
      if (sigmaRef.current) {
        sigmaRef.current.kill();
      }
    };
  }, [graphData]);

  return <div ref={containerRef} style={{ width: '100%', height: '600px' }} />;
};

export default GraphVisualization;
