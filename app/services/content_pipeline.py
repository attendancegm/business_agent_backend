import json
from datetime import datetime
from typing import Any, Dict

from app.services.openrouter_client import OpenRouterClient


class ContentPipeline:
    """Handles the content lifecycle from creation to optimization."""

    def __init__(self, ai_client: OpenRouterClient):
        self.ai_client = ai_client

    async def create_content(
        self,
        platform: str,
        topic: str,
        content_type: str,
        tone: str,
        target_audience: str,
    ) -> Dict[str, Any]:
        platform_rules = self._get_platform_rules(platform)
        system_prompt = f"""You are a professional content creator specialized in {platform}.
Platform Guidelines:
{json.dumps(platform_rules, indent=2)}
Return content as JSON."""
        result = await self.ai_client.complete(
            system_prompt=system_prompt,
            user_message=f"Create {content_type} about: {topic}",
            temperature=0.8,
            response_format="json",
        )
        content = json.loads(result["content"])
        content["platform"] = platform
        content["content_type"] = content_type
        content["tone"] = tone
        content["target_audience"] = target_audience
        content["created_at"] = datetime.utcnow().isoformat()
        content["ai_model"] = result["model"]
        return content

    def _get_platform_rules(self, platform: str) -> Dict[str, Any]:
        rules = {
            "whatsapp": {"max_length": 1000, "best_format": "conversational"},
            "facebook": {"max_length": 63206, "best_format": "storytelling"},
            "instagram": {"max_length": 2200, "best_format": "visual-first"},
        }
        return rules.get(platform, rules["facebook"])

    async def evaluate_content(self, content: Dict[str, Any]) -> float:
        result = await self.ai_client.complete(
            system_prompt="Score this content from 0 to 1 and return only the number.",
            user_message=json.dumps(content),
            temperature=0.1,
        )
        try:
            return float(result["content"])
        except Exception:
            return 0.7

    async def optimize_content(self, content: Dict[str, Any], performance_data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.ai_client.complete(
            system_prompt="Optimize content based on performance and return JSON.",
            user_message=json.dumps({"content": content, "performance": performance_data}),
            response_format="json",
        )
        return json.loads(result["content"])
