#!/usr/bin/env python3
"""
Setup Qdrant collection for the book content.
Run this script before ingesting book content.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import settings


def setup_qdrant_collection():
    """Create Qdrant collection with proper configuration."""
    
    print(f"Connecting to Qdrant at {settings.qdrant_url}...")
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key
    )
    
    collection_name = settings.qdrant_collection_name
    
    # Check if collection exists
    try:
        collections = client.get_collections()
        existing_collections = [col.name for col in collections.collections]
        
        if collection_name in existing_collections:
            print(f"Collection '{collection_name}' already exists.")
            response = input("Do you want to recreate it? (yes/no): ")
            if response.lower() == 'yes':
                print(f"Deleting existing collection '{collection_name}'...")
                client.delete_collection(collection_name)
            else:
                print("Keeping existing collection.")
                return
    except Exception as e:
        print(f"Error checking collections: {e}")
    
    # Create collection
    # OpenAI text-embedding-3-small produces 1536-dimensional vectors
    print(f"Creating collection '{collection_name}'...")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=1536,  # OpenAI embedding dimension
            distance=Distance.COSINE
        )
    )
    
    print(f"✓ Collection '{collection_name}' created successfully!")
    print(f"  - Vector size: 1536")
    print(f"  - Distance metric: Cosine")
    

if __name__ == "__main__":
    try:
        setup_qdrant_collection()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
