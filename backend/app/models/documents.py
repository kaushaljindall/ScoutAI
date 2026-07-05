from typing import Optional, List
from beanie import Indexed
from app.models.base import BaseDocument


class Document(BaseDocument):
    user_id: Indexed(str)
    lead_id: Optional[str] = None
    type: str  # proposal, quotation, scope, contract, meeting
    title: str
    content: str  # Markdown or HTML
    status: str = "draft"
    version: int = 1

    class Settings:
        name = "documents"


class DocumentTemplate(BaseDocument):
    user_id: Indexed(str)
    name: str
    category: str
    content: str

    class Settings:
        name = "document_templates"
