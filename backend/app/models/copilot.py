from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class AIChat(BaseModel):
    __tablename__ = "ai_chats"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False, default="New Chat")

    user = relationship("User")
    messages = relationship("AIMessage", back_populates="chat", cascade="all, delete-orphan", order_by="AIMessage.created_at")

class AIMessage(BaseModel):
    __tablename__ = "ai_messages"

    chat_id = Column(UUID(as_uuid=True), ForeignKey("ai_chats.id"), nullable=False, index=True)
    role = Column(String, nullable=False) # user or assistant
    message = Column(Text, nullable=False)
    context_used = Column(JSON, nullable=True) # Store what context was used for this reply

    chat = relationship("AIChat", back_populates="messages")

class UserPreference(BaseModel):
    __tablename__ = "user_preferences"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    preferred_tone = Column(String, nullable=True)
    preferred_language = Column(String, nullable=True)
    preferred_services = Column(JSON, default=[])
    preferred_industries = Column(JSON, default=[])
    preferred_templates = Column(JSON, default=[])

    user = relationship("User")
