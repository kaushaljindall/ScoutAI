from typing import Optional, List
from beanie import Indexed
from pydantic import Field
from app.models.base import BaseDocument


class MessageTemplate(BaseDocument):
    user_id: Indexed(str)
    title: str
    type: str  # email, linkedin, whatsapp
    tone: str
    language: str
    template: str
    is_favorite: bool = False

    class Settings:
        name = "message_templates"


class GeneratedMessage(BaseDocument):
    business_id: Indexed(str)
    template_id: Optional[str] = None
    message_type: str
    tone: str
    language: str
    ai_version: str  # Version A, B, C
    opening: Optional[str] = None
    observation: Optional[str] = None
    value_proposition: Optional[str] = None
    cta: Optional[str] = None
    closing: Optional[str] = None
    full_message: str
    ai_suggestions: Optional[dict] = None

    class Settings:
        name = "generated_messages"
