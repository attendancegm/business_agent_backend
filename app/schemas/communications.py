from typing import Optional

from pydantic import BaseModel


class FollowUpRequest(BaseModel):
    contact_id: int
    context: str
    sequence_type: str = "standard"


class MessageResponse(BaseModel):
    status: str
    message: Optional[str] = None


class MeetingRequest(BaseModel):
    meeting_id: int
