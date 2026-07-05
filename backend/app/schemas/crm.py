from pydantic import BaseModel, ConfigDict, BeforeValidator
from typing import List, Optional, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

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
    id: PyObjectId
    lead_id: PyObjectId
    created_at: datetime
    analysis: Optional[AIConversationAnalysisBase] = None
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class TaskBase(BaseModel):
    title: str
    due_date: Optional[datetime] = None
    type: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    type: Optional[str] = None

class TaskResponse(TaskBase):
    id: PyObjectId
    lead_id: PyObjectId
    completed: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class TimelineEventBase(BaseModel):
    event_type: str
    description: str
    metadata_json: Optional[dict] = None

class TimelineEventResponse(TimelineEventBase):
    id: PyObjectId
    lead_id: PyObjectId
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class PipelineStatusUpdate(BaseModel):
    status: str

class GenerateReplyRequest(BaseModel):
    context: str

class GenerateReplyResponse(BaseModel):
    replies: List[str]
    ai_suggestions: Optional[dict] = None
