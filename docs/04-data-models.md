# Data Models

This project uses SQLAlchemy models grouped by domain.

## Model Registration

- Base class: `app.db.session.Base`
- Import hub: `app/models/__init__.py`
- Startup table creation: `Base.metadata.create_all` in `app/main.py`

## Content Domain (`app/models/content.py`)

- `ContentLibrary`
  - Main generated/published content record.
  - Includes metadata, targeting, lifecycle state, and performance metrics.
- `Campaign`
  - Campaign metadata and relationship to content records.
- `ApprovalHistory`
  - Tracks approval/rejection/modification events per content item.

## Communications Domain (`app/models/communications.py`)

- `Contact`
  - CRM-like entity for people/accounts.
- `Message`
  - Sent/generated messages and delivery/response telemetry.
- `Meeting`
  - Meeting scheduling, notes, follow-up context.
- `TeamMember`
  - Internal workload/check-in tracking model.

## Decisions Domain (`app/models/decisions.py`)

- `DecisionLog`
  - Decision context, recommendation, confidence, and outcome tracking.
- `PricingAnalysis`
  - Pricing inputs, AI suggestions, final chosen price.
- `ClientPriority`
  - Multi-factor client scoring and recommendation.

## SQLite Notes

- Current local DB file is `agent.db`.
- SQLite is good for local dev and iteration.
- For production scale, migrate to Postgres and Alembic migrations.
