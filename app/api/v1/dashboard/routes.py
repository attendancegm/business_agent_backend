from datetime import datetime

from fastapi import APIRouter, Depends

from app.api.deps import get_agent_orchestrator
from app.services.agent_orchestrator import AgentOrchestrator

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview")
async def get_dashboard_overview(agent: AgentOrchestrator = Depends(get_agent_orchestrator)):
    pending_approvals = await agent.content_repo.get_pending_approvals()
    dashboard = {
        "pending_approvals": len(pending_approvals),
        "content_scheduled_today": await agent._get_content_schedule(),
        "team_updates": await agent._get_team_status(),
        "active_tasks": {}, # Deprecated in-memory active tasks
        "recent_decisions": await agent._get_recent_decisions(),
        "performance_metrics": await agent._get_performance_metrics(),
    }
    return dashboard


@router.get("/metrics")
async def get_metrics():
    return {
        "content_metrics": {"total_posts": 0, "engagement_rate": 0, "conversion_rate": 0},
        "communication_metrics": {"follow_ups_sent": 0, "response_rate": 0, "meetings_booked": 0},
        "time_saved": {"content_creation_hours": 0, "admin_hours": 0, "communication_hours": 0},
    }


@router.post("/override")
async def override_agent(
    command: str, priority: str = "high", agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    result = await agent.override_agent_action(
        action_id=f"manual_{datetime.utcnow().timestamp()}",
        new_instructions=command,
    )
    return {"status": "overridden", "priority": priority, "result": result}
