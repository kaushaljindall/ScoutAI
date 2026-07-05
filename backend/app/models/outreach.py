from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class MessageTemplate(BaseModel):
    __tablename__ = "message_templates"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False) # e.g., email, linkedin, whatsapp
    tone = Column(String, nullable=False)
    language = Column(String, nullable=False)
    template = Column(Text, nullable=False)
    is_favorite = Column(String, nullable=True) # boolean string or generic metadata

    user = relationship("User")

class GeneratedMessage(BaseModel):
    __tablename__ = "generated_messages"

    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False, index=True)
    template_id = Column(UUID(as_uuid=True), ForeignKey("message_templates.id"), nullable=True)
    message_type = Column(String, nullable=False)
    tone = Column(String, nullable=False)
    language = Column(String, nullable=False)
    ai_version = Column(String, nullable=False) # Version A, B, C
    
    # Structured JSON
    opening = Column(Text, nullable=True)
    observation = Column(Text, nullable=True)
    value_proposition = Column(Text, nullable=True)
    cta = Column(Text, nullable=True)
    closing = Column(Text, nullable=True)
    full_message = Column(Text, nullable=False)
    
    # Context
    ai_suggestions = Column(JSON, nullable=True) # Best time, channel, pain points

    business = relationship("Business")
    template = relationship("MessageTemplate")
