from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class DecisionRequest(BaseModel):
    decision_type: str
    context: Dict[str, Any]


class DecisionResponse(BaseModel):
    id: Optional[int] = None
    decision_type: str
    context: Dict[str, Any]
    requires_approval: bool
    impact: str = "unknown"
    confidence_score: Optional[float] = None
    ai_recommendation: Optional[str] = None


class PricingRequest(BaseModel):
    product_info: Dict[str, Any]
    market_data: Dict[str, Any]
    competitors: List[Dict[str, Any]]


class ClientPriorityRequest(BaseModel):
    client_name: str
    revenue_potential: int
    relationship_strength: int
    growth_opportunity: int
    strategic_value: int
    urgency: int
