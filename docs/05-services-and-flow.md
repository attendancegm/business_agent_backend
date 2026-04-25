# Services and Code Flow

## Service Modules

### `AgentOrchestrator` (`app/services/agent_orchestrator.py`)

Central coordinator for AI workflows.

Key responsibilities:
- Initiates content request processing
- Adds generated variations
- Scores confidence and updates approval queue
- Provides dashboard-compatible state access methods
- Handles manual override commands

Important fields:
- `active_tasks`: in-memory task state
- `approval_queue`: in-memory pending approval IDs

### `ContentPipeline` (`app/services/content_pipeline.py`)

Domain logic for content:
- `create_content(...)`
- `evaluate_content(...)`
- `optimize_content(...)`

Uses platform-specific rule selection and delegates text generation to `OpenRouterClient`.

### `OpenRouterClient` (`app/services/openrouter_client.py`)

AI API client with retry:
- Uses `httpx.AsyncClient`
- Uses `tenacity` exponential retry
- Handles JSON response mode
- Exposes:
  - `complete(...)`
  - `generate_content_variations(...)`
  - `analyze_content_performance(...)`

### `PlatformConnector` (`app/services/platform_connectors.py`)

Current placeholder integration adapter for:
- Facebook post
- Instagram post
- WhatsApp send

### `CommunicationManager` (`app/services/communication_manager.py`)

Handles communication operations:
- follow-up sequence generation
- meeting reminder payload creation
- team progress snapshot payload
- bulk follow-up queue payload
- onboarding sequence generation

## End-to-End Flow Example: Content Generate

1. `POST /api/v1/content/generate`
2. Route validates `ContentCreate`
3. Route gets orchestrator dependency
4. Orchestrator calls `ContentPipeline.create_content`
5. Orchestrator asks OpenRouter for variations
6. Orchestrator evaluates confidence score
7. Orchestrator decides `approved` vs `pending_approval`
8. Route returns `ContentResponse`

## Background Flow Example: Daily Content Task

From `app/tasks/content_tasks.py`:

1. Celery task starts
2. Build `OpenRouterClient` + `ContentPipeline`
3. Fetch trending topics (placeholder function)
4. Generate content for each platform/topic
5. Return summary payload

## Known Placeholder Areas

- `decision_engine` internals are not implemented.
- Some non-communication routes still return scaffold values pending full integration.
