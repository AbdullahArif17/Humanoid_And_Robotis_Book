# Deployment Guide for Humanoid & Robotics Book

## Overview

This document provides a comprehensive guide for deploying the Humanoid & Robotics Book project to production. The project consists of:
- Frontend: Docusaurus-based documentation site
- Backend: FastAPI-based RAG chatbot API
- Database: PostgreSQL with SQLAlchemy ORM
- Vector Store: Qdrant for document embeddings
- AI Services: OpenAI API for embeddings and chat completions

## Prerequisites

### System Requirements
- Node.js 18+ for frontend
- Python 3.9+ for backend
- PostgreSQL 12+ for database
- Docker and Docker Compose (recommended)
- Git for version control

### Environment Variables
Create a `.env` file in the `rag-chatbot` directory with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Qdrant Configuration
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=humanoid_robotics_book

# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database_name

# CORS Configuration
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

## Deployment Architecture

### Backend (FastAPI)
- Hosted on a cloud platform (AWS, GCP, Azure, or VPS)
- Handles API requests and RAG processing
- Connects to PostgreSQL and Qdrant
- Serves chatbot functionality

### Frontend (Docusaurus)
- Static site hosted on CDN or static hosting (GitHub Pages, Netlify, Vercel)
- Communicates with backend API
- Serves documentation content

### Infrastructure Components
- Load balancer (optional but recommended)
- SSL/TLS termination
- CDN for static assets
- Database with backup and monitoring
- Vector database with monitoring

## Docker Configuration

### Backend Dockerfile
Create `rag-chatbot/Dockerfile`:

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose Configuration
Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./rag-chatbot
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - QDRANT_URL=${QDRANT_URL}
      - QDRANT_API_KEY=${QDRANT_API_KEY}
      - CORS_ORIGINS=${CORS_ORIGINS}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-neondb}
      POSTGRES_USER: ${POSTGRES_USER:-neondb_owner}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

## Frontend Deployment

### Build Configuration
Update `book/docusaurus.config.js` for production:

```js
const config = {
  // ... existing configuration
  url: 'https://yourdomain.com',  // Production URL
  baseUrl: '/',
  trailingSlash: true,

  // Custom fields for production
  customFields: {
    backendUrl: process.env.REACT_APP_BACKEND_URL || 'https://api.yourdomain.com',
  },

  // ... rest of configuration
};
```

### Build Process
```bash
cd book
npm run build
```

This creates a `build/` directory with static files ready for deployment.

## Deployment Steps

### 1. Backend Deployment

#### Option A: Platform as a Service (Recommended)
Deploy to platforms like:
- Render
- Railway
- Heroku
- DigitalOcean App Platform

For Render, create `render.yaml`:

```yaml
services:
  - type: web
    name: rag-chatbot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase: rag-db
      - key: OPENAI_API_KEY
        sync: false
      - key: QDRANT_URL
        sync: false
      - key: QDRANT_API_KEY
        sync: false
databases:
  - name: rag-db
    region: oregon
    plan: free
```

#### Option B: Self-Hosted with Docker
```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Set up environment variables
cp rag-chatbot/.env.example rag-chatbot/.env
# Edit rag-chatbot/.env with your production values

# Deploy with Docker Compose
docker-compose up -d
```

### 2. Frontend Deployment

#### GitHub Pages (Free)
```bash
# Configure for GitHub Pages
cd book
git remote add origin <your-github-repo>
git push origin main

# Set up GitHub Pages in repository settings
# Or use GitHub Actions for automated deployment
```

#### Netlify/Vercel (Recommended)
```bash
# Build the site
cd book
npm run build

# Deploy to Netlify
netlify deploy --prod --dir=build

# Or deploy to Vercel
vercel --prod
```

### 3. Content Ingestion

After deployment, ingest the book content into the vector database:

```bash
# Run the ingestion script
cd rag-chatbot
python scripts/ingest_book_content.py
```

## Security Configuration

### HTTPS Setup
- Configure SSL certificates for both frontend and backend
- Set up automatic certificate renewal
- Redirect HTTP to HTTPS

### API Security
- Implement rate limiting
- Add authentication if needed
- Sanitize all inputs
- Use environment variables for secrets

### Database Security
- Use encrypted connections
- Implement proper access controls
- Regular backups
- Monitor for suspicious activity

## Monitoring and Logging

### Application Monitoring
- Set up health check endpoints
- Implement structured logging
- Monitor API response times
- Track error rates

### Infrastructure Monitoring
- Monitor server resources
- Database performance
- Vector database performance
- Network connectivity

## Scaling Configuration

### Horizontal Scaling
- Use multiple backend instances behind a load balancer
- Implement database connection pooling
- Configure auto-scaling rules

### Performance Optimization
- Enable caching where appropriate
- Optimize database queries
- Use CDN for static assets
- Implement efficient vector search

## Backup and Recovery

### Database Backup
- Regular automated backups
- Point-in-time recovery
- Offsite backup storage
- Test backup restoration procedures

### Content Backup
- Version control for documentation
- Backup vector database
- Archive previous deployments

## Troubleshooting

### Common Issues
- API key configuration
- CORS policy issues
- Database connection problems
- Vector database connectivity

### Debugging
- Check application logs
- Verify environment variables
- Test API endpoints
- Monitor system resources

## Maintenance

### Regular Tasks
- Monitor application health
- Update dependencies
- Review security patches
- Optimize performance

### Updates
- Deploy frontend updates
- Update backend with new features
- Refresh content in vector database
- Maintain documentation

## Environment-Specific Configurations

### Development
- Local PostgreSQL and Qdrant instances
- Mock OpenAI responses for testing
- Debug mode enabled
- Local development server

### Staging
- Separate staging environment
- Staging database and vector store
- Limited access for testing
- Performance testing

### Production
- Production-grade infrastructure
- Optimized for performance and reliability
- Full security measures
- Monitoring and alerting

## Deployment Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] Security measures implemented
- [ ] Backup procedures in place
- [ ] Monitoring configured
- [ ] Load testing completed

### Deployment
- [ ] Deploy backend service
- [ ] Deploy frontend application
- [ ] Run content ingestion
- [ ] Verify API connectivity
- [ ] Test chatbot functionality

### Post-Deployment
- [ ] Monitor application health
- [ ] Verify all features work
- [ ] Set up alerts
- [ ] Document deployment
- [ ] Plan for maintenance
```