# API Contract Guardian
 
This is a simple project that catches breaking API changes before they get merged. Built with **FastAPI** (the API + auto-generated OpenAPI schema) and **GitHub Actions** (the CI pipeline that diffs schemas between branches).
 
## What it does
 
On every pull request, a GitHub Actions workflow:
1. Spins up the API from both `main` and the PR branch.
2. Fetches each version's OpenAPI schema.
3. Diffs them to detect breaking changes (removed endpoints, removed/renamed fields, new required fields, etc.).
4. Posts a comment on the PR summarizing the changes.
5. Fails the check if there are unacknowledged breaking changes (add the `breaking-change` label to override).
## Project structure
 
```
app/            FastAPI application (models, routers, main)
tools/          Schema fetch + diff scripts
tests/          Pytest tests for the API
.github/workflows/   CI pipelines (tests + contract check)
```
