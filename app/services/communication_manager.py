from datetime import datetime, timedelta
from typing import Any, Dict, List

from app.repositories.communication_repo import CommunicationRepository
from app.services.openrouter_client import OpenRouterClient


class CommunicationManager:
    """Handles follow-ups, reminders, and lightweight team communication workflows."""

    def __init__(self, ai_client: OpenRouterClient, repo: CommunicationRepository):
        self.ai_client = ai_client
        self.repo = repo

    async def create_follow_up_sequence(
        self, contact_id: int, context: str, sequence_type: str = "standard"
    ) -> List[Dict[str, Any]]:
        if sequence_type == "aggressive":
            offsets = [0, 2, 5]
        elif sequence_type == "gentle":
            offsets = [0, 5, 10]
        else:
            offsets = [0, 3, 7]

        base = datetime.utcnow()
        messages = []
        for index, day_offset in enumerate(offsets, start=1):
            scheduled_for = base + timedelta(days=day_offset)
            msg = await self.repo.create_message(
                contact_id=contact_id,
                message_type=f"follow_up_step_{index}",
                generation_context={"sequence_type": sequence_type, "context": context},
                status="scheduled",
                sent_at=scheduled_for,
            )
            messages.append(
                {
                    "id": msg.id,
                    "contact_id": msg.contact_id,
                    "step": index,
                    "sequence_type": sequence_type,
                    "scheduled_for": scheduled_for.isoformat(),
                    "status": msg.status,
                }
            )
        return messages

    async def create_meeting_reminder(self, contact_id: int, meeting_id: int) -> Dict[str, Any]:
        msg = await self.repo.create_message(
            contact_id=contact_id,
            message_type="meeting_reminder",
            generation_context={"meeting_id": meeting_id},
            status="queued",
        )
        return {
            "message_id": msg.id,
            "meeting_id": meeting_id,
            "message": "Reminder prepared and queued for delivery.",
            "created_at": datetime.utcnow().isoformat(),
        }

    async def get_team_progress(self) -> List[Dict[str, Any]]:
        members = await self.repo.get_team_members()
        if not members:
            return [{"team_member": "unassigned", "tasks_completed": 0, "blockers": []}]
        return [
            {
                "team_member": m.name,
                "tasks_completed": m.tasks_completed_this_week,
                "blockers": m.blockers,
            }
            for m in members
        ]

    async def bulk_follow_up(self, contact_ids: List[int], context: str) -> Dict[str, Any]:
        items = []
        for contact_id in contact_ids:
            msg = await self.repo.create_message(
                contact_id=contact_id,
                message_type="bulk_follow_up",
                generation_context={"context": context},
                status="queued",
            )
            items.append(
                {
                    "message_id": msg.id,
                    "contact_id": contact_id,
                    "status": "queued",
                    "queued_at": datetime.utcnow().isoformat(),
                }
            )
        return {"total": len(contact_ids), "items": items}

    async def create_onboarding_sequence(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "user_data": user_data,
            "steps": ["welcome", "setup", "first-value", "follow-up"],
            "created_at": datetime.utcnow().isoformat(),
        }
