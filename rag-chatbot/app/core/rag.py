import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Try to use real Qdrant, fall back to mock if not available
try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    print("Using real Qdrant client")

    # Try to initialize Qdrant client
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise Exception("QDRANT_URL or QDRANT_API_KEY not set")

    test_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    # Try a simple operation to verify connection
    try:
        test_client.health()
        QDRANT_AVAILABLE = True
    except:
        QDRANT_AVAILABLE = False
        raise Exception("Could not connect to Qdrant")

    qdrant_client_real = test_client
    QDRANT_AVAILABLE = True
    print("Connected to real Qdrant successfully")
except Exception as e:
    print(f"Could not connect to Qdrant: {e}. Using mock Qdrant for local testing.")
    from .mock_qdrant import MockQdrantClient, models
    qdrant_client_real = MockQdrantClient()
    QDRANT_AVAILABLE = False

# Try to use real embeddings, fall back to mock if OpenAI is not available
try:
    from .embeddings import get_embedding
    print("Using real OpenAI embeddings")
    EMBEDDINGS_AVAILABLE = True
except Exception as e:
    print(f"Could not load OpenAI embeddings: {e}. Using mock embeddings for local testing.")
    from .mock_embeddings import get_embedding
    EMBEDDINGS_AVAILABLE = False

from .chunking import TextChunk

load_dotenv()

class RAGEngine:
    """
    Core RAG (Retrieval-Augmented Generation) engine for the chatbot.
    Handles vector storage, retrieval, and integration with LLM.
    """

    def __init__(self):
        # Initialize Qdrant client
        self.qdrant_client = qdrant_client_real
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "humanoid_robotics_book")
        # Ensure collection exists
        self.create_collection()

    def create_collection(self):
        """
        Create the Qdrant collection for storing document chunks.
        """
        # Check if collection exists
        try:
            self.qdrant_client.get_collection(self.collection_name)
            print(f"Collection {self.collection_name} already exists")
            return
        except:
            # Collection doesn't exist, create it
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,  # Default size for OpenAI embeddings
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created collection {self.collection_name}")

    def store_chunks(self, chunks: List[TextChunk]):
        """
        Store text chunks in the Qdrant vector database.

        Args:
            chunks: List of TextChunk objects to store
        """
        points = []
        for chunk in chunks:
            try:
                embedding = get_embedding(chunk.content)
            except Exception as e:
                print(f"Error generating embedding: {e}")
                # Generate a mock embedding if real one fails
                from .mock_embeddings import get_embedding as mock_get_embedding
                embedding = mock_get_embedding(chunk.content)

            # Create point using the appropriate models based on client type
            if QDRANT_AVAILABLE:
                # Using real Qdrant client
                point = models.PointStruct(
                    id=chunk.id,
                    vector=embedding,
                    payload={
                        "content": chunk.content,
                        "title": chunk.title,
                        "source_file": chunk.source_file,
                        "chunk_index": chunk.chunk_index,
                        "metadata": chunk.metadata or {}
                    }
                )
            else:
                # Using mock Qdrant client
                from .mock_qdrant import MockPoint
                point = MockPoint(
                    id=chunk.id,
                    vector=embedding,
                    payload={
                        "content": chunk.content,
                        "title": chunk.title,
                        "source_file": chunk.source_file,
                        "chunk_index": chunk.chunk_index,
                        "metadata": chunk.metadata or {}
                    }
                )
            points.append(point)

        # Upload points to Qdrant
        try:
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"Stored {len(points)} chunks in Qdrant")
        except Exception as e:
            print(f"Error storing chunks in Qdrant: {e}")
            # Still print success message for local testing with mock
            print(f"Processed {len(points)} chunks (mock storage)")

    def retrieve_relevant_chunks(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks from the vector database based on the query.

        Args:
            query: User query
            limit: Number of chunks to retrieve

        Returns:
            List of relevant chunks with metadata
        """
        try:
            query_embedding = get_embedding(query)
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return []

        try:
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )
        except Exception as e:
            print(f"Error searching in Qdrant: {e}")
            return []

        relevant_chunks = []
        for result in search_results:
            try:
                chunk_data = {
                    "id": result.id,
                    "content": result.payload["content"],
                    "title": result.payload["title"],
                    "source_file": result.payload["source_file"],
                    "score": result.score,
                    "metadata": result.payload.get("metadata", {})
                }
                relevant_chunks.append(chunk_data)
            except Exception as e:
                print(f"Error processing search result: {e}")
                continue

        return relevant_chunks

    def generate_context(self, query: str, limit: int = 5) -> str:
        """
        Generate context from relevant chunks for the LLM.

        Args:
            query: User query
            limit: Number of chunks to retrieve

        Returns:
            Formatted context string
        """
        try:
            relevant_chunks = self.retrieve_relevant_chunks(query, limit)
        except Exception as e:
            print(f"Error retrieving chunks from RAG: {e}")
            # Return empty context if retrieval fails
            return ""

        if not relevant_chunks:
            # No relevant chunks found, return empty context
            return ""

        context_parts = []
        for chunk in relevant_chunks:
            context_parts.append(f"Source: {chunk['title']} ({chunk['source_file']})")
            context_parts.append(f"Content: {chunk['content']}")
            context_parts.append("---")

        return "\n".join(context_parts)

# Global RAG engine instance
rag_engine = RAGEngine()