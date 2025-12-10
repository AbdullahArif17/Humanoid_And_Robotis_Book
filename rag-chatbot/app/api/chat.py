from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import os

# Try to use real OpenAI, fall back to mock if not available
try:
    from openai import OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key.strip() == "":
        raise Exception("OPENAI_API_KEY not set")
    client = OpenAI(api_key=openai_api_key)
    OPENAI_AVAILABLE = True
    print("OpenAI client initialized successfully")
except Exception as e:
    print(f"Could not initialize OpenAI: {e}. Using mock responses for local testing.")
    OPENAI_AVAILABLE = False

from dotenv import load_dotenv

from ..db.database import get_db
from ..db.models import ChatSession, ChatMessage
from ..core.rag import rag_engine

load_dotenv()

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str
    context_text: Optional[str] = None  # For context-aware Q&A

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: List[dict] = []

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint that handles user queries and returns AI responses.
    """
    try:
        # Create or get existing session
        session = db.query(ChatSession).filter(ChatSession.session_id == chat_request.session_id).first()
        if not session:
            session = ChatSession(session_id=chat_request.session_id)
            db.add(session)
            db.commit()
            db.refresh(session)

        # Save user message
        user_message = ChatMessage(
            session_id=session.id,
            role="user",
            content=chat_request.message
        )
        db.add(user_message)
        db.commit()

        # Generate context from RAG if no specific context provided
        if not chat_request.context_text:
            try:
                context = rag_engine.generate_context(chat_request.message)
            except Exception as e:
                print(f"Error generating context from RAG: {e}")
                context = ""
        else:
            context = chat_request.context_text

        # Prepare the prompt for the LLM
        if context:
            system_prompt = f"""
            You are an expert assistant for the Humanoid & Robotics Book.
            Use the following context to answer the user's question:

            {context}

            If the context doesn't contain the information needed to answer the question,
            say "I don't have enough information from the book to answer that question.
            Please refer to the relevant sections of the book."

            Provide accurate, helpful, and concise answers based on the book content.
            """
        else:
            system_prompt = """
            You are an expert assistant for the Humanoid & Robotics Book.
            Provide accurate, helpful, and concise answers based on your knowledge of robotics,
            AI, and related topics.
            """

        if OPENAI_AVAILABLE:
            # Call OpenAI API
            try:
                response = client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": chat_request.message}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                ai_response = response.choices[0].message.content
            except Exception as e:
                print(f"Error calling OpenAI API: {e}")
                # Fallback to mock response
                ai_response = f"I'm having trouble connecting to the AI service right now. Based on the context provided, I can tell you that the book covers: {chat_request.message[:100]}... [This is a simulated response for local testing]"
        else:
            # Mock response for local testing
            ai_response = f"This is a simulated response for local testing. Your question was: '{chat_request.message}'. In a production environment with OpenAI access, this would return a detailed answer based on the book content. The context used was: {context[:200] if context else 'No context provided'}..."

        # Save AI response
        ai_message = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=ai_response
        )
        db.add(ai_message)
        db.commit()

        # Get relevant sources if context was used
        sources = []
        if context and "Source:" in context:
            # Extract source information from context
            import re
            source_matches = re.findall(r'Source: (.+?) \((.+?)\)', context)
            for title, source_file in source_matches[:3]:  # Limit to 3 sources
                sources.append({
                    "title": title,
                    "file": source_file
                })

        return ChatResponse(
            response=ai_response,
            session_id=chat_request.session_id,
            sources=sources
        )

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@router.get("/sessions/{session_id}")
async def get_session(session_id: str, db: Session = Depends(get_db)):
    """
    Get chat history for a specific session.
    """
    session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).order_by(ChatMessage.timestamp).all()

    return {
        "session_id": session.session_id,
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    }