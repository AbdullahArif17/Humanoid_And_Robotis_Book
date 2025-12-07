from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from ..main import settings # Import settings from main.py

# Initialize Qdrant client
# This client will connect to the Qdrant instance specified in QDRANT_URL
# using the QDRANT_API_KEY for authentication.
def get_qdrant_client() -> QdrantClient:
    """
    Initializes and returns a Qdrant client.
    """
    client = QdrantClient(
        url=settings.QDRANT_URL, 
        api_key=settings.QDRANT_API_KEY
    )
    return client

# You might also want to add functions here for:
# - Creating collections if they don't exist
# - Upserting vectors
# - Performing search queries
# - Deleting vectors/collections

# Example function to ensure collection exists (can be called during app startup)
async def initialize_qdrant_collection(
    client: QdrantClient, 
    collection_name: str, 
    vector_size: int, 
    distance_metric: Distance = Distance.COSINE
):
    """
    Ensures that a Qdrant collection with the specified name and vector parameters exists.
    If the collection does not exist, it will be created.
    """
    try:
        client.get_collection(collection_name=collection_name)
        print(f"Collection '{collection_name}' already exists.")
    except Exception: # Qdrant client raises exceptions if collection not found
        print(f"Collection '{collection_name}' not found. Creating it...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance_metric),
        )
        print(f"Collection '{collection_name}' created.")

