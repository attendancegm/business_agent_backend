import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.repositories.communication_repo import CommunicationRepository
from app.repositories.content_repo import ContentRepository
from app.repositories.decision_repo import DecisionRepository
from app.services.communication_manager import CommunicationManager
from app.services.content_pipeline import ContentPipeline
from app.services.decision_engine import DecisionEngine
from app.services.openrouter_client import OpenRouterClient

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Coordinates content, communication, and decision workflows."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.ai_client = OpenRouterClient()
        self.content_pipeline = ContentPipeline(self.ai_client)
        
        # Repositories
        self.comm_repo = CommunicationRepository(session)
        self.content_repo = ContentRepository(session)
        self.decision_repo = DecisionRepository(session)
        
        # Services
        self.communication_manager = CommunicationManager(self.ai_client, self.comm_repo)
        self.decision_engine = DecisionEngine(self.ai_client, self.decision_repo)

    async def execute_daily_brief(self) -> Dict[str, Any]:
        context = await self._gather_system_context()
        result = await self.ai_client.complete(
            system_prompt="Create a concise executive daily brief in JSON.",
            user_message=f"Current system context:\n{json.dumps(context, indent=2)}",
            response_format="json",
        )
        brief = json.loads(result["content"])
        return brief

    async def _gather_system_context(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "pending_tasks": await self._get_pending_tasks(),
            "team_status": await self._get_team_status(),
            "content_schedule": await self._get_content_schedule(),
            "recent_activity": await self._get_recent_activity(),
        }

    async def process_content_request(
        self,
        platform: str,
        topic: str,
        content_type: str = "social_post",
        tone: str = "professional",
        target_audience: str = "general",
        campaign_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        content = await self.content_pipeline.create_content(
            platform=platform,
            topic=topic,
            content_type=content_type,
            tone=tone,
            target_audience=target_audience,
        )
        variations = await self.ai_client.generate_content_variations(
            base_content=content.get("content_text", ""),
            platform=platform,
        )
        content["variations"] = variations
        content["campaign_id"] = campaign_id
        confidence = await self.content_pipeline.evaluate_content(content)
        content["confidence_score"] = confidence
        if confidence >= settings.AUTO_APPROVE_THRESHOLD:
            status = "approved"
        else:
            status = "pending_approval"
        
        # Save to DB instead of returning directly
        content_record = await self.content_repo.create_content(
            title=f"Content for {platform} on {topic}",
            content_type=content_type,
            platform=platform,
            content_text=content.get("content_text", ""),
            variations=variations,
            campaign_id=campaign_id,
            confidence_score=confidence,
            status=status,
            tone=tone,
            target_audience=target_audience,
            ai_model_used="openrouter"
        )
        content["id"] = content_record.id
        content["status"] = status
        return content

    async def handle_follow_up_sequence(
        self, contact_id: int, context: str, sequence_type: str = "standard"
    ) -> List[Dict[str, Any]]:
        return await self.communication_manager.create_follow_up_sequence(
            contact_id=contact_id,
            context=context,
            sequence_type=sequence_type,
        )

    async def make_decision(self, decision_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return await self.decision_engine.evaluate_options(decision_type, context)

    async def override_agent_action(self, action_id: str, new_instructions: str) -> Dict[str, Any]:
        return {"status": "overridden", "action_id": action_id, "instructions": new_instructions}

    async def _get_pending_tasks(self) -> List[Dict[str, Any]]:
        return []

    async def _get_team_status(self) -> List[Dict[str, Any]]:
        return []

    async def _get_content_schedule(self) -> List[Dict[str, Any]]:
        return []

    async def _get_recent_activity(self) -> List[Dict[str, Any]]:
        return []

    async def _get_recent_decisions(self) -> List[Dict[str, Any]]:
        logs = await self.decision_repo.get_recent_decisions()
        return [{"id": log.id, "type": log.decision_type, "recommendation": log.ai_recommendation} for log in logs]

    async def _get_performance_metrics(self) -> Dict[str, Any]:
        return {}
