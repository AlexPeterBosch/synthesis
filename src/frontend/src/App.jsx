/**
 * Main Application Component
 * 
 * Synthesis - Text-to-Knowledge-Graph System
 */

import React, { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // TODO: Implement API calls
      console.log('Processing text:', text);
    } catch (error) {
      console.error('Error processing text:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Synthesis</h1>
        <p>Text-to-Knowledge-Graph System</p>
      </header>
      
      <main className="container mx-auto p-4">
        <form onSubmit={handleTextSubmit} className="mb-8">
          <textarea
            className="w-full p-4 border rounded"
            rows="10"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter your text here..."
          />
          <button
            type="submit"
            disabled={loading || !text}
            className="mt-4 px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-300"
          >
            {loading ? 'Processing...' : 'Analyze Text'}
          </button>
        </form>
        
        <div id="graph-container" className="w-full h-96 border rounded">
          {/* Graph visualization will be rendered here */}
          <p className="text-center text-gray-500 mt-32">Graph will appear here</p>
        </div>
      </main>
    </div>
  );
}

export default App;
