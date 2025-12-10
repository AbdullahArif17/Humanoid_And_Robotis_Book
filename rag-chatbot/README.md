# RAG Chatbot Backend

This is the FastAPI backend for the Humanoid & Robotics Book RAG (Retrieval-Augmented Generation) chatbot.

## Overview

The backend provides:
- API endpoints for chat interactions
- Integration with Qdrant vector database for content retrieval
- OpenAI integration for response generation
- Chat history management with Neon Postgres

## Tech Stack

- **Framework**: FastAPI
- **Vector Database**: Qdrant Cloud
- **LLM**: OpenAI GPT models
- **Database**: Neon Serverless Postgres
- **Language**: Python 3.11

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

3. Set up Qdrant collection:
   ```bash
   python scripts/setup_qdrant.py
   ```

4. Ingest book content:
   ```bash
   python scripts/ingest_book_content.py
   ```

5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `GET /health` - Health check
- `POST /api/v1/chat` - Chat endpoint
- `GET /api/v1/sessions/{session_id}` - Get chat history

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key
- `QDRANT_URL` - Your Qdrant cluster URL
- `QDRANT_API_KEY` - Your Qdrant API key
- `DATABASE_URL` - Neon Postgres connection string
- `CORS_ORIGINS` - Comma-separated list of allowed origins