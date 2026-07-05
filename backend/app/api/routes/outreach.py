from fastapi import APIRouter, HTTPException
from typing import Any, List
from app.api.deps import SessionDep, CurrentUser
from app.schemas.outreach import MessageGenerationRequest, GenerateMessageResponse, MessageTemplateBase, MessageTemplateResponse
from app.core.config import settings
from app.services.ai.provider import GeminiProvider
from app.services.outreach.generator import OutreachService
from app.services.outreach.template import TemplateService
from app.models.outreach import GeneratedMessage

router = APIRouter()

def get_outreach_service(db: SessionDep) -> OutreachService:
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Provider API key not configured")
    provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
    return OutreachService(provider=provider, db=db)

@router.post("/generate-message/{business_id}", response_model=GenerateMessageResponse)
def generate_message(
    business_id: str,
    request: MessageGenerationRequest,
    db: SessionDep,
    current_user: CurrentUser,
) -> Any:
    service = get_outreach_service(db)
    try:
        variations = service.generate_variations(business_id, request)
        return GenerateMessageResponse(business_id=business_id, variations=variations)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/regenerate/{business_id}", response_model=GenerateMessageResponse)
def regenerate_message(
    business_id: str,
    request: MessageGenerationRequest,
    db: SessionDep,
    current_user: CurrentUser,
) -> Any:
    return generate_message(business_id, request, db, current_user)

@router.get("/messages/{business_id}")
def get_generated_messages(
    business_id: str,
    db: SessionDep,
    current_user: CurrentUser,
) -> Any:
    messages = db.query(GeneratedMessage).filter(GeneratedMessage.business_id == business_id).order_by(GeneratedMessage.created_at.desc()).all()
    return messages

# Template Endpoints
@router.get("/templates", response_model=List[MessageTemplateResponse])
def get_templates(db: SessionDep, current_user: CurrentUser):
    return TemplateService(db).get_templates(current_user.id)

@router.post("/templates", response_model=MessageTemplateResponse)
def create_template(template_in: MessageTemplateBase, db: SessionDep, current_user: CurrentUser):
    return TemplateService(db).create_template(current_user.id, template_in)

@router.put("/templates/{id}", response_model=MessageTemplateResponse)
def update_template(id: str, template_in: MessageTemplateBase, db: SessionDep, current_user: CurrentUser):
    try:
        return TemplateService(db).update_template(id, current_user.id, template_in)
    except ValueError:
        raise HTTPException(status_code=404, detail="Template not found")

@router.delete("/templates/{id}")
def delete_template(id: str, db: SessionDep, current_user: CurrentUser):
    try:
        TemplateService(db).delete_template(id, current_user.id)
        return {"status": "success"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Template not found")
