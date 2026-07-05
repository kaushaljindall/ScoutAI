from fastapi import APIRouter, HTTPException
from typing import Any, List
from app.api.deps import SessionDep, CurrentUser
from app.schemas.crm import (
    ConversationCreate, ConversationResponse,
    TaskCreate, TaskUpdate, TaskResponse,
    TimelineEventResponse, PipelineStatusUpdate,
    GenerateReplyRequest, GenerateReplyResponse
)
from app.core.config import settings
from app.services.ai.provider import GeminiProvider
from app.services.crm.manager import CRMService, ConversationService, TaskService
from app.services.crm.timeline import TimelineService
from app.services.crm.ai import AIConversationService, ReplyGenerationService

router = APIRouter()

def get_ai_provider():
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Provider API key not configured")
    return GeminiProvider(api_key=settings.GEMINI_API_KEY)

@router.post("/update-status/{lead_id}")
def update_status(lead_id: str, payload: PipelineStatusUpdate, db: SessionDep, current_user: CurrentUser):
    try:
        return CRMService.update_status(db, lead_id, payload.status, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/conversation/{lead_id}", response_model=ConversationResponse)
def add_conversation(lead_id: str, conv_in: ConversationCreate, db: SessionDep, current_user: CurrentUser):
    conv = ConversationService.add_conversation(db, lead_id, conv_in, current_user.id)
    
    # Auto-trigger AI Analysis
    ai_service = AIConversationService(get_ai_provider(), db)
    try:
        ai_service.analyze_conversation(str(conv.id))
    except Exception as e:
        pass # Non-blocking if AI fails
        
    db.refresh(conv)
    return conv

@router.get("/conversation/{lead_id}", response_model=List[ConversationResponse])
def get_conversations(lead_id: str, db: SessionDep, current_user: CurrentUser):
    return ConversationService.get_conversations(db, lead_id)

@router.post("/analyze-conversation/{conversation_id}")
def analyze_conversation(conversation_id: str, db: SessionDep, current_user: CurrentUser):
    ai_service = AIConversationService(get_ai_provider(), db)
    try:
        return ai_service.analyze_conversation(conversation_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-reply", response_model=GenerateReplyResponse)
def generate_reply(request: GenerateReplyRequest, current_user: CurrentUser):
    service = ReplyGenerationService(get_ai_provider())
    try:
        suggestions = service.generate_replies(request.context)
        return {
            "replies": suggestions.replies,
            "ai_suggestions": {
                "best_follow_up_date": suggestions.best_follow_up_date,
                "suggested_channel": suggestions.suggested_channel,
                "reason": suggestions.reason
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/task/{lead_id}", response_model=TaskResponse)
def create_task(lead_id: str, task_in: TaskCreate, db: SessionDep, current_user: CurrentUser):
    return TaskService.create_task(db, lead_id, task_in, current_user.id)

@router.put("/task/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_in: TaskUpdate, db: SessionDep, current_user: CurrentUser):
    try:
        return TaskService.update_task(db, task_id, task_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: SessionDep, current_user: CurrentUser, lead_id: str = None):
    return TaskService.get_tasks(db, current_user.id, lead_id)

@router.get("/timeline/{lead_id}", response_model=List[TimelineEventResponse])
def get_timeline(lead_id: str, db: SessionDep, current_user: CurrentUser):
    return TimelineService.get_timeline(db, lead_id)
