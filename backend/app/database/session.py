from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings

_client: AsyncIOMotorClient = None

def get_client() -> AsyncIOMotorClient:
    return _client

async def connect_db():
    global _client
    _client = AsyncIOMotorClient(settings.MONGODB_URI)
    
    # Import all documents for beanie initialization
    from app.models.user import User, RefreshToken, PasswordResetToken, Settings as UserSettings, AuditLog
    from app.models.scout import Business, BusinessAnalysis, SearchHistory, SavedLead
    from app.models.outreach import MessageTemplate, GeneratedMessage
    from app.models.crm import Conversation, Task, TimelineEvent
    from app.models.copilot import AIChat, AIMessage, UserPreferences, Branding
    from app.models.documents import Document, DocumentTemplate
    from app.models.analytics import Goal, AnalyticsEvent, Report

    await init_beanie(
        database=_client[settings.MONGODB_DB_NAME],
        document_models=[
            User, RefreshToken, PasswordResetToken, UserSettings, AuditLog,
            Business, BusinessAnalysis, SearchHistory, SavedLead,
            MessageTemplate, GeneratedMessage,
            Conversation, Task, TimelineEvent,
            AIChat, AIMessage, UserPreferences, Branding,
            Document, DocumentTemplate,
            Goal, AnalyticsEvent, Report,
        ]
    )

async def disconnect_db():
    global _client
    if _client:
        _client.close()
