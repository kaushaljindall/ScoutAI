from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.models.base import BaseModel

class Business(BaseModel):
    __tablename__ = "businesses"

    business_name = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=True)
    website = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    instagram = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    facebook_url = Column(String, nullable=True)
    city = Column(String, index=True, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    google_rating = Column(Float, nullable=True)
    review_count = Column(Integer, default=0)
    
    # Enrichment fields
    website_status = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    last_checked = Column(DateTime, nullable=True)
    source = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)
    raw_data = Column(JSON, nullable=True)

    saved_leads = relationship("SavedLead", back_populates="business")

class SearchHistory(BaseModel):
    __tablename__ = "search_history"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    search_query = Column(String, index=True, nullable=False)
    filters = Column(JSON, default={})
    results_count = Column(Integer, default=0)
    execution_time = Column(Float, default=0.0)

    user = relationship("User")

class SavedLead(BaseModel):
    __tablename__ = "saved_leads"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False, index=True)
    status = Column(String, default="new")
    tags = Column(JSON, default=[])
    notes = Column(String, nullable=True)

    user = relationship("User")
    business = relationship("Business", back_populates="saved_leads")
