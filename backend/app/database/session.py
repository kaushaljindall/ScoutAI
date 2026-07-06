from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

_client: AsyncIOMotorClient = None


def get_client() -> AsyncIOMotorClient:
    return _client


async def connect_db():
    global _client
    try:
        _client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000,   # 5s timeout instead of hanging
            connectTimeoutMS=5000,
        )

        from app.models.user import User, RefreshToken, PasswordResetToken, Settings as UserSettings, AuditLog
        from app.models.scout import Business, BusinessAnalysis, SearchHistory, SavedLead
        from app.models.outreach import MessageTemplate, GeneratedMessage
        from app.models.crm import Conversation, Task, TimelineEvent, AIConversationAnalysis
        from app.models.copilot import AIChat, AIMessage, UserPreferences, Branding
        from app.models.documents import Document, DocumentTemplate
        from app.models.analytics import Goal, AnalyticsEvent, Report
        from app.models.validation import ValidatedBusiness

        await init_beanie(
            database=_client[settings.MONGODB_DB_NAME],
            document_models=[
                User, RefreshToken, PasswordResetToken, UserSettings, AuditLog,
                Business, BusinessAnalysis, SearchHistory, SavedLead,
                MessageTemplate, GeneratedMessage,
                Conversation, Task, TimelineEvent, AIConversationAnalysis,
                AIChat, AIMessage, UserPreferences, Branding,
                Document, DocumentTemplate,
                Goal, AnalyticsEvent, Report, ValidatedBusiness
            ]
        )
        logger.info(f"✅ Connected to MongoDB: {settings.MONGODB_DB_NAME}")

    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        raise


async def disconnect_db():
    global _client
    if _client:
        _client.close()
        logger.info("MongoDB disconnected")
