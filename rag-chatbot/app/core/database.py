import asyncpg
from ..main import settings

_pool = None

async def connect_db():
    """
    Establishes a connection pool to the PostgreSQL database.
    """
    global _pool
    if not _pool:
        _pool = await asyncpg.create_pool(settings.DATABASE_URL)
        print("Database connection pool created.")

async def disconnect_db():
    """
    Closes the PostgreSQL database connection pool.
    """
    global _pool
    if _pool:
        await _pool.close()
        print("Database connection pool closed.")

async def create_chat_history_table():
    """
    Creates the chat_history table if it doesn't exist.
    """
    async with _pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                session_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Chat history table ensured.")

async def add_chat_entry(session_id: str, user_message: str, ai_response: str):
    """
    Adds a new chat entry to the chat_history table.
    """
    async with _pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO chat_history (session_id, user_message, ai_response)
            VALUES ($1, $2, $3);
            """,
            session_id, user_message, ai_response
        )

async def get_chat_history(session_id: str):
    """
    Retrieves chat history for a given session ID.
    """
    async with _pool.acquire() as conn:
        records = await conn.fetch(
            """
            SELECT session_id, user_message, ai_response, timestamp
            FROM chat_history
            WHERE session_id = $1
            ORDER BY timestamp ASC;
            """,
            session_id
        )
        return [dict(r) for r in records]

