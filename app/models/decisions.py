from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, Integer, String, Text

from app.db.session import Base


class DecisionLog(Base):
    __tablename__ = "decision_logs"

    id = Column(Integer, primary_key=True, index=True)
    decision_type = Column(String(100))
    context = Column(JSON)
    options_considered = Column(JSON)
    ai_recommendation = Column(Text)
    confidence_score = Column(Float)
    reasoning = Column(Text)
    your_decision = Column(Text, nullable=True)
    override_reason = Column(Text, nullable=True)
    implemented = Column(Boolean, default=False)
    outcome_metrics = Column(JSON)
    success_rating = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)


class PricingAnalysis(Base):
    __tablename__ = "pricing_analyses"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(200))
    market_segment = Column(String(200))
    competitor_prices = Column(JSON)
    value_proposition = Column(Text)
    costs = Column(JSON)
    recommended_price = Column(Float)
    price_range = Column(JSON)
    pricing_model = Column(String(100))
    confidence_interval = Column(JSON)
    reasoning = Column(Text)
    final_price = Column(Float, nullable=True)
    adjusted_by = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)


class ClientPriority(Base):
    __tablename__ = "client_priorities"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(200))
    revenue_potential = Column(Integer)
    relationship_strength = Column(Integer)
    growth_opportunity = Column(Integer)
    strategic_value = Column(Integer)
    urgency = Column(Integer)
    overall_score = Column(Float)
    recommended_action = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
