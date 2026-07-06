from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class ValidationRequest(BaseModel):
    businesses: List[Dict[str, Any]] = Field(description="List of raw businesses from discovery engine")

class ValidationStatusResponse(BaseModel):
    id: UUID
    business_name: str
    status: str
    progress: str = ""

class BusinessValidationResponse(BaseModel):
    id: UUID
    business_name: str
    status: str
    duplicate_status: str
    overall_confidence: float
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
