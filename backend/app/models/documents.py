from sqlalchemy import Column, String, Text, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel

class Document(BaseModel):
    __tablename__ = "documents"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("saved_leads.id"), nullable=True, index=True)
    type = Column(String, nullable=False) # proposal, quotation, scope, contract, meeting
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False) # Markdown or HTML
    status = Column(String, default="draft")
    version = Column(Integer, default=1)

    user = relationship("User")
    lead = relationship("SavedLead")

class DocumentTemplate(BaseModel):
    __tablename__ = "document_templates"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    user = relationship("User")

class Branding(BaseModel):
    __tablename__ = "branding"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    company_name = Column(String, nullable=True)
    logo = Column(String, nullable=True)
    website = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    colors = Column(JSON, default={})
    signature = Column(Text, nullable=True)

    user = relationship("User")
