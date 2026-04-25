# Musbi Backend

FastAPI backend for the Musbi AI agent system. This service exposes REST + WebSocket endpoints, coordinates AI-assisted workflows, and stores domain data in SQLite (for now).

## Tech Stack

- `FastAPI` for HTTP + WebSocket APIs
- `SQLAlchemy` async ORM with `aiosqlite`
- `Pydantic Settings` + `python-dotenv` for config
- `Celery` for background task workers/scheduling
- `httpx` + `tenacity` for OpenRouter API calls
- `uv` for dependency and runtime management

## Project Layout

```text
backend/
├── app/
│   ├── main.py                # FastAPI app entrypoint and lifecycle
│   ├── api/                   # API dependencies and v1 routers
│   ├── core/                  # Settings/config/security primitives
│   ├── db/                    # DB engine, session, initialization
│   ├── models/                # SQLAlchemy domain models
│   ├── schemas/               # Request/response schemas
│   ├── services/              # Business orchestration and integrations
│   ├── tasks/                 # Celery app and background jobs
│   └── utils/                 # Utility modules
├── docs/                      # Full backend documentation
├── .env.example               # Environment variable template
├── pyproject.toml             # Project metadata and dependencies
└── README.md
```

## Local Setup (UV)

1. Copy env file:
   - `cp .env.example .env` (PowerShell: `Copy-Item .env.example .env`)
2. Update `.env` values:
   - `OPENROUTER_API_KEY`
   - `JWT_SECRET_KEY`
3. Install dependencies:
   - `uv sync`
4. Start API server:
   - `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## Running the Backend

- Health endpoint: `GET /health`
- API base prefix: `/api/v1`
- Admin onboarding endpoint: `POST /api/v1/admin/onboarding-sequence`
- API docs:
  - Swagger: `http://localhost:8000/docs`
  - ReDoc: `http://localhost:8000/redoc`

## Database (Current State)

- Default DB is SQLite:
  - `DATABASE_URL=sqlite+aiosqlite:///./agent.db`
- Tables are auto-created on startup from model metadata.
- Manual initialization:
  - `uv run python -m app.db.init_db`

## Environment Variables

See `.env.example` for complete list.

Required for local boot:
- `OPENROUTER_API_KEY`
- `JWT_SECRET_KEY`

Key runtime variables:
- `DATABASE_URL`
- `DEBUG`
- `API_V1_PREFIX`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`

## Background Tasks

- Celery app is configured in `app/tasks/celery_app.py`.
- Content task examples live in `app/tasks/content_tasks.py`.
- A sample beat schedule is set in app lifespan (`app/main.py`).

## Documentation Map

Read these in order if you are new to the project:

1. `docs/01-overview.md`
2. `docs/02-architecture.md`
3. `docs/03-api-reference.md`
4. `docs/04-data-models.md`
5. `docs/05-services-and-flow.md`
6. `docs/06-dev-runbook.md`

## Current Implementation Notes

- Some modules are scaffolds/placeholders and return mock/default structures.
- `communication_manager` is wired into communications/admin routes.
- `decision_engine` internals are not fully implemented yet.
- Endpoints are structured and wired, but parts of domain logic are still in progressive refactor.
