import os
from typing import List
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_embeddings(texts: List[str], model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")) -> List[List[float]]:
    """
    Generate mock embeddings for a list of texts.
    This is for local testing when OpenAI API is not available.

    Args:
        texts: List of text strings to embed
        model: Embedding model to use (ignored for mock)

    Returns:
        List of embedding vectors
    """
    # Create deterministic embeddings based on text content
    embeddings = []
    for text in texts:
        # Create a simple hash-based embedding
        text_hash = hash(text) % (10 ** 8)  # Get a hash value
        # Generate a 1536-dimensional vector (standard for OpenAI embeddings)
        embedding = []
        for i in range(1536):
            # Use the hash and position to generate pseudo-random values
            val = ((text_hash * (i + 1)) % 10000) / 10000.0
            # Normalize to be between -1 and 1
            val = (val * 2) - 1
            embedding.append(val)
        embeddings.append(embedding)

    return embeddings

def get_embedding(text: str, model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")) -> List[float]:
    """
    Generate mock embedding for a single text string.

    Args:
        text: Text string to embed
        model: Embedding model to use (ignored for mock)

    Returns:
        Embedding vector
    """
    return get_embeddings([text], model)[0]