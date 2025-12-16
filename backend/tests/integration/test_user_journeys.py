"""
Integration tests for user journeys

Tests complete user flows end-to-end to verify the system
works as expected from a user's perspective.
"""
import pytest


class TestLandingPageJourney:
    """User Story 1 - Landing Page Experience"""

    def test_visitor_can_access_landing_info(self, client, api_prefix):
        """
        Scenario: Visitor arrives at the platform
        Given a visitor loads the homepage
        When they request platform statistics
        Then they receive data about books, users, and AI interactions
        """
        # Get platform stats (used by landing page)
        response = client.get(f"{api_prefix}/stats/")
        assert response.status_code == 200
        data = response.json()

        # Verify stats are available
        assert data["books_count"] >= 1
        assert "active_users" in data
        assert "ai_interactions" in data

    def test_visitor_can_view_platform_features(self, client, api_prefix):
        """
        Scenario: Visitor views feature cards
        When they request the stats summary
        Then they see available platform features
        """
        response = client.get(f"{api_prefix}/stats/summary")
        assert response.status_code == 200
        data = response.json()

        # Verify features are listed
        features = data["features"]
        assert features["personalization"]["enabled"] is True
        assert features["translation"]["enabled"] is True
        assert features["chatbot"]["enabled"] is True


class TestChatbotJourney:
    """User Story 4 - RAG Chatbot with AI Skills"""

    def test_chatbot_health_check_available(self, client, api_prefix):
        """
        Scenario: Learner opens chat widget
        Given a learner is on any page
        When they open the chatbot
        Then the chatbot system is available
        """
        response = client.get(f"{api_prefix}/rag/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_chatbot_validates_query(self, client, api_prefix):
        """
        Scenario: Learner types a question
        When they send an empty query
        Then they receive validation feedback
        """
        response = client.post(f"{api_prefix}/rag/query", json={"query": ""})
        assert response.status_code == 422  # Validation error

    def test_chatbot_context_selection_mode(self, client, api_prefix):
        """
        Scenario: Learner selects text and asks question
        When context_mode is 'selection'
        Then selected_text is required
        """
        response = client.post(
            f"{api_prefix}/rag/query",
            json={
                "query": "What does this mean?",
                "context_mode": "selection"
            }
        )
        assert response.status_code == 400
        assert "selected_text" in response.json()["detail"].lower()


class TestAPIHealthJourney:
    """System Health Verification"""

    def test_all_core_endpoints_healthy(self, client, api_prefix):
        """
        Scenario: System administrator checks platform health
        When checking all core endpoints
        Then all return successful responses
        """
        # Root endpoint
        assert client.get("/").status_code == 200

        # Health endpoint
        assert client.get("/health").status_code == 200

        # Stats endpoint
        assert client.get(f"{api_prefix}/stats/").status_code == 200

        # RAG health
        assert client.get(f"{api_prefix}/rag/health").status_code == 200

    def test_api_documentation_available(self, client):
        """
        Scenario: Developer needs API documentation
        When accessing /docs
        Then OpenAPI documentation is available
        """
        response = client.get("/docs")
        assert response.status_code == 200

        response = client.get("/redoc")
        assert response.status_code == 200
