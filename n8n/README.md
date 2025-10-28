# n8n Workflows for Synthesis

This directory contains n8n workflow templates for Synthesis automation and AI integration.

## Workflows

### 1. graphrag-query.json
GraphRAG query processing workflow with Claude AI integration.
- Receives query via webhook
- Processes query through Synthesis API
- Sends context to Claude for response generation
- Returns AI-generated answer

### 2. gap-bridging.json
Structural gap detection and bridging idea generation.
- Receives graph context via webhook
- Detects structural gaps
- Generates bridging ideas using Claude AI
- Returns suggestions

### 3. csv-import.json
Batch text processing from CSV files.
- Receives CSV file via webhook
- Parses CSV data
- Processes text through Synthesis
- Returns processed graph data

## Setup

1. Import workflows into n8n
2. Configure Claude API credentials
3. Set Synthesis API endpoint
4. Activate workflows

## Configuration

- Synthesis API: `http://localhost:8000`
- Claude API: `https://api.anthropic.com/v1/messages`
- Model: `claude-sonnet-4-20250514`

## Usage

See individual workflow files for webhook URLs and request formats.
