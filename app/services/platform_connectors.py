from typing import Any, Dict, List, Optional


class PlatformConnector:
    """Minimal platform connector placeholder."""

    async def post_to_facebook(self, text: str, media_urls: List[str]) -> Dict[str, Any]:
        return {"platform": "facebook", "posted": True, "text": text, "media_urls": media_urls}

    async def post_to_instagram(self, text: str, media_url: Optional[str]) -> Dict[str, Any]:
        return {"platform": "instagram", "posted": True, "text": text, "media_url": media_url}

    async def send_whatsapp(self, contact_id: int, text: str) -> Dict[str, Any]:
        return {"platform": "whatsapp", "sent": True, "contact_id": contact_id, "text": text}
