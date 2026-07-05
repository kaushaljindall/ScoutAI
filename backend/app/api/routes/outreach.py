from fastapi import APIRouter, HTTPException
from typing import Any, List
from app.api.deps import CurrentUser
from app.schemas.outreach import MessageGenerationRequest, GenerateMessageResponse, MessageTemplateBase, MessageTemplateResponse
from app.core.config import settings
from app.services.ai.provider import GeminiProvider
from app.models.outreach import GeneratedMessage, MessageTemplate

router = APIRouter()

def get_ai_provider():
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Provider API key not configured")
    return GeminiProvider(api_key=settings.GEMINI_API_KEY)

@router.post("/generate-message/{business_id}", response_model=GenerateMessageResponse)
async def generate_message(business_id: str, request: MessageGenerationRequest, current_user: CurrentUser) -> Any:
    try:
        provider = get_ai_provider()
        from app.services.outreach.generator import OutreachService
        service = OutreachService(provider=provider)
        variations = service.generate_variations(business_id, request)
        return GenerateMessageResponse(business_id=business_id, variations=variations)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/regenerate/{business_id}", response_model=GenerateMessageResponse)
async def regenerate_message(business_id: str, request: MessageGenerationRequest, current_user: CurrentUser) -> Any:
    return await generate_message(business_id, request, current_user)

@router.get("/messages/{business_id}")
async def get_generated_messages(business_id: str, current_user: CurrentUser) -> Any:
    return await GeneratedMessage.find(
        GeneratedMessage.business_id == business_id,
        GeneratedMessage.is_deleted == False
    ).sort("-created_at").to_list()

@router.get("/templates", response_model=List[MessageTemplateResponse])
async def get_templates(current_user: CurrentUser):
    return await MessageTemplate.find(
        MessageTemplate.user_id == str(current_user.id),
        MessageTemplate.is_deleted == False
    ).to_list()

@router.post("/templates", response_model=MessageTemplateResponse)
async def create_template(template_in: MessageTemplateBase, current_user: CurrentUser):
    template = MessageTemplate(user_id=str(current_user.id), **template_in.model_dump())
    await template.insert()
    return template

@router.put("/templates/{id}", response_model=MessageTemplateResponse)
async def update_template(id: str, template_in: MessageTemplateBase, current_user: CurrentUser):
    template = await MessageTemplate.find_one(MessageTemplate.id == id, MessageTemplate.user_id == str(current_user.id))
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    for k, v in template_in.model_dump().items():
        setattr(template, k, v)
    await template.save()
    return template

@router.delete("/templates/{id}")
async def delete_template(id: str, current_user: CurrentUser):
    template = await MessageTemplate.find_one(MessageTemplate.id == id, MessageTemplate.user_id == str(current_user.id))
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    template.is_deleted = True
    await template.save()
    return {"status": "success"}
