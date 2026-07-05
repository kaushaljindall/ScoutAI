from fastapi import APIRouter, HTTPException
from typing import Any, List, Optional
from app.api.deps import CurrentUser
from app.models.crm import Conversation, Task, TimelineEvent, AIConversationAnalysis
from app.schemas.crm import (
    ConversationCreate, ConversationResponse,
    TaskCreate, TaskUpdate, TaskResponse,
    TimelineEventResponse, PipelineStatusUpdate,
    GenerateReplyRequest, GenerateReplyResponse
)
from app.models.scout import SavedLead
from app.core.config import settings
from app.services.ai.provider import GeminiProvider

router = APIRouter()

def get_ai_provider():
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Provider API key not configured")
    return GeminiProvider(api_key=settings.GEMINI_API_KEY)

@router.post("/update-status/{lead_id}")
async def update_status(lead_id: str, payload: PipelineStatusUpdate, current_user: CurrentUser):
    lead = await SavedLead.find_one(SavedLead.id == lead_id, SavedLead.user_id == str(current_user.id))
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = payload.status
    await lead.save()
    return {"status": "updated", "lead_id": lead_id, "new_status": payload.status}

@router.post("/conversation/{lead_id}", response_model=ConversationResponse)
async def add_conversation(lead_id: str, conv_in: ConversationCreate, current_user: CurrentUser):
    conv = Conversation(
        lead_id=lead_id,
        type=conv_in.type,
        message=conv_in.message,
        sender=conv_in.sender
    )
    await conv.insert()

    # Timeline event
    event = TimelineEvent(
        lead_id=lead_id,
        event_type="conversation_added",
        description=f"New {conv_in.type} message logged"
    )
    await event.insert()
    return conv

@router.get("/conversation/{lead_id}", response_model=List[ConversationResponse])
async def get_conversations(lead_id: str, current_user: CurrentUser):
    return await Conversation.find(
        Conversation.lead_id == lead_id,
        Conversation.is_deleted == False
    ).sort("created_at").to_list()

@router.post("/task/{lead_id}", response_model=TaskResponse)
async def create_task(lead_id: str, task_in: TaskCreate, current_user: CurrentUser):
    task = Task(
        lead_id=lead_id,
        title=task_in.title,
        due_date=task_in.due_date,
        type=task_in.type
    )
    await task.insert()
    return task

@router.put("/task/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_in: TaskUpdate, current_user: CurrentUser):
    task = await Task.find_one(Task.id == task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_in.title is not None:
        task.title = task_in.title
    if task_in.completed is not None:
        task.completed = task_in.completed
    if task_in.due_date is not None:
        task.due_date = task_in.due_date
    await task.save()
    return task

@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(current_user: CurrentUser, lead_id: Optional[str] = None):
    filter_q = {"is_deleted": False}
    if lead_id:
        filter_q["lead_id"] = lead_id
    return await Task.find(filter_q).sort("due_date").to_list()

@router.get("/timeline/{lead_id}", response_model=List[TimelineEventResponse])
async def get_timeline(lead_id: str, current_user: CurrentUser):
    return await TimelineEvent.find(
        TimelineEvent.lead_id == lead_id
    ).sort("created_at").to_list()

@router.post("/generate-reply", response_model=GenerateReplyResponse)
async def generate_reply(request: GenerateReplyRequest, current_user: CurrentUser):
    from app.services.crm.ai import ReplyGenerationService
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
