import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import Base, async_engine
from app.db.session import AsyncSessionLocal
from app.models import communications, content, decisions  # noqa: F401
from app.services.agent_orchestrator import AgentOrchestrator
from app.tasks.celery_app import celery_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Business Agent System...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    celery_app.conf.beat_schedule = {
        "content-posting-morning": {"task": "app.tasks.content_tasks.post_scheduled_content", "schedule": "09:00"}
    }
    yield
    logger.info("Shutting down...")
    await async_engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production AI Agent System for Business Operations",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass


manager = ConnectionManager()


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION, "timestamp": datetime.utcnow().isoformat()}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("action") == "override":
                async with AsyncSessionLocal() as session:
                    agent_orchestrator = AgentOrchestrator(session)
                    result = await agent_orchestrator.override_agent_action(
                        action_id=data.get("action_id", "manual_ws"),
                        new_instructions=data.get("instructions", ""),
                    )
                    await websocket.send_json(result)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error("Global exception: %s", str(exc))
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
