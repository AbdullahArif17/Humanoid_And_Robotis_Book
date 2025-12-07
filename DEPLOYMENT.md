# Humanoid & Robotics Book - Production Deployment Guide

This guide walks you through deploying the complete Humanoid & Robotics Book project with the RAG chatbot to production.

## Overview

The project consists of two main components:
1. **Frontend**: Docusaurus book deployed to GitHub Pages
2. **Backend**: FastAPI RAG chatbot deployed to a cloud platform

## Prerequisites

Before deploying, ensure you have:

- ✅ GitHub account with repository access
- ✅ OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ✅ Qdrant Cloud account ([Sign up for free](https://cloud.qdrant.io/))
- ✅ Neon Serverless Postgres account ([Sign up for free](https://neon.tech/))
- ✅ Cloud platform account for backend (Render, Railway, etc.)

## Part 1: Cloud Services Setup

### 1.1 Qdrant Cloud Setup

1. Go to [Qdrant Cloud](https://cloud.qdrant.io/)
2. Create a new cluster (free tier available)
3. Note your **Cluster URL** (e.g., `https://xyz.qdrant.io`)
4. Create an **API Key** from the dashboard
5. Save these credentials for later

### 1.2 Neon Postgres Setup

1. Go to [Neon](https://neon.tech/)
2. Create a new project
3. Copy the **Connection String** (it should look like: `postgresql://user:password@host/database?sslmode=require`)
4. Save this for later

### 1.3 OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Save it securely (you won't be able to see it again)

## Part 2: Backend Deployment

### Option A: Deploy to Render (Recommended)

1. **Create Render Account**
   - Go to [Render](https://render.com/) and sign up

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `rag-chatbot` directory as the root

3. **Configure Service**
   - **Name**: `humanoid-robotics-chatbot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   
   Go to "Environment" tab and add:
   
   ```
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_COLLECTION_NAME=humanoid_robotics_book
   DATABASE_URL=postgresql://user:password@host/database?sslmode=require
   CORS_ORIGINS=http://localhost:3000,https://abdullaharif17.github.io
   API_HOST=0.0.0.0
   API_PORT=8000
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note your backend URL (e.g., `https://humanoid-robotics-chatbot.onrender.com`)

### Option B: Deploy to Railway

1. Go to [Railway](https://railway.app/)
2. Create new project from GitHub repo
3. Select `rag-chatbot` directory
4. Add environment variables (same as Render)
5. Deploy

### Option C: Deploy with Docker

If using a platform that supports Docker:

```bash
cd rag-chatbot
docker build -t rag-chatbot .
docker push your-registry/rag-chatbot
```

Then deploy the image to your platform.

## Part 3: Data Ingestion

After backend is deployed, you need to populate the vector database:

### 3.1 Setup Qdrant Collection

On your local machine:

```bash
cd rag-chatbot
cp .env.example .env
# Edit .env with your production credentials
python scripts/setup_qdrant.py
```

### 3.2 Ingest Book Content

```bash
python scripts/ingest_book_content.py
```

This will:
- Read all markdown files from `book/docs/`
- Chunk the content
- Generate embeddings
- Upload to Qdrant

**Note**: This may take 5-10 minutes depending on content size.

## Part 4: Frontend Deployment

### 4.1 Update GitHub Actions Workflow

Edit `.github/workflows/deploy.yml` and add the backend URL as an environment variable:

```yaml
- name: Build Docusaurus website
  run: npm run build
  working-directory: ./book
  env:
    # ... existing env vars ...
    REACT_APP_BACKEND_URL: https://your-backend-url.onrender.com
```

### 4.2 Enable GitHub Pages

1. Go to your repository on GitHub
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: `gh-pages` / `root`
5. Save

### 4.3 Deploy

Push to the `main` branch:

```bash
git add .
git commit -m "Configure production deployment"
git push origin main
```

GitHub Actions will automatically:
1. Build the Docusaurus site
2. Deploy to GitHub Pages

## Part 5: Verification

### 5.1 Test Backend

```bash
curl https://your-backend-url.onrender.com/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "..."}
```

### 5.2 Test Chat Endpoint

```bash
curl -X POST https://your-backend-url.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is ROS 2?",
    "session_id": "test_session"
  }'
```

### 5.3 Test Frontend

1. Visit `https://abdullaharif17.github.io/Humanoid_And_Robotis_Book/`
2. Navigate to the Chatbot page
3. Ask a question about the book
4. Verify you get a relevant response

## Troubleshooting

### Backend Issues

**Problem**: "Collection not found" error

**Solution**: Run `python scripts/setup_qdrant.py` to create the collection

---

**Problem**: CORS errors in browser console

**Solution**: Ensure `CORS_ORIGINS` includes `https://abdullaharif17.github.io`

---

**Problem**: Database connection errors

**Solution**: Verify `DATABASE_URL` is correct and includes `?sslmode=require`

### Frontend Issues

**Problem**: 404 errors on GitHub Pages

**Solution**: Ensure `baseUrl` in `docusaurus.config.ts` matches your repository name

---

**Problem**: Chatbot not connecting to backend

**Solution**: 
1. Check browser console for errors
2. Verify `REACT_APP_BACKEND_URL` is set correctly
3. Test backend health endpoint directly

### Ingestion Issues

**Problem**: "No markdown files found"

**Solution**: Ensure you're running the script from the `rag-chatbot` directory

---

**Problem**: OpenAI rate limit errors

**Solution**: The script has retry logic, but you may need to wait and re-run

## Monitoring

### Backend Monitoring

- **Render**: Check logs in the Render dashboard
- **Railway**: Check logs in the Railway dashboard

### Frontend Monitoring

- **GitHub Actions**: Check workflow runs in the Actions tab
- **GitHub Pages**: Check deployment status in Settings → Pages

## Updating Content

When you update book content:

1. Push changes to GitHub (frontend will auto-deploy)
2. Re-run ingestion script to update vector database:
   ```bash
   python scripts/ingest_book_content.py
   ```

## Cost Estimates

With free tiers:

- **Qdrant Cloud**: Free tier (1GB storage)
- **Neon Postgres**: Free tier (0.5GB storage)
- **OpenAI API**: Pay-per-use (~$0.10-0.50 per 1000 questions)
- **Render/Railway**: Free tier available (may sleep after inactivity)
- **GitHub Pages**: Free for public repositories

**Estimated monthly cost**: $0-5 for light usage

## Security Best Practices

1. ✅ Never commit `.env` files
2. ✅ Use environment variables for all secrets
3. ✅ Rotate API keys periodically
4. ✅ Monitor API usage for anomalies
5. ✅ Keep dependencies updated

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review backend logs
3. Check GitHub Actions logs
4. Verify all environment variables are set correctly

## Next Steps

After successful deployment:

1. ✅ Test all chatbot features
2. ✅ Monitor API usage and costs
3. ✅ Set up monitoring/alerting
4. ✅ Consider adding analytics
5. ✅ Gather user feedback

---

**Congratulations!** Your Humanoid & Robotics Book with RAG chatbot is now live! 🎉
