# API Reference (v1)

Base prefix: `/api/v1`

## Global Endpoints

- `GET /health`
  - Health check with version and timestamp.
- `WS /ws/{client_id}`
  - Real-time command channel (currently supports `override` action).

## Agents

- `GET /api/v1/agents/status`
  - Returns service status.

## Content

- `POST /api/v1/content/generate`
  - Input: `ContentCreate`
  - Output: `ContentResponse`
  - Uses orchestrator + content pipeline + AI variations + confidence scoring.

- `POST /api/v1/content/generate-calendar`
  - Input: topics list + optional days/platforms
  - Output: generated calendar skeleton

- `POST /api/v1/content/{content_id}/approve`
  - Input: `ContentApprove`
  - Handles `approve | reject | modify` action branches.

- `GET /api/v1/content/queue`
  - Returns in-memory approval queue summary.

## Communications

- `POST /api/v1/communications/follow-up`
- `POST /api/v1/communications/meeting-reminder`
- `GET /api/v1/communications/team-progress`
- `POST /api/v1/communications/bulk-follow-up`

Note: current communications routes are scaffold responses while integration is completed.

## Decisions

- `POST /api/v1/decisions/analyze`
  - Input: `DecisionRequest`
  - Output: `DecisionResponse`

- `POST /api/v1/decisions/pricing`
- `POST /api/v1/decisions/client-priority`
- `POST /api/v1/decisions/feature-priority`

## Approvals

- `GET /api/v1/approvals/pending`

## Dashboard

- `GET /api/v1/dashboard/overview`
- `GET /api/v1/dashboard/metrics`
- `POST /api/v1/dashboard/override`

## Admin

- `POST /api/v1/admin/onboarding-sequence`
  - Input: generic `user_data` object
  - Output: generated onboarding sequence payload from `CommunicationManager`

## OpenAPI UI

- Swagger: `/docs`
- ReDoc: `/redoc`
