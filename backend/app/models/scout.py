from typing import Optional, List
from datetime import datetime
from beanie import Indexed
from pydantic import Field
from app.models.base import BaseDocument


class Business(BaseDocument):
    business_name: Indexed(str)
    category: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    facebook_url: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    google_rating: Optional[float] = None
    review_count: int = 0
    website_status: Optional[str] = None
    logo_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    last_checked: Optional[datetime] = None
    source: Optional[str] = None
    confidence_score: Optional[float] = None
    raw_data: Optional[dict] = None

    class Settings:
        name = "businesses"


class BusinessAnalysis(BaseDocument):
    business_id: Indexed(str, unique=True)
    summary_short: Optional[str] = None
    summary_medium: Optional[str] = None
    summary_long: Optional[str] = None
    strengths: List[str] = []
    weaknesses: List[str] = []
    opportunities: List[str] = []
    opportunity_score: Optional[int] = None
    confidence_score: Optional[float] = None
    ai_tags: List[str] = []
    estimated_budget: Optional[str] = None
    recommended_services: List[str] = []

    class Settings:
        name = "business_analyses"


class SearchHistory(BaseDocument):
    user_id: Indexed(str)
    search_query: str
    filters: dict = {}
    results_count: int = 0
    execution_time: float = 0.0

    class Settings:
        name = "search_history"


class SavedLead(BaseDocument):
    user_id: Indexed(str)
    business_id: Indexed(str)
    status: str = "new"
    tags: List[str] = []
    notes: Optional[str] = None
    pipeline_stage: Optional[str] = None

    class Settings:
        name = "saved_leads"
