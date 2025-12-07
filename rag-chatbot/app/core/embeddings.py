from sentence_transformers import SentenceTransformer

_embedding_model = None

def get_embedding_model():
    """
    Initializes and returns the SentenceTransformer embedding model.
    """
    global _embedding_model
    if _embedding_model is None:
        # You can choose a different model here if needed.
        # Ensure it's suitable for your specific use case and available resources.
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model

def embed_text(text: str):
    """
    Embeds a given text using the initialized SentenceTransformer model.
    """
    model = get_embedding_model()
    embedding = model.encode(text)
    return embedding.tolist()