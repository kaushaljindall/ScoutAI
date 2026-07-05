from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class DiscoverRequest(BaseModel):
    query: str
    location: Optional[str] = None
    radius: Optional[int] = None
    max_results: int = 10
    filters: Optional[Dict[str, Any]] = None

class DiscoverResponse(BaseModel):
    status: str
    businesses_discovered: int
    execution_time: float

class ValidateBusinessRequest(BaseModel):
    business_id: str
