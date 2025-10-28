# Deployment Architecture

## Components

### Backend Services
- **NLP Service** (FastAPI, port 8000)
- **Graph API** (FastAPI, port 8001)
- **PostgreSQL** (port 5432)
- **n8n** (Docker, port 5678)

### Frontend
- **React App** (port 3000)
- Sigma.js visualization

## Deployment Options

### Local Development
```bash
# Database
createdb synthesis
psql synthesis < database/schema.sql

# Backend
pip install -r requirements.txt
uvicorn src.api.main:app --reload

# Frontend
cd src/frontend
npm install
npm start

# n8n
docker run -p 5678:5678 n8nio/n8n
```

### Production
- Docker containers
- Load balancer
- Managed PostgreSQL
- CDN for frontend

## Environment Variables

```bash
DATABASE_URL=postgresql://...
CLAUDE_API_KEY=sk-...
N8N_WEBHOOK_URL=https://...
```

## Reference

- Setup script: `scripts/setup.sh`