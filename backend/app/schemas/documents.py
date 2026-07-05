from pydantic import BaseModel, ConfigDict, BeforeValidator
from typing import List, Optional, Any, Dict, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class DocumentBase(BaseModel):
    title: str
    type: str
    content: str
    status: Optional[str] = "draft"
    version: Optional[int] = 1

class DocumentCreate(DocumentBase):
    lead_id: Optional[str] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    version: Optional[int] = None

class DocumentResponse(DocumentBase):
    id: PyObjectId
    user_id: PyObjectId
    lead_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class DocumentTemplateBase(BaseModel):
    name: str
    category: str
    content: str

class DocumentTemplateCreate(DocumentTemplateBase):
    pass

class DocumentTemplateResponse(DocumentTemplateBase):
    id: PyObjectId
    user_id: PyObjectId
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class BrandingBase(BaseModel):
    company_name: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    colors: Optional[dict] = None
    signature: Optional[str] = None

class BrandingResponse(BrandingBase):
    id: PyObjectId
    user_id: PyObjectId
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class GenerateDocumentRequest(BaseModel):
    lead_id: str
    type: str
    context: Optional[dict] = None
