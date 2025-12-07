#!/usr/bin/env python3
"""
Ingest book content into Qdrant vector database.
This script scans all markdown files in the book/docs directory,
chunks them, generates embeddings, and uploads to Qdrant.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from app.config import settings
from app.core.chunking import chunker
from app.core.embeddings import embedding_generator


def find_markdown_files(docs_dir: str) -> List[Path]:
    """Find all markdown files in the docs directory."""
    docs_path = Path(docs_dir)
    if not docs_path.exists():
        raise FileNotFoundError(f"Documentation directory not found: {docs_dir}")
    
    md_files = list(docs_path.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files")
    return md_files


def process_file(file_path: Path) -> List[Dict]:
    """Process a single markdown file into chunks."""
    print(f"Processing: {file_path.name}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chunk the content
        chunks = chunker.chunk_by_headers(content, str(file_path))
        
        print(f"  → Generated {len(chunks)} chunks")
        return chunks
    
    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}")
        return []


def ingest_to_qdrant(chunks: List[Dict], batch_size: int = 10):
    """
    Generate embeddings and upload chunks to Qdrant.
    
    Args:
        chunks: List of text chunks with metadata
        batch_size: Number of chunks to process in each batch
    """
    print(f"\nConnecting to Qdrant at {settings.qdrant_url}...")
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key
    )
    
    collection_name = settings.qdrant_collection_name
    
    # Verify collection exists
    try:
        client.get_collection(collection_name)
    except Exception:
        print(f"Error: Collection '{collection_name}' does not exist.")
        print("Please run 'python scripts/setup_qdrant.py' first.")
        sys.exit(1)
    
    print(f"Uploading {len(chunks)} chunks to Qdrant...")
    
    # Process in batches
    total_uploaded = 0
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        
        try:
            # Generate embeddings for batch
            texts = [chunk['content'] for chunk in batch]
            embeddings = embedding_generator.generate_embeddings_batch(texts)
            
            # Create points for Qdrant
            points = []
            for j, (chunk, embedding) in enumerate(zip(batch, embeddings)):
                point_id = total_uploaded + j
                points.append(
                    PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            'content': chunk['content'],
                            'metadata': chunk['metadata']
                        }
                    )
                )
            
            # Upload to Qdrant
            client.upsert(
                collection_name=collection_name,
                points=points
            )
            
            total_uploaded += len(batch)
            print(f"  Uploaded {total_uploaded}/{len(chunks)} chunks...")
            
            # Small delay to avoid rate limits
            time.sleep(0.5)
        
        except Exception as e:
            print(f"  ✗ Error uploading batch: {e}")
            continue
    
    print(f"\n✓ Successfully uploaded {total_uploaded} chunks to Qdrant!")


def main():
    """Main ingestion pipeline."""
    print("=" * 60)
    print("Book Content Ingestion Pipeline")
    print("=" * 60)
    
    # Find book docs directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    docs_dir = project_root / "book" / "docs"
    
    print(f"\nBook docs directory: {docs_dir}")
    
    # Find all markdown files
    md_files = find_markdown_files(str(docs_dir))
    
    if not md_files:
        print("No markdown files found!")
        return
    
    # Process all files
    print("\n" + "=" * 60)
    print("Processing markdown files...")
    print("=" * 60 + "\n")
    
    all_chunks = []
    for md_file in md_files:
        chunks = process_file(md_file)
        all_chunks.extend(chunks)
    
    print(f"\nTotal chunks generated: {len(all_chunks)}")
    
    if not all_chunks:
        print("No chunks to upload!")
        return
    
    # Ingest to Qdrant
    print("\n" + "=" * 60)
    print("Uploading to Qdrant...")
    print("=" * 60)
    
    ingest_to_qdrant(all_chunks)
    
    print("\n" + "=" * 60)
    print("Ingestion complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nIngestion interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
