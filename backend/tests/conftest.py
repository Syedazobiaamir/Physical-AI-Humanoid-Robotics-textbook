"""
Pytest configuration and fixtures for backend tests
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Set test environment variables BEFORE importing any modules
os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")
os.environ.setdefault("GEMINI_API_KEY", "test-key-for-testing")
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-for-testing")
os.environ.setdefault("QDRANT_API_KEY", "test-key-for-testing")
os.environ.setdefault("QDRANT_URL", "https://test.qdrant.io")
os.environ.setdefault("DATABASE_URL", "")
os.environ.setdefault("TESTING", "true")

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def client():
    """Create a test client for the FastAPI application"""
    # Import app inside fixture to avoid import issues
    from src.main import app
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def api_prefix():
    """Return the API v1 prefix"""
    return "/api/v1"
