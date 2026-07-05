from typing import Optional, List
from beanie import Indexed
from app.models.base import BaseDocument


class AIChat(BaseDocument):
    user_id: Indexed(str)
    title: str = "New Chat"

    class Settings:
        name = "ai_chats"


class AIMessage(BaseDocument):
    chat_id: Indexed(str)
    role: str  # user or assistant
    message: str
    context_used: Optional[dict] = None

    class Settings:
        name = "ai_messages"


class UserPreferences(BaseDocument):
    user_id: Indexed(str, unique=True)
    preferred_tone: Optional[str] = None
    preferred_language: Optional[str] = None
    preferred_services: List[str] = []
    preferred_industries: List[str] = []
    preferred_templates: List[str] = []

    class Settings:
        name = "user_preferences"


class Branding(BaseDocument):
    user_id: Indexed(str, unique=True)
    company_name: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    colors: dict = {}
    signature: Optional[str] = None

    class Settings:
        name = "branding"
