"""
Contract tests for API endpoints

These tests verify API responses conform to expected schemas,
validating the contract between frontend and backend.
"""
import pytest
from typing import Any


def validate_schema(data: dict, required_fields: list[str], field_types: dict[str, type] | None = None) -> bool:
    """Validate response data against required fields and types"""
    # Check all required fields exist
    for field in required_fields:
        if field not in data:
            return False

    # Check types if specified
    if field_types:
        for field, expected_type in field_types.items():
            if field in data and not isinstance(data[field], expected_type):
                return False

    return True


class TestStatsAPIContract:
    """Contract tests for Statistics API"""

    def test_platform_stats_contract(self, client, api_prefix):
        """Verify platform stats response matches expected schema"""
        response = client.get(f"{api_prefix}/stats/")
        assert response.status_code == 200
        data = response.json()

        required_fields = [
            "books_count",
            "active_users",
            "ai_interactions",
            "chapters_count",
            "updated_at"
        ]
        field_types = {
            "books_count": int,
            "active_users": int,
            "ai_interactions": int,
            "chapters_count": int,
            "updated_at": str
        }

        assert validate_schema(data, required_fields, field_types)

    def test_stats_summary_contract(self, client, api_prefix):
        """Verify stats summary response matches expected schema"""
        response = client.get(f"{api_prefix}/stats/summary")
        assert response.status_code == 200
        data = response.json()

        # Top-level structure
        required_fields = ["platform", "features", "last_updated"]
        assert validate_schema(data, required_fields)

        # Platform object
        platform_fields = ["books_count", "active_users", "ai_interactions"]
        assert validate_schema(data["platform"], platform_fields)


class TestRAGAPIContract:
    """Contract tests for RAG API"""

    def test_rag_health_contract(self, client, api_prefix):
        """Verify RAG health response matches expected schema"""
        response = client.get(f"{api_prefix}/rag/health")
        assert response.status_code == 200
        data = response.json()

        required_fields = ["status", "models", "components"]
        field_types = {
            "status": str,
            "models": list,
            "components": dict
        }

        assert validate_schema(data, required_fields, field_types)


class TestRootAPIContract:
    """Contract tests for root endpoints"""

    def test_root_contract(self, client):
        """Verify root endpoint response matches expected schema"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()

        required_fields = ["message", "version", "status"]
        assert validate_schema(data, required_fields)
        assert data["version"] == "1.0.0"

    def test_health_contract(self, client):
        """Verify health endpoint response matches expected schema"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()

        required_fields = ["status", "service", "database"]
        assert validate_schema(data, required_fields)

        # Database sub-object
        db_fields = ["type", "configured"]
        assert validate_schema(data["database"], db_fields)
