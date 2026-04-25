import json
import logging
from typing import Any, Dict

from app.repositories.decision_repo import DecisionRepository
from app.services.openrouter_client import OpenRouterClient

logger = logging.getLogger(__name__)


class DecisionEngine:
    def __init__(self, ai_client: OpenRouterClient, repo: DecisionRepository):
        self.ai_client = ai_client
        self.repo = repo

    async def evaluate_options(self, decision_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.ai_client.complete(
            system_prompt="Evaluate the context and provide a recommended decision. Output JSON.",
            user_message=f"Type: {decision_type}\nContext: {json.dumps(context)}",
            response_format="json",
        )
        try:
            decision_data = json.loads(result["content"])
        except Exception as e:
            logger.error(f"Failed to parse decision: {e}")
            decision_data = {"recommendation": "unknown", "confidence": 0.0}

        log = await self.repo.create_decision_log(
            decision_type=decision_type,
            context=context,
            ai_recommendation=decision_data.get("recommendation", ""),
            confidence_score=decision_data.get("confidence", 0.0),
        )

        return {
            "id": log.id,
            "decision_type": log.decision_type,
            "context": log.context,
            "ai_recommendation": log.ai_recommendation,
            "confidence_score": log.confidence_score,
            "requires_approval": log.confidence_score < 0.8,
        }
