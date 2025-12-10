import os
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from .mock_embeddings import get_embedding

@dataclass
class MockPoint:
    id: str
    vector: List[float]
    payload: Dict[str, Any]

class MockQdrantClient:
    """
    Mock implementation of Qdrant client for local development
    when the real Qdrant service is not available.
    """
    def __init__(self, url=None, api_key=None):
        self.collections = {}
        self.points = {}
        print("Using Mock Qdrant Client for local development")

    def get_collection(self, collection_name: str):
        """Mock getting a collection - raises exception if not exists"""
        if collection_name not in self.collections:
            raise Exception(f"Collection {collection_name} does not exist")
        return {"name": collection_name, "vectors_count": len(self.points.get(collection_name, []))}

    def create_collection(self, collection_name: str, vectors_config: Dict[str, Any]):
        """Mock creating a collection"""
        self.collections[collection_name] = {
            "name": collection_name,
            "config": vectors_config
        }
        self.points[collection_name] = []
        print(f"Created mock collection {collection_name}")

    def upsert(self, collection_name: str, points: List[MockPoint]):
        """Mock upserting points"""
        if collection_name not in self.points:
            self.points[collection_name] = []

        # Add or update points
        for point in points:
            # Check if point with same ID already exists and update it
            existing_idx = None
            for i, existing_point in enumerate(self.points[collection_name]):
                if existing_point.id == point.id:
                    existing_idx = i
                    break

            if existing_idx is not None:
                self.points[collection_name][existing_idx] = point
            else:
                self.points[collection_name].append(point)

        print(f"Upserted {len(points)} points to mock collection {collection_name}")

    def search(self, collection_name: str, query_vector: List[float], limit: int = 5):
        """Mock search - finds similar vectors using cosine similarity"""
        if collection_name not in self.points:
            return []

        collection_points = self.points[collection_name]

        # Calculate cosine similarity between query vector and all stored vectors
        similarities = []
        for point in collection_points:
            similarity = self._cosine_similarity(query_vector, point.vector)
            similarities.append((similarity, point))

        # Sort by similarity (descending) and return top results
        similarities.sort(key=lambda x: x[0], reverse=True)
        top_results = similarities[:limit]

        # Format results to match Qdrant response structure
        results = []
        for score, point in top_results:
            result = type('MockResult', (), {
                'id': point.id,
                'payload': point.payload,
                'score': score
            })()
            results.append(result)

        return results

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0

        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))

        # Calculate magnitudes
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        # Calculate cosine similarity
        return dot_product / (magnitude1 * magnitude2)

# Mock models for compatibility
class MockVectorParams:
    def __init__(self, size: int, distance: str):
        self.size = size
        self.distance = distance

class MockDistance:
    COSINE = "cosine"

# Mock models module
models = type('models', (), {
    'VectorParams': MockVectorParams,
    'Distance': MockDistance()
})()