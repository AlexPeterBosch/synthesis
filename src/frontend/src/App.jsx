import React from 'react'

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 border-b border-gray-700 p-4">
        <h1 className="text-2xl font-bold">Synthesis</h1>
        <p className="text-gray-400 text-sm">Knowledge Graph Visualization</p>
      </header>
      
      <main className="p-4">
        <div className="max-w-6xl mx-auto">
          <div className="bg-gray-800 rounded-lg p-6 mb-4">
            <h2 className="text-xl font-semibold mb-4">Getting Started</h2>
            <p className="text-gray-300">
              Upload text or enter a URL to generate a knowledge graph.
            </p>
          </div>
          
          <div className="bg-gray-800 rounded-lg p-6" style={{ height: '600px' }}>
            <div className="flex items-center justify-center h-full text-gray-500">
              Graph visualization will appear here
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
