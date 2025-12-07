from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.config import settings
from app.db.database import get_db, init_db
from app.db.models import ChatSession, ChatMessage
from app.core.rag import rag_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Humanoid & Robotics Book RAG Chatbot",
    description="RAG-powered chatbot for the Physical AI & Humanoid Robotics book",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")


# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    session_id: str
    selected_text: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    contexts_used: int
    sources: List[str]


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Humanoid & Robotics Book RAG Chatbot API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat endpoint for RAG-powered Q&A.
    
    Args:
        request: Chat request with message, session_id, and optional selected_text
        db: Database session
        
    Returns:
        Chat response with AI-generated answer
    """
    try:
        # Ensure session exists
        session = db.query(ChatSession).filter(
            ChatSession.session_id == request.session_id
        ).first()
        
        if not session:
            session = ChatSession(session_id=request.session_id)
            db.add(session)
            db.commit()
        
        # Get chat history for context
        history_messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == request.session_id
        ).order_by(ChatMessage.timestamp.desc()).limit(6).all()
        
        # Format history for RAG engine
        chat_history = [
            {"role": msg.role, "content": msg.content}
            for msg in reversed(history_messages)
        ]
        
        # Save user message
        user_message = ChatMessage(
            session_id=request.session_id,
            role="user",
            content=request.message,
            selected_text=request.selected_text
        )
        db.add(user_message)
        db.commit()
        
        # Generate response using RAG
        rag_result = rag_engine.chat(
            query=request.message,
            selected_text=request.selected_text,
            chat_history=chat_history
        )
        
        # Save assistant message
        assistant_message = ChatMessage(
            session_id=request.session_id,
            role="assistant",
            content=rag_result['response']
        )
        db.add(assistant_message)
        db.commit()
        
        # Return response
        return ChatResponse(
            response=rag_result['response'],
            session_id=request.session_id,
            contexts_used=rag_result['contexts_used'],
            sources=rag_result['sources']
        )
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


@app.get("/sessions/{session_id}/history")
async def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    """
    Get chat history for a session.
    
    Args:
        session_id: Session identifier
        db: Database session
        
    Returns:
        List of messages in the session
    """
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.timestamp).all()
    
    return {
        "session_id": session_id,
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "selected_text": msg.selected_text
            }
            for msg in messages
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
