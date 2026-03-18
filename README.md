# QA API Test Automation + GitHub Actions CI/CD

> **Goal:** Understand how automated API tests plug into a CI/CD pipeline so every code change is automatically validated.

---

## Project Overview

This project demonstrates a complete QA automation setup using:

| Tool | Role |
|---|---|
| **Python + pytest** | Test framework |
| **requests** | HTTP client for API calls |
| **JSONPlaceholder API** | Free public API used as the System Under Test |
| **GitHub Actions** | CI/CD platform that runs tests automatically |
| **pytest-html** | Generates human-readable HTML test reports |

---

## Folder Structure

```
qa-cicd-project/
│
├── .github/
│   └── workflows/
│       └── api-tests.yml       ← CI/CD pipeline definition
│
├── tests/
│   ├── conftest.py             ← Shared fixtures (api_client, payloads)
│   ├── test_users_api.py       ← 10 test cases for /users endpoint
│   ├── test_posts_api.py       ← 15 test cases for /posts endpoint (CRUD)
│   └── test_comments_api.py    ←  6 test cases for /comments endpoint
│
├── reports/                    ← Auto-generated test reports (gitignored)
├── requirements.txt            ← Python dependencies
├── pytest.ini                  ← Pytest configuration
└── README.md                   ← This file
```

---

## Test Cases Summary (31 total)

### Users API (`test_users_api.py`) — 10 tests
| Test ID | Description | Type |
|---|---|---|
| TC-USR-001 | GET /users returns HTTP 200 | Smoke |
| TC-USR-002 | Response is a non-empty list | Smoke |
| TC-USR-003 | Exactly 10 users returned | Regression |
| TC-USR-004 | User object has all required fields | Regression |
| TC-USR-005 | GET /users/1 returns HTTP 200 | Smoke |
| TC-USR-006 | Correct user ID returned | Regression |
| TC-USR-007 | Email contains '@' | Regression |
| TC-USR-008 | Non-existent user returns 404 | Negative |
| TC-USR-009 | Content-Type is application/json | Regression |
| TC-USR-010 | Response time under 3 seconds | Performance |

### Posts API (`test_posts_api.py`) — 15 tests
| Test ID | Description | Type |
|---|---|---|
| TC-PST-001 | GET /posts returns 200 | Smoke |
| TC-PST-002 | Response is a list | Smoke |
| TC-PST-003 | Exactly 100 posts returned | Regression |
| TC-PST-004 | Post schema has required fields | Regression |
| TC-PST-005 | GET /posts/1 returns 200 | Smoke |
| TC-PST-006 | Correct post ID returned | Regression |
| TC-PST-007 | Filter by userId works | Regression |
| TC-PST-008 | Non-existent post returns 404 | Negative |
| TC-PST-009 | POST /posts returns 201 Created | Regression |
| TC-PST-010 | New post has an ID in response | Regression |
| TC-PST-011 | POST response reflects payload | Regression |
| TC-PST-012 | PUT /posts/1 returns 200 | Regression |
| TC-PST-013 | PUT response has updated fields | Regression |
| TC-PST-014 | DELETE /posts/1 returns 200 | Regression |
| TC-PST-015 | DELETE returns empty JSON body | Regression |

### Comments API (`test_comments_api.py`) — 6 tests
| Test ID | Description | Type |
|---|---|---|
| TC-CMT-001 | GET /comments returns 200 | Smoke |
| TC-CMT-002 | Exactly 500 comments returned | Regression |
| TC-CMT-003 | Comment schema has required fields | Regression |
| TC-CMT-004 | Filter by postId works | Regression |
| TC-CMT-005 | Email fields are valid format | Regression |
| TC-CMT-006 | Nested route /posts/1/comments works | Regression |

---

## How to Run Tests Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run all tests
```bash
pytest
```

### 3. Run only smoke tests
```bash
pytest -m smoke
```

### 4. Run only negative tests
```bash
pytest -m negative
```

### 5. Run against a different environment
```bash
pytest --base-url=https://your-staging-api.com
```

### 6. View the HTML report
After running, open `reports/test-report.html` in your browser.

---

## How the CI/CD Pipeline Works

The file `.github/workflows/api-tests.yml` defines the pipeline. Here's the flow:

```
Developer pushes code
        │
        ▼
┌─────────────────────────────┐
│    GitHub Actions triggered  │
│    (push / PR / nightly)    │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│   JOB 1: Smoke Tests        │
│   - Checkout code           │
│   - Set up Python 3.11      │
│   - pip install -r req.txt  │
│   - pytest -m smoke         │
│   - Upload smoke report     │
└─────────────┬───────────────┘
              │  (only if smoke PASS)
              ▼
┌─────────────────────────────┐
│   JOB 2: Full Regression    │
│   - Checkout code           │
│   - Set up Python 3.11      │
│   - pip install -r req.txt  │
│   - pytest (all tests)      │
│   - Upload full report      │
└─────────────┬───────────────┘
              │  (only if any job FAILS)
              ▼
┌─────────────────────────────┐
│   JOB 3: Notify on Failure  │
│   - Log failure message     │
│   - (Extend to Slack/email) │
└─────────────────────────────┘
```

### Pipeline Triggers Explained

| Trigger | When It Fires | What Runs |
|---|---|---|
| `push` to `main`/`develop` | Every code push | Smoke + Regression |
| `pull_request` to `main`/`develop` | Every PR | Smoke + Regression |
| `workflow_dispatch` | Manual click in GitHub UI | Smoke + Regression |
| `schedule` (cron `0 6 * * *`) | Every night at 6 AM UTC | Smoke + Regression |

### The `needs` Keyword (Gate)
Job 2 has `needs: smoke-tests` — this means the regression suite only runs if smoke tests PASS. This is a **quality gate**: no point running 100 tests if the basics are broken.

---

## Key Concepts for QA Awareness

### What is conftest.py?
It's pytest's shared configuration file. Any fixture defined here is available to every test file automatically. No imports needed. Key fixtures:
- `api_client` — a pre-configured `requests.Session` with base URL and headers
- `sample_post_payload` — a reusable dict for POST/PUT body data
- `base_url` — reads `--base-url` from CLI so you can point at any environment

### What are Markers?
Markers are tags you attach to tests (`@pytest.mark.smoke`). They let you run subsets:
- **smoke** → Fast sanity check on every push
- **regression** → Full coverage, run nightly or on release
- **negative** → Invalid input / error path tests
- **performance** → Response time threshold checks

### What is an Artifact in GitHub Actions?
After tests run, reports are uploaded as **artifacts** — downloadable files attached to that pipeline run. You can download the HTML report and open it without setting up any reporting server.

### How to Extend This Pipeline
| Goal | How |
|---|---|
| Add Slack alerts | Uncomment the Slack block in `api-tests.yml`, add `SLACK_WEBHOOK_URL` as a GitHub Secret |
| Run on multiple Python versions | Add a `matrix` strategy to the job |
| Add test data setup | Add a `before_suite` fixture in `conftest.py` |
| Parallel test execution | Add `pytest-xdist` to requirements and use `-n auto` flag |
| Allure reports | Replace `pytest-html` with `allure-pytest` and add Allure GitHub Action |

---

## Getting Started on GitHub

1. Create a new GitHub repository
2. Copy this project folder into it
3. Push to GitHub:
   ```bash
   git init
   git add .
   git commit -m "feat: initial QA automation project with CI/CD"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```
4. Go to **Actions** tab in GitHub — the pipeline fires automatically!
5. After it completes, click the run → **Artifacts** → download the HTML report

---

*Built with pytest + GitHub Actions | API: JSONPlaceholder (typicode.com)*
