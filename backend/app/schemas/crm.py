from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime
from app.schemas.scout import BusinessBase

class AIConversationAnalysisBase(BaseModel):
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    interest_level: Optional[str] = None
    objections: List[str] = []
    buying_intent: Optional[str] = None
    next_action: Optional[str] = None
    confidence_score: Optional[float] = None

class ConversationBase(BaseModel):
    type: str
    message: str
    sender: str

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: UUID
    lead_id: UUID
    created_at: datetime
    analysis: Optional[AIConversationAnalysisBase] = None
    
    model_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    title: str
    due_date: Optional[datetime] = None
    type: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: UUID
    lead_id: UUID
    completed: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TimelineEventBase(BaseModel):
    event_type: str
    description: str
    metadata_json: Optional[dict] = None

class TimelineEventResponse(TimelineEventBase):
    id: UUID
    lead_id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PipelineStatusUpdate(BaseModel):
    status: str

class GenerateReplyRequest(BaseModel):
    context: str

class GenerateReplyResponse(BaseModel):
    replies: List[str]
    ai_suggestions: Optional[dict] = None
