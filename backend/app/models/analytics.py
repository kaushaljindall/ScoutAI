from sqlalchemy import Column, String, Text, ForeignKey, JSON, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.models.base import BaseModel

class Goal(BaseModel):
    __tablename__ = "goals"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False) # revenue, contacts, deals, follow_ups
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, default=0.0)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default="active") # active, completed, failed

    user = relationship("User")

class AnalyticsEvent(BaseModel):
    __tablename__ = "analytics_events"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False, index=True)
    event_data = Column(JSON, default={})

    user = relationship("User")

class Report(BaseModel):
    __tablename__ = "reports"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    type = Column(String, nullable=False) # weekly, monthly, quarterly
    insights = Column(JSON, nullable=False)
    date_range = Column(String, nullable=False)

    user = relationship("User")
