#!/usr/bin/env python3
"""
Script to ingest book content into the Qdrant vector database.
This script reads markdown files from the book/docs directory,
chunks them, generates embeddings, and stores them in Qdrant.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import with fallback logic similar to the main app
try:
    from app.core.embeddings import get_embedding
    print("Using real OpenAI embeddings for ingestion")
except Exception as e:
    print(f"Could not load OpenAI embeddings: {e}. Using mock embeddings for local testing.")
    from app.core.mock_embeddings import get_embedding

from app.core.chunking import chunk_markdown_files, MarkdownChunker
from app.core.rag import rag_engine

def main():
    print("Starting book content ingestion...")

    # Initialize the Qdrant collection
    print("Initializing Qdrant collection...")
    rag_engine.create_collection()

    # Find all markdown files in the book/docs directory
    book_docs_path = Path("../docs")  # Relative to rag-chatbot/ (parent directory)

    if not book_docs_path.exists():
        print(f"Error: Book docs directory not found at {book_docs_path}")
        return

    markdown_files = list(book_docs_path.glob("*.md"))

    if not markdown_files:
        print(f"No markdown files found in {book_docs_path}")
        return

    print(f"Found {len(markdown_files)} markdown files to process")

    # Process each markdown file
    for md_file in markdown_files:
        print(f"Processing {md_file.name}...")

        # Chunk the file
        chunker = MarkdownChunker()
        chunks = chunker.chunk_file(str(md_file), str(md_file.name))

        print(f"  Generated {len(chunks)} chunks")

        # Store chunks in Qdrant
        rag_engine.store_chunks(chunks)

    print("Ingestion completed successfully!")

if __name__ == "__main__":
    main()