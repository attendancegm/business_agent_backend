from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ContentCreate(BaseModel):
    platform: str
    topic: str
    content_type: str = "social_post"
    tone: str = "professional"
    target_audience: str = "general"


class ContentResponse(BaseModel):
    content_text: Optional[str] = None
    platform: str
    content_type: str
    tone: str
    target_audience: str
    status: Optional[str] = None
    confidence_score: Optional[float] = None
    variations: Optional[List[str]] = None
    created_at: Optional[str] = None


class ContentSchedule(BaseModel):
    content_id: int
    scheduled_time: datetime


class ContentApprove(BaseModel):
    action: str  # approve | reject | modify
    scheduled_time: Optional[datetime] = None
    modifications: Optional[Dict[str, Any]] = None
