from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    type: str
    content: str
    status: Optional[str] = "draft"
    version: Optional[int] = 1

class DocumentCreate(DocumentBase):
    lead_id: Optional[UUID] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    version: Optional[int] = None

class DocumentResponse(DocumentBase):
    id: UUID
    user_id: UUID
    lead_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class DocumentTemplateBase(BaseModel):
    name: str
    category: str
    content: str

class DocumentTemplateCreate(DocumentTemplateBase):
    pass

class DocumentTemplateResponse(DocumentTemplateBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class BrandingBase(BaseModel):
    company_name: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    colors: Optional[dict] = None
    signature: Optional[str] = None

class BrandingResponse(BrandingBase):
    id: UUID
    user_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class GenerateDocumentRequest(BaseModel):
    lead_id: UUID
    type: str # proposal, quotation, scope, contract, meeting
    context: Optional[dict] = None
