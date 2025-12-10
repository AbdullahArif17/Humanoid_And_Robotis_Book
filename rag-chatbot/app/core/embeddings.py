import os
from typing import List
import openai
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client only if API key is provided
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key or openai_api_key.strip() == "":
    raise Exception("OPENAI_API_KEY not set")
client = OpenAI(api_key=openai_api_key)

def get_embeddings(texts: List[str], model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using OpenAI's embedding API.

    Args:
        texts: List of text strings to embed
        model: OpenAI embedding model to use

    Returns:
        List of embedding vectors
    """
    try:
        response = client.embeddings.create(
            input=texts,
            model=model
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        raise e

def get_embedding(text: str, model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")) -> List[float]:
    """
    Generate embedding for a single text string.

    Args:
        text: Text string to embed
        model: OpenAI embedding model to use

    Returns:
        Embedding vector
    """
    return get_embeddings([text], model)[0]