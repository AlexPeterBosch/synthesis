/**
 * Custom hook for managing graph data
 * 
 * Handles:
 * - Loading graph data from API
 * - Processing updates
 * - Error handling
 */

import { useState, useEffect } from 'react';
import axios from 'axios';

const useGraphData = (contextId) => {
  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchGraphData = async () => {
    if (!contextId) return;

    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(`/api/v1/viz/graph/${contextId}`);
      setGraphData(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGraphData();
  }, [contextId]);

  return { graphData, loading, error, refetch: fetchGraphData };
};

export default useGraphData;
