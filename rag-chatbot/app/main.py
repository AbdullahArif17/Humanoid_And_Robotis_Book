import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: str
    selected_text: str = None # Optional: for context-aware Q&A

class Settings(BaseSettings):
    """
    Settings for the FastAPI application, loaded from environment variables.
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # FastAPI application settings
    APP_NAME: str = "RAG Chatbot API"
    APP_VERSION: str = "0.0.1"
    DEBUG: bool = False

    # OpenAI API settings
    OPENAI_API_KEY: str
    OPENAI_ORG_ID: str = None
    OPENAI_PROJECT_ID: str = None

    # Qdrant settings
    QDRANT_URL: str
    QDRANT_API_KEY: str

    # Neon Postgres settings
    DATABASE_URL: str


settings = Settings()
from app.core.database import connect_db, disconnect_db, create_chat_history_table

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

@app.on_event("startup")
async def startup_event():
    await connect_db()
    await create_chat_history_table()

@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_db()

# Set up CORS middleware
# This allows the Docusaurus frontend (running on a different port/domain)
# to make requests to this FastAPI backend.
origins = [
    "http://localhost",  # For local development
    "http://localhost:3000", # Default Docusaurus local dev server
    # Add your deployed Docusaurus URL here when known
    # "[GITHUB_PAGES_URL]" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "RAG Chatbot is running!"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "ok", "app_name": settings.APP_NAME, "app_version": settings.APP_VERSION}

from app.core.rag_pipeline import retrieve_context, augment_prompt
from app.core.openai_client import get_chat_completion
from app.core.database import add_chat_entry, get_chat_history

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id
    user_message = request.message
    selected_text = request.selected_text

    # 1. Retrieve context
    context = []
    if selected_text:
        context.append(selected_text) # Prioritize selected text
    
    # Retrieve additional context from Qdrant based on user message
    qdrant_context = await retrieve_context(user_message)
    context.extend(qdrant_context)

    # 2. Augment prompt
    augmented_prompt = augment_prompt(user_message, context)

    # 3. Get chat completion from OpenAI
    # For now, let's just use the augmented_prompt as the user message for the LLM
    # In a more advanced setup, you'd manage conversational history
    
    messages = [{"role": "user", "content": augmented_prompt}]
    ai_response = await get_chat_completion(messages)

    # 4. Store chat interaction
    await add_chat_entry(session_id, user_message, ai_response)

    return {"response": ai_response, "session_id": session_id}