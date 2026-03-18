"""
=============================================================
  Test Suite: Posts API
  API Under Test: https://jsonplaceholder.typicode.com/posts
  Author: QA Team
  Description:
      Validates CRUD-like operations on the /posts endpoint:
      GET (list & single), POST (create), PUT (update),
      DELETE, and negative/edge cases.
=============================================================
"""
import pytest


class TestPostsAPIGet:
    """Test cases for GET /posts"""

    @pytest.mark.smoke
    def test_get_all_posts_status_200(self, api_client):
        """TC-PST-001: Verify GET /posts returns HTTP 200"""
        response = api_client.get("/posts")
        assert response.status_code == 200

    def test_get_all_posts_is_list(self, api_client):
        """TC-PST-002: Verify GET /posts returns a list"""
        response = api_client.get("/posts")
        assert isinstance(response.json(), list)

    def test_get_all_posts_count(self, api_client):
        """TC-PST-003: Verify GET /posts returns 100 posts"""
        response = api_client.get("/posts")
        assert len(response.json()) == 100

    def test_post_schema_has_required_fields(self, api_client):
        """TC-PST-004: Verify each post has id, userId, title, body"""
        response = api_client.get("/posts")
        posts = response.json()
        required_fields = ["id", "userId", "title", "body"]
        for post in posts:
            for field in required_fields:
                assert field in post, (
                    f"Missing field '{field}' in post id={post.get('id')}"
                )
    @pytest.mark.smoke
    def test_get_single_post_status_200(self, api_client):
        """TC-PST-005: Verify GET /posts/1 returns HTTP 200"""
        response = api_client.get("/posts/1")
        assert response.status_code == 200

    def test_get_single_post_correct_id(self, api_client):
        """TC-PST-006: Verify GET /posts/1 returns post with id=1"""
        response = api_client.get("/posts/1")
        post = response.json()
        assert post["id"] == 1

    def test_get_posts_by_user_filter(self, api_client):
        """TC-PST-007: Verify GET /posts?userId=1 filters correctly"""
        response = api_client.get("/posts?userId=1")
        posts = response.json()
        assert len(posts) > 0, "Should return posts for userId=1"
        for post in posts:
            assert post["userId"] == 1, (
                f"Expected userId=1, got {post['userId']}"
            )

    def test_get_nonexistent_post_returns_404(self, api_client):
        """TC-PST-008: Verify GET /posts/9999 returns 404"""
        response = api_client.get("/posts/9999")
        assert response.status_code == 404


class TestPostsAPICreate:
    """Test cases for POST /posts (Create)"""

    def test_create_post_returns_201(self, api_client, sample_post_payload):
        """TC-PST-009: Verify POST /posts returns HTTP 201 Created"""
        response = api_client.post("/posts", json=sample_post_payload)
        assert response.status_code == 201, (
            f"Expected 201 Created, got {response.status_code}"
        )

    def test_create_post_returns_new_id(self, api_client, sample_post_payload):
        """TC-PST-010: Verify POST /posts returns a new post with an id"""
        response = api_client.post("/posts", json=sample_post_payload)
        post = response.json()
        assert "id" in post, "Response should include 'id' for the new post"
        assert post["id"] is not None

    def test_create_post_reflects_payload(self, api_client, sample_post_payload):
        """TC-PST-011: Verify POST /posts response reflects submitted data"""
        response = api_client.post("/posts", json=sample_post_payload)
        post = response.json()
        assert post["title"] == sample_post_payload["title"]
        assert post["body"] == sample_post_payload["body"]
        assert post["userId"] == sample_post_payload["userId"]


class TestPostsAPIUpdate:
    """Test cases for PUT /posts (Update)"""

    def test_update_post_returns_200(self, api_client, sample_post_payload):
        """TC-PST-012: Verify PUT /posts/1 returns HTTP 200"""
        response = api_client.put("/posts/1", json=sample_post_payload)
        assert response.status_code == 200

    def test_update_post_reflects_new_data(self, api_client, sample_post_payload):
        """TC-PST-013: Verify PUT /posts/1 response has updated fields"""
        response = api_client.put("/posts/1", json=sample_post_payload)
        post = response.json()
        assert post["title"] == sample_post_payload["title"]
        assert post["body"] == sample_post_payload["body"]


class TestPostsAPIDelete:
    """Test cases for DELETE /posts"""

    def test_delete_post_returns_200(self, api_client):
        """TC-PST-014: Verify DELETE /posts/1 returns HTTP 200"""
        response = api_client.delete("/posts/1")
        assert response.status_code == 200

    def test_delete_post_returns_empty_body(self, api_client):
        """TC-PST-015: Verify DELETE /posts/1 returns empty JSON object"""
        response = api_client.delete("/posts/1")
        assert response.json() == {}, (
            "DELETE response body should be an empty JSON object"
        )
