"""
Unit tests for Statistics API endpoints
"""
import pytest


class TestStatsEndpoints:
    """Tests for statistics endpoints"""

    def test_get_platform_stats(self, client, api_prefix):
        """Test getting platform statistics"""
        response = client.get(f"{api_prefix}/stats/")
        assert response.status_code == 200
        data = response.json()

        # Verify required fields
        assert "books_count" in data
        assert "active_users" in data
        assert "ai_interactions" in data
        assert "chapters_count" in data
        assert "updated_at" in data

        # Verify types
        assert isinstance(data["books_count"], int)
        assert isinstance(data["active_users"], int)
        assert isinstance(data["ai_interactions"], int)
        assert data["books_count"] >= 1  # At least 1 book

    def test_get_stats_summary(self, client, api_prefix):
        """Test getting detailed statistics summary"""
        response = client.get(f"{api_prefix}/stats/summary")
        assert response.status_code == 200
        data = response.json()

        # Verify structure
        assert "platform" in data
        assert "features" in data
        assert "last_updated" in data

        # Verify platform stats
        platform = data["platform"]
        assert "books_count" in platform
        assert "active_users" in platform

        # Verify features
        features = data["features"]
        assert "personalization" in features
        assert "translation" in features
        assert "chatbot" in features

    def test_increment_interactions(self, client, api_prefix):
        """Test incrementing AI interactions counter"""
        # Get current count
        response = client.get(f"{api_prefix}/stats/")
        initial_count = response.json()["ai_interactions"]

        # Increment
        response = client.post(f"{api_prefix}/stats/increment-interactions")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        # Verify increment
        response = client.get(f"{api_prefix}/stats/")
        new_count = response.json()["ai_interactions"]
        assert new_count == initial_count + 1
