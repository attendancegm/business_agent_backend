# Developer Runbook

This runbook is for team members onboarding to backend development.

## Prerequisites

- Python 3.11+
- `uv` installed
- Redis (optional for local API-only work, required for Celery broker/backend)

## First-Time Setup

1. Go to backend folder:
   - `cd backend`
2. Create env file:
   - `Copy-Item .env.example .env`
3. Fill required secrets in `.env`:
   - `OPENROUTER_API_KEY`
   - `JWT_SECRET_KEY`
4. Install deps:
   - `uv sync`
5. Initialize DB:
   - `uv run python -m app.db.init_db`

## Run Commands

- API server:
  - `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Optional Celery worker:
  - `uv run celery -A app.tasks.celery_app.celery_app worker --loglevel=info`
- Optional Celery beat:
  - `uv run celery -A app.tasks.celery_app.celery_app beat --loglevel=info`

## Verification Checklist

- `GET /health` returns `200`
- `/docs` page loads
- `POST /api/v1/content/generate` returns valid JSON
- `agent.db` file is created after startup/init

## Coding Conventions for This Project

- Keep route handlers thin; move logic to services.
- Keep service methods async-friendly.
- Put request/response contracts in `app/schemas`.
- Add model imports to `app/models/__init__.py` when creating new tables.
- Never hardcode secrets; use `.env`.

## Common Issues

- Missing env variables -> app boot fails in settings load.
- SQLite path confusion -> run commands from `backend/` root.
- Redis not running -> Celery worker/beat fail; API can still run for many routes.

## Refactor Roadmap (Current)

- Complete communication manager service wiring
- Complete decision engine implementation
- Replace in-memory queues/state with DB-backed equivalents
- Add repository layer usage in route/service paths
- Add tests for each domain route group
