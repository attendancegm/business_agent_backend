from fastapi import APIRouter

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/status")
async def get_agents_status():
    return {"status": "running"}
