from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Import API routes
from .api.chat import router as chat_router

# Import database models to ensure tables are created
# Import database models to ensure tables are created
# We import models so they are registered with Base
from .db import models
from .db.database import engine, Base

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Humanoid & Robotics Book RAG Chatbot API",
    description="API for the RAG-powered chatbot integrated with the Humanoid & Robotics Book",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS middleware - allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-12-09T02:57:00Z"}

@app.get("/")
async def root():
    return {"message": "Humanoid & Robotics Book RAG Chatbot API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))