#!/bin/bash
# Synthesis Setup Script
# Sets up development environment for Synthesis project

set -e

echo "🚀 Setting up Synthesis development environment..."

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.10+ required. Found: $python_version"
    exit 1
fi
echo "✅ Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "✅ Virtual environment created"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✅ Pip upgraded"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Install spaCy model
echo "Installing spaCy English model..."
python -m spacy download en_core_web_sm
echo "✅ spaCy model installed"

# Setup Prisma
echo "Setting up Prisma..."
prisma generate --schema=database/schema.prisma
echo "✅ Prisma client generated"

# Check PostgreSQL
echo "Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL found"
else
    echo "⚠️  PostgreSQL not found. Please install PostgreSQL 15+"
fi

# Setup frontend
echo "Setting up frontend..."
cd src/frontend
if command -v npm &> /dev/null; then
    npm install
    echo "✅ Frontend dependencies installed"
else
    echo "⚠️  npm not found. Please install Node.js 18+"
fi
cd ../..

# Create .env template
echo "Creating .env template..."
cat > .env.example << 'EOF'
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/synthesis"

# API
API_HOST="localhost"
API_PORT=8000

# Claude API
CLAUDE_API_KEY="your-api-key-here"

# n8n
N8N_HOST="localhost"
N8N_PORT=5678
EOF
echo "✅ .env.example created"

# Check if .env exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Created .env file - please update with your credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your credentials"
echo "2. Create database: createdb synthesis"
echo "3. Run migrations: prisma migrate dev"
echo "4. Seed database: python database/seed.py"
echo "5. Start API: uvicorn src.api.main:app --reload"
echo "6. Start frontend: cd src/frontend && npm run dev"
echo ""
echo "Happy coding! 🎉"
