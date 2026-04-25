from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends

from app.api.deps import get_agent_orchestrator
from app.schemas.content import ContentApprove, ContentCreate, ContentResponse
from app.services.agent_orchestrator import AgentOrchestrator

router = APIRouter(prefix="/content", tags=["content"])


@router.post("/generate", response_model=ContentResponse)
async def generate_content(
    request: ContentCreate, agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    content = await agent.process_content_request(
        platform=request.platform,
        topic=request.topic,
        content_type=request.content_type,
        tone=request.tone,
        target_audience=request.target_audience,
    )
    return ContentResponse(**content)


@router.post("/generate-calendar")
async def generate_content_calendar(
    topics: List[str],
    days: int = 7,
    platforms: List[str] = ["facebook", "instagram", "whatsapp"],
    agent: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    calendar = [{"topic": t, "days": days, "platforms": platforms} for t in topics]
    return {"calendar": calendar}


@router.post("/{content_id}/approve")
async def approve_content(
    content_id: int,
    approval: ContentApprove,
    background_tasks: BackgroundTasks,
    agent: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    if approval.action == "approve":
        return {"status": "approved", "content_id": content_id, "scheduled_time": approval.scheduled_time}
    if approval.action == "reject":
        return {"status": "rejected", "content_id": content_id}
    if approval.action == "modify":
        return {"status": "modified", "content_id": content_id, "changes": approval.modifications}
    return {"status": "unknown_action", "content_id": content_id}


@router.get("/queue")
async def get_content_queue(
    status: Optional[str] = "pending_approval", agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    if status == "pending_approval":
        queue = await agent.content_repo.get_pending_approvals()
    else:
        queue = []
    
    return {"status": status, "pending_items": len(queue), "items": queue}
