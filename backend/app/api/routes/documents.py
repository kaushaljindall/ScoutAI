from fastapi import APIRouter, HTTPException
from typing import Any, List
from app.api.deps import CurrentUser
from app.schemas.documents import (
    DocumentCreate, DocumentUpdate, DocumentResponse,
    DocumentTemplateCreate, DocumentTemplateResponse,
    BrandingBase, BrandingResponse, GenerateDocumentRequest
)
from app.models.documents import Document, DocumentTemplate
from app.models.copilot import Branding
from app.core.config import settings

router = APIRouter()

@router.get("", response_model=List[DocumentResponse])
async def get_documents(current_user: CurrentUser):
    return await Document.find(
        Document.user_id == str(current_user.id),
        Document.is_deleted == False
    ).sort("-created_at").to_list()

@router.post("", response_model=DocumentResponse)
async def create_document(doc_in: DocumentCreate, current_user: CurrentUser):
    doc = Document(user_id=str(current_user.id), **doc_in.model_dump())
    await doc.insert()
    return doc

@router.get("/{id}", response_model=DocumentResponse)
async def get_document(id: str, current_user: CurrentUser):
    doc = await Document.find_one(Document.id == id, Document.user_id == str(current_user.id))
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.put("/{id}", response_model=DocumentResponse)
async def update_document(id: str, doc_in: DocumentUpdate, current_user: CurrentUser):
    doc = await Document.find_one(Document.id == id, Document.user_id == str(current_user.id))
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    for k, v in doc_in.model_dump(exclude_unset=True).items():
        setattr(doc, k, v)
    await doc.save()
    return doc

@router.delete("/{id}")
async def delete_document(id: str, current_user: CurrentUser):
    doc = await Document.find_one(Document.id == id, Document.user_id == str(current_user.id))
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.is_deleted = True
    await doc.save()
    return {"status": "success"}

@router.get("/branding/current", response_model=BrandingResponse)
async def get_branding(current_user: CurrentUser):
    branding = await Branding.find_one(Branding.user_id == str(current_user.id))
    if not branding:
        branding = Branding(user_id=str(current_user.id))
        await branding.insert()
    return branding

@router.put("/branding/current", response_model=BrandingResponse)
async def update_branding(brand_in: BrandingBase, current_user: CurrentUser):
    branding = await Branding.find_one(Branding.user_id == str(current_user.id))
    if not branding:
        branding = Branding(user_id=str(current_user.id))
    for k, v in brand_in.model_dump(exclude_unset=True).items():
        setattr(branding, k, v)
    await branding.save()
    return branding

@router.get("/templates/all", response_model=List[DocumentTemplateResponse])
async def get_templates(current_user: CurrentUser):
    return await DocumentTemplate.find(
        DocumentTemplate.user_id == str(current_user.id),
        DocumentTemplate.is_deleted == False
    ).to_list()
