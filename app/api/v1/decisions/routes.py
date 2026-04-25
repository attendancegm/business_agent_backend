from typing import List

from fastapi import APIRouter, Depends

from app.api.deps import get_agent_orchestrator
from app.schemas.decisions import (
    ClientPriorityRequest,
    DecisionRequest,
    DecisionResponse,
    PricingRequest,
)
from app.services.agent_orchestrator import AgentOrchestrator

router = APIRouter(prefix="/decisions", tags=["decisions"])


@router.post("/analyze", response_model=DecisionResponse)
async def analyze_decision(
    request: DecisionRequest, agent: AgentOrchestrator = Depends(get_agent_orchestrator)
):
    result = await agent.make_decision(decision_type=request.decision_type, context=request.context)
    return DecisionResponse(**result)


@router.post("/pricing")
async def analyze_pricing(request: PricingRequest):
    return {"pricing_analysis": {"product": request.product_info, "market_data": request.market_data}}


@router.post("/client-priority")
async def prioritize_clients(clients: List[ClientPriorityRequest]):
    return {"prioritized_clients": [c.model_dump() for c in clients]}


@router.post("/feature-priority")
async def prioritize_features(features: List[str], business_goals: str, resources: dict):
    return {"feature_priorities": {"features": features, "business_goals": business_goals, "resources": resources}}
