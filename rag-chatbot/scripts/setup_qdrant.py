#!/usr/bin/env python3
"""
Script to setup Qdrant collection for the book content.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.rag import rag_engine

def main():
    print("Setting up Qdrant collection...")

    # Initialize the Qdrant collection
    rag_engine.create_collection()

    print("Qdrant collection setup completed successfully!")

if __name__ == "__main__":
    main()