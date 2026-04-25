from typing import List

from fastapi import APIRouter, Depends

from pydantic import BaseModel
from app.api.deps import get_agent_orchestrator
from app.schemas.communications import FollowUpRequest
from app.services.agent_orchestrator import AgentOrchestrator

class BulkFollowUpRequest(BaseModel):
    contact_ids: List[int]
    context: str

router = APIRouter(prefix="/communications", tags=["communications"])


@router.post("/follow-up")
async def create_follow_up(
    request: FollowUpRequest, agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    follow_up = await agent.handle_follow_up_sequence(
        contact_id=request.contact_id,
        context=request.context,
        sequence_type=request.sequence_type,
    )
    return {"follow_up": follow_up}


@router.post("/meeting-reminder")
async def create_meeting_reminder(
    contact_id: int, meeting_id: int, agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    reminder = await agent.communication_manager.create_meeting_reminder(contact_id=contact_id, meeting_id=meeting_id)
    return {"reminder": reminder, "status": "sent"}


@router.get("/team-progress")
async def get_team_progress(agent: AgentOrchestrator = Depends(get_agent_orchestrator)):
    progress = await agent.communication_manager.get_team_progress()
    return {"team_progress": progress}


@router.post("/bulk-follow-up")
async def bulk_follow_up(
    request: BulkFollowUpRequest, agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    result = await agent.communication_manager.bulk_follow_up(contact_ids=request.contact_ids, context=request.context)
    return {"status": "processing", "result": result}
