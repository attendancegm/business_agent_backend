from fastapi import APIRouter

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.get("/pending")
async def get_pending_approvals():
    return {"pending": []}
