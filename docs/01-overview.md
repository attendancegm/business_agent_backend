# Backend Overview

This backend powers AI-assisted business workflows:

- Content generation and optimization
- Communications automation
- Decision-support endpoints
- Dashboard/override controls

## Goals

- Provide a stable API surface for frontend integration
- Keep orchestration logic centralized (`AgentOrchestrator`)
- Isolate integrations (`OpenRouterClient`, platform connectors)
- Support async DB access and background workloads

## Runtime Entry Points

- API app: `app/main.py`
- API router root: `app/api/v1/router.py`
- Background worker app: `app/tasks/celery_app.py`
- DB bootstrap script: `app/db/init_db.py`

## Request Lifecycle (High-Level)

1. Client calls a versioned endpoint under `/api/v1`.
2. Route validates payload with Pydantic schemas.
3. Route delegates to service/orchestrator methods.
4. Service may call:
   - DB models/repositories
   - OpenRouter API
   - platform connectors
5. Response is normalized into response schema JSON.

## Current Maturity

- API structure is in place and modularized by domain.
- Core content pipeline and OpenRouter integration are implemented.
- Several domain operations are intentionally placeholder while the refactor continues.
