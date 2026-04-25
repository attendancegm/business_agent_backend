import asyncio
import logging
from typing import Any, Dict, List

from app.services.content_pipeline import ContentPipeline
from app.services.openrouter_client import OpenRouterClient
from app.services.platform_connectors import PlatformConnector
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


async def get_trending_topics() -> List[str]:
    return ["business growth", "team productivity", "customer retention"]


async def get_content_for_current_timeslot() -> List[Dict[str, Any]]:
    return []


async def fetch_content_performance() -> List[Dict[str, Any]]:
    return []


async def store_performance_insights(analysis: Dict[str, Any]) -> None:
    logger.info("Stored performance insights: %s", analysis)


@celery_app.task(bind=True, max_retries=3)
def generate_daily_content(self):
    async def _generate():
        ai_client = OpenRouterClient()
        pipeline = ContentPipeline(ai_client)
        platforms = ["facebook", "instagram", "whatsapp"]
        topics = await get_trending_topics()
        content_list = []
        for platform in platforms:
            for topic in topics:
                content = await pipeline.create_content(
                    platform=platform,
                    topic=topic,
                    content_type="social_post",
                    tone="professional",
                    target_audience="general",
                )
                content_list.append(content)
        return content_list

    loop = asyncio.get_event_loop()
    content = loop.run_until_complete(_generate())
    return {"generated": len(content), "status": "success"}


@celery_app.task(bind=True)
def post_scheduled_content(self):
    async def _post():
        connector = PlatformConnector()
        scheduled_content = await get_content_for_current_timeslot()
        results = []
        for content in scheduled_content:
            try:
                if content["platform"] == "facebook":
                    result = await connector.post_to_facebook(content["content_text"], content.get("media_urls", []))
                elif content["platform"] == "instagram":
                    result = await connector.post_to_instagram(
                        content["content_text"], content.get("media_urls", [None])[0]
                    )
                elif content["platform"] == "whatsapp":
                    result = await connector.send_whatsapp(content["contact_id"], content["content_text"])
                else:
                    result = {"skipped": True}
                results.append({"content_id": content.get("id"), "status": "posted", "result": result})
            except Exception as exc:
                logger.error("Failed to post content %s: %s", content.get("id"), str(exc))
                results.append({"content_id": content.get("id"), "status": "failed", "error": str(exc)})
        return results

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_post())


@celery_app.task(bind=True)
def analyze_content_performance(self):
    async def _analyze():
        ai_client = OpenRouterClient()
        performance_data = await fetch_content_performance()
        analysis = await ai_client.analyze_content_performance(performance_data)
        await store_performance_insights(analysis)
        return analysis

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_analyze())
