# Architecture

## System Diagram (Conceptual)

Frontend (Next.js) -> FastAPI Backend -> SQLite/Redis/OpenRouter

- Frontend communicates with:
  - REST endpoints (`/api/v1/*`)
  - WebSocket endpoint (`/ws/{client_id}`)
- Backend composes domain routers and service modules.
- SQLAlchemy models persist domain entities.
- OpenRouter provides LLM completion services.
- Celery handles async/background jobs.

## Layered Structure

### 1) API Layer (`app/api`)
- Defines routes and dependency wiring.
- Splits endpoints by domain (`content`, `communications`, `decisions`, `dashboard`, `agents`, `approvals`).

### 2) Service Layer (`app/services`)
- Encapsulates orchestration/business behavior.
- `AgentOrchestrator` coordinates cross-domain flow.
- `ContentPipeline` handles content generation/evaluation/optimization.
- `OpenRouterClient` manages external LLM calls with retry.

### 3) Data Layer (`app/db`, `app/models`)
- `session.py` configures async engine and session factory.
- Models define persistence schema for content, communications, decisions.
- Startup lifecycle creates missing tables from model metadata.

### 4) Background Layer (`app/tasks`)
- Celery app config and content tasks.
- Designed for scheduled and long-running operations.

## App Startup Sequence

From `app/main.py`:

1. Load settings via `app.core.config`.
2. Create FastAPI app with lifespan manager.
3. On startup:
   - run `Base.metadata.create_all`
   - configure Celery beat schedule
4. Register CORS and API routers.
5. Expose health endpoint and WebSocket endpoint.

## Configuration Architecture

- `.env` is loaded using `python-dotenv`.
- `Settings` class (`pydantic-settings`) is the typed source of configuration.
- Defaults are local-dev friendly (SQLite).

## Database Strategy (Current)

- Local default: `sqlite+aiosqlite:///./agent.db`
- Engine options are conditional:
  - SQLite -> `check_same_thread=False`
  - Other engines -> pooling settings enabled

## Extensibility Points

- Add new domain router under `app/api/v1/<domain>/routes.py`
- Add service module in `app/services`
- Add Pydantic schemas in `app/schemas`
- Add SQLAlchemy model in `app/models` and import via `app/models/__init__.py`
