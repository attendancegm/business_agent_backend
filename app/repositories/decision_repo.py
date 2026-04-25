from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.decisions import DecisionLog


class DecisionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_decision_log(self, **kwargs) -> DecisionLog:
        log = DecisionLog(**kwargs)
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        return log

    async def get_recent_decisions(self, limit: int = 10) -> List[DecisionLog]:
        result = await self.session.execute(
            select(DecisionLog).order_by(DecisionLog.timestamp.desc()).limit(limit)
        )
        return list(result.scalars().all())
