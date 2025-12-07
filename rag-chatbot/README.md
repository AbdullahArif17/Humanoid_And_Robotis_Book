# RAG Chatbot Backend

FastAPI backend for the Humanoid & Robotics Book RAG-powered chatbot.

## Features

- 🤖 **RAG-Powered Q&A**: Retrieval-Augmented Generation using OpenAI and Qdrant
- 💬 **Chat History**: Persistent conversation storage with Neon Postgres
- 🎯 **Context-Aware**: Support for user-selected text context
- 🔍 **Vector Search**: Semantic search across book content
- 🚀 **Production Ready**: Docker support, health checks, CORS configured

## Prerequisites

- Python 3.11+
- OpenAI API key
- Qdrant Cloud account (free tier)
- Neon Serverless Postgres account (free tier)

## Quick Start

### 1. Install Dependencies

```bash
cd rag-chatbot
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual API keys and connection strings.

### 3. Setup Qdrant Collection

```bash
python scripts/setup_qdrant.py
```

### 4. Ingest Book Content

```bash
python scripts/ingest_book_content.py
```

This will:
- Scan all markdown files in `../book/docs/`
- Chunk the content intelligently
- Generate embeddings using OpenAI
- Upload to Qdrant vector database

### 5. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /health
```

### Chat
```
POST /chat
Content-Type: application/json

{
  "message": "What is ROS 2?",
  "session_id": "user_session_123",
  "selected_text": "optional context text"
}
```

### Get Chat History
```
GET /sessions/{session_id}/history
```

## Docker Deployment

### Build and Run with Docker Compose

```bash
docker-compose up --build
```

### Build Docker Image

```bash
docker build -t rag-chatbot .
```

### Run Docker Container

```bash
docker run -p 8000:8000 --env-file .env rag-chatbot
```

## Project Structure

```
rag-chatbot/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── core/
│   │   ├── rag.py          # RAG engine
│   │   ├── embeddings.py   # Embedding generation
│   │   └── chunking.py     # Markdown chunking
│   └── db/
│       ├── database.py     # Database connection
│       ├── models.py       # SQLAlchemy models
│       └── schema.sql      # SQL schema
├── scripts/
│   ├── setup_qdrant.py     # Qdrant setup
│   └── ingest_book_content.py  # Content ingestion
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | GPT model to use | `gpt-4o-mini` |
| `OPENAI_EMBEDDING_MODEL` | Embedding model | `text-embedding-3-small` |
| `QDRANT_URL` | Qdrant cluster URL | Required |
| `QDRANT_API_KEY` | Qdrant API key | Optional |
| `DATABASE_URL` | Postgres connection string | Required |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `MAX_CONTEXT_CHUNKS` | Max chunks for RAG | `5` |

## Development

### Run Tests

```bash
pytest tests/ -v
```

### Code Formatting

```bash
black app/
isort app/
```

### Type Checking

```bash
mypy app/
```

## Deployment

### Recommended Platforms

- **Render**: Easy deployment, free tier available
- **Railway**: Good for FastAPI + Postgres
- **Google Cloud Run**: Serverless, pay-as-you-go
- **Vercel**: With serverless adapter

### Environment Setup on Cloud Platform

1. Set all environment variables from `.env.example`
2. Ensure `CORS_ORIGINS` includes your production domain
3. Run ingestion script after deployment

## Troubleshooting

### "Collection not found" error
Run `python scripts/setup_qdrant.py` to create the collection.

### "No chunks to upload" error
Ensure the book content is in `../book/docs/` directory.

### CORS errors
Add your frontend domain to `CORS_ORIGINS` in `.env`.

### Database connection errors
Verify your `DATABASE_URL` is correct and includes `?sslmode=require` for Neon.

## License

Part of the Humanoid & Robotics Book project.
