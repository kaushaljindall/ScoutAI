from typing import Optional, List
from datetime import datetime
from beanie import Indexed
from pydantic import Field
from app.models.base import BaseDocument


class Conversation(BaseDocument):
    lead_id: Indexed(str)
    type: str  # email, linkedin, whatsapp, meeting, call, note
    message: str
    sender: str  # user, lead, system
    sentiment: Optional[str] = None
    interest_level: Optional[str] = None
    buying_intent: Optional[str] = None

    class Settings:
        name = "conversations"


class AIConversationAnalysis(BaseDocument):
    conversation_id: Indexed(str, unique=True)
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    interest_level: Optional[str] = None
    objections: List[str] = []
    buying_intent: Optional[str] = None
    next_action: Optional[str] = None
    confidence_score: Optional[float] = None

    class Settings:
        name = "ai_conversation_analyses"


class Task(BaseDocument):
    lead_id: Indexed(str)
    title: str
    due_date: Optional[datetime] = None
    completed: bool = False
    type: Optional[str] = None  # call, email, meeting, custom

    class Settings:
        name = "tasks"


class TimelineEvent(BaseDocument):
    lead_id: Indexed(str)
    event_type: str
    description: str
    metadata_json: Optional[dict] = None

    class Settings:
        name = "timeline_events"
