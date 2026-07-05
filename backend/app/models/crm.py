from sqlalchemy import Column, String, Text, ForeignKey, JSON, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
from datetime import datetime

class Conversation(BaseModel):
    __tablename__ = "conversations"

    lead_id = Column(UUID(as_uuid=True), ForeignKey("saved_leads.id"), nullable=False, index=True)
    type = Column(String, nullable=False) # email, linkedin, whatsapp, meeting, call, note
    message = Column(Text, nullable=False)
    sender = Column(String, nullable=False) # user, lead, system

    lead = relationship("SavedLead", back_populates="conversations")
    analysis = relationship("AIConversationAnalysis", back_populates="conversation", uselist=False)

class AIConversationAnalysis(BaseModel):
    __tablename__ = "ai_conversation_analyses"

    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, unique=True, index=True)
    summary = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True)
    interest_level = Column(String, nullable=True)
    objections = Column(JSON, default=[])
    buying_intent = Column(String, nullable=True)
    next_action = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)

    conversation = relationship("Conversation", back_populates="analysis")

class Task(BaseModel):
    __tablename__ = "tasks"

    lead_id = Column(UUID(as_uuid=True), ForeignKey("saved_leads.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    type = Column(String, nullable=True) # call, email, meeting, custom

    lead = relationship("SavedLead", back_populates="tasks")

class TimelineEvent(BaseModel):
    __tablename__ = "timeline_events"

    lead_id = Column(UUID(as_uuid=True), ForeignKey("saved_leads.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)

    lead = relationship("SavedLead", back_populates="timeline_events")
