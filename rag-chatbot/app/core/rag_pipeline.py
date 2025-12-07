from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from .embeddings import embed_text
from .qdrant_client import get_qdrant_client

# Define the Qdrant collection name where book content chunks are stored
QDRANT_COLLECTION_NAME = "book_content_chunks"

async def retrieve_context(query: str, top_k: int = 5) -> List[str]:
    """
    Retrieves relevant text chunks from Qdrant based on the embedded query.
    """
    qdrant_client = get_qdrant_client()
    query_embedding = embed_text(query)

    search_result = qdrant_client.search(
        collection_name=QDRANT_COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k,
        # You can add filters here if needed, e.g., to filter by module or chapter
        # query_filter=Filter(
        #     must=[
        #         FieldCondition(
        #             key="module",
        #             match=MatchValue(value="ROS 2")
        #         )
        #     ]
        # )
    )
    
    context_chunks = [hit.payload["text"] for hit in search_result if hit.payload and "text" in hit.payload]
    return context_chunks

def augment_prompt(query: str, context: List[str]) -> str:
    """
    Combines the original query with retrieved context to create an augmented prompt.
    """
    if not context:
        return query
    
    context_str = "\n".join(context)
    augmented_prompt = f"Based on the following information:\n\n{context_str}\n\nAnswer the question: {query}"
    return augmented_prompt
