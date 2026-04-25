from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.content import ContentLibrary, ContentStatus


class ContentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_content(self, **kwargs) -> ContentLibrary:
        content = ContentLibrary(**kwargs)
        self.session.add(content)
        await self.session.commit()
        await self.session.refresh(content)
        return content

    async def get_pending_approvals(self) -> List[ContentLibrary]:
        result = await self.session.execute(
            select(ContentLibrary).where(ContentLibrary.status == ContentStatus.PENDING_APPROVAL)
        )
        return list(result.scalars().all())

    async def get_scheduled_content(self) -> List[ContentLibrary]:
        result = await self.session.execute(
            select(ContentLibrary).where(ContentLibrary.status == ContentStatus.SCHEDULED)
        )
        return list(result.scalars().all())
