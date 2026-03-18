"""
=============================================================
  conftest.py — Pytest Fixtures & Shared Configuration
  -------------------------------------------------------
  This file is automatically loaded by pytest before any
  test runs. It provides reusable fixtures available to
  ALL test files without needing to import them.

  Fixtures defined here:
    - api_client       : Pre-configured requests Session
    - sample_post_payload : Reusable POST payload dict
    - base_url         : The base API URL (can be overridden
                         via --base-url CLI flag for environments)
=============================================================
"""
import pytest
import requests


# ─── CLI Option: Override base URL per environment ─────────────────────────────
def pytest_addoption(parser):
    """Add --base-url option so CI can inject different env URLs."""
    parser.addoption(
        "--base-url",
        action="store",
        default="https://jsonplaceholder.typicode.com",
        help="Base URL for the API under test (default: JSONPlaceholder)"
    )


# ─── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url(pytestconfig):
    """
    Returns the base URL for the API.
    Scope=session means this is evaluated ONCE per test run,
    not once per test — saves overhead.
    """
    return pytestconfig.getoption("--base-url")


@pytest.fixture(scope="session")
def api_client(base_url):
    """
    Returns a configured requests.Session with:
      - base_url baked in via a helper
      - default headers (Content-Type, Accept)
      - a reasonable timeout (10s)

    Scope=session: one client for the entire test run.
    This is efficient and mimics real-world usage.
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })

    # Monkey-patch the session so tests can call:
    #   api_client.get("/users")
    # instead of:
    #   api_client.get("https://jsonplaceholder.typicode.com/users")
    _base = base_url.rstrip("/")

    original_request = session.request

    def request_with_base(method, url, **kwargs):
        if not url.startswith("http"):
            url = f"{_base}{url}"
        kwargs.setdefault("timeout", 10)
        return original_request(method, url, **kwargs)

    session.request = request_with_base

    yield session
    session.close()


@pytest.fixture
def sample_post_payload():
    """
    A reusable sample payload for POST/PUT tests.
    Scope=function (default): fresh dict per test.
    """
    return {
        "title": "QA Automation Test Post",
        "body": "This post was created by an automated test case.",
        "userId": 1
    }
