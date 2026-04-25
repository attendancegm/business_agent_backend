import asyncio

from app.db.session import Base, async_engine
from app.models import communications, content, decisions  # noqa: F401


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
