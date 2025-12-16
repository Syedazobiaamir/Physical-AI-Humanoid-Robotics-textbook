"""
Unit tests for RAG API endpoints
"""
import pytest


class TestRAGEndpoints:
    """Tests for RAG chatbot endpoints"""

    def test_rag_health_endpoint(self, client, api_prefix):
        """Test RAG health check endpoint"""
        response = client.get(f"{api_prefix}/rag/health")
        assert response.status_code == 200
        data = response.json()

        # Verify required fields
        assert "status" in data
        assert "models" in data
        assert "components" in data

        # Status should be a string
        assert isinstance(data["status"], str)
        assert isinstance(data["models"], list)
        assert isinstance(data["components"], dict)

    def test_rag_query_validation(self, client, api_prefix):
        """Test RAG query input validation - empty query"""
        response = client.post(
            f"{api_prefix}/rag/query",
            json={"query": ""}
        )
        assert response.status_code == 422  # Validation error

    def test_rag_query_selection_mode_requires_text(self, client, api_prefix):
        """Test RAG query - selection mode requires selected_text"""
        response = client.post(
            f"{api_prefix}/rag/query",
            json={
                "query": "What does this mean?",
                "context_mode": "selection"
                # Missing selected_text
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert "selected_text" in data["detail"].lower()
