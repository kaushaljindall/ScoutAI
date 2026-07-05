from fastapi import APIRouter, HTTPException
from typing import Any, List
from app.api.deps import SessionDep, CurrentUser
from app.schemas.documents import (
    DocumentCreate, DocumentUpdate, DocumentResponse,
    DocumentTemplateCreate, DocumentTemplateResponse,
    BrandingBase, BrandingResponse, GenerateDocumentRequest
)
from app.core.config import settings
from app.services.ai.provider import GeminiProvider
from app.services.documents.manager import DocumentService, TemplateService, BrandingService
from app.services.documents.generator import DocumentGenerator

router = APIRouter()

def get_generator(db: SessionDep):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Provider API key not configured")
    provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
    return DocumentGenerator(provider=provider, db=db)

# --- Generator Endpoints ---
@router.post("/generate", response_model=DocumentResponse)
def generate_document(req: GenerateDocumentRequest, db: SessionDep, current_user: CurrentUser):
    gen = get_generator(db)
    try:
        output = gen.generate(str(current_user.id), str(req.lead_id), req.type, req.context)
        
        # Save generated document as draft
        doc_in = DocumentCreate(
            lead_id=req.lead_id,
            title=output.title,
            type=req.type,
            content=output.content,
            status="draft"
        )
        return DocumentService.create_document(db, current_user.id, doc_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Document CRUD ---
@router.get("", response_model=List[DocumentResponse])
def get_documents(db: SessionDep, current_user: CurrentUser):
    return DocumentService.get_documents(db, current_user.id)

@router.get("/{id}", response_model=DocumentResponse)
def get_document(id: str, db: SessionDep, current_user: CurrentUser):
    doc = DocumentService.get_document(db, id, current_user.id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.put("/{id}", response_model=DocumentResponse)
def update_document(id: str, doc_in: DocumentUpdate, db: SessionDep, current_user: CurrentUser):
    try:
        return DocumentService.update_document(db, id, current_user.id, doc_in)
    except ValueError:
        raise HTTPException(status_code=404, detail="Document not found")

@router.delete("/{id}")
def delete_document(id: str, db: SessionDep, current_user: CurrentUser):
    try:
        DocumentService.delete_document(db, id, current_user.id)
        return {"status": "success"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Document not found")

# --- Branding ---
@router.get("/branding/current", response_model=BrandingResponse)
def get_branding(db: SessionDep, current_user: CurrentUser):
    return BrandingService.get_branding(db, current_user.id)

@router.put("/branding/current", response_model=BrandingResponse)
def update_branding(brand_in: BrandingBase, db: SessionDep, current_user: CurrentUser):
    return BrandingService.update_branding(db, current_user.id, brand_in)

# --- Templates ---
@router.get("/templates/all", response_model=List[DocumentTemplateResponse])
def get_templates(db: SessionDep, current_user: CurrentUser):
    return TemplateService.get_templates(db, current_user.id)
