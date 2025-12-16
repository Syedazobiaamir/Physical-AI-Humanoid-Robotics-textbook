"""
Unit tests for main FastAPI application
"""
import pytest


class TestRootEndpoints:
    """Tests for root endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint returns correct response"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data
        assert "type" in data["database"]
        assert "configured" in data["database"]

    def test_docs_endpoint_available(self, client):
        """Test OpenAPI docs endpoint is available"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_endpoint_available(self, client):
        """Test ReDoc endpoint is available"""
        response = client.get("/redoc")
        assert response.status_code == 200
