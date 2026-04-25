from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.communications import Contact, Meeting, Message, TeamMember


class CommunicationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_message(self, **kwargs) -> Message:
        message = Message(**kwargs)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def create_meeting(self, **kwargs) -> Meeting:
        meeting = Meeting(**kwargs)
        self.session.add(meeting)
        await self.session.commit()
        await self.session.refresh(meeting)
        return meeting

    async def get_team_members(self) -> List[TeamMember]:
        result = await self.session.execute(select(TeamMember))
        return list(result.scalars().all())
