from openai import OpenAI
from ..main import settings

_openai_client = None

def get_openai_client() -> OpenAI:
    """
    Initializes and returns an OpenAI client.
    """
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            organization=settings.OPENAI_ORG_ID if settings.OPENAI_ORG_ID else None,
            project=settings.OPENAI_PROJECT_ID if settings.OPENAI_PROJECT_ID else None,
        )
    return _openai_client

async def get_chat_completion(
    messages: list, 
    model: str = "gpt-4o", 
    temperature: float = 0.7, 
    max_tokens: int = 500
) -> str:
    """
    Gets a chat completion from the OpenAI model.
    """
    client = get_openai_client()
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting chat completion: {e}")
        return "I apologize, but I encountered an error when trying to generate a response."