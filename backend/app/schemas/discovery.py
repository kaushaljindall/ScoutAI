"""Pydantic schemas for the Discovery API (Phase 5B)."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


# Keep original schema for compatibility
class ValidateBusinessRequest(BaseModel):
    business_id: str


class DiscoverRequest(BaseModel):
    query: str = Field(..., example="Find dentists in Chandigarh")
    location: Optional[str] = Field(None, example="Chandigarh")
    max_results_per_provider: Optional[int] = Field(None, ge=1, le=50)


class DiscoveredBusinessSchema(BaseModel):
    id: str
    business_name: str
    category: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    google_rating: Optional[float] = None
    review_count: Optional[int] = None
    provider: str
    source_url: Optional[str] = None
    provider_confidence: float
    discovered_at: datetime

    model_config = {"from_attributes": True}


class ProviderStatus(BaseModel):
    name: str
    display_name: str
    status: str   # pending | running | completed | failed
    count: Optional[int] = 0
    duration: Optional[float] = None
    error: Optional[str] = None


class ProviderHealthStatus(BaseModel):
    name: str
    display_name: str
    priority: int
    is_healthy: bool
    requires_key: bool
    key_configured: bool
