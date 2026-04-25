from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.api.deps import get_agent_orchestrator
from app.services.agent_orchestrator import AgentOrchestrator

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/onboarding-sequence")
async def create_onboarding_sequence(
    user_data: Dict[str, Any], agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    sequence = await agent.communication_manager.create_onboarding_sequence(user_data=user_data)
    return {"onboarding_sequence": sequence}
