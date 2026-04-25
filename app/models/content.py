from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.session import Base


class ContentStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    REJECTED = "rejected"


class Platform(str, Enum):
    WHATSAPP = "whatsapp"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"


class ContentType(str, Enum):
    SOCIAL_POST = "social_post"
    STORY = "story"
    REEL = "reel"
    CAROUSEL = "carousel"
    NEWSLETTER = "newsletter"
    AD_COPY = "ad_copy"


class ContentLibrary(Base):
    __tablename__ = "content_library"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content_type = Column(SQLEnum(ContentType), nullable=False)
    platform = Column(SQLEnum(Platform), nullable=False)
    content_text = Column(Text, nullable=False)
    variations = Column(JSON, default=list)
    media_urls = Column(JSON, default=list)
    hashtags = Column(JSON, default=list)
    call_to_action = Column(String(500))
    tone = Column(String(50))
    target_audience = Column(String(200))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    status = Column(SQLEnum(ContentStatus), default=ContentStatus.DRAFT)
    scheduled_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    ai_model_used = Column(String(100))
    generation_prompt = Column(Text)
    confidence_score = Column(Float)
    impressions = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    version = Column(Integer, default=1)
    parent_content_id = Column(Integer, ForeignKey("content_library.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    is_archived = Column(Boolean, default=False)

    approval_history = relationship("ApprovalHistory", back_populates="content")
    campaign = relationship("Campaign", back_populates="contents")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    goals = Column(JSON)
    budget = Column(Float)
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    contents = relationship("ContentLibrary", back_populates="campaign")


class ApprovalHistory(Base):
    __tablename__ = "approval_history"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content_library.id"))
    approved_by = Column(String(100))
    status = Column(String(50))
    feedback = Column(Text)
    changes_made = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

    content = relationship("ContentLibrary", back_populates="approval_history")
