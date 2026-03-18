"""
=============================================================
  Test Suite: Comments API
  API Under Test: https://jsonplaceholder.typicode.com/comments
  Author: QA Team
  Description:
      Validates the /comments endpoint including filtering
      by postId and data integrity checks on nested resources.
=============================================================
"""
import pytest


class TestCommentsAPI:
    """Test cases for GET /comments"""

    def test_get_all_comments_status_200(self, api_client):
        """TC-CMT-001: Verify GET /comments returns HTTP 200"""
        response = api_client.get("/comments")
        assert response.status_code == 200

    def test_get_all_comments_count(self, api_client):
        """TC-CMT-002: Verify GET /comments returns 500 comments"""
        response = api_client.get("/comments")
        assert len(response.json()) == 500

    def test_comment_schema_fields(self, api_client):
        """TC-CMT-003: Verify each comment has required fields"""
        response = api_client.get("/comments")
        comments = response.json()
        required_fields = ["postId", "id", "name", "email", "body"]
        for comment in comments:
            for field in required_fields:
                assert field in comment, (
                    f"Missing field '{field}' in comment id={comment.get('id')}"
                )

    def test_filter_comments_by_post_id(self, api_client):
        """TC-CMT-004: Verify GET /comments?postId=1 returns only post 1 comments"""
        response = api_client.get("/comments?postId=1")
        comments = response.json()
        assert len(comments) > 0, "Should return comments for postId=1"
        for comment in comments:
            assert comment["postId"] == 1, (
                f"Expected postId=1, got {comment['postId']}"
            )

    def test_comment_email_format(self, api_client):
        """TC-CMT-005: Verify all comment email fields contain '@'"""
        response = api_client.get("/comments?postId=1")
        comments = response.json()
        for comment in comments:
            assert "@" in comment["email"], (
                f"Invalid email in comment id={comment['id']}: {comment['email']}"
            )

    def test_nested_comments_via_post(self, api_client):
        """TC-CMT-006: Verify nested route GET /posts/1/comments returns comments"""
        response = api_client.get("/posts/1/comments")
        assert response.status_code == 200
        comments = response.json()
        assert isinstance(comments, list)
        assert len(comments) > 0, "Nested comments for post 1 should not be empty"
        for comment in comments:
            assert comment["postId"] == 1
