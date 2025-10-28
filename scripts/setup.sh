#!/bin/bash
# Synthesis Setup Script
# Sets up development environment

set -e

echo "=== Synthesis Setup ==="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 10) else 1)'; then
    echo "Error: Python 3.10+ required"
    exit 1
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt --break-system-packages

# Download spaCy model
echo ""
echo "Downloading spaCy English model..."
python3 -m spacy download en_core_web_sm

# Setup Prisma
echo ""
echo "Setting up Prisma..."
if [ -f "database/schema.prisma" ]; then
    cd database
    echo "Generating Prisma client..."
    prisma generate
    cd ..
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file..."
    cat > .env << EOF
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/synthesis"

# API
API_PORT=8000
API_HOST=0.0.0.0

# Claude API
CLAUDE_API_KEY=your_api_key_here

# Environment
ENVIRONMENT=development
EOF
    echo ".env file created - please update with your credentials"
fi

# Frontend setup
if [ -d "src/frontend" ]; then
    echo ""
    echo "Setting up frontend..."
    cd src/frontend
    if command -v npm &> /dev/null; then
        npm install
        echo "Frontend dependencies installed"
    else
        echo "Warning: npm not found, skipping frontend setup"
    fi
    cd ../..
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Update .env file with your database credentials"
echo "2. Create PostgreSQL database: createdb synthesis"
echo "3. Run database migrations: cd database && prisma migrate dev"
echo "4. Seed database: python database/seed.py"
echo "5. Start API server: uvicorn src.api.main:app --reload"
echo "6. Start frontend: cd src/frontend && npm start"
echo ""
