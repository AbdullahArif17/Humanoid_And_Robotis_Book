#!/bin/bash

# Deployment script for Humanoid & Robotics Book
# This script automates the deployment process

set -e  # Exit on any error

echo "🚀 Starting deployment of Humanoid & Robotics Book..."

# Check if we're in the correct directory
if [ ! -f "rag-chatbot/requirements.txt" ] || [ ! -f "book/package.json" ]; then
    echo "❌ Error: Not in the project root directory"
    exit 1
fi

# Check if .env file exists
if [ ! -f "rag-chatbot/.env" ]; then
    echo "❌ Error: rag-chatbot/.env file not found"
    echo "Please create the .env file with required environment variables"
    exit 1
fi

# Load environment variables
source rag-chatbot/.env

echo "✅ Environment variables loaded"

# Build frontend
echo "🏗️  Building frontend..."
cd book
npm install
npm run build
echo "✅ Frontend built successfully"

# Go back to root
cd ..

# Build and start backend services
echo "🏗️  Building backend services..."
docker-compose -f docker-compose.prod.yml build

echo "🚀 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Run database migrations if needed
echo "🔄 Running database setup..."
docker-compose -f docker-compose.prod.yml exec backend python -c "
from app.db.database import engine, Base
from app.db import models
Base.metadata.create_all(bind=engine)
print('Database tables created successfully')
"

# Ingest content into vector database
echo "📚 Ingesting book content into vector database..."
docker-compose -f docker-compose.prod.yml exec backend python scripts/ingest_book_content.py

# Verify deployment
echo "🔍 Verifying deployment..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "⚠️  Health check failed, trying alternative endpoint..."
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend health check passed"
    else
        echo "❌ Both health checks failed"
    fi
fi

# Wait a bit more for everything to be ready
sleep 10

echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Deployment Summary:"
echo "   - Backend API: http://localhost:8000 (proxied through nginx)"
echo "   - Frontend: http://localhost (served by nginx)"
echo "   - Health Check: http://localhost/health"
echo ""
echo "🔧 Next Steps:"
echo "   1. Configure SSL certificates in ./ssl/ directory for HTTPS"
echo "   2. Update nginx.conf with your domain name"
echo "   3. Set up DNS to point to your server"
echo "   4. Monitor application logs: docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "💡 To stop the application: docker-compose -f docker-compose.prod.yml down"
echo "💡 To restart the application: docker-compose -f docker-compose.prod.yml restart"