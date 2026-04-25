from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    company = Column(String(200))
    role = Column(String(100))
    whatsapp_number = Column(String(50))
    facebook_id = Column(String(100))
    instagram_handle = Column(String(100))
    priority = Column(Integer, default=3)
    relationship_strength = Column(Integer, default=1)
    last_contacted = Column(DateTime)
    next_scheduled_contact = Column(DateTime)
    tags = Column(JSON, default=list)
    custom_fields = Column(JSON, default=dict)
    total_interactions = Column(Integer, default=0)
    conversion_status = Column(String(50))
    lifetime_value = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Message", back_populates="contact")
    meetings = relationship("Meeting", back_populates="contact")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    platform = Column(String(50))
    message_type = Column(String(50))
    content = Column(Text)
    ai_generated = Column(Boolean, default=True)
    generation_context = Column(JSON)
    template_used = Column(String(100))
    status = Column(String(50))
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    read_at = Column(DateTime)
    replied_at = Column(DateTime)
    response_rate = Column(Float)
    sentiment_score = Column(Float)

    contact = relationship("Contact", back_populates="messages")


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    title = Column(String(255))
    description = Column(Text)
    meeting_type = Column(String(50))
    scheduled_at = Column(DateTime)
    duration_minutes = Column(Integer)
    agenda = Column(Text)
    preparation_notes = Column(Text)
    follow_up_template = Column(Text)
    status = Column(String(50))
    notes = Column(Text)
    action_items = Column(JSON)

    contact = relationship("Contact", back_populates="meetings")


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    role = Column(String(100))
    email = Column(String(255))
    current_tasks = Column(JSON, default=list)
    workload_percentage = Column(Integer, default=0)
    last_check_in = Column(DateTime)
    next_check_in = Column(DateTime)
    check_in_frequency = Column(String(50))
    tasks_completed_this_week = Column(Integer, default=0)
    blockers = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
