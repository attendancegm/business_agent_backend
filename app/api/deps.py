from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.agent_orchestrator import AgentOrchestrator


async def get_agent_orchestrator(session: AsyncSession = Depends(get_db)) -> AgentOrchestrator:
    return AgentOrchestrator(session)
