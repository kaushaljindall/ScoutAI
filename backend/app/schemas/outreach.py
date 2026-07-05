from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class MessageGenerationRequest(BaseModel):
    message_type: str # WhatsApp, Cold Email, LinkedIn, etc.
    tone: str # Professional, Friendly, Consultative, etc.
    language: str # English, Hindi, Punjabi, Bilingual
    length: str # Short, Medium, Long
    cta_style: str # Soft, Direct, Consultative
    personalization_level: str # Basic, Medium, Deep
    user_context: Optional[dict] = None # Freelancer name, portfolio, skills

class StructuredMessageOutput(BaseModel):
    opening: str
    observation: str
    value_proposition: str
    cta: str
    closing: str

class AISuggestions(BaseModel):
    best_time: str
    recommended_channel: str
    likely_pain_points: List[str]
    recommended_service: str
    reply_probability: str
    follow_up_day: str

class MessageVariation(BaseModel):
    version: str # Version A, B, C
    message_type: str
    structured_content: StructuredMessageOutput
    full_message: str
    ai_suggestions: AISuggestions

class GenerateMessageResponse(BaseModel):
    business_id: UUID
    variations: List[MessageVariation]

class MessageTemplateBase(BaseModel):
    title: str
    type: str
    tone: str
    language: str
    template: str
    is_favorite: Optional[str] = "false"

class MessageTemplateResponse(MessageTemplateBase):
    id: UUID
    
    class Config:
        from_attributes = True
