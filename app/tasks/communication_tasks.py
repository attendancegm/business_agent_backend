import asyncio
from typing import Any, Dict

from app.services.communication_manager import CommunicationManager
from app.services.openrouter_client import OpenRouterClient
from app.tasks.celery_app import celery_app


@celery_app.task(bind=True)
def check_team_progress(self) -> Dict[str, Any]:
    async def _run() -> Dict[str, Any]:
        manager = CommunicationManager(OpenRouterClient())
        progress = await manager.get_team_progress()
        return {"status": "ok", "team_progress": progress}

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_run())
