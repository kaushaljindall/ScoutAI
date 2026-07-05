from pydantic import BaseModel, ConfigDict, BeforeValidator
from typing import Optional, List, Dict, Any, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class BusinessBase(BaseModel):
    business_name: str
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
    raw_data: Optional[Dict[str, Any]] = None

class BusinessResponse(BusinessBase):
    id: PyObjectId
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class SavedLeadBase(BaseModel):
    business_id: str
    status: str = "new"
    tags: List[str] = []
    notes: Optional[str] = None

class SavedLeadCreate(SavedLeadBase):
    pass

class SavedLeadResponse(SavedLeadBase):
    id: PyObjectId
    user_id: PyObjectId
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class PaginatedBusinesses(BaseModel):
    items: List[BusinessResponse]
    total: int
    page: int
    size: int
    pages: int
