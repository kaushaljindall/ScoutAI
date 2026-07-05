from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime

class AIChatBase(BaseModel):
    title: str

class AIChatCreate(AIChatBase):
    pass

class AIMessageBase(BaseModel):
    role: str
    message: str
    context_used: Optional[dict] = None

class AIMessageResponse(AIMessageBase):
    id: UUID
    chat_id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AIChatResponse(AIChatBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    messages: List[AIMessageResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class UserPreferenceBase(BaseModel):
    preferred_tone: Optional[str] = None
    preferred_language: Optional[str] = None
    preferred_services: List[str] = []
    preferred_industries: List[str] = []
    preferred_templates: List[str] = []

class UserPreferenceResponse(UserPreferenceBase):
    id: UUID
    user_id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class CopilotChatRequest(BaseModel):
    message: str
    chat_id: Optional[UUID] = None
    current_context: Optional[dict] = None # Passes current UI state (e.g. active lead id)

class CopilotChatResponse(BaseModel):
    chat_id: UUID
    message: AIMessageResponse
    suggested_actions: List[str] = []
    
class ContextSummary(BaseModel):
    leads_count: int
    overdue_follow_ups: int
    high_opportunity_leads: int
    unreplied_leads: int
