from fastapi import APIRouter, HTTPException
from typing import Any, List
from app.api.deps import CurrentUser
from app.schemas.copilot import (
    CopilotChatRequest, CopilotChatResponse, AIChatResponse,
    UserPreferenceBase, UserPreferenceResponse
)
from app.core.config import settings
from app.services.ai.provider import GeminiProvider
from app.models.copilot import AIChat, AIMessage, UserPreferences

router = APIRouter()

def get_ai_provider():
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Provider API key not configured")
    return GeminiProvider(api_key=settings.GEMINI_API_KEY)

@router.post("/chat", response_model=CopilotChatResponse)
async def chat(request: CopilotChatRequest, current_user: CurrentUser):
    try:
        provider = get_ai_provider()
        from app.services.copilot.engine import ContextEngine
        engine = ContextEngine(provider=provider)
        return await engine.process_chat(str(current_user.id), request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[AIChatResponse])
async def get_chat_history(current_user: CurrentUser):
    chats = await AIChat.find(
        AIChat.user_id == str(current_user.id),
        AIChat.is_deleted == False
    ).sort("-created_at").to_list()
    return chats

@router.get("/preferences", response_model=UserPreferenceResponse)
async def get_preferences(current_user: CurrentUser):
    prefs = await UserPreferences.find_one(UserPreferences.user_id == str(current_user.id))
    if not prefs:
        prefs = UserPreferences(user_id=str(current_user.id))
        await prefs.insert()
    return prefs

@router.put("/preferences", response_model=UserPreferenceResponse)
async def update_preferences(prefs_in: UserPreferenceBase, current_user: CurrentUser):
    prefs = await UserPreferences.find_one(UserPreferences.user_id == str(current_user.id))
    if not prefs:
        prefs = UserPreferences(user_id=str(current_user.id))
    for k, v in prefs_in.model_dump(exclude_unset=True).items():
        setattr(prefs, k, v)
    await prefs.save()
    return prefs
