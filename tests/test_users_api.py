"""
=============================================================
  Test Suite: Users API
  API Under Test: https://jsonplaceholder.typicode.com/users
  Author: QA Team
  Description:
      Validates the /users endpoint for status codes,
      response schema, data integrity, and edge cases.
=============================================================
"""
import pytest


class TestUsersAPI:
    """Test cases for GET /users endpoint"""

    def test_get_all_users_status_200(self, api_client):
        """TC-USR-001: Verify GET /users returns HTTP 200 OK"""
        response = api_client.get("/users")
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )

    def test_get_all_users_returns_list(self, api_client):
        """TC-USR-002: Verify GET /users returns a non-empty list"""
        response = api_client.get("/users")
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        assert len(data) > 0, "Users list should not be empty"

    def test_get_all_users_count(self, api_client):
        """TC-USR-003: Verify GET /users returns exactly 10 users"""
        response = api_client.get("/users")
        data = response.json()
        assert len(data) == 10, f"Expected 10 users, got {len(data)}"

    def test_user_schema_fields_present(self, api_client):
        """TC-USR-004: Verify each user object has required fields"""
        required_fields = ["id", "name", "username", "email", "address", "phone", "website", "company"]
        response = api_client.get("/users")
        users = response.json()
        for user in users:
            for field in required_fields:
                assert field in user, (
                    f"Field '{field}' missing in user id={user.get('id')}"
                )

    def test_get_single_user_status_200(self, api_client):
        """TC-USR-005: Verify GET /users/1 returns HTTP 200 OK"""
        response = api_client.get("/users/1")
        assert response.status_code == 200

    def test_get_single_user_correct_id(self, api_client):
        """TC-USR-006: Verify GET /users/1 returns user with id=1"""
        response = api_client.get("/users/1")
        user = response.json()
        assert user["id"] == 1, f"Expected id=1, got id={user['id']}"

    def test_get_single_user_email_format(self, api_client):
        """TC-USR-007: Verify user email contains '@' symbol"""
        response = api_client.get("/users/1")
        user = response.json()
        assert "@" in user["email"], (
            f"Invalid email format: {user['email']}"
        )

    def test_get_nonexistent_user_returns_404(self, api_client):
        """TC-USR-008: Verify GET /users/9999 returns HTTP 404 Not Found"""
        response = api_client.get("/users/9999")
        assert response.status_code == 404, (
            f"Expected 404 for nonexistent user, got {response.status_code}"
        )

    def test_response_content_type_is_json(self, api_client):
        """TC-USR-009: Verify Content-Type header is application/json"""
        response = api_client.get("/users")
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, (
            f"Expected application/json, got: {content_type}"
        )

    def test_response_time_under_threshold(self, api_client):
        """TC-USR-010: Verify GET /users responds within 3 seconds"""
        import time
        start = time.time()
        response = api_client.get("/users")
        elapsed = time.time() - start
        assert elapsed < 3.0, (
            f"Response took {elapsed:.2f}s, exceeded 3s threshold"
        )
