from pydantic import BaseModel, ConfigDict, BeforeValidator
from typing import List, Optional, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class AIChatBase(BaseModel):
    title: str

class AIChatCreate(AIChatBase):
    pass

class AIMessageBase(BaseModel):
    role: str
    message: str
    context_used: Optional[dict] = None

class AIMessageResponse(AIMessageBase):
    id: PyObjectId
    chat_id: PyObjectId
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class AIChatResponse(AIChatBase):
    id: PyObjectId
    user_id: PyObjectId
    created_at: datetime
    messages: List[AIMessageResponse] = []
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserPreferenceBase(BaseModel):
    preferred_tone: Optional[str] = None
    preferred_language: Optional[str] = None
    preferred_services: List[str] = []
    preferred_industries: List[str] = []
    preferred_templates: List[str] = []

class UserPreferenceResponse(UserPreferenceBase):
    id: PyObjectId
    user_id: PyObjectId
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class CopilotChatRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None
    current_context: Optional[dict] = None

class CopilotChatResponse(BaseModel):
    chat_id: str
    message: AIMessageResponse
    suggested_actions: List[str] = []
