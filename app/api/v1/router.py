from fastapi import APIRouter

from app.api.v1.admin.routes import router as admin_router
from app.api.v1.agents.routes import router as agents_router
from app.api.v1.approvals.routes import router as approvals_router
from app.api.v1.communications.routes import router as communications_router
from app.api.v1.content.routes import router as content_router
from app.api.v1.dashboard.routes import router as dashboard_router
from app.api.v1.decisions.routes import router as decisions_router

api_router = APIRouter()
api_router.include_router(agents_router)
api_router.include_router(content_router)
api_router.include_router(communications_router)
api_router.include_router(decisions_router)
api_router.include_router(approvals_router)
api_router.include_router(dashboard_router)
api_router.include_router(admin_router)
