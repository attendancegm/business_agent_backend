import json
import logging
from typing import Any, Dict, List, Optional

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenRouterClient:
    """Production OpenRouter API client with retries and error handling."""

    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.client = httpx.AsyncClient(
            timeout=settings.AGENT_TIMEOUT_SECONDS,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "https://your-business-agent.com",
                "X-Title": "Business Agent System",
                "Content-Type": "application/json",
            },
        )

    @retry(
        stop=stop_after_attempt(settings.AGENT_MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    async def complete(
        self,
        system_prompt: str,
        user_message: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        response_format: Optional[str] = None,
    ) -> Dict[str, Any]:
        if model is None:
            model = settings.OPENROUTER_DEFAULT_MODEL

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 0.9,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1,
        }

        if response_format == "json":
            payload["response_format"] = {"type": "json_object"}

        response = await self.client.post(f"{self.base_url}/chat/completions", json=payload)
        if response.status_code == 200:
            data = response.json()
            usage = data.get("usage", {})
            logger.info("Tokens used: %s", usage.get("total_tokens", 0))
            return {
                "content": data["choices"][0]["message"]["content"],
                "model": data.get("model", model),
                "usage": usage,
                "finish_reason": data["choices"][0].get("finish_reason"),
            }
        if response.status_code == 429:
            raise Exception("Rate limit exceeded")
        raise Exception(f"API error: {response.status_code} - {response.text}")

    async def generate_content_variations(
        self, base_content: str, platform: str, num_variations: int = 3
    ) -> List[str]:
        system_prompt = f"""You are a content optimization expert for {platform}.
Generate {num_variations} variations of the provided content.
Return as JSON array of strings."""

        result = await self.complete(
            system_prompt=system_prompt,
            user_message=f"Base content:\n{base_content}",
            temperature=0.8,
            response_format="json",
        )
        variations = json.loads(result["content"])
        return variations if isinstance(variations, list) else [variations]

    async def analyze_content_performance(self, content_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        result = await self.complete(
            system_prompt="Analyze content performance and return JSON recommendations.",
            user_message=json.dumps(content_data),
            temperature=0.3,
            response_format="json",
        )
        return json.loads(result["content"])
