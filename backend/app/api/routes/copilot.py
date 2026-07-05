from fastapi import APIRouter, HTTPException
from typing import Any, List
from app.api.deps import SessionDep, CurrentUser
from app.schemas.copilot import (
    CopilotChatRequest, CopilotChatResponse, AIChatResponse,
    UserPreferenceBase, UserPreferenceResponse
)
from app.core.config import settings
from app.services.ai.provider import GeminiProvider
from app.services.copilot.engine import ContextEngine
from app.services.copilot.manager import ChatRepository, PreferenceService

router = APIRouter()

def get_engine(db: SessionDep):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Provider API key not configured")
    provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
    return ContextEngine(provider=provider, db=db)

@router.post("/chat", response_model=CopilotChatResponse)
def chat(request: CopilotChatRequest, db: SessionDep, current_user: CurrentUser):
    engine = get_engine(db)
    try:
        return engine.process_chat(current_user.id, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[AIChatResponse])
def get_chat_history(db: SessionDep, current_user: CurrentUser):
    repo = ChatRepository(db)
    return repo.get_user_chats(current_user.id)

@router.get("/preferences", response_model=UserPreferenceResponse)
def get_preferences(db: SessionDep, current_user: CurrentUser):
    service = PreferenceService(db)
    return service.get_preferences(current_user.id)

@router.put("/preferences", response_model=UserPreferenceResponse)
def update_preferences(prefs: UserPreferenceBase, db: SessionDep, current_user: CurrentUser):
    service = PreferenceService(db)
    return service.update_preferences(current_user.id, prefs)
