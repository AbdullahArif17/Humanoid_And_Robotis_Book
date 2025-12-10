"""
Unit tests for the chat API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from ...main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_chat_endpoint_success():
    """Test the chat endpoint with a successful request."""
    with patch('app.api.chat.client') as mock_openai, \
         patch('app.api.chat.rag_engine') as mock_rag, \
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
        mock_rag.generate_context.return_value = "Sample context from book"

        # Mock the OpenAI client response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "This is a test response from the AI."

        mock_openai.chat.completions.create.return_value = mock_response

        # Mock the dependency
        mock_db_dependency = Mock()
        mock_db_dependency.__enter__ = Mock(return_value=mock_session)
        mock_db_dependency.__exit__ = Mock(return_value=None)
        mock_db.return_value = mock_db_dependency

        # Make the request
        payload = {
            "message": "What is ROS 2?",
            "session_id": "test_session_123"
        }

        response = client.post("/api/v1/chat", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "session_id" in data
        assert data["session_id"] == "test_session_123"

def test_chat_endpoint_missing_message():
    """Test the chat endpoint with missing message."""
    payload = {
        "session_id": "test_session_123"
    }

    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 422  # Validation error

def test_chat_endpoint_missing_session_id():
    """Test the chat endpoint with missing session_id."""
    payload = {
        "message": "What is ROS 2?"
    }

    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 422  # Validation error