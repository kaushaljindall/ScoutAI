from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from pydantic import Field, BaseModel
from beanie import Link
from enum import Enum

from app.models.base import BaseDocument

class ValidationStatus(str, Enum):
    PENDING = "Pending"
    VALIDATING = "Validating"
    COMPLETED = "Completed"
    FAILED = "Failed"

class DuplicateStatus(str, Enum):
    UNIQUE = "Unique"
    DUPLICATE = "Duplicate"
    MERGE_CANDIDATE = "Merge Candidate"

class ContactType(str, Enum):
    PHONE = "Phone"
    EMAIL = "Email"
    WEBSITE = "Website"

class ConfidenceScore(BaseModel):
    overall: float = 0.0
    business_name: float = 0.0
    phone: float = 0.0
    email: float = 0.0
    website: float = 0.0
    address: float = 0.0

class ValidationResultEmbedded(BaseModel):
    validation_type: str  # e.g., "email", "phone", "website", "duplicate"
    status: str  # "success", "failed", "error"
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CrawlerLogEmbedded(BaseModel):
    url: str
    crawler_used: str
    execution_time: Optional[float] = None
    status_code: Optional[int] = None
    success: bool = False
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BusinessContact(BaseModel):
    contact_type: ContactType
    value: str
    is_valid: bool = False
    validation_details: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WebsiteMetadata(BaseModel):
    url: str
    is_reachable: bool = False
    https_enabled: bool = False
    has_ssl: bool = False
    response_time: Optional[float] = None
    tech_stack: Optional[List[str]] = None
    has_booking_system: bool = False
    has_contact_form: bool = False
    last_crawled_at: Optional[datetime] = None

class BusinessSource(BaseModel):
    source_name: str
    source_url: Optional[str] = None
    extraction_time: Optional[datetime] = None
    confidence: Optional[float] = None
    raw_data: Optional[Dict[str, Any]] = None

class ValidatedBusiness(BaseDocument):
    """
    Validated Business record stored in MongoDB.
    This holds the aggregated, enriched, and validated data.
    """
    business_name: str = Field(index=True)
    description: Optional[str] = None
    services: Optional[List[str]] = None
    
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    social_links: Optional[Dict[str, str]] = None
    business_hours: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    logo_url: Optional[str] = None
    
    status: ValidationStatus = ValidationStatus.PENDING
    duplicate_status: DuplicateStatus = DuplicateStatus.UNIQUE
    
    contacts: List[BusinessContact] = Field(default_factory=list)
    website: Optional[WebsiteMetadata] = None
    sources: List[BusinessSource] = Field(default_factory=list)
    confidence: ConfidenceScore = Field(default_factory=ConfidenceScore)
    
    validation_results: List[ValidationResultEmbedded] = Field(default_factory=list)
    crawler_logs: List[CrawlerLogEmbedded] = Field(default_factory=list)

    class Settings:
        name = "validated_businesses"
        indexes = [
            "business_name",
            "status"
        ]
