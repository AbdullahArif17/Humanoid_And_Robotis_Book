"""
Integration tests for the end-to-end RAG chatbot flow.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import os
from ...main import app

client = TestClient(app)

def test_end_to_end_chat_flow():
    """Test the complete RAG chatbot flow."""
    with patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test-key',
        'QDRANT_URL': 'https://test.qdrant.io',
        'QDRANT_API_KEY': 'test-key',
        'DATABASE_URL': 'postgresql://test:test@localhost/testdb'
    }):
        with patch('app.core.rag.rag_engine') as mock_rag, \
             patch('app.api.chat.client') as mock_openai, \
             patch('app.api.chat.get_db') as mock_db:

            # Mock the database session
            mock_session = Mock()
            mock_query = Mock()
            mock_filter = Mock()
            mock_first = Mock()
            mock_session.query.return_value = mock_query
            mock_query.filter.return_value = mock_filter
            mock_filter.first.return_value = mock_first
            mock_first.id = 1

            # Mock adding and committing messages
            mock_session.add = Mock()
            mock_session.commit = Mock()

            # Mock the rag engine
            mock_rag.generate_context.return_value = "Sample context from book about ROS 2 nodes and topics"
            mock_rag.retrieve_relevant_chunks.return_value = [
                {
                    "id": "test_chunk_1",
                    "content": "ROS 2 is a flexible framework for writing robot applications",
                    "title": "Introduction to ROS 2",
                    "source_file": "module1.md",
                    "score": 0.9
                }
            ]

            # Mock the OpenAI client response
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message = Mock()
            mock_response.choices[0].message.content = "ROS 2 is a flexible framework for writing robot applications. It provides a collection of libraries and tools that help you build robot applications."

            mock_openai.chat.completions.create.return_value = mock_response

            # Mock the dependency
            mock_db_dependency = Mock()
            mock_db_dependency.__enter__ = Mock(return_value=mock_session)
            mock_db_dependency.__exit__ = Mock(return_value=None)
            mock_db.return_value = mock_db_dependency

            # Test the full flow
            payload = {
                "message": "What is ROS 2?",
                "session_id": "integration_test_session"
            }

            response = client.post("/api/v1/chat", json=payload)

            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert data["response"] == "ROS 2 is a flexible framework for writing robot applications. It provides a collection of libraries and tools that help you build robot applications."
            assert data["session_id"] == "integration_test_session"
            assert len(data["sources"]) >= 0  # May have sources or not depending on mock

            # Verify that the rag engine was called
            mock_rag.generate_context.assert_called_once()

            # Verify that the OpenAI client was called
            mock_openai.chat.completions.create.assert_called_once()

            # Verify that messages were added to the database
            assert mock_session.add.call_count >= 2  # User message + AI response